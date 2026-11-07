# -*- coding: utf-8 -*-
"""Meet us: who we are, in few words. Three screens, one scroll each.

    1  who we are     one photograph, the client's own line
    2  one statement  the client's words, lit word by word, over the crew line-up
                      (a transparent Remotion film, SwarmLineup, that plays as the screen arrives)
    3  on the job     a feed: one photograph at a time, the next one showing, a
                      caption under each; swipe, drag or tap the next one

The client asked that nothing promise the owners will be on a job in person
(everyone would ask for them), so the page talks about the team, not the owners.
Copy: build/cinema/content.py (STATEMENT). The film: ai-studio/remotion
(SwarmCrew), made from the crew's own photograph.
"""
import os
import sys

from common import crumb_html, ihero, img, page

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cinema"))
import content as C                                              # noqa: E402

# (image, widths, place, caption, alt): working photographs, captioned like posts
FEED = [
    ("own-crew-venue", (600, 1000), "Toronto", "First in, last out. Every door, every night.",
     "The Swarm crew at a venue entrance."),
    ("lot-tall", (560, 1000), "Toronto", "Car's warm. Route's planned. Let's go.",
     "Three Swarm officers beside a car in a parking lot at night."),
    ("svc-event-security", (800, 1600), "GTA", "Best seat in the house. Facing the other way, on purpose.",
     "A security officer at the barrier in front of a concert crowd."),
    ("svc-close-protection", (800, 1600), "Toronto", "The quiet part of the job: arrivals.",
     "Two Swarm close protection officers in black beside a client's car at a hotel entrance."),
    ("svc-venue-security", (800, 1600), "Toronto", "Dress code: enforced. Smile: optional.",
     "Five Swarm officers in black at a venue entrance at night."),
    ("svc-limousine-service", (800, 1600), "GTA", "Door to door. Literally.",
     "A black stretch limousine waiting under a hotel canopy at night."),
]


def _feed():
    return "".join(
        '<li class="gram" style="--k:{k}"><p class="gram__by"><img src="assets/logo/emblem-108.webp" alt="" '
        'width="108" height="119" loading="lazy"><b>Swarm</b><span>{place}</span></p>'
        '<figure class="gram__pic">{pic}</figure>'
        '<p class="gram__cap"><b>Swarm</b> {cap}</p></li>'.format(
            k=i, place=place, cap=cap, pic=img(name, widths, "(max-width:899px) 78vw, 36vw", alt))
        for i, (name, widths, place, cap, alt) in enumerate(FEED))


BODY = """{hero}

<section class="scr say say--crew" id="why" data-label="Our product">
<div class="wrap scr__in say__in">
<p class="say__t">{statement}</p>
<p class="say__l">{line}</p>
</div>
<figure class="crew crew--lineup" aria-hidden="true"><img class="crew__still" src="assets/cine/lineup-poster.webp" alt="" width="1312" height="800" loading="lazy" decoding="async"><video class="crew__vid" muted playsinline preload="none" width="1312" height="800" data-play data-alpha><source src="assets/cine/lineup.webm" type='video/webm; codecs="vp09.00.10.08"'></video></figure>
</section>

<section class="scr job" id="on-the-job" data-label="On the job" aria-labelledby="h-job">
<div class="wrap scr__in job__in">
<h2 id="h-job">Real work, real crew</h2>
<div class="feed" tabindex="0" role="region" aria-label="Photographs from the job. Swipe for more.">
<ol class="feed__track">{feed}</ol>
</div>
</div>
</section>"""


ABOUT = page(
    path="/about.html", depth=0,
    title="Meet Swarm Protective Services | Who We Are, Toronto",
    desc="Meet Swarm Protective Services: Canadian owned and operated. Trained, certified officers "
         "across Toronto, the GTA and Canada.",
    og="/assets/og/og-default.jpg",
    bodyattr=' class="screens"',
    body=BODY.format(
        hero=ihero(crumb_html([("Home", "index.html"), ("Meet us", "")]), "Who we are",
                   "Canadian owned. Canadian operated. Trusted to protect.",
                   img("stock-guard", (800, 1600), "100vw",
                       "A close protection officer in a black suit and dark glasses.", cls="at-face", loading="eager",
                       priority=True, ratio=1.5), label="Who we are"),
        statement="".join('<span class="say__ln" data-words>%s</span>' % ln for ln in C.STATEMENT.split(". ", 1)).replace("happened</span>", "happened.</span>"),
        line=C.STATEMENT_LINE, feed=_feed()),
)

PAGES = {"about.html": ABOUT}
