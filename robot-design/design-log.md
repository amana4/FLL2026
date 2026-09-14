# Design Log

Dated record of every meaningful change to the robot. **This is the single most
valuable document for Robot Design judging** — it's the proof that we iterated
rather than got lucky.

Add an entry whenever something changes. Failed experiments count and are often
the most interesting entries; write those down too.

Use **Kid 1** to **Kid 5** rather than real names — this page is published to the
public website. The roster is the key and is kept off the site.

## How to write an entry

Copy this block, newest at the top:

```markdown
## YYYY-MM-DD — Short title

**Problem:** what wasn't working
**Change:** what we did
**Result:** what happened, with numbers if we have them
**Next:** what this tells us to try next
**Who:** Kid 1, Kid 2
```

---

## YYYY-MM-DD — Example entry (delete once real entries exist)

**Problem:** The robot curved right on long drives — about 4cm off over 1m, enough
to miss the drop zone on R2.

**Change:** Added gyro correction inside the `drive_straight` My Block instead of
relying on matched motor power.

**Result:** Drift down to under 1cm over 1m. R2 success rate went from 4/10 to
9/10.

**Next:** Apply the same block to R1 and R3, which have the same problem.

**Who:** _Kid 1, Kid 2_

---

---

## 2026-09-13 — Port map in toolkit.py did not match the robot

**Problem:** `code/library/toolkit.py` had the wrong ports. Two sockets were
claimed twice and two sat empty:

- `LEFT_DRIVE = port.F`, but port F holds the right colour sensor
- `RIGHT_DRIVE = port.A`, but port A is the **left** drive motor
- `right_color = port.F` as well, so F was double-booked
- `attachment2` was commented out on port E, which the left colour sensor already had
- B and D were unused

So `init_robot` was asking the hub to pair a colour sensor with a motor, and to
treat the left wheel as the right one.

**Change:** Read all six port letters off the hub and made the file match.

| Socket | What is plugged in |
| --- | --- |
| A | Left drive motor |
| B | Right drive motor |
| C | Left attachment motor |
| D | Right attachment motor |
| E | Left colour sensor |
| F | Right colour sensor |

Also corrected the header comment, which claimed "Drive: A (left), E (right)". The
"A (left)" half was right and the code below it was wrong.

**Result:** Not yet retested on the robot. The file now describes a robot that can
exist, which the old one did not.

**Next:** Two things still unmeasured, both in the same file. Wheel diameter and
track width — the header says 87 mm and 143 mm, the code says 62.4 mm and 130 mm,
and nobody has used calipers. Also measure the attachment gear ratio; see
[`attachments/boxor-frame.md`](attachments/boxor-frame.md).

**Who:** _TODO_

---

## 2026-09-13 — Mat is 200 cm wide, not 236

**Problem:** The mission simulator was built assuming a 236.2 cm mat, from the FLL
table's inside width of 93 in. Every position in it was on a mat 18% too wide.

**Change:** Measured the mat two independent ways. The wireframe grid is 10 columns
of 20 cm, so 200 cm. The Mission Model Placement photo measures to an aspect ratio
of 1.75, and 2000/1143 = 1.750 while 2362/1143 = 2.066. The mat does not fill the
table's width.

**Result:** Simulator corrected to 200 × 114.3 cm. Also fixed the home areas, which
were drawn as a 45 cm square and are really quarter-circles of radius 48 cm.

**Next:** Confirm with a tape measure on the real mat. Measure the mat, not the
table. Survey data is in
[`../robot-game/field-positions.md`](../robot-game/field-positions.md).

**Who:** _TODO_

---

_Newest entries above this line._
