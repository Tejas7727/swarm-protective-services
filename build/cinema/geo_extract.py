# -*- coding: utf-8 -*-
"""Turn Natural Earth geodata into the map drawings this site uses.

Run once; it writes `build/cinema/geo.json`, which the build reads. The source
files are not in the repo (85 MB); fetch them first:

    curl -O https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_lakes.geojson
    curl -O .../ne_10m_urban_areas.geojson
    curl -O .../ne_10m_roads.geojson
    curl -O .../ne_50m_admin_0_countries.geojson
    curl -O .../ne_50m_admin_1_states_provinces_lakes.geojson

    python build/cinema/geo_extract.py --src <folder with those files>

Natural Earth is public domain (no permission, no attribution required) and is
the same data most printed reference maps start from, so the shoreline, the
built-up areas and the 400-series highways are the real ones.

Two drawings come out:

  gta     the Golden Horseshoe in an equirectangular projection, scaled by
          cos(43.65 deg) so shapes are true at this latitude: Lake Ontario and
          Lake Simcoe, the built-up areas, and the expressways.
  canada  the country in an Albers conic, for "we travel with you", with the
          provinces faint and Toronto where it really is.
"""
import argparse
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# --- the Golden Horseshoe window -------------------------------------------
LON_W, LAT_N, LON_E, LAT_S = -81.30, 44.70, -77.80, 42.80
LAT_C = 43.65
K = 1000.0                                     # svg units per degree of latitude
KX = K * math.cos(math.radians(LAT_C))

# --- Canada, Albers equal-area conic ---------------------------------------
CA_LON0, CA_LAT0, CA_P1, CA_P2 = -95.0, 49.0, 50.0, 70.0
CA_K = 1.0


def gta_xy(lat, lon):
    return ((lon - LON_W) * KX, (LAT_N - lat) * K)


def albers(lat, lon):
    p1, p2, l0, f0 = (math.radians(v) for v in (CA_P1, CA_P2, CA_LON0, CA_LAT0))
    n = 0.5 * (math.sin(p1) + math.sin(p2))
    c = math.cos(p1) ** 2 + 2 * n * math.sin(p1)
    r0 = math.sqrt(c - 2 * n * math.sin(f0)) / n
    f, l = math.radians(lat), math.radians(lon)
    r = math.sqrt(c - 2 * n * math.sin(f)) / n
    t = n * (l - l0)
    return (r * math.sin(t) * 1000.0, (r0 - r * math.cos(t)) * -1000.0)


def simplify(pts, tol):
    """Ramer-Douglas-Peucker, iterative."""
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = pts[a]
        bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        n = math.hypot(dx, dy)
        worst, wi = -1.0, -1
        for i in range(a + 1, b):
            px, py = pts[i]
            # a closed ring starts and ends on the same point: measure from it
            d = math.hypot(px - ax, py - ay) if n < 1e-9 else abs(dy * (px - ax) - dx * (py - ay)) / n
            if d > worst:
                worst, wi = d, i
        if wi > 0 and worst > tol:
            keep[wi] = True
            stack.append((a, wi))
            stack.append((wi, b))
    return [p for p, k in zip(pts, keep) if k]


