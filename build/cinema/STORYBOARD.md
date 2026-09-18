# Swarm — the home page

Five screens and a form. Phone-first, a few words per screen, one camera.

| # | Screen | id | On screen | How the camera leaves it |
|---|--------|----|-----------|--------------------------|
| 1 | **Home** | `home` | The crew (client photo), SWARM lockup with the emblem, PROTECTIVE SERVICES, "Licensed security service", Get a quote + Call | Pushes *through the centre officer's suit* into the next scene |
| 2 | **What we do** | `services` | Event security · Venue security · Close protection, one line each; PSISA licensed · $5M insured · WSIB covered | Pushes through the officer's back into the split |
| 3 | **On the job** | `work` | At the door \| At your side — side by side on landscape, stacked on portrait | Pulls **out**: the side photo fades, the doorman shrinks onto Toronto |
| 4 | **Across the GTA** | `coverage` | Map, 18 cities pinned with the bee, Toronto marked with the emblem | Settles back to a faint base under the crew (no screen is ever empty) |
| 5 | **The crew** | `crew` | Crew and event tiles — placeholders until real photos exist | The form slides up over it |
| — | **Get a quote** | `contact` | Heading, one line, the phone, socials, the form | — |

**The ask travels.** Get a quote and Call start on the first screen, move into the header on the
way to screen 2, and drop from the header into the form's own buttons when the form arrives (on
phones, where the form buttons are below the fold, they hand over and fade instead).

**Motif.** Every push goes through one of our people: the camera passes through the crew into the
work. The only pull-back is into the map, because that is the one screen about reach.

**Mechanics.** CSS scroll-snap (one flick, one screen) · a critically damped spring drives the
camera · WebGL2 draws the page's own `<img>` elements, so nothing downloads twice · the split
plate is the screen itself, halved, with each photo cover-fitted into its half.

**Fallbacks.** Without WebGL, with reduced motion, or with no JavaScript, the page is five
full-bleed screens and the form in normal flow. Same words, same actions.

**Editing.** Words: `content.py`. Images and portals: `assets.py`. Placeholders (crew, events)
render as clean empty tiles until filled in.
