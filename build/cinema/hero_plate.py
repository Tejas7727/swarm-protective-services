# -*- coding: utf-8 -*-
"""Build the first screen's photograph: the crew, and the mark behind them.

The client asked for the five of them to come forward and for the Swarm emblem
to stand on the wall behind, with some depth to it. So this takes the client's
own group photograph and rebuilds everything that is not a person:

  * the venue is gone — a plain dark wall with one pool of light, which also
    settles the question of the venue's sign being legible,
  * the emblem is extruded on that wall, lit from the upper left, with its own
    cast shadow, and kept dim so it reads as an object in the room,
  * the crew are lifted — a little more contrast, a warm rim on the shoulders,
    and a contact shadow so they sit in the room rather than float on it.

Inputs (not in the repo; see SOURCES.md):
  crew.png            the client photograph, already widened to 3:2
  mask_isnet.png      people matte   (rembg, isnet-general-use)
  mask_human.png      people matte   (rembg, u2net_human_seg) - fills what isnet drops
  emblem.png          docs/assets/logo/swarm-emblem-gold.svg rasterised 1800px wide

    python build/cinema/hero_plate.py --src <folder> --out source-art/scene-v5/crew.png

The camera pushes through the front officer's chest into the next screen, so the
middle of the frame has to stay dark: nothing bright goes behind him.
"""
import argparse
import math
import os

import numpy as np
from PIL import Image, ImageFilter

GOLD_TOP = (218, 180, 96)
GOLD_BOT = (132, 100, 36)
GOLD_LIT = (247, 226, 170)
WALL_LO = (8, 9, 11)
WALL_HI = (26, 27, 31)


def f32(img):
    return np.asarray(img, dtype=np.float32) / 255.0


def u8(arr):
    return Image.fromarray(np.clip(arr * 255.0 + 0.5, 0, 255).astype(np.uint8))


def blur(a, r):
    """Gaussian blur on a float plane or stack."""
    if a.ndim == 2:
        return f32(u8(a).filter(ImageFilter.GaussianBlur(r)))
    return np.dstack([blur(a[:, :, i], r) for i in range(a.shape[2])])


def shift(a, dx, dy):
    out = np.zeros_like(a)
    h, w = a.shape[:2]
    x0, x1 = max(0, dx), min(w, w + dx)
    y0, y1 = max(0, dy), min(h, h + dy)
    out[y0:y1, x0:x1] = a[y0 - dy:y1 - dy, x0 - dx:x1 - dx]
    return out


def matte(src, size):
    """One clean people matte from the two models.

    Neither model is right on its own: the general model takes the lit wall
    columns behind them for part of the subject, and the human model takes the
    lit floor they stand on. They disagree in different places, so the overlap
    is the people.
    """
    a = f32(Image.open(os.path.join(src, "mask_isnet.png")).convert("L").resize(size))
    b = f32(Image.open(os.path.join(src, "mask_human.png")).convert("L").resize(size))
    m = np.minimum(a, b)
    m = f32(u8(m).filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(5)))   # close pinholes
    m = np.clip(blur(m, 2.0) * 1.06, 0, 1)
    # one sliver of lit wall survives between the first two of them; cut it out
    w, h = size
    box = np.ones((h, w), dtype=np.float32)
    box[int(0.49 * h):int(0.73 * h), int(0.366 * w):int(0.417 * w)] = 0.0
    m *= blur(box, 14.0)
    # let them stand out of the dark rather than end on a cut: the matte fades
    # away below the knee, where black trousers and a black floor are the same
    return m * np.clip((0.86 - np.linspace(0, 1, h)) / 0.14, 0, 1)[:, None]


def wall(w, h):
    """A dark room: one soft pool of light behind the group, a darker floor."""
    y = np.linspace(0, 1, h)[:, None]
    x = np.linspace(0, 1, w)[None, :]
    v = 1.0 - np.abs(y - 0.42) / 0.75
    g = np.exp(-(((x - 0.5) / 0.52) ** 2 + ((y - 0.40) / 0.46) ** 2) * 1.6)
    k = np.clip(v * 0.45 + g * 0.85, 0, 1)
    floor = np.clip((y - 0.78) / 0.05, 0, 1)                     # where the wall meets the floor
    pool = np.exp(-(((x - 0.5) / 0.42) ** 2 + ((y - 0.95) / 0.22) ** 2) * 2.2)
    k = k * (1 - 0.55 * floor) + pool * floor * 0.5
    lo = np.array(WALL_LO, dtype=np.float32) / 255.0
    hi = np.array(WALL_HI, dtype=np.float32) / 255.0
    return lo + (hi - lo) * np.clip(k, 0, 1)[:, :, None]


