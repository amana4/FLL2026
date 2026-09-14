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
LEFT_DRIVE = port.A
RIGHT_DRIVE = port.B

left_color = port.E
right_color = port.F

attachment1 = port.C          # left attachment
attachment2 = port.D          # right attachment

WHEEL_D_MM = 62.4
TRACK_W_MM = 130
```

Six sockets, six things, one each. That is the whole wiring diagram.

Why bother naming them? Because if the wiring changes, you edit one line instead of
hunting through the whole file. Everything downstream says `LEFT_DRIVE`, not
`port.A`.

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

Everything above is real. So is this, and it is a bug we actually found and fixed.

Until 13 September 2026 the setup block read like this:

```python
LEFT_DRIVE = port.F     # the left driving wheel
RIGHT_DRIVE = port.A    # the right driving wheel

left_color = port.E
right_color = port.F    # the right colour sensor
#attachment2 = port.E   # commented out
```

Two sockets claimed twice. **F** held the left drive motor and the right colour
sensor. **E** held the left colour sensor and, the moment anybody uncommented that
line, the second attachment motor. Meanwhile B and D sat empty.

A socket holds one plug. So the file was describing a robot that cannot exist.

### It was worse than a clash

Somebody then read the port letters off the hub. The real wiring is:

| Socket | What is plugged in | The old file said |
| --- | --- | --- |
| A | left drive motor | right drive motor |
| B | right drive motor | nothing |
| C | left attachment motor | first attachment motor |
| D | right attachment motor | nothing |
| E | left colour sensor | left colour sensor |
| F | right colour sensor | left drive motor **and** right colour sensor |

Read the A and F rows again. The old file paired **port F** as a drive motor, and
port F is a colour sensor. It also called port A the *right* drive when it is the
*left* one.

So `init_robot` was asking the hub to pair a colour sensor with a motor, and to
treat the left wheel as the right one. That does not drive slightly wrong. That
does not drive.

??? question "How did nobody notice?"

    Almost certainly because the working version lived on the hub and never came
    back to the repo. The Team Meeting Guide is blunt about this:

    > "After a program is downloaded on to the controller, it cannot be transferred
    > back to be opened and edited."

    So somebody fixed the ports in the app, the robot drove, and the file in git
    kept the old numbers. See [`code/spike-lessons.md`](../spike-lessons.md).

    **The hub is not a backup.** This is what that costs: a file that looks
    authoritative and is not.

### The comment was half right

The header at the top of the file used to say:

```python
# Drive: A (left), E (right)
# Wheels: 87 mm diameter
# Track width: 143 mm (center-to-center distance between wheels)
```

"A (left)" turned out to be **correct**, and the code below it was wrong. "E
(right)" is wrong — B is the right drive.

So the comment was not simply stale. It was a fossil of an older, partly correct
wiring, and it disagreed with the code in both directions.

The wheel and track numbers are **still unsettled**. The comment says 87 mm and
143 mm, the code says 62.4 mm and 130 mm, and nobody has put calipers on the robot.
[Lesson 6](06-numbers.md) shows exactly what a wrong wheel diameter costs.

- [ ] Measure the wheel diameter
- [ ] Measure the track width, wheel centre to wheel centre
- [ ] Make the file say that, and fix the header

**Do this with the real robot in front of you, at a meeting.** It is a fifteen
minute job and it protects every distance the robot ever drives.

## Your turn

Print a line for every port the toolkit names, in the form
`port 0 left drive motor`. There are six names to cover: `LEFT_DRIVE`,
`RIGHT_DRIVE`, `attachment1`, `attachment2`, `left_color` and `right_color`.

<div class="spike-run" data-view="none" markdown="1">

```python
# your code here
```

</div>

??? question "Show one answer"

    ```python
    print("port", LEFT_DRIVE, "left drive motor")
    print("port", RIGHT_DRIVE, "right drive motor")
    print("port", attachment1, "left attachment motor")
    print("port", attachment2, "right attachment motor")
    print("port", left_color, "left colour sensor")
    print("port", right_color, "right colour sensor")
    ```

    Six lines, and the numbers should come out 0 to 5 with no repeats. Printing
    them side by side is how the clash on port 5 was spotted in the first place,
    which is a fair reason to write the little program rather than read the file.

## Words from this lesson

| Word | Meaning |
| --- | --- |
| variable | A name for a value |
| port | One of the six sockets on the hub, A to F |
| pair | Telling the hub that two motors drive together |
| comment | A line starting with `#`. Python ignores it. People read it |
| convention | Something programmers agree to do, that the language does not enforce |

--8<-- "includes/abbreviations.md"
