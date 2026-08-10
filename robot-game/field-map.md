# Field Map

Twelve mission pages say things like "Position 05" without anywhere showing where
that is. This is that page. Run planning is entirely about grouping missions by
physical location, and that grouping freezes at Meeting 9, so this is worth
studying before then.

Drawn from the field map on page 8 of the Robot Game Rulebook and the Mission Model
Placement page of the Field Setup Reference Guide. It is our own diagram, not a
copy of theirs — so check it against the real mat, and trust the mat.

## The layout

The mat is landscape, roughly twice as wide as it is deep. Both home areas are
quarter-circles in the **bottom two corners**, which means every run starts and
ends at the bottom of the field and the far missions are along the top edge.

```
        ┌────────────────────────────────────────────────────────────┐
        │  04    05 08 09 10                    06 07          ▓MINE▓│  ← top edge
        │         ╲___                            ╲___              │
        │                                                           │
        │  03                    10                            12   │
        │                      ▓FARM▓        11                     │
        │            02                                             │
        │                        ╲__                                │
        │  ╭──────╮                                                 │
        │  │ LEFT │        01        ▓CITY▓            ╭───────╮    │
        │  │ HOME │                                    │ RIGHT │    │
        └──┴──────┴────────────────────────────────────┴ HOME  ┴────┘
                                                       bottom edge
```

`▓ ▓` marks the three interchangeable docks. `╲__` marks the three black lines
printed on the mat, which are there for line-following and squaring up.

## Where each mission sits

| Mission | Where | Distance from home |
| --- | --- | --- |
| **M01** Drone Survey | Bottom centre, just right of the left home | **Closest to home** |
| **M02** Exploding Seeds | Centre-left, mid-depth | Middle |
| **M03** Flip the Rock | Far left edge, mid-depth | Middle, but a long way left |
| **M04** Lucky Leaves | Top-left corner | **Far** |
| **M05** Reaching Roots | Top edge, left of centre | Far |
| **M06** Leafcutter Frenzy | Top edge, right of centre | Far |
| **M07** Humongous Fungus | Top edge, right of centre, beside M06 | Far |
| **M08** Tangled | Top edge, left of centre, beside M05 | Far |
| **M09** Research Platform | Top edge, left of centre, beside M08 | Far |
| **M10** Fragile Microhabitats | **Two places:** top edge near M09, and centre of the field | Both |
| **M11** Window to the Past | Centre-right, mid-depth | Middle |
| **M12** Forest Elder | Far right edge, mid-depth | Middle, but a long way right |
| **M13/M14/M15** | Whichever dock you place them on | Depends |

## The three docks

You choose which of M13, M14 and M15 goes on each dock before the match, and the
referee records the choice for M15 on the scoresheet.

| Dock | Where it is | M15 bonus action if placed here |
| --- | --- | --- |
| **Mine** | Top-right corner, on the rocky ground | Nesting canopy raised |
| **Farm** | Centre of the field, on the tan farmland | Compost hatch opened, touching the mat |
| **City** | Bottom centre-right, in the grey built-up area | Garden skylight completely in |

The dock *positions* are certain — they are marked on the official placement page.
Matching each position to its **name** is our reading of the mat artwork: crop rows
in the centre, buildings and roads at the bottom right, rocky ground top right. The
M13 setup photo showing the "Mine dock" is on rocky ground at the blue right-hand
edge, which supports it. **Confirm the names against the real mat before relying on
this for M15's bonus.**

## What the layout implies for run planning

**Everything far is along the top edge.** M04, M05, M08, M09, M06, M07 and one of
the M10 pairs all sit on the top edge. That is one long trip, and it is where most
of the driving time goes.

**Two natural top-edge clusters.** M05, M08, M09 and the upper M10 sit together
left of centre. M06 and M07 sit together right of centre. Those are two runs, not
one, unless the robot can cross the top of the field reliably.

**M03 and M12 are the outliers.** One is hard left, the other hard right, both at
mid-depth. Each is a detour rather than something you pick up on the way past.

**M01 is nearly free.** It is the closest thing to home. Worth doing on whichever
run leaves or returns past it.

**M10 is a hazard, not a destination.** Its two locations sit in the middle of the
routes to the top edge. You score its 20 points by *not* disturbing it, so plan
routes that keep clear of both. It also carries the No Equipment Constraint, so
nothing may be left touching it at the end.

**The docks are spread out on purpose.** Mine is top-right, Farm is centre, City is
bottom-right. Placing an easy mission on the far dock and a hard one near home is a
real decision, so make it deliberately rather than by habit.

## Starting side

Rule 21 of the coach guide is blunt about this: when developing your mission
strategy, decide which launch area each run starts from. With both homes at the
bottom corners:

- Left home is closer to M03, M04 and the left half of the top edge.
- Right home is closer to M12, M11, M06, M07 and the City dock.

You may launch from either home on any run, and equipment can be split between
both — but you cannot pass anything from one home to the other during the match, so
whatever a run needs must already be on the correct side.

## Use the wireframe grid for the details

For real distances, print the
[Wireframe and Path Grid](https://github.com/amana4/FLL2026/blob/main/docs/official-materials/fll-challenge-bioglow-wireframe-grid.pdf).
It is an A–J by 1–6 grid of **20 cm cells** over the mat, which gives the team a
shared vocabulary — "drive to F3, turn left, then square on the line" — instead of
vague gestures at the field.

It also pairs with the official Pseudocode Worksheet in the Engineering Notebook,
which has a Robot Path Diagram box expecting exactly this kind of plan. Judges
recognise that worksheet because FIRST wrote it.

## Fill this in as you learn it

The table above is geography. What matters is your own timings.

| From | To | Time | Notes |
| --- | --- | --- | --- |
| Left home | | | |
| Right home | | | |

Then group by location in [`strategy.md`](strategy.md) and write the runs up in
[`runs/`](runs/README.md).

--8<-- "includes/abbreviations.md"
