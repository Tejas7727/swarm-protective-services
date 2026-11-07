# -*- coding: utf-8 -*-
"""Coverage: where we work, as one camera move in three screens, then the list.

    1-3  the map film  one scroll per beat, the film pinned behind and scrubbed
                       by the scroll: close on Toronto ("Based in Toronto"), out
                       to the GTA as routes run to 17 cities ("Across the GTA"),
                       out to Canada as arcs draw coast to coast ("Anywhere in Canada")
    4    every city    the 18, grouped by direction from downtown, over the film's GTA frame

The film is rendered in Remotion with MapLibre on OpenFreeMap tiles
(ai-studio/remotion/src/projects/SwarmCoverage.tsx): 72 frames for wide screens
(assets/cine/cov-w) and 72 for tall ones (assets/cine/cov-t). Without the
script, or with reduced motion, the last frame stands as a poster and all three
sentences show in reading order.
"""
import os
import sys

from common import page

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cinema"))
import content as C                                              # noqa: E402

REGIONS = [
    ("Toronto", ["Toronto", "Etobicoke", "North York", "Scarborough"]),
    ("West", ["Mississauga", "Brampton", "Oakville", "Milton", "Burlington", "Hamilton"]),
    ("North", ["Vaughan", "Richmond Hill", "Markham", "Newmarket"]),
    ("East", ["Pickering", "Ajax", "Whitby", "Oshawa"]),
]
FRAMES = 72


def body():
    regions = "".join(
        '<div class="reg" style="--k:%d"><h3>%s</h3><ul>%s</ul></div>'
        % (i, r, "".join("<li>%s</li>" % c for c in cities)) for i, (r, cities) in enumerate(REGIONS))
    return """<div class="cov cov--poster" data-cov>
<div class="cov__stage" aria-hidden="true">
<picture class="cov__poster">
<source media="(max-aspect-ratio:1/1)" srcset="assets/cine/cov-t/f{last:02d}.webp">
<img src="assets/cine/cov-w/f{last:02d}.webp" alt="" width="1440" height="810" decoding="async">
</picture>
<canvas class="cov__film" data-n="{n}" data-wide="assets/cine/cov-w/" data-tall="assets/cine/cov-t/"></canvas>
<p class="cov__credit">Map &copy; <a href="https://openfreemap.org" rel="noopener">OpenFreeMap</a>,
<a href="https://www.openstreetmap.org/copyright" rel="noopener">OpenStreetMap</a> contributors</p>
</div>
<section class="scr cov__beat" id="top" data-label="Toronto" aria-labelledby="h-cov">
<div class="wrap scr__in">
<h1 id="h-cov"><span class="pz__sub">Based in</span> <span class="pz__big" data-fit=".96" data-fit-wide=".6">Toronto</span></h1><p class="lede">Dispatch answers from here, 24 hours a day.</p></div>
</section>
<section class="scr cov__beat" id="gta" data-label="The GTA">
<div class="wrap scr__in"><h2><span class="pz__sub">Across</span> <span class="pz__big" data-fit=".96" data-fit-wide=".6">the GTA</span></h2><p class="lede">{line}</p></div>
</section>
<section class="scr cov__beat" id="canada" data-label="Canada">
<div class="wrap scr__in"><h2><span class="pz__sub">Anywhere in</span> <span class="pz__big" data-fit=".96" data-fit-wide=".6">Canada</span></h2><p class="lede">{national}</p></div>
</section>
</div>

<section class="scr regions" id="cities" data-label="Every city" aria-labelledby="h-reg">
<picture class="regions__map" aria-hidden="true">
<source media="(max-aspect-ratio:1/1)" srcset="assets/cine/cov-t/f40.webp">
<img src="assets/cine/cov-w/f40.webp" alt="" width="1440" height="810" loading="lazy" decoding="async">
</picture>
<div class="wrap scr__in">
<h2 id="h-reg">Eighteen cities, one dispatch</h2>
<div class="regions__grid">{regions}</div>
</div>
</section>""".format(n=FRAMES, last=FRAMES - 1, line=C.COVERAGE["line"], national=C.COVERAGE["national"],
                     regions=regions)


PAGES = {"coverage.html": page(
    path="/coverage.html", depth=0,
    title="Where We Work | Security in Toronto, the GTA &amp; Across Canada | Swarm",
    desc="Swarm Protective Services covers Toronto and 17 GTA cities (Mississauga, Brampton, Vaughan, "
         "Markham, Oakville, Hamilton and more) and travels with clients anywhere in Canada.",
    og="/assets/og/og-default.jpg",
    bodyattr=' class="screens"',
    body=body())}
