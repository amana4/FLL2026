# 1. What is Python?

Never written code before? Start here. There is no robot on this page.

## A program is a list of instructions

Think about telling somebody how to make toast. Bread in the toaster. Push the
lever. Wait. Take it out. Four instructions, in order, and the order matters.

A program is the same thing written for a computer. Two differences, and both
catch people out.

**A computer does exactly what you say.** Not what you meant. If you tell it to
take the toast out before pushing the lever, it will.

**A computer never gets bored.** Ask it to do something four hundred times and it
does it four hundred times, at the same speed each time. That is why the robot
can drive the same route every match.

Python is one way of writing those instructions down. It is the same language used
for websites, science and film effects. Ours happens to drive a LEGO robot.

## Your first line

Press **Run**. The first time takes a few seconds while Python loads.

<div class="spike-run" data-view="none" markdown="1">

```python
print("Hello")
```

</div>

`print` means "show this". The words inside the quotes appear in the black panel.

Change `Hello` to your name and run it again. Add more lines:

<div class="spike-run" data-view="none" markdown="1">

```python
print("Hello")
print("I am learning Python")
print("This is line three")
```

</div>

Three instructions, done in order, top to bottom. That is all a program is.

## Python is fussy

Computers do not guess. Leave out one quote mark and the whole thing stops.

Run this. It is broken on purpose.

<div class="spike-run" data-view="none" markdown="1">

```python
# expect-error
print("Hello)
```

</div>

You get `SyntaxError`, which means "I cannot even read this". The closing quote is
missing, so Python never finds the end of the words.

Here is a different mistake:

<div class="spike-run" data-view="none" markdown="1">

```python
# expect-error
pirnt("Hello")
```

</div>

`NameError: name 'pirnt' is not defined`. Python has never heard of `pirnt`. It
does not suggest `print`, because guessing is exactly what it refuses to do.

And one more:

<div class="spike-run" data-view="none" markdown="1">

```python
# expect-error
print(score)
```

</div>

`NameError` again. You asked it to show `score`, and nothing called `score` exists
yet.

**Errors are normal.** Everybody gets them, all day. The skill is not avoiding them,
it is reading them. Two habits:

1. Read the **last line** first. That is the actual problem.
2. Look for the line number. Python tells you where it gave up.

Nothing here can be broken. Press **Start again** and you get the original code
back.

## Python does arithmetic

<div class="spike-run" data-view="none" markdown="1">

```python
print(2 + 2)
print(10 - 3)
print(6 * 7)
print(20 / 4)
print((2 + 3) * 10)
```

</div>

| Symbol | Means |
| --- | --- |
| `+` | add |
| `-` | take away |
| `*` | times |
| `/` | divide |
| `( )` | do this bit first |

`*` and `/` instead of the signs you write at school, because a keyboard has no
times sign. Brackets work exactly as they do in maths.

Notice `20 / 4` printed `5.0`, not `5`. Division always gives a number with a
decimal point, even when it comes out even.

## Words and numbers are different things

Quotes make a difference:

<div class="spike-run" data-view="none" markdown="1">

```python
print(2 + 2)
print("2 + 2")
```

</div>

The first is a sum. The second is four characters of text, and Python shows them
back unchanged. Text in quotes is called a **string**.

You can print both at once by separating them with commas:

<div class="spike-run" data-view="none" markdown="1">

```python
print("Two plus two is", 2 + 2)
print("Our wheels are", 62.4, "mm across")
```

</div>

Python puts a space in for you at each comma.

Mixing them up is an error, and it is a common one:

<div class="spike-run" data-view="none" markdown="1">

```python
# expect-error
print("Score: " + 20)
```

</div>

`TypeError` means you used the wrong kind of thing. `+` joins two strings or adds
two numbers, but it will not glue a number onto a string. Use a comma.

## Giving things names

A **variable** is a name for a value. You make one with `=`.

<div class="spike-run" data-view="none" markdown="1">

```python
score = 20
print(score)
print(score * 3)
```

</div>

`=` does not mean "equals" the way it does in maths. It means "put this value into
this name". So this makes sense in Python and not in maths:

<div class="spike-run" data-view="none" markdown="1">

