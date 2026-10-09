# TALS-Mathematik · Styleguide

**Version 1.15 · Stand: 27. August 2026** · (1.15: §2.1 `·` nur als Multiplikationszeichen, nie als Trennzeichen; 1.14: Zusatzmaterial ohne Formelauszug, Animations-Hinweise ohne Vorlese-Knopf, neuer Beschriftungs-Helfer `beschriftung()` und `drawGrid`-Optionen §2.9; 1.13: §11 Nachschlagen-Seiten Glossar/Formelsammlung; 1.12: §10.4 verbindliche Färbe-Regel präzisiert)

Dieser Styleguide ist die verbindliche Referenz für alle Themenseiten des Lehrmittels „TALS-Mathematik". Er sichert Konsistenz in Notation, Aufbau, Sprache und visuellem Design — kapitelübergreifend und chatübergreifend.

> **Verwendungshinweis:** Diese Datei liegt im Project-Knowledge des Claude-Projekts. In jedem neuen Chat wird sie automatisch berücksichtigt. Wer eine neue Themenseite baut, liest zuerst hier nach, bevor neue Konventionen erfunden werden.

---

## 1. Verbindliche Quellen

| Bereich | Quelle |
|---|---|
| Notation, Symbole, Begriffe | *Formeln, Tabellen, Begriffe* (Orell Füssli), kurz **FTB** |
| Lehrziele, Kompetenzen | **RLP 2030** (Rahmenlehrplan vom 13. Juni 2025, in Kraft ab 2030) |
| Hilfsmittel-Status | **Promath (SBFI)** — offizielle Formelsammlung der BM |

**Sprachregelung:**
- *„RLP 2030"* bezeichnet das aktuell gültige Rahmenlehrplan-Dokument (datiert 2025, ab 2030 für alle Klassen verbindlich). Zitate immer „RLP 2030", nie „RLP 2025" oder „RLP-BM 2026".
- *„Berufsmaturität Technik, Architektur, Life Sciences"* — Vollform; Kürzel **TALS** nur in Logos/Pills.
- *„Grundlagenfach"* / *„Schwerpunktfach"* — keine Abkürzungen wie „GLF" / „SPF".

---

## 2. Mathematische Notation (FTB-konform)

### 2.1 Multiplikation

- **Mit Multiplikationspunkt** (`·`) zwischen Zahl und Variable, wenn die Variable explizit gemeint ist:
  `f(x) = 2·x + 5` ✓
- **Ohne Punkt** in zusammengesetzten Termen ist toleriert, aber in Live-Anzeigen (interaktive Widgets) immer mit Punkt zur Eindeutigkeit.
- **In LaTeX:** `\cdot` für den Multiplikationspunkt; `*` ist verboten.
- **`·` ist ausschliesslich Multiplikationszeichen — nie Trennzeichen.** Zwischen zwei
  Aussagen, Werten oder Formeln darf kein `·` stehen; es wird sonst als Produkt gelesen
  (`|−3| = 3 · |−3 − 2| = 5` liest sich als «mal 3»). Ersatz je nach Kontext:

  | Situation | Ersatz |
  |---|---|
  | Zwei/drei gleichrangige Ergebnisse in einer Live-Anzeige | Strichpunkt `;` |
  | Zwei aufeinanderfolgende Rechenschritte | Pfeil `→` |
  | Aufzählung von Fällen in Tabelle oder Prosa | Strichpunkt `;` oder echte Liste |
  | Label-Wert-Paare («Amplitude 1 · Periode p = 2π») | Strichpunkt `;` |

  Als reiner **Prosa**-Trenner ohne Mathematik daneben bleibt `·` erlaubt (Fusszeile,
  Link-Untertitel, «Handout · A4 · Bereit zum Drucken», `pt-bereich`-Zeile).
  Geprüft wird das zur Laufzeit mit `node .claude/tools/scan-live.mjs <seiten>` — das
  Skript liest alle Live-Anzeigen im Browser aus, auch die erst beim Reglerziehen
  erzeugten Zweige. Der statische Blick in den Quelltext genügt nicht.
- **LaTeX-Display-Konvention:** Im LaTeX-Display ohne Punkt schreiben (z.B. `f(x) = 3x - 1`), weil MathJax `3x` ohnehin satztechnisch als Multiplikation rendert. Nur dort `\cdot` setzen, wo der Punkt didaktisch nötig ist (z.B. `m_1 \cdot m_2 = -1` bei senkrechten Geraden, oder bei Zahl-mal-Zahl wie `2 \cdot 3 = 6`). In Live-JS-Anzeigen dagegen IMMER mit `·` (siehe oben).

### 2.2 Funktionsschreibweise

```
f(x) = m·x + b           ← Funktionsterm
f : ℝ → ℝ, x ↦ m·x + b   ← Funktion mit Definitions-/Wertemenge
```

In LaTeX:
```latex
f : \mathbb{R} \longrightarrow \mathbb{R}, \quad x \longmapsto m \cdot x + b
```

### 2.3 Variablen und Konstanten

| Was | Schreibweise | Beispiel |
|---|---|---|
| Variablen | kursiv | $x$, $y$, $t$ |
| Funktionen | kursiv | $f$, $g$, $h$ |
| Punkte | grosser Buchstabe, kursiv, mit Koordinaten | $P(2 \mid 3)$ |
| Vektoren | mit Pfeil | $\vec{a}$ |
| Mengen | Doppelstrich | $\mathbb{N}, \mathbb{Z}, \mathbb{Q}, \mathbb{R}$ |
| Zahlen | aufrecht (kein Kursiv) | 2, 5, 0.5 |

### 2.4 Punkt-Komma-Notation

- Koordinatenpaar: `P(2 | 3)` (mit senkrechtem Strich, **nicht** Komma) — FTB-Standard
- Zahlen: Dezimal**punkt** (Schweizer Schulkonvention), nicht Dezimalkomma: `0.5`, nicht `0,5`

### 2.5 Begriffe (verbindlich)

| Korrekt | Falsch |
|---|---|
| Graph | Graf |
| Gerade | Linie (im math. Sinn) |
| Steigung | Anstieg |
| Achsenabschnitt | Y-Achsenschnittpunkt |
| Nullstelle | x-Wert wo y=0 |
| kartesisches Koordinatensystem | XY-System |
| Definitionsmenge \(D\) | Definitionsbereich |
| Wertemenge \(W\) | Wertebereich |
| Probe (Einsetzen in Ausgangsgleichung) | Kontrolle |
| Streckfaktor \(k\) | Streckungsfaktor / Streckenfaktor / Ähnlichkeitsfaktor |
| waagrecht | waagerecht |
| CHF (Währung) | Fr. |

Weitere verbindliche Festlegungen (Terminologie-Audit 2026-07):
- Zentriwinkel/Sektorwinkel/Mittelpunktswinkel: durchgehend das Symbol \(\varphi\) (nicht \(\zeta\)/\(\alpha\)); Namen dürfen kontextpassend variieren.
- Lerngebiet 1 SP heisst «Arithmetik und Algebra» (nicht «Arithmetik/Algebra»).
- Richtungsvektoren einer Ebene = Spannvektoren (Synonyme; bei Erstnennung gleichsetzen).

### 2.6 LaTeX-Konventionen

- **Inline-Formeln:** `\(...\)` — z.B. `\(f(x) = m \cdot x + b\)`
- **Display-Formeln:** `\[...\]` — eigene Zeile
- **Fraktionen:** `\frac{Zähler}{Nenner}`, in Tabellen `\displaystyle\frac{...}{...}` für volle Höhe
- **Bedingung am Ende:** `\quad (m \neq 0)`
- **Symbole:** `\parallel`, `\perp`, Folgerungspfeil `\Longrightarrow` oder `\Rightarrow` (innerhalb einer Seite einheitlich; nie der einfache Pfeil `\rightarrow` als Folgerung)
- **Mengen:** `\mathbb{R}`, `\mathbb{N}`

**Highlighting verbundener Formel-Teile (`\bbox`):** Wenn derselbe Term in zwei Formeln auftaucht und visuell verbunden werden soll (z.B. Diskriminante in Mitternachtsformel und in `D = b² − 4ac` in g3-3), benutze `\bbox[#fde9c7, 3px]{b^2 - 4ac}` (orange Hinterlegung mit 3 px Padding) konsistent in beiden Formeln. Optional ein verbindender Text „↑ derselbe Ausdruck ↓" zwischen den Formeln. Bei dynamischer Live-Anzeige im JS gleiche Farbgebung über CSS-Klasse (z.B. `<span class="disk-hl">`, Hintergrund `#fde9c7`).

MathJax-Voraussetzung: `bbox` und `color` müssen als Pakete geladen sein. Konfig:

```js
MathJax = {
  loader: { load: ['[tex]/bbox', '[tex]/color'] },
  tex: { packages: { '[+]': ['boldsymbol', 'bbox', 'color'] }, ... }
};
```

Ohne die Loader-Erweiterung wird `\bbox` nicht gerendert und die Formel bleibt unhervorgehoben.

**Antipattern: lange `\quad`-Inline-Formel-Reihen in Druckdateien.** Eine Inline-Formel `\(A; \quad B; \quad C; \quad D; ...\)` rendert MathJax als zusammenhängenden, nicht-umbrechbaren Block. Auf A4-Druckseiten mit fester Spaltenbreite läuft so eine Reihe leicht über den rechten Rand hinaus, ohne dass am Semikolon oder `\quad` umgebrochen werden kann. Stattdessen: jeden Beispiel-Eintrag als **eigene Inline-Formel in einer Tabellenzelle**:

```html
<!-- FALSCH (überläuft im Druck) -->
<p>\(\sqrt{12} = 2\sqrt{3};\quad \sqrt{18} = 3\sqrt{2};\quad \sqrt{20} = 2\sqrt{5};\quad ...\)</p>

<!-- RICHTIG (jede Zelle eigene Inline-Formel, Tabelle bricht zwischen Zellen um) -->
<table class="ftb-tabelle"><tbody>
  <tr><td class="li">\(\sqrt{12} = 2\sqrt{3}\)</td>
      <td class="li">\(\sqrt{18} = 3\sqrt{2}\)</td>
      <td class="li">\(\sqrt{20} = 2\sqrt{5}\)</td></tr>
</tbody></table>
```

Faustregel: Inline-Formeln in Druckdateien > 120 Zeichen Inhalt sind verdächtig — entweder als Display-Formel `\[...\]` umbauen oder auf mehrere Inline-Formeln in einer Tabelle/Liste aufteilen.

### 2.7 Intervallnotation (verbindlich, deutsche Schreibweise)

Das Lehrmittel verwendet die **deutsche Intervallnotation** (ISO 31-11), nicht die internationale:

| Typ | Lehrmittel-Standard | NICHT verwenden |
|---|---|---|
| geschlossen | `\([a;\, b]\)` | `[a, b]` (Komma) |
| offen | `\(]a;\, b[\)` | `(a, b)` oder `(a; b)` |
| halboffen (links zu) | `\([a;\, b[\)` | `[a, b)` |
| halboffen (rechts zu) | `\(]a;\, b]\)` | `(a, b]` |
| unbeschränkt nach links | `\(]-\infty;\, b]\)` | `(-\infty, b]` |
| unbeschränkt nach rechts | `\([a;\, +\infty[\)` | `[a, +\infty)` |

**Regel-Logik:**

- **Trennzeichen ist das Semikolon** `;`, nicht das Komma (Komma ist im deutschsprachigen Raum für Aufzählungen reserviert).
- **Klammer-Richtung signalisiert offen/zu:** Klammer zeigt zum Intervall hin → Grenze dabei (zu); Klammer zeigt weg → Grenze nicht dabei (offen). Eckige Klammer wird also entweder nach innen `[…]` oder nach aussen `]…[` geöffnet.
- **Bei `\infty` immer Klammer nach aussen** — Unendlich ist keine Zahl und kann nicht „dabei" sein.

**Verbale Begleitsprache:**

- Schreib nicht „runde Klammer für offen" — die offene Intervall-Klammer ist eckig nach aussen geöffnet, nicht rund. Sag stattdessen „Klammer nach aussen geöffnet" oder „Klammer weist vom Intervall weg".
- Im Zweifel an die Tabelle in g1-2 §5 (Intervalle — Teilmengen von ℝ) anlehnen.

**Am Zahlenstrahl steht dieselbe Klammer wie in der Schreibweise (verbindlich seit 02.08.2026).**
Wo ein Canvas eine Intervall- oder Lösungsmengengrenze markiert, wird sie als
**Klammer** gezeichnet — nicht mehr als gefüllter bzw. hohler Punkt. Der Helfer
dafür ist `intervallKlammer(ctx, x, y, oeffnetRechts, opt)` aus `mathlib.js`:

```js
intervallKlammer(ctx, px(g), y, true,  {farbe:'#1a4f8a'});   // «[»  öffnet nach rechts
intervallKlammer(ctx, px(g), y, false, {farbe:'#1a4f8a'});   // «]»  öffnet nach links
```

Merksatz für die Aufrufstelle: **die Klammer öffnet zur Menge hin, wenn die Grenze
dazugehört, und von ihr weg, wenn sie nicht dazugehört.** Am linken Rand heisst das
`oeffnetRechts = «gehört dazu»`, am rechten Rand `oeffnetRechts = «gehört NICHT dazu»`.

Die Klammer steht **immer symmetrisch zur Achse**, gleich weit nach oben wie nach
unten. Wo dicht darunter die freigestellten Achsenzahlen von `drawGrid` stehen
(auf `y + 14`), wird sie **nach** den Zahlen gezeichnet — die weisse Unterlegung
des Helfers trennt sie dann von der Zahl. Nicht stattdessen die Klammer
verkürzen: die Symmetrie ist Teil der Notation.

Der gefüllte/hohle **Punkt bleibt richtig**, wo es nicht um eine Intervallgrenze geht:
für einen einzelnen ausgeschlossenen Wert (Polstelle, `\(\mathbb{R} \setminus \{2\}\)` —
so etwa `s2-2a` · `br-canvas`), für Lösungspunkte und für Wertemarken auf einer Achse.

Umgesetzt in `g1-2` · `cv-iv`, `g2-1` · `cv-ungl` und `s2-2b` · `ld-canvas`. Die
Begleittexte dürfen dann nicht mehr von „gefülltem" oder „hohlem Punkt" sprechen —
bei einer Umstellung immer mitprüfen (Erklärzeilen, Hinweispaare 👁/💡).

**Diese Konvention gilt auch in Zusammenfassungs- und Kurzform-Tabellen.** Restfunde des M1-Patches (Mai 2026) zeigten, dass Zusammenfassungstabellen leicht übersehen werden — bei Migrationen jede Tabelle einzeln prüfen, die das Wort „Intervall", „Klammer" oder den Begriff „offen/geschlossen" enthält.

---

## 2.8 Kein Gedankenstrich unmittelbar an einer Formel (verbindlich seit 03.08.2026)

In **Titeln** (`<h2>`, `<h3>`, `.anim-titel`, `.block-titel`, `.aufg-titel-text`,
in Physik auch die Diagrammtitel `.cv-titel` — Entscheid Auftraggeber 28.09.2026)
trennt kein Gedankenstrich den Text von der Formel. Gerendert steht der Strich
direkt an der Formel und liest sich als **Vorzeichen**. Das gilt in **beide
Richtungen** — der Strich darf weder unmittelbar vor `\(` noch unmittelbar nach
`\)` stehen:

