# -*- coding: utf-8 -*-
"""Meet us — who we are and how we work. Six screens, one scroll each.

    1  the crew        their own photograph
    2  one statement   the client's words, lit word by word as the screen arrives
    3  leadership      the founder named, an on-the-job photograph
    4  the standard    four cards on warm stone (the client's words)
    5  on the job      working photographs, no captions
    6  the ask

For the visitor who came from Instagram or TikTok to see who these people are,
and then wants a price. The client asked that nothing promise the owners will be
on a job in person (everyone would ask for them), so the page names the founder
and talks about the team. Copy: build/cinema/content.py (ELITE, STATEMENT).
"""
import os
import sys

from common import BIZ, cta_final, crumb_html, ihero, img, page

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cinema"))
import content as C                                              # noqa: E402

ARROW = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')

# (image, widths, alt) — working photographs, no captions (the client asked)
ON_THE_JOB = [
    ("own-crew-venue", (600, 1000), "The Swarm crew at a venue entrance."),
    ("svc-event-security", (800, 1600), "A Swarm officer at the barrier in front of a concert crowd."),
    ("svc-close-protection", (800, 1600), "A Swarm close protection officer beside a client's car at a hotel entrance."),
]


def _standard():
    return "".join('<li style="--k:%d"><span class="gx__k">%02d</span><h3>%s</h3><p>%s</p></li>'
                   % (i, i + 1, t, b) for i, (t, b) in enumerate(C.ELITE["items"]))


def _gallery():
    return "".join(
        '<li style="--k:%d"><figure>%s</figure></li>'
        % (i, img(name, widths, "(max-width:900px) 30vw, 26vw", alt))
        for i, (name, widths, alt) in enumerate(ON_THE_JOB))


BODY = """{hero}

<section class="scr say" id="why" data-label="Our product">
<div class="wrap scr__in"><p class="say__t" data-words>{statement}</p>
<p class="say__after">{statement_2}</p></div>
</section>

<section class="scr own" id="leadership" data-label="Leadership" aria-labelledby="h-own">
<div class="wrap scr__in own__in">
<figure class="own__photo"><img src="assets/img/own-escort-suits-1000.webp"
 srcset="assets/img/own-escort-suits-600.webp 600w, assets/img/own-escort-suits-1000.webp 1000w"
 sizes="(max-width:899px) 100vw, 40vw" width="1000" height="1333" loading="lazy" decoding="async"
 alt="Two Swarm close protection officers escorting a client through an event hall."></figure>
<div class="own__txt">
<p class="eyebrow">Leadership</p>
<h2 id="h-own">Founded by {founder}</h2>
<p class="lede">{founder}, {role}, built Swarm Protective Services on one standard of protection:
trained personnel, one point of contact, and documented results.</p>
<a class="go" href="index.html#contact">Talk to us about your detail {arrow}</a>
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
<p class="eyebrow">On the job</p><h2 id="h-job">Real work, real crew</h2>
<ul class="job__pics">{gallery}</ul>
</div>
</section>
{cta}"""


ABOUT = page(
    path="/about.html", depth=0,
    title="Meet Swarm Protective Services — Who We Are, Toronto",
    desc="Meet Swarm Protective Services: Canadian owned and operated, founded by Nigel Wright. "
         "Trained, certified officers across Toronto, the GTA and Canada.",
    og="/assets/og/og-default.jpg",
    bodyattr=' class="screens"',
    body=BODY.format(
        hero=ihero(crumb_html([("Home", "index.html"), ("Meet us", "")]), "Meet us", "Who we are.",
                   "Licensed, trained personnel who plan ahead, communicate first, and document every detail.",
                   img("crew-hero", (640, 900, 1200, 1600), "100vw",
                       "Five Swarm officers in black under a lit venue sign.", loading="eager",
                       priority=True, ratio=16 / 9.0), label="The crew"),
        statement=C.STATEMENT, statement_2=C.STATEMENT_2, founder=BIZ["founder"],
        role=BIZ["founder_role"], arrow=ARROW,
        kicker=C.ELITE["kicker"], standard_h=C.ELITE["h"], standard=_standard(),
        gallery=_gallery(), cta=cta_final(0)),
)

PAGES = {"about.html": ABOUT}
