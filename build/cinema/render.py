# -*- coding: utf-8 -*-
"""Render the home page: five screens and a form.

    home -> what we do -> on the job -> across the GTA -> the crew -> get a quote

The markup is a complete static page first: each screen is a section with its
own image and copy, readable with no JavaScript, no WebGL and no motion. The
camera in site.js is an enhancement laid over those same sections — it never
owns the content, so nothing on the page depends on it.

Copy lives in content.py; plate geometry in assets.py.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import common                                                       # noqa: E402
from common import AREAS, BIZ, ICONS, asset_version, canonical      # noqa: E402
import content as C                                                 # noqa: E402

PHONE_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 2.5 9 7l-2 2.2a13 13 0 0 0 '
              '5.8 5.8L15 13l4.5 2.4-1.2 4a2 2 0 0 1-2.2 1.4C8.6 20 4 15.4 2.7 6.9A2 2 0 0 1 4.1 '
              '4.7l2.5-2.2Z"/></svg>')
MAIL_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18v14H3V5Zm2.4 2 6.6 5 '
             '6.6-5H5.4Zm13.6 2.3-7 5.3-7-5.3V17h14V9.3Z"/></svg>')

# approximate municipal centres (lat, lon), Toronto first
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
MW, MH = 1200, 640
LON0, LON1, LAT0, LAT1 = -80.02, -78.68, 44.12, 43.18
# labels that would collide with a neighbour go to the other side
LEFT = {"Etobicoke", "Mississauga", "Oakville", "Burlington", "Hamilton", "Milton", "Brampton", "Vaughan", "Pickering"}
# Phones see a tighter window of the map (data-narrow), so labels are placed
# for it separately: (dx, dy, anchor). Cities outside that window keep their
# pin and lose only the label. All labels are decorative — every city is named
# in the map's <title>.
PHONE = {
    "Mississauga": (0, 30, "middle"), "Brampton": (14, 5, "start"), "Vaughan": (14, 5, "start"),
    "Richmond Hill": (0, -18, "middle"), "Markham": (14, 5, "start"), "North York": (14, 5, "start"),
    "Scarborough": (14, 5, "start"), "Etobicoke": (-14, 5, "end"), "Newmarket": (14, 5, "start"),
    "Pickering": (-14, 5, "end"),
}


def xy(lat, lon):
    return ((lon - LON0) / (LON1 - LON0) * MW, (lat - LAT0) / (LAT1 - LAT0) * MH)


def map_svg():
    hx, hy = xy(CITIES[0][1], CITIES[0][2])
    shore = " ".join("%s%.1f %.1f" % ("M" if i == 0 else "L", *xy(la, lo)) for i, (la, lo) in enumerate(SHORE))
    lake = shore + " L%.1f %.1f L0 %.1f Z" % (MW, MH, MH)
    grid = "".join('<line class="gm__grid" x1="%d" y1="0" x2="%d" y2="%d"/>' % (x, x, MH)
                   for x in range(100, MW, 100))
    grid += "".join('<line class="gm__grid" x1="0" y1="%d" x2="%d" y2="%d"/>' % (y, MW, y)
                    for y in range(80, MH, 80))
    routes, pins, labels = [], [], []
    for name, la, lo in CITIES[1:]:
        x, y = xy(la, lo)
        mx, my = (hx + x) / 2, (hy + y) / 2 - abs(x - hx) * 0.1
        routes.append('<path class="gm__route" pathLength="1" d="M%.1f %.1f Q%.1f %.1f %.1f %.1f"/>'
                      % (hx, hy, mx, my, x, y))
        pins.append('<image class="gm__pin" href="assets/logo/bee-160.webp" x="%.1f" y="%.1f" '
                    'width="17" height="20"/>' % (x - 8.5, y - 10))
        left = name in LEFT
        labels.append('<text class="gm__lbl gm__lbl--d" x="%.1f" y="%.1f" text-anchor="%s">%s</text>'
                      % (x + (-14 if left else 14), y + 5, "end" if left else "start", name))
        if name in PHONE:
            dx, dy, anchor = PHONE[name]
            labels.append('<text class="gm__lbl gm__lbl--m" x="%.1f" y="%.1f" text-anchor="%s">%s</text>'
                          % (x + dx, y + dy, anchor, name))
    return ('<svg class="gm" viewBox="0 0 %d %d" data-full="0 0 %d %d" data-narrow="215 20 700 600" '
            'role="img" aria-labelledby="gm-title"><title id="gm-title">Map of the 18 Greater Toronto '
            'Area cities Swarm covers: %s.</title>'
            '<g aria-hidden="true">%s<path class="gm__lake" d="%s"/><path class="gm__shore" d="%s"/>'
            '%s%s'
            '<circle class="gm__ring" cx="%.1f" cy="%.1f" r="30"/>'
            '<image class="gm__hq" id="gm-hq" href="assets/logo/emblem-108.webp" x="%.1f" y="%.1f" '
            'width="40" height="44"/>%s'
            '<text class="gm__lbl gm__lbl--hq" x="%.1f" y="%.1f" text-anchor="middle">Toronto</text></g></svg>'
            % (MW, MH, MW, MH, ", ".join(c[0] for c in CITIES), grid, lake, shore,
               "".join(routes), "".join(pins), hx, hy, hx - 20, hy - 22, "".join(labels), hx, hy + 44))


def btn_quote(cls="btn"):
    return '<a class="%s" href="#contact" data-quote><span>%s</span></a>' % (cls, C.HOME["quote"])


def btn_call(cls="btn btn--ghost", label=None):
    return ('<a class="%s" href="tel:%s">%s<span>%s</span></a>'
            % (cls, BIZ["phone_tel"], PHONE_ICON, label or C.HOME["call"]))


def img_tag(plate, cls, alt, sizes="100vw", priority=False):
    srcset = ", ".join("%s %dw" % (s["src"], s["w"]) for s in plate["sizes"])
    return ('<img class="%s" src="%s" srcset="%s" sizes="%s" alt="%s" width="%d" height="%d"%s decoding="async">'
            % (cls, plate["sizes"][1]["src"], srcset, sizes, alt, plate["w"], plate["h"],
               ' fetchpriority="high"' if priority else ' loading="lazy"'))


def stops_html(scene):
    P = {p["id"]: p for p in scene["plates"]}

    def half_img(name, alt):
        sizes = scene["halves"][name]
        return ('<img class="split__img" src="%s" srcset="%s" sizes="(orientation: portrait) 100vw, 50vw" alt="%s" '
                'width="%d" height="%d" loading="lazy" decoding="async">'
                % (sizes[1]["src"], ", ".join("%s %dw" % (x["src"], x["w"]) for x in sizes), alt,
                   sizes[0]["w"], sizes[0]["h"]))
    S, W, V, K = C.SERVICES, C.WORK, C.COVERAGE, C.CREW

    home = """<section class="stop stop--home" id="home" data-stop="0" aria-labelledby="h-home">
