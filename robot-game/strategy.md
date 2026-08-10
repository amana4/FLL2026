# Robot Game Strategy

The plan for turning 2 minutes 30 seconds into points.

## Target score

| | Points | Set on |
| --- | --- | --- |
| Realistic target | _TODO_ | _TODO_ |
| Stretch target | _TODO_ | _TODO_ |
| Best practice score so far | _TODO_ | _TODO_ |
| Best official match score | _TODO_ | _TODO_ |

**Why this target:** _TODO — which missions add up to it_

## Run breakdown

Missions are grouped into runs by **field location**, not by theme. The robot
should never cross the mat twice for the same area.

| Run | Missions | Points | Est. time | Attachment | Success rate | Status |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | _TODO_ | | | | | ☐ |
| R2 | _TODO_ | | | | | ☐ |
| R3 | _TODO_ | | | | | ☐ |
| R4 | _TODO_ | | | | | ☐ |
| | **Total** | _TODO_ | _TODO_ / 150s | | | |

**Time check:** total run time + attachment swaps must fit in 150 seconds. Budget
~5s per swap. If the total is over, cut the lowest points-per-second run.

## Missions we're skipping

Be explicit. Judges ask "why didn't you do that one?" and "it was too hard" is a
weak answer; "12 points, 25 seconds, and it risked knocking over a 40-point model"
is a strong one.

| Mission | Points | Why skipped |
| --- | --- | --- |
| _TODO_ | | |

## FIRST's own mission-selection heuristic

From the Team Meeting Guide, p14. More concrete than a points-per-second calculation
alone, and worth applying first as a filter:

> "Look for missions that:
> - Use basic robot skills like push, pull, or lift.
> - Have models close to a launch area.
> - Involve navigation with line detection.
> - Have easy access to home."

Score each candidate against those four, then use points-per-second to choose between
the survivors. A 40-point mission that needs a novel mechanism and a long crossing is
usually worse than two 20-point missions near a launch area.

See the [field map](field-map.md) for which missions are close to home and which are
along the far edge.

## Principles

Decisions we've committed to, so we stop re-arguing them:

1. **Consistency over maximum points.** An 80%-reliable run beats a 50%-reliable
   one worth more. Expected value, not best case.
2. **Fast attachment swaps.** Seconds in Base are dead seconds. Design for one
   motion, one hand.
3. **Square up before precision moves.** Wall or line alignment resets accumulated
   drift; gyro turns drift over a long run.
4. **One student, one run — but everyone can run everything.** Judges may ask
   anyone anything.
5. **Freeze the design at Meeting 19, Sunday 11 October.** Changes after that cause competition failures.

## Navigation method

| Technique | Where we use it | Why |
| --- | --- | --- |
| Gyro turns | _TODO_ | Accurate turns independent of wheel slip |
| Line following | _TODO_ | |
| Wall squaring | _TODO_ | Resets position error |
| Timed drive | _TODO_ | Last resort — least repeatable |

## Match-day sequencing

Order to run programs in, and who does what.

| Order | Run | Driver | Swap crew | Cumulative time |
| --- | --- | --- | --- | --- |
| 1 | _TODO_ | | | |

**If we're behind on time:** drop _TODO_ first, then _TODO_.
**If a run fails mid-match:** _TODO — recover or skip to next?_ Decide this now,
not at the table.

--8<-- "includes/abbreviations.md"
