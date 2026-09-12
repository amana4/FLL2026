# Mission 04 — Lucky Leaves

> Scoring conditions below are quoted from the official BIOGLOW Robot Game
> Rulebook (page 9). **The rulebook and Challenge Updates are the only
> authority** — if this file disagrees with them, they win.
>
> **Important: Challenge Update 01, published 2 September 2026, rewrote the
> constraints on this mission.** The update supersedes the rulebook. The new
> wording is in [Scoring constraints](#scoring-constraints-updated-2-september-2026)
> below.

| Field | Value |
| --- | --- |
| Mission ID | `M04` |
| Name | Lucky Leaves |
| Rulebook page | 9 |
| Challenge Set bags | 6 |
| **Max points** | **30** |
| Field location | Position 04 |

## The story

> Hidden in plain sight, the katydid camouflages with its leafy surroundings. Collect as many leaves as you can without disturbing this master of disguise.

## Scoring conditions

| Condition | Points |
| --- | --- |
| One leaf is completely removed, no longer touching the nest | **10** |
| **Bonus:** and the second leaf is completely removed, no longer touching the nest, with the katydid in its original starting position | **20 added** |

**Maximum: 30 points**

The bonus line above is the mission card wording. Read it together with the
updated constraints below, which say when the bonus is lost.

## Scoring constraints (updated 2 September 2026)

Challenge Update 01 replaced the constraint wording for this mission. Exact
text of the update:

> The nest is the mission model that holds the leaves and the katydid.
>
> The leaf habitat includes the nest and the marked area on the mat that
> surrounds it.
>
> If the katydid is completely outside the leaf habitat at any time during the
> match, the bonus is no longer available.
>
> If the katydid is completely outside the leaf habitat at the end of the match,
> the team scores zero points for this mission.

The update also states the reason for the change:

> Before the match begins, the leaves will be randomized within the nest, and
> teams will not be told the starting placement of the katydid. This is an
> intentional part of the challenge. To account for this unpredictability,
> mission constraints have been updated to extend flexibility.

FIRST says the Scoresheets, the Robot Game Excel Scorer and the Event Hub Score
Calculator will be reissued to match.

### What changed

| | Rulebook, 4 August | Update 01, 2 September |
| --- | --- | --- |
| Bonus lost when | katydid completely removed from **the nest**, at any time | katydid completely outside **the leaf habitat**, at any time |
| Mission scores zero when | katydid outside the leaf habitat at the end, **even partly** | katydid **completely** outside the leaf habitat at the end |

Both changes make the mission easier. The katydid may now be pushed out of the
nest and still earn the bonus, as long as it stays at least partly inside the
marked habitat area on the mat. A katydid hanging half over the habitat line at
the end of the match now scores, where before it scored zero.

**Open question for the referee.** The mission card still asks for the katydid
"in its original starting position" for the bonus, but the update says the
bonus survives anywhere inside the leaf habitat — and teams are no longer told
what the starting position was. Ask a referee at the first event which one they
call, and write the answer here.

## Notes and gotchas

**This mission can still score zero.** Push the katydid fully off the marked
habitat area and all 30 points go, not just the bonus. There is more room for
error than there was in August, but the failure is still total.

### The referee randomises the start position

From the Field Setup Reference Guide, p6:

> "The starting position of the katydid and leaves is randomized by the referee at
> the start of the match."

Update 01 confirms this and adds that the team is not told where the katydid
starts. A program that assumes fixed positions will fail on the day. Either
solve it with a sensor, or design a mechanism physically tolerant of where the
leaves are — or decide deliberately to skip it.

M04 is still one of the higher-risk missions on the field, but the update moved
it down from the worst. The scoresheet ticks **0, 1 or 2** leaves.

### No Equipment Constraint applies to this mission

This mission carries the crossed-out-brick symbol, so:

> "A mission model cannot earn points if it is touching equipment at the end of
> the match."

If the robot leaves an attachment, a wheel or anything else touching this model
when the match ends, the mission scores nothing even if it looks completed. Check
it at the end of every practice run.

## Our analysis

Fill this in during Weeks 3–4. Points-per-second is what drives the run plan.

| Question | Answer |
| --- | --- |
| Realistic points for us | _TODO_ |
| Difficulty (1 easy – 5 hard) | _TODO_ |
| Estimated time to run | _TODO_ s |
| Points per second | _TODO_ |
| Needs a special attachment? | _TODO_ |
| Combine with which missions? | _TODO_ |
| Risk of disturbing other models | _TODO_ |

**Verdict:** _Attempt / Attempt if time / Skip_ — because: _TODO_

## Our approach

_TODO — how we plan to solve it. Add a sketch or photo._

**Attachment:** _link to `robot-design/attachments/…`_
**Assigned to run:** _link to `robot-game/runs/…`_

## Attempt log

| Date | Attempts | Successes | Rate | What changed |
| --- | --- | --- | --- | --- |
| _TODO_ | | | | |

## Status

- [ ] Mission model built per instructions
- [ ] Scoring conditions understood by the whole team
- [ ] Approach designed
- [ ] Attachment built
- [ ] Programmed
- [ ] ≥80% success over 10 consecutive attempts
- [ ] Included in a full-match run
