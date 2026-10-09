# HOWTO — Erklärclip bauen und einbauen

Ein Clip ist eine kurze, stumme Animation, die einen einzelnen Gedankengang Zeile für
Zeile aufbaut — kein Video, sondern eine HTML-Seite von rund 17 kB. Kein MP4, kein
Drittanbieter, scharf auf jedem Bildschirm.

Verwandte Dokumente: `STYLEGUIDE.md` (§5.3.1 keine Drittanbieter), `HOWTO-neue-themenseite.md`,
`CLAUDE.md` (Pre-Flight und Commit-Regel).

---

## Überblick

```
clips/
  <lektion>-<kurzname>.json          ← das Drehbuch. Die einzige Quelle.
  <lektion>-<kurzname>.html          ← generiert
  sprechertext-<lektion>-<kurzname>.txt   ← generiert, wird zum Transkript
  clips.json                         ← generierter Index
  themes/  begreifbar | heft | tafel | papier
  vorlage.json                       ← kommentierte Drehbuch-Vorlage
scripts/build-clips.py               ← Drehbuch  → Clip
scripts/build-clips-einbau.py        ← Clip      → Lektionsseite
```

Von Hand geschrieben wird **nur das Drehbuch**. Alles andere ist erzeugt und wird
mitversioniert, weil GitHub Pages nichts baut.

---

## Schritt 1 — Drehbuch schreiben

`clips/vorlage.json` kopieren nach `clips/<lektion>-<kurzname>.json` und ausfüllen. Alle
Felder, die mit `_` beginnen, sind Kommentare und werden ignoriert — sie dokumentieren
die Formelschreibweise, die Elementtypen und die Farbführung direkt in der Vorlage.

Drei Felder entscheiden über den Einbau:

| Feld | Bedeutung |
|---|---|
| `dateiname` | ohne Endung, ohne Umlaute — daraus werden `.html` und Sprechertext |
| `lektion` | **Liste** von Codes aus `nav.js`, z.B. `["g2-2b", "s2-2a"]`. Der **erste** Code ist die Heimatlektion: Dort steht der Clip in der Reihe, auf den übrigen Seiten hängt er als Gast hinten an. |
| `reihe` | didaktische Familie, z.B. `Parametergleichung` |
| `folge` | Platz in dieser Reihe: 1, 2, 3 … — weglassen bei Ergänzungen |
| `werkzeug` | `true` bei Rechner-Clips: ans Ende der eigenen Reihe, Zeile orange |
| `theme` | `begreifbar` ist Standard und übernimmt die Farben aus `style.css` |

### Titel: «Reihe: Fokus»

Ein Clip beantwortet **eine** Frage, und der Titel sagt welche:

```
Parametergleichung: nach x auflösen          folge 1
Parametergleichung: Bedingung für Lösung     folge 2
Lineare Gleichungen: Minus vor der Klammer   folge 1
```

Der Teil vor dem Doppelpunkt ist die `reihe`, der Teil danach der Fokus. In der
Bibliothek stehen Clips derselben Reihe beieinander und in der Reihenfolge ihrer
`folge` — die Nummer steht als Plakette vor dem Titel.

**Jede Reihe bekommt eine eigene Farbnuance**, in der Reihenfolge ihres Auftretens; bei
der nächsten Reihe wird weitergeschaltet, nach acht beginnt der Zyklus von vorn. Die Farbe
sitzt an der Plakette **und** an der linken Kante der Zeile — ein 19-px-Kreis allein
gruppiert zu schwach, die Kanten aufeinanderfolgender Clips bilden dagegen einen
durchgehenden Balken. Es sind bewusst nur Nuancen der Bereichsfarbe (blau im
Grundlagenfach, violett im Schwerpunktfach): Die didaktischen Farben aus §5.1 bedeuten
etwas, und sie für eine Gruppierung zu verwenden hiesse, sie umzudeuten. Alle Nuancen
tragen weisse Schrift mit mindestens 4.9 Kontrast, nachgerechnet.

**Innerhalb eines Lerngebiets ordnet die Themenseite** — 1.2, dann 1.3, dann 1.4, in
genau der Folge, in der die Seiten im Menü stehen. `build-clips-einbau.py` liest diese
Folge aus `nav.js`, statt sie zu wiederholen: Verschiebt sich eine Seite im Menü,
verschiebt sie sich auch in der Bibliothek. Innerhalb einer Seite ordnen die Reihen nach
der Liste `REIHEN` (wo die Folge didaktisch statt alphabetisch ist), innerhalb einer
Reihe die `folge`. Clips ohne `folge` sind Ergänzungen und rutschen ans Ende ihrer
Reihe; sie tragen einen Punkt statt einer Zahl.

**Rechner-Clips bekommen keine eigene Reihe.** Ein Clip zum Taschenrechner gehört
thematisch dorthin, wo sein Stoff steht — als letzter seiner Reihe: «Quadratische
Gleichungen: mit poly-solv lösen» ist Folge 7 der `Quadratische Gleichungen`, nicht
Folge 1 einer Reihe `Taschenrechner`. Dafür ist das Feld `werkzeug` da. Es sortiert den
Clip ans Ende seiner Reihe und färbt die Zeile orange — als einzige, in beiden
Bereichen gleich, denn sie soll gerade *nicht* zur Bereichsfamilie gehören. Auch der
Titel wiederholt das Werkzeug nicht: Sonst steht in der Bibliothek eine Spalte gleich
anfangender Titel, die nichts über den Stoff sagt.

Warum so und nicht «ein Clip für den ganzen Ablauf, dann Beispiel 1, Beispiel 2»: Eine
Minute reicht für einen Gedanken, nicht für ein Verfahren mit vier Schritten und drei
Fällen. Und «Beispiel 2» sagt niemandem, was darin zu holen ist, während «Bedingung für
Lösung» genau das sagt. Wer später doch einen Überblicks-Clip je Reihe will: `folge: 0`
ist frei und sortiert sich von selbst nach vorn.

**`lektion` ist eine Liste, auch bei nur einem Eintrag.** Ein Clip gehört oft auf mehrere
Seiten: die Bruchgleichung steht im Grundlagenfach unter `g2-2b` und im Schwerpunktfach
unter `s2-2a`. Ohne Liste müsste man ihn duplizieren, und zwei Kopien laufen auseinander.
Jeder Code muss zu einer `id` in `nav.js` passen — `build-clips-einbau.py` meldet einen
Tippfehler als `[FEHLER]`.

### Formelschreibweise — LaTeX

**Formeln stehen in LaTeX**, gesetzt von MathJax, genau wie auf den Lektionsseiten. Der
Grund ist nicht Schönheit, sondern Wegfall einer Übersetzung: Eine Formel lässt sich von
einer Seite ins Drehbuch kopieren, ohne sie in eine zweite Schreibweise zu übertragen —
und jede Übertragung war eine Gelegenheit für einen Fehler.

```
\dfrac{4}{11}          Bruch — \dfrac, nicht \frac: \frac wird in der Zeile klein
x^2   x_{1,2}          hoch- und tiefgestellt
\cdot \pm \neq \leq \geq \longrightarrow \Longrightarrow
\in \notin \setminus \cap \cup  \mathbb{R}  \sqrt{x}  \overline{36}
\quad                  sichtbarer Abstand innerhalb einer Zeile
```

**Zwei Dinge, die LaTeX anders will als die frühere eigene Schreibweise:**

**Prosa braucht `\text{…}`.** Die alte Schreibweise kursivierte nur *einzelne* Buchstaben,
darum durfte «es entstehen Faktoren» unmarkiert mitten in einer Formelzeile stehen. In
LaTeX wären das zwanzig kursive Variablen mit falschen Abständen. Also
`\text{es entstehen Faktoren}` — und **ein** `\text{}` um den ganzen Satz, nicht eines je
Wort, sonst setzt LaTeX zwischen die Wörter Mathe-Abstände.

**Einheiten gehören in `\mathrm{}`, mit `\,` davor.** `1.2\,\mathrm{m}` — ohne das `\,`
klebt die Einheit an der Zahl, weil LaTeX ein gewöhnliches Leerzeichen ignoriert.

### Koordinatenbild — `typ: "graf"`

Für Clips, die eine Gerade zeigen müssen. Kein Diagrammwerkzeug, nur so viel, wie ein
Clip braucht: Achsen mit Teilung, Geraden über Steigung und Achsenabschnitt, markierte
Punkte. Gezeichnet wird als SVG in den Theme-Farben.

```json
{"typ": "graf", "breite": 800, "hoehe": 620, "abstand": 650,
 "xbereich": [-1, 5], "ybereich": [-1, 8],
 "geraden": [{"m": -2, "q": 7, "farbe": 1, "beschriftung": "y = −2x + 7",
              "beschriftung_bei": [3.55, 1.15]},
             {"m": 2, "q": 1, "farbe": 2, "gestrichelt": true, "dicke": 9}],
 "punkte":  [{"x": 2, "y": 3, "farbe": 3, "beschriftung": "S(2 | 3)"}]}
```

Parabeln gehen genauso, als `parabeln` mit `a`, `b`, `c` für \(y = ax^2+bx+c\) —
gezeichnet als Streckenzug, der ausserhalb des Fensters abbricht und danach wieder
einsetzt.

Die Geraden werden **am Fenster** abgeschnitten, nicht an ihren Endpunkten — eine
Gerade, die aus dem Bild läuft, hört am Rand auf statt an einer willkürlichen Stelle
davor. `farbe` ist 1 bis 4 wie bei den Farbgruppen.

**`beschriftung_bei` gibt es für alle drei** — Geraden, Parabeln und Punkte. Ohne die
Angabe steht die Beschriftung eines Punktes rechts über ihm, und genau dort liegt am
Scheitel einer Parabel die Achsenbeschriftung. Die Koordinaten sind Datenkoordinaten,
nicht Pixel:

```json
"punkte": [{"x": 2, "y": -1, "farbe": 3,
            "beschriftung": "S(2 | −1)", "beschriftung_bei": [2.35, -1.35],
            "anker": "start"}]
```

**Die freie Stelle ausrechnen, nicht schätzen.** Vor dem Setzen kurz prüfen, wo die
Kurve an dieser Stelle verläuft — bei `y = x²` liegt die Kurve an `x = 1.35` auf `1.82`,
ein Label bei `7.6` ist also frei. Vier Kollisionen sind auf diese Weise entstanden und
erst im Bild aufgefallen, nicht in der Prüfung.

### Theme `begreifbar-schlicht` — Standard für neue Clips (seit 02.10.2026)

Wie `begreifbar`, aber **ohne Häuschenpapier und ohne roten Rand** (`karo: false`,
`rand: false`). Karo und Koordinatengitter eines `graf` stören sich, besonders in Bewegung.
Neue Clips setzen `"theme": "begreifbar-schlicht"`; bestehende bleiben, wie sie sind.
Das Theme kennt eine fünfte Farbe: `farbe: 5` ist Tinte, also «ungefärbt» — für Punkte und
Begleiter im `graf`, die keine der Termfarben tragen sollen (Nullstellen, \((0 \mid c)\),
gegebene Punkte). In den Clips `g3-3-lp-*` gilt durchgehend: 1 blau = \(a\), 2 orange =
\(x_s\), 3 grün = \(y_s\) bzw. Scheitel.

### Achsen mit Pfeil und Namen: `pfeile`, `xname`, `yname` (seit 02.10.2026)

`"pfeile": true` setzt Pfeilspitzen in positiver Richtung; `"xname"`/`"yname"` ersetzen die
Beschriftung «x»/«y» — bei Anwendungen mit Grösse und Einheit: `"xname": "x [m]", "yname": "A [m²]"`.
Benannte Achsen werden zuletzt gezeichnet, mit einem Hof in der Papierfarbe, damit eine Kurve sie
nicht überdeckt. Ohne die Felder bleibt das Bild wie bisher (bestehende Clips bauen gleich).
Für neue Clips mit Koordinatenbild: `pfeile` immer setzen.

### Bewegte Parabel und Gerade im `graf`: `bewegung` (seit 02.10.2026)

Statt eines festen Bildes je Szene kann eine Parabel **während der Szene gleiten**:

```json
{"typ": "graf", "xbereich": [-4, 5], "ybereich": [-4, 6], "parabeln": [
  {"a": 1, "gestrichelt": true, "dicke": 3},
  {"bewegung": [[0.8, 1, 0, 0], [3.6, 1, 0, 2]], "farbe": 1, "scheitel": {"farbe": 3}}]}
```

`bewegung` ist eine Liste von Stützpunkten `[t, a, u, v]` für \(y = a(x-u)^2 + v\), `t` in
Sekunden **ab Szenenbeginn**. Dazwischen weich überblendet (smoothstep), vor dem ersten und
nach dem letzten Punkt steht die Parabel still. Ein einziger Stützpunkt ergibt eine stehende
Parabel, an der sich trotzdem Begleiter bewegen können.

Begleiter — alle aus derselben Zeit gerechnet, alle mit `farbe`:

| Schlüssel | zeigt |
|---|---|
| `"scheitel": {}` | Scheitelpunkt mit mitlaufender Beschriftung «S(u \| v)» |
| `"nullstellen": {}` | die beiden Nullstellen; sie laufen zusammen und verschwinden, wenn die Parabel die Achse verlässt; mit `"beschriftung": true` steht «(x \| 0)» daneben |
| `"yachse": {}` | den \(y\)-Achsenabschnitt mit «(0 \| c)» |
| `"marken": [{"x": 0, "text": "h(0) = {y}"}]` | Punkt an festem \(x\) mit Live-Wert |
| `"laeufer": {"bahn": [[t, x], …], "text": "A = {y}", "spiegel": true}` | Punkt, der auf der Kurve fährt; `spiegel` zeigt blass den Partner bei \(2u - x\) |

In `text` stehen `{x}` und `{y}` für die laufenden Werte (eine Nachkommastelle, echtes
Minus).

**Geraden und Kurven bewegen sich genauso** (seit 03.10.2026). Der Stützpunkt ist
`[t, m, q]` für \(y = m x + q\); gezeichnet wird die am Fenster abgeschnittene Strecke:

