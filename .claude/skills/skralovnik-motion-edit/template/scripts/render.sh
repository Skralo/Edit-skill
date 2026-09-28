#!/usr/bin/env bash
# The whole pipeline, from film/film.json + film/events.ts + film/sfx-plan.json:
#   plates (colour, 1-bit) + elements + cut-outs -> timeline export -> SFX (palette, audition reel,
#   cue sheet, QC, soundtrack) -> Remotion frames -> grain + H.264/AAC master + web version
#   -> sync / true-peak / flash checks -> contact sheet + clean share.
# track.json and matte/ are committed once made, so MediaPipe only reruns if they are missing.
#
# Usage: scripts/render.sh [out-name]      (writes video/<out-name>.mp4, -web.mp4, -sheet.jpg)
set -euo pipefail
cd "$(dirname "$0")/.."
NAME=${1:-film}
mkdir -p video
if [[ ! -f public/film/plate/org/0000.jpg ]]; then
  if [[ -f public/film/track.json ]]; then python3 scripts/prep.py --skip-track; else python3 scripts/prep.py; fi
fi
python3 scripts/prep.py --elements
if python3 -c "import json,sys; sys.exit(0 if json.load(open('film/film.json')).get('matteShots') else 1)"; then
  [[ -d public/film/matte ]] || python3 scripts/prep.py --matte
  [[ -d public/film/plate/cut ]] || python3 scripts/prep.py --cutouts
fi
npx tsx scripts/export-cues.ts
python3 scripts/sfx.py
FRAMES=out/film/frames
rm -rf "$FRAMES"
npx remotion render src/index.ts Film "$FRAMES" --sequence --image-format=png --gl=angle --log=error
python3 scripts/post.py "$FRAMES" "video/$NAME.mp4"
cp out/film/post-report.json "out/film/post-report-$NAME.json"
python3 scripts/post.py "$FRAMES" "video/$NAME-web.mp4" --crf 23 --maxrate 8
python3 scripts/sheet.py "$FRAMES" "video/$NAME-sheet.jpg"
npx tsx scripts/clean.ts
