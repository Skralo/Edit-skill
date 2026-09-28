import { staticFile } from 'remotion';
import { FILM } from './config';

// Brand colours from film.json: a near-black canvas, paper-white for everything the edit draws,
// and the symbol's accent (used only in the chrome studio's floor glow).
export const INK: string = FILM.brand.ink;
export const PAPER: string = FILM.brand.paper;
export const ACCENT: string = FILM.brand.accent;
const rgb = (hex: string) => [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16)).join(', ');
export const HAIR = `rgba(${rgb(PAPER)}, 0.82)`;
export const HAIR_FAINT = `rgba(${rgb(PAPER)}, 0.28)`;

export const SERIF = '"Cormorant Garamond", serif';
export const PIXEL = '"Silkscreen", monospace';

const pad = (n: number) => String(n).padStart(4, '0');
export const plate = (kind: 'org' | 'd4' | 'd8', src: number) =>
  staticFile(`film/plate/${kind}/${pad(src)}.${kind === 'org' ? 'jpg' : 'png'}`);
export const elementFile = (file: string) => staticFile(`film/elements/${file}.png`);
export const cutPlate = (src: number) => staticFile(`film/plate/cut/${pad(src)}.png`);
export const brandFile = (file: string) => staticFile(`film/${file}`);

/** Deterministic hash noise in [0, 1). */
export const rnd = (a: number, b = 0, c = 0) => {
  let h = (a * 374761393 + b * 668265263 + c * 2147483647) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  h ^= h >>> 16;
  return ((h >>> 0) % 100000) / 100000;
};

export const clamp = (x: number, a: number, b: number) => Math.max(a, Math.min(b, x));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
