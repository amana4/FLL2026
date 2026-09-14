# 14. Simulated missions

The whole field is on the mat now — all fifteen missions, 460 points, and the page
keeps score.

Press **Run**. The robot does nothing at all, and it still scores 20 points.

<div class="spike-run" data-height="320" markdown="1">

```python
await init_robot()
field.report()
```

</div>

Read the total: **20 of 460**. That 460 is the real number. The scoresheet's 530
is 460 of missions plus 20 for passing inspection and 50 for keeping all six
precision tokens, and neither of those is something a program can earn.

M10a and M10b scored 10 each **for not being touched**. That is the whole of
[M10 Fragile Microhabitats](../../robot-game/missions/M10-fragile-microhabitats.md):
both habitats start in position, and you keep the points by leaving them alone.

Twenty points for doing nothing is the best points-per-second on the field.

## Reading the picture

| On screen | Meaning |
| --- | --- |
| Dashed ring | An attachment has to get inside this to score |
| Solid ring | Scored |
| Red ring | A fragile model you disturbed |
| Small dot in the middle | Where the model actually is |
| Red dot with its own dashed circle | M04's katydid, and the leaf habitat |

Under the picture there is now a **score**, next to the position readout.

## Every mission, and how to reach it

Turn and drive from the left launch area at 30, 20. Worked out with `atan2` and
`hypot`, which the next section explains.

| Mission | Cell | Worth | `turn_deg` | `drive_cm` |
| --- | --- | --- | --- | --- |
| M01 Drone Survey | E1 | 30 | 101 | 50 |
| M02 Exploding Seeds | D3 | 30 | 44 | 40 |
| M03 Flip the Rock | A4 | 30 | -23 | 43 |
| M04 Lucky Leaves | A5 | 30 | -10 | 71 |
| M05 Reaching Roots | C6 | 20 | 7 | 78 |
| M06 Leafcutter Frenzy | H6 | 40 | 55 | 140 |
| M07 Humongous Fungus | I6 | 40 | 57 | 150 |
| M08 Tangled | C6 | 30 | 16 | 80 |
| M09 Research Platform | D6 | 30 | 23 | 84 |
| M10a spider habitat | D6 | 10 | — | leave it alone |
| M10b snail habitat | F4 | 10 | — | leave it alone |
| M11 Window to the Past | H4 | 20 | 70 | 108 |
| M12 Forest Elder | J4 | 30 | 71 | 163 |
| M13 Keystone Species | J6 | 30 | 63 | 170 |
| M14 Seeds of Renewal | G1 | 40 | 96 | 90 |
| M15 Biocentric Architecture | F4 | 40 | 58 | 75 |

Those are single-mission routes from home. A real run does several without going
back, which is harder, and is the point of this page.

**The field is crowded.** M05, M08, M09 and M10a all sit within 40 cm of each other
along the top edge, and M10b sits in the middle of almost every route to the right
half. So a straight line often scores a neighbour by accident, or wrecks one. Both
happen in the examples below.

## Your first real mission

M11 is at 140.2, 60.5. Home is at 30, 20. So the robot needs to turn towards it,
drive, and run the left attachment.

<div class="spike-run" data-height="320" markdown="1">

```python
await init_robot()

await turn_deg(70)
await drive_cm(109)
await run_attachment_deg(attachment1, 120)

field.report()
```

</div>

Twenty points. Now delete the `run_attachment_deg` line and run it again. The robot
arrives in exactly the right place and scores nothing, because arriving is not the
mission.

### Where 70 and 109 came from

Straight trigonometry, and you can make Python do it.

<div class="spike-run" data-view="none" markdown="1">

```python
from math import atan2, degrees, hypot

start_x, start_y = 30.0, 20.0
target = field.get("M11")

dx = target.x - start_x
dy = target.y - start_y

print("across ", round(dx, 1), "cm")
print("up     ", round(dy, 1), "cm")
print("turn   ", round(degrees(atan2(dx, dy)), 1), "degrees")
print("drive  ", round(hypot(dx, dy), 1), "cm")
```

</div>

`atan2(dx, dy)` gives the heading, and `hypot(dx, dy)` gives the straight-line
distance. Note the order: `dx` first, because our headings are measured from
straight up the mat rather than from the side.

The drive comes out at 117.4 and we used 109. That is deliberate — stop short so
the attachment reaches the model instead of the robot parking on top of it.

## A mission with no attachment

[M08 Tangled](../../robot-game/missions/M08-tangled.md) is 30 points for one
condition, the best single-action value on the field. The robot just has to reach
it.

<div class="spike-run" data-height="320" markdown="1">

```python
await init_robot()
await turn_deg(16)
await drive_cm(84)
field.report()
```

