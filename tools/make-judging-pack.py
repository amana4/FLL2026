#!/usr/bin/env python3
"""Generate the Robot Design judging pack: slides, cue cards, question sheet.

Three things, all from this one file, so they cannot drift apart:

  judging-deck.pptx and judging-deck.html
      The slides we show the judges on a laptop during our 5-minute Robot
      Design explanation. Eleven slides, in the speaking order Strategy, Robot,
      Code, Sensors, Iteration and team. Speaker notes hold each cue card.
  cue-cards.html and cue-cards.pptx
      One card per speaker. The HTML prints two to a page: cut along the dashed
      line, and hold the card while you talk. The .pptx has the same cards, one
      per half-Letter slide, to edit in PowerPoint, Keynote or Google Slides.
  judge-questions.html
      All 32 judge questions with strong answers, grouped by who leads them,
      then a one-page drill list the coach reads from.

The words come from the shared script doc (tools/create-script-docs.gs) and
section 6 and 7 of robot-design/exceeds-prep.md. If you change a fact there,
change it here too.

FILL IN THE GAPS. Some facts only the team can measure: the swap time, the
10-run results, who built and coded what. Put them in FILL below and run this
again. Until then, the slides and cards show "fill in" in orange, so a gap
cannot slip through to the day.

NAMES. The repo and the website are public, so the normal copy shows roles
only. --named reads first names from docs/team-roster.md and writes to
robot-design/private/, which .gitignore keeps out of git and mkdocs.yml keeps
off the website. It also writes judging-pack-named.zip there: the two editable
.pptx files in one file to send to the team. Share it by hand. Never commit it.

Run:
    python3 tools/make-judging-pack.py            public copy, roles only
    python3 tools/make-judging-pack.py --named    private copy, with names

Print the cue cards and the question sheet from Chrome or Safari: File, Print,
paper size Letter, scale 100%, "Background graphics" on.

The diagrams come from PNG copies in robot-design/diagrams/png/, made with
tools/svg2png.swift. The skin and the slide helpers are the same as
tools/make-exceeds-pptx.py.
"""

import base64
import html
import os
import re
import struct
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNG = os.path.join(REPO, "robot-design", "diagrams", "png")
PHOTOS = os.path.join(REPO, "robot-design", "photos")
NAMED = "--named" in sys.argv

# =============================================================================
# FILL: facts only the team can give. None shows "fill in" on every output.
# =============================================================================
FILL = {
    # The middle time of five timed swaps, for example "4 seconds".
    "swap": None,
    # Each run 10 times in a row, for example "8 / 10".
    "runs": {
        "Phase 0": None,
        "Phase 1": None,
        "Phase 2": None,
        "Phase 3": None,
        "Phase 5": None,
        "Phase 6": None,
        "Phase 7": None,
    },
    # The arm fix, before and after, for example "Before: 5 / 10. After: 9 / 10."
    "arm_result": None,
    # One thing each person built, and one thing each person coded.
    "built": {"Strategy": None, "Robot": None, "Code": None,
              "Sensors": None, "Iteration and team": None},
    "coded": {"Strategy": None, "Robot": None, "Code": None,
              "Sensors": None, "Iteration and team": None},
    # What the team is most proud of, in one sentence.
    "proud": None,
}

ROLES = ["Strategy", "Robot", "Code", "Sensors", "Iteration and team"]
# Who leads each part, by roster slot. The same as ROLE_SLOT in
# tools/make-exceeds-pptx.py and tools/create-script-docs.gs.
ROLE_SLOT = {"Strategy": "Kid 5", "Robot": "Kid 2", "Code": "Kid 1",
             "Sensors": "Kid 3", "Iteration and team": "Kid 4"}


def _roster_names():
    """Slot to first name, from the private roster. Only used with --named."""
    names = {}
    for line in open(os.path.join(REPO, "docs", "team-roster.md"), encoding="utf-8"):
        m = re.match(r"\|\s*(Kid [1-5])\s*\|\s*([^|]+?)\s*\|", line)
        if m:
            names[m.group(1)] = m.group(2)
    return names


NAMES = _roster_names() if NAMED else {}


def who(role):
    """A role as a person: the first name in the private copy."""
    return NAMES.get(ROLE_SLOT[role], "the %s lead" % role) if NAMED else "the %s lead" % role


def who_cap(role):
    w = who(role)
    return w[0].upper() + w[1:]


def label(role):
    """The heading for a role: 'Robot: <first name>' in the private copy."""
    return "%s: %s" % (role, NAMES[ROLE_SLOT[role]]) if NAMED else role


def filled(value, blank="fill in"):
    return value if value else blank


# =============================================================================
# THE FIVE PARTS: time, rubric line, what to show, cue card, handover
# =============================================================================
PARTS = {
    "Strategy": {
        "time": "0:00 to 1:10", "rubric": "IDENTIFY: mission strategy",
        "show": "Point at the mission map.",
        "cue": ["Time is our biggest limit",
                "Close missions first",
                "Phase 2: one straight push and back",
                "Robo taxi: attachment and keystone to the right",
                "Skipped Lucky Leaves: far, luck, 10 or 20 points"],
        "next": "will show you the robot.",
    },
    "Robot": {
        "time": "1:10 to 2:15", "rubric": "CREATE: attachments. IDENTIFY: resources",
        "show": "Do a live attachment swap. Hold up an old attachment next to the new one.",
        "cue": ["Six designs: blue wheels slip",
                "Flat: lines up on walls and mat lines",
                "6 ports: 2 wheels, 2 attachments, 2 colour sensors",
                "Gravity mounting: one move (do the swap)",
                "Push before motors. Arm starts on the stopper"],
        "next": "will explain our code.",
    },
    "Code": {
        "time": "2:15 to 3:00", "rubric": "CREATE: code",
        "show": "The code on the slide, the code layers picture, and the flowchart.",
        "cue": ["Python: we reused last year's drive_cm",
                "Changed the wheel size, 88 mm to 62.4 mm",
                "Layers: the run says what, the library says how",
                "45 degrees off: it stops"],
        "next": "will tell you about our sensors.",
        # A picture printed on the cue card, under the bullets.
        "figure": "drive-simple",
    },
    "Sensors": {
        "time": "3:00 to 4:00", "rubric": "CREATE: code and sensors",
        "show": "The gyro steps picture, and the gyro loop.",
        "cue": ["Only the gyroscope steers",
                "Colour sensors: plugged in, not used",
                "Yaw = the way the robot points",
                "1 zero, 2 turn, 3 drive straight",
                "Drifts 5 left: steers back right"],
        "next": "will tell you how we test, and about our team.",
    },
    "Iteration and team": {
        "time": "4:00 to 5:00",
        "rubric": "ITERATE: testing and improvements. DESIGN and COMMUNICATE: team",
        "show": "The run results slide, then the who-did-what slide.",
        "cue": ["10 runs each: say the real number",
                "Arm fix: measured, 2 ideas failed, stopper works",
                "Measure first, then fix",
                "Everyone: I built ... I coded ...",
                "Proud of ... Ask any of us anything"],
        "next": None,
    },
}


