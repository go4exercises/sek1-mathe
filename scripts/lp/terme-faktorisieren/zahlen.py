"""Rechnet jede feste Zahl und jeden Term des Leitprogramms Terme und Faktorisieren nach (Seite, Simulationen,
Clips, PDFs) — exakt, mit einem kleinen Polynomrechner (ganzzahlige Koeffizienten, ohne sympy).

  python3 scripts/lp/terme-faktorisieren/zahlen.py      # Exit 1 bei einer Abweichung

soll(name, links, rechts): beide Seiten gleich (Terme: expand(links − rechts) = 0).
falsch(name, falscher, richtiger): Ein Fehlerbeispiel muss wirklich vom richtigen abweichen (HOWTO §15).
"""
import sys
from math import gcd


class P:
    """Polynom in x, y, a mit ganzen Koeffizienten: {(ex, ey, ea): k}."""
    def __init__(self, d=None):
        self.d = {k: v for k, v in (d or {}).items() if v}
    @staticmethod
    def von(w):
        return w if isinstance(w, P) else P({(0, 0, 0): w})
    def __add__(s, o):
        o = P.von(o); d = dict(s.d)
        for k, v in o.d.items():
            d[k] = d.get(k, 0) + v
        return P(d)
    __radd__ = __add__
    def __neg__(s):
        return P({k: -v for k, v in s.d.items()})
    def __sub__(s, o):
        return s + (-P.von(o))
    def __rsub__(s, o):
        return P.von(o) - s
    def __mul__(s, o):
        o = P.von(o); d = {}
        for k1, v1 in s.d.items():
            for k2, v2 in o.d.items():
                k = tuple(i + j for i, j in zip(k1, k2)); d[k] = d.get(k, 0) + v1 * v2
        return P(d)
    __rmul__ = __mul__
    def __pow__(s, n):
        r = P.von(1)
        for _ in range(n):
            r = r * s
        return r
    def subs(s, var, w):
        i = {'x': 0, 'y': 1, 'a': 2}[var]; d = {}
        for k, v in s.d.items():
            k2 = list(k); f = w ** k2[i]; k2[i] = 0; d[tuple(k2)] = d.get(tuple(k2), 0) + v * f
        r = P(d)
        return r.d.get((0, 0, 0), 0) if all(k == (0, 0, 0) for k in r.d) else r
    def __repr__(s):
        return ' + '.join(f"{v}·x^{k[0]}y^{k[1]}a^{k[2]}" for k, v in sorted(s.d.items())) or '0'


x, y, a = P({(1, 0, 0): 1}), P({(0, 1, 0): 1}), P({(0, 0, 1): 1})
fehler = 0


def gleich(l, r):
    if isinstance(l, P) or isinstance(r, P):
        return (P.von(l) - P.von(r)).d == {}
    return l == r


def soll(name, l, r):
    global fehler
    ok = gleich(l, r)
    fehler += not ok
    print(('ok   ' if ok else 'FALSCH'), name, '|', l, '=', r)


def falsch(name, f, r):
    global fehler
    ok = not gleich(f, r)
    fehler += not ok
    print(('ok   ' if ok else 'FALSCH'), 'Fehlerbeispiel', name, '|', f, '≠', r)


# ---- Vortest
soll('0a', [(-3) * (-4), -2 * 5, -7 + 3, -4 - 6] == [12, -10, -4, -10], True)
soll('0b', [3 * (4 + 5), 3 * 4 + 3 * 5], [27, 27])
soll('0c x·x', x * x, x**2); soll('0c 3x·2x', 3 * x * 2 * x, 6 * x**2); soll('0c (−2x)·5', -2 * x * 5, -10 * x)
soll('0d', (2 * x**2 - x).subs('x', 3), 15)
soll('0e', [gcd(12, 18), gcd(8, 20)], [6, 4])

