# -*- coding: utf-8 -*-
"""The six service pages — what the home page's one-liners actually mean.

The home page sells; these pages answer. Each one shows what you get (an annotated plan of that kind of
job that plays out as the screen arrives, build/stories.py) and the two or three questions people ask about
that service specifically. No prices: every job is quoted.

Edit the copy here. `build/service_art.py` exports the photographs.
"""
from common import BIZ, crumb_html, faq_html, faq_schema, ihero, img, page, plain
import stories

# the quote page, with this service already picked
QUOTE = "quote.html?service=%s"

# slug, name, art, title, h1, lede, includes, steps, for_whom, faq
# ("steps", "for_whom" and the "includes" details are not drawn any more: the three steps live on process.html; kept as the
#  per-service wording for the quote follow-up)
SERVICES = [
    {
        "slug": "close-protection",
        "name": "Close protection",
        "art": "svc-close-protection",
        "alt": "Two Swarm close protection officers in black beside a client's car at a hotel entrance.",
        "title": "Close Protection & Bodyguards | Toronto &amp; GTA",
        "desc": 'Discreet close protection in Toronto and the GTA for executives, artists, visiting clients and families. Advance planning, trained officers and secure transport.',
        "h1": "Close protection",
        "lede": 'Discreet, trained officers who stay close and plan every move ahead of you.',
        "includes": [
            ('A named lead', 'One person runs your detail and is easy to reach throughout.'),
            ('Advance on the location', 'We visit the venue and the route before you arrive.'),
            ('Arrivals and departures', 'The moments you step in and out of a car are planned carefully.'),
            ('Secure transport', 'A chauffeured vehicle with an officer, or we work alongside your driver.'),
            ('Discretion in writing', 'We sign a confidentiality agreement that covers your details and plans.'),
            ('A second way out', 'Every venue we work has an exit plan ready in case it is needed.'),
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
            ('Are your bodyguards armed?', 'No. Private security officers in Ontario are not allowed to carry firearms. We protect you through careful planning, a steady presence and calm, clear communication.'),
            ('Can you travel with us?', 'Yes. We can travel with you anywhere in Canada. Where another province has its own rules, we work with trusted local partners.'),
            ('How discreet is it?', 'As discreet as you would like. Our officers can dress and act like part of your team, or stay clearly visible when that helps keep people at a distance.'),
        ],
    },
    {
        "slug": "event-security",
        "name": "Event security",
        "art": "svc-event-security",
        "alt": "A security officer at the barrier in front of a concert crowd.",
        "title": "Event Security Toronto | Concerts, Weddings, Galas",
        "desc": 'Event security across Toronto and the GTA for concerts, weddings, galas, festivals and private parties. Door, barrier and floor teams, quoted for each event.',
        "h1": "Event security",
        "lede": 'The right number of officers in the right places, from doors open until the last guest leaves.',
        "includes": [
            ('A plan before the day', 'We map entrances, exits and key positions before the event.'),
            ('Door and ID checks', 'Guest lists, wristbands and ID are handled politely and quickly.'),
            ('Barrier and floor', 'Officers at the stage, the aisles and the VIP areas, as your event needs.'),
            ('One lead on site', 'You have one person to talk to for the whole event.'),
            ('Artist and VIP route', 'A clear, private path for performers and special guests.'),
            ('Close-out', 'We stay until your guests have left and the venue is clear.'),
        ],
        "steps": [
            ("Send the date and the room", "Venue, headcount, hours, bar, and whether alcohol is served."),
            ("We size the crew", "A written number of officers with the reasoning, not a guess."),
            ("We work it", "Briefing before doors, one lead on the radio, report before we leave."),
        ],
        "for_whom": ["Concerts and club nights", "Weddings and receptions", "Galas and corporate evenings",
                     "Festivals and street events", "Private parties at home"],
        "faq": [
            ('How many officers does my event need?', 'It depends on the number of guests, whether alcohol is served, how many entrances there are and how late the event runs. Send us those details and we will recommend a number, usually the same day.'),
            ("Do you work with the venue's own staff?", 'Yes, we often do. We meet the venue team beforehand so everyone works from one shared plan.'),
            ('How late can you stay?', 'As late as your event needs, including load-out and helping guests get home safely. You can reach us at any hour.'),
        ],
    },
    {
        "slug": "venue-security",
        "name": "Venue security",
        "art": "svc-venue-security",
        "alt": "Five Swarm officers in black at a venue entrance at night.",
        "title": "Bar &amp; Nightclub Security Toronto | Door Staff",
        "desc": 'Door and floor security for bars, clubs and lounges in Toronto. The same trained team every week, focused on keeping your guests safe and your nights calm.',
        "h1": "Venue security",
        "lede": 'A steady door and floor team that gets to know your venue and your regulars.',
        "includes": [
            ('The same crew weekly', 'The same faces every week, so your regulars know who we are.'),
            ('Door and ID', 'Guests are checked in a friendly, consistent way.'),
            ('Floor coverage', 'Officers keep an eye on the room, the washrooms and the patio.'),
            ('Bar watch', 'We support your bar staff when a guest has had enough.'),
            ('VIP room', 'Your private areas stay comfortable and under control.'),
            ('Close and sweep', 'A calm last call, a clear room and a final walk of the venue.'),
        ],
        "steps": [
            ("Walk the room with us", "We see the door, the bar, the blind corners and the exits."),
            ("Agree the standing order", "Capacity, entry policy, when we call police, who signs the report."),
            ("We staff it weekly", "Same crew, same standard, reviewed with you monthly."),
        ],
        "for_whom": ["Bars and lounges", "Nightclubs", "Restaurants with a late licence",
                     "Venues under an AGCO condition", "Rooms that changed hands and need a reset"],
        "faq": [
            ('Can you cover one busy night a week?', 'Yes. Many venues start with Friday and Saturday and add more nights when it suits them.'),
            ('What happens when a guest has to leave?', 'We talk first and keep a respectful distance. Most situations calm down with the right words, and physical contact is always the very last option.'),
            ('Do you handle capacity counts?', 'Yes. We keep a running count at the door, so you always know how many people are inside.'),
        ],
    },
    {
        "slug": "party-bus-security",
        "name": "Party bus security",
        "art": "svc-party-bus-security",
        "alt": "A black party bus at the curb outside a venue at night.",
        "title": "Party Bus Security Toronto | Officers On Board",
        "desc": 'Security for party buses and group nights out in Toronto and the GTA. An officer travels with your group and stays with them at every stop.',
        "h1": "Party bus security",
        "lede": 'An officer rides with your group and stays with them at every stop.',
        "includes": [
            ('Driver liaison', 'We agree the route, the stops and the timings with your driver.'),
            ('An officer on board', 'Your officer rides with the group for the whole night.'),
            ('Every stop covered', 'The officer goes into each venue with your group.'),
            ('Headcount at each stop', 'Everyone is counted back on before the bus moves.'),
            ('Alcohol and conduct', "Your group's own rules are kept calmly and politely."),
            ('Safe drop-off', 'Everyone gets home or to their next stop safely.'),
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
            ('Do you provide the bus as well?', 'We can arrange one through our transport partners, or ride with the company you have already booked.'),
            ('Will the venues let you in?', "Yes. Our officer introduces themselves to each venue's door team when your group arrives."),
            ('What if a guest becomes a problem?', 'Our officer handles it quietly on the bus, before it affects the rest of the group or the next venue.'),
        ],
    },
    {
        "slug": "limousine-service",
        "name": "Limousine service",
        "art": "svc-limousine-service",
        "alt": "A black stretch limousine waiting under a hotel canopy at night.",
        "title": "Limousine Service with Security | Toronto &amp; GTA",
        "desc": 'Chauffeured limousine and executive transport in Toronto and the GTA with a security officer on board, for airport runs, events, nights out and client visits.',
        "h1": "Limousine service",
        "lede": 'A chauffeured car with a trained officer, from your door to your destination.',
        "includes": [
            ('Chauffeured vehicle', 'A sedan, SUV or limousine, depending on the occasion.'),
            ('A trained officer', 'Optional on any trip, and standard on close protection.'),
            ('Door to door', 'We collect you at your door and walk you to the next one.'),
            ('Airport runs', 'Pearson and Billy Bishop, with your flight tracked so the car is waiting.'),
            ('Route planning', 'Traffic, construction and the quiet way into each venue, worked out ahead.'),
            ('Discretion', 'Unmarked cars and a confidentiality agreement when you need one.'),
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
            ('Is the driver also the security officer?', 'No. Your driver focuses on driving. When you book security, a separate officer travels with you.'),
            ('Can you do multi-city trips?', 'Yes. We can travel with you anywhere in Canada, and the same team stays with you for the whole trip.'),
            ('Are the cars marked?', 'No. Our cars are unmarked, because most clients prefer to arrive without drawing attention.'),
        ],
    },
    {
        "slug": "monitoring",
        "name": "Monitoring",
        "art": "svc-monitoring",
        "alt": "A house at night with the driveway lit and a camera under the eaves.",
        "title": "Home &amp; Business Monitoring | Toronto &amp; GTA",
        "desc": 'Mobile patrols and property checks for homes, businesses, sites and vacant property across Toronto and the GTA, on the schedule you choose.',
        "h1": "Monitoring",
        "lede": 'Regular checks on your home, business or empty property, on the schedule you choose.',
        "includes": [
            ('Scheduled checks', 'Visits on the days and at the times you choose.'),
            ('Vacant and renovation property', 'Empty homes and building sites are checked regularly.'),
            ('Business after hours', 'Doors, windows and lights are checked once you have closed.'),
            ('A standing order', 'Clear instructions on what we check and who we call.'),
            ('Escalation', 'If something is wrong, we call you and the right services straight away.'),
            ('Every corner checked', 'Each visit covers the whole property, not only the front door.'),
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
            ('Is this the same as alarm monitoring?', 'No. Our officers visit your property in person. We work alongside your existing alarm system rather than replacing it.'),
            ('How often do you visit?', 'As often as you need, from one check a night to a regular pattern across the week.'),
            ('What happens if something is wrong?', 'We call you straight away and, if needed, the police or the fire service.'),
        ],
    },
]

