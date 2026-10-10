# TODO Schwesterprojekte

Änderungen am gemeinsamen Werkzeug, die auch nach TALS Mathe (oder Physik) gehören.
Je Eintrag: was, wo, warum — nachgezählt.

- [ ] **`scripts/build-clip-ton.py`, Liste `TAUSCH`:** neuer Eintrag `("kürz", "kührz")` (09.10.2026). Piper
      spricht «kürzen», «gekürzt», «kürzbar» mit unklarem ü; Whisper medium hörte «kratzen», «kerzen», «cutzen»
      (13 von 15 Stellen im LP Bruchrechnen). Mit Dehnungs-h in allen Proben richtig. Gilt für jeden Clip mit
      «kürzen» — in TALS Mathe die Clips zu Bruchtermen und Bruchgleichungen nachhören und neu vertonen.
- [ ] **`HOWTO-leitprogramme.md` §15 Prüfliste:** vier neue Punkte aus der Prüfung des LP Bruchrechnen (09.10.2026):
      Regeln nur für positive Zahlen, Zwischenergebnis macht Fehler unsichtbar, allgemeine Begründung im Raster,
      Wortanker scharf halten / Whisper medium / ß. Gelten unverändert für TALS Mathe; die Wortanker-Logik steckt dort in
      `scripts/lp/*/clips.py` (`passt`, Schwelle 0.7, kürzere Wörter erlaubt).
- [ ] **`HOWTO-leitprogramme.md` §15 Prüfliste:** vier neue Punkte aus der Prüfung des LP Terme und Faktorisieren
      (10.10.2026): Sperrschlüssel normieren und im Prüfskript dieselbe Normierung nutzen (unsortierte Paare
      sperrten nichts), Probe nicht mit 0 oder 1, gesprochene Klammerprodukte («Klammer … mal Klammer …»), Regeln nie
      ohne ihre Bedingung. In TALS Mathe die Sperrlisten der LP-Seiten (`seite.js`, Schlüssel mit Paaren) gegen
      `T.schl` nachprüfen.
- [ ] **`scripts/build-clip-ton.py`, Liste `TAUSCH`:** neuer Eintrag `("Bruchterm", "Bruch-Term")` (10.10.2026). Piper sprach
      «Bruchterm(e)» als «Bruchdämm(e)» (Whisper medium, LP Bruchterme, Gleichungen und Formeln, 6 Stellen); mit Bindestrich
      richtig. In TALS Mathe die Clips zu Bruchtermen (g1-3) nachhören und neu vertonen.
- [ ] **`HOWTO-leitprogramme.md` §15 Prüfliste:** fünf neue Punkte aus der Prüfung des LP Bruchterme, Gleichungen und Formeln
      (10.10.2026): Gleichwertigkeit an Zufallsstellen mit Mindestzahl definierter Stellen, Lösungsweg mit dem echten Faktor,
      «geht auch»-Optionen, Erkundungen über das Ergebnis statt Reihenfolge prüfen, Probe nicht an einer Nullstelle.
      In TALS Mathe die Formel-Übungen (Formeln umstellen) auf `1/0` als Eingabe prüfen.

## HOWTO §15: fünf Fehlerklassen aus der Prüfung «Lineare Funktionen» (Sek I, 10.10.2026)

Was: In `HOWTO-leitprogramme.md` §15 nach «Probe nicht an einer Nullstelle eines Faktors» fünf Punkte ergänzen
(Hilfsfunktion nur einmal definieren; Probe mit abweichendem Punkt; Sachgraphen enden bei 0; «Probe mit dem nicht
eingesetzten Punkt»; `@…@` im Clip ist Mathematik, «|» trennt Notizzeilen). Wo: ~/tals-mathe/HOWTO-leitprogramme.md §15.
Warum: Fehler, die im Sek-I-Leitprogramm auftraten und sich in TALS genauso einschleichen können. Nachgezählt: 5 Punkte.

## HOWTO §15: vier Fehlerklassen aus der Prüfung «Darstellungen wechseln» (Sek I, 10.10.2026)

Was: In `HOWTO-leitprogramme.md` §15 nach dem Punkt zu `@…@` vier Punkte ergänzen (gleiche Differenzen nur bei gleichen Schritten;
Bewegung folgt der Richtung im Ton; Zufallsübungen ohne verräterisches Muster; Sperrliste für jeden Übungstyp).
Wo: ~/tals-mathe/HOWTO-leitprogramme.md §15. Warum: in TALS ebenso möglich (Tabellenübungen, bewegte Figuren). Nachgezählt: 4 Punkte.

## HOWTO §15: neun Fehlerklassen aus «Funktionstypen und Graphen» und «Texte, Geschwindigkeit und Begegnung» (Sek I, 10.10.2026)

Was: In `HOWTO-leitprogramme.md` §15 ergänzen. Fachlich: «Ein Test an einer Stelle ist keine Regel», «Merkmale der Grundform
sagen, wofür sie gelten», «Gleiche Wörter, verschiedene Bezugsgrössen». Clips: «Vorhersagen: nichts davon in der Szene davor»,
«Zahlenfolgen im Ton eindeutig sprechen». Übungen: «Ein Hinweis in der Aufgabe darf die Antwort nicht festlegen», «Rückmeldung
nach der Wahl, nicht nach der Lösung», «Ein Zahlenfeld heisst nie `w`». PDFs: «Ein Testpunkt in der Musterlösung muss trennen».
Wo: ~/tals-mathe/HOWTO-leitprogramme.md §15 (Wortlaut wie in der Sek-I-Fassung). Warum: alle neun Fehler sind im TALS-Gerüst
genauso möglich (gleiche Übungslogik, gleiche Clip-Helfer). Nachgezählt: 9 Punkte.

## HOWTO §15: vier Fehlerklassen aus der Prüfung «Texte, Geschwindigkeit und Begegnung» (Sek I, 10.10.2026)

Was: In `HOWTO-leitprogramme.md` §15 ergänzen. Fachlich: «Eine Merkregel, mehrere Modelle», «Modellannahmen passen zu allen
Beispielen», «Sachsituationen auf Erlaubtheit prüfen». PDFs: «Jede Testaufgabe dem Kapitel zuordnen, das sie übt».
Wo: ~/tals-mathe/HOWTO-leitprogramme.md §15. Warum: Bewegungs- und Modellieraufgaben gibt es in TALS ebenso (g2-modellieren).
Nachgezählt: 4 Punkte.

## HOWTO §15: vier Fehlerklassen aus der Prüfung «Flächen, Pythagoras und Ähnlichkeit» (Sek I, 10.10.2026)

Was: In `HOWTO-leitprogramme.md` §15 nach «Sperrliste für jeden Übungstyp» vier Punkte ergänzen («Sperrschlüssel nach der Sache,
nicht nach der Fragerichtung», «Kontrollfragen nur zu dem, was der Clip gezeigt hat», «Ohne Taschenrechner braucht jede Wurzel
ein Verfahren», «Leisten-Ziele sind keine Clip- oder Kontrollbeispiele») und den Punkt «Live-Anzeigen runden nur mit ≈» um
«endliche Werte exakt (k² = 0.5625)» erweitern. Wo: ~/tals-mathe/HOWTO-leitprogramme.md §15 (Wortlaut wie in der Sek-I-Fassung).
Warum: Sperrlisten, Leisten und Kontrollclips sind im TALS-Gerüst gleich gebaut; die Wurzel-Regel betrifft TALS nur bei
Aufgaben ohne Rechner. Nachgezählt: 4 neue Punkte, 1 erweiterter.
