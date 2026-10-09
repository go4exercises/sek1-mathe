"""Rechnet jede feste Zahl des Leitprogramms Bruchrechnen nach (Seite, Simulationen, PDFs).

  python3 scripts/lp/bruchrechnen/zahlen.py      # Exit 1 bei einer Abweichung

Jede Zeile: Ausdruck (Python mit Fraction F) und der Wert, der im Leitprogramm steht.
Fehlerbeispiele: Der falsche Wert muss wirklich vom richtigen abweichen (HOWTO §15).
"""
from fractions import Fraction as F
from math import gcd, lcm
import sys

fehler = 0
def soll(name, wert, erwartet):
    global fehler
    ok = wert == erwartet
    if not ok:
        fehler += 1
    print(('ok   ' if ok else 'FALSCH'), name, '=', wert, '' if ok else f'(erwartet {erwartet})')
def falsch(name, falscher, richtiger):
    global fehler
    ok = falscher != richtiger
    if not ok:
        fehler += 1
    print(('ok   ' if ok else 'FALSCH'), 'Fehlerbeispiel', name, falscher, '≠', richtiger)

# ---- Vortest
soll('0a ggT(16,40)', gcd(16, 40), 8)
soll('0a kgV(6,10)', lcm(6, 10), 30)
soll('0b', [(-2) * 3, F(-12, -4), -5 + 8, 3 - 7, 3 - (-7)], [-6, 3, 3, -4, 10])
soll('Kurz wiederholt', [gcd(12, 18), lcm(4, 6), 5 - (-2), -3**2], [6, 12, 7, -9])
soll('0c 12:3·2', F(12, 3) * 2, 8)
soll('0c 2+3·4', 2 + 3 * 4, 14)
soll('0d', [F(3, 8), 1 - F(3, 8)], [F(3, 8), F(5, 8)])
soll('0e', [2**3, (-3)**2, -3**2], [8, 9, -9])

# ---- Kapitel 1
soll('Festhalten 12/18', F(12, 18), F(2, 3)); soll('ggT(12,18)', gcd(12, 18), 6)
soll('2/3 = 8/12', F(8, 12), F(2, 3)); soll('3/4 = 9/12', F(9, 12), F(3, 4))
falsch('(2+3)/(2+5) vs 3/5', F(2 + 3, 2 + 5), F(3, 5))
falsch('(3+1)/(4+1) vs 3/4', F(4, 5), F(3, 4))
soll('Sim1 3/4=6/8', F(6, 8), F(3, 4)); soll('Sim1 3/4=15/20', F(15, 20), F(3, 4))
soll('Sim1 12/18=2/3', F(12, 18), F(2, 3)); soll('Sim1 5/6=10/12', F(10, 12), F(5, 6))
soll('Sim1 5/6 mit Nenner 4 unmöglich', any(F(k, 4) == F(5, 6) for k in range(5)), False)
soll('Sim1 kleinster Nenner >6 für 5/6', min(n for n in range(7, 25) if (5 * n) % 6 == 0), 12)
soll('Sim1 kgV(3,4)', lcm(3, 4), 12); soll('Sim1 3/4=9/12', F(9, 12), F(3, 4))
soll('1a 5/6 = 20/24', F(20, 24), F(5, 6)); soll('1a 45/60', F(45, 60), F(3, 4))
soll('1b gleich 2/5', [str(x) for x in ['4/10', '6/15', '7/10', '10/25', '3/6'] if F(x) == F(2, 5)], ['4/10', '6/15', '10/25'])
soll('1c HN', lcm(6, 5, 10), 30)
soll('1c', [F(5, 6) * 30, F(4, 5) * 30, F(7, 10) * 30], [25, 24, 21])
soll('1c Reihenfolge', sorted([F(5, 6), F(4, 5), F(7, 10)]), [F(7, 10), F(4, 5), F(5, 6)])
falsch('1d (6+4)/(6+9) «gekürzt» 4/9', F(4, 9), F(6 + 4, 6 + 9)); soll('1d richtig', F(10, 15), F(2, 3))
soll('1f 6/8', F(6, 8), F(3, 4)); soll('1f 12/16', F(12, 16), F(3, 4))

