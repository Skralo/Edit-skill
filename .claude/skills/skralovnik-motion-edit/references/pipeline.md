# Pipeline: how the template works

## Contents
1. Architecture
2. File map
3. film.json schema
4. events.ts: the event API and every look
5. Commands
6. Environment (Claude Code cloud and local)
7. Gotchas
8. Changing the engine (new looks, 9:16, 4K)

---

## 1. Architecture

```
source.mp4 ──prep.py──► plates (org colour jpg, d4/d8 1-bit png), track.json (lock boxes, contours),
                        elements/*.png (+ -bit), matte/ + plate/cut/ (subject cut-outs)
film/film.json ─┐
film/events.ts ─┼─► src/film (Remotion: React → frames) ──► PNG frames ─┐
                │                                                          ├─ post.py ─► master + web mp4
                └─► export-cues.ts → out/film/cues.json ─► sfx.py ─► soundtrack.wav ┘   + sync/TP/flash checks
film/sfx-plan.json ──────────────────────────────────────────┘
```

One timeline drives both picture and sound: `events.ts` is read frame by frame by the picture and
exported as cues for the sound, so every sound sits on its event's frame.

## 2. File map (template/)

| Path | What |
| --- | --- |
| `film/film.json` | per film: source, cuts, chapters, brand, tracking, grade, mattes, elements |
| `film/events.ts` | per film: **the edit** (every event, frame-exact) |
| `film/sfx-plan.json` | per film: which events sound, variant and tier |
| `src/film/config.ts` | timing from film.json, event types, helpers (`s`, `scan`, `element`, `boot`, `outro`) |
| `src/film/timeline.ts` | re-exports config + EVENTS; `eventsAt`, `baseAt`, `lookAt` |
| `src/film/Film.tsx` | composition: Plate → overlays in fixed order → Outro → Hud |
| `src/film/Plate.tsx` | full-frame layer: footage, `neg`, `dit`, `type`; `Strips` |
| `src/film/Scan.tsx` | `Scan`, `OrbitScan`, `Ring`, `Element` |
| `src/film/Textures.tsx` | `Strip`, `Contour`, `Boot` |
| `src/film/Chrome.tsx` | Three.js chrome sparkle (`ChromeStage`), `Wipe` transition |
| `src/film/Outro.tsx` | recap sheet, fold, converge, lock, wordmark, flat logo |
| `src/film/Hud.tsx` | crosses, wordmark, chapter caption, progress |
| `src/film/Sparkle.tsx`, `Bits.tsx`, `Label.tsx`, `Fonts.tsx`, `tokens.ts`, `track.ts` | shared pieces |
| `scripts/prep.py` | cuts, plates, tracking, elements, mattes, cut-outs |
| `scripts/export-cues.ts` | events → `out/film/cues.json` |
| `scripts/sfx.py` | palette, audition reel, cue sheet, QC, soundtrack |
| `scripts/post.py` | grain, H.264/AAC mux, sync / true-peak / flash checks |
| `scripts/sheet.py` | contact sheet (auto-picks the edit's moments) |
| `scripts/clean.ts` | clean share per shot |
| `scripts/render.sh` | everything, end to end |
| `public/film/` | `source.mp4` (add), brand SVGs, `elements/src/`, generated plates/elements/track/matte |

The brand SVGs: `logo.svg` (266×116 units, symbol + wordmark), `logo-symbol.svg` (the same box,
symbol only, for the flat outro), `wordmark.svg` (same box, wordmark only), `symbol.svg` (the
sparkle). The chrome sparkle's 3D outline in `Chrome.tsx` (`SEG`) and `Sparkle.tsx` is the
SKRALOVNIK four-point sparkle; for another brand's symbol, replace those Bézier segments and the
outro's `SYM` / `FORM` offsets (they place the symbol inside logo.svg).

## 3. film.json schema

```jsonc
{
  "name": "SKRALOVNIK personal film v3",
  "source": "public/film/source.mp4",
  "fps": 30, "width": 1920, "height": 1080,
  "pre": 6,                     // boot frames before the footage
  "outroHold": 11,              // frames held on the final logo
  "recapLabel": "[REPEAT]",     // header of the outro contact sheet
  "cuts": [0, 30, …, 242],      // shot k = cuts[k]..cuts[k+1]; last = frame count (prep.py --detect-cuts)
  "chapters": ["Present", …],   // one word per shot (HUD caption, chapter flash, recap labels)
  "brand": { "wordmark": "SKRALOVNIK", "ink": "#050607", "paper": "#f4f1ea", "accent": "#00202d" },
  "logo": { "width": 1040, "cx": 960, "cy": 540 },   // outro logo placement
  "shots": [                    // one per shot
    { "track": { "target": "face", "pad": 1.9, "minW": 190, "aspect": 1.25, "lift": 0.08 },
      "grade": { "lo": 0.5, "hi": 99.7, "gamma": 0.92, "k": 6.0 },   // 1-bit plates only
      "contours": 1 },          // how many silhouettes to keep (2 for a two-person shot)
    { "track": { "target": "flow", "seedFrame": 44, "seed": [1105, 575], "box": [230, 170] } }
  ],
  "matteShots": [3],            // shots that get a person matte (an element passes behind)
  "elements": { "tiger": { "side": 700, "h": 300, "treat": "lift|white|lines" },
                "logo": { "side": 1200, "h": 250, "svg": "public/film/logo.svg" } },
  "sfxRound": 2                 // sfx.py writes sfx/round2/
}
```

Track targets: `face`, `head_shoulders` (+ `which: "all"` for groups), `body` (+ `vis`), `flow`.
`pad` scales the landmark extent, `minW` is the minimum box width (px), `aspect` forces h/w,
`lift` moves the box up by a fraction of its height. Boxes are smoothed per shot (centre σ 1.3,
size σ 2.2 frames) and kept 40 px inside the frame.

## 4. events.ts: the event API

```ts
type Ev = { id, o /*first frame*/, dur, hit? /*sound frame*/, fn, look, shot, note, p? };
s(k)                                   // first output frame of shot k (boot offset included)
scan(id, k, at, dur, note, label)      // → `${id}-scan`, locks (hit) on its last frame
element(id, k, at, el, label, note, side?)  // → `${id}-el`, 4 frames
boot(), outro()                        // the standard boot and outro events
```

| look | kind | frames | params (`p`) |
| --- | --- | --- | --- |
| `strips` | overlay | 2 | – |
| `neg` | base (full frame) | 1 | `src` (source frame, optional) |
| `dit` | base | 1 | `src` |
| `type` | base | 1 | `size`, `x`, `word` (defaults: chapter, auto size, centre) |
| `wipe` | overlay (chrome) | 4 | set `o = s(k) − 2`, `hit = s(k)` |
| `scan` | overlay | 5–6 | `label` (via `scan()`) |
| `orbit` | overlay | 6 | `label`, `fx`, `fy` (eye focus as box fractions) |
| `element` | overlay | 4 | `el`, `label`, `side` (via `element()`) |
| `ring` | overlay + cut-out | 8 | – (shot must be in `matteShots`) |
| `strip` | overlay | 4 | – |
| `contour` | overlay | 4 | – |
| `boot`, `recap`, `collapse`, `converge`, `lockup`, `wordmark`, `flat` | boot/outro | – | from `boot()` / `outro()` |

Base looks replace the footage for their frames; overlays draw over it in the order
`boot, strips, strip, ring, contour, scan, orbit, element, wipe`, then the outro, then the HUD.
`fn` must be set for the sound: transition on cut entries, lock on scans, micro on flashes and
results, texture on travelling things, resolve on the logo lock.

## 5. Commands

```bash
python3 scripts/prep.py --detect-cuts          # cuts → film.json
python3 scripts/prep.py                        # frames, elements, plates, tracking
python3 scripts/prep.py --skip-track           # same without MediaPipe (track.json exists)
python3 scripts/prep.py --elements | --matte | --cutouts
npx tsc --noEmit -p .                          # after prep (needs track.json, sizes.json)
npx tsx scripts/export-cues.ts && python3 scripts/sfx.py
npx remotion render src/index.ts Film out/check --sequence --frames=A-B --scale=0.5 --image-format=jpeg --gl=angle --log=error
python3 scripts/sheet.py out/check out/check.jpg [--frames 1,2,3]
npx tsx scripts/clean.ts
scripts/render.sh film-v1                      # everything → video/film-v1{,-web}.mp4, -sheet.jpg
npx remotion studio                            # interactive preview (local only)
```

## 6. Environment

Needs Node 18+, Python 3.10+, ffmpeg with libx264 and the usual filters, headless Chromium.

**Claude Code cloud container** (what v1–v3 were made in):
- Chromium is preinstalled; `remotion.config.ts` points Remotion at it automatically.
- Remotion's bundled ffmpeg lacks filters post.py needs: `pip install imageio-ffmpeg` and
  `ln -sf $(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())") /usr/local/bin/ffmpeg`.
- MediaPipe needs `apt-get install -y libegl1 libgles2 libgl1`. A `TypeError` printed at
  MediaPipe shutdown is harmless.
- The chrome needs WebGL: always render with `--gl=angle`.
- Model downloads (storage.googleapis.com) and npm/pip must be allowed by the network policy.
- Disk is limited: plates for 250 frames are ~150 MB, full-res PNG frames ~1 GB; delete
  `out/film/frames` after encoding if space is short.

**Local (Mac/Windows):** `brew install ffmpeg` (or equivalent), `npm install`, `pip install -r
requirements.txt`; Remotion downloads its own Chromium.

## 7. Gotchas

- `tsc` fails with "Cannot find module …/sizes.json / track.json" until prep has run. Expected.
- Frame files are named `element-NNN.png` by Remotion (zero-padded to the frame count's width).
- Remotion renders with concurrency 4; a full 1080p render of ~300 frames takes ~10 min, most of it
  on the chrome frames.
- The flash scan counts full-frame luminance swings; two base looks within ~10 frames of each other
  can push it up. Keep full-frame flashes single and apart.
- A 1-bit frame (`dit`) of a very bright shot is mostly white: it reads as a flash. Grade that
  shot's plates darker (`hi` 97, gamma > 1) or use `neg`.
- `post.py` needs `out/film/soundtrack.wav`: run `sfx.py` first (render.sh does).
- The ring cut-out uses the committed matte; if plates are regenerated, rerun `--cutouts`.
- Never re-encode the approved master to change anything: change the film files and re-render.

## 8. Changing the engine

- **A new look:** add it to `OverLook`/`BaseLook` in `config.ts`, a component (overlay: in
  `Film.tsx`'s `ORDER` + switch; base: in `Plate.tsx`), then use it in events.ts. Keep it white,
  glowed, short.
- **9:16 (Reels):** `width`/`height` in film.json drive most sizes, but the layout was designed for
  16:9: the strip panel (right 360 px), the outro grid and logo size, the HUD positions and the
  element placement need a pass, and the footage needs a vertical crop (prep.py `original()` would
  crop per shot around the tracked subject). Plan it as its own round and ask first.
- **4K master:** render with `--scale=2` and pass 3840×2160 to post.py (change W/H there).
