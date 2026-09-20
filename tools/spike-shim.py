"""A pretend SPIKE Prime hub, for the Learn Python pages on the team website.

The real hub modules only exist inside the LEGO Education SPIKE App. There is no
`hub`, `motor`, `motor_pair` or `runloop` in a web browser. This file builds
stand-ins with the same names and the same call signatures, registers them in
`sys.modules`, and drives a simple two-wheel robot model instead of a real one.

The point is that `code/library/toolkit.py` runs against this file unchanged.
Nothing here talks to a robot. It moves a dot on a drawing.

Deliberately plain stdlib Python, with no reference to the browser. That means
this file also runs under normal CPython, so the maths can be tested outside a
browser. `tools/spike-sim.js` supplies the drawing callback through `set_push`.

Two numbers matter and are easy to confuse:

  toolkit.WHEEL_D_MM   what the robot BELIEVES its wheels measure
  sim.true_wheel_d_mm  what the pretend wheels ACTUALLY measure

They start equal, so distances come out exact. Lesson 8 pulls them apart, which
is the whole reason calibration exists.
"""

import asyncio
import math
import sys
import time
import types

# ---------------------------------------------------------------------------
# The mat, in centimetres.
#
# Measured, not assumed. The BIOGLOW mat is about 200 x 114 cm, which is NOT the
# 236 cm the FLL table's inside width would suggest — the mat is narrower than
# the table. Two independent official documents agree:
#
#   The wireframe grid is 10 columns (A-J) of 20 cm cells, so 200 cm across, and
#   its 28.3 cm diagonal label confirms the cells are square.
#
#   The Mission Model Placement photo measures to an aspect ratio of 1.75, and
#   2000/1143 = 1.750. A 236 cm mat would measure 2.07.
#
# Survey data and the method are in robot-game/field-positions.md. Confirm with a
# tape measure on the real mat before anything depends on the last millimetre.
# ---------------------------------------------------------------------------
MAT_W_CM = 200.0
MAT_H_CM = 114.3

# Bottom-left home area, near where a real run starts.
START_X_CM = 30.0
START_Y_CM = 20.0
START_HEADING = 0.0

# A run that has not finished after this many seconds is stopped. Without this
# an endless `while True` would spin until the tab is closed.
TIME_LIMIT_S = 20.0


class SimStop(Exception):
    """Raised to end a run: the time limit, or the Stop button."""


def _wrap180(a):
    """Fold any angle into the range -180 to 180."""
    return (a + 180.0) % 360.0 - 180.0


def _now():
    return time.monotonic()


# ---------------------------------------------------------------------------
# Stop modes and port numbers. The real API uses plain integers, so these are
# plain integers too — a student who prints `port.A` sees the same 0 either way.
# ---------------------------------------------------------------------------
COAST = 0
BRAKE = 1
HOLD = 2
CONTINUE = 3
SMART_COAST = 4
SMART_BRAKE = 5

PORT_NAMES = ("A", "B", "C", "D", "E", "F")


def port_name(p):
    """Turn a port number back into its letter, for the readout."""
    try:
        return PORT_NAMES[int(p)]
    except (TypeError, ValueError, IndexError):
        return str(p)


