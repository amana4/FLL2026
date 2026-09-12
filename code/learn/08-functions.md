# 8. Making your own functions

A function is a name for a piece of code. You have been calling them since lesson
2: `drive_cm`, `turn_deg`, `print`. Now write your own.

<div class="spike-run" markdown="1">

```python
async def leg():
    await drive_cm(25)
    await turn_deg(90)

await init_robot()

for i in range(4):
    await leg()

print(sim.pose())
```

</div>

Two things happened. The pair of moves got a name, `leg`, and the loop got shorter.

## The shape of a definition

```python
async def leg():
    await drive_cm(25)
    await turn_deg(90)
```

| Part | Job |
| --- | --- |
| `async def` | Start a definition. `async` because the body contains `await` |
| `leg` | The name. Lower case, words joined by underscores |
| `()` | Where arguments go. Empty here |
| `:` | End of the header |
| indented lines | The body. What actually runs |

Defining a function runs nothing. `leg()` runs it. That is why `runloop.run(main())`
is on the last line of every mission program: without it, `main` is defined and
never called.

## `async def` or plain `def`

Use `async def` if the body contains `await`. Use plain `def` otherwise.

<div class="spike-run" data-view="none" markdown="1">

```python
def rotations_for(cm):
    return _cm_to_deg(cm) / 360.0

print("30 cm is", round(rotations_for(30), 2), "wheel rotations")
print("100 cm is", round(rotations_for(100), 2), "wheel rotations")
```

</div>

`rotations_for` only does arithmetic, so it is a plain `def` and you call it
without `await`.

Get it wrong and Python tells you. This tries to `await` inside a plain `def`:

<div class="spike-run" data-height="180" markdown="1">

```python
# expect-error
def broken():
    await drive_cm(10)

await broken()
```

</div>

The error says `'await' outside async function`. The fix is to add `async`.

## Arguments

A function that always drives 25 cm is not much use. Pass the distance in:

<div class="spike-run" markdown="1">

```python
async def leg(distance, angle):
    await drive_cm(distance)
    await turn_deg(angle)

await init_robot()

await leg(30, 90)
await leg(15, 90)
await leg(30, 90)
await leg(15, 90)

print(sim.pose())
```

</div>

A rectangle, from one function called four times with different numbers.
`distance` and `angle` are **parameters** — names that stand for whatever gets
passed in.

## Defaults

Give a parameter a default and callers can leave it out:

<div class="spike-run" markdown="1">

```python
async def leg(distance, angle=90):
    await drive_cm(distance)
    await turn_deg(angle)

await init_robot()

for i in range(4):
    await leg(20)

await leg(20, 45)
print(sim.pose())
```

</div>

Most calls want 90, so 90 is the default. The one call that wants something else
says so. This is how the whole toolkit is written: `drive_cm(cm, velocity=500)`
means you say the distance and you only mention speed when it matters.

Parameters with defaults have to come last in the list. `def leg(angle=90, distance)`
is an error.

## Returning a value

`return` hands an answer back.

<div class="spike-run" data-view="none" markdown="1">

```python
def seconds_for(cm, velocity=500):
    """Roughly how long a drive will take, in seconds."""
    return _cm_to_deg(cm) / velocity

print("30 cm at 500:", round(seconds_for(30), 2), "s")
print("30 cm at 200:", round(seconds_for(30, 200), 2), "s")
print("a 150 cm dash:", round(seconds_for(150, 900), 2), "s")
```

</div>

That function is genuinely useful. A match is 150 seconds and a run plan is mostly
guessing at times, so being able to add up a route before building it saves a
meeting.

The line in triple quotes is a **docstring** — a note about what the function does,
kept inside the function itself. Every function in the toolkit has one. Read them.

## Putting a whole shape in a function

<div class="spike-run" markdown="1">

```python
async def polygon(sides, side_cm):
    """Drive a closed shape with the given number of equal sides."""
    for i in range(sides):
        await drive_cm(side_cm)
        await turn_deg(360 / sides)

await init_robot()
await polygon(3, 30)
print(sim.pose())
```

</div>

Change `polygon(3, 30)` to `polygon(5, 18)` and run it again. One function, every
shape.

## Why the toolkit exists

This is the point of [`code/library/toolkit.py`](../library/toolkit.py). Nobody
wants to work out motor degrees in a mission program. `drive_cm` was written once,
carefully, and every mission gets it for free.

The same argument applies to your own code. If two missions both need to approach a
model slowly and nudge into it, that is a function, written once:

<div class="spike-run" markdown="1">

```python
async def approach(distance):
    """Cross the gap quickly, then arrive slowly and settle."""
    await drive_cm(distance - 10, velocity=900)
    await drive_cm(10, velocity=150)
    await nudge_cm()

await init_robot()
await approach(70)
print(sim.pose())
```

</div>

## Your turn

Write `async def square(side)` that drives a square of any size. Then use it three
times, for 15, 25 and 35 cm, with a turn between each so the squares do not sit on
top of each other.

<div class="spike-run" markdown="1">

```python
await init_robot()
# your code here
```

</div>

??? question "Show one answer"

    ```python
    async def square(side):
        """Drive a square with sides of `side` centimetres."""
        for i in range(4):
            await drive_cm(side)
            await turn_deg(90)

    await init_robot()
    await square(15)
    await turn_deg(30)
    await square(25)
    print(sim.pose())
    ```

    Three squares is more than 20 seconds of driving, so this answer does two.
    Getting stopped by the time limit is a fair result to notice: a real match is
    150 seconds and driving decorative shapes is not free either.

## Words from this lesson

| Word | Meaning |
| --- | --- |
| define | Write a function, without running it |
| call | Run a function by name |
| parameter | A name in the definition, standing for a value passed in |
| argument | The actual value passed in when you call it |
| default | A value used when an argument is left out |
| `return` | Hand an answer back to whoever called |
| docstring | The note in triple quotes at the top of a function |

--8<-- "includes/abbreviations.md"
