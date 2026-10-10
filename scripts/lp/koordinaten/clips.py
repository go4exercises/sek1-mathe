"""Erzeugt die acht Drehbücher des Leitprogramms «Abbildungen und Geraden im Koordinatensystem» (10.10.2026).

  python3 scripts/lp/koordinaten/clips.py

Gerüst und Zeitlogik aus scripts/lp/pythagoras/clips.py: Je Kapitel ein Einführungsclip (mit einer Vorhersagefrage)
und ein Kontrollclip (fünf Fragen mit neuen Zahlen, Anfänge der Fragetexte verschieden). Gemessene `dauer` werden beim
Neulauf gerettet; Einblendungen stehen als «@wort» auf dem Wort, das sie nennen (wortzeiten.json, faster-whisper medium).
Zahlwörter hört Whisper als Ziffern: Anker darum auf Wörtern ohne Zahl.

Bild rechts (x 1010, y 175, 760 × 760), Rechnung links (x 150). Koordinatensystem −7 … 7 mit Achsen und Karo, Punkte mit
Namen, Wege und Achsen als Strecken.

Fragebild (HOWTO-leitprogramme §15): In den Kontrollclips zeigt das Bild beim Erscheinen einer Frage nur das Gegebene
(FRAGEBILD unten); die Auflösung erscheint ab 1.0 s, nach der Antwort.

Farben — gleich wie auf der Seite:
  1 blau   = Original (P, Figur)                    \\fa{…}
  2 orange = Bild (P', Bildfigur)                   \\fb{…}
  3 grün   = Zentrum, Achse, Gerade, Ergebnis       \\fc{…}
  4 rot    = Fehler                                 \\fd{…}
  5 Tinte  = Wege, Hilfslinien
Gesprochen: Punkte als «P mit fünf und drei», «P Strich» für P', Zahlwörter ausgeschrieben.
Alle Zahlen in zahlen.py nachgerechnet.
"""
import difflib
import json
import os
import re
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # scripts/lp/grafgeom.py
from grafgeom import achsenkisten, frei, kiste, masse       # Geometrie wie in build-clips.py

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
HIER = os.path.dirname(os.path.abspath(__file__)) + '/'
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150
PRAEFIX = 'koo-lp-'
WZ = json.load(open(HIER + 'wortzeiten.json')) if os.path.exists(HIER + 'wortzeiten.json') else {}
FEHLT = []

# ---------------------------------------------------------------- Zeiten auf den Ton
SPRECH = {}
ZAHLWORT = {'eins': '1', 'zwei': '2', 'drei': '3', 'vier': '4', 'fünf': '5', 'sechs': '6', 'sieben': '7', 'acht': '8',
            'neun': '9', 'zehn': '10', 'zwölf': '12', 'fünfzehn': '15', 'zwanzig': '20', 'dreissig': '30',
            'hundert': '100', 'null': '0'}
NENNERWORT = {'halb': '2', 'drittel': '3', 'viertel': '4', 'fünftel': '5'}


def passt(wort, gehoert):
    g = re.sub(r'[^\wäöü]', '', gehoert.lower().replace('ß', 'ss'))
    w_ = wort.lower()
    if not g:
        return False
    if w_ in ZAHLWORT and re.sub(r'\D', '', gehoert) == ZAHLWORT[w_]:
        return True
    if '⁄' in gehoert:
        z_, n_ = (re.sub(r'\D', '', t) for t in gehoert.split('⁄', 1))
        return (w_ in ZAHLWORT and z_ == ZAHLWORT[w_]) or (w_ in NENNERWORT and n_ == NENNERWORT[w_])
    if g.isdigit():
        return False
    if g.startswith(w_) or (len(w_) >= 6 and w_ in g):
        return True
    return (len(w_) >= 5 and w_[0] == g[0] and len(w_) <= len(g) <= len(w_) + 3
            and difflib.SequenceMatcher(None, w_, g).ratio() >= 0.8)


def wann(clip_, szene, wort, nr=1, dazu=0.0):
    """Sekunde ab Szenenbeginn, zu der `wort` zum nr-ten Mal beginnt; ohne Messung aus der Lage im Text geschätzt."""
    w = WZ.get(clip_.replace(PRAEFIX, ''), {}).get(szene)
    text = SPRECH.get((clip_, szene), '')
    if w and w.get('sprecher') == text:
        k = 0
        for wt, a, e in w['woerter']:
            if passt(wort, wt):
                k += 1
                if k == nr:
                    return round(max(0.3, a + dazu), 2)
    FEHLT.append((clip_, szene, wort))
    if w and w.get('sprecher') == text and w['woerter']:
        ws = text.split()
        k, idx = 0, None
        for i, t in enumerate(ws):
            if re.sub(r'[^\wäöü]', '', t.lower()).startswith(wort.lower()):
                k += 1
                if k == nr:
                    idx = i
                    break
        if idx is not None:
            j = min(len(w['woerter']) - 1, round(idx / len(ws) * len(w['woerter'])))
            return round(max(0.3, w['woerter'][j][1] + dazu), 2)
    pos, k = -1, 0
    for m in re.finditer(r'(?<!\w)' + re.escape(wort), text, re.I):
        k += 1
        if k == nr:
            pos = m.start()
            break
    if pos < 0:
        raise SystemExit('Wort nicht im Sprechertext: %s / %s / %s' % (clip_, szene, wort))
    d = len(text.split()) / 2.5 + 1.0
    return round(max(0.3, 0.4 + max(0, pos) / max(1, len(text)) * (d - 1.0) + dazu), 2)


def zeiten(clip_, szenen):
    """Ersetzt «@wort», «@wort#2», «@wort+0.3» in `ein`/`aus` und im ersten Feld jeder `bewegung`/`bahn`
    (Geraden, Steigungsdreiecke, Figuren) durch Sekunden."""
    def los(sname, v):
        if isinstance(v, str) and v.startswith('@'):
            m = re.match(r'@([^#+\-]+)(?:#(\d+))?(?:([+\-])([\d.]+))?$', v)
            dazu = float(m.group(4) or 0) * (-1 if m.group(3) == '-' else 1)
            return wann(clip_, sname, m.group(1), int(m.group(2) or 1), dazu)
        return v

    def lauf(sname, o):
        if isinstance(o, dict):
            for z in ('ein', 'aus'):
                if z in o:
                    o[z] = los(sname, o[z])
            for k in ('bewegung', 'bahn'):
                if isinstance(o.get(k), list):
                    o[k] = [[los(sname, b[0])] + list(b[1:]) for b in o[k]]
            for v in o.values():
                if isinstance(v, (dict, list)):
                    lauf(sname, v)
        elif isinstance(o, list):
            for v in o:
                lauf(sname, v)
    for q in szenen:
        SPRECH[(clip_, q['name'])] = q['sprecher']
    for q in szenen:
        lauf(q['name'], q['elemente'])


# ---------------------------------------------------------------- Bild (Helfer aus TALS lineare-funktionen)
def stelle(text, x, y, geraden, punkte, W, belegt):
    """Freie Stelle für eine feste Beschriftung — gerechnet, nicht geschätzt."""
    x0, x1, y0, y1, ex, ey = masse(W)
    dx, dy = 0.26 * (x1 - x0) / 9, 0.5 * (y1 - y0) / 9
    for k in (1, 1.6, 2.4, 3.4):
        for ax, ay, anker in ((1, -1, 'start'), (1, 1, 'start'), (-1, -1, 'end'), (-1, 1, 'end')):
            lx, ly = x + ax * dx, y + ay * dy * k
            kk = kiste(text, lx, ly, anker, ex, ey)
            if frei(kk, geraden, punkte, belegt, W, (x, y)):
                belegt.append(kk)
                return [round(lx, 3), round(ly, 3)], anker
    raise SystemExit('[FEHLER] keine freie Stelle fuer «%s» bei (%s | %s) im Fenster %s' % (text, x, y, W))


def graf(W, geraden=(), punkte=(), ein=0.05, mit_geraden=(), **kw):
    """`mit_geraden`: (m, b) weiterer Geraden, die beim Freihalten der Beschriftungen zählen (aus anderen Bildern)."""
    ger_l = [(g['m'], g['q']) for g in geraden if 'm' in g] + list(mit_geraden)
    ger_l += [(g['bewegung'][-1][1], g['bewegung'][-1][2]) for g in geraden if 'bewegung' in g]
    pkt_l = [(p['x'], p['y']) for p in punkte]
    belegt = achsenkisten(dict(W, **{k: v for k, v in kw.items() if k in ('xname', 'yname')}))
    for p in punkte:
        if p.get('beschriftung') and 'beschriftung_bei' not in p:
            p['beschriftung_bei'], p['anker'] = stelle(p['beschriftung'], p['x'], p['y'], ger_l, pkt_l, W, belegt)
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             geraden=list(geraden), punkte=list(punkte), pfeile=True, tippbar=True, **W)
    g.update(kw)
    return g


