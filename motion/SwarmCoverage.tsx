// Swarm Protective Services: the coverage map films.
//  * SwarmCoverageWide/Tall: the camera move, scrubbed by scroll on coverage.html
//    (Toronto -> the GTA -> Canada). Routes are not drawn here: they draw in the hold films.
//  * SwarmCoverageHold{Gta,Canada}*: what plays once the scroll rests on a beat, from that
//    beat's exact frame: the routes to the named cities curve out slowly from just outside
//    the emblem, then hold. The ripple around the emblem is drawn live by the page (swarm.js),
//    so it pulses from the first moment; cov_toronto.py gives the page the emblem's position.
// Tiles: OpenFreeMap (OpenMapTiles schema, OpenStreetMap data); the page carries the attribution.
import * as turf from "@turf/turf";
import { useEffect, useRef, useState } from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  staticFile,
  useCurrentFrame,
  useDelayRender,
  useVideoConfig,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Saira";
import * as maplibregl from "maplibre-gl";
import { type GeoJSONSource, type Map } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

const { fontFamily } = loadFont("normal", { weights: ["600", "700"], subsets: ["latin"] });

type LngLat = [number, number];
const TORONTO: LngLat = [-79.3832, 43.6532];
const GTA: Array<[string, LngLat]> = [
  ["Etobicoke", [-79.5132, 43.6205]], ["North York", [-79.4111, 43.7615]], ["Scarborough", [-79.2318, 43.7764]],
  ["Mississauga", [-79.6441, 43.589]], ["Brampton", [-79.7624, 43.7315]], ["Vaughan", [-79.4983, 43.8361]],
  ["Markham", [-79.337, 43.8561]], ["Richmond Hill", [-79.4403, 43.8828]], ["Oakville", [-79.6877, 43.4675]],
  ["Burlington", [-79.799, 43.3255]], ["Hamilton", [-79.8711, 43.2557]], ["Pickering", [-79.0868, 43.8384]],
  ["Ajax", [-79.0204, 43.8509]], ["Whitby", [-78.9429, 43.8975]], ["Oshawa", [-78.8658, 43.8971]],
  ["Milton", [-79.8774, 43.5183]], ["Newmarket", [-79.4613, 44.0592]],
];
// a route only to a city that is named; the other dots stay as the rest of the 17
const GTA_LABELS = new Set(["Mississauga", "Brampton", "Vaughan", "Markham", "Oshawa", "Newmarket"]);
const GTA_LABELS_TALL = new Set(["Mississauga", "Brampton", "Markham", "Oshawa", "Newmarket"]);
const CAN_LABELS_TALL = new Set(["Vancouver", "Winnipeg", "Halifax"]);
const CAN_LABELS = new Set(["Vancouver", "Calgary", "Edmonton", "Winnipeg", "Montréal", "Halifax"]);
// Montréal and Ottawa sit inside the emblem's clearance at Canada's zoom: named, no route
const CAN_ROUTES = new Set(["Vancouver", "Calgary", "Edmonton", "Winnipeg", "Halifax"]);
// west of Toronto the name sits to the left of its dot, so it never runs into the routes
// on a tall screen these names sit above their dots, clear of the edges
const ABOVE_TALL = new Set(["Winnipeg", "Halifax", "Mississauga", "Brampton", "Oshawa"]);
const BELOW_TALL = new Set(["Vancouver"]);
const LEFT = new Set(["Mississauga", "Brampton", "Vaughan", "Milton", "Oakville", "Hamilton", "Vancouver", "Calgary", "Edmonton", "Winnipeg"]);
const CANADA: Array<[string, LngLat]> = [
  ["Vancouver", [-123.1207, 49.2827]], ["Calgary", [-114.0719, 51.0447]], ["Edmonton", [-113.4938, 53.5461]],
  ["Winnipeg", [-97.1384, 49.8951]], ["Ottawa", [-75.6972, 45.4215]], ["Montréal", [-73.5673, 45.5017]],
  ["Halifax", [-63.5752, 44.6488]],
];