# ---------------------------------------------------------------------------
# The robot model
# ---------------------------------------------------------------------------
class Robot:
    """A two-wheel robot on a flat mat.

    Heading is in degrees, 0 pointing up the mat, counted clockwise. That
    matches the toolkit, where `turn_deg(90)` is a quarter turn to the right.
    """

    def __init__(self):
        self.true_wheel_d_mm = 62.4
        self.true_track_w_mm = 130.0
        self.drift_deg_s = 0.0
        # Per-run, not per-reset. A lesson calling `sim.reset()` mid-program must
        # not be able to extend the watchdog or cancel a press of Stop.
        self.run_started = _now()
        self.stop_requested = False
        self.reset()

    def reset(self):
        self.x = START_X_CM
        self.y = START_Y_CM
        self.heading = START_HEADING

        # Motor shaft angles, in degrees, counted from the start of the run.
        self.left_deg = 0.0
        self.right_deg = 0.0
        self.left_zero = 0.0
        self.right_zero = 0.0

        # Gyro. `yaw_ref` is the heading at the last reset, `yaw_set` is the
        # value the yaw was reset to.
        self.yaw_ref = self.heading
        self.yaw_set = 0.0

        # The current drive command.
        self.steering = 0
        self.velocity = 0.0

        # Average wheel degrees still owed on a `move_for_degrees`, or None for
        # a command that runs until something stops it.
        self.deg_budget = None
        # Seconds still owed on a `move_for_time`, or None.
        self.time_budget = None

        # Attachment motors, keyed by port number.
        self.motors = {}

        # Which ports the drive pair uses, filled in by `motor_pair.pair`.
        self.left_port = None
        self.right_port = None
        self.paired = False

        self.last_t = _now()
        self.messages = []

    # -- helpers ----------------------------------------------------------
    def motor_state(self, p):
        p = int(p)
        if p not in self.motors:
            self.motors[p] = {"deg": 0.0, "zero": 0.0, "velocity": 0.0,
                              "deg_budget": None, "time_budget": None}
        return self.motors[p]

    def is_drive_port(self, p):
        return self.paired and int(p) in (self.left_port, self.right_port)

    def wheel_circumference_cm(self):
        return math.pi * self.true_wheel_d_mm / 10.0

    def wheel_velocities(self):
        """Split the drive command into left and right shaft speeds, deg/s.

        This is the usual LEGO steering curve. At steering 0 the wheels match.
        At 50 the inner wheel stops. At 100 it runs backwards at full speed,
        which spins the robot on the spot.
        """
        v = self.velocity
        s = self.steering
        if s > 100:
            s = 100
        if s < -100:
            s = -100
        if s >= 0:
            return v, v * (1.0 - s / 50.0)
        return v * (1.0 + s / 50.0), v

    def yaw(self):
        """Gyro reading, in degrees.

        Note the minus sign. `heading` counts clockwise, but the gyro reports
        counter-clockwise as positive. That is the convention `drive_cm_gyro`
        in the toolkit is built around: it steers by `+yaw_err * kp`, which only
        pulls the robot back towards straight if the two signs are opposite.

        Confirmed against the real hub on 20 September 2026, so this is no
        longer an assumption. code/library/advanced.py was written with the
        opposite sign, copied out of the Word Blocks, and on the robot a 44 cm
        drive spun on the spot instead of driving. That library now sets
        YAW_SIGN = -1 to agree with this file.
        """
        return _wrap180(-(self.heading - self.yaw_ref) + self.yaw_set)

    def reset_yaw(self, decidegrees=0):
        self.yaw_ref = self.heading
        self.yaw_set = float(decidegrees) / 10.0

    def off_mat(self):
        return not (0.0 <= self.x <= MAT_W_CM and 0.0 <= self.y <= MAT_H_CM)

    # -- the integrator ---------------------------------------------------
    def step(self, t=None):
        """Advance the model to time `t`.

        Called from `runloop.sleep_ms`, so simulated time and real time run
        together. A move with a budget lands exactly on its target: the final
        slice of time is shortened to fit rather than overshooting by however
        far the robot travelled between two checks.
        """
        if t is None:
            t = _now()
        dt = t - self.last_t
        self.last_t = t
        if dt <= 0:
            ROBOT_STEP_DT[0] = 0.0
            return
        # A backgrounded tab can hand back a huge gap. Do not teleport.
        if dt > 0.25:
            dt = 0.25
        ROBOT_STEP_DT[0] = dt

        self._step_drive(dt)
        self._step_attachments(dt)

    def _step_drive(self, dt):
        lv, rv = self.wheel_velocities()
        avg_rate = (abs(lv) + abs(rv)) / 2.0
        finished = False

        if self.deg_budget is not None and avg_rate > 0.0:
            max_dt = self.deg_budget / avg_rate
            if dt >= max_dt:
                dt = max_dt
                finished = True
        if self.time_budget is not None:
            if dt >= self.time_budget:
                dt = self.time_budget
                finished = True
            else:
                self.time_budget -= dt

        if dt <= 0.0:
            if finished:
                self._stop_drive()
            return

        self.left_deg += lv * dt
        self.right_deg += rv * dt
        if self.deg_budget is not None:
            self.deg_budget = max(0.0, self.deg_budget - avg_rate * dt)

        circ = self.wheel_circumference_cm()
        l_cm = lv / 360.0 * circ * dt
        r_cm = rv / 360.0 * circ * dt

        forward_cm = (l_cm + r_cm) / 2.0
        track_cm = self.true_track_w_mm / 10.0
        turn_deg = math.degrees((l_cm - r_cm) / track_cm)
        if self.velocity != 0.0:
            turn_deg += self.drift_deg_s * dt

        self.heading = (self.heading + turn_deg) % 360.0
        h = math.radians(self.heading)
        self.x += forward_cm * math.sin(h)
        self.y += forward_cm * math.cos(h)

        if finished:
            self._stop_drive()

    def _stop_drive(self):
        self.velocity = 0.0
        self.steering = 0
        self.deg_budget = None
        self.time_budget = None

    def _step_attachments(self, dt):
        for st in self.motors.values():
            if st["velocity"] == 0.0:
                continue
            slice_dt = dt
            finished = False
            rate = abs(st["velocity"])
            if st["deg_budget"] is not None and rate > 0.0:
                max_dt = st["deg_budget"] / rate
                if slice_dt >= max_dt:
                    slice_dt = max_dt
                    finished = True
            if st["time_budget"] is not None:
                if slice_dt >= st["time_budget"]:
                    slice_dt = st["time_budget"]
                    finished = True
                else:
                    st["time_budget"] -= slice_dt
            st["deg"] += st["velocity"] * slice_dt
            if st["deg_budget"] is not None:
                st["deg_budget"] = max(0.0, st["deg_budget"] - rate * slice_dt)
            if finished:
                st["velocity"] = 0.0
                st["deg_budget"] = None
                st["time_budget"] = None


