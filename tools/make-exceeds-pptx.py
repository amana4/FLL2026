#!/usr/bin/env python3
"""Generate the Robot Design "going for Exceeds" workshop deck.

One PowerPoint in three parts:

  Part 1  Today in class. Closes the gaps the Robot Design test survey showed
          (22 November 2026): motor sockets, face, YAW_SIGN, the six designs,
          BOXOR and gravity mounting, fix stories, reliability numbers.
  Part 2  Homework. The eleven slides of our 5-minute Robot Design
          explanation, as templates. Each has "Your turn" boxes to fill in, an
          Exceeds checklist, and speaker notes with what to say.
  Part 3  Putting it together. Speaking order, handovers, rehearsal and
          discussion.

Upload the .pptx to Google Slides so the team can edit one copy together.

Each part has a role, not a person: Strategy, Robot, Code, Testing and Team.
The coach puts names against the roles. Do not put names in this file: the
repo and the website are public. Names go in the Google Slides copy only.

Run:
    python3 tools/make-exceeds-pptx.py            public copy, roles only
    python3 tools/make-exceeds-pptx.py --named    private copy, with names

--named reads the names from docs/team-roster.md and writes to
robot-design/private/, which .gitignore keeps out of git and mkdocs.yml keeps off
the website. Share that copy with the team by hand. Never commit it.

Writes robot-design/exceeds-workshop.pptx, and robot-design/exceeds-workshop.html
for showing in class. Both come from the same calls below, so they cannot drift
apart: every helper draws its shape in the .pptx and writes the same shape into
the HTML. The HTML is for presenting. Edit the homework in Google Slides.

The diagrams come from PNG copies in robot-design/diagrams/png/, made with
tools/svg2png.swift.
"""

import base64
import html
import os
import re
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

# Who leads each part, by roster slot. Slots are in docs/team-roster.md. Change
# this table to change who does which homework.
ROLE_SLOT = {"Strategy": "Kid 5", "Robot": "Kid 2", "Code": "Kid 1",
             "Sensors": "Kid 3", "Iteration and team": "Kid 4"}
SLOTS = ["Kid 1", "Kid 2", "Kid 3", "Kid 4", "Kid 5"]


def _roster_names():
    """Slot to first name, from the private roster. Only used with --named."""
    path = os.path.join(REPO, "docs", "team-roster.md")
    names = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"\|\s*(Kid [1-5])\s*\|\s*([^|]+?)\s*\|", line)
        if m:
            names[m.group(1)] = m.group(2)
    return names


NAMES = _roster_names() if NAMED else {}


def person(slot):
    """A slot as shown on the slides: a name in the private copy."""
    return NAMES.get(slot, slot)


def lead(role):
    """The role, plus who leads it in the private copy."""
    return "%s: %s" % (role, person(ROLE_SLOT[role])) if NAMED else role


def next_up(role):
    """How the next speaker is named in a handover line."""
    return person(ROLE_SLOT[role]) if NAMED else "[name]"


if NAMED:
    OUT_DIR = os.path.join(REPO, "robot-design", "private")
    os.makedirs(OUT_DIR, exist_ok=True)
    OUT = os.path.join(OUT_DIR, "exceeds-workshop-named.pptx")
    OUT_HTML = os.path.join(OUT_DIR, "exceeds-workshop-named.html")
else:
    OUT_DIR = os.path.join(REPO, "robot-design")
    OUT = os.path.join(OUT_DIR, "exceeds-workshop.pptx")
    OUT_HTML = os.path.join(OUT_DIR, "exceeds-workshop.html")
HTML_BASE = OUT_DIR

# --- BIOGLOW skin, the same as tools/make-design-pptx.py ---------------------
INK = RGBColor(0x16, 0x36, 0x2B)
MUTED = RGBColor(0x4A, 0x63, 0x57)
SOFT = RGBColor(0x7D, 0x94, 0x88)
ACCENT = RGBColor(0xEB, 0x6C, 0x36)
PAPER = RGBColor(0xF5, 0xF5, 0xF5)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TINT = RGBColor(0xFC, 0xE6, 0xDC)
GREY = RGBColor(0xD8, 0xDE, 0xDA)
PALE = RGBColor(0xE7, 0xF0, 0xEB)

# The run colours on the mission map, from tools/make-robot-diagrams.py.
RUN_GREEN = RGBColor(0x1B, 0x6B, 0x47)
RUN_PURPLE = RGBColor(0x6B, 0x46, 0xC1)
RUN_ORANGE = RGBColor(0xDD, 0x6B, 0x20)
RUN_BLUE = RGBColor(0x2B, 0x6C, 0xB0)
RUN_GOLD = RGBColor(0xB7, 0x79, 0x1F)

FONT = "Trebuchet MS"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

# The HTML copy. One entry per slide, keyed by the python-pptx slide object.
HTML_SLIDES = []
_HTML = {}


def _hex(c):
    return "#" + str(c)


def _u(v):
    """Inches to the HTML unit. --u is one inch of the slide."""
    return "calc(%g * var(--u))" % v


def _emit(s, fragment):
    _HTML[id(s)]["parts"].append(fragment)


# --- helpers -------------------------------------------------------------------
def slide(dark=False):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = INK if dark else PAPER
    entry = {"dark": dark, "parts": [], "notes": ""}
    HTML_SLIDES.append(entry)
    _HTML[id(s)] = entry
    return s


def text(s, txt, x, y, w, h, size=18, color=MUTED, bold=False,
         align=PP_ALIGN.LEFT, italic=False, spacing=1.2):
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
            r.font.name = FONT
            r.font.size = Pt(size)
            r.font.color.rgb = color
            r.font.bold = bold
            r.font.italic = italic
    lines = "".join("<div>%s</div>" % (html.escape(line) or "&nbsp;")
                    for line in txt.split("\n"))
    _emit(s, "<div class='t' style='left:%s;top:%s;width:%s;font-size:%s;"
             "color:%s;font-weight:%s;font-style:%s;text-align:%s;"
             "line-height:%g'>%s</div>"
          % (_u(x), _u(y), _u(w), _u(size / 72.0), _hex(color),
             "700" if bold else "400", "italic" if italic else "normal",
             {PP_ALIGN.CENTER: "center", PP_ALIGN.RIGHT: "right"}.get(align, "left"),
             spacing * 1.1, lines))
    return box


def eyebrow(s, txt, color=MUTED):
    text(s, txt.upper(), 0.7, 0.45, 12, 0.35, size=11, color=color, bold=True)


def title(s, txt, size=34, y=0.8, color=INK, w=11.9):
    text(s, txt, 0.7, y, w, 1.2, size=size, color=color, bold=True, spacing=1.05)


def lede(s, txt, y=1.75, size=16, w=11.9, color=MUTED):
    text(s, txt, 0.7, y, w, 1.0, size=size, color=color)


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


def card(s, x, y, w, h, head, body, fill=WHITE, line=GREY, head_color=INK,
         size=14):
    rect(s, x, y, w, h, fill=fill, line=line)
    text(s, head, x + 0.2, y + 0.15, w - 0.4, 0.45, size=size + 2,
         color=head_color, bold=True)
    text(s, body, x + 0.2, y + 0.65, w - 0.4, h - 0.8, size=size, color=MUTED)


