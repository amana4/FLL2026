# 5. Turning

`turn_deg` spins the robot on the spot. The number is degrees.

<div class="spike-run" markdown="1">

```python
await init_robot()
await turn_deg(90)
```

</div>

The robot did not move across the mat. Only the heading changed, from 0 to about
90. One wheel went forwards while the other went backwards, so it turned around
its own middle.

## Which way is positive

Positive turns clockwise, so `turn_deg(90)` points the robot to the right.
Negative turns anticlockwise.

<div class="spike-run" markdown="1">

```python
await init_robot()
await drive_cm(30)
await turn_deg(-90)
await drive_cm(30)
```

</div>

Up 30, turn left, across 30. The `x` reading dropped, so the robot went to the
left as seen from home.

Getting this backwards is the single most common mistake in a mission program.
The robot ends up facing the wrong way and then drives confidently into a model.
When a run goes wrong at the second turn, check the sign first.

## Heading and 360

The heading never goes above 360 or below 0. It wraps.

<div class="spike-run" data-height="200" markdown="1">

```python
await init_robot()
await turn_deg(90)
print(sim.pose())
await turn_deg(90)
print(sim.pose())
await turn_deg(90)
print(sim.pose())
await turn_deg(90)
print(sim.pose())
```

</div>

Four right angles get back to roughly 0, not to 360. And "roughly" is the
interesting word: the last one lands near 359, not exactly 0.

That error is real, not a bug in the website. `turn_deg` converts your angle to
whole motor degrees and throws the fraction away, at
[`toolkit.py:59`](../library/toolkit.py):

```python
return int(round(wheel_rot * 360.0))
```

A fraction of a degree per turn does not matter once. Over a 150 second run with
fifteen turns in it, it does.

## Driving a square

Four sides and four turns:

<div class="spike-run" markdown="1">

```python
await init_robot()
await drive_cm(25)
await turn_deg(90)
await drive_cm(25)
await turn_deg(90)
await drive_cm(25)
await turn_deg(90)
await drive_cm(25)
await turn_deg(90)
print(sim.pose())
```

</div>

Look at the trail. It is a square, and the robot almost gets back to its starting
point but not quite. Compare the pose it printed with the start of `(30.0, 20.0,
0.0)`.

Eight lines of near-identical code should annoy you. Lesson 7 replaces the whole
thing with three.

## Half of a turn is spent doing nothing

That square took about 7.6 seconds. Time each piece and the split is strange:

| Call | Time |
| --- | --- |
| `drive_cm(25)` | 0.92 s |
| `turn_deg(90)` | 0.98 s |
| `init_robot()` | 0.50 s |

A 90 degree turn is 187 motor degrees at velocity 400, which is 0.47 seconds of
actual turning. So where does the other half second go?

The last line of `turn_deg` is `await reset_yaw()`, and `reset_yaw` ends with
`await runloop.sleep_ms(500)` at [`toolkit.py:106`](../library/toolkit.py). Every
turn waits half a second afterwards, doing nothing.

The wait is there for a reason. The gyro needs a moment to settle after the robot
stops, or the next move starts from a wrong reading. But 500 ms is a guess, and a
run with fifteen turns in it spends **7.5 seconds** on those guesses. A match is
150 seconds long.

??? question "Is that worth changing?"

    Probably, and it is a measurement rather than an argument. Drop the wait to
    200 ms, run the same mission ten times, and count how many still score. If
    ten out of ten score, you have found three seconds. If eight do, put it back.

    This is the whole of engineering in one exercise, and it belongs in
    [`robot-design/design-log.md`](../../robot-design/design-log.md) when you do
    it: what we changed, what we measured, what we decided.

## Turning gently

`turn_deg` spins on the spot. `arc_turn` curves instead, so the robot keeps moving
forwards while it turns. It takes a radius in centimetres and an angle in degrees.

<div class="spike-run" markdown="1">

```python
await init_robot()
await drive_cm(20)
await arc_turn(25, 90)
print(sim.pose())
```

</div>

Read the heading it printed. You asked for 90 degrees and got about 121.

That is not a fault in this page. `arc_turn` says so itself, in its own docstring:

```python
"""
Smooth arc using constant steering (approximate).
For precise arcs, use per-wheel degrees with motor.run_for_degrees.
"""
```

"Approximate" is doing a lot of work there. Being 31 degrees out on a 90 degree
turn is not an approximation you can plan a mission around, and the reason is a
missing term in one line of arithmetic.
[Lesson 6](06-numbers.md#the-arc-turn-bug) works out what it should say.

Until it is fixed, treat `arc_turn` as unusable and spin instead. An arc costs
space, a spin costs time, and near a mission model you usually have time and not
space, so spins were going to win most of the time anyway.

There is also `micro_turn_deg` for small corrections, which defaults to 3 degrees
at a slow speed.

<div class="spike-run" data-height="200" markdown="1">

```python
await init_robot()
await turn_deg(45)
await micro_turn_deg()
await micro_turn_deg(-6)
print(sim.pose())
```

</div>

## Your turn

Drive a triangle: three sides of 40 cm. The robot has to end up facing the way it
started.

<div class="spike-run" markdown="1">

```python
await init_robot()
# your code here
```

</div>

??? question "What angle do you turn at each corner?"

    120, not 60. You turn through the **outside** angle, not the corner of the
    triangle. Three turns of 120 add up to 360, which is a full circle, and that
    is what "ends up facing the way it started" means.

    ```python
    await init_robot()
    await drive_cm(40)
    await turn_deg(120)
    await drive_cm(40)
    await turn_deg(120)
    await drive_cm(40)
    await turn_deg(120)
    print(sim.pose())
    ```

    The same reasoning gives 90 for a square, 72 for a pentagon, and 360 divided
    by the number of sides in general.

## Words from this lesson

| Word | Meaning |
| --- | --- |
| heading | Which way the robot faces, in degrees, 0 straight up the mat |
| clockwise | The direction a clock's hands go. Positive for `turn_deg` |
| spin | Turning on the spot, wheels going opposite ways |
| arc | Turning while still moving forwards |
| rounding | Throwing away the fraction of a number |

--8<-- "includes/abbreviations.md"
