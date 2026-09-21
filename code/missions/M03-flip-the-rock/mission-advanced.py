# GENERATED FILE — do not edit above the marker.
#
# The part above the marker is a copy of code/library/advanced.py. Refresh it
# with:
#
#     python3 tools/build-mission.py code/missions/M03-flip-the-rock/mission-advanced.py
#
# Edit below the marker. That is where the ports and the mission live.

# Advanced library — Python version of our Word Blocks library
#
# This is the same movement code as the SPIKE App project "Advanced Coding 26",
# rewritten in Python. Paste this whole file onto the hub above your mission.
#
# Distances are in centimetres. Speeds are in degrees per second, the same as
# code/library/toolkit.py, so the names you learned in code/learn/ still work.
#
# turn_deg turns BY an amount. face turns TO a direction, measured from base,
# which is what stops the mistakes piling up over a run.
#
# The story behind this file — the bugs we found in the blocks, which port the
# motors are on, and why YAW_SIGN is -1 — is in code/library/README.md.

from hub import port, motion_sensor
import runloop
import motor_pair
import motor
from math import pi

# -----------------------------
# Our robot
# -----------------------------
PAIR = motor_pair.PAIR_1

LEFT_DRIVE = port.F
RIGHT_DRIVE = port.A

attachment1 = port.C
attachment2 = port.D           # not confirmed

WHEEL_D_MM = 62.4              # measure this. Everything depends on it
TRACK_W_MM = 130.0             # only arc_turn uses this one
ACCEL = 1000
DECEL = 1000

# Stretches or shrinks every distance. 1.0 means no change.
CALIBRATION_SCALE = 1.0

# True prints a line every 15 ms, which is a lot. Only turn it on to hunt a bug.
DEBUG = False


# -----------------------------
# Which way does the gyro count?
# -----------------------------
# -1 means the number goes UP when the robot turns left.
# We measured this on our hub on 20 September 2026. Before that we guessed +1,
# and the robot spun on the spot instead of driving, because the correction was
# pushing the wrong way. bench_check_yaw_sign() measures it again in a minute.
YAW_SIGN = -1


# -----------------------------
# Speeds, in degrees per second
# -----------------------------
# The blocks used percent. We use degrees per second everywhere, so nothing has
# to be converted while the robot is moving. 100 percent is MAX_DEG_S.
MAX_DEG_S = 1050

TOP_SPEED = 630                # blocks: 60 percent
TOP_SPEED_SHORT = 315          # blocks: 30 percent, for moves under 30 cm
START_SPEED = 262              # blocks: 25 percent, where a ramp starts
TURN_MAX = 630                 # how hard a gyro turn is allowed to push
TURN_MIN = 126                 # below this the wheels buzz and do not move

# How hard to push back when the robot drifts off straight.
# These came from the blocks as 1.8 and 0.5 percent per degree. Multiplied by
# 10.5 to turn percent into degrees per second, so the robot behaves the same.
KP_STRAIGHT = 18.9
KD_STRAIGHT = 5.25

KP_BACK = 15.75                # blocks: 1.5
KD_BACK = 10.5                 # blocks: 1.0

KP_TURN = 7.35                 # blocks: 0.7
KI_TURN = 0.0105               # blocks: 0.001
KD_TURN = 1.05                 # blocks: 0.1

# How far the robot rolls after the brakes go on. We take this off the target so
# the rolling lands us on the mark. Measure it: the mission log prints it.
STOP_COMP_FWD_CM = 1.4
STOP_COMP_REV_CM = 1.5

# drive_cm works these out for you, the way the .Forward block did.
RAMP_FRACTION = 4.0            # ramp over a quarter of the distance
RAMP_MIN_CM = 3.0
RAMP_MAX_CM = 10.0
SHORT_RUN_CM = 30.0            # under this, drive slower

# The mat is 200 cm wide. A longer straight drive is always millimetres typed
# into a centimetres argument by mistake.
MAX_SENSIBLE_CM = 200.0

# Give up after this long rather than getting stuck forever.
DEFAULT_TIMEOUT_MS = 8000
LOOP_MS = 15                   # one trip round a correction loop

# How far off straight a "straight" drive may get before it gives up.
#
# A drive that is holding a heading should never be tens of degrees out. If it
# is, the loop is pushing the wrong way and the robot is spinning, not driving.
# That happened on 20 September 2026 with YAW_SIGN set the wrong way. Without
# this the robot spun until the distance counter filled up, which took it clean
# off the table.
RUNAWAY_DEG = 45.0

