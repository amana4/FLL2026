# Robot Design: Presentation and Q&A

This page is for the Robot Design part of judging. It has the plan for our
5-minute explanation, and the questions judges are likely to ask afterwards,
with answers taken from [Our Robot, Explained](our-robot-explained.md) and
[How Our Code Is Designed](how-our-code-works.md).

The slides for the judges are the [judging deck](judging-deck.html), also as
[PowerPoint](judging-deck.pptx). They follow our speaking order: Strategy, Robot,
Code, Sensors, then Iteration and team. Press F for full screen and N for the
speaker notes. Print the [cue cards](cue-cards.html) to hold while you talk, and
the [judge questions](judge-questions.html) to practise with. All four come from
`python3 tools/make-judging-pack.py`. Orange "fill in" boxes are facts only we
can give, such as the swap time and the 10-run results.

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

The slide numbers are for the [judging deck](judging-deck.html). Each speaker's
[cue card](cue-cards.html) has the same points.

| Time | Slides | Part | Who | Rubric row | What to say |
| --- | --- | --- | --- | --- | --- |
| 0:00 to 1:10 | 1 and 2 | Strategy | Kid 5 | IDENTIFY: mission strategy | Who we are. Time is our biggest limit. Seven runs, Phase 0 to Phase 7, with no Phase 4. Close missions first. Phase 2 is one straight push and back. Phase 3 is the robo taxi. We skipped Lucky Leaves, with the reason. |
| 1:10 to 2:15 | 3 to 5 | Robot | Kid 2 | CREATE: attachments. IDENTIFY: resources | We studied six designs, and the ones that slipped all had blue SPIKE wheels. The flat box lines up on walls and mat lines. Gravity mounting: one move, so do a live swap. Push before motors, and the arm starts on a stopper. |
| 2:15 to 3:00 | 6 and 7 | Code | Kid 1 | CREATE: code | Python, so we reused last year's `drive_cm` and changed the wheel size. Code in layers: the run says what, the library says how. The flowchart: more than 45 degrees off, it stops. |
| 3:00 to 4:00 | 8 and 9 | Sensors | Kid 3 | CREATE: code and sensors | Only the gyroscope steers. Yaw is the way the robot points. Zero, turn, drive straight. Drifts 5 degrees left, steers back right. |
| 4:00 to 5:00 | 10 to 12 | Iteration and team | Kid 4 | ITERATE. DESIGN and COMMUNICATE | Every run tested 10 times, with the real numbers. The arm fix: measured, two ideas failed, the stopper works. Then each of us says one line: "I built ... and I coded ...". What we are proud of. "Ask any of us anything." |

**Handovers.** Each person ends by saying the next person's topic: "Now Kid 1
will explain our code." It sounds planned, and it gives the next person a second
to start. Practise the handovers more than the parts.

**If someone is away.** Every part has a backup person. Write them here:

| Part | Lead | Backup |
| --- | --- | --- |
| Strategy | Kid 5 | _TODO_ |
| Robot | Kid 2 | _TODO_ |
| Code | Kid 1 | _TODO_ |
| Sensors | Kid 3 | _TODO_ |
| Iteration and team | Kid 4 | _TODO_ |

## Gaps to fill before we practise

The slides have orange boxes marked **fill in**. These are facts only we know,
and the knowledge base does not have them. Do not leave a box empty on the day,
and do not make a number up. If we don't know, we measure it.

To fill a box, put the fact in `FILL` at the top of `tools/make-judging-pack.py`,
then run `python3 tools/make-judging-pack.py`. The slides, the cue cards and the
judge questions all update together. Important: the public copy is on the
website, so never type a name into `FILL`. Names come only from the private
roster, with `--named`.

| Gap | Where it shows | How to find it |
| --- | --- | --- |
| How long a swap takes | Slide 5, question 6 | Time five swaps with a stopwatch. Use the middle one. |
| How often each run works, for example "8 out of 10" | Slide 10, question 23 | Run each phase 10 times. Write it in a run log. |
| The arm fix, before and after | Slide 11 | How often the arm was right before the stopper fix, and after. |
| Who built what, and who coded what | Slide 12, question 28 | [Who did what](../docs/who-did-what.md). |
| What we are proud of | Slide 12, question 32 | Each person writes one sentence. |
| Which mission numbers "Pull", "open door", "ant" and "Tree support" are in `Phase 5.py` | Questions | Read the code with the mission list next to it. |
| One thing we changed from the BOXOR design | Questions | Ask the builders. Compare with the instructions. |
| How much time the arm-lift trick saves | Question 20 | Time the end of `phase0-alt.py` with and without `await`. |
| Best practice score | Questions | From the [points tracker](../robot-game/scoring-tracker.md). |

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
goes. Each run starts in base, does a few missions, and comes home. We use
seven runs, Phase 0 to Phase 7. We dropped Phase 4."

**Which missions did you choose, and why those?**
Team to answer. Start from the runs, as on the [mission map](diagrams/mission-route.svg).
Phase 0 does M03 Flip the Rock and M02 Exploding Seeds. Phase 1 does M05 Reaching
Roots. Phase 2 does M01 Drone Survey and the M15 garden skylight. Phase 3 is the
robo taxi. Phase 5 does four jobs on the right side. Phase 6 does M13 Keystone
Species. Phase 7 does the M15 nesting canopy and compost hatch. Then give the
reason. FIRST's
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
