# -*- coding: utf-8 -*-
"""Shared shell, navigation, footer and structured data for the Swarm site.

Every user-facing constant that must be replaced before launch lives in BIZ.
Change it here once and it changes on every page.

All internal URLs are emitted RELATIVE, so the same build works at a domain
root, inside a GitHub Pages project path, and from the local filesystem.
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.abspath(os.path.join(HERE, "..", "docs"))

BIZ = {
    "name":      "Swarm Protective Services",
    "short":     "Swarm",
    "base":      "https://swarmprotective.ca",   # PLACEHOLDER — final domain
    "phone_ui":  "(647) 555-0173",               # PLACEHOLDER
    "phone_tel": "+16475550173",                 # PLACEHOLDER
    "email":     "dispatch@swarmprotective.ca",  # PLACEHOLDER
    "licence":   "#0000000",                     # PLACEHOLDER — Ontario agency licence
    "city":      "Toronto",
    "region":    "ON",
    "ig":        "https://instagram.com/swarmprotective",
    "tt":        "https://tiktok.com/@swarmprotective",
    "li":        "https://linkedin.com/company/swarmprotective",
    "founded":   "2021",
}

# Build mode. `preview` points canonicals at the GitHub Pages URL and adds
# noindex, so a client preview never competes with the real site in search.
MODE = {"preview": False, "preview_base": ""}

# One page. Every nav item is an anchor on it.
NAV = [
    ("#venues",     "Venues",     "Bars, nightclubs, lounges"),
    ("#events",     "Events",     "Concerts, weddings, corporate"),
    ("#protection", "Protection", "Executive and personal details"),
    ("#report",     "Reporting",  "What lands in your inbox by morning"),
    ("#answers",    "Answers",    "What people ask before booking"),
]

AREAS = [
    "Toronto", "Etobicoke", "North York", "Scarborough", "Mississauga", "Brampton",
    "Vaughan", "Markham", "Richmond Hill", "Oakville", "Burlington", "Hamilton",
    "Pickering", "Ajax", "Whitby", "Oshawa", "Milton", "Newmarket",
]

ICONS = {
    "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 2.5 9 7l-2 2.2a13 13 0 0 0 5.8 5.8L15 13l4.5 2.4-1.2 4a2 2 0 0 1-2.2 1.4C8.6 20 4 15.4 2.7 6.9A2 2 0 0 1 4.1 4.7l2.5-2.2Z"/></svg>',
    "ig":    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.3 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.3 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.3 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .3-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.3-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.3-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.3-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.3 2.2-.4C8.4 2.2 8.8 2.2 12 2.2Zm0 3.2A6.6 6.6 0 1 0 18.6 12 6.6 6.6 0 0 0 12 5.4Zm0 10.9A4.3 4.3 0 1 1 16.3 12 4.3 4.3 0 0 1 12 16.3Zm6.9-11.1a1.5 1.5 0 1 1-1.5-1.5 1.5 1.5 0 0 1 1.5 1.5Z"/></svg>',
    "tt":    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.2 2h-3v13.1a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .7.1V9.5a5.7 5.7 0 1 0 4.9 5.6V8.6a6.5 6.5 0 0 0 3.8 1.2V6.7a3.6 3.6 0 0 1-3.8-3.4V2Z"/></svg>',
    "li":    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9h4v12H3V9Zm7 0h3.8v1.7h.05a4.2 4.2 0 0 1 3.75-2c4 0 4.75 2.6 4.75 6V21h-4v-5.5c0-1.3 0-3-1.85-3s-2.15 1.45-2.15 2.9V21h-4V9Z"/></svg>',
}


# ---------------------------------------------------------------------------
# relative-path helpers
# ---------------------------------------------------------------------------
def pfx(depth):
    """'' at the site root, '../' one folder down, and so on."""
    return "../" * depth


def home(depth, anchor=""):
    """Link back to the single page, optionally at an anchor."""
    return (pfx(depth) + "index.html" + anchor) if depth else (anchor or "index.html")


def _j(s):
    return json.dumps(s, ensure_ascii=False)


def asset_version(rel):
    """Short content hash. `_headers` marks assets immutable, so without this a
    CSS or JS change would never reach a returning visitor."""
    path = os.path.join(OUTDIR, *rel.split("/"))
    try:
        with open(path, "rb") as fh:
            return hashlib.sha1(fh.read()).hexdigest()[:8]
    except OSError:
        return "0"


def canonical(path):
    base = MODE["preview_base"] if MODE["preview"] else BIZ["base"]
    return base.rstrip("/") + path


# ---------------------------------------------------------------------------
# chrome
# ---------------------------------------------------------------------------
def nav_html(depth):
    return "".join('<a href="%s">%s</a>' % (home(depth, h), label) for h, label, _ in NAV)


def drawer_html(depth):
    out = ['<a href="%s">%s<small>%s</small></a>' % (home(depth, h), label, blurb)
           for h, label, blurb in NAV]
    out.append('<a href="%sjournal/index.html">Journal<small>Field notes for venue owners</small></a>'
               % pfx(depth))
    out.append('<a class="btn btn--full" href="%s"><span>Request a quote</span></a>'
               % home(depth, "#quote"))
    out.append('<a class="btn btn--ghost btn--full" style="margin-top:10px" href="tel:%s">'
               '<span>Call dispatch %s</span></a>' % (BIZ["phone_tel"], BIZ["phone_ui"]))
    return "".join(out)


def status_html():
    return (
        '<div class="status"><div class="status__in">'
        '<span class="dot" aria-hidden="true"></span>'
        '<span>Dispatch open — <b>answered 24 hours</b></span>'
        '<span class="status__right">'
        '<span data-clock>Toronto</span>'
        '<span>Ontario licence <b>%s</b></span>'
        '</span></div></div>' % BIZ["licence"])


def mast_html(depth):
    p = pfx(depth)
    return """<header class="mast">
