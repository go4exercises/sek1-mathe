# HOWTO — Neue Themenseite ausarbeiten

Dieser Leitfaden beschreibt den Workflow für **eine neue Themenseite plus Materialien** (4 Druckseiten + 1 Anki-Deck). Die Schwerpunkt-Stubs sind inzwischen alle ausgearbeitet (Stand Juli 2026); der Ablauf gilt für jede neu hinzukommende Seite — etwa weitere TALS-Ergänzungen nach dem Muster von 3.6/4.3d.

Verwandte Dokumente: `STYLEGUIDE.md` (Pflicht-Konventionen), `CLAUDE.md` (Arbeitsweise mit Claude Code, Pre-Flight), `CHANGELOG.md` (Versions-Historie).

---

## Überblick

Eine vollständig ausgearbeitete Themenseite besteht aus:

```
grundlagen/<slug>.html                            ← die Themenseite (ca. 400–900 Zeilen HTML)
downloads/grundlagen/<slug>/
  ├── handout.html                                ← Theorie kompakt
  ├── teste-dich-selbst.html                      ← 12–15 Grundlagenaufgaben mit Lösungen
  ├── aufgabenserie.html                          ← 6 Anwendungsaufgaben mit Lösungen
  └── ankideck.apkg                               ← 15–30 Karten, Anki-kompatibel
```

Reihenfolge der Erstellung: **Themenseite zuerst, Materialien danach.** Inhalte der Themenseite sind die Substanz, aus der die Materialien gezogen werden.

---

## Schritt 1 — Themenseite

### 1a. Skelett aufsetzen

Vorlage ist eine fertige Themenseite des gleichen didaktischen Bereichs. Für Datenanalyse: `g4-2-diagramme.html`. Für Algebra: `g1-3-algebraische-terme.html`. Für Funktionen: `g3-2-lineare-funktionen.html`. Generell: nimm die strukturell ähnlichste fertige Seite und passe Inhalt + Titel + IDs an.

Das Pflicht-Skelett (laut STYLEGUIDE §6.1):

```html
<body>
  <div id="nav-root"></div>
  <div class="page-wrap">
    <main class="content">
      <!-- Inhalt: page-titel, rlp-kompetenzen, h2-Sektionen -->
    </main>
    <aside class="toc-wrap"><div id="toc"></div></aside>
  </div>
  <footer class="site-footer">
    <p><strong>Mathe begreifbar</strong> — Lernmaterial für die Berufsmaturität …</p>
    <p>Grundlagenfach <RLP-Nr> <Themenname></p>
  </footer>
  <script src="../nav.js"></script>
  <script src="../mathlib.js"></script>
  <script>buildNav({...});</script>
</body>
```

### 1b. h2-Standard-Schema

Die Sektion-IDs sollen aus diesem festen Vokabular kommen:

```
einstieg → definition → darstellungen → typen → theorie → aufgaben → zusammenfassung → downloads → ressourcen
```

