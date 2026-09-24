# 10. The gyro

The wheels tell the robot how far it has gone. Nothing so far tells it which way it
is pointing. The gyro does that, and it is the difference between a run that works
once and a run that works ten times.

If you would rather see it than read it, there are four pictures:
[**how gyro correction works**](gyro-correction.html). Drift, the error angle, the
two wheel speeds, the loop, and what happens when the sign is backwards.

## Which library this page uses

Lessons 1 to 9 ran on `toolkit.py`. Every Run button on this page runs on
[`advanced.py`](../library/advanced.py) instead, which is the library the M02 and
M03 missions now use. The names are mostly the same, but three of them do more:

| Function | What it does in `advanced.py` |
| --- | --- |
| `drive_cm(cm)` | Drives straight and **holds its heading with the gyro**. Always |
| `turn_deg(deg)` | Turns **by** that many degrees, using the gyro. Positive is right |
| `face(deg)` | Turns **to** a direction, counted from where the robot started |
| `bearing()` | Tells you which way the robot points now, counted the same way |

`drive_cm_gyro` and `turn_deg_gyro` still work. They are second names for
`drive_cm` and `turn_deg`, so old code does not break.

## Drifting

A real robot does not drive straight. One motor is a little stronger, one tyre grips
a little better, the battery sags. Over 40 cm it barely shows. Over 180 cm it misses
the model.

`sim.set_drift` puts that in on purpose, in degrees of veer per second. Setting
`kp=0, kd=0` switches the gyro correction off, so this is a drive with no gyro:

<div class="spike-run" data-lib="advanced" markdown="1">

```python
sim.set_drift(8)

await init_robot()
await drive_cm(40, kp=0, kd=0)
print(sim.pose())
```

</div>

The robot ended about 4 cm to the right and pointing about 11 degrees off. The
trail on the picture is visibly a curve.

Now the same drive with the correction left on:

<div class="spike-run" data-lib="advanced" markdown="1">

```python
sim.set_drift(8)

await init_robot()
await drive_cm(40)
print(sim.pose())
```

</div>

About 0.6 cm off, and under 1 degree. Same robot, same drift, same distance.

The pretend robot runs in real time, so your numbers can differ from these by a
few tenths. That is normal. The tables on this page are from one run.

| Drift | Gyro off | Gyro on |
| --- | --- | --- |
| none | dead straight | dead straight |
| 8 deg/s | 3.9 cm sideways, 11.4 deg off | 0.6 cm sideways, 0.9 deg off |
| 20 deg/s | 9.6 cm sideways, 28.6 deg off | 1.4 cm sideways, 2.2 deg off |

Turn the drift up to 20 in either block above and watch the uncorrected version
give up entirely.

Note: the robot stops at about 58.7, not 60. `drive_cm` brakes 1.4 cm early,
because the real robot rolls that far after the brakes go on. The pretend robot
stops dead, so on this page it lands short. That number is `STOP_COMP_FWD_CM` at
[`advanced.py:82`](../library/advanced.py), and lesson 9 is how you measure it.

## What the gyro actually reports

The sensor is `motion_sensor`, and it reports angles in **tenths of a degree**.
That is why the library has a helper to divide by ten, at
[`advanced.py:155`](../library/advanced.py):

```python
def _yaw_deg():
    y_decideg, _, _ = motion_sensor.tilt_angles()
    return y_decideg / 10.0
```

Two things to notice.

`tilt_angles()` hands back three numbers at once — yaw, pitch and roll. The
`_, _` means "I do not care about the other two". That is a real Python idiom, and
it is clearer than naming variables you never use.

The units are tenths, so 900 means 90 degrees. Forgetting the divide gives you
answers ten times too big, and the robot spins wildly. Whenever a gyro number looks
absurd, count the zeros first.

The next helper fixes the direction. Our hub counts **up** when the robot turns
**left**, which is the opposite of what the rest of the library wants. So one line
flips it:

```python
YAW_SIGN = -1

def _yaw_cw():
    return YAW_SIGN * _yaw_deg()
```

From here on, every number in this lesson counts clockwise: turning right is
positive, turning left is negative. The whole library steers off `_yaw_cw()`, so if
the hub is ever rebuilt and counts the other way, one number at the top changes and
nothing else.

<div class="spike-run" data-lib="advanced" data-view="none" markdown="1">

```python
await init_robot()
await turn_deg(30)
print("raw from the sensor:", motion_sensor.tilt_angles())
print("in degrees:         ", _yaw_deg())
print("clockwise:          ", _yaw_cw())
```

</div>

