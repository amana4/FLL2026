# My Blocks — our shared building blocks

Custom Word Blocks we reuse across every run. Build these **once**, get them
reliable, then never rewrite movement logic again.

Rebuilding "drive forward" from scratch in each program is how teams end up with
five subtly different movements and unexplainable bugs.

> Document each block here as it's built. Judges love this — it's a clear,
> demonstrable engineering practice.

## Where the blocks actually live

Most of this page used to be a wish list. It is not any more. The blocks are
built, in the SPIKE App project **Advanced Coding 26**
(`Advanced-Coding-26.llsp3`), which holds fourteen of them.

Every one has now been ported to Python as well, in
[`library/advanced.py`](library/advanced.py). The Python version fixes eight
real bugs in the blocks, listed at the top of that file. If the two ever
disagree, the Python file says which is which and why.

Names starting with `.` are the ones to use. Names starting with `z` are
internals that a `.` block calls, named that way so they sort to the bottom of
the palette.

| Block | Python | Also called |
| --- | --- | --- |
| `.Forward (Mm)` | `drive_cm(cm)` | `forward(cm)` |
| `.Backward (mm)` | `drive_cm(-cm)` | `backward(cm)` |
| `.Left (PID)` / `.Right (PID)` | `turn_deg_gyro(-deg)` / `turn_deg_gyro(deg)` | `left_pid()` / `right_pid()` |
| `Left (simple)` / `Right (simple)` | `turn_deg(-deg)` / `turn_deg(deg)` | `left_simple()` / `right_simple()` |
| `Gyro Backwards (degrees) basic` | `gyro_backward_deg(speed_pct, degrees)` | `gyro_backwards()` |
| `Line Square` | `line_square()` | |
| `Line Follow` | `line_follow(side, seconds)` | |

The middle column uses the same names as
[`library/toolkit.py`](library/toolkit.py), so mission code can move between the
two Python files without renaming anything. The sign says which way to go:
positive is forward or clockwise.

The last column reads closer to the palette, for anybody comparing the blocks
and the Python. They are the same functions.

**The units are not the same.** The blocks take millimetres and the Python takes
centimetres. `.Forward 300` is `drive_cm(30)`, not `drive_cm(300)`. Getting that
wrong asks for three metres, so the Python refuses anything longer than the mat
and tells you what you probably meant.

---

## `drive_straight` — built as `.Forward` and `.Backward`

Drives straight, correcting heading with the gyro so it doesn't curve.

**Use this instead of the ready-made movement blocks.** Those look easier and
they drift; there is no way to hold a heading with them. This is the single
biggest accuracy win available in code.

| Parameter | Meaning | Typical |
| --- | --- | --- |
| `Mm` | How far, in millimetres | 300 |

There is no speed parameter. The block works it out: a quarter of the distance
becomes the ramp length, clamped between 30 and 100 mm, at 60 percent, dropping
to 30 percent for anything under 300 mm. It starts and finishes at 25 percent.

**How it works:** zero the gyro before moving, then loop: read the heading, and
because the target is 0°, the reading *is* the error. Multiply it by a constant
(`kp`) and add that to one wheel's speed while subtracting it from the other, so
the robot steers back toward 0°. Repeat every few milliseconds until the motor
encoder says you have gone far enough. Bump a mission model mid-run and it
steers itself back instead of carrying the error to the end of the match.

On top of that it ramps: up over the first stretch, flat through the middle,
down over the last. Starting gently stops the wheels slipping, and finishing
gently stops the robot carrying past the mark.

**Stop compensation.** The block subtracts 14 mm from whatever you asked for,
because the robot coasts about that far after the brakes go on. So
`.Forward 300` drives 286 mm and lands at 300. Measure this on your own floor;
it changes with speed and grip.

**Tuning notes:** `kp` too low and it corrects too slowly and drifts wide; too
high and it weaves back and forth past the line. Tune it at the speed you will
actually drive at, because the right value changes with speed. The blocks use
`kp` 1.8 and `kd` 0.5. Combinations that worked on last season's robot are in
the comment above `drive_cm_gyro` in [the toolkit](library/README.md) —
600/2.8, 500/2.6, 400/3.2 — but they depend on weight and grip, so re-tune
rather than assume.

