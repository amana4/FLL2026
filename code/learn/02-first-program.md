# 2. Your first program

New to all of this? [Lesson 1](01-what-is-python.md) starts further back, with no
robot in it at all.

Press **Run**. Wait a few seconds the first time, then watch.

<div class="spike-run" markdown="1">

```python
await init_robot()
await drive_cm(30)
```

</div>

Two lines. The robot set itself up, then drove 30 cm up the mat. The `y` reading
went from 20 to 50.

## What those two lines say

`init_robot()` gets the robot ready. It tells the hub which two motors are the
driving wheels and sets the gyro to zero. You call it once, at the start, and
everything after that depends on it. Delete that line and the next line fails.

Try it. Take out the first line and press Run.

<div class="spike-run" data-height="180" markdown="1">

```python
# expect-error
await drive_cm(30)
```

</div>

You get an error instead of a robot:

```
The drive motors are not paired yet. Call `await init_robot()` first
```

That is a good error. It says what is wrong and what to do. Most errors are not
this kind, so read them anyway — the useful part is usually the last line.

## The word `await`

Every line above starts with `await`. This is the one piece of Python that is
strange at the start, so here it is plainly.

`drive_cm(30)` does not happen instantly. It takes about a second, because a real
robot takes about a second to move 30 cm. `await` means:

> Start this, and do not go on to the next line until it has finished.

Without `await`, Python sets the job up and immediately moves on. Watch what
happens:

<div class="spike-run" markdown="1">

```python
await init_robot()
drive_cm(30)
print("done already?")
```

</div>

The robot never moves. `print` runs straight away, and the drive is set up but
never started, so it is thrown away.

**Rule:** if the name is in the toolkit and it moves the robot, it needs `await`.
If it just works out a number, it does not.

## Putting it in a real program

On the hub a program looks like this. Everything goes inside a function called
`main`, and the last line starts it.

<div class="spike-run" markdown="1">

```python
async def main():
    await init_robot()
    await drive_cm(20)
    await drive_cm(-20)

runloop.run(main())
```

</div>

Three new pieces:

| Piece | What it means |
| --- | --- |
| `async def main():` | Define a function called `main` that is allowed to contain `await` |
| the indented lines | The body of the function. Four spaces. Python uses the indentation to know what is inside |
| `runloop.run(main())` | Start it. Nothing happens without this line |

`drive_cm(-20)` drove back down again, which is lesson 4.

This is exactly the shape of every file in
[`code/missions/`](../missions/README.md). Open one and you will recognise it.

## Printing

`print` puts a message in the black panel under the picture. It is how you find
out what your program thinks is happening.

<div class="spike-run" data-view="none" markdown="1">

```python
print("Hello from the hub")
print("Wheel diameter is", WHEEL_D_MM, "mm")
print(2 + 2)
```

</div>

That block has no picture, because nothing moves.

You will also see lines like `yaw_before 0.0` appear on their own. Those come from
two `print` calls inside `drive_cm`, at
[`toolkit.py:130`](../library/toolkit.py) and `:143`. Every drive prints them,
whether you want them or not.

There is a `DEBUG` switch at the top of the toolkit, but `drive_cm` ignores it.
Only `drive_cm_gyro` checks it. Setting it to `False` quietens lesson 10, not this
lesson.

<div class="spike-run" data-height="180" markdown="1">

```python
DEBUG = False
await init_robot()
await drive_cm(25)
print("drive_cm still printed its yaw lines above")
```

</div>

Worth fixing one day: those two prints should sit behind `if DEBUG:` like the ones
in `drive_cm_gyro` do. Small job, real improvement, and a fair first change for
somebody learning the file.

## Your turn

Make the robot drive 60 cm, print the word `there`, drive back 60 cm, then print
`back`.

<div class="spike-run" markdown="1">

```python
await init_robot()
# your code here
```

</div>

??? question "Show one answer"

    ```python
    await init_robot()
    await drive_cm(60)
    print("there")
    await drive_cm(-60)
    print("back")
    ```

    Did it end up exactly where it started? Check the `y` reading. Lesson 6
    explains why the answer is "nearly".

## Words from this lesson

| Word | Meaning |
| --- | --- |
| `await` | Wait for this to finish before the next line |
| `async def` | A function that is allowed to contain `await` |
| function | A named piece of code you can run by name |
| argument | The value in the brackets, like the `30` in `drive_cm(30)` |
| `print` | Show a message |
| error | Python telling you it could not do what you asked |

--8<-- "includes/abbreviations.md"
