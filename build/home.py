# -*- coding: utf-8 -*-
"""The single page. Every nav item is an anchor on this document."""
from common import (AREAS, BIZ, faq_html, faq_schema, img, page, picture, plain)

P = BIZ["phone_ui"]
T = BIZ["phone_tel"]


# ---------------------------------------------------------------------------
# 1. Hero
# ---------------------------------------------------------------------------
HERO = """<section class="hero" id="top">
<div class="hero__media">{im}</div>
<div class="hero__shutter" aria-hidden="true"></div>
<div class="wrap hero__in">
<p class="hero__kicker rise" style="--i:0">Last night at your venue</p>
<h1 class="rise" style="--i:1">Nothing<br>happened.</h1>
<p class="hero__lede rise" style="--i:2">That is the product. Licensed door staff, event
security and close protection across Toronto and the GTA — a crew large enough that nobody
tries it, trained well enough that it never gets that far.</p>
<div class="hero__cta rise" style="--i:3">
<a class="btn" href="#quote"><span>Request a quote</span></a>
<a class="btn btn--ghost" href="tel:{tel}"><span>Call dispatch {phone}</span></a>
</div>
<div class="hero__foot rise" style="--i:4">
<span>PSISA-licensed officers</span>
<span>$5M liability</span>
<span>WSIB covered</span>
<span>Same crew every week</span>
</div>
</div>
<a class="hero__scroll rise" style="--i:5" href="#proof" aria-label="Scroll to what we do">
<i></i></a>
</section>""".format(
    im=picture(("crew-hero", [640, 900, 1200, 1600]), ("hall-tall", [640, 900]),
               "Swarm Protective Services door staff on shift at a Toronto venue",
               loading="eager", priority=True, ratio=16 / 9),
    tel=T, phone=P)


# ---------------------------------------------------------------------------
# 2. Proof + ticker
# ---------------------------------------------------------------------------
PROOF = """<section class="proof" id="proof">
<div class="proof__grid">
<div class="proof__cell reveal"><span class="proof__n" data-count="24" data-suffix=" h">24 h</span>
<span class="proof__l">Dispatch answered. Every day of the year, including the call you make at 1am.</span></div>
<div class="proof__cell reveal"><span class="proof__n" data-count="5" data-prefix="$" data-suffix="M">$5M</span>
<span class="proof__l">Commercial general liability. Certificate sent before the first shift.</span></div>
<div class="proof__cell reveal"><span class="proof__n" data-count="40" data-suffix=" h">40 h</span>
<span class="proof__l">Ministry-approved training and a provincial exam before anyone works a door.</span></div>
<div class="proof__cell reveal"><span class="proof__n" data-count="100" data-suffix="%">100%</span>
<span class="proof__l">Shifts closed with a written incident report before the crew leaves.</span></div>
</div>
</section>

<div class="ticker" aria-hidden="true">
<div class="ticker__row">{row}{row}</div>
</div>""".format(row="".join(
    '<span>%s</span><b></b>' % t for t in [
        "Nightclub security", "Event security", "Close protection", "Door staff",
        "Weddings", "Corporate", "Film and production", "Festivals",
        "Executive protection", "Residential", "High-risk details", "24-hour dispatch",
    ]))


# ---------------------------------------------------------------------------
# 3. Services — one anchored block each
# ---------------------------------------------------------------------------
def service(anchor, label, blurb, h2, lede, bullets, image, alt, ratio, mobile=None,
            flip=False, extra="", alt_bg=False):
    lis = "".join("<li>%s</li>" % b for b in bullets)
    media = (picture(image, mobile, alt, sizes="(min-width:900px) 46vw, 100vw",
                     ratio=ratio) if mobile
             else img(image[0], image[1], "(min-width:900px) 46vw, 100vw", alt, ratio=ratio))
    return """<section class="svc-block{bg}" id="{a}">
<div class="wrap">
<div class="split{fl} reveal">
<div class="stack">
<p class="eyebrow">{label}</p>
<h2>{h2}</h2>
<p class="lede">{lede}</p>
<ul class="ticks">{lis}</ul>
{extra}
<a class="btn" href="#quote"><span>Request a quote</span></a>
</div>
<figure class="frame frame--{r}"><span class="frame__zoom">{media}</span>
<figcaption>{blurb}</figcaption></figure>
</div>
</div>
</section>""".format(a=anchor, label=label, h2=h2, lede=lede, lis=lis, media=media,
                     blurb=blurb, extra=extra, fl=" split--flip" if flip else "",
                     bg=" alt" if alt_bg else "",
                     r="tall" if ratio < 1 else ("sq" if ratio == 1 else "wide"))


