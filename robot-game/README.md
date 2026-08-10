# Robot Game

Scoring points on the table in **2.5 minutes**. Three official matches; **only
your best score counts** toward awards and advancement.

| File | What's in it |
| --- | --- |
| [`missions/`](missions/README.md) | All 15 missions with official scoring |
| [`strategy.md`](strategy.md) | Target score, run grouping, what we skip |
| [`scoring-tracker.md`](scoring-tracker.md) | Points available, practice scores |
| [`runs/`](runs/README.md) | One plan per robot run, with reliability logs |

## The loop

```
Analyze mission  →  Group into runs  →  Build attachment
       ↑                                       ↓
   Log results  ←  Run it 10 times  ←   Program the run
```

Stay in that loop until every run clears 80%.

## Equipment limits

From the rulebook (pages 14–15). Check these before designing anything:

| Limit | Value |
| --- | --- |
| Controllers | **1** max per match |
| Motors | **4** max, any mix |
| Sensors | Touch/force, colour, distance/ultrasonic, gyro only — any number |
| Power | One controller power pack **or** six AA batteries |
| Height limit at inspection | **12 in. (305 mm)** — a rule, not a bonus |
| Notebook paper | One sheet per home area, doesn't count as equipment |

All pieces must be **LEGO in original factory condition** — only string and
pneumatic tubes may be cut. Any programming language is allowed; the robot must
be autonomous outside home.

**Four motors is the real constraint.** Two go to driving, leaving two for
attachments. Plan mechanisms around that.

**On the height limit.** Everything must fit within the **two** launch areas and
under 12 in. — that is a requirement, and a taller robot fails inspection. Fitting
everything into **one** launch area is a separate thing, and it earns 20 points.

## The No Equipment Constraint

Eight of the fifteen missions carry a crossed-out-brick symbol, and for those:

> "A mission model cannot earn points if it is touching equipment at the end of
> the match."

**M01, M04, M05, M07, M09, M10, M12, M15.** If the robot parks or drops anything
touching one of those models, that mission scores nothing even though it looks
completed. Add "nothing left touching a model" to the end of every practice run.

## Rules that decide matches

Direct from the rulebook — these are the ones teams lose points to:

- **All wording means precisely and only what it says.** If a detail isn't
  mentioned, it doesn't matter. Read scoring conditions literally.
- **Ties/unclear calls go to the team** — benefit of the doubt is yours.
- Mission requirements must be **visibly met at the end of the match**, unless
  the mission specifies a method.
- "In" an area **includes the lines and the airspace above it**.
- Technicians may only handle things **completely within their own home area**,
  and may not pass anything between the two home areas.
- Interrupting the robot outside home costs **one precision token**.
- Objects picked up outside home after the last launch **go to the referee** —
  you don't get them back.
- You may not take models apart, separate the Dual Lock, or break a model.
  Points scored that way don't count.
- A mission model combined with your robot must be freeable **in a single
  motion, in perfect original condition**, if the referee asks.
- Don't touch the opposing team's field. Points they lose to your interference
  **score automatically for them**.

## Gracious Professionalism is scored at the table

Referees score every match: **Accomplished (3)** by default, **Exceeds (4)** for
above-and-beyond sportsmanship, **Developing (2)** for less. It adds to your
Core Values score.

Can't run the robot? Show up and explain what happened — you can still score 2–4.
Not showing up scores zero.

## Field setup

Follow the official Field Setup Video and `field-setup-reference-guide.pdf`. A
mat 1 cm out of position makes every program lie to you.

- [ ] Mat flat, aligned to the bottom wall, centred left-to-right
- [ ] Optional: tape the left and right edges with matte black gaffer tape
- [ ] Dual Lock placed per the wireframe
- [ ] All mission models built **exactly** per the building instructions
- [ ] The three interchangeable docks (mine, city, farm) seated and latched

**Recheck before every practice session.** Models drift.

> **At events, setups vary** — table construction, surface smoothness, shared
> mission interactions. Expect it and adapt graciously.

## The interchangeable docks — new this year

Missions 13, 14, and 15 sit on three docks: **mine, city, farm**. You choose
which model goes where before the match.

This matters for M15 Biocentric Architecture, whose Environmental Bonus depends
on the dock:

| Dock | Bonus action |
| --- | --- |
| Mine | Nesting canopy raised |
| City | Garden skylight completely in |
| Farm | Compost hatch opened, touching mat |

Put M15 on the dock matching whichever action your robot does **most reliably**.
It's a free 10 points for a decision made in the pit.

--8<-- "includes/abbreviations.md"
