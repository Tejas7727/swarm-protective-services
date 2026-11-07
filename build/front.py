# -*- coding: utf-8 -*-
"""The home page: five screens, one scroll each, every one complete on its own.

    1  welcome     the motto on the Toronto night; get a quote / meet the crew /
                   our services
    2  services    one scroll pushes the camera into his jacket and a gold ring
                   opens from it onto a night event; six photographs arrive over
                   it, two by three, each one opening its page
    3  know us     three ways deeper: who we are, how we work, where we work
    4  questions   the six asked before every booking
    5  the quote   a three-step form beside the phone and the email

Every "Get a quote" on the site opens quote.html directly; this last screen is
the same form, for whoever scrolls all the way down.

The first screen's plates come from build/cinema/assets.py, the map from
build/cinema/render.py. Every word is in build/cinema/content.py or services.py.
"""
import io
import json
import os

import common
from common import AREAS, BIZ, ICONS, faq_html, faq_schema, img, page
import content as C
import render as cinema
from services import SERVICES

SIZES = ["Just me or my family", "Under 50", "50 to 150", "150 to 500", "Over 500", "Not sure yet"]


def srcset(sizes):
    return ", ".join("%s %dw" % (s["src"], s["w"]) for s in sizes)


def welcome(scene):
    P = {p["id"]: p for p in scene["plates"]}
    first, rest = C.HOME["motto"].split(", ", 1)
    rest = rest.replace(C.HOME["gold"], "<em>%s</em>" % C.HOME["gold"], 1)
    wide = P["crew"]
    # for the camera: each plate's size, the centre of its portal (the dark jacket
    # under the emblem) and the object-position the styles give it
    pos = {"crew-m": (0.55, 1.0), "crew-t": (1.0, 0.5), "crew": (0.6, 0.45)}
    plates = json.dumps({k: [P[k]["w"], P[k]["h"],
                             round(P[k]["portal"]["aper"][0] + P[k]["portal"]["aper"][2] / 2, 4),
                             round(P[k]["portal"]["aper"][1] + P[k]["portal"]["aper"][3] / 2, 4)] + list(pos[k])
                         for k in pos}, separators=(",", ":"))
    return """<div class="film__stage">
<div class="film__hero"><picture>
<source media="{up}" srcset="{mset}" sizes="75vh">
<source media="{mid}" srcset="{tset}" sizes="100vw">
<img src="{src}" srcset="{wset}" sizes="100vw" width="{w}" height="{h}" fetchpriority="high" decoding="async"
 data-plates='{plates}'
 alt="A Swarm officer seen from behind, SWARM on his jacket, looking out over the Toronto skyline and the CN Tower at night.">
</picture></div>
<div class="film__portal" aria-hidden="true"><img src="assets/img/svc-event-security-1600.webp"
 srcset="assets/img/svc-event-security-800.webp 800w, assets/img/svc-event-security-1600.webp 1600w" sizes="100vw"
 alt="" width="1600" height="1095" decoding="async"></div>
<i class="film__ring" aria-hidden="true"></i>
</div>
<section class="scr hx" id="top" data-label="Welcome" aria-labelledby="h-home">
<div class="hx__copy">
<h1 id="h-home">{first},<br> <span class="hx__nw">{rest}</span></h1>
<nav class="doors" aria-label="Where to start">
<a class="btn doors__q" href="quote.html"><span>Get a quote</span></a>
<a class="btn btn--glass" href="about.html"><span>Meet the crew</span></a>
<a class="btn btn--glass" href="#services"><span>Our services</span></a>
</nav>
</div>
</section>""".format(up=cinema.UPRIGHT, mid=cinema.MIDDLE, mset=srcset(P["crew-m"]["sizes"]),
                     tset=srcset(P["crew-t"]["sizes"]), src=wide["sizes"][1]["src"], wset=srcset(wide["sizes"]),
                     w=wide["w"], h=wide["h"], plates=plates, line=C.HOME["line"],
                     where=C.HOME["where"].replace("&", "&amp;"), first=first, rest=rest, lede=C.HOME["lede"])


