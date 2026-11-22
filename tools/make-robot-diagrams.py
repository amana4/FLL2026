"""Draws the diagrams on robot-design/our-robot-explained.md and
robot-design/how-our-code-works.md.

Run: python3 tools/make-robot-diagrams.py robot-design/diagrams

Writes every .svg in robot-design/diagrams/. Edit the text
or numbers here and re-run, rather than editing the SVG files by hand.
"""
import math, sys, os
out = sys.argv[1]
LEAF='#1b6b47'; LEAFL='#2e8f61'; INK='#1f2933'; MUTE='#5f6b76'; RED='#c0392b'; PALE='#e8f3ee'; LINE='#9aa5ad'
FONT='font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif"'
def svg(w,h,title,desc,body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" {FONT}>
<title id="t">{title}</title>
<desc id="d">{desc}</desc>
<rect width="{w}" height="{h}" rx="16" fill="#ffffff"/>
{body}
</svg>
'''
def text(x,y,s,size=18,fill=INK,anchor='middle',weight='normal'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'

# 1. Wiring map, top view, schematic
b=[]
b.append(text(400,40,'Our robot from above',24,INK,weight='bold'))
b.append(text(400,66,'A map of what is plugged in where. Not to scale.',16,MUTE))
# arrow showing driving direction (backwards, down the page)
b.append(text(400,96,'FRONT',16,MUTE,weight='bold'))
# chassis
b.append(f'<rect x="200" y="110" width="400" height="300" rx="6" fill="{PALE}" stroke="{LEAF}" stroke-width="7"/>')
b.append(text(400, 140, 'straight, flat walls all round', 14, LEAF, weight='bold'))
# hub
b.append(f'<rect x="320" y="170" width="160" height="150" rx="14" fill="#ffffff" stroke="{INK}" stroke-width="3"/>')
b.append(text(400,235,'Hub',22,INK,weight='bold'))
b.append(text(400,260,'gyro inside',15,MUTE))
b.append(text(400,282,'face up, button on top',15,MUTE))
# wheels
for x,lab,sock in ((250,'Left wheel','F'),(550,'Right wheel','A')):
    b.append(f'<rect x="{x-25}" y="200" width="50" height="110" rx="12" fill="{INK}"/>')
    b.append(f'<circle cx="{x}" cy="255" r="20" fill="{LEAF}" stroke="#ffffff" stroke-width="3"/>')
    b.append(text(x,262,sock,20,'#ffffff',weight='bold'))
    tx = 105 if x<400 else 695
    b.append(text(tx,248,lab,17,INK,weight='bold'))
    b.append(text(tx,270,f'motor on {sock}',16,MUTE))
# attachment at back
b.append(f'<rect x="270" y="410" width="260" height="70" rx="12" fill="#fff4d6" stroke="#b7791f" stroke-width="3"/>')
b.append(text(400,440,'Attachment (BOXOR frame)',17,INK,weight='bold'))
for x,s in ((335,'C'),(465,'E')):
    b.append(f'<circle cx="{x}" cy="462" r="15" fill="#b7791f"/>')
    b.append(text(x,468,s,17,'#ffffff',weight='bold'))
b.append(text(400,467,'motors',14,MUTE))
b.append(text(400,505,'BACK',16,MUTE,weight='bold'))
# drive arrow
b.append(f'<line x1="680" y1="380" x2="680" y2="490" stroke="{LEAF}" stroke-width="6" stroke-linecap="round"/>')
b.append(f'<polygon points="666,485 694,485 680,510" fill="{LEAF}"/>')
b.append(text(690,540,'drives backwards',16,LEAF,weight='bold'))
b.append(text(690,560,'into the models',16,LEAF,weight='bold'))
b.append(text(400,585,'The wheels sit inside the frame. Socket letters F, A, C and E come from our final code.',15,MUTE))
open(os.path.join(out,'robot-wiring.svg'),'w').write(svg(800,610,'Our robot from above: what is plugged in where',
 'Schematic top view. The frame has straight, flat walls, and the wheels sit inside it. The left wheel motor is on socket F and the right wheel motor on socket A. The hub sits in the middle, face up. The attachment is on the back, with motors on sockets C and E. The robot drives backwards into the models.',''.join(b)))

# 2. Square test: turn-by vs face
def path(errs, side=150, ox=0, oy=0):
    x,y,h=0.0,0.0,0.0
    pts=[(x,y)]
    for e in errs:
        x+=side*math.cos(math.radians(h)); y+=side*math.sin(math.radians(h)); pts.append((x,y))
        h=e
    return pts
# turn-by: each turn 4.25 short, errors pile up (headings 0, 85.75, 171.5, 257.25) -> ends 17 off
turn_h=[0, 90-4.25, 180-8.5, 270-12.75]
face_h=[0, 90-1.0, 180+0.8, 270-1.0]
def draw(headings, cx, cy, color, label1, label2):
    side=150; x,y=0.0,0.0; pts=[(x,y)]
    for h in headings:
        # screen y grows downward; turn left = negative angle on screen
        x+=side*math.cos(math.radians(-h)); y+=side*math.sin(math.radians(-h)); pts.append((x,y))
    s=[]
    # ideal square, dashed
    sq=[(0,0),(side,0),(side,-side),(0,-side),(0,0)]
    s.append('<polyline fill="none" stroke="%s" stroke-width="2" stroke-dasharray="6 6" points="%s"/>'%(LINE,' '.join(f'{cx+px:.1f},{cy+py:.1f}' for px,py in sq)))
    s.append('<polyline fill="none" stroke="%s" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" points="%s"/>'%(color,' '.join(f'{cx+px:.1f},{cy+py:.1f}' for px,py in pts)))
    s.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{INK}"/>')
    ex,ey=pts[-1]
    s.append(f'<circle cx="{cx+ex:.1f}" cy="{cy+ey:.1f}" r="9" fill="{color}"/>')
    s.append(text(cx-14,cy+30,'start',15,INK,'end'))
    s.append(text(cx+side/2,cy+70,label1,20,INK,weight='bold'))
    s.append(text(cx+side/2,cy+96,label2,18,color,weight='bold'))
    return ''.join(s), pts
b=[text(450,40,'Drive round a square: four turns',24,INK,weight='bold'),
   text(450,66,'The dashed line is a perfect square. The thick line is where the robot goes.',16,MUTE)]
s1,_=draw(turn_h,110,290,RED,'Turn 90 degrees each time','ends 17 degrees off')
s2,_=draw(face_h,580,290,LEAF,'face(90), face(180) ...','ends about 1 degree off')
b+= [s1,s2]
b.append(text(450,450,'Each small mistake gets added to the next turn.',16,RED))
b.append(text(450,474,'face measures every turn from base, so mistakes do not add up.',16,LEAF))
open(os.path.join(out,'face-square.svg'),'w').write(svg(900,500,'Drive round a square: turning by 90 degrees against using face',
 'Two paths round a square. On the left, the robot turns 90 degrees each time; each turn is a little short, the mistakes add up, and it ends 17 degrees off. On the right, the robot uses face, which measures from base; it ends about 1 degree off.',''.join(b)))

# 3. Iterate loop
b=[text(450,40,'How we make the robot better',24,INK,weight='bold'),
   text(450,66,'This is what ITERATE means. Example from M03 Flip the Rock.',16,MUTE)]
cx,cy,r=450,300,165
steps=[('1. Test it','Run M03 on the mat.'),('2. Find a problem','The bump knocks the','robot crooked.'),
       ('3. Change something','Add await face(0)','right after the bump.'),('4. Test again','Is it straight now?','Write it in the log.')]
ang=[-90,0,90,180]
for i,(st,*lines) in enumerate(steps):
    a=math.radians(ang[i]); x=cx+r*math.cos(a)*1.35; y=cy+r*math.sin(a)
    b.append(f'<rect x="{x-120:.0f}" y="{y-42:.0f}" width="240" height="{84 if len(lines)>1 else 70}" rx="14" fill="{PALE}" stroke="{LEAF}" stroke-width="3"/>')
    b.append(text(x,y-14,st,19,LEAF,weight='bold'))
    for j,l in enumerate(lines):
        b.append(text(x,y+10+j*21,l,15,INK))
# arrows between boxes, drawn by hand so they stop short of each box
b.insert(0,f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="16" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{LEAFL}"/></marker></defs>')
for d in ("M574,128 Q650,130 660,248", "M673,350 Q673,465 582,465",
          "M318,465 Q227,465 227,352", "M227,252 Q227,128 318,128"):
    b.append(f'<path d="{d}" fill="none" stroke="{LEAFL}" stroke-width="4" marker-end="url(#ah)"/>')
b.append(text(cx,cy+6,'repeat',20,MUTE,weight='bold'))
open(os.path.join(out,'iterate-loop.svg'),'w').write(svg(900,560,'How we make the robot better: test, find a problem, change something, test again',
 'A loop of four steps. 1, test it: run M03 on the mat. 2, find a problem: the bump knocks the robot crooked. 3, change something: add await face(0) right after the bump. 4, test again and write it in the log. Then repeat.',''.join(b)))
print('ok')

# ---------------------------------------------------------------------------
# Diagrams for robot-design/how-our-code-works.md
# ---------------------------------------------------------------------------
GOLD='#b7791f'; GOLDP='#fff4d6'; REDP='#fdecea'; BLUE='#2b6cb0'; BLUEP='#e6f0fa'

def wrap_lines(cx, cy, lines, size=16, fill=INK, weight='normal', gap=None):
    gap = gap or size + 5
    y0 = cy - (len(lines) - 1) * gap / 2 + size * 0.35
    return ''.join(text(cx, y0 + i * gap, l, size, fill, weight=weight if i == 0 else 'normal')
                   for i, l in enumerate(lines))

def node(kind, cx, cy, w, h, lines, size=16):
    if kind == 'start':
        shape = f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="{h/2}" fill="{LEAF}"/>'
        return shape + wrap_lines(cx, cy, lines, size, '#ffffff', 'bold')
    if kind == 'end':
        shape = f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="{h/2}" fill="{INK}"/>'
        return shape + wrap_lines(cx, cy, lines, size, '#ffffff', 'bold')
    if kind == 'stop':
        shape = f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="12" fill="{REDP}" stroke="{RED}" stroke-width="2.5"/>'
        return shape + wrap_lines(cx, cy, lines, size, RED, 'bold')
    if kind == 'ask':
        pts = f'{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}'
        shape = f'<polygon points="{pts}" fill="{GOLDP}" stroke="{GOLD}" stroke-width="2.5"/>'
        return shape + wrap_lines(cx, cy, lines, size, INK, 'bold')
    # step
    shape = f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="10" fill="{PALE}" stroke="{LEAF}" stroke-width="2.5"/>'
    return shape + wrap_lines(cx, cy, lines, size, INK, 'bold')

ARROW_DEFS = (f'<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" '
              f'markerWidth="12" markerHeight="12" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{MUTE}"/></marker></defs>')

def arrow(pts, label=None, lx=None, ly=None, color=MUTE):
    p = ' '.join(f'{x},{y}' for x, y in pts)
    s = f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="2.5" marker-end="url(#ar)"/>'
    if label:
        s += text(lx, ly, label, 15, color, 'middle', 'bold')
    return s

def save(name, w, h, title, desc, parts):
    open(os.path.join(out, name), 'w').write(svg(w, h, title, desc, ARROW_DEFS + ''.join(parts)))

# A. Layers ------------------------------------------------------------------
p = [text(450, 40, 'Our code is built in layers', 24, INK, weight='bold'),
     text(450, 66, 'Each layer only uses the layer under it.', 16, MUTE)]
layers = [
    (GOLDP, GOLD, 'Run programs', 'phase0-alt.py, phase3.py, Phase 5.py, Phase 6.py',
     'Says WHAT to do: "back 44 cm, then face 90"'),
    (PALE, LEAF, 'Our library: advanced.py', 'drive_cm, face, turn_deg, arc_turn, attachments, safety stops',
     'Says HOW to do it: speed up, steer with the gyro, stop exactly'),
    (BLUEP, BLUE, 'The SPIKE hub', 'motors on F, A, C, E, the gyro, the wheel encoders',
     'Does it: turns the motors, measures the turn'),
]
for i, (fill, stroke, t1, t2, t3) in enumerate(layers):
    y = 100 + i * 140
    p.append(f'<rect x="90" y="{y}" width="720" height="110" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
    p.append(text(450, y + 36, t1, 21, INK, weight='bold'))
    p.append(text(450, y + 63, t2, 16, INK))
    p.append(text(450, y + 89, t3, 16, stroke, weight='bold'))
    if i < 2:
        p.append(arrow([(450, y + 112), (450, y + 136)]))
p.append(text(450, 540, 'Like My Blocks: we write drive_cm once, and every run uses it.', 16, MUTE))
save('code-layers.svg', 900, 570, 'Our code is built in layers',
     'Three layers. At the top, the run programs say what to do, such as back 44 cm then face 90. In the middle, '
     'our library advanced.py says how: drive_cm, face, turn_deg, arc_turn, attachments and safety stops. At the '
     'bottom, the SPIKE hub turns the motors and measures with the gyro and encoders.', p)

# B. Build flow --------------------------------------------------------------
p = [text(450, 40, 'One library, copied into every run by a tool', 24, INK, weight='bold'),
     text(450, 66, 'The SPIKE app cannot load one file from another, so each run carries its own copy.', 16, MUTE)]
p.append(node('step', 160, 170, 220, 90, ['advanced.py', 'our one library']))
p.append(node('ask', 160, 330, 230, 120, ['34 checks pass', 'on the pretend', 'hub?'], 15))
p.append(arrow([(160, 215), (160, 268)]))
p.append(node('stop', 160, 470, 200, 64, ['Fix the library', 'first']))
p.append(arrow([(160, 390), (160, 436)], 'no', 182, 416, RED))
p.append(node('step', 450, 330, 220, 90, ['build-mission.py', 'copies it in']))
p.append(arrow([(275, 330), (338, 330)], 'yes', 306, 318, LEAF))
# run file
p.append(f'<rect x="630" y="200" width="220" height="260" rx="12" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>')
p.append(text(740, 190, 'phase0-alt.py', 17, INK, weight='bold'))
p.append(f'<rect x="642" y="212" width="196" height="120" rx="8" fill="{PALE}"/>')
p.append(wrap_lines(740, 272, ['Top part:', 'the library,', 'replaced every time'], 15))
p.append(f'<line x1="642" y1="345" x2="838" y2="345" stroke="{RED}" stroke-width="2.5" stroke-dasharray="8 5"/>')
p.append(text(740, 366, 'the marker line', 14, RED, weight='bold'))
p.append(f'<rect x="642" y="378" width="196" height="70" rx="8" fill="{GOLDP}"/>')
p.append(wrap_lines(740, 413, ['Bottom part: our mission,', 'never touched'], 15))
p.append(arrow([(562, 330), (628, 330)]))
p.append(node('end', 740, 530, 220, 56, ['Load onto the hub']))
p.append(arrow([(740, 462), (740, 500)]))
p.append(text(450, 600, 'Copying by hand once left a wrong note about the motor sockets in M03. The tool cannot make that mistake.', 15, MUTE))
save('build-flow.svg', 900, 630, 'One library, copied into every run by a tool',
     'advanced.py is checked by 34 checks on the pretend hub. If they pass, build-mission.py copies the library into '
     'the top part of each run file, above a marker line. The mission code below the marker line is never touched. '
     'Then the file is loaded onto the hub.', p)

# C. drive_cm flowchart ------------------------------------------------------
p = [text(450, 40, 'How drive_cm drives straight', 24, INK, weight='bold'),
     text(450, 66, 'This loop runs about 66 times every second.', 16, MUTE)]
X = 330
p.append(node('start', X, 110, 240, 50, ['drive_cm(-44)']))
p.append(node('ask', X, 210, 270, 110, ['Longer than', 'the mat (200 cm)?'], 15))
p.append(arrow([(X, 135), (X, 154)]))
p.append(node('stop', 700, 210, 250, 64, ['Stop: "longer than', 'the mat"'], 15))
p.append(arrow([(X + 136, 210), (574, 210)], 'yes', 520, 198, RED))
p.append(node('step', X, 335, 330, 76, ['Work out the speed and ramp.', 'Aim a little short: it rolls.'], 15))
p.append(arrow([(X, 266), (X, 296)], 'no', X + 20, 286, LEAF))
p.append(node('step', X, 435, 330, 56, ['Zero the wheel counters and gyro'], 15))
p.append(arrow([(X, 374), (X, 406)]))
p.append(node('ask', X, 545, 270, 110, ['Gone far', 'enough?'], 16))
p.append(arrow([(X, 464), (X, 489)]))
p.append(node('end', 700, 545, 200, 56, ['Brake. Done.']))
p.append(arrow([(X + 136, 545), (598, 545)], 'yes', 520, 533, LEAF))
p.append(node('step', X, 665, 330, 76, ['Pick the speed:', 'speed up, hold, or slow down'], 15))
p.append(arrow([(X, 601), (X, 626)], 'no', X + 20, 618, RED))
p.append(node('step', X, 765, 330, 56, ['Read the gyro: how far off straight?'], 15))
p.append(arrow([(X, 704), (X, 736)]))
p.append(node('ask', X, 875, 270, 110, ['More than', '45 degrees off?'], 15))
p.append(arrow([(X, 794), (X, 819)]))
p.append(node('stop', 700, 875, 250, 64, ['Brake. Stop with', 'an error.'], 15))
p.append(arrow([(X + 136, 875), (574, 875)], 'yes', 520, 863, RED))
p.append(node('step', X, 995, 330, 76, ['Steer the other way,', 'harder if it is further off'], 15))
p.append(arrow([(X, 931), (X, 956)], 'no', X + 20, 948, LEAF))
p.append(node('step', X, 1090, 330, 50, ['Wait 15 milliseconds'], 15))
p.append(arrow([(X, 1034), (X, 1064)]))
p.append(arrow([(X - 165, 1090), (90, 1090), (90, 545), (X - 138, 545)], 'loop', 70, 820, LEAF))
save('drive-flowchart.svg', 900, 1140, 'Flowchart: how drive_cm drives straight',
     'drive_cm first refuses any distance longer than the 200 cm mat. It works out the speed and ramp, aims a little '
     'short because the robot rolls after braking, and zeroes the wheel counters and gyro. Then it loops: if it has '
     'gone far enough it brakes and is done. If not, it picks the speed, reads how far off straight it is, stops with '
     'an error if that is more than 45 degrees, otherwise steers the other way, waits 15 milliseconds and loops.', p)

# D. face flowchart ----------------------------------------------------------
p = [text(450, 40, 'How face turns to exactly the right direction', 24, INK, weight='bold'),
     text(450, 66, 'The gyro is checked about 66 times every second.', 16, MUTE)]
X = 300
p.append(node('start', X, 110, 240, 50, ['face(90)']))
p.append(node('step', X, 200, 340, 76, ['How far is 90 from where we', 'point now? That is the error.'], 15))
p.append(arrow([(X, 135), (X, 161)]))
p.append(node('ask', X, 330, 270, 110, ['Error less than', '1 degree?'], 15))
p.append(arrow([(X, 239), (X, 274)]))
p.append(node('step', 700, 330, 230, 70, ['Brake. Wait', '0.15 seconds.'], 15))
p.append(arrow([(X + 136, 330), (584, 330)], 'yes', 510, 318, LEAF))
p.append(node('ask', 700, 470, 250, 120, ['Still less than', '1 degree off?'], 15))
p.append(arrow([(700, 366), (700, 409)]))
p.append(node('end', 700, 610, 160, 52, ['Done']))
p.append(arrow([(700, 531), (700, 583)], 'yes', 720, 562, LEAF))
p.append(arrow([(826, 470), (870, 470), (870, 200), (X + 172, 200)]))
p.append(text(686, 190, 'no: it rolled past, so go again', 15, GOLD, weight='bold'))
p.append(node('step', X, 500, 380, 116, ['Work out the turning speed:', 'far off: turn fast', 'close: turn slowly', 'stuck a bit short: push a bit more'], 15))
p.append(arrow([(X, 386), (X, 440)], 'no', X + 20, 418, RED))
p.append(node('step', X, 630, 340, 56, ['Spin the wheels opposite ways'], 15))
p.append(arrow([(X, 559), (X, 600)]))
p.append(node('step', X, 730, 340, 50, ['Wait 15 milliseconds'], 15))
p.append(arrow([(X, 659), (X, 703)]))
p.append(arrow([(X - 171, 730), (70, 730), (70, 200), (X - 171, 200)], 'loop', 50, 470, LEAF))
save('face-flowchart.svg', 900, 790, 'Flowchart: how face turns to exactly the right direction',
     'face works out the error: how far the target is from where the robot points now. If the error is under 1 '
     'degree, it brakes, waits 0.15 seconds and checks again. If it is still under 1 degree it is done; if it rolled '
     'past, it goes again. If the error is not under 1 degree, it works out the turning speed, fast when far off, '
     'slow when close, a little extra push when stuck just short, spins the wheels opposite ways, waits 15 '
     'milliseconds and loops.', p)

# E. Speed ramp graph --------------------------------------------------------
top, start, ramp = 500.0, 262.0, 10.0
comp = 1.5 * top / 630.0
target = 44 - comp
gx, gy, gw, gh = 110, 110, 700, 300
def px(d): return gx + d / 45.0 * gw
def py(v): return gy + gh - v / 600.0 * gh
p = [text(450, 40, 'How fast drive_cm(-44) goes, all the way along', 24, INK, weight='bold'),
     text(450, 66, 'This is the M03 drive into the rock. Speed is in degrees per second of wheel turn.', 16, MUTE)]
for v in (0, 100, 200, 300, 400, 500, 600):
    p.append(f'<line x1="{gx}" y1="{py(v):.1f}" x2="{gx+gw}" y2="{py(v):.1f}" stroke="#e3e8ec" stroke-width="1"/>')
    p.append(text(gx - 10, py(v) + 5, str(v), 14, MUTE, 'end'))
for d in range(0, 46, 5):
    p.append(text(px(d), gy + gh + 24, str(d), 14, MUTE))
p.append(f'<line x1="{gx}" y1="{gy+gh}" x2="{gx+gw}" y2="{gy+gh}" stroke="{INK}" stroke-width="2"/>')
p.append(f'<line x1="{gx}" y1="{gy}" x2="{gx}" y2="{gy+gh}" stroke="{INK}" stroke-width="2"/>')
p.append(text(gx + gw / 2, gy + gh + 52, 'distance driven (cm)', 16, INK, weight='bold'))
p.append(f'<text x="{gx-62}" y="{gy+gh/2}" font-size="16" fill="{INK}" font-weight="bold" text-anchor="middle" transform="rotate(-90 {gx-62} {gy+gh/2})">speed</text>')
pts = [(0, start), (ramp, top), (target - ramp, top), (target, start)]
poly = ' '.join(f'{px(d):.1f},{py(v):.1f}' for d, v in pts)
area = f'{px(0):.1f},{py(0):.1f} ' + poly + f' {px(target):.1f},{py(0):.1f}'
p.append(f'<polygon points="{area}" fill="{PALE}"/>')
p.append(f'<polyline points="{poly}" fill="none" stroke="{LEAF}" stroke-width="5" stroke-linejoin="round"/>')
p.append(f'<line x1="{px(target):.1f}" y1="{py(0)}" x2="{px(target):.1f}" y2="{py(0)-8}" stroke="{RED}" stroke-width="3"/>')
p.append(f'<line x1="{px(target):.1f}" y1="{py(start)+4:.1f}" x2="{px(target):.1f}" y2="{py(0):.1f}" stroke="{RED}" stroke-width="2" stroke-dasharray="5 4"/>')
p.append(f'<line x1="{px(44):.1f}" y1="{py(0)}" x2="{px(44):.1f}" y2="{py(0)-70}" stroke="{INK}" stroke-width="2" stroke-dasharray="5 4"/>')
p.append(text(px(44) + 6, py(0) - 56, '44 cm', 14, INK, 'start', 'bold'))
p.append(text(px(5), py(130), 'speed up', 16, LEAF, weight='bold'))
p.append(text(px(5), py(130) + 20, 'so the wheels', 14, MUTE))
p.append(text(px(5), py(130) + 37, 'do not slip', 14, MUTE))
p.append(text(px(target / 2), py(top) - 14, 'hold the speed', 16, LEAF, weight='bold'))
p.append(text(px(target - 5), py(130), 'slow down', 16, LEAF, weight='bold'))
p.append(text(px(target - 5), py(130) + 20, 'so it does not', 14, MUTE))
p.append(text(px(target - 5), py(130) + 37, 'overshoot', 14, MUTE))
p.append(text(450, 520, f'It brakes about {comp:.1f} cm early, because the robot rolls a little after braking.', 15, RED))
save('speed-ramp.svg', 900, 550, 'Graph: how fast drive_cm(-44) goes along the drive',
     f'Speed starts at 262, rises to 500 over the first 10 cm so the wheels do not slip, holds at 500, and falls back '
     f'to 262 over the last 10 cm so the robot does not overshoot. It brakes about {comp:.1f} cm before 44 cm, '
     f'because the robot rolls a little after braking.', p)

# F. Whole run: phase0-alt ---------------------------------------------------
p = [text(450, 40, 'One whole run: phase0-alt.py', 24, INK, weight='bold'),
     text(450, 66, 'M03 Flip the Rock, then M02 Exploding Seeds, then home.', 16, MUTE)]
X = 450
steps = [
    ('start', ['Start in base']),
    ('step', ['init_robot: this way is now "base"']),
    ('step', ['Set calibration: 179/180']),
    ('mission', ['M03 Flip the Rock']),
    ('step', ['Back 44 cm into the rock']),
    ('step', ['face(0): straighten after the bump']),
    ('step', ['Forward 22 cm']),
    ('mission', ['M02 Exploding Seeds']),
    ('step', ['face(90), back 24 cm, face(46)']),
    ('step', ['Arm down: 380 degrees']),
    ('step', ['Back 22 cm']),
    ('step', ['Arm up 200 degrees']),
    ('both', ['Arm up 180 more AND drive 35 cm fast', 'at the same time']),
    ('end', ['Home']),
]
y = 110
prev = None
for kind, lines in steps:
    h = 46 if len(lines) == 1 else 64
    if kind == 'mission':
        p.append(f'<rect x="{X-230}" y="{y-16}" width="460" height="32" rx="6" fill="{GOLDP}"/>')
        p.append(text(X, y + 6, lines[0], 17, GOLD, weight='bold'))
        if prev is not None:
            p.append(f'<line x1="{X}" y1="{prev}" x2="{X}" y2="{y-17}" stroke="{MUTE}" stroke-width="2.5"/>')
        prev = y + 16
        y += 46
        continue
    if kind == 'both':
        p.append(f'<rect x="{X-210}" y="{y-h/2}" width="420" height="{h}" rx="10" fill="{BLUEP}" stroke="{BLUE}" stroke-width="2.5"/>')
        p.append(wrap_lines(X, y, lines, 15, INK, 'bold'))
    else:
        p.append(node(kind, X, y, 420 if kind == 'step' else 220, h, lines, 15))
    if prev is not None:
        p.append(arrow([(X, prev), (X, y - h / 2 - 2)]))
    prev = y + h / 2
    y += h + 26
H = y + 10
save('run-phase0-alt.svg', 900, int(H), 'Flowchart of one whole run: phase0-alt.py',
     'Start in base. init_robot makes this direction base. Set calibration 179/180. M03 Flip the Rock: back 44 cm into '
     'the rock, face(0) to straighten after the bump, forward 22 cm. M02 Exploding Seeds: face(90), back 24 cm, '
     'face(46), arm down 380 degrees, back 22 cm, arm up 200 degrees, then arm up 180 more and drive 35 cm fast at '
     'the same time, and home.', p)

# G. How we test code --------------------------------------------------------
p = [text(450, 40, 'How we test our code', 24, INK, weight='bold'),
     text(450, 66, 'Cheap, fast tests first. The real mat last.', 16, MUTE)]
stages = [
    (BLUEP, BLUE, '1. Pretend robot', ['Run the code on a', 'pretend mat in the', 'browser. No robot', 'needed.']),
    (PALE, LEAF, '2. Automatic checks', ['check-library.py', 'runs 34 checks on', 'the pretend hub in', 'seconds.']),
    (GOLDP, GOLD, '3. Real mat', ['Run it, measure it,', 'change a number.', 'The #was notes', 'show this.']),
    ('#f1f3f5', INK, '4. Save in git', ['Every change is', 'saved with a note.', '33 saves to our', 'code so far.']),
]
for i, (fill, stroke, t, lines) in enumerate(stages):
    x = 40 + i * 215
    p.append(f'<rect x="{x}" y="110" width="190" height="210" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
    p.append(text(x + 95, 145, t, 17, stroke, weight='bold'))
    for j, l in enumerate(lines):
        p.append(text(x + 95, 190 + j * 26, l, 15, INK))
    if i < 3:
        p.append(arrow([(x + 192, 215), (x + 213, 215)]))
p.append(f'<path d="M800,330 Q800,390 450,390 Q100,390 100,334" fill="none" stroke="{LEAFL}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#ar)"/>')
p.append(text(450, 420, 'Found a problem? Go round again.', 16, LEAF, weight='bold'))
save('test-pipeline.svg', 900, 450, 'How we test our code: pretend robot, automatic checks, real mat, save in git',
     'Four steps from left to right. 1, pretend robot: run the code on a pretend mat in the browser. 2, automatic '
     'checks: check-library.py runs 34 checks on the pretend hub in seconds. 3, real mat: run it, measure it, change '
     'a number. 4, save in git with a note; 33 saves to our code so far. If a problem is found, go round again.', p)

# H. Squaring against a wall --------------------------------------------------
WALL = '#8a949c'
def robot_box(cx, cy, w, h, angle, label=None):
    g = (f'<g transform="rotate({angle} {cx} {cy})">'
         f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="5" fill="{PALE}" stroke="{LEAF}" stroke-width="6"/>'
         f'<rect x="{cx-w/2+14}" y="{cy-30}" width="22" height="60" rx="6" fill="{INK}"/>'
         f'<rect x="{cx+w/2-36}" y="{cy-30}" width="22" height="60" rx="6" fill="{INK}"/>'
         f'<rect x="{cx-38}" y="{cy-34}" width="76" height="68" rx="8" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>'
         '</g>')
    return g
p = [text(450, 40, 'Why straight walls matter', 24, INK, weight='bold'),
     text(450, 66, 'Seen from above. A flat wall can only sit one way against another flat wall.', 16, MUTE)]
for x0 in (60, 500):
    p.append(f'<rect x="{x0}" y="372" width="340" height="18" fill="{WALL}"/>')
    p.append(text(x0 + 170, 412, 'the wall of the field', 14, MUTE))
p.append(robot_box(230, 255, 200, 160, -14))
p.append(text(230, 120, '1. Put down a bit crooked', 18, INK, weight='bold'))
p.append(text(230, 444, 'One corner touches first.', 15, MUTE))
p.append(arrow([(410, 255), (480, 255)]))
p.append(text(445, 230, 'then push', 14, LEAF, 'middle', 'bold'))
p.append(text(445, 246, 'it flat', 14, LEAF, 'middle', 'bold'))
p.append(robot_box(670, 290, 200, 160, 0))
p.append(text(670, 120, '2. Pushed flat against it', 18, INK, weight='bold'))
p.append(text(670, 444, 'The whole wall touches. It is square.', 15, LEAF, weight='bold'))
p.append(text(450, 490, 'Every run starts square, and the robot can square up again during a run, with no extra code.', 15, MUTE))
save('wall-squaring.svg', 900, 520, 'Why straight walls matter: squaring against a wall',
     'Two pictures from above. 1: the robot is put down a bit crooked, and one corner touches the wall first. '
     '2: it is pushed back flat against the wall, the whole wall touches, and it sits square. So every run starts '
     'square, and the robot can square up again during a run, with no extra code.', p)

# I. Gravity mounting ----------------------------------------------------------
def chassis_side(cx, top):
    g = [f'<rect x="{cx-170}" y="{top}" width="340" height="70" rx="6" fill="{PALE}" stroke="{LEAF}" stroke-width="4"/>',
         text(cx, top + 44, 'robot', 16, LEAF, weight='bold')]
    for dx in (-110, 110):
        g.append(f'<rect x="{cx+dx-9}" y="{top-34}" width="18" height="36" rx="4" fill="{GOLD}"/>')
    return ''.join(g)
def attachment_side(cx, bottom, holes=True):
    g = [f'<rect x="{cx-150}" y="{bottom-60}" width="300" height="60" rx="6" fill="{GOLDP}" stroke="{GOLD}" stroke-width="4"/>',
         text(cx, bottom - 24, 'attachment', 16, GOLD, weight='bold')]
    if holes:
        for dx in (-110, 110):
            g.append(f'<rect x="{cx+dx-12}" y="{bottom-38}" width="24" height="38" fill="#ffffff" stroke="{GOLD}" stroke-width="2"/>')
    return ''.join(g)
p = [text(450, 40, 'Gravity mounting', 24, INK, weight='bold'),
     text(450, 66, 'Seen from the side. Pegs line it up. Its own weight holds it on. Nothing clips.', 16, MUTE)]
p.append(text(225, 108, '1. Lower it onto the pegs', 18, INK, weight='bold'))
p.append(attachment_side(225, 210))
p.append(arrow([(225, 222), (225, 270)], None, None, None, LEAF))
p.append(chassis_side(225, 330))
p.append(text(225, 438, 'The pegs fit into holes, so it', 15, MUTE))
p.append(text(225, 458, 'can only go on one way.', 15, MUTE))
p.append(text(675, 108, '2. On, and held by its weight', 18, INK, weight='bold'))
p.append(chassis_side(675, 330))
p.append(attachment_side(675, 332))
p.append(arrow([(675, 210), (675, 140)], None, None, None, LEAF))
p.append(text(700, 175, 'lift straight', 14, LEAF, 'start', 'bold'))
p.append(text(700, 193, 'up to take off', 14, LEAF, 'start', 'bold'))
p.append(text(675, 438, 'No pins to push in or forget.', 15, MUTE))
p.append(text(675, 458, 'On or off in one move.', 15, MUTE))
save('gravity-mount.svg', 900, 490, 'Gravity mounting: pegs line the attachment up and its weight holds it',
     'Two side views. 1: the attachment is lowered onto two pegs on the robot, which fit into holes so it can only '
     'go on one way. 2: it sits on the pegs, held by its own weight, with nothing clipping it. To take it off, '
     'lift it straight up. No pins to push in or forget; on or off in one move.', p)

# J. Wheel pattern across the six designs ------------------------------------
p = [text(450, 40, 'Six designs: three slip, three do not', 24, INK, weight='bold'),
     text(450, 66, 'Sort them by their wheels, and the slipping stops exactly where the wheels change.', 16, MUTE)]
groups = [
    ('Blue SPIKE wheels', RED, REDP, ['HummerOne Pro', 'Xbot', 'YellowBot v1'], 'wheels slip'),
    ('62.4 mm LEGO wheels', LEAF, PALE, ['YellowBot v2', 'Track-X', 'Boxor'], 'no slipping listed'),
]
for gi, (head, col, fill, names, verdict) in enumerate(groups):
    x0 = 60 + gi * 420
    p.append(f'<rect x="{x0}" y="100" width="360" height="300" rx="16" fill="{fill}" stroke="{col}" stroke-width="3"/>')
    p.append(text(x0 + 180, 135, head, 18, col, weight='bold'))
    for i, n in enumerate(names):
        y = 175 + i * 62
        p.append(f'<rect x="{x0+40}" y="{y}" width="280" height="46" rx="10" fill="#ffffff" stroke="{col}" stroke-width="2"/>')
        p.append(f'<circle cx="{x0+72}" cy="{y+23}" r="14" fill="{INK}"/><circle cx="{x0+72}" cy="{y+23}" r="6" fill="{col}"/>')
        p.append(text(x0 + 200, y + 29, n, 17, INK, weight='bold'))
    p.append(text(x0 + 180, 380, verdict, 18, col, weight='bold'))
p.append(text(450, 440, 'A coach who switched to 62.4 mm wheels says the robot stopped slipping on turns.', 15, MUTE))
save('wheel-pattern.svg', 900, 470, 'Six designs sorted by their wheels: three slip, three do not',
     'Left group, blue SPIKE wheels: HummerOne Pro, Xbot and YellowBot v1, which all list wheel slipping. Right group, '
     '62.4 mm LEGO wheels: YellowBot v2, Track-X and Boxor, which list no slipping. A coach who switched to 62.4 mm '
     'wheels says the robot stopped slipping on turns.', p)

# K. Mission map and our route -------------------------------------------------
# Positions are FIRST's wireframe coordinates from robot-game/field-positions.md,
# in cm from the bottom-left corner of the mat. The routes are a sketch of our
# runs, not measured paths.
MS = 4.4                      # px per cm
MX, MY = 60, 96               # top-left of the mat in the picture
def mx(x): return MX + x * MS
def my(y): return MY + (114.3 - y) * MS
ORANGE = '#dd6b20'; PURPLE = '#6b46c1'
def colour_arrow_defs():
    d = ['<defs>']
    for name, col in (('arG', LEAF), ('arO', ORANGE), ('arB', BLUE), ('arY', GOLD), ('arP', PURPLE)):
        d.append(f'<marker id="{name}" viewBox="0 0 10 10" refX="8" refY="5" markerUnits="userSpaceOnUse" '
                 f'markerWidth="16" markerHeight="16" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
    d.append('</defs>')
    return ''.join(d)
def route(pts, col, marker, width=5, dash=None):
    p_ = ' '.join(f'{mx(x):.1f},{my(y):.1f}' for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<polyline points="{p_}" fill="none" stroke="{col}" stroke-width="{width}" stroke-linecap="round" '
            f'stroke-linejoin="round"{da} marker-end="url(#{marker})"/>')
W_, H_ = 1000, 760
p = [colour_arrow_defs(),
     text(W_/2, 40, 'Our missions and our route', 24, INK, weight='bold'),
     text(W_/2, 66, 'Start on the left, finish what is close, then carry one attachment and the keystone species to the right.', 16, MUTE)]
# the mat and its 20 cm wireframe
p.append(f'<rect x="{mx(0)}" y="{my(114.3)}" width="{200*MS}" height="{114.3*MS}" rx="8" fill="#f7faf6" stroke="{LINE}" stroke-width="2"/>')
for gx_ in range(20, 200, 20):
    p.append(f'<line x1="{mx(gx_)}" y1="{my(114.3)}" x2="{mx(gx_)}" y2="{my(0)}" stroke="#e3e9e5" stroke-width="1"/>')
for gy_ in range(20, 114, 20):
    p.append(f'<line x1="{mx(0)}" y1="{my(gy_)}" x2="{mx(200)}" y2="{my(gy_)}" stroke="#e3e9e5" stroke-width="1"/>')
# the three printed black lines (bounding boxes from field-positions.md)
for cx_, cy_, w_, h_ in ((59.9, 87.7, 30.4, 9.6), (149.8, 89.1, 36.1, 11.1), (97.5, 36.2, 8.3, 12.9)):
    p.append(f'<line x1="{mx(cx_-w_/2)}" y1="{my(cy_-h_/2)}" x2="{mx(cx_+w_/2)}" y2="{my(cy_+h_/2)}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
# home areas: quarter circles of radius 48 cm in the bottom corners
r_ = 48 * MS
p.append(f'<path d="M{mx(0)},{my(48)} A{r_},{r_} 0 0 1 {mx(48)},{my(0)} L{mx(0)},{my(0)} Z" fill="{REDP}" stroke="{RED}" stroke-width="3"/>')
p.append(f'<path d="M{mx(200)},{my(48)} A{r_},{r_} 0 0 0 {mx(152)},{my(0)} L{mx(200)},{my(0)} Z" fill="{BLUEP}" stroke="{BLUE}" stroke-width="3"/>')
p.append(text(mx(15), my(22), 'LEFT', 15, RED, weight='bold'))
p.append(text(mx(15), my(16), 'HOME', 15, RED, weight='bold'))
p.append(text(mx(185), my(22), 'RIGHT', 15, BLUE, weight='bold'))
p.append(text(mx(185), my(16), 'HOME', 15, BLUE, weight='bold'))
# the three docks
for nm, x_, y_ in (('Mine dock', 189.1, 102.7), ('Farm dock', 101.2, 64.9), ('City dock', 128.6, 10.2)):
    p.append(f'<rect x="{mx(x_)-17}" y="{my(y_)-17}" width="34" height="34" rx="5" fill="#ffffff" stroke="{MUTE}" stroke-width="2" stroke-dasharray="4 3"/>')
    p.append(text(mx(x_), my(y_) + 32, nm, 12, MUTE, weight='bold'))
# routes, drawn under the mission dots
p.append(route([(30, 30), (14, 62)], LEAF, 'arG'))                          # phase0-alt: back into the rock
p.append(route([(16, 66), (58, 55)], LEAF, 'arG'))                          # then the seeds
p.append(route([(46, 13), (122, 13)], PURPLE, 'arP', 6))                   # phase2: one straight push, drone and City dock
p.append(route([(118, 5), (46, 5)], PURPLE, 'arP', 3, '8 6'))              # and straight back
p.append(route([(36, 40), (40, 98)], ORANGE, 'arO', 7))                     # phase3: up to the roots
p.append(route([(44, 96), (90, 90), (125, 83), (160, 70), (182, 46)], ORANGE, 'arO', 7, '14 8'))  # robo taxi to the right
p.append(route([(166, 24), (146, 54)], BLUE, 'arB'))                        # Phase 5: window
p.append(route([(150, 64), (152, 100)], BLUE, 'arB'))                       # leafcutters, fungus
p.append(route([(168, 100), (188, 82)], BLUE, 'arB'))                       # forest elder
p.append(route([(178, 40), (184, 92)], GOLD, 'arY', 6))                    # Phase 6: keystone to the Mine dock
# missions: (label, x, y, status). done / part / skip / not
# (label, x, y, status, colour of the run that does it)
missions = [('M01', 88.0, 9.2, 'done', PURPLE), ('M15', 128.6, 10.2, 'done', PURPLE),
            ('M02', 63.8, 55.1, 'done', LEAF), ('M03', 9.7, 68.0, 'done', LEAF),
            ('M04', 15.7, 99.0, 'skip', None), ('M05', 40.1, 106.1, 'done', ORANGE),
            ('M06', 151.3, 106.2, 'done', BLUE), ('M07', 163.7, 106.2, 'done', BLUE),
            ('M08', 54.3, 106.1, 'not', None), ('M09', 65.9, 106.1, 'not', None),
            ('M10', 78.3, 102.3, 'not', None), ('M10', 109.2, 77.3, 'not', None),
            ('M11', 140.2, 60.5, 'done', BLUE), ('M12', 192.0, 76.5, 'part', BLUE),
            ('M13', 189.1, 102.7, 'done', GOLD)]
for lab, x_, y_, st, rc in missions:
    cx_, cy_ = mx(x_), my(y_)
    if st == 'done':
        p.append(f'<circle cx="{cx_}" cy="{cy_}" r="17" fill="{rc}" stroke="#ffffff" stroke-width="3"/>')
        p.append(text(cx_, cy_ + 5, lab[1:], 13, '#ffffff', weight='bold'))
    elif st == 'part':
        p.append(f'<circle cx="{cx_}" cy="{cy_}" r="17" fill="#ffffff" stroke="{rc}" stroke-width="4" stroke-dasharray="5 3"/>')
        p.append(text(cx_, cy_ + 5, lab[1:], 13, rc, weight='bold'))
    elif st == 'skip':
        p.append(f'<circle cx="{cx_}" cy="{cy_}" r="17" fill="#ffffff" stroke="{RED}" stroke-width="3"/>')
        p.append(f'<line x1="{cx_-10}" y1="{cy_-10}" x2="{cx_+10}" y2="{cy_+10}" stroke="{RED}" stroke-width="3"/>')
        p.append(f'<line x1="{cx_+10}" y1="{cy_-10}" x2="{cx_-10}" y2="{cy_+10}" stroke="{RED}" stroke-width="3"/>')
    else:
        p.append(f'<circle cx="{cx_}" cy="{cy_}" r="15" fill="#ffffff" stroke="{LINE}" stroke-width="2.5"/>')
        p.append(text(cx_, cy_ + 5, lab[1:], 12, MUTE, weight='bold'))
# keystone species riding the taxi
p.append(f'<rect x="{mx(112)-34}" y="{my(86)-15}" width="68" height="30" rx="15" fill="{GOLDP}" stroke="{GOLD}" stroke-width="2.5"/>')
p.append(text(mx(112), my(86) + 5, 'keystone', 13, GOLD, weight='bold'))
p.append(text(mx(112), my(86) - 24, 'ROBO TAXI', 14, ORANGE, weight='bold'))
# legend
ly0 = my(0) + 38
items = [(INK, 'done', 'Done: coloured by its run'), (BLUE, 'part', 'Part of it (M12)'),
         (RED, 'skip', 'Skipped on purpose (M04)'), (LINE, 'not', 'Not in our runs')]
for i, (col, st, lab) in enumerate(items):
    lx_ = 80 + i * 225
    if st == 'skip':
        p.append(f'<circle cx="{lx_}" cy="{ly0}" r="10" fill="#ffffff" stroke="{RED}" stroke-width="2.5"/>')
    elif st == 'not':
        p.append(f'<circle cx="{lx_}" cy="{ly0}" r="10" fill="#ffffff" stroke="{LINE}" stroke-width="2.5"/>')
    elif st == 'part':
        p.append(f'<circle cx="{lx_}" cy="{ly0}" r="10" fill="#ffffff" stroke="{col}" stroke-width="3" stroke-dasharray="4 2"/>')
    else:
        for k, c_ in enumerate((LEAF, PURPLE, ORANGE)):
            p.append(f'<circle cx="{lx_-22+k*11}" cy="{ly0}" r="7" fill="{c_}" stroke="#ffffff" stroke-width="1.5"/>')
    p.append(text(lx_ + 18, ly0 + 5, lab, 14, INK, 'start'))
ly1 = ly0 + 34
for i, (col, lab) in enumerate(((LEAF, 'phase0-alt: rock, seeds'), (PURPLE, 'phase2: drone, M15'),
                                (ORANGE, 'phase3: roots, robo taxi'), (BLUE, 'Phase 5: right side'),
                                (GOLD, 'Phase 6: keystone'))):
    lx_ = 40 + i * 190
    p.append(f'<line x1="{lx_}" y1="{ly1}" x2="{lx_+30}" y2="{ly1}" stroke="{col}" stroke-width="6" stroke-linecap="round"/>')
    p.append(text(lx_ + 40, ly1 + 5, lab, 14, INK, 'start'))
p.append(text(W_/2, ly1 + 36, 'Routes are a sketch of our runs, not measured paths. Mission spots are from FIRST\'s wireframe.', 13, MUTE))
open(os.path.join(out, 'mission-route.svg'), 'w').write(svg(W_, H_,
    'Our missions and our route across the mat',
    'A map of the mat from above. The left home is bottom left and the right home is bottom right. '
    'From the left home, phase0-alt does M03 Flip the Rock and M02 Exploding Seeds. phase2 does M01 Drone Survey and '
    'M15 Biocentric Architecture on the City dock with one straight push, and comes straight back. phase3 does M05 Reaching Roots, '
    'then drives to the right side as a robo taxi, carrying one attachment and the keystone species. From the right, '
    'Phase 5 does M11, M06, M07 and part of M12, and Phase 6 takes the keystone species to the Mine dock for M13. '
    'M04 Lucky Leaves is skipped on purpose. M08, M09, M10 and M14 are not in our runs. '
    'Routes are a sketch, not measured paths.', ''.join(p)))

# L. HummerOne Pro against our robot -------------------------------------------
# Facts for HummerOne Pro come from robot-design/chassis-designs-slides.html.
# The design rules are the ones in robot-design/our-robot-explained.md.
p = [text(500, 40, 'Why we chose our robot', 24, INK, weight='bold'),
     text(500, 66, 'HummerOne Pro was the easiest design we looked at. Here is what we did differently, and why.', 16, MUTE)]
def side_robot(cx, base, flat):
    g = []
    if flat:
        g.append(f'<rect x="{cx-150}" y="{base-70}" width="300" height="62" rx="6" fill="{PALE}" stroke="{LEAF}" stroke-width="5"/>')
        g.append(text(cx, base - 32, 'flat box, wheels inside', 14, LEAF, weight='bold'))
        for dx in (-95, 95):
            g.append(f'<circle cx="{cx+dx}" cy="{base-12}" r="12" fill="{INK}"/>')
        g.append(f'<rect x="{cx-120}" y="{base-108}" width="240" height="38" rx="6" fill="{GOLDP}" stroke="{GOLD}" stroke-width="3"/>')
        g.append(text(cx, base - 83, 'attachment sits on pegs', 13, GOLD, weight='bold'))
    else:
        g.append(f'<rect x="{cx-110}" y="{base-150}" width="220" height="110" rx="6" fill="#f2f2f2" stroke="{MUTE}" stroke-width="4"/>')
        g.append(text(cx, base - 92, 'robot body', 14, MUTE, weight='bold'))
        for dx in (-70, 70):
            g.append(f'<circle cx="{cx+dx}" cy="{base-28}" r="28" fill="{BLUE}" stroke="{INK}" stroke-width="3"/>')
        g.append(f'<rect x="{cx+110}" y="{base-120}" width="60" height="50" rx="5" fill="{GOLDP}" stroke="{GOLD}" stroke-width="3"/>')
        g.append(f'<circle cx="{cx+120}" cy="{base-108}" r="5" fill="{RED}"/><circle cx="{cx+120}" cy="{base-82}" r="5" fill="{RED}"/>')
        g.append(text(cx + 140, base - 130, 'clip-on', 13, GOLD, weight='bold'))
    g.append(f'<line x1="{cx-200}" y1="{base}" x2="{cx+200}" y2="{base}" stroke="{LINE}" stroke-width="3"/>')
    return ''.join(g)
p.append(text(250, 110, 'HummerOne Pro', 20, MUTE, weight='bold'))
p.append(text(250, 132, 'one of the six designs we studied', 14, MUTE))
p.append(side_robot(240, 300, False))
p.append(text(750, 110, 'Our robot', 20, LEAF, weight='bold'))
p.append(text(750, 132, 'took the good ideas from all six designs', 14, LEAF))
p.append(side_robot(750, 300, True))
p.append(text(500, 330, 'sketches, not to scale', 12, MUTE))
rows = [('Building it', 'Easiest to build: one kit plus the expansion set', 'good',
         'More work to build, but it fixes the problems below', 'none'),
        ('Wheels', 'Blue SPIKE wheels: they slip once an attachment gets heavy', 'bad',
         'Black grippy wheels, held on both sides by the frame', 'good'),
        ('Lining up', 'Not one of the box-frame designs', 'bad',
         'Flat walls: it squares up on the wall and on the lines on the mat', 'good'),
        ('Changing attachments', 'Simple clip-on attachments', 'none',
         'Gravity: drop it on the pegs, one move. Last season swaps were slow', 'good')]
def mark(cx, cy, kind):
    if kind == 'good':
        return (f'<circle cx="{cx}" cy="{cy}" r="12" fill="{PALE}" stroke="{LEAF}" stroke-width="2"/>'
                f'<polyline points="{cx-6},{cy} {cx-1},{cy+5} {cx+7},{cy-5}" fill="none" stroke="{LEAF}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == 'bad':
        return (f'<circle cx="{cx}" cy="{cy}" r="12" fill="{REDP}" stroke="{RED}" stroke-width="2"/>'
                f'<line x1="{cx-5}" y1="{cy-5}" x2="{cx+5}" y2="{cy+5}" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>'
                f'<line x1="{cx+5}" y1="{cy-5}" x2="{cx-5}" y2="{cy+5}" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>')
    return f'<circle cx="{cx}" cy="{cy}" r="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>'
y = 350
for head, theirs, tk, ours, ok in rows:
    p.append(f'<rect x="40" y="{y}" width="920" height="84" rx="10" fill="#ffffff" stroke="#e3e9e5" stroke-width="2"/>')
    p.append(text(60, y + 30, head, 16, INK, 'start', 'bold'))
    p.append(f'<line x1="{60}" y1="{y+46}" x2="{240}" y2="{y+46}" stroke="#e3e9e5"/>')
    p.append(mark(92, y + 64, tk))
    p.append(text(112, y + 69, theirs, 14, MUTE, 'start'))
    p.append(mark(532, y + 64, ok))
    p.append(text(552, y + 69, ours, 14, INK, 'start'))
    y += 96
open(os.path.join(out, 'robot-compare.svg'), 'w').write(svg(1000, y + 20,
    'Why we chose our robot: HummerOne Pro against our robot',
    'Sketched side views of HummerOne Pro and our robot, not to scale, and four rows comparing them. Building it: '
    'HummerOne Pro is the easiest to build, from one kit plus the expansion set; ours is more work but fixes the '
    'problems below. Wheels: HummerOne Pro uses blue SPIKE wheels that slip once an attachment gets heavy; ours uses '
    'black grippy wheels held on both sides by the frame. Lining up: HummerOne Pro is not one of the box-frame designs; '
    'ours has flat walls that square up on the wall and on the lines on the mat. Changing attachments: HummerOne Pro '
    'uses simple clip-on attachments; ours drops them onto pegs in one move, because last season swaps were slow.',
    ARROW_DEFS + ''.join(p)))


# M. The gyro correction loop, simple version ---------------------------------
# For the workshop deck. The full drive_cm flowchart is drive-flowchart.svg.
p = [text(350, 40, 'How the gyro keeps us straight', 24, INK, weight='bold'),
     text(350, 66, 'This loop runs about 66 times every second.', 16, MUTE)]
p.append(node('start', 350, 110, 260, 46, ['drive_cm(30)'], 18))
p.append(arrow([(350, 133), (350, 163)]))
p.append(node('step', 350, 195, 420, 60, ['1. Read the gyro', 'How far off straight are we?'], 17))
p.append(arrow([(350, 225), (350, 255)]))
p.append(node('step', 350, 287, 420, 60, ['2. Steer back', 'The further off, the harder it steers'], 17))
p.append(arrow([(350, 317), (350, 347)]))
p.append(node('ask', 350, 400, 300, 100, ['Gone', 'far enough?'], 17))
p.append(arrow([(500, 400), (548, 400)], 'yes', 524, 388))
p.append(node('end', 640, 400, 180, 50, ['Brake. Done.'], 17))
p.append(arrow([(350, 450), (350, 485)], 'no', 372, 472))
p.append(node('step', 350, 515, 260, 50, ['3. Wait 15 ms'], 17))
p.append(arrow([(220, 515), (90, 515), (90, 195), (140, 195)], 'repeat', 60, 360))
save('gyro-loop.svg', 750, 570, 'How the gyro keeps us straight: the correction loop',
     'A simple loop. drive_cm(30) starts. 1: read the gyro to see how far off straight we are. 2: steer back, '
     'harder the further off we are. Then ask: gone far enough? If yes, brake and stop. If no, 3: wait 15 '
     'milliseconds and repeat from step 1. The loop runs about 66 times every second.', p)

print('ok2')
