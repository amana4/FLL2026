#!/usr/bin/env python3
"""Run code/library/advanced.py against the pretend hub, outside a browser.

tools/check-lessons.py only looks at code/learn/ and only ever loads
code/library/toolkit.py, so nothing exercises the advanced library. This does.

It drives each simulator-safe function and checks where the robot ended up, so
a typo or a runaway loop fails a check here instead of failing on the table five
minutes before a match.

The two line-following functions cannot be checked. The pretend hub has no
colour sensor, so all this can confirm is that they refuse politely.

Usage:
    python3 tools/check-library.py
"""

import asyncio
import math
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHIM = os.path.join(REPO, "tools", "spike-shim.py")
MISSIONS = os.path.join(REPO, "tools", "spike-missions.py")
LIBRARY = os.path.join(REPO, "code", "library", "advanced.py")


def _as_module(name, path):
    """Run a file and hand it back as a module, the way the website's loader does."""
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    ns = {"__name__": name}
    exec(compile(src, path, "exec"), ns)
    module = type(sys)(name)
    for key, value in ns.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


def load_shim():
    shim = _as_module("spike_shim", SHIM)
    missions = _as_module("spike_missions", MISSIONS)
    field = missions.install(shim)
    return shim, field


def load_library():
    """Exec the library into its own namespace, the way the SPIKE App would."""
    with open(LIBRARY, encoding="utf-8") as fh:
        src = fh.read()
    ns = {"__name__": "advanced"}
    exec(compile(src, LIBRARY, "exec"), ns)
    return ns


class Failure(Exception):
    pass


def close(got, want, tol, what):
    if abs(got - want) > tol:
        raise Failure("%s: got %.2f, wanted %.2f plus or minus %.2f"
                      % (what, got, want, tol))


def heading_error(got, want):
    """Smallest angle between two headings, in degrees."""
    return abs((got - want + 180.0) % 360.0 - 180.0)


async def drive(shim, field, lib, coro, drift=0.0):
    """Reset the robot, run one coroutine, and return the pose it ended at."""
    shim.sim.set_true_wheel_diameter(62.4)
    shim.sim.set_true_track_width(130.0)
    shim.sim.set_drift(drift)
    field.reset(seed=1)
    shim.begin_run()
    # field.reset() unpairs the motors, so pair them again. On the hub this is
    # what init_robot() does, but that also sleeps, which would skew the pose.
    lib["motor_pair"].pair(lib["PAIR"], lib["LEFT_DRIVE"], lib["RIGHT_DRIVE"])
    # init_robot() also declares "here is base" by zeroing this. Skipping it
    # would leak the last check's bearing into the next one.
    lib["_HEADING_BASE"] = 0.0

    start = shim.sim.pose()
    stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")
    try:
        await coro
        await shim.drain()
    finally:
        sys.stdout.close()
        sys.stdout = stdout
    shim.end_run()
    return start, shim.sim.pose()


def travelled(start, end):
    """How far the robot moved, in cm, ignoring which way."""
    return math.hypot(end[0] - start[0], end[1] - start[1])


def sideways(start, end):
    """How far the robot moved across its starting heading, in cm.

    The robot starts pointing along +y, so that is the x difference.
    """
    return end[0] - start[0]


async def detect_yaw_sign(shim, field, lib):
    """Check the library's YAW_SIGN against the pretend gyro.

    This is the software twin of bench_check_yaw_sign(). The question it used to
    settle is now settled: on 20 September 2026 the hub was measured, and it
    counts yaw up ANTICLOCKWISE, so YAW_SIGN is -1.

    That agrees with tools/spike-shim.py:182-193 and toolkit.py:223. It means
    Advanced-Coding-26.llsp3 and Gyro-Drive-Straight both have the sign wrong.

    So this no longer overrides anything. If the library and the simulator ever
    disagree again, that is a failure, not a note.
    """
    shim.sim.set_drift(0.0)
    field.reset(seed=1)
    shim.begin_run()

    lib["motor_pair"].pair(lib["PAIR"], lib["LEFT_DRIVE"], lib["RIGHT_DRIVE"])
    lib["_reset_yaw"](0)
    await shim.runloop.sleep_ms(50)

    before = lib["_yaw_deg"]()
    power = lib["_pct_to_deg_s"](20)
    lib["_tank"](power, -power)          # clockwise, by definition of _tank
    await shim.runloop.sleep_ms(400)
    lib["motor_pair"].stop(lib["PAIR"])
    await shim.runloop.sleep_ms(50)
    after = lib["_yaw_deg"]()

    turned = shim.sim.pose()[2]
    shim.end_run()

    change = (after - before + 180.0) % 360.0 - 180.0
    if heading_error(turned, 0.0) < 5.0:
        raise Failure("_tank did not turn the robot at all")
    return (+1 if change > 0 else -1), change, turned


