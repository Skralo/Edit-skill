// How much of every shot stays clean: frames with the footage as it is and no overlay. The HUD
// furniture (crosses, brand line, chapter caption, progress hairline) does not count as an edit.
// v3 measured 56 % overall (55-62 % per shot, 41 % in the busiest shot); the target is ~60 %.
// Run: npx tsx scripts/clean.ts
import { baseAt, CHAPTERS, eventsAt, isBase, lookAt, N, shotEnd, shotStart } from '../src/film/timeline';

let tot = 0;
let clean = 0;
const per: string[] = [];
for (let k = 0; k < N; k++) {
  let n = 0;
  let c = 0;
  for (let o = shotStart(k); o < shotEnd(k); o++) {
    n++;
    const busy = eventsAt(o).some((e) => !isBase(lookAt(e, o))) || baseAt(o).look !== 'org';
    if (!busy) c++;
  }
  tot += n;
  clean += c;
  per.push(`${k + 1} ${CHAPTERS[k]} ${Math.round((100 * c) / n)}%`);
}
console.log(`clean ${Math.round((100 * clean) / tot)}% of shot frames | ${per.join(' | ')}`);
