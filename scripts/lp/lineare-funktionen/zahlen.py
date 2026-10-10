"""Rechnet jede feste Zahl des Leitprogramms «Lineare Funktionen» nach (Seite, Simulationen, Clips, PDFs) —
exakt mit Fraction.

  python3 scripts/lp/lineare-funktionen/zahlen.py      # Exit 1 bei einer Abweichung

gerade(name, m, b, punkte): die Gerade y = m·x + b geht durch alle Punkte.
soll(name, ist, wert): Gleichheit. falsch(name, a, b): Ein Fehlerbeispiel weicht wirklich ab.
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


def leer(v0, rate):
    return F(v0) / F(rate)


# ---- Vortest
soll('0b', [y(4, -7, 3), y(4, -7, -2)], [5, -15])
soll('0c', [F(-6, 3), F(11 + 4, 5)], [-2, 3])
soll('0d', [F(9 - 1, 6 - 2), F(2 - 8, 4 - 1)], [2, -2]); soll('0f', [F(3, 4) * 8, F(6) / F(3, 4)], [6, 8]); soll('Kurz wiederholt', [F(2, 3) * 6, F(4) / F(2, 3)], [4, 6])
soll('0e', [2 * k for k in range(4)], [0, 2, 4, 6])

# ---- Kapitel 1
gerade('F1 Tank', 15, 200, [(0, 200), (1, 215), (2, 230), (10, 350)])
soll('F1 rückwärts 350', F(350 - 200, 15), 10)
falsch('F1 vertauscht x=2', y(200, 15, 2), y(15, 200, 2)); soll('F1 vertauscht x=1 gleich (Probe mit 1 verdeckt den Fehler)', y(200, 15, 1), y(15, 200, 1))
gerade('Clip1 Tank', 15, 200, [(4, 260)]); soll('Clip1 Fallen', [200 + 15, 15 * 4 * 200 // 15], [215, 800])
# Sim 1
gerade('Sim1.4', 20, 20, [(0, 20), (4, 100)]); soll('Sim1.5', durch((3, 45), (5, 65)), (10, 15))
# Aufgaben 1
gerade('1a Velo', 3, 8, [(5, 23), (8, 32)])
soll('1b', [y(-2, 5, x) for x in (-1, 0, 1, 2, 3)], [7, 5, 3, 1, -1])
soll('1c linear', [4 + 3 * x for x in range(4)], [4, 7, 10, 13]); soll('1c nicht', [8 // 4 - 2 * 0, 2 - 1, 4 - 2, 8 - 4], [2, 1, 2, 4])
falsch('1d Lea x=2', y(50, -4, 2), y(-4, 50, 2)); gerade('1d', -4, 50, [(0, 50), (1, 46)])
gerade('1e Ballon', 40, 300, [(20, 1100)])

# ---- Kapitel 2
soll('F2 m', steigung((1, 2), (4, 8)), 2); falsch('F2 vertauscht', F(3, 6), 2)
soll('F2 gemischt', F(8 - 2, 1 - 4), -2)
soll('Clip2 Fallen', [F(3, 6), 8 - 2], [F(1, 2), 6])
soll('2a', steigung((2, 3), (6, 11)), 2); soll('2b', steigung((-1, 4), (3, -4)), -2)
soll('2c Bild', steigung((0, 1), (3, 3)), F(2, 3))
soll('2d Tim', [F(5 - 1, 2 - 4), steigung((2, 1), (4, 5))], [-2, 2])
soll('2e Reihenfolge |m|', sorted([3, -4, F(1, 2), -1], key=lambda m: -abs(m)), [-4, 3, -1, F(1, 2)])
# Sim 2 (Steigung messen)
soll('Sim2 Ziele', [F(2), F(-1), F(1, 2), F(-3, 2), F(0)], [2, -1, F(1, 2), F(-3, 2), 0])

# ---- Kapitel 3
gerade('F3 y=2/3x−1', F(2, 3), -1, [(0, -1), (3, 1), (6, 3), (F(3, 2), 0)])
soll('F3 Nullstelle', F(1) / F(2, 3), F(3, 2))
gerade('Clip3', F(2, 3), -1, [(6, 3)])
# Sim 3
soll('Sim3.2', durch((0, -1), (2, 3)), (2, -1)); soll('Sim3.4', durch((2, 0), (0, 4)), (-2, 4))
# Aufgaben 3
soll('3b A', y(2, -3, 4), 5); soll('3b B', y(2, -3, -2), -7)
soll('3c', [F(6, 3), F(-2) / F(-1, 2)], [2, 4])
soll('3e Schnitt', [y(2, -3, 2), y(F(-1, 2), 2, 2)], [1, 1])

# ---- Kapitel 4
soll('F4 zwei Punkte', durch((2, 5), (6, 7)), (F(1, 2), 4)); soll('F4 Probe', y(F(1, 2), 4, 6), 7)
falsch('F4 Fehler b=5', y(F(1, 2), 5, 2), 5)
soll('F4 Infusion leer', leer(500, 2), 250); soll('F4 nach 100', 500 - 2 * 100, 300); soll('F4 Wechsel leer', 100 + leer(300, 1), 400)
# Sim 4
soll('Sim4.1', leer(400, 4), 100); soll('Sim4.2', 600 - 3 * 120, 240); soll('Sim4.3', 60 + leer(500 - 5 * 60, 2), 160)
soll('Sim4.4', F(900, 300), 3); soll('Sim4.5', 100 + leer(800 - 4 * 100, 8), 150)
# Aufgaben 4
soll('4a Bild', durch((0, -2), (4, 0)), (F(1, 2), -2))
soll('4b', durch((1, 3), (3, 7)), (2, 1)); soll('4c', durch((-2, 6), (4, 3)), (F(-1, 2), 5))
soll('4d Max', durch((3, 4), (5, 8)), (2, -2)); soll('4d Max b=4', y(2, 4, 3), 10)
soll('4e Tank', [leer(240, 6), 240 - 6 * 10, 10 + leer(180, 4)], [40, 180, 55]); soll('4e Häuschen', [F(240, 40), F(10, 10), F(180, 40), F(55, 10)], [6, 1, F(9, 2), F(11, 2)])

# ---- Clips: Kontrollfragen
gerade('K1F1', 5, 80, [(0, 80), (1, 85)]); soll('K1F2', y(-3, 20, 4), 8); soll('K1F3', F(45 - 9, 6), 6)
soll('K1F4', [2 + 3 * x for x in range(4)], [2, 5, 8, 11])
soll('K2F1', steigung((2, 1), (5, 7)), 2); soll('K2F2', steigung((-1, 3), (1, -1)), -2); soll('K2F3', F(-1, 3), F(-1, 3))
soll('K3F1', y(F(3, 4), 1, 4), 4); falsch('K3F1 b', y(F(3, 4), 1, 3), 5)
soll('K3F2', y(3, -1, 2), 5); soll('K3F3', F(8, 2), 4)
gerade('K3F4 Bild', 1, -2, [(0, -2), (2, 0)])
gerade('K4F1 Bild', F(2, 3), 2, [(0, 2), (3, 4)]); falsch('K4F1 3/2x+2', y(F(3, 2), 2, 3), 4); falsch('K4F1 b=4', y(F(2, 3), 4, 0), 2); soll('K4F2', durch((1, 4), (3, 10)), (3, 1))
soll('K4F3', leer(400, 5), 80); gerade('K4F5', -3, 450, [(0, 450), (150, 0)])

soll('Clip1 abnehmend leer', F(200, 20), 10); gerade('K1F5 Kerze', -2, 24, [(0, 24), (12, 0)])
falsch('K1F2 ohne Minus', 3 * 4 + 20, 8); falsch('K1F2 ohne x', -3 + 20, 8); soll('K1F3 Fallen', [6 * 45 + 9, F(45, 6)], [279, F(15, 2)])
falsch('K1F4 2x+3 bei 0', y(2, 3, 0), 2); falsch('K1F4 3x+5 bei 0', y(3, 5, 0), 2)
gerade('Clip2 Gerade', 2, 0, [(1, 2), (4, 8), (2, 4)]); soll('Clip2 Fallen Vorhersage', [F(3, 6), 6], [F(1, 2), 6])
gerade('K2F1 Bild', 2, -3, [(2, 1), (5, 7)]); gerade('K2F2 Bild', -2, 1, [(-1, 3), (1, -1)])
gerade('K2F3 Bild', F(-1, 3), 2, [(0, 2), (3, 1), (6, 0)]); soll('K2F5', F(-3, 2), F(-3, 2))
gerade('Clip3 Dreieck', F(2, 3), -1, [(3, 1)]); falsch('Clip3 (2|2)', y(F(2, 3), -1, 2), 2); falsch('Clip3 (3|2)', y(F(2, 3), -1, 3), 2)
falsch('K3F1 (4|3)', y(F(3, 4), 1, 4), 3); soll('K3F3 Fallen', [y(2, -8, 0), y(2, -8, -4), y(2, -8, 2)], [-8, -16, -4])
gerade('K3F4 B', 1, -2, [(0, -2), (2, 0)]); soll('K3F4 Namen bei A(1.9|4.8), B(3.9|0.8), C(−1.6|−1) neben A, B, C', [y(1, 2, F(19, 10)) - F(48, 10), y(1, -2, F(39, 10)) - F(8, 10), y(-1, -2, F(-16, 10)) + 1], [F(-9, 10), F(11, 10), F(3, 5)])
gerade('K3F5', -2, 3, [(0, 3), (1, 1)]); falsch('K3F5 (1|5)', y(-2, 3, 1), 5); falsch('K3F5 (2|2)', y(-2, 3, 2), 2)
gerade('Clip4 Ablesen', F(-1, 2), 3, [(0, 3), (2, 2)])
falsch('K4F2 3x+4', y(3, 4, 1), 4); falsch('K4F2 2x+2', y(2, 2, 3), 10)
soll('K4F4', 300 - 3 * 50, 150); soll('K4F4 danach leer', 50 + leer(150, 1), 200)

# ---- Gesamttest (neue Zahlen nach der Prüfung vom 10.10.2026)
soll('G1', [y(-3, 12, -2), F(-6 - 12, -3)], [18, 6]); soll('G1 Fehler', [F(-6 + 12), y(-3, 12, -6)], [6, 30])
gerade('G2 Akku', -6, 80, [(0, 80), (1, 74), (2, 68), (5, 50), (10, 20)]); soll('G2 Fehler', [y(80, -6, 5), y(6, 80, 5)], [394, 110])
soll('G3', steigung((-2, 1), (4, 4)), F(1, 2)); soll('G3 Fehler', [F(4 - 1, -2 - 4), F(4 - (-2), 4 - 1), F(3, 2)], [F(-1, 2), 2, F(3, 2)])
gerade('G4', F(-2, 3), 3, [(0, 3), (3, 1), (6, -1), (F(9, 2), 0), (-2, F(13, 3)), (9, -3)]); falsch('G4 hinauf (3|5)', y(F(-2, 3), 3, 3), 5)
gerade('G5 Bild', F(-3, 4), 1, [(0, 1), (4, -2), (-2, F(5, 2)), (6, F(-7, 2))])
gerade('G6', -5, 800, [(0, 800), (160, 0)]); soll('G6 Zellen (40 min, 100 ml)', [F(160, 40), F(800, 100)], [4, 8])
soll('G7', durch((2, -1), (6, 5)), (F(3, 2), -4)); soll('G7 Probe Q', y(F(3, 2), -4, 6), 5); soll('G7 umgedreht', F(-1) - F(2, 3) * 2, F(-7, 3))
soll('G8', [700 - 6 * 50, 50 + leer(400, 2)], [400, 250]); soll('G8 Fehler', [50 + leer(700, 2), leer(700, 6)], [400, F(350, 3)])
soll('G8 Zellen', [F(700, 100), F(50, 50), F(400, 100), F(250, 50)], [7, 1, 4, 5])
soll('Punkte', 3 + 3 + 3 + 4 + 3 + 3 + 3 + 3, 25); soll('Teile', [3 + 3, 3 + 4 + 3, 3 + 3 + 3], [6, 10, 9])

print('\n' + ('ALLE ZAHLEN STIMMEN' if not fehler else f'{fehler} ABWEICHUNG(EN)'))
sys.exit(1 if fehler else 0)
