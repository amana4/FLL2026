"""Draws the three diagrams on robot-design/our-robot-explained.md.

Run: python3 tools/make-robot-diagrams.py robot-design/diagrams

Writes robot-wiring.svg, face-square.svg and iterate-loop.svg. Edit the text
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
b.append(f'<rect x="250" y="110" width="300" height="300" rx="18" fill="{PALE}" stroke="{LEAF}" stroke-width="3"/>')
# hub
b.append(f'<rect x="320" y="170" width="160" height="150" rx="14" fill="#ffffff" stroke="{INK}" stroke-width="3"/>')
b.append(text(400,235,'Hub',22,INK,weight='bold'))
b.append(text(400,260,'gyro inside',15,MUTE))
b.append(text(400,282,'face up, button on top',15,MUTE))
# wheels
for x,lab,sock in ((215,'Left wheel','F'),(585,'Right wheel','A')):
    b.append(f'<rect x="{x-25}" y="200" width="50" height="110" rx="12" fill="{INK}"/>')
    b.append(f'<circle cx="{x}" cy="255" r="20" fill="{LEAF}" stroke="#ffffff" stroke-width="3"/>')
    b.append(text(x,262,sock,20,'#ffffff',weight='bold'))
    tx = 110 if x<400 else 690
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
b.append(text(400,585,'Socket letters F, A, C and E come from our final code.',15,MUTE))
open(os.path.join(out,'robot-wiring.svg'),'w').write(svg(800,610,'Our robot from above: what is plugged in where',
 'Schematic top view. The left wheel motor is on socket F and the right wheel motor on socket A. The hub sits in the middle, face up. The attachment is on the back, with motors on sockets C and E. The robot drives backwards into the models.',''.join(b)))

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
