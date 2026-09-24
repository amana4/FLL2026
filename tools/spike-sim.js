/*
 * spike-sim.js — runnable Python on the Learn Python pages.
 *
 * What it does, in order:
 *
 *   1. Finds every <div class="spike-run"> on the page and takes the fenced
 *      code inside it as the starting program.
 *   2. Replaces it with an editor, a Run button, a top-down view of the mat and
 *      an output panel.
 *   3. On the first Run, downloads Pyodide (CPython built for the browser),
 *      loads tools/spike-shim.py to stand in for the hub, then loads the team's
 *      real code/library/toolkit.py on top of it. A block marked
 *      data-lib="advanced" gets code/library/advanced.py instead.
 *   4. Runs what the student typed and animates the result.
 *
 * The code in the markdown stays in the page, hidden on screen and visible when
 * printed. So a page still reads correctly with no JavaScript, on paper, and
 * before the 8 MB download finishes.
 *
 * Only one program runs at a time. There is a single interpreter shared by every
 * block on the page, and the robot is reset before each run.
 */

(function () {
  "use strict";

  // Pinned on purpose. Bump it deliberately and re-test both a plain drive and
  // drive_cm_gyro afterwards, because a Pyodide upgrade can change asyncio
  // timing and the gyro loop is sensitive to it.
  var PYODIDE_VERSION = "v0.26.4";
  var PYODIDE_BASE = "https://cdn.jsdelivr.net/pyodide/" + PYODIDE_VERSION + "/full/";

  var SCRIPT_URL = document.currentScript ? document.currentScript.src : "";
  var SITE_ROOT = SCRIPT_URL ? new URL("../", SCRIPT_URL).href : "/";

  // Mat and robot geometry, all in centimetres. These are measured numbers, not
  // guesses — see robot-game/field-positions.md for where each one comes from.
  // The mat is 200 cm wide, not the 236 cm the table's inside width suggests.
  var MAT_W_CM = 200.0;
  var MAT_H_CM = 114.3;
  var CELL_CM = 20; // the official wireframe: columns A-J, rows 1-6
  var HOME_R_CM = 48; // both home areas, quarter-circles on the bottom corners
  var ROBOT_L_CM = 18;
  var ROBOT_W_CM = 18;

  // The three lines printed on the mat, for line following and squaring up.
  // Bounding boxes measured off the wireframe grid.
  var MAT_LINES = [
    { x: 59.9, y: 87.7, w: 30.4, h: 9.6 },
    { x: 149.8, y: 89.1, w: 36.1, h: 11.1 },
    { x: 97.5, y: 36.2, w: 8.3, h: 12.9 }
  ];

  // ---------------------------------------------------------------------
  // The shared interpreter
  // ---------------------------------------------------------------------
  var pyodide = null;
  var bootPromise = null;
  var active = null; // the block currently running

  function fetchText(url) {
    return fetch(url, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) {
        throw new Error("Could not load " + url + " (" + r.status + ")");
      }
      return r.text();
    });
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = function () {
        reject(new Error("Could not load " + src));
      };
      document.head.appendChild(s);
    });
  }

  // The Python side of the harness. Loads the shim, keeps both library sources,
  // and gives JavaScript one function to call per run.
  var DRIVER = [
    "import sys, json",
    "from pyodide.code import eval_code_async",
    "",
    "_shim = sys.modules['spike_shim']",
    "_missions = sys.modules['spike_missions']",
    "_field = _missions.install(_shim)",
    "_shim.set_push(_spike_push)",
    "_missions.FIELD.on_change = lambda state: _spike_models(json.dumps(state))",
    "",
    "async def _spike_run(user_code, lib):",
    "    ns = {'__name__': '__main__'}",
    "    if lib == 'advanced':",
    "        exec(compile(_SPIKE_ADVANCED_SRC, 'advanced.py', 'exec'), ns)",
    "    else:",
    "        exec(compile(_SPIKE_TOOLKIT_SRC, 'toolkit.py', 'exec'), ns)",
    "    ns['sim'] = sys.modules['sim']",
    "    ns['field'] = _field",
    "    _shim.begin_run()",
    "    try:",
    "        await eval_code_async(user_code, globals=ns)",
    "        await _shim.drain()",
    "    except _shim.SimStop as stop:",
    "        print('')",
    "        print('[stopped] %s' % stop)",
    "    finally:",
    "        _shim.ROBOT._stop_drive()",
    "        _shim.end_run()",
    ""
  ].join("\n");

  function boot(onStatus) {
    if (bootPromise) {
      return bootPromise;
    }
    bootPromise = (function () {
      onStatus("Downloading Python, about 8 MB. This happens once.");
      return loadScript(PYODIDE_BASE + "pyodide.js")
        .then(function () {
          onStatus("Starting Python.");
          return window.loadPyodide({ indexURL: PYODIDE_BASE });
        })
        .then(function (py) {
          pyodide = py;
          pyodide.setStdout({
            batched: function (line) {
              if (active) {
                active.write(line + "\n");
              }
            }
          });
          pyodide.setStderr({
            batched: function (line) {
              if (active) {
                active.write(line + "\n");
              }
            }
          });
          onStatus("Loading the pretend robot.");
          return Promise.all([
            fetchText(SITE_ROOT + "tools/spike-shim.py"),
            fetchText(SITE_ROOT + "tools/spike-missions.py"),
            fetchText(SITE_ROOT + "code/library/toolkit.py"),
            fetchText(SITE_ROOT + "code/library/advanced.py")
          ]);
        })
        .then(function (sources) {
          var shimSrc = sources[0];
          var missionsSrc = sources[1];
          var toolkitSrc = sources[2];
          var advancedSrc = sources[3];

          // The shim registers the pretend hub modules in sys.modules when it
          // runs, so it has to run before the toolkit imports them. The mission
          // models attach to the shim, so they come second.
          pyodide.FS.writeFile("/spike_shim.py", shimSrc, { encoding: "utf8" });
          pyodide.FS.writeFile("/spike_missions.py", missionsSrc, { encoding: "utf8" });
          pyodide.runPython("import sys; sys.path.insert(0, '/')");
          pyodide.runPython("import spike_shim, spike_missions");

          pyodide.globals.set("_SPIKE_TOOLKIT_SRC", toolkitSrc);
          pyodide.globals.set("_SPIKE_ADVANCED_SRC", advancedSrc);
          pyodide.globals.set("_spike_push", function (x, y, heading, yaw, offMat) {
            if (active) {
              active.push(x, y, heading, yaw, offMat);
            }
          });
          pyodide.globals.set("_spike_models", function (json) {
            if (active) {
              active.setModels(json);
            }
          });
          pyodide.runPython(DRIVER);
          onStatus("");
          return pyodide;
        })
        .catch(function (err) {
          bootPromise = null;
          throw err;
        });
    })();
    return bootPromise;
  }

  // ---------------------------------------------------------------------
  // Colours, taken from the Material theme so light and dark both work
  // ---------------------------------------------------------------------
  function themeColours() {
    var s = getComputedStyle(document.body);
    function pick(name, fallback) {
      var v = s.getPropertyValue(name);
      v = v ? v.trim() : "";
      return v || fallback;
    }
    return {
      mat: pick("--md-code-bg-color", "#f5f5f5"),
      grid: pick("--md-default-fg-color--lightest", "#e0e0e0"),
      edge: pick("--md-default-fg-color--light", "#9e9e9e"),
      label: pick("--md-default-fg-color--light", "#757575"),
      robot: pick("--md-primary-fg-color", "#2e7d32"),
      trail: pick("--md-accent-fg-color", "#00897b"),
      warn: "#c62828"
    };
  }

  // ---------------------------------------------------------------------
  // One runnable block
  // ---------------------------------------------------------------------

  // Drop the ``` lines from raw fence text. Only used when md_in_html did not
  // convert the fence into a <pre>, which should not happen but is cheap to
  // survive.
  function stripFences(text) {
    var kept = [];
    var lines = (text || "").split("\n");
    for (var i = 0; i < lines.length; i++) {
      if (/^\s*```/.test(lines[i])) {
        continue;
      }
      kept.push(lines[i]);
    }
    return kept.join("\n").replace(/^\n+/, "").replace(/\s+$/, "");
  }

  function Block(host) {
    this.host = host;
    this.showView = host.getAttribute("data-view") !== "none";
    this.lib = host.getAttribute("data-lib") || "toolkit";
    this.trail = [];
    this.models = [];
    this.pose = { x: 30, y: 20, heading: 0, yaw: 0, offMat: false };
    this.running = false;
    this.build();
  }

  Block.prototype.build = function () {
    var self = this;
    var source = this.host.querySelector("pre");
    var initial = source
      ? source.textContent.replace(/\s+$/, "")
      : stripFences(this.host.textContent);
    if (source) {
      source.classList.add("spike-source-print");
    } else {
      // No <pre>, so the markdown fence inside the div was not turned into a
      // code block. Recover the source from the raw text and hide it, rather
      // than presenting an empty editor.
      this.host.setAttribute("data-spike-raw", "1");
    }

    var wrap = document.createElement("div");
    wrap.className = "spike-widget";

    this.editor = document.createElement("textarea");
    this.editor.className = "spike-editor";
    this.editor.spellcheck = false;
    this.editor.setAttribute("autocapitalize", "off");
    this.editor.setAttribute("autocorrect", "off");
    this.editor.setAttribute("aria-label", "Python program you can edit and run");
    this.editor.value = initial;
    this.initial = initial;
    wrap.appendChild(this.editor);

    var bar = document.createElement("div");
    bar.className = "spike-bar";

    this.runBtn = this.button(bar, "Run", "spike-btn-run", function () {
      self.run();
    });
    this.stopBtn = this.button(bar, "Stop", "spike-btn-stop", function () {
      self.stop();
    });
    this.stopBtn.disabled = true;
    this.button(bar, "Start again", "spike-btn-reset", function () {
      self.restore();
    });

    this.status = document.createElement("span");
    this.status.className = "spike-status";
    bar.appendChild(this.status);
    wrap.appendChild(bar);

    if (this.showView) {
      this.canvas = document.createElement("canvas");
      this.canvas.className = "spike-canvas";
      this.canvas.setAttribute("role", "img");
      this.canvas.setAttribute("aria-label", "Top-down view of the robot on the mat");
      var height = parseInt(this.host.getAttribute("data-height") || "300", 10);
      this.canvas.style.height = height + "px";
      wrap.appendChild(this.canvas);

      this.readout = document.createElement("div");
      this.readout.className = "spike-readout";
      wrap.appendChild(this.readout);
    }

    this.output = document.createElement("pre");
    this.output.className = "spike-output";
    wrap.appendChild(this.output);

    this.host.appendChild(wrap);

    this.autosize();
    this.editor.addEventListener("input", function () {
      self.autosize();
    });
    this.editor.addEventListener("keydown", function (e) {
      self.onKey(e);
    });

    if (this.showView) {
      this.resize();
      window.addEventListener("resize", function () {
        self.resize();
      });
      this.observeTheme();
    }
  };

  Block.prototype.button = function (bar, label, cls, fn) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "spike-btn " + cls;
    b.textContent = label;
    b.addEventListener("click", fn);
    bar.appendChild(b);
    return b;
  };

  Block.prototype.observeTheme = function () {
    var self = this;
    var mo = new MutationObserver(function () {
      self.draw();
    });
    mo.observe(document.body, {
      attributes: true,
      attributeFilter: ["data-md-color-scheme", "data-md-color-primary"]
    });
  };

  Block.prototype.autosize = function () {
    var lines = this.editor.value.split("\n").length;
    this.editor.rows = Math.max(4, Math.min(28, lines + 1));
  };

  // Tab inserts four spaces, Enter keeps the indentation, and Ctrl or Cmd with
  // Enter runs. A textarea does none of that on its own, and Python without
  // indentation help is miserable to type.
  Block.prototype.onKey = function (e) {
    var el = this.editor;
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      this.run();
      return;
    }
    if (e.key === "Tab") {
      e.preventDefault();
      this.insert("    ");
      return;
    }
    if (e.key === "Enter") {
      var upto = el.value.slice(0, el.selectionStart);
      var line = upto.slice(upto.lastIndexOf("\n") + 1);
      var indent = (line.match(/^[ ]*/) || [""])[0];
      if (/:\s*$/.test(line)) {
        indent += "    ";
      }
      if (indent) {
        e.preventDefault();
        this.insert("\n" + indent);
      }
    }
  };

  Block.prototype.insert = function (text) {
    var el = this.editor;
    var start = el.selectionStart;
    var end = el.selectionEnd;
    el.value = el.value.slice(0, start) + text + el.value.slice(end);
    el.selectionStart = el.selectionEnd = start + text.length;
    this.autosize();
  };

  Block.prototype.write = function (text) {
    this.output.textContent += text;
    this.output.scrollTop = this.output.scrollHeight;
  };

  Block.prototype.setStatus = function (text) {
    this.status.textContent = text;
  };

  Block.prototype.restore = function () {
    this.editor.value = this.initial;
    this.autosize();
    this.output.textContent = "";
    this.trail = [];
    this.pose = { x: 30, y: 20, heading: 0, yaw: 0, offMat: false };
    this.setStatus("");
    this.draw();
    this.updateReadout();
  };

  Block.prototype.setModels = function (json) {
    try {
      this.models = JSON.parse(json);
    } catch (e) {
      this.models = [];
    }
    this.draw();
    this.updateReadout();
  };

  Block.prototype.push = function (x, y, heading, yaw, offMat) {
    this.pose = { x: x, y: y, heading: heading, yaw: yaw, offMat: !!offMat };
    var last = this.trail[this.trail.length - 1];
    if (!last || Math.abs(last[0] - x) > 0.25 || Math.abs(last[1] - y) > 0.25) {
      this.trail.push([x, y]);
      if (this.trail.length > 4000) {
        this.trail.shift();
      }
    }
    this.draw();
    this.updateReadout();
  };

  Block.prototype.stop = function () {
    if (pyodide && this.running) {
      pyodide.runPython("import sys; sys.modules['spike_shim'].request_stop()");
    }
  };

  Block.prototype.run = function () {
    var self = this;
    if (active) {
      return;
    }
    this.output.textContent = "";
    this.trail = [];
    this.setBusy(true);
    var code = this.editor.value;

    boot(function (msg) {
      self.setStatus(msg);
    })
      .then(function () {
        active = self;
        self.setStatus("Running.");
        // The source goes across as a Python value rather than being spliced
        // into the program text, which would break the moment a student typed
        // a quote character. `_spike_run` builds a fresh namespace for it.
        pyodide.globals.set("_SPIKE_USER_CODE", code);
        pyodide.globals.set("_SPIKE_LIB", self.lib);
        return pyodide.runPythonAsync("await _spike_run(_SPIKE_USER_CODE, _SPIKE_LIB)");
      })
      .then(function () {
        self.setStatus("Finished.");
      })
      .catch(function (err) {
        self.reportError(err);
      })
      .then(function () {
        active = null;
        self.setBusy(false);
      });
  };

  Block.prototype.setBusy = function (busy) {
    this.running = busy;
    this.stopBtn.disabled = !busy;
    var all = document.querySelectorAll(".spike-btn-run");
    for (var i = 0; i < all.length; i++) {
      all[i].disabled = busy;
    }
  };

  Block.prototype.reportError = function (err) {
    var text = err && err.message ? err.message : String(err);
    var lines = text.replace(/\s+$/, "").split("\n");
    var last = lines[lines.length - 1] || "Something went wrong.";
    this.setStatus("Stopped on an error.");
    this.write("\n" + last + "\n");
    if (lines.length > 1) {
      var d = document.createElement("details");
      var s = document.createElement("summary");
      s.textContent = "Show the full error";
      var p = document.createElement("pre");
      p.textContent = text;
      d.appendChild(s);
      d.appendChild(p);
      this.output.appendChild(d);
    }
  };

  // ---------------------------------------------------------------------
  // Drawing
  // ---------------------------------------------------------------------
  Block.prototype.resize = function () {
    if (!this.canvas) {
      return;
    }
    var dpr = window.devicePixelRatio || 1;
    var w = this.canvas.clientWidth;
    var h = this.canvas.clientHeight;
    if (!w || !h) {
      return;
    }
    this.canvas.width = Math.round(w * dpr);
    this.canvas.height = Math.round(h * dpr);
    this.dpr = dpr;
    this.draw();
  };

  Block.prototype.updateReadout = function () {
    if (!this.readout) {
      return;
    }
    var p = this.pose;
    var parts = [
      "x " + p.x.toFixed(1) + " cm",
      "y " + p.y.toFixed(1) + " cm",
      "heading " + p.heading.toFixed(1) + " deg",
      "gyro " + p.yaw.toFixed(1) + " deg"
    ];
    if (this.models && this.models.length) {
      var got = 0;
      var most = 0;
      for (var i = 0; i < this.models.length; i++) {
        got += this.models[i].points;
        most += this.models[i].max;
      }
      parts.push("score " + got + "/" + most);
    }
    this.readout.textContent = parts.join("   ");
    if (p.offMat) {
      var warn = document.createElement("strong");
      warn.className = "spike-offmat";
      warn.textContent = "  off the mat";
      this.readout.appendChild(warn);
    }
  };

  Block.prototype.draw = function () {
    if (!this.canvas || !this.canvas.width) {
      return;
    }
    var ctx = this.canvas.getContext("2d");
    var dpr = this.dpr || 1;
    var W = this.canvas.width / dpr;
    var H = this.canvas.height / dpr;
    var c = themeColours();

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);

    var pad = 26;
    var scale = Math.min((W - 2 * pad) / MAT_W_CM, (H - 2 * pad) / MAT_H_CM);
    var matW = MAT_W_CM * scale;
    var matH = MAT_H_CM * scale;
    var ox = (W - matW) / 2;
    var oy = (H - matH) / 2;

    // cm on the mat to pixels on the canvas. y grows upwards on the mat and
    // downwards on a canvas, hence the subtraction.
    function px(x) {
      return ox + x * scale;
    }
    function py(y) {
      return oy + matH - y * scale;
    }

    ctx.fillStyle = c.mat;
    ctx.fillRect(ox, oy, matW, matH);

    // The official wireframe: 20 cm cells, columns A to J, rows 1 to 6. Row 6 is
    // a short band, because six 20 cm rows would be 120 cm on a 114.3 cm mat.
    ctx.strokeStyle = c.grid;
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (var gx = 0; gx <= MAT_W_CM + 0.1; gx += CELL_CM) {
      ctx.moveTo(px(gx), py(0));
      ctx.lineTo(px(gx), py(MAT_H_CM));
    }
    for (var gy = 0; gy <= MAT_H_CM; gy += CELL_CM) {
      ctx.moveTo(px(0), py(gy));
      ctx.lineTo(px(MAT_W_CM), py(gy));
    }
    ctx.stroke();

    // The three printed lines. Drawn as a reminder of where they are, not to
    // scale in shape — the sim has no colour sensor to read them yet.
    ctx.strokeStyle = c.edge;
    ctx.lineWidth = 3;
    for (var mi = 0; mi < MAT_LINES.length; mi++) {
      var L = MAT_LINES[mi];
      ctx.beginPath();
      ctx.moveTo(px(L.x - L.w / 2), py(L.y - L.h / 2));
      ctx.lineTo(px(L.x + L.w / 2), py(L.y + L.h / 2));
      ctx.stroke();
    }

    ctx.strokeStyle = c.edge;
    ctx.lineWidth = 1.5;
    ctx.strokeRect(ox, oy, matW, matH);

    // Both home areas are quarter-circles of radius 48 cm on the bottom corners.
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.arc(px(0), py(0), HOME_R_CM * scale, -Math.PI / 2, 0);
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(px(MAT_W_CM), py(0), HOME_R_CM * scale, Math.PI, Math.PI * 1.5);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.fillStyle = c.label;
    ctx.font = "11px " + (getComputedStyle(document.body).fontFamily || "sans-serif");
    ctx.textAlign = "center";
    var LETTERS = "ABCDEFGHIJ";
    for (var ci = 0; ci < LETTERS.length; ci++) {
      ctx.fillText(LETTERS[ci], px((ci + 0.5) * CELL_CM), py(0) + 15);
    }
    ctx.textAlign = "right";
    for (var ri = 0; ri < 6; ri++) {
      var mid = Math.min((ri + 0.5) * CELL_CM, (MAT_H_CM + ri * CELL_CM) / 2);
      ctx.fillText(String(ri + 1), px(0) - 6, py(mid) + 4);
    }

    if (this.trail.length > 1) {
      ctx.strokeStyle = c.trail;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(px(this.trail[0][0]), py(this.trail[0][1]));
      for (var i = 1; i < this.trail.length; i++) {
        ctx.lineTo(px(this.trail[i][0]), py(this.trail[i][1]));
      }
      ctx.stroke();
    }

    this.drawModels(ctx, px, py, scale, c);
    this.drawRobot(ctx, px, py, scale, c);
  };

  // Mission models. A dashed ring is how close an attachment has to get. Filled
  // means scored; red means a fragile model that has been disturbed.
  Block.prototype.drawModels = function (ctx, px, py, scale, c) {
    if (!this.models || !this.models.length) {
      return;
    }
    ctx.font = "10px " + (getComputedStyle(document.body).fontFamily || "sans-serif");
    ctx.textAlign = "center";

    for (var i = 0; i < this.models.length; i++) {
      var m = this.models[i];
      var scored = m.points > 0;
      var lost = m.kind === "fragile" && m.done === 0;

      ctx.strokeStyle = lost ? c.warn : scored ? c.trail : c.edge;
      ctx.fillStyle = ctx.strokeStyle;
      ctx.lineWidth = scored || lost ? 2 : 1;

      ctx.setLineDash(scored || lost ? [] : [3, 3]);
      ctx.beginPath();
      ctx.arc(px(m.x), py(m.y), Math.max(3, m.reach * scale), 0, Math.PI * 2);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.globalAlpha = 0.75;
      ctx.beginPath();
      ctx.arc(px(m.x), py(m.y), 3.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1;

      // M04 carries a katydid, which is the whole difficulty of that mission.
      if (m.kx !== undefined) {
        ctx.strokeStyle = c.label;
        ctx.setLineDash([2, 4]);
        ctx.beginPath();
        ctx.arc(px(m.x), py(m.y), m.habitat * scale, 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = c.warn;
        ctx.beginPath();
        ctx.arc(px(m.kx), py(m.ky), 4, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.fillStyle = c.label;
      ctx.fillText(m.key, px(m.x), py(m.y) - Math.max(6, m.reach * scale) - 3);
    }
  };

  Block.prototype.drawRobot = function (ctx, px, py, scale, c) {
    var p = this.pose;
    var L = ROBOT_L_CM * scale;
    var Wd = ROBOT_W_CM * scale;

    ctx.save();
    ctx.translate(px(p.x), py(p.y));
    // Heading counts clockwise from straight up the mat, which is what a canvas
    // rotation already does once the origin is at the robot.
    ctx.rotate((p.heading * Math.PI) / 180);

    ctx.fillStyle = p.offMat ? c.warn : c.robot;
    ctx.globalAlpha = 0.85;
    ctx.fillRect(-Wd / 2, -L / 2, Wd, L);
    ctx.globalAlpha = 1;

    // A nose so the direction is obvious at a glance.
    ctx.beginPath();
    ctx.moveTo(-Wd / 2, -L / 2);
    ctx.lineTo(0, -L / 2 - Wd * 0.4);
    ctx.lineTo(Wd / 2, -L / 2);
    ctx.closePath();
    ctx.fill();

    ctx.restore();
  };

  // ---------------------------------------------------------------------
  // Mount
  // ---------------------------------------------------------------------
  function mount() {
    var hosts = document.querySelectorAll(".spike-run");
    for (var i = 0; i < hosts.length; i++) {
      if (hosts[i].getAttribute("data-spike-ready")) {
        continue;
      }
      hosts[i].setAttribute("data-spike-ready", "1");
      try {
        new Block(hosts[i]);
      } catch (e) {
        // A broken widget must not take the rest of the page with it. The
        // fenced code stays visible either way.
        hosts[i].removeAttribute("data-spike-ready");
      }
    }
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    // Material's instant navigation swaps the page without a reload.
    window.document$.subscribe(mount);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
