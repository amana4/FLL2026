# Library — shared Python movement code

`toolkit.py` (in this folder) holds the drive, turn, and attachment functions
every 2026 mission program builds on: `init_robot`, `drive_cm`,
`drive_cm_gyro`, `turn_deg`, `turn_deg_gyro`, `arc_turn`,
`run_attachment_deg`, plus wheel-diameter calibration helpers.

Ported from last season's `Library/toolKit.py` — see `code/2025-reference/`
(not published to this site) for where it came from and what changed.

## Before trusting any of it on the 2026 robot

The robot configuration block at the top of `toolkit.py` — port assignments,
wheel diameter, track width — is **last year's robot**, carried over as a
starting point:

| Setting | Value in the file | |
| --- | --- | --- |
| Drive motors | Ports A (left), E (right) | _TODO — confirm or update_ |
| Color sensors | Ports F (left), B (right) | _TODO_ |
| Attachment motors | Ports C, D | _TODO_ |
| Wheel diameter | 88.0 mm | _TODO — measure this year's wheels_ |
| Track width | 143.0 mm | _TODO — measure this year's chassis_ |

Update these once the 2026 driving base is built (see
[`robot-design/chassis.md`](../../robot-design/chassis.md)), and use
`calibrate_wheel_diameter()` to correct for any remaining drift between
commanded and actual distance.

## Tuning notes carried over from last season

The comment above `drive_cm_gyro` lists three speed/kp/steer-limit
combinations that worked on last year's robot. They won't transfer exactly —
weight and wheel grip changed — but they're a sane starting point for tuning
rather than guessing from zero.

## Deployment note

This file is meant to be imported (`from library.toolkit import ...`) while
editing mission code here in git. The SPIKE App's Python canvas does not
support that import at upload time — see
[`code/missions/README.md`](../missions/README.md) for the paste-it-in-manually
step this currently requires.