```json
{"typ": "graf", "xbereich": [-4, 5], "ybereich": [-5, 6], "geraden": [
  {"m": 2, "q": 0, "gestrichelt": true, "farbe": 5, "dicke": 3},
  {"bewegung": [[0.8, 2, 0], [3.4, 2, 3]], "farbe": 1, "yachse": {"farbe": 2}}]}
```

Begleiter der bewegten Geraden — alle aus derselben Zeit gerechnet, alle mit `farbe`:

| Schlüssel | zeigt |
|---|---|
| `"yachse": {}` | den \(y\)-Achsenabschnitt mit «(0 \| q)»; `"beschriftung": false` lässt den Text weg |
| `"nullstelle": {}` | die Nullstelle mit «(x \| 0)»; verschwindet bei \(m = 0\) |
| `"marken": [{"x": 2, "text": "f(2) = {y}"}]` | Punkt an festem \(x\) mit Live-Wert |
| `"laeufer": {"bahn": [[t, x], …], "text": "{x} \| {y}"}` | Punkt, der auf der Geraden fährt |
| `"dreieck": {"x": -3, "dx": 2}` | mitlaufendes Steigungsdreieck ab \(x\), mit «Δx = …» und «Δy = …» |

In `text` gibt es zusätzlich `{m}` und `{q}`. Die Beschriftung setzt sich selbst auf die
Seite, auf der die Gerade *nicht* verläuft (bei \(m \gt 0\) unter den Punkt, sonst darüber) —
eine freie Stelle von Hand suchen muss man nur bei **festen** Punkten.

**Potenz- und Wurzelkurven** stehen in `kurven` mit einer `bewegung` aus Stützpunkten
`[t, a, p, u, v]` für \(y = a\,(x-u)^p + v\). Damit gehen Parabeln n-ter Ordnung (\(p \in \mathbb{N}\)),
Hyperbeln (\(p \lt 0\)) und Wurzelkurven (\(p = \tfrac1n\)) mit demselben Schlüssel:

```json
{"typ": "graf", "xbereich": [-4, 5], "ybereich": [-4, 5], "kurven": [
  {"bewegung": [[0.5, 1, 2, 0, 0], [4.0, 1, 5, 0, 0]], "stufen": true, "farbe": 1},
  {"bewegung": [[0, 1, -1, 0, 0]], "farbe": 1, "asymptoten": {"farbe": 5}}]}
```

| Schlüssel | zeigt |
|---|---|
| `"startpunkt": {}` | den Punkt \((u \mid v)\) mit Beschriftung — der Anfang einer Wurzelkurve |
| `"asymptoten": {}` | Polgerade \(x = u\) und waagrechte Asymptote \(y = v\), gestrichelt |
| `"marken": [{"x": 1, "text": "(1 \| {y})"}]` | Punkt an festem \(x\) mit Live-Wert |
| `"spiegel": {}` | **dieselbe Kurve an \(y = x\) gespiegelt** — die Umkehrfunktion |
| `"von"` / `"bis"` | schränken die Kurve auf ein Stück ein; \(y = x^2\) ist erst auf \(x \geq 0\) umkehrbar |

**Polynome in Linearfaktordarstellung** (seit 04.10.2026): `"polynom": true` liest die
Stützpunkte als `[t, a, x1, x2, …]` für \(y = a\,(x-x_1)(x-x_2)\cdots\). Legt man zwei
Nullstellen aufeinander, entsteht die doppelte Nullstelle von selbst. Begleiter:
`"nullstellen": {}` (je Linearfaktor ein Punkt «(x | 0)», zusammenfallende zeigen einen),
`"extrema": {}` (Hoch- und Tiefpunkte «H(…)», «T(…)», numerisch aus dem Vorzeichenwechsel
der Steigung) und `marken` wie oben. Vorbild: `scripts/lp/polynomfunktionen/clips.py`.

**Exponential- und Logarithmuskurven** (seit 04.10.2026): `"exponential": true` bzw.
`"logarithmus": true` lesen die Stützpunkte als `[t, c, a, v]` für \(y = c \cdot a^x + v\) bzw.
\(y = c \cdot \log_a x + v\). Begleiter: `asymptoten` (waagrecht \(y = v\) bzw. senkrecht
\(x = 0\)), `startpunkt` (\((0 \mid c + v)\) bzw. \((1 \mid v)\)), `marken` und `spiegel` — die an
\(y = x\) gespiegelte Exponentialkurve ist die Logarithmuskurve. Die Live-Beschriftung rundet auf
eine Stelle: Wo es auf zwei Stellen ankommt (\(0.25\)), die Marke mit festem Text schreiben.
Vorbild: `scripts/lp/exp-log-funktionen/clips.py`.

**Sinus- und Tangenskurven** (seit 05.10.2026): `"trig": "sin"` bzw. `"tan"` liest die
Stützpunkte als `[t, a, b, u, v]` für \(y = a \sin\big(b(x - u)\big) + v\) (Tangens ebenso); die
Cosinuskurve ist die Sinuskurve mit \(u = -\tfrac{\pi}{2}\). `asymptoten` zeichnet beim Sinus die
Mittellinie \(y = v\), beim Tangens alle Polgeraden. **`kreis`** setzt den Einheitskreis links
neben die Kurve: `{"mx": -1.6, "bahn": [[t, Winkel], …], "spur": true}` — Mittelpunkt
\((mx \mid 0)\), Radius 1 in \(y\)-Einheiten (bleibt rund, auch bei ungleicher Teilung), der Punkt
\(P\) folgt der Bahn, der markierte Bogen zeigt den Winkel im Bogenmass, eine gestrichelte
Waagrechte trägt die Höhe zur Kurve; beim Tangens trifft der Strahl die Tangente \(x = 1\).
`spur` zeichnet die Kurve nur bis zum aktuellen Winkel (Abrollen), `"projektion": false` zeigt
nur den Kreis. Die Kurve muss dann bei \(x = 0\) beginnen (`von`), sonst liegt sie über dem Kreis.
Für Sinuskurven das Bild breit statt quadratisch setzen (1640 × 480 unter dem Text).
Vorbild: `scripts/lp/trigonometrische-funktionen/clips.py`.

**Betragskurven** (seit 05.10.2026): `"betrag": true` liest die Stützpunkte als `[t, a, u, v]` für
\(y = a\,|x - u| + v\) — gezeichnet aus drei Punkten (Rand, Knick, Rand), der Knick bleibt scharf.
`startpunkt` ist der Knickpunkt \((u \mid v)\) mit Live-Beschriftung, `asymptoten` die
Symmetrieachse \(x = u\), `marken` wie oben. Für \(|f(x)|\) mit krummem \(f\) eine feste `formel`
mit `abs(…)` nehmen. Vorbild: `scripts/lp/betragsfunktionen/clips.py`.

**Klickfragen brauchen ein Bild mit Fenster.** Der Abspieler sucht für eine Klickfrage das
sichtbare Bild mit `[data-fenster]` — das tragen nur bewegte Kurven und Geraden. Zeigt die
Szene nur feste Kurven (`formel`), wird die Frage **stumm übersprungen**; `pruef-fragen` meldet
es als «Durchlauf: jede Frage genau einmal». Abhilfe: `"tippbar": true` im `graf`.

**`"stufen": true`** rundet \(p\) beim Überblenden auf ganze Zahlen. Ohne das entstünde
zwischen \(x^2\) und \(x^3\) kurz ein gebrochener Exponent — und der löscht den linken Ast
mitten in der Bewegung, weil es \((-2)^{2.5}\) nicht gibt. Wo es keinen Wert gibt (Pol,
negative Basis mit gebrochenem Exponenten), bricht der Streckenzug ab und beginnt danach
neu; so entstehen die zwei Äste einer Hyperbel von selbst.

Gezeichnet wird im Abspieler, **allein aus der Zeit**: `seek(t)` wird nur in Clips mit
`bewegung` um `bewegen(t)` erweitert (`BEWEGUNG_JS` in `build-clips.py`). Darum stimmen
Pause, Spulen und die Bilder von `pruef-clip.mjs` — ein Prüfbild mitten in der Bewegung
zeigt den Zwischenstand. Alle anderen Clips bleiben beim Neubau Byte für Byte gleich.
«Bewegung reduzieren» im Betriebssystem lässt die Parabel von Stützpunkt zu Stützpunkt
springen statt gleiten.

**Stützpunkte an den Sprechertext legen:** Die Bewegung soll laufen, während der Satz sie
nennt — die Zeiten nach der Vertonung aus der Szenendauer wählen. Bewegungen von 2–3 s
wirken ruhig, unter 1 s hektisch. Geht \(a\) durch 0 (Umklappen), ist die Parabel
kurz eine Gerade — das ist gewollt und zeigt, was dabei passiert.

Im Einsatz: die fünf Clips `g3-3-lp-*` («Parabel sehen», Leitprogramm Quadratische
Funktionen), die acht Clips `g3-2-lp-*` («Gerade sehen», Leitprogramm Lineare
Funktionen) und die Clips `s3-2-lp-*` («Kurve sehen», Leitprogramm Potenz- und
Wurzelfunktionen). Noch nicht: bewegte freie Formeln, Live-Zahlen in Formelzeilen.
**Formelzeile und Bewegung abstimmen:** Nennt die Formel links schon den Endwert, soll die
Bewegung früh und kurz sein (unter 2 s) — sonst steht im Text etwas anderes als im Bild.

### Fragen im Clip: `fragen` (Prototyp 02.10.2026)

Ein Clip kann **anhalten und fragen**, bevor der Sprecher die Auflösung nennt — die
Voraussage (predict–observe–explain) wandert in den Clip selbst:

```json
"fragen": [
  {"szene": "u schiebt", "bei": 0.35, "typ": "wahl",
   "text": "Gleich steht in der Klammer x − 2. Wohin wandert die Parabel?",
   "optionen": ["2 nach links", "2 nach rechts", "2 nach unten"], "richtig": 1,
   "rueck": {"0": "Das denken die meisten — wegen des Minus. Schau genau hin …"}},
  {"szene": "Zusammen", "bei": 0.38, "typ": "klick",
   "text": "y = (x − 2)² − 1: Wo landet der Scheitel? Tipp die Stelle ins Bild.",
   "ziel": [2, -1], "toleranz": 0.6, "richtig_text": "Getroffen …",
   "fallen": [{"bei": [-2, -1], "text": "Das Minus in der Klammer heisst rechts …"}],
   "falsch_text": "Nicht ganz …"}
]
```

- `bei` ist die Sekunde **ab Szenenbeginn** — vor `sprecher_bei` (0.4) legen, sonst
  bricht der Satz mitten im Wort ab.
- **Richtig → der Clip rollt sofort weiter** (kurzes ✓, keine Ansage). Nur eine falsche
  Antwort zeigt die Erklärung, liest sie vor und wartet auf «Weiter». Darum werden die
  Rückmeldungen zu richtigen Antworten nicht vertont (`fragen_texte()` lässt sie aus).
- `wahl`: Knöpfe, `rueck` gibt **je Antwort** eine eigene Rückmeldung. Bei einer
  falschen Voraussage die Lösung nicht verraten, sondern aufs Hinschauen lenken — der
  Clip löst sie gleich danach auf.
- `klick`: Tippen ins bewegte Bild der Szene (braucht ein `graf` mit `bewegung` —
  Parabel oder Gerade —, denn dessen Fenster rechnet den Tipp in Koordinaten um). `fallen` sind typische falsche
  Stellen mit eigener Rückmeldung (liegt ein Tipp in mehreren, gewinnt die nächste; Ziel und Fallen
  auch als Strecke — «Dritte Runde» unten); ein grüner Kreis zeigt danach die richtige Stelle.
  `toleranz` ist eine Zahl (Abstand in Dateneinheiten) oder `[dx, dy]` je Achse, wenn die
  Achsen verschiedene Grössen tragen. **`eingabe`: `["x", "y"]`** — dieselbe Antwort ohne
  Zeigegerät: zwei Zahlfelder und «Prüfen», gleiche Auswertung samt `fallen`. Die Namen sind die
  Achsennamen des `graf` (`["t", "y"]` beim Sättigungsclip). Gesetzt bei allen Klickfragen mit
  ablesbaren Koordinaten (34 Fragen, Stand 06.10.2026); nicht in der Planimetrie, deren Figuren
  ohne Achsen stehen. Die LP-Bauskripte setzen es im Helfer `klick()` (Vorgabe `('x', 'y')`).
- **Bedienung ohne Maus** (aus Physik, 06.10.2026): Beim Erscheinen einer Frage liegt der Fokus
  auf der ersten Antwort bzw. dem ersten Eingabefeld; Tab, Enter und die Leertaste bedienen sie.
  Die Leertaste schaltet nur dann Play/Pause, wenn kein Knopf, Link oder Eingabefeld den Fokus
  hat. Nach der Frage geht der Fokus zurück auf Play/Pause. `kopf` ersetzt die Kopfzeile «Deine
  Vorhersage» (z. B. «Dein Vorgehen»); ohne das Feld unverändert.
- Der Clip hält nur beim **Abspielen** an. Spulen erkennt `FRAGEN_JS` ausdrücklich
  (Klick auf die Zeitleiste, ← →), nicht am Zeitabstand zweier Bilder: Ein Sprung an
  einer Frage vorbei löst sie nicht aus, eine beantwortete Frage kommt beim Zurückspulen
  nicht wieder. Springt dagegen ein *Bild* über eine Frage (langsames Laden,
  Hintergrund-Tab), wird sie gestellt und der Clip an ihre Stelle zurückgesetzt.
  **R** und ein Sprung vor die erste Frage sind ein Neustart: offene Frage, Markierungen
  und Frage-Ton weg, alle Fragen wieder offen. Eine nur weggespulte, unbeantwortete
  Frage bleibt offen. Im Prüfmodus (`?render`, `pruef-clip.mjs`) gibt es keine Fragen.
- Wie `bewegung` nur in Clips mit `fragen` eingebaut (`FRAGEN_JS`); alle anderen bleiben
  Byte für Byte gleich.
