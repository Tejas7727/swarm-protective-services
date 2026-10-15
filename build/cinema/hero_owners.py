# -*- coding: utf-8 -*-
"""Build the first screen from the owners' own photograph.

No generated people, no fabricated gear: the two owners as they were shot, on a
dark field with room for the name, the motto and the two buttons. The camera
flies into this plate, so the right half carries the photograph and the left
half is the quiet side the type sits on.

    python build/cinema/hero_owners.py --src source-art/owners/2.jpg \
        --out source-art/scene-v6/crew.png
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

W, H = 2400, 1600
PANEL_W = 1240                     # the photograph, at its own 3:4
PANEL_X = 1030                     # left edge of the photograph inside the plate
FIELD_LO = (10, 11, 13)
FIELD_HI = (26, 29, 33)
GOLD = (184, 145, 78)


def f32(img):
    return np.asarray(img, dtype=np.float32) / 255.0


def u8(a):
    return Image.fromarray(np.clip(a * 255.0 + 0.5, 0, 255).astype(np.uint8))


def field(w, h):
    """The quiet side: a dark room with one soft pool of light behind the type."""
    y = np.linspace(0, 1, h)[:, None]
    x = np.linspace(0, 1, w)[None, :]
    glow = np.exp(-(((x - 0.22) / 0.55) ** 2 + ((y - 0.42) / 0.7) ** 2) * 1.5)
    k = np.clip(0.18 + 0.82 * glow, 0, 1)[:, :, None]
    lo = np.array(FIELD_LO, dtype=np.float32) / 255.0
    hi = np.array(FIELD_HI, dtype=np.float32) / 255.0
    return lo + (hi - lo) * k


def grade(img):
    """Night-black, metal-cool: deepen the blacks, hold the car and the skin."""
    a = f32(img)
    a = np.clip((a - 0.5) * 1.12 + 0.5, 0, 1)          # contrast
    a = a ** 1.06                                       # pull the floor down
    lum = a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    a = np.clip(lum[:, :, None] + (a - lum[:, :, None]) * 0.72, 0, 1)   # desaturate a touch
    a *= np.array([1.0, 0.995, 0.985], dtype=np.float32)                # warm it a hair
    return u8(a)


def build(src, out):
    photo = Image.open(src).convert("RGB")
    ph = int(round(PANEL_W * photo.height / photo.width))
    photo = photo.resize((PANEL_W, ph), Image.LANCZOS)
    if ph > H:                                           # keep the heads, trim the ground
        photo = photo.crop((0, int((ph - H) * 0.30), PANEL_W, int((ph - H) * 0.30) + H))
    photo = grade(photo)

    plate = u8(field(W, H)).convert("RGB")

    # a soft shadow so the photograph sits in front of the field
    sh = Image.new("L", (W, H), 0)
    sh.paste(255, (PANEL_X - 40, 0, PANEL_X + PANEL_W + 40, H))
    sh = sh.filter(ImageFilter.GaussianBlur(70))
    plate = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), plate, sh.point(lambda v: int(v * 0.55)))

    plate.paste(photo, (PANEL_X, 0))

    # one gold hairline where the field meets the photograph
    rule = Image.new("RGB", (3, H), GOLD)
    plate.paste(Image.blend(plate.crop((PANEL_X - 1, 0, PANEL_X + 2, H)), rule, 0.75), (PANEL_X - 1, 0))

    # the photograph's own edges fall off into the plate, so no hard seam at the frame
    a = f32(plate)
    x = np.linspace(0, 1, W)[None, :, None]
    vig = np.clip((x - 0.955) / 0.045, 0, 1) * 0.55 + np.clip((0.02 - x) / 0.02, 0, 1) * 0.3
    y = np.linspace(0, 1, H)[:, None, None]
    vig = vig + np.clip((y - 0.93) / 0.07, 0, 1) * 0.35 + np.clip((0.04 - y) / 0.04, 0, 1) * 0.25
    a = a * (1 - np.clip(vig, 0, 0.8))
    u8(a).save(out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    print(build(a.src, a.out))
