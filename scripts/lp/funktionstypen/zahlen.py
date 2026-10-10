"""Rechnet jede feste Zahl des Leitprogramms «Funktionstypen und Graphen» nach — Seite, Simulationen, Clips und PDFs,
exakt mit Fraction (Wurzeln nur aus Quadratzahlen).

  python3 scripts/lp/funktionstypen/zahlen.py      # Exit 1 bei einer Abweichung
"""
import sys
from fractions import Fraction as F
from math import isqrt

fehler = 0


def melde(ok, text):
    global fehler
    fehler += not ok
    print(('ok    ' if ok else 'FALSCH'), text)


def soll(name, ist, wert):
    melde(ist == wert, '%s | %s = %s' % (name, ist, wert))


def falsch(name, a, b):
    melde(a != b, 'Fehlerbeispiel %s | %s ≠ %s' % (name, a, b))


def wurzel(q):
    q = F(q)
    z, n = isqrt(q.numerator), isqrt(q.denominator)
    assert z * z == q.numerator and n * n == q.denominator, q
    return F(z, n)


def f(typ, a, b, x):
    """Familien wie in seite.js: g Gerade a·x + b, q Parabel a·x² + b, w Wurzel a·√x + b, k Kehrwert a/x + b."""
    a, b, x = F(a), F(b), F(x)
    if typ == 'g': return a * x + b
    if typ == 'q': return a * x * x + b
    if typ == 'w': return a * wurzel(x) + b
    return a / x + b


def strecken(stuetz):
    """Weg-Zeit-Graph aus Stützpunkten (t | s): Geschwindigkeiten je Abschnitt."""
    return [F(s2 - s1, t2 - t1) for (t1, s1), (t2, s2) in zip(stuetz, stuetz[1:])]


# ---- Vortest
soll('0a', [3 ** 2, (-3) ** 2, F(1, 2) ** 2], [9, 9, F(1, 4)])
soll('0b', [wurzel(16), wurzel(49)], [4, 7])
soll('0c', [F(12, 3), F(12) / F(1, 2)], [4, 24])
soll('0d', F(8 - 2, 2 - 0), 3)
soll('0e', F(30, 2), 15)

# ---- Kapitel 1: Vier Graphen-Familien
soll('Clip1 Parabel', [f('q', 1, 0, x) for x in (-2, 1, 2, 3)], [4, 1, 4, 9])
soll('Clip1 Wurzel', [f('w', 1, 0, x) for x in (1, 4, 9)], [1, 2, 3])
soll('Clip1 Kehrwert', [f('k', 1, 0, x) for x in (1, 2, F(1, 2))], [1, F(1, 2), 2])
soll('Clip1 Vorhersage (4|2), (9|3) nur Wurzel', [f('w', 1, 0, 4), f('w', 1, 0, 9), f('q', 1, 0, 2), f('g', 1, 0, 4)], [2, 3, 4, 4])
soll('Festhalten Testpunkt x = 4', [f('g', 1, 0, 4), f('q', 1, 0, 4), f('w', 1, 0, 4), f('k', 1, 0, 4)], [4, 16, 2, F(1, 4)])
soll('Sim1 Ziele', [f('g', 2, -1, 2), f('q', 1, -2, 2), f('w', 2, 0, 4), f('k', 4, 0, 2), f('q', F(-1, 2), 3, 2)], [3, 2, 4, 2, 1])
soll('1a x = 9', [f('g', 2, 0, 9), f('q', 1, 0, 9), f('w', 1, 0, 9), f('k', 18, 0, 9)], [18, 81, 3, 2])
soll('1b', [f('q', F(1, 2), 0, x) for x in (-4, -2, 0, 2, 4)], [8, 2, 0, 2, 8])
soll('1c y = 3/x', [f('k', 3, 0, 1), f('k', 3, 0, 3)], [3, 1])
soll('1d y = 6/x', [f('k', 6, 0, x) for x in (1, 2, 3, 6)], [6, 3, 2, 1])
soll('1f y = −0.5x²', [f('q', F(-1, 2), 0, 2), f('q', F(-1, 2), 0, -2)], [-2, -2])

# ---- Kapitel 2: Proportional, antiproportional, linear
soll('Clip2 Benzin', [f('g', F(9, 5), 0, 2), f('g', F(9, 5), 0, 4)], [F(18, 5), F(36, 5)])
soll('Clip2 Taxi', [f('g', F(5, 2), 6, 2), f('g', F(5, 2), 6, 4), 2 * f('g', F(5, 2), 6, 2)], [11, 16, 22])
soll('Clip2 Pizza', [f('k', 36, 0, 2), f('k', 36, 0, 4)], [18, 9])
soll('Sim2', [f('g', 3, 0, 2), f('g', 3, 4, 2), f('k', 12, 0, 3), f('k', 18, 0, 2)], [6, 10, 4, 9])
soll('2b', [[5 * x for x in (1, 2, 3)], [2 * x + 5 for x in (1, 2, 3)], [F(30, x) for x in (1, 2, 3)]], [[5, 10, 15], [7, 9, 11], [30, 15, 10]])
soll('2c', [F(5 * 12, 6), F(5 * 12, 3)], [10, 20])
soll('2d', [f('g', 3, 4, 2), f('g', 3, 4, 4)], [10, 16]); falsch('2d Ben verdoppelt', 2 * 10, 16)
soll('2e', [F(10, 4), 4 * 10], [F(5, 2), 40])
soll('2a Temperatur', [20 - F(6, 10) * 10], [14])

