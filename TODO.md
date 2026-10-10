## Abgleich mit TALS Mathe (10.10.2026)

Gemeinsame Dateien gegen ~/tals-mathe verglichen (TALS-`scripts/abgleich.py` passt nicht auf Sek1: erwartet Physik-Dateien).
Gleich: mathlib.js, minicheck.js, anim-hinweise.js, suche.js, build-clips.py, build-clip-fragen-ton.py, build-lp-pdf.py, alle
.claude/tools ausser build-bilder.mjs. Projekteigen: style.css (Petrol), build-bilder.mjs, build-seo.py, build-suchindex.py, preflight.py.
- [x] `build-clip-ton.py`: neue `TAUSCH`-Einträge aus der TALS-Hörprobe vom 10.10.2026 übernommen (eigene «kürz», «Bruchterm» bleiben).
- [x] Davon betroffen: «Kacheln» in `terme-lp-zusammenfassen`, Szenen 2, 4, 5 neu vertont.
- [x] Hörprobe 10.10.2026 umgesetzt (`~/hoerproben/2026-10-10/AUFTRAG-sek1.md`): Tabelle gleich wie TALS, Kommentarzeile repariert;
      «Kacheln» mit langem ch (terme-lp-zusammenfassen, Sz. 2, 4, 5), «y» → «Ypsilon» in den Terme-Clips (9 Stellen, Regel `ypsilon()`
      in `scripts/lp/terme-faktorisieren/clips.py`, «y-Glieder» bleibt), «Nun stelle …» in den Fragetönen 1–4 von gleich-lp-kontrolle-formeln.
      Whisper medium schreibt «Ypsilon» weiterhin als «Epsilon» und «Kacheln» einmal als «Karre» — massgebend ist die Hörprobe.

## Leitprogramm Abbildungen und Geraden im Koordinatensystem (10.10.2026)

`leitprogramme/koordinaten.html`, gebaut mit `scripts/lp/koordinaten/` (README dort), nach
`~/TODO-BM-Vorkurs-LP03-15.md` §7 (LP 09, Koordinatengeometrie: Abbildungen und Geraden). Bereich «Geometrie».

- [x] Unabhängige Prüfung: `/lp-pruefung leitprogramme/koordinaten.html` (Abschnitt unten).
- [x] Freigeschaltet (nav.js, index.html Bereich «Geometrie», build-seo, Suchindex, Sitemap); alle Befunde der Prüfung behoben.
- [ ] 🔑 Abnahme: Bewertungspaket mit einer absichtlich fehlerhaften Lösung einer KI geben (G1 mit P + Z, G5 vom Ursprung aus gestreckt).
- [ ] 🔑 Hörprobe der acht Clips `koo-lp-*`, je eine Frage absichtlich falsch beantworten. Besonders hinhören:
      «P Strich», «x gleich zwei», «Ursprung», «hunderteins» und «zweihunderteins» (Whisper schreibt Ziffern).
- [ ] Bearbeitungszeit mit 2–3 Lernenden messen (geschätzt 200 min).

## Prüfung `koordinaten` (10.10.2026)

Drei unabhängige Prüfagenten (Seite, Clips, PDFs) nach HOWTO §15, nur lesend; geprüft Stand `c7e4290`. HOCH-Befunde
an der Quelle nachgeprüft und bestätigt. Rechenfehler: keine (alle Zahlen nachgerechnet). Neuvertonung nötig: 🔊.
**Behoben am 10.10.2026** (alles ausser der Hörprobe): G8 mit y = −2x + 7, G3c an der schrägen Achse y = −x + 2 konstruiert,
G2b und G5 neu, G6 in Häuschen, A' orange, Raster mit «Ergebnis genügt» und halbem Rechteck; 2c schräge Achse mit Gitter, 3a und 4a
mit Zeichnung, 4a/4b/4d neu; Festhalten mit «Achse gesucht», k > 0 und 0 < k < 1, Flächenregel mit Bedingung, x_A ≠ x_B, Merksatz
waagrecht/senkrecht, Regel «P + Z» mit Bedingung; Vorwissen mit Rechteck und Steigung; neue Clipszenen «Mitte», «Gesucht», «Faktor»,
Fragebild K2F5 mit P(2 | 5), Fehlerbild im grösseren Fenster, Randdreiecke grau mit Massen, B blau, «P Strich» und «Achsenabschnitt b»
im Ton, Text = Ton; `gerade2` prüft zuerst m, Sonderwerte ausgeschlossen, `achsbild` erkennt «an der Koordinatenachse», Lösungswege mit
Schritten, Sperrschlüssel ohne Fragerichtung, Sim 4 b exakt, Bild ausserhalb mit Hinweis. Neu vertont: drei Einführungsclips ganz,
vier Szenen, alle Fragetöne. Nicht geändert: Sim 3 Leiste 3 (Fläche 9-mal, die Live-Zeile zeigt k² als Rückmeldung), Raten bei
`punktprobe`, Zeit des Gesamttests (Messung mit Lernenden offen), Leerraum im PDF.
Als korrekt geprüft: alle Zahlen und Fehlerwerte, Punktsummen, Leisten auf dem Reglerraster, Fragebilder (ausser zwei), Datenschutz.

### HOCH
- [x] Gesamttest: G8 nennt «y = 3x − 2», die Lösung von G7; ebenso 4b die Lösung von 4a (und Vortest 0d dieselbe Gerade).
- [x] Kontrollclip Achsenspiegelung F5: P(2 | 7) bei y = 6.4 gezeichnet, Achse y = 3 sichtbar nicht in der Mitte. 🔊
- [x] Festhalten 1: «P + Z oder Z − P ist nicht das Bild» ohne Bedingung (am Ursprung ist Z − P das Bild).
- [x] Übung `gerade2`: bei m = ±1 meldet «m richtig, b falsch» «Bruch auf dem Kopf» (27 % der Würfe).

### MITTEL
- [x] «Schräge Achse konstruieren» in Ziel und Kompetenz, nur im Clip gezeigt, nie geübt oder geprüft.
- [x] «Achse aus Punkt und Bild», «k aus P und P'», «Zentrum als Mittelpunkt» fehlen in Festhalten bzw. Einführungsclip, gefragt
      in Kontrollclips, Übung und G4. 🔊
- [x] Fläche aus Koordinaten: Randdreiecke im Clip ohne Masse und Einzelflächen, orange (= Bild); Regel ohne Bedingung «jede Ecke
      auf dem Rand»; Rückmeldung «ein Dreieck ist halb so gross» (G6 halbes Rechteck 24 ungeregelt).
- [x] Wiederholungen: G3c = Sim 2 Leiste 4, G5 = Sim 3 Leiste 2, G2b nah an Festhalten 1, 4d = Vortest 0e; Sperrliste mit Lücken
      und falschem Schlüssel `zt|-5|0|-1|2`.
- [x] Sim 4 zeigt b gerundet ohne ≈ (1/3 · x − 0.33); «parallel» nicht eingeführt (Sim 4 Leiste 3).
- [x] Sonderwerte machen Fehler unsichtbar (`zentrum`/`punktbild` mit Z = (0 | 0), `achsbild` an y = x mit py = −px); `achsbild`
      an x = a erkennt «an der Koordinatenachse gespiegelt» nicht; Lösungswege ohne Schritte (`koordflaeche`, `gerade2`).
- [x] Fragen ohne `sprich`: «P im Bild» statt «P Strich» (Kontrolle Punktspiegelung F3, Achsenspiegelung F5). 🔊
- [x] Kapitel 3 und 4 ohne Aufgabe am Gitter, G5b verlangt Zeichnen; k zwischen 0 und 1 nie erklärt; Vorhersage Streckung abzählbar. 🔊

### NIEDRIG
- [x] «x−Achse» mit Rechenminus in `achsbild`; Tipp «(−3) nach rechts»; «Gerade x = 5» (Geraden); Bild ausserhalb ohne Hinweis
      (Sim 2, Sim 3); Sim 4 Leiste 4 Wortlaut; Sim 3 Leiste 3 ablesbar; Merksatz «was parallel zur Achse läuft»; k > 0, xA ≠ xB.
- [x] Clips: Text ≠ Ton in zwei Rückmeldungen; «viermal: k Quadrat», «minus zwei. x bleibt», «null und eins und zwei und sieben»,
      Parameter b = Punkt B im Ton; Formel/P' zu spät (Vorhersage Punktspiegelung, Diagonale); lange Stille am Szenenende;
      (7 | 4) am Rand; Rückmeldungen mit ganzer Rechnung. 🔊
- [x] PDFs: G6 «Einheit cm» bei 6-mm-Karo; A' in G4 blau; G3 «Ergebnis genügt»; Leerraum; Zeilen G1.
- [ ] 🔑 Hörprobe (Whisper-Vermutungen): «Längen» («Lenin»), «ändert» («endet»).

## Leitprogramm Flächen, Pythagoras und Ähnlichkeit (10.10.2026)

`leitprogramme/pythagoras.html`, gebaut mit `scripts/lp/pythagoras/` (README dort), nach
`~/TODO-BM-Vorkurs-LP03-15.md` §6 (LP 08, Ebene Geometrie: Flächen, Pythagoras, Ähnlichkeit). Neuer Bereich «Geometrie».

