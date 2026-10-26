# -*- coding: utf-8 -*-
"""Every word on the home page, in one file. Edit here, then rebuild.

The rule for this page is fewer words, not smaller type: one heading and a
line or two per screen, because most visitors arrive on a phone from Instagram,
TikTok or a search result and decide in seconds. The detail they ask for next
lives on the service pages (build/services.py), not here.

The motto and the licence line are the client's own words — leave them exactly
as they are written here.

Anything whose first field starts with PLACEHOLDER shows a clean empty tile.
Replace it with real content and it renders as a real card.
"""

HOME = {
    "line": "Licensed security service",           # the client's words, kept as written
    "where": "Toronto & the GTA",
    "motto": "Life is unpredictable, Let us Protect you",
    "gold": "Protect",                              # the one word of the motto set in gold
    "lede": "Close protection, event and venue security, party bus and limousine details, and monitoring.",
}

# (slug, name, one line, page strapline) — the slug is the detail page.
SERVICES = {
    "kicker": "What we do",
    "h": "Six ways we cover you",
    "items": [
        ("close-protection", "Close protection", "Executives, artists, families"),
        ("event-security", "Event security", "Concerts, weddings, galas"),
        ("venue-security", "Venue security", "Bars, clubs, lounges"),
        ("party-bus-security", "Party bus security", "Groups on the move"),
        ("limousine-service", "Limousine service", "Chauffeured, secured"),
        ("monitoring", "Monitoring", "Homes and businesses"),
    ],
    "creds": ["PSISA licensed", "$5M insured", "WSIB covered"],
    "more": "See what it includes",
}

WORK = {
    "kicker": "On the job",
    "left": ("At the door", "Same crew, every week"),
    "right": ("At your side", "Discreet. Suited. Trained."),
}

# The client's own words, from their review deck (SWARM Protection.pptx,
# October 2026). Keep them as written. Nothing here promises that the owners
# themselves attend a job — the client asked for that to stay off the site.

# Meet us: the standard (deck slide 1)
ELITE = {
    "kicker": "Why Swarm",
    "h": "The standard our people are held to",
    "items": [
        ("Continuously trained &amp; certified",
         "Our security personnel complete annual recertification and ongoing training, ensuring "
         "strict compliance with Ontario regulations and national Canadian industry standards."),
        ("Strategic resolution first",
         "Our team leads with articulate communication, situational awareness, and professional "
         "presence to control environments and resolve issues before they escalate."),
        ("Single point of command",
         "One dedicated Security Concierge manages your detail from start to finish, keeping "
         "communication streamlined and your team&rsquo;s operations completely synchronized."),
        ("Comprehensive shift logs",
         "Complete transparency from briefing to debrief. Meticulously maintained incident and "
         "shift reports are kept strictly on record and provided on demand for total accountability."),
    ],
}

# Home: who we are (deck slide 3)
PEOPLE = {
    "kicker": "Who we are",
    "h": "Canadian Owned. Canadian Operated. Trusted to Protect.",
    "line": "Swarm Protective Services combines extensive security experience with professional "
            "protection strategies to safeguard people, property, and operations.",
    "items": [
        ("Trained, Certified, Accountable",
         "Annual training and performance development ensure our personnel remain prepared to "
         "deliver professional security services in accordance with industry standards and "
         "client expectations."),
        ("Prevent, Defuse, and Control",
         "Control the environment. Communicate professionally. Maintain reactionary distance. "
         "Physical intervention is a last resort."),
        ("Observe &rarr; Respond &rarr; Report",
         "Every incident is documented accurately and promptly, ensuring operational "
         "accountability, investigative integrity, and a defensible record of events."),
    ],
}

# Meet us: the statement (deck slide 2), lit word by word
STATEMENT = ("Peace of mind is our product. We deliver it through proactive planning, skilled "
             "communication, and unyielding professionalism.")
STATEMENT_2 = ("After all, true security isn&rsquo;t measured by how a crisis is handled, "
               "it&rsquo;s measured by the total absence of one.")

# Home: how it works (deck slide 6)
STEPS = {
    "h": "Protection delivered in three steps",
    "items": [
        ("Initial consultation", "Discuss your security requirements and operational objectives."),
        ("Customized service plan", "Receive a tailored protection strategy and deployment plan."),
        ("Professional execution", "Trained personnel, dedicated oversight, and documented results."),
    ],
}

# Coverage: outside the GTA (deck slide 5)
TRAVEL = {
    "kicker": "Wherever protection is required, we deliver",
    "h": "Protection without boundaries.",
    "items": [
        ("Nationwide coverage", "Professional protection services across Canada."),
        ("Operational excellence", "Trained personnel. Proven performance."),
        ("One lead, one report", "One point of contact. One standard of protection."),
    ],
}

COVERAGE = {
    "kicker": "Coverage",
    "h": "Across the GTA",
    "line": "Toronto and 17 cities around it.",
    "national": "And we travel with you anywhere in Canada.",
    "inset_label": "Canada",
}

CREW = {
    "kicker": "The team",
    "h": "The crew",
    "line": "The people who turn up, and the nights they have covered.",
    # (name or title, role or place, image path under docs/ or "")
    "people": [
        ("PLACEHOLDER", "Operations lead", ""),
        ("PLACEHOLDER", "Venue lead", ""),
        ("PLACEHOLDER", "Close protection", ""),
    ],
    "events": [
        ("PLACEHOLDER", "Event photo", ""),
        ("PLACEHOLDER", "Event photo", ""),
        ("PLACEHOLDER", "Event photo", ""),
    ],
}

# Short, true answers to what people actually ask before they call. They are
# also what a search engine or an AI assistant quotes, so each answer stands on
# its own and the longer versions live on answers.html.
FAQ = {
    "kicker": "Questions",
    "h": "Asked before every booking",
    "more": "More answers",
    "items": [
        ("Where do you work?",
         "Toronto and 17 cities around it, and we travel with clients anywhere in Canada."),
        ("Are your officers licensed?",
         "Yes. PSISA-licensed officers, $5M insurance and WSIB coverage on every job."),
        ("Are your bodyguards armed?",
         "No. Ontario does not allow it. We work on presence, planning and de-escalation."),
        ("What can you cover?",
         "Close protection, events, venues, party buses, limousines, and monitoring for "
         "homes and businesses."),
        ("How soon can you start?",
         "Same day for most jobs. Large events and travel need a few days."),
        ("How do I book you?",
         "Send the date, the place and the headcount. We reply the same day."),
    ],
}

CONTACT = {
    "h": "Get a quote",
    "line": "Tell us the date, the place and the headcount. We reply the same day.",
    "note": "Answered 24/7",
    "send": "Send request",
}
