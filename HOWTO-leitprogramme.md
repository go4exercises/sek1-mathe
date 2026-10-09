# HOWTO — Leitprogramme

**Gilt seit 02.10.2026.** Was in ein Leitprogramm gehört, in welcher Reihenfolge, und wie es
technisch ins Repo kommt — für die Art «nach Thema». Die Art «Übungsprüfung» hat ihre eigene
Anleitung (`HOWTO-uebungspruefung.md`); Layout, Gerüst und Eintragen (§6, §11–§13) gelten für
beide. Bei Widerspruch gilt `STYLEGUIDE.md` §6.5.

Entstanden am 30.09.–02.10.2026 aus der früheren technischen Anleitung (gleicher Dateiname)
und einer Didaktik-Anleitung, erprobt an `leitprogramme/quadratische-funktionen.html`. Wo die
Fassung bewusst von einem der Vorgänger abweicht, steht es als **⟂ Entscheid** dabei; die
Vorgänger stehen in der Git-Geschichte (bis Commit `9c1a4a5`).

**Vorbild für ein neues Leitprogramm:** `leitprogramme/quadratische-funktionen.html`, gebaut mit
`scripts/lp/quadratische-funktionen/seite.py` (siehe dortige README).
**Vor der Freischaltung:** unabhängige Prüfung nach §15 (`/lp-pruefung`).
---

## 0 · Zwei Arten, ein Layout

| | gegliedert nach | Beispiele | Anleitung |
|---|---|---|---|
| **Thema** | dem Stoff: Vorwissen, Kapitel, Gesamttest | `potenzen`, `quadratische-gleichungen`, `gleichungssysteme` | diese Datei |
| **Übungsprüfung** | dem Prüfungsbogen: je Teilaufgabe Clip, Musterlösung, Punktezeile | `uebungspruefung-1`, `trigo2` | `HOWTO-uebungspruefung.md` |

Layout, Kopf, Fuss, Farbtokens und Clip-Bühne sind bei beiden dieselben (§11–§12 gelten
für beide).

---

## 1 · Grundsatz: RLP → Themenseite → Leitprogramm

Drei Ebenen, jede begrenzt die nächste:

1. **Der RLP bestimmt, *was* gelernt wird — und wie die Begriffe heissen.** Quelle: `../Math-GL.pdf` (Grundlagenfach,
   RLP-BM, Abschnitt 6.4.4.1, Gruppe 1) und `../Math-SP.pdf` (Schwerpunktfach, 7.4.4).
   Ein Leitprogramm deckt die **fachlichen Kompetenzen genau eines Teilgebiets** ab
   (z. B. GF 3.3) oder einer klar benannten Teilmenge davon — und **nichts darüber
   hinaus**.
2. **Die Themenseite bestimmt, *wie* es aussieht:** Notation,
   Vorzeichenkonventionen, Achsen, Konstanten, Merksätze, Beispiele. Das Leitprogramm
   erfindet nichts Eigenes.
3. **Das Leitprogramm bestimmt nur den Weg:** Reihenfolge, Umfang, Tests.

### 1.1 Bindung an den RLP (neu)

- **Kompetenzliste wörtlich übernehmen.** Die Kompetenzen des Teilgebiets stehen
  wörtlich (1:1 wie in der RLP-Box der Themenseite) als Kommentarblock im Kopf der
  Leitprogramm-Datei und nummeriert (K1, K2, …) in der Planung (§2).
- **Jedes Kapitelziel gehört zu mindestens einer Kompetenz**, und jede Kompetenz des
  Teilgebiets zu mindestens einem Kapitel. Ein Ziel ohne Kompetenz fliegt raus; eine
  Kompetenz ohne Kapitel wird im Kopf ausdrücklich ausgeschlossen («nicht in diesem
  Leitprogramm: … → eigenes Leitprogramm / Themenseite»).
- **Vorwissen darf aus früheren Teilgebieten stammen** (mit Nummer, z. B. «GF 2.2»),
  aber nicht aus späteren und nicht aus dem Schwerpunktfach, wenn das Leitprogramm im
  Grundlagenfach steht.
- **Was die Themenseite über den RLP hinaus bietet, bleibt dort** — Notationen anderer
  Lehrmittel, Zusatzverfahren, Exkurse. Im Leitprogramm höchstens als Satz «Mehr dazu auf
  der Themenseite».
- **«auch ohne Hilfsmittel» ist verbindlich.** Trägt eine Kompetenz den Vermerk, werden
  ihre Aufgaben im Gesamttest ohne Taschenrechner gestellt. Kompetenzen ohne Vermerk
  dürfen den Rechner verwenden; Rechner-Clips (`werkzeug: true`) gehören dann dazu. Die
  Hilfsmittel stehen im Kopf des Gesamttests, je Teil.
- **Zuordnung sichtbar machen.** Jedes Kapitel trägt in `.kap-meta` die RLP-Nummer
  (`GF 3.3`) und die Kompetenz-Kürzel (`K1 · K2`); die Selbsteinschätzung verweist von
  Testteil über Kapitel auf die Kompetenz.

⟂ Entscheid: Die Didaktik-Fassung sagte «keine Inhalte, die *weder* auf der Themenseite
*noch* im RLP stehen» — damit war alles erlaubt, was irgendwo auf der Themenseite steht.
Jetzt gilt: RLP **und** Themenseite.

### 1.2 Themenseite als fachliche Wahrheit

Variation zwischen den beiden Spuren ist erlaubt, wenn sie eine Funktion hat (anderes
Format, weniger Regler, anderer Kontext). Zufällige Abweichung ist ein Fehler.
**Prüfkriterium:** Lässt sich in einem Satz sagen, *warum* das Leitprogramm es anders
macht? Ja → bleibt, und der Satz steht als Kommentar im Code. Nein → angleichen.

| | Themenseite | Leitprogramm |
|---|---|---|
| Rolle | Referenz: nachschlagen, erkunden, im Unterricht zeigen | geführter Pfad: selbstständig erarbeiten, nachholen |
| Umfang | ganzes Teilgebiet, samt Exkursen | die RLP-Kompetenzen, ausdrücklich abgegrenzt |
| Reihenfolge | nach Sachlogik, springbar | linear, jeder Schritt baut auf dem vorigen auf |
| Animationen | offen, mehrere Regler | Erkundungsauftrag mit einer Frage |
| Übungen | Mini-Checks, Aufgaben A1–A7 | Vortest, Selbsttests mit Punkten, Gesamttest |

---

## 2 · Planung (Pflicht, vor dem HTML)

Aus RLP, Themenseite, Clips und Styleguide entstehen vier Dinge:

**a) Kompetenzmatrix**

```
Kompetenz (RLP, wörtlich gekürzt) | ohne HM? | Kapitel | Selbsttest-Aufg. | Gesamttest-Aufg.
```

**b) Planungstabelle**

```
Kapitel | Lernziel («Du …») | Kompetenz | Clip(s) | Erkundung (Anker) | Beispiel (Quelle) | Häufiger Fehler | min
```

**c) Kern / Vertiefung / bewusst weggelassen.** Was weggelassen wird, steht später im
Leitprogramm als «Nicht in diesem Leitprogramm → Themenseite, Abschnitt …».

**d) Konventionen und Widersprüche.** Liste der Begriffe, Notation, Vorzeichen, Achsen,
Einheiten der Themenseite — und alles, was sich **in der Themenseite selbst**
widerspricht (Text gegen eigene Clips, Tabelle gegen Mini-Check). Widersprüche werden
**nicht** ins Leitprogramm übernommen, sondern gemeldet und zuerst in der Themenseite
entschieden. Wo das Leitprogramm trotzdem schon entstehen soll: die Konvention der
Themenseite nehmen (nicht die des Clips) und die Abweichung im Text in einem Satz
benennen.

⟂ Entscheid: Die Didaktik-Fassung verlangte, die Planungstabelle **vor** jeder Zeile
HTML vorzulegen; `CLAUDE.md` verlangt, klare Aufträge direkt umzusetzen. Jetzt: Die
Planung steht als HTML-Kommentar im Kopf der Datei und im Bericht (§14). **Vorgelegt und
abgewartet** wird nur, wenn (d) einen Widerspruch enthält, der ein Kernkapitel betrifft,
oder wenn eine RLP-Kompetenz sich nicht im Zeitrahmen von §3 unterbringen lässt.

---

## 3 · Umfang und Zeit

- **Eine Lektion = 45 Minuten.** Die Minuten der Kapitel (inkl. Vorwissen und
  Gesamttest) werden addiert; die Summe bestimmt die Lektionenzahl im Kopf. «Zwei
  Lektionen» bei 130 Minuten ist falsch.
