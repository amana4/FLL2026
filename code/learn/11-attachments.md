# 11. Attachments

Driving gets the robot to a mission model. An attachment is what does the work when
it arrives: a hook, an arm, a fork, a lever. Most of them are one motor turning by a
set amount.

The toolkit names one attachment port at the top:

```python
attachment1 = port.C
```

<div class="spike-run" data-view="none" markdown="1">

```python
print("attachment1 is port", attachment1)
print("motor C is at", motor.relative_position(port.C), "degrees")
```

</div>

## Turning a motor by degrees

`run_attachment_deg` takes a port and a number of degrees.

<div class="spike-run" data-view="none" markdown="1">

```python
await init_robot()

await run_attachment_deg(attachment1, 90)
print("after 90: ", motor.relative_position(attachment1))

await run_attachment_deg(attachment1, 90)
print("after another 90:", motor.relative_position(attachment1))

await run_attachment_deg(attachment1, -180)
print("after -180:", motor.relative_position(attachment1))
```

</div>

There is no picture, because an attachment does not move the robot. The number is
where the motor shaft has got to, counting from zero at the start of the run.

Degrees are relative, not absolute. Each call turns *by* that much from wherever it
already is. Two 90s make 180, and -180 brings it back to zero.

## Turning a motor for a time

Sometimes you do not want a set angle. You want to push against something until it
gives, or hold a lever down while the robot drives away. Then use time.

<div class="spike-run" data-view="none" markdown="1">

```python
await init_robot()

await timed_attachment(attachment1, velocity=400, ms=250)
print("after 250 ms at 400 deg/s:", motor.relative_position(attachment1), "degrees")
```

</div>

400 degrees per second for a quarter of a second is 100 degrees, and that is what it
reports. Time and degrees are two ways of asking for the same thing, as long as
nothing gets in the way.

**Which to use.** Degrees when you know the angle and nothing will block it. Time
when the motor might stall against a model, because a `run_for_degrees` that cannot
reach its target waits for ever.

## The trap in `run_attachment_deg`

Run this. It should turn the motor a full circle.

<div class="spike-run" data-view="none" markdown="1">

```python
await init_robot()
await run_attachment_deg(attachment1, 360)
print("motor C is at", motor.relative_position(attachment1), "degrees")
```

</div>

Zero. It did nothing at all, and said nothing about it.

Here is the whole function, from [`toolkit.py:356`](../library/toolkit.py):

```python
async def run_attachment_deg(which_port, degrees, velocity=300, stop_mode=motor.BRAKE):
    """Run an attachment motor by degrees (C or D typically)."""
    if(degrees > 200):
        return
    await motor.run_for_degrees(which_port, degrees, velocity, stop=stop_mode)
```

Anything over 200 degrees is thrown away. `return` with nothing after it means "stop
here and give back nothing", so the function ends before the motor is ever asked to
move.

<div class="spike-run" data-view="none" markdown="1">

```python
await init_robot()

for degrees in (90, 200, 201, 360, -360):
    sim.reset()
    await init_robot()
    await run_attachment_deg(attachment1, degrees)
    print("asked for", degrees, "-> motor moved to",
          motor.relative_position(attachment1))
```

</div>

200 works. 201 does nothing. And -360 works fine, because the check only looks at
numbers going up.

??? question "Is that a bug or a safety feature?"

    It was probably meant as a guard. An attachment arm with a hard stop can be
    damaged by being driven past it, and a limit stops that.

    It is still wrong, for three reasons.

    - It **fails silently**. Nothing errors and nothing prints. The robot arrives at
      the model, does not lift the thing, and drives away. You find out from the
      referee.
    - It is **one-sided**. Negative angles are not checked, so the guard does not
      even protect the thing it was protecting.
    - It is in **the wrong place**. 200 degrees is a limit for one particular
      attachment. Baking it into the shared function limits every attachment the
      team will ever build.

    The honest fix is to say so out loud:

    ```python
    async def run_attachment_deg(which_port, degrees, velocity=300,
                                 stop_mode=motor.BRAKE, limit=None):
        """Run an attachment motor by degrees.

        `limit` caps the size of the move, in degrees, for attachments with a
        hard stop. Raises rather than failing quietly.
        """
        if limit is not None and abs(degrees) > limit:
            raise ValueError(
                "asked for %d degrees, limit is %d" % (degrees, limit))
        await motor.run_for_degrees(which_port, degrees, velocity, stop=stop_mode)
    ```

    Now the limit is per attachment, works in both directions, and an over-large
    move stops the program with a message instead of quietly not happening.

## The other one

There is a second function that does the same job with no limit at all:

```python
async def move_attachment_deg(which_port, degrees, velocity=1000):
    await motor.run_for_degrees(which_port, degrees, velocity=velocity)
```

<div class="spike-run" data-view="none" markdown="1">

```python
await init_robot()
await move_attachment_deg(attachment1, 360)
print("motor C is at", motor.relative_position(attachment1), "degrees")
```

</div>

360, as asked. Two functions, nearly the same name, and the only real difference is
that one of them silently refuses large moves. That is worse than either one alone,
because the next person picks whichever they find first.

**Pick one and delete the other.** This is a fair job for somebody learning the
file, and it is exactly the kind of thing the Robot Design judges want to hear about.

## Doing two things at once

Two motors can run together if you start one without awaiting it and await the other.

<div class="spike-run" data-view="none" markdown="1">

```python
await init_robot()

motor.run(port.C, velocity=300)
motor.run(port.D, velocity=-300)

await runloop.sleep_ms(500)

motor.stop(port.C)
motor.stop(port.D)

print("C:", motor.relative_position(port.C))
print("D:", motor.relative_position(port.D))
```

</div>

`motor.run` starts a motor and returns straight away, so it needs no `await`. Then
`sleep_ms` waits while both turn, and `motor.stop` ends them. One went forwards, the
other backwards, by the same amount.

This is how you lift an arm while driving, which saves real seconds in a match. It is
also how you break things, because now two mechanisms are moving and nobody is
watching either.

## Your turn

Write a function `async def lift(degrees)` that raises an arm on `attachment1`,
waits a quarter of a second for it to settle, and prints where it ended up. Then use
it to lift 150, and again to lower back to zero.

<div class="spike-run" data-view="none" markdown="1">

```python
await init_robot()
# your code here
```

</div>

??? question "Show one answer"

    ```python
    async def lift(degrees):
        """Move the arm by `degrees` and let it settle."""
        await move_attachment_deg(attachment1, degrees, velocity=300)
        await runloop.sleep_ms(250)
        print("arm at", motor.relative_position(attachment1), "degrees")

    await init_robot()
    await lift(150)
    await lift(-150)
    ```

    `move_attachment_deg` rather than `run_attachment_deg`, because 150 is under the
    200 limit today and the next person will try 250.

## Words from this lesson

| Word | Meaning |
| --- | --- |
| attachment | A mechanism on the robot that does a mission, not driving |
| relative position | How far a motor has turned since it was last zeroed |
| stall | A motor pushing against something it cannot move |
| `return` | Leave a function immediately |
| fail silently | Not work, and not say so. The worst kind of bug |
| raise | Stop the program with an error message on purpose |

--8<-- "includes/abbreviations.md"