const GOLD = "#C9A35E";
const BONE = "#E7E4D3";

// a gentle bow from Toronto to each GTA city (a quadratic curve, bulging to one side)
const bow = (a: LngLat, b: LngLat, k = 0.22, n = 48) => {
  const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1];
  const c: LngLat = [mx - dy * k * 1.35, my + dx * k * 0.74];      // perpendicular, scaled for latitude
  const pts: number[][] = [];
  for (let i = 0; i <= n; i++) {
    const u = i / n, v = 1 - u;
    pts.push([v * v * a[0] + 2 * v * u * c[0] + u * u * b[0], v * v * a[1] + 2 * v * u * c[1] + u * u * b[1]]);
  }
  return turf.lineString(pts);
};
const routesTo = (list: Array<[string, LngLat]>, keep: Set<string>) => list.filter(([n]) => keep.has(n));
const gtaW = routesTo(GTA, GTA_LABELS).map(([, p]) => bow(TORONTO, p));
const gtaT = routesTo(GTA, GTA_LABELS_TALL).map(([, p]) => bow(TORONTO, p));
const great = (list: Array<[string, LngLat]>) => list.map(([, p]) => {
  const g = turf.greatCircle(TORONTO, p, { npoints: 80 });
  return turf.lineString(g.geometry.type === "LineString" ? g.geometry.coordinates : (g.geometry.coordinates as number[][][])[0]);
});
const canW = great(routesTo(CANADA, CAN_ROUTES));
const canT = great(routesTo(CANADA, new Set([...CAN_ROUTES].filter((n) => CAN_LABELS_TALL.has(n)))));

const clamp = (x: number) => Math.min(1, Math.max(0, x));
const ease = Easing.bezier(0.65, 0, 0.35, 1);