</div>

Thirty points, no arm, no attachment. Worth remembering when you plan a run.

## A mission worth 30 in three pieces

[M02 Exploding Seeds](../../robot-game/missions/M02-exploding-seeds.md) has three
seeds at 10 points each. One long attachment run can release all three.

<div class="spike-run" data-height="320" markdown="1">

```python
await init_robot()
await turn_deg(44)
await drive_cm(41)
await run_attachment_deg(attachment1, 180)
field.report()
```

</div>

Try 60 instead of 180 and watch the score drop. The arm has to travel far enough,
which is exactly the thing you cannot tell from the code and have to measure on the
mat.

## The mission that punishes you

[M04 Lucky Leaves](../../robot-game/missions/M04-lucky-leaves.md) is the
interesting one. Two leaves, 10 and then a 20 bonus, and a katydid that must stay
at least partly inside the leaf habitat.

The katydid's starting position is **randomised**, because Challenge Update 01 says
teams are not told it. Run this a few times and watch the red dot move.

<div class="spike-run" data-height="320" markdown="1">

```python
await init_robot()

await turn_deg(-10)
await drive_cm(72)
await run_attachment_deg(attachment1, 150)
await drive_cm(-20)

field.report()
```

</div>

Thirty points, bonus kept. Now be greedy. Drive 82 instead of 72, ten centimetres
deeper in:

<div class="spike-run" data-height="320" markdown="1">

```python
await init_robot()

await turn_deg(-10)
await drive_cm(82)
await run_attachment_deg(attachment1, 150)

field.report()
```

</div>

**Zero.** Not "fewer points" — zero. The robot shoved the katydid completely out of
the leaf habitat, and that is the one mission on the field where a careless approach
loses everything.

Ten centimetres. That is the whole lesson.

## Six shapes of scoring

Not every mission is "do the thing, get the points". The scoresheet has six
different shapes, and knowing which one you are facing changes how you program it.

### One: a bonus that needs a second action

M01, M03 and M12 all pay a base then a bonus. The bonus is a *different* action, so
in this simulator it wants more arm travel.

<div class="spike-run" data-height="320" markdown="1">

```python
await init_robot()
await turn_deg(-23)
await drive_cm(43)

await move_attachment_deg(attachment1, 60, velocity=400)
print("after a short run: ", field.get("M03").scored_points())

await move_attachment_deg(attachment1, 200, velocity=400)
print("after a longer run:", field.get("M03").scored_points())

field.report(only_scoring=True)
```

</div>

Twenty, then thirty. The flag went down first, and the rock only got put back when
the arm kept going.

Note `move_attachment_deg` rather than `run_attachment_deg` — the second of those
silently refuses anything over 200 degrees, which is
[lesson 11](11-attachments.md).

### Two: partial credit

M05 is the only mission with a middle answer. The scoresheet reads
**No / Partially (10) / Completely (20)**, and they do not add up.

<div class="spike-run" data-height="320" markdown="1">

```python
await init_robot()
await turn_deg(7)
await drive_cm(78)

await move_attachment_deg(attachment1, 60, velocity=400)
print("partly extended:    ", field.get("M05").scored_points())

await move_attachment_deg(attachment1, 120, velocity=400)
print("completely extended:", field.get("M05").scored_points())

await drive_cm(-25)
field.report(only_scoring=True)
```

</div>

Ten, then twenty. Not thirty. Half a job is worth exactly half.

### Three: a gate

M06 has a row on the scoresheet with **no points**: "ant touching the nest". It is
not worth anything on its own, and nothing else counts until it is done.

<div class="spike-run" data-height="320" markdown="1">

```python
await init_robot()

# straight up the middle runs over M10b, so go along the bottom first
await turn_deg(90)
await drive_cm(110)
await turn_deg(-82)
await drive_cm(78)

await move_attachment_deg(attachment1, 300, velocity=500)
field.report(only_scoring=True)
```

</div>

Forty points: the ant, then four leaf fragments at 10 each. Drop the 300 to 20 and
the whole thing scores nothing, because the gate never opened.

The two-leg route is not decoration. Driving straight at M06 crosses M10b, and that
costs 10 points before you arrive.

### Four: three separate conditions

M09 pays 10, 10 and 10 for three unrelated things. There is no bonus and no gate,
so more arm travel simply scores more.

<div class="spike-run" data-height="320" markdown="1">

```python
await init_robot()
await turn_deg(23)
await drive_cm(84)

for degrees in (60, 60, 60):
    await move_attachment_deg(attachment1, degrees, velocity=400)
    print("score so far:", field.get("M09").scored_points())

await drive_cm(-25)
field.report(only_scoring=True)
```

</div>

### Five: the one you cannot do alone