- [x] Unabhängige Prüfung: `/lp-pruefung leitprogramme/pythagoras.html` (Abschnitt unten).
- [x] Freigeschaltet (nav.js mit Bereich 5 «Geometrie», index.html, build-seo, Suchindex, Sitemap); alle Befunde der Prüfung behoben.
- [ ] 🔑 Abnahme: Bewertungspaket mit einer absichtlich fehlerhaften Lösung einer KI geben (G1 mit schräger Seite als Höhe, G7 mit k statt k²).
- [ ] 🔑 Hörprobe der acht Clips `pyt-lp-*`, je eine Frage absichtlich falsch beantworten. Besonders hinhören:
      «subtrahierst» (Whisper: «verbreihe»), «gleichschenkliges» (Whisper: «gleischinkliges»), «Hypotenuse», «Katheten», «Quadrat»;
      neu vertont: «in den Ecken» (Whisper: «Etten»), «je sechs Kästchen» (Whisper: «Hier 6»), «Flächenfaktor gleich Längenfaktor»
      (Whisper: «Gleichlängenfaktor»), «sechsundfünfzig Komma zwei fünf» (Kontrollfragen mit halben Zahlen).
- [ ] Bearbeitungszeit mit 2–3 Lernenden messen (geschätzt 200 min).

## Prüfung `pythagoras` (10.10.2026)

Drei unabhängige Prüfagenten (Seite, Clips, PDFs) nach HOWTO §15, nur lesend; geprüft Stand `43d8490`. HOCH-Befunde
an der Quelle nachgeprüft und bestätigt. Rechenfehler: ein Ablenker (22.6 statt 22.7). Neuvertonung nötig: 🔊.
**Behoben am 10.10.2026** (alles ausser der Hörprobe): Vorwissen mit Quadraten bis 30² und Dezimalquadraten; Wurzel eingrenzen
(Festhalten 2, Clip hilfsdreieck) und halbe Zahlen (7.5² = 7 · 8 + 0.25); Zufallsübungen nur mit Seiten ganz bis 30, halb bis 15 oder
einer Dezimale bis 3, Leitern steil (67° bis 80°), Sperrschlüssel nach dem Dreieck über alle Typen, Sehne ohne Fragerichtung, ähnlich
nach k; Clip flaechen mit Trapez-Szene (Diagonale zerlegt), Parallelogramm abschneiden und ansetzen, Höhe auf der Verlängerung;
Clip pythagoras mit schrägem Quadrat (7 × 7 minus vier Dreiecke) und Umkehrung; Kontrollfragen neu (7.5/6, 7-24-26 nein, 12.5/12,
Rechteck 7.5 × 4, r 2.5/1.5, Rohr r 6.5), Fragebild K3F4 neutral; Diagonale heisst e; Hilfsdreieck überall orange; Rohr-Breite
angeschrieben; Ähnlichkeit mit rechten Winkeln und Begründung beim Schatten; Regal «sechzig mal vierzig durch zwei»; Sim 4 exakt
(k² = 0.5625), Sim 1 Parallelogramm im Bild, Leisten mit eigenen Zielen (Sim 1 g 7, Sim 2 c² = 200, Sim 3 r 15/24 und Rohr r 5,
Sim 4 13.5 cm², k 2.25, 3.75 cm); Festhalten 4 mit «ähnlich erkennen», Strahlensatz begründet, 4f «ähnlich oder nicht?»,
3b/3e mit Skizze, 3f neu; Gesamttest neu (Trapez-Grundstück, Grundseite aus Fläche, 18-24-30 und 8-15-18, Hypotenuse erkennen,
Basis 30/Schenkel 39, Rohr 10 cm tief, Eckregal 90/60, Schatten 1.2/0.8), Raster mit Ansatzzeilen und gleichwertigen Wegen.
Neu vertont: Clip flaechen ganz, 15 Szenen in vier weiteren Clips, Fragetöne.
Als korrekt geprüft: alle übrigen Zahlen, Figurenkoordinaten, rechte Winkel, Leisten, Fragebilder (ausser einem), Datenschutz.

### HOCH
- [x] Grosse Wurzeln ohne Verfahren: Übungen bis √3422, Clip √841, √1369, G3 √1156; Vorwissen nur bis 15². Eingrenzen zeigen,
      Übungen auf kleinere Tripel begrenzen, Quadrate bis 30² und 1.4² ins Vorwissen.
- [x] Kontrollfragen fragen, was erst das Festhalten bringt: Trapez (K1F3), Umkehrung des Pythagoras (K2F4). 🔊
- [x] Gesamttest: G4 (Leiter) im Teil von Kapitel 2, geübt in Kapitel 3; Strahlensatz, fehlende Längen, Diagonale ungeprüft;
      fast jede Aufgabe wiederholt ein Modell (Haus, 21-20-29, 9-12-15, Regal, Lea k statt k²); G6-Raster widersprüchlich.
- [x] Sim 4 Live-Zeile rundet ohne ≈ (k² = 0.56 statt 0.5625); Sim 1 Parallelogramm ragt aus dem Bild.
- [x] Clip Parallelogramm zeigt kein Rechteck (Teil nicht abgeschnitten); Regal «sechzig mal vierzig, also zwölfhundert» klingt
      wie 60 · 40 = 1200; Formel in der Kreisszene 8 s zu früh; Ablenker 22.6 statt 22.7. 🔊

### MITTEL
- [x] Wiederholungen: Leisten-Ziele = Clip-Beispiele (Sim 4 k = 2/24, «9-mal», Sim 1 6/4, Sim 2 20-21-29); Kontrollfragen = Leisten
      (Sim 3 r 10/8, r 13/12, Sim 2 8-15-17, K2F5 6-8-10); 3f = 6-8-10; Sperrliste mit falschem ae-Schlüssel und ohne Gegenrichtung.
- [x] «Ähnlich erkennen» und Strahlensatz versprochen, nie geübt; Begründung der Ähnlichkeit beim Schatten fehlt.
- [x] Skizzen im Test verlangt, auf der Seite nie geübt; G6 massstäblich ausmessbar; G7-Figur mit mehrdeutigen Massen; G8 unrealistisch.
- [x] K3F4: grüne Farbe verrät die Hypotenuse; Quadrat über c lässt sich nicht «abzählen»; Scheren ohne Höhe auf der Verlängerung.
- [x] Leitern zu flach (3-4-5); Rückmeldungen sehne/kathete unterstellen einen Fehler.

### NIEDRIG
- [x] Umfang «zweimal Länge plus Breite» mehrdeutig; «Flächen wachsen mit k²» bei k < 1; Regal «60 × 40» ohne Einheit;
      Sim 3 d > r ohne Hinweis; Minus als Bindestrich am Regler; Beschriftungen überlappen (Sim 1, Sim 2 bei a = 1, Sim 4 bei k = 0.5,
      FIG 1, FIG 3); «Basis/Schenkel» nicht eingeführt; «Aussagen aus einer Liste» ohne Auswahlübung; Sperrlücken.
- [x] Clips: Merkbilder mit «·» als Trenner; Hilfsdreieck mal orange, mal grün; Hypotenuse 17 unbeschriftet; Rohr-Breite nicht angeschrieben;
      d doppelt belegt; Ähnlichkeit ohne Winkelzeichen; «immer» gegen «oft» die Hälfte.
- [ ] 🔑 Hörprobe (Whisper-Vermutungen): «subtrahierst», «addierst», «Spitze», «Flächenfaktor», «Hilfsdreiecks», «unter dem Clip».

## Leitprogramm Texte, Geschwindigkeit und Begegnung (10.10.2026)

`leitprogramme/bewegung.html`, gebaut mit `scripts/lp/bewegung/` (README dort), nach
`~/TODO-BM-Vorkurs-LP03-15.md` §5 (LP 07, Mathematisieren: Texte, Geschwindigkeit und Begegnung). Neuer Bereich «Mathematisieren».

- [x] Unabhängige Prüfung: `/lp-pruefung leitprogramme/bewegung.html` (Abschnitt unten).
- [x] Freigeschaltet (nav.js mit Bereich 4 «Mathematisieren», index.html, build-seo, Suchindex, Sitemap, CLAUDE.md).
- [ ] 🔑 Abnahme: Bewertungspaket mit einer absichtlich fehlerhaften Lösung einer KI geben (G1 ohne Antwortsatz, G5 mit Mittelwert).
- [x] 🔑 Hörprobe Runde 7: «Bea» als BE-a (Lautschrift über `bea()` in `scripts/lp/bewegung/clips.py`, nur das ganze Wort;
      3 Szenen und die Fragetöne neu vertont, Whisper hört weiter «wir», «Beher»); «addierst», «Rappen», «Durchschnitt»,
      «Teilen statt mal», «neun Zahlungen» und die drei Fragetöne bleiben wie bisher.
- [ ] 🔑 Ganze Clips `bew-lp-*` anhören, je eine Frage absichtlich falsch beantworten.
- [ ] Bearbeitungszeit mit 2–3 Lernenden messen (geschätzt 200 min).

## Prüfung `bewegung` (10.10.2026)

Drei unabhängige Prüfagenten (Seite, Clips, PDFs) nach HOWTO §15, nur lesend; geprüft Stand `8aa214a`. HOCH-Befunde
an der Quelle nachgeprüft und bestätigt. Rechenfehler: keine. Neuvertonung nötig: 🔊.
**Behoben am 10.10.2026** (alles ausser der Hörprobe): Rolltreppe nur noch in Fahrrichtung und stehend, als Geschwindigkeit
gegenüber dem Boden abgegrenzt (Kontrollfrage: Rollband); Modell «Start zur angegebenen Zeit», Einholregel mit Bedingung,
Annäherungsgeschwindigkeit definiert; Gesamttest mit Graph (G6), Einholen (G8), neuen Zahlen in G1/G5/G7, Plausibilität in G4,
Raster mit Antwortsatz-Regel und getrennten Pause-Fällen; geübt jetzt auch gerade/ungerade Zahlen (1b, `raetsel`), Modellannahmen (4f),
Graph (3f); Sim 4 zeigt den Abstand über die ganze Zeit; Wiederholungen ersetzt, Sperrliste mit Rollentausch; Rückmeldungen ohne
Rechenweg, Text = Ton; 17 Szenen neu vertont.
Als korrekt geprüft: alle Zahlen und Fehlerwerte, Punktsummen, Leisten auf dem Reglerraster, Fragebilder ohne Antwort, Datenschutz.

