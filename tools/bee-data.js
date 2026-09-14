/*
 * bee-data.js — the counts so far, on innovation-project/bee-data.md.
 *
 * Fetches a summary from the Apps Script endpoint in
 * tools/create-field-log-sheet.gs and draws it. The endpoint returns a summary,
 * never the rows: no garden locations, no plant names, no descriptions. See the
 * doGet comment in that file for why.
 *
 * Does nothing at all unless the page has a #bee-data element, so it costs
 * other pages one function call.
 *
 * Chart decisions, for anyone changing it:
 *   Form is change-over-time on one measure, so a bar per session. The headline
 *   measure is the number of different wild bee GROUPS, because that is what
 *   field-protocol.md defines as the diversity score. Visitor counts live in the
 *   table rather than a second series, because groups and visitors are different
 *   scales and a second y-axis is never the answer.
 *   One series, so no legend: the title names it. Every bar is directly labelled.
 *   Colour is #008300, which passes contrast on both the light and dark chart
 *   surfaces.
 */

(function () {
  "use strict";

  var ENDPOINT = "https://script.google.com/macros/s/AKfycbzN1qofXvcJOX7y-qUzxDJB1lgY5naMWkbngvGzgnuoGZ0CATdVVWf-ek0Pw2P5B04M/exec";

  var CSS = [
    ".viz-root{color-scheme:light;--surface-1:#fcfcfb;--text-primary:#0b0b0b;",
    "  --text-secondary:#52514e;--series-1:#008300;--rule:rgba(11,11,11,.14)}",
    "@media (prefers-color-scheme: dark){",
    "  [data-md-color-scheme=slate] .viz-root{color-scheme:dark;--surface-1:#1a1a19;",
    "  --text-primary:#fff;--text-secondary:#c3c2b7;--series-1:#008300;",
    "  --rule:rgba(255,255,255,.16)}}",
    "[data-md-color-scheme=slate] .viz-root{color-scheme:dark;--surface-1:#1a1a19;",
    "  --text-primary:#fff;--text-secondary:#c3c2b7;--series-1:#008300;",
    "  --rule:rgba(255,255,255,.16)}",
    ".viz-root{background:var(--surface-1);border:1px solid var(--rule);",
    "  border-radius:.3rem;padding:1rem 1.1rem 1.2rem;margin:1rem 0}",
    ".viz-tiles{display:flex;flex-wrap:wrap;gap:1.6rem;margin-bottom:1.2rem}",
    ".viz-tile .n{font-size:1.9rem;font-weight:700;line-height:1.1;",
    "  color:var(--text-primary)}",
    ".viz-tile .l{font-size:.62rem;letter-spacing:.09em;text-transform:uppercase;",
    "  color:var(--text-secondary)}",
    ".viz-title{font-size:.78rem;font-weight:700;color:var(--text-primary);margin:0 0 .1rem}",
    ".viz-sub{font-size:.66rem;color:var(--text-secondary);margin:0 0 .7rem}",
    ".viz-chart{width:100%;height:auto;display:block;overflow:visible}",
    ".viz-note{font-size:.66rem;color:var(--text-secondary);margin:.6rem 0 0}",
    ".viz-root table{font-size:.7rem;margin:.9rem 0 0}",
    ".viz-bar{transition:opacity .12s}",
    ".viz-root g:hover .viz-bar{opacity:.78}"
  ].join("");

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) { n.className = cls; }
    if (text !== undefined) { n.textContent = text; }
    return n;
  }

  function tile(parent, n, label) {
    var t = el("div", "viz-tile");
    t.appendChild(el("div", "n", String(n)));
    t.appendChild(el("div", "l", label));
    parent.appendChild(t);
  }

  function shortDate(iso) {
    var p = String(iso).split("-");
    if (p.length !== 3) { return iso; }
    var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    return Number(p[2]) + " " + (months[Number(p[1]) - 1] || p[1]);
  }

  // Bars: 4px rounded top corners, anchored to the baseline, 2px gap between
  // neighbours, every bar directly labelled because there is only one series.
  function chart(sessions) {
    var W = 760, H = 260, padL = 34, padR = 12, padT = 26, padB = 44;
    var plotW = W - padL - padR, plotH = H - padT - padB;
    var max = Math.max(4, Math.apply(null, sessions.map(function (s) { return s.groups; })));
    var step = plotW / sessions.length;
    var bw = Math.min(56, Math.max(10, step - 14));

    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    svg.setAttribute("class", "viz-chart");
    svg.setAttribute("role", "img");
    svg.setAttribute("aria-label",
      "Different wild bee groups seen at each count, " + sessions.length + " counts");

    function add(tag, attrs, text) {
      var n = document.createElementNS("http://www.w3.org/2000/svg", tag);
      for (var k in attrs) { n.setAttribute(k, attrs[k]); }
      if (text !== undefined) { n.textContent = text; }
      svg.appendChild(n);
      return n;
    }

    // Recessive gridlines and a baseline.
    var ticks = Math.min(max, 5);
    for (var i = 0; i <= ticks; i++) {
      var v = Math.round(max * i / ticks);
      var y = padT + plotH - (v / max) * plotH;
      add("line", { x1: padL, x2: W - padR, y1: y, y2: y,
                    stroke: "var(--rule)", "stroke-width": 1 });
      add("text", { x: padL - 8, y: y + 4, "text-anchor": "end",
                    "font-size": 11, fill: "var(--text-secondary)" }, String(v));
    }

    sessions.forEach(function (s, i) {
      var x = padL + i * step + (step - bw) / 2;
      var h = (s.groups / max) * plotH;
      var y = padT + plotH - h;
      var g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      svg.appendChild(g);

      var rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      rect.setAttribute("x", x);
      rect.setAttribute("y", h > 0 ? y : padT + plotH - 1);
      rect.setAttribute("width", bw);
      rect.setAttribute("height", Math.max(h, 1));
      rect.setAttribute("rx", 4);
      rect.setAttribute("fill", "var(--series-1)");
      rect.setAttribute("class", "viz-bar");
      g.appendChild(rect);

      var title = document.createElementNS("http://www.w3.org/2000/svg", "title");
      title.textContent = shortDate(s.date) + ": " + s.groups + " groups, "
        + s.wild + " wild visitors, " + s.honeybees + " honeybees";
      g.appendChild(title);

      add("text", { x: x + bw / 2, y: y - 7, "text-anchor": "middle",
                    "font-size": 12, "font-weight": 700,
                    fill: "var(--text-primary)" }, String(s.groups));
      add("text", { x: x + bw / 2, y: padT + plotH + 18, "text-anchor": "middle",
                    "font-size": 11, fill: "var(--text-secondary)" },
          shortDate(s.date));
    });

    return svg;
  }

  function table(sessions) {
    var t = el("table");
    var head = el("thead");
    var hr = el("tr");
    ["Count", "Bee groups", "Wild visitors", "Honeybees", "Who counted"]
      .forEach(function (h) { hr.appendChild(el("th", null, h)); });
    head.appendChild(hr);
    t.appendChild(head);
    var body = el("tbody");
    sessions.forEach(function (s) {
      var tr = el("tr");
      [shortDate(s.date), s.groups, s.wild, s.honeybees, (s.who || []).join(", ")]
        .forEach(function (c) { tr.appendChild(el("td", null, String(c))); });
      body.appendChild(tr);
    });
    t.appendChild(body);
    return t;
  }

  function render(mount, data) {
    mount.textContent = "";
    var root = el("div", "viz-root");

    var tiles = el("div", "viz-tiles");
    tile(tiles, data.totals.sessions, "counts done");
    tile(tiles, data.totals.groups, "different bee groups");
    tile(tiles, data.totals.wild, "wild bees seen");
    tile(tiles, data.totals.honeybees, "honeybees seen");
    root.appendChild(tiles);

    if (!data.sessions.length) {
      root.appendChild(el("p", "viz-note",
        "No counts yet. The first one will appear here within a minute of being sent."));
      mount.appendChild(root);
      return;
    }

    root.appendChild(el("p", "viz-title", "Different wild bee groups, each count"));
    root.appendChild(el("p", "viz-sub",
      "This is the diversity score. More groups means more kinds of bee, "
      + "which is what the project is trying to change."));
    root.appendChild(chart(data.sessions));
    root.appendChild(el("p", "viz-note",
      "Honeybees are counted but left out of this score, because they are kept "
      + "livestock rather than wild. The table has them."));
    root.appendChild(table(data.sessions));
    mount.appendChild(root);
  }

  function load() {
    var mount = document.getElementById("bee-data");
    if (!mount) { return; }
    mount.textContent = "Loading the counts...";
    fetch(ENDPOINT, { method: "GET" })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (!data || !data.ok) { throw new Error(data && data.error ? data.error : "no data"); }
        render(mount, data);
      })
      .catch(function (err) {
        mount.textContent = "";
        var p = el("p", "viz-note",
          "Could not load the counts (" + err.message + "). "
          + "The data is still safe in the team sheet. Try reloading.");
        mount.appendChild(p);
      });
  }

  var style = document.createElement("style");
  style.textContent = CSS;
  document.head.appendChild(style);

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(load);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", load);
  } else {
    load();
  }
})();
