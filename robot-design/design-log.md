# Design Log

Dated record of every meaningful change to the robot. **This is the single most
valuable document for Robot Design judging** — it's the proof that we iterated
rather than got lucky.

Add an entry whenever something changes. Failed experiments count and are often
the most interesting entries; write those down too.

## How to write an entry

Copy this block, newest at the top:

```markdown
## YYYY-MM-DD — Short title

**Problem:** what wasn't working
**Change:** what we did
**Result:** what happened, with numbers if we have them
**Next:** what this tells us to try next
**Who:** names
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

**Who:** _names_

---

_Newest entries above this line._