ROBOT = Robot()

# The most recent physics timestep, in seconds, in a one-element list so other
# modules can read it without importing anything. tools/spike-missions.py uses it
# to work out how far an attachment motor turned during a step.
ROBOT_STEP_DT = [0.0]

# Extension points, so mission models can attach without this file knowing about
# them. See tools/spike-missions.py.
step_hooks = []      # run after every physics step
end_hooks = []       # run when a run finishes
reset_hooks = []     # run at the start of each run

# The drawing callback, supplied by tools/spike-sim.js. Left as None under
# CPython, where there is nothing to draw on.
_push = None

# Coroutines handed to `runloop.run`, drained after the student's code returns.
_pending = []


def set_push(fn):
    global _push
    _push = fn


def push():
    """Run the step hooks, then hand the current pose to whatever draws it."""
    for hook in step_hooks:
        hook()
    if _push is None:
        return
    r = ROBOT
    _push(r.x, r.y, r.heading, r.yaw(), bool(r.off_mat()))


def check_stop():
    r = ROBOT
    if r.stop_requested:
        raise SimStop("Stopped.")
    if _now() - r.run_started > TIME_LIMIT_S:
        raise SimStop(
            "The robot ran for more than %d seconds and was stopped. "
            "Look for a loop that never ends." % int(TIME_LIMIT_S)
        )


# ---------------------------------------------------------------------------
# The pretend modules
# ---------------------------------------------------------------------------
def _module(name, doc):
    m = types.ModuleType(name)
    m.__doc__ = doc
    return m


def _unknown(name, module_name):
    raise AttributeError(
        "`%s.%s` is not in the pretend hub yet, so it cannot run on this page. "
        "It may still work on the real robot in the SPIKE App."
        % (module_name, name)
    )


# -- runloop ----------------------------------------------------------------
runloop = _module("runloop", "Pretend version of the SPIKE App's runloop.")


