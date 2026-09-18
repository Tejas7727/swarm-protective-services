# -*- coding: utf-8 -*-
"""Render the home page.

Order is the argument, not the art direction: what this is → who it is for →
proof → what you get → how it works → one night of it → where → who → answers →
ask. The film is one section in the middle, not the whole page.

All copy lives in `content.py`. All scene geometry lives in `assets.py`.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import common                                                       # noqa: E402
from common import AREAS, BIZ, ICONS, asset_version, canonical, faq_schema, plain  # noqa: E402
from home import FAQS                                               # noqa: E402
import content as C                                                 # noqa: E402

MAIL = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18v14H3V5Zm2.4 2 6.6 5 '
        '6.6-5H5.4Zm13.6 2.3-7 5.3-7-5.3V17h14V9.3Z"/></svg>')


def quote_btn(cls="btn", label=None):
    return ('<a class="%s" href="#quote" data-quote><span>%s</span></a>'
            % (cls, label or C.HERO["cta"]))


def call_btn(cls="btn btn--ghost", label=None):
    return ('<a class="%s" href="tel:%s"><span>%s</span></a>'
            % (cls, BIZ["phone_tel"], label or BIZ["phone_ui"]))


def words(text):
    """Each word rides up out of a mask when its block arrives."""
    out = []
    for n, part in enumerate(text.split("|")):
        if n:
            out.append("<br>")
        out.append("".join('<span class="word"><i>%s</i></span> ' % w
                           for w in part.strip().split(" ")))
    return "".join(out).strip()


# --------------------------------------------------------------------------
def hero_html(scene):
    plate = next(p for p in scene["plates"] if p["id"] == "street")
    layer = plate["layers"][0]
    srcset = ", ".join("%s %dw" % (s["src"], s["w"]) for s in plate["sizes"])
    cut = ", ".join("%s %dw" % (s["src"], s["w"]) for s in layer["sizes"])
    proof = "".join("<li>%s</li>" % p for p in C.PROOF)
    return """<section class="hero" id="top">
<div class="hero__bg" aria-hidden="true">
<img src="{bg}" srcset="{bgset}" sizes="100vw" alt="" width="{bw}" height="{bh}"
 fetchpriority="high" decoding="async" data-par="0.05">
<img class="hero__cut" src="{cut}" srcset="{cutset}" sizes="70vw" alt=""
 width="{cw}" height="{ch}" decoding="async" data-par="0.16">
</div>
<div class="hero__in">
<img class="hero__logo" src="assets/logo/swarm-horizontal-gold.svg"
 alt="{name}" width="440" height="114" fetchpriority="high">
<h1>{h}</h1>
<p class="lede">{sub}</p>
<div class="acts">{q}{c}</div>
<p class="micro"><span class="dot" aria-hidden="true"></span>{note}</p>
</div>
<ul class="proof" aria-label="Credentials">{proof}</ul>
</section>""".format(
        bg=plate["sizes"][1]["src"], bgset=srcset,
        bw=plate["sizes"][0]["w"], bh=plate["sizes"][0]["h"],
        cut=layer["sizes"][1]["src"], cutset=cut,
        cw=layer["sizes"][0]["w"], ch=layer["sizes"][0]["h"],
        name=BIZ["name"], h=C.HERO["h"], sub=C.HERO["sub"],
        q=quote_btn(), c=call_btn(label="Call dispatch"),
        note=C.HERO["note"], proof=proof)


def services_html():
    cards = []
    for s in C.SERVICES:
        pts = "".join("<li>%s</li>" % p for p in s["points"])
        cards.append("""<article class="card reveal" id="{id}">
<p class="kicker">{k}</p>
<h3>{h}</h3>
<p class="card__line">{line}</p>
<ul class="ticks">{pts}</ul>
<a class="link" href="#quote" data-quote><span>Get a quote for this</span></a>
</article>""".format(id=s["id"], k=s["kicker"], h=s["h"], line=s["line"], pts=pts))
    return """<section class="band" id="services">
<div class="wrap">
<p class="kicker reveal">What we provide</p>
<h2 class="reveal">Three jobs, done the same way every time.</h2>
<div class="cards">{cards}</div>
<p class="band__foot reveal">Not sure which one you need? Send the date and the place and we
will tell you what it takes. {q}</p>
</div>
</section>""".format(cards="".join(cards), q=quote_btn("link", "Ask us"))


def stance_html():
    pts = "".join('<li class="reveal"><h4>%s</h4><p>%s</p></li>' % (h, p)
                  for h, p in C.STANCE["points"])
    return """<section class="band band--alt" id="how">
<div class="wrap">
<p class="kicker reveal">{k}</p>
<h2 class="reveal">{h}</h2>
<p class="lede reveal">{line}</p>
<ul class="grid3">{pts}</ul>
</div>
</section>""".format(k=C.STANCE["kicker"], h=C.STANCE["h"], line=C.STANCE["line"], pts=pts)


def steps_html():
    items = "".join('<li class="reveal"><span class="step__n">%02d</span><h4>%s</h4><p>%s</p></li>'
                    % (i + 1, h, p) for i, (h, p) in enumerate(C.STEPS))
    return """<section class="band" id="process">
