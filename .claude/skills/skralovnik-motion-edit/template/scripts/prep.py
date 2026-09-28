#!/usr/bin/env python3
"""
Plate preparation. Everything per film comes from film/film.json.

The source video (film.json "source") becomes everything the picture needs, per source frame:

  public/film/plate/org/NNNN.jpg   WxH, the footage in its own colour (a light sharpen only)
  public/film/plate/d4/NNNN.png    W/4 x H/4 1-bit dither (full-frame 1-bit flashes)
  public/film/plate/d8/NNNN.png    W/8 x H/8 1-bit dither (film strip and contact-sheet tiles)
  public/film/track.json           per-frame lock box and subject contour (commit it)

and, from the overlay elements in public/film/elements/src/ (and the logo SVG):

  public/film/elements/NAME.png, NAME-bit.png   trimmed, mostly white, and a white 1-bit version
  public/film/elements/sizes.json               their pixel sizes
  public/film/matte/NNNN.png                    person matte for film.json "matteShots" (commit it)
  public/film/plate/cut/NNNN.png                the colour plate cut out with that matte

The lock boxes come from MediaPipe pose landmarks, per shot as film.json "shots[k].track" says
(face / head_shoulders / body, or "flow": an object followed with optical flow from a hand-placed
seed, for things that are not a pose). Contours come from two person segmenters (selfie
multiclass + DeepLab person), maxed. Models download on first run.

Usage: python3 scripts/prep.py [--detect-cuts] [--skip-track] [--elements] [--matte] [--cutouts]
  --detect-cuts   print the cut frames found by frame differencing (paste them into film.json)
"""
import json
import os
import subprocess
import sys
import urllib.request

import cv2
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILM = json.load(open(os.path.join(ROOT, 'film', 'film.json')))
PUB = os.path.join(ROOT, 'public', 'film')
SRC = os.path.join(ROOT, FILM['source'])
PLATE = os.path.join(PUB, 'plate')
WORK = os.path.join(ROOT, 'out', 'film')
MODELS = os.path.join(WORK, 'models')
W, H = FILM['width'], FILM['height']

# Cut frames of the source (CUTS[k]..CUTS[k+1] is shot k; the last entry is the frame count).
CUTS = FILM['cuts']
SHOTS = len(CUTS) - 1
N = CUTS[-1]
SHOT_CFG = FILM.get('shots', [])

MODEL_URLS = {
    'pose.task': 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task',
    'selfie_mc.tflite': 'https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite',
    'deeplab.tflite': 'https://storage.googleapis.com/mediapipe-models/image_segmenter/deeplab_v3/float32/latest/deeplab_v3.tflite',
}

def shot_of(f):
    for s in range(SHOTS):
        if CUTS[s] <= f < CUTS[s + 1]:
            return s
    return SHOTS - 1


def shot_cfg(s):
    return SHOT_CFG[s] if s < len(SHOT_CFG) else {}


# ---------------------------------------------------------------------------------------
# frames
# ---------------------------------------------------------------------------------------
def extract_frames(n=None):
    d = os.path.join(WORK, 'frames')
    os.makedirs(d, exist_ok=True)
    if len(os.listdir(d)) >= (n or N):
        return d
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', SRC, '-vf', f'scale={W}:{H}:flags=lanczos',
                    '-q:v', '1', '-start_number', '0', os.path.join(d, '%04d.jpg')], check=True)
    return d


def load(d, f):
    return cv2.imread(os.path.join(d, f'{f:04d}.jpg'))


# ---------------------------------------------------------------------------------------
# grade
# ---------------------------------------------------------------------------------------
def luma(bgr):
    x = bgr.astype(np.float32) / 255.0
    return 0.0722 * x[..., 0] + 0.7152 * x[..., 1] + 0.2126 * x[..., 2]


def s_curve(y, k=5.5, pivot=0.46):
    """Normalised sigmoid: 0 -> 0, 1 -> 1, steepest at the pivot."""
    lo = 1 / (1 + np.exp(k * pivot))
    hi = 1 / (1 + np.exp(-k * (1 - pivot)))
    return (1 / (1 + np.exp(-k * (y - pivot))) - lo) / (hi - lo)