- **Zielgrösse nach Format** (Entscheid Auftraggeber 03.10.2026):

  | Format | Kapitel | Gesamt |
  |---|---|---|
  | **Kapitelmuster** (§4; Einführungsclip → Animation → Kontrollclip → Übungen → Aufgaben; Vorbild *Quadratische Funktionen*) | 4–5 Kapitel, je 35–45 Minuten — ein Kapitel ≈ eine Lektion | bis 5 Lektionen plus Vorwissen und Gesamttest |
  | **klassisch** (Leitprogramme vor dem 02.10.2026) | 4–5 Kapitel, je höchstens 30 Minuten | 2–3 Lektionen plus Vorwissen und Gesamttest |

  Ein Kapitel = eine Idee, in beiden Formaten.
- **Lektion und Kapitel nicht doppelt beschriften** (Abnahme 06.10.2026). Im Kapitelmuster ist
  ein Kapitel eine Lektion: Die Seitenleiste fasst die Kapitel unter «Kapitel» zusammen, und es
  gibt keine Lektionsbänder zwischen den Kapiteln — der Kapitelkopf trägt Nummer und Minuten.
  Eine Lektionsgliederung braucht es nur, wo eine Lektion mehrere Kapitel umfasst (klassisches
  Format, z. B. *Gleichungssysteme*).
- **Clips:** rund 6–11 Clips, 8–12 Minuten Clipzeit (STYLEGUIDE §6.5).
- **Über der Zielgrösse (klassisch mehr als 4, Kapitelmuster mehr als 5 Lektionen ohne
  Gesamttest) oder deutlich mehr als 11 Clips → teilen**, jedes Teil mit
  eigenem Vorwissen und Gesamttest (Vorbild: *Quadratische Gleichungen* /
  *Gleichungssysteme*, 07.09.2026).
- Der Kern ist, was ohne Leitprogramm in der Prüfung fehlen würde. Parameter,
  Spezialfälle, zweite Methoden → «Vertiefung» oder Themenseite.

⟂ Entscheid: Didaktik «3–5 Kapitel», Styleguide «vier bis fünf» → **4–5**.

---

## 4 · Aufbau der Seite

```
Kopf          Titel · Standfirst · Fach + Teilgebiet (RLP) · Lektionen
Ablauf        Kapitelliste nach Lektionen, Fortschrittszähler      (Schiene links)
So arbeitest  ① Erfahren → ② Clip → ③ Verallgemeinern → ④ Üben (ohne Lösung) → abhaken
Kompetenzen   RLP-Liste des Teilgebiets, K1…Kn, mit «ohne HM»-Vermerk; Abgrenzung
Kapitel 0     Vorwissen: kurze Klärung + Vortest (Verweis auf Vorwissens-LP/Themenseite)
Kapitel 1…n   je: Lernziel · ① Erfahren (Simulation) · ② Clip · ③ Verallgemeinern
              (Regel, Definition, Beispiel, Häufiger Fehler) · Ausführlich-Link · ④ Üben
Gesamttest    Teile A/B/C ↔ Kapitel ↔ Kompetenzen · Hilfsmittel je Teil · Punkte
Einschätzung  Punktebereiche → konkrete Rückverweise auf Kapitel
Weiter        nächstes Leitprogramm · Themenseite · bewusst Weggelassenes
```

### Innerhalb eines Kapitels: das Muster (Fassung 3, 02.10.2026)

Alle Kapitel von `leitprogramme/quadratische-funktionen.html` folgen diesem Muster; die Seite
entsteht aus einer Kapitelbeschreibung, damit es überall gleich bleibt. Phasen
(`<p class="phase">`) über den Abschnitten — **kein** Fahrplan unter dem Kapiteltitel
(Entscheid 02.10.2026). «So arbeitest du» und die RLP-Kompetenzen stehen oben, beide
eingeklappt (`details.anleitung`).

1. **① Clip.** Ein Einführungsclip zeigt **alles**, was das Kapitel bringt — in Bewegung —
   und endet mit dem allgemeinen Auftrag: «Erkunde diese Zusammenhänge in der nachfolgenden
   Animation und löse die Aufgaben.» Der erste Clip eines Themas führt die Grundform ein
   (hier: Normalparabel über die Wertetabelle).
2. **② Tüfteln.** Die Simulation (§8) trägt ihre Aufgaben **selbst**. Reihenfolge: zuerst
   **Erkunden** (frei an allen Reglern ziehen), dann **konkrete Funktionen zum Nachbauen** —
   nicht die Beispiele aus dem Clip —, dann Zielspiele. Hilfslinien (gestrichelte
   Bezugskurven) lassen sich in jeder Animation, die welche hat, mit einem Schalter aus- und einblenden
   (`<label class="hilfs-schalter">` in der Figur, Klasse `hilfslinie` am Element). Technik: eine Aufgabenleiste
   (`.leiste`) über dem Bild zeigt eine Aufgabe nach der anderen, setzt ✓, sobald der Zustand
   stimmt, und bietet «Nächste ▶» bzw. «überspringen». **Kein Text links daneben** — lange
   Aufträge schrecken ab. Eine Aufgabe = ein Satz. Zielspiele («Triff die grüne Parabel»)
   gehören als letzte Aufgaben dazu.
3. **③ Kontrollfragen.** Ein zweiter Clip mit **neuen** Beispielen — ohne Einleitungsszene, er
   beginnt direkt mit Frage 1 — hält an und fragt
   (Knöpfe oder Tippen ins Bild). Richtig → kurzes ✓, der Clip rollt sofort weiter; falsch →
   Erklärung (vorgelesen) und «Weiter». Danach **Festhalten**: ein Merkkasten (Definition im
   Wortlaut der Themenseite, kurz) und der Häufige Fehler in einem Satz.
4. **④ Üben mit Rückmeldung.** Zwei bis drei `.uebung`-Kästen (§9).
5. **⑤ Aufgaben mit Lösungen.** Drei bis vier Aufgaben auf Papier, Lösung aufklappbar.

**Text aufs Nötigste.** Clip-Karten nur mit Titel und Dauer (keine Unterzeile). Lernziel ein Satz, keine Einleitungsabsätze, keine Hinweise, die der
Clip schon gibt; «Mehr dazu» als eine Zeile mit Link.

Am Ende des Leitprogramms: **Gesamttest und Bewertungspaket als PDF** (§9) — kein HTML.

Zeit: 35–45 Minuten je Kapitel (zwei Clips à ~1 min, Tüfteln ~8–10, Übungen ~8, Selbsttest ~15–20)
— ein Kapitel ≈ eine Lektion (§3). Vorbild: 5 Kapitel + Vorwissen + Gesamttest ≈ 235 Minuten,
rund fünf Lektionen plus Gesamttest. Die Zeiten werden geschätzt, nicht aus der Planung übernommen.

---

## 5 · Entstehung: im Repo, nicht extern

**Der Normalfall ist: eine bestehende Leitprogramm-Seite kopieren** und nur den Inhalt
ersetzen — Kopf, Schiene, Anleitung, Kapitel, Fuss. Dann stehen Dokumentrahmen,
Hosts, Stylesheets, Tokens, Dunkelmodus und Skripte schon richtig (§11). **Nicht
vergessen:** die `localStorage`-Schlüssel (`lp-<name>-thema`, `lp-<name>-stand`), sonst
teilen zwei Leitprogramme einen Fortschrittsstand.

Kommt eine Datei von aussen, gilt die Übertragsliste in §12.

---

## 6 · Layout und Bildschirmbreite (neu)

### Befund

Das Raster der bestehenden Leitprogramme: `.huelle` max. 1180 px, Schiene 236 px,
Abstand 52 px, und `.inhalt` **max. 70ch** — bei 17 px Serif rund 620 px. Auf einem
1280-px-Schirm bleiben rechts vom Text rund 230 px leer, ab 1440 px wächst der leere Rand
auf beiden Seiten. Beispiele, Tabellen und Tests sind dadurch schmaler als nötig, und
ein Graph lässt sich nicht neben den Text stellen, der ihn erklärt.

### Regel: Fliesstext schmal, Arbeitsflächen breit

- **Fliesstext bleibt lesbar schmal:** Absätze, Lernziel, Überschriften höchstens
  **68ch**. Das ist die Zeilenlänge, bei der man am Stück lesen kann — sie wird nicht
  geopfert.
- **Arbeitsflächen nutzen die ganze Spalte:** Beispiel-Tabellen, Selbsttests,
  Gesamttest, Erkundungen, Simulationen, Merk-/Warnkästen. Dafür bekommt `.inhalt`
  **kein** `max-width` mehr; die Begrenzung sitzt auf den Textelementen.
- **Hülle breiter:** `.huelle` max. **1440 px**. Ab 1000 px Schiene links wie bisher.
- **Nebeneinander ab 1180 px:** Der Baustein `.duo` stellt zwei zusammengehörige Teile
  nebeneinander — Beispiel neben Graph, Clip + Merkkasten neben Häufigem Fehler,
  Simulation neben ihrer Anleitung. Darunter stapeln sie sich in Lesereihenfolge (erst
  links, dann rechts). **Die Reihenfolge im Quelltext ist die Lesereihenfolge auf dem
  Handy.**