# ---- Kapitel 2
soll('Sim2 kgV(2,3)', lcm(2, 3), 6); soll('Sim2 1/2+1/3', F(1, 2) + F(1, 3), F(5, 6))
soll('Sim2 falsch 2/5 < 1/2', F(2, 5) < F(1, 2), True)
soll('Sim2 kgV(4,6)', lcm(4, 6), 12); soll('Sim2 3/4+1/6', F(3, 4) + F(1, 6), F(11, 12))
soll('Sim2 kgV(8,6)', lcm(8, 6), 24); soll('Sim2 7/8-1/6', F(7, 8) - F(1, 6), F(17, 24))
soll('Sim2 kgV(9,6)', lcm(9, 6), 18); soll('Sim2 2/9+1/6', F(2, 9) + F(1, 6), F(7, 18))
soll('Sim2 alle Ergebnisse ≤ 1', all(x <= 1 for x in [F(5, 6), F(11, 12), F(17, 24), F(7, 18)]), True)
soll('Festhalten 5/12+7/18', F(5, 12) + F(7, 18), F(29, 36)); soll('kgV(12,18)', lcm(12, 18), 36)
soll('Festhalten 2-3/4', 2 - F(3, 4), F(5, 4))
soll('Festhalten 1/6+1/3', F(1, 6) + F(1, 3), F(1, 2))
soll('2a', [F(5, 12) + F(1, 12), F(9, 10) - F(3, 10), 3 - F(5, 7)], [F(1, 2), F(3, 5), F(16, 7)])
soll('2e', [F(5, 15) + F(3, 15), F(1, 3) + F(1, 5)], [F(8, 15), F(8, 15)])
soll('2f', F(1, 2) + F(2, 3) - F(3, 4), F(5, 12)); soll('2f HN', lcm(2, 3, 4), 12)
soll('Festhalten 3 4/5:2', F(4, 5) / 2, F(2, 5)); soll('Festhalten 4 1/2-(-1/4)', F(1, 2) - F(-1, 4), F(3, 4))
soll('2b', F(3, 4) + F(5, 6), F(19, 12))
soll('2c', F(11, 12) - F(4, 9), F(17, 36)); soll('2c HN', lcm(12, 9), 36)
soll('2d', 3 - F(5, 7), F(16, 7))
falsch('2d 3/7', F(3, 7), F(2, 3) + F(1, 4)); soll('2d 3/7 < 2/3', F(3, 7) < F(2, 3), True)
soll('2d', F(2, 3) + F(1, 4), F(11, 12))

# ---- Kapitel 3
soll('Sim3 2/3·3/4', F(2, 3) * F(3, 4), F(1, 2))
soll('Sim3 3/4:1/8', F(3, 4) / F(1, 8), 6); soll('Sim3 3/4:1/2', F(3, 4) / F(1, 2), F(3, 2))
soll('Festhalten 2/3·3/4 = 6/12', F(6, 12), F(1, 2)); soll('Festhalten 3·2/5', 3 * F(2, 5), F(6, 5))
soll('Festhalten 4/9·3/8', F(4, 9) * F(3, 8), F(1, 6)); soll('Festhalten 2/3 von 12', F(2, 3) * 12, 8)
falsch('Festhalten Kehrwert vom ersten', F(4, 3) * F(1, 8), F(3, 4) / F(1, 8)); soll('4/3·1/8', F(4, 3) * F(1, 8), F(1, 6))
soll('3a', F(5, 6) * F(3, 10), F(1, 4))
soll('3b (1/2)', [4 * F(5, 6), F(2, 3) * 15], [F(10, 3), 10])
soll('3c', F(3, 5) / F(9, 10), F(2, 3))
soll('3b (2/2)', [F(7, 8) / 7, 6 / F(3, 4)], [F(1, 8), 8])
falsch('3d 10/7', F(5, 2) * F(4, 7), F(2, 5) / F(4, 7)); soll('3d 5/2·4/7', F(5, 2) * F(4, 7), F(10, 7)); soll('3d', F(2, 5) / F(4, 7), F(7, 10))
soll('3d', [F(5, 6) * F(3, 5), F(5, 6) / F(3, 5)], [F(1, 2), F(25, 18)]); soll('3d grösser', F(25, 18) > F(5, 6), True)
soll('3f Mehl', [F(5, 4) / F(3, 8), F(2, 5) * F(5, 4), F(5, 4) - 3 * F(3, 8)], [F(10, 3), F(1, 2), F(1, 8)])
soll('3f', F(3, 4) * F(2, 5), F(3, 10))

