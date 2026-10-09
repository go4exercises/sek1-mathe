# Bauskripte: Leitprogramm Bruchrechnen

Leitprogramm zur Themenseite 1.4 «Rechnen in ℚ» (Vorwissen 1.1–1.3), gebaut am 09.10.2026 im Kapitelmuster
von `HOWTO-leitprogramme.md`, didaktisch ergänzt nach `~/HOWTO-TODO-BM-Vorkurs-LP01-02.md` §4 (LP 01), für die
Sek I umgesetzt. Kapitel: Erweitern, Kürzen, Vergleichen · Addieren und Subtrahieren · Multiplizieren und
Dividieren · Rechenreihenfolge und negative Brüche. Alles ohne Taschenrechner. **Ohne Clips** (Bibliothek leer):
Phase ① ist die Erkundung mit Aufgabenleiste. Die Seite steht bis zur Prüfung nach §15 unverlinkt
(`noindex, nofollow`, keine Karte, kein Suchindex).

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/bruchrechnen.html` vollständig aus diesem Ordner (nur der SEO-Block kommt aus der bestehenden Seite) | **ja**, nach jeder Änderung hier |
| `kopf.css` | Grundgerüst der Leitprogramme (aus TALS Mathe, Bereichsfarbe auf Petrol, Dunkelmodus mit Petrol) | wird eingebunden |
| `seite.css` | Streifen, Flächenmodell, Schrittwähler, HTML-Brüche, Tipps in Stufen | wird eingebunden |
| `basis.js` | Thema hell/dunkel, Fortschritt (`lp-bruch-*`), Schiene, «alle Lösungen» | wird eingebunden |
| `seite.js` | Sim 1–4 mit Aufgabenleiste, 8 Übungstypen (`TYPEN`), Minibilder | wird eingebunden |
| `zahlen.py` | rechnet jede feste Zahl von Seite, Simulationen und PDFs nach, auch die Fehlerwerte | **muss bestehen** |
| `pruef-schritte.mjs` | Lösbarkeit der Leisten, Schrittwähler-Durchlauf mit Fehlklick, Verteilung von 20 000 Würfen je Typ | **muss bestehen** |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/bruchrechnen/*.tex`, gebaut mit
`python3 scripts/build-lp-pdf.py bruchrechnen` (gemeinsame Gestaltung `downloads/leitprogramme/lp-druck.sty`).

## Bausteine

- **Brüche exakt:** `{z, n}` mit `n > 0`, nur ganze Zahlen (`B`, `plus`, `minus`, `mal`, `durch`, `hoch`).
- **Eingabe** (`bruchLesen`): `3/4`, `-3/4`, `−3/4`, `(-3)/4`, `3/-4`, `-(3/4)`, ganze Zahlen. Gleicher Wert,
  aber nicht vollständig gekürzt → eigener Hinweis, kein Fehlversuch; Dezimalzahl → «als Bruch angeben»;
  gemischte Zahl → abgelehnt (liest sich als Produkt).
- **Tipps in drei Stufen** (`T.tipps(A)` + `T.loesung(A)`): Impuls → nächster Schritt → Lösungsweg. Die Lösung
  erscheint ausserdem nach dem zweiten Fehlversuch. «in Folge» zählt nur ohne Tipp beim ersten Versuch.
- **Schrittwähler** (Sim 4): Term als Baum (`Z`, `O`, `K`, `P`); was zuerst kommt, sagt der Baum. Falsches
  Zeichen → Regel (Klammer, Potenz, Punkt vor Strich, links nach rechts), falsches Teilergebnis → Fehlertyp.
- **Sperrliste** `SPERRE`: alle festen Aufgaben (Sim, Festhalten, Kapitelaufgaben, Vortest, Gesamttest), je Typ
  ein Schlüssel; kommutative Rechnungen sortiert.

## Farben — eine Farbe, eine Bedeutung

blau = erster Bruch · orange = zweiter Bruch, Aufgabenleiste · grün = Ergebnis · rot = Fehler. Bereichsfarbe Petrol
(Links, Kapitel-Pillen, PDF-Knöpfe).

## Prüfen

```sh
python3 scripts/lp/bruchrechnen/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/bruchrechnen.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/bruchrechnen.html 3000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/bruchrechnen.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/bruchrechnen.html
node scripts/lp/bruchrechnen/pruef-schritte.mjs
node .claude/tools/render-check.mjs leitprogramme/bruchrechnen.html
```