def your_turn(s, x, y, w, h, prompt, size=14):
    """A dashed orange box: the team replaces the text inside."""
    rect(s, x, y, w, h, fill=TINT, line=ACCENT, dash=True, lw=1.5)
    text(s, "YOUR TURN", x + 0.2, y + 0.12, w - 0.4, 0.3, size=10,
         color=ACCENT, bold=True)
    text(s, prompt, x + 0.2, y + 0.45, w - 0.4, h - 0.55, size=size, color=INK)


def checklist(s, x, y, w, h, items, head="EXCEEDS CHECKLIST"):
    rect(s, x, y, w, h, fill=WHITE, line=INK, lw=1.25)
    text(s, head, x + 0.2, y + 0.12, w - 0.4, 0.3, size=10, color=INK, bold=True)
    text(s, "\n".join("☐  " + i for i in items), x + 0.2, y + 0.5,
         w - 0.4, h - 0.6, size=13, color=MUTED, spacing=1.3)


def bullets(s, items, x=0.7, y=1.9, w=11.9, h=4.5, size=17, color=MUTED):
    text(s, "\n".join("•  " + i for i in items), x, y, w, h, size=size,
         color=color, spacing=1.35)


def image(s, path, x, y, w=None, h=None):
    kwargs = {}
    if w:
        kwargs["width"] = Inches(w)
    if h:
        kwargs["height"] = Inches(h)
    pic = s.shapes.add_picture(path, Inches(x), Inches(y), **kwargs)
    if NAMED:
        # The named copy is shared by hand as one file, and browsers block a
        # local page from reading the folder above it. So carry the pictures.
        mime = "image/jpeg" if path.lower().endswith((".jpg", ".jpeg")) else "image/png"
        with open(path, "rb") as fh:
            src = "data:%s;base64,%s" % (mime, base64.b64encode(fh.read()).decode("ascii"))
    else:
        src = os.path.relpath(path, HTML_BASE).replace(os.sep, "/")
    _emit(s, "<img src='%s' alt='' style='left:%s;top:%s;width:%s;height:%s'>"
          % (html.escape(src), _u(x), _u(y), _u(pic.width / 914400.0),
             _u(pic.height / 914400.0)))
    return pic


def table(s, rows, x, y, w, col_w, row_h=0.42, size=12, head_fill=INK, first_col=None):
    """first_col: optional colours for the first cell of each body row."""
    shape = s.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y),
                               Inches(w), Inches(row_h * len(rows)))
    t = shape.table
    for c, cw in enumerate(col_w):
        t.columns[c].width = Inches(cw)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = t.cell(r, c)
            cell.text = val
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = head_fill
            else:
                cell.fill.fore_color.rgb = WHITE if r % 2 else PALE
            for p in cell.text_frame.paragraphs:
                for run in p.runs:
                    run.font.name = FONT
                    run.font.size = Pt(size)
                    run.font.bold = (r == 0) or (c == 0 and first_col is not None)
                    run.font.color.rgb = WHITE if r == 0 else (
                        first_col[r - 1] if (c == 0 and first_col) else INK)
    cols = "".join("<col style='width:%s'>" % _u(cw) for cw in col_w)
    body = []
    for r, row in enumerate(rows):
        fill = head_fill if r == 0 else (WHITE if r % 2 else PALE)
        cells = "".join("<td style='background:%s;color:%s;font-weight:%s'>%s</td>"
                        % (_hex(fill),
                           _hex(WHITE if r == 0 else (first_col[r - 1] if (c == 0 and first_col) else INK)),
                           "700" if (r == 0 or (c == 0 and first_col)) else "400", html.escape(v))
                        for c, v in enumerate(row))
        body.append("<tr style='height:%s'>%s</tr>" % (_u(row_h), cells))
    _emit(s, "<table style='left:%s;top:%s;width:%s;font-size:%s'>"
             "<colgroup>%s</colgroup>%s</table>"
          % (_u(x), _u(y), _u(w), _u(size / 72.0), cols, "".join(body)))
    return t


def notes(s, txt):
    s.notes_slide.notes_text_frame.text = txt
    _HTML[id(s)]["notes"] = txt


def divider(num, head, sub):
    s = slide(dark=True)
    text(s, num, 0.7, 1.6, 4, 1.5, size=88, color=ACCENT, bold=True)
    text(s, head, 0.7, 3.3, 11.9, 1.2, size=40, color=WHITE, bold=True)
    text(s, sub, 0.7, 4.5, 11.9, 1.5, size=18, color=PALE)
    return s


def png(name):
    return os.path.join(PNG, name + ".png")


# =============================================================================
# OPENING
# =============================================================================
s = slide(dark=True)
text(s, "BIOGLOW  ·  ROBOT DESIGN  ·  CLASS, SUNDAY 22 NOVEMBER 2026",
     0.7, 0.6, 12, 0.4, size=11, color=PALE, bold=True)
text(s, "Going for Exceeds\nin Robot Design", 0.7, 1.6, 11.9, 2.4, size=52,
     color=WHITE, bold=True, spacing=1.0)
text(s, "Today we close the gaps from the Robot Design test. For homework, each "
        "of us finishes our slides. Next class, we put them together and "
        "practise.", 0.7, 4.3, 11, 1.2, size=20, color=PALE)
notes(s, "Coach: this deck has three parts. Part 1 is today's lesson. Part 2 is "
         "the homework slides. Part 3 is how we put it together. The survey "
         "results on slide 3 are shown without names on purpose.")

s = slide()
eyebrow(s, "What Exceeds means")
title(s, "Exceeds has no set words. The judge writes why.")
lede(s, "The rubric has four levels: Beginning 1, Developing 2, Accomplished 3, "
        "Exceeds 4. For Exceeds, the judge must write a comment saying how we "
        "exceeded. So we need things a judge can write down.")
for i, (lvl, name, fill, col) in enumerate((
        ("1", "Beginning", PALE, MUTED), ("2", "Developing", GREY, INK),
        ("3", "Accomplished", RGBColor(0x7F, 0xC2, 0x96), INK),
        ("4", "Exceeds", ACCENT, WHITE))):
    rect(s, 0.7 + i * 2.98, 2.8, 2.88, 0.9, fill=fill, line=fill)
    text(s, lvl + "  " + name, 0.7 + i * 2.98, 3.05, 2.88, 0.5, size=18,
         color=col, bold=True, align=PP_ALIGN.CENTER)
text(s, "the judge writes why", 9.64, 3.75, 2.88, 0.4, size=12, color=ACCENT,
     bold=True, align=PP_ALIGN.CENTER)
card(s, 0.7, 4.3, 3.8, 2.4, "1. Accomplished first",
     "Every row needs the Accomplished words first. You can't skip a level.")
card(s, 4.75, 4.3, 3.8, 2.4, "2. Evidence to write down",
     "A number we measured. A true story with before and after. A thing we "
     "can show, like an old attachment.")
card(s, 8.8, 4.3, 3.8, 2.4, "3. All five of us",
     "The judges choose who answers. Any of us can explain any part, with our "
     "own examples.")
notes(s, "Ask: what is the difference between 'it works' and 'it worked 9 out "
         "of 10 times'? The second one is something a judge can write in the "
         "Exceeds box.")

s = slide()
eyebrow(s, "What the Robot Design test showed")
title(s, "We know a lot. Some things only one of us knows.")
card(s, 0.7, 1.9, 5.85, 4.6, "Strong already",
     "•  Why we skipped missions, with points and how often they worked\n"
     "•  How we share work: roles, swapping roles, voting\n"
     "•  Great proud moments, like the award and the 32-team table\n"
     "•  Ideas from videos and building instructions\n"
     "•  One of us got all 12 quiz questions right",
     size=15)