def handover(role):
    i = ROLES.index(role)
    if i + 1 == len(ROLES):
        return '"Thank you. Ask any of us anything."'
    return '"Now %s %s"' % (who(ROLES[i + 1]), PARTS[role]["next"])


# =============================================================================
# THE 32 QUESTIONS: number, question, strong answer, follow-up, team must answer
# =============================================================================
def _swap_answer():
    if FILL["swap"]:
        return "About %s. We timed five swaps and used the middle one." % FILL["swap"]
    return "Give the measured time."


def _reliability_answer():
    got = [(r, v) for r, v in FILL["runs"].items() if v]
    if got:
        return "Give the 10-run numbers: " + ", ".join("%s %s" % rv for rv in got) + "."
    return "Give the 10-run numbers."


QUESTIONS = [
    (1, "Robot", "Why is your robot shaped like that?",
     "A flat box squares up on a wall, so every run starts the same way.",
     "What if it starts crooked?", False),
    (2, "Robot", "Why those wheels?",
     "The designs that slipped all used blue SPIKE wheels, so we use grippy ones.",
     "How did you check yours don't slip?", False),
    (3, "Robot", "Where is the robot's weight?",
     "Team to measure: say where the heaviest part is, and that you checked for a wobble.",
     "How did you test it?", True),
    (4, "Robot", "How does the BOXOR frame move the arm?",
     "Two bevel gears turn the movement through 90 degrees.",
     "What is the gear ratio?", False),
    (5, "Robot", "Why gravity mounting?",
     "One move to swap. Last season, swaps were slow.",
     "Has one ever fallen off?", False),
    (6, "Robot", "How long does a swap take?", _swap_answer(),
     "How did you measure it?", not FILL["swap"]),
    (7, "Robot", "Why a push instead of a motor?",
     "Motors can go wrong. A push can't.",
     "When did you need a motor anyway?", False),
    (8, "Robot", "Why is the attachment on the back?",
     "Team to agree.",
     "Why do your distances have minus signs?", True),
    (9, "Robot", "What would you change with more time?",
     "Take the play out of the arm gears, maybe with a rubber band.",
     "How would you know it worked?", False),
    (10, "Strategy", "What is the robo taxi?",
     "One trip carries the attachment and the keystone to the right.",
     "What if the keystone falls off?", False),
    (11, "Sensors", "How does it drive straight?",
     "It reads the gyro every 15 ms and steers back, harder the further off.",
     "What stops it wiggling?", False),
    (12, "Code", "Why Python?",
     "Last year's Python, more control, and git shows every change.",
     "What was hard about switching?", False),
    (13, "Sensors", "What does face(90) do?",
     "Turns to point 90 degrees from where we started.",
     "Why not just turn 90?", False),
    (14, "Sensors", "What is PID?",
     "P pushes harder when far off, I pushes more when stuck, D eases off when "
     "closing in fast.",
     "Which parts does drive_cm use?", False),
    (15, "Sensors", "Why not the colour sensors?",
     "They're plugged in, but only the gyroscope steers. It works everywhere on "
     "the mat, not just near a line.",
     "Would a sensor have helped anywhere?", False),
    (16, "Code", "What if something goes wrong in a run?",
     "More than 45 degrees off, it stops. Over 8 seconds, it gives up and goes on.",
     "Why stop?", False),
    (17, "Code", "How are distances accurate?",
     "We asked for 180 cm and got 179, so we scale by 179/180.",
     "What if you change the wheels?", False),
    (18, "Code", "What did you reuse from last year?",
     "drive_cm. We changed the wheel size from 88 mm to 62.4 mm.",
     "Why did that number matter?", False),
    (19, "Robot", "How does the arm know where it is?",
     "It starts on its stopper, and the code calls that zero.",
     "What if it doesn't start there?", False),
    (20, "Code", "What's the cleverest thing in your code?",
     "The arm lifts while the robot drives home, by leaving out await.",
     "How much time does it save?", False),
    (21, "Strategy", "Why this order of runs?",
     "Left first, close first, then the robo taxi.",
     "What if the first run fails?", False),
    (22, "Strategy", "Which mission did you skip?",
     "Lucky Leaves: far, partly luck, 10 or 20 points.",
     "What would make it worth doing?", False),
    (23, "Iteration and team", "How reliable is your robot?", _reliability_answer(),
     "Which run is weakest?", not any(FILL["runs"].values())),
    (24, "Iteration and team", "How do you test a change?",
     "Change one thing, run it 10 times, compare.",
     "Give an example.", False),
    (25, "Iteration and team", "What broke, and how did you fix it?",
     "One fix story, four parts: problem, how we found out, what we changed, result.",
     "How did you find the cause?", False),
    (26, "Iteration and team", "What didn't work?",
     "Pushing the arm into its stopper lifted the attachment, so we dropped that idea.",
     "What did you do instead?", False),
    (27, "Iteration and team", "How do you know a fix helped?",
     "A number before and a number after.",
     "What if it only helped sometimes?", False),
    (28, "Iteration and team", "Who built and coded what?",
     "Each member answers for themselves.",
     "Explain your teammate's part.", True),
    (29, "Iteration and team", "How did you share the work?",
     "Roles, and we swapped so everyone tried each.",
     "What happened when you disagreed?", False),
    (30, "Strategy", "Whose idea was the robo taxi?",
     "The true answer.",
     "How did the team decide?", True),
    (31, "Iteration and team", "What did you learn?",
     "One real lesson each.",
     "How will you use it next season?", True),
    (32, "Iteration and team", "What are you most proud of?",
     "Said like you mean it.",
     "Why that one?", True),
]

