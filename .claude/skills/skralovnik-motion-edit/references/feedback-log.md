# Feedback log: how v3 came to be (28. 9. 2026)

His words verbatim (Slovenian), what they meant, and what changed. Read this to understand the
*why* behind the style, and to predict what he will like on a new film.

## The brief (session 1)

- Take the 8 s personal landing video (8 shots: Present · Build · Train · Build · Run · Team ·
  Recover · Repeat) and make it "artistic, sharp motion design": overlays in a Y2K chrome /
  tech-glitch / fine technical graphics style, flash-like, with synchronized SFX; the original
  sound removed. References: an X post (AmirMushich: "res se hitro spreminjajo frame-i") and an IG reel.
- Logo and wordmark exactly as on his website (repo `Skralo/skralovnik`, branch `website-v1`,
  `assets/logo.svg`, `symbol.svg`): "isti napis, kot sva pushala logo + wordmark".
- Working rules: "ask me through pop up anketo if you need anything"; "if you need to do or
  research, connect or do anything else, go for it, but you need to ask me before if it's something
  kar še nisi delal"; at every session start ask with extensive popups linked to detailed feedback
  and explain each question "z domačimi besedami".

## v1 → v2 (feedback round 1)

v1 was black-and-white, dense, with punch-ins and full-frame replacements (IG/SYS panels, a chrome
star on black, paper with text, black frames), a lot of HUD furniture.

| He said | Meaning | Change |
| --- | --- | --- |
| "odstrani približavanje … kader naj ostane takšen kot je in se kinda nad ta kader doda kot overlay kot neka nadgradnja, aka ironman style … hitrost videa mora ostati" | no zoom; the frame and its speed are untouchable; the edit is an HUD layer over it | punch-ins out; everything becomes an overlay |
| "naj ima video kadri svojo originalno barvo! … tvoj edit pa je bolj usmerjen v white/black stil" | footage in colour, the edit is the black/white part | colour plates; B/W only in the edit |
| "da je večinoma časa v barvnem … da so tudi overlayi taki, da niso sivo-beli, all the time … samo bliskoviti" | the edit comes in flashes, not all the time | bursts per shot; ~60 % clean frames |
| Full frame allowed (all 4): negative / color invert, a big word over the moving frame, chrome sparkle on the cut, 1-bit frame | these four, for a frame or two | the four base looks |
| "Krom, potem ploščat" | outro: chrome sparkles, then the flat website logo | chrome → flat logo-symbol |
| Labels: "lahko več, IG stil, ampak tako, da ni preveč šuma … minimalistične" | small pixel captions, but minimal | bracket labels |
| HUD: "minimal črte"; fixed furniture: "lahko ostanejo, in mogoče 1/2 daš stran" | keep half | timecode, frame counter, DAY.LOOP, barcode removed |
| Elements (he sent 5): "tvoj predlog, ampak naj bodo minimalistični, kot abstract"; "poleg edita, ki je okrogel scan, da kao rezultat analize se pole pojavi element, minimalistično"; "bliskovito"; "prilagodi kadru" | scan → result element beside it, flash-short, adapted to the shot | the scan/result burst (4-frame element) |
| Clean share: "60 %" | | target measured per shot |

SFX round 1 (three prototypes): A shutter "deluje, kul je, ampak da se manjkrat ponovi"; B lock
"deluje … več dinamike (kovina, metal, vzmet)"; C grain "deluje"; overall "malo preveč zvokov …
vzorec se ponovi večkrat … za vsako sceno drugače … manj zvokov, bolj mehke, par močnejših" →
round 2: variant families, a pattern per scene, 31 instead of 55 sounds, mostly soft, 4 strong.

## v2 → v3 (feedback round 2)

"Nič ne odstranjuj iz V2 … edino tisto, kar ti rečem." v2 was kept untouched on its own branch.

| He said | Change in v3 |
| --- | --- |
| "možgane pusti" | brain stays (Present) |
| "Orel pri drogu naj postane bolj bel" | eagle `lift` treatment |
| "Geparda odstrani, zamenjaj z (tiger) in ne spreminjaj njegovo barvo" | tiger, colour kept |
| "vsi elementi … v prevladujoči beli barvi" | every element mostly white |
| "team kader – tri ljudje … belo, high contrast, malo jih povečaj" | figures solid white, 420 px |
| savna: "odstrani element z žarki … meč in oko z krogi … ne hkrati, z rahlim zamikom" | ray-eye out; orbital HUD + sword, 2 frames apart |
| "orbital HUD … lahko ga probaš dati kot scan v enem kadru, če bo dobro zgledal – če ne bo, ne daj" | orbit *is* the scan in Recover, eye locked on the head (it looked good) |
| "orel drugič → gladiator čelada" | Spartan helmet in Repeat |
| 4. kader: "BESEDE v krogu – okrog mene, za menoj" + "moj logo element – beli, bigger" | logo as the result (250 px, white), word ring behind him via a person matte |
| "nujno: scani, tanke linije, krogi, črte – vse bele!" | every line white with a dark glow |

## v3 verdict (feedback round 3)

- Sauna (orbital scan + sword): "Deluje, pusti tako".
- Shot 4 (logo + word ring + contour, only 41 % clean): "Ne, pusti tako".
- White everything with the dark glow: "Točno to, deluje" → white stays the rule.
- SFX round 2 in context: "Deluje, gremo naprej" → the sound palette is locked.
- Open: website hero (the site overlays its own logo and chapters: remove them there or render a
  clean version; cut times shift by +6 boot frames; new poster; 1280×720 mobile), a 9:16 version for
  IG/Reels, a 4K master; the `network` element unused.

## What this says about his taste

- He protects the footage: real colour, real speed, his real day. The edit must *add*, never replace.
- He likes decisive, fast, sparse: flashes, not layers that sit.
- White, high contrast, clean; minimal labels; abstract symbols with a meaning.
- He wants to be asked, with clear options and consequences, and to see results fast.
