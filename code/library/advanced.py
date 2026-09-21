# Advanced library – Python port of the word-blocks library (SPIKE App 3.5)
#
# This is a port of Advanced-Coding-26.llsp3, the team's Word Blocks library,
# last saved 2 August 2026. Fourteen My Blocks, carried across to Python.
#
# It sits NEXT TO code/library/toolkit.py. It does not replace it. Missions that
# already inline the toolkit keep working. Reach for this file when you want the
# ramped drives, the PID turns, or the line blocks.
#
# THE FUNCTION NAMES ARE toolkit.py's NAMES. Same names, same meaning, same
# order of arguments for the ones that matter. A mission written against the
# toolkit reads the same against this file. What changes is what happens
# underneath: every drive here ramps up and down, and every turn here uses the
# gyro.
#
# Block                              Function here
# ---------------------------------  -------------------------------------
# .Forward (Mm)                      drive_cm(cm)          positive cm
# .Backward (mm)                     drive_cm(-cm)         negative cm
# zEnd Speed / zBackwards Acc        _drive_ramp_cm(...)   (one function)
# .Left (PID) / .Right (PID)         turn_deg_gyro(-deg) / turn_deg_gyro(deg)
# Left (simple) / Right (simple)     turn_deg(-deg) / turn_deg(deg)
# Gyro Backwards (degrees) basic     gyro_backward_deg(speed_pct, degrees)
# Line Square                        line_square()             HUB ONLY
# Line Follow                        line_follow(side, secs)   HUB ONLY
# zFind Line / zAcquire Line /       _find_line / _acquire_line /
#   zFollowing a line                  _follow_line
#
# There are also aliases named after the palette — forward, backward, left_pid,
# right_pid, left_simple, right_simple, gyro_backwards — at the bottom of the
# file. Same functions. They exist for reading the SPIKE App and this side by
# side, not for mission code.
#
# Two toolkit functions behave differently here, and both are improvements:
#   drive_cm      holds a heading with the gyro. The toolkit's does not.
#   turn_deg_gyro works. The toolkit's never moves the motors, see
#                 code/learn/10-gyro.md:241-274.
#
# Some of the toolkit's tuning arguments do not exist here, because they
# describe a control loop this file does not have: steer_limit, deadband_deg,
# steer_rate_limit, min_steer_kick, acceleration and deceleration. Passing one
# raises a TypeError rather than being quietly ignored. The ramp does the job
# acceleration and deceleration used to.
#
# Units: the blocks work in millimetres and speed percent. This file works in
# centimetres and deg/s, so it matches toolkit.py. Speeds given as a percent in
# the blocks go through _pct_to_deg_s() once.
#
# Eight things the blocks got wrong, fixed here. Each is noted again at the
# function that had it, so the blocks and this file can be reconciled later.
#
#   1. The blocks use 3.146 for pi. That is 0.14 percent long. This file uses
#      math.pi, so measured distances shift very slightly. Re-measure the wheel
#      calibration after switching.
#   2. zEnd Speed phase 1 sets "Gyro last error.." to 0 inside the loop, so its
#      D term collapsed into extra P gain. zBackwards Acc did not do this.
#   3. The D term flipped sign between phase 1 and phases 2 and 3. One form is
#      used in all three phases here.
#   4. zEnd Speed counted motor B, zBackwards Acc counted motor A. That was not
#      arbitrary: the two encoders are mirrored, so each one counts up in one
#      direction only. This file averages abs() of both, the way
#      toolkit.py:202-205 already does, and works in either direction.
#   5. Gyro Backwards basic never zeroed its last-error variable, so its first
#      step used whatever the previously run block left behind.
#   6. .Right (PID) stopped about a degree early and .Left (PID) did not. Both
#      now take stop_early_deg, defaulting to 0.
#   7. The PID turns never clamped Output or guarded the integral against
#      windup. Both are clamped here.
#   8. Every "wait until" in the line blocks was unbounded. A missed line hung
#      the robot for the rest of the match. Everything here has a timeout.
#
# Wiring below is copied from toolkit.py, which claims ports A and B were
# confirmed on 13 September 2026. On 20 September 2026 the hub disagreed:
# init_robot raised OSError: [Errno 19] ENODEV, meaning no motor on A or B.
# code/missions/M03-flip-the-rock/mission.py:17-18 says F and A instead.
# Run scan_ports() on the hub and set LEFT_DRIVE and RIGHT_DRIVE from what it
# prints. Wheel diameter and track width are NOT confirmed either.

from hub import port, motion_sensor
import runloop
import motor_pair
import motor
from math import pi

# The colour sensor is not in the pretend hub used by the lesson pages, so
# importing it has to be allowed to fail. See tools/spike-shim.py, which
# registers runloop, motor, motor_pair and hub but no color_sensor.
try:
    import color_sensor
    _HAS_COLOUR = True
except ImportError:
    _HAS_COLOUR = False

# -----------------------------
# Robot configuration
# -----------------------------
PAIR = motor_pair.PAIR_1

# Main drive motors. Reference wiring, from
# code/missions/M03-flip-the-rock/mission.py:17-18, confirmed on the hub on
# 20 September 2026 when A and B raised ENODEV.
LEFT_DRIVE = port.F
RIGHT_DRIVE = port.A

# Downward colour sensors. NOT CONFIRMED, and right_color cannot be correct:
# port F now holds the left drive motor, so it cannot also hold a sensor. The
# line functions check this and tell you to run scan_ports().
left_color = port.E
right_color = port.F

# Attachment motors
attachment1 = port.C           # left attachment
attachment2 = port.D           # right attachment, NOT CONFIRMED

# Wheel and robot dimensions
WHEEL_D_MM = 62.4              # the blocks agree: WheelDia = 62.4
TRACK_W_MM = 130.0
ACCEL = 1000                   # deg/s^2, matches the blocks' 1000 1000
DECEL = 1000

# Calibration multiplier for effective wheel diameter. 1.0 = no change.
CALIBRATION_SCALE = 1.0

# Enable debug prints (set False to silence)
DEBUG = False

# -----------------------------
# Which way does the gyro count?
# -----------------------------
# -1 means the gyro reads more positive as the robot turns ANTICLOCKWISE.
#
# SETTLED ON THE HUB, 20 September 2026. It used to be +1, which is what
# Advanced-Coding-26.llsp3 and Gyro-Drive-Straight both assume. On the robot
# that made the heading loop push the wrong way, so a drive_cm(-44) spun on the
# spot instead of driving. The debug trace showed yaw falling straight through
# 180 and wrapping, which is what positive feedback looks like.
#
# So the two Word Blocks programs have the sign wrong, and toolkit.py:223 and
# tools/spike-shim.py:193 had it right all along.
#
# Every correction in this file is written in terms of this, so this line is the
# whole setting. bench_check_yaw_sign() re-measures it after any rebuild.
YAW_SIGN = -1