# Cruise speed for drive_cm. None means "work it out for each move".
DEFAULT_DRIVE_DEG_S = None

# Which direction the gyro's zero stands for. See _reset_yaw and bearing.
_HEADING_BASE = 0.0

# What the last drive aimed for, so a mission log can check itself.
_LAST_DRIVE_TARGET_CM = 0.0
_LAST_DRIVE_COMP_CM = 0.0


# -----------------------------
# Sums
# -----------------------------
def _cm_to_deg(cm):
    """How many degrees the wheels must turn to travel this far."""
    circ_mm = pi * WHEEL_D_MM * CALIBRATION_SCALE
    return int(round((abs(cm) * 10.0) / circ_mm * 360.0))


def _deg_to_cm(deg):
    """The other way round: wheel degrees back into centimetres.

    Do not do this by dividing by _cm_to_deg(1). That rounds 18.47 down to 18,
    and then every distance you print is 2.6 percent too big.
    """
    circ_mm = pi * WHEEL_D_MM * CALIBRATION_SCALE
    return (abs(deg) / 360.0) * circ_mm / 10.0


def _wrap180(a):
    """Squash any angle into -180 to 180, so 350 becomes -10."""
    return (a + 180.0) % 360.0 - 180.0


def _clamp(value, low, high):
    """Keep a number between two limits."""
    if value < low:
        return low
    if value > high:
        return high
    return value


# -----------------------------
# The gyro
# -----------------------------
def _yaw_deg():
    """What the gyro says, in degrees. It reports tenths, so divide by ten."""
    y_decideg, _, _ = motion_sensor.tilt_angles()
    return y_decideg / 10.0


def _yaw_cw():
    """The gyro reading, made to count up clockwise whatever our hub does.

    Everything steers off this instead of _yaw_deg, which is why fixing the
    direction is one line at the top and not twenty lines scattered about.
    """
    return YAW_SIGN * _yaw_deg()


def _reset_yaw(deg=0):
    """Set the gyro back to zero, but remember which way we were pointing.

    Some moves zero the gyro so that "straight ahead" reads 0. That would
    normally lose track of base. So we add up what the gyro said first, like
    writing down the mileage before resetting a car's trip counter.
    """
    global _HEADING_BASE
    _HEADING_BASE = _HEADING_BASE + _yaw_cw() - deg
    motion_sensor.reset_yaw(int(deg * 10))


def bearing():
    """Which way we are pointing, in degrees from base. Right is positive.

    Base is however you put the robot down before init_robot(). This keeps
    counting past 360, so four right turns read about 360 and not 0.
    """
    return _HEADING_BASE + _yaw_cw()


# -----------------------------
# Driving the two wheels
# -----------------------------
def _drive_degrees():
    """How far the wheels have turned since the last reset.

    We take the size of both and average them. The two encoders are mirrored, so
    one counts up going forwards and the other counts up going backwards. Using
    the size of both means this works whichever way we are driving.
    """
    left = abs(motor.relative_position(LEFT_DRIVE))
    right = abs(motor.relative_position(RIGHT_DRIVE))
    return (left + right) // 2


def _tank(left_deg_s, right_deg_s):
    """Run the two wheels at different speeds. That is how the robot steers.

    We cannot just start each motor on its own, because they are paired and
    would fight. motor_pair.move wants one speed and one steering number, so
    this works out which pair gives the two wheel speeds we asked for.

    The faster wheel becomes the speed. The slower one sets the steering.
    """
    left = float(left_deg_s)
    right = float(right_deg_s)

    if left == 0.0 and right == 0.0:
        motor_pair.move(PAIR, 0, velocity=0)
        return

    # A big correction on top of a fast speed can ask for more than the motor
    # has. Slow both wheels by the same amount, so we still steer the same way.
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
# What is plugged in where
# -----------------------------
ALL_PORTS = (("A", port.A), ("B", port.B), ("C", port.C),
             ("D", port.D), ("E", port.E), ("F", port.F))


def port_label(which_port):
    """Turn a port into its letter, so messages can say "C"."""
    for name, candidate in ALL_PORTS:
        if candidate is which_port:
            return name
    return "?"


def _has_motor(which_port):
    """Is there a motor on this port? Asking it is the only way to find out."""
    try:
        motor.relative_position(which_port)
        return True
    except Exception:
        return False


