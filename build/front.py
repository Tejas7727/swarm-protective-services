# -*- coding: utf-8 -*-
"""The home page — seven screens, one scroll each, every one complete on its own.

    1  welcome       the motto on the Toronto night, and three quiet ways in:
                     get a quote / meet the crew / see the services
    2  services      one scroll pushes the camera into his jacket and a gold
                     ring opens from it onto a night event; the six services
                     arrive over it (each card opens its page)
    3  who we are    "Canadian Owned. Canadian Operated. Trusted to Protect." on
                     warm stone, an on-the-job photograph, three standards;
                     "Meet the crew" for the visitor who came for the people
    4  how it works  three steps, the trust facts, "start with step one"
    5  coverage      the map and one line; every city lives on coverage.html
    6  questions     the six asked before every booking
    7  the quote     a three-step form beside the phone and the email

Who it serves: someone who wants a price now (Call and Get a quote are one tap
away on every screen; door one), someone from Instagram or TikTok who wants to
see who these people are (door two, screen 3), someone weighing the services
(door three, screen 2). Every screen ends on a quiet cue to the next one
(swarm.js), and the desktop rail names where you are.

The first screen's plates come from build/cinema/assets.py, the maps from
build/cinema/render.py. Every word is in build/cinema/content.py or services.py.
"""
import io
import json
import os

import common
from common import AREAS, BIZ, ICONS, faq_html, faq_schema, page
import content as C
import render as cinema
from services import SERVICES

ARROW = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
DOWN = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2">'
        '<path d="M12 5v14M6 13l6 6 6-6"/></svg>')

# (icon path, label) — the trust facts; every one of these is in the brand guide
BAND = [
    ('<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2.2"/>'
     '<path d="M5.8 16c.6-1.6 1.8-2.4 3.2-2.4s2.6.8 3.2 2.4M14 10h4M14 13h3"/>', "PSISA licensed"),
    ('<path d="M12 3 4 6v6c0 4.6 3.4 8.4 8 9 4.6-.6 8-4.4 8-9V6z"/><path d="m8.5 12 2.4 2.4 4.6-4.8"/>',
     "$5M insured"),
    ('<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.6 2.5L16 9.5"/>', "WSIB covered"),
    ('<rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M12 8v8M8 12h8"/>', "First aid on every shift"),
    ('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>', "Answered 24/7"),
]


SIZES = ["Just me or my family", "Under 50", "50 to 150", "150 to 500", "Over 500", "Not sure yet"]


def svg(paths, cls="ico"):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'aria-hidden="true">%s</svg>' % (cls, paths))


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
<p class="hx__line">{line}<span class="hx__dot" aria-hidden="true"> &middot; </span> <span class="hx__where">{where}</span></p>
<h1 id="h-home">{first},<br> <span class="hx__nw">{rest}</span></h1>
<p class="hx__lede">{lede}</p>
<nav class="doors" aria-label="Where to start">
<a class="doors__a doors__a--go" href="#contact"><b>Get a quote</b><span>Three short steps</span>{arrow}</a>
<a class="doors__a" href="about.html"><b>Meet the crew</b><span>Who turns up</span>{arrow}</a>
<a class="doors__a" href="#services"><b>Our services</b><span>Six ways we cover you</span>{down}</a>
</nav>
</div>
</section>""".format(up=cinema.UPRIGHT, mid=cinema.MIDDLE, mset=srcset(P["crew-m"]["sizes"]),
                     tset=srcset(P["crew-t"]["sizes"]), src=wide["sizes"][1]["src"], wset=srcset(wide["sizes"]),
                     w=wide["w"], h=wide["h"], plates=plates, line=C.HOME["line"],
                     where=C.HOME["where"].replace("&", "&amp;"), first=first, rest=rest, lede=C.HOME["lede"],
                     arrow=ARROW, down=DOWN)


def services():
    lines = {slug: line for slug, _, line in C.SERVICES["items"]}
    cards = "".join(
        '<li style="--k:{k}"><a class="scard" href="{slug}.html">'
        '<span class="scard__pic"><img src="assets/img/{art}-800.webp" alt="" width="800" height="547" '
        'loading="lazy" decoding="async"></span>'
        '<span class="scard__t"><b>{name}</b><span>{line}</span></span>{arrow}</a></li>'.format(
            k=i % 3 + i // 3, slug=s["slug"], art=s["art"], name=s["name"], line=lines.get(s["slug"], ""),
            arrow=ARROW)
        for i, s in enumerate(SERVICES))
    return """<section class="scr sx" id="services" data-label="Services" aria-labelledby="h-services">
