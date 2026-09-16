# -*- coding: utf-8 -*-
"""The four service pages."""
from common import (BIZ, breadcrumbs, crumb_html, cta_final, faq_html, faq_schema,
                    img, page, _j)


def service_schema(name, desc, path, low, unit):
    offer = ''
    if low:
        offer = (',"offers":{"@type":"Offer","priceCurrency":"CAD","price":"%s",'
                 '"priceSpecification":{"@type":"UnitPriceSpecification","price":"%s",'
                 '"priceCurrency":"CAD","unitText":"%s"}}' % (low, low, unit))
    return ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Service",'
            '"name":%s,"description":%s,"url":"%s%s","serviceType":%s,'
            '"provider":{"@id":"%s/#org"},"areaServed":{"@type":"State","name":"Ontario"}%s}</script>'
            % (_j(name), _j(desc), BIZ["base"], path, _j(name), BIZ["base"], offer))


def shell(path, h1, kicker, lede, hero_img, hero_alt, ratio, crumbs, sections,
          title, desc, faqs, schema_name, schema_desc, price, unit, og, current):
    phero = """<section class="phero">
<div class="phero__media">{im}</div>
<div class="wrap">
{cr}
<p class="hero__kicker">{k}</p>
<h1>{h1}</h1>
<p class="lede">{lede}</p>
<div class="hero__cta">
<a class="btn" href="/contact.html"><span>Get a quote</span></a>
<a class="btn btn--ghost" href="tel:{tel}"><span>Call dispatch {phone}</span></a>
</div>
</div>
</section>""".format(im=img(hero_img, *hero_alt, ratio=ratio), cr=crumb_html(crumbs),
                     k=kicker, h1=h1, lede=lede, tel=BIZ["phone_tel"], phone=BIZ["phone_ui"])

    faq_sec = """<section class="alt">
<div class="wrap">
<div class="rail">
<div class="rail__label">Straight answers<span>What people ask before they book this, and what we actually tell them.</span></div>
<div><h2>Questions worth<br>asking us.</h2>
<div style="margin-top:34px">{f}</div></div>
</div>
</div>
</section>""".format(f=faq_html(faqs))

    body = phero + "".join(sections) + faq_sec + cta_final()
    return page(path=path, title=title, desc=desc, body=body, current=current, og=og,
                schema=(service_schema(schema_name, schema_desc, path, price, unit)
                        + breadcrumbs(crumbs)
                        + faq_schema([(q, _plain(a)) for q, a in faqs])))


def _plain(html):
    import re
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def rail(label, blurb, h2, inner, alt=False, extra=""):
    return """<section class="{cls}">
<div class="wrap">
<div class="rail">
<div class="rail__label">{label}<span>{blurb}</span></div>
<div><h2>{h2}</h2>{inner}</div>
</div>
</div>
</section>""".format(cls=("alt" if alt else "") + extra, label=label, blurb=blurb, h2=h2, inner=inner)


def cards(items, cols=2):
    body = "".join('<div class="card"><h3>%s</h3><p>%s</p></div>' % (t, d) for t, d in items)
    return '<div class="cards cards--%d" style="margin-top:38px">%s</div>' % (cols, body)


def kv(rows):
    body = "".join('<div class="kv__row"><dt>%s</dt><dd>%s</dd></div>' % (a, b) for a, b in rows)
    return '<dl class="kv" style="margin-top:34px">%s</dl>' % body


