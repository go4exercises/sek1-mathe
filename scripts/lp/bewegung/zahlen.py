"""Rechnet jede feste Zahl des Leitprogramms «Bewegung und Begegnung» (Mathematisieren) nach — Seite, Simulationen,
Clips und PDFs, exakt mit Fraction.

  python3 scripts/lp/bewegung/zahlen.py      # Exit 1 bei einer Abweichung
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


def gleich(a1, m1, a2, m2):
    """Grundbetrag a, Preis m pro Stück: gleich teuer bei x = (a2 − a1) / (m1 − m2)."""
    return (F(a2) - F(a1)) / (F(m1) - F(m2))


def treffen(d, v1, v2, entgegen=True):
    return F(d) / (F(v1) + F(v2) if entgegen else F(v1) - F(v2))


# ---- Vortest
soll('0a', [F(3, 4) * 60, F(90, 60)], [45, F(3, 2)])
soll('0b', (F(21) + 3) / 4, 6)
soll('0c', [F(150, 3), F(100, 50)], [50, 2])
soll('0d', 2 * F(5, 2) + 1, 6)
soll('0e', F(1000, 60) * 60, 1000)

# ---- Kapitel 1: Vom Text zur Gleichung
soll('Clip1 Bank gleich', gleich(4, F(1, 2), 7, F(1, 5)), 10); soll('Clip1 Kosten bei 10', [4 + F(1, 2) * 10, 7 + F(1, 5) * 10], [9, 9])
soll('Clip1 bei 11', [4 + F(1, 2) * 11, 7 + F(1, 5) * 11], [F(19, 2), F(46, 5)])          # 9.50 gegen 9.20: B günstiger
soll('Sim1', [gleich(15, 2, 5, 4), gleich(40, 5, 100, 2), gleich(8, 2, 4, 3), gleich(3, F(3, 2), 6, F(3, 4))], [5, 20, 4, 4])
soll('Sim1.2 bei 6', [15 + 2 * 6, 5 + 4 * 6], [27, 29])
soll('1a Velo', [gleich(20, 3, 32, 1)], [6]); soll('1a bei 7', [20 + 3 * 7, 32 + 7], [41, 39])
soll('1b ungerade', (F(45) - 6) / 3, 13); soll('1b Probe', 13 + 15 + 17, 45)
soll('1c Alter', (F(41) - 5) / 2, 18)
soll('1d Busse', [F(75, 9), 8 * 9], [F(25, 3), 72])                                                  # 10.83… → 11 Busse
soll('1e Probe', 4 * 7 + 3, 31)

# ---- Kapitel 2: s = v · t
soll('Clip2 Zug', [F(240, 2), F(240, 120)], [120, 2]); soll('Clip2 Velo 20 min', 18 * F(20, 60), 6)
soll('Clip2 Fallen', [18 * 20, F(18 * 20, 100)], [360, F(18, 5)])
soll('Clip2 Einheiten', [F(45, 60), F(36, F(18, 5))], [F(3, 4), 10]); falsch('Clip2 45 min ≠ 0.45 h', F(45, 100), F(3, 4))
soll('Sim2', [F(45, 60) * 60, F(30) / F(40, 60), 90 * F(20, 60), F(3, 12) * 60, F(100) / F(75, 60)], [45, 45, 30, 15, 80])
soll('2a', [F(150, F(5, 2)), 60 * F(40, 60)], [60, 40])
soll('2b', [F(5, 1) * F(18, 5), F(90, F(18, 5))], [18, 25])
soll('2c', F(12, 15) * 60, 48)
soll('2d', 4 * F(9, 4), 9); falsch('2d Lia 2.15 h', 4 * F(43, 20), 9); soll('3f', [F(24, 2), F(16, 1), F(40, 4)], [12, 16, 10]); soll('4e', F(12, 18 - 14), 3); falsch('4e Mia', F(12, 32), 3); soll('4f', F(30, 25), F(6, 5))
soll('2e Schall', 340 * 3, 1020)

# ---- Kapitel 3: Abschnitte
soll('Clip3', [F(30, 20), F(1, 2), F(20, 10), F(50) / (F(30, 20) + F(1, 2) + 2)], [F(3, 2), F(1, 2), 2, F(25, 2)])
falsch('Clip3 Mittel', F(20 + 10, 2), F(25, 2))
soll('Sim3', [(80 + 40 * 1) / F(2), (40 + 80) / F(2), F(120) / (1 + 2), (30 + 90) / F(2), F(40 * F(3, 2)) / 2], [60, 60, 40, 60, 30])
soll('3a', [F(12, 4) + 1 + F(6, 3), (F(12) + 6) / (F(12, 4) + 1 + F(6, 3))], [6, 3])
soll('3b', [F(60, 120) + F(60, 60), F(120) / (F(60, 120) + F(60, 60))], [F(3, 2), 80]); falsch('3b Mittel', F(120 + 60, 2), 80)
soll('3c', (2 * 50 + 1 * 80) / F(3), 60)
soll('3d', F(42) / F(7, 2), 12)

# ---- Kapitel 4: Begegnung und Einholen
soll('Clip4 Begegnung', [treffen(36, 14, 10), 14 * treffen(36, 14, 10)], [F(3, 2), 21])
soll('Clip4 Einholen', [10 * 1, treffen(10, 15, 10, False)], [10, 2])
soll('Clip4 Rolltreppe', [F(30) / (1 + F(1, 2)), F(30) / F(1, 2)], [20, 60])
soll('Sim4', [treffen(30, 12, 8), treffen(20, 15, 10, False), treffen(42, 20, 15), treffen(10, 20, 15, False), (F(30) - 6) / 20], [F(3, 2), 4, F(6, 5), 2, F(6, 5)])
soll('4a', [treffen(60, 18, 12), 18 * treffen(60, 18, 12)], [2, 36])
soll('4b', [12 * F(1, 2), treffen(6, 20, 12, False), 20 * F(3, 4)], [6, F(3, 4), 15])
soll('4c', [F(48) / (F(3, 2) + F(1, 2)), F(48) / F(1, 2)], [24, 96])
soll('4d', [80 + 100, F(450, 180)], [180, F(5, 2)])

# ---- Kontrollclips
soll('K1F1', (F(30) - 4) / 2, 13); soll('K1F2', gleich(5, 2, 11, 1), 6); soll('K1F3', (F(60) - 20) / 8, 5); falsch('K1F3 a', F(60 + 20, 8), 5); falsch('K1F3 b', F(60, 8), 5)
soll('K1F4', F(36, 4), 9); soll('K1F5', F(46, 8), F(23, 4))
soll('K2F1', F(90) / F(5, 4), 72); falsch('K2F1 1.15', F(90) / F(115, 100), 72); soll('K2F2', F(15, 60), F(1, 4)); soll('K2F3', [F(108) / F(18, 5), 108 * F(18, 5)], [30, F(1944, 5)])
soll('K2F4', 50 * F(1, 2), 25); soll('K2F5', F(400, 50), 8)
soll('K3F1', F(60 + 20, 2), 40); soll('K3F2', F(120) / (1 + 3), 30); soll('K3F3', F(2 * 30, 3), 20); soll('K3F4', F(10, 20) + F(6, 12), 1)
soll('K4F1', 30 + 20, 50); soll('K4F2', 30 - 20, 10); soll('K4F3', treffen(100, 60, 40), 1); soll('K4F4', [treffen(8, 14, 10, False), F(8, 24)], [2, F(1, 3)])
soll('K4F5', [F(60) / (1 + F(1, 2)), F(60) / F(1, 2)], [40, 120]); soll('Fest4 Rolltreppe', [F(30) / F(3, 2), F(30) / F(1, 2)], [20, 60])

# ---- Gesamttest
soll('G1 Streaming', gleich(9, 3, 30, 0), 7); soll('G1 bei 8', [9 + 3 * 8, 30], [33, 30]); falsch('G1 vertauscht', (F(30) - 3) / 9, 7)
soll('G4', [F(54) / F(18, 5), F(36, 60), 5 * F(18, 5)], [15, F(3, 5), 18])
soll('G5', [F(9) / F(9, 2), F(1, 2), F(3, 2), F(12) / (2 + F(1, 2) + F(3, 2))], [2, F(1, 2), F(3, 2), 3]); falsch('G5 Mittel', (F(9, 2) + 2) / 2, 3); falsch('G5 ohne Pause', F(12) / F(7, 2), 3)
soll('G6', [F(18, 1), F(30 - 18, F(3, 2)), F(30, 3)], [18, 8, 10]); falsch('G6 ohne Pause', F(30) / F(5, 2), 10)
soll('G7', [18 + 12, treffen(50, 18, 12), 18 * treffen(50, 18, 12), 12 * treffen(50, 18, 12), treffen(50, 18, 12) * 60], [30, F(5, 3), 30, 20, 100])
soll('G8', [60 * F(1, 2), treffen(30, 90, 60, False), 90 * treffen(30, 90, 60, False), 60 * F(3, 2)], [30, 1, 90, 90]); falsch('G8 addiert', F(30, 150), 1)
soll('G2 gerade', (F(84) - 6) / 3, 26); soll('G2 Probe', 26 + 28 + 30, 84)
soll('G3', [F(135) / F(3, 2), F(60, 90) * 60], [90, 40]); falsch('G3 1.30 h', F(135) / F(13, 10), 90)
soll('Punkte', 4 + 3 + 3 + 3 + 4 + 2 + 3 + 3, 25)

print('\n' + ('ALLE ZAHLEN STIMMEN' if not fehler else f'{fehler} ABWEICHUNG(EN)'))
sys.exit(1 if fehler else 0)
