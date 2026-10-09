---
name: lp-pruefung
description: Unabhängige fachliche und didaktische Prüfung eines Leitprogramms vor der Freischaltung (HOWTO-leitprogramme §15). Startet drei frische Agenten parallel — Seite, Clips, PDFs —, die nur lesen, jede Zahl mit python3 nachrechnen und gegen die Prüfliste in §15 prüfen. Die Befunde werden nachgeprüft und nach TODO.md geschrieben. Aufruf mit dem Pfad der Seite, z. B. /lp-pruefung leitprogramme/quadratische-funktionen.html. Ändert nichts am Leitprogramm.
---

# Prüfung eines Leitprogramms

Argument: Pfad der Seite, `leitprogramme/<name>.html`. Ohne Argument nachfragen.
Vom Repo-Wurzelverzeichnis arbeiten. Die Prüfung **ändert nichts** am Leitprogramm;
behoben wird erst auf Auftrag.

## 1 · Bestand erheben

```bash
S=leitprogramme/<name>.html
grep -o 'clips/[a-z0-9-]*\.html' $S | sort -u                 # Clips
ls downloads/leitprogramme/<name>/ 2>/dev/null                 # PDFs + .tex
ls scripts/lp/<name>/ 2>/dev/null                              # Bauskripte (Quelle der Seite)
grep -o 'grundlagen/[a-z0-9-]*\.html\|schwerpunkt/[a-z0-9-]*\.html' $S | sort -u | head -3   # Themenseite
```

Ist die Seite live, mit `curl -s https://mathe.begreifbar.ch/$S | md5sum` gegen `md5sum $S`
vergleichen und im Bericht sagen, welcher Stand geprüft wurde.

## 2 · Drei Agenten parallel starten

In **einer** Nachricht drei `Agent`-Aufrufe (`subagent_type: general-purpose`), mit den
Aufträgen unten; `<…>` aus Schritt 1 einsetzen. Alle drei bekommen denselben Vorspann:

> Du prüfst NUR LESEND (keine Datei ändern, nichts committen, keine Build-Skripte laufen
> lassen) das Leitprogramm `<S>` im Repo /home/paps/tals-mathe (BM Schweiz, RLP-BM 2030,
> Zielgruppe 16–20 J.) auf fachliche und didaktische Richtigkeit. Lies zuerst CLAUDE.md
> (Konventionen) und `HOWTO-leitprogramme.md` §15 «Prüfliste» — prüfe gegen jeden Punkt dort
> **und darüber hinaus**. Gewollte Konventionen sind keine Befunde (Dezimalpunkt, Punkte
> `(x | y)`, leere Menge `\{\,\}`, kein ß, Notation des Leitprogramms). Rechne JEDE Zahl mit
> python3 nach. Massstab: die Themenseite `<Themenseite>`, der RLP (`/home/paps/Math-GL.pdf`
> bzw. `Math-SP.pdf`, mit pdftotext lesbar), das HOWTO. Bericht auf Deutsch: Befunde nach
> Schwere (fachlicher Fehler / Logik- oder Bild-Ton-Fehler / didaktische Schwäche /
> Kleinigkeit), je mit Fundstelle (Datei:Zeile bzw. Clip/Szene/Feld), Zitat, Nachweis
> (Rechnung), Vorschlag. Nur belegte Befunde; Vermutungen markieren. Am Ende kurz, was als
> korrekt geprüft wurde.