Der **sichtbare h2-Text** darf themenspezifisch sein („Lagemasse — wo liegt die Mitte?"), aber die `id` bleibt aus dem Schema. So funktioniert die ToC-Sidebar konsistent.

### 1c. RLP-Kompetenzen-Block

Direkt unter dem `page-titel`, vor dem ersten h2. Format:

```html
<div class="rlp-kompetenzen">
  <div class="rlp-titel">📋 Kompetenzen nach RLP 2030 — Teilgebiet <RLP-Nr></div>
  <ul>
    <li>[wörtliche Übernahme aus RLP 2030, Seite 41–46]</li>
    ...
  </ul>
</div>
```

Kompetenz-Wortlaut: **1:1 aus dem RLP-PDF.** Nicht umformulieren, nicht zusammenfassen. Wenn der RLP „auch ohne Hilfsmittel" markiert, gehört das in eine Pill rechts neben dem Listen-Eintrag — Klasse `ohm`, im Pill-Text **ohne** umgebende Klammern (siehe STYLEGUIDE §3):

```html
<li>lineare Gleichungen lösen <span class="ohm">auch ohne Hilfsmittel</span></li>
```

Die Pill ist **nur** für exakt „auch ohne Hilfsmittel" zu setzen. Differenzierte RLP-Formulierungen (z.B. „mit und ohne Hilfsmittel" in s3-5 oder „kleine Stichproben auch ohne Hilfsmittel und grosse Stichproben mit Hilfsmitteln" in g4-3) bleiben Inline-Klammertext im Bullet, nicht Pill.

### 1d. Schriften und MathJax (Pflicht-Standard)

**Beides kommt aus dem Repo, nie von einem fremden Host** — siehe STYLEGUIDE §5.3.1. Der
Pre-Flight meldet `fonts.googleapis.com`, `fonts.gstatic.com` und `cdn.jsdelivr.net` als
`[FEHLER]`. Die Pfade sind relativ zur Tiefe der Seite; für `grundlagen/` und
`schwerpunkt/` also ein `../`:

```html
<link rel="stylesheet" href="../schriften.css">
<link rel="stylesheet" href="../style.css">
<script>
MathJax = {
  tex: { inlineMath:[['\\(','\\)']], displayMath:[['\\[','\\]']], packages:{'[+]':['boldsymbol']} },
  svg: { fontCache:'global', scale:1.05 },
  loader: { load:['[tex]/boldsymbol'] },
  options: { skipHtmlTags:['script','noscript','style','textarea'] }
};
</script>
<script src="../vendor/mathjax/tex-svg.js"></script>
```

`loader: { load:['[tex]/boldsymbol'] }` lädt die Erweiterung **relativ zum Pfad der
Startdatei** nach. Nicht nur diese eine: Auch `\textcolor`, `\cancel`, `\bbox`, `\class`,
`\enclose` und ein Dutzend weitere Befehle ziehen sich ihre Erweiterung selbst nach.
Darum liegt der Ordner `vendor/mathjax/input/tex/extensions/` **vollständig** im Repo.

**Fällt eine davon aus, bleibt die ganze Seite ohne Formelsatz** — nicht nur der eine
Ausdruck, und ohne Fehlermeldung im Bild. Genau das passierte am 31.8.2026 auf `g1-2`:
ein einziges `\textcolor`, dessen `color.js` fehlte, und alle 329 Ausdrücke standen als
roher LaTeX-Text da. Der Pre-Flight sieht das nicht — `verify_mathjax.js` setzt mit
`mathjax-full` aus `node_modules` und schaut nie in `vendor/`. Sichtbar wird es im
Netzwerk-Tab oder mit `node .claude/tools/pruef-mathjax.mjs <url>`.

**Nicht** `tex-chtml.js` (anderer Renderer, andere Optik). **Nicht** `window.MathJax = …` (das ist Legacy-Syntax, die manche Konfig-Pfade nicht annimmt).

### 1e. Farben und Fonts

Niemals Tailwind-Hex-Codes oder andere Hartfarben in Inline-Styles oder `<style>`-Blöcken. Stattdessen die CSS-Variablen aus `style.css`:

| Zweck | Variable |
|---|---|
| TALS-Blau (Hauptfarbe) | `var(--blau)` |
| Blau hell (Definitions-Hintergrund) | `var(--blau-hell)` |
| Grün (Beispiel-Akzent) | `var(--gruen)`, `var(--gruen-rand)` |
| Rot (Fehler/Warnung) | `var(--rot)`, `var(--rot-rand)` |
| Orange (Aufgabe) | `var(--orange)` |
| Lila (Beweis) | `var(--lila)` |
| Linienfarbe | `var(--linie)` |
| Papier-Hintergrund | `var(--papier)`, `var(--papier-2)` |
| Tinte (Text) | `var(--tinte)`, `var(--tinte-2)` |
| Monospace-Font | `var(--mono)` (= JetBrains Mono) |

### 1f. nav.js-Eintrag

Wenn die Seite neu ist, muss sie ins SITE-Array in `nav.js` eingetragen werden:

```js
{ id:'s1-1', nr:'1.1', titel:'Grundlagen', url:'schwerpunkt/s1-1-grundlagen.html' },
```

Die `id` ist die Kurzform (`s1-1`, nicht `s1-1-grundlagen`). Sie wird im `buildNav`-Aufruf der Seite referenziert für das Dropdown-Highlight.

### 1f-1. Animationen einbetten

Jede eigenständige Animation steht in einem `.widget` (Kopfzeile mit
`.widget-titelzeile` und Hinweispaar, darunter `.widget-body`) — die Klassen kommen
aus `style.css`, **nie in der Seite neu definieren**. Ohne Rahmen bleiben nur
Grafiken innerhalb eines `.block` und die zweite Ansicht einer bereits betitelten
Grafik. Verbindlich: STYLEGUIDE §2.10.

### 1f-2. Metadaten eintragen (Auffindbarkeit)

Neue Seite in der Tabelle `SEITEN` von `scripts/build-seo.py` eintragen —
`beschreibung` (140–165 Zeichen, mit den Begriffen, die jemand tatsächlich sucht),
`themen` (Stichworte) und `tg` (Teilgebiet für `educationalAlignment`; weglassen,
wenn die Seite keine RLP-Kompetenzbox trägt). Dann:

```bash
python3 scripts/build-seo.py
```

Das schreibt den Kopfblock in die Seite und führt `sitemap.xml` nach. Ohne diesen
Schritt hat die Seite keine Beschreibung, keine Link-Vorschau und steht in keiner
Sitemap — der Pre-Flight meldet das als Warnung.

### 1g. Pre-Flight-Check

Nach dem Editieren auf der Konsole im Repo-Root:

```bash
for f in grundlagen/g*.html schwerpunkt/s*.html; do
  pw=$(grep -c "page-wrap" "$f")
  mc=$(grep -c 'main class="content"' "$f")
  bn=$(grep -cE 'buildNav\(\{' "$f")
  toc=$(grep -c 'id="toc"' "$f")
  sf=$(grep -c '<footer class="site-footer"' "$f")
  bad=$(grep -cE 'class="(inhalt|brot|seiten-kopf|rlp\b|rlp-list|rlp-label|seiten-fuss|dl-box|ressourcen-grid|ress|ress-titel|ress-beschr|ress-quelle)"' "$f")
  if [ "$pw" -ne 1 ] || [ "$mc" -ne 1 ] || [ "$bn" -ne 1 ] || [ "$toc" -ne 1 ] || [ "$sf" -ne 1 ] || [ "$bad" -ne 0 ]; then
    printf "%-55s pw=%s mc=%s bn=%s toc=%s sf=%s bad=%s\n" "$(basename $f)" "$pw" "$mc" "$bn" "$toc" "$sf" "$bad"
  fi
done
echo "Pre-Flight fertig."
```

Wenn die Zeile mit der bearbeiteten Datei nicht erscheint → alles grün. Sonst zeigen die Werte, welche Konvention verletzt ist.

---

## Schritt 2 — Materialien (Druckseiten)

Sobald die Themenseite inhaltlich steht, werden die 4 HTML-Druckseiten aus den Inhalten der Themenseite generiert. **Die Materialien sind Auszüge und Vertiefungen, keine Kopien.**

### 2a. Vorlage

Schlanker Stil: `downloads/grundlagen/g5-1-grundlagen/*.html`. Jede der 4 Druckseiten hat den gleichen Aufbau:

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Rolle} · {Thema} — Mathe begreifbar</title>
  <link rel="stylesheet" href="../../../schriften.css">
  <link rel="stylesheet" href="../../print.css">
  <script>MathJax = {…};</script>
  <script src="../../../vendor/mathjax/tex-svg.js"></script>
