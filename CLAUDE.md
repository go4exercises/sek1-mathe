# CLAUDE.md — Sek1-Mathe begreifbar

Statisches HTML/CSS/JS-Lehrmittel Mathematik für die **Sekundarstufe I**, gehostet via
GitHub Pages unter `sek1-mathe.begreifbar.ch`, verlinkt von `begreifbar.ch`.
Schwesterprojekte: **TALS Mathe** (`~/tals-mathe`, mathe.begreifbar.ch, Berufsmaturität)
und **TALS Physik** (`~/tals-physik`). Werkzeug, Menü, Kopf und Fusszeile sind aus TALS Mathe
übernommen (Stand 09.10.2026); verschieden sind **Bereichsfarbe**, **Aufbau** und **Inhalt**.

**Aufbau (Entscheid Auftraggeber 09.10.2026): Leitprogramme stehen im Zentrum. Es gibt keine
Themenseiten.** Die Startseite und das Menü zeigen nur fertige Leitprogramme. Vertieft wird mit
Links auf die Themenseiten von Mathe begreifbar (`https://mathe.begreifbar.ch/grundlagen/…`,
neuer Tab, Pfeil ↗).

**Detail-Konventionen stehen in `STYLEGUIDE.md`, das Vorgehen in `HOWTO-leitprogramme.md`.**
Beide sind die Fassungen aus TALS Mathe und gelten hier mit den Abweichungen unten. Wo sie von
RLP-BM, Grundlagen-/Schwerpunktfach, Themenseiten (`grundlagen/`, `schwerpunkt/`, Skelett,
`TEMPLATE.html`) sprechen, gilt: Das Leitprogramm ist selbst die fachliche Quelle; Notation und
Begriffe nach STYLEGUIDE; Vertiefung über TALS-Links statt Verweis auf eine eigene Themenseite.

## Sprache & Notation (nicht verhandelbar — wie TALS Mathe)

- Schweizer Hochdeutsch. **Kein ß.**
- **Dezimaltrennzeichen ist der Punkt, nie das Komma** — überall: LaTeX, Aufgabentexte,
  Live-Anzeigen, JS-Code.
- MathJax-Delimiter: `\(…\)` inline, `\[…\]` abgesetzt. Niemals `$…$`.
- **Leere Menge als `\{\,\}`**, nie `\emptyset` oder `∅`.
- Zahlenmengen in LaTeX als `\mathbb{N}`, `\mathbb{Z}`, `\mathbb{Q}`; im Menü (kein
  MathJax) als ℕ, ℤ, ℚ.
- ggT/kgV mit Strichpunkt: `\text{ggT}(12;\ 18)`. Ergebnisse als (unechte) Brüche, keine gemischten Zahlen.
- Kein Gedankenstrich unmittelbar vor oder nach einer Formel (STYLEGUIDE §2.8) — er liest sich als Minus.

## Farben

- **Bereichsfarbe: Petrol** (`--petrol`, `--petrol-hell`, `--petrol-rand` in
  `style.css`). Sie trägt Kopf, Menü, Links, Startseite, Leitprogramm-Karten und
  Bedienelemente — überall dort, wo TALS Mathe `--blau` als Bereichsfarbe nutzt.
- **Didaktische Farben — dieselbe Bedeutung wie in TALS Mathe und Physik:**
  Blau = Definition/Theorie/Merkkasten · Grün = Beispiel/Lösung/Ergebnis · Orange =
  Aufgabe/Übung · Rot = Fehler/Achtung · Lila = Beweis/Herleitung, Clipkarten.
  Nie umdeuten, nie durch Petrol ersetzen.
- `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, `og-bild.png`: erzeugt von
  `node .claude/tools/build-bilder.mjs` (braucht Netz für Google Fonts).

## Projektstruktur

- `leitprogramme/<name>.html` — die Inhaltsseiten. Jede wird aus `scripts/lp/<name>/seite.py`
  gebaut (README im Ordner); **nie die HTML-Datei direkt ändern**.
- **Einzige Quelle der Leitprogramm-Liste ist `nav.js`** (`SITE.leitprogramme`,
  `GROUPS.leitprogramme`); Menü und Suchindex lesen sie von dort, Clips verweisen mit
  `lektion` auf die `id`. Neues Leitprogramm = Eintrag in `nav.js`, Karte in `index.html`
  (Block `LEITPROGRAMME:ANFANG`, unter seinem Bereich), Eintrag in `scripts/build-seo.py`
  (`SEITEN`). Nur **fertige** Leitprogramme erscheinen; geplante nicht.
- Bereiche (Gruppierung): 1 Arithmetik/Algebra · 2 Gleichungen · 3 Funktionen · 4 Geometrie.
- `index.html` — Startseite mit den Leitprogramm-Karten. `leitprogramme.html` ist nur noch
  Weiterleitung auf `index.html#leitprogramme` (noindex).
- Clips der Leitprogramme: `clips/<präfix>-lp-*.json` (Drehbuch, Quelle), erzeugt mit
  `scripts/lp/<name>/clips.py`; `"probe": true` — nicht in der Bibliothek `clips.html`.
- Gesamttest und Bewertungspaket: `downloads/leitprogramme/<name>/*.tex` → PDF mit
  `python3 scripts/build-lp-pdf.py <name>`.