def emblem_3d(src, w, h, cx, cy, width):
    """The emblem as an object on the wall: cast shadow, extrusion, lit face."""
    em = Image.open(os.path.join(src, "emblem.png")).convert("RGBA")
    ew = int(width)
    eh = int(round(ew * em.height / em.width))
    em = em.resize((ew, eh), Image.LANCZOS)
    a = np.zeros((h, w), dtype=np.float32)
    x0, y0 = int(cx - ew / 2), int(cy - eh / 2)
    sx0, sy0 = max(0, x0), max(0, y0)
    sx1, sy1 = min(w, x0 + ew), min(h, y0 + eh)
    a[sy0:sy1, sx0:sx1] = f32(em.getchannel("A"))[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0]

    rgb = np.zeros((h, w, 3), dtype=np.float32)
    alpha = np.zeros((h, w), dtype=np.float32)

    # cast shadow on the wall, down and to the right of the light
    sh = blur(shift(a, 26, 32), 26.0) * 0.75
    shadow = sh

    # extruded side faces
    steps = 30
    for i in range(steps, 0, -1):
        t = i / float(steps)
        s = shift(a, int(round(i * 0.85)), int(round(i * 1.15)))
        c = np.array(GOLD_BOT, dtype=np.float32) / 255.0 * (0.30 + 0.34 * (1 - t))
        m = s[:, :, None]
        rgb = rgb * (1 - m) + c[None, None, :] * m
        alpha = np.maximum(alpha, s)

    # front face: gold down the height, brighter where the light falls
    yy = np.linspace(0, 1, h)[:, None]
    top = np.array(GOLD_TOP, dtype=np.float32) / 255.0
    bot = np.array(GOLD_BOT, dtype=np.float32) / 255.0
    face = top[None, None, :] + (bot - top)[None, None, :] * yy[:, :, None]
    lit = np.exp(-(((np.linspace(0, 1, w)[None, :] - 0.42) / 0.5) ** 2) * 1.4)
    face = face * (0.74 + 0.5 * lit[:, :, None])

    # bevel: light from the upper left, read off the slope of the blurred alpha
    sm = blur(a, 7.0)
    gy, gx = np.gradient(sm)
    n = np.clip(-(gx * 0.7 + gy * 0.7) * 9.0, 0, 1) * a
    face = face + (np.array(GOLD_LIT, dtype=np.float32) / 255.0)[None, None, :] * n[:, :, None] * 0.85

    m = a[:, :, None]
    rgb = rgb * (1 - m) + face * m
    alpha = np.maximum(alpha, a)
    return rgb, alpha, shadow


def build(src, out, width_frac=0.60, cx_frac=0.5, cy_frac=0.43, strength=0.52):
    photo = Image.open(os.path.join(src, "crew.png")).convert("RGB")
    w, h = photo.size
    P = f32(photo)
    m = matte(src, (w, h))

    bg = wall(w, h)
    rgb, ea, esh = emblem_3d(src, w, h, w * cx_frac, h * cy_frac, w * width_frac)
    bg = bg * (1 - esh[:, :, None] * 0.8)                       # the emblem's own shadow
    k = (ea * strength)[:, :, None]
    bg = bg * (1 - k) + rgb * k

    # contact shadow under the group
    cs = blur(shift(m, 0, 26), 30.0) * 0.55
    bg = bg * (1 - cs[:, :, None])

    # the crew come forward: more contrast, a key from above, a warm rim
    key = 1.0 + 0.16 * np.clip(1.0 - np.linspace(0, 1, h) * 1.8, 0, 1)[:, None, None]
    people = np.clip(((P - 0.5) * 1.2 + 0.5 + 0.06) * key, 0, 1)
    sharp = f32(u8(people).filter(ImageFilter.UnsharpMask(radius=3, percent=45, threshold=3)))
    rim = np.clip(m - blur(shift(m, 6, 7), 7.0), 0, 1) * m
    rim *= np.clip(1.15 - np.linspace(0, 1, h) * 1.3, 0, 1)[:, None]
    people = np.clip(sharp + (np.array(GOLD_LIT, dtype=np.float32) / 255.0)[None, None, :] * rim[:, :, None] * 0.3, 0, 1)

    mm = m[:, :, None]
    final = bg * (1 - mm) + people * mm
    u8(np.clip(final, 0, 1)).save(out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=float, default=0.60)
    ap.add_argument("--cy", type=float, default=0.43)
    ap.add_argument("--strength", type=float, default=0.52)
    a = ap.parse_args()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    print(build(a.src, a.out, a.width, 0.5, a.cy, a.strength))
