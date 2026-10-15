# -*- coding: utf-8 -*-
"""Render the site into ../docs/ (the folder GitHub Pages serves).

    python build/build.py                 # production build
    python build/build.py --preview URL   # client preview: noindex + preview canonicals
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.abspath(os.path.join(HERE, "..", "docs"))

import common                       # noqa: E402

if "--preview" in sys.argv:
    i = sys.argv.index("--preview")
    common.MODE["preview"] = True
    common.MODE["preview_base"] = sys.argv[i + 1] if len(sys.argv) > i + 1 else ""

import about, coverage, front, journal, pages, services, service_art   # noqa: E402
sys.path.insert(0, os.path.join(HERE, "cinema"))
import assets as scene_assets        # noqa: E402


# Cloudflare Pages (and GitHub Pages) serve about.html at /about and redirect
# the .html form, so every internal link is written in the clean form: no
# redirect on a click, and the URL people share is the one search engines index.
LINK = re.compile(r'href="(?!https?:|mailto:|tel:|//|#)([^"#?]*?)(index)?\.html([?#][^"]*)?"')


def clean_links(html):
    def fix(m):
        path, idx, tail = m.group(1), m.group(2), m.group(3) or ""
        return 'href="%s%s"' % ((path or "./") if idx else path, tail)
    return LINK.sub(fix, html)


def clean_url(rel):
    """docs-relative file -> the clean public path."""
    if rel.endswith("index.html"):
        return "/" + rel[:-len("index.html")]
    return "/" + rel[:-len(".html")] if rel.endswith(".html") else "/" + rel


def write(rel, text):
    if rel.endswith(".html"):
        text = clean_links(text)
    path = os.path.join(OUT, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return rel, len(text)


def llms_txt(base):
    """The site in plain text, for assistants that answer instead of linking.

    Same facts as the page, in the order someone would ask for them. Short on
    purpose: an assistant quotes a sentence, so every sentence has to stand up
    on its own.
    """
    import content as C                                           # noqa: E402
    B = common.BIZ
    out = ["# %s" % B["name"], "",
           "> Licensed security company in Toronto and the Greater Toronto Area: event security, "
           "bar and nightclub door staff, close protection, and monitoring for homes and "
           "businesses. PSISA-licensed officers, $5M insured, WSIB covered. Based in Toronto; "
           "we travel with clients anywhere in Canada.", "",
           "Motto: %s." % C.HOME["motto"], "",
           "## Services", ""]
    out += ["- **%s** — %s. [Details](%s/%s)" % (name, line, base, slug)
            for slug, name, line in C.SERVICES["items"]]
    out += ["", "## Coverage", "",
            "- %s %s" % (C.COVERAGE["line"], C.COVERAGE["national"]),
            "- Cities: %s." % ", ".join(common.AREAS), "",
            "## Licences and insurance", ""]
    out += ["- %s" % c for c in C.SERVICES["creds"]]
    out += ["- Officers are not armed: Ontario does not permit private security to carry firearms.",
            "", "## Answers", ""]
    out += ["- **%s** %s" % qa for qa in C.FAQ["items"]]
    out += ["", "## Contact", "",
            "- Phone: %s (answered 24/7)" % B["phone_ui"],
            "- Email: %s" % B["email"],
            "- Quote form: %s/#contact" % base,
            "- Prices are quoted per job; nothing is published.", "",
            "## More", "",
            "- [Meet us](%s/about.html): who turns up and the standard they are held to." % base,
            "- [Coverage](%s/coverage.html): the 18 GTA cities we cover, and travel across Canada." % base,
            "- [Answers](%s/answers.html): the longer answers to these questions." % base,
            "- [Journal](%s/journal/): field notes for venue owners and event organisers." % base,
            "- [Privacy](%s/privacy.html): what we keep and for how long." % base, ""]
    return "\n".join(out)


def main():
    scene_assets.build()             # plates + camera manifest, before the page reads it
    service_art.build()              # one photograph per service page
    files = {"index.html": front.render()}
    files.update(pages.PAGES)
    files.update(services.pages())
    files.update(about.PAGES)
    files.update(coverage.PAGES)
    files.update(journal.pages())

    written = [write(rel, html) for rel, html in sorted(files.items())]

    base = common.BIZ["base"]
    urls = []
    for rel, _ in written:
        if rel == "404.html":
            continue
        loc = clean_url(rel)
        pri = "1.0" if loc == "/" else "0.7"
        urls.append('<url><loc>%s%s</loc><changefreq>monthly</changefreq>'
                    '<priority>%s</priority></url>' % (base, loc, pri))
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n'
          % "\n".join(urls))

    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % base)

    write("llms.txt", llms_txt(base))

    write("site.webmanifest",
          '{"name":"%s","short_name":"Swarm","start_url":"./","display":"standalone",'
          '"background_color":"#08090A","theme_color":"#08090A","icons":['
          '{"src":"assets/icon/favicon-180.png","sizes":"180x180","type":"image/png"},'
          '{"src":"assets/icon/favicon-512.png","sizes":"512x512","type":"image/png"}]}'
          % common.BIZ["name"])

    # GitHub Pages: stop Jekyll eating files, and serve the SPA-less 404
    write(".nojekyll", "")

    # CSS and JS carry a content hash in their URL (?v=), so they can be kept a
    # year. Images keep their names when they are re-exported, so a week.
    write("_headers",
          "/assets/css/*\n  Cache-Control: public, max-age=31536000, immutable\n"
          "/assets/js/*\n  Cache-Control: public, max-age=31536000, immutable\n"
          "/assets/cine/*\n  Cache-Control: public, max-age=31536000, immutable\n"
          "/assets/img/*\n  Cache-Control: public, max-age=604800\n"
          "/assets/scene/*\n  Cache-Control: public, max-age=604800\n"
          "/assets/logo/*\n  Cache-Control: public, max-age=604800\n"
          "/assets/icon/*\n  Cache-Control: public, max-age=604800\n"
          "/assets/og/*\n  Cache-Control: public, max-age=604800\n"
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
