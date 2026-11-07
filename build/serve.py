# -*- coding: utf-8 -*-
"""Serve docs/ locally the way Cloudflare Pages does: /about answers with
about.html, so the site's clean links work in the preview too. Byte ranges
are honoured, as on Cloudflare, so the coverage films can seek and loop.

    python build/serve.py [port]        (default 8150)
"""
import http.server
import os
import re
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

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")      # the preview always shows the latest render
        super().end_headers()

    def send_head(self):
        m = re.match(r"bytes=(\d+)-(\d*)$", self.headers.get("Range", ""))
        path = self.translate_path(self.path)
        if not m or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        a = int(m.group(1)); b = min(int(m.group(2) or size - 1), size - 1)
        f = open(path, "rb"); f.seek(a)
        self.send_response(206)
        self.send_header("Content-type", self.guess_type(path))
        self.send_header("Content-Range", "bytes %d-%d/%d" % (a, b, size))
        self.send_header("Content-Length", str(b - a + 1))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        self._left = b - a + 1
        return f

    def copyfile(self, src, dst):
        left = getattr(self, "_left", None)
        if left is None:
            return super().copyfile(src, dst)
        self._left = None
        while left > 0:
            buf = src.read(min(65536, left))
            if not buf:
                break
            dst.write(buf); left -= len(buf)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8150
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
