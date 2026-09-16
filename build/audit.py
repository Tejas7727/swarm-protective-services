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
        for cls in ("reveal", "parallax", "frame__zoom", "ticker", "beeflight", "rise"):
            if ("." + cls) in css and ('class="' + cls) not in html_all                     and (" " + cls + '"') not in html_all and (" " + cls + " ") not in html_all:
                errs.append("css: .%s is styled but never used in any page" % cls)

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