- **Vorlesen:** Frage und Rückmeldung spricht dieselbe Stimme wie der Clip, sobald sie
  erscheinen — aber nur, wenn der Ton des Clips an ist. Erzeugt werden die Dateien
  getrennt von der Haupttonspur:
  ```sh
  python3 scripts/build-clip-fragen-ton.py <clip>   # je Text clips/ton/<clip>-f<i>-<schluessel>.mp3
  python3 scripts/build-clips.py <clip>             # danach: der Clip nimmt nur vorhandene Dateien auf
  ```
  Einzelne Fragen neu: `--fragen 2,5:r1` spricht alle Töne von Frage 2 und nur `r1` von
  Frage 5 (Fragen ab 1 wie in der Ausgabe; die Dateien zählen ab 0, also `-f1-*` und
  `-f4-r1`). Alle anderen Fragetöne bleiben unberührt. Ohne den Schalter löscht das Skript
  alle Fragetöne des Clips und spricht sie neu.
  Gesprochen wird der Wortlaut aus `sprich`, `rueck_sprich` (je Option), `richtig_sprich`,
  `falsch_sprich` und `fallen[].sprich` — wie beim Sprechertext ausgeschrieben («x minus
  zwei», nicht «x − 2»). Fehlt er, liest die Stimme den angezeigten Text. Welche Texte es
  gibt, steht an einer Stelle (`fragen_texte()` in `build-clips.py`); das Ton-Skript und der
  Abspieler benutzen dieselbe Liste. Das Skript ist Mathe-eigen und benutzt `sprich()` und
  `aussprache()` aus dem geteilten `build-clip-ton.py`, ohne es zu ändern.
- **Lokal testen:** `python3 -m http.server` kann keine Bereichsanfragen; darum springt
  der Ton beim Spulen auf den Anfang zurück. Auf GitHub Pages tritt das nicht auf.

Im Einsatz: `g3-3-lp-verschieben` (drei Fragen) und die vier Kontrollclips
`g3-2-lp-kontrolle-*` (je fünf, `wahl` und `klick` gemischt).

### Kurven im `graf`: `kurven`, `xteilung`/`yteilung`, `von`/`bis`

Bis zum 07.09.2026 konnte ein `graf` nur Geraden, Parabeln und Punkte. Für die Reihe zu
den trigonometrischen Funktionen kamen drei Dinge dazu.

**`kurven` zeichnet \(y = f(x)\) als Streckenzug.** Im Drehbuch steht die Formel, keine
Punktliste:

```json
{"typ": "graf", "kurven": [
  {"formel": "sin(x)", "farbe": 1, "beschriftung": "y = sin x", "beschriftung_bei": [1.8, 1.35]},
  {"formel": "3*sin(2*x-pi/2)", "farbe": 2}
]}
```

Erlaubt sind `sin cos tan asin acos atan sqrt exp log abs` sowie `pi` und `e` — mehr
nicht. Ein Drehbuch beschreibt eine Kurve, es rechnet nicht.

**Lücken entstehen von selbst.** Wo die Formel keinen Wert liefert oder der Wert aus dem
Fenster läuft, bricht der Streckenzug ab und beginnt danach neu. Genau daran entstehen
die Polstellen der Tangenskurve — im Drehbuch steht kein Wort über Pole.

**`xteilung` / `yteilung` ersetzen die ganzen Zahlen an der Achse.** Eine Sinuskurve
gehört bei \(\pi/2\) geteilt, nicht bei 1, 2, 3. Paare aus Stelle und Beschriftung; die
Beschriftung ist Text, denn das SVG kennt kein LaTeX — also `π/2`, nicht `\tfrac{\pi}{2}`:

```json
"xteilung": [[0, "0"], [1.5708, "π/2"], [3.1416, "π"]]
```

Das Karo folgt der Teilung mit; sonst stünde das Raster bei ganzen Zahlen und die Striche
bei Vielfachen von \(\pi\).

**`von` / `bis` begrenzen eine Kurve auf ein Stück des Fensters.** Gebraucht für
Hilfslinien: Eine Mittellinie `{"formel": "35", "von": 0, "bis": 24.6}` läuft sonst über
die Achsenbeschriftung am linken Rand — im Bild sichtbar, für den Prüfer unsichtbar.

**Zwei Fallstricke, beide beim Bau dieser Reihe bezahlt:**

1. **`abstand` bei einem `graf` ist die Bildhöhe plus rund 30**, kein Zeilenabstand. Mit
   `abstand: 120` unter einem 560 px hohen Bild überlappt die nächste Zeile um 62 px.
   Die Konvention der bestehenden Clips: `hoehe + 30`.
2. **Farbkopplung prüfen.** `farbe: 3` im `graf` und `\fc{…}` im Text sind dieselbe
   Farbe — beide greifen auf `farben` des Themes zu (1 blau, 2 orange, 3 grün, 4 rot).
   Wer im Text `\fd{v}` schreibt und die zugehörige Linie mit `farbe: 3` zeichnet,
   koppelt falsch. Der Prüfer sieht das nicht; im Bild fällt es sofort auf.

**Und: die Bedingungsleiste verträgt keine hohe Szene.** Trägt das Drehbuch eine
`voraussetzung`, bricht der Bau ab, wenn eine Szene mit `oben < 170` beginnt. Bei einer
Szene mit grossem Bild ist die Versuchung gross, `oben` klein zu setzen — dann lieber die
Bildhöhe verkleinern.

**Der senkrechte Strich `|` bricht im Fliesstext die Zeile.** Wer in einer Notiz
\(2|a|\) schreiben will, packt es in `@…@` — dort ist der Strich geschützt. Sonst steht
die Hälfte des Satzes auf einer neuen Zeile und die Betragsstriche sind weg.

**`abstand` von Hand setzen**, sonst überschreibt die nächste Zeile das Bild: Der
senkrechte Fluss nimmt ohne Angabe `hoehe` als Abstand, und dann beginnt die nächste
Zeile genau an der Unterkante. Faustregel: `hoehe` plus 30.

In einer Szene mit Merkschiene ist das Bild **nicht** zentriert (dort ist nichts
zentriert) — es steht bei `x`, standardmässig 680. Ein eigenes `x` richtet es an den
Formelzeilen darüber aus.

### Boxplot — `typ: "boxplot"`

Für die Datenanalyse. Gezeichnet werden die fünf Kennzahlen, sonst nichts:

```json
{"typ": "boxplot", "min": 2, "q1": 4, "med": 5.5, "q3": 7.5, "max": 12,
 "breite": 1250, "hoehe": 290, "abstand": 330,
 "teilung": [2, 4, 6, 8, 10, 12], "farbe": 1}
```

`teilung` setzt die Achsenteilung — ohne sie ist das Bild nicht ablesbar.
`marken: false` lässt die Beschriftung *min · Q1 · Median · Q3 · max* weg, wenn sie
schon im Text steht. `abstand` wie beim Koordinatenbild von Hand setzen: `hoehe` plus 30.

**Die Konvention ist die der Themenseite 4.3**: Box von \(Q_1\) bis \(Q_3\), Strich beim
Median, Antennen bis zum kleinsten und grössten Wert. **Keine Ausreisserregel** — die
Seite kennt keine, und ein Clip führt keine ein, die dort nicht steht. Wer die
Quartile rechnet, nimmt die Median-der-Hälften-Methode; bei ungeradem \(n\) bleibt der
Median selbst aussen vor.

### Rechneranzeige — `typ: "rechner"`

Für Clips über den Taschenrechner. Nachgebaut wird **die Anzeige, nicht das Tastenfeld**:

```json
{"typ": "rechner", "breite": 700,
 "zeilen": ["[3|4]+[1|6]"], "ergebnis": "[11|12]", "taste": "n/d"}
```

`[a|b]` wird zweistöckig gesetzt, wie MathPrint es tut. `ergebnis` steht rechtsbündig
unter der Eingabe, `taste` zeigt darunter die gedrückte Taste als Kappe. Höhe und
Abstand rechnet der Generator selbst — Zeilen mit Bruch bekommen die anderthalbfache
Höhe, sonst schneidet der Rand Zähler und Nenner ab.

**Tastenfolge — Taste für Taste.** Mehrere Anzeigen an *derselben* Stelle mit
gestaffeltem `ein` ergeben einen Stapel: Jede neue legt sich über die vorige, die alte
bleibt darunter stehen. Das braucht keine neue Mechanik, nur drei Felder:

```json
{"typ":"rechner", "zeilen":["2+"],  "taste":"+", "y":190, "ein":1.55, "anim":"fade", "abstand":0}
{"typ":"rechner", "zeilen":["2+3"], "taste":"3", "y":190, "ein":2.50, "anim":"fade", "abstand":0}
```

Gleiches `y`, gleiche `breite`, `anim: "fade"` (sonst wackelt es beim Einblenden) und
`abstand: 0` bei allen ausser der letzten — sonst schiebt der Fluss die folgende Zeile
um die Höhe jeder einzelnen Anzeige nach unten. `pruef-clip.mjs` erkennt
deckungsgleiche Kästen als Stapel und meldet sie nicht als Zusammenstoss.

**Warum kein Tastenfeld:** Wo eine Taste auf dem Gerät liegt, ist nicht nachgeprüft.
Eine erfundene Anordnung wäre schlimmer als keine — wer sie lernt, greift am Gerät
daneben. Gezeigt wird darum nur, *welche* Taste gedrückt wird.

**Was am TI-30X Pro MathPrint belegt ist** (Handbuch von Texas Instruments): vier Zeilen
zu 16 Zeichen, Eingabe oben, Ergebnis rechtsbündig, getrennte Tasten für Subtraktion
`−` und negatives Vorzeichen `(−)`, Berechnen mit `=`, Brüche über `n/d`, `del` löscht
ein Zeichen, `clear` die Eingabe. Was darüber hinausgeht, gehört nachgeschlagen, bevor
es in einen Clip kommt.

Seit dem 30.09.2026 ausserdem belegt (Online-Hilfe, siehe unten, mit Bildschirmfotos):
`num-solv` mit seinen fünf Schirmen (`□=□` · «EDIT VARIABLE IF NEEDED» · «SOLVE FOR:» ·
«SOLVE ON [LOWER,UPPER]:» mit `LOWER=-1E99`, `UPPER=1E99` · Ergebnis mit `LEFT-RIGHT=0`),
`poly-solv` (`POLY SOLVER`, `1:ax²+bx+c=0`, Koeffizienten einzeln, `x1=`/`x2=` je ein
Schirm, exakt mit Bruch oder Wurzel wie \(2 \pm \sqrt{5}\), komplexe Lösungen mit `i` auch im Modus REAL, Scheitelform), `sys-solv` (`SYSTEM SOLVER`,
`1:2x2 Linear EQs`, Maske `(2)x+(3)y= 12`, Zeichen mit `+`/`−` gewählt, Ergebnisse in
`x`, `y`, `z` abgelegt, `INFINITE SOLUTIONS`), das Konstanten-Menü (`1:c Speed Light`,
`2:g GravityAccel`, `3↓h Planck Const`; UNITS `m/s`, `m/s²`, `J s`), Matrizen `[A]`–`[C]`
und Vektoren `[u]`–`[w]` bis 3×3. Wurzelform und `i` im Modus REAL hat der Auftraggeber am 30.09.2026 am Gerät bestätigt; die Einzelheiten stehen in der Git-Geschichte von `TODO-ti30x-am-geraet.md` (Commit d8022c3).
**Kopfzeilen** wie «EDIT VARIABLE IF NEEDED» stehen am Gerät in kleiner, inverser Schrift
und passen nicht in die 16 Zeichen des Nachbaus — weglassen, nicht kürzen.

**Die Quelle, jedes Mal dieselbe.** Das deutsche Handbuch von Texas Instruments,
68 Seiten:

```
https://education.ti.com/download/de/ed-tech/4AF74FB5F81C45348BF24C0BFD52ECA7/B5FC5D6EE7194B27B631854AE04188D5/TI-30X_Pro_MathPrint_Guidebook_DE.pdf
```

`WebFetch` scheitert am Binär-PDF, legt es aber lokal ab; den Text danach mit `pypdf`
herausziehen und `grep`en — rund 62 kB. Die Extraktion verschluckt die Leerzeichen
(`TastenmitMehrfachbelegung`), also nach Wortteilen suchen, nicht nach Wortgruppen.

**Die zweite Quelle: die Online-Hilfe von TI.** Sie hat Kapitel, die im PDF fehlen
(Gleichungslöser, Matrizen, Vektoren), und zu jedem Schritt ein Bildschirmfoto der
Anzeige (150 × 58 Pixel, PNG):

```
https://education.ti.com/html/webhelp/30Xpro/de/content/m_mathtools/mt_solvers.HTML
https://education.ti.com/html/webhelp/30Xpro/de/Data/Toc.js        # Inhaltsverzeichnis
```

Mit `curl` holen, Tags entfernen, die Bilder aus `../_images/…` nachladen und vergrössert
ansehen (`PIL`, `Image.NEAREST`, Faktor 3). Die Tasten stehen in einer eigenen
Symbolschrift (`<span class="Keys_TI-30X_Pro">`): `%` ist `2nd`, `<` ist `enter`,
`!` `"` `#` `$` sind die Pfeile links, rechts, auf, ab, `r` ist die Umschalttaste.
Die englische Fassung liegt unter `…/30Xpro/en-gb/…`.

**Zeilenlänge vorher zählen.** Sechzehn Zeichen sind sechzehn Zeichen — `"LEFT=3(x-15)"`
passt, `"RIGHT=.7168(200-x)"` nicht. Der Prüfer meldet das *nicht*: Der SVG-Text läuft
still über den Rand des Displays hinaus. Zahlenspalten mit `"%4s%7s" % (x, wert)`
formatieren, dann stehen sie auch untereinander.

**Ergebnisse mit zehn Stellen.** Das Gerät zeigt bis zu zehn signifikante Stellen —
`6.666666667E-8`, nicht `6.67E-8`. Exponent als `E`, Malzeichen als `×`, Divisions­zeichen
als `÷`, so wie es die bestehenden Clips halten.