</head>
<body>
  <div class="druck-bar no-print">
    <a class="db-back" href="../../../grundlagen/{themenseite}#downloads">← zurück zur Themenseite</a>
    <span class="db-info">{Rolle} · A4 · Bereit zum Drucken</span>
    <button class="db-print" onclick="window.print()">Seite drucken</button>
  </div>
  <div class="druck-wrapper">
    <header class="doc-kopf">
      <div class="dk-bereich">Mathe begreifbar · Grundlagenfach · {RLP-Nr} {Thema}</div>
      <h1>{Rolle-H1}</h1>
    </header>
    <!-- Inhalt -->
  </div>
</body>
</html>
```

### 2b. Inhalt pro Rolle

| Datei | Umfang | Stil | Zweck |
|---|---|---|---|
| `handout.html` | ~150–250 Zeilen | Theorie mit didaktischen Block-Klassen (block-def, block-tipp, block-fehler) und FTB-Tabellen | Lesetext: was muss man wissen? |
| `teste-dich-selbst.html` | ~100–150 Zeilen, 12–15 Aufgaben | nummerierte Liste oben, Lösungen unten in derselben Datei | Selbstkontrolle der Grundlagen |
| `aufgabenserie.html` | ~200–300 Zeilen, 6 Aufgaben | Aufgaben in `block-aufg`-Boxen, Lösungen in `block-bsp`-Boxen darunter | Anwendungsaufgaben mit Lebensbezug |

### 2c. Generator-Skript für eine Themen-Serie

Für die g4-Reihe wurde `scripts/build_print_g4.py` als Generator genutzt: HTML-Skelett als Template, Inhalt pro Druckseite als Python-Triple-Quoted-String, Generation in einer Schleife. **Dieses Pattern ist gut für eine 3er- oder 4er-Themen-Serie** (gleicher Lerngebiet-Bereich), aber Overkill für eine einzelne Themenseite.

In der Praxis hat sich für den gesamten Schwerpunkt-Ausbau **ein einziger Generator** bewährt: `scripts/build_print_s3.py` enthält die Blöcke aller Schwerpunkt-Seiten (A–W, ein Buchstabe pro Seite) und reproduziert bestehende Ausgaben byte-identisch — neue Seiten werden dort als weiterer Block plus `SEITEN`-Einträge ergänzt.

Alternativ: einzeln per Hand. Bei einer einzelnen Themenseite ist das genauso schnell.

---

## Schritt 3 — Anki-Deck

### 3a. Inhalt-Struktur

15–30 Karten pro Thema, in der bestehenden Schwarz-Weiß-Form: Front mit `<i>Begriff</i>` (Italic für Definitionsbegriffe), Back mit `<b>Schlüsselantwort</b>` (Bold für die Kernaussage). Jede Karte ein Konzept, kein Multi-Frage-Bandwurm.

Typische Karten-Typen pro Themenseite:
- **Definitions-Karten** (5–10): „Was ist eine Stichprobe?" → „Eine Teilmenge der Grundgesamtheit, die tatsächlich untersucht wird."
- **Formel-Karten** (3–6): „Mittelwert berechnen" → „x̄ = (1/n)·Σxᵢ"
- **Beispiel-Karten** (4–8): „Berechne den Median von 3, 5, 8, 10" → „n gerade. Mittel der Positionen 2 und 3: (5+8)/2 = **6.5**"
- **Faustregel-Karten** (2–4): „Wann Median statt Mittelwert?" → „Bei schiefer Verteilung oder mit Ausreissern."

### 3b. Kartenliste in `scripts/build_apkg.py` ergänzen

In `scripts/build_apkg.py` gibt es eine `NEW_DECKS`-Liste. Ein neuer Eintrag pro Thema:

```python
NEW_DECKS = [
    ...
    ('s1-1-grundlagen', '1.1 Grundlagen Schwerpunkt',
     'Schwerpunktfach · Vertiefung Algebra für TALS.', s11_cards),
]
```

Plus die Kartenliste als Python-Variable, im selben Skript darüber:

```python
s11_cards = [
    ("Was ist X?", "<b>Antwort</b> mit HTML-Formatierung."),
    ...
]
```

**Wichtig — Smartquote-Falle:** In Karten-Texten kommen oft deutsche Anführungszeichen `„…"` vor. Wenn ein Karten-Tupel mit `"…"` (Double-Quote-String in Python) anfängt **und** der Inhalt `"` enthält (das schließende deutsche Quote), schließt Python den String an der falschen Stelle. Lösung: Smartquotes als `\u201e` und `\u201c` schreiben:

```python
("Häufiger Fehler: \u201eSuggestive Fragen\u201c", ...)
```

Oder den ganzen String mit `'…'` (Single-Quote) statt `"…"` umschließen.

### 3c. Build laufen lassen

```bash
cd <repo-root>
python3 scripts/build_apkg.py
```

Erzeugt automatisch alle Decks neu, inklusive Self-Test am Ende (prüft SQLite-Schema, notes/cards-Konsistenz, Dateigröße).

---

## Schritt 4 — Verifikation

Vor dem Commit folgende Bash-Schnipsel laufen lassen:

### Konventions-Check (Massenpatches falls nötig)

Wenn neue Inhalte aus externer Vorlage übernommen wurden (z.B. bei Schwerpunktfach-Migration), kommen typische deutsche Konventionen mit (Dezimalkomma, ß, „Kosinus"). Die `scripts/_archiv/convert_*.py`-Skripte beseitigen das in Massen-Operation — Details siehe **STYLEGUIDE §6.3**:

```bash
python3 scripts/_archiv/convert_eszett.py        # ß → ss
python3 scripts/_archiv/convert_cosinus.py       # Kosinus → Cosinus
python3 scripts/_archiv/convert_decimals.py      # Dezimalkomma → Dezimalpunkt
python3 scripts/check_identifier_collisions.py
```

Anschliessend Verifikations-Loop (auch im STYLEGUIDE §6.3.6):

```python
import glob, sys
sys.path.insert(0, 'scripts')
import convert_decimals as cd
files = sorted(glob.glob('grundlagen/*.html') +
               glob.glob('downloads/grundlagen/**/*.html', recursive=True) +
               glob.glob('schwerpunkt/*.html'))