# -----------------------------
# Getting started
# -----------------------------
async def reset_yaw():
    """Zero the gyro and both wheel counters, and call this spot base."""
    global _HEADING_BASE
    motion_sensor.reset_yaw(0)
    _HEADING_BASE = 0.0
    motor.reset_relative_position(LEFT_DRIVE, 0)
    motor.reset_relative_position(RIGHT_DRIVE, 0)
    await runloop.sleep_ms(500)


async def init_robot(default_speed=None):
    """Pair the wheels and zero everything. Call this once, first.

    Leave default_speed out and each drive picks its own speed. Give it a number
    in degrees per second to make every drive use that instead.
    """
    global DEFAULT_DRIVE_DEG_S
    DEFAULT_DRIVE_DEG_S = None if default_speed is None else int(default_speed)

    # Check before pairing. Pairing an empty port throws ENODEV, which does not
    # tell you which port was wrong.
    missing = []
    if not _has_motor(LEFT_DRIVE):
        missing.append("LEFT_DRIVE")
    if not _has_motor(RIGHT_DRIVE):
        missing.append("RIGHT_DRIVE")
    if missing:
        raise RuntimeError(
            "No motor on the %s port. Check the cables, then fix LEFT_DRIVE "
            "and RIGHT_DRIVE at the top of this file."
            % " or ".join(missing))

    motor_pair.pair(PAIR, LEFT_DRIVE, RIGHT_DRIVE)
    await reset_yaw()


async def _settle():
    """Wait for the gyro to stop wobbling before we zero it.

    The gyro keeps drifting for a moment after the motors stop. Zeroing it while
    it is still moving bakes that mistake into everything afterwards.
    """
    await runloop.sleep_ms(300)


def set_calibration_scale(scale):
    """Stretch or shrink every distance. Returns what it is now."""
    global CALIBRATION_SCALE
    value = float(scale)
    if value > 0:
        CALIBRATION_SCALE = value
    return CALIBRATION_SCALE


def calibrate_wheel_diameter(commanded_cm, measured_cm):
    """Work the scale out from one measured drive. Returns what it is now."""
    global CALIBRATION_SCALE
    if commanded_cm == 0:
        return CALIBRATION_SCALE
    CALIBRATION_SCALE = float(measured_cm) / float(commanded_cm)
    return CALIBRATION_SCALE


# -----------------------------
# Driving straight
# -----------------------------
async def _drive_ramp_cm(cm,
                         top_speed=TOP_SPEED,
                         start_speed=START_SPEED,
                         ramp_cm=RAMP_MIN_CM,
                         stop_comp_cm=None,
                         kp=KP_STRAIGHT,
                         kd=KD_STRAIGHT,
                         stop_mode=motor.BRAKE,
                         timeout_ms=DEFAULT_TIMEOUT_MS):
    """Drive straight, speeding up and slowing down, held straight by the gyro.

    Three parts: speed up over the first ramp_cm, hold, slow down over the last
    ramp_cm. Starting gently stops the wheels slipping. Finishing gently stops
    the robot carrying past the mark.
    """
    if cm == 0:
        return

    direction = 1.0 if cm > 0 else -1.0

    if stop_comp_cm is None:
        stop_comp_cm = STOP_COMP_FWD_CM if cm > 0 else STOP_COMP_REV_CM
        # The blocks took off a flat 14 mm, which is only right at full speed.
        # The robot rolls further when it is going faster, so scale it.
        stop_comp_cm *= top_speed / float(TOP_SPEED)
        # And never give away more than a quarter of a short move, or a 1.5 cm
        # nudge loses nearly all of itself.
        stop_comp_cm = min(stop_comp_cm, abs(cm) * 0.25)

    target_cm = abs(cm) - stop_comp_cm
    if target_cm <= 0:
        return

    # Remember what we aimed for, so a mission log can compare fairly.
    global _LAST_DRIVE_TARGET_CM, _LAST_DRIVE_COMP_CM
    _LAST_DRIVE_TARGET_CM = target_cm
    _LAST_DRIVE_COMP_CM = stop_comp_cm

    dist_deg = _cm_to_deg(target_cm)
    ramp_deg = max(1, _cm_to_deg(abs(ramp_cm)))
    if ramp_deg * 2 > dist_deg:              # two ramps cannot be longer than the move
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
                print("drive gave up at", travelled, "of", dist_deg)
            break

        # Which part of the ramp are we in, and how fast should we be going?
        if travelled < ramp_deg:
            fraction = travelled / ramp_deg
        elif travelled < (dist_deg - ramp_deg):
            fraction = 1.0
        else:
            fraction = (dist_deg - travelled) / ramp_deg
        speed = (top_speed - start_speed) * fraction + start_speed

        # The gyro reads 0 when we are straight, so the reading IS the mistake.
        # The minus sign makes the correction push against it. Take the minus
        # away and it pushes with it, and the robot spirals instead of driving.
        error = _wrap180(_yaw_cw())
        trim = -(kp * error + kd * (error - last_error))
        last_error = error

        if abs(error) > RUNAWAY_DEG:
            motor_pair.stop(PAIR, stop=motor.BRAKE)
            raise RuntimeError(
                "Straight drive is %.0f degrees off course, so it stopped. The "
                "heading loop is pushing the wrong way. Either YAW_SIGN is "
                "wrong, or LEFT_DRIVE and RIGHT_DRIVE are swapped. Run "
                "bench_check_yaw_sign() and watch which way the robot turns."
                % error)

        base = direction * speed
        _tank(base + trim, base - trim)

        if DEBUG:
            print("deg:", travelled, "of", dist_deg,
                  "speed:", int(speed), "yaw:", round(error, 2))

        await runloop.sleep_ms(LOOP_MS)

    motor_pair.stop(PAIR, stop=stop_mode)
    await runloop.sleep_ms(200)