**Ein Tastenstapel muss gleich hoch sein.** Mehrere Anzeigen an derselben `y`-Position
mit gestaffeltem `ein` bilden einen Stapel — und jede neue muss die vorige **vollständig
verdecken**. Hat der spätere Schirm *weniger* Zeilen als der frühere, schaut unten ein
schwarzer Balken samt alter Tastenkappe hervor. Der Prüfer erkennt deckungsgleiche
Kästen als Stapel und schweigt dazu; sichtbar wird es erst im Bild. Also: alle `zeilen`-
Listen eines Stapels auf dieselbe Länge bringen, notfalls mit einer leeren Zeile `""`.

**Was beide Quellen nicht hergeben, kommt nach `TODO-ti30x-am-geraet.md`** — die Datei
ist seit dem 30.09.2026 gelöscht, weil alle Fragen geklärt sind, und wird bei der
nächsten offenen Gerätefrage neu angelegt. Wer eine Frage klärt, trägt die Antwort
in die Liste oben ein.

### Flächen, Strecken, Texte im `graf`; Parabeln von–bis (aus Physik, 07.10.2026)

Seit Mathe den gemeinsamen Bauer benutzt (siehe «Ein Bauer für beide Fächer» unten), stehen Physiks
Felder auch hier zur Verfügung. Alle statisch, in Datenkoordinaten; ohne die Felder ändert sich nichts.

```json
{"typ": "graf", "xbereich": [-1, 6], "ybereich": [-1, 10],
 "flaechen": [{"punkte": [[0, 0], [3, 9], [3, 0]], "farbe": 1, "deckung": 0.28, "beschriftung": "A"}],
 "strecken": [{"von": [3, 0], "bis": [3, 9], "farbe": 3, "gestrichelt": true,
               "beschriftung": "Δy = 9", "beschriftung_bei": [3.2, 4.5]},
              {"von": [0, 0], "bis": [2, 4], "farbe": 4, "pfeil": true}],
 "texte": [{"bei": [0.4, 9], "text": "f(x) = x²", "farbe": 5, "groesse": 28, "anker": "start"}]}
```

- `flaechen` liegen unter allen Linien; `deckung` ist die Füllstärke (Standard 0.22).
- `strecken`: Hilfs-, Mass- und Vektorlinien; `"pfeil": true` setzt die Spitze ans Ende. Beschriftung
  mit hellem Hof, Lage per `beschriftung_bei`, `anker`, `groesse`. `texte`: freie Beschriftungen.
- SVG-Text kennt kein LaTeX: «Δy = 9», «x²», «x₀» gehen, `\frac` nicht.
- Bewegte Parabeln kennen `"ab"`/`"bis"` (nur zwischen diesen x zeichnen), bewegte Geraden `"ab"`.
- `"achsen": false` lässt in Mathe das Karo stehen (Planimetrie); als Deckblatt darum zusätzlich
  `"raster": false` (siehe «Später einblenden»).

### Figuren im Graf — `"figuren"` und `"achsen": false`

Seit 06.10.2026 (Leitprogramm Planimetrie). Ein `graf` zeichnet unter Geraden und Punkten
beliebige Figuren in Fensterkoordinaten; mit `"achsen": false` bleibt nur das Karo.

```json
{"typ": "graf", "xbereich": [-1, 9], "ybereich": [-1, 9], "breite": 760, "hoehe": 760, "achsen": false,
 "figuren": [
   {"art": "vieleck", "punkte": [[0,0],[8,0],[4,3]], "farbe": 1, "fuellung": 0.12},
   {"art": "strecke", "von": [4,3], "bis": [4,0], "farbe": 2, "gestrichelt": true},
   {"art": "rechts", "bei": [4,0], "r1": 0, "r2": 90},
   {"art": "kreis", "m": [4,4], "r": 3, "farbe": 1},
   {"art": "sektor", "m": [4,4], "r": 3, "von": 0, "bis": 60, "farbe": 3, "fuellung": 0.25},
   {"art": "bogen", "m": [4,4], "r": 3, "von": 0, "bis": 60, "farbe": 2},
   {"art": "winkel", "bei": [0,0], "von": 0, "bis": 37, "r_px": 40, "farbe": 2},
   {"art": "text", "bei": [4,-0.6], "text": "g = 8 cm", "farbe": 5, "kursiv": false}]}
```

Farben 1–4 wie sonst, 5 = Tinte; `dicke` (Standard 4), `gestrichelt`, `fuellung` (Deckkraft der
Fläche), `deckkraft` (der Linie — ein Kreisring ist ein Kreis mit `dicke` = Ringbreite und `deckkraft` 0.3). Winkel in Grad gegen den Uhrzeigersinn. **Das Fenster gleich teilen** (Spanne x zu
Spanne y wie Breite zu Höhe), sonst wird der Kreis zur Ellipse und der rechte Winkel schief.

### Später einblenden, bewegen, mitlaufen — Erweiterungen vom 07.10.2026

Entstanden aus der Übersicht `TODO-lp-clips-visualisierung.md`. Ohne die neuen Felder baut jeder
Clip wie vorher (geprüft: alle 514 neu gebaut, nur Abspielcode geändert, keine JS-Fehler).

**`ein`/`aus` an einem Teil.** Jeder Punkt, jede Kurve, Gerade, Parabel, Figur, Strecke, Fläche und
jeder Text im `graf` darf ein eigenes `ein` und `aus` tragen — Sekunden ab Szenenbeginn, wie beim
Element. Der Teil blendet weich ein und aus. Das ersetzt das frühere Deckblatt (zweiter `graf`
mit `"achsen": false, "raster": false` darüber); bestehende Deckblätter bleiben gültig.

```json
"punkte": [{"x": 5, "y": 0, "farbe": 3, "beschriftung": "(5 | 0)", "ein": 3.4},
           {"x": 0, "y": 0, "farbe": 4, "beschriftung": "verloren", "ein": 4.3, "aus": 9}]
```

**Läufer auf Kurven.** `"laeufer": {"bahn": [[t, x], …], "text": "({x} | {y})", "farbe": 3}` — an
bewegten `kurven` jeder Art (Potenz, Exponential, Logarithmus, Betrag, Sinus/Tangens, Polynom) und
an festen Formelkurven (`"formel"`; der Abspieler liest dort aus einer Wertetabelle, `n` Stellen).

**Zahlen in Live-Beschriftungen** (`{x}`, `{y}`, Nullstellen, Scheitel): eine Nachkommastelle, ausser
der Wert hat genau zwei — dann beide (−0.75, −1.25 statt −0.8, −1.2). Während einer Bewegung sind
die Werte krumm und bleiben bei einer Stelle.

**Parabel in Normalform.** `"normalform": true` an einer bewegten Parabel liest die Stützpunkte als
`[t, a, b, c]` für \(y = ax^2 + bx + c\). So läuft \(a\) stetig durch 0 (Parabel → Gerade → Parabel);
bei \(a = 0\) zeigen `nullstellen` die eine Nullstelle der Geraden, `scheitel` verschwindet.
**`"achse": true`** (oder `{"farbe": n}`) zeichnet die Symmetrieachse \(x = u\) gestrichelt mit, in beiden Formen.

**Mitlaufende Schnittpunkte.** An einer bewegten Geraden:
`"schnitte": {"kurve": 0, "farbe": 2, "beschriftung": true, "anzahl": 6}` — die Schnittpunkte mit
der festen Formelkurve `kurven[0]`, auch Berührstellen (Knick auf der Waagrechten). Beschriftungen
stehen abwechselnd über und unter der Geraden; bei vielen Punkten `"beschriftung": false` und die
Werte als Notiz.

**Bewegte Figuren.** `"bewegung": [[t, {Felder}], …]` an einer Figur: Jeder Stützpunkt überschreibt
Felder (`punkte`, `von`, `bis`, `m`, `r`, `bei`, `text` …), dazwischen werden alle Zahlen weich
übergeblendet. Vor dem ersten Stützpunkt steht die Figur, wie sie definiert ist; `{}` als erster
Stützpunkt heisst «so bleiben bis t». Gerechnet wird in Python mit 20 Bildern je Sekunde — eine
Bewegung von 3 s kostet rund 60 Bilder der Figur, also nur bewegen, was sich bewegen soll.

```json
{"art": "vieleck", "punkte": [[0,0],[8,0],[2,5]], "farbe": 1, "fuellung": 0.12,
 "bewegung": [[1, {}], [4, {"punkte": [[0,0],[8,0],[6,5]]}]]}
```

**Bereich, der wandert.** `"grenzen": [[t, von, bis], …]` an einer bewegten Kurve statt festem
`von`/`bis` — Einschränken auf einen umkehrbaren Teil, ein Intervall, das sich zusammenzieht.

**Gleichmässig statt weich (seit 08.10.2026, aus Physik).** Zwischen zwei Stützpunkten blendet der
Abspieler weich über: Er fährt langsam an, ist in der Mitte 1.5-mal so schnell wie im Mittel und
bremst wieder ab. Für eine laufende Welle ist das falsch — sie zeigt gerade eine konstante
Geschwindigkeit \(c = \lambda/T\). `"gleichmaessig": true` an einer bewegten Kurve blendet ihre
Stützpunkte, ihre `"grenzen"` und die `bahn` ihrer Läufer, Marken und ihres Einheitskreises linear über
— sonst schwebt ein Läufer vor dem Kurvenende oder rutscht vom Wellenberg. Mehr Stützpunkte helfen nicht: Jedes Stück fährt
wieder an und bremst.

**Tangens am Einheitskreis** läuft über den Fensterrand: Die Strecke wird am Rand abgeschnitten
statt ausgeblendet, der Strahl endet dort auf seiner Richtung; liegt P links der y-Achse, geht der
Strahl von P durch den Mittelpunkt.

**Nachgetragen beim Einbau (07.10.2026):** `ein`/`aus` auch direkt an einem `laeufer` (jeder Art) und
am `dreieck` einer bewegten Geraden — keine zweite, deckungsgleiche Kurve mehr nötig. Bei Figuren
mit `bewegung` wird Feld für Feld übergeblendet (bis zur Korrektur sprang die Figur in der Mitte
zwischen zwei Stützpunkten); `farbe` wird umgeschaltet, nicht gemischt. Gleiche Nachbarbilder
(Pausen mit `{}`) fasst der Bauer zu einem zusammen. Beim Steigungsdreieck mit Δx < 0 steht «Δy»
links der Kathete.

**Zweite Runde (07.10.2026), die kleinen Wünsche der Bearbeiter:**

| Feld | wo | was |
|---|---|---|
| `"drehung": w`, `"um": [x, y]` | Figur, auch als Feld in ihrer `bewegung` | dreht die Figur um `um` (Grad, gegen den Uhrzeigersinn). In der `bewegung` wird der Winkel übergeblendet: `[[1.9, {"drehung": 0}], [3.3, {"drehung": 180}]]` — die Figur bleibt gleich gross, keine dichten Stützpunkte mehr. Texte drehen ihre Lage mit, nicht die Schrift. |
| `"parameter": [[t, {"q": -4}], …]` | feste Formelkurve | Buchstaben in der `formel`, die sich während der Szene ändern; der Abspieler zeichnet die Kurve selbst. Der erste Stützpunkt nennt alle Buchstaben. Erlaubt ist, was `kurven`-Formeln können (`abs`, `sqrt`, `sin`, `pi`, `**` …). |
| `"punkte": [{"x": "pi/(6*b)", "text": "({x} \| {y})"}]` | Formelkurve mit `parameter` | Punkte, die auf der Kurve mitfahren; ihr `x` ist eine Zahl oder eine Formel in den Parametern (der Punkt, der beim Stauchen wandert); `ein`/`aus` je Punkt. |
| `"betrag_von": "x**2+q"` | Formelkurve | kurz für `"formel": "abs(x**2+q)"` — die umgeklappte Kurve in einem Stück, mit `parameter` auch bewegt (statt dreier Stücke mit dicht nachgeführten Grenzen). |
| `"lage": "oben"` | `laeufer` (jeder Art), `marken`, Punkt einer Formelkurve | wo die Beschriftung steht: `oben`, `unten`, `links`, `rechts` oder zwei davon (`"oben links"`). Ohne Angabe wie bisher. |

Ausserdem ohne neues Feld: Läufer liegen jetzt **über** festen Punkten (sie werden zuletzt gezeichnet
und nehmen das `ein`/`aus` ihrer Kurve mit), und keine Beschriftung eines mitfahrenden Punkts ragt
mehr über den Bildrand — sie klappt auf die andere Seite des Punkts oder wird hereingeschoben.

**Dritte Runde (08.10.2026), Wünsche aus den LPs 5.3–5.5.** Ohne die Felder baut jeder Clip Byte für
Byte wie vorher (alle 543 neu gebaut); neuer Abspielcode kommt nur in Clips, die das Feld benutzen. Einzige
Ausnahme ist die nächstgelegene Falle unten — sie ändert den Abspielcode aller 58 Clips mit Fragen.