- **Selbsttests zweispaltig ab 1180 px** (`.aufg.zwei`), wenn die Aufgaben kurz sind;
  jede Aufgabe samt aufklappbarer Lösung bleibt eine Zelle (`break-inside: avoid`).
- **Nicht alles verbreitern.** `.duo` nur, wo die beiden Hälften wirklich zusammen
  angeschaut werden. Zwei unabhängige Kästen nebeneinander zwingen das Auge zum
  Pendeln.
- **Prüfen bei 360, 1280 und 1600 px** (§14); `npm run render-check` meldet seitliches
  Scrollen.

```css
.huelle{max-width:1440px}
.inhalt{min-width:0}                        /* kein max-width mehr */
.kap>p,.kap>h2,.kap>h3,.ziel,.anleitung ol{max-width:68ch}
.duo{display:grid;gap:22px}
@media(min-width:1180px){
  .duo{grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:start}
  .aufg.zwei{columns:2;column-gap:34px}
  .aufg.zwei>li{break-inside:avoid}
}
```

---

## 7 · Clips

- **Clips zeigen, sie erzählen nicht nur.** Wo es einen Graphen gibt, steht er im Clip
  (`graf` mit `parabeln`, `geraden`, `kurven`, `punkte`; HOWTO-clips.md). Bewegung
  entsteht aus einer Folge kurzer Szenen mit je einem Zustand und einem Satz — dieselbe
  Parabel an derselben Stelle, Szene für Szene verschoben, die Normalparabel gestrichelt
  als Bezug. Ein Clip, der «die Parabel wandert nach rechts» nur sagt, verfehlt sein Thema.
- **Je Kapitel zwei eigene Clips** (Entscheid 02.10.2026): Einführungsclip und Kontrollclip.
  Theme **`begreifbar-schlicht`** — ohne Häuschenpapier und roten Rand, weil sich Karo und
  Koordinatengitter stören. Notation wie im Leitprogramm (hier \(x_s\), \(y_s\); gesprochen
  «x s», «y s»).
- **Leitprogramm-eigene Clips sind erlaubt**, wenn sie eine Simulation *des
  Leitprogramms* beschreiben (Entscheid 30.09.2026). Dann: `"probe": true` mit
  `_probe`-Begründung (nicht in der Bibliothek, auf keiner Themenseite), Dateiname
  `<lektion>-lp-<name>`, eine eigene Reihe «<Thema> sehen», Startwert und Farben der
  Simulation. Layout, das sich bewährt hat: Bild rechts (`x` 1010, `y` 175, 760 × 760),
  Formeln und Notizen links (`x` 150), `anim: "fade"` am Bild.
  **Werkstatt:** Drehbücher per Skript erzeugen (gleiche Fenster und Farben in allen
  Szenen), zuerst ohne Ton bauen und mit `pruef-clip.mjs` Szene für Szene ansehen
  (Übersichtsbild), dann `build-clip-ton.py` → `build-clips.py`. **Nach der Vertonung
  das Erzeugerskript nicht mehr laufen lassen** — es überschreibt die gemessenen `dauer`;
  späte Layoutkorrekturen direkt im JSON und nur neu bauen.
- **Sonst nur bestehende Clips**, dieselben Dateien wie auf der Themenseite. Keine fast
  gleichen Varianten mit anderen Zahlen.
- **Themenclips** (Alltagsfrage, Verfahren, «Zum Mitnehmen») passen ins Leitprogramm.
- **Animations-Clips** (`*-anim-*`, «In der Animation hast du …») setzen voraus, dass
  die Animation bedient wurde — nur nach einer Erkundung (§8a).
- **Rechner-Clips** (`werkzeug: true`) nur bei Kompetenzen **ohne** «auch ohne
  Hilfsmittel» im Kern, sonst als «Kontrolle mit dem Rechner» nach dem Handverfahren.
- **Clips anderer Themenseiten** sind im Vorwissen erwünscht.
- **Zahlen im Clip = Zahlen im Text direkt danach.** Widerspricht eine Simulation ihrem
  Clip, wird die Simulation angepasst, nicht der Clip (neu vertonen ist teuer).
- **Dauer** von der Themenseite übernehmen (`cl-zeit` bzw. aria-label des «▶ Clip»),
  bei eigenen Clips die Tonlänge aus `build-clip-ton.py` (abgerundet auf Sekunden) —
  nicht aus dem Drehbuch summieren.
- Fehlt für einen Kernschritt ein Clip: melden, nicht ohne Auftrag bauen.

---

## 8 · Erkundungen und Simulationen

**Bei Funktionen ist die eingebettete Simulation (b) der Normalfall** (Fassung 2). Ein
Link in einen zweiten Tab reisst den Faden ab; wer erst suchen muss, wo er ist, erfährt
nichts. Der Link auf die Themenseite bleibt für die Vertiefung.

**Ist das zu nahe an der Themenseite?** Nein, solange die Rollen verschieden sind: Die
Themenseite ist der offene Spielplatz (alle Regler, alles gleichzeitig, kein Auftrag),
das Leitprogramm führt (ein bis drei Regler, eine Frage, Voraussage, Zielspiel, Treffer-
Rückmeldung). Gleich sein müssen Konventionen und Beispiele, nicht die Bedienung. Jede
Simulation trägt im Code einen Satz, worin sie sich von der Themenseiten-Animation
unterscheidet — lässt er sich nicht schreiben, ist sie überflüssig und der Link genügt.

Entscheid pro Kapitel:

**a) Die Animation der Themenseite passt genau so → Erkundungsauftrag, keine Code-Kopie.**
Kasten «🔍 Erkunden» mit Link auf den Anker (`../grundlagen/<seite>.html#anim-…`, neuer
Tab) und einem **konkreten Auftrag**: was einstellen, was beobachten, was notieren. Die
Frage kommt im Selbsttest wieder. Danach darf der passende `*-anim-*`-Clip folgen.
Höchstens eine Erkundung pro Kapitel.

**b) Geführte Variante** (ein bis drei Regler, eine Aussage, eingebettet) → kleine
SVG-Simulation. Bewährte Muster: Regler + Bezugskurve (gestrichelt) · Zielspiel mit
Treffer-Rückmeldung · Knöpfe, die je ein Merkmal hervorheben · fester Punkt, der
«eingefangen» werden muss · Spiegelpunkt, der eine Symmetrie verrät. Verbindlich:
- Achsen, Variablennamen, Einheiten, Konstanten, **Reglerfarben** (`akz-blau/orange/
  gruen`) identisch zur Themenseiten-Animation
- **Startwert = Beispiel im Text bzw. Clip** desselben Kapitels
- Merksatz in der Bildlegende gleichlautend wie in der «Erkenntnis» der Themenseite
- der Unterschied zur Themenseiten-Animation als Ein-Satz-Kommentar im Code
- Reglerenden und Sichtfenster vorab mit `python3` durchrechnen (bleibt der Scheitel
  im Bild? wo stehen Beschriftungen?)
- trägt ihre Aufträge selbst: Aufgabenleiste `.leiste` mit `Leiste(fig, aufgaben, sim)` —
  je Aufgabe ein Satz (`text`), eine Prüfbedingung auf den Zustand (`ok`) und optional
  `setup` (Ziel einblenden, Modus wechseln); ✓ erscheint von selbst (§4)
- Werte im Text mit Dezimalpunkt und echtem Minus, gerundete mit «≈»

**c) Reine Rechentechnik → keine Animation.** Nur, wo sich wirklich nichts zeigen lässt.

**d) Gleichungen → Umformer** (seit 06.10.2026, Leitprogramm *Lineare und quadratische
Gleichungen*, nach dem Leitfaden des Auftraggebers). Statt Reglern wählen die Lernenden jeden
Umformungsschritt selbst, füllen Lücken und geben die Lösungsmenge ein; die Aufgabenleiste setzt ✓,
sobald sie stimmt. Gültige andere Wege führen ebenfalls ans Ziel, jeder Fehler hat eine eigene
Rückmeldung, Ergebnisse erscheinen erst nach der Antwort. Ein Graph unterstützt höchstens, er
ersetzt den algebraischen Weg nicht. Aufbau der Knoten und Prüfwerkzeug
(`.claude/tools/pruef-umformer.mjs`): `scripts/lp/lineare-quadratische-gleichungen/README.md`.

**e) Geometrie → Arbeitsbereich** (seit 06.10.2026, Leitprogramm *Planimetrie*, nach dem Leitfaden
des Auftraggebers). Drei Arbeitsweisen: Figur verändern (Regler), Hilfslinie antippen (Kandidaten mit
eigener Rückmeldung), Grösse berechnen und eingeben. Gefragte Werte erscheinen erst nach der Antwort;
nichts wird aus Bildschirm-Pixeln abgelesen. Aufbau und Prüfwerkzeug (`.claude/tools/pruef-geo.mjs`):
`scripts/lp/planimetrie/README.md`.
Ebenso gebaut: *Trigonometrische Berechnungen* (GF 5.3, Aufgaben mit festen Werten zeigen sie auch neben
den Reglern, Gesuchtes als «?»; `scripts/lp/trigonometrische-berechnungen/README.md`). *Einheitskreis* und
*Trigonometrische Gleichungen* (GF 5.4/5.5) arbeiten mit Simulationen am Einheitskreis (Regler für den Winkel in
ganzen Grad, Toleranz gegen den ungerundeten Zielwinkel); Aufbau in den README ihrer Ordner.

