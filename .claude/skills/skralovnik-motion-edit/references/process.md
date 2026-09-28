# Process: the procedure for every step

In order. Each step says what to do, the command, and what to check before moving on. `$SKILL` is
this skill's folder; `$FILM` is the film's project folder (a repo or a folder in the repo).

## Contents
0. Session start
1. Intake
2. Project setup
3. Footage analysis
4. The plan (and his yes)
5. Writing the film files
6. Plates, tracking, elements, mattes
7. Look before you render
8. Sound
9. Render and finish
10. Deliver and feedback
11. Next round

---

## 0. Session start

- Read the film's `NEXT.md` if it exists (the last round's feedback and open points).
- **First action: a popup** (questions.md §0 or §1). Even when you think you know what he wants.
- If a video/element arrives as an upload, ask before storing it anywhere new (repo, Drive).

## 1. Intake

Popup (questions.md §1). Settle: the footage file(s); the brand (default SKRALOVNIK); which
elements (bundled, new ones, or none yet); where it will live (website hero, IG, X); length and
format (16:9 is what the template does; 9:16 needs adaptation, see pipeline.md); what "done" means.

Get the source into `$FILM/public/film/source.mp4`. Keep the original resolution (4K is fine: plates
are made at 1080p).

## 2. Project setup

```bash
cp -r $SKILL/template $FILM            # or into an existing repo folder
cd $FILM
npm install                            # Remotion 4, Three.js, fonts
pip install -r requirements.txt        # numpy scipy opencv pillow soundfile pyloudnorm cairosvg imageio-ffmpeg mediapipe
```

Check `ffmpeg -filters | grep -c scale` works and ffmpeg has libx264. In Claude Code cloud
containers: `ln -sf $(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())") /usr/local/bin/ffmpeg`
and `apt-get install -y libegl1 libgles2 libgl1` for MediaPipe (pipeline.md §Environment).

Commit early; work on a branch per version (`film-v1`, …); never overwrite an approved version.

## 3. Footage analysis

```bash
python3 scripts/prep.py --detect-cuts     # prints "cuts": [...] and a score per cut
```

- Look at the frames either side of any cut with a score near 1: a hitch or whip pan can look like
  a cut, a soft cut between similar scenes can be missed. The last number is the frame count.
- Extract one frame from the middle of every shot and view them as one contact sheet. For each
  shot write down: what happens, who/what the subject is, where it sits in the frame (left/right,
  how big), how bright the shot is, and what it *means* in the story (the chapter word).
