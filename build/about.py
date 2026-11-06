# -*- coding: utf-8 -*-
"""Meet us: who we are, in few words. Four screens, one scroll each.

    1  who we are     one photograph, the client's own line
    2  one statement  the client's words, lit word by word; the founder named
    3  on the job     working photographs, no captions
    4  the ask

The client asked that nothing promise the owners will be on a job in person
(everyone would ask for them), so the page names the founder and talks about
the team. Copy: build/cinema/content.py (STATEMENT).
"""
import os
import sys

from common import BIZ, cta_final, crumb_html, ihero, img, page

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cinema"))
import content as C                                              # noqa: E402

# (image, widths, alt): working photographs, no captions (the client asked)
ON_THE_JOB = [
    ("own-crew-venue", (600, 1000), "The Swarm crew at a venue entrance."),
    ("svc-event-security", (800, 1600), "A Swarm officer at the barrier in front of a concert crowd."),
    ("svc-close-protection", (800, 1600), "A Swarm close protection officer beside a client's car at a hotel entrance."),
]


def _gallery():
    return "".join(
        '<li style="--k:%d"><figure>%s</figure></li>'
        % (i, img(name, widths, "(max-width:900px) 30vw, 26vw", alt))
        for i, (name, widths, alt) in enumerate(ON_THE_JOB))


BODY = """{hero}

<section class="scr say" id="why" data-label="Our product">
<div class="wrap scr__in"><p class="say__t" data-words>{statement}</p>
<p class="say__by">Founded by {founder}, {role}.</p></div>
</section>

<section class="scr job" id="on-the-job" data-label="On the job" aria-labelledby="h-job">
<div class="wrap scr__in">
<h2 id="h-job">Real work, real crew</h2>
<ul class="job__pics">{gallery}</ul>
</div>
</section>
{cta}"""


ABOUT = page(
    path="/about.html", depth=0,
    title="Meet Swarm Protective Services | Who We Are, Toronto",
    desc="Meet Swarm Protective Services: Canadian owned and operated, founded by Nigel Wright. "
         "Trained, certified officers across Toronto, the GTA and Canada.",
    og="/assets/og/og-default.jpg",
    bodyattr=' class="screens"',
    body=BODY.format(
        hero=ihero(crumb_html([("Home", "index.html"), ("Meet us", "")]), "Who we are",
                   "Canadian owned. Canadian operated. Trusted to protect.",
                   img("stock-guard", (800, 1600), "100vw",
                       "A close protection officer in a black suit and dark glasses.", cls="at-face", loading="eager",
                       priority=True, ratio=1.5), label="Who we are"),
        statement=C.STATEMENT, founder=BIZ["founder"], role=BIZ["founder_role"],
        gallery=_gallery(), cta=cta_final(0)),
)

PAGES = {"about.html": ABOUT}