<div class="wrap">
<p class="kicker reveal">How booking works</p>
<h2 class="reveal">Three steps, and two of them are ours.</h2>
<ol class="steps">{items}</ol>
<div class="acts reveal">{q}{c}</div>
</div>
</section>""".format(items=items, q=quote_btn(), c=call_btn())


def film_html(scene):
    beats = []
    for b in C.BEATS:
        plate = next(p for p in scene["plates"] if p["id"] == b["plate"])
        beats.append("""<div class="beat" id="{id}" data-plate="{p}" data-time="{t}" data-label="{l}"
 style="--plate:url({bg})">
<div class="beat__in">
<p class="kicker">{t} &middot; {l}</p>
<h3>{h}</h3>
<p class="beat__line">{line}</p>
</div>
</div>""".format(id=b["id"], p=b["plate"], t=b["time"], l=b["label"], h=words(b["h"]), line=b["line"],
                 bg="../" + plate.get("flat", plate["sizes"][1]["src"]).split("assets/", 1)[1]))
    rail = "".join('<button class="tick" type="button" aria-label="%s %s"></button>'
                   % (b["time"], b["label"]) for b in C.BEATS)
    spacers = "".join('<div class="film__step"></div>' for _ in C.BEATS)
    return """<section class="film" id="night" aria-label="One night">
<div class="wrap film__head">
<p class="kicker reveal">{k}</p>
<h2 class="reveal">{h}</h2>
<p class="lede reveal">{line}</p>
</div>
<div class="film__stage">
<canvas id="stage" data-stage aria-hidden="true"></canvas>
<div class="film__grade" aria-hidden="true"></div>
<div class="beats">{beats}</div>
<div class="hud" id="hud">
<span class="hud__dot" aria-hidden="true"></span>
<b data-time>22:15</b><span data-label>The door</span>
<span class="hud__sp"></span>
<nav class="rail" aria-label="Moments">{rail}</nav>
</div>
</div>
<div class="film__scroll" aria-hidden="true">{spacers}</div>
</section>""".format(k=C.FILM_INTRO["kicker"], h=C.FILM_INTRO["h"], line=C.FILM_INTRO["line"],
                     beats="".join(beats), rail=rail, spacers=spacers)


def coverage_html():
    items = "".join("<li>%s</li>" % a for a in AREAS)
    return """<section class="band band--alt" id="coverage">
<div class="wrap">
<p class="kicker reveal">Where we work</p>
<h2 class="reveal">Toronto and 17 more.</h2>
<ul class="areas reveal">{items}</ul>
<p class="band__foot reveal">{note}</p>
</div>
</section>""".format(items=items, note=C.COVERAGE_NOTE)


def people_html():
    preview = common.MODE["preview"]
    live_t = [t for t in C.TESTIMONIALS if not t[0].startswith("PLACEHOLDER")]
    live_p = [p for p in C.TEAM if not p[0].startswith("PLACEHOLDER")]
    show_t = live_t or (C.TESTIMONIALS if preview else [])
    show_p = live_p or (C.TEAM if preview else [])
    out = ['<section class="band" id="people"><div class="wrap">']
    out.append('<p class="kicker reveal">%s</p><h2 class="reveal">%s</h2>'
               '<p class="lede reveal">%s</p>'
               % (C.TESTIMONIAL_INTRO["kicker"], C.TESTIMONIAL_INTRO["h"],
                  C.TESTIMONIAL_INTRO["line"]))
    if show_t:
        cards = "".join(
            '<figure class="quote reveal%s"><blockquote>%s</blockquote>'
            '<figcaption><b>%s</b><span>%s</span></figcaption></figure>'
            % (" is-placeholder" if q.startswith("PLACEHOLDER") else "", q, n, r)
            for q, n, r in show_t)
        out.append('<div class="quotes">%s</div>' % cards)
    out.append('<div class="crew"><p class="kicker reveal">%s</p><h3 class="reveal">%s</h3>'
               '<p class="lede reveal">%s</p>'
               % (C.TEAM_INTRO["kicker"], C.TEAM_INTRO["h"], C.TEAM_INTRO["line"]))
    if show_p:
        cards = "".join(
            '<li class="reveal%s"><div class="crew__ph" aria-hidden="true"></div>'
            '<h4>%s</h4><p class="crew__role">%s</p><p>%s</p></li>'
            % (" is-placeholder" if n.startswith("PLACEHOLDER") else "", n, role, line)
            for n, role, line, _img in show_p)
        out.append('<ul class="crewlist">%s</ul>' % cards)
    out.append("</div></div></section>")
    return "".join(out)


def faq_html():
    return "".join('<details class="reveal"><summary>%s</summary><div class="a">%s</div></details>'
                   % (q, a) for q, a in FAQS)


def close_html():
    return """<section class="band band--close" id="book">
