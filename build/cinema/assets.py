# -*- coding: utf-8 -*-
"""Assets for the "One Night" scroll film.

    python build/cinema/assets.py

Reads   ClientImages/  +  build/cinema/cutouts/*.png  (hyperframes remove-background)
Writes  docs/assets/cine/
  <name>-plate-<w>.webp   graded full frame (hero grade — type and crew sit on it)
  <name>-crew-<w>.webp    graded cutout with alpha, pixel-aligned to its plate
  bee-points.js           particle targets sampled from the bee emblem
  report.json             aperture centre inside the shield (for the push-through)
"""
import json
import math
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "build"))
import grade as G  # noqa: E402

SRC = os.path.join(ROOT, "ClientImages")
CUT = os.path.join(HERE, "cutouts")
OUT = os.path.join(ROOT, "docs", "assets", "cine")
os.makedirs(OUT, exist_ok=True)

PHOTOS = {
    "wall":  "WhatsApp Image2.jpeg",
    "hallw": "WhatsApp Image3.jpeg",
    "hallp": "WhatsApp Image 4.jpeg",
    "lot":   "WhatsApp Image 2026-09-15 at 6.51.52 AM.jpeg",
}


def tone(im, lo, hi, gamma, lut, strength, sat, contrast, bright):
    """The grade from build/grade.py without vignette or grain, so a cutout can be
    toned independently of the frame edges it used to sit in."""
    im = G.curve(im.convert("RGB"), lo, hi, gamma)
    lum = ImageOps.grayscale(im)
    toned = Image.merge("RGB", [lum] * 3).point(lut)
    base = ImageEnhance.Color(im).enhance(sat)
    im = Image.blend(base, toned, strength)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    return ImageEnhance.Brightness(im).enhance(bright)


def grain(im, amount=4, mix=0.2):
    n = Image.effect_noise(im.size, amount).convert("L")
    n = Image.merge("RGB", [n] * 3).point(lambda v: 128 + (v - 128) * mix)
    return ImageChops.overlay(im, n)


