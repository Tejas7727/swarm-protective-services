# -*- coding: utf-8 -*-
"""Render the home page: one night, six stops, one camera.

The copy lives here, not in a template, because the word budgets in
`brand-copy` are checked against it (see COPY.md for the scorecards).
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import common                                                       # noqa: E402
from common import AREAS, BIZ, ICONS, asset_version, canonical, faq_schema, plain  # noqa: E402
from home import FAQS                                               # noqa: E402

# --------------------------------------------------------------------------
# the film
# --------------------------------------------------------------------------
STOPS = [
    {
        "id": "call", "plate": "street", "time": "", "label": "On call",
        "eyebrow": 'Toronto <b id="clock">--:--</b> &middot; a team is on call',
        "h": "Big on purpose.|Calm by training.",
        "line": "Licensed door staff, event security and close protection across the GTA.",
        "ask": True, "acts": "hero",
    },
    {
        "id": "venues", "plate": "door", "time": "22:15", "label": "The door",
        "eyebrow": "Bars, nightclubs and lounges",
        "h": "Most trouble|never gets in.",
        "line": "IDs checked by hand. Headcount kept all night.",
        "alt": {
            "venue": "IDs checked by hand. Headcount kept all night.",
            "event": "Every name against your list. Gatecrashers turned around.",
            "person": "Your way in is walked before you arrive.",
        },
    },
    {
        "id": "events", "plate": "floor", "time": "00:40", "label": "The floor",
        "eyebrow": "Events, weddings and corporate",
        "h": "Nothing worth|filming.",
        "line": "De-escalation first, refreshed twice a year, not once at hire.",
        "alt": {
            "venue": "Two officers, two angles, and a quiet word first.",
            "event": "Guests never meet the problem that was already handled.",
            "person": "Someone watches the room so you do not have to.",
        },
    },
    {
        "id": "protection", "plate": "exit", "time": "02:10", "label": "The exit",
        "eyebrow": "Close protection",
        "h": "The exit is planned|before the entrance.",
        "line": "Close protection from the first door to your own.",
        "alt": {
            "venue": "Your staff walked to their cars at close.",
            "event": "The people the night is about leave quietly.",
            "person": "Close protection from the first door to your own.",
        },
    },
    {
        "id": "report", "plate": "dawn", "time": "06:00", "label": "The report",
        "eyebrow": "Written reporting",
        "h": "You slept.|We wrote it down.",
        "line": "Written before the crew leaves your building.",
        "report": True,
    },
    {
        "id": "book", "plate": "dawn", "time": "", "label": "Book the night",
        "eyebrow": "Dispatch answered 24 hours",
        "h": "Forget about it.|We won't.",
        "line": "Tell us the date and the place. You get a number the same day.",
        "acts": "book",
    },
]

REPORT = [("Refused at the door", "4"), ("Settled without contact", "1"),
          ("Injuries", "0"), ("Police called", "0")]


def words(text):
    """Each word rides up out of a mask; '|' is a line the copywriter chose."""
    out = []
    for n, part in enumerate(text.split("|")):
        if n:
            out.append("<br>")
        out.append("".join('<span class="word"><i>%s</i></span> ' % w
                           for w in part.strip().split(" ")))
    return "".join(out).strip()


def stop_html(i, s, scene):
    plate = next(p for p in scene["plates"] if p["id"] == s["plate"])
    # url() inside a custom property resolves against the stylesheet, not the
    # page, so this path is written relative to assets/cine/push.css.
    bg = "../" + plate.get("flat", plate["sizes"][1]["src"]).split("assets/", 1)[1]
    tag = "h1" if i == 0 else "h2"
    alt = ""
    if s.get("alt"):
        alt = "".join(' data-%s="%s"' % (k, v) for k, v in sorted(s["alt"].items()))
    out = ['<section class="stop" id="%s" data-time="%s" data-label="%s" style="--plate:url(%s)">'
           % (s["id"], s["time"] or "&mdash;&mdash;", s["label"], bg)]
    out.append('<div class="copy">')
    out.append('<p class="eyebrow">%s</p>' % s["eyebrow"])
    out.append("<%s>%s</%s>" % (tag, words(s["h"]), tag))
    out.append('<p class="line"%s>%s</p>' % (alt, s["line"]))
    if s.get("ask"):
        out.append('<div class="ask"><span class="ask__q">What needs covering?</span>'
                   '<button class="chip" type="button" data-mode="venue" aria-pressed="false">A venue</button>'
                   '<button class="chip" type="button" data-mode="event" aria-pressed="false">An event</button>'
                   '<button class="chip" type="button" data-mode="person" aria-pressed="false">A person</button>'
                   '</div><p class="reply" id="reply" role="status"></p>')
    if s.get("acts") == "hero":
        out.append('<div class="acts"><a class="btn" href="#quote" data-quote><span>Get a quote</span></a>'
                   '<a class="btn btn--ghost" href="tel:%s"><span>Call dispatch</span></a></div>' % BIZ["phone_tel"])
    if s.get("acts") == "book":
        out.append('<div class="acts"><a class="btn" href="#quote" data-quote><span>Request a quote</span></a>'
                   '<a class="btn btn--ghost" href="tel:%s"><span>%s</span></a></div>'
                   % (BIZ["phone_tel"], BIZ["phone_ui"]))
        out.append('<div class="social"><a href="%s" rel="me noopener" target="_blank" aria-label="Swarm on Instagram">%s</a>'
                   '<a href="%s" rel="me noopener" target="_blank" aria-label="Swarm on TikTok">%s</a>'
                   '<a href="mailto:%s" aria-label="Email dispatch">%s</a></div>'
                   % (BIZ["ig"], ICONS["ig"], BIZ["tt"], ICONS["tt"], BIZ["email"],
                      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18v14H3V5Zm2.4 2 6.6 5 6.6-5H5.4Zm13.6 2.3-7 5.3-7-5.3V17h14V9.3Z"/></svg>'))
    out.append("</div>")
    if s.get("report"):
        rows = "".join("<dt>%s</dt><dd>%s</dd>" % (k, v) for k, v in REPORT)
        out.append('<aside class="report"><h3>Shift report &mdash; sample</h3><dl>%s</dl>'
                   '<p class="report__foot">Filed 06:04 &middot; signed by the lead</p></aside>' % rows)
    out.append("</section>")
    return "".join(out)


def rail_html():
    return "".join('<button class="tick" type="button" aria-label="%s"></button>' % s["label"]
                   for s in STOPS)


def faq_html():
    return "".join('<details><summary>%s</summary><div class="a">%s</div></details>' % (q, a)
                   for q, a in FAQS)


def after_html():
    svc = "".join('<li><a href="#%s">%s</a></li>' % (a, t) for a, t in [
        ("venues", "Venue and door security"), ("events", "Event security"),
        ("protection", "Close protection"), ("report", "Written reporting")])
    comp = "".join('<li><a href="%s">%s</a></li>' % (u, t) for u, t in [
        ("journal/index.html", "Journal"), ("#quote", "Request a quote"),
        ("privacy.html", "Privacy")])
    return """<section class="after" id="answers">
