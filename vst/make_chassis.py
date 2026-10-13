#!/usr/bin/env python3
"""layout.conf -> images/chassis_<tab>.svg: the skin's hardware box (see skin.css for the controls' half of the look).

One light source, top left. Dark cheeks with screws at both ends, a grained faceplate raised between them, a recessed
well under every `frame`, an overall light falloff on top. Frame positions come from layout.conf, so re-run this after
moving a frame:  python3 vst/make_chassis.py   (plain Python, no dependencies; the build never runs it).
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "images")

W, H = 1280, 800
CHEEK = 24            # width of each side cheek
PLATE_TOP = 60        # above the visible area (the skin shows layout y 86..714), so no top edge

DEFS = """<defs>
<linearGradient id="cd-plate" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#d6d1bf"/><stop offset="0.45" stop-color="#c9c4b2"/><stop offset="1" stop-color="#b8b3a0"/>
</linearGradient>
<linearGradient id="cd-well" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#aca793"/><stop offset="0.5" stop-color="#b9b4a1"/><stop offset="1" stop-color="#c4bfad"/>
</linearGradient>
<linearGradient id="cd-cheek-l" x1="0" y1="0" x2="1" y2="0">
 <stop offset="0" stop-color="#16120d"/><stop offset="0.35" stop-color="#3a3126"/><stop offset="0.8" stop-color="#2a2319"/><stop offset="1" stop-color="#0f0c08"/>
</linearGradient>
<linearGradient id="cd-cheek-r" x1="0" y1="0" x2="1" y2="0">
 <stop offset="0" stop-color="#0f0c08"/><stop offset="0.2" stop-color="#2a2319"/><stop offset="0.65" stop-color="#3a3126"/><stop offset="1" stop-color="#16120d"/>
</linearGradient>
<radialGradient id="cd-light" cx="0.22" cy="0.0" r="0.95" gradientUnits="objectBoundingBox">
 <stop offset="0" stop-color="#fff" stop-opacity="0.22"/><stop offset="0.55" stop-color="#fff" stop-opacity="0"/>
</radialGradient>
<radialGradient id="cd-vignette" cx="0.5" cy="0.5" r="0.78">
 <stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#1a1408" stop-opacity="0.32"/>
</radialGradient>
<radialGradient id="cd-screw" cx="0.38" cy="0.32" r="0.8">
 <stop offset="0" stop-color="#f2f2ee"/><stop offset="0.55" stop-color="#a5a5a1"/><stop offset="1" stop-color="#55554f"/>
</radialGradient>
<filter id="cd-inset" x="-4%" y="-4%" width="108%" height="108%">
 <feComponentTransfer in="SourceAlpha"><feFuncA type="table" tableValues="1 0"/></feComponentTransfer>
 <feGaussianBlur stdDeviation="3.6"/>
 <feOffset dx="2" dy="4.5" result="off"/>
 <feFlood flood-color="#241c0e" flood-opacity="0.9"/>
 <feComposite in2="off" operator="in"/>
 <feComposite in2="SourceAlpha" operator="in" result="shade"/>
 <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="shade"/></feMerge>
</filter>
<filter id="cd-wood" x="0" y="0" width="100%" height="100%">
 <feTurbulence type="fractalNoise" baseFrequency="0.5 0.014" numOctaves="3" seed="11"/>
 <feColorMatrix type="matrix" values="0 0 0 0 0.05  0 0 0 0 0.03  0 0 0 0 0.01  0 0 1.4 0 -0.45"/>
