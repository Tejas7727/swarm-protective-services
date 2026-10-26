# -*- coding: utf-8 -*-
"""The six service pages — what the home page's one-liners actually mean.

The home page sells; these pages answer. Each one says what you get, how a
booking runs, who it is for, and the two or three questions people ask about
that service specifically. No prices: every job is quoted.

Edit the copy here. `build/service_art.py` exports the photographs.
"""
from common import BIZ, cta_final, crumb_html, faq_html, faq_schema, ihero, img, page, plain

# the quote form on the home page, with this service already picked
QUOTE = "index.html?service=%s#contact"

# slug, name, art, title, h1, lede, includes, steps, for_whom, faq
SERVICES = [
    {
        "slug": "close-protection",
        "name": "Close protection",
        "art": "svc-close-protection",
        "alt": "Two Swarm close protection officers in black beside a client's car at a hotel entrance.",
        "title": "Close Protection & Bodyguards — Toronto &amp; GTA",
        "desc": "Licensed close protection in Toronto and the GTA: executives, artists, visiting "
                "clients and families. Advance work, discreet officers, secure transport, same-day quotes.",
        "h1": "Close protection.",
        "lede": "A licensed officer at your side, or a team around you. Suited, briefed, and boring "
                "to look at — which is the point.",
        "includes": [
            ("A named lead", "One person owns your detail and is reachable for the whole booking."),
            ("Advance on the location", "We walk the venue, the route and the exits before you arrive."),
            ("Arrivals and departures", "The two minutes that matter are planned, not improvised."),
            ("Secure transport", "Chauffeured vehicle with an officer, or we work with your driver."),
            ("Discretion in writing", "A confidentiality agreement covers the detail, the address and the names."),
            ("A written report", "What happened, when, and what we did — before the detail ends."),
        ],
        "steps": [
            ("Tell us the shape of it", "Dates, cities, who is being covered and how visible you want us."),
            ("We plan it", "Advance, routes, timings, vehicle, and the number of officers it actually needs."),
            ("We run it", "One lead, one line of contact, and a report at the end of each day."),
        ],
        "for_whom": ["Executives and founders", "Artists, DJs and touring crews",
                     "Visiting clients and delegations", "Families and private residences",
                     "Anyone with a situation that changed this week"],
        "faq": [
            ("Are your bodyguards armed?",
             "No. Private security in Ontario is not permitted to carry firearms. Our work is advance "
             "planning, presence and de-escalation — and that is what the licence covers."),
            ("Can you travel with us?",
             "Yes. We travel with clients anywhere in Canada. Outside Ontario we work with licensed "
             "partners where the province requires it."),
            ("How discreet is it?",
             "As discreet as you want. Officers can be in suits and read as staff, or be visible on "
             "purpose when visibility is the deterrent."),
        ],
    },
    {
        "slug": "event-security",
        "name": "Event security",
        "art": "svc-event-security",
        "alt": "A security officer at the barrier in front of a concert crowd.",
        "title": "Event Security Toronto — Concerts, Weddings, Galas",
        "desc": "Licensed event security across Toronto and the GTA: concerts, weddings, galas, "
                "festivals and private parties. Door, barrier, floor and close-out, quoted per event.",
        "h1": "Event security.",
        "lede": "From a 60-person wedding to a room of two thousand: the right number of licensed "
                "officers, in the right places, from load-in to lock-up.",
        "includes": [
            ("A plan before the day", "Headcount, entry points, bar positions, close-out and the what-if list."),
            ("Door and ID checks", "Guest lists, wristbands, ID — handled politely and quickly."),
            ("Barrier and floor", "Front-of-stage, aisles, VIP and back-of-house, as the room needs."),
            ("Close-out", "The last hour is the one that goes wrong; we staff it properly."),
            ("One lead on site", "Your point of contact all night, not a rotating cast."),
            ("Incident report", "Filed before the crew leaves, whether or not anything happened."),
        ],
        "steps": [
            ("Send the date and the room", "Venue, headcount, hours, bar, and whether alcohol is served."),
            ("We size the crew", "A written number of officers with the reasoning, not a guess."),
            ("We work it", "Briefing before doors, one lead on the radio, report before we leave."),
        ],
        "for_whom": ["Concerts and club nights", "Weddings and receptions", "Galas and corporate evenings",
                     "Festivals and street events", "Private parties at home"],
        "faq": [
            ("How many officers does my event need?",
             "It depends on headcount, alcohol, the number of entrances and the hours. Send those four "
             "things and we will put a number in writing the same day."),
            ("Do you work with the venue's own staff?",
             "Yes, often. We brief with the venue's team so the room has one plan rather than two."),
            ("How late can you cover?",
             "Any hours, including load-out and the drive home. Dispatch is answered 24/7."),
        ],
    },
    {
        "slug": "venue-security",
        "name": "Venue security",
        "art": "svc-venue-security",
        "alt": "Five Swarm officers in black at a venue entrance at night.",
        "title": "Bar &amp; Nightclub Security Toronto — Door Staff",
        "desc": "Licensed door staff and floor security for Toronto bars, clubs and lounges. The same "
                "crew every week, trained to de-escalate, with a written incident report every night.",
        "h1": "Venue security.",
        "lede": "Door, floor and close. The same faces every week, so the regulars are known and the "
                "trouble is spotted before it starts.",
        "includes": [
            ("The same crew weekly", "Continuity is the service. Your room gets learned, not re-learned."),
            ("Door and ID", "Capacity counts, ID checks, dress and entry policy as you set it."),
            ("Floor coverage", "Walkthroughs, bar watch, washroom checks, and eyes on the smoking area."),
            ("Close and sweep", "Last call, clear-out and a walk of the perimeter before lock-up."),
            ("Licence-safe practice", "Everything done the way the AGCO and your insurer expect it."),
            ("Nightly report", "Refusals, ejections, injuries and timings — filed before the shift ends."),
        ],
        "steps": [
            ("Walk the room with us", "We see the door, the bar, the blind corners and the exits."),
            ("Agree the standing order", "Capacity, entry policy, when we call police, who signs the report."),
            ("We staff it weekly", "Same crew, same standard, reviewed with you monthly."),
        ],
        "for_whom": ["Bars and lounges", "Nightclubs", "Restaurants with a late licence",
                     "Venues under an AGCO condition", "Rooms that changed hands and need a reset"],
        "faq": [
            ("Can you cover one busy night a week?",
             "Yes. Most venue clients start with Friday and Saturday and add nights when it works."),
            ("What happens when someone has to go?",
             "Position, distance, tone — in that order. Hands are the last resort, and the report says why."),
            ("Do you handle capacity counts?",
             "Yes, with a clicker and a number the venue can show an inspector."),
        ],
    },
    {
        "slug": "party-bus-security",
        "name": "Party bus security",
        "art": "svc-party-bus-security",
        "alt": "A black party bus at the curb outside a venue at night.",
        "title": "Party Bus Security Toronto — Officers On Board",
        "desc": "Licensed security on party buses and group transport in Toronto and the GTA: on board, "
                "at each stop, and at the door of every venue on the route. Quoted per night.",
        "h1": "Party bus security.",
        "lede": "A moving room with a bar in it and a new door every hour. We ride with it.",
        "includes": [
            ("An officer on board", "On the bus for the whole route, not meeting you at the venue."),
            ("Every stop covered", "Off the bus first, on the bus last, at each door on the route."),
            ("Headcount at each stop", "Nobody gets left on a curb at 2am. Everyone is counted back on."),
            ("Driver liaison", "We work with your operator so pickups and parking are agreed in advance."),
            ("Alcohol and conduct", "The group's own rules enforced calmly, before the venue has to."),
            ("Report in the morning", "Stops, timings and anything worth knowing, written up."),
        ],
        "steps": [
            ("Send the route", "Pickup, stops, venues, the number of guests and the finish time."),
            ("We size it", "One or two officers depending on headcount, venues and the hours."),
            ("We ride it", "On board from the first pickup to the last drop-off."),
        ],
        "for_whom": ["Bachelor and bachelorette parties", "Birthdays and group nights out",
                     "Corporate outings and team events", "Prom and graduation nights",
                     "Any group whose night ends in a different city"],
        "faq": [
            ("Do you provide the bus as well?",
             "We can arrange it with our transport partners, or ride with the operator you have already booked."),
            ("Will the venues let you in?",
             "Our officers are licensed and we announce ourselves to each venue's own door team on arrival."),
            ("What if a guest becomes a problem?",
             "They are managed quietly, on the bus, before the next venue has to make it their problem."),
        ],
    },
    {
        "slug": "limousine-service",
        "name": "Limousine service",
        "art": "svc-limousine-service",
        "alt": "A black stretch limousine waiting under a hotel canopy at night.",
        "title": "Limousine Service with Security — Toronto &amp; GTA",
        "desc": "Chauffeured limousine and executive transport in Toronto and the GTA with a licensed "
                "security officer on the detail: airport runs, events, nights out and client visits.",
        "h1": "Limousine service.",
        "lede": "The car, the driver, and an officer who travels with it. One booking, one number, "
                "one person responsible for the whole trip.",
        "includes": [
            ("Chauffeured vehicle", "Sedan, SUV or stretch depending on the party and the occasion."),
            ("A licensed officer", "Optional on every trip, standard on close protection details."),
            ("Door to door", "Collected at the door, walked to the door — not dropped at a curb."),
            ("Airport runs", "Pearson and Billy Bishop, with the flight watched so the car is there when you land."),
            ("Route planning", "Traffic, construction and the quiet way out of a venue, worked out in advance."),
            ("Discretion", "Unmarked vehicles, no branding, and a confidentiality agreement on request."),
        ],
        "steps": [
            ("Tell us the trip", "Date, pickup, stops, party size and whether you want an officer along."),
            ("We confirm the car", "Vehicle, driver and timings in writing, with a single price."),
            ("We drive it", "One contact for the whole night, however many stops it has."),
        ],
        "for_whom": ["Executives and visiting clients", "Weddings and formal events",
                     "Nights out that should end quietly", "Airport transfers",
                     "Artists and touring crews between venues"],
        "faq": [
            ("Is the driver also the security officer?",
             "No. The driver drives. When you book security, a separate licensed officer travels with the car."),
            ("Can you do multi-city trips?",
             "Yes — we travel with clients anywhere in Canada, and the same crew stays with you for the trip."),
            ("Are the cars marked?",
             "No. Unmarked and unbranded, because most clients would rather not be announced."),
        ],
    },
    {
        "slug": "monitoring",
        "name": "Monitoring",
        "art": "svc-monitoring",
        "alt": "A house at night with the driveway lit and a camera under the eaves.",
        "title": "Home &amp; Business Monitoring — Toronto &amp; GTA",
        "desc": "Monitoring and patrols for homes, businesses, sites and vacant property across Toronto "
                "and the GTA: scheduled checks, alarm response support and a written log every visit.",
        "h1": "Monitoring.",
        "lede": "Somebody checks. On a schedule you set, with a record you can show an insurer.",
        "includes": [
            ("Scheduled checks", "Nightly, weekly or to a pattern you choose — doors, windows, gates, lights."),
            ("Vacant and renovation property", "The cases insurers ask about, covered properly."),
            ("Business after hours", "Offices, warehouses and retail once the staff have gone home."),
            ("A standing order", "Written instructions for what we check and who we call, agreed with you."),
            ("Escalation", "Your contact list, in order, and police when the situation calls for it."),
            ("A log per visit", "Time on, time off, what was found. Monthly summary on request."),
        ],
        "steps": [
            ("Walk the property", "We see what there is to protect and where the weak points are."),
            ("Agree the schedule", "How often, what gets checked, who gets called and when."),
            ("We check it", "Logged every visit, with photographs when something has changed."),
        ],
        "for_whom": ["Homes while the owners travel", "Vacant and listed properties",
                     "Construction and renovation sites", "Offices, warehouses and retail after hours",
                     "Condo boards and property managers"],
        "faq": [
            ("Is this alarm monitoring?",
             "It is physical checks by a licensed officer, and support alongside whatever alarm system you "
             "already have. We attend; we do not replace your alarm provider's central station."),
            ("How often do you attend?",
             "As often as you want it — from one check a night to a pattern across a week."),
            ("What do we get after each visit?",
             "A log entry with times and findings, and photographs when something has changed."),
        ],
    },
]

