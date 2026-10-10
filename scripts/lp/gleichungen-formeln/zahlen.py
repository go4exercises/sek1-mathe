"""Rechnet jede feste Zahl und jeden Term des Leitprogramms «Bruchterme, Gleichungen und Formeln» nach
(Seite, Simulationen, Clips, PDFs) — exakt mit Fraction.

  python3 scripts/lp/gleichungen-formeln/zahlen.py      # Exit 1 bei einer Abweichung

term(name, f, g): f und g gleichwertig (an 40 rationalen Stellen gleich, Pole übersprungen).
falsch(name, f, g): Ein Fehlerbeispiel weicht wirklich ab.
loes(name, gl, x0): x0 löst die Gleichung gl(x) = (links, rechts).
formel(name, f, g, namen): Formeln in mehreren Grössen gleichwertig (an 30 zufälligen positiven Stellen).
"""
import random
import sys
from fractions import Fraction as F
from math import gcd

fehler = 0
STELLEN = [F(k, 7) for k in range(-20, 21)] + [F(k, 3) for k in range(-9, 10)]


def werte(f):
    out = {}
    for x in STELLEN:
        try:
            out[x] = F(f(x))
        except ZeroDivisionError:
            pass
    return out


def melde(ok, text):
    global fehler
    fehler += not ok
    print(('ok    ' if ok else 'FALSCH'), text)


def term(name, f, g):
    a, b = werte(f), werte(g)
    gemeinsam = [x for x in a if x in b]
    melde(len(gemeinsam) > 20 and all(a[x] == b[x] for x in gemeinsam), name)


def falsch(name, f, g):
    a, b = werte(f), werte(g)
    melde(any(a[x] != b[x] for x in a if x in b), 'Fehlerbeispiel ' + name)


def soll(name, ist, wert):
    melde(ist == wert, '%s | %s = %s' % (name, ist, wert))


def loes(name, gl, x0, keine_andere=True):
    l, r = gl(F(x0))
    ok = l == r
    if keine_andere:          # lineare Gleichung: genau eine Lösung → an einer anderen Stelle ungleich
        l2, r2 = gl(F(x0) + 1)
        ok = ok and l2 != r2
    melde(ok, '%s | x = %s' % (name, x0))


def alle(name, gl):
    melde(all(gl(x)[0] == gl(x)[1] for x in STELLEN), name + ' | L = Q')


def keine(name, gl):
    melde(all(gl(x)[0] != gl(x)[1] for x in STELLEN), name + ' | L = {}')


def formel(name, f, g, namen):
    rnd = random.Random(name)
    ok = True
    for _ in range(30):
        w = {n: F(rnd.randint(1, 60), rnd.randint(1, 7)) for n in namen}
        try:
            ok = ok and F(f(w)) == F(g(w))
        except ZeroDivisionError:
            pass
    melde(ok, 'Formel ' + name)


# ---- Vortest
soll('0a ggT', gcd(4, 12), 4); term('0a 4x−12', lambda x: 4 * x - 12, lambda x: 4 * (x - 3))
term('0a x²−49', lambda x: x * x - 49, lambda x: (x - 7) * (x + 7))
soll('0b', [F(18, 24), F(3 * 5, 5 * 7)], [F(3, 4), F(3, 7)])
soll('0c Nenner 0', 4 - 4, 0)
loes('0d', lambda x: (3 * x + 5, 20), 5)
soll('0e', 2 * 3 - (-4), 10)