# ---- Kapitel 1: Festhalten / Clip
soll('F1 3x+5x', 3 * x + 5 * x, 8 * x)
soll('F1 Minus vor Klammer', 7 * x - (2 * x - 5), 5 * x + 5)
soll('F1 3(2x−4)', 3 * (2 * x - 4), 6 * x - 12); soll('F1 −2(x−3)', -2 * (x - 3), -2 * x + 6)
soll('F1 verschachtelt', 4 * x - (2 * x - 3 * (1 - x)), 3 - x)
soll('F1 Zwischen', 2 * x - 3 * (1 - x), 5 * x - 3)
falsch('F1 −(a−b) = −a−b', 7 * x - 2 * x - 5, 5 * x + 5)
falsch('F1 3(x+4)=3x+4', 3 * x + 4, 3 * (x + 4))
falsch('F1 3x+2=5x', 5 * x, 3 * x + 2)
soll('Clip1 Kacheln 2x+4+3x−1', 2 * x + 4 + 3 * x - 1, 5 * x + 3)
soll('Clip1 Probe x=2', [(7 * x - (2 * x - 5)).subs('x', 2), (5 * x + 5).subs('x', 2)], [15, 15])
# Sim 1
soll('Sim1.1', 3 * x + 2 - x + 4, 2 * x + 6); soll('Sim1.2', 2 * x - 5 + 4 * x + 1, 6 * x - 4)
soll('Sim1.3', 3 * (x + 2), 3 * x + 6); soll('Sim1.4', 2 * (2 * x - 1) + x, 5 * x - 2); soll('Sim1.5', 4 * x - (x + 3), 3 * x - 3)
# Aufgaben 1
soll('1a', 5 * a + 3 - 2 * a + 7, 3 * a + 10); soll('1a2', x**2 + 4 * x - 2 * x**2 + x, -x**2 + 5 * x)
soll('1b', 4 * (3 * x - 2), 12 * x - 8); soll('1b2', -3 * (2 - x), -6 + 3 * x)
soll('1c', 6 * x - (4 - 2 * x) + 3 * (x - 1), 11 * x - 7)
soll('1d', 2 * x - (x - 2 * (3 - x)), -x + 6); soll('1d innen', x - 2 * (3 - x), 3 * x - 6)
falsch('1e Ben', 5 * x - 5, 8 * x - (3 * x - 5)); soll('1e', 8 * x - (3 * x - 5), 5 * x + 5)
soll('1e Probe x=1', [(8 * x - (3 * x - 5)).subs('x', 1), (5 * x - 5).subs('x', 1)], [10, 0])
soll('1f x=1 gleich', [(3 * x + 2).subs('x', 1), (5 * x).subs('x', 1)], [5, 5]); soll('1f x=2', [(3 * x + 2).subs('x', 2), (5 * x).subs('x', 2)], [8, 10])

# ---- Kapitel 2
soll('F2 (x+2)(x+3)', (x + 2) * (x + 3), x**2 + 5 * x + 6)
soll('F2 (3x−2)(x+4)', (3 * x - 2) * (x + 4), 3 * x**2 + 10 * x - 8)
falsch('F2 x²+6', x**2 + 6, (x + 2) * (x + 3))
soll('F2 Probe x=1', [((x + 2) * (x + 3)).subs('x', 1), (x**2 + 5 * x + 6).subs('x', 1)], [12, 12])
# Sim 2
soll('Sim2.1', (x + 3) * (x + 1), x**2 + 4 * x + 3)
soll('Sim2.2', (x + 4) * (x - 1), x**2 + 3 * x - 4); soll('Sim2.4', (x + 4) * (x - 3), x**2 + x - 12)
soll('Sim2.5', (x - 2) * (x - 5), x**2 - 7 * x + 10)
# Aufgaben 2
soll('2a', (x + 4) * (x + 5), x**2 + 9 * x + 20); soll('2b', (2 * x - 3) * (x + 6), 2 * x**2 + 9 * x - 18)
soll('2c', (a - 4) * (a - 7), a**2 - 11 * a + 28)
falsch('2d Lara', x**2 - 10, (x + 5) * (x - 2)); soll('2d', (x + 5) * (x - 2), x**2 + 3 * x - 10)
soll('2e', (x + 1) * (x + 4), x**2 + 5 * x + 4); soll('2f', (x + 3) * (x - 3), x**2 - 9)