# =============================================================================
# OUTPUT PATHS
# =============================================================================
if NAMED:
    OUT_DIR = os.path.join(REPO, "robot-design", "private")
    os.makedirs(OUT_DIR, exist_ok=True)
    SUFFIX = "-named"
else:
    OUT_DIR = os.path.join(REPO, "robot-design")
    SUFFIX = ""
OUT_PPTX = os.path.join(OUT_DIR, "judging-deck%s.pptx" % SUFFIX)
OUT_DECK = os.path.join(OUT_DIR, "judging-deck%s.html" % SUFFIX)
OUT_CARDS = os.path.join(OUT_DIR, "cue-cards%s.html" % SUFFIX)
OUT_CARDS_PPTX = os.path.join(OUT_DIR, "cue-cards%s.pptx" % SUFFIX)
OUT_QS = os.path.join(OUT_DIR, "judge-questions%s.html" % SUFFIX)
# With --named only: the editable slides and cue cards in one file to send round.
OUT_ZIP = os.path.join(OUT_DIR, "judging-pack%s.zip" % SUFFIX)

# --- BIOGLOW skin, the same as tools/make-exceeds-pptx.py ---------------------
INK = RGBColor(0x16, 0x36, 0x2B)
MUTED = RGBColor(0x4A, 0x63, 0x57)
SOFT = RGBColor(0x7D, 0x94, 0x88)
ACCENT = RGBColor(0xEB, 0x6C, 0x36)
PAPER = RGBColor(0xF5, 0xF5, 0xF5)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TINT = RGBColor(0xFC, 0xE6, 0xDC)
GREY = RGBColor(0xD8, 0xDE, 0xDA)
PALE = RGBColor(0xE7, 0xF0, 0xEB)
CODE_BG = RGBColor(0x1E, 0x2A, 0x25)
CODE_FG = RGBColor(0xE7, 0xF0, 0xEB)

# The part colours from robot-design/diagrams/speaking-order.svg.
PART_COLOUR = {"Strategy": RGBColor(0xB7, 0x79, 0x1F),
               "Robot": RGBColor(0x2B, 0x6C, 0xB0),
               "Code": RGBColor(0x1B, 0x6B, 0x47),
               "Sensors": RGBColor(0x6B, 0x46, 0xC1),
               "Iteration and team": RGBColor(0xDD, 0x6B, 0x20)}

FONT = "Trebuchet MS"
MONO = "Courier New"


def _hex(c):
    return "#" + str(c)


# =============================================================================
# THE SLIDES: each helper draws in the .pptx and writes the same shape in HTML
# =============================================================================
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
HTML_SLIDES = []
_HTML = {}


def _u(v):
    """Inches to the HTML unit. --u is one inch of the slide."""
    return "calc(%g * var(--u))" % v


def _emit(s, fragment):
    _HTML[id(s)]["parts"].append(fragment)


def slide(dark=False):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = INK if dark else PAPER
    entry = {"dark": dark, "parts": [], "notes": ""}
    HTML_SLIDES.append(entry)
    _HTML[id(s)] = entry
    return s


def text(s, txt, x, y, w, h, size=18, color=MUTED, bold=False,
         align=PP_ALIGN.LEFT, spacing=1.2, font=FONT):
    box = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(txt.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = align
        p.line_spacing = spacing
        for r in p.runs:
            r.font.name = font
            r.font.size = Pt(size)
            r.font.color.rgb = color
            r.font.bold = bold
    lines = "".join("<div>%s</div>" % (html.escape(line) or "&nbsp;")
                    for line in txt.split("\n"))
    family = "'Courier New', Menlo, monospace" if font == MONO else \
        "'Trebuchet MS', 'Segoe UI', system-ui, sans-serif"
    _emit(s, "<div class='t' style='left:%s;top:%s;width:%s;font-size:%s;"
             "color:%s;font-weight:%s;text-align:%s;line-height:%g;"
             "font-family:%s'>%s</div>"
          % (_u(x), _u(y), _u(w), _u(size / 72.0), _hex(color),
             "700" if bold else "400",
             {PP_ALIGN.CENTER: "center", PP_ALIGN.RIGHT: "right"}.get(align, "left"),
             spacing * 1.1, family, lines))
    return box


def rect(s, x, y, w, h, fill=WHITE, line=GREY, dash=False, lw=1.0):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y),
                            Inches(w), Inches(h))
    sh.adjustments[0] = 0.05
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = line
    sh.line.width = Pt(lw)
    if dash:
        sh.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    sh.shadow.inherit = False
    sh.text_frame.text = ""
    _emit(s, "<div class='r' style='left:%s;top:%s;width:%s;height:%s;"
             "background:%s;border:%s %s %s'></div>"
          % (_u(x), _u(y), _u(w), _u(h), _hex(fill), _u(lw / 72.0),
             "dashed" if dash else "solid", _hex(line)))
    return sh


def _image_size(path):
    """Pixel width and height of a PNG or JPEG, without extra libraries."""
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    i = 2
    while i < len(data):
        marker, size = data[i + 1], struct.unpack(">H", data[i + 2:i + 4])[0]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + size
    raise ValueError("cannot read image size: " + path)


def img_src(path):
    """How an HTML page points at a picture."""
    if NAMED:
        # The named copy is shared by hand as one file, so carry the pictures.
        mime = "image/jpeg" if path.lower().endswith((".jpg", ".jpeg")) else "image/png"
        with open(path, "rb") as fh:
            return "data:%s;base64,%s" % (mime, base64.b64encode(fh.read()).decode("ascii"))
    return os.path.relpath(path, OUT_DIR).replace(os.sep, "/")


def image(s, path, x, y, w, h):
    """Place a picture as big as fits in the box, centred in it."""
    pw, ph = _image_size(path)
    scale = min(w / pw, h / ph)
    iw, ih = pw * scale, ph * scale
    ix, iy = x + (w - iw) / 2, y + (h - ih) / 2
    s.shapes.add_picture(path, Inches(ix), Inches(iy), Inches(iw), Inches(ih))
    _emit(s, "<img src='%s' alt='' style='left:%s;top:%s;width:%s;height:%s'>"
          % (html.escape(img_src(path)), _u(ix), _u(iy), _u(iw), _u(ih)))


