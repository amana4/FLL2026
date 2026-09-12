# 6. The maths behind a drive

The robot has no idea how far it has gone. Motors count how far they have turned,
in degrees, and that is all the information there is. So `drive_cm(30)` has to
turn 30 centimetres into a number of motor degrees before anything can happen.

That conversion is nine lines of the toolkit, and it decides whether every mission
works.

<div class="spike-run" data-view="none" markdown="1">

```python
print("1 cm  is", _cm_to_deg(1), "motor degrees")
print("10 cm is", _cm_to_deg(10), "motor degrees")
print("30 cm is", _cm_to_deg(30), "motor degrees")
```

</div>

## Working it out

Here is the function, from [`toolkit.py:45`](../library/toolkit.py):

```python
def _cm_to_deg(cm):
    effective_wheel_d = WHEEL_D_MM * CALIBRATION_SCALE
    circ_mm = pi * effective_wheel_d
    rotations = (abs(cm) * 10.0) / circ_mm
    return int(round(rotations * 360.0))
```

Four steps, and each one is a single idea.

**One.** How big is the wheel? `WHEEL_D_MM` is 62.4, the diameter in millimetres.
Ignore `CALIBRATION_SCALE` for now; it is 1.0 and it changes nothing. Lesson 9 is
about that.

**Two.** How far does the robot travel in one full wheel turn? That is the
distance around the outside of the wheel, its circumference, and the rule is
`pi × diameter`.

<div class="spike-run" data-view="none" markdown="1">

```python
from math import pi
print("wheel diameter    ", WHEEL_D_MM, "mm")
print("once around       ", round(pi * WHEEL_D_MM, 2), "mm")
print("which is          ", round(pi * WHEEL_D_MM / 10, 2), "cm")
```

</div>

So one wheel rotation moves the robot 19.6 cm. That is a useful number to hold in
your head. Half the mat is six rotations.

**Three.** How many rotations do we need? Distance divided by circumference. The
`* 10.0` is there because the distance came in as centimetres and the wheel is
measured in millimetres, and mixing the two is how you end up ten times off.

**Four.** Turn rotations into degrees, because that is what the motor understands.
One rotation is 360 degrees.

<div class="spike-run" data-view="none" markdown="1">

```python
from math import pi

cm = 30
circ_mm = pi * WHEEL_D_MM
rotations = (cm * 10.0) / circ_mm
degrees = rotations * 360.0

print("distance   ", cm, "cm")
print("circumference", round(circ_mm, 2), "mm")
print("rotations  ", round(rotations, 4))
print("degrees    ", round(degrees, 1))
print("toolkit says", _cm_to_deg(cm))
```

</div>

Change `cm` and run it again. The toolkit agrees with you every time, because you
just wrote the same thing it does.

## Why wheel size decides everything

`WHEEL_D_MM` is what the code **believes** about the wheels. If the belief is
wrong, every distance is wrong, and the robot has no way to notice.

Try it. This tells the code the wheels are 88 mm across when the real ones on this
page are 62.4 mm:

<div class="spike-run" markdown="1">

```python
WHEEL_D_MM = 88
await init_robot()
await drive_cm(30)
print(sim.pose())
```

</div>

You asked for 30 cm. You got 21.3 cm. Nothing errored, nothing warned, and a
mission built on that lands 9 cm short of a model.

Now the other way:

<div class="spike-run" markdown="1">

```python
WHEEL_D_MM = 56
await init_robot()
await drive_cm(30)
print(sim.pose())
```

</div>

33.4 cm instead of 30. Believing the wheels are smaller than they are makes the
robot drive further.

| Belief | Truth | Asked for | Actually went |
| --- | --- | --- | --- |
| 62.4 mm | 62.4 mm | 30 cm | 30.00 cm |
| 88 mm | 62.4 mm | 30 cm | 21.29 cm |
| 56 mm | 62.4 mm | 30 cm | 33.43 cm |

