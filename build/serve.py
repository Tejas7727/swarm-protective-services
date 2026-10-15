# -*- coding: utf-8 -*-
"""Serve docs/ locally the way Cloudflare Pages does: /about answers with
about.html, so the site's clean links work in the preview too.

    python build/serve.py [port]        (default 8150)
"""
import http.server
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs"))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def translate_path(self, path):
        p = super().translate_path(path)
        if not os.path.exists(p) and os.path.exists(p + ".html"):
            return p + ".html"
        return p


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8150
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
