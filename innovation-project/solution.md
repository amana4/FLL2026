# Our Solution

## In one sentence

> A cheap backyard kit — a camera watching one marked flower patch, plus a fixed
> counting method — that lets an ordinary family measure **how many different
> kinds** of native bee visit their garden, make one deliberate change, and see
> whether it worked.

## What it is

Three parts, and the third is the one that matters.

**1. A camera on a patch.** A phone or a small camera on a tripod pointed at a
marked patch of flowers, recording for a set time, at set times of day.

**2. A counting method.** Photographs get sorted into visibly different types of
bee. Same patch size, same duration, same weather rules every time, so two counts
can honestly be compared. Written up in
[`field-protocol.md`](field-protocol.md).

**3. An experiment.** Each student counts their own garden **before** changing
anything, then makes one change, then counts again the same way. Five gardens,
five experiments, each its own control.

The kit is the deliverable. The result is the proof it works.

## Why it's innovative

Not "nobody has done this" — usually somebody has. The question is what's new
about *our* approach.

| | |
| --- | --- |
| What exists already | Scientists survey bee diversity using **pan traps** — coloured bowls of soapy water. It is the standard method and it is accurate. Citizen apps like iNaturalist identify individual photos. Plenty of guides tell you which flowers to plant. |
| What we do differently | Pan traps **kill the bees they count**, which is indefensible in a project about helping bees, and they need an expert to identify the catch. We measure **non-lethally**, from photographs, at a level of detail a child can actually apply — and we measure the *same garden twice*, before and after one change. |
| Why that difference matters | It turns "plant these flowers, it should help" into "we changed this one thing and the number of different bees went from four to seven." A household can repeat that. A pan trap survey is not something a family will ever do. |

**The non-lethal choice is a design decision, not an accident.** Say so to judges.
Choosing a slightly less precise method on purpose, for a stated reason, is
exactly the kind of thinking the rubric rewards.

## Who it's for

Families with a garden who want to help native bees and currently have no way to
know whether what they did worked. Secondarily: schools, and anyone giving
planting advice who would like local before-and-after evidence.

## Interventions worth testing

One change per garden, so each student owns a result. Chosen for **whether an
effect could show inside our season** — that is the constraint that rules things
in and out.

| Change | Why it should work | Shows a result by November? |
| --- | --- | --- |
| **Add native flowers already in bloom** | Immediate food. Locally native species suit local bees. | Yes — bees arrive within days |
| **Clear a patch of bare, undisturbed soil** | The large majority of native bees nest in the ground and cannot use mulched or compacted soil. Most overlooked change there is. | Possibly — worth trying, and the reasoning impresses |
| **Stop mowing one area** | Lets small flowers bloom and leaves stems standing | Maybe, within weeks |
| **Shallow water with a landing surface** | Bees drown in steep-sided water | Fast, but a small effect |
| **Stop using pesticide in the test area** | Removes direct harm | Yes, but hard to show as a *gain* |
| **Bee hotel** | Homes for cavity-nesting species | **No — and be careful.** Occupancy takes a season, and a badly built or never-cleaned hotel concentrates parasites and disease, so it can do net harm. If we build one, we must plan the cleaning and say so. |

The bare-soil one is the sleeper. Ask an expert about it early — if it holds up
locally, it is a genuinely counter-intuitive finding for a presentation.

## Prototype

What we built to show it: model, drawing, app mockup, working device.

| | |
| --- | --- |
| Type | Camera rig plus a written protocol and a photo dataset |
| Built on | _TODO — date_ |
| Materials | _TODO — phone or Raspberry Pi + camera module, tripod, patch markers, printed ID sheet_ |

Start with a phone on a tripod. It costs nothing and proves the method before any
money is spent. Only move to a Raspberry Pi and camera module if the team needs
long unattended recording — and note that **fixed-interval stills or continuous
video over a known patch beats motion detection**, because small fast insects
trigger motion sensors badly.

_TODO — photos_

## Versions

**Keep every version.** The v1 → v2 change *is* the Iterate score.

| Version | Date | What it looked like | Why we changed it | Feedback that drove it |
| --- | --- | --- | --- | --- |
| v1 | _TODO_ | | | |
| v2 | _TODO_ | | | |

## Honest limitations

What it doesn't do, what it would cost, what would have to be true for it to work
at scale. Naming your own weaknesses reads as confidence, not doubt — judges
respond well to it.

- **We cannot identify most native bees to species from a photograph.** Many
  species are only separable under a microscope by a specialist. We count
  *visibly different types*, which is a real method but a coarser one. Say this
  plainly rather than claiming a species list.
- **Six weeks is short.** Flower changes can show up fast; nesting changes cannot.
- **Five gardens is a small sample**, and they are all in one neighbourhood.
- **Weather and time of day affect counts more than most interventions do.** If we
  do not control them, our result is just weather.
- **Photos miss the smallest and fastest bees**, and any species active before we
  start recording.
- We measure *visits to a patch*, not how many bees live there. A bee counted may
  be nesting next door.

## What we'd do next

_TODO — after the first round of counts, and after an expert has reviewed the
protocol_
