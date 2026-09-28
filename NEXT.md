# Edit-skill: stanje in naslednji koraki (28. 9. 2026)

## Stanje
- Skill `skralovnik-motion-edit` je narejen, preverjen in pushan (`main`).
- Predloga naredi potrjeni v3 točno (303/303 sličic enakih, zvok bit za bit enak).
- Lahek test (evals/iteration-1): svež Claude s skillom je v prvo zadel v3 stil (100 % preverjanj),
  brez skilla 21 %. Oba testa sta uporabila posnetke iz v3.
- Paket za Claude račun: `dist/skralovnik-motion-edit.skill`. Anže ga shrani v račun ("Shranim ga zdaj").
- Repo ostane javen (Anže: "Ostane javen").

## Odprto
- **Test na čisto novem posnetku** (Anže: "Zaenkrat dovolj"): pravi test bo naslednji pravi video.
  Ko pride, po njem posodobi skill (feedback-log, style, po potrebi predloga) in nov paket v `dist/`.
- Hero na spletni strani (`Skralo/skralovnik`, `website-v1`): glej `examples/skralovnik-v3/NEXT.md` §5.
- 9:16 verzija za Reels (motor je narejen za 16:9; pipeline.md §8).
- Element `network` še ni uporabljen.

## Kako sprašujem
Ob vsakem začetku seje najprej pop-up anketa, obširna, vsako vprašanje razloženo po domače, pri
vsakem odgovoru napisano, kaj spremeni (`references/questions.md`).
