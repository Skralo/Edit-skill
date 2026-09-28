# SFX: sound for the edit

The original camera sound is removed. The film is scored with an original SFX palette only: no
music, no samples, no DAW. Everything is synthesized in `scripts/sfx.py` (seeded, reproducible)
and placed on the exact frame of the visual event it belongs to.

## Contents
1. The brief (Anže's SFX prompt)
2. The approved palette (round 2)
3. Planning a film (sfx-plan.json)
4. Rounds: how to build a palette for a new brand
5. QC and delivery

---

## 1. The brief

His prompt, which still governs every round:

- An original palette; no DAW, no samples.
- Map visual events **by function**: micro-cut, object lock, texture movement, transition, resolve.
  These are the event `fn` values: `micro`, `lock`, `texture`, `transition`, `resolve`.
- Start with **three dry mechanical-digital sounds**.
- Avoid: tonal beeps, pitch-sweep lasers, bells, conventional drums, long reverb.
- Export 48 kHz / 24-bit WAVs, a **level-matched audition reel** and a **cue sheet**.
- Check peaks, clean endings and mono compatibility.
- **Don't claim to hear the result.** Ask which prototype works or fails and why, and iterate
  before making variations.

## 2. The approved palette (SKRALOVNIK, round 2)

Round 1 tested one sound per family. His verdict: A "deluje, kul je, ampak … da se manjkrat
ponovi"; B "deluje … lahko dodaš več dinamike (kovina, metal, vzmet)"; C "deluje"; overall "malo
preveč zvokov … vzorec se ponovi večkrat … za vsako sceno drugače … večinoma mehki, le par
močnejših". Round 2 answers that and was approved in context on v3 ("deluje, gremo naprej").

| Family | Character | Variants |
| --- | --- | --- |
| **A SHUTTER** | leaf shutter: open click + dull thock, close click, spring rattle | `A1_heavy` (strong cuts), `A2_mid`, `A3_mid_tight`, `A4_soft`, `A5_soft_dull`, `A6_tick` (smallest) |
| **B LOCK** | focus-servo steps (crescendo) into a metal latch that rings ~10–20 ms, spring settle, a burst of crushed bits | `B1_soft`, `B2_mid`, `B3_strong` (the logo lock, with a 20 ms filtered-noise weight) |
| **C GRAIN** | scanner head: Poisson cloud of crushed noise grains over a stepped held-noise bed, stereo scatter | `C1_short` 120 ms, `C2_mid` 260 ms, `C3_long` 520 ms, `C4_swell` (density rises into a chrome-wipe hit) |

Material, not pitch: metal is a cluster of short inharmonic resonators (decays in tens of ms), so
it reads as metal and never as a note. Every variant is matched to −20 LUFS momentary; tiers
apply only in the film mix: **soft −10 dB, mid −4.5 dB, strong 0 dB**. The film mix is normalized
so its loudest true peak sits at −1 dBTP.

## 3. Planning a film (`film/sfx-plan.json`)

```json
"plan": {
  "p-in":   [["A1_heavy", "strong"]],
  "t-in":   [["C4_swell", "mid", -5], ["A1_heavy", "strong"]],
  "p-scan": [["B1_soft", "soft"]]
}
```

Keys are event ids from `film/events.ts`; each entry is `[sound, tier]` or `[sound, tier, offset
in frames]` (negative = earlier, e.g. the swell 5 frames before the wipe). Events not listed are
**silent on purpose**. `scenes` is one line per scene for the cue sheet; `sceneOfShot` names each
shot's scene.

Rules that came out of the feedback:
- **Fewer sounds than events.** v3: 33 sounds on 31 of 44 events, 13 silent.
- **Mostly soft**, a few mid, **3–4 strong** (v3: 18 soft, 11 mid, 4 strong). Strong goes to: the
  first entry, the two chrome wipes, the logo lock.
- **A different pattern per scene**, following the picture. Examples from v3: Team, the cut is
  silent and only the lock sounds; Train, the scan is silent and only the wipe hits; Build/notebook,
  logo and ring share one long soft grain and the contour stays silent.
- **Never the same variant twice in a row**; rotate A variants on cuts.
- Map by function: transitions → A (or C4 + A1 for chrome); locks → B; results and textures → C
  (short for quick, long for slow traces), tiny micro-flashes → A6.
- The outro: a fading 4-shot motor drive over the recap (A3, A4, A5, A6 soft), C3 on the
  converge, **B3 strong** on the lock-up, C1 on the wordmark.
- Pan follows the event's place on screen (scans and results from the lock box x), ±0.7 max.

## 4. Rounds: a palette for a new brand

When the brand is new or he asks for different sounds, follow the brief literally:
1. **Round 1:** three prototypes, one per family (or three new dry mechanical-digital characters),
   plus the audition reel (level-matched, 0.5 s apart), cue sheet and QC. Send the reel **and** the
   soundtrack on the current picture.
2. **Ask** (questions.md §3, sound part): per prototype works / works but / fails and why; overall
   density; which scenes. Do not make variations before this answer.
3. **Round 2:** families of variants around what worked, the plan thinned per his density answer.
4. Keep each round in `sfx/roundN/` and never overwrite an earlier round.

To change the palette, edit the family tables in `scripts/sfx.py` (`A_FAMILY`, `B_FAMILY`,
`C_FAMILY`: each variant is a seed + parameters) and bump `sfxRound` in film.json.

## 5. QC and delivery

`sfx.py` writes to `sfx/roundN/`: every variant as a WAV (48 kHz / 24-bit), `audition-reel.wav`,
`cue-sheet.md` + `.csv` (every sound with frame, timecode, tier, pan, scene and the visual event),
`qc.md`, and `out/film/soundtrack.wav` for the mux. QC per file: momentary loudness, sample and
true peak (4× oversampled), first/last sample and the last 5 ms (clean endings), DC, L/R
correlation and mono-sum change. After muxing, `post.py` checks sync (≤ 1 ms, v3: 0 samples) and
the decoded AAC true peak (≤ −1 dBTP).

Report numbers; say plainly that you cannot hear it; ask him to listen with headphones.