The robot turned 30 degrees right. The sensor says about -300, the helper says -30,
and `_yaw_cw()` says +30.

## Zeroing it

The gyro has no idea which way is north, and does not need to. What matters is how
far the robot has turned **since you last told it to start counting**.

`drive_cm` zeroes the gyro first thing, every time. From then on, "yaw is 0" means
"still pointing the way I started this drive", and "yaw is 4" means "4 degrees off".
The whole correction is built on that one idea: **zero it, then keep it at zero.**

There is a catch. If every drive zeroes the gyro, how does the robot remember
which way it pointed at the start of the run? The zeroing helper, at
[`advanced.py:170`](../library/advanced.py), writes the old reading down first:

```python
def _reset_yaw(deg=0):
    global _HEADING_BASE
    _HEADING_BASE = _HEADING_BASE + _yaw_cw() - deg
    motion_sensor.reset_yaw(int(deg * 10))
```

It is like writing down a car's mileage before you reset the trip counter.
`_HEADING_BASE` is the mileage. We come back to it in the section on `face`.

## The correction loop

This is the heart of `drive_cm`, from
[`advanced.py:409`](../library/advanced.py), with the ramp and the safety checks
stripped out:

```python
while travelled < dist_deg:
    error = _wrap180(_yaw_cw())               # how far off straight are we
    trim = -(kp * error + kd * (error - last_error))
    last_error = error

    _tank(base + trim, base - trim)           # one wheel faster, one slower

    await runloop.sleep_ms(15)
```

Sixty-six times a second, it asks two questions. How far off am I, and how hard
should I push back.

`error` is the gyro reading itself, because the gyro reads 0 when the robot is
straight. `trim` is the push back. It is added to the left wheel and taken off the
right, so the robot turns back towards straight.

**Look hard at the minus sign.** If the robot has drifted right, `error` is
positive, so `trim` is negative. The left wheel slows, the right wheel speeds up,
and the robot turns left, back to straight. Take the minus away and the push goes
the same way as the drift, which spins the robot. A wrong `YAW_SIGN` does the same
thing from the other end. Our robot had exactly that on 20 September 2026, and it
is the bug at the end of this page.

`kp` is how hard to push. It is a multiplier: a bigger `kp` corrects harder. The
library default is 18.9, at [`advanced.py:70`](../library/advanced.py).

<div class="spike-run" data-lib="advanced" markdown="1">

```python
sim.set_drift(8)

await init_robot()
await drive_cm(40, kp=0, kd=0)
print("kp 0:", sim.pose())
```

</div>

Try 2, then 5, then 10, then 18.9. Keep `kd=0` for now, so you only change one
thing at a time.

| `kp` | Ends up sideways by |
| --- | --- |
| 0 | 3.91 cm |
| 2 | 2.63 cm |
| 5 | 1.71 cm |
| 10 | 1.01 cm |
| 18.9 | 0.56 cm |
| 40 | 0.29 cm |

This is called **proportional control**: the correction is proportional to the
error. Small error, gentle nudge. Big error, hard shove.

`kd` is the second knob. It looks at how fast the error is **changing**, not how
big it is, and pushes against the change. That calms the robot down before it
overshoots. On this page it hardly matters, for the reason in the note below.

!!! note "Where this page misleads you"

    In that table, bigger is always better, and on a real robot it is not. A real
    motor takes time to respond, so a hard correction arrives slightly late, has
    overshot, and then gets corrected the other way. The robot wobbles down the mat
    instead of driving down it. Set `kp` too high on the real robot and you will see
    it immediately. That wobble is also what `kd` is for.

    This page has no motor lag, so it cannot show you that. The numbers recorded in
    the toolkit comments came from a real mat, with the toolkit's older loop:

    ```python
    # Speed: 600, kp: 2.8, steer rate limit: 4
    # Speed: 500, kp: 2.6, steer rate limit: 6
    # Speed: 400, kp 3.2, steer rate limit : 10
    ```

    Those are not the same scale as `advanced.py`'s `kp`, so do not copy them
    across. The lesson in them still holds: faster driving wants a lower `kp`.
    Trust that, not the table above.

## Watching it think

`DEBUG` is `False` at the top of `advanced.py`. Set it to `True` and `drive_cm`
prints a line every time round the loop:

<div class="spike-run" data-lib="advanced" data-height="200" markdown="1">

```python
DEBUG = True
sim.set_drift(15)

await init_robot()
await drive_cm(10)
```

</div>

Each line has how far the wheels have turned out of how far they need to, the
speed, and the yaw. Read the `speed` column first. It climbs at the start and
falls at the end, because `drive_cm` ramps up and down instead of lurching.

