#!/usr/bin/env python3
"""
Clip-Generator für mathe.begreifbar.ch
======================================

Macht aus jedem Drehbuch in clips/ einen animierten Erklärclip als HTML.

    python3 scripts/build-clips.py                 # alle Clips bauen
    python3 scripts/build-clips.py bruchgleichungen
    python3 scripts/build-clips.py --eigenstaendig  # Schriften einbetten

Standardfall ist die Web-Fassung: sie verweist auf ../schriften.css und wiegt
rund 10 kB. Sie ist dafür gebaut, in einer Lektionsseite in einem <iframe> zu
stecken oder direkt geöffnet zu werden.

Mit --eigenstaendig entsteht stattdessen eine Datei, die alles enthält —
für Moodle, zum Verschicken, fürs Archiv.

Nebenbei entstehen clips/clips.json (Verzeichnis aller Clips für die
Bibliotheksseite) und je ein sprechertext-<name>.txt für die Vertonung.

Drehbuch-Aufbau: siehe clips/vorlage.json und todo.md.
"""

import argparse
import glob
import json
import math
import os
import re
import subprocess
import sys
from datetime import date

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS = os.path.join(WURZEL, "clips")

# ---------------------------------------------------------------- Standardwerte
STD = {
    "takt": 1.7,          # Abstand zwischen Einblendungen, wenn nichts angegeben
    "nachlauf": 2.6,      # Standzeit nach der letzten Einblendung
    "vorlauf": 0.4,       # Verzögerung am Szenenanfang
    "sprechtempo": 1.45,  # Wörter pro Sekunde — für die Szenenlänge ohne Tonspur
    "theme": "heft",
}

# "achsen": false laesst Achsen und Teilung weg. Ob das Karo bleibt, ist je Projekt
# verschieden: In Physik ist eine Ebene ohne Achsen eine Zeichnung, die spaeter
# deckungsgleich ueber einem graf mit demselben Fenster erscheint (die Antwort nach
# der Frage) — ein zweites Karo verdunkelte das erste. In Mathe stehen Figuren der
# Planimetrie im Karo. "raster" im Drehbuch geht in beiden Projekten vor.
KARO_OHNE_ACHSEN = True
# Textbreite begrenzen (Physik 07.10.2026): zentrierte Zeilen mit Rand (130 px je Seite),
# links gesetzte Texte ohne eigenes "breite" auf die Spaltenbreite des Layouts. Physik True.
# Mathe False: Die 514 Mathe-Clips sind auf die volle Bühnenbreite gesetzt; mit True brechen
# 62 Elemente in 56 Clips neu um (gemessen 07.10.2026). Je Projekt eine Einstellung, der
# Code bleibt gemeinsam.
TEXTBREITE_BEGRENZEN = False


# ---------------------------------------------------------------- Formelsatz
# Formelsatz. Seit dem 31.08.2026 setzt MathJax alle Clips: eine Formel
# lässt sich damit unverändert von einer Lektionsseite ins Drehbuch
# kopieren, statt in eine zweite Schreibweise übersetzt zu werden. Die
# eigene Schreibweise unten bleibt erreichbar über "latex": false — die
# 28 umgestellten Drehbücher brauchen sie nicht mehr.
LATEX = True

def tex(text):
    """Rohes LaTeX fuer MathJax verpacken — nur HTML-Zeichen entschaerfen."""
    t = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return "\\(" + t + "\\)"


def formel(text):
    """Kompakte Formelschreibweise in HTML.

        [a|b]   Bruch a über b
        x^2     Hochstellung
        -       echtes Minus
        *       Malpunkt
        !=      Ungleichheitszeichen,  <=  >=  ->  =>  in  notin  R  D
        _1      Tiefstellung
        "36"    Überstrich — die Periode einer Dezimalzahl

    Einzelne lateinische Buchstaben werden kursiv gesetzt (Variablen).
    """
    if LATEX:
        return tex(text)
    t = text

    def zeichen(s):
        # <=> muss vor <= stehen, sonst wird daraus ein «≤>».
        for a, b in [("<=>", "⟺"), ("!=", "≠"), ("<=", "≤"), (">=", "≥"),
                     ("=>", "⟹"), ("->", "⟶"), ("\\R", "ℝ"),
                     ("*", "·"), ("+-", "±")]:
            s = s.replace(a, b)
        # Was jetzt noch an < und > dasteht, ist gemeint — «2 < 3». Hier
        # maskieren, solange noch keine Tags im Text sind; sonst hält der
        # Browser ein «a <b» für den Anfang eines Elements und verschluckt es.
        s = s.replace("<", "&lt;").replace(">", "&gt;")
        # Wortzeichen nur als eigenständiges Wort ersetzen, sonst wird
        # aus «Scheinlösung» ein «Sche∈lösung».
        for a, b in [("notin", "∉"), ("in", "∈"), ("sqrt", "√"), ("inf", "∞")]:
            s = re.sub(r"(?<![A-Za-zÄÖÜäöü])" + a + r"(?![A-Za-zÄÖÜäöü])", b, s)
        # - sind die Platzhalter für Farb- und Kursivgruppen.
        # Sie müssen hier wie Zeichen zählen, sonst bleibt ein «-» davor
        # oder dahinter ein Bindestrich statt eines Minuszeichens.
        s = re.sub(r"(?<=[\w\)\]\s-])-(?=[\w\(\[\s-])", "−", s)
        s = re.sub(r"^-", "−", s)
        s = re.sub(r"(?<=[\s\(\{\[=,;])-(?=[\d-]|[a-zA-Z])", "−", s)
        s = re.sub(r"  +", lambda m: "\u00a0" * len(m.group()), s)
        return s

    def hoch_tief(s):
        # Was hochgestellt werden darf: {…} · ein Vorzeichen mit Ziffern ·
        # ein Platzhalter (dort steckt eine Farbgruppe) · ein einzelnes
        # Zeichen. Ohne die mittleren beiden blieb «10^-6» und «10^{3:4}»
        # als roher Text mit Dach stehen.
        stelle = r"(\{[^}]*\}|[-\u2212]?\d+|[\uE000-\uE1FF]|\w)"

        def setzen(tag):
            def f(m):
                inhalt = m.group(1).strip("{}").replace("-", "\u2212")
                return "<%s>%s</%s>" % (tag, inhalt, tag)
            return f

        s = re.sub(r"\^" + stelle, setzen("sup"), s)
        s = re.sub(r"_" + stelle, setzen("sub"), s)
        return s

    def variablen(s):
        # einzelne lateinische Buchstaben kursiv, ausserhalb von Tags
        teile = re.split(r"(<[^>]*>)", s)
        for i, p in enumerate(teile):
            if p.startswith("<"):
                continue
            teile[i] = re.sub(r"(?<![A-Za-zÄÖÜäöü])([a-z])(?![A-Za-zÄÖÜäöü])",
                              r"<i>\1</i>", p)
        return "".join(teile)

    def stueck(s):
        return variablen(hoch_tief(zeichen(s)))

    # `ax` — zusammengeschriebenes Variablenprodukt kursiv setzen. Die
    # Automatik unten erwischt nur einzelne Buchstaben, sonst würde aus
    # «kgV» ein «kgV» in Kursiv und aus «wahre Aussage» ein Buchstabensalat.
    kursiv = []

    def merken_kursiv(m):
        kursiv.append(m.group(1))
        return chr(0xE080 + len(kursiv) - 1)

    t = re.sub(r"`([^`]*)`", merken_kursiv, t)

    # #m# — aufrecht stehen lassen. Einheiten sind keine Variablen: «1 m»
    # und «20 a» gehören aufrecht, das a einer Seitenlänge kursiv.
    aufrecht = []

    def merken_aufrecht(m):
        aufrecht.append(m.group(1))
        return chr(0xE0C0 + len(aufrecht) - 1)

    t = re.sub(r"#([^#]*)#", merken_aufrecht, t)

    # "36" — Überstrich über der Periode: 0."36" ist 0.363636…  Bewusst
    # nicht ~…~: das Zeichen heisst im Fliesstext schon «gedämpft», und
    # zwei Bedeutungen für dasselbe Zeichen sind eine Falle.
    strich = []

    def merken_strich(m):
        strich.append(m.group(1))
        return chr(0xE140 + len(strich) - 1)

    t = re.sub(r'"([^"]*)"', merken_strich, t)

    # Didaktische Einfärbung {1:...} zuerst herausnehmen, damit die
    # Zeichenersetzung sie nicht zerlegt. Platzhalter aus der privaten
    # Unicode-Zone werden von keiner der folgenden Regeln angefasst.
    farbig = []

    def merken(m):
        farbig.append((m.group(1), m.group(2)))
        return chr(0xE000 + len(farbig) - 1)

    while True:
        neu_t = re.sub(r"\{([1-4]):([^{}]*)\}", merken, t, count=1)
        if neu_t == t:
            break
        t = neu_t

    # Brüche zuerst, sie enthalten eigene Teilausdrücke
    aus = []
    rest = t
    while True:
        m = re.search(r"\[([^\[\]|]*)\|([^\[\]|]*)\]", rest)
        if not m:
            aus.append(stueck(rest))
            break
        aus.append(stueck(rest[:m.start()]))
        aus.append('<span class="fr"><span>' + stueck(m.group(1))
                   + '</span><span>' + stueck(m.group(2)) + '</span></span>')
        rest = rest[m.end():]
    ergebnis = "".join(aus)
    for i, (nr, inhalt) in enumerate(farbig):
        ergebnis = ergebnis.replace(
            chr(0xE000 + i), '<span class="f%s">%s</span>' % (nr, formel(inhalt)))
    for i, inhalt in enumerate(kursiv):
        ergebnis = ergebnis.replace(chr(0xE080 + i), "<i>" + formel(inhalt) + "</i>")
    for i, inhalt in enumerate(strich):
        ergebnis = ergebnis.replace(
            chr(0xE140 + i), '<span class="ov">' + formel(inhalt) + "</span>")
    for i, inhalt in enumerate(aufrecht):
        # bewusst ohne variablen(): genau darum geht es hier
        ergebnis = ergebnis.replace(chr(0xE0C0 + i), hoch_tief(zeichen(inhalt)))
    return ergebnis


def entschaerfen(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text_html(s):
    """Fliesstext: Zeilenumbruch mit |, Formelteile in @...@ .

    Die Formelteile werden zuerst herausgenommen. Täte man es später, hätte
    die HTML-Maskierung aus «<=» längst ein «&lt;=» gemacht, und der
    Formelsatz erkennt das Zeichen nicht mehr. Nebenbei darf so auch ein
    senkrechter Strich in einer eingebetteten Formel stehen, ohne dass er
    zum Zeilenumbruch wird.
    """
    formeln = []

    def merken(m):
        formeln.append(m.group(1))
        return chr(0xE100 + len(formeln) - 1)

    s = re.sub(r"@([^@]*)@", merken, s)
    s = entschaerfen(s).replace("|", "<br>")
    s = re.sub(r"~([^~]*)~", r'<span class="dim">\1</span>', s)
    s = re.sub(r"\{([1-4]):([^{}]*)\}",
               lambda m: '<span class="f%s">%s</span>' % (m.group(1), m.group(2)), s)
    for i, f in enumerate(formeln):
        s = s.replace(chr(0xE100 + i), formel(f))
    return s


# ---------------------------------------------------------------- Boxplot
def boxplot_svg(el, theme):
    """Ein Boxplot aus den fuenf Kennzahlen.

    Die Konvention ist die der Themenseite 4.3: Box von Q1 bis Q3, Strich
    beim Median, Antennen bis zum kleinsten und groessten Wert. Keine
    Ausreisserregel — die Seite kennt keine, und ein Clip soll keine
    einfuehren, die dort nicht steht.
    """
    b = el.get("breite", 1180)
    h = el.get("hoehe", 300)
    fv = theme.get("farben", ["#1F6FB2", "#C2621C", "#2C7A58", "#8A4BA0"])
    tinte = theme.get("tinte", "#20303a")
    papier = theme.get("papier", "#f7f5ef")
    kf = fv[el.get("farbe", 1) - 1]
    fl = theme.get("flaechen", ["rgba(31,111,178,.12)"] * 4)[el.get("farbe", 1) - 1]

    lo, hi = el["min"], el["max"]
    x0 = el.get("von", lo - (hi - lo) * 0.12)
    x1 = el.get("bis", hi + (hi - lo) * 0.12)
    rl, rr = 70, b - 70
    def px(v):
        return rl + (rr - rl) * (v - x0) / (x1 - x0)

    achse_y = h - 62
    box_o, box_u = 44, achse_y - 58
    mitte = (box_o + box_u) / 2

    t = ['<svg width="%d" height="%d" viewBox="0 0 %d %d" '
         'xmlns="http://www.w3.org/2000/svg" font-family="Source Sans 3,sans-serif">'
         % (b, h, b, h)]
    # Achse mit Teilung
    t.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"/>'
             % (rl - 20, achse_y, rr + 20, achse_y, tinte))
    for v in el.get("teilung", []):
        t.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.5"/>'
                 % (px(v), achse_y - 9, px(v), achse_y + 9, tinte))
        t.append('<text x="%.1f" y="%.1f" font-size="26" fill="%s" text-anchor="middle" '
                 'opacity=".72">%s</text>' % (px(v), achse_y + 42, tinte, formel_zahl(v)))
    # Antennen
    for a_, e_ in ((lo, el["q1"]), (el["q3"], hi)):
        t.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="4"/>'
                 % (px(a_), mitte, px(e_), mitte, kf))
    for v in (lo, hi):
        t.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="5" '
                 'stroke-linecap="round"/>' % (px(v), box_o + 12, px(v), box_u - 12, kf))
    # Box und Median
    t.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" '
             'stroke-width="5" rx="4"/>'
             % (px(el["q1"]), box_o, px(el["q3"]) - px(el["q1"]), box_u - box_o, fl, kf))
    t.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="7"/>'
             % (px(el["med"]), box_o, px(el["med"]), box_u, tinte))
    # Beschriftung der fuenf Zahlen
    if el.get("marken", True):
        namen = [(lo, "min"), (el["q1"], "Q1"), (el["med"], "Median"),
                 (el["q3"], "Q3"), (hi, "max")]
        for v, nm in namen:
            t.append('<text x="%.1f" y="%.1f" font-size="25" font-weight="600" fill="%s" '
                     'text-anchor="middle">%s</text>' % (px(v), box_o - 14, kf, nm))
    t.append("</svg>")
    return "".join(t)


def formel_zahl(v):
    """Zahl fuer eine Achsenbeschriftung — Punkt als Trennzeichen, ohne .0."""
    return ("%g" % v)


# ---------------------------------------------------------------- Koordinatenbild
# Was in der Formel eines "kurven"-Eintrags stehen darf. Bewusst knapp:
# Ein Drehbuch beschreibt eine Kurve, es rechnet nicht.
_KURVE_NS = {"sin": math.sin, "cos": math.cos, "tan": math.tan,
             "asin": math.asin, "acos": math.acos, "atan": math.atan,
             "sqrt": math.sqrt, "exp": math.exp, "log": math.log,
             "abs": abs, "pi": math.pi, "e": math.e}


def kurve_wert(formel, x):
    """Wert einer Drehbuch-Formel an der Stelle x, oder None.

    None heisst: hier gibt es keinen Punkt. Der Streckenzug bricht dann ab
    und faengt danach neu an — genau das braucht die Tangenskurve an ihren
    Polstellen, ohne dass im Drehbuch etwas ueber Pole stehen muss.
    """
    try:
        return float(eval(formel, {"__builtins__": {}}, dict(_KURVE_NS, x=x)))
    except Exception:
        return None


def formel_js(formel):
    """Eine Drehbuch-Formel als JavaScript-Ausdruck, voll geklammert.

    Fuer Formelkurven mit "parameter" (seit 07.10.2026): Der Abspieler zeichnet sie selbst.
    Uebersetzt wird ueber den Python-Syntaxbaum, nicht mit Textersetzung — sonst waere
    -x**2 in JavaScript ein Syntaxfehler und x^2 etwas anderes als gemeint.
    """
    import ast
    ops = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/", ast.Pow: "**", ast.Mod: "%"}
    def js(n):
        if isinstance(n, ast.Expression):
            return js(n.body)
        if isinstance(n, ast.BinOp) and type(n.op) in ops:
            return "(%s%s%s)" % (js(n.left), ops[type(n.op)], js(n.right))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
            return "(%s%s)" % ("-" if isinstance(n.op, ast.USub) else "+", js(n.operand))
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return repr(n.value)
        if isinstance(n, ast.Name):
            return {"pi": "Math.PI", "e": "Math.E"}.get(n.id, n.id)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in _KURVE_NS:
            return "Math.%s(%s)" % (n.func.id, ",".join(js(a) for a in n.args))
        raise SystemExit("Formel %r: %s geht im Abspieler nicht" % (formel, type(n).__name__))
    return js(ast.parse(formel, mode="eval"))