<div class="stop__media">{img}</div>
<div class="stop__copy home">
<h1 id="h-home" class="home__name" aria-label="{name}"><span class="home__row"><img class="home__mark" src="assets/logo/emblem-216.webp" alt="" width="216" height="238"><span class="home__swarm">SWARM</span></span><span class="home__ps">PROTECTIVE SERVICES</span></h1>
<p class="home__line">{line}</p>
<div class="acts home__acts" id="hero-cta">{q}{c}</div>
</div>
</section>""".format(img=img_tag(P["crew"], "stop__img", "The Swarm crew: six officers in black suits.", priority=True),
                     name=BIZ["name"], line=C.HOME["line"], q=btn_quote(), c=btn_call())

    items = "".join('<li><b>%s</b><span>%s</span></li>' % it for it in S["items"])
    creds = "".join("<li>%s</li>" % c for c in S["creds"])
    services = """<section class="stop stop--services" id="services" data-stop="1" aria-labelledby="h-services">
<div class="stop__media">{img}</div>
<div class="stop__copy svc">
<h2 id="h-services" class="kicker">{k}</h2>
<ul class="svc__list">{items}</ul>
<ul class="creds" aria-label="Licences and insurance">{creds}</ul>
</div>
</section>""".format(img=img_tag(P["event"], "stop__img", "A security officer at the barrier in front of a concert crowd."),
                     k=S["kicker"], items=items, creds=creds)

    work = """<section class="stop stop--work" id="work" data-stop="2" aria-labelledby="h-work">