---

## 9 · Selbsttests und Gesamttest

- **Vortest** prüft nur Voraussetzungen, 8–13 Punkte, mit Verweis bei Lücken.
- **Selbsttest je Kapitel**, 7–16 Punkte, 3–6 Aufgaben à 2–5 Punkte. Mischung:
  Rechnen · Erkennen/Entscheiden · Begründen (mindestens eine «Warum»-Frage).
- **Üben mit Rückmeldung vor dem Selbsttest** (Prototyp 02.10.2026, Kapitel 1 und 3 in
  `quadratische-funktionen.html`): `<div class="uebung" data-typ="…">` — jede Aufgabe
  würfelt neue Zahlen, die Eingabe wird im Browser geprüft (echtes Minus, `0.5`, `1/2`;
  Komma wird verstanden, aber angemerkt), und **jedes bekannte Fehlermuster hat eine eigene
  Rückmeldung** (Vorzeichen in der Klammer, \(c\) statt \(v\), vertauschte Koordinaten,
  Minus in \(-\frac{b}{2a}\) vergessen). Die Lösung erscheint erst nach dem zweiten
  Fehlversuch. Zähler «auf Anhieb richtig in Folge»; nichts wird gespeichert. Neue
  Aufgabentypen stehen als Objekt in `TYPEN` (Felder, Eingabemuster, `neu`, `pruefen`,
  `loesung`). Der Selbsttest mit Papier bleibt danach — er prüft das Aufschreiben.
- **Clips, die fragen**: Wo ein eigener Clip eine Voraussage zulässt, hält er an und
  fragt (HOWTO-clips, «Fragen im Clip»).
- **Mindestens eine Aufgabe am Graphen je Kapitel**, wo es einen gibt: zuordnen
  (Graph ↔ Gleichung), ablesen (Gleichung aus dem Graphen), skizzieren, am Bild
  entscheiden (Vorzeichen von \(D\)). Minigrafen als `<svg class="mini" data-f="a,xs,ys"
  data-fenster="…" data-punkte="…">`, gezeichnet vom Seitenskript — Punkte auf
  Gitterpunkte legen, sonst ist nichts ablesbar. Eine Aufgabe nimmt die Voraussage aus
  ① wieder auf.
- **Kein Selbsttest wiederholt ein Beispiel** (gleicher Typ, andere Zahlen), **kein
  Gesamttest einen Selbsttest.**
- **Jedes Kapitelziel wird geprüft; nichts wird geprüft, was nicht eingeführt ist.**
- **Lösung aufklappbar**, darunter optional eine Zeile `.komm` zur typischen
  Fehlerquelle.
- **Gesamttest und Bewertungspaket nur als PDF aus LaTeX** (Entscheid 02.10.2026, keine
  HTML-Ansicht). Quellen `downloads/leitprogramme/<name>/{gesamttest,bewertungspaket}.tex`,
  gemeinsame Gestaltung `downloads/leitprogramme/lp-druck.sty` (pdfLaTeX, Palatino über
  `mathpazo`, Graphen mit pgfplots). Bauen: `python3 scripts/build-lp-pdf.py [filter]` —
  übersetzt in einem temporären Ordner und legt nur das PDF neben die Quelle. Im Leitprogramm
  steht nur ein Dreischritt mit den beiden Downloads und die Selbsteinschätzung.
  - *Gesamttest-Blatt:* Feld «Code (kein Name)», Anleitung mit Zeit und Hilfsmitteln je Teil,
    Schreibflächen, Hinweis auf das Bewertungspaket.
  - *Bewertungspaket:* (1) So gehst du vor — erst lösen, fotografieren ohne Namen; ob und
    welche KI, entscheiden die Lernenden **selbst und in eigener Verantwortung** nach dem, was
    ihnen aufgrund von Alter und persönlicher Situation erlaubt ist (Altersgrenzen,
    Nutzungsbedingungen, allenfalls Einverständnis der Eltern) — die Seite ist frei
    zugänglich, nicht an eine Schule gebunden; ohne KI Selbstbewertung nach dem Raster;
    Lesung der KI prüfen; (2) **Auftrag an die KI**
    zum Kopieren — erst abschreiben, was sie liest, `[unsicher]` statt raten, Punkte nach
    Raster, Folgefehler nur einmal abziehen, andere Wege voll, jeden Abzug begründen,
    Musterlösung nicht abschreiben, Tabelle und Rückverweis aufs Kapitel, keine Note;
    (3) **Musterlösung und Punkteraster** je Aufgabe (Teilschritt · Punkt · Lösung) mit
    typischen Fehlern und Abzug; (4) Selbsteinschätzung.
  - Ganze Punkte je Teilschritt — halbe Punkte machen die KI-Bewertung unzuverlässig.
- **Gesamttest** 20–25 Punkte, rund 20 Minuten, Teile = Kapitel = Kompetenzen, Hilfsmittel
  je Teil nach RLP-Vermerk (§1.1).
- **Selbsteinschätzung** mit Punktebereichen, die auf **bestimmte Kapitel** zurückverweisen.
- Punkte summieren (Kopf = Summe der Aufgaben), Minuten summieren (§3).

---

## 10 · Notation und Fachsprache

Immer nach `STYLEGUIDE.md`. Beim Vergleich schiefgegangen:

| Was | Regel |
|---|---|
| Lösungsmenge | `\mathbb{L}`, nie ein einfaches L (§2.11) |
| leere Menge | `\mathbb{L} = \{\,\}` |
| Elemente einer Menge | Strichpunkt: `\{-3;\ 3\}` (§2.11, seit 29.09.2026) |
| Lösung eines Systems | als Menge: `\mathbb{L} = \{(2 \mid 3)\}` |
| Parametrisierte Menge | Doppelpunkt: `\{(x \mid 2x-3) : x \in \mathbb{R}\}` |
| Intervalle | `]a;\, b[` |
| Zahlen | Dezimalpunkt; Brüche, wo die Themenseite Brüche verwendet |
| Koordinatensysteme | Achsen mit **Pfeil in positiver Richtung** und Namen am Pfeil (\(x\), \(y\)); bei Anwendungen **Grösse und Einheit** («x [m]», «h [m]», «A [m²]»). Gilt für Simulationen, Minigrafen, Übungsbilder, Clips (`pfeile`, `xname`, `yname`) und PDFs (pgfplots `axis lines=middle`) |
| Scheitel | im Leitprogramm \(S(x_s \mid y_s)\), \(f(x) = a(x - x_s)^2 + y_s\) (Entscheid 02.10.2026); einmal vermerken, dass die Themenseite \(u, v\) schreibt |
| Fachbegriffe | **der Begriff aus den RLP-Kompetenzen** (z. B. Grund-, Scheitel-, Produktform); weicht die Themenseite oder ein Clip ab, deren Namen einmal in Klammern nennen (z. B. «Produktform (Linearfaktorform)»). Die Synonyme stehen auf der Themenseite beim Begriff |
| Methodenwahl | andere Hauptmethode als die Themenseite → beide nennen, Wahl in einem Satz begründen |

Sprache: Du-Form, kurze Sätze, Schweizer Rechtschreibung (ss), kein «wir».

---

## 11 · Technisches Gerüst (gilt immer)

Steht in jeder kopierten Vorlage schon richtig; bei einer Datei von aussen §12.

- Datei unter `leitprogramme/<name>.html`, **genau eine Ebene** unter der Wurzel.
- `<!DOCTYPE html>`, `<html lang="de-CH">`, `<meta charset="UTF-8">`, Viewport.
- **Kein fremder Host:** `../schriften.css`, `../vendor/mathjax/tex-svg.js`.
- **`../style.css` vor dem eigenen `<style>`** — der eigene gewinnt bei gleichem Gewicht.
- **Tokens erben:** im eigenen `:root` nur Übersetzungen (`--karte:var(--weiss)`) und
  der Dunkelmodus; dieser setzt `--weiss` mit und behandelt `.site-footer` eigens.
- **Kopf und Fuss der Site:** `<div id="nav-root">`, `.site-footer` nach STYLEGUIDE §7,
  am Schluss `../mathlib.js`, `../nav.js`, `buildNav({ id: 'leitprogramme' })`.
- **Clip-Bühne aus `mathlib.js`** (`clipBuehne(quelle, titel)`), `BASIS = '../'`.
- **`h2` mit `id`** (Suche schneidet an `h2[id]`); keine `id` doppelt zwischen
  `<section>` und Überschrift.
- **Nicht in `page-wrap` + `main.content` pressen.**

---