Then read the `yaw` column. It climbs for a moment and then sits at about 1.6.
It never gets back to 0. The drift pushes the robot right all the time, so the loop
has to push left all the time, and proportional control can only push while there
is some error. 1.6 degrees is where the two pushes balance.

This is the single most useful debugging habit in the whole library. When a run
misbehaves, print the thing the code is deciding on.

## Turning by an amount: `turn_deg`

`turn_deg` spins on the spot and watches the gyro until it has turned far enough.
Positive is right, negative is left.

<div class="spike-run" data-lib="advanced" markdown="1">

```python
await init_robot()
await turn_deg(90)
print("bearing:", bearing())
```

</div>

`bearing()` says about 89.5 to 90. The turn stops when it is within 1 degree of the
target, then waits, looks again, and goes round once more if the robot rolled past.
On our hub the roll after braking was worth about 2.4 degrees every turn, so that
second look matters.

## Turning to a direction: `face`

`turn_deg(90)` means "a quarter turn right **from wherever I am now**". If the
robot is already 3 degrees off, it ends up 3 degrees off plus a quarter turn.

`face(90)` means "point **90 degrees right of where I started the run**". It does
not matter where the robot is pointing now. It works out the difference and turns
by that.

That is what `bearing()` and `_HEADING_BASE` are for. `bearing()` adds the
remembered mileage to what the gyro says now, so it counts from the start of the
run, however many times a drive has zeroed the gyro since.

The difference shows when turns are not perfect. A real turn often lands a few
degrees short. `stop_early_deg=3` makes the pretend robot do the same thing on
purpose. Here is a square with `turn_deg`:

<div class="spike-run" data-lib="advanced" markdown="1">

```python
await init_robot()
for side in range(4):
    await drive_cm(30)
    await turn_deg(90, stop_early_deg=3)
    print("bearing:", round(bearing(), 1))
print(sim.pose())
```

</div>

Each turn is 3 degrees short, and each one starts from where the last one ended.
The mistakes pile up: about 87, 173, 260, 346. The robot finishes about 14
degrees off, and the square does not close.

Now the same square with `face`:

<div class="spike-run" data-lib="advanced" markdown="1">

```python
await init_robot()
for target in (90, 180, 270, 360):
    await drive_cm(30)
    await face(target, stop_early_deg=3)
    print("bearing:", round(bearing(), 1))
print(sim.pose())
```

</div>

About 86, 176, 266, 357. Every turn still lands 3 degrees short, but only 3. The mistake
from one turn is not passed on to the next, because every target is counted from
the same place.

| | `turn_deg` | `face` |
| --- | --- | --- |
| Means | turn **by** this much | turn **to** this direction |
| Counts from | wherever the robot is now | where the robot started the run |
| Mistakes | pile up, turn after turn | stay the size of one turn |
| Use it for | a small adjustment, like "5 more degrees" | getting lined up for the next drive |

`face` goes whichever way round is shorter. `face(0)` and `face(360)` both mean
"back the way I started", and `face(-90)` and `face(270)` both mean "a quarter turn
left of where I started".

## Find the bug

This is the bug from 20 September 2026. Before that date, `advanced.py` had
`YAW_SIGN = +1`, copied from the Word Blocks. Put it back and run:

<div class="spike-run" data-lib="advanced" data-height="200" markdown="1">

```python
# expect-error
YAW_SIGN = +1
sim.set_drift(8)

await init_robot()
await drive_cm(40)
```

</div>

The robot swerves off to the right and then stops with an error. Read the error,
then read the correction loop above again.

??? question "What went wrong?"

    With `YAW_SIGN` the wrong way round, `_yaw_cw()` reports a drift to the right
    as a drift to the left. So the loop pushes right to "fix" it, which makes the
    real error bigger, which makes the loop push harder. Each push makes the next
    one worse. That is what a **runaway** is.

    On the real robot there was no error message. The robot spun on the spot
    instead of driving, and nearly went off the table. The distance counter
    adds up both wheels, and a spin turns both wheels, so the loop thought it was
    still driving forwards.

    The fix had two parts. `YAW_SIGN` went to `-1`, which was measured on the hub
    and not guessed. And `RUNAWAY_DEG = 45` at
    [`advanced.py:106`](../library/advanced.py) stops the robot if a straight
    drive is ever more than 45 degrees off course, because a drive holding a
    heading is never that far out unless the loop is pushing the wrong way.

    **What to do after a rebuild.** Run `bench_check_yaw_sign()` on the table. It
    turns right a quarter turn and tells you which value `YAW_SIGN` should be.
    Never copy a sign out of the Word Blocks: both of those programs have it
    backwards.

