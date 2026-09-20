# Missions — 2026 Python programs

One folder per BIOGLOW mission, matching the slugs in
[`robot-game/missions/`](../../robot-game/missions/README.md). Each folder has
a `mission.py` stub — fill it in once that mission's page has an Approach
designed, not before.

```
code/missions/
  M01-drone-survey/mission.py
  M02-exploding-seeds/mission.py
  ...
  M15-biocentric-architecture/mission.py
```

## Why one file per mission instead of one big program

Matches how you actually run: each mission (or small combo of missions) is its
own hub program, loaded into its own slot. Keeping them separate here means the
file you edit is the file you paste onto the hub — no risk of editing the wrong
section of a giant script.

## The shared library

Every mission file starts with:

```python
from library.toolkit import init_robot, drive_cm, drive_cm_gyro, turn_deg, run_attachment_deg
```

`library.toolkit` is [`code/library/`](../library/README.md)'s `toolkit.py` —
drive, turn, and attachment helpers built once and reused everywhere, instead
of rebuilding movement logic from scratch in every mission.

**Important limitation:** the SPIKE App's Python canvas runs one
self-contained file per hub slot — it does not import a separate local module
across files. So the `import` line above works for editing and reviewing here
in git, but before a mission program actually runs on the hub, paste
`toolkit.py`'s contents above the import line (replacing it), the way last
season's `Missions/` files did — see `code/2025-reference/` (not published to
this site).

## The concatenation step is now a tool

For the advanced library there is no pasting. A mission that uses
[`../library/advanced.py`](../library/README.md) is called
`mission-advanced.py`, and it is built:

```
python3 tools/build-mission.py
```

Everything above this marker line is a copy of `advanced.py`:

```
# ===== MISSION CODE BELOW. THE GENERATOR DOES NOT TOUCH THIS =====
```

Everything below it is yours. Edit there. Then rebuild, and paste the whole
file onto the hub.

**Port assignments go below the marker, not above.** Python runs the file top to
bottom, and every function reads `LEFT_DRIVE` when it is called rather than when
it is defined. So reassigning it after the library body works, and it survives a
rebuild.

`python3 tools/build-mission.py --check` fails if a built file has fallen behind
the library. Run it before pushing.

This is worth having because the hand-copied version went wrong.
`M03-flip-the-rock/mission.py` still carries a header reading
`Drive: A (left), E (right)` while its own code says `port.F` and `port.A`. Two
lines apart, disagreeing, for weeks.

`M03-flip-the-rock/mission-advanced.py` is the first one built this way.

## Workflow

1. Design the approach on the mission's page in `robot-game/missions/`.
2. Fill in `run()` in that mission's `mission.py` here.
3. Paste `toolkit.py` above the import, test on the hub, iterate.
4. Once it's reliable, record the result in the mission's Attempt log and in
   [`robot-game/runs/`](../../robot-game/runs/README.md).

--8<-- "includes/abbreviations.md"
