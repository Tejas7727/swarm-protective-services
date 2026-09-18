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

A service page that happens to be cinematic, not a film with a phone number. The
order is the argument: what this is → what we provide → how we work → how booking
works → one night of it → where → who → answers → the ask. Full map:
[`build/cinema/STORYBOARD.md`](build/cinema/STORYBOARD.md). Every string lives in
[`build/cinema/content.py`](build/cinema/content.py).

| Section | id | What it does |
|---|---|---|
| Hero | `top` | Logo and company name, **Everything under control.**, what we do and where, quote + phone, six credentials |
| What we provide | `services` | Three services, three concrete deliverables each, its own quote link |
| How we work | `how` | *We talk first* — de-escalation, licences carried, hands stay down |
| How booking works | `process` | Three steps: tell us the night → walk-through and written plan → shift and report |
| One night | `night` | Four beats of a Saturday, one camera pushing through four scenes |
| Where we work | `coverage` | 18 GTA municipalities |
| Clients and crew | `people` | Testimonials and crew — placeholders until they are real |
| Answers | `answers` | Eight straight answers, FAQ schema |
| Tell us the night | `book` | The ask: quote, phone, Instagram, TikTok, email |

**Request a quote** and the phone number are in the sticky header everywhere, in most
sections, and in a fixed bottom bar on phones. `privacy.html`, `404.html` and the
six-article `journal/` stay separate — the journal is what ranks for long-tail search.
**No prices anywhere**; quoting happens on request.

**Placeholders.** Anything in `content.py` marked `PLACEHOLDER` (testimonials, crew)
renders only in preview builds, so a half-filled section never reaches the public
site. Fill it in and it publishes itself. `SHOW_FILM = False` removes the film
section entirely, and nothing else on the page changes.

**Engine** — `docs/assets/cine/site.js`, no framework, 519 KB and 14 requests for the
whole page:

- Sections arrive with an IntersectionObserver; the hero has pointer and scroll
  parallax; nothing else animates on a timer.
- The film is a sticky stage with four viewport-tall scroll steps. A WebGL2 renderer
  draws each plate as one quad; blur is a mip bias; the doorway is a feathered clip
  rect that opens faster than the scene behind it grows (the exponent is solved from
  the viewport, not tuned). A critically damped spring drives the camera, so it lands
  a beat after the scroll.
- Its textures load only when the section is within 120% of the viewport, and it only
  draws while it is on screen.
- Photography is graded quiet in `assets.py: quiet()` — desaturated, darkened — so the
  type is always the brightest thing on the page.
- `prefers-reduced-motion`, no WebGL2 or no JS: the beats become four full-bleed
  stills with the same words. Nothing is lost.

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
| `build/cinema/content.py` | **every word on the home page**, including the placeholders |
| `build/cinema/render.py` | the markup for each section, schema, FAQ, the quote dialog |
| `build/cinema/assets.py` | plates, cut-outs, grades, portals — everything in `scene.json` |
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

## Verified (2026-09-17, live URL)

- **16/16 behaviour checks**: the company name, headline, quote button, phone and
  credentials are all above the fold; ten quote entry points; the header keeps a
  visible quote button while you scroll; three services with three proof points each;
  the film reaches its last beat at 60 fps; the dialog opens; deep links land; the
  mobile offer bar is fixed to the bottom; the canvas fills its stage at 3× device
  resolution; and with motion turned off the page is complete (949 words, four stills).
- **Weight**: 519 KB transferred, 14 requests, DOM ready 192 ms, load 222 ms.
- **Build audit**: 10 pages, no dead links or missing assets, valid JSON-LD
  (`SecurityService`, `Service` ×3, `FAQPage`, `BlogPosting`, `BreadcrumbList`).
