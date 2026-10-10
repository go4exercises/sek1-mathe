"""Rechnet jede feste Zahl des Leitprogramms «Flächen, Pythagoras und Ähnlichkeit» (Geometrie) nach — Seite, Simulationen,
Clips und PDFs, exakt mit Fraction. Wurzeln nur, wo sie aufgehen (ohne Taschenrechner).

  python3 scripts/lp/pythagoras/zahlen.py      # Exit 1 bei einer Abweichung
"""
import math
import sys
from fractions import Fraction as F

fehler = 0


def melde(ok, text):
    global fehler
    fehler += not ok
    print(('ok    ' if ok else 'FALSCH'), text)


def soll(name, ist, wert):
    melde(ist == wert, '%s | %s = %s' % (name, ist, wert))


def falsch(name, a, b):
    melde(a != b, 'Fehlerbeispiel %s | %s ≠ %s' % (name, a, b))


def w(q):
    """Exakte Wurzel einer Quadratzahl (auch Brüche); sonst Fehler."""
    q = F(q)
    z, n = math.isqrt(q.numerator), math.isqrt(q.denominator)
    assert z * z == q.numerator and n * n == q.denominator, ('keine Quadratzahl', q)
    return F(z, n)


def hyp(a, b):
    return w(F(a) ** 2 + F(b) ** 2)


def kat(c, a):
    return w(F(c) ** 2 - F(a) ** 2)


def dreieck(g, h):
    return F(g) * F(h) / 2


def trapez(a, c, h):
    return (F(a) + F(c)) / 2 * F(h)


def ca(op, a, b):
    """gerundete Wurzel für Ablenker und schräge Seiten (geht nicht auf)"""
    import math
    return round(math.sqrt(float(F(a) ** 2 + F(b) ** 2 if op == '+' else F(a) ** 2 - F(b) ** 2)), 1)


# ---- Vortest
soll('0a', [7 * 4, 2 * (7 + 4)], [28, 22])
soll('0b', [7 ** 2, 12 ** 2, w(81), w(144)], [49, 144, 9, 12])
soll('0c', w(64), 8)
soll('0d', [100 * 100, F(35, 10) * 100], [10000, 350])
soll('0e', F(9 * 4, 6), 6)

# ---- Kapitel 1 · Flächen
soll('Clip1 Dreieck', dreieck(6, 4), 12); falsch('Clip1 schräge Seite', dreieck(6, 5), 12)
soll('Clip1 Parallelogramm', 6 * 4, 24); soll('Clip1 Trapez', [dreieck(7, 4) + dreieck(3, 4), trapez(7, 3, 4)], [20, 20]); soll('Clip1 Haus', 6 * 4 + dreieck(6, 3), 33)
soll('Fest1', [dreieck(8, 5), 7 * 4, trapez(9, 5, 4), 8 * 6 - 3 * 2], [20, 28, 28, 42])
soll('Sim1', [F(2 * 16, 8), dreieck(7, 4), F(20, 5), dreieck(10, 3), F(24, 4)], [4, 14, 4, 15, 6])
soll('1a', [dreieck(9, 6), 12 * 5], [27, 60]); falsch('1a schräg', 12 * 7, 60)
soll('1b', trapez(11, 7, 6), 54)
soll('1c', 10 * 8 - dreieck(4, 3), 74)
soll('1d', dreieck(12, 8), 48); falsch('1d Mia', dreieck(12, 10), 48)
soll('1e', F(2 * 30, 12), 5)
soll('K1', [dreieck(10, 7), 9 * 4, trapez(8, 4, 5), 6 * 5 - 2 * 2], [35, 36, 30, 26]); falsch('K1F3 Seite', 9 * 5, 36)

# ---- Kapitel 2 · Pythagoras
soll('Clip2 3-4-5', [3 ** 2 + 4 ** 2, hyp(3, 4), 7 * 7 - 4 * dreieck(3, 4)], [25, 5, 25])           # schräges Quadrat: 7 × 7 minus vier Dreiecke
soll('Clip2 Vorhersage', hyp(6, 8), 10); falsch('Clip2 6+8', 6 + 8, 10)
soll('Clip2 Kathete', kat(10, 6), 8); falsch('Clip2 Kathete addiert', F(10 ** 2 + 6 ** 2), 64)
soll('Sim2', [hyp(9, 12), kat(17, 8), hyp(12, 16), kat(25, 7), 10 ** 2 + 10 ** 2], [15, 15, 20, 24, 200])
soll('2a', hyp(15, 20), 25)
soll('2b', kat(26, 10), 24)
soll('2c', [7 ** 2 + 24 ** 2, 25 ** 2, 6 ** 2 + 7 ** 2, 9 ** 2], [625, 625, 85, 81])
soll('2d', kat(13, 5), 12); falsch('2d Ben', F(13 ** 2 + 5 ** 2), 144)
soll('2e', kat(41, 40), 9)
soll('K2', [hyp(5, 12), kat(F(15, 2), 6), 7 ** 2 + 24 ** 2, 26 ** 2, kat(F(25, 2), 12)], [13, F(9, 2), 625, 676, F(7, 2)])
soll('K2 Ablenker', [F(15, 2) - 6, ca('+', F(15, 2), 6), ca('+', F(25, 2), 12), F(25, 2) - 12], [F(3, 2), 9.6, 17.3, F(1, 2)])
soll('Fest2 halbe', [F(15, 2) ** 2, w(F(7225, 100))], [F(5625, 100), F(17, 2)])

