# Bauskripte: Leitprogramm Bruchrechnen

Leitprogramm zur Themenseite 1.4 «Rechnen in ℚ» (Vorwissen 1.1–1.3), gebaut am 09.10.2026 im Kapitelmuster
von `HOWTO-leitprogramme.md`, didaktisch ergänzt nach `~/HOWTO-TODO-BM-Vorkurs-LP01-02.md` §4 (LP 01), für die
Sek I umgesetzt. Kapitel: Erweitern, Kürzen, Vergleichen · Addieren und Subtrahieren · Multiplizieren und
Dividieren · Rechenreihenfolge und negative Brüche. Alles ohne Taschenrechner. Je Kapitel ① Einführungsclip (mit einer
Vorhersagefrage) → ② Erkundung mit Aufgabenleiste → ③ Kontrollclip (fünf Fragen) → Festhalten → ④ Üben → ⑤ Aufgaben.
Die Erkundungen benutzen andere Zahlen als Clip und Festhalten. Die Seite steht bis zur Prüfung nach §15 unverlinkt
(`noindex, nofollow`, keine Karte, kein Suchindex).

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/bruchrechnen.html` vollständig aus diesem Ordner (nur der SEO-Block kommt aus der bestehenden Seite) | **ja**, nach jeder Änderung hier |
| `kopf.css` | Grundgerüst der Leitprogramme (aus TALS Mathe, Bereichsfarbe auf Petrol, Dunkelmodus mit Petrol) | wird eingebunden |
| `seite.css` | Streifen, Flächenmodell, Schrittwähler, HTML-Brüche, Tipps in Stufen | wird eingebunden |
| `basis.js` | Thema hell/dunkel, Fortschritt (`lp-bruch-*`), Schiene, «alle Lösungen» | wird eingebunden |
| `seite.js` | Sim 1–4 mit Aufgabenleiste, 8 Übungstypen (`TYPEN`), Minibilder | wird eingebunden |
| `clips.py` | erzeugt die acht Drehbücher `clips/t1-4-lp-*.json` (Reihe «Brüche sehen», `probe`); rettet gemessene `dauer`, meldet Szenen mit neuem Text | **ja**, nach jeder Änderung an den Clips; danach `build-clips.py` |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips (faster-whisper **medium**; small verhörte «Fünftel» als «Viertel») → `wortzeiten.json`; `clips.py` legt Einblendungen «@wort» darauf | nach jeder (Teil-)Vertonung |
| `zahlen.py` | rechnet jede feste Zahl von Seite, Simulationen und PDFs nach, auch die Fehlerwerte | **muss bestehen** |
| `pruef-schritte.mjs` | Lösbarkeit der Leisten, Schrittwähler-Durchlauf mit Fehlklick, Verteilung von 20 000 Würfen je Typ | **muss bestehen** |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/bruchrechnen/*.tex`, gebaut mit
`python3 scripts/build-lp-pdf.py bruchrechnen` (gemeinsame Gestaltung `downloads/leitprogramme/lp-druck.sty`).

## Clips

```sh
python3 scripts/lp/bruchrechnen/clips.py                       # Drehbücher
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py t1-4-lp-<name> [--szenen 2,5]  # Ton, misst dauer
python3 scripts/build-clip-fragen-ton.py t1-4-lp-<name>          # Ton der Fragen
python3 scripts/lp/bruchrechnen/wortzeiten.py                   # Wortzeiten, dann clips.py nochmals
python3 scripts/build-clips.py t1-4-lp-<name>                    # HTML
python3 scripts/lp/bruchrechnen/seite.py                        # Clipzeiten auf den Karten
```

Bilder: Bruchstreifen, Flächenmodell, «Wie oft passt es?», Zahlenstrahl der Vielfachen, Rechenbaum — alles `graf` mit
`figuren` und `"achsen": false` im Fenster 0 … 10. Aussprache: «Hauptnenner» wird als «Haupt Nenner» gesprochen
(`TAUSCH` in `build-clip-ton.py`).

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

blau = erster Bruch · orange = zweiter Bruch, Aufgabenleiste, Regler · grün = Ergebnis · rot = Fehler. Bereichsfarbe Petrol
(Links, Kapitel-Pillen, PDF-Knöpfe). Ausnahmen in den Clips: In Rechenketten markiert orange den Schritt, der gerade
gerechnet wird; beim Kürzen über Kreuz tragen die beiden Kürzpaare je eine Farbe.

## Lösungswege der Übungen

`stufen(o, x, y)` liefert die Teilschritte einer Rechnung (gleichnamig → Zähler verrechnen → kürzen; mal Kehrwert; Quadrat
als Produkt), `weg(term)` setzt daraus den Weg eines ganzen Terms zusammen. `hnMax(term)` begrenzt den grössten
Hauptnenner in einem Zwischenschritt (Übung «Reihenfolge»: höchstens 48).

## Prüfen

```sh
python3 scripts/lp/bruchrechnen/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/bruchrechnen.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/bruchrechnen.html 3000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/bruchrechnen.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/bruchrechnen.html
node scripts/lp/bruchrechnen/pruef-schritte.mjs
node .claude/tools/pruef-fragen.mjs t1-4-lp-erweitern t1-4-lp-kontrolle-erweitern …   # alle acht
node .claude/tools/render-check.mjs leitprogramme/bruchrechnen.html
```
