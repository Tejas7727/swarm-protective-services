# -*- coding: utf-8 -*-
"""Meet us — the people who turn up. Six screens, one scroll each.

    1  the crew        their own photograph
    2  one sentence    lit word by word as the screen arrives
    3  the owners      cut out of their photograph in Swarm vests; the founder named
    4  the standard    four cards on warm stone
    5  on the job      their real photographs
    6  the ask

For the visitor who came from Instagram or TikTok to see who these people are,
and then wants a price. No invented names, faces or numbers: crew names and
photographs go in as each officer agrees to be shown (content.py CREW).
"""
import os
import sys

from common import BIZ, cta_final, crumb_html, ihero, img, page

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cinema"))
import content as C                                              # noqa: E402

ARROW = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')

STATEMENT = ("The product is a night where nothing happened. That takes people who plan for "
             "the worst, talk before they touch, and behave the same whether or not anyone "
             "is watching.")

# (image, caption) — the client's own photographs, nothing staged
ON_THE_JOB = [
    ("own-owners-car", "The owners, beside a client&rsquo;s car."),
    ("own-crew-venue", "The crew at a venue."),
    ("own-owners-wide", "The owners, on the job."),
]


def _standard():
    return "".join('<li style="--k:%d"><span class="gx__k">%02d</span><h3>%s</h3><p>%s</p></li>'
                   % (i, i + 1, t, b) for i, (t, b) in enumerate(C.ELITE["items"]))


def _gallery():
    return "".join(
        '<li style="--k:%d"><figure>%s<figcaption>%s</figcaption></figure></li>'
        % (i, img(name, (600, 1000), "(max-width:900px) 30vw, 26vw", cap, ratio=3 / 4.0), cap)
        for i, (name, cap) in enumerate(ON_THE_JOB))


BODY = """{hero}

<section class="scr say" id="why" data-label="Why we do it">
<div class="wrap scr__in"><p class="say__t" data-words>{statement}</p></div>
</section>

<section class="scr own" id="owners" data-label="The owners" aria-labelledby="h-own">
<div class="wrap scr__in own__in">
<div class="own__stage">
<img class="own__em" src="assets/logo/emblem-216.webp" alt="" width="216" height="238" aria-hidden="true">
<img class="own__cut" src="assets/img/own-pair-cut-1000.webp"
 srcset="assets/img/own-pair-cut-600.webp 600w, assets/img/own-pair-cut-1000.webp 1000w"
 sizes="(max-width:899px) 60vw, 34vw" width="1000" height="1535" loading="lazy" decoding="async"
 alt="The two owners of Swarm Protective Services in black tactical vests with the Swarm emblem.">
</div>
<div class="own__txt">
<p class="eyebrow">The owners</p>
<h2 id="h-own">First on the floor</h2>
<p class="lede">Swarm was founded by {founder}, {role}. The owners still work details
themselves, and they are the first names on every standing order we write.</p>
<p class="sub">The person who quotes your night is the person who answers for it.</p>
<a class="go" href="index.html#contact">Talk to the owners about your night {arrow}</a>
</div>
</div>
</section>

<section class="scr std7" id="standard" data-label="The standard" aria-labelledby="h-std">
<div class="wrap scr__in">
<p class="eyebrow">{kicker}</p><h2 id="h-std">{standard_h}</h2>
<ol class="std7__grid">{standard}</ol>
</div>
</section>

<section class="scr job" id="on-the-job" data-label="On the job" aria-labelledby="h-job">
<div class="wrap scr__in">
<p class="eyebrow">On the job</p><h2 id="h-job">Real nights, real crew</h2>
<ul class="job__pics">{gallery}</ul>
<p class="job__note">Crew names and photographs go in as each officer agrees to be shown.</p>
</div>
</section>
{cta}"""


ABOUT = page(
    path="/about.html", depth=0,
    title="Meet Swarm Protective Services — The Crew, Toronto",
    desc="Meet Swarm Protective Services: founded by Nigel Wright, run by licensed officers who still "
         "work details themselves, across Toronto and the GTA.",
    og="/assets/og/og-default.jpg",
    bodyattr=' class="screens"',
    body=BODY.format(
        hero=ihero(crumb_html([("Home", "index.html"), ("Meet us", "")]), "Meet us", "Who turns up.",
                   "Licensed officers who plan the night, talk first, and write it up before they leave.",
                   img("crew-hero", (640, 900, 1200, 1600), "100vw",
                       "Five Swarm officers in black under a lit venue sign.", loading="eager",
                       priority=True, ratio=16 / 9.0), label="The crew"),
        statement=STATEMENT, founder=BIZ["founder"], role=BIZ["founder_role"], arrow=ARROW,
        kicker=C.ELITE["kicker"], standard_h=C.ELITE["h"], standard=_standard(),
        gallery=_gallery(), cta=cta_final(0)),
)

PAGES = {"about.html": ABOUT}