# ---- Kapitel 3 · Hilfsdreiecke und Kreis
soll('Clip3 Rechteck', hyp(20, 21), 29)
soll('Clip3 gleichschenklig', kat(17, 8), 15)
soll('Clip3 Sehne', kat(10, 8), 6)                                  # r = 10, halbe Sehne 8 → Abstand 6
soll('Clip3 Rohr', [kat(25, 24), 25 - kat(25, 24)], [7, 18])        # Ø 50, Wasserspiegel 48 → d = 7, Tiefe 18
soll('Sim3', [2 * kat(13, 5), kat(5, 4), kat(15, 9), kat(15, 12), kat(5, 3), 5 - kat(5, 3)], [24, 3, 12, 9, 4, 1])   # Aufgabe 5: r 5, Breite 6 → d 4, Tiefe 1
soll('3a', hyp(15, 8), 17)
soll('3b', [kat(25, 15), dreieck(30, kat(25, 15))], [20, 300])
soll('3c', kat(5, F(14, 10)), F(48, 10))
soll('3d', kat(26, 24), 10)
soll('3e', [kat(17, 15), 17 - kat(17, 15)], [8, 9])                 # Ø 34, Wasserspiegel 30 → d = 8, Tiefe 9
soll('3f', hyp(F(17, 2) - 1, 11 - 1), F(25, 2))
soll('K3', [hyp(F(15, 2), 4), kat(15, 9), 2 * kat(F(5, 2), F(3, 2)), kat(F(13, 2), 6), F(13, 2) - kat(F(13, 2), 6)], [F(17, 2), 12, 4, F(5, 2), 4])
soll('K3 Ablenker', [F(15, 2) + 4, ca('-', F(15, 2), 4), kat(F(5, 2), F(3, 2)), F(5, 2) - F(3, 2), F(13, 2) + F(5, 2)], [F(23, 2), 6.3, 2, 1, 9])

# ---- Kapitel 4 · Ähnlichkeit
soll('Clip4', [[2 * s for s in (3, 4, 5)], dreieck(3, 4), dreieck(6, 8), F(dreieck(6, 8), dreieck(3, 4))], [[6, 8, 10], 6, 24, 4])
soll('Clip4 Schatten', F(2, 3) * 15, 10)
soll('Clip4 Regal', [dreieck(60, 40), dreieck(30, 20), dreieck(60, 40) - dreieck(30, 20)], [1200, 300, 900])
soll('Sim4', [6 * F(3, 2) ** 2, F(1, 2) ** 2, F(9, 4), F(125, 10) / 5, F(375, 100) / 5], [F(27, 2), F(1, 4), F(9, 4), F(5, 2), F(3, 4)])
soll('4a', [F(12, 8), [F(3, 2) * s for s in (4, 6, 8)]], [F(3, 2), [6, 9, 12]])
soll('4b', 10 * 3 ** 2, 90)
soll('4c', F(15, 10) / 2 * 12, 9)
soll('4d', 15 * 3 ** 2, 135); falsch('4d Lea', 15 * 3, 135)
soll('4f', [F(6, 4), F(9, 6), F(105, 70), F(4, 2), F(5, 3)], [F(3, 2), F(3, 2), F(3, 2), 2, F(5, 3)])
soll('4e', [dreieck(80, 60), dreieck(20, 15), dreieck(80, 60) - dreieck(20, 15)], [2400, 150, 2250])
soll('K4', [2 * 9, 8 * 3 ** 2, w(16), F(2, F(16, 10)) * 24, F(75, 10) / 3], [18, 72, 4, 30, F(5, 2)])

# ---- Gesamttest (neu nach der Prüfung 10.10.2026)
soll('G1', trapez(15, 9, 8), 96); soll('G1 schräge Seiten', [ca('+', 2, 8), ca('+', 4, 8)], [8.2, 8.9])
soll('G2', [F(2 * 42, 7), 9 * 6], [12, 54])
soll('G3', hyp(18, 24), 30); falsch('G3 addiert', 18 + 24, 30); soll('G3b', [8 ** 2 + 15 ** 2, 18 ** 2], [289, 324])
soll('G4', kat(61, 11), 60)
soll('G5', [kat(39, 15), dreieck(30, kat(39, 15))], [36, 540])
soll('G6', [25 - 10, kat(25, 15), 2 * kat(25, 15)], [15, 20, 40])     # Ø 50, Wasser 10 tief → d = 15, Breite 40
soll('G7', [F(30, 90), F(1, 3) * 60, dreieck(90, 60), dreieck(30, 20), dreieck(90, 60) - dreieck(30, 20)], [F(1, 3), 20, 2700, 300, 2400])
soll('G8', F(12, 8) * 14, 21)

# ---- Vertiefung
soll('V1 Raumdiagonale', hyp(hyp(3, 4), 12), 13)
soll('V2 Quadrat im Kreis', [F(10, 1) ** 2 / 2], [50])            # Diagonale 10 = Durchmesser → Seite² = 50
soll('V3 Gitter', hyp(5, 12), 13)

print('\nALLE ZAHLEN STIMMEN' if not fehler else '\n%d ABWEICHUNG(EN)' % fehler)
sys.exit(1 if fehler else 0)
