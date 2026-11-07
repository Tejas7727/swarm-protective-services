// Swarm Protective Services: the poster hero, as a motion study (experimental type direction).
// Layers, back to front: the night photograph, the poster line, the officer cut out of the
// photograph (so his head sits in front of the words), then the light subheading and the body.
// Type: Saira at its narrowest and heaviest (the wordmark's family) for the poster line,
// Archivo at its widest and lightest for the subheading. Sizes step by the golden ratio.
import { useLayoutEffect, useRef, useState } from "react";
import {
  AbsoluteFill, Easing, Img, continueRender, delayRender, interpolate, staticFile, useCurrentFrame,
} from "remotion";

const PHI = 1.618;
const ease = Easing.bezier(0.16, 1, 0.3, 1);
const c = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const BONE = "#EDE3CB";

type Layout = "wide" | "tall";
const L = {
  // plate, cut-out, object-position x/y, head share of plate height, plate w/h, words per line
  wide: { bg: "crew-2000.webp", fg: "crew-fg.png", ox: 0.6, oy: 0.45, head: 0.2295, pw: 2000, ph: 1111,
          lines: [["We", "plan", "for", "it."]], gut: 96, body: 30 },
  tall: { bg: "crew-m-1440.webp", fg: "crew-m-fg.png", ox: 0.55, oy: 1, head: 0.519, pw: 1440, ph: 1920,
          lines: [["We", "plan"], ["for", "it."]], gut: 64, body: 34 },
};

const fontCss = `
@font-face{font-family:PosterSaira;src:url(${staticFile("swarm/poster/Saira.ttf")}) format("truetype");font-weight:100 900;font-stretch:50% 125%}
@font-face{font-family:PosterArchivo;src:url(${staticFile("swarm/poster/Archivo.ttf")}) format("truetype");font-weight:100 900;font-stretch:62% 125%}`;

export const SwarmPosterHero: React.FC<{ layout: Layout }> = ({ layout }) => {
  const f = useCurrentFrame();
  const g = L[layout];
  const W = layout === "wide" ? 1920 : 1080, H = layout === "wide" ? 1080 : 1920;
  const lineRef = useRef<HTMLDivElement>(null);
  const [fs, setFs] = useState(200);
  const [handle] = useState(() => delayRender("fonts and fit"));

  // fit the widest line to the width between the gutters, once the fonts are in
  useLayoutEffect(() => {
    Promise.all([document.fonts.load("200px PosterSaira"), document.fonts.load("40px PosterArchivo")]).then(() => {
      const el = lineRef.current;
      if (el) { el.style.fontSize = "200px"; setFs((200 * (W - 2 * g.gut)) / el.scrollWidth); }
      continueRender(handle);
    });
  }, [W, g.gut, handle]);

  // where his head lands in this crop (cover fit), so it overlaps the lower part of the line
  const sc = Math.max(W / g.pw, H / g.ph), dh = g.ph * sc, dw = g.pw * sc;
  const headY = (H - dh) * g.oy + g.head * dh;
  const lineH = fs * 0.84, bh = lineH * g.lines.length;
  const top = Math.max(150, headY - bh * 0.6);
  const sub = g.body * PHI * PHI * (layout === "wide" ? 1 : 0.62);

  const camera = interpolate(f, [0, 149], [1.07, 1], { ...c, easing: Easing.out(Easing.quad) });
  const near = interpolate(f, [0, 149], [1.1, 1], { ...c, easing: Easing.out(Easing.quad) });   // the officer moves a touch more: depth
  const light = interpolate(f, [0, 24], [0, 1], c);
  const subIn = interpolate(f, [12, 44], [0, 1], { ...c, easing: ease });
  const bodyIn = interpolate(f, [84, 112], [0, 1], { ...c, easing: ease });
  let k = 0;

  const plate = (src: string, scale: number) => (
    <AbsoluteFill style={{ scale: String(scale), transformOrigin: `${g.ox * 100}% ${(g.head + 0.1) * 100}%` }}>
      <Img src={staticFile(`swarm/poster/${src}`)} style={{ position: "absolute", width: dw, height: dh,
        left: (W - dw) * g.ox, top: (H - dh) * g.oy }} />
    </AbsoluteFill>
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#07090B", overflow: "hidden" }}>
      <style>{fontCss}</style>
      <AbsoluteFill style={{ opacity: light }}>{plate(g.bg, camera)}</AbsoluteFill>
      {/* the poster line: every word rises out of its own mask, in turn */}
      <div ref={lineRef} style={{ position: "absolute", left: g.gut, top, fontFamily: "PosterSaira", fontSize: fs,
        fontVariationSettings: "'wdth' 55, 'wght' 850", lineHeight: 0.84, color: BONE, textTransform: "uppercase",
        whiteSpace: "nowrap", letterSpacing: "-0.004em" }}>
        {g.lines.map((words, li) => (
          <div key={li} style={{ display: "flex", gap: "0.22em", overflow: "hidden", paddingTop: "0.06em" }}>
            {words.map((w) => {
              const s = 30 + 7 * k++;
              const up = interpolate(f, [s, s + 34], [1.05, 0], { ...c, easing: ease });
              return <span key={w} style={{ display: "inline-block", transform: `translateY(${up * 100}%)` }}>{w}</span>;
            })}
          </div>
        ))}
      </div>
      <AbsoluteFill style={{ opacity: light }}>{plate(g.fg, near)}</AbsoluteFill>
      <AbsoluteFill style={{ background: "linear-gradient(0deg, rgba(7,9,11,.9), rgba(7,9,11,0) 42%)" }} />
      <div style={{ position: "absolute", left: g.gut, top: top - sub * 1.35, fontFamily: "PosterArchivo", fontSize: sub,
        fontVariationSettings: "'wdth' 125, 'wght' 300", letterSpacing: "-0.015em", color: "#E7E4D3",
        opacity: subIn, transform: `translateY(${(1 - subIn) * 18}px)`, filter: `blur(${(1 - subIn) * 6}px)` }}>
        Life is unpredictable.
      </div>
      <div style={{ position: "absolute", left: g.gut, bottom: layout === "wide" ? 84 : 150, width: layout === "wide" ? 760 : W - 2 * g.gut,
        fontFamily: "PosterArchivo", fontSize: g.body, lineHeight: 1.55, color: "#CFCCC0", opacity: bodyIn,
        transform: `translateY(${(1 - bodyIn) * 14}px)` }}>
        Discreet, trained security for venues, events and private clients across Toronto and the GTA.
      </div>
    </AbsoluteFill>
  );
};
