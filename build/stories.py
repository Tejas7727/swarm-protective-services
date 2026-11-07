# -*- coding: utf-8 -*-
"""What you get, shown instead of listed: each service page's second screen is
one annotated plan that plays out like a short film when the screen arrives.

    the plan draws itself  ->  officers land on their posts  ->  vehicles and
    people move along their routes  ->  each thing you get appears as a callout
    pinned to the place and the moment it happens  ->  the report arrives last

One clock (--t, 0 to 1) drives everything; swarm.js runs it once per arrival.
Without the script, or with reduced motion, --t stays at its default of 1 and
the finished, fully labelled plan is what shows. The six items are also in the
page as a list for screen readers and search.

Two layouts from the same story: wide (callouts left and right of the plan) and
tall (callouts above and below), shown by the window's shape (swarm.css).
Plan coordinates are 640 x 640, the same as build/plans.py.
"""
import html

# ---------- drawing parts (plan coordinates) ----------------------------------


def W(d, faint=False):
    return '<path class="%s" pathLength="1" d="%s"/>' % ("s-w2" if faint else "s-w", d)


def R(d, a, b):
    """A gold route drawn between story times a and b."""
    return '<path class="s-r" pathLength="1" style="--a:%.2f;--b:%.2f" d="%s"/>' % (a, b, d)


def DASH(d, a):
    return '<path class="s-r2" style="--a:%.2f" d="%s"/>' % (a, d)


def POST(x, y, a, lead=False):
    ring = '<circle class="s-ring" cx="%d" cy="%d" r="24"/>' % (x, y) if lead else ""
    return ('<g class="s-pop" style="--a:%.2f">%s<path class="s-p" d="M%d %dl10 10-10 10-10-10z"/></g>'
            % (a, ring, x, y - 10))


def DOC(x, y, a, seal=False):
    s = '<circle cx="%d" cy="%d" r="6"/>' % (x + 9, y + 15) if seal else \
        '<path d="M%d %dh18"/>' % (x - 9, y + 13)
    return ('<g class="s-doc" style="--a:%.2f"><path d="M%d %dh22l10 10v34h-32z M%d %dv10h10"/>'
            '<path d="M%d %dh18M%d %dh18M%d %dh12"/>%s</g>'
            % (a, x - 16, y - 22, x + 6, y - 22, x - 9, y - 8, x - 9, y - 1, x - 9, y + 6, s))


