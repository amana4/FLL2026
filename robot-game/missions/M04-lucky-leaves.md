# Mission 04 — Lucky Leaves

> Scoring conditions below are quoted from the official BIOGLOW Robot Game
> Rulebook (page 9). **The rulebook and Challenge Updates are the only
> authority** — if this file disagrees with them, they win.

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

## Notes and gotchas

**This mission can score you zero.** Direct rulebook wording:

> If the katydid is completely removed from the nest at any time, the bonus is no longer available.
>
> If the katydid is outside the leaf habitat at the end of the match, even partly, the team scores zero points for this mission. The leaf habitat includes the nest and the marked area on the mat surrounding it.

So a careless grab loses all 30 points, not just the bonus. Design for precision here.

### The referee randomises the start position

From the Field Setup Reference Guide, p6:

> "The starting position of the katydid and leaves is randomized by the referee at
> the start of the match."

This is the most important fact about this mission and it changes the approach
completely. A program that assumes fixed positions will fail on the day. Either
solve it with a sensor, or design a mechanism physically tolerant of where the
leaves are — or decide deliberately to skip it.

Combined with the zero-score rule below, M04 is the highest-risk mission on the
field. The scoresheet ticks **0, 1 or 2** leaves.

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
