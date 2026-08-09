# Official BIOGLOW Materials

**Nothing in this repo overrides these documents.** If our notes disagree with
the official rulebook, the rulebook wins — always. When you find a conflict, fix
our notes and mention it at the next meeting.

> 🔒 **These files are gitignored and must stay that way.** They're FIRST's
> copyrighted material and this repo is public. `.gitignore` allowlists only
> this README; the CI build fails if anything else here gets committed. They
> live on team members' computers, not on GitHub.

## What we have (downloaded 9 Aug 2026)

| File | What it is | Read? |
| --- | --- | --- |
| `fll-challenge-bioglow-rgr.pdf` | **Robot Game Rulebook** — 15 missions, all rules | ✅ extracted into [`robot-game/`](../../robot-game/README.md) |
| `fll-challenge-bioglow-rubrics-color.pdf` | The judging rubrics | ✅ extracted into [`docs/judging/`](../judging/README.md) |
| `fll-challenge-bioglow-updates.pdf` | **Challenge Updates** | ✅ no updates as of 4 Aug 2026 |
| `fll-challenge-bioglow-season-overview.pdf` | Season summary, project brief | ✅ |
| `fll-challenge-bioglow-en.pdf` / `RsaYLB-...-tmg.pdf` | Team Meeting Guide (32 pp) — session plans | ☐ |
| `fll-challenge-bioglow-field-setup-reference-guide.pdf` | Field setup | ☐ |
| `fll-challenge-bioglow-participation-rules.pdf` | Participation rules | ☐ |
| `fll-challenge-bioglow-awards.pdf` | Award descriptions | ☐ |
| `fll-challenge-bioglow-judging-session-flowchart.pdf` | How judging runs | ☐ |
| `fll-challenge-bioglow-software-scoresheet.pdf` | Scoresheet | ☐ |
| `fll-challenge-bioglow-wireframe-grid.pdf` | Mat wireframe for model placement | ☐ |
| `fll-challenge-bioglow-multimedia-resources.pdf` | Links to videos | ☐ |
| `fll-challenge-bioglow-session-slide-*.pptx` | 13 meeting slide decks | ☐ |
| `fll-challenge-bioglow-robot-game-missions.mp4` | Missions video (1.4 GB) | ☐ |
| `guided-mission-bioglow-11.llsp3` | SPIKE guided program for Mission 11 | ☐ |

Two files came down with no extension (`scoresheet`, `wDan0826cn0`) and are
HTML, not documents — safe to delete.

## Still worth downloading

- [ ] **Mission Model Building Instructions** — needed to build the field
- [ ] Engineering Notebook template
- [ ] Table Building Instructions (if building a practice table)

Source: <https://www.firstinspires.org/resources/library/fll/season-materials>

## Challenge Updates — check monthly

FIRST publishes rule changes after launch that **supersede the rulebook**. Teams
lose points every year practicing against outdated rules.

Assign one person to check on the 1st of each month:

| Date checked | Version | Anything affecting us? | Checked by |
| --- | --- | --- | --- |
| 9 Aug 2026 | 4 Aug 2026 | No updates at this time | _initial scaffold_ |

## Reading PDFs

macOS ships PDFKit, so no install is needed. The team can just open them in
Preview. For text extraction (useful for quoting exact scoring wording):

```bash
# Build once
swiftc -O /tmp/pdftext.swift -o /tmp/pdftext
# Then
/tmp/pdftext docs/official-materials/fll-challenge-bioglow-rgr.pdf 9 12
```

## The four you'll reach for most

These live in this folder on your computer. They're deliberately **not** linked
as pages — the website can't serve them, and the build fails if it tries.

- `fll-challenge-bioglow-rgr.pdf` — Robot Game Rulebook
- `fll-challenge-bioglow-rubrics-color.pdf` — Rubrics
- `fll-challenge-bioglow-updates.pdf` — Challenge Updates
- `fll-challenge-bioglow-field-setup-reference-guide.pdf` — Field Setup
