"""Simulated mission models for the Learn Python pages — all fifteen.

Companion to spike-shim.py. That file models a robot; this one puts the whole
BIOGLOW field on the mat for it to do, and keeps score.

Load order matters. A loader does:

    import spike_shim
    import spike_missions
    spike_missions.install(spike_shim)

after which `field` is importable from lesson code, and every physics step tests
the robot against the mission models.

WHAT IS MEASURED AND WHAT IS INVENTED
-------------------------------------
Three things are official and worth trusting:

  * Model positions, from FIRST's own diagrams. See robot-game/field-positions.md.
  * Scoring conditions and points, quoted from the rulebook via the scoresheet.
  * Which missions carry the No Equipment Constraint.

Everything about how a model *moves* is invented. No official document says which
way the root cover hinges, how far, or how hard you have to push it. So the rule
below is a plausible guess, applied uniformly:

  * get an attachment within `reach` centimetres of the model
  * then run that attachment at least `trigger_deg` degrees

Bonuses generally want more arm travel than the base condition, on the theory that
a bonus is a second action rather than the same one. That is a guess too.

Use this to practise sequencing and routing. Use the real mat to find out whether
your numbers work.
"""

import math
import random
import sys
import types

# Robot geometry, in cm, from the real robot: 18 x 18 cm.
ROBOT_HALF = 9.0
TOOL_FORWARD = 9.0
TOOL_SIDE = 6.0

# The three interchangeable docks, in cm. M13, M14 and M15 sit on these and the
# team chooses which goes where before the match.
DOCKS = {
    "mine": (189.1, 102.7),
    "farm": (101.2, 64.9),
    "city": (128.6, 10.2),
}

_shim = None


# ---------------------------------------------------------------------------
# Conditions
# ---------------------------------------------------------------------------
class Condition:
    """One tickable line on the scoresheet.

    trigger:
      "attachment"  run an attachment nearby. Most conditions.
      "contact"     drive into it. No attachment needed.
      "keep"        starts satisfied. Touching the model loses it.
      "partner"     only the opposing team can give you this. field.partner().
      "declare"     a decision made before the match. field.declare().

    needs   another condition in the same model that must be met first. That is
            how the scoresheet's bonus rows and gate rows work.
    levels  [(degrees, points), ...] for graded credit, like M05's
            "Partially 10 / Completely 20". The highest level reached wins, and
            they do not add up.
    """

    def __init__(self, key, label, points, trigger,
                 units=1, needs=None, trigger_deg=45, levels=None):
        self.key = key
        self.label = label
        self.points = points
        self.trigger = trigger
        self.units = units
        self.needs = needs
        self.trigger_deg = trigger_deg
        self.levels = levels
        self.reset()

    def reset(self):
        self.done = self.units if self.trigger == "keep" else 0
        self.level = 0
        self.travel = 0.0
        self.progress = {}

    def max_points(self):
        if self.levels:
            return max(p for _, p in self.levels)
        return self.units * self.points

    def earned(self):
        if self.levels:
            return self.levels[self.level - 1][1] if self.level else 0
        return self.done * self.points

    def satisfied(self):
        return self.level > 0 if self.levels else self.done > 0


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class Model:
    def __init__(self, key, name, x, y, conditions,
                 reach=10.0, nec=False, dock=None, note=""):
        self.key = key
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.conditions = conditions
        self.reach = reach
        self.nec = nec
        self.dock = dock
        self.note = note
        self.blocked_by_equipment = False
        self.reset()

    def reset(self):
        for c in self.conditions:
            c.reset()
        self.blocked_by_equipment = False

    def cond(self, key):
        for c in self.conditions:
            if c.key == key:
                return c
        raise KeyError("%s has no condition %r" % (self.key, key))

    def gate_open(self, c):
        return c.needs is None or self.cond(c.needs).satisfied()

    def raw_points(self):
        total = 0
        for c in self.conditions:
            if self.gate_open(c):
                total += c.earned()
        return total

    def scored_points(self):
        return 0 if self.blocked_by_equipment else self.raw_points()

    def max_points(self):
        return sum(c.max_points() for c in self.conditions)

    def status(self):
        if self.blocked_by_equipment:
            return "0 — equipment touching it at the end"
        bits = []
        for c in self.conditions:
            if c.trigger == "keep":
                bits.append("%s %s" % (c.label, "kept" if c.satisfied() else "LOST"))
            elif c.levels:
                bits.append("%s %s" % (
                    c.label, self.levels_word(c)))
            elif c.units > 1:
                bits.append("%s %d/%d" % (c.label, c.done, c.units))
            elif c.satisfied():
                bits.append(c.label + " done" if self.gate_open(c)
                            else c.label + " done but blocked")
            else:
                bits.append(c.label + " no")
        return ", ".join(bits)

    @staticmethod
    def levels_word(c):
        if not c.level:
            return "no"
        return "level %d" % c.level


