// Outro, frames FOOT_END..TOTAL. r counts from FOOT_END; q = r - N + 8 is the same clock
// shifted so the phases after the recap keep their v3 timing for any number of shots N:
//   r 0..N-1  the day again: a contact sheet fills one tile per frame
//   q 8-12    the grid folds into a point
//   q 13-27   four chrome sparkles fly in from the corners
//   q 28      they lock into the brand symbol (resolve)
//   q 29-35   the symbol settles into its place in the logo
//   q 32-38   the wordmark resolves from 1-bit noise
//   q 40-43   the chrome symbol gives way to the flat one from logo-symbol.svg
//   q 44-     hold on the logo, over the last frame of the day, veiled like a website hero
import { Img } from 'remotion';
import { Dither, Still } from './Bits';
import { ChromeStage, Spark } from './Chrome';
import { FlatSparkle } from './Sparkle';
import { Label } from './Label';
import { CHAPTERS, CUTS, FILM, FOOT_END, H, LOGO, N, W } from './timeline';
import { brandFile, HAIR, HAIR_FAINT, lerp, PAPER, rnd } from './tokens';

const easeInOut = (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const easeOut = (t: number) => 1 - Math.pow(1 - t, 4);

// logo.svg: viewBox 274 434 266 116; its symbol's white layer spans x 388.5-419.7, y 445.1-478.1.
const K = LOGO.width / 266;
const LOGO_BOX = { x: LOGO.cx - 133 * K, y: LOGO.cy - 58 * K, w: 266 * K, h: 116 * K };
const SYM = { cx: LOGO.cx + (404.1 - 407) * K, cy: LOGO.cy + (461.6 - 492) * K, w: 31.2 * K, h: 33 * K };
// symbol.svg places four sparkles 12 units from the centre, each 25 units tip to tip, 49 units overall
const FORM = { cx: W / 2, cy: H / 2 - 20, u: 7.4 };
const OFFS: [number, number][] = [[0, -12], [12, 0], [0, 12], [-12, 0]]; // N E S W
const FROM: [number, number][] = [[W + 220, -260], [W + 220, H + 260], [-220, H + 260], [-220, -260]]; // swirl in from the corners

// contact sheet: 240x135 tiles, up to 4 per row, centred
const COLS = N <= 4 ? N : Math.min(4, Math.ceil(N / 2));
const ROWS = Math.ceil(N / COLS);
const GRID = { dx: 276, dy: 205, x: W / 2 - ((COLS - 1) * 276 + 240) / 2, y: H / 2 - ((ROWS - 1) * 205 + 135) / 2 - 10 };
const pad2 = (n: number) => String(n).padStart(2, '0');
const tileSrc = (k: number) => Math.round((CUTS[k] + CUTS[k + 1]) / 2);

/** Formation state at outro clock q (see the top): centre, unit (x/y), per-sparkle rotation. */
const formation = (r: number) => {
  if (r <= 28) return { cx: FORM.cx, cy: FORM.cy, ux: FORM.u, uy: FORM.u };
  const t = easeOut(Math.min(1, (r - 28) / 7));
  return {
    cx: lerp(FORM.cx, SYM.cx, t),
    cy: lerp(FORM.cy, SYM.cy, t),
    ux: lerp(FORM.u, SYM.w / 49, t),
    uy: lerp(FORM.u, SYM.h / 49, t),
  };
};

const sparks = (r: number): Spark[] => {
  const f = formation(r);
  const fly = r < 28 ? easeInOut(Math.min(1, Math.max(0, (r - 13) / 14))) : 1;
  const idle = r > 28 ? 0.3 * Math.sin((r - 28) * 0.2) : 0;
  return OFFS.map(([ox, oy], i) => {
    const tx = f.cx + ox * f.ux;
    const ty = f.cy + oy * f.uy;
    const spin = (1 - fly) * (i % 2 ? -1 : 1);
    return {
      x: lerp(FROM[i][0], tx, fly),
      y: lerp(FROM[i][1], ty, fly),
      size: lerp(1100, 25 * f.ux, fly),
      sx: f.uy / f.ux,
      rz: spin * Math.PI * 1.25,
      rx: (1 - fly) * 0.9 + idle * 0.5,
      ry: (1 - fly) * -0.8 + idle,
    };
  });
};

/** 1-bit dissolve: whole 10 px cells switch on in random order. */
const dissolve = (w: number, h: number, p: number, seed: number) => {
  const cell = 10;
  let d = '';
  for (let y = 0; y < h; y += cell) for (let x = 0; x < w; x += cell) if (rnd(x, y, seed) < p) d += `M${x} ${y}h${cell}v${cell}h-${cell}Z`;
  return d || 'M0 0Z';
};

export const Outro: React.FC<{ o: number }> = ({ o }) => {
  const r = o - FOOT_END;
  const q = r - N + 8;
  const flat = Math.min(1, Math.max(0, (q - 40) / 4));

  // contact sheet + fold
  let sheet: React.ReactNode = null;
  if (q < 13) {
    const fold = q >= 8 ? [0.72, 0.46, 0.24, 0.1, 0][q - 8] : 1;
    sheet = (
      <>
        {CHAPTERS.map((ch, k) => {
          if (k > r) return null;
          const col = k % COLS;
          const row = Math.floor(k / COLS);
          const x = GRID.x + col * GRID.dx;
          const y = GRID.y + row * GRID.dy;
          const cx = lerp(W / 2, x + 120, fold);
          const cy = lerp(H / 2, y + 67, fold);
          if (fold === 0) return null;
          const fresh = k === r && r < N;
          return (
            <div key={k} style={{ position: 'absolute', left: cx - 120, top: cy - 67, width: 240, height: 135, transform: `scale(${fold})` }}>
              <Dither src={tileSrc(k)} kind="d8" scale={1} style={fresh ? { filter: 'invert(1)' } : undefined} />
              <div style={{ position: 'absolute', left: -8, top: -8, width: 254, height: 149, border: `1px solid ${fresh ? PAPER : HAIR}` }} />
              {fold === 1 && (
                <Label x={0} y={149}>
                  {`${String(k + 1).padStart(2, '0')} ${ch.toUpperCase()}`}
                </Label>
              )}
            </div>
          );
        })}
        {r < N && (
          <svg width={W} height={H} style={{ position: 'absolute', left: 0, top: 0 }} shapeRendering="crispEdges">
            <path d={`M${GRID.x - 40}.5 ${GRID.y - 60}.5H${GRID.x + (COLS - 1) * GRID.dx + 280}.5M${GRID.x - 40}.5 ${GRID.y + ROWS * GRID.dy + 40}.5H${GRID.x + (COLS - 1) * GRID.dx + 280}.5`} stroke={HAIR_FAINT} />
          </svg>
        )}
        {r < N && <Label x={GRID.x - 40} y={GRID.y - 90}>{`${FILM.recapLabel}  ${pad2(r + 1)}/${pad2(N)}`}</Label>}
        {q === 12 && <FlatSparkle x={W / 2} y={H / 2} size={34} color={PAPER} />}
      </>
    );
  }

  // lock language around the formation on the resolve frame
  const lockR = q >= 28 && q <= 31;
  const ringR = 170 + (q - 28) * 60;
  const wordP = q < 32 ? 0 : [0.12, 0.28, 0.46, 0.64, 0.8, 0.93, 1][Math.min(6, q - 32)];

  return (
    <div style={{ position: 'absolute', inset: 0 }}>
      {/* the last frame of the day, held and veiled like the website's hero */}
      <Still src={CUTS[N] - 1} style={{ filter: `brightness(${q < 13 ? 0.28 : 0.4}) saturate(0.85)` }} />
      <div style={{ position: 'absolute', inset: 0, background: 'radial-gradient(ellipse 55% 50% at 50% 50%, rgba(5,6,7,0.35) 0%, rgba(5,6,7,0.6) 100%)' }} />
      {sheet}
      {q >= 13 && flat < 1 && (
        <div style={{ position: 'absolute', inset: 0, opacity: 1 - flat }}>
          <ChromeStage items={sparks(q)} glow={q === 28 ? 2.2 : q > 34 ? 1.7 : 1.1} />
        </div>
      )}
      {flat > 0 && (
        <Img src={brandFile('logo-symbol.svg')} style={{ position: 'absolute', left: LOGO_BOX.x, top: LOGO_BOX.y, width: LOGO_BOX.w, height: LOGO_BOX.h, opacity: flat }} />
      )}
      {lockR && (
        <svg width={W} height={H} style={{ position: 'absolute', left: 0, top: 0 }}>
          <circle cx={FORM.cx} cy={FORM.cy} r={ringR} fill="none" stroke={PAPER} strokeOpacity={1 - (q - 28) / 4} strokeWidth={1.5} />
          {q === 28 &&
            [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([sx, sy], i) => {
              const x = FORM.cx + sx * 230;
              const y = FORM.cy + sy * 230;
              return <path key={i} d={`M${x} ${y - sy * 44}V${y}H${x - sx * 44}`} fill="none" stroke={PAPER} strokeWidth={3} />;
            })}
        </svg>
      )}
      {q === 28 && <FlatSparkle x={FORM.cx} y={FORM.cy} size={400} color={PAPER} opacity={0.75} />}
      {q === 29 && <FlatSparkle x={FORM.cx} y={FORM.cy} size={180} color={PAPER} opacity={0.6} />}
      {wordP > 0 && (
        <div
          style={{
            position: 'absolute',
            left: LOGO_BOX.x,
            top: LOGO_BOX.y,
            width: LOGO_BOX.w,
            height: LOGO_BOX.h,
            clipPath: wordP < 1 ? `path('${dissolve(Math.ceil(LOGO_BOX.w), Math.ceil(LOGO_BOX.h), wordP, 77)}')` : undefined,
          }}
        >
          <Img src={brandFile('wordmark.svg')} style={{ width: '100%', height: '100%' }} />
        </div>
      )}
      {q >= 30 && q < 36 && <Label x={LOGO.cx + 150} y={SYM.cy - 10} color={HAIR_FAINT}>{`[LOCK ${pad2(N + 1)}] SYMBOL`}</Label>}
    </div>
  );
};
