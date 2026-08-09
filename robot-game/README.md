# Robot Game

Everything about scoring points on the table in 2:30.

| File | What's in it |
| --- | --- |
| [`strategy.md`](strategy.md) | Target score, run grouping, what we skip and why |
| [`scoring-tracker.md`](scoring-tracker.md) | Points available, practice scores over time |
| [`missions/`](missions/) | One analysis file per mission |
| [`runs/`](runs/) | One plan per robot run, with reliability logs |

## The loop

```
Analyze mission  →  Group into runs  →  Build attachment
       ↑                                       ↓
   Log results  ←  Run it 10 times  ←   Program the run
```

Stay in that loop until every run clears 80%.

## Rules that bite teams every year

Verify each against the BIOGLOW rulebook — these are general FLL patterns, not
season-specific quotes.

- Equipment must fit within the launch area at the start of the match.
- You may only touch the robot in Base; touching it elsewhere is an interruption.
- Interruptions cost Precision Tokens, and leftover tokens are worth points.
- Anything the robot leaves outside Base stays there — you can't retrieve it freely.
- The match ends at 2:30 exactly; a mission half-done scores nothing.

## Field setup

Build it exactly per `field-setup.pdf`. A mat that's 1cm off makes every program
lie to you.

- [ ] Mat flat, no wrinkles, taped or bordered per spec
- [ ] All mission models built and dual-locked in the correct positions
- [ ] Border walls square
- [ ] Lighting consistent if we're using light/color sensors

**Recheck the field before every practice session.** Models drift.
