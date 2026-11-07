"""The crew, drawn for the Remotion films: cut-out figures composed into a group,
then three looks per group for the animation (SwarmPeople.tsx):

    <name>-photo.png  duotone photograph (charcoal shadows, bone highlights)
    <name>-dots.png   gold halftone of the same figures
    <name>-rim.png    a thin gold outline around each figure
    <name>.json       where each figure stands (for the stagger)

Interim figures are free stock (Unsplash), cut out locally (image-studio
cutout, BiRefNet); the client will replace them with their own crew later.
Usage: python people_layers.py <cutout dir> <out dir>
"""
import json
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

CUT, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
GOLD = (201, 163, 94)
SHADOW, HIGH = (12, 14, 15), (236, 226, 204)

# (file stem, head height in source px, horizontal centre on the canvas, head top, extra scale)
HEAD = 200
GROUPS = {
    "lineup": ((1640, 1000), [
        ("1750741268857-7e44510f867d", 490, 250, 150, 1.0),
        ("1618371690240-e0d46eead4b8", 533, 630, 140, 1.0),
        ("1618371731836-2b9bff9ac72a", 239, 1010, 118, 1.08),   # front and centre
        ("1618886614638-80e3c103d31a", 300, 1390, 150, 1.0),
    ]),
    "pair": ((900, 1100), [
        ("1618371690240-e0d46eead4b8", 533, 300, 120, 1.0),
        ("1618371731836-2b9bff9ac72a", 239, 620, 104, 1.05),
    ]),
}


def duotone(rgba):
    g = ImageOps.autocontrast(ImageOps.grayscale(rgba.convert("RGB")), cutoff=0.5)
    g = g.point(lambda v: int(255 * (v / 255) ** 0.85))          # lift the suits a little
    im = ImageOps.colorize(g, SHADOW, HIGH, mid=(120, 106, 84))
    im.putalpha(rgba.getchannel("A"))
    return im


def halftone(rgba, cell=9, s=3):
    W, H = rgba.size
    a = rgba.getchannel("A")
    g = ImageOps.autocontrast(ImageOps.grayscale(rgba.convert("RGB")), cutoff=1)
    small = g.resize((W // cell, H // cell), Image.BOX)
    amask = a.resize((W // cell, H // cell), Image.BOX)
    big = Image.new("L", (W * s, H * s), 0)
    d = ImageDraw.Draw(big)
    for j in range(small.height):
        for i in range(small.width):
            av = amask.getpixel((i, j)) / 255.0
            if av < 0.08:
                continue
            v = 0.16 + 0.84 * (small.getpixel((i, j)) / 255.0)         # every part of a figure gets a dot
            r = (cell * s / 2) * (v ** 0.8) * min(1.0, av * 1.15)      # and the dots thin out with the fade
            cx, cy = (i + .5) * cell * s, (j + .5) * cell * s
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    out = Image.new("RGBA", (W, H), GOLD + (0,))
    out.putalpha(big.resize((W, H), Image.LANCZOS))
    return out


def rim(rgba, width=3):
    a = rgba.getchannel("A").point(lambda v: 255 if v > 110 else 0)
    edge = ImageChops.subtract(a.filter(ImageFilter.MaxFilter(width * 2 + 1)), a)
    edge = edge.filter(ImageFilter.GaussianBlur(.6))
    out = Image.new("RGBA", rgba.size, GOLD + (0,))
    out.putalpha(edge)
    return out


for name, ((W, H), figs) in GROUPS.items():
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bands, bottoms = [], []
    # back to front: the larger "extra scale" figure is pasted last
    for stem, head, cx, top, extra in sorted(figs, key=lambda f: f[4]):
        im = Image.open(os.path.join(CUT, stem + ".png")).convert("RGBA")
        im = im.crop(im.getbbox())
        k = HEAD / head * extra
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        x = round(cx - im.width / 2)
        canvas.alpha_composite(im, (x, top)) if x >= 0 else canvas.paste(im, (x, top), im)
        bands.append({"x0": max(0, x) / W, "x1": min(W, x + im.width) / W, "cx": cx / W})
        bottoms.append(top + im.height)
    # the group fades out toward the bottom edge, so it stands in the page
    # ...ending above the shortest figure's cut, so no flat edge shows
    f1 = min(H, min(bottoms)) - 6
    f0 = int(f1 - H * .34)
    fade = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(fade)
    for y in range(H):
        v = 1 if y < f0 else max(0.0, 1 - (y - f0) / (f1 - f0))
        d.line([(0, y), (W, y)], fill=int(255 * v ** 1.5))
    solid = canvas.copy()
    canvas.putalpha(ImageChops.multiply(canvas.getchannel("A"), fade))
    duotone(canvas).save(os.path.join(OUT, name + "-photo.png"))
    halftone(canvas).save(os.path.join(OUT, name + "-dots.png"))
    r = rim(solid)                                   # the outline of the whole figure, faded the same way
    r.putalpha(ImageChops.multiply(r.getchannel("A"), fade))
    r.save(os.path.join(OUT, name + "-rim.png"))
    bands.sort(key=lambda b: b["cx"])
    json.dump({"w": W, "h": H, "bands": bands}, open(os.path.join(OUT, name + ".json"), "w"), indent=1)
    print(name, W, H, len(bands))
