# 4. Driving

One function does all the straight-line driving: `drive_cm`.

<div class="spike-run" markdown="1">

```python
await init_robot()
await drive_cm(40)
```

</div>

The number is centimetres. Change the 40 and run it again. Try 100. Try 250, and
watch the robot leave the mat and turn red.

## Backwards

A negative number drives backwards. There is no separate function for it.

<div class="spike-run" markdown="1">

```python
await init_robot()
await drive_cm(50)
await drive_cm(-30)
```

</div>

Up 50, back down 30, so it ends 20 cm above where it started. Check the `y`
reading: it should read 40, from a start of 20.

Inside `drive_cm` the sign is handled by one line, at
[`toolkit.py:133`](../library/toolkit.py):

```python
vel = velocity if cm >= 0 else -velocity
```

Read it as a sentence: *velocity, if cm is zero or more, otherwise minus
velocity*. It is a compact `if`, and it is worth learning to read because the
toolkit uses the pattern more than once.

## Speed

`drive_cm` takes a second argument, `velocity`, in motor degrees per second. It
defaults to 500 when you leave it out, so `drive_cm(40)` and
`drive_cm(40, 500)` do the same thing.

<div class="spike-run" markdown="1">

```python
await init_robot()
await drive_cm(40, velocity=200)
```

</div>

That run took over twice as long. Watch the clock, not the picture: the distance
is the same, the time is not.

Writing `velocity=200` rather than just `200` is a **keyword argument**. It says
which argument you mean. With four or five optional arguments, naming them is the
difference between code you can read next month and code you cannot.

<div class="spike-run" data-height="200" markdown="1">

```python
await init_robot()
await drive_cm(30, velocity=900)
print("fast")
await drive_cm(-30, velocity=150)
print("slow")
```

</div>

## Which speed to use

Speed is a real trade-off, and it is a match strategy question, not a coding one.

| Speed | Good for | Costs you |
| --- | --- | --- |
| 800 to 1000 | Crossing the mat with nothing in the way | Overshoot, and the robot drifts more |
| 400 to 600 | Most driving. The toolkit default is 500 | Nothing much. Start here |
| 100 to 250 | The last few centimetres into a mission model | Time, and you only have 150 seconds |

A common pattern is fast to get near, slow to arrive:

<div class="spike-run" markdown="1">

```python
await init_robot()
await drive_cm(60, velocity=900)
await drive_cm(15, velocity=150)
```

</div>

## Tiny moves

For nudging into a model there is `nudge_cm`, which is `drive_cm` with small
defaults already filled in: 1.5 cm at velocity 250.

<div class="spike-run" data-height="200" markdown="1">

```python
await init_robot()
await drive_cm(40)
await nudge_cm()
await nudge_cm(-3)
print(sim.pose())
```

</div>

`sim.pose()` prints where the robot ended up, as `(x, y, heading)`. It only
exists on this website. There is no such thing on the real hub, because a real
robot has no idea where it is.

That last sentence is the most important idea in this lesson. **The robot cannot
see the mat.** It counts wheel rotations and hopes. Everything in lessons 6, 9
and 9 follows from that.

## Your turn

Drive out 80 cm, come back 40, then go out another 20 — but do the first leg fast
and the last leg slowly. Finish by printing the pose.

<div class="spike-run" markdown="1">

```python
await init_robot()
# your code here
```

</div>

??? question "Show one answer"

    ```python
    await init_robot()
    await drive_cm(80, velocity=900)
    await drive_cm(-40)
    await drive_cm(20, velocity=150)
    print(sim.pose())
    ```

    It should end at y of about 80, from a start of 20: up 80, back 40, up 20.

## Words from this lesson

| Word | Meaning |
| --- | --- |
| argument | A value you pass into a function |
| keyword argument | An argument given by name, like `velocity=200` |
| default | The value used when you leave an argument out |
| velocity | Speed, here in motor degrees per second |
| negative | Below zero. In `drive_cm` it means backwards |

--8<-- "includes/abbreviations.md"
