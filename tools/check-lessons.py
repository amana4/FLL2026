#!/usr/bin/env python3
"""Run every code example on the Learn Python pages, outside a browser.

The lesson pages at code/learn/ contain runnable Python. On the website that code
runs in Pyodide against tools/spike-shim.py. The shim is deliberately plain
stdlib Python, so the same examples can be run here under CPython, and a typo in
a lesson fails a check instead of failing in front of a student.

Two kinds of block are collected:

  <div class="spike-run"> ... ```python ... ``` ... </div>   the Run buttons
  ??? question ...  four-space-indented ```python fence           the answers

A block whose first line is `# expect-error` is required to raise. Anything else
is required to finish cleanly.

Usage:
    python3 tools/check-lessons.py
    python3 tools/check-lessons.py code/learn/03-driving.md
"""

import asyncio
import os
import re
import sys
import traceback
import warnings

# One lesson deliberately calls a drive without `await`, to show that nothing
# happens. That is the point of the example, not a defect to report.
warnings.filterwarnings("ignore", message="coroutine .* was never awaited")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHIM = os.path.join(REPO, "tools", "spike-shim.py")
TOOLKIT = os.path.join(REPO, "code", "library", "toolkit.py")
LESSONS = os.path.join(REPO, "code", "learn")

EXPECT_ERROR = "# expect-error"

RUN_BLOCK = re.compile(
    r'<div class="spike-run"[^>]*>(.*?)</div>', re.DOTALL)
FENCE = re.compile(r"```python\n(.*?)```", re.DOTALL)
# A fence indented by four spaces, which is how the ??? answer blocks are held.
INDENTED_FENCE = re.compile(r"\n    ```python\n(.*?)\n    ```", re.DOTALL)


def dedent4(text):
    out = []
    for line in text.split("\n"):
        out.append(line[4:] if line.startswith("    ") else line)
    return "\n".join(out)


def collect(path):
    """Return a list of (label, source) for one markdown file."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    blocks = []
    for i, div in enumerate(RUN_BLOCK.findall(text), start=1):
        for fence in FENCE.findall(div):
            blocks.append(("run %d" % i, fence))

    # Answer fences live inside the details blocks, indented by four spaces. The
    # run blocks above are not indented, so there is no overlap.
    for i, fence in enumerate(INDENTED_FENCE.findall(text), start=1):
        blocks.append(("answer %d" % i, dedent4(fence)))

    return blocks


def load_shim():
    with open(SHIM, encoding="utf-8") as fh:
        src = fh.read()
    ns = {"__name__": "spike_shim"}
    exec(compile(src, SHIM, "exec"), ns)
    # The lessons import nothing, but the toolkit does `import runloop` and so
    # on, which the shim has just registered in sys.modules.
    sys.modules["spike_shim"] = type(sys)("spike_shim")
    for key, value in ns.items():
        setattr(sys.modules["spike_shim"], key, value)
    return ns


async def run_block(shim, toolkit_src, source):
    ns = {"__name__": "__main__"}
    exec(compile(toolkit_src, "toolkit.py", "exec"), ns)
    ns["sim"] = sys.modules["sim"]
    shim["begin_run"]()

    # CPython has no top-level await, so wrap the block in a coroutine. Comments
    # and blank lines survive the indent untouched.
    body = "\n".join("    " + line for line in source.split("\n"))
    wrapper = "async def __block():\n" + body + "\n    pass\n"
    exec(compile(wrapper, "<lesson>", "exec"), ns)
    await ns["__block"]()
    await shim["drain"]()


def main(argv):
    if argv:
        paths = [os.path.join(REPO, p) for p in argv]
    else:
        paths = sorted(
            os.path.join(LESSONS, name)
            for name in os.listdir(LESSONS)
            if name.endswith(".md")
        )

    shim = load_shim()
    # Keep the same limit the website uses, so a block that passes here is a
    # block a student can actually sit through.
    shim["TIME_LIMIT_S"] = 20.0
    with open(TOOLKIT, encoding="utf-8") as fh:
        toolkit_src = fh.read()

    failures = []
    checked = 0

    for path in paths:
        rel = os.path.relpath(path, REPO)
        blocks = collect(path)
        if not blocks:
            print("%-38s no code blocks" % rel)
            continue
        for label, source in blocks:
            checked += 1
            wants_error = source.lstrip().startswith(EXPECT_ERROR)
            # Reset the physical robot between blocks, or one lesson's tampering
            # leaks into the next.
            shim["sim"].set_true_wheel_diameter(62.4)
            shim["sim"].set_true_track_width(130.0)
            shim["sim"].set_drift(0.0)

            stdout = sys.stdout
            sys.stdout = open(os.devnull, "w")
            try:
                asyncio.run(run_block(shim, toolkit_src, source))
                raised = None
            except Exception as exc:  # noqa: BLE001 - a lesson may raise anything
                raised = exc
            finally:
                sys.stdout.close()
                sys.stdout = stdout

            if wants_error and raised is None:
                failures.append((rel, label, "expected an error, finished cleanly"))
            elif not wants_error and raised is not None:
                detail = "%s: %s" % (type(raised).__name__, raised)
                failures.append((rel, label, detail))

        print("%-38s %d blocks" % (rel, len(blocks)))

    print("")
    if failures:
        print("%d of %d blocks failed:" % (len(failures), checked))
        for rel, label, detail in failures:
            print("  %s  (%s)  %s" % (rel, label, detail))
        return 1
    print("all %d blocks ran" % checked)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
