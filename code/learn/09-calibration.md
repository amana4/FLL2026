# 9. When the robot lies to you

The robot counts wheel degrees and multiplies. It cannot check the answer. So when
the answer is wrong, it is confidently wrong, every single run.

This lesson is how you find out and how you fix it.

## Making the robot wrong on purpose

`sim.set_true_wheel_diameter` changes what the pretend wheels really measure. The
toolkit's `WHEEL_D_MM` is untouched, so the code still believes 62.4 mm.

<div class="spike-run" markdown="1">

```python
sim.set_true_wheel_diameter(56.0)

await init_robot()
await drive_cm(30)
print("asked for 30 cm, ended at y =", sim.pose()[1], "from a start of 20")
```

</div>

It went 26.9 cm, not 30. A 10 percent error, silently.

A real robot is wrong for the same reason plus several more: tyres compress under
weight, the mat has a different grip from the table it is tested on, and a
half-charged battery turns slower than a full one.

## Measuring the error

The trick is to stop guessing at the cause and measure the effect.

1. Tell the robot to drive a long, known distance. Long, because a 2 mm error over
   20 cm is hard to see and the same error over 180 cm is not.
2. Measure what it actually did, with a tape measure.
3. Write both numbers down.

That is what these lines in [`toolkit.py:390`](../library/toolkit.py) are:

```python
print(set_calibration_scale(179.7/180))  # Home mat Actual/ requested
#print(set_calibration_scale(319/300))   # Hardwood
```

Somebody asked for 180 cm on the home mat and got 179.7. Then asked for 300 cm on
a hardwood floor and got 319. Those are two real measurements, and they say the
robot needs different numbers on different surfaces.

<div class="spike-run" data-view="none" markdown="1">

```python
from math import pi

for name, actual, requested in (("home mat", 179.7, 180),
                                ("hardwood", 319, 300)):
    scale = actual / requested
    print(name, "  scale", round(scale, 4),
          "  effective wheel", round(WHEEL_D_MM * scale, 2), "mm")
```

</div>

On the mat the correction is tiny. On hardwood the code has to pretend the wheels
are 66.35 mm instead of 62.4, a 6 percent change, because the robot was
over-travelling badly.

**Calibrate on the surface you will compete on.** A number measured on the kitchen
floor is worse than no number at all.

## The correction

`CALIBRATION_SCALE` sits in `_cm_to_deg`, in one line:

```python
effective_wheel_d = WHEEL_D_MM * CALIBRATION_SCALE
```

The code keeps believing the wheels are 62.4 mm. The scale nudges what it does with
that belief. Two functions set it.

`set_calibration_scale(scale)` takes the number directly, which is what you use once
you know it:

<div class="spike-run" markdown="1">

```python
sim.set_true_wheel_diameter(56.0)

print("scale is now", set_calibration_scale(26.93 / 30))

await init_robot()
await drive_cm(30)
print("asked for 30 cm, got", round(sim.pose()[1] - 20, 2))
```

</div>

30.01 cm. One measurement fixed it.

`calibrate_wheel_diameter(commanded, measured)` does the division for you, which is
friendlier at a meeting with a tape measure in your hand:

<div class="spike-run" markdown="1">

```python
sim.set_true_wheel_diameter(56.0)

scale = calibrate_wheel_diameter(30, 26.93)
print("scale", round(scale, 4), " effective wheel",
      round(WHEEL_D_MM * scale, 2), "mm")

await init_robot()
await drive_cm(30)
print("30 cm ->", round(sim.pose()[1] - 20, 2))
```

</div>

It worked out an effective diameter of 56.01 mm, which is the real answer to within
a hundredth of a millimetre. Not because it is clever, but because the relationship
is a straight proportion: twice the error over twice the distance.

## One measurement fixes every distance

This is the part worth being convinced by. Calibrate once, at 30 cm, then drive
something completely different:

<div class="spike-run" markdown="1">

```python
sim.set_true_wheel_diameter(56.0)
calibrate_wheel_diameter(30, 26.93)

await init_robot()
await drive_cm(80)
print("asked for 80 cm, got", round(sim.pose()[1] - 20, 2))
```

</div>

80.0 cm. The scale is not a patch for one distance, it is a correction to the
belief, so it works everywhere.

## What calibration does not fix

Only distance. It does nothing about:

- **Turning.** `_robot_deg_to_wheel_deg` uses `CALIBRATION_SCALE` too, but the
  number that decides a turn is `TRACK_W_MM`, and nothing here calibrates that.
  Turns need their own measurement: ask for four 90 degree turns and see whether
  the robot comes back to where it started.
- **Drifting off straight.** That is [lesson 10](10-gyro.md).
- **A wheel that slips.** No amount of arithmetic fixes a wheel spinning on a
  smooth patch of mat.

## The routine to actually use

At the start of a practice session, on the competition mat:

1. Put the robot on a straight edge of the mat. Note where the front is.
2. Run `await drive_cm(180)`.
3. Measure how far it went, in centimetres, honestly.
4. Put `set_calibration_scale(measured / 180)` at the top of `main()`.
5. Run `await drive_cm(180)` again and check it lands within a centimetre.
6. Write the number and the date in
   [`robot-design/design-log.md`](../../robot-design/design-log.md).

Step 6 is the one that gets skipped and the one that pays. When the robot is
mysteriously wrong in three weeks, the log tells you whether the number changed.

## Your turn

The pretend wheels are set to 60 mm below. Measure the error and correct it,
without being told the answer.

<div class="spike-run" markdown="1">

```python
sim.set_true_wheel_diameter(60.0)

await init_robot()
await drive_cm(100)
print("uncorrected:", round(sim.pose()[1] - 20, 2), "cm")

# now work out the scale and set it
```

</div>

??? question "Show one answer"

    Run the first part, read the number, then use it. `sim.reset()` puts the robot
    back at the start so the second measurement is clean, and `init_robot` has to
    be called again afterwards because resetting unpairs the motors.

    ```python
    sim.set_true_wheel_diameter(60.0)

    await init_robot()
    await drive_cm(100)
    measured = sim.pose()[1] - 20
    print("uncorrected:", round(measured, 2), "cm")

    calibrate_wheel_diameter(100, measured)

    sim.reset()
    await init_robot()
    await drive_cm(100)
    print("corrected:  ", round(sim.pose()[1] - 20, 2), "cm")
    ```

    Reading `sim.pose()` is standing in for a tape measure. On the real robot that
    step is a person on their knees on the floor, and it is the only step that
    matters.

    You should get about 96.15 uncorrected, a scale near 0.9615, and 100 after.
    And 62.4 times 0.9615 is 60.0, which is the answer you were not told.

## Words from this lesson

| Word | Meaning |
| --- | --- |
| calibrate | Measure the error, then correct for it |
| scale | A multiplier that stretches or shrinks a number |
| proportion | Double the distance, double the error |
| systematic error | An error that happens the same way every time, so it can be corrected |
| slip | A wheel turning without the robot moving. Not correctable |

--8<-- "includes/abbreviations.md"
