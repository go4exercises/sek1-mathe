# TODO — Sek1-Mathe begreifbar

Stand 09.10.2026, nach dem Aufbau des Gerüsts aus TALS Mathe.

## Veröffentlichen (einmalig)

- [ ] 🔑 DNS bei Infomaniak: CNAME `sek1-mathe` → `go4exercises.github.io.`
- [ ] 🔑 Repo `go4exercises/sek1-mathe` anlegen (öffentlich), pushen
      (`git remote add origin …`, `git push -u origin main`).
- [ ] 🔑 Settings → Pages: Branch `main`, Ordner `/ (root)`; Custom domain steht aus
      `CNAME`; nach dem Zertifikat **Enforce HTTPS**.
- [ ] 🔑 Kachel auf `begreifbar.ch` (Repo `~/begreifbar`, Block `FAECHER`) und Prosa dort
      nachziehen, die von «zwei Lehrmitteln» spricht.
- [ ] Nach dem Live-Gang: `python3 scripts/build-seo.py` ist schon gelaufen;
      `curl -sI https://sek1-mathe.begreifbar.ch/` prüfen.

## Werkzeug, das noch Grundlagen-/Schwerpunktfach kennt

Unverändert übernommen, passt erst, wenn es gebraucht wird:

- [ ] `scripts/build-clips-einbau.py` (Z. 164–166, 389, 408) und
      `scripts/clips_bibliothek.py` (Z. 107, 127) teilen nach `grundlagen`/`schwerpunkt`
      auf — auf `SITE.themen` umstellen, bevor der erste Clip eingebaut wird
      (Physik hat dieselbe Ein-Listen-Struktur: dort nachsehen).
- [ ] `HOWTO-*.md` und `STYLEGUIDE.md` sind die Fassungen aus TALS Mathe; Pfade und
      RLP-Bezüge bei Gelegenheit nachführen.
- [ ] `formelsammlung.html`: die ToC-Kurzlabels in `nav.js` erwarten Anker `lg1`–`lg3`.

## Inhalt

- [ ] 11 Themenseiten in `themen/` sind Gerüste — je nach `TEMPLATE.html` ausbauen.
      Die SEO-Beschreibungen in `scripts/build-seo.py` sind Platzhalter.
- [ ] Glossar, Formelsammlung, Clips, Leitprogramme.
- [ ] `feedback.html` sendet an dasselbe Google-Apps-Skript wie TALS Mathe — prüfen, ob
      die Rückmeldungen dort nach Site unterscheidbar sind.

## Leitprogramm Bruchrechnen (09.10.2026, unverlinkt)

`leitprogramme/bruchrechnen.html`, gebaut mit `scripts/lp/bruchrechnen/` (README dort). Steht mit
`noindex`, ohne Karte, Suchindex und Themenseiten-Kasten (HOWTO-leitprogramme §13/§15).

- [ ] Unabhängige Prüfung: `/lp-pruefung leitprogramme/bruchrechnen.html`, Befunde hierher.
- [ ] 🔑 Abnahme: Bewertungspaket mit einer absichtlich fehlerhaften Lösung einer KI geben (PDFs am 09.10.2026
      angesehen, Rastertabellen auseinandergezogen).
- [ ] 🔑 Hörprobe der acht Clips `t1-4-lp-*`, je eine Frage absichtlich falsch beantworten. Mit Whisper medium
      gegengehört: «kürzen» wird jetzt als «kührzen» gesprochen (`TAUSCH`), «Hauptnenner» gesprochen nur im Clip «Addieren und Subtrahieren»,
      Szene «Hauptnenner» (sonst «kleinster gemeinsamer Nenner»), «Nenner» nach Pausen mit «und» verbunden.
      Besonders hinhören: «Fünftel» (Whisper verstand an einer Stelle «Fünfte»).
- [ ] Bearbeitungszeit mit 2–3 Lernenden verschiedener Stärke messen (geschätzt 215 min mit Clips, BM-Vorlage §4.3).
- [ ] Themenseite 1.4 ist ein Gerüst: Notation des Leitprogramms (ggT/kgV mit Strichpunkt, Hauptnenner,
      Kehrwert, «vollständig gekürzt», keine gemischten Zahlen) dort übernehmen oder abweichend entscheiden.
- [ ] Freischalten (alle fünf Stellen nach §13), erst nach Prüfung und Abnahme.