| falsch | wird gelesen als | richtig |
|---|---|---|
| `Ungleichungs-Labor — \(x^2 + c\)` | \(-x^2 + c\) | `Ungleichungs-Labor: \(x^2 + c\)` |
| `Häufiger Fehler — \((-x)^n\)` | \(-(-x)^n\) | `Häufiger Fehler: \((-x)^n\)` |
| `Gerade \(f(x) = a x + b\) — Achsenschnitte erkunden` | \(b-\) …, Minus am Formelende | `Achsenschnitte erkunden: Gerade \(f(x) = a x + b\)` |
| `Bereich \([0°; 720°[\) — mehrere Perioden` | Strich klebt an der Klammer | `Mehrere Perioden: Bereich \([0°; 720°[\)` |

**Vor** der Formel ist der Ersatz der **Doppelpunkt**; nach einem Frage- oder
Ausrufezeichen entfällt er ersatzlos (`Welches Werkzeug? \(\sin/\cos/\tan\)`).
Kein Mittepunkt `·` als Ersatz — der wird als Malpunkt gelesen und schafft
dasselbe Problem.

**Nach** der Formel hilft kein Ersatzzeichen: dort wird umgestellt. Der Teil nach
dem Strich ist fast immer die Tätigkeit («… erkunden», «… zählen») und gehört an
den Anfang, die Formel ans Ende — dann steht neben ihr überhaupt nichts mehr.
Ist der erste Teil dagegen ein blosses Etikett (`⚠ Wichtig`, `🟢 Beispiel 2`,
`💡 Strategie`), wird nicht umgestellt, sondern der Strich durch den Doppelpunkt
ersetzt.

**Text dazwischen entschärft den Strich.** Kritisch ist nur der direkte Kontakt
mit `\(` oder `\)`. Steht zwischen Formel und Strich noch ein Wort, klärt es die
Lesart, und der Titel bleibt: `Warum \(A = 2\pi r_m \cdot b\) gilt — den Ring
aufrollen` ist in Ordnung.

**Nicht betroffen ist der Fliesstext.** Dort ist der Gedankenstrich ein
Satzzeichen mit grammatischer Funktion («Der Ausdruck unter der Wurzel — \(D =
b^2 - 4ac\) — heisst Diskriminante»); er steht in einem Satzzusammenhang, der die
Lesart klärt, und bleibt.

---

## 2.10 Einbettung von Canvas-Animationen (verbindlich seit 03.08.2026)

Eine Themenseite verwendet für ihre Animationen **eine** Einbettung, nicht zwei
nebeneinander. Es gibt drei Formen, und die Wahl folgt der Rolle der Grafik:

| Form | wofür | Markup |
|---|---|---|
| **`.widget`** | eigenständige interaktive Animation mit Reglern, Live-Formel und Canvas — der Regelfall | `.widget > .widget-header > .widget-titelzeile` + optionaler Untertitel-`<p>`, darunter `.widget-body` mit allem übrigen |
| **`.anim`** | ältere Karte mit Canvas links und Bedienfeld rechts (`.anim-layout`) | bleibt, wo sie steht — **für Neues nicht mehr verwenden** |
| **ohne Rahmen** | Grafik, die zu einem `.block` gehört (Beispiel, Definition) oder zweite Ansicht einer bereits betitelten Grafik | `.cv-wrap` direkt im Block |

Die Klassen `.widget`, `.widget-header`, `.widget-body` stehen **zentral in
`style.css`** (seit 03.08.2026). Sie werden in einer Themenseite **nie erneut
definiert** — seiten-eigene Abwandlungen nur als Modifier daneben, wie
`.widget-kompakt` in `g3-3`.

**Nicht zulässig:** eine freistehende `.widget-titelzeile` mit Reglern und Canvas
direkt im Textfluss. Das ergibt eine Animation ohne Rahmen neben gerahmten auf
derselben Seite; ausserdem bricht das Hinweispaar dort auf eine zweite Zeile um,
weil der Titel oft ein langer Fliesstext-`<p>` ist statt eines `<h3>`.

---

## 2.9 Canvas-Beschriftungen (verbindlich seit Version 1.0)

Jede Beschriftung auf einem Canvas wird über `beschriftung()` aus `mathlib.js`
gesetzt, **nicht** über `ctx.fillText`. Der Helfer stellt den Text frei und klemmt
ihn in die Zeichenfläche — beides war vorher die häufigste Fehlerquelle: Achsenzahlen
lagen ausserhalb des Canvas, Punktnamen auf Kurven, Captions übereinander.

```js
beschriftung(ctx, txt, x, y, { align, baseline, frei, halo, bg, pad, W, H })
```

| Option | Wirkung |
|---|---|
| `align` / `baseline` | wie `ctx.textAlign` / `ctx.textBaseline` |
| `W`, `H` | Canvasmasse — **immer mitgeben**, nur damit wird geklemmt |
| `halo: true` | Kontur entlang der Buchstaben statt Kasten. Für ungleichmässigen Untergrund: Geometriefüllungen, farbige Bereiche |
| `bg` | Farbe der Freistellung. Fehlt sie, gilt die CSS-Hintergrundfarbe des Canvas |
| `frei: false` | keine Freistellung, nur Klemmen |

**Nicht** `bgAuto` im Zeichenpfad einer Animation verwenden — es tastet den Untergrund
pixelweise ab und kostet vier `getImageData` je Beschriftung. Beim Ziehen eines Reglers
sind das GPU-Readbacks im Bildtakt und als Ruckeln sichtbar.

**Punktbeschriftungen** stehen rechts bzw. rechts unterhalb des Punktes, nicht darüber;
nahe am rechten Rand nach links kippen.

**`drawGrid()`** nimmt ein Options-Objekt:

