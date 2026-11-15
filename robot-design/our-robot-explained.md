# Our Robot, Explained

Read this before the [Robot Design test](robot-design-test.md). It collects in
one place what our robot is, how its code works, and why we made the choices we
made. Judges will ask any of you about any part of it, so everyone reads all of
it, not just their own part.

**On this page:**

- [How judges score Robot Design](#how-judges-score-robot-design)
- [1. The driving base](#1-the-driving-base)
- [2. Attachments](#2-attachments)
- [3. The code](#3-the-code)
- [4. Mission strategy and the runs](#4-mission-strategy-and-the-runs)
- [5. Testing and changing things](#5-testing-and-changing-things)
- [6. Words to know](#6-words-to-know)

The page has two kinds of content.

**Facts.** These come from our code, our design log and our git history. Each
one says where it came from, so you can check it.

**Team to answer.** Some of the *why* was never written down. Nobody else can
fill those boxes in, because only you know why you did it. They look like this:

!!! question "Team to answer"
    A question only the team can answer. Bring your answer to the brainstorm.

Important: do not invent an answer for a box you do not know. "I don't know,
Kid 3 built that part" is a fine answer in the judging room. A made-up reason
that falls apart at the next question is not.

## How judges score Robot Design

Robot Design judges use a rubric with five rows. This wording is copied from
the official rubric, `fll-challenge-bioglow-rubrics-color.pdf`, page 3. For each
row, the right-hand column is what you need for **Accomplished**, which is 3 out
of 4.

| Row | What the row is about | To score Accomplished |
| --- | --- | --- |
| **IDENTIFY** | Team determined which missions to attempt, explored building and coding resources, and sought guidance as needed. | Clear evidence of mission strategy. Clear use of building or coding resources to support their mission strategy. |
| **DESIGN** | Team members worked collaboratively on their designs and developed the building and coding skills needed. | Clear evidence that all team members contributed ideas. Clear evidence of building and coding skills in all team members. |
| **CREATE** | Team developed original designs or improved on existing ones according to their mission strategy. | Clear explanation of innovative attachments and their purpose. Clear explanation of innovative code and/or sensor use. |
| **ITERATE** | Team repeatedly tested their robot and code to identify areas for improvement and incorporated the findings into their solutions. | Clear evidence of repeated testing of their robot and code. Clear evidence of improvements based on testing. |
| **COMMUNICATE** | Team effectively explained what they learned from the robot design process and celebrated their progress. | Detailed explanation of process and lessons learned. Team clearly shows pride or enthusiasm for their work. |

Some of these lines also count toward the **Core Values** award. On the rubric
they have a gear-shaped box instead of a square one. They are:

- Using building or coding resources (IDENTIFY)
- All team members contributing ideas (DESIGN)
- Improvements based on testing (ITERATE)
- Both COMMUNICATE lines

Note the words "all team members" in the DESIGN row. Judges choose who they ask.
One person who knows everything scores lower than five people who each know
their part well.

## 1. The driving base

**What is plugged in where.** This is from the code we use now, in
`code/Phases/Final/`:

| Socket | What is plugged in |
| --- | --- |
| F | Left drive motor |
| A | Right drive motor |
| C | Attachment motor (`attachment1`) |
| E | Attachment motor (`attachment2` in `Phase 5.py` and `phase3.py`) |

This took three tries to get right, which is itself a good ITERATE story. On
13 September 2026 the team read the sockets off the hub and fixed the code to
match. On 20 September the hub disagreed: the robot stopped with the error
`OSError: [Errno 19] ENODEV`, which means "no motor on that socket". Drive
motors on F and A worked. Then `Phase 5.py` has the note `confirmed :D` next to
socket E. (Sources: [design log](design-log.md),
[library notes](../code/library/README.md).)

Note: some older pages, such as the [BOXOR frame page](attachments/boxor-frame.md),
still show the 13 September wiring. The final code is the one that runs.

**How the robot finds its way.** It uses the **gyro** inside the hub to know
which way it points, and the **motor encoders** to count how far the wheels
have turned. On 20 September 2026 the team decided not to use the colour
sensors, and the line-following code was removed. (Source:
[library notes](../code/library/README.md).)

That choice has a cost. The gyro can correct which way the robot *points*, but
nothing corrects how *far* it has gone. The code fixes that a different way:
the robot backs into a wall or a model and lets it push the robot square.

**The hub** is mounted flat and face up, so the centre button can be pressed
with one hand at the table. (Source: [BOXOR frame page](attachments/boxor-frame.md).)

**Wheel size.** The code assumes wheels 62.4 mm across. The design log says
nobody has checked this with calipers yet.

!!! question "Team to answer"
    - Why did we pick this driving base? What did we like about it from the
      [six chassis designs](chassis-designs-slides.html) we looked at?
    - Which wheels are on the robot, and why those?
    - Why did we stop using the colour sensors? Was it the lines on the mat,
      the time, or something else?
    - Where is the heavy part of the robot? Does it tip or rock when it stops?

## 2. Attachments

**The BOXOR frame.** Our attachment frame comes from a published design, the
BOXOR Frame Attachment by Next Level Teacher. A motor turns a **bevel gear
pair**, which turns the movement through 90 degrees and swings an arm. Change
the arm, and the same frame does a different job. (Source:
[BOXOR frame page](attachments/boxor-frame.md).)

Using a published design is allowed. The CREATE row says "original designs **or
improved on existing ones**". So the strong answer is not "we designed it all
ourselves". It is "we started from this design, and here is what we changed and
why".

**Where it sits.** In the final code, the attachment is on the **back** of the
robot. So the robot drives backwards into each model, and most distances in the
code are negative. (Source: the comments in `code/Phases/Final/phase0.py`.)

**Photos.** There are 11 photos of the final attachments from 8 November 2026,
in `code/Phases/Final/attachment pics/`. Ask the coach to show them, because
most browsers cannot open that file type.

!!! question "Team to answer"
    - What did we change from the BOXOR instructions? Each change is a CREATE
      answer.
    - How many different arms do we have, and which mission uses each one?
    - How long does an attachment swap take? Time it with a stopwatch.
    - Why did we move the attachment to the back of the robot?

## 3. The code

**Why Python.** This season the team moved from Word Blocks to Python.
Last season's team had good, tuned Python code to start from. Git can also
show exactly what changed in a `.py` file, but not in a Word Blocks file.
(Source: [code overview](../code/README.md).)

**Our library.** Every program starts with a copy of
`code/library/advanced.py`. It is a Python version of the Word Blocks library
"Advanced Coding 26". The team found **eight bugs** in the blocks by reading
them, and three more by testing on the robot, and fixed all eleven. Two
examples:

- The blocks used 3.146 for pi. Python uses the exact value.
- In the line-following blocks, every "wait until" could wait forever. Miss the
  line once and the robot sits still for the rest of the match.

The full list is in the [library notes](../code/library/README.md).

**The main commands.**

| Command | What it does |
| --- | --- |
| `drive_cm(30)` | Drives 30 cm forwards. It speeds up gently, slows down gently, and uses the gyro to stay straight. `drive_cm(-30)` drives backwards. |
| `face(90)` | Turns until the robot points 90 degrees away from the way it pointed when the program started in base. |
| `motor.run_for_degrees(attachment2, -380, 1000)` | Turns an attachment motor 380 degrees backwards, at speed 1000. |
| `init_robot(default_speed=500)` | Starts the program. It pairs the wheels and zeroes the gyro, so the spot it starts in becomes "base". |

**Why `face`, and not "turn 90 degrees".** A turn that lands one degree short
passes that mistake on to the next turn, and the mistakes add up. `face` always
measures from base, so a mistake in one turn does not pass to the next. The
code notes say four turns round a square end about 1 degree out with `face`,
instead of 17 degrees out. (Source: the comment above `face` in `advanced.py`.)

**Why the gyro turn.** The team measured the old turn, which only counted wheel
rotations. It took 1.54 seconds and was 4.26 degrees out. The gyro turn took
1.18 seconds and was 0.58 degrees out. It was faster *and* more accurate, so
the old turn was deleted. (Source: [library notes](../code/library/README.md).)

**Why `YAW_SIGN = -1`.** This tells the code which way the gyro counts. Ours
counts up when the robot turns anticlockwise. The team found this on
20 September 2026, when `drive_cm(-44)` made the robot spin on the spot instead
of driving. The blocks had it the wrong way round.

**The safety stop.** If a straight drive goes more than 45 degrees off course,
the robot brakes and stops with an error. Before this was added, a wrong
setting made the robot keep spinning, because the code counted the spin as
driving forwards.

**The calibration line.** Most programs have `set_calibration_scale(179/180)`.
On our mat, the robot drove 179 cm when asked for 180, so every distance is
scaled to match.

**Centimetres, not millimetres.** The Word Blocks used millimetres, and Python
uses centimetres. So `.Forward 300` in blocks is `drive_cm(30)` in Python.

!!! question "Team to answer"
    - Who wrote which program? This goes in [who did what](../docs/who-did-what.md).
    - Which bug was the hardest to find, and how did you find it?
    - What would you explain first to a judge who has never seen Python?

## 4. Mission strategy and the runs

Our final programs are in `code/Phases/Final/`. This is what each one does,
read from the code and its comments:

| Program | What the code does |
| --- | --- |
| `phase0.py` and `phase0-alt.py` | **M03 Flip the Rock**: backs 44 cm into the rock. Then **M02 Exploding Seeds**: turns, backs up, and uses the attachment. `phase0-alt.py` adds a straighten-up after hitting the rock (see section 5). |
| `phase1.py` and `phase2.py` | At the moment these hold the same code as `phase0-alt.py`. |
| `phase3.py` | Faces "the root", lowers the attachment, and drives back while lifting it. That matches **M05 Reaching Roots**. Then it drives across to the right side. |
| `Phase 5.py` | Four jobs in one run. The code calls them "Pull", "open door", "ant" and "Tree support". Then it drives back to base. |
| `Phase 6.py` | **M13 Keystone Species**, then back to base. |

The [strategy page](../robot-game/strategy.md) has FIRST's own advice on choosing
missions: pick missions that use push, pull or lift, that are close to a launch
area, and that are easy to get home from.

!!! question "Team to answer"
    - The `phase0.py` comment says "Missions 3, 2 and 1", but the code only does
      3 and 2. Does the robot also do M01 Drone Survey in this run?
    - Which mission numbers are "Pull", "open door", "ant" and "Tree support"
      in `Phase 5.py`?
    - Which missions did we decide **not** to do, and why? "It was too hard" is
      a weak answer. "It was worth 10 points but took 40 seconds" is a strong
      one.
    - Why are the runs grouped the way they are?
    - What is our best score in practice?

## 5. Testing and changing things

The ITERATE row wants proof that we tested, found problems, and changed
things. Our git history shows a lot of this. Some examples:

| Date | What happened |
| --- | --- |
| 13 Sep 2026 | Found that the code had the wrong sockets for the motors and sensors, and fixed it. Found that the simulator mat was 236 cm wide, but the real mat is 200 cm. |
| 20 Sep 2026 | Found the gyro counted the other way (`YAW_SIGN`). Found the drive motors were on F and A. Decided to stop using the colour sensors. |
| 26 Sep 2026 | Fixed a bug where the gyro jumps from 180 to -179, which made some turns spin for 30 seconds. |
| 10 to 11 Oct 2026 | First run programs. Fixed the curve turn, then tuned the mission paths. |
| 25 to 31 Oct 2026 | Programs for the right-hand side of the field, including Keystone Species. |
| 1 Nov 2026 | First versions of the final programs. |
| 7 to 13 Nov 2026 | Tuning the final programs. |

**Tuning you can see in the code.** Many lines have a comment such as
`#was 60`. Each one is a number someone changed after a test run. In
`Phase 5.py`:

- `await drive_cm(14) #was 12`
- `await face(-62) #was 60`
- `await drive_cm(-28) #was 30`
- `motor.run_for_degrees(port.C,360,1000) #was 350`

**A fix from testing.** When the robot backs into the rock in M03, the hit
knocks it a little crooked. `phase0-alt.py` adds `await face(0)` straight after,
with the comment "Straighten post collision before backing off for accuracy".
That is a test, a problem, and a fix, which is exactly what ITERATE asks for.

Note: the [design log](design-log.md) has only two entries, both from September.
Everything after that is in git and in people's memories. Writing it up is part
of the brainstorm.

!!! question "Team to answer"
    - Pick one `#was` line. Who changed it, and what went wrong before?
    - What is the success rate of each run? For example, "8 out of 10".
    - What is the biggest thing we changed on the robot itself, not the code?
      Do we have a photo of the version before?

## 6. Words to know

**Gyro.** The sensor inside the hub that knows which way the robot points.

**Yaw.** The direction the robot points, as a number of degrees.

**Encoder.** The part of a motor that counts how far it has turned.

**Base.** The way the robot points when the program starts. Every `face` turn
measures from base.

**Bevel gears.** Two gears that meet at a right angle, so the turning movement
changes direction by 90 degrees.

**Calibration.** Measuring how the real robot behaves and adjusting the code to
match, like `set_calibration_scale(179/180)`.

**Iterate.** Test, find a problem, change something, test again.

## Next

When you have read this page, do the [Robot Design test](robot-design-test.md).

--8<-- "includes/abbreviations.md"