def ueber(W, geraden=(), punkte=(), ein=0.05, **kw):
    """Zweites Bild deckungsgleich über dem ersten, nur Inhalt (ohne Achsen und Karo)."""
    return graf(W, geraden, punkte, ein=ein, achsen=False, raster=False, **kw)


def ger(m, q, farbe=1, gestrichelt=False, dicke=None):
    d = dict(m=m, q=q, farbe=farbe)
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = dicke or 3
    elif dicke:
        d['dicke'] = dicke
    return d


def bew(stuetz, farbe=1, yachse=None, dreieck=None, gestrichelt=False):
    """Bewegte (oder mit Begleitern gezeigte) Gerade: Stützpunkte [t, m, b] ab Szenenbeginn."""
    d = {'bewegung': stuetz, 'farbe': farbe}
    if gestrichelt:
        d['gestrichelt'] = True
        d['dicke'] = 3
    if yachse is not None:
        d['yachse'] = yachse
    if dreieck is not None:
        d['dreieck'] = dreieck
    return d


def dreieck(x, dx, bahn=None, ein=None):
    d = {'bahn': bahn, 'farbe': 5} if bahn else {'x': x, 'dx': dx, 'farbe': 5}
    if ein is not None:
        d['ein'] = ein
    return d


def pt(x, y, farbe=5, text=None, bei=None, anker='start'):
    d = dict(x=x, y=y, farbe=farbe, anker=anker)
    if text:
        d['beschriftung'] = text
    if bei:
        d['beschriftung_bei'] = bei
    return d


def r3(v):
    return round(v, 3)


def S(a, b, farbe=5, dicke=4, gest=False, **kw):
    d = dict(art='strecke', von=[r3(a[0]), r3(a[1])], bis=[r3(b[0]), r3(b[1])], farbe=farbe, dicke=dicke, **kw)
    if gest:
        d['gestrichelt'] = True
    return d


def T(x, y, text, farbe=5, anker='middle', g=30, **kw):
    return dict(art='text', bei=[r3(x), r3(y)], text=text, farbe=farbe, anker=anker, groesse=g, kursiv=False, **kw)


# ---------------------------------------------------------------- Text und Szenen
def f(t, y, g=56, ein=0.8, x=LX):
    return dict(typ='formel', text=t, x=x, y=y, groesse=g, ein=ein)


def n(t, y, farbe='blau', g=44, ein=2.4):
    return dict(typ='notiz', text=t, x=LX, y=y, groesse=g, farbe=farbe, ein=ein)


def titel(t, y=280, g=86):
    return dict(typ='titel', text=t, x=LX, y=y, groesse=g)


def sz(name, spr, *el):
    spr = spr.replace('Δy', 'delta y').replace('Δx', 'delta x')          # Piper liest «Δ» nicht
    return dict(name=name, layout='zentriert', oben=200, sprecher=spr, elemente=list(el))


def wahl(szene, text, opt, richtig, rueck, sprich=None, rueck_sprich=None, bei=0.3):
    """Die richtige Antwort steht nicht immer zuoberst (deterministisch gedreht, wie in den Vorbildern)."""
    k = zlib.crc32((szene + '|' + text).encode('utf-8')) % len(opt)
    dreh = lambda i: (i - k) % len(opt)
    opt = [opt[(i + k) % len(opt)] for i in range(len(opt))]
    d = {'szene': szene, 'bei': bei, 'typ': 'wahl', 'text': text, 'optionen': opt,
         'richtig': dreh(richtig), 'rueck': {str(dreh(i)): v for i, v in rueck.items()}}
    if sprich:
        d['sprich'] = sprich
    if rueck_sprich:
        d['rueck_sprich'] = {str(dreh(i)): v for i, v in rueck_sprich.items()}
    return d


def klick(szene, text, ziel, richtig_text, fallen, falsch_text, sprich=None, falsch_sprich=None, tol=0.6, bei=0.3):
    d = {'szene': szene, 'bei': bei, 'typ': 'klick', 'text': text, 'ziel': ziel, 'toleranz': tol,
         'richtig_text': richtig_text, 'fallen': fallen, 'falsch_text': falsch_text, 'eingabe': ['x', 'y']}
    if sprich:
        d['sprich'] = sprich
    if falsch_sprich:
        d['falsch_sprich'] = falsch_sprich
    return d


def jetzt_du(wo='in der Animation'):
    return sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge %s unter dem Clip und löse die Aufgaben.' % wo,
              titel('Jetzt du', 280, 86),
              n('Erkunde diese Zusammenhänge|%s unter dem Clip|und löse die Aufgaben.' % wo, 430, 'blau', 50, ein=0.6))


def merke(spr, zeilen):
    return sz('Merke', spr, titel('Zum Mitnehmen', 250, 76), n(zeilen, 400, 'blau', 44, ein=1.2))


def hoehe(el):
    g, t = el.get('groesse', 50), el.get('text', '')
    if el['typ'] == 'notiz':
        return 1.35 * g * (t.count('|') + 1)
    if '\\begin{array}' in t:
        return 2.9 * g
    if '\\dfrac' in t:
        return 2.25 * g
    return 1.35 * g


def abstaende(szenen, luft=26):
    """Schiebt Zeilen der linken Spalte nach unten, bis keine die nächste berührt."""
    for q in szenen:
        zeilen = sorted((el for el in q['elemente'] if el['typ'] in ('formel', 'notiz', 'titel') and el.get('x') == LX
                         and 'aus' not in el), key=lambda el: el['y'])
        for a_, b_ in zip(zeilen, zeilen[1:]):
            unten = a_['y'] + hoehe(a_) + luft
            if b_['y'] < unten:
                b_['y'] = int(round(unten))
        if zeilen and zeilen[-1]['y'] + hoehe(zeilen[-1]) > 1020:
            print('  zu tief:', q['name'], zeilen[-1]['y'])


# Was das Bild beim Erscheinen einer Kontrollfrage zeigen darf: genau das Gegebene.
# (Clip, Szene) -> (Fenster, feste Geraden, Punkte, Extras); fehlt eine Szene, bleiben nur die Achsen.
FRAGEBILD = {}


def fragebild(name, szene):
    grafen = [e for e in szene['elemente'] if e.get('typ') == 'graf']
    if not grafen:
        return
    W, geraden, punkte, extra = FRAGEBILD.get((name, szene['name']), (None, [], [], {}))
    if W is None:
        W = {k: grafen[0][k] for k in ('xbereich', 'ybereich', 'xteilung', 'yteilung') if k in grafen[0]}
        extra = {k: grafen[0][k] for k in ('xname', 'yname') if k in grafen[0]}
    for g in grafen:
        g['ein'] = max(g.get('ein', 0.05), 1.0)
    szene['elemente'].insert(0, graf(W, geraden, punkte, **extra))


def clip(name, folge, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip'):
    dname = PRAEFIX + name
    if art == 'Kontrollclip':
        for q in szenen:
            if q['name'].startswith('Frage'):
                fragebild(name, q)
    zeiten(dname, szenen)
    abstaende(szenen)
    alt = R + 'clips/' + dname + '.json'
    if os.path.exists(alt):
        frueher = {q['name']: (q.get('sprecher'), q.get('dauer')) for q in json.load(open(alt))['szenen']}
        for k, q in enumerate(szenen):
            spr, d_ = frueher.get(q['name'], (None, None))
            if d_:
                q['dauer'] = d_
            if spr is not None and spr != q['sprecher']:
                print('  neu zu vertonen:', dname, 'Szene', k + 1, q['name'])
    d = {'titel': titel_, 'dateiname': dname, 'kurzbeschrieb': kurz,
         'schlagworte': schlag, 'themenbereich': 'Geometrie · Abbildungen und Geraden im Koordinatensystem',
         'fach': 'Sekundarstufe I', 'lerngebiet': '5 · Geometrie',
         'lektion': ['lp-koordinaten'], 'stufe': ['Sek I'], 'datum': '2026-10-10',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Geometrie', 'folge': folge,
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms koordinaten; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + dname + '.json', 'w'), ensure_ascii=False, indent=1)
    print(dname, len(szenen), 'Szenen', len(fragen or []), 'Fragen')


def mit(fg, **kw):
    d = dict(fg)
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def teil(*werte):
    return [[v, str(v).replace('-', '−')] for v in werte]


# ---------------------------------------------------------------- Bausteine
def V(pkte, farbe=1, fu=0.15, **kw):
    return dict(art='vieleck', punkte=[[r3(x), r3(y)] for x, y in pkte], farbe=farbe, fuellung=fu, **kw)


