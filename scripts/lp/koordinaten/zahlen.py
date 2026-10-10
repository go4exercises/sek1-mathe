"""Rechnet jede feste Zahl des Leitprogramms «Abbildungen und Geraden im Koordinatensystem» (Geometrie) nach — Seite,
Simulationen, Clips und PDFs, exakt mit Fraction.

  python3 scripts/lp/koordinaten/zahlen.py      # Exit 1 bei einer Abweichung
"""
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


def P(x, y):
    return (F(x), F(y))


def punkt(P_, Z):
    """Punktspiegelung: P' = 2Z − P."""
    return (2 * Z[0] - P_[0], 2 * Z[1] - P_[1])


def zentrum(P_, Q):
    return ((P_[0] + Q[0]) / 2, (P_[1] + Q[1]) / 2)


def achse(P_, art, a=0):
    x, y = P_
    return {'x': (x, -y), 'y': (-x, y), 'xa': (2 * F(a) - x, y), 'yb': (x, 2 * F(a) - y), 'd': (y, x)}[art]


def streck(P_, Z, k):
    k = F(k)
    return (Z[0] + k * (P_[0] - Z[0]), Z[1] + k * (P_[1] - Z[1]))


def flaeche(*pk):
    """Schnürsenkel-Formel (Kontrolle der Rechteck-minus-Dreiecke-Rechnung)."""
    s = 0
    for (x1, y1), (x2, y2) in zip(pk, pk[1:] + pk[:1]):
        s += F(x1) * F(y2) - F(x2) * F(y1)
    return abs(s) / 2


def gerade(A, B):
    m = (F(B[1]) - F(A[1])) / (F(B[0]) - F(A[0]))
    return m, F(A[1]) - m * F(A[0])


def auf(m, b, Q):
    return F(m) * F(Q[0]) + F(b) == F(Q[1])


# ---- Vortest
soll('0a', zentrum(P(2, 6), P(8, 2)), P(5, 4))
soll('0b', [2 * 3 - 7, 2 * (-1) - 4], [-1, -6])
soll('0c', 5 * 3, 15)
soll('0d', [2 * 4 - 3, 2 * 1 - 3], [5, -1])
soll('0e', gerade(P(1, 2), P(3, 8))[0], 3)

# ---- Kapitel 1 · Punktspiegelung
soll('Clip1', punkt(P(5, 3), P(2, 1)), P(-1, -1)); falsch('Clip1 P+Z', (F(7), F(4)), P(-1, -1))
soll('Clip1 Vorhersage', punkt(P(3, 4), P(2, 1)), P(1, -2))
soll('Clip1 Dreieck', [punkt(p, P(0, 0)) for p in (P(1, 1), P(4, 1), P(2, 3))], [P(-1, -1), P(-4, -1), P(-2, -3)])
soll('Fest1', [punkt(P(4, 3), P(1, 2)), [punkt(p, P(0, 0)) for p in (P(2, 1), P(5, 1), P(4, 4))]], [P(-2, 1), [P(-2, -1), P(-5, -1), P(-4, -4)]])
soll('Sim1', [zentrum(P(3, 1), P(-1, 5)), punkt(P(2, -3), P(0, 0)), zentrum(P(-4, 1), P(2, -3)), punkt(P(-5, 0), P(-1, 2))],
     [P(1, 3), P(-2, 3), P(-1, -1), P(3, 4)])
soll('1a', [punkt(P(5, 2), P(1, 1)), punkt(P(3, -1), P(1, 1))], [P(-3, 0), P(-1, 3)])
soll('1b', punkt(P(1, 5), P(-2, 3)), P(-5, 1))
soll('1c', [[punkt(p, P(0, 2)) for p in (P(1, 1), P(4, 1), P(1, 3))], flaeche(P(1, 1), P(4, 1), P(1, 3))], [[P(-1, 3), P(-4, 3), P(-1, 1)], 3])
soll('1d', punkt(P(4, 1), P(2, 3)), P(0, 5)); falsch('1d Tim', (F(6), F(4)), P(0, 5))
soll('1e', zentrum(P(7, 2), P(-1, 6)), P(3, 4))
soll('K1', [punkt(P(3, -4), P(0, 0)), punkt(P(4, 6), P(1, 2)), zentrum(P(2, 5), P(6, 1))], [P(-3, 4), P(-2, -2), P(4, 3)])
soll('K1F5', punkt(P(3, 1), P(1, 0)), P(-1, -1)); falsch('K1F5 P+Z', (F(4), F(1)), P(-1, -1))

