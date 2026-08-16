# Code — SPIKE Prime Python

For the 2026 season we program in **Python**, not Word Blocks. Last season's
team (`code/2025-reference/`) had solid, tuned Python on the SPIKE App's native
Python canvas, and unlike a `.llsp3` file, git can actually diff a `.py` file —
so changes review properly instead of relying on screenshots.

```
code/
  library/           Shared movement code — toolkit.py, imported by every mission
  missions/           One folder per mission, matching robot-game/missions/
  2025-reference/     Last season's code, kept for reuse (excluded from the site)
  spike-projects/     Word Blocks .llsp3 files from earlier in the season, and my-blocks.md
  screenshots/        PNG block-stack images from the Word Blocks period
```

## Workflow

1. Design the approach on the mission's page in `robot-game/missions/`.
2. Fill in `run()` in that mission's `code/missions/MXX-name/mission.py`,
   using `library/toolkit.py` for driving and turning.
3. Before loading onto the hub: paste `toolkit.py`'s contents above the
   `import` line in the mission file — the SPIKE App's Python canvas runs one
   self-contained file per slot and can't import across files. See
   [`code/missions/README.md`](missions/README.md).
4. Test on the hub, iterate, then commit with a message saying *what changed
   and why*: `M07: slow approach speed to 30% — was overshooting the drop zone`.

## Naming

| Thing | Pattern | Example |
| --- | --- | --- |
| Mission program | `code/missions/MXX-slug/mission.py` | `code/missions/M07-humongous-fungus/mission.py` |
| Shared library | `code/library/toolkit.py` | |

## Earlier this season: Word Blocks

`spike-projects/`, `screenshots/`, and `my-blocks.md` document work from when
the team was on Word Blocks, before switching to Python. Kept as the record of
that — the Robot Design rubric's ITERATE criterion rewards showing what
changed and why, and a documented switch is exactly that.

## Before a tournament

- [ ] All programs loaded onto the hub **in match order** (slots 0, 1, 2, …)
- [ ] Slot order matches [`../robot-game/strategy.md`](../robot-game/strategy.md)
- [ ] Hub name set to our team name
- [ ] Programs tested on the hub after loading, not just in the app
- [ ] A second hub loaded identically as a backup, if we have one
- [ ] Each mission's code in `code/missions/` matches what's actually loaded on
      the hub (including any manual toolkit paste-in — see
      [`code/missions/README.md`](missions/README.md))

That last one matters: if the hub gets wiped at the tournament, this folder is the
only way back.

--8<-- "includes/abbreviations.md"