VENUES = service(
    "venues", "Bars · nightclubs · lounges", "Door and floor — Toronto",
    "Nightclub and bar<br>security, run properly.",
    "Licensed door and floor officers for late-licence venues across Toronto and the GTA. "
    "Your regulars should never learn our names.",
    ["An ID position fast enough that no queue ever becomes the problem",
     "A running count held legal at peak, because that is what an inspector checks",
     "Refusals and ejections logged with a time and a stated reason",
     "The same named lead every week, who knows your room and your staff"],
    ("crew-wide", [640, 900, 1200, 1600]),
    "Swarm door staff at a licensed Toronto venue", 16 / 9)

EVENTS = service(
    "events", "Concerts · weddings · corporate · film", "Event crew — GTA",
    "Event security, built<br>from your floor plan.",
    "Concerts, festivals, weddings, corporate functions and production. We size the crew from "
    "your site, not from a headcount you guessed.",
    ["A post map on your floor plan before the day, not a verbal on arrival",
     "Access control, wristband tiers and guest lists enforced politely",
     "Artist and VIP routes walked before the doors open",
     "One named lead with a mobile number — not a dispatch queue"],
    ("crew-hall", [640, 900, 1200, 1600]),
    "Swarm event security crew at a venue entrance", 16 / 10, flip=True, alt_bg=True)

PROTECTION = service(
    "protection", "Executive · personal · family · talent", "Close protection — Toronto",
    "Close protection<br>that reads as staff.",
    "Executive and personal protection across the GTA. Most of the work is finished before you "
    "see anybody standing near you.",
    ["Every venue and route walked in advance, not discovered with you in the car",
     "Arrivals and departures managed — where almost every incident happens",
     "Agents who dress to the room and hold distance",
     "Residential, family and school-run coverage by the same faces"],
    ("lot-wide", [640, 900, 1200]),
    "Swarm close protection agents at a vehicle at night", 16 / 9)

HIGH_RISK = """<section class="alt" id="high-risk">
<div class="wrap">
<div class="rail reveal">
<div class="rail__label">Read this one first
<span>The page where we would rather be accurate than impressive.</span></div>
<div class="stack">
<h2>High-risk work,<br>and the truth about<br>armed security.</h2>
<div class="note">
<p><b>Bodyguards in Canada do not carry firearms.</b> A restricted firearm needs a federal
Authorization to Carry, and the regulations issue it for moving cash, negotiable instruments and
goods of substantial value — not for protecting a person going about their day.</p>
<p>Any GTA company advertising armed bodyguards is either wrong or selling you a legal problem.
We would rather publish that and lose the enquiry.</p>
</div>
<p class="lede">What we do take on: threat-assessed protective details, escalated personal
threats, hostile terminations, residential hardening, and high-value goods in transit — the one
category where Canadian law does contemplate armed coverage, staffed only where the federal
authorization genuinely applies.</p>
<ul class="ticks">
<li>A written threat assessment before we quote anything</li>
<li>Same-day triage, with cover placed inside 24 hours while the assessment runs</li>
<li>Declined outright if it cannot be done lawfully — or if you need police, not a guard</li>
</ul>
<a class="btn" href="#quote"><span>Start a confidential triage call</span></a>
</div>
</div>
</div>
</section>"""


