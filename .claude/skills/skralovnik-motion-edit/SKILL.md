---
name: skralovnik-motion-edit
description: Turn a short video (personal/brand/landing clip, a few shots) into a sharp motion-design edit in the SKRALOVNIK v3 style — the footage stays in its own colour and speed, a white Iron-Man/Jarvis HUD edit arrives over it in bursts (circular scans lock on the subject, then a symbolic element flashes beside it as the "result"), full-frame flashes only for a frame (negative, 1-bit, giant chapter word, chrome-sparkle wipe), a chrome sparkle → flat logo outro, and an original SFX-only soundtrack (dry shutter / metal lock / grain, no music, no samples). Built in code (Remotion + Python) from a bundled, verified template. Use this whenever Anže or anyone asks to edit or "upgrade" a video with motion design, overlays, HUD, scans, glitch, Y2K chrome, IG/X-style fast edits, SFX, a launch/hero/landing video or a reel — e.g. "naredi edit", "podoben edit kot v3", "dodaj overlaye in SFX", "motion design za moj video" — even when they just drop a video and say "naredi mi edit". Default brand is SKRALOVNIK (logo, wordmark and Anže's elements are bundled); for any other brand swap the logo and elements. Also use it to run feedback rounds (v2, v3...) on such a film.
---

# SKRALOVNIK motion edit

A short clip becomes a ~10 s film: the day in its own colour, *analysed* in bursts. Every shot keeps
its cut and its speed and stays clean for most of its frames; the edit is a thin white HUD layer
that arrives, finds the subject, shows a "result", and leaves. The reference result is SKRALOVNIK
v3 (approved 28. 9. 2026; `examples/skralovnik-v3/` in the Skralo/Edit-skill repo).

The template in `template/` renders v3 exactly (verified: identical cues, bit-identical soundtrack,
identical frames). A new film = the same engine + three files you write: `film/film.json`,
`film/events.ts`, `film/sfx-plan.json`.

## How to work with Anže (this matters as much as the pixels)

These are his standing rules from the sessions that produced v1–v3. Follow them; they are why v3
landed.

- **Speak Slovenian, in plain words ("po domače").** Technical terms are fine once explained.
- **Ask with popups (AskUserQuestion), extensively, at the start of every session** and whenever you
  need something. Each question: explain in plain words what you mean, and in each option say what
  that answer will change. Recommend one option first. Question banks: `references/questions.md`.
- **Ask before doing anything you have not done with him before** — a new tool or service, uploading
  or copying his files somewhere, pushing to another repo, spending credits. When he says stop, stop.
- **Never claim to hear the sound.** You can measure it (peaks, sync, mono); ask him which sound works
  or fails and why.
- **Keep every version.** Each approved version stays untouched on its own branch; a new round goes to
  a new branch (`…-v2`, `…-v3`). Change only what he asked for in that round ("nič ne odstranjuj …
  edino tisto, kar ti rečem").
- **Deliver, then ask.** Push, send the video and its contact sheet with SendUserFile, then a feedback
  popup (`references/questions.md` §3). Record the answers (a `NEXT.md` in the film's repo).
- Be direct and give a recommendation; he wants a strategic partner, not a menu.

## The style in ten rules

Full grammar with every size and frame count: `references/style.md`. What each element means:
`references/elements.md`.

1. **The footage is sacred.** Original colour, original speed, no zoom/punch-in, no reframing. The
   edit is an overlay *over* the frame ("nadgradnja, Iron Man style").
2. **Everything the edit draws is white** (paper `#f4f1ea`) with a soft dark glow so it reads on
   bright shots: scans, circles, hairlines, labels, elements. No grey or black overlays.
3. **Per shot, one burst:** in-transition on the cut → a circular scan finds the subject and locks
   (6 frames) → the *result*, one element, flashes beside it for 4 frames (1-bit, clean, clean, 1-bit)
   → at most one extra beat. Then the shot stays clean.
4. **~55–60 % of every shot's frames stay clean** (no overlay at all). Measure it (`npx tsx scripts/clean.ts`).
5. **Only four looks may take the whole frame, for 1 frame** (the chrome wipe for 4): negative, 1-bit
   dither, the chapter word too big for the frame over the moving footage, the chrome sparkle wipe.
6. **Transitions rotate** (strips / negative / 1-bit / chrome wipe) and never repeat back to back.
   The chrome wipe goes on the two biggest-energy cuts only.
7. **Results are symbols, minimal and abstract**, mapped to the shot's meaning (mind → brain, strength
   → eagle, speed → tiger, team → figures, insight → orbital eye, sharpen → sword, discipline →
   helmet, plan → the logo). Mostly white.
8. **Furniture is minimal:** four registration crosses, the wordmark top left, the chapter caption
   bottom left, a hairline progress bar. Nothing else (timecode, counters, barcodes were cut as noise).
9. **Outro:** the day again as a 1-bit contact sheet, fold, four chrome sparkles fly in and lock
   into the brand symbol, the wordmark resolves from 1-bit noise, chrome settles into the flat logo.
10. **Sound is SFX only**, synced to the frame of each visual event: mostly soft, a few strong, a
    different pattern per scene, many events silent on purpose. `references/sfx.md`.

## Workflow

The step-by-step procedure with commands and what to check at each step is in
`references/process.md`. The skeleton:

1. **Intake popup** (questions §1): footage, brand (default SKRALOVNIK), elements, where it will live
   (website hero / IG / X), format, what "done" means. Get the files into the session.
2. **Set up the project** from `template/` (copy it, `npm install`, `pip install -r requirements.txt`,
   ffmpeg with libx264). Environment gotchas: `references/pipeline.md`.
3. **Analyse the footage:** `python3 scripts/prep.py --detect-cuts`, look at a contact sheet of every
   shot, decide per shot what the subject is and how to track it, and what it *means*.
4. **Plan popup** (questions §2): a shot table — chapter word, subject, in-transition, result element
   and its label, extra beat. Get his yes before building. Unknown element mapping → ask.
5. **Write the three film files** (`film.json`, `events.ts`, `sfx-plan.json`; the template's are the
   v3 values, use them as the pattern). Run `prep.py` (plates, tracking, elements, mattes).
6. **Look before you render:** render the key frames at half scale into contact sheets and *look at
   them* (legibility on bright shots, element placement, scan centred on the subject, nothing
   covering the face). Fix, then render.
7. **SFX:** for SKRALOVNIK the palette is approved (round 2): only write the per-scene plan. For a new
   brand or if he asks for new sounds, run prototype rounds first (`references/sfx.md`).
8. **Render + finish:** `scripts/render.sh <name>` → master, web version (8 Mb/s), contact sheet, and
   the checks: audio sync 0 samples, true peak ≤ −1 dBTP, ≤ 3 flashes per second (v3: 1), clean share.
9. **Deliver + feedback popup** (questions §3). Next round: change only what he names.

## References

| File | Read when |
| --- | --- |
| `references/process.md` | Doing the work: every step, command and check, in order |
| `references/style.md` | Designing or judging the picture: the full visual grammar with numbers |
| `references/elements.md` | Choosing results: the bundled elements, their meaning and treatment |
| `references/sfx.md` | Anything about sound: the brief, the palette, planning, QC, prototype rounds |
| `references/pipeline.md` | Running or changing code: architecture, film.json schema, events API, gotchas |
| `references/feedback-log.md` | Understanding *why* v3 looks as it does (v1 → v2 → v3 decisions, his words) |
| `references/questions.md` | Before any popup: the question banks with plain-language explanations |

## Bundled files

- `template/` — the working project (Remotion 4 + Three.js picture, Python plates/SFX/finishing).
  `template/film/` holds the three per-film files, currently SKRALOVNIK v3.
- `template/public/film/` — SKRALOVNIK brand (`logo.svg`, `symbol.svg`, `wordmark.svg`,
  `logo-symbol.svg`) and Anže's elements (`elements/src/*.webp`). Add `source.mp4` per film.
- The v3 example (source footage, tracking, matte, result video, cue sheet) is in the Skralo/Edit-skill
  repo under `examples/skralovnik-v3/`, not in this skill (size).