<a class="mast__logo" href="{home}" aria-label="{name} — home">
<img src="{p}assets/logo/swarm-horizontal-gold.svg" alt="{name}" width="200" height="52" fetchpriority="high">
</a>
<nav class="mast__nav" aria-label="Primary">{nav}</nav>
<div class="mast__cta">
<a class="btn btn--ghost btn--sm mast__tel" href="tel:{tel}">
<span>{phone}</span></a>
<a class="btn btn--sm mast__quote" href="{quote}"><span>Request a quote</span></a>
<a class="btn mast__call" href="tel:{tel}" aria-label="Call dispatch {phone}">
<span aria-hidden="true">{i_phone}</span></a>
<button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open menu">
<span></span><span></span><span></span></button>
</div>
</header>
<div class="scrollbar" aria-hidden="true"><i></i></div>""".format(
        p=p, home=home(depth), name=BIZ["name"], nav=nav_html(depth),
        quote=home(depth, "#quote"), tel=BIZ["phone_tel"], phone=BIZ["phone_ui"],
        i_phone=ICONS["phone"])


def drawer_wrap(depth):
    return '<div class="drawer" id="drawer">%s</div>' % drawer_html(depth)


def foot_html(depth):
    p = pfx(depth)
    svc = "".join('<li><a href="%s">%s</a></li>' % (home(depth, h), t) for h, t in [
        ("#venues", "Venue and door security"),
        ("#events", "Event security"),
        ("#protection", "Close protection"),
        ("#report", "Written reporting"),
    ])
    comp = "".join('<li><a href="%s">%s</a></li>' % (u, t) for u, t in [
        (home(depth, "#answers"), "Answers"),
        (home(depth, "#coverage"), "Where we work"),
        (p + "journal/index.html", "Journal"),
        (home(depth, "#quote"), "Request a quote"),
    ])
    return """<footer class="foot">
