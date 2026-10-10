"""Erzeugt die acht Drehbücher des Leitprogramms «Funktionstypen und Graphen» (10.10.2026).

  python3 scripts/lp/funktionstypen/clips.py

Gerüst und Zeitlogik aus scripts/lp/lineare-funktionen/clips.py: Je Kapitel ein Einführungsclip (mit einer Vorhersagefrage)
und ein Kontrollclip (fünf Fragen mit neuen Zahlen). Gemessene `dauer` werden beim Neulauf gerettet; Einblendungen
und Stützpunkte von Bewegungen stehen als «@wort» auf dem Wort, das sie nennen (wortzeiten.json, faster-whisper medium).

Bild rechts (x 1010, y 175, 760 × 760), Rechnung links (x 150). Geraden wie im TALS-Leitprogramm lineare-funktionen
(Helfer graf/ueber/ger/bew/dreieck/pt von dort): bewegte Geraden mit Stützpunkten [t, m, b], Begleiter `yachse`
und `dreieck` (Steigungsdreieck). Was erst bei einem Wort erscheint, steht in einem deckungsgleichen `ueber`-Bild.
Wo das Auge Schritte zählt, sind x- und y-Spanne gleich.

Fragebild (HOWTO-leitprogramme §15): In den Kontrollclips zeigt das Bild beim Erscheinen einer Frage nur das Gegebene
(FRAGEBILD unten); die Auflösung erscheint ab 1.0 s, nach der Antwort.

Farben — gleich wie auf der Seite:
  1 blau   = m und die Gerade                       \\fa{…}
  2 orange = b und der Punkt (0 | b)                 \\fb{…}
  3 grün   = «stimmt»: Treffer, Probe, Nullstelle    \\fc{…}
  4 rot    = Fehler                                  \\fd{…}
  5 Tinte  = neutral: gegebener Punkt, Steigungsdreieck, antiproportionale Kurve
Gesprochen: Punkte als «P mit zwei und fünf», Brüche als «… durch …» oder «zwei Drittel», nie «ein Halb» (HOWTO §15).
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
PRAEFIX = 'typ-lp-'
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
         'schlagworte': schlag, 'themenbereich': 'Funktionen · Funktionstypen und Graphen',
         'fach': 'Sekundarstufe I', 'lerngebiet': '3 · Funktionen',
         'lektion': ['lp-funktionstypen'], 'stufe': ['Sek I'], 'datum': '2026-10-10',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Funktionen sehen', 'folge': folge,
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms funktionstypen; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
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


# ---------------------------------------------------------------- Fenster
W_F = dict(xbereich=[-4, 5], ybereich=[-3, 6])                       # 9 / 9
W_W = dict(xbereich=[-1.5, 10.5], ybereich=[-1, 5], xteilung=teil(1, 4, 9), yteilung=teil(1, 2, 3))
W_W2 = dict(xbereich=[-2, 18], ybereich=[-0.8, 5.2], xteilung=teil(4, 9, 16), yteilung=teil(1, 2, 3, 4))
W_A = dict(xbereich=[-2.6, 23.5], ybereich=[-100, 1600], xteilung=teil(5, 10, 15, 20), yteilung=teil(400, 800, 1200))
WZ_ = dict(xname='t [min]', yname='s [m]')
W_P = dict(xbereich=[-0.4, 5.5], ybereich=[-2, 38], xteilung=teil(1, 2, 3, 4, 5), yteilung=teil(10, 20, 30))
PZ = dict(xname='x', yname='y [Fr.]')
W_R = dict(xbereich=[-0.1, 1.75], ybereich=[-1.5, 27], xteilung=[[0.5, '0.5'], [1, '1'], [1.5, '1.5']], yteilung=teil(8, 16, 24))
RZ = dict(xname='t [h]', yname='Strecke [km]')
ANNA = [(0, 0), (10, 800), (15, 800), (20, 1400)]

# ════════════════════════════════════════════════ Kapitel 1 · Einführung: Vier Graphen-Familien
clip('familien', 1, 'Funktionen sehen: Vier Graphen-Familien',
     'Gerade y = x, Parabel y = x² (symmetrisch, Scheitel), Wurzelgraph y = √x (ab 0, immer flacher), Kehrwertgraph y = 1/x '
     '(zwei Äste, keine Achse); Vorhersage (9 | 3), (16 | 4); Testpunkt x = 4; Strecken mit a; Fehler: zu wenige Punkte.',
     ['Parabel', 'Wurzel', 'Kehrwert', 'Gerade', 'Graph'], [
         sz('Gerade',
            'Verschiedene Gleichungen geben verschiedene Graphen. Die einfachste kennst du: y gleich x, eine Gerade durch null, null. '
            'Wird x um eins grösser, wird auch y um eins grösser.',
            f(r'y = x', 300, 72, ein='@einfachste'),
            n('Gerade: gleich viel mehr|bei jedem Schritt', 450, 'blau', 44, ein='@grösser'),
            graf(W_F),
            ueber(W_F, kurven=[kurve('x', -4, 5)], ein='@Gerade')),
         sz('Parabel',
            'y gleich x Quadrat. Für x gleich zwei kommt vier heraus, für minus zwei auch vier. Der Graph ist symmetrisch zur y-Achse, '
            'hat unten einen Scheitel und wird nach aussen immer steiler. Das ist eine Parabel.',
            f(r'y = x^2', 300, 72, ein=0.3),
            n('Parabel: symmetrisch,|Scheitel, immer steiler', 450, 'blau', 44, ein='@symmetrisch'),
            graf(W_F, punkte=[pt(2, 4, 5, '(2 | 4)'), pt(-2, 4, 5, '(−2 | 4)', [-2.3, 4.6], 'end')]),
            ueber(W_F, kurven=[kurve('x*x', -4, 5)], ein='@symmetrisch')),
         sz('Wurzel',
            'y gleich Wurzel aus x. Wurzel aus eins ist eins, Wurzel aus vier ist zwei. Der Graph beginnt bei null, null und wird immer flacher. '
            'Links von der y-Achse gibt es keine Punkte: Aus negativen Zahlen gibt es keine Wurzel.',
            f(r'y = \sqrt{x}', 300, 72, ein=0.3),
            n('Wurzelgraph: ab (0 ∣ 0),|immer flacher, nur x ≥ 0', 450, 'blau', 44, ein='@beginnt'),
            graf(W_W, punkte=[pt(1, 1, 5, '(1 | 1)'), pt(4, 2, 5, '(4 | 2)')]),
            ueber(W_W, kurven=[kurve('sqrt(x)', 0, 10.5)], ein='@beginnt')),
         sz('Kehrwert',
            'y gleich eins durch x. Für x gleich eins kommt eins heraus, für x gleich zwei null Komma fünf, und für x gleich null Komma fünf kommt zwei heraus. '
            'Bei null gibt es keinen Wert. Der Graph hat zwei Äste und trifft keine Achse.',
            f(r'y = \dfrac{1}{x}', 300, 72, ein=0.3),
            n('Kehrwertgraph: zwei Äste,|trifft keine Achse, x ≠ 0', 470, 'blau', 44, ein='@Wert+1.4'),
            graf(W_F, punkte=[pt(1, 1, 5), pt(2, 0.5, 5), pt(0.5, 2, 5)]),
            ueber(W_F, kurven=[kurve('1/x', -4, 5)], ein='@Wert+1.4')),
         sz('Vorhersage',
            'Wurzel aus neun ist drei, Wurzel aus sechzehn ist vier: Das passt zu y gleich Wurzel aus x. Die Gerade y gleich x durch drei trifft nur den ersten Punkt.',
            f(r'\sqrt{9} = 3, \quad \sqrt{16} = 4', 300, 58, ein='@passt'),
            graf(W_W2, punkte=[pt(9, 3, 5, '(9 | 3)', [8.6, 3.6], 'end'), pt(16, 4, 5, '(16 | 4)', [15.6, 4.6], 'end')]),
            ueber(W_W2, kurven=[kurve('sqrt(x)', 0, 18, 3)], ein='@passt')),
         sz('Testpunkt',
            'Mit Testpunkten ordnest du zu. Setz zum Beispiel x gleich vier ein: Die Gerade gibt vier, die Parabel sechzehn, die Wurzel zwei, '
            'der Kehrwert null Komma zwei fünf. Und x gleich null oder eine negative Zahl zeigt, wo es gar keinen Wert gibt.',
            f(r'x = 4: \quad 4, \;\; 16, \;\; 2, \;\; 0.25', 300, 54, ein='@Setz'),
            n('x = 0 und negative x:|Wo gibt es keinen Wert?', 450, 'blau', 42, ein='@negative')),
         sz('Strecken',
            'Eine Zahl davor streckt den Graphen. Zwei x Quadrat ist doppelt so hoch wie x Quadrat. Mit einem Minus davor kippt die Parabel nach unten.',
            f(r'\fa{y = 2x^2} \qquad \fa{y = -x^2}', 300, 58, ein='@Zwei'),
            graf(W_F, kurven=[kurve('x*x', -4, 5, 5)]),
            ueber(W_F, kurven=[kurve('2*x*x', -4, 5)], ein='@Zwei'),
            ueber(W_F, kurven=[kurve('-x*x', -4, 5)], ein='@Minus')),
         sz('Fehler',
            'Häufiger Fehler: zu wenige Punkte. Null, null und eins, eins liegen auf der Geraden und auf der Parabel. Erst x gleich zwei trennt die beiden: zwei gegen vier.',
            n('(0 ∣ 0) und (1 ∣ 1) reichen nicht', 300, 'rot', 44, ein='@wenige'),
            f(r'x = 2: \quad 2 \neq 4', 430, 58, ein='@trennt'),
            graf(W_F, kurven=[kurve('x', -4, 5), kurve('x*x', -4, 5, 5)], punkte=[pt(0, 0, 4), pt(1, 1, 4)]),
            ueber(W_F, punkte=[pt(2, 2, 3, '(2 | 2)', [2.3, 1.4], 'start'), pt(2, 4, 3, '(2 | 4)', [1.7, 4.6], 'end')], ein='@trennt')),
         merke('Zum Mitnehmen: Gerade, Parabel, Wurzel- und Kehrwertgraph erkennst du an der Form. Zum Zuordnen setzt du Testpunkte ein, auch x gleich null und eine negative Zahl.',
               'Gerade · Parabel · Wurzel · Kehrwert|an der Form erkennen|mit Testpunkten zuordnen'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Welche Gleichung passt zu einem Graphen durch P(9 | 3) und Q(16 | 4)?', ['y = √x', 'y = x²', 'y = x : 3'], 0,
              {0: 'Ja.', 1: 'Setz x = 9 ein: 9² = 81, nicht 3.', 2: 'Bei x = 9 stimmt es. Gibt 16 : 3 genau 4?'},
              sprich='Welche Gleichung passt zu einem Graphen durch P mit neun und drei und Q mit sechzehn und vier?',
              rueck_sprich={1: 'Setz x gleich neun ein: neun Quadrat ist einundachtzig, nicht drei.', 2: 'Bei x gleich neun stimmt es. Gibt sechzehn durch drei genau vier?'}),
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
FRAGEBILD.update({('kontrolle-familien', 'Frage 1'): (W_F, [], [pt(-2, 2, 5), pt(0, 0, 5), pt(2, 2, 5)], {'kurven': [kurve('0.5*x*x', -4, 5)]})})
clip('kontrolle-familien', 2, 'Funktionen sehen: Kontrollfragen zu den Familien',
     'Fünf Fragen: Parabel y = 0.5x² im Bild, y = 3/x für x = 6, kein Punkt bei x = −1, y = 2√x für x = 9, Scheitel von y = x² + 2.',
     ['Parabel', 'Wurzel', 'Kehrwert', 'Kontrollfragen'], [
         sz('Frage 1',
            'Symmetrisch zur y-Achse, Scheitel bei null, null, und zwei gibt zwei: y gleich null Komma fünf x Quadrat.',
            f(r'\fc{y = 0.5x^2}', 330, 66, ein=1.0),
            graf(W_F, punkte=[pt(-2, 2, 5), pt(0, 0, 5), pt(2, 2, 5)], kurven=[kurve('0.5*x*x', -4, 5)])),
         sz('Frage 2',
            'Drei durch sechs gibt null Komma fünf.',
            f(r'\dfrac{3}{6} = \fc{0.5}', 330, 64, ein=1.0)),
         sz('Frage 3',
            'Aus minus eins gibt es keine Wurzel. Darum hat y gleich Wurzel aus x bei x gleich minus eins keinen Punkt.',
            f(r'\sqrt{-1}\; \text{gibt es nicht}', 330, 58, ein=1.0)),
         sz('Frage 4',
            'Zuerst die Wurzel: Wurzel aus neun ist drei. Dann mal zwei: sechs.',
            f(r'2 \cdot \sqrt{9} = 2 \cdot 3 = \fc{6}', 330, 60, ein=1.0)),
         sz('Frage 5',
            'Plus zwei schiebt die Parabel um zwei nach oben: Der Scheitel liegt bei null, zwei.',
            f(r'y = x^2 + 2', 300, 64, ein=0.05),
            graf(W_F, kurven=[kurve('x*x+2', -4, 5)]),
            ueber(W_F, punkte=[pt(0, 2, 3, '(0 | 2)')], ein=1.0)),
         merke('Zum Mitnehmen: Form zuerst, dann Testpunkte. Wurzeln gibt es nur für x ab null, Kehrwerte nicht für null. Ein Plus b schiebt den Graphen nach oben.',
               'Form zuerst, dann Testpunkte|√x nur für x ≥ 0, 1/x nicht für 0|plus b: nach oben geschoben'),
     ], [
         wahl('Frage 1', 'Welche Gleichung gehört zum Graphen im Bild?', ['y = 0.5x²', 'y = x²', 'y = √x'], 0,
              {0: 'Ja.', 1: 'Setz x = 2 ein: 2² = 4. Liegt (2 | 4) auf dem Graphen?', 2: 'Ein Wurzelgraph hat links von der y-Achse keine Punkte.'},
              sprich='Welche Gleichung gehört zum Graphen im Bild?',
              rueck_sprich={1: 'Setz x gleich zwei ein: zwei Quadrat ist vier. Liegt dieser Punkt auf dem Graphen?', 2: 'Ein Wurzelgraph hat links von der y-Achse keine Punkte.'}),
         wahl('Frage 2', 'y = 3/x. Wie gross ist y für x = 6?', ['0.5', '2', '18'], 0,
              {0: 'Ja.', 1: 'Das ist 6 durch 3. Im Bruch steht x unten.', 2: 'Das ist 3 mal 6. Hier wird geteilt.'},
              sprich='y gleich drei durch x. Wie gross ist y für x gleich sechs?',
              rueck_sprich={1: 'Das ist sechs durch drei. Im Bruch steht x unten.', 2: 'Das ist drei mal sechs. Hier wird geteilt.'}),
         wahl('Frage 3', 'Welcher Graph hat bei x = −1 keinen Punkt?', ['y = √x', 'y = x²', 'y = 1/x'], 0,
              {0: 'Ja.', 1: '(−1)² = 1: Den Punkt gibt es.', 2: '1 durch −1 ist −1: Den Punkt gibt es.'},
              sprich='Welcher Graph hat bei x gleich minus eins keinen Punkt?',
              rueck_sprich={1: 'Minus eins im Quadrat ist eins: Den Punkt gibt es.', 2: 'Eins durch minus eins ist minus eins: Den Punkt gibt es.'}),
         wahl('Frage 4', 'y = 2√x. Wie gross ist y für x = 9?', ['6', '18', '3'], 0,
              {0: 'Ja.', 1: 'Zuerst die Wurzel aus 9, dann mal 2.', 2: 'Das ist nur die Wurzel. Was macht die 2 davor?'},
              sprich='y gleich zwei mal Wurzel aus x. Wie gross ist y für x gleich neun?',
              rueck_sprich={1: 'Zuerst die Wurzel aus neun, dann mal zwei.', 2: 'Das ist nur die Wurzel. Was macht die Zwei davor?'}),
         wahl('Frage 5', 'Wo liegt der Scheitel der Parabel y = x² + 2?', ['bei (0 | 2)', 'bei (2 | 0)', 'bei (0 | 0)'], 0,
              {0: 'Ja.', 1: 'Setz x = 2 ein: 2² + 2 = 6, nicht 0.', 2: 'Setz x = 0 ein: 0² + 2 = 2.'},
              sprich='Wo liegt der Scheitel der Parabel y gleich x Quadrat plus zwei?',
              rueck_sprich={1: 'Setz x gleich zwei ein: Das gibt sechs, nicht null.', 2: 'Setz x gleich null ein: Das gibt zwei.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung: Proportional, antiproportional, linear
clip('zusammenhaenge', 3, 'Funktionen sehen: Proportional, antiproportional, linear',
     'Benzin 1.80 Fr./l: proportional, Gerade durch (0 | 0); Taxi 6 Fr. + 2.50 Fr./km: linear mit Anfangswert, 4 km kosten 16 statt 22 Fr.; '
     'Pizza 36 Fr. geteilt: antiproportional, Kehrwertgraph; Doppelt-Test; Fehler «steigt, also proportional».',
     ['proportional', 'antiproportional', 'linear', 'Anfangswert', 'Doppelt-Test'], [
         sz('Benzin',
            'Ein Liter Benzin kostet eins Komma achtzig Franken. Zwei Liter kosten drei Franken sechzig, vier Liter sieben Franken zwanzig. '
            'Doppelt so viel Benzin, doppelt so teuer: proportional. Der Graph ist eine Gerade durch null, null.',
            f(r'y = 1.8x', 280, 62, ein=0.3),
            n('proportional:|x doppelt, y doppelt', 420, 'blau', 44, ein='@Doppelt'),
            graf(W_P, punkte=[pt(2, 3.6, 5), pt(4, 7.2, 5)], xname='x [l]', yname='y [Fr.]'),
            ueber(W_P, kurven=[kurve('1.8*x', 0, 5.5)], ein='@Gerade', xname='x [l]', yname='y [Fr.]')),
         sz('Taxi',
            'Vier Kilometer kosten sechzehn Franken, nicht zweiundzwanzig. Die Grundtaxe zählt nur einmal. '
            'Das ist linear mit Anfangswert: eine Gerade, die nicht durch null, null geht.',
            f(r'y = 2.5x + 6', 280, 62, ein=0.05),
            f(r'x = 4: \; 2.5 \cdot 4 + 6 = \fc{16} \neq 22', 400, 50, ein='@nicht'),
            n('linear mit Anfangswert:|x doppelt, y nicht doppelt', 540, 'blau', 42, ein='@linear'),
            graf(W_P, punkte=[pt(2, 11, 5, '(2 | 11)')], xname='x [km]', yname='y [Fr.]'),
            ueber(W_P, kurven=[kurve('2.5*x+6', 0, 5.5)], punkte=[pt(0, 6, 2, '(0 | 6)', [0.25, 3.6], 'start')], ein='@linear', xname='x [km]', yname='y [Fr.]'),
            ueber(W_P, punkte=[pt(4, 16, 3, '(4 | 16)')], ein='@nicht', xname='x [km]', yname='y [Fr.]')),
         sz('Pizza',
            'Eine Pizza-Bestellung kostet sechsunddreissig Franken. Bei zwei Personen zahlt jede achtzehn Franken, bei vier Personen neun. '
            'Doppelt so viele Personen, halb so viel pro Person: antiproportional. Das Produkt bleibt sechsunddreissig, die Punkte liegen auf einem Kehrwertgraphen.',
            f(r'y = \dfrac{36}{x}', 280, 64, ein=0.3),
            n('antiproportional:|x doppelt, y halb', 450, 'blau', 44, ein='@halb'),
            graf(W_P, punkte=[pt(2, 18, 5, '(2 | 18)'), pt(4, 9, 5, '(4 | 9)')], xname='x [Personen]', yname='y [Fr.]'),
            ueber(W_P, punkte=[pt(1, 36, 1), pt(3, 12, 1), pt(5, 7.2, 1)], ein='@Produkt', xname='x [Personen]', yname='y [Fr.]')),
         sz('Test',
            'So unterscheidest du: Schau zuerst die Form an. Dann verdopple x an mehreren Stellen. Wird y jedes Mal doppelt so gross, ist es proportional. '
            'Wird y jedes Mal halb so gross, antiproportional. Eine Gerade, die nicht durch null, null geht, ist linear mit Anfangswert.',
            n('zuerst die Form, dann x verdoppeln:|y immer doppelt: proportional|y immer halb: antiproportional|Gerade nicht durch (0 ∣ 0): linear mit Anfangswert', 280, 'blau', 40, ein='@Form')),
         sz('Fehler',
            'Häufiger Fehler: Was steigt, ist nicht automatisch proportional, das Taxi zeigt es. Und was fällt, ist nicht automatisch antiproportional: '
            'Eine fallende Gerade ist linear.',
            n('steigt: nicht automatisch proportional', 300, 'rot', 42, ein='@steigt'),
            n('fällt: nicht automatisch antiproportional', 420, 'rot', 42, ein='@fällt')),
         merke('Zum Mitnehmen: Proportional ist eine Gerade durch null, null. Linear mit Anfangswert ist eine Gerade, die die y-Achse weiter oben oder unten trifft. '
               'Antiproportional ist ein Kehrwertgraph, das Produkt bleibt gleich.',
               'proportional: Gerade durch (0 ∣ 0)|linear: Gerade mit Anfangswert|antiproportional: Kehrwertgraph'),
         jetzt_du(),
     ], [
         wahl('Taxi', 'Ein Taxi kostet 6 Fr. Grundtaxe und 2.50 Fr. pro km. 2 km kosten 11 Fr. Was kosten 4 km?', ['16 Fr.', '22 Fr.', '11 Fr.'], 0,
              {0: 'Ja.', 1: 'Die Grundtaxe bezahlst du nur einmal, nicht doppelt.', 2: 'Pro Kilometer kommen 2.50 Fr. dazu.'},
              sprich='Ein Taxi kostet sechs Franken Grundtaxe und zwei Franken fünfzig pro Kilometer. Zwei Kilometer kosten elf Franken. Was kosten vier Kilometer?',
              rueck_sprich={1: 'Die Grundtaxe bezahlst du nur einmal, nicht doppelt.', 2: 'Pro Kilometer kommen zwei Franken fünfzig dazu.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
clip('kontrolle-zusammenhaenge', 4, 'Funktionen sehen: Kontrollfragen zu den Zusammenhängen',
     'Fünf Fragen: Kinoeintritte, Pumpen und Zeit, Fitnessabo mit Grundgebühr, Tabelle 12, 6, 3 für x = 6, y = 5x + 2 beim Verdoppeln.',
     ['proportional', 'antiproportional', 'linear', 'Kontrollfragen'], [
         sz('Frage 1',
            'Doppelt so viele Personen zahlen doppelt so viel, und null Personen zahlen nichts: proportional.',
            n('proportional', 330, 'gruen', 50, ein=1.0)),
         sz('Frage 2',
            'Doppelt so viele Pumpen brauchen halb so lange: antiproportional.',
            n('antiproportional', 330, 'gruen', 50, ein=1.0)),
         sz('Frage 3',
            'Die dreissig Franken zahlst du auch ohne Besuch: ein Anfangswert. Linear mit Anfangswert.',
            n('linear mit Anfangswert', 330, 'gruen', 50, ein=1.0)),
         sz('Frage 4',
            'Das Produkt ist immer vierundzwanzig. Bei x gleich sechs ist y also vier.',
            f(r'x \cdot y = 24 \;\Rightarrow\; y = \dfrac{24}{6} = \fc{4}', 330, 54, ein=1.0)),
         sz('Frage 5',
            'Bei x gleich zwei ist y zwölf, bei x gleich vier ist y zweiundzwanzig. Nicht doppelt so viel, wegen des Anfangswerts zwei.',
            f(r'x = 4: \; 5 \cdot 4 + 2 = \fc{22}', 330, 56, ein=1.0)),
         merke('Zum Mitnehmen: Zuerst die Form, dann der Doppelt-Test an mehreren Stellen. Gibt es einen Anfangswert? Bei antiproportional bleibt das Produkt überall gleich.',
               'Form, dann Doppelt-Test an mehreren Stellen|Gibt es einen Anfangswert?|antiproportional: Produkt gleich'),
     ], [
         wahl('Frage 1', 'Ein Kinoeintritt kostet 15 Fr. Kosten für x Personen: welcher Zusammenhang?', ['proportional', 'antiproportional', 'linear mit Anfangswert'], 0,
              {0: 'Ja.', 1: 'Mehr Personen zahlen mehr, nicht weniger.', 2: 'Gibt es Kosten, wenn niemand ins Kino geht?'},
              sprich='Ein Kinoeintritt kostet fünfzehn Franken. Kosten für x Personen: welcher Zusammenhang?',
              rueck_sprich={1: 'Mehr Personen zahlen mehr, nicht weniger.', 2: 'Gibt es Kosten, wenn niemand ins Kino geht?'}),
         wahl('Frage 2', 'Ein Becken wird mit x gleichen Pumpen geleert. Dauer: welcher Zusammenhang?', ['antiproportional', 'proportional', 'linear mit Anfangswert'], 0,
              {0: 'Ja.', 1: 'Mit mehr Pumpen dauert es weniger lang, nicht länger.', 2: 'Mach den Doppelt-Test: doppelt so viele Pumpen, wie lange?'},
              sprich='Ein Becken wird mit x gleichen Pumpen geleert. Dauer: welcher Zusammenhang?',
              rueck_sprich={1: 'Mit mehr Pumpen dauert es weniger lang, nicht länger.', 2: 'Mach den Doppelt-Test: doppelt so viele Pumpen, wie lange?'}),
         wahl('Frage 3', 'Ein Fitnessabo kostet 30 Fr. und 5 Fr. pro Besuch. Welcher Zusammenhang?', ['linear mit Anfangswert', 'proportional', 'antiproportional'], 0,
              {0: 'Ja.', 1: 'Kosten 2 Besuche doppelt so viel wie 1 Besuch?', 2: 'Mehr Besuche kosten mehr, nicht weniger.'},
              sprich='Ein Fitnessabo kostet dreissig Franken und fünf Franken pro Besuch. Welcher Zusammenhang?',
              rueck_sprich={1: 'Kosten zwei Besuche doppelt so viel wie ein Besuch?', 2: 'Mehr Besuche kosten mehr, nicht weniger.'}),
         wahl('Frage 4', 'Tabelle: x: 2, 4, 8 und y: 12, 6, 3. Wie gross ist y bei x = 6?', ['4', '9', '3'], 0,
              {0: 'Ja.', 1: 'Rechne das Produkt x · y. Es bleibt gleich.', 2: '3 ist der Wert bei x = 8. Bei x = 6 ist y grösser.'},
              sprich='Tabelle: x zwei, vier, acht und y zwölf, sechs, drei. Wie gross ist y bei x gleich sechs?',
              rueck_sprich={1: 'Rechne das Produkt x mal y. Es bleibt gleich.', 2: 'Drei ist der Wert bei x gleich acht. Bei x gleich sechs ist y grösser.'}),
         wahl('Frage 5', 'y = 5x + 2. Bei x = 2 ist y = 12. Wie gross ist y bei x = 4?', ['22', '24', '14'], 0,
              {0: 'Ja.', 1: 'Der Anfangswert 2 zählt nur einmal.', 2: 'Setz x = 4 in die Gleichung ein.'},
              sprich='y gleich fünf x plus zwei. Bei x gleich zwei ist y gleich zwölf. Wie gross ist y bei x gleich vier?',
              rueck_sprich={1: 'Der Anfangswert zwei zählt nur einmal.', 2: 'Setz x gleich vier in die Gleichung ein.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung: Weg-Zeit-Graphen lesen
clip('wegzeit', 5, 'Funktionen sehen: Weg-Zeit-Graphen lesen',
     'Annas Schulweg: 10 min mit 80 m/min, 5 min Pause (waagrecht), 5 min mit 120 m/min (steiler); Knick = Tempowechsel; fallend = zurück, '
     'senkrecht unmöglich; Fehler: Graph als Landschaft gelesen.',
     ['Weg-Zeit-Graph', 'Geschwindigkeit', 'Steigung', 'Pause'], [
         sz('Graph',
            'Anna geht zur Schule. Der Graph zeigt, wie weit sie zu jeder Zeit von zu Hause entfernt ist. Nach rechts die Zeit in Minuten, nach oben die Entfernung in Metern.',
            n('t: Zeit in min|s: Entfernung von zu Hause in m', 300, 'blau', 44, ein='@Zeit'),
            graf(W_A, **WZ_)),
         sz('Gehen',
            'In den ersten zehn Minuten kommt sie achthundert Meter weit. Das sind achtzig Meter pro Minute: die Steigung des Graphen.',
            f(r'v = \dfrac{800}{10} = \fa{80}\ \text{m/min}', 300, 54, ein='@Steigung'),
            graf(W_A, punkte=[pt(10, 800, 5, '(10 | 800)', [9.4, 920], 'end')], **WZ_),
            dict(ueber(W_A, ein='@ersten', **WZ_), figuren=zug(ANNA[:2]))),
         sz('Warten',
            'Dann wartet sie fünf Minuten an der Ampel. Die Entfernung bleibt gleich: Der Graph ist waagrecht.',
            n('waagrecht: Pause', 300, 'blau', 46, ein='@waagrecht'),
            dict(graf(W_A, **WZ_), figuren=zug(ANNA[:2])),
            dict(ueber(W_A, ein='@wartet', **WZ_), figuren=zug(ANNA[1:3]))),
         sz('Rennen',
            'Am Schluss rennt sie: sechshundert Meter in fünf Minuten, hundertzwanzig Meter pro Minute. Der steilste Abschnitt ist der schnellste. '
            'Wo das Tempo wechselt, hat der Graph einen Knick.',
            f(r'v = \dfrac{600}{5} = \fa{120}\ \text{m/min}', 300, 54, ein='@rennt+1.5'),
            n('steiler: schneller · Knick: neues Tempo', 450, 'blau', 40, ein='@Knick'),
            dict(graf(W_A, punkte=[pt(20, 1400, 5, '(20 | 1400)', [19.4, 1500], 'end')], **WZ_), figuren=zug(ANNA))),
         sz('Zurück',
            'Geht jemand zurück, wird die Entfernung von zu Hause kleiner: Der Graph fällt. Senkrecht kann er nie sein, denn Weg ohne Zeit gibt es nicht.',
            n('fallend: zurück|senkrecht: unmöglich', 300, 'blau', 44, ein='@fällt'),
            dict(graf(W_A, **WZ_), figuren=zug([(0, 0), (8, 800), (12, 800), (20, 0)])),
            dict(ueber(W_A, ein='@Senkrecht', **WZ_), figuren=[S((14, 200), (14, 1200), 4, 3, gest=True), T(14.4, 1250, 'unmöglich', 4, 'start', g=26)])),
         sz('Fehler',
            'Häufiger Fehler: den Graphen als Landschaft lesen. Steigt er, heisst das nicht, dass es bergauf geht. Er zeigt die Entfernung, nicht die Höhe.',
            n('kein Bild der Landschaft:|Entfernung, nicht Höhe', 300, 'rot', 44, ein='@Landschaft'),
            dict(graf(W_A, **WZ_), figuren=zug(ANNA))),
         merke('Zum Mitnehmen: Im Weg-Zeit-Graphen ist die Steigung die Geschwindigkeit. Waagrecht ist eine Pause, fallend ein Rückweg, ein Knick ein neues Tempo.',
               'Steigung = Geschwindigkeit|waagrecht: Pause · fallend: zurück|Knick: neues Tempo'),
         jetzt_du(),
     ], [
         wahl('Rennen', 'In welchem Abschnitt ist Anna am schnellsten?', ['im dritten', 'im ersten', 'im zweiten'], 0,
              {0: 'Ja.', 1: 'Vergleich die Steilheit: Welcher Abschnitt ist am steilsten?', 2: 'Im zweiten ist der Graph waagrecht. Was heisst das?'},
              sprich='In welchem Abschnitt ist Anna am schnellsten?',
              rueck_sprich={1: 'Vergleich die Steilheit: Welcher Abschnitt ist am steilsten?', 2: 'Im zweiten ist der Graph waagrecht. Was heisst das?'}),
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
W_K3 = dict(xbereich=[-1.3, 11], ybereich=[-50, 1100], xteilung=teil(2, 4, 6, 8, 10), yteilung=teil(200, 400, 600, 800, 1000))
FRAGEBILD.update({
    ('kontrolle-wegzeit', 'Frage 1'): (W_K3, [], [pt(5, 500, 5, '(5 | 500)', [5.4, 430], 'start')], {'figuren': zug([(0, 0), (5, 500)]), **WZ_}),
    ('kontrolle-wegzeit', 'Frage 3'): (W_K3, [], [], {'figuren': zug([(0, 0), (10, 600)], 5) + zug([(0, 0), (10, 900)]) +
                                                        [T(10.2, 560, 'A', 5, 'start', g=34), T(9.6, 950, 'B', 1, 'end', g=34)], **WZ_}),
})
clip('kontrolle-wegzeit', 6, 'Funktionen sehen: Kontrollfragen zu Weg-Zeit-Graphen',
     'Fünf Fragen: Tempo bei 500 m in 5 min, waagrechtes Stück, steilerer Graph, fallender Graph, senkrechtes Stück.',
     ['Weg-Zeit-Graph', 'Geschwindigkeit', 'Kontrollfragen'], [
         sz('Frage 1',
            'Fünfhundert Meter in fünf Minuten: hundert Meter pro Minute.',
            f(r'\dfrac{500}{5} = \fc{100}\ \text{m/min}', 330, 56, ein=1.0),
            dict(graf(W_K3, punkte=[pt(5, 500, 5, '(5 | 500)', [5.4, 430], 'start')], **WZ_), figuren=zug([(0, 0), (5, 500)]))),
         sz('Frage 2',
            'Waagrecht heisst: Die Entfernung bleibt gleich. Die Person steht still.',
            n('steht still', 330, 'gruen', 50, ein=1.0)),
         sz('Frage 3',
            'B ist steiler: In derselben Zeit kommt B weiter. B ist schneller.',
            n('B: steiler, also schneller', 330, 'gruen', 46, ein=1.0),
            dict(graf(W_K3, **WZ_), figuren=zug([(0, 0), (10, 600)], 5) + zug([(0, 0), (10, 900)]))),
         sz('Frage 4',
            'Die Entfernung von zu Hause wird kleiner: Die Person geht nach Hause zurück.',
            n('geht zurück nach Hause', 330, 'gruen', 46, ein=1.0)),
         sz('Frage 5',
            'Senkrecht hiesse: Weg ohne Zeit. Das ist unmöglich.',
            n('unmöglich', 330, 'gruen', 50, ein=1.0)),
         merke('Zum Mitnehmen: Steigung ist Geschwindigkeit. Waagrecht steht man still, fallend geht es zurück, und senkrecht gibt es nicht.',
               'Steigung = Geschwindigkeit|waagrecht: still · fallend: zurück|senkrecht: unmöglich'),
     ], [
         wahl('Frage 1', 'Wie schnell ist die Person im Bild (t in min, s in m)?', ['100 m/min', '500 m/min', '5 m/min'], 0,
              {0: 'Ja.', 1: 'Die 500 m dauern 5 Minuten. Wie viel pro Minute?', 2: 'Geschwindigkeit ist Weg durch Zeit, nicht Zeit durch Weg.'},
              rueck_sprich={1: 'Die fünfhundert Meter dauern fünf Minuten. Wie viel pro Minute?', 2: 'Geschwindigkeit ist Weg durch Zeit, nicht Zeit durch Weg.'}),
         wahl('Frage 2', 'Ein Weg-Zeit-Graph ist ein Stück waagrecht. Was heisst das?', ['Die Person steht still.', 'Die Person geht gleichmässig.', 'Die Person geht bergab.'], 0,
              {0: 'Ja.', 1: 'Gleichmässig gehen gäbe eine schräge Gerade.', 2: 'Der Graph zeigt die Entfernung, nicht die Höhe.'},
              rueck_sprich={1: 'Gleichmässig gehen gäbe eine schräge Gerade.', 2: 'Der Graph zeigt die Entfernung, nicht die Höhe.'}),
         wahl('Frage 3', 'Welche Person im Bild ist schneller?', ['B', 'A', 'beide gleich'], 0,
              {0: 'Ja.', 1: 'Wer kommt in 10 Minuten weiter?', 2: 'Nach 10 Minuten sind sie verschieden weit.'},
              rueck_sprich={1: 'Wer kommt in zehn Minuten weiter?', 2: 'Nach zehn Minuten sind sie verschieden weit.'}),
         wahl('Frage 4', 'Der Graph der Entfernung von zu Hause fällt. Was heisst das?', ['Die Person geht nach Hause zurück.', 'Die Person wird langsamer.', 'Die Person geht bergab.'], 0,
              {0: 'Ja.', 1: 'Langsamer hiesse: flacher, aber immer noch steigend.', 2: 'Der Graph zeigt die Entfernung, nicht die Höhe.'},
              rueck_sprich={1: 'Langsamer hiesse: flacher, aber immer noch steigend.', 2: 'Der Graph zeigt die Entfernung, nicht die Höhe.'}),
         wahl('Frage 5', 'Ein Weg-Zeit-Graph hat ein senkrechtes Stück. Was stimmt?', ['Das ist unmöglich.', 'Die Person ist sehr schnell.', 'Die Person macht eine Pause.'], 0,
              {0: 'Ja.', 1: 'Senkrecht hiesse: Weg ohne jede Zeit. Geht das?', 2: 'Eine Pause wäre waagrecht.'},
              rueck_sprich={1: 'Senkrecht hiesse: Weg ohne jede Zeit. Geht das?', 2: 'Eine Pause wäre waagrecht.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung: Zurückgelegt oder noch entfernt
clip('rest', 7, 'Funktionen sehen: Zurückgelegt oder noch entfernt',
     'Velotour 24 km mit 16 km/h: zurückgelegt s = 16t (steigt), noch entfernt d = 24 − 16t (fällt); gleich gross nach 0.75 h; zusammen immer 24 km; '
     'Diagramme prüfen: zurückgelegter Weg fällt nie, keine senkrechten Stücke, keine nach links.',
     ['zurückgelegt', 'Entfernung', 'Weg-Zeit-Graph', 'Diagramm prüfen'], [
         sz('Tour',
            'Eine Velotour nach Bern ist vierundzwanzig Kilometer lang. Du fährst gleichmässig sechzehn Kilometer pro Stunde.',
            n('24 km bis Bern|16 km pro Stunde', 300, 'blau', 46, ein='@Velotour'),
            graf(W_R, **RZ)),
         sz('Gefahren',
            'Der zurückgelegte Weg wächst: s gleich sechzehn t. Nach einer halben Stunde acht Kilometer, nach einer Stunde sechzehn.',
            f(r'\fa{s = 16t}', 300, 64, ein='@wächst'),
            graf(W_R, **RZ),
            dict(ueber(W_R, ein='@wächst', **RZ), figuren=[S((0, 0), (0.5, 8), 1, 5), T(0.55, 6.2, 's', 1, 'start', g=34)])),
         sz('Rest',
            'Die Entfernung bis Bern nimmt ab: d gleich vierundzwanzig minus sechzehn t. Am Anfang vierundzwanzig, nach einer Stunde noch acht.',
            f(r'\fa{s = 16t}', 260, 54, ein=0.05),
            f(r'\fb{d = 24 - 16t}', 380, 60, ein='@Entfernung'),
            dict(graf(W_R, **RZ), figuren=[S((0, 0), (0.5, 8), 1, 5), T(0.55, 6.2, 's', 1, 'start', g=34)]),
            dict(ueber(W_R, ein='@Entfernung', **RZ), figuren=[S((0, 24), (0.5, 16), 2, 5), T(0.55, 17.5, 'd', 2, 'start', g=34)])),
         sz('Vorhersage',
            'Bei der Hälfte: zwölf Kilometer gefahren, zwölf noch vor dir. Sechzehn t gleich zwölf, t gleich null Komma sieben fünf Stunden, also fünfundvierzig Minuten.',
            f(r'16t = 12 \;\Rightarrow\; t = \fc{0.75}\ \text{h}', 300, 54, ein='@vor+0.5'),
            dict(graf(W_R, **RZ), figuren=[S((0, 0), (0.5, 8), 1, 5), S((0, 24), (0.5, 16), 2, 5)]),
            dict(ueber(W_R, punkte=[pt(0.75, 12, 3, '(0.75 | 12)', [0.75, 6.4], 'middle')], ein='@Hälfte', **RZ),
                 figuren=[S((0.5, 8), (1.5, 24), 1, 5), S((0.5, 16), (1.5, 0), 2, 5), T(1.4, 24.5, 's', 1, 'end', g=34), T(1.4, 3.2, 'd', 2, 'end', g=34)])),
         sz('Summe',
            'Zusammen sind es immer vierundzwanzig Kilometer. Beide Graphen enden bei der Ankunft, nach eins Komma fünf Stunden.',
            f(r's + d = 24', 300, 62, ein='@Zusammen'),
            f(r'\text{Ankunft: } 24 : 16 = 1.5\ \text{h}', 420, 50, ein='@Ankunft'),
            dict(graf(W_R, **RZ), figuren=[S((0, 0), (1.5, 24), 1, 5), S((0, 24), (1.5, 0), 2, 5), T(1.4, 24.5, 's', 1, 'end', g=34), T(1.4, 3.2, 'd', 2, 'end', g=34)])),
         sz('Prüfen',
            'Prüf jedes Bewegungsdiagramm. Der zurückgelegte Weg kann nie kleiner werden, eine Entfernung schon. Und kein Stück ist senkrecht oder läuft nach links.',
            n('zurückgelegt: nie fallend|Entfernung: darf fallen|nie senkrecht, nie nach links', 300, 'blau', 42, ein='@Prüf')),
         merke('Zum Mitnehmen: Zurückgelegt wächst, noch entfernt nimmt ab, zusammen ergeben sie die ganze Strecke. Lies immer zuerst, was an der y-Achse steht.',
               'zurückgelegt wächst · Rest nimmt ab|zusammen: ganze Strecke|zuerst die y-Achse lesen'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', '24 km mit 16 km/h: Wann sind zurückgelegter Weg und Rest gleich gross?', ['nach 0.75 h', 'nach 1.5 h', 'nach 12 h'], 0,
              {0: 'Ja.', 1: 'Nach 1.5 h bist du schon in Bern.', 2: 'Die 12 sind Kilometer, nicht Stunden.'},
              sprich='Vierundzwanzig Kilometer mit sechzehn Kilometern pro Stunde: Wann sind zurückgelegter Weg und Rest gleich gross?',
              rueck_sprich={1: 'Nach eins Komma fünf Stunden bist du schon in Bern.', 2: 'Die Zwölf sind Kilometer, nicht Stunden.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
W_K4 = dict(xbereich=[-1.8, 15], ybereich=[-60, 1100], xteilung=teil(4, 8, 12), yteilung=teil(400, 800))
FRAGEBILD.update({('kontrolle-rest', 'Frage 5'): (W_K4, [], [], {'figuren': zug([(0, 0), (8, 600), (6, 900), (12, 1000)]), 'xname': 't [min]', 'yname': 'zurückgelegt [m]'})})
clip('kontrolle-rest', 8, 'Funktionen sehen: Kontrollfragen zurückgelegt oder entfernt',
     'Fünf Fragen: 30 km mit 20 km/h nach 0.5 h, welcher Graph fällt, Hälfte bei 30 km, zurückgelegter Weg auf dem Heimweg, Diagramm nach links.',
     ['zurückgelegt', 'Entfernung', 'Kontrollfragen'], [
         sz('Frage 1',
            'Nach einer halben Stunde sind zehn Kilometer gefahren. Bleiben zwanzig Kilometer.',
            f(r'30 - 20 \cdot 0.5 = \fc{20}', 330, 58, ein=1.0)),
         sz('Frage 2',
            'Die Entfernung zum Ziel wird kleiner, ihr Graph fällt. Der zurückgelegte Weg wächst.',
            n('Entfernung zum Ziel fällt', 330, 'gruen', 46, ein=1.0)),
         sz('Frage 3',
            'Die Hälfte sind fünfzehn Kilometer. Fünfzehn durch zwölf gibt eins Komma zwei fünf Stunden.',
            f(r'15 : 12 = \fc{1.25}\ \text{h}', 330, 58, ein=1.0)),
         sz('Frage 4',
            'Zurückgelegt und noch entfernt ergeben zusammen die ganze Strecke: Dreissig minus achtzehn gibt zwölf Kilometer.',
            f(r'30 - 18 = \fc{12}\ \text{km}', 330, 58, ein=1.0)),
         sz('Frage 5',
            'Ein Stück läuft nach links: Die Zeit liefe rückwärts. Das ist unmöglich.',
            n('Zeit läuft nie rückwärts', 330, 'gruen', 46, ein=1.0),
            dict(graf(W_K4, xname='t [min]', yname='zurückgelegt [m]'), figuren=zug([(0, 0), (8, 600)]) + zug([(8, 600), (6, 900)], 4) + zug([(6, 900), (12, 1000)]))),
         merke('Zum Mitnehmen: Zurückgelegter Weg und Entfernung zum Ziel ergeben zusammen die ganze Strecke. Der zurückgelegte Weg nimmt nie ab, und die Zeit läuft nur nach rechts.',
               'zurückgelegt + noch entfernt = ganze Strecke|zurückgelegt nimmt nie ab|Zeit nur nach rechts'),
     ], [
         wahl('Frage 1', 'Eine Tour ist 30 km lang, du fährst 20 km/h. Wie weit ist es nach 0.5 h noch?', ['20 km', '10 km', '29.5 km'], 0,
              {0: 'Ja.', 1: 'Das ist die gefahrene Strecke. Gefragt ist, was noch bleibt.', 2: 'Gefahren hast du 20 · 0.5 km, nicht 0.5 km.'},
              sprich='Eine Tour ist dreissig Kilometer lang, du fährst zwanzig Kilometer pro Stunde. Wie weit ist es nach einer halben Stunde noch?',
              rueck_sprich={1: 'Das ist die gefahrene Strecke. Gefragt ist, was noch bleibt.', 2: 'Gefahren hast du zwanzig mal null Komma fünf Kilometer, nicht null Komma fünf Kilometer.'}),
         wahl('Frage 2', 'Welcher Graph fällt auf dem Weg zum Ziel?', ['die Entfernung zum Ziel', 'der zurückgelegte Weg', 'keiner'], 0,
              {0: 'Ja.', 1: 'Je länger du fährst, desto mehr hast du zurückgelegt.', 2: 'Einer wird kleiner, je näher du dem Ziel kommst.'},
              rueck_sprich={1: 'Je länger du fährst, desto mehr hast du zurückgelegt.', 2: 'Einer wird kleiner, je näher du dem Ziel kommst.'}),
         wahl('Frage 3', '30 km mit 12 km/h: Nach welcher Zeit ist die Hälfte gefahren?', ['1.25 h', '2.5 h', '15 h'], 0,
              {0: 'Ja.', 1: 'Nach 2.5 h bist du am Ziel.', 2: 'Die Hälfte sind 15 Kilometer, nicht 15 Stunden.'},
              sprich='Dreissig Kilometer mit zwölf Kilometern pro Stunde: Nach welcher Zeit ist die Hälfte gefahren?',
              rueck_sprich={1: 'Nach zwei Komma fünf Stunden bist du am Ziel.', 2: 'Die Hälfte sind fünfzehn Kilometer, nicht fünfzehn Stunden.'}),
         wahl('Frage 4', 'Auf dem Heimweg: Was macht der zurückgelegte Weg?', ['Er wächst weiter.', 'Er wird kleiner.', 'Er bleibt gleich.'], 0,
              {0: 'Ja.', 1: 'Kleiner wird die Entfernung von zu Hause. Gefahren hast du immer mehr.', 2: 'Du fährst ja weiter.'},
              rueck_sprich={1: 'Kleiner wird die Entfernung von zu Hause. Gefahren hast du immer mehr.', 2: 'Du fährst ja weiter.'}),
         wahl('Frage 5', 'Was ist an diesem Diagramm falsch?', ['Ein Stück läuft nach links.', 'Ein Stück ist zu steil.', 'Nichts.'], 0,
              {0: 'Ja.', 1: 'Steil heisst nur schnell. Schau, in welche Richtung die Zeit läuft.', 2: 'Folge dem Graphen von links nach rechts.'},
              rueck_sprich={1: 'Steil heisst nur schnell. Schau, in welche Richtung die Zeit läuft.', 2: 'Folge dem Graphen von links nach rechts.'}),
     ], art='Kontrollclip')

if FEHLT:
    print('ohne gemessene Wortzeit (geschätzt):', len(FEHLT), FEHLT)