| Feld | wo | was |
|---|---|---|
| `"aus": 6.5` | jedes Element, auch ein ganzer `graf` | blendet das Element mitten in der Szene aus (Sekunden ab Szenenbeginn, wie `ein`); geht vor `halten`. Kein `aus` mehr an jede Figur einzeln. |
| `"parameter": [[t, {"w": 0}], [t, {"w": 150}]]` | Figur | Buchstaben, die weich laufen; Lage- und Massfelder dürfen Formeln darin sein. `sind`, `cosd`, `tand` rechnen in Grad. So fährt ein Punkt **auf dem Kreisbogen** statt quer durch den Kreis: `{"art": "kreis", "m": ["cosd(w)", "sind(w)"], "r": 0.04, "fuellung": 1, "parameter": …}`; Radius `"bis": ["cosd(w)", "sind(w)"]`, Dreieck `"punkte": [[0, 0], ["cosd(w)", 0], ["cosd(w)", "sind(w)"]]` mit derselben Liste. Ersetzt die dichten Stützpunkte (`Lauf` in `scripts/lp/einheitskreis/clips.py`). Nicht zusammen mit `bewegung`. |
| `"folgt": 1`, `"versatz": [dx, dy]` oder `"radial": 0.17` | Figur, meist `text` | hängt an Figur 1 derselben Liste und fährt Bild für Bild mit: an `m` (Kreis, Sektor, Bogen), `bei` (Text, Winkel, Zeichen) oder der Ecke `"ecke"` (Strecke 0/1, Vieleck: Index; ohne Angabe die letzte). `radial` setzt den Text um seine Mitte, so weit von `"mitte"` (Standard [0, 0]) weg nach aussen — der Name am Punkt P. |
| `"name": "P"`, `"name_abstand": 30` | `kreis`-Begleiter einer Sinus-/Tangenskurve | beschriftet den laufenden Punkt, radial nach aussen (px). |
| `"zahlen_neben_kreis": true` (oder Radius) | `graf` | die Zahlen ±1 stehen neben bzw. über/unter dem Kreis um den Ursprung statt auf der Kreislinie. |
| `"grad": true` | bewegte Kurve mit `"trig"` | x-Achse in Grad: Stützpunkte `[t, a, b, u, v]` mit `u` in Grad, \(y = a\sin\big(b(x-u)\big)+v\) mit dem Argument in Grad; `von`/`bis`, `grenzen`, `marken`, `laeufer` und beim `kreis` `mx` und die `bahn` ebenfalls in Grad. `{x}` zeigt Grad. Kein `xteilung`-Behelf mit Bogenmass mehr; eine Klickfrage mit `eingabe` verlangt dann Grad. |
| `"farbwechsel": [[2, 2], [3.5, 3]]` | bewegte Kurve, Gerade, Parabel | ab t (ab Szenenbeginn) trägt die Linie diese Farbe (1–5); vorher ihre eigene. Umgeschaltet, nicht gemischt. Begleiter behalten ihre Farbe. |
| `"strich": "4 9"` oder `"voll"`, `"dicke": 2` | `asymptoten` einer bewegten Kurve | eigene Strichart (SVG-Strichmuster) und Dicke; Standard bleibt `"10 8"`, 3 px. Pole und Mittellinie tragen dieselbe. |
| `"ausweichen": true` | `graf` | Beschriftungen von Punkten — feste und mitfahrende — weichen einander und fremden Punkten aus: Eine Beschriftung bleibt, solange sie frei ist, sonst nimmt sie die erste freie von acht Lagen um ihren Punkt. Kurven und Linien sind kein Hindernis. Ohne das Feld wie bisher (bewusst als Option: Es hätte sonst in allen bewegten Clips Beschriftungen verschoben). |
| `"ziel": [[0, 0], [4, 3]]` | Klickfrage, auch `fallen[].bei` | **Strecke** statt Punkt: Es zählt der Abstand zur Strecke (bei `toleranz` `[dx, dy]` in Toleranz-Einheiten). Ein Fehltipp zieht die Strecke grün nach. Für «Tipp die Hypotenuse an». |

**Nächste Falle gewinnt** (ohne neues Feld, 08.10.2026): Liegt ein Tipp in mehreren `fallen`, kommt die
Rückmeldung der nächstgelegenen, nicht mehr die der ersten in der Liste; bei Gleichstand die erste. Betroffen
waren vier Kontrollclips mit überlappenden Fallen (`g3-2-lp-kontrolle-typen`, `g3-3-lp-kontrolle-extremwert`,
`g5-3-lp-kontrolle-seiten`, `g5-4-lp-kontrolle-periode-umkehr`) — dort sagte ein Tipp bei \(x = 2.3\) bisher
«3 ist der halbe Abstand» statt «Bei x = 2 …». `pruef-fragen.mjs` tippt bei einer Strecke ihre Mitte an.

```json
{"typ": "graf", "aus": 6.5, "zahlen_neben_kreis": true, "xteilung": [[-1, "−1"], [1, "1"]], "yteilung": [[-1, "−1"], [1, "1"]],
 "figuren": [
   {"art": "kreis", "m": [0, 0], "r": 1, "farbe": 5, "dicke": 3},
   {"art": "kreis", "m": ["cosd(w)", "sind(w)"], "r": 0.04, "farbe": 5, "fuellung": 1,
    "parameter": [[0.5, {"w": 0}], [3.5, {"w": 150}]]},
   {"art": "text", "text": "P", "folgt": 1, "radial": 0.17, "farbe": 5, "groesse": 34}]}
```

**Noch nicht:** ein bewegtes Fenster (Zoom) und eine senkrechte bewegte Gerade. Behelf für den Zoom:
mehrere `graf` nacheinander mit wachsendem Fenster.

### Bild einer Animation — `typ: "bild"` und `"animation"`

Übernommen aus TALS Physik am 27.09.2026 (dort Prototyp
`p6-2-fi-stromvergleich`). **Stand 27.09.2026 nutzt kein Mathe-Drehbuch das
Werkzeug**; es liegt bereit für Clips, die die Erkenntnisse *einer* Animation einer
Lektionsseite zusammenfassen.

```json
{"typ": "bild", "datei": "bilder/g3-2-kartoffeln-1.jpg", "breite": 1140, "abstand": 450}
```

`datei` ist relativ zu `clips/`. Eine SVG wird beim Bauen eingegossen (sie muss mit
`<svg` beginnen), JPG und PNG als `data:`-URL; der Clip bleibt eine Datei. `breite`
in Bühnenpixeln, die Höhe folgt dem Seitenverhältnis. Im Schienen-Layout passt ein Bild
von 1140 × 400 px über Formelzeile, Text und Notiz; `abstand` auf etwa 450 setzen.
Aufnahmen der Animation selbst macht
`node .claude/tools/aufnahme-anim.mjs <plan.json>` (Zustände per Klick, Reglerwert
oder JS-Aufruf, doppelte Pixeldichte, JPEG; Aufbau des Plans im Kopf der Datei). Das
zeigt im Clip genau das Bild, das auf der Seite steht. Eine eigene SVG-Skizze lohnt nur,
wo die Animation etwas nicht zeigen kann. Ihre Zahlen werden aus der Rechnung der
Animation nachgerechnet, nie abgeschrieben.

Das Drehbuch trägt dazu `"animation": "<id des h3>"`. `build-clips.py` schreibt das
Feld nach `clips.json`, und `build-clips-einbau.py` macht drei Dinge daraus:

- Es setzt «▶ Clip» als letzten Eintrag in die `.widget-titelzeile` der Animation,
  rechts neben «Worauf achten?» und «Erkenntnis», zwischen die Marker
  `<!-- CLIP-ANIM … -->`. Nie von Hand ändern.
- Auf der Lektionsseite stellt es den Clip in eine eigene Gruppe «Clips zu den
  Animationen».
- Die Zeile wird dort und in `clips.html` in der Farbe der Animations-Hinweise
  abgesetzt (Blau, `.cl-anim`), mit dem Link «Anim» davor.

**Falle, nur in Mathe:** Die `h3` in Mathes Titelzeilen tragen keine `id`. Vor dem
ersten Animationsclip bekommt die Überschrift der Animation einen Anker
(`<h3 id="anim-…">`), sonst meldet der Einbau `[FEHLER] … Animation #… nicht gefunden`.
Animationen in Aufgaben haben statt `h3` ein `div.anim-titel`; der Anker kommt dann
dorthin (`<div class="anim-titel" id="anim-…">`), der Einbau findet beide.
Der Titel muss sich klar vom Stoff-Clip zum selben Thema unterscheiden, denn dieselbe
Liste zeigt beide.

**Ausgerollt 28.09.2026:** alle 46 Themenseiten mit Animationen, 223 Clips, einer je Titelzeile. Ausgangspunkt war der **Pilot g3-2**. Sechs Clips `g3-2-anim-*`, einer je Animation,
Reihe «Animationen erklärt», `folge` = Nummer der Animation auf der Seite. Aufbau je
Clip: Titel mit der Frage, drei Schritte im Schienen-Layout mit je einer Aufnahme,
«Was man sich merkt»; der Inhalt ist die 💡 Erkenntnis der Animation. Bildbreiten, die
sich bewährt haben: Tabelle und Graph nebeneinander (`.zwei-spalten`) 860 px, ein
quadratisches Canvas 480 px, `abstand` rund 500. Vor den Aufnahmen die Animation selbst
ansehen: Was im Bild falsch sitzt (Beschriftung über Achsenzahlen, Text aus dem Canvas),
steht auch im Clip — zuerst die Animation beheben, dann aufnehmen.

Was beim Ausrollen immer wieder auffiel und darum vor jedem neuen Animationsclip geprüft
wird:
- **Lesbarkeit:** Die kleinste Schrift, auf die der Clip Bezug nimmt, ist auf der
  1920er-Bühne mindestens 20 px hoch (Faktor = Bildbreite ÷ CSS-Breite des Elements).
  Tabelle und Graph zusammen sind fast immer zu klein; dann nur das Canvas aufnehmen,
  bei schmaler Fensterbreite (360–640 px), und Tabellenwerte in der Formelzeile nennen.
- **Farben:** `\fd` ist Rot und heisst «falsch» — nie für eine vierte Grösse.
- **Grenzen der Animation** (Regler, Bildrand) sind keine Bedingungen der Mathematik.
- **💡/👁 prüfen:** verlangen sie etwas, das die Animation nicht kann (fehlender Regler,
  nicht einstellbarer Wert), oder gilt die Aussage nur für einen Teil der Werte?
- **Live-Anzeigen:** gerundete Werte mit «≈», exakte mit «=».
- **Achsen 1:1**, wo Winkel oder Senkrechte gezeigt werden.

### Die Bedingungsleiste — `voraussetzung`

Der häufigste didaktische Mangel in einem mehrszenigen Clip: In Szene 2 wird eine
Voraussetzung genannt — die Definitionsmenge, `a ≠ 0`, «vor `x²` steht eine 1» — und in
Szene 6 rechnet der Clip darauf weiter, während sie längst vom Bild verschwunden ist.
Wer erst dort einsteigt, sieht eine Rechnung ohne Grundlage.

`halten` löst das nur halb: Ein gehaltenes Element behält die Position **seiner** Szene
und blockiert damit den Fluss aller folgenden — deshalb steht in dieser Datei die Regel,
dass Folgeszenen dann tiefer beginnen müssen. Für eine Bedingung ist das ein hoher Preis.

Die Bedingungsleiste steht **ausserhalb des Flusses** und kostet darum keine Zeile:

```json
"voraussetzung": "a \\neq 0"
"voraussetzung": {"text": "D = \\mathbb{R} \\setminus \\{2\\}", "tag": "gilt", "ab": "Schritt 1 · D"}
"voraussetzung": [ {…}, {…} ]
```

| Feld | |
|---|---|
| `text` | LaTeX, wie jede Formel |
| `tag` | die Beschriftung links, Standard `Voraussetzung`. Bewährt: `gilt`, `gilt für`, `Bedingung` |
| `ab` | Szenenname — erst ab dort sichtbar. Ohne Angabe von Anfang an |
| `bis` | Szenenname — bis dorthin sichtbar. Ohne Angabe bis zum Schluss |

Sie sitzt bei `top: 96px` und endet bei `y = 150`. **Mit einer Leiste beginnen alle Szenen
bei `oben ≥ 170`** — der Generator bricht sonst mit einer Meldung ab, statt es im Bild
verstecken zu lassen. `pruef-clip.mjs` prüft die Leiste wie jede andere Zeile mit.

**Wofür sie nicht da ist.** Wenn die Bedingung das *Ergebnis* des Clips ist, gehört sie
nicht von Anfang an ins Bild — sie nähme die Frage vorweg. `g2-2a-warum-a-ungleich-5`
heisst «Warum \(a \neq 5\)?»; dort wäre eine stehende Leiste die Antwort vor der Frage.
Entweder `ab` auf die Szene setzen, in der sie hergeleitet ist, oder ganz weglassen.

### Farbführung

`{1:x-2}` färbt einen Term ein — Text und weiche Fläche. Zweck ist ausschliesslich,
denselben Term über mehrere Zeilen hinweg wiedererkennbar zu machen: man sieht, was von
wo nach wo wandert.

**1 und 2 (Blau/Orange) sind das sichere Paar**, auch bei Rotgrünschwäche. Dass Orange
auf den Seiten „Aufgabe" markiert, ist hier kein Widerspruch: im Clip markiert Farbe
einen Term, nicht einen Blocktyp. Sparsam bleiben — ein Bild mit sechs Farben erklärt
nichts mehr.

---

## Schritt 2 — Clip bauen

```sh
python3 scripts/build-clips.py                      # alle
python3 scripts/build-clips.py g2-2b-bruchgleichungen
python3 scripts/build-clips.py g2-2b-bruchgleichungen --eigenstaendig
```

Braucht nur Python 3. Der Lauf gibt die Szenenzeiten aus — daran sieht man sofort, ob
eine Szene zu hetzt oder steht.

`clips.json` wird **fortgeschrieben**, nicht überschrieben: Ein Lauf für einen einzelnen
Clip lässt die übrigen Einträge stehen und entfernt nur solche, deren HTML-Datei nicht
mehr existiert.

Die eigenständige Fassung (rund 480 kB) bettet die Schriften ein und läuft ohne die
Site — für Moodle, zum Verschicken, fürs Archiv. Nicht routinemässig bauen und **nicht
committen**; die Web-Fassung ist die gepflegte.

### `"probe": true` — gebaut, aber nicht in der Bibliothek

Ein Drehbuch mit `"probe": true` wird ganz normal gebaut und ausgeliefert, aber

- es kommt **nicht** in `clips/clips.json`,
- es erscheint **nicht** in der Bibliothek `clips.html` — ausser es gehört zu einem
  sichtbaren Leitprogramm nach Thema: dann in dessen Spalte «Leitprogramm» (seit 06.10.2026),
- `build-clips-einbau.py` baut es auf **keine** Lektionsseite ein,
- der Pre-Flight nimmt es von der Ablage-Konsistenzprüfung aus (sonst meldete er die
  HTML-Datei als «fehlt in clips.json»).