- Pick a tracking target per shot (film.json `shots[k].track`):
  - `face`: close-ups and talking heads (pad 1.9, aspect 1.25, lift 0.08; a runner's head: pad 2.4)
  - `head_shoulders`: medium shots (pad 1.35); groups: `which: "all"` (pad 1.25, minW 300)
  - `body`: wide shots, seated or lifting (vis 0.5, pad 1.12)
  - `flow`: an object that is not a person (a ring, a cup): give `seedFrame`, `seed` [x, y] in
    1920×1080 px, and a `box` [w, h]. Find the seed by viewing one frame at full size.
- Grade per shot (`grade`, only for the 1-bit plates): dark scene `lo 0.5, gamma 0.85–0.92, k 6`;
  bright window light `hi 97–98, gamma 0.8`; default is fine for most.

## 4. The plan (and his yes)

Build the shot table and put it in a popup (questions.md §2) before any rendering:

| # | Chapter | Subject | In | Scan | Result (label) | Extra beat |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Present | face, talking | strips | face | brain `[MIND]` | PRESENT word |
| … |

Rules for the table (style.md):
- in-transitions rotate, no repeats back to back; chrome wipe on the 2 biggest cuts; the first entry
  is the strongest;
- one result per shot, mapped by meaning (elements.md); no element that fits → scan only;
- at most one extra beat per shot, chapter word on 2 shots at most;
- if an element should pass behind the subject (word ring), that shot goes in `matteShots`.

## 5. Writing the film files

- `film/film.json`: source, cuts, chapters, brand (wordmark, colours), logo position, per-shot
  track + grade, matteShots, elements, sfxRound (schema: pipeline.md).
- `film/events.ts`: the edit, frame-exact, using the helpers (`s(k)`, `scan`, `element`, `boot`,
  `outro`). Copy the pattern of the v3 file: in-transition at `s(k)`, scan at `s(k)+3` or `+4` for 6
  frames, element right after the lock, extra beat later in the shot (`+14` … `+26`). Keep 3–4
  frames of clean footage after the cut before the scan when the in-transition is 2 frames long.
- `film/sfx-plan.json`: which events sound (section 8).

Typecheck after prep (it needs `track.json` and `elements/sizes.json`): `npx tsc --noEmit -p .`

## 6. Plates, tracking, elements, mattes

```bash
python3 scripts/prep.py              # frames, elements, plates (org/d4/d8), tracking -> track.json
python3 scripts/prep.py --matte      # only if matteShots: person matte -> public/film/matte/, cut-outs
python3 scripts/prep.py --elements   # after changing elements or their treatment
python3 scripts/prep.py --cutouts    # plates changed but the matte is committed
```

Tracking downloads three MediaPipe models on the first run (pose heavy, selfie multiclass,
DeepLab). Commit `track.json` and `matte/` (they are small and make re-renders need no MediaPipe);
plates stay out of git (regenerated).

Check the tracking: draw the boxes on a few frames per shot (or render the scan frames, step 7).
A box on the wrong person or drifting off → change that shot's target, pad or which.

## 7. Look before you render

Render the moments that matter at half scale and look at them as a contact sheet:

```bash
npx tsx scripts/export-cues.ts
npx remotion render src/index.ts Film out/check --sequence --frames=100-115 --scale=0.5 --image-format=jpeg --gl=angle --log=error
python3 scripts/sheet.py out/check out/check.jpg --frames 104,106,108,110,112,114
```

Check, per shot:
- the scan is centred on the subject and its circle does not leave the frame;
- the element sits on the open side, does not cover the face, is readable (white + dark glow) on
  the brightest part of the shot;
- labels do not collide with element details or the HUD;
- the chapter word overflows both frame edges (tune `p.size`, `p.x`);
- for a ring behind the subject: no halo around the person (tighten the matte threshold).

Then measure the clean share: `npx tsx scripts/clean.ts` (target ~55–60 % per shot; a busier
shot is fine if he asked for it).

## 8. Sound

- SKRALOVNIK: the palette is approved (round 2, confirmed in context on v3). Write only
  `film/sfx-plan.json`: fewer sounds than events, mostly soft, 3–4 strong, a different pattern
  per scene (sfx.md §Planning). `python3 scripts/sfx.py` → soundtrack + cue sheet + QC.
- New brand, or he asks for different sounds: run prototype rounds first (sfx.md §Rounds).

## 9. Render and finish

```bash
scripts/render.sh film-v1     # → video/film-v1.mp4, film-v1-web.mp4, film-v1-sheet.jpg
```

Takes ~10–15 min at 1080p (the chrome frames are the slow ones). It prints the post report:
- `sync_worst_samples` 0 (must be ≤ 48),
- `true_peak_dbtp` ≤ −1.0,
- `max_flashes_per_second` ≤ 3 (aim for 1),
- and the clean share.

Look at the contact sheet yourself before sending. If anything fails, fix and re-render; never
ship a failing check.

## 10. Deliver and feedback

- Commit (video, sheet, film files, track.json, matte, SFX round folder) and push to the version's
  branch.
- SendUserFile: the master video + the contact sheet (say where the web version is).
- Short message in Slovenian: what changed, the checks in one line, what you want him to judge.
- Feedback popup (questions.md §3): picture per changed item, the new pieces, white/legibility,
  sound in context. Always offer "works, keep it" first.
- Write the answers into `NEXT.md` (his words verbatim + what they mean for the next round).

## 11. Next round

Change exactly what he named, on a new branch, nothing else. Re-render, re-check, deliver, ask.
Stop when he approves; then offer the next leverage step (website hero, 9:16 for Reels) in one line.