def table(s, rows, x, y, col_w, row_h=0.5, size=16):
    """A plain table. A cell that says 'fill in' turns orange."""
    w = sum(col_w)
    shape = s.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y),
                               Inches(w), Inches(row_h * len(rows)))
    t = shape.table
    for c, cw in enumerate(col_w):
        t.columns[c].width = Inches(cw)
    body = []
    for r, row in enumerate(rows):
        cells = []
        for c, val in enumerate(row):
            gap = val == "fill in"
            fill = INK if r == 0 else (TINT if gap else (WHITE if r % 2 else PALE))
            ink = WHITE if r == 0 else (ACCENT if gap else INK)
            bold = r == 0 or c == 0 or gap
            cell = t.cell(r, c)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = fill
            for p in cell.text_frame.paragraphs:
                for run in p.runs:
                    run.font.name = FONT
                    run.font.size = Pt(size)
                    run.font.bold = bold
                    run.font.color.rgb = ink
            cells.append("<td style='background:%s;color:%s;font-weight:%s'>%s</td>"
                         % (_hex(fill), _hex(ink), "700" if bold else "400",
                            html.escape(val)))
        body.append("<tr style='height:%s'>%s</tr>" % (_u(row_h), "".join(cells)))
    cols = "".join("<col style='width:%s'>" % _u(cw) for cw in col_w)
    _emit(s, "<table style='left:%s;top:%s;width:%s;font-size:%s'>"
             "<colgroup>%s</colgroup>%s</table>"
          % (_u(x), _u(y), _u(w), _u(size / 72.0), cols, "".join(body)))


def notes(s, role):
    """Speaker notes: the cue card, then the handover."""
    p = PARTS[role]
    txt = "%s, %s\n\n%s\n\nShow: %s\n\nHand over: %s" % (
        label(role), p["time"], "\n".join("- " + c for c in p["cue"]),
        p["show"], handover(role))
    s.notes_slide.notes_text_frame.text = txt
    _HTML[id(s)]["notes"] = txt


def part_slide(role, head):
    """A light slide with the part's colour bar, its name and a headline."""
    s = slide()
    colour = PART_COLOUR[role]
    rect(s, 0, 0, 0.22, 7.5, fill=colour, line=colour)
    text(s, label(role).upper(), 0.7, 0.4, 12, 0.35, size=13, color=colour, bold=True)
    text(s, head, 0.7, 0.75, 12, 1.0, size=34, color=INK, bold=True, spacing=1.05)
    notes(s, role)
    return s


def point(s, x, y, w, head, body, colour=INK, size=17):
    """A short bold line, and a sentence under it."""
    text(s, head, x, y, w, 0.45, size=size + 3, color=colour, bold=True)
    if body:
        text(s, body, x, y + 0.5, w, 0.9, size=size, color=MUTED)


def gap_box(s, x, y, w, h, prompt):
    """An orange dashed box: a fact the team still has to give."""
    rect(s, x, y, w, h, fill=TINT, line=ACCENT, dash=True, lw=1.5)
    text(s, "FILL IN BEFORE JUDGING", x + 0.2, y + 0.12, w - 0.4, 0.3, size=11,
         color=ACCENT, bold=True)
    text(s, prompt, x + 0.2, y + 0.45, w - 0.4, h - 0.55, size=15, color=INK)


def png(name):
    return os.path.join(PNG, name + ".png")


# --- 1. Title -----------------------------------------------------------------
s = slide(dark=True)
text(s, "ROBOT DESIGN  ·  FLL BIOGLOW 2026-27", 0.7, 0.55, 12, 0.35, size=13,
     color=ACCENT, bold=True)
text(s, "The Bumble Bots", 0.7, 1.0, 12, 1.0, size=54, color=WHITE, bold=True)
text(s, "One flat robot. Attachments that drop on.\nA gyroscope that keeps it straight.",
     0.7, 2.15, 12, 1.2, size=24, color=PALE)
x = 0.7
widths = [2.75, 2.45, 1.7, 2.3, 2.7]
for role, w in zip(ROLES, widths):
    rect(s, x, 4.1, w - 0.1, 1.35, fill=PART_COLOUR[role], line=PART_COLOUR[role])
    text(s, role, x + 0.15, 4.25, w - 0.4, 0.5, size=19, color=WHITE, bold=True)
    text(s, PARTS[role]["time"], x + 0.15, 4.8, w - 0.4, 0.4, size=14, color=WHITE)
    if NAMED:
        text(s, NAMES[ROLE_SLOT[role]], x + 0.15, 5.6, w - 0.4, 0.4, size=17,
             color=WHITE, bold=True)
    x += w
text(s, "Then 5 minutes of questions. Ask any of us anything.", 0.7, 6.35, 12, 0.4,
     size=16, color=SOFT)
notes(s, "Strategy")

# --- 2. Strategy: the mission map -------------------------------------------------
# The slide copy of the map: the mat alone, with big phase tags. The list on the
# right uses the same colours as the routes in tools/make-robot-diagrams.py.
RUN_COLOUR = {0: RGBColor(0x1B, 0x6B, 0x47), 1: RGBColor(0x0E, 0x7C, 0x86),
              2: RGBColor(0x6B, 0x46, 0xC1), 3: RGBColor(0xDD, 0x6B, 0x20),
              5: RGBColor(0x2B, 0x6C, 0xB0), 6: RGBColor(0xB7, 0x79, 0x1F),
              7: RGBColor(0xB8, 0x32, 0x80)}
RUN_LIST = [(0, "Flip the Rock, Exploding Seeds"), (1, "Reaching Roots"),
            (2, "Drone Survey, garden skylight"), (3, "Robo taxi to the right"),
            (4, "Dropped"), (5, "Right side: 06, 07, 11, 12"),
            (6, "Keystone to the Mine dock"), (7, "Canopy and compost hatch")]
s = part_slide("Strategy", "Seven runs in 2 minutes 30 seconds")
image(s, png("mission-route-slide"), 0.5, 1.6, 8.2, 4.9)
for i, (num, what) in enumerate(RUN_LIST):
    y = 1.65 + i * 0.6
    colour = RUN_COLOUR.get(num, GREY)
    rect(s, 8.95, y, 1.15, 0.44, fill=colour, line=colour)
    text(s, "Phase %d" % num, 8.95, y + 0.09, 1.15, 0.3, size=13,
         color=WHITE if num in RUN_COLOUR else MUTED, bold=True, align=PP_ALIGN.CENTER)
    text(s, what, 10.25, y + 0.07, 2.9, 0.4, size=14,
         color=INK if num in RUN_COLOUR else SOFT, bold=num in RUN_COLOUR)