## 12 · Übertragsliste für extern gebaute Dateien

Der Reihe nach; in Klammern, woran man merkt, dass der Punkt fehlt.

1. Nach `leitprogramme/<name>.html` verschieben.
2. Google-Fonts-/CDN-Zeilen samt `preconnect` streichen, lokale Pfade setzen (Pre-Flight
   meldet Hosts; ohne Netz Georgia).
3. Dokumentrahmen und Zeichensatz ergänzen (Umlaute zerfallen, erst im Browser).
4. `id` an alle Kapitel-`h2` (Suche findet nur einen Treffer).
5. `BASIS` relativ (Vorschau zeigt Live-Clips).
6. `style.css`, Kopf, Fuss, Skripte einbauen; mitgelieferte Bühne löschen (Sackgasse).
7. Mitgelieferte Palette löschen, soweit mit `style.css` gleich (läuft auseinander).
8. Dunkelmodus: `--weiss` mitsetzen, `.site-footer` eigens (weisse Kopfleiste, weisser Fuss).
9. Eintragen (§13).
10. Layout nach §6 nachziehen.

---

## 13 · Verknüpfen und Eintragen

**Fünf Stellen** — fehlt eine, ist die Seite unsichtbar, unauffindbar oder einseitig:

| Datei | was |
|---|---|
| `leitprogramme.html` | eine Kachel je Leitprogramm unter «Nach Thema» (führt zum Leitprogramm); darauf je Themenseite ihr Titel und die Pille mit ihrer Nummer (`g3.3`, `s3.4a`, führt zur Themenseite); unter Fach und Themenbereich, nach Nummer sortiert (sichtbar sind seit 06.10.2026 nur die Leitprogramme mit Kontrollfragen; die älteren vorübergehend unter «Alte Leitprogramme») |
| `scripts/build-seo.py` | Eintrag in `SEITEN` (Beschreibung, Sitemap) |
| `scripts/build-suchindex.py` | Eintrag in der Liste `ZUSATZSEITEN` (Nachschlagewerke und Leitprogramme) |
| Themenseite | Kasten nach den Lernzielen: «🧭 Lieber geführt? Leitprogramm *…* (≈ n Lektionen)» |
| `index.html` | Pille «LP» neben der Karte jeder Themenseite, die das Leitprogramm abdeckt: Karte in `<div class="karte-lp">` legen, `<a class="lp-link">` daneben (seit 06.10.2026) |

Danach `python3 scripts/build-seo.py` und `python3 scripts/build-suchindex.py` (beide schreiben ohne Schalter; `--schreiben` aus der alten Fassung gibt es nicht).

Im Leitprogramm selbst: «Ausführlich»-Link je Kapitel (§4), Vorwissen verweist auf das
vorausgehende Leitprogramm, der Schluss auf das folgende und auf das bewusst
Weggelassene.

⟂ Entscheid: Die Technik-Fassung kannte drei Stellen, die Didaktik-Fassung forderte den
Themenseiten-Kasten zusätzlich. Jetzt sind es vier.

**Unverlinkt veröffentlichen** (Erprobung, Übungsprüfung per Link): keine Karte, kein
Suchindex, Themenseite ohne Kasten, aber `build-seo.py` **mit `noindex=True`** (nicht
weglassen). Kein `Disallow` in `robots.txt`. Es ist Unauffindbarkeit, keine
Zugangskontrolle. Prüfen:

```sh
grep -c "<dateiname>" sitemap.xml suchindex.js leitprogramme.html   # dreimal 0
grep 'name="robots"' leitprogramme/<name>.html                      # noindex, nofollow
```

---

## 14 · Abnahme vor dem Commit

1. **Jede Lösung nachrechnen** mit einem kurzen `python3`-Skript. Keine Zahl ungeprüft.
2. **Kompetenzmatrix vollständig:** jede Kompetenz ↔ Kapitel ↔ Test; kein Ziel ohne
   Kompetenz; Hilfsmittel im Gesamttest stimmen mit den RLP-Vermerken.
3. Punkte- und Minutensummen stimmen mit Kopf, Ablauf und Testköpfen überein.
4. Konventions-Grep gegen die Themenseite: Fachbegriffe, `\mathbb{L}`, Strichpunkt in
   Mengen, Scheitel-/Parameterbuchstaben, Achsen.
5. Clip-Zahlen gegen Text und Simulationsstartwerte desselben Kapitels.
6. Links in beide Richtungen; Anker der Erkundungen existieren
   (`grep -o 'id="anim-…"'` auf der Themenseite).
7. Kein Selbsttest wiederholt ein Beispiel, kein Gesamttest einen Selbsttest.
8. Technik:
   ```bash
   python3 .claude/skills/preflight/preflight.py leitprogramme/<name>.html leitprogramme.html
   python3 -m http.server 8899 &
   node .claude/tools/pruef-mathjax.mjs http://localhost:8899/leitprogramme/<name>.html
   node .claude/tools/render-check.mjs leitprogramme/<name>.html
   node .claude/tools/pruef-uebungen.mjs leitprogramme/<name>.html 1000   # Zufallsübungen
   node .claude/tools/pruef-formelsatz.mjs leitprogramme/<name>.html 60   # Übungen mit echtem MathJax gesetzt
   node .claude/tools/pruef-leiste.mjs leitprogramme/<name>.html          # Aufgabenleisten
   node .claude/tools/pruef-umformer.mjs leitprogramme/<name>.html        # Umformer (Gleichungen)
   node .claude/tools/pruef-geo.mjs leitprogramme/<name>.html             # Geometrie-Arbeitsbereiche
   node .claude/tools/pruef-fragen.mjs <clip> …                           # Fragen in Kontrollclips
   ```
   Alle drei starten einen eigenen Server und enden mit Exit 1 bei einem Befund.
   `pruef-uebungen` braucht im Seitenskript die Testhaken `box.__aufgabe = A` und
   `box.__typ = T`; die richtige Eingabe ist `A[feld]`, sonst liefert der Typ
   `eingabe(A)`. Gezielte Fehler mit erwarteter Meldung: `fehler(A)` →
   `[[{ feld: 'wert' }, 'Stichwort'], …]` — ohne sie prüft das Werkzeug nur, dass eine
   verschobene Eingabe nicht als richtig gilt, nicht, ob die Diagnose stimmt.
   Bewegung im Clip auf den Ton legen: `python3 .claude/tools/sprechzeiten.py <clip>`.
   und **hinschauen**: hell und dunkel, 360 / 1280 / 1600 px. Keine Prüfung sieht
   zerfallene Umlaute, eine weisse Kopfleiste über dunkler Seite oder einen Clip vom
   Live-Stand.
9. **Bericht** an den Auftraggeber: Planung (§2), was bewusst anders ist als auf der
   Themenseite und warum, welche Widersprüche in der Themenseite gefunden wurden, welche
   Clips fehlen.

---

## 15 · Prüfung vor der Freischaltung

Die Selbstkontrolle in §14 macht, wer baut — und sieht darum, was er sehen will. Beim Vorbild
haben zwei unabhängige Prüfungen nach bestandener §14 noch je rund 25 Befunde gefunden
(03.10.2026, Git-Geschichte von `TODO.md`). Darum gilt für jedes neue Leitprogramm:

1. **Unverlinkt veröffentlichen** (§13), noch nicht freischalten.
2. **Unabhängige Prüfung:** Skill `/lp-pruefung leitprogramme/<name>.html`. Drei frische
   Agenten prüfen Seite, Clips und PDFs gegen die Prüfliste unten und rechnen jede Zahl nach;
   sie ändern nichts. Die Befunde kommen nach `TODO.md`, nach HOCH / MITTEL / NIEDRIG.
3. **Beheben**, Befund für Befund, mit §14 danach; in `TODO.md` abhaken.
4. **Abnahme durch den Auftraggeber** (kann niemand sonst): Hörprobe aller neu vertonten
   Clips mit Fragen — je eine Frage absichtlich falsch beantworten —, und das
   Bewertungspaket mit einer absichtlich fehlerhaften Schülerlösung einer KI geben.
5. **Erst dann freischalten** (§13, alle fünf Stellen).

### Prüfliste — was bei den Prüfungen des Vorbilds aufgefallen ist

Jeder Punkt war ein echter Befund. Wer baut, geht sie vor §15 selbst durch; wer prüft, prüft
gegen sie und darüber hinaus.

**Fachlich**
- Voraussetzungen ausschreiben: Definitionen mit ihren Bedingungen (\(a \neq 0\), reell,
  «nur bei \(D \geq 0\)»), Sachaufgaben mit Variable und zulässigem Bereich.
- Vorzeichen- und Richtungsregeln wörtlich prüfen: «\(x_s\) hat umgekehrtes Vorzeichen» ist
  falsch, «steht in der Klammer mit umgekehrtem Vorzeichen» richtig. Clip, Seite und
  Themenseite müssen dasselbe sagen.
