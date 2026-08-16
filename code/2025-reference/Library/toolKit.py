# Team Toolkit – Single File (SPIKE App 3.5)
# Drive: A (left), E (right)
# Wheels: 87 mm diameter
# Track width: 143 mm (center-to-center distance between wheels)

from hub import port, motion_sensor
import runloop
import motor_pair
import motor
from math import pi

# -----------------------------
# Robot configuration
# -----------------------------
PAIR = motor_pair.PAIR_1

# Main Drive motors
LEFT_DRIVE= port.A
RIGHT_DRIVE = port.E

# Downward color sensors
left_color = port.F
right_color = port.B

# Attachment/Tool motors
attachment1 = port.C
attachment2 = port.D

# Wheel and robot dimensions
WHEEL_D_MM= 88.0    # wheel diameter
TRACK_W_MM= 143.0    # track width
ACCEL    = 1000    # deg/s^2
DECEL    = 1000

# Calibration multiplier for effective wheel diameter. 1.0 = no change.
CALIBRATION_SCALE = 1.0

# Enable debug prints in drive routines (set False to silence)
DEBUG = True

# -----------------------------
# Geometry helpers
# -----------------------------
def _cm_to_deg(cm: float) -> int:
    """Convert straight-line distance (cm) to motor shaft degrees."""
    effective_wheel_d = WHEEL_D_MM * CALIBRATION_SCALE
    circ_mm = pi * effective_wheel_d          # wheel circumference (mm)
    rotations = (abs(cm) * 10.0) / circ_mm    # cm -> mm -> rotations
    return int(round(rotations * 360.0))      # -> degrees


def _robot_deg_to_wheel_deg(robot_deg: float) -> int:
    """Convert a robot in-place rotation (degrees) to wheel shaft degrees."""
    turn_circ_mm = pi * TRACK_W_MM                        # turn circle (mm)
    travel_mm = (abs(robot_deg) / 360.0) * turn_circ_mm    # wheel path (mm)
    effective_wheel_d = WHEEL_D_MM * CALIBRATION_SCALE
    wheel_rot = travel_mm / (pi * effective_wheel_d)
    return int(round(wheel_rot * 360.0))

def _yaw_deg() -> float:
    y_decideg, _, _ = motion_sensor.tilt_angles()
    return y_decideg / 10.0

def _reset_yaw(deg: int = 0) -> None:
    motion_sensor.reset_yaw(int(deg * 10))


#------------------------------
# Calibration
#-----------------------------
def calibrate_wheel_diameter(commanded_cm: float, measured_cm: float) -> float:
    """Compute and set a calibration scale so future commands match measured travel.

    Returns the new calibration scale. Use this after measuring a known commanded distance
    and the actual distance the robot traveled.
    """
    global CALIBRATION_SCALE
    if commanded_cm == 0:
        return CALIBRATION_SCALE
    CALIBRATION_SCALE = float(measured_cm) / float(commanded_cm)
    return CALIBRATION_SCALE


def set_calibration_scale(scale: float) -> float:
    """Set the calibration scale directly (must be > 0). Returns the new scale."""
    global CALIBRATION_SCALE
    try:
        s = float(scale)
        if s <= 0:
            return CALIBRATION_SCALE
        CALIBRATION_SCALE = s
    except Exception:
        pass
    return CALIBRATION_SCALE


# -----------------------------
# Init
# -----------------------------

async def reset_yaw():
    motion_sensor.reset_yaw(0)
    motor.reset_relative_position(LEFT_DRIVE, 0)
    motor.reset_relative_position(RIGHT_DRIVE, 0)
    await runloop.sleep_ms(500)

async def init_robot(default_speed: int = 500):
    """
    Pair A/E as the drive motors and set a default speed for the pair.
    Call this once at the start of your program.
    """
    motor_pair.pair(PAIR, LEFT_DRIVE, RIGHT_DRIVE)
    await reset_yaw()


# -----------------------------
# Core movement
# -----------------------------
async def drive_cm(cm: float,
                velocity: int = 500,
                stop_mode: int = motor.BRAKE,
                acceleration: int = ACCEL,
                deceleration: int = DECEL):
    """
    Drive straight for 'cm' centimeters using encoders.
    +cm = forward, -cm = backward
    """
    _reset_yaw(0)
    print("yaw_before", _yaw_deg())

    deg = _cm_to_deg(cm)
    vel = velocity if cm >= 0 else -velocity
    await motor_pair.move_for_degrees(
        PAIR,
        deg,
        0,                            # steering = 0 → straight
        velocity=vel,
        stop=stop_mode,
        acceleration=acceleration,
        deceleration=deceleration
    )
    print ("yaw_now", _yaw_deg())