# ---------------------------------------------------------------------------
# 4. The night
# ---------------------------------------------------------------------------
NIGHT_ROWS = [
    ("19:40", "The lead walks your room before the crew arrives",
     "Fire exits, blind corners, where the line will form, which camera covers the patio. "
     "Anything that changed since last week gets found now, not at midnight."),
    ("20:15", "Posts assigned out loud, in front of everyone",
     "Door, ID, floor, patio, back of house. Each officer repeats their post and their "
     "escalation path. Your manager gets the lead's mobile, not a call centre."),
    ("21:00", "Doors open and the line behaves itself",
     "ID checked properly and fast — a slow door builds the crowd that becomes the incident. "
     "Refusals are polite, final, and logged. Nobody is made an example of on the sidewalk."),
    ("23:30", "Peak. Floor officers are counting, not watching",
     "Capacity stays legal. Drinks stop moving toward the people who should stop drinking. "
     "Most of the job happens here and none of it looks like anything."),
    ("01:15", "The one that would have been a story",
     "Two people, one table, voices up. Two officers arrive from different angles and stand "
     "close enough to be inevitable. One goes to the bar, one goes outside for air. Nobody is "
     "touched, nobody is humiliated, and neither of them mentions it tomorrow."),
    ("02:20", "Last call, and the slow clear",
     "Lights and volume do most of it. We clear inside-out, keep the sidewalk moving, watch "
     "the rideshare corner, and stay until your staff have cashed out."),
    ("03:05", "The report is written before we leave",
     "Head count, refusals, ejections, first aid, police attendance, and everything that nearly "
     "happened. In your inbox before the crew is in the car — because in eighteen months, when "
     "someone's lawyer asks, that document is the difference."),
]

NIGHT = """<section id="night">
<div class="wrap">
<div class="rail rail--wide">
<div class="rail__label">One shift, start to finish
<span>A Saturday in a 300-capacity room. This is the thing you are actually buying.</span></div>
<div>
<h2 class="reveal">What a night<br>with us looks like.</h2>
<div class="night">{rows}</div>
</div>
</div>
</div>
</section>""".format(rows="".join(
    '<div class="night__row reveal"><div class="night__t">%s</div>'
    '<div class="night__b"><h3>%s</h3><p>%s</p></div></div>' % r for r in NIGHT_ROWS))


# ---------------------------------------------------------------------------
# 5. The crew
# ---------------------------------------------------------------------------
BAND = """<section class="band">
<div class="band__media">{im}</div>
<div class="wrap reveal">
<h2>Size gets you looked at.<br>Training gets<br>everyone home.</h2>
<p class="lede" style="margin-top:26px">Presence ends most of it. A doorway that is physically
difficult to argue with is the cheapest security a venue can buy, and we are not going to be
coy about that.</p>
<p class="lede" style="margin-top:16px"><strong>But size is the entry requirement, not the
qualification.</strong> We are not selling you a fight we win. We are selling you a night that
never turns into one.</p>
<div class="hero__cta"><a class="btn btn--ghost" href="#crew"><span>Meet the crew</span></a></div>
</div>
</section>""".format(
    im=img("crew-hall", [640, 900, 1200, 1600], "100vw",
           "Swarm officers holding a corridor at a licensed venue", ratio=16 / 10,
           cls="parallax"))

CREDS = [
    ("Ontario security agency licence", BIZ["licence"]),
    ("Officer licensing", "PSISA, current, digital"),
    ("Ministry-approved training", "40 hours + exam"),
    ("Background check", "CRJMC at every renewal"),
    ("First aid", "Standard First Aid + CPR-C"),
    ("Naloxone", "Carried on venue shifts"),
    ("Use-of-force refresher", "Twice a year"),
    ("De-escalation refresher", "Twice a year"),
    ("Commercial general liability", "$5,000,000"),
    ("WSIB", "Full coverage, cleared"),
    ("Incident reporting", "Before the shift ends"),
    ("Subcontracting", "None. Ever."),
]

