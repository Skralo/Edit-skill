# Elements: Anže's overlay cut-outs

All are Anže's own images (transparent WebP, 1125×2000, sent 28. 9. 2026), in
`template/public/film/elements/src/`. `prep.py --elements` trims each one to its alpha, scales
it to `side` px, applies its treatment (keeps it mostly white), and writes `NAME.png` plus
`NAME-bit.png` (white 1-bit dots for the first and last flash frame) and `sizes.json`.

**Mapping rule:** the result must *mean* the shot. One element per shot, one word label in
brackets. Minimal and abstract ("minimalistični, kot abstract"). If a shot has no fitting element,
it gets the scan only (v3: Build/typing). Ask Anže before inventing a new mapping.

| Name | What it shows | Meaning / label | Treatment | On-screen h | Used in v3 |
| --- | --- | --- | --- | --- | --- |
| `brain` | engraved white brain, side view | mind, thinking: `[MIND]` | as drawn | 270 | Present (talking to camera) |
| `eagle` | eagle with spread wings, grey-white | strength, rise: `[STRENGTH]` | `lift` (lighter, "bolj bel") | 310 | Train (pull-up bar) |
| `tiger` | leaping tiger, black and white engraving | speed, power: `[SPEED]` | as drawn (**colour stays**, his rule) | 300 | Run (placed ahead of the runner, `side: 1`) |
| `figures` | three standing human silhouettes | team: `[TEAM]` | `white` (solid white, high contrast) | 420 | Team |
| `sword` | long straight sword, vertical | sharpen, focus, cut: `[SHARPEN]` | as drawn | 470 | Recover (sauna), 2 frames after the orbital lock |
| `helmet` | Spartan/gladiator helmet with crest | discipline, fight: `[DISCIPLINE]` | as drawn | 330 | Repeat (gym, lifting) |
| `orbit` | orbital HUD: concentric eye rings, orbit lines, small discs | insight, analysis: `[INSIGHT]` | `lines` (dark line art → white lines) | used as the scan | Recover: **is the scan** (eye on the head) |
| `words` | word ring: INTRODUCE · REFINE · IMPROVE · EVOLVE · ENVISION · PLAN · CRAFT (outer) + small inner ring | the method, the loop | as drawn | 720 ring | Build/notebook: turns **behind** him (matte) |
| `logo` | the SKRALOVNIK logo (sparkle symbol + wordmark), from `logo.svg` | plan, the brand itself: `[PLAN]` | as drawn, white | 250 | Build/notebook, big and white |
| `cheetah` | walking cheetah on a light patch | speed | as drawn | 280 | v2 Run (replaced by the tiger in v3) |
| `eye` | eye radiating lines above a tiny standing figure | insight, vision | as drawn | 300 | v2 Recover (replaced by orbit + sword) |
| `network` | overlapping circles (flower of life) with small figures at the nodes | network, community, connections | as drawn | 320 | not used yet |

Treatments (film.json `elements.NAME.treat`):
- *(none)*: the art as drawn. Use for art that is already light, or where colour must stay.
- `lift`: `rgb = 255 − (255 − rgb) × 0.45`, lighter overall with detail kept.
- `white`: solid white keeping alpha. Use for silhouettes.
- `lines`: dark line art becomes white lines, light fills are dropped (`alpha × clip((235 − lum)/150)`).

Adding a new element: put `NAME.webp` (or `.png`, transparent) in `elements/src/`, add
`"NAME": {"side": 700, "h": 300}` to film.json `elements` (plus a treatment if it is dark), run
`python3 scripts/prep.py --elements`, then look at it over the brightest shot before using it.
For another brand: its own elements, and `logo` pointing at its logo SVG.
