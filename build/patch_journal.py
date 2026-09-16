# -*- coding: utf-8 -*-
"""One-shot migration of journal.py to the single-page structure.

- relative asset/link paths (depth 1)
- Swarm's own published rates removed; market ranges kept, since those are
  industry data rather than our price list
- cross-links now point at anchors on the single page
Safe to re-run: every replacement is idempotent.
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "journal.py")

s = io.open(SRC, encoding="utf-8").read()

REPLACEMENTS = [
    # --- imports / helpers -------------------------------------------------
    ("from common import BIZ, breadcrumbs, crumb_html, cta_final, img, page, _j",
     "from common import (BIZ, breadcrumbs, crumb_html, cta_final, img, page, _j)"),

    # --- kill Swarm's own published rates ----------------------------------
    ("<p>For reference, we quote from $38/hr for venue and door work, $42/hr for events and $95/hr per agent for close\n"
     "protection. We publish that because a client who cannot see a number cannot compare anything, and because a\n"
     "company that will only give you a price after a sales call is usually about to price you on what you look like\n"
     "you can afford.</p>",
     "<p>Those are market ranges, not a price list. We quote from a site plan rather than a phone call, because a\n"
     "300-capacity room with one exit and a 300-capacity room with six are not the same job at the same number.\n"
     "What you should insist on from anyone you ask is a written figure with a named lead attached to it.</p>"),

    ("<h3>A 250-capacity bar, Friday and Saturday</h3>\n"
     "<p>Three officers — one on ID, one on door, one on floor — 21:00 to 03:00, both nights. Twelve officer-shifts of\n"
     "six hours at $38 is roughly <strong>$1,370 per weekend</strong>, or about $5,900 a month on a flat recurring rate.\n"
     "For a room doing that kind of volume, it is a smaller line item than your bar spill.</p>",
     "<h3>A 250-capacity bar, Friday and Saturday</h3>\n"
     "<p>Three officers — one on ID, one on door, one on floor — 21:00 to 03:00, both nights. That is twelve\n"
     "officer-shifts of six hours. At the market rates above it lands in the low four figures per weekend, and for a\n"
     "room doing that volume it is a smaller line item than your bar spill. Recurring bookings should be quoted as a\n"
     "flat monthly rate so you can budget.</p>"),

    ("<h3>A 300-guest wedding at a banquet hall</h3>\n"
     "<p>Four suited officers from 17:00 to 01:00 — two on the entrance and gift table, two on the floor and parking lot\n"
     "at the end. Eight hours at $42 across four officers is about <strong>$1,340</strong>, plus a supervisor if the\n"
     "guest list is complicated.</p>",
     "<h3>A 300-guest wedding at a banquet hall</h3>\n"
     "<p>Four suited officers from 17:00 to 01:00 — two on the entrance and gift table, two on the floor and parking\n"
     "lot at the end. Thirty-two officer-hours, plus a supervisor if the guest list is complicated. Ask for the\n"
     "supervisor to be priced separately so you can see what you are paying for.</p>"),

    ("<h3>A one-day outdoor event, 1,500 attendees</h3>\n"
     "<p>Ten officers plus a lead, 10:00 to 23:00 including set-up and clear, with overnight equipment watch. Expect\n"
     "<strong>$7,000–$9,000</strong> depending on the number of gates, whether alcohol is served and whether the site\n"
     "needs holding overnight.</p>",
     "<h3>A one-day outdoor event, 1,500 attendees</h3>\n"
     "<p>Ten officers plus a lead, 10:00 to 23:00 including set-up and clear, with overnight equipment watch. The\n"
     "number of gates, whether alcohol is served and whether the site needs holding overnight move this more than the\n"
     "attendee count does — which is why a quote given over the phone without a site plan is a guess.</p>"),

    ("<p>From $38 per hour per licensed guard with a four-hour minimum. A typical Friday and Saturday for a "
     "200&ndash;300 capacity room &mdash; three officers, 21:00 to 03:00 &mdash; lands around $1,400 for the weekend. "
     "Recurring weekly bookings are quoted at a flat rate so you can budget.</p>",
     "<p>It depends on the room and the hours, which is why we price from a walk-through rather than a phone call. "
     "Recurring weekly bookings go on a flat rate so you can budget.</p>"),

    ("<p>Eight hours per agent, from $95 per hour. Multi-day and touring work is quoted as a flat daily rate with "
     "travel and accommodation stated in advance. Short-notice overnight coverage is available through 24-hour "
     "dispatch.</p>",
     "<p>Protection details are quoted per assignment. Multi-day and touring work goes on a flat daily rate with "
     "travel and accommodation stated in advance. Short-notice overnight coverage is available through 24-hour "
     "dispatch.</p>"),

    # --- cross-links to the old multi-page structure ------------------------
    ('<a href="/services/high-risk.html">high-risk work</a>',
     '<a href="../index.html#high-risk">high-risk work</a>'),
    ('<a href="/services/high-risk.html">Our high-risk\npage</a>',
     '<a href="../index.html#high-risk">Our high-risk\nsection</a>'),
    ('<a href="/services/high-risk.html">high-risk work</a> for the assessed end of this.',
     '<a href="../index.html#high-risk">high-risk work</a> for the assessed end of this.'),
]

for old, new in REPLACEMENTS:
    if old in s:
        s = s.replace(old, new)

# any remaining absolute service/page links -> anchors on the single page
s = re.sub(r'href="/services/high-risk\.html"', 'href="../index.html#high-risk"', s)
s = re.sub(r'href="/services/([a-z-]+)\.html"', r'href="../index.html#\1"', s)
s = re.sub(r'href="/contact\.html"', 'href="../index.html#quote"', s)
s = re.sub(r'href="/about\.html"', 'href="../index.html#crew"', s)
s = re.sub(r'href="/coverage\.html"', 'href="../index.html#coverage"', s)
s = re.sub(r'href="/journal/([a-z-]+)\.html"', r'href="\1.html"', s)
s = re.sub(r'href="/journal/"', 'href="index.html"', s)
s = re.sub(r'href="/"(?![^>]*index)', 'href="../index.html"', s)

io.open(SRC, "w", encoding="utf-8").write(s)
print("journal.py migrated")

# report anything that still names a Swarm rate
leftovers = [m for m in re.findall(r"[^\n]*\$\d[^\n]*", s)
             if "market" not in m.lower() and "$5M" not in m and "$5,000,000" not in m]
print("lines still containing a dollar figure: %d" % len(leftovers))
for m in leftovers[:20]:
    print("   ", m.strip()[:120])
