#!/usr/bin/env python3
"""Draws images/sync_off.png (dark) and images/sync_on.png (amber) for the TRANSPORT SYNC button.

The label is baked in: light on the dark off state, dark on the amber on state.
Needs Pillow and Titillium Web SemiBold (OFL): FONT=<path to TitilliumWeb-SemiBold.ttf>, e.g. from
mpc-vst's tools/html_art/fonts/.  Run:  FONT=... python3 vst/make_sync_images.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.environ["FONT"]
S, W, H = 4, 176, 48


def lerp(c0, c1, t):
    return tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))


def make(name, lit=False):
    """A dark keycap with a light rim (off) or the amber keycap (on), drawn at 4x and scaled down."""
    top, bot = ((247, 194, 98), (224, 149, 47)) if lit else ((38, 42, 48), (24, 27, 32))
    rim = (255, 212, 138, 255) if lit else (74, 82, 93, 255)
    ink = (26, 19, 5, 255) if lit else (230, 233, 238, 255)
    im = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    face = Image.new("RGBA", (W * S, (H - 3) * S), (0, 0, 0, 0))
    fd = ImageDraw.Draw(face)
    for y in range((H - 3) * S):
        t = y / ((H - 3) * S - 1)
        fd.line((0, y, W * S, y), fill=lerp(top, bot, t) + (255,))
    mask = Image.new("L", face.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((S, S, W * S - 1 - S, (H - 3) * S - 1), 7 * S, fill=255)
    shadow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((S, 2 * S, W * S - 1 - S, H * S - 1 - S), 7 * S, fill=(0, 0, 0, 150))
    im.alpha_composite(shadow)
    im.paste(face, (0, 0), mask)
    d = ImageDraw.Draw(im, "RGBA")
    d.rounded_rectangle((S, S, W * S - 1 - S, (H - 3) * S - 1), 7 * S, outline=rim, width=int(1.3 * S))
    gloss = Image.new("RGBA", im.size, (0, 0, 0, 0))   # drawn on its own layer: RGBA drawing replaces pixels, it doesn't blend
    ImageDraw.Draw(gloss).rounded_rectangle((4 * S, 2 * S, W * S - 1 - 4 * S, ((H - 3) // 2) * S), 4 * S, fill=(255, 255, 255, 22))
    im.alpha_composite(gloss)
    d = ImageDraw.Draw(im, "RGBA")
    f = ImageFont.truetype(FONT, 17 * S)
    txt = "TRANSPORT SYNC"
    tw = d.textlength(txt, font=f) + len(txt) * S * 1.2
    x = (W * S - tw) / 2
    y = (H - 3) * S / 2
    for ch in txt:
        d.text((x, y), ch, font=f, fill=ink, anchor="lm")
        x += d.textlength(ch, font=f) + S * 1.2
    im.resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "images", name))


make("sync_off.png")
make("sync_on.png", lit=True)