def _auto_ramp_cm(cm):
    """How long a ramp to use, if you did not say."""
    return _clamp(abs(cm) / RAMP_FRACTION, RAMP_MIN_CM, RAMP_MAX_CM)


def _auto_top_speed(cm):
    """How fast to go, if you did not say. Short moves go slower."""
    return TOP_SPEED_SHORT if abs(cm) < SHORT_RUN_CM else TOP_SPEED


def _check_sensible(cm):
    """Catch millimetres typed into a centimetres argument.

    The blocks take millimetres and this takes centimetres. ".Forward 300"
    copied straight across asks for three metres, and the mat is only two.
    """
    if abs(cm) > MAX_SENSIBLE_CM:
        raise ValueError(
            "%g cm is longer than the mat. The Word Blocks take millimetres "
            "and this takes centimetres, so .Forward 300 is drive_cm(30)." % cm)


async def drive_cm(cm,
                   velocity=None,
                   stop_mode=motor.BRAKE,
                   start_velocity=None,
                   ramp_cm=None,
                   kp=KP_STRAIGHT,
                   kd=KD_STRAIGHT):
    """Drive straight. Positive is forwards, negative is backwards.

    Unlike the toolkit's drive_cm, this one holds its heading with the gyro.
    Leave velocity out and it picks its own speed.
    """
    _check_sensible(cm)
    if cm == 0:
        return

    distance = abs(cm)

    if velocity is None:
        velocity = DEFAULT_DRIVE_DEG_S
    top_speed = _auto_top_speed(distance) if velocity is None else abs(int(velocity))
    top_speed = _clamp(top_speed, 1, MAX_DEG_S)

    if start_velocity is None:
        start_speed = min(START_SPEED, top_speed)
    else:
        start_speed = _clamp(abs(int(start_velocity)), 1, top_speed)

    if ramp_cm is None:
        ramp_cm = _auto_ramp_cm(distance)

    await _drive_ramp_cm(distance if cm > 0 else -distance,
                         top_speed=top_speed,
                         start_speed=start_speed,
                         ramp_cm=ramp_cm,
                         kp=kp, kd=kd, stop_mode=stop_mode)


async def drive_cm_gyro(cm, velocity=None, kp=KP_STRAIGHT, kd=KD_STRAIGHT,
                        stop_mode=motor.BRAKE, **kwargs):
    """The same thing as drive_cm. Both names work, both use the gyro."""
    await drive_cm(cm, velocity=velocity, kp=kp, kd=kd,
                   stop_mode=stop_mode, **kwargs)


