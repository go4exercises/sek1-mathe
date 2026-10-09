# CLAUDE.md — Sek1-Mathe begreifbar

Statisches HTML/CSS/JS-Lehrmittel Mathematik für die **Sekundarstufe I**, gehostet via
GitHub Pages unter `sek1-mathe.begreifbar.ch`, verlinkt von `begreifbar.ch`.
Schwesterprojekte: **TALS Mathe** (`~/tals-mathe`, mathe.begreifbar.ch, Berufsmaturität)
und **TALS Physik** (`~/tals-physik`). Werkzeug, Aufbau, Menü, Kopf und Fusszeile sind
aus TALS Mathe übernommen (Stand 09.10.2026); verschieden sind nur **Bereichsfarbe** und
**Inhalt**.

**Detail-Konventionen stehen in `STYLEGUIDE.md`.** Es ist die Fassung aus TALS Mathe und
gilt hier mit den Abweichungen unten. Wo es von RLP-BM, Grundlagen-/Schwerpunktfach oder
`grundlagen/`/`schwerpunkt/` spricht, gilt sinngemäss: ein Bereich, Ordner `themen/`.

## Sprache & Notation (nicht verhandelbar — wie TALS Mathe)

- Schweizer Hochdeutsch. **Kein ß.**
- **Dezimaltrennzeichen ist der Punkt, nie das Komma** — überall: LaTeX, Aufgabentexte,
  Live-Anzeigen, JS-Code.
- MathJax-Delimiter: `\(…\)` inline, `\[…\]` abgesetzt. Niemals `$…$`.
- **Leere Menge als `\{\,\}`**, nie `\emptyset` oder `∅`.
- Zahlenmengen in LaTeX als `\mathbb{N}`, `\mathbb{Z}`, `\mathbb{Q}`; im Menü (kein
  MathJax) als ℕ, ℤ, ℚ.

## Farben

- **Bereichsfarbe: Petrol** (`--petrol`, `--petrol-hell`, `--petrol-rand` in
  `style.css`). Sie trägt Kopf, Menü, Links, Inhaltsverzeichnis, Startseite und
  Bedienelemente — überall dort, wo TALS Mathe `--blau` als Bereichsfarbe nutzt.
- **Didaktische Farben — dieselbe Bedeutung wie in TALS Mathe und Physik:**
  Blau = Definition/Theorie (`block-def`, 📘) · Grün = Beispiel/Lösung · Orange =
  Aufgabe/Übung (`block-aufg`) · Rot = Fehler/Achtung · Lila = Beweis/Herleitung ·
  Blau-Variante = Merksatz (`block-merksatz`, ⭐). Nie umdeuten, nie durch Petrol ersetzen.
- `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, `og-bild.png`: erzeugt von
  `node .claude/tools/build-bilder.mjs` (braucht Netz für Google Fonts).

## Projektstruktur

- `themen/` — 11 Themenseiten `t<Bereich>-<Nr>-<name>.html` in drei Bereichen
  (1 Arithmetik/Algebra: 1.1–1.4 · 2 Gleichungen: 2.1–2.2 · 3 Geometrie: 3.1–3.5).
  **Einzige Quelle der Seitenliste ist `nav.js`** (`SITE.themen`, `GROUPS.themen`);
  der Suchindex liest sie von dort. Neue Seite = Eintrag in `nav.js`, Karte in
  `index.html`, Eintrag in `scripts/build-seo.py` (`SEITEN`), prev/next der Nachbarn.
- Sub-Split bei grossen Themen: Buchstaben-Suffix (`t3-2a`, `t3-2b`).
- `mathlib.js`, `minicheck.js`, `anim-hinweise.js`, `suche.js`, `style.css` — **1:1 aus
  TALS Mathe**, ausser den Farb-Tokens in `style.css`. Ein Fix an diesen Dateien gehört
  in beide Repos: hier umsetzen und in `TODO-schwesterprojekt.md` vermerken (oder
  umgekehrt aus Mathe übernehmen).
- `glossar.html`, `formelsammlung.html`, `clips.html`, `leitprogramme.html` — die vier
  Nachschlag-Seiten, vorerst Gerüste.
- `clips/`, `leitprogramme/`, `downloads/themen/` — leer, Aufbau wie in TALS Mathe
  (`HOWTO-clips.md`, `HOWTO-leitprogramme.md`).
- Skelett-Quelle: `TEMPLATE.html` + `HOWTO-neue-themenseite.md`.
- Offene Anpassungen am übernommenen Werkzeug: **`TODO.md`**.

## Inhaltliche Regeln

- **Master-Schema je Seite vollständig:** eigener Einstieg, eigene Definition, eigene
  Aufgaben A1–A6 (optional A7 Vertiefung), eigene Zusammenfassung. Keine Verweise auf
  Nachbarseiten für fehlende Inhalte.
- Statt der RLP-Box: Box `rlp-kompetenzen` mit Titel «📋 Kompetenzen» (Klasse bleibt,
  das CSS hängt daran). **Keine erfundenen Lehrplan-Stellen** — ein Bezug auf den
  Lehrplan 21 oder einen kantonalen Lehrplan nur mit überprüfter Quelle.
- Aufgaben-Markup, Lernziele («Ich kann …», 4–6 Punkte), Slider-Farbkopplung: wie
  STYLEGUIDE.
- **Niveau Sek I:** Sprache und Beispiele für 12- bis 16-Jährige; Rechenwege
  kleinschrittig.

## Skelett & Klassen — kopieren, nicht erfinden

- Neue Seite / neuer Block: Skelett aus `TEMPLATE.html` oder einer Nachbarseite
  **1:1 kopieren**, nur Inhalt anpassen. Keine eigenen Klassennamen erfinden.
- Jede Seite mit `onclick="toggleL(…)"` **muss `mathlib.js` einbinden**. Mit
  `.anim-hinweis`-Markup → `anim-hinweise.js`. Mit `.minicheck`-Markup → `minicheck.js`.
- `buildNav({ bereich:'themen', id:'t2-1', kapitelNr:'2.1', … })`.

## Pre-Flight (verbindlich vor jedem Commit)

```bash
python3 .claude/skills/preflight/preflight.py themen/*.html
```

Erwartet: `ALLE CHECKS BESTANDEN`. `[FEHLER]` wird vor dem Commit behoben, `[WARN]`
ist kein Blocker. Stufe 2 braucht `node_modules` (`npm install`; lokal genügt ein
Symlink auf `~/tals-mathe/node_modules`). **Vom Repo-Root aufrufen.**
Nach Änderungen an Seiten oder `SEITEN`: `python3 scripts/build-seo.py` und
`python3 scripts/build-suchindex.py`.

## Verifikations-Standard

- **Alle Zahlenwerte vor dem Einbau mit `python3` nachrechnen** — nie aus dem Gedächtnis.
- Geometrie und Graphen von Canvas-Animationen vorab in Python durchrechnen.
- Render-Check bei 1280 px **und** 360 px: `node .claude/tools/render-check.mjs <seiten>`.
- Clips: `node .claude/tools/pruef-clip.mjs clips/<name>.html <sekunden…>`, Bilder ansehen.

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