BY_SLUG = {s["slug"]: s for s in SERVICES}





def _others(slug):
    return "".join(
        '<li><a class="olink" href="{slug}.html"><img src="assets/img/{art}-800.webp" alt="" width="800" height="547" '
        'loading="lazy" decoding="async"><b>{name}</b></a></li>'
        .format(slug=o["slug"], art=o["art"], name=o["name"])
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
    return "\n".join([
        ihero(crumb_html([("Home", "index.html"), ("Services", "index.html#services"), (s["name"], "")]),
              s["h1"], s["lede"],
              img(s["art"], (800, 1600), "100vw", s["alt"], loading="eager", priority=True, ratio=1216 / 832.0),
              ctas, label=s["name"], poster=True),
        """<section class="scr gx gx--story" id="includes" data-label="What you get" aria-labelledby="h-gets">
<div class="wrap scr__in gx__in">
<h2 id="h-gets">What is included</h2>
{story}
</div>
</section>""".format(story=stories.figure(s["slug"], [t for t, _ in s["includes"]])),
        """<section class="scr qx" id="questions" data-label="Questions" aria-labelledby="h-q">
<div class="wrap scr__in qx__in">
<div class="qx__side"><h2 id="h-q">Questions about {name_l}</h2>
<div class="others"><p class="others__h">More services</p><ul>{others}</ul><a class="others__all" href="index.html#services"><img src="assets/img/svc-event-security-800.webp" alt="" width="800" height="547" loading="lazy" decoding="async"><span>Explore our services</span></a></div></div>
<div>{faq}</div>
</div>
</section>""".format(name_l=s["name"].lower(), faq=faq_html(s["faq"]), others=_others(s["slug"])),
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