class LuckyLeaves(Model):
    """M04, the only mission that can score zero for a careless approach.

    Challenge Update 01 of 2 September 2026 relaxed both constraints. The
    katydid's start is randomised, because the update says teams are not told it.
    See robot-game/missions/M04-lucky-leaves.md.
    """

    HABITAT_R = 14.0

    def __init__(self, x, y):
        Model.__init__(self, "M04", "Lucky Leaves", x, y, [
            Condition("leaves", "leaves", 10, "attachment", units=2,
                      trigger_deg=40),
            Condition("bonus", "bonus", 20, "attachment", needs="leaves",
                      trigger_deg=0),
        ], reach=10.0, nec=True, note="randomised start, and it can score zero")

    def reset(self):
        Model.reset(self)
        a = random.uniform(0, 2 * math.pi)
        r = random.uniform(0, 5.0)
        self.kx = self.x + r * math.cos(a)
        self.ky = self.y + r * math.sin(a)
        self.katydid_left_habitat = False

    def katydid_in_habitat(self):
        dx, dy = self.kx - self.x, self.ky - self.y
        return math.hypot(dx, dy) <= self.HABITAT_R

    def nudge_katydid(self, pose):
        if not _point_in_robot(self.kx, self.ky, pose, margin=1.0):
            return False
        h = math.radians(pose[2])
        self.kx += 1.2 * math.sin(h)
        self.ky += 1.2 * math.cos(h)
        if not self.katydid_in_habitat():
            self.katydid_left_habitat = True
        return True

    def raw_points(self):
        if not self.katydid_in_habitat():
            return 0
        leaves = self.cond("leaves").done
        if leaves >= 2 and not self.katydid_left_habitat:
            return 30
        return leaves * 10

    def max_points(self):
        return 30

    def status(self):
        if self.blocked_by_equipment:
            return "0 — equipment touching it at the end"
        if not self.katydid_in_habitat():
            return "0 — katydid completely outside the leaf habitat"
        leaves = self.cond("leaves").done
        bits = ["leaves %d/2" % leaves]
        if leaves >= 2:
            bits.append("bonus LOST" if self.katydid_left_habitat else "bonus kept")
        return ", ".join(bits)


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------
def _point_in_robot(mx, my, pose, margin=0.0):
    """Is a point under the robot's 18 x 18 cm footprint?"""
    rx, ry, heading = pose
    h = math.radians(heading)
    dx, dy = mx - rx, my - ry
    fwd = dx * math.sin(h) + dy * math.cos(h)
    side = dx * math.cos(h) - dy * math.sin(h)
    lim = ROBOT_HALF + margin
    return abs(fwd) <= lim and abs(side) <= lim


def _tool_points(pose):
    rx, ry, heading = pose
    h = math.radians(heading)
    fx, fy = math.sin(h), math.cos(h)
    sx, sy = math.cos(h), -math.sin(h)
    nx, ny = rx + TOOL_FORWARD * fx, ry + TOOL_FORWARD * fy
    return {
        "left": (nx - TOOL_SIDE * sx, ny - TOOL_SIDE * sy),
        "right": (nx + TOOL_SIDE * sx, ny + TOOL_SIDE * sy),
    }


