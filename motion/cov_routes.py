"""The coverage routes, drawn live by the page (an SVG over the film) instead of baked
into video, so they start drawing the instant the GTA or Canada framing is reached.

Each route is one path in the beat's own frame pixels. Between any two camera
positions the map moves by a similarity (scale, turn, shift), so every film frame
gets a matrix that carries the beat's paths onto that frame: the lines stay pinned
to the map while the camera eases in and out. They draw over a window of frames
(WINDOW) that opens while the camera is still arriving. The SVG uses the frame size
as its viewBox with `slice`, the same cover crop the canvas draws.

Geometry mirrors SwarmCoverage.tsx: a gentle bow to each GTA city (westward routes
bow north), great circles across Canada, routes only to named cities. Each route
starts where it leaves the emblem's own outline (its alpha, plus a hair of gap), so
the lines almost touch the shield. Change the two together.

    svg(shape) -> '<svg ...>...</svg>'   shape "w" (1440x810) or "t" (720x1280)
"""
import math
import os

from PIL import Image, ImageFilter

from cov_toronto import CAM, T_BEAR, T_POS, T_ZOOM, TORONTO, _interp, _merc

GTA = {"Mississauga": (-79.6441, 43.589), "Brampton": (-79.7624, 43.7315), "Milton": (-79.8774, 43.5183),
       "Oakville": (-79.6877, 43.4675), "Vaughan": (-79.4983, 43.8361), "Richmond Hill": (-79.4403, 43.8828),
       "Markham": (-79.337, 43.8561), "Oshawa": (-78.8658, 43.8971), "Newmarket": (-79.4613, 44.0592)}
CANADA = {"Vancouver": (-123.1207, 49.2827), "Calgary": (-114.0719, 51.0447), "Edmonton": (-113.4938, 53.5461),
          "Yellowknife": (-114.3718, 62.454), "Winnipeg": (-97.1384, 49.8951), "Montréal": (-73.5673, 45.5017),
          "Halifax": (-63.5752, 44.6488), "St. John's": (-52.7126, 47.5615)}
ROUTES = {
    "w": {"gta": ["Mississauga", "Brampton", "Milton", "Vaughan", "Richmond Hill", "Markham", "Oshawa", "Newmarket"],
          "canada": ["Vancouver", "Calgary", "Edmonton", "Yellowknife", "Winnipeg", "Montréal", "Halifax", "St. John's"]},
    "t": {"gta": ["Mississauga", "Brampton", "Oakville", "Vaughan", "Markham", "Oshawa", "Newmarket"],
          "canada": ["Vancouver", "Edmonton", "Yellowknife", "Winnipeg", "Halifax"]},
}
BEAT_T = {"gta": 36 / 71, "canada": 1.0}
WINDOW = {"gta": (0.30, 0.60), "canada": (0.86, 1.0)}     # t where each set is drawn out
FRAMES = 72


def bow(a, b, k=0.22, n=48):
    mx, my, dx, dy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, b[0] - a[0], b[1] - a[1]
    w = -1 if dx < 0 else 1
    c = (mx - w * dy * k * 1.35, my + w * dx * k * 0.74)
    out = []
    for i in range(n + 1):
        u = i / n
        v = 1 - u
        out.append((v * v * a[0] + 2 * v * u * c[0] + u * u * b[0], v * v * a[1] + 2 * v * u * c[1] + u * u * b[1]))
    return out


def great(a, b, n=80):
    def vec(p):
        lo, la = math.radians(p[0]), math.radians(p[1])
        return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))
    p, q = vec(a), vec(b)
    om = math.acos(max(-1, min(1, sum(x * y for x, y in zip(p, q)))))
    out = []
    for i in range(n):
        u = i / (n - 1)
        s1, s2 = math.sin((1 - u) * om) / math.sin(om), math.sin(u * om) / math.sin(om)
        x, y, z = (s1 * p[j] + s2 * q[j] for j in range(3))
        out.append((math.degrees(math.atan2(y, x)), math.degrees(math.atan2(z, math.hypot(x, y)))))
    return out


def projector(shape, t):
    c = CAM[shape]
    W, H = c["size"]
    z = _interp(t, T_ZOOM, c["zoom"])
    cx, cy = _merc(_interp(t, T_POS, c["lng"]), _interp(t, T_POS, c["lat"]))
    r = math.radians(-_interp(t, T_BEAR, c["bear"]))
    ws = 512 * 2 ** z

    def proj(p):
        x, y = _merc(*p)
        dx, dy = (x - cx) * ws, (y - cy) * ws
        return (W / 2 + dx * math.cos(r) - dy * math.sin(r), H / 2 + dx * math.sin(r) + dy * math.cos(r))
    return proj