strays = sum(1 for fp in files if '\x00' in open(fp).read() or '\x01' in open(fp).read())
residue = sum(1 for fp in files if any(cd.verify_no_residuals(fp).values()))
ss = sum(open(fp).read().count('ß') for fp in files)
print(f"Stray: {strays} | Residuen: {residue} | ß: {ss}")
```

Erwartet: alle drei Zähler auf `0`.

### Pre-Flight aller Themenseiten

Siehe Schritt 1g.

### Broken-Link-Check Downloads

```bash
total=0; broken=0
for f in grundlagen/g*.html schwerpunkt/s*.html; do
  for url in $(grep -oE 'href="\.\./downloads/[^"]+"' "$f" | sed 's/href="//;s/"$//'); do
    total=$((total+1))
    rel="${url#../}"
    [ -f "$rel" ] || { broken=$((broken+1)); echo "MISSING: $f → $url"; }
  done
done
echo "Total: $total · Broken: $broken"
```

Erwartung: `Broken: 0`.

### Render-Test

Im Browser öffnen, durchscrollen, Sticky-ToC prüfen, Tabs (falls vorhanden) klicken, Druckseiten-Links auf der Themenseite ausprobieren.

Für **Canvas-Widgets** zusätzlich der automatisierte Rendercheck: das eigene Canvas in
`.claude/tools/screenshot-widgets.mjs` (Liste `WIDGETS`) eintragen und `npm run shots`
laufen lassen. Das Skript schiesst je Widget zwei PNGs (1280 px Desktop + 360 px Mobil)
nach `widget-shots/` und meldet leere/nicht gezeichnete Canvases (stiller JS-Fehler).
Beide Screenshots sichten — auf 360 px kollidieren Beschriftungen sonst leicht
(Label-Grössen an die Canvas-Breite koppeln, vgl. STYLEGUIDE). Playwright ist lokal
installiert, kein Setup nötig.

---

## Häufige Stolpersteine

1. **ToC fehlt → leere rechte Spalte.** Ursache: `<aside class="toc-wrap"></aside>` ohne inneres `<div id="toc"></div>`. Korrekt: `<aside class="toc-wrap"><div id="toc"></div></aside>`.
2. **MathJax rendert nicht.** Ursache 1: `tex-chtml.js` statt `tex-svg.js`. Ursache 2: `window.MathJax = …` statt `MathJax = …`. Beides nutzt nicht die Standard-Optik.
   - **Formeln rendern sporadisch leer (nur beim Hard-Refresh, beim Zurückblättern aber korrekt).** Ursache: eigene `MathJax.typesetPromise(…)`-Aufrufe beim Laden kollidieren mit dem Initial-Render von MathJax (Race, verstärkt durch `fontCache:'global'`). Lösung: zum Neu-Rendern von dynamisch (per `innerHTML`) geänderter Mathematik **immer `mjTypeset([el, …])` aus `mathlib.js`** verwenden statt direkt `MathJax.typesetPromise(…)`. Der Helfer serialisiert die Durchläufe und wartet auf `startup.promise`. Statisch im HTML stehende Formeln nicht erneut typesetzen — die rendert MathJax beim Laden selbst.
3. **Footer im falschen Bereich.** Muss **außerhalb** von `</main>` **und außerhalb** von `</div>` (page-wrap) stehen. Sonst zu schmal / nicht über die ganze Seite.
4. **Page-Titel ohne Lerngebiet-Lektionen.** Korrekt: `Grundlagenfach · Lerngebiet 4 · Datenanalyse · 20 Lektionen`. Die Lektionen-Zahl steht im RLP (Tabelle 6.4.4.1 für Gruppe 1, Tabelle 6.4.4.2 für Gruppe 2).
5. **`buildNav`-id passt nicht zu `nav.js`-SITE.** Wenn die Seite `id:'g4-3-masszahlen'` schreibt, aber `nav.js` `id:'g4-3'` hat, wird das aktuelle Kapitel im Dropdown nicht hervorgehoben. Konvention: Kurzform `<bereich-buchstabe><lerngebiet>-<teilgebiet>`, also `g4-3` oder `s1-1`. Ausnahme: eine Seite ohne eigene RLP-Nummer wie `g2-modellieren` trägt `g2-M` (STYLEGUIDE, Naming-Regeln).
6. **Smartquotes in `build_apkg.py`.** Siehe Schritt 3b.
7. **Materialien verlinkt, aber Ordner leer.** Themenseite wird auf der Homepage als „fertig" markiert, aber `downloads/grundlagen/<slug>/` enthält noch keine Files. Resultat: 5 broken Links pro Thema. Materialien erst nach Themenseite anlegen, dann Status setzen.
8. **Canvas-Animationen unscharf auf Retina/HiDPI-Displays.** Ursache: die `initCv`-Funktion skaliert den Canvas-Buffer nicht auf die physische Display-Auflösung. Korrekte Implementierung mit `devicePixelRatio` und `dataset.logicalW/H` siehe STYLEGUIDE §5.5.1.

---

## Checkliste vor dem Commit

- [ ] Pre-Flight-Check für die neue Seite grün (`pw=1 mc=1 bn=1 toc=1 sf=1 bad=0`)
- [ ] RLP-Kompetenzen wörtlich übernommen, nicht umformuliert
- [ ] h2-IDs aus dem Standard-Schema, sprechende Titel als sichtbarer Text
- [ ] Page-Titel mit „· N Lektionen" am Ende
- [ ] Skript-Reihenfolge `nav.js` vor `mathlib.js` (falls letzteres genutzt wird)
- [ ] Eintrag in `nav.js` SITE-Array ergänzt
- [ ] 4 Druckseiten + 1 Anki-Deck erzeugt, alle Links heil
- [ ] Broken-Link-Check global: 0 broken
- [ ] CHANGELOG.md-Eintrag in der nächsten Version
- [ ] Anki-Deck mit Anki-Desktop testweise importiert (manuell vor Release)

---

## Verwandte Ressourcen

- **`STYLEGUIDE.md`** — verbindliche Konventionen (Pre-Flight-Check-Spezifikation, Klassen-Namen, Pflicht-Skelett, h2-Standard-Schema, Werkzeug-Skripte §6.3)
- **`HOWTO-externe-ressourcen.md`** — Schritt-für-Schritt-Anleitung für die Sektion „Externe Videos &amp; Aufgabensammlungen". Anbieter-Reihenfolge, `web_fetch`-Verifikation, Anbieter-Map mit bereits verifizierten Playlist-IDs.
- **`CLAUDE.md`** — regelt die Arbeitsweise mit Claude Code (Pre-Flight, Commit nach jedem Durchgang, Schwesterprojekt). Ersetzt die frühere `COLLABORATION.md` aus dem Project-Knowledge des Claude-Projekts.
- **`scripts/build_apkg.py`** — Anki-Build-Skript, parametrisiert über `NEW_DECKS`-Liste
- **`scripts/build_print_g4.py`** — Druckseiten-Generator für die g4-Reihe (Vorlage für analoge Generatoren)
- **`scripts/_archiv/convert_*.py`** — Massenpatch-Skripte für Konventions-Erzwingung: `convert_eszett.py` (ß→ss), `convert_cosinus.py` (Kosinus→Cosinus), `convert_decimals.py` (Komma→Punkt, plus `verify_no_residuals`-Helper), `convert_punktkoord.py` (Punkt-Koord-Notation, Template-Pattern). Details: STYLEGUIDE §6.3.
- **`scripts/check_identifier_collisions.py`** — prüft Top-Level-JS-Identifier auf Kollisionen mit `nav.js` / `mathlib.js`. Details: STYLEGUIDE §6.2.
- **`CHANGELOG.md`** — was wurde wann geändert
- **RLP 2030 (SBFI)** — Quelldokument für die Kompetenz-Wortlaute. Lerngebiete 1–5 Grundlagen TALS auf Seiten 41–44, Schwerpunkt TALS auf Seiten 90 ff.
