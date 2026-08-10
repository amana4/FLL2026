/* Persist checkbox state.
 *
 * The site has roughly 700 checkboxes across the meeting plans, mission pages,
 * packing lists and judging prep sheets, and the meeting plan describes itself as
 * "the season's progress tracker". Material renders markdown task lists as
 * disabled inputs by default, so before this they did nothing when tapped and
 * remembered nothing — the tracking premise was false. clickable_checkbox in
 * mkdocs.yml makes them tappable; this file makes them stick.
 *
 * Deliberately simple:
 *   - localStorage, so it works offline and needs no login or backend
 *   - per device and per browser, which is the honest trade for zero setup
 *   - keyed by page path plus checkbox index
 *
 * Consequence worth knowing: state is NOT shared between people. Two coaches
 * ticking on two phones see different views. Anything the whole team must agree
 * on belongs in a committed markdown edit or the shared spreadsheet, not here.
 * The page footer says so.
 */

(function () {
  "use strict";

  var PREFIX = "fll-check:";

  function keyFor(index) {
    return PREFIX + window.location.pathname + "#" + index;
  }

  function boxes() {
    return document.querySelectorAll(".md-typeset .task-list-item input[type=checkbox]");
  }

  function restore() {
    boxes().forEach(function (box, index) {
      var saved = localStorage.getItem(keyFor(index));
      if (saved !== null) {
        box.checked = saved === "1";
      }
      box.disabled = false;

      if (!box.dataset.fllBound) {
        box.dataset.fllBound = "1";
        box.addEventListener("change", function () {
          try {
            localStorage.setItem(keyFor(index), box.checked ? "1" : "0");
          } catch (e) {
            /* Private browsing or a full quota. Ticking still works for the
               session; it just will not survive a reload. */
          }
        });
      }
    });
  }

  function addResetControl() {
    var list = document.querySelector(".md-typeset ul.task-list");
    if (!list || document.querySelector(".fll-reset")) return;

    var note = document.createElement("p");
    note.className = "fll-reset";
    note.style.cssText = "font-size:.72rem;opacity:.65;margin-top:1.2em";

    var link = document.createElement("a");
    link.href = "#";
    link.textContent = "Clear the ticks on this page";
    link.addEventListener("click", function (event) {
      event.preventDefault();
      boxes().forEach(function (box, index) {
        localStorage.removeItem(keyFor(index));
        box.checked = false;
      });
    });

    note.appendChild(link);
    note.appendChild(document.createTextNode(
      ". Ticks are saved in this browser only, so they are not shared with the rest of the team."
    ));

    var content = document.querySelector(".md-content__inner");
    if (content) content.appendChild(note);
  }

  function init() {
    restore();
    addResetControl();
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