### HOCH
- [x] Rolltreppe widerspricht der Merkregel «aufeinander zu addieren, gleiche Richtung subtrahieren» (Clip begegnung, K4F5):
      Geschwindigkeiten setzen sich gegenüber dem Boden zusammen; «gegen die Fahrrichtung» ist auf Rolltreppen verboten (G8, Festhalten). 🔊
- [x] Modell «gleichzeitiger Start» widerspricht dem Einholen-Beispiel (Festhalten 4, Clip Modell); Einholregel ohne Bedingung
      (Hinterer schneller), v₁, v₂ undefiniert, «Treffpunkt in der Mitte» ohne «gleichzeitig». 🔊
- [x] Gesamttest: G6 (Plausibilität) im Teil Abschnitte; Einholen fehlt; G2 «gerade Zahlen» und G7c «Modellannahme» nirgends geübt;
      G5 = Velotour aus Clip und Festhalten (gleiche Zeiten), G7 mit Zahlen aus dem Clip, G1 mit Lösung 6/7 wie 1a und K1F2.
- [x] Sim 4 nach der Begegnung: Punkt neben dem Graphen, Fahrzeuge ausserhalb; Sim 2 Live-Zeile rundet mit «=».

### MITTEL
- [x] Raster: Pause-Fehler G5 doppelt abgezogen; Antwortsatz und Einheiten nur in G1 geregelt; G6(a) «ohne Rechnen» rechnet;
      Probe mit x = 6 oder 7; Tabelle statt Gleichung; G3(b) Weg über Minuten; Folgepunkt mit unplausiblem Treffpunkt.
- [x] Wiederholungen: 1d (= Festhalten 10.8 Busse), 2d (= Festhalten 1.30 h), 4e (= Sim 4), K4F4/F5 (= 4b/4c), K2F1/F3, K1F4;
      Sperrliste lässt Festhalten- und Clipbeispiele durch (falscher Schlüssel sv|s|240|120, keine Rollentausch-Normierung).
- [x] Keine Aufgabe am Graphen (Diagrammsteigung nur in K3F5); «gegeben, gesucht» nicht umgesetzt; «Annäherungsgeschwindigkeit» nie erklärt.
- [x] Plausibilitätsregel «Zug 100 km/h und mehr» widerspricht 2a (60 km/h); Velo mit 45 km/h in Sim 2; Vortest 0b/0c = «Kurz wiederholt».
- [x] Zufallsübungen: Velo- und Autotempo gemischt (durchschnitt), Tom «fährt» 4 km/h, Velomiete bis 20 h, Jahreskarte 5 Fr.;
      Rückmeldungen begegnung/einholen nennen die Rechnung.
- [x] Clips: Abschnitte «erster steiler als dritter» bei Tabelle 1 | Pause | 2; Ton «nur null Komma fünf: sechzig Sekunden»,
      «Abschnitt eins nur dreissig» mehrdeutig; Rückmeldungen nennen den Rechenweg; Text ≠ Ton bei mehreren Rückmeldungen;
      K1F3 und K2F3 vor dem Festhalten nicht eingeführt; Einholzeit ohne Bezug («nach Annas Start»). 🔊

### NIEDRIG
- [x] Dativ «Eintritte/Plakate», «Setz die Kosten Gleichung», Franken mit zwei Stellen, Warn-Titel «Komma statt Bruch»,
      Sim-4-Graph blau, «noch 6 km» auch nach dem Treffen, «0.5 h später».
- [x] Clips: «Viertelauto», Doppelpunkt «x = 11:», Einblendezeiten Bea und «= 2 h», Label (1.5 | 21) weit unter dem Punkt,
      K3F5 Abschnitt 2 nicht orange, «darf man».
- [x] PDFs: Schreibplatz G1/G5/G7, Silbentrennung in der Kopfzeile, leere Flächen im Bewertungspaket.
- [x] 🔑 Hörprobe (Whisper-Vermutungen): erledigt in Runde 7, siehe oben.

## Leitprogramm Funktionstypen und Graphen (10.10.2026)

`leitprogramme/funktionstypen.html`, gebaut mit `scripts/lp/funktionstypen/` (README dort), nach
`~/TODO-BM-Vorkurs-LP03-15.md` §4 (LP 06, Funktionstypen und Graphen interpretieren).

- [x] Unabhängige Prüfung: `/lp-pruefung leitprogramme/funktionstypen.html` (Abschnitt unten).
- [x] Freigeschaltet (nav.js, index.html Bereich «Funktionen», build-seo, Suchindex, Sitemap).
- [ ] 🔑 Abnahme: Bewertungspaket mit einer absichtlich fehlerhaften Lösung einer KI geben (mit Graph G6 und Skizze G8).
- [x] 🔑 Hörprobe Runde 7 (`~/hoerproben/2026-10-10/runde7/`): «null, null» → «durch den Nullpunkt» / «im Nullpunkt»
      (7 Stellen, 7 Szenen neu vertont); «y», «Grundtaxe», «Kehrwertgraph», «hundertzwanzig», «liefe» bleiben wie bisher.
- [ ] 🔑 Ganze Clips `typ-lp-*` anhören, je eine Frage absichtlich falsch beantworten.
- [ ] Bearbeitungszeit mit 2–3 Lernenden messen (geschätzt 200 min).

## Prüfung `funktionstypen` (10.10.2026)

Drei unabhängige Prüfagenten (Seite, Clips, PDFs) nach HOWTO §15, nur lesend; geprüft Stand `5baa2b8`. HOCH-Befunde
an der Quelle nachgeprüft und bestätigt. Rechenfehler: keine (alle Zahlen nachgerechnet). Neuvertonung nötig: 🔊.
**Behoben am 10.10.2026** (alles ausser der Hörprobe): Doppelt-Test mit Bedingung «überall, Form zuerst» (Clip, Festhalten,
Sim 2 nur b ≥ 0), Bezug «von zu Hause / zum Ziel», «nimmt nie ab», Vorhersagen ohne sichtbare Antwort (Punkte (9 | 3), (16 | 4);
Geraden bis t = 0.5), Raster G1 mit trennenden Testpunkten und Restpunkten überall, G4/G5/G3(b) neu, G2 mit Gitter, G8 mit
Skizzenfeld, `kritik` mit beiden Achsnamen in allen Fällen und Rückmeldung nach Wahl, `situation` nach Wahl und mit neuen Kontexten,
1a/1d (Kehrwert skizzieren)/1e/1f/3e/3f (Text → Graph, Hin- gegen Rücktempo)/4d/4f neu, Sim 4 Aufgaben 1 und 3 neu, Kontrollfragen
familien F1/F5, zusammenhaenge F5, rest F3/F4 neu, Pizza als Punkte, Achsen mit Grösse, Sperrliste ergänzt, Wanderung statt
Velo bei v ≤ 6. 13 Szenen neu vertont. Nicht geändert: Kapitelziel 2 «an Text, Tabelle, Gleichung und Graph» (auf der Seite
geübt, im Test nur teilweise), Zeiten je Kapitel (Messung mit Lernenden offen).
Als korrekt geprüft: alle Zahlen, Punktsummen, Leisten auf dem Reglerraster, Zufallsübungen lösbar, Fragebilder, Datenschutz.

### HOCH
- [x] Doppelt-Test ohne Bedingung (Clip zusammenhaenge «Test», kontrolle-zusammenhaenge Merke, Festhalten 2, Sim 2 mit b < 0):
      fallende Gerade kann beim Verdoppeln halbieren (y = −x + 6, x = 2 → 4). Bedingung «immer, an mehreren Stellen» und Form zuerst. 🔊
- [x] Festhalten 4: «fallender Graph der Entfernung zeigt Zurückfahren» widerspricht d = 24 − 16t: «von zu Hause» ergänzen.
- [x] kontrolle-rest Merke «zurückgelegt wächst immer» falsch (Pause): «nimmt nie ab». 🔊
- [x] Vorhersagen mit sichtbarer Antwort: rest (Schnittpunkt 0.75 im Bild), familien ((4 | 2) schon in der Wurzel-Szene). 🔊
- [x] Bewertungspaket G1: Testpunkt (2 | 2) trennt B und C nicht; G7 Folgepunkt-Regel widersprüchlich.
- [x] Übung `kritik`: Achsenname verrät die Antwort, Rückmeldung «ok» nennt die Lösung; `situation`: Rückmeldung nach Lösung statt Wahl.

### MITTEL
- [x] Wiederholungen (HOWTO §9): 1a, 1d, 1e, 1f, 3e, 4d; Sim 4 Aufgabe 1 (= Clip rest); kontrolle-familien F1/F5, kontrolle-zusammenhaenge F5,
      kontrolle-rest F3/F4; G4 (= 2c, Produkt 60), G5 (= Anna), G3(b) (= Übung situation k = 120); `situation` mit Kontexten des Kontrollclips.
