# -*- coding: utf-8 -*-
"""Generate 1200x630 Open Graph cards for every page. Pillow only."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
IMG = os.path.join(ROOT, "docs", "assets", "img")
OUT = os.path.join(ROOT, "docs", "assets", "og")
FONTS = os.path.join(HERE, "fonts")
LOGO = os.path.join(ROOT, "brand", "png", "swarm-horizontal-gold.png")
os.makedirs(OUT, exist_ok=True)

W, H = 1200, 630
GOLD = (214, 178, 116)
GOLD_D = (184, 145, 78)
BONE = (231, 228, 211)
MUTE = (150, 147, 138)
INK = (8, 9, 10)


def f(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name + ".ttf"), size)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def card(out_name, headline, kicker, photo, focus=0.5):
    base = Image.new("RGB", (W, H), INK)

    # photo, cover-cropped, pushed right
    src = Image.open(os.path.join(IMG, photo)).convert("RGB")
    scale = max(W / src.width, H / src.height)
    src = src.resize((max(W, round(src.width * scale)), max(H, round(src.height * scale))), Image.LANCZOS)
    x = int((src.width - W) * focus)
    y = int((src.height - H) * 0.32)
    base.paste(src.crop((x, y, x + W, y + H)), (0, 0))

    # left-to-right scrim so type always has contrast
    scrim = Image.new("L", (W, 1))
    for i in range(W):
        t = i / (W - 1)
        scrim.putpixel((i, 0), int(255 * max(0.0, min(1.0, 1.0 - (t - 0.40) / 0.46)) ** 0.85))
    scrim = scrim.resize((W, H))
    base = Image.composite(Image.new("RGB", (W, H), INK), base, scrim)

    # bottom fade
    fade = Image.new("L", (1, H))
    for j in range(H):
        t = j / (H - 1)
        fade.putpixel((0, j), int(255 * (max(0.0, (t - 0.66) / 0.34) ** 1.2) * 0.92))
    base = Image.composite(Image.new("RGB", (W, H), INK), base, fade.resize((W, H)))

    d = ImageDraw.Draw(base)

    PAD = 68
    # gold hairline top
    d.rectangle([0, 0, W, 3], fill=GOLD_D)

    # kicker
    fk = f("saira600", 21)
    d.text((PAD, 74), kicker.upper(), font=fk, fill=GOLD, spacing=0)

    # headline
    fh = f("saira800", 76)
    lines = wrap(d, headline.upper(), fh, W * 0.50)
    if len(lines) > 3:
        fh = f("saira800", 60)
        lines = wrap(d, headline.upper(), fh, W * 0.52)
    ly = 74 + 46
    for ln in lines:
        d.text((PAD - 4, ly), ln, font=fh, fill=BONE)
        ly += int(fh.size * 0.94)

    # logo bottom-left
    logo = Image.open(LOGO).convert("RGBA")
    lw = 260
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    base.paste(logo, (PAD - 6, H - logo.height - 58), logo)

    # credentials bottom-right
    fb = f("archivo500", 20)
    txt = "PSISA licensed  ·  $5M liability  ·  Dispatch 24h"
    tw = d.textlength(txt, font=fb)
    d.text((W - PAD - tw, H - 82), txt, font=fb, fill=MUTE)

    # gold rule above footer row
    d.rectangle([PAD, H - 118, W - PAD, H - 117], fill=(60, 58, 52))

    # grain
    n = Image.effect_noise((W, H), 4).convert("L")
    base = ImageChops.overlay(base, Image.merge("RGB", [n] * 3).point(lambda v: 128 + (v - 128) * 0.16))

    p = os.path.join(OUT, out_name)
    base.save(p, "JPEG", quality=84, optimize=True, progressive=True)
    print("  %-26s %5d KB" % (out_name, os.path.getsize(p) // 1024))


CARDS = [
    ("og-home.jpg",     "Nothing happened.",            "Door staff · events · close protection · GTA", "crew-hero-1600.webp", 0.5),
    ("og-default.jpg",  "Swarm Protective Services",    "Licensed protection across the GTA",           "crew-wide-1600.webp", 0.5),
    ("og-venue.jpg",    "Door staff who know your room","Bars · nightclubs · lounges",                  "crew-wide-1600.webp", 0.62),
    ("og-event.jpg",    "Your event runs. We handle the rest.", "Concerts · weddings · corporate · film","crew-hall-1600.webp", 0.55),
    ("og-cp.jpg",       "Protection that reads as staff","Executive · personal · family",               "lot-wide-1200.webp",  0.5),
    ("og-highrisk.jpg", "When an ordinary guard is the wrong answer", "Threat-assessed details",        "lot-cine-1200.webp",  0.5),
    ("og-about.jpg",    "The part of the night you never think about", "The crew",                      "crew-hall-1600.webp", 0.45),
    ("og-contact.jpg",  "Tell us the night.",           "Dispatch answered 24 hours",                   "crew-wide-1600.webp", 0.4),
]

if __name__ == "__main__":
    for name, head, kick, photo, focus in CARDS:
        card(name, head, kick, photo, focus)
    print("og cards done")