def graf_svg(el, theme):
    """Kleines Koordinatensystem mit Geraden und Punkten, als SVG.

    Nur so viel, wie ein Clip braucht: Achsen mit Teilung, Geraden ueber
    Steigung und Achsenabschnitt (oder zwei Punkte) und markierte Punkte
    mit Beschriftung. Kein Diagrammwerkzeug — wer mehr will, zeichnet die
    Figur wie auf den Themenseiten in physiklib.js bzw. mathlib.js.

    Die Geraden werden am Fenster abgeschnitten, nicht an ihren Endpunkten:
    eine Gerade, die aus dem Bild laeuft, soll am Rand aufhoeren und nicht
    an einer willkuerlichen Stelle davor.
    """
    b = el.get("breite", 760)
    h = el.get("hoehe", 560)
    x0, x1 = el.get("xbereich", [-1, 6])
    y0, y1 = el.get("ybereich", [-1, 8])
    fv = theme.get("farben", ["#1F6FB2", "#C2621C", "#2C7A58", "#8A4BA0"])
    tinte, papier = theme["tinte"], theme["papier"]
    rand = 8

    def px(x):
        return rand + (x - x0) / (x1 - x0) * (b - 2 * rand)

    def py(y):
        return h - rand - (y - y0) / (y1 - y0) * (h - 2 * rand)

    # "ausweichen": true (seit 08.10.2026): Beschriftungen von Punkten — feste und mitfahrende — weichen
    # einander im Abspieler aus (AUSWEICHEN_JS). Ohne das Feld stehen sie, wo sie berechnet sind.
    ausw = bool(el.get("ausweichen"))
    teile = ['<svg width="%d" height="%d" viewBox="0 0 %d %d"%s>' % (b, h, b, h, ' data-ausweichen="1"' if ausw else "")]
    # Laeufer kommen zuletzt ins Bild, ueber feste Punkte (seit 07.10.2026). Was ihr Teil an
    # "ein"/"aus" traegt, nehmen sie mit (zeitlich() wickelt nur, was in "teile" steht).
    zuoberst = []
    def nach_oben(teil, lf, html):
        zuoberst.append(mit_zeit(teil, mit_zeit(lf, html)))
    # "lage" am Laeufer: "oben", "unten", "links", "rechts" oder zwei davon ("oben links") —
    # wo seine Beschriftung steht. Ohne Angabe sucht der Abspieler wie bisher selbst.
    def lage(lf):
        return ' data-lage="%s"' % entschaerfen(lf["lage"]) if lf.get("lage") else ""
    # "farbwechsel": [[t, farbe], …] an einer bewegten Kurve, Geraden oder Parabel (seit 08.10.2026):
    # ab t (Sekunden ab Szenenbeginn) traegt die Linie diese Farbe; vorher ihre eigene. bauen() rechnet
    # die Zeiten auf den Clip um, FARBWECHSEL_JS schaltet.
    def farbwechsel(it):
        if not it.get("farbwechsel"):
            return ""
        return ' data-farben-rel="%s"' % ";".join(
            "%g,%s" % (t_, tinte if n_ == 5 and len(fv) < 5 else fv[n_ - 1]) for t_, n_ in it["farbwechsel"])

    # "ein"/"aus" an einem einzelnen Teil (Punkt, Kurve, Gerade, Parabel, Figur, Strecke,
    # Flaeche, Text; seit 07.10.2026): Sekunden ab Szenenbeginn wie beim Element. Was der
    # Teil in seinem Durchgang zeichnet, kommt in eine Gruppe, die der Abspieler ein- und
    # ausblendet; bauen() rechnet die Zeiten auf den Clip um. Ohne die Felder bleibt alles
    # Byte fuer Byte wie vorher.
    def mit_zeit(it, html):
        """Ein Begleiter (laeufer, dreieck) mit eigenem "ein"/"aus" — wie zeitlich(), fuer ein Stueck."""
        if not isinstance(it, dict) or (it.get("ein") is None and it.get("aus") is None):
            return html
        a = "".join(' data-%s-rel="%g"' % (k, it[k]) for k in ("ein", "aus") if it.get(k) is not None)
        return '<g class="zt"%s>%s</g>' % (a, html)

    def zeitlich(teile_liste):
        for it in teile_liste:
            n = len(teile)
            yield it
            if isinstance(it, dict) and (it.get("ein") is not None or it.get("aus") is not None):
                a = "".join(' data-%s-rel="%g"' % (k, it[k]) for k in ("ein", "aus") if it.get(k) is not None)
                teile[n:] = ['<g class="zt"%s>' % a] + teile[n:] + ['</g>']

    # Wo die Achse geteilt wird. Ganze Zahlen sind der Normalfall; wo die
    # x-Achse ein Winkel ist, taugen sie nicht — eine Sinuskurve gehoert bei
    # pi/2 geteilt und nicht bei 1, 2, 3. Darum "xteilung"/"yteilung":
    # Paare [Stelle, Beschriftung], die die ganzen Zahlen ersetzen.
    def teilung(schluessel, a, e):
        eigen = el.get(schluessel)
        if eigen:
            return [(float(w), str(t)) for w, t in eigen]
        return [(float(k), str(k).replace("-", "\u2212"))
                for k in range(int(math.ceil(a)), int(math.floor(e)) + 1)]

    xt = teilung("xteilung", x0, x1)
    yt = teilung("yteilung", y0, y1)

    # Karo
    # Was "achsen": false mit dem Karo macht, ist je Projekt verschieden (KARO_OHNE_ACHSEN
    # oben); "raster" im Drehbuch entscheidet in beiden Projekten ausdruecklich.
    if el.get("raster", KARO_OHNE_ACHSEN if el.get("achsen", True) is False else True):
        for x, _ in xt:
            teile.append('<line x1="%.1f" y1="0" x2="%.1f" y2="%d" stroke="%s" '
                         'stroke-opacity=".13" stroke-width="1.5"/>' % (px(x), px(x), h, tinte))
        for y, _ in yt:
            teile.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                         'stroke-opacity=".13" stroke-width="1.5"/>' % (py(y), b, py(y), tinte))

    # Achsen mit Pfeil und Beschriftung ("achsen": false lässt sie weg — für Figuren der
    # Planimetrie, die im Karo stehen, aber kein Koordinatensystem brauchen; seit 06.10.2026)
    vor_achsen = len(teile)
    teile.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="3"/>'
                 % (py(0), b, py(0), tinte))
    teile.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="0" stroke="%s" stroke-width="3"/>'
                 % (px(0), h, px(0), tinte))
    # "pfeile": Pfeilspitzen in positiver Richtung; "xname"/"yname": Achsenbeschriftung,
    # bei Anwendungen mit Grösse und Einheit ("x [m]", "A [m²]"). Ohne Angabe bleibt das
    # Bild wie bisher — bestehende Clips bauen Byte für Byte gleich.
    xname, yname = el.get("xname", "x"), el.get("yname", "y")
    achsnamen = []      # benannte Achsen kommen zuletzt, mit Hof — sonst liegt die Kurve darüber
    if el.get("pfeile"):
        teile.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                     % (b, py(0), b - 18, py(0) - 9, b - 18, py(0) + 9, tinte))
        teile.append('<polygon points="%.1f,0 %.1f,18 %.1f,18" fill="%s"/>'
                     % (px(0), px(0) - 9, px(0) + 9, tinte))
    if xname == "x":
        teile.append('<text x="%.1f" y="%.1f" font-size="26" font-style="italic" fill="%s">x</text>'
                     % (b - 26, py(0) - 14, tinte))
    else:
        achsnamen.append('<text x="%.1f" y="%.1f" font-size="26" font-style="italic" fill="%s" '
                         'stroke="%s" stroke-width="10" paint-order="stroke" text-anchor="end">%s</text>'
                         % (b - 8, py(0) - 16, tinte, papier, entschaerfen(xname)))
    if yname == "y":
        teile.append('<text x="%.1f" y="26" font-size="26" font-style="italic" fill="%s">y</text>'
                     % (px(0) + 14, tinte))
    else:
        achsnamen.append('<text x="%.1f" y="26" font-size="26" font-style="italic" fill="%s" '
                         'stroke="%s" stroke-width="10" paint-order="stroke">%s</text>'
                         % (px(0) + 14, tinte, papier, entschaerfen(yname)))
    # "zahlen_neben_kreis": true oder ein Radius r (seit 08.10.2026, Einheitskreis): Die Zahlen bei
    # x = ±r und y = ±r stehen sonst genau auf der Kreislinie um den Ursprung. Sie ruecken nach
    # aussen — an der x-Achse neben den Kreis, an der y-Achse ueber bzw. unter ihn.
    rk = el.get("zahlen_neben_kreis")
    rk = (1.0 if rk is True else float(rk)) if rk else None
    def auf_kreis(w):
        return rk is not None and abs(abs(w) - rk) < 1e-9
    for x, mark in xt:
        if abs(x) < 1e-9:
            continue
        teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.5"/>'
                     % (px(x), py(0) - 7, px(x), py(0) + 7, tinte))
        if auf_kreis(x):
            teile.append('<text x="%.1f" y="%.1f" font-size="22" text-anchor="%s" fill="%s" '
                         'fill-opacity=".75">%s</text>'
                         % (px(x) + (10 if x > 0 else -10), py(0) + 32, "start" if x > 0 else "end",
                            tinte, entschaerfen(mark)))
            continue
        teile.append('<text x="%.1f" y="%.1f" font-size="22" text-anchor="middle" fill="%s" '
                     'fill-opacity=".75">%s</text>'
                     % (px(x), py(0) + 32, tinte, entschaerfen(mark)))
    for y, mark in yt:
        if abs(y) < 1e-9:
            continue
        teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.5"/>'
                     % (px(0) - 7, py(y), px(0) + 7, py(y), tinte))
        teile.append('<text x="%.1f" y="%.1f" font-size="22" text-anchor="end" fill="%s" '
                     'fill-opacity=".75">%s</text>'
                     % (px(0) - 13, py(y) + ((-12 if y > 0 else 30) if auf_kreis(y) else 8),
                        tinte, entschaerfen(mark)))

    if el.get("achsen", True) is False:
        del teile[vor_achsen:]
        achsnamen = []

    # Flaechen: gefuellte Vielecke in Datenkoordinaten, unter allen Linien
    # (Physik 06.10.2026). Gebraucht fuer den Weg als Flaeche unter der
    # v-t-Geraden; "beschriftung" steht in der Mitte oder bei "beschriftung_bei".
    for fl in zeitlich(el.get("flaechen", [])):
        farbe = fv[fl.get("farbe", 1) - 1]
        teile.append('<polygon points="%s" fill="%s" fill-opacity="%s" stroke="none"/>'
                     % (" ".join("%.1f,%.1f" % (px(x), py(y)) for x, y in fl["punkte"]),
                        farbe, fl.get("deckung", 0.22)))
        if fl.get("beschriftung"):
            bx_, by_ = fl.get("beschriftung_bei") or (
                sum(x for x, _ in fl["punkte"]) / len(fl["punkte"]),
                sum(y for _, y in fl["punkte"]) / len(fl["punkte"]))
            teile.append('<text x="%.1f" y="%.1f" font-size="29" font-weight="600" fill="%s" '
                         'text-anchor="middle" stroke="%s" stroke-width="8" paint-order="stroke">%s</text>'
                         % (px(bx_), py(by_) + 10, farbe, papier, entschaerfen(fl["beschriftung"])))

    # "figuren" (seit 06.10.2026, Leitprogramm Planimetrie): Strecken, Vielecke, Kreise,
    # Sektoren, Winkelbögen, Zeichen für den rechten Winkel und Texte in Fensterkoordinaten.
    # Das Fenster muss dafür in x und y gleich geteilt sein (breite/hoehe passend zu den
    # Bereichen), sonst wird ein Kreis zur Ellipse. Gezeichnet unter Geraden und Punkten.
    skala = (b - 2 * rand) / (x1 - x0)
    if el.get("figuren"):
        import hashlib
        cid = "fg" + hashlib.md5(repr(sorted(el.items(), key=lambda kv: kv[0])).encode()).hexdigest()[:8]
        teile.append('<clipPath id="%s"><rect x="0" y="0" width="%d" height="%d"/></clipPath><g clip-path="url(#%s)">'
                     % (cid, b, h, cid))
    # "drehung" (Grad, gegen den Uhrzeigersinn) um "um" [x, y] (seit 07.10.2026): dreht die Figur,
    # bevor sie gezeichnet wird. In einer "bewegung" wird der Winkel uebergeblendet, nicht die Ecken —
    # die Figur bleibt unterwegs gleich gross. Texte drehen ihre Lage mit, nicht die Schrift.
    def gedreht(fg):
        w = math.radians(fg.get("drehung") or 0)
        if not w:
            return fg
        mx, my = fg.get("um", [0, 0])
        def d(p):
            x, y = p[0] - mx, p[1] - my
            return [mx + x * math.cos(w) - y * math.sin(w), my + x * math.sin(w) + y * math.cos(w)]
        g = dict(fg)
        art, grad = g["art"], math.degrees(w)
        if art == "strecke":
            g["von"], g["bis"] = d(g["von"]), d(g["bis"])
        elif art == "vieleck":
            g["punkte"] = [d(p) for p in g["punkte"]]
        elif art == "kreis":
            g["m"] = d(g["m"])
        elif art in ("sektor", "bogen"):
            g["m"], g["von"], g["bis"] = d(g["m"]), g["von"] + grad, g["bis"] + grad
        elif art == "winkel":
            g["bei"], g["von"], g["bis"] = d(g["bei"]), g["von"] + grad, g["bis"] + grad
        elif art == "rechts":
            g["bei"], g["r1"], g["r2"] = d(g["bei"]), g["r1"] + grad, g["r2"] + grad
        elif art == "text":
            g["bei"] = d(g["bei"])
        return g

    def zeichne_figur(fg):
        fg = gedreht(fg)
        art, nr_f = fg["art"], fg.get("farbe", 1)
        f_ = tinte if nr_f == 5 else fv[(nr_f - 1) % len(fv)]
        strich = ' stroke-dasharray="14 10"' if fg.get("gestrichelt") else ''
        if fg.get("deckkraft") is not None:          # Deckkraft der Linie, z. B. ein dicker Kreis als Ring
            strich += ' stroke-opacity="%g"' % fg["deckkraft"]
        dicke = fg.get("dicke", 4)
        fuell = fg.get("fuellung", 0)
        if art == "strecke":
            (xa, ya), (xb, yb) = fg["von"], fg["bis"]
            teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%g" '
                         'stroke-linecap="round"%s/>' % (px(xa), py(ya), px(xb), py(yb), f_, dicke, strich))
        elif art == "vieleck":
            pts = " ".join("%.1f,%.1f" % (px(x), py(y)) for x, y in fg["punkte"])
            teile.append('<polygon points="%s" fill="%s" fill-opacity="%g" stroke="%s" stroke-width="%g" '
                         'stroke-linejoin="round"%s/>' % (pts, f_, fuell, f_, dicke, strich))
        elif art == "kreis":
            (mx, my), r = fg["m"], fg["r"]
            teile.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" fill-opacity="%g" stroke="%s" '
                         'stroke-width="%g"%s/>' % (px(mx), py(my), r * skala, f_, fuell, f_, dicke, strich))
        elif art in ("sektor", "bogen"):
            # Winkel in Grad, gegen den Uhrzeigersinn ab der positiven x-Richtung
            (mx, my), r, w0, w1 = fg["m"], fg["r"], fg["von"], fg["bis"]
            ax, ay = px(mx + r * math.cos(math.radians(w0))), py(my + r * math.sin(math.radians(w0)))
            bx, by = px(mx + r * math.cos(math.radians(w1))), py(my + r * math.sin(math.radians(w1)))
            gross = 1 if (w1 - w0) % 360 > 180 else 0
            bogen = 'A%.1f %.1f 0 %d 0 %.1f %.1f' % (r * skala, r * skala, gross, bx, by)
            if art == "sektor":
                d = 'M%.1f %.1f L%.1f %.1f %s Z' % (px(mx), py(my), ax, ay, bogen)
            else:
                d = 'M%.1f %.1f %s' % (ax, ay, bogen)
            teile.append('<path d="%s" fill="%s" fill-opacity="%g" stroke="%s" stroke-width="%g"%s/>'
                         % (d, f_ if art == "sektor" else "none", fuell, f_, dicke, strich))
        elif art == "winkel":
            # Winkelbogen mit festem Pixelradius an der Ecke "bei", von/bis in Grad
            (mx, my), w0, w1, rp = fg["bei"], fg["von"], fg["bis"], fg.get("r_px", 38)
            cx_, cy_ = px(mx), py(my)
            ax, ay = cx_ + rp * math.cos(math.radians(w0)), cy_ - rp * math.sin(math.radians(w0))
            bx, by = cx_ + rp * math.cos(math.radians(w1)), cy_ - rp * math.sin(math.radians(w1))
            gross = 1 if (w1 - w0) % 360 > 180 else 0
            teile.append('<path d="M%.1f %.1f L%.1f %.1f A%g %g 0 %d 0 %.1f %.1f Z" fill="%s" fill-opacity=".22" '
                         'stroke="%s" stroke-width="2.5"/>' % (cx_, cy_, ax, ay, rp, rp, gross, bx, by, f_, f_))
        elif art == "rechts":
            # Zeichen für den rechten Winkel: Ecke "bei", Richtungen "r1"/"r2" (Grad), Seitenlänge in px
            (mx, my), w0, w1, q = fg["bei"], fg["r1"], fg["r2"], fg.get("px", 22)
            cx_, cy_ = px(mx), py(my)
            u = (math.cos(math.radians(w0)) * q, -math.sin(math.radians(w0)) * q)
            v = (math.cos(math.radians(w1)) * q, -math.sin(math.radians(w1)) * q)
            teile.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f" fill="none" stroke="%s" stroke-width="2.5"/>'
                         % (cx_ + u[0], cy_ + u[1], cx_ + u[0] + v[0], cy_ + u[1] + v[1], cx_ + v[0], cy_ + v[1], f_))
            teile.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (cx_ + (u[0] + v[0]) / 2, cy_ + (u[1] + v[1]) / 2, f_))
        elif art == "text":
            (tx, ty) = fg["bei"]
            teile.append('<text x="%.1f" y="%.1f" font-size="%d" font-style="%s" fill="%s" text-anchor="%s" '
                         'stroke="%s" stroke-width="8" paint-order="stroke">%s</text>'
                         % (px(tx), py(ty), fg.get("groesse", 30), "italic" if fg.get("kursiv", True) else "normal",
                            f_, fg.get("anker", "middle"), papier, entschaerfen(fg["text"])))
        else:
            raise SystemExit("figuren: unbekannte Art %r" % art)

    # "bewegung" an einer Figur (seit 07.10.2026): [[t, {Felder}], …] mit t ab Szenenbeginn.
    # Jeder Stuetzpunkt ueberschreibt Felder der Figur ("punkte", "von", "bis", "m", "r", "bei", …);
    # dazwischen werden alle Zahlen weich uebergeblendet (wie bewZustand). Gezeichnet wird in
    # Python, 20 Bilder je Sekunde; der Abspieler zeigt das passende (g.fb). So bewegt sich jede
    # Figurart, ohne dass ihre Zeichnung in JavaScript ein zweites Mal steht.
    def mischen(a, b, q):
        if isinstance(a, dict) and isinstance(b, dict):
            # Feld fuer Feld; "farbe" ist eine Nummer und wird umgeschaltet, nicht gemischt
            return {k: (v if q < 0.5 else b.get(k, v)) if k == "farbe" else mischen(v, b.get(k, v), q)
                    for k, v in a.items()}
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a + (b - a) * q
        if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
            return [mischen(u, v, q) for u, v in zip(a, b)]
        return a if q < 0.5 else b
    def knapp_machen(bilder):
        """Gleiche Nachbarbilder (eine Pause, {} als Stuetzpunkt) zu einem zusammenfassen."""
        knapp = [bilder[0]]
        for bi in bilder[1:]:
            if json.dumps(bi[2], sort_keys=True) == json.dumps(knapp[-1][2], sort_keys=True):
                knapp[-1][1] = bi[1]
            else:
                knapp.append(bi)
        return knapp

    # "parameter" an einer Figur (seit 08.10.2026): [[t, {"w": 0}], [t, {"w": 120}], …] — Buchstaben, die
    # sich waehrend der Szene aendern, weich wie jede Bewegung. Lage- und Massfelder der Figur duerfen
    # dann Formeln in diesen Buchstaben sein: {"art": "kreis", "m": ["cosd(w)", "sind(w)"], "r": 0.04}
    # faehrt auf dem Einheitskreis, statt quer durch ihn. sind/cosd/tand rechnen in Grad wie alle Figuren.
    # Gerechnet in Python mit 20 Bildern je Sekunde, gezeigt wie eine bewegte Figur (g.fb).
    FIG_NS = dict(_KURVE_NS, sind=lambda w: math.sin(math.radians(w)),
                  cosd=lambda w: math.cos(math.radians(w)), tand=lambda w: math.tan(math.radians(w)))
    FIG_FELDER = ("punkte", "von", "bis", "m", "r", "bei", "r1", "r2", "drehung", "um",
                  "deckkraft", "fuellung", "dicke", "r_px", "px", "groesse")

    def mit_parametern(fg):
        par = fg["parameter"]
        namen = []
        for _, felder in par:
            namen += [k for k in felder if k not in namen]
        for k in namen:
            if k in FIG_NS or k == "x":
                raise SystemExit("figuren/parameter: %r ist schon vergeben" % k)
        basis = {k: v for k, v in fg.items() if k not in ("parameter", "ein", "aus")}

        def rechne(v, werte):
            if isinstance(v, str):
                try:
                    return float(eval(v, {"__builtins__": {}}, dict(FIG_NS, **werte)))
                except Exception as e:
                    raise SystemExit("figuren/parameter: Formel %r geht nicht (%s)" % (v, e))
            if isinstance(v, list):
                return [rechne(u, werte) for u in v]
            return v

        def auswerten(werte):
            return {k: (rechne(v, werte) if k in FIG_FELDER else v) for k, v in basis.items()}
        stand, zust = {}, []
        for t_, felder in par:
            stand.update(felder)
            if len(stand) < len(namen):
                raise SystemExit("figuren/parameter: der erste Stuetzpunkt braucht alle Buchstaben %s" % namen)
            zust.append((t_, dict(stand)))
        bilder = [[None, zust[0][0], auswerten(zust[0][1])]]
        for (ta, wa), (tb, wb) in zip(zust, zust[1:]):
            schritte = max(1, int(round((tb - ta) * 20)))
            for k in range(schritte):
                q = (k + 0.5) / schritte
                q = q * q * (3 - 2 * q)
                bilder.append([ta + (tb - ta) * k / schritte, ta + (tb - ta) * (k + 1) / schritte,
                               auswerten({n: wa[n] + (wb[n] - wa[n]) * q for n in namen})])
        bilder.append([zust[-1][0], None, auswerten(zust[-1][1])])
        return knapp_machen(bilder)

    def figur_bilder(i, tiefe=0):
        """Die Bilder der Figur i: (bewegt, [[von, bis, Felder], …]); eine stehende Figur hat eines."""
        figs = el.get("figuren", [])
        fg = figs[i]
        if fg.get("folgt") is not None:
            return gefolgt(fg, tiefe)
        if fg.get("parameter"):
            if fg.get("bewegung"):
                raise SystemExit("figuren: parameter und bewegung zugleich geht nicht")
            return True, mit_parametern(fg)
        bew = fg.get("bewegung")
        if not bew:
            return False, [[None, None, fg]]
        basis = {k: v for k, v in fg.items() if k not in ("bewegung", "ein", "aus")}
        zust = []
        for t_, felder in bew:
            z = dict(zust[-1][1] if zust else basis)
            z.update(felder)
            zust.append((t_, z))
        bilder = [[None, zust[0][0], zust[0][1]]]
        for (ta, za), (tb, zb) in zip(zust, zust[1:]):
            schritte = max(1, int(round((tb - ta) * 20)))
            for k in range(schritte):
                q = (k + 0.5) / schritte
                q = q * q * (3 - 2 * q)
                bilder.append([ta + (tb - ta) * k / schritte, ta + (tb - ta) * (k + 1) / schritte, mischen(za, zb, q)])
        bilder.append([zust[-1][0], None, zust[-1][1]])
        return True, knapp_machen(bilder)

    # "folgt": i (seit 08.10.2026) — die Figur, meist ein Text, haengt an Figur i dieser Liste und faehrt
    # mit ihr, Bild fuer Bild: an deren Mittelpunkt (kreis, sektor, bogen), Ecke "bei" (text, winkel,
    # rechts) oder Ecke "ecke" (strecke: 0 = von, 1 = bis; vieleck: Index; ohne Angabe die letzte).
    # Dazu "versatz": [dx, dy] in Fensterkoordinaten, oder "radial": d — um d von "mitte" (Standard
    # [0, 0]) weg nach aussen, ein Text dabei um seine Mitte gesetzt (der Name am Punkt P).
    def gefolgt(fg, tiefe):
        if tiefe > 8:
            raise SystemExit("figuren/folgt: Kreis im Folgen")
        figs = el.get("figuren", [])
        j = fg["folgt"]
        if not (isinstance(j, int) and 0 <= j < len(figs)) or figs[j] is fg:
            raise SystemExit("figuren/folgt: %r ist keine andere Figur dieser Liste" % (j,))
        bewegt, fuehrer = figur_bilder(j, tiefe + 1)
        basis = {k: v for k, v in fg.items()
                 if k not in ("folgt", "versatz", "radial", "mitte", "ecke", "ein", "aus", "bewegung", "parameter")}
        feld = "m" if fg["art"] in ("kreis", "sektor", "bogen") else "bei"

        def anker(z):
            z = gedreht(z)
            art = z["art"]
            if art in ("kreis", "sektor", "bogen"):
                return z["m"]
            if art == "strecke":
                return [z["von"], z["bis"]][fg.get("ecke", -1)]
            if art == "vieleck":
                return z["punkte"][fg.get("ecke", -1)]
            return z["bei"]
        bilder = []
        for von, bis, z in fuehrer:
            ax, ay = anker(z)
            if fg.get("radial") is not None:
                mx, my = fg.get("mitte", [0, 0])
                d = math.hypot(ax - mx, ay - my)
                if d > 1e-12:
                    ax, ay = ax + fg["radial"] * (ax - mx) / d, ay + fg["radial"] * (ay - my) / d
                if fg["art"] == "text":      # Grundlinie: die Mitte der Schrift auf den Punkt
                    ay -= 0.35 * fg.get("groesse", 30) * (y1 - y0) / (h - 2 * rand)
            else:
                dx, dy = fg.get("versatz", [0, 0])
                ax, ay = ax + dx, ay + dy
            bilder.append([von, bis, dict(basis, **{feld: [ax, ay]})])
        return bewegt, knapp_machen(bilder) if bewegt else bilder

    figs_ = el.get("figuren", [])
    for fi, fg in enumerate(zeitlich(figs_)):
        bewegt, knapp = figur_bilder(fi)
        if not bewegt:
            zeichne_figur(knapp[0][2])
            continue
        for von, bis, z in knapp:
            n = len(teile)
            zeichne_figur(z)
            a = (' data-fvon-rel="%g"' % von if von is not None else "") + (' data-fbis-rel="%g"' % bis if bis is not None else "")
            teile[n:] = ['<g class="fb"%s>' % a] + teile[n:] + ["</g>"]
    if el.get("figuren"):
        teile.append('</g>')

    # Geraden y = m x + q, am Fenster abgeschnitten
    for nr, g in enumerate(zeitlich(el.get("geraden", []))):
        # "bewegung": [[t, m, q], ...] — eine Gerade, die sich waehrend der Szene
        # bewegt (t ab Szenenbeginn, seit 03.10.2026). Wie bei den Parabeln wird
        # sie erst im Abspieler gezeichnet, aus der Zeit allein; siehe BEWEGUNG_JS.
        if g.get("bewegung"):
            farbe = fv[g.get("farbe", 1) - 1]
            gid = "bewg%d" % nr
            teile.append('<path data-bewg="%s" data-paar="%s" data-fenster="%g,%g,%g,%g,%d,%d,%d" '
                         'fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" %s%s/>'
                         % (entschaerfen(json.dumps(g["bewegung"])), gid, x0, x1, y0, y1, b, h, rand,
                            farbe, g.get("dicke", 5),
                            'stroke-dasharray="14 10"' if g.get("gestrichelt") else "",
                            # "ab": die Gerade beginnt erst bei diesem x (Physik 03.10.2026:
                            # eine Q-t-Gerade hat keinen Teil bei negativer Zeit)
                            (' data-ab="%g"' % g["ab"] if g.get("ab") is not None else "") + farbwechsel(g)))

            # Begleiter der bewegten Geraden, alle aus derselben Zeit gerechnet:
            # yachse ((0 | q)), nullstelle ((x_0 | 0)), marken (Punkt an festem x
            # mit Live-Wert), laeufer (Punkt, der auf der Geraden faehrt) und
            # dreieck (Steigungsdreieck ab Stelle x mit Breite dx, mit Delta-Zahlen).
            def g_punkt(klasse, farbe_, attr="", text=True):
                f_ = fv[farbe_ - 1]
                t_ = '<g class="%s" data-zu="%s"%s>' % (klasse, gid, attr)
                t_ += ('<g class="bew-pt"><circle r="11" fill="%s" stroke="%s" stroke-width="3.5"/>'
                       '<circle r="5" fill="%s"/></g>' % (papier, f_, f_))
                if text:
                    t_ += '<text font-size="29" font-weight="600" fill="%s" stroke="%s" stroke-width="5" paint-order="stroke" stroke-linejoin="round"></text>' % (f_, papier)
                return t_ + '</g>'
            if g.get("yachse"):
                teile.append(g_punkt("bew-gy", g["yachse"].get("farbe", 2),
                                     text=g["yachse"].get("beschriftung", True) is not False))
            if g.get("nullstelle"):
                teile.append(g_punkt("bew-gn", g["nullstelle"].get("farbe", 3),
                                     text=g["nullstelle"].get("beschriftung", True) is not False))
            for mk in g.get("marken", []):
                teile.append(g_punkt("bew-gm", mk.get("farbe", 5),
                                     ' data-x="%g" data-text="%s"%s' % (mk["x"], entschaerfen(mk.get("text", "")), lage(mk))))
            # "schnitte" (seit 07.10.2026): {"kurve": i, "farbe": 2, "beschriftung": true} — die
            # Schnittpunkte mit der festen Formelkurve el["kurven"][i], mitlaufend. Der Abspieler
            # bekommt die Kurve als Wertetabelle und sucht Vorzeichenwechsel und Beruehrstellen
            # (bis zu "anzahl" Punkte, Standard 6).
            sch = g.get("schnitte")
            if sch:
                kv_ = el["kurven"][sch["kurve"]]
                if "formel" not in kv_:
                    raise SystemExit("schnitte: kurve %d hat keine formel" % sch["kurve"])
                n_ = sch.get("n", 800)
                a_, e_ = kv_.get("von", x0), kv_.get("bis", x1)
                tab = [kurve_wert(kv_["formel"], a_ + (e_ - a_) * i / n_) for i in range(n_ + 1)]
                tab = [None if y is None else round(y, 5) for y in tab]
                teile.append('<g class="bew-gs-tab" data-zu="%s" data-tab="%s" data-ab="%g" data-bis="%g"></g>'
                             % (gid, json.dumps(tab).replace(" ", ""), a_, e_))
                for i_ in range(sch.get("anzahl", 6)):
                    teile.append(g_punkt("bew-gs", sch.get("farbe", 2), ' data-i="%d"' % i_,
                                         text=bool(sch.get("beschriftung"))))
            lf = g.get("laeufer")
            if lf:
                nach_oben(g, lf, g_punkt("bew-gl", lf.get("farbe", 5),
                                     ' data-bahn="%s" data-text="%s"%s'
                                     % (entschaerfen(json.dumps(lf["bahn"])), entschaerfen(lf.get("text", "")), lage(lf))))
            dr = g.get("dreieck")
            if dr:
                f_ = fv[dr.get("farbe", 5) - 1]
                # Feste Stelle und Breite — oder "bahn": [[t, x, dx], ...], dann wandert
                # und waechst das Dreieck waehrend der Szene mit.
                if dr.get("bahn"):
                    teile.append(mit_zeit(dr, '<g class="bew-gd" data-zu="%s" data-bahn="%s">'
                                 '<path class="bew-gd-w" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="9 7"/>'
                                 '<path class="bew-gd-s" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="9 7"/>'
                                 '<text class="bew-gd-tx" font-size="27" font-weight="600" fill="%s" text-anchor="middle"></text>'
                                 '<text class="bew-gd-ty" font-size="27" font-weight="600" fill="%s"></text>'
                                 '</g>' % (gid, entschaerfen(json.dumps(dr["bahn"])), f_, f_, f_, f_)))
                    continue
                teile.append(mit_zeit(dr, '<g class="bew-gd" data-zu="%s" data-x="%g" data-dx="%g">'
                             '<path class="bew-gd-w" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="9 7"/>'
                             '<path class="bew-gd-s" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="9 7"/>'
                             '<text class="bew-gd-tx" font-size="27" font-weight="600" fill="%s" text-anchor="middle"></text>'
                             '<text class="bew-gd-ty" font-size="27" font-weight="600" fill="%s"></text>'
                             '</g>' % (gid, dr["x"], dr["dx"], f_, f_, f_, f_)))
            continue
        m, q = g["m"], g["q"]
        punkte = []
        for x in (x0, x1):
            y = m * x + q
            if y0 - 1e-9 <= y <= y1 + 1e-9:
                punkte.append((x, y))
        if abs(m) > 1e-9:
            for y in (y0, y1):
                x = (y - q) / m
                if x0 - 1e-9 <= x <= x1 + 1e-9:
                    punkte.append((x, y))
        if len(punkte) < 2:
            continue
        punkte.sort()
        (ax, ay), (bx, by) = punkte[0], punkte[-1]
        farbe = fv[g.get("farbe", 1) - 1]
        teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                     'stroke-width="%s" stroke-linecap="round" %s/>'
                     % (px(ax), py(ay), px(bx), py(by), farbe, g.get("dicke", 5),
                        'stroke-dasharray="14 10"' if g.get("gestrichelt") else ""))
        if g.get("beschriftung"):
            bx_, by_ = g.get("beschriftung_bei", [bx, by])
            teile.append('<text x="%.1f" y="%.1f" font-size="27" fill="%s" '
                         'text-anchor="%s">%s</text>'
                         % (px(bx_), py(by_), farbe, g.get("anker", "start"),
                            entschaerfen(g["beschriftung"])))

    # Parabeln y = a x^2 + b x + c, als Streckenzug im Fenster
    for nr, pa in enumerate(zeitlich(el.get("parabeln", []))):
        # "bewegung": [[t, a, u, v], ...] — eine Parabel in Scheitelform, die
        # sich waehrend der Szene bewegt (t ab Szenenbeginn). Gezeichnet wird
        # sie erst im Abspieler, aus der Zeit allein: Pause, Spulen und die
        # Pruefbilder bleiben so richtig. Siehe BEWEGUNG_JS.
        if pa.get("bewegung"):
            farbe = fv[pa.get("farbe", 1) - 1]
            bid = "bew%d" % nr
            # "ab"/"bis" (Physik 06.10.2026): die Parabel nur zwischen diesen x zeichnen
            # (Wurf: keine negative Zeit, nichts unter dem Boden); ohne die Felder wie bisher.
            # "normalform": true (seit 07.10.2026) liest die Stuetzpunkte als [t, a, b, c] fuer
            # y = a x^2 + b x + c. Nur so kann a stetig durch 0 laufen (Parabel → Gerade →
            # Parabel); Scheitelform und Linearfaktoren laufen dort davon.
            teile.append('<path data-bew="%s" data-paar="%s" data-fenster="%g,%g,%g,%g,%d,%d,%d"%s%s%s '
                         'fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" '
                         'stroke-linejoin="round" %s/>'
                         % (entschaerfen(json.dumps(pa["bewegung"])), bid, x0, x1, y0, y1, b, h, rand,
                            ' data-ab="%g"' % pa["ab"] if pa.get("ab") is not None else "",
                            ' data-bis="%g"' % pa["bis"] if pa.get("bis") is not None else "",
                            (' data-normal="1"' if pa.get("normalform") else "") + farbwechsel(pa),
                            farbe, pa.get("dicke", 5),
                            'stroke-dasharray="14 10"' if pa.get("gestrichelt") else ""))
            # Begleiter der bewegten Parabel, alle aus derselben Zeit gerechnet:
            # scheitel (mit "S(u | v)"), nullstellen, yachse, marken (Punkt an
            # festem x mit Live-Wert) und laeufer (Punkt, der auf der Kurve
            # faehrt; "spiegel" zeigt den Partner bei 2u - x).
            def punkt_g(klasse, farbe, attr="", geist=False, text=True):
                f_ = fv[farbe - 1]
                g = '<g class="%s" data-zu="%s"%s>' % (klasse, bid, attr)
                if geist:
                    g += ('<g class="bew-geist" opacity=".35"><circle r="11" fill="%s" stroke="%s" '
                          'stroke-width="3.5"/><circle r="5" fill="%s"/></g>' % (papier, f_, f_))
                g += ('<g class="bew-pt"><circle r="11" fill="%s" stroke="%s" stroke-width="3.5"/>'
                      '<circle r="5" fill="%s"/></g>' % (papier, f_, f_))
                if text:
                    g += '<text font-size="29" font-weight="600" fill="%s" stroke="%s" stroke-width="5" paint-order="stroke" stroke-linejoin="round"></text>' % (f_, papier)
                return g + '</g>'
            # "achse" (seit 07.10.2026): die Symmetrieachse x = u, gestrichelt, wandert mit
            if pa.get("achse") not in (None, False):          # true oder {"farbe": n}
                fa_ = pa["achse"].get("farbe", 5) if isinstance(pa["achse"], dict) else 5
                teile.append('<g class="bew-a" data-zu="%s"><path fill="none" stroke="%s" stroke-width="3" '
                             'stroke-dasharray="10 8"/></g>' % (bid, tinte if fa_ == 5 else fv[fa_ - 1]))
            if pa.get("scheitel"):
                teile.append(punkt_g("bew-s", pa["scheitel"].get("farbe", 3)))
            if pa.get("nullstellen"):
                f_ = pa["nullstellen"].get("farbe", 2)
                mit = bool(pa["nullstellen"].get("beschriftung"))   # «(x | 0)» an den Nullstellen
                teile.append(punkt_g("bew-n bew-n1", f_, text=mit))
                teile.append(punkt_g("bew-n bew-n2", f_, text=mit))
            if pa.get("yachse"):
                teile.append(punkt_g("bew-y", pa["yachse"].get("farbe", 1)))
            for m in pa.get("marken", []):
                teile.append(punkt_g("bew-m", m.get("farbe", 4),
                                     ' data-x="%g" data-text="%s"%s' % (m["x"], entschaerfen(m.get("text", "")), lage(m))))
            lf = pa.get("laeufer")
            if lf:
                nach_oben(pa, lf, punkt_g("bew-l", lf.get("farbe", 2),
                                     ' data-bahn="%s" data-text="%s"%s' % (entschaerfen(json.dumps(lf["bahn"])),
                                                                           entschaerfen(lf.get("text", "")), lage(lf)),
                                     geist=bool(lf.get("spiegel"))))
            continue
        a_, b_, c_ = pa["a"], pa.get("b", 0), pa.get("c", 0)
        stuecke, lauf = [], []
        n = 240
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            y = a_ * x * x + b_ * x + c_
            if y0 <= y <= y1:
                lauf.append("%.1f,%.1f" % (px(x), py(y)))
            elif lauf:
                stuecke.append(lauf); lauf = []
        if lauf:
            stuecke.append(lauf)
        farbe = fv[pa.get("farbe", 1) - 1]
        for st in stuecke:
            if len(st) > 1:
                teile.append('<polyline points="%s" fill="none" stroke="%s" '
                             'stroke-width="%s" stroke-linecap="round" '
                             'stroke-linejoin="round" %s/>'
                             % (" ".join(st), farbe, pa.get("dicke", 5),
                                'stroke-dasharray="14 10"' if pa.get("gestrichelt") else ""))
        if pa.get("beschriftung"):
            bx_, by_ = pa["beschriftung_bei"]
            teile.append('<text x="%.1f" y="%.1f" font-size="27" fill="%s" '
                         'text-anchor="%s">%s</text>'
                         % (px(bx_), py(by_), farbe, pa.get("anker", "start"),
                            entschaerfen(pa["beschriftung"])))

    # Kurven y = f(x), als Streckenzug im Fenster. Wie die Parabeln, nur
    # mit freier Formel — und mit dem Zusatz, dass ein Stueck auch dann
    # abbricht, wenn f an einer Stelle gar nicht definiert ist. Genau daran
    # entstehen die Luecken der Tangenskurve an ihren Polstellen.
    for nr, kv in enumerate(zeitlich(el.get("kurven", []))):
        # "bewegung": [[t, a, p, u, v], ...] fuer y = a*(x-u)^p + v — Potenz- und
        # Wurzelkurven, die sich waehrend der Szene aendern (seit 03.10.2026).
        # "stufen": true rundet p beim Ueberblenden auf ganze Zahlen; zwischen
        # x^2 und x^3 gibt es auf ganz R nichts, und ein gebrochener Exponent
        # loeschte den linken Ast mitten in der Bewegung.
        if kv.get("bewegung"):
            # "grad": true (seit 08.10.2026, nur "trig"): die x-Achse in Grad — u, von/bis, grenzen, Marken,
            # Laeufer und beim Kreis mx und die Bahn stehen im Drehbuch in Grad. Der Bauer gibt sie dem
            # Abspieler im Bogenmass; GRAD_JS rechnet nur die Abbildung aufs Fenster um.
            if kv.get("grad"):
                if not kv.get("trig"):
                    raise SystemExit("kurven: \"grad\" gibt es nur mit \"trig\"")
                K_ = math.pi / 180
                kv = dict(kv, bewegung=[[st[0], st[1], st[2], st[3] * K_, st[4]] for st in kv["bewegung"]],
                          von=kv.get("von", x0) * K_, bis=kv.get("bis", x1) * K_)
                if kv.get("grenzen"):
                    kv["grenzen"] = [[g_[0], g_[1] * K_, g_[2] * K_] for g_ in kv["grenzen"]]
                if kv.get("kreis"):
                    kv["kreis"] = dict(kv["kreis"], mx=kv["kreis"].get("mx", -1.6) * K_,
                                       bahn=[[b_[0], b_[1] * K_] for b_ in kv["kreis"]["bahn"]])
                if kv.get("marken"):
                    kv["marken"] = [dict(m_, x=m_["x"] * K_) for m_ in kv["marken"]]
                if kv.get("laeufer"):
                    kv["laeufer"] = dict(kv["laeufer"], bahn=[[b_[0], b_[1] * K_] for b_ in kv["laeufer"]["bahn"]])
            farbe = fv[kv.get("farbe", 1) - 1]
            kid = "bewk%d" % nr
            # "von"/"bis" schraenken die Kurve auf ein Stueck ein — gebraucht fuer die
            # Umkehrbarkeit: y = x^2 ist erst auf x >= 0 umkehrbar.
            # "exponential": true / "logarithmus": true (seit 04.10.2026) lesen die Stuetzpunkte
            # als [t, c, a, v] fuer y = c*a^x + v bzw. y = c*log_a(x) + v; Begleiter wie unten
            # (asymptoten, startpunkt = (0 | c + v) bzw. (1 | v), marken, spiegel).
            # "betrag": true (seit 05.10.2026) liest die Stuetzpunkte als [t, a, u, v] fuer
            # y = a*|x - u| + v; startpunkt = Knickpunkt (u | v), asymptoten = Symmetrieachse x = u.
            # "trig": "sin" / "tan" (seit 05.10.2026) liest die Stuetzpunkte als [t, a, b, u, v]
            # fuer y = a*sin(b(x-u)) + v bzw. a*tan(b(x-u)) + v. "asymptoten" zeichnet bei sin die
            # Mittellinie y = v, bei tan die Polgeraden; "kreis" den Einheitskreis mit Laeufer
            # (siehe unten). "art": "cos" zeigt statt der Höhe die waagrechte Koordinate von P.
            # "polynom": true (seit 04.10.2026) liest die Stuetzpunkte als [t, a, x1, x2, …]
            # fuer y = a*(x-x1)*(x-x2)*… — die Linearfaktordarstellung. Legt man zwei
            # Nullstellen aufeinander, entsteht die doppelte Nullstelle von selbst.
            teile.append('<path data-bewk="%s" data-paar="%s" data-fenster="%g,%g,%g,%g,%d,%d,%d" '
                         'data-stufen="%d" data-poly="%d" data-el="%s" data-von="%g" data-bis="%g"%s%s fill="none" stroke="%s" '
                         'stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" %s/>'
                         % (entschaerfen(json.dumps(kv["bewegung"])), kid, x0, x1, y0, y1, b, h, rand,
                            1 if kv.get("stufen") else 0, 1 if kv.get("polynom") else 0,
                            "e" if kv.get("exponential") else "l" if kv.get("logarithmus") else
                            ("v" if kv.get("betrag") else {"sin": "s", "tan": "t"}.get(kv.get("trig"), "")),
                            kv.get("von", x0), kv.get("bis", x1),
                            # "grenzen": [[t, von, bis], …] — der Bereich wandert (seit 07.10.2026)
                            (' data-grenzen="%s"' % entschaerfen(json.dumps(kv["grenzen"])) if kv.get("grenzen") else ""),
                            # "gleichmaessig": true (seit 08.10.2026, aus Physik) — Stuetzpunkte, "grenzen" und die
                            # Bahn ihrer Laeufer und Marken linear statt weich: eine Welle mit konstanter Geschwindigkeit.
                            (' data-gleich="1"' if kv.get("gleichmaessig") else "")
                            + (' data-grad="1"' if kv.get("grad") else "") + farbwechsel(kv),
                            farbe, kv.get("dicke", 5),
                            'stroke-dasharray="14 10"' if kv.get("gestrichelt") else ""))
            # Begleiter: startpunkt (u | v), asymptoten (x = u und y = v),
            # marken (Punkt an festem x mit Live-Wert) und spiegel (dieselbe
            # Kurve an y = x gespiegelt — die Umkehrfunktion).
            sp = kv.get("spiegel")
            if sp:
                teile.append('<path data-spiegel="%s" fill="none" stroke="%s" stroke-width="%s" '
                             'stroke-linecap="round" stroke-linejoin="round" %s/>'
                             % (kid, fv[sp.get("farbe", 3) - 1], sp.get("dicke", 5),
                                'stroke-dasharray="14 10"' if sp.get("gestrichelt") else ""))
            if kv.get("asymptoten"):
                f_ = fv[kv["asymptoten"].get("farbe", 5) - 1]
                # "strich" (seit 08.10.2026): eigene Strichart, als SVG-Strichmuster ("4 9") oder "voll";
                # "dicke" in px. Ohne die Felder wie bisher: 3 px, "10 8".
                st_ = kv["asymptoten"].get("strich", "10 8")
                st_ = "" if st_ == "voll" else ' stroke-dasharray="%s"' % entschaerfen(str(st_))
                dk_ = kv["asymptoten"].get("dicke", 3)
                teile.append('<g class="bew-ka" data-zu="%s">'
                             '<path class="bew-ka-s" fill="none" stroke="%s" stroke-width="%s"%s/>'
                             '<path class="bew-ka-w" fill="none" stroke="%s" stroke-width="%s"%s/>'
                             '</g>' % (kid, f_, dk_, st_, f_, dk_, st_))

            def k_punkt(klasse, farbe_, attr="", text=True):
                f_ = fv[farbe_ - 1]
                t_ = '<g class="%s" data-zu="%s"%s>' % (klasse, kid, attr)
                t_ += ('<g class="bew-pt"><circle r="11" fill="%s" stroke="%s" stroke-width="3.5"/>'
                       '<circle r="5" fill="%s"/></g>' % (papier, f_, f_))
                if text:
                    t_ += '<text font-size="29" font-weight="600" fill="%s" stroke="%s" stroke-width="5" paint-order="stroke" stroke-linejoin="round"></text>' % (f_, papier)
                return t_ + '</g>'
            # Nur bei "trig": der Einheitskreis links neben der Kurve. Mittelpunkt (mx | 0),
            # Radius 1 in y-Einheiten (der Kreis bleibt rund, auch wenn die Achsen verschieden
            # geteilt sind). "bahn": [[t, Winkel], …] fuehrt den Punkt P; eine waagrechte
            # Strecke traegt seine Hoehe zur Kurve (bei tan: der Punkt auf der Tangente x = 1).
            # "spur": true zeichnet die Kurve nur bis zum aktuellen Winkel — das Abrollen.
            kk = kv.get("kreis")
            if kv.get("trig") and kk:
                f_ = fv[kk.get("farbe", 1) - 1]
                teile.append(
                    '<g class="bew-kk" data-zu="%s" data-mx="%g" data-bahn="%s" data-spur="%d" data-proj="%d" data-art="%s">'
                    '<circle class="kk-kreis" fill="none" stroke="%s" stroke-width="3" stroke-opacity=".55"/>'
                    '<path class="kk-bogen" fill="none" stroke="%s" stroke-width="7" stroke-opacity=".45" stroke-linecap="round"/>'
                    '<line class="kk-tang" stroke="%s" stroke-width="3" stroke-opacity=".55"/>'
                    '<line class="kk-radius" stroke="%s" stroke-width="3"/>'
                    '<line class="kk-hoehe" stroke="%s" stroke-width="5"/>'
                    '<line class="kk-proj" stroke="%s" stroke-width="3" stroke-dasharray="10 8"/>'
                    '<circle class="kk-p" r="11" fill="%s" stroke="%s" stroke-width="3.5"/>'
                    '<circle class="kk-q" r="11" fill="%s" stroke="%s" stroke-width="3.5"/>'
                    '%s</g>' % (kid, kk.get("mx", -1.6), entschaerfen(json.dumps(kk["bahn"])),
                              1 if kk.get("spur") else 0, 0 if kk.get("projektion") is False else 1,
                              kk.get("art", "sin"),
                              tinte, f_, tinte, tinte, f_, tinte,
                              papier, f_, papier, f_,
                              # "name": "P" (seit 08.10.2026) — der Name am laufenden Punkt, radial nach
                              # aussen, "name_abstand" px (Standard 30); KREISNAME_JS setzt ihn
                              '<text class="kk-name" data-abstand="%g" font-size="34" font-style="italic" '
                              'fill="%s" stroke="%s" stroke-width="8" paint-order="stroke" text-anchor="middle">%s</text>'
                              % (kk.get("name_abstand", 30), tinte, papier, entschaerfen(kk["name"]))
                              if kk.get("name") else ""))
            if kv.get("startpunkt"):
                teile.append(k_punkt("bew-ks", kv["startpunkt"].get("farbe", 3),
                                     text=kv["startpunkt"].get("beschriftung", True) is not False))
            # Nur bei "polynom": die Nullstellen (je Linearfaktor ein Punkt auf der
            # x-Achse; zusammenfallende zeigen einen) und die Extrempunkte H und T,
            # numerisch aus dem Vorzeichenwechsel der Steigung.
            if kv.get("polynom") and kv.get("nullstellen"):
                nst = kv["nullstellen"]
                for i_ in range(len(kv["bewegung"][0]) - 2):
                    teile.append(k_punkt("bew-kn", nst.get("farbe", 2), ' data-i="%d"' % i_,
                                         text=nst.get("beschriftung", True) is not False))
            if kv.get("polynom") and kv.get("extrema"):
                ex_ = kv["extrema"]
                for i_ in range(len(kv["bewegung"][0]) - 3):
                    teile.append(k_punkt("bew-ke", ex_.get("farbe", 3), ' data-i="%d"' % i_,
                                         text=ex_.get("beschriftung", True) is not False))
            for mk in kv.get("marken", []):
                teile.append(k_punkt("bew-km", mk.get("farbe", 5),
                                     ' data-x="%g" data-text="%s"%s' % (mk["x"], entschaerfen(mk.get("text", "")), lage(mk))))
            # "laeufer" (seit 07.10.2026): {"bahn": [[t, x], …], "text": "({x} | {y})", "farbe": 3} —
            # ein Punkt, der auf der Kurve faehrt, wie bei Parabel und Gerade. Technisch eine
            # Marke, deren x aus der Bahn kommt; darum fuer alle Kurvenarten.
            lf = kv.get("laeufer")
            if lf:
                nach_oben(kv, lf, k_punkt("bew-km", lf.get("farbe", 3),
                                     ' data-x="0" data-bahn="%s" data-text="%s"%s'
                                     % (entschaerfen(json.dumps(lf["bahn"])), entschaerfen(lf.get("text", "")), lage(lf)),
                                     text=bool(lf.get("text"))))
            continue
        # "betrag_von": "x**2+q" (seit 07.10.2026) ist kurz fuer "formel": "abs(x**2+q)" — die
        # umgeklappte Kurve |f| in einem Stueck, auch wenn sie sich bewegt.
        if kv.get("betrag_von"):
            kv = dict(kv, formel="abs(%s)" % kv["betrag_von"])
        # "parameter": [[t, {"q": -4}], [t, {"q": -1}], …] (seit 07.10.2026) — eine Formelkurve mit
        # Buchstaben, die sich waehrend der Szene aendern. Gezeichnet im Abspieler (formel_js);
        # "punkte": [{"x": "pi/(6*b)", "text": "({x} | {y})", "farbe": 2}] fahren mit, ihr x
        # ist selbst eine Formel in den Parametern (oder eine Zahl).
        if kv.get("parameter"):
            namen = []
            for _, felder in kv["parameter"]:
                namen += [k for k in felder if k not in namen]
            stand, zeilen = {}, []
            for t_, felder in kv["parameter"]:
                stand.update(felder)
                if len(stand) < len(namen):
                    raise SystemExit("parameter: der erste Stuetzpunkt braucht alle Buchstaben %s" % namen)
                zeilen.append([t_] + [stand[k] for k in namen])
            for k in namen:
                if k in _KURVE_NS or k == "x":
                    raise SystemExit("parameter: %r ist schon vergeben" % k)
            fid = "fp%d" % nr
            farbe = fv[kv.get("farbe", 1) - 1]
            teile.append('<path data-fp="%s" data-paar="%s" data-namen="%s" data-js="%s" data-fenster="%g,%g,%g,%g,%d,%d,%d" '
                         'data-von="%g" data-bis="%g" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" '
                         'stroke-linejoin="round" %s/>'
                         % (entschaerfen(json.dumps(zeilen)), fid, ",".join(namen), entschaerfen(formel_js(kv["formel"])),
                            x0, x1, y0, y1, b, h, rand, kv.get("von", x0), kv.get("bis", x1),
                            farbe, kv.get("dicke", 5), 'stroke-dasharray="14 10"' if kv.get("gestrichelt") else ""))
            for pt_ in kv.get("punkte", []):
                f_ = fv[pt_.get("farbe", 2) - 1]
                # eigenes "ein"/"aus" je Punkt (mit_zeit), wie beim Laeufer
                teile.append(mit_zeit(pt_, '<g class="fp-p" data-zu="%s" data-xjs="%s" data-text="%s"%s>'
                             '<g class="bew-pt"><circle r="11" fill="%s" stroke="%s" stroke-width="3.5"/>'
                             '<circle r="5" fill="%s"/></g>%s</g>'
                             % (fid, entschaerfen(formel_js(str(pt_["x"]))), entschaerfen(pt_.get("text", "")), lage(pt_),
                                papier, f_, f_,
                                ('<text font-size="29" font-weight="600" fill="%s" stroke="%s" stroke-width="5" '
                                 'paint-order="stroke" stroke-linejoin="round"></text>' % (f_, papier))
                                if pt_.get("text") else "")))
            continue
        n = kv.get("n", 480)
        # Eine Kurve darf auch nur ein Stueck des Fensters belegen. Gebraucht
        # wird das fuer Hilfslinien wie die Mittellinie einer Schwingung: Ohne
        # Grenze laeuft sie ueber die Achsenbeschriftung am linken Rand.
        a_ = kv.get("von", x0)
        e_ = kv.get("bis", x1)
        stuecke, lauf = [], []
        for i in range(n + 1):
            x = a_ + (e_ - a_) * i / n
            y = kurve_wert(kv["formel"], x)
            if y is not None and y0 <= y <= y1:
                lauf.append("%.1f,%.1f" % (px(x), py(y)))
            elif lauf:
                stuecke.append(lauf)
                lauf = []
        if lauf:
            stuecke.append(lauf)
        farbe = fv[kv.get("farbe", 1) - 1]
        # "laeufer" an einer festen Formelkurve (seit 07.10.2026): Der Abspieler kennt die
        # Formel nicht; er bekommt die Werte als Tabelle (n + 1 Stellen von "von" bis "bis")
        # und liest dazwischen linear ab. Bahn, Text und Farbe wie bei den bewegten Kurven.
        lf = kv.get("laeufer")
        if lf:
            tab = []
            for i in range(n + 1):
                y = kurve_wert(kv["formel"], a_ + (e_ - a_) * i / n)
                tab.append(None if y is None else round(y, 5))
            f_ = fv[lf.get("farbe", 3) - 1]
            nach_oben(kv, lf, '<g class="fk-l" data-fkl="%s" data-tab="%s" data-ab="%g" data-bis="%g" data-text="%s"%s '
                         'data-fenster="%g,%g,%g,%g,%d,%d,%d">'
                         '<g class="bew-pt"><circle r="11" fill="%s" stroke="%s" stroke-width="3.5"/>'
                         '<circle r="5" fill="%s"/></g>%s</g>'
                         % (entschaerfen(json.dumps(lf["bahn"])), json.dumps(tab).replace(" ", ""), a_, e_,
                            entschaerfen(lf.get("text", "")), lage(lf), x0, x1, y0, y1, b, h, rand, papier, f_, f_,
                            ('<text font-size="29" font-weight="600" fill="%s" stroke="%s" stroke-width="5" '
                             'paint-order="stroke" stroke-linejoin="round"></text>' % (f_, papier))
                            if lf.get("text") else ""))
        for st in stuecke:
            if len(st) > 1:
                teile.append('<polyline points="%s" fill="none" stroke="%s" '
                             'stroke-width="%s" stroke-linecap="round" '
                             'stroke-linejoin="round" %s/>'
                             % (" ".join(st), farbe, kv.get("dicke", 5),
                                'stroke-dasharray="14 10"' if kv.get("gestrichelt") else ""))
        if kv.get("beschriftung"):
            bx_, by_ = kv["beschriftung_bei"]
            teile.append('<text x="%.1f" y="%.1f" font-size="27" fill="%s" '
                         'text-anchor="%s">%s</text>'
                         % (px(bx_), py(by_), farbe, kv.get("anker", "start"),
                            entschaerfen(kv["beschriftung"])))

    # Strecken und Pfeile in Datenkoordinaten (Physik 06.10.2026): Hilfslinien
    # zu einem Ablesewert, Vektoren, Kraftpfeile. "pfeil": true setzt eine
    # Spitze am Ende; die Beschriftung steht bei "beschriftung_bei" oder rechts
    # neben der Mitte. Gezeichnet ueber den Kurven, unter den Punkten.
    for st in zeitlich(el.get("strecken", [])):
        farbe = fv[st.get("farbe", 5) - 1]
        (ax, ay), (bx, by) = st["von"], st["bis"]
        X1, Y1, X2, Y2 = px(ax), py(ay), px(bx), py(by)
        dicke = st.get("dicke", 3 if st.get("gestrichelt") else 5)
        if st.get("pfeil"):
            lg = math.hypot(X2 - X1, Y2 - Y1) or 1
            ux, uy = (X2 - X1) / lg, (Y2 - Y1) / lg
            sp = st.get("spitze", 22)
            X2s, Y2s = X2 - ux * sp * 0.8, Y2 - uy * sp * 0.8
            teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" '
                         'stroke-linecap="round" %s/>'
                         % (X1, Y1, X2s, Y2s, farbe, dicke,
                            'stroke-dasharray="9 7"' if st.get("gestrichelt") else ""))
            teile.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                         % (X2, Y2, X2 - ux * sp - uy * sp * 0.45, Y2 - uy * sp + ux * sp * 0.45,
                            X2 - ux * sp + uy * sp * 0.45, Y2 - uy * sp - ux * sp * 0.45, farbe))
        else:
            teile.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" '
                         'stroke-linecap="round" %s/>'
                         % (X1, Y1, X2, Y2, farbe, dicke,
                            'stroke-dasharray="9 7"' if st.get("gestrichelt") else ""))
        if st.get("beschriftung"):
            if st.get("beschriftung_bei"):
                tx, ty = px(st["beschriftung_bei"][0]), py(st["beschriftung_bei"][1])
            else:
                tx, ty = (X1 + X2) / 2 + 14, (Y1 + Y2) / 2 - 10
            teile.append('<text x="%.1f" y="%.1f" font-size="%s" font-weight="600" fill="%s" '
                         'text-anchor="%s" stroke="%s" stroke-width="8" paint-order="stroke">%s</text>'
                         % (tx, ty, st.get("groesse", 27), farbe, st.get("anker", "start"), papier,
                            entschaerfen(st["beschriftung"])))

    # Freie Beschriftungen in Datenkoordinaten (Physik 06.10.2026)
    for tx_ in zeitlich(el.get("texte", [])):
        farbe = fv[tx_.get("farbe", 5) - 1]
        teile.append('<text x="%.1f" y="%.1f" font-size="%s" font-weight="%s" fill="%s" text-anchor="%s" '
                     'stroke="%s" stroke-width="8" paint-order="stroke">%s</text>'
                     % (px(tx_["bei"][0]), py(tx_["bei"][1]), tx_.get("groesse", 27),
                        tx_.get("gewicht", 600), farbe, tx_.get("anker", "start"), papier,
                        entschaerfen(tx_["text"])))

    # Punkte
    for pt in zeitlich(el.get("punkte", [])):
        farbe = fv[pt.get("farbe", 3) - 1]
        teile.append('<circle cx="%.1f" cy="%.1f" r="11" fill="%s" stroke="%s" stroke-width="3.5"/>'
                     % (px(pt["x"]), py(pt["y"]), papier, farbe))
        teile.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>'
                     % (px(pt["x"]), py(pt["y"]), farbe))
        if pt.get("beschriftung"):
            # Ohne Angabe steht die Beschriftung rechts ueber dem Punkt. Das
            # trifft am Scheitel einer Parabel die Achsenbeschriftung — darum
            # kann man sie wie bei Geraden und Parabeln frei setzen.
            if pt.get("beschriftung_bei"):
                bx_, by_ = pt["beschriftung_bei"]
                tx, ty = px(bx_), py(by_)
            else:
                tx, ty = px(pt["x"]) + 18, py(pt["y"]) - 16
            teile.append('<text x="%.1f" y="%.1f" font-size="29" font-weight="600" fill="%s" '
                         'text-anchor="%s"%s>%s</text>'
                         % (tx, ty, farbe, pt.get("anker", "start"),
                            ' class="pb" data-pt="%.1f,%.1f"' % (px(pt["x"]), py(pt["y"])) if ausw else "",
                            entschaerfen(pt["beschriftung"])))
    # "tippbar": true (seit 05.10.2026) — ein leerer Pfad mit dem Fenster, damit eine Klickfrage
    # das Bild auch dann findet, wenn es nur feste Kurven zeigt. Der Abspieler sucht fuer
    # Klickfragen das sichtbare Bild mit [data-fenster]; bisher trugen das nur bewegte Kurven.
    teile.extend(zuoberst)
    if el.get("tippbar"):
        teile.append('<path data-fenster="%g,%g,%g,%g,%d,%d,%d" d="" fill="none"/>' % (x0, x1, y0, y1, b, h, rand))
    teile.extend(achsnamen)
    teile.append("</svg>")
    return "".join(teile)