# Per shot (film.json shots[k].grade): black point / white point percentiles and a gamma for the
# luminance the 1-bit plates are dithered from, set by eye so every shot dithers alike: deep
# blacks, faces in the upper mids. Dark scenes: lo 0.5, gamma < 1; bright scenes: hi 97-98.
GRADE_DEFAULT = dict(lo=1.0, hi=98.5, gamma=1.05, k=5.5)
SHOT_GRADE = [GRADE_DEFAULT | shot_cfg(s).get('grade', {}) for s in range(SHOTS)]


def shot_levels(frames_dir):
    lv = []
    for s in range(SHOTS):
        ys = [cv2.resize(luma(load(frames_dir, f)), (480, 270), interpolation=cv2.INTER_AREA)
              for f in range(CUTS[s], CUTS[s + 1], 3)]
        ys = np.stack(ys)
        g = SHOT_GRADE[s]
        lv.append((float(np.percentile(ys, g['lo'])), float(np.percentile(ys, g['hi']))))
    return lv


def grade_luma(bgr, s, levels):
    g = SHOT_GRADE[s]
    lo, hi = levels[s]
    y = luma(bgr)
    y = np.clip((y - lo) / max(hi - lo, 1e-3), 0, 1) ** g['gamma']
    y = s_curve(y, g['k'])
    # clarity (large-radius local contrast) + a fine sharpen, the "sharp" in the brief
    base = cv2.GaussianBlur(y, (0, 0), 28)
    y = y + 0.32 * (y - base)
    fine = cv2.GaussianBlur(y, (0, 0), 1.1)
    y = y + 0.55 * (y - fine)
    return np.clip(y, 0, 1)


def original(bgr):
    """The footage as it is: its own colour and levels, only a light sharpen after the 4K -> 1080p
    downscale."""
    x = bgr.astype(np.float32)
    x = x + 0.35 * (x - cv2.GaussianBlur(x, (0, 0), 1.0))
    return np.clip(x, 0, 255).astype(np.uint8)


def dither(y, size):
    im = Image.fromarray((cv2.resize(y, size, interpolation=cv2.INTER_AREA) * 255).astype(np.uint8), 'L')
    return im.convert('1')  # Floyd-Steinberg