<div class="stop__media split">
<figure class="split__half">{a}<figcaption><b>{lh}</b><span>{ll}</span></figcaption></figure>
<figure class="split__half">{b}<figcaption><b>{rh}</b><span>{rl}</span></figcaption></figure>
</div>
<div class="stop__copy work"><h2 id="h-work" class="kicker">{k}</h2></div>
</section>""".format(
        a=half_img("door", "A doorman in a black suit at a venue entrance at night."),
        b=half_img("detail", "Three Swarm officers standing by a client&rsquo;s car in a parking garage."),
        k=W["kicker"], lh=W["left"][0], ll=W["left"][1], rh=W["right"][0], rl=W["right"][1])

    coverage = """<section class="stop stop--coverage" id="coverage" data-stop="3" aria-labelledby="h-coverage">
<div class="stop__media map">{svg}</div>
<div class="stop__copy cov">
<p class="kicker">{k}</p>
<h2 id="h-coverage">{h}</h2>
<p class="cov__line">{line}</p>
</div>
</section>""".format(svg=map_svg(), k=V["kicker"], h=V["h"], line=V["line"])

    def tile(title, sub, img):
        empty = title.startswith("PLACEHOLDER")
        pic = ('<img src="%s" alt="%s" loading="lazy" decoding="async">' % (img, title)) if img else \
              '<span class="tile__ph" aria-hidden="true"></span>'
        return ('<li class="tile%s"><div class="tile__pic">%s</div><p class="tile__t">%s</p><p class="tile__s">%s</p></li>'
                % (" is-empty" if empty else "", pic, "Photo coming" if empty else title, sub))
    tiles = "".join(tile(*t) for t in K["people"] + K["events"])
    crew = """<section class="stop stop--crew" id="crew" data-stop="4" aria-labelledby="h-crew">
<div class="stop__copy crew">
<div class="crew__head"><p class="kicker">{k}</p><h2 id="h-crew">{h}</h2><p class="crew__line">{line}</p></div>
<ul class="tiles">{tiles}</ul>
</div>
</section>""".format(k=K["kicker"], h=K["h"], line=K["line"], tiles=tiles)
    return home + services + work + coverage + crew


def contact_html():
    T = C.CONTACT
    return """<section class="contact" id="contact" aria-labelledby="h-contact">
