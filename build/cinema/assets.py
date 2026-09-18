# -*- coding: utf-8 -*-
"""Scene assets for the push-through film.

Takes the art in `source-art/scene-v3/` and writes, into `docs/assets/scene/`:

  * every plate as WebP at three widths (the camera only ever magnifies the
    plate it is pushing into, so three steps is plenty),
  * the hero cut-out cropped to its alpha, with the rect it occupies in its
    plate so the engine can put it back exactly where it was,
  * `scene.json` — the camera manifest: portals, apertures, grades, layers.

The portal is where the next scene sits inside this one; the aperture is the
opening you see it through (a doorway, a corridor, the road out of an alley).
The engine zooms the portal up to full frame, so the two together are the cut.
"""
import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(ROOT, "source-art", "scene-v3")
OUT = os.path.join(ROOT, "docs", "assets", "scene")

SCALES = (1.0, 0.72, 0.5)
QUALITY = 82

# Each stop: the plate, how it is graded, where the next scene lives inside it.
# rect  — where the child plate is drawn, in this plate's normalised coordinates
#         (same aspect as the child, so w and h are the same fraction).
# aper  — the opening it is seen through, before the camera arrives.
PLATES = [
    {
        "id": "street", "file": "p0-street.png",
        "focal": [0.50, 0.55], "focalM": [0.62, 0.56],
        "grade": {"exp": 1.02, "tint": [0.97, 0.99, 1.06], "lift": 0.0},
        "layers": [{"file": "p0-hero.png", "depth": 1.85, "fade": [0.14, 0.42]}],
        "portal": {"rect": [0.2275, 0.3900, 0.26, 0.2078],
                   "aper": [0.315, 0.436, 0.085, 0.116], "feather": 0.9, "depth": 2.4},
    },
    {
        "id": "door", "file": "p1-door.png",
        "focal": [0.55, 0.44], "focalM": [0.55, 0.42],
        "grade": {"exp": 0.94, "tint": [1.00, 0.985, 1.00], "lift": 0.0},
        "portal": {"rect": [0.4225, 0.290, 0.26, 0.26],
                   "aper": [0.478, 0.225, 0.150, 0.390], "feather": 0.7, "depth": 2.2},
    },
    {
        "id": "floor", "file": "p2-floor.png",
        "focal": [0.56, 0.48], "focalM": [0.62, 0.46],
        "grade": {"exp": 0.92, "tint": [1.00, 0.97, 0.96], "lift": 0.0},
        "layers": [{"file": "p2-officer.png", "depth": 1.8, "fade": [0.10, 0.34]}],
        "portal": {"rect": [0.5925, 0.275, 0.26, 0.26],
                   "aper": [0.655, 0.320, 0.135, 0.170], "feather": 0.95, "depth": 2.4},
    },
    {
        "id": "exit", "file": "p3-exit.png",
        "focal": [0.58, 0.50], "focalM": [0.64, 0.50],
        "grade": {"exp": 1.00, "tint": [0.96, 0.99, 1.07], "lift": 0.0},
        "portal": {"rect": [0.680, 0.330, 0.26, 0.26],
                   "aper": [0.740, 0.375, 0.140, 0.170], "feather": 0.95, "depth": 2.4,
                   "cross": 0.55, "flood": [1.0, 0.93, 0.82]},
    },
    {
        "id": "dawn", "file": "p4-dawn.png",
        "focal": [0.50, 0.50], "focalM": [0.52, 0.48],
        "grade": {"exp": 1.04, "tint": [1.04, 1.00, 0.97], "lift": 0.02},
    },
]


def _export(img, stem, alpha=False):
    """Write three widths; return the srcset list, widest first."""
    out = []
    for s in SCALES:
        w = int(round(img.width * s / 2) * 2)
        h = int(round(img.height * s / 2) * 2)
        name = "%s-%d.webp" % (stem, w)
        im = img.resize((w, h), Image.LANCZOS) if s != 1.0 else img
        im.save(os.path.join(OUT, name), "WEBP", quality=QUALITY,
                method=6, exact=alpha)
        out.append({"w": w, "h": h, "src": "assets/scene/" + name})
    return out


def build():
    os.makedirs(OUT, exist_ok=True)
    scene = {"plates": []}
    for i, spec in enumerate(PLATES):
        img = Image.open(os.path.join(SRC, spec["file"])).convert("RGB")
        entry = {
            "id": spec["id"], "w": img.width, "h": img.height,
            "sizes": _export(img, spec["id"]),
            "focal": spec["focal"], "focalM": spec["focalM"], "grade": spec["grade"],
            "layers": [],
        }
        flat = None
        for layer in spec.get("layers", []):
            cut = Image.open(os.path.join(SRC, layer["file"])).convert("RGBA")
            flat = Image.alpha_composite((flat or img).convert("RGBA"), cut).convert("RGB")
            box = cut.getbbox()                     # crop to the figure
            crop = cut.crop(box)
            stem = "%s-%s" % (spec["id"], os.path.splitext(layer["file"])[0].split("-")[-1])
            entry["layers"].append({
                "sizes": _export(crop, stem, alpha=True),
                "rect": [box[0] / cut.width, box[1] / cut.height,
                         (box[2] - box[0]) / cut.width, (box[3] - box[1]) / cut.height],
                "depth": layer["depth"], "fade": layer["fade"],
            })
        # one flattened frame per plate: what a browser with no WebGL, or a
        # visitor who asked for no motion, sees as a plain background
        entry["flat"] = _export(flat, spec["id"] + "-flat")[1]["src"] if flat \
            else entry["sizes"][1]["src"]
        if "portal" in spec:
            entry["portal"] = dict({"depth": 2.2}, **dict(spec["portal"], child=i + 1))
        scene["plates"].append(entry)
    with open(os.path.join(OUT, "scene.json"), "w", encoding="utf-8") as fh:
        json.dump(scene, fh, separators=(",", ":"))
    return scene


if __name__ == "__main__":
    s = build()
    for p in s["plates"]:
        print(p["id"], p["w"], "x", p["h"], "layers:", len(p["layers"]),
              "portal:" if "portal" in p else "end", p.get("portal", {}).get("rect", ""))