# ---------------------------------------------------------------- Rechneranzeige
def rechner_svg(el, theme):
    """Die Anzeige des TI-30X Pro MathPrint, so weit sie nachpruefbar ist.

    Belegt sind: vier Zeilen zu 16 Zeichen, Eingabe oben, Ergebnis
    rechtsbuendig, getrennte Tasten fuer Subtraktion (−) und negatives
    Vorzeichen ((−)), Berechnen mit =, Brueche ueber n/d. Quelle ist das
    Handbuch von Texas Instruments.

    **Nachgebaut wird die Anzeige, nicht das Tastenfeld.** Wo die Tasten
    auf dem Geraet liegen, steht hier nicht — es wird nur gezeigt, welche
    gedrueckt wird. Eine erfundene Tastenanordnung waere schlimmer als
    keine: Wer sie lernt, greift am Geraet daneben.

    Bruchdarstellung im Text: [a|b] wird zweistoeckig gesetzt, wie es
    MathPrint tut.
    """
    b = el.get("breite", 700)
    zeilen = el.get("zeilen", [])
    # Die Hoehe ergibt sich aus der Breite: 16 Zeichen, vier Zeilen. Sie
    # wird ins Element geschrieben, damit der senkrechte Fluss sie kennt
    # und die naechste Zeile nicht in die Anzeige laeuft.
    # Das Geraet hat vier Zeilen. Gezeigt werden nur die benutzten plus
    # die Ergebniszeile — ein zu drei Vierteln leeres Feld sieht nach
    # Fehler aus, nicht nach Anzeige.
    benutzt = min(4, max(2, len(el.get("zeilen", []))
                         + (1 if el.get("ergebnis") is not None else 0)))
    el["_zeilen"] = benutzt
    # Ein Bruch ist zweistoeckig und braucht rund die anderthalbfache
    # Zeilenhoehe — sonst schneidet der Rand Zaehler und Nenner ab.
    bruch = any("[" in z for z in list(el.get("zeilen", []))
                + ([el["ergebnis"]] if el.get("ergebnis") else []))
    el["_hoch"] = 1.55 if bruch else 1.0
    el.setdefault("hoehe", int(benutzt * ((b - 60) / 16 * 1.85 * el["_hoch"]) + 46
                               + (82 if (el.get("taste") or el.get("tasten")) else 0)))
    ergebnis = el.get("ergebnis")
    # Eine Taste oder eine Reihe: gedrueckte Tasten bleiben stehen, die
    # zuletzt gedrueckte ist gefuellt. So sieht man die ganze Folge, nicht
    # nur den letzten Anschlag.
    reihe = el.get("tasten") or ([el["taste"]] if el.get("taste") else [])
    taste = reihe[-1] if reihe else None
    tinte = theme["tinte"]
    lcd = el.get("lcd", "#c9d4c4")          # gruenlich, wie ein LCD
    rahmen = el.get("rahmen", "#2b2b2b")

    zeichen = 16
    zb = (b - 60) / zeichen                  # Zeichenbreite
    zh = zb * 1.85 * el.get("_hoch", 1.0)    # Zeilenhoehe
    reihen = el.get("_zeilen", 4)
    h_disp = reihen * zh + 46
    h = h_disp + (74 if taste else 0)
    t = ['<svg width="%d" height="%d" viewBox="0 0 %d %d">' % (b, h, b, h)]
    # Deckende Flaeche ueber das ganze Element. Eine Tastenfolge wird als
    # Stapel gebaut: Jede neue Anzeige muss die vorige vollstaendig
    # verdecken, auch im Tastenband — sonst schauen aeltere Kappen zwischen
    # den neuen hervor.
    t.append('<rect x="0" y="0" width="%d" height="%d" fill="%s"/>'
             % (b, h, theme["papier"]))
    t.append('<rect x="0" y="0" width="%d" height="%.0f" rx="14" fill="%s"/>'
             % (b, h_disp, rahmen))
    t.append('<rect x="18" y="16" width="%d" height="%.0f" rx="5" fill="%s"/>'
             % (b - 36, h_disp - 32, lcd))

    def setzen(text, y, rechts=False):
        """Eine Displayzeile. [a|b] wird zum Bruch."""
        teile = re.split(r"(\[[^\[\]|]*\|[^\[\]|]*\])", text)
        breite = 0
        for st in teile:
            breite += (len(st) - 3) * zb if st.startswith("[") else len(st) * zb
        x = (b - 30 - breite) if rechts else 30
        for st in teile:
            if st.startswith("["):
                oben, unten = st[1:-1].split("|")
                w = max(len(oben), len(unten)) * zb
                mitte = y - zb * 0.55            # Strich etwa auf halber Zeichenhoehe
                t.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="%.1f" '
                         'text-anchor="middle" fill="%s">%s</text>'
                         % (x + w / 2, mitte - zb * 0.22, "monospace", zb * 1.25, tinte,
                            entschaerfen(oben)))
                t.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                         'stroke-width="2.5"/>' % (x, mitte, x + w, mitte, tinte))
                t.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="%.1f" '
                         'text-anchor="middle" fill="%s">%s</text>'
                         % (x + w / 2, mitte + zb * 1.15, "monospace", zb * 1.25, tinte,
                            entschaerfen(unten)))
                x += w
            elif st:
                t.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="%.1f" '
                         'fill="%s" xml:space="preserve">%s</text>'
                         % (x, y, "monospace", zb * 1.7, tinte, entschaerfen(st)))
                x += len(st) * zb

    # Grundlinie der ersten Zeile: so weit unter der Oberkante, dass die
    # Oberlaengen im Feld bleiben.
    y0 = 22 + zh * 0.78
    for i, z in enumerate(zeilen[:reihen]):
        setzen(z, y0 + i * zh)
    if ergebnis is not None:
        setzen(ergebnis, y0 + min(len(zeilen), reihen - 1) * zh, rechts=True)

    if taste:
        kappen = [(k, max(60, 26 + len(k) * 19)) for k in reihe]
        luecke = 9
        platz = b - 16

        def gesamtbreite(ks, f=1.0):
            return sum(w * f for _, w in ks) + luecke * (len(ks) - 1)

        # Passt die Reihe nicht, wird sie erst schmaler gesetzt und, wenn das
        # nicht reicht, vorn gekuerzt: Die letzten Anschlaege sind die, auf
        # die es ankommt.
        skala = 1.0
        if gesamtbreite(kappen) > platz:
            skala = max(0.62, platz / gesamtbreite(kappen))
        while len(kappen) > 1 and gesamtbreite(kappen, skala) > platz:
            kappen = kappen[1:]
            if kappen and kappen[0][0] != "…":
                kappen = [("…", 40 / skala)] + kappen
        kappen = [(k, w * skala) for k, w in kappen]
        gesamt = sum(w for _, w in kappen) + luecke * (len(kappen) - 1)
        x = max(8, (b - gesamt) / 2)
        y = h_disp + 12
        for i, (k, w) in enumerate(kappen):
            jetzt = (i == len(kappen) - 1)
            t.append('<rect x="%.1f" y="%.1f" width="%.1f" height="54" rx="10" fill="%s" '
                     'stroke="%s" stroke-width="%s" %s/>'
                     % (x, y, w, tinte if jetzt else theme.get("karte", "#fff"),
                        tinte, "2.5" if jetzt else "2",
                        "" if jetzt else 'stroke-opacity=".45"'))
            t.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="%d" '
                     'text-anchor="middle" font-weight="600" fill="%s" %s>%s</text>'
                     % (x + w / 2, y + 36, "monospace",
                        max(14, int((26 if len(k) < 4 else 20) * skala)),
                        theme["papier"] if jetzt else tinte,
                        "" if jetzt else 'fill-opacity=".5"', entschaerfen(k)))
            x += w + luecke
    t.append("</svg>")
    return "".join(t)