def rechteck(x, y, farbe=1, **kw):
    return V([(0, 0), (x, 0), (x, y), (0, y)], farbe, 0.15, **kw)


def kurve(formel, von, bis, farbe=1):
    return dict(formel=formel, farbe=farbe, von=von, bis=bis)


def zug(punkte, farbe=1, dicke=5, **kw):
    """Streckenzug (Weg-Zeit-Graph) als Strecken."""
    return [S(a, b, farbe, dicke, **kw) for a, b in zip(punkte, punkte[1:])]


# ---------------------------------------------------------------- Geometrie-Bausteine
import math


def geo(W, figuren=(), ein=0.05, raster=True, **kw):
    """Figur ohne Achsen, im Karo (raster) oder auf leerem Grund."""
    d = graf(W, ein=ein, achsen=False, raster=raster, **kw)
    d['figuren'] = list(figuren)
    return d


def dazu(W, figuren, ein):
    """Deckungsgleich über dem Grundbild: kommt bei `ein` dazu."""
    d = ueber(W, ein=ein)
    d['figuren'] = list(figuren)
    return d


def RW(p, r1, r2, farbe=5):
    return dict(art='rechts', bei=[r3(p[0]), r3(p[1])], r1=r1, r2=r2, farbe=farbe, px=22)


def KR(m, r, farbe=5, fu=0.0, **kw):
    return dict(art='kreis', m=[r3(m[0]), r3(m[1])], r=r3(r), farbe=farbe, fuellung=fu, **kw)


