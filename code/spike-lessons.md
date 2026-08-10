# SPIKE Lessons and the Guided Mission

FIRST and LEGO Education ship a teaching sequence for exactly the skills this team
needs, and our plan ignored it entirely. `my-blocks.md` sets out to build
`drive_straight`, `turn_degrees` and line squaring from scratch, when there are
lessons that teach each one and a worked example already sitting in the repo.

Use these. They are faster than inventing it, and the coach guide schedules them.

## The prescribed order

| Order | Lesson | Teaches | Official session |
| --- | --- | --- | --- |
| 0 | Tutorial Activities 1–6 (optional) | The app, connecting the hub, basic blocks | 2 |
| 1 | **Training Camp 1: Driving Around** | Driving straight, turning, moving a set distance | 2 |
| 2 | **Training Camp 2: Playing with Objects** | Obstacle avoidance with a sensor, and powering an attachment motor | 3 |
| 3 | **Training Camp 3: Reacting to Lines** | Line detection and following with the colour sensor | 4 |
| 4 | **Guided Mission** | A complete mission, end to end | 5 |
| 5 | Assembling an Advanced Driving Base (optional) | A sturdier chassis | 5 |

All of them live in the **Competition Ready** unit in the LEGO Education SPIKE app.
Open the app, find Competition Ready, and work through in that order.

Mapped onto our meetings that is roughly M3–M4 for Training Camp 1, M5–M6 for 2,
M7–M8 for 3, and M9–M10 for the Guided Mission. See
[`official-sessions.md`](../docs/official-sessions.md).

## Why bother when we are writing My Blocks anyway

Because the Training Camps teach the *techniques* and our My Blocks are the
*packaging*. Doing them in that order means writing `drive_straight` with gyro
correction because you have seen why uncorrected driving curves — rather than
discovering it three weeks later when a run keeps missing.

Suggested split: do the Training Camp as a group, then immediately turn what it taught
into a My Block so the technique is reusable. That gives the team both the skill and
the reusable component, and it gives the design log a genuine "here is what we learned
and what we built from it" entry.

## The guided mission is already in the repo

`docs/official-materials/guided-mission-bioglow-11.llsp3` is FIRST's worked solution,
and it is available only for SPIKE Prime sets. The coach guide notes:

> "The provided program for the guided mission will not only solve the mission but
> also be helpful to use on other missions."

**Open it in the SPIKE app.** From the filename it targets Mission 11, Window to the
Past — which is a good first mission anyway: one condition, 20 points, no No Equipment
Constraint.

What is inside it, from inspecting the project file:

| Block | What it is doing |
| --- | --- |
| `setMovementPair`, `movementSpeed` | Chassis setup |
| `resetYaw` | Zeroing the gyro at the start — the habit our troubleshooting page insists on |
| `startMove`, `move` | Driving |
| `startDualSpeed` with `orientationAxis` comparisons | **Gyro-gated turns** — turning until the yaw reaches a target rather than for a fixed time |
| `isColor` on a colour sensor | **Sensor-gated stopping** — driving until a colour is seen |
| Seven `wait_until` gates | Sequencing on conditions rather than on timers |
| Two `motorTurnForDirection` | Running an attachment motor |

That is the whole toolkit. Gyro-gated turns and sensor-gated stops are what make a run
survive a battery that is no longer full — which is the single biggest cause of "it
worked last week" in [troubleshooting](../robot-design/troubleshooting.md).

**Worth doing as a team exercise:** open it, read it aloud block by block, and work out
why FIRST used `wait_until` and a gyro comparison where a beginner would have used a
timer. Then copy the pattern into our own My Blocks.

## A trap the coach guide warns about

> "After a program is downloaded on to the controller, it cannot be transferred back to
> be opened and edited." — Team Meeting Guide, p11

**The hub is not a backup.** A program that exists only on the hub is gone when the hub
is wiped or the firmware updated. So:

- Export every program to `code/spike-projects/` and commit it
- Keep a second copy on a USB stick or in the team Drive, as the guide also recommends
  on p26
- Screenshot the blocks into `code/screenshots/` so the logic is reviewable without the
  app

That is already the workflow in [`README.md`](README.md); this is the reason for it.

## Key vocabulary, session by session

From the slide decks. Useful as a drip-feed rather than handing over the whole glossary
at once, and a few of FIRST's definitions are tighter than ours.

| Session | Terms introduced |
| --- | --- |
| 1 | mission model, project spark, innovation project |
| 2 | **robot** ("the controller and any attached equipment that is intended to remain connected"), code, controller |
| 3 | research, robot game, sensor |
| 4 | **mission strategy** ("plan for missions to attempt, order to complete them, attachments and programming needed"), autonomous, match |
| 5 | solution, attachment, engineering design process |
| 6 | prototype, **pseudocode** ("simple representation of a robot's plan or simple diagrams instead of code") |
| 7 | rubric, feedback, improve |
| 8 | evaluate, expert, test |
| 9 | judge, **field** ("playing area defined by walls, including the mat, mission models, and home areas") |
| 10 | presentation, script |
| 11 | explanation, robot design |

## Checklist

- [ ] Tutorial activities, if the team is new to the app
- [ ] Training Camp 1 done, then `drive_straight` and `turn_degrees` written
- [ ] Training Camp 2 done, then `run_attachment` written
- [ ] Training Camp 3 done, then `square_to_line` written
- [ ] Guided mission opened, read as a group, and one mission scored on the field
- [ ] Every program exported, committed, and backed up off the hub

--8<-- "includes/abbreviations.md"
