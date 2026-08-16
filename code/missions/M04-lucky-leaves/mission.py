"""M04 — Lucky Leaves.

Strategy and scoring: robot-game/missions/M04-lucky-leaves.md
Status: not started — build this once that page's Approach section is filled in.

The SPIKE App's Python canvas runs one self-contained file per hub slot, so it
can't import code/library/toolkit.py directly. When it's time to load this
onto the hub, paste toolkit.py's contents above the import line below (or use
whatever local tooling replaces this note once one exists).
"""
from library.toolkit import init_robot, drive_cm, drive_cm_gyro, turn_deg, run_attachment_deg
import runloop


async def run():
    # TODO: build once the approach for M04 is designed
    pass


async def main():
    await init_robot()
    await run()


runloop.run(main())
