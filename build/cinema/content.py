# -*- coding: utf-8 -*-
"""Every word on the home page, in one file. Edit here, then rebuild.

The rule for this page is fewer words, not smaller type: one heading and a
line or two per screen, because most visitors arrive on a phone from Instagram,
TikTok or a search result and decide in seconds.

Anything whose first field starts with PLACEHOLDER shows a clean empty tile.
Replace it with real content and it renders as a real card.
"""

HOME = {
    "line": "Licensed security service",           # the client's words, kept as written
    "quote": "Get a quote",
    "call": "Call",
}

SERVICES = {
    "kicker": "What we do",
    "items": [
        ("Event security", "Concerts, weddings, galas"),
        ("Venue security", "Bars, clubs, lounges"),
        ("Close protection", "Executives, artists, families"),
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

CONTACT = {
    "h": "Get a quote",
    "line": "Tell us the date, the place and the headcount. We reply the same day.",
    "note": "Answered 24/7",
    "send": "Send request",
}
