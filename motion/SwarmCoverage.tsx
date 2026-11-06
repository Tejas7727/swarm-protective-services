// Swarm Protective Services: the coverage map film (scrubbed by scroll on coverage.html).
// Toronto -> the GTA (routes draw to 17 cities) -> Canada (arcs draw to the major cities).
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
// labels kept off the crowded core so the GTA beat reads at a glance
const GTA_LABELS = new Set(["Mississauga", "Brampton", "Vaughan", "Markham", "Oakville", "Hamilton", "Oshawa", "Newmarket", "Milton", "Pickering"]);
const GTA_LABELS_TALL = new Set(["Mississauga", "Brampton", "Markham", "Oakville", "Hamilton", "Oshawa", "Newmarket"]);
const CAN_LABELS_TALL = new Set(["Vancouver", "Halifax"]);
const CAN_LABELS = new Set(["Vancouver", "Calgary", "Edmonton", "Winnipeg", "Montréal", "Halifax"]);
// west of Toronto the name sits to the left of its dot, so it never runs into the routes
const LEFT = new Set(["Mississauga", "Brampton", "Milton", "Oakville", "Hamilton", "Vancouver", "Calgary", "Edmonton", "Winnipeg"]);
const CANADA: Array<[string, LngLat]> = [
  ["Vancouver", [-123.1207, 49.2827]], ["Calgary", [-114.0719, 51.0447]], ["Edmonton", [-113.4938, 53.5461]],
  ["Winnipeg", [-97.1384, 49.8951]], ["Ottawa", [-75.6972, 45.4215]], ["Montréal", [-73.5673, 45.5017]],
  ["Halifax", [-63.5752, 44.6488]],
];

const GOLD = "#C9A35E";
const BONE = "#E7E4D3";

const gtaRoutes = GTA.map(([, p]) => turf.lineString([TORONTO, p]));
const canRoutes = CANADA.map(([, p]) => {
  const g = turf.greatCircle(TORONTO, p, { npoints: 80 });
  return turf.lineString(g.geometry.type === "LineString" ? g.geometry.coordinates : (g.geometry.coordinates as number[][][])[0]);
});
const lens = (rs: ReturnType<typeof turf.lineString>[]) => rs.map((r) => turf.length(r));
const gtaLen = lens(gtaRoutes), canLen = lens(canRoutes);

const clamp = (x: number) => Math.min(1, Math.max(0, x));
const ease = Easing.bezier(0.65, 0, 0.35, 1);
const reveal = (rs: ReturnType<typeof turf.lineString>[], ls: number[], p0: number, p1: number, t: number) =>
  turf.featureCollection(
    rs.map((r, i) => {
      const n = rs.length, s = p0 + ((p1 - p0) * 0.45 * i) / n, e = s + (p1 - p0) * 0.55;
      const k = clamp((t - s) / (e - s));
      return turf.lineSliceAlong(r, 0, Math.max(0.0005, ls[i] * ease(k)));
    }),
  );

// the camera: Toronto close, the GTA, Canada; zoom is already logarithmic so it interpolates evenly
const camera = (t: number, portrait: boolean) => {
  const o = portrait ? -0.45 : 0, oc = portrait ? -0.72 : 0;
  const zoom = interpolate(t, [0, 0.08, 0.42, 0.56, 0.9, 1], [10.6 + o, 10.6 + o, 8.6 + o, 8.6 + o, 3.25 + oc, 3.25 + oc], {
    easing: ease, extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  const lng = interpolate(t, [0, 0.42, 0.56, 0.9], [TORONTO[0], -79.42, -79.42, portrait ? -99 : -92], {
    easing: ease, extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  const lat = interpolate(t, [0, 0.42, 0.56, 0.9], [TORONTO[1], 43.66, 43.66, portrait ? 50 : 50.5], {
    easing: ease, extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  return { center: [lng, lat] as LngLat, zoom };
};

export const SwarmCoverage: React.FC = () => {
  const ref = useRef<HTMLDivElement>(null);
  const frame = useCurrentFrame();
  const { width, height, durationInFrames } = useVideoConfig();
  const portrait = height > width;
  const { delayRender, continueRender } = useDelayRender();
  const [map, setMap] = useState<Map | null>(null);
  const [boot] = useState(() => delayRender("Loading the map"));
  const [pts, setPts] = useState<Record<string, { x: number; y: number }>>({});
  const t = frame / (durationInFrames - 1);

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
      m.addSource("gta", { type: "geojson", data: reveal(gtaRoutes, gtaLen, 0.16, 0.5, 0) });
      m.addLayer({ id: "gta", type: "line", source: "gta", layout: { "line-cap": "round" },
        paint: { "line-color": GOLD, "line-width": portrait ? 2.4 : 2, "line-opacity": 0.9 } });
      m.addSource("can", { type: "geojson", data: reveal(canRoutes, canLen, 0.62, 0.96, 0) });
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
    (map.getSource("gta") as GeoJSONSource).setData(reveal(gtaRoutes, gtaLen, 0.16, 0.5, t));
    (map.getSource("can") as GeoJSONSource).setData(reveal(canRoutes, canLen, 0.62, 0.96, t));
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
    const above = portrait && (n === "Vancouver" || n === "Halifax");
    const left = !above && LEFT.has(n);
    const k = portrait && CAN_LABELS_TALL.has(n) && t > 0.6 ? 0.85 : 1;
    return (
      <div key={n} style={{ position: "absolute", left: p.x + (above ? 0 : (left ? -10 : 10) * s),
        top: above ? p.y - 10 * s : p.y - 11 * s * k,
        translate: above ? "-50% -100%" : left ? "-100% 0" : "0 0", opacity: o, fontFamily,
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
            <div style={{ position: "absolute", left: hq.x, top: hq.y, width: 120 * s, height: 120 * s,
              translate: "-50% -50%", borderRadius: "50%", border: `1.5px solid ${GOLD}`,
              opacity: 0.55 - 0.35 * Math.abs(Math.sin(frame / 9)),
              scale: String(0.7 + 0.3 * Math.abs(Math.sin(frame / 9))) }} />
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
