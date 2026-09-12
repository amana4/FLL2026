# 10. The gyro

The wheels tell the robot how far it has gone. Nothing so far tells it which way it
is pointing. The gyro does that, and it is the difference between a run that works
once and a run that works ten times.

## Drifting

A real robot does not drive straight. One motor is a little stronger, one tyre grips
a little better, the battery sags. Over 40 cm it barely shows. Over 180 cm it misses
the model.

`sim.set_drift` puts that in on purpose, in degrees of veer per second:

<div class="spike-run" markdown="1">

```python
DEBUG = False
sim.set_drift(8)

await init_robot()
await drive_cm(40)
print(sim.pose())
```

</div>

Asked to drive straight up the mat, the robot ended 4 cm to the right and pointing
11.8 degrees off. The trail on the picture is visibly a curve.

Now the same drive with the gyro version:

<div class="spike-run" markdown="1">

```python
DEBUG = False
sim.set_drift(8)

await init_robot()
await drive_cm_gyro(40)
print(sim.pose())
```

</div>

0.8 cm off, and 1.3 degrees. Same robot, same drift, same distance.

| Drift | `drive_cm(40)` | `drive_cm_gyro(40)` |
| --- | --- | --- |
| none | dead straight | dead straight |
| 8 deg/s | 4.1 cm sideways, 11.8 deg off | 0.8 cm sideways, 1.3 deg off |
| 20 deg/s | 10.1 cm sideways, 29.4 deg off | 2.0 cm sideways, 3.3 deg off |

Turn the drift up to 20 in either block above and watch the plain version give up
entirely.

## What the gyro actually reports

The sensor is `motion_sensor`, and it reports angles in **tenths of a degree**.
That is why the toolkit has a helper to divide by ten, at
[`toolkit.py:61`](../library/toolkit.py):

```python
def _yaw_deg():
    y_decideg, _, _ = motion_sensor.tilt_angles()
    return y_decideg / 10.0
```

Two things worth noticing.

`tilt_angles()` hands back three numbers at once — yaw, pitch and roll. The
`_, _` means "I do not care about the other two". That is a real Python idiom, and
it is clearer than naming variables you never use.

The units are tenths, so 900 means 90 degrees. Forgetting the divide gives you
answers ten times too big, and the robot spins wildly. Whenever a gyro number looks
absurd, count the zeros first.

<div class="spike-run" data-view="none" markdown="1">

```python
print("raw from the sensor:", motion_sensor.tilt_angles())
print("after the helper:   ", _yaw_deg())
```

</div>

## Zeroing it

The gyro has no idea which way is north, and does not need to. What matters is how
far the robot has turned **since you last told it to start counting**.

```python
def _reset_yaw(deg=0):
    motion_sensor.reset_yaw(int(deg * 10))
```

`drive_cm_gyro` calls that first thing. From then on, "yaw is 0" means "still
pointing the way I started", and "yaw is 4" means "4 degrees off". The whole
correction is built on that one idea: **zero it, then keep it at zero.**

## The correction loop

This is the heart of `drive_cm_gyro`, with the tuning stripped out:

```python
while True:
    if traveled >= target_deg:
        break

    yaw_err = _wrap180(_yaw_deg())      # how far off straight are we
    steer = round(yaw_err * kp)         # how hard to correct
    motor_pair.move(PAIR, steer, velocity=...)

    await runloop.sleep_ms(15)
```

Sixty-six times a second, it asks two questions. How far off am I, and how hard
should I push back.

`kp` is the answer to the second one. It is a multiplier: a bigger `kp` corrects
harder. The toolkit defaults to 2.6.

<div class="spike-run" markdown="1">

```python
DEBUG = False
sim.set_drift(8)

await init_robot()
await drive_cm_gyro(40, kp=0.0)
print("kp 0.0:", sim.pose())
```

</div>

With `kp` at zero the correction is switched off, and you get the plain version back
— 4 cm off. Try 0.5, then 2.6, then 8.

| `kp` | Ends up sideways by |
| --- | --- |
| 0.0 | 4.15 cm |
| 0.5 | 2.52 cm |
| 2.6 | 0.83 cm |
| 8.0 | 0.30 cm |

This is called **proportional control**: the correction is proportional to the
error. Small error, gentle nudge. Big error, hard shove.

!!! note "Where this page misleads you"

    In that table, bigger is always better, and on a real robot it is not. A real
    motor takes time to respond, so a hard correction arrives slightly late, has
    overshot, and then gets corrected the other way. The robot wobbles down the mat
    instead of driving down it. Set `kp` too high on the real robot and you will see
    it immediately.

    This page has no motor lag, so it cannot show you that. The numbers recorded in
    the toolkit comments came from a real mat:

    ```python
    # Speed: 600, kp: 2.8, steer rate limit: 4
    # Speed: 500, kp: 2.6, steer rate limit: 6
    # Speed: 400, kp 3.2, steer rate limit : 10
    ```

    Faster driving wants a lower `kp`. Trust that, not the table above.

