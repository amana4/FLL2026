# Official BIOGLOW Materials

**Nothing in this repo overrides these documents.** If our notes disagree with the
official rulebook, the rulebook wins — always. When you find a conflict, fix our
notes and mention it at the next meeting.

## These files ARE committed, on purpose

By a team decision on 9 August, FIRST's materials are tracked in git so that a
clone gets everything instead of each person re-downloading them. They are
excluded from the *website* build only to keep the deploy artifact small.

Two things follow. This repo is public, so FIRST's copyrighted material is
publicly visible — a deliberate choice, not an accident. And committed binaries
live in git history permanently, so removing them later means a history rewrite
rather than a delete.

**Do not run `git rm` on them.** An earlier version of this page said they were
gitignored and that CI would block them. Both claims were wrong, and following
them would have deleted the team's materials.

Never committed: purchase paperwork (a sales order carries a billing name and
home address — `.gitignore` blocks it) and the 1.4 GB missions video, which
exceeds GitHub's 100 MB per-file limit.

## What we have

Downloaded 9 August 2026. "Mined" means the content has been extracted into our
own pages, not just skimmed.

| File | What it is | Status |
| --- | --- | --- |
| `fll-challenge-bioglow-rgr.pdf` | **Robot Game Rulebook**, 20 pp — 15 missions and all rules | Mined into [`robot-game/`](../../robot-game/README.md) |
| `fll-challenge-bioglow-rubrics-color.pdf` | The two judging rubrics plus the feedback sheet, 3 pp | Mined into [`docs/judging/`](../judging/README.md) |
| `fll-challenge-bioglow-judging-session-flowchart.pdf` | The 30-minute judging session, minute by minute | Mined into [`docs/judging/`](../judging/README.md) |
| `fll-challenge-bioglow-software-scoresheet.pdf` | The referee's scoresheet — settles every piece count | Mined into [`robot-game/`](../../robot-game/README.md) |
| `fll-challenge-bioglow-awards.pdf` | All 11 awards and how Champion's rank is calculated | Mined |
| `fll-challenge-bioglow-participation-rules.pdf` | Team size, ages, adult-help rules, consequences | Mined |
| `fll-challenge-bioglow-field-setup-reference-guide.pdf` | One page per mission showing starting positions, 17 pp | Mined |
| `fll-challenge-bioglow-wireframe-grid.pdf` | Printable A–J by 1–6 grid of 20 cm cells, for path planning | Mined |
| `fll-challenge-bioglow-en.pdf` | **The student Engineering Notebook**, 32 pp — the workbook the team writes in | Mined into [`engineering-notebook/`](../../engineering-notebook/README.md) |
| `RsaYLB-fll-challenge-bioglow-tmg.pdf` | **The coach's Team Meeting Guide**, 32 pp — the 12-session curriculum | Mined |
| `fll-challenge-bioglow-session-slide-*.pptx` | 13 ready-to-run session decks with objectives and vocabulary | Mined |
| `fll-challenge-bioglow-multimedia-resources.pdf` | Curated video and book list, session by session | Mined |
| `fll-challenge-bioglow-season-overview.pdf` | Season summary and the project brief | Mined |
| `fll-challenge-bioglow-updates.pdf` | **Challenge Updates** — supersedes the rulebook | Checked, none as of 4 Aug 2026 |
| `fll-challenge-bioglow-coach-mentor-nomination-print.pdf` | Form the **kids** fill in to nominate their coach | Mined — belongs on the packing list |
| `fll-challenge-bioglow-bi-enus-prepack.pdf` | Building instructions, 13 pp — image only, no extractable text | Needs opening in Preview |
| `guided-mission-bioglow-11.llsp3` | SPIKE Word Blocks program for Mission 11 | Inspected — a worked gyro and colour-sensor example |

Note that `fll-challenge-bioglow-en.pdf` and `RsaYLB-...-tmg.pdf` are **two
different books**, not the same one. They share a page layout; the coach guide adds
a facilitator column. An earlier version of this table conflated them.

Two files arrived with no extension (`scoresheet`, `wDan0826cn0`). They are saved
HTML pages, not documents, and are gitignored.

## Still worth getting

- [ ] **Mission Model Building Instructions.** `bi-enus-prepack.pdf` may already be
      this — open it in Preview and check before downloading again.
- [ ] Table Building Instructions, if building a practice table.

Source: <https://www.firstinspires.org/resources/library/fll/season-materials>

## Challenge Updates — check monthly

FIRST publishes rule changes after launch that **supersede the rulebook**. Teams
lose points every year practising against outdated rules.

One person checks on the 1st of each month and logs it here:

| Date checked | Version | Anything affecting us? | Checked by |
| --- | --- | --- | --- |
| 9 Aug 2026 | 4 Aug 2026 | No updates at this time | initial scaffold |

## Reading the PDFs

Open them in Preview like anything else. For extracting text — useful when you
need to quote exact scoring wording — there is a small tool in the repo:

```bash
# Build once
swiftc -O tools/pdftext.swift -o /tmp/pdftext

# Whole document, or a page range
/tmp/pdftext docs/official-materials/fll-challenge-bioglow-rgr.pdf
/tmp/pdftext docs/official-materials/fll-challenge-bioglow-rgr.pdf 9 12
```

It uses macOS PDFKit, so there is nothing to install. It cannot read image-only
PDFs such as the building instructions — there is no OCR.

## The four you will reach for most

- `fll-challenge-bioglow-rgr.pdf` — Robot Game Rulebook
- `fll-challenge-bioglow-rubrics-color.pdf` — Rubrics
- `fll-challenge-bioglow-updates.pdf` — Challenge Updates
- `fll-challenge-bioglow-field-setup-reference-guide.pdf` — Field Setup

They are files in this folder, not pages on the website, so they are listed here
rather than linked.