<div class="contact__in">
<div class="contact__lead">
<h2 id="h-contact">{h}</h2>
<p class="contact__line">{line}</p>
<a class="contact__tel" href="tel:{tel}">{icon}<span>{phone}</span></a>
<p class="contact__note"><span class="dot" aria-hidden="true"></span>{note}</p>
<div class="social">
<a href="{ig}" rel="me noopener" target="_blank" aria-label="Swarm on Instagram">{i_ig}</a>
<a href="{tt}" rel="me noopener" target="_blank" aria-label="Swarm on TikTok">{i_tt}</a>
<a href="mailto:{email}" aria-label="Email {email}">{i_mail}</a>
</div>
</div>
<form class="form" data-form novalidate>
<label>Name<input name="name" autocomplete="name" required></label>
<label>Phone<input name="phone" type="tel" autocomplete="tel" required></label>
<label>What needs covering
<select name="service" id="q-service"><option>Event</option><option>Venue / bar</option><option>Close protection</option><option>Something else</option></select></label>
<label>Date<input name="date" type="date"></label>
<label class="form__wide">Anything we should know <em>(optional)</em><textarea name="note" rows="2"></textarea></label>
<label class="vh">Leave this empty<input name="company" tabindex="-1" autocomplete="off"></label>
<div class="form__acts" id="form-cta">
<button class="btn" type="submit"><span>{send}</span></button>
<a class="btn btn--ghost" href="tel:{tel}">{icon}<span>Call</span></a>
</div>
<p class="form__sent" role="status" hidden>Thanks — sent. If your mail app did not open, call {phone}.</p>
</form>
</div>
<footer class="foot">
<span>&copy; <span id="yr">2026</span> {name}</span>
<span>Ontario agency licence {lic} &middot; PSISA-licensed officers</span>
<nav aria-label="More"><a href="answers.html">Answers</a><a href="journal/index.html">Journal</a><a href="privacy.html">Privacy</a></nav>
</footer>
</section>""".format(h=T["h"], line=T["line"], note=T["note"], send=T["send"], tel=BIZ["phone_tel"],
                     phone=BIZ["phone_ui"], icon=PHONE_ICON, email=BIZ["email"], ig=BIZ["ig"],
                     tt=BIZ["tt"], i_ig=ICONS["ig"], i_tt=ICONS["tt"], i_mail=MAIL_ICON,
                     name=BIZ["name"], lic=BIZ["licence"])


NAV = [("#services", "Services"), ("#coverage", "Coverage"), ("#crew", "Crew"), ("#contact", "Contact")]

HTML = """<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#08090A">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{name}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{base}/assets/og/og-default.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="CA-ON">
<meta name="geo.placename" content="Toronto">
<link rel="icon" href="assets/icon/favicon.ico" sizes="any">
<link rel="icon" href="assets/icon/favicon-512.png" type="image/png" sizes="512x512">
<link rel="apple-touch-icon" href="assets/icon/favicon-180.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Saira:wdth,wght@100..125,500..800&family=Archivo:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/cine/site.css?v={cssv}">
<link rel="preload" as="image" href="{hero}" imagesrcset="{heroset}" imagesizes="100vw" fetchpriority="high">
<script type="application/ld+json">{org}</script>
{svc}
</head>
<body>
<a class="skip" href="#contact"><span>Skip to the quote form</span></a>
<header class="mast" id="mast">
<a class="mast__logo" href="#home" aria-label="{name} — top of page">
<img src="assets/logo/swarm-horizontal-gold.svg" alt="{name}" width="200" height="52"></a>
<nav class="mast__nav" aria-label="Primary">{nav}</nav>
<div class="mast__cta" id="mast-cta">
<a class="btn btn--ghost btn--sm mast__call" href="tel:{tel}" aria-label="Call {phone}">{icon}<span>{phone}</span></a>
<a class="btn btn--sm" href="#contact" data-quote><span>Get a quote</span></a>
</div>
<button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Menu"><span></span><span></span></button>
</header>
<div class="drawer" id="drawer" hidden>{drawer}
<a class="btn" href="#contact" data-quote><span>Get a quote</span></a>
<a class="btn btn--ghost" href="tel:{tel}">{icon}<span>{phone}</span></a>
</div>
<canvas id="stage" data-stage aria-hidden="true"></canvas>
<div class="shade" aria-hidden="true"></div>
<main id="main" class="track">
{stops}
</main>
{contact}
<script id="scene-data" type="application/json">{scene}</script>
<script src="assets/cine/site.js?v={jsv}" defer></script>
</body>
</html>
"""


def render():
    scene = json.loads(io.open(os.path.join(common.OUTDIR, "assets", "scene", "scene.json"),
                               encoding="utf-8").read())
    svc = "".join(
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service",'
        '"name":"%s","serviceType":"%s","url":"%s/#services","provider":{"@id":"%s/#org"},'
        '"areaServed":{"@type":"State","name":"Ontario"}}</script>' % (n, n, BIZ["base"], BIZ["base"])
        for n in ("Event security", "Nightclub and bar security", "Close protection"))
    base = common.MODE["preview_base"] if common.MODE["preview"] else BIZ["base"]
    crew = next(p for p in scene["plates"] if p["id"] == "crew")
    nav = "".join('<a href="%s">%s</a>' % n for n in NAV)
    return HTML.format(
        title="Swarm Protective Services — Security Company, Toronto &amp; GTA",
        desc="Licensed security in Toronto and the GTA: event security, bar and nightclub door "
             "staff and close protection. PSISA licensed, $5M insured. Get a quote.",
        canon=canonical("/"), base=base.rstrip("/"), name=BIZ["name"],
        robots="noindex,nofollow" if common.MODE["preview"] else "index,follow,max-image-preview:large",
        org=common.org_schema(), svc=svc, tel=BIZ["phone_tel"], phone=BIZ["phone_ui"], icon=PHONE_ICON,
        nav=nav, drawer=nav,
        hero=crew["sizes"][1]["src"], heroset=", ".join("%s %dw" % (s["src"], s["w"]) for s in crew["sizes"]),
        cssv=asset_version("assets/cine/site.css"), jsv=asset_version("assets/cine/site.js"),
        stops=stops_html(scene), contact=contact_html(),
        scene=json.dumps(scene, separators=(",", ":")))