# ---- Kapitel 4 (Schrittwähler)
soll('Sim4.1 1/4+2/3·3/8', F(1, 4) + F(2, 3) * F(3, 8), F(1, 2))
soll('Sim4.2 5/6-(1/4:3/2)', F(5, 6) - (F(1, 4) / F(3, 2)), F(2, 3))
soll('Sim4.3 2/3:4/9·1/2', F(2, 3) / F(4, 9) * F(1, 2), F(3, 4))
falsch('Sim4.3 rechts zuerst', F(2, 3) / (F(4, 9) * F(1, 2)), F(3, 4))
soll('Sim4.4 (-2/3)²-1/3·1/2', F(-2, 3)**2 - F(1, 3) * F(1, 2), F(5, 18))
soll('Sim4.5 -3/4-(1/2-5/4):3', F(-3, 4) - (F(1, 2) - F(5, 4)) / 3, F(-1, 2))
soll('Festhalten 1/2-1/3·(3/4-1/4)', F(1, 2) - F(1, 3) * (F(3, 4) - F(1, 4)), F(1, 3))
soll('Festhalten (-3/4)·(-2/9)', F(-3, 4) * F(-2, 9), F(1, 6))
soll('Festhalten (2/3)²', F(2, 3)**2, F(4, 9)); soll('(-1/2)²', F(-1, 2)**2, F(1, 4)); soll('-(1/2)²', -F(1, 2)**2, F(-1, 4))
soll('Warn 3/4-(1/2-1/4)', F(3, 4) - (F(1, 2) - F(1, 4)), F(1, 2)); falsch('Warn ohne Klammer', F(3, 4) - F(1, 2) - F(1, 4), F(1, 2))
soll('Warn 1:1/2·1/2', 1 / F(1, 2) * F(1, 2), 1); falsch('Warn 1:(1/2·1/2)', 1 / (F(1, 2) * F(1, 2)), 1)
soll('4a', F(7, 12) - F(1, 4) * F(2, 3), F(5, 12))
soll('4b', (F(3, 4) - F(1, 3)) / F(5, 6), F(1, 2))
soll('4c', F(-2, 5) + F(3, 10) * F(-4, 3), F(-4, 5))
soll('4d', [F(-3, 2)**2 - F(3, 4), -F(3, 2)**2 + F(3, 4)], [F(3, 2), F(-3, 2)])
falsch('4e 3/4:(3/8·1/2)', F(3, 4) / (F(3, 8) * F(1, 2)), F(3, 4) / F(3, 8) * F(1, 2))
soll('4e falsch = 4', F(3, 4) / (F(3, 8) * F(1, 2)), 4); soll('4e richtig', F(3, 4) / F(3, 8) * F(1, 2), 1)
soll('4f', [F(-2, 3) * F(-3, 4), F(-2, 3) + F(-3, 4)], [F(1, 2), F(-17, 12)])

