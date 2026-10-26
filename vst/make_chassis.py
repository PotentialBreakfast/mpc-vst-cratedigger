#!/usr/bin/env python3
"""layout.conf -> images/chassis_<tab>.svg: the skin's dark case (skin.css styles the controls on top of it).

Near-black base, a brushed charcoal panel under every `frame` with a lighter title strip and a small amber tick, and
the CRATE DIGGER mark in the first frame of each tab. Frame positions come from layout.conf, so re-run this after
moving a frame:  python3 vst/make_chassis.py   (plain Python, no dependencies; the build never runs it).
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "images")

W, H = 1280, 800
STRIP = 38            # height of a panel's title strip (the renderer draws the title rule at the same height)
AMBER = "#f2b34a"

DEFS = """<defs>
<linearGradient id="cd-base" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#191c21"/><stop offset="1" stop-color="#101216"/>
</linearGradient>
<linearGradient id="cd-panel" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#262a30"/><stop offset="1" stop-color="#1e2126"/>
</linearGradient>
<linearGradient id="cd-strip" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#363b43"/><stop offset="1" stop-color="#2b3037"/>
</linearGradient>
<filter id="cd-brush" x="0" y="0" width="100%" height="100%">
 <feTurbulence type="fractalNoise" baseFrequency="0.9 0.012" numOctaves="2" seed="4"/>
 <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.9 -0.35"/>
</filter>
<filter id="cd-blur8" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="8"/></filter>
</defs>"""


def logo(x_right, y_top):
    """images/logo.svg (make_logo.py), inlined with its right edge at x_right; vertically centred in the title strip."""
    src = open(os.path.join(OUT, "logo.svg"), encoding="utf-8").read()
    w, h = (int(v) for v in re.search(r'width="(\d+)" height="(\d+)"', src).groups())
    inner = src[src.index(">") + 1:src.rindex("</svg>")]
    return ('<svg x="%d" y="%d" width="%d" height="%d" viewBox="0 0 %d %d" overflow="visible">%s</svg>'
            % (x_right - w, y_top, w, h, w, h, inner))


def panel(x, y, w, h):
    """A charcoal panel: soft drop shadow, brushed face, a lighter title strip with an amber tick, a thin rim."""
    r = 10
    strip = ('M%g %g V%g A%g %g 0 0 1 %g %g H%g A%g %g 0 0 1 %g %g V%g Z'
             % (x + 1, y + STRIP, y + r, r, r, x + 1 + r, y + 1, x + w - 1 - r, r, r, x + w - 1, y + r, y + STRIP))
    return (
        '<rect x="%g" y="%g" width="%g" height="%g" rx="%d" fill="#000" opacity="0.55" filter="url(#cd-blur8)" transform="translate(0 4)"/>' % (x, y, w, h, r) +
        '<rect x="%g" y="%g" width="%g" height="%g" rx="%d" fill="url(#cd-panel)"/>' % (x, y, w, h, r) +
        '<rect x="%g" y="%g" width="%g" height="%g" rx="%d" fill="#fff" filter="url(#cd-brush)" opacity="0.03"/>' % (x, y, w, h, r) +
        '<path d="%s" fill="url(#cd-strip)"/>' % strip +
        '<path d="M%g %g H%g" stroke="#000" stroke-opacity="0.45" stroke-width="1"/>' % (x + 1, y + STRIP + 0.5, x + w - 1) +
        '<rect x="%g" y="%g" width="3" height="16" rx="1.5" fill="%s"/>' % (x + 8, y + STRIP / 2 - 8, AMBER) +
        '<rect x="%g" y="%g" width="%g" height="%g" rx="%d" fill="none" stroke="#3a4049" stroke-width="1.2"/>' % (x + 0.6, y + 0.6, w - 1.2, h - 1.2, r))


def chassis(frames, brand):
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">' % (W, H, W, H), DEFS]
    o.append('<rect width="%d" height="%d" fill="url(#cd-base)"/>' % (W, H))
    o.append('<rect width="%d" height="%d" fill="#fff" filter="url(#cd-brush)" opacity="0.015"/>' % (W, H))
    for f in frames:
        o.append(panel(*f))
    if brand:
        o.append(logo(*brand))
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