# Helper to wrap any angle to [-180, 180)
def _wrap180(a: float) -> float:
    a = (a + 180.0) % 360.0 - 180.0
    return a

#Drive with gyro
# Speed: 600, kp: 2.8, steer rate limit: 4, deadband_deg: float = 0.1 
# Speed: 500, kp: 2.6, steer rate limit: 6, deadband_deg: float = 0.1, min_steer_kick = 0 
# Speed: 400, kp 3.2, steer rate limit : 10, deadband_deg: float = 0.1
async def drive_cm_gyro(cm: float,
                        velocity: int = 500,
                        kp: float = 2.6,
                        steer_limit: int = 70,    # must be <= 100
                        deadband_deg: float = 0.1,# 0.0 to micro-correct tiny errors
                        steer_rate_limit: int = 6,# set 8–10 later for smoothness
                        min_steer_kick: int = 0,  # 0–2 to overcome quantization
                        stop_mode_end: int = motor.SMART_BRAKE):
    """
    SPIKE App 3.5 gyro-straight drive using motor_pair.move().
    Steering is clamped to [-100, 100] and updated continuously.
    Works for forward (+cm) and reverse (-cm).
    """
    if cm == 0:
        return

    # Enforce legal limits for steering
    STEER_LIMIT = int(steer_limit)
    if STEER_LIMIT < 0:
        STEER_LIMIT = 0
    if STEER_LIMIT > 100:
        STEER_LIMIT = 100

    MIN_STEER = int(min_steer_kick)
    if MIN_STEER < 0:
        MIN_STEER = 0
    if MIN_STEER > 2:
        MIN_STEER = 2

    # Distance bookkeeping
    target_deg = abs(_cm_to_deg(cm))
    dir_sign = 1 if cm >= 0 else -1

    # Reset sensors and let the IMU settle
    _reset_yaw(0)
    motor.reset_relative_position(LEFT_DRIVE, 0)
    motor.reset_relative_position(RIGHT_DRIVE, 0)
    await runloop.sleep_ms(200)

    # Begin motion with persistent command
    motor_pair.move(PAIR, 0, velocity=dir_sign * velocity)

    def _avg_deg():
        ld = abs(motor.relative_position(LEFT_DRIVE))
        rd = abs(motor.relative_position(RIGHT_DRIVE))
        return (ld + rd) // 2

    prev_steer = 0
    _reset_yaw(0)
    while True:
        traveled = _avg_deg()
        if traveled >= target_deg:
            break

        yaw_now = _yaw_deg()
        yaw_err = _wrap180(yaw_now)

        if dir_sign < 0:
            yaw_err = -yaw_err

        if abs(yaw_err) <= deadband_deg:
            raw_steer = 0
        else:
            raw_steer = round(yaw_err * kp)
            if raw_steer > STEER_LIMIT:
                raw_steer = STEER_LIMIT
            if raw_steer < -STEER_LIMIT:
                raw_steer = -STEER_LIMIT
            if raw_steer != 0 and abs(raw_steer) < MIN_STEER:
                if raw_steer > 0:
                    raw_steer = MIN_STEER
                else:
                    raw_steer = -MIN_STEER

        if steer_rate_limit == 0:
            steer = raw_steer
        else:
            delta = raw_steer - prev_steer
            if delta > steer_rate_limit:
                steer = prev_steer + steer_rate_limit
            elif delta < -steer_rate_limit:
                steer = prev_steer - steer_rate_limit
            else:
                steer = raw_steer

        if steer > 100:
            steer = 100
        if steer < -100:
            steer = -100
        steer = int(steer)

        prev_steer = steer

        motor_pair.move(PAIR, steer, velocity=dir_sign * velocity)

        if DEBUG:
            remaining_deg = target_deg - traveled
            remaining_cm = remaining_deg / max(1, _cm_to_deg(1))
            print(
                "rem_cm:", round(remaining_cm, 3),
                "yaw:", round(yaw_now, 3),
                "steer:", steer,
                "err:", round(yaw_err, 3)
            )

        await runloop.sleep_ms(15)

    motor.stop(LEFT_DRIVE, stop=stop_mode_end)
    motor.stop(RIGHT_DRIVE, stop=stop_mode_end)
    await runloop.sleep_ms(200)
    _reset_yaw(0)


# -----------------------------
# Turn (in place) 
# -----------------------------

