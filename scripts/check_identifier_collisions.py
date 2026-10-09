#!/usr/bin/env python3
"""
Mathe begreifbar — Identifier-Kollisions-Check

Findet Top-Level-Symbole in Inline-Skripten der Themenseiten, die mit
Symbolen aus mathlib.js oder nav.js kollidieren.

Hard-Errors (const/let/class) blockieren die Seite komplett — der
Browser bricht das gesamte Inline-Skript beim Parsen ab.

Soft-Errors (function/var) überleben (zweite Definition gewinnt), sind
aber unsauber.

Aufruf vom Repo-Root:
    python3 scripts/check_identifier_collisions.py

Konvention: siehe STYLEGUIDE.md §6.2.
"""

import re
import sys
from pathlib import Path

RESERVED = {
    # mathlib.js
    'fmt', 'fmtS', 'fmtMx', 'fmtAffine', 'parseL', 'toggleL',
    'initCanvas', 'drawGrid', 'drawLine', 'drawDot',
    'flTex', 'flHtml', 'flTeil', 'flOffen', 'texE',
    # nav.js
    'SITE', 'GROUPS', 'TOC_KURZ',
    'buildNav', 'buildToC', 'toggleDD', 'toggleMobileNav',
}


def find_top_level_decls(js):
    """Findet const/let/var/function/class-Deklarationen NUR auf Top-Level
    (Klammertiefe = 0, Strings/Kommentare ausgeschlossen)."""
    decls, depth, i = [], 0, 0
    in_s = in_d = in_b = in_lc = in_bc = False
    line_start = True
    while i < len(js):
        c = js[i]
        nxt = js[i+1] if i+1 < len(js) else ''
        if in_lc:
            if c == '\n':
                in_lc = False
                line_start = True
            i += 1
            continue
        if in_bc:
            if c == '*' and nxt == '/':
                in_bc = False
                i += 2
                continue
            i += 1
            continue
        if in_s:
            if c == '\\':
                i += 2
                continue
            if c == "'":
                in_s = False
            i += 1
            continue
        if in_d:
            if c == '\\':
                i += 2
                continue
            if c == '"':
                in_d = False
            i += 1
            continue
        if in_b:
            if c == '\\':
                i += 2
                continue
            if c == '`':
                in_b = False
            i += 1
            continue
        if c == '/' and nxt == '/':
            in_lc = True
            i += 2
            continue
        if c == '/' and nxt == '*':
            in_bc = True
            i += 2
            continue
        if c == "'":
            in_s = True
            i += 1
            continue
        if c == '"':
            in_d = True
            i += 1
            continue
        if c == '`':
            in_b = True
            i += 1
            continue
        if c in '{[(':
            depth += 1
        if c in '}])':
            depth -= 1
        if c == '\n':
            line_start = True
            i += 1
            continue
        if line_start and depth == 0:
            if c in ' \t':
                i += 1
                continue
            m = re.match(r'(const|let|var|function|class)\s+(\w+)', js[i:])
            if m:
                decls.append((m.group(2), m.group(1)))
            line_start = False
        i += 1
    return decls


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    hard = []  # const/let/class → SyntaxError, blockierend
    soft = []  # function/var → unsauber, läuft aber
    for f in sorted(root.rglob('*.html')):
        # Nur Themenseiten (mit nav.js + mathlib.js)
        html = f.read_text(encoding='utf-8')
        if '../nav.js' not in html and 'nav.js' not in html:
            continue
        for s in re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', html, re.DOTALL):
            for name, kind in find_top_level_decls(s):
                if name in RESERVED:
                    rel = f.relative_to(root)
                    entry = (str(rel), name, kind)
                    if kind in ('const', 'let', 'class'):
                        hard.append(entry)
                    else:
                        soft.append(entry)

    if hard:
        print("⛔ BLOCKIEREND (Seite bricht beim Parsen, alle Inline-JS-Funktionen undefiniert):")
        for f, n, k in hard:
            print(f"  {f}: {k} {n}")
        print()
    if soft:
        print("⚠  AUFRÄUMEN (unsauber, läuft technisch — überschreibt die mathlib/nav-Variante):")
        for f, n, k in soft:
            print(f"  {f}: {k} {n}")
        print()
    if not (hard or soft):
        print("✓ Keine Kollisionen")

    return 1 if hard else 0


if __name__ == '__main__':
    sys.exit(main())