async def gyro_backward_deg(speed, degrees,
                            kp=KP_BACK, kd=KD_BACK,
                            timeout_ms=DEFAULT_TIMEOUT_MS):
    """Reverse at one speed for a number of WHEEL degrees, held straight.

    The odd one out: it counts wheel degrees, not centimetres. That is how the
    "Gyro Backwards basic" block worked and we kept it the same.
    """
    target_deg = abs(degrees)
    if target_deg == 0:
        return

    motor.reset_relative_position(LEFT_DRIVE, 0)
    motor.reset_relative_position(RIGHT_DRIVE, 0)
    await _settle()
    _reset_yaw(0)

    last_error = 0.0           # the block forgot this, and used stale data
    steps = 0
    max_steps = int(timeout_ms / LOOP_MS)

    while _drive_degrees() < target_deg:
        steps += 1
        if steps > max_steps:
            if DEBUG:
                print("gyro_backward_deg gave up")
            break

        error = _wrap180(_yaw_cw())
        trim = -(kp * error + kd * (error - last_error))
        last_error = error

        if abs(error) > RUNAWAY_DEG:
            motor_pair.stop(PAIR, stop=motor.BRAKE)
            raise RuntimeError(
                "Reverse drive is %.0f degrees off course, so it stopped. See "
                "the note on RUNAWAY_DEG, and run bench_check_yaw_sign()."
                % error)

        base = -abs(int(speed))
        _tank(base + trim, base - trim)
        await runloop.sleep_ms(LOOP_MS)

    motor_pair.stop(PAIR, stop=motor.BRAKE)
    await runloop.sleep_ms(200)


# -----------------------------
# Turning
# -----------------------------
async def _turn_to_bearing(target,
                           velocity=TURN_MAX,
                           kp=KP_TURN, ki=KI_TURN, kd=KD_TURN,
                           tolerance=1.0,
                           stop_mode=motor.BRAKE,
                           min_speed=TURN_MIN,
                           integral_limit=500.0,
                           settle_ms=150,
                           settle_passes=2,
                           timeout_ms=DEFAULT_TIMEOUT_MS):
    """Spin until bearing() reaches target. Both turns share this loop.

    After braking it waits, looks again, and goes round once more if the robot
    rolled past. Without that the roll after the brake is never corrected, and
    on our hub that was worth about 2.4 degrees every turn.
    """
    max_speed = abs(int(velocity))
    max_steps = int(timeout_ms / LOOP_MS)

    for _attempt in range(1 + max(0, settle_passes)):
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
                    print("turn gave up", round(error, 2), "degrees short")
                break

            integral = _clamp(integral + error, -integral_limit, integral_limit)
            derivative = error - previous_error
            previous_error = error

            speed = _clamp(kp * error + ki * integral + kd * derivative,
                           -max_speed, max_speed)
            # Too slow to move at all, so give it the minimum push instead.
            if 0 < abs(speed) < min_speed:
                speed = min_speed if speed > 0 else -min_speed

            _tank(speed, -speed)
            if DEBUG:
                print("turn err:", round(error, 2), "speed:", int(speed))
            await runloop.sleep_ms(LOOP_MS)

        motor_pair.stop(PAIR, stop=stop_mode)
        await runloop.sleep_ms(settle_ms)

        if abs(target - bearing()) < tolerance:
            break
        if DEBUG:
            print("rolled past by", round(target - bearing(), 2), "- going again")


async def turn_deg(angle_deg, stop_early_deg=0.0, **kwargs):
    """Turn BY this many degrees. Positive is right, negative is left.

    This is a relative turn: 90 means a quarter turn from wherever we are now.
    Call it four times and the small mistakes add up. Use face() when that
    matters. There are pictures in code/learn/gyro-correction.html.
    """
    if angle_deg == 0:
        return
    facing = 1.0 if angle_deg > 0 else -1.0
    await _settle()
    await _turn_to_bearing(bearing() + angle_deg - stop_early_deg * facing,
                           **kwargs)


async def turn_deg_gyro(angle_deg, stop_early_deg=0.0, **kwargs):
    """The same thing as turn_deg. Both names work, both use the gyro.

    toolkit.py has a slow turn_deg and a gyro turn_deg_gyro. Here there is only
    the gyro one, so it does not matter which name you reach for.
    """
    await turn_deg(angle_deg, stop_early_deg=stop_early_deg, **kwargs)


async def face(bearing_deg, shortest=True, stop_early_deg=0.0, **kwargs):
    """Turn to point a particular way, counting from base.

    face(90) means the same direction all run long, however far the robot has
    wandered. Because every target is measured from base, a turn that lands a
    degree short does not pass that degree on to the next one. Four turns round
    a square end about 1 degree out instead of 17.

    shortest=True goes whichever way is nearer, so face(0) and face(360) both
    mean "back the way we started".
    """
    await _settle()
    target = bearing() + _wrap180(bearing_deg - bearing()) if shortest else bearing_deg
    if stop_early_deg:
        facing = 1.0 if target > bearing() else -1.0
        target = target - stop_early_deg * facing
    await _turn_to_bearing(target, **kwargs)


