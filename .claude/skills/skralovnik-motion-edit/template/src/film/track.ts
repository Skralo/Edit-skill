import trackJson from '../../public/film/track.json';
import { srcAt } from './config';

// Written by scripts/prep.py: per source frame, the lock box [cx, cy, w, h] in output px and the
// subject's contour(s) as flat [x0, y0, x1, y1, ...] lists.
type Frame = { box: [number, number, number, number]; contour: number[][] };
const TRACK = trackJson as unknown as { frames: Frame[] };

export const boxAt = (o: number) => TRACK.frames[srcAt(o)].box;
export const boxOfSrc = (src: number) => TRACK.frames[Math.max(0, Math.min(TRACK.frames.length - 1, src))].box;
export const contourAt = (o: number) => TRACK.frames[srcAt(o)].contour;