# ---- Gesamttest (nach der Prüfung vom 09.10.2026)
soll('G1 84/126', F(84, 126), F(2, 3)); soll('G1 ggT', gcd(84, 126), 42)
soll('G1b', [F(21, 28), F(15, 20)], [F(3, 4), F(3, 4)]); soll('G1b Kreuzprodukt', [21 * 20, 28 * 15], [420, 420])
soll('G2', F(7, 15) + F(5, 6) - F(1, 2), F(4, 5)); soll('G2 HN', lcm(15, 6, 2), 30)
soll('G2 Zähler', [F(7, 15) * 30, F(5, 6) * 30, F(1, 2) * 30], [14, 25, 15])
soll('G3', [F(3, 4) * 36, F(7, 9) * 36], [27, 28]); soll('G3 Unterschied', F(7, 9) - F(3, 4), F(1, 36))
falsch('G3 Nenner subtrahiert', F(7 - 3, 9 - 4), F(1, 36))
soll('G4', F(9, 14) * F(7, 12) / F(3, 4), F(1, 2)); soll('G4 Zwischen', F(9, 14) * F(7, 12), F(3, 8))
soll('G4 Zwischen ≠ Divisor', F(3, 8) != F(3, 4), True)
soll('G4 Kehrwert vergessen', F(3, 8) * F(3, 4), F(9, 32)); soll('G4 Kehrwert falsch', F(8, 3) * F(3, 4), 2)
soll('G4 rechts zuerst gleich', [F(7, 12) / F(3, 4), F(9, 14) * F(7, 9)], [F(7, 9), F(1, 2)])
soll('G5', [F(3, 2) / F(1, 4), F(2, 3) * F(3, 2), F(3, 2) / F(1, 4)], [6, 1, 6])
soll('G5 Fehler', [F(3, 2) * F(1, 4), F(3, 2) / F(2, 3)], [F(3, 8), F(9, 4)])
soll('G6', (F(5, 6) - F(1, 3)) * F(3, 4) + F(1, 8), F(1, 2)); soll('G6 Schritte', [F(5, 6) - F(1, 3), F(1, 2) * F(3, 4)], [F(1, 2), F(3, 8)])
soll('G6 zuerst addiert', F(1, 2) * (F(3, 4) + F(1, 8)), F(7, 16)); soll('G6 Klammer weg', F(5, 6) - F(1, 3) * F(3, 4) + F(1, 8), F(17, 24))
soll('G7', F(-3, 4)**2 / F(9, 8) - 1, F(-1, 2)); soll('G7 9/16:9/8', F(9, 16) / F(9, 8), F(1, 2))
soll('G7 Fehler', [-F(9, 16) / F(9, 8) - 1, F(9, 4) / F(9, 8) - 1, F(16, 9) * F(9, 8) - 1, F(9, 16) / (F(9, 8) - 1)], [F(-3, 2), 1, 1, F(9, 2)])
soll('G8 2/3:(-4/9)', F(2, 3) / F(-4, 9), F(-3, 2)); soll('G8', F(-5, 6) + F(2, 3) / F(-4, 9), F(-7, 3))
soll('G8 Fehler', [F(-5, 6) + F(3, 2), (F(-5, 6) + F(2, 3)) / F(-4, 9), F(3, 2) * F(-4, 9), F(-5, 6) + F(-2, 3)], [F(2, 3), F(3, 8), F(-2, 3), F(-3, 2)])
soll('G9 richtig', F(1, 3) + F(1, 6) * 4, 1); soll('G9 falsch', (F(1, 3) + F(1, 6)) * 4, 2); soll('G9 4/24', F(1, 3) + F(4, 24), F(1, 2))
soll('G2 Fehler', [F(7 + 5 - 1, 15 + 6 - 2), F(7 + 5 - 1, 30)], [F(11, 19), F(11, 30)])
soll('Punkte', 2 + 3 + 2 + 3 + 3 + 3 + 3 + 3 + 3, 25)

# ---- Erkundungen (neu 09.10.2026: andere Zahlen als Clip und Festhalten)
soll('Sim1 3/5=6/10', F(6, 10), F(3, 5)); soll('Sim1 3/5=12/20', F(12, 20), F(3, 5)); soll('Sim1 10/16=5/8', F(10, 16), F(5, 8))
soll('Sim1 kleinster Nenner 10/16', min(n for n in range(1, 25) if (10 * n) % 16 == 0), 8)
soll('Sim1 kgV(8,3)', lcm(8, 3), 24); soll('Sim1 1/3=8/24, 3/8=9/24', [F(8, 24), F(9, 24)], [F(1, 3), F(3, 8)]); soll('Sim1 3/8 > 1/3', F(3, 8) > F(1, 3), True)
soll('Sim2 kgV(4,6)', lcm(4, 6), 12); soll('Sim2 1/4+1/6', F(1, 4) + F(1, 6), F(5, 12)); soll('Sim2 2/10 < 1/4', F(2, 10) < F(1, 4), True)
soll('Sim2 kgV(8,6)', lcm(8, 6), 24); soll('Sim2 3/8+1/6', F(3, 8) + F(1, 6), F(13, 24))
soll('Sim2 kgV(9,6)', lcm(9, 6), 18); soll('Sim2 7/9-1/6', F(7, 9) - F(1, 6), F(11, 18))
soll('Sim2 kgV(5,3)=15', lcm(5, 3), 15); soll('Sim2 2/5+1/3', F(2, 5) + F(1, 3), F(11, 15))
soll('Sim2 alle ≤ 1', all(x <= 1 for x in [F(5, 12), F(13, 24), F(11, 18), F(11, 15)]), True)
soll('Sim3 3/5·2/3', F(3, 5) * F(2, 3), F(2, 5)); soll('Sim3 1/2:1/6', F(1, 2) / F(1, 6), 3); soll('Sim3 2/3:1/2', F(2, 3) / F(1, 2), F(4, 3))
soll('Sim3 2/3:1/2 < 2', F(4, 3) < 2, True)

