# Swarm — the home page

Six screens and a form. Phone-first, a few words per screen, one camera.

| # | Screen | id | On screen | How the camera leaves it |
|---|--------|----|-----------|--------------------------|
| 1 | **Home** | `home` | The crew in front of the emblem, SWARM lockup, PROTECTIVE SERVICES, the motto, "Licensed security service", Get a quote + Call | Pushes *through the centre officer's suit* into the next scene |
| 2 | **What we do** | `services` | Event security · Venue security · Close protection · Monitoring, one line each; PSISA licensed · $5M insured · WSIB covered | Pushes through the officer's back into the split |
| 3 | **On the job** | `work` | At the door \| At your side — side by side on landscape, stacked on portrait | Pulls **out**: the side photo fades, the doorman shrinks onto Toronto |
| 4 | **Across the GTA** | `coverage` | The drawn map — Lake Ontario, the built-up areas, the 400-series highways — 18 cities pinned with the bee, Toronto marked with the emblem, and a Canada inset for "we travel with you" | Settles back to a faint base under the crew (no screen is ever empty) |
| 5 | **The crew** | `crew` | Crew and event tiles — placeholders until real photos exist | Holds the faint map; the questions fade up over it |
| 6 | **Questions** | `faq` | Six answers people ask before booking, and a link to the long ones | The form slides up over it |
| — | **Get a quote** | `contact` | Heading, one line, the phone, socials, the form | — |

**The ask travels.** Get a quote and Call start on the first screen, move into the header on the
way to screen 2, and drop from the header into the form's own buttons when the form arrives (on
phones, where the form buttons are below the fold, they hand over and fade instead).

**Motif.** Every push goes through one of our people: the camera passes through the crew into the
work. The only pull-back is into the map, because that is the one screen about reach.

**The first screen is built, not shot.** `hero_plate.py` takes the client's group photograph,
cuts the five of them out of it with two matting models (one takes the lit wall for subject, the
other takes the floor — the overlap is the people), and rebuilds everything behind them: a dark
wall, one pool of light, and the emblem extruded on it with its own cast shadow. They get a
little more contrast, a warm rim and a contact shadow, so they stand in the room.

**The maps are drawings.** `geo_extract.py` reduces Natural Earth (public domain) to
`geo.json`; `render.py` projects it — equirectangular, scaled by cos 43.65° so shapes are true —
and emits plain SVG paths. Land is one sheet with the lakes punched out of it, so the water is
the page's own glow. Nothing is fetched at runtime, and no map service is involved. City labels
are placed at build time by trying right, left, above, below and taking the first position that
collides with nothing; the two windows (landscape and portrait) are placed separately.

**Mechanics.** CSS scroll-snap (one flick, one screen) · a critically damped spring drives the
camera · WebGL2 draws the page's own `<img>` elements, so nothing downloads twice · the split
plate is the screen itself, halved, with each photo cover-fitted into its half.

**Fallbacks.** Without WebGL, with reduced motion, or with no JavaScript, the page is six
full-bleed screens and the form in normal flow. Same words, same actions.

**Editing.** Words: `content.py` (the motto and the questions live there too). Images and
portals: `assets.py`. Map geometry: `geo_extract.py` → `geo.json`. Placeholders (crew, events)
render as clean empty tiles until filled in. The questions are emitted three times from one
list — on the page, as FAQPage structured data, and into `docs/llms.txt` for assistants — and
`audit.py` fails the build if those copies drift apart.
