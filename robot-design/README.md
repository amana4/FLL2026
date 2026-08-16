# Robot Design

The physical robot: how it's built, why it's built that way, and the evidence we
show judges.

| File | What's in it |
| --- | --- |
| [`chassis.md`](chassis.md) | The driving base and its sensors |
| [`design-log.md`](design-log.md) | Dated record of what we changed and why |
| [`attachments/`](attachments/README.md) | One file per attachment |

## Before we design ours: what other teams worked out

**Six chassis designs, side by side** — ten slides comparing HummerOne Pro, Xbot,
YellowBot v1 and v2, Track-X and Boxor, and pulling out the choices the good ones
all make. About fifteen to twenty minutes.

| Format | File | Use it for |
| --- | --- | --- |
| PowerPoint | `robot-design/chassis-designs.pptx` | Presenting. Opens in PowerPoint, Keynote or Google Slides. Every diagram is editable shapes, not a picture. |
| Web page | [in the browser](chassis-designs-slides.html) | Reading on a laptop or phone. Arrow keys to move; prints one slide per page. |

Both come from the same content. If you change one, regenerate the other —
`python3 tools/make-design-pptx.py` rebuilds the PowerPoint.

The point is not to copy one design. It is that every one on that list was
somebody's best idea, and the newer ones are better because they collected the
good bits from the older ones. That is exactly what the ITERATE criterion
rewards, so the discussion doubles as judging practice.

The criteria the deck argues for are written up as a decision table in
[`chassis.md`](chassis.md) — fill that in as the team decides.

## What Robot Design judging actually rewards

Judges are not scoring "is the robot impressive." They score, roughly:

- **Identify** — did you understand the mission problems before building?
- **Design** — is the build deliberate, and can you explain the choices?
- **Build** — is it durable, and did you test it?
- **Program** — is the code structured and understandable?
- **Iterate** — **can you show what failed and how you improved it?**

That last one carries enormous weight and is the easiest to lose by not writing
things down. A robot that got worse and then better, documented, beats a robot
that was fine from the start with no record.

Keep [`design-log.md`](design-log.md) current. It's the whole answer to "iterate."

## Design principles

1. **Durable beats clever.** If it falls off in a match it scores zero.
2. **Fast swaps.** Attachments should mount in one motion.
3. **Repeatable.** Same starting position, same result, every time.
4. **Explainable.** Every student should be able to describe any subsystem.
5. **Symmetric where possible.** Uneven weight makes the robot curve.

## Photo checklist for judging

- [ ] Robot from front, side, top
- [ ] Each attachment, mounted and detached
- [ ] Close-ups of anything unusual we want to talk about
- [ ] "Before and after" pairs of things we redesigned

--8<-- "includes/abbreviations.md"
