# Attachment — BOXOR frame

| Field | Value |
| --- | --- |
| Name | BOXOR frame attachment |
| Used by run | _TODO — link_ |
| Missions | _TODO — links_ |
| Motor(s) / port | **Two.** Left on port C (`attachment1`), right on port D (`attachment2`) |
| Passive or powered | Powered, through a bevel gear pair |
| Swap time | _TODO_ s |

## What it does

A mounting frame that sits on the chassis and carries one powered output. A motor
turns a bevel gear pair, which changes the drive direction through 90 degrees and
turns an arm. Swap the arm and the same frame does a different job.

The point of it is the mount, not the arm. One frame means every attachment lines
up the same way every time, which is design goal 3 in
[`README.md`](README.md).

**Two are fitted**, mirrored left and right across the front of the robot. Each has
its own gear cluster, its own arm, and its own motor.

## The wiring, confirmed

Six sockets, six things, one each. Read off the hub on 13 September 2026.

| Socket | What is plugged in |
| --- | --- |
| A | Left drive motor |
| B | Right drive motor |
| C | Left attachment motor |
| D | Right attachment motor |
| E | Left colour sensor |
| F | Right colour sensor |

`toolkit.py` now matches this. It did not before, and the mismatch was serious
rather than cosmetic: the file paired **port F** as a drive motor, and port F is a
colour sensor. It also had the left and right drive motors swapped.

The likely story is that somebody fixed the ports in the SPIKE App and the fix
never came back to the repo, because a program cannot be pulled off the hub.
[Lesson 3](../../code/learn/03-ports.md) tells the whole story as a worked example.

## Source

**BOXOR Frame Attachment**, by Next Level Teacher. Ten pages, eight build steps.

The instruction PDF is **not** in this repo. It is somebody else's material and
this repo is public, so it stays on the coach's machine. Ask the coach for it.

## The gear ratio, and why it matters

The frame drives its output through a **tan bevel gear pair**, visible in step 8 of
the instructions and in the photos. Step 8's parts list shows two different sizes,
which reads as the usual LEGO 20-tooth and 12-tooth pair — a ratio of 5 to 3.

So the arm does not turn as far as the motor. If it is that pair, one of these is
true:

| If the motor drives | Then `run_attachment_deg(port, 90)` moves the arm |
| --- | --- |
| the 12-tooth gear | 150 degrees |
| the 20-tooth gear | 54 degrees |

**None of this is established.** The build renders do not make the drive path
traceable, and the close-up photo is too soft to count teeth on. Guessing would put
a wrong number into a mission program.

And there are two attachments. They may not be geared the same way. Test both.

### The test that settles it

Five minutes with the robot and a protractor, per attachment:

1. Mark the arm's starting angle.
2. Run `await run_attachment_deg(attachment1, 90)`.
3. Measure how far the arm actually moved.
4. Write the answer in the table above, and the date.

Divide the arm's movement by 90 to get the ratio. Do it twice in each direction,
because the difference between the two tells you the backlash — the slop in the
gear teeth — and that is worth knowing before a mission depends on the arm
stopping in one place.

### It collides with a bug in the toolkit

`run_attachment_deg` silently discards any angle over 200 degrees
([`toolkit.py:361`](../../code/library/toolkit.py)). With this gearing that limit
is tighter than it looks:

- Driving the 12-tooth gear, 200 motor degrees is 333 degrees of arm. Probably
  more than the arm can travel anyway.
- Driving the 20-tooth gear, 200 motor degrees is only 120 degrees of arm. A
  full half-turn of the arm is not reachable through this function.

Use `move_attachment_deg` instead, which has no limit, or fix the guard. The whole
argument is in [lesson 11](../../code/learn/11-attachments.md).

## Why this design

| Option | Pros | Cons | Chosen? |
| --- | --- | --- | --- |
| BOXOR frame with swappable arms | One mount, one alignment, fast swaps | Bevel pair adds a ratio to reason about | Yes, for now |
| Motor mounted directly on the arm | No gearing, 1:1, nothing to work out | Every attachment needs its own mount and alignment | _TODO_ |
| Passive arm, no motor | Nothing to program, nothing to break | Cannot lift or push on command | _TODO_ |

Fill in the two rejected rows properly before judging. The Robot Design rubric's
CREATE row wants "Clear explanation of innovative code and/or sensor use", and the
alternatives you turned down are half of that explanation. See
[lesson 13](../../code/learn/13-flowcharts-judges.md).

## Build notes

Eight steps. The gear pair goes in at step 8, and it is the fiddly part — the
small bevel has to seat properly in the black bracket or the teeth skip under
load.

Both attachments sit on the front of the chassis, mirrored. The hub is mounted
flat and face up, so the centre button is reachable without lifting anything. That
matters at the table: a technician has to start a run one-handed.

Photos of the built robot and of the frame on the mat exist on the coach's machine
(`IMG_2222` and `IMG_2223`).

- [ ] Frame footprint, in studs and in mm. One Technic stud is 8 mm
- [ ] Arm length from pivot to tip, in cm, for each of the two arms
- [ ] How far each arm can swing before it hits the frame

Those numbers are what the [simulator](../../code/learn/README.md) needs before it
can model this attachment, and they are also what the
[field survey](../../robot-game/field-positions.md) is missing.

## Versions

| Version | Date | What changed | Why |
| --- | --- | --- | --- |
| v1 | 13 Sep 2026 | Built from the Next Level Teacher instructions, unmodified | Starting point |

## Reliability

| Date | Attempts | Successes | Notes |
| --- | --- | --- | --- |
| _TODO_ | | | |

## Photos

- [ ] Mounted on the chassis
- [ ] Detached, showing the mounting points
- [ ] Close-up of the bevel pair, with the teeth countable

That last one is worth taking. It settles the ratio question permanently, and it is
the kind of photo the engineering notebook wants.

## Status

- [x] Designed — taken from an existing design, which is allowed and worth saying
- [x] Built
- [ ] Gear ratio measured
- [ ] Tested on the field
- [ ] Durable (survives a full match)
- [ ] Swaps in under 10s

--8<-- "includes/abbreviations.md"