# ---- Kapitel 1: Festhalten, Clip
term('F1 6x/(9x²)', lambda x: 6 * x / (9 * x * x), lambda x: F(2) / (3 * x))
term('F1 (x²−9)/(2x+6)', lambda x: (x * x - 9) / (2 * x + 6), lambda x: (x - 3) / 2)
term('F1 (x²+4x+4)/(x²−4)', lambda x: (x * x + 4 * x + 4) / (x * x - 4), lambda x: (x + 2) / (x - 2))
falsch('F1 (x+3)/(x+5) ≠ 3/5', lambda x: (x + 3) / (x + 5), lambda x: F(3, 5))
soll('F1 Probe x=1', [F(1 + 3, 1 + 5), F(3, 5)], [F(2, 3), F(3, 5)])
term('F1 (x−3)/(3−x)', lambda x: (x - 3) / (3 - x), lambda x: -1)
soll('Clip1 12/18', F(12, 18), F(2, 3))
# Sim 1 (Faktoren, schon zerlegt)
term('Sim1.1 6x/(15x)', lambda x: 6 * x / (15 * x), lambda x: F(2, 5))
term('Sim1.2 4(x+1)/(6(x+1))', lambda x: 4 * (x + 1) / (6 * (x + 1)), lambda x: F(2, 3))
term('Sim1.3 x(x−2)/(3x)', lambda x: x * (x - 2) / (3 * x), lambda x: (x - 2) / 3)
term('Sim1.4 (x+1)(x−1)/((x−1)(x+4))', lambda x: (x + 1) * (x - 1) / ((x - 1) * (x + 4)), lambda x: (x + 1) / (x + 4))
falsch('Sim1.5 (x+2)/(x+6) nicht kürzbar', lambda x: (x + 2) / (x + 6), lambda x: F(1, 3))
# Aufgaben 1
term('1a 12a²/(18a)', lambda a: 12 * a * a / (18 * a), lambda a: 2 * a / 3)
term('1b (5x−10)/(x−2)', lambda x: (5 * x - 10) / (x - 2), lambda x: 5)
term('1b (x²−16)/(x+4)', lambda x: (x * x - 16) / (x + 4), lambda x: x - 4)
term('1c (x²−6x+9)/(x²−9)', lambda x: (x * x - 6 * x + 9) / (x * x - 9), lambda x: (x - 3) / (x + 3))
falsch('1d Nina (x+6)/(x+2)=3', lambda x: (x + 6) / (x + 2), lambda x: 3)
soll('1d Probe x=1', [F(1 + 6, 1 + 2), F(3)], [F(7, 3), F(3)])
soll('1e Nennernullstellen x²−4x', [x for x in range(-10, 11) if x * x - 4 * x == 0], [0, 4])
term('1f (2−x)/(x−2)', lambda x: (2 - x) / (x - 2), lambda x: -1)

# ---- Kapitel 2
term('F2 mal', lambda x: (3 * x / 4) * (8 / (9 * x * x)), lambda x: F(2) / (3 * x))
term('F2 durch', lambda x: (5 / x) / (10 / (x * x)), lambda x: x / 2)
term('F2 5/x+2/x', lambda x: 5 / x + 2 / x, lambda x: 7 / x)
term('F2 1/x+1/(2x)', lambda x: 1 / x + 1 / (2 * x), lambda x: F(3) / (2 * x))
term('F2 2/x−1/(x+1)', lambda x: 2 / x - 1 / (x + 1), lambda x: (x + 2) / (x * (x + 1)))
falsch('F2 1/x+1/2 ≠ 2/(x+2)', lambda x: 1 / x + F(1, 2), lambda x: 2 / (x + 2)); term('F2 1/x+1/2', lambda x: 1 / x + F(1, 2), lambda x: (2 + x) / (2 * x))
soll('F2 Probe x=2', [F(1, 2) + F(1, 2), F(2, 4)], [1, F(1, 2)])
soll('Clip4 Trapez Zahlen', [F(60, 5 + 7), F(60, 5) + 7], [5, 19])
term('F2 Minus vor Bruchstrich', lambda x: 1 - (x - 1) / x, lambda x: 1 / x)
falsch('F2 Minus vergessen', lambda x: (x - (x - 1)) / x, lambda x: (x - x - 1) / x)
# Sim 2: Hauptnenner
soll('Sim2 kgV', ['2x', '3x²', 'x(x+1)', '(x−1)(x+1)', '12x'], ['2x', '3x²', 'x(x+1)', '(x−1)(x+1)', '12x'])
# Aufgaben 2
term('2a', lambda x: (2 * x / 3) * (9 / (4 * x * x)), lambda x: F(3) / (2 * x))
term('2b', lambda x: (x * x - 1) / x * (3 * x) / (x + 1), lambda x: 3 * (x - 1))
term('2c', lambda a: F(3) / (2 * a) + F(5) / (6 * a), lambda a: F(7) / (3 * a))
term('2d', lambda x: 4 / x - 3 / (x + 2), lambda x: (x + 8) / (x * (x + 2)))
falsch('2e Tim 1/x+1/3=2/(x+3)', lambda x: 1 / x + F(1, 3), lambda x: 2 / (x + 3))
soll('2e Probe x=3', [F(1, 3) + F(1, 3), F(2, 6)], [F(2, 3), F(1, 3)])
term('2e richtig', lambda x: 1 / x + F(1, 3), lambda x: (3 + x) / (3 * x))

