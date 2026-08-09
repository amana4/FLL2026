# BIGGLOW Season Plan

> **Dates are placeholders.** Fill in the real tournament date first — everything
> else works backward from it. Once you know it, replace `T-minus` weeks with
> actual calendar dates.

| Key date | Date | Notes |
| --- | --- | --- |
| Season kickoff | _TODO_ | Challenge released |
| Team registration deadline | _TODO_ | Check with regional partner |
| Engineering Notebook due | _TODO_ | Often 1–2 weeks before tournament |
| **Qualifying tournament** | _TODO_ | ← anchor date |
| Championship (if we advance) | _TODO_ | |

## How to read this plan

Four workstreams run **in parallel** all season. The single most common way teams
fail is to spend September–December only on the robot, then improvise the
Innovation Project the week before. Robot Game is one quarter of the score.
Protect the project time.

Each phase below lists a **Definition of done** — the thing that must be true
before moving on. If a phase isn't done, that's fine; carry it. Don't skip it.

---

## Phase 0 — Setup (Weeks 1–2)

Goal: everyone can find things, and we all know what BIGGLOW actually asks for.

**Everyone**
- [ ] Read the Robot Game Rulebook cover to cover. Yes, all of it.
- [ ] Build the field: mat, mission models, dual-lock. Follow `field-setup.pdf` exactly.
- [ ] Sign the [team agreement](../core-values/team-agreement.md)
- [ ] Fill in [`docs/team-roster.md`](team-roster.md) — names, roles, who's on what

**Coaches / mentors**
- [ ] Confirm tournament date and registration
- [ ] Download all official PDFs into [`docs/official-materials/`](official-materials/)
- [ ] Set the meeting schedule

**Definition of done:** field is built and legal, everyone has read the rulebook,
tournament date is on the calendar.

---

## Phase 1 — Explore (Weeks 3–5)

Goal: understand every mission and pick a project problem. Commit to nothing yet.

**Robot Game**
- [ ] One mission analysis file per mission in [`robot-game/missions/`](../robot-game/missions/) — copy `_TEMPLATE.md`
- [ ] Score every mission for points, difficulty, and field position
- [ ] Fill in [`robot-game/scoring-tracker.md`](../robot-game/scoring-tracker.md)

**Innovation Project**
- [ ] Brainstorm problems inside the BIGGLOW theme — go wide, 20+ ideas
- [ ] Pick 3 candidates, do a quick feasibility pass on each
- [ ] Choose one → write it up in [`innovation-project/problem.md`](../innovation-project/problem.md)

**Robot Design**
- [ ] Build a driving base. Don't attach anything to it yet.
- [ ] Test: can it drive straight 1m? Turn 90° repeatably? Fix that before anything else.

**Core Values**
- [ ] Team name, identity, and how we'll make decisions when we disagree

**Definition of done:** every mission has an analysis file, one project problem is
chosen and written down, base robot drives repeatably.

---

## Phase 2 — Design (Weeks 6–10)

Goal: turn analysis into a strategy and a first working solution.

**Robot Game**
- [ ] Group missions into **runs** by field location — see [`robot-game/strategy.md`](../robot-game/strategy.md)
- [ ] Target score: pick a realistic number and write down why
- [ ] Draft a run plan per run in [`robot-game/runs/`](../robot-game/runs/)

**Robot Design**
- [ ] Design attachments per run. Aim for fast swaps — seconds spent in base are points lost.
- [ ] Document each in [`robot-design/attachments/`](../robot-design/attachments/)
- [ ] Decide on a navigation method (gyro / line following / wall squaring) and log the reasoning

**Code**
- [ ] One SPIKE project per run, saved to [`code/spike-projects/`](../code/spike-projects/)
- [ ] Build the reusable blocks first: `drive_straight`, `turn_degrees`, `line_square`

**Innovation Project**
- [ ] Interview at least **two** people affected by the problem — real people, not web pages
- [ ] Research existing solutions. Find out why they don't fully work.
- [ ] Sketch our solution → [`innovation-project/solution.md`](../innovation-project/solution.md)

**Definition of done:** run strategy is written, each run has a draft program that
completes at least once, project has original research and a proposed solution.

---

## Phase 3 — Build & Iterate (Weeks 11–16)

Goal: reliability. This is the longest phase and it is mostly repetition.

**Robot Game — this is the whole game**
- [ ] Run each program **10 times**. Log every attempt in the run's file.
- [ ] Anything below 80% success gets redesigned, not re-tuned.
- [ ] Full 2:30 practice matches, timed, with attachment swaps
- [ ] Track scores over time in [`robot-game/scoring-tracker.md`](../robot-game/scoring-tracker.md)

> **Consistency beats ambition.** A 250-point run that works half the time
> averages worse than a 180-point run that always works — and it's miserable at a
> tournament. Cut missions that won't stabilize.

**Innovation Project**
- [ ] Build a model, prototype, or detailed drawing of the solution
- [ ] Share it with an expert / the affected community and get real feedback
- [ ] Iterate based on that feedback — **judges specifically look for this**
- [ ] Draft the 5-minute presentation

**Robot Design**
- [ ] Durability pass: what falls off? Fix it.
- [ ] Can a team member swap any attachment in under 10 seconds?

**Engineering Notebook**
- [ ] Should be ~70% complete by the end of this phase. Do not leave it to the end.

**Definition of done:** each run at ≥80% success, project solution built and
revised after outside feedback, notebook mostly written.

---

## Phase 4 — Polish & Rehearse (Weeks 17–19)

Goal: nothing new. Only refinement.

- [ ] **Freeze the robot design.** Changes after this point cause tournament failures.
- [ ] Innovation Project presentation rehearsed to time, from memory
- [ ] Every student can explain *any* part of the robot — judges pick who they ask
- [ ] Mock judging session with an outside adult asking rubric questions
- [ ] Practice matches under pressure: noise, a timer, strangers watching
- [ ] Complete [`docs/judging/`](judging/) prep sheets for all three judged areas
- [ ] Engineering Notebook finished and exported

**Definition of done:** presentation runs clean without notes, notebook submitted,
robot untouched for a week and still scoring.

---

## Phase 5 — Tournament (Week 20)

- [ ] Work through [`competition/packing-list.md`](../competition/packing-list.md) the night before
- [ ] Follow [`competition/tournament-day.md`](../competition/tournament-day.md) on the day
- [ ] Charge every hub and spare battery
- [ ] Print the notebook and any handouts
- [ ] Sleep. Genuinely — tired teams make judging mistakes.

---

## Phase 6 — Retrospective (after)

- [ ] What worked, what didn't → [`docs/retrospective.md`](retrospective.md)
- [ ] Write it while it's fresh. Next season's team will thank you.

---

## Weekly rhythm

A meeting that works, roughly 2 hours:

| Time | What |
| --- | --- |
| 0:00–0:10 | Standup — what did you do, what's next, what's blocking you |
| 0:10–1:30 | Split into workstreams and build |
| 1:30–1:50 | Come back together, demo to each other |
| 1:50–2:00 | Log the meeting in [`meetings/`](../meetings/), assign next steps |

Copy [`meetings/_TEMPLATE.md`](../meetings/_TEMPLATE.md) for every session. The
meeting log is not busywork — it's the raw material for the Engineering Notebook
and it's the evidence judges ask for.