# ---------------------------------------------------------------- Elemente
# Abspieler-Zusatz fuer "bewegung" (Prototyp 02.10.2026). seek(t) wird
# umgehaengt: erst die Ebenen wie immer, dann jede bewegte Parabel aus der
# Zeit neu gerechnet. Zwischen zwei Stuetzpunkten weich (smoothstep); wer
# "Bewegung reduzieren" eingestellt hat, sieht die Stuetzpunkte als Spruenge.
BEWEGUNG_JS = r'''
const RUHIG = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
const BEW = [...document.querySelectorAll('[data-t0]')].map(L => ({
  t0: parseFloat(L.dataset.t0),
  teile: [...L.querySelectorAll('[data-bew]')].map(p => ({
    art: 'p', p, L, t0: parseFloat(L.dataset.t0), k: JSON.parse(p.dataset.bew), f: p.dataset.fenster.split(',').map(Number) }))
    .concat([...L.querySelectorAll('[data-bewg]')].map(p => ({
      art: 'g', p, L, t0: parseFloat(L.dataset.t0), k: JSON.parse(p.dataset.bewg), f: p.dataset.fenster.split(',').map(Number) })))
    .concat([...L.querySelectorAll('[data-bewk]')].map(p => ({
      art: 'k', p, L, t0: parseFloat(L.dataset.t0), k: JSON.parse(p.dataset.bewk), f: p.dataset.fenster.split(',').map(Number),
      stufen: p.dataset.stufen === '1', poly: p.dataset.poly === '1', el: p.dataset.el || '', lin: p.dataset.gleich === '1' })))
    .concat([...L.querySelectorAll('[data-fkl]')].map(p => ({
      art: 'f', p, L, t0: parseFloat(L.dataset.t0), k: JSON.parse(p.dataset.fkl), f: p.dataset.fenster.split(',').map(Number),
      tab: JSON.parse(p.dataset.tab), ab: parseFloat(p.dataset.ab), bis: parseFloat(p.dataset.bis) })))
    .concat([...L.querySelectorAll('[data-fp]')].map(p => {
      const namen = p.dataset.namen.split(',');
      return { art: 'fp', p, L, t0: parseFloat(L.dataset.t0), k: JSON.parse(p.dataset.fp), f: p.dataset.fenster.split(',').map(Number),
        fn: new Function('x', ...namen, 'return ' + p.dataset.js), namen };
    }))
}));
// Formelkurve mit Parametern ("parameter", seit 07.10.2026): die Formel kommt als JavaScript aus
// dem Bauer (formel_js), die Buchstaben aus der Zeit. Luecken (NaN, Pole) brechen den Zug ab.
function bewegeFormel(T, t, px, py, x0, x1, y0, y1) {
  const P = bewZustand(T.k, t - T.t0);
  const f = x => { const y = T.fn(x, ...P); return isFinite(y) ? y : null; };
  const a0 = Math.max(x0, parseFloat(T.p.dataset.von)), a1 = Math.min(x1, parseFloat(T.p.dataset.bis));
  let d = '', an = false;
  for (let i = 0; i <= 600; i++) {
    const x = a0 + (a1 - a0) * i / 600, y = f(x);
    if (y === null || y < y0 || y > y1) { an = false; continue; }
    d += (an ? 'L' : 'M') + px(x).toFixed(1) + ',' + py(y).toFixed(1); an = true;
  }
  T.p.setAttribute('d', d);
  for (const g of T.L.querySelectorAll('[data-zu="' + T.p.dataset.paar + '"]')) {
    const fx = g._fx || (g._fx = new Function(...T.namen, 'return ' + g.dataset.xjs));
    const x = fx(...P), y = f(x);
    const ok = y !== null && x >= x0 && x <= x1 && y >= y0 && y <= y1;
    g.style.display = ok ? '' : 'none';
    if (!ok) continue;
    g.querySelectorAll('circle').forEach(c => { c.setAttribute('cx', px(x)); c.setAttribute('cy', py(y)); });
    const tx = g.querySelector(':scope > text'); if (!tx) continue;
    const rechts = x > x1 - (x1 - x0) * 0.3;
    tx.setAttribute('x', px(x) + (rechts ? -18 : 18)); tx.setAttribute('y', py(y) < 60 ? py(y) + 44 : py(y) - 22);
    tx.setAttribute('text-anchor', rechts ? 'end' : 'start');
    tx.textContent = g.dataset.text.replace('{x}', bewZahl(x)).replace('{y}', bewZahl(y));
  }
}
// Zuletzt die Beschriftungen der mitfahrenden Punkte (seit 07.10.2026): "lage" setzt sie fest
// (oben, unten, links, rechts, auch zwei davon), und keine ragt ueber den Rand des Bildes.
function beschriftungenRichten() {
  for (const L of document.querySelectorAll('[data-t0]'))
    for (const g of L.querySelectorAll('[data-zu], .fk-l')) {
      if (g.style.display === 'none') continue;
      const tx = g.querySelector(':scope > text'), c = g.querySelector('.bew-pt circle');
      if (!tx || !c || !tx.textContent) continue;
      const X = parseFloat(c.getAttribute('cx')), Y = parseFloat(c.getAttribute('cy'));
      if (g.dataset.lage) {
        const w = g.dataset.lage.split(/\s+/), li = w.includes('links'), re = w.includes('rechts');
        const ob = w.includes('oben'), un = w.includes('unten');
        tx.setAttribute('x', X + (li ? -18 : re ? 18 : 0));
        tx.setAttribute('y', ob ? Y - 22 : un ? Y + 44 : Y + 10);
        tx.setAttribute('text-anchor', li ? 'end' : re ? 'start' : 'middle');
      }
      let w;
      try { w = tx.getComputedTextLength(); } catch (e) { continue; }
      const svg = tx.ownerSVGElement; if (!w || !svg) continue;
      const B = svg.viewBox.baseVal && svg.viewBox.baseVal.width || svg.width.baseVal.value;
      const x = parseFloat(tx.getAttribute('x')), an = tx.getAttribute('text-anchor') || 'start';
      const l = an === 'start' ? x : an === 'end' ? x - w : x - w / 2;
      // Seitlich stehende Beschriftung auf die andere Seite des Punkts klappen, mittige schieben
      if (l + w > B - 4) {
        if (an === 'start' && X - 18 - w >= 4) { tx.setAttribute('x', X - 18); tx.setAttribute('text-anchor', 'end'); }
        else tx.setAttribute('x', x - (l + w - (B - 4)));
      } else if (l < 4) {
        if (an === 'end' && X + 18 + w <= B - 4) { tx.setAttribute('x', X + 18); tx.setAttribute('text-anchor', 'start'); }
        else tx.setAttribute('x', x + (4 - l));
      }
    }
}
// Laeufer auf einer festen Formelkurve: x aus der Bahn, y linear aus der Wertetabelle.
function laufeFest(T, t, px, py, x0, x1, y0, y1) {
  const x = bewZustand(T.k, t - T.t0)[0], n = T.tab.length - 1;
  const q = (x - T.ab) / (T.bis - T.ab) * n, i = Math.min(n - 1, Math.max(0, Math.floor(q)));
  const ya = T.tab[i], yb = T.tab[i + 1];
  const y = ya === null || yb === null ? null : ya + (yb - ya) * (q - i);
  const ok = y !== null && q >= 0 && q <= n && x >= x0 && x <= x1 && y >= y0 && y <= y1;
  T.p.style.display = ok ? '' : 'none';
  if (!ok) return;
  T.p.querySelectorAll('circle').forEach(c => { c.setAttribute('cx', px(x)); c.setAttribute('cy', py(y)); });
  const tx = T.p.querySelector(':scope > text'); if (!tx) return;
  const rechts = x > x1 - (x1 - x0) * 0.25;
  tx.setAttribute('x', px(x) + (rechts ? -18 : 18)); tx.setAttribute('y', py(y) < 60 ? py(y) + 44 : py(y) - 22);
  tx.setAttribute('text-anchor', rechts ? 'end' : 'start');
  tx.textContent = T.p.dataset.text.replace('{x}', bewZahl(x)).replace('{y}', bewZahl(y));
}
// Zwischen zwei Stuetzpunkten weich (lin: gleichmaessig). Wie viele Zahlen ein Stuetzpunkt traegt, sagt er
// selbst: [t, a, u, v] bei einer Parabel, [t, m, q] bei einer Geraden, [t, x] bei einer Bahn.
function bewZustand(k, t, lin) {
  const n = k[0].length - 1;
  if (t <= k[0][0]) return k[0].slice(1);
  for (let i = 0; i < k.length - 1; i++) {
    if (t < k[i + 1][0]) {
      let q = (t - k[i][0]) / (k[i + 1][0] - k[i][0]);
      q = RUHIG ? 0 : lin ? q : q * q * (3 - 2 * q);
      const aus = [];
      for (let j = 1; j <= n; j++) aus.push(k[i][j] + (k[i + 1][j] - k[i][j]) * q);
      return aus;
    }
  }
  return k[k.length - 1].slice(1);
}
// Eine Nachkommastelle — ausser der Wert hat genau zwei (−0.75, −1.25): dann beide, sonst
// stuende an einem ruhenden Punkt eine falsch gerundete Zahl (seit 07.10.2026). Waehrend einer
// Bewegung sind die Werte krumm und bleiben bei einer Stelle.
const bewZahl = x => {
  const z = Math.round(x * 100);
  const r = Math.abs(x * 100 - z) < 1e-6 && z % 10 !== 0 ? z / 100 : Math.round(x * 10) / 10;
  return (r < 0 ? '−' : '') + Math.abs(r);
};
// Eine bewegte Gerade y = m x + q: am Fenster abgeschnitten, dazu ihre Begleiter.
function bewegeGerade(T, t, px, py, x0, x1, y0, y1) {
  const [m, q] = bewZustand(T.k, t - T.t0);
  if (T.p.dataset.ab !== undefined) x0 = Math.max(x0, parseFloat(T.p.dataset.ab));
  const f = x => m * x + q, innen = (x, y) => x >= x0 - 1e-9 && x <= x1 + 1e-9 && y >= y0 - 1e-9 && y <= y1 + 1e-9;
  const pt = [];
  for (const x of [x0, x1]) { const y = f(x); if (y >= y0 - 1e-9 && y <= y1 + 1e-9) pt.push([x, y]); }
  if (Math.abs(m) > 1e-9) for (const y of [y0, y1]) { const x = (y - q) / m; if (x >= x0 - 1e-9 && x <= x1 + 1e-9) pt.push([x, y]); }
  pt.sort((u, v) => u[0] - v[0]);
  T.p.setAttribute('d', pt.length > 1
    ? 'M' + px(pt[0][0]).toFixed(1) + ',' + py(pt[0][1]).toFixed(1) +
      'L' + px(pt[pt.length - 1][0]).toFixed(1) + ',' + py(pt[pt.length - 1][1]).toFixed(1)
    : '');
  const setze = (g, x, y) => { g.style.display = innen(x, y) ? '' : 'none';
    g.querySelectorAll('circle').forEach(c => { c.setAttribute('cx', px(x)); c.setAttribute('cy', py(y)); }); };
  const beschrifte = (g, x, y, text) => {
    const tx = g.querySelector(':scope > text'); if (!tx) return;
    const rechts = x > x1 - (x1 - x0) * 0.3;
    tx.setAttribute('x', px(x) + (rechts ? -18 : 18));
    const nahAchse = Math.abs(py(y) - py(0)) < 40;             // dort stehen die x-Marken
    tx.setAttribute('y', py(y) + (nahAchse ? -18 : (m > 0 ? 44 : -18)));
    tx.setAttribute('text-anchor', rechts ? 'end' : 'start');
    tx.textContent = text;
  };
  const fuell = (v, x, y) => v.replace('{x}', bewZahl(x)).replace('{y}', bewZahl(y))
                              .replace('{m}', bewZahl(m)).replace('{q}', bewZahl(q));
  for (const g of T.L.querySelectorAll('[data-zu="' + T.p.dataset.paar + '"]')) {
    if (g.classList.contains('bew-gy')) {
      setze(g, 0, q); beschrifte(g, 0, q, '(0 | ' + bewZahl(q) + ')');
    } else if (g.classList.contains('bew-gn')) {
      if (Math.abs(m) < 1e-9) { g.style.display = 'none'; continue; }
      const xn = -q / m; setze(g, xn, 0); beschrifte(g, xn, 0, '(' + bewZahl(xn) + ' | 0)');
    } else if (g.classList.contains('bew-gm')) {
      const x = parseFloat(g.dataset.x);
      setze(g, x, f(x)); beschrifte(g, x, f(x), fuell(g.dataset.text, x, f(x)));
    } else if (g.classList.contains('bew-gl')) {
      const bahn = g._bahn || (g._bahn = JSON.parse(g.dataset.bahn));
      const x = bewZustand(bahn, t - T.t0)[0];
      setze(g, x, f(x)); beschrifte(g, x, f(x), fuell(g.dataset.text, x, f(x)));
    } else if (g.classList.contains('bew-gs-tab')) {
      // Schnittpunkte mit einer festen Kurve (Tabelle): Vorzeichenwechsel von Kurve − Gerade,
      // dazu Beruehrstellen (|Differenz| lokal minimal und fast null).
      const tab = g._tab || (g._tab = JSON.parse(g.dataset.tab));
      const ab = parseFloat(g.dataset.ab), bis = parseFloat(g.dataset.bis), n = tab.length - 1;
      const X = i => ab + (bis - ab) * i / n, d = i => tab[i] === null ? null : tab[i] - f(X(i));
      const eps = (y1 - y0) * 2e-3, sn = [];
      for (let i = 0; i < n; i++) {
        const da = d(i), db = d(i + 1);
        if (da === null || db === null) continue;
        if (da === 0) sn.push(X(i));
        else if (da * db < 0) sn.push(X(i) + (X(i + 1) - X(i)) * da / (da - db));
        else if (i > 0 && d(i - 1) !== null && Math.abs(da) < eps && Math.abs(da) <= Math.abs(d(i - 1)) && Math.abs(da) <= Math.abs(db)) sn.push(X(i));
      }
      const gs = [];
      for (const x of sn) if (!gs.length || x - gs[gs.length - 1] > (bis - ab) / n * 1.5) gs.push(x);
      T._gs = gs;
    } else if (g.classList.contains('bew-gs')) {
      const x = (T._gs || [])[parseInt(g.dataset.i)];
      if (x === undefined) { g.style.display = 'none'; continue; }
      setze(g, x, f(x)); beschrifte(g, x, f(x), '(' + bewZahl(x) + ' | ' + bewZahl(f(x)) + ')');
      // abwechselnd ueber und unter der Geraden, sonst stossen nahe Beschriftungen zusammen
      const tx = g.querySelector(':scope > text');
      if (tx) { tx.setAttribute('y', py(f(x)) + (parseInt(g.dataset.i) % 2 ? 44 : -18));
        tx.setAttribute('text-anchor', 'middle'); tx.setAttribute('x', px(x)); }
    } else if (g.classList.contains('bew-gd')) {
      // Steigungsdreieck: von (x | f(x)) nach rechts, dann senkrecht auf die Gerade.
      let xa, dx;
      if (g.dataset.bahn) {
        const bahn = g._bahn || (g._bahn = JSON.parse(g.dataset.bahn));
        [xa, dx] = bewZustand(bahn, t - T.t0);
      } else { xa = parseFloat(g.dataset.x); dx = parseFloat(g.dataset.dx); }
      const xb = xa + dx;
      // dx = 0: kein Dreieck, auch keine Beschriftung «Δx = 0» (es waechst erst noch)
      const ya = f(xa), yb = f(xb), sichtbar = Math.abs(dx) > 1e-9 && innen(xa, ya) && innen(xb, yb);
      g.style.display = sichtbar ? '' : 'none';
      if (!sichtbar) continue;
      g.querySelector('.bew-gd-w').setAttribute('d', 'M' + px(xa) + ',' + py(ya) + 'L' + px(xb) + ',' + py(ya));
      g.querySelector('.bew-gd-s').setAttribute('d', 'M' + px(xb) + ',' + py(ya) + 'L' + px(xb) + ',' + py(yb));
      const tx = g.querySelector('.bew-gd-tx'), ty = g.querySelector('.bew-gd-ty');
      tx.setAttribute('x', px((xa + xb) / 2)); tx.setAttribute('y', py(ya) + (m > 0 ? 36 : -14));
      tx.textContent = 'Δx = ' + bewZahl(dx);
      // dx < 0: die senkrechte Kathete steht links, ihre Beschriftung auch (sonst liegt sie
      // auf der Geraden oder der y-Achse)
      ty.setAttribute('x', px(xb) + (dx < 0 ? -12 : 12)); ty.setAttribute('y', py((ya + yb) / 2) + 10);
      ty.setAttribute('text-anchor', dx < 0 ? 'end' : 'start');
      ty.textContent = 'Δy = ' + bewZahl(yb - ya);
    }
  }
}
// Eine bewegte Potenz- oder Wurzelkurve y = a*(x-u)^p + v, am Fenster abgeschnitten.
// Wo es keinen Wert gibt (Pol, negative Basis mit gebrochenem Exponenten), bricht der
// Streckenzug ab und beginnt danach neu — genau so entstehen Aeste und Definitionsluecken.
// x einer Marke an einer bewegten Kurve: fest (data-x) oder aus einer Bahn [[t, x], …] (Laeufer).
function kmX(g, T) {
  if (!g.dataset.bahn) return parseFloat(g.dataset.x);
  const bahn = g._bahn || (g._bahn = JSON.parse(g.dataset.bahn));
  return bewZustand(bahn, T._t - T.t0, T.lin)[0];
}
// Definitionsbereich einer bewegten Kurve: fest (data-von/data-bis) oder mitwandernd
// ("grenzen": [[t, von, bis], …], seit 07.10.2026 — Einschraenken, ein Intervall zieht sich zu).
function kGrenzen(T) {
  if (!T.p.dataset.grenzen) return [parseFloat(T.p.dataset.von), parseFloat(T.p.dataset.bis)];
  const gr = T._gr || (T._gr = JSON.parse(T.p.dataset.grenzen));
  return bewZustand(gr, T._t - T.t0, T.lin);
}
function bewegeKurve(T, t, px, py, x0, x1, y0, y1) {
  T._t = t;
  const Z = bewZustand(T.k, t - T.t0, T.lin);
  if (T.poly) return bewegePolynom(T, Z, px, py, x0, x1, y0, y1);
  if (T.el === 's' || T.el === 't') return bewegeTrig(T, Z, t, px, py, x0, x1, y0, y1);
  if (T.el === 'v') return bewegeBetrag(T, Z, px, py, x0, x1, y0, y1);
  if (T.el) return bewegeExpLog(T, Z, px, py, x0, x1, y0, y1);
  const [a, p0, u, v] = Z;
  const p = T.stufen ? Math.round(p0) : p0;
  // Negative Basis: Math.pow(-8, 1/3) ist NaN, die dritte Wurzel aus -8 ist -2.
  // Bei ungeradem Wurzelexponenten (1/p ganz und ungerade) gibt es den Wert, bei
  // geradem nicht — genau dort endet die Definitionsmenge.
  const pot = b => {
    if (b >= 0 || Number.isInteger(p)) return Math.pow(b, p);
    const q = Math.round(1 / p);
    return (Math.abs(1 / p - q) < 1e-9 && q % 2 !== 0) ? -Math.pow(-b, p) : NaN;
  };
  const f = x => { const y = a * pot(x - u) + v;
    return (isFinite(y) && !isNaN(y)) ? y : null; };
  const [vx, bx] = kGrenzen(T);
  const a0 = Math.max(x0, vx), a1 = Math.min(x1, bx);
  const zug = (abx, aby) => {           // abx/aby: wie der Punkt auf die Achsen faellt
    let d = '', an = false;
    if (a1 <= a0) return '';
    for (let i = 0; i <= 600; i++) {
      const x = a0 + (a1 - a0) * i / 600, y = f(x);
      if (y === null) { an = false; continue; }
      const sx = abx(x, y), sy = aby(x, y);
      if (sx < -5 || sx > 1e5 || sy < -5 || sy > 1e5) { an = false; continue; }
      if (!(abx === px ? (y >= y0 && y <= y1) : (y >= x0 && y <= x1 && x >= y0 && x <= y1))) { an = false; continue; }
      d += (an ? 'L' : 'M') + sx.toFixed(1) + ',' + sy.toFixed(1); an = true;
    }
    return d;
  };
  T.p.setAttribute('d', zug(px, (x, y) => py(y)));
  // Spiegelkurve an y = x: aus (x | y) wird (y | x) — die Umkehrfunktion.
  const sp = T.L.querySelector('[data-spiegel="' + T.p.dataset.paar + '"]');
  if (sp) sp.setAttribute('d', zug((x, y) => px(y), (x, y) => py(x)));
  const innen = (x, y) => x >= x0 && x <= x1 && y >= y0 && y <= y1;
  const setze = (g, x, y) => { g.style.display = innen(x, y) ? '' : 'none';
    g.querySelectorAll('circle').forEach(c => { c.setAttribute('cx', px(x)); c.setAttribute('cy', py(y)); }); };
  const beschrifte = (g, x, y, text) => {
    const tx = g.querySelector(':scope > text'); if (!tx) return;
    const rechts = x > x1 - (x1 - x0) * 0.3;
    tx.setAttribute('x', px(x) + (rechts ? -18 : 18));
    const nahAchse = Math.abs(py(y) - py(0)) < 40;             // dort stehen die x-Marken
    tx.setAttribute('y', py(y) + (nahAchse ? -18 : (a > 0 ? 44 : -18)));
    tx.setAttribute('text-anchor', rechts ? 'end' : 'start');
    tx.textContent = text;
  };
  for (const g of T.L.querySelectorAll('[data-zu="' + T.p.dataset.paar + '"]')) {
    if (g.classList.contains('bew-ks')) {
      setze(g, u, v); beschrifte(g, u, v, '(' + bewZahl(u) + ' | ' + bewZahl(v) + ')');
    } else if (g.classList.contains('bew-ka')) {
      // Polgerade x = u und waagrechte Asymptote y = v
      g.querySelector('.bew-ka-s').setAttribute('d',
        (u >= x0 && u <= x1) ? 'M' + px(u) + ',' + py(y0) + 'L' + px(u) + ',' + py(y1) : '');
      g.querySelector('.bew-ka-w').setAttribute('d',
        (v >= y0 && v <= y1) ? 'M' + px(x0) + ',' + py(v) + 'L' + px(x1) + ',' + py(v) : '');
    } else if (g.classList.contains('bew-km')) {
      const x = kmX(g, T), y = f(x);
      if (y === null) { g.style.display = 'none'; continue; }
      setze(g, x, y);
      beschrifte(g, x, y, g.dataset.text.replace('{x}', bewZahl(x)).replace('{y}', bewZahl(y)));
    }
  }
}
// Exponentialkurve y = c*a^x + v (el 'e') oder Logarithmuskurve y = c*log_a(x) + v (el 'l');
// Z = [c, a, v]. Die Spiegelkurve an y = x ist die Umkehrfunktion.
function bewegeExpLog(T, Z, px, py, x0, x1, y0, y1) {
  const [c, a, v] = Z, ex = T.el === 'e';
  const f = x => { if (ex) return c * Math.pow(a, x) + v;
    if (x <= 0 || Math.abs(Math.log(a)) < 1e-9) return null; return c * Math.log(x) / Math.log(a) + v; };
  const [vx, bx] = kGrenzen(T);
  const a0 = Math.max(x0, vx), a1 = Math.min(x1, bx);
  const zug = (abx, aby, imBild) => {
    let d = '', an = false;
    for (let i = 0; i <= 800; i++) {
      // Nahe x = 0 fein abtasten, sonst endet die Logarithmuskurve weit über der Asymptote.
      const q = i / 800, x = a0 + (a1 - a0) * (T.el === 'l' ? q * q : q), y = f(x);
      if (y === null || !isFinite(y) || !imBild(x, y)) { an = false; continue; }
      d += (an ? 'L' : 'M') + abx(x, y).toFixed(1) + ',' + aby(x, y).toFixed(1); an = true;
    }
    return d;
  };
  const H = y1 - y0;
  T.p.setAttribute('d', zug(px, (x, y) => py(y), (x, y) => y >= y0 - H && y <= y1 + H));
  const sp = T.L.querySelector('[data-spiegel="' + T.p.dataset.paar + '"]');
  if (sp) sp.setAttribute('d', zug((x, y) => px(y), (x, y) => py(x), (x, y) => y >= x0 - 1 && y <= x1 + 1 && x >= y0 - 1 && x <= y1 + 1));
  const innen = (x, y) => x >= x0 && x <= x1 && y >= y0 && y <= y1;
  const setze = (g, x, y) => { g.style.display = innen(x, y) ? '' : 'none';
    g.querySelectorAll('circle').forEach(k => { k.setAttribute('cx', px(x)); k.setAttribute('cy', py(y)); }); };
  // Beschriftung auf die Seite, auf der die Kurve nicht verläuft: rechts unter dem Punkt bei
  // steigender, rechts über ihm bei fallender Kurve (sonst kreuzt die Kurve den Text).
  const beschrifte = (g, x, y, text) => {
    const tx = g.querySelector(':scope > text'); if (!tx) return;
    const rechts = x > x1 - (x1 - x0) * 0.3;
    const ya = f(x - 1e-3), yb = f(x + 1e-3), steigt = ya !== null && yb !== null && yb > ya;
    tx.setAttribute('x', px(x) + (rechts ? -18 : 18));
    tx.setAttribute('y', py(y) + ((steigt !== rechts) ? 44 : -18));
    tx.setAttribute('text-anchor', rechts ? 'end' : 'start');
    tx.textContent = text;
  };
  for (const g of T.L.querySelectorAll('[data-zu="' + T.p.dataset.paar + '"]')) {
    if (g.classList.contains('bew-ka')) {
      g.querySelector('.bew-ka-s').setAttribute('d', ex ? '' : 'M' + px(0) + ',' + py(y0) + 'L' + px(0) + ',' + py(y1));
      g.querySelector('.bew-ka-w').setAttribute('d', ex && v >= y0 && v <= y1 ? 'M' + px(x0) + ',' + py(v) + 'L' + px(x1) + ',' + py(v) : '');
    } else if (g.classList.contains('bew-ks')) {
      const x = ex ? 0 : 1, y = f(x); setze(g, x, y); beschrifte(g, x, y, '(' + bewZahl(x) + ' | ' + bewZahl(y) + ')');
    } else if (g.classList.contains('bew-km')) {
      const x = kmX(g, T), y = f(x);
      if (y === null) { g.style.display = 'none'; continue; }
      setze(g, x, y); beschrifte(g, x, y, g.dataset.text.replace('{x}', bewZahl(x)).replace('{y}', bewZahl(y)));
    }
  }
}
// Betragskurve y = a*|x - u| + v (el 'v'); Z = [a, u, v]. Begleiter: Knickpunkt (startpunkt),
// Symmetrieachse x = u (asymptoten), Marken.
function bewegeBetrag(T, Z, px, py, x0, x1, y0, y1) {
  const [a, u, v] = Z;
  const f = x => a * Math.abs(x - u) + v;
  const [vx, bx] = kGrenzen(T);
  const a0 = Math.max(x0, vx), a1 = Math.min(x1, bx);
  // Drei Punkte genügen: linker Rand, Knick, rechter Rand — der Knick bleibt scharf.
  const xs = [a0, Math.min(Math.max(u, a0), a1), a1];
  T.p.setAttribute('d', a1 > a0 ? xs.map((x, i) => (i ? 'L' : 'M') + px(x).toFixed(1) + ',' + py(f(x)).toFixed(1)).join('') : '');
  const innen = (x, y) => x >= x0 && x <= x1 && y >= y0 && y <= y1;
  const setze = (g, x, y) => { g.style.display = innen(x, y) ? '' : 'none';
    g.querySelectorAll('circle').forEach(k => { k.setAttribute('cx', px(x)); k.setAttribute('cy', py(y)); }); };
  const beschrifte = (g, x, y, text) => {
    const tx = g.querySelector(':scope > text'); if (!tx) return;
    const rechts = x > x1 - (x1 - x0) * 0.3;
    tx.setAttribute('x', px(x) + (rechts ? -18 : 18));
    // Unter dem Knick eines V (a > 0) ist Platz, über dem Knick eines Dachs (a < 0).
    tx.setAttribute('y', py(y) + (Math.abs(x - u) < 1e-9 ? (a > 0 ? 44 : -22) : (a > 0 ? -22 : 44)));
    tx.setAttribute('text-anchor', rechts ? 'end' : 'start');
    tx.textContent = text;
  };
  for (const g of T.L.querySelectorAll('[data-zu="' + T.p.dataset.paar + '"]')) {
    if (g.classList.contains('bew-ka')) {
      g.querySelector('.bew-ka-s').setAttribute('d', u >= x0 && u <= x1 ? 'M' + px(u) + ',' + py(y0) + 'L' + px(u) + ',' + py(y1) : '');
      g.querySelector('.bew-ka-w').setAttribute('d', '');
    } else if (g.classList.contains('bew-ks')) {
      setze(g, u, v); beschrifte(g, u, v, '(' + bewZahl(u) + ' | ' + bewZahl(v) + ')');
    } else if (g.classList.contains('bew-km')) {
      const x = kmX(g, T), y = f(x);
      setze(g, x, y); beschrifte(g, x, y, g.dataset.text.replace('{x}', bewZahl(x)).replace('{y}', bewZahl(y)));
    }
  }
}
// Sinus- oder Tangenskurve y = a*sin(b(x-u)) + v (el 's') bzw. a*tan(b(x-u)) + v (el 't');
// Z = [a, b, u, v]. Begleiter: Mittellinie bzw. Pole, Marken, Einheitskreis mit Läufer.
function bewegeTrig(T, Z, t, px, py, x0, x1, y0, y1) {
  const [a, b, u, v] = Z, tg = T.el === 't';
  const f = x => { const w = b * (x - u);
    if (tg) { if (Math.abs(Math.cos(w)) < 1e-4) return null; return a * Math.tan(w) + v; }
    return a * Math.sin(w) + v; };
  const kk = T.L.querySelector('.bew-kk[data-zu="' + T.p.dataset.paar + '"]');
  let th = null;
  if (kk) { const bahn = kk._bahn || (kk._bahn = JSON.parse(kk.dataset.bahn)); th = bewZustand(bahn, t - T.t0, T.lin)[0]; }
  const kg_ = kGrenzen(T), vx = kg_[0];
  let bx = kg_[1];
  if (kk && kk.dataset.spur === '1') bx = Math.min(bx, th);
  const a0 = Math.max(x0, vx), a1 = Math.min(x1, bx), H = y1 - y0;
  let d = '', an = false, yl = null;
  for (let i = 0; i <= 900 && a1 > a0; i++) {
    const x = a0 + (a1 - a0) * i / 900, y = f(x);
    if (y === null || !isFinite(y) || y < y0 - H || y > y1 + H) { an = false; yl = null; continue; }
    // Am Pol springt der Tangens von oben nach unten: dort neu ansetzen, nicht verbinden.
    if (tg && yl !== null && Math.abs(y - yl) > H) an = false;
    d += (an ? 'L' : 'M') + px(x).toFixed(1) + ',' + py(y).toFixed(1); an = true; yl = y;
  }
  T.p.setAttribute('d', d);
  const innen = (x, y) => x >= x0 && x <= x1 && y >= y0 && y <= y1;
  const setze = (g, x, y) => { g.style.display = innen(x, y) ? '' : 'none';
    g.querySelectorAll('circle').forEach(k => { k.setAttribute('cx', px(x)); k.setAttribute('cy', py(y)); }); };
  const beschrifte = (g, x, y, text) => {
    const tx = g.querySelector(':scope > text'); if (!tx) return;
    const rechts = x > x1 - (x1 - x0) * 0.25;
    const ya = f(x - 1e-3), yb = f(x + 1e-3), steigt = ya !== null && yb !== null && yb > ya;
    const oben = y > v + 1e-9 || (Math.abs(y - v) < 1e-9 && !steigt);
    tx.setAttribute('x', px(x) + (rechts ? -18 : 18));
    tx.setAttribute('y', py(y) + (oben ? -22 : 44));
    tx.setAttribute('text-anchor', rechts ? 'end' : 'start');
    tx.textContent = text;
  };
  for (const g of T.L.querySelectorAll('[data-zu="' + T.p.dataset.paar + '"]')) {
    if (g.classList.contains('bew-ka')) {
      let pole = '';
      if (tg && Math.abs(b) > 1e-9) {
        const per = Math.PI / Math.abs(b), start = u + per / 2;
        for (let k = Math.ceil((x0 - start) / per); start + k * per <= x1; k++) {
          const xp = start + k * per;
          pole += 'M' + px(xp).toFixed(1) + ',' + py(y0) + 'L' + px(xp).toFixed(1) + ',' + py(y1);
        }
      }
      g.querySelector('.bew-ka-s').setAttribute('d', pole);
      g.querySelector('.bew-ka-w').setAttribute('d', !tg && Math.abs(v) > 1e-9 && v >= y0 && v <= y1
        ? 'M' + px(x0) + ',' + py(v) + 'L' + px(x1) + ',' + py(v) : '');
    } else if (g.classList.contains('bew-km')) {
      const x = kmX(g, T), y = f(x);
      if (y === null) { g.style.display = 'none'; continue; }
      setze(g, x, y); beschrifte(g, x, y, g.dataset.text.replace('{x}', bewZahl(x)).replace('{y}', bewZahl(y)));
    } else if (g.classList.contains('bew-kk')) {
      // Einheitskreis: Pixelradius aus der y-Teilung, Mittelpunkt (mx | 0).
      const r = Math.abs(py(1) - py(0)), cx = px(parseFloat(g.dataset.mx)), cy = py(0);
      const P = [cx + r * Math.cos(th), cy - r * Math.sin(th)];
      const k = g.querySelector('.kk-kreis'); k.setAttribute('cx', cx); k.setAttribute('cy', cy); k.setAttribute('r', r);
      const lin = (c, xa, ya, xb, yb) => { const l = g.querySelector(c);
        l.setAttribute('x1', xa); l.setAttribute('y1', ya); l.setAttribute('x2', xb); l.setAttribute('y2', yb); };
      // "projektion": false — nur der Kreis, ohne Strecke zur Kurve (Winkel zeigen).
      const yq = f(th), sichtbar = yq !== null && innen(th, yq) && g.dataset.proj !== '0';
      if (tg) {
        // Tangente x = 1 am Kreis; der Strahl durch P trifft sie in T = (1 | tan th).
        // Ueber den Fensterrand hinaus: die Strecke am Rand abschneiden (seit 07.10.2026), nicht
        // ausblenden — «waechst ueber alle Grenzen» soll man sehen. Die Projektion faellt dann weg.
        const ty0 = Math.tan(th), drin = ty0 >= y0 && ty0 <= y1, ty = Math.min(y1, Math.max(y0, ty0));
        const T_ = [cx + r, cy - r * ty], ok = Math.abs(Math.cos(th)) > 1e-4;
        lin('.kk-tang', cx + r, py(y0), cx + r, py(y1));
        // P links der y-Achse (2. und 3. Quadrant): der Strahl geht von P durch M zur Tangente,
        // sonst haengt P neben der Linie.
        const vonP = ok && Math.cos(th) < 0;
        // abgeschnitten: der Strahl endet am Fensterrand, auf seiner eigenen Richtung
        const R_ = drin ? T_ : [cx + r * ty / ty0, cy - r * ty];
        lin('.kk-radius', vonP ? P[0] : cx, vonP ? P[1] : cy, ok ? R_[0] : P[0], ok ? R_[1] : P[1]);
        lin('.kk-hoehe', cx + r, cy, ok ? T_[0] : cx + r, ok ? T_[1] : cy);
        lin('.kk-proj', ok ? T_[0] : 0, ok ? T_[1] : 0, ok && drin && sichtbar ? px(th) : (ok ? T_[0] : 0), ok ? T_[1] : 0);
        const q = g.querySelector('.kk-q'); q.style.display = ok && drin && sichtbar ? '' : 'none';
        q.setAttribute('cx', px(th)); q.setAttribute('cy', py(ty));
      } else if (g.dataset.art === 'cos') {
        // Cosinus: die waagrechte Koordinate von P als Strecke auf der Achse, ohne Projektion.
        lin('.kk-tang', 0, 0, 0, 0);
        lin('.kk-radius', cx, cy, P[0], P[1]);
        lin('.kk-hoehe', cx, cy, P[0], cy);
        lin('.kk-proj', P[0], P[1], P[0], cy);
        const q = g.querySelector('.kk-q'); q.style.display = sichtbar ? '' : 'none';
        q.setAttribute('cx', px(th)); q.setAttribute('cy', sichtbar ? py(yq) : 0);
      } else {
        lin('.kk-tang', 0, 0, 0, 0);
        lin('.kk-radius', cx, cy, P[0], P[1]);
        lin('.kk-hoehe', P[0], cy, P[0], P[1]);
        lin('.kk-proj', P[0], P[1], sichtbar ? px(th) : P[0], P[1]);
        const q = g.querySelector('.kk-q'); q.style.display = sichtbar ? '' : 'none';
        q.setAttribute('cx', px(th)); q.setAttribute('cy', sichtbar ? py(yq) : 0);
      }
      // Der Bogen vom Start (1 | 0) bis P — seine Länge ist der Winkel im Bogenmass.
      const gross = Math.abs(th) > Math.PI ? 1 : 0, dreh = th >= 0 ? 0 : 1;
      g.querySelector('.kk-bogen').setAttribute('d', Math.abs(th) < 1e-6 ? '' :
        Math.abs(th) >= 2 * Math.PI - 1e-6
          ? 'M' + (cx + r) + ',' + cy + 'A' + r + ',' + r + ' 0 1 0 ' + (cx - r) + ',' + cy + 'A' + r + ',' + r + ' 0 1 0 ' + (cx + r) + ',' + cy
          : 'M' + (cx + r) + ',' + cy + 'A' + r + ',' + r + ' 0 ' + gross + ' ' + dreh + ' ' + P[0].toFixed(1) + ',' + P[1].toFixed(1));
      const pp = g.querySelector('.kk-p'); pp.setAttribute('cx', P[0]); pp.setAttribute('cy', P[1]);
    }
  }
}
// Polynom in Linearfaktordarstellung y = a*(x-x1)*(x-x2)*…; Z = [a, x1, x2, …].
function bewegePolynom(T, Z, px, py, x0, x1, y0, y1) {
  const a = Z[0], r = Z.slice(1);
  const f = x => r.reduce((s, q) => s * (x - q), a);
  const [vx, bx] = kGrenzen(T);
  const a0 = Math.max(x0, vx), a1 = Math.min(x1, bx);
  let d = '', an = false;
  for (let i = 0; i <= 600; i++) {
    const x = a0 + (a1 - a0) * i / 600, y = f(x);
    if (y < y0 - (y1 - y0) || y > y1 + (y1 - y0)) { an = false; continue; }
    d += (an ? 'L' : 'M') + px(x).toFixed(1) + ',' + py(y).toFixed(1); an = true;
  }
  T.p.setAttribute('d', d);
  // Extrempunkte: Vorzeichenwechsel der Steigung, verfeinert durch Halbieren.
  const ex = [];
  const df = x => (f(x + 1e-5) - f(x - 1e-5)) / 2e-5;
  for (let i = 0; i < 800; i++) {
    let p = a0 + (a1 - a0) * i / 800, q = a0 + (a1 - a0) * (i + 1) / 800;
    const dp = df(p), dq = df(q);
    // Faellt ein Gitterpunkt genau auf die Extremstelle, ist dort df = 0 — darum
    // «bis einschliesslich null», sonst geht der Scheitel x = 3 von (x−1)(x−5) verloren.
    if ((dp > 0 && dq <= 0) || (dp < 0 && dq >= 0)) {
      const hoch = dp > 0;
      for (let k = 0; k < 40; k++) { const m = (p + q) / 2; if ((df(m) > 0) === (df(p) > 0)) p = m; else q = m; }
      ex.push([(p + q) / 2, hoch]);
    }
  }
  const innen = (x, y) => x >= x0 && x <= x1 && y >= y0 && y <= y1;
  const setze = (g, x, y) => { g.style.display = innen(x, y) ? '' : 'none';
    g.querySelectorAll('circle').forEach(c => { c.setAttribute('cx', px(x)); c.setAttribute('cy', py(y)); }); };
  const beschrifte = (g, x, y, text, unten) => {
    const tx = g.querySelector(':scope > text'); if (!tx) return;
    const rechts = x > x1 - (x1 - x0) * 0.3;
    tx.setAttribute('x', px(x) + (rechts ? -18 : 18));
    tx.setAttribute('y', py(y) + (unten ? 44 : -18));
    tx.setAttribute('text-anchor', rechts ? 'end' : 'start');
    tx.textContent = text;
  };
  for (const g of T.L.querySelectorAll('[data-zu="' + T.p.dataset.paar + '"]')) {
    if (g.classList.contains('bew-kn')) {
      const i = +g.dataset.i, x = r[i];
      // Zusammenfallende Nullstellen zeigen nur einen Punkt — den ersten.
      if (r.slice(0, i).some(q => Math.abs(q - x) < 0.05)) { g.style.display = 'none'; continue; }
      setze(g, x, 0);
      // Beschriftungen abwechselnd ueber und unter der x-Achse, nach der Lage von
      // links nach rechts — sonst laufen zwei nahe Nullstellen ineinander.
      const rang = [...new Set(r.map(q => Math.round(q * 20)))].sort((p, q) => p - q).indexOf(Math.round(x * 20));
      beschrifte(g, x, 0, '(' + bewZahl(x) + ' | 0)', rang % 2 === 1);
    } else if (g.classList.contains('bew-ke')) {
      const e = ex[+g.dataset.i];
      if (!e) { g.style.display = 'none'; continue; }
      const y = f(e[0]); setze(g, e[0], y);
      beschrifte(g, e[0], y, (e[1] ? 'H' : 'T') + '(' + bewZahl(e[0]) + ' | ' + bewZahl(y) + ')', !e[1]);
    } else if (g.classList.contains('bew-km')) {
      const x = kmX(g, T), y = f(x);
      setze(g, x, y);
      beschrifte(g, x, y, g.dataset.text.replace('{x}', bewZahl(x)).replace('{y}', bewZahl(y)), a < 0);
    }
  }
}
function bewegen(t) {
  for (const L of BEW) for (const T of L.teile) {
    const [x0, x1, y0, y1, b, h, rd] = T.f;
    const px = x => rd + (x - x0) / (x1 - x0) * (b - 2 * rd);
    const py = y => h - rd - (y - y0) / (y1 - y0) * (h - 2 * rd);
    if (T.art === 'g') { bewegeGerade(T, t, px, py, x0, x1, y0, y1); continue; }
    if (T.art === 'k') { bewegeKurve(T, t, px, py, x0, x1, y0, y1); continue; }
    if (T.art === 'f') { laufeFest(T, t, px, py, x0, x1, y0, y1); continue; }
    if (T.art === 'fp') { bewegeFormel(T, t, px, py, x0, x1, y0, y1); continue; }
    // Scheitelform [a, u, v] oder Normalform [a, b, c] (data-normal); f ist die Kurve,
    // u und v der Scheitel (bei a = 0 keiner: NaN).
    const Z = bewZustand(T.k, t - L.t0), normal = T.p.dataset.normal === '1';
    const a = Z[0];
    const f = normal ? (x => a * x * x + Z[1] * x + Z[2]) : (x => a * (x - Z[1]) * (x - Z[1]) + Z[2]);
    const u = normal ? (Math.abs(a) > 1e-9 ? -Z[1] / (2 * a) : NaN) : Z[1];
    const v = normal ? f(u) : Z[2];
    const xa = T.p.dataset.ab !== undefined ? Math.max(x0, parseFloat(T.p.dataset.ab)) : x0;
    const xb = T.p.dataset.bis !== undefined ? Math.min(x1, parseFloat(T.p.dataset.bis)) : x1;
    let d = '', zug = false;
    for (let i = 0; i <= 240; i++) {
      const x = xa + (xb - xa) * i / 240, y = f(x);
      if (y >= y0 && y <= y1) { d += (zug ? 'L' : 'M') + px(x).toFixed(1) + ',' + py(y).toFixed(1); zug = true; }
      else zug = false;
    }
    T.p.setAttribute('d', d);
    const innen = (x, y) => x >= x0 && x <= x1 && y >= y0 && y <= y1;
    const setze = (g, x, y) => { g.style.display = innen(x, y) ? '' : 'none';
      g.querySelectorAll('circle').forEach(c => { c.setAttribute('cx', px(x)); c.setAttribute('cy', py(y)); }); };
    const beschrifte = (g, x, y, text, unten) => {
      const tx = g.querySelector(':scope > text'); if (!tx) return;
      const rechts = x > x1 - (x1 - x0) * 0.3;
      tx.setAttribute('x', px(x) + (rechts ? -18 : 18));
      tx.setAttribute('y', py(y) + (unten ? 44 : -18));
      tx.setAttribute('text-anchor', rechts ? 'end' : 'start');
      tx.textContent = text;
    };
    const fuell = (vorlage, x, y) => vorlage.replace('{x}', bewZahl(x)).replace('{y}', bewZahl(y));
    for (const g of T.L.querySelectorAll('[data-zu="' + T.p.dataset.paar + '"]')) {
      if (g.classList.contains('bew-a')) {
        g.style.display = isNaN(u) || u < x0 || u > x1 ? 'none' : '';
        g.querySelector('path').setAttribute('d', 'M' + px(u) + ',' + py(y0) + 'L' + px(u) + ',' + py(y1));
      } else if (g.classList.contains('bew-s')) {
        if (isNaN(u)) { g.style.display = 'none'; continue; }
        setze(g, u, v); beschrifte(g, u, v, 'S(' + bewZahl(u) + ' | ' + bewZahl(v) + ')', a > 0);
      } else if (g.classList.contains('bew-n')) {
        let xn;
        if (isNaN(u)) {
          // a = 0 (nur Normalform): eine Gerade b x + c, hoechstens eine Nullstelle (als n1)
          if (g.classList.contains('bew-n2') || Math.abs(Z[1]) < 1e-9) { g.style.display = 'none'; continue; }
          xn = -Z[2] / Z[1];
        } else {
          const q = a !== 0 ? -v / a : -1, w = q >= 0 ? Math.sqrt(q) : NaN;
          if (isNaN(w)) { g.style.display = 'none'; continue; }
          xn = g.classList.contains('bew-n1') ? u - w : u + w;
        }
        setze(g, xn, 0);
        if (g.querySelector(':scope > text')) {
          const tx = g.querySelector(':scope > text'), links = g.classList.contains('bew-n1') && !isNaN(u) && Math.abs(xn - u) > 1e-9;
          tx.setAttribute('x', px(xn) + (links ? -16 : 16)); tx.setAttribute('y', py(0) + (a > 0 ? -18 : 44));
          tx.setAttribute('text-anchor', links ? 'end' : 'start'); tx.textContent = '(' + bewZahl(xn) + ' | 0)';
        }
      } else if (g.classList.contains('bew-y')) {
        setze(g, 0, f(0)); beschrifte(g, 0, f(0), '(0 | ' + bewZahl(f(0)) + ')', false);
      } else if (g.classList.contains('bew-m')) {
        const x = parseFloat(g.dataset.x);
        setze(g, x, f(x)); beschrifte(g, x, f(x), fuell(g.dataset.text, x, f(x)), false);
      } else if (g.classList.contains('bew-l')) {
        const bahn = g._bahn || (g._bahn = JSON.parse(g.dataset.bahn).map(b => [b[0], b[1], 0, 0]));
        const x = bewZustand(bahn, t - L.t0)[0], y = f(x);
        setze(g.querySelector('.bew-pt'), x, y);
        g.style.display = innen(x, y) ? '' : 'none';
        const gs = g.querySelector('.bew-geist');
        if (gs) { const xs = 2 * u - x; gs.style.display = !isNaN(u) && Math.abs(xs - x) > 0.05 && innen(xs, f(xs)) ? '' : 'none';
          gs.querySelectorAll('circle').forEach(c => { c.setAttribute('cx', px(xs)); c.setAttribute('cy', py(f(xs))); }); }
        beschrifte(g, x, y, fuell(g.dataset.text, x, y), a > 0 && Math.abs(x - u) < (x1 - x0) * 0.15);
      }
    }
  }
}
const seekOhneBewegung = seek;
seek = function (t) { seekOhneBewegung(t); bewegen(t); beschriftungenRichten(); };
'''