- [x] Merkmale der Familien gelten nur ohne +b (Sim 1 erlaubt b); «nach oben» auch bei b < 0; Sim 1 bei a = 0.
- [x] s in Kapitel 3 Entfernung von zu Hause, in Kapitel 4 zurückgelegter Weg: Achsen nach der Grösse benennen; Minus-Geschwindigkeit in Sim 3 erklären.
- [x] K3 «Graph zu einer Beschreibung» nur in Gegenrichtung geübt; Hin- gegen Rücktempo nie verglichen (G6).
- [x] Kehrwertgraph wird nie skizziert (G2 verlangt es); G2 ohne Gitter, G8 ohne Platz für die Skizze.
- [x] Buchstaben a, k, m für die Steigung gemischt.
- [x] Raster: «Typische Fehler» ohne Restpunkte bei G2–G8; (E) uneinheitlich; Kommalisten wie Dezimalkomma.
- [x] Clip-Ton: «für null Komma fünf zwei» mehrdeutig (familien Kehrwert); «Steigt er, geht es nicht bergauf» (wegzeit Fehler). 🔊

### NIEDRIG
- [x] Pizza als durchgezogene Kurve (Personen ganzzahlig); Endpunkt (5 | 500) in kontrolle-wegzeit F1 unbeschriftet; Benzin/Taxi x ohne Einheit;
      −x² orange; Achsnamen überlagert (Kehrwert, wegzeit Zurück); Punkte im Fehlerbild nicht markiert; «Steigung = Geschwindigkeit» → «Steilheit».
- [x] Sperrliste unvollständig (zu|g|1|0, we|q|0.5|±2, we|k|12|…); Velo mit 4 km/h in `restweg`; Tipp `neuwert` mit 10 : 3.
- [x] Rückmeldung kontrolle-zusammenhaenge F4 «nicht darunter»; kontrolle-rest F1 «Kilometer» fehlt im Ton; Fragepunkte «vier, zwei und neun, drei».
- [x] G6 «gleiches Tempo» → «gleichbleibendes»; G6-Buchstabe auf Graph C; KI-Auftrag «Fotos» → «Bilder»; G7 ohne Bereich; 2f ohne Kontext.
- [x] 🔑 Hörprobe (Vermutung Whisper): erledigt in Runde 7, siehe oben.

## Leitprogramm Darstellungen wechseln (10.10.2026)

`leitprogramme/darstellungen.html`, gebaut mit `scripts/lp/darstellungen/` (README dort), nach
`~/TODO-BM-Vorkurs-LP03-15.md` §3 (LP 05, Lineare Funktionen II: Darstellungswechsel).

- [x] Unabhängige Prüfung: `/lp-pruefung leitprogramme/darstellungen.html` (Abschnitt unten, behoben).
- [x] Freigeschaltet (nav.js, index.html Bereich «Funktionen», build-seo, Suchindex, Sitemap).
- [ ] 🔑 Abnahme: Bewertungspaket mit einer absichtlich fehlerhaften Lösung einer KI geben (mit Zeichnung G5).
- [ ] 🔑 Hörprobe der acht Clips `dar-lp-*`, je eine Frage absichtlich falsch beantworten. Besonders hinhören:
      «Geraden» (Whisper: «Graden»), «geknickt» (Whisper: «geknippt»), «y» als «Ypsilon», «antiproportional».
- [ ] Bearbeitungszeit mit 2–3 Lernenden messen (geschätzt 200 min).

## Prüfung `darstellungen` (10.10.2026)

Drei unabhängige Prüfagenten (Seite, Clips, PDFs) nach HOWTO §15, nur lesend; geprüft Stand `739cec9`. HOCH-Befunde
an der Quelle nachgeprüft und bestätigt. Legende wie oben; Neuvertonung nötig: 🔊.

**Behoben am 10.10.2026** (alles ausser der Hörprobe): Regeln mit Bedingung (gleiche Schritte, c ≠ 0, «verlängert»), Rechteck-Bewegung
im Clip summe und Strecke statt Gerade, Vorhersage Velo ohne Lösung im Bild, Raster G1/G3/G5 eindeutig, G6 mit eigener Skala, G8 mit
Umfang 28, G1(b) mit Tabelle, «bereich» mit steigender Variante (Becken bis voll) und Sim 3 mit Regenfass, «art» ohne Muster und mit
Richtungsdiagnose, Sperrliste für alle Typen, 1c als Sachgraph ab 0 mit Einheiten, 1e/2e/3a/4e neu (Division durch 2.5, Steigung −1.5
deuten, Treppe selbst umformen), «aufloesen» auch mit b = 7.5, Kontrollclip Kapitel 4 F1/F3/F4 neu, Rückmeldungen ohne Lösung,
sieben Szenen neu vertont. HOWTO §15 um vier Fehlerklassen ergänzt (auch in TODO-schwesterprojekt).
Bewusst so gelassen: Punkte auf den Achsenzahlen (0 | 40) im Clip, leere halbe Seiten im Testblatt.

Rechenfehler: keine — alle Zahlen von Seite, Clips und PDFs samt Fehlerwerten nachgerechnet.
Als korrekt geprüft: Fragen aller acht Clips (`pruef-fragen`), Fragebilder, Leistenziele, Zufallsübungen (Eindeutigkeit von
`deuten` und `art`, Dreiecksungleichung, gedrehte Rechtecke), Punktesummen, TikZ-Bilder, Datenschutz, Konventionen, TALS-Anker.

### HOCH
- [x] 🔊 **«Gleiche Differenzen → linear» ohne Bedingung** (Festhalten 4, Clip antiproportional «Erkennen»/«Merke», Kontrollclip «Merke»):
      G7 B und 4a B sind linear mit ungleichen Differenzen. «Trifft beide Achsen» gilt nur verlängert.
- [x] **Festhalten 4 «x verdoppeln: y wird um gleich viel kleiner»** mehrdeutig (12 − x: −1, −2, −4).
- [x] 🔊 **Clip summe «Gerade»:** Das Rechteck wird bei «x länger» kürzer (Stützpunkte gegen den Ton); ganze Gerade statt Strecke.
- [x] **Clip antiproportional «Vorhersage»:** (20 | 1.5) und «v · 2 ⇒ t : 2» schon beim Erscheinen der Frage im Bild.
- [x] **Raster:** G3 Ansatz-Zeile gegen Fehlerfall; G1(d) als (E) trotz Abhängigkeit von (a); G5 Zeilen (c)/(d) bei Teilaufgaben (a)–(c).
- [x] **Wiederholungen im Gesamttest:** G6 = 3e und Clip-Fehlerbild (0, 10, 20, 50); G8a = Kontrollclip K4F4 (x + y = 10, x = 2 und 4).

### MITTEL
- [x] G5 «bis voll» (steigend mit Obergrenze) nirgends geübt; Tipp `bereich` «endet bei y = 0» verallgemeinert falsch.
- [x] `art`: ungleiche x-Schritte verraten «antiproportional» (98 %); Diagnose bei falscher Richtung (steigend/fallend) bestätigt nur Linearität.
- [x] Sperrliste ohne `be|`, `sk|`, `ar|`, `de|`: Akku 100/8 = Sim 3 (6 %), G7 A, 4a A, Kontrollclip-Werte, 1a als Zufallsübung.
- [x] 1c: Sachgraph als ganze Gerade ins Negative, ohne Einheiten, abzulesender Punkt am unbeschrifteten Rand.
- [x] 4e wiederholt Festhalten (Umfang 24, 6 × 6); K4F3/K4F4/K4F1 wiederholen V3, Kurz wiederholt, 4d, G7.
- [x] Ungeübt im Test: b = 7.5 (G4a), Steigung −1.5 bei Anzahlen deuten (G4b), Division durch 0.3 (G1d), Treppe selbst formulieren (§3).
- [x] 🔊 Rückmeldungen verraten die Lösung (K1F5, Vorhersage Velo, K2F2); K4F1 angezeigt ≠ gesprochen; K3F4 «Schritte zu 4 und 8».
- [x] 🔊 Clip achsen: «33 : 8» ohne die 8 zu nennen; Clip summe «Preise» erklärt x und y nicht, Anker «@Drei» zu früh.
- [x] «Schritt» doppeldeutig (x + 1 gegen Tabellensprung); Sim 3 Variablen (t/Höhe gegen x/y, «1 · x»); 3c(c) Lift unklar; 3d ohne 8 Häuschen.
- [x] Festhalten 2 ohne \(c \neq 0\); Vertiefungslink Kapitel 4 (Modellieren) passt nicht.

### NIEDRIG
- [x] Tipp `tabelle` bei x₀ = 0, `skala` «=» statt «≈», `aufloesen` «durch 1» und Probe bei x = 2 zufällig gleich, `art` ASCII-Minus,
      `deuten` Kerze «die Zahl 3» bei −3x, `bereich` Hefte ohne «nur ganze Zahlen».
- [x] Sim 1 Leiste 5 «Graph:»; Sim 2 Strecke bis zu den Achsen, Beschriftung bei U = 40 verdeckt; 3a «leer» bei der Kerze.
- [x] PDF: G1(b) ohne gedruckte Tabelle, Gedankenstrich neben Formel (G4c), unklarer Satz G4(c), G6(b)-Lösung ungenau, 0 im Musterbild G5.
- [x] Clips: gestrichelte ganze Gerade nicht als falsch markiert (achsen), zweites Rechteck orange, Punkte decken Achsenzahlen,
      Hilfsgerade bis x < 0; Definitionsbereich auch «Definitionsmenge» nennen; Vortest-Hinweis ohne Link auf LP 4.