# ---- Kapitel 3
soll('F3 (x+4)²', (x + 4)**2, x**2 + 8 * x + 16); soll('F3 (2y−3)²', (2 * y - 3)**2, 4 * y**2 - 12 * y + 9)
soll('F3 (5+x)(5−x)', (5 + x) * (5 - x), 25 - x**2); soll('F3 (3+4)²', (3 + 4)**2, 49); soll('F3 3²+4²', 3**2 + 4**2, 25)
# Sim 3
soll('Sim3.1 (5+2)²', [(5 + 2)**2, 25 + 20 + 4], [49, 49])
soll('Sim3.2 a+b=8, a²+b²=34', [5 + 3, 5**2 + 3**2, 2 * 5 * 3], [8, 34, 30])
soll('Sim3.2 einzig', [(p, q) for p in range(2, 9) for q in range(1, 5) if q < p and (p + q)**2 == 64 and p * p + q * q == 34], [(5, 3)])
soll('Sim3.3 (7−4)²', (7 - 4)**2, 9); soll('Sim3.3 einzig', [q for q in range(1, 5) if (7 - q)**2 == 9], [4])
soll('Sim3.4 a²−b²=24', [(p, q) for p in range(2, 9) for q in range(1, 5) if q < p and p * p - q * q == 24], [(5, 1)])
# Aufgaben 3
soll('3a', (x + 6)**2, x**2 + 12 * x + 36); soll('3a2', (x - 1)**2, x**2 - 2 * x + 1)
soll('3b', (3 * a - 2)**2, 9 * a**2 - 12 * a + 4)
soll('3c', (x + 7) * (x - 7), x**2 - 49); soll('3c2', (4 - y) * (4 + y), 16 - y**2)
falsch('3d Tom', x**2 + 25, (x + 5)**2); soll('3d Probe', [((x + 5)**2).subs('x', 1), (x**2 + 25).subs('x', 1)], [36, 26])
soll('3e', [21**2, 400 + 40 + 1, 19 * 21, 400 - 1], [441, 441, 399, 399])

# ---- Kapitel 4
soll('F4 6a²−9a', 3 * a * (2 * a - 3), 6 * a**2 - 9 * a); soll('F4 ggT', gcd(6, 9), 3)
falsch('F4 a(6a−9) unvollständig?', a * (6 * a - 9), 0)       # gleichwertig, aber Faktor 3 bleibt (siehe Seite)
soll('F4 a(6a−9) gleichwertig', a * (6 * a - 9), 6 * a**2 - 9 * a)
soll('F4 y²−10y+25', (y - 5)**2, y**2 - 10 * y + 25); soll('F4 9y²−25', (3 * y - 5) * (3 * y + 5), 9 * y**2 - 25)
soll('F4 x²−7x+12', (x - 3) * (x - 4), x**2 - 7 * x + 12); soll('F4 Paar', [(-3) * (-4), -3 + -4], [12, -7])
falsch('F4 (x+3)(x+4)', (x + 3) * (x + 4), x**2 - 7 * x + 12)
# Sim 4
soll('Sim4.1', (x + 2) * (x + 4), x**2 + 6 * x + 8); soll('Sim4.2', (x - 3) * (x - 5), x**2 - 8 * x + 15)
soll('Sim4.3', (x + 5) * (x - 3), x**2 + 2 * x - 15); soll('Sim4.4', (x - 3)**2, x**2 - 6 * x + 9); soll('Sim4.5', (x + 4) * (x - 4), x**2 - 16)
# Aufgaben 4
soll('4a', 4 * (2 * x + 3), 8 * x + 12); soll('4a2', 5 * y * (y - 3), 5 * y**2 - 15 * y)
soll('4b', (x + 7)**2, x**2 + 14 * x + 49); soll('4b2', (2 * a - 1) * (2 * a + 1), 4 * a**2 - 1)
soll('4c', (x + 2) * (x + 7), x**2 + 9 * x + 14); soll('4c2', (x - 5) * (x + 2), x**2 - 3 * x - 10)
soll('4d', (x - 3) * (x + 3), x**2 - 9)
soll('4e', 2 * (x - 3) * (x + 3), 2 * x**2 - 18); soll('4e Zwischen', 2 * (x**2 - 9), 2 * x**2 - 18)
soll('F4 5x²−20', 5 * (x - 2) * (x + 2), 5 * x**2 - 20); soll('F4 x²−25', (x - 5) * (x + 5), x**2 - 25)
soll('4f keine ganzen m, n', [(m, n) for m in range(-20, 21) for n in range(-20, 21) if m * n == 4 and m + n == 0], [])