# ---------------------------------------------------------------------------
# The fifteen missions
# ---------------------------------------------------------------------------
# Positions are cm from the mat's bottom-left corner, from
# robot-game/field-positions.md. Points and conditions are from the scoresheet.
# Reach and trigger degrees are guesses.
def _build():
    C = Condition
    return [
        Model("M01", "Drone Survey", 88.0, 9.2, [
            C("drone", "drone off the mat", 20, "attachment", trigger_deg=50),
            C("map", "LiDAR bonus", 10, "attachment", needs="drone",
              trigger_deg=120),
        ], reach=10.0, nec=True, note="closest to home, and carries the NEC"),

        Model("M02", "Exploding Seeds", 63.8, 55.1, [
            C("seeds", "seeds", 10, "attachment", units=3, trigger_deg=35),
        ], reach=11.0, note="three seeds, 10 each"),

        Model("M03", "Flip the Rock", 9.7, 68.0, [
            C("flag", "flag down", 20, "attachment", trigger_deg=45),
            C("rock", "rock replaced bonus", 10, "attachment", needs="flag",
              trigger_deg=140),
        ], reach=10.0, note="far left edge; the bonus is a second action"),

        LuckyLeaves(15.7, 99.0),

        Model("M05", "Reaching Roots", 40.1, 106.1, [
            C("root", "root extended", 0, "attachment",
              levels=[(40, 10), (110, 20)]),
        ], reach=11.0, nec=True,
            note="partial credit: 10 for partly, 20 for completely"),

        Model("M06", "Leafcutter Frenzy", 151.3, 106.2, [
            C("ant", "ant touching the nest", 0, "attachment", trigger_deg=30),
            C("frags", "fragments", 10, "attachment", units=4, needs="ant",
              trigger_deg=45),
        ], reach=11.0,
            note="the ant is a gate: no fragments count until it is in place"),

        Model("M07", "Humongous Fungus", 163.7, 106.2, [
            C("mycelium", "mycelium extended", 20, "attachment", trigger_deg=70),
            C("links", "connections", 10, "partner", units=2, needs="mycelium"),
        ], reach=11.0, nec=True,
            note="the bonus needs your match partner. Ask them before the round"),

        Model("M08", "Tangled", 54.3, 106.1, [
            C("vine", "vine touching the mat", 30, "contact"),
        ], reach=3.0, note="30 for one condition, the best single action on the field"),

        Model("M09", "Research Platform", 65.9, 106.1, [
            C("platform", "platform raised", 10, "attachment", trigger_deg=45),
            C("camera", "camera trap", 10, "attachment", trigger_deg=90),
            C("seed", "seed off the tree", 10, "attachment", trigger_deg=135),
        ], reach=11.0, nec=True,
            note="three independent conditions, so more arm travel scores more"),

        Model("M10a", "Fragile Microhabitats, spider", 78.3, 102.3, [
            C("spider", "spider habitat", 10, "keep"),
        ], reach=8.0, nec=True, note="starts scored — do not touch it"),

        Model("M10b", "Fragile Microhabitats, snail", 109.2, 77.3, [
            C("snail", "snail habitat", 10, "keep"),
        ], reach=8.0, nec=True, note="the other one, in the middle of the field"),

        Model("M11", "Window to the Past", 140.2, 60.5, [
            C("cover", "root cover down", 20, "attachment", trigger_deg=60),
        ], reach=10.0, note="one hinge, one condition, no NEC — the easiest start"),

        Model("M12", "Forest Elder", 192.0, 76.5, [
            C("cane", "cane raised", 20, "attachment", trigger_deg=60),
            C("tie", "support tie", 10, "attachment", needs="cane",
              trigger_deg=150),
        ], reach=10.0, nec=True, note="far right edge, a long way from home"),

        Model("M13", "Keystone Species", 0, 0, [
            C("both", "species placed and trees raised", 30, "attachment",
              trigger_deg=100),
        ], reach=10.0, dock="mine",
            note="one 30-point condition, but it needs two things done at once"),

        Model("M14", "Seeds of Renewal", 0, 0, [
            C("seeds", "seeds contained", 5, "attachment", units=4,
              trigger_deg=40),
            C("mat", "and touching the mat", 5, "attachment", units=4,
              needs="seeds", trigger_deg=90),
        ], reach=11.0, dock="city", note="4 seeds at 5, then 4 bonuses at 5"),

        Model("M15", "Biocentric Architecture", 0, 0, [
            C("canopy", "nesting canopy", 10, "attachment", trigger_deg=40),
            C("skylight", "garden skylight", 10, "attachment", trigger_deg=85),
            C("compost", "compost hatch", 10, "attachment", trigger_deg=130),
            C("env", "environmental bonus", 10, "declare"),
        ], reach=11.0, nec=True, dock="farm",
            note="the bonus depends on which dock you declared it on"),
    ]


