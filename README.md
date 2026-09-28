# Edit-skill: SKRALOVNIK motion edit

Vse, kar je potrebno, da Claude naslednjič **v prvo** naredi edit, kot je SKRALOVNIK v3: skill
(navodila + postopek), delujoča predloga (koda), Anžetovi elementi in brand ter v3 kot referenčni primer.

[![SKRALOVNIK v3](examples/skralovnik-v3/video/skralovnik-v3-sheet.jpg)](examples/skralovnik-v3/video/skralovnik-v3.mp4)

**Stil v enem stavku:** posnetek ostane v svoji barvi in hitrosti, čez njega v "izbruhih" pride
bel HUD edit (okrogel scan najde subjekt, zaklene, ob njem za 4 sličice blisne simbol kot
"rezultat"), cel kader za trenutek prekrijejo samo negativ, 1-bit sličica, velika beseda in krom
iskrica. Na koncu se krom iskrice zaklenejo v logo, ki postane ploščat. Zvok: samo originalni SFX.

## Kaj je v repu

```
.claude/skills/skralovnik-motion-edit/     ← SKILL (Claude ga v tem repu naloži sam)
  SKILL.md                                 kdaj in kako; 10 pravil stila; potek dela
  references/
    process.md                             POSTOPEK za vsak korak: ukazi, kaj preveriti
    style.md                               vizualna slovnica z vsemi merami in časi
    elements.md                            elementi: kaj pomenijo, obdelava, kje so bili
    sfx.md                                 zvok: brief, potrjena paleta, planiranje, krogi, QC
    pipeline.md                            koda: arhitektura, film.json, dogodki, okolje, pasti
    feedback-log.md                        tvoj feedback v1 → v2 → v3 (tvoje besede) in zakaj
    questions.md                           ankete (pop-up), razložene po domače
  template/                                delujoč projekt (Remotion + Three.js + Python)
    film/film.json, events.ts, sfx-plan.json   ← 3 datoteke, ki se pišejo za vsak film (zdaj v3)
    public/film/                           SKRALOVNIK logo, simbol, wordmark + tvoji elementi
    src/film/, scripts/                    motor: slika, plošče, sledenje, SFX, končna obdelava
examples/skralovnik-v3/                    posnetek, sledenje, maska, video v3, SFX krogi, zapiski
dist/skralovnik-motion-edit.skill          paket za tvoj Claude račun ("Save skill")
```

## Kako ga uporabiš

**V Claude Code (ta repo odprt):** skill se naloži sam. Reci npr. *"naredi edit tega videa v
SKRALOVNIK stilu"* in dodaj posnetek. Claude te najprej vpraša z anketo, pokaže plan po kadrih,
nato naredi video, ga preveri in pošlje ter te vpraša za feedback.

**V drugem repu / v navadnem chatu:** dodaj `dist/skralovnik-motion-edit.skill` v svoj Claude račun
(gumb *Save skill*, ali claude.ai → Settings → Capabilities → Skills). Skill ima predlogo in
elemente v sebi. Za render potrebuje okolje, ki poganja kodo (Claude Code).

**Ročno:**
```bash
cp -r .claude/skills/skralovnik-motion-edit/template moj-film && cd moj-film
cp /pot/do/videa.mp4 public/film/source.mp4
npm install && pip install -r requirements.txt
python3 scripts/prep.py --detect-cuts      # rezi → film/film.json
# uredi film/film.json, film/events.ts, film/sfx-plan.json (vzorec je v3)
python3 scripts/prep.py                    # plošče, sledenje, elementi
scripts/render.sh moj-film-v1              # → video/moj-film-v1.mp4, -web.mp4, -sheet.jpg
```

Predloga je preverjena: iz `examples/skralovnik-v3/` naredi v3 točno tak, kot je bil potrjen
(vseh 303 sličic enakih, zvok bit za bit enak, vsa preverjanja zelena).

## Posodabljanje skilla

Ko potrdiš novo verzijo (v4 …), naj Claude posodobi `references/feedback-log.md` (tvoje besede),
po potrebi `style.md`, predlogo v `template/film/` in nov paket v `dist/`. Stari primeri ostanejo.