async def _sleep_ms(ms):
    """Wait, and move the robot while waiting.

    Real time and robot time are the same here, so a 30 cm drive at 500 deg/s
    takes about a second on screen, as it would on the mat.
    """
    end = _now() + max(0.0, float(ms)) / 1000.0
    while True:
        check_stop()
        remaining = end - _now()
        if remaining <= 0.0:
            break
        await asyncio.sleep(min(0.02, remaining))
        ROBOT.step()
        push()
    ROBOT.step()
    push()


def _runloop_run(*coroutines):
    """Queue coroutines the way `runloop.run` does on the hub.

    On the hub this starts the event loop. Here the page is already running one,
    so the coroutines are collected and awaited by `drain` once the student's
    code has finished. That way both styles work: a bare `await drive_cm(30)`,
    or a full program ending in `runloop.run(main())`.
    """
    for c in coroutines:
        _pending.append(c)


async def _runloop_until(condition, timeout_ms=0):
    deadline = None if not timeout_ms else _now() + float(timeout_ms) / 1000.0
    while not condition():
        if deadline is not None and _now() >= deadline:
            return False
        await _sleep_ms(10)
    return True


runloop.sleep_ms = _sleep_ms
runloop.run = _runloop_run
runloop.until = _runloop_until


async def drain():
    """Await anything that was handed to `runloop.run`."""
    while _pending:
        await _pending.pop(0)


# -- motor ------------------------------------------------------------------
motor = _module("motor", "Pretend version of the SPIKE App's motor module.")

motor.COAST = COAST
motor.BRAKE = BRAKE
motor.HOLD = HOLD
motor.CONTINUE = CONTINUE
motor.SMART_COAST = SMART_COAST
motor.SMART_BRAKE = SMART_BRAKE
motor.READY = 0
motor.RUNNING = 1
motor.STALLED = 2


def _motor_relative_position(p):
    r = ROBOT
    if r.paired and int(p) == r.left_port:
        return int(round(r.left_deg - r.left_zero))
    if r.paired and int(p) == r.right_port:
        return int(round(r.right_deg - r.right_zero))
    st = r.motor_state(p)
    return int(round(st["deg"] - st["zero"]))


def _motor_reset_relative_position(p, position=0):
    r = ROBOT
    if r.paired and int(p) == r.left_port:
        r.left_zero = r.left_deg - position
        return
    if r.paired and int(p) == r.right_port:
        r.right_zero = r.right_deg - position
        return
    st = r.motor_state(p)
    st["zero"] = st["deg"] - position


def _motor_absolute_position(p):
    return _wrap180(_motor_relative_position(p))


def _motor_velocity(p):
    r = ROBOT
    if r.is_drive_port(p):
        lv, rv = r.wheel_velocities()
        return int(round(lv if int(p) == r.left_port else rv))
    return int(round(r.motor_state(p)["velocity"]))


def _motor_stop(p, stop=BRAKE):
    r = ROBOT
    if r.is_drive_port(p):
        r._stop_drive()
    else:
        st = r.motor_state(p)
        st["velocity"] = 0.0
        st["deg_budget"] = None
        st["time_budget"] = None
    push()


async def _motor_run_for_degrees(p, degrees, velocity=1000, stop=BRAKE,
                                 acceleration=1000, deceleration=1000):
    r = ROBOT
    degrees = int(degrees)
    if degrees == 0:
        return
    if r.is_drive_port(p):
        # One wheel of the pair. Turning a single drive wheel steers the robot,
        # so hand it to the drive model as a pivot.
        steering = 50 if int(p) == r.left_port else -50
        await _pair_move_for_degrees(motor_pair.PAIR_1, abs(degrees), steering,
                                     velocity=velocity if degrees > 0 else -velocity,
                                     stop=stop)
        return
    st = r.motor_state(p)
    st["deg_budget"] = abs(degrees)
    st["time_budget"] = None
    st["velocity"] = abs(velocity) * (1 if degrees > 0 else -1)
    while st["deg_budget"] is not None:
        await _sleep_ms(10)


