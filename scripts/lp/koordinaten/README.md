# Bauskripte: Leitprogramm Abbildungen und Geraden im Koordinatensystem

Neuntes Leitprogramm (Bereich Geometrie), gebaut am 10.10.2026 im Kapitelmuster von `HOWTO-leitprogramme.md`,
nach `~/TODO-BM-Vorkurs-LP03-15.md` §7 («Koordinatengeometrie: Abbildungen und Geraden»), für die Sek I umgesetzt.
Gerüst aus `scripts/lp/pythagoras/`.
Kapitel: Punktspiegelung · Achsenspiegelung · Zentrische Streckung · Geraden durch zwei Punkte.
Aus der Vorlage umgesetzt: Koordinaten im Raster, P' = 2Z − P komponentenweise und Zentrum als Mittelpunkt, Achsenspiegelung an
den Koordinatenachsen, an Parallelen und an y = x (gleicher senkrechter Abstand), Achse aus Punkt und Bild, Streckung mit Zentrum
und Faktor k, Fläche aus Koordinaten (umschliessendes Rechteck), Flächenfaktor k², Gerade aus zwei Punkten, Punktprobe durch
Einsetzen auch weit ausserhalb jeder Zeichnung. Rechenweg und Zeichnung im Test getrennt bewertbar.
Nicht umgesetzt: Teams-Ablauf, Lehrpersonenteil, Drehungen, Abbildungsverkettung (nur als Vertiefung V1), Fläche zusammengesetzter
Figuren aus Koordinaten (nur Dreiecke, deren Ecken auf dem umschliessenden Rechteck liegen).

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/koordinaten.html` vollständig aus diesem Ordner (nur der SEO-Block kommt aus der bestehenden Seite) | **ja**, nach jeder Änderung hier |
| `kopf.css` | Grundgerüst der Leitprogramme (wie Bruchrechnen) | wird eingebunden |
| `seite.css` | wie Pythagoras | wird eingebunden |
| `basis.js` | Thema hell/dunkel, Fortschritt (`lp-koo-*`), Schiene, «alle Lösungen» | wird eingebunden |
| `seite.js` | `Achsen`, `Geo`, Sim 1 Punktspiegelung, Sim 2 Achsenspiegelung (Achse wählbar), Sim 3 Streckung, Sim 4 Gerade durch zwei Punkte, 8 Übungstypen | wird eingebunden |
| `clips.py` | erzeugt die acht Drehbücher `clips/koo-lp-*.json` (Reihe «Geometrie», `probe`); Bausteine `ks`, `ksdazu`, Fenster `WK` (−7 bis 7) | **ja**, nach jeder Änderung an den Clips; danach `build-clips.py` |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips (faster-whisper **medium**) → `wortzeiten.json` | nach jeder (Teil-)Vertonung |
| `zahlen.py` | rechnet jede feste Zahl nach (`punkt`, `zentrum`, `achse`, `streck`, `flaeche`, `gerade`, `auf`) | **muss bestehen** |
| `pruef-schritte.mjs` | Lösbarkeit der Leisten, Verteilung der Würfe je Typ | **muss bestehen** |

Übungsfelder heissen nie `w`, ausser es ist eine Auswahlliste (`achsefinden`: Achsenart, `punktprobe`: ja/nein).
Im Ton: «P mit drei und zwei» für P(3 | 2), der Ursprung heisst «Ursprung» (nie «null, null»); Whisper schreibt Zahlen als Ziffern,
Wortanker deshalb auf Wörter setzen («@also», «@gibt»), nicht auf Zahlwörter.

Gesamttest und Bewertungspaket: `downloads/leitprogramme/koordinaten/*.tex` mit Gittern aus `ko-gitter.sty`,
gebaut mit `python3 scripts/build-lp-pdf.py koordinaten`.

## Clips

```sh
python3 scripts/lp/koordinaten/clips.py                              # Drehbücher
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py koo-lp-<name> [--szenen 2,5]      # Ton, misst dauer
python3 scripts/build-clip-fragen-ton.py koo-lp-<name>              # Ton der Fragen
python3 scripts/lp/koordinaten/wortzeiten.py                         # Wortzeiten, dann clips.py nochmals
python3 scripts/build-clips.py koo-lp-<name>                        # HTML
python3 scripts/lp/koordinaten/seite.py                              # Clipzeiten auf den Karten
```

## Farben — eine Farbe, eine Bedeutung

blau = Original · orange = Bild · grün = Zentrum, Achse, Gerade · rot = Fehler. Bereichsfarbe Petrol.

## Prüfen

```sh
python3 scripts/lp/koordinaten/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/koordinaten.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/koordinaten.html 3000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/koordinaten.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/koordinaten.html
node scripts/lp/koordinaten/pruef-schritte.mjs
node .claude/tools/pruef-fragen.mjs clips/koo-lp-*.html
node .claude/tools/render-check.mjs leitprogramme/koordinaten.html
```
