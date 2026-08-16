# 2025 season reference code

Carried over from last year's repo (`FLL2025`) for reference while building this
season's code. **Not excluded from git, but excluded from the published site**
in `mkdocs.yml` — none of this is meant to be read as a documentation page.

One change was made to the copies: the same attribution comment named a student
in `Missions/Mission 3/mission3.py` and in `Missions/Mission 3-10/mission 3-10.py`
(the second was built from the first). This repo is public and git history is
permanent, so the name was replaced in both. Otherwise the files are
byte-for-byte last season's.

Worth knowing if you ever run that check yourself: in `FLL2025` the second file
had no `.py` extension, so a `grep --include="*.py"` misses it. Scan with no
extension filter.

```
Library/toolKit.py            Last year's shared movement library — the real asset here
Essentials/Pybricks/          Early experiments on Pybricks, a different (third-party)
                               firmware — not compatible with toolKit.py's API, kept for history
Missions/                     Last year's per-mission programs. Each one pastes in its own
                               copy of the toolkit rather than importing it — that's how the
                               SPIKE App's Python canvas required it, not a mistake.
```

## Two things worth deciding before reusing this

**1. This is a different Python API than `code/spike-projects/Acceleration.py`.**
`toolKit.py` is written against the SPIKE App 3.5 native Python API — `from hub
import port, motion_sensor`, `motor_pair`, `motor`, `runloop`, all `async`/`await`.
That's confirmed working, because it's what the team actually ran on hardware
last season. `Acceleration.py` (this year's port of the Acceleration My Block)
used the older `spike` module (`PrimeHub`, `Motor`, `MotorPair`) instead — a
different, earlier API. If `Acceleration.py` doesn't behave like the block
version on the hub, that mismatch is the first thing to check, and `toolKit.py`
is the pattern to copy, not the `spike` module.

**2. `code/README.md` says this season programs in Word Blocks, not Python.**
Last year's team clearly had solid, tuned Python — real `kp` and steering
values from actual runs, calibration helpers, gyro-corrected driving. Worth a
deliberate call on whether 2026 uses Python again (starting from `toolKit.py`)
or stays with Word Blocks as currently documented, rather than drifting between
the two by accident.

## Before reusing any of it

- **Ports and dimensions are last year's robot**, not this one: `LEFT_DRIVE =
  port.A`, `RIGHT_DRIVE = port.E`, wheel diameter 87–88 mm, track width 143 mm.
  Re-measure for this year's build before trusting any distance or turn.
- **The tuning comments above `drive_cm_gyro` are real data** — `kp`, speed,
  and steer-limit combinations that were actually tried. Worth reading even if
  the code itself gets rewritten.
- Mission-specific files (`Missions/`) solve *last season's* missions and won't
  map onto BIOGLOW's — kept for the driving patterns, not the mission logic.
