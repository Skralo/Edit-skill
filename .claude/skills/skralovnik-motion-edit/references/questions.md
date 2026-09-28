# Questions: the popup banks

Anže's rule: ask with popups (AskUserQuestion), extensively; explain every question in plain
Slovenian ("po domače"), and in every option say **what that answer will change**. Put your
recommendation first with "(Recommended)". Max 4 questions per popup, 2–4 options each (he can
always type "Other"). Pick the questions that matter now; do not ask what you can decide or check
yourself.

Template for one question:

```
question: "<TEMA>: <plain-language explanation of what you mean, 1–3 sentences>. <the question>?"
header:   "<≤12 chars>"
options:  label = short answer; description = "<kaj se zgodi / kaj spremenim, če izbereš to>"
```

---

## §0 Session start (returning to a film)

Use when a `NEXT.md` exists. Summarise the state in one sentence inside the first question.

1. **Kje nadaljujeva?** "Zadnjič sva končala pri <v3, potrjeno / čakam feedback na …>. Kaj je danes na vrsti?"
   Options: the open items from NEXT.md (e.g. "Feedback na vN", "Spletna stran (hero)",
   "9:16 za Reels", "Nov video"), each with what you will do.
2. **Obseg sprememb:** "Ali spreminjava samo to, kar poveš, ali lahko predlagam še kaj?"
   "Samo to, kar rečem (Recommended)" → nothing else changes; "Predlagaj" → you add 1–2 proposals
   as options in the next popup.

## §1 Intake (a new film)

1. **Posnetek:** "Kateri video urejava? Po domače: potrebujem originalni posnetek (najboljša
   kakovost), ne že stisnjenega z Instagrama." Options: "Pošljem zdaj" / "Je že v repu (povem pot)" /
   "Na Drive-u (povem kje)" — each says where you will store it and that you ask before storing.
2. **Brand:** "Čigav je video? To določi logo in wordmark na koncu in v kotu."
   "SKRALOVNIK (Recommended)" → uses the bundled logo/wordmark; "Drug brand" → you need its logo SVG
   (+ symbol) and colours; "Brez brenda" → outro ends on the last frame + chapter word only.
3. **Elementi (rezultati scanov):** "Ob vsakem scanu se kot 'rezultat' za trenutek pokaže simbol
   (možgani, orel …). Katere uporabiva?" "Moje obstoječe (Recommended)" → mapping from elements.md;
   "Pošljem nove" → transparent PNG/WebP, you map them and show the mapping; "Samo scani" → no results.
4. **Kje bo video živel:** "To določi format in stiskanje." "Spletna stran – hero (16:9)" → master +
   8 Mb/s web + poster; "IG/Reels (9:16)" → needs a vertical version (its own round); "Oboje".

Optional: length (keep all shots at original speed vs. a shorter cut), chapter words (his own or
proposed), reference videos (a screen recording is enough).

## §2 The plan (before building)

Show the shot table first in the message, then ask:

1. **Rezultati po kadrih:** "Za vsak kader sem izbral simbol, ki pomeni to, kar se v kadru dogaja
   (tabela zgoraj). Se strinjaš?" "Da, tako (Recommended)" → build as planned; "Zamenjaj nekaj" →
   he names which; "Manj elementov" → some shots get the scan only.
2. **Prehodi in poudarki:** "Na rezih se izmenjujejo negativ, 1-bit sličica, glitch trakovi in
   krom iskrica (krom na dveh največjih rezih). Velika beseda poglavja se pokaže 2×." Options:
   as planned / more chrome / fewer full-frame flashes.
3. **Koliko edita:** "Kader ostane čist ~60 % časa, edit pride v 'izbruhih'." "~60 % čisto
   (Recommended)" / "Več edita (~45 %)" / "Manj edita (~75 %)" — each says what gets added/removed.
4. **Zvok:** "Original zvok gre ven, ostanejo samo SFX." "Moja paleta (SKRALOVNIK) (Recommended)" →
   approved sounds, new plan per scene; "Nova paleta" → 3 prototypes first, you judge, then variants.

## §3 Feedback (after delivering a version)

Ask per thing that changed, plus the constants. Always offer "deluje, pusti tako" first.

1. **<Nov element / sprememba X>:** "Po domače: <kaj vidi, v katerem kadru, koliko sličic>. Kako
   deluje?" "Deluje, pusti tako" → nothing changes; "Dober, a <prevelik/preglasen/…>" → the concrete
   tweak; "Ne, vrni <prejšnje>" → the fallback; "<Drug čas/mesto>" → he writes how in Other.
2. **Gostota:** "Kader X je čist samo NN % (ostali ~58 %). Je prenatrpan?" "Ne, pusti" / "Odstrani
   <najmanj pomembno>" (→ back to ~55 %) / "Podaljšaj/upočasni <ključno>".
3. **Barva in berljivost:** "Vse črte in elementi so beli z mehko temno senco. Kako zgleda?"
   "Točno to" / "Na svetlih se slabo vidi" (→ stronger glow) / "Senca je umazana" (→ less glow) /
   "Nek element ne paše" (→ which, in Other).
4. **Zvok v kontekstu:** "Poslušaj s slušalkami. <kaj je novega>. Kako deluje?" "Deluje, gremo
   naprej" (→ lock the sound) / "Še vedno preveč zvokov" (→ remove ~1/3) / "Premehko" (→ lift soft
   tier, more strong hits on …) / "Posamezni zvoki ne pašejo" (→ which scene/sound, why).

SFX prototype round (sfx.md §4): per prototype A/B/C: "Deluje" / "Deluje, ampak … (napiši)" /
"Ne deluje (zakaj)"; plus overall: too many / too few / pattern repeats / too loud.

## §4 Before anything new

Whenever the next step is something not done with him before (a new service or connector, storing
his files in a new place, pushing to another repo, a paid generation), one short question: what you
want to do, why, what it costs or touches, "Da, naredi" / "Ne" / "Drugače (napiši)". Then wait.
