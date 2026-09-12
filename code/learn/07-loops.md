# 7. Doing things again — loops

Here is the square from [lesson 5](05-turning.md#driving-a-square), all eight
lines of it:

```python
await drive_cm(25)
await turn_deg(90)
await drive_cm(25)
await turn_deg(90)
await drive_cm(25)
await turn_deg(90)
await drive_cm(25)
await turn_deg(90)
```

Copying a line four times is a warning sign. Change the side length and you have
to remember to change it in four places, and you will miss one.

Here is the same square:

<div class="spike-run" markdown="1">

```python
await init_robot()

for i in range(4):
    await drive_cm(25)
    await turn_deg(90)

print(sim.pose())
```

</div>

Change the 25 once and all four sides change. Change the 4 to a 3 and you get a
triangle shape with right-angle corners, which is worth running just to see.

## How `for` and `range` work

`range(4)` is the numbers 0, 1, 2, 3. Four numbers, starting at zero.

<div class="spike-run" data-view="none" markdown="1">

```python
for i in range(4):
    print("i is", i)

print("---")

for i in range(1, 5):
    print("counting from one:", i)

print("---")

for i in range(0, 100, 25):
    print("in steps of 25:", i)
```

</div>

| Written | Gives |
| --- | --- |
| `range(4)` | 0, 1, 2, 3 |
| `range(1, 5)` | 1, 2, 3, 4 |
| `range(0, 100, 25)` | 0, 25, 50, 75 |

The last number is never included. `range(4)` stops before 4. This catches
everybody at least once.

## The indentation is the loop

Python has no `end` and no closing bracket. What is inside the loop is decided
entirely by how far the lines are indented.

<div class="spike-run" data-height="220" markdown="1">

```python
await init_robot()

for i in range(3):
    await drive_cm(15)
    print("inside the loop, i is", i)

print("outside the loop, once only")
print(sim.pose())
```

</div>

Move that last `print` four spaces to the right and it happens three times. Four
spaces is the standard. Use the Tab key; the editor turns it into four spaces.

## Using the counter

`i` is a real variable, so you can do arithmetic with it. This drives a spiral,
each leg longer than the last:

<div class="spike-run" markdown="1">

```python
await init_robot()

for i in range(6):
    await drive_cm(10 + i * 6)
    await turn_deg(60)

print(sim.pose())
```

</div>

Six legs, six 60 degree turns, each leg 6 cm longer than the one before. Two
numbers control a shape it would take thirty lines to write out.

## Repeating without a number: `while`

`for` repeats a set number of times. `while` repeats until something becomes
false.

<div class="spike-run" data-height="220" markdown="1">

```python
await init_robot()

distance = 0
while distance < 60:
    await drive_cm(12)
    distance = distance + 12
    print("travelled", distance, "cm so far")

print(sim.pose())
```

</div>

You will meet `while` inside `drive_cm_gyro`, where it runs until the robot has
gone far enough. That is [lesson 10](10-gyro.md).

## The loop that never ends

`while` is where programs hang. If the condition never becomes false, the loop
never stops.

<div class="spike-run" data-height="180" markdown="1">

```python
# expect-error
await init_robot()

distance = 0
while distance < 60:
    await drive_cm(12)
    # the line that adds to distance is missing

print("never gets here")
```

</div>

The robot drives off the mat and keeps going. After 20 seconds the page stops it
for you and says so. On a real robot nobody stops it, and it drives into the wall
until the match ends.

The **Stop** button ends it early.

## Loops inside loops

The inner loop finishes completely, every time the outer loop goes round once.

<div class="spike-run" data-view="none" markdown="1">

```python
for row in range(3):
    for column in range(2):
        print("row", row, "column", column)
```

</div>

Six lines from two loops. Useful for a grid, rarely useful for driving.

## Your turn

Drive a hexagon with 20 cm sides using a loop. Then work out what a 12-sided shape
would need, and change two numbers to get it.

<div class="spike-run" markdown="1">

```python
await init_robot()
# your code here
```

</div>

??? question "Show one answer"

    A hexagon has six sides, so each turn is 360 divided by 6:

    ```python
    await init_robot()
    for i in range(6):
        await drive_cm(20)
        await turn_deg(60)
    print(sim.pose())
    ```

    Twelve sides means `range(12)` and `turn_deg(30)`. Better still, let Python
    do the division so the two numbers cannot disagree:

    ```python
    await init_robot()
    sides = 12
    for i in range(sides):
        await drive_cm(20)
        await turn_deg(360 / sides)
    print(sim.pose())
    ```

    Now one number controls the whole shape. That idea is the whole of
    [lesson 8](08-functions.md).

## Words from this lesson

| Word | Meaning |
| --- | --- |
| loop | Code that runs more than once |
| `for` | Repeat a set number of times |
| `range` | A run of numbers to loop over |
| `while` | Repeat until a condition becomes false |
| indentation | The spaces at the start of a line. Python uses them to group code |
| counter | The variable that holds where the loop has got to, often `i` |
| infinite loop | A loop with no way out |

--8<-- "includes/abbreviations.md"