<div class="wrap">
<div class="foot__grid">
<div>
<a class="foot__logo" href="{home}" aria-label="{name} — home"><img src="{p}assets/logo/swarm-horizontal-gold.svg" alt="{name}" width="188" height="49" loading="lazy"></a>
<p class="foot__blurb">Licensed door staff, event security and close protection across the Greater Toronto Area. The product is a night where nothing happened.</p>
<div class="foot__social">
<a href="{ig}" aria-label="Swarm on Instagram" rel="me noopener" target="_blank">{i_ig}</a>
<a href="{tt}" aria-label="Swarm on TikTok" rel="me noopener" target="_blank">{i_tt}</a>
<a href="{li}" aria-label="Swarm on LinkedIn" rel="me noopener" target="_blank">{i_li}</a>
</div>
</div>
<div><h4>What we do</h4><ul>{svc}</ul></div>
<div><h4>Company</h4><ul>{comp}</ul></div>
<div>
<h4>Dispatch</h4>
<ul>
<li><a href="tel:{tel}">{phone}</a></li>
<li><a href="mailto:{email}">{email}</a></li>
<li>Answered 24 hours, every day of the year</li>
<li>Ontario security agency licence {lic}</li>
</ul>
</div>
</div>
<div class="foot__bar">
<span>&copy; <span id="yr">2026</span> {name}</span>
<span>PSISA-licensed · $5M commercial general liability · WSIB covered</span>
<a href="{p}privacy.html">Privacy</a>
</div>
</div>
</footer>""".format(
        p=p, home=home(depth), name=BIZ["name"], svc=svc, comp=comp,
        tel=BIZ["phone_tel"], phone=BIZ["phone_ui"], email=BIZ["email"],
        lic=BIZ["licence"], ig=BIZ["ig"], tt=BIZ["tt"], li=BIZ["li"],
        i_ig=ICONS["ig"], i_tt=ICONS["tt"], i_li=ICONS["li"])


def org_schema():
    return """{{
"@context":"https://schema.org",
"@type":["SecurityService","LocalBusiness"],
"@id":"{base}/#org",
"name":"{name}",
"url":"{base}/",
"logo":"{base}/assets/icon/favicon-512.png",
"image":"{base}/assets/img/crew-wide-1200.webp",
"telephone":"{tel}",
"email":"{email}",
"priceRange":"$$$",
"foundingDate":"{founded}",
"description":"Licensed door staff, event security and close protection across the Greater Toronto Area. PSISA-licensed officers, $5M commercial general liability, a written incident report before the shift ends, and dispatch answered 24 hours.",
"knowsLanguage":"en-CA",
"address":{{"@type":"PostalAddress","addressLocality":"Toronto","addressRegion":"ON","addressCountry":"CA"}},
"geo":{{"@type":"GeoCoordinates","latitude":43.6532,"longitude":-79.3832}},
"areaServed":[{areas}],
"openingHoursSpecification":[{{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"}}],
"sameAs":["{ig}","{tt}","{li}"],
"hasOfferCatalog":{{"@type":"OfferCatalog","name":"Protective services","itemListElement":[
{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"Nightclub and bar security","url":"{base}/#venues"}}}},
{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"Event security","url":"{base}/#events"}}}},
{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"Close protection and executive protection","url":"{base}/#protection"}}}},
{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"High-risk protective detail","url":"{base}/#high-risk"}}}}
]}}
}}""".format(
        base=BIZ["base"], name=BIZ["name"], tel=BIZ["phone_tel"], email=BIZ["email"],
        founded=BIZ["founded"], ig=BIZ["ig"], tt=BIZ["tt"], li=BIZ["li"],
        areas=",".join('{"@type":"City","name":"%s"}' % a for a in AREAS))


PAGE = """<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#08090A">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="{name}">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{base}{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_CA">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ogtitle}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{base}{og}">
<meta name="robots" content="{robots}">
<meta name="geo.region" content="CA-ON">
<meta name="geo.placename" content="Toronto">
<link rel="icon" href="{p}assets/icon/favicon.ico" sizes="any">
<link rel="icon" href="{p}assets/icon/favicon-512.png" type="image/png" sizes="512x512">
<link rel="apple-touch-icon" href="{p}assets/icon/favicon-180.png">
<link rel="manifest" href="{p}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Saira:wdth,wght@75..125,400..900&family=Archivo:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{p}assets/css/swarm.css?v={cssv}">
{head}
<script type="application/ld+json">{org}</script>
{schema}
</head>
<body{bodyattr}>
<a href="#main" class="skip"><span>Skip to content</span></a>
<div class="topbar">
{status}
{mast}
</div>
{drawer}
<main id="main">
{body}
</main>
{foot}
<script src="{p}assets/js/swarm.js?v={jsv}" defer></script>
</body>
</html>
"""


def page(path, title, desc, body, depth=0, og="/assets/og/og-default.jpg",
         ogtype="website", schema="", head="", ogtitle=None, noindex=False,
         bodyattr=""):
    robots = "noindex,nofollow" if (noindex or MODE["preview"]) \
        else "index,follow,max-image-preview:large"
    return PAGE.format(
        p=pfx(depth), title=title, desc=desc, base=BIZ["base"], canon=canonical(path),
        name=BIZ["name"], ogtitle=(ogtitle or title), og=og, ogtype=ogtype,
        org=org_schema(), schema=schema, head=head, robots=robots, bodyattr=bodyattr,
        cssv=asset_version("assets/css/swarm.css"), jsv=asset_version("assets/js/swarm.js"),
        status=status_html(), mast=mast_html(depth), drawer=drawer_wrap(depth),
        body=body, foot=foot_html(depth))


# ---------------------------------------------------------------------------
# fragments
# ---------------------------------------------------------------------------
def faq_schema(pairs):
    items = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (_j(q), _j(a)) for q, a in pairs)
    return ('<script type="application/ld+json">{"@context":"https://schema.org",'
            '"@type":"FAQPage","mainEntity":[%s]}</script>' % items)


def breadcrumbs(items):
    li = ",".join(
        '{"@type":"ListItem","position":%d,"name":%s,"item":"%s%s"}'
        % (i + 1, _j(n), BIZ["base"], u) for i, (n, u) in enumerate(items))
    return ('<script type="application/ld+json">{"@context":"https://schema.org",'
            '"@type":"BreadcrumbList","itemListElement":[%s]}</script>' % li)


def plain(html):
    import re
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def faq_html(pairs):
    return '<div class="faq">%s</div>' % "".join(
        '<details><summary>%s</summary><div class="faq__a">%s</div></details>' % (q, a)
        for q, a in pairs)


def img(name, widths, sizes, alt, cls="", loading="lazy", ratio=None,
        priority=False, depth=0):
    p = pfx(depth)
    srcset = ", ".join("%sassets/img/%s-%d.webp %dw" % (p, name, w, w) for w in widths)
    big = max(widths)
    dims = ' width="%d" height="%d"' % (big, round(big / ratio)) if ratio else ""
    extra = ' fetchpriority="high"' if priority else ""
    return ('<img src="%sassets/img/%s-%d.webp" srcset="%s" sizes="%s" alt="%s"%s '
            'class="%s" loading="%s" decoding="async"%s>'
            % (p, name, big, srcset, sizes, alt, dims, cls, loading, extra))


def picture(desktop, mobile, alt, sizes="100vw", loading="lazy", priority=False,
            ratio=None, depth=0):
    p = pfx(depth)
    m_name, m_widths = mobile
    m_set = ", ".join("%sassets/img/%s-%d.webp %dw" % (p, m_name, w, w) for w in m_widths)
    return ('<picture><source media="(max-width:760px)" srcset="%s" sizes="100vw">%s</picture>'
            % (m_set, img(desktop[0], desktop[1], sizes, alt, loading=loading,
                          priority=priority, ratio=ratio, depth=depth)))


def crumb_html(items):
    """items: [(label, href), ...] — the last entry renders as plain text."""
    parts = []
    for i, (label, href) in enumerate(items):
        if i == len(items) - 1:
            parts.append("<span>%s</span>" % label)
        else:
            parts.append('<a href="%s">%s</a>' % (href, label))
    return '<div class="crumbs">%s</div>' % "<i>/</i>".join(parts)


def cta_final(depth=0, heading="Tell us the night.",
              lede="Date, venue and headcount is enough to start. You get a written number and "
                   "a named lead, usually the same day."):
    return """<section class="cta-final">
<div class="wrap reveal">
<img class="cta-final__em" src="{p}assets/logo/emblem-216.webp"
 srcset="{p}assets/logo/emblem-108.webp 108w, {p}assets/logo/emblem-216.webp 216w"
 sizes="72px" alt="" width="216" height="238" loading="lazy" decoding="async">
<h2>{h}</h2>
<p class="lede">{l}</p>
<div class="hero__cta">
<a class="btn" href="{quote}"><span>Request a quote</span></a>
<a class="btn btn--ghost" href="tel:{tel}"><span>Call dispatch</span></a>
</div>
</div>
</section>""".format(p=pfx(depth), h=heading, l=lede, quote=home(depth, "#quote"),
                     tel=BIZ["phone_tel"])
