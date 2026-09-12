# Learn Python with our robot

Thirteen short lessons, starting from "what is a program" and ending at "explain it
to a judge". Every one has code you can change and run right here in the page, most
with a top-down view of the robot moving on the mat.

The code is not a toy version. Each page loads our real
[`code/library/toolkit.py`](../library/toolkit.py) and calls the same
`drive_cm` and `turn_deg` the competition programs use. If someone edits the
toolkit, these pages change with it.

## The lessons

| | Lesson | What you can do at the end |
| --- | --- | --- |
| 1 | [What is Python?](01-what-is-python.md) | Print, do sums, use a variable, read an error. No robot |
| 2 | [Your first program](02-first-program.md) | Make the robot move, and explain what `await` is for |
| 3 | [Which motor is where](03-ports.md) | Read the setup block at the top of the toolkit |
| 4 | [Driving](04-driving.md) | Drive any distance, forwards and backwards, fast or slow |
| 5 | [Turning](05-turning.md) | Turn by degrees, and drive a square |
| 6 | [The maths behind a drive](06-numbers.md) | Explain why wheel size decides the distance |
| 7 | [Doing things again — loops](07-loops.md) | Use `for` and `range` instead of copying lines |
| 8 | [Making your own functions](08-functions.md) | Write `def`, take arguments, give a default |
| 9 | [When the robot lies to you](09-calibration.md) | Measure the error, then correct it |
| 10 | [The gyro](10-gyro.md) | Explain why `drive_cm_gyro` drives straighter |
| 11 | [Attachments](11-attachments.md) | Run a motor on port C by degrees or by time |
| 12 | [Write a real mission](12-a-mission.md) | Turn a plan into a mission program |
| 13 | [Flowcharts, and explaining your code](13-flowcharts-judges.md) | Draw a mission, and answer a judge with a number in it |

Roughly one lesson per meeting, alongside everything else.

Start at 1 if you have never coded. Start at 2 if you have. Lessons 2 to 5 are the
ones everybody needs. Lessons 6, 9 and 10 are where the interesting arguments are.
Lesson 13 is worth doing twice, once early and once in the week before the event.

## How the Run button works

Press **Run** and the page starts a real Python interpreter, inside your browser.
The first Run downloads about 8 MB, which takes a few seconds on a good
connection. After that it is instant, and it stays loaded while you move between
lessons.

Nothing is sent anywhere. Nothing needs a hub. You cannot break anything.

- **Run** runs what is in the box. Ctrl and Enter together do the same.
- **Stop** ends a program that is stuck.
- **Start again** puts the original code back, so experimenting is safe.

A program that has not finished after 20 seconds is stopped for you. That is
almost always a loop with no way out.

## What the picture shows

The grey rectangle is a mat, 236 cm by 114 cm, the size of a real one. Grid lines
are every 10 cm and the numbers are centimetres. The dashed square in the bottom
left is roughly where home is.

The green block is the robot, and the pointed end is the front. The line behind it
is where it has been. Under the picture:

| Reading | Meaning |
| --- | --- |
| `x` | how far across the mat, in cm |
| `y` | how far up the mat, in cm |
| `heading` | which way it faces, 0 is straight up the mat, counted clockwise |
| `gyro` | what the gyro sensor reports, which is **not** the same as heading — lesson 10 |

If the robot leaves the mat it turns red and the readout says so. On a real table
it would have driven off the edge.

## Important: this is a pretend robot

The robot on this page is a simple model of two wheels on a flat surface. It is
good enough to learn Python with and to reason about distances and angles. It is
not the mat, and it will not settle an argument about the real robot.

What it does not do:

- No friction, no wheel slip, no battery going flat. A real robot changes
  behaviour as the battery drains, which is the most common cause of "it worked
  last week".
- No motors speeding up or slowing down, so distances come out slightly neater
  than they really are.
- No colour sensors yet. `color_sensor` gives a clear error rather than a wrong
  answer. Line following has to be practised on the real robot.
- No mission models, and nothing to collide with.

Use it to understand the code. Use the mat to find out what is true.

## For the coach

Lesson 1 is ordinary Python with no robot in it, for a student who has never coded.
After that the order follows the toolkit rather than a general Python course,
because the `hub` and `motor_pair` modules do not exist outside the SPIKE App and a
generic Python course does not transfer to them directly. Run the official Training
Camps alongside these: [`../spike-lessons.md`](../spike-lessons.md) maps them onto
our meeting numbers.

Four lessons end at a **real bug in our own toolkit** rather than a made-up
exercise. Those are the ones worth doing as a group, with the file open:

| Lesson | The problem it lands on |
| --- | --- |
| [3](03-ports.md) | Port F is claimed by both the left drive motor and the right colour sensor, and the header comment contradicts the code on three counts |
| [6](06-numbers.md) | `arc_turn` has a missing term, so it turns 121 degrees when asked for 90 |
| [10](10-gyro.md) | `turn_deg_gyro` never commands the motors, and hangs |
| [11](11-attachments.md) | `run_attachment_deg` silently ignores anything over 200 degrees |

Each ends with a decision for the team to make, not an answer. Deciding to delete a
broken function counts as iteration, and
[lesson 13](13-flowcharts-judges.md) is about saying so to a judge.

How the machinery works, if you need to change it:

| File | Job |
| --- | --- |
| `tools/spike-shim.py` | The pretend `hub`, `motor`, `motor_pair` and `runloop`, and the robot model |
| `tools/spike-sim.js` | Builds the editor and the drawing, and boots Python |
| `tools/spike-sim.css` | Styling, taken from the site's own colours |

--8<-- "includes/abbreviations.md"