// the camera: Toronto close, the GTA, Canada; zoom is already logarithmic so it interpolates evenly.
// On the GTA beat the map turns 18 degrees, so the cities fan out above the poster line
// instead of along it (Mississauga comes level with Toronto). Mirrored in cov_toronto.py.
const CAM = {
  wide: { zoom: [10.6, 10.6, 8.75, 8.75, 3.25, 3.25], lng: [TORONTO[0], -79.46, -79.46, -92], lat: [TORONTO[1], 43.7, 43.7, 50.5] },
  tall: { zoom: [10.15, 10.15, 8.4, 8.4, 2.53, 2.53], lng: [TORONTO[0], -79.16, -79.16, -99], lat: [TORONTO[1], 43.6, 43.6, 50] },
};
const BEAR = { wide: [0, 0, -18, -18, 0], tall: [0, 0, -25, -25, 0] };
const camera = (t: number, portrait: boolean) => {
  const c = CAM[portrait ? "tall" : "wide"];
  const o = { easing: ease, extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
  const zoom = interpolate(t, [0, 0.08, 0.42, 0.56, 0.9, 1], c.zoom, o);
  const lng = interpolate(t, [0, 0.42, 0.56, 0.9], c.lng, o);
  const lat = interpolate(t, [0, 0.42, 0.56, 0.9], c.lat, o);
  const bearing = interpolate(t, [0, 0.08, 0.42, 0.56, 0.9], BEAR[portrait ? "tall" : "wide"], o);
  return { center: [lng, lat] as LngLat, zoom, bearing };
};

// where each hold sits on the camera move, and its own clock
type Beat = "toronto" | "gta" | "canada";
const BEAT_T: Record<Beat, number> = { toronto: 0, gta: 36 / 71, canada: 1 };
const none = turf.featureCollection([] as ReturnType<typeof turf.lineString>[]);
// each route starts at the edge of the emblem's clearance (gap km), never inside the logo
const drawn = (rs: ReturnType<typeof turf.lineString>[], gap: number, f: number) =>
  turf.featureCollection(rs.map((r, i) => {
    const len = turf.length(r), k = clamp((f - 6 - i * (54 / rs.length)) / 40);   // in turn, each over 40 frames
    return turf.lineSliceAlong(r, gap, gap + Math.max(0.0005, (len - gap) * ease(k)));
  }));
// km covered by `px` frame pixels at this zoom, at Toronto's latitude (MapLibre's 512px tiles)
const kmAt = (px: number, zoom: number) => (px * 40075.016686 * Math.cos((TORONTO[1] * Math.PI) / 180)) / (512 * 2 ** zoom);

export const SwarmCoverage: React.FC<{ hold?: Beat }> = ({ hold }) => {
  const ref = useRef<HTMLDivElement>(null);
  const frame = useCurrentFrame();
  const { width, height, durationInFrames } = useVideoConfig();
  const portrait = height > width;
  const { delayRender, continueRender } = useDelayRender();
  const [map, setMap] = useState<Map | null>(null);
  const [boot] = useState(() => delayRender("Loading the map"));
  const [pts, setPts] = useState<Record<string, { x: number; y: number }>>({});
  const t = hold ? BEAT_T[hold] : frame / (durationInFrames - 1);

  useEffect(() => {
    if (!ref.current) return;
    maplibregl.setWorkerUrl(
      URL.createObjectURL(
        new Blob([`import "https://unpkg.com/maplibre-gl@${maplibregl.getVersion()}/dist/maplibre-gl-worker.mjs";`], {
          type: "text/javascript",
        }),
      ),
    );
    const m = new maplibregl.Map({
      container: ref.current,
      style: "https://tiles.openfreemap.org/styles/dark",
      ...camera(0, portrait),
      interactive: false,
      attributionControl: false,
      fadeDuration: 0,
      canvasContextAttributes: { preserveDrawingBuffer: true },
    });
    m.on("load", () => {
      // our own labels only; the brand's charcoal, with the water a shade cooler
      for (const l of m.getStyle().layers) {
        if (l.type === "symbol") m.removeLayer(l.id);
      }
      m.setPaintProperty("background", "background-color", "#0A0C0E");
      m.setPaintProperty("water", "fill-color", "#0F151B");
      m.addSource("gta", { type: "geojson", data: none });
      m.addLayer({ id: "gta", type: "line", source: "gta", layout: { "line-cap": "round" },
        paint: { "line-color": GOLD, "line-width": portrait ? 2.4 : 2, "line-opacity": 0.9 } });
      m.addSource("can", { type: "geojson", data: none });
      m.addLayer({ id: "can", type: "line", source: "can", layout: { "line-cap": "round" },
        paint: { "line-color": GOLD, "line-width": portrait ? 2.6 : 2.2, "line-opacity": 0.95 } });
      m.addSource("dots", { type: "geojson", data: turf.featureCollection(GTA.map(([n, p]) => turf.point(p, { n }))) });
      m.addLayer({ id: "dots", type: "circle", source: "dots",
        paint: { "circle-color": GOLD, "circle-radius": portrait ? 4.5 : 3.6, "circle-opacity": 0 } });
      m.addSource("cdots", { type: "geojson", data: turf.featureCollection(CANADA.map(([n, p]) => turf.point(p, { n }))) });
      m.addLayer({ id: "cdots", type: "circle", source: "cdots",
        paint: { "circle-color": GOLD, "circle-radius": portrait ? 5.5 : 4.5, "circle-opacity": 0 } });
      m.jumpTo(camera(0, portrait));
      m.once("idle", () => {
        setMap(m);
        continueRender(boot);
      });
    });
  }, [boot, continueRender, portrait]);

  useEffect(() => {
    if (!map) return;
    const h = delayRender("Frame " + frame);
    // the scroll film shows the GTA routes only once they have been drawn (after the GTA beat);
    // the hold films draw them, slowly, from the beat's own frame
    const sc = portrait ? 1.75 : 1, gta = portrait ? gtaT : gtaW, can = portrait ? canT : canW;
    const gGap = kmAt(40 * sc, camera(BEAT_T.gta, portrait).zoom), cGap = kmAt(40 * sc, camera(1, portrait).zoom);
    const gtaData = hold === "gta" ? drawn(gta, gGap, frame)
      : !hold && t > BEAT_T.gta + 0.01 ? drawn(gta, gGap, 999) : none;
    const canData = hold === "canada" ? drawn(can, cGap, frame) : none;
    (map.getSource("gta") as GeoJSONSource).setData(gtaData);
    (map.getSource("can") as GeoJSONSource).setData(canData);
    const gtaOn = clamp((t - 0.22) / 0.14) * (1 - clamp((t - 0.6) / 0.12));
    map.setPaintProperty("dots", "circle-opacity", gtaOn);
    map.setPaintProperty("cdots", "circle-opacity", clamp((t - 0.8) / 0.1));
    map.setPaintProperty("gta", "line-opacity", 0.9 * (1 - clamp((t - 0.7) / 0.15) * 0.6));
    map.jumpTo(camera(t, portrait));
    map.once("idle", () => {
      const next: Record<string, { x: number; y: number }> = {};
      for (const [n, p] of [["Toronto", TORONTO] as [string, LngLat], ...GTA, ...CANADA]) {
        const q = map.project(p);
        next[n] = { x: q.x, y: q.y };
      }
      setPts(next);
      continueRender(h);
    });
    map.triggerRepaint();
  }, [continueRender, delayRender, frame, map, portrait, t]);

  const gtaLbl = clamp((t - 0.28) / 0.12) * (1 - clamp((t - 0.56) / 0.08));
  const canLbl = clamp((t - 0.84) / 0.1);
  const hq = pts["Toronto"];
  const s = portrait ? 1.75 : 1;
  const label = (n: string, o: number, big = false) => {
    const p = pts[n];
    if (!p || o <= 0) return null;
    // on a tall screen the far cities' names sit above their dots, clear of the edges and of Toronto
    const above = portrait && ABOVE_TALL.has(n), below = portrait && BELOW_TALL.has(n);
    const left = !above && !below && LEFT.has(n);
    const k = portrait && CAN_LABELS_TALL.has(n) && t > 0.6 ? 0.85 : 1;
    return (
      <div key={n} style={{ position: "absolute", left: p.x + (above || below ? 0 : (left ? -10 : 10) * s),
        top: above ? p.y - 10 * s : below ? p.y + 8 * s : p.y - 11 * s * k,
        translate: above ? "-50% -100%" : below ? "-50% 0" : left ? "-100% 0" : "0 0", opacity: o, fontFamily,
        fontWeight: 600, fontSize: (big ? 20 : 15) * s * k, letterSpacing: "0.06em", textTransform: "uppercase",
        color: BONE, textShadow: "0 1px 10px rgba(0,0,0,.9)", whiteSpace: "nowrap" }}>{n}</div>
    );
  };
  return (
    <AbsoluteFill style={{ backgroundColor: "#0A0C0E" }}>
      <div ref={ref} style={{ width, height, position: "absolute" }} />
      <AbsoluteFill style={{ pointerEvents: "none" }}>
        {GTA.filter(([n]) => (portrait ? GTA_LABELS_TALL : GTA_LABELS).has(n)).map(([n]) => label(n, gtaLbl))}
        {CANADA.filter(([n]) => (portrait ? CAN_LABELS_TALL : CAN_LABELS).has(n)).map(([n]) => label(n, canLbl))}
        {hq ? (
          <>
            <img src={staticFile("swarm/emblem-216.webp")} style={{ position: "absolute", left: hq.x, top: hq.y,
              width: 46 * s, translate: "-50% -54%" }} />
            <div style={{ position: "absolute", left: hq.x, top: hq.y - 40 * s, translate: "-50% -100%", fontFamily,
              fontWeight: 700, fontSize: 22 * s, letterSpacing: "0.12em", textTransform: "uppercase", color: GOLD,
              textShadow: "0 1px 12px rgba(0,0,0,.95)", opacity: 1 - clamp((t - 0.2) / 0.1) }}>Toronto</div>
          </>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