BY_SLUG = {s["slug"]: s for s in SERVICES}


ARROW = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def gets(items):
    """What you get: every item on one screen, arriving in a gentle stagger."""
    return "".join('<li style="--k:%d"><span class="gx__k">%02d</span><h3>%s</h3><p>%s</p></li>'
                   % (i % 3 + i // 3, i + 1, t, d) for i, (t, d) in enumerate(items))


def steps(items):
    return "".join('<li class="hw__step" style="--k:%d"><span class="hw__n">%02d</span><h3>%s</h3><p>%s</p></li>'
                   % (i, i + 1, t, d) for i, (t, d) in enumerate(items))


def _others(slug):
    return "".join(
        '<li><a class="olink" href="{slug}.html"><img src="assets/img/{art}-800.webp" alt="" width="800" height="547" '
        'loading="lazy" decoding="async"><b>{name}</b>{arrow}</a></li>'
        .format(slug=o["slug"], art=o["art"], name=o["name"], arrow=ARROW)
        for o in SERVICES if o["slug"] != slug)


def _schema(s):
    return ('<script type="application/ld+json">{"@context":"https://schema.org",'
            '"@type":"Service","name":"%s","serviceType":"%s","url":"%s/%s",'
            '"provider":{"@id":"%s/#org"},"areaServed":[{"@type":"State","name":"Ontario"},'
            '{"@type":"Country","name":"Canada"}]}</script>'
            % (s["name"], s["name"], BIZ["base"], s["slug"], BIZ["base"]))


def _body(s):
    quote = QUOTE % s["slug"]
    ctas = ('<div class="hero__cta"><a class="btn" href="{q}"><span>Get a quote</span></a>'
            '<a class="btn btn--ghost" href="tel:{tel}"><span>Call {phone}</span></a></div>'
            .format(q=quote, tel=BIZ["phone_tel"], phone=BIZ["phone_ui"]))
    who = "".join("<li>%s</li>" % w for w in s["for_whom"])
    return "\n".join([
        ihero(crumb_html([("Home", "index.html"), ("Services", "index.html#services"), (s["name"], "")]),
              "Service", s["h1"], s["lede"],
              img(s["art"], (800, 1600), "100vw", s["alt"], loading="eager", priority=True, ratio=1216 / 832.0),
              ctas, label=s["name"]),
        """<section class="scr gx" id="includes" data-label="What you get" aria-labelledby="h-gets">
<div class="wrap scr__in">
<p class="eyebrow">What you get</p><h2 id="h-gets">In every booking</h2>
<ol class="gx__list">{gets}</ol>
<a class="go" href="{q}">Get a quote for {name_l} {arrow}</a>
</div>
</section>""".format(gets=gets(s["includes"]), q=quote, name_l=s["name"].lower(), arrow=ARROW),
        """<section class="scr hw" id="runs" data-label="How it runs" aria-labelledby="h-runs">
<div class="wrap scr__in">
<p class="eyebrow">How a booking runs</p><h2 id="h-runs">Three steps, one lead</h2>
<ol class="hw__steps">{steps}</ol>
<div class="whofor"><p class="eyebrow">Who it is for</p><ul>{who}</ul></div>
</div>
</section>""".format(steps=steps(s["steps"]), who=who),
        """<section class="scr qx" id="questions" data-label="Questions" aria-labelledby="h-q">
<div class="wrap scr__in qx__in">
<div><p class="eyebrow">Questions</p><h2 id="h-q">Asked about {name_l}</h2>
<p class="qx__more"><a class="go" href="answers.html">More answers {arrow}</a></p></div>
<div>{faq}
<div class="others"><p class="eyebrow">The rest of what we do</p><ul>{others}</ul></div></div>
</div>
</section>""".format(name_l=s["name"].lower(), arrow=ARROW, faq=faq_html(s["faq"]), others=_others(s["slug"])),
        cta_final(0, quote=quote),
    ])


def pages():
    out = {}
    for s in SERVICES:
        out["%s.html" % s["slug"]] = page(
            path="/%s.html" % s["slug"], depth=0, title=s["title"], desc=s["desc"],
            og="/assets/og/og-default.jpg",
            schema=_schema(s) + faq_schema([(q, plain(a)) for q, a in s["faq"]]),
            body=_body(s), bodyattr=' class="screens"')
    return out
