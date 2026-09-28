#!/usr/bin/env python3
"""
Contact sheet of a rendered film: a 3-column grid of 640x360 frames on ink, for the README and for
review. By default it picks the moments that show the edit, from out/film/cues.json: each result
(the second, clean frame of every element flash), each word ring and orbital lock, the outro
lock-up and last frame, then chapter words; at most 12, in time order.

Usage: python3 scripts/sheet.py <frames_dir> <out.jpg> [--frames 16,77,108,...]
"""
import glob
import json
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pick():
    """The edit's moments, most important first: every result, ring and orbital lock, then the
    outro lock-up and the last frame, then the chapter words; the first 12, shown in time order."""
    cues = json.load(open(os.path.join(ROOT, 'out', 'film', 'cues.json')))
    first, second, third = [], [], []
    for c in cues['cues']:
        start = c['frame'] if c['fn'] != 'lock' else c['frame'] - c['dur'] + 1
        if c['look'] == 'element':
            first.append(start + 1)
        elif c['look'] in ('ring', 'orbit'):
            first.append(start + c['dur'] // 2)
        elif c['look'] == 'lockup':
            second.append(start + 4)
        elif c['look'] == 'type':
            third.append(start)
    second.append(cues['total'] - 1)
    ranked = list(dict.fromkeys(first + second + third))
    return sorted(ranked[:12])


def main():
    d, out = sys.argv[1], sys.argv[2]
    frames = [int(x) for x in sys.argv[sys.argv.index('--frames') + 1].split(',')] if '--frames' in sys.argv else pick()
    files = sorted(glob.glob(os.path.join(d, '*.png')) + glob.glob(os.path.join(d, '*.jpeg')) + glob.glob(os.path.join(d, '*.jpg')))
    by_index = {}
    for f in files:
        stem = os.path.splitext(os.path.basename(f))[0]
        num = ''.join(ch for ch in stem.split('-')[-1] if ch.isdigit())
        if num:
            by_index[int(num)] = f
    W, H, G = 640, 360, 6
    rows = (len(frames) + 2) // 3
    sheet = Image.new('RGB', (3 * W + 2 * G, rows * H + (rows - 1) * G), (5, 6, 7))
    for j, i in enumerate(frames):
        if i not in by_index:
            raise SystemExit(f'no frame {i} in {d}')
        im = Image.open(by_index[i]).convert('RGB').resize((W, H), Image.LANCZOS)
        sheet.paste(im, ((j % 3) * (W + G), (j // 3) * (H + G)))
    sheet.save(out, quality=86)
    print(out, sheet.size, 'frames', frames)


if __name__ == '__main__':
    main()
