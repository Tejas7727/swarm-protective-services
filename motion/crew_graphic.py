"""The crew as a graphic: gold halftone dots + gold line art, from the real crew photo.
Writes RGBA layers for the Remotion composition (SwarmCrew)."""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageChops

SRC = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1440
GOLD = (201, 163, 94)

im = Image.open(SRC).convert("RGB").resize((W, H), Image.LANCZOS)
g = ImageOps.grayscale(im)
g = ImageOps.autocontrast(g, cutoff=1)

# fade the venue sign behind their heads (someone else's name) and the floor edge
fade = Image.new("L", (W, H), 255)
d = ImageDraw.Draw(fade)
top = int(H * 0.12)
for y in range(top):
    d.line([(0, y), (W, y)], fill=int(255 * (y / top) ** 2.2))
for y in range(int(H * 0.92), H):
    d.line([(0, y), (W, y)], fill=int(255 * (H - y) / (H * 0.08)))
g = ImageChops.multiply(g, fade)

# halftone: one dot per cell, area following brightness (drawn 3x, then downsampled)
CELL, S = 11, 3
big = Image.new("L", (W * S, H * S), 0)
bd = ImageDraw.Draw(big)
small = g.resize((W // CELL, H // CELL), Image.BOX)
for j in range(small.height):
    for i in range(small.width):
        v = small.getpixel((i, j)) / 255.0
        if v < 0.06:
            continue
        r = (CELL * S / 2) * (v ** 0.75) * 1.05
        cx, cy = (i + 0.5) * CELL * S, (j + 0.5) * CELL * S
        bd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
alpha = big.resize((W, H), Image.LANCZOS)
dots = Image.new("RGBA", (W, H), GOLD + (0,))
dots.putalpha(alpha)
dots.save(os.path.join(OUT, "crew-halftone.png"))

# line art: the edges of the figures, in gold
e = g.filter(ImageFilter.GaussianBlur(1.6)).filter(ImageFilter.FIND_EDGES)
e = ImageOps.autocontrast(e, cutoff=2).point(lambda x: 0 if x < 60 else min(255, int((x - 60) * 2.2)))
e = ImageChops.multiply(e, fade)
lines = Image.new("RGBA", (W, H), (231, 228, 211, 0))
lines.putalpha(e)
lines.save(os.path.join(OUT, "crew-lines.png"))

# a preview of both on charcoal
prev = Image.new("RGBA", (W, H), (10, 12, 14, 255))
prev.alpha_composite(dots)
prev.alpha_composite(lines)
prev.convert("RGB").resize((540, 720)).save(os.path.join(OUT, "preview.jpg"), quality=85)
print("ok", OUT)