M07's bonus is **connections formed with the opposing plant root**. Both teams
score if both fully extend. You cannot earn it by yourself, and no amount of
programming changes that.

<div class="spike-run" data-height="320" markdown="1">

```python
await init_robot()

await turn_deg(90)
await drive_cm(110)
await turn_deg(-75)
await drive_cm(80)

await move_attachment_deg(attachment1, 100, velocity=400)
await drive_cm(-25)

print("on our own:      ", field.get("M07").scored_points())

field.partner(2)
print("partner extends: ", field.get("M07").scored_points())

field.report(only_scoring=True)
```

</div>

Twenty on our own, forty with the partner. `field.partner()` stands in for a
thirty-second conversation at the table before the round. It is free points for
both teams, and teams forget to ask.

That route also picks up 10 from M06 on the way past, because the two models sit
side by side on the top edge. Accidental points are still points.

### Six: a decision made before the match

M13, M14 and M15 sit on the three interchangeable docks, and you choose which goes
where. M15 pays a further 10 if **the dock's greatest need was met** — and the
referee writes your choice on the scoresheet before you launch.

<div class="spike-run" data-height="320" markdown="1">

```python
field.declare("M15", "city")          # we tell the referee: city dock

await init_robot()
await turn_deg(58)
await drive_cm(75)
await move_attachment_deg(attachment1, 320, velocity=500)
await drive_cm(-25)

field.report(only_scoring=True)
```

</div>

Thirty, not forty. M15 is actually on the **farm** dock, so the declaration was
wrong and the bonus is gone. Change `"city"` to `"farm"` and run it again.

You can also move it:

<div class="spike-run" data-height="320" markdown="1">

```python
field.set_dock("M15", "mine")
field.declare("M15", "mine")

target = field.get("M15")
print("M15 is now at", round(target.x, 1), round(target.y, 1))

await init_robot()
await turn_deg(63)
await drive_cm(170)
await move_attachment_deg(attachment1, 320, velocity=500)
await drive_cm(-25)

field.report(only_scoring=True)
```

</div>

Forty. Same mission, a different corner of the mat, and a much longer drive. That
trade is the whole reason the dock choice is a strategy decision rather than a
detail.

`set_dock` is a **swap**, not a move. There are three models and three docks, so
sending M15 to the mine sends whatever was there to the farm. Two models cannot
share a dock on a real field either.

Try 160 instead of 170. It scores 10, because the arm ends up just too far away to
reach anything, and the only thing that still pays is the declaration. Ten
centimetres again.

## The No Equipment Constraint

Eight missions carry a crossed-out-brick symbol, M10 among them. If your robot is
touching the model when the match ends, that mission scores nothing, however well
it went.

<div class="spike-run" data-height="320" markdown="1">

```python
await init_robot()
await turn_deg(30)
await drive_cm(95)
field.report()
```

</div>

The robot parked on M10a. Read its line: **0, equipment touching it at the end.**

Now reverse off it before the match ends:

<div class="spike-run" data-height="320" markdown="1">

```python
await init_robot()
await turn_deg(30)
await drive_cm(95)
await drive_cm(-35)
field.report()
```

</div>

Still 0, but for a different reason: **disturbed**. Nothing is touching it now, but
the habitat has been shoved out of its starting position, and that is what M10 pays
for. Backing off does not undo it.

Two different rules, two identical scores, and only the message tells you which one
bit you.

## Scoring more than one

Nothing stops you doing several in a row. Here are M11 and M02 in one launch:

<div class="spike-run" data-height="340" markdown="1">

```python
async def run_m02():
    await turn_deg(44)
    await drive_cm(41)
    await run_attachment_deg(attachment1, 180)

async def run_m11():
    await turn_deg(38)
    await drive_cm(72)
    await run_attachment_deg(attachment1, 120)

async def main():
    await init_robot()
    await run_m02()
    await run_m11()
    field.report()

runloop.run(main())
```

</div>

Seventy points: 30 for M02, 20 for M11, and 20 for leaving both M10 habitats alone.

That is the `run` and `main` shape from [lesson 12](12-a-mission.md), doing two
missions from one launch.

### Turns are relative, and that is the trap

The second turn is 38, not 70. After M02 the robot sits at about 58.5, 49.5 and is
already pointing at 44 degrees.

From there the heading it *wants* is 82 degrees. So the turn it needs is the
difference: 82 minus 44 is 38.

`turn_deg` always turns **from where you are now**, never to a compass bearing.
Combined runs go wrong here more than anywhere else. Draw it before you code it —
[lesson 13](13-flowcharts-judges.md).

## Useful things `field` can do

