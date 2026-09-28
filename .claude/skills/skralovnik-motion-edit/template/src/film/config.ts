// The film's timing, read from film/film.json, plus the event types and the helpers that
// film/events.ts uses to write the edit. Nothing in here is specific to one film: cuts, chapters,
// brand and sizes all come from film.json.
import film from '../../film/film.json';

export const FILM = film;
export const FPS: number = film.fps;
export const W: number = film.width;
export const H: number = film.height;

/** Cut frames of the source: CUTS[k]..CUTS[k+1] is shot k; the last entry is the frame count. */
export const CUTS: number[] = film.cuts;
export const N = CUTS.length - 1;
export const CHAPTERS: string[] = film.chapters;

/** Boot frames before the footage starts. */
export const PRE: number = film.pre;
export const FOOT_END = PRE + CUTS[N];
/** Outro: N recap frames, 36 frames of fold, chrome and logo, then the hold on the logo. */
export const OUTRO = N + 36 + (film.outroHold as number);
export const TOTAL = FOOT_END + OUTRO;

export const shotStart = (k: number) => PRE + CUTS[k];
export const shotEnd = (k: number) => PRE + CUTS[k + 1]; // exclusive
/** Shot index at output frame o: -1 during the boot, N during the outro. */
export const shotAt = (o: number) => {
  for (let k = 0; k < N; k++) if (o < shotEnd(k)) return o < shotStart(k) ? -1 : k;
  return N;
};
/** Source frame on screen at output frame o (clamped into the footage). */
export const srcAt = (o: number) => Math.max(0, Math.min(CUTS[N] - 1, o - PRE));

/** Where the outro's logo sits (px). logo.svg is 266x116 in its own units. */
export const LOGO: { width: number; cx: number; cy: number } = film.logo;

// ---------------------------------------------------------------------------------------
// Events
// ---------------------------------------------------------------------------------------
// fn is the event's job, which is what the sound design maps:
//   micro      a 1-4 frame interruption inside a shot (a flash, a result, the chapter word)
//   transition the hit on a cut
//   lock       a scan locks onto the subject
//   texture    something textural travels (film strip, contour trace, word ring, chrome travel)
//   resolve    the logo locks
export type Fn = 'micro' | 'transition' | 'lock' | 'texture' | 'resolve';

// Base looks take the whole frame (for a frame or two at most); overlays draw over the footage.
export type BaseLook = 'neg' | 'dit' | 'type';
export type OverLook = 'boot' | 'wipe' | 'strips' | 'strip' | 'contour' | 'scan' | 'orbit' | 'element' | 'ring' | 'recap' | 'collapse' | 'converge' | 'lockup' | 'wordmark' | 'flat';
export type Look = BaseLook | OverLook;

export type Ev = {
  id: string;
  /** first frame on screen */
  o: number;
  dur: number;
  /** frame the sound belongs to (default o) */
  hit?: number;
  fn: Fn;
  /** one look for the whole event, or one per frame */
  look: Look | Look[];
  /** shot index 0..N-1, -1 boot, N outro */
  shot: number;
  note: string;
  p?: Record<string, number | string>;
};

const BASE: ReadonlySet<string> = new Set(['neg', 'dit', 'type']);
export const isBase = (l: Look): l is BaseLook => BASE.has(l);

// ---------------------------------------------------------------------------------------
// Helpers for film/events.ts
// ---------------------------------------------------------------------------------------
export const s = shotStart;

/** A circular scan around the subject; it locks (the sound) on its last frame. */
export const scan = (id: string, k: number, at: number, dur: number, note: string, label: string): Ev => ({
  id: `${id}-scan`, o: s(k) + at, dur, hit: s(k) + at + dur - 1, fn: 'lock', look: 'scan', shot: k, note, p: { label },
});

/** The result: an element flashes beside the scan for 4 frames (1-bit, clean, clean, 1-bit).
 *  side: 1 = right of the subject, -1 = left, default = towards the open side of the frame. */
export const element = (id: string, k: number, at: number, el: string, label: string, note: string, side?: number): Ev => ({
  id: `${id}-el`, o: s(k) + at, dur: 4, fn: 'micro', look: 'element', shot: k, note, p: side === undefined ? { el, label } : { el, label, side },
});

/** The boot: hairlines and a glint, then a 1-bit frame of the first shot. */
export const boot = (): Ev[] => [
  { id: 'boot', o: 0, dur: PRE - 1, fn: 'texture', look: 'boot', shot: -1, note: 'hairlines draw in from the corners around a glint' },
  { id: 'boot-dit', o: PRE - 1, dur: 1, fn: 'micro', look: 'dit', shot: -1, note: '1-bit frame of the first shot', p: { src: 0 } },
];

/** The outro: contact sheet of the day, fold, chrome sparkles converge, lock, wordmark, flat logo. */
export const outro = (): Ev[] => [
  ...Array.from({ length: N }, (_, k): Ev => ({
    id: `recap-${k + 1}`, o: FOOT_END + k, dur: 1, fn: 'micro', look: 'recap', shot: N,
    note: `contact sheet: ${CHAPTERS[k].toUpperCase()} drops into the grid`, p: { k },
  })),
  { id: 'collapse', o: FOOT_END + N, dur: 5, fn: 'texture', look: 'collapse', shot: N, note: 'the grid folds into one point' },
  { id: 'converge', o: FOOT_END + N + 5, dur: 15, hit: FOOT_END + N + 6, fn: 'texture', look: 'converge', shot: N, note: 'four chrome sparkles fly in from the corners' },
  { id: 'lockup', o: FOOT_END + N + 20, dur: 1, fn: 'resolve', look: 'lockup', shot: N, note: 'the sparkles lock into the symbol' },
  { id: 'wordmark', o: FOOT_END + N + 24, dur: 7, fn: 'texture', look: 'wordmark', shot: N, note: 'the wordmark resolves from 1-bit noise' },
  { id: 'flat', o: FOOT_END + N + 32, dur: 4, fn: 'texture', look: 'flat', shot: N, note: 'the chrome symbol settles into the flat logo' },
];
