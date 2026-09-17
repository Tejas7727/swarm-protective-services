# Swarm Protective Services

Licensed door staff, event security and close protection across the Greater Toronto Area.
This repo holds the website, the brand system and the build that generates them.

**Live preview:** https://tejas7727.github.io/swarm-protective-services/

> The preview is deliberately `noindex` — it must never compete with the real domain in search.
> Building without `--preview` flips that off and points canonicals at `swarmprotective.ca`.

---

## Layout

    build/            the generator — edit here, never in docs/*.html
      cinema/         the home page: template, renderer, asset pipeline, STORYBOARD.md
    docs/             the built site. GitHub Pages serves this folder.
      assets/cine/    the scroll-film engine (cine.js, cine.css) and its graded imagery
    brand/            logo system, favicons, social, email, print, brand-kit.html
    content/          brand playbook, Google Business, Instagram, TikTok, blog plan, launch
                      checklist, image prompts
    ClientImages/     original crew photography; drop generated plates in ClientImages/generated/

`content/`, `ClientImages/`, `source-art/` and `build/cinema/cutouts/` are gitignored — Pages
needs a public repo on a free account and none of them has to be public.

---

## The home page — "One Night"

A scroll film, not a document. The page is one night on the door, 19:40 to 03:05, and scroll is
the clock. Nine pinned scenes; each arrives as a sheet sliding over the still-pinned scene
beneath it, so there is no plain scroll between scenes at all. Full script:
[`build/cinema/STORYBOARD.md`](build/cinema/STORYBOARD.md).

| Time | Scene | Scroll drives |
|---|---|---|
| 19:40 | The mark | camera pushes through the gold emblem; the crew is visible inside the shield |
| 20:15 | The crew | real officers cut out and pushed toward camera; the room defocuses behind them |
| 21:00 | Four promises | Licensed · Insured · Briefed · Reported, each dealing one proof card |
| 22:30 | The rooms | Venues, Events, Close protection, High-risk — dolly to each, hold, next |
| 01:15 | The table | three de-escalation beats under a headlight sweep |
| 02:20 | The truth | "armed bodyguards" struck through in gold, then the legal fact |
| 03:05 | The report | a sample incident report writes, signs and stamps itself |
| — | The GTA | routes spread from Toronto to 18 municipalities |
| — | Call the swarm | ~2,500 gold particles assemble into the bee emblem |

Nav, menu and the night-clock rail are all anchors on this one page. The quote form opens as a
dialog from any "Request a quote" (and from `index.html#quote`). `privacy.html`, `404.html` and
the six-article `journal/` stay as separate documents — the journal is what ranks for long-tail
search. **No prices anywhere**; quoting happens on request.

**Engine:** GSAP + ScrollTrigger + Lenis from jsDelivr, one clock (GSAP ticker drives Lenis).
Only transform, opacity, clip-path and canvas draws animate. `prefers-reduced-motion` and no-JS
both render every scene at rest with the full content.

---

## Working on it

```bash
python build/build.py --preview https://tejas7727.github.io/swarm-protective-services   # the client preview
python build/build.py                                                                  # production (indexable)
python build/audit.py            # dead links, missing assets, SEO lengths, JSON-LD, scene hooks
python build/cinema/assets.py    # re-grade plates, cutouts, clean backgrounds, bee particles
python build/og.py               # regenerate the 1200x630 social cards
```

| File | What lives there |
|---|---|
| `build/common.py` | **`BIZ` — phone, licence, domain, email, socials.** Shared shell for journal/privacy. |
| `build/cinema/index.html` | the one-page template (`{{TOKENS}}` filled by `render.py`) |
| `build/cinema/render.py` | fills the template: schema, FAQ, GTA map geometry |
| `build/cinema/assets.py` | photo pipeline for the film |
| `docs/assets/cine/cine.js` | every scene timeline, the stack, navigation, dialog |
| `docs/assets/cine/cine.css` | the film's design system; default CSS is each scene's resting state |

### Adding client photos or generated plates

1. `hyperframes remove-background photo.jpg -o build/cinema/cutouts/<name>.png`
   (needs ffmpeg on PATH — the winget install lives under
   `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin`)
2. Add the photo to `PHOTOS` in `build/cinema/assets.py` and run it. You get a graded plate,
   a graded cutout pixel-aligned to it, and a clean defocused background with the people removed.
3. Reference the new files in `build/cinema/index.html`, rebuild, audit.

Prompts for the environment plates that would remove the site's one repetition (the garage
photo appears three times) are in `content/07-image-prompts.md`.

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

- **The quote form sends nothing yet.** Add `data-endpoint="https://formspree.io/f/…"` (or your
  own function URL) to `<form … data-form>` in `build/cinema/index.html`; the JS already POSTs,
  handles failure and blocks the honeypot.
- **Venue consent.** The crew photographs show identifiable venue signage.
- **No testimonials anywhere** — deliberate. `content/01-google-business-profile.md` §8 is the
  process for collecting real ones. The on-page incident report is labelled as a sample.

---

## Verified (2026-09-16, live URL)

- **Scroll motion** — `scroll-cinema` book detector: **98% desktop / 96% mobile CINEMATIC**,
  zero console errors; every handoff screenshotted at two points and reviewed.
- **Interactions** — 27/27: menu and rail land on the right scene with copy on screen, header
  colour follows the scene, quote dialog opens with focus / validates / confirms / closes on
  Escape (desktop and mobile), deep links `#high-risk` `#answers` `#quote` from the journal,
  first Tab reaches a visible skip link.
- **Build audit** — 10 pages, no dead links or missing assets, valid JSON-LD
  (`SecurityService`, `Service` ×4, `FAQPage`, `BlogPosting`, `BreadcrumbList`).
- **Reduced motion** — all nine scenes readable in order, nothing hidden.
