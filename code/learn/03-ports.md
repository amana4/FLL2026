# 3. Which motor is where

The hub has six sockets, labelled A to F. Every motor and sensor plugs into one of
them. Before the code can drive anything, it has to know which socket is which.

Run this:

<div class="spike-run" data-view="none" markdown="1">

```python
print("port A is", port.A)
print("port F is", port.F)
print("left drive motor is on port", LEFT_DRIVE)
print("right drive motor is on port", RIGHT_DRIVE)
```

</div>

Ports are plain numbers. `port.A` is 0 and `port.F` is 5. `port.A` is just a
friendlier way of writing 0, and the toolkit gives them a second, even friendlier
name: `LEFT_DRIVE` and `RIGHT_DRIVE`.

That is what a **variable** is. A name for a value, so you can say what you mean
once and use it everywhere.

## The setup block

Open [`code/library/toolkit.py`](../library/toolkit.py) and look at the first 40
lines. Nothing there moves a robot. It is all names for numbers.

```python
LEFT_DRIVE = port.F
RIGHT_DRIVE = port.A

left_color = port.E
right_color = port.F

attachment1 = port.C

WHEEL_D_MM = 62.4
TRACK_W_MM = 130
```

Why bother? Because if the wiring changes, you edit one line instead of hunting
through the whole file. Everything downstream says `LEFT_DRIVE`, not `port.F`.

## Why `init_robot` matters

`init_robot` hands those two names to the hub:

```python
motor_pair.pair(PAIR, LEFT_DRIVE, RIGHT_DRIVE)
```

That means "these two motors are a pair, treat them as one thing". From then on
`motor_pair` can drive both together and keep them in step. Two motors driven
separately do not stay in step, and the robot curves.

You can see what pairing does by breaking it. This asks for the same port twice:

<div class="spike-run" data-height="180" markdown="1">

```python
# expect-error
motor_pair.pair(PAIR, port.A, port.A)
await drive_cm(20)
```

</div>

## Names with an underscore in front

Some names in the toolkit start with `_`, like `_cm_to_deg` and `_yaw_deg`.

The underscore is a message from whoever wrote the file: this is a helper, used
inside the toolkit, and you probably do not need to call it yourself. Python does
not stop you. It is a convention, not a rule.

<div class="spike-run" data-view="none" markdown="1">

```python
print("30 cm is", _cm_to_deg(30), "motor degrees")
print("a 90 degree turn is", _robot_deg_to_wheel_deg(90), "motor degrees")
```

</div>

Lesson 6 is entirely about those two numbers.

## Find the problem

Everything above is real. So is this. Look at the setup block again:

```python
LEFT_DRIVE = port.F     # the left driving wheel
right_color = port.F    # the right colour sensor
```

Both are on port F. A socket holds one plug. One of those two lines is wrong, and
the code cannot tell you which, because nothing in the file uses `right_color`
yet — so nothing has ever failed.

It gets worse. The comment at the very top of the file says:

```python
# Drive: A (left), E (right)
# Wheels: 87 mm diameter
# Track width: 143 mm (center-to-center distance between wheels)
```

Three claims, and the code below disagrees with all three. The code says left is
F and right is A. It says the wheels are 62.4 mm and the track is 130 mm.

??? question "Which one do you believe, the comment or the code?"

    The code. The robot only ever runs the code. A comment cannot be wrong in a
    way that breaks a run, which is exactly why it drifts out of date without
    anybody noticing.

    So the comment is stale, and the safe reading is that somebody rebuilt the
    chassis, remeasured the wheels, updated the numbers and never came back to
    the comment at the top.

    Two jobs come out of this:

    1. Check the real robot. Which ports are the drive motors actually in? Is the
       colour sensor in E, F, or somewhere else? Measure the wheel and the track
       width. Then make the file say that.
    2. Fix or delete the comment. A comment that lies is worse than no comment,
       because it is trusted.

**Do this with the real robot in front of you, at a meeting.** It is a fifteen
minute job and it protects every distance the robot ever drives.

## Your turn

Print a line for every port the toolkit names, in the form
`port 0 right drive motor`. There are five names to cover: `LEFT_DRIVE`,
`RIGHT_DRIVE`, `left_color`, `right_color` and `attachment1`.

<div class="spike-run" data-view="none" markdown="1">

```python
# your code here
```

</div>

??? question "Show one answer"

    ```python
    print("port", RIGHT_DRIVE, "right drive motor")
    print("port", LEFT_DRIVE, "left drive motor")
    print("port", attachment1, "attachment motor")
    print("port", left_color, "left colour sensor")
    print("port", right_color, "right colour sensor")
    ```

    Printing the numbers side by side makes the clash on port 5 obvious, which is
    a fair reason to write the little program rather than read the file.

## Words from this lesson

| Word | Meaning |
| --- | --- |
| variable | A name for a value |
| port | One of the six sockets on the hub, A to F |
| pair | Telling the hub that two motors drive together |
| comment | A line starting with `#`. Python ignores it. People read it |
| convention | Something programmers agree to do, that the language does not enforce |

--8<-- "includes/abbreviations.md"