def segment(r, d, n=60):
    """Kreissegment unter einer waagrechten Sehne im Abstand d unter dem Mittelpunkt (Wasser im Rohr)."""
    hs = math.sqrt(r * r - d * d)
    a0 = math.pi + math.atan2(d, hs)
    a1 = 2 * math.pi - math.atan2(d, hs)
    return [(r * math.cos(a0 + (a1 - a0) * k / n), r * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]


def fenster(x0, x1, y0, y1):
    assert abs((x1 - x0) - (y1 - y0)) < 1e-9, 'Fenster nicht quadratisch'
    return dict(xbereich=[x0, x1], ybereich=[y0, y1])


# ---------------------------------------------------------------- Fenster und Bausteine
WK = dict(xbereich=[-7, 7], ybereich=[-7, 7], xteilung=teil(-6, -4, -2, 2, 4, 6), yteilung=teil(-6, -4, -2, 2, 4, 6))


W9 = dict(xbereich=[-2, 10], ybereich=[-2, 10], xteilung=teil(2, 4, 6, 8), yteilung=teil(2, 4, 6, 8))   # Streckung mit Z(1|1), k = 3


def ks(punkte=(), figuren=(), ein=0.05, W=None, **kw):
    d = graf(W or WK, punkte=list(punkte), ein=ein, **kw)
    d['figuren'] = list(figuren)
    return d


def ksdazu(punkte=(), figuren=(), ein=0.05, W=None):
    d = ueber(W or WK, punkte=list(punkte), ein=ein)
    d['figuren'] = list(figuren)
    return d


def P_(x, y, farbe, name, bei=None, anker='start'):
    return pt(x, y, farbe, name, bei, anker)


def dreieck_(pk, farbe, fu=0.15):
    return V(pk, farbe, fu)


# ════════════════════════════════════════════════ Kapitel 1 · Einführung: Punktspiegelung
clip('punktspiegelung', 1, 'Geometrie: Punktspiegelung',
     'P(5 | 3) am Zentrum Z(2 | 1): Weg von P nach Z nochmals gehen, P\'(−1 | −1); Formel P\' = 2Z − P; Vorhersage Q(3 | 4) → (1 | −2); '
     'Zentrum gesucht: Mitte von P und P\'; Dreieck am Ursprung: beide Vorzeichen wechseln, Drehung um 180°; Fehler: P + Z.',
     ['Punktspiegelung', 'Zentrum', 'Koordinaten', 'Abbildung'], [
         sz('Weg',
            'Spiegle den Punkt P mit fünf und drei am Zentrum Z mit zwei und eins. Von P nach Z gehst du drei nach links und zwei nach unten. Geh denselben Weg ab Z nochmals: Du landest bei P Strich mit minus eins und minus eins.',
            n('P(5 ∣ 3) → Z(2 ∣ 1): −3 und −2|nochmals ab Z: P\'(−1 ∣ −1)', 300, 'blau', 42, ein='@Weg'),
            ks([P_(5, 3, 1, 'P', [5.3, 3.6]), P_(2, 1, 3, 'Z', [2.3, 0.4])]),
            ksdazu(figuren=[S((5, 3), (2, 1), 5, 4, gest=True)], ein='@links'),
            ksdazu([P_(-1, -1, 2, "P'", [-1.3, -1.7], 'end')], [S((2, 1), (-1, -1), 2, 4, gest=True)], '@nochmals')),
         sz('Formel',
            'Z liegt genau in der Mitte zwischen P und P Strich. Darum gilt für jede Koordinate: P Strich gleich zwei mal Z minus P. Zwei mal zwei minus fünf gibt minus eins, zwei mal eins minus drei gibt minus eins.',
            f(r"P' = 2Z - P", 280, 64, ein='@Darum'),
            f(r"(2 \cdot 2 - 5 \mid 2 \cdot 1 - 3) = \fb{(-1 \mid -1)}", 400, 48, ein='@Zwei'),
            ks([P_(5, 3, 1, 'P', [5.3, 3.6]), P_(2, 1, 3, 'Z', [2.3, 0.4]), P_(-1, -1, 2, "P'", [-1.3, -1.7], 'end')], [S((5, 3), (-1, -1), 5, 3, gest=True)])),
         sz('Vorhersage',
            'Q mit drei und vier, Zentrum zwei und eins: Zwei mal zwei minus drei gibt eins, zwei mal eins minus vier gibt minus zwei. Q Strich liegt bei eins und minus zwei.',
            f(r"Q' = (4 - 3 \mid 2 - 4) = \fb{(1 \mid -2)}", 300, 50, ein='@Zwei'),
            ks([P_(3, 4, 1, 'Q', [3.3, 4.6]), P_(2, 1, 3, 'Z', [2.4, 0.4])]),
            ksdazu([P_(1, -2, 2, "Q'", [0.7, -2.7], 'end')], [S((3, 4), (1, -2), 5, 3, gest=True)], '@liegt')),
         sz('Mitte',
            'Kennst du P und P Strich, findest du das Zentrum als Mitte: Addiere je die beiden Koordinaten und teile durch zwei. P mit fünf und drei, P Strich mit minus eins und minus eins: Fünf plus minus eins durch zwei gibt zwei, drei plus minus eins durch zwei gibt eins. Das Zentrum liegt bei zwei und eins.',
            f(r"Z = \left(\dfrac{5 + (-1)}{2} \;\middle|\; \dfrac{3 + (-1)}{2}\right) = \fc{(2 \mid 1)}", 300, 44, ein='@Addiere'),
            ks([P_(5, 3, 1, 'P', [5.3, 3.6]), P_(-1, -1, 2, "P'", [-1.3, -1.7], 'end')], [S((5, 3), (-1, -1), 5, 3, gest=True)]),
            ksdazu([P_(2, 1, 3, 'Z', [2.3, 0.4])], [], '@Zentrum#2')),
         sz('Figur',
            'Eine Figur spiegelst du Ecke für Ecke. Am Ursprung wechseln bei jeder Ecke beide Vorzeichen. Das Bild ist um hundertachtzig Grad gedreht: Längen, Winkel und Fläche bleiben gleich.',
            n('am Ursprung: beide Vorzeichen wechseln|Drehung um 180°: Fläche bleibt', 300, 'blau', 42, ein='@Ursprung'),
            ks([], [dreieck_([(1, 1), (4, 1), (2, 3)], 1)]),
            ksdazu([P_(0, 0, 3, 'Z', [0.3, -0.7])], [dreieck_([(-1, -1), (-4, -1), (-2, -3)], 2), S((4, 1), (-4, -1), 5, 2, gest=True), S((2, 3), (-2, -3), 5, 2, gest=True)], '@Vorzeichen')),
         sz('Fehler',
            'Häufiger Fehler: P und Z einfach addieren. Fünf plus zwei und drei plus eins gibt sieben und vier. Dann liegt Z aber nicht in der Mitte. Prüf immer: Ist Z die Mitte zwischen P und P Strich?',
            f(r"\fd{P + Z = (7 \mid 4)}", 300, 56, ein='@addieren'),
            n('Probe: Z ist die Mitte von P und P\'', 430, 'blau', 42, ein='@Prüf'),
            ks([P_(5, 3, 1, 'P', [5.3, 3.6]), P_(2, 1, 3, 'Z', [2.3, 0.4])], W=W9),
            ksdazu([pt(7, 4, 4, '(7 | 4)', [6.7, 4.6], 'end')], [], '@sieben', W=W9)),
         merke("Zum Mitnehmen: Bei der Punktspiegelung liegt das Zentrum in der Mitte zwischen Punkt und Bild. Rechne für jede Koordinate zwei mal Z minus P.",
               "Z ist die Mitte von P und P'|P' = 2Z − P, jede Koordinate|Längen und Flächen bleiben"),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Q(3 | 4) wird am Zentrum Z(2 | 1) gespiegelt. Wo liegt Q\'?', ['(1 | −2)', '(5 | 5)', '(−1 | −3)'], 0,
              {0: 'Ja.', 1: 'Das ist Q + Z. Liegt Z dann in der Mitte?', 2: 'Das ist Z − Q. Geh von Q bis Z und nochmals gleich weit.'},
              sprich='Q mit drei und vier wird am Zentrum Z mit zwei und eins gespiegelt. Wo liegt Q Strich?',
              rueck_sprich={1: 'Das ist Q plus Z. Liegt Z dann in der Mitte?', 2: 'Das ist Z minus Q. Geh von Q bis Z und nochmals gleich weit.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
FRAGEBILD.update({('kontrolle-punktspiegelung', 'Frage 3'): (WK, [], [P_(2, 5, 1, 'P(2 | 5)', [2.3, 5.6]), P_(6, 1, 2, "P'(6 | 1)", [5.7, 1.7], 'end')], {})})
clip('kontrolle-punktspiegelung', 2, 'Geometrie: Kontrollfragen zur Punktspiegelung',
     'Fünf Fragen: P(3 | −4) am Ursprung, P(4 | 6) an Z(1 | 2), Zentrum aus P(2 | 5) und P\'(6 | 1), Fläche bleibt, Fehler P + Z.',
     ['Punktspiegelung', 'Kontrollfragen'], [
         sz('Frage 1', 'Am Ursprung wechseln beide Vorzeichen: minus drei und vier.',
            f(r"P' = \fc{(-3 \mid 4)}", 330, 60, ein=1.0)),
         sz('Frage 2', 'Zwei mal eins minus vier gibt minus zwei, zwei mal zwei minus sechs gibt minus zwei.',
            f(r"P' = (2 - 4 \mid 4 - 6) = \fc{(-2 \mid -2)}", 330, 50, ein=1.0)),
         sz('Frage 3', 'Das Zentrum ist die Mitte: zwei plus sechs durch zwei gibt vier, fünf plus eins durch zwei gibt drei.',
            f(r"Z = \fc{(4 \mid 3)}", 330, 60, ein=1.0),
            ks([P_(2, 5, 1, 'P(2 | 5)', [2.3, 5.6]), P_(6, 1, 2, "P'(6 | 1)", [5.7, 1.7], 'end'), P_(4, 3, 3, 'Z', [4.4, 3.6])], [S((2, 5), (6, 1), 5, 3, gest=True)])),
         sz('Frage 4', 'Die Punktspiegelung dreht die Figur nur. Die Fläche bleibt sechs.',
            n('Fläche bleibt 6', 330, 'gruen', 50, ein=1.0)),
         sz('Frage 5', 'Nein. Zwei mal eins minus drei gibt minus eins, zwei mal null minus eins gibt minus eins. Richtig ist minus eins und minus eins.',
            f(r"P' = \fc{(-1 \mid -1)}", 330, 60, ein=1.0)),
         merke("Zum Mitnehmen: Das Zentrum ist die Mitte. Bildpunkt gleich zwei mal Z minus P, Zentrum gleich Mittelpunkt von P und P Strich.",
               "P' = 2Z − P|Z = Mitte von P und P'"),
     ], [
         wahl('Frage 1', 'P(3 | −4) wird am Ursprung gespiegelt. Wo liegt P\'?', ['(−3 | 4)', '(3 | 4)', '(−3 | −4)'], 0,
              {0: 'Ja.', 1: 'Nur ein Vorzeichen gewechselt. Am Ursprung wechseln beide.', 2: 'Nur ein Vorzeichen gewechselt. Am Ursprung wechseln beide.'},
              sprich='P mit drei und minus vier wird am Ursprung gespiegelt. Wo liegt P Strich?',
              rueck_sprich={1: 'Nur ein Vorzeichen gewechselt. Am Ursprung wechseln beide.', 2: 'Nur ein Vorzeichen gewechselt. Am Ursprung wechseln beide.'}),
         wahl('Frage 2', 'Spiegle P(4 | 6) am Zentrum Z(1 | 2).', ['(−2 | −2)', '(5 | 8)', '(−3 | −4)'], 0,
              {0: 'Ja.', 1: 'Das ist P + Z. Liegt Z in der Mitte?', 2: 'Das ist Z − P. Geh von P bis Z und nochmals gleich weit.'},
              sprich='Spiegle P mit vier und sechs am Zentrum Z mit eins und zwei.',
              rueck_sprich={1: 'Das ist P plus Z. Liegt Z in der Mitte?', 2: 'Das ist Z minus P. Geh von P bis Z und nochmals gleich weit.'}),
         wahl('Frage 3', 'Wo liegt das Zentrum Z, wenn P im Bild auf P\' fällt?', ['(4 | 3)', '(8 | 6)', '(4 | −4)'], 0,
              {0: 'Ja.', 1: 'Das ist die Summe. Die Mitte ist die Summe durch 2.', 2: 'Das ist der Weg von P nach P\'. Z liegt in seiner Mitte.'},
              sprich='Wo liegt das Zentrum Z, wenn P im Bild auf P Strich fällt?',
              rueck_sprich={1: 'Das ist die Summe. Die Mitte ist die Summe durch zwei.', 2: 'Das ist der Weg von P nach P Strich. Z liegt in seiner Mitte.'}),
         wahl('Frage 4', 'Ein Dreieck mit Fläche 6 wird punktgespiegelt. Wie gross ist das Bild?', ['6', '12', '−6'], 0,
              {0: 'Ja.', 1: 'Eine Spiegelung vergrössert nicht.', 2: 'Flächen sind nie negativ, auch wenn die Koordinaten negativ werden.'},
              sprich='Ein Dreieck mit Fläche sechs wird punktgespiegelt. Wie gross ist das Bild?',
              rueck_sprich={1: 'Eine Spiegelung vergrössert nicht.', 2: 'Flächen sind nie negativ, auch wenn die Koordinaten negativ werden.'}),
         wahl('Frage 5', 'Ali spiegelt P(3 | 1) an Z(1 | 0) und schreibt P\'(4 | 1). Stimmt das?', ['nein, P\'(−1 | −1)', 'ja', 'nein, P\'(2 | 1)'], 0,
              {0: 'Ja.', 1: 'Prüf: Liegt Z in der Mitte der beiden Punkte?', 2: 'Das ist P − Z. Rechne 2Z − P.'},
              sprich='Ali spiegelt P mit drei und eins an Z mit eins und null und schreibt P Strich mit vier und eins. Stimmt das?',
              rueck_sprich={1: 'Prüf: Liegt Z in der Mitte der beiden Punkte?', 2: 'Das ist P minus Z. Rechne zwei mal Z minus P.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung: Achsenspiegelung
clip('achsenspiegelung', 3, 'Geometrie: Achsenspiegelung',
     'P(3 | 2) an der x-Achse (3 | −2), an der y-Achse (−3 | 2), an x = 1 (−1 | 2); Vorhersage Q(4 | 1) an x = 2 → (0 | 1); '
     'Achse gesucht: Mitte von P(−4 | −2) und P\'(2 | −2), x = −1; an y = x Koordinaten tauschen (5 | 1) → (1 | 5); schräge Achse x + y = 4 konstruiert; Fehler: falsche Koordinate.',
     ['Achsenspiegelung', 'Spiegelachse', 'Koordinaten'], [
         sz('xAchse',
            'Spiegle P mit drei und zwei an der x-Achse. P liegt zwei über der Achse, also liegt das Bild zwei darunter: drei und minus zwei. Die x-Koordinate bleibt, nur das Vorzeichen von y wechselt.',
            f(r"(x \mid y) \to (x \mid -y)", 300, 56, ein='@bleibt'),
            ks([P_(3, 2, 1, 'P', [3.3, 2.6])], [S((-7, 0), (7, 0), 3, 6)]),
            ksdazu([P_(3, -2, 2, "P'", [3.3, -2.7])], [S((3, 2), (3, -2), 5, 3, gest=True)], '@darunter')),
         sz('yAchse',
            'An der y-Achse ist es umgekehrt: y bleibt, x wechselt das Vorzeichen. P Strich liegt bei minus drei und zwei.',
            f(r"(x \mid y) \to (-x \mid y)", 300, 56, ein='@umgekehrt'),
            ks([P_(3, 2, 1, 'P', [3.3, 2.6])], [S((0, -7), (0, 7), 3, 6)]),
            ksdazu([P_(-3, 2, 2, "P'", [-3.3, 2.6], 'end')], [S((3, 2), (-3, 2), 5, 3, gest=True)], '@Strich')),
         sz('Parallele',
            'Die Achse kann auch die Gerade x gleich eins sein. P ist zwei rechts davon, das Bild zwei links davon: minus eins und zwei. Gerechnet: zwei mal eins minus drei. Genauso an einer waagrechten Achse y gleich b: Dann ändert sich nur y.',
            f(r"x' = 2 \cdot 1 - 3 = -1", 300, 56, ein='@Gerechnet'),
            f(r"y = b: \;\; y' = 2b - y", 420, 50, ein='@waagrechten'),
            ks([P_(3, 2, 1, 'P', [3.3, 2.6])], [S((1, -7), (1, 7), 3, 6)]),
            ksdazu([P_(-1, 2, 2, "P'", [-1.3, 2.6], 'end')], [S((3, 2), (-1, 2), 5, 3, gest=True)], '@links')),
         sz('Vorhersage',
            'Q mit vier und eins liegt zwei rechts der Achse x gleich zwei. Das Bild liegt zwei links davon, bei null und eins.',
            f(r"Q' = (2 \cdot 2 - 4 \mid 1) = \fb{(0 \mid 1)}", 300, 50, ein='@Bild'),
            ks([P_(4, 1, 1, 'Q', [4.3, 1.6])], [S((2, -7), (2, 7), 3, 6)]),
            ksdazu([P_(0, 1, 2, "Q'", [-0.3, 1.6], 'end')], [S((4, 1), (0, 1), 5, 3, gest=True)], '@Bild')),
         sz('Gesucht',
            'Kennst du P und P Strich, findest du die Achse: Sie geht durch die Mitte der beiden Punkte und steht senkrecht auf ihrer Verbindung. P mit minus vier und minus zwei, P Strich mit zwei und minus zwei: Die Mitte von minus vier und zwei ist minus eins. Die Achse ist die Gerade x gleich minus eins.',
            f(r"\dfrac{-4 + 2}{2} = -1 \;\Rightarrow\; \fc{x = -1}", 300, 50, ein='@Mitte#2'),
            ks([P_(-4, -2, 1, 'P', [-4.3, -1.4], 'end'), P_(2, -2, 2, "P'", [2.3, -1.4])], [S((-4, -2), (2, -2), 5, 3, gest=True)]),
            ksdazu(figuren=[S((-1, -7), (-1, 7), 3, 6), RW((-1, -2), 0, 90)], ein='@Achse#2')),
         sz('Diagonale',
            'An der Geraden y gleich x tauschen die Koordinaten ihre Plätze. Aus fünf und eins wird eins und fünf. Die Verbindung steht wieder senkrecht auf der Achse.',
            f(r"(x \mid y) \to (y \mid x)", 300, 56, ein='@tauschen'),
            ks([P_(5, 1, 1, 'P', [5.4, 0.5])], [S((-7, -7), (7, 7), 3, 6)]),
            ksdazu([P_(1, 5, 2, "P'", [0.7, 5.6], 'end')], [S((5, 1), (1, 5), 5, 3, gest=True), RW((3, 3), 45, 135)], '@wird')),
         sz('Schraeg',
            'Bei einer anderen schrägen Achse konstruierst du: Zeichne durch P die Senkrechte zur Achse, miss den Abstand und trag ihn auf der anderen Seite gleich weit ab.',
            n('Senkrechte durch P|Abstand messen|gleich weit dahinter abtragen', 300, 'blau', 44, ein='@konstruierst'),
            ks([P_(5, 3, 1, 'P', [5.4, 3.4])], [S((-3, 7), (7, -3), 3, 6)]),                     # Achse x + y = 4: P(5|3) → P'(1|−1), Fusspunkt (3|1)
            ksdazu(figuren=[S((5, 3), (3, 1), 5, 3, gest=True), RW((3, 1), 45, 135)], ein='@Senkrechte'),
            ksdazu([P_(1, -1, 2, "P'", [0.6, -1.6], 'end')], [S((3, 1), (1, -1), 5, 3, gest=True)], ein='@gleich')),
         sz('Fehler',
            'Häufiger Fehler: die falsche Koordinate ändern. An der x-Achse bleibt x gleich, es ändert sich nur y.',
            f(r"\fd{(3 \mid 2) \to (-3 \mid 2)}", 300, 56, ein='@Fehler'),
            n('x-Achse: nur y ändert sich', 430, 'rot', 44, ein='@ändert')),
         merke('Zum Mitnehmen: Punkt und Bild liegen gleich weit von der Achse, ihre Verbindung steht senkrecht darauf. An einer waagrechten Achse ändert sich y, an einer senkrechten x, an y gleich x tauschen die Koordinaten.',
               'gleich weit, Verbindung senkrecht|waagrechte Achse: y ändert sich|y = x: Koordinaten tauschen'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Q(4 | 1) wird an der Geraden x = 2 gespiegelt. Wo liegt Q\'?', ['(0 | 1)', '(4 | −1)', '(−4 | 1)'], 0,
              {0: 'Ja.', 1: 'Das wäre an der x-Achse. Die Achse x = 2 ist senkrecht: x ändert sich.', 2: 'Das wäre an der y-Achse. Die Achse liegt bei x = 2.'},
              sprich='Q mit vier und eins wird an der Geraden x gleich zwei gespiegelt. Wo liegt Q Strich?',
              rueck_sprich={1: 'Das wäre an der x-Achse. Die Achse x gleich zwei ist senkrecht: x ändert sich.', 2: 'Das wäre an der y-Achse. Die Achse liegt bei x gleich zwei.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
FRAGEBILD.update({('kontrolle-achsenspiegelung', 'Frage 5'): (WK, [], [P_(2, 5, 1, 'P(2 | 5)', [2.4, 5.6]), P_(2, -1, 2, "P'(2 | −1)", [2.4, -1.7])], {})})
clip('kontrolle-achsenspiegelung', 4, 'Geometrie: Kontrollfragen zur Achsenspiegelung',
     'Fünf Fragen: P(−4 | 1) an der y-Achse, P(2 | 3) an x = 5, P(6 | −1) an y = x, P(0 | 4) an y = 1, Achse aus (2 | 5) und (2 | −1).',
     ['Achsenspiegelung', 'Kontrollfragen'], [
         sz('Frage 1', 'An der y-Achse wechselt nur das Vorzeichen von x: vier und eins.',
            f(r"P' = \fc{(4 \mid 1)}", 330, 60, ein=1.0)),
         sz('Frage 2', 'P ist drei links der Achse, das Bild drei rechts: acht und drei.',
            f(r"x' = 2 \cdot 5 - 2 = \fc{8}", 330, 56, ein=1.0)),
         sz('Frage 3', 'An y gleich x tauschen die Koordinaten: minus eins und sechs.',
            f(r"P' = \fc{(-1 \mid 6)}", 330, 60, ein=1.0)),
         sz('Frage 4', 'P ist drei über der Achse y gleich eins, das Bild drei darunter: null und minus zwei.',
            f(r"y' = 2 \cdot 1 - 4 = \fc{-2}", 330, 56, ein=1.0)),
         sz('Frage 5', 'Nur y ändert sich, die Achse ist waagrecht. Sie liegt in der Mitte von fünf und minus eins: y gleich zwei.',
            f(r"y = \dfrac{5 + (-1)}{2} = \fc{2}", 330, 50, ein=1.0),
            ks([P_(2, 5, 1, 'P(2 | 5)', [2.4, 5.6]), P_(2, -1, 2, "P'(2 | −1)", [2.4, -1.7])], [S((-7, 2), (7, 2), 3, 6)])),
         merke('Zum Mitnehmen: Gleich weit von der Achse, Verbindung senkrecht. Die Achse liegt in der Mitte zwischen Punkt und Bild.',
               'gleich weit, senkrecht|Achse in der Mitte'),
     ], [
         wahl('Frage 1', 'P(−4 | 1) wird an der y-Achse gespiegelt. Wo liegt P\'?', ['(4 | 1)', '(−4 | −1)', '(4 | −1)'], 0,
              {0: 'Ja.', 1: 'Das wäre an der x-Achse.', 2: 'Beide Vorzeichen gewechselt: Das wäre am Ursprung.'},
              sprich='P mit minus vier und eins wird an der y-Achse gespiegelt. Wo liegt P Strich?',
              rueck_sprich={1: 'Das wäre an der x-Achse.', 2: 'Beide Vorzeichen gewechselt: Das wäre am Ursprung.'}),
         wahl('Frage 2', 'Spiegle P(2 | 3) an der Geraden x = 5.', ['(8 | 3)', '(−2 | 3)', '(2 | 7)'], 0,
              {0: 'Ja.', 1: 'Das wäre an der y-Achse. Die Achse liegt bei x = 5.', 2: 'Die Achse x = 5 ist senkrecht: y bleibt gleich.'},
              sprich='Spiegle P mit zwei und drei an der Geraden x gleich fünf.',
              rueck_sprich={1: 'Das wäre an der y-Achse. Die Achse liegt bei x gleich fünf.', 2: 'Die Achse x gleich fünf ist senkrecht: y bleibt gleich.'}),
         wahl('Frage 3', 'Bild von P(6 | −1) an der Geraden y = x?', ['(−1 | 6)', '(1 | −6)', '(−6 | 1)'], 0,
              {0: 'Ja.', 1: 'Tauschen, ohne die Vorzeichen zu ändern.', 2: 'Tauschen heisst: x wird y und y wird x.'},
              sprich='Was ist das Bild von P mit sechs und minus eins an der Geraden y gleich x?',
              rueck_sprich={1: 'Tauschen, ohne die Vorzeichen zu ändern.', 2: 'Tauschen heisst: x wird y und y wird x.'}),
         wahl('Frage 4', 'Wohin kommt P(0 | 4) an der Geraden y = 1?', ['(0 | −2)', '(0 | −4)', '(0 | 2)'], 0,
              {0: 'Ja.', 1: 'Das wäre an der x-Achse. Die Achse liegt bei y = 1.', 2: 'Das Bild liegt gleich weit unter der Achse wie P darüber.'},
              sprich='Wohin kommt P mit null und vier an der Geraden y gleich eins?',
              rueck_sprich={1: 'Das wäre an der x-Achse. Die Achse liegt bei y gleich eins.', 2: 'Das Bild liegt gleich weit unter der Achse wie P darüber.'}),
         wahl('Frage 5', 'Welche Gerade ist die Spiegelachse für P und P\' im Bild?', ['y = 2', 'x = 2', 'y = 3'], 0,
              {0: 'Ja.', 1: 'P und P\' liegen beide auf x = 2. Die Achse steht senkrecht auf ihrer Verbindung.', 2: 'Das ist die halbe Differenz. Die Achse liegt in der Mitte von 5 und −1.'},
              sprich='Welche Gerade ist die Spiegelachse für P und P Strich im Bild?',
              rueck_sprich={1: 'P und P Strich liegen beide auf x gleich zwei. Die Achse steht senkrecht auf ihrer Verbindung.', 2: 'Das ist die halbe Differenz. Die Achse liegt in der Mitte von fünf und minus eins.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung: Zentrische Streckung und Flächen
DR = [(1, 1), (3, 1), (1, 2)]
DR2 = [(2, 2), (6, 2), (2, 4)]
clip('streckung', 5, 'Geometrie: Zentrische Streckung und Flächen',
     'Dreieck (1 | 1), (3 | 1), (1 | 2) mit Z(0 | 0), k = 2: Koordinaten mal 2; Vorhersage Fläche 1 → 4; Zentrum Z(1 | 1), k = 3: P(2 | 3) → (4 | 7); '
     'k aus P(2 | 1) und P\'(5 | 2.5): 2.5, k < 1 verkleinert; Fläche aus Koordinaten: Rechteck minus Randdreiecke, 5.5; Fehler: Zentrum vergessen.',
     ['zentrische Streckung', 'Streckfaktor', 'Fläche', 'Koordinaten'], [
         sz('Ursprung',
            'Strecke das Dreieck vom Ursprung aus mit dem Faktor zwei. Jeder Weg vom Ursprung zu einer Ecke wird doppelt so lang. Ist der Ursprung das Zentrum, heisst das einfach: alle Koordinaten mal zwei.',
            f(r"Z(0 \mid 0),\ k = 2: \;\; (x \mid y) \to (2x \mid 2y)", 300, 46, ein='@Koordinaten'),
            ks([P_(0, 0, 3, 'Z', [-0.4, -0.8], 'end')], [V(DR, 1, 0.2)]),
            ksdazu(figuren=[V(DR2, 2, 0.12), S((0, 0), (6, 2), 5, 2, gest=True), S((0, 0), (2, 4), 5, 2, gest=True)], ein='@doppelt')),
         sz('Vorhersage',
            'Das kleine Dreieck hat die Fläche eins, das Bild die Fläche vier. Breite und Höhe sind beide doppelt so gross, die Fläche also viermal so gross. Das ist k Quadrat.',
            f(r"1 \cdot 2^2 = \fb{4}", 300, 60, ein='@also'),
            ks([P_(0, 0, 3, 'Z', [-0.4, -0.8], 'end')], [V(DR, 1, 0.3)]),
            ksdazu(figuren=[V(DR2, 2, 0.12)], ein='@Bild')),
         sz('Zentrum',
            'Liegt das Zentrum nicht im Ursprung, streckst du den Weg ab Z. Z mit eins und eins, k gleich drei, P mit zwei und drei: Der Weg ist eins und zwei, mal drei gibt drei und sechs. Ab Z abgetragen: vier und sieben.',
            f(r"P' = Z + k \cdot (P - Z)", 280, 52, ein='@Weg'),
            f(r"(1 + 3 \mid 1 + 6) = \fb{(4 \mid 7)}", 400, 52, ein='@abgetragen'),
            ks([P_(1, 1, 3, 'Z', [1.3, 0.4]), P_(2, 3, 1, 'P', [1.7, 3.3], 'end')], [S((1, 1), (2, 3), 1, 4)], W=W9),
            ksdazu([P_(4, 7, 2, "P'", [4.3, 6.4])], [S((2, 3), (4, 7), 2, 4, gest=True)], '@abgetragen', W=W9)),
         sz('Faktor',
            'Kennst du P und das Bild P Strich, findest du k: Teile den Weg ab Z zum Bild durch den Weg ab Z zum Punkt. Vom Ursprung aus fällt P mit zwei und eins auf P Strich mit fünf und zwei Komma fünf. Fünf durch zwei gibt zwei Komma fünf, also ist k gleich zwei Komma fünf. Ist k kleiner als eins, wird die Figur kleiner.',
            f(r"k = \dfrac{5}{2} = \dfrac{2.5}{1} = \fc{2.5}", 280, 50, ein='@Teile'),
            n('0 < k < 1: Das Bild wird kleiner.', 420, 'blau', 42, ein='@kleiner'),
            ks([P_(0, 0, 3, 'Z', [-0.4, -0.8], 'end'), P_(2, 1, 1, 'P', [2.0, 1.6], 'end')], [S((0, 0), (2, 1), 1, 4)]),
            ksdazu([P_(5, 2.5, 2, "P'", [5.3, 3.0])], [S((2, 1), (5, 2.5), 2, 4, gest=True)], '@fällt')),
         sz('Flaeche',
            'Die Fläche eines Dreiecks aus Koordinaten: Zeichne das kleinste Rechteck darum, hier vier mal drei. Zieh die drei rechtwinkligen Randdreiecke ab: zwei, eins Komma fünf und drei. Es bleiben fünf Komma fünf.',
            f(r"4 \cdot 3 - 2 - 1.5 - 3 = \fc{5.5}", 300, 50, ein='@bleiben'),
            ks([], [V([(1, 1), (5, 2), (2, 4)], 1, 0.25)]),
            ksdazu(figuren=[V([(1, 1), (5, 1), (5, 4), (1, 4)], 5, 0.0, gestrichelt=True, dicke=3)], ein='@Rechteck'),
            ksdazu(figuren=[T(3, 0.4, '4', 5, g=30), T(5.4, 2.5, '3', 5, 'start', g=30)], ein='@hier'),
            ksdazu(figuren=[V([(1, 1), (5, 1), (5, 2)], 5, 0.2, dicke=2), V([(5, 2), (5, 4), (2, 4)], 5, 0.2, dicke=2), V([(2, 4), (1, 4), (1, 1)], 5, 0.2, dicke=2),
                            T(3.9, 1.25, '2', 5, g=28), T(4.1, 3.35, '3', 5, g=28), T(1.3, 3.0, '1.5', 5, g=26)], ein='@rechtwinkligen')),
         sz('Fehler',
            'Häufiger Fehler: das Zentrum vergessen und einfach mal drei rechnen. Zwei mal drei und drei mal drei gibt sechs und neun. Das stimmt nur, wenn das Zentrum im Ursprung liegt.',
            f(r"\fd{(6 \mid 9)}", 300, 56, ein='@vergessen'),
            n('Weg ab Z strecken, nicht die Koordinaten', 430, 'rot', 42, ein='@Ursprung'),
            ks([P_(1, 1, 3, 'Z', [1.3, 0.4]), P_(2, 3, 1, 'P', [1.7, 3.3], 'end'), P_(4, 7, 2, "P'", [3.7, 7.4], 'end')], [S((1, 1), (4, 7), 2, 3, gest=True)], W=W9),
            ksdazu([P_(6, 9, 4, '(6 | 9)', [6.3, 8.4])], [S((0, 0), (6, 9), 4, 3, gest=True)], '@Zwei', W=W9)),
         merke('Zum Mitnehmen: Bei einer Streckung wird der Weg vom Zentrum zu jedem Punkt mit k multipliziert. Längen werden mal k, Flächen mal k Quadrat. Flächen aus Koordinaten: Rechteck darum, Randdreiecke abziehen.',
               "P' = Z + k · (P − Z)|Längen · k, Flächen · k²|Rechteck minus Randdreiecke"),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Das kleine Dreieck hat die Fläche 1. Wie gross ist die Fläche des Bildes bei k = 2?', ['4', '2', '8'], 0,
              {0: 'Ja.', 1: 'Breite und Höhe werden beide verdoppelt.', 2: 'Die Fläche hat zwei Richtungen, nicht drei.'},
              sprich='Das kleine Dreieck hat die Fläche eins. Wie gross ist die Fläche des Bildes bei k gleich zwei?',
              rueck_sprich={1: 'Breite und Höhe werden beide verdoppelt.', 2: 'Die Fläche hat zwei Richtungen, nicht drei.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
FRAGEBILD.update({('kontrolle-streckung', 'Frage 4'): (WK, [], [], {'figuren': [V([(1, 1), (5, 1), (3, 4)], 1, 0.2)]})})
clip('kontrolle-streckung', 6, 'Geometrie: Kontrollfragen zur Streckung',
     'Fünf Fragen: P(2 | −1) mit k = 3 am Ursprung, P(3 | 3) mit Z(1 | 2) und k = 2, Fläche 7 mit k = 2, Dreiecksfläche aus Koordinaten, k aus P und P\'.',
     ['zentrische Streckung', 'Fläche', 'Kontrollfragen'], [
         sz('Frage 1', 'Zentrum im Ursprung: beide Koordinaten mal drei, sechs und minus drei.',
            f(r"P' = \fc{(6 \mid -3)}", 330, 60, ein=1.0)),
         sz('Frage 2', 'Weg von Z nach P: zwei und eins. Mal zwei gibt vier und zwei, ab Z: fünf und vier.',
            f(r"P' = (1 + 4 \mid 2 + 2) = \fc{(5 \mid 4)}", 330, 50, ein=1.0)),
         sz('Frage 3', 'Sieben mal zwei Quadrat gibt achtundzwanzig.',
            f(r"7 \cdot 2^2 = \fc{28}", 330, 60, ein=1.0)),
         sz('Frage 4', 'Grundseite vier, Höhe drei: Die Fläche ist sechs.',
            f(r"\dfrac{4 \cdot 3}{2} = \fc{6}", 330, 56, ein=1.0),
            ks([], [V([(1, 1), (5, 1), (3, 4)], 1, 0.2), S((3, 1), (3, 4), 5, 3, gest=True)])),
         sz('Frage 5', 'Drei durch eins und sechs durch zwei geben je drei. Der Faktor ist drei.',
            f(r"k = \dfrac{3}{1} = \dfrac{6}{2} = \fc{3}", 330, 54, ein=1.0)),
         merke('Zum Mitnehmen: Weg ab Z mal k. Längen mal k, Flächen mal k Quadrat.',
               "P' = Z + k · (P − Z)|Flächen · k²"),
     ], [
         wahl('Frage 1', 'P(2 | −1) wird vom Ursprung aus mit k = 3 gestreckt. Wo liegt P\'?', ['(6 | −3)', '(5 | 2)', '(6 | 3)'], 0,
              {0: 'Ja.', 1: 'Strecken heisst mal k, nicht plus k.', 2: 'Auch das Minus wird mal 3 gerechnet.'},
              sprich='P mit zwei und minus eins wird vom Ursprung aus mit k gleich drei gestreckt. Wo liegt P Strich?',
              rueck_sprich={1: 'Strecken heisst mal k, nicht plus k.', 2: 'Auch das Minus wird mal drei gerechnet.'}),
         wahl('Frage 2', 'Strecke P(3 | 3) von Z(1 | 2) aus mit k = 2.', ['(5 | 4)', '(6 | 6)', '(4 | 2)'], 0,
              {0: 'Ja.', 1: 'Das wäre mit Zentrum im Ursprung.', 2: 'Das ist nur der gestreckte Weg. Trag ihn ab Z ab.'},
              sprich='Strecke P mit drei und drei von Z mit eins und zwei aus mit k gleich zwei.',
              rueck_sprich={1: 'Das wäre mit Zentrum im Ursprung.', 2: 'Das ist nur der gestreckte Weg. Trag ihn ab Z ab.'}),
         wahl('Frage 3', 'Eine Figur mit Fläche 7 wird mit k = 2 gestreckt. Wie gross ist das Bild?', ['28', '14', '49'], 0,
              {0: 'Ja.', 1: 'Längen mal k, Flächen mal k².', 2: 'Quadriert wird k, nicht die Fläche.'},
              sprich='Eine Figur mit Fläche sieben wird mit k gleich zwei gestreckt. Wie gross ist das Bild?',
              rueck_sprich={1: 'Längen mal k, Flächen mal k Quadrat.', 2: 'Quadriert wird k, nicht die Fläche.'}),
         wahl('Frage 4', 'Dreieck im Bild mit den Ecken (1 | 1), (5 | 1), (3 | 4): Wie gross ist die Fläche?', ['6', '12', '7'], 0,
              {0: 'Ja.', 1: 'Das ist das ganze Rechteck um das Dreieck. Welcher Teil davon gehört zum Dreieck?', 2: 'Eine Fläche entsteht durch Multiplizieren, nicht durch Addieren.'},
              sprich='Das Dreieck im Bild hat die Ecken eins und eins, fünf und eins, drei und vier. Wie gross ist die Fläche?',
              rueck_sprich={1: 'Das ist das ganze Rechteck um das Dreieck. Welcher Teil davon gehört zum Dreieck?', 2: 'Eine Fläche entsteht durch Multiplizieren, nicht durch Addieren.'}),
         wahl('Frage 5', 'Vom Ursprung aus fällt P(1 | 2) auf P\'(3 | 6). Welcher Faktor k?', ['3', '2', '4'], 0,
              {0: 'Ja.', 1: 'Das ist der Unterschied in x. k ist ein Faktor.', 2: 'Das ist der Unterschied in y. k ist ein Faktor.'},
              sprich='Vom Ursprung aus fällt P mit eins und zwei auf P Strich mit drei und sechs. Welcher Faktor k?',
              rueck_sprich={1: 'Das ist der Unterschied in x. k ist ein Faktor.', 2: 'Das ist der Unterschied in y. k ist ein Faktor.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung: Gerade durch zwei Punkte
clip('gerade', 7, 'Geometrie: Gerade durch zwei Punkte',
     'A(1 | 3), B(4 | 9): Steigungsdreieck Δx = 3, Δy = 6, m = 2; A einsetzen: b = 1, y = 2x + 1; Vorhersage: Q(100 | 201) liegt darauf; '
     'D(50 | 102) knapp daneben; Fehler: Δx : Δy.',
     ['Gerade', 'Steigung', 'Punktprobe', 'Geradengleichung'], [
         sz('Steigung',
            'Eine Gerade geht durch A mit eins und drei und B mit vier und neun. Von A nach B geht es drei nach rechts und sechs nach oben. Die Steigung ist sechs durch drei, also zwei.',
            f(r"m = \dfrac{\Delta y}{\Delta x} = \dfrac{6}{3} = \fc{2}", 300, 50, ein='@Steigung'),
            graf(dict(xbereich=[-2, 10], ybereich=[-1, 11], xteilung=teil(2, 4, 6, 8), yteilung=teil(2, 4, 6, 8, 10)),
                 punkte=[pt(1, 3, 1, 'A', [0.7, 3.5], 'end'), pt(4, 9, 1, 'B', [4.3, 9.5])]),
            dict(ueber(dict(xbereich=[-2, 10], ybereich=[-1, 11]), ein='@rechts'), figuren=[S((1, 3), (4, 3), 5, 3, gest=True), S((4, 3), (4, 9), 5, 3, gest=True), T(2.5, 2.2, '3', 5, g=32), T(4.4, 6, '6', 5, 'start', g=32)])),
         sz('Achsenabschnitt',
            'Für den Achsenabschnitt b setzt du einen Punkt ein, zum Beispiel A: drei gleich zwei mal eins plus b. Der Achsenabschnitt ist eins. Die Gleichung heisst y gleich zwei x plus eins.',
            f(r"3 = 2 \cdot 1 + b \;\Rightarrow\; b = 1", 280, 50, ein='@setzt'),
            f(r"\fc{y = 2x + 1}", 400, 60, ein='@Gleichung'),
            graf(dict(xbereich=[-2, 10], ybereich=[-1, 11], xteilung=teil(2, 4, 6, 8), yteilung=teil(2, 4, 6, 8, 10)),
                 geraden=[ger(2, 1, 3)], punkte=[pt(1, 3, 1, 'A', [0.6, 3.6], 'end'), pt(4, 9, 1, 'B', [4.5, 9.1])])),
         sz('Vorhersage',
            'Liegt Q mit hundert und zweihunderteins auf der Geraden? Einsetzen: zwei mal hundert plus eins gibt zweihunderteins. Die Gleichung stimmt, Q liegt darauf, auch wenn er weit ausserhalb jeder Zeichnung ist.',
            f(r"2 \cdot 100 + 1 = 201 \;\Rightarrow\; \fc{\text{ja}}", 300, 50, ein='@Einsetzen')),
         sz('Knapp',
            'Und D mit fünfzig und hundertzwei? Zwei mal fünfzig plus eins gibt hunderteins, nicht hundertzwei. D liegt knapp daneben. Ablesen hätte das nie gezeigt, nur das Einsetzen.',
            f(r"2 \cdot 50 + 1 = 101 \neq 102", 300, 52, ein='@gibt'),
            n('nur Einsetzen entscheidet', 430, 'blau', 46, ein='@Einsetzen')),
         sz('Fehler',
            'Häufiger Fehler: den Bruch auf den Kopf stellen. Drei durch sechs gibt ein Halb, nicht zwei. Die Steigung ist immer y-Unterschied durch x-Unterschied.',
            f(r"\fd{\dfrac{\Delta x}{\Delta y} = \dfrac{3}{6}}", 300, 50, ein='@Kopf'),
            n('m = Δy : Δx', 440, 'rot', 46, ein='@immer')),
         merke('Zum Mitnehmen: Steigung gleich y-Unterschied durch x-Unterschied. Dann einen Punkt einsetzen und den Achsenabschnitt b bestimmen. Ob ein Punkt auf der Geraden liegt, entscheidet das Einsetzen.',
               'm = Δy : Δx|einen Punkt einsetzen: b|Punktprobe durch Einsetzen'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Liegt Q(100 | 201) auf der Geraden y = 2x + 1?', ['ja', 'nein', 'nur mit einer Zeichnung zu entscheiden'], 0,
              {0: 'Ja.', 1: 'Setz x = 100 ein und vergleiche.', 2: 'Einsetzen entscheidet auch ohne Zeichnung.'},
              sprich='Liegt Q mit hundert und zweihunderteins auf der Geraden y gleich zwei x plus eins?',
              rueck_sprich={1: 'Setz x gleich hundert ein und vergleiche.', 2: 'Einsetzen entscheidet auch ohne Zeichnung.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
clip('kontrolle-gerade', 8, 'Geometrie: Kontrollfragen zu Geraden',
     'Fünf Fragen: m aus (0 | 1) und (2 | 7), b bei m = 2 durch (3 | 4), Punktprobe (10 | 25) auf y = 3x − 5, (20 | 50) auf y = 2x + 5, Fehler Δx : Δy.',
     ['Gerade', 'Punktprobe', 'Kontrollfragen'], [
         sz('Frage 1', 'Sieben minus eins durch zwei minus null gibt sechs durch zwei, also drei.',
            f(r"m = \dfrac{6}{2} = \fc{3}", 330, 56, ein=1.0)),
         sz('Frage 2', 'Vier gleich zwei mal drei plus b, also ist b minus zwei.',
            f(r"4 = 6 + b \;\Rightarrow\; b = \fc{-2}", 330, 54, ein=1.0)),
         sz('Frage 3', 'Drei mal zehn minus fünf gibt fünfundzwanzig. Der Punkt liegt darauf.',
            f(r"3 \cdot 10 - 5 = 25 \;\Rightarrow\; \fc{\text{ja}}", 330, 50, ein=1.0)),
         sz('Frage 4', 'Zwei mal zwanzig plus fünf gibt fünfundvierzig, nicht fünfzig. Der Punkt liegt nicht darauf.',
            f(r"2 \cdot 20 + 5 = 45 \neq 50", 330, 54, ein=1.0)),
         sz('Frage 5', 'Ben hat den Bruch auf den Kopf gestellt. Richtig ist vier durch eins, also vier.',
            f(r"m = \dfrac{5 - 1}{2 - 1} = \fc{4}", 330, 52, ein=1.0)),
         merke('Zum Mitnehmen: Steigung gleich y-Unterschied durch x-Unterschied, dann b durch Einsetzen. Die Punktprobe macht das Einsetzen.',
               'm = Δy : Δx, dann b|Punktprobe: einsetzen'),
     ], [
         wahl('Frage 1', 'Welche Steigung hat die Gerade durch (0 | 1) und (2 | 7)?', ['3', '1/3', '6'], 0,
              {0: 'Ja.', 1: 'Der Bruch steht auf dem Kopf: Δy durch Δx.', 2: 'Das ist nur Δy. Teile noch durch Δx.'},
              sprich='Welche Steigung hat die Gerade durch den Punkt null und eins und den Punkt zwei und sieben?',
              rueck_sprich={1: 'Der Bruch steht auf dem Kopf: delta y durch delta x.', 2: 'Das ist nur delta y. Teile noch durch delta x.'}),
         wahl('Frage 2', 'Eine Gerade mit m = 2 geht durch (3 | 4). Wie gross ist b?', ['−2', '2', '10'], 0,
              {0: 'Ja.', 1: 'Setz ein: 4 = 2 · 3 + b.', 2: 'b ist das, was zu 2 · 3 noch dazukommt, um 4 zu erhalten.'},
              sprich='Eine Gerade mit m gleich zwei geht durch drei und vier. Wie gross ist b?',
              rueck_sprich={1: 'Setz ein: vier gleich zwei mal drei plus b.', 2: 'b ist das, was zu zwei mal drei noch dazukommt, um vier zu erhalten.'}),
         wahl('Frage 3', 'Liegt (10 | 25) auf y = 3x − 5?', ['ja', 'nein', 'kann man ohne Zeichnung nicht sagen'], 0,
              {0: 'Ja.', 1: 'Setz x = 10 ein und vergleiche mit 25.', 2: 'Einsetzen genügt.'},
              sprich='Liegt der Punkt zehn und fünfundzwanzig auf y gleich drei x minus fünf?',
              rueck_sprich={1: 'Setz x gleich zehn ein und vergleiche mit fünfundzwanzig.', 2: 'Einsetzen genügt.'}),
         wahl('Frage 4', 'Punktprobe: Liegt (20 | 50) auf y = 2x + 5?', ['nein', 'ja', 'kann man ohne Zeichnung nicht sagen'], 0,
              {0: 'Ja.', 1: 'Rechne 2 · 20 + 5 nach.', 2: 'Einsetzen genügt.'},
              sprich='Punktprobe: Liegt der Punkt zwanzig und fünfzig auf y gleich zwei x plus fünf?',
              rueck_sprich={1: 'Rechne zwei mal zwanzig plus fünf nach.', 2: 'Einsetzen genügt.'}),
         wahl('Frage 5', 'Ben rechnet für A(1 | 1) und B(2 | 5): m = 1/4. Stimmt das?', ['nein, m = 4', 'ja', 'nein, m = 5'], 0,
              {0: 'Ja.', 1: 'Welcher Unterschied steht oben im Bruch?', 2: 'Das ist nur der y-Wert von B. Rechne die Unterschiede.'},
              sprich='Ben rechnet für A mit eins und eins und B mit zwei und fünf: m gleich ein Viertel. Stimmt das?',
              rueck_sprich={1: 'Welcher Unterschied steht oben im Bruch?', 2: 'Das ist nur der y-Wert von B. Rechne die Unterschiede.'}),
     ], art='Kontrollclip')

if FEHLT:
    print('ohne gemessene Wortzeit (geschätzt):', len(FEHLT), FEHLT)
