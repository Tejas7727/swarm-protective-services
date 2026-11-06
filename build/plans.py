# -*- coding: utf-8 -*-
"""Advance sketches: the plan a detail is run from, drawn as gold line art.

Every protection job starts on paper: the building, the way in, the way out,
where each officer stands. These drawings put that on the screens that were
only words. They are plan views, not pictures of people, so nothing here is
passed off as a real site.

Parts, all drawn as the screen arrives (--draw, set by swarm.js; 1 without it):
    w   structure (walls, kerbs, stage)     drawn first
    w2  faint context (streets, rows)       drawn first, quieter
    r   the route, gold                     drawn second
    r2  the second way out, gold dashes     fades in with the route
    z   zones (crowd, queue)                fades in
    p   an officer's post, a gold diamond   each lands at its own --at
    l   a label                             last
Styles: swarm.css, "advance sketches".
"""

VB = 640


def _post(x, y, at):
    return ('<path class="p" style="--at:%.2f" d="M%d %dl8 8-8 8-8-8z"/>' % (at, x, y - 8))


def _label(x, y, text, anchor="start"):
    return '<text class="l" x="%d" y="%d" text-anchor="%s">%s</text>' % (x, y, anchor, text)


def _car(x, y, w=26, h=50, rot=0):
    """A car seen from above, centred on x,y."""
    return ('<g class="w" transform="translate(%d %d) rotate(%d)"><rect x="%d" y="%d" width="%d" height="%d" rx="7" '
            'pathLength="1"/><path d="M%d %dh%d" pathLength="1"/></g>'
            % (x, y, rot, -w // 2, -h // 2, w, h, -w // 2 + 4, -h // 2 + 14, w - 8))


def _svg(inner, label):
    return ('<svg class="pl" viewBox="0 0 {v} {v}" role="img" aria-label="{a}">'
            '<defs><pattern id="hatch" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<path d="M0 0v9" stroke="currentColor" stroke-width="1"/></pattern></defs>{i}</svg>'
            ).format(v=VB, a=label, i=inner)


def close_protection():
    i = [
        # the hotel, its front doors under the canopy and a side door; the street in front
        '<path class="w" pathLength="1" d="M280 330H90V60h460v140M550 250v80H360"/>',
        '<path class="w" pathLength="1" d="M270 330v80h100v-80"/>',                      # canopy
        '<path class="w2" pathLength="1" d="M40 450h560M40 600h560"/>',                  # kerb, far kerb
        _car(320, 510, 70, 32),
        # the arrival: car door, canopy, lobby; and the second way out
        '<path class="r" pathLength="1" d="M320 492V160"/>',
        '<path class="r2" d="M320 225H600"/>',
        _post(278, 510, .45), _post(362, 510, .5), _post(320, 395, .58), _post(320, 140, .66),
        _label(320, 110, "Lobby", "middle"), _label(386, 380, "Canopy"),
        _label(370, 560, "The kerb"), _label(350, 262, "Second way out"),
    ]
    return _svg("".join(i), "Plan of a hotel arrival: car at the kerb, the walk under the canopy to the lobby, "
                            "four officer positions and a second way out.")


def event_security():
    i = [
        '<path class="w" pathLength="1" d="M70 60h500v520H70z"/>',                        # the hall
        '<path class="w" pathLength="1" d="M170 60v90h300V60"/>',                         # stage
        '<path class="w" pathLength="1" d="M150 190h340M150 198h340"/>',                  # barrier
        '<rect class="z" x="130" y="215" width="380" height="250"/>',                     # the crowd
        '<path class="w" pathLength="1" d="M70 580h120M250 580h140M450 580h120"/>',       # gates in the wall
        '<path class="w2" pathLength="1" d="M70 300h-20M570 300h20M70 420h-20M570 420h20"/>',  # fire exits
        '<path class="r" pathLength="1" d="M600 110H520q-20 0-20 20v20H470"/>',            # artist route
        '<path class="r2" d="M40 300h30M570 420h30"/>',
        _post(200, 206, .42), _post(320, 206, .46), _post(440, 206, .5),
        _post(220, 560, .58), _post(420, 560, .62), _post(550, 300, .68),
        _label(320, 112, "Stage", "middle"), _label(320, 345, "Crowd", "middle"),
        _label(320, 620, "Gates", "middle"), _label(510, 92, "Artist route"),
    ]
    return _svg("".join(i), "Plan of a concert floor: stage, barrier with three officers, the crowd, "
                            "two gate posts, a fire exit post and the artist route.")


def venue_security():
    i = [
        '<path class="w" pathLength="1" d="M90 60h460v400H370v-0M90 60v400h180"/>',       # the room, door gap
        '<path class="w" pathLength="1" d="M120 90h170v40H120z"/>',                       # bar
        '<path class="w" pathLength="1" d="M330 160h190v170H330z"/>',                     # dance floor
        '<path class="w2" pathLength="1" d="M120 300h120v120H120z"/>',                    # VIP
        '<path class="w2" pathLength="1" d="M30 520h580"/>',                              # kerb
        '<path class="z" d="M140 600h6v-6h-6zM180 600h6v-6h-6zM220 600h6v-6h-6zM260 600h6v-6h-6zM300 600h6v-6h-6z"/>',
        '<path class="r" pathLength="1" d="M150 580h140q30 0 30-30v-90q0-60 60-90l40-20"/>',
        '<path class="r2" d="M550 400h40"/>',
        _post(300, 470, .45), _post(340, 470, .5), _post(205, 150, .58),
        _post(425, 360, .64), _post(180, 280, .7),
        _label(205, 82, "Bar", "middle"), _label(425, 250, "Floor", "middle"),
        _label(180, 440, "VIP", "middle"), _label(140, 630, "The line"), _label(360, 500, "ID and door"),
    ]
    return _svg("".join(i), "Plan of a club: the line outside, ID and door, the bar, the floor and the VIP "
                            "room, with five officer positions.")


def party_bus_security():
    i = [
        '<path class="w2" pathLength="1" d="M40 140h560M40 320h560M40 500h560M140 40v560M320 40v560M500 40v560"/>',
        '<path class="r" pathLength="1" d="M140 500H320V320H500V140"/>',
        '<circle class="w" pathLength="1" cx="140" cy="500" r="16"/>',
        '<circle class="w" pathLength="1" cx="320" cy="320" r="16"/>',
        '<circle class="w" pathLength="1" cx="500" cy="140" r="16"/>',
        '<g class="w" transform="translate(230 500)"><rect x="-44" y="-15" width="88" height="30" rx="6" pathLength="1"/>'
        '<path d="M-30-15v30M-14-15v30M2-15v30M18-15v30" pathLength="1"/></g>',
        _post(140, 500, .45), _post(230, 500, .55), _post(320, 320, .62), _post(500, 140, .7),
        _label(140, 545, "Pick-up", "middle"), _label(320, 365, "Second stop", "middle"),
        _label(500, 105, "Drop-off", "middle"), _label(230, 470, "On board", "middle"),
    ]
    return _svg("".join(i), "Route of a party bus: pick-up, a second stop and the drop-off, with an officer on "
                            "board and at every stop.")


def limousine_service():
    i = [
        '<path class="w2" pathLength="1" d="M40 200h560M40 440h560M200 40v560M440 40v560"/>',
        '<path class="w" pathLength="1" d="M60 60h110v110H60z"/>',                        # home
        '<path class="w" pathLength="1" d="M470 470h120v120H470z"/>',                     # venue
        '<path class="w" pathLength="1" d="M500 470v-20h60v20"/>',                        # canopy
        '<path class="r" pathLength="1" d="M115 170v30h85v240h245v30h85"/>',
        _car(150, 214, 46, 24),
        _post(115, 186, .5), _post(530, 455, .68),
        _label(115, 100, "Home", "middle"), _label(530, 530, "Venue", "middle"),
        _label(212, 320, "One car, one route"),
    ]
    return _svg("".join(i), "Route of a chauffeured car from home to the venue door, with an officer at each door.")


def monitoring():
    i = [
        '<path class="w" pathLength="1" d="M60 60h520v520H60z"/>',                        # fence line
        '<path class="w" pathLength="1" d="M190 190h260v220H190z"/>',                     # building
        '<path class="w2" pathLength="1" d="M280 580v-40M360 580v-40"/>',                 # gate
        '<path class="r" pathLength="1" d="M110 110h420v420H110z"/>',                     # the patrol loop
        '<path class="z" d="M190 190l-90-40 30-40zM450 190l90-40-30-40zM450 410l90 40-30 40zM190 410l-90 40 30 40z"/>',
        _post(110, 110, .45), _post(530, 110, .52), _post(530, 530, .59), _post(110, 530, .66),
        _post(320, 560, .72),
        _label(320, 305, "Site", "middle"), _label(320, 618, "Gate", "middle"),
        _label(320, 98, "Patrol loop", "middle"),
    ]
    return _svg("".join(i), "Plan of a property: the fence line, the building, four cameras, the patrol loop "
                            "and the gate, with check points at each corner.")


SERVICE = {
    "close-protection": close_protection,
    "event-security": event_security,
    "venue-security": venue_security,
    "party-bus-security": party_bus_security,
    "limousine-service": limousine_service,
    "monitoring": monitoring,
}


def process():
    """The plan builds with the steps: the call gives the building (step 1), the plan
    adds the routes (step 2), the run puts officers in place (step 3)."""
    i = [
        '<g class="st" style="--at:0">',
        '<path class="w" pathLength="1" d="M70 60h500v520H70z"/>',
        '<path class="w" pathLength="1" d="M170 60v90h300V60"/>',
        '<path class="w" pathLength="1" d="M70 580h120M250 580h140M450 580h120"/>',
        '<rect class="z" x="130" y="215" width="380" height="250"/>',
        '</g><g class="st" style="--at:.333">',
        '<path class="r" pathLength="1" d="M320 610V480q0-20-20-20H140"/>',
        '<path class="r" pathLength="1" d="M600 110H520q-20 0-20 20v20H470"/>',
        '<path class="w" pathLength="1" d="M150 190h340M150 198h340"/>',
        '</g><g class="st" style="--at:.667">',
        _post(200, 206, 0), _post(320, 206, 0), _post(440, 206, 0),
        _post(220, 560, 0), _post(420, 560, 0),
        '</g>',
    ]
    return _svg("".join(i), "A venue plan that builds with the three steps: the building, then the routes and "
                            "the barrier, then the officers in place.")


def dead_end():
    """404: the route that leads nowhere, and the dashed way back to the front."""
    i = [
        '<path class="w2" pathLength="1" d="M40 120h560M40 280h560M40 440h560M40 560h560'
        'M120 40v560M280 40v560M440 40v560M560 40v560"/>',
        '<path class="w" pathLength="1" d="M300 40h120v60H300zM460 300h80v120h-80zM140 460h120v80H140z"/>',
        '<path class="r" pathLength="1" d="M120 600V440h160V280h132"/>',
        '<path class="w" pathLength="1" d="M426 248v64" style="stroke-width:4"/>',
        _post(404, 280, .7),
        '<path class="r2" d="M280 440h280V128"/>',
        '<rect class="w" pathLength="1" x="544" y="104" width="32" height="24"/>',
        _label(426, 232, "Nothing past here", "middle"), _label(560, 88, "The front", "middle"),
    ]
    return _svg("".join(i), "A route on a street map that ends at a wall, and a dashed way back to the front.")
