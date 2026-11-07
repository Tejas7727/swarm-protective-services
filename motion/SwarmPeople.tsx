// Swarm Protective Services: the crew, animated (Meet us statement, the quote form).
// Each figure arrives in turn: a gold outline rises, gold halftone fills it, the
// photograph resolves through the dots, then one gold light passes across them.
// Transparent background: the site plays it straight onto the page.
// Layers: swarm/motion/people_layers.py -> shared/assets/swarm/people.
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import lineup from "../../../shared/assets/swarm/people/lineup.json";
import pair from "../../../shared/assets/swarm/people/pair.json";

type Band = { x0: number; x1: number; cx: number };
const GROUPS: Record<string, { w: number; h: number; bands: Band[] }> = { lineup, pair };
const ease = Easing.bezier(0.16, 1, 0.3, 1);
const c = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const GOLD = "#D6B274";

export const SwarmPeople: React.FC<{ group: string }> = ({ group }) => {
  const f = useCurrentFrame();
  const g = GROUPS[group];
  const src = (k: string) => staticFile(`swarm/people/${group}-${k}.png`);
  const full = { width: "100%", height: "100%" };
  const zoom = interpolate(f, [0, 149], [1.035, 1], { ...c, easing: Easing.out(Easing.quad) });
  const sweep = interpolate(f, [100, 142], [-0.3, 1.3], c);
  const dotsOut = interpolate(f, [92, 125], [1, 0.28], c);
  const rimOut = interpolate(f, [100, 135], [1, 0.45], c);
  return (
    <AbsoluteFill style={{ scale: String(zoom) }}>
      {g.bands.map((b, i) => {
        const s = i * 9;
        const rim = interpolate(f, [s, s + 30], [0, 1], { ...c, easing: ease });
        const dots = interpolate(f, [s + 14, s + 50], [0, 1], { ...c, easing: ease });
        const photo = interpolate(f, [s + 46, s + 86], [0, 1], { ...c, easing: ease });
        const side = `${(1 - b.x1) * 100}% 0 ${b.x0 * 100}%`;
        return (
          <AbsoluteFill key={i}>
            <AbsoluteFill style={{ opacity: photo }}>
              <Img src={src("photo")} style={{ ...full, clipPath: `inset(0 ${side})` }} />
            </AbsoluteFill>
            <AbsoluteFill style={{ opacity: dots * dotsOut, translate: `0 ${(1 - dots) * 26}px` }}>
              <Img src={src("dots")} style={{ ...full, clipPath: `inset(0 ${side})` }} />
            </AbsoluteFill>
            <AbsoluteFill style={{ opacity: rimOut }}>
              <Img src={src("rim")} style={{ ...full, clipPath: `inset(${(1 - rim) * 100}% ${side})` }} />
            </AbsoluteFill>
          </AbsoluteFill>
        );
      })}
      {/* one gold light across the figures, only where they stand */}
      <AbsoluteFill style={{
        WebkitMaskImage: `url(${src("photo")})`, maskImage: `url(${src("photo")})`,
        WebkitMaskSize: "100% 100%", maskSize: "100% 100%", mixBlendMode: "screen",
        background: `linear-gradient(105deg, transparent ${sweep * 100 - 14}%, rgba(214,178,116,.34) ${sweep * 100}%, transparent ${sweep * 100 + 14}%)`,
      }} />
      {f < 44 ? (
        <div style={{ position: "absolute", left: 0, right: 0, height: 2,
          top: `${interpolate(f, [0, 40], [92, 6], { ...c, easing: ease })}%`,
          background: `linear-gradient(90deg, transparent, ${GOLD} 30%, ${GOLD} 70%, transparent)`,
          opacity: interpolate(f, [30, 44], [0.8, 0], c) }} />
      ) : null}
    </AbsoluteFill>
  );
};