text(s, "Close missions first: short trips are quicker and more reliable. "
        "We skipped M04 Lucky Leaves: far away, partly luck, and only 10 or 20 points.",
     0.7, 6.65, 12.2, 0.7, size=15, color=MUTED)

# --- 3. Robot: six designs --------------------------------------------------------
# The numbered copy: the team does not name the six designs to the judges.
s = part_slide("Robot", "We studied six designs before we built ours")
image(s, png("wheel-pattern-unnamed"), 0.6, 1.8, 8.4, 5.3)
point(s, 9.3, 2.4, 3.7, "Blue wheels slip",
      "The three designs that slipped all used blue SPIKE wheels.",
      PART_COLOUR["Robot"])
point(s, 9.3, 4.0, 3.7, "So ours grip",
      "We chose the grippy 62.4 mm wheels.", PART_COLOUR["Robot"])

# --- 4. Robot: shape and ports ----------------------------------------------------
s = part_slide("Robot", "Flat walls, so every run starts straight")
image(s, png("wall-squaring"), 0.5, 1.8, 6.2, 4.3)
image(s, png("robot-wiring"), 6.9, 1.8, 6.0, 4.3)
text(s, "Push it flat against the wall, and it can only sit square.",
     0.7, 6.3, 6.0, 0.8, size=17, color=MUTED)
text(s, "6 ports: 2 wheel motors, 2 attachment motors, 2 colour sensors.",
     7.1, 6.3, 5.8, 0.8, size=17, color=MUTED)

# --- 5. Robot: gravity mounting ---------------------------------------------------
s = part_slide("Robot", "Attachments drop on, and gravity holds them")
image(s, png("gravity-mount"), 0.5, 1.8, 6.4, 3.6)
image(s, os.path.join(PHOTOS, "attachment-1.jpg"), 7.1, 1.8, 2.6, 3.6)
point(s, 10.0, 1.9, 3.0, "One move", "Pegs line it up. Its own weight holds it.",
      PART_COLOUR["Robot"], size=15)
point(s, 10.0, 3.3, 3.0, "Push before motors", "A motor can go wrong. A push can't.",
      PART_COLOUR["Robot"], size=15)
point(s, 10.0, 4.7, 3.0, "Arm starts on a stopper",
      "The same fixed point every run.", PART_COLOUR["Robot"], size=15)
if FILL["swap"]:
    text(s, "A swap takes %s. Last season, swaps took a long time." % FILL["swap"],
         0.7, 5.9, 12, 0.6, size=22, color=INK, bold=True)
else:
    gap_box(s, 0.7, 5.75, 12, 1.2,
            "How long a swap takes: time five swaps, use the middle one. "
            "Put it in FILL['swap'] in tools/make-judging-pack.py.")

# --- 6. Code: Python in layers ----------------------------------------------------
s = part_slide("Code", "Python, in layers")
image(s, png("code-layers"), 0.5, 1.75, 6.6, 4.3)
rect(s, 7.4, 1.9, 5.5, 2.5, fill=CODE_BG, line=CODE_BG)
text(s, "# phase0-alt.py: Flip the Rock\n"
        "await drive_cm(-44)\n"
        "await face(0)\n"
        "await drive_cm(22)\n"
        "await face(90)",
     7.65, 2.1, 5.1, 2.2, size=18, color=CODE_FG, font=MONO, spacing=1.25)
point(s, 7.4, 4.65, 5.5, "Reused from last year",
      "drive_cm came from last year's team. We changed the wheel size, 88 mm to 62.4 mm.",
      PART_COLOUR["Code"], size=15)
point(s, 7.4, 5.95, 5.5, "45 degrees off: it stops",
      "It stops instead of spinning off the table.", PART_COLOUR["Code"], size=15)
text(s, "The run says WHAT. The library says HOW.", 0.7, 6.3, 6.4, 0.6, size=18,
     color=INK, bold=True)

# --- 7. Code: the flowchart -------------------------------------------------------
s = part_slide("Code", "What drive_cm(-44) does, step by step")
image(s, png("drive-simple"), 0.5, 1.9, 12.3, 3.6)
point(s, 0.7, 5.75, 5.8, "The run says one line",
      "drive_cm(-44): drive back 44 cm.", PART_COLOUR["Code"])
point(s, 6.9, 5.75, 6.0, "The library does the rest",
      "About 66 times a second, until it reaches the mark.", PART_COLOUR["Code"])

# --- 7. Sensors: three steps ------------------------------------------------------
s = part_slide("Sensors", "Only the gyroscope steers")
image(s, png("gyro-steps"), 0.5, 1.7, 12.3, 4.6)
text(s, "The two colour sensors are plugged in, but we don't use them. "
        "The gyroscope works anywhere on the mat, not just near a line.",
     0.7, 6.45, 12, 0.8, size=17, color=MUTED)

# --- 8. Sensors: the loop ---------------------------------------------------------
s = part_slide("Sensors", "Drifts 5 degrees left, steers back right")
image(s, png("gyro-loop"), 0.5, 1.7, 6.6, 5.6)
point(s, 7.6, 2.0, 5.3, "Every 15 milliseconds",
      "While it drives, it checks the yaw. Yaw is the way the robot points.",
      PART_COLOUR["Sensors"])
point(s, 7.6, 3.5, 5.3, "Error of -5",
      "It drifted 5 degrees left, so it steers back right.", PART_COLOUR["Sensors"])
point(s, 7.6, 5.0, 5.3, "Harder the further off",
      "A small drift gets a small fix. A big drift gets a big one.",
      PART_COLOUR["Sensors"])

# --- 9. Iteration: 10 runs each ---------------------------------------------------
s = part_slide("Iteration and team", "We test every run 10 times in a row")
# The seven runs, confirmed by the coach on 25 November 2026. There is no Phase 4.
PHASES = [("Phase 0", "M03 Flip the Rock, M02 Exploding Seeds"),
          ("Phase 1", "M05 Reaching Roots"),
          ("Phase 2", "M01 Drone Survey, M15 garden skylight"),
          ("Phase 3", "The robo taxi: attachment and keystone to the right"),
          ("Phase 5", "The right side: M06, M07, M11, part of M12"),
          ("Phase 6", "M13 Keystone Species"),
          ("Phase 7", "M15 nesting canopy and compost hatch")]
