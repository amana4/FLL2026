#!/usr/bin/env node
/*
 * Renders tools/bee-data.js against fake data, with a minimal stub DOM.
 *
 * The chart only ever ran in a browser, and two bugs reached the coach that way:
 * a crash on an old endpoint response, and `Math.apply` for `Math.max.apply`.
 * Neither needed a browser to catch. This does not check that the chart looks
 * right — open the page for that — only that every path runs without throwing.
 *
 * Usage:
 *   node tools/check-bee-data.js
 */

"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const SRC = path.join(__dirname, "bee-data.js");

// --- the smallest DOM the script actually touches ------------------------
function makeNode(tag) {
  return {
    tagName: tag,
    children: [],
    attributes: {},
    style: {},
    _text: "",
    set textContent(v) { this._text = String(v); this.children.length = 0; },
    get textContent() { return this._text; },
    set className(v) { this.attributes.class = v; },
    get className() { return this.attributes.class || ""; },
    setAttribute(k, v) { this.attributes[k] = String(v); },
    getAttribute(k) { return this.attributes[k]; },
    appendChild(c) { this.children.push(c); return c; }
  };
}

function countTags(node, out) {
  out = out || {};
  out[node.tagName] = (out[node.tagName] || 0) + 1;
  node.children.forEach(function (c) { countTags(c, out); });
  return out;
}

function run(payload, label) {
  const mount = makeNode("div");
  const head = makeNode("head");

  const document = {
    head: head,
    readyState: "complete",
    getElementById: function (id) { return id === "bee-data" ? mount : null; },
    createElement: makeNode,
    createElementNS: function (ns, tag) { return makeNode(tag); },
    addEventListener: function () {}
  };

  const sandbox = {
    document: document,
    window: {},
    console: console,
    Math: Math,
    Number: Number,
    String: String,
    Object: Object,
    Array: Array,
    fetch: function () {
      return Promise.resolve({ json: function () { return Promise.resolve(payload); } });
    }
  };
  sandbox.window.document = document;
  sandbox.globalThis = sandbox;

  vm.createContext(sandbox);
  vm.runInContext(fs.readFileSync(SRC, "utf8"), sandbox, { filename: "bee-data.js" });

  // The script's fetch chain is async; let the microtasks drain.
  return new Promise(function (resolve) { setTimeout(resolve, 0); }).then(function () {
    const text = JSON.stringify(mount).toLowerCase();
    const tags = countTags(mount);
    const broke = text.indexOf("could not load") >= 0;
    return { label: label, tags: tags, broke: broke, mount: mount };
  });
}

// --- cases ---------------------------------------------------------------
const CASES = [
  ["no counts yet", { ok: true, sessions: [], totals: { sessions: 0, groups: 0, wild: 0, honeybees: 0 } }, false],
  ["one count", {
    ok: true,
    sessions: [{ date: "2026-09-14", groups: 1, wild: 1, honeybees: 2, who: ["Kid 1"] }],
    totals: { sessions: 1, groups: 1, wild: 1, honeybees: 2 }
  }, true],
  ["several counts", {
    ok: true,
    sessions: [
      { date: "2026-09-20", groups: 4, wild: 31, honeybees: 12, who: ["Kid 1", "Kid 2"] },
      { date: "2026-09-27", groups: 5, wild: 28, honeybees: 9, who: ["Kid 3"] },
      { date: "2026-10-04", groups: 7, wild: 30, honeybees: 7, who: ["Kid 2"] }
    ],
    totals: { sessions: 3, groups: 7, wild: 89, honeybees: 28 }
  }, true],
  ["all zero groups", {
    ok: true,
    sessions: [{ date: "2026-09-14", groups: 0, wild: 0, honeybees: 0, who: [] }],
    totals: { sessions: 1, groups: 0, wild: 0, honeybees: 0 }
  }, true],
  ["missing who", {
    ok: true,
    sessions: [{ date: "2026-09-14", groups: 2, wild: 3, honeybees: 0 }],
    totals: { sessions: 1, groups: 2, wild: 3, honeybees: 0 }
  }, true],
  // The two shapes that actually broke in the wild.
  ["old deployment", { ok: true, message: "Bee field log endpoint. POST to it." }, false],
  ["script error", { ok: false, error: "not set up yet" }, false]
];

(async function () {
  let failures = 0;
  for (const [label, payload, wantChart] of CASES) {
    let result;
    try {
      result = await run(payload, label);
    } catch (err) {
      console.log(`  FAIL  ${label}: threw ${err.message}`);
      failures++;
      continue;
    }
    const bars = result.tags.rect || 0;
    const rows = result.tags.tr || 0;
    if (wantChart && bars === 0) {
      console.log(`  FAIL  ${label}: expected bars, drew none`);
      failures++;
    } else if (!wantChart && !result.broke && bars > 0) {
      console.log(`  FAIL  ${label}: drew a chart from data it should have rejected`);
      failures++;
    } else {
      console.log(`  ok    ${label.padEnd(18)} bars ${bars}  table rows ${rows}`
        + (result.broke ? "  (showed the error message)" : ""));
    }
  }
  console.log("");
  if (failures) {
    console.log(`${failures} of ${CASES.length} cases failed`);
    process.exit(1);
  }
  console.log(`all ${CASES.length} cases rendered`);
})();