# -----------------------------
# Tuning, carried over from the blocks
# -----------------------------
# Straight driving, from zEnd Speed and zBackwards Acc.
KP_STRAIGHT = 1.8
KD_STRAIGHT = 0.5

# Gyro Backwards basic used its own, slightly softer pair.
KP_BACK = 1.5
KD_BACK = 1.0

# The PID turns. Kp is passed in by the caller; the main block program used 0.7.
KP_TURN = 0.7
KI_TURN = 0.001
KD_TURN = 0.1

# Stop compensation, in cm. The blocks called this StopComp and subtracted it
# from the target so the robot's coast landed on the mark.
STOP_COMP_FWD_CM = 1.4         # blocks: 14 mm
STOP_COMP_REV_CM = 1.5         # blocks: 15 mm

# .Forward and .Backward picked these for you.
RAMP_FRACTION = 4.0            # ramp = distance / 4
RAMP_MIN_CM = 3.0              # blocks: 30 mm
RAMP_MAX_CM = 10.0             # blocks: 100 mm
TOP_SPEED_PCT = 60
TOP_SPEED_SHORT_PCT = 30       # used under SHORT_RUN_CM
SHORT_RUN_CM = 30.0            # blocks: 300 mm
START_SPEED_PCT = 25

# The mat is 200 cm by 114 cm. A single straight drive cannot be longer than
# that, so anything bigger is almost always millimetres typed in by mistake.
MAX_SENSIBLE_CM = 200.0

# Line thresholds. The blocks had these as bare numbers in six places.
LINE_DARK = 15                 # zFind Line: dark enough to be on the line
LINE_ACQUIRE = 50              # zAcquire Line: light enough to have swung off
LINE_TARGET = 45               # zFollowing a line: the edge it holds
LINE_KP = 2.0
LINE_SPEED_PCT = 30
SQUARE_DARK = 20               # Line Square, coarse pass
SQUARE_LIGHT = 55              # Line Square, fine pass

# 100 percent in the Word Blocks is full motor speed. Confirm this against the
# motors actually on the drive base; a large motor is nearer 1050 than 1110.
MAX_DEG_S = 1050

# Default speeds, in deg/s, so the arguments read the same as toolkit.py.
# The numbers come from the blocks: 15 percent for a quick turn, 60 percent for
# the PID turn's ceiling. The toolkit's defaults of 400 and 250 are not used,
# because overshoot_deg below was tuned against 15 percent and nothing else.
TURN_SIMPLE_DEG_S = int(15 * MAX_DEG_S / 100)      # 157
TURN_PID_MAX_DEG_S = int(60 * MAX_DEG_S / 100)     # 630

# How long any loop is allowed to run before it gives up, in milliseconds.
DEFAULT_TIMEOUT_MS = 8000
LOOP_MS = 15

# How far off straight a "straight" drive is allowed to get before it gives up.
#
# A drive that is meant to hold a heading should never be tens of degrees off.
# If it is, the loop is pushing the wrong way and the robot is spinning, not
# driving. That happened on 20 September 2026 with YAW_SIGN set the wrong way.
# Without this guard the robot spun until the distance counter filled up, which
# took it right off the table.
RUNAWAY_DEG = 45.0

# Cruise speed for drive_cm, in deg/s. None means "work it out per move", the
# way the .Forward block did. init_robot(default_speed=...) sets it.
DEFAULT_DRIVE_DEG_S = None

# Which bearing the gyro's current zero stands for, in degrees from base.
# Maintained by _reset_yaw and read by bearing(). init_robot() sets it to 0,
# which is what makes base "zero" for the whole run.
_HEADING_BASE = 0.0

# What the last drive actually aimed for, in cm, and how much coast allowance it
# gave away to get there. For debug logs in mission code. See
# code/missions/M02-exploding-seeds/mission-advanced.py.
_LAST_DRIVE_TARGET_CM = 0.0
_LAST_DRIVE_COMP_CM = 0.0

# -----------------------------
# Geometry helpers
# -----------------------------
# These are the same helpers as toolkit.py:51-73 and toolkit.py:152-154. They
# are copied rather than imported because the SPIKE App's Python canvas cannot
# import, so this file has to stand alone. See code/library/README.md.


def _cm_to_deg(cm):
    """Convert straight-line distance (cm) to motor shaft degrees."""
    effective_wheel_d = WHEEL_D_MM * CALIBRATION_SCALE
    circ_mm = pi * effective_wheel_d
    rotations = (abs(cm) * 10.0) / circ_mm
    return int(round(rotations * 360.0))


def _deg_to_cm(deg):
    """Motor shaft degrees back to distance in cm. The inverse of _cm_to_deg.

    Do NOT do this by dividing by _cm_to_deg(1). That rounds to a whole number of
    degrees, which on these wheels is 18 instead of 18.47, and every distance you
    report comes out 2.6 percent long.
    """
    effective_wheel_d = WHEEL_D_MM * CALIBRATION_SCALE
    circ_mm = pi * effective_wheel_d
    return (abs(deg) / 360.0) * circ_mm / 10.0


def _robot_deg_to_wheel_deg(robot_deg):
    """Convert a robot in-place rotation (degrees) to wheel shaft degrees."""
    turn_circ_mm = pi * TRACK_W_MM
    travel_mm = (abs(robot_deg) / 360.0) * turn_circ_mm
    effective_wheel_d = WHEEL_D_MM * CALIBRATION_SCALE
    wheel_rot = travel_mm / (pi * effective_wheel_d)
    return int(round(wheel_rot * 360.0))


def _yaw_deg():
    """Raw gyro yaw, in degrees. The sensor reports tenths."""
    y_decideg, _, _ = motion_sensor.tilt_angles()
    return y_decideg / 10.0


def _yaw_cw():
    """Yaw in degrees, counting up clockwise, whatever the hub does.

    Everything in this file steers off this, not off _yaw_deg(). That is what
    makes YAW_SIGN a one-line change.
    """
    return YAW_SIGN * _yaw_deg()


