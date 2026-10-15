# -*- coding: utf-8 -*-
"""Export one wide photograph per service page into docs/assets/img/.

Sources: the night scenes generated locally for the approved wireframe (v4),
upscaled 2x (source-art/scene-v6/svc/). People in them are only ever seen from
behind and wear nothing of ours, so no one is passed off as a real officer.
A service with no photograph yet gets a branded placeholder, so the build never
ships a broken image and the gap is obvious on the page.
"""
import os
import sys

from PIL import Image, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "docs", "assets", "img")
WIDTHS = (1600, 800)
AR = 1216 / 832.0                                  # the frame on the service pages

# slug -> (source file, crop centre as a fraction of the height)
SOURCES = {
    "close-protection": ("source-art/scene-v6/svc/close-k.png", 0.5),   # head repainted (close_black.py)
    "event-security": ("source-art/scene-v6/svc/event.png", 0.5),
    "venue-security": ("source-art/scene-v6/svc/venue.png", 0.5),
    "party-bus-security": ("source-art/scene-v6/svc/bus.png", 0.5),
    "limousine-service": ("source-art/scene-v6/svc/limo.png", 0.5),
    "monitoring": ("source-art/scene-v6/svc/monitor.png", 0.5),
}


# Portraits for the about page: the owners, and the crew at a venue.
PORTRAITS = {
    "owners-car": ("source-art/owners/2.jpg", 0.46),
    "owners-wide": ("source-art/owners/4.jpg", 0.46),
    "crew-venue": ("ClientImages/WhatsApp Image 5.jpeg", 0.42),
}
PORTRAIT_AR = 3 / 4.0


def quiet(img):
    """One look across every service page: dark, a little cool, type stays brightest."""
    img = ImageEnhance.Color(img).enhance(0.72)
    img = ImageEnhance.Brightness(img).enhance(0.9)
    return ImageEnhance.Contrast(img).enhance(1.06)


def crop_to(img, fy, ar):
    w, h = img.size
    if w / h > ar:                                 # too wide: trim the sides
        nw = int(round(h * ar))
        x = (w - nw) // 2
        return img.crop((x, 0, x + nw, h))
    nh = int(round(w / ar))                        # too tall: keep the band around fy
    y = int(round(min(max(fy * h - nh / 2, 0), h - nh)))
    return img.crop((0, y, w, y + nh))


def crop_wide(img, fy):
    return crop_to(img, fy, AR)


def placeholder(slug):
    """A clean branded frame, so a missing photograph reads as deliberate."""
    w = 1600
    img = Image.new("RGB", (w, int(w / AR)), (16, 18, 21))
    bee = os.path.join(ROOT, "docs", "assets", "logo", "bee-320.webp")
    if os.path.exists(bee):
        b = Image.open(bee).convert("RGBA")
        s = int(img.height * 0.42)
        b = b.resize((int(s * b.width / b.height), s), Image.LANCZOS)
        a = b.getchannel("A").point(lambda v: int(v * 0.14))
        img.paste(b.convert("RGB"), ((img.width - b.width) // 2, (img.height - b.height) // 2), a)
    return img.filter(ImageFilter.GaussianBlur(0.4))


def build():
    os.makedirs(OUT, exist_ok=True)
    made, missing = [], []
    for slug, (rel, fy) in SOURCES.items():
        src = os.path.join(ROOT, rel.replace("/", os.sep))
        if os.path.exists(src):
            img = quiet(crop_wide(Image.open(src).convert("RGB"), fy))
        else:
            img, = (placeholder(slug),)
            missing.append(slug)
        for w in WIDTHS:
            im = img.resize((w, int(round(w / AR))), Image.LANCZOS)
            im.save(os.path.join(OUT, "svc-%s-%d.webp" % (slug, w)), "WEBP", quality=76, method=6)
        made.append(slug)

    for name, (rel, fy) in PORTRAITS.items():
        src = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.exists(src):
            missing.append(name)
            continue
        img = quiet(crop_to(Image.open(src).convert("RGB"), fy, PORTRAIT_AR))
        for w in (1000, 600):
            im = img.resize((w, int(round(w / PORTRAIT_AR))), Image.LANCZOS)
            im.save(os.path.join(OUT, "own-%s-%d.webp" % (name, w)), "WEBP", quality=78, method=6)
        made.append(name)
    # the owners, cut out of their own photograph (Swarm vests), for the Meet us
    # page: trimmed to the people, a touch darker and cooler, transparent around them
    src = os.path.join(ROOT, "source-art", "owners", "pair-swarm-cut.png")
    if os.path.exists(src):
        cut = Image.open(src).convert("RGBA")
        cut = cut.crop(cut.getbbox())
        rgb = ImageEnhance.Contrast(ImageEnhance.Brightness(ImageEnhance.Color(cut.convert("RGB"))
                                                           .enhance(0.82)).enhance(0.9)).enhance(1.08)
        rgb.putalpha(cut.getchannel("A"))
        for w in (1000, 600):
            rgb.resize((w, int(round(w * rgb.height / rgb.width))), Image.LANCZOS).save(
                os.path.join(OUT, "own-pair-cut-%d.webp" % w), "WEBP", quality=82, method=6)
        made.append("pair-cut")
    else:
        missing.append("pair-cut")
    return made, missing


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    made, missing = build()
    print("exported %d service images -> docs/assets/img/" % len(made))
    if missing:
        print("placeholder (no photograph yet): %s" % ", ".join(missing))