# ===========================================================================
# 1. Venue & door security
# ===========================================================================
VENUE_FAQ = [
    ("How many door staff does a bar in Ontario actually need?",
     "<p>There is no single provincial ratio for licensed premises, so it comes down to your occupancy load, your "
     "licence conditions, your layout and your history. A workable starting point for a late-night room is one "
     "officer per 75&ndash;100 patrons, plus a dedicated ID position once there is a line and one floor officer per "
     "distinct area &mdash; patio, mezzanine, back bar.</p>"
     "<p>We size it from your floor plan rather than a formula, and we will tell you if you are over-staffed. "
     "Selling you two guards you do not need is a short conversation and a lost client.</p>"),
    ("Can your door staff refuse entry and remove people?",
     "<p>Yes, within the law. Licensed guards acting for an occupier can refuse entry, ask someone to leave, and use "
     "reasonable force to remove a trespasser who will not go. What they cannot do is detain someone as punishment, "
     "search a patron without consent, imply they are police, or continue force once a person is compliant.</p>"
     "<p>Our post orders spell out exactly where that line is for your room, and every refusal and ejection is logged "
     "with a reason and a time. That log is what protects your licence.</p>"),
    ("Will it be the same people every week?",
     "<p>That is the whole model. You get a named lead and a core crew who work your nights, know your regulars and "
     "your staff, and hand over to each other properly. When someone is off, cover is arranged from the same pool "
     "and briefed by the lead &mdash; you will not meet a stranger on a Saturday at 21:00.</p>"),
    ("Do you carry naloxone?",
     "<p>On every venue shift. Officers hold current Standard First Aid and CPR-C, and naloxone is carried and "
     "checked. If it is used, it is in the report that night, along with the time EMS was called.</p>"),
    ("What does it cost to put door staff on for a weekend?",
     "<p>From $38 per hour per licensed guard with a four-hour minimum. A typical Friday and Saturday for a "
     "200&ndash;300 capacity room &mdash; three officers, 21:00 to 03:00 &mdash; lands around $1,400 for the weekend. "
     "Recurring weekly bookings are quoted at a flat rate so you can budget.</p>"),
]

VENUE = shell(
    path="/services/venue-security.html",
    current="/services/venue-security.html",
    h1="Door staff who<br>know your room.",
    kicker="Bars · nightclubs · lounges · restaurants",
    lede="Licensed door and floor officers for licensed premises across the GTA. The same crew every week, an ID "
         "position that keeps the line moving, and a refusal log that holds up when the AGCO asks.",
    hero_img="crew-wide",
    hero_alt=([640, 900, 1200, 1600], "100vw", "Swarm door staff at a licensed venue in Toronto"),
    ratio=16 / 9,
    crumbs=[("Home", "/"), ("Venue security", "/services/venue-security.html")],
    title="Nightclub & Bar Security Toronto | Licensed Door Staff",
    desc="PSISA-licensed door and floor staff for Toronto and GTA bars, nightclubs and lounges. Same crew "
         "weekly, written report every shift. From $38/hr.",
    og="/assets/og/og-venue.jpg",
    schema_name="Venue and door security",
    schema_desc="Licensed door and floor security for bars, nightclubs, lounges and restaurants across the "
                "Greater Toronto Area.",
    price="38", unit="HUR",
    faqs=VENUE_FAQ,
    sections=[
        rail("The problem", "Most venues do not lose their licence over a fight. They lose it over the paperwork "
                            "that did not exist afterwards.",
             "A bad door costs<br>more than a bad night.",
             """<div class="stack" style="margin-top:30px">
<p class="lede">A slow ID check builds the crowd that becomes the incident. An ejection done badly becomes a phone
video. A night with no written record becomes your word against a claim, eighteen months later, in front of
someone who was not there.</p>
<p class="lede">The door is not where you save money. It is the only position in your venue that decides who is
inside for the next six hours.</p>
</div>"""),
        rail("What we run", "Every position is defined in writing before the first shift and agreed with your manager.",
             "The positions<br>we hold.",
             cards([
                 ("Door and ID",
                  "Speed matters more than theatre. Correct ID checks, clean refusals with a stated reason, and a line "
                  "that keeps moving so it never turns into its own problem."),
                 ("Capacity and count",
                  "A running count against your licensed occupancy, held legal at peak. If the number is wrong when an "
                  "inspector walks in, nothing else you did that night matters."),
                 ("Floor and patio",
                  "Officers moving, not posted like statues. Watching for over-service, drink tampering, the table that "
                  "is getting loud, and the person who has been alone too long."),
                 ("Close and clear",
                  "Inside-out clear at last call, sidewalk kept moving, rideshare corner watched, and we stay until your "
                  "staff have cashed out and the door is locked."),
             ], cols=2), alt=True),
        rail("Standards", "The credentials your insurer, your landlord and the AGCO will each ask about.",
             "What every officer<br>on your door holds.",
             kv([
                 ("Ontario PSISA security guard licence", "Current, digital, carried on shift"),
                 ("Ministry-approved training", "40 hours + provincial exam"),
                 ("Criminal Record and Judicial Matters Check", "Required at every renewal"),
                 ("Standard First Aid and CPR-C", "Current"),
                 ("Naloxone", "Carried on venue shifts"),
                 ("De-escalation and use-of-force refresher", "Twice a year"),
                 ("Commercial general liability", "$5M, certificate on request"),
                 ("WSIB", "Full coverage, cleared"),
             ]) + '<div style="margin-top:34px"><a class="tlink" href="/about.html">'
                  '<span>How we hire and train</span></a></div>'),
        """<section class="band">
<div class="band__media">%s</div>
<div class="wrap">
<h2>Your regulars should<br>never learn our names.</h2>
<p class="lede" style="margin-top:26px">The best compliment a door crew gets is that nobody noticed them. We are
large, visible and unmistakable at the entrance &mdash; and almost invisible once you are inside, because the
work has already been done by standing in the right place at the right time.</p>
<div class="hero__cta"><a class="btn" href="/contact.html"><span>Book a walk-through</span></a></div>
</div>
</section>""" % img("hall-tall", [640, 900], "100vw", "Swarm officers in a venue corridor", ratio=9 / 16),
    ],
)