Gedacht war das Feld für Versuchsclips. Es trägt inzwischen einen zweiten, dauerhaften
Fall: **Clips, die zu einer bestimmten Seite gehören und nirgends sonst.** Die 26
Prüfungsclips des Leitprogramms `uebungspruefung-1` sind so eingebunden — sie stehen in
der Seite, aber die Bibliothek bleibt bei 62 Einträgen, und die acht betroffenen
Lektionsseiten bleiben unverändert. Ohne das Feld wären beide ungefragt mitgewachsen.

Weil «probe» dann etwas anderes heisst als «Versuch», gehört eine Begründung daneben:

```json
"probe": true,
"_probe": "Prueferklaerung — gehoert zum Leitprogramm uebungspruefung-1, nicht in die Clip-Bibliothek."
```

`lektion`, `reihe` und `folge` trotzdem ausfüllen: Sie werden bei `probe` nicht
ausgewertet, aber wer den Clip später in die Bibliothek heben will, soll nur ein Feld
löschen müssen. Der ganze Ablauf für Prüfungsclips steht in `HOWTO-uebungspruefung.md`.

---

## Schritt 3 — In die Lektionsseite einbauen

Einmal pro Seite die beiden Kommentarzeilen setzen, **nach der Zusammenfassung und
vor dem Zusatzmaterial** — direkt vor dem Kommentarkopf von `<h2 id="downloads">`
(Entscheid Auftraggeber 27.09.2026, wie TALS Physik; STYLEGUIDE §4, Punkt 8b):

```html
<!-- CLIPS:ANFANG — generiert von scripts/build-clips-einbau.py, nicht von Hand ändern -->
<!-- CLIPS:ENDE -->
```

Danach:

```sh
python3 scripts/build-clips-einbau.py               # Probelauf
python3 scripts/build-clips-einbau.py --schreiben
```

Das Skript liest `clips/clips.json`, holt die Zuordnung Lektion → Datei aus `nav.js` und
schreibt zwischen die Marker: eine `<h2 id="clips">`-Überschrift (die Seiten-Navigation
nimmt sie automatisch auf), darunter **dieselbe zweispaltige Auswahl wie in der
Bibliothek** und darunter die Transkripte in einem Aufklapper.

Es ist dieselbe Aufgabe wie dort, also dieselbe Form: eine Zeile aus Nummer, Titel und
Laufzeit; der Clip läuft **gross über dem Fenster**, nicht in der Zeile. Auch die Ordnung
ist dieselbe — Reihen alphabetisch, darin nach `folge`.

Die Transkripte stehen gesammelt unter der Auswahl, jedes mit seiner eigenen
`<h3 id="clip-…" class="clip-h">`. Für Leserinnen und Suchmaschinen ist der Aufklapper
weiterhin das Einzige, was von einem animierten Clip überhaupt zu sehen ist — wer ihn
entfernt, nimmt den Clips ihre Auffindbarkeit.

**Für die Volltextsuche der Site gilt das seit dem 13.09.2026 nicht mehr.** Sie nimmt
jeden Clip **einmal** unter `clips.html#clip-<name>` auf, gebaut aus `clips/clips.json`
und `clips/sprechertext-*.txt`; der Aufklapper der Lektionsseite ist dafür von der
Indexierung ausgenommen (`clip-transkripte` steht in `SKIP_CLASSES`). Vorher lag jeder
Clip so oft im Index, wie er eingebettet ist — 162 Clips ergaben 213 Abschnitte —, und
jeder Treffer führte auf eine Lektionsseite, auf der man den Clip dann selbst suchen
musste.

Damit ein Suchtreffer nicht in einem zugeklappten `<details>` verschwindet, öffnet
`mathlib.js` beim Laden alle `<details>` über dem Sprungziel aus `location.hash`.

Früher stand hier je Clip

```html
<h3 id="clip-<dateiname>" class="clip-h">Titel</h3>
<p class="clip-text">Kurzbeschrieb</p>
<div class="clip" data-clip="…" data-titel="…">
  <button class="clip-start" …>▶ 1:21</button>
</div>
<details class="clip-transkript">…</details>
```

**Die eigene `h3` je Clip ist nicht Schmuck.** `scripts/build-suchindex.py` schneidet an
`h3.clip-h[id]` einen eigenen Abschnitt. Ohne sie heisst in den Suchergebnissen jeder
Clip einer Seite „Clips" und alle führen auf dasselbe Sprungziel. Weil der Titel damit in
der Überschrift steht, trägt der Knopf nur noch das Dreieck und die Dauer — er ist rund
67 × 29 px gross statt einer Karte über die volle Breite. Im Inhaltsverzeichnis der Seite
taucht er nicht auf: `buildToC` nimmt nur `h2`.

**Der Clip wird nicht beim Seitenaufruf geladen.** Sichtbar ist zuerst nur der Knopf;
erst der Klick setzt das `<iframe>` ein (`clipStart` in `mathlib.js`). So läuft bei
mehreren Clips auf einer Seite keiner von selbst los, und die Seite lädt nicht N
zusätzliche Dokumente mit. Der Clip startet dann von selbst — er ist frisch eingesetzt,
sein Autostart ist genau richtig.

**In der Bibliothek läuft er gross.** Dort trägt die Karte `data-modus="gross"`, und
`clipStart` legt statt des Rahmens in der Zeile eine Bühne über das Fenster — rund 80 %
der Fensterfläche statt einer schmalen Spalte. Escape oder ein Klick auf den dunklen Rand
schliesst sie, der Clip hält an.

Warum kein neuer Tab: Er verlässt die Liste, und ein vergessener Tab spielt weiter. Fürs
Projizieren oder Verschicken führt im Kopf der Bühne trotzdem ein Link **eigener Tab ↗**
auf die Clipdatei.

**Auf der Lektionsseite läuft er weiterhin an Ort und Stelle** — dort gehört er zwischen
Theorie und Aufgaben, nicht über die Seite gelegt. Gesteuert wird das allein über
`data-modus`; ohne das Attribut bleibt es beim Rahmen in der Zeile.

**Und er lässt sich wieder einklappen.** Über dem Rahmen steht „✕ Clip schliessen"
(`clipStop`); das entfernt das `<iframe>`, der Clip hält an, gibt den Platz frei, und der
Knopf kommt zurück. Ein zweiter Klick startet ihn von vorn.

Jede Seite mit einem Clip-Block **muss `mathlib.js` einbinden.** Themenseiten tun das
ohnehin.

---

## Schritt 4 — Verifikation

0. **Layout prüfen** — `node .claude/tools/pruef-clip.mjs clips/<name>.html 10 22 34 …`
   springt in die genannten Sekunden, meldet überlappende Zeilen und alles, was über die
   Bühne hinausragt, und legt je Zeitpunkt ein Bild ab. **Die Bilder trotzdem ansehen:**
   Der Prüfer sieht Überlappung, nicht Gestaltung. Ein Bruchstrich macht eine Zeile
   doppelt hoch — Zeilen mit `[a|b]` brauchen `abstand` ≥ 200.
   **Seit dem 07.09.2026 misst der Prüfer den Inhalt, nicht den Container.** Eine
   zentrierte Zeile spannt sich über die ganze Bühne (`left:0;right:0`), ihr Text trägt
   aber `white-space: nowrap`: Er kann über den Rand hinauslaufen, ohne dass der
   Container breiter wird — die alte Messung sah davon nichts. Die Regel stammt aus TALS
   Physik, wo sie beim Umstellen zehn abgeschnittene Zeilen in fünf Clips aufdeckte.
   In Mathe brachte die Umstellung **0 zusätzliche Funde über alle 177 Clips**; die
   Zeilen sind hier schmaler gesetzt. Vorsorge also, keine Reparatur — aber wer eine
   lange Formelzeile ohne `|` schreibt, verlässt sich jetzt zu Recht auf den Prüfer.
   **Deckungsgleiche Kästen meldet er nicht**: Die Rechner-Clips stapeln die
   Display-Zustände absichtlich an derselben Stelle.
1. **Pre-Flight** über die geänderten Lektionsseiten, wie immer vor dem Commit.
2. **Im Browser bei 1280 und 360 px**: Karte sichtbar, Klick lädt den Clip, Rahmen im
   richtigen Verhältnis, Bedienleiste ohne Überlauf. Auf schmalen Schirmen blendet der
   Clip die Tastaturhinweise aus — dort gibt es weder Leertaste noch Pfeiltasten.
3. **Netzwerk-Tab**: keine Anfrage an einen fremden Host. Der Clip zieht die Schriften
   per `@import url("../schriften.css")` aus dem Repo.
4. **Transkript vorhanden und lesbar.** Fehlt der Sprechertext, meldet das
   Einbau-Skript `[WARN]` und lässt den Block weg.

---

## Häufige Stolpersteine

**Jeder Eintrag der `schiene` braucht eine Szene mit passendem `schritt`.** Der Merkweg
blendet Eintrag *i* ein, sobald die erste Szene mit `schritt ≥ i` beginnt. Gibt es zu
einem Eintrag gar keine solche Szene, fällt er auf den Startzeitpunkt der ganzen Schiene
zurück — er steht dann **von Anfang an** da, während die Einträge davor noch fehlen, und
reisst eine Lücke in die Nummerierung: 1, 2, … 4. Vier Einträge in der `schiene` heissen
also vier Szenen mit `schritt` 1 bis 4; mehrere Szenen dürfen sich denselben `schritt`
teilen, aber keine Nummer darf fehlen. Der Prüfer sieht das nicht — es ist kein Überlauf
und keine Überlappung, nur eine falsche Liste.

**Der Clip liegt eine Ebene unter der Wurzel — und das ist nicht frei wählbar.** Er zieht
die Schriften per `@import url("../schriften.css")`. Verschiebt man `clips/` tiefer, sind
die Schriften weg, ohne dass etwas bricht: die Seite fällt still auf Georgia zurück.

**Das Transkript ist nicht Beiwerk.** Von einem animierten Clip sieht eine Suchmaschine
gar nichts. Der Aufklapper der Lektionsseite ist das, was sie liest — er bleibt.

Für die **site-eigene** Suche steht `clip-transkripte` dagegen bewusst in `SKIP_CLASSES`
von `scripts/build-suchindex.py`: Dort ist der Clip über seinen eigenen Eintrag unter
`clips.html` auffindbar, und ohne die Ausnahme fände man denselben Satz zweimal — der
zweite Treffer führte nur auf eine Seite mit hundertsechzig Clips.

**Nach jedem Drehbuch-Edit beide Skripte laufen lassen**, erst `build-clips.py`, dann
`build-clips-einbau.py`. Das zweite liest nur `clips.json` und baut selbst nichts; ohne
den ersten Lauf steht in der Seite die alte Dauer und der alte Kurzbeschrieb.

**`build-seo.py` danach**, damit `dateModified` und die Sitemap stimmen. Der Pre-Flight
warnt, wenn es fehlt.

**Brüche funktionieren nur in Formel-Elementen, nicht in Prosa.** `formel`, `karte` und
`box` schicken ihren ganzen Text durch `formel()` — dort wird `[a|b]` zum Bruch. Die
Prosa-Typen `text`, `notiz`, `titel`, `untertitel`, `aussage` und `liste` gehen dagegen
durch `text_html`, und das ersetzt `|` **zuerst** durch einen Zeilenumbruch, bevor es die
`@…@`-Abschnitte auswertet. Aus `@x = [b|a]@` wird darum kein Bruch, sondern eine
umgebrochene eckige Klammer — ohne Fehlermeldung, es sieht nur falsch aus. Wer in einer
Merkzeile einen Bruch braucht, macht daraus ein eigenes `formel`-Element.

**Ein `display` in der Regel schlägt das `hidden`-Attribut.** Sobald eine Klasse
`display: grid` oder `display: flex` setzt, hört `hidden` auf zu wirken — die Gruppen
standen alle offen, ohne dass etwas gemeldet wurde. Es braucht dann ausdrücklich
`.klasse[hidden] { display: none; }`. Betrifft in diesem Projekt `.cl-body` und
`.clip-start`.

**`liste` wird nicht zentriert.** Der Typ bekommt die Klassen `l sans`, aber kein `mitte`
— der Block läuft über die volle Bühnenbreite und beginnt am linken Rand, auch im Layout
`zentriert`. In einer sonst mittigen Szene wirkt das wie ein Versehen. Für aufgezählte
Merkpunkte in der Mitte drei `formel`-Zeilen nehmen; die tragen `row` und sitzen zentriert.

**`<` und `>`: in LaTeX-Drehbüchern `\lt` und `\gt` schreiben.** Seit der Umstellung
auf LaTeX (Standard, `"latex": true`) geht **jede** Formel durch `tex()` — auch die in
`@…@` eingebettete Prosa-Formel — und `tex()` maskiert selbst: aus `&lt;` wird `&amp;lt;`,
und im Bild steht dann der sichtbare Text „&lt;". MathJax bricht daran ab, `verify_mathjax.js`
meldet **Misplaced &** und der Pre-Flight blockiert den Commit.

Die LaTeX-Makros `\lt` und `\gt` enthalten kein HTML-Sonderzeichen und sind darum unter
beiden Pfaden richtig — sie sind der Weg, den man nimmt:

| | `formel` / `karte` / `box` / `@…@` | `text` / `notiz` / `titel` / `untertitel` / `aussage` / `liste` |
|---|---|---|
| kleiner als | `x \lt 3` | `Aus @x \lt 3@ folgt …` |
| grösser als | `x \gt 3` | `Aus @x \gt 3@ folgt …` |

Nur ausserhalb von `@…@` schreibt die Prosa das Zeichen direkt (`Aus x < 3 folgt …`); dort
escapt `text_html()` selbst, und ein `&lt;` erschiene als sichtbarer Text „&lt;".

