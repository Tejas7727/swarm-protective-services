# -*- coding: utf-8 -*-
"""Static audit: dead links, missing assets, SEO field lengths, JSON-LD validity."""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "docs"))


def norm(p):
    return p.replace(os.sep, "/")


def main():
    pages = [norm(p) for p in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)]
    assets = set()
    for root, _, files in os.walk(SITE):
        for f in files:
            assets.add(norm(os.path.join(root, f))[len(norm(SITE)):])

    errs, titles, descs = [], {}, {}
    for p in pages:
        s = open(p, encoding="utf-8").read()
        rel = norm(p)[len(norm(SITE)):]

        t = re.search(r"<title>(.*?)</title>", s, re.S)
        d = re.search(r'<meta name="description" content="(.*?)"', s, re.S)
        titles.setdefault(t.group(1) if t else "", []).append(rel)
        descs.setdefault(d.group(1) if d else "", []).append(rel)

        n_h1 = len(re.findall(r"<h1[ >]", s))
        if n_h1 != 1:
            errs.append("%s: %d h1 tags" % (rel, n_h1))
        if t and len(t.group(1)) > 72:
            errs.append("%s: title %d chars" % (rel, len(t.group(1))))
        if d and not (110 <= len(d.group(1)) <= 180):
            errs.append("%s: description %d chars" % (rel, len(d.group(1))))

        here = os.path.dirname(rel)

        def resolve(u):
            """Resolve a page-relative URL to a site-root path, or None if external."""
            u = u.split("#")[0].split("?")[0]
            if not u or u.startswith(("http", "mailto:", "tel:", "data:", "//")):
                return None
            is_dir = u.endswith("/")
            if u.startswith("/"):
                target = u
            else:
                target = norm(os.path.normpath(os.path.join(here, u)))
                if not target.startswith("/"):
                    target = "/" + target
            if is_dir:
                target = target.rstrip("/") + "/index.html"
            return target

        for href in re.findall(r'href="([^"]+)"', s):
            t = resolve(href)
            if t and t not in assets:
                errs.append("%s: dead link %s" % (rel, href))

        for attr in re.findall(r'(?:src|srcset)="([^"]+)"', s):
            for u in attr.split(","):
                t = resolve(u.strip().split(" ")[0])
                if t and t not in assets:
                    errs.append("%s: missing asset %s" % (rel, u.strip()))

        for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                json.loads(blk)
            except Exception as exc:
                errs.append("%s: invalid JSON-LD — %s" % (rel, exc))

        if "alt=" in s:
            missing_alt = len(re.findall(r"<img(?![^>]*\salt=)[^>]*>", s))
            if missing_alt:
                errs.append("%s: %d img without alt" % (rel, missing_alt))

    # A utility class defined in CSS but never applied is a silent no-op. This is
    # exactly how the first build shipped with no scroll motion at all.
    css_path = os.path.join(SITE, "assets", "css", "swarm.css")
    if os.path.exists(css_path):
        css = open(css_path, encoding="utf-8").read()
        html_all = "".join(open(p, encoding="utf-8").read() for p in pages)
        for cls in ("reveal",):
            if ("." + cls) in css and ('class="' + cls) not in html_all                     and (" " + cls + '"') not in html_all and (" " + cls + " ") not in html_all:
                errs.append("css: .%s is styled but never used in any page" % cls)

    # the home page is a funnel: every service card reaches its page, every
    # step of the quote form exists, the phone is one tap away, and the first
    # screen's photographs are all on disk
    idx = os.path.join(SITE, "index.html")
    if os.path.exists(idx):
        page_html = open(idx, encoding="utf-8").read()
        hooks = ['id="contact"', "data-quote", 'id="services"', 'id="faq"', 'id="coverage"', 'id="people"',
                 'class="gm"', 'id="gm-hq"', 'gm__land', 'gm__shore', 'class="abar"']
        for hook in hooks:
            if hook not in page_html:
                errs.append("index.html: hook %s missing" % hook)
        if 'href="tel:' not in page_html:
            errs.append("index.html: no phone link")
        # the coverage page carries both maps
        cov = os.path.join(SITE, "coverage.html")
        cov_html = open(cov, encoding="utf-8").read() if os.path.exists(cov) else ""
        for hook in ('data-cov', 'class="gm"', 'class="ca"', 'gm__route'):
            if hook not in cov_html:
                errs.append("coverage.html: hook %s missing" % hook)
        if len(re.findall(r'<h1[ >]', page_html)) != 1:
            errs.append("index.html: expected exactly one h1")
        cards = re.findall(r'<a class="scard" href="([^"]+)"', page_html)
        if len(cards) != 6:
            errs.append("index.html: %d service cards, expected 6" % len(cards))
        for href in cards:
            if not os.path.exists(os.path.join(SITE, href)):
                errs.append("index.html: service card points at missing %s" % href)
        if len(re.findall(r'class="qf__step" data-step="\d"', page_html)) != 3:
            errs.append("index.html: the quote form needs its three steps")
        for src in re.findall(r'(?:srcset|imagesrcset)="([^"]+)"', page_html):
            for part in src.split(","):
                url = part.strip().split(" ")[0]
                if url.startswith("assets/") and "/" + url not in assets:
                    errs.append("index.html: missing image %s" % url)
        # the questions are the part search engines and assistants quote, so the
        # answers on the page and the answers in the structured data must agree
        qa = re.findall(r"<summary>(.*?)</summary><div class=\"faq__a\">(.*?)</div>", page_html, re.S)
        if len(qa) < 5:
            errs.append("index.html: %d questions on the page, expected at least 5" % len(qa))
        fp = re.search(r'"@type":"FAQPage","mainEntity":\[(.*?)\]\}</script>', page_html, re.S)
        if not fp:
            errs.append("index.html: no FAQPage structured data")
        else:
            for q, a in qa:
                if q not in fp.group(1) or a not in fp.group(1):
                    errs.append("index.html: question %r is not in the FAQ structured data" % q)

    # every fragment that points at a page must match an id on that page
    ids = {}
    for p in pages:
        rel = norm(p)[len(norm(SITE)):]
        ids[rel] = set(re.findall(r'\sid="([^"]+)"', open(p, encoding="utf-8").read()))
    for p in pages:
        rel = norm(p)[len(norm(SITE)):]
        here = os.path.dirname(rel)
        for href in re.findall(r'href="([^"#]*)#([^"]+)"', open(p, encoding="utf-8").read()):
            target, frag = href
            if target.startswith(("http", "mailto:", "tel:")):
                continue
            tpath = rel if not target else "/" + norm(os.path.normpath(os.path.join(here.lstrip("/"), target)))
            if tpath in ids and frag not in ids[tpath]:
                errs.append("%s: link to %s#%s — no such id" % (rel, tpath, frag))

    # the plain-text copy for assistants has to say the same things as the page
    llms = os.path.join(SITE, "llms.txt")
    if not os.path.exists(llms):
        errs.append("llms.txt: missing")
    else:
        txt = open(llms, encoding="utf-8").read()
        for want in ("## Services", "## Coverage", "## Answers", "## Contact", "Monitoring"):
            if want not in txt:
                errs.append("llms.txt: %r missing" % want)

    for k, v in titles.items():
        if len(v) > 1:
            errs.append("duplicate title %r on %s" % (k, v))
    for _, v in descs.items():
        if len(v) > 1:
            errs.append("duplicate description on %s" % v)

    out = sorted(set(errs))
    print("\n".join(out) if out else "NO ISSUES")
    print("--- %d pages checked, %d issues" % (len(pages), len(out)))
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main())