# ===========================================================================
# 2. Event security
# ===========================================================================
EVENT_FAQ = [
    ("How many guards do I need for my event?",
     "<p>The honest answer is that it depends on far more than headcount &mdash; alcohol, ticketing, entry points, "
     "cash on site, whether the artist has a following that turns up without tickets, and whether the venue has one "
     "exit or six.</p>"
     "<p>As a starting frame: roughly one officer per 100 guests at a controlled private event, one per 75 where "
     "alcohol is served late, plus dedicated positions for each entry, the cash or bar area, and back-of-house. "
     "Send us the floor plan and the run sheet and we will size it properly and in writing.</p>"),
    ("Do you work weddings?",
     "<p>Regularly, and it is not the job people expect. Wedding work is gift-table and envelope security, managing "
     "an uninvited guest without a scene in front of 200 people, keeping the bar from becoming the problem at "
     "23:00, and getting elderly relatives to their cars safely. Suits, not bomber jackets.</p>"),
    ("Can you handle access control, wristbands and VIP?",
     "<p>Yes &mdash; ticket and accreditation checks, wristband or lanyard tiers, guest-list management at the door, "
     "green room and VIP access, and a controlled artist route from vehicle to stage. We run it off your list, not "
     "off whoever shouts loudest at the barrier.</p>"),
    ("How far in advance should I book?",
     "<p>One to three weeks for most events so we can walk the site and build a real staffing plan. Large or "
     "multi-day events want a month. We will still take the Thursday call for a Saturday if we have the crew &mdash; "
     "dispatch is answered 24 hours &mdash; but the plan is better when the site visit happens.</p>"),
    ("Do you provide security for film and production?",
     "<p>Yes: set and basecamp security, equipment and vehicle watch, location lock-up overnight, crowd and "
     "pedestrian management around an active shot, and talent protection where it is needed. Quoted per day with "
     "overnight rates stated up front.</p>"),
]