card(s, 6.75, 1.9, 5.85, 4.6, "Gaps to close today",
     "•  Motor sockets, YAW_SIGN and face: 2 of 4 missed each\n"
     "•  No one listed which missions our robot does\n"
     "•  No one mentioned the six designs, BOXOR or gravity mounting\n"
     "•  Hardly any test-and-fix stories, and only one number\n"
     "•  Some of us couldn't say what we built and coded\n"
     "•  Two of us left the three sentences blank",
     fill=TINT, line=ACCENT, head_color=ACCENT, size=15)
notes(s, "No names. Say: the gaps belong to the team, not to one person. "
         "That is why we close them together today.")

# =============================================================================
# PART 1: TODAY IN CLASS
# =============================================================================
divider("1", "Today: fix the gaps",
        "Short lessons, then we do it. Every slide ends with something we say "
        "or write.")

s = slide()
eyebrow(s, "Quick fix  ·  2 of 4 missed this")
title(s, "Wheels on F and A. Attachments on C and E.")
image(s, png("robot-wiring"), 0.7, 1.8, w=7.0)
table(s, [["Socket", "What is plugged in"],
          ["F", "Left wheel motor"],
          ["A", "Right wheel motor"],
          ["C", "Attachment motor (attachment1)"],
          ["E", "Attachment motor (attachment2)"]],
      8.0, 2.0, 4.6, [1.1, 3.5], row_h=0.55, size=14)
text(s, "Two of us chose C and D. C is an attachment motor, and the final runs "
        "use C and E. The other two ports have colour sensors, plugged in but not "
        "used to steer.", 8.0, 4.9, 4.6, 1.6, size=14, color=MUTED)
notes(s, "Check: point at the real robot. Ask a kid who missed it to touch "
         "the F cable and the A cable. The ITERATE story: on 20 September the "
         "robot stopped with a 'no motor' error until the code used F and A.")

s = slide()
eyebrow(s, "Quick fix  ·  2 of 4 missed a face question")
title(s, "face(90) points 90 degrees from where we started")
image(s, png("face-square"), 0.7, 1.75, w=7.2)
card(s, 8.2, 1.9, 4.4, 4.4, "Why it matters",
     "face measures every turn from base, the way the robot pointed at the "
     "start. A small mistake in one turn is not passed on to the next.\n\n"
     "Round a square: about 1 degree off with face. 17 degrees off without it.",
     size=15)
notes(s, "Check question: the robot is already pointing at 90. What does "
         "face(90) do? Answer: nothing, it is already there. A 'turn 90' would "
         "turn another quarter.")

s = slide()
eyebrow(s, "Quick fix  ·  2 of 4 missed this")
title(s, "YAW_SIGN = -1 says which way the gyro counts")
card(s, 0.7, 1.9, 5.85, 4.3, "What it means",
     "The gyro gives a number for which way the robot points. Ours counts UP "
     "when the robot turns anticlockwise. YAW_SIGN = -1 tells the code that, "
     "so it steers the right way.",
     size=16)
card(s, 6.75, 1.9, 5.85, 4.3, "How we found out (20 September)",
     "drive_cm(-44) should have driven backwards. The robot spun on the spot "
     "instead, because the code was steering the wrong way. We flipped the "
     "sign, and it drove straight.\n\nThat is an ITERATE story.",
     size=16)
notes(s, "Not 'the robot drives backwards', not 'the motor is plugged in "
         "backwards', not 'how fast it turns'. Those were the wrong answers "
         "picked.")

s = slide()
eyebrow(s, "IDENTIFY gap  ·  no one mentioned this")
title(s, "We studied six designs before we built ours")
image(s, png("wheel-pattern"), 0.7, 1.75, w=7.4)
rect(s, 8.4, 1.9, 4.2, 4.6, fill=WHITE, line=ACCENT, lw=1.5)
text(s, "SAY IT TO A JUDGE", 8.6, 2.05, 3.8, 0.3, size=10, color=ACCENT, bold=True)
text(s, "\"Before we built anything, we compared six robot designs other teams "
        "had made, and what went wrong for each one. The three that slipped "
        "all used the blue SPIKE wheels. So we took the best ideas, like a "
        "box frame and gravity mounting, and built ours from those.\"",
     8.6, 2.45, 3.8, 3.9, size=14, color=INK)
notes(s, "This is our strongest IDENTIFY answer: 'clear use of building or "
         "coding resources to support their mission strategy'. It is a gear "
         "row, so it counts for Core Values too. Each kid says it once, in "
         "their own words.")

s = slide()
eyebrow(s, "IDENTIFY and CREATE  ·  why this robot")
title(s, "We compared it with another robot")
image(s, png("robot-compare"), 2.0, 1.55, h=5.55)
notes(s, "HummerOne Pro is one of the six designs. It is the easiest to build, "
         "and that is a real strength. Ask: so why didn't we build it? Answers "
         "are on the slide: the blue wheels slip, it doesn't square up on a "
         "wall, and clip-on attachments are slow to swap. Last season, swaps "
         "took a long time. That is why we chose gravity mounting.")

