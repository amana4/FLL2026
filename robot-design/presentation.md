# Robot Design: Presentation and Q&A

This page is for the Robot Design part of judging. It has the plan for our
5-minute explanation, and the questions judges are likely to ask afterwards,
with answers taken from [Our Robot, Explained](our-robot-explained.md) and
[How Our Code Is Designed](how-our-code-works.md).

The short slides for the judges are here: [Robot Design slides](presentation-slides.html). Open them
on a laptop, or print them. Each slide is one page when printed.

To build the slides together, use the [Exceeds workshop deck](exceeds-workshop.pptx).
It has a template for each slide below, with an Exceeds checklist and speaker notes.

To learn the robot first, use the [class lesson slides](robot-lesson-slides.html).
They teach both knowledge base pages, one idea per slide. Then do the
[Robot Design test](robot-design-test.md). Every fact on the judging slides
is something the test already asked you to find.

**On this page:**

- [How the 10 minutes work](#how-the-10-minutes-work)
- [The 5-minute explanation](#the-5-minute-explanation)
- [Gaps to fill before we practise](#gaps-to-fill-before-we-practise)
- [Q&A: questions judges ask](#qa-questions-judges-ask)
- [How to practise](#how-to-practise)

## How the 10 minutes work

From the official Judging Session Flowchart, Robot Design comes straight after
the Innovation Project, in the same room, with the same judges:

| Part | Time | What happens |
| --- | --- | --- |
| Robot Design Team Explanation | 5 minutes | We explain the robot, the code and our strategy. |
| Robot Design Question & Answer | 5 minutes | The judges ask questions. They choose who answers. |

There is no robot game field in the judging room, so we cannot show a mission.
We bring the robot, the attachments, these slides printed or on a laptop, and
the [design log](design-log.md).

Note: ask the regional partner whether we can use a laptop in the judging room.
If not, print the slides. Printed slides work just as well, and nothing can go
wrong with them.

## The 5-minute explanation

Each of us owns one part, about one minute each. The rubric has five rows, and
each part covers at least one row, so the judges hear something for every row.

Kid 1 to Kid 5 below are slots, not people. The coach puts names against them
using [who did what](../docs/who-did-what.md). The rule is simple: you present
the part you worked on most.

Important: these are talking points, not a script. Do not learn the words by
heart. Know the points, and say them your way. A learned speech sounds learned,
and it falls apart when a judge interrupts.

| Time | Slide | Who | Rubric row | What to say |
| --- | --- | --- | --- | --- |
| 0:00 to 0:20 | 1 | Kid 1 | | Who we are. "Our robot is one base with attachments we swap. We'll each explain one part." |
| 0:20 to 1:00 | 2 and 3 | Kid 1 | IDENTIFY | We compared six robot designs before building. The three that slipped all used the blue SPIKE wheels. We took the good ideas from all six. Then: which missions each run does, and why those. |
| 1:00 to 2:00 | 4 and 5 | Kid 2 | CREATE (attachments) | The box shape: push it against a wall and it sits square. Wheels inside the frame. The BOXOR frame and its bevel gears. Gravity mounting: pegs line it up, its weight holds it, on or off in one move. One thing we changed from the BOXOR design. |
| 2:00 to 3:00 | 6 and 7 | Kid 3 | CREATE (code) | Code in three layers. `face` measures every turn from base, so a square ends about 1 degree off, not 17. The gyro turn was faster and more accurate than the old turn: 1.18 s and 0.58 degrees against 1.54 s and 4.26 degrees. The arm lifts while the robot drives home. |
| 3:00 to 4:00 | 8 and 9 | Kid 4 | ITERATE | How we test: pretend robot, 34 automatic checks, real mat, save in git. One real story: the rock bump knocked the robot crooked, so we added `face(0)`. Every `#was` note in our code is a test that changed a number. Our reliability number. |
| 4:00 to 5:00 | 10 and 11 | Kid 5 | DESIGN and COMMUNICATE | Who built and coded what, and that all five of us did both. What we learned. What we are most proud of. "Ask any of us anything." |

**Handovers.** Each person ends by saying the next person's topic: "Now Kid 3
will tell you about the code." It sounds planned, and it gives the next person
a second to start. Practise the handovers more than the parts.

**If someone is away.** Every part has a backup person. Write them here:

| Part | Lead | Backup |
| --- | --- | --- |
| IDENTIFY: designs and missions | Kid 1 | _TODO_ |
| Driving base and attachments | Kid 2 | _TODO_ |
| Code | Kid 3 | _TODO_ |
| Testing and changes | Kid 4 | _TODO_ |
| Teamwork and lessons | Kid 5 | _TODO_ |

## Gaps to fill before we practise

The slides have boxes marked **Team to fill in**. These are facts only we know,
and the knowledge base does not have them. Do not leave a box empty on the day,
and do not make a number up. If we don't know, we measure it.

To fill a box, open `robot-design/presentation-slides.html` and search for
`TEAM:`. Each comment sits just above the text to replace. Important: the slides
are on the public website, so keep the Kid 1 to Kid 5 labels and never type a
name into them.

| Gap | Slide | How to find it |
| --- | --- | --- |
| Which mission numbers "Pull", "open door", "ant" and "Tree support" are in `Phase 5.py` | 3 | Read the code with the mission list next to it. |
| Does `phase0.py` also do M01 Drone Survey? | 3 | Run it and watch. |
| One mission we skipped, with its points and time | 3 | Use the [scoresheet](../robot-game/scoresheet.md). |
| One thing we changed from the BOXOR design | 5 | Ask the builders. Compare with the instructions. |
| How long a swap takes | 5 | Time five swaps with a stopwatch. Use the middle one. |
| How much time the arm-lift trick saves | 7 | Time the end of `phase0-alt.py` with and without `await`. |
| How often each run works, for example "8 out of 10" | 9 | Run each program 10 times. Write it in a run log. |
| Best practice score | 9 | From the [points tracker](../robot-game/scoring-tracker.md). |
| Who built what, and who coded what | 10 | [Who did what](../docs/who-did-what.md). |
| What we learned, and what we are proud of | 11 | Each person writes one sentence. |

## Q&A: questions judges ask

In the 5 minutes of questions, the judges pick who answers. So everyone reads
every answer here, not just their own part.

Each answer is how a team member might say it. Read it, understand why it is a
good answer, then say it your own way. Answers marked **Team to answer** need
our own facts. Find them before practice.

Three rules for the room:

1. Answer in two or three sentences, then stop. The judge will ask more if they
   want more.
2. "I don't know, but Kid 2 built that, and can tell you" is a good answer. A
   made-up answer falls apart at the next question.
3. Talk about what went wrong. Judges score iterating, and a problem we fixed is
   worth more than a story with no problems.

### IDENTIFY: strategy and resources

**Walk us through your robot.**
"It's one driving base, a box with flat walls, and we swap attachments onto
the back. The gyro keeps it straight and the motor encoders measure how far it
goes. Each run starts in base, does a few missions, and comes home."
Team to answer: how many runs do we use in a match?

**Which missions did you choose, and why those?**
Team to answer. Start from the runs: `phase0-alt.py` does M03 Flip the Rock and
M02 Exploding Seeds. `phase3.py` does M05 Reaching Roots. `Phase 5.py` does four
jobs. `Phase 6.py` does M13 Keystone Species. Then give the reason. FIRST's
advice is to pick missions with simple moves like push, pull or lift, close to
base, and easy to get home from. Say which of those fit our missions.

**Why did you skip the others?**
Team to answer. Give a number, not "it was too hard". For example: "It was only
10 points and took 40 seconds", or "it risked knocking over another model".

**Why did you group the missions into runs that way?**
Team to answer. Missions close together on the mat go in the same run, so the
robot does not cross the mat twice.

**What resources did you use?**
"Before we built anything, we compared six robot designs other teams had made,
and what went wrong for each one. The three that slipped all used the blue
SPIKE wheels. We took the best ideas, like a box frame and gravity mounting.
Our attachment frame comes from a published design, the BOXOR frame. And last
year's team left us Python code to start from."

**Which design is your robot closest to?**
Team to answer. Boxor, YellowBot, Track-X, Xbot or HummerOne Pro. Say which
idea came from which design.

**Did you use the colour sensors?**
"We had two, but on 20 September we decided not to use them, and we took that
code out. We steer with the gyro instead." Team to answer: why did we stop?

### DESIGN: teamwork and skills

**Who built the robot? Who wrote the code?**
Team to answer. Each person says one thing they built and one thing they coded.
The rubric says "all team members", so all five need an answer.

**How did you share out the work?**
Team to answer. For example: one person per run, and everyone can run every
program.

**Did you all agree on everything?**
Team to answer. Pick one real disagreement and say how we decided. Judges like
this question, because it is about Core Values too.

### CREATE: attachments

**Why is your robot shaped like that?**
"It's a box with flat walls and the wheels inside. When we push it back against
the wall, it can only sit square, so every run starts the same way. It can
square up on a wall during a run too, and the wheels can't rub on anything and
steer us off course."

**How do you change attachments?**
"We use gravity mounting. Pegs line the attachment up so it can only go on the
right way, and its own weight holds it. It goes on or off in one move, so we
waste less match time in base."

**How long does a swap take?**
Team to answer. Time it with a stopwatch and give the number.

**What does the BOXOR frame do?**
"Inside it is a pair of bevel gears. They turn the motor's movement around a
corner, through 90 degrees, and that swings an arm. Put a different arm on, and
the same frame does a different job."

**Did you design that yourselves?**
"We started from a published design called the BOXOR frame." Then Team to
answer: what did we change, and why? The rubric says "original designs or
improved on existing ones", so changing a design is fine. Say what we changed.

**Why is the attachment on the back?**
Team to answer. It is why the robot drives backwards into most models, and why
so many distances in the code have a minus sign.

**Has an attachment ever fallen off?**
Team to answer. If yes, say what we changed.

### CREATE: code and sensors

**How do you make it drive straight?**
"About 66 times a second, our drive command reads the gyro to see how far off
straight it is, and steers the other way. The further off, the harder it
steers. It also speeds up and slows down gently, so the wheels don't slip and
it doesn't overshoot."

**How do you get consistent turns?**
"Our turns use the gyro and measure every direction from where the robot
started, so mistakes don't add up. Drive round a square that way and you end
about 1 degree off, not 17. The turn slows down as it gets close, and after
braking it checks the gyro again, because our robot rolls about 2 degrees
past."

**Why the gyro and not just counting wheel turns?**
"We timed and measured both. The old turn, counting wheels, took 1.54 seconds
and ended 4.26 degrees off. The gyro turn took 1.18 seconds and ended 0.58
degrees off. It was faster and more accurate, so we deleted the old one."

**What is clever about your code?**
"Our robot can do two things at once. At the end of the M02 run, the arm lifts
while the robot is already driving home. We did that by leaving out `await` on
the arm command, and it saves time in a two and a half minute match."
Team to answer: how much time does it save?

**How is your code organised?**
"Our code is in layers. The run programs only say what to do, like back 44 cm
then face 90. Our library says how: it speeds up, steers with the gyro, and
stops on the mark. When we improve the library, every run gets better at once."

**How do you get the code onto the robot?**
"The SPIKE app can't load one file from another, so each run needs its own copy
of our library. Copying by hand once gave us the wrong motor ports in a file.
So we use a small tool that copies the library in for us, and never touches
the mission part."

**Why Python and not Word Blocks?**
"We started in Word Blocks and moved to Python. Last year's team left us good
Python code, and with Python, git shows exactly which line changed and when.
When we turned the blocks library into Python, we found eight bugs just by
reading it, and three more by testing."

**Can you give an example of one of those bugs?**
"The blocks used 3.146 for pi, but the real value starts 3.14159. And in the
line-following blocks, if the robot missed the line once, it would wait for it
forever and sit still for the rest of the match."

**What is PID?**
"It's how our turn works out how hard to turn. P: far from the target, turn
fast; close, turn slowly. I: stuck a little short for a while, push a bit more.
D: closing in fast, ease off so it doesn't swing past."

**What happens if something goes wrong in a run?**
"Our code watches for trouble. If the robot gets more than 45 degrees off
course, it stops, instead of spinning off the table. We added that after it
really spun off the table in testing, on 20 September. And if a drive or turn
takes more than 8 seconds, it gives up and goes on, because the robot is stuck."

**How does the robot know where it is?**
"It can't see. The gyro tells it which way it points, and the motor encoders
count how far the wheels have turned. Nothing fixes how far it has gone, so
sometimes it backs gently into a wall or a model to square up."

**What does `set_calibration_scale(179/180)` do?**
"We told the robot to drive 180 cm, and it drove 179 cm. That line fixes every
distance to match our real robot."

### ITERATE: testing and changes

**How do you know your code works?**
"We test in steps. First on a pretend robot in the browser, then with 34
automatic checks, then on the real mat. Every change is saved in git with a
note, so we can see what we changed and go back if it gets worse."

**How do you know a run is reliable?**
Team to answer, with a number: "Run 1 worked 8 out of 10 times." A number
shows we measured. "It mostly works" shows we didn't.

**What broke, and how did you fix it?**
Pick one. Three true stories from our season:

- "In Flip the Rock, the robot backs into the rock, and the bump knocks it a
  little crooked. So we added `face(0)` right after the bump to straighten up."
- "On 20 September, `drive_cm(-44)` should have driven backwards, but the robot
  spun on the spot. The gyro counted the other way from what the code expected,
  so we fixed `YAW_SIGN`."
- "On 26 September some turns spun for 30 seconds. When the gyro goes past 180
  it jumps to -179, and the code didn't expect that. We fixed it."

**Show us something you changed after testing.**
"Lots of lines in our code have a note like `#was 60`. Each one is a number we
changed after a test run. In `Phase 5.py`, `face(-62)` was 60 and `drive_cm(-28)`
was 30." Team to answer: who changed one, and what went wrong before?

**Did you ever get the motor ports wrong?**
"Yes, it took three tries. On 13 September we read the ports off the hub and
put them in the code. On 20 September the robot stopped with an error that
means there's no motor on that port. We tested again and found the wheel motors
were on F and A."

**What is the biggest change you made to the robot itself?**
Team to answer. A photo of before and after is the best answer.

**What would you improve with more time?**
Team to answer. Pick something real, for example a run that only works some of
the time.

### COMMUNICATE: lessons and pride

**Explain your robot in three sentences.**
Each person needs their own version. For example: "It's a box-shaped base that
squares up on walls, with attachments that drop on by gravity. It steers with
the gyro and measures every turn from where it started, so mistakes don't add
up. We tested every run again and again, and every `#was` in our code is a fix
from a test."

**What was the hardest part?**
Team to answer. Which bug was hardest to find, and how did you find it?

**What did you learn?**
Team to answer. Each person, one sentence. Something real, like "test one thing
at a time" or "measure, don't guess".

**What are you most proud of?**
Team to answer. Say it like you mean it. The COMMUNICATE row asks for pride and
enthusiasm, and judges can tell.

## How to practise

1. Practise the 5-minute explanation with a timer. Stop at 5 minutes, even if
   you are not finished. Then cut what ran long.
2. Practise the handovers on their own, three times.
3. For the Q&A, the coach reads a random question and points at a random
   person. That person answers in under 30 seconds.
4. Swap parts once. Present someone else's minute. That is how we find out what
   each of us can't explain yet.
5. Do one full mock: Innovation Project and Robot Design back to back, with a
   grown-up who is not the coach asking the questions.

Write down every question you couldn't answer. Find the answer before the next
practice, and add it to this page.

--8<-- "includes/abbreviations.md"