EVENT = shell(
    path="/services/event-security.html",
    current="/services/event-security.html",
    h1="Your event runs.<br>We handle the rest.",
    kicker="Concerts · festivals · weddings · corporate · film",
    lede="Licensed event security across the GTA, built from your floor plan rather than a template. Access control, "
         "crowd flow, VIP and artist movement, and one named lead who answers for the whole night.",
    hero_img="crew-cine",
    hero_alt=([900, 1200, 1600], "100vw", "Swarm event security crew"),
    ratio=21 / 9,
    crumbs=[("Home", "/"), ("Event security", "/services/event-security.html")],
    title="Event Security Toronto & GTA | Concerts, Weddings | Swarm",
    desc="Licensed event security guards across Toronto and the GTA — concerts, festivals, weddings, corporate "
         "and film. From $42/hr per guard. Dispatch 24 hours.",
    og="/assets/og/og-event.jpg",
    schema_name="Event security",
    schema_desc="Licensed event security staffing for concerts, festivals, private events, weddings, corporate "
                "functions and film production across the Greater Toronto Area.",
    price="42", unit="HUR",
    faqs=EVENT_FAQ,
    sections=[
        rail("The work", "Six event types, one method: plan the site, define the posts, name the lead, write the report.",
             "What we cover.",
             cards([
                 ("Concerts and club nights",
                  "Barrier and pit, artist route from vehicle to stage, green room control, merch and cash positions, "
                  "and a load-out that does not turn into a scrum."),
                 ("Festivals and outdoor events",
                  "Perimeter and gate, wristband tiers, vendor and compound security, overnight site watch, and "
                  "crowd-flow planning done before the gates open, not at the gate."),
                 ("Weddings and private functions",
                  "Suited, quiet, and briefed on who matters. Gift table, guest list, the uninvited guest handled "
                  "away from the room, and safe departures at the end."),
                 ("Corporate and conferences",
                  "Reception and badge control, executive floors, AGM and town-hall coverage, and discreet removal "
                  "of a disruptive attendee without it becoming the story of the day."),
                 ("Film, TV and production",
                  "Basecamp and set security, equipment watch, overnight lock-up, pedestrian and traffic control "
                  "around a live shot, and talent protection when the location leaks."),
                 ("Pop-ups, launches and galleries",
                  "Door list, capacity, high-value product watch, and staff who can hold a door politely in front of "
                  "a queue of people who all believe they are on the list."),
             ], cols=3), alt=True),
        rail("The plan", "You get all of this in a document before the event, not a verbal on the day.",
             "What lands in<br>your inbox first.",
             """<div class="steps" style="margin-top:38px">
<div class="step"><h3>Site plan and post map</h3><p>Every position marked on your floor plan, with sightlines,
entry and egress, and the route we will use to move someone out without crossing the room.</p></div>
<div class="step"><h3>Post orders and escalation</h3><p>What each officer does, what they never do, who they call,
and the exact point at which police or EMS are contacted rather than debated.</p></div>
<div class="step"><h3>One named lead</h3><p>A mobile number for a person, not a dispatch line. Your event manager
talks to one human all night and gets the report from the same one.</p></div>
</div>"""),
        """<section class="band">
<div class="band__media">%s</div>
<div class="wrap">
<h2>The crowd decides<br>in the first ten minutes.</h2>
<p class="lede" style="margin-top:26px">How an event feels for six hours is set by what happens at the gate in
the first ten minutes. A queue that moves, a check that is quick and correct, and staff who look like they have
done this before &mdash; that is the whole tone of the night, and it is almost entirely a staffing decision.</p>
<div class="hero__cta"><a class="btn" href="/contact.html"><span>Send us your run sheet</span></a></div>
</div>
</section>""" % img("crew-hall", [640, 900, 1200, 1600], "100vw",
                    "Swarm crew at an event entrance", ratio=16 / 10),
        rail("Rates", "Indicative. Final numbers come from the site plan, not the phone call.",
             "What events<br>usually cost.",
             kv([
                 ("Licensed event guard", "from $42/hr"),
                 ("Supervisor / named lead", "from $55/hr"),
                 ("Suited close-protection agent on an event", "from $95/hr"),
                 ("Overnight site and equipment watch", "from $40/hr"),
                 ("Minimum booking", "4 hours per officer"),
                 ("Statutory holidays and New Year's Eve", "Quoted separately"),
             ]) + '<p class="sub" style="margin-top:20px">Travel outside the GTA is quoted up front. '
                  'Recurring events are placed on a flat weekly or monthly rate.</p>'),
    ],
)

