# -*- coding: utf-8 -*-
"""Every word on the home page, in one file.

Edit here and rebuild — nothing in `docs/` is written by hand. Anything marked
PLACEHOLDER is waiting on the client; the build shows those blocks only in
preview mode, so a half-filled section never reaches the public site.
"""
from common import BIZ

# --------------------------------------------------------------------------
# 1. hero — the five-second test: what is this, is it for me, what do I do
# --------------------------------------------------------------------------
HERO = {
    "h": "Everything under control.",
    "sub": "Licensed door staff, event security and close protection across Toronto "
           "and the GTA. De-escalation first, the same crew every week, and a written "
           "report before we leave.",
    "cta": "Request a quote",
    "note": "Dispatch answered 24 hours &middot; most quotes back the same day",
}

# the band that sits directly under the fold, where doubt starts
PROOF = [
    "PSISA-licensed officers",
    "$5M liability insurance",
    "WSIB covered",
    "First aid &amp; CPR-C current",
    "Naloxone on venue shifts",
    "Serving 18 GTA municipalities",
]

# --------------------------------------------------------------------------
# 2. what we provide
# --------------------------------------------------------------------------
SERVICES = [
    {
        "id": "venues",
        "kicker": "Bars, nightclubs and lounges",
        "h": "Door staff who protect your licence.",
        "line": "The same faces every week, so your regulars and your staff know them.",
        "points": [
            "IDs checked by hand, headcount kept all night",
            "Capacity and last call handled the way your licence requires",
            "Written incident report before the doors are locked",
        ],
    },
    {
        "id": "events",
        "kicker": "Events, weddings and corporate",
        "h": "Guests never meet the problem.",
        "line": "Suited officers who read as staff, not as a barrier to your night.",
        "points": [
            "Guest list at the entrance, gatecrashers turned around quietly",
            "Gift table, bar and back-of-house covered as posts, not guesses",
            "One lead holding no post, running the floor and talking to you",
        ],
    },
    {
        "id": "protection",
        "kicker": "Close protection",
        "h": "The route is walked before you arrive.",
        "line": "For artists, executives, families and anyone who needs to get home quietly.",
        "points": [
            "Advance work on the venue, the route and every exit",
            "Discreet detail — a suit in the room, not a scene in the room",
            "Staff walked to their cars and cash escorted after close",
        ],
    },
]

# --------------------------------------------------------------------------
# 3. the objection nobody says out loud: "will the guards be the problem?"
# --------------------------------------------------------------------------
STANCE = {
    "kicker": "How we work",
    "h": "We talk first.",
    "line": "Size gets us listened to. Training is why we rarely need it. Our officers "
            "are hired for temperament and re-certified on de-escalation twice a year — "
            "not once when they were hired.",
    "points": [
        ("Nobody's night ends on someone's phone",
         "The job is to make the incident small and boring. Hands stay down until "
         "there is no lawful alternative, and every contact is documented."),
        ("Licences carried, shown on request",
         "Every officer holds a current PSISA licence and carries it on shift. Ask any "
         "of them and they will show you."),
        ("Real people, not a uniform",
         "Door staff who talk to your regulars, remember names, and hand you the room "
         "back at the end of the night."),
    ],
}

# --------------------------------------------------------------------------
# 4. how it works — three steps, because effort is a conversion lever
# --------------------------------------------------------------------------
STEPS = [
    ("Tell us the night",
     "Date, place and headcount is enough. Dispatch is answered 24 hours, "
     "and most quotes come back the same day."),
    ("Walk-through and a written plan",
     "We count the posts, size the team and name the lead who will run it. "
     "You get it in writing with the number, before anyone is booked."),
    ("The shift, then the report",
     "The crew arrives early and works the plan. The incident report is written "
     "before they leave your building."),
]

# --------------------------------------------------------------------------
# 5. one night — the film. Four beats, one camera, then back to business.
#    Set SHOW_FILM = False and the section disappears; nothing else changes.
# --------------------------------------------------------------------------
SHOW_FILM = True
FILM_INTRO = {
    "kicker": "One night",
    "h": "What it looks like when it works.",
    "line": "Four moments from an ordinary Saturday. Nothing in it made the news, "
            "which is the point.",
}
BEATS = [
    {"id": "beat-door", "plate": "door", "time": "22:15", "label": "The door",
     "h": "Most trouble never gets in.",
     "line": "Two officers on the door, IDs by hand, and a headcount that is still right at 1 a.m."},
    {"id": "beat-floor", "plate": "floor", "time": "00:40", "label": "The floor",
     "h": "Two voices up. Nobody touched.",
     "line": "A quiet word, two angles, and the room never notices it happened."},
    {"id": "beat-exit", "plate": "exit", "time": "02:10", "label": "The exit",
     "h": "Out the back, into the car.",
     "line": "The exit was planned before the doors opened — and the staff get walked to their cars."},
    {"id": "beat-report", "plate": "dawn", "time": "06:00", "label": "The report",
     "h": "You slept. We wrote it down.",
     "line": "Refused at the door 4 &middot; settled without contact 1 &middot; injuries 0 &middot; police called 0."},
]

# --------------------------------------------------------------------------
# 6. proof that will be real soon — PLACEHOLDERS
#    Fill these in and they publish. Empty, they only show in preview.
# --------------------------------------------------------------------------
TESTIMONIALS = [
    # ("Quote from the client, one or two sentences.", "Name", "Role, venue")
    ("PLACEHOLDER — a venue owner on what changed after the crew started.",
     "Name", "Owner, venue name"),
    ("PLACEHOLDER — an event planner on the wedding or gala you covered.",
     "Name", "Planner, company"),
    ("PLACEHOLDER — a client on close protection, discretion, getting home.",
     "Name", "Client"),
]

TEAM = [
    # (name, role, one line, photo filename in assets/img/)
    ("PLACEHOLDER", "Operations lead", "Years on the door, what they are known for.", ""),
    ("PLACEHOLDER", "Venue lead", "Which rooms they run and what they are known for.", ""),
    ("PLACEHOLDER", "Close protection lead", "Background, training, languages.", ""),
]

TEAM_INTRO = {
    "kicker": "The crew",
    "h": "The people who turn up.",
    "line": "You get the same leads every week, and you get their names before the first shift.",
}

TESTIMONIAL_INTRO = {
    "kicker": "What clients say",
    "h": "Ask us for references.",
    "line": "We are collecting reviews from the venues we cover now. Until they are "
            "published here, we will put you on the phone with a client who runs a room "
            "like yours.",
}

# --------------------------------------------------------------------------
# 7. closing
# --------------------------------------------------------------------------
CLOSE = {
    "kicker": "Dispatch answered 24 hours",
    "h": "Tell us the night.",
    "line": "Date, place and headcount is enough to start. You get a written number and "
            "a named lead, usually the same day.",
}

COVERAGE_NOTE = ("Outside this list? Ask anyway — we travel for events and protection "
                 "details across the Golden Horseshoe.")
