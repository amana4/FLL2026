/* Persistent note boxes.
 *
 * Companion to checkbox-state.js, and it makes the same trade for the same
 * reason: localStorage, so notes work offline on a phone in a car park after
 * class with no login and no backend.
 *
 * But notes are higher stakes than ticks. A lost tick costs nothing; three
 * months of judging-day notes lost in November is unrecoverable. localStorage
 * is per browser, per device, and iOS Safari will evict it. So this file adds
 * the thing checkbox-state.js does not need: an EXPORT PATH. Every page with
 * note boxes gets Copy and Download buttons, and the page text tells students
 * to move notes somewhere real.
 *
 * Treat a note box as a pocket notebook, not a filing cabinet.
 *
 * Markup, in any published page (md_in_html is enabled in mkdocs.yml):
 *
 *   <div class="fll-note" data-note="unique-id" data-label="Heading shown"></div>
 *
 * data-note must be unique within the page; it is half the storage key, so
 * renaming it orphans whatever was already typed there.
 */

(function () {
  "use strict";

  var PREFIX = "fll-note:";
  var SAVE_DELAY_MS = 400;

  function keyFor(id) {
    return PREFIX + window.location.pathname + "#" + id;
  }

  function holders() {
    return document.querySelectorAll(".md-typeset .fll-note[data-note]");
  }

  function timeNow() {
    var d = new Date();
    var hh = String(d.getHours()).padStart(2, "0");
    var mm = String(d.getMinutes()).padStart(2, "0");
    return hh + ":" + mm;
  }

  function autosize(box) {
    box.style.height = "auto";
    box.style.height = Math.max(box.scrollHeight, 90) + "px";
  }

  /* mkdocs.yml sets toc.permalink, which injects an anchor link inside every
     heading. Reading textContent would drag that character into the export, so
     clone the heading and drop the anchor first. */
  function headingText(heading) {
    if (!heading) return "";
    var copy = heading.cloneNode(true);
    copy.querySelectorAll(".headerlink").forEach(function (a) {
      a.remove();
    });
    return copy.textContent.trim();
  }

  function build(holder) {
    if (holder.dataset.fllBuilt) return;
    holder.dataset.fllBuilt = "1";

    var id = holder.dataset.note;
    var label = holder.dataset.label || id;

    var wrap = document.createElement("div");
    wrap.className = "fll-note-wrap";

    var caption = document.createElement("label");
    caption.className = "fll-note-label";
    caption.textContent = label;

    var box = document.createElement("textarea");
    box.className = "fll-note-box";
    box.setAttribute("rows", "4");
    box.setAttribute("spellcheck", "true");
    box.placeholder = "Type here. Saves as you go, in this browser only.";

    var status = document.createElement("span");
    status.className = "fll-note-status";

    try {
      var saved = localStorage.getItem(keyFor(id));
      if (saved !== null) {
        box.value = saved;
        status.textContent = "Saved earlier";
      }
    } catch (e) {
      status.textContent = "This browser will not save notes (private mode?)";
    }

    var timer = null;
    box.addEventListener("input", function () {
      autosize(box);
      status.textContent = "Typing…";
      if (timer) clearTimeout(timer);
      timer = setTimeout(function () {
        try {
          localStorage.setItem(keyFor(id), box.value);
          status.textContent = "Saved at " + timeNow();
        } catch (e) {
          status.textContent = "Could not save. Copy this text somewhere safe.";
        }
      }, SAVE_DELAY_MS);
    });

    caption.appendChild(box);
    wrap.appendChild(caption);
    wrap.appendChild(status);
    holder.appendChild(wrap);

    // Height is wrong until the element is laid out, so size after insertion.
    autosize(box);
  }

  /* Collect every note on the page as plain text, ready to paste into the
     meeting log, the design log, or the shared Drive folder. */
  function collect() {
    var parts = [];
    var heading = document.querySelector(".md-typeset h1");
    parts.push(headingText(heading) || document.title.trim());
    parts.push("Notes exported " + new Date().toString());
    parts.push("");

    holders().forEach(function (holder) {
      var box = holder.querySelector(".fll-note-box");
      if (!box || !box.value.trim()) return;
      parts.push("## " + (holder.dataset.label || holder.dataset.note));
      parts.push(box.value.trim());
      parts.push("");
    });

    if (parts.length <= 3) return null; // nothing typed yet
    return parts.join("\n");
  }

  function flash(button, message) {
    var original = button.textContent;
    button.textContent = message;
    setTimeout(function () {
      button.textContent = original;
    }, 1800);
  }

  function addToolbar() {
    if (!holders().length) return;
    if (document.querySelector(".fll-note-tools")) return;

    var bar = document.createElement("div");
    bar.className = "fll-note-tools";

    var copy = document.createElement("button");
    copy.type = "button";
    copy.className = "fll-note-btn";
    copy.textContent = "Copy all notes on this page";
    copy.addEventListener("click", function () {
      var text = collect();
      if (!text) {
        flash(copy, "Nothing typed yet");
        return;
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(
          function () { flash(copy, "Copied. Now paste it somewhere safe."); },
          function () { flash(copy, "Copy failed — use Download instead"); }
        );
      } else {
        flash(copy, "Copy unavailable — use Download instead");
      }
    });

    var save = document.createElement("button");
    save.type = "button";
    save.className = "fll-note-btn";
    save.textContent = "Download as a text file";
    save.addEventListener("click", function () {
      var text = collect();
      if (!text) {
        flash(save, "Nothing typed yet");
        return;
      }
      var stamp = new Date().toISOString().slice(0, 10);
      var blob = new Blob([text], { type: "text/plain;charset=utf-8" });
      var url = URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url;
      a.download = "fll-notes-" + stamp + ".txt";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      flash(save, "Downloaded");
    });

    var warn = document.createElement("p");
    warn.className = "fll-note-warning";
    warn.textContent =
      "Important: these notes live in this browser only. They are not shared " +
      "with the team, and clearing your history or using a different device " +
      "loses them. Before judging day, copy them into the meeting log or the " +
      "team Drive folder.";

    bar.appendChild(copy);
    bar.appendChild(save);
    bar.appendChild(warn);

    var last = holders()[holders().length - 1];
    if (last && last.parentNode) {
      last.parentNode.insertBefore(bar, last.nextSibling);
    }
  }

  function init() {
    holders().forEach(build);
    addToolbar();
  }

  if (document.readyState !== "loading") {
    init();
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }

  // navigation.instant swaps page content without a reload, so re-bind.
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  }
})();
