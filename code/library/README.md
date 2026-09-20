# Library — shared Python movement code

Two files, and they do not do the same thing.

`toolkit.py` holds the drive, turn, and attachment functions every 2026 mission
program builds on: `init_robot`, `drive_cm`, `drive_cm_gyro`, `turn_deg`,
`turn_deg_gyro`, `arc_turn`, `run_attachment_deg`, plus wheel-diameter
calibration helpers.

Ported from last season's `Library/toolKit.py` — see `code/2025-reference/`
(not published to this site) for where it came from and what changed.

`advanced.py` is a Python port of the Word Blocks library, **Advanced Coding
26**. All fourteen My Blocks: ramped straight drives, PID turns, quick turns,
line squaring and line following. See [`../my-blocks.md`](../my-blocks.md) for
the block-by-block mapping.

## Which one do I use?

| You want | Use |
| --- | --- |
| What the missions already use | `toolkit.py` |
| The same movement as the Word Blocks | `advanced.py` |
| A drive that ramps up and down | `advanced.py`, `drive_cm` |
| A gyro turn that actually works | `advanced.py`, `turn_deg_gyro` |
| To follow or square on a line | `advanced.py`, hub only |

Neither imports the other. They disagree in one place, described below.

## Same names in both files

`advanced.py` uses `toolkit.py`'s function names. `init_robot`, `reset_yaw`,
`drive_cm`, `drive_cm_gyro`, `turn_deg`, `turn_deg_gyro`, `arc_turn`,
`run_attachment_deg`, `timed_attachment`, `move_attachment_deg`, `nudge_cm`,
`micro_turn_deg`, `calibrate_wheel_diameter`, `set_calibration_scale`.

A mission can move between the two files without hunting for a renamed
function. `tools/check-library.py` fails if a name goes missing.

What changes is what happens underneath:

| Function | `toolkit.py` | `advanced.py` |
| --- | --- | --- |
| `drive_cm` | constant speed, no gyro | ramps up and down, holds the heading |
| `drive_cm_gyro` | steering loop with five tuning knobs | the same function as `drive_cm` |
| `turn_deg` | counts wheel degrees, needs `TRACK_W_MM` | spins on the gyro |
| `turn_deg_gyro` | never moves the motors, see `code/learn/10-gyro.md` | works |

Some toolkit arguments are gone, because they describe a control loop
`advanced.py` does not have: `steer_limit`, `deadband_deg`, `steer_rate_limit`,
`min_steer_kick`, `acceleration` and `deceleration`. Passing one raises a
`TypeError` rather than being quietly ignored. The ramp does the job
`acceleration` and `deceleration` used to.

There are also aliases named after the SPIKE palette — `forward`, `backward`,
`left_pid`, `right_pid`, `left_simple`, `right_simple`, `gyro_backwards`. They
are for reading the blocks and the Python side by side. Use the toolkit names in
mission code.

**The units are not the same as the blocks.** The blocks take millimetres and
this takes centimetres, so `.Forward 300` is `drive_cm(30)`. Copying the 300
across asks for three metres. `drive_cm` refuses anything longer than the mat
and says what you probably meant.

## The two files disagree about the gyro

`toolkit.py` steers by `+yaw_err * kp`. `advanced.py` defaults to the opposite,
because both Word Blocks programs it came from assume the gyro counts up
clockwise. The pretend hub in `tools/spike-shim.py` matches `toolkit.py`, and
says in its own docstring that this is only because the toolkit was there first.

Nobody has measured it on the hub. Until somebody does, run
`bench_check_yaw_sign()` from `advanced.py` — it spins the robot a quarter turn
and prints which value to use. Then set `YAW_SIGN` at the top of that file.

`code/learn/10-gyro.md` has the long version.

## Never read Python before?

[**Reading the toolkit**](toolkit-slides.html) is a 20-slide walk through
`toolkit.py`, assuming you have never written a line of code. It covers imports,
the settings block, why the motor only understands degrees, `async`/`await`, the
gyro correction loop, calibration, and the three bugs sitting in the file right
now. Arrow keys to move between slides; it prints one slide per page.

## Checking a change

```
python3 tools/check-library.py
```

Drives `advanced.py` against the pretend hub and checks where the robot ended
up. It catches a runaway loop or a flipped sign in about ten seconds.
`tools/check-lessons.py` does not cover this file; it only reads `code/learn/`
and only ever loads `toolkit.py`.

The two line functions cannot be checked. The pretend hub has no colour sensor,
so the run only confirms they refuse politely instead of crashing.

## Before trusting any of it on the 2026 robot

**This table is out of date and has been for a while.** `toolkit.py:1-10`
records the wiring as confirmed against the hub on 13 September 2026: drive
motors A and B, colour sensors E and F, wheel 62.4 mm, track 130 mm.
`advanced.py` uses those same numbers. The table below says something else.
Somebody with the robot in front of them should settle it and delete whichever
is wrong.

| Setting | Value in the file | |
| --- | --- | --- |
| Drive motors | Ports A (left), E (right) | _TODO — confirm or update_ |
| Color sensors | Ports F (left), B (right) | _TODO_ |
| Attachment motors | Ports C, D | _TODO_ |
| Wheel diameter | 88.0 mm | _TODO — measure this year's wheels_ |
| Track width | 143.0 mm | _TODO — measure this year's chassis_ |

Update these once the 2026 driving base is built (see
[`robot-design/chassis.md`](../../robot-design/chassis.md)), and use
`calibrate_wheel_diameter()` to correct for any remaining drift between
commanded and actual distance.

## Tuning notes carried over from last season

The comment above `drive_cm_gyro` lists three speed/kp/steer-limit
combinations that worked on last year's robot. They won't transfer exactly —
weight and wheel grip changed — but they're a sane starting point for tuning
rather than guessing from zero.

`advanced.py` carries its own numbers across from the blocks: `kp` 1.8 and `kd`
0.5 for straight driving, `kp` 0.7 with `ki` 0.001 and `kd` 0.1 for the PID
turns. Those came off a real mat too, but with a different control loop, so they
are a starting point and not an answer.

## Deployment note

Both files are meant to be imported (`from library.toolkit import ...`) while
editing mission code here in git. The SPIKE App's Python canvas does not
support that import at upload time — see
[`code/missions/README.md`](../missions/README.md) for the paste-it-in-manually
step this currently requires. That is why `advanced.py` is one self-contained
file that repeats the geometry helpers rather than importing them.
