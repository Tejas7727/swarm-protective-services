# Motion sources

The two films on the site are rendered in the local Remotion studio
(`Documents/CludeProject/ai-studio/remotion`, compositions in the "Swarm" folder).
These are copies of their sources, kept with the site they belong to.

- `SwarmCoverage.tsx`: the coverage map film (MapLibre on OpenFreeMap tiles, Turf routes).
  Rendered as `SwarmCoverageWide` (1440x810) and `SwarmCoverageTall` (720x1280), 72 frames each,
  `--sequence --image-format=jpeg --gl=angle --concurrency=1`, then saved as WebP q62 to
  `docs/assets/cine/cov-w/` and `docs/assets/cine/cov-t/` (`fNN.webp`). Attribution is on the page.
- `SwarmCrew.tsx`: the crew drawn as a graphic, beside the Meet us statement. Layers come from
  `crew_graphic.py` (input `docs/assets/img/lot-tall-1000.webp`, output to the studio's
  `shared/assets/swarm/`). Rendered 720x960, 120 frames, then re-encoded 540x720 H.264 CRF 32 to
  `docs/assets/cine/crew.mp4`; the last frame is `crew-poster.webp`.
