---
name: preflight
description: Pflicht-Qualitätscheck für Sek1-Mathe (Leitprogramme und Wurzelseiten). IMMER ausführen, bevor Änderungen an leitprogramme/*.html oder index.html committet werden. Zweistufig: schnelle Eigen-Checks (Tag-Bilanz, ß, Dezimalkomma in Math, doppelte IDs, Skelett, Phantom-Klassen, mathlib-Einbindung, Ressourcen-Marker) plus Aufruf der autoritativen Repo-Skripte verify_mathjax.js (echte Render-Prüfung), verify_js_runtime.js (JS-Laufzeit in jsdom) und check_identifier_collisions.py. Fehlen die npm-Module mathjax-full/jsdom, werden die Tiefen-Checks sauber übersprungen.
---

# Pre-Flight für Sek1-Mathe

Vor jedem Commit, der `leitprogramme/*.html` oder `index.html` betrifft. Themenseiten gibt es seit 09.10.2026 nicht mehr.
**Vom Repo-Wurzelverzeichnis aufrufen** (wegen `scripts/` und `node_modules/`).

## Ausführen

```bash
python3 .claude/skills/preflight/preflight.py leitprogramme/*.html index.html
```

## Erwartetes Ergebnis

Letzte Zeile `ALLE CHECKS BESTANDEN`, Exit 0. Jede `[FEHLER]`-Zeile vor dem Commit
beheben. `[WARN]` ist kein Blocker (typisch: npm-Modul fehlt -> Tiefen-Check übersprungen).

## Stufe 1 — schnelle Eigen-Checks (ohne Abhängigkeiten)

div/details-Bilanz · doppelte HTML-`id` · kein `ß` · Dezimalkomma in Body-Math
(Index-Listen `x_{1,2}` ausgenommen, Scripts ausgeklammert) · Skelett (`page-wrap`,
`main class="content"`, `nav.js` ohne `defer`) · Phantom-Klassen (`rlp` ist legitim) ·
`mathlib.js` eingebunden bei Lösungs-Toggles · Ressourcen-Strukturmarker.

## Stufe 2 — autoritative Repo-Skripte (in scripts/)

- **verify_mathjax.js** — rendert jeden Ausdruck mit `mathjax-full`, findet echte
  TeX-Fehler. Braucht `node_modules/mathjax-full`.
- **verify_js_runtime.js** — führt den Seiten-JS in jsdom aus, findet Laufzeitfehler.
  Braucht `node_modules/jsdom`.
- **check_identifier_collisions.py** — Inline-Symbole vs. mathlib/nav. Ohne npm.
- **check_todo_schwester** — liest `TODO-schwesterprojekt.md` im Schwesterrepo
  (Physik liest Mathes; Physik führt keine solche Datei, in Mathe schweigt der
  Check) und meldet offene Einträge unter «## Offen» als `[WARN]`. Schreibt nie.

Fehlt ein npm-Modul, meldet der Pre-Flight das als `[WARN]` und überspringt nur diesen
Teil. Einmalig installieren mit: `npm install mathjax-full jsdom` (im Repo-Root).