# ---- Kapitel 3
loes('F3 5x−7=2x+8', lambda x: (5 * x - 7, 2 * x + 8), 5); soll('F3 Probe', [5 * 5 - 7, 2 * 5 + 8], [18, 18])
alle('F3 3(x−2)−(x+4)=2x−10', lambda x: (3 * (x - 2) - (x + 4), 2 * x - 10))
keine('F3 2(x+1)=2x+5', lambda x: (2 * (x + 1), 2 * x + 5))
loes('F3 Brüche', lambda x: ((x + 1) / 3 - (x - 2) / 4, 1), 2)
term('F3 ·12', lambda x: 12 * ((x + 1) / 3 - (x - 2) / 4), lambda x: x + 10)
falsch('F3 Fehler −3(x−2)=−3x−6', lambda x: -3 * x - 6, lambda x: -3 * (x - 2))
# Sim 3
loes('Sim3.1 4x+3=x+15', lambda x: (4 * x + 3, x + 15), 4)
loes('Sim3.2 7x−2=3x+10', lambda x: (7 * x - 2, 3 * x + 10), 3)
loes('Sim3.3 2x+9=5x', lambda x: (2 * x + 9, 5 * x), 3)
keine('Sim3.4 3x+1=3x+4', lambda x: (3 * x + 1, 3 * x + 4))
loes('Sim3.5 6−2x=x−9', lambda x: (6 - 2 * x, x - 9), 5)
# Aufgaben 3
loes('3a', lambda x: (8 * x - 5, 3 * x + 20), 5)
loes('3b', lambda x: (4 * (x - 3), 2 * (x + 1)), 7)
loes('3c', lambda x: (x / 2 + x / 3, 10), 12)
loes('3d', lambda x: ((2 * x - 1) / 5, (x + 4) / 3), 23)
soll('3e Lea falsch', F(7, 3) * 3, 7); loes('3e Lea Gleichung', lambda x: (5 - x + 2, 2 * x), F(7, 3))
loes('3e richtig', lambda x: (5 - (x + 2), 2 * x), 1)
alle('3f a', lambda x: (2 * (x + 3), 2 * x + 6)); keine('3f b', lambda x: (2 * (x + 3), 2 * x + 3))

# ---- Kapitel 4
formel('F4 s=v·t', lambda w: w['s'] / w['v'], lambda w: w['s'] / w['v'], 'sv')
formel('F4 F=1.8C+32 → C', lambda w: (w['F'] - 32) / F(9, 5), lambda w: (w['F'] - 32) * F(5, 9), 'F')
soll('F4 212 °F', (212 - 32) / F(9, 5), 100)
formel('F4 Trapez h', lambda w: 2 * w['A'] / (w['a'] + w['c']),
       lambda w: w['A'] / ((w['a'] + w['c']) / 2), 'Aac')
formel('F4 Trapez Probe', lambda w: (w['a'] + w['c']) / 2 * (2 * w['A'] / (w['a'] + w['c'])), lambda w: w['A'], 'Aac')
falsch('F4 Fehler 2A/a + c', lambda c: F(2 * 30) / 5 + c, lambda c: F(2 * 30) / (5 + c))
# Sim 4 (Rückwärtskette)
formel('Sim4.1 t', lambda w: w['s'] / w['v'], lambda w: w['s'] / w['v'], 'sv')
formel('Sim4.2 R', lambda w: w['U'] / w['I'], lambda w: w['U'] / w['I'], 'UI')
formel('Sim4.3 x aus y=4x−5', lambda w: (w['y'] + 5) / 4, lambda w: (w['y'] + 5) / 4, 'y')
formel('Sim4.4 a aus A=a·b/2', lambda w: 2 * w['A'] / w['b'], lambda w: w['A'] / (w['b'] / 2), 'Ab')
formel('Sim4.5 b aus U=2(a+b)', lambda w: w['U'] / 2 - w['a'], lambda w: (w['U'] - 2 * w['a']) / 2, 'Ua')
# Aufgaben 4
formel('4a I=P/U', lambda w: w['P'] / w['U'], lambda w: w['P'] / w['U'], 'PU')
formel('4b h=2A/g', lambda w: 2 * w['A'] / w['g'], lambda w: w['A'] / (w['g'] / 2), 'Ag')
soll('4c Taxi', (31 - 6) / F(5, 2), 10)
soll('4d Umfang', F(24, 2) - 7, 5)
falsch('4e Max h=V−ab', lambda h: 60 - 3 * 4, lambda h: F(60, 3 * 4))
soll('4f Schrittmass', 63 - 2 * 18, 27); formel('4f h', lambda w: (63 - w['a']) / 2, lambda w: (63 - w['a']) / 2, 'a')

