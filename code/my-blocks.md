# My Blocks — our shared building blocks

Custom Word Blocks we reuse across every run. Build these **once**, get them
reliable, then never rewrite movement logic again.

Rebuilding "drive forward" from scratch in each program is how teams end up with
five subtly different movements and unexplainable bugs.

> Document each block here as it's built. Judges love this — it's a clear,
> demonstrable engineering practice.

## `drive_straight (distance_cm, speed)`

Drives straight, correcting heading with the gyro so it doesn't curve.

**Use this instead of the ready-made movement blocks.** Those look easier and
they drift; there is no way to hold a heading with them. This is the single
biggest accuracy win available in code.

| Parameter | Meaning | Typical |
| --- | --- | --- |
| `distance_cm` | How far | _TODO_ |
| `speed` | Motor power % | _TODO_ |

**How it works:** zero the gyro before moving, then loop: read the heading, and
because the target is 0°, the reading *is* the error. Multiply it by a constant
(`kp`) and add that to one wheel's speed while subtracting it from the other, so
the robot steers back toward 0°. Repeat every few milliseconds until the motor
encoder says you have gone far enough. Bump a mission model mid-run and it
steers itself back instead of carrying the error to the end of the match.

**Tuning notes:** `kp` too low and it corrects too slowly and drifts wide; too
high and it weaves back and forth past the line. Tune it at the speed you will
actually drive at, because the right value changes with speed. Combinations that
worked on last season's robot are in the comment above `drive_cm_gyro` in
[`../code/library/README.md`](library/README.md)'s toolkit — 600/2.8, 500/2.6,
400/3.2 — but they depend on weight and grip, so re-tune rather than assume.

**We already have two of these.** The `Acceleration` My Block in
`spike-projects/Acceleration.llsp3` ramps the speed up, holds the gyro heading
through the middle, then eases off — and `drive_cm_gyro` in the Python toolkit is
the same idea. Read one before writing a third.

**Status:** ☐ built ☐ tested ☐ used in a run

---

## `turn_degrees (angle, speed)`

Turns in place to a gyro-measured angle.

| Parameter | Meaning | Typical |
| --- | --- | --- |
| `angle` | Degrees, + right / − left | _TODO_ |
| `speed` | Motor power % | _TODO_ |

**Gotcha:** turning too fast overshoots; the gyro reads correctly but momentum
carries the robot past. Slow the final few degrees.
**Status:** ☐ built ☐ tested ☐ used in a run

---

## `square_to_line (speed)`

Drives until both colour sensors see the line, squaring the robot against it.
Resets accumulated position error — use before anything precise.

**Status:** ☐ built ☐ tested ☐ used in a run

---

## `reset_gyro ()`

Zeroes the gyro. **Call this at the start of every program**, with the robot
already still in Base. Calling it while the robot is moving gives a bad zero, and
every turn afterwards is wrong — a genuinely common and very confusing bug.

**Status:** ☐ built ☐ tested ☐ used in a run

---

## `run_attachment (motor, degrees, speed)`

Runs an attachment motor a set amount.

**Status:** ☐ built ☐ tested ☐ used in a run

---

## Add new blocks above this line

Template:

```
## `block_name (params)`
What it does.
**Parameters:** …
**Gotchas:** …
**Status:** ☐ built ☐ tested ☐ used in a run
```

--8<-- "includes/abbreviations.md"
