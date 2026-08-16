# Chassis

The driving base. Everything else bolts onto this, so it gets fixed first and
changed last.

**One base, many attachments.** The base should stop changing as early as
possible. Every change to it re-breaks every attachment and every program built
on top, so the goal is to get it reliable once and then only ever build
attachments. The slide deck that walks the team through this is
[six chassis designs](chassis-designs-slides.html).

## What we are aiming for

Criteria before choices — decide against these, then fill in the table below.
Drawn from six community designs and a coach with ten seasons behind them.

| Aim | Why it matters |
| --- | --- |
| **Box frame** | Push it flat to the wall and it can only sit square. A free, perfect start position every run, with no code. Also lets you line an edge on a black line and press go. |
| **Wheels supported on both sides** | Motor on one side, frame on the other. A heavy attachment presses down and bends unsupported wheels slightly inward, and the robot stops driving straight. |
| **Weight low** | Weight up high rocks on starting, stopping and turning. Rocking lifts load off a wheel, and an unloaded wheel spins instead of driving. Recess the hub. |
| **Weight even, front to back** | All the mass at one end makes turns stop repeating. |
| **Four wheels with rubber tyres** | Not a ball-bearing castor. Four driven wheels track straighter. |
| **62.4 mm wheels** | Bigger diameter drives faster, and grip is far better than the blue SPIKE wheels. The coach's team switched and the slipping on turns stopped. |
| **Two attachment points** | Top and front. One build can then do two jobs. |
| **Gravity mounting** | Guide pegs align the attachment, gravity holds it, nothing clamps. Under a second to fit or remove. |

Note on wheels: of the six designs surveyed, the three that list wheel slipping
as a fault all run blue SPIKE wheels, and the three that require 62.4 mm wheels
list no slipping at all. Six for six. Confirm the 62.4 mm wheels are actually in
our kit before committing to them — that is the one cost of this choice.

## Configuration

| Item | Choice | Why |
| --- | --- | --- |
| Drive type | _TODO — differential / other_ | |
| Drive motors | _TODO — ports_ | |
| Wheel size | _TODO_ | Bigger = faster, smaller = more precise |
| Wheelbase | _TODO_ | |
| Castor / third point | _TODO_ | Aim for four driven wheels instead |
| Attachment motors | _TODO — ports_ | |
| Hub position | _TODO_ | Recessed and low; affects weight balance and button access |
| Weight balance | _TODO — where does it sit front to back?_ | Even beats end-heavy |

## Sensors

One colour sensor is worth having, but it is no longer the primary way to
navigate: the black lines are getting sparser on FIRST's mats each season, so
most teams now steer on the gyro and count distance on the motor encoders, and
keep the colour sensor for the occasional line.

| Sensor | Port | Position | Used for |
| --- | --- | --- | --- |
| Gyro (built in) | — | Hub | **Primary.** Straight driving, accurate turns |
| Motor encoders | — | Drive motors | **Primary.** Exact distance and turn angles |
| Colour | _TODO_ | _TODO_ | Line following / squaring, when there is a line |
| Colour | _TODO_ | _TODO_ | |
| Distance | _TODO_ | _TODO_ | |

## Calibration

Numbers other programs depend on. **Re-measure after any chassis change** — if the
wheels change, every distance in every program is wrong.

| Value | Measured | Date | How we measured it |
| --- | --- | --- | --- |
| Wheel circumference | _TODO_ cm | | |
| Motor degrees per cm | _TODO_ | | |
| Motor degrees per 90° turn | _TODO_ | | Only if not using gyro |
| Reflected light: white | _TODO_ | | On the mat. **Re-measure at the venue** — see [troubleshooting](troubleshooting.md) |
| Reflected light: black | _TODO_ | | |
| Line threshold (midpoint) | _TODO_ | | |

## Attachment mounting system

How attachments connect. A consistent system means any attachment fits any time.

Aim for the gravity technique: a couple of small pegs that guide the attachment
into position without clamping it, so its own weight does the holding. If it has
to be forced or pinned, it is too slow for a match and it will be got wrong under
pressure.

_TODO — describe our mount once built: peg positions, axle alignment, motor coupling_

**Swap time:** _TODO_ s (target: under 10, and the gravity technique should get
this to about 1)

## Photos

_TODO — add photos here_