**Measure the wheels.** With calipers if you have them, or by rolling the robot a
metre and counting. And remember the comment at the top of the toolkit claims 87
mm while the code says 62.4 — [lesson 3](03-ports.md#find-the-problem) has the
rest of that argument.

## Turning uses the same idea

`_robot_deg_to_wheel_deg` answers a different question: to spin the robot 90
degrees, how far do the wheels have to travel?

<div class="spike-run" data-view="none" markdown="1">

```python
print("90 degrees  ->", _robot_deg_to_wheel_deg(90), "motor degrees")
print("180 degrees ->", _robot_deg_to_wheel_deg(180), "motor degrees")
print("360 degrees ->", _robot_deg_to_wheel_deg(360), "motor degrees")
```

</div>

Neat: 180 is twice 90, and 360 is four times. It is a straight proportion.

When the robot spins on the spot, each wheel drives around a circle. The diameter
of that circle is the distance between the two wheels, which is `TRACK_W_MM`, 130
mm. So a full spin makes each wheel travel `pi × 130` mm.

<div class="spike-run" data-view="none" markdown="1">

```python
from math import pi
print("track width      ", TRACK_W_MM, "mm")
print("full spin circle ", round(pi * TRACK_W_MM, 1), "mm")
print("quarter of that  ", round(pi * TRACK_W_MM / 4, 1), "mm")
print("in wheel degrees ", _robot_deg_to_wheel_deg(90))
```

</div>

A wide robot has to turn its wheels further for the same spin. That is worth
knowing when somebody proposes widening the chassis: every turn in every program
changes.

## The arc turn bug

This section is the hardest thing on the site. Skip it and come back.

[Lesson 5](05-turning.md#turning-gently) showed `arc_turn(25, 90)` turning about
121 degrees instead of 90. Here is the line that decides it, from
[`toolkit.py:345`](../library/toolkit.py):

```python
s = int(max(-100, min(100, (TRACK_W_MM / (2.0 * (radius_cm * 10.0))) * 100.0)))
```

`s` is the steering value, from 0 to 100. At 0 both wheels run at the same speed.
At 50 the inner wheel stops. At 100 it runs backwards as fast as the outer one
goes forwards, which is a spin on the spot.

So with the outer wheel at speed `v`, the inner wheel runs at `v × (1 − s/50)`.

The radius the robot actually curves on is set by the ratio between the two
wheels. Work it through with `outer` and `inner` as speeds:

```
radius = (track / 2) × (outer + inner) / (outer − inner)
```

Substitute `inner = outer × (1 − s/50)`, and `outer` cancels:

```
radius = (track / 2) × (2 − s/50) / (s/50)
       = (track / 2) × (100/s − 1)
```

Rearranged for `s`:

```
s = 100 × track / (2 × radius + track)
```

The toolkit uses `s = 100 × track / (2 × radius)`. It is missing `+ track` on the
bottom. Compare them:

<div class="spike-run" data-view="none" markdown="1">

```python
for radius_cm in (15, 25, 40, 60):
    radius_mm = radius_cm * 10.0
    theirs = 100.0 * TRACK_W_MM / (2.0 * radius_mm)
    fixed = 100.0 * TRACK_W_MM / (2.0 * radius_mm + TRACK_W_MM)
    print("radius", radius_cm, "cm  toolkit", round(theirs, 1),
          " correct", round(fixed, 1))
```

</div>

Steering too high means the arc is too tight, so the robot turns further than you
asked. That is exactly the 121 degrees instead of 90.

The fix is one line:

```python
s = int(round(100.0 * TRACK_W_MM / (2.0 * radius_cm * 10.0 + TRACK_W_MM)))
```

With that, `arc_turn(25, 90)` comes out at 92 degrees and `arc_turn(40, 90)` at
90.2. The last couple of degrees are lost because steering has to be a whole
number, so there are only so many arcs available. For anything that has to be
exact, do what the docstring says and drive each wheel its own distance with
`motor.run_for_degrees`.

??? question "Why did nobody notice?"

    Because nothing calls `arc_turn`. Search the repo: it is defined and never
    used. Code that never runs is never tested, and it sits there looking
    trustworthy until somebody reaches for it in week nine.

    Two reasonable answers: fix it, or delete it. Both are better than leaving
    it. If you fix it, `arc_turn(25, 90)` on the real robot is the test.

## Your turn

Write a program that prints, for each of 5, 10, 20, 50 and 100 cm, how many motor
degrees and how many whole wheel rotations that is.

<div class="spike-run" data-view="none" markdown="1">

```python
# your code here
```

</div>

??? question "Show one answer"

    ```python
    for cm in (5, 10, 20, 50, 100):
        degrees = _cm_to_deg(cm)
        print(cm, "cm ->", degrees, "degrees ->",
              round(degrees / 360.0, 2), "rotations")
    ```

    100 cm is about 5.1 rotations. If the answers look ten times out, check
    whether you mixed millimetres and centimetres. Everybody does it once.

## Words from this lesson

| Word | Meaning |
| --- | --- |
| diameter | The width of a circle through its middle |
| circumference | The distance around the outside of a circle, `pi × diameter` |
| pi | About 3.14159. The number that links the two |
| track width | The distance between the two driving wheels |
| radius | Half a diameter. How tightly a curve bends |
| proportion | Two things that grow together at the same rate |

--8<-- "includes/abbreviations.md"