<div class="wrap">
<p class="kicker reveal">{k}</p>
<h2 class="reveal">{h}</h2>
<p class="lede reveal">{line}</p>
<div class="acts reveal">{q}{c}</div>
<div class="social reveal">
<a href="{ig}" rel="me noopener" target="_blank" aria-label="Swarm on Instagram">{i_ig}</a>
<a href="{tt}" rel="me noopener" target="_blank" aria-label="Swarm on TikTok">{i_tt}</a>
<a href="mailto:{email}" aria-label="Email dispatch">{i_mail}</a>
</div>
</div>
</section>""".format(k=C.CLOSE["kicker"], h=C.CLOSE["h"], line=C.CLOSE["line"],
                     q=quote_btn(), c=call_btn(), ig=BIZ["ig"], tt=BIZ["tt"],
                     email=BIZ["email"], i_ig=ICONS["ig"], i_tt=ICONS["tt"], i_mail=MAIL)


def answers_html():
    svc = "".join('<li><a href="#%s">%s</a></li>' % (s["id"], s["kicker"]) for s in C.SERVICES)
    comp = "".join('<li><a href="%s">%s</a></li>' % (u, t) for u, t in [
        ("#night", "One night"), ("#coverage", "Where we work"),
        ("journal/index.html", "Journal"), ("privacy.html", "Privacy")])
    return """<section class="band band--alt" id="answers">
<div class="wrap">
<p class="kicker reveal">Answers</p>
<h2 class="reveal">What people ask before they book.</h2>
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
</div>
<div class="foot__bar">
<span>&copy; <span id="yr">2026</span> {name}</span>
<span>PSISA-licensed &middot; $5M commercial general liability &middot; WSIB covered</span>
</div>
</div>
</section>""".format(faq=faq_html(), svc=svc, comp=comp, tel=BIZ["phone_tel"],
                     phone=BIZ["phone_ui"], email=BIZ["email"], lic=BIZ["licence"],
                     name=BIZ["name"])


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
<link rel="stylesheet" href="assets/cine/site.css?v={cssv}">
<link rel="preload" as="image" href="{hero}" imagesrcset="{heroset}" imagesizes="100vw" fetchpriority="high">
{schema}
</head>
<body>
<a class="skip" href="#services"><span>Skip to services</span></a>
<header class="mast" id="mast">
<a class="mast__logo" href="#top" aria-label="{name} — top">
<img src="assets/logo/swarm-horizontal-gold.svg" alt="{name}" width="200" height="52"></a>
<nav class="mast__nav" aria-label="Primary">
<a href="#services">Services</a><a href="#how">How we work</a><a href="#night">One night</a>
<a href="#coverage">Coverage</a><a href="#answers">Answers</a>
</nav>
<div class="mast__cta">
<a class="btn btn--ghost btn--sm mast__tel" href="tel:{tel}"><span>{phone}</span></a>
<a class="btn btn--sm" href="#quote" data-quote><span>Request a quote</span></a>
<button class="burger" type="button" aria-expanded="false" aria-controls="drawer"
 aria-label="Open menu"><span></span><span></span><span></span></button>
</div>
</header>
<div class="drawer" id="drawer" hidden>
<a href="#services">Services</a><a href="#how">How we work</a><a href="#night">One night</a>
<a href="#coverage">Coverage</a><a href="#people">The crew</a><a href="#answers">Answers</a>
<a class="btn" href="#quote" data-quote><span>Request a quote</span></a>
<a class="btn btn--ghost" href="tel:{tel}"><span>Call {phone}</span></a>
</div>
<main id="main">
{hero_s}
{services}
{stance}
{steps}
{film}
{coverage}
{people}
{answers}
{close}
</main>
<div class="bar">
<a class="bar__call" href="tel:{tel}"><span>Call dispatch</span></a>
<a class="bar__quote" href="#quote" data-quote><span>Request a quote</span></a>
</div>
{dialog}
<script id="scene-data" type="application/json">{scene}</script>
<script src="assets/cine/site.js?v={jsv}" defer></script>
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
    street = next(p for p in scene["plates"] if p["id"] == "street")
    return HTML.format(
        title="Security Company Toronto — Door Staff, Events, Close Protection",
        desc="Licensed security company in Toronto and the GTA. Bar and nightclub door staff, "
             "event security and close protection. De-escalation first, dispatch answered 24 hours.",
        canon=canonical("/"), base=base.rstrip("/"), name=BIZ["name"],
        robots="noindex,nofollow" if common.MODE["preview"] else "index,follow,max-image-preview:large",
        schema=schema, tel=BIZ["phone_tel"], phone=BIZ["phone_ui"],
        hero=street["sizes"][1]["src"],
        heroset=", ".join("%s %dw" % (s["src"], s["w"]) for s in street["sizes"]),
        cssv=asset_version("assets/cine/site.css"), jsv=asset_version("assets/cine/site.js"),
        hero_s=hero_html(scene), services=services_html(), stance=stance_html(),
        steps=steps_html(), film=film_html(scene), coverage=coverage_html(),
        people=people_html(), answers=answers_html(), close=close_html(),
        dialog=dialog_html(), scene=json.dumps(scene, separators=(",", ":")))
