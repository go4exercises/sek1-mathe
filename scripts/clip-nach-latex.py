#!/usr/bin/env python3
"""
Übersetzt die Drehbücher von der eigenen Formelschreibweise nach LaTeX.

Einmalige Umstellung: ab jetzt setzt MathJax alle Clips (Drehbuchfeld
"latex"). Das Skript bleibt im Repo, weil es dokumentiert, was mit den
381 Formelzeilen geschehen ist — und weil es sich wiederholen lässt, wenn
irgendwo noch ein altes Drehbuch auftaucht.

    python3 scripts/clip-nach-latex.py            # Probelauf, zeigt alles
    python3 scripts/clip-nach-latex.py --schreiben

Der heikle Teil ist nicht die Formel, sondern die Prosa dazwischen. Die
eigene Schreibweise kursiviert nur *einzelne* Buchstaben, darum durfte
«es entstehen Faktoren» unmarkiert mitten in einer Zeile stehen. In LaTeX
wäre das ein Buchstabensalat aus zwölf Variablen. Jede Buchstabenfolge ab
zwei Zeichen muss darum entschieden werden: Mathematik oder Text.

Entschieden wird über eine Liste, nicht über eine Heuristik. Was nicht in
MATHWORT steht, ist Text — und benachbarte Textstücke werden zu *einem*
\\text{…} zusammengezogen, sonst zerfällt ein Satz in Wörter mit falschen
Abständen dazwischen.
"""

import argparse
import glob
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS = os.path.join(WURZEL, "clips")

# Buchstabenfolgen, die Mathematik sind. Alles andere ist Text.
MATHWORT = {
    # Funktionen
    "sin": r"\sin", "cos": r"\cos", "tan": r"\tan",
    # Operatoren mit aufrechtem Namen
    "ggT": r"\operatorname{ggT}", "kgV": r"\operatorname{kgV}",
    # Mengenzeichen
    "in": r"\in", "notin": r"\notin", "inf": r"\infty", "sqrt": r"\sqrt{}",
    # Bezeichner der Trigonometrie-Seiten
    "GK": r"\mathrm{GK}", "AK": r"\mathrm{AK}", "HY": r"\mathrm{HY}",
    # Einheiten und Währung
    "cm": r"\mathrm{cm}", "dm": r"\mathrm{dm}", "km": r"\mathrm{km}",
    "mm": r"\mathrm{mm}", "kg": r"\mathrm{kg}", "ha": r"\mathrm{ha}",
    "hl": r"\mathrm{hl}", "CHF": r"\mathrm{CHF}",
}
# Variablenprodukte: bleiben Mathematik, LaTeX kursiviert von selbst.
VARPROD = {"ax", "ay", "bx", "by", "ab", "ac", "pq", "xy"}

ZEICHEN = {
    "≠": r"\neq", "≤": r"\leq", "≥": r"\geq", "±": r"\pm",
    "·": r"\cdot", "−": "-", "⟶": r"\longrightarrow",
    "⟹": r"\Longrightarrow", "⟺": r"\Longleftrightarrow",
    "∈": r"\in", "∉": r"\notin", "∩": r"\cap", "∪": r"\cup",
    "∖": r"\setminus",
    "∞": r"\infty", "√": r"\sqrt{}", "ℝ": r"\mathbb{R}", "ℕ": r"\mathbb{N}",
    "ℤ": r"\mathbb{Z}", "ℚ": r"\mathbb{Q}", "ℓ": r"\ell",
    "%": r"\%", "‰": r"\text{‰}", "Ω": r"\Omega", "µ": r"\mu",
    "°": r"^\circ", "∅": r"\{\,\}",
}
# Zeichen, die in einen Textblock gehören — im Mathesatz sähen sie falsch aus.
TEXTZEICHEN = set("✓✗—…«»„“")


NEUTRAL = set(",;:!?.")


def _teilen(s):
    """Rohtext in Stücke zerlegen: ('math'|'text'|'neutral'|'lueck', Inhalt)."""
    aus, i = [], 0
    while i < len(s):
        c = s[i]
        if c == " ":
            j = i
            while j < len(s) and s[j] == " ":
                j += 1
            aus.append(("lueck", j - i))
            i = j
        # Zeichentabelle VOR isalpha: ℝ und ℕ sind für Python Buchstaben.
        elif c in ZEICHEN:
            aus.append(("math", ZEICHEN[c]))
            i += 1
        elif c in TEXTZEICHEN:
            aus.append(("text", c))
            i += 1
        elif c.isdigit():
            j = i
            while j < len(s) and (s[j].isdigit()
                                  or (s[j] in "." and j + 1 < len(s) and s[j+1].isdigit())):
                j += 1
            aus.append(("math", s[i:j]))
            i = j
        elif c.isalpha():
            j = i
            while j < len(s) and s[j].isalpha():
                j += 1
            w = s[i:j]
            if w in MATHWORT:
                aus.append(("math", MATHWORT[w]))
            elif w in VARPROD or len(w) == 1:
                aus.append(("math", w))
            else:
                aus.append(("text", w))
            i = j
        elif c in NEUTRAL:
            aus.append(("neutral", c))
            i += 1
        elif c in "{}":
            aus.append(("math", "\\" + c))
            i += 1
        elif c == "|":
            aus.append(("math", r"\mid"))
            i += 1
        else:
            aus.append(("math", c))
            i += 1
    return aus