CREW = """<section class="alt" id="crew">
<div class="wrap">
<div class="split split--wide reveal">
<figure class="frame frame--sq"><span class="frame__zoom">{im}</span>
<figcaption>The crew — Toronto</figcaption></figure>
<div class="stack">
<p class="eyebrow">The crew</p>
<h2>Staffing by<br>relationship,<br>not by rota.</h2>
<p class="lede">Most security in this city is sold as a commodity. A venue calls an agency, the
agency sends whoever is free, and a stranger arrives at 21:00 who has never seen the room.</p>
<p class="lede">That is cheap for the agency and expensive for you. It is also why door staff
get a reputation for being heavy-handed — a person with no context has only one tool.</p>
<p class="lede"><strong>We built Swarm the other way round.</strong> A named lead owns your
account. The same faces work your nights. Cover comes from the same pool, briefed by the same
lead. We take on new venues slowly, on purpose.</p>
</div>
</div>

<div class="rail reveal" style="margin-top:clamp(56px,8vw,96px)">
<div class="rail__label">What every officer holds
<span>All of it verifiable. Ask for any of it and it arrives the same day.</span></div>
<div>
<h3 class="h2ish">Credentials, not claims.</h3>
<dl class="kv">{creds}</dl>
</div>
</div>

<div class="rail reveal" style="margin-top:clamp(48px,7vw,80px)">
<div class="rail__label">What we decline
<span>Four rules that decide what we take on.</span></div>
<div>
<h3 class="h2ish">We turn work down.</h3>
<div class="cards cards--2">
<div class="card"><h3>We never sell fear</h3><p>You will not find a crime statistic on this
site. If you are here you already know why. Frightening you into a bigger package is a sales
technique, not a service.</p></div>
<div class="card"><h3>We never imply violence</h3><p>A crew that advertises how hard it hits is
telling you how its incidents end. That is a liability you would be buying.</p></div>
<div class="card"><h3>We say when you do not need us</h3><p>Over-staffing a room is easy money
and a short relationship. If two officers will do, we quote two.</p></div>
<div class="card"><h3>We decline work</h3><p>Anything unlawful, anything that is intimidation
wearing a uniform, and any client who wants presence in order to start something.</p></div>
</div>
</div>
</div>
</div>
</section>""".format(
    im=img("crew-sq", [500, 700, 1000], "(min-width:900px) 46vw, 100vw",
           "Five Swarm officers in matching black at a venue entrance", ratio=1),
    creds="".join('<div class="kv__row"><dt>%s</dt><dd>%s</dd></div>' % c for c in CREDS))


# ---------------------------------------------------------------------------
# 6. Process + coverage
# ---------------------------------------------------------------------------
PROCESS = """<section id="process">
<div class="wrap">
<div class="rail">
<div class="rail__label">Booking
<span>Most quotes go out the same day. Urgent nights are triaged in under an hour.</span></div>
<div>
<h2 class="reveal">Three steps to<br>a covered night.</h2>
<div class="steps">
<div class="step reveal"><h3>Tell us the night</h3><p>Date, venue, capacity, dress code, and
what has gone wrong before. Two minutes on the form, ninety seconds on the phone.</p></div>
<div class="step reveal"><h3>We walk it, then quote it</h3><p>For anything recurring we come and
look at the room first. Twenty minutes, free, no pitch. You get a staffing plan, a flat number
and the name of the lead who will run it.</p></div>
<div class="step reveal"><h3>The crew turns up early</h3><p>Briefed, in uniform or in suits,
ahead of the time you asked for. You go back to running your business.</p></div>
</div>
</div>
</div>
</div>
</section>

<section class="alt" id="coverage">
<div class="wrap">
<div class="rail reveal">
<div class="rail__label">Where we work
<span>No travel charge inside this list. Further afield quoted up front.</span></div>
<div>
<h2>Toronto and<br>the wider GTA.</h2>
<ul class="areas" style="margin-top:28px">{areas}</ul>
<p class="lede" style="margin-top:30px">Same-day cover for existing clients, next-day for a new
venue after a walk-through. Multi-day events and protection details travel further, with costs
agreed before the booking rather than added to the invoice.</p>
</div>
</div>
</div>
</section>""".format(areas="".join("<li>%s</li>" % a for a in AREAS))


