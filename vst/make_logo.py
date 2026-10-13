#!/usr/bin/env python3
"""Draws images/logo.svg: the CRATE DIGGER silk-screen (make_chassis.py puts it in each frame's title row).

A record and the name, one ink, as printed lettering on the plate. The record stands a little taller than the capitals. The letters
are outlined into paths, so the finished SVG needs no font.
Needs fontTools and Bebas Neue Bold (SIL OFL):  FONT=<path to BebasNeue-Bold .ttf> python3 vst/make_logo.py
"""
import os

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#6b6558"      # the skin's ink_dim: quieter than the frame titles
CAP = 17.0           # capital height in px
REC = 25.0           # the record's diameter: taller than the capitals, centred on them
TRACK = 3.2          # extra space between letters, px
WORD_GAP = 7         # extra space at the word break, px
GAP = 8              # between the record and the name
PAD = 1              # room for the record's outer stroke
H = int(REC) + 2 * PAD


def record(cx, cy, r):
    """A record in one ink: a rim, two grooves, a solid label with the spindle hole punched out."""
    ring = lambda rr, w: '<circle cx="%g" cy="%g" r="%g" fill="none" stroke="%s" stroke-width="%g"/>' % (cx, cy, rr, INK, w)
    hole = "M%g %g a%g %g 0 1 0 %g 0 a%g %g 0 1 0 %g 0Z" % (cx - 0.8, cy, 0.8, 0.8, 1.6, 0.8, 0.8, -1.6)
    label = "M%g %g a%g %g 0 1 0 %g 0 a%g %g 0 1 0 %g 0Z" % (cx - r * 0.34, cy, r * 0.34, r * 0.34, r * 0.68, r * 0.34, r * 0.34, -r * 0.68)
    return (ring(r - 0.6, 1.2) + ring(r * 0.78, 0.55) + ring(r * 0.62, 0.55) +
            '<path d="%s%s" fill="%s" fill-rule="evenodd"/>' % (label, hole, INK))


def main():
    font = TTFont(os.environ["FONT"])
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    bp = BoundsPen(gs)
    gs[cmap[ord("H")]].draw(bp)
    scale = CAP / (bp.bounds[3] - bp.bounds[1])          # em -> px so that capitals are CAP tall
    cy = H / 2
    base = cy + CAP / 2
    r = REC / 2
    ox = 2 * r + PAD * 2 + GAP
    pen = SVGPathPen(gs)
    x = ox
    for ch in "CRATE DIGGER":
        if ch == " ":
            x += WORD_GAP
            continue
        name = cmap[ord(ch)]
        gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, base)))
        x += gs[name].width * scale + TRACK
    w = int(round(x - TRACK))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s'
           '<path d="%s" fill="%s"/></svg>\n' % (w, H, w, H, record(PAD + r, cy, r), pen.getCommands(), INK))
    with open(os.path.join(HERE, "images", "logo.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote images/logo.svg (%d x %d)" % (w, H))


if __name__ == "__main__":
    main()
