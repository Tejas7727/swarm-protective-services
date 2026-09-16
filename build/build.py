# -*- coding: utf-8 -*-
"""Render the site into ../docs/ (the folder GitHub Pages serves).

    python build/build.py                 # production build
    python build/build.py --preview URL   # client preview: noindex + preview canonicals
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.abspath(os.path.join(HERE, "..", "docs"))

import common                       # noqa: E402

if "--preview" in sys.argv:
    i = sys.argv.index("--preview")
    common.MODE["preview"] = True
    common.MODE["preview_base"] = sys.argv[i + 1] if len(sys.argv) > i + 1 else ""

import home, journal, pages         # noqa: E402


def write(rel, text):
    path = os.path.join(OUT, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return rel, len(text)


def main():
    files = {"index.html": home.build()}
    files.update(pages.PAGES)
    files.update(journal.pages())

    written = [write(rel, html) for rel, html in sorted(files.items())]

    base = common.BIZ["base"]
    urls = []
    for rel, _ in written:
        if rel == "404.html":
            continue
        loc = "/" if rel == "index.html" else "/" + rel.replace("journal/index.html", "journal/")
        pri = "1.0" if loc == "/" else "0.7"
        urls.append('<url><loc>%s%s</loc><changefreq>monthly</changefreq>'
                    '<priority>%s</priority></url>' % (base, loc, pri))
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n'
          % "\n".join(urls))

    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % base)

    write("site.webmanifest",
          '{"name":"%s","short_name":"Swarm","start_url":"./","display":"standalone",'
          '"background_color":"#08090A","theme_color":"#08090A","icons":['
          '{"src":"assets/icon/favicon-180.png","sizes":"180x180","type":"image/png"},'
          '{"src":"assets/icon/favicon-512.png","sizes":"512x512","type":"image/png"}]}'
          % common.BIZ["name"])

    # GitHub Pages: stop Jekyll eating files, and serve the SPA-less 404
    write(".nojekyll", "")

    write("_headers",
          "/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n"
          "/*\n  X-Content-Type-Options: nosniff\n"
          "  Referrer-Policy: strict-origin-when-cross-origin\n"
          "  X-Frame-Options: SAMEORIGIN\n"
          "  Permissions-Policy: geolocation=(), microphone=(), camera=()\n")

    total = 0
    for rel, n in written:
        total += n
        print("  %-46s %6.1f KB" % (rel, n / 1024))
    print("  %-46s %6.1f KB" % ("TOTAL HTML", total / 1024))
    mode = "PREVIEW (noindex)" if common.MODE["preview"] else "production"
    print("%d pages -> %s  [%s]" % (len(written), OUT, mode))


if __name__ == "__main__":
    main()
