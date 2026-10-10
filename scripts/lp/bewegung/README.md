# Bauskripte: Leitprogramm Texte, Geschwindigkeit und Begegnung

Siebtes Leitprogramm (Bereich Mathematisieren), gebaut am 10.10.2026 im Kapitelmuster von `HOWTO-leitprogramme.md`,
nach `~/TODO-BM-Vorkurs-LP03-15.md` §5 («Mathematisieren: Texte, Geschwindigkeit und Begegnung»), für die Sek I umgesetzt.
Gerüst aus `scripts/lp/funktionstypen/`. Baut auf LP 3 (Gleichungen) und LP 6 (Weg-Zeit-Graphen) auf.
Kapitel: Vom Text zur Gleichung · Weg, Geschwindigkeit, Zeit · Fahrt in Abschnitten · Begegnung und Einholen.
Alles ohne Taschenrechner. Aus der Vorlage umgesetzt: gegeben/gesucht, Variable mit Einheit, Gleichung aus Text mit
Hilfekarte (Skizze → Variable → Beziehung → Gleichung → Prüfung), `s = v · t` in drei Formen, Abschnitte in einer Tabelle,
Annäherungsgeschwindigkeit, Begegnung zweier Velos, Rolltreppe mit und gegen die Fahrrichtung, Modellannahmen,
Plausibilität. Die drei typischen Fehler: Zeit/Einheit (Kapitel 2), Annäherung gegen gleiche Richtung (Kapitel 4),
falsche Diagrammsteigung (Kapitel 3). Nicht umgesetzt: Teams-Ablauf, Lehrpersonenteil, Prüfungsnummern.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/bewegung.html` vollständig aus diesem Ordner (nur der SEO-Block kommt aus der bestehenden Seite) | **ja**, nach jeder Änderung hier |
| `kopf.css` | Grundgerüst der Leitprogramme (wie Bruchrechnen) | wird eingebunden |
| `seite.css` | wie Funktionstypen, dazu `.hilfekarte` und `svg.bahn` | wird eingebunden |
| `basis.js` | Thema hell/dunkel, Fortschritt (`lp-bew-*`), Schiene, «alle Lösungen» | wird eingebunden |
| `seite.js` | Sim 1 Tarife, Sim 2 `s = v · t`, Sim 3 zwei Abschnitte mit Tabelle und Durchschnitt, Sim 4 Begegnung/Einholen (Strecke und Abstand), 8 Übungstypen | wird eingebunden |
| `clips.py` | erzeugt die acht Drehbücher `clips/bew-lp-*.json` (Reihe «Mathematisieren», `probe`); rettet gemessene `dauer` | **ja**, nach jeder Änderung an den Clips; danach `build-clips.py` |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips (faster-whisper **medium**) → `wortzeiten.json` | nach jeder (Teil-)Vertonung |
| `zahlen.py` | rechnet jede feste Zahl von Seite, Simulationen, Clips und PDFs nach, auch die Fehlerwerte | **muss bestehen** |
| `pruef-schritte.mjs` | Lösbarkeit der Leisten, Meldungen in Sim 3/4, Verteilung der Würfe je Typ | **muss bestehen** |

Übungsfelder heissen nie `w`: `w` ist im Gerüst die Auswahlliste (`select`), ein Zahlenfeld `w` bricht die Übung.

Gesamttest und Bewertungspaket: `downloads/leitprogramme/bewegung/*.tex`, gebaut mit `python3 scripts/build-lp-pdf.py bewegung`.

## Clips

```sh
python3 scripts/lp/bewegung/clips.py                               # Drehbücher
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py bew-lp-<name> [--szenen 2,5]      # Ton, misst dauer
python3 scripts/build-clip-fragen-ton.py bew-lp-<name>              # Ton der Fragen
python3 scripts/lp/bewegung/wortzeiten.py                          # Wortzeiten, dann clips.py nochmals
python3 scripts/build-clips.py bew-lp-<name>                        # HTML
python3 scripts/lp/bewegung/seite.py                               # Clipzeiten auf den Karten
```

Bilder: Graphen nur als Strecken (`figuren`), nie als ganze Geraden (keine negativen Zeiten oder Anzahlen). Gesprochen:
Zahlwörter ausgeschrieben, Geld als «Franken» und «Rappen», «null Komma fünf» statt «ein Halb».

## Farben — eine Farbe, eine Bedeutung

blau = A bzw. erster Abschnitt · orange = B bzw. zweiter Abschnitt · grau gestrichelt = Durchschnitt bzw. Zeitpunkt ·
grün = Treffpunkt und Ergebnis · rot = Fehler. Bereichsfarbe Petrol.

## Prüfen

```sh
python3 scripts/lp/bewegung/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/bewegung.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/bewegung.html 3000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/bewegung.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/bewegung.html
node scripts/lp/bewegung/pruef-schritte.mjs
node .claude/tools/pruef-fragen.mjs clips/bew-lp-*.html
node .claude/tools/render-check.mjs leitprogramme/bewegung.html
```