# ---------------------------------------------------------------------------
# 7. FAQ
# ---------------------------------------------------------------------------
FAQS = [
    ("How much does security cost in Toronto?",
     "<p>It depends on the room, the hours and the risk, so we price from a site plan rather "
     "than a phone call. Recurring venue work goes on a flat weekly rate so you can budget; "
     "events are quoted per floor plan; protection details are quoted per assignment.</p>"
     "<p>Send us the night and you will have a written number, usually the same day, with the "
     "name of the lead who would run it.</p>"),
    ("Are your officers actually licensed?",
     "<p>Yes. Every officer holds a current licence under Ontario's <em>Private Security and "
     "Investigative Services Act</em> — a 40-hour ministry-approved program, a provincial exam, "
     "a Criminal Record and Judicial Matters Check, and emergency first aid. Licences are "
     "digital and carried on shift. Ask any officer and they will show you theirs.</p>"
     "<p>We also hold an Ontario security agency licence, which is the one that lets a company "
     "supply guards at all. Ours is {lic}.</p>".format(lic=BIZ["licence"])),
    ("Do you provide armed guards or armed bodyguards?",
     "<p>In Ontario, bodyguards cannot carry firearms. A federal Authorization to Carry is "
     "issued almost exclusively for protecting cash and goods of substantial value in transit, "
     "not for personal protection.</p>"
     "<p>Any company advertising armed bodyguards for your event is misinformed or misleading "
     "you. Tell us what is actually happening and we will tell you what is lawfully available "
     "— and if the honest answer is police rather than a guard, we will say that.</p>"),
    ("How many officers does my event need?",
     "<p>Count positions before ratios. Every open entrance, every ID point, back of house, the "
     "bar or cash area, each area you cannot see from another, and one lead holding no post at "
     "all. Then sanity-check the total — roughly one officer per 75–100 guests where alcohol is "
     "served late, nearer one per 150 for a controlled corporate event.</p>"
     "<p>Send the floor plan and we will size it properly and put it in writing.</p>"),
    ("How fast can you staff a shift?",
     "<p>Dispatch is answered 24 hours. Same-day cover for an existing client. Next-day for a "
     "new venue, after a twenty-minute walk-through. Large events want one to three weeks so "
     "the staffing plan is built rather than guessed.</p>"),
    ("What happens if something does go wrong?",
     "<p>The officer on scene manages it, the lead takes command, and emergency services are "
     "called when the situation crosses that line — not after a debate about how it looks. You "
     "get a verbal from the lead that night and a written incident report before the crew "
     "leaves your building.</p>"
     "<p>We carry $5M commercial general liability and full WSIB coverage, and our officers are "
     "trained on the limits of a guard's lawful authority. Knowing what you may not do is most "
     "of this job.</p>"),
    ("Do you work outside Toronto?",
     "<p>Across the GTA and the Golden Horseshoe as standard — Mississauga, Brampton, Vaughan, "
     "Markham, Oakville, Burlington, Hamilton and the Durham municipalities. Further for "
     "multi-day events and protection details, with travel agreed up front.</p>"),
    ("Do you subcontract?",
     "<p>No. Every officer on your site is ours, on our payroll, briefed by our lead and "
     "covered by our insurance. Subcontracting is how a client ends up with an unvetted stranger "
     "at their door and an unanswerable question about liability afterwards.</p>"),
]

FAQ_SECTION = """<section id="answers">
<div class="wrap">
<div class="rail">
<div class="rail__label">Before you call
<span>What venue owners and event managers actually ask, answered without the sales voice.</span></div>
<div>
<h2 class="reveal">Questions we<br>get every week.</h2>
<div class="reveal">{faq}</div>
</div>
</div>
</div>
</section>""".format(faq=faq_html(FAQS))