<div class="wrap">
<h2>Answers</h2>
<p class="sub">What people ask before they book</p>
<div class="faq">{faq}</div>
<div class="cols">
<div><h4>What we do</h4><ul>{svc}</ul></div>
<div><h4>Company</h4><ul>{comp}</ul></div>
<div><h4>Dispatch</h4><ul>
<li><a href="tel:{tel}">{phone}</a></li>
<li><a href="mailto:{email}">{email}</a></li>
<li>Answered 24 hours, every day</li>
<li>Ontario agency licence {lic}</li>
</ul></div>
<div id="coverage"><h4>Where we work</h4><ul><li>{areas}</li></ul></div>
</div>
<div class="foot__bar">
<span>&copy; <span id="yr">2026</span> {name}</span>
<span>PSISA-licensed &middot; $5M commercial general liability &middot; WSIB covered</span>
</div>
</div>
</section>""".format(faq=faq_html(), svc=svc, comp=comp, tel=BIZ["phone_tel"],
                     phone=BIZ["phone_ui"], email=BIZ["email"], lic=BIZ["licence"],
                     areas=", ".join(AREAS) + ".", name=BIZ["name"])


def dialog_html():
    return """<dialog id="quote" aria-labelledby="q-title">
<form class="q" data-form novalidate>
<h2 id="q-title">Tell us the night.</h2>
<p>Date, place and headcount is enough to start. You get a written number and a named lead,
usually the same day.</p>
<div class="q__row">
<label>Name<input name="name" autocomplete="name" required></label>
<label>Phone<input name="phone" type="tel" autocomplete="tel" required></label>
</div>
<div class="q__row">
<label>Email<input name="email" type="email" autocomplete="email" required></label>
<label>What needs covering
<select name="service" id="q-service">
<option>Venue / bar</option><option>Event</option><option>Close protection</option><option>Something else</option>
</select></label>
</div>
<div class="q__row">
<label>Date<input name="date" type="date"></label>
<label>Place<input name="place" placeholder="Venue or area"></label>
</div>
<label>Anything we should know<textarea name="note" rows="3"></textarea></label>
<label class="vh">Leave this empty<input name="company" tabindex="-1" autocomplete="off"></label>
<div class="q__acts">
<button class="btn" type="submit"><span>Send it</span></button>
<a class="btn btn--ghost" href="tel:{tel}"><span>Call {phone}</span></a>
<button class="q__close" type="button" data-close>Close</button>
</div>
<p class="q__sent" hidden>Sent. If your mail app did not open, call {phone} &mdash; answered 24 hours.</p>
</form>
</dialog>""".format(tel=BIZ["phone_tel"], phone=BIZ["phone_ui"])


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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Saira:wdth,wght@100..125,600..800&family=Archivo:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/cine/push.css?v={cssv}">
<link rel="preload" as="image" href="{hero}" fetchpriority="high">
{schema}
</head>
<body>
<a class="skip" href="#answers"><span>Skip to the answers</span></a>
<canvas id="stage" aria-hidden="true"></canvas>
<div class="grade" aria-hidden="true"></div>
<div class="grain" aria-hidden="true"></div>
<header class="mast">
<a class="mast__logo" href="#call" aria-label="{name} — top">
<img src="assets/logo/swarm-horizontal-gold.svg" alt="{name}" width="200" height="52" fetchpriority="high"></a>
<span class="mast__sp"></span>
<a class="btn btn--ghost btn--sm" href="tel:{tel}"><span>{phone}</span></a>
<a class="btn btn--sm" href="#quote" data-quote><span>Get a quote</span></a>
</header>
<main class="film" id="main">
{stops}
</main>
<div class="hud" id="hud">
<span class="hud__dot" aria-hidden="true"></span>
<b data-time>&mdash;&mdash;</b><span data-label>On call</span>
<span class="hud__sp"></span>
<nav class="rail" aria-label="Chapters">{rail}</nav>
</div>
{after}
{dialog}
<script id="scene-data" type="application/json">{scene}</script>
<script src="assets/cine/push.js?v={jsv}" defer></script>
</body>
</html>
"""