# ---- Kapitel 2 · Achsenspiegelung
soll('Clip2', [achse(P(3, 2), 'x'), achse(P(3, 2), 'y'), achse(P(3, 2), 'xa', 1), achse(P(3, 2), 'd')], [P(3, -2), P(-3, 2), P(-1, 2), P(2, 3)])
soll('Clip2 Vorhersage', achse(P(4, 1), 'xa', 2), P(0, 1))
soll('Fest2', [achse(P(5, -1), 'x'), achse(P(5, -1), 'y'), achse(P(5, -1), 'xa', 2), achse(P(5, -1), 'yb', 2), achse(P(5, -1), 'd')],
     [P(5, 1), P(-5, -1), P(-1, -1), P(5, 5), P(-1, 5)])
soll('Sim2', [(F(5) + F(-1)) / 2, achse(P(3, -2), 'y'), (F(4) + F(-2)) / 2, achse(P(-1, 4), 'd'), (F(2) + F(-4)) / 2], [2, P(-3, -2), 1, P(4, -1), -1])
soll('2a', [achse(P(4, -3), 'x'), achse(P(4, -3), 'y'), achse(P(4, -3), 'd')], [P(4, 3), P(-4, -3), P(-3, 4)])
soll('2b', achse(P(-2, 5), 'xa', 3), P(8, 5))
soll('2c', achse(P(1, -2), 'yb', 2), P(1, 6))
soll('2d', [achse(p, 'd') for p in (P(1, 2), P(4, 2), P(4, 5))], [P(2, 1), P(2, 4), P(5, 4)])
soll('2e', achse(P(3, 5), 'x'), P(3, -5)); falsch('2e Lea', P(-3, 5), P(3, -5))
soll('K2', [achse(P(-4, 1), 'y'), achse(P(2, 3), 'xa', 5), achse(P(6, -1), 'd'), achse(P(0, 4), 'yb', 1), (F(7) + F(-1)) / 2],
     [P(4, 1), P(8, 3), P(-1, 6), P(0, -2), 3])

# ---- Kapitel 3 · Zentrische Streckung und Flächen
soll('Clip3', [[streck(p, P(0, 0), 2) for p in (P(1, 1), P(3, 1), P(1, 2))], flaeche(P(1, 1), P(3, 1), P(1, 2)), flaeche(P(2, 2), P(6, 2), P(2, 4))],
     [[P(2, 2), P(6, 2), P(2, 4)], 1, 4])
soll('Clip3 Z', streck(P(2, 3), P(1, 1), 3), P(4, 7)); falsch('Clip3 ohne Z', (F(6), F(9)), P(4, 7))
soll('Clip3 Vorhersage', 2 * 1 * 2 ** 2, 8)
soll('Clip3 Fläche', [4 * 3 - F(4 * 1, 2) - F(1 * 3, 2) - F(3 * 2, 2), flaeche(P(1, 1), P(5, 2), P(2, 4))], [F(11, 2), F(11, 2)])
soll('Sim3', [streck(P(2, 1), P(0, 0), 2), streck(P(2, 1), P(1, 1), 2), 9, F(1, 2)], [P(4, 2), P(3, 1), 9, F(1, 2)])
soll('3a', [[streck(p, P(0, 0), 3) for p in (P(1, 0), P(3, 0), P(1, 2))], flaeche(P(1, 0), P(3, 0), P(1, 2)), flaeche(P(3, 0), P(9, 0), P(3, 6))],
     [[P(3, 0), P(9, 0), P(3, 6)], 2, 18])
soll('3b', streck(P(5, 3), P(2, 1), 2), P(8, 5))
soll('3c', [6 * 5 - F(6 * 1, 2) - F(4 * 4, 2) - F(2 * 5, 2), flaeche(P(0, 0), P(6, 1), P(2, 5))], [14, 14])
soll('3d', streck(P(4, 3), P(1, 1), 2), P(7, 5)); falsch('3d Ben', P(8, 6), P(7, 5))
soll('3e', 5 * 4 ** 2, 80)
soll('K3', [streck(P(2, -1), P(0, 0), 3), streck(P(3, 3), P(1, 2), 2), 7 * 2 ** 2, flaeche(P(1, 1), P(5, 1), P(3, 4)), F(3, 1)],
     [P(6, -3), P(5, 4), 28, 6, 3])

