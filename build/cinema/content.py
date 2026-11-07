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
    "motto": "Life is unpredictable, let us protect you",   # the client's motto (schema slogan)
    # the hero turns the motto into a promise (brand-copy scorecard 10/12; runner-up
    # "Nothing happened. That's the job." 11/12, used as the Meet us statement)
    "headline": ("Life is unpredictable.", "We plan for it."),
    "sub": "Discreet, trained security for venues, events and private clients across Toronto and the GTA.",
    "gold": "protect",                              # the one word of the motto set in gold
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

# Meet us: the statement (deck slide 2), lit word by word
# was "Peace of mind is our product. We deliver it through proactive planning, skilled
# communication, and unyielding professionalism." (the client's; "peace of mind" is banned by
# the brand voice). Same idea, said as the brand line.
STATEMENT = "You look after your guests. We look after their safety."
STATEMENT_LINE = "Every job starts with a plan, so your event runs the way you expect it to."

# Home: how it works (deck slide 6)
STEPS = {
    "h": "How a booking works",
    # the client's deck said "Initial consultation / Customized service plan / Professional
    # execution"; same three steps, in plain words (2026-11 copy pass)
    "items": [
        ("Tell us what you need", "Share the date, the place, the number of guests and anything that worries you."),
        ("We plan it with you", "We work out where our officers stand, how people arrive and leave, and who leads on the day."),
        ("We look after it on the day", "One team lead stays on site the whole time and keeps in touch with you."),
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
    "h": "Common questions",
    "items": [
        ("Where do you work?",
         "We work across Toronto and 17 nearby cities in the GTA. We can also travel with you anywhere in Canada."),
        ("Are your officers licensed?",
         "Yes. Every officer we send is licensed to work in security in Ontario and trained to calm tense "
         "situations rather than escalate them."),
        ("Are your bodyguards armed?",
         "No. Private security officers in Ontario are not allowed to carry firearms. We keep people safe "
         "through careful planning, a steady presence and calm communication."),
        ("What can you cover?",
         "Close protection, events, venues, party buses, limousine trips, and patrols for homes and businesses. "
         "If you are not sure which fits, tell us what is happening and we will suggest the right option."),
        ("How soon can you start?",
         "For most jobs we can start the same day. Large events and travel need a few days so we can plan "
         "them properly."),
        ("How do I book you?",
         "Send us the date, the place and roughly how many people will be there. We usually reply with a clear "
         "quote the same day."),
    ],
}


CONTACT = {
    "h": "Get a quote",
    "line": "Tell us the date, the place and the headcount. We reply the same day.",
    "note": "Answered 24/7",
    "send": "Send request",
}
