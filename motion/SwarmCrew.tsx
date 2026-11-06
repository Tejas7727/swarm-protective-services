// Swarm Protective Services: the crew as a graphic (Meet us, beside the statement).
// Gold line art rises first, then the halftone arrives figure by figure, then one gold glint.
// Layers come from the real crew photograph (scratchpad crew_graphic.py -> shared/assets/swarm).
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const ease = Easing.bezier(0.16, 1, 0.3, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
// the three figures stand roughly in these thirds of the frame
const BANDS: Array<[number, number, number]> = [
  [0, 36, 18], [36, 66, 34], [66, 100, 26],
];

export const SwarmCrew: React.FC = () => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const rise = interpolate(f, [0, 34], [100, 0], { ...clamp, easing: ease });
  const scan = interpolate(f, [0, 34], [height, 0], { ...clamp, easing: ease });
  const zoom = interpolate(f, [0, 119], [1.06, 1], { ...clamp, easing: Easing.out(Easing.quad) });
  const glint = interpolate(f, [78, 112], [-0.4, 1.4], clamp);
  const lineFade = interpolate(f, [60, 100], [1, 0.55], clamp);
  return (
    <AbsoluteFill style={{ backgroundColor: "#0A0C0E", overflow: "hidden" }}>
      <AbsoluteFill style={{ scale: String(zoom) }}>
        {BANDS.map(([a, b, start]) => {
          const k = interpolate(f, [start, start + 34], [0, 1], { ...clamp, easing: ease });
          return (
            <AbsoluteFill key={a} style={{ clipPath: `inset(0 ${100 - b}% 0 ${a}%)`, opacity: k,
              translate: `0 ${(1 - k) * 60}px` }}>
              <Img src={staticFile("swarm/crew-halftone.png")} style={{ width, height }} />
            </AbsoluteFill>
          );
        })}
        <AbsoluteFill style={{ clipPath: `inset(${rise}% 0 0 0)`, opacity: lineFade }}>
          <Img src={staticFile("swarm/crew-lines.png")} style={{ width, height }} />
        </AbsoluteFill>
      </AbsoluteFill>
      {f < 36 ? (
        <div style={{ position: "absolute", left: 0, right: 0, top: scan, height: 2,
          background: "linear-gradient(90deg, transparent, #D6B274, transparent)", opacity: 0.9 }} />
      ) : null}
      <AbsoluteFill style={{ mixBlendMode: "screen", pointerEvents: "none",
        background: `linear-gradient(115deg, transparent ${glint * 100 - 12}%, rgba(214,178,116,.28) ${glint * 100}%, transparent ${glint * 100 + 12}%)` }} />
      <AbsoluteFill style={{ background: "radial-gradient(120% 90% at 50% 45%, transparent 55%, rgba(10,12,14,.85) 100%)" }} />
    </AbsoluteFill>
  );
};