def _reset_yaw(deg=0):
    """Zero the gyro, and remember which bearing that zero now stands for.

    Several moves zero the gyro so they can hold "straight" as zero. That throws
    away where the robot is pointing relative to base, which is what face()
    needs. So this keeps a running total: _HEADING_BASE is the bearing the
    gyro's current zero represents, and bearing() adds the two back together.
    """
    global _HEADING_BASE
    _HEADING_BASE = _HEADING_BASE + _yaw_cw() - deg
    motion_sensor.reset_yaw(int(deg * 10))


def bearing():
    """Which way the robot is pointing, in degrees from base.

    Base is however you set the robot down when init_robot() ran. It does not
    move for the rest of the run, no matter how many times a move zeroes the
    gyro. Clockwise is positive, and it keeps counting past 360 rather than
    wrapping, so a robot that has turned right four times reads about 360.
    """
    return _HEADING_BASE + _yaw_cw()


def _wrap180(a):
    """Wrap any angle into -180 to 180."""
    return (a + 180.0) % 360.0 - 180.0


def _clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value


def _pct_to_deg_s(pct):
    """Word Blocks speed percent to deg/s.

    The blocks talk in -100 to 100. The SPIKE Python API and toolkit.py talk in
    deg/s. The pretend hub does not clamp velocity, so this does.
    """
    return int(round(_clamp(pct, -100.0, 100.0) * MAX_DEG_S / 100.0))


def _deg_s_to_pct(deg_s):
    """deg/s back to Word Blocks speed percent.

    The other direction. Arguments named `velocity` arrive in deg/s, because
    that is what toolkit.py and the real SPIKE API use, but the ramp and the
    turns were tuned in percent.
    """
    return _clamp(float(deg_s) * 100.0 / MAX_DEG_S, -100.0, 100.0)


def _drive_degrees():
    """How far the drive wheels have turned since the last reset, in degrees.

    abs() on both, then averaged. The two encoders are mirrored, so one counts
    up going forward and the other counts up going back. That is why the blocks
    used motor B for the forward ramp and motor A for the reverse one. Taking
    the size of both instead works in either direction, and does not care which
    motor is mounted which way round.
    """
    left = abs(motor.relative_position(LEFT_DRIVE))
    right = abs(motor.relative_position(RIGHT_DRIVE))
    return (left + right) // 2


# -----------------------------
# The tank primitive
# -----------------------------
def _tank(left_deg_s, right_deg_s):
    """Drive the two wheels at independent speeds.

    This is the blocks' "start moving  left=A  right=B", which every block in
    the library uses and toolkit.py has no equivalent for.

    It cannot be two motor.run() calls. On a paired base those fight each other,
    and the pretend hub models a single paired motor as steering plus or minus
    50 (tools/spike-shim.py:490-493). So the wheel speeds are turned back into
    the steering-and-velocity pair that motor_pair.move() wants, by inverting
    the LEGO steering curve at tools/spike-shim.py:165-180:

        steering >= 0:  left = v,               right = v * (1 - s / 50)
        steering <  0:  left = v * (1 + s / 50), right = v

    Whichever wheel is turning faster becomes the velocity, and the other one
    sets the steering. Exact both here and on the hub.
    """
    left = float(left_deg_s)
    right = float(right_deg_s)

    if left == 0.0 and right == 0.0:
        motor_pair.move(PAIR, 0, velocity=0)
        return

    # A big correction on top of a fast base speed can ask for more than the
    # motor has. Scale both wheels down together rather than clipping one, so
    # the robot keeps steering the way it meant to and just does it slower.
    fastest = max(abs(left), abs(right))
    if fastest > MAX_DEG_S:
        scale = MAX_DEG_S / fastest
        left *= scale
        right *= scale

    if abs(left) >= abs(right):
        velocity = left
        steering = 50.0 * (1.0 - right / left)
    else:
        velocity = right
        steering = 50.0 * (left / right - 1.0)

    motor_pair.move(PAIR, int(round(_clamp(steering, -100.0, 100.0))),
                    velocity=int(round(velocity)))


# -----------------------------
# What is actually plugged in?
# -----------------------------
ALL_PORTS = (("A", port.A), ("B", port.B), ("C", port.C),
             ("D", port.D), ("E", port.E), ("F", port.F))


def port_label(which_port):
    """Turn a port object back into its letter, for readable messages."""
    for name, candidate in ALL_PORTS:
        if candidate is which_port:
            return name
    return "?"


def _has_motor(which_port):
    """True if there is a motor on this port. Asking is the only way to know."""
    try:
        motor.relative_position(which_port)
        return True
    except Exception:
        return False


def _has_colour(which_port):
    if not _HAS_COLOUR:
        return False
    try:
        color_sensor.reflection(which_port)
        return True
    except Exception:
        return False


def scan_ports():
    """Print what is plugged into each port. Run this first, on the hub.

    OSError: [Errno 19] ENODEV out of init_robot means LEFT_DRIVE or RIGHT_DRIVE
    names a port with nothing on it. This says which ports do have something,
    so you can fix the two lines at the top of this file.
    """
    motors = []
    sensors = []
    for name, which_port in ALL_PORTS:
        if _has_motor(which_port):
            kind = "motor"
            motors.append(name)
        elif _has_colour(which_port):
            kind = "colour sensor"
            sensors.append(name)
        else:
            kind = "empty"
        print("port", name, "-", kind)

    print("")
    print("motors on:", ", ".join(motors) if motors else "none")
    print("colour sensors on:", ", ".join(sensors) if sensors else "none")
    print("")
    print("this file expects LEFT_DRIVE = A and RIGHT_DRIVE = B")
    print("and left_color = E, right_color = F")

    for label, wanted in (("LEFT_DRIVE", LEFT_DRIVE), ("RIGHT_DRIVE", RIGHT_DRIVE)):
        if not _has_motor(wanted):
            print("=> nothing on the", label, "port. Change it at the top.")
    return motors, sensors


# -----------------------------
# Init
# -----------------------------
async def reset_yaw():
    """Zero the gyro and both drive encoders, then let the gyro settle.

    Same name and same job as toolkit.py:108. This also declares "here is base":
    bearing() reads 0 afterwards, and face() measures from this direction for the
    rest of the run.
    """
    global _HEADING_BASE
    motion_sensor.reset_yaw(0)
    _HEADING_BASE = 0.0
    motor.reset_relative_position(LEFT_DRIVE, 0)
    motor.reset_relative_position(RIGHT_DRIVE, 0)
    await runloop.sleep_ms(500)