```python
score = 20
print("at the start:", score)

score = score + 10
print("after scoring M11:", score)

score = score + 30
print("after scoring M08:", score)
```

</div>

Read `score = score + 10` as "make the new score equal to the old score plus ten".

Why bother? Because the name says what the number means. Compare:

```python
await drive_cm(55)
```

with

```python
distance_to_root_cover = 55
await drive_cm(distance_to_root_cover)
```

The second explains itself, and if the distance changes you fix it in one place.
That is why the toolkit is full of names like `WHEEL_D_MM` and `LEFT_DRIVE`.

### Naming rules

- Letters, numbers and underscores. No spaces.
- Cannot start with a number.
- Capitals matter: `score` and `Score` are two different names.
- Use lower case with underscores: `wheel_size`, not `WheelSize`.

## Notes to humans

A line starting with `#` is a **comment**. Python skips it completely.

<div class="spike-run" data-view="none" markdown="1">

```python
# This line does nothing at all.
print("but this one runs")   # and so does this, up to the hash

# print("this is switched off")
```

</div>

Comments are for explaining *why*, not *what*. `# add 10 to score` is useless
next to `score = score + 10`. `# 10 points per leaf, from the rulebook` is worth
having.

## Asking a question

So far every line runs. `if` lets a program choose.

<div class="spike-run" data-view="none" markdown="1">

```python
score = 45

if score > 40:
    print("Good run")
```

</div>

Change the 45 to 20 and run it again. Nothing prints, because 20 is not more than
40.

Add an `else` for the other case:

<div class="spike-run" data-view="none" markdown="1">

```python
score = 20

if score > 40:
    print("Good run")
else:
    print("Try again")
```

</div>

| Symbol | Means |
| --- | --- |
| `>` | more than |
| `<` | less than |
| `>=` | more than or the same as |
| `<=` | less than or the same as |
| `==` | the same as |
| `!=` | not the same as |

**`=` and `==` are different.** One puts a value into a name, the other asks a
question. Mixing them up is the single most common beginner mistake in any
language.

### The spaces at the start of a line matter

Look again at what sits under the `if`:

```python
if score > 40:
    print("Good run")
print("Match over")
```

The indented line only runs when the answer is yes. The line that is not indented
always runs. Python uses those four spaces to work out what belongs to what, where
most languages use brackets.

<div class="spike-run" data-view="none" markdown="1">

```python
score = 20

if score > 40:
    print("Good run")
    print("both of these only happen when the score is over 40")

print("this one always happens")
```

</div>

Use the Tab key. The editor on this page turns it into four spaces.

## Your turn

Make a variable called `leaves` holding how many leaves the robot collected, 0, 1
or 2. Print the points, at 10 points each. Then print `bonus` if it got both.

<div class="spike-run" data-view="none" markdown="1">

```python
leaves = 2
# your code here
```

</div>

??? question "Show one answer"

    ```python
    leaves = 2

    points = leaves * 10
    print("leaves:", leaves)
    print("points:", points)

    if leaves == 2:
        print("bonus")
    ```

    Change `leaves` to 1 and run it again. The bonus line should disappear.

    Two `=` in `leaves == 2`, because that is a question, not an instruction.
    That is M04 from the [mission page](../../robot-game/missions/M04-lucky-leaves.md),
    give or take the rule about the katydid.

## Now the robot

Everything above is ordinary Python. Here is the same language driving a robot:

<div class="spike-run" markdown="1">

```python
await init_robot()
await drive_cm(30)
```

</div>

A picture appeared, because that code moves something.
[Lesson 2](02-first-program.md) explains every word of it.

## Words from this lesson

| Word | Meaning |
| --- | --- |
| program | A list of instructions, done in order |
| `print` | Show something |
| string | Text, written inside quotes |
| variable | A name holding a value |
| `=` | Put this value into this name |
| `==` | Ask whether two things are the same |
| comment | A line starting with `#`. Python ignores it |
| `if` | Only do this when something is true |
| indentation | The four spaces that say which lines belong together |
| error | Python saying it could not do what you asked |
| `SyntaxError` | Python cannot read your code at all |
| `NameError` | You used a name Python has never seen |
| `TypeError` | You used the wrong kind of thing, like adding a number to text |

--8<-- "includes/abbreviations.md"