s = slide()
eyebrow(s, "IDENTIFY  ·  our mission strategy")
title(s, "Our strategy in six choices")
choices = [
    ("1", "Start on the left", "Finish the missions close to the left home first."),
    ("2", "Reuse attachments", "One frame with arms we swap. One attachment does several missions."),
    ("3", "Push where we can", "Motors can go wrong. A push can't. phase2 is one straight push and back."),
    ("4", "A flat robot", "Flat walls line up on the field wall and on the lines on the mat."),
    ("5", "Gravity mounting", "Last season, swaps took a long time. Now it's one move."),
    ("6", "The robo taxi", "Attachments and the keystone wait on the left. The robot carries them to the right."),
]
for i, (num, head, body) in enumerate(choices):
    cx, cy = 0.7 + (i % 3) * 4.05, 1.85 + (i // 3) * 2.6
    rect(s, cx, cy, 3.85, 2.4, fill=WHITE, line=GREY)
    text(s, num, cx + 0.25, cy + 0.15, 0.8, 0.9, size=40, color=ACCENT, bold=True)
    text(s, head, cx + 1.05, cy + 0.35, 2.65, 0.5, size=18, color=INK, bold=True)
    text(s, body, cx + 0.25, cy + 1.1, 3.4, 1.2, size=14, color=MUTED)
notes(s, "Each choice is a reason a judge can write down. Ask a different kid "
         "to explain each one, with an example from our robot. For choice 3: "
         "phase2 does M01 Drone Survey and M15 Biocentric Architecture with one "
         "straight push and back, which is why it is so reliable. Measure it: "
         "how many out of 10?")

s = slide()
eyebrow(s, "IDENTIFY  ·  the mission map")
title(s, "Left first, then the robo taxi to the right")
image(s, png("mission-route"), 0.7, 1.5, h=5.5)
card(s, 8.55, 1.6, 4.05, 5.5, "Why this order",
     "Everything we need waits on the left: the attachments and the keystone "
     "species.\n\nphase0-alt does the rock and the seeds, close to home. "
     "phase2 does the drone and M15 with one straight push and back.\n\n"
     "phase3 does the roots, then drives right as a robo taxi, carrying one "
     "attachment and the keystone.\n\nFrom the right: Phase 5, then Phase 6 "
     "puts the keystone on the Mine dock.", size=13)
notes(s, "The routes are a sketch, not measured paths. Check each run's "
         "missions with the team: the Phase 5 numbers (M07, M11, M06, M12) "
         "came from one teammate's answer. M12 is partly done: we skipped the "
         "ring.")

s = slide()
eyebrow(s, "IDENTIFY  ·  the robo taxi")
title(s, "One trip carries everything to the right")
for i, (head, body) in enumerate((
        ("Load up", "On the left: the attachment and the keystone species go on the robot."),
        ("Work on the way", "phase3 does M05 Reaching Roots, then drives across the mat."),
        ("Drop off", "On the right, the same attachment does the right-side missions, and the keystone goes to the Mine dock."))):
    cx = 0.7 + i * 2.85
    rect(s, cx, 1.9, 2.65, 2.6, fill=PALE if i < 2 else TINT, line=GREY)
    text(s, str(i + 1), cx + 0.2, 2.0, 0.6, 0.7, size=30, color=ACCENT, bold=True)
    text(s, head, cx + 0.8, 2.15, 1.8, 0.5, size=16, color=INK, bold=True)
    text(s, body, cx + 0.2, 2.8, 2.3, 1.6, size=13, color=MUTED)
your_turn(s, 9.25, 1.9, 3.35, 4.95,
          "REMINDER: add the robo taxi video here.\n\nPick the clip that shows "
          "the robot carrying the attachment and the keystone from left to "
          "right.\n\nKeep it under 20 seconds.", size=14)
text(s, "Why: the robot doesn't come back to the left for the next attachment, "
        "and the keystone arrives with the robot that needs it.", 0.7, 4.85, 8.3, 1.2, size=16,
     color=INK, bold=True)
notes(s, "Video still to add. The videos are kept out of git because of their "
         "size, so add the clip to the Google Slides copy.")

s = slide()
eyebrow(s, "IDENTIFY gap  ·  activity: fill this in together")
title(s, "Our missions, one list we all agree on")
table(s, [["Program", "Missions", "Points", "Seconds", "Works /10", "Why this one"],
          ["phase0-alt.py", "M03 Flip the Rock, M02 Exploding Seeds", "", "", "", ""],
          ["phase2.py", "M01 Drone Survey, M15 Biocentric Architecture (City dock)", "", "", "", "One straight push and back"],
          ["phase3.py", "M05 Reaching Roots", "", "", "", ""],
          ["Phase 5.py", "Pull, open door, ant, Tree support: M07, M11, M06, M12?", "", "", "", ""],
          ["Phase 6.py", "M13 Keystone Species", "", "", "", ""],
          ["Phase 7.py", "Mission N (18 November)", "", "", "", ""],
          ["Skipped", "M04 Lucky Leaves, M12 ring on the Elder tree", "", "", "", ""]],
      0.7, 1.8, 11.9, [1.8, 4.3, 1.1, 1.2, 1.3, 2.2], row_h=0.52, size=13)
text(s, "One of us thinks Phase 5 is M07, M11, M06 and M12. Check it together. "
        "One answer said we do 11 missions: count them.", 0.7, 6.25, 11.9,
     0.8, size=14, color=ACCENT, bold=True)
notes(s, "Fill the blank columns as a team. Use the official scoresheet for "
         "points. Seconds: time it. Works /10 is homework if we don't know it. "
         "This table becomes homework slide T2.")

s = slide()
eyebrow(s, "CREATE gap  ·  no one mentioned this")
title(s, "The BOXOR frame and gravity mounting")
image(s, os.path.join(PHOTOS, "attachment-1.jpg"), 0.7, 1.8, h=4.6)
image(s, png("gravity-mount"), 5.0, 1.8, w=4.3)
card(s, 9.55, 1.8, 3.05, 4.6, "Say it",
     "\"We started from a published design, the BOXOR frame. Its bevel gears "
     "turn the motor's movement round a corner to swing an arm. Attachments "
     "sit on pegs, held by their own weight, so a swap is one move.\"",
     size=13)
notes(s, "The rubric says 'original designs OR improved on existing ones'. So "
         "never say 'we invented it'. Say what we changed. Good examples from "
         "the test: one arm became two arms for missions 1 and 2. The mission 2 "
         "attachment with a circle kept getting stuck, so we changed it.")

s = slide()
eyebrow(s, "CREATE  ·  why Python")
title(s, "We code in Python. Here's why.")
reasons = [
    ("Last year's code", "Last season's team left us tuned Python, with drive_cm in it. We only changed the wheel size."),
    ("More control", "We choose every number, write our own commands, and do maths like the gyro correction."),
    ("Write it once", "drive_cm and face live in our library. Every run uses them, so one fix helps every run."),
    ("See every change", "git shows exactly which line changed and when. Every #was note is a test."),
    ("Test without the robot", "A pretend robot in the browser, and 34 automatic checks in a few seconds."),
    ("It found bugs", "Turning the blocks library into Python found 11 bugs, like pi written as 3.146."),
]
for i, (head, body) in enumerate(reasons):
    cx, cy = 0.7 + (i % 3) * 4.05, 1.85 + (i // 3) * 2.6
    rect(s, cx, cy, 3.85, 2.4, fill=WHITE, line=GREY)
    rect(s, cx, cy, 0.12, 2.4, fill=ACCENT, line=ACCENT)
    text(s, head, cx + 0.35, cy + 0.3, 3.3, 0.5, size=18, color=INK, bold=True)
    text(s, body, cx + 0.35, cy + 0.95, 3.3, 1.35, size=14, color=MUTED)
notes(s, "We started the season in Word Blocks, then moved to Python. Say it "
         "fairly: blocks are a good way to start. Python gave us more control "
         "and let us test and track every change. The 11 bugs: 8 found by "
         "reading the blocks, 3 more by testing on the robot.")

s = slide()
eyebrow(s, "CREATE  ·  how drive_cm works")
title(s, "drive_cm: last year's command, our wheels")
rect(s, 0.7, 1.75, 4.6, 5.3, fill=PALE, line=GREY)
text(s, "FROM LAST YEAR", 0.95, 1.95, 4.1, 0.3, size=11, color=MUTED, bold=True)
text(s, "drive_cm came from last season's Python. Our wheels are smaller, so we "
        "changed one number.", 0.95, 2.35, 4.1, 1.2, size=15, color=INK)
table(s, [["", "Wheel size", "30 cm is"],
          ["Last year", "88 mm", "391 wheel degrees"],
          ["Our robot", "62.4 mm", "551 wheel degrees"]],
      0.95, 3.6, 4.1, [1.25, 1.2, 1.65], row_h=0.55, size=13)
text(s, "WHEEL_D_MM = 62.4\nset_calibration_scale(179/180)", 0.95, 5.5, 4.1, 0.8,
     size=13, color=INK, bold=True)
text(s, "We asked for 180 cm and got 179, so the second line fixes every distance.",
     0.95, 6.25, 4.1, 0.7, size=12, color=MUTED)
dsteps = [
    ("1", "Centimetres to wheel degrees", "One wheel turn is pi x 62.4 mm = 196 mm. So 30 cm is 551 degrees of wheel turn."),
    ("2", "Pick a speed", "Under 30 cm it goes slower. drive_cm(-30) goes backwards."),
    ("3", "Ramp up and down", "Speed up gently, hold, slow down gently, so the wheels don't slip."),
    ("4", "Steer with the gyro", "Every 15 ms it checks the gyro and steers back to straight. Next slide."),
    ("5", "Brake a little early", "The robot rolls on after braking, so it brakes about 1.4 cm early."),
]
for i, (num, head, body) in enumerate(dsteps):
    cy = 1.75 + i * 1.07
    rect(s, 5.55, cy, 7.05, 0.95, fill=WHITE, line=GREY)
    text(s, num, 5.7, cy + 0.15, 0.5, 0.7, size=24, color=ACCENT, bold=True)
    text(s, head, 6.2, cy + 0.12, 2.6, 0.75, size=14, color=INK, bold=True)
    text(s, body, 8.85, cy + 0.12, 3.65, 0.8, size=12, color=MUTED)
notes(s, "Last year's toolKit.py is in code/2025-reference/Library/. It had "
         "drive_cm and set_calibration_scale already, with WHEEL_D_MM = 88.0. "
         "Our robot has 62.4 mm wheels, so we changed that one number. The "
         "distance maths is the same: centimetres, then wheel turns, then "
         "degrees. Say it to a judge: 'We kept last year's drive command and "
         "measured our own robot to fit it.' The safety stop: it refuses any "
         "distance longer than the mat, 200 cm.")

s = slide()
eyebrow(s, "CREATE  ·  the gyro correction algorithm")
title(s, "How the gyro keeps us driving straight")
image(s, png("gyro-loop"), 0.7, 1.7, w=4.5)
text(s, "The full version, with the safety stops, is the drive_cm flowchart on How Our Code Is Designed.", 0.7, 5.3, 4.4, 0.9, size=12, color=MUTED)
steps = [
    ("1", "Read the gyro", "How far are we off straight? That is the error, in degrees."),
    ("2", "Work out the steer", "trim = -(18.9 x error + 5.25 x how fast the error changes)"),
    ("3", "Steer", "Left wheel: speed + trim. Right wheel: speed - trim."),
    ("4", "Wait and repeat", "Wait 15 ms and go round again: about 66 times a second."),
]
for i, (num, head, body) in enumerate(steps):
    cy = 1.6 + i * 1.08
    rect(s, 5.35, cy, 7.25, 0.95, fill=WHITE, line=GREY)
    text(s, num, 5.5, cy + 0.15, 0.5, 0.7, size=26, color=ACCENT, bold=True)
    text(s, head, 6.05, cy + 0.12, 2.3, 0.5, size=16, color=INK, bold=True)
    text(s, body, 8.3, cy + 0.12, 4.2, 0.8, size=13, color=MUTED)
rect(s, 5.35, 5.95, 7.25, 1.15, fill=TINT, line=ACCENT)
text(s, "Example: the robot drifts 5 degrees left, so the error is -5. trim = "
        "-(18.9 x -5) = +94. The left wheel speeds up by 94 and the right slows "
        "by 94, so it steers back right. More than 45 degrees off: it stops.",
     5.55, 6.05, 6.9, 1.0, size=13, color=INK)
notes(s, "This is in code/library/advanced.py, lines 446 to 460. The first part "
         "steers harder the further off we are. The second part, 5.25 x the "
         "change, calms the steering so the robot doesn't wiggle. The minus "
         "sign makes it steer against the mistake: without it, the robot "
         "spirals. The pretend robot in code/learn/gyro-correction.html shows "
         "it moving.")

s = slide()
eyebrow(s, "Discussion  ·  10 minutes")
title(s, "Two answers that don't match")
card(s, 0.7, 1.9, 5.85, 4.5, "Colour sensors: settled",
     "One of us wrote that we never used colour sensors. Our notes say we "
     "stopped using them on 20 September.\n\n"
     "The agreed answer: two colour sensors are plugged into the hub, but only "
     "the gyroscope steers.\n\n"
     "•  Why the gyroscope? It works everywhere on the mat, not only near a line.",
     size=15)
card(s, 6.75, 1.9, 5.85, 4.5, "How many missions",
     "One answer said 11 missions. Our final programs show fewer runs.\n\n"
     "•  Count them on the missions table.\n"
     "•  Which ones work every time, and which only sometimes?\n"
     "•  Which number would we say to a judge?",
     size=15)
notes(s, "Judges notice when teammates give different answers. The goal is "
         "one true answer we all give. Write the agreed answers on the "
         "missions table.")

s = slide()
eyebrow(s, "ITERATE gap  ·  the weakest row in the test")
title(s, "A fix story has four parts")
table(s, [["Part", "Question", "Example: the rock"],
          ["1. Problem", "What went wrong?", "After backing into the rock, the robot was crooked."],
          ["2. How we found out", "What did we test or measure?", "The next moves missed. We watched where it pointed."],
          ["3. What we changed", "What exactly did we change?", "We added face(0) right after the bump."],
          ["4. Result", "What happened after? Give a number.", "It drives on straight. Works __ out of 10."]],
      0.7, 1.8, 11.9, [2.4, 3.6, 5.9], row_h=0.7, size=14)
text(s, "Weak: \"We stopped doing that mission.\" That is not a fix.\n"
        "Weak: \"It broke, so we fixed it as a team.\" What broke? What did you change?",
     0.7, 5.6, 11.9, 1.2, size=15, color=ACCENT)
notes(s, "ITERATE has a gear row: 'improvements based on testing'. A good fix "
         "story counts for Robot Design AND Core Values.")

s = slide()
eyebrow(s, "ITERATE  ·  a worked example from this week")
title(s, "The arm that was sometimes too high")
table(s, [["Step", "What happened"],
          ["Problem", "The arm in Phase 7 was too high on some runs and too low on others."],
          ["Measure", "We printed the motor's position after every move and logged every run."],
          ["Found", "Two runs started 45 degrees apart, though we thought they started the same."],
          ["Try 1", "Measure from the motor's own angle. Worked, until the attachment went back on."],
          ["Try 2", "Push the arm into its stopper to find zero. It lifted the attachment. Dropped."],
          ["Fix", "The stopper is zero. Good runs ended within 2 degrees, even after re-seating."],
          ["Still open", "A little play in the build. Next: a rubber band or bracing."]],
      0.7, 1.75, 11.9, [1.8, 10.1], row_h=0.58, size=14)
notes(s, "Point out: two ideas failed, and that is fine. Judges score the "
         "process, not a perfect first try. Bring the printed log on the day.")

s = slide()
eyebrow(s, "ITERATE  ·  activity: 10 minutes")
title(s, "Write your own fix story now")
lede(s, "Pick one. Write the four parts in four short lines. Then read it to a "
        "partner, who asks one more question.")
table(s, [["Stories we have", ""],
          ["Motor sockets: three tries to get F and A", "Gyro past 180: turns spun for 30 seconds"],
          ["YAW_SIGN: the robot spun instead of driving", "179/180: asked for 180 cm, drove 179"],
          ["face(0) after the rock", "The Phase 7 arm"],
          ["One arm became two arms (missions 1 and 2)", "The stuck mission 2 attachment"]],
      0.7, 2.6, 11.9, [5.95, 5.95], row_h=0.6, size=14)
your_turn(s, 0.7, 5.75, 11.9, 1.3,
          "Problem: ...   How we found out: ...   What we changed: ...   Result, with a number: ...")
notes(s, "Each kid should leave with one story, and no two kids should pick "
         "the same one.")

s = slide()
eyebrow(s, "ITERATE  ·  only one of us gave a number")
title(s, "\"It worked 8 out of 10\" beats \"it mostly works\"")
card(s, 0.7, 1.9, 5.85, 4.4, "How to measure",
     "1. Run the program 10 times, the same way each time.\n"
     "2. Tally: worked, or didn't.\n"
     "3. Write it in the run log with the date.\n"
     "4. If you change something, do 10 more. Compare.",
     size=16)
card(s, 6.75, 1.9, 5.85, 4.4, "Why judges like it",
     "A number proves we tested again and again. Before and after numbers "
     "prove the change helped.\n\nExample: 6 out of 10, then we added face(0), "
     "then 9 out of 10.",
     size=16)
notes(s, "This is homework for whoever owns each run. Real numbers only. "
         "If we didn't measure it, we say so.")

s = slide()
eyebrow(s, "DESIGN gap  ·  say it in one breath")
title(s, "\"I built ___. I coded ___. I helped ___ with ___.\"")
lede(s, "The rubric says ALL team members contributed ideas, and ALL have "
        "building and coding skills. Each of us says it out loud now.")
your_turn(s, 0.7, 3.0, 11.9, 2.0,
          "I built ...\nI coded ...\nAn idea I had: ...", size=18)
text(s, "A name and a part beats \"I helped with stuff\". If you only built, or "
        "only coded, tell the coach today.", 0.7, 5.4, 11.9, 1.0, size=15,
     color=ACCENT)
notes(s, "Go round the room. If a kid can't name a build AND a code example, "
         "give them a small coding or building job before the next class.")

s = slide()
eyebrow(s, "Homework  ·  due before next class")
title(s, "Finish your slides in Part 2")
table(s, [["Who", "Slides", "Rubric row"],
          [lead("Strategy"), "T1 Intro, T2 Mission map, T3 Resources", "IDENTIFY"],
          [lead("Robot"), "T4 Why this robot, T5 Attachments", "CREATE"],
          [lead("Code"), "T6 Code", "CREATE"],
          [lead("Sensors"), "T7 Sensors", "CREATE"],
          [lead("Iteration and team"), "T8 Testing, T9 Fix story, T10 Team, T11 Lessons", "ITERATE, DESIGN, COMMUNICATE"],
          ["Everyone", "Your row on T10, your line on T11, your fix story", "All"]],
      0.7, 1.75, 11.9, [2.6, 6.0, 3.3], row_h=0.52, size=14)
text(s, "Rules: replace every YOUR TURN box. Real numbers only: measure it or "
        "say we don't know. Add a photo where you can. Read the speaker notes: "
        "they say what to say.", 0.7, 5.6, 11.9, 1.3, size=15, color=INK)
notes(s, "Coach: put a name against each role in the Google Slides copy, "
         "not in the repo. The person who did most of that work leads it.")

# =============================================================================
# PART 2: HOMEWORK TEMPLATES
# =============================================================================
divider("2", "Homework: finish your slides",
        "These eleven slides are our 5-minute Robot Design explanation. Replace "
        "every YOUR TURN box. Keep the words short: we say the rest out loud.")


def template(code, who, row, head, secs, say, handover, ticks):
    s = slide()
    eyebrow(s, "%s  ·  %s  ·  %s  ·  about %s seconds"
            % (code, who, row, secs))
    title(s, head, size=30)
    checklist(s, 9.35, 1.7, 3.25, 5.2, ticks)
    notes(s, "WHAT TO SAY\n" + say + "\n\nHANDOVER\n" + handover)
    return s


s = template("T1", lead("Strategy"), "Intro", "Meet our robot", 20,
             "Who we are, and our robot in one sentence. 'Our robot is one "
             "base with attachments we swap. We'll each explain one part.'",
             "\"First, how we chose our missions.\"",
             ["Team name", "Robot in one sentence", "Says all five will speak"])
your_turn(s, 0.7, 1.9, 8.4, 1.4, "Team name and one sentence about our robot")
your_turn(s, 0.7, 3.55, 8.4, 3.35, "A photo of the whole robot, from the front")

s = template("T2", lead("Strategy"), "IDENTIFY", "How we chose our missions", 35,
             "Point at the map. Left first, close missions first. Then the robo "
             "taxi: one trip carries the attachment and the keystone to the "
             "right, so the robot doesn't come back for them. Then one skipped mission with numbers. Show "
             "the robo taxi video if we are allowed a screen.",
             "\"Next: where our ideas came from.\"",
             ["Each phase and its missions", "Left first, close first", "Reused attachments",
              "Robo taxi: why we carry the keystone", "Points, seconds, works /10",
              "One skipped mission, with numbers"])
image(s, png("mission-route"), 0.7, 1.6, w=4.5)
your_turn(s, 5.4, 1.6, 3.7, 3.35,
          "Skipped: M__ was only __ points, took __ seconds, worked __ out of 10.", size=13)
table(s, [["Phase", "Missions", "Points", "Seconds", "Works /10"],
          ["phase0-alt", "M03, M02", "", "", ""],
          ["phase2", "M01, M15 (City dock)", "", "", ""],
          ["phase3", "M05, then robo taxi", "", "", ""],
          ["Phase 5", "M06, M07, M11, part of M12", "", "", ""],
          ["Phase 6", "M13 (Mine dock)", "", "", ""]],
      0.7, 5.1, 8.4, [1.45, 3.35, 1.1, 1.2, 1.3], row_h=0.3, size=11,
      first_col=[RUN_GREEN, RUN_PURPLE, RUN_ORANGE, RUN_BLUE, RUN_GOLD])

s = template("T3", lead("Strategy"), "IDENTIFY", "Where our ideas came from", 25,
             "We compared six designs and spotted the wheel pattern. Then "
             "videos and building instructions: say what we changed, not "
             "'we copied it'.",
             "\"Now %s will show you the robot itself.\"" % next_up("Robot"),
             ["The six designs", "The wheel pattern", "One idea and where it came from",
              "What we changed from it"])
image(s, png("wheel-pattern"), 0.7, 1.85, w=5.2)
your_turn(s, 6.1, 1.85, 3.0, 5.05,
          "Our base is closest to: ...\n\nIdea we took, and from where: ...\n\n"
          "A video that helped, and what we changed: ...", size=13)

s = template("T4", lead("Robot"), "CREATE", "Why we chose this robot", 30,
             "Compare with HummerOne Pro, the easiest design. It is easy to "
             "build, but its blue wheels slip, it doesn't square up on a wall, "
             "and clip-on attachments are slow. Ours is a flat box that lines up "
             "on walls and lines, with grippy wheels and gravity mounting.",
             "\"The attachments are what make it work, so here they are.\"",
             ["Another robot as an example", "Flat box: lines up on walls and lines",
              "Which wheels, and why", "Gravity: last season's slow swaps",
              "A real photo"])
image(s, png("robot-compare"), 0.7, 1.75, w=5.2)
your_turn(s, 6.1, 1.75, 3.0, 5.15,
          "Photo of our robot from the side\n\nOur wheels: ...\nWhy: ...", size=13)

s = template("T5", lead("Robot"), "CREATE", "Our attachments", 35,
             "Hold up the attachment. What it does, what it was like before, "
             "what we changed and why. Then do a live swap: say how many "
             "seconds it takes.",
             "\"%s will explain the code that drives it.\"" % next_up("Code"),
             ["BOXOR frame and bevel gears", "Gravity mounting",
              "Before and after photos", "What we changed, and why",
              "Swap time, measured"])
your_turn(s, 0.7, 1.85, 4.1, 3.0, "Photo BEFORE: the first version")
your_turn(s, 5.0, 1.85, 4.1, 3.0, "Photo AFTER: what we use now")
your_turn(s, 0.7, 5.05, 8.4, 1.85,
          "We changed ... because ... . A swap takes __ seconds (timed 5 times).")

s = template("T6", lead("Code"), "CREATE", "The clever part of our code", 30,
             "Why Python: last year's code, more control, test every change. "
             "drive_cm came from last year: we only changed the wheel size from "
             "88 mm to 62.4 mm. "
             "Code in layers: the runs say what, the library says how. face "
             "measures from base: 1 degree off round a square, not 17. Then "
             "one thing you think is clever.",
             "\"Now %s will tell you about our sensors.\"" % next_up("Sensors"),
             ["Why Python, in your words", "drive_cm from last year, new wheel size",
              "Layers: what and how",
              "face: 1 degree, not 17", "One clever thing, in your words",
              "A flowchart of one run"])
image(s, png("code-layers"), 0.7, 1.85, w=4.2)
image(s, png("face-square"), 5.0, 1.85, w=4.1)
your_turn(s, 0.7, 5.05, 8.4, 1.85,
          "The cleverest thing in our code is ... because ...")

s = template("T7", lead("Sensors"), "CREATE", "How the robot finds its way", 60,
             "The gyro correction in 4 steps: read the error, work out the "
             "steer, steer, repeat 66 times a second. Then the gyro for "
             "direction, the motor encoders for distance. We "
             "measured both turns, and the gyro turn won. Then why we don't "
             "use the colour sensors.",
             "\"Now %s will tell you how we test, and about our team.\"" % next_up("Iteration and team"),
             ["What yaw is", "Zero, turn, drive straight", "The correction in 4 steps",
              "The 5-degree example", "The measured turn numbers",
              "The agreed colour sensor answer"])
table(s, [["Turn", "Time", "How far off"],
          ["Old turn (counting wheels)", "1.54 s", "4.26 degrees"],
          ["Gyro turn", "1.18 s", "0.58 degrees"]],
      0.7, 1.9, 8.4, [4.2, 2.0, 2.2], row_h=0.6, size=15)
your_turn(s, 0.7, 4.0, 8.4, 2.9,
          "Yaw is: ...\n\nThe three gyroscope steps, in your words: ...\n\n"
          "Why only the gyroscope, not the colour sensors: ...")

s = template("T8", lead("Iteration and team"), "ITERATE", "How we know it works", 30,
             "We tested each run 10 times. Read the numbers. Point at one "
             "change that made a number go up.",
             "\"Here is one fix in detail.\"",
             ["Every run tested 10 times", "Real numbers, with dates",
              "A before and after for one change"])
table(s, [["Run", "Before change", "What we changed", "After change"],
          ["", "__ / 10", "", "__ / 10"], ["", "__ / 10", "", "__ / 10"],
          ["", "__ / 10", "", "__ / 10"], ["", "__ / 10", "", "__ / 10"]],
      0.7, 1.9, 8.4, [1.9, 1.7, 3.1, 1.7], row_h=0.6, size=14)
your_turn(s, 0.7, 5.15, 8.4, 1.75,
          "Our tests: pretend robot first, then 34 automatic checks, then the real mat.")

s = template("T9", lead("Iteration and team"), "ITERATE", "A fix, start to finish", 40,
             "Tell the arm story, or your own: problem, how we found out, what "
             "we changed, the result with a number. Say what failed on the way.",
             "\"And now, our team.\"",
             ["Problem", "How we found out", "What we changed",
              "Result with a number", "Something that failed first"])
image(s, png("iterate-loop"), 0.7, 1.85, w=4.2)
your_turn(s, 5.1, 1.85, 4.0, 5.05,
          "Problem: ...\n\nHow we found out: ...\n\nWhat we changed: ...\n\n"
          "Result: __ out of 10", size=13)

s = template("T10", lead("Iteration and team"), "DESIGN", "Everyone built. Everyone coded.", 30,
             "Each person points at their row, or says it themselves in one "
             "breath. Then how we shared the work: roles, swapping, voting.",
             "\"And what we learned.\"",
             ["All five rows filled", "Everyone built AND coded",
              "One idea from each person", "How we decided things"])
table(s, [["", "I built", "I coded", "An idea I had"],
          [person("Kid 1"), "", "", ""], [person("Kid 2"), "", "", ""],
          [person("Kid 3"), "", "", ""], [person("Kid 4"), "", "", ""],
          [person("Kid 5"), "", "", ""]],
      0.7, 1.9, 8.4, [1.2, 2.4, 2.4, 2.4], row_h=0.55, size=14)
your_turn(s, 0.7, 5.4, 8.4, 1.5, "How we shared the work and decided things: ...")

s = template("T11", lead("Iteration and team"), "COMMUNICATE", "What we learned, and what we're proud of", 35,
             "Each person says one lesson, one sentence each. Then what we are "
             "proudest of. Say it like you mean it: this row is about pride.",
             "\"Thank you. Ask any of us anything.\"",
             ["One lesson from each person", "Lessons, not just events",
              "What we're proud of", "Everyone sounds proud"])
your_turn(s, 0.7, 1.85, 8.4, 3.1,
          "\n".join("%s learned: ..." % person(k) for k in SLOTS), size=14)
your_turn(s, 0.7, 5.15, 8.4, 1.75,
          "We are most proud of: ... (check any number before we say it)")

# =============================================================================
# PART 3: PUTTING IT TOGETHER
# =============================================================================
divider("3", "Put it together",
        "Next class: join the slides, practise the 5 minutes, then practise "
        "the questions.")

s = slide()
eyebrow(s, "Speaking order  ·  5 minutes")
title(s, "Who speaks when")
table(s, [["Time", "Slides", "Who", "Row"],
          ["0:00 to 1:10", "T1, T2, T3", lead("Strategy"), "Intro, IDENTIFY"],
          ["1:10 to 2:15", "T4, T5 and a live swap", lead("Robot"), "CREATE: robot and attachments"],
          ["2:15 to 3:00", "T6", lead("Code"), "CREATE: code"],
          ["3:00 to 4:00", "T7", lead("Sensors"), "CREATE: sensors"],
          ["4:00 to 5:00", "T8, T9, T10, T11", lead("Iteration and team"), "ITERATE. DESIGN, COMMUNICATE"]],
      0.7, 1.75, 11.9, [1.9, 3.0, 3.3, 3.7], row_h=0.6, size=14)
text(s, "End every part with the handover line in the speaker notes. Practise "
        "the handovers more than the parts.", 0.7, 5.6, 11.9, 1.0, size=16,
     color=INK)
notes(s, "If a kid is away, their backup takes the part. Backups are in "
         "robot-design/presentation.md.")

s = slide()
eyebrow(s, "Rehearsal  ·  next class")
title(s, "Practise like the real room")
table(s, [["Step", "How", "Why"],
          ["1. Time it", "Run the 5 minutes with a timer. Stop at 5:00.", "Judges stop us on time."],
          ["2. Handovers", "Only the handover lines, three times.", "That is where teams stumble."],
          ["3. Question drill", "Coach reads a question, points at anyone. Answer in 30 seconds.", "Judges pick who answers."],
          ["4. Swap parts", "Present someone else's minute.", "Shows what we can't explain yet."],
          ["5. Mock judge", "A grown-up who isn't the coach asks the questions.", "Awkward questions, before the real ones."]],
      0.7, 1.75, 11.9, [2.2, 6.0, 3.7], row_h=0.66, size=14)
text(s, "Questions for the drill are in robot-design/presentation.md.", 0.7,
     6.0, 11.9, 0.6, size=15, color=MUTED)
notes(s, "Write down every question nobody could answer. Find the answer "
         "before the next practice.")

s = slide()
eyebrow(s, "Discussion  ·  end of next class")
title(s, "Talk about it together")
bullets(s, [
    "Which parts of our robot show test, find a problem, change it, test again?",
    "How does our presentation show what each of us did?",
    "Which answer are we still unsure about? Who will find out, and by when?",
    "If a judge asks something none of us knows, what do we say?",
    "What are we proudest of this season, and how do we show it?",
], y=1.9, size=19)
notes(s, "The first two come from FIRST's own Team Meeting Guide, Session 11. "
         "For the fourth: 'I don't know, but here is how we would find out' is "
         "a good answer. A made-up one is not.")

s = slide()
eyebrow(s, "Before judging day")
title(s, "Our Exceeds checklist")
table(s, [["Row", "Accomplished needs", "Exceeds evidence we bring", "☐"],
          ["IDENTIFY", "Clear mission strategy, clear use of resources",
           "Missions table with points, seconds, works /10. The six designs.", "☐"],
          ["DESIGN", "All of us had ideas, all can build and code",
           "T10 filled. Anyone answers about anyone's part.", "☐"],
          ["CREATE", "Innovative attachments and code, clearly explained",
           "Before and after attachments. Measured turn numbers. Swap time.", "☐"],
          ["ITERATE", "Repeated testing, improvements from testing",
           "10-run numbers, before and after. The printed arm log.", "☐"],
          ["COMMUNICATE", "Detailed process and lessons, clear pride",
           "One lesson each. Smooth handovers. We sound proud.", "☐"]],
      0.7, 1.75, 11.9, [1.8, 4.2, 5.3, 0.6], row_h=0.78, size=13)
notes(s, "Rubric wording is from the official BIOGLOW Robot Design rubric. "
         "Exceeds has no set wording: the judge writes a comment, so the "
         "third column is what we hope they write.")

prs.save(OUT)
print("wrote", os.path.relpath(OUT, REPO), "with", len(prs.slides), "slides")


# =============================================================================
# THE HTML COPY
# =============================================================================
PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Going for Exceeds in Robot Design: class workshop, BIOGLOW</title>
<style>
  /* Generated by tools/make-exceeds-pptx.py from the same calls as
     exceeds-workshop.pptx. Do not edit by hand: change the script and run it.

     Each slide is 13.333 by 7.5 units, the PowerPoint size in inches. --u is
     one unit, sized so a whole slide fits the screen. Scrolling moves between
     slides with no JavaScript. The small script at the end adds arrow keys,
     space, PageUp and PageDown, and the buttons in the corner. */
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root { --u: min(calc(100vw / 13.333), calc(100vh / 7.5)); }
  html { scroll-snap-type: y mandatory; background: #0e221b; }
  body { font-family: 'Trebuchet MS', 'Segoe UI', system-ui, sans-serif; }
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
  body { counter-reset: slide; }
  .t { position: absolute; white-space: pre-wrap; overflow-wrap: break-word; }
  .r { position: absolute; border-radius: calc(0.08 * var(--u)); }
  img { position: absolute; display: block; }
  table { position: absolute; border-collapse: collapse; table-layout: fixed; }
  td {
    padding: calc(0.05 * var(--u)) calc(0.1 * var(--u));
    border: calc(0.01 * var(--u)) solid GREY; vertical-align: middle;
    line-height: 1.25;
  }
  details.notes {
    position: absolute; left: calc(0.7 * var(--u)); bottom: calc(0.15 * var(--u));
    max-width: calc(11.9 * var(--u)); font-size: calc(0.15 * var(--u)); z-index: 5;
  }
  details.notes summary {
    cursor: pointer; color: SOFT; list-style: none;
    font-size: calc(0.13 * var(--u)); letter-spacing: 0.08em;
  }
  details.notes[open] summary { color: ACCENT; }
  details.notes p {
    margin-top: calc(0.08 * var(--u)); padding: calc(0.15 * var(--u)) calc(0.2 * var(--u));
    background: #fff; color: INK; border: calc(0.015 * var(--u)) solid ACCENT;
    border-radius: calc(0.08 * var(--u)); white-space: pre-wrap; line-height: 1.4;
    box-shadow: 0 calc(0.05 * var(--u)) calc(0.2 * var(--u)) rgba(0,0,0,0.2);
  }
  .nav {
    position: fixed; right: 14px; bottom: 14px; z-index: 10;
    display: flex; gap: 6px; align-items: center;
    font: 600 13px 'Trebuchet MS', sans-serif; color: #fff;
  }
  .nav button {
    width: 38px; height: 38px; border-radius: 19px; border: 0; cursor: pointer;
    background: rgba(22, 54, 43, 0.85); color: #fff; font-size: 18px;
  }
  .nav button:hover { background: ACCENT; }
  .nav span { background: rgba(22, 54, 43, 0.85); padding: 9px 12px; border-radius: 19px; }
  @media print {
    .nav { display: none; }
    :root { --u: 0.75in; }
    @page { size: 10in 5.625in; margin: 0; }
    html { scroll-snap-type: none; background: #fff; }
    section { height: auto; page-break-after: always; }
    details.notes { display: none; }
  }
</style>
</head>
<body>
"""
for key, value in (("PAPER", PAPER), ("INK", INK), ("SOFT", SOFT),
                   ("ACCENT", ACCENT), ("GREY", GREY)):
    PAGE = PAGE.replace(key, _hex(value))

out = [PAGE]
for entry in HTML_SLIDES:
    out.append("<section><div class='slide%s'>" % (" dark" if entry["dark"] else ""))
    out.extend(entry["parts"])
    if entry["notes"]:
        out.append("<details class='notes'><summary>NOTES</summary><p>%s</p></details>"
                   % html.escape(entry["notes"]))
    out.append("</div></section>\n")
out.append("""<div class="nav"><button id="prev" aria-label="Previous slide">&#8249;</button>
<span id="where"></span><button id="next" aria-label="Next slide">&#8250;</button></div>
<script>
// Move one slide at a time. Works in every browser, and after clicking a link.
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
    // Instant, not smooth: a smooth scroll fights scroll-snap in Safari.
    window.scrollTo(0, slides[i].offsetTop);
    show();
  }
  function show() {
    document.getElementById('where').textContent = (current() + 1) + ' / ' + slides.length;
  }
  document.getElementById('prev').onclick = function () { go(current() - 1); };
  document.getElementById('next').onclick = function () { go(current() + 1); };
  document.addEventListener('keydown', function (e) {
    if (e.target.closest && e.target.closest('summary')) return;
    var k = e.key;
    if (k === 'ArrowRight' || k === 'ArrowDown' || k === 'PageDown' || k === ' ') {
      e.preventDefault(); go(current() + 1);
    } else if (k === 'ArrowLeft' || k === 'ArrowUp' || k === 'PageUp') {
      e.preventDefault(); go(current() - 1);
    } else if (k === 'Home') { e.preventDefault(); go(0); }
    else if (k === 'End') { e.preventDefault(); go(slides.length - 1); }
  });
  window.addEventListener('scroll', show, { passive: true });
  show();
})();
</script>
""")
out.append("</body>\n</html>\n")
with open(OUT_HTML, "w", encoding="utf-8") as fh:
    fh.write("".join(out))
print("wrote", os.path.relpath(OUT_HTML, REPO), "with", len(HTML_SLIDES), "slides")