# ---- Kapitel 3: Weg-Zeit-Graphen
soll('Clip3 Anna', strecken([(0, 0), (10, 800), (15, 800), (20, 1400)]), [80, 0, 120])
soll('Sim3 Stände', [[0, 10 * a, 10 * (a + b), 10 * (a + b + c)] for a, b, c in [(60, 0, 120), (100, 50, 0), (80, 0, -80), (40, 80, 120), (120, -60, 30)]],
     [[0, 600, 600, 1800], [0, 1000, 1500, 1500], [0, 800, 800, 0], [0, 400, 1200, 2400], [0, 1200, 600, 900]])
soll('3a', strecken([(0, 0), (4, 600), (10, 600), (14, 1400)]), [150, 0, 200])
soll('3e 90 m/min in km/h', F(90 * 60, 1000), F(27, 5)); soll('Fest3 6 km/h', F(6000, 60), 100); soll('3f', [6 * 200, F(1200, 100), 6 + 4 + 12], [1200, 12, 22])

soll('3e 12 km/h in m/min', F(12000, 60), 200)

# ---- Kapitel 4: Zurückgelegt oder noch entfernt
soll('Clip4 Velo', [16 * F(3, 4), 24 - 16 * F(3, 4), F(24, 16)], [12, 12, F(3, 2)])
soll('Sim4', [F(20, 2 * 10), F(20 - 4, 8), F(14 - 6, 4), F(30, 12), F(18 * 2, 3 * 6)], [1, 2, 2, F(5, 2), 2])
soll('4a', [12 * 2, 36 - 12 * 2], [24, 12]); soll('4b', [F(18, 12), 12 * F(3, 2)], [F(3, 2), 18]); soll('4c', F(36 - 6, 12), F(5, 2)); soll('4d', F(15, 5), 3); soll('4f', [40 - 27, F(27) / F(3, 2)], [13, 18]); soll('Fehler2 y = −x + 6', [-x + 6 for x in (1, 2, 4)], [5, 4, 2])

soll('V1', [F(1, 2), F(1, 16)], [wurzel(F(1, 4)), F(1, 4) ** 2]); soll('V2', F(60 + 100, 2), 80)

# ---- Kontrollclips
soll('K1F2', f('k', 3, 0, 6), F(1, 2)); soll('K1F4', f('w', 2, 0, 9), 6); soll('K1F1', [f('q', F(1, 2), 0, 2), f('q', F(1, 2), 0, -2)], [2, 2]); soll('K1F5', [f('q', 1, 2, 0), f('q', 1, 2, 2)], [2, 6]); soll('Clip1 Vorhersage', [f('w', 1, 0, 9), f('w', 1, 0, 16), F(16, 3)], [3, 4, F(16, 3)])
soll('K2F4', [F(24, x) for x in (2, 4, 8, 6)], [12, 6, 3, 4]); soll('K2F5', [f('g', 5, 2, 2), f('g', 5, 2, 4)], [12, 22])
soll('K3F1', strecken([(0, 0), (5, 500)]), [100])
soll('K4F1', 30 - 20 * F(1, 2), 20); soll('K4F3', [F(15, 12), F(30, 12)], [F(5, 4), F(5, 2)]); soll('K4F4', 30 - 18, 12)

# ---- Gesamttest
soll('G1 x = 4', [f('g', 2, 1, 4), f('q', F(1, 2), 0, 4), f('w', 2, 0, 4), f('k', 4, 0, 4)], [9, 8, 4, 1])
soll('G1 Bildpunkte', [f('g', 2, 1, 0), f('q', F(1, 2), 0, 2), f('w', 2, 0, 1), f('k', 4, 0, 2)], [1, 2, 2, 2])
soll('G2', [f('k', 8, 0, x) for x in (1, 2, 4, 8)], [8, 4, 2, 1])
soll('G4', [8 * 9, F(72, 6), F(72, 12)], [72, 12, 6]); soll('G4 Fehler proportional', F(9, 8) * 6, F(27, 4))
soll('G5', strecken([(0, 0), (6, 480), (12, 480), (20, 1280)]), [80, 0, 100]); soll('G5 Gitter', [480 / 160, 1280 / 160, 6 / 2, 12 / 2, 20 / 2], [3, 8, 3, 6, 10])
soll('G7', [4 * 2, 12 - 4 * 2, F(12 - 3, 4)], [8, 4, F(9, 4)])
soll('Punkte', 4 + 3 + 3 + 3 + 4 + 2 + 3 + 3, 25)

print('\n' + ('ALLE ZAHLEN STIMMEN' if not fehler else f'{fehler} ABWEICHUNG(EN)'))
sys.exit(1 if fehler else 0)