def TAG(x, y, text, a):
    w = 14 + 11 * len(text)
    return ('<g class="s-tag" style="--a:%.2f"><rect x="%d" y="%d" width="%d" height="28" rx="14"/>'
            '<text x="%d" y="%d" text-anchor="middle">%s</text></g>' % (a, x - w // 2, y - 14, w, x, y + 6, text))


def CAR(w=88, h=40):
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="8"/><path d="M%d %dv%d"/>'
            % (-w // 2, -h // 2, w, h, w // 2 - 18, -h // 2 + 4, h - 8))


def BUS():
    return ('<rect x="-60" y="-21" width="120" height="42" rx="9"/><path d="M-38-21v42M-16-21v42M6-21v42M28-21v42"/>'
            '<path class="s-p" d="M-27-10l10 10-10 10-10-10z"/>')


def MOVER(glyph, path, keys, end, rotate=False, cls="s-mv"):
    """A thing that travels `path`; keys are (story time, fraction of the path).
    `end` is where it rests without the script: (x, y, degrees)."""
    k = ",".join("%.3f:%.3f" % kv for kv in keys)
    return ('<path class="s-mp" d="%s"/><g class="%s" style="--a:%.2f" data-keys="%s"%s '
            'transform="translate(%d %d) rotate(%d)">%s</g>'
            % (path, cls, keys[0][0] - .04, k, ' data-rotate' if rotate else "", end[0], end[1], end[2], glyph))


def DOTS(points, a0, a1, out=None):
    """Crowd or queue: dots that appear between a0 and a1 (and leave from `out`)."""
    n = len(points)
    dots = "".join('<circle class="s-dot" style="--a:%.3f" cx="%d" cy="%d" r="5"/>'
                   % (a0 + (a1 - a0) * i / max(1, n - 1), x, y) for i, (x, y) in enumerate(points))
    return '<g class="s-crowd"%s>%s</g>' % (' style="--o:%.2f"' % out if out else "", dots)


def grid_points(x0, y0, x1, y1, step, seed=7):
    pts, k = [], seed
    for y in range(y0, y1, step):
        for x in range(x0, x1, step):
            k = (k * 1103515245 + 12345) & 0x7fffffff
            if k % 10 < 7:
                pts.append((x + (k >> 8) % 9 - 4, y + (k >> 12) % 9 - 4))
    pts.sort(key=lambda p: -p[1])           # they come in from the gates, at the bottom
    return pts


# ---------- the six stories ---------------------------------------------------
# callouts: (item title exactly as in services.py, anchor x, anchor y, story time)

STORIES = {
    "close-protection": dict(
        label="A hotel arrival, planned: the lobby walked before you come, the car to the kerb, two officers at the "
              "door, the walk under the canopy to the lobby, a second way out, and a written report.",
        parts=[
            W("M280 330H90V60h460v140M550 250v80H360"), W("M270 330v80h100v-80"),
            W("M40 450h560M40 600h560", True),
            POST(320, 140, .16), DOC(150, 120, .80, seal=True),
            MOVER('<g class="s-car">%s</g>' % CAR(), "M-80 520H320", [(.22, 0), (.42, 1)], (320, 520, 0)),
            POST(272, 520, .46, lead=True), POST(368, 520, .48),
            R("M320 500V170", .52, .70),
            MOVER('<circle class="s-client" r="9"/>', "M320 500V170", [(.54, 0), (.72, 1)], (320, 170, 0)),
            POST(320, 395, .30), DASH("M320 225H600", .74), DOC(560, 120, .90),
        ],
        callouts=[("Advance on the location", 320, 140, .20), ("Secure transport", 320, 520, .40),
                  ("A named lead", 272, 520, .50), ("Arrivals and departures", 320, 395, .62),
                  ("Discretion in writing", 150, 120, .82), ("A written report", 560, 120, .92)],
    ),
    "event-security": dict(
        label="A concert floor, planned: the plan before the day, door and ID checks at the gates, officers on the "
              "barrier, one lead on site, the crowd in and out, and an incident report.",
        parts=[
            W("M70 60h500v520H70z"), W("M170 60v90h300V60"), W("M150 190h340M150 198h340"),
            W("M70 580h120M250 580h140M450 580h120", True),
            POST(220, 560, .26), POST(420, 560, .28),
            DOTS(grid_points(140, 225, 500, 455, 26), .30, .52, out=.80),
            POST(200, 206, .50), POST(320, 206, .52), POST(440, 206, .54),
            POST(545, 330, .58, lead=True),
            R("M610 110H520q-20 0-20 20v20H470", .60, .70),
            DOC(590, 40, .90),
        ],
        callouts=[("A plan before the day", 70, 60, .16), ("Door and ID checks", 220, 560, .32),
                  ("Barrier and floor", 440, 206, .56), ("One lead on site", 545, 330, .62),
                  ("Close-out", 420, 560, .86), ("Incident report", 590, 40, .92)],
    ),
    "venue-security": dict(
        label="A club night, planned: the same crew every week at the door, ID checks as the line comes in, the floor "
              "and the bar covered, a sweep at close, and a nightly report.",
        parts=[
            W("M90 60h460v400H370M90 60v400h180"), W("M120 90h170v40H120z"), W("M330 160h190v170H330z"),
            W("M120 300h120v120H120z", True), W("M30 520h580", True),
            POST(300, 470, .18), POST(340, 470, .22),
        ] + [MOVER('<circle class="s-guest" r="6"/>',
                   "M%d 600H300Q320 600 320 575V470Q320 430 360 410L%d %d" % (qx, ex, ey),
                   [(.30 + i * .06, 0), (.44 + i * .06, 1)], (ex, ey, 0))
             for i, (qx, ex, ey) in enumerate([(250, 395, 300), (215, 440, 250), (180, 470, 300), (145, 420, 210)])] + [
            POST(425, 360, .48), POST(205, 150, .54), POST(180, 280, .58),
            '<rect class="s-sweep" x="96" y="66" width="3" height="388"/>',
            DOC(590, 40, .92),
        ],
        callouts=[("The same crew weekly", 300, 470, .22), ("Door and ID", 340, 470, .30),
                  ("Floor coverage", 425, 360, .50), ("Licence-safe practice", 205, 150, .58),
                  ("Close and sweep", 540, 250, .86), ("Nightly report", 590, 40, .94)],
    ),
    "party-bus-security": dict(
        label="A party bus route: an officer on board, the driver briefed, a headcount at every stop, conduct kept on "
              "the bus, every stop covered, and a report in the morning.",
        parts=[
            W("M40 140h560M40 320h560M40 500h560M140 40v560M320 40v560M500 40v560", True),
            R("M140 500H320V320H500V140", .10, .22),
            W("M156 500a16 16 0 1 0-32 0a16 16 0 1 0 32 0"), W("M336 320a16 16 0 1 0-32 0a16 16 0 1 0 32 0"),
            W("M516 140a16 16 0 1 0-32 0a16 16 0 1 0 32 0"),
            TAG(140, 560, "14 / 14", .18), TAG(245, 320, "14 / 14", .40), TAG(590, 140, "14 / 14", .66),
            MOVER('<g class="s-bus">%s</g>' % BUS(), "M140 500H320V320H500V140",
                  [(.20, 0), (.34, .5), (.46, .5), (.62, 1)], (500, 140, -90), rotate=True),
            DOC(590, 260, .90),
        ],
        callouts=[("Driver liaison", 140, 500, .12), ("An officer on board", 230, 500, .26),
                  ("Every stop covered", 320, 320, .36), ("Headcount at each stop", 245, 320, .44),
                  ("Alcohol and conduct", 500, 230, .56), ("Report in the morning", 590, 260, .92)],
    ),
    "limousine-service": dict(
        label="A chauffeured trip: a licensed officer at the door, the car and the route planned, a run to the "
              "airport when it is needed, door to door, and nothing said about it afterwards.",
        parts=[
            W("M40 205h560M40 420h560M200 40v560M440 40v560", True),
            W("M60 60h110v110H60z"), W("M470 470h120v120H470z"), W("M500 470v-18h60v18"),
            W("M400 96h190v26H400z"), W("M410 109h170", True),
            POST(115, 186, .14),
            DASH("M200 205H440V420", .30), DASH("M200 205V109H400", .48),
            R("M115 175V205H200V420H530V452", .26, .40),
            MOVER('<g class="s-car">%s</g>' % CAR(56, 28), "M115 200H200V420H530V445",
                  [(.32, 0), (.72, 1)], (530, 445, 90), rotate=True),
            POST(560, 455, .74),
        ],
        callouts=[("A licensed officer", 115, 186, .18), ("Chauffeured vehicle", 150, 205, .30),
                  ("Route planning", 440, 300, .36), ("Airport runs", 495, 109, .52),
                  ("Discretion", 320, 420, .62), ("Door to door", 560, 455, .78)],
    ),
    "monitoring": dict(
        label="A property on a schedule: a standing order, timed patrols with a check at every corner, the building "
              "after hours, vacant or under renovation, escalation from the gate, and a log of every visit.",
        parts=[
            W("M60 60h520v520H60z"), W("M190 190h260v220H190z"), W("M280 580v-40M360 580v-40", True),
            '<path class="s-z" d="M330 300h120v110H330z"/>',
            '<g class="s-win"><rect x="214" y="214" width="34" height="22"/><rect x="266" y="214" width="34" height="22"/>'
            '<rect x="214" y="252" width="34" height="22"/><rect x="266" y="252" width="34" height="22"/></g>',
            R("M110 110H530V530H110Z", .18, .30),
            TAG(110, 70, "22:00", .30), TAG(530, 70, "22:04", .42), TAG(530, 610, "22:09", .56), TAG(110, 610, "22:13", .70),
            MOVER('<path class="s-p" d="M0-11l11 11-11 11-11-11z"/>', "M110 110H530V530H110Z",
                  [(.28, 0), (.80, 1)], (110, 110, 0)),
            DOC(300, 330, .20),
            '<g class="s-alert" style="--a:.76"><circle cx="320" cy="560" r="26"/></g>',
            DOC(600, 330, .92),
        ],
        callouts=[("A standing order", 300, 330, .22), ("Scheduled checks", 530, 110, .44),
                  ("Business after hours", 231, 225, .50), ("Vacant and renovation property", 450, 400, .62),
                  ("Escalation", 320, 560, .80), ("A log per visit", 600, 330, .94)],
    ),
}

# ---------- layout: the plan in the middle, the callouts around it -------------

LAYOUTS = {
    # name: (canvas w, h, plan scale, plan x, plan y, font size, line height)
    "wide": (1600, 900, 1.24, 403, 54, 33, 39),
    "tall": (900, 1500, 1.30, 34, 330, 40, 48),
}


def _wrap(text, n):
    if len(text) <= n:
        return [text]
    words, a = text.split(), []
    while words and len(" ".join(a + [words[0]])) <= n:
        a.append(words.pop(0))
    return [" ".join(a), " ".join(words)]


def _callouts(story, layout):
    cw, ch, k, px, py, fs, lh = LAYOUTS[layout]
    items = [(t, px + ax * k, py + ay * k, a) for t, ax, ay, a in story["callouts"]]
    out = []
    if layout == "wide":
        # left of the plan's middle goes left, right goes right (never more than four a side)
        mid = px + 320 * k
        by_x = sorted(items, key=lambda i: i[1])
        n_left = min(4, max(2, sum(1 for i in items if i[1] < mid)))
        sides = [("L", sorted(by_x[:n_left], key=lambda i: i[2])), ("R", sorted(by_x[n_left:], key=lambda i: i[2]))]
        for side, group in sides:
            # each label sits level with what it points at, pushed apart only where they would touch
            ys, gap = [], 132
            for (_, _, y, _) in group:
                ys.append(max(min(y, ch - 60), (ys[-1] + gap) if ys else 80))
            over = ys[-1] - (ch - 70)
            if over > 0:
                ys = [v - over for v in ys]
                for j in range(len(ys) - 2, -1, -1):
                    ys[j] = min(ys[j], ys[j + 1] - gap)
            for j, (t, x, y, a) in enumerate(group):
                ty = ys[j]
                lines = _wrap(t, 17)
                tx = 350 if side == "L" else 1250
                anchor = "end" if side == "L" else "start"
                ex = tx + (16 if side == "L" else -16)
                text = "".join('<tspan x="%d" dy="%d">%s</tspan>' % (tx, 0 if i == 0 else lh, html.escape(s))
                               for i, s in enumerate(lines))
                mid = ty - fs // 3 + (lh * (len(lines) - 1)) // 2
                out.append('<g class="s-call" style="--a:%.2f"><path class="s-lead" pathLength="1" d="M%d %dH%d L%d %d"/>'
                           '<circle class="s-pin" cx="%d" cy="%d" r="6"/><text class="s-ct" x="%d" y="%d" '
                           'text-anchor="%s">%s</text></g>'
                           % (a, ex, mid, ex + (40 if side == "L" else -40), x, y, x, y, tx, ty, anchor, text))
    else:
        by_y = sorted(items, key=lambda i: i[2])
        rows = [("T", sorted(by_y[:3], key=lambda i: i[1])), ("B", sorted(by_y[3:], key=lambda i: i[1]))]
        for side, group in rows:
            for j, (t, x, y, a) in enumerate(group):
                tx = 150 + j * 300
                lines = _wrap(t, 13)
                ty = (80 if side == "T" else 1250) + (0 if len(lines) == 2 or side == "B" else lh // 2)
                text = "".join('<tspan x="%d" dy="%d">%s</tspan>' % (tx, 0 if i == 0 else lh, html.escape(s))
                               for i, s in enumerate(lines))
                ey = (ty + lh * (len(lines) - 1) + 22) if side == "T" else (ty - fs - 8)
                out.append('<g class="s-call" style="--a:%.2f"><path class="s-lead" pathLength="1" d="M%d %dV%d L%d %d"/>'
                           '<circle class="s-pin" cx="%d" cy="%d" r="7"/><text class="s-ct" x="%d" y="%d" '
                           'text-anchor="middle">%s</text></g>'
                           % (a, tx, ey, ey + (26 if side == "T" else -26), x, y, x, y, tx, ty, text))
    return "".join(out)


def svg(slug, layout):
    s = STORIES[slug]
    cw, ch, k, px, py, fs, lh = LAYOUTS[layout]
    return ('<svg class="story__svg story__svg--%s" viewBox="0 0 %d %d" aria-hidden="true" style="--fs:%dpx">'
            '<defs><pattern id="hatch-%s" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<path d="M0 0v9" stroke="currentColor" stroke-width="1"/></pattern></defs>'
            '<g transform="translate(%d %d) scale(%.3f)" style="--hatch:url(#hatch-%s)">%s</g>%s</svg>'
            % (layout, cw, ch, fs, layout, px, py, k, layout, "".join(s["parts"]), _callouts(s, layout)))


def figure(slug, items):
    s = STORIES[slug]
    have = {t for t, _, _, _ in s["callouts"]}
    assert have == set(items), (slug, have ^ set(items))
    listed = "".join("<li>%s</li>" % html.escape(t) for t in items)
    return ('<figure class="story" data-story data-dur="7600" role="img" aria-label="%s">%s%s</figure>'
            '<ul class="sr-only">%s</ul>'
            % (html.escape(s["label"]), svg(slug, "wide"), svg(slug, "tall"), listed))