# Zusaetze zum Abspieler (08.10.2026). Jeder kommt nur in Clips, die sein Feld benutzen (bauen()),
# und haengt sich wie BEWEGUNG_JS an seek — so bleibt BEWEGUNG_JS selbst und mit ihm jeder
# bestehende Clip unveraendert.

# "grad": true an einer Sinus-/Tangenskurve: Der Bauer liefert alle x-Werte im Bogenmass, das Fenster
# ist in Grad. bewegeTrig rechnet also wie immer, nur die Abbildung aufs Fenster wird umgerechnet; {x}
# in Marken und Laeufern wird danach in Grad geschrieben.
GRAD_JS = r'''
const bewegeTrigBogen = bewegeTrig;
bewegeTrig = function (T, Z, t, px, py, x0, x1, y0, y1) {
  if (T.p.dataset.grad !== '1') return bewegeTrigBogen(T, Z, t, px, py, x0, x1, y0, y1);
  const G = 180 / Math.PI;
  bewegeTrigBogen(T, Z, t, X => px(X * G), py, x0 / G, x1 / G, y0, y1);
  const [a, b, u, v] = Z, tg = T.el === 't';
  for (const g of T.L.querySelectorAll('.bew-km[data-zu="' + T.p.dataset.paar + '"]')) {
    const tx = g.querySelector(':scope > text');
    if (!tx || g.style.display === 'none' || !g.dataset.text.includes('{x}')) continue;
    const x = kmX(g, T), w = b * (x - u), y = a * (tg ? Math.tan(w) : Math.sin(w)) + v;
    tx.textContent = g.dataset.text.replace('{x}', bewZahl(x * G)).replace('{y}', bewZahl(y));
  }
};
'''

