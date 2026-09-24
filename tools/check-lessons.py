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
is required to finish cleanly. A run block marked data-lib="advanced" runs
against code/library/advanced.py instead of toolkit.py, as it does on the site.

Usage:
    python3 tools/check-lessons.py
    python3 tools/check-lessons.py code/learn/03-driving.md
"""

import ast
import asyncio
import inspect
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
MISSIONS = os.path.join(REPO, "tools", "spike-missions.py")
TOOLKIT = os.path.join(REPO, "code", "library", "toolkit.py")
ADVANCED = os.path.join(REPO, "code", "library", "advanced.py")
LESSONS = os.path.join(REPO, "code", "learn")

EXPECT_ERROR = "# expect-error"

RUN_BLOCK = re.compile(
    r'<div class="spike-run"([^>]*)>(.*?)</div>', re.DOTALL)
LIB_ATTR = re.compile(r'data-lib="([a-z]+)"')
FENCE = re.compile(r"```python\n(.*?)```", re.DOTALL)
# A fence indented by four spaces, which is how the ??? answer blocks are held.
INDENTED_FENCE = re.compile(r"\n    ```python\n(.*?)\n    ```", re.DOTALL)


def dedent4(text):
    out = []
    for line in text.split("\n"):
        out.append(line[4:] if line.startswith("    ") else line)
    return "\n".join(out)


def collect(path):
    """Return a list of (label, lib, source) for one markdown file."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    blocks = []
    for i, (attrs, div) in enumerate(RUN_BLOCK.findall(text), start=1):
        lib = LIB_ATTR.search(attrs)
        lib = lib.group(1) if lib else "toolkit"
        for fence in FENCE.findall(div):
            blocks.append(("run %d" % i, lib, fence))

    # Answer fences live inside the details blocks, indented by four spaces. The
    # run blocks above are not indented, so there is no overlap. An answer uses
    # whichever library the page's run blocks use.
    page_lib = "advanced" if 'data-lib="advanced"' in text else "toolkit"
    for i, fence in enumerate(INDENTED_FENCE.findall(text), start=1):
        blocks.append(("answer %d" % i, page_lib, dedent4(fence)))

    return blocks


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
    # The shim registers the pretend hub modules in sys.modules as it runs, which
    # is what lets the toolkit's `import runloop` work. The mission models attach
    # to it afterwards, exactly as tools/spike-sim.js does in the browser.
    shim = _as_module("spike_shim", SHIM)
    missions = _as_module("spike_missions", MISSIONS)
    field = missions.install(shim)
    return shim, field


async def run_block(shim, field, lib_name, lib_src, source):
    ns = {"__name__": "__main__"}
    exec(compile(lib_src, lib_name, "exec"), ns)
    ns["sim"] = sys.modules["sim"]
    ns["field"] = field
    shim.begin_run()

    # Run the block at the top level with await allowed, the way Pyodide's
    # eval_code_async does. So `DEBUG = True` in a block changes the library's
    # DEBUG here too, instead of making a local variable nobody reads.
    code = compile(source, "<lesson>", "exec",
                   flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
    result = eval(code, ns)
    if inspect.iscoroutine(result):
        await result
    await shim.drain()
    shim.end_run()


def main(argv):
    if argv:
        paths = [os.path.join(REPO, p) for p in argv]
    else:
        paths = sorted(
            os.path.join(LESSONS, name)
            for name in os.listdir(LESSONS)
            if name.endswith(".md")
        )

    shim, field = load_shim()
    # Keep the same limit the website uses, so a block that passes here is a
    # block a student can actually sit through.
    shim.TIME_LIMIT_S = 20.0
    libs = {}
    for name, path in (("toolkit", TOOLKIT), ("advanced", ADVANCED)):
        with open(path, encoding="utf-8") as fh:
            libs[name] = (os.path.basename(path), fh.read())

    failures = []
    checked = 0

    for path in paths:
        rel = os.path.relpath(path, REPO)
        blocks = collect(path)
        if not blocks:
            print("%-38s no code blocks" % rel)
            continue
        for label, lib, source in blocks:
            checked += 1
            wants_error = source.lstrip().startswith(EXPECT_ERROR)
            # Reset the physical robot between blocks, or one lesson's tampering
            # leaks into the next.
            shim.sim.set_true_wheel_diameter(62.4)
            shim.sim.set_true_track_width(130.0)
            shim.sim.set_drift(0.0)
            field.reset(seed=1)

            stdout = sys.stdout
            sys.stdout = open(os.devnull, "w")
            try:
                asyncio.run(run_block(shim, field, *libs[lib], source))
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
