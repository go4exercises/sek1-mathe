# Bauskripte: Leitprogramm Lineare Funktionen

Viertes Leitprogramm (Bereich Funktionen), gebaut am 10.10.2026 im Kapitelmuster von `HOWTO-leitprogramme.md`,
nach `~/TODO-BM-Vorkurs-LP03-15.md` §2 («Lineare Funktionen I: Grundidee, Graph und Parameter»), für die Sek I umgesetzt.
Gerüst aus `scripts/lp/gleichungen-formeln/`, Geraden-Helfer der Clips aus dem TALS-Leitprogramm lineare-funktionen
(dorthin verweist die Vertiefung, ohne dass es 1:1 übernommen ist).
Kapitel: Anfangswert und Änderung · Die Steigung · Geraden zeichnen · Die Gleichung finden. Alles ohne Taschenrechner.
Je Kapitel ① Einführungsclip (mit einer Vorhersagefrage) → ② Erkundung mit Aufgabenleiste → ③ Kontrollclip
(fünf Fragen) → Festhalten → ④ Üben → ⑤ Aufgaben. Aus der Vorlage umgesetzt: m/b-Geradenexperiment (Sim 3),
Infusion als Prüfungsanker (Sim 4, Festhalten 4, Gesamttest G6/G8) mit Ratenwechsel, Selbstcheck mit zwei Wechseln
Graph/Gleichung (G4, G5) und Sachaufgaben. Nicht umgesetzt: Teams-Ablauf, Lehrpersonenteil.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/lineare-funktionen.html` vollständig aus diesem Ordner (nur SEO-Block und Footer kommen aus der bestehenden Seite, beide schreibt `build-seo.py`) | **ja**, nach jeder Änderung hier |
| `kopf.css` | Grundgerüst der Leitprogramme (wie Bruchrechnen) | wird eingebunden |
| `seite.css` | Achsen, Geraden, Punkte, Steigungsdreieck, Wertetabelle, Mini-Graphen, Klickgitter | wird eingebunden |
| `basis.js` | Thema hell/dunkel, Fortschritt (`lp-linear-*`), Schiene, «alle Lösungen» | wird eingebunden |
| `seite.js` | `Achsen` (SVG-Koordinatensystem), Sim 1 Fass, Sim 2 Steigung messen, Sim 3 b schiebt / m kippt, Sim 4 Infusion mit Wechsel, 8 Übungstypen (`TYPEN`) | wird eingebunden |
| `clips.py` | erzeugt die acht Drehbücher `clips/lin-lp-*.json` (Reihe «Funktionen sehen», `probe`); rettet gemessene `dauer` | **ja**, nach jeder Änderung an den Clips; danach `build-clips.py` |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips (faster-whisper **medium**) → `wortzeiten.json` | nach jeder (Teil-)Vertonung |
| `zahlen.py` | rechnet jede feste Zahl von Seite, Simulationen, Clips und PDFs nach, auch die Fehlerwerte | **muss bestehen** |
| `pruef-schritte.mjs` | Lösbarkeit der Leisten, Klickgitter, Verteilung der Würfe je Typ | **muss bestehen** |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/lineare-funktionen/*.tex` (Gitter aus `lf-gitter.sty`),
gebaut mit `python3 scripts/build-lp-pdf.py lineare-funktionen`.

## Clips

```sh
python3 scripts/lp/lineare-funktionen/clips.py                     # Drehbücher
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py lin-lp-<name> [--szenen 2,5]       # Ton, misst dauer
python3 scripts/build-clip-fragen-ton.py lin-lp-<name>               # Ton der Fragen
python3 scripts/lp/lineare-funktionen/wortzeiten.py                # Wortzeiten, dann clips.py nochmals
python3 scripts/build-clips.py lin-lp-<name>                         # HTML
python3 scripts/lp/lineare-funktionen/seite.py                     # Clipzeiten auf den Karten
```

Bilder: `graf` mit Geraden (`ger`), bewegten Geraden mit Stützpunkten `[t, m, b]` und Begleitern `yachse`/`dreieck`
(`bew`), Punkten mit gerechneter Beschriftung (`grafgeom`); was später erscheint, steht in einem deckungsgleichen
`ueber`-Bild. Stückweise Graphen der Infusion als `figuren` (Strecken). Gesprochen: «delta y» statt «Δy» (in `sz`
ersetzt), Punkte als «P mit zwei und fünf», Brüche als «… durch …» oder «zwei Drittel».

## Farben — eine Farbe, eine Bedeutung

blau = m und die Gerade · orange = b und der Punkt (0 | b) · grün = Treffer, Probe, Nullstelle · rot = Fehler.
Bereichsfarbe Petrol.

## Prüfen

```sh
python3 scripts/lp/lineare-funktionen/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/lineare-funktionen.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/lineare-funktionen.html 3000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/lineare-funktionen.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/lineare-funktionen.html
node scripts/lp/lineare-funktionen/pruef-schritte.mjs
node .claude/tools/pruef-fragen.mjs lin-lp-anfangswert lin-lp-kontrolle-anfangswert lin-lp-steigung lin-lp-kontrolle-steigung lin-lp-zeichnen lin-lp-kontrolle-zeichnen lin-lp-gleichung lin-lp-kontrolle-gleichung
node .claude/tools/render-check.mjs leitprogramme/lineare-funktionen.html
```
