"""Erzeugt die acht Drehbücher des Leitprogramms «Flächen, Pythagoras und Ähnlichkeit» (10.10.2026).

  python3 scripts/lp/pythagoras/clips.py

Gerüst und Zeitlogik aus scripts/lp/bewegung/clips.py: Je Kapitel ein Einführungsclip (mit einer Vorhersagefrage)
und ein Kontrollclip (fünf Fragen mit neuen Zahlen). Gemessene `dauer` werden beim Neulauf gerettet; Einblendungen
stehen als «@wort» auf dem Wort, das sie nennen (wortzeiten.json, faster-whisper medium). Zahlwörter hört Whisper als
Ziffern: Anker darum auf Wörtern ohne Zahl.

Bild rechts (x 1010, y 175, 760 × 760), Rechnung links (x 150). Figuren ohne Achsen, im Karo; jedes Fenster ist in x und
y gleich weit, sonst würde ein Kreis zur Ellipse. Das Hilfsdreieck wird Schritt für Schritt eingeblendet
(Vorlage §6: «Hilfsdreieck zuerst finden»).

Fragebild (HOWTO-leitprogramme §15): In den Kontrollclips zeigt das Bild beim Erscheinen einer Frage nur das Gegebene
(FRAGEBILD unten); die Auflösung erscheint ab 1.0 s, nach der Antwort.

Farben — gleich wie auf der Seite:
  1 blau   = Figur, Grundseite, Kathete a           \\fa{…}
  2 orange = Höhe, Abstand, Kathete b, Bildfigur     \\fb{…}
  3 grün   = Hypotenuse, Radius, Ergebnis            \\fc{…}
  4 rot    = Fehler                                  \\fd{…}
  5 Tinte  = neutral, Kreis, rechter Winkel
Gesprochen: Zahlwörter ausgeschrieben, «Quadrat» für die Hochzahl 2, «Wurzel aus».
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
PRAEFIX = 'pyt-lp-'
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
         'schlagworte': schlag, 'themenbereich': 'Geometrie · Flächen, Pythagoras und Ähnlichkeit',
         'fach': 'Sekundarstufe I', 'lerngebiet': '5 · Geometrie',
         'lektion': ['lp-pythagoras'], 'stufe': ['Sek I'], 'datum': '2026-10-10',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Geometrie', 'folge': folge,
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms pythagoras; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
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


# ---------------------------------------------------------------- Fenster
W1 = fenster(-1.5, 12.5, -2, 12)
W2 = fenster(-5.5, 8.5, -4.5, 9.5)
W2B = fenster(-1.5, 11.5, -1.5, 11.5)
W3R = fenster(-2, 25, -3, 24)
W3G = fenster(-2, 18, -2, 18)
W3K = fenster(-12.5, 12.5, -12.5, 12.5)
W3W = fenster(-30, 30, -30, 30)
W4 = fenster(-1, 11, -1.5, 10.5)
W4S = fenster(-1.5, 17.5, -3, 16)
W4R = fenster(-6, 66, -16, 56)

DR1 = [(0, 0), (6, 0), (3, 4)]                         # Dreieck g = 6, h = 4, schräge Seiten 5
HAUS = [(0, 0), (6, 0), (6, 4), (0, 4)]


def hlinie(x, h, farbe=2):
    return [S((x, 0), (x, h), farbe, 4, gest=True), RW((x, 0), 0, 90)]


# ════════════════════════════════════════════════ Kapitel 1 · Einführung: Grundseite und Höhe
clip('flaechen', 1, 'Geometrie: Grundseite und Höhe',
     'Dreieck g = 6, h = 4, schräge Seiten 5: Vorhersage Fläche 12 (Hälfte des Rechtecks 6 × 4); Spitze parallel verschieben, Fläche bleibt, '
     'Höhe auf der verlängerten Grundseite; Parallelogramm 6 · 4 = 24 (Dreieck abschneiden, Rechteck); Trapez 7 und 3, h = 4: 14 + 6 = 20; '
     'Haus aus Rechteck und Dreieck 24 + 9 = 33; Fehler: schräge Seite statt Höhe.',
     ['Fläche', 'Dreieck', 'Parallelogramm', 'Höhe', 'Grundseite', 'zusammengesetzte Figur'], [
         sz('Dreieck',
            'Ein Dreieck mit der Grundseite sechs Zentimeter. Die Höhe steht senkrecht auf der Grundseite: vier Zentimeter. Die schrägen Seiten sind je fünf Zentimeter lang.',
            n('Grundseite g = 6 cm|Höhe h = 4 cm (senkrecht)|schräge Seiten 5 cm', 300, 'blau', 44, ein='@Grundseite'),
            geo(W1, [V(DR1, 1, 0.15), T(3, -1, 'g = 6', 1, g=32), T(-0.2, 2.3, '5', 5, 'end', g=30), T(6.2, 2.3, '5', 5, 'start', g=30)]),
            dazu(W1, hlinie(3, 4) + [T(3.3, 1.6, 'h = 4', 2, 'start', g=30)], '@Höhe')),
         sz('Vorhersage',
            'Ergänze das Dreieck zum Rechteck sechs mal vier. Das Dreieck ist genau die Hälfte davon: sechs mal vier durch zwei, zwölf Quadratzentimeter.',
            f(r'A = \dfrac{6 \cdot 4}{2} = \fc{12}\ \text{cm}^2', 300, 56, ein='@Hälfte'),
            geo(W1, [V(DR1, 1, 0.15)] + hlinie(3, 4)),
            dazu(W1, [V(HAUS, 5, 0.0, gestrichelt=True, dicke=3), V([(0, 0), (3, 4), (0, 4)], 2, 0.12, dicke=2), V([(6, 0), (6, 4), (3, 4)], 2, 0.12, dicke=2)], '@Rechteck')),
         sz('Scheren',
            'Schiebst du die Spitze parallel zur Grundseite, ändern sich die schrägen Seiten. Grundseite und Höhe bleiben, also bleibt auch die Fläche: zwölf Quadratzentimeter. Die Höhe kann dabei neben dem Dreieck liegen, auf der verlängerten Grundseite.',
            f(r'A = \dfrac{g \cdot h}{2}', 300, 60, ein='@bleiben'),
            geo(W1, [S((-1, 4), (12, 4), 5, 2, gest=True), S((6, 0), (11, 0), 5, 2, gest=True),
                     mit(V(DR1, 1, 0.15), bewegung=[[1.0, {'punkte': [[0, 0], [6, 0], [3, 4]]}], [4.5, {'punkte': [[0, 0], [6, 0], [10, 4]]}], [6.5, {'punkte': [[0, 0], [6, 0], [10, 4]]}]]),
                     mit(S((3, 0), (3, 4), 2, 4, gest=True), bewegung=[[1.0, {'von': [3, 0], 'bis': [3, 4]}], [4.5, {'von': [10, 0], 'bis': [10, 4]}]]),
                     mit(RW((3, 0), 0, 90), aus=1.0), mit(RW((10, 0), 90, 180), ein=4.5)])),
         sz('Parallelogramm',
            'Beim Parallelogramm schneidest du links ein Dreieck ab und setzt es rechts an. Es entsteht ein Rechteck: Grundseite mal Höhe, sechs mal vier gleich vierundzwanzig.',
            f(r'A = g \cdot h = 6 \cdot 4 = \fc{24}\ \text{cm}^2', 300, 54, ein='@Rechteck'),
            geo(W1, [V([(0, 0), (6, 0), (8, 4), (2, 4)], 5, 0.0, gestrichelt=True, dicke=2), V([(2, 0), (6, 0), (8, 4), (2, 4)], 1, 0.15)] + hlinie(2, 4)
                     + [mit(V([(0, 0), (2, 0), (2, 4)], 2, 0.3, dicke=2), bewegung=[[2.5, {'punkte': [[0, 0], [2, 0], [2, 4]]}], [5.0, {'punkte': [[6, 0], [8, 0], [8, 4]]}]])])),
         sz('Trapez',
            'Beim Trapez sind zwei Seiten parallel, sieben und drei Zentimeter lang, die Höhe ist vier. Eine Diagonale zerlegt es in zwei Dreiecke: sieben mal vier durch zwei plus drei mal vier durch zwei, vierzehn plus sechs gleich zwanzig. Kurz: der Mittelwert der parallelen Seiten mal die Höhe.',
            f(r'\dfrac{7 \cdot 4}{2} + \dfrac{3 \cdot 4}{2} = 14 + 6 = 20', 280, 46, ein='@zerlegt+1.5'),
            f(r'A = \dfrac{a + c}{2} \cdot h = 5 \cdot 4 = \fc{20}\ \text{cm}^2', 400, 48, ein='@Kurz'),
            geo(W1, [V([(0, 0), (7, 0), (5, 4), (2, 4)], 1, 0.12), S((2, 0), (2, 4), 2, 4, gest=True), RW((2, 0), 0, 90),
                     T(3.5, -1, 'a = 7', 1, g=30), T(3.5, 4.5, 'c = 3', 1, g=30), T(2.2, 3.4, 'h = 4', 2, 'start', g=28)]),
            dazu(W1, [S((0, 0), (5, 4), 5, 4), V([(0, 0), (7, 0), (5, 4)], 1, 0.25, dicke=0), V([(0, 0), (5, 4), (2, 4)], 2, 0.25, dicke=0)], '@Diagonale')),
         sz('Haus',
            'Zusammengesetzte Figuren zerlegst du. Das Haus besteht aus einem Rechteck sechs mal vier und einem Dreieck mit Grundseite sechs und Höhe drei: vierundzwanzig plus neun gleich dreiunddreissig.',
            f(r'6 \cdot 4 + \dfrac{6 \cdot 3}{2} = 24 + 9 = \fc{33}\ \text{cm}^2', 300, 46, ein='@plus-0.6'),
            geo(W1, [V(HAUS, 1, 0.15), V([(0, 4), (6, 4), (3, 7)], 2, 0.15), S((3, 4), (3, 7), 2, 3, gest=True),
                     T(3, -1, '6', 1, g=32), T(6.3, 2, '4', 1, 'start', g=32), T(3.3, 5.3, '3', 2, 'start', g=32)])),
         sz('Fehler',
            'Häufiger Fehler: die schräge Seite statt der Höhe nehmen. Sechs mal fünf durch zwei gibt fünfzehn, das Dreieck hat aber nur zwölf Quadratzentimeter.',
            f(r'\fd{\dfrac{6 \cdot 5}{2} = 15}', 300, 56, ein='@Fehler'),
            n('Höhe: senkrecht zur Grundseite', 450, 'rot', 44, ein='@Höhe'),
            geo(W1, [V(DR1, 1, 0.15)] + hlinie(3, 4) + [S((0, 0), (3, 4), 4, 7)])),
         merke('Zum Mitnehmen: Dreieck gleich Grundseite mal Höhe durch zwei, Parallelogramm Grundseite mal Höhe, Trapez der Mittelwert der parallelen Seiten mal die Höhe. Die Höhe steht senkrecht auf der Grundseite. Zusammengesetzte Figuren zerlegst oder ergänzt du.',
               'Dreieck: g · h : 2|Parallelogramm: g · h|Trapez: (a + c) : 2 · h|Höhe senkrecht zur Grundseite|zerlegen oder ergänzen'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Wie gross ist die Fläche des Dreiecks (g = 6 cm, h = 4 cm, schräge Seiten 5 cm)?', ['12 cm²', '15 cm²', '24 cm²'], 0,
              {0: 'Ja.', 1: 'Das gibt die schräge Seite. Welche Strecke steht senkrecht auf der Grundseite?', 2: 'Das wäre das ganze Rechteck. Welcher Teil davon ist das Dreieck?'},
              sprich='Wie gross ist die Fläche des Dreiecks mit Grundseite sechs, Höhe vier und schrägen Seiten von fünf Zentimetern?',
              rueck_sprich={1: 'Das gibt die schräge Seite. Welche Strecke steht senkrecht auf der Grundseite?', 2: 'Das wäre das ganze Rechteck. Welcher Teil davon ist das Dreieck?'}),
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
WK1 = fenster(-1.5, 12.5, -2, 12)
FB_K1 = {
    'Frage 1': [V([(0, 0), (10, 0), (7, 7)], 1, 0.15), S((7, 0), (7, 7), 2, 3, gest=True), RW((7, 0), 90, 180), T(5, -1, '10 cm', 1, g=30), T(7.3, 3.2, '7 cm', 2, 'start', g=30)],
    'Frage 2': [V([(0, 0), (9, 0), (12, 4), (3, 4)], 1, 0.15), S((3, 0), (3, 4), 2, 3, gest=True), RW((3, 0), 0, 90), T(4.5, -1, '9 cm', 1, g=30),
                T(3.3, 1.8, '4 cm', 2, 'start', g=30), T(1.1, 2.6, '5 cm', 5, 'end', g=30)],
    'Frage 3': [V([(0, 0), (8, 0), (6, 5), (2, 5)], 1, 0.15), S((2, 0), (2, 5), 2, 3, gest=True), RW((2, 0), 0, 90), T(4, -1, '8 cm', 1, g=30),
                T(4, 5.6, '4 cm', 1, g=30), T(2.3, 2.3, '5 cm', 2, 'start', g=30)],
    'Frage 4': [V([(0, 0), (6, 0), (6, 3), (4, 3), (4, 5), (0, 5)], 1, 0.15), T(3, -1, '6 cm', 1, g=30), T(-0.3, 2.5, '5 cm', 1, 'end', g=30),
                T(5, 5.3, '2 cm', 5, g=28), T(6.3, 4, '2 cm', 5, 'start', g=28), S((4, 5), (6, 5), 5, 2, gest=True), S((6, 3), (6, 5), 5, 2, gest=True)],
}
FRAGEBILD.update({('kontrolle-flaechen', k): (WK1, [], [], {'figuren': v, 'achsen': False, 'raster': True}) for k, v in FB_K1.items()})
clip('kontrolle-flaechen', 2, 'Geometrie: Kontrollfragen zu Flächen',
     'Fünf Fragen: Dreieck 10 und 7, Parallelogramm 9 · 4 mit Seite 5, Trapez 8, 4, Höhe 5, ausgeschnittene Ecke 6 · 5 − 2 · 2, Spitze verschieben.',
     ['Fläche', 'Höhe', 'Kontrollfragen'], [
         sz('Frage 1', 'Zehn mal sieben durch zwei gibt fünfunddreissig Quadratzentimeter.',
            f(r'\dfrac{10 \cdot 7}{2} = \fc{35}\ \text{cm}^2', 330, 56, ein=1.0), geo(WK1, FB_K1['Frage 1'])),
         sz('Frage 2', 'Grundseite neun mal Höhe vier gibt sechsunddreissig. Die schräge Seite brauchst du nicht.',
            f(r'9 \cdot 4 = \fc{36}\ \text{cm}^2', 330, 56, ein=1.0), geo(WK1, FB_K1['Frage 2'])),
         sz('Frage 3', 'Acht plus vier durch zwei gibt sechs, mal die Höhe fünf: dreissig Quadratzentimeter.',
            f(r'\dfrac{8 + 4}{2} \cdot 5 = \fc{30}\ \text{cm}^2', 330, 54, ein=1.0), geo(WK1, FB_K1['Frage 3'])),
         sz('Frage 4', 'Ergänze zum Rechteck sechs mal fünf, also dreissig, und zieh die Ecke zwei mal zwei ab: sechsundzwanzig.',
            f(r'6 \cdot 5 - 2 \cdot 2 = \fc{26}\ \text{cm}^2', 330, 54, ein=1.0), geo(WK1, FB_K1['Frage 4'])),
         sz('Frage 5', 'Grundseite und Höhe bleiben gleich, also bleibt auch die Fläche gleich.',
            n('Die Fläche bleibt gleich.', 330, 'gruen', 48, ein=1.0)),
         merke('Zum Mitnehmen: Grundseite und Höhe bestimmen die Fläche. Die schräge Seite zählt nicht. Zusammengesetzte Figuren zerlegen oder ergänzen.',
               'Grundseite und Höhe|schräge Seite zählt nicht|zerlegen oder ergänzen'),
     ], [
         wahl('Frage 1', 'Wie gross ist die Fläche des Dreiecks im Bild?', ['35 cm²', '70 cm²', '17 cm²'], 0,
              {0: 'Ja.', 1: 'Das ist ein Rechteck mit denselben Massen. Ein Dreieck ist halb so gross.', 2: 'Multipliziere zuerst Grundseite und Höhe.'},
              rueck_sprich={1: 'Das ist ein Rechteck mit denselben Massen. Ein Dreieck ist halb so gross.', 2: 'Multipliziere zuerst Grundseite und Höhe.'}),
         wahl('Frage 2', 'Parallelogramm im Bild: Wie gross ist seine Fläche?', ['36 cm²', '45 cm²', '18 cm²'], 0,
              {0: 'Ja.', 1: 'Du hast die schräge Seite genommen. Welche Strecke steht senkrecht?', 2: 'Beim Parallelogramm wird nicht halbiert.'},
              rueck_sprich={1: 'Du hast die schräge Seite genommen. Welche Strecke steht senkrecht?', 2: 'Beim Parallelogramm wird nicht halbiert.'}),
         wahl('Frage 3', 'Trapez im Bild: Wie gross ist seine Fläche?', ['30 cm²', '60 cm²', '160 cm²'], 0,
              {0: 'Ja.', 1: 'Von den parallelen Seiten nimmst du das Mittel, also die Summe durch 2.', 2: 'Die parallelen Seiten werden addiert, nicht multipliziert.'},
              rueck_sprich={1: 'Von den parallelen Seiten nimmst du das Mittel, also die Summe durch zwei.', 2: 'Die parallelen Seiten werden addiert, nicht multipliziert.'}),
         wahl('Frage 4', 'Rechteck mit ausgeschnittener Ecke im Bild: Wie gross ist die Fläche?', ['26 cm²', '34 cm²', '30 cm²'], 0,
              {0: 'Ja.', 1: 'Die Ecke fehlt in der Figur. Abziehen, nicht dazuzählen.', 2: 'Das ist das ganze Rechteck. Was fehlt?'},
              rueck_sprich={1: 'Die Ecke fehlt in der Figur. Abziehen, nicht dazuzählen.', 2: 'Das ist das ganze Rechteck. Was fehlt?'}),
         wahl('Frage 5', 'Die Spitze eines Dreiecks wird parallel zur Grundseite verschoben. Was passiert mit der Fläche?', ['Sie bleibt gleich.', 'Sie wird grösser.', 'Sie wird kleiner.'], 0,
              {0: 'Ja.', 1: 'Die schrägen Seiten werden länger, aber zählen sie für die Fläche?', 2: 'Ändert sich die Höhe beim Verschieben?'},
              rueck_sprich={1: 'Die schrägen Seiten werden länger, aber zählen sie für die Fläche?', 2: 'Ändert sich die Höhe beim Verschieben?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung: Der Satz des Pythagoras
P3 = [(0, 0), (3, 0), (0, 4)]
Q_A = [(0, 0), (3, 0), (3, -3), (0, -3)]
Q_B = [(0, 0), (0, 4), (-4, 4), (-4, 0)]
Q_C = [(3, 0), (0, 4), (4, 7), (7, 3)]
clip('pythagoras', 3, 'Geometrie: Der Satz des Pythagoras',
     'Rechtwinkliges Dreieck 3, 4, 5 im Karo: Katheten, Hypotenuse; Quadrate 9 + 16 = 25 (schräges Quadrat: 7 × 7 minus vier Dreiecke); a² + b² = c² und Umkehrung; Vorhersage 6 und 8 gibt 10; '
     'Kathete c = 10, a = 6 gibt b = 8; Fehler: bei der Kathete addiert.',
     ['Pythagoras', 'Hypotenuse', 'Kathete', 'rechtwinklig'], [
         sz('Dreieck',
            'Ein rechtwinkliges Dreieck. Die Seite gegenüber dem rechten Winkel heisst Hypotenuse, sie ist die längste. Die beiden anderen Seiten heissen Katheten.',
            n('Hypotenuse: gegenüber dem rechten Winkel|Katheten: die beiden anderen', 300, 'blau', 42, ein='@Hypotenuse'),
            geo(W2, [V(P3, 5, 0.06), RW((0, 0), 0, 90), T(1.5, -0.8, 'a', 1, g=36), T(-0.6, 2, 'b', 2, g=36)]),
            dazu(W2, [S((3, 0), (0, 4), 3, 7), T(1.9, 2.5, 'c', 3, 'start', g=36)], '@Hypotenuse')),
         sz('Quadrate',
            'Zeichne über jeder Seite ein Quadrat. Über der Kathete drei liegen neun Kästchen, über der Kathete vier sechzehn. Das Quadrat über der Hypotenuse steht schräg. Ergänze es zum Quadrat sieben mal sieben und zieh die vier Dreiecke in den Ecken ab, je sechs Kästchen: neunundvierzig minus vierundzwanzig gibt fünfundzwanzig. Genau neun plus sechzehn.',
            f(r'49 - 4 \cdot 6 = \fc{25}', 280, 54, ein='@gibt'),
            f(r'\fa{9} + \fb{16} = \fc{25}', 400, 62, ein='@Genau'),
            geo(W2, [V(P3, 5, 0.06), RW((0, 0), 0, 90)]),
            dazu(W2, [V(Q_A, 1, 0.2), T(1.5, -1.9, '9', 1, g=36)], '@Kathete'),
            dazu(W2, [V(Q_B, 2, 0.2), T(-2, 1.7, '16', 2, g=36)], '@Kathete#2'),
            dazu(W2, [V(Q_C, 3, 0.2)], '@schräg'),
            dazu(W2, [V([(0, 0), (7, 0), (7, 7), (0, 7)], 5, 0.0, gestrichelt=True, dicke=3)], '@Ergänze'),
            dazu(W2, [V([(3, 0), (7, 0), (7, 3)], 5, 0.25, dicke=1), V([(7, 3), (7, 7), (4, 7)], 5, 0.25, dicke=1), V([(4, 7), (0, 7), (0, 4)], 5, 0.25, dicke=1), V(P3, 5, 0.25, dicke=1)], '@Dreiecke'),
            dazu(W2, [T(3.5, 3.3, '25', 3, g=36)], '@gibt+0.3')),
         sz('Satz',
            'Das gilt in jedem rechtwinkligen Dreieck: a Quadrat plus b Quadrat gleich c Quadrat. Die Quadrate der Katheten ergeben zusammen das Quadrat der Hypotenuse. Und umgekehrt: Gilt für drei Seiten a Quadrat plus b Quadrat gleich c Quadrat, dann ist das Dreieck rechtwinklig.',
            f(r'\fa{a^2} + \fb{b^2} = \fc{c^2}', 300, 72, ein='@jedem'),
            n('Umgekehrt: Gilt a² + b² = c²,|ist das Dreieck rechtwinklig.', 430, 'blau', 40, ein='@umgekehrt'),
            geo(W2, [V(P3, 5, 0.06), RW((0, 0), 0, 90), V(Q_A, 1, 0.2), V(Q_B, 2, 0.2), V(Q_C, 3, 0.2)])),
         sz('Vorhersage',
            'Sechs Quadrat plus acht Quadrat gibt sechsunddreissig plus vierundsechzig, also hundert. Die Wurzel aus hundert ist zehn: Die Hypotenuse ist zehn Zentimeter lang.',
            f(r'c^2 = 36 + 64 = 100', 280, 56, ein='@plus'),
            f(r'c = \sqrt{100} = \fc{10}\ \text{cm}', 400, 56, ein='@Wurzel'),
            geo(W2B, [V([(0, 0), (6, 0), (0, 8)], 1, 0.12), RW((0, 0), 0, 90), T(3, -0.8, '6', 1, g=34), T(-0.5, 4, '8', 2, 'end', g=34)]),
            dazu(W2B, [S((6, 0), (0, 8), 3, 7), T(3.4, 4.6, '10', 3, 'start', g=34)], '@Hypotenuse')),
         sz('Kathete',
            'Ist eine Kathete gesucht, subtrahierst du. Hypotenuse zehn, Kathete sechs: b Quadrat gleich hundert minus sechsunddreissig, gleich vierundsechzig. b ist acht.',
            f(r'b^2 = c^2 - a^2 = 100 - 36 = 64', 280, 48, ein='@gesucht+0.7'),
            f(r'b = \sqrt{64} = \fc{8}\ \text{cm}', 400, 54, ein='@acht-0.3'),
            geo(W2B, [V([(0, 0), (6, 0), (0, 8)], 1, 0.12), RW((0, 0), 0, 90), S((6, 0), (0, 8), 3, 7), T(3, -0.8, '6', 1, g=34), T(3.4, 4.6, '10', 3, 'start', g=34), T(-0.5, 4, 'b', 2, 'end', g=36)])),
         sz('Fehler',
            'Häufiger Fehler: bei der Kathete addieren. Hundert plus sechsunddreissig gibt mehr als hundert, die Kathete wäre länger als die Hypotenuse. Das ist unmöglich.',
            f(r'\fd{b^2 = 100 + 36}', 300, 56, ein='@addieren'),
            n('Kathete: minus|Hypotenuse: plus', 430, 'rot', 44, ein='@unmöglich')),
         merke('Zum Mitnehmen: Im rechtwinkligen Dreieck gilt a Quadrat plus b Quadrat gleich c Quadrat. Für die Hypotenuse addierst du die Quadrate, für eine Kathete subtrahierst du. Am Schluss die Wurzel ziehen.',
               'a² + b² = c²|Hypotenuse: Quadrate addieren|Kathete: Quadrate subtrahieren|am Schluss die Wurzel'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Die Katheten sind 6 cm und 8 cm lang. Wie lang ist die Hypotenuse?', ['10 cm', '14 cm', '100 cm'], 0,
              {0: 'Ja.', 1: 'Die Seiten werden nicht einfach addiert. Was gilt für die Quadrate?', 2: '100 ist c², nicht c.'},
              sprich='Die Katheten sind sechs und acht Zentimeter lang. Wie lang ist die Hypotenuse?',
              rueck_sprich={1: 'Die Seiten werden nicht einfach addiert. Was gilt für die Quadrate?', 2: 'Hundert ist c Quadrat, nicht c.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
WK2 = fenster(-1.5, 11.5, -1.5, 11.5)
FB_K2 = {'Frage 3': [V([(1, 1), (9, 1), (1, 7)], 1, 0.12), RW((1, 1), 0, 90), T(5, 0.2, 'p', 1, g=38), T(0.4, 4, 'q', 1, 'end', g=38), T(5.4, 4.6, 'r', 1, 'start', g=38)]}
FRAGEBILD.update({('kontrolle-pythagoras', 'Frage 3'): (WK2, [], [], {'figuren': FB_K2['Frage 3'], 'achsen': False, 'raster': True})})
clip('kontrolle-pythagoras', 4, 'Geometrie: Kontrollfragen zu Pythagoras',
     'Fünf Fragen: Katheten 5 und 12, Hypotenuse 7.5 mit Kathete 6, welche Seite ist die Hypotenuse, ist 7, 24, 26 rechtwinklig (nein), Kathete aus 12.5 und 12.',
     ['Pythagoras', 'Hypotenuse', 'Kathete', 'Kontrollfragen'], [
         sz('Frage 1', 'Fünfundzwanzig plus hundertvierundvierzig gibt hundertneunundsechzig. Die Wurzel daraus ist dreizehn.',
            f(r'\sqrt{25 + 144} = \sqrt{169} = \fc{13}', 330, 54, ein=1.0)),
         sz('Frage 2', 'Sechsundfünfzig Komma zwei fünf minus sechsunddreissig gibt zwanzig Komma zwei fünf. Die Wurzel ist vier Komma fünf.',
            f(r'\sqrt{7.5^2 - 6^2} = \sqrt{20.25} = \fc{4.5}', 330, 52, ein=1.0)),
         sz('Frage 3', 'Die Hypotenuse liegt gegenüber dem rechten Winkel: die Seite r.',
            n('r: gegenüber dem rechten Winkel', 330, 'gruen', 44, ein=1.0),
            geo(WK2, FB_K2['Frage 3'] + [S((9, 1), (1, 7), 3, 7)])),
         sz('Frage 4', 'Neunundvierzig plus fünfhundertsechsundsiebzig gibt sechshundertfünfundzwanzig. Sechsundzwanzig Quadrat ist aber sechshundertsechsundsiebzig. Das Dreieck ist nicht rechtwinklig.',
            f(r'49 + 576 = 625 \neq 676 = 26^2', 330, 54, ein=1.0)),
         sz('Frage 5', 'Für eine Kathete subtrahierst du: hundertsechsundfünfzig Komma zwei fünf minus hundertvierundvierzig gibt zwölf Komma zwei fünf. Die Kathete ist drei Komma fünf Zentimeter.',
            f(r'\sqrt{156.25 - 144} = \sqrt{12.25} = \fc{3.5}', 330, 50, ein=1.0)),
         merke('Zum Mitnehmen: Zuerst die Hypotenuse finden, gegenüber dem rechten Winkel. Für sie addierst du die Quadrate, für eine Kathete subtrahierst du.',
               'Hypotenuse gegenüber dem rechten Winkel|plus für c, minus für eine Kathete'),
     ], [
         wahl('Frage 1', 'Die Katheten sind 5 cm und 12 cm lang. Wie lang ist die Hypotenuse?', ['13 cm', '17 cm', '169 cm'], 0,
              {0: 'Ja.', 1: 'Nicht die Seiten addieren, sondern ihre Quadrate.', 2: '169 ist c². Zieh noch die Wurzel.'},
              sprich='Die Katheten sind fünf und zwölf Zentimeter lang. Wie lang ist die Hypotenuse?',
              rueck_sprich={1: 'Nicht die Seiten addieren, sondern ihre Quadrate.', 2: 'Hundertneunundsechzig ist c Quadrat. Zieh noch die Wurzel.'}),
         wahl('Frage 2', 'Die Hypotenuse ist 7.5 cm, eine Kathete 6 cm. Wie lang ist die andere Kathete?', ['4.5 cm', '1.5 cm', '9.6 cm'], 0,
              {0: 'Ja.', 1: 'Nicht die Seiten subtrahieren, sondern ihre Quadrate.', 2: 'Eine Kathete ist kürzer als die Hypotenuse. Subtrahieren statt addieren.'},
              sprich='Die Hypotenuse ist sieben Komma fünf, eine Kathete sechs Zentimeter lang. Wie lang ist die andere Kathete?',
              rueck_sprich={1: 'Nicht die Seiten subtrahieren, sondern ihre Quadrate.', 2: 'Eine Kathete ist kürzer als die Hypotenuse. Subtrahieren statt addieren.'}),
         wahl('Frage 3', 'Welche Seite im Bild ist die Hypotenuse?', ['r', 'p', 'q'], 0,
              {0: 'Ja.', 1: 'p liegt am rechten Winkel an. Welche Seite liegt ihm gegenüber?', 2: 'q liegt am rechten Winkel an. Welche Seite liegt ihm gegenüber?'},
              rueck_sprich={1: 'p liegt am rechten Winkel an. Welche Seite liegt ihm gegenüber?', 2: 'q liegt am rechten Winkel an. Welche Seite liegt ihm gegenüber?'}),
         wahl('Frage 4', 'Ein Dreieck hat die Seiten 7 cm, 24 cm und 26 cm. Ist es rechtwinklig?', ['nein', 'ja', 'kann man nicht sagen'], 0,
              {0: 'Ja.', 1: 'Rechne 7² + 24² und vergleiche mit 26².', 2: 'Mit den drei Seiten kannst du es prüfen.'},
              sprich='Ein Dreieck hat die Seiten sieben, vierundzwanzig und sechsundzwanzig Zentimeter. Ist es rechtwinklig?',
              rueck_sprich={1: 'Rechne sieben Quadrat plus vierundzwanzig Quadrat und vergleiche mit sechsundzwanzig Quadrat.', 2: 'Mit den drei Seiten kannst du es prüfen.'}),
         wahl('Frage 5', 'Hypotenuse 12.5 cm, eine Kathete 12 cm: Wie lang ist die andere Kathete?', ['3.5 cm', '17.3 cm', '0.5 cm'], 0,
              {0: 'Ja.', 1: 'Die Kathete wäre länger als die Hypotenuse. Subtrahieren statt addieren.', 2: 'Nicht die Seiten subtrahieren, sondern ihre Quadrate.'},
              sprich='Hypotenuse zwölf Komma fünf, eine Kathete zwölf Zentimeter: Wie lang ist die andere Kathete?',
              rueck_sprich={1: 'Die Kathete wäre länger als die Hypotenuse. Subtrahieren statt addieren.', 2: 'Nicht die Seiten subtrahieren, sondern ihre Quadrate.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung: Hilfsdreiecke und Kreis
RE = [(0, 0), (21, 0), (21, 20), (0, 20)]
GL = [(0, 0), (16, 0), (8, 15)]
clip('hilfsdreieck', 5, 'Geometrie: Hilfsdreiecke und Kreis',
     'Hilfsdreieck Schritt für Schritt: Rechteck 21 × 20, Diagonale 29 (Vorhersage); gleichschenkliges Dreieck Basis 16, Schenkel 17, Höhe 15; '
     'Wurzel eingrenzen (√841 zwischen 25 und 30, Endziffer); Kreis r = 10, Sehne 16, Abstand 6; Rohr Ø 50, Wasserspiegel 48, Tiefe 18; Fehler: ganze statt halbe Strecke.',
     ['Hilfsdreieck', 'Pythagoras', 'Diagonale', 'Kreis', 'Sehne', 'Radius'], [
         sz('Rechteck',
            'Wie lang ist die Diagonale eines Rechtecks einundzwanzig mal zwanzig? Such zuerst das Hilfsdreieck: Die Diagonale schneidet das Rechteck in zwei rechtwinklige Dreiecke. Die Diagonale ist ihre Hypotenuse.',
            n('① rechten Winkel suchen|② Hilfsdreieck markieren|③ Seiten eintragen|④ Pythagoras', 290, 'blau', 42, ein='@Hilfsdreieck'),
            geo(W3R, [V(RE, 1, 0.06), T(10.5, -1.6, '21', 1, g=34), T(-0.8, 10, '20', 1, 'end', g=34)]),
            dazu(W3R, [S((0, 0), (21, 20), 3, 6)], '@Diagonale'),
            dazu(W3R, [V([(0, 0), (21, 0), (21, 20)], 2, 0.25, dicke=2), RW((21, 0), 90, 180)], '@rechtwinklige'),
            dazu(W3R, [T(9.4, 11.4, 'e', 3, 'end', g=38)], '@Hypotenuse')),
         sz('Vorhersage',
            'Einundzwanzig Quadrat plus zwanzig Quadrat gibt vierhunderteinundvierzig plus vierhundert, also achthunderteinundvierzig. Die Wurzel grenzt du ein: Fünfundzwanzig Quadrat ist sechshundertfünfundzwanzig, dreissig Quadrat neunhundert. Sie endet auf eins oder neun, also einundzwanzig oder neunundzwanzig. Neunundzwanzig Quadrat ist achthunderteinundvierzig.',
            f(r'e^2 = 441 + 400 = 841', 250, 50, ein='@plus'),
            n('25² = 625 und 30² = 900|Endziffer 1: nur 21 oder 29', 350, 'blau', 38, ein='@grenzt'),
            f(r'e = \sqrt{841} = \fc{29}', 480, 54, ein='@ist#3-0.6'),
            geo(W3R, [V(RE, 1, 0.06), V([(0, 0), (21, 0), (21, 20)], 2, 0.25, dicke=2), RW((21, 0), 90, 180), S((0, 0), (21, 20), 3, 6),
                      T(10.5, -1.6, '21', 1, g=34), T(22, 10, '20', 1, 'start', g=34)])),
         sz('Gleichschenklig',
            'Ein gleichschenkliges Dreieck mit Basis sechzehn und Schenkeln von siebzehn. Die Höhe halbiert die Basis. Das Hilfsdreieck hat die Katheten acht und h und die Hypotenuse siebzehn: h ist fünfzehn.',
            f(r'h = \sqrt{17^2 - 8^2} = \sqrt{225} = \fc{15}', 300, 46, ein='@Hypotenuse'),
            geo(W3G, [V(GL, 1, 0.08), T(8, -1.3, '16', 1, g=34), T(3.2, 8.4, '17', 1, 'end', g=34)]),
            dazu(W3G, [S((8, 0), (8, 15), 2, 4, gest=True), RW((8, 0), 0, 90)], '@halbiert'),
            dazu(W3G, [V([(8, 0), (16, 0), (8, 15)], 2, 0.25, dicke=2), T(12, -1.3, '8', 2, g=34), T(8.5, 6, 'h', 2, 'start', g=36), T(12.8, 8.4, '17', 2, 'start', g=34)], '@Hilfsdreieck')),
         sz('Kreis',
            'Im Kreis verbindet eine Sehne zwei Punkte des Kreises. Der Abstand zum Mittelpunkt steht senkrecht auf ihr und halbiert sie. Radius zehn, Sehne sechzehn: Das Hilfsdreieck hat die Hypotenuse zehn und die Kathete acht, der Abstand ist sechs.',
            f(r'd = \sqrt{10^2 - 8^2} = \fc{6}', 300, 50, ein='@Kathete'),
            geo(W3K, [KR((0, 0), 10, 5), S((-8, -6), (8, -6), 1, 5), T(0, -8, 's = 16', 1, g=32)], raster=False),
            dazu(W3K, [S((0, 0), (0, -6), 2, 5), RW((0, -6), 0, 90), T(-0.6, -3, 'd', 2, 'end', g=36)], '@Abstand'),
            dazu(W3K, [S((0, 0), (8, -6), 3, 5), V([(0, 0), (0, -6), (8, -6)], 2, 0.25, dicke=1), T(4.6, -2.2, 'r = 10', 3, 'start', g=32)], '@Hilfsdreieck')),
         sz('Rohr',
            'Ein Rohr mit fünfzig Zentimetern Durchmesser, der Wasserspiegel ist achtundvierzig Zentimeter breit. Radius fünfundzwanzig, halbe Breite vierundzwanzig: Der Abstand ist sieben. Das Wasser ist fünfundzwanzig minus sieben, also achtzehn Zentimeter tief.',
            f(r'd = \sqrt{25^2 - 24^2} = 7', 280, 48, ein='@Abstand'),
            f(r'\text{Tiefe } 25 - 7 = \fc{18}\ \text{cm}', 400, 48, ein='@tief'),
            geo(W3W, [V(segment(25, 7), 1, 0.25, dicke=0), KR((0, 0), 25, 5), S((-24, -7), (24, -7), 1, 5)], raster=False),
            dazu(W3W, [T(-12, -11.5, '48', 1, g=32)], '@breit'),
            dazu(W3W, [S((0, 0), (0, -7), 2, 5), S((0, 0), (24, -7), 3, 5), RW((0, -7), 0, 90), T(-1, -3.5, '7', 2, 'end', g=32), T(12, -2, '25', 3, 'start', g=32)], '@Radius'),
            dazu(W3W, [S((0, -7), (0, -25), 2, 3, gest=True), T(1.5, -17, '18', 2, 'start', g=32)], '@tief')),
         sz('Fehler',
            'Häufiger Fehler: die ganze Basis oder die ganze Sehne ins Hilfsdreieck setzen. Im gleichschenkligen Dreieck und beim Kreis gehört die Hälfte hinein, denn Höhe und Abstand halbieren sie.',
            n('ganze statt halbe Strecke', 300, 'rot', 44, ein='@Fehler'),
            n('Höhe und Abstand halbieren', 420, 'blau', 44, ein='@halbieren')),
         merke('Zum Mitnehmen: Such zuerst das rechtwinklige Hilfsdreieck und seine Hypotenuse. Trag die bekannten Längen ein, oft die Hälfte. Dann rechnest du mit Pythagoras.',
               'zuerst das Hilfsdreieck|Hypotenuse bestimmen|oft die Hälfte eintragen'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Wie lang ist die Diagonale des Rechtecks 21 × 20?', ['29', '41', '841'], 0,
              {0: 'Ja.', 1: 'Die Seiten werden nicht addiert. Rechne mit den Quadraten.', 2: '841 ist e². Zieh die Wurzel.'},
              sprich='Wie lang ist die Diagonale des Rechtecks einundzwanzig mal zwanzig?',
              rueck_sprich={1: 'Die Seiten werden nicht addiert. Rechne mit den Quadraten.', 2: 'Achthunderteinundvierzig ist e Quadrat. Zieh die Wurzel.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
WKK = fenster(-12.5, 12.5, -12.5, 12.5)
FB_K3 = {'Frage 4': [KR((0, 0), 10, 5), S((-8, -6), (8, -6), 5, 5), S((0, 0), (0, -6), 5, 5), S((0, 0), (8, -6), 5, 5), RW((0, -6), 0, 90),
                     T(0, -8, 'Sehne', 5, g=30), T(-0.6, -3, 'Abstand', 5, 'end', g=30), T(4.6, -2, 'Radius', 5, 'start', g=30)]}   # neutral: Farbe verrät nichts
FB_K3_LOES = [KR((0, 0), 10, 5), S((-8, -6), (8, -6), 1, 5), S((0, 0), (0, -6), 2, 5), S((0, 0), (8, -6), 3, 5), RW((0, -6), 0, 90),
              T(0, -8, 'Sehne', 1, g=30), T(-0.6, -3, 'Abstand', 2, 'end', g=30), T(4.6, -2, 'Radius', 3, 'start', g=30)]
FRAGEBILD.update({('kontrolle-hilfsdreieck', 'Frage 4'): (WKK, [], [], {'figuren': FB_K3['Frage 4'], 'achsen': False, 'raster': False})})
clip('kontrolle-hilfsdreieck', 6, 'Geometrie: Kontrollfragen zu Hilfsdreiecken',
     'Fünf Fragen: Diagonale Rechteck 7.5 × 4, Höhe Basis 18 Schenkel 15, Sehne bei r = 2.5 und Abstand 1.5, Hypotenuse im Kreis, Wassertiefe bei r = 6.5 und Breite 12.',
     ['Hilfsdreieck', 'Kreis', 'Kontrollfragen'], [
         sz('Frage 1', 'Sechsundfünfzig Komma zwei fünf plus sechzehn gibt zweiundsiebzig Komma zwei fünf. Die Wurzel ist acht Komma fünf.',
            f(r'\sqrt{7.5^2 + 4^2} = \sqrt{72.25} = \fc{8.5}', 330, 50, ein=1.0)),
         sz('Frage 2', 'Halbe Basis neun, Schenkel fünfzehn: zweihundertfünfundzwanzig minus einundachtzig gibt hundertvierundvierzig, die Höhe ist zwölf.',
            f(r'h = \sqrt{15^2 - 9^2} = \fc{12}', 330, 52, ein=1.0)),
         sz('Frage 3', 'Sechs Komma zwei fünf minus zwei Komma zwei fünf gibt vier. Die halbe Sehne ist zwei, die ganze vier Zentimeter.',
            f(r'\tfrac{s}{2} = \sqrt{2.5^2 - 1.5^2} = 2, \;\; s = \fc{4}', 330, 46, ein=1.0)),
         sz('Frage 4', 'Der Radius liegt gegenüber dem rechten Winkel. Er ist die Hypotenuse des Hilfsdreiecks.',
            n('der Radius', 330, 'gruen', 50, ein=1.0), geo(WKK, FB_K3_LOES, raster=False)),
         sz('Frage 5', 'Halbe Breite sechs, Radius sechs Komma fünf: Der Abstand ist zwei Komma fünf. Das Wasser ist sechs Komma fünf minus zwei Komma fünf, also vier Zentimeter tief.',
            f(r'd = \sqrt{42.25 - 36} = 2.5, \;\; 6.5 - 2.5 = \fc{4}', 330, 44, ein=1.0)),
         merke('Zum Mitnehmen: Zuerst das Hilfsdreieck finden. Im Kreis ist der Radius die Hypotenuse, und die Sehne geht nur zur Hälfte hinein.',
               'zuerst das Hilfsdreieck|im Kreis: Radius = Hypotenuse|halbe Sehne'),
     ], [
         wahl('Frage 1', 'Wie lang ist die Diagonale eines Rechtecks 7.5 cm × 4 cm?', ['8.5 cm', '11.5 cm', '6.3 cm'], 0,
              {0: 'Ja.', 1: 'Die Seiten werden nicht addiert. Rechne mit den Quadraten.', 2: 'Die Diagonale ist die Hypotenuse. Addieren statt subtrahieren.'},
              sprich='Wie lang ist die Diagonale eines Rechtecks sieben Komma fünf mal vier Zentimeter?',
              rueck_sprich={1: 'Die Seiten werden nicht addiert. Rechne mit den Quadraten.', 2: 'Die Diagonale ist die Hypotenuse. Addieren statt subtrahieren.'}),
         wahl('Frage 2', 'Ein gleichschenkliges Dreieck hat die Basis 18 cm und Schenkel von 15 cm. Wie hoch ist es?', ['12 cm', '6 cm', '9 cm'], 0,
              {0: 'Ja.', 1: 'Nicht die Seiten subtrahieren. Welches Hilfsdreieck entsteht?', 2: 'Das ist die halbe Basis. Gesucht ist die andere Kathete.'},
              sprich='Ein gleichschenkliges Dreieck hat die Basis achtzehn und Schenkel von fünfzehn Zentimetern. Wie hoch ist es?',
              rueck_sprich={1: 'Nicht die Seiten subtrahieren. Welches Hilfsdreieck entsteht?', 2: 'Das ist die halbe Basis. Gesucht ist die andere Kathete.'}),
         wahl('Frage 3', 'Ein Kreis hat den Radius 2.5 cm. Eine Sehne hat den Abstand 1.5 cm vom Mittelpunkt. Wie lang ist sie?', ['4 cm', '2 cm', '1 cm'], 0,
              {0: 'Ja.', 1: 'Das ist die halbe Sehne.', 2: 'Nicht die Längen subtrahieren, sondern ihre Quadrate.'},
              sprich='Ein Kreis hat den Radius zwei Komma fünf Zentimeter. Eine Sehne hat den Abstand eins Komma fünf vom Mittelpunkt. Wie lang ist sie?',
              rueck_sprich={1: 'Das ist die halbe Sehne.', 2: 'Nicht die Längen subtrahieren, sondern ihre Quadrate.'}),
         wahl('Frage 4', 'Welche Strecke im Bild ist die Hypotenuse des Hilfsdreiecks?', ['der Radius', 'die Sehne', 'der Abstand'], 0,
              {0: 'Ja.', 1: 'Nur die halbe Sehne gehört ins Hilfsdreieck, und sie liegt am rechten Winkel.', 2: 'Der Abstand liegt am rechten Winkel an.'},
              rueck_sprich={1: 'Nur die halbe Sehne gehört ins Hilfsdreieck, und sie liegt am rechten Winkel.', 2: 'Der Abstand liegt am rechten Winkel an.'}),
         wahl('Frage 5', 'Ein Rohr hat den Radius 6.5 cm, der Wasserspiegel ist 12 cm breit, das Wasser steht unter der Mitte. Wie tief ist es?', ['4 cm', '2.5 cm', '9 cm'], 0,
              {0: 'Ja.', 1: 'Das ist der Abstand zur Mitte. Wie tief ist das Wasser darunter?', 2: 'So tief wäre es, wenn der Spiegel über der Mitte läge.'},
              sprich='Ein Rohr hat den Radius sechs Komma fünf Zentimeter, der Wasserspiegel ist zwölf Zentimeter breit, das Wasser steht unter der Mitte. Wie tief ist es?',
              rueck_sprich={1: 'Das ist der Abstand zur Mitte. Wie tief ist das Wasser darunter?', 2: 'So tief wäre es, wenn der Spiegel über der Mitte läge.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung: Ähnliche Figuren
D4 = [(0, 0), (4, 0), (4, 3)]
D8 = [(0, 0), (8, 0), (8, 6)]
clip('aehnlichkeit', 7, 'Geometrie: Ähnliche Figuren',
     'Dreieck 4, 3, 5 mit k = 2: 8, 6, 10; Vorhersage Fläche viermal (6 → 24, vier Teildreiecke); Flächenfaktor k²; '
     'Schatten: Stab 2 m, Schatten 3 m, Baum 15 m Schatten → 10 m; Regal 60 × 40 minus ähnliches mit k = 1/2: 1200 − 300 = 900.',
     ['ähnlich', 'Streckfaktor', 'Flächenfaktor', 'Strahlensatz', 'Verhältnis'], [
         sz('Strecken',
            'Ein rechtwinkliges Dreieck mit den Seiten vier, drei und fünf. Verdoppelst du jede Seite, entsteht ein ähnliches Dreieck: acht, sechs und zehn. Die Winkel bleiben gleich, der Streckfaktor ist zwei.',
            f(r'k = \dfrac{\text{Bild}}{\text{Original}} = \dfrac{8}{4} = \fb{2}', 300, 50, ein='@Streckfaktor'),
            geo(W4, [V(D4, 1, 0.2), RW((4, 0), 90, 180), T(2, -0.7, '4', 1, g=32), T(4.3, 1.5, '3', 1, 'start', g=32)]),
            dazu(W4, [V(D8, 2, 0.1), RW((8, 0), 90, 180), T(4, -0.7, '8', 2, g=32), T(8.3, 3, '6', 2, 'start', g=32), T(3.6, 3.6, '10', 2, 'end', g=32)], '@Verdoppelst')),
         sz('Vorhersage',
            'Die Fläche wird nicht doppelt, sondern viermal so gross. Das grosse Dreieck lässt sich in vier Dreiecke von der Grösse des kleinen zerlegen: sechs Quadratzentimeter werden vierundzwanzig.',
            f(r'6 \cdot \fb{4} = 24\ \text{cm}^2', 300, 56, ein='@sondern'),
            geo(W4, [V(D8, 2, 0.1), V(D4, 1, 0.25)]),
            dazu(W4, [S((4, 0), (4, 3), 2, 3), S((4, 3), (8, 3), 2, 3), S((4, 0), (8, 3), 2, 3)], '@zerlegen')),
         sz('Faktor',
            'Allgemein: Längen werden mit k multipliziert, Flächen mit k Quadrat. Bei k gleich drei werden die Längen dreimal, die Flächen neunmal so gross.',
            f(r'\text{Längen} \cdot k, \qquad \text{Flächen} \cdot \fb{k^2}', 300, 52, ein='@Allgemein'),
            f(r'k = 3: \;\; \text{Fläche} \cdot 9', 420, 52, ein='@Flächen#2')),
         sz('Schatten',
            'Ähnliche Dreiecke helfen beim Messen. Ein zwei Meter langer Stab wirft drei Meter Schatten, ein Baum zur selben Zeit fünfzehn Meter. Die Sonnenstrahlen sind parallel, Stab und Baum stehen senkrecht: Die beiden Dreiecke haben gleiche Winkel, sie sind ähnlich. Also sind die Verhältnisse gleich: Höhe zu Schatten ist zwei zu drei. Der Baum ist zehn Meter hoch.',
            f(r'\dfrac{h}{15} = \dfrac{2}{3} \;\Rightarrow\; h = \fc{10}\ \text{m}', 300, 48, ein='@Verhältnisse'),
            geo(W4S, [S((-1, 0), (17, 0), 5, 3), S((15, 0), (0, 10), 5, 2, gest=True), S((12, 0), (12, 2), 1, 7), RW((12, 0), 0, 90), T(11.7, 0.9, '2 m', 1, 'end', g=28),
                      T(13.5, -1.2, '3 m', 1, g=28), T(7.5, -2.3, '15 m', 2, g=28)], raster=False),
            dazu(W4S, [S((0, 0), (0, 10), 2, 9), RW((0, 0), 0, 90), T(0.5, 5, 'h', 2, 'start', g=34)], '@Baum')),
         sz('Regal',
            'Ein dreieckiges Regalbrett hat die Katheten sechzig und vierzig Zentimeter. Seine Fläche ist sechzig mal vierzig durch zwei, also zwölfhundert Quadratzentimeter. In der Ecke fehlt ein ähnliches Dreieck mit halb so langen Seiten. Seine Fläche ist ein Viertel: dreihundert. Es bleiben neunhundert.',
            f(r'1200 - 1200 \cdot \left(\tfrac{1}{2}\right)^2 = 1200 - 300 = \fc{900}', 300, 40, ein='@Viertel'),
            geo(W4R, [V([(0, 0), (60, 0), (0, 40)], 1, 0.15), RW((0, 0), 0, 90), T(30, -6, '60 cm', 1, g=30), T(1.5, 31, '40 cm', 1, 'start', g=30)], raster=False),
            dazu(W4R, [V([(0, 0), (30, 0), (0, 20)], 2, 0.35), T(15, 2.5, '30', 2, g=28), T(2, 12, '20', 2, 'start', g=28)], '@fehlt')),
         sz('Fehler',
            'Häufiger Fehler: Flächenfaktor gleich Längenfaktor. Werden die Seiten verdreifacht, wird die Fläche nicht dreimal, sondern neunmal so gross.',
            f(r'\fd{\text{Fläche} \cdot 3}', 300, 56, ein='@Fehler'),
            n('Fläche · k², nicht · k', 420, 'rot', 46, ein='@sondern')),
         merke('Zum Mitnehmen: Ähnliche Figuren haben gleiche Winkel, alle Längen werden mit k multipliziert. Flächen werden mit k Quadrat multipliziert. Verhältnisse entsprechender Strecken sind gleich.',
               'Längen · k, Winkel gleich|Flächen · k²|gleiche Verhältnisse'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Alle Seiten des Dreiecks werden verdoppelt. Wie verändert sich die Fläche?', ['viermal so gross', 'doppelt so gross', 'achtmal so gross'], 0,
              {0: 'Ja.', 1: 'Grundseite und Höhe werden beide verdoppelt. Was heisst das für die Fläche?', 2: 'Die Fläche hat zwei Richtungen, nicht drei.'},
              sprich='Alle Seiten des Dreiecks werden verdoppelt. Wie verändert sich die Fläche?',
              rueck_sprich={1: 'Grundseite und Höhe werden beide verdoppelt. Was heisst das für die Fläche?', 2: 'Die Fläche hat zwei Richtungen, nicht drei.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
clip('kontrolle-aehnlichkeit', 8, 'Geometrie: Kontrollfragen zur Ähnlichkeit',
     'Fünf Fragen: Seiten 5, 7, 9 mit k = 2, Fläche 8 cm² mit k = 3, Fläche mal 16, Turm aus Schatten 1.6 m und 24 m, Streckfaktor 3 → 7.5.',
     ['ähnlich', 'Streckfaktor', 'Flächenfaktor', 'Kontrollfragen'], [
         sz('Frage 1', 'Die längste Seite neun wird mal zwei gerechnet: achtzehn Zentimeter.',
            f(r'9 \cdot 2 = \fc{18}\ \text{cm}', 330, 56, ein=1.0)),
         sz('Frage 2', 'Die Fläche wird mal k Quadrat gerechnet, also mal neun: zweiundsiebzig Quadratzentimeter.',
            f(r'8 \cdot 3^2 = \fc{72}\ \text{cm}^2', 330, 56, ein=1.0)),
         sz('Frage 3', 'k Quadrat gleich sechzehn, also ist k gleich vier.',
            f(r'k^2 = 16 \;\Rightarrow\; k = \fc{4}', 330, 56, ein=1.0)),
         sz('Frage 4', 'Der Turmschatten ist fünfzehnmal so lang wie der Stabschatten. Also ist auch der Turm fünfzehnmal so hoch: dreissig Meter.',
            f(r'\dfrac{24}{1.6} = 15, \;\; 2 \cdot 15 = \fc{30}\ \text{m}', 330, 48, ein=1.0)),
         sz('Frage 5', 'Sieben Komma fünf durch drei gibt zwei Komma fünf.',
            f(r'k = \dfrac{7.5}{3} = \fc{2.5}', 330, 56, ein=1.0)),
         merke('Zum Mitnehmen: Längen mal k, Flächen mal k Quadrat. Den Streckfaktor findest du als Bild durch Original.',
               'Längen mal k|Flächen mal k²|k = Bild : Original'),
     ], [
         wahl('Frage 1', 'Ein Dreieck hat die Seiten 5, 7 und 9 cm. Es wird mit k = 2 gestreckt. Wie lang ist die längste Seite des Bildes?', ['18 cm', '11 cm', '81 cm'], 0,
              {0: 'Ja.', 1: 'Ähnlich heisst mal k, nicht plus.', 2: 'Längen werden mal k gerechnet, nicht quadriert.'},
              sprich='Ein Dreieck hat die Seiten fünf, sieben und neun Zentimeter. Es wird mit k gleich zwei gestreckt. Wie lang ist die längste Seite des Bildes?',
              rueck_sprich={1: 'Ähnlich heisst mal k, nicht plus.', 2: 'Längen werden mal k gerechnet, nicht quadriert.'}),
         wahl('Frage 2', 'Eine Figur hat 8 cm² Fläche und wird mit k = 3 gestreckt. Wie gross ist die Bildfläche?', ['72 cm²', '24 cm²', '11 cm²'], 0,
              {0: 'Ja.', 1: 'Länge und Breite wachsen beide. Die Fläche wächst mit k².', 2: 'Ähnlich heisst mal, nicht plus.'},
              sprich='Eine Figur hat acht Quadratzentimeter Fläche und wird mit k gleich drei gestreckt. Wie gross ist die Bildfläche?',
              rueck_sprich={1: 'Länge und Breite wachsen beide. Die Fläche wächst mit k Quadrat.', 2: 'Ähnlich heisst mal, nicht plus.'}),
         wahl('Frage 3', 'Bei einer Streckung wird die Fläche 16-mal so gross. Wie gross ist der Streckfaktor k?', ['4', '16', '8'], 0,
              {0: 'Ja.', 1: '16 ist der Flächenfaktor k². Gesucht ist k.', 2: 'Welche Zahl gibt im Quadrat 16?'},
              sprich='Bei einer Streckung wird die Fläche sechzehnmal so gross. Wie gross ist der Streckfaktor k?',
              rueck_sprich={1: 'Sechzehn ist der Flächenfaktor k Quadrat. Gesucht ist k.', 2: 'Welche Zahl gibt im Quadrat sechzehn?'}),
         wahl('Frage 4', 'Ein 2 m langer Stab wirft 1.6 m Schatten, ein Turm gleichzeitig 24 m. Wie hoch ist der Turm?', ['30 m', '19.2 m', '24.4 m'], 0,
              {0: 'Ja.', 1: 'Der Turm ist höher, als sein Schatten lang ist, wie beim Stab. Prüf das Verhältnis.', 2: 'Ähnlich heisst gleiches Verhältnis, nicht gleicher Unterschied.'},
              sprich='Ein zwei Meter langer Stab wirft eins Komma sechs Meter Schatten, ein Turm gleichzeitig vierundzwanzig Meter. Wie hoch ist der Turm?',
              rueck_sprich={1: 'Der Turm ist höher, als sein Schatten lang ist, wie beim Stab. Prüf das Verhältnis.', 2: 'Ähnlich heisst gleiches Verhältnis, nicht gleicher Unterschied.'}),
         wahl('Frage 5', 'Eine Seite von 3 cm ist im ähnlichen Bild 7.5 cm lang. Wie gross ist k?', ['2.5', '4.5', '0.4'], 0,
              {0: 'Ja.', 1: 'Das ist der Unterschied. k ist ein Faktor: Bild durch Original.', 2: 'Das ist Original durch Bild. Umgekehrt.'},
              sprich='Eine Seite von drei Zentimetern ist im ähnlichen Bild sieben Komma fünf Zentimeter lang. Wie gross ist k?',
              rueck_sprich={1: 'Das ist der Unterschied. k ist ein Faktor: Bild durch Original.', 2: 'Das ist Original durch Bild. Umgekehrt.'}),
     ], art='Kontrollclip')

if FEHLT:
    print('ohne gemessene Wortzeit (geschätzt):', len(FEHLT), FEHLT)