## Leitprogramm Lineare Funktionen (10.10.2026)

`leitprogramme/lineare-funktionen.html`, gebaut mit `scripts/lp/lineare-funktionen/` (README dort), nach
`~/TODO-BM-Vorkurs-LP03-15.md` §2 (Lineare Funktionen I).

- [x] Unabhängige Prüfung: `/lp-pruefung leitprogramme/lineare-funktionen.html` (Abschnitt unten, behoben).
- [x] Freigeschaltet (nav.js, index.html Bereich «Funktionen», build-seo, Suchindex, Sitemap).
- [ ] 🔑 Abnahme: Bewertungspaket mit einer absichtlich fehlerhaften Lösung einer KI geben (mit Zeichnungen G4, G6, G8).
- [x] 🔑 Hörprobe der acht Clips `lin-lp-*` (10.10.2026, Runde 5: «m», «Geraden», «delta y» bleiben wie bisher). Besonders hinhören:
      «m» (Whisper schreibt oft «n»), «Geraden» (Whisper: «Graben»), «y» als «Ypsilon», «delta y».
- [ ] Bearbeitungszeit mit 2–3 Lernenden messen (geschätzt 205 min).

## Prüfung `lineare-funktionen` (10.10.2026)

Drei unabhängige Prüfagenten (Seite, Clips, PDFs) nach HOWTO §15, nur lesend; geprüft Stand `ae97ad1`. HOCH-Befunde
an der Quelle nachgeprüft und bestätigt. Legende wie oben; Neuvertonung nötig: 🔊.

**Behoben am 10.10.2026** (alles ausser der Hörprobe): `zeigeWert` einmal, Probe mit abweichendem Punkt, Sim 4 ohne Leerzeit,
Farben vereinheitlicht (m und Raten blau, b orange, Dreieck neutral), Gesamttest mit neuen Zahlen (G1, G3–G8; G4 mit Nullstelle,
Teile 6/10/9), Raster (Probe mit dem anderen Punkt, Folgezeilen, Prozentpunkte), 1b mit Gitter, 4d/4e neu (Deutung, Zeichnung),
Bruch mal Zahl in «Kurz wiederholt» und Vortest 0f, y-Achsenabschnitt, Nullstelle mit Schritt und m ≠ 0, Minigraphen voll
beschriftet, m = 0 in den Übungen, Kontrollfragen K4F1 und K4F5 neu vertont. HOWTO §15 um fünf Fehlerklassen ergänzt.
Offen gelassen: Vertiefung Kapitel 4 bleibt der Link aufs lange TALS-Leitprogramm (Vorgabe §2); «Δx = 2» auf der y-Achse (K2F2)
und der Dreiecksschenkel über der Achsenzahl (Clip zeichnen) — beide lesbar.

Rechenfehler: keine — alle Zahlen von Seite, Clips und PDFs samt Fehlerwerten nachgerechnet.
Als korrekt geprüft: Fragen aller acht Clips (`pruef-fragen`), Fragebilder, Geraden und Steigungsdreiecke gegen Formel und
Ton, Knick der Infusion, Leistenziele (Raster, nicht im Start erfüllt), Zufallsübungen samt Sonderwerten, Punktesummen,
TikZ-Koordinaten, Selbsteinschätzung, Datenschutz, Konventionen, TALS-Anker.

### HOCH
- [x] **`zeigeWert` doppelt** in seite.js (Z. 91 und 312): Die zweite Fassung gewinnt, alle Reglerwerte ohne Einheit (Sim 1, 4).
- [x] **Übung `zweipunkte`, Probe-Satz** prüft immer mit B: «gibt bei x = 3 den Wert 7, nicht 7». Mit dem abweichenden Punkt prüfen.
- [x] **Sim 4, Live-Zeile** zeigt «leer nach … min» und den grünen Leerpunkt: verrät Leiste 1, 3, 5. Aufgaben 3 und 5 nennen
      den Zeitregler nicht.
- [x] **Sim 2, Aufgabe 4** «Fallend und flach» bei m = −3/2 (steiler als −1).
- [x] **Gesamttest wiederholt Kapitelaufgaben:** G3 ≈ 2b (gleiches Δx, Δy, m = −2, gleiche Frage), G5 ≈ 4a (b = −2, Nullstelle),
      G7 mit Q(6 | 7) aus Festhalten 4; G6, G8 und Festhalten 4 alle «leer nach 250».
- [x] 🔊 **Clip gleichung, Szene Fehler:** Anker `@Wert` trifft «y-Wert», Notiz 4 s zu früh.
- [x] 🔊 **Kontrolle-gleichung F1 = 4d** (y = 2x + 1, Fehler b = 5); 4d wiederholt Festhalten-Fehler bei P(2 | 5).

### MITTEL
- [x] **G6c, G8c Sachgraph zeichnen** (skaliertes Gitter, Knick) nirgends geübt → 4e um eine Zeichnung ergänzen.
- [x] **Raster:** G4 «mit Steigungsdreieck» gegen «Wertetabelle zählt»; G7 «Probe mit Q» leer, wenn Q eingesetzt wurde;
      G8(b) und G2(c) als (E) obwohl aus eigenem Zwischenwert; G2 «verliert 6 %» mehrdeutig (Prozentpunkte).
- [x] **Farben:** Sim 1 Punkt b grün, Differenzzeile orange (ist m); Δ-Regler Sim 2 orange, Sim 3 blau; Sim 4 «Rate danach»
      orange; `akz-grau` undefiniert; Steigungsdreieck Seite orange, Clips Tinte; Clip steigung Q orange.
- [x] **Bruchrechnen ab Kapitel 3** (⅔x = 1, ½ · 2 + b) weder in «Kurz wiederholt» noch im Vortest; Zwischenschritt fehlt.
- [x] **Kapitel 1 ohne Aufgabe am Graphen** (HOWTO §9).
- [x] **Minigraphen** beschriften nur ±2, ±4: Übung `gleichung` (b ungerade, keine Punkte), 0a, 2c schwer ablesbar.
- [x] **Sim 1 und Clips mit negativen Grössen:** Tabelle −20 l; Kerze und −20x + 200 als ganze Gerade unter 0.
- [x] **«y-Achsenabschnitt»** nie eingeführt; Nullstelle ohne «m ≠ 0».
- [x] **Deutung Gleichung → Sachverhalt** (Vorgabe §2 «erklären») nicht geübt → Teilfrage in 4e.
- [x] **m = 0** kommt in keiner Zufallsübung vor.

### NIEDRIG
- [x] Festhalten 1 «wächst um m» → «ändert sich um m»; 4e «fördert» → «pumpt ab»; 1a Variablen nennen.
- [x] Übung `wert`: Tipp «1x = …» bei m = ±1; `kontext` «(x: t [min])», tautologischer Rückfall; `zeichnen` gleicher Punkt
      zweimal → «senkrecht»; Sperrliste ohne 4d-Paar (2 | 5), (4 | 9).
- [x] Sim 3, Aufgabe 3 «parallel» nicht eingeführt.
- [x] Clips: Merkbild Malpunkt als Trenner; angezeigt «(0 | 0)» gesprochen «Ursprung»; zwei Rückmeldungen nennen fast die Lösung;
      P(6 | 3) schon grün vor der Rechnung; Tabelle in «Tabelle» ganz vor dem Sprechen; «200l» ohne Leerzeichen (`@…@`);
      Dreiecksschenkel über Achsenzahl, «Δx = 2» auf der y-Achse; Merkbild zeichnen ohne Nullstelle; gesprochene Punkte
      uneinheitlich («eins, vier und drei, zehn»); K2F1 = Vortest 0d; K4F5 ≈ Sim 4.2.
- [x] PDF: G5-Punkte verdecken Achsenzahlen; Dreieck im Paket grau; G1a Dezimalzahl nicht geübt; G6 Toleranz bei 750.
- [x] Vertiefung Kapitel 4 auf das lange LP statt auf eine Themenseite (Vorgabe §2 verlangt den LP-Link — bleibt, Themenseite dazu).

## Leitprogramm Bruchterme, Gleichungen und Formeln (10.10.2026)

`leitprogramme/gleichungen-formeln.html`, gebaut mit `scripts/lp/gleichungen-formeln/` (README dort), nach
`~/TODO-BM-Vorkurs-LP03-15.md` §1 (LP 03).

- [x] Unabhängige Prüfung: `/lp-pruefung leitprogramme/gleichungen-formeln.html` (Abschnitt unten, behoben).
- [x] Freigeschaltet (nav.js, index.html, build-seo ohne noindex, Suchindex, Sitemap).
- [ ] 🔑 Abnahme: Bewertungspaket mit einer absichtlich fehlerhaften Lösung einer KI geben.
- [x] 🔑 Hörprobe der acht Clips `gleich-lp-*` (10.10.2026, umgesetzt: «Nun stelle …»). Besonders hinhören:
      «Bruch-Term» (`TAUSCH`), «Zerlege», «Nenner», Fragestart («Kürze», «Rechne», «Stelle»), «y», «A» gegen «a».
- [ ] Bearbeitungszeit mit 2–3 Lernenden messen (geschätzt 210 min).

## Prüfung `gleichungen-formeln` (10.10.2026)

Drei unabhängige Prüfagenten (Seite, Clips, PDFs) nach HOWTO §15, nur lesend; geprüft Stand `3fade4e`. HOCH-Befunde
an der Quelle nachgeprüft und bestätigt. Legende wie oben; Neuvertonung nötig: 🔊.

