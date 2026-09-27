#!/usr/bin/env python3
"""Run code/library/advanced.py against the pretend hub, outside a browser.

tools/check-lessons.py only runs the lesson examples, and only lesson 10 loads
the advanced library. This drives the library itself.

It drives each simulator-safe function and checks where the robot ended up, so
a typo or a runaway loop fails a check here instead of failing on the table five
minutes before a match.

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
    # init_robot() also declares "here is base" by zeroing these. Skipping it
    # would leak the last check's bearing into the next one.
    lib["_HEADING_BASE"] = 0.0
    lib["_YAW_LAST"] = 0.0
    lib["_YAW_TOTAL"] = 0.0

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


def log_tank(lib, calls, move=True):
    """Swap _tank for one that writes down each left-wheel speed first.

    A turn calls _tank(speed, -speed), so the left wheel is positive when the
    robot turns right and negative when it turns left. move=False jams the
    wheels: the calls are still written down, but the robot stays put.

    Returns the real _tank. Put it back in a finally block.
    """
    real = lib["_tank"]

    def logged(left, right):
        calls.append(left)
        if move:
            real(left, right)

    lib["_tank"] = logged
    return real


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
    power = 210            # 20 percent of MAX_DEG_S, in deg/s
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


@check("turn_deg(90) then turn_deg(-90) comes back to square")
async def _(shim, field, lib):
    async def out_and_back():
        await lib["turn_deg"](90)
        await lib["turn_deg"](-90)

    start, end = await drive(shim, field, lib, out_and_back())
    close(heading_error(end[2], start[2]), 0.0, 4.0, "heading")


@check("turn_deg(90) turns clockwise, near 90")
async def _(shim, field, lib):
    start, end = await drive(shim, field, lib, lib["turn_deg"](90))
    close(heading_error(end[2], start[2] + 90.0), 0.0, 5.0, "turn size")


@check("turn_deg is the gyro turn now, so -90 lands close")
async def _(shim, field, lib):
    # The old open-loop turn_deg was about 4 degrees out and slower. It was
    # deleted on 20 September 2026 and this name now means the gyro turn, which
    # is what code/learn/ teaches in 62 places.
    start, end = await drive(shim, field, lib, lib["turn_deg"](-90))
    close(heading_error(end[2], start[2] - 90.0), 0.0, 3.0, "turn size")


@check("turn_deg_gyro is the same function as turn_deg")
async def _(shim, field, lib):
    _, plain = await drive(shim, field, lib, lib["turn_deg"](45))
    _, alias = await drive(shim, field, lib, lib["turn_deg_gyro"](45))
    close(heading_error(alias[2], plain[2]), 0.0, 1.5, "heading")


@check("bearing() survives the yaw resets other moves do")
async def _(shim, field, lib):
    async def out_and_back():
        await lib["turn_deg"](90)
        await lib["drive_cm"](20)      # this zeroes the gyro internally
        # bearing() must still report about 90, not about 0
        if abs(lib["bearing"]() - 90.0) > 4.0:
            raise Failure("bearing() reads %.2f after a drive, wanted about 90"
                          % lib["bearing"]())

    await drive(shim, field, lib, out_and_back())


@check("face() is absolute, so a square does not accumulate error")
async def _(shim, field, lib):
    # Every turn lands 3 degrees short on purpose, as in code/learn/10-gyro.md.
    # This used to lean on drift alone, which leaves each side about 1 degree
    # out. That is the same size as the turn tolerance, and the pretend hub
    # runs on the wall clock, so about one run in eight turn_deg came out ahead.
    async def square(turn):
        for k in range(4):
            await lib["drive_cm"](30)
            await turn(k)

    # relative turns: each one inherits the last one's shortfall
    _, rel = await drive(shim, field, lib,
                         square(lambda k: lib["turn_deg"](90, stop_early_deg=3)),
                         drift=8.0)
    # absolute bearings: every target measured from base
    _, absolute = await drive(shim, field, lib,
                              square(lambda k: lib["face"](90 * (k + 1),
                                                           stop_early_deg=3)),
                              drift=8.0)

    rel_off = heading_error(rel[2], 0.0)
    abs_off = heading_error(absolute[2], 0.0)
    if abs_off > rel_off - 4.0:
        raise Failure("face() was not clearly better: %.2f deg against %.2f deg"
                      % (abs_off, rel_off))
    if abs_off > 5.0:
        raise Failure("face() left the square %.2f deg out, wanted under 5" % abs_off)


@check("face(0) and face(360) both take the short way home")
async def _(shim, field, lib):
    async def go(target):
        await lib["turn_deg"](90)
        await lib["face"](target)

    _, zero = await drive(shim, field, lib, go(0))
    _, full = await drive(shim, field, lib, go(360))
    close(heading_error(zero[2], 0.0), 0.0, 3.0, "face(0)")
    close(heading_error(full[2], 0.0), 0.0, 3.0, "face(360)")


@check("a half turn goes left every time, whichever side of 90 it stopped")
async def _(shim, field, lib):
    # face(90) stops anywhere within a degree of 90. On 26 September 2026 one
    # that stopped a little past 90 made face(-90) go right instead of left,
    # through the place where the gyro jumps from 180 to -180, and the robot
    # spun for half a minute. Which way a half turn goes must not hang on a
    # tenth of a degree.
    for landed in (89.5, 90.5):
        calls = []
        ended = []

        async def half_turn():
            await lib["face"](90)
            # Pretend the turn stopped at `landed`.
            lib["_HEADING_BASE"] += landed - lib["bearing"]()
            real = log_tank(lib, calls)
            try:
                await lib["face"](-90)
            finally:
                lib["_tank"] = real
            ended.append(lib["bearing"]())

        await drive(shim, field, lib, half_turn())
        if not calls or calls[0] > 0:
            raise Failure("from %.1f, face(-90) went right, not left" % landed)
        close(ended[0], -90.0, 1.5, "bearing after face(-90) from %.1f" % landed)


@check("four turn_deg(90) in a row count up past 180")
async def _(shim, field, lib):
    # No drive in between, so nothing zeroes the gyro, and the third turn has
    # to go past 180. The hub then says -180. Until 26 September 2026 bearing()
    # believed it, so that turn never arrived.
    seen = []

    async def four_turns():
        for _ in range(4):
            await lib["turn_deg"](90)
            seen.append(lib["bearing"]())

    start, end = await drive(shim, field, lib, four_turns())
    close(seen[-1], 360.0, 4.0, "bearing after four quarter turns")
    close(heading_error(end[2], start[2]), 0.0, 4.0, "heading after four quarter turns")


@check("a short turn across the back of the gyro stays short")
async def _(shim, field, lib):
    # face(170) then face(-170) is 20 degrees to the right. The drive zeroed the
    # gyro, so those 20 degrees take the hub's reading through 180.
    async def across():
        await lib["drive_cm"](20)
        await lib["face"](170)
        await lib["face"](-170)

    start, end = await drive(shim, field, lib, across())
    close(heading_error(end[2], start[2] + 190.0), 0.0, 3.0, "heading")


@check("a stuck turn gives up after one timeout")
async def _(shim, field, lib):
    # Jam the wheels. Once a turn has timed out, trying again only burns another
    # timeout of match time. Before 26 September 2026 it tried three times.
    calls = []
    real = log_tank(lib, calls, move=False)
    try:
        await drive(shim, field, lib, lib["face"](90, timeout_ms=600))
    finally:
        lib["_tank"] = real
    one_try = int(600 / lib["LOOP_MS"])
    if len(calls) > one_try:
        raise Failure("pushed %d times, wanted one timeout's worth, %d"
                      % (len(calls), one_try))


@check("a turn going the wrong way stops instead of spinning")
async def _(shim, field, lib):
    # The turn's half of the 20 September 2026 failure. With YAW_SIGN flipped,
    # every push takes the turn further from its target. Before 26 September
    # 2026 nothing noticed, and it spun until three timeouts ran out.
    lib["YAW_SIGN"] = -lib["YAW_SIGN"]
    try:
        start, end = await drive(shim, field, lib, lib["face"](90))
    except RuntimeError as exc:
        if "wrong way" not in str(exc):
            raise Failure("wrong message: %s" % exc)
        return
    finally:
        lib["YAW_SIGN"] = -lib["YAW_SIGN"]
    raise Failure("turned to %.0f degrees without stopping" % end[2])


@check("a slow turn stays slow")
async def _(shim, field, lib):
    # min_speed is the push that gets the wheels moving. It used to beat a slow
    # velocity asked for on purpose, so velocity=60 still turned at 126.
    calls = []
    real = log_tank(lib, calls)
    try:
        start, end = await drive(shim, field, lib, lib["face"](90, velocity=60))
    finally:
        lib["_tank"] = real
    fastest = max(abs(c) for c in calls)
    if fastest > 60:
        raise Failure("asked for 60, pushed at %.0f" % fastest)
    close(heading_error(end[2], start[2] + 90.0), 0.0, 3.0, "heading")


@check("_reset_yaw(30) moves the gyro's zero, not the bearing")
async def _(shim, field, lib):
    # Nothing calls it with anything but 0 yet. With YAW_SIGN = -1 it used to
    # set the hub to +30, which _yaw_cw() then read as -30.
    got = []

    async def rezero():
        await lib["turn_deg"](40)
        before = lib["bearing"]()
        lib["_reset_yaw"](30)
        got.append((before, lib["bearing"](), lib["_yaw_cw"]()))

    await drive(shim, field, lib, rezero())
    before, after, yaw = got[0]
    close(after, before, 0.3, "bearing across _reset_yaw(30)")
    close(yaw, 30.0, 0.3, "_yaw_cw() after _reset_yaw(30)")


@check("stop_early_deg never turns the robot the wrong way")
async def _(shim, field, lib):
    # Stopping 5 degrees early on a 2 degree turn used to aim 3 degrees the
    # other way. A turn smaller than stop_early_deg now does not happen.
    for name in ("turn_deg", "face"):
        calls = []
        real = log_tank(lib, calls)
        try:
            await drive(shim, field, lib, lib[name](2, stop_early_deg=5))
        finally:
            lib["_tank"] = real
        if any(c < 0 for c in calls):
            raise Failure("%s(2, stop_early_deg=5) turned left" % name)


@check("turn_deg(3) does not stall below the minimum power")
async def _(shim, field, lib):
    start, end = await drive(shim, field, lib, lib["turn_deg"](3))
    if heading_error(end[2], start[2]) < 0.5:
        raise Failure("a 3 degree turn did not move the robot at all")


@check("gyro_backward_deg(400, 360) terminates")
async def _(shim, field, lib):
    start, end = await drive(shim, field, lib, lib["gyro_backward_deg"](400, 360))
    if travelled(start, end) < 1.0:
        raise Failure("never moved")
    if end[1] >= start[1]:
        raise Failure("went forwards, not backwards")


@check("drive_cm_gyro is the same function as drive_cm")
async def _(shim, field, lib):
    _, plain = await drive(shim, field, lib, lib["drive_cm"](25))
    _, gyro = await drive(shim, field, lib, lib["drive_cm_gyro"](25))
    close(gyro[0], plain[0], 0.3, "x")
    close(gyro[1], plain[1], 0.3, "y")


@check("the names missions actually use are all here")
async def _(shim, field, lib):
    # The point of this file is that a mission can move between the two
    # libraries without hunting for a renamed function.
    # Not the whole of toolkit.py any more. nudge_cm, micro_turn_deg and
    # timed_attachment were dropped on 20 September 2026 because the team does
    # not use them. The lessons still teach them against toolkit.py, so a kid
    # calling nudge_cm here gets a NameError.
    expected = [
        "init_robot", "reset_yaw", "drive_cm", "drive_cm_gyro",
        "turn_deg", "turn_deg_gyro", "arc_turn", "run_attachment_deg",
        "move_attachment_deg", "calibrate_wheel_diameter",
        "set_calibration_scale", "face", "bearing",
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
                       ("drive_cm_gyro", (300,))]:
        try:
            await drive(shim, field, lib, lib[name](*args))
        except ValueError as exc:
            if "millimetres" not in str(exc):
                raise Failure("%s: wrong message: %s" % (name, exc))
        else:
            raise Failure("%s%r drove 3 metres instead of refusing" % (name, args))


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