- Erst das allgemeine Verfahren, dann die Abkürzung — und die Abkürzung als solche
  kennzeichnen, mit ihrer Bedingung («Nullstellen-Mitte, wenn die Nullstellen ablesbar sind»).
- Nichts abfragen, was nicht eingeführt ist (Begriff, Schreibweise, Verfahren). Jedes
  Verfahren, das der Gesamttest verlangt, wird in einem Kapitel geübt — **auch seine
  Variante**: Wer \(\sin x = c\) übt, kann noch nicht \(\sin(bx) = c\) (Argument ersetzen).
- Lösung und Aufgabenstellung passen zusammen («ohne Rechnen» + Lösung rechnet = Befund).
- **Ein Verfahren gilt erst als gezeigt, wenn seine Schritte zu sehen sind** — nicht nur das
  Ergebnis. Polynomfunktionen (04.10.2026): Clip, Festhalten und Simulation zeigten von der
  Polynomdivision nur den Quotienten, Aufgaben und Gesamttest verlangten sie von Hand.
- **Auch die Begründung eines richtigen Satzes prüfen.** «Höchstens n − 1 Extremstellen, weil
  zwischen zwei Nullstellen höchstens ein Hoch- oder Tiefpunkt liegt» — der Satz stimmt, die
  Begründung nicht (\(x^4 - 2x^2 - 3\)). Gegenbeispiele stehen oft schon im eigenen Leitprogramm.
- **Die eigene Simulation als Gegenbeispiel-Probe.** Exp/Log (04.10.2026): «\(f\) erreicht \(S\)
  nie» und «der Rückstand \(S - f(t)\) zerfällt» — die Sättigungs-Simulation liess \(A = S\)
  (konstant) und \(A \gt S\) (Rückstand negativ, steigt) einstellen. Jede Aussage gegen alle
  Reglerstellungen der eigenen Animation lesen; richtig war «Abstand \(|S - f(t)|\)» mit \(A \neq S\).
- **Was eine Formel sagt, sagt der Ton genau so.** «Faktor eins plus p» statt «eins plus
  p Hundertstel» gibt bei 5 % den Faktor 6 — gesprochene Kurzformen gegen das Festhalten rechnen.
- **Deutungen in allen Fällen prüfen, nicht im ersten Quadranten.** Trigonometrie (05.10.2026):
  «\(\tan x\) ist die Höhe, in der der *Strahl* durch \(P\) die Tangente trifft» — im 2. und
  3. Quadranten trifft ihn nur die Verlängerung über O hinaus. Die Simulation zeichnete es
  ebenso falsch. Jede geometrische Deutung an je einem Wert pro Quadrant nachzeichnen.
- **Geometrische Regeln mit Bedingung:** «Im stumpfwinkligen Dreieck liegt die Höhe ausserhalb» stimmt nur für
  die zwei Höhen aus den spitzen Ecken; «Segment = Sektor − Dreieck» nur für φ < 180° (Planimetrie 06.10.2026).
- **Regeln mit Bedingung:** «An den Nullstellen von \(f\) entstehen Knicke» stimmt nur bei
  Vorzeichenwechsel (\(x^2\): Nullstelle, kein Knick); «links der Grenze das Vorzeichen drehen» nur
  bei positiver Steigung (\(|4 - 2x|\)). Die eigene Simulation liefert beide Gegenbeispiele.
- **Folgewerte aus ungerundeten Zwischenwerten:** \(0.775 + 2\pi\) gibt 7.058, richtig ist
  \(7.0586 \to 7.059\). Jede gerundete Zahl aus dem exakten Wert neu runden.
- **Kompetenzdeckung ehrlich ausweisen.** Hat ein Teilgebiet wenig Kompetenzen, wandern
  Kapitel leicht in Nachbargebiete (Gleichungen → GF 5.5, Transformationen → SP 3.1). Das ist
  erlaubt, gehört aber in Kompetenzbox und Matrix — sonst verspricht die Seite eine Deckung,
  die der Lehrplan nicht hergibt.
- **Nicht nur nicht abfragen, auch nicht benutzen, was erst später kommt**: \(\ln\) in Kapitel 3,
  erklärt erst in Kapitel 5. Vorgezogenes kurz erklären und im Vortest prüfen.
- **Umkehrung nicht als Folgerung** (Einheitskreis 08.10.2026): «\(\sin\varphi = w \Rightarrow \varphi = \arcsin w\)»
  ist falsch (\(\sin 150^\circ = 0.5\), \(\arcsin 0.5 = 30^\circ\)) — und stand auch auf der Themenseite.
  \(\arcsin w\) ist *der* Winkel aus dem Hauptwertbereich; die Gleichung hat mehr Lösungen.

- **Sachzusammenhang physikalisch möglich** (Modellieren 08.10.2026): Kochsalzlösung mit 30 % (löslich ≈ 26 %),
  Zufallsübung bis 95 % Salz, 60 % Stickstoff. Gehalte je Stoff begrenzen, auch in Würfen.
- **Rechneranzeige nur so weit belegt wie die Quelle**: «poly-solv zeigt den Bruch» ist nur für ganzzahlige
  Koeffizienten belegt. Grundform ganzzahlig machen (mit einem Faktor erweitern) oder die Anzeigeform nicht nennen.

- **Gegenbeispiel-Texte für jede Klasse prüfen** (Vierecke 08.10.2026): «Es hat keine rechten Winkel» stimmt für ein
  Parallelogramm, nicht für jedes Trapez. Eine Rückmeldung «Denk an X» nennt besser ein bestimmtes, gezeigtes X.
- **Definition über eine Eigenschaft, die eine Oberklasse auch hat** (gleichschenkliges Trapez über b = d — gilt für
  jedes Parallelogramm). Definitionen an der Klassenhierarchie des Leitprogramms prüfen.

**Clips**
- **Eine neue Bewegung einmal wirklich laufen lassen.** Nicht ein Bild ansehen, sondern
  über `window.__seek(t)` im `?render`-Modus mehrere Zeitpunkte abtasten und die Pfade
  (`getAttribute('d')`) vergleichen. Am 03.10.2026 standen *alle* bewegten Geraden und
  Kurven still (ein `undefined` in `t0` machte die Zeit zu `NaN`, und `bewZustand` fiel
  auf den letzten Stützpunkt) — `pruef-clip` schiesst Bilder, vergleicht sie aber nicht
  über die Zeit, und keiner der drei Prüfagenten hätte es ohne diese Messung gesehen.
- **Beim Erscheinen einer Frage zeigt das Bild nur, was die Frage gibt** (Abnahme 06.10.2026):
  gegebene Punkte, eine gegebene Kurve («im Bild», «gestrichelt»), sonst nur die Achsen — keine
  «neutrale» Startkurve, kein Steigungsdreieck, kein Lösungspunkt, und die gefragte Kurve nicht,
  wenn sie aus der Gleichung zu bestimmen ist (sonst wird Rechnen zu Ablesen). Die Auflösung
  erscheint erst nach der Antwort (ab 1.0 s) und zeigt dann alles: die Kurve und bei Wahlfragen
  auch die falschen Angebote (z. B. alle drei Punkte, die falschen rot). Umgesetzt
  mit `scripts/lp/fragebild.py` (Tabelle `REGELN` je Clip und Frage; die Bauskripte rufen
  `anwenden(d)` vor dem Schreiben, für Quadratische Funktionen wird es direkt auf die JSONs
  angewendet) und mit `fragebild()` in `scripts/lp/lineare-funktionen/clips.py`. Eine Kurve
  bleibt nur, wo die Frage sie als Bild gibt («im Bild», «gestrichelt», «dieser Kurve») oder
  wo sie im Leitprogramm nicht aus der Gleichung zu gewinnen ist (Extrema einer kubischen
  Funktion ohne Ableitung). Bisher galt: Antwort nicht im Bild
  (erster Stützpunkt neutral, Begleiter und Beschriftung erst nach der Antwort). Das gilt auch für
  **Begleiter, die ihre Koordinaten anschreiben** — ein `startpunkt` oder eine `marke`
  auf dem Klickziel beantwortet die Frage, bevor sie gestellt ist.
- **Klicktoleranz gilt in Dateneinheiten, auf beiden Achsen.** Liegt die Kurve näher am Klickziel
  als die Toleranz (Sättigung: \(f(8) = 98.5\) bei Ziel 100, Toleranz 4), zählt der Klick auf die
  Kurve als richtig. Abstand zur Kurve nachrechnen und die Kurve als `fallen`-Punkt eintragen;
  bei grosser \(y\)-Spanne (1000) ist ein Klick untreffbar — dort eine Wahlfrage.
- Bild und Ton gleichzeitig: Bewegungen nach `sprechzeiten.py` legen, nicht nach Gefühl.
  Was der Ton sagt («senkt um eins»), zeigt das Bild genau so.
- Eindeutige Begriffe («x-Achse» oder «Symmetrieachse», nie «Achse»).
- Eine Farbe, eine Bedeutung — im ganzen Leitprogramm, Clips und Seite (Vorbild: blau \(a\),
  orange \(x_s\), grün \(y_s\)).