# ---- Clips: Kontrollfragen
term('K1F1', lambda x: 8 * x / (12 * x * x), lambda x: F(2) / (3 * x)); falsch('K1F1 b', lambda x: 2 * x / 3, lambda x: F(2) / (3 * x))
term('K1F2', lambda x: (x * x - 4) / (x + 2), lambda x: x - 2); falsch('K1F2 b', lambda x: x * x - 2, lambda x: x - 2)
soll('K1F3', [x for x in range(-10, 11) if x * (x + 5) == 0], [-5, 0])
falsch('K1F4 (x+7)/(x+1) ≠ 7', lambda x: (x + 7) / (x + 1), lambda x: 7)
term('K1F5', lambda x: (5 - x) / (x - 5), lambda x: -1)
term('K2F1', lambda x: (2 / x) * (x * x / 6), lambda x: x / 3)
term('K2F2', lambda x: (4 / x) / (2 / (x * x)), lambda x: 2 * x); falsch('K2F2 b', lambda x: 8 / x**3, lambda x: 2 * x)
term('K2F3', lambda x: 3 / x + 4 / x, lambda x: 7 / x); falsch('K2F3 b', lambda x: 7 / (2 * x), lambda x: 7 / x)
soll('K2F4 kgV(3x, 2x²) = 6x²', 'ok', 'ok')
term('K2F5', lambda x: 1 / x - 1 / (x + 1), lambda x: 1 / (x * (x + 1)))
loes('K3F1', lambda x: (6 * x + 4, 2 * x + 24), 5)
loes('K3F2', lambda x: (3 * (x - 2), x + 8), 7); loes('K3F2 Fehler 3x−2', lambda x: (3 * x - 2, x + 8), 5)
loes('K3F3', lambda x: (x / 3 + x / 6, 4), 8); loes('K3F3 Fehler x/9', lambda x: (x / 9, 4), 36)
alle('K3F4', lambda x: (2 * (x + 4), 2 * x + 8)); keine('K3F5', lambda x: (x + 5, x + 2))
formel('K4F1', lambda w: w['U'] / w['R'], lambda w: w['U'] / w['R'], 'UR')
formel('K4F2', lambda w: w['A'] / w['a'], lambda w: w['A'] / w['a'], 'Aa')
formel('K4F3', lambda w: (w['y'] - 6) / 3, lambda w: w['y'] / 3 - 2, 'y')
formel('K4F4', lambda w: w['P'] / 2 - w['b'], lambda w: (w['P'] - 2 * w['b']) / 2, 'Pb')
soll('K4F5', F(150, 60), F(5, 2))

# ---- Gesamttest
term('G1', lambda x: (x * x - 10 * x + 25) / (3 * x - 15), lambda x: (x - 5) / 3)
term('G2', lambda x: 3 / x + 2 / (x - 1), lambda x: (5 * x - 3) / (x * (x - 1)))
falsch('G3 (x²+9)/(x+3) ≠ x+3', lambda x: (x * x + 9) / (x + 3), lambda x: x + 3)
soll('G3 Probe x=1', [F(1 + 9, 1 + 3), 1 + 3], [F(5, 2), 4])
loes('G4', lambda x: (7 * x - 3 * (x - 2), 2 * x + 14), 4)
loes('G5', lambda x: ((x + 3) / 4 - (x - 1) / 6, 2), 13)
alle('G6', lambda x: (4 * (x - 1) + 6, 4 * x + 2))
soll('G7', [F(63 - 25, 2)], [19])
soll('G8', F(100 * 150, 2000 * 3), F(5, 2))
formel('G8 p', lambda w: 100 * w['Z'] / (w['K'] * w['t']), lambda w: w['Z'] / (w['K'] * w['t'] / 100), 'ZKt')
formel('G9 G=3V/h', lambda w: 3 * w['V'] / w['h'], lambda w: w['V'] / (w['h'] / 3), 'Vh')
falsch('G9 G=V·h/3', lambda h: F(12) * h / 3, lambda h: 3 * F(12) / h)
soll('Punkte', 3 + 3 + 3 + 3 + 3 + 2 + 3 + 3 + 2, 25)

# ---- Bewertungspaket: typische Fehler
loes('BP G4 −3x−6', lambda x: (7 * x - 3 * x - 6, 2 * x + 14), 10)
loes('BP G5 rechts vergessen', lambda x: (3 * (x + 3) - 2 * (x - 1), 2), -9)
loes('BP G5 Minus', lambda x: (3 * (x + 3) - 2 * x - 2, 24), 17)
soll('BP G7 63/2−a', F(63, 2) - 25, F(13, 2))
soll('BP G8 nur durch K', F(100 * 150, 2000) * 3, F(45, 2))
soll('BP G9 falsch', [F(12 * 5, 3), F(20 * 5, 3), F(3 * 20, 5)], [20, F(100, 3), 12])
falsch('BP G2 Nenner addiert', lambda x: 3 / x + 2 / (x - 1), lambda x: 5 / (2 * x - 1))

# ---- Vertiefung
soll('V1', sum(F(1, k * (k + 1)) for k in range(1, 10)), F(9, 10))
soll('V2 a=2 keine Lösung', [a for a in range(-5, 6) if a - 2 == 0], [2])
soll('V3 Schnitt', 3 * 5 - F(9, 2) - 5, F(11, 2))

print('\n' + ('ALLE ZAHLEN STIMMEN' if not fehler else f'{fehler} ABWEICHUNG(EN)'))
sys.exit(1 if fehler else 0)