# ===========================================================================
# 3. Close protection
# ===========================================================================
CP_FAQ = [
    ("What does a close protection detail actually involve?",
     "<p>Most of it happens before you see anybody. Advance work on the venues and routes, checking arrival and "
     "departure points, agreeing a schedule with your assistant, identifying where you are exposed and building a "
     "plan that removes it quietly.</p>"
     "<p>On the day it looks like one or two people who arrive before you, stay close without crowding, manage the "
     "vehicle and the entrance, and leave when you do. If it looks dramatic, it has been done badly.</p>"),
    ("Will it be obvious that I have security?",
     "<p>Only if you want it to be. Visible deterrence is sometimes the point &mdash; a large suited agent at the "
     "door changes behaviour before anything starts. Where discretion matters more, agents dress to the room, keep "
     "distance, and read as part of your party rather than a detail.</p>"
     "<p>We agree the posture with you in advance and we do not change it to look impressive.</p>"),
    ("Do close protection agents in Ontario carry firearms?",
     "<p>No. Under the federal <em>Firearms Act</em>, an Authorization to Carry is issued almost exclusively for the "
     "protection of cash, valuables and goods of substantial value in transit. It is not available for personal "
     "bodyguard work in Canada, and any firm telling you otherwise is selling you a legal problem.</p>"
     "<p>What actually protects a principal here is advance work, positioning, vehicle discipline, and people who "
     "are large, calm and trained. See <a href=\"/services/high-risk.html\">high-risk work</a> for what is lawfully "
     "available at the top end.</p>"),
    ("Can you cover a family, not just one person?",
     "<p>Yes. Residential coverage, school runs, a spouse travelling separately, and children's routines &mdash; "
     "handled by the same agents each time so your family is not meeting a stranger at the door. Discretion around "
     "children is briefed specifically and taken seriously.</p>"),
    ("What is the minimum booking?",
     "<p>Eight hours per agent, from $95 per hour. Multi-day and touring work is quoted as a flat daily rate with "
     "travel and accommodation stated in advance. Short-notice overnight coverage is available through 24-hour "
     "dispatch.</p>"),
]

CP = shell(
    path="/services/close-protection.html",
    current="/services/close-protection.html",
    h1="Protection that<br>reads as staff.",
    kicker="Executive · personal · family · visiting talent",
    lede="Close protection across the GTA for executives, artists, athletes and private clients. Advance work on "
         "every venue and route, discreet agents who dress to the room, and a detail that is felt rather than seen.",
    hero_img="lot-wide",
    hero_alt=([640, 900, 1200], "100vw", "Swarm close protection agents at a vehicle at night"),
    ratio=16 / 9,
    crumbs=[("Home", "/"), ("Close protection", "/services/close-protection.html")],
    title="Close Protection & Bodyguards Toronto | Swarm Protective",
    desc="Licensed close protection and executive bodyguards in Toronto and the GTA. Advance work, secure "
         "arrivals, discreet agents. From $95/hr per agent.",
    og="/assets/og/og-cp.jpg",
    schema_name="Close protection",
    schema_desc="Executive and personal close protection, secure transport and residential coverage across the "
                "Greater Toronto Area.",
    price="95", unit="HUR",
    faqs=CP_FAQ,
    sections=[
        rail("Who calls us", "Four situations that account for most of our protection work.",
             "When people<br>pick up the phone.",
             cards([
                 ("Executives and public-facing leadership",
                  "Board meetings that will not go well, a termination that needs a witness, an AGM with a known "
                  "attendee, or an address that has appeared on the internet."),
                 ("Artists, athletes and visiting talent",
                  "Airport to hotel to venue to hotel, green room control, meet-and-greet management, and a route out "
                  "of the building that was walked before the show started."),
                 ("Private clients and families",
                  "Residential coverage, school runs, an ex-partner who has stopped taking the hint, and travel where "
                  "one member of the family is exposed and the others are not."),
                 ("High-value movement",
                  "Jewellery, art, cash and documents moving between locations. See "
                  "<a href=\"/services/high-risk.html\">high-risk work</a> for the assessed end of this."),
             ], cols=2), alt=True),
        rail("The method", "Protection is a planning job that occasionally becomes a physical one.",
             "Most of the work<br>happens before<br>you see anyone.",
             """<div class="night" style="margin-top:38px">
<div class="night__row"><div class="night__t">Brief</div><div class="night__b">
<h4>We take the schedule and find the exposure in it</h4>
<p>Where you are predictable, where you are static, where you are alone, and who already knows all three.
A short conversation with you or your assistant, and nothing on paper that should not be.</p></div></div>
<div class="night__row"><div class="night__t">Advance</div><div class="night__b">
<h4>Every venue and route is walked first</h4>
<p>Entrances, exits, lifts, the quiet way out, where the car waits, and what the building's own security will
and will not do. We arrive somewhere for the first time before you do, not with you.</p></div></div>
<div class="night__row"><div class="night__t">Detail</div><div class="night__b">
<h4>Agents dress to the room and hold distance</h4>
<p>Close enough to act, far enough that you are not performing having security. Arrivals and departures managed,
vehicle kept in the right place, and a hand on the door before you reach it.</p></div></div>
<div class="night__row"><div class="night__t">Close</div><div class="night__b">
<h4>You get a written record of anything that mattered</h4>
<p>Incidents, approaches, anyone who turned up twice, plates that appeared more than once. It is the record that
turns a bad feeling into something a lawyer or the police can act on.</p></div></div>
</div>"""),
        """<section class="band">
<div class="band__media">%s</div>
<div class="wrap">
<h2>Discretion is a<br>skill, not a suit.</h2>
<p class="lede" style="margin-top:26px">Anyone can stand near you in black. The job is reading a room fast enough
to move you before it changes, ending an approach in a way the person walks away from feeling fine about, and
never becoming the reason people are looking in your direction.</p>
<div class="hero__cta"><a class="btn" href="/contact.html"><span>Arrange a confidential call</span></a></div>
</div>
</section>""" % img("lot-tall", [560, 760, 1000], "100vw",
                    "Close protection agents beside a vehicle in a parking structure", ratio=3 / 4),
    ],
)