# ---------------------------------------------------------------------------
# 8. Quote form
# ---------------------------------------------------------------------------
QUOTE = """<section class="alt" id="quote">
<div class="wrap">
<div class="rail rail--wide">
<div class="rail__label">Request a quote
<span>Nothing here is shared with anyone. We do not sell, rent or pass on your details, and we
do not add you to a mailing list.</span>
<span style="margin-top:18px">Or call dispatch — <a href="tel:{tel}" style="color:var(--gold-hi)">{phone}</a>,
answered 24 hours.</span></div>
<div>
<h2 class="reveal">Tell us<br>the night.</h2>
<p class="lede" style="margin-top:18px;margin-bottom:34px">Date, venue and headcount is enough
to start. You get a written number and a named lead, usually the same day.</p>
<form class="form reveal" data-quote novalidate>
<div class="f"><label for="nm">Your name</label>
<input id="nm" name="name" autocomplete="name" required>
<span class="err">We need a name to put on the quote.</span></div>

<div class="f"><label for="ph">Phone</label>
<input id="ph" name="phone" type="tel" inputmode="tel" autocomplete="tel" required>
<span class="err">A number we can reach you on tonight.</span></div>

<div class="f"><label for="em">Email</label>
<input id="em" name="email" type="email" autocomplete="email" required>
<span class="err">Check the email address.</span></div>

<div class="f"><label for="kd">What do you need</label>
<select id="kd" name="service">
<option>Venue and door security — recurring</option>
<option>Venue and door security — one night</option>
<option>Event security</option>
<option>Wedding or private function</option>
<option>Close protection</option>
<option>Film or production</option>
<option>High-risk — confidential</option>
<option>Not sure yet</option>
</select></div>

<div class="f"><label for="dt">Date it starts</label>
<input id="dt" name="date" type="date"></div>

<div class="f"><label for="gd">Officers needed</label>
<select id="gd" name="guards">
<option>1–2</option><option>3–5</option><option>6–10</option><option>11–20</option>
<option>More than 20</option><option>Not sure — advise me</option>
</select></div>

<div class="f f--full"><label for="lc">Venue or area</label>
<input id="lc" name="location" placeholder="Venue name, or the neighbourhood if it is private"></div>

<div class="f f--full"><label for="nt">Anything we should know</label>
<textarea id="nt" name="notes" rows="4" placeholder="Capacity, licensed hours, dress code, what happened last time, whether anyone has been barred."></textarea></div>

<input class="hp" type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">

<div class="f--full">
<button class="btn btn--full" type="submit"><span>Send it to dispatch</span></button>
<p class="form__note" style="margin-top:14px">For confidential protection enquiries, say so on
the call and we will keep it off email.</p>
<p class="form__note" data-senderr hidden style="color:#D98572">That did not send. Call
<a href="tel:{tel}" style="color:var(--gold-hi)">{phone}</a> and we will take it down on the phone.</p>
</div>

<div class="form__ok">
<h3>Received.</h3>
<p>A lead will come back to you with a number and a name. If this is for tonight, call {phone}
now rather than waiting on the email — dispatch is answered 24 hours.</p>
</div>
</form>
</div>
</div>
</div>
</section>""".format(tel=T, phone=P)


FINAL = """<section class="cta-final">
<div class="wrap reveal">
<img class="cta-final__em" src="assets/logo/emblem-216.webp" srcset="assets/logo/emblem-108.webp 108w, assets/logo/emblem-216.webp 216w" sizes="72px" alt="" width="216" height="238" loading="lazy" decoding="async">
<h2>You want the night to go smoothly.<br>Book it and stop thinking about it.</h2>
<p class="lede">Call the swarm.</p>
<div class="hero__cta">
<a class="btn" href="#quote"><span>Request a quote</span></a>
<a class="btn btn--ghost" href="tel:{tel}"><span>Call dispatch</span></a>
</div>
</div>
</section>""".format(tel=T)


BEE = """<div class="beeflight" aria-hidden="true">
<svg class="beeflight__trail" viewBox="0 0 100 1000" preserveAspectRatio="none">
<path id="beepath" d="M 88 0 C 20 120, 92 240, 30 360 C -10 470, 80 560, 26 690 C -6 800, 84 870, 50 1000"/>
</svg>
<div class="beeflight__bee"><img src="assets/logo/bee-160.webp" srcset="assets/logo/bee-160.webp 160w, assets/logo/bee-320.webp 320w" sizes="92px" alt="" width="160" height="190" loading="lazy" decoding="async"></div>
</div>"""


BODY = (BEE + HERO + PROOF + VENUES + EVENTS + PROTECTION + HIGH_RISK + NIGHT
        + BAND + CREW + PROCESS + FAQ_SECTION + QUOTE + FINAL)


SERVICE_SCHEMA = "".join(
    '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service",'
    '"name":"%s","serviceType":"%s","url":"%s/#%s",'
    '"provider":{"@id":"%s/#org"},'
    '"areaServed":{"@type":"State","name":"Ontario"}}</script>'
    % (n, n, BIZ["base"], a, BIZ["base"])
    for n, a in [
        ("Nightclub and bar security", "venues"),
        ("Event security", "events"),
        ("Close protection and executive protection", "protection"),
        ("High-risk protective detail", "high-risk"),
    ])


def build():
    return page(
        path="/",
        depth=0,
        title="Security Company Toronto | Door Staff, Event Security & Close Protection",
        ogtitle="Swarm Protective Services — nothing happened.",
        desc="Licensed security company in Toronto and the GTA — nightclub and bar door staff, "
             "event security and close protection. Same crew every week. Dispatch answered 24 hours.",
        body=BODY,
        og="/assets/og/og-home.jpg",
        schema=SERVICE_SCHEMA + faq_schema([(q, plain(a)) for q, a in FAQS]),
    )