# ---- Clips: Einführung (Zahlen = Festhalten)
soll('Clip1 3/4=15/20', F(15, 20), F(3, 4)); falsch('Clip1 (3+1)/(4+1)', F(4, 5), F(3, 4)); soll('Clip1 4/5 > 3/4', F(4, 5) > F(3, 4), True)
soll('Clip1 Frage: 3 Viertel · 5', 3 * 5, 15)
soll('Clip1 6/9', F(6, 9), F(2, 3)); soll('Clip1 ggT(6,9)', gcd(6, 9), 3)
soll('Clip2 3/8+1/8', F(3, 8) + F(1, 8), F(1, 2)); soll('Clip2 2/5 < 1/2', F(2, 5) < F(1, 2), True)
soll('Clip2 Vielfache 18', [18 * k for k in (1, 2)], [18, 36]); soll('Clip2 36:12', 36 // 12, 3)
soll('Clip2 Erweitern', [F(5, 12) * 36, F(7, 18) * 36], [15, 14])
soll('Clip3 Flächen 2/3·3/4 Kästchen', (2 * 3, 3 * 4), (6, 12)); soll('Clip3 3·2/5', 3 * F(2, 5), F(6, 5)); soll('Clip3 6/5 > 1', F(6, 5) > 1, True)
soll('Clip3 Zahlenstrahl: 3·2.4 = 7.2 = 6/5 von 6', 3 * F(12, 5), F(36, 5)); soll('Clip3 7.2/6', F(36, 5) / 6, F(6, 5))
soll('Clip3 2/3 von 12', F(2, 3) * 12, 8); soll('Clip3 24/4', F(24, 4), 6)
soll('Clip4 Baum Klammer', F(3, 4) - F(1, 4), F(1, 2)); soll('Clip4 Baum mal', F(1, 3) * F(1, 2), F(1, 6))
soll('Clip4 Potenz 4 von 9', (2 * 2, 3 * 3), (4, 9))

# ---- Kontrollclips
soll('K1F1 4/6=2/3', F(4, 6), F(2, 3)); soll('K1F1 3/4 > 2/3 > 3/5', F(3, 4) > F(2, 3) > F(3, 5), True)
soll('K1F2 2/7=6/21', F(6, 21), F(2, 7)); falsch('K1F2 16', F(16, 21), F(2, 7)); falsch('K1F2 2', F(2, 21), F(2, 7))
soll('K1F3 18/24', F(18, 24), F(3, 4)); soll('K1F3 ggT', gcd(18, 24), 6); soll('K1F3 9/12, 6/8 kürzbar', [gcd(9, 12), gcd(6, 8)], [3, 2])
soll('K1F4', [F(5, 8) * 40, F(3, 5) * 40], [25, 24]); soll('K1F4 5/8 > 3/5', F(5, 8) > F(3, 5), True)
soll('K1F5', F(3 + 5, 3 + 7), F(4, 5)); falsch('K1F5 5/7', F(5, 7), F(4, 5))
soll('K2F1', F(3, 10) + F(1, 10), F(2, 5)); falsch('K2F1 4/20', F(4, 20), F(2, 5))
soll('K2F2 kgV(8,12)', lcm(8, 12), 24); soll('K2F2 96 = 8·12', 8 * 12, 96)
soll('K2F3', F(1, 4) + F(1, 5), F(9, 20)); falsch('K2F3 2/9', F(2, 9), F(9, 20)); soll('K2F3 2/9 < 1/4', F(2, 9) < F(1, 4), True); falsch('K2F3 2/20', F(2, 20), F(9, 20))
soll('K2F4', F(5, 6) - F(1, 4), F(7, 12)); falsch('K2F4 4/2', F(4, 2), F(7, 12)); falsch('K2F4 4/12', F(4, 12), F(7, 12))
soll('K2F5 2/7 < 1/3', F(2, 7) < F(1, 3), True); soll('K2F5 richtig', F(1, 3) + F(1, 4), F(7, 12)); soll('K2F5 2/7 gekürzt', gcd(2, 7), 1)
soll('K3F1 neu', F(3, 5) * F(5, 6), F(1, 2)); soll('K3F1 Fehler', [F(3, 5) / F(5, 6), F(3 + 5, 5 + 6)], [F(18, 25), F(8, 11)])
soll('K3F1 alt (nicht mehr verwendet)', F(2, 5) * F(3, 4), F(3, 10)); falsch('K3F1 8/15', F(2, 5) / F(3, 4), F(3, 10)); soll('K3F1 8/15 = geteilt', F(2, 5) / F(3, 4), F(8, 15)); falsch('K3F1 5/9', F(5, 9), F(3, 10))
soll('K3F2', F(1, 3) * F(3, 4), F(1, 4)); soll('K3F2 Kästchen', (1 * 3, 3 * 4), (3, 12))
soll('K3F3', F(4, 5) / F(2, 3), F(6, 5)); soll('K3F3 Kehrwert vergessen', F(4, 5) * F(2, 3), F(8, 15)); soll('K3F3 erster umgedreht', F(5, 4) * F(2, 3), F(5, 6))
soll('K3F4', F(2, 3) / F(1, 6), 4); soll('K3F4 1/9 = mal', F(2, 3) * F(1, 6), F(1, 9))
soll('K3F5', 5 * F(2, 7), F(10, 7)); soll('K3F5 10/35', F(10, 35), F(2, 7)); falsch('K3F5 7/10', F(7, 10), F(10, 7))
soll('K4F1', F(2, 5) + F(3, 5) * F(1, 3), F(3, 5)); soll('K4F1 falsch', (F(2, 5) + F(3, 5)) * F(1, 3), F(1, 3))
soll('K4F2', F(3, 4) / F(1, 4) * F(1, 3), 1); soll('K4F2 rechts zuerst', F(3, 4) / (F(1, 4) * F(1, 3)), 9)
soll('K4F3', F(-2, 5) * F(-5, 6), F(1, 3)); falsch('K4F3 -10/11', F(-10, 11), F(1, 3))
soll('K4F4', -F(3, 4)**2, F(-9, 16)); falsch('K4F4 -3/2', F(-3, 2), F(-9, 16))
soll('K4F5', F(2, 3) - (F(1, 2) - F(1, 6)), F(1, 3)); soll('K4F5 ohne Klammer', F(2, 3) - F(1, 2) - F(1, 6), 0); falsch('K4F5 1', F(1), F(1, 3))
soll('K4F5 2/3+1/2-1/6', F(2, 3) + F(1, 2) - F(1, 6), 1)

# ---- Vertiefung
soll('V1', F(1, 2) + F(1, 4) + F(1, 8) + F(1, 16), F(15, 16))
soll('V2', F(1, 3) + F(1, 6), F(1, 2))
soll('V2 alle Paare 1/a+1/b=1/2, a<b', [(a, b) for a in range(3, 50) for b in range(a + 1, 200) if F(1, a) + F(1, b) == F(1, 2)], [(3, 6)])
soll('V3', F(2025, 2026) < F(2026, 2027), True)
soll('V3 Abstand', [1 - F(2025, 2026), 1 - F(2026, 2027)], [F(1, 2026), F(1, 2027)])

print('\n' + ('ALLE ZAHLEN STIMMEN' if not fehler else f'{fehler} ABWEICHUNG(EN)'))
sys.exit(1 if fehler else 0)