- Rückmeldungen lenken aufs Hinschauen und verraten die Lösung nicht; angezeigter Text =
  gesprochener Text.
- Notation wie im Leitprogramm, auch im Merkbild (keine \(u, v\), wo \(x_s, y_s\) gilt).
- **Klickziel auf einer Strecke** (Trig. Berechnungen 08.10.2026): Der Abspieler misst den Abstand zu einem
  Punkt; mit Toleranz 0.9 um die Mitte einer 5 Einheiten langen Seite zählten nur 36 % der Seite. Toleranz bis
  knapp unter den Abstand zu den Nachbarseiten, Fallen auf die anderen Seiten, nachzählen (200 Klickstellen je Seite).
- **Die Rückmeldung einer Falle am Fallenpunkt nachrechnen** (Einheitskreis 08.10.2026): «im Uhrzeigersinn
  gedreht» stand bei \((0.71 \mid -0.71)\) = 315°, gemeint war \((-0.71 \mid -0.71)\).
- **Eine Gerade auf einer Achse ist unsichtbar** (Gerade OP bei 90°): eigens hervorheben und beschriften.

- **Das Einführungsbild verrät die Lösung nicht** (Modellieren 08.10.2026): Becher bis 20/10 gefüllt, Rechtecke
  5 und 7 breit, Balken 14 : 16, bevor gerechnet ist. Neutral beginnen, die Lösung beim Satz zeigen, der sie nennt.
- **Rechnereingaben, die im Bild ablaufen, mitsprechen** — sonst sieben Sekunden Tastendrücke in Stille.
- **Anker nicht auf Zahlwörter legen**: Whisper schreibt «sechzehntausend» als «16 000», der Anker fällt stumm auf
  eine Schätzung zurück. Nachbarwort wählen. Nach Teilvertonung die Szenendauer prüfen (Stille am Ende).

- **Verdeckte Grössen verraten sich** über das Karo, einen gesperrten Regler am Anschlag oder eine massstäbliche
  Figur im PDF (Vierecke 08.10.2026). Karo aus, Regler ausblenden, im Test bewusst verzerrt zeichnen.
- **Würfe mit gegebenen Seiten und Höhen auf Existenz prüfen** (h_a < b, Dreiecksungleichung, 2·Schenkel > Basis)
  und **gerundet angezeigte Angaben nicht ungerundet bewerten** (Dreiecke 08.10.2026: «0.04 m» angezeigt, mit 0.035
  gerechnet — 28 % der richtigen Rechnungen falsch).
- **Linien aus derselben Ecke**: Ihre Treffstreifen überlappen; der nächstliegende Kandidat muss gewinnen, und
  Beschriftungen dürfen den Klick nicht schlucken. Mit echten Klicks messen, nicht nur mit `pruef-geo`.

**Animationen und Übungen**
- Kein Ziel der Aufgabenleiste ist schon im Startzustand erfüllt; Ziele sind nicht die
  Beispiele aus dem Clip; Überspringen wird als Überspringen gezählt (`pruef-leiste`).
- **Auch nicht beim Wechsel**: Setzt eine Aufgabe ein neues Polynom, darf der Endzustand der
  vorigen Aufgabe (Reglerstellung) das neue Ziel nicht schon erfüllen — `pruef-leiste` prüft nur
  den Startzustand. Im `setup` die Regler zurücksetzen — oder allgemein in der Leiste: `gehe(j)`
  setzt alle `input[type=range]` auf `defaultValue` (Vorbild `exp-log-funktionen/seite.js`).
- **Periodische Ziele haben mehrere Lösungen.** Ein Leistenziel «triff die Kurve» mit
  \(u = \tfrac{\pi}{6}\) wird auch von \(u = -\tfrac{5\pi}{6}\) getroffen (Periode \(\pi\)). Kurven
  vergleichen (an einigen Stellen auswerten), nicht Reglerwerte.
- **«Erkunde» auch nach dem Überspringen lösbar?** Betrag/Trigonometrie (05.10.2026): Die
  Leiste leerte das Merk-Objekt `bewegt` mit `bewegt = {}`; die Regler schrieben ins alte Objekt,
  das ihnen beim Start übergeben worden war. Ergebnis: Nach «überspringen» und «zu den offenen»
  gab die erste Aufgabe nie mehr ✓. Objekte leeren, nicht neu zuweisen. Prüfen: alles
  überspringen, «zu den offenen», alle Regler ganz durchfahren — ✓ erwartet.
- **Ein Schalterklick ist keine Lösung.** Liegt der Startwert eines Reglers schon im Ziel, löst
  das Umlegen eines Schalters die Aufgabe (Sim 3: «Betrag ändert nichts» bei q = 1 ≥ 0).
  `pruef-leiste` sieht das nicht, weil es Schalter nicht umlegt.
- **Schalter beim Wechsel zurücksetzen** wie die Regler (`.sim-schalter` auf `defaultChecked`),
  und eine Aufgabe, die einen Schalterzustand braucht, nennt ihn im Text («Sinus: …»).
- **Korrigierende Listener vor dem Zeichnen registrieren** (`ohneNull`): Sonst zeichnet die
  Simulation noch den verbotenen Wert, während der Regler schon daneben steht.
- **Gültige Umwege sind keine Fehler** (Umformer, Gleichungen 06.10.2026): Eine erlaubte, aber ungeschickte
  Umformung bekommt einen grauen Hinweis («Erlaubt, aber …»), keine rote Rückmeldung — sonst lernt man,
  dass nur der kürzeste Weg richtig sei. Im Umformer: Knopfziel mit `?` statt `!`.
- **Gesamttest: Variante üben, ohne das Modell zu wiederholen.** Verlangt der Test eine Variante (zwei kritische
  Werte, D(k) quadratisch, irrationale Lösungen), steht sie vorher in einer Kapitelaufgabe; der Test kombiniert
  dann Geübtes neu (Bruch + Minusklammer, Ergänzung → Lösungsanzahl, Verfahren begründen statt lösen,
  Fehler in einer fremden Lösung finden).
- Zufallsübungen: nur lösbare, «schöne» Fälle; Sonderwerte (0, ±1, gleiche Zahlen) erzeugen
  keine falsche Diagnose; Randfälle des Stoffs mit üben (z. B. \(D = 0\), \(D \lt 0\));
  kein Zufallsfall gleich einer festen Aufgabe (`pruef-uebungen` mit `fehler()`).
- **Die Sperrliste gegen feste Aufgaben darf den Wurfraum nicht leerfegen.** Hängt die
  Aufgabe eines Typs nur an einem Merkmal (etwa der Parität des Exponenten), sperrt eine
  Liste nach Funktion fast alles — der Typ zeigt dann immer dieselbe Aufgabe mit immer
  derselben Antwort. Nachzählen: 20 000 Würfe simulieren und die Verteilung ansehen.
- **Was eine Rundungsfunktion ausgibt, gehört nachgerechnet.** Eine Live-Anzeige auf zwei
  Stellen macht aus \(0.04^2 = 0.0016\) ein «\(= 0\)» — und damit eine falsche Aussage.
- Hinweise rechnen nicht anders als die Lösung (Klammerzahlen ≠ Nullstellen).
- **Sperrliste für jeden Typ**, nicht nur für die mit Nullstellenliste: Ein Typ «Extrempunkt
  berechnen» würfelte sonst genau eine Gesamttest-Aufgabe samt Lösung. Eigener Schlüssel je Typ.
- **Sonderwerte können einen Fehler unsichtbar machen**: Bei einer doppelten Nullstelle ±1 gibt
  das vergessene Quadrat dasselbe \(a\) — die falsche Rechnung gilt als richtig. Solche Werte
  nicht würfeln.
  Ebenso **kleine Winkel**: \(\arcsin 0.05 = 2.87^\circ\), \(\arctan 0.05 = 2.86^\circ\) — «Sinus statt Tangens»
  galt in 23 % der Würfe als richtig (Trig. Berechnungen 08.10.2026). Nur Fälle würfeln, in denen sich falsche
  und richtige Formel auf der verlangten Genauigkeit unterscheiden.
- **Feste Werte bestimmen auch die Anzeige neben den Reglern** (Trig. Berechnungen 08.10.2026): Die Figur
  zeichnete `fest`, die Regler zeigten ihren Startwert — teils als Wert der gesuchten Grösse. Gesuchtes als «?».
- **Erreichbarkeit mit Maus und Finger messen** (Trig. Gleichungen 08.10.2026): Toleranz 0.3° bei Schritt 0.5°
  auf 721 Stufen in 144 px — nur ein Reglerwert trifft, auf dem Handy keiner. Toleranz gegen den ungerundeten
  Zielwert, mindestens zwei treffende Reglerwerte, pixelweise nachmessen.
- **CSS für Bilder mit Kindselektor** (`.rahmen > svg`): `.sim-breit svg{display:block}` traf auch die
  MathJax-Formeln der Aufgabenleiste — jede Formel stand auf eigener Zeile.