def _satz(stuecke):
    """Zusammensetzen; benachbarte Textstücke werden zu *einem* \\text{…}.

    Sonst zerfiele «es entstehen Faktoren» in drei Blöcke, zwischen denen
    LaTeX Mathe-Abstände setzt — sichtbar zu weit und an der falschen Stelle.
    Satzzeichen und einfache Lücken sind neutral: sie schliessen sich dem
    Text an, wenn links und rechts Text steht."""
    def naechste_art(k):
        for art, _ in stuecke[k+1:]:
            if art in ("text", "math"):
                return art
        return None

    zus = []
    for k, (art, inh) in enumerate(stuecke):
        links_text = bool(zus) and zus[-1][0] == "text"
        if art in ("lueck", "neutral") and links_text and naechste_art(k) == "text":
            zus[-1] = ("text", zus[-1][1] + (" " * inh if art == "lueck" else inh))
            continue
        if art == "neutral" and links_text:
            zus[-1] = ("text", zus[-1][1] + inh)
            continue
        if art == "text" and links_text:
            zus[-1] = ("text", zus[-1][1] + inh)
            continue
        zus.append((art, inh))

    aus = []
    for k, (art, inh) in enumerate(zus):
        if art == "lueck":
            # Ein einzelnes Leerzeichen ignoriert LaTeX. Zwischen Formel und
            # Text braucht es aber eines, sonst klebt «x» an «gerade».
            links = zus[k-1] if k else (None, "")
            rechts = zus[k+1] if k + 1 < len(zus) else (None, "")
            nachbar_text = links[0] == "text" or rechts[0] == "text"
            # Zwischen Zahl und Einheit gehoert ein schmales Leerzeichen:
            # «1.2 m», nicht «1.2m». LaTeX schluckt das gewoehnliche.
            einheit = (rechts[0] == "math" and str(rechts[1]).startswith("\\mathrm")
                       and links[0] == "math"
                       and str(links[1])[-1:] in "0123456789}")
            aus.append(r"\quad " if inh >= 2
                       else (r"\, " if einheit
                             else (r"\; " if nachbar_text else " ")))
        elif art == "text":
            aus.append(r"\text{%s}" % inh.strip() if inh.strip() else "")
        else:
            aus.append(inh + (" " if re.match(r"^\\[a-zA-Z]+$", inh) else ""))
    return re.sub(r" +", " ", "".join(aus)).strip()