Die alte Regel `&lt;` / `&gt;` galt der eigenen Schreibweise (`"latex": false`), wo
`formel()` nicht maskiert. Nachgemessen am 06.09.2026 an den 26 Drehbüchern der
Übungsprüfung: 8 Ausdrücke in 6 Dateien fielen als **Misplaced &** durch, nach der
Umstellung auf `\lt` / `\gt` waren es 0 von 765.

Für `≤` und `≥` gibt es keine Falle: `<=` und `>=` werden in beiden Fällen ersetzt.

**Vor `inf` braucht es ein echtes Minuszeichen.** `-inf` ergibt `-∞` mit ASCII-Bindestrich
statt `−∞`. Grund: Die Wortersetzung `inf` → `∞` läuft **vor** den Minus-Regeln, und `∞`
ist kein Wortzeichen — danach greift keine der Regeln mehr, die aus `-` ein `−` machen. Im
Drehbuch also `]−inf; -3[` schreiben, mit `−` (U+2212) an der ersten Stelle und dem
normalen `-` an der zweiten, wo die Ersetzung greift. Ergibt `]−∞; −3[`, wie es
STYLEGUIDE §2.7 verlangt.

**Eine gehaltene Ankerzeile belegt die oberste Zeile — Folgeszenen müssen tiefer
beginnen.** Steht auf einem Element `halten`, bleibt es über die folgenden Szenen stehen.
Deren `oben` muss dann unter der Ankerzeile liegen, sonst rendern beide übereinander und
die Formeln stehen ineinander. Bewährt: die einführende Szene auf `oben: 178`, alle
Folgeszenen auf `oben: 348`. Beide bestehenden Clips machen es so.

---

## Die Bühne ist geteilt

`clipBuehne(quelle, titel)` in `mathlib.js` ist nicht nur für Lektionsseiten da — die
Leitprogramme unter `leitprogramme/` binden dieselbe Funktion ein. Wer an ihr etwas
ändert, ändert es dort mit.

Seit dem 01.09.2026 tut sie zwei Dinge mehr, die vorher nur die Kopie im Leitprogramm
konnte: Sie **sperrt das Scrollen**, solange sie offen ist (sonst wandert die Seite
darunter weg, und beim Schliessen ist man woanders), und sie **gibt den Fokus zurück**
an den Knopf, der sie geöffnet hat (sonst landet er am Seitenanfang).

## Ein Bauer für beide Fächer (seit 07.10.2026)

`scripts/build-clips.py` ist in Mathe und Physik **derselbe Code** (Abgleich: KERN, Grundlinie 0.99).
Verschieden sind nur drei Einstellungen am Dateianfang und der Seitenname:

| Einstellung | Mathe | Physik | Wirkung |
|---|---|---|---|
| `KARO_OHNE_ACHSEN` | `True` | `False` | Karo bei `"achsen": false` (Planimetrie steht im Karo) |
| `TEXTBREITE_BEGRENZEN` | `False` | `True` | Rand 130 px bei zentrierten Zeilen, Spaltenbreite bei links gesetztem Text |

`TEXTBREITE_BEGRENZEN = True` hätte in Mathe 62 Textelemente in 56 Clips neu umbrechen lassen
(im Browser an allen 514 Clips gemessen, alter gegen neuen Bau). Das Feld `"werkzeug"` im Index
(Rechner-Clips) braucht nur Mathe. **Eine Korrektur am Bauer gehört in beide Repos**: hier
einbauen, in `TODO-schwesterprojekt.md` und in der Warteschlange `OFFEN` von `scripts/abgleich.py`
vermerken. Wer eine neue Geschmacksfrage findet, macht daraus eine weitere Einstellung, keine Abzweigung.

## Bibliotheksseite `clips.html`

**Je Themenseite drei Spalten** (seit 06.10.2026). Innerhalb eines Lerngebiets steht jede
Themenseite mit ihrer Nummer als Zwischenüberschrift (Link zur Seite), darunter eine
dreispaltige Tabelle: **Animationen** (Clips mit `animation`), **Leitprogramm** (die eigenen
Clips der sichtbaren Leitprogramme, `"probe": true`, in der Reihenfolge des Leitprogramms;
die Spaltenüberschrift verlinkt es; jede Zeile trägt vorn den Link «LP» auf die Animation
ihres Kapitels im Leitprogramm, `#simN`, wie «Anim» bei den Clips der Themenseiten) und
**Weitere Clips** (alle übrigen).

**Farben in der Tabelle:** Spalte 1 hinterlegt, mit «Anim», in der Bereichsfarbe (GF blau, SP violett; auf den
Themenseiten bleibt sie blau).
Spalte 3 ruhig: weisse Zeilen, Nummer in der Bereichsfarbe (GF blau, SP violett) statt
der Reihen-Nuancen; Spalte 2 in einem helleren Ton der Bereichsfarbe hinterlegt (#eef4fb / #f5f1fb, heller als
die Animationen), mit «LP» — kein Orange oder Bernstein (das ist die Physik). Taschenrechner-Clips (`werkzeug`) stechen heraus: dunkle
Zeile (`--tinte`) mit Marke «TR». Ein
Bibliotheksclip, den ein Leitprogramm mitbenutzt, bleibt in Spalte 1 oder 3. Unter 720 px
stehen die Spalten untereinander.

Gebaut wird der Block von `scripts/clips_bibliothek.py` (nur Mathe); `build-clips-einbau.py`
ruft es auf und liefert Zeilenform (`zeile()`), Ordnung und Marken — so bleibt das geteilte
Skript nahe an der Physik-Fassung. Spalten 1 und 3 ordnet `ordnung()` (Reihe, `folge`,
`REIHEN`): Spalte 1 folgt damit der Lage der Animationen auf der Seite, Spalte 2 dem
Leitprogramm. Reihen, deren Folge dem Aufbau der Themenseite folgt statt dem Alphabet
(1.2–1.4), stehen in `REIHEN_VORN` in `clips_bibliothek.py` — sie gelten auch für die
Clipblöcke der Themenseiten. «Sichtbar» heisst: von `leitprogramme.html` vor dem Abschnitt der alten
Leitprogramme verlinkt; deren Prüfungsclips bleiben draussen. Die Regeln stehen im
`<style>` von `clips.html`, nicht in `style.css`.



Die Übersicht über alle Clips, gruppiert nach Fach und darin nach Lerngebiet. Sie ist
**nicht** von Hand gepflegt: `build-clips-einbau.py` füllt auch dort einen Block,

```html
<!-- CLIPS-BIBLIOTHEK:ANFANG — generiert von scripts/build-clips-einbau.py, nicht von Hand ändern -->
<!-- CLIPS-BIBLIOTHEK:ENDE -->
```

und baut daraus eine **aufklappbare Übersicht, nach Fach und Lerngebiet** — dieselbe
Gliederung wie die Startseite. Die Gruppen kommen aus dem Block `GROUPS` in `nav.js`, nicht
aus dem Freitextfeld `lerngebiet` im Drehbuch: Sonst ergäbe ein Tippfehler dort eine neue
Gruppe. Lerngebiete ohne Clips werden weggelassen.

Die Lerngebiete stehen über die ganze Breite untereinander. **Zweispaltig ist erst die
Clipauswahl darin** — und zwar spaltenweise gefüllt: erst die linke Spalte von oben nach
unten, dann die rechte. Zeilenweise gefüllt würde eine nummerierte Reihe über beide
Spalten zickzacken (1 links, 2 rechts, 3 wieder links). Die Zeilenzahl setzt der Generator
je Gruppe als Inline-Stil, weil sie an der Anzahl Clips hängt; unter 720 px wird sie
zurückgenommen und alles steht untereinander.

Jede Gruppe ist beim Laden **zu** und nennt in der Kopfzeile Anzahl und Gesamtlaufzeit;
darin steht je Clip eine Zeile mit **nur Titel und Laufzeit**. Kurzbeschrieb, Verweise und
Transkript stehen bewusst nicht dort — sie gehören auf die Lektionsseite, wo der Clip im
Zusammenhang steht. Bei hundert Clips wären hundert Transkripte auf einer Seite das Ende
der Übersicht, und für die Suche zählen sie ohnehin schon dort.

Ein Clip mit mehreren `lektion`-Codes erscheint in jeder Gruppe, zu der er gehört — man
findet ihn dort, wo man sucht. Innerhalb einer Gruppe wird er nur einmal gezeigt, auch
wenn zwei seiner Lektionen darin liegen.

Ein neuer Clip erscheint automatisch, sobald sein Drehbuch gebaut ist.

Angebunden ist die Seite an drei Stellen — die sind schon gesetzt und müssen für neue
Clips nicht angefasst werden:

| Datei | was |
|---|---|
| `nav.js` | Eintrag `▶ Clips` im Menü *Nachschlagen*, in der Kopfzeile und im Mobilmenü |
| `scripts/build-seo.py` | Zeile in der `SEITEN`-Tabelle — Beschreibung, canonical, Sitemap |
| `scripts/build-suchindex.py` | `clips.html` in der Liste `ZUSATZSEITEN` |

Die Clip-Dateien selbst stehen bewusst **nicht** in der Sitemap: ohne Seitengerüst,
Navigation und Fussbereich wären sie als Landeseite aus einer Suche eine Sackgasse.
Für Suchmaschinen tragen `clips.html` und die Lektionsseite das Transkript; die
site-eigene Suche führt seit dem 13.09.2026 auf `clips.html#clip-<name>`, also auf die
einzelne Zeile in der Bibliothek.

---

## Pre-Flight

Clips werden mitgeprüft, wenn man sie übergibt:

```sh
python3 .claude/skills/preflight/preflight.py grundlagen/*.html schwerpunkt/*.html clips/*.html clips.html
```

Auf den Clip-Bühnen laufen nur die allgemeinen Checks (Tag-Bilanz, doppelte IDs, kein ß,
Dezimalpunkt, keine Fremdhosts) — Skelett-, nav- und Ressourcen-Checks gelten für sie
nicht, sie haben kein Seitengerüst.

Dazu kommt eine Konsistenzprüfung der Ablage, die immer läuft:

- jeder `clips.json`-Eintrag hat eine Datei → sonst `[FEHLER]` (toter Knopf in der Bibliothek)
- jede Datei steht in `clips.json` → sonst `[FEHLER]` (fehlt lautlos in der Bibliothek)
- jedes `lektion`-Kürzel existiert in `nav.js` → sonst `[FEHLER]` (landet auf keiner Seite)
- Sprechertext vorhanden → sonst `[WARN]` (die Seite bekommt kein Transkript)

---

## Ton

Alle vier Clips haben eine gesprochene Tonspur, lokal erzeugt.

### Warum es überhaupt passt

Der Sprechertext steht schon je Szene im Drehbuch. Bisher wurde daraus die Szenendauer nur
**geschätzt** (`Wörter / sprechtempo`). `scripts/build-clip-ton.py` misst stattdessen die
echte Länge und schreibt sie als Feld `dauer` ins Drehbuch zurück — danach stimmt Bild zu
Sprache exakt statt ungefähr.

### Und darum gehört `nachlauf` ins Drehbuch

Die alte Schätzung veranschlagte rund 1.5 s mehr, als die Stimme wirklich braucht. Diese
Dehnung war ein Fehler — aber sie leistete unbeabsichtigt etwas: Sie liess die letzte Zeile
einer Szene länger stehen. Als die Messung den Fehler entfernte, fiel die Standzeit überall
auf den Standard `nachlauf = 2.6 s` zusammen, im Merkbild von 5.3 s herunter.

**Darum setzen alle Clips `nachlauf: 4.0`.** Damit steht jede letzte Zeile vier Sekunden,
und der Wert ist eine Entscheidung statt ein Nebenprodukt einer Schätzformel. Wer einen
neuen Clip anlegt, setzt ihn mit — sonst läuft dieser eine schneller als die anderen.
Kontrollieren lässt sich das mit `dauer − letzte Einblendung` je Szene; bei allen vier
Clips ergibt das durchgehend 4.0 s.

### Einrichten

```sh
pip install piper-tts soundfile
# Stimme laden: rhasspy/piper-voices → de/de_DE/thorsten/high (rund 109 MB)
export PIPER_MODELL=/pfad/de_DE-thorsten-high.onnx
```

Beides gehört **nicht ins Repo** — nur die fertige MP3 wird versioniert.

### Bauen

```sh
python3 scripts/build-clip-ton.py <clip>     # spricht, misst, schreibt dauer + ton/<clip>.mp3
python3 scripts/build-clips.py    <clip>     # baut den Clip mit den neuen Dauern
```

Die Reihenfolge ist zwingend: Das erste Skript ändert nur das Drehbuch und legt den Ton ab.

**Nur einzelne Szenen neu (seit 08.10.2026).** Piper klingt bei jedem Lauf etwas anders.
Nach einer Korrektur an einer Szene sollen die übrigen so bleiben, wie sie abgenommen wurden:

```sh
python3 scripts/build-clip-ton.py <clip> --szenen 2,5   # Nummern ab 1, wie die Ausgabe zählt
```

Gesprochen werden nur die Szenen 2 und 5; ihre `dauer` wird neu gemessen. Alle anderen
Szenen behalten `dauer` und Ton: Das Skript schneidet sie samt Stille aus der bisherigen
`ton/<clip>.mp3` (Lage nach den Dauern im Drehbuch) und setzt sie an ihren neuen Start.
Kopfraum 0.95 bekommen nur die neuen Stücke, die alte Spur hat ihn schon — der Pegel bleibt
gleich. Die übernommenen Szenen werden ein zweites Mal als MP3 kodiert (gemessen rund 3–4 %
RMS-Abweichung, nicht hörbar). Passt die Spur nicht mehr zum Drehbuch (Länge weicht über
0.05 s ab, etwa weil eine Szene dazukam oder eine `dauer` von Hand geändert wurde), bricht
das Skript ab — dann ganz vertonen. **Wer den Text einer Szene ändert, muss sie nennen:**
Das Skript merkt nicht, dass eine nicht genannte Szene neuen Text hat.

### Wie es im Clip läuft

- **Eine Spur je Clip**, nicht eine je Szene. Die Sprache sitzt an `Szenenstart + 0.4 s`,
  dazwischen ist Stille. Mit einer einzigen Spur gibt es nichts zu verketten und kein
  Stolpern an den Szenengrenzen. Rund die Hälfte der Spur ist Stille, das kostet fast nichts.
