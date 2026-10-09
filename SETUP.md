# SETUP — TALS Mathe lokal mit Claude Code

Auf diesem Computer sind Git, Node, Python, Claude Code und die GitHub-Anmeldung (`gh`)
durch die Physik-Einrichtung **bereits vorhanden**. Für Mathe brauchst du darum nur noch:
Repo klonen, Kit einspielen, ersten Commit. Stand: Juni 2026.

## 1. Repo von GitHub klonen

Klon-URL holen: GitHub-Repo-Seite von tals-mathe → grüner Button „Code" → HTTPS kopieren.
Ins Linux-Home klonen (nicht unter `/mnt/c/…`):

```bash
cd ~
git clone https://github.com/<DEIN-USER>/<TALS-MATHE-REPO>.git tals-mathe
cd tals-mathe
```

Da `gh` schon angemeldet ist, läuft das ohne erneute Passwort-/Token-Abfrage.

## 2. Kit einspielen

Dieses Kit (`CLAUDE.md`, `SETUP.md`, `.gitignore`, `TODO-schwesterprojekt.md`,
`.claude/…`) ins **Wurzelverzeichnis** auspacken — neben `grundlagen/`, `schwerpunkt/`,
`mathlib.js`, `style.css`:

```bash
unzip /mnt/c/Users/<WINDOWS-USER>/Downloads/tals-mathe-claude-code-kit-*.zip -d ~/tals-mathe
ls -la ~/tals-mathe
```

Hat das Repo schon eine `.gitignore`, beim Überschreiben mit `n` die bestehende behalten
(dann den Inhalt zusammenführen).

## 3. Erster Commit

```bash
python3 .claude/skills/preflight/preflight.py grundlagen/*.html schwerpunkt/*.html
git add -A
git commit -m "Claude-Code-Kit: CLAUDE.md, preflight-Skill, settings.json"
```

(Noch kein `git push` — erst nach inhaltlichen Änderungen, wenn du zufrieden bist.)

**Einmalig für die Tiefen-Checks** (MathJax-Render + JS-Laufzeit im Pre-Flight):

```bash
npm install mathjax-full jsdom
```

Ohne diese Module laufen nur die schnellen Eigen-Checks; die Tiefen-Checks werden mit
einem `[WARN]` übersprungen (kein Blocker).

## 4. Laufender Workflow (identisch zu Physik)

Drei Tabs im Ubuntu-Terminal, alle in `~/tals-mathe`:

- **Tab 1 — Claude Code:** `claude` starten, Auftrag direkt in den Chat tippen. Editiert
  in-place; `acceptEdits` greift (keine Diff-Bestätigung).
- **Tab 2 — Git:** nach jedem Durchgang
  ```bash
  git add . && python3 .claude/skills/preflight/preflight.py grundlagen/*.html schwerpunkt/*.html && git commit -m "deine Beschreibung"
  ```
  am Schluss, wenn happy: `git push`.
- **Tab 3 — Vorschau:** `python3 -m http.server`, dann im Windows-Browser
  `http://localhost:8000/grundlagen/g2-1-grundlagen.html` (bzw. `schwerpunkt/…`),
  nach Änderungen F5.

## 5. Übertrag ins Schwesterprojekt

Claude Code editiert nur dieses Repo. Was auch nach TALS-Physik gehört, wird in
`TODO-schwesterprojekt.md` vermerkt und später in einer Physik-Session von Hand portiert.
(Dieselbe Datei kannst du auch im Physik-Repo anlegen, für die Gegenrichtung.)
