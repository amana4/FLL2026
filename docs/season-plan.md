# BIOGLOW Season Plan — 12 Weeks

**Theme: Biodiversity.** Challenge announced 4 August 2026. Local competition:
early November 2026.

> ⏱️ **This is a 12-week season, not a 20-week one.** From today (9 Aug) to an
> early-November competition is about 12 weeks. That's enough time to do well,
> but not enough to do things twice. The plan below is compressed accordingly:
> shorter exploration, earlier commitment, more overlap between workstreams.

| Key date | Date | Notes |
| --- | --- | --- |
| Challenge announced | **4 Aug 2026** | ✅ done |
| Team registration deadline | _TODO — check now_ | ⚠️ may already be close |
| LEGO kits ordered | _TODO_ | ⚠️ **blocks everything** — see below |
| Engineering Notebook due | _TODO_ | Often 1–2 weeks before the competition |
| **Local competition** | **Early Nov 2026** | ← everything works back from here |

## Do these this week

Three things gate the whole season. None involve the robot.

1. **Order the LEGO kits.** Nothing on the robot side can start without them,
   and shipping is unpredictable. If they take three weeks, that's a quarter of
   the season gone. Order today; work the paper side while you wait.
2. **Confirm the competition date and register.** Registration deadlines are
   real and unforgiving.
3. **Download the official BIOGLOW materials** into
   [`official-materials/`](official-materials/) and read the rulebook.

## The 12-week shape

| Weeks | Phase | Robot | Innovation Project |
| --- | --- | --- | --- |
| 1–2 | Setup | Order kits, read rulebook, build field | Brainstorm, contact experts |
| 3–4 | Explore | Driving base, analyse all missions | Pick problem, first expert call |
| 5–6 | Commit | Choose missions, group into runs | Research, design solution |
| 7–9 | Build & iterate | Attachments, code, repeat until reliable | Prototype, share, revise |
| 10–11 | Polish | Freeze design, practice matches | Rehearse presentation |
| 12 | Compete | | |

The compression versus a normal season is mostly in weeks 3–6: you commit to a
mission list sooner and explore less. That's the right trade at this length.

---

## Weeks 1–2 — Setup

Goal: unblock everything, and understand what BIOGLOW actually asks for.

**Blocking tasks (coaches)**
- [ ] **Order LEGO kits** — SPIKE Prime sets + this season's field/mission model set
- [ ] Confirm competition date, venue, and registration deadline
- [ ] Register the team, pay fees
- [ ] Download all official PDFs → [`official-materials/`](official-materials/)
- [ ] Set the weekly meeting schedule