# "kreis": {"name": "P"}: der Name am laufenden Punkt P, radial nach aussen (data-abstand px).
KREISNAME_JS = r'''
function kreisNamen() {
  for (const n of document.querySelectorAll('.bew-kk > .kk-name')) {
    const g = n.parentNode, k = g.querySelector('.kk-kreis'), p = g.querySelector('.kk-p');
    const cx = +k.getAttribute('cx'), cy = +k.getAttribute('cy'), X = +p.getAttribute('cx'), Y = +p.getAttribute('cy');
    const d = Math.hypot(X - cx, Y - cy) || 1, a = parseFloat(n.dataset.abstand);
    n.setAttribute('x', (X + (X - cx) / d * a).toFixed(1));
    n.setAttribute('y', (Y + (Y - cy) / d * a + 12).toFixed(1));
  }
}
const seekOhneKreisname = seek;
seek = function (t) { seekOhneKreisname(t); kreisNamen(); };
'''

# "farbwechsel": [[t, farbe], …]: die Linie schaltet zu den (vom Bauer umgerechneten) Zeiten die Farbe.
FARBWECHSEL_JS = r'''
const FARBWECHSEL = [...document.querySelectorAll('[data-farben]')].map(p => ({ p, f0: p.getAttribute('stroke'),
  w: p.dataset.farben.split(';').map(s => s.split(',')).map(([t, f]) => [parseFloat(t), f]) }));
const seekOhneFarbwechsel = seek;
seek = function (t) {
  seekOhneFarbwechsel(t);
  for (const F of FARBWECHSEL) { let f = F.f0; for (const [ta, fa] of F.w) if (t >= ta) f = fa; F.p.setAttribute('stroke', f); }
};
'''

# "ausweichen": true am graf: Beschriftungen von Punkten weichen einander aus. Erst die festen (class pb),
# dann die mitfahrenden; jede bleibt, wo sie steht, solange sie frei ist. Sonst die erste freie von acht
# Lagen um ihren Punkt (rechts oben, links oben, rechts unten, links unten, oben, unten, rechts, links);
# ist keine frei, bleibt sie. Hindernisse: schon gesetzte Beschriftungen und alle Punkte.
AUSWEICHEN_JS = r'''
function ausweichen() {
  for (const svg of document.querySelectorAll('svg[data-ausweichen="1"]')) {
    const L = svg.closest('.l');
    if (!L || L.style.opacity === '0' || L.style.opacity === '') continue;
    const sichtbar = el => { for (let e = el; e && e !== svg; e = e.parentNode)
      if (e.style && (e.style.display === 'none' || e.style.opacity === '0')) return false; return true; };
    const marken = [];
    for (const tx of svg.querySelectorAll('text.pb')) {
      // feste Beschriftung: jedes Mal von ihrer berechneten Lage aus
      if (!tx._lage) tx._lage = [tx.getAttribute('x'), tx.getAttribute('y'), tx.getAttribute('text-anchor')];
      tx.setAttribute('x', tx._lage[0]); tx.setAttribute('y', tx._lage[1]); tx.setAttribute('text-anchor', tx._lage[2]);
      const [X, Y] = tx.dataset.pt.split(',').map(Number);
      if (sichtbar(tx)) marken.push([tx, X, Y]);
    }
    for (const g of svg.querySelectorAll('[data-zu], .fk-l')) {
      const tx = g.querySelector(':scope > text'), c = g.querySelector('.bew-pt circle');
      if (tx && c && tx.textContent && sichtbar(tx)) marken.push([tx, +c.getAttribute('cx'), +c.getAttribute('cy')]);
    }
    const B = svg.viewBox.baseVal.width, H = svg.viewBox.baseVal.height;
    const punkte = marken.map(([, X, Y]) => [X - 13, Y - 13, X + 13, Y + 13]);
    const gesetzt = [];
    const frei = (r, i) => r[0] >= 2 && r[1] >= 2 && r[2] <= B - 2 && r[3] <= H - 2
      && !gesetzt.some(q => r[0] < q[2] && q[0] < r[2] && r[1] < q[3] && q[1] < r[3])
      && !punkte.some((q, j) => j !== i && r[0] < q[2] && q[0] < r[2] && r[1] < q[3] && q[1] < r[3]);
    marken.forEach(([tx, X, Y], i) => {
      let bb; try { bb = tx.getBBox(); } catch (e) { return; }
      if (!bb.width) return;
      const r = [bb.x, bb.y, bb.x + bb.width, bb.y + bb.height];
      if (frei(r, i)) { gesetzt.push(r); return; }
      const w = bb.width, h = bb.height, grund = parseFloat(tx.getAttribute('y')) - bb.y;   // Oberkante bis Grundlinie
      const lagen = [[X + 16, Y - 16 - h], [X - 16 - w, Y - 16 - h], [X + 16, Y + 16], [X - 16 - w, Y + 16],
                     [X - w / 2, Y - 20 - h], [X - w / 2, Y + 20], [X + 18, Y - h / 2], [X - 18 - w, Y - h / 2]];
      for (const [l, o] of lagen) {
        const q = [l, o, l + w, o + h];
        if (!frei(q, i)) continue;
        tx.setAttribute('text-anchor', 'start'); tx.setAttribute('x', l.toFixed(1)); tx.setAttribute('y', (o + grund).toFixed(1));
        gesetzt.push(q); return;
      }
      gesetzt.push(r);
    });
  }
}
const seekOhneAusweichen = seek;
seek = function (t) { seekOhneAusweichen(t); ausweichen(); };
'''


# Abspieler-Zusatz fuer "fragen" (Prototyp 02.10.2026): Der Clip haelt an,
# stellt eine Frage (Knoepfe oder Tippen ins Bild), gibt Rueckmeldung und
# laeuft auf «Weiter» weiter. Nur in Clips mit "fragen", nie im Pruefmodus
# (?render). Gespult wird an Fragen vorbei, ohne anzuhalten.
FRAGEN_JS = r'''
(() => {
  if (location.search.includes('render')) return;
  const pp = document.getElementById('pp');
  const css = document.createElement('style');
  css.textContent = `
    #frage{position:absolute;left:110px;top:560px;width:820px;z-index:50;display:none;
      background:rgba(255,255,255,.97);border:3px solid var(--f2);border-radius:22px;
      padding:28px 34px;box-shadow:0 10px 40px rgba(0,0,0,.18);font-family:inherit;color:inherit}
    #frage .fr-kopf{font-size:26px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--f2);margin-bottom:10px}
    #frage .fr-text{font-size:38px;line-height:1.3;margin-bottom:22px}
    #frage .fr-knoepfe{display:flex;flex-wrap:wrap;gap:14px}
    #frage button{font:inherit;font-size:32px;padding:10px 26px;border-radius:999px;cursor:pointer;
      border:2.5px solid var(--f2);background:var(--f2w);color:inherit}
    #frage button.ok{border-color:var(--f3);background:var(--f3w)}
    #frage button.nein{border-color:var(--f4);background:var(--f4w)}
    #frage .fr-rueck{font-size:32px;line-height:1.35;margin-top:20px}
    #frage .fr-weiter{margin-top:20px}
    #frage .fr-eingabe{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;font-size:30px;margin-top:14px;width:100%}
    #frage .fr-eingabe input{font:inherit;font-size:30px;width:4.2em;padding:4px 10px;border:2.5px solid var(--f2);border-radius:12px}
    .fr-tippbar, .fr-tippbar svg{pointer-events:auto !important;cursor:crosshair}`;
  document.head.appendChild(css);
  const box = document.createElement('div'); box.id = 'frage'; stage.appendChild(box);
  let letzt = 0, offen = null, tippen = null, stimme = null, sprung = false;
  // Vorlesen mit derselben Stimme wie der Clip — nur wenn dessen Ton an ist.
  const hauptton = document.getElementById('ton');
  const vorlesen = src => {
    if (stimme) { stimme.pause(); stimme = null; }
    if (!src || !hauptton || hauptton.muted) return;
    stimme = new Audio(src); stimme.play().catch(() => {});
  };
  const erledigt = new Set();     // beantwortete Fragen
  const pause = () => { if (pp.textContent === 'Pause') pp.click(); };
  const weiter = () => { if (pp.textContent === 'Play') pp.click(); };
  function schliessen() {
    vorlesen(null);
    // Fokus zurueck auf Play/Pause — auch wenn er mit dem gesperrten Antwortknopf
    // schon auf <body> gefallen ist
    const fo = document.activeElement;
    if (!fo || fo === document.body || box.contains(fo)) pp.focus({ preventScroll: true });
    box.style.display = 'none'; box.innerHTML = '';
    document.querySelectorAll('.fr-marke').forEach(m => m.remove());
    document.querySelectorAll('.fr-tippbar').forEach(l => l.classList.remove('fr-tippbar'));
    if (tippen) { stage.removeEventListener('click', tippen); tippen = null; }
    offen = null;
  }
  function antwort(F, ok, text, schl) {
    const o = offen; erledigt.add(o.i);
    box.dataset.fertig = '1';
    vorlesen((F.ton || {})[schl]);
    if (F.typ === 'klick') box.querySelector('.fr-knoepfe').innerHTML = '';
    const r = box.querySelector('.fr-rueck');
    r.innerHTML = (ok ? '✓ ' : '') + text;
    r.style.color = ok ? 'var(--f3)' : '';
    if (ok) {                      // richtig: kurz bestaetigen, dann von selbst weiter
      setTimeout(() => { if (offen === o) { schliessen(); weiter(); } }, 1300);
      return;
    }
    const w = document.createElement('button'); w.className = 'fr-weiter'; w.textContent = 'Weiter ▶';
    w.onclick = () => { schliessen(); weiter(); };
    box.appendChild(w); w.focus();
  }
  function zeigen(i, F) {
    offen = { i, t: F.t }; pause(); delete box.dataset.fertig;
    box.innerHTML = '<div class="fr-kopf"></div><div class="fr-text"></div>'
      + '<div class="fr-knoepfe"></div><div class="fr-rueck"></div>';
    box.querySelector('.fr-kopf').textContent = F.kopf || 'Deine Vorhersage';  // "kopf": z. B. «Dein Vorgehen»
    box.querySelector('.fr-text').textContent = F.text;
    const kn = box.querySelector('.fr-knoepfe');
    if (F.typ === 'wahl') {
      F.optionen.forEach((o, j) => {
        const b = document.createElement('button'); b.textContent = o;
        b.onclick = () => {
          kn.querySelectorAll('button').forEach(x => x.disabled = true);
          b.classList.add(j === F.richtig ? 'ok' : 'nein');
          antwort(F, j === F.richtig, (F.rueck || {})[j] || (j === F.richtig ? 'Richtig.' : 'Schau, was der Clip zeigt.'), 'r' + j);
        };
        kn.appendChild(b);
      });
    } else if (F.typ === 'klick') {
      const L = [...document.querySelectorAll('.l')].find(l => +l.style.opacity > 0.5 && l.querySelector('[data-fenster]'));
      if (!L) { schliessen(); weiter(); return; }
      const svg = L.querySelector('svg'), fe = L.querySelector('[data-fenster]').dataset.fenster.split(',').map(Number);
      const [x0, x1, y0, y1, b, h, rd] = fe;
      L.classList.add('fr-tippbar');
      // Toleranz: eine Zahl (Abstand in Dateneinheiten) oder [dx, dy] je Achse —
      // Letzteres, wenn die Achsen verschiedene Grössen tragen (s und C).
      const tol = F.toleranz || 0.5;
      // Ziel und Fallen sind ein Punkt [x, y] oder eine Strecke [[x1, y1], [x2, y2]] (seit 08.10.2026):
      // Bei einer Strecke zaehlt ihr naechster Punkt — gerechnet in Toleranz-Einheiten, wenn die Achsen
      // verschiedene Toleranzen tragen.
      const tx_ = Array.isArray(tol) ? tol[0] : 1, ty_ = Array.isArray(tol) ? tol[1] : 1;
      const fuss = (x, y, z) => {
        if (!Array.isArray(z[0])) return z;
        const [[ax, ay], [bx, by]] = z, dx = (bx - ax) / tx_, dy = (by - ay) / ty_, l2 = dx * dx + dy * dy;
        const q = l2 ? Math.max(0, Math.min(1, ((x - ax) / tx_ * dx + (y - ay) / ty_ * dy) / l2)) : 0;
        return [ax + (bx - ax) * q, ay + (by - ay) * q];
      };
      const nah = (x, y, z) => { z = fuss(x, y, z);
        return Array.isArray(tol) ? Math.abs(x - z[0]) <= tol[0] && Math.abs(y - z[1]) <= tol[1]
                                  : Math.hypot(x - z[0], y - z[1]) <= tol; };
      // Wie weit weg, in Toleranzen — liegt ein Tipp in zwei Fallen, gewinnt die naechste (seit 08.10.2026)
      const weit = (x, y, z) => { z = fuss(x, y, z);
        return Array.isArray(tol) ? Math.max(Math.abs(x - z[0]) / tol[0], Math.abs(y - z[1]) / tol[1])
                                  : Math.hypot(x - z[0], y - z[1]) / tol; };
      const px = (x, y) => [rd + (x - x0) / (x1 - x0) * (b - 2 * rd), h - rd - (y - y0) / (y1 - y0) * (h - 2 * rd)];
      const mk = (cx, cy, farbe) => { const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        c.setAttribute('cx', cx); c.setAttribute('cy', cy); c.setAttribute('r', 16); c.setAttribute('class', 'fr-marke');
        c.setAttribute('fill', 'none'); c.setAttribute('stroke', farbe); c.setAttribute('stroke-width', 6); svg.appendChild(c); };
      const pruefePunkt = (x, y) => {
        mk(...px(x, y), 'var(--f2)');
        if (nah(x, y, F.ziel)) return antwort(F, true, F.richtig_text || 'Getroffen.', 'ok');
        if (Array.isArray(F.ziel[0])) {        // Strecke als Ziel: grün nachgezogen
          const [a, e] = [px(...F.ziel[0]), px(...F.ziel[1])], l = document.createElementNS('http://www.w3.org/2000/svg', 'line');
          l.setAttribute('x1', a[0]); l.setAttribute('y1', a[1]); l.setAttribute('x2', e[0]); l.setAttribute('y2', e[1]);
          l.setAttribute('class', 'fr-marke'); l.setAttribute('stroke', 'var(--f3)'); l.setAttribute('stroke-width', 14);
          l.setAttribute('stroke-linecap', 'round'); l.setAttribute('stroke-opacity', '.6'); svg.appendChild(l);
        } else mk(...px(F.ziel[0], F.ziel[1]), 'var(--f3)');
        let fk = -1;
        (F.fallen || []).forEach((f, k) => { if (nah(x, y, f.bei) && (fk < 0 || weit(x, y, f.bei) < weit(x, y, F.fallen[fk].bei))) fk = k; });
        antwort(F, false, fk >= 0 ? F.fallen[fk].text : (F.falsch_text || 'Nicht ganz — der grüne Kreis zeigt die Stelle.'),
                fk >= 0 ? 'fall' + fk : 'falsch');
      };
      // Am Stage horchen, nicht am Layer: unsichtbare spaetere Layer (Deckkraft 0)
      // liegen obenauf und wuerden den Tipp abfangen.
      tippen = ev => {
        if (!offen || box.dataset.fertig || box.contains(ev.target)) return;
        const r = svg.getBoundingClientRect();
        if (ev.clientX < r.left || ev.clientX > r.right || ev.clientY < r.top || ev.clientY > r.bottom) return;
        const sx = (ev.clientX - r.left) / r.width * b, sy = (ev.clientY - r.top) / r.height * h;
        pruefePunkt(x0 + (sx - rd) / (b - 2 * rd) * (x1 - x0), y0 + (h - rd - sy) / (h - 2 * rd) * (y1 - y0));
      };
      stage.addEventListener('click', tippen);
      kn.innerHTML = '<span style="font-size:30px;color:var(--f2)">👉 Tipp ins Bild rechts.</span>';
      // Ohne Zeigegeraet: dieselbe Antwort als zwei Zahlen ("eingabe": [Name x, Name y])
      if (F.eingabe) {
        const f = document.createElement('form'); f.className = 'fr-eingabe';
        f.innerHTML = '<span>oder eingeben:</span>' + F.eingabe.map((n, k) =>
          '<label>' + n + ' <input inputmode="decimal" autocomplete="off" data-k="' + k + '"></label>').join('')
          + '<button type="submit">Prüfen</button>';
        f.onsubmit = ev => {
          ev.preventDefault();
          if (box.dataset.fertig) return;
          const w = [...f.querySelectorAll('input')].map(i => parseFloat(i.value.replace(',', '.')));
          if (w.some(isNaN)) { f.querySelector('input').focus(); return; }
          pruefePunkt(w[0], w[1]);
        };
        kn.appendChild(f);
      }
    }
    box.style.display = 'block';
    // Fokus auf die erste Antwort: Tab, Enter und Leertaste reichen dann
    const erst = box.querySelector('.fr-knoepfe button, .fr-eingabe input');
    if (erst) erst.focus({ preventScroll: true });
    vorlesen((F.ton || {}).frage);
  }
  // Spulen wird ausdruecklich erkannt: Pfeiltasten und ein Klick auf die
  // Zeitleiste setzen ein Zeichen, das das naechste Bild auswertet. Ein
  // spaetes Bild (langsames Laden, Hintergrund-Tab) ist kein Spulen.
  // Neustart (R) und ein Sprung vor die erste Frage stellen alle Fragen neu;
  // nach R laeuft der Clip ab 0 wie beim ersten Abspielen.
  document.addEventListener('keydown', e => {
    if (e.target && e.target.closest && e.target.closest('input, select, textarea')) return;
    if ((e.key || '').toLowerCase() === 'r') { schliessen(); erledigt.clear(); letzt = 0; }
    if (e.code === 'ArrowLeft' || e.code === 'ArrowRight') sprung = true;
  });
  const bar = document.getElementById('bar');
  bar.addEventListener('click', () => { sprung = true; });
  // Die Abspielzeit ist im Abspieler lokal; zurueckgestellt wird sie ueber
  // dessen Zeitleiste.
  const zurueck = s => {
    const r = bar.getBoundingClientRect();
    if (r.width > 0 && bar.onclick) bar.onclick({ currentTarget: bar, clientX: r.left + s / DUR * r.width });
  };
  const vorFragen = seek;
  seek = function (t) {
    vorFragen(t);
    if (sprung) {
      // gespult: eine uebersprungene Frage wird nicht gestellt, eine
      // beantwortete kommt nicht wieder — ausser zurueck an den Anfang
      sprung = false;
      if (FRAGEN.length && t < Math.min(...FRAGEN.map(F => F.t))) { schliessen(); erledigt.clear(); }
    } else if (!offen && pp.textContent === 'Pause') {
      // gewoehnliches Abspielen, auch wenn ein Bild weit springt: die erste
      // ueberschrittene Frage wird gestellt, der Clip geht an ihre Stelle zurueck
      let i = -1;
      FRAGEN.forEach((F, j) => {
        if (!erledigt.has(j) && letzt < F.t && t >= F.t && (i < 0 || F.t < FRAGEN[i].t)) i = j;
      });
      if (i >= 0) {
        zeigen(i, FRAGEN[i]);
        if (offen && t - offen.t > 0.1) { t = offen.t; zurueck(t); vorFragen(t); }
      }
    }
    if (offen && Math.abs(t - offen.t) > 1.0) schliessen();
    letzt = t;
  };
})();
'''