**Behoben am 10.10.2026** (alles ausser der Hörprobe): Lösungsweg «gl», `formelGleich` mit Mindestzahl definierter Stellen,
Erkundung 4 über die Probe, Gesamttest G2 mit Division (4 P) und G3 (2 P), Raster G8/G2/Bruchstrich-Regel, 4f Kerze statt Treppe,
Übung «Handy-Abo» statt Treppe, Bedingungen nach dem Kürzen, Kontrollfragen K1F1, K2F5, K4F4, K4F5 neu, Sperrliste normiert,
alle acht Clips neu vertont. HOWTO §15 um fünf Fehlerklassen ergänzt (auch in TODO-schwesterprojekt).

Rechenfehler: keine — alle Zahlen von Seite, Clips und PDFs samt Fehlerwerten nachgerechnet (`zahlen.py` 134 × ok).
Als korrekt geprüft: Fragen aller acht Clips (`pruef-fragen`), Fragebilder der Kontrollclips, Leistenziele, Eingabe
(Schreibweisen, gekürzt, ein Bruchstrich, Mengen, Zahlen), Diagnosen, Punktesummen, Datenschutz, Konventionen.

### HOCH
- [x] **Lösungsweg `bruchgleichung`/gl** multipliziert mit p·q, schreibt «· Hauptnenner» (11 % der Würfe, z. B. Paar 2/6).
- [x] **`formelGleich`** wertet `1/0`, `0/0`, `F/(a-a)` als richtig (keine endliche Stelle → «gleich»).
- [x] 🔊 **Kontrollclip Kürzen F5, Rückmeldung zu «0»:** «Nur wenn der Zähler null ist» — der Bruch ist nie 0.
- [x] 🔊 **Clip Rechnen, Vorhersagefrage:** «2x²» gilt als falsch, obwohl die Rückmeldung «geht auch» sagt.
- [x] **K2 «multiplizieren, dividieren»** weder in 2a–2f (Division) noch im Gesamttest geprüft.
- [x] **G7 wiederholt 4f** (Treppe nach h) und den Übungstyp `formelwert/treppe`; Kopfkommentar behauptet das Gegenteil.
- [x] **G8 Raster widersprüchlich:** «Zahlen zuerst eingesetzt: volle Punkte» gegen Pflichtzeile «Formel».

### MITTEL
- [x] Erkundung 4, Aufgabe 4: «: b, dann · 2» ist richtig (Probe stimmt), Leiste gibt kein ✓.
- [x] G3 verlangt «x² + 9 lässt sich nicht zerlegen» — nirgends eingeführt.
- [x] Bedingungen fehlen nach dem Kürzen (Festhalten x ≠ −2, Gegenzahlen x ≠ 3, 1f x ≠ 2, Clip-Zerlegen x ≠ −3).
- [x] Wiederholungen: Sim 4.1 = Clip/Festhalten (s = v·t nach t), Sim 4.5/K4F4/4d dreimal u = 2(l + b), K1F1 gleiches Ergebnis
      wie Festhalten, K2F5 ≈ Festhalten und V1, K4F5 ≈ Clip (km/h), `formelwert/treppe` = 4f.
- [x] Sperrliste: K2F4-Schlüssel fehlt, vertauschte Seiten (3c gespiegelt, gl links/rechts) nicht normiert.
- [x] Zweiklammersatz in Übungen gebraucht, nirgends vorgeführt (Vortest, «Kurz wiederholt»).
- [x] 🔊 Clip Gleichungen «Schritte»: «| −2x» steht beim Erscheinen der Frage schon im Bild.
- [x] 🔊 Bild-Ton: Clip Kürzen «Faktoren» (2/3 zu früh), «Zerlegen» (Zerlegung zu spät), Rechnen «Fehler» (richtig nicht gesprochen).
- [x] 🔊 Rückmeldungen verraten die Lösung (K3F4, K3F5); «Klammer bleibt» bei 2A/(a + c) passt nicht zum Bild (Clip, Festhalten).
- [x] Raster: Regel «ein Bruchstrich» gegen 1/3(x − 5) und Teil C; G2-Fehler in falscher Zeile; Einheiten im Ziel, nicht geprüft.

### NIEDRIG
- [x] Sim 1 «nicht erlaubt: x ≠ …» (doppelte Verneinung), Probe x = 2 bei x(x − 2) zeigt 0 = 0; Sim 2 Reglerfarben.
- [x] `kuerzen/lin` Tipp «1(x − 8)»; `ausschluss` Vorzeichen-Hinweis bei jedem Fehler; `0.5x-1.5` als «nicht gekürzt».
- [x] Grosse Zahlen in `gleichung` (bis ±144) und `bruchgleichung` (bis 120).
- [x] 🔊 «ein Halb» gehört als «1,5»; Brüche gesprochen ohne Klammer um den Zähler; «verboten» statt «nicht erlaubt».
- [x] Clip Rechnen «Mal»: Farbpaare gegen Zähler/Nenner-Farben; Rechenkette: Startkasten F grün.
- [x] K2F1 «Rechne» ohne «kürze»; K2F5 Rückmeldung zu −1 passt nicht zum Fehler.
- [x] G8 «Jahreszins»; PDF-Zeilen eng (G2, G7, G8, G9); G1-Fehlerbeispiele vage; G4/G6 Schreibweisen; README-Verweise.
- [x] Aussprache (Hörprobe 10.10.2026): «gross A / klein a» bleibt wie bisher.

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

- [x] Aufbau umgestellt (09.10.2026, Entscheid Auftraggeber): keine Themenseiten, Leitprogramme auf der Startseite;
      `themen/`, `TEMPLATE.html`, `HOWTO-neue-themenseite.md` gelöscht, `leitprogramme.html` leitet weiter.
- [ ] Weitere Leitprogramme (Bereiche Arithmetik/Algebra, Gleichungen, Geometrie) — Vorlage `scripts/lp/bruchrechnen/`.
- [ ] Glossar, Formelsammlung, Clips (Nachschlag-Seiten, Gerüste). Das Glossar soll auf Leitprogramme verweisen.
- [ ] Werkzeug aus TALS, das noch Themenseiten erwartet: `scripts/build-clips-einbau.py`, `scripts/clips_bibliothek.py`,
      `verify_js_runtime.js` im Pre-Flight (Zweig für `themen/`), `HOWTO-externe-ressourcen.md` — erst anpassen, wenn
      gebraucht (Clips der Leitprogramme sind `probe` und brauchen den Einbau nicht).
- [ ] `feedback.html` sendet an dasselbe Google-Apps-Skript wie TALS Mathe — prüfen, ob
      die Rückmeldungen dort nach Site unterscheidbar sind.

## Leitprogramm Bruchrechnen (09.10.2026, freigeschaltet am selben Tag)

`leitprogramme/bruchrechnen.html`, gebaut mit `scripts/lp/bruchrechnen/` (README dort). Auf Wunsch des Auftraggebers
freigeschaltet (Karte auf der Startseite, Menü, Suchindex, Sitemap), bevor Hörprobe und KI-Test erledigt sind.

- [x] Unabhängige Prüfung: `/lp-pruefung leitprogramme/bruchrechnen.html` (Abschnitt unten, alles behoben).
- [ ] 🔑 Abnahme: Bewertungspaket mit einer absichtlich fehlerhaften Lösung einer KI geben (PDFs am 09.10.2026
      angesehen, Rastertabellen auseinandergezogen).
- [ ] 🔑 Hörprobe der acht Clips `t1-4-lp-*`, je eine Frage absichtlich falsch beantworten. Mit Whisper medium
      gegengehört: «kürzen» wird jetzt als «kührzen» gesprochen (`TAUSCH`), «Hauptnenner» gesprochen nur im Clip «Addieren und Subtrahieren»,
      Szene «Hauptnenner» (sonst «kleinster gemeinsamer Nenner»), «Nenner» nach Pausen mit «und» verbunden.
      Besonders hinhören: «Fünftel» (Whisper verstand an einer Stelle «Fünfte»).
- [ ] Bearbeitungszeit mit 2–3 Lernenden verschiedener Stärke messen (geschätzt 215 min mit Clips, BM-Vorlage §4.3).
- [x] Themenseiten entfallen; Vertiefungslinks auf Mathe begreifbar (g1-1, g1-2, g1-3) statt Themenseite 1.4.
- [x] Freigeschaltet (nav.js, index.html, build-seo ohne noindex, Suchindex, Sitemap).

## Prüfung `bruchrechnen` (09.10.2026)

Drei unabhängige Prüfagenten (Seite, Clips, PDFs) nach HOWTO-leitprogramme §15, nur lesend; geprüft Stand
`ad0ab7a`. HOCH-Befunde von Hand nachgerechnet und bestätigt. Legende: **HOCH** fachlich falsch oder wertet Falsches
als richtig · **MITTEL** Logik, Bild-Ton, Prüfliste verletzt · **NIEDRIG** Kleinigkeit. Neuvertonung nötig: 🔊.

Rechenfehler: keine — alle festen Zahlen (Seite 65, Clips 55, PDFs inkl. aller Fehlerwerte) mit `fractions`
nachgerechnet. Als korrekt geprüft: Fragen aller acht Clips (`pruef-fragen`), Fragebild, Antwortdrehung, Figuren
nachgezählt, Bewegungen, Leistenziele erreichbar und nicht im Start erfüllt, Kürz-Erkennung, Punktesummen, Datenschutz.

**Behoben am 09.10.2026** (Commit nach `95e8940`; HOWTO §15 um vier Fehlerklassen ergänzt). Offen bleibt unten.

