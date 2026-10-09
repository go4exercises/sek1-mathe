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

## Prüfung `bruchrechnen` (09.10.2026)

Drei unabhängige Prüfagenten (Seite, Clips, PDFs) nach HOWTO-leitprogramme §15, nur lesend; geprüft Stand
`ad0ab7a`. HOCH-Befunde von Hand nachgerechnet und bestätigt. Legende: **HOCH** fachlich falsch oder wertet Falsches
als richtig · **MITTEL** Logik, Bild-Ton, Prüfliste verletzt · **NIEDRIG** Kleinigkeit. Neuvertonung nötig: 🔊.

Rechenfehler: keine — alle festen Zahlen (Seite 65, Clips 55, PDFs inkl. aller Fehlerwerte) mit `fractions`
nachgerechnet. Als korrekt geprüft: Fragen aller acht Clips (`pruef-fragen`), Fragebild, Antwortdrehung, Figuren
nachgezählt, Bewegungen, Leistenziele erreichbar und nicht im Start erfüllt, Kürz-Erkennung, Punktesummen, Datenschutz.

### HOCH
- [ ] **Übung `addsub` wertet einen Fehler als richtig** (seite.js `neu`/`falsche`): «Zähler nicht erweitert» gibt bei
      2/3 − 1/2 → (2 − 1)/6 = 1/6 = richtig (1.0 % der Würfe, alle Subtraktionen). Würfe verwerfen, in denen
      `{z: x.z ± y.z, n: h}` gleich dem Ergebnis ist (§15 «Sonderwerte»).
- [ ] **Gesamttest G4 macht den gelehrten Kehrwert-Fehler unsichtbar** (gesamttest.tex, bewertungspaket.tex G4):
      9/14 · 7/12 = 3/8 ist der Divisor, falscher Kehrwert 8/3 · 3/8 = 1 = richtig. Vorschlag 9/14 · 7/12 : 3/4 = 1/2
      (falscher Kehrwert 2, vergessen 9/32).
- [ ] **Raster G4: falsche allgemeine Begründung** (bewertungspaket.tex G4): «bei Mal und Durch ändert die Reihenfolge
      das Ergebnis nicht» widerspricht Festhalten 4 und Aufgabe 4e (1 : ½ · ½ = 1 ≠ 4). Nur den Einzelfall begründen.
- [ ] 🔊 **Summenregel ohne «positiv»** (Clip `addieren` Szene «Fehler», Kontrollclip `addieren` Frage 5): «Eine Summe
      kann nicht kleiner sein als einer ihrer Summanden» — falsch für −2/5 + (−2/5) (Aufgabe 4c). Festhalten 2 sagt
      richtig «positiven». Ebenso Sim 3 Aufgabe 3 «Mal einen Bruch kleiner als 1 gibt weniger» → «… positiven Bruch …».

### MITTEL
- [ ] **Clip-Anker treffen zu früh** (clips.py `passt` ist zu grosszügig): `@quadriert` trifft «Quadrat» (Notiz «Potenz
      vor Strich» 2.8 s zu früh, Clip `reihenfolge` «Klammer beim Minus»), `@Vielfachen` trifft «Vielfache» (Vielfache
      von 18 2.6 s zu früh, Clip `addieren` «Hauptnenner» → `@Vielfachen#2`). Clip `erweitern` «Vergleichen»: «9»
      bei «acht»; «Vollständig»: Notiz «durch den ggT» vor der Zeile darüber und ungesprochen.
- [ ] **Raster G8: gleicher Fehler, andere Restpunkte**: «von links nach rechts» gibt in G6/G7 1 von 3 P, in G8 0 —
      Zeile «Kehrwert» verlangt dort zusätzlich «Punkt vor Strich». Nur den Kehrwert bewerten → 1 von 3 P.
- [ ] **Raster: Dezimalzahl/gemischte Zahl** nur im KI-Auftrag geregelt, nicht unter «Allgemein» (Selbstbewertung);
      periodische/gerundete Dezimalzahl ungeregelt. Restpunkte fehlen bei G7 «nur Zähler quadriert» (1 von 3 P) und G9
      «Fehler bei 1/3 + 1/6 gesucht» (2 von 3 P). «Kehrwert vom falschen Bruch» in G7/G8 ungeregelt.