def fragen_texte(F):
    """Alle Texte einer Frage, die vorgelesen werden: Liste (schluessel,
    angezeigt, gesprochen). Der gesprochene Wortlaut steht in den *_sprich-
    Feldern (wie «x minus zwei» statt «x − 2»); fehlt er, wird der angezeigte
    Text gelesen. Dieselbe Liste benutzt build-clip-fragen-ton.py — so passen
    Tondateien und Abspieler immer zusammen."""
    t = [("frage", F["text"], F.get("sprich", F["text"]))]
    # Richtige Antworten werden nicht vorgelesen: Der Clip zeigt kurz ✓ und
    # rollt weiter (Entscheid 02.10.2026) — eine Ansage liefe in den Sprecher.
    if F.get("typ") == "wahl":
        rs = F.get("rueck_sprich", {})
        for j in range(len(F.get("optionen", []))):
            if j == F.get("richtig"):
                continue
            if str(j) in F.get("rueck", {}):
                t.append(("r%d" % j, F["rueck"][str(j)], rs.get(str(j), F["rueck"][str(j)])))
    else:
        for k, f in enumerate(F.get("fallen", [])):
            t.append(("fall%d" % k, f["text"], f.get("sprich", f["text"])))
        if F.get("falsch_text"):
            t.append(("falsch", F["falsch_text"], F.get("falsch_sprich", F["falsch_text"])))
    return t


def fragen_tondatei(dateiname, i, schluessel):
    return "%s-f%d-%s.mp3" % (dateiname, i, schluessel)


def element_html(el, theme):
    typ = el.get("typ", "text")
    stil = []
    klassen = ["l"]

    if typ == "titel":
        klassen += ["hand", "mitte"]
        stil.append("font-size:%dpx;font-weight:600;color:var(--tinte)" % el.get("groesse", 132))
        inhalt = text_html(el["text"])
    elif typ == "untertitel":
        klassen += ["sans", "mitte"]
        stil.append("font-size:%dpx;color:var(--blau)" % el.get("groesse", 48))
        inhalt = text_html(el["text"])
    elif typ == "aussage":
        klassen += ["m", "mitte"]
        stil.append("font-size:%dpx;font-weight:600" % el.get("groesse", 116))
        inhalt = text_html(el["text"])
    elif typ == "formel":
        klassen += ["m", "row"]
        stil.append("font-size:%dpx" % el.get("groesse", 56))
        if el.get("fett"):
            stil.append("font-weight:600")
        inhalt = "<span>" + formel(el["text"]) + "</span>"
    elif typ == "text":
        klassen += ["m"]
        stil.append("font-size:%dpx" % el.get("groesse", 50))
        inhalt = text_html(el["text"])
    elif typ == "notiz":
        klassen += ["hand"]
        # Ein unbekannter Name ergab frueher still color:None, das der Browser wegwirft —
        # die Notiz stand dann schwarz statt farbig, ohne jede Meldung (03.10.2026).
        FARBEN = {"rot": "var(--rot)", "blau": "var(--blau)", "tinte": "var(--tinte)",
                  "gruen": "var(--gruen)", "gold": "var(--gold)", "orange": "var(--gold)"}
        name = el.get("farbe", "blau")
        if name not in FARBEN:
            raise SystemExit("[FEHLER] Notizfarbe «%s» gibt es nicht. Erlaubt: %s"
                             % (name, ", ".join(sorted(FARBEN))))
        farbe = FARBEN[name]
        stil.append("font-size:%dpx;color:%s" % (el.get("groesse", 50), farbe))
        inhalt = text_html(el["text"])
    elif typ == "karte":
        klassen += ["m", "huelle"]
        stil.append("font-size:%dpx" % el.get("groesse", 42))
        inhalt = '<span class="karte row"><span>' + formel(el["text"]) + "</span></span>"
    elif typ == "box":
        klassen += ["m", "huelle"]
        kl = "box row" + (" boxg" if el.get("farbe") == "gruen" else "")
        stil.append("font-size:%dpx;font-weight:600" % el.get("groesse", 58))
        inhalt = '<span class="%s"><span>%s</span></span>' % (kl, formel(el["text"]))
    elif typ == "liste":
        klassen += ["sans"]
        stil.append("font-size:%dpx" % el.get("groesse", 50))
        zeilen = []
        for i, z in enumerate(el["punkte"], 1):
            zeilen.append('<div class="lz"><span class="ln">%d</span>%s</div>'
                          % (i, text_html(z)))
        inhalt = "".join(zeilen)
    elif typ == "graf":
        klassen += ["graf"]
        inhalt = graf_svg(el, theme)
    elif typ == "boxplot":
        klassen += ["graf"]
        inhalt = boxplot_svg(el, theme)
    elif typ == "rechner":
        klassen += ["graf"]
        inhalt = rechner_svg(el, theme)
    elif typ == "bild":
        # Eine fertige SVG-Zeichnung aus clips/bilder/, eingegossen statt
        # verlinkt: Der Clip bleibt eine Datei. Gedacht fuer Skizzen, die eine
        # Animation der Lektionsseite wiederholen — der Clip zeigt dann
        # dasselbe Bild, das die Lernenden eben selbst bedient haben.
        klassen += ["graf"]
        pfad = os.path.join(CLIPS, el["datei"])
        endung = os.path.splitext(pfad)[1].lower()
        if endung == ".svg":
            with open(pfad, encoding="utf-8") as f:
                inhalt = f.read().strip()
            if not inhalt.startswith("<svg"):
                raise SystemExit("bild: keine SVG-Datei: %s" % el["datei"])
        elif endung in (".jpg", ".jpeg", ".png"):
            # Aufnahme einer Animation (Canvas), als data:-URL eingegossen.
            # `breite` in Buehnenpixeln; die Hoehe folgt dem Seitenverhaeltnis.
            import base64
            typ_ = "image/png" if endung == ".png" else "image/jpeg"
            with open(pfad, "rb") as f:
                daten = base64.b64encode(f.read()).decode("ascii")
            inhalt = ('<img src="data:%s;base64,%s" alt="" style="width:%dpx;'
                      'display:block;border:2px solid rgba(0,0,0,.12);border-radius:10px">'
                      % (typ_, daten, el.get("breite", 1140)))
        else:
            raise SystemExit("bild: SVG, JPG oder PNG erwartet: %s" % el["datei"])
    elif typ == "strich":
        klassen += ["strich"]
        stil.append("width:%dpx" % el.get("breite", 760))
        inhalt = ""
    else:
        raise SystemExit("Unbekannter Elementtyp: %s" % typ)

    return klassen, stil, inhalt


# ---------------------------------------------------------------- Zeitplanung
def szenen_planen(dreh):
    takt = dreh.get("takt", STD["takt"])
    nachlauf = dreh.get("nachlauf", STD["nachlauf"])
    tempo = dreh.get("sprechtempo", STD["sprechtempo"])
    t = 0.0
    plan = []
    for si, sz in enumerate(dreh["szenen"]):
        start = t
        letzte = 0.0
        eintritte = []
        for i, el in enumerate(sz.get("elemente", [])):
            ein = el.get("ein", STD["vorlauf"] + i * takt)
            eintritte.append(ein)
            letzte = max(letzte, ein)
        dauer = sz.get("dauer")
        if dauer is None:
            dauer = letzte + nachlauf
            sprech = sz.get("sprecher")
            if sprech:
                noetig = len(sprech.split()) / tempo + 1.4
                dauer = max(dauer, noetig)
            dauer = max(dauer, 3.0)
        plan.append({"start": start, "dauer": dauer, "eintritte": eintritte, "sz": sz})
        t += dauer
    return plan, t


# ---------------------------------------------------------------- HTML
def schriften_einbetten():
    """Alle woff2 aus schriften/ als data:-URL in @font-face-Regeln giessen."""
    import base64
    css = open(os.path.join(WURZEL, "schriften.css"), encoding="utf-8").read()
    # Nur latin und nur die drei Familien, die ein Clip benutzt — sonst
    # schleppt die Datei Kyrillisch und JetBrains Mono mit.
    regeln = [r for r in re.findall(r"@font-face\{[^}]*\}", css)
              if "-latin-" in r and "latin-ext" not in r
              and ("Source Serif 4" in r or "Source Sans 3" in r or "Caveat" in r)
              and not ("Source Sans 3" in r and "italic" in r)]
    css = "\n".join(regeln)
    def ersetzen(m):
        pfad = os.path.join(WURZEL, m.group(1))
        roh = base64.b64encode(open(pfad, "rb").read()).decode()
        return "url(data:font/woff2;base64,%s)" % roh
    return re.sub(r"url\((schriften/[^)]+\.woff2)\)", ersetzen, css)


def bauen(quelle, eigenstaendig=False):
    dreh = json.load(open(quelle, encoding="utf-8"))
    global LATEX
    LATEX = bool(dreh.get("latex", True))
    theme_name = dreh.get("theme", STD["theme"])
    theme = json.load(open(os.path.join(CLIPS, "themes", theme_name + ".json"), encoding="utf-8"))
    if eigenstaendig:
        fonts_css = schriften_einbetten()
    else:
        fonts_css = '@import url("../schriften.css");' 

    plan, gesamt = szenen_planen(dreh)
    schiene = dreh.get("schiene", [])

    # Tonspur, falls scripts/build-clip-ton.py eine erzeugt hat. Der Clip
    # laeuft ohne genauso; der Ton ist eine Zutat, keine Voraussetzung.
    tonname = (dreh.get("dateiname") or
               os.path.splitext(os.path.basename(quelle))[0]) + ".mp3"
    tonpfad = os.path.join(CLIPS, "ton", tonname)
    if not os.path.exists(tonpfad):
        ton_html = ""
    elif eigenstaendig:
        import base64
        roh = base64.b64encode(open(tonpfad, "rb").read()).decode("ascii")
        ton_html = ('<audio id="ton" preload="auto" '
                    'src="data:audio/mpeg;base64,%s"></audio>' % roh)
    else:
        ton_html = ('<audio id="ton" preload="auto" src="ton/%s"></audio>'
                    % tonname)

    teile = []          # HTML-Schnipsel
    sprecher = []       # Sprechertexte mit Zeitpunkt

    # --- Kopf- und Fusszeile: immer sichtbar
    marke = dreh.get("marke", "begreifbar.ch")
    bereich = dreh.get("themenbereich", "")
    autor = dreh.get("autor", "Raphael Arnold Kohler")
    datum = dreh.get("datum") or date.today().strftime("%d.%m.%Y")
    if re.match(r"^\d{4}-\d{2}-\d{2}$", datum):
        j, m_, t_ = datum.split("-")
        datum = f"{t_}.{m_}.{j}"

    teile.append(
        f'<div id="kopf"><span class="marke">{entschaerfen(marke)}</span>'
        f'<span class="bereich">{entschaerfen(bereich)}</span></div>')
    teile.append(
        f'<div id="fuss"><span>{entschaerfen(autor)}</span>'
        f'<span>{entschaerfen(datum)}</span></div>')

    # --- Bedingungsleiste ------------------------------------------------
    # Was eine Rechnung voraussetzt, verschwindet sonst mit der Szene, in der
    # es genannt wurde — und drei Szenen spaeter rechnet der Clip auf einer
    # Bedingung weiter, die niemand mehr sieht. `halten` loest das nur halb:
    # ein gehaltenes Element behaelt die Position seiner Szene und blockiert
    # damit den Fluss aller folgenden. Die Leiste steht ausserhalb des
    # Flusses und kostet darum keine Zeile.
    #
    #   "voraussetzung": "a \\neq 0"
    #   "voraussetzung": {"text": "...", "ab": "Szenenname", "bis": "Szenenname"}
    #   "voraussetzung": [ {...}, {...} ]      mehrere nacheinander
    #
    vor = dreh.get("voraussetzung")
    if vor:
        if not isinstance(vor, list):
            vor = [vor]
        leiste = []
        for v in vor:
            if isinstance(v, str):
                v = {"text": v}
            def szene_zeit(name, feld):
                if name is None:
                    return None
                q = next((q for q in plan if q["sz"].get("name") == name), None)
                if q is None:
                    raise SystemExit("voraussetzung verweist auf unbekannte Szene: %s" % name)
                return q["start"] if feld == "start" else q["start"] + q["dauer"]
            ab = szene_zeit(v.get("ab"), "start")
            bis = szene_zeit(v.get("bis"), "ende")
            ein = (ab if ab is not None else 0.0) + v.get("verzug", 0.6)
            attr = f' data-at="{ein:.2f}"'
            if bis is not None:
                attr += f' data-out="{bis:.2f}"'
            attr += ' data-anim="fade"'
            tag = entschaerfen(v.get("tag", "Voraussetzung"))
            leiste.append(f'<div class="l vorzeile"{attr} style="position:relative">'
                          f'<span class="vor"><span class="vor-tag">{tag}</span>'
                          f'<span class="vor-txt">{formel(v["text"])}</span></span></div>')
        teile.append('<div id="vorleiste">' + "".join(leiste) + '</div>')

    # --- Schiene (Merkweg) wird einmal gebaut, Sichtbarkeit über die Szenen
    schienen_szenen = [p for p in plan if p["sz"].get("schritt")]
    if schiene and schienen_szenen:
        von = schienen_szenen[0]["start"]
        bis = schienen_szenen[-1]["start"] + schienen_szenen[-1]["dauer"]
        eintraege = []
        for i, s in enumerate(schiene, 1):
            # Zeitpunkt, ab dem dieser Schritt sichtbar ist
            erste = next((p for p in schienen_szenen if p["sz"]["schritt"] >= i), None)
            ein = erste["start"] + 0.3 if erste else von
            aktiv = [p for p in schienen_szenen if p["sz"].get("schritt") == i]
            dim = ""
            if aktiv:
                a0 = aktiv[0]["start"]
                a1 = aktiv[-1]["start"] + aktiv[-1]["dauer"]
                dim = f' data-dim="{a0:.2f},{a1:.2f}"'
            eintraege.append(
                f'<div class="step l flow" data-at="{ein:.2f}" data-anim="rise"{dim}>'
                f'<div class="num">{i}</div><div class="stxt">{text_html(s)}</div></div>')
        teile.append(
            f'<div class="l" data-at="{von:.2f}" data-out="{bis:.2f}" data-anim="fade" '
            f'style="left:130px;top:296px;width:470px">' + "".join(eintraege) + '</div>')

    # --- Szenen
    for pi, p in enumerate(plan):
        naechste = plan[pi + 1] if pi + 1 < len(plan) else None
        sz, start, dauer = p["sz"], p["start"], p["dauer"]
        layout = sz.get("layout", "zentriert")
        ende = start + dauer
        if sz.get("sprecher"):
            sprecher.append({"bei": round(start + sz.get("sprecher_bei", 0.4), 2),
                             "text": sz["sprecher"]})

        # Grundraster
        if layout == "schiene":
            links, breite, oben, abstand = 680, 1140, 168, 112
            mitte = False
        else:
            links, breite, oben, abstand = 130, 1660, 230, 118
            mitte = True

        y = sz.get("oben", oben)
        for i, el in enumerate(sz.get("elemente", [])):
            klassen, stil, inhalt = element_html(el, theme)
            ein = start + p["eintritte"][i]
            h = el.get("halten")
            if h is True:
                aus = None
            elif isinstance(h, str):
                ziel_sz = next((q for q in plan if q["sz"].get("name") == h), None)
                if ziel_sz is None:
                    raise SystemExit("halten verweist auf unbekannte Szene: %s" % h)
                aus = ziel_sz["start"] + ziel_sz["dauer"]
            else:
                aus = ende
            # "aus" am ganzen Element (seit 08.10.2026): Sekunden ab Szenenbeginn wie "ein" — das
            # Element blendet dann aus, auch mitten in der Szene; geht vor "halten".
            if el.get("aus") is not None:
                aus = start + el["aus"]
            anim = el.get("anim", "pop" if el.get("typ") in ("box", "aussage") else "rise")

            # Die Textbreite begrenzen. Ohne das laeuft eine lange Zeile bis an
            # den Buehnenrand und bricht dort unausgeglichen um — im
            # Schienen-Layout bis 1920 statt bis 1820, in der Mitte ueber die
            # volle Breite ohne Rand. `breite` war bisher totes Kapital.
            if mitte and "x" not in el:
                klassen.append("mitte")
                rand = (1920 - breite) // 2 if TEXTBREITE_BEGRENZEN else 0
                stil.insert(0, "left:%dpx;right:%dpx;text-align:center" % (rand, rand))
            else:
                stil.insert(0, "left:%dpx" % el.get("x", links))
                if (TEXTBREITE_BEGRENZEN and "breite" not in el
                        and el.get("typ") not in ("graf", "bild", "strich")):
                    stil.append("width:%dpx" % breite)
            stil.insert(1, "top:%dpx" % el.get("y", y))

            hoehe = el.get("hoehe", int(el.get("groesse", 50) * 1.5) + 40)
            y = el.get("y", y) + el.get("abstand", max(abstand, hoehe))

            attr = f' data-at="{ein:.2f}"'
            if el.get("typ") == "graf" and (any(pa.get("bewegung") for pa in el.get("parabeln", []))
                                            or any(ge.get("bewegung") for ge in el.get("geraden", []))
                                            or any(kv.get("bewegung") or kv.get("laeufer") or kv.get("parameter")
                                                   for kv in el.get("kurven", []))):
                attr += f' data-t0="{start:.2f}"'
            if aus is not None:
                attr += f' data-out="{aus:.2f}"'
            attr += f' data-anim="{anim}"'
            if "-rel=" in inhalt:
                inhalt = re.sub(r'data-(ein|aus|fvon|fbis)-rel="([-\d.e]+)"',
                                lambda m: 'data-%s="%.2f"' % (m.group(1), start + float(m.group(2))), inhalt)
                inhalt = re.sub(r'data-farben-rel="([^"]*)"', lambda m: 'data-farben="%s"' % ";".join(
                    "%.2f,%s" % (start + float(w.split(",")[0]), w.split(",")[1]) for w in m.group(1).split(";")), inhalt)
            teile.append(f'<div class="{" ".join(klassen)}"{attr} '
                         f'style="{";".join(stil)}">{inhalt}</div>')

            # --- Anschluss an den vorherigen Schritt ------------------------
            # `mitnehmen: true` zeigt dieses Element in der naechsten
            # Schritt-Szene noch einmal, oben im Band, das das Schienen-Layout
            # dafuer frei laesst (168 bis 430 px). Das ist nicht dasselbe wie
            # `halten`: Gehalten bleibt ein Element an seinem Platz stehen —
            # was nur beim ersten Schritt oben passt. Mitgenommen wird es an
            # den Kopf der naechsten Szene gesetzt, gleich wo es vorher stand.
            #
            # Wozu: Ohne das faellt beim Szenenwechsel die Formel weg, die der
            # naechste Schritt gerade einsetzt. Auf der Merkschiene links steht
            # dann zwar noch, *dass* es einen Schritt davor gab, aber nicht
            # mehr, *was* er ergeben hat — und das Ansatz-Prinzip (erst die
            # Formel, dann die Werte) ist im Bild nicht mehr zu sehen.
            if el.get("mitnehmen"):
                if naechste is None or naechste["sz"].get("layout") != "schiene":
                    print("  [WARN] mitnehmen ohne folgende Schritt-Szene: %s"
                          % sz.get("name"))
                else:
                    a_kl, a_stil, a_inhalt = element_html(el, theme)
                    a_kl.append("anschluss")
                    a_stil.insert(0, "left:680px;top:168px")
                    if "breite" not in el and el.get("typ") not in ("graf", "bild", "strich"):
                        a_stil.append("width:1140px")
                    a_ein = naechste["start"] + 0.25
                    a_aus = naechste["start"] + naechste["dauer"]
                    teile.append(
                        f'<div class="{" ".join(a_kl)}" data-at="{a_ein:.2f}" '
                        f'data-out="{a_aus:.2f}" data-anim="fade" '
                        f'style="{";".join(a_stil)}">{a_inhalt}</div>')

        # Die Bedingungsleiste sitzt bei top:96px und ist rund 54px hoch, sie
        # endet also bei y = 150. Wer sie benutzt, laesst die Szenen darunter
        # beginnen. Lieber hier abbrechen als es spaeter im Bild suchen.
        if dreh.get("voraussetzung") and sz.get("oben", oben) < 170:
            raise SystemExit(
                "Szene %r beginnt bei oben=%d und liefe in die Bedingungsleiste "
                "(sie endet bei y=150). Mit einer Voraussetzung beginnen die Szenen "
                "bei oben >= 170." % (sz.get("name", "?"), sz.get("oben", oben)))

    karo = ""
    if theme.get("karo"):
        k = theme.get("karo_farbe", "rgba(43,95,140,.12)")
        karo = ("background-image:repeating-linear-gradient(to right,%s 0 1.5px,transparent 1.5px 60px),"
                "repeating-linear-gradient(to bottom,%s 0 1.5px,transparent 1.5px 60px);" % (k, k))
    rand = ""
    if theme.get("rand"):
        rand = ('<div id="rand" style="background:%s"></div>'
                % theme.get("rand_farbe", "rgba(191,59,43,.26)"))

    fv = theme.get("farben", ["#1F6FB2", "#C2621C", "#2C7A58", "#8A4BA0"])
    fl = theme.get("flaechen", ["rgba(31,111,178,.12)", "rgba(194,98,28,.13)",
                                "rgba(44,122,88,.12)", "rgba(138,75,160,.12)"])
    didaktik = ";".join("--f%d:%s;--f%dw:%s" % (i + 1, fv[i], i + 1, fl[i])
                        for i in range(4))

    # Im LaTeX-Versuch setzt MathJax. Die vier Farbmakros bilden die
    # Farbgruppen der eigenen Schreibweise nach — gleiche Werte, damit der
    # Vergleich der beiden Fassungen einer ueber die Gestaltung ist und
    # nicht einer ueber die Palette.
    mathjax = ""
    if LATEX:
        # Das Doppelkreuz einer Farbe muss verdoppelt werden: In einer
        # Makrodefinition ist #1 der Parameter, und «#1a4f8a» liest TeX
        # als «Parameter 1, dann a4f8a» — Fehlermeldung statt Formel.
        makros = ",".join(
            "%s:['\\\\bbox[%s,3px]{\\\\textcolor{%s}{#1}}',1]"
            % (n, fl[i].replace("#", "##"), fv[i].replace("#", "##"))
            for i, n in enumerate(["fa", "fb", "fc", "fd"]))
        mathjax = (
            "<script>window.MathJax={tex:{inlineMath:[['\\\\(','\\\\)']],"
            "displayMath:[],macros:{%s}},svg:{fontCache:'global'},"
            "options:{enableMenu:false}};</script>"
            "<script src=\"../vendor/mathjax/tex-svg.js\"></script>" % makros)

    html = VORLAGE.format(
        mathjax=mathjax,
        didaktik=didaktik,
        titel=entschaerfen(dreh.get("titel", "Clip")),
        fonts=fonts_css,
        papier=theme["papier"], tinte=theme["tinte"], blau=theme["blau"],
        rot=theme["rot"], gruen=theme["gruen"], gold=theme.get("gold", "#E0A32E"),
        karte_bg=theme.get("karte", "rgba(255,255,255,.66)"),
        box_bg=theme.get("box", "rgba(255,255,255,.6)"),
        vignette=theme.get("vignette", "rgba(90,70,40,.10)"),
        karo=karo, rand=rand, ton=ton_html,
        dauer=round(gesamt, 2),
        inhalt="\n".join(teile),
        sprecher=json.dumps(sprecher, ensure_ascii=False),
    )

    # Nur Clips mit bewegten Bildern bekommen den Zusatz — alle anderen
    # bleiben Byte fuer Byte, wie sie waren.
    if "data-bew=" in html or "data-bewg=" in html or "data-bewk=" in html or "data-fkl=" in html \
            or "data-fp=" in html:
        html = html.replace("window.__seek = seek;", BEWEGUNG_JS + "window.__seek = seek;", 1)
    # Zusaetze vom 08.10.2026: nur in Clips, die das Feld benutzen — alle anderen bleiben Byte fuer Byte.
    for marke, js in (('data-grad="1"', GRAD_JS), ('class="kk-name"', KREISNAME_JS),
                      ('data-farben="', FARBWECHSEL_JS), ('data-ausweichen="1"', AUSWEICHEN_JS)):
        if marke in html:
            html = html.replace("window.__seek = seek;", js + "window.__seek = seek;", 1)
    if dreh.get("fragen"):
        fr = []
        for F in dreh["fragen"]:
            sz = next((q for q in plan if q["sz"].get("name") == F["szene"]), None)
            if sz is None:
                raise SystemExit("Frage verweist auf unbekannte Szene: %s" % F["szene"])
            G = {k: v for k, v in F.items() if not k.startswith("_") and k not in ("szene", "bei")
                 and not k.endswith("sprich")}
            for f_ in G.get("fallen", []):
                f_.pop("sprich", None)
            G["t"] = round(sz["start"] + F.get("bei", 0.3), 2)
            G["ton"] = {}
            for schl, _, _ in fragen_texte(F):
                datei = fragen_tondatei(dreh["dateiname"], len(fr), schl)
                if os.path.exists(os.path.join(CLIPS, "ton", datei)):
                    G["ton"][schl] = "ton/" + datei
            fr.append(G)
        html = html.replace("window.__seek = seek;", "const FRAGEN = " + json.dumps(fr, ensure_ascii=False)
                            + ";" + FRAGEN_JS + "window.__seek = seek;", 1)

    name = dreh.get("dateiname") or os.path.splitext(os.path.basename(quelle))[0]
    if eigenstaendig:
        name += "-eigenstaendig"
    ziel = os.path.join(CLIPS, name + ".html")
    open(ziel, "w", encoding="utf-8").write(html)

    print(f"{ziel}")
    print(f"  {len(plan)} Szenen, {gesamt:.1f} s, {len(sprecher)} Sprechertexte")
    for i, p in enumerate(plan, 1):
        print(f"  {i:2d}  {p['start']:6.1f}–{p['start']+p['dauer']:6.1f}s  "
              f"{p['sz'].get('name','')}")

    # Sprechertexte als Skript herausschreiben — Grundlage für die Vertonung
    if sprecher:
        with open(os.path.join(CLIPS, "sprechertext-" + name + ".txt"), "w",
                  encoding="utf-8") as f:
            for s in sprecher:
                f.write(f"{s['bei']:.2f}\t{s['text']}\n")

    return ziel, dreh, gesamt