CHECKS = []


def check(name):
    def wrap(fn):
        CHECKS.append((name, fn))
        return fn
    return wrap


@check("drive_cm(30) drives 28.6 cm straight")
async def _(shim, field, lib):
    # 28.6 and not 30: drive_cm subtracts STOP_COMP_FWD_CM, because on the
    # real hub the robot coasts that last 1.4 cm after the brake. The pretend
    # hub stops dead, so here the shortfall shows up as a real shortfall.
    start, end = await drive(shim, field, lib, lib["drive_cm"](30))
    close(travelled(start, end), 30.0 - lib["STOP_COMP_FWD_CM"], 1.0, "distance")
    close(heading_error(end[2], start[2]), 0.0, 1.0, "heading drift")


@check("drive_cm(30) holds its line against drift")
async def _(shim, field, lib):
    start, end = await drive(shim, field, lib, lib["drive_cm"](30), drift=8.0)
    if abs(sideways(start, end)) > 1.5:
        raise Failure("drifted %.2f cm sideways, wanted under 1.5"
                      % sideways(start, end))


@check("drive_cm(-30) drives 28.5 cm back")
async def _(shim, field, lib):
    start, end = await drive(shim, field, lib, lib["drive_cm"](-30))
    close(travelled(start, end), 30.0 - lib["STOP_COMP_REV_CM"], 1.0, "distance")
    if end[1] >= start[1]:
        raise Failure("went forwards, not backwards")


@check("forward then backward returns to the start")
async def _(shim, field, lib):
    async def there_and_back():
        await lib["drive_cm"](40)
        await lib["drive_cm"](-40)

    start, end = await drive(shim, field, lib, there_and_back())
    # Each leg loses its own stop compensation, so it lands about 3 cm short.
    if travelled(start, end) > 4.0:
        raise Failure("ended %.2f cm from where it started" % travelled(start, end))


@check("turn_deg_gyro(90) then turn_deg_gyro(-90) comes back to square")
async def _(shim, field, lib):
    async def out_and_back():
        await lib["turn_deg_gyro"](90)
        await lib["turn_deg_gyro"](-90)

    start, end = await drive(shim, field, lib, out_and_back())
    close(heading_error(end[2], start[2]), 0.0, 4.0, "heading")


@check("turn_deg_gyro(90) turns clockwise, near 90")
async def _(shim, field, lib):
    start, end = await drive(shim, field, lib, lib["turn_deg_gyro"](90))
    close(heading_error(end[2], start[2] + 90.0), 0.0, 5.0, "turn size")


@check("turn_deg(-90) lands inside its own tolerance")
async def _(shim, field, lib):
    start, end = await drive(shim, field, lib, lib["turn_deg"](-90))
    close(heading_error(end[2], start[2] - 90.0), 0.0, 8.0, "turn size")


@check("bearing() survives the yaw resets other moves do")
async def _(shim, field, lib):
    async def out_and_back():
        await lib["turn_deg_gyro"](90)
        await lib["drive_cm"](20)      # this zeroes the gyro internally
        # bearing() must still report about 90, not about 0
        if abs(lib["bearing"]() - 90.0) > 4.0:
            raise Failure("bearing() reads %.2f after a drive, wanted about 90"
                          % lib["bearing"]())

    await drive(shim, field, lib, out_and_back())