**Agent «Seite»** — zusätzlich:
> Prüfe die Seite: Vorwissenstest, Kapiteltexte, Festhalten, Aufgaben mit Lösungen,
> Selbsttests, Gesamttest-Abschnitt, Zeitangaben. Ist die Seite generiert, lies die Quelle
> `<scripts/lp/name/seite.py, seite.js>`. JS-Logik: Sind die `ok`-Bedingungen der
> Aufgabenleisten erfüllbar (Reglerraster, Toleranzen) und nicht schon im Startzustand
> erfüllt? Erzeugen die Zufallsübungen immer lösbare, schöne Aufgaben, und stimmen ihre
> Diagnosen — auch bei Sonderwerten (0, ±1)? Lass laufen und werte aus:
> `node .claude/tools/pruef-uebungen.mjs <S> 2000`, `node .claude/tools/pruef-formelsatz.mjs <S> 60`,
> `node .claude/tools/pruef-leiste.mjs <S>`;
> prüfe Diagnosen darüber hinaus selbst (node, viele Zufallsfälle). Didaktik: Reihenfolge
> erfahren → verallgemeinern, nichts abgefragt, was nicht eingeführt ist, Passung zu
> Lernzielen und RLP-Kompetenzen, Begriffe und Farben einheitlich, Widersprüche zur
> Themenseite, realistische Zeiten.

**Agent «Clips»** — zusätzlich:
> Prüfe die Clips `<Liste>` (Quelle `clips/<name>.json`; Format in HOWTO-clips.md). Stimmen
> Sprechertext, Bildformeln und gezeichnete Graphen (Stützpunkte von `bewegung`, Begleiter)
> überein? Passt das Gesprochene zum Zeitpunkt zum Bild — miss mit
> `python3 .claude/tools/sprechzeiten.py <clip>`. Steht beim Erscheinen einer Frage die
> Antwort schon im Bild? Sind die als richtig markierten Antworten richtig, die falschen
> eindeutig falsch, die Rückmeldungen zutreffend und ohne die Lösung zu verraten, Text =
> gesprochener Text? Lass `node .claude/tools/pruef-fragen.mjs <Kontrollclips>` laufen.
> Bilder an kritischen Stellen: `SP=<scratchpad>/lp-pruefung node .claude/tools/pruef-clip.mjs
> clips/<name>.html <sekunden…>` und die PNGs ansehen (Fragen, Merkbilder, Schlussbilder).

**Agent «PDFs»** — zusätzlich:
> Prüfe Gesamttest und Bewertungspaket `<downloads/leitprogramme/name/*.tex>` und die PDFs
> daneben (Seiten ansehen). Jede Aufgabe selbst lösen, jede Zahl der Musterlösung und jeden
> Folgefehler-Fall nachrechnen, Grafiken gegen die Gleichungen. Punkte summieren
> (Kopf, Teile, Raster, Seite). Ist das Raster für eine KI eindeutig (Ergebnis- und
> Ablesepunkte, Restpunkte bei typischen Fehlern, gleichwertige Schreibweisen)? Wird jedes
> Kapitelziel geprüft, jedes verlangte Verfahren vorher geübt (Seite lesen)? Verspricht die
> Selbsteinschätzung mehr, als der Test prüft? Datenschutz-Hinweis, Layout, Umbrüche.

## 3 · Befunde nachprüfen und eintragen

Während die Agenten laufen, nichts an denselben Dateien tun. Wenn alle drei fertig sind:

1. Die HOCH-Befunde und alles, was überrascht, **selbst an der Quelle nachprüfen** (grep,
   enger Blick, python3). Was sich nicht bestätigt, fällt weg — im Bericht sagen.
2. In `TODO.md` einen Abschnitt «Prüfung `<name>` (Datum)» anlegen (Format wie die
   bestehenden Abschnitte: Legende, HOCH / MITTEL / NIEDRIG, je Befund Fundstelle, warum,
   Vorschlag; oben «Rechenfehler: …» und was als korrekt geprüft wurde).
3. Committen (nur `TODO.md`), nicht pushen.
4. Dem Auftraggeber berichten: die Befunde nach Schwere in Kürze, welche Neuvertonungen
   eine Behebung nach sich zieht, und dass Hörprobe und KI-Test (§15 Punkt 4) bei ihm liegen.

Neue Fehlerklassen, die nicht in der Prüfliste stehen, nach der Behebung dort ergänzen
(`HOWTO-leitprogramme.md` §15) — so lernt die Liste mit.