| Call | What it gives you |
| --- | --- |
| `field.report()` | The table, all sixteen models |
| `field.report(only_scoring=True)` | Just the ones that scored |
| `field.score()` | The total, as a number |
| `field.max_score()` | 460, the most the missions can give |
| `field.get("M11")` | One model, with `.x`, `.y`, `.scored_points()`, `.status()` |
| `field.set_dock("M15", "mine")` | Move M13, M14 or M15 to another dock |
| `field.declare("M15", "mine")` | Tell the referee your dock choice |
| `field.partner(2)` | Your match partner extends theirs, for M07 |
| `field.reset()` | Put everything back and re-randomise M04 |
| `field.models` | The whole list, to loop over |
| `field.DOCKS` | Where the three docks are |

<div class="spike-run" data-view="none" markdown="1">

```python
total = 0
for m in field.models:
    total = total + m.max_points()
    print("%-5s %3d points  at %5.1f %5.1f" % (m.key, m.max_points(), m.x, m.y))
print("the missions are worth", total, "altogether")
```

</div>

Sixteen models for fifteen missions, because M10's two habitats score separately.

`field` exists only on this website. There is no such thing on the hub, because a
real robot cannot see the mat or read the score.

## Your turn

Score M08 and M11 in one launch, and finish **without disturbing either M10
habitat**. Full marks is 70: thirty for M08, twenty for M11, twenty for restraint.

<div class="spike-run" data-height="340" markdown="1">

```python
async def main():
    await init_robot()
    # your route here
    field.report()

runloop.run(main())
```

</div>

??? question "Try the obvious route first"

    M08 is on the way out, so do it first and then head across to M11.

    ```python
    async def main():
        await init_robot()
        await turn_deg(16)
        await drive_cm(84)          # M08 scores on contact
        await turn_deg(99)
        await drive_cm(86)
        await run_attachment_deg(attachment1, 120)
        field.report()

    runloop.run(main())
    ```

    Sixty, not seventy. Both missions scored, and **M10b is red**.

    The straight line from M08 to M11 runs almost exactly over the centre
    habitat at 109.2, 77.3. The robot drove through it.

??? question "Now the route that scores 70"

    Do M11 first, reverse away from it, then cross underneath M10b.

    ```python
    async def main():
        await init_robot()

        await turn_deg(70)
        await drive_cm(109)
        await run_attachment_deg(attachment1, 120)   # M11

        await drive_cm(-30)                          # back off, keeps NEC clear
        await turn_deg(-110)
        await drive_cm(77)                           # M08 on contact

        field.report()

    runloop.run(main())
    ```

    Seventy. The reverse does two jobs: it clears M11 so the No Equipment
    Constraint cannot bite, and it drops the robot low enough to pass south of
    M10b.

    **This is what route planning actually is.** Not the shortest path between two
    models, but the shortest one that does not wreck a third. Every real run plan
    in [`robot-game/runs/`](../../robot-game/runs/README.md) is this argument,
    fifteen times over.

## Important: this is not the real mat

Three things here are official and worth trusting:

- **Positions**, from FIRST's own diagrams. See
  [`robot-game/field-positions.md`](../../robot-game/field-positions.md).
- **Points and conditions**, from the scoresheet. The 460 total is a real check:
  it matches the official 530 once you take off inspection and tokens.
- **Which missions carry the NEC**, all nine models of them.

**Everything about how a model moves is invented.** No official document says which
way the root cover hinges, how far, or how hard you have to push it. So this page
assumes: get an attachment within a few centimetres, run it far enough, and the
model does its thing. Bonuses want more travel than base conditions, on the theory
that a bonus is a second action.

That is the right shape and the wrong detail. What this page is genuinely good for:

- sequencing a mission, and seeing that arriving is not scoring
- working out routes with `atan2` and `hypot`
- feeling why M04 can score zero and why M10 pays you for restraint
- learning the six scoring shapes before you meet them on a scoresheet
- practising combined runs and relative turns
- arguing about dock placement with numbers instead of opinions

What only the real mat can tell you: whether 120 degrees of arm is enough, how
close is close enough, and what happens on the tenth run rather than the first.

To make this properly faithful, somebody has to sit with each model and write down
how it actually moves. There is a blank table waiting in
[`field-positions.md`](../../robot-game/field-positions.md) — one row per model,
and it is a genuinely useful hour with the field in front of you.

## Words from this lesson

| Word | Meaning |
| --- | --- |
| trigger zone | How close an attachment has to get for a model to react |
| `atan2` | Works out an angle from an across and an up distance |
| `hypot` | Works out a straight-line distance from the same two |
| relative turn | A turn measured from where you are already pointing |
| NEC | No Equipment Constraint. Touching the model at the end scores zero |

--8<-- "includes/abbreviations.md"