**Everyone**
- [ ] Read the Robot Game Rulebook cover to cover
- [ ] Sign the [team agreement](../core-values/team-agreement.md)
- [ ] Fill in the [team roster](https://github.com/amana4/FLL2026/blob/main/docs/team-roster.md)

**Innovation Project — start now, don't wait for kits**
- [ ] Brainstorm 20+ biodiversity questions. Go wide; judge nothing yet.
- [ ] **Start emailing local experts this week.** University biology
      departments, nature reserves, conservation charities, council ecology
      officers, botanic gardens, wildlife trusts. Expect slow replies — that
      lag is exactly why this can't wait until week 6.

> **Why experts now:** a researcher who takes three weeks to answer an email is
> normal. Contact ten people in week 1 and you'll have two conversations by
> week 4. Contact them in week 6 and you'll have none before the competition.

**Once kits arrive**
- [ ] Build the field: mat, mission models, dual-lock, per `field-setup.pdf`
- [ ] Build a driving base — nothing attached to it yet

**Done when:** kits ordered, team registered, rulebook read, expert emails sent.

---

## Weeks 3–4 — Explore

Goal: understand every mission; lock the project problem.

**Robot Game**
- [ ] One analysis file per mission → [`../robot-game/missions/`](../robot-game/missions/README.md)
- [ ] Score each: points, difficulty 1–5, estimated seconds, field position
- [ ] Roll up into [`scoring-tracker.md`](../robot-game/scoring-tracker.md)

**Robot Design**
- [ ] Driving base drives straight 1m and turns 90° repeatably.
      **Fix this before building anything else** — every later problem
      compounds from an unreliable base.

**Code**
- [ ] Build the reusable My Blocks first: `drive_straight`, `turn_degrees`,
      `reset_gyro` → [`../code/my-blocks.md`](../code/my-blocks.md)

**Innovation Project**
- [ ] Narrow 20 ideas → 3 candidates → **1 chosen problem**
- [ ] Write it up in [`problem.md`](../innovation-project/problem.md)
- [ ] First expert conversation happens in this window

**Done when:** every mission analysed, base robot reliable, problem chosen.

---

## Weeks 5–6 — Commit

Goal: decide what you're actually doing. **After this, the mission list is fixed.**

**Robot Game**
- [ ] Pick the mission list. Use points-per-second, not enthusiasm.
- [ ] Group into runs by field location → [`strategy.md`](../robot-game/strategy.md)
- [ ] Write down a target score and why it's realistic
- [ ] Draft a run plan each → [`../robot-game/runs/`](../robot-game/runs/README.md)

> **Commit harder than feels comfortable.** With 6 weeks left, a mission list
> that keeps changing is the main way teams end up with nothing reliable.
> Pick fewer missions than you think you can do.

**Robot Design**
- [ ] Design and build one attachment per run
- [ ] Document each → [`../robot-design/attachments/`](../robot-design/attachments/README.md)
- [ ] Choose a navigation method and record the reasoning

**Innovation Project**
- [ ] Second expert interview
- [ ] Research existing solutions; find out why they fall short
- [ ] Design our solution → [`solution.md`](../innovation-project/solution.md)

**Done when:** mission list frozen, runs defined, attachments built, solution designed.

---

## Weeks 7–9 — Build & Iterate

The longest phase, and mostly repetition. This is where the score comes from.

**Robot Game — the core loop**
- [ ] Run each program **10 times**; log every attempt in its run file
- [ ] Below 80%? **Redesign it, don't re-tune it.**
- [ ] Full 2:30 timed practice matches with attachment swaps
- [ ] Track scores in [`scoring-tracker.md`](../robot-game/scoring-tracker.md)

> **Consistency beats ambition.** A 250-point run that works half the time
> averages worse than a 180-point run that always works — and it's miserable on
> the day. Cut what won't stabilise.

**Innovation Project**
- [ ] Build the prototype / model / detailed drawing
- [ ] **Share it with an expert and get real feedback**
- [ ] **Revise it based on what they said** — judges score this directly
- [ ] Draft the 5-minute presentation

**Engineering Notebook**
- [ ] ~70% complete by the end of week 9. Do not leave it to the last week.

**Done when:** every run ≥80%, solution revised after outside feedback,
notebook mostly written.

---

## Weeks 10–11 — Polish

Nothing new. Only refinement.

- [ ] **Freeze the robot design.** Late changes cause competition failures.
- [ ] Presentation rehearsed to time, without notes
- [ ] Every student can explain *any* part of the robot — judges choose who to ask
- [ ] Mock judging with an outside adult using the real rubrics
- [ ] Practice under pressure: noise, a timer, strangers watching
- [ ] Fill in the [judging prep sheets](judging/README.md)
- [ ] Notebook finished and submitted

**Done when:** presentation runs clean, notebook submitted, robot untouched for
a week and still scoring.

---

## Week 12 — Competition

- [ ] [`packing-list.md`](../competition/packing-list.md) the night before
- [ ] [`tournament-day.md`](../competition/tournament-day.md) on the day
- [ ] Every hub and spare battery charged
- [ ] Sleep. Tired teams make judging mistakes.

---

## After

- [ ] [`retrospective.md`](retrospective.md), written while it's fresh

---

## Weekly rhythm

Roughly 2 hours:

| Time | What |
| --- | --- |
| 0:00–0:10 | Standup — did, next, blocked |
| 0:10–1:30 | Split into workstreams and build |
| 1:30–1:50 | Regroup, demo to each other |
| 1:50–2:00 | Log the meeting, assign next steps |

Copy [`_TEMPLATE.md`](../meetings/_TEMPLATE.md) each session. The log is the raw
material for the Engineering Notebook and the evidence judges ask for.

**At 12 weeks, consider meeting twice a week** if schedules allow. Weeks 7–9
especially — reliability comes from repetition, and repetition needs table time.

## Protecting the project time

Robot Game is **one quarter** of the Champion's Award. The classic failure is
spending twelve weeks on the robot and improvising the Innovation Project in
week 11.

Guard against it: **every meeting, someone works on the project.** Even 20
minutes. Split the team rather than serialising the work.