class Field:
    def __init__(self):
        self.models = _build()
        self.on_change = None
        self.match_over = False
        self.declared = {}
        # Where M13, M14 and M15 start. `reset` puts them back here, so one
        # lesson's dock choice cannot leak into the next.
        self.default_docks = dict((m.key, m.dock) for m in self.models if m.dock)
        self._place_docks()

    def _place_docks(self):
        for m in self.models:
            if m.dock:
                m.x, m.y = DOCKS[m.dock]

    # -- setup ------------------------------------------------------------
    def by_key(self, key):
        for m in self.models:
            if m.key == key:
                return m
        raise KeyError("no mission model called %r" % key)

    def set_dock(self, mission, dock):
        """Put M13, M14 or M15 on the mine, farm or city dock.

        Three models, three docks, so this is a swap rather than a move. Whichever
        mission was already on that dock takes the vacated one. Two models cannot
        share a dock on a real field either.
        """
        if dock not in DOCKS:
            raise ValueError("dock must be one of %s" % ", ".join(sorted(DOCKS)))
        m = self.by_key(mission)
        if m.dock is None:
            raise ValueError("%s does not sit on a dock" % mission)
        if m.dock == dock:
            return
        for other in self.models:
            if other is not m and other.dock == dock:
                other.dock = m.dock
                other.x, other.y = DOCKS[other.dock]
                break
        m.dock = dock
        m.x, m.y = DOCKS[dock]
        self._changed()

    def declare(self, mission, dock):
        """Declare a before-the-match decision, as the referee records it."""
        self.declared[mission] = dock
        self._changed()

    def partner(self, connections=2):
        """Your match partner fully extends their mycelium, so M07's bonus lands."""
        m = self.by_key("M07")
        c = m.cond("links")
        c.done = max(0, min(c.units, int(connections)))
        self._changed()

    def reset(self, seed=None):
        if seed is not None:
            random.seed(seed)
        for m in self.models:
            m.reset()
            if m.dock:
                m.dock = self.default_docks[m.key]
        self._place_docks()
        self.declared = {}
        self.match_over = False
        self._changed()

    # -- the per-step test ------------------------------------------------
    def update(self):
        if _shim is None or self.match_over:
            return
        r = _shim.ROBOT
        pose = (r.x, r.y, r.heading)
        tools = _tool_points(pose)
        dt = _shim.ROBOT_STEP_DT[0]
        changed = False

        for m in self.models:
            if isinstance(m, LuckyLeaves) and m.nudge_katydid(pose):
                changed = True

            for c in m.conditions:
                if c.trigger == "keep":
                    if c.done and _point_in_robot(m.x, m.y, pose):
                        c.done = 0
                        changed = True
                    continue
                if c.trigger in ("partner", "declare"):
                    continue
                if c.trigger == "contact":
                    if c.done < c.units and _point_in_robot(m.x, m.y, pose,
                                                            margin=m.reach):
                        c.done = c.units
                        changed = True
                    continue

                # "attachment"
                if not m.gate_open(c):
                    continue
                if c.levels:
                    if c.level >= len(c.levels):
                        continue
                elif c.done >= c.units:
                    continue

                for side, port in (("left", 2), ("right", 3)):
                    if not _within(tools[side], m, m.reach):
                        c.progress[side] = 0.0
                        continue
                    moved = abs(_motor_speed(port)) * dt
                    if moved <= 0:
                        continue
                    c.progress[side] = c.progress.get(side, 0.0) + moved
                    if c.levels:
                        want = c.levels[c.level][0]
                        if c.progress[side] >= want:
                            c.level += 1
                            changed = True
                            if c.level >= len(c.levels):
                                break
                    else:
                        need = c.trigger_deg if c.trigger_deg > 0 else 1
                        while c.progress[side] >= need and c.done < c.units:
                            c.progress[side] -= need
                            c.done += 1
                            changed = True
                        if c.done >= c.units:
                            break

        if changed:
            self._changed()

    def end_match(self):
        if _shim is None:
            return
        r = _shim.ROBOT
        pose = (r.x, r.y, r.heading)
        for m in self.models:
            if m.nec:
                m.blocked_by_equipment = _point_in_robot(m.x, m.y, pose, margin=1.0)
            if m.key == "M15":
                c = m.cond("env")
                c.done = 1 if self.declared.get("M15") == m.dock else 0
        self.match_over = True
        self._changed()

    # -- results ----------------------------------------------------------
    def score(self):
        return sum(m.scored_points() for m in self.models)

    def max_score(self):
        return sum(m.max_points() for m in self.models)

    def report(self, only_scoring=False):
        print("Mission                             Points  Detail")
        for m in self.models:
            got = m.scored_points()
            if only_scoring and not got:
                continue
            print("%-4s %-30s %3d/%-3d %s"
                  % (m.key, m.name, got, m.max_points(), m.status()))
        print("%-35s %3d/%-3d" % ("TOTAL", self.score(), self.max_score()))

    def state(self):
        out = []
        for m in self.models:
            item = {"key": m.key, "name": m.name, "x": m.x, "y": m.y,
                    "points": m.scored_points(), "max": m.max_points(),
                    "reach": m.reach, "nec": m.nec,
                    "lost": any(c.trigger == "keep" and not c.satisfied()
                                for c in m.conditions)}
            if isinstance(m, LuckyLeaves):
                item["kx"] = round(m.kx, 2)
                item["ky"] = round(m.ky, 2)
                item["habitat"] = m.HABITAT_R
            out.append(item)
        return out

    def _changed(self):
        if self.on_change is not None:
            self.on_change(self.state())


def _within(tool, model, reach):
    return math.hypot(tool[0] - model.x, tool[1] - model.y) <= reach


FIELD = Field()


def _motor_speed(port):
    st = _shim.ROBOT.motors.get(int(port))
    return st["velocity"] if st else 0.0


# ---------------------------------------------------------------------------
# Wiring in
# ---------------------------------------------------------------------------
def install(shim):
    """Attach to a loaded spike_shim and publish the `field` module."""
    global _shim
    _shim = shim

    shim.step_hooks.append(FIELD.update)
    shim.end_hooks.append(FIELD.end_match)
    shim.reset_hooks.append(lambda: FIELD.reset())

    field = types.ModuleType("field")
    field.__doc__ = "The mission models on the mat. Not on the real hub."
    field.models = FIELD.models
    field.DOCKS = DOCKS
    field.reset = FIELD.reset
    field.score = FIELD.score
    field.max_score = FIELD.max_score
    field.report = FIELD.report
    field.state = FIELD.state
    field.get = FIELD.by_key
    field.set_dock = FIELD.set_dock
    field.declare = FIELD.declare
    field.partner = FIELD.partner
    field.end_match = FIELD.end_match
    sys.modules["field"] = field
    return field