def save(im, name, widths, q=78):
    for w in widths:
        w = min(w, im.width)
        r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        p = os.path.join(OUT, "%s-%d.webp" % (name, w))
        r.save(p, "WEBP", quality=q, method=6, alpha_quality=90)
        print("  %-26s %4dx%-4d %4d KB" % (os.path.basename(p), r.width, r.height, os.path.getsize(p) // 1024))


def plates_and_crews():
    for key, fn in PHOTOS.items():
        src = Image.open(os.path.join(SRC, fn)).convert("RGB")

        # the plate sits behind: darker, softer, so the crew in front owns the light
        plate = G.grade(src, "hero")
        save(plate, key + "-plate", [1600, 960])

        cut = Image.open(os.path.join(CUT, key + ".png")).convert("RGBA")
        alpha = cut.split()[3]
        # tighten the matte edge a touch: kill the soft halo the model leaves on dark suits
        alpha = alpha.point(lambda v: 0 if v < 28 else min(255, int((v - 28) * 1.12)))
        alpha = alpha.filter(ImageFilter.GaussianBlur(0.6))
        rgb = tone(cut, lo=.01, hi=.98, gamma=.78, lut=G.LUT_PLATE, strength=.6, sat=.36,
                   contrast=1.12, bright=1.08)
        rgb = grain(rgb, 4, .18)
        crew = rgb.copy()
        crew.putalpha(alpha)
        save(crew, key + "-crew", [1600, 960], q=80)

        # clean background: crew removed and filled, pre-blurred and darkened. It is what
        # the room looks like out of focus once the crew steps toward the camera — with
        # no ghost doubles, because there is no crew left in it.
        save(clean_plate(plate, alpha), key + "-bg", [1600, 960], q=72)


def clean_plate(plate, alpha):
    """Normalised-convolution fill: blur(image*known) / blur(known), coarse to fine."""
    hole = alpha.point(lambda v: 255 if v > 20 else 0).filter(ImageFilter.MaxFilter(21))
    known = ImageOps.invert(hole)
    w, h = plate.size
    small = (w // 4, h // 4)
    img = plate.resize(small, Image.BILINEAR)
    k = known.resize(small, Image.BILINEAR)
    filled = img.copy()
    for radius in (60, 30, 14, 6):
        num = ImageChops.multiply(img, Image.merge("RGB", [k] * 3)).filter(ImageFilter.GaussianBlur(radius))
        den = k.filter(ImageFilter.GaussianBlur(radius))
        dpx, npx, fpx, kpx = den.load(), num.load(), filled.load(), k.load()
        for y in range(small[1]):
            for x in range(small[0]):
                if kpx[x, y] < 250:
                    d = dpx[x, y]
                    if d > 3:
                        n = npx[x, y]
                        fpx[x, y] = (min(255, n[0] * 255 // d), min(255, n[1] * 255 // d), min(255, n[2] * 255 // d))
        img = filled
    bg = filled.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(10))
    bg = ImageEnhance.Brightness(bg).enhance(.62)
    return grain(bg, 5, .22)


def bee_points(n_target=2200):
    """Sample the bee emblem into particle targets. Gold body vs bone wings keep
    their colour so the assembled swarm reads as the real mark."""
    im = Image.open(os.path.join(ROOT, "brand", "png", "swarm-emblem-gold.png")).convert("RGBA")
    scale = 220 / im.width
    small = im.resize((220, round(im.height * scale)), Image.LANCZOS)
    px = small.load()
    pts = []
    for y in range(small.height):
        for x in range(small.width):
            r, g, b, a = px[x, y]
            if a < 150:
                continue
            bone = (r + g + b) / 3 > 190 and abs(r - b) < 45
            pts.append((x, y, 1 if bone else 0))
    stride = max(1, len(pts) // n_target)
    pts = pts[::stride]
    w, h = small.width, small.height
    s = max(w, h)
    flat = []
    for x, y, c in pts:
        flat += [round((x - w / 2) / s, 4), round((y - h / 2) / s, 4), c]
    js = "window.BEE_POINTS=%s;window.BEE_ASPECT=%s;" % (json.dumps(flat, separators=(",", ":")), round(h / w, 4))
    p = os.path.join(OUT, "bee-points.js")
    open(p, "w", encoding="utf-8").write(js)
    print("  bee-points.js              %d particles  %d KB" % (len(pts), os.path.getsize(p) // 1024))


def shield_aperture():
    """Find the deepest empty point inside the emblem's shield. Scaling the emblem
    around that point pushes the camera through darkness, not into the bee's body."""
    im = Image.open(os.path.join(ROOT, "brand", "png", "swarm-emblem-gold.png")).convert("RGBA")
    small = im.resize((240, round(im.height * 240 / im.width)), Image.LANCZOS)
    solid = small.split()[3].point(lambda v: 255 if v > 60 else 0)

    # mark the outside of the shield by flooding from the corners
    outside = solid.copy()
    for seed in [(0, 0), (outside.width - 1, 0), (0, outside.height - 1),
                 (outside.width - 1, outside.height - 1)]:
        if outside.getpixel(seed) == 0:
            ImageDraw.floodfill(outside, seed, 128)

    # interior empty pixels = neither solid nor outside; erode until one blob is left
    interior = outside.point(lambda v: 255 if v == 0 else 0)
    last = interior
    for _ in range(60):
        nxt = last.filter(ImageFilter.MinFilter(3))
        if not nxt.getbbox():
            break
        last = nxt
    box = last.getbbox()
    cx = (box[0] + box[2]) / 2 / small.width
    cy = (box[1] + box[3]) / 2 / small.height
    data = {"aperture": [round(cx, 4), round(cy, 4)], "emblemAspect": round(small.height / small.width, 4)}
    open(os.path.join(OUT, "report.json"), "w").write(json.dumps(data))
    print("  shield aperture           ", data)
    return data


if __name__ == "__main__":
    plates_and_crews()
    bee_points()
    shield_aperture()