# ---- Kapitel 4 · Gerade durch zwei Punkte und Punktprobe
soll('Clip4', gerade(P(1, 3), P(4, 9)), (2, 1))
soll('Clip4 Proben', [auf(2, 1, P(10, 21)), auf(2, 1, P(50, 102)), auf(2, 1, P(100, 201))], [True, False, True])
falsch('Clip4 Δx/Δy', F(3, 6), 2)
soll('Sim4', [gerade(P(0, -2), P(4, 4)), gerade(P(-3, 0), P(3, 4))], [(F(3, 2), -2), (F(2, 3), 2)])
soll('4a', gerade(P(2, 1), P(6, 9)), (2, -3))
soll('4b', [auf(2, -3, P(40, 77)), auf(2, -3, P(25, 46))], [True, False])
soll('4c', gerade(P(-2, 5), P(4, -1)), (-1, 3))
soll('4d', gerade(P(1, 2), P(3, 8))[0], 3); falsch('4d Mia', F(2, 6), 3)
soll('4e', [punkt(P(1, 2), P(3, 3)), gerade(P(1, 2), P(5, 4)), auf(F(1, 2), F(3, 2), P(3, 3))], [P(5, 4), (F(1, 2), F(3, 2)), True])
soll('K4', [gerade(P(0, 1), P(2, 7))[0], 4 - 2 * 3, auf(3, -5, P(10, 25)), auf(2, 5, P(20, 50))], [3, -2, True, False])
soll('K4F5', gerade(P(1, 1), P(2, 5))[0], 4); falsch('K4F5 Δx/Δy', F(1, 4), 4)

# ---- Gesamttest
soll('G1', [punkt(p, P(1, 0)) for p in (P(2, 1), P(5, 2), P(3, 4))], [P(0, -1), P(-3, -2), P(-1, -4)])
soll('G2', [zentrum(P(-3, 4), P(5, 0)), punkt(P(4, 5), P(1, 2))], [P(1, 2), P(-2, -1)]); falsch('G2b Q + Z', P(5, 7), P(-2, -1))
soll('G3', [achse(P(4, -1), 'x'), achse(P(4, -1), 'y'), achse(P(4, -1), 'd')], [P(4, 1), P(-4, -1), P(-1, 4)])
soll('G4', [(F(-2) + 6) / 2, achse(P(1, -1), 'xa', 2)], [2, P(3, -1)])
soll('G5', [[streck(p, P(1, 1), 2) for p in (P(2, 1), P(4, 1), P(2, 3))], flaeche(P(2, 1), P(4, 1), P(2, 3)), flaeche(P(3, 1), P(7, 1), P(3, 5))],
     [[P(3, 1), P(7, 1), P(3, 5)], 2, 8])
soll('G6', [8 * 6 - F(8 * 2, 2) - F(5 * 4, 2) - F(3 * 6, 2), flaeche(P(0, 0), P(8, 2), P(3, 6))], [21, 21])
soll('G7', gerade(P(-1, -5), P(3, 7)), (3, -2))
soll('G8', [auf(3, -2, P(50, 148)), auf(3, -2, P(-20, -61)), 3 * (-20) - 2], [True, False, -62])

# ---- Vertiefung
soll('V1 zweimal punktgespiegelt', punkt(punkt(P(2, 1), P(0, 0)), P(3, 0)), P(8, 1))     # = Verschiebung um 2 · (3|0)
soll('V2 Spiegelung an y = −x', (-P(5, 3)[1], -P(5, 3)[0]), P(-3, -5))                         # P(5|3) → (−3|−5)
soll('V3 Streckung k = −1', streck(P(4, 2), P(1, 1), -1), punkt(P(4, 2), P(1, 1)))

print('\nALLE ZAHLEN STIMMEN' if not fehler else '\n%d ABWEICHUNG(EN)' % fehler)
sys.exit(1 if fehler else 0)
