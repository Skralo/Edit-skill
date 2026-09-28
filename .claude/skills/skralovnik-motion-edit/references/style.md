# Style: the visual grammar of the SKRALOVNIK edit

Everything here is what v3 does, with the numbers the template uses. Frame counts are at 30 fps,
sizes at 1920×1080. `o` is the output frame; `s(k)` is the first frame of shot k.

## Contents
1. Idea and references
2. Palette, type, legibility
3. The per-shot burst (scan → result → extra beat)
4. Transitions on the cut
5. Extra beats
6. Special pieces: orbital scan, word ring
7. HUD furniture
8. Boot and outro
9. Finishing: grain, flashes, clean share
10. What failed (do not bring back)

---

## 1. Idea and references

"The day in its own colour, analysed in bursts." A person's day in 8 shots (Present · Build ·
Train · Build · Run · Team · Recover · Repeat) is read by a machine: it boots, scans each moment,
finds the subject, returns a symbolic result, and at the end folds the day into the brand mark.

Aesthetic sources Anže gave: Y2K chrome, tech glitch, fine technical graphics; an X post by
AmirMushich (frames change extremely fast, a new look every frame or two: "bliskovito") and an IG
reel (small uppercase pixel captions, minimal labels, no noise). From them the edit takes the
*speed* and the *labels*, but applies them in short bursts over untouched footage.

## 2. Palette, type, legibility

| Token | Value | Use |
| --- | --- | --- |
| INK | `#050607` | canvas (boot, outro), glow/shadow colour |
| PAPER | `#f4f1ea` | **everything the edit draws** |
| HAIR | PAPER at 0.82 | hairlines, pixel labels |
| HAIR_FAINT | PAPER at 0.28 | secondary rules |
| accent | `#00202d` (SKRALOVNIK teal) | only as the floor glow in the chrome studio |

- **Legibility on bright shots:** every white overlay gets a dark glow:
  lines `drop-shadow(0 0 3px rgba(5,6,7,0.65))`, elements `drop-shadow(0 0 6px rgba(5,6,7,0.45))`,
  text `text-shadow: 0 1px 5px rgba(5,6,7,0.75)`. This is what made white work on the white gym
  and the living room (v3); v2's "ink on bright shots" was rejected.
- **Pixel labels:** Silkscreen 16 px, line height 20, letter spacing 1, uppercase, in brackets:
  `[MIND]`, `SCAN 01`, `RESULT 03`, `LOCKED [FOCUS]`, `[CONTOUR] 214 PTS`.
