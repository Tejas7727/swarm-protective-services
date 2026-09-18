# -*- coding: utf-8 -*-
"""Scene plates for the home page camera.

Reads `source-art/scene-v4/` and writes into `docs/assets/scene/`:

  * each plate as WebP at three widths, graded quiet (the copy leads, the
    photograph supports),
  * `scene.json` — what the camera needs: plate sizes, focal points, and the
    portal each push travels through.

A portal is where the next plate sits inside this one (`rect`, in this plate's
normalised coordinates, same aspect as the child) and the opening it is seen
through (`aper`). The camera zooms `rect` up to full frame. On this site every
opening is the dark suit of one of our own people: the camera passes through
the crew into the work.

Sources and rights — see source-art/scene-v4/SOURCES.md:
  crew     client photograph, background softened so the venue is not identifiable
  event    Pexels 13602781 (Pexels licence, free for commercial use); another
           agency's badge on the vest is blurred
  split    left: generated locally (door); right: client photograph (detail)
"""
import json
import os

from PIL import Image, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(ROOT, "source-art", "scene-v4")
OUT = os.path.join(ROOT, "docs", "assets", "scene")

SCALES = (1.0, 0.72, 0.5)
MAXW = 2000
QUALITY = 78

PLATES = [
    {"id": "crew", "file": "crew.png", "grade": (0.62, 0.92, 0.96),
     "focal": [0.50, 0.50], "focalM": [0.50, 0.48],
     "portal": {"child": "event", "aper": [0.466, 0.385, 0.068, 0.13]}},
    # the portrait event photo is trimmed of smoke above and barrier below —
    # neither is ever on screen — and capped at 1600 wide: it was 616 KB
    {"id": "event", "file": "event.png", "grade": (0.5, 0.86, 0.95), "crop": (0.0, 0.12, 1.0, 0.96),
     "maxw": 1600, "focal": [0.52, 0.42], "focalM": [0.53, 0.43],
     "portal": {"child": "split", "aper": [0.492, 0.428, 0.086, 0.083]},
     "portalM": {"child": "split-m", "aper": [0.492, 0.416, 0.086, 0.107]}},
]

# The split is not an image file: the camera draws the two page photos (door,
# detail) side by side on landscape screens and stacked on portrait ones.
# These are its virtual plates, so portals and the pull-out can be computed.
SPLIT = {
    "split":   {"id": "split", "w": 1600, "h": 1000, "focal": [0.5, 0.5], "focalM": [0.5, 0.5],
                "anchor": [0.25, 0.46], "halves": "row"},
    "split-m": {"id": "split-m", "w": 800, "h": 2000, "focal": [0.5, 0.5], "focalM": [0.5, 0.5],
                "anchor": [0.5, 0.23], "halves": "column"},
}


def quiet(img, sat, bright, contrast):
    """Pull every photograph back so the type is the brightest thing on screen."""
    img = ImageEnhance.Color(img).enhance(sat)
    img = ImageEnhance.Brightness(img).enhance(bright)
    return ImageEnhance.Contrast(img).enhance(contrast)


def export(img, stem, maxw=MAXW):
    if img.width > maxw:
        img = img.resize((maxw, round(img.height * maxw / img.width)), Image.LANCZOS)
    out = []
    for s in SCALES:
        w, h = int(round(img.width * s / 2) * 2), int(round(img.height * s / 2) * 2)
        name = "%s-%d.webp" % (stem, w)
        (img if s == 1.0 else img.resize((w, h), Image.LANCZOS)).save(
            os.path.join(OUT, name), "WEBP", quality=QUALITY, method=6)
        out.append({"w": w, "h": h, "src": "assets/scene/" + name})
    return out


def portal_rect(parent, child, aper):
    """Centre the child on the opening, sized so the opening sits well inside it."""
    cx, cy = aper[0] + aper[2] / 2, aper[1] + aper[3] / 2
    w = max(aper[2], aper[3] * parent["h"] / parent["w"] * child["w"] / child["h"]) * 1.6
    h = w * parent["w"] / parent["h"] * child["h"] / child["w"]
    return [round(cx - w / 2, 5), round(cy - h / 2, 5), round(w, 5), round(h, 5)]


def build():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".webp"):
            os.remove(os.path.join(OUT, f))
    plates = {}
    for spec in PLATES:
        img = quiet(Image.open(os.path.join(SRC, spec["file"])).convert("RGB"), *spec["grade"])
        if "crop" in spec:
            c = spec["crop"]
            img = img.crop((int(c[0] * img.width), int(c[1] * img.height), int(c[2] * img.width), int(c[3] * img.height)))
        sizes = export(img, spec["id"], spec.get("maxw", MAXW))
        plates[spec["id"]] = {"id": spec["id"], "w": sizes[0]["w"], "h": sizes[0]["h"], "sizes": sizes,
                              "focal": spec["focal"], "focalM": spec.get("focalM", spec["focal"])}
        if "anchor" in spec:
            plates[spec["id"]]["anchor"] = spec["anchor"]
    plates.update(SPLIT)
    for spec in PLATES:
        for key in ("portal", "portalM"):
            if key in spec:
                p = spec[key]
                parent, child = plates[spec["id"]], plates[p["child"]]
                plates[spec["id"]][key] = {"child": p["child"], "aper": p["aper"],
                                           "rect": portal_rect(parent, child, p["aper"])}
    # the two halves of the split, one file each (4:5), used by the page and the camera alike
    split = quiet(Image.open(os.path.join(SRC, "split.png")).convert("RGB"), 0.5, 0.86, 0.95)
    half = split.width // 2
    halves = {}
    for name, box in (("door", (0, 0, half, split.height)), ("detail", (half, 0, split.width, split.height))):
        im = split.crop(box)
        halves[name] = []
        for w in (1000, 700):
            h = int(w * 1.25)
            im.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, "%s-%d.webp" % (name, w)), "WEBP", quality=QUALITY, method=6)
            halves[name].append({"w": w, "h": h, "src": "assets/scene/%s-%d.webp" % (name, w)})
    scene = {"plates": [plates[s["id"]] for s in PLATES] + [SPLIT["split"], SPLIT["split-m"]], "halves": halves}
    with open(os.path.join(OUT, "scene.json"), "w", encoding="utf-8") as fh:
        json.dump(scene, fh, separators=(",", ":"))
    return scene


if __name__ == "__main__":
    for p in build()["plates"]:
        print(p["id"], p["w"], "x", p["h"], {k: p[k]["rect"] for k in ("portal", "portalM") if k in p})
