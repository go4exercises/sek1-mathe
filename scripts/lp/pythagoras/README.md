# Bauskripte: Leitprogramm Flächen, Pythagoras und Ähnlichkeit

Achtes Leitprogramm (Bereich Geometrie), gebaut am 10.10.2026 im Kapitelmuster von `HOWTO-leitprogramme.md`,
nach `~/TODO-BM-Vorkurs-LP03-15.md` §6 («Ebene Geometrie: Flächen, Pythagoras, Ähnlichkeit»), für die Sek I umgesetzt.
Gerüst aus `scripts/lp/bewegung/`.
Kapitel: Grundseite und Höhe · Der Satz des Pythagoras · Hilfsdreiecke und Kreis · Ähnliche Figuren.
Alles ohne Taschenrechner: alle Wurzeln gehen auf (pythagoreische Tripel; in den Übungen jede Seite ganz bis 30, halb bis 15 oder
mit einer Dezimale bis 3), grosse Wurzeln werden eingegrenzt (zwischen 25² und 30², Endziffer; halbe Zahlen über 7.5² = 7 · 8 + 0.25). Aus der Vorlage umgesetzt:
Grundseite/Höhe und Zerlegen, Pythagoras mit «Hilfsdreieck zuerst finden» (im Clip Schritt für Schritt eingeblendet),
Radius, Durchmesser, Sehne und Wasserspiegel im Rohr, ähnliche Dreiecke, Verhältnisse, Regal mit Differenzfläche,
Fehlermodule «Höhe ≠ schräge Seite» und «Flächenfaktor ≠ Längenfaktor». Nicht umgesetzt: Teams-Ablauf, Lehrpersonenteil,
Kreissektoren.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/pythagoras.html` vollständig aus diesem Ordner (nur der SEO-Block kommt aus der bestehenden Seite) | **ja**, nach jeder Änderung hier |
| `kopf.css` | Grundgerüst der Leitprogramme (wie Bruchrechnen) | wird eingebunden |
| `seite.css` | wie Bewegung, dazu `.flaeche`, `.mini-figur`, `.fest-figur` | wird eingebunden |
| `basis.js` | Thema hell/dunkel, Fortschritt (`lp-pyt-*`), Schiene, «alle Lösungen» | wird eingebunden |
| `seite.js` | `Achsen` mit `ohneAchsen`/`ohneGitter`, `Geo` (Vieleck, Kreis, rechter Winkel), Sim 1 Grundseite und Höhe, Sim 2 Quadrate, Sim 3 Sehne im Kreis, Sim 4 Streckfaktor, 8 Übungstypen mit Figuren (`figur()`) | wird eingebunden |
| `clips.py` | erzeugt die acht Drehbücher `clips/pyt-lp-*.json` (Reihe «Geometrie», `probe`); Bausteine `geo`, `dazu`, `RW`, `KR`, `segment` | **ja**, nach jeder Änderung an den Clips; danach `build-clips.py` |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips (faster-whisper **medium**) → `wortzeiten.json` | nach jeder (Teil-)Vertonung |
| `zahlen.py` | rechnet jede feste Zahl nach; `w()` prüft, dass jede Wurzel aufgeht | **muss bestehen** |
| `pruef-schritte.mjs` | Lösbarkeit der Leisten, Sim 3 bei d > r, Verteilung der Würfe je Typ (hypotenuse ≥ 12, kathete ≥ 24: ohne Rechner gibt es nicht mehr Dreiecke) | **muss bestehen** |

Übungsfelder heissen nie `w`: `w` ist im Gerüst die Auswahlliste. Clip-Fenster sind quadratisch (`fenster()` prüft das),
sonst wird ein Kreis zur Ellipse. Eine eigene Hilfsfunktion darf nicht `hoehe` heissen (überdeckt den Zeilenhöhen-Helfer).

Gesamttest und Bewertungspaket: `downloads/leitprogramme/pythagoras/*.tex` (Figuren als TikZ), gebaut mit `python3 scripts/build-lp-pdf.py pythagoras`.

## Clips

```sh
python3 scripts/lp/pythagoras/clips.py                               # Drehbücher
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py pyt-lp-<name> [--szenen 2,5]      # Ton, misst dauer
python3 scripts/build-clip-fragen-ton.py pyt-lp-<name>              # Ton der Fragen
python3 scripts/lp/pythagoras/wortzeiten.py                          # Wortzeiten, dann clips.py nochmals
python3 scripts/build-clips.py pyt-lp-<name>                        # HTML
python3 scripts/lp/pythagoras/seite.py                               # Clipzeiten auf den Karten
```

Bilder: Figuren ohne Achsen im Karo (`geo`), was erst bei einem Wort erscheint, als deckungsgleiches `dazu`-Bild.
Gesprochen: Zahlwörter ausgeschrieben, «Quadrat» für die Hochzahl 2, «Wurzel aus».

## Farben — eine Farbe, eine Bedeutung

blau = Figur, Grundseite, Kathete a · orange = Höhe, Abstand, Kathete b, Hilfsdreieck, Bildfigur · grün = Hypotenuse, Radius, Ergebnis ·
rot = Fehler. Bereichsfarbe Petrol.

## Prüfen

```sh
python3 scripts/lp/pythagoras/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/pythagoras.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/pythagoras.html 3000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/pythagoras.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/pythagoras.html
node scripts/lp/pythagoras/pruef-schritte.mjs
node .claude/tools/pruef-fragen.mjs clips/pyt-lp-*.html
node .claude/tools/render-check.mjs leitprogramme/pythagoras.html
```
