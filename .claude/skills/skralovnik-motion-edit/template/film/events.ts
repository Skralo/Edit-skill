// THE EDIT. This is the one creative file per film (with film.json and sfx-plan.json): every
// visual event, frame-exact. The picture draws it and export-cues.ts hands the same list to the
// sound design, so every sound lands on the frame of its event.
//
// This version is SKRALOVNIK v3 (approved 28. 9. 2026). Per shot the recipe is:
//   in-transition on the cut (strips / neg / dit / chrome wipe, never the same twice in a row)
//   -> a white circular scan finds the subject and locks (6 frames)
//   -> the result: an element flashes beside it for 4 frames
//   -> at most one extra beat (chapter word, film strip, word ring, contour, negative)
// and the footage stays clean for the rest of the shot (~55-60 % of its frames).
import { boot, element, Ev, outro, s, scan } from '../src/film/config';

export const EVENTS: Ev[] = [
  ...boot(),

  // 1 Present: the mind ----------------------------------------------------------------
  { id: 'p-in', o: s(0), dur: 2, fn: 'transition', look: 'strips', shot: 0, note: 'thin glitch strips knock the first shot in' },
  scan('p', 0, 3, 6, 'circular scan of the face', '[MIND]'),
  element('p', 0, 9, 'brain', '[MIND]', 'result: the brain flashes beside the scan'),
  { id: 'p-type', o: s(0) + 23, dur: 1, fn: 'micro', look: 'type', shot: 0, note: 'PRESENT over the footage, too big for the frame', p: { size: 760, x: 900 } },

  // 2 Build (typing) --------------------------------------------------------------------
  { id: 'b1-in', o: s(1), dur: 1, fn: 'transition', look: 'neg', shot: 1, note: 'cut in on the negative' },
  scan('b1', 1, 4, 6, 'small scan of the meander ring', '[FOCUS]'),
  { id: 'b1-strip', o: s(1) + 14, dur: 4, fn: 'texture', look: 'strip', shot: 1, note: 'film strip of the last frames rolls up the right edge' },

  // 3 Train: strength --------------------------------------------------------------------
  { id: 't-in', o: s(2) - 2, dur: 4, hit: s(2), fn: 'transition', look: 'wipe', shot: 2, note: 'chrome sparkle swells through the lens and wipes to TRAIN' },
  scan('t', 2, 4, 6, 'scan of the head on the bar', '[STRENGTH]'),
  element('t', 2, 10, 'eagle', '[STRENGTH]', 'result: the eagle flashes beside the scan'),

  // 4 Build (notebook) --------------------------------------------------------------------
  { id: 'b2-in', o: s(3), dur: 1, fn: 'transition', look: 'dit', shot: 3, note: 'cut in on a 1-bit frame' },
  scan('b2', 3, 4, 6, 'scan of the face over the notebook', '[PLAN]'),
  element('b2', 3, 10, 'logo', '[PLAN]', 'result: the SKRALOVNIK logo, white and big'),
  { id: 'b2-ring', o: s(3) + 10, dur: 8, fn: 'texture', look: 'ring', shot: 3, note: 'the word ring turns around him, behind him (needs this shot in matteShots)' },
  { id: 'b2-contour', o: s(3) + 19, dur: 4, fn: 'texture', look: 'contour', shot: 3, note: 'the silhouette traces itself in hairline' },

  // 5 Run: speed ---------------------------------------------------------------------------
  { id: 'r-in', o: s(4), dur: 2, fn: 'transition', look: 'strips', shot: 4, note: 'thin glitch strips' },
  scan('r', 4, 3, 6, "scan of the runner's head", '[SPEED]'),
  element('r', 4, 9, 'tiger', '[SPEED]', 'result: the tiger leaps ahead of the runner', 1),
  { id: 'r-type', o: s(4) + 24, dur: 1, fn: 'micro', look: 'type', shot: 4, note: 'RUN over the footage, too big for the frame', p: { size: 1060, x: 1000 } },

  // 6 Team -------------------------------------------------------------------------------
  { id: 'tm-in', o: s(5), dur: 1, fn: 'transition', look: 'neg', shot: 5, note: 'cut in on the negative' },
  scan('tm', 5, 3, 6, 'scan of the two of them', '[TEAM]'),
  element('tm', 5, 9, 'figures', '[TEAM]', 'result: three figures flash beside the scan'),

  // 7 Recover: insight -------------------------------------------------------------------
  { id: 'rc-in', o: s(6), dur: 1, fn: 'transition', look: 'dit', shot: 6, note: 'cut in on a 1-bit frame' },
  { id: 'rc-orbit', o: s(6) + 5, dur: 6, hit: s(6) + 10, fn: 'lock', look: 'orbit', shot: 6, note: 'the orbital HUD is the scan: its eye locks on the head', p: { label: '[INSIGHT]', fx: 0.4, fy: -0.5 } },
  element('rc', 6, 12, 'sword', '[SHARPEN]', 'result, a beat later: the sword'),
  { id: 'rc-neg', o: s(6) + 26, dur: 1, fn: 'micro', look: 'neg', shot: 6, note: 'negative of the heat' },

  // 8 Repeat: rise -------------------------------------------------------------------------
  { id: 'rp-in', o: s(7) - 2, dur: 4, hit: s(7), fn: 'transition', look: 'wipe', shot: 7, note: 'chrome sparkle wipes to REPEAT' },
  scan('rp', 7, 4, 5, 'scan of the lift as the camera pulls back', '[RISE]'),
  element('rp', 7, 9, 'helmet', '[DISCIPLINE]', 'result: the Spartan helmet'),

  // Outro: the day again, then the mark ----------------------------------------------
  ...outro(),
];
