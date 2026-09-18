# Swarm Protective Services

Licensed door staff, event security and close protection across the Greater Toronto Area.
This repo holds the website, the brand system and the build that generates them.

**Live preview:** https://tejas7727.github.io/swarm-protective-services/

> The preview is deliberately `noindex` — it must never compete with the real domain in search.
> Building without `--preview` flips that off and points canonicals at `swarmprotective.ca`.

---

## Layout

    build/            the generator — edit here, never in docs/*.html
      cinema/         the home page: renderer, asset pipeline, STORYBOARD.md, COPY.md
    docs/             the built site. GitHub Pages serves this folder.
      assets/cine/    the camera engine (push.js, push.css)
      assets/scene/   the plates, the cut-out layers and scene.json (the camera manifest)
    brand/            logo system, favicons, social, email, print, brand-kit.html
    content/          brand playbook, Google Business, Instagram, TikTok, blog plan, launch
                      checklist, image packs
    source-art/       full-resolution scene art before export
    ClientImages/     original crew photography; drop generated plates in ClientImages/generated/

`content/`, `ClientImages/`, `source-art/` and `build/cinema/cutouts/` are gitignored — Pages
needs a public repo on a free account and none of them has to be public.

---

## The home page — "The push"

One camera, one night, five scrolls. Every scene contains a lit opening with the next scene
already inside it; scrolling pushes the camera through that opening, so the background of one
stop becomes the foreground of the next. Nothing is ever replaced, so it never reads as a
slideshow. Full script: [`build/cinema/STORYBOARD.md`](build/cinema/STORYBOARD.md); every line of
copy, with its scorecard, is in [`build/cinema/COPY.md`](build/cinema/COPY.md).

| Stop | Time | Scene | On screen |
|---|---|---|---|
| `#call` | live Toronto clock | the street, one officer, venue glow behind him | BIG ON PURPOSE. CALM BY TRAINING. |
| `#venues` | 22:15 | the door | MOST TROUBLE NEVER GETS IN. |
| `#events` | 00:40 | the floor | NOTHING WORTH FILMING. |
| `#protection` | 02:10 | the exit, the car | THE EXIT IS PLANNED BEFORE THE ENTRANCE. |
| `#report` | 06:00 | dawn, the sample shift report | YOU SLEPT. WE WROTE IT DOWN. |
| `#book` | — | the morning, pushed in | FORGET ABOUT IT. WE WON'T. |

Below the film, as an ordinary document: the answers (FAQ), the service links, dispatch details
and the coverage list. `privacy.html`, `404.html` and the six-article `journal/` stay separate —
the journal is what ranks for long-tail search. **No prices anywhere**; quoting happens on request.

**Engine** — `docs/assets/cine/push.js`, about 400 lines, no framework:

- A WebGL2 renderer draws each plate as one quad. Blur is a mip bias, so a focus pull costs
  nothing; the doorway is a feathered clip rect that opens faster than the scene behind it grows.
- **Scroll snapping is the browser's** (CSS `scroll-snap-type: y mandatory`,
  `scroll-snap-stop: always`), so one flick is one stop and every landing is a composed frame.
- A **critically damped spring** drives the camera from the scroll position, so it arrives a beat
  later and never jumps. There is no easing between scroll and camera, only mass.
- Copy is HTML pinned to the viewport; it rides out of a mask as the camera arrives and scales
  past you as the camera leaves.
- `prefers-reduced-motion`, no WebGL2 or no JS: every stop becomes a full-bleed still with its
  copy, natively scrolled. No content is lost.

---

## Working on it

```bash
python build/build.py --preview https://tejas7727.github.io/swarm-protective-services   # client preview
python build/build.py                                                                  # production (indexable)
python build/audit.py            # dead links, assets, SEO lengths, JSON-LD, film hooks, portal sanity
python build/cinema/assets.py    # re-export the plates and rewrite scene.json
python build/og.py               # regenerate the 1200x630 social cards
```

| File | What lives there |
|---|---|
| `build/common.py` | **`BIZ` — phone, licence, domain, email, socials.** Shared shell for journal/privacy. |
| `build/cinema/render.py` | the film's copy and markup, schema, FAQ, the quote dialog |
| `build/cinema/assets.py` | plates, cut-outs, grades, portals — everything in `scene.json` |
| `docs/assets/cine/push.js` | the camera, the snap, the copy choreography, the dialog |
| `docs/assets/cine/push.css` | the film's design system; plain mode is the fallback page |

### Replacing the scene art

The six plates currently on the site are **placeholders generated locally** — a motion study, not
the design. `content/08-image-pack-v3.md` is the brief for the real ones: what each frame holds,
where its opening must sit, and the rules (no text, no weapons, dark left third).

When new art lands:

1. Put the full-resolution files in `source-art/scene-v3/` with the names in `PLATES`
   (`build/cinema/assets.py`).
2. Cut out anyone who should pass the camera:
   `npx hyperframes remove-background p0-street.png --output p0-hero.png`
   (needs ffmpeg on PATH — the winget install lives under
   `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin`), then paint the plate
   behind them clean.
3. Measure the opening and write `portal.rect` (where the next plate is drawn) and `portal.aper`
   (the opening it is seen through) into `PLATES`. `python build/audit.py` checks that the two
   are concentric and in range.
4. `python build/build.py` and re-shoot the stops before shipping.

---

## Deploying

GitHub Pages serves `main` → `/docs`. Push and it redeploys in about thirty seconds.

For the real domain, Cloudflare Pages reads the same folder (`_headers` is already written):

```bash
cd docs
npx wrangler pages deploy . --project-name swarm
```

---

## Before the real launch

Placeholders, all in `BIZ` in `build/common.py` — change once, rebuild:

- Ontario security agency licence — `#0000000`
- Phone — `(647) 555-0173`
- Domain and email — `swarmprotective.ca`
- Founding year — `2021`

Also blocking:

- **The quote form has no service wired up.** It currently hands the details to the visitor's
  mail app. Add `data-endpoint="https://formspree.io/f/…"` to the `<form … data-form>` in
  `build/cinema/render.py` and the JS POSTs instead.
- **Scene art** — the placeholders above.
- **Venue consent** if the real crew photographs (identifiable signage) go on the site.
- **No testimonials anywhere** — deliberate. `content/01-google-business-profile.md` §8 is the
  process for collecting real ones. The on-page shift report is labelled a sample.

---

## Verified (2026-09-17, local build)

- **Behaviour** — 12/12 automated checks: the film runs on WebGL2, all six plates load, deep
  links land on their stop, reverse scrolling returns, the chips rewrite the story lines and
  preset the quote form, the dialog opens, stops you cannot see are `inert`, no console errors,
  and reduced motion renders the complete page.
- **Frames** — every stop and every quarter-step screenshotted at 1440×900 and 390×844, plus 24
  random in-between positions with snapping disabled, reviewed by eye. 60 fps throughout.
- **Build audit** — 10 pages, no dead links or missing assets, valid JSON-LD
  (`SecurityService`, `Service` ×3, `FAQPage`, `BlogPosting`, `BreadcrumbList`), all six film
  hooks present, portals concentric.
