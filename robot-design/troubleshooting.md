# Robot Troubleshooting

Symptom first, because that is how problems arrive. Find the row that matches what
you are seeing.

The single most useful habit: when something changes, **change one thing at a
time**. The coach guide says it outright, and it is the difference between fixing a
problem and collecting three new ones.

## "It worked last week and now it doesn't"

Almost always one of these four, in this order of likelihood.

### 1. Battery charge

**This is the most common cause and the easiest to miss.** A SPIKE Prime hub at 40%
drives measurably shorter and slower than the same hub at 100%. Every timed move and
every degree-based move quietly changes length as the battery drains, so a run tuned
on a full battery drifts short by the afternoon.

What to do:

- Charge to full before every practice session, not just before matches
- Check the hub's battery indicator *before* blaming the program
- If a run is inconsistent between attempts, note the battery level next to each
  attempt in the run log. The pattern usually appears within five runs.
- Prefer gyro-based turns and sensor-based stops over timed moves, because they are
  much less sensitive to voltage

### 2. Ambient light changed

Colour and reflected-light readings depend on the light in the room. A threshold
measured at your kitchen table under a lamp will be wrong in a gym with skylights,
and wrong again under stage lighting at an event.

[`chassis.md`](../robot-design/chassis.md) has you record white, black and the
midpoint threshold. Those numbers are **not** portable between venues.

What to do:

- Re-measure white, black and the threshold **at the venue**, before your first
  match. Add it to the tournament-day routine.
- Write a tiny program that just displays the sensor reading, so measuring takes
  thirty seconds rather than a code change
- Keep the sensor at a consistent height. A millimetre of ride height changes the
  reading more than most people expect.
- Avoid thresholds that sit close to the midpoint of a narrow range; if white reads
  85 and black reads 70, that run is fragile anywhere

### 3. The gyro drifted or was zeroed while moving

The gyro accumulates error over a long run, and it takes a bad zero if it is reset
while the robot is moving — even slightly. Every turn afterwards is then wrong by
the same offset, which looks like a mysterious, consistent bias.

What to do:

- Call `reset_gyro` at the **start of every program**, with the robot already still
  in the launch area
- Let it settle a moment before launching. Do not reset and immediately drive.
- Do not carry the robot while a program is initialising
- Square up against a wall or a line partway through a long run, which resets
  accumulated position error rather than relying on the gyro all the way

### 4. Something moved that you did not think was part of the program

An attachment motor turned by hand has a different zero than it did last week.
Mission models drift out of position. The mat develops a wrinkle. Tyres pick up
dust and grip differently.

What to do:

- Re-seat every mission model and check the Dual Lock before each session
- Return attachment motors to a known position at the start of each program rather
  than assuming where they are
- Wipe the tyres and the mat

## Symptom table

| Symptom | Likely cause | What to check |
| --- | --- | --- |
| Curves consistently to one side | Motor power mismatch, or no gyro correction | Put gyro correction inside `drive_straight` rather than matching powers by hand |
| Drives a different distance each time | Battery level; wheel slip; dusty tyres | Charge to full, wipe tyres, prefer sensor stops to timed moves |
| Turns overshoot | Turning too fast — the gyro reads right but momentum carries the robot past | Slow the last few degrees of the turn |
| Turns are consistently off by the same amount | Bad gyro zero | Reset the gyro with the robot stationary in the launch area |
| Line following works at home, fails at the venue | Ambient light | Re-measure the threshold at the venue |
| Works on the floor, fails on the table | Different surface friction, and table flex | Practise on a table. Matches are on tables. |
| Attachment misses by a few millimetres | Robot start position, or accumulated drift | Add an alignment jig for launching, and square up mid-run |
| Motor stops mid-move | Stall, or thermal cut-out from repeated stalling | Reduce load or speed; let it cool; check nothing is jammed |
| Attachment falls off during a run | Not enough pins, or a single-point mount | Two mounting points minimum. If it falls off it scores zero. |
| Robot completes the mission but scores nothing | **No Equipment Constraint** on that mission | Nothing may be touching the model at the end. Applies to M01, M04, M05, M07, M09, M10, M12, M15. |

## Hub will not connect

Work through these in order:

1. **Restart the hub.** Hold the centre button until it powers down, then on again.
2. **Try USB instead of Bluetooth.** Cable is more reliable and rules out pairing.
3. **Check the cable.** Charge-only cables exist and look identical to data cables.
4. **Restart the SPIKE app**, then the laptop.
5. **Clear the Bluetooth pairing** on the laptop and pair again.
6. **Check the firmware.** A hub on older firmware than the app expects will
   connect intermittently or not at all.
7. **One laptop at a time.** A hub paired to two laptops will fight over the
   connection.

## A trap worth knowing about in advance

From the coach guide, page 11:

> "After a program is downloaded on to the controller, it cannot be transferred
> back to be opened and edited."

**The hub is not a backup.** If the only copy of a program is on the hub, it is
gone the moment the hub is wiped or the firmware updated. Export every program to
`code/spike-projects/` and commit it, and keep a copy on a USB stick or in the team
Drive as the coach guide also recommends.

## Before you conclude the robot is broken

Check in this order, because each is faster than the last to rule out:

- [ ] Battery charged to full
- [ ] Correct program selected, and in the right slot
- [ ] Gyro reset with the robot stationary
- [ ] Mission models re-seated and Dual Lock engaged
- [ ] Mat flat, no wrinkles
- [ ] Robot in the correct start position, aligned the same way as last time
- [ ] Attachment mounted the right way round and at its zero position
- [ ] Nothing left touching a model from the previous run

Most "broken robot" reports are one of those eight.

## Record what you find

Every fix belongs in [`design-log.md`](../robot-design/design-log.md) with the
problem, the change and the result. That log is the direct evidence for the
**Iterate** criterion on the Robot Design rubric, and "what broke and how did you
fix it?" is a question judges ask almost every time.

A failure you diagnosed and fixed is worth more in the judging room than a robot
that never went wrong.

--8<-- "includes/abbreviations.md"
