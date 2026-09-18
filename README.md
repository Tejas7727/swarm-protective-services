# Swarm Protective Services

Licensed door staff, event security and close protection across the Greater Toronto Area.
This repo holds the website, the brand system and the build that generates them.

**Live preview:** https://tejas7727.github.io/swarm-protective-services/

> The preview is deliberately `noindex` — it must never compete with the real domain in search.
> Building without `--preview` flips that off and points canonicals at `swarmprotective.ca`.

---

## Layout

    build/            the generator — edit here, never in docs/*.html
      cinema/         the home page: content.py (all copy), renderer, asset pipeline, STORYBOARD.md
    docs/             the built site. GitHub Pages serves this folder.
      assets/cine/    site.js and site.css — behaviour and the design system
      assets/scene/   the plates, the cut-out layers and scene.json (the camera manifest)
    brand/            logo system, favicons, social, email, print, brand-kit.html
    content/          brand playbook, Google Business, Instagram, TikTok, blog plan, launch
                      checklist, image packs
    source-art/       full-resolution scene art before export
    ClientImages/     original crew photography; drop generated plates in ClientImages/generated/

`content/`, `ClientImages/`, `source-art/` and `build/cinema/cutouts/` are gitignored — Pages
needs a public repo on a free account and none of them has to be public.

---

## The home page

Five screens and a form, phone-first, a few words per screen, one camera. Full map:
[`build/cinema/STORYBOARD.md`](build/cinema/STORYBOARD.md). Every word:
[`build/cinema/content.py`](build/cinema/content.py).

| Screen | id | What it holds |
|---|---|---|
| Home | `home` | The crew, the SWARM lockup, "Licensed security service", Get a quote + Call |
| What we do | `services` | Event security · Venue security · Close protection; PSISA licensed · $5M insured · WSIB |
| On the job | `work` | At the door \| At your side |
| Across the GTA | `coverage` | Map of 18 cities, bee pins, Toronto marked |
| The crew | `crew` | Crew and event tiles (placeholders until real photos exist) |
| Get a quote | `contact` | The form, the phone, socials |

The camera pushes through one of our officers into each of the first two scenes, then pulls
back out of the door into the map. Get a quote and Call start on the first screen, move into
the header, then drop into the form. `answers.html` carries the FAQ for search.
**No prices anywhere**; quoting happens on request.

**Engine** — `docs/assets/cine/site.js`, no framework, about 700 KB for the whole page:

- CSS scroll-snap (one flick, one screen) and a critically damped spring for the camera.
- WebGL2 draws the page's own `<img>` elements — one download per photo, at the size the
  browser picked for this screen.
- The split is the screen halved (side by side on landscape, stacked on portrait); each photo
  is cover-fitted into its half.
- Without WebGL, with reduced motion, or with no JavaScript, it is five full-bleed screens and
  the form in normal flow. Copy off-stage is transparent, never hidden; focusing it moves the
  camera to it.

**Images** — provenance in `source-art/scene-v4/SOURCES.md`: the crew and the garage detail are
the client's photos; the event shot is Pexels 13602781 (free commercial licence, another agency's
badge blurred, never captioned as Swarm); the doorman is generated locally. Every photo is graded
quiet in `assets.py` so the type stays the brightest thing on screen.

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
| `build/cinema/content.py` | **every word on the home page**, including the crew/event placeholders |
| `build/cinema/render.py` | the markup for each section, schema, FAQ, the quote dialog |
| `build/cinema/assets.py` | photo grading, the split halves, portals — everything in `scene.json` |
| `docs/assets/cine/site.js` | reveals, hero parallax, the quote dialog, the film camera |
| `docs/assets/cine/site.css` | the design system; plain mode is the no-motion fallback |

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

## Verified (2026-09-18)

- **Devices**: every screen and the form shot at 1920×1080, 1440×900, 1280×720, 1024×768,
  768×1024, 390×844 @3×, 375×667 and 360×740 @3×, plus transition midpoints — no sideways
  overflow, no console errors, every sampled depth a composed frame.
- **Behaviour**: 46/46 — name, licence line and both actions on the first screen; actions move to
  the header and then into the form; every screen lands with its copy, reverse included; deep
  links; Get a quote lands on the form; the form refuses an empty submit; resize; reduced motion
  and no-JavaScript are complete pages.
- **cinematic-scroll verifier**: PASS — doctor 94/100, runtime page-proof clean on desktop,
  mobile, reduced-motion, mobile-reduced-motion and no-JS.
- **Weight**: 705 KB and 15 requests for the whole page, LCP 0.31 s on a laptop.
- **Build audit**: 11 pages, no dead links, missing assets or broken fragments, valid JSON-LD.