async def init_robot(default_speed=None):
    """Pair the drive motors and zero everything. Call this once, first.

    Same name as toolkit.py:114. `default_speed` is in deg/s and is the cruise
    speed drive_cm uses when it is not given one.

    Leave it out and drive_cm picks the speed itself, the way .Forward did: 60
    percent, or 30 percent for anything under 30 cm. That is usually what you
    want. Pass a number to force one speed for the whole run, which is how the
    toolkit behaves.
    """
    global DEFAULT_DRIVE_DEG_S
    DEFAULT_DRIVE_DEG_S = None if default_speed is None else int(default_speed)

    # Check before pairing. motor_pair.pair() on an empty port raises
    # OSError: [Errno 19] ENODEV, which says nothing about which port is wrong.
    missing = []
    if not _has_motor(LEFT_DRIVE):
        missing.append("LEFT_DRIVE")
    if not _has_motor(RIGHT_DRIVE):
        missing.append("RIGHT_DRIVE")
    if missing:
        raise RuntimeError(
            "No motor on the %s port. Run scan_ports() to see what is plugged "
            "in, then fix LEFT_DRIVE and RIGHT_DRIVE at the top of this file."
            % " or ".join(missing)
        )

    motor_pair.pair(PAIR, LEFT_DRIVE, RIGHT_DRIVE)
    await reset_yaw()


async def _settle():
    """The blocks' "wait 0.3 seconds" before zeroing the gyro.

    The hub's gyro drifts for a moment after the motors stop. Zeroing it while
    it is still settling bakes that error into the whole next move.
    """
    await runloop.sleep_ms(300)


def set_calibration_scale(scale):
    """Set the calibration scale directly. Must be above 0. Returns the scale."""
    global CALIBRATION_SCALE
    value = float(scale)
    if value > 0:
        CALIBRATION_SCALE = value
    return CALIBRATION_SCALE


def calibrate_wheel_diameter(commanded_cm, measured_cm):
    """Set the scale from one measured run. Returns the new scale."""
    global CALIBRATION_SCALE
    if commanded_cm == 0:
        return CALIBRATION_SCALE
    CALIBRATION_SCALE = float(measured_cm) / float(commanded_cm)
    return CALIBRATION_SCALE