- [x] HOCH `addsub`: Würfe mit «Zähler nicht erweitert = richtig» verworfen (20 000 Würfe: 0 Treffer).
- [x] HOCH G4 neu \(\tfrac{9}{14} \cdot \tfrac{7}{12} : \tfrac34 = \tfrac12\); Raster mit beiden Kehrwert-Fehlern, Begründung nur für \(a \cdot b : c\).
- [x] HOCH 🔊 «positiver Brüche» in Clip und Kontrollclip Addieren (neu vertont), Sim 3 «positiven Bruch».
- [x] MITTEL Wortanker: Vergleich nur noch mit gleich langen oder längeren Wörtern, ß → ss; «9», ggT-Notiz (jetzt gesprochen).
- [x] MITTEL Raster: G8 einheitlich 1 von 3 P; Schreibweise des Ergebnisses unter «Allgemein»; fehlende Restpunkte und
      Kehrwert-Fehler in G7/G8; Testblatt mit hochladen; (E) bei G1(a) und G5(b) geklärt.
- [x] MITTEL Wiederholungen: 1c, 2a, 2e (statt 2f), 3d (statt 3e), 4f neu; Kontrollclip Malnehmen Frage 1 neu (3/5 · 5/6, vertont);
      Vortest 0a neu; Gesamttest G1(b), G3 (Vergleichen + Unterschied), G6, G7 neu.
- [x] MITTEL Eingeführt: a − (−b) (Festhalten 4, Vortest 0b, «Kurz wiederholt»), Division durch ganze Zahl (Festhalten 3),
      drei Brüche (Festhalten 2, Aufgabe 2f), Sachaufgabe mit Streifen (3f); Kapitelziel 3 im Gesamttest (G5 Skizze, 3 P).
- [x] MITTEL Sim 4: Diagnose «Minus einer negativen Zahl», «schon gleichnamig»; tote Diagnose entfernt.
- [x] MITTEL `reihenfolge`: kein Zwischen-Hauptnenner über 48; Lösungswege von `reihenfolge`, `vorzeichen`, `mal` in Teilschritten.
- [x] MITTEL Sperrliste: falscher Schlüssel entfernt, Teilschritte und neue Aufgaben ergänzt, `vz`-Produkte sortiert.
- [x] MITTEL 🔊 Clip Reihenfolge: «Steht das Minus vor der Klammer …», Zwischenschritt 2/6 (auch Festhalten 4).
- [x] MITTEL Vortest verweist nicht mehr auf leere Seiten: Kasten «Kurz wiederholt».
- [x] NIEDRIG alle: Klicktoleranz 0.7, Optionen ohne Ergebnis, Rückmeldung 1/9, Farben dokumentiert, Du-Form statt «wir»
      (🔊), «Vielfachen … und so weiter», Kapitel 4 jetzt 45 min, Meldungen bei Subtraktion, Tipp Hauptnenner, «über Kreuz»
      nur fürs Kürzen, 3.0 → ganze Zahl, Vortest 0d, Sim-2-Farben, Formulierung 3d, ungekürzt zählt als Versuch, PDF-
      Tabellen mit mehr Zeilenabstand, G5-Brüche gross, Gesamttest auf 3 Seiten, Selbsteinschätzung nach Anteil je Teil.

**Noch offen**
- [x] «Mehr dazu» und Kompetenzbox verweisen jetzt auf Mathe begreifbar statt auf eine eigene Themenseite.
- [ ] Sim 4 kürzt jedes Teilergebnis selbst (ungekürzte Eingabe wird angenommen und gekürzt angezeigt) — bewusst so,
      «vollständig gekürzt» wird in den Übungen und Aufgaben geübt.

<details><summary>Befunde der Prüfung (Wortlaut)</summary>

### HOCH
- [x] **Übung `addsub` wertet einen Fehler als richtig** (seite.js `neu`/`falsche`): «Zähler nicht erweitert» gibt bei
      2/3 − 1/2 → (2 − 1)/6 = 1/6 = richtig (1.0 % der Würfe, alle Subtraktionen). Würfe verwerfen, in denen
      `{z: x.z ± y.z, n: h}` gleich dem Ergebnis ist (§15 «Sonderwerte»).
- [x] **Gesamttest G4 macht den gelehrten Kehrwert-Fehler unsichtbar** (gesamttest.tex, bewertungspaket.tex G4):
      9/14 · 7/12 = 3/8 ist der Divisor, falscher Kehrwert 8/3 · 3/8 = 1 = richtig. Vorschlag 9/14 · 7/12 : 3/4 = 1/2
      (falscher Kehrwert 2, vergessen 9/32).
- [x] **Raster G4: falsche allgemeine Begründung** (bewertungspaket.tex G4): «bei Mal und Durch ändert die Reihenfolge
      das Ergebnis nicht» widerspricht Festhalten 4 und Aufgabe 4e (1 : ½ · ½ = 1 ≠ 4). Nur den Einzelfall begründen.
- [x] 🔊 **Summenregel ohne «positiv»** (Clip `addieren` Szene «Fehler», Kontrollclip `addieren` Frage 5): «Eine Summe
      kann nicht kleiner sein als einer ihrer Summanden» — falsch für −2/5 + (−2/5) (Aufgabe 4c). Festhalten 2 sagt
      richtig «positiven». Ebenso Sim 3 Aufgabe 3 «Mal einen Bruch kleiner als 1 gibt weniger» → «… positiven Bruch …».

### MITTEL
- [x] **Clip-Anker treffen zu früh** (clips.py `passt` ist zu grosszügig): `@quadriert` trifft «Quadrat» (Notiz «Potenz
      vor Strich» 2.8 s zu früh, Clip `reihenfolge` «Klammer beim Minus»), `@Vielfachen` trifft «Vielfache» (Vielfache
      von 18 2.6 s zu früh, Clip `addieren` «Hauptnenner» → `@Vielfachen#2`). Clip `erweitern` «Vergleichen»: «9»
      bei «acht»; «Vollständig»: Notiz «durch den ggT» vor der Zeile darüber und ungesprochen.
- [x] **Raster G8: gleicher Fehler, andere Restpunkte**: «von links nach rechts» gibt in G6/G7 1 von 3 P, in G8 0 —
      Zeile «Kehrwert» verlangt dort zusätzlich «Punkt vor Strich». Nur den Kehrwert bewerten → 1 von 3 P.
- [x] **Raster: Dezimalzahl/gemischte Zahl** nur im KI-Auftrag geregelt, nicht unter «Allgemein» (Selbstbewertung);
      periodische/gerundete Dezimalzahl ungeregelt. Restpunkte fehlen bei G7 «nur Zähler quadriert» (1 von 3 P) und G9
      «Fehler bei 1/3 + 1/6 gesucht» (2 von 3 P). «Kehrwert vom falschen Bruch» in G7/G8 ungeregelt.
- [x] **Wiederholungen (§9/§15)**: Kapitelaufgabe 2a = Clip/Festhalten 3/8 + 1/8; 2f nimmt 1/2 + 1/3 und 1/6 + 2/6;
      3e = Clip-Produkt 3/4 · 2/3; 4d und 4f prüfen denselben Gegensatz, 4f mit der Festhalten-Basis 2/3 (auch in
      Sim 4); Kontrollclip `malnehmen` Frage 1 = Aufgabe 3f (2/5 · 3/4); Kontrollclip `erweitern` Frage 3 = Vortest
      0a (ggT 18; 24). Gesamttest: G1(b) mit 6/15 wie 1b, G3 Typ von 1c, G6 Struktur des Festhalten-Beispiels, G7
      beginnt wie 4f mit (−2/3)².
- [x] **Nicht eingeführt, aber verlangt**: a − (−b) (Sim 4 Aufgabe 5, 21.5 % der Übung `vorzeichen`) → Zeile im
      Festhalten 4 und Vortest-Aufgabe 3 − (−7); Division durch ganze Zahl (3b, 30 % von `durch`) → Zeile «Kehrwert
      von 7 ist 1/7»; drei Brüche (G2) nur in Kapitel 4 geübt; Sachaufgabe (G5) nirgends geübt; Kapitelziel 3
      «erklärst am Bild» im Gesamttest nicht geprüft.
- [x] **Sim 4 Schrittwähler**: Diagnose «Reihenfolge» unerreichbar (vorher abgefangen); bei −3/4 − (−1/4) = −1 kommt
      «Gleichnamig machen» → «Minus einer negativen Zahl heisst plus».
- [x] **Übung `reihenfolge`**: Hauptnenner in Zwischenschritten bis 130 (3.3 % über 48) → kgV je Schritt ≤ 48.
      Lösungswege von `reihenfolge` und `vorzeichen` nicht kleinschrittig (Gleichnamig/Kehrwert fehlen).
- [x] **Sperrliste**: `dv|2/3|-4/9` sperrt nichts (G8-Schritt kommt als `vz|2/3:-4/9`); es fehlen `er|3/4|16` (1f),
      Teilschritte von 1c, 2a, 4a, 4b, G2, G3, G6, G9; `vz`-Produkte nicht sortiert.
- [x] 🔊 **Clip `reihenfolge` «Klammer beim Minus»**: «Ohne Klammer wird zuerst quadriert», im Bild steht −(1/2)² mit
      Klammer → «Steht das Minus vor der Klammer …». «Beispiel»: Zwischenschritt 2/6 fehlt (auch Festhalten 4).
- [x] **Verweise auf leere Themenseiten** (Vortest-Empfehlung, «Mehr dazu»): vor der Freischaltung lösen.

