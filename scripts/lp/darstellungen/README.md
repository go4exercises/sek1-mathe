# Bauskripte: Leitprogramm Darstellungen wechseln (Lineare Funktionen II)

Fünftes Leitprogramm (Bereich Funktionen), gebaut am 10.10.2026 im Kapitelmuster von `HOWTO-leitprogramme.md`,
nach `~/TODO-BM-Vorkurs-LP03-15.md` §3 («Lineare Funktionen II: Darstellungswechsel»), für die Sek I umgesetzt.
Gerüst aus `scripts/lp/lineare-funktionen/` (Achsen, Leiste, Übungsschleife, Clip-Helfer). Baut auf LP 4 auf.
Kapitel: Vier Darstellungen · Wenn die Summe gleich bleibt · Sinnvolle Werte, saubere Achsen · Linear fallend oder
antiproportional? Alles ohne Taschenrechner. Je Kapitel ① Einführungsclip (mit einer Vorhersagefrage) → ② Erkundung mit
Aufgabenleiste → ③ Kontrollclip (fünf Fragen) → Festhalten → ④ Üben → ⑤ Aufgaben. Aus der Vorlage umgesetzt:
Text ↔ Term ↔ Tabelle ↔ Graph ↔ Aussage, 2x + 2y = U → y = U/2 − x, Definitionsbereich und Achsen mit Einheit,
linear fallend ≠ antiproportional (Rechteck mit konstantem Umfang, Velofahrt), Falsch-Aussagen mit Gegenbeispiel
(Übung `gegenbeispiel`, 4d, G8). Prüfungsanker: Treppe (Clip 3), Rechteckumfang (Kapitel 2, G3, G8), Velofahrt (Clip 4).
Nicht umgesetzt: Teams-Ablauf, Lehrpersonenteil.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/darstellungen.html` vollständig aus diesem Ordner (nur der SEO-Block kommt aus der bestehenden Seite) | **ja**, nach jeder Änderung hier |
| `kopf.css` | Grundgerüst der Leitprogramme (wie Bruchrechnen) | wird eingebunden |
| `seite.css` | wie Lineare Funktionen, dazu Rechteckbild, Kurve, Auswahlfeld | wird eingebunden |
| `basis.js` | Thema hell/dunkel, Fortschritt (`lp-darst-*`), Schiene, «alle Lösungen» | wird eingebunden |
| `seite.js` | `Achsen` mit `kurve`, Sim 1 vier Darstellungen, Sim 2 Rechteck mit festem Umfang, Sim 3 Definitionsbereich (Strecke/Punkte), Sim 4 Summe oder Produkt, 8 Übungstypen (`TYPEN`, Feld `w` = Auswahl) | wird eingebunden |
| `clips.py` | erzeugt die acht Drehbücher `clips/dar-lp-*.json` (Reihe «Funktionen sehen», `probe`); rettet gemessene `dauer` | **ja**, nach jeder Änderung an den Clips; danach `build-clips.py` |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips (faster-whisper **medium**) → `wortzeiten.json` | nach jeder (Teil-)Vertonung |
| `zahlen.py` | rechnet jede feste Zahl von Seite, Simulationen, Clips und PDFs nach, auch die Fehlerwerte | **muss bestehen** |
| `pruef-schritte.mjs` | Lösbarkeit der Leisten, Ränder von Sim 2 und 3, Verteilung der Würfe je Typ | **muss bestehen** |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/darstellungen/*.tex` (Gitter aus `ds-gitter.sty`, dazu `\leernetz`
ohne Achsen für G5), gebaut mit `python3 scripts/build-lp-pdf.py darstellungen`.

## Clips

```sh
python3 scripts/lp/darstellungen/clips.py                         # Drehbücher
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py dar-lp-<name> [--szenen 2,5]      # Ton, misst dauer
python3 scripts/build-clip-fragen-ton.py dar-lp-<name>              # Ton der Fragen
python3 scripts/lp/darstellungen/wortzeiten.py                    # Wortzeiten, dann clips.py nochmals
python3 scripts/build-clips.py dar-lp-<name>                        # HTML
python3 scripts/lp/darstellungen/seite.py                         # Clipzeiten auf den Karten
```

Bilder wie in Lineare Funktionen (`graf`, `ger`, `bew`, `ueber`), dazu Rechtecke als `vieleck` (die Ecke läuft mit
`bewegung` auf y = 12 − x), die Kurve t = 30/v als `kurven` mit Formel, das Fehlerbild der ungleichmässigen Skala als
`figuren` ohne Achsen. Gesprochen: «delta y», Punkte als «fünf, siebzig», Zahlen ausgeschrieben.

## Farben — eine Farbe, eine Bedeutung

blau = Gerade, m und lineare Zusammenhänge · orange = b · Tinte = antiproportionale Kurve · grün = Treffer · rot = Fehler.
Bereichsfarbe Petrol.

## Prüfen

```sh
python3 scripts/lp/darstellungen/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/darstellungen.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/darstellungen.html 3000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/darstellungen.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/darstellungen.html
node scripts/lp/darstellungen/pruef-schritte.mjs
node .claude/tools/pruef-fragen.mjs dar-lp-darstellungen dar-lp-kontrolle-darstellungen dar-lp-summe dar-lp-kontrolle-summe dar-lp-achsen dar-lp-kontrolle-achsen dar-lp-antiproportional dar-lp-kontrolle-antiproportional
node .claude/tools/render-check.mjs leitprogramme/darstellungen.html
```