rows = [["Run", "Missions", "Worked, out of 10"]]
rows += [[name, what, filled(FILL["runs"][name])] for name, what in PHASES]
table(s, rows, 0.7, 1.85, [2.0, 7.4, 2.6], row_h=0.5, size=15)
text(s, "Change one thing, run it 10 times, compare.", 0.7, 6.1, 12, 0.6, size=22,
     color=INK, bold=True)

# --- 10. Iteration: the arm fix -----------------------------------------------------
s = part_slide("Iteration and team", "One fix: the arm that would not line up")
steps = [("1. The problem", "Our arm was sometimes too high and sometimes too low."),
         ("2. How we found out", "We printed where the motor was after every move. "
                                 "The arm was not starting in the same place."),
         ("3. Two ideas failed", "Pushing the arm into its stopper lifted the "
                                 "attachment, so we dropped it."),
         ("4. What worked", "The arm starts on its stopper every time, and the code "
                            "counts from there.")]
colour = PART_COLOUR["Iteration and team"]
for i, (head, body) in enumerate(steps):
    x = 0.7 + i * 3.05
    rect(s, x, 1.95, 2.85, 3.0, fill=WHITE, line=colour, lw=1.5)
    text(s, head, x + 0.2, 2.1, 2.45, 0.5, size=18, color=colour, bold=True)
    text(s, body, x + 0.2, 2.7, 2.45, 2.2, size=15, color=MUTED)
if FILL["arm_result"]:
    text(s, FILL["arm_result"], 0.7, 5.25, 12, 0.6, size=22, color=INK, bold=True)
else:
    gap_box(s, 0.7, 5.15, 12, 1.0,
            "The result as numbers: how often the arm was right before, and after. "
            "Put it in FILL['arm_result'].")
text(s, "We learned to measure first, then fix.", 0.7, 6.45, 12, 0.6, size=22,
     color=INK, bold=True)

# --- 11. Team ---------------------------------------------------------------------
s = part_slide("Iteration and team", "All five of us built something and coded something")
rows = [["Who", "I built ...", "I coded ..."]]
for role in ROLES:
    rows.append([NAMES[ROLE_SLOT[role]] if NAMED else role,
                 filled(FILL["built"][role]), filled(FILL["coded"][role])])
table(s, rows, 0.7, 1.9, [3.0, 4.5, 4.5], row_h=0.58, size=17)
if FILL["proud"]:
    text(s, "We're most proud of: " + FILL["proud"], 0.7, 5.6, 12, 0.7, size=20,
         color=INK, bold=True)
else:
    gap_box(s, 0.7, 5.55, 7.6, 1.15, "What we are most proud of, in one sentence. "
                                     "Put it in FILL['proud'].")
text(s, "Thank you.\nAsk any of us anything.", 8.7, 5.55, 4.3, 1.3, size=24,
     color=colour, bold=True, align=PP_ALIGN.RIGHT)

prs.save(OUT_PPTX)
print("wrote", os.path.relpath(OUT_PPTX, REPO), "with", len(prs.slides), "slides")

