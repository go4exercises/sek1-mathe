"""Fragebild der Kontrollclips: Beim Erscheinen einer Frage zeigt das Bild nur das Gegebene.

Regel (HOWTO-leitprogramme §15, Abnahme 06.10.2026): keine neutrale Startkurve, keine Kurve,
die aus der Gleichung zu bestimmen ist, kein Begleiter (Scheitel, Nullstellen, Spiegelbild …).
Die Auflösungsgrafik erscheint erst nach der Antwort (ab 1.0 s).

REGELN nennt je Clip und Frage, was aus dem bisherigen Fragebild bleibt (Indizes in kurven,
parabeln, punkte des ersten Grafen) und welche Punkte dazukommen; ein leerer Eintrag heisst:
nur die Achsen. Fragen, die nicht in REGELN stehen, bleiben unverändert — dort ist die
gezeigte Kurve das Gegebene («im Bild», «gestrichelt», «dieser Kurve»).

Aufruf: anwenden(d) im Bauskript vor json.dump, oder für Clips ohne aktuelles Bauskript
(Quadratische Funktionen): python3 scripts/lp/fragebild.py clips/<name>.json …
Beides ist idempotent.
"""
import copy
import json
import math
import sys

BEGLEITER = ('scheitel', 'nullstellen', 'yachse', 'marken', 'laeufer', 'extrema', 'spiegel',
             'startpunkt', 'asymptoten', 'stufen', 'projektion', 'kreis', 'spur', 'dreieck')


def _pt(x, y, farbe, text, bei, anker='start'):
    return {'x': x, 'y': y, 'farbe': farbe, 'anker': anker, 'beschriftung': text, 'beschriftung_bei': bei}


P6 = math.pi / 6
REGELN = {
    'g3-3-lp-kontrolle-aufstellen': {
        'Frage 1': dict(p=[0, 1]), 'Frage 2': dict(p=[0, 1, 2]), 'Frage 3': {},
        'Frage 4': dict(p=[0, 1, 2]),
        # S ohne Beschriftung: Der Begleiter «scheitel» der Auflösung schreibt sie an dieselbe Stelle.
        'Frage 5': dict(extra=[{'x': 2, 'y': -1, 'farbe': 3, 'anker': 'start'}])},
    'g3-3-lp-kontrolle-formen': {'Frage 1': {}, 'Frage 2': {}, 'Frage 4': {}, 'Frage 5': {}},
    'g3-3-lp-kontrolle-nullstellen': {'Frage 1': {}, 'Frage 2': {}},
    'g3-3-lp-kontrolle-scheitelform': {f: dict(par=[0]) for f in ('Frage 1', 'Frage 2', 'Frage 3', 'Frage 4')},
    's3-2-lp-kontrolle-exponent': {'Frage 1': {}, 'Frage 2': {}, 'Frage 3': {}},
    's3-2-lp-kontrolle-hyperbel': {'Frage 3': {}},
    's3-2-lp-kontrolle-umkehren': {'Frage 1': {}, 'Frage 3': dict(p=[0])},
    's3-2-lp-kontrolle-verschieben': {'Frage 1': dict(k=[0]), 'Frage 2': dict(k=[0]), 'Frage 3': {}},
    's3-2-lp-kontrolle-wurzel': {'Frage 3': {}},
    's3-3-lp-kontrolle-linearfaktoren': {'Frage 3': {}, 'Frage 5': {}},
    's3-3-lp-kontrolle-vielfachheit': {'Frage 3': {}},
    's3-4-lp-kontrolle-e-funktion': {'Frage 5': {}},
    's3-4-lp-kontrolle-exponentialfunktion': {'Frage 3': {}},
    's3-4-lp-kontrolle-logarithmus': {
        'Frage 3': dict(k=[0, 1], extra=[_pt(2, 4, 1, '(2 | 4)', [1.6, 4.9], 'end')])},
    's3-5-lp-kontrolle-gleichungen': {
        'Frage 4': dict(k=[1], extra=[_pt(P6, 0.5, 1, '(π/6 | 0.5)', [P6 + 0.15, 0.15])])},
    's3-5-lp-kontrolle-kreis-kurve': {'Frage 3': {}},
    's3-5-lp-kontrolle-periode-symmetrie': {'Frage 5': {}},
    's3-5-lp-kontrolle-tangens': {'Frage 4': {}},
    's3-6-lp-kontrolle-abschnittsweise': {'Frage 4': {}},
    's3-6-lp-kontrolle-betragsfunktion': {'Frage 3': {}},
    's3-6-lp-kontrolle-gleichungen': {'Frage 4': dict(k=[1])},
}

FENSTER = ('x', 'y', 'breite', 'hoehe', 'abstand', 'pfeile', 'xbereich', 'ybereich',
           'xteilung', 'yteilung', 'xname', 'yname')


def _ohne_begleiter(k):
    return {a: b for a, b in k.items() if a not in BEGLEITER}


def anwenden(d):
    regeln = REGELN.get(d['dateiname'], {})
    for szene in d['szenen']:
        regel = regeln.get(szene['name'])
        if regel is None:
            continue
        el = szene['elemente']
        grafen = [e for e in el if e.get('typ') == 'graf']
        if not grafen or grafen[0].get('_fragebild'):
            continue                                   # schon angewendet
        g0 = grafen[0]
        neu = {'typ': 'graf', 'anim': 'fade', 'ein': 0.05, '_fragebild': True, 'tippbar': True}
        neu.update({a: copy.deepcopy(g0[a]) for a in FENSTER if a in g0})
        neu['kurven'] = [_ohne_begleiter(g0['kurven'][i]) for i in regel.get('k', [])]
        neu['parabeln'] = [_ohne_begleiter(g0['parabeln'][i]) for i in regel.get('par', [])]
        neu['geraden'] = []
        neu['punkte'] = [copy.deepcopy(g0['punkte'][i]) for i in regel.get('p', [])] + regel.get('extra', [])
        for g in grafen:
            g['ein'] = max(g.get('ein', 0.05), 1.0)
        el.insert(el.index(g0), neu)
    return d


if __name__ == '__main__':
    for pfad in sys.argv[1:]:
        d = json.load(open(pfad))
        json.dump(anwenden(d), open(pfad, 'w'), ensure_ascii=False, indent=1)
        print(pfad)