| Option | wann |
|---|---|
| `{ achsenLabels: false }` | Die Seite schreibt eigene Achsenbeschriftungen mit Einheit („x [kg]"). Die generischen `x`/`y` werden dann gar nicht erst gezeichnet — **nicht** mit `fillRect` übermalen, das liess je nach Skalierung einen Strichrest stehen |
| `{ zahlen: false }` | Die Seite bringt eine eigene Zahlenteilung mit; sonst liegen zwei Reihen übereinander |
| Rückgabe `zahlenOben()` | Achsenzahlen nach den Kurven noch einmal obenauf setzen, wenn eine Kurve sie sonst kreuzt |

`drawGrid` wählt die Schrittweite der Zahlenteilung selbst nach verfügbarem Platz
(1-2-5-10) und legt die Zahlen innen an die Achse, wenn der Nullpunkt am Canvasrand
liegt (`xMin = 0` / `yMin = 0`).

**Prüfen:** `node scripts/audit-beschriftungen/audit-run.mjs` (Server auf 8001) misst
Überlappungen, Text auf Grafik und Beschriftungen ausserhalb des Canvas;
`audit-ruckeln.mjs` misst Reglerlast und Bildabstände.

---

## 2.11 Leere Menge (verbindlich seit 21.09.2026)

Die leere Menge wird **als leere Mengenklammer** geschrieben, nie als durchgestrichene Null:

| Wo | Lehrmittel-Standard | NICHT verwenden |
|---|---|---|
| LaTeX (Seiten, Clips, Druckseiten) | `\(\mathbb{L} = \{\,\}\)` | `\emptyset`, `\varnothing` |
| Live-Anzeige (JS-Text), Anki-Karten | `𝕃 = { }` | `∅` |

- **Genau diese Form:** `\{\,\}` mit schmalem Abstand. Nicht `\{\}`, `\{\ \}` oder `\{\;\}` —
  alle stellen dasselbe dar, eine einheitliche Schreibweise macht die Suche nach Restfunden
  aber trivial (`grep -rn 'emptyset\|∅'`).
- **Begleittext:** «die leere Menge», «die Lösungsmenge ist leer». Wo es didaktisch nötig ist:
  «zwischen den Klammern steht nichts». Nicht vom «Leere-Menge-Zeichen» sprechen.
- **Typischer Fehler, der benannt werden darf:** \(\{0\}\) statt \(\{\,\}\) — das ist eine Menge
  mit einem Element, der Null.
- Gilt auch für Sprechertexte von Clips: gesprochen wird «die Lösungsmenge ist leer», nie das
  Zeichen beschrieben.

Umgestellt am 21.09.2026 in allen Themenseiten, Leitprogrammen, Glossar, Formelsammlung,
Druckseiten, Clip-Drehbüchern, Anki-Decks und im Notationstrainer.

**Aufzählende Mengen (verbindlich seit 29.09.2026).** Die Elemente einer aufzählenden Menge
trennt ein **Strichpunkt**, wie bei den Intervallen (§2.7) und den Live-Anzeigen (§2.1):
`\(\mathbb{L} = \{3;\,4\}\)`, in JS-Text `𝕃 = { 3; 4 }` — nicht `\{3,\,4\}`. Das Komma
bleibt der Aufzählung in Prosa vorbehalten. Koordinaten schreiben weiter `(3 | 4)`.
Umgestellt am 29.09.2026 im Lerngebiet G2 (Themenseiten, Clips, Leitprogramme
Quadratische Gleichungen und Gleichungssysteme); **die übrigen Seiten sind noch nicht
umgestellt** — wer eine anfasst, zieht sie mit (`grep -n '\\{[^}]*,' <seite>`).

## 2.12 Eine Rechnung, eine Zeile (verbindlich seit 27.09.2026)

Übernommen aus TALS Physik (Entscheid Auftraggeber 26.09.2026). Symbol, Formel,
eingesetzte Zahlen und Ergebnis stehen in einer Live-Formel (`.formel-live`) als
**eine Kette** in **einer** `.fl-eq`, nicht als Formelzeile mit Zahlenzeile darunter:

- \( t = \log_2(y) = \log_2(64) = 6.00\;\text{h} \) ✓
- oben `t = log₂(y)`, darunter `t = log₂(64) = 6.00 h` ✗

Fehlt der Platz (360 px), bricht die Kette **nur vor einem Gleichheitszeichen** um, nie
mitten in einem Bruch oder Term. Umsetzung: `flTex(id, glieder)` aus `mathlib.js`. Jedes
Glied (`t = \log_2(y)`, `= \log_2(64)`, `= 6.00\;\text{h}`) wird eine eigene Inline-Formel
mit `\displaystyle`, dazwischen `<wbr>`. Ein führendes `=` bekommt ein `{}` davor, sonst
fehlt ihm links der Abstand. Die Formel-Container werden `inline-block`, damit
umgebrochene Brüche sich nicht berühren. Gesetzt wird über die Queue von `mjTypeset`,
höchstens einmal je Frame. `texE(zahl, einheit)` schreibt eine Zahl mit Einheit
(`6.00\;\text{h}`). Ein Array von Glieder-Arrays ergibt mehrere Rechnungen, durch
Strichpunkt getrennt.

**Wie das in Mathe gelesen wird:**

- **Funktionsvorschrift und Funktionswert** sind zwei Aussagen, keine Formel- und
  Zahlenzeile derselben Rechnung. \(f(x) = 2^x\) darf über \(f(3) = 2^3 = 8\) stehen,
  weil sich \(f(3)\) nicht mit \(2^x\) gleichsetzen lässt. Die Wertzeile ist dann aber
  selbst eine **vollständige Kette** (Symbol = eingesetzte Vorschrift = Ergebnis), nicht
  nur \(f(3) = 8\).
- **Produktform = Summenform** ist eine Kette: \(f(x) = 0.5 \cdot (x-1)(x+2)(x-3) =
  0.5 \cdot x^3 - x^2 - 2.5 \cdot x + 3\) in einer Zeile.
- **Umformung und Zahlenprobe** bleiben getrennt, wenn sie zwei Wege zum selben Ergebnis
  sind, etwa \(2^3 \cdot 2^4 = 2^{3+4} = 2^7\) und darunter \(8 \cdot 16 = 128\), oder eine
  quadratische Ergänzung mit der Probe «mit \(x = 4\)».
- **Verschiedene Rechnungen** bleiben getrennte Zeilen. Reine Wertanzeigen (ein Winkel, eine
  Lösungsmenge, ein Status) sind keine Rechnung.

Umgestellt am 27.09.2026: s3-2a (Drei Darstellungen), s3-2b (Pendel), s3-3
(Linearfaktor-Baukasten), s3-4a (Drei Darstellungen), s3-4b (Umkehrfrage).

---

## 3. Achsenskalierung (verbindlich)

> **Diese Regel kommt direkt aus den Projekt-Instructions und gilt unbedingt.**

### 3.1 Reine Mathematik-Aufgaben → 1:1
Alle Diagramme, in denen $x$ und $y$ abstrakte Variablen sind (Beispiele: „Zeichne $f(x) = 2x − 3$"), müssen **kartesisch quadratisch** dargestellt werden — eine Einheit auf der x-Achse hat dieselbe Pixellänge wie eine Einheit auf der y-Achse.

**Code-Konvention:** im Canvas-Helper das Argument `square: true` setzen:
```js
const {ctx, W, H} = initCanvas('canvas-id', 280, true);  // square = true
```

### 3.2 Anwendungsaufgaben → aufgabenbezogen
Wenn $x$ und $y$ unterschiedliche physikalische Grössen mit unterschiedlichen Einheiten sind (Kilogramm und Franken, Sekunden und Meter), wird die Skalierung **aufgabenbezogen** gewählt — also so, dass die relevante Information klar lesbar ist. **Keine 1:1-Forderung.**

**Beispiel — Kartoffeln (Kostenfunktion):**
- x-Achse: 0 bis 15 kg
- y-Achse: 0 bis 35 CHF
- Achsenbeschriftung mit Einheit: `x [kg]`, `K [CHF]` (siehe 3.3)

### 3.3 Achsenbeschriftung mit Einheit

Bei Anwendungsaufgaben **immer** Achsen mit Grösse und Einheit beschriften, in eckigen Klammern:
- `x [kg]`, `K [CHF]`, `t [s]`, `s [m]`, `T [°C]`, `F [°F]` …

Bei reiner Mathematik genügt `x` und `y` ohne Einheit.

### 3.4 Canvas-Inhalt darf bei keinem Schieber-Wert überlaufen (verbindlich)

> **Diese Regel ist aus der Iteration [26_7] hinzugekommen — vergessen kostet Zeit.**

Bei jeder Canvas-Animation, deren Inhalt von Schiebern abhängt, muss die Zeichnung im **Extremfall jedes Sliders** noch komplett im Canvas liegen. Konkret:

- Für **jeden** Schieber das **Worst Case**-Ende durchrechnen — bei `min` und bei `max`. Beispiele:
  - Streckung mit \(k \in [-2, 2]\): bei \(k = -2\) und \(k = +2\) muss das Bild noch in den Canvas passen.
  - Strahlensatz mit Strahlenabschnitt \(\overline{SA} \in [1,4]\) und Streckfaktor \(k \in [2,4]\): worst case \(\overline{SA'} = 4 \cdot 4 = 16\) Einheiten — die Skala (Pixel pro Einheit) muss daraufhin festgelegt sein.
- **Faustregel**: aus den Worst-Case-Pixelkoordinaten ableiten, wie viele Pixel/Einheit zur Verfügung stehen. Dann eher 10–20% Reserve einbauen für Beschriftungen.
- **Originalfigur klein genug wählen**, damit das Bild auch bei \(k = -2\) noch reinpasst — bei zentraler Position bedeutet das: \(|\text{rel}_x|_{\max} \cdot |k|_{\max} + \text{Rand} \leq W/2\).
- **Prüfung beim Schreiben** mit kurzem Python-Skript oder durch Bewegen des Schiebers in beide Extreme. Visuelle Inspektion „in der Mitte" reicht nicht — am Rand wird's eng.

Verstösse in der Vergangenheit: Anim 1/2/3/4 in g5-2d hatten initial Werte gewählt, die bei Schieber-Extremen weit über die Canvas-Grenzen hinausragten. Korrektur in Iteration [26_7].

---

## 4. Didaktischer Aufbau (Master-Schema)

Jede Themenseite folgt diesem Schema in genau dieser Reihenfolge:

```
1. Titel + RLP-Header (Kompetenzen-Liste mit „mit/ohne Hilfsmittel"-Hinweis)
2. Einstieg               — konkretes Anwendungsbeispiel, motivierend, erlebbar
3. Definition             — formal, sauber, FTB-konform
4. Verknüpfung der Darstellungen — Gleichung ↔ Tabelle ↔ Graph (interaktiv)
5. Spezialfälle / Typen   — Übersichtstabelle + Klick-Visualisierung
6. Weitere Theorie        — z.B. Aufstellen der Gleichung, Schnittpunkte, …
7. Aufgaben               — A1 → A6, mit zunehmender Selbstständigkeit:
      • A1: Erkennen / Ablesen
      • A2: Konstruieren / Zeichnen
      • A3: Rechnen (mehrere Teilaufgaben)
      • A4–A6: Anwendung in Realsituation
8. Zusammenfassung        — kompakte Tabelle, Merksatz
8b. Clips                 — generiert zwischen <!-- CLIPS:ANFANG/ENDE --> (build-clips-einbau.py);
                            immer nach der Zusammenfassung, vor dem Zusatzmaterial
                            (Entscheid Auftraggeber 27.09.2026, wie TALS Physik)
9. Zusatzmaterial         — vier Einträge in fester Reihenfolge:
      • Handout (HTML-Druckseite, neuer Tab) — Theorie ohne Beispiele und ohne Aufgaben
      • Anki-Deck erstellen zu automatisieren der Grundlagen (Download `.apkg`)
      • Teste dich selbst (HTML-Druckseite, neuer Tab) — Grundlagenaufgaben mit Lösungen
      • Aufgabenserie (HTML-Druckseite, neuer Tab) — Anwendungsaufgaben mit Lösungen
10. Externe Videos &amp; Aufgabensammlungen — Sektions-ID `ressourcen`, kuratierte Playlists/Watch-URLs in fester Anbieter-Reihenfolge (Details siehe §4 weiter unten)
```

Das Schema ist **didaktisch begründet**:
- Erst der Anker ins Anwendungswissen, dann die Abstraktion (nicht umgekehrt).
- Drei Darstellungen früh verknüpfen — das verhindert das „Symbol-Schubsen" ohne Verständnis.
- Spezialfälle sichtbar machen, bevor sie in Aufgaben auftauchen.
- Aufgabentypen steigern Selbstständigkeit.
- Clips und Zusatzmaterial kommen **vor** den externen Links — denn das eigene Material ist primär.

**Trennung Handout ↔ Aufgaben:** Das Handout enthält nur Theorie (Definitionen, Sätze, Tabellen, Übersichts-SVGs wie eine Geradenschar). **Beispiele** stehen in der Themenseite und in „Teste dich selbst", **Aufgaben** in „Teste dich selbst" (rein-mathematisch) und in der „Aufgabenserie" (Anwendungen). So bleibt das Handout als knapper Theorie-Auszug zum Mitnehmen brauchbar.

**Druckseiten-Anforderungen:** Jede HTML-Druckseite hat oben einen sticky „Seite drucken"-Knopf (`window.print()`) und einen Rück-Link zur Themenseite. Druck-CSS (`@page A4 portrait`, 14 mm Rand, `@media print`) sorgt für saubere Ausnutzung und gute Seitenwechsel. Druckseiten öffnen von der Themenseite immer in einem neuen Tab (`target="_blank" rel="noopener"`).

**Optionale Zusatz-Druckseiten („über RLP hinaus"):** Über die fünf Standard-Druckseiten hinaus dürfen weitere Druckseiten existieren, wenn sie methodisch wertvoll sind, aber den RLP-Stoff verlassen (z.B. `zusatz-gauss-cramer.html` in g2-3). Solche Seiten **müssen** auf der Themenseite klar gekennzeichnet sein — der Subtitel des Download-Links enthält den Zusatz „— fakultativ, über RLP hinaus", und das Format-Feld lautet „Druckseite · über RLP hinaus". Zusatz-Druckseiten zählen nicht zur Pflicht-Materialliste der Themenseite und werden in Übersichten nicht als RLP-Pflichtstoff gewertet.

**Externe Ressourcen (Sektion 10) — Konventionen:**

- Sektions-Header einheitlich: `<h2 id="ressourcen">Externe Videos &amp; Aufgabensammlungen</h2>` — die ID ist immer `ressourcen` (nicht `extern`), der Titel immer dieser exakte Wortlaut. Begründung: ToC-Anchor-Konsistenz, vorhersagbare Cross-Page-Links.
- Strukturiert in zwei Untergruppen mit `<div class="ressourcen-subtitel">`:
  - „🎬 Erklärvideos (Playlists)" — bis zu 4 Einträge
  - „📝 Aufgabensammlungen" — bis zu 4 Einträge
- **Video-Links: nur stabile Watch-/Playlist-URLs** (`youtube.com/playlist?list=…` bevorzugt, ersatzweise `youtube.com/watch?v=…`). **Keine YouTube-Suchergebnis-Links** (`youtube.com/results?search_query=…`) und **keine `youtu.be/…`-Kurz-URLs**.
- **Bevorzugte YouTube-Kanäle (verbindliche Reihenfolge, max. 1 Playlist pro Anbieter, max. 4 Links total):**
  1. MathemaTrick · 2. Lehrerschmidt · 3. Mathe SMI · 4. Mathehoch13 · 5. Magda liebt Mathe · 6. Mathe by Daniel Jung.
  Playlists strikt bevorzugt. Hat ein Anbieter zum Thema keine Playlist → überspringen. Falls nach Durchlauf aller 6 Anbieter weniger als 4 Playlists vorhanden → mit Einzelvideos in derselben Anbieter-Reihenfolge auffüllen.
- **Bevorzugte Aufgabensammlungen (verbindliche Reihenfolge, mehrere Treffer pro Plattform erlaubt, max. 4 Links total):**
  1. sos-mathe.ch · 2. serlo.org · 3. SwissEduc Munterbunt.
  Lösungen müssen verfügbar sein. Negativ-Liste: kein mathebibel.de, kein mathepower.com, kein klassenarbeiten.de.
- **Verifikations-Methode bei Playlist-Kandidaten:** `web_fetch` auf die Playlist-URL liefert Owner und Videocount. Playlist-ID-Präfixe sind keine zuverlässigen Kanal-Indikatoren — immer per `web_fetch` verifizieren.
- **Detail-Anleitung:** `HOWTO-externe-ressourcen.md` (im Repo) enthält das Schritt-für-Schritt-Verfahren, die Anbieter-Map mit bereits verifizierten Playlist-IDs und Platzhalter-HTML für leere Slots. Kurzfassung in `CLAUDE.md`, Abschnitt «Externe Ressourcen».

**RLP-Hilfsmittel-Pill (`<span class="ohm">`) — wann verwenden:**

- Pill **nur** dann, wenn der RLP-Originaltext exakt **„auch ohne Hilfsmittel"** lautet (also für eindeutige, vollständige ohne-Hilfsmittel-Kompetenzen).
- **Nicht** als Pill, sondern als **Inline-Klammertext**, wenn die RLP-Formulierung differenziert ist:
  - „(mit und ohne Hilfsmittel)" — z.B. Schwerpunkt 3.5 Trigonometrische Funktionen
  - „kleine Stichproben auch ohne Hilfsmittel und grosse Stichproben mit Hilfsmitteln" — z.B. Grundlagen 4.3 Masszahlen
  - Solche differenzierten Bedingungen lassen sich nicht in eine kurze Pill pressen, ohne Information zu verlieren — der ungekürzte Klammertext ist hier richtig.
- Begründung für die enge Pill-Verwendung: Eine Pill ist eine **starke visuelle Botschaft** („dieser Stoff muss kopfgerecht sitzen"). Wenn sie inflationär bei jeder „mit Hilfsmittel"-Variation aufkäme, würde sie ihre Signalkraft verlieren.

---

## 4.1 Sub-Split bei umfangreichen RLP-Punkten

Manche RLP-Punkte umfassen so viel Stoff, dass eine einzelne Themenseite nach Master-Schema unhandlich wird (Richtwert: > 1500 HTML-Zeilen oder > 45 Min. Lesezeit). In diesem Fall wird das **RLP-Teilgebiet** auf **zwei oder mehr aufeinanderfolgende Themenseiten** aufgeteilt, die mit Buchstaben-Suffixen `a`, `b`, `c`… nummeriert sind.

**Beispiel:** RLP-Punkt 2.2 *„Lineare und quadratische Gleichungen"* wird umgesetzt als:

```
g2-2a-lineare-gleichungen.html       ← Teil 1 von 2
g2-2b-quadratische-gleichungen.html  ← Teil 2 von 2
```

**Regeln für den Sub-Split:**

- Jede Sub-Seite folgt **vollständig** dem Master-Schema (Abschnitte 1–10): eigener Einstieg, eigene Definition, eigene A1–A6 (plus optional A7 Vertiefung), eigene Zusammenfassung — keine Verweise auf die Schwesterseite für fehlende Inhalte.
- Im **RLP-Header** wird auf die Aufteilung hingewiesen: „Teil 1 von 2" bzw. „Teil 2 von 2". Die genannten RLP-Kompetenzen sind diejenigen, die auf der jeweiligen Sub-Seite tatsächlich abgedeckt werden (anteilig, nicht das ganze Bündel).
- **Zusatzmaterial getrennt pro Sub-Seite**: jede Sub-Seite hat ihren eigenen Ordner unter `downloads/<bereich>/<id>/` mit den vier Standard-Dateien (Handout, Anki-Deck, Teste dich selbst, Aufgabenserie). Damit bleibt jede Sub-Seite als eigene Lerneinheit selbsttragend.
- **Externe Ressourcen ebenfalls getrennt** und auf den Inhalt der Sub-Seite zugeschnitten.
- **Footer pro Sub-Seite** nennt den Sub-Themennamen (nicht den RLP-Sammeltitel): „Grundlagenfach 2.2a Lineare Gleichungen" für `g2-2a`, „Grundlagenfach 2.2b Quadratische Gleichungen" für `g2-2b` (Format gemäss §7).
- **Hinweis im RLP-Header (zwischen Themen-Titel und RLP-Kompetenz-Box)** explizit setzen: „RLP 2.2 · Teil 1 von 2" bzw. „RLP 2.2 · Teil 2 von 2". Bei nicht-gesplitteten Themenseiten erscheint dieser Hinweis **nicht**.
- Die **Lektionenangabe** im RLP-Header gibt die Lektionen des gesamten **Lerngebiets** an (z.B. „35 Lektionen" für alle Sub-Seiten in Lerngebiet 2, „50 Lektionen" für alle in Lerngebiet 5). Sie steht in der `<div class="pt-bereich">`-Zeile (Format: „Grundlagenfach · Lerngebiet X · &lt;Name&gt; · N Lektionen") und ist über alle Sub-Seiten desselben Lerngebiets identisch — auch für nicht gesplittete Themenseiten dieses Lerngebiets. Der Sub-Indikator („Teil 1 von 2" etc.) erscheint **getrennt** in der `<div class="pt-untertitel">`-Zeile darunter (Format: „RLP 2.2 · Teil 1 von 2"); siehe vorherige Regel. Diese Trennung wurde gewählt, weil die Lerngebiet-Lektionen für den Lernenden die nützlichere Orientierungsangabe sind (Gesamtgewicht des Lerngebiets im RLP) und sich der Sub-Split-Hinweis auf die RLP-Punkt-Ebene bezieht — die zwei Aussagen sind separierbar und lesen sich übersichtlicher in zwei Zeilen.
- **Praxisbeispiel-Seiten** (Dateiname-Präfix `gN-0-…` oder `sN-0-…`) sind Sonderfälle: sie tragen ein zusätzliches Suffix `· Praxisbeispiel` in der `pt-bereich`-Zeile (Beispiel: „Grundlagenfach · Lerngebiet 4 · Datenanalyse · 20 Lektionen · Praxisbeispiel"). Praxisbeispiel-Seiten sind keine RLP-Teilgebiete, sondern thematische Hüllen — siehe §6.1.1.
- **Index.html**: Sub-Seiten werden in einem gemeinsamen Sub-Container `<div class="ksub">` gerendert: ein Header mit der gemeinsamen RLP-Nummer und dem RLP-Sammeltitel (z.B. „2.2 Lineare und quadratische Gleichungen"), darunter die zwei Sub-Karten als 2-Spalten-Grid (`<div class="ksub-grid">`). So sieht man auf einen Blick, dass es sich um *ein* RLP-Teilgebiet handelt, ohne den Klick-Zugang zur einzelnen Sub-Seite zu verlieren.
- **Nav-Verkettung** läuft kontinuierlich durch: …→ 2.1 → 2.2a → 2.2b → 2.3 → … . Die Sub-Seiten kennen sich gegenseitig als prev/next.
- Die **Zählung der RLP-Teilgebiete** im Index (z.B. „3 Teilgebiete" für Lerngebiet 2) bleibt **unverändert** — die RLP-Struktur wird nicht angetastet, nur die interne Themenseiten-Aufteilung. In den Stats werden allerdings *Themenseiten* gezählt (also `2.2a` und `2.2b` getrennt), nicht RLP-Teilgebiete; der Hint unter den Stats macht diese Unterscheidung sichtbar.

**Wann sub-splitten und wann nicht:** Faustregel — zwei klar abgrenzbare didaktische Verfahren mit eigenen Animationen rechtfertigen einen Split. Reine Längenbedenken nicht; eine 1200-Zeilen-Seite zu einem geschlossenen Thema bleibt lesbar.

---

## 5. Visuelles Design

### 5.1 Farbsemantik (verbindlich, in `style.css` zentral definiert)

| Farbe | Bedeutung | Verwendung |
|---|---|---|
| 🔵 Blau | Definition, Theorie | `block-def`, „📘"-Blöcke |
| 🟢 Grün | Beispiel, Lösung | `block-bsp`, „🟢"-Blöcke |
| 🟠 Orange | Aufgabe, Übung | `block-aufg`, „🟠"-Blöcke |
| 🔴 Rot | Häufiger Fehler, Warnung | `block-fehler`, „⚠"-Blöcke |
| 🟣 Violett | Beweis, Herleitung | `block-beweis`, „🔷"-Blöcke |
| 🟢 Grün (Variante) | Tipp, Strategie, Hinweis | `block-tipp`, „💡"-Blöcke |
| 🔵 Blau (Variante) | Merksatz, Schlussfazit | `block-merksatz`, „⭐"-Blöcke |

Die Farben sind kapitelübergreifend identisch — das schafft ein konsistentes mentales Modell beim Schüler.

### 5.2 Bereichsfarben

- **Grundlagenfach:** Blau (`--blau`, `--blau-hell`)
- **Schwerpunktfach:** Violett (`--lila`, `--lila-hell`)

### 5.3 Schriften

- **Serif** (`Source Serif 4`): Überschriften, Titel
- **Sans** (`Source Sans 3`): Fliesstext
- **Mono** (`JetBrains Mono`): Code, Formeln in Live-Anzeigen, Slider-Werte, Chip-Labels

**Schriften werden lokal ausgeliefert (verbindlich seit 30.08.2026).** Jede Seite bindet
`schriften.css` relativ zur eigenen Tiefe ein, nie `fonts.googleapis.com`:

```html
<link rel="stylesheet" href="../schriften.css">   <!-- grundlagen/, schwerpunkt/ -->
<link rel="stylesheet" href="schriften.css">      <!-- Repo-Wurzel -->
```

Die Dateien liegen in `schriften/` (Fontsource 5.3.0, variable Schnitte, getrennt nach
latin / latin-ext / greek per `unicode-range`). Griechisch ist nötig: α, β, π, Σ, Ω
kommen ausserhalb von MathJax in SVG-Beschriftungen und Legenden vor. Neue Schriftschnitte
nur als vollständige Fontsource-Datei dazulegen, samt OFL-Lizenz.

### 5.3.1 Keine Drittanbieter (verbindlich seit 30.08.2026)

Eine Seite darf **keine Ressource von einem fremden Host laden**. Das betrifft heute
genau zwei Dinge, beide sind lokal:

| Ressource | lokal | früher |
|---|---|---|
| Schriften | `schriften.css` + `schriften/` | `fonts.googleapis.com` |
| Formelsatz | `vendor/mathjax/tex-svg.js` | `cdn.jsdelivr.net` |

Grund: Der Fussbereich sagt „Keine Cookies · Kein Tracking", und `rechtliches.html`
sagt es ausdrücklich zu. Jede fremde Ressource überträgt die IP-Adresse der Besucherin.

Zwei Fallstricke:

- **MathJax-Erweiterungen** werden relativ zum Pfad der Startdatei nachgeladen, und
  zwar erst beim Gebrauch. Ein fehlendes Stück fällt darum weder beim Laden noch im
  Pre-Flight auf — nur im Netzwerk-Tab als 404. Was dort liegen muss:
  `input/tex/extensions/boldsymbol.js` (alle Seiten setzen
  `loader: { load:['[tex]/boldsymbol'] }`), `input/mml.js` mit `input/mml/`, `a11y/`
  und `sre/mathmaps/` für die Sprachausgabe (der Explorer zieht den MathML-Eingang
  nach) und `output/chtml.js` mit `output/chtml/` für den Renderer-Wechsel. Geprüft
  wird das nur im Browser, nicht statisch.
- **Der Renderer-Wechsel muss funktionieren, nicht nur nicht abstürzen.** Rechtsklick
  auf eine Formel → *Math Settings → Math Renderer → CHTML*. Fehlt `output/chtml.js`,
  scheitert der Wechsel still — aber MathJax merkt sich die Wahl in `localStorage`
  (`MathJax-Menu-Settings`). Ab dem nächsten Seitenaufruf steht dann auf **allen**
  Seiten roher LaTeX-Quelltext statt Formeln, und weil es keine gerenderte Formel
  mehr gibt, kommt die Besucherin nicht einmal mehr ans Kontextmenü, um es
  zurückzustellen. Nur Site-Daten löschen hilft. Darum liegt CHTML bei: 610 kB im
  Repo, 0 Byte für alle, die nichts umstellen.
- **Vorlagen kopieren.** Eine alte Seite als Muster zu nehmen holt den CDN-Aufruf
  zurück. `TEMPLATE.html` ist umgestellt — von dort kopieren.

Der Pre-Flight prüft das (`check_keine_fremdhosts`) und meldet einen Treffer als
`[FEHLER]`. Verlinkte Videos und Aufgabensammlungen sind davon nicht betroffen: ein
`<a href>` lädt nichts, bevor jemand klickt. Eingebettete `<iframe>` zu fremden Hosts
sind nicht erlaubt.

Die Startseite `begreifbar.ch` liegt im eigenen Repo `go4exercises/begreifbar` und
trägt dort eine eigene, kleinere Schriftkopie.

### 5.4 Aufgaben-Nummerierung (verbindlich)

Zwei Stellen, an denen Aufgabennummern in Themenseiten erscheinen. Beide nutzen ausschliesslich Klassen aus `style.css`, **nicht** lokal in der Themenseite definieren.

**Aufgaben-Karten-Titel** (jede `block-aufg`-Karte hat einen Titel mit Aufgabennummer):

```html
<div class="block block-aufg">
  <div class="block-titel">🟠 <span class="aufg-nr-tag">A1</span><span class="aufg-titel-text">Hauptoperation erkennen</span></div>
  …
</div>
```

Die `aufg-nr-tag`-Pille ist orange (auf der orangen `block-aufg`-Hintergrundfarbe), monospace, kompakt. Der `aufg-titel-text`-Span enthält den eigentlichen Aufgabentitel; ein optionales `<span class="aufg-vertiefung">`-Pille darf am Ende stehen.

**Vertiefung steht am Ende der Reihe (verbindlich seit 29.09.2026).** Aufgaben mit der Pille «Vertiefung» kommen nach allen übrigen. Kommt später eine reguläre Aufgabe dazu, wird sie *vor* der Vertiefung eingereiht und die Vertiefung umnummeriert — mit allen IDs, `toggleL`-Argumenten und Prüffunktionen (so am 29./30.09.2026 auf `g2-2b` und `g2-3`: Vertiefung jetzt A10).

Verboten: das alte Muster `🟠 A1 — Hauptoperation erkennen` mit Spiegelstrich.

**Teil-Listen innerhalb einer Aufgabe** (mehrere nummerierte Teilaufgaben):

```html
<ol class="aufg-liste">
  <li>\(7 - 3 \cdot x\)</li>
  <li>\((x - 2) \cdot (x + 5)\)</li>
  …
</ol>
```

Die Klasse `aufg-liste` ersetzt das frühere `<ol style="margin:8px 0 0 22px">` mit Default-Marker. Die `1.`, `2.`, `3.` werden via CSS-Counter als kleine orange Pillen gerendert und stehen deutlich abgesetzt vom Listeninhalt. Funktioniert ohne JS, kein MathJax-Konflikt.

**Klassifizier-Term-Nummern** (`kl-spiel`-Widget; bisher nur in g1-1):

```html
<div class="kl-term"><span class="kl-nr">(1)</span>5+2·x</div>
```

`kl-nr` ist eine kleine neutrale Pille mit `margin-right:18px` zum Term.

### 5.5 Canvas-Animationen — technische Konventionen

Interaktive Animationen werden mit HTML5 Canvas und reinem JavaScript (kein Framework) umgesetzt. Folgende Konventionen sind verbindlich, weil sie sich über mehrere Iterationen als robust erwiesen haben.

#### 5.5.1 HiDPI-Rendering (Pflicht bei jeder neuen Canvas-Datei)

Auf Retina-/HiDPI-Displays werden Canvas-Inhalte unscharf gerendert, wenn der Buffer auf logische Pixel statt auf echte Display-Pixel angelegt wird. Standard-`initCv`-Funktion (in jeder Themenseite mit Canvas eigenständig vorhanden, gemeinsame Library möglich aber nicht zwingend):

```js
function initCv(id) {
  const cv = document.getElementById(id);
  if (!cv) return null;
  // Logische Zeichenfläche aus den initial gesetzten width/height-Attributen lesen
  if (!cv.dataset.logicalW) {
    cv.dataset.logicalW = cv.width;
    cv.dataset.logicalH = cv.height;
  }
  const W = +cv.dataset.logicalW;
  const H = +cv.dataset.logicalH;
  // Buffer-Auflösung an Display-Pixel-Ratio anpassen
  const dpr = window.devicePixelRatio || 1;
  const rect = cv.getBoundingClientRect();
  const cssW = rect.width  || W;
  const cssH = rect.height || H;
  const bufW = Math.max(1, Math.round(cssW * dpr));
  const bufH = Math.max(1, Math.round(cssH * dpr));
  if (cv.width !== bufW || cv.height !== bufH) {
    cv.width  = bufW;
    cv.height = bufH;
  }
  const ctx = cv.getContext('2d');
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.scale(bufW / W, bufH / H);
  ctx.clearRect(0, 0, W, H);
  return { ctx, W, H, cv };
}
```

**Konsequenzen für die Zeichnungs-Logik:**

- Alle Koordinaten arbeiten in **logischen Pixeln** (z.B. 0..560 × 0..440 für ein `<canvas width="560" height="440">`)
- `cv.width` / `cv.height` enthalten nach `initCv` die **physischen** Pixel — niemals direkt für Layout-Logik verwenden. Stattdessen `cv.dataset.logicalW` / `logicalH` (oder die `W`/`H` aus dem `initCv`-Rückgabewert) verwenden
- Bei Pointer-Events (Drag&Drop, Klick-Hit-Tests) muss `getBoundingClientRect()` mit der **logischen** Auflösung verglichen werden, nicht mit `cv.width`

#### 5.5.2 Helper für Winkelmarkierungen — Bisektrix-Formel

Die naive Formel für die Winkelhalbierende zwischen zwei Strahlen vom selben Vertex,

```js
let mid = (a1 + a2) / 2;  // FALSCH bei Branch-Cut von atan2
```

liefert das **falsche Ergebnis**, sobald die Strahlen den ±π-Branch-Cut von `atan2` überstreichen (z.B. ein Strahl bei +170°, der andere bei −170°: naive Mitte = 0°, korrekt wäre ±180°). Die robuste Formel arbeitet mit dem **signierten Winkel-Diff in (−π, π]**:

```js
const dSigned = ((a2 - a1 + Math.PI) % (2*Math.PI) + 2*Math.PI) % (2*Math.PI) - Math.PI;
const mid = a1 + dSigned / 2;
```

Die Helper-Funktion `drawAngleArc` in `grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html` (ab Anim 4) verwendet diese Formel. Bei jeder zukünftigen Winkelmarkierung diese Formel übernehmen, um Spiegelungs-Bugs zu vermeiden.

#### 5.5.3 Drag-&-Drop-Punkte (Pointer Events)

Für interaktive Eckpunkte (Maus + Touch in einer Implementierung) wird das **Pointer-Events-API** verwendet (`pointerdown` / `pointermove` / `pointerup` / `pointercancel` / `pointerleave`), nicht Maus- und Touch-Events separat. Wichtige Details:

- **`touch-action: none`** im CSS auf dem Canvas-Element setzen (verhindert Browser-Pinch/Scroll während Drag)
- **`setPointerCapture(ev.pointerId)`** beim `pointerdown` — der Pointer bleibt am Canvas gebunden, auch wenn er zwischendurch ausserhalb gleitet
- **Hit-Toleranz** grosszügig wählen (mind. 12–14 px), damit Touch-Bedienung funktioniert; sichtbarer Punkt-Radius kann kleiner sein (4–6 px ist ausreichend)
- **Visuelles Feedback**: Halo-Ring bei Hover/Drag macht die Hit-Area sichtbar
- **Cursor**: `grab` über aktivem Punkt, `grabbing` während Drag, sonst `default`

Vollständige Referenz-Implementierung in `grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html` (Anim 1, Funktion `strInitDrag` mit Helfern `canvasCoordsFromEvent`, `strHitTest`, `strClamp`).

#### 5.5.4 Skizzen-Geometrie für ganzzahlige Beispielwerte

Wenn eine Skizze ganzzahlige Werte zeigen soll (z.B. SA=2, SA'=4), aber abgeleitete Grössen (z.B. AB-Parallelenabschnitt) durch die Geometrie automatisch krumm würden, **kann die Geometrie selbst angepasst werden**, statt die Werte zu runden. Beispiel aus den Strahlensätzen:

- Nach Kosinussatz: \\(AB^2 = SA^2 + SB^2 - 2 \\cdot SA \\cdot SB \\cdot \\cos \\gamma\\)
- Wahl \\(\\cos \\gamma = 0{.}75\\) (statt z.B. 0.7) → für SA=2, SB=3 ergibt sich \\(AB^2 = 13 - 9 = 4\\) → AB = 2 (ganzzahlig)
- Strahl-Winkel symmetrisch zur Horizontalen: \\(\\pm \\gamma/2 \\approx \\pm 20.7°\\)

Solche „massgeschneiderten" Winkel sind didaktisch wertvoll und sollten Skizzen mit krummen Werten vorgezogen werden.

---

## 6. Datei-Naming und Struktur

```
TALS-Mathe/
├── index.html                              ← Übersichtsseite
├── style.css                               ← gemeinsames Stylesheet
├── nav.js                                  ← Navigation (sticky header + breadcrumb + ToC)
├── README.md
├── STYLEGUIDE.md                           ← diese Datei
├── TEMPLATE.html                           ← Vorlage für neue Themen
├── grundlagen/
│   ├── g1-arithmetik-algebra.html
│   ├── g2-gleichungen.html
│   ├── g3-1-funktionen-grundlagen.html
│   ├── g3-2-lineare-funktionen.html        ← Referenz-Implementierung
│   ├── g3-3-quadratische-funktionen.html
│   ├── g3-4-…
│   ├── g4-datenanalyse.html
│   └── g5-geometrie.html
├── schwerpunkt/
│   ├── s1-arithmetik.html
│   ├── s2-gleichungen.html
│   ├── s3-1-funktionen-grundlagen.html
│   ├── s3-2-polynome.html
│   ├── …
│   └── s4-geometrie.html
└── downloads/
    ├── README.md
    ├── print.css                              ← gemeinsames Druck-Stylesheet (A4)
    ├── diagram.js                             ← SVG-Helper für Achsenkreuze in Druckseiten
    ├── grundlagen/
    │   ├── g3-2-lineare-funktionen/
    │   │   ├── handout.html                   ← Druckseite (Theorie, ohne Beispiele/Aufgaben)
    │   │   ├── ankideck.apkg                  ← Anki-Karteikarten (Download)
    │   │   ├── teste-dich-selbst.html         ← Druckseite (Grundlagenaufgaben + Lösungen)
    │   │   └── aufgabenserie.html             ← Druckseite (Anwendungsaufgaben + Lösungen)
    │   └── …
    └── schwerpunkt/
        └── …
```

**Naming-Regeln:**
- Bereichs-Präfix: `g` für Grundlagen, `s` für Schwerpunkt
- Lerngebiet-Nummer: `g3-2` = Grundlagen, Lerngebiet 3 (Funktionen), Thema 2 (Lineare)
- **Sub-Split** (siehe 4.1): Buchstaben-Suffixe `a`, `b`, `c` direkt an die RLP-Nummer angehängt — `g2-2a`, `g2-2b`. Die Schwesterseiten teilen das gemeinsame Numerik-Präfix (`g2-2`), unterscheiden sich nur im Suffix.
- **Seite ohne eigene RLP-Nummer** (seit 15.09.2026, bisher nur `g2-modellieren.html`): Sie
  bündelt Stoff mehrerer Teilgebiete eines Lerngebiets. Dateiname `g<lerngebiet>-<thema>.html`
  ohne Teilgebiet-Nummer; in `nav.js` `id:'g2-M'`, `nr:'2.M'`, eingereiht nach dem letzten
  Teilgebiet des Lerngebiets; `pt-untertitel` nennt die bedienten RLP-Punkte
  («Vertiefung zu RLP 2.1 und 2.3»). Clip-Dateinamen folgen dem nav-Code (`g2-M-…`).
- Dateinamen kleingeschrieben, mit Bindestrichen, ohne Umlaute (`-funktionen.html`, nicht `_Funktionen.html`)
- **Druckseiten-Dateinamen** sind über alle Themen hinweg identisch: `handout.html`, `teste-dich-selbst.html`, `aufgabenserie.html` (plus `ankideck.apkg`). Das erleichtert Verlinkung, Kopiervorlagen und Suche.

---

## 6.1 HTML-Skelett für Themenseiten (verbindlich)

Direkt nach dem `<title>` steht der **generierte** SEO-Block, begrenzt von den
Marken `SEO:ANFANG` und `SEO:ENDE` (Beschreibung, `canonical`, Favicons, Open
Graph, JSON-LD nach schema.org/LearningResource). Er wird nie von Hand bearbeitet,
sondern von `scripts/build-seo.py` geschrieben; eine neue Seite muss dort in der
Tabelle `SEITEN` eingetragen werden, sonst bleibt sie ohne Beschreibung und ohne
Sitemap-Eintrag.

Jede Themenseite verwendet **exakt** die folgende Body-Struktur. Abweichungen (eigene Wrapper-Klassen, hardcoded TOC, semantische `<section>`-Tags um die h2-Sektionen, abweichende `buildNav`-Signatur) brechen das CSS-Grid-Layout `.page-wrap` und/oder die Navigation und sind verboten.

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>⟪RLP-Nr⟫ ⟪Themenname⟫ — Mathe begreifbar</title>
  <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:..." rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
  <script>
  MathJax = {
    tex: { inlineMath: [['\(','\)']], displayMath: [['\[','\]']] },
    svg: { fontCache: 'global', scale: 1.0 }
  };
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
  <!-- ggf. seitenspezifisches <style>…</style> hier -->
</head>
<body>
<div id="nav-root"></div>
<div class="page-wrap">
<main class="content">

  <div class="page-titel">
    <div class="pt-bereich">⟪Bereich⟫ · Lerngebiet ⟪n⟫ · ⟪Lerngebiet-Name⟫ · ⟪L⟫ Lektionen</div>
    <h1 class="pt-h1">⟪RLP-Nr⟫ ⟪Themenname⟫</h1>
  </div>

  <p class="lead">⟪Lead-Absatz⟫</p>

  <div class="rlp-kompetenzen">
    <div class="rlp-titel">📋 Kompetenzen nach RLP 2030 — Teilgebiet ⟪RLP-Nr⟫</div>
    <ul>
      <li>⟪Kompetenz⟫ <span class="ohm">auch ohne Hilfsmittel</span></li>
    </ul>
  </div>

  <h2 id="einstieg">Einstieg — ⟪Titel⟫</h2>
  <!-- … weitere h2-Abschnitte gemäss Master-Schema, jeweils mit id="…" direkt am h2 … -->
  <h2 id="ressourcen">Externe Videos &amp; Aufgabensammlungen</h2>
  <!-- … -->

</main>
<aside class="toc-wrap"><div id="toc"></div></aside>
</div>

<footer class="site-footer">
  <p><strong>Mathe begreifbar</strong> — Lernmaterial für die Berufsmaturität Technik, Architektur, Life Sciences</p>
  <p>⟪Bereich⟫ ⟪RLP-Nr⟫ ⟪Themenname⟫</p>
</footer>

<script src="../nav.js"></script>
<script src="../mathlib.js"></script>
<script>
buildNav({
  bereich:'grundlagen', id:'g⟪RLP⟫',
  kapitelNr:'⟪RLP-Nr⟫', kapitelTitel:'⟪Themenname⟫',
  prev:{nr:'⟪prev⟫',titel:'⟪prev-titel⟫',url:'⟪prev⟫.html'},
  next:{nr:'⟪next⟫',titel:'⟪next-titel⟫',url:'⟪next⟫.html'}
});
</script>

</body>
</html>
```

**Verbindlich (nicht verhandelbar):**

| Regel | Warum |
|---|---|
| **Genau diese Container-Hierarchie:** `body > div#nav-root > div.page-wrap > main.content` und parallel `aside.toc-wrap` *als Geschwister von `main`*, beide innerhalb von `.page-wrap`. | `.page-wrap` ist das CSS-Grid mit `grid-template-areas: "content toc"`. Ohne `.page-wrap` oder mit `<aside>` *vor* `<main>` greift das Grid nicht — Sidebar und Inhalt überlappen. |
| **`<main class="content">`** — *nicht* `class="inhalt"` oder ähnlich. | CSS-Selektor `.content` definiert das gesamte Typographie-Stack der Themenseite. |
| **TOC als leerer Container `<aside class="toc-wrap"><div id="toc"></div></aside>`**, keine hardcoded TOC-Liste. | nav.js generiert die TOC dynamisch aus den `<h2 id="…">` und hält sie sticky. Eine handgeschriebene TOC bleibt veraltet. |
| **`<h2 id="…">…</h2>`** — IDs *direkt* an den h2, **nicht** an einem `<section>`-Wrapper. | Konsistenz aller 32 Seiten; Sticky-Highlight in nav.js orientiert sich an h2-IDs. Keine `<section>`-Wrapper rund um Abschnitte. |
| **`<script src="../nav.js"></script>` ohne `defer`** — direkt vor dem `buildNav()`-Inline-Script am Ende des Body. | Mit `defer` läuft nav.js *nach* dem Inline-Aufruf. `buildNav` ist dann undefined, Navigation und TOC fehlen komplett. |
| **`<script src="../mathlib.js"></script>` direkt nach `nav.js`** — auch wenn die Seite (scheinbar) keine mathlib-Funktion nutzt. | `toggleL` (Lösungs-Aufklapp-Mechanismus) lebt in `mathlib.js`. Fehlt das Skript, klappen die Lösungen ohne Konsole-Hinweis nicht auf — der User sieht nur, dass der Klick nichts tut. Auch `fmt`, `parseL` u.a. werden gerne ad-hoc gebraucht. |
| **`buildNav()`-Signatur:** `{ bereich, id, kapitelNr, kapitelTitel, prev, next }`. | Die einzige API von nav.js. Falsche Signaturen (`{current: {…}}` o.ä.) führen zu stillen Fehlern. |
| **Footer:** `<footer class="site-footer">` mit zwei `<p>` (siehe § 7). | Konsistente Fusszeile über alle Seiten. |

**Zusatzmaterial-Sektion (Pflicht-Konvention):**

```html
<h2 id="downloads">Zusatzmaterial</h2>

<p>Zum Ausdrucken und Mitnehmen — Theorie, Formelsammlung, Karteikarten und Aufgaben mit Lösungen.</p>

<div class="dl-grid">
  <a href="../downloads/grundlagen/⟪slug⟫/handout.html" target="_blank" rel="noopener" class="dl"><span class="dl-ic">📄</span><div><div class="dl-t">Handout</div><div class="dl-s">Theorie-Zusammenfassung</div><div class="dl-fmt">Druckseite</div></div></a>
  <a href="../downloads/grundlagen/⟪slug⟫/teste-dich-selbst.html" target="_blank" rel="noopener" class="dl"><span class="dl-ic">✅</span><div><div class="dl-t">Teste dich selbst</div><div class="dl-s">Grundlagenaufgaben mit Lösungen</div><div class="dl-fmt">Druckseite</div></div></a>
  <a href="../downloads/grundlagen/⟪slug⟫/aufgabenserie.html" target="_blank" rel="noopener" class="dl"><span class="dl-ic">🧩</span><div><div class="dl-t">Aufgabenserie</div><div class="dl-s">Anwendungsaufgaben mit Lösungen</div><div class="dl-fmt">Druckseite</div></div></a>
  <a href="../downloads/grundlagen/⟪slug⟫/ankideck.apkg" class="dl"><span class="dl-ic">🃏</span><div><div class="dl-t">Anki-Deck</div><div class="dl-s">Karteikarten zum Auswendiglernen</div><div class="dl-fmt">APKG</div></div></a>
</div>
```

Container ist `.dl-grid` (nicht `dl-box`, das existiert nicht). Jede Karte ist `<a class="dl">` mit Icon-Span, Titel-Div und Sub-Div. Reihenfolge ist fix: Handout → Teste dich selbst → Aufgabenserie → Anki-Deck. Optionale 6. Karte für „Zusatz: …" über RLP hinaus erlaubt — sie steht am Ende des Grids (nach dem Anki-Deck).

**Externe-Ressourcen-Sektion (Pflicht-Konvention):**

```html
<h2 id="ressourcen">Externe Videos &amp; Aufgabensammlungen</h2>

<div class="ressourcen-subtitel">🎬 Erklärvideos (Playlists)</div>
<div class="links-grid">
  <a href="…" target="_blank" rel="noopener" class="lk"><span class="lk-ic">▶️</span><div><div class="lk-t">Titel</div><div class="lk-s">Quelle · kurze Beschreibung</div></div></a>
  …
</div>

<div class="ressourcen-subtitel" style="margin-top:18px">📝 Aufgabensammlungen</div>
<div class="links-grid">
  <a href="…" target="_blank" rel="noopener" class="lk aufg"><span class="lk-ic">📝</span><div><div class="lk-t">Titel</div><div class="lk-s">Quelle · Beschreibung</div></div></a>
  …
</div>
```

Container ist `.links-grid` (nicht `ressourcen-grid`, das existiert nicht). Jeder Link ist `<a class="lk">` für Videos (▶️, roter Hover) oder `<a class="lk aufg">` für Aufgabensammlungen (📝, oranger Hover). Innere Struktur: ein `<span class="lk-ic">` + ein verschachteltes `<div>` mit `<div class="lk-t">` (Titel) und `<div class="lk-s">` (Sub-Zeile, hier konvergieren Quelle und Beschreibung mit `·`-Trenner).

**Pre-Flight-Check vor Commit** (Bash-Schnipsel, kopierbar):

```bash
for f in grundlagen/g*.html schwerpunkt/s*.html; do
  pw=$(grep -c "page-wrap" "$f")
  mc=$(grep -c 'main class="content"' "$f")
  navjs=$(grep -c 'src="../nav.js">' "$f")
  navdef=$(grep -c 'src="../nav.js" defer' "$f")
  ml=$(grep -c 'src="../mathlib.js"' "$f")
  bn=$(grep -cE 'buildNav\(\{[[:space:]]*$|buildNav\(\{ bereich' "$f")
  sec=$(grep -cE '<section\b' "$f")
  # Klassen-Check: Phantom-Klassen, die im CSS nicht existieren
  bad=$(grep -cE 'class="(inhalt|brot|seiten-kopf|rlp\b|rlp-list|rlp-label|seiten-fuss|dl-box|ressourcen-grid|ress|ress-titel|ress-beschr|ress-quelle)"' "$f")
  # Skript-Konsistenz: wenn loesung-toggle benutzt, MUSS mathlib.js eingebunden sein
  togL=$(grep -c 'class="loesung-toggle"' "$f")
  if [ "$togL" != "0" ] && [ "$ml" = "0" ]; then mlw="MATHLIB-FEHLT!"; else mlw="ok"; fi
  printf "%-50s pw=%s mc=%s nav=%s def=%s ml=%s bn=%s sec=%s bad=%s tog=%s/%s\n" "$f" "$pw" "$mc" "$navjs" "$navdef" "$ml" "$bn" "$sec" "$bad" "$togL" "$mlw"
done
```

Erwartete Werte: `pw=1 mc=1 nav=1 def=0 ml=1 bn=1 sec=0 bad=0` und `tog=N/ok` (N = beliebige Anzahl Toggles, `ok` = mathlib.js eingebunden). Jede Phantom-Klasse (im Klassen-Check) zeigt eine eigenkreierte Klasse an, die nicht im CSS existiert — Layout bricht entsprechend stillschweigend. `MATHLIB-FEHLT!` zeigt eine Seite, die `toggleL` aufruft, aber `mathlib.js` nicht lädt — Lösungen klappen ohne Konsole-Hinweis nicht auf.

---

## 6.1.1 Praxisbeispiel-Seiten (Sonderfall des Skeletts)

Praxisbeispiel-Seiten sind thematische Hüllen, die einem ganzen Lerngebiet ein konkretes, durchgehendes Anwendungs-Beispiel zur Seite stellen (z.B. eine BM2-Klasse als Datensatz für alle Themen aus Lerngebiet 4). Sie sind **keine RLP-Teilgebiete** und folgen einem reduzierten Skelett.

**Erkennungsmerkmal** ist der Dateiname-Präfix `gN-0-…` (Grundlagenfach) oder `sN-0-…` (Schwerpunktfach) — die `0`-Position kollidiert nie mit RLP-Teilgebiet-Nummern, die ab `1` zählen.

**Erlaubte Abweichungen vom Standard-Skelett:**

| Element | Standard-Themenseite | Praxisbeispiel-Seite |
|---|---|---|
| `pt-bereich`-Suffix | Endet mit Lektionenzahl | Zusätzlich `· Praxisbeispiel` am Ende |
| `<div class="rlp-kompetenzen">` | Pflicht | **Entfällt** (kein RLP-Teilgebiet) |
| `<h2 id="aufgaben">` | Pflicht | **Entfällt** (Aufgaben stehen auf den verlinkten Themenseiten) |
| `<h2 id="downloads">` | Pflicht | **Entfällt** |
| `<h2 id="ressourcen">` | Pflicht | **Entfällt** |
| Merksatz-Block | Üblich | Entfällt typischerweise |

**Pflicht bleibt** weiterhin: HTML-Skelett (`page-wrap`/`main.content`/`nav.js`/`mathlib.js`/`buildNav`), `pt-bereich`, `pt-h1`, `<p class="lead">`, `<h2 id="einstieg">`, Footer.

**Erkennbar bleiben muss** im `pt-bereich`, dass es sich um ein Praxisbeispiel handelt (Suffix `· Praxisbeispiel`). Damit weiss die Lernende sofort, dass diese Seite die Themen-Anwendung zeigt, nicht ein eigenständiges Lerngebiet.

Aktuell ist `g4-0-praxisbeispiel-bm2-klasse.html` die einzige Praxisbeispiel-Seite im Lehrmittel. Beim Anlegen weiterer (z.B. `s2-0-…` für ein Schwerpunkt-Anwendungsbeispiel) gelten dieselben Regeln.

---

## 6.2 Reservierte Top-Level-Identifier (kollidieren mit `mathlib.js` / `nav.js`)

Themenseiten binden `nav.js` und `mathlib.js` als geteilte Bibliotheken ein. Beide deklarieren mehrere Symbole im globalen Scope. Wenn Inline-Skripte einer Themenseite ein Symbol mit demselben Namen erneut deklarieren, ist das Verhalten je nach Deklarationsart unterschiedlich:

- **`const`, `let`, `class`** → harter `SyntaxError: Identifier '...' has already been declared` beim Parsen. Das **gesamte** weitere Inline-Skript wird nicht ausgeführt. Effekt: alle Animationen blank, Console rot, isolierter `node --check` der Themenseite findet's nicht (Kollision entsteht erst beim kombinierten Laden).
- **`function`, `var`** → keine Fehlermeldung, die zweite Definition überschreibt die erste. Funktioniert technisch, ist aber unsauber und ein versteckter Stolperstein für die nächste Person, die `mathlib.toggleL()` aufruft und plötzlich anderes Verhalten bekommt.

**Aus `mathlib.js` reserviert:**

| Symbol | Typ | Zweck |
|---|---|---|
| `fmt` | `const` | Zahlen-Formatierer (0, ganzzahlig, sonst eine Nachkommastelle) |
| `fmtS` | `const` | Vorzeichen-Term mit Unicode-Minus |
| `fmtMx` | `const` | Matrix-Formatierer |
| `fmtAffine` | `const` | Affine Abbildung als String |
| `parseL` | `function` | Term-Parser für Aufgaben |
| `toggleL` | `function` | Lösungs-Toggle |
| `initCanvas` | `function` | Canvas-Initialisierung mit DPR |
| `drawGrid` | `function` | Achsenraster zeichnen |
| `drawLine` | `function` | Linie mit logischen Koordinaten |
| `drawDot` | `function` | Punkt mit logischen Koordinaten |
| `intervallKlammer` | `function` | Intervallgrenze als Klammer (§2.7) |
| `flTex`, `flHtml`, `flTeil`, `flOffen` | `function`/`const` | Eine Rechnung, eine Zeile (§2.12) |
| `texE` | `const` | Zahl mit Einheit in LaTeX (§2.12) |

**Aus `nav.js` reserviert:**

| Symbol | Typ | Zweck |
|---|---|---|
| `SITE` | `const` | Komplette Themenseiten-Hierarchie |
| `GROUPS` | `const` | Bereich-Gruppierung für Header |
| `TOC_KURZ` | `const` | Kurz-Labels für Standard-Sektionen |
| `buildNav` | `function` | Header und Breadcrumb einsetzen |
| `buildToC` | `function` | Sticky ToC aufbauen |
| `toggleDD` | `function` | Dropdown-Menü-Toggle |
| `toggleMobileNav` | `function` | Mobile-Nav-Toggle |

**Vermeiden in Inline-Skripten von Themenseiten:**
- **`const`/`let`/`class` mit reserviertem Namen auf Top-Level redeklarieren** ist verboten — bricht die ganze Seite. Lokal innerhalb einer Funktion (`function foo() { const fmt = ...; }`) ist okay, das ist Block-Scope.
- **`function`/`var` mit reserviertem Namen redeklarieren** ist erlaubt, aber zu vermeiden — wenn andere Codestellen die mathlib-Variante des Symbols erwarten, bekommen sie deine Ersatz-Implementierung. Stattdessen unter eigenem Namensraum ablegen (`const Anim = { fmt: ..., draw: ... }`), oder lokal in einer IIFE.
- **Keine griechischen Unicode-Buchstaben als Identifier** (`const α = ...`). Sprachspezifikation erlaubt sie, Browser-Engines sind aber inkonsistent — vor allem bei Misch-Identifiern wie `αs`. Stattdessen `alpha`, `beta`, `gamma`, `alphaS` etc. verwenden. Strings für die Anzeige (`txt(ctx, x, y, 'α', ...)`) bleiben unverändert.

**Pre-Flight-Erweiterung — Kollisions-Check:**

```python
# scripts/check_identifier_collisions.py
import re
from pathlib import Path

reserved = {'fmt', 'fmtS', 'fmtMx', 'fmtAffine', 'parseL', 'toggleL',
            'initCanvas', 'drawGrid', 'drawLine', 'drawDot',
            'SITE', 'GROUPS', 'TOC_KURZ',
            'buildNav', 'buildToC', 'toggleDD', 'toggleMobileNav'}

def find_top_level_decls(js):
    """Findet const/let/var/function/class-Deklarationen NUR auf Top-Level
    (Klammertiefe = 0, Strings/Kommentare ausgeschlossen)."""
    decls, depth, i = [], 0, 0
    in_s = in_d = in_b = in_lc = in_bc = False
    line_start = True
    while i < len(js):
        c = js[i]; nxt = js[i+1] if i+1 < len(js) else ''
        if in_lc:
            if c == '\n': in_lc = False; line_start = True
            i += 1; continue
        if in_bc:
            if c == '*' and nxt == '/': in_bc = False; i += 2; continue
            i += 1; continue
        if in_s:
            if c == '\\': i += 2; continue
            if c == "'": in_s = False
            i += 1; continue
        if in_d:
            if c == '\\': i += 2; continue
            if c == '"': in_d = False
            i += 1; continue
        if in_b:
            if c == '\\': i += 2; continue
            if c == '`': in_b = False
            i += 1; continue
        if c == '/' and nxt == '/': in_lc = True; i += 2; continue
        if c == '/' and nxt == '*': in_bc = True; i += 2; continue
        if c == "'": in_s = True; i += 1; continue
        if c == '"': in_d = True; i += 1; continue
        if c == '`': in_b = True; i += 1; continue
        if c in '{[(': depth += 1
        if c in '}])': depth -= 1
        if c == '\n': line_start = True; i += 1; continue
        if line_start and depth == 0:
            if c in ' \t': i += 1; continue
            m = re.match(r'(const|let|var|function|class)\s+(\w+)', js[i:])
            if m: decls.append((m.group(2), m.group(1)))
            line_start = False
        i += 1
    return decls

hard = []  # const/let/class → harter Fehler
soft = []  # function/var → unsauber, überlebt
for f in sorted(Path('.').rglob('*.html')):
    html = f.read_text()
    for s in re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', html, re.DOTALL):
        for name, kind in find_top_level_decls(s):
            if name in reserved:
                (hard if kind in ('const', 'let', 'class') else soft).append((str(f), name, kind))

if hard:
    print("BLOCKIEREND (Seite bricht):")
    for f, n, k in hard: print(f"  ⛔ {f}: {k} {n}")
if soft:
    print("AUFRÄUMEN (unsauber, läuft aber):")
    for f, n, k in soft: print(f"  ⚠  {f}: {k} {n}")
if not (hard or soft):
    print("✓ Keine Kollisionen")
```

Erwartet im sauberen Repo: keine Ausgabe. Eine `⛔`-Meldung blockiert die betroffene Seite komplett (alle Inline-JS-Funktionen nicht definiert); `⚠` ist tolerierbar, sollte aber bei nächster Berührung der Seite saubergezogen werden.

---

## 6.3 Werkzeug-Skripte für Konventions-Erzwingung

Unter `scripts/_archiv/` liegen mehrere Python-Skripte, die bei der Massen-Bereinigung des Lehrmittels nach Konventions-Updates **wiederverwendbar** sind. Sie haben ihren Zweck erfüllt und liegen darum im Archiv — für einen erneuten Migrationslauf sind sie unverändert brauchbar. Besonders relevant bei der Schwerpunktfach-Ausarbeitung (s1–s4), wenn neue Inhalte aus externen Vorlagen übernommen werden, die typische deutsche Konventionen mitbringen (Dezimalkomma, ß, „Kosinus").

Alle vier `convert_*.py`-Skripte folgen dem gleichen Aufbau:
- Schutzlogik (protect_regions): URLs, `<script>`, `<style>`, `<svg>`, SVG-Attribute werden vor der Ersetzung ausmaskiert
- Dry-Run-Modus möglich (Aufruf-Argument `--dry-run`)
- Diff-Ausgabe pro veränderte Datei (zur Inspektion)
- Verifikations-Funktion `verify_no_residuals(filepath)` für nachgelagerte Checks

### 6.3.1 `scripts/_archiv/convert_decimals.py` — Dezimalkomma → Dezimalpunkt

**Zweck:** Massenkonversion aller Klartext- und MathJax-Dezimalkommas auf Dezimalpunkte (gemäss §2.4 dieses Styleguides).

**Strategie:** Behält Funktionskommas in `f(1, 2)` etc. bei. Greift nur auf Muster `[0-9],[0-9]` zu, schützt zuvor `<style>`, `<svg>`, Google-Fonts-URLs, SVG-Attribute (`d/points/viewBox/transform`). In `<script>`-Blöcken werden nur eindeutige MathJax-Dezimal-Strings (`[0-9]{,}[0-9]`) ersetzt.

**Bietet auch:** `verify_no_residuals(filepath)` — liefert ein Dictionary mit eventuellen Rest-Funden (für Verifikations-Loops nach Massenpatches).

```bash
python3 scripts/_archiv/convert_decimals.py            # echte Konversion
python3 scripts/_archiv/convert_decimals.py --dry-run  # nur Diff anzeigen
```

### 6.3.2 `scripts/_archiv/convert_eszett.py` — ß → ss

**Zweck:** Schweizer Hochdeutsch ohne ß (gemäss §2.5). Variante A: auch Eigennamen (`Gauß-Algorithmus → Gauss-Algorithmus`).

**Geltungsbereich:** alle HTML-Lehrmittel-Dateien (grundlagen/, downloads/, schwerpunkt/, index, TEMPLATE). **KEINE** Markdown-Dokumentation — dort sind ß in Meta-Erwähnungen der Regel selbst legitim.

**Schutz:** ß-Vorkommen in `<style>`, `<svg>`, SVG-Attributen werden nicht angetastet (defensiv — kommt in der Praxis nicht vor).

### 6.3.3 `scripts/_archiv/convert_cosinus.py` — Kosinus → Cosinus

**Zweck:** Schweizer Konvention (gemäss §2.5). Ersetzt case-erhaltend (`Kosinus` → `Cosinus`, `kosinus` → `cosinus`).

**Schutz:** URLs (`href`/`src`), `<script>`, `<style>`, `<svg>`, SVG-Attribute werden ausmaskiert. Externe Serlo-Links mit `kosinus` im URL-Pfad bleiben so erhalten.

### 6.3.4 `scripts/_archiv/convert_punktkoord.py` — Punkt-Koordinaten `(x, y)` → `(x | y)`

**Zweck:** FTB-Notation für Punkt-Koordinaten (gemäss §2.4: `P(x \mid y)`).

**Strategie:** Pro Datei eine handgepflegte Liste von alt→neu-Replacements. Das vermeidet Falsch-Positiva in Datenwert-Aufzählungen wie „2 Werte (158, 162)" in Statistik-Übungen. **Beim Übernehmen für Schwerpunktfach-Seiten** muss die `REPLACEMENTS`-Liste pro neuer Seite manuell um die identifizierten Stellen erweitert werden — die Skript-Struktur ist als Template gedacht.

### 6.3.5 Empfohlene Reihenfolge bei einer neuen Seitenfamilie (z.B. s1–s4)

Nach Erstellung der neuen Themenseiten und vor Pre-Flight-Check:

```bash
python3 scripts/_archiv/convert_eszett.py        # ß → ss
python3 scripts/_archiv/convert_cosinus.py       # Kosinus → Cosinus
python3 scripts/_archiv/convert_decimals.py      # Dezimalkomma → Dezimalpunkt
# convert_punktkoord.py NUR ausführen, wenn die REPLACEMENTS-Liste für die neuen
# Seiten manuell ergänzt wurde (sonst sinnlos, da hartkodiert).
python3 scripts/check_identifier_collisions.py
```

Anschliessend Pre-Flight-Check aus §6.1 fahren.

### 6.3.6 Verifikations-Loop nach Massenpatches

Nach jedem Skript-Lauf sollte global geprüft werden, ob keine Residuen oder Strays übrig sind. Standard-Snippet (in mehreren Sessions bewährt):

```python
import glob, sys
sys.path.insert(0, 'scripts')
import convert_decimals as cd

files = sorted(glob.glob('grundlagen/*.html') +
               glob.glob('downloads/grundlagen/**/*.html', recursive=True) +
               glob.glob('schwerpunkt/*.html'))
strays = sum(1 for fp in files if '\x00' in open(fp).read() or '\x01' in open(fp).read())
residue = sum(1 for fp in files if any(cd.verify_no_residuals(fp).values()))
total_ss = sum(open(fp).read().count('ß') for fp in files)
print(f"Stray: {strays} | Residuen: {residue} | ß: {total_ss}")
```

Erwartet: `Stray: 0 | Residuen: 0 | ß: 0`. Jede Abweichung muss vor dem nächsten Schritt behoben werden.

---

## 6.4 Clips (verbindlich seit 30.08.2026)

Ein Clip ist eine HTML-Animation in `clips/`, kein Video: Die Bühne baut einen
Gedankengang Zeile für Zeile auf, dazu läuft eine gesprochene Spur. Ausführlich in
`HOWTO-clips.md`; hier nur, was nicht verhandelbar ist. Stand 08.10.2026: 391 Clips in
`clips.json` (363:01 min, davon 223 Animationsclips), dazu 195 mit `"probe": true` — 160 Clips der
Leitprogramme nach Thema (die 150 der sichtbaren in `clips.html` in der Spalte «Leitprogramm») und 35 Prüfungsclips.

- **`clips/` liegt genau eine Ebene unter der Wurzel.** Die Clips ziehen die Schriften per
  `@import url("../schriften.css")`. Tiefer verschoben sind die Schriften weg, ohne dass
  etwas bricht — die Bühne fällt still auf Georgia zurück.
- **Dateiname `<lektion>-<kurzname>`**, passend zum Schema der Themenseiten.
- **Von Hand geschrieben wird nur das Drehbuch** (`clips/<name>.json`). `.html`,
  `sprechertext-*.txt` und `clips.json` erzeugt `scripts/build-clips.py` und werden
  mitversioniert — GitHub Pages baut nichts.
- **Formeln stehen in LaTeX**, gesetzt von MathJax — dieselbe Schreibweise wie auf den
  Seiten. Damit lässt sich eine Formel von der Lektionsseite ins Drehbuch kopieren,
  statt sie in eine zweite Schreibweise zu übersetzen; jede Übersetzung war eine
  Gelegenheit für einen Fehler. Prosa in einer Formelzeile braucht `\text{…}`, und
  zwar **ein** `\text{}` um den ganzen Satz.
- **Der Ton ist eine Zutat, keine Voraussetzung.** Ohne Tonspur läuft der Clip
  unverändert. Gesprochen wird der Sprechertext des Drehbuchs; er wird nicht
  nachträglich umgeschrieben, ohne die Spur neu zu bauen — sonst sagen Bild und Ton
  Verschiedenes. Die Dauern im Drehbuch stammen aus der Messung
  (`scripts/build-clip-ton.py` **vor** `build-clips.py`).
- **`lektion` ist eine Liste**, auch bei einem Eintrag. Ein Clip gehört oft auf mehrere
  Seiten; ohne Liste müsste man ihn duplizieren, und zwei Kopien laufen auseinander.
  Jeder Code muss einer `id` in `nav.js` entsprechen — der Pre-Flight prüft das.
  **Der erste Code ist die Heimatlektion:** Dort steht der Clip in seiner Reihe, auf den
  übrigen Seiten hängt er als Gast hinten an.
- **Kein `<iframe>` beim Seitenaufruf.** In der Seite steht nur die Startkarte, erst der
  Klick setzt den Rahmen ein (`clipStart` in `mathlib.js`). Sonst laufen bei mehreren
  Clips alle gleichzeitig los und die Seite lädt N zusätzliche Dokumente mit.
- **Transkript ist Pflicht.** Von einer Animation sieht eine Suchmaschine nichts, und die
  Volltextsuche ebenso wenig. Klasse `clip-transkript` — die darf **nicht** in
  `SKIP_CLASSES` von `scripts/build-suchindex.py` landen.
- **Farbe im Clip bedeutet etwas anderes als auf der Seite.** `{1:…}` bis `{4:…}` verfolgen
  einen *Term* über mehrere Zeilen, nicht einen Blocktyp. Dass Orange auf den Seiten
  „Aufgabe" markiert (§5.1), gilt hier nicht — anderer Kontext. 1 und 2 (Blau/Orange) sind
  das Paar, das auch bei Rotgrünschwäche unterscheidbar bleibt. Sparsam einsetzen.
- **Die Bibliothek `clips.html` zeigt je Themenseite drei Spalten** (seit 06.10.2026):
  **Animationen** (Clips mit `animation`, «Anim»), **Leitprogramm** (die eigenen Clips der
  sichtbaren Leitprogramme, in deren Reihenfolge, «LP» auf die Animation des Kapitels) und
  **Weitere Clips**. Gebaut von `scripts/clips_bibliothek.py`. Die Themenseiten stehen in der
  Reihenfolge des Menüs (aus `nav.js` gelesen, nicht wiederholt); in den Spalten 1 und 3
  ordnet `ordnung()` in `build-clips-einbau.py`: die Reihe (`REIHEN_VORN` + `REIHEN`, wo die
  Folge dem Aufbau der Seite statt dem Alphabet folgt), dann `folge`. Der Zweig ordnet
  **nicht** mit. Farben: Bereichsfarbe (GF blau, SP violett), Spalte 1 hinterlegt, Spalte 2
  heller hinterlegt, Spalte 3 weiss — kein Orange oder Bernstein. Einzelheiten:
  HOWTO-clips «Bibliotheksseite».
- **Werkzeug-Clips: `"werkzeug": true` im Drehbuch, sonst nichts Besonderes.** Ein
  Taschenrechner-Clip bekommt **keine eigene Reihe** — er steht in der Reihe seines
  Stoffs, als deren letzter: der poly-solv-Clip als Folge 7 der `Quadratische
  Gleichungen`, der sys-solv-Clip als Folge 6 der `Gleichungssysteme`. Das Flag macht
  genau zwei Dinge: Es sortiert den Clip ans Ende seiner Reihe (`ordnung()`) und gibt
  der Zeile `cl-tr` statt `cl-r1…8` — auf den Themenseiten Orange, in beiden Bereichen
  dieselbe Farbe, weil sie gerade *nicht* zur Bereichsfamilie gehören soll (Ausnahme von
  §5.1, in `style.css` vermerkt). In `clips.html` stechen sie als dunkle Zeile mit Marke
  «TR» heraus.
- **Auch der Titel wiederholt das Werkzeug nicht.** Er beginnt wie jeder Clip mit seiner
  Reihe: «Quadratische Gleichungen: mit poly-solv lösen», nicht «Taschenrechner: …».
  Sonst steht in der Bibliothek eine Spalte gleich anfangender Titel, die nichts über
  den Stoff sagt.
- **Was die Rechnung voraussetzt, bleibt sichtbar.** Wird eine Bedingung genannt und
  später gebraucht — Definitionsmenge, \(a \neq 0\), Leitkoeffizient 1 —, gehört sie in die
  Bedingungsleiste (`voraussetzung` im Drehbuch). Sie steht ausserhalb des Szenenflusses
  und kostet keine Zeile. Nicht in die Leiste gehört eine Bedingung, die das *Ergebnis*
  des Clips ist: Sie nähme die Frage vorweg.
- **`"probe": true` hält einen Clip aus der Bibliothek heraus.** Er wird gebaut und
  ausgeliefert, kommt aber nicht in `clips.json` und auf keine Lektionsseite, und in
  `clips.html` nur als Clip eines sichtbaren Leitprogramms (Spalte «Leitprogramm»); der Pre-Flight nimmt ihn von der Ablage-Prüfung aus. Zwei Fälle: ein
  Versuchsclip — und ein Clip, der **zu einer bestimmten Seite gehört und nirgends
  sonst**, wie die Prüfungsclips eines Leitprogramms nach §6.5. Weil das Feld dann
  etwas anderes heisst als «Versuch», gehört ein `"_probe"` mit der Begründung daneben.
  `lektion`, `reihe` und `folge` trotzdem ausfüllen: Wer den Clip später doch in die
  Bibliothek hebt, soll nur ein Feld löschen müssen.
- **Reihenfolge nach jedem Drehbuch-Edit:** `build-clip-ton.py` (falls der Sprechertext
  geändert hat), `build-clips.py`, `build-clips-einbau.py`, dann `build-seo.py` und
  `build-suchindex.py`.
- **Kurven im `graf`:** `kurven` mit einer `formel` (erlaubt: `sin cos tan asin acos atan
  sqrt exp log abs`, `pi`, `e`), `xteilung`/`yteilung` für eine Achsenteilung in
  Vielfachen von \(\pi\), `von`/`bis` für Kurvenstücke. **`abstand` eines `graf` ist die
  Bildhöhe plus rund 30**, kein Zeilenabstand — sonst überlappt die nächste Zeile.
  **Farbkopplung ist Pflicht:** `farbe: n` im Bild und `\fa`…`\fd` im Text greifen auf
  dieselbe Themenfarbliste zu (1 blau, 2 orange, 3 grün, 4 rot).
- **Vor dem Commit das Layout prüfen:** `node .claude/tools/pruef-clip.mjs
  clips/<name>.html <sekunden…>` meldet überlappende Zeilen und Überlauf. Die Bilder
  trotzdem ansehen — der Prüfer sieht Überlappung, nicht Gestaltung. Er misst seit dem
  07.09.2026 den **Inhalt**, nicht den Container: Eine `nowrap`-Zeile kann über ihren
  Container hinauslaufen, ohne dass dieser breiter wird. Deckungsgleiche Kästen gelten
  als Stapel und werden nicht gemeldet (Rechner-Clips).

## 6.5 Leitprogramme (verbindlich seit 01.09.2026)

Ein Leitprogramm ist eine eigenständige Seite unter `leitprogramme/` zum
selbstständigen Durcharbeiten. Es ist **keine Themenseite** und folgt darum nicht dem
Skelett aus §6.1. Es gibt zwei Arten, mit **identischem Layout** und verschiedener
Gliederung:

| | gegliedert nach | Beispiele (Stand 07.09.2026) | Anleitung |
|---|---|---|---|
| **Thema** | dem Stoff: Vorwissenstest, Kapitel, Gesamttest | `potenzen`, `quadratische-gleichungen`, `gleichungssysteme`, `quadratische-funktionen` (Vorbild, seit 02.10.2026) | `HOWTO-leitprogramme.md` |
| **Übungsprüfung** | dem Prüfungsbogen: je Teilaufgabe ein Clip, Musterlösung, Punktezeile | `uebungspruefung-1`, `trigo2` | `HOWTO-uebungspruefung.md` |

**Umfang eines Themen-Leitprogramms:** rund **6 bis 11 Clips** und **8 bis 12 Minuten**
Clipzeit, aufgeteilt auf vier bis fünf Kapitel mit je einem Selbsttest, dazu ein
Gesamttest von etwa 24 Punkten. Wird ein Thema deutlich grösser, gehört es geteilt —
zwei Programme mit je eigenem Vorwissenstest und Gesamttest tragen mehr als eines mit
zwei unverbundenen Hälften. Am 07.09.2026 wurde ein Entwurf mit 19 Clips aus genau
diesem Grund in *Quadratische Gleichungen* und *Gleichungssysteme* zerlegt.

**Die `localStorage`-Schlüssel sind je Seite eigen** (`lp-<name>-thema`,
`lp-<name>-stand`). Wer eine Seite als Vorlage kopiert und sie vergisst, lässt zwei
Leitprogramme denselben Fortschritt teilen: Das Häkchen im einen erscheint im anderen.

Hier nur, was für beide nicht verhandelbar ist.

- **`leitprogramme/` liegt genau eine Ebene unter der Wurzel**, wie `clips/`. Alle
  relativen Pfade setzen das voraus.
- **Kein fremder Host.** Schriften über `../schriften.css`, MathJax über
  `../vendor/mathjax/tex-svg.js` — wie überall sonst (§5.3.1).
- **Vollständiger Dokumentrahmen.** `<!DOCTYPE html>`, `<html lang="de-CH">`,
  `<meta charset="UTF-8">`, Viewport. Ohne Zeichensatz rät der Browser falsch, und die
  Umlaute zerfallen — sichtbar erst im Browser, in keiner Prüfung.
- **Kopf und Fuss der Site gehören dazu.** `<div id="nav-root">` mit
  `buildNav({ id: 'leitprogramme' })` und ein `.site-footer` nach §7. Ohne sie ist die
  Seite eine Sackgasse.
- **Geerbt wird, nicht kopiert.** `../style.css` **vor** dem eigenen `<style>` einbinden
  (dann gewinnt das eigene Layout bei gleichem Gewicht), Farbtokens aus `style.css`
  nehmen, die Clip-Bühne aus `mathlib.js`. Eine mitgelieferte Kopie der Bühne oder der
  Palette wird gelöscht — sie stimmt heute und läuft morgen auseinander.
- **Eigenes Layout ist erlaubt und erwünscht.** Ablaufspalte, Fortschrittszähler,
  Testköpfe stehen im eigenen `<style>`. Das Leitprogramm wird *nicht* in `page-wrap` +
  `main.content` gepresst.
- **Ein Dunkelmodus ist erlaubt** (man liest ein Leitprogramm am Stück), muss dann aber
  `--weiss` mitsetzen — `style.css` färbt seine Flächen damit — und `.site-footer`
  eigens behandeln, weil der `--tinte` als Fläche benutzt.
- **Kapitelüberschriften brauchen `id`.** Die Suche schneidet an `h2[id]`; ohne Anker
  ist die ganze Seite ein einziger Treffer.
- **Eintragen in `leitprogramme.html`, `build-seo.py` und `build-suchindex.py`** (dazu Pille
  «LP» auf `index.html` und Kasten «🧭 Lieber geführt?» auf der Themenseite). Der Block in
  `leitprogramme.html` wird von Hand gepflegt: eine Kachel je Leitprogramm, darauf je
  Themenseite Titel und Nummernpille (HOWTO-leitprogramme §13).
- **Unverlinkt veröffentlichen ist erlaubt — aber nur vollständig.** Soll eine Seite
  ausgeliefert, jedoch nicht gefunden werden (etwa eine Übungsprüfung, die eine Klasse
  per Link bekommt), dann **alle drei Stellen zusammen**: keine Karte in
  `leitprogramme.html`, kein Eintrag in `build-suchindex.py`, und in `build-seo.py` ein
  Eintrag **mit `noindex=True`** (nicht das Weglassen — sonst fehlen Beschreibung und
  canonical). `noindex=True` nimmt die Seite aus der Sitemap *und* setzt
  `<meta name="robots" content="noindex, nofollow">`; die Sitemap allein hält keine
  Suchmaschine ab, die die URL anderswoher kennt. **Kein `Disallow` in `robots.txt`** —
  die Datei ist öffentlich lesbar und würde die URL gerade bekanntmachen. Und es bleibt
  Unauffindbarkeit, keine Zugangskontrolle: Wer den Link hat, kommt hinein.

### Nur bei der Art «Übungsprüfung»

- **Die Aufgabentexte stehen wörtlich da**, samt Punktzahl — geglättete Formulierungen
  erklären eine andere Prüfung als die, die geschrieben wurde.
- **Der Prüfungsbogen steht am Anfang, vollständig und ohne Lösungen.** Er ist der Grund,
  dass die Aufgabentexte zweimal auf der Seite stehen; das ist Absicht.
- **Je Teilaufgabe ein Clip**, und die Clips tragen `"probe": true` (§6.4) — sie gehören
  zur Seite, nicht in die Bibliothek und nicht auf eine Lektionsseite.
- **Die Punktezeile unter jeder Lösung ist orange** (`.pkt-hinweis`) und damit nach §5.1
  „Aufgabe/Übung": Sie sagt, was in der Prüfung zählt. Sie kommt aus der Musterlösung —
  steht dort keine Aufteilung, wird keine erfunden.

## 7. Footer-Konvention

| Seite | Footer-Inhalt |
|---|---|
| **`index.html`** | Zeile 1: „**Mathe begreifbar** — Lernmaterial für die Berufsmaturität Technik, Architektur, Life Sciences"<br>Zeile 2: GitHub Pages-Link zum Repo (`https://github.com/go4exercises/tals-mathe`) |
| **Themenseiten** | Zeile 1: „**Mathe begreifbar** — Lernmaterial für die Berufsmaturität Technik, Architektur, Life Sciences"<br>Zeile 2: „⟪Bereich⟫ ⟪RLP-Nr⟫ ⟪Themenname⟫" — z.B. „Grundlagenfach 3.2 Lineare Funktionen", „Schwerpunktfach 3.4 Exponential- und Logarithmusfunktionen" |

**Format Bereich/Nr/Thema:** Vollständige Bereichsbezeichnung („Grundlagenfach" oder „Schwerpunktfach", **mit** „-fach"-Suffix), Leerzeichen, RLP-Teilgebiet-Nummer (z.B. `3.2`, bei Sub-Split mit Suffix `2.2a`), Leerzeichen, Themenname (= Sub-Themenname bei Sub-Split, also „Lineare Gleichungen", nicht „Lineare und quadratische Gleichungen"). Keine zusätzlichen Wörter, kein Lerngebiets-Name.

---

## 8. Qualitäts-Checkliste vor Veröffentlichung

Bevor eine Themenseite live geht, prüfe:

**Inhalt**
- [ ] Alle RLP-Kompetenzen des Themas abgedeckt
- [ ] „mit/ohne Hilfsmittel"-Hinweise gemäss RLP gesetzt
- [ ] Mindestens ein Anwendungsbeispiel im Einstieg
- [ ] Drei Darstellungen (Gleichung/Tabelle/Graph) verknüpft
- [ ] Spezialfälle visualisiert
- [ ] 6 Aufgaben (A1–A6) mit zunehmender Selbstständigkeit; optional eine 7. Vertiefungsaufgabe (A7, Badge „Vertiefung") — der Intro-Text nennt dann „Sieben Aufgaben" bzw. eine neutrale Formulierung. Weitere reguläre Aufgaben stehen **vor** der Vertiefung (§5.4)
- [ ] Zusammenfassung als kompakte Tabelle

**Notation**
- [ ] Multiplikationspunkt in Live-Anzeigen (`2·x`, nicht `2x`)
- [ ] Punkt-Komma-Notation: `(2 | 3)`, nicht `(2, 3)`
- [ ] Leere Menge als `\{\,\}`, nicht `\emptyset` / `∅` (§2.11)
- [ ] Dezimal**punkt**, nicht Komma
- [ ] „Graph" geschrieben, nicht „Graf"
- [ ] LaTeX für alle Formeln (kein Unicode-Improvising)

**Grafik**
- [ ] Reine Mathematik: 1:1-Skalierung (`square: true`)
- [ ] Anwendung: aufgabenbezogene Skalierung
- [ ] Anwendung: Achsenbeschriftung mit Einheit (`x [kg]`)
- [ ] Mathematik: Achsenbeschriftung `x` und `y` ohne Einheit

**Struktur & Konventionen**
- [ ] Zusatzmaterial-Sektion vor externen Ressourcen
- [ ] Alle 4 Einträge in fester Reihenfolge: Handout · Teste dich selbst · Aufgabenserie · Anki-Deck (optionale Zusatz-Karte am Ende)
- [ ] Druckseiten öffnen in neuem Tab (`target="_blank" rel="noopener"`)
- [ ] Anki-Deck als Download verlinkt (`.apkg`), die anderen drei als HTML-Druckseiten
- [ ] **Footer korrekt im Format „⟪Bereich⟫ ⟪RLP-Nr⟫ ⟪Themenname⟫"** — z.B. „Grundlagenfach 3.2 Lineare Funktionen" (siehe §7)
- [ ] **Titel-Präfix in `<h1 class="pt-h1">`** enthält die RLP-Nummer — z.B. „3.2 Lineare Funktionen", bei Sub-Split „2.2a Lineare Gleichungen"
- [ ] **Externe-Ressourcen-Sektion: `<h2 id="ressourcen">Externe Videos &amp; Aufgabensammlungen</h2>`** (genauer Wortlaut, siehe §4)
- [ ] **YouTube-Links sind stabile Watch-/Playlist-URLs** — keine `youtube.com/results?…`-Suchen
- [ ] **RLP-Pill `<span class="ohm">`** nur für exakt „auch ohne Hilfsmittel" — differenzierte Hinweise als Inline-Klammertext
- [ ] **Bei Sub-Split**: Hinweis „RLP X.Y · Teil n von m" zwischen Titel und RLP-Box; Sub-Karten im Index in `<div class="ksub">`-Container gruppiert

**HTML-Skelett (siehe §6.1)**
- [ ] Body-Struktur: `body > div#nav-root > div.page-wrap > main.content` + Geschwister `aside.toc-wrap`
- [ ] **`<main class="content">`** — nicht `inhalt` oder andere Eigenkreationen
- [ ] **`<aside class="toc-wrap"><div id="toc"></div></aside>`** als leerer Container *nach* `</main>`, nicht davor; keine hardcoded TOC-Liste
- [ ] **Anker-IDs direkt am `<h2 id="…">`** — keine `<section>`-Wrapper rund um Abschnitte
- [ ] **`<script src="../nav.js"></script>` ohne `defer`** und direkt vor dem `buildNav()`-Inline-Script
- [ ] **`buildNav({ bereich, id, kapitelNr, kapitelTitel, prev, next })`** — exakt diese Signatur, alle Felder gesetzt
- [ ] **Zusatzmaterial:** Container `<div class="dl-grid">`, Karten `<a class="dl">` (siehe §6.1) — nicht `dl-box`
- [ ] **Externe Ressourcen:** Container `<div class="links-grid">`, Karten `<a class="lk">` für Videos / `<a class="lk aufg">` für Aufgabensammlungen mit `<span class="lk-ic">` + verschachtelter Title/Sub-Struktur — nicht `ressourcen-grid`/`ress`
- [ ] **Block-Modifier** sind aus dem Inventar von §5.1: `block-def`/`block-bsp`/`block-aufg`/`block-fehler`/`block-beweis`/`block-tipp`/`block-merksatz` — keine Eigenkreationen
- [ ] Pre-Flight-Bash-Check aus §6.1 ausgeführt — alle Werte stimmen, Phantom-Klassen-Check `bad=0`
- [ ] ToC funktioniert (jeder h2 mit Sektionsfunktion hat eine `id`)

**Druckseiten (`downloads/.../*.html`)**
- [ ] Handout enthält ausschliesslich Theorie — keine Beispiele, keine Aufgaben
- [ ] „Seite drucken"-Knopf oben (sticky), Rück-Link zur Themenseite
- [ ] `print.css` und (falls Diagramme) `diagram.js` eingebunden
- [ ] Saubere A4-Seitenwechsel (`page-break-inside: avoid` für Aufgaben/Lösungs-Blöcke)
- [ ] Diagramme: reine Mathematik 1:1, Anwendungen mit Achsenbeschriftung und Einheit
- [ ] Ankideck erstellt und verlinkt?

**Technisch**
- [ ] MathJax lädt
- [ ] Responsiv auf Mobile (≤500 px Viewport)
- [ ] Alle interaktiven Widgets funktionieren
- [ ] Lösungen zugeklappt by default

---

## 9. Stub-Seiten (in Vorbereitung)

Eine **Stub-Seite** ist eine Themenseite, deren Struktur (RLP-Header, Master-Schema, Section-Headings, Footer, Nav) bereits steht, aber inhaltlich noch leer ist. Sie macht die Lehrplan-Abdeckung vollständig sichtbar, ohne 404-Links zu produzieren.

*Status Juli 2026: Es gibt aktuell keine Stub-Seiten mehr — alle 31 RLP-Teilgebiete (Grundlagen- und Schwerpunktfach) sind ausgearbeitet. Die Konvention bleibt für künftige Erweiterungen verbindlich.*

**Pflicht-Elemente einer Stub-Seite:**

- **Stub-Banner** als allererstes Element nach dem `<div class="page-titel">` und **vor** der RLP-Kompetenzen-Box. Genauer Wortlaut:
  ```html
  <div class="stub-banner">
    <strong>In Vorbereitung</strong>
    Diese Seite ist noch in Vorbereitung — die Themenstruktur und RLP-Kompetenzen stehen, der Inhalt folgt. Stand: ⟪Monat Jahr⟫.
  </div>
  ```
  Beim Veröffentlichen einer Themenseite (Übergang Stub → fertig) wird der Banner ersatzlos entfernt.
- **RLP-Kompetenzen-Box** vollständig — die Stub-Seite ist die zuverlässige Quelle dafür, was später inhaltlich abgedeckt wird.
- **Master-Schema-Skelett** mit Platzhalter-Texten („*Wird ausgearbeitet — formal nach FTB-Notation.*") in jedem Abschnitt. Die `<h2 id="…">`-IDs müssen schon richtig stehen, damit ToC und Cross-Links auch im Stub-Zustand funktionieren.
- **Footer und Nav (`buildNav`)** sind bereits korrekt gesetzt — Stubs sind voll in der Prev/Next-Kette.
- Kein `dl-grid` (Download-Karten) und keine externen Ressourcen-Karten, solange die Seite Stub ist (würde leere Karten produzieren). Die `<h2 id="downloads">`- und `<h2 id="ressourcen">`-Überschriften mit Platzhaltertext „*Wird ergänzt.*" sind zulässig und erwünscht, damit ToC und Cross-Links bereits funktionieren.

**Index-Karte einer Stub-Seite:** Die Karte erhält die Klasse `karte geplant` (kein grüner Streifen, ausgegrauter Titel, Cursor `help`, Pseudo-Element-Badge „in Vorbereitung" oben rechts). Sie bleibt klickbar — der Stub-Banner auf der Zielseite ist dann selbsterklärend.

---


---

## 10. Didaktische Module (übernommen aus TALS-Physik, ab ZIP 49–53)

Vier Muster, pilotiert auf `g3-2` und ausgerollt ab LG1. Klassen und Skripte werden **1:1 verwendet, nie nachgebaut**; Referenz-Implementierung: `grundlagen/g3-2-lineare-funktionen.html`.

### 10.1 Lernziele

Aufklappbare Ich-kann-Liste **direkt nach der RLP-Kompetenzen-Box**, Blau-Familie. 4–6 Punkte, abgeleitet aus RLP-Kompetenzen + Seiteninhalt, jede beginnt mit «Ich kann …».

```html
<details class="lernziele">
  <summary>🎯 Lernziele — das kann ich nach dieser Seite</summary>
  <div class="lz-body"><ul><li>Ich kann …</li></ul></div>
</details>
```

### 10.2 Mini-Checks

Einklappbare Verständnisfragen **vor jeder Sektionsgrenze** (vor dem nächsten `<h2>`), Orange-Familie (= Aufgabe/Übung). Akkordeon via `minicheck.js` (Pflicht-Einbindung: `<script src="../minicheck.js"></script>`). Pro Check vier Items in fester Reihenfolge: **Multiple Choice** (3 Optionen, `data-opt="A|B|C"`), **Lückentext** (`<span class="mc-luecke"></span>`), **Kurze Rechnung**, **Transfer** (Lösung als «Lösungsweg anzeigen»). Alle Rechnungen vor Auslieferung sympy-verifizieren.

```html
<details class="minicheck">
<summary class="mc-kopf">✏️ Mini-Check — <Thema></summary>
<div class="mc-item"><span class="mc-typ">Multiple Choice</span><p class="mc-frage">…</p>
  <ul class="mc-optionen"><li data-opt="A">…</li>…</ul>
  <details class="mc-loesung"><summary>Lösung anzeigen</summary><div class="mc-antwort">…</div></details></div>
…
</details>
```

### 10.3 Animations-Hinweise

Rollover-Paar «👁 Worauf achten?» (links) / «💡 Erkenntnis» (rechts) pro interaktiver Animation, Blau-Familie, Logik in `anim-hinweise.js` (Pflicht-Einbindung). Container ist eine `.widget-titelzeile`:
- **Widgets:** das `<h3>` im `widget-header` in die Titelzeile fassen, Untertitel-`<p>` bleibt darunter.
- **`.anim`-Blöcke:** den bestehenden `.anim-titel` in die Titelzeile fassen (Trigger stehen ausserhalb des uppercase-Titels und bleiben gemischt geschrieben).

```html
<div class="widget-titelzeile">
  <div class="anim-titel">…</div>  <!-- oder <h3>…</h3> -->
  <div class="anim-hinweis links">
    <span class="ah-trigger" tabindex="0">👁 Worauf achten?</span>
    <div class="ah-pop"><span class="ah-titel">Worauf achten?</span>
      <div class="ah-text">…</div>
    </div>
  </div>
  <div class="anim-hinweis rechts">…analog mit «💡 Erkenntnis»…</div>
</div>
```

### 10.4 Slider-Gruppierung und akz-Farbkopplung

Mehrere Regler **einer** Animation stehen in EINER `.sl-row`, jeder Regler als `.sl-grp` (Label + Slider + Wert unzertrennlich; Umbruch gruppenweise). Wertanzeige steht links direkt am Slider (zentrale Übersteuerung der lokalen `.sl-val`-Regeln).

**Farbkopplung:** `akz-blau / akz-orange / akz-gruen` auf `.sl-grp` (oder `.sl-row` bei Einzel-Reglern) färbt Slider, Wert und die Label-Variable (`label .var`, MathJax erbt currentColor). **Dieselben Farben in der Live-Formel**: HTML-Teile via `.tx-blau/-orange/-gruen`-Spans (innerHTML nur mit Slider-Zahlen), MathJax-Teile via `\textcolor{#1a4f8a}{…}` (blau) / `\textcolor{#b85c00}{…}` (orange) / `\textcolor{#1f6b3a}{…}` (grün).

**Verbindliche Färbe-Regel (was genau gefärbt wird):**
1. **Nur der slider-gebundene Wert** (die Ziffern) wird gefärbt — nie Operatoren (+, −, ·, =) und nie fremde Variablen. Falsch: `x² <span>− 5·x</span>` (das x ist nicht der Regler); richtig: `x² − <span>5</span>·x`.
2. **Die Variable selbst wird nur gefärbt, wenn sie der Regler ist** — z.B. x im Kartoffeln-Widget (`K(x)`, x ist der Schieber) oder k in einer Parameterdiskussion (`D(k)`, k ist der Schieber). Ein Koeffizienten-Regler (p, q, m, b) färbt nur seinen Zahlwert, nicht das daneben stehende x.
3. **Abgeleitete Resultate bleiben neutral** (Lösungen, gekürzte Brüche, D-Wert, Funktionswert).
4. Verschwindet der Wert aus der Anzeige (Koeffizient ±1 wird nicht geschrieben, Glied entfällt bei 0), erscheint dort folgerichtig keine Farbe — die gefärbte Wertanzeige am Slider bleibt die Referenz.

**Pflicht-Verifikation** bei jeder JS-Umstellung von textContent auf innerHTML: Äquivalenz der Ausgabe nach Tag-Strip über das **volle Sliderraster** (alle Wertkombinationen inkl. Sonderfälle 0, ±1, Vorzeichenwechsel) — null Abweichungen, sonst kein ZIP.

```html
<div class="sl-row">
  <div class="sl-grp akz-blau"><label>Steigung <span class="var">\(m\)</span></label>
    <input type="range" id="…"><span class="sl-val" id="…">2</span></div>
  …
</div>
```



---

## 11. Nachschlagen: Glossar und Formelsammlung (ab ZIP 59)

Zwei zentrale Referenzseiten im Repo-Root, übernommen aus TALS-Physik:

- **`glossar.html`** (`buildNav({ id:'glossar', homepage:true })`): A–Z-Sprungleiste (`.glossar-az`), Einträge als `.glossar-eintrag` mit `.ge-begriff`, optional `.ge-formel`, Definition (`<p>`) und `.ge-quer`-Themenverweis. Begriffe knapp und einheitlich; Herleitung bleibt auf der Themenseite.
- **`formelsammlung.html`** (`buildNav({ id:'formeln', homepage:true })`): pro Lerngebiet ein `.fs-block` mit `<h3>`, `.fs-thema`-Label und `.fs-zeile`-Einträgen (`.fs-name` / `.fs-formel` / `.fs-quer`-Themenlink). Die Formelsammlung ist die zentrale Formelübersicht des Lehrmittels (thematische Formelauszüge gab es bis Version 1.0, sie sind darin aufgegangen); die offizielle SBFI-Prüfungs-Formelsammlung bleibt separat verlinkt.

**Navigation:** Header-Dropdown «Nachschlagen ▾» (Gruppen «In diesem Lehrmittel» / «Extern») plus Mobile-Nav-Gruppe; aktiv bei `cfg.id==='glossar'||cfg.id==='formeln'`. Der Physik-Querlink ist relativ (`${prefix}../tals-physik/…`), funktioniert von Root- (`prefix=''`) und Themenseiten (`prefix='../'`) gleichermassen.

**Pflege:** Jeder `.fs-quer`/`.ge-quer`-Link zeigt auf eine existierende `#id` einer Themenseite — vor jedem ZIP per Anker-Validierung gegen die realen `h2 id`-Werte prüfen (verhindert tote Sprungmarken). CSS-Klassen liegen zentral in `style.css` (Mathe-Akzentvariablen `--blau`/`--orange`, nicht Physik-`--bernstein`).


*Pflege dieses Dokuments: bei Konvention-Erweiterungen Version hochzählen, Datum aktualisieren.*