async def _motor_run_for_time(p, duration, velocity=1000, stop=BRAKE,
                              acceleration=1000, deceleration=1000):
    r = ROBOT
    if r.is_drive_port(p):
        await _pair_move_for_time(motor_pair.PAIR_1, duration, 0,
                                  velocity=velocity, stop=stop)
        return
    st = r.motor_state(p)
    st["time_budget"] = max(0.0, float(duration) / 1000.0)
    st["deg_budget"] = None
    st["velocity"] = float(velocity)
    while st["time_budget"] is not None:
        await _sleep_ms(10)


def _motor_run(p, velocity=1000, acceleration=1000):
    r = ROBOT
    if r.is_drive_port(p):
        r.steering = 50 if int(p) == r.left_port else -50
        r.velocity = float(velocity)
        r.deg_budget = None
        r.time_budget = None
        return
    st = r.motor_state(p)
    st["velocity"] = float(velocity)
    st["deg_budget"] = None
    st["time_budget"] = None


motor.relative_position = _motor_relative_position
motor.reset_relative_position = _motor_reset_relative_position
motor.absolute_position = _motor_absolute_position
motor.velocity = _motor_velocity
motor.stop = _motor_stop
motor.run = _motor_run
motor.run_for_degrees = _motor_run_for_degrees
motor.run_for_time = _motor_run_for_time
motor.__getattr__ = lambda name: _unknown(name, "motor")


# -- motor_pair -------------------------------------------------------------
motor_pair = _module("motor_pair", "Pretend version of the SPIKE App's motor_pair.")

motor_pair.PAIR_1 = 0
motor_pair.PAIR_2 = 1
motor_pair.PAIR_3 = 2


def _require_pair():
    if not ROBOT.paired:
        raise RuntimeError(
            "The drive motors are not paired yet. Call `await init_robot()` "
            "first, which does `motor_pair.pair(...)` for you."
        )


def _pair_pair(pair, left, right):
    r = ROBOT
    r.left_port = int(left)
    r.right_port = int(right)
    r.paired = True
    if r.left_port == r.right_port:
        raise ValueError(
            "The left and right drive motors are both on port %s. "
            "They need two different ports." % port_name(left)
        )


def _pair_unpair(pair):
    ROBOT.paired = False


def _pair_move(pair, steering, velocity=336, acceleration=1000):
    _require_pair()
    r = ROBOT
    r.steering = int(steering)
    r.velocity = float(velocity)
    r.deg_budget = None
    r.time_budget = None


async def _pair_move_for_degrees(pair, degrees, steering, velocity=336,
                                 stop=BRAKE, acceleration=1000, deceleration=1000):
    _require_pair()
    r = ROBOT
    target = abs(int(degrees))
    if target == 0:
        return
    r.steering = int(steering)
    r.velocity = float(velocity)
    r.deg_budget = float(target)
    r.time_budget = None
    while r.deg_budget is not None:
        await _sleep_ms(10)


async def _pair_move_for_time(pair, duration, steering, velocity=336,
                              stop=BRAKE, acceleration=1000, deceleration=1000):
    _require_pair()
    r = ROBOT
    r.steering = int(steering)
    r.velocity = float(velocity)
    r.time_budget = max(0.0, float(duration) / 1000.0)
    r.deg_budget = None
    while r.time_budget is not None:
        await _sleep_ms(10)


def _pair_stop(pair, stop=BRAKE):
    _require_pair()
    ROBOT._stop_drive()
    push()


motor_pair.pair = _pair_pair
motor_pair.unpair = _pair_unpair
motor_pair.move = _pair_move
motor_pair.move_for_degrees = _pair_move_for_degrees
motor_pair.move_for_time = _pair_move_for_time
motor_pair.stop = _pair_stop
motor_pair.__getattr__ = lambda name: _unknown(name, "motor_pair")


# -- hub --------------------------------------------------------------------
hub = _module("hub", "Pretend version of the SPIKE App's hub module.")

_port = _module("hub.port", "Port numbers A to F.")
for _i, _letter in enumerate(PORT_NAMES):
    setattr(_port, _letter, _i)