def camera(shape, t):
    c = CAM[shape]
    z = _interp(t, T_ZOOM, c["zoom"])
    m = _merc(_interp(t, T_POS, c["lng"]), _interp(t, T_POS, c["lat"]))
    return 512 * 2 ** z, math.radians(-_interp(t, T_BEAR, c["bear"])), m


def carry(shape, tb, tk):
    """The matrix (SVG a b c d e f) that takes frame-pixel points at camera tb to camera tk."""
    W, H = CAM[shape]["size"]
    C = (W / 2, H / 2)
    sb, rb, mb = camera(shape, tb)
    sk, rk, mk = camera(shape, tk)
    k, th = sk / sb, rk - rb
    a, b, c, d = k * math.cos(th), k * math.sin(th), -k * math.sin(th), k * math.cos(th)
    vx, vy = (mb[0] - mk[0]) * sk, (mb[1] - mk[1]) * sk               # Sk (mb - mk), then turned by rk
    tx, ty = vx * math.cos(rk) - vy * math.sin(rk), vx * math.sin(rk) + vy * math.cos(rk)
    e = C[0] + tx - (a * C[0] + c * C[1])
    f = C[1] + ty - (b * C[0] + d * C[1])
    return a, b, c, d, e, f


EMBLEM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "assets", "logo", "emblem-216.webp")


def shield(o, s, gap=3.0):
    """inside(x, y): is this frame point on the emblem (drawn 46*s wide, centred on o and
    lifted 54% as SwarmCoverage.tsx draws it), grown by `gap` frame pixels?"""
    im = Image.open(EMBLEM).convert("RGBA")
    f = 46 * s / im.width                                        # frame px per image px
    grow = max(1, round(gap / f)) * 2 + 1
    a = im.getchannel("A").point(lambda v: 255 if v > 40 else 0).filter(ImageFilter.MaxFilter(grow))
    left, top = o[0] - im.width * f / 2, o[1] - im.height * f * 0.54

    def inside(x, y):
        u, v = int((x - left) / f), int((y - top) / f)
        return 0 <= u < im.width and 0 <= v < im.height and a.getpixel((u, v)) > 0
    return inside


def clip_shield(pts, inside, step=0.25):
    """The polyline from where it last leaves the shield (walked in small steps)."""
    out = None
    for i in range(1, len(pts)):
        a, b = pts[i - 1], pts[i]
        n = max(1, int(math.dist(a, b) / step))
        for j in range(n + 1):
            q = (a[0] + (b[0] - a[0]) * j / n, a[1] + (b[1] - a[1]) * j / n)
            if inside(*q):
                out = (i, q)
    if out is None:
        return pts
    i, q = out
    return [q] + pts[i:]


def svg(shape):
    W, H = CAM[shape]["size"]
    s = 1.75 if shape == "t" else 1
    groups = []
    for beat, cities in ROUTES[shape].items():
        proj = projector(shape, BEAT_T[beat])
        o = proj(TORONTO)
        inside = shield(o, s)
        lines = []
        for name in cities:
            p = GTA[name] if beat == "gta" else CANADA[name]
            geo = bow(TORONTO, p) if beat == "gta" else great(TORONTO, p)
            pts = clip_shield([proj(q) for q in geo], inside)
            ang = math.atan2(pts[-1][1] - o[1], pts[-1][0] - o[0])
            lines.append((ang, "M" + " ".join("%.1f %.1f" % q for q in pts)))
        # they draw in a sweep around the emblem, west first, then north, then east
        lines.sort(key=lambda a: (a[0] - math.pi / 2) % (2 * math.pi))
        paths = "".join('<path pathLength="1" style="--i:%d" d="%s"/>' % (i, d) for i, (_, d) in enumerate(lines))
        lo, hi = WINDOW[beat]
        on = [i for i in range(FRAMES) if lo - 1e-9 <= i / (FRAMES - 1) <= hi + 1e-9]
        # matrices run a few frames past the window, so a set fading out still rides the map
        ks = range(max(0, on[0] - 8), min(FRAMES, on[-1] + 9))
        mats = ";".join("%.5f %.5f %.5f %.5f %.1f %.1f" % carry(shape, BEAT_T[beat], i / (FRAMES - 1)) for i in ks)
        groups.append('<g data-beat="%s" data-k0="%d" data-on="%d %d" data-x="%s">%s</g>'
                      % (beat, ks[0], on[0], on[-1], mats, paths))
    return ('<svg class="cov__routes cov__routes--%s" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice" '
            'aria-hidden="true">%s</svg>' % (shape, W, H, "".join(groups)))


if __name__ == "__main__":
    for sh in "wt":
        print(sh, len(svg(sh)))