# ---- Clips: Kontrollfragen
soll('K1F1', 4 * y - 7 + 2 * y + 3, 6 * y - 4); falsch('K1F1 2y', 2 * y, 6 * y - 4); falsch('K1F1 6y−10', 6 * y - 10, 6 * y - 4)
soll('K1F2', -(3 * x - 8), -3 * x + 8); falsch('K1F2 a', -3 * x - 8, -3 * x + 8); falsch('K1F2 b', 3 * x - 8, -3 * x + 8)
soll('K1F3', 5 * (2 * a - 3), 10 * a - 15); falsch('K1F3 a', 10 * a - 3, 10 * a - 15); falsch('K1F3 b', 2 * a - 15, 10 * a - 15)
soll('K1F4 nicht gleich', gleich(2 * x + 3 * x**2, 5 * x**3), False)
soll('K1F5', x - (4 - 3 * x), 4 * x - 4); falsch('K1F5 a', -2 * x - 4, 4 * x - 4); soll('K1F5 a als Fehler', x - 4 - 3 * x, -2 * x - 4)
falsch('K1F5 b', 4 * x + 4, 4 * x - 4)
soll('K2F1', (x + 6) * (x + 1), x**2 + 7 * x + 6); falsch('K2F1 a', x**2 + 6, x**2 + 7 * x + 6); falsch('K2F1 b', x**2 + 6 * x + 7, x**2 + 7 * x + 6)
soll('K2F2', ((x - 3) * (x + 5)).subs('x', 0), -15)
soll('K2F3', (2 * a + 1) * (a - 4), 2 * a**2 - 7 * a - 4); falsch('K2F3 a', 2 * a**2 - 4, 2 * a**2 - 7 * a - 4)
falsch('K2F3 b', 2 * a**2 + 9 * a - 4, 2 * a**2 - 7 * a - 4)
soll('K2F4', (x + 5) * (x + 2), x**2 + 7 * x + 10)
soll('K2F5', [((x + 2) * (x - 1)).subs('x', 3), (x**2 + x - 2).subs('x', 3)], [10, 10]); soll('K2F5 allg', (x + 2) * (x - 1), x**2 + x - 2)
soll('K3F1', (x + 9)**2, x**2 + 18 * x + 81); falsch('K3F1 a', x**2 + 81, (x + 9)**2); falsch('K3F1 b', x**2 + 9 * x + 81, (x + 9)**2)
soll('K3F2', (y - 6)**2, y**2 - 12 * y + 36); falsch('K3F2 a', y**2 - 36, (y - 6)**2); falsch('K3F2 b', y**2 + 12 * y + 36, (y - 6)**2)
soll('K3F3', (2 * x + 5) * (2 * x - 5), 4 * x**2 - 25); falsch('K3F3 a', 2 * x**2 - 25, 4 * x**2 - 25)
soll('K3F4', (3 * y)**2, 9 * y**2)
soll('K3F5', [41**2, (40 + 1)**2, 1600 + 1, 1600 + 40 + 1], [1681, 1681, 1601, 1641])
soll('K4F1', 7 * (2 * x - 3), 14 * x - 21); falsch('K4F1 a', 7 * (2 * x - 21), 14 * x - 21)
soll('K4F2', (x - 9) * (x + 9), x**2 - 81); falsch('K4F2 a', (x - 9)**2, x**2 - 81)
soll('K4F3', (x + 5)**2, x**2 + 10 * x + 25); falsch('K4F3 a', (x + 5) * (x - 5), x**2 + 10 * x + 25)
soll('K4F4', (x + 4) * (x - 3), x**2 + x - 12); falsch('K4F4 a', (x - 4) * (x + 3), x**2 + x - 12); falsch('K4F4 b', (x + 6) * (x - 2), x**2 + x - 12)
soll('K4F5 ist Summe', 5 * a * (a + 2) + 1, 5 * a**2 + 10 * a + 1)

# ---- Bewertungspaket: typische Fehler
soll('BP G1 Vorzeichen', 5 * x - 6 * x - 8 + x - 1, -9); soll('BP G1 nur erstes', 5 * x - 6 * x - 4 + x - 1, -5)
soll('BP G2 Minus nur erstes', 3 * a**2 - a**2 - 2 * a - 2 * a, 2 * a**2 - 4 * a)
soll('BP G3 Vorzeichen', 2 * x**2 + 6 * x + 5 * x - 15, 2 * x**2 + 11 * x - 15); falsch('BP G3', 2 * x**2 + 11 * x - 15, (2 * x + 5) * (x - 3))
falsch('BP G4 a', 9 * y**2 - 12 * y + 16, (3 * y - 4)**2); falsch('BP G4 b', 9 * y**2 + 24 * y + 16, (3 * y - 4)**2)
soll('BP G5', [30**2 - 1, 900 + 1, 31**2], [899, 901, 961])
for fak in [6 * (2 * a**2 + 3 * a), a * (12 * a + 18), 3 * a * (4 * a + 6), 2 * a * (6 * a + 9)]:
    soll('BP G6 gleichwertig', fak, 12 * a**2 + 18 * a)
