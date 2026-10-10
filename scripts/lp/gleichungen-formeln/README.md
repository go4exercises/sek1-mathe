# Bauskripte: Leitprogramm Bruchterme, Gleichungen und Formeln

Drittes Leitprogramm (Bereich Gleichungen), gebaut am 10.10.2026 im Kapitelmuster von `HOWTO-leitprogramme.md`,
nach `~/TODO-BM-Vorkurs-LP03-15.md` §1 (LP 03), für die Sek I umgesetzt. Gerüst aus `scripts/lp/terme-faktorisieren/`.
Kapitel: Bruchterme kürzen · Rechnen mit Bruchtermen · Lineare Gleichungen lösen · Formeln umstellen. Alles ohne
Taschenrechner. Je Kapitel ① Einführungsclip (mit einer Vorhersagefrage) → ② Erkundung mit Aufgabenleiste →
③ Kontrollclip (fünf Fragen) → Festhalten → ④ Üben → ⑤ Aufgaben. Aus der Vorlage umgesetzt: Fehlermodul «Kürzen von
Summanden», Antwortprüfung mit gleichwertigen Termen und nicht erlaubten Zahlen, Selbstcheck mit Bruchterm, Gleichung
und Formel, Treppenmodell. Nicht umgesetzt: Teams-Ablauf, Lehrpersonenteil.

| Datei | Zweck | laufen lassen? |
|---|---|---|
| `seite.py` | baut `leitprogramme/gleichungen-formeln.html` vollständig aus diesem Ordner (nur der SEO-Block kommt aus der bestehenden Seite) | **ja**, nach jeder Änderung hier |
| `kopf.css` | Grundgerüst der Leitprogramme (wie Bruchrechnen) | wird eingebunden |
| `seite.css` | Faktor-Chips, Hauptnenner-Tabelle, Umformungsverlauf, Rechenkette, Termfeld | wird eingebunden |
| `basis.js` | Thema hell/dunkel, Fortschritt (`lp-gleich-*`), Schiene, «alle Lösungen» | wird eingebunden |
| `seite.js` | Brüche exakt, Polynome, Bruchterme, Term-/Formel-/Mengeneingabe, Sim 1–4 mit Aufgabenleiste, 8 Übungstypen (`TYPEN`) | wird eingebunden |
| `clips.py` | erzeugt die acht Drehbücher `clips/gleich-lp-*.json` (Reihe «Gleichungen sehen», `probe`); rettet gemessene `dauer` | **ja**, nach jeder Änderung an den Clips; danach `build-clips.py` |
| `wortzeiten.py` | misst die Wortzeiten der vertonten Clips (faster-whisper **medium**) → `wortzeiten.json` | nach jeder (Teil-)Vertonung |
| `zahlen.py` | rechnet jede feste Zahl und jeden Term von Seite, Simulationen, Clips und PDFs nach, auch die Fehlerwerte | **muss bestehen** |
| `pruef-schritte.mjs` | Lösbarkeit der Leisten, Eingabe (Bruchterme gekürzt/ein Bruchstrich, Mengen, Zahlen, Formeln), Verteilung von 20 000 Würfen je Typ | **muss bestehen** |

Gesamttest und Bewertungspaket: `downloads/leitprogramme/gleichungen-formeln/*.tex`, gebaut mit
`python3 scripts/build-lp-pdf.py gleichungen-formeln`.

## Clips

```sh
python3 scripts/lp/gleichungen-formeln/clips.py                     # Drehbücher
export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
python3 scripts/build-clip-ton.py gleich-lp-<name> [--szenen 2,5]     # Ton, misst dauer
python3 scripts/build-clip-fragen-ton.py gleich-lp-<name>             # Ton der Fragen
python3 scripts/lp/gleichungen-formeln/wortzeiten.py                # Wortzeiten, dann clips.py nochmals
python3 scripts/build-clips.py gleich-lp-<name>                       # HTML
python3 scripts/lp/gleichungen-formeln/seite.py                     # Clipzeiten auf den Karten
```

Bilder: Faktor-Chips über und unter dem Bruchstrich, Waage, Rechenkette vorwärts und rückwärts — `graf` mit `figuren` im
Fenster 0 … 10. Gesprochen: Brüche als «… durch …», Klammerprodukte als «Klammer … mal Klammer …».

## Bausteine

- **Brüche exakt** `[z, n]` (`B`, `bAdd`, …), Zahleingabe `zahlLesen` (−4, 2.5, 7/3; Dezimalkomma abgelehnt).
- **Bruchterme** `{z, n}` aus zwei Polynomen; `gemeinsam()` findet einen gemeinsamen Faktor (Zahl oder Nullstelle p/q),
  `rKurz()` kürzt für Musterlösungen. Gleichwertig: `z1·n2 = z2·n1`.
- **Termeingabe** `termLesen(s, namen, ziel)`: Brüche mit `/` (zusammengesetzter Nenner in Klammern, `3/2x` abgelehnt),
  mehrere Grössen für Formeln, «t =» vorne erlaubt. Formeln gleichwertig an acht Zufallsstellen (`formelGleich`).
  Formprüfungen: `einBruch` (auf einem Bruchstrich), gekürzt, gesuchte Grösse nicht rechts.
- **Lösungsmenge** `mengeLesen`: Zahl, `{5}`, `x=5`, `{}`/leer, `Q`/alle.
- **Rückmeldung:** gezielte Diagnose (Summanden gekürzt, Kehrwert, Nenner addiert, Vorzeichen, Minus vor Bruch, rechte
  Seite nicht multipliziert, Umkehrung, Reihenfolge), sonst die **Probe mit einer Zahl**: eigener Wert gegen den richtigen.
- **Sperrliste** in Normalform: Bruchterme «Zähler|Nenner» ausmultipliziert, Gleichungen «links|rechts» zusammengefasst.

## Farben — eine Farbe, eine Bedeutung

blau = Zähler, x-Glieder · orange = Nenner, Zahlen, Umformung · grün = gekürzt, Ergebnis · rot = Fehler. Bereichsfarbe Petrol.

## Prüfen

```sh
python3 scripts/lp/gleichungen-formeln/zahlen.py
python3 .claude/skills/preflight/preflight.py leitprogramme/gleichungen-formeln.html
node .claude/tools/pruef-uebungen.mjs leitprogramme/gleichungen-formeln.html 3000
node .claude/tools/pruef-formelsatz.mjs leitprogramme/gleichungen-formeln.html 60
node .claude/tools/pruef-leiste.mjs leitprogramme/gleichungen-formeln.html
node scripts/lp/gleichungen-formeln/pruef-schritte.mjs
node .claude/tools/pruef-fragen.mjs gleich-lp-kuerzen gleich-lp-kontrolle-kuerzen gleich-lp-rechnen gleich-lp-kontrolle-rechnen gleich-lp-gleichungen gleich-lp-kontrolle-gleichungen gleich-lp-formeln gleich-lp-kontrolle-formeln
node .claude/tools/render-check.mjs leitprogramme/gleichungen-formeln.html
```