# -----------------------------
# Arcs, attachments, little moves
# -----------------------------
# The blocks have none of these. They come from toolkit.py, because that is what
# the lessons in code/learn/ teach.


async def arc_turn(radius_cm, angle_deg, velocity=400, stop_mode=motor.BRAKE):
    """Drive a curve instead of turning on the spot. Roughly."""
    if radius_cm <= 0:
        return
    s = int(_clamp((TRACK_W_MM / (2.0 * radius_cm * 10.0)) * 100.0, -100.0, 100.0))
    arc_len_cm = abs(radius_cm * (angle_deg * pi / 180.0))
    await motor_pair.move_for_degrees(PAIR, _cm_to_deg(arc_len_cm),
                                      s if angle_deg > 0 else -s,
                                      velocity=velocity, stop=stop_mode)


def _attachment_args(degrees, velocity):
    """Split signed degrees into (degrees, signed speed).

    SPIKE takes the direction from the sign of the SPEED. The degrees are a
    distance and must be positive. Give it negative degrees and the target sits
    behind the motor, so it never arrives and the await never finishes. No
    error, no timeout, the program just stops. That cost us an evening.
    """
    turns = abs(int(degrees))
    speed = abs(int(velocity))
    return turns, (-speed if degrees < 0 else speed)


async def run_attachment_deg(which_port, degrees, velocity=300,
                             stop_mode=motor.BRAKE):
    """Turn an attachment motor. Refuses anything over 200 degrees."""
    if abs(degrees) > 200:
        return
    turns, speed = _attachment_args(degrees, velocity)
    await motor.run_for_degrees(which_port, turns, speed, stop=stop_mode)


async def move_attachment_deg(which_port, degrees, velocity=1000):
    """Turn an attachment motor, with no 200 degree limit."""
    turns, speed = _attachment_args(degrees, velocity)
    await motor.run_for_degrees(which_port, turns, speed)


# -----------------------------
# Checking the gyro direction
# -----------------------------
async def bench_check_yaw_sign():
    """Work out which way our gyro counts. Run this once, on the table.

    Give the robot room to spin. It turns right about a quarter turn and tells
    you what to put in YAW_SIGN at the top of this file.
    """
    await init_robot()
    _reset_yaw(0)
    await runloop.sleep_ms(300)

    before = _yaw_deg()
    _tank(157, -157)                  # right, because that is what _tank means
    await runloop.sleep_ms(1200)
    motor_pair.stop(PAIR, stop=motor.BRAKE)
    await runloop.sleep_ms(400)
    after = _yaw_deg()

    change = _wrap180(after - before)
    print("yaw before:", round(before, 1))
    print("yaw after: ", round(after, 1))
    print("we turned right, and the gyro changed by", round(change, 1))
    if change > 0:
        print("=> it counts UP going right. Set YAW_SIGN = +1")
    elif change < 0:
        print("=> it counts DOWN going right. Set YAW_SIGN = -1")
    else:
        print("=> it did not move. Check the wheels are paired and try again.")
    return change


# ===== MISSION CODE BELOW. THE GENERATOR DOES NOT TOUCH THIS =====
#
# M03 — Flip the Rock, on the advanced library.
#
# Everything above the marker is generated from code/library/advanced.py.
# Refresh it with:  python3 tools/build-mission.py
#
# Ports come from the library above (F left, A right). Override them here
# if this robot is wired differently, and the override survives a rebuild.

# -----------------------------
# Main program
# -----------------------------
async def main():
    await init_robot(default_speed=500)

    motor.run_for_degrees(port.C, 180, 500)
    print (set_calibration_scale(179/180))
    await drive_cm(-44)
    await drive_cm(44)
    #await motor.run_for_degrees(port.D, 180, 200)


    #await drive_cm(-60)

    #await turn_deg_gyro(45)

    # await turn_deg_gyro(90)
    # await turn_deg_gyro(90)
    # await turn_deg_gyro(90)

    # await turn_deg_gyro(-90)

    # await run_mission1()

# Run the main loop
runloop.run(main())