- [ ] **Wiederholungen (§9/§15)**: Kapitelaufgabe 2a = Clip/Festhalten 3/8 + 1/8; 2f nimmt 1/2 + 1/3 und 1/6 + 2/6;
      3e = Clip-Produkt 3/4 · 2/3; 4d und 4f prüfen denselben Gegensatz, 4f mit der Festhalten-Basis 2/3 (auch in
      Sim 4); Kontrollclip `malnehmen` Frage 1 = Aufgabe 3f (2/5 · 3/4); Kontrollclip `erweitern` Frage 3 = Vortest
      0a (ggT 18; 24). Gesamttest: G1(b) mit 6/15 wie 1b, G3 Typ von 1c, G6 Struktur des Festhalten-Beispiels, G7
      beginnt wie 4f mit (−2/3)².
- [ ] **Nicht eingeführt, aber verlangt**: a − (−b) (Sim 4 Aufgabe 5, 21.5 % der Übung `vorzeichen`) → Zeile im
      Festhalten 4 und Vortest-Aufgabe 3 − (−7); Division durch ganze Zahl (3b, 30 % von `durch`) → Zeile «Kehrwert
      von 7 ist 1/7»; drei Brüche (G2) nur in Kapitel 4 geübt; Sachaufgabe (G5) nirgends geübt; Kapitelziel 3
      «erklärst am Bild» im Gesamttest nicht geprüft.
- [ ] **Sim 4 Schrittwähler**: Diagnose «Reihenfolge» unerreichbar (vorher abgefangen); bei −3/4 − (−1/4) = −1 kommt
      «Gleichnamig machen» → «Minus einer negativen Zahl heisst plus».
- [ ] **Übung `reihenfolge`**: Hauptnenner in Zwischenschritten bis 130 (3.3 % über 48) → kgV je Schritt ≤ 48.
      Lösungswege von `reihenfolge` und `vorzeichen` nicht kleinschrittig (Gleichnamig/Kehrwert fehlen).
- [ ] **Sperrliste**: `dv|2/3|-4/9` sperrt nichts (G8-Schritt kommt als `vz|2/3:-4/9`); es fehlen `er|3/4|16` (1f),
      Teilschritte von 1c, 2a, 4a, 4b, G2, G3, G6, G9; `vz`-Produkte nicht sortiert.
- [ ] 🔊 **Clip `reihenfolge` «Klammer beim Minus»**: «Ohne Klammer wird zuerst quadriert», im Bild steht −(1/2)² mit
      Klammer → «Steht das Minus vor der Klammer …». «Beispiel»: Zwischenschritt 2/6 fehlt (auch Festhalten 4).
- [ ] **Verweise auf leere Themenseiten** (Vortest-Empfehlung, «Mehr dazu»): vor der Freischaltung lösen.

### NIEDRIG
- [ ] Kontrollclip `erweitern` Frage 1: Klicktoleranz 0.5 bei Streifenhöhe 1.2 → 0.7.
- [ ] Kontrollclip `malnehmen` Frage 2: nur die richtige Option trägt ein Ergebnis («= 1/4») → alle mit oder ohne.
- [ ] Kontrollclip `reihenfolge` Frage 2: Rückmeldung zu 1/9 trifft den Fehler nur halb.
- [ ] Farbbedeutung blau/orange in «Vorher kürzen» (Kürzpaar), Kontrollclip `addieren` Frage 2 und Clip `reihenfolge`
      (aktueller Schritt) anders als «erster/zweiter Bruch» → in README dokumentieren oder angleichen.
- [ ] Sprechertexte mit «wir» (HOWTO §10: Du-Form). Clip `addieren` «Hauptnenner»: «Die Vielfachen von achtzehn sind
      achtzehn und sechsunddreissig» klingt abschliessend.
- [ ] Seite: Kapitel 4 mit 50 min über dem Kapitelmuster; `addsub`-Meldung «plus» auch bei Subtraktion; Tipp
      `hauptnenner` zeigt nur 5 Vielfache (5.7 % ohne Antwort); Lösung `mal` kürzt nachher statt vorher; «über Kreuz» in
      zwei Bedeutungen; 3.0 als Eingabe → «als ganze Zahl»; Vortest 0d (0.75 als Bruch) gegen Kompetenzbox; Sim 2
      Reglerfarbe grün; Formulierung 3e «weniger als das Ganze, 1/2».
- [ ] PDFs: in Rasterzellen berühren umbrochene \dfrac-Zeilen einander (G3, G5) → \tfrac oder Zeilenabstand;
      G5-Brüche im Testblatt klein; G9 allein auf Seite 4; (E) «Weg erkennbar» bei G1(a), G5(b); Bewertungspaket
      ohne Aufgabenstellungen (Testblatt mit hochladen); Teil C 12 von 24 P lenkt die Selbsteinschätzung auf Kapitel 4.