_motion = _module("hub.motion_sensor", "Pretend gyro.")


def _tilt_angles():
    """Yaw, pitch and roll in tenths of a degree, as the real hub reports."""
    return (int(round(ROBOT.yaw() * 10.0)), 0, 0)


_motion.tilt_angles = _tilt_angles
_motion.reset_yaw = lambda decidegrees=0: ROBOT.reset_yaw(decidegrees)
_motion.up_face = lambda: 0
_motion.stable = lambda: True
_motion.__getattr__ = lambda name: _unknown(name, "motion_sensor")

_light_matrix = _module("hub.light_matrix", "Pretend 5 by 5 display.")


def _lm_write(text):
    ROBOT.messages.append(str(text))
    print("[display] %s" % text)


_light_matrix.write = _lm_write
_light_matrix.clear = lambda: None
_light_matrix.show_image = lambda image: print("[display] image %s" % image)
_light_matrix.__getattr__ = lambda name: _unknown(name, "light_matrix")

hub.port = _port
hub.motion_sensor = _motion
hub.light_matrix = _light_matrix
hub.__getattr__ = lambda name: _unknown(name, "hub")


# -- sim: the knobs the lessons turn --------------------------------------
sim = _module("sim", "Controls for the pretend robot. Not on the real hub.")

sim.MAT_W_CM = MAT_W_CM
sim.MAT_H_CM = MAT_H_CM
sim.SimStop = SimStop


def _sim_pose():
    """Where the robot is: x cm, y cm, heading degrees."""
    r = ROBOT
    return (round(r.x, 2), round(r.y, 2), round(r.heading, 2))


def _sim_set_true_wheel_diameter(mm):
    """Change what the pretend wheels really measure, in millimetres.

    The toolkit's own `WHEEL_D_MM` is unchanged, so this is how a real robot
    whose wheels are not what the code thinks behaves.
    """
    ROBOT.true_wheel_d_mm = float(mm)
    return ROBOT.true_wheel_d_mm


def _sim_set_true_track_width(mm):
    ROBOT.true_track_w_mm = float(mm)
    return ROBOT.true_track_w_mm


def _sim_set_drift(deg_per_s):
    """Make the robot veer while driving, in degrees per second.

    A real robot drifts because of tyre grip, battery level and floor. Set this
    to something like 8 and a plain `drive_cm` no longer ends up straight.
    """
    ROBOT.drift_deg_s = float(deg_per_s)
    return ROBOT.drift_deg_s


def _sim_reset():
    ROBOT.reset()
    push()


sim.pose = _sim_pose
sim.set_true_wheel_diameter = _sim_set_true_wheel_diameter
sim.set_true_track_width = _sim_set_true_track_width
sim.set_drift = _sim_set_drift
sim.reset = _sim_reset
sim.robot = ROBOT


# ---------------------------------------------------------------------------
# Register everything, so `from hub import port` works from here on.
# ---------------------------------------------------------------------------
sys.modules["runloop"] = runloop
sys.modules["motor"] = motor
sys.modules["motor_pair"] = motor_pair
sys.modules["hub"] = hub
sys.modules["hub.port"] = _port
sys.modules["hub.motion_sensor"] = _motion
sys.modules["hub.light_matrix"] = _light_matrix
sys.modules["sim"] = sim


def begin_run():
    """Called before each run: clear the pose and restart the watchdog.

    Loading the toolkit runs its last line, `runloop.run(main())`, which queues
    the team's own `main`. Dropping the queue here means a lesson page runs only
    what the student typed.
    """
    ROBOT.reset()
    while _pending:
        coroutine = _pending.pop(0)
        close = getattr(coroutine, "close", None)
        if close is not None:
            close()
    ROBOT.run_started = _now()
    ROBOT.last_t = _now()
    ROBOT.stop_requested = False
    for hook in reset_hooks:
        hook()
    push()


def end_run():
    """Called when a run finishes: apply any end-of-match checks."""
    for hook in end_hooks:
        hook()
    push()


def request_stop():
    ROBOT.stop_requested = True