async def turn_deg(angle_deg: float,
                velocity: int = 400,
                stop_mode: int = motor.BRAKE,
                acceleration: int = ACCEL,
                deceleration: int = DECEL):
    """
    In-place pivot by robot degrees (positive = one way, negative = the other).
    Uses track width to compute wheel rotation.
    """
    deg = _robot_deg_to_wheel_deg(angle_deg)
    steering = 100 if angle_deg > 0 else -100    # ±100 = spin in place
    await motor_pair.move_for_degrees(
        PAIR,
        deg,
        steering,
        velocity=velocity,
        stop=stop_mode,
        acceleration=acceleration,
        deceleration=deceleration
    )
    await reset_yaw()

# -----------------------------
# Turn (in place) with gyro
# -----------------------------

async def turn_deg_gyro(angle_deg: float,
                        velocity: int = 250,
                        kp: float = 2.5,
                        tolerance: float = 1.0,
                        stop_mode: int = motor.BRAKE):
    """
    In-place pivot to a target yaw angle using the gyro.
    Positive angle = clockwise, Negative angle = counter-clockwise.
    """
    _reset_yaw(0)
    target_angle = angle_deg

    while True:
        current_angle = _yaw_deg()
        error = target_angle - current_angle

        if abs(error) <= tolerance:
            motor_pair.stop(PAIR, stop=stop_mode)
            break

        # Proportional control
        turn_rate = int(error * kp)

        # Clamp the turn rate to the velocity
        turn_rate = max(-velocity, min(velocity, turn_rate))

        # Start motors to turn. Positive turn_rate = clockwise.
        #motor_pair.start(PAIR, steering=100, velocity=turn_rate)

        await runloop.sleep_ms(10) # Loop delay

    motor_pair.stop(PAIR, stop=stop_mode)
    await runloop.sleep_ms(100) # Wait for motors to physically stop
    _reset_yaw(0) # Reset yaw for the next sequential move



async def arc_turn(radius_cm: float,
                angle_deg: float,
                velocity: int = 400,
                stop_mode: int = motor.BRAKE):
    """
    Smooth arc using constant steering (approximate).
    For precise arcs, use per-wheel degrees with motor.run_for_degrees.
    """
    if radius_cm <= 0:
        return
    # Steering approximation: s ≈ (track / (2R)) * 100 (clip to [-100, 100])
    s = int(max(-100, min(100, (TRACK_W_MM / (2.0 * (radius_cm * 10.0))) * 100.0)))
    # Arc length ≈ R * theta
    arc_len_cm = abs(radius_cm * (angle_deg * pi / 180.0))
    deg = _cm_to_deg(arc_len_cm)
    steering = s if angle_deg > 0 else -s
    await motor_pair.move_for_degrees(PAIR, deg, steering, velocity=velocity, stop=stop_mode)


# -----------------------------
# Attachments (examples)
# -----------------------------
async def run_attachment_deg(which_port,
                            degrees: int,
                            velocity: int = 300,
                            stop_mode: int = motor.BRAKE):
    """Run an attachment motor by degrees (C or D typically)."""
    if(degrees > 200):
        return
    await motor.run_for_degrees(which_port, degrees, velocity, stop=stop_mode)


async def timed_attachment(which_port,
                        velocity: int = 400,
                        ms: int = 250,
                        stop_mode: int = motor.BRAKE):
    """Run an attachment motor for a fixed time (ms)."""
    await motor.run_for_time(which_port, ms, velocity=velocity, stop=stop_mode)

# -----------------------------
# Micro moves
# -----------------------------
async def nudge_cm(cm: float = 1.5, velocity: int = 250):
    """Small forward/backward bump to settle into models."""
    await drive_cm(cm, velocity=velocity)

async def micro_turn_deg(angle: float = 3.0, velocity: int = 200):
    """Tiny heading adjustment."""
    await turn_deg(angle, velocity=velocity)

async def move_attachment_deg(which_port, degrees, velocity=1000):
    """Move an attachment motor by degrees."""
    await motor.run_for_degrees(which_port, degrees, velocity=velocity)

#Set Attachment height to 2 3/4 inches, these instuctions are for attachment on the back side of the robot
async def run_mission1():
    #print(set_calibration_scale(319/300)) # Hardwood
    print(set_calibration_scale(179.7/180)) # Home mat Actual/ requested
    #print(set_calibration_scale(1.0)) # No calibration
    #await drive_cm_gyro(-190)
    #await drive_cm_gyro(190)

    await drive_cm(-190)
    await drive_cm(190)

    #for i in range(4):
        #await drive_cm(-66)
        #await turn_deg(90)


# -----------------------------
# Main program
# -----------------------------
async def main():
    await init_robot(default_speed=500)

    await run_mission1()

# Run the main loop
runloop.run(main())