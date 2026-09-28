// The film's single source of truth: the timing from film/film.json (config.ts) and the edit
// from film/events.ts. The picture reads EVENTS frame by frame; scripts/export-cues.ts hands the
// same list to the sound design.
import { EVENTS } from '../../film/events';
import { BaseLook, Ev, isBase, Look } from './config';

export * from './config';
export { EVENTS };

/** The look of event e at output frame o (one look for the event, or one per frame). */
export const lookAt = (e: Ev, o: number): Look => (Array.isArray(e.look) ? e.look[Math.min(o - e.o, e.look.length - 1)] : e.look);

export const eventsAt = (o: number) => EVENTS.filter((e) => o >= e.o && o < e.o + e.dur);

export const baseAt = (o: number): { look: BaseLook | 'org'; ev?: Ev } => {
  for (const e of eventsAt(o)) {
    const l = lookAt(e, o);
    if (isBase(l)) return { look: l, ev: e };
  }
  return { look: 'org' };
};