- **Der Ton versucht hörbar zu starten.** Der Clip wird durch einen Klick geöffnet,
  darum lässt der Browser das meist zu; das `<iframe>` bekommt dafür `allow="autoplay"`.
  Wehrt der Browser sich, fällt es lautlos auf stumm zurück und der Knopf „🔇 Ton an"
  macht daraus die nötige Geste. Nie stumm *und* ohne Knopf — sonst wäre der Ton
  unerreichbar.
- **Sobald der Ton läuft, führt er die Uhr** (`t = ton.currentTime`). Tondrift fällt auf,
  Bilddrift nicht. Läuft kein Ton, zählt wie bisher `requestAnimationFrame`.
- Pause, Spulen, Neustart nehmen den Ton mit. Gemessene Abweichung Ton/Bild: 0.01–0.06 s.
- Ohne Tonspur ändert sich am Clip **nichts** — der Ton ist eine Zutat, keine Voraussetzung.

### Stolperstein beim lokalen Prüfen

**`python3 -m http.server` beherrscht keine Range-Requests.** Ohne die kann der Browser in
einer MP3 nicht springen: Der Klick auf den Fortschrittsbalken wirft den Ton an den Anfang
zurück, und es sieht nach einem Fehler im Clip aus. GitHub Pages beherrscht sie. Zum
lokalen Testen einen Server mit Range nehmen, sonst jagt man ein Phantom.

### Grösse und Qualität

Sprache als MP3 mono bei rund 50 kbit/s kostet etwa 3.3 kB je Sekunde — die vier Clips
zusammen **912 kB**. `--qualitaet` steuert das
(0.0 gross bis 1.0 klein). Die Spur bekommt Kopfraum auf 0.95, sonst übersteuert der
Encoder — Piper steuert einzelne Sätze bis an die Grenze aus.

Opus wäre kleiner, scheidet aber vorerst aus: libsndfile schreibt Opus nur bei 8/12/16/24/48 kHz,
Piper liefert 22.05 kHz. Ohne Resampling bleibt MP3 — das dafür überall abspielbar ist.

### Aussprache

Liest die Stimme ein Fremdwort falsch, kommt es in `AUSSPRACHE` in
`scripts/build-clip-ton.py`: Wortstamm und Lautschrift (IPA), Piper erhält es als
`[[…]]`. Buchstabierte Abkürzungen stehen in `ABKUERZUNGEN` (nur exakt als ganzes
Wort), einfache Worttausche ohne Lautschrift in `TAUSCH` (achthundert). Vorsilben
(Mega-, Kilo-, …) und Zusammensetzungen greifen mit — «Megahertz» fällt unter
«hertz». Getauscht wird nur im Text an Piper; Drehbuch, Sprechertext und Suchindex
behalten die Schreibweise. Das Skript ist **dasselbe wie in TALS Physik** (Grundlinie
1.000 in `scripts/abgleich.py`); die Tabellen sind nach Hörproben des Auftraggebers
entschieden und gelten für Thorsten in beiden Repos. Ein neuer Eintrag hier gehört
darum auch drüben hin — per `TODO-schwesterprojekt.md`, nicht quer editiert.

Zwei Fallen, beide im Skript abgefangen: Ein Satzzeichen direkt nach `]]` verschluckt
Piper samt Pause und klebt das nächste Wort an — es gehört in die Klammer. Und ohne
Wortgrenze träfe «ampere» auch «Schlamperei». Probe vor dem Eintrag:
`PiperVoice.load(modell).phonemize(text)` zeigt, was die Stimme daraus macht;
Hörproben mit `synthesize_wav`.

*Problemwörter finden* — zwei Durchgänge über alle Drehbücher: (1) nach Schreibung:
Personennamen, Einheiten, Abkürzungen, Fremdschreibungen (c, y, ph, th, ou …)
phonemisieren und die Lautschrift lesen; (2) über **alle** Wörter der Sprechertexte:
englische Laute (ɹ, ð, θ, w, æ …) und Wörter mit drei und mehr Silben ohne
Hauptbetonung. Ein deutsches Wort, das nur auf der falschen Silbe betont ist, findet
keiner der beiden — das hört man nur. *Hörproben zeigen:* je Wort «bisher» und
«Vorschlag» als WAV, dazu eine kleine `index.html` mit `<audio>`-Knöpfen im selben
Ordner; im Windows-Browser über `file://wsl.localhost/Ubuntu/<pfad>/index.html` öffnen.
Nach einem neuen Eintrag die betroffenen Clips ermitteln (`aussprache(text) != text`)
und neu vertonen — am 27.09.2026 waren es neun (Pythagoras 7, Megahertz 1,
achthundert 1).

### Lizenzlage (geprüft am 30.08.2026)

| | |
|---|---|
| Piper, aktuell (`OHF-Voice/piper1-gpl`) | **GPL-3.0** |
| Piper, alt (`rhasspy/piper`) | MIT, am 06.10.2025 archiviert |
| Stimme `de_DE-thorsten` (Datensatz Thorsten-Voice) | **CC0-1.0** |

Die GPL regelt die Weitergabe des **Programms**, nicht das, was es erzeugt — und Piper
kommt ohnehin nicht ins Repo. Die Stimme steht unter CC0: keine Einschränkung auf
nicht-kommerzielle Nutzung, keine Namensnennung nötig. Der Autor Thorsten Müller freut
sich über eine Nennung.

**Nicht geprüft:** Die deutsche Thorsten-Stimme wurde nicht von Grund auf trainiert,
sondern aus der englischen Lessac-Stimme feinabgestimmt. Ob deren Herkunftsdaten
Bedingungen mitbringen, die ins abgeleitete Modell hineinreichen, ist offen. Ebenso
ungeprüft: die Lizenzen der übrigen sieben deutschen Stimmen.

---

## Die Umstellung auf LaTeX (31.08.2026)

Alle 28 Drehbücher wurden umgestellt — 371 Formelzeilen. `scripts/clip-nach-latex.py`
hat das gemacht und bleibt im Repo: als Beleg, was mit den Zeilen geschehen ist, und
falls irgendwo noch ein Drehbuch in der alten Schreibweise auftaucht.

`"latex": false` schaltet ein einzelnes Drehbuch auf die alte Schreibweise zurück;
`formel()` in `scripts/build-clips.py` ist unangetastet.

### Was die Umstellung gekostet hat

| | |
|---|---|
| Drehbücher | 28 |
| übersetzte Zeilen | 371 |
| davon rein mechanisch | 279 |
| davon mit Prosa dazwischen | 102 — hier musste die Grenze Mathematik/Text gezogen werden |
| Ton | **unverändert.** Es wurde kein Wort neu gesprochen: der Umbau betraf die Formeln, nicht den Sprechertext, und damit auch keine Dauer |
| Lektionsseiten, `clips.json`, Suchindex | **unverändert** — Titel und Längen sind dieselben |
| Layout | eine einzige Kollision (`g1-2-zahlformen`, 5 px), behoben mit 40 px mehr `abstand` |

### Fehler, die der Umbau selbst produziert hat

Alle vier fielen erst in der Prüfung auf, keiner im Augenschein:

1. **`A \ B` verlor das Zeichen.** Der Backslash der Mengendifferenz wurde in LaTeX zu
   einem Abstandsbefehl — die Differenz sah aus wie ein Produkt. 6 Zeilen.
2. **`\%` wurde zur Mengendifferenz.** Dieselbe Regel, eine Rekursion zu spät angewandt:
   sie traf den Backslash eines schon gesetzten `\%`.
3. **`x_{1,2}` und `\tan^{-1}`** bekamen Mengenklammern: die geschweiften Klammern einer
   Hoch- oder Tiefstellung wurden escaped wie die einer Menge.
4. **`√(1+8)`** verlor die Wurzel: der Radikand steht in der alten Schreibweise *neben*
   dem Zeichen, in LaTeX gehört er *hinein*.

### Wie geprüft wurde

Nicht durch Ansehen — 28 Clips mit rund 150 Szenen sah damals niemand vollständig durch, und heute sind es 88.

**Textvergleich.** `.claude/tools/clip-text.mjs` liest den sichtbaren Text jeder Zeile.
Einmal vor dem Umbau, einmal danach, dann Zeile gegen Zeile. Von 719 Zeilen blieben 31
Abweichungen übrig, alle derselben Art: MathJax zählt bei ä, ö, ü, ✓, ✗, ‰ und µ eine
Ersatzglyphe doppelt in die Textauslese — **im Bild steht sie nicht**, an drei Stellen
mit Screenshots bestätigt.

**Layoutvergleich.** `.claude/tools/pruef-clip.mjs` zum Ende jeder Szene über alle 28
Clips: Überlappungen und Überlauf. LaTeX setzt Brüche etwas höher als der alte Satz —
darum war das der eigentliche Risikopunkt, und es blieb bei der einen Kollision.

### Was bleibt

**Zwei Serifenschriften in einem Bild.** Die Prosa steht in der Schrift des Clips, die
Formeln in der TeX-Schrift. Am deutlichsten in den roten Handnotizen, wenn dort ein
Formelstück steht. Ändern lässt sich das nicht: MathJax bringt eigene Glyphen mit.

**2 MB `tex-svg.js`.** Wer den Clip von einer Lektionsseite aus öffnet, hat die Datei im
Cache. Wer ihn direkt aufruft, lädt sie — gemessen 2190 statt 531 kB, 191 statt 119 ms.

---

## Stand und was offen bleibt

Mechanik und Inhalt stehen. Was bleibt, ist Feinarbeit und der Übertrag:

- **Der Bestand ist beisammen.** Stand 30.09.2026: **426 Drehbücher**, alle vertont —
  391 in der Bibliothek (362:25 min, 56 Reihen) und 35 unverlinkte Prüfungsclips mit
  `"probe": true` (28:07 min). **46 der 47 Themenseiten tragen Clips** und den Marker;
  ohne Clip ist nur `g4-0` (Praxisbeispiel, keine Animation). Seit den Animationsclips
  ist das Schwerpunktfach nicht mehr dünn besetzt: 259 Zuordnungen auf den 23
  GF-Seiten (Median 11 je Seite), 142 auf den 23 SF-Seiten (Median 6).

- **Der Rechner ist ein eigener Strang.** 22 der 391 Clips tragen `werkzeug: true`
  (31:38 min) und liegen auf 14 Seiten — von `g1-2` (Brüche, ggT und kgV) bis `s4-2a`
  (Formeln mehrfach auswerten). Sie bilden keine eigene Reihe, sondern hängen als
  letzter Clip an der Reihe, deren Stoff sie bedienen. Die Belegquellen stehen oben
  unter «Rechneranzeige». Offene Gerätefragen gibt es seit dem 30.09.2026 keine mehr:
  drei hat die TI-Online-Hilfe beantwortet, zwei der Auftraggeber am Gerät.

- **Ein Clip kann auf mehreren Seiten stehen — auch fachübergreifend.** `lektion` ist
  eine Liste; ein zweiter Eintrag kostet eine Zeile und keine Produktion. Am 07.09.2026
  hat `s1-2-potenzen` auf diesem Weg sechs Clips aus `g1-4` bekommen, weil die Seite
  denselben Stoff behandelt und die Clips ohnehin `stufe: ["BM1", "BM2"]` tragen.
  Acht Clips stehen heute auf Seiten beider Fächer.
  **Zwei Dinge vorher prüfen:** ob die `stufe` passt, und ob die Zielseite den Stoff
  wirklich auf derselben Höhe behandelt — sonst schickt man BM1-Material in eine
  BM2-Lektion. **Und nach dem Ändern der `lektion`-Liste muss jeder betroffene Clip
  einzeln neu gebaut werden**, sonst steht die alte Zuordnung weiter in `clips.json`
  und `build-clips-einbau.py` schreibt nichts.

  Verteilung (28.09.2026, Clips je Lerngebiet): Lerngebiet 1 mit 51, 2 mit 57, 3 mit 43,
  4 mit 28, 5 mit 79 — im Schwerpunktfach 1.x mit 20, 2.x mit 27, 3.x mit 62, 4.x mit 33.

  **Als Referenz für ein neues Drehbuch:**

  | Form | Clip |
  |---|---|
  | Herleitung Schritt für Schritt | `g2-2b-mitternachtsformel-herleitung` |
  | Rechnung mit Bedingung | `g2-2a-warum-a-ungleich-5` |
  | Fallunterscheidung mit Bild | `g2-3-anzahl-loesungen` |
  | durchgehende Bedingungsleiste | `g5-3-cosinussatz` |
  | Koordinatenbild | `g3-1-schnittpunkte` |
  | Boxplot | `g4-2-boxplot-lesen` |
  | Entscheidungsclip («welches Verfahren?») | `g5-3-welcher-satz` |
  | Gegenüberstellung robust/empfindlich | `g4-3-robust-oder-empfindlich` |

  **Ein durchgehendes Beispiel trägt eine ganze Reihe.** Bei den Parabeln ist es
  \(x^2-4x+3\) durch neun Clips, bei den Sätzen der Trigonometrie das Dreieck
  \(a=7,\ b=8,\ c=5,\ \alpha=60^\circ\) durch fünf, bei der Datenanalyse der Satz
  \(2,4,4,5,6,7,8,12\) durch fünfzehn. Wer eine neue Reihe anlegt, sucht zuerst dieses
  eine Beispiel — es spart in jedem Folgeclip die Einführung.
- **Urteil über die Stimme.** Alle Clips sind synthetisch vertont. Ob die Stimme im
  Unterricht trägt, ist noch nicht entschieden; falls nicht, ist der Wechsel auf eine
  eigene Aufnahme nur ein Dateiaustausch — das Verfahren bleibt dasselbe.
- **Untertitel.** Text und Zeitmarken liegen vor; eine WebVTT-Spur wäre fast geschenkt und
  funktioniert im Schulzimmer besser als Ton: lautlos abspielbar, an der Wand mitlesbar.