- **Was ein Übungsbild zeigen soll, in Pixeln nachrechnen**: Bei Nullstellenabstand 1 ist der
  Buckel einer doppelten Nullstelle 1–2 px hoch — Berühren und Schneiden sind nicht zu unterscheiden.
- **Farbwörter in Rückmeldungen gegen den Abspieler prüfen.** Nach einem Fehlklick zeichnet er den
  eigenen Tipp orange und das Ziel **grün** — «Der blaue Kreis zeigt die Stelle» war in zwei
  Leitprogrammen falsch.
- **Klickfragen auch ohne Maus lösbar** (aus Physik, 06.10.2026): Wo der Punkt ablesbare Koordinaten
  hat, bekommt die Frage `"eingabe": ["x", "y"]` (Achsennamen des Graf) — der Helfer `klick()` der
  LP-Bauskripte setzt das als Vorgabe. Ohne Achsen (Planimetrie) kein `eingabe` — dort fehlt der Parameter.
- **Klickfragen brauchen im Bild ein Fenster** (`"tippbar": true`, HOWTO-clips) — sonst werden
  sie stumm übersprungen; `pruef-fragen` meldet «Durchlauf: jede Frage genau einmal».
- **Sperrliste über die Normalform** (Gleichungen 06.10.2026): Ein Schlüssel pro Typ (`ak|a|b`, `zk|b|c`)
  übersieht dieselbe Gleichung in anderer Schreibweise und ignoriert Koeffizienten (18.8 % der Würfe von
  «Verfahren wählen» trafen feste Aufgaben, darunter eine des Gesamttests). Besser: alle festen Gleichungen
  einmal als gekürzte Normalform `a|b|c` sammeln und jeden Typ seine Normalform nennen lassen (`T.quad`).
  **Aber:** Gekürzt wird jedes \(ax^2 = 0\) zu \(x^2 = 0\) — ein fester Eintrag `[4, 0, 0]` sperrte den Fall
  \(b = 0\) ganz (Nachprüfung Gleichungen 06.10.2026). Reine \(ax^2\)-Formen nur über den Typschlüssel sperren
  und nach jeder Änderung an der Liste die Verteilung neu zählen.
- **Ein Fehlerbeispiel muss wirklich falsch sein** (Gleichungen 06.10.2026): «\((x - 3)(x + 1) = 5 \Rightarrow
  x = 8\) oder \(x = 4\) — was ist falsch?» — aber \(4\) ist eine Lösung. Jede angeblich falsche Zahl einsetzen;
  und die richtige Lösung darf keinen Stoff späterer Kapitel brauchen.
- **Ein Beispiel im Festhalten ist nicht die Aufgabe darunter** und nicht die des Gesamttests: Beim Ersetzen
  eines Testbeispiels prüfen, ob die neue Zahl schon in Festhalten, Clip oder Simulation steht.
- **Sperrliste gegen den Schlüssel prüfen, nicht gegen die Aufgabe.** Ein Schlüssel mit
  falschem Vorzeichen (`bg|1|-1|3` für \(|x - 1| = 3\)) sperrt nichts — der Clip-Fall kam weiter.
- **Fragetexte eines Kontrollclips verschieden beginnen lassen**: `pruef-fragen` erkennt eine Frage
  an ihren ersten 20 Zeichen; zwei Fragen «Welche Nullstellen hat …» lassen den Durchlauf scheitern.
- Live-Anzeigen runden nur mit «≈».
- **Die Live-Zeile verrät keine Antwort** (Planimetrie 06.10.2026): Fragt eine Aufgabe der Leiste nach einer
  Grösse, darf die Zeile über der Figur sie nicht anzeigen — auch nicht in den Aufgaben davor bei denselben
  Werten («A = 18 cm²» in A1–A4, gefragt in A5) und nicht als Faktor («k² = 6.25» bei der Frage nach der Bildfläche).
- **Kandidaten zum Antippen dürfen nicht übereinanderliegen** (Planimetrie 06.10.2026): Bei C über der Mitte
  von AB fallen Höhe und Seitenhalbierende zusammen; der Tipp trifft nur die obere, die Aufgabe ist mit der
  Maus unlösbar, und die Rückmeldung zur falschen Linie ist dort falsch. `pruef-geo` prüft das seither.
- **Sollwerte aus ungerundeten Grössen**: Ein Sollwert aus gerundeten Zwischenwerten (γ = 180° − 56.3° − 36.9°
  = 86.8°) lässt die genauere Eingabe 86.82 als «zu grob gerundet» durchfallen. Toleranz je Feld (`tol`).
- **Kein Malpunkt als Trenner neben Mathematik** (STYLEGUIDE §2.1): «m = 2 · f(x) = …» liest sich
  als Produkt. In Live-Anzeigen, Lösungen («\(8\) · \(-4\)»), Clip-Notizen und der Zeile
  «Aufgabe → Kapitel» steht der Strichpunkt. Prüfen: `node .claude/tools/scan-live.mjs --alle`
  (sieht zugeklappte Lösungen nicht — dort `grep ' · '` in den Quellen).
- **Ein Steigungsdreieck, das mit der Steigung mitläuft**, wo m erklärt wird — im Clip wie in der
  Animation; seine Beschriftung weg von den Achsenbeschriftungen setzen (bei \(x = 1\), nicht bei 0).
- Je Kapitel mindestens eine «Warum»-Aufgabe und eine Aufgabe am Graphen (§9). Ein Graph zum
  **Ablesen** braucht beschriftete Stellen an den abzulesenden Werten, nicht nur an der Einheit.
- Verlangt ein Kapitelziel «zeichnen» oder «skizzieren», wird gezeichnet — in einer Aufgabe und im
  Gesamttest (Exp/Log: \(\log_2 x\) durch Spiegeln einzeichnen).

**Gesamttest und Bewertungspaket**
- Jedes Kapitelziel hat eine Aufgabe; kein Modell aus Selbsttest oder Übung wiederholt.
- Raster mit (E) Ergebnis- und (A) Ablesepunkt, typische Fehler mit Restpunkten statt
  Abzügen, gleichwertige Schreibweisen geregelt, Folgefehler je Aufgabe.
- Selbsteinschätzung verspricht keine Kompetenz, die der Test nicht prüft; jede Aufgabe ist
  einem Kapitel zugeordnet.
- Datenschutz: kein Name, keine Standortdaten im Foto.
- **Teile nach Hilfsmittel, nicht nach Aufgabenart** (Modellieren 08.10.2026): Ein Teil «Zahlenrätsel, ohne
  Rechner» verlangte eine quadratische Gleichung von Hand, die das Leitprogramm nur mit poly-solv löste. Was im
  Teil ohne Rechner steht, muss ohne Rechner geübt sein.
- **Eine Regel für Folgepunkte, im ganzen Raster gleich** (5.2a–d 08.10.2026): (E) für Ergebnisse direkt aus den
  Angaben, Folgezeilen für Schritte aus eigenen Zwischenwerten; derselbe Begriffsfehler nochmals gibt keinen
  Folgepunkt; was als «unmöglich» gilt, steht ausgeschrieben. Fehlerwerte so rechnen, wie der Fehler wirklich läuft
  (Ähnlichkeit: «Zuordnung nach Buchstaben» gab PQ ≈ 11.23, nicht 9).
- **Ein Fehlerbeispiel im Raster muss wirklich falsch sein** (Einheitskreis 08.10.2026): «180° − 63.4°» als
  Fehler ergab 116.6° — die richtige Antwort. Jede Fehlerzahl ausrechnen.
- **Gleiche Zahlen, gleiche Punkte**: Zwei typische Fehler mit denselben Ergebnissen dürfen nicht verschieden
  bewertet werden — die KI sieht nur die Zahlen. Unterscheidet nur die Skizze, das so sagen.
- **Fehlt eine Lösung, greift kein Folgepunkt für die Lösungsmenge** (Trig. Gleichungen 08.10.2026: «nur
  339.5°» gab 3 von 4 P). Typischen Fehler «nur der Rechnerwert» in jeder Aufgabe mit mehreren Lösungen regeln.
- **Folgepunkte bei Konstruktionen** auf die eigene Konstruktion beziehen (S auf der Geraden durch den eigenen P),
  nicht auf eine feste Koordinate mit Toleranz.

**Zeit:** geschätzt aus den Teilen, nicht aus der Planung übernommen (§3).

---

## Nicht tun

- Keine Inhalte jenseits der RLP-Kompetenzen des Teilgebiets.
- Keine Animation der Themenseite kopieren — verlinken (§8a) oder bewusst reduziert
  nachbauen (§8b).
- Keine neuen Beispiele erfinden, wenn die Themenseite ein passendes hat.
- Nicht still angleichen, wenn die Themenseite widersprüchlich ist. Melden.
- Keine Bühne, keine Palette doppelt halten.
- Rechnerangaben nur mit Beleg (`HOWTO-clips.md`, «Rechneranzeige»).
