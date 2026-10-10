"""Geometrie eines `graf` im Clip — gemeinsam genutzt von allen Leitprogramm-Bauskripten
unter `scripts/lp/`: `<thema>/clips.py` setzt damit die Beschriftungen, `<thema>/pruef-graf.py`
prüft sie nach. Liegt seit dem 03.10.2026 eine Ebene höher, weil es das zweite Leitprogramm
mit Clip-Bildern gibt und zwei Kopien auseinanderlaufen würden.

Die Zahlen stammen aus scripts/build-clips.py, Funktion `graf_svg`: Innenrand 8 px,
Punktbeschriftung font-size 29, Achsenteilung font-size 22 (x-Marken 32 px unter der
Achse, mittig; y-Marken 13 px links davon, rechtsbündig, 8 px tiefer), Achsennamen
font-size 26 an den Pfeilen. Eine Beschriftung ohne Hof ist unlesbar, sobald eine
Gerade, ein Punkt oder eine Achsenbeschriftung darunter liegt — darum wird jede Stelle
gerechnet statt geschätzt (HOWTO-clips.md, «Die freie Stelle ausrechnen, nicht schätzen»).
"""
BILD = 760.0
RAND = 8.0
ZEICHEN = 16.0          # Breite eines Zeichens bei font-size 29
ZEICHEN_22 = 12.0       # dito bei font-size 22 (Achsenmarken)
HOCH, TIEF = 0.34, 0.12  # Textkiste über/unter der Grundlinie, als Anteil der Schriftgrösse


def masse(W, breite=BILD, hoehe=BILD):
    x0, x1 = W['xbereich']
    y0, y1 = W['ybereich']
    return x0, x1, y0, y1, (x1 - x0) / (breite - 2 * RAND), (y1 - y0) / (hoehe - 2 * RAND)


def kiste(text, lx, ly, anker, ex, ey, groesse=29.0, zeichen=ZEICHEN):
    """(links, rechts, unten, oben) der Textkiste in Datenkoordinaten."""
    br = len(text) * zeichen * ex
    a, b = (lx, lx + br) if anker == 'start' else (lx - br, lx) if anker == 'end' else (lx - br / 2, lx + br / 2)
    return a, b, ly - groesse * HOCH * ey, ly + groesse * TIEF * ey


def teilung(W, schluessel, a, e):
    eigen = W.get(schluessel)
    if eigen:
        return [(float(w), str(t)) for w, t in eigen]
    import math
    return [(float(i), str(i).replace('-', '−')) for i in range(math.ceil(a), int(math.floor(e)) + 1)]


def achsenkisten(W, breite=BILD, hoehe=BILD):
    """Textkisten der Achsenmarken und Achsennamen — Stellen, die schon belegt sind."""
    x0, x1, y0, y1, ex, ey = masse(W, breite, hoehe)
    aus = []
    for x, mark in teilung(W, 'xteilung', x0, x1):
        if abs(x) < 1e-9 or not (x0 <= x <= x1):
            continue
        aus.append(kiste(mark, x, -32 * ey, 'mitte', ex, ey, 22.0, ZEICHEN_22))
    for y, mark in teilung(W, 'yteilung', y0, y1):
        if abs(y) < 1e-9 or not (y0 <= y <= y1):
            continue
        aus.append(kiste(mark, -13 * ex, y - 8 * ey, 'end', ex, ey, 22.0, ZEICHEN_22))
    xn, yn = W.get('xname', 'x'), W.get('yname', 'y')
    aus.append(kiste(xn, x1 - 8 * ex, 14 * ey, 'end', ex, ey, 26.0, 14.0))
    aus.append(kiste(yn, 14 * ex, y1 - 4 * ey, 'start', ex, ey, 26.0, 14.0))
    return aus


def frei(k, geraden, punkte, belegt, W, eigen=None):
    """Liegt die Kiste k im Fenster und auf nichts drauf?"""
    x0, x1, y0, y1, _, _ = masse(W)
    a, b, u, o = k
    if not (x0 <= a and b <= x1 and y0 <= u and o <= y1):
        return False
    for m, q in geraden:
        if max(m * a + q, m * b + q) >= u and min(m * a + q, m * b + q) <= o:
            return False
    for px, py in punkte:
        if (px, py) == eigen:
            continue
        if a - 0.2 * (x1 - x0) / 9 <= px <= b + 0.2 * (x1 - x0) / 9 and \
           u - 0.2 * (y1 - y0) / 9 <= py <= o + 0.2 * (y1 - y0) / 9:
            return False
    for a2, b2, u2, o2 in belegt:
        if a < b2 and a2 < b and u < o2 and u2 < o:
            return False
    return True
