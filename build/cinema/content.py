# -*- coding: utf-8 -*-
"""Every word on the home page, in one file. Edit here, then rebuild.

The rule for this page is fewer words, not smaller type: one heading and a
line or two per screen, because most visitors arrive on a phone from Instagram,
TikTok or a search result and decide in seconds.

The motto and the licence line are the client's own words — leave them exactly
as they are written here.

Anything whose first field starts with PLACEHOLDER shows a clean empty tile.
Replace it with real content and it renders as a real card.
"""

HOME = {
    "line": "Licensed security service",           # the client's words, kept as written
    "motto": "Life is unpredictable, let us keep you protected",
    "quote": "Get a quote",
    "call": "Call",
}

SERVICES = {
    "kicker": "What we do",
    "items": [
        ("Event security", "Concerts, weddings, galas"),
        ("Venue security", "Bars, clubs, lounges"),
        ("Close protection", "Executives, artists, families"),
        ("Monitoring", "Homes and businesses"),
    ],
    "creds": ["PSISA licensed", "$5M insured", "WSIB covered"],
}

WORK = {
    "kicker": "On the job",
    "left": ("At the door", "Same crew, every week"),
    "right": ("At your side", "Discreet. Suited. Trained."),
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
         "Events, bars and clubs, close protection, and monitoring for homes and businesses."),
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
