# 15. Test our code: a simulator quiz

This quiz tests the parts of our code a judge is most likely to ask about:
`drive_cm`, `face`, the gyro, and the safety stops. Every Run button on this page
runs on our real library, [`advanced.py`](../library/advanced.py), the same code
that is on the robot.

**How each question works:**

1. Read the question and write your guess down first. Guessing first is the
   point: it shows what you really understand.
2. Press **Run** and watch the robot.
3. Open the **Answer** box and check.

Every block starts by setting up the pretend robot, for example
`sim.set_drift(0)` for a robot that drives perfectly straight. The pretend
robot remembers these settings between Run buttons, so each block sets its own.

The facts behind these questions are in
[Our key facts](../../robot-design/exceeds-prep.md#our-key-facts).

## Part 1: drive_cm

### Question 1: does drive_cm(30) drive exactly 30 cm?

The robot starts at 20 cm up the mat. `sim.pose()` prints where it ends: across,
up, and which way it points. **Guess:** how far up does it end?

<div class="spike-run" data-lib="advanced" markdown="1">

```python
sim.set_drift(0)
sim.set_true_wheel_diameter(62.4)

await init_robot()
await drive_cm(30)
print(sim.pose())
```

</div>

??? question "Answer"
    It ends at about 48.7 cm up, so it drove about 28.7 cm, not 30.

    `drive_cm` brakes 1.4 cm early on purpose. A real robot rolls on a little
    after the brakes go on, and that roll carries it onto the mark. The pretend
    robot stops dead, so here you see the gap.

### Question 2: what if the wheels are bigger than the code thinks?

Our code says the wheels are 62.4 mm across. This block gives the pretend robot
66 mm wheels. **Guess:** will `drive_cm(100)` go further or shorter than before?

<div class="spike-run" data-lib="advanced" markdown="1">

```python
sim.set_drift(0)
sim.set_true_wheel_diameter(66)

await init_robot()
await drive_cm(100)
print(sim.pose())
```

</div>

??? question "Answer"
    Further: it ends at about 124.3 cm up instead of about 118.7 cm. Each turn of
    a bigger wheel covers more ground, so the same number of turns goes further.

    This is why we changed one number when we reused last year's `drive_cm`: last
    year's wheels were 88 mm, ours are 62.4 mm. It is also what
    `set_calibration_scale(179/180)` fixes on our real robot. This fixes the
    pretend one:

    ```python
    sim.set_drift(0)
    sim.set_true_wheel_diameter(66)

    await init_robot()
    set_calibration_scale(66 / 62.4)
    await drive_cm(100)
    print(sim.pose())
    ```

    Now it ends at about 118.7 cm again.

### Question 3: what does the gyro correction do?

`sim.set_drift(8)` makes the robot veer, like a real robot with one tyre gripping
better than the other. `kp=0, kd=0` switches our gyro correction off. **Guess:**
how far sideways does it end up, with the correction off and then on?

<div class="spike-run" data-lib="advanced" markdown="1">

```python
sim.set_drift(8)
sim.set_true_wheel_diameter(62.4)

await init_robot()
await drive_cm(60, kp=0, kd=0)
print("gyro correction OFF:", sim.pose())
```

</div>

<div class="spike-run" data-lib="advanced" markdown="1">

```python
sim.set_drift(8)
sim.set_true_wheel_diameter(62.4)

await init_robot()
await drive_cm(60)
print("gyro correction ON: ", sim.pose())
```

</div>

??? question "Answer"
    With the correction off, it ends about 8 cm to the right of 30 and points
    about 16 degrees off. With it on, it ends within about 1 cm of 30 and points
    about 1 degree off.

    Every 15 milliseconds, `drive_cm` reads the yaw. If the robot has drifted, it
    steers back: `trim = -(18.9 x error + 5.25 x change)`. The further off, the
    harder it steers.

### Question 4: what happens if you type millimetres?

Word Blocks use millimetres. Our Python uses centimetres. **Guess:** what does
`drive_cm(300)` do?

<div class="spike-run" data-lib="advanced" markdown="1">

```python
# expect-error
sim.set_drift(0)

await init_robot()
await drive_cm(300)
```

</div>

??? question "Answer"
    It refuses, with: "300 cm is longer than the mat. The Word Blocks take
    millimetres and this takes centimetres, so .Forward 300 is drive_cm(30)."

    The mat is only 200 cm wide, so 300 cm is always a mistake. This is one of our
    safety stops.

## Part 2: face, and the yaw

**Yaw** is the direction the robot is pointing, in degrees, like a compass.
`bearing()` prints it.

### Question 5: what does face(30) do to the yaw?

**Guess:** what does `bearing()` print after `face(30)`?

<div class="spike-run" data-lib="advanced" markdown="1">

```python
sim.set_drift(0)

await init_robot()
await face(30)
print("yaw:", round(bearing()))
```

</div>

??? question "Answer"
    About 30. `face(30)` turns until the yaw is 30 degrees from where the robot
    pointed when `init_robot()` zeroed it.

### Question 6: face twice, or turn twice?

`face(90)` turns **to** 90. `turn_deg(90)` turns **by** 90. **Guess:** what is
the yaw after doing each one twice?

<div class="spike-run" data-lib="advanced" markdown="1">

```python
sim.set_drift(0)

await init_robot()
await face(90)
await face(90)
print("face twice:", round(bearing()))
```

</div>

<div class="spike-run" data-lib="advanced" markdown="1">

```python
sim.set_drift(0)

await init_robot()
await turn_deg(90)
await turn_deg(90)
print("turn twice:", round(bearing()))
```

</div>

??? question "Answer"
    `face` twice: about 90. The second `face(90)` does nothing, because the robot
    already points at 90.

    `turn_deg` twice: about 180. Each one turns another quarter.

    That is why our runs use `face`: every turn is measured from the start, so a
    small mistake in one turn is not passed on to the next.

### Question 7: what does zeroing the yaw do?

We zero the yaw at the start of every mission program. Here the robot turns to
45, then zeroes the yaw again with `reset_yaw()`. **Guess:** after that, which
way does `face(0)` point the robot?

<div class="spike-run" data-lib="advanced" markdown="1">

```python
sim.set_drift(0)

await init_robot()
await face(45)
await reset_yaw()
print("yaw after zeroing:", round(bearing()))
await face(0)
print(sim.pose())
```

</div>

??? question "Answer"
    It stays pointing at about 45 on the mat, because zeroing makes the way the
    robot points right now become 0. The pose shows about 45 degrees.

    So zeroing at the start matters. Every `face` in the run is measured from the
    way the robot pointed at that moment. Put the robot down the same way every
    time, square on the wall, and every run turns the same way.

### Question 8: what if the gyro counts the wrong way?

`YAW_SIGN` tells the code which way our gyro counts. Ours is `-1`. This block sets
it to `1`, the wrong way. A real robot always drifts a little, so the block adds a
small drift too. **Guess:** what happens?

<div class="spike-run" data-lib="advanced" markdown="1">

```python
# expect-error
sim.set_drift(3)
YAW_SIGN = 1

await init_robot()
await drive_cm(40)
```

</div>

??? question "Answer"
    It stops with an error that starts "Straight drive is" and then says how many
    degrees off course it got, over 45. With the sign wrong, the correction steers
    the same way as the drift instead of against it, and the robot spins. Our safety stop brakes once it is 45 degrees off, instead of
    spinning off the table.

    This really happened on 20 September, before the safety stop existed.

## Part 3: simulated missions

The field report at the end scores the missions. M10 scores 20 points for
leaving both habitats alone, so a run that does nothing still scores 20.

### Question 9: score M02 Exploding Seeds

The robot starts in the left home, faces the seeds, drives to them, and swings
the attachment. **Guess:** how many points does M02 score?

<div class="spike-run" data-lib="advanced" data-height="320" markdown="1">

```python
sim.set_drift(0)

await init_robot()
await face(44)
await drive_cm(41)
await run_attachment_deg(attachment1, 180)
field.report(only_scoring=True)
```

</div>

??? question "Answer"
    M02 scores 30 out of 30, with all 3 seeds. The total is 50: 30 for M02 and 20
    for leaving M10 alone.

### Question 10: does the gyro matter on a long drive?

M11 Window to the Past is 109 cm away. Both blocks have drift. The first switches
the gyro correction off. **Guess:** which one scores M11?

<div class="spike-run" data-lib="advanced" data-height="320" markdown="1">

```python
sim.set_drift(6)

await init_robot()
await face(70)
await drive_cm(109, kp=0, kd=0)
await run_attachment_deg(attachment1, 120)
field.report(only_scoring=True)
```

</div>

<div class="spike-run" data-lib="advanced" data-height="320" markdown="1">

```python
sim.set_drift(6)

await init_robot()
await face(70)
await drive_cm(109)
await run_attachment_deg(attachment1, 120)
field.report(only_scoring=True)
```

</div>

??? question "Answer"
    Only the second. With the correction off, the robot curves away and misses
    M11, so the total is just the 20 for M10. With it on, M11 scores 20 out of 20.

    On a short drive, like the 41 cm to M02, drift hardly matters. On a long drive
    it decides the mission. That is why the gyro does the driving.

### Question 11: challenge, two missions in one run

Write one run that scores M02 **and** M11. The start is done for you. Some hints:

- After the seeds, drive back with a negative distance.
- Put the attachment back with a negative number of degrees.
- `face` measures from the start, so `face(70)` works wherever you are pointing.

<div class="spike-run" data-lib="advanced" data-height="320" markdown="1">

```python
sim.set_drift(6)

await init_robot()
await face(44)
await drive_cm(41)
await run_attachment_deg(attachment1, 180)

# Your code here: back off, then go and score M11.

field.report(only_scoring=True)
```

</div>

??? question "Answer"
    One run that scores both, for a total of 70: 30 for M02, 20 for M11 and 20
    for M10. It works even with drift on, because the gyro corrects it.

    ```python
    sim.set_drift(6)

    await init_robot()
    await face(44)
    await drive_cm(41)
    await run_attachment_deg(attachment1, 180)
    await drive_cm(-41)
    await run_attachment_deg(attachment1, -180)
    await face(70)
    await drive_cm(109)
    await run_attachment_deg(attachment1, 120)
    field.report(only_scoring=True)
    ```

    Doing two missions in one trip is our real strategy too: fewer trips back to
    base means more time for scoring.

## What one thing on this page can't show

On the real hub, an arm command without `await` starts the arm and carries on to
the next line, so the arm and the drive happen together. The end of
`phase0-alt.py` uses that. The pretend robot doesn't copy this: without `await`,
its arm doesn't move at all. Test that one on the real robot.

## Next

Explain each answer to a teammate, the way you would to a judge. Then take the
strategy quiz, and practise the code part of the
[five-minute explanation](../../robot-design/exceeds-prep.md#6-the-five-minute-explanation).

--8<-- "includes/abbreviations.md"