def build_plates(frames_dir):
    for sub in ('org', 'd4', 'd8'):
        os.makedirs(os.path.join(PLATE, sub), exist_ok=True)
    levels = shot_levels(frames_dir)
    for f in range(N):
        s = shot_of(f)
        bgr = load(frames_dir, f)
        y = grade_luma(bgr, s, levels)
        cv2.imwrite(os.path.join(PLATE, 'org', f'{f:04d}.jpg'), original(bgr), [cv2.IMWRITE_JPEG_QUALITY, 94])
        dither(y, (W // 4, H // 4)).save(os.path.join(PLATE, 'd4', f'{f:04d}.png'))
        dither(y, (W // 8, H // 8)).save(os.path.join(PLATE, 'd8', f'{f:04d}.png'))
        if f % 40 == 0:
            print(f'  plate {f}/{N}', flush=True)


# ---------------------------------------------------------------------------------------
# tracking
# ---------------------------------------------------------------------------------------
def models():
    os.makedirs(MODELS, exist_ok=True)
    for name, url in MODEL_URLS.items():
        p = os.path.join(MODELS, name)
        if not os.path.exists(p):
            print('  downloading', name)
            urllib.request.urlretrieve(url, p)
    return {k: os.path.join(MODELS, k) for k in MODEL_URLS}


def detect(frames_dir):
    import mediapipe as mp
    from mediapipe.tasks import python as mpt
    from mediapipe.tasks.python import vision
    m = models()
    pose = vision.PoseLandmarker.create_from_options(vision.PoseLandmarkerOptions(
        base_options=mpt.BaseOptions(model_asset_path=m['pose.task']),
        running_mode=vision.RunningMode.IMAGE, num_poses=2,
        min_pose_detection_confidence=0.3, min_pose_presence_confidence=0.3))
    seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
        base_options=mpt.BaseOptions(model_asset_path=m['selfie_mc.tflite']),
        running_mode=vision.RunningMode.IMAGE, output_confidence_masks=True))
    dl = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
        base_options=mpt.BaseOptions(model_asset_path=m['deeplab.tflite']),
        running_mode=vision.RunningMode.IMAGE, output_confidence_masks=True))
    poses, masks = [], []
    for f in range(N):
        rgb = cv2.cvtColor(load(frames_dir, f), cv2.COLOR_BGR2RGB)
        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        r = pose.detect(img)
        poses.append([[(lm.x * W, lm.y * H, lm.visibility) for lm in p] for p in r.pose_landmarks])
        a = 1.0 - seg.segment(img).confidence_masks[0].numpy_view()
        b = dl.segment(img).confidence_masks[15].numpy_view()  # VOC class 15: person
        a = cv2.resize(a, (W // 2, H // 2), interpolation=cv2.INTER_LINEAR)
        b = cv2.resize(b, (W // 2, H // 2), interpolation=cv2.INTER_LINEAR)
        masks.append(np.maximum(a, b))
        if f % 40 == 0:
            print(f'  detect {f}/{N}', flush=True)
    return poses, masks


def pick(poses_f, idx, vis=0.4, which='best'):
    """Landmarks idx of one pose (or 'all' poses) with visibility above vis."""
    if not poses_f:
        return []
    cand = poses_f if which == 'all' else [max(poses_f, key=lambda p: sum(p[i][2] for i in idx))]
    return [(p[i][0], p[i][1]) for p in cand for i in idx if p[i][2] >= vis]


FACE = list(range(11))
HEAD_SHOULDERS = list(range(13))
BODY = list(range(33))


def box_of(pts, pad, min_w, aspect=None, lift=0.0):
    if not pts:
        return None
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    w = max((max(xs) - min(xs)) * pad, min_w)
    h = max((max(ys) - min(ys)) * pad, min_w * 0.75)
    if aspect:
        h = w * aspect
    return [cx, cy - lift * h, w, h]


def flow_track(frames_dir, s, cfg):
    """An object that is not a pose (v3: the ring on the typing hand), followed with median
    optical flow from a hand-placed seed: cfg seedFrame, seed [x, y] in output px, box [w, h]."""
    a, b = CUTS[s], CUTS[s + 1]
    seed_f, seed = cfg['seedFrame'], np.array(cfg['seed'], np.float64)
    bw, bh = cfg.get('box', [230, 170])
    gray = {f: cv2.cvtColor(load(frames_dir, f), cv2.COLOR_BGR2GRAY) for f in range(a, b)}
    pos = {seed_f: seed.copy()}
    for step in (1, -1):
        p = seed.copy()
        f = seed_f
        while a <= f + step < b:
            g0, g1 = gray[f], gray[f + step]
            x0, y0 = int(p[0]) - 70, int(p[1]) - 50
            pts = cv2.goodFeaturesToTrack(g0[y0:y0 + 100, x0:x0 + 140], 40, 0.01, 4)
            if pts is not None:
                pts = pts.reshape(-1, 2) + [x0, y0]
                nxt, st, _ = cv2.calcOpticalFlowPyrLK(g0, g1, pts.astype(np.float32), None,
                                                      winSize=(31, 31), maxLevel=3)
                ok = st.reshape(-1) == 1
                if ok.sum() >= 4:
                    p = p + np.median(nxt[ok] - pts[ok], axis=0)
            f += step
            pos[f] = p.copy()
    return {f: [float(pos[f][0]), float(pos[f][1]), float(bw), float(bh)] for f in range(a, b)}


def smooth(seq, sigma):
    """Gaussian smoothing of a list of equal-length vectors, edges clamped."""
    x = np.array(seq, np.float64)
    r = int(3 * sigma)
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    pad = np.concatenate([np.repeat(x[:1], r, 0), x, np.repeat(x[-1:], r, 0)])
    return np.stack([np.convolve(pad[:, i], k, 'valid') for i in range(x.shape[1])], 1)


def clamp_box(b, margin=40):
    cx, cy, w, h = b
    w, h = min(w, W - 2 * margin), min(h, H - 2 * margin)
    cx = min(max(cx, margin + w / 2), W - margin - w / 2)
    cy = min(max(cy, margin + h / 2), H - margin - h / 2)
    return [cx, cy, w, h]


def contours_of(mask, shot):
    m = (mask > 0.5).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cs = sorted(cs, key=cv2.contourArea, reverse=True)[:shot_cfg(shot).get('contours', 1)]
    out = []
    for c in cs:
        if cv2.contourArea(c) < 400:
            continue
        c = cv2.approxPolyDP(c, 1.6, True).reshape(-1, 2) * 2
        out.append([int(v) for v in c.reshape(-1)])
    return out


LANDMARKS = {'face': FACE, 'head_shoulders': HEAD_SHOULDERS, 'body': BODY}
TRACK_DEFAULT = {'target': 'body', 'vis': 0.5, 'pad': 1.12, 'minW': 220}


def build_track(frames_dir):
    """Lock box per frame, by film.json shots[k].track:
      face            the face (close-ups; pad ~1.9, aspect 1.25, lift 0.08 to include the hair)
      head_shoulders  head and shoulders (medium shots); which: "all" boxes every person (groups)
      body            the whole body (wide shots; vis 0.5 drops unsure limbs)
      flow            a non-pose object followed by optical flow (seedFrame, seed, box)"""
    poses, masks = detect(frames_dir)
    flows = {s: flow_track(frames_dir, s, shot_cfg(s)['track'])
             for s in range(SHOTS) if shot_cfg(s).get('track', {}).get('target') == 'flow'}
    raw = []
    for f in range(N):
        s, P = shot_of(f), poses[f]
        t = shot_cfg(s).get('track', TRACK_DEFAULT)
        if t['target'] == 'flow':
            b = flows[s][f]
        else:
            pts = pick(P, LANDMARKS[t['target']], vis=t.get('vis', 0.4), which=t.get('which', 'best'))
            b = box_of(pts, t.get('pad', 1.2), t.get('minW', 200), aspect=t.get('aspect'), lift=t.get('lift', 0.0))
        raw.append(b)
    frames = []
    for s in range(SHOTS):
        a, e = CUTS[s], CUTS[s + 1]
        seq = raw[a:e]
        # fill gaps from the nearest detected frame
        known = [i for i, b in enumerate(seq) if b is not None]
        if not known:  # nobody found in the whole shot: lock on the centre of the frame
            seq, known = [[W / 2, H / 2, W * 0.3, H * 0.4]] * len(seq), [0]
        seq = [seq[min(known, key=lambda k: abs(k - i))] for i in range(len(seq))]
        c = smooth([b[:2] for b in seq], 1.3)
        z = smooth([b[2:] for b in seq], 2.2)
        for i in range(e - a):
            frames.append({'box': [round(v, 1) for v in clamp_box([*c[i], *z[i]])],
                           'contour': contours_of(masks[a + i], s)})
    track = {'fps': FILM['fps'], 'width': W, 'height': H, 'cuts': CUTS, 'frames': frames}
    with open(os.path.join(PUB, 'track.json'), 'w') as fh:
        json.dump(track, fh, separators=(',', ':'))
    print('  track.json written')


# ---------------------------------------------------------------------------------------
# overlay elements
# ---------------------------------------------------------------------------------------
# film.json "elements": name -> {side: longest side in px, treat, h: on-screen height, svg}.
# Treatments keep every element mostly white (the v3 rule):
#   (none) the cut-out as drawn (use for art that is already white/light, or colour that must stay)
#   lift   lighter overall, detail kept (the eagle, "more white")
#   white  solid white, alpha kept (silhouettes: the figures, high contrast)
#   lines  dark line art turned into white lines on transparent, light fills dropped (orbital HUD)
ELEMENTS = FILM.get('elements', {})


def element_rgba(name, cfg):
    """The source cut-out as RGBA from elements/src/NAME.(webp|png), or an SVG (the logo)."""
    if cfg.get('svg'):
        import io
        import cairosvg
        png = cairosvg.svg2png(url=os.path.join(ROOT, cfg['svg']), output_width=2400)
        return np.array(Image.open(io.BytesIO(png)).convert('RGBA'))
    for ext in ('webp', 'png'):
        p = os.path.join(PUB, 'elements', 'src', f'{name}.{ext}')
        if os.path.exists(p):
            return np.array(Image.open(p).convert('RGBA'))
    raise SystemExit(f'element {name}: no elements/src/{name}.webp or .png')


def build_elements():
    """Each cut-out trimmed to its alpha, scaled, given its treatment, and saved twice: as drawn
    (NAME.png) and as white 1-bit dots (NAME-bit.png, the first and last flash frames)."""
    out_dir = os.path.join(PUB, 'elements')
    sizes = {}
    for name, cfg in ELEMENTS.items():
        side, treat = cfg.get('side', 640), cfg.get('treat')
        a = element_rgba(name, cfg)
        ys, xs = np.nonzero(a[..., 3] > 8)
        a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        k = side / max(a.shape[:2])
        a = cv2.resize(a, (round(a.shape[1] * k), round(a.shape[0] * k)), interpolation=cv2.INTER_AREA)
        rgb, alpha = a[..., :3].astype(np.float32), a[..., 3].astype(np.float32)
        lum = cv2.cvtColor(a[..., :3], cv2.COLOR_RGB2GRAY).astype(np.float32)
        if treat == 'lift':
            rgb = 255 - (255 - rgb) * 0.45
        elif treat == 'white':
            rgb = np.full_like(rgb, 255)
        elif treat == 'lines':
            alpha = np.clip(alpha * np.clip((235 - lum) / 150, 0, 1) * 1.4, 0, 255)
            rgb = np.full_like(rgb, 255)
        clean = np.dstack([rgb, alpha]).astype(np.uint8)
        value = (cv2.cvtColor(clean[..., :3], cv2.COLOR_RGB2GRAY).astype(np.float32) * alpha / 255).astype(np.uint8)
        bits = np.array(Image.fromarray(value, 'L').convert('1').convert('L'))
        bit = np.dstack([np.full(bits.shape + (3,), 255, np.uint8), np.where(alpha > 40, bits, 0).astype(np.uint8)])
        Image.fromarray(clean, 'RGBA').save(os.path.join(out_dir, f'{name}.png'))
        Image.fromarray(bit, 'RGBA').save(os.path.join(out_dir, f'{name}-bit.png'))
        sizes[name] = [int(a.shape[1]), int(a.shape[0])]
        print(f'  element {name} {sizes[name]} {treat or ""}')
    with open(os.path.join(out_dir, 'sizes.json'), 'w') as fh:
        json.dump(sizes, fh)


# ---------------------------------------------------------------------------------------
# matte (v3: the word ring passes behind Anže in the notebook shot)
# ---------------------------------------------------------------------------------------
MATTE_SHOTS = tuple(FILM.get('matteShots', []))


def build_matte(frames_dir):
    """Person matte for the shots where an element goes behind the subject: both segmenters,
    maxed, thresholded softly and feathered; saved as white-on-alpha PNGs (committed)."""
    import mediapipe as mp
    from mediapipe.tasks import python as mpt
    from mediapipe.tasks.python import vision
    m = models()
    seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
        base_options=mpt.BaseOptions(model_asset_path=m['selfie_mc.tflite']),
        running_mode=vision.RunningMode.IMAGE, output_confidence_masks=True))
    dl = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
        base_options=mpt.BaseOptions(model_asset_path=m['deeplab.tflite']),
        running_mode=vision.RunningMode.IMAGE, output_confidence_masks=True))
    out_dir = os.path.join(PUB, 'matte')
    os.makedirs(out_dir, exist_ok=True)
    for s in MATTE_SHOTS:
        for f in range(CUTS[s], CUTS[s + 1]):
            rgb = cv2.cvtColor(load(frames_dir, f), cv2.COLOR_BGR2RGB)
            img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            a = 1.0 - seg.segment(img).confidence_masks[0].numpy_view()
            b = dl.segment(img).confidence_masks[15].numpy_view()
            mk = np.maximum(cv2.resize(a, (W // 2, H // 2)), cv2.resize(b, (W // 2, H // 2)))
            mk = np.clip((mk - 0.55) / 0.25, 0, 1)  # tight: spill onto the background shows as a halo
            mk = cv2.GaussianBlur(mk, (0, 0), 1.5)
            px = np.dstack([np.full((H // 2, W // 2, 3), 255, np.uint8), (mk * 255).astype(np.uint8)])
            Image.fromarray(px, 'RGBA').save(os.path.join(out_dir, f'{f:04d}.png'))
        print(f'  matte shot {s + 1}')
    build_cutouts()


def build_cutouts():
    """The subject cut out of the colour plate with the committed matte (no MediaPipe needed), so
    an element can pass behind them: plate/cut/NNNN.png, WxH RGBA."""
    matte_dir = os.path.join(PUB, 'matte')
    if not os.path.isdir(matte_dir):
        return
    out_dir = os.path.join(PLATE, 'cut')
    os.makedirs(out_dir, exist_ok=True)
    for name in sorted(os.listdir(matte_dir)):
        f = int(name[:4])
        rgb = cv2.cvtColor(cv2.imread(os.path.join(PLATE, 'org', f'{f:04d}.jpg')), cv2.COLOR_BGR2RGB)
        alpha = cv2.resize(np.array(Image.open(os.path.join(matte_dir, name)))[..., 3], (W, H), interpolation=cv2.INTER_LINEAR)
        Image.fromarray(np.dstack([rgb, alpha]), 'RGBA').save(os.path.join(out_dir, name))


def detect_cuts():
    """Hard cuts by frame differencing: a frame whose difference to the previous one is a sharp
    peak (well above its neighbours and the clip's median) starts a new shot."""
    cap = cv2.VideoCapture(SRC)
    prev, diffs = None, []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        g = cv2.resize(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), (320, 180)).astype(np.float32)
        h = cv2.calcHist([g.astype(np.uint8)], [0], None, [32], [0, 256]).ravel()
        h /= h.sum() + 1e-9
        if prev is not None:
            diffs.append(float(np.mean(np.abs(g - prev[0]))) / 255 + 2 * float(np.abs(h - prev[1]).sum()))
        else:
            diffs.append(0.0)
        prev = (g, h)
    d = np.array(diffs)
    med = float(np.median(d[1:])) if len(d) > 1 else 0.0
    cuts = [0]
    for i in range(1, len(d)):
        lo, hi = max(1, i - 4), min(len(d), i + 5)
        others = np.concatenate([d[lo:i], d[i + 1:hi]])
        # score = mean pixel change + 2 x histogram change; hard cuts score ~1.8+, a hitch or a
        # fast pan inside one shot ~0.8. Look at the frames either side of anything near 1.
        if d[i] > max(4 * med, 1.0) and d[i] >= 2.2 * (others.max() if len(others) else 0) and i - cuts[-1] >= 8:
            cuts.append(i)
            print(f'  cut at {i}: score {d[i]:.2f}')
    cuts.append(len(d))
    print('frames', len(d), 'fps', cap.get(cv2.CAP_PROP_FPS))
    print('"cuts":', json.dumps(cuts))
    print('shot lengths:', [b - a for a, b in zip(cuts, cuts[1:])])
    return cuts


if __name__ == '__main__':
    if '--detect-cuts' in sys.argv:
        detect_cuts()
        sys.exit(0)
    if '--elements' in sys.argv:
        build_elements()
        sys.exit(0)
    if '--matte' in sys.argv:
        build_matte(extract_frames())
        sys.exit(0)
    if '--cutouts' in sys.argv:
        build_cutouts()
        sys.exit(0)
    frames_dir = extract_frames()
    print('elements')
    build_elements()
    print('plates')
    build_plates(frames_dir)
    if '--skip-track' not in sys.argv:
        print('tracking')
        build_track(frames_dir)