# --- the HTML copy of the deck -------------------------------------------------
DECK_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Robot Design judging slides, BIOGLOW</title>
<style>
  /* Generated by tools/make-judging-pack.py from the same calls as
     judging-deck.pptx. Do not edit by hand: change the script and run it.

     Each slide is 13.333 by 7.5 units, the PowerPoint size in inches. --u is
     one unit, sized so a whole slide fits the screen. Press F for full screen.
     Arrow keys, space, PageUp and PageDown move between slides. N shows the
     speaker notes. */
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root { --u: min(calc(100vw / 13.333), calc(100vh / 7.5)); }
  html { scroll-snap-type: y mandatory; background: #0e221b; }
  body { font-family: 'Trebuchet MS', 'Segoe UI', system-ui, sans-serif; counter-reset: slide; }
  section {
    height: 100vh; scroll-snap-align: start;
    display: flex; align-items: center; justify-content: center;
  }
  .slide {
    position: relative; overflow: hidden;
    width: calc(13.333 * var(--u)); height: calc(7.5 * var(--u));
    background: PAPER; counter-increment: slide;
  }
  .slide.dark { background: INK; }
  .slide::after {
    content: counter(slide); position: absolute;
    right: calc(0.3 * var(--u)); bottom: calc(0.2 * var(--u));
    font-size: calc(0.14 * var(--u)); color: SOFT;
  }
  .t { position: absolute; white-space: pre-wrap; overflow-wrap: break-word; }
  .r { position: absolute; border-radius: calc(0.08 * var(--u)); }
  img { position: absolute; display: block; }
  table { position: absolute; border-collapse: collapse; table-layout: fixed; }
  td {
    padding: calc(0.05 * var(--u)) calc(0.12 * var(--u));
    border: calc(0.01 * var(--u)) solid GREY; vertical-align: middle; line-height: 1.25;
  }
  .notes {
    display: none; position: absolute; left: calc(0.7 * var(--u)); right: calc(0.7 * var(--u));
    bottom: calc(0.25 * var(--u)); z-index: 5; padding: calc(0.15 * var(--u)) calc(0.2 * var(--u));
    background: #fff; color: INK; border: calc(0.015 * var(--u)) solid ACCENT;
    border-radius: calc(0.08 * var(--u)); white-space: pre-wrap; line-height: 1.35;
    font-size: calc(0.17 * var(--u)); box-shadow: 0 calc(0.05 * var(--u)) calc(0.2 * var(--u)) rgba(0,0,0,0.25);
  }
  body.show-notes .notes { display: block; }
  .nav {
    position: fixed; right: 14px; bottom: 14px; z-index: 10;
    display: flex; gap: 6px; align-items: center;
    font: 600 13px 'Trebuchet MS', sans-serif; color: #fff; opacity: 0.25;
  }
  .nav:hover { opacity: 1; }
  .nav button {
    height: 38px; min-width: 38px; padding: 0 10px; border-radius: 19px; border: 0;
    cursor: pointer; background: rgba(22, 54, 43, 0.85); color: #fff; font-size: 15px;
  }
  .nav button:hover { background: ACCENT; }
  .nav span { background: rgba(22, 54, 43, 0.85); padding: 9px 12px; border-radius: 19px; }
  @media print {
    .nav, .notes { display: none !important; }
    :root { --u: 0.75in; }
    @page { size: 10in 5.625in; margin: 0; }
    html { scroll-snap-type: none; background: #fff; }
    section { height: auto; page-break-after: always; }
  }
</style>
</head>
<body>
"""


def skin(page):
    for key, value in (("PAPER", PAPER), ("INK", INK), ("SOFT", SOFT),
                       ("ACCENT", ACCENT), ("GREY", GREY)):
        page = page.replace(key, _hex(value))
    return page


out = [skin(DECK_PAGE)]
for entry in HTML_SLIDES:
    out.append("<section><div class='slide%s'>" % (" dark" if entry["dark"] else ""))
    out.extend(entry["parts"])
    if entry["notes"]:
        out.append("<div class='notes'>%s</div>" % html.escape(entry["notes"]))
    out.append("</div></section>\n")
out.append("""<div class="nav"><button id="prev" aria-label="Previous slide">&#8249;</button>
<span id="where"></span><button id="next" aria-label="Next slide">&#8250;</button>
<button id="notes" aria-label="Show or hide speaker notes">Notes</button>
<button id="full" aria-label="Full screen">Full screen</button></div>
<script>
(function () {
  var slides = Array.prototype.slice.call(document.querySelectorAll('section'));
  function current() {
    var mid = window.innerHeight / 2, best = 0;
    slides.forEach(function (s, i) {
      var r = s.getBoundingClientRect();
      if (r.top <= mid && r.bottom >= mid) best = i;
    });
    return best;
  }
  function go(i) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    window.scrollTo(0, slides[i].offsetTop);
    show();
  }
  function show() {
    document.getElementById('where').textContent = (current() + 1) + ' / ' + slides.length;
  }
  function notes() { document.body.classList.toggle('show-notes'); }
  function full() {
    var i = current();
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen();
    setTimeout(function () { go(i); }, 300);
  }
  document.getElementById('prev').onclick = function () { go(current() - 1); };
  document.getElementById('next').onclick = function () { go(current() + 1); };
  document.getElementById('notes').onclick = notes;
  document.getElementById('full').onclick = full;
  document.addEventListener('keydown', function (e) {
    var k = e.key;
    if (k === 'ArrowRight' || k === 'ArrowDown' || k === 'PageDown' || k === ' ') {
      e.preventDefault(); go(current() + 1);
    } else if (k === 'ArrowLeft' || k === 'ArrowUp' || k === 'PageUp') {
      e.preventDefault(); go(current() - 1);
    } else if (k === 'Home') { e.preventDefault(); go(0); }
    else if (k === 'End') { e.preventDefault(); go(slides.length - 1); }
    else if (k === 'n' || k === 'N') { notes(); }
    else if (k === 'f' || k === 'F') { full(); }
  });
  window.addEventListener('scroll', show, { passive: true });
  window.addEventListener('resize', function () { go(current()); });
  show();
})();
</script>
</body>
</html>
""")
with open(OUT_DECK, "w", encoding="utf-8") as fh:
    fh.write("".join(out))
print("wrote", os.path.relpath(OUT_DECK, REPO))

# =============================================================================
# PRINTED PAGES: cue cards and the question sheet
# =============================================================================
PRINT_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TITLE</title>
<style>
  /* Generated by tools/make-judging-pack.py. Do not edit by hand. Print on
     Letter paper at 100%, with "Background graphics" turned on. */
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  @page { size: letter; margin: 0.4in; }
  body { font-family: 'Trebuchet MS', 'Segoe UI', system-ui, sans-serif; color: INK;
         background: #e9ece9; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .page { width: 7.7in; margin: 0.3in auto; background: #fff; }
  @media print { body { background: #fff; } .page { margin: 0; } .help { display: none; } }
  .help { width: 7.7in; margin: 0.3in auto 0; font-size: 14px; color: MUTED; }
  .gap { color: ACCENT; font-weight: 700; }
EXTRA
</style>
</head>
<body>
"""


def print_page(title, extra_css):
    return skin(PRINT_HEAD.replace("TITLE", title).replace("EXTRA", extra_css)
                .replace("MUTED", _hex(MUTED)))


def esc(t):
    return html.escape(t)


# --- cue cards ----------------------------------------------------------------
CARD_CSS = """
  .card { height: 4.75in; border: 2px dashed SOFT; border-radius: 0.12in; padding: 0.3in 0.4in;
          position: relative; page-break-inside: avoid; overflow: hidden; }
  .card + .card { margin-top: 0.3in; }
  .pair { page-break-after: always; }
  .pair:last-child { page-break-after: auto; }
  .band { position: absolute; left: 0; top: 0; bottom: 0; width: 0.22in; }
  .who { font-size: 30px; font-weight: 700; }
  .meta { font-size: 15px; color: SOFT; margin-top: 2px; }
  .show { font-size: 15px; margin-top: 10px; }
  ul { list-style: none; margin-top: 14px; }
  li { font-size: 23px; line-height: 1.25; padding: 5px 0 5px 28px; position: relative; }
  li::before { content: ""; position: absolute; left: 4px; top: 15px; width: 11px; height: 11px;
               border-radius: 50%; background: currentColor; opacity: 0.8; }
  .next { position: absolute; left: 0.4in; right: 0.4in; bottom: 0.28in; font-size: 17px;
          border-top: 1px solid GREY; padding-top: 8px; }
  .next b { color: INK; }
  /* A card with a picture: smaller bullets, so the picture fits above the handover. */
  .has-fig { padding-top: 0.22in; }
  .has-fig ul { margin-top: 6px; }
  .has-fig li { font-size: 19px; padding: 2px 0 2px 26px; }
  .has-fig li::before { top: 11px; width: 10px; height: 10px; }
  .fig { display: block; width: 88%; margin: 4px auto 0; }
"""
cards = [print_page("Robot Design cue cards, BIOGLOW", skin(CARD_CSS)),
         "<p class='help'>Print on Letter at 100%%. Cut along the dashed lines. "
         "Five cards, two to a page.%s</p>\n"
         % ("" if NAMED else " This copy shows roles. The coach's private copy has names.")]
for i in range(0, len(ROLES), 2):
    cards.append("<div class='page pair'>")
    for role in ROLES[i:i + 2]:
        p = PARTS[role]
        c = _hex(PART_COLOUR[role])
        bullets = "".join("<li style='color:%s'><span style='color:%s'>%s</span></li>"
                          % (c, _hex(INK), esc(b)) for b in p["cue"])
        figure = ("<img class='fig' alt='' src='%s'>" % html.escape(img_src(png(p["figure"])))
                  if p.get("figure") else "")
        cards.append(
            "<div class='card%s'><div class='band' style='background:%s'></div>"
            "<div class='who' style='color:%s'>%s</div>"
            "<div class='meta'>%s &nbsp;·&nbsp; %s</div>"
            "<div class='show'><b>Show:</b> %s</div><ul>%s</ul>%s"
            "<div class='next'><b>Then say:</b> %s</div></div>"
            % (" has-fig" if figure else "", c, c, esc(label(role)), esc(p["time"]),
               esc(p["rubric"]), esc(p["show"]), bullets, figure, esc(handover(role))))
    cards.append("</div>\n")
cards.append("</body>\n</html>\n")
with open(OUT_CARDS, "w", encoding="utf-8") as fh:
    fh.write("".join(cards))
print("wrote", os.path.relpath(OUT_CARDS, REPO))

# --- cue cards you can edit: one card per slide, half a Letter page --------------
# The same words as the printed cards above. Open in PowerPoint, Keynote or Google
# Slides. To print two to a page, choose "2 slides per page" or print at half size.
card_prs = Presentation()
card_prs.slide_width = Inches(8.5)
card_prs.slide_height = Inches(5.5)
for role in ROLES:
    p = PARTS[role]
    colour = PART_COLOUR[role]
    s = card_prs.slides.add_slide(card_prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = WHITE
    _HTML[id(s)] = {"parts": []}   # the shape helpers also write HTML; drop it
    rect(s, 0, 0, 0.22, 5.5, fill=colour, line=colour)
    text(s, label(role), 0.55, 0.3, 7.6, 0.55, size=26, color=colour, bold=True)
    text(s, "%s  ·  %s" % (p["time"], p["rubric"]), 0.55, 0.88, 7.6, 0.3, size=12,
         color=SOFT)
    text(s, "Show: " + p["show"], 0.55, 1.2, 7.6, 0.4, size=12, color=INK)
    small = bool(p.get("figure"))
    text(s, "\n".join("•  " + b for b in p["cue"]), 0.55, 1.65, 7.6, 1.9,
         size=16 if small else 20, color=INK, spacing=1.3)
    if small:
        image(s, png(p["figure"]), 0.55, 2.88, 7.6, 1.78)
    rect(s, 0.55, 4.72, 7.6, 0.01, fill=GREY, line=GREY, lw=0.5)
    text(s, "Then say: " + handover(role), 0.55, 4.85, 7.6, 0.4, size=14, color=INK)
card_prs.save(OUT_CARDS_PPTX)
print("wrote", os.path.relpath(OUT_CARDS_PPTX, REPO), "with", len(card_prs.slides), "cards")

# --- the question sheet ---------------------------------------------------------
QS_CSS = """
  .page { padding: 0.1in 0; }
  h1 { font-size: 24px; }
  .sub { font-size: 14px; color: SOFT; margin: 4px 0 12px; }
  .rules { display: flex; gap: 10px; margin-bottom: 14px; }
  .rules div { flex: 1; border: 1px solid GREY; border-radius: 8px; padding: 8px 10px;
               font-size: 12.5px; line-height: 1.3; }
  .rules b { display: block; font-size: 14px; }
  h2 { font-size: 17px; color: #fff; padding: 5px 10px; border-radius: 6px; margin: 14px 0 6px;
       page-break-after: avoid; }
  .q { display: grid; grid-template-columns: 0.42in 1fr; padding: 6px 0;
       border-bottom: 1px solid GREY; page-break-inside: avoid; font-size: 13px; line-height: 1.3; }
  .n { font-weight: 700; font-size: 15px; color: SOFT; }
  .qq { font-weight: 700; font-size: 14px; }
  .a { margin-top: 2px; }
  .f { margin-top: 2px; color: MUTED; font-style: italic; }
  .drill { page-break-before: always; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { background: INK; color: #fff; text-align: left; padding: 5px 8px; }
  td { border-bottom: 1px solid GREY; padding: 4px 8px; }
  td.box { text-align: center; font-size: 15px; }
"""
qs = [print_page("Robot Design judge questions, BIOGLOW", skin(QS_CSS)),
      "<p class='help'>Print on Letter at 100%. The last page is the drill list "
      "for the coach: questions only, no answers.</p>\n",
      "<div class='page'><h1>Robot Design: the questions judges might ask</h1>"
      "<p class='sub'>5 minutes of questions after our 5-minute explanation. "
      "The judges choose who answers, so read every part, not just yours.</p>"
      "<div class='rules'>"
      "<div><b>Short</b>Two or three sentences, then stop. The judge asks more if "
      "they want more.</div>"
      "<div><b>Honest</b>\"I don't know, but my teammate built that\" is a good "
      "answer. A made-up one falls apart at the follow-up.</div>"
      "<div><b>Your words</b>Know the idea, not the words. Orange answers need our "
      "own facts: find them before practice.</div></div>"]
for role in ROLES:
    qs.append("<h2 style='background:%s'>%s</h2>" % (_hex(PART_COLOUR[role]), esc(label(role))))
    for n, part, q, a, f, team in QUESTIONS:
        if part != role:
            continue
        qs.append("<div class='q'><div class='n'>%d</div><div><div class='qq'>%s</div>"
                  "<div class='a%s'>%s</div><div class='f'>Follow-up: %s</div></div></div>"
                  % (n, esc(q), " gap" if team else "", esc(a), esc(f)))
qs.append("</div>\n<div class='page drill'><h1>Question drill: all 32</h1>"
          "<p class='sub'>The coach reads a question and points at anyone. Answer in "
          "two or three sentences, then stop. Tick a box each time it is answered well.</p>"
          "<table><tr><th>#</th><th>Question</th><th>Part</th><th>1</th><th>2</th><th>3</th></tr>")
for n, part, q, a, f, team in QUESTIONS:
    qs.append("<tr><td>%d</td><td>%s</td><td>%s</td>%s</tr>"
              % (n, esc(q), esc(part), "<td class='box'>☐</td>" * 3))
qs.append("</table></div>\n</body>\n</html>\n")
with open(OUT_QS, "w", encoding="utf-8") as fh:
    fh.write("".join(qs))
print("wrote", os.path.relpath(OUT_QS, REPO))

# --- one zip of the editable files, for sending to the team ---------------------
if NAMED:
    import zipfile
    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in (OUT_PPTX, OUT_CARDS_PPTX):
            z.write(path, os.path.basename(path))
    print("wrote", os.path.relpath(OUT_ZIP, REPO))
