# Swarm — "The push" · one night, one camera, five scrolls

The home page is a single continuous camera move through one night. Nothing is ever
replaced: inside every scene there is a lit opening, and the next scene is already
inside it. Scroll pushes the camera through that opening, so the background of one
stop becomes the foreground of the next.

Five scrolls take you from the street to the morning report. The sixth frame is the
booking. Everything else — answers, journal, policy — sits below the film as an
ordinary document.

## The stops

| # | id | Time | Scene | Focal point | Copy | How the camera leaves |
|---|----|------|-------|-------------|------|-----------------------|
| 0 | `call` | live Toronto clock | **The street.** One officer, lit from the venue behind him, city bokeh, wet road | his face, dead centre of the eye path | BIG ON PURPOSE. CALM BY TRAINING. + one line + *what needs covering?* + two buttons | Camera pushes past him — he scales, slides right, blurs and is gone — toward the glow of the venue entrance |
| 1 | `venues` | 22:15 | **The door.** Brass entrance, warm spill, one doorman inside the opening | the lit doorway | MOST TROUBLE NEVER GETS IN. | Through the doorway; the opening widens past the frame before the room fills it |
| 2 | `events` | 00:40 | **The floor.** Haze, crowd, one officer standing still in it | the officer's silhouette against the light | NOTHING WORTH FILMING. | Past the officer, down the room, toward the lit corridor at the back |
| 3 | `protection` | 02:10 | **The exit.** Black SUV at a back door, wet asphalt, cold light | the tail lights and the open road beyond | THE EXIT IS PLANNED BEFORE THE ENTRANCE. | The alley mouth blooms to warm white — the night ends in light, not a dissolve |
| 4 | `report` | 06:00 | **The morning.** Skyline at dawn from an empty road | the sample report card, right | YOU SLEPT. WE WROTE IT DOWN. | The camera keeps drifting into the sunrise |
| 5 | `book` | — | Same morning, pushed in | the gold button | FORGET ABOUT IT. WE WON'T. + quote, phone, Instagram, TikTok, email | End of film; the document begins |

## Rules this film keeps

- **One focal point per frame.** If two things compete, one of them is deleted.
- **No photo is used twice.** Six plates, two cut-out layers, nothing repeated.
- **Copy is sparse.** ≤ 25 words on screen at any stop; ~120 words in the whole film.
  Word budgets and scorecards are in `COPY.md`.
- **Every rest position is composed.** CSS scroll-snap lands each flick on a stop;
  a critically damped spring drives the camera so it arrives a beat later, never jumps,
  and never leaves you in a half-transition.
- **The copy belongs to the camera.** It rides up out of a mask as the camera arrives,
  scales past you as the camera leaves. It is never "revealed on scroll" on a document.
- **The night is the colour script.** Steel blue street → brass and amber door →
  deep amber floor → cold blue exit → pale gold morning.

## What a visitor can do

- Answer *what needs covering?* — venue, event or person. The story lines rewrite
  themselves for that answer, dispatch replies in the HUD, the camera moves on, and the
  quote form opens preset to it.
- Jump to any stop from the chapter rail, the menu or a deep link (`#events`).
- Pointer parallax at rest: the officer sits nearer the camera than the street does.

## If the film cannot run

`prefers-reduced-motion`, no WebGL2, or no JS at all: every stop becomes a full-bleed
still of its own scene with the copy set on it, in document order, natively scrolled.
No content is lost — the film is the delivery, not the content.