def wandeln(t, tiefe=0):
    """Eine Formelzeile der eigenen Schreibweise nach LaTeX."""
    if tiefe > 8:
        raise RecursionError("zu tief verschachtelt: " + t)

    # Ganz zuerst: der einzelne Backslash der Quelle ist das Differenz-
    # zeichen zweier Mengen. In LaTeX waere er ein Abstandsbefehl und das
    # Zeichen verschwaende spurlos. Muss vor jeder Rekursion geschehen —
    # danach stehen in der Zeile auch die Backslashes fertiger LaTeX-Teile,
    # und aus dem \% eines Prozentzeichens wuerde eine Mengendifferenz.
    t = re.sub(r"\\(?![a-zA-Z])", "∖", t)

    # 1. Farbgruppen {n:…}  ->  \fa{…} … \fd{…}
    def farbe(m):
        return "\\f%s{%s}" % ("abcd"[int(m.group(1)) - 1], wandeln(m.group(2), tiefe + 1))
    while True:
        neu = re.sub(r"\{([1-4]):([^{}]*)\}", farbe, t, count=1)
        if neu == t:
            break
        t = neu

    # 2. Brüche [a|b] — von innen nach aussen
    while True:
        m = re.search(r"\[([^\[\]|]*)\|([^\[\]|]*)\]", t)
        if not m:
            break
        t = t[:m.start()] + "\\dfrac{%s}{%s}" % (wandeln(m.group(1), tiefe + 1),
                                                 wandeln(m.group(2), tiefe + 1)) \
            + t[m.end():]

    # 3. Auszeichnungen
    t = re.sub(r"`([^`]*)`", lambda m: m.group(1), t)                 # kursiv: LaTeX tut das selbst
    t = re.sub(r"#([^#]*)#", lambda m: r"\mathrm{%s}" % m.group(1), t)
    t = re.sub(r'"([^"]*)"', lambda m: r"\overline{%s}" % m.group(1), t)

    # 4. Mehrzeichen-Operatoren vor der Zerlegung
    for a, b in [("<=>", "⟺"), ("!=", "≠"), ("<=", "≤"), (">=", "≥"),
                 ("=>", "⟹"), ("->", "⟶"), ("\\R", "ℝ"), ("+-", "±"),
                 ("*", "·")]:
        t = t.replace(a, b)

    # Ab hier werden fertige LaTeX-Stücke gegen die weitere Zerlegung
    # geschützt: sie stehen als Platzhalter aus der privaten Unicode-Zone
    # in der Zeile und werden ganz am Schluss wieder eingesetzt.
    schutz = []

    def merken_fertig(stueck):
        schutz.append(stueck)
        return chr(0xE200 + len(schutz) - 1)

    # 4b. Wurzel: «√(1+8)» meint \sqrt{1+8}. Der Radikand steht in der
    # eigenen Schreibweise neben dem Zeichen, in LaTeX gehört er hinein.
    def wurzel(text):
        aus, i = [], 0
        while i < len(text):
            if text[i] == "√" and text[i+1:i+2] == "(":
                tiefe_k, j = 0, i + 1
                while j < len(text):
                    if text[j] == "(":
                        tiefe_k += 1
                    elif text[j] == ")":
                        tiefe_k -= 1
                        if tiefe_k == 0:
                            break
                    j += 1
                aus.append("\\sqrt{%s}" % wandeln(text[i+2:j], tiefe + 1))
                i = j + 1
            else:
                aus.append(text[i]); i += 1
        return "".join(aus)
    t = t.replace("sqrt", "√")
    t = wurzel(t)

    # 4c. Hoch- und Tiefstellung mit geschweiften Klammern retten, bevor
    # unten jede Klammer zur Mengenklammer \{ wird.
    t = re.sub(r"([\^_])\{([^{}]*)\}",
               lambda m: merken_fertig("%s{%s}" % (m.group(1),
                                                   wandeln(m.group(2), tiefe + 1))), t)

    # 5. Die übrigen fertigen LaTeX-Teile (aus der Rekursion) schützen

    def merken(m):
        schutz.append(m.group(0))
        return chr(0xE200 + len(schutz) - 1)
    def schuetzen(text):
        # \befehl gefolgt von beliebig tief geschachtelten {…}-Gruppen.
        aus, i = [], 0
        while i < len(text):
            m = re.match(r"\\[a-zA-Z]+", text[i:])
            if not m:
                aus.append(text[i]); i += 1; continue
            j = i + m.end()
            while j < len(text) and text[j] == "{":
                tiefe_k, j = 0, j
                while j < len(text):
                    if text[j] == "{":
                        tiefe_k += 1
                    elif text[j] == "}":
                        tiefe_k -= 1
                        if tiefe_k == 0:
                            j += 1
                            break
                    j += 1
            schutz.append(text[i:j])
            aus.append(chr(0xE200 + len(schutz) - 1))
            i = j
        return "".join(aus)

    t = schuetzen(t)

    stuecke = _teilen(t)
    stuecke = [(a, schutz[ord(i) - 0xE200]) if a == "math" and len(i) == 1
               and 0xE200 <= ord(i) < 0xE200 + len(schutz) else (a, i)
               for a, i in stuecke]
    return _satz(stuecke).strip()


FORMELTYP = {"formel", "box", "karte"}


def drehbuch(pfad):
    """Alle Formeltexte eines Drehbuchs übersetzen. Gibt die Paare zurück."""
    d = json.load(open(pfad, encoding="utf-8"))
    paare = []
    for sz in d.get("szenen", []):
        for el in sz.get("elemente", []):
            t = el.get("text", "")
            if el.get("typ") in FORMELTYP:
                neu = wandeln(t)
            elif "@" in t:
                # Fliesstext mit eingebetteter Formel: nur das @…@ wandeln.
                neu = re.sub(r"@([^@]*)@", lambda m: "@%s@" % wandeln(m.group(1)), t)
            else:
                continue
            if neu != t:
                paare.append((t, neu))
                el["text"] = neu
    d["latex"] = True
    return d, paare


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("clip", nargs="?", help="einzelnes Drehbuch; ohne Angabe alle")
    ap.add_argument("--schreiben", action="store_true")
    a = ap.parse_args()

    if a.clip:
        quellen = [os.path.join(CLIPS, a.clip.removesuffix(".json") + ".json")]
    else:
        quellen = sorted(g for g in glob.glob(os.path.join(CLIPS, "*.json"))
                         if os.path.basename(g) not in ("clips.json", "vorlage.json"))

    gesamt = 0
    for q in quellen:
        roh = json.load(open(q, encoding="utf-8"))
        if roh.get("latex"):
            continue
        d, paare = drehbuch(q)
        gesamt += len(paare)
        print("── %s  (%d Zeilen)" % (os.path.basename(q), len(paare)))
        for alt, neu in paare:
            print("   %s\n   → %s" % (alt, neu))
        if a.schreiben:
            with open(q, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=1)
                f.write("\n")
    print("\n%d Zeilen%s." % (gesamt, " geschrieben" if a.schreiben else " — Probelauf"))