@check("face() is absolute, so a square does not accumulate error")
async def _(shim, field, lib):
    async def square(turn):
        for k in range(4):
            await lib["drive_cm"](30)
            await turn(k)

    # relative turns: each one inherits the last one's shortfall
    _, rel = await drive(shim, field, lib,
                         square(lambda k: lib["turn_deg"](90)), drift=8.0)
    # absolute bearings: every target measured from base
    _, absolute = await drive(shim, field, lib,
                              square(lambda k: lib["face"](90 * (k + 1))), drift=8.0)

    rel_off = heading_error(rel[2], 0.0)
    abs_off = heading_error(absolute[2], 0.0)
    if abs_off >= rel_off:
        raise Failure("face() was no better: %.2f deg against %.2f deg"
                      % (abs_off, rel_off))
    if abs_off > 4.0:
        raise Failure("face() left the square %.2f deg out, wanted under 4" % abs_off)


@check("face(0) and face(360) both take the short way home")
async def _(shim, field, lib):
    async def go(target):
        await lib["turn_deg_gyro"](90)
        await lib["face"](target)

    _, zero = await drive(shim, field, lib, go(0))
    _, full = await drive(shim, field, lib, go(360))
    close(heading_error(zero[2], 0.0), 0.0, 3.0, "face(0)")
    close(heading_error(full[2], 0.0), 0.0, 3.0, "face(360)")


@check("turn_deg_gyro(3) does not stall below the minimum power")
async def _(shim, field, lib):
    start, end = await drive(shim, field, lib, lib["turn_deg_gyro"](3))
    if heading_error(end[2], start[2]) < 0.5:
        raise Failure("a 3 degree turn did not move the robot at all")


@check("gyro_backward_deg(50, 360) terminates")
async def _(shim, field, lib):
    start, end = await drive(shim, field, lib, lib["gyro_backward_deg"](50, 360))
    if travelled(start, end) < 1.0:
        raise Failure("never moved")
    if end[1] >= start[1]:
        raise Failure("went forwards, not backwards")


@check("the palette aliases do the same thing as the toolkit names")
async def _(shim, field, lib):
    # Not exactly the same: the simulator steps on real time, so the loop can
    # overshoot its target by up to one 15 ms tick. That is about 0.3 cm at
    # these speeds, and it varies between two runs of the same function.
    _, plain = await drive(shim, field, lib, lib["drive_cm"](25))
    _, alias = await drive(shim, field, lib, lib["forward"](25))
    close(alias[0], plain[0], 0.3, "x")
    close(alias[1], plain[1], 0.3, "y")

    _, plain = await drive(shim, field, lib, lib["drive_cm"](-25))
    _, alias = await drive(shim, field, lib, lib["backward"](25))
    close(alias[0], plain[0], 0.3, "x")
    close(alias[1], plain[1], 0.3, "y")

    _, plain = await drive(shim, field, lib, lib["turn_deg_gyro"](45))
    _, alias = await drive(shim, field, lib, lib["right_pid"](45))
    close(heading_error(alias[2], plain[2]), 0.0, 1.5, "heading")

    _, plain = await drive(shim, field, lib, lib["turn_deg"](-45))
    _, alias = await drive(shim, field, lib, lib["left_simple"](45))
    close(heading_error(alias[2], plain[2]), 0.0, 1.5, "heading")


@check("drive_cm_gyro is the same function as drive_cm")
async def _(shim, field, lib):
    _, plain = await drive(shim, field, lib, lib["drive_cm"](25))
    _, gyro = await drive(shim, field, lib, lib["drive_cm_gyro"](25))
    close(gyro[0], plain[0], 0.3, "x")
    close(gyro[1], plain[1], 0.3, "y")


@check("every toolkit.py public name exists here too")
async def _(shim, field, lib):
    # The point of this file is that a mission can move between the two
    # libraries without hunting for a renamed function.
    expected = [
        "init_robot", "reset_yaw", "drive_cm", "drive_cm_gyro",
        "turn_deg", "turn_deg_gyro", "arc_turn", "run_attachment_deg",
        "timed_attachment", "move_attachment_deg", "nudge_cm",
        "micro_turn_deg", "calibrate_wheel_diameter", "set_calibration_scale",
        "face", "bearing",
    ]
    missing = [name for name in expected if name not in lib]
    if missing:
        raise Failure("missing from advanced.py: %s" % ", ".join(missing))