# -----------------------------
# Straight driving, with a ramp
# -----------------------------
async def _drive_ramp_cm(cm,
                         top_pct=TOP_SPEED_PCT,
                         start_pct=START_SPEED_PCT,
                         ramp_cm=RAMP_MIN_CM,
                         stop_comp_cm=None,
                         kp=KP_STRAIGHT,
                         kd=KD_STRAIGHT,
                         stop_mode=motor.BRAKE,
                         timeout_ms=DEFAULT_TIMEOUT_MS):
    """Drive straight with a trapezoid speed profile, held straight by the gyro.

    Positive cm is forward, negative is backward. This is zEnd Speed and
    zBackwards Acc merged: they were the same three phases with the signs
    flipped, so keeping them apart only let them drift apart.

    Three phases, exactly as the blocks had them:
      1. ramp from start_pct up to top_pct over the first ramp_cm
      2. hold top_pct until ramp_cm is left
      3. ramp back down to start_pct over the last ramp_cm

    Fixes 1 to 4 in the header live here. math.pi instead of 3.146; the D term
    keeps its memory in every phase; the D term keeps one sign in every phase;
    both encoders are counted instead of one.
    """
    if cm == 0:
        return

    direction = 1.0 if cm > 0 else -1.0
    if stop_comp_cm is None:
        stop_comp_cm = STOP_COMP_FWD_CM if cm > 0 else STOP_COMP_REV_CM
        # The blocks subtracted a flat 14 or 15 mm, which is right at their 60
        # percent cruise and wrong everywhere else. Coasting distance goes with
        # speed, so scale it. Without this a 1.5 cm nudge loses almost all of
        # itself, and anything under 1.4 cm does not move at all.
        stop_comp_cm *= top_pct / float(TOP_SPEED_PCT)
        # And never give away more than a quarter of a short move.
        stop_comp_cm = min(stop_comp_cm, abs(cm) * 0.25)

    target_cm = abs(cm) - stop_comp_cm
    if target_cm <= 0:
        return

    # Record what this move actually aimed for, so a mission's debug log can
    # compare the wheels against the real target instead of guessing at the
    # coast allowance and reporting a gap that is not a fault.
    global _LAST_DRIVE_TARGET_CM, _LAST_DRIVE_COMP_CM
    _LAST_DRIVE_TARGET_CM = target_cm
    _LAST_DRIVE_COMP_CM = stop_comp_cm

    dist_deg = _cm_to_deg(target_cm)
    ramp_deg = _cm_to_deg(abs(ramp_cm))
    if ramp_deg < 1:
        ramp_deg = 1
    # Two ramps cannot be longer than the whole move.
    if ramp_deg * 2 > dist_deg:
        ramp_deg = max(1, dist_deg // 2)

    motor.reset_relative_position(LEFT_DRIVE, 0)
    motor.reset_relative_position(RIGHT_DRIVE, 0)
    await _settle()
    _reset_yaw(0)
    await runloop.sleep_ms(100)

    last_error = 0.0
    steps = 0
    max_steps = int(timeout_ms / LOOP_MS)

    while True:
        travelled = _drive_degrees()
        if travelled >= dist_deg:
            break
        steps += 1
        if steps > max_steps:
            if DEBUG:
                print("ramp drive timed out at", travelled, "of", dist_deg)
            break

        # Which phase are we in, and how fast should the base speed be?
        if travelled < ramp_deg:
            fraction = travelled / ramp_deg
            base_pct = (top_pct - start_pct) * fraction + start_pct
        elif travelled < (dist_deg - ramp_deg):
            base_pct = top_pct
        else:
            remaining = dist_deg - travelled
            fraction = remaining / ramp_deg
            base_pct = (top_pct - start_pct) * fraction + start_pct

        error = _wrap180(_yaw_cw())
        correction = -(kp * error + kd * (error - last_error))
        last_error = error

        if abs(error) > RUNAWAY_DEG:
            motor_pair.stop(PAIR, stop=motor.BRAKE)
            raise RuntimeError(
                "Straight drive is %.0f degrees off course, so it stopped. The "
                "heading loop is pushing the wrong way. Either YAW_SIGN is "
                "wrong, or LEFT_DRIVE and RIGHT_DRIVE are swapped. Run "
                "bench_check_yaw_sign() and watch which way the robot turns."
                % error
            )

        base = direction * _pct_to_deg_s(base_pct)
        trim = _pct_to_deg_s(correction)
        _tank(base + trim, base - trim)

        if DEBUG:
            print("deg:", travelled, "of", dist_deg,
                  "base%:", round(base_pct, 1),
                  "yaw:", round(error, 2))

        await runloop.sleep_ms(LOOP_MS)

    motor_pair.stop(PAIR, stop=stop_mode)
    await runloop.sleep_ms(200)


def _auto_ramp_cm(cm):
    """The ramp length .Forward and .Backward worked out for you."""
    ramp = abs(cm) / RAMP_FRACTION
    return _clamp(ramp, RAMP_MIN_CM, RAMP_MAX_CM)


def _auto_top_pct(cm):
    """The top speed .Forward and .Backward worked out for you."""
    if abs(cm) < SHORT_RUN_CM:
        return TOP_SPEED_SHORT_PCT
    return TOP_SPEED_PCT


def _check_sensible(cm):
    """Catch millimetres typed into a centimetres argument.

    The blocks take mm, this file takes cm, and ".Forward 300" copied straight
    across becomes three metres. The mat is only two metres wide, so a straight
    drive longer than that is a mistake every time.
    """
    if abs(cm) > MAX_SENSIBLE_CM:
        raise ValueError(
            "%g cm is longer than the mat. The Word Blocks take millimetres "
            "and this takes centimetres, so .Forward 300 is drive_cm(30)."
            % cm
        )


async def drive_cm(cm,
                   velocity=None,
                   stop_mode=motor.BRAKE,
                   start_velocity=None,
                   ramp_cm=None,
                   kp=KP_STRAIGHT,
                   kd=KD_STRAIGHT):
    """Drive straight, ramping up and down, holding the heading with the gyro.

    Same name as toolkit.py:126. Positive cm is forward, negative is backward,
    which is the toolkit's rule too. This is ".Forward" and ".Backward" in one
    function, because the sign already says which.

    Unlike the toolkit's drive_cm, this one corrects its heading. There is no
    separate plain version, so drive_cm_gyro below is the same function.

    velocity is deg/s, as in the toolkit. Leave it out and the speed is picked
    the way the block did: 60 percent, or 30 percent under 30 cm. Ramp length is
    a quarter of the distance, between 3 and 10 cm.

    The toolkit's acceleration and deceleration arguments are not here. The ramp
    replaces them.
    """
    _check_sensible(cm)
    if cm == 0:
        return

    distance = abs(cm)
    if velocity is None:
        velocity = DEFAULT_DRIVE_DEG_S
    if velocity is None:
        top_pct = _auto_top_pct(distance)
    else:
        top_pct = abs(_deg_s_to_pct(velocity))

    if start_velocity is None:
        start_pct = min(START_SPEED_PCT, top_pct)
    else:
        start_pct = abs(_deg_s_to_pct(start_velocity))

    if ramp_cm is None:
        ramp_cm = _auto_ramp_cm(distance)

    await _drive_ramp_cm(distance if cm > 0 else -distance,
                         top_pct=top_pct,
                         start_pct=start_pct,
                         ramp_cm=ramp_cm,
                         kp=kp,
                         kd=kd,
                         stop_mode=stop_mode)


async def drive_cm_gyro(cm, velocity=None, kp=KP_STRAIGHT, kd=KD_STRAIGHT,
                        stop_mode=motor.BRAKE, **kwargs):
    """The same function as drive_cm. Both names exist, both hold a heading.

    Same name as toolkit.py:160. In the toolkit these are two different
    functions, one with gyro correction and one without. Here there is only the
    corrected one, so the name you reach for does not change what happens.

    The toolkit's steer_limit, deadband_deg, steer_rate_limit and
    min_steer_kick are not here. They tune a steering loop this file does not
    use; it drives the two wheels at independent speeds instead.
    """
    await drive_cm(cm, velocity=velocity, kp=kp, kd=kd, stop_mode=stop_mode,
                   **kwargs)


async def gyro_backward_deg(speed_pct, degrees,
                            kp=KP_BACK,
                            kd=KD_BACK,
                            timeout_ms=DEFAULT_TIMEOUT_MS):
    """Reverse at a fixed speed for a number of MOTOR degrees, held straight.

    The blocks' "Gyro Backwards (degrees) basic". It is the odd one out in the
    library: it counts motor degrees, not distance. Kept that way so a mission
    ported from the blocks still reads the same.

    Fix 5 lives here. The block never zeroed its last-error variable, so its
    first step corrected using whatever the previous block had left in it.
    """
    target_deg = abs(degrees)
    if target_deg == 0:
        return

    motor.reset_relative_position(LEFT_DRIVE, 0)
    motor.reset_relative_position(RIGHT_DRIVE, 0)
    await _settle()
    _reset_yaw(0)

    last_error = 0.0          # fix 5: the block left this holding stale data
    steps = 0
    max_steps = int(timeout_ms / LOOP_MS)

    while _drive_degrees() < target_deg:
        steps += 1
        if steps > max_steps:
            if DEBUG:
                print("gyro_backward_deg timed out")
            break

        error = _wrap180(_yaw_cw())
        correction = -(kp * error + kd * (error - last_error))
        last_error = error

        if abs(error) > RUNAWAY_DEG:
            motor_pair.stop(PAIR, stop=motor.BRAKE)
            raise RuntimeError(
                "Reverse drive is %.0f degrees off course, so it stopped. See "
                "the note on RUNAWAY_DEG, and run bench_check_yaw_sign()."
                % error
            )

        base = -_pct_to_deg_s(abs(speed_pct))
        trim = _pct_to_deg_s(correction)
        _tank(base + trim, base - trim)

        await runloop.sleep_ms(LOOP_MS)

    motor_pair.stop(PAIR, stop=motor.BRAKE)
    await runloop.sleep_ms(200)


# -----------------------------
# Turns, PID
# -----------------------------
async def _turn_to_bearing(target,
                           velocity=TURN_PID_MAX_DEG_S,
                           kp=KP_TURN,
                           ki=KI_TURN,
                           kd=KD_TURN,
                           tolerance=1.0,
                           stop_mode=motor.BRAKE,
                           min_pct=12,
                           integral_limit=500.0,
                           settle_ms=150,
                           settle_passes=2,
                           timeout_ms=DEFAULT_TIMEOUT_MS):
    """Spin until bearing() reaches `target`. The shared loop behind both turns.

    It does not zero the gyro. It does not need to: bearing() is absolute, so the
    loop can aim at a bearing directly. That is what lets face() exist.

    After braking it waits settle_ms, reads the gyro again, and goes round once
    more if the robot coasted past. Without that the momentum after the brake is
    never corrected. On the hub that was worth about 2.4 degrees a turn, measured
    20 September 2026. The simulator has no momentum, so it could not show it.

    Fix 7 lives here. The blocks never clamped Output and never guarded Integral,
    so a stall grew the integral without limit. min_pct is new as well: below
    roughly 12 percent the motors buzz without moving, which is what the block's
    1 degree fudge was quietly working around.
    """
    max_pct = abs(_deg_s_to_pct(velocity))
    max_steps = int(timeout_ms / LOOP_MS)

    for attempt in range(1 + max(0, settle_passes)):
        previous_error = 0.0
        integral = 0.0
        steps = 0

        while True:
            error = target - bearing()
            if abs(error) < tolerance:
                break
            steps += 1
            if steps > max_steps:
                if DEBUG:
                    print("turn timed out", round(error, 2), "degrees short")
                break

            integral = _clamp(integral + error, -integral_limit, integral_limit)
            derivative = error - previous_error
            previous_error = error

            output = kp * error + ki * integral + kd * derivative
            output = _clamp(output, -max_pct, max_pct)
            # Below the stall speed the wheels buzz and do not move.
            if 0 < abs(output) < min_pct:
                output = min_pct if output > 0 else -min_pct

            power = _pct_to_deg_s(output)
            _tank(power, -power)

            if DEBUG:
                print("turn err:", round(error, 2), "out%:", round(output, 1))

            await runloop.sleep_ms(LOOP_MS)

        motor_pair.stop(PAIR, stop=stop_mode)
        await runloop.sleep_ms(settle_ms)

        # Did the robot coast past while it was braking?
        if abs(target - bearing()) < tolerance:
            break
        if DEBUG:
            print("coasted past by", round(target - bearing(), 2), "- going again")


async def turn_deg_gyro(angle_deg, stop_early_deg=0.0, **kwargs):
    """Spin in place BY this many degrees, using full PID.

    Same name as toolkit.py:303, and unlike that one this actually turns the
    robot. The toolkit's version has its motor call commented out and has never
    worked; code/learn/10-gyro.md:241-274 walks through why.

    Positive angle_deg turns clockwise (right), negative turns counter-clockwise
    (left), matching the toolkit's documented rule. This is ".Left (PID)" and
    ".Right (PID)" merged, because they were the same loop with the target
    negated.

    This is a RELATIVE turn: 90 means "a quarter turn from wherever I am now".
    Call it four times and the small errors add up. Use face() instead when that
    matters. See code/learn/gyro-correction.html.

    Fix 6: the right-hand block exited on abs((Degrees - 1) - yaw) < 1 while
    driving on Error = Degrees - yaw, so it stopped about a degree short. The
    left-hand block was symmetric. Stopping short is now stop_early_deg, it is
    off by default, and it applies to both directions.
    """
    if angle_deg == 0:
        return
    facing = 1.0 if angle_deg > 0 else -1.0
    await _settle()
    target = bearing() + angle_deg - (stop_early_deg * facing)
    await _turn_to_bearing(target, **kwargs)


async def face(bearing_deg, shortest=True, stop_early_deg=0.0, **kwargs):
    """Turn to point at an absolute bearing, measured from base.

    Base is however you set the robot down when init_robot() ran. face(90) means
    the same physical direction all run long, however far the robot has wandered
    since. That is the difference from turn_deg_gyro, which measures from
    wherever the robot happens to be pointing this second.

    Because every target is measured from the same fixed line, a turn that lands
    a degree short does not pass that degree on. Errors stop piling up. Four
    turns round a square end about 1 degree out instead of 17. The numbers are in
    code/learn/gyro-correction.html.

    shortest=True turns whichever way is nearer, so face(0) and face(360) both
    mean "back to the bearing you started on" and both take the short way round.
    Pass shortest=False to make the robot travel the long way on purpose.
    """
    await _settle()
    if shortest:
        target = bearing() + _wrap180(bearing_deg - bearing())
    else:
        target = bearing_deg
    if stop_early_deg:
        facing = 1.0 if target > bearing() else -1.0
        target = target - (stop_early_deg * facing)
    await _turn_to_bearing(target, **kwargs)


# -----------------------------
# Turns, simple
# -----------------------------
async def turn_deg(angle_deg,
                   velocity=TURN_SIMPLE_DEG_S,
                   stop_mode=motor.BRAKE,
                   overshoot_deg=None,
                   timeout_ms=DEFAULT_TIMEOUT_MS):
    """Spin in place at one fixed speed until the gyro is nearly there.

    Same name as toolkit.py:277. Positive angle_deg turns clockwise, negative
    counter-clockwise. This is "Left (simple)" and "Right (simple)" merged.

    PREFER turn_deg_gyro, OR face. This one is open loop: it spins at a flat
    speed, brakes a few degrees early, and never checks the result. That costs
    about 4 degrees a turn against turn_deg_gyro's 1. It is kept because the
    Word Blocks library has it and it is quicker.

    Cruder than turn_deg_gyro and quite a lot quicker, which is why the blocks
    kept both. It stops overshoot_deg short and lets momentum finish the turn.
    The blocks used 5 going right and 4 going left, and so does this.

    Unlike the toolkit's turn_deg, this steers off the gyro rather than counting
    wheel degrees, so it does not depend on TRACK_W_MM being right.
    """
    if angle_deg == 0:
        return

    facing = 1.0 if angle_deg > 0 else -1.0
    if overshoot_deg is None:
        overshoot_deg = 5 if angle_deg > 0 else 4

    target = abs(angle_deg)
    if target <= overshoot_deg:
        # Asking for less than the overshoot means the exit test is already
        # true, and the robot would not move at all. Fall back to the PID turn.
        await turn_deg_gyro(angle_deg, stop_mode=stop_mode)
        return

    motor_pair.move(PAIR, 0, velocity=0, acceleration=ACCEL)
    _reset_yaw(0)
    await _settle()

    power = abs(int(velocity))
    _tank(facing * power, -facing * power)

    steps = 0
    max_steps = int(timeout_ms / LOOP_MS)
    while abs(_wrap180(_yaw_cw())) < (target - overshoot_deg):
        steps += 1
        if steps > max_steps:
            if DEBUG:
                print("turn_deg timed out")
            break
        await runloop.sleep_ms(LOOP_MS)

    motor_pair.stop(PAIR, stop=stop_mode)
    await runloop.sleep_ms(100)


# -----------------------------
# Arcs, attachments and micro moves
# -----------------------------
# The blocks have none of these. They are carried over from toolkit.py so that
# the two files offer the same set of names, and a mission can move between
# them without hunting for a missing function.


async def arc_turn(radius_cm, angle_deg, velocity=400, stop_mode=motor.BRAKE):
    """Smooth arc using constant steering (approximate).

    Same as toolkit.py:340. For precise arcs, use per-wheel degrees instead.
    """
    if radius_cm <= 0:
        return
    # Steering approximation: s = (track / (2R)) * 100, clipped to -100 to 100.
    s = int(_clamp((TRACK_W_MM / (2.0 * (radius_cm * 10.0))) * 100.0,
                   -100.0, 100.0))
    arc_len_cm = abs(radius_cm * (angle_deg * pi / 180.0))
    deg = _cm_to_deg(arc_len_cm)
    steering = s if angle_deg > 0 else -s
    await motor_pair.move_for_degrees(PAIR, deg, steering,
                                      velocity=velocity, stop=stop_mode)


def _attachment_args(degrees, velocity):
    """Split a signed degree count into (degrees, signed velocity).

    SPIKE takes the direction from the sign of the VELOCITY. The degree count is
    a distance and has to be positive. Pass a negative degree count and the
    target sits behind the direction of travel, so the motor never arrives and
    the await never returns. No error, no timeout, just a program that stops.

    That cost us a hub session on 20 September 2026. The pretend hub hides it:
    tools/spike-shim.py:483-494 takes abs(degrees) and flips the velocity itself,
    so the mistake only shows on the real robot.

    Missions can therefore write -150 and mean "150 degrees the other way".
    """
    turns = abs(int(degrees))
    speed = abs(int(velocity))
    if degrees < 0:
        speed = -speed
    return turns, speed


async def run_attachment_deg(which_port, degrees, velocity=300,
                             stop_mode=motor.BRAKE):
    """Run an attachment motor by degrees (C or D typically).

    Same as toolkit.py:362, including its 200 degree guard. Negative degrees run
    the other way; see _attachment_args for why that needs handling.
    """
    if abs(degrees) > 200:
        return
    turns, speed = _attachment_args(degrees, velocity)
    await motor.run_for_degrees(which_port, turns, speed, stop=stop_mode)


async def timed_attachment(which_port, velocity=400, ms=250,
                           stop_mode=motor.BRAKE):
    """Run an attachment motor for a fixed time (ms). Same as toolkit.py:372."""
    await motor.run_for_time(which_port, ms, velocity=velocity, stop=stop_mode)


async def move_attachment_deg(which_port, degrees, velocity=1000):
    """Move an attachment motor by degrees, with no 200 degree guard.

    Same as toolkit.py:390. Negative degrees run the other way; see
    _attachment_args for why that has to be translated rather than passed
    straight through.
    """
    turns, speed = _attachment_args(degrees, velocity)
    await motor.run_for_degrees(which_port, turns, speed)


async def nudge_cm(cm=1.5, velocity=250):
    """Small forward or backward bump to settle into models. Same as toolkit.py:382."""
    await drive_cm(cm, velocity=velocity)


async def micro_turn_deg(angle=3.0, velocity=200):
    """Tiny heading adjustment. Same as toolkit.py:386.

    Anything this small goes through turn_deg_gyro, because the quick turn
    cannot resolve a few degrees.
    """
    await turn_deg_gyro(angle, velocity=velocity)


# -----------------------------
# Line blocks. Hub only.
# -----------------------------
def _need_colour():
    """Stop with something readable when the colour sensors are not usable."""
    if not _HAS_COLOUR:
        raise RuntimeError(
            "This needs the colour sensors, so it only runs on the real hub. "
            "The pretend hub used by the lesson pages has no color_sensor "
            "module. Paste this file into the SPIKE App and run it there."
        )
    for label, which_port in (("left_color", left_color),
                              ("right_color", right_color)):
        if not _has_colour(which_port):
            raise RuntimeError(
                "No colour sensor on the %s port. Under the reference wiring "
                "port F is the left drive motor, so right_color is certainly "
                "wrong. Run scan_ports() and fix the two lines at the top."
                % label
            )


def _reflect(which_port):
    return color_sensor.reflection(which_port)


async def _wait_until(test, timeout_ms=DEFAULT_TIMEOUT_MS):
    """Wait for a condition, but give up eventually.

    Fix 8. Every "wait until" in the blocks was unbounded. Miss the line once
    and the robot sits there for the rest of the match.

    Returns True if the condition came true, False if it timed out.
    """
    steps = 0
    max_steps = int(timeout_ms / LOOP_MS)
    while not test():
        steps += 1
        if steps > max_steps:
            return False
        await runloop.sleep_ms(LOOP_MS)
    return True


async def _find_line(timeout_ms=DEFAULT_TIMEOUT_MS):
    """Drive forward until the left sensor sees the line. The blocks' zFind Line."""
    speed = _pct_to_deg_s(LINE_SPEED_PCT)
    _tank(speed, speed)
    found = await _wait_until(lambda: _reflect(left_color) < LINE_DARK,
                              timeout_ms)
    motor_pair.stop(PAIR, stop=motor.BRAKE)
    return found


async def _acquire_line(side, timeout_ms=DEFAULT_TIMEOUT_MS):
    """Swing until the left sensor comes back off the line. The blocks' zAcquire Line.

    side is 1 to swing right, -1 to swing left.
    """
    speed = _pct_to_deg_s(20)
    _tank(side * speed, -side * speed)
    found = await _wait_until(lambda: _reflect(left_color) > LINE_ACQUIRE,
                              timeout_ms)
    motor_pair.stop(PAIR, stop=motor.BRAKE)
    return found


async def _follow_line(side, seconds):
    """Follow the line edge for a time. The blocks' zFollowing a line.

    One sensor, proportional. It holds the reading at LINE_TARGET, which is the
    grey halfway between the black line and the white mat. Steer is the error
    times LINE_KP, and side decides which edge of the line it rides.
    """
    speed = _pct_to_deg_s(LINE_SPEED_PCT)
    steps = int((seconds * 1000) / LOOP_MS)
    for _ in range(steps):
        error = _reflect(left_color) - LINE_TARGET
        steering = _clamp(error * LINE_KP * side * -1, -100.0, 100.0)
        motor_pair.move(PAIR, int(round(steering)), velocity=speed)
        await runloop.sleep_ms(LOOP_MS)
    motor_pair.stop(PAIR, stop=motor.BRAKE)


async def line_follow(side, seconds):
    """Find a line, get onto its edge, then follow it. HUB ONLY.

    The blocks' "Line Follow". side is 1 to swing right, -1 to swing left.
    """
    _need_colour()
    if not await _find_line():
        raise RuntimeError("Drove the whole way and never found a line.")
    if not await _acquire_line(side):
        raise RuntimeError("Found the line but could not swing off its edge.")
    await _follow_line(side, seconds)


async def _nudge_until(which_motor, speed_pct, test, timeout_ms=3000):
    """Creep one wheel until a sensor says stop. Used by line_square."""
    motor.run(which_motor, _pct_to_deg_s(speed_pct))
    reached = await _wait_until(test, timeout_ms)
    motor.stop(which_motor, stop=motor.BRAKE)
    return reached


async def line_square():
    """Square up on a line using both colour sensors. HUB ONLY.

    The blocks' "Line Square". Two passes. First drive on until either sensor
    sees black, then creep each wheel forward until both do. Then back each
    wheel off until both read light again, which lands the robot square on the
    edge rather than square on the middle.
    """
    _need_colour()

    speed = _pct_to_deg_s(15)
    _tank(speed, speed)
    seen = await _wait_until(
        lambda: _reflect(left_color) < SQUARE_DARK
        or _reflect(right_color) < SQUARE_DARK)
    motor_pair.stop(PAIR, stop=motor.BRAKE)
    if not seen:
        raise RuntimeError("Drove the whole way and never found a line to square on.")

    # Coarse pass: bring whichever side is lagging onto the black.
    if _reflect(left_color) > SQUARE_DARK:
        await _nudge_until(LEFT_DRIVE, -20,
                           lambda: _reflect(left_color) < SQUARE_DARK)
    if _reflect(right_color) > SQUARE_DARK:
        await _nudge_until(RIGHT_DRIVE, 20,
                           lambda: _reflect(right_color) < SQUARE_DARK)

    # Fine pass: back off until each sensor reads the light side of the edge.
    await _nudge_until(RIGHT_DRIVE, -10,
                       lambda: _reflect(right_color) > SQUARE_LIGHT)
    await _nudge_until(LEFT_DRIVE, 10,
                       lambda: _reflect(left_color) > SQUARE_LIGHT)
    await runloop.sleep_ms(200)

    # And once more, gently, for anything that crept past.
    if _reflect(left_color) > SQUARE_LIGHT:
        await _nudge_until(LEFT_DRIVE, -8,
                           lambda: _reflect(left_color) < SQUARE_LIGHT)
    if _reflect(right_color) > SQUARE_LIGHT:
        await _nudge_until(RIGHT_DRIVE, 8,
                           lambda: _reflect(right_color) < SQUARE_LIGHT)
    await runloop.sleep_ms(100)


# -----------------------------
# Settling YAW_SIGN
# -----------------------------
async def bench_check_yaw_sign():
    """Work out which way the gyro counts. Run this on the hub, once.

    Put the robot on the table with room to spin. It turns clockwise about a
    quarter turn and prints what the gyro did.

    Then set YAW_SIGN at the top of this file to the number it tells you, and
    write the answer into code/learn/10-gyro.md so nobody has to ask again.
    """
    await init_robot()
    _reset_yaw(0)
    await runloop.sleep_ms(300)

    before = _yaw_deg()
    power = _pct_to_deg_s(15)
    _tank(power, -power)               # clockwise, by definition of _tank
    await runloop.sleep_ms(1200)
    motor_pair.stop(PAIR, stop=motor.BRAKE)
    await runloop.sleep_ms(400)
    after = _yaw_deg()

    change = _wrap180(after - before)
    print("yaw before:", round(before, 1))
    print("yaw after: ", round(after, 1))
    print("the robot turned clockwise, and the gyro changed by", round(change, 1))
    if change > 0:
        print("=> the gyro counts UP clockwise. Set YAW_SIGN = +1")
    elif change < 0:
        print("=> the gyro counts DOWN clockwise. Set YAW_SIGN = -1")
    else:
        print("=> it did not move. Check the motors are paired and try again.")
    return change


# -----------------------------
# Names closer to the block palette
# -----------------------------
# The functions above are named after toolkit.py, so the two Python files read
# the same. These wrappers are named after the SPIKE App palette instead, for
# anybody reading the blocks and this file side by side. Same functions.
#
# Prefer the toolkit names in mission code. These take CENTIMETRES where the
# block took millimetres, which is exactly the trap drive_cm already guards
# against.


async def forward(cm, **kwargs):
    """The blocks' ".Forward". Centimetres here, millimetres in the block."""
    await drive_cm(abs(cm), **kwargs)


async def backward(cm, **kwargs):
    """The blocks' ".Backward". Centimetres here, millimetres in the block."""
    await drive_cm(-abs(cm), **kwargs)


async def left_pid(degrees, **kwargs):
    """The blocks' ".Left (PID)". Degrees, same as the block."""
    await turn_deg_gyro(-abs(degrees), **kwargs)


async def right_pid(degrees, **kwargs):
    """The blocks' ".Right (PID)". Degrees, same as the block."""
    await turn_deg_gyro(abs(degrees), **kwargs)


async def left_simple(degrees, **kwargs):
    """The blocks' "Left (simple)". Degrees, same as the block."""
    await turn_deg(-abs(degrees), **kwargs)


async def right_simple(degrees, **kwargs):
    """The blocks' "Right (simple)". Degrees, same as the block."""
    await turn_deg(abs(degrees), **kwargs)


async def gyro_backwards(speed_pct, degrees, **kwargs):
    """The blocks' "Gyro Backwards (degrees) basic". Motor degrees, not distance."""
    await gyro_backward_deg(speed_pct, degrees, **kwargs)


# -----------------------------
# Demo
# -----------------------------
# This mirrors the "when program starts" stack in Advanced-Coding-26.llsp3:
# forward 300 mm, left 90, right 90, backward 300 mm.
#
# It is NOT called at the bottom of this file, on purpose. toolkit.py:436 calls
# runloop.run(main()) at the top level, and tools/check-lessons.py execs the
# toolkit for every lesson block, so that program is queued and drained on every
# single one. To run this, call runloop.run(demo()) yourself.
async def demo():
    await init_robot()
    await drive_cm(30)
    await turn_deg_gyro(-90)
    await turn_deg_gyro(90)
    await drive_cm(-30)
