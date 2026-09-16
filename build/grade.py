# -*- coding: utf-8 -*-
"""Swarm photo pipeline — cinematic split-tone grade + responsive WebP export.

Reads ClientImages/, writes site/assets/img/. Two grade modes:
  plate — lifted midtones, faces read clearly. For images you look at.
  hero  — crushed and vignetted. For images with type sitting on top.

Adjust `jobs` below to re-crop; adjust `cfg` inside grade() to re-grade.
"""
import os, math
from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SRC  = os.path.join(ROOT, "ClientImages")
OUT  = os.path.join(ROOT, "docs", "assets", "img")
os.makedirs(OUT, exist_ok=True)

def ramp(a, b, c):
    out = []
    for ch in range(3):
        col = []
        for i in range(256):
            t = i / 255
            if t < 0.5:
                v = a[ch] + (b[ch] - a[ch]) * (t / 0.5)
            else:
                v = b[ch] + (c[ch] - b[ch]) * ((t - 0.5) / 0.5)
            col.append(int(max(0, min(255, round(v)))))
        out += col
    return out

# split tone: cool charcoal shadows -> neutral mid -> warm bone highlights
LUT_PLATE = ramp((0x1A,0x1D,0x1F), (0x78,0x73,0x66), (0xEE,0xE8,0xD4))
LUT_HERO  = ramp((0x0E,0x10,0x11), (0x5E,0x59,0x4D), (0xE4,0xDC,0xC6))

def curve(img, lo, hi, gamma):
    lut = []
    for i in range(256):
        t = max(0.0, min(1.0, (i/255 - lo) / (hi - lo))) ** gamma
        lut.append(int(round(t * 255)))
    return img.point(lut * len(img.getbands()))

def vignette_mask(w, h, amount, cy_rel=0.46, inner=0.44):
    step = 4
    vg = Image.new("L", (w//step + 1, h//step + 1), 0)
    px = vg.load()
    cx, cy = w/2, h*cy_rel
    maxd = math.hypot(cx, cy)
    for y in range(vg.height):
        for x in range(vg.width):
            d = math.hypot(x*step - cx, y*step - cy) / maxd
            px[x, y] = int(255 * max(0.0, min(1.0, 1 - amount * max(0.0, d-inner)/(1-inner))))
    return vg.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(w/50))

def grade(im, mode="plate"):
    cfg = dict(
        plate=dict(lo=.012, hi=.985, gamma=.80, lut=LUT_PLATE, strength=.62, sat=.34,
                   contrast=1.10, bright=1.06, vig=.34, grain=4),
        hero =dict(lo=.030, hi=.985, gamma=.94, lut=LUT_HERO,  strength=.74, sat=.26,
                   contrast=1.14, bright=.94, vig=.62, grain=5),
    )[mode]
    im = im.convert("RGB")
    im = curve(im, cfg["lo"], cfg["hi"], cfg["gamma"])
    lum = ImageOps.grayscale(im)
    toned = Image.merge("RGB", [lum]*3).point(cfg["lut"])
    base = ImageEnhance.Color(im).enhance(cfg["sat"])
    im = Image.blend(base, toned, cfg["strength"])
    im = ImageEnhance.Contrast(im).enhance(cfg["contrast"])
    im = ImageEnhance.Brightness(im).enhance(cfg["bright"])

    w, h = im.size
    im = Image.composite(im, Image.new("RGB", (w,h), (9,10,11)), vignette_mask(w, h, cfg["vig"]))

    if cfg["grain"]:
        n = Image.effect_noise((w, h), cfg["grain"]).convert("L")
        n = Image.merge("RGB", [n]*3).point(lambda v: 128 + (v-128)*0.22)
        im = ImageChops.overlay(im, n)
    return im

def crop_box(im, focus, ar, zoom=1.0):
    w, h = im.size
    tw, th = w, w/ar
    if th > h: th, tw = h, h*ar
    tw, th = tw/zoom, th/zoom
    cx, cy = focus[0]*w, focus[1]*h
    x0 = max(0, min(w-tw, cx-tw/2)); y0 = max(0, min(h-th, cy-th/2))
    return im.crop((int(x0), int(y0), int(x0+tw), int(y0+th)))

def export(im, name, widths, q=80):
    seen = set()
    for wpx in widths:
        wpx = min(wpx, im.width)
        if wpx in seen: continue
        seen.add(wpx)
        r = im.resize((wpx, max(1, round(im.height*wpx/im.width))), Image.LANCZOS)
        p = os.path.join(OUT, f"{name}-{wpx}.webp")
        r.save(p, "WEBP", quality=q, method=6)
        print(f"  {os.path.basename(p):32s} {r.size[0]}x{r.size[1]}  {os.path.getsize(p)//1024}KB")

S = {
    "lot":   os.path.join(SRC, "WhatsApp Image 2026-09-15 at 6.51.52 AM.jpeg"),
    "wall":  os.path.join(SRC, "WhatsApp Image2.jpeg"),
    "hallw": os.path.join(SRC, "WhatsApp Image3.jpeg"),
    "hallp": os.path.join(SRC, "WhatsApp Image 4.jpeg"),
}

jobs = [
 ("crew-wide",  "wall", 16/9,  (.50,.50), 1.00, "plate", [1600,1200,900,640]),
 ("crew-hero",  "wall", 16/9,  (.50,.50), 1.00, "hero",  [1600,1200,900,640]),
 ("crew-cine",  "wall", 21/9,  (.50,.48), 1.00, "hero",  [1600,1200,900]),
 ("crew-sq",    "wall", 1/1,   (.50,.50), 1.00, "plate", [1000,700,500]),
 ("crew-hall",  "hallw",16/10, (.50,.46), 1.00, "plate", [1600,1200,900,640]),
 ("crew-tall",  "hallp",3/4,   (.50,.50), 1.00, "plate", [1000,760,560]),
 ("crew-lead",  "wall", 4/5,   (.50,.52), 1.70, "plate", [900,700,520]),
 ("faces",      "wall", 21/9,  (.52,.34), 1.40, "plate", [1400,1000,700]),
 ("lot-wide",   "lot",  16/9,  (.50,.50), 1.00, "hero",  [1200,900,640]),
 ("lot-cine",   "lot",  21/9,  (.50,.47), 1.00, "hero",  [1200,900]),
 ("lot-tall",   "lot",  3/4,   (.50,.48), 1.00, "plate", [1000,760,560]),
 ("lot-sq",     "lot",  1/1,   (.50,.46), 1.20, "plate", [900,640]),
 ("hall-tall",  "hallp",9/16,  (.50,.50), 1.00, "hero",  [900,640]),
 ("hall-sq",    "hallw",1/1,   (.50,.48), 1.15, "plate", [900,640]),
]

for name, key, ar, focus, zoom, mode, widths in jobs:
    c = crop_box(Image.open(S[key]), focus, ar, zoom)
    print(name)
    export(grade(c, mode), name, widths)
print("done")
