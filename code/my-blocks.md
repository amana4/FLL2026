# My Blocks — our shared building blocks

Custom Word Blocks we reuse across every run. Build these **once**, get them
reliable, then never rewrite movement logic again.

Rebuilding "drive forward" from scratch in each program is how teams end up with
five subtly different movements and unexplainable bugs.

> Document each block here as it's built. Judges love this — it's a clear,
> demonstrable engineering practice.

## `drive_straight (distance_cm, speed)`

Drives straight, correcting heading with the gyro so it doesn't curve.

| Parameter | Meaning | Typical |
| --- | --- | --- |
| `distance_cm` | How far | _TODO_ |
| `speed` | Motor power % | _TODO_ |

**How it works:** _TODO — describe the gyro correction_
**Tuning notes:** _TODO — proportional constant, what happens if too high_
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
