#!/usr/bin/env python3
"""Build a self-contained mission file from code/library/advanced.py.

The SPIKE App's Python canvas runs one file per hub slot and cannot import a
local module. So a mission program has to carry the whole library inside it.
Copying by hand is how code/missions/M03-flip-the-rock/mission.py ended up with
a header claiming "Drive: A (left), E (right)" while its code said F and A.

This does the copy instead. Everything above the marker is replaced from
advanced.py. Everything below the marker is yours and is never touched.

    # ===== MISSION CODE BELOW. THE GENERATOR DOES NOT TOUCH THIS =====

Port assignments go *below* the marker, not above. Python runs the file top to
bottom, so reassigning LEFT_DRIVE after the library body works: every function
reads the module global when it is called, not when it is defined.

Usage:
    python3 tools/build-mission.py code/missions/M03-flip-the-rock/mission-advanced.py
    python3 tools/build-mission.py --check          # fail if any file is stale
"""

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBRARY = os.path.join(REPO, "code", "library", "advanced.py")
MISSIONS = os.path.join(REPO, "code", "missions")

MARKER = "# ===== MISSION CODE BELOW. THE GENERATOR DOES NOT TOUCH THIS ====="

BANNER = """# GENERATED FILE — do not edit above the marker.
#
# The part above the marker is a copy of code/library/advanced.py. Refresh it
# with:
#
#     python3 tools/build-mission.py %s
#
# Edit below the marker. That is where the ports and the mission live.
"""


def split_tail(path):
    """Return the part of an existing file from the marker onwards."""
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if MARKER not in text:
        return None
    return text[text.index(MARKER):]


def build(path):
    with open(LIBRARY, encoding="utf-8") as fh:
        library = fh.read()
    rel = os.path.relpath(path, REPO)
    tail = split_tail(path)
    if tail is None:
        raise SystemExit(
            "%s has no marker line. Add this, then put the ports and main() "
            "under it:\n\n%s" % (rel, MARKER))
    return (BANNER % rel) + "\n" + library.rstrip() + "\n\n\n" + tail


def targets():
    found = []
    for name in sorted(os.listdir(MISSIONS)):
        path = os.path.join(MISSIONS, name, "mission-advanced.py")
        if os.path.exists(path):
            found.append(path)
    return found


def main(argv):
    check = "--check" in argv
    paths = [os.path.join(REPO, a) for a in argv if not a.startswith("--")]
    if not paths:
        paths = targets()
    if not paths:
        print("no mission-advanced.py files found")
        return 0

    stale = []
    for path in paths:
        rel = os.path.relpath(path, REPO)
        wanted = build(path)
        with open(path, encoding="utf-8") as fh:
            current = fh.read()
        if current == wanted:
            print("%-56s up to date" % rel)
            continue
        if check:
            stale.append(rel)
            print("%-56s STALE" % rel)
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(wanted)
        print("%-56s rebuilt" % rel)

    if stale:
        print("")
        print("%d file(s) are behind code/library/advanced.py." % len(stale))
        print("Run: python3 tools/build-mission.py")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