The toolkit has a gyro bug of its own. `turn_deg_gyro` in
[`toolkit.py:303`](../library/toolkit.py) never tells the motors to move, so it sits
still until something stops it. The line that would drive the motors is commented
out, and it calls `motor_pair.start`, which does not exist in SPIKE App 3.5. That
is why `advanced.py` has a new `turn_deg` and not a copy of that one.

## Your turn

Four exercises. Do them in order, and write down what you get each time.

**1. Tune `kp`.** At drift 12, find the lowest `kp` that keeps a 100 cm drive within
1 cm of straight. Change one number at a time.

<div class="spike-run" data-lib="advanced" markdown="1">

```python
sim.set_drift(12)

await init_robot()
await drive_cm(100, kp=10)
print("sideways error:", round(sim.pose()[0] - 30, 2), "cm")
```

</div>

??? question "How to go about it"

    Do not guess randomly. Halve the gap each time: try 10, then 60, then 30, then
    45. Four runs gets you closer than ten random ones. It is the same method as
    guessing a number between 1 and 100.

    The default of 18.9 gives 2.16 cm, so it is not enough on this page. The answer
    is close to 40.

    Write the results in a table as you go. That table is exactly what the Robot
    Design judges mean by evidence of iteration, and it belongs in
    [`robot-design/design-log.md`](../../robot-design/design-log.md).

    Then do it again on the real robot, where the answer will be different and the
    wobble is real.

**2. Predict, then run.** Before you press Run, write down the three numbers you
expect this to print.

<div class="spike-run" data-lib="advanced" data-view="none" markdown="1">

```python
await init_robot()
await face(90)
print(round(bearing()))
await turn_deg(45)
print(round(bearing()))
await face(90)
print(round(bearing()))
```

</div>

??? question "What it prints, and why"

    About 90, then 135, then 90.

    `turn_deg(45)` adds 45 to wherever the robot is. The second `face(90)` does not
    turn by 90. It looks at where the robot is, 135, sees that 90 is 45 degrees to
    the left, and turns left by 45. If you wrote 180 for the last number, you
    treated `face` like `turn_deg`.

**3. Back where you started.** Change the square from earlier so it ends pointing
exactly the way it started, even though every turn lands 3 degrees short. You may
add one line.

<div class="spike-run" data-lib="advanced" markdown="1">

```python
await init_robot()
for side in range(4):
    await drive_cm(30)
    await turn_deg(90, stop_early_deg=3)
print("bearing:", round(bearing(), 1))
```

</div>

??? question "One answer"

    Add `face(0)` after the loop. However far off the four turns left the robot,
    `face` works out the difference from the start of the run and turns by that.

    ```python
    await init_robot()
    for side in range(4):
        await drive_cm(30)
        await turn_deg(90, stop_early_deg=3)
    await face(0)
    print("bearing:", round(bearing(), 1))
    ```

    This is how to use `face` in a mission: line up with it before every long
    drive, so an early mistake does not follow the robot round the mat.

**4. Draw an L.** Drive 40 cm up the mat, then 30 cm right, then point back up the
mat. Use `face` for both turns, with drift 8 switched on.

<div class="spike-run" data-lib="advanced" markdown="1">

```python
sim.set_drift(8)

await init_robot()
await drive_cm(40)
# your turn and drive go here
print(sim.pose(), round(bearing(), 1))
```

</div>

??? question "One answer"

    ```python
    sim.set_drift(8)

    await init_robot()
    await drive_cm(40)
    await face(90)
    await drive_cm(30)
    await face(0)
    print(sim.pose(), round(bearing(), 1))
    ```

    The last number `sim.pose()` prints is the heading. It should be within about
    a degree of 0, or of 360, which is the same direction.

## Words from this lesson

| Word | Meaning |
| --- | --- |
| gyro | The sensor inside the hub that measures turning |
| yaw | Rotation left and right, the one that matters for driving |
| decidegree | A tenth of a degree. What the sensor reports in |
| drift | Veering off straight without being told to |
| error | How far the measurement is from what you wanted |
| proportional control | Correcting in proportion to the error |
| `kp` | The multiplier that decides how hard to correct |
| `kd` | The multiplier that pushes against the error changing too fast |
| bearing | Which way the robot points, counted from the start of the run |
| base | The direction the robot pointed when `init_robot()` ran |
| runaway | A loop whose correction makes the error bigger, so it never settles |
| tuning | Finding the numbers that work, by measuring |

--8<-- "includes/abbreviations.md"
