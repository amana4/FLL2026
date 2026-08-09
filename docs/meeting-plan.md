# Meeting Plan — 26 Sessions to Competition

**Sundays and Wednesdays**, 9 Aug → 4 Nov 2026. Competition **Sat 7 Nov**.

> ⚠️ **Competition date assumed as Sat 7 Nov.** Confirm it and adjust — if
> yours is later, you gain meetings at the end; if earlier, cut from the
> Build & Iterate block, never from the last three.

> ✅ **Kits arrived 8 Aug.** No waiting — robot work starts at meeting 1. This
> plan assumes that, which buys roughly two extra weeks of build time versus
> a typical season. Spend it on **reliability**, not on more missions.

## How to use this

Each meeting has a **focus**, an **agenda**, and **deliverables** as checkboxes.
Tick them as you go — this page is the season's progress tracker.

Two rules that keep the plan honest:

- **Sunday = long session** (2 hrs, deep work). **Wednesday = short** (1–1.5 hrs,
  iterate and test). Adjust to your reality, but keep one longer session.
- **Every meeting has an Innovation Project item.** Never zero. That's the
  discipline that stops the classic week-11 panic.

## Progress at a glance

| Block | Meetings | Dates | Goal |
| --- | --- | --- | --- |
| [Setup](#block-1--setup) | 1–4 | Aug 9 – Aug 19 | Unblock everything |
| [Explore](#block-2--explore) | 5–8 | Aug 23 – Sep 2 | Understand all 15 missions, pick a problem |
| [Commit](#block-3--commit) | 9–12 | Sep 6 – Sep 16 | Freeze mission list, design solution |
| [Build & Iterate](#block-4--build--iterate) | 13–18 | Sep 20 – Oct 7 | Reliability. The score comes from here. |
| [Polish](#block-5--polish) | 19–22 | Oct 11 – Oct 21 | Freeze, rehearse, mock judge |
| [Final](#block-6--final) | 23–26 | Oct 25 – Nov 4 | Notebook, dress rehearsal, pack |

---

## Block 1 — Setup

**Meetings 1–4 · Aug 9–19 · Goal: unblock everything with a long lead time**

Kits are already here, so this block builds the field *and* does the paper work
in parallel. Split the team rather than doing one then the other.

### M1 · Sun 9 Aug — Kickoff
Full agenda: [`day-1.md`](day-1.md)

- [ ] Watch the missions video
- [ ] Team name, roster, roles
- [ ] Split and read all 15 missions, report back
- [ ] Biodiversity brainstorm — 20+ ideas
- [ ] **List 10 experts to contact**; assign 2 students to email
- [ ] Team agreement, including how we resolve disagreements
- [ ] **Unbox the kits, inventory against the parts list, charge the hubs**
- [ ] ⚠️ **Coach: register the team** (kits are done)

### M2 · Wed 12 Aug — Build the field
- [ ] **Build mission models** — split by bag number, everyone builds
- [ ] Rulebook quiz — 10 questions, teams of two
- [ ] Walk through equipment limits: **1 controller, 4 motors, 12 in.**
- [ ] Confirm the expert emails went out. **If not, send them in the meeting.**
- [ ] Narrow the brainstorm from 20+ to a shortlist of 3

### M3 · Sun 16 Aug — Field setup + driving base
- [ ] **Finish mission models, lay the mat, place Dual Lock per the wireframe**
- [ ] Seat the three interchangeable docks (mine, city, farm)
- [ ] **Start the driving base** — nothing attached yet
- [ ] Each student presents their assigned missions: points, catch, difficulty
- [ ] Pressure-test the 3 shortlisted problems → [`brainstorm.md`](../innovation-project/brainstorm.md)
- [ ] Chase experts who haven't replied (7–10 days is the right gap)

### M4 · Wed 19 Aug — Base driving reliably
- [ ] **Test: drives straight 1 m? Turns 90° repeatably?** Fix before anything else
- [ ] Measure wheel circumference and degrees-per-cm → [`chassis.md`](../robot-design/chassis.md)
- [ ] Fill in the analysis tables in [`missions/`](../robot-game/missions/README.md)
- [ ] Log interview #1 if an expert has replied

**✅ Block 1 done when:** field built and legal, base drives repeatably, all 15
missions analysed, team registered, 10 experts emailed, 3 problems shortlisted.

---

## Block 2 — Explore

**Meetings 5–8 · Aug 23 – Sep 2 · Goal: reusable code, chosen problem, first
attachment**

The early kits buy a head start here — attachment work begins in this block
rather than Block 3.

### M5 · Sun 23 Aug — My Blocks
- [ ] Build `reset_gyro`, `drive_straight`, `turn_degrees` → [`my-blocks.md`](../code/my-blocks.md)
- [ ] Test each 10× and log the results
- [ ] Record the light/colour thresholds off the mat
- [ ] Expert interview #1 (or chase replies)

### M6 · Wed 26 Aug — Points-per-second
- [ ] Time the robot reaching each mission area
- [ ] Compute points-per-second for every mission
- [ ] Rank all 15 → [`scoring-tracker.md`](../robot-game/scoring-tracker.md)
- [ ] Add `square_to_line` to My Blocks
- [ ] Research existing solutions for the top problem candidate

### M7 · Sun 30 Aug — Choose the problem
- [ ] **Decide the Innovation Project problem.** Write it up in
      [`problem.md`](../innovation-project/problem.md), including the rejected options
- [ ] Test: does it *put biodiversity at risk*? If not, it doesn't fit the brief
- [ ] First pass at grouping missions by field position
- [ ] **Prototype the first attachment** — even a rough one teaches you a lot

### M8 · Wed 2 Sep — First mission scored
- [ ] **Score a real mission on the field.** Start with M11 Window to the Past —
      a guided SPIKE program for it ships in the official materials
- [ ] Refine run grouping based on what you learn
- [ ] Draft interview questions for expert #2

**✅ Block 2 done when:** My Blocks tested, missions ranked by points-per-second,
problem chosen and written up, at least one mission scored on the field.

---

## Block 3 — Commit

**Meetings 9–12 · Sep 6–16 · Goal: decide, then stop deciding**

### M9 · Sun 6 Sep — Freeze the mission list ⚠️
- [ ] **Choose the missions. This list does not change after today.**
- [ ] Group into 3–5 runs by field location → [`strategy.md`](../robot-game/strategy.md)
- [ ] Set a target score and write down why it's realistic
- [ ] **Decide the dock strategy** for M13–M15 — M15's bonus depends on it
- [ ] Expert interview #2

> Pick fewer missions than feels comfortable. A shifting list is the main
> reason teams arrive in November with nothing reliable.

### M10 · Wed 9 Sep — Attachment design
- [ ] Sketch one attachment per run
- [ ] Check the motor budget: **4 total, 2 already driving**
- [ ] Start building attachment #1 → [`attachments/`](../robot-design/attachments/README.md)
- [ ] Write up interview #2 in [`research.md`](../innovation-project/research.md)

### M11 · Sun 13 Sep — Build and program
- [ ] Build attachments #1 and #2
- [ ] Program Run 1 end to end
- [ ] First timed attempt — log it
- [ ] **Design the solution** → [`solution.md`](../innovation-project/solution.md)

### M12 · Wed 16 Sep — Run 2
- [ ] Program Run 2
- [ ] Test attachment swap time (target: under 10 s)
- [ ] Sketch the prototype; list what you need to build it

**✅ Block 3 done when:** mission list frozen, runs defined, 2+ attachments
built, Run 1 completes, solution designed.

---

## Block 4 — Build & Iterate

**Meetings 13–18 · Sep 20 – Oct 7 · Goal: reliability. This is where the score
comes from.**

Every meeting in this block follows the same loop. It is repetitive on purpose.

```
Run it 10 times  →  Log honestly  →  Below 80%? Redesign, don't re-tune
```

### M13 · Sun 20 Sep — Run 1 to 80%
- [ ] Run 1 ×10, log every attempt
- [ ] Redesign whatever fails
- [ ] **Build the prototype**

### M14 · Wed 23 Sep — Run 2 to 80%
- [ ] Run 2 ×10, log
- [ ] Fix the top failure mode
- [ ] Finish the prototype

### M15 · Sun 27 Sep — Run 3 + share the solution
- [ ] Program and test Run 3
- [ ] **Share the solution with an expert** — this is the ITERATE score
- [ ] First full 2:30 practice match

### M16 · Wed 30 Sep — Act on feedback
- [ ] **Revise the solution based on what they said** → [`sharing.md`](../innovation-project/sharing.md)
- [ ] Run 3 ×10
- [ ] Durability check: what's falling off?

### M17 · Sun 4 Oct — Full matches
- [ ] Three full timed matches with swaps
- [ ] Record scores → [`scoring-tracker.md`](../robot-game/scoring-tracker.md)
- [ ] Cut any run still under 80%
- [ ] **Share with a second person/group** — the rubric wants *multiple*
- [ ] Start the presentation draft

### M18 · Wed 7 Oct — Notebook checkpoint
- [ ] **Engineering Notebook should be ~70% done.** Catch up if not.
- [ ] Fix the biggest remaining failure mode
- [ ] Draft all five presentation sections

**✅ Block 4 done when:** every run ≥80%, solution shared with 2+ groups and
revised, notebook 70% complete.

---

## Block 5 — Polish

**Meetings 19–22 · Oct 11–21 · Goal: nothing new. Refinement only.**

### M19 · Sun 11 Oct — Freeze the robot ⚠️
- [ ] **Design freeze. No new attachments, no new missions.**
- [ ] Full matches ×3, record scores
- [ ] First full presentation run-through, timed

### M20 · Wed 14 Oct — Presentation
- [ ] Rehearse without notes
- [ ] Fix the handoffs between speakers — that's where teams stumble
- [ ] Practice matches

### M21 · Sun 18 Oct — Mock judging
- [ ] **Full mock judging with an outside adult** using the real rubrics
- [ ] All three sessions: Robot Design, Innovation Project, Core Values
- [ ] Write down every question you couldn't answer
- [ ] Fill the [judging prep sheets](judging/README.md)

### M22 · Wed 21 Oct — Close the gaps
- [ ] Answer everything the mock judges exposed
- [ ] **Every student can explain any part of the robot** — test it randomly
- [ ] Practice under pressure: noise, timer, an audience

**✅ Block 5 done when:** robot frozen, presentation clean without notes, mock
judging done and gaps closed.

---

## Block 6 — Final

**Meetings 23–26 · Oct 25 – Nov 4 · Goal: arrive ready, not exhausted**

### M23 · Sun 25 Oct — Notebook done
- [ ] **Engineering Notebook finished** → [`engineering-notebook/`](../engineering-notebook/README.md)
- [ ] Full matches ×3
- [ ] Presentation rehearsal

### M24 · Wed 28 Oct — Submit
- [ ] **Submit the notebook** (check your region's deadline — it may be earlier)
- [ ] Practice matches
- [ ] Print handouts

### M25 · Sun 1 Nov — Dress rehearsal
- [ ] Run the whole competition day in order: inspection → judging → 3 matches
- [ ] Everything in team shirts, timed, with an audience
- [ ] Fix only what's clearly broken

### M26 · Wed 4 Nov — Pack
- [ ] Work through [`packing-list.md`](../competition/packing-list.md) — two people, independently
- [ ] Charge every hub and spare battery
- [ ] Confirm programs are loaded **in match order**
- [ ] Read [`tournament-day.md`](../competition/tournament-day.md) together
- [ ] Celebrate — the work is done

### 🏆 Sat 7 Nov — Competition

---

## Standing agenda

Every meeting, regardless of block:

| Time | What |
| --- | --- |
| First 10 min | Standup: did / next / blocked |
| Middle | Split into workstreams — **never all on the robot** |
| Last 10 min | Log the meeting, tick this page, assign homework |

Copy [`_TEMPLATE.md`](../meetings/_TEMPLATE.md) each session and drop it in
[`meetings/`](../meetings/README.md) as `YYYY-MM-DD.md`.

## If you fall behind

You will, somewhere. Priority order when time runs short:

1. **Never cut** the last three meetings (M24–M26). Submission and packing are
   not optional.
2. **Never cut** the Innovation Project. It's 25% and can't be rushed at the end.
3. **Do cut** missions. Fewer runs at 90% beats more runs at 50%.
4. **Do cut** polish on attachments that already work.

## Milestone dates

Copy these into a real calendar with reminders.

| By | Milestone |
| --- | --- |
| Wed 12 Aug | Team registered, 10 expert emails sent, field models built |
| Wed 19 Aug | Field set up, base driving reliably, all 15 missions analysed |
| Sun 30 Aug | Innovation Project problem chosen |
| Wed 2 Sep | First mission scored on the field |
| Sun 6 Sep | **Mission list frozen** |
| Sun 27 Sep | Solution shared with expert #1 |
| Sun 4 Oct | Solution shared with group #2 |
| Wed 7 Oct | Notebook 70% |
| Sun 11 Oct | **Robot design frozen** |
| Sun 18 Oct | Mock judging done |
| Wed 28 Oct | **Notebook submitted** |
| Sat 7 Nov | 🏆 Competition |
