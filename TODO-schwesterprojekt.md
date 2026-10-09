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
