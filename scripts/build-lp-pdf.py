#!/usr/bin/env python3
"""Übersetzt die LaTeX-Quellen der Leitprogramme (downloads/leitprogramme/**/*.tex) mit pdfLaTeX
und legt nur das PDF neben die Quelle — Hilfsdateien entstehen in einem temporären Ordner.

  python3 scripts/build-lp-pdf.py                 # alle
  python3 scripts/build-lp-pdf.py gesamttest      # nur Quellen, deren Pfad das Wort enthält

Gemeinsame Gestaltung: downloads/leitprogramme/lp-druck.sty. Braucht latexmk und pdfLaTeX
(LuaLaTeX scheitert hier an der Schriftverwaltung: luaotfload-tool fehlt).
"""
import glob, os, shutil, subprocess, sys, tempfile
WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIS = os.path.join(WURZEL, "downloads", "leitprogramme")
filter_ = sys.argv[1:]
fehler = 0
for tex in sorted(glob.glob(os.path.join(BASIS, "**", "*.tex"), recursive=True)):
    if filter_ and not any(f in tex for f in filter_):
        continue
    ordner, name = os.path.split(tex)
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
                            "-outdir=" + tmp, name], cwd=ordner, capture_output=True, text=True)
        pdf = os.path.join(tmp, name[:-4] + ".pdf")
        log = open(os.path.join(tmp, name[:-4] + ".log"), errors="replace").read() if os.path.exists(os.path.join(tmp, name[:-4] + ".log")) else ""
        warn = [z for z in log.splitlines() if ("Overfull" in z and "hbox" in z) or "Missing character" in z]
        if r.returncode or not os.path.exists(pdf):
            fehler += 1
            print("  FEHLER", os.path.relpath(tex, WURZEL)); print("\n".join(log.splitlines()[-25:]))
            continue
        shutil.copy(pdf, os.path.join(ordner, name[:-4] + ".pdf"))
        print("  ok    ", os.path.relpath(tex, WURZEL)[:-4] + ".pdf", ("  — " + str(len(warn)) + " Warnung(en): " + "; ".join(warn[:3])) if warn else "")
sys.exit(1 if fehler else 0)