</filter>
<filter id="cd-blur6" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="cd-blur2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="1.6"/></filter>
</defs>"""


def screw(cx, cy, ang):
    r = 6
    return (
        '<circle cx="%g" cy="%g" r="%g" fill="#000" opacity="0.55" filter="url(#cd-blur2)" transform="translate(1.2 2)"/>'
        '<circle cx="%g" cy="%g" r="%g" fill="url(#cd-screw)" stroke="#2c2c28" stroke-width="0.8"/>'
        '<g transform="rotate(%d %g %g)"><rect x="%g" y="%g" width="%g" height="1.8" fill="#26261f"/>'
        '<rect x="%g" y="%g" width="1.8" height="%g" fill="#26261f"/></g>'
        '<path d="M%g %g A%g %g 0 0 1 %g %g" fill="none" stroke="#fff" stroke-opacity="0.55" stroke-width="0.9"/>'
        % (cx, cy, r, cx, cy, r, ang, cx, cy, cx - r + 1.6, cy - 0.9, 2 * r - 3.2, cx - 0.9, cy - r + 1.6, 2 * r - 3.2,
           cx - r * 0.7, cy - r * 0.2, r * 0.74, r * 0.74, cx + r * 0.2, cy - r * 0.7))


def well(x, y, w, h):
    """A recessed panel: a light lip below and to the right, a gradient floor, the inner shadow filter, a dark rim."""
    return (
        '<rect x="%g" y="%g" width="%g" height="%g" rx="11" fill="#fff" opacity="0.6"/>' % (x + 0.5, y + 1.8, w - 1, h - 1) +
        '<rect x="%g" y="%g" width="%g" height="%g" rx="10" fill="url(#cd-well)" filter="url(#cd-inset)"/>' % (x + 1, y + 1, w - 2, h - 2) +
        '<rect x="%g" y="%g" width="%g" height="%g" rx="10" fill="none" stroke="#3d3624" stroke-opacity="0.55" stroke-width="1.2"/>'
        % (x + 1, y + 1, w - 2, h - 2) +
        '<path d="M%g %g H%g" stroke="#fff" stroke-opacity="0.25" stroke-width="1"/>' % (x + 14, y + 2.6, x + w - 14))


def logo(x_right, y_top):
    """images/logo.svg (make_logo.py), inlined with its right edge at x_right; vertically centred in the title row."""
    src = open(os.path.join(OUT, "logo.svg"), encoding="utf-8").read()
    w, h = (int(v) for v in re.search(r'width="(\d+)" height="(\d+)"', src).groups())
    inner = src[src.index(">") + 1:src.rindex("</svg>")]
    # printed on the plate: a faint light edge below, like every other piece of lettering
    return ('<svg x="%d" y="%d" width="%d" height="%d" viewBox="0 0 %d %d" overflow="visible" '
            'style="filter:drop-shadow(0 1px 0 rgba(255,255,255,.5))">%s</svg>' % (x_right - w, y_top, w, h, w, h, inner))


def chassis(frames, brand):
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">' % (W, H, W, H), DEFS]
    o.append('<rect width="%d" height="%d" fill="#17130e"/>' % (W, H))
    # cheeks: dark stained wood, a lit edge toward the plate
    for x0, grad in ((0, "cd-cheek-l"), (W - CHEEK, "cd-cheek-r")):
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="url(#%s)"/>' % (x0, CHEEK + 2, H, grad))
        o.append('<rect x="%d" y="0" width="%d" height="%d" filter="url(#cd-wood)" opacity="0.8"/>' % (x0, CHEEK + 2, H))
    # the plate's shadow falls on the cheeks, then the plate itself with a lit top-left bevel and a dark lower-right one
    px0, px1 = CHEEK, W - CHEEK
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#000" opacity="0.7" filter="url(#cd-blur6)" transform="translate(2 4)"/>'
             % (px0, PLATE_TOP, px1 - px0, H))
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="url(#cd-plate)"/>' % (px0, PLATE_TOP, px1 - px0, H))
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#a39e8a" filter="url(#grain)" opacity="0.55"/>'
             % (px0, PLATE_TOP, px1 - px0, H))
    o.append('<rect x="%d" y="%d" width="2" height="%d" fill="#fff" opacity="0.7"/>' % (px0, PLATE_TOP, H))
    o.append('<rect x="%d" y="%d" width="1.5" height="%d" fill="#2a2418" opacity="0.7"/>' % (px1 - 1.5, PLATE_TOP, H))
    o.append('<rect x="%d" y="%d" width="1" height="%d" fill="#000" opacity="0.55"/>' % (px0 - 1, PLATE_TOP, H))
    o.append('<rect x="%d" y="%d" width="1" height="%d" fill="#000" opacity="0.55"/>' % (px1, PLATE_TOP, H))
    for f in frames:
        o.append(well(*f))
    if brand:
        x, y = brand
        o.append(logo(x, y))
    # screws in the cheeks, slots at odd angles as no two are ever turned alike
    for i, (cy, ang) in enumerate(((112, 25), (400, 70), (688, 160))):
        o.append(screw(CHEEK // 2, cy, ang) + screw(W - CHEEK // 2, cy, ang + 40 + 11 * i))
    # lighting over everything: a soft key light from the top left, the edges falling off
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="url(#cd-light)"/>' % (px0, PLATE_TOP, px1 - px0, H - PLATE_TOP))
    o.append('<rect width="%d" height="%d" fill="url(#cd-vignette)"/>' % (W, H))
    o.append("</svg>")
    return "\n".join(o)


def tabs(layout):
    cur = None
    for line in open(layout, encoding="utf-8"):
        m = re.match(r"\[tab (.+?)\]", line)
        if m:
            cur = m.group(1)
            yield cur, None
        elif cur and line.startswith("frame "):
            d = dict(re.findall(r"\b([xywh])=(\d+)", line))
            yield cur, tuple(int(d[k]) for k in "xywh")


def main():
    frames = {}
    for tab, f in tabs(os.path.join(ROOT, "layout.conf")):
        frames.setdefault(tab, [])
        if f:
            frames[tab].append(f)
    os.makedirs(OUT, exist_ok=True)
    for tab, fs in frames.items():
        name = "chassis_%s.svg" % tab.lower()
        first = min(fs, key=lambda f: (f[1], f[0]))
        brand = (first[0] + first[2] - 20, first[1] + 7) if fs else None
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(chassis(fs, brand) + "\n")
        print("wrote images/%s (%d frames)" % (name, len(fs)))


if __name__ == "__main__":
    main()
