# Field positions — measured

Where every mission model sits, in centimetres. This is the survey the
[mission simulator](../code/learn/README.md) uses, and the numbers the team should
check with a tape measure.

> **These are read off official diagrams, not measured on our mat.** Good to
> within a centimetre or two. Correct them at a meeting and date the change.

## The coordinate system

FIRST's own. The mat has a wireframe printed on it: **columns A to J** across,
**rows 1 to 6** up, cells **20 × 20 cm**. The Field Setup Guide says "Align each
model exactly to the mat wireframe", so this grid is the authority.

The 28.3 cm diagonal on the wireframe sheet confirms the cells are square, since
√2 × 20 = 28.28.

Our origin is the **bottom-left corner of the mat**. `x` runs right, `y` runs up,
both in centimetres.

## Mat size

**200 cm wide by 114.3 cm deep.**

This is narrower than people expect. The FLL table's inside width is 93 in
(2,362 mm), so the obvious assumption is a 236 cm mat. That is wrong — the mat
does not fill the table's width.

Two official documents agree on 200 cm:

| Source | Evidence |
| --- | --- |
| Wireframe grid | 10 columns of 20 cm is exactly 200 cm, and the sheet measures 113.4 cm tall |
| Mission Model Placement photo | Mat measures to an aspect ratio of 1.75. 2000/1143 = 1.750, while 2362/1143 = 2.066 |

Rows 1 to 5 are full 20 cm bands. Row 6 is short, about 12.6 cm, because six full
rows would need 120 cm on a 114.3 cm mat.

- [ ] Confirm with a tape measure. Measure the mat, not the table.

## Home areas

Both are **quarter-circles of radius 48 cm**, centred on the two bottom corners.
Measured independently from the wireframe sheet and from the placement photo;
both give 48.0 to 48.2 cm.

The left one is printed with a red border, the right with blue.

## The three printed lines

For line following and squaring up. Centre point and bounding box, in cm.

| Line | Centre | Box | Cells |
| --- | --- | --- | --- |
| Bent, upper left | 59.9, 87.7 | 30.4 × 9.6 | C5-D5 |
| Bent, upper right | 149.8, 89.1 | 36.1 × 11.1 | H5-I5 |
| Diagonal, centre | 97.5, 36.2 | 8.3 × 12.9 | E2-F2 |

These are bounding boxes, not shapes. The two upper lines are bent, not straight.

- [ ] Measure the actual line shapes and widths, so a colour sensor can be simulated

## Mission positions

From the mission number badges on the Mission Model Placement page. A badge sits
beside its model rather than on it, so treat these as "within a couple of
centimetres".

Where the wireframe sheet also shows a model outline in the same place, the two
sources are listed side by side. They agree closely, which is the main reason to
trust the 200 cm mat width.

| Mission | x cm | y cm | Cell | Outline on the wireframe sheet |
| --- | --- | --- | --- | --- |
| M01 Drone Survey | 88.0 | 9.2 | E1 | — |
| M02 Exploding Seeds | 63.8 | 55.1 | D3 | 63.8, 53.7 |
| M03 Flip the Rock | 9.7 | 68.0 | A4 | 8.1, 65.8 |
| M04 Lucky Leaves | 15.7 | 99.0 | A5 | 12.6, 101.1 |
| M05 Reaching Roots | 40.1 | 106.1 | C6 | — |
| M06 Leafcutter Frenzy | 151.3 | 106.2 | H6 | 153.6, 106.0 |
| M07 Humongous Fungus | 163.7 | 106.2 | I6 | — |
| M08 Tangled | 54.3 | 106.1 | C6 | 57.0, 106.3 |
| M09 Research Platform | 65.9 | 106.1 | D6 | — |
| M10 Fragile Microhabitats (top) | 78.3 | 102.3 | D6 | 75.2, 104.4 |
| M10 Fragile Microhabitats (centre) | 109.2 | 77.3 | F4 | — |
| M11 Window to the Past | 140.2 | 60.5 | H4 | 140.5, 59.1 |
| M12 Forest Elder | 192.0 | 76.5 | J4 | 193.8, 75.2 |

