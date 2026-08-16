# Working notes for Claude

## Writing style

No emojis. Anywhere: documents, WhatsApp or email drafts, commit messages,
tables, headings. Use words, bold, or plain text markers instead.

Write like a person, not a content generator:

- Start with the substance. No "Great news!" or "Here's everything you need."
- Normal sentences and paragraphs, not stacked one-line fragments.
- Warnings read "Important:" or "Note:", not warning symbols.
- Plain numbers or dashes for lists, never numbered emoji.
- Say the thing once. Don't restate a point in a callout box after making it.

Exception: the ballot-box character used as a checkbox in table cells, and the
box-drawing characters in ASCII diagrams, are functional rather than decorative.
Those stay.

## About this repo

Team workspace for the FLL 2026-27 BIOGLOW season. The theme is biodiversity.

Five kids. Meetings are Sundays 11:00 to 12:30 and Wednesdays 18:00 to 19:30,
running from 9 August 2026 to the competition in early November. 26 sessions.

The audience is students aged roughly 9 to 14, their parents, and coaches. Some
have never used git. Write for them, not for engineers.

## Ground rules

The official FIRST materials in `docs/official-materials/` are the only
authority on missions, points, and rules. If a repo document contradicts them,
the PDFs win. Extract from them rather than working from memory. Text extraction
works via macOS PDFKit and a small Swift helper; there is no `pdftotext` or
`poppler` on this machine and no network access to install one.

Source page for the materials:
https://www.firstinspires.org/resources/library/fll/season-materials

Nothing published to the website may contain students' names or contact details,
with one deliberate exception: on 15 August 2026 the coach decided the
after-class notes form may identify its author by **first name**, and that form
is embedded on the public `docs/after-class-notes.md` page, so those first names
are public and search-indexable. That was a considered call, not an oversight —
do not "fix" it back.

Everything else still holds. Surnames, grades, contact details and photos of
students stay off the site. `docs/team-roster.md` is deliberately excluded from
the site build in `mkdocs.yml`, and CI fails if that exclusion is removed.
Markdown files in the repo still use the `Kid 1` to `Kid 5` labels rather than
names, because those pages get committed and printed and there is no reason to
widen the exposure further.

The site is MkDocs Material, published to GitHub Pages from `main`. Every markdown
link must point at a real `.md` file — link `dir/README.md` explicitly rather than
`dir/`, because MkDocs reports a bare directory link as unrecognized and
`validation.unrecognized_links` is set to `warn`, which `strict: true` turns into a
build failure.

Run `python3 tools/check-links.py` before pushing. It catches two things
`mkdocs build --strict` misses: broken in-page anchors, and published pages linking
to pages that `exclude_docs` keeps off the site.

`exclude_docs` keeps a file off the website. `.gitignore` keeps it out of the repo,
which is the only real privacy mechanism. `not_in_nav` does neither — it only
silences a warning, and the file stays published. Confusing the last two put
internal notes on the public site for a day.

## Lessons learned the hard way

**Bulk find-and-replace.** Do not use regex character ranges for Unicode.
Enumerate the exact characters present first, then substitute only those. A stray
character inside a class once stripped every digit "2" from every file in the repo,
turning 2026 into 06. Always grep a known string afterwards, and revert rather than
patch if the result is wrong.

**Editing `mkdocs.yml` by string index.** `cfg.index('nav:')` matches inside
`not_in_nav:` and will truncate the file from the wrong place, destroying
`exclude_docs` and `not_in_nav`. Use an anchored regex (`re.search(r'^nav:', s,
re.M)`) and check the YAML still parses and still has every top-level key
afterwards.

**Inserting rows into `docs/team-fund.csv`.** Every `=SUM()` range and every
summary cell reference shifts. Recompute the ranges from measured row positions
rather than editing them by hand, then verify each formula against the row it
should cover.