## The other three knobs

`drive_cm_gyro` takes four tuning arguments beyond `kp`. Each one exists to stop a
specific bad behaviour.

| Argument | Default | Stops |
| --- | --- | --- |
| `deadband_deg` | 0.1 | Fidgeting. Errors under a tenth of a degree are ignored |
| `steer_limit` | 70 | Panicking. The correction can never exceed 70 out of 100 |
| `steer_rate_limit` | 6 | Jerking. The steering can only change by 6 per step |
| `min_steer_kick` | 0 | Doing nothing. Forces a minimum push when a tiny correction rounds to zero |

Try breaking one:

<div class="spike-run" markdown="1">

```python
DEBUG = False
sim.set_drift(20)

await init_robot()
await drive_cm_gyro(60, kp=6, steer_rate_limit=1)
print(sim.pose())
```

</div>

With the rate limit at 1 the steering can only creep towards the value `kp` wants,
so the correction arrives too slowly to help much. That is the same problem motor
lag causes on the real robot, which is why the two are tuned together.

## Watching it think

`DEBUG` is `True` at the top of the toolkit, and `drive_cm_gyro` prints every step
when it is on. Leave it on and read the numbers:

<div class="spike-run" data-height="200" markdown="1">

```python
sim.set_drift(15)

await init_robot()
await drive_cm_gyro(25)
```

</div>

Four columns per line: centimetres remaining, the yaw reading, the steering being
applied, and the error. Read down the `yaw` column and watch it get pulled back
towards zero after every push away from it.

This is the single most useful debugging habit in the whole toolkit. When a run
misbehaves, print the thing the code is deciding on.

## Find the bug

There is a second gyro function, `turn_deg_gyro`, meant to turn to an exact angle
using the sensor instead of counting wheel degrees. Run it:

<div class="spike-run" data-height="180" markdown="1">

```python
# expect-error
await init_robot()
await turn_deg_gyro(90)
```

</div>

Twenty seconds, and the robot never moves. Open
[`toolkit.py:297`](../library/toolkit.py) and read the loop.

??? question "What is wrong with it?"

    Three things, and the first is enough on its own.

    **One. It never tells the motors to do anything.** The line that would is
    commented out:

    ```python
    #motor_pair.start(PAIR, steering=100, velocity=turn_rate)
    ```

    So the loop reads the gyro, works out a `turn_rate`, and throws it away. The
    robot never turns, `error` never shrinks, and the loop runs until something
    stops it.

    **Two. Even uncommented, that line is wrong.** `motor_pair.start` is not part of
    the SPIKE App 3.5 module. The function for a move that keeps running is
    `motor_pair.move`, which is exactly what `drive_cm_gyro` uses two hundred lines
    further up.

    **Three. The direction is probably backwards.** The function computes
    `error = target_angle - current_angle` and steers by `error * kp`.
    `drive_cm_gyro` steers by `+yaw_err * kp` and works, which means the gyro and
    the steering count in opposite directions. If that is right, then
    `turn_deg_gyro` fights itself and runs away from its target.

    Check that on the real hub before fixing it. Print `_yaw_deg()` before and
    after a known `turn_deg(90)` and see which sign comes back. That one experiment
    settles it, and it is a five minute job with the robot on the table.

    **What to do.** `turn_deg` works and is used everywhere. `turn_deg_gyro` has
    never been called by anything. Either finish it properly and test it, or delete
    it. Leaving a broken function next to a working one is how somebody loses a
    match at 4 pm on a Saturday.

## Your turn

At drift 12, find the lowest `kp` that keeps a 100 cm drive within 1 cm of straight.
Change one number at a time and write down what you get.

<div class="spike-run" markdown="1">

```python
DEBUG = False
sim.set_drift(12)

await init_robot()
await drive_cm_gyro(100, kp=1.0)
print("sideways error:", round(sim.pose()[0] - 30, 2), "cm")
```

</div>

??? question "How to go about it"

    Do not guess randomly. Halve the gap each time: try 1, then 4, then 2, then 3.
    Four runs gets you closer than ten random ones. It is the same method as
    guessing a number between 1 and 100.

    Write the results in a table as you go. That table is exactly what the Robot
    Design judges mean by evidence of iteration, and it belongs in
    [`robot-design/design-log.md`](../../robot-design/design-log.md).

    Then do it again on the real robot, where the answer will be different and the
    wobble is real.

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
| deadband | A band around zero small enough to ignore |
| tuning | Finding the numbers that work, by measuring |

--8<-- "includes/abbreviations.md"