def clip_poly(pts, box):
    """Sutherland-Hodgman against (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    for edge in range(4):
        if not pts:
            return []
        out = []
        n = len(pts)
        for i in range(n):
            cx, cy = pts[i]
            px, py = pts[(i - 1) % n]

            def inside(x, y, e=edge):
                return (x >= x0, x <= x1, y >= y0, y <= y1)[e]

            def cross(xa, ya, xb, yb, e=edge):
                if e < 2:
                    xe = x0 if e == 0 else x1
                    return (xe, ya + (yb - ya) * (xe - xa) / (xb - xa))
                ye = y0 if e == 2 else y1
                return (xa + (xb - xa) * (ye - ya) / (yb - ya), ye)

            ci, pi = inside(cx, cy), inside(px, py)
            if ci:
                if not pi:
                    out.append(cross(px, py, cx, cy))
                out.append((cx, cy))
            elif pi:
                out.append(cross(px, py, cx, cy))
        pts = out
    return pts


def clip_line(pts, box):
    """Split a line into the pieces that fall inside the box."""
    x0, y0, x1, y1 = box
    runs, cur = [], []
    for p in pts:
        if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
            cur.append(p)
        else:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
    if len(cur) > 1:
        runs.append(cur)
    return runs


def path(pts, close=False, dp=1):
    f = "%." + str(dp) + "f"
    d = "M" + (" L".join((f + " " + f) % (x, y) for x, y in pts))
    return d + (" Z" if close else "")


def rings(geom):
    t, c = geom["type"], geom["coordinates"]
    if t == "Polygon":
        return [c[0]]
    if t == "MultiPolygon":
        return [p[0] for p in c]
    if t == "LineString":
        return [c]
    if t == "MultiLineString":
        return list(c)
    return []


def touches(ring, bb):
    return any(bb[0] <= x <= bb[2] and bb[1] <= y <= bb[3] for x, y in ring)


def load(src, name):
    with open(os.path.join(src, name + ".geojson" if os.path.exists(
            os.path.join(src, name + ".geojson")) else name + ".json"), encoding="utf-8") as fh:
        return json.load(fh)["features"]


def build(src):
    bb = (LON_W, LAT_S, LON_E, LAT_N)
    box = (0.0, 0.0, (LON_E - LON_W) * KX, (LAT_N - LAT_S) * K)
    out = {"gta": {"w": round(box[2]), "h": round(box[3]),
                   "proj": {"lon_w": LON_W, "lat_n": LAT_N, "k": K, "kx": KX}}}

    lakes, lake_names = [], []
    for f in load(src, "ne_10m_lakes"):
        nm = f["properties"].get("name") or ""
        if nm not in ("Lake Ontario", "Lake Simcoe", "Lake Erie"):
            continue
        for r in rings(f["geometry"]):
            if not touches(r, bb):
                continue
            pts = clip_poly([gta_xy(la, lo) for lo, la in r], box)
            pts = simplify(pts, 2.2)
            if len(pts) > 3:
                lakes.append(path(pts, True))
                lake_names.append(nm)
    out["gta"]["lake"] = lakes
    out["gta"]["lake_names"] = lake_names

    urban = []
    for f in load(src, "ne_10m_urban_areas"):
        if f["properties"].get("area_sqkm", 0) < 12:
            continue
        for r in rings(f["geometry"]):
            if not touches(r, bb):
                continue
            pts = clip_poly([gta_xy(la, lo) for lo, la in r], box)
            pts = simplify(pts, 3.0)
            if len(pts) > 3:
                urban.append(path(pts, True, 0))
    out["gta"]["urban"] = urban

    hwy = {}
    for f in load(src, "ne_10m_roads"):
        p = f["properties"]
        if p.get("expressway") != 1 or (p.get("continent") or "North America") != "North America":
            continue
        nm = (p.get("name") or "").strip()
        if nm not in ("401", "400", "403", "404", "407", "409", "410", "427", "QEW", "115", "7", "12", "11"):
            continue
        for r in rings(f["geometry"]):
            if not touches(r, bb):
                continue
            for run in clip_line([gta_xy(la, lo) for lo, la in r], box):
                run = simplify(run, 2.0)
                if len(run) > 1:
                    hwy.setdefault(nm, []).append(path(run, False, 0))
    out["gta"]["hwy"] = [{"n": k, "d": v} for k, v in sorted(hwy.items())]

    prov = []
    for f in load(src, "ne_50m_admin_1_states_provinces_lakes"):
        if f["properties"].get("admin") != "Canada":
            continue
        for r in rings(f["geometry"]):
            pts = simplify([albers(la, lo) for lo, la in r], 10.0)
            if len(pts) > 6:
                prov.append(path(pts, True, 0))
    ca = []
    for f in load(src, "ne_50m_admin_0_countries"):
        if (f["properties"].get("ADMIN") or f["properties"].get("admin")) != "Canada":
            continue
        for r in rings(f["geometry"]):
            pts = simplify([albers(la, lo) for lo, la in r], 5.0)
            if len(pts) > 20:
                ca.append(path(pts, True, 0))
    xs = [p for d in ca for p in _pts(d)]
    x0 = min(x for x, y in xs)
    y0 = min(y for x, y in xs)
    x1 = max(x for x, y in xs)
    y1 = max(y for x, y in xs)
    out["canada"] = {"outline": ca, "prov": prov,
                     "box": [round(x0), round(y0), round(x1 - x0), round(y1 - y0)],
                     "toronto": [round(v) for v in albers(43.6532, -79.3832)],
                     "cities": {n: [round(v) for v in albers(la, lo)] for n, la, lo in (
                         ("Vancouver", 49.2827, -123.1207), ("Calgary", 51.0447, -114.0719),
                         ("Winnipeg", 49.8951, -97.1384), ("Ottawa", 45.4215, -75.6972),
                         ("Montréal", 45.5019, -73.5674), ("Halifax", 44.6488, -63.5752))}}
    return out


def _pts(d):
    for seg in d.replace("M", " ").replace("Z", " ").split("L"):
        seg = seg.strip()
        if not seg:
            continue
        a, b = seg.split()
        yield (float(a), float(b))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", default=os.path.join(HERE, "geo.json"))
    a = ap.parse_args()
    geo = build(a.src)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(geo, fh, separators=(",", ":"), sort_keys=True)
    g = geo["gta"]
    print("gta %dx%d  lakes %d  urban %d  hwy %s" % (
        g["w"], g["h"], len(g["lake"]), len(g["urban"]), ",".join(h["n"] for h in g["hwy"])))
    print("canada box %s  outline %d  prov %d" % (geo["canada"]["box"], len(geo["canada"]["outline"]),
                                                  len(geo["canada"]["prov"])))
    print("geo.json %.1f KB" % (os.path.getsize(a.out) / 1024.0))
