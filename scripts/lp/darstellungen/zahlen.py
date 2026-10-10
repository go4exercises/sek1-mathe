"""Rechnet jede feste Zahl des Leitprogramms «Darstellungen wechseln» (Lineare Funktionen II) nach —
Seite, Simulationen, Clips und PDFs, exakt mit Fraction.

  python3 scripts/lp/darstellungen/zahlen.py      # Exit 1 bei einer Abweichung

gerade(name, m, b, punkte): y = m·x + b geht durch alle Punkte. soll(name, ist, wert): Gleichheit.
falsch(name, a, b): Ein Fehlerbeispiel weicht wirklich ab.
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


def y(m, b, x):
    return F(m) * F(x) + F(b)


def gerade(name, m, b, punkte):
    melde(all(y(m, b, px) == F(py) for px, py in punkte), '%s | y = %s·x + %s durch %s' % (name, m, b, punkte))


def steigung(p, q):
    return F(q[1] - p[1]) / F(q[0] - p[0])


def durch(p, q):
    m = steigung(p, q)
    return m, F(p[1]) - m * p[0]


def summe(a, c, s):
    """a·x + c·y = s nach y: (m, b)."""
    return F(-a, c), F(s, c)


def tabelle(xs, ys):
    """Gleichung aus einer Tabelle — alle Paare auf einer Geraden?"""
    m, b = durch((xs[0], ys[0]), (xs[1], ys[1]))
    assert all(y(m, b, u) == v for u, v in zip(xs, ys)), (xs, ys)
    return m, b


def art(xs, ys):
    d = [F(ys[i + 1] - ys[i], xs[i + 1] - xs[i]) for i in range(len(xs) - 1)]
    if len(set(d)) == 1:
        return 'proportional' if ys[0] * xs[1] == ys[1] * xs[0] else ('linear fallend' if d[0] < 0 else 'linear steigend')
    if len({F(u) * v for u, v in zip(xs, ys)}) == 1:
        return 'antiproportional'
    return 'keines'


# ---- Vortest
soll('0a', [y(4, 10, 0), y(4, 10, 3)], [10, 22])
soll('0b', [summe(1, 1, 25), summe(3, 1, 12)], [(-1, 25), (-3, 12)])
soll('0c', steigung((1, 5), (4, 14)), 3)
soll('0d', [art([1, 2, 4], [12, 6, 3]), art([1, 2, 4], [3, 6, 12])], ['antiproportional', 'proportional'])
soll('0e', [2 + F(30, 60), F(90, 60)], [F(5, 2), F(3, 2)])

# ---- Kapitel 1: Vier Darstellungen
gerade('Clip1 Kletterhalle', 6, 40, [(0, 40), (1, 46), (2, 52), (3, 58), (4, 64), (5, 70), (10, 100)])
soll('Clip1 rückwärts 100 Fr.', F(100 - 40, 6), 10)
soll('F1 Tabelle mit Schritt 2', tabelle([2, 4, 6], [52, 64, 76]), (6, 40)); falsch('F1 Δx vergessen', 64 - 52, 6)
soll('Sim1', [tabelle([0, 1, 2], [30, 27, 24]), tabelle([2, 4, 6], [18, 26, 34]), (7, 42 - 7 * 4), durch((2, 35), (6, 15))],
     [(-3, 30), (4, 10), (7, 14), (-5, 45)])
gerade('1a Handy', 4, 15, [(0, 15), (1, 19), (2, 23), (3, 27), (6, 39)])
soll('1b Planschbecken', tabelle([0, 5, 10], [200, 175, 150]), (-1 * 5, 200)); soll('1b leer', F(200, 5), 40)
gerade('1c Parkieren', 1, 2, [(0, 2), (4, 6)])
soll('1d Lia', tabelle([2, 4, 6], [9, 15, 21]), (3, 3)); falsch('1d Lia m = 6', 15 - 9, 3)
gerade('1e Taxi', F(5, 2), 6, [(8, 26)])

# ---- Kapitel 2: Summe bleibt gleich
soll('Clip2 Rechteck U = 24', summe(2, 2, 24), (-1, 12)); soll('Clip2 Vorhersage x = 5', [12 - 5, 24 - 5, 24 - 2 * 5], [7, 19, 14])
soll('Clip2 Tabelle', [12 - x for x in (2, 4, 6, 8, 10)], [10, 8, 6, 4, 2])
soll('Clip2 Fest', summe(3, 2, 30), (F(-3, 2), 15)); soll('Clip2 Fest x = 4', y(F(-3, 2), 15, 4), 9)
soll('Clip2 Fehler y = 24 − 2x, Probe x = 2', 2 * 2 + 2 * (24 - 2 * 2), 44)
soll('Sim2', [20 // 2 - 3, F(30, 4), 24 // 2 - 4, 2 * (5 + 9), 16 // 2 - F(3, 2)], [7, F(15, 2), 8, 28, F(13, 2)])
soll('Sim2.3 y doppelt', 2 * 4, 24 // 2 - 4)
gerade('2a Saal', -1, 50, [(0, 50), (50, 0)])
soll('2b', [summe(3, 1, 21), summe(6, 3, 24)], [(-3, 21), (-2, 8)])
soll('2c Dreieck', [summe(2, 1, 30), y(-2, 30, 10), y(-2, 30, 12)], [(-2, 30), 10, 6])
soll('2d Ben Probe x = 5', 2 * 5 + 2 * (40 - 2 * 5), 70); soll('2d richtig', summe(2, 2, 40), (-1, 20))
soll('2e Budget', summe(3, 2, 24), (F(-3, 2), 12))
soll('2e ganzzahlig', [(x, y(F(-3, 2), 12, x)) for x in range(0, 9) if y(F(-3, 2), 12, x).denominator == 1],
     [(0, 12), (2, 9), (4, 6), (6, 3), (8, 0)])

# ---- Kapitel 3: Sinnvolle Werte, saubere Achsen
gerade('Clip3 Treppe a = 63 − 2h', -2, 63, [(15, 33), (20, 23), (18, 27)])
soll('Sim3 Bereiche', [F(30, F(5, 2)), F(120, 8), F(18, 2), F(100, 8)], [12, 15, 9, F(25, 2)])
soll('3a Kerze', [F(20, F(5, 2)), y(F(-5, 2), 20, 8)], [8, 0])
soll('3b Skala', [F(450, 9), F(70, 8)], [50, F(35, 4)])          # 8.75 → bequem 10
gerade('3d Taxi', 3, 6, [(0, 6), (10, 36)])

# ---- Kapitel 4: Linear fallend oder antiproportional
gerade('Clip4 Restweg s = 30 − 15t', -15, 30, [(0, 30), (1, 15), (2, 0), (F(1, 2), F(45, 2))])
soll('Clip4 Fahrzeit t = 30/v', [F(30, v) for v in (10, 15, 20, 30)], [3, 2, F(3, 2), 1])
soll('Clip4 Restweg nicht halbiert', [y(-15, 30, F(1, 2)), y(-15, 30, 1)], [F(45, 2), 15])
soll('Clip4 Rechteck Fläche 36, x 3 → 6', [F(36, 3), F(36, 6)], [12, 6])
soll('Sim4', [6 + 6 == 12 and 6 * 6 == 36, 4 + 6 == 10 and 4 * 6 == 24, F(24, 3), F(24, 6), 12 - 2, 12 - 7, 4 * 5 == 20 and 4 + 5 == 9],
     [True, True, 8, 4, 10, 5, True])
soll('4a', [art([1, 2, 4, 5], [20, 10, 5, 4]), art([1, 2, 4, 5], [18, 15, 9, 6]), art([1, 2, 4, 5], [2, 4, 8, 10])],
     ['antiproportional', 'linear fallend', 'proportional'])
soll('4a B Gleichung', tabelle([1, 2, 4, 5], [18, 15, 9, 6]), (-3, 21))
soll('4b', [F(120, v) for v in (40, 60, 80)], [3, 2, F(3, 2)])
soll('4c', y(-60, 120, F(3, 2)), 30)
soll('4d Gegenbeispiel y = 10 − x', [9 * 1, 8 * 2], [9, 16])
soll('4e', [[F(36, x) for x in (3, 6, 9)], [12 - x for x in (3, 6, 9)]], [[12, 6, 4], [9, 6, 3]])

# ---- Vertiefung
soll('V1 Flächen', [x * (10 - x) for x in range(1, 10)], [9, 16, 21, 24, 25, 24, 21, 16, 9])
soll('V2', F(63, 3), 21); soll('V3', [F(24, 3), F(24, 100), F(24, 100) * 60], [8, F(6, 25), F(72, 5)])

# ---- Clips: Kontrollfragen
gerade('K1F1 Streaming', 2, 5, [(0, 5), (3, 11)]); soll('K1F2', tabelle([0, 2, 4], [7, 13, 19]), (3, 7)); falsch('K1F2 m = 6', 6, 3)
soll('K1F4', tabelle([1, 3, 5], [10, 6, 2]), (-2, 12)); gerade('K1F5 Pool', F(1, 2), 3, [(2, 4)])
soll('K2F1', summe(2, 2, 30), (-1, 15)); soll('K2F2', 15 - 4, 11); soll('K2F3', summe(2, 1, 10), (-2, 10))
soll('K2F4', summe(3, 3, 21), (-1, 7)); soll('K2F5 Zaun', [summe(2, 1, 40), y(-2, 40, 12)], [(-2, 40), 16])
soll('K3F1 Kerze', F(18, 3), 6); soll('K3F3 Skala 170 : 9 → 20', [F(170, 9) > 10, F(170, 9) <= 20, 10 * 9 < 170], [True, True, True]); soll('K3F5 Tank', F(60, 4), 15)
soll('K4F1', art([1, 2, 3, 6], [18, 9, 6, 3]), 'antiproportional'); soll('K4F2', art([0, 1, 2, 3], [12, 9, 6, 3]), 'linear fallend')
soll('K4F3', F(4 * 6, 8), 3); soll('K4F4', [10 - 2, 10 - 4], [8, 6]); soll('K4F5', [2 * 6, 4 * 4], [12, 16])

# ---- Gesamttest
gerade('G1 Scooter', F(3, 10), F(3, 2), [(0, F(3, 2)), (10, F(9, 2)), (20, F(15, 2)), (25, 9)])
soll('G2', tabelle([3, 5, 9], [17, 25, 41]), (4, 5)); falsch('G2 Δy ohne Δx', 25 - 17, 4)
soll('G3', [summe(2, 2, 36), y(-1, 18, F(15, 2))], [(-1, 18), F(21, 2)])
soll('G4 Gutschein', summe(12, 8, 60), (F(-3, 2), F(15, 2)))
soll('G4 ganzzahlig', [(x, y(F(-3, 2), F(15, 2), x)) for x in range(0, 6) if y(F(-3, 2), F(15, 2), x).denominator == 1],
     [(1, 6), (3, 3), (5, 0)])
gerade('G5 Pool', 15, 40, [(0, 40), (8, 160)])
soll('G7', [art([1, 2, 3, 6], [30, 15, 10, 5]), art([1, 2, 3, 6], [25, 20, 15, 0]), tabelle([1, 2, 3, 6], [25, 20, 15, 0])],
     ['antiproportional', 'linear fallend', (-5, 30)])
soll('G8a', [10 - 2, 10 - 4, F(10 - 2, 2)], [8, 6, 4]); soll('G8b', [2 * 8, 4 * 6], [16, 24])
soll('Punkte', 4 + 3 + 3 + 3 + 4 + 2 + 3 + 3, 25)

print('\n' + ('ALLE ZAHLEN STIMMEN' if not fehler else f'{fehler} ABWEICHUNG(EN)'))
sys.exit(1 if fehler else 0)
