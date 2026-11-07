# -*- coding: utf-8 -*-
"""How we work: the client's three steps (deck slide 6) and the licences behind
them. Two screens: the opening, then the steps on a gold line that draws itself
as the screen arrives (swarm.js writes --draw), each step lighting as the line
reaches it."""
import os
import sys

from common import crumb_html, ihero, img, page
import plans

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cinema"))
import content as C                                              # noqa: E402

# (icon path, label): the trust facts; every one of these is in the brand guide
BAND = [
    ('<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2.2"/>'
     '<path d="M5.8 16c.6-1.6 1.8-2.4 3.2-2.4s2.6.8 3.2 2.4M14 10h4M14 13h3"/>', "Licensed officers"),
    ('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>', "Reachable 24/7"),
    ('<path d="M12 3 4 6v6c0 4.6 3.4 8.4 8 9 4.6-.6 8-4.4 8-9V6z"/><path d="m8.5 12 2.4 2.4 4.6-4.8"/>',
     "Canadian owned"),
]


def _facts():
    return "".join('<li><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                   'stroke-width="1.7" aria-hidden="true">%s</svg>%s</li>' % (p, t) for p, t in BAND)


def _steps():
    return "".join('<li class="hw__step" style="--k:%d;--at:%.2f"><span class="hw__n">%02d</span><h3>%s</h3><p>%s</p></li>'
                   % (i, i / 3.0, i + 1, t, d) for i, (t, d) in enumerate(C.STEPS["items"]))


BODY = """{hero}

<section class="scr hw tl tl--split" id="steps" data-label="Three steps" aria-labelledby="h-how" data-draw>
<div class="wrap scr__in tl__in">
<div class="tl__text">
<h2 id="h-how" class="sr-only">{h}</h2>
<div class="tl__run">
<svg class="tl__line" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
<line class="tl__base" x1="0" y1="0" x2="100" y2="100"/><line class="tl__gold" x1="0" y1="0" x2="100" y2="100" pathLength="1"/></svg>
<ol class="hw__steps tl__steps">{steps}</ol>
</div>
<ul class="facts" aria-label="About us">{facts}</ul>
</div>
<figure class="plan plan--build">{plan}</figure>
</div>
</section>"""

PROCESS = page(
    path="/process.html", depth=0,
    title="How We Work | Swarm Protective Services, Toronto",
    desc="How a Swarm Protective Services booking runs: an initial consultation, a customized service "
         "plan, and professional execution with documented results.",
    bodyattr=' class="screens"',
    body=BODY.format(
        hero=ihero(crumb_html([("Home", "index.html"), ("How we work", "")]), "How we work",
                   "From your first call to the end of the job, you deal with one team and one point of contact.",
                   img("stock-earpiece", (800, 1600), "100vw",
                       "A close protection officer in a black suit speaking into an earpiece.", cls="at-face", loading="eager",
                       priority=True, ratio=2 / 3.0), label="How we work", poster=True),
        h=C.STEPS["h"], steps=_steps(), facts=_facts(), plan=plans.process()),
)

PAGES = {"process.html": PROCESS}