- `mathlib.js`, `minicheck.js`, `anim-hinweise.js`, `suche.js`, `style.css` — **1:1 aus
  TALS Mathe**, ausser den Farb-Tokens in `style.css`. Ein Fix an diesen Dateien gehört
  in beide Repos: hier umsetzen und in `TODO-schwesterprojekt.md` vermerken (oder
  umgekehrt aus Mathe übernehmen). Ebenso Fixes an gemeinsamen Bauskripten
  (`scripts/build-clip*.py`, `.claude/tools/*`).
- `glossar.html`, `formelsammlung.html`, `clips.html` — Nachschlag-Seiten, vorerst Gerüste.
- Offene Punkte: **`TODO.md`**.

## Inhaltliche Regeln

- **Ein Leitprogramm ist vollständig in sich:** Vorwissen, Kapitel nach dem Kapitelmuster
  (HOWTO-leitprogramme §4: Clip → Tüfteln → Kontrollclip → Festhalten → Üben → Aufgaben),
  Gesamttest. Keine Verweise auf fehlende eigene Seiten; Vertiefung nur als TALS-Link.
- Kompetenzen eigen formuliert («Das kannst du danach»), **keine erfundenen Lehrplan-Stellen** —
  ein Bezug auf den Lehrplan 21 oder einen kantonalen Lehrplan nur mit überprüfter Quelle.
- **Niveau Sek I:** Sprache und Beispiele für 12- bis 16-Jährige; Rechenwege
  kleinschrittig; Du-Form, kein «wir» (auch in Sprechertexten).
- Erkundungen, Kapitelaufgaben, Kontrollclips und Gesamttest wiederholen keine Beispiele
  aus Clip und Festhalten (HOWTO §9/§15).
- **Vor der Freischaltung** unabhängige Prüfung `/lp-pruefung leitprogramme/<name>.html`
  (HOWTO §15); Hörprobe und KI-Test des Bewertungspakets macht der Auftraggeber.

## Gerüst — kopieren, nicht erfinden

- Neues Leitprogramm: `scripts/lp/bruchrechnen/` als Vorlage kopieren (kopf.css, basis.js,
  seite.css/js/py, clips.py, zahlen.py, wortzeiten.py, pruef-schritte.mjs) und nur den Inhalt
  ersetzen; eigene `localStorage`-Schlüssel (`lp-<name>-*`). Keine eigenen Klassennamen
  erfinden, wo es eine passende gibt.
- Leitprogramm-Seiten rufen `buildNav({ bereich: 'lp', id: '<id aus nav.js>' })`.

## Pre-Flight (verbindlich vor jedem Commit)

```bash
python3 .claude/skills/preflight/preflight.py leitprogramme/*.html index.html
```

Erwartet: `ALLE CHECKS BESTANDEN`. `[FEHLER]` wird vor dem Commit behoben, `[WARN]`
ist kein Blocker. Stufe 2 braucht `node_modules` (`npm install`; lokal genügt ein
Symlink auf `~/tals-mathe/node_modules`). **Vom Repo-Root aufrufen.**
Nach Änderungen an Seiten, `nav.js` oder `SEITEN`: `python3 scripts/build-seo.py` und
`python3 scripts/build-suchindex.py`.
Dazu je Leitprogramm die Prüfungen aus seiner README (Zahlen, Übungen, Leisten, Fragen, Render).

## Verifikations-Standard

- **Alle Zahlenwerte vor dem Einbau mit `python3` nachrechnen** — nie aus dem Gedächtnis
  (`scripts/lp/<name>/zahlen.py`).
- Geometrie und Graphen von Animationen vorab in Python durchrechnen.
- Render-Check bei 1280 px **und** 360 px: `node .claude/tools/render-check.mjs <seiten>`.
- Clips: `SP=<scratchpad> node .claude/tools/pruef-clip.mjs clips/<name>.html <sekunden…>`,
  Bilder ansehen; Ton mit Whisper **medium** gegenhören (`wortzeiten.py`).
- PDFs ansehen: Read-Werkzeug ohne `pages`, oder pypdfium2 → PNG.

## Schwesterprojekte — lesen ja, schreiben nie

Aus einer Session in diesem Repo wird nur hier geschrieben. `~/tals-mathe` und
`~/tals-physik` dürfen gelesen werden (Vorlagen, Werkzeug-Stand vergleichen). Was dort
hingehört, kommt nach `TODO-schwesterprojekt.md` (was, wo, warum, nachgezählt).

## Arbeitsweise

- **Bei klarem Auftrag direkt umsetzen.** Annahme nötig → inline kurz erwähnen.
- **Keine ungebetene Verbesserungs-Initiative.**
- Mehr als 3 gleichartige Edits → ein Skript.

## Automatik: Commit nach jedem Durchgang

Modus `acceptEdits` (`.claude/settings.json`). Nach jedem abgeschlossenen Auftrag ohne
Rückfrage: Pre-Flight über die geänderten Seiten; **nur bei `ALLE CHECKS BESTANDEN`**
`git add -A` und `git commit`. **Niemals `git push`** — der Push bleibt beim Auftraggeber.