falsch('BP G6 Inhalt falsch', 6 * a * (2 * a + 18), 12 * a**2 + 18 * a)
soll('BP G7 vertauscht', (x + 6) * (x - 4), x**2 + 2 * x - 24); soll('BP G7 Summe/Produkt', (x - 8) * (x + 3), x**2 - 5 * x - 24)
soll('BP G8 gleichwertig', (3 * x - 6) * (x + 2), 3 * x**2 - 12); falsch('BP G8 Binom', 3 * (x - 2)**2, 3 * x**2 - 12)
soll('BP G9 (x+3)(x−3)', (x + 3) * (x - 3), x**2 - 9)
# ---- Clips (Einführung, Kontrolle) zusätzlich
soll('C1 3(2x−4) Kacheln', [6, -12], [3 * 2, 3 * -4]); soll('C1 x=2 3x+2 / 5x', [(3 * x + 2).subs('x', 2), (5 * x).subs('x', 2)], [8, 10])
soll('C2 Probe x=1', [((x + 2) * (x + 3)).subs('x', 1), (x**2 + 6).subs('x', 1)], [12, 7])
soll('C3 3²+4²', [(3 + 4)**2, 9 + 16, 2 * 12], [49, 25, 24]); soll('C3 (2y−3)²', (2 * y - 3)**2, 4 * y**2 - 12 * y + 9)
soll('C3 51²', [51**2, 2500 + 100 + 1, 49 * 51, 2500 - 1], [2601, 2601, 2499, 2499])
soll('C4 x²−25', (x - 5) * (x + 5), x**2 - 25); soll('C4 5x²−20', 5 * (x - 2) * (x + 2), 5 * x**2 - 20)
soll('C4 Paare 12', sorted((p, 12 // p) for p in (1, 2, 3, -1, -2, -3) if p * (12 // p) == 12 and p + 12 // p == -7), [(-3, -4)])
soll('K1F4 Probe x=2', [(2 * x + 3 * x**2).subs('x', 2), 5 * 8], [16, 40])
soll('K2F2', (x - 3) * (x + 5), x**2 + 2 * x - 15); falsch('K2F1 c', x**2 + 6 * x + 7, (x + 6) * (x + 1))
falsch('K3F3 b', 4 * x**2 - 20 * x - 25, (2 * x + 5) * (2 * x - 5)); falsch('K3F4', 3 * y**2, (3 * y)**2)
falsch('K4F1 b', 2 * (7 * x - 10), 14 * x - 21); soll('K4F2 b', (x - 81) * (x + 1), x**2 - 80 * x - 81)
soll('K4F3 b', (x + 10) * (x + 25), x**2 + 35 * x + 250)
soll('V1', (x + 1)**2 - x**2, 2 * x + 1); soll('V2', [45**2, 100 * 4 * 5 + 25, 35**2], [2025, 2025, 1225])
soll('V3', [(x**2 + 5 * x + 6).subs('x', 10), 12 * 13], [156, 156])

# ---- Gesamttest
soll('G1', 5 * x - 2 * (3 * x - 4) + (x - 1), 7)
soll('G2', 3 * a**2 - (a**2 - 2 * a) - 2 * a, 2 * a**2)
soll('G3', (2 * x + 5) * (x - 3), 2 * x**2 - x - 15); falsch('G3 Mitte fehlt', 2 * x**2 - 15, 2 * x**2 - x - 15)
soll('G4', (3 * y - 4)**2, 9 * y**2 - 24 * y + 16); falsch('G4 Mitte fehlt', 9 * y**2 + 16, (3 * y - 4)**2)
falsch('G4 3y² statt 9y²', 3 * y**2 - 24 * y + 16, (3 * y - 4)**2)
soll('G5', [31 * 29, 900 - 1], [899, 899])
soll('G6', 6 * a * (2 * a + 3), 12 * a**2 + 18 * a); soll('G6 ggT', gcd(12, 18), 6)
soll('G7', (x - 6) * (x + 4), x**2 - 2 * x - 24); falsch('G7 Vorzeichen', (x + 6) * (x - 4), x**2 - 2 * x - 24)
soll('G8', 3 * (x - 2) * (x + 2), 3 * x**2 - 12)
soll('G9', (x + 3)**2, x**2 + 6 * x + 9); soll('G9 Summe gleichwertig', x * (x + 6) + 9, x**2 + 6 * x + 9)
soll('Punkte', 3 + 2 + 3 + 3 + 2 + 3 + 3 + 3 + 3, 25)

print('\n' + ('ALLE ZAHLEN STIMMEN' if not fehler else f'{fehler} ABWEICHUNG(EN)'))
sys.exit(1 if fehler else 0)
