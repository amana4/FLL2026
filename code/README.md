# Code — SPIKE Prime Word Blocks

We program in **Word Blocks** (SPIKE's visual language), not Python. Git can't
diff a `.llsp3` file, so our workflow trades automatic diffing for screenshots and
good commit messages.

```
code/
  spike-projects/    Exported .llsp3 files — the real programs
  screenshots/       PNG of each program's blocks — how we review changes
  my-blocks.md       The shared reusable blocks, documented
```

## Workflow

Follow this every time you change a program:

1. Edit in the SPIKE app as normal.
2. **Export** the project: `File → Save to computer` → save into `code/spike-projects/`
   as `RX-name.llsp3` (same name as its run file).
3. **Screenshot** the full block stack → `code/screenshots/RX-name.png`.
   Scroll and take multiple images if it doesn't fit on one screen
   (`RX-name-1.png`, `RX-name-2.png`).
4. Commit both together with a message saying *what changed and why*:
   `R2: slow approach speed to 30% — was overshooting the drop zone`

The screenshot is what teammates actually review — nobody can read a `.llsp3` in a
pull request. Skipping it means the change is invisible to everyone else.

## Naming

| Thing | Pattern | Example |
| --- | --- | --- |
| Run program | `RX-name` | `R2-cargo-line.llsp3` |
| Screenshot | `RX-name.png` | `R2-cargo-line.png` |
| Test / scratch program | `test-thing` | `test-gyro-drift.llsp3` |

Test programs are fine to commit — they document experiments. Delete them once the
lesson is captured in a run file or in `my-blocks.md`.

## Before a tournament

- [ ] All programs loaded onto the hub **in match order** (slots 0, 1, 2, …)
- [ ] Slot order matches [`../robot-game/strategy.md`](../robot-game/strategy.md)
- [ ] Hub name set to our team name
- [ ] Programs tested on the hub after loading, not just in the app
- [ ] A second hub loaded identically as a backup, if we have one
- [ ] `.llsp3` files in this folder match what's on the hub

That last one matters: if the hub gets wiped at the tournament, this folder is the
only way back.