# ===========================================================================
# 4. High-risk & armed-capable
# ===========================================================================
HR_FAQ = [
    ("Can I hire an armed bodyguard in Ontario?",
     "<p>No, and we would rather lose the booking than pretend otherwise. Carrying a restricted firearm in Canada "
     "requires a federal Authorization to Carry, and the regulations issue it for the handling, transportation or "
     "protection of cash, negotiable instruments and other goods of substantial value &mdash; not for personal "
     "protection.</p>"
     "<p>If your risk genuinely needs more than a protective detail can lawfully deliver, that is a police matter "
     "and we will help you take it to them properly, with a documented record of what has been happening.</p>"),
    ("So what does armed-capable mean on this page?",
     "<p>It means we can staff assignments where an Authorization to Carry lawfully applies &mdash; primarily the "
     "movement and protection of cash and high-value goods &mdash; using officers who hold the required federal "
     "authorization and firearms licensing, with the Ministry notified as the PSISA requires.</p>"
     "<p>Everything else is unarmed and deliberately so. We will tell you which category your job falls into before "
     "we quote it.</p>"),
    ("What is in a threat assessment?",
     "<p>What has happened so far and when, who is involved, what they have access to, what they have said or "
     "posted, where you are predictable, what has already been reported to police, and what would have to be true "
     "for this to escalate.</p>"
     "<p>It ends with a written recommendation: what coverage we suggest, what it will cost, what you should change "
     "yourself, and &mdash; sometimes &mdash; that you do not need us.</p>"),
    ("Will you turn work down?",
     "<p>Yes. We decline anything that cannot be done lawfully, anything that looks like intimidation or debt "
     "collection dressed up as security, and anything where a client wants presence in order to start something "
     "rather than stop it. We also decline jobs where the honest answer is that you need the police, not a guard.</p>"),
    ("How quickly can a high-risk detail be stood up?",
     "<p>Triage the same day, always. A short-term protective detail can normally be placed within 24 hours while "
     "the full assessment is completed in parallel &mdash; we do not leave someone uncovered while paperwork is "
     "written.</p>"),
]