**M10 appears twice.** Two separate habitats, both scoring, at opposite ends of
the field. Check it against every run plan.

### The three interchangeable docks

M13, M14 and M15 go on these, and the team chooses which goes where before the
match. See [`field-map.md`](field-map.md).

| Dock | x cm | y cm | Cell |
| --- | --- | --- | --- |
| Mine | 189.1 | 102.7 | J6 |
| Farm | 101.2 | 64.9 | F4 |
| City | 128.6 | 10.2 | G1 |

## Our robot

| Measurement | Value |
| --- | --- |
| Width | 18 cm |
| Length | 18 cm |
| Height | 6 cm |

Height is not used by the simulator, which is a flat top-down view. It matters for
the 12 in (305 mm) inspection limit, where 6 cm is comfortable.

- [ ] Wheel diameter, measured with calipers
- [ ] Track width, wheel centre to wheel centre
- [ ] Where each attachment mounts, and how far it reaches

The first two are in [`toolkit.py`](../code/library/toolkit.py) as 62.4 mm and
130 mm, but the comment at the top of that file claims 87 mm and 143 mm. One of
them is wrong. See [lesson 3](../code/learn/03-ports.md).

## What is still missing

Position is not enough to simulate a mission. Each model also needs its
**kinematics**, and no official document gives them:

- what kind of joint — hinge, slider, rotation, or a loose piece pushed clear
- where the axis is, and how far it travels
- which direction of push moves it
- whether it latches or springs back

All fifteen missions are simulated at
[lesson 14](../code/learn/14-simulated-missions.md), with the right positions and
the right points, but the interaction rule is a uniform guess: get an attachment
within a few centimetres, run it far enough. Filling this table in is what would
make it faithful.

| Mission | Joint type | Axis at | Travel | Scores when |
| --- | --- | --- | --- | --- |
| M01 | _TODO_ | _TODO_ | _TODO_ | drone no longer touching the mat |
| M02 | _TODO_ | _TODO_ | _TODO_ | each seed no longer touching the stalk |
| M03 | _TODO_ | _TODO_ | _TODO_ | research flag down |
| M04 | _TODO_ | _TODO_ | _TODO_ | each leaf off the nest, katydid still in the habitat |
| M05 | _TODO_ | _TODO_ | _TODO_ | root partly, then completely, extended |
| M06 | _TODO_ | _TODO_ | _TODO_ | ant on the nest, then each fragment contained |
| M07 | _TODO_ | _TODO_ | _TODO_ | mycelium completely extended |
| M08 | _TODO_ | _TODO_ | _TODO_ | vine touching the mat |
| M09 | _TODO_ | _TODO_ | _TODO_ | platform raised, camera deployed, seed off the tree |
| M10 | none, do not touch | — | — | both habitats still in place |
| M11 | _TODO_ | _TODO_ | _TODO_ | root cover down, touching the mat |
| M12 | _TODO_ | _TODO_ | _TODO_ | cane raised, then support tie on the post |
| M13 | _TODO_ | _TODO_ | _TODO_ | species placed and young trees raised |
| M14 | _TODO_ | _TODO_ | _TODO_ | each seed contained, then each touching the mat |
| M15 | _TODO_ | _TODO_ | _TODO_ | canopy raised, skylight in, compost hatch open |

Start with M11 and M02. One is a single hinge, the other is loose objects, so
between them they cover most of the field.

## How these numbers were produced

Both source PDFs carry their information as pictures, so nothing is extractable
as text. The positions came from rendering the pages and measuring pixels:

```bash
swiftc -O tools/pdfpage.swift -o /tmp/pdfpage
/tmp/pdfpage docs/official-materials/fll-challenge-bioglow-field-setup-reference-guide.pdf /tmp/fsg 2 2 3
```

Then the red grid lines give the scale, and the mission badges give the positions.
Repeat it if FIRST reissues either document.

--8<-- "includes/abbreviations.md"
