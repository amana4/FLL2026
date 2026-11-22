# Robot Design

Everything about how our robot is built, why it is built that way, and how
to explain it to the judges.

## Start here

1. Read [Our Robot, Explained](our-robot-explained.md). It covers the driving
   base, the attachments, the code, the missions, and what we tested and
   changed.
2. Read [How Our Code Is Designed](how-our-code-works.md). It has the
   flowcharts and diagrams of how our code works.
   In class, the coach teaches both pages with the
   [class lesson slides](robot-lesson-slides.html).
3. Then take the [Robot Design test](robot-design-test.md).
4. Then practise with [Presentation and Q&A](presentation.md): the 5-minute
   explanation, the [slides](presentation-slides.html), and the questions judges ask.
5. Going for Exceeds: the workshop has the gap lesson from the Robot Design
   test, the homework slides each of us fills in, and how we put them together.
   [Show it in class](exceeds-workshop.html), or upload the
   [PowerPoint](exceeds-workshop.pptx) to Google Slides to edit it together.
6. Read [Going for Exceeds](exceeds-prep.md): what judges look for on all ten
   rubric lines, testing tables, a notebook template, 32 judge questions, and our
   readiness scorecard.

## Team workspace

These are the pages the build team works in. They are full of tables still to
fill in, so read Our Robot, Explained first.

| Page | What's in it |
| --- | --- |
| [Design log](design-log.md) | Dated record of what we changed and why. This is the evidence for ITERATE |
| [Driving base details](chassis.md) | What we aimed for, and the tables for measurements |
| [Attachments list](attachments/README.md) | One page per attachment |
| [BOXOR frame](attachments/boxor-frame.md) | The attachment frame, its gears, and the wiring |
| [When something breaks](troubleshooting.md) | Fixes for common problems |
| [Class lesson slides](robot-lesson-slides.html) | 68 slides that teach the whole robot, with check questions after each part |
| [Exceeds workshop](exceeds-workshop.html), also as [PowerPoint](exceeds-workshop.pptx) | 41 slides: the gap lesson, why this robot, the mission map and robo taxi, why Python, how drive_cm works, the gyro correction, the homework templates, and the rehearsal plan. `python3 tools/make-exceeds-pptx.py` rebuilds it, and `--named` makes a private copy with names |
| [Six chassis designs](chassis-designs-slides.html) | Ten slides comparing other teams' driving bases. Also in `robot-design/chassis-designs.pptx`; `python3 tools/make-design-pptx.py` rebuilds it |

## Design principles

1. **Durable beats clever.** If it falls off in a match it scores zero.
2. **Fast swaps.** Attachments should mount in one motion.
3. **Repeatable.** Same starting position, same result, every time.
4. **Explainable.** Every student should be able to describe any subsystem.
5. **Symmetric where possible.** Uneven weight makes the robot curve.

## Photo checklist for judging

- [ ] Robot from front, side, top
- [ ] Each attachment, mounted and detached
- [ ] Close-ups of anything unusual we want to talk about
- [ ] "Before and after" pairs of things we redesigned

--8<-- "includes/abbreviations.md"