HR = shell(
    path="/services/high-risk.html",
    current="/services/high-risk.html",
    h1="When an ordinary<br>guard is the<br>wrong answer.",
    kicker="Threat-assessed details · valuables in transit · armed-capable",
    lede="Assessed protective work for situations that have already escalated, and lawful armed coverage where the "
         "federal authorization genuinely applies. Written assessment before we quote. Declined if it cannot be "
         "done lawfully.",
    hero_img="lot-cine",
    hero_alt=([900, 1200], "100vw", "Swarm protective detail at night"),
    ratio=21 / 9,
    crumbs=[("Home", "/"), ("High-risk and armed-capable", "/services/high-risk.html")],
    title="High-Risk & Armed-Capable Security Toronto | Swarm",
    desc="Threat-assessed protective details, valuables and cash-in-transit coverage, and lawful armed-capable "
         "staffing in Ontario. Written threat assessment before quote. 24-hour triage.",
    og="/assets/og/og-highrisk.jpg",
    schema_name="High-risk protective detail",
    schema_desc="Threat-assessed protective details, high-value transport and lawful armed-capable security "
                "staffing in Ontario.",
    price="", unit="",
    faqs=HR_FAQ,
    sections=[
        """<section>
<div class="wrap">
<div class="rail">
<div class="rail__label">Read this first<span>The one page on this site where we would rather be accurate than
impressive.</span></div>
<div>
<h2>The law on armed<br>security in Ontario,<br>without the spin.</h2>
<div class="note" style="margin-top:34px">
<p><b>Bodyguards in Canada do not carry firearms.</b> A restricted firearm may only be carried with a federal
Authorization to Carry, and the <em>Authorizations to Carry Restricted Firearms and Certain Handguns Regulations</em>
issue it for the handling, transportation or protection of cash, negotiable instruments or other goods of
substantial value &mdash; not for protecting a person going about their day.</p>
<p>Any GTA company advertising armed bodyguards for your event or your family is either wrong or lying, and either
way you do not want them holding your liability. We would rather tell you this on a public page and lose the
enquiry.</p>
</div>
<p class="lede" style="margin-top:30px">What we do instead is build the coverage that is lawful, effective and
documented &mdash; and tell you honestly when the thing you actually need is a police report and a lawyer, not a
guard on a chair.</p>
</div>
</div>
</div>
</section>""",
        rail("Where this applies", "Four categories. Each one is assessed before it is priced.",
             "What we take on.",
             cards([
                 ("Escalated personal threat",
                  "Stalking, a persistent ex-partner, a former employee who has not moved on, or a dispute that has "
                  "already reached someone's home. Assessed, documented, and coordinated with police reporting."),
                 ("Valuables and cash in transit",
                  "Jewellery, bullion, art, collections and cash moving between locations. This is the narrow category "
                  "where Canadian law does contemplate armed protection, and where we can staff it lawfully."),
                 ("Hostile terminations and site disputes",
                  "A dismissal that needs witnesses, a locked-out contractor, a site with an ongoing dispute. Presence, "
                  "documentation, and nobody escalating on our side."),
                 ("Residential hardening",
                  "Overnight coverage at a home while an assessment runs, combined with practical fixes &mdash; "
                  "lighting, cameras, routine changes &mdash; that reduce the exposure permanently."),
             ], cols=2), alt=True),
        rail("How it starts", "No quote until there is an assessment. No assessment until we have spoken to you.",
             "Assessment first,<br>always.",
             """<div class="steps" style="margin-top:38px">
<div class="step"><h3>Same-day triage call</h3><p>Thirty minutes, confidential. What has happened, when it started,
what is already reported, and whether anyone needs cover tonight while we work.</p></div>
<div class="step"><h3>Written threat assessment</h3><p>Findings, exposure points, a recommended posture, the cost,
and what you should change regardless of whether you hire us.</p></div>
<div class="step"><h3>Detail placed, or referred</h3><p>If we are the right answer we place a named team. If you
need police, a lawyer or a technical fix instead, we will say so and help you get there.</p></div>
</div>""" + '<div style="margin-top:34px"><a class="tlink" href="/contact.html">'
            '<span>Start a confidential triage call</span></a></div>'),
    ],
)

PAGES = {
    "services/venue-security.html": VENUE,
    "services/event-security.html": EVENT,
    "services/close-protection.html": CP,
    "services/high-risk.html": HR,
}