def render():
    scene = json.loads(io.open(os.path.join(common.OUTDIR, "assets", "scene", "scene.json"),
                               encoding="utf-8").read())
    service_schema = "".join(
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service",'
        '"name":"%s","serviceType":"%s","url":"%s/#%s","provider":{"@id":"%s/#org"},'
        '"areaServed":{"@type":"State","name":"Ontario"}}</script>' % (n, n, BIZ["base"], a, BIZ["base"])
        for n, a in [("Nightclub and bar security", "venues"), ("Event security", "events"),
                     ("Close protection and executive protection", "protection")])
    schema = ('<script type="application/ld+json">%s</script>' % common.org_schema()) \
        + service_schema + faq_schema([(q, plain(a)) for q, a in FAQS])
    base = common.MODE["preview_base"] if common.MODE["preview"] else BIZ["base"]
    hero = next(p for p in scene["plates"] if p["id"] == "street")["sizes"][0]["src"]
    return HTML.format(
        title="Security Company Toronto — Door Staff &amp; Close Protection | Swarm",
        desc="Licensed security company in Toronto and the GTA — bar and nightclub door staff, "
             "event security and close protection. Big on purpose, calm by training. "
             "Dispatch answered 24 hours.",
        canon=canonical("/"), base=base.rstrip("/"), name=BIZ["name"],
        robots="noindex,nofollow" if common.MODE["preview"] else "index,follow,max-image-preview:large",
        schema=schema, hero=hero, tel=BIZ["phone_tel"], phone=BIZ["phone_ui"],
        cssv=asset_version("assets/cine/push.css"), jsv=asset_version("assets/cine/push.js"),
        stops="\n".join(stop_html(i, s, scene) for i, s in enumerate(STOPS)),
        rail=rail_html(), after=after_html(), dialog=dialog_html(),
        scene=json.dumps(scene, separators=(",", ":")))