VORLAGE = r"""<!DOCTYPE html>
<html lang="de-CH"><head><meta charset="utf-8"><title>{titel}</title><style>
{fonts}
:root{{--papier:{papier};--tinte:{tinte};--blau:{blau};--rot:{rot};--gruen:{gruen};--gold:{gold};{didaktik}}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:100%;height:100%;background:#0d1418;overflow:hidden}}
#wrap{{position:absolute;left:0;right:0;top:0;bottom:60px;overflow:hidden}}
:fullscreen #wrap{{bottom:0}} :fullscreen #ui{{display:none}}
#stage{{width:1920px;height:1080px;position:absolute;left:50%;top:50%;overflow:hidden;
 background:var(--papier);color:var(--tinte);font-family:'Source Serif 4',Georgia,serif;transform-origin:center center}}
body.render #wrap{{bottom:0}} body.render #stage{{left:0;top:0;transform:none!important}}
#stage::before{{content:"";position:absolute;inset:0;pointer-events:none;{karo}}}
#stage::after{{content:"";position:absolute;inset:0;pointer-events:none;
 background:radial-gradient(120% 100% at 50% 40%,rgba(255,255,255,0) 55%,{vignette} 100%)}}
#rand{{position:absolute;left:76px;top:0;bottom:0;width:3px}}

#kopf,#fuss{{position:absolute;left:130px;right:100px;display:flex;justify-content:space-between;
 align-items:baseline;font-family:'Source Sans 3',sans-serif;z-index:5}}
#kopf{{top:46px;font-size:27px}}
#kopf .marke{{font-weight:600;letter-spacing:.01em;color:var(--blau)}}
#kopf .bereich{{color:var(--tinte);opacity:.55;letter-spacing:.07em;text-transform:uppercase;font-size:22px}}
#fuss{{bottom:44px;font-size:21px;color:var(--tinte);opacity:.42}}

/* Bedingungsleiste: die Voraussetzung, auf der die Rechnung steht.
   Sie liegt ausserhalb des Szenenflusses — darum kostet sie keine Zeile
   und kann trotzdem stehen bleiben, solange sie gilt. Unterhalb des
   Inhalts, oberhalb der Fusszeile. */
#vorleiste{{position:absolute;left:130px;right:100px;top:96px;
 display:flex;justify-content:center;gap:14px;z-index:5;pointer-events:none}}
.vor{{display:inline-flex;align-items:center;gap:.58em;
 background:var(--f1w);border:1.5px solid var(--f1);border-radius:10px;
 padding:7px 19px 8px;color:var(--tinte);font-size:30px;line-height:1.14;
 box-shadow:0 1px 0 rgba(0,0,0,.03)}}
.vor .vor-tag{{font-family:'Source Sans 3',sans-serif;font-size:18px;font-weight:700;
 letter-spacing:.13em;text-transform:uppercase;color:var(--f1);opacity:.95;
 white-space:nowrap;align-self:center}}
.vor .vor-txt{{white-space:nowrap}}

.l{{position:absolute;will-change:opacity,transform}}
.l.flow{{position:relative}}
.m{{font-family:'Source Serif 4',Georgia,serif}} .m i,i{{font-style:italic}}
.hand{{font-family:'Caveat',cursive;line-height:1.24}}
.sans{{font-family:'Source Sans 3',system-ui,sans-serif}}
.huelle{{display:flex;justify-content:flex-start}}
.mitte.huelle{{justify-content:center}}
.huelle>span{{white-space:nowrap}}
.f1,.f2,.f3,.f4{{border-radius:7px;padding:0 .14em;margin:0 .02em}}
.f1{{color:var(--f1);background:var(--f1w)}}
.f2{{color:var(--f2);background:var(--f2w)}}
.f3{{color:var(--f3);background:var(--f3w)}}
.f4{{color:var(--f4);background:var(--f4w)}}
.dim{{opacity:.62}}
.graf{{line-height:0}}
.graf svg{{display:inline-block;vertical-align:top}}
.ov{{display:inline-block;line-height:1;padding-top:.07em;margin-top:.12em;border-top:3.5px solid currentColor}}
.row{{display:flex;align-items:center;line-height:1.06;white-space:nowrap;gap:.26em}}
.mitte.row{{justify-content:center}}
.fr{{position:relative;z-index:1;display:inline-flex;flex-direction:column;align-items:center;
 line-height:1.08;margin:0 .12em;vertical-align:middle}}
.fr>span:first-child{{padding:0 .32em .07em}}
.fr>span:last-child{{padding:.20em .32em 0;border-top:3.5px solid currentColor}}
.box{{border:3.5px solid var(--tinte);border-radius:14px;padding:12px 30px;background:{box_bg}}}
.boxg{{border-color:var(--gruen);color:var(--gruen)}}
.karte{{background:{karte_bg};border:2.5px solid rgba(128,128,128,.28);border-radius:16px;padding:14px 26px}}
.strich{{height:5px;background:var(--rot);border-radius:3px;transform-origin:left center}}
.lz{{display:flex;align-items:baseline;gap:22px;margin-bottom:26px}}
.ln{{color:var(--blau);font-weight:600;min-width:34px}}
.step{{display:flex;align-items:flex-start;gap:18px;margin-bottom:34px}}
.num{{flex:0 0 auto;width:56px;height:56px;border-radius:50%;background:var(--blau);color:var(--papier);
 font-family:'Source Sans 3',sans-serif;font-weight:600;font-size:31px;display:grid;place-items:center}}
.stxt{{font-family:'Source Sans 3',sans-serif;font-size:31px;line-height:1.24;padding-top:7px}}

#ui{{position:absolute;left:0;right:0;bottom:0;height:60px;display:flex;align-items:center;gap:18px;
 padding:0 26px;background:rgba(13,20,24,.85);color:#e8eef2;font-family:system-ui,sans-serif;font-size:14px;z-index:99}}
body.render #ui{{display:none}}
#bar{{flex:1;height:8px;background:rgba(255,255,255,.18);border-radius:4px;overflow:hidden;cursor:pointer}}
#barf{{height:100%;width:0;background:var(--gold)}}
#ui button{{background:rgba(255,255,255,.12);color:#e8eef2;border:0;border-radius:7px;padding:7px 14px;
 font-size:14px;cursor:pointer;white-space:nowrap}}
#tt{{white-space:nowrap;font-variant-numeric:tabular-nums}}
#tip{{opacity:.6;white-space:nowrap}}
/* Auf dem Telefon gibt es weder Leertaste noch Pfeiltasten — der Hinweis
   waere dort nur Text, der die 60px hohe Leiste sprengt. */
@media (max-width:700px){{#ui{{gap:11px;padding:0 12px}} #tip{{display:none}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
</style>{mathjax}</head><body>
<div id="wrap"><div id="stage">
{rand}
{inhalt}
</div></div>
{ton}
<div id="ui">
  <button id="pp">Pause</button>
  <button id="ts" hidden>🔇 Ton an</button>
  <div id="bar"><div id="barf"></div></div>
  <span id="tt">0.0 s</span>
  <span id="tip">Leertaste = Pause &middot; &larr; &rarr; = 5 s &middot; R = Neustart &middot; F = Vollbild</span>
</div>
<script>
const DUR = {dauer};
const SPRECHER = {sprecher};
const stage = document.getElementById('stage');
const layers = [...document.querySelectorAll('.l')].map(el => ({{
  el, at: parseFloat(el.dataset.at || '0'),
  out: el.dataset.out ? parseFloat(el.dataset.out) : Infinity,
  anim: el.dataset.anim || 'fade',
  dim: el.dataset.dim ? el.dataset.dim.split(',').map(Number) : null
}}));
const IN = 0.5, OUT = 0.4;
// Teile eines Bildes mit eigenem "ein"/"aus" (g.zt): blenden fuer sich ein und aus.
// Bewegte Figuren (g.fb): vorgerechnete Bilder, je eines zwischen data-fvon und data-fbis.
const fbilder = [...document.querySelectorAll('g.fb')].map(el => ({{
  el, von: el.dataset.fvon ? parseFloat(el.dataset.fvon) : -Infinity,
  bis: el.dataset.fbis ? parseFloat(el.dataset.fbis) : Infinity }}));
const zteile = [...document.querySelectorAll('g.zt')].map(el => ({{
  el, at: el.dataset.ein ? parseFloat(el.dataset.ein) : -Infinity,
  out: el.dataset.aus ? parseFloat(el.dataset.aus) : Infinity }}));
const ease = p => 1 - Math.pow(1 - p, 3);
const cl = p => p < 0 ? 0 : p > 1 ? 1 : p;
function seek(t)  {{
  for (const L of layers) {{
    const pi = ease(cl((t - L.at) / IN));
    const po = L.out === Infinity ? 0 : ease(cl((t - L.out) / OUT));
    let o = pi * (1 - po), tr = '';
    if (L.anim === 'rise') tr = 'translateY(' + ((1 - pi) * 26) + 'px)';
    else if (L.anim === 'pop') tr = 'scale(' + (0.90 + 0.10 * pi) + ')';
    else if (L.anim === 'wipe') {{ tr = 'scaleX(' + pi + ')'; o = (t >= L.at ? 1 : 0) * (1 - po); }}
    if (L.dim && !(t >= L.dim[0] && t < L.dim[1])) o *= 0.34;
    L.el.style.transform = tr; L.el.style.opacity = o;
  }}
  for (const Z of zteile) {{
    const pi = Z.at === -Infinity ? 1 : ease(cl((t - Z.at) / IN));
    const po = Z.out === Infinity ? 0 : ease(cl((t - Z.out) / OUT));
    Z.el.style.opacity = pi * (1 - po);
  }}
  for (const F of fbilder) F.el.style.display = t >= F.von && t < F.bis ? '' : 'none';
}}
window.__seek = seek;
window.__dauer = DUR;
if (!location.search.includes('render')) {{
  let t0 = performance.now(), playing = true, t = 0;
  const barf = document.getElementById('barf'), tt = document.getElementById('tt'),
        pp = document.getElementById('pp'), wrap = document.getElementById('wrap');
  const fit = () => {{ stage.style.transform = 'translate(-50%,-50%) scale('
      + Math.min(wrap.clientWidth / 1920, wrap.clientHeight / 1080) + ')'; }};
  window.addEventListener('resize', fit);
  document.addEventListener('fullscreenchange', () => setTimeout(fit, 60));
  fit();
  // Der Ton laeuft von selbst und hoerbar los. Erlaubt ist das, weil der
  // Klick auf die Clipkarte die noetige Nutzergeste war und das <iframe>
  // sie ueber `allow="autoplay"` weitergereicht bekommt (clipRahmen in
  // physiklib.js bzw. mathlib.js). Verweigert der Browser trotzdem — etwa wenn jemand die
  // Clipdatei direkt aufruft, ohne vorher zu klicken —, faellt der Clip auf
  // stumm zurueck und der Knopf «Ton an» holt ihn hervor. Sobald der Ton
  // laeuft, fuehrt er die Uhr: Tondrift faellt auf, Bilddrift nicht.
  const ton = document.getElementById('ton'), ts = document.getElementById('ts');
  const tonBeschriften = () => {{
    if (ts) ts.textContent = (!ton || ton.muted) ? '🔇 Ton an' : '🔊 Ton aus';
  }};
  if (ton) {{
    ts.hidden = false;
    ton.muted = false;
    ton.play().then(tonBeschriften).catch(() => {{
      ton.muted = true;
      tonBeschriften();
      ton.play().catch(() => {{}});
    }});
    tonBeschriften();
    ts.onclick = () => {{
      ton.muted = !ton.muted;
      tonBeschriften();
      if (!ton.muted) {{ ton.currentTime = t; if (playing) ton.play().catch(() => {{}}); }}
    }};
  }}
  const tonLaeuft = () => ton && !ton.paused && !ton.ended;
  function loop(now) {{
    if (playing) {{
      if (tonLaeuft()) t = ton.currentTime;
      else {{ t += (now - t0) / 1000; if (t > DUR) t = DUR; }}
    }}
    t0 = now; seek(t);
    barf.style.width = (t / DUR * 100) + '%'; tt.textContent = t.toFixed(1) + ' s';
    requestAnimationFrame(loop);
  }}
  requestAnimationFrame(loop);
  const tonAn = () => {{ if (ton) {{ ton.currentTime = t; if (playing) ton.play().catch(() => {{}}); }} }};
  const toggle = () => {{
    playing = !playing;
    pp.textContent = playing ? 'Pause' : 'Play';
    if (ton) {{ if (playing) ton.play().catch(() => {{}}); else ton.pause(); }}
  }};
  pp.onclick = toggle;
  // Tastenkuerzel nicht in Eingabefeldern; die Leertaste nicht auf Knoepfen —
  // dort bestaetigt sie den Knopf (Antwort einer Frage, Play/Pause selbst).
  document.addEventListener('keydown', e => {{
    const ziel = e.target && e.target.closest ? e.target : null;
    if (ziel && ziel.closest('input, select, textarea')) return;
    if (e.code === 'Space' && ziel && ziel.closest('button, a, summary')) return;
    if (e.code === 'Space') {{ e.preventDefault(); toggle(); }}
    if (e.code === 'ArrowRight') {{ t = Math.min(DUR, t + 5); tonAn(); }}
    if (e.code === 'ArrowLeft') {{ t = Math.max(0, t - 5); tonAn(); }}
    const k = e.key.toLowerCase();
    if (k === 'r') {{ t = 0; playing = true; pp.textContent = 'Pause'; tonAn(); }}
    if (k === 'f') document.documentElement.requestFullscreen?.();
  }});
  document.getElementById('bar').onclick = e => {{
    const r = e.currentTarget.getBoundingClientRect();
    t = (e.clientX - r.left) / r.width * DUR; tonAn();
  }};
}} else {{ document.body.classList.add('render'); seek(0); }}
</script></body></html>
"""


def lektionen(dreh):
    """`lektion` darf ein Code oder eine Liste sein — hier immer eine Liste.

    Ein Clip gehoert oft auf mehrere Seiten. Die Bruchgleichung etwa passt
    ins Grundlagenfach unter g2-2b und ins Schwerpunktfach unter s2-2a; ohne
    Liste muesste man ihn duplizieren."""
    v = dreh.get("lektion", [])
    if isinstance(v, str):
        v = [v] if v else []
    return [str(x) for x in v]


def verzeichnis(neue):
    """clips.json fortschreiben — Grundlage fuer die Bibliotheksseite.

    Wichtig: Ein Lauf fuer einen einzelnen Clip darf die uebrigen Eintraege
    nicht wegwerfen. Darum wird der bestehende Index gelesen, die neu
    gebauten Eintraege ersetzen ihre Namensvettern, alles andere bleibt —
    ausser Eintraegen, deren HTML-Datei nicht mehr existiert."""
    ziel = os.path.join(CLIPS, "clips.json")
    bestand = []
    if os.path.exists(ziel):
        try:
            bestand = json.load(open(ziel, encoding="utf-8")).get("clips", [])
        except (ValueError, OSError) as e:
            print(f"  clips.json nicht lesbar ({e}) — wird neu angelegt.")

    frisch = {e["datei"] for e in neue}
    eintraege = list(neue)
    verwaist = 0
    for e in bestand:
        if e.get("datei") in frisch:
            continue
        if not os.path.exists(os.path.join(CLIPS, e.get("datei", ""))):
            verwaist += 1
            continue
        eintraege.append(e)

    eintraege.sort(key=lambda e: (e.get("fach", ""),
                                  (e.get("lektion") or [""])[0],
                                  e["titel"]))
    json.dump({"stand": date.today().isoformat(), "clips": eintraege},
              open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    hinweis = f", {verwaist} verwaiste entfernt" if verwaist else ""
    print(f"\n{ziel}  —  {len(eintraege)} Clips "
          f"({len(neue)} neu gebaut{hinweis})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Clip-Generator für mathe.begreifbar.ch")
    ap.add_argument("clip", nargs="?", help="einzelnes Drehbuch (ohne .json); ohne Angabe alle")
    ap.add_argument("--eigenstaendig", action="store_true",
                    help="Schriften einbetten — Datei läuft ohne die Site")
    a = ap.parse_args()

    if a.clip:
        quellen = [os.path.join(CLIPS, a.clip.removesuffix(".json") + ".json")]
    else:
        quellen = sorted(g for g in glob.glob(os.path.join(CLIPS, "*.json"))
                         if os.path.basename(g) not in ("clips.json", "vorlage.json"))
    if not quellen:
        sys.exit("Keine Drehbücher in clips/ gefunden.")

    eintraege = []
    for q in quellen:
        ziel, dreh, dauer = bauen(q, a.eigenstaendig)
        # "probe": true — ein Versuchsclip. Er wird gebaut, aber nicht in
        # clips.json aufgenommen und erscheint darum weder in der Bibliothek
        # noch auf einer Lektionsseite.
        if not a.eigenstaendig and not dreh.get("probe"):
            eintraege.append({
                "datei": os.path.basename(ziel),
                "titel": dreh.get("titel", ""),
                "kurzbeschrieb": dreh.get("kurzbeschrieb", ""),
                "fach": dreh.get("fach", ""),
                "lerngebiet": dreh.get("lerngebiet", ""),
                "lektion": lektionen(dreh),
                "themenbereich": dreh.get("themenbereich", ""),
                "reihe": dreh.get("reihe", ""),
                "folge": dreh.get("folge"),
                # Werkzeug-Clip: zeigt nicht den Stoff, sondern wie ein
                # Geraet ihn abkuerzt. Steht am Schluss seiner Reihe.
                "werkzeug": bool(dreh.get("werkzeug")),
                "stufe": dreh.get("stufe", []),
                "schlagworte": dreh.get("schlagworte", []),
                "dauer_s": round(dauer),
                "datum": dreh.get("datum", ""),
            })
            # Clip zu einer einzelnen Animation: Anker ihres <h3>. Daran
            # haengt build-clips-einbau.py den Knopf «▶ Clip» in die
            # Titelzeile und hebt die Zeile in den Listen farbig ab.
            if dreh.get("animation"):
                eintraege[-1]["animation"] = dreh["animation"]
    if eintraege:
        verzeichnis(eintraege)
