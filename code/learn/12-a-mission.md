# 12. Write a real mission

Everything so far has been practice. This lesson turns a plan into a file that goes
on the hub.

The example is **M11, Window to the Past**. It is the right first mission: one
condition, 20 points, and no No Equipment Constraint, so nothing has to be clear of
the model at the end. It sits centre-right at mid-depth on the mat.

Its page is [`robot-game/missions/M11-window-to-the-past.md`](../../robot-game/missions/M11-window-to-the-past.md),
and the scoring condition is one line:

> The root cover is down, touching the mat: **20**

## Start with words, not code

Write the plan in plain English first. Every line has to be something the robot can
actually do.

```
1. Start in the right launch area, facing up the mat.
2. Drive forward to the depth of the root cover.
3. Turn to face it.
4. Drive up to it slowly.
5. Push the arm down to close the cover.
6. Back away.
```

This is **pseudocode**, and FIRST names it as a skill in Session 6. It is worth the
five minutes because arguments about the plan are cheap and arguments about code are
not.

Now guess the numbers. Guesses are fine; measuring comes later.

<div class="spike-run" markdown="1">

```python
async def run():
    """M11 — push the root cover down."""
    await drive_cm_gyro(55)          # up the mat to the right depth
    await turn_deg(-90)              # face the root cover
    await drive_cm(18, velocity=200) # arrive slowly
    await run_attachment_deg(attachment1, 120)   # push the cover down
    await drive_cm(-20)              # get clear

await init_robot()
await run()
print(sim.pose())
```

</div>

Six lines and a comment on each. That is a whole mission.

## Why `run` is separate from `main`

Look at the shape of every file in [`code/missions/`](../missions/README.md):

```python
async def run():
    # the mission itself

async def main():
    await init_robot()
    await run()

runloop.run(main())
```

`run` is the mission. `main` is the setup plus the mission. They are split so that
`run` can be called from a combined program that does three missions in one launch,
without pairing the motors three times.

<div class="spike-run" markdown="1">

```python
async def run_m11():
    await drive_cm_gyro(55)
    await turn_deg(-90)
    await drive_cm(18, velocity=200)
    await run_attachment_deg(attachment1, 120)
    await drive_cm(-20)

async def run_m02():
    await turn_deg(-90)
    await drive_cm_gyro(40)
    await run_attachment_deg(attachment1, 90)

async def main():
    await init_robot()
    await run_m11()
    await run_m02()

runloop.run(main())
```

</div>

One launch, two missions, one `init_robot`. That is how a run plan in
[`robot-game/runs/`](../../robot-game/runs/README.md) becomes a program.

## Where the real work is

The code above runs. It would also score nothing, because the numbers are invented.
Turning invented numbers into real ones is the whole job, and it happens at the mat,
not at a laptop:

1. Put the robot in the launch area. Run it. Watch where it ends up.
2. Change **one** number.
3. Run it again.
4. When it works, run it ten more times and count the successes.

Step 4 is the one teams skip. A mission that works once is not a mission that works.
Eight out of ten is a mission. The mission page has an attempt log for exactly this:

| Date | Attempts | Successes | Rate | What changed |
| --- | --- | --- | --- | --- |

## Make it survive a bad day

Two habits, both cheap, both saving runs.

**Zero the gyro before anything that depends on it.** `drive_cm_gyro` does it for
you. If you write your own loop, do it yourself.

**Slow down at the end, not the whole way.** Fast where there is space, slow where
precision matters:

<div class="spike-run" markdown="1">

```python
async def run():
    await drive_cm_gyro(45, velocity=900)   # cross the open mat fast
    await turn_deg(-90)
    await drive_cm(20, velocity=180)        # approach carefully
    await nudge_cm()                        # settle against the model
    await run_attachment_deg(attachment1, 120)
    await drive_cm(-25, velocity=900)       # leave fast

await init_robot()
await run()
print(sim.pose())
```

</div>

The mission takes the same time as the all-one-speed version and hits the model more
consistently. This is the single most useful pattern in the toolkit.

## Getting it onto the hub

One awkward step, and it is not your fault. The SPIKE App's Python canvas runs one
self-contained file per slot. It cannot `import` another file, so this line at the
top of every mission file does not work on the hub:

```python
from library.toolkit import init_robot, drive_cm, drive_cm_gyro, turn_deg, run_attachment_deg
```

It is there so the file makes sense in the repo. Before loading onto the hub:

1. Open `code/library/toolkit.py` and copy all of it.
2. Paste it **above** that `import` line in the mission file.
3. Delete the `import` line.
4. Load the result into a slot in the app.

Details, and what to do about it, are in
[`code/missions/README.md`](../missions/README.md).

**And then commit the mission file.** A program that only exists on the hub is gone
when the hub is wiped or the firmware updated. The Team Meeting Guide is blunt about
it: a downloaded program cannot be pulled back off. See
[`code/spike-lessons.md`](../spike-lessons.md).

## Your turn

Pick a mission from [`robot-game/missions/README.md`](../../robot-game/missions/README.md)
that your team plans to attempt. Write the pseudocode, then write the `run` function
here and get it to do roughly the right shape on the picture.

<div class="spike-run" markdown="1">

```python
async def run():
    """MXX — what this mission does."""
    # your plan, one line at a time

await init_robot()
await run()
print(sim.pose())
```

</div>

Then put it in the real file at `code/missions/MXX-name/mission.py`, and write the
approach on the mission's page so the next person knows why the numbers are what
they are.

## Where to go next

- The official Training Camps, mapped onto our meetings:
  [`code/spike-lessons.md`](../spike-lessons.md)
- A slide-by-slide read of the toolkit: [`code/library/README.md`](../library/README.md)
- What to do when the robot misbehaves:
  [`robot-design/troubleshooting.md`](../../robot-design/troubleshooting.md)

## Words from this lesson

| Word | Meaning |
| --- | --- |
| pseudocode | The plan in plain words, before any code |
| success rate | Successes out of attempts. The only honest measure of a mission |
| combined run | One launch that scores several missions |
| slot | One of the program positions on the hub, 0 upwards |

--8<-- "includes/abbreviations.md"
