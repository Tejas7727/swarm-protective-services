"""Where the Toronto emblem sits in each frame of the coverage film, so the page can
draw the ripple around it live (it pulses from the first moment, at any scroll).

Mirrors camera() in SwarmCoverage.tsx: the same keyframes, the same easing
(cubic-bezier .65,0,.35,1 per segment, as Remotion's interpolate applies it) and
MapLibre's Web Mercator with 512px tiles, turned by the bearing about the centre.
Change the two together.

    toronto(shape, frames) -> [(x, y), ...] as fractions of the frame
"""
import math

TORONTO = (-79.3832, 43.6532)
CAM = {
    "w": {"size": (1440, 810), "zoom": [10.6, 10.6, 8.75, 8.75, 3.25, 3.25],
          "lng": [TORONTO[0], -79.46, -79.46, -92], "lat": [TORONTO[1], 43.7, 43.7, 50.5],
          "bear": [0, 0, -18, -18, 0]},
    "t": {"size": (720, 1280), "zoom": [10.15, 10.15, 8.4, 8.4, 2.53, 2.53],
          "lng": [TORONTO[0], -79.16, -79.16, -99], "lat": [TORONTO[1], 43.6, 43.6, 50],
          "bear": [0, 0, -25, -25, 0]},
}
T_ZOOM = [0, 0.08, 0.42, 0.56, 0.9, 1]
T_POS = [0, 0.42, 0.56, 0.9]
T_BEAR = [0, 0.08, 0.42, 0.56, 0.9]


def _bezier(x1, y1, x2, y2):
    def coord(t, a, b):
        return 3 * (1 - t) ** 2 * t * a + 3 * (1 - t) * t * t * b + t ** 3

    def ease(x):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if coord(mid, x1, x2) < x:
                lo = mid
            else:
                hi = mid
        return coord((lo + hi) / 2, y1, y2)
    return ease


EASE = _bezier(0.65, 0, 0.35, 1)


def _interp(t, xs, ys):
    if t <= xs[0]:
        return ys[0]
    for i in range(len(xs) - 1):
        if t <= xs[i + 1]:
            u = (t - xs[i]) / (xs[i + 1] - xs[i])
            return ys[i] + (ys[i + 1] - ys[i]) * EASE(u)
    return ys[-1]


def _merc(lng, lat):
    return ((lng + 180) / 360,
            (180 - 180 / math.pi * math.log(math.tan(math.pi / 4 + lat * math.pi / 360))) / 360)


def toronto(shape, frames):
    c = CAM[shape]
    W, H = c["size"]
    out = []
    for i in range(frames):
        t = i / (frames - 1)
        z = _interp(t, T_ZOOM, c["zoom"])
        cx, cy = _merc(_interp(t, T_POS, c["lng"]), _interp(t, T_POS, c["lat"]))
        px, py = _merc(*TORONTO)
        ws = 512 * 2 ** z
        dx, dy = (px - cx) * ws, (py - cy) * ws
        r = math.radians(-_interp(t, T_BEAR, c["bear"]))
        out.append(((W / 2 + dx * math.cos(r) - dy * math.sin(r)) / W,
                    (H / 2 + dx * math.sin(r) + dy * math.cos(r)) / H))
    return out


if __name__ == "__main__":
    for s in "wt":
        p = toronto(s, 72)
        print(s, ["%.3f,%.3f" % p[i] for i in (0, 20, 36, 50, 71)])
