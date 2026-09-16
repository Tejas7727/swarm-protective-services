# Swarm Protective Services — brand, site and content package

    brand/            logo system, favicons, social, email, print, brand-kit.html
    ClientImages/     original crew photography (source of truth, unedited)
    build/            the site generator — edit here, not in site/
    site/             the built website. This is what deploys.
    content/          brand playbook, Google Business, Instagram, TikTok, blog plan, launch checklist
    site-v1-archive/  the earlier single-page site, kept for reference
    .claude/          brand skill for Claude Code

---

## Start here

1. **`content/00-brand-playbook.md`** — the positioning, the one claim, the voice rules.
   Everything else is downstream of this page.
2. **`content/06-launch-checklist.md`** — what must be replaced and confirmed before this goes
   live. There are real placeholders in the site right now.
3. **`brand/brand-kit.html`** — open in a browser for every lockup, colourway and usage rule.

---

## The site

17 pages, static HTML, no framework, no build step at serve time.

    /                              home
    /services/venue-security.html  bars, nightclubs, lounges
    /services/event-security.html  concerts, weddings, corporate, film
    /services/close-protection.html
    /services/high-risk.html       threat-assessed and armed-capable work
    /about.html                    the crew, credentials, what we decline
    /coverage.html                 service area
    /contact.html                  quote form
    /journal/                      index + 6 long-form posts
    /privacy.html  /404.html

**Design direction: Blackout.** Near-black surfaces, one gold accent, hairline structure, and
the crew photography carrying the weight. The signature moment is the hero — the page opens
black and a hard light wipe brings the crew up, once, on load. Everything else is deliberately
quiet so that lands.

### Editing

Never edit `site/*.html` by hand — it is generated and will be overwritten.

```bash
python build/build.py     # regenerate every page, sitemap, robots, manifest, _headers
python build/audit.py     # dead links, missing assets, SEO lengths, JSON-LD validity
python build/og.py        # regenerate the 1200x630 social cards
python build/grade.py     # re-grade and re-crop the photography from ClientImages/
```

| File | What lives there |
|---|---|
| `build/common.py` | **`BIZ` — every phone number, licence, domain and social URL.** Shell, nav, footer, org schema. |
| `build/home.py` | home page |
| `build/services.py` | the four service pages |
| `build/pages.py` | about, contact, coverage, privacy, 404 |
| `build/journal.py` | journal index and all posts |
| `site/assets/css/swarm.css` | the whole design system, hand-edited |
| `site/assets/js/swarm.js` | ~90 lines, no dependencies |

### Photography

`build/grade.py` reads `ClientImages/`, applies a cinematic split-tone grade (cool shadows,
warm highlights, crushed but not lost blacks, vignette, film grain) and exports responsive
WebP at several widths in two modes — `plate` for images you look at, `hero` for images with
type on top. Adjust the `jobs` list to re-crop; adjust the `cfg` dict in `grade()` to re-grade.

The whole image set is 1.9 MB across every variant; a typical page loads 60–120 KB of it.

### Deploying

```bash
cd site
npx wrangler pages deploy . --project-name swarm
```

`_headers` sets immutable caching on `/assets/*` plus the usual security headers. `404.html`
should be wired as the error page.

**The contact form currently confirms on screen and sends nothing.** Wire it before launch —
`content/06-launch-checklist.md` §4 has both options. The JavaScript already handles POSTing,
the failure path and a honeypot.

---

## What is verified

- 17/17 pages: one `<h1>`, unique title and description at Google-safe lengths, no dead
  internal links, no missing assets, valid JSON-LD, every image has alt text
- Structured data: `SecurityService` (org), `Service` per service page with price, `FAQPage`,
  `BlogPosting`, `BreadcrumbList`
- Contrast on dark: body 15.6:1, secondary 9.5:1, muted 5.9:1, gold 6.8:1, gold on button
  6.75:1 — all above WCAG AA
- Checked at 375, 768 and 1440; keyboard-navigable with visible focus; `prefers-reduced-motion`
  removes the hero wipe and all movement; no console errors

---

## Before launch — the blocking items

These are stated as fact on the live site and are currently **placeholders**:

- Ontario security agency licence — `#0000000`
- Phone — `(647) 555-0173`
- Domain and email — `swarmprotective.ca`
- Founding year — `2021`
- Published rates — $38 / $42 / $95 per hour, confirm against the real price list

All of them live in `BIZ` in `build/common.py`. Change once, rebuild, done.

Two more, equally blocking:

- **Venue consent.** The crew photographs show identifiable venue signage. Get written
  permission or re-crop (`build/grade.py`, the `focus` values).
- **No testimonials anywhere on this site.** That is deliberate — inventing them would break
  the one thing the brand is built on. `content/01-google-business-profile.md` §8 is the
  process for collecting real ones from night one; add them once they exist.

---

## Using this with Claude Code

    cd swarm
    claude

`.claude/skills/swarm-brand/` loads automatically and carries the colour, type and logo rules.
