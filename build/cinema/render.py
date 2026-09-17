# -*- coding: utf-8 -*-
"""Render build/cinema/index.html (the scroll film) into docs/index.html."""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import common                                       # noqa: E402
from common import AREAS, BIZ, asset_version, canonical, faq_schema, plain  # noqa: E402
from home import FAQS                               # noqa: E402

# approximate municipal centres (lat, lon)
CITIES = [
    ("Toronto", 43.6532, -79.3832), ("Etobicoke", 43.6205, -79.5132), ("North York", 43.7615, -79.4111),
    ("Scarborough", 43.7764, -79.2318), ("Mississauga", 43.5890, -79.6441), ("Brampton", 43.7315, -79.7624),
    ("Vaughan", 43.8361, -79.4983), ("Markham", 43.8561, -79.3370), ("Richmond Hill", 43.8828, -79.4403),
    ("Oakville", 43.4675, -79.6877), ("Burlington", 43.3255, -79.7990), ("Hamilton", 43.2557, -79.8711),
    ("Pickering", 43.8384, -79.0868), ("Ajax", 43.8509, -79.0204), ("Whitby", 43.8975, -78.9429),
    ("Oshawa", 43.8971, -78.8658), ("Milton", 43.5183, -79.8774), ("Newmarket", 44.0592, -79.4613),
]
SHORE = [(43.24, -79.98), (43.27, -79.84), (43.31, -79.79), (43.44, -79.67), (43.55, -79.58),
         (43.60, -79.50), (43.635, -79.38), (43.70, -79.23), (43.81, -79.08), (43.83, -79.02),
         (43.85, -78.94), (43.86, -78.85), (43.87, -78.72)]

W, H = 1200, 640
LON0, LON1, LAT0, LAT1 = -80.02, -78.68, 44.12, 43.18


def xy(lat, lon):
    return ((lon - LON0) / (LON1 - LON0) * W, (lat - LAT0) / (LAT1 - LAT0) * H)


def map_svg():
    hx, hy = xy(CITIES[0][1], CITIES[0][2])
    shore = " ".join("%s%.1f %.1f" % ("M" if i == 0 else "L", *xy(la, lo)) for i, (la, lo) in enumerate(SHORE))
    lake = shore + " L%.1f %.1f L0 %.1f Z" % (W, H, H)
    others = sorted(CITIES[1:], key=lambda c: (xy(c[1], c[2])[0] - hx) ** 2 + (xy(c[1], c[2])[1] - hy) ** 2)
    routes, dots, lbls = [], [], []
    for name, la, lo in others:
        x, y = xy(la, lo)
        mx, my = (hx + x) / 2, (hy + y) / 2 - abs(x - hx) * 0.12
        routes.append('<path class="gm__route" pathLength="1" d="M%.1f %.1f Q%.1f %.1f %.1f %.1f"/>' % (hx, hy, mx, my, x, y))
        dots.append('<circle class="gm__dot" cx="%.1f" cy="%.1f" r="4.5"/>' % (x, y))
        anchor = "end" if x > W * 0.78 else "start"
        dx = -9 if anchor == "end" else 9
        lbls.append('<text class="gm__lbl" x="%.1f" y="%.1f" text-anchor="%s">%s</text>' % (x + dx, y - 8, anchor, name))
    return ('<svg viewBox="0 0 %d %d" role="img" aria-label="Map of the Greater Toronto Area service area">'
            '<path class="gm__lake" d="%s"/>%s'
            '<circle class="gm__ring" cx="%.1f" cy="%.1f" r="14"/>%s'
            '<circle class="gm__dot gm__dot--hq" cx="%.1f" cy="%.1f" r="7"/>%s'
            '<text class="gm__lbl" x="%.1f" y="%.1f" style="fill:#E7E4D3">Toronto</text></svg>'
            % (W, H, lake, "".join(routes), hx, hy, "".join(dots), hx, hy, "".join(lbls), hx + 12, hy + 22))


def faq_html():
    return "".join('<details><summary>%s</summary><div class="a">%s</div></details>' % (q, a) for q, a in FAQS)


def render():
    src = io.open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
    base = common.MODE["preview_base"] if common.MODE["preview"] else BIZ["base"]
    service_schema = "".join(
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service",'
        '"name":"%s","serviceType":"%s","url":"%s/#%s","provider":{"@id":"%s/#org"},'
        '"areaServed":{"@type":"State","name":"Ontario"}}</script>' % (n, n, BIZ["base"], a, BIZ["base"])
        for n, a in [("Nightclub and bar security", "venues"), ("Event security", "events"),
                     ("Close protection and executive protection", "protection"),
                     ("High-risk protective detail", "high-risk")])
    schema = ('<script type="application/ld+json">%s</script>' % common.org_schema()) + service_schema \
        + faq_schema([(q, plain(a)) for q, a in FAQS])
    tokens = {
        "TITLE": "Security Company Toronto — Door Staff &amp; Close Protection | Swarm",
        "DESC": "Licensed security company in Toronto and the GTA — nightclub and bar door staff, event "
                "security and close protection. Same crew every week. Dispatch answered 24 hours.",
        "CANON": canonical("/"),
        "ROBOTS": "noindex,nofollow" if common.MODE["preview"] else "index,follow,max-image-preview:large",
        "BASE": base.rstrip("/"),
        "PHONE_UI": BIZ["phone_ui"], "PHONE_TEL": BIZ["phone_tel"], "EMAIL": BIZ["email"],
        "LICENCE": BIZ["licence"], "IG": BIZ["ig"], "TT": BIZ["tt"],
        "CSSV": asset_version("assets/cine/cine.css"), "JSV": asset_version("assets/cine/cine.js"),
        "BEEV": asset_version("assets/cine/bee-points.js"),
        "MAP": map_svg(), "FAQ": faq_html(), "SCHEMA": schema,
        "AREAS": "Service area: " + ", ".join(AREAS) + ".",
    }
    for k, v in tokens.items():
        src = src.replace("{{%s}}" % k, v)
    left = [t for t in ("{{",) if t in src]
    if left:
        raise SystemExit("unreplaced token in cinema template")
    return src
