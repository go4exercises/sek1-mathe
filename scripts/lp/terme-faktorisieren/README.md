# Bauskripte: Leitprogramm Terme und Faktorisieren

Zweites Leitprogramm (Bereich Arithmetik/Algebra), gebaut am 09.10.2026 im Kapitelmuster von
`HOWTO-leitprogramme.md`, didaktisch nach `~/HOWTO-TODO-BM-Vorkurs-LP01-02.md` (LP 02), für die Sek I umgesetzt.
Gerüst 1:1 aus `scripts/lp/bruchrechnen/`. Kapitel: Terme vereinfachen · Klammer mal Klammer · Binomische Formeln ·
Faktorisieren. Alles ohne Taschenrechner. Je Kapitel ① Einführungsclip (mit einer Vorhersagefrage) → ② Erkundung mit
Aufgabenleiste → ③ Kontrollclip (fünf Fragen) → Festhalten → ④ Üben → ⑤ Aufgaben. Erkundungen, Kapitelaufgaben,
Kontrollfragen und Gesamttest wiederholen keine Beispiele aus Clip und Festhalten.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/terme-faktorisieren.html` vollständig aus diesem Ordner (nur SEO-Block und Footer kommen aus der bestehenden Seite, beide schreibt `build-seo.py`) | **ja**, nach jeder Änderung hier |
| `kopf.css` | Grundgerüst der Leitprogramme (wie Bruchrechnen) | wird eingebunden |
| `seite.css` | Termkacheln, Flächenmodell, Rechteckschema, Quadrat, Termfeld, Tipps in Stufen | wird eingebunden |
| `basis.js` | Thema hell/dunkel, Fortschritt (`lp-terme-*`), Schiene, «alle Lösungen» | wird eingebunden |
| `seite.js` | Polynome, Termeingabe, Sim 1–4 mit Aufgabenleiste, 8 Übungstypen (`TYPEN`), Minibilder | wird eingebunden |
| `clips.py` | erzeugt die acht Drehbücher `clips/terme-lp-*.json` (Reihe «Terme sehen», `probe`); rettet gemessene `dauer` | **ja**, nach jeder Änderung an den Clips; danach `build-clips.py` |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips (faster-whisper **medium**) → `wortzeiten.json` | nach jeder (Teil-)Vertonung |
| `zahlen.py` | rechnet jede feste Zahl und jeden Term von Seite, Simulationen, Clips und PDFs nach, auch die Fehlerwerte | **muss bestehen** |
| `pruef-schritte.mjs` | Lösbarkeit der Leisten, Termeingabe (Schreibweisen, Summe/unvollständig), Verteilung von 20 000 Würfen je Typ | **muss bestehen** |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/terme-faktorisieren/*.tex`, gebaut mit
`python3 scripts/build-lp-pdf.py terme-faktorisieren`.

## Clips

```sh
python3 scripts/lp/terme-faktorisieren/clips.py                     # Drehbücher
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py terme-lp-<name> [--szenen 2,5]     # Ton, misst dauer
python3 scripts/build-clip-fragen-ton.py terme-lp-<name>             # Ton der Fragen
python3 scripts/lp/terme-faktorisieren/wortzeiten.py                # Wortzeiten, dann clips.py nochmals
python3 scripts/build-clips.py terme-lp-<name>                       # HTML
python3 scripts/lp/terme-faktorisieren/seite.py                     # Clipzeiten auf den Karten
```

Bilder: Termkacheln (x als Streifen, 1 als kleines Quadrat, negativ rot), Flächenmodell, Rechteckschema, Quadrat der
binomischen Formeln mit umgelegtem Stück, Paartabelle — alles `graf` mit `figuren` im Fenster 0 … 10.

## Bausteine

- **Polynome** in einer Variablen als Koeffizientenliste `[c0, c1, c2]` (`P`, `pAdd`, `pMul`, `pPow`, `pEq`, `pTex`).
- **Termeingabe** (`termLesen`): `3x^2`, `3x²`, Mal-Punkt darf fehlen (`3x`, `2(x+1)`, `(x+1)(x-1)`), `−`, Klammern,
  Potenzen; `x2` wird abgelehnt (Hochzahl mit `^`), eine fremde Variable ebenso. Der Baum bleibt erhalten:
  `zusammengefasst(baum)` (keine Klammern, jede Art Glied einmal) und `produktBefund(lese)` → `summe` /
  `unvollstaendig` (Faktor mit gemeinsamem Teiler, gemeinsamer Variable oder ganzzahlig zerlegbarer Quadratik) / fertig.
  Gleichwertig, aber nicht fertig → eigener Hinweis, zählt als Versuch.
- **Tipps in drei Stufen** (`T.tipps(A)` + `T.loesung(A)`); die Lösung erscheint ausserdem nach dem zweiten Fehlversuch.
- **Sperrliste** `SPERRE`: alle festen Aufgaben, je Typ ein Schlüssel; Paare sortiert.

## Farben — eine Farbe, eine Bedeutung

blau = x², x (Variable) · orange = Zahlen, gemeinsamer Faktor · grün = Ergebnis · rot = negativ, Fehler. Im Quadrat der
binomischen Formeln: a² blau, ab orange, b² grün. Bereichsfarbe Petrol.

## Prüfen

```sh
python3 scripts/lp/terme-faktorisieren/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/terme-faktorisieren.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/terme-faktorisieren.html 3000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/terme-faktorisieren.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/terme-faktorisieren.html
node scripts/lp/terme-faktorisieren/pruef-schritte.mjs
node .claude/tools/pruef-fragen.mjs terme-lp-zusammenfassen terme-lp-kontrolle-zusammenfassen …   # alle acht
node .claude/tools/render-check.mjs leitprogramme/terme-faktorisieren.html
```