### NIEDRIG
- [x] Kontrollclip `erweitern` Frage 1: Klicktoleranz 0.5 bei Streifenhöhe 1.2 → 0.7.
- [x] Kontrollclip `malnehmen` Frage 2: nur die richtige Option trägt ein Ergebnis («= 1/4») → alle mit oder ohne.
- [x] Kontrollclip `reihenfolge` Frage 2: Rückmeldung zu 1/9 trifft den Fehler nur halb.
- [x] Farbbedeutung blau/orange in «Vorher kürzen» (Kürzpaar), Kontrollclip `addieren` Frage 2 und Clip `reihenfolge`
      (aktueller Schritt) anders als «erster/zweiter Bruch» → in README dokumentieren oder angleichen.
- [x] Sprechertexte mit «wir» (HOWTO §10: Du-Form). Clip `addieren` «Hauptnenner»: «Die Vielfachen von achtzehn sind
      achtzehn und sechsunddreissig» klingt abschliessend.
- [x] Seite: Kapitel 4 mit 50 min über dem Kapitelmuster; `addsub`-Meldung «plus» auch bei Subtraktion; Tipp
      `hauptnenner` zeigt nur 5 Vielfache (5.7 % ohne Antwort); Lösung `mal` kürzt nachher statt vorher; «über Kreuz» in
      zwei Bedeutungen; 3.0 als Eingabe → «als ganze Zahl»; Vortest 0d (0.75 als Bruch) gegen Kompetenzbox; Sim 2
      Reglerfarbe grün; Formulierung 3e «weniger als das Ganze, 1/2».
- [x] PDFs: in Rasterzellen berühren umbrochene \dfrac-Zeilen einander (G3, G5) → \tfrac oder Zeilenabstand;
      G5-Brüche im Testblatt klein; G9 allein auf Seite 4; (E) «Weg erkennbar» bei G1(a), G5(b); Bewertungspaket
      ohne Aufgabenstellungen (Testblatt mit hochladen); Teil C 12 von 24 P lenkt die Selbsteinschätzung auf Kapitel 4.

</details>

## Leitprogramm Terme und Faktorisieren (09./10.10.2026, freigeschaltet)

`leitprogramme/terme-faktorisieren.html`, gebaut mit `scripts/lp/terme-faktorisieren/` (README dort).

- [x] Unabhängige Prüfung: `/lp-pruefung leitprogramme/terme-faktorisieren.html` (Abschnitt unten, behoben).
- [ ] 🔑 Abnahme: Bewertungspaket mit einer absichtlich fehlerhaften Lösung einer KI geben.
- [x] 🔑 Hörprobe der acht Clips `terme-lp-*` (10.10.2026, umgesetzt: Kacheln, Ypsilon). Besonders hinhören:
      «Kacheln», «y», «Zweiklammersatz», «Rechteck-Schema».
- [ ] Bearbeitungszeit mit 2–3 Lernenden messen (geschätzt 205 min).
- [x] Freigeschaltet (nav.js, index.html, build-seo ohne noindex, Suchindex, Sitemap).

## Prüfung `terme-faktorisieren` (10.10.2026)

Drei unabhängige Prüfagenten (Seite, Clips, PDFs) nach HOWTO-leitprogramme §15, nur lesend; geprüft Stand `1ec3721`.
HOCH-Befunde von Hand nachgeprüft und bestätigt (Sperrliste: `paarSchl` sortiert, Einträge unsortiert; Clipbilder B3/B4
in eigenen Standbildern sichtbar). Legende wie oben; Neuvertonung nötig: 🔊.

**Behoben am 10.10.2026** (alle Punkte ausser den zwei offenen unten): Sperrschlüssel normiert (`norm`, Testhaken `__gesperrt`),
Gesamttest G1/G3/G5/G8 neu (jedes Kapitelziel geprüft), Raster nachgeführt, Probe mit x = 2, Regel (x + m)(x + n) im
Festhalten, neue Übungsart «erst ausklammern», Begriffe der Seite in Rückmeldungen, 7 Clips neu vertont (Klammerprodukte
eindeutig gesprochen), Bilder B3/B4/B5 korrigiert. HOWTO §15 um vier Fehlerklassen ergänzt (auch in TODO-schwesterprojekt).

Rechenfehler: keine — alle Terme und Zahlen von Seite, Clips (60 Gleichungen) und PDFs samt Fehlerwerten nachgerechnet.
Als korrekt geprüft: Fragen aller acht Clips (`pruef-fragen`), Leistenziele erreichbar und eindeutig, Termeingabe
(Schreibweisen, Summe/unvollständig), Punktesummen, Zuordnung Aufgabe → Kapitel, Datenschutz, Konventionen.

### HOCH
- [x] **Sperrliste wirkungslos** (seite.js `SPERRE`): Paare unsortiert eingetragen, `ausmult` reihenfolgeabhängig →
      Festhalten-/Clipbeispiel x² − 7x + 12, Kontrollfragen und Erkundungsziele kommen in den Übungen (bis 4.5 %).
      Schlüssel normieren; fehlende Einträge (bl|p|1|3 = G9, bl|p|1|6, bi|d|1|3, fz|d|1|5, kl|-2|3|-4, zs 1a);
      pruef-schritte zählt über dieselbe Normierung.
- [x] **Lösung 4f «Eine Summe von zwei Quadraten zerfällt nicht»** zu allgemein (4x² + 16 = 4(x² + 4)).
- [x] **Aufgabe 3f** «(a + b)² grösser als a² + b²» gilt nur für positive a, b.
- [x] 🔊 **Kontrollclip Ausmultiplizieren, Merke**: «Zahl am Schluss Produkt, x-Glied Summe» ohne «bei (x + m)(x + n)»
      (Frage 3 desselben Clips widerspricht).
- [x] 🔊 **Clip Vereinfachen, «Minus vor der Klammer»**: Minus-Rahmen bleibt nach dem Umdrehen stehen, «7x» bleibt.
- [x] 🔊 **Clip Binome, «Dritte Formel»**: blaue Fläche doppelt (oben Kopie, unten Original).

### MITTEL
- [x] Probe mit x = 1 (Festhalten 2, 2b, Rückmeldungen) verdeckt Hochzahlfehler → x = 2, «nicht 0 oder 1»; 🔊 «zeigt Fehler sofort».
- [x] Regel (x + m)(x + n) = x² + (m + n)x + mn fehlt im Festhalten (Kap. 2 Übung, Kap. 4 Zweiklammersatz).
- [x] Gesamttest prüft nicht: verschachtelte Klammern, Probe, Flächenmodell, Quadrat-Begründung; G1 ergibt Konstante;
      G8 wiederholt das Festhalten-Muster k(x² − c²).
- [x] Wiederholungen: 1f = Clip/Festhalten (3x + 2 vs 5x), Vortest = «Kurz wiederholt» (3 · (4 + 5), ggT(12; 18), 2x² bei x = 3),
      Sim 2 A5 = Kontrollfrage K4F4, Sim 4 A3 ↔ K2F2.
- [x] Übung `binom`: (a − b)²-Fehler x² − b² nicht erkannt, Meldung zitiert Plus-Formel; `binomluecke` Tipps bei Minus.
- [x] Übung `faktorisieren` übt nie «erst ausklammern, dann binomisch».
- [x] Begriffe in Rückmeldungen nicht eingeführt: Zahlglied, Koeffizient, Binom.
- [x] 🔊 Clip Faktorisieren «Binomisch rückwärts»: Terme erst mit der Lösung im Bild; Bild-Ton-Versätze in «Zusammenfassen»
      (Streifen) und «Fehler» (Anker traf «Fehler» statt «fehlen»); 7² = 49 gleichzeitig mit der Frage.
- [x] 🔊 Gesprochene Klammerprodukte mehrdeutig («x plus zwei mal x plus drei») → «Klammer … mal Klammer …».
- [x] Raster: G5 «andere Wege» unklar, G9 Restpunkte fehlen, andere Begründungen ungeregelt.
- [x] «Vollständig faktorisiert» ohne «mit ganzen Zahlen».

### NIEDRIG
- [x] Übung `klammern` würfelt «0 − (…)»; Tipps «3 · −2x», «3 · (5)»; Gedankenstrich nach Formel in `binom`.
- [x] «zusammengefasst» nimmt `2*3x`, `x*x+5x+6` an; `⋅` und `X` abgelehnt.
- [x] Sim 3 bei a = 8, b = 4 rechts abgeschnitten; Sim 4 «m + n» ohne Erklärung.
- [x] Festhalten 1: Zahlen als gleichartige Glieder nicht genannt; «Kurz wiederholt» ohne Produkt wie 3x · 2x.
- [x] 🔊 Rückmeldungen: Text ≠ Ton (Binome «Ja, richtig», Faktorisieren «nicht −7», K4F2, K4F4); B7 «Einer unten rechts» noch nicht sichtbar;
      K1F4 «Streifen und Quadrate», «Hochzahlen addiert man …», «man».
- [x] Clip Binome «Minus»: warum + b² nicht gesprochen.
- [x] Raster-Kleinigkeiten: G2-Beispiel 2a⁴, G7 «Summe statt Produkt», G4 −16, G8 Gleichung gelöst, PDF-Umbrüche in Formeln, G9 Platz.
- [ ] Farben: ab orange (Kap. 3) vs x-Streifen blau (Kap. 2) — bewusst (README), nicht geändert.
- [x] Aussprache (Hörprobe 10.10.2026): «Kacheln» mit langem ch, «y» → «Ypsilon»; «Zweiklammersatz», «rückwärts» bleiben.