**There are three of these now.** `.Forward`, the older `Acceleration` My Block
in `spike-projects/Acceleration.llsp3`, and `drive_cm_gyro` in the Python
toolkit. `.Forward` is the one to use. Read the other two before writing a
fourth.

**Status:** ☑ built ☐ tested ☐ used in a run

---

## `turn_degrees` — built twice, as PID and as simple

Turns in place to a gyro-measured angle. There are two versions on purpose.

`.Left (PID)` and `.Right (PID)` run a full PID loop on the gyro. Accurate to
about half a degree, and slower.

`Left (simple)` and `Right (simple)` spin at a flat 15 percent until the gyro is
nearly there, then brake. Cruder and quicker.

| Parameter | Meaning | Typical |
| --- | --- | --- |
| `Degrees` | How far to turn. Always positive; the block name picks the side | 90 |
| `Kp` | PID versions only. How hard to correct | 0.7 |

**Gotcha:** turning too fast overshoots; the gyro reads correctly but momentum
carries the robot past. Slow the final few degrees. The simple versions handle
this by stopping 4 or 5 degrees short and letting momentum finish the turn. That
number is right for one speed and one floor, so check it on the competition mat.

**Gotcha, PID version:** below roughly 12 percent power the wheels buzz without
moving. The block gets around it by accepting anything within a degree. The
Python port sets a minimum power instead, which is why `turn_deg_gyro(3)` works
and the block version of a 3 degree turn does not.

**Status:** ☑ built ☐ tested ☐ used in a run

---

## `square_to_line` — built as `Line Square`

Drives until both colour sensors see the line, squaring the robot against it.
Resets accumulated position error — use before anything precise.

Two passes. It drives on until either sensor sees black, then creeps each wheel
forward until both do. Then it backs each wheel off until both read light again,
so the robot finishes square on the *edge* of the line rather than square on the
middle of it. The edge is the sharper target.

Sensor E is the left one and F is the right, matching the Python library.

**Gotcha:** in the blocks, every wait here is unbounded. Miss the line and the
robot sits still for the rest of the match. `line_square()` in the Python port
times out and says so.

**Status:** ☑ built ☐ tested ☐ used in a run

---

## `Line Follow (side, seconds)` — built

Finds a line, swings onto its edge, then follows it for a number of seconds.
Three internal blocks do the work: `zFind Line`, `zAcquire Line`, and
`zFollowing a line`.

| Parameter | Meaning | Typical |
| --- | --- | --- |
| `Right or Left` | 1 to ride the right edge, -1 for the left | 1 |
| `Time` | How many seconds to follow for | 3 |

One sensor, proportional. It holds the reading at 45, the grey halfway between
black line and white mat, and steers by the error times 2.

**Gotcha:** it follows for a *time*, not a distance. A slower battery covers less
ground in the same three seconds. Do not trust it to end somewhere exact.

**Status:** ☑ built ☐ tested ☐ used in a run

---

## `Gyro Backwards (degrees) basic` — built

Reverses at a fixed speed, held straight by the gyro, for a number of **motor
degrees** rather than a distance. The odd one out: everything else in the
library takes millimetres.

**Status:** ☑ built ☐ tested ☐ used in a run

---

## `reset_gyro ()`

Zeroes the gyro. **Call this at the start of every program**, with the robot
already still in Base. Calling it while the robot is moving gives a bad zero, and
every turn afterwards is wrong — a genuinely common and very confusing bug.

Not built as a separate block, and it does not need to be. Every block in
Advanced Coding 26 waits 0.3 seconds and zeroes the gyro itself before it moves.
The wait is the important half: the hub's gyro keeps drifting for a moment after
the motors stop, and zeroing it too early bakes that error into the next move.

**Status:** ☑ not needed, handled inside each block

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