def services():
    lines = {slug: line for slug, _, line in C.SERVICES["items"]}
    tiles = "".join(
        '<li style="--k:{k}"><a class="tile" href="{slug}.html">'
        '<img src="assets/img/{art}-800.webp" srcset="assets/img/{art}-800.webp 800w, '
        'assets/img/{art}-1600.webp 1600w" sizes="(max-width:899px) 50vw, 34vw" alt="" width="800" height="547" '
        'loading="lazy" decoding="async">'
        '<span class="tile__t"><b>{name}</b></span></a></li>'.format(
            k=i // 2, slug=s["slug"], art=s["art"], name=s["name"], line=lines.get(s["slug"], ""))
        for i, s in enumerate(SERVICES))
    return """<section class="scr sx" id="services" data-label="Services" aria-labelledby="h-services">
<div class="wrap scr__in sx__in">
<h2 id="h-services">Services</h2>
<ul class="tiles">{tiles}</ul>
</div>
</section>""".format(tiles=tiles)


def more():
    """Three ways deeper, each a whole panel: the people, the process, the map."""
    panel = ('<li style="--k:{k}"><a class="mx__p" href="{href}">{art}'
             '<span class="mx__t"><b>{t}</b></span></a></li>')
    panels = "".join([
        panel.format(k=0, href="about.html", t="Who we are", d="The people and the standard they keep",
                     art=img("stock-guard", (800, 1600), "(max-width:899px) 100vw, 40vw",
                             "A close protection officer in a black suit and dark glasses.", cls="at-face", ratio=1.5)),
        panel.format(k=1, href="process.html", t="How we work", d="From the first call to the written report",
                     art=img("stock-suv", (800, 1600), "(max-width:899px) 100vw, 40vw",
                             "A black SUV waiting in a parking lot at night.", ratio=2 / 3.0)),
        panel.format(k=2, href="coverage.html", t="Where we work", d="Toronto, the GTA and anywhere in Canada",
                     art='<span class="mx__map" aria-hidden="true">%s</span>' % cinema.map_svg(narrow_aspect=0.8).replace(
                         '<svg class="gm"', '<svg class="gm" preserveAspectRatio="xMidYMid slice"', 1)),
    ])
    return """<section class="scr mx" id="more" data-label="Know us" aria-labelledby="h-more" data-draw>
<div class="wrap scr__in mx__in">
<h2 id="h-more">Know who you hire</h2>
<ul class="mx__list">{panels}</ul>
</div>
</section>""".format(panels=panels)


def faq():
    Q = C.FAQ
    return """<section class="scr qx" id="faq" data-label="Questions" aria-labelledby="h-faq">
<figure class="qx__bg">{pic}</figure>
<div class="wrap scr__in qx__in">
<div class="qx__side"><h2 id="h-faq">{h}</h2></div>
{faq}
</div>
</section>""".format(h=Q["h"], faq=faq_html(Q["items"]),
           pic=img("own-escort-suits", (600, 1000), "(max-width:899px) 100vw, 32vw",
                   "Swarm officers in black suits escorting guests through a gala.", ratio=0.75))


def quote(tag="h2"):
    """The quote form. The home page ends on it; quote.html is nothing else (and
    there it carries the page's h1)."""
    opts = "".join(
        '<label class="qf__opt"><input type="radio" name="service" value="{n}" data-slug="{s}"{req}>'
        '<span>{n}</span></label>'.format(n=s["name"], s=s["slug"], req=" required" if i == 0 else "")
        for i, s in enumerate(SERVICES))
    opts += ('<label class="qf__opt"><input type="radio" name="service" value="Something else" data-slug="other">'
             '<span>Something else</span></label>')
    cities = "".join("<option>%s</option>" % a for a in AREAS) + "<option>Elsewhere in Canada</option>"
    sizes = "".join("<option>%s</option>" % s for s in SIZES)
    return """<section class="scr kx" id="contact" data-label="Get a quote" aria-labelledby="h-contact">
<div class="wrap scr__in kx__in">
<div class="kx__side">
<{tag} id="h-contact">Tell us what you need</{tag}>
<p class="kx__lede">Three short steps. Answered the same day.</p>
<a class="kx__tel" href="tel:{tel}">{i_phone}<span>{phone}</span></a>
<p class="kx__note"><span class="kx__live">Answered 24/7</span> or email <a href="mailto:{email}">{email}</a></p>
<figure class="crew crew--pair" aria-hidden="true"><img class="crew__still" src="assets/cine/pair-poster.webp" alt="" width="720" height="880" loading="lazy" decoding="async"><video class="crew__vid" muted playsinline preload="none" width="720" height="880" data-play data-alpha><source src="assets/cine/pair.webm" type='video/webm; codecs="vp09.00.10.08"'></video></figure>
</div>
<form class="qf" data-quote data-to="{email}" aria-labelledby="h-contact">
<p class="qf__prog" aria-live="polite"><span data-prog>Three short steps</span><i aria-hidden="true"><b></b></i></p>
<fieldset class="qf__step" data-step="1">
<legend>What do you need?</legend>
<div class="qf__opts">{opts}</div>
</fieldset>
<fieldset class="qf__step" data-step="2">
<legend>When and where?</legend>
<div class="qf__grid">
<div class="f"><label for="q-date">Date</label><input id="q-date" name="date" type="date"></div>
<div class="f"><label for="q-city">Where</label><select id="q-city" name="city" required>
<option value="">Choose a city</option>{cities}</select><span class="err">Choose the closest city.</span></div>
<div class="f f--full"><label for="q-size">How many people</label><select id="q-size" name="people">
<option value="">Choose one</option>{sizes}</select></div>
<div class="f f--full"><label for="q-notes">Anything we should know <em>(optional)</em></label>
<textarea id="q-notes" name="notes" rows="2" placeholder="Venue, hours, alcohol served, who needs cover"></textarea></div>
</div>
</fieldset>
<fieldset class="qf__step" data-step="3">
<legend>Where do we send the plan?</legend>
<div class="qf__grid">
<div class="f f--full"><label for="q-name">Your name</label>
<input id="q-name" name="name" autocomplete="name" required><span class="err">We need a name to reply to.</span></div>
<div class="f f--full"><label for="q-reach">Phone or email</label>
<input id="q-reach" name="reach" autocomplete="email" inputmode="email" required>
<span class="err">A phone number or an email, whichever you prefer.</span></div>
</div>
</fieldset>
<div class="hp" aria-hidden="true"><label for="q-company">Company</label><input id="q-company" name="company" tabindex="-1" autocomplete="off"></div>
<div class="qf__nav">
<button class="btn btn--ghost" type="button" data-back><span>Back</span></button>
<button class="btn" type="button" data-next><span>Next</span></button>
<button class="btn" type="submit" data-send><span>Send my request</span></button>
</div>
<p class="form__note">We use this to answer you, nothing else. <a href="privacy.html">Privacy</a></p>
<p class="qf__err" data-senderr hidden>That did not go through. Call {phone} or email {email}.</p>
<div class="form__ok" role="status">
<h3>Your email is ready to send</h3>
<p>Your email app opened with the request filled in. Press Send. Nothing opened?
Call <a href="tel:{tel}">{phone}</a> or email <a href="mailto:{email}">{email}</a>.</p>
</div>
</form>
</div>
</section>""".format(tel=BIZ["phone_tel"], phone=BIZ["phone_ui"], email=BIZ["email"], i_phone=ICONS["phone"],
                     opts=opts, cities=cities, sizes=sizes, tag=tag)


def render():
    scene = json.loads(io.open(os.path.join(common.OUTDIR, "assets", "scene", "scene.json"),
                               encoding="utf-8").read())
    P = {p["id"]: p for p in scene["plates"]}
    # the first screen's photograph, for whichever shape this screen is
    head = "".join(
        '<link rel="preload" as="image" href="%s" imagesrcset="%s" imagesizes="%s" media="%s" fetchpriority="high">'
        % (P[i]["sizes"][1]["src"], srcset(P[i]["sizes"]), sz, m)
        for i, sz, m in (("crew-m", "75vh", cinema.UPRIGHT), ("crew-t", "100vw", cinema.MIDDLE),
                         ("crew", "100vw", cinema.WIDE)))
    svc = "".join(
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service",'
        '"name":"%s","serviceType":"%s","url":"%s/%s","provider":{"@id":"%s/#org"},'
        '"areaServed":[{"@type":"State","name":"Ontario"},{"@type":"Country","name":"Canada"}]}</script>'
        % (s["name"], s["name"], BIZ["base"], s["slug"], BIZ["base"]) for s in SERVICES)
    film = '<div class="film" data-film>%s\n%s\n</div>' % (welcome(scene), services())
    body = "\n".join([film, more(), faq(), quote()])
    return page("/", "Swarm Protective Services | Security Company, Toronto &amp; GTA",
                "Licensed security in Toronto and the GTA: close protection, event and venue security, "
                "party bus and limousine details, and monitoring. PSISA licensed, $5M insured. Get a quote.",
                body, head=head, schema=svc + faq_schema(C.FAQ["items"]), bodyattr=' class="is-home screens"')


def quote_page():
    return page("/quote.html", "Get a Quote | Swarm Protective Services, Toronto",
                "Request a security quote from Swarm Protective Services: tell us the date, the place and "
                "the headcount, and get a written plan with one point of contact, usually the same day.",
                quote("h1"), bodyattr=' class="screens is-quote"')
