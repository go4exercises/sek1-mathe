"""Erzeugt die acht Drehbücher des Leitprogramms «Darstellungen wechseln» (Lineare Funktionen II, 10.10.2026).

  python3 scripts/lp/darstellungen/clips.py

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
PRAEFIX = 'dar-lp-'
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
         'schlagworte': schlag, 'themenbereich': 'Funktionen · Darstellungen wechseln',
         'fach': 'Sekundarstufe I', 'lerngebiet': '3 · Funktionen',
         'lektion': ['lp-darstellungen'], 'stufe': ['Sek I'], 'datum': '2026-10-10',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Funktionen sehen', 'folge': folge,
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms darstellungen; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
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


def kurve(formel, von, bis, farbe=5):
    return dict(formel=formel, farbe=farbe, von=von, bis=bis)


# ---------------------------------------------------------------- Fenster
W_K = dict(xbereich=[-0.6, 11], ybereich=[-8, 115], xteilung=teil(0, 2, 4, 6, 8, 10), yteilung=teil(0, 20, 40, 60, 80, 100))
KH = dict(xname='x [Eintritte]', yname='y [Fr.]')
W_R = dict(xbereich=[-1, 14], ybereich=[-1, 14], xteilung=teil(0, 2, 4, 6, 8, 10, 12), yteilung=teil(0, 2, 4, 6, 8, 10, 12))
RE = dict(xname='x [cm]', yname='y [cm]')
W_T = dict(xbereich=[-1.5, 26], ybereich=[-3, 42], xteilung=teil(0, 5, 10, 15, 20, 25), yteilung=teil(0, 5, 10, 15, 20, 25, 30, 35, 40))
TR = dict(xname='h [cm]', yname='a [cm]')
W_V = dict(xbereich=[-1.5, 33], ybereich=[-0.3, 3.6], xteilung=teil(0, 10, 20, 30), yteilung=teil(1, 2, 3))
VE = dict(xname='v [km/h]', yname='t [h]')
W_S = dict(xbereich=[-0.15, 3.2], ybereich=[-3, 34], xteilung=teil(1, 2, 3), yteilung=teil(0, 10, 20, 30))
SR = dict(xname='t [h]', yname='s [km]')
TAB_K = r'\begin{array}{c|ccccc} x & 0 & 1 & 2 & 3 & 4 \\ \hline y & 40 & 46 & 52 & 58 & 64 \end{array}'

# ════════════════════════════════════════════════ Kapitel 1 · Einführung: Vier Darstellungen
clip('darstellungen', 1, 'Funktionen sehen: Vier Darstellungen',
     'Kletterhalle: 40 Fr. Jahresbeitrag und 6 Fr. pro Eintritt als Text, Gleichung y = 6x + 40, Tabelle und Graph aus Punkten; '
     'der Punkt (5 | 70) in Worten; rückwärts 100 Fr. → 10 Eintritte; Tabelle mit Schritt 2 → m = 12/2 = 6; Fehler m = 12.',
     ['Darstellung', 'Wertetabelle', 'Graph', 'Gleichung', 'deuten'], [
         sz('Situation',
            'In einer Kletterhalle zahlst du vierzig Franken Jahresbeitrag und dazu sechs Franken für jeden Eintritt. '
            'Das kannst du auf vier Arten zeigen: als Text, als Gleichung, als Tabelle und als Graph.',
            n('Text: 40 Fr. im Jahr,|dazu 6 Fr. pro Eintritt', 300, 'blau', 46, ein='@Kletterhalle'),
            n('Text · Gleichung · Tabelle · Graph', 470, 'blau', 40, ein='@vier'),
            graf(W_K, **KH)),
         sz('Gleichung',
            'x ist die Anzahl Eintritte, y sind die Kosten in Franken. Zu den vierzig Franken kommen x mal sechs Franken: '
            'y gleich sechs x plus vierzig.',
            f(r'y = \fa{6}x + \fb{40}', 300, 72, ein='@gleich'),
            n('x: Anzahl Eintritte|y: Kosten in Fr.', 450, 'blau', 42, ein=0.3),
            graf(W_K, **KH)),
         sz('Tabelle',
            'In der Tabelle setzt du null, eins, zwei, drei und vier ein. Bei jedem Eintritt mehr kommen sechs Franken dazu. '
            'Im Graphen wird jedes Wertepaar ein Punkt.',
            f(r'y = \fa{6}x + \fb{40}', 260, 56, ein=0.05),
            f(TAB_K, 380, 50, ein='@Tabelle'),
            n('+ 6 pro Eintritt', 560, 'blau', 42, ein='@Bei'),
            graf(W_K, **KH),
            ueber(W_K, punkte=[pt(0, 40, 2), pt(1, 46, 5), pt(2, 52, 5), pt(3, 58, 5), pt(4, 64, 5)], ein='@Wertepaar', **KH)),
         sz('Punkte',
            'Weil es nur ganze Eintritte gibt, zeichnest du einzelne Punkte und keine durchgezogene Linie. Sie liegen auf einer Geraden.',
            n('nur ganze Eintritte:|einzelne Punkte', 300, 'blau', 46, ein='@ganze'),
            graf(W_K, punkte=[pt(x, 6 * x + 40, 2 if x == 0 else 5) for x in range(11)], **KH),
            ueber(W_K, [ger(6, 40, 5, gestrichelt=True)], ein='@liegen', **KH)),
         sz('Vorhersage',
            'Der Punkt fünf, siebzig heisst: Fünf Eintritte kosten zusammen siebzig Franken. Der y-Wert ist das Ganze, nicht der Preis eines Eintritts.',
            f(r'(5 \mid 70)', 300, 66, ein=0.05),
            f(r'6 \cdot 5 + 40 = \fc{70}', 430, 56, ein='@zusammen'),
            n('5 Eintritte kosten zusammen 70 Fr.', 560, 'gruen', 42, ein='@zusammen'),
            graf(W_K, punkte=[pt(x, 6 * x + 40, 2 if x == 0 else 5) for x in range(11)], **KH),
            ueber(W_K, punkte=[pt(5, 70, 3, '(5 | 70)', [4.6, 80], 'end')], ein=0.05, **KH)),
         sz('Rückwärts',
            'Umgekehrt: Wie viele Eintritte bekommst du für hundert Franken? Sechs x plus vierzig gleich hundert, '
            'sechs x gleich sechzig, also x gleich zehn.',
            f(r'6x + 40 = 100', 280, 58, ein='@Sechs'),
            f(r'6x = 60 \qquad \fc{x = 10}', 400, 58, ein='@also'),
            graf(W_K, punkte=[pt(x, 6 * x + 40, 2 if x == 0 else 5) for x in range(11)], **KH),
            ueber(W_K, punkte=[pt(10, 100, 3, '(10 | 100)', [9.6, 108], 'end')], ein='@also', **KH)),
         sz('Schritt',
            'Beginnt eine Tabelle nicht bei null, rechnest du zuerst m. Hier springt x um zwei und y um zwölf. '
            'm ist zwölf durch zwei, also sechs. Dann ein Wertepaar einsetzen: zweiundfünfzig gleich sechs mal zwei plus b, also b gleich vierzig.',
            f(r'\begin{array}{c|ccc} x & 2 & 4 & 6 \\ \hline y & 52 & 64 & 76 \end{array}', 240, 50, ein=0.3),
            f(r'm = \dfrac{\Delta y}{\Delta x} = \dfrac{12}{2} = \fa{6}', 420, 52, ein='@springt'),
            f(r'52 = 6 \cdot 2 + b \quad \Rightarrow \quad \fb{b = 40}', 600, 50, ein='@einsetzen')),
         sz('Fehler',
            'Häufiger Fehler: die zwölf als Steigung nehmen. Die zwölf gehört aber zu zwei Schritten. Und der Punkt fünf, siebzig heisst nicht, '
            'dass ein Eintritt siebzig Franken kostet.',
            f(r'\fd{m = 12}', 300, 62, ein='@Steigung'),
            n('12 gehört zu 2 Schritten: m = 6', 430, 'rot', 42, ein='@gehört'),
            n('(5 ∣ 70): nicht «ein Eintritt kostet 70 Fr.»', 560, 'rot', 42, ein='@Punkt')),
         merke('Zum Mitnehmen: Text, Gleichung, Tabelle und Graph zeigen dieselbe Situation. In der Tabelle ist m gleich delta y durch delta x, '
               'auch wenn x in grösseren Schritten springt. Und ein Punkt sagt: Bei diesem x ist das Ganze so gross.',
               'vier Darstellungen, eine Situation|m = Δy / Δx, auch bei grossen Schritten|Punkt: bei diesem x so viel insgesamt'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Was bedeutet der Punkt (5 | 70)?',
              ['5 Eintritte kosten zusammen 70 Fr.', 'Ein Eintritt kostet 70 Fr.', 'Für 5 Fr. gibt es 70 Eintritte.'], 0,
              {0: 'Ja.', 1: 'Der y-Wert ist das Ganze bei x = 5, nicht der Preis pro Eintritt.', 2: 'Im Punkt steht zuerst x, die Anzahl Eintritte, dann y, die Kosten.'},
              sprich='Was bedeutet der Punkt fünf, siebzig?',
              rueck_sprich={1: 'Der y-Wert ist das Ganze bei x gleich fünf, nicht der Preis pro Eintritt.',
                            2: 'Im Punkt steht zuerst x, die Anzahl Eintritte, dann y, die Kosten.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
W_K1 = dict(xbereich=[-0.5, 7], ybereich=[-2, 22], xteilung=teil(0, 2, 4, 6), yteilung=teil(0, 5, 10, 15, 20))
clip('kontrolle-darstellungen', 2, 'Funktionen sehen: Kontrollfragen zu den Darstellungen',
     'Fünf Fragen: Streaming 5 Fr. + 2 Fr. pro Film als Gleichung, m aus einer Tabelle mit Schritt 2, der Punkt (3 | 11) in Worten, '
     'Gleichung aus der Tabelle 10, 6, 2, Bedeutung von 0.5 in y = 0.5x + 3.',
     ['Darstellung', 'Wertetabelle', 'deuten', 'Kontrollfragen'], [
         sz('Frage 1',
            'Fünf Franken sind fix, das ist b. Pro Film zwei Franken, das ist m. Also y gleich zwei x plus fünf.',
            f(r'\fc{y = 2x + 5}', 330, 62, ein=1.0),
            graf(W_K1, punkte=[pt(x, 2 * x + 5, 2 if x == 0 else 5) for x in range(7)], xname='x [Filme]', yname='y [Fr.]')),
         sz('Frage 2',
            'x springt um zwei, y um sechs. m ist sechs durch zwei, also drei.',
            f(r'\begin{array}{c|ccc} x & 0 & 2 & 4 \\ \hline y & 7 & 13 & 19 \end{array}', 260, 50, ein=0.05),
            f(r'm = \dfrac{6}{2} = \fc{3}', 440, 56, ein=1.0)),
         sz('Frage 3',
            'Der Punkt drei, elf heisst: Drei Filme kosten zusammen elf Franken.',
            f(r'2 \cdot 3 + 5 = \fc{11}', 330, 56, ein=1.0),
            graf(W_K1, punkte=[pt(x, 2 * x + 5, 5) for x in range(7)], xname='x [Filme]', yname='y [Fr.]'),
            ueber(W_K1, punkte=[pt(3, 11, 3, '(3 | 11)', [2.7, 13], 'end')], ein=1.0, xname='x [Filme]', yname='y [Fr.]')),
         sz('Frage 4',
            'x springt um zwei, y fällt um vier: m ist minus zwei. Von x gleich eins zurück bis null: zehn plus zwei gibt zwölf. y gleich minus zwei x plus zwölf.',
            f(r'\begin{array}{c|ccc} x & 1 & 3 & 5 \\ \hline y & 10 & 6 & 2 \end{array}', 260, 50, ein=0.05),
            f(r'm = \dfrac{-4}{2} = -2, \quad b = 12', 440, 50, ein=1.0),
            f(r'\fc{y = -2x + 12}', 570, 56, ein=1.0)),
         sz('Frage 5',
            'Die null Komma fünf steht vor dem x: Pro Stunde steigt das Wasser um null Komma fünf Dezimeter. Die drei ist der Wasserstand am Anfang.',
            f(r'y = \fa{0.5}x + \fb{3}', 330, 60, ein=0.05),
            n('pro Stunde + 0.5 dm', 470, 'gruen', 44, ein=1.0)),
         merke('Zum Mitnehmen: Zuerst klären, was x und was y ist. m ist die Änderung pro Schritt, b der Wert bei x gleich null, und ein Punkt sagt, wie viel es bei diesem x insgesamt ist.',
               'zuerst: Was ist x, was ist y?|m pro Schritt, b bei x = 0|Punkt: insgesamt bei diesem x'),
     ], [
         wahl('Frage 1', 'Ein Streamingdienst kostet 5 Fr. im Monat und 2 Fr. pro Film. Welche Gleichung passt (x: Filme, y: Fr.)?',
              ['y = 2x + 5', 'y = 5x + 2', 'y = 7x'], 0,
              {0: 'Ja.', 1: 'Prüf mit x = 0: Ohne Film zahlst du 5 Fr.', 2: 'Die 5 Fr. kommen nur einmal dazu, nicht bei jedem Film.'},
              sprich='Ein Streamingdienst kostet fünf Franken im Monat und zwei Franken pro Film. Welche Gleichung passt?',
              rueck_sprich={1: 'Prüf mit x gleich null: Ohne Film zahlst du fünf Franken.', 2: 'Die fünf Franken kommen nur einmal dazu, nicht bei jedem Film.'}),
         wahl('Frage 2', 'Tabelle: x: 0, 2, 4 und y: 7, 13, 19. Wie gross ist m?', ['3', '6', '7'], 0,
              {0: 'Ja.', 1: 'Die 6 gehört zu 2 Schritten in x.', 2: 'Das ist der Wert bei x = 0, also b.'},
              sprich='Tabelle: x null, zwei, vier und y sieben, dreizehn, neunzehn. Wie gross ist m?',
              rueck_sprich={1: 'Die Sechs gehört zu zwei Schritten in x.', 2: 'Das ist der Wert bei x gleich null, also b.'}),
         wahl('Frage 3', 'Beim Streaming (y = 2x + 5): Was bedeutet der Punkt (3 | 11)?',
              ['3 Filme kosten zusammen 11 Fr.', 'Ein Film kostet 11 Fr.', '11 Filme kosten 3 Fr.'], 0,
              {0: 'Ja.', 1: 'Der y-Wert ist das Ganze bei x = 3.', 2: 'Im Punkt steht zuerst x, die Anzahl Filme.'},
              sprich='Beim Streaming: Was bedeutet der Punkt drei, elf?',
              rueck_sprich={1: 'Der y-Wert ist das Ganze bei x gleich drei.', 2: 'Im Punkt steht zuerst x, die Anzahl Filme.'}),
         wahl('Frage 4', 'Tabelle: x: 1, 3, 5 und y: 10, 6, 2. Welche Gleichung passt?', ['y = −2x + 12', 'y = −4x + 10', 'y = −2x + 10'], 0,
              {0: 'Ja.', 1: 'Die −4 gehört zu 2 Schritten in x.', 2: 'Die 10 ist der Wert bei x = 1, nicht bei x = 0.'},
              sprich='Tabelle: x eins, drei, fünf und y zehn, sechs, zwei. Welche Gleichung passt?',
              rueck_sprich={1: 'Die minus vier gehört zu zwei Schritten in x.', 2: 'Die Zehn ist der Wert bei x gleich eins, nicht bei x gleich null.'}),
         wahl('Frage 5', 'Ein Pool wird gefüllt: y = 0.5x + 3 (x in Stunden, y in dm). Was bedeutet 0.5?',
              ['Pro Stunde steigt das Wasser um 0.5 dm.', 'Am Anfang steht das Wasser 0.5 dm hoch.', 'Nach 0.5 Stunden ist der Pool voll.'], 0,
              {0: 'Ja.', 1: 'Was am Anfang ist, sagt die Zahl ohne x.', 2: 'Die Zahl vor dem x ist die Änderung pro Stunde.'},
              sprich='Ein Pool wird gefüllt: y gleich null Komma fünf x plus drei. Was bedeutet null Komma fünf?',
              rueck_sprich={1: 'Was am Anfang ist, sagt die Zahl ohne x.', 2: 'Die Zahl vor dem x ist die Änderung pro Stunde.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung: Wenn die Summe gleich bleibt
clip('summe', 3, 'Funktionen sehen: Wenn die Summe gleich bleibt',
     'Rechteck mit Umfang 24 cm: 2x + 2y = 24 → x + y = 12 → y = 12 − x; die Ecke (x | y) läuft auf der Geraden, Steigung −1; '
     'Einkauf 3x + 2y = 30 → y = 15 − 1.5x; Fehler y = 24 − 2x mit Probe.',
     ['Umfang', 'Summe', 'nach y auflösen', 'fallend'], [
         sz('Rechteck',
            'Ein Rechteck hat den Umfang vierundzwanzig Zentimeter. Seine Seiten heissen x und y. Wie hängen sie zusammen?',
            n('Umfang 24 cm|Seiten x und y', 300, 'blau', 46, ein='@Umfang'),
            dict(graf(W_R, **RE), figuren=[rechteck(3, 9), T(1.5, 0.45, 'x', 1, g=30), T(0.45, 4.5, 'y', 1, 'start', g=30)])),
         sz('Gleichung',
            'Jede Seite kommt zweimal vor: zwei x plus zwei y gleich vierundzwanzig. Durch zwei: x plus y gleich zwölf. '
            'Minus x: y gleich zwölf minus x.',
            f(r'2x + 2y = 24 \qquad | : 2', 260, 54, ein='@Seite'),
            f(r'x + y = 12 \qquad | - x', 380, 54, ein='@Durch'),
            f(r'\fc{y = 12 - x}', 500, 62, ein='@Minus'),
            dict(graf(W_R, **RE), figuren=[rechteck(3, 9)])),
         sz('Vorhersage',
            'Für x gleich fünf ist y gleich zwölf minus fünf, also sieben Zentimeter. Probe: zwei mal fünf plus zwei mal sieben gibt vierundzwanzig.',
            f(r'y = 12 - x', 260, 56, ein=0.05),
            f(r'x = 5: \quad y = 12 - 5 = \fc{7}', 380, 54, ein='@sieben'),
            f(r'2 \cdot 5 + 2 \cdot 7 = 24', 500, 50, ein='@Probe'),
            dict(graf(W_R, **RE), figuren=[mit(rechteck(5, 7), ein='@sieben')])),
         sz('Gerade',
            'Alle Rechtecke mit diesem Umfang: Ihre obere rechte Ecke liegt auf der Geraden y gleich zwölf minus x. '
            'Wird x um eins länger, wird y um eins kürzer. Die Steigung ist minus eins.',
            f(r'y = \fa{-1} \cdot x + \fb{12}', 280, 58, ein='@Geraden'),
            n('x + 1 cm, y − 1 cm', 420, 'blau', 44, ein='@länger'),
            dict(graf(W_R, **RE), figuren=[dict(rechteck(2, 10), bewegung=[['@Alle', {}], ['@Ecke+1.2', {'punkte': [[0, 0], [10, 0], [10, 2], [0, 2]]}],
                                                                             ['@Wird', {}], ['@kürzer+0.5', {'punkte': [[0, 0], [4, 0], [4, 8], [0, 8]]}]])]),
            ueber(W_R, [bew([[0, -1, 12]], dreieck=dreieck(5, 1, ein='@länger'))], ein='@Geraden', **RE)),
         sz('Preise',
            'Das geht auch mit Preisen. Für dreissig Franken kaufst du Getränke zu drei Franken und Snacks zu zwei Franken. '
            'Drei x plus zwei y gleich dreissig. Minus drei x, dann durch zwei: y gleich fünfzehn minus eins Komma fünf x.',
            f(r'3x + 2y = 30', 260, 56, ein='@Drei'),
            f(r'2y = 30 - 3x', 380, 56, ein='@Minus'),
            f(r'\fc{y = 15 - 1.5x}', 500, 60, ein='@fünfzehn')),
         sz('Fehler',
            'Häufiger Fehler: nur zwei x abziehen und nicht durch zwei teilen. y gleich vierundzwanzig minus zwei x stimmt nicht: '
            'Mit x gleich zwei wäre y gleich zwanzig, und der Umfang wäre vierundvierzig.',
            f(r'\fd{y = 24 - 2x}', 280, 62, ein='@abziehen'),
            f(r'x = 2: \quad 2 \cdot 2 + 2 \cdot 20 = \fd{44} \neq 24', 420, 50, ein='@wäre')),
         merke('Zum Mitnehmen: Bleibt eine Summe gleich, ist der Zusammenhang linear fallend. Löse nach y auf: zuerst den x-Teil abziehen, '
               'dann durch die Zahl vor dem y teilen. Mach die Probe mit einer Zahl.',
               'feste Summe: linear fallend|zuerst x-Teil weg, dann durch die Zahl vor y|Probe mit einer Zahl'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Umfang 24 cm, x = 5 cm. Wie lang ist y?', ['7 cm', '19 cm', '14 cm'], 0,
              {0: 'Ja.', 1: 'Im Umfang kommt jede Seite zweimal vor: Rechne die Probe 2 · 5 + 2 · 19.', 2: 'Du hast 24 − 2 · 5 gerechnet. Dann gehört y aber zweimal dazu.'},
              sprich='Umfang vierundzwanzig Zentimeter, x gleich fünf Zentimeter. Wie lang ist y?',
              rueck_sprich={1: 'Im Umfang kommt jede Seite zweimal vor: Rechne die Probe zwei mal fünf plus zwei mal neunzehn.',
                            2: 'Du hast vierundzwanzig minus zwei mal fünf gerechnet. Dann gehört y aber zweimal dazu.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
clip('kontrolle-summe', 4, 'Funktionen sehen: Kontrollfragen zur festen Summe',
     'Fünf Fragen: Rechteck mit Umfang 30 cm als Gleichung und für x = 4, 2x + y = 10 und 3x + 3y = 21 nach y, Zaun an einer Mauer 2x + y = 40.',
     ['Umfang', 'nach y auflösen', 'Kontrollfragen'], [
         sz('Frage 1',
            'Zwei x plus zwei y gleich dreissig, durch zwei: x plus y gleich fünfzehn. Also y gleich fünfzehn minus x.',
            f(r'2x + 2y = 30 \;\Rightarrow\; \fc{y = 15 - x}', 330, 56, ein=1.0)),
         sz('Frage 2',
            'y gleich fünfzehn minus vier, also elf Zentimeter. Probe: zwei mal vier plus zwei mal elf gibt dreissig.',
            f(r'y = 15 - 4 = \fc{11}', 300, 58, ein=1.0),
            f(r'2 \cdot 4 + 2 \cdot 11 = 30', 420, 50, ein=1.0)),
         sz('Frage 3',
            'Minus zwei x auf beiden Seiten: y gleich minus zwei x plus zehn.',
            f(r'2x + y = 10 \;\Rightarrow\; \fc{y = -2x + 10}', 330, 56, ein=1.0)),
         sz('Frage 4',
            'Durch drei: x plus y gleich sieben. Also y gleich sieben minus x.',
            f(r'3x + 3y = 21 \;\Rightarrow\; x + y = 7 \;\Rightarrow\; \fc{y = 7 - x}', 330, 50, ein=1.0)),
         sz('Frage 5',
            'Zwei Seiten x und eine Seite y: Zwei x plus y gleich vierzig. Mit x gleich zwölf bleibt für y vierzig minus vierundzwanzig, also sechzehn Meter.',
            f(r'2x + y = 40', 280, 56, ein=1.0),
            f(r'y = 40 - 2 \cdot 12 = \fc{16}', 400, 56, ein=1.0)),
         merke('Zum Mitnehmen: Zähl genau, wie oft jede Seite vorkommt. Dann zuerst den x-Teil abziehen und durch die Zahl vor dem y teilen.',
               'Wie oft kommt jede Seite vor?|x-Teil weg, dann teilen|Probe mit Zahlen'),
     ], [
         wahl('Frage 1', 'Ein Rechteck hat den Umfang 30 cm. Welche Gleichung verbindet die Seiten x und y?', ['y = 15 − x', 'y = 30 − x', 'y = 30 − 2x'], 0,
              {0: 'Ja.', 1: 'Im Umfang kommt jede Seite zweimal vor.', 2: 'Nach dem Abziehen von 2x steht noch 2y da: Durch 2 teilen.'},
              sprich='Ein Rechteck hat den Umfang dreissig Zentimeter. Welche Gleichung verbindet die Seiten x und y?',
              rueck_sprich={1: 'Im Umfang kommt jede Seite zweimal vor.', 2: 'Nach dem Abziehen von zwei x steht noch zwei y da: Durch zwei teilen.'}),
         wahl('Frage 2', 'Umfang 30 cm, x = 4 cm. Wie lang ist y?', ['11 cm', '26 cm', '22 cm'], 0,
              {0: 'Ja.', 1: 'Probe: 2 · 4 + 2 · 26 ist viel mehr als 30.', 2: 'Du hast 30 − 2 · 4 gerechnet. Dann steht da noch 2y = 22.'},
              sprich='Umfang dreissig Zentimeter, x gleich vier Zentimeter. Wie lang ist y?',
              rueck_sprich={1: 'Probe: zwei mal vier plus zwei mal sechsundzwanzig ist viel mehr als dreissig.', 2: 'Du hast dreissig minus zwei mal vier gerechnet. Dann steht da noch zwei y gleich zweiundzwanzig.'}),
         wahl('Frage 3', 'Löse nach y auf: 2x + y = 10.', ['y = −2x + 10', 'y = 2x + 10', 'y = −2x + 5'], 0,
              {0: 'Ja.', 1: 'Wechselt 2x die Seite, wird daraus −2x.', 2: 'Vor dem y steht keine Zahl: Hier wird nicht geteilt.'},
              sprich='Löse nach y auf: zwei x plus y gleich zehn.',
              rueck_sprich={1: 'Wechselt zwei x die Seite, wird daraus minus zwei x.', 2: 'Vor dem y steht keine Zahl: Hier wird nicht geteilt.'}),
         wahl('Frage 4', 'Löse nach y auf: 3x + 3y = 21.', ['y = 7 − x', 'y = 21 − x', 'y = 7 − 3x'], 0,
              {0: 'Ja.', 1: 'Die 21 muss auch durch 3 geteilt werden.', 2: 'Durch 3 teilen gilt für alle Glieder, auch für 3x.'},
              sprich='Löse nach y auf: drei x plus drei y gleich einundzwanzig.',
              rueck_sprich={1: 'Die einundzwanzig muss auch durch drei geteilt werden.', 2: 'Durch drei teilen gilt für alle Glieder, auch für drei x.'}),
         wahl('Frage 5', 'Mit 40 m Zaun wird an einer Mauer ein Rechteck abgesteckt: zwei Seiten x, eine Seite y. Wie lang ist y für x = 12 m?', ['16 m', '8 m', '28 m'], 0,
              {0: 'Ja.', 1: 'Die Seite y kommt nur einmal vor, an der Mauer braucht es keinen Zaun.', 2: 'Die Seite x kommt zweimal vor.'},
              sprich='Mit vierzig Metern Zaun wird an einer Mauer ein Rechteck abgesteckt: zwei Seiten x, eine Seite y. Wie lang ist y für x gleich zwölf Meter?',
              rueck_sprich={1: 'Die Seite y kommt nur einmal vor, an der Mauer braucht es keinen Zaun.', 2: 'Die Seite x kommt zweimal vor.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung: Sinnvolle Werte, saubere Achsen
# Fehlerbild: Achse mit 0, 10, 20, 50 in gleichen Abständen; die Punkte von y = x liegen dann nicht mehr auf einer Geraden.
W_F = dict(xbereich=[-1, 7], ybereich=[-1, 5], achsen=False, raster=False)
SKALA_F = [S((0, 0), (6.2, 0), 5, 3), S((0, 0), (0, 4.2), 5, 3)] + \
          [T(-0.35, k - 0.12, str(w), 4, 'end', g=30) for k, w in enumerate([0, 10, 20, 50])] + \
          [T(k, -0.55, str(10 * k), 5, g=26) for k in range(0, 6)] + \
          [S((0, 0), (1, 1), 4, 4), S((1, 1), (2, 2), 4, 4), S((2, 2), (5, 3), 4, 4)]
clip('achsen', 5, 'Funktionen sehen: Sinnvolle Werte, saubere Achsen',
     'Treppe 2h + a = 63 → a = 63 − 2h; Definitionsbereich 15 ≤ h ≤ 20, Endpunkte (15 | 33) und (20 | 23); Achsen mit Grösse, Einheit, '
     'Einteilung 5 cm; nur die Strecke; Anzahlen als Punkte; Fehler: ungleichmässige Skala, ganze Gerade, fehlende Einheit.',
     ['Definitionsbereich', 'Achsen', 'Skala', 'Sachgraph'], [
         sz('Treppe',
            'Für bequeme Treppen gibt es eine Schrittregel: zwei mal die Stufenhöhe h plus die Auftrittsbreite a gibt dreiundsechzig Zentimeter. '
            'Nach a aufgelöst: a gleich dreiundsechzig minus zwei h.',
            f(r'2h + a = 63', 280, 60, ein='@Schrittregel'),
            f(r'a = 63 - 2h', 400, 60, ein='@aufgelöst'),
            n('h: Stufenhöhe · a: Auftrittsbreite (cm)', 540, 'blau', 40, ein='@Stufenhöhe')),
         sz('Bereich',
            'Sinnvoll sind hier Stufen von fünfzehn bis zwanzig Zentimetern. Das ist der Definitionsbereich. '
            'An seinen Enden rechnest du a aus: bei fünfzehn dreiunddreissig, bei zwanzig dreiundzwanzig Zentimeter.',
            f(r'15 \le h \le 20', 280, 60, ein='@Sinnvoll'),
            n('Definitionsbereich', 400, 'blau', 42, ein='@Definitionsbereich'),
            f(r'h = 15: \; a = 33 \qquad h = 20: \; a = 23', 520, 48, ein='@Enden')),
         sz('Achsen',
            'Jetzt die Achsen. Nach rechts die Stufenhöhe h in Zentimetern, nach oben die Auftrittsbreite a in Zentimetern. '
            'Die Werte gehen bis dreiunddreissig. Ein Häuschen für fünf Zentimeter passt gut.',
            n('Achse: Grösse und Einheit|gleichmässige Einteilung', 300, 'blau', 44, ein='@Achsen'),
            f(r'33 : 8 \approx 4.1 \;\to\; 5', 470, 50, ein='@Häuschen'),
            graf(W_T, ein='@Achsen', **TR)),
         sz('Strecke',
            'Du zeichnest nur die Strecke zwischen den beiden Endpunkten. Stufen dazwischen, etwa siebzehn Komma fünf Zentimeter, gibt es auch. '
            'Ausserhalb des Bereichs hat der Graph keinen Sinn.',
            f(r'a = 63 - 2h, \quad 15 \le h \le 20', 280, 50, ein=0.05),
            graf(W_T, punkte=[pt(15, 33, 5, '(15 | 33)', [15.8, 36], 'start'), pt(20, 23, 5, '(20 | 23)', [20.8, 26], 'start')], **TR),
            ueber(W_T, [ger(-2, 63, 5, gestrichelt=True)], ein='@Ausserhalb', **TR),
            dict(ueber(W_T, ein='@Strecke', **TR), figuren=[S((15, 33), (20, 23), 1, 5)])),
         sz('Punkte',
            'Anders bei Anzahlen. Bei der Kletterhalle gibt es nur ganze Eintritte. Dort zeichnest du einzelne Punkte.',
            n('Längen, Zeiten: Strecke|Anzahlen: einzelne Punkte', 300, 'blau', 44, ein='@Anzahlen'),
            graf(W_K, punkte=[pt(x, 6 * x + 40, 5) for x in range(11)], ein='@Kletterhalle', **KH)),
         sz('Fehler',
            'Häufiger Fehler: eine ungleichmässige Skala. Stehen null, zehn, zwanzig und fünfzig in gleichen Abständen, sieht eine Gerade geknickt aus. '
            'Und ohne Einheit an der Achse weiss niemand, was gemeint ist.',
            n('0, 10, 20, 50 in gleichen Abständen', 300, 'rot', 42, ein='@ungleichmässige'),
            n('y = x sieht geknickt aus', 420, 'rot', 42, ein='@sieht'),
            n('Einheit an jede Achse', 540, 'blau', 42, ein='@Einheit'),
            dict(graf(W_F, ein='@ungleichmässige'), figuren=SKALA_F)),
         merke('Zum Mitnehmen: Zuerst den sinnvollen Bereich aus dem Text holen und die Endpunkte rechnen. Dann Achsen mit Grösse, Einheit und '
               'gleichmässiger Einteilung. Längen und Zeiten werden eine Strecke, Anzahlen einzelne Punkte.',
               'Bereich und Endpunkte|Achsen: Grösse, Einheit, gleichmässig|Strecke oder Punkte'),
         jetzt_du(),
     ], [
         wahl('Strecke', 'Was zeichnest du für a = 63 − 2h mit 15 ≤ h ≤ 20?',
              ['die Strecke von h = 15 bis h = 20', 'die ganze Gerade', 'nur die beiden Endpunkte'], 0,
              {0: 'Ja.', 1: 'Was hiesse h = 30 cm? Ausserhalb des Bereichs hat der Graph keinen Sinn.', 2: 'Gibt es Stufen mit 17.5 cm? Dann gehören auch die Werte dazwischen dazu.'},
              sprich='Was zeichnest du für a gleich dreiundsechzig minus zwei h, mit h von fünfzehn bis zwanzig?',
              rueck_sprich={1: 'Was hiesse h gleich dreissig Zentimeter? Ausserhalb des Bereichs hat der Graph keinen Sinn.',
                            2: 'Gibt es Stufen mit siebzehn Komma fünf Zentimetern? Dann gehören auch die Werte dazwischen dazu.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
clip('kontrolle-achsen', 6, 'Funktionen sehen: Kontrollfragen zu Bereich und Achsen',
     'Fünf Fragen: Bereich einer Kerze (18 cm, 3 cm pro Stunde), Pizzas als Punkte, Einteilung für Werte bis 170 auf 9 Häuschen, '
     'Achse 0, 1, 2, 4, 8 in gleichen Abständen, Wertebereich eines Tanks (60 l, 4 l pro Minute).',
     ['Definitionsbereich', 'Skala', 'Kontrollfragen'], [
         sz('Frage 1',
            'Leer ist die Kerze bei achtzehn durch drei, also nach sechs Stunden. Der Bereich geht von null bis sechs Stunden.',
            f(r'18 - 3x = 0 \;\Rightarrow\; x = 6', 300, 54, ein=1.0),
            f(r'\fc{0 \le x \le 6}', 420, 58, ein=1.0)),
         sz('Frage 2',
            'Pizzas gibt es nur ganz. Darum einzelne Punkte.',
            n('Anzahl: einzelne Punkte', 330, 'gruen', 46, ein=1.0)),
         sz('Frage 3',
            'Hundertsiebzig durch neun gibt etwa achtzehn Komma neun. Die nächste bequeme Zahl ist zwanzig.',
            f(r'170 : 9 \approx 18.9 \;\to\; \fc{20}', 330, 56, ein=1.0)),
         sz('Frage 4',
            'Die Abstände sind gleich, aber sie stehen für eins, eins, zwei und vier. Die Skala ist nicht gleichmässig.',
            n('gleiche Abstände, verschiedene Schritte', 330, 'rot', 44, ein=1.0)),
         sz('Frage 5',
            'Am Anfang sind sechzig Liter drin, am Schluss null. Der Wertebereich geht von null bis sechzig Liter.',
            f(r'\fc{0 \le y \le 60}', 330, 58, ein=1.0)),
         merke('Zum Mitnehmen: Der Bereich endet, wo die Grösse aufhört. Anzahlen werden Punkte. Und jede Achse braucht eine gleichmässige, bequeme Einteilung.',
               'Bereich: bis die Grösse aufhört|Anzahlen: Punkte|gleichmässig und bequem einteilen'),
     ], [
         wahl('Frage 1', 'Eine Kerze ist 18 cm hoch und wird pro Stunde 3 cm kürzer. Welche Zeiten x sind sinnvoll?', ['0 bis 6 h', '0 bis 18 h', '0 bis 54 h'], 0,
              {0: 'Ja.', 1: 'Nach 18 h wäre die Kerze 18 − 54 cm hoch. Wann ist sie leer?', 2: 'Teilen, nicht multiplizieren: Wie oft passen 3 cm in 18 cm?'},
              sprich='Eine Kerze ist achtzehn Zentimeter hoch und wird pro Stunde drei Zentimeter kürzer. Welche Zeiten x sind sinnvoll?',
              rueck_sprich={1: 'Nach achtzehn Stunden wäre die Kerze achtzehn minus vierundfünfzig Zentimeter hoch. Wann ist sie leer?', 2: 'Teilen, nicht multiplizieren: Wie oft passen drei Zentimeter in achtzehn Zentimeter?'}),
         wahl('Frage 2', 'Kosten für x Pizzas: Wie sieht der Graph aus?', ['einzelne Punkte', 'eine Strecke', 'eine ganze Gerade'], 0,
              {0: 'Ja.', 1: 'Gibt es 2.5 Pizzas zu kaufen?', 2: 'Gibt es −1 Pizza? Und 2.5 Pizzas?'},
              sprich='Kosten für x Pizzas: Wie sieht der Graph aus?',
              rueck_sprich={1: 'Gibt es zwei Komma fünf Pizzas zu kaufen?', 2: 'Gibt es minus eine Pizza? Und zwei Komma fünf Pizzas?'}),
         wahl('Frage 3', 'Werte bis 170, die Achse hat 9 Häuschen. Wie viel soll ein Häuschen bedeuten?', ['20', '10', '18.9'], 0,
              {0: 'Ja.', 1: '9 Häuschen zu 10 reichen nur bis 90.', 2: 'Das reicht knapp, ist aber keine bequeme Zahl zum Ablesen.'},
              sprich='Werte bis hundertsiebzig, die Achse hat neun Häuschen. Wie viel soll ein Häuschen bedeuten?',
              rueck_sprich={1: 'Neun Häuschen zu zehn reichen nur bis neunzig.', 2: 'Das reicht knapp, ist aber keine bequeme Zahl zum Ablesen.'}),
         wahl('Frage 4', 'Eine Achse zeigt 0, 1, 2, 4, 8 in gleichen Abständen. Was stimmt?',
              ['Die Abstände stehen für verschiedene Schritte.', 'Alles in Ordnung, die Zahlen werden grösser.', 'Es fehlt nur die 3.'], 0,
              {0: 'Ja.', 1: 'Von 2 bis 4 ist ein grösserer Schritt als von 1 bis 2, im Bild aber gleich weit.', 2: 'Auch mit der 3 wären die Schritte zu 4 und 8 zu gross.'},
              sprich='Eine Achse zeigt null, eins, zwei, vier, acht in gleichen Abständen. Was stimmt?',
              rueck_sprich={1: 'Von zwei bis vier ist ein grösserer Schritt als von eins bis zwei, im Bild aber gleich weit.', 2: 'Auch mit der Drei wären die Schritte zu vier und acht zu gross.'}),
         wahl('Frage 5', 'Ein Tank mit 60 l verliert 4 l pro Minute. Welche Werte nimmt der Inhalt y an?', ['0 bis 60 l', '0 bis 15 l', '4 bis 60 l'], 0,
              {0: 'Ja.', 1: '15 sind die Minuten bis leer, nicht die Liter.', 2: 'Am Schluss ist der Tank ganz leer.'},
              sprich='Ein Tank mit sechzig Litern verliert vier Liter pro Minute. Welche Werte nimmt der Inhalt y an?',
              rueck_sprich={1: 'Fünfzehn sind die Minuten bis leer, nicht die Liter.', 2: 'Am Schluss ist der Tank ganz leer.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung: Linear fallend oder antiproportional?
clip('antiproportional', 7, 'Funktionen sehen: Linear fallend oder antiproportional?',
     'Velotour 30 km: Restweg s = 30 − 15t (linear fallend, Gerade) und Fahrzeit t = 30/v (antiproportional, Kurve); doppelt so schnell, '
     'halb so lang; doppelte Zeit heisst nicht halber Restweg; Erkennen an Differenzen und Produkten; Rechteck: Umfang gegen Fläche.',
     ['antiproportional', 'linear fallend', 'Produkt', 'Gegenbeispiel'], [
         sz('Restweg',
            'Eine Velotour ist dreissig Kilometer lang. Du fährst mit fünfzehn Kilometern pro Stunde. Der Restweg ist s gleich dreissig minus fünfzehn t. '
            'Er fällt linear: Jede Stunde fünfzehn Kilometer weniger.',
            f(r's = 30 - 15t', 280, 62, ein='@Restweg'),
            n('jede Stunde − 15 km', 420, 'blau', 44, ein='@linear'),
            graf(W_S, **SR),
            dict(ueber(W_S, ein='@Restweg', **SR), figuren=[S((0, 30), (2, 0), 1, 5)])),
         sz('Fahrzeit',
            'Andere Frage: Wie lange dauert die ganze Tour bei anderem Tempo? Bei zehn Kilometern pro Stunde drei Stunden, bei fünfzehn zwei, '
            'bei dreissig eine Stunde. Das Produkt v mal t ist immer dreissig.',
            f(r'\begin{array}{c|cccc} v & 10 & 15 & 20 & 30 \\ \hline t & 3 & 2 & 1.5 & 1 \end{array}', 260, 46, ein='@Tempo'),
            f(r'v \cdot t = 30 \qquad t = \dfrac{30}{v}', 460, 50, ein='@Produkt'),
            graf(W_V, punkte=[pt(10, 3, 5), pt(15, 2, 5), pt(20, 1.5, 5), pt(30, 1, 5)], ein='@Tempo', **VE),
            ueber(W_V, kurven=[kurve('30/x', 8.6, 33)], ein='@Produkt', **VE)),
         sz('Vorhersage',
            'Doppelt so schnell heisst halb so lang: von zehn auf zwanzig Kilometer pro Stunde, von drei auf eins Komma fünf Stunden. '
            'Das ist antiproportional.',
            f(r'v \cdot 2 \;\Rightarrow\; t : 2', 300, 60, ein='@Doppelt'),
            n('antiproportional', 430, 'blau', 46, ein='@antiproportional'),
            graf(W_V, punkte=[pt(10, 3, 5, '(10 | 3)'), pt(20, 1.5, 3, '(20 | 1.5)', [21, 2.05], 'start')], **VE),
            ueber(W_V, kurven=[kurve('30/x', 8.6, 33)], **VE)),
         sz('Vergleich',
            'Beim Restweg ist das anders. Nach einer halben Stunde sind es noch zweiundzwanzig Komma fünf Kilometer, nach einer Stunde fünfzehn. '
            'Doppelte Zeit heisst nicht halber Restweg. Linear fallend ist nicht antiproportional.',
            f(r't = 0.5: \; s = 22.5 \qquad t = 1: \; s = 15', 280, 48, ein='@halben'),
            f(r'\fd{15 \neq 22.5 : 2}', 400, 54, ein='@Doppelte'),
            n('linear fallend ≠ antiproportional', 530, 'rot', 42, ein='@Linear'),
            graf(W_S, punkte=[pt(0.5, 22.5, 5, '(0.5 | 22.5)', [0.62, 25.5], 'start'), pt(1, 15, 5, '(1 | 15)', [1.12, 18], 'start')], **SR),
            dict(ueber(W_S, **SR), figuren=[S((0, 30), (2, 0), 1, 5)])),
         sz('Erkennen',
            'So erkennst du es. Linear heisst: gleiche Differenzen, der Graph ist eine Gerade und trifft beide Achsen. '
            'Antiproportional heisst: gleiche Produkte, der Graph ist eine Kurve und trifft keine Achse.',
            n('linear: gleiche Differenzen,|Gerade, trifft die Achsen', 280, 'blau', 42, ein='@Linear'),
            n('antiproportional: gleiche Produkte,|Kurve, trifft keine Achse', 450, 'blau', 42, ein='@Antiproportional')),
         sz('Rechteck',
            'Auch beim Rechteck. Bleibt der Umfang gleich, ist es linear fallend. Bleibt die Fläche gleich, ist es antiproportional. '
            'Und Achtung: Bei gleichem Umfang ist die Fläche nicht gleich. Zwei mal zehn gibt zwanzig, sechs mal sechs gibt sechsunddreissig.',
            f(r'x + y = 12: \text{ linear fallend}', 260, 46, ein='@Umfang'),
            f(r'x \cdot y = 36: \text{ antiproportional}', 360, 46, ein='@Fläche'),
            f(r'2 \cdot 10 = 20 \neq 6 \cdot 6 = 36', 480, 46, ein='@Achtung'),
            dict(graf(W_R, ein='@Achtung', **RE), figuren=[rechteck(2, 10, 1), rechteck(6, 6, 2)])),
         merke('Zum Mitnehmen: Fällt y, wenn x wächst, prüfe Differenzen und Produkte. Gleiche Differenzen: linear fallend. Gleiche Produkte: antiproportional. '
               'Und ein Gegenbeispiel genügt, um eine falsche Aussage zu widerlegen.',
               'gleiche Differenzen: linear|gleiche Produkte: antiproportional|ein Gegenbeispiel widerlegt'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Du fährst die 30 km doppelt so schnell. Wie lange dauert die Tour?', ['halb so lang', 'eine Stunde weniger', 'gleich lang'], 0,
              {0: 'Ja.', 1: 'Prüf mit der Tabelle: Von 10 auf 20 km/h wird es 3 h zu 1.5 h.', 2: 'In der gleichen Zeit kommst du doppelt so weit.'},
              sprich='Du fährst die dreissig Kilometer doppelt so schnell. Wie lange dauert die Tour?',
              rueck_sprich={1: 'Prüf mit der Tabelle: Von zehn auf zwanzig Kilometer pro Stunde wird es drei Stunden zu eins Komma fünf Stunden.',
                            2: 'In der gleichen Zeit kommst du doppelt so weit.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
clip('kontrolle-antiproportional', 8, 'Funktionen sehen: Kontrollfragen linear oder antiproportional',
     'Fünf Fragen: Tabelle 18, 9, 6, 3 (Produkt 18), Tabelle 12, 9, 6, 3 (Differenz 3), 4 Personen 6 h → 8 Personen, x + y = 10 bei x von 2 auf 4, '
     'Gegenbeispiel zu «gleicher Umfang, gleiche Fläche» bei Umfang 16 cm.',
     ['antiproportional', 'linear fallend', 'Gegenbeispiel', 'Kontrollfragen'], [
         sz('Frage 1',
            'Eins mal achtzehn, zwei mal neun, drei mal sechs, sechs mal drei: Das Produkt ist immer achtzehn. Antiproportional.',
            f(r'\begin{array}{c|cccc} x & 1 & 2 & 3 & 6 \\ \hline y & 18 & 9 & 6 & 3 \end{array}', 260, 46, ein=0.05),
            f(r'x \cdot y = \fc{18}', 440, 56, ein=1.0)),
         sz('Frage 2',
            'Bei jedem Schritt wird y um drei kleiner: gleiche Differenzen. Linear fallend.',
            f(r'\begin{array}{c|cccc} x & 0 & 1 & 2 & 3 \\ \hline y & 12 & 9 & 6 & 3 \end{array}', 260, 46, ein=0.05),
            f(r'\fc{-3, \; -3, \; -3}', 440, 56, ein=1.0)),
         sz('Frage 3',
            'Doppelt so viele Personen brauchen halb so lange: drei Stunden. Vier mal sechs gibt vierundzwanzig, acht mal drei auch.',
            f(r'4 \cdot 6 = 24 = 8 \cdot \fc{3}', 330, 56, ein=1.0)),
         sz('Frage 4',
            'y gleich zehn minus x. Bei x gleich zwei ist y acht, bei x gleich vier ist y sechs. Nicht halbiert.',
            f(r'x = 2: \; y = 8 \qquad x = 4: \; y = \fc{6}', 330, 50, ein=1.0)),
         sz('Frage 5',
            'Zwei mal sechs und vier mal vier haben beide den Umfang sechzehn, aber die Flächen zwölf und sechzehn. Das widerlegt die Aussage.',
            f(r'2 \cdot 6 = 12 \neq 4 \cdot 4 = 16', 330, 50, ein=1.0),
            dict(graf(W_R, **RE), figuren=[rechteck(2, 6, 1), rechteck(4, 4, 2)])),
         merke('Zum Mitnehmen: Differenzen gleich, dann linear. Produkte gleich, dann antiproportional. Für ein Gegenbeispiel brauchst du zwei wirklich verschiedene Fälle.',
               'Differenzen gleich: linear|Produkte gleich: antiproportional|Gegenbeispiel: zwei verschiedene Fälle'),
     ], [
         wahl('Frage 1', 'Tabelle: x: 1, 2, 3, 6 und y: 18, 9, 6, 3. Welcher Zusammenhang?', ['antiproportional', 'linear fallend', 'proportional'], 0,
              {0: 'Ja.', 1: 'Die Differenzen sind −9, −3, −3 bei verschiedenen Schritten: Rechne die Produkte x · y.', 2: 'Proportional hiesse: y wächst mit x.'},
              sprich='Tabelle: x eins, zwei, drei, sechs und y achtzehn, neun, sechs, drei. Welcher Zusammenhang?',
              rueck_sprich={1: 'Rechne die Produkte x mal y.', 2: 'Proportional hiesse: y wächst mit x.'}),
         wahl('Frage 2', 'Tabelle: x: 0, 1, 2, 3 und y: 12, 9, 6, 3. Welcher Zusammenhang?', ['linear fallend', 'antiproportional', 'proportional'], 0,
              {0: 'Ja.', 1: 'Bei x = 0 wäre das Produkt 0, bei x = 1 aber 9.', 2: 'Proportional hiesse: y wächst mit x.'},
              sprich='Tabelle: x null, eins, zwei, drei und y zwölf, neun, sechs, drei. Welcher Zusammenhang?',
              rueck_sprich={1: 'Bei x gleich null wäre das Produkt null, bei x gleich eins aber neun.', 2: 'Proportional hiesse: y wächst mit x.'}),
         wahl('Frage 3', '4 Personen streichen einen Zaun in 6 h. Wie lange brauchen 8 gleich schnelle Personen?', ['3 h', '12 h', '2 h'], 0,
              {0: 'Ja.', 1: 'Mehr Personen arbeiten schneller, nicht langsamer.', 2: 'Prüf das Produkt: 4 · 6 und 8 · 2.'},
              sprich='Vier Personen streichen einen Zaun in sechs Stunden. Wie lange brauchen acht gleich schnelle Personen?',
              rueck_sprich={1: 'Mehr Personen arbeiten schneller, nicht langsamer.', 2: 'Prüf das Produkt: vier mal sechs und acht mal zwei.'}),
         wahl('Frage 4', 'x + y = 10. Bei x = 2 ist y = 8. Wie gross ist y bei x = 4?', ['6', '4', '12'], 0,
              {0: 'Ja.', 1: 'Halbieren gilt bei gleichem Produkt. Hier bleibt die Summe gleich.', 2: 'Prüf die Summe: 4 + 12 ist nicht 10.'},
              sprich='x plus y gleich zehn. Bei x gleich zwei ist y gleich acht. Wie gross ist y bei x gleich vier?',
              rueck_sprich={1: 'Halbieren gilt bei gleichem Produkt. Hier bleibt die Summe gleich.', 2: 'Prüf die Summe: vier plus zwölf ist nicht zehn.'}),
         wahl('Frage 5', 'Welches Paar widerlegt «Rechtecke mit dem Umfang 16 cm sind gleich gross»?',
              ['2 × 6 und 4 × 4', '2 × 6 und 6 × 2', '3 × 5 und 5 × 3'], 0,
              {0: 'Ja.', 1: 'Das ist dasselbe Rechteck, nur gedreht.', 2: 'Das ist dasselbe Rechteck, nur gedreht.'},
              sprich='Welches Paar widerlegt: Rechtecke mit dem Umfang sechzehn Zentimeter sind gleich gross?',
              rueck_sprich={1: 'Das ist dasselbe Rechteck, nur gedreht.', 2: 'Das ist dasselbe Rechteck, nur gedreht.'}),
     ], art='Kontrollclip')

if FEHLT:
    print('ohne gemessene Wortzeit (geschätzt):', len(FEHLT), FEHLT)