@check("short moves still move")
async def _(shim, field, lib):
    # Stop compensation is 1.4 cm at full cruise. Subtracted flat, as the blocks
    # did, it eats a 1.5 cm nudge and stops a 1 cm move happening at all. It
    # scales with speed and is capped at a quarter of the move.
    for asked in (1.0, 1.5, 5.0):
        start, end = await drive(shim, field, lib, lib["drive_cm"](asked))
        moved = travelled(start, end)
        if moved < asked * 0.7:
            raise Failure("asked %.1f cm, moved only %.2f cm" % (asked, moved))


@check("a wrong YAW_SIGN stops instead of spinning")
async def _(shim, field, lib):
    # This is the 20 September 2026 failure, reproduced on purpose. With the
    # sign inverted the heading loop pushes the wrong way, and without the
    # RUNAWAY_DEG guard the robot spins until the distance counter fills up.
    # _drive_degrees() averages abs() of both encoders, so a spin reads as
    # forward progress and the drive never notices.
    #
    # Needs drift to reproduce. Positive feedback amplifies an error, and with a
    # perfect simulator and no drift the error stays exactly 0, so there is
    # nothing to amplify. On the real robot, mismatched motors seed it.
    lib["YAW_SIGN"] = -lib["YAW_SIGN"]
    try:
        start, end = await drive(shim, field, lib, lib["drive_cm"](44),
                                 drift=8.0)
    except RuntimeError as exc:
        if "off course" not in str(exc):
            raise Failure("wrong message: %s" % exc)
        return
    finally:
        lib["YAW_SIGN"] = -lib["YAW_SIGN"]
    raise Failure("spun to %.0f degrees without stopping"
                  % heading_error(end[2], start[2]))


@check("millimetres typed into a centimetres argument is refused")
async def _(shim, field, lib):
    for name, args in [("drive_cm", (300,)), ("drive_cm", (-300,)),
                       ("forward", (300,)), ("backward", (300,))]:
        try:
            await drive(shim, field, lib, lib[name](*args))
        except ValueError as exc:
            if "millimetres" not in str(exc):
                raise Failure("%s: wrong message: %s" % (name, exc))
        else:
            raise Failure("%s%r drove 3 metres instead of refusing" % (name, args))


@check("line_square refuses politely with no colour sensor")
async def _(shim, field, lib):
    if lib["_HAS_COLOUR"]:
        return
    try:
        await drive(shim, field, lib, lib["line_square"]())
    except RuntimeError as exc:
        if "real hub" not in str(exc):
            raise Failure("wrong message: %s" % exc)
        return
    raise Failure("should have refused, but ran")


@check("line_follow refuses politely with no colour sensor")
async def _(shim, field, lib):
    if lib["_HAS_COLOUR"]:
        return
    try:
        await drive(shim, field, lib, lib["line_follow"](1, 2))
    except RuntimeError as exc:
        if "real hub" not in str(exc):
            raise Failure("wrong message: %s" % exc)
        return
    raise Failure("should have refused, but ran")


async def run_all():
    shim, field = load_shim()
    shim.TIME_LIMIT_S = 20.0
    lib = load_library()

    sign, change, turned = await detect_yaw_sign(shim, field, lib)
    print("pretend gyro: turning clockwise %.1f degrees changed yaw by %.1f"
          % (turned, change))
    if sign != lib["YAW_SIGN"]:
        print("")
        print("YAW_SIGN = %+d in the library, but the gyro wants %+d."
              % (lib["YAW_SIGN"], sign))
        print("With the sign wrong, a straight drive spins instead of driving.")
        print("That happened on the hub on 20 September 2026. Fix the library,")
        print("do not override it here.")
        return 1
    print("YAW_SIGN = %+d, which matches. Measured on the hub 20 Sep 2026."
          % lib["YAW_SIGN"])
    print("")

    failures = []
    for name, fn in CHECKS:
        try:
            await fn(shim, field, lib)
        except Failure as exc:
            failures.append((name, str(exc)))
            print("FAIL  %s" % name)
        except Exception as exc:  # noqa: BLE001 - report anything the library raises
            failures.append((name, "%s: %s" % (type(exc).__name__, exc)))
            print("FAIL  %s" % name)
        else:
            print("ok    %s" % name)

    print("")
    if failures:
        print("%d of %d checks failed:" % (len(failures), len(CHECKS)))
        for name, detail in failures:
            print("  %s\n      %s" % (name, detail))
        return 1
    print("all %d checks passed" % len(CHECKS))
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(run_all()))