<div class="wrap scr__in">
<div class="sx__head"><p class="eyebrow">{k}</p><h2 id="h-services">{h}</h2>
<p class="sx__lede">Pick one: what you get, how it runs, who it is for.</p></div>
<ul class="scards">{cards}</ul>
</div>
</section>""".format(k=C.SERVICES["kicker"], h=C.SERVICES["h"], cards=cards)


def people():
    P = C.PEOPLE
    items = "".join('<li style="--k:%d"><h3>%s</h3><p>%s</p></li>' % (i, t, d)
                    for i, (t, d) in enumerate(P["items"]))
    return """<section class="scr px" id="people" data-label="Who we are" aria-labelledby="h-people">
<div class="wrap scr__in px__in">
<figure class="px__pic px__pic--photo"><img src="assets/img/own-escort-caps-1000.webp"
 srcset="assets/img/own-escort-caps-600.webp 600w, assets/img/own-escort-caps-1000.webp 1000w"
 sizes="(max-width:899px) 100vw, 34vw" width="1000" height="1333" loading="lazy" decoding="async"
 alt="Two Swarm close protection officers escorting a client through a crowded event hall."></figure>
<div class="px__txt">
<p class="eyebrow">{k}</p>
<h2 id="h-people">{h}</h2>
<p class="px__lede">{line}</p>
<ul class="px__std px__std--3">{items}</ul>
<a class="go" href="about.html">Meet the crew {arrow}</a>
</div>
</div>
</section>""".format(k=P["kicker"], h=P["h"], line=P["line"], items=items, arrow=ARROW)


def how():
    steps = "".join('<li class="hw__step" style="--k:%d"><span class="hw__n">%02d</span><h3>%s</h3><p>%s</p></li>'
                    % (i, i + 1, t, d) for i, (t, d) in enumerate(C.STEPS["items"]))
    facts = "".join("<li>%s%s</li>" % (svg(p), t) for p, t in BAND)
    return """<section class="scr hw" id="how" data-label="How it works" aria-labelledby="h-how">
<div class="wrap scr__in">
<p class="eyebrow">How it works</p><h2 id="h-how">{h}</h2>
<ol class="hw__steps">{steps}</ol>
<a class="go" href="#contact">Start with step one {arrow}</a>
</div>
<ul class="facts" aria-label="Licences and insurance">{facts}</ul>
</section>""".format(h=C.STEPS["h"], steps=steps, facts=facts, arrow=ARROW)


def coverage():
    # the home page shows the map and one line; every city and the travel
    # detail live on coverage.html
    V = C.COVERAGE
    return """<section class="scr cx" id="coverage" data-label="Coverage" aria-labelledby="h-coverage" data-draw>
<div class="wrap scr__in cx__in">
<div class="cx__txt">
<p class="eyebrow">{k}</p><h2 id="h-coverage">{h}</h2>
<p class="lede">{line} {national}</p>
<a class="go" href="coverage.html">See every city we cover {arrow}</a>
</div>
<div class="cx__map">{map}</div>
</div>
</section>""".format(k=V["kicker"], h=V["h"], line=V["line"], national=V["national"], arrow=ARROW,
                     map=cinema.map_svg(narrow_aspect=0.95))


def faq():
    Q = C.FAQ
    return """<section class="scr qx" id="faq" data-label="Questions" aria-labelledby="h-faq">
<div class="wrap scr__in qx__in">
<div><p class="eyebrow">{k}</p><h2 id="h-faq">{h}</h2>
<p class="qx__more"><a class="go" href="answers.html">{more} {arrow}</a></p></div>
{faq}
</div>
</section>""".format(k=Q["kicker"], h=Q["h"], more=Q["more"], arrow=ARROW, faq=faq_html(Q["items"]))


def quote():
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
<p class="eyebrow">Get a quote</p>
<h2 id="h-contact">Tell us what you need</h2>
<p class="kx__lede">Three short steps. You get a written number and a named lead, usually the same day.</p>
<a class="kx__tel" href="tel:{tel}">{i_phone}<span>{phone}</span></a>
<p class="kx__note"><span class="dot" aria-hidden="true"></span>Answered 24/7 &middot; or email
<a href="mailto:{email}">{email}</a></p>
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
<legend>Where do we send the number?</legend>
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
<p>Your email app opened with the request filled in &mdash; press Send. Nothing opened?
Call <a href="tel:{tel}">{phone}</a> or email <a href="mailto:{email}">{email}</a>.</p>
</div>
</form>
</div>
</section>""".format(tel=BIZ["phone_tel"], phone=BIZ["phone_ui"], email=BIZ["email"], i_phone=ICONS["phone"],
                     opts=opts, cities=cities, sizes=sizes)


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
    body = "\n".join([film, people(), how(), coverage(), faq(), quote()])
    return page("/", "Swarm Protective Services — Security Company, Toronto &amp; GTA",
                "Licensed security in Toronto and the GTA: close protection, event and venue security, "
                "party bus and limousine details, and monitoring. PSISA licensed, $5M insured. Get a quote.",
                body, head=head, schema=svc + faq_schema(C.FAQ["items"]), bodyattr=' class="is-home screens"')
