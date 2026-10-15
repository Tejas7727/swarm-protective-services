# -*- coding: utf-8 -*-
"""Coverage — where we work, as one camera move in three screens, then a list.

    1-3  the map      one scroll per beat, the map pinned behind:
                      close on Toronto ("Based in Toronto"), out to the GTA as
                      routes run to 17 cities ("Across the GTA"), out to Canada
                      as the travel arcs draw ("Anywhere in Canada")
    4    every city   the 18, grouped by direction from downtown
    5    travel       how it works outside the GTA
    6    the ask

Both maps are drawings from Natural Earth (build/cinema/geo_extract.py).
Without the script, or with reduced motion, the map and all three sentences
show in reading order.
"""
import os
import sys

from common import cta_final, page

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cinema"))
import content as C                                              # noqa: E402
import render as cinema                                          # noqa: E402

REGIONS = [
    ("Toronto", ["Toronto", "Etobicoke", "North York", "Scarborough"]),
    ("West", ["Mississauga", "Brampton", "Oakville", "Milton", "Burlington", "Hamilton"]),
    ("North", ["Vaughan", "Richmond Hill", "Markham", "Newmarket"]),
    ("East", ["Pickering", "Ajax", "Whitby", "Oshawa"]),
]

TRAVEL = [
    ("We travel with you", "Anywhere in Canada, and the same crew stays with you for the trip."),
    ("Licensed where it counts", "Outside Ontario we work with licensed partners where the province "
                                 "requires it."),
    ("One lead, one report", "The same named lead and the same written report, wherever the night is."),
]


def body():
    regions = "".join(
        '<div class="reg" style="--k:%d"><h3>%s</h3><ul>%s</ul></div>'
        % (i, r, "".join("<li>%s</li>" % c for c in cities)) for i, (r, cities) in enumerate(REGIONS))
    travel = "".join('<li class="hw__step" style="--k:%d"><span class="hw__n">%02d</span><h3>%s</h3><p>%s</p></li>'
                     % (i, i + 1, t, d) for i, (t, d) in enumerate(TRAVEL))
    return """<div class="cov" data-cov>
<div class="cov__stage" aria-hidden="true">
<div class="cov__gta">{gta}</div>
<div class="cov__can">{can}</div>
</div>
<section class="scr cov__beat" id="top" data-label="Toronto" aria-labelledby="h-cov">
<div class="wrap scr__in"><p class="eyebrow">Coverage</p>
<h1 id="h-cov">Based in Toronto.</h1><p class="lede">Dispatch answers from here, 24 hours a day.</p></div>
</section>
<section class="scr cov__beat" id="gta" data-label="The GTA">
<div class="wrap scr__in"><h2>Across the GTA.</h2><p class="lede">{line}</p></div>
</section>
<section class="scr cov__beat" id="canada" data-label="Canada">
<div class="wrap scr__in"><h2>Anywhere in Canada.</h2><p class="lede">{national}</p></div>
</section>
</div>

<section class="scr regions" id="cities" data-label="Every city" aria-labelledby="h-reg">
<div class="wrap scr__in">
<p class="eyebrow">Every city we cover</p><h2 id="h-reg">Eighteen cities, one dispatch</h2>
<div class="regions__grid">{regions}</div>
</div>
</section>

<section class="scr hw travel" id="travel" data-label="Travel" aria-labelledby="h-travel">
<div class="wrap scr__in">
<p class="eyebrow">Outside the GTA</p><h2 id="h-travel">When the night is somewhere else</h2>
<ol class="hw__steps">{travel}</ol>
</div>
</section>
{cta}""".format(gta=cinema.map_svg(narrow_aspect=0.6), can=cinema.canada_svg(),
                line=C.COVERAGE["line"], national=C.COVERAGE["national"],
                regions=regions, travel=travel,
                cta=cta_final(0, heading="Tell us where.",
                              lede="City, date and headcount is enough to start. We reply the same day."))


PAGES = {"coverage.html": page(
    path="/coverage.html", depth=0,
    title="Where We Work — Security in Toronto, the GTA &amp; Across Canada | Swarm",
    desc="Swarm Protective Services covers Toronto and 17 GTA cities — Mississauga, Brampton, Vaughan, "
         "Markham, Oakville, Hamilton and more — and travels with clients anywhere in Canada.",
    og="/assets/og/og-default.jpg",
    bodyattr=' class="screens"',
    body=body())}