- **Serif:** Cormorant Garamond 500/600 for the chapter caption and the giant chapter word
  (the website's type).

## 3. The per-shot burst

Timeline of one shot (v3 shot 1, Present, 30 frames):

```
s+0..1  in-transition (strips)
s+3..8  scan (6 f), locks on s+8  ← sound: lock
s+9..12 result element (4 f)      ← sound: soft grain
s+23    chapter word (1 f)        ← sound: shutter
rest    clean footage
```

### Scan (`look: 'scan'`, 6 frames, 5 in a short last shot)
- Centre and size from the tracked lock box `[cx, cy, w, h]` (pose landmarks per film.json).
  Radius `R = clamp(0.5·hypot(w, h) + 16, 70, 400)`.
- Circle draws on over 2 frames (stroke 1.4), locks at stroke 3 on the last frame.
- Three arcs at `R + 11`, 38° long, rotating (+26°, −19°, +33° per frame), 60° and stroke 3 when locked.
- Ticks every 15° from `R − 9` to `R − 3` (from frame 1); a sweep line from the centre (not on
  the lock frame); a 16 px centre cross.
- Label at −38° outside the circle: `SCAN 0k` + `NN%`, then `LOCKED [LABEL]` on the lock frame.
- The sound hits on the lock frame (`hit`).
- Start 3–4 frames after the cut, after the in-transition.

### Result element (`look: 'element'`, 4 frames, right after the lock)
- Frames 0 and 3: the 1-bit version (white dots, `imageRendering: pixelated`); frames 1–2 clean.
- Placed beside the scan, on the open side of the frame (subject left of centre → element right),
  `R + 40` px from the circle, clamped 60 px from the sides and 90/110 from top/bottom. `side` forces it.
- Height per element (film.json `elements.NAME.h`): 250–470 px (brain 270, eagle 310, tiger 300,
  figures 420, sword 470, helmet 330, logo 250).
- A leader line from the circle to the element, 14 px corner brackets 8 px around it, the scan
  circle kept at 45 % opacity, and from frame 1 the label `[LABEL]` / `RESULT 0k` under it.
- The result must **mean** something about the shot (see elements.md); the label is its word.

## 4. Transitions on the cut

| Look | Frames | What it is |
| --- | --- | --- |
| `strips` | 2 | 7 thin horizontal strips (8–54 px) of the frame knocked sideways ±40 or ±180 px, 45 % of them RGB-split (8–20 px), 30 % from 3 frames earlier. The footage stays underneath. |
| `neg` | 1 | the frame inverted |
| `dit` | 1 | Floyd–Steinberg 1-bit of the frame at ¼ resolution, scaled ×4 pixelated, paper on ink |
| `wipe` | 4 | a 3D chrome sparkle leaves the outgoing subject (380 px), swells (2300 px), fills the lens (8400 px, glow off), lands small (250 px) on the incoming subject; starts 2 frames before the cut, `hit` = the cut |

v3 order: strips, neg, wipe, dit, strips, neg, dit, wipe. Never the same look twice in a row. The
wipes sit on the two biggest cuts (into Train and into Repeat). The first shot's entry is the
strongest cut of the film (strong sound).

Short films and teasers (≤ 4 shots): one or two wipes at most (ask), never on the first entry (the
wipe flies from the outgoing subject, and before shot 1 there is only the boot: open on strips).
A wipe starts 2 frames before its cut, so those frames count against the *outgoing* shot's clean
share; with a 1-frame chapter word in the same shot the clean share can drop below 55 %: move the
word to another shot.

## 5. Extra beats (at most one per shot, sometimes none)

| Look | Frames | What it is |
| --- | --- | --- |
| `type` | 1 | the chapter word in Cormorant 600, far too big for the frame (760–1060 px), over the moving footage at brightness 0.55. Set `p.size` and `p.x` by eye so the word overflows both edges. v3 uses it twice (PRESENT, RUN). |
| `strip` | 4 | a film strip of the shot's last frames (1-bit tiles) rolls up a 360 px black panel on the right, with `F 0042` labels |
| `contour` | 4 | the subject's silhouette (segmentation) traces itself in a 2 px hairline with small square markers; label `[CONTOUR] N PTS` |
| `neg` (micro) | 1 | a negative inside the shot (v3: the heat of the sauna) |
| `ring` | 8 | the word ring (see 6) |

## 6. Special pieces

### Orbital scan (`look: 'orbit'`, v3 Recover)
Anže's orbital-HUD element used *as the scan itself*. Its concentric "eye" is placed on a focus
point (`p.fx`, `p.fy` as fractions of the lock box from its centre; v3: 0.4, −0.5 = the head).
It rotates −48° + 8°/frame and scales 0.82 → 1 over 6 frames; frame 0 is 1-bit; label at 18°
(to the right, clear of the element's own discs). Size `clamp(2.3·R, 460, 820)`. The next result
(the sword) comes two frames after the lock: "ne hkrati, z rahlim zamikom".

### Word ring (`look: 'ring'`, v3 Build/notebook)
The circular word element turns around the subject **behind** them: ring first (720 px, centred on
the lock box, 0.3·h lower, 3.5°/frame, 1-bit on its first and last frames), then the subject's
cut-out (person matte, `matteShots` in film.json) drawn over it. The matte threshold is tight
(0.55–0.80) so no background spills into a halo.

## 7. HUD furniture (always on, deliberately little)

- Four registration crosses, 18 px, 48 px in from each corner.
- Top left (72, 40): the wordmark in pixel type; it types on during the boot (30 %, 60 %, 80 %, 100 %).
- Bottom left: `0k / 0N` (pixel, 60 % paper) above a 30 px rule + the chapter word in Cormorant 500,
  25 px, letter spacing 0.32em, typed two letters per frame after each cut with a block cursor.
- Bottom edge: 2 px progress hairline (14 % track, 60 % fill).
- A light scrim only at the top 10 % and bottom 16 % so the type reads.

## 8. Boot and outro

**Boot (6 frames before the footage):** hairlines draw from two corners, a flat sparkle glints in
the centre (64 px, then 22 px), `[BOOT]`; frame 5 is a 1-bit frame of the first shot.

**Outro (N + 36 + 11 frames):**
- r 0..N−1: the day again. A contact sheet (240×135 1-bit tiles, up to 4 per row) fills one
  tile per frame, the new tile inverted, labels `01 PRESENT`…, header `[REPEAT] 03/08`, over
  the last frame of the day darkened to 0.28 with a radial veil.
- next 5 frames: the grid folds into a point (a small flat sparkle on the last).
- 15 frames: four chrome sparkles swirl in from the corners (1100 px → formation), spinning.
- lock frame: a ring expands from the formation, four corner brackets, a big flat sparkle flash
  (strong metal lock sound). `[LOCK 09] SYMBOL` label.
- 7 frames: the formation settles into the symbol's place in the logo.
- 7 frames: the wordmark resolves from 1-bit noise (10 px cells switching on).
- 4 frames: chrome cross-fades to the flat `logo-symbol.svg` ("krom, potem ploščat").
- 11 frames hold on the logo over the last frame veiled to 0.4, like the website's hero.

The chrome is real 3D (Three.js): the symbol's outline inflated with a round profile, metalness 1,
roughness 0.13, reflecting a procedural studio (black sky, white softboxes, hard horizon, accent
floor glow), with a soft bloom.

## 9. Finishing

- Film grain in post: luminance-weighted (clean blacks, quiet highlights), amplitude 0.032, seeded
  per frame, then 1-LSB TPDF dither so dark gradients don't band.
- H.264 master crf 18 / 24 Mb/s, AAC 320 kb/s 48 kHz; web version crf 23 / 8 Mb/s.
- **Photosensitivity:** full-frame flashes are single frames and spaced out; the WCAG 2.3.1 scan
  must stay ≤ 3 flashes per second (v3: 1).
- **Clean share:** v3 56 % overall (shots 55–62 %, the notebook shot 41 % with logo + ring +
  contour, which Anže approved). Target ~60 %.

## 10. What failed (do not bring back)

| Tried | Why it went | Round |
| --- | --- | --- |
| Black-and-white / heavy grade of the footage | "naj ima video kadri svojo originalno barvo" | v1 → v2 |
| Zoom / punch-in on the subject | "odstrani približevanje … kader naj ostane takšen, kot je" | v1 → v2 |
| Full-frame replacements (IG/SYS panels, star on black, paper with text, black frames) | only 4 looks may cover the frame, for a frame | v1 → v2 |
| Overlays sitting on screen for long, grey-white all the time | "overlayi … ne sivo-beli all the time … samo bliskoviti" | v2 |
| Timecode, frame counter, DAY.LOOP, barcode | "lahko ostanejo, in mogoče 1/2 daš stran" → removed half | v2 |
| Ink (black) elements on bright shots | everything white, high contrast | v2 → v3 |
| Ray-eye in the sauna, cheetah, a second eagle | replaced by his choice: sword + orbital HUD, tiger, helmet | v2 → v3 |
