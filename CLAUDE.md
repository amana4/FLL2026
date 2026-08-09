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

Nothing published to the website may contain students' names or contact details.
`docs/team-roster.md` is deliberately excluded from the site build in
`mkdocs.yml`, and CI fails if that exclusion is removed.

The site is MkDocs Material, published to GitHub Pages from `main`. Every
markdown link must point at a real `.md` file or at a directory containing a
`README.md`, because the build runs `--strict` and a broken link fails CI.

## Lessons learned the hard way

When doing a bulk find-and-replace across many files, do not use regex character
ranges for Unicode. Enumerate the exact characters present first, then substitute
only those. A stray character inside a class once stripped every digit "2" from
every file in the repo, turning 2026 into 06. Always sanity-check a known string
afterwards and revert rather than patch if the result is wrong.
