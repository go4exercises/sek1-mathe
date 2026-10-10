# Bauskripte: Leitprogramm Funktionstypen und Graphen

Sechstes Leitprogramm (Bereich Funktionen), gebaut am 10.10.2026 im Kapitelmuster von `HOWTO-leitprogramme.md`,
nach `~/TODO-BM-Vorkurs-LP03-15.md` §4 («Funktionstypen und Graphen interpretieren»), für die Sek I umgesetzt.
Gerüst aus `scripts/lp/funktionstypen/`. Baut auf LP 4 und LP 5 auf.
Kapitel: Vier Graphen-Familien · Proportional, antiproportional, linear · Weg-Zeit-Graphen lesen · Zurückgelegt oder noch
entfernt. Alles ohne Taschenrechner. Aus der Vorlage umgesetzt: Gerade, Parabel, Wurzel- und Kehrwertgraph qualitativ und mit
Testpunkten, proportional/antiproportional/linear mit Anfangswert, Steigung und Knicke im Weg-Zeit-Graphen, Graph zu einer
Beschreibung, zurückgelegt gegen verbleibend, fehlerhaftes Bewegungsdiagramm kritisieren (Übung `kritik`, 4e, G8). Achsen
überall mit Grösse und Einheit, jedes Bild mit Textalternative (aria-label). Nicht umgesetzt: Teams-Ablauf, Lehrpersonenteil.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/funktionstypen.html` vollständig aus diesem Ordner (nur der SEO-Block kommt aus der bestehenden Seite) | **ja**, nach jeder Änderung hier |
| `kopf.css` | Grundgerüst der Leitprogramme (wie Bruchrechnen) | wird eingebunden |
| `seite.css` | wie Darstellungen wechseln, dazu Punkt «leer» | wird eingebunden |
| `basis.js` | Thema hell/dunkel, Fortschritt (`lp-typ-*`), Schiene, «alle Lösungen» | wird eingebunden |
| `seite.js` | Familien `fam()`, Sim 1 Familie einstellen, Sim 2 Doppelt-Test, Sim 3 Weg-Zeit aus drei Abschnitten, Sim 4 Weg und Rest, Minigraphen mit `data-kurven`/`data-linie`, 8 Übungstypen | wird eingebunden |
| `clips.py` | erzeugt die acht Drehbücher `clips/typ-lp-*.json` (Reihe «Funktionen sehen», `probe`); rettet gemessene `dauer` | **ja**, nach jeder Änderung an den Clips; danach `build-clips.py` |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips (faster-whisper **medium**) → `wortzeiten.json` | nach jeder (Teil-)Vertonung |
| `zahlen.py` | rechnet jede feste Zahl von Seite, Simulationen, Clips und PDFs nach, auch die Fehlerwerte | **muss bestehen** |
| `pruef-schritte.mjs` | Lösbarkeit der Leisten, Warnung in Sim 3, Verteilung der Würfe je Typ | **muss bestehen** |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/funktionstypen/*.tex` (Gitter aus `ft-gitter.sty`, dazu `\kleingraph`, `\wegzeit`, `\skizze`), gebaut mit `python3 scripts/build-lp-pdf.py funktionstypen`.

## Clips

```sh
python3 scripts/lp/funktionstypen/clips.py                         # Drehbücher
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py typ-lp-<name> [--szenen 2,5]      # Ton, misst dauer
python3 scripts/build-clip-fragen-ton.py typ-lp-<name>              # Ton der Fragen
python3 scripts/lp/funktionstypen/wortzeiten.py                    # Wortzeiten, dann clips.py nochmals
python3 scripts/build-clips.py typ-lp-<name>                        # HTML
python3 scripts/lp/funktionstypen/seite.py                         # Clipzeiten auf den Karten
```

Bilder: Familien als `kurven` mit Formel (`x*x`, `sqrt(x)`, `1/x`), Weg-Zeit-Graphen als Strecken (`zug`), Fragebilder
nur mit dem Gegebenen. Gesprochen: Zahlwörter ausgeschrieben, «null Komma fünf» statt «ein Halb».

## Farben — eine Farbe, eine Bedeutung

blau = eigener Graph und zurückgelegter Weg · orange = Anfangswert und Rest · grau gestrichelt = Ziel · grün = Treffer · rot = Fehler.
Bereichsfarbe Petrol.

## Prüfen

```sh
python3 scripts/lp/funktionstypen/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/funktionstypen.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/funktionstypen.html 3000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/funktionstypen.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/funktionstypen.html
node scripts/lp/funktionstypen/pruef-schritte.mjs
node .claude/tools/pruef-fragen.mjs typ-lp-familien typ-lp-kontrolle-familien typ-lp-zusammenhaenge typ-lp-kontrolle-zusammenhaenge typ-lp-wegzeit typ-lp-kontrolle-wegzeit typ-lp-rest typ-lp-kontrolle-rest
node .claude/tools/render-check.mjs leitprogramme/funktionstypen.html
```
