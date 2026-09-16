# Swarm Protective Services

Licensed door staff, event security and close protection across the Greater Toronto Area.
This repo holds the website, the brand system and the build that generates them.

**Live preview:** https://tejas7727.github.io/swarm-protective-services/

> The preview is deliberately `noindex` — it must never compete with the real domain in search.
> Building without `--preview` flips that off and points canonicals at `swarmprotective.ca`.

---

## Layout

    build/            the generator — edit here, never in docs/
    docs/             the built site. GitHub Pages serves this folder.
    brand/            logo system, favicons, social, email, print, brand-kit.html
    content/          brand playbook, Google Business, Instagram, TikTok, blog plan, launch checklist
    ClientImages/     original crew photography (input to build/grade.py)

`content/`, `ClientImages/` and `source-art/` are gitignored — Pages needs a public repo on a
free account and none of them has to be public. See `.gitignore` for how to change that.

---

## The site

**One page.** Every nav item is an anchor that scrolls to a section on `index.html`:

    #venues      nightclub and bar security
    #events      concerts, weddings, corporate, film
    #protection  close protection and executive protection
    #high-risk   threat-assessed work, and the truth about armed security
    #night       a shift, 19:40 to 03:05
    #crew        who turns up and what they hold
    #coverage    service area
    #answers     FAQ
    #quote       the form

Plus `privacy.html`, `404.html`, and `journal/` — six long-form posts kept as separate
documents on purpose. The one-page site converts; the journal is what ranks for the long-tail
queries the big agencies will not answer honestly. Deleting it would cost the SEO goal.

**Design direction: Blackout.** Near-black surfaces, one gold accent, hairline structure, and
the crew photography carrying the weight.

**No prices anywhere.** Quoting happens on request. The journal's cost article cites published
industry ranges — that is market data, not our rate card, and it is the reason that page ranks.

### Motion

Every scroll-linked effect runs on a **CSS scroll timeline**, so it is on the compositor thread
with no scroll listeners:

| Effect | Trigger |
|---|---|
| Hero shutter — a light wipe brings the crew up, once | page load |
| The muscle bee flying a weaving path across the viewport | `scroll(root)` |
| Section and row reveals, staggered | `view()` |
| Image zoom-out inside every frame, parallax on the band | `view()` |
| Gold progress hairline under the masthead | `scroll(root)` |
| Ticker of services, pauses on hover | time |
| Counters on the proof bar | IntersectionObserver |
| Ken Burns on the hero photo, bee wing-bob, dispatch pulse | time |

Browsers without scroll timelines (Safari < 26) get an IntersectionObserver fallback — JS adds
`.js-io` to `<html>` and the reveals become transitions. `prefers-reduced-motion` removes the
bee, the shutter and all movement.

---

## Working on it

Never edit `docs/*.html` by hand — it is generated and will be overwritten.

```bash
python build/build.py            # production build
python build/build.py --preview https://tejas7727.github.io/swarm-protective-services
python build/audit.py            # dead links, missing assets, SEO lengths, JSON-LD
python build/grade.py            # re-grade and re-crop photography from ClientImages/
python build/og.py               # regenerate the 1200x630 social cards
```

| File | What lives there |
|---|---|
| `build/common.py` | **`BIZ` — every phone number, licence, domain and social URL.** Shell, nav, footer, org schema, relative-path helpers. |
| `build/home.py` | the single page, section by section |
| `build/journal.py` | journal index and all posts |
| `build/pages.py` | privacy and 404 |
| `docs/assets/css/swarm.css` | the whole design system, hand-edited |
| `docs/assets/js/swarm.js` | ~170 lines, no dependencies |

All internal URLs are emitted **relative**, so the same build works at a domain root, under a
GitHub Pages project path, and from the filesystem. CSS and JS carry a content-hash query
string, because `_headers` marks assets immutable.

### Photography

`build/grade.py` applies a cinematic split-tone grade — cool shadows, warm highlights, crushed
but not lost blacks, vignette, film grain — and exports responsive WebP in two modes: `plate`
for images you look at, `hero` for images with type on top. Adjust `jobs` to re-crop, `cfg`
inside `grade()` to re-grade.

**Adding new client photos:** drop them in `ClientImages/`, add entries to the `jobs` list in
`grade.py`, run it, then reference the new names from `build/home.py`.

---

## Deploying

GitHub Pages is already wired to `main` → `/docs`. Push and it redeploys.

For the real domain, Cloudflare Pages reads the same folder:

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

- **The contact form sends nothing yet.** `content/06-launch-checklist.md` §4 has both options;
  the JS already handles POST, failure and a honeypot.
- **Venue consent.** The crew photographs show identifiable venue signage. Get written
  permission or re-crop via `grade.py`.
- **No testimonials anywhere** — deliberate. Inventing them would break the one thing the brand
  is built on. `content/01-google-business-profile.md` §8 is the process for collecting real
  ones from night one.

---

## Verified

10 pages: one `<h1>` each, unique titles and descriptions at Google-safe lengths, no dead links,
no missing assets, valid JSON-LD (`SecurityService`, `Service` ×4, `FAQPage`, `BlogPosting`,
`BreadcrumbList`), every image with alt text. Contrast on dark: body 15.6:1, secondary 9.5:1,
muted 5.9:1, gold 6.8:1 — all above WCAG AA. Checked at 375 / 768 / 1440, keyboard-navigable,
no console errors.
