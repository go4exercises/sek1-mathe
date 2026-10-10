"""Erzeugt die acht Drehbücher des Leitprogramms «Lineare Funktionen» (10.10.2026).

  python3 scripts/lp/lineare-funktionen/clips.py

Zeitlogik aus scripts/lp/gleichungen-formeln/clips.py: Je Kapitel ein Einführungsclip (mit einer Vorhersagefrage)
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
  5 Tinte  = neutral: gegebener Punkt, Steigungsdreieck
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
PRAEFIX = 'lin-lp-'
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
         'schlagworte': schlag, 'themenbereich': 'Funktionen · Lineare Funktionen',
         'fach': 'Sekundarstufe I', 'lerngebiet': '3 · Funktionen',
         'lektion': ['lp-linear'], 'stufe': ['Sek I'], 'datum': '2026-10-10',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Funktionen sehen', 'folge': folge,
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms lineare-funktionen; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + dname + '.json', 'w'), ensure_ascii=False, indent=1)
    print(dname, len(szenen), 'Szenen', len(fragen or []), 'Fragen')


def teil(*werte):
    return [[v, str(v).replace('-', '−')] for v in werte]


# ---------------------------------------------------------------- Fenster
W_TANK = dict(xbereich=[-1, 11], ybereich=[-30, 430], xteilung=teil(0, 2, 4, 6, 8, 10), yteilung=teil(0, 100, 200, 300, 400))
TANK = dict(xname='x [min]', yname='y [l]')
W_ST = dict(xbereich=[-2, 8], ybereich=[-1, 9])        # 10 / 10: y = 2x, P(1 | 2), Q(4 | 8) nicht am Rand
W_MB = dict(xbereich=[-4, 5], ybereich=[-4, 5])        # 9 / 9
W_Z = dict(xbereich=[-2, 7], ybereich=[-3, 6])         # 9 / 9: y = 2/3 x − 1, (6 | 3), (1.5 | 0)
W_GL = dict(xbereich=[-1, 8], ybereich=[-1, 8])        # 9 / 9: y = −1/2 x + 3; P(2 | 5), Q(6 | 7)
W_INF = dict(xbereich=[-30, 490], ybereich=[-40, 560], xteilung=teil(0, 100, 200, 300, 400), yteilung=teil(0, 100, 200, 300, 400, 500))
INF = dict(xname='t [min]', yname='V [ml]')

# ════════════════════════════════════════════════ Kapitel 1 · Einführung: Anfangswert und Änderung
TAB = r'\begin{array}{c|cccc} x & 0 & 1 & 2 & 3 \\ \hline y & 200 & 215 & 230 & 245 \end{array}'
clip('anfangswert', 1, 'Funktionen sehen: Anfangswert und Änderung',
     'Tank mit 200 l, pro Minute 15 l dazu: Wertetabelle, Punkte auf einer Geraden, y = 15x + 200; b = Anfangswert, '
     'm = Änderung pro Minute; abnehmend: y = −20x + 200; rückwärts: 350 l nach 10 Minuten; Fehler m und b vertauscht.',
     ['lineare Funktion', 'Anfangswert', 'Änderung', 'Wertetabelle', 'Gerade'], [
         sz('Tank',
            'Ein Wassertank enthält am Anfang zweihundert Liter. Pro Minute fliessen fünfzehn Liter dazu. '
            'Wie viel Wasser ist nach x Minuten im Tank?',
            n('am Anfang: @200 l@', 300, 'orange', 50, ein='@Anfang'),
            n('pro Minute: @+ 15 l@', 420, 'blau', 50, ein='@Minute'),
            graf(W_TANK, **TANK),
            ueber(W_TANK, punkte=[pt(0, 200, 2, '(0 | 200)')], ein='@Anfang', **TANK)),
         sz('Tabelle',
            'Nach einer Minute sind es zweihundertfünfzehn Liter. Nach zwei Minuten zweihundertdreissig. '
            'Nach drei Minuten zweihundertfünfundvierzig. Bei jedem Schritt kommt gleich viel dazu: fünfzehn Liter. '
            'Darum liegen die Punkte auf einer Geraden.',
            f(TAB, 300, 50, ein=0.3),
            graf(W_TANK, punkte=[pt(0, 200, 2)], **TANK),
            ueber(W_TANK, punkte=[pt(1, 215, 5)], ein='@Nach#1', **TANK),
            ueber(W_TANK, punkte=[pt(2, 230, 5)], ein='@Nach#2', **TANK),
            ueber(W_TANK, punkte=[pt(3, 245, 5)], ein='@Nach#3', **TANK),
            n('+ 15 bei jedem Schritt', 520, 'blau', 44, ein='@Schritt'),
            ueber(W_TANK, [ger(15, 200, 1, gestrichelt=True)], ein='@Geraden', **TANK)),
         sz('Vorhersage',
            'Nach vier Minuten kommen vier mal fünfzehn Liter dazu, also sechzig. Im Tank sind dann zweihundertsechzig Liter.',
            f(TAB, 300, 50, ein=0.05),
            f(r'200 + 4 \cdot \fa{15} = \fc{260}', 520, 56, ein='@vier#2'),
            graf(W_TANK, punkte=[pt(0, 200, 2), pt(1, 215, 5), pt(2, 230, 5), pt(3, 245, 5)], **TANK),
            ueber(W_TANK, punkte=[pt(4, 260, 3, '(4 | 260)')], ein='@Tank', **TANK)),
         sz('Gleichung',
            'Nach x Minuten kommen x mal fünfzehn Liter dazu. Also y gleich fünfzehn x plus zweihundert. '
            'Die zweihundert ist der Anfangswert b: der Wert bei x gleich null. Die fünfzehn ist die Änderung pro Minute: m.',
            f(r'y = \fa{15} \cdot x + \fb{200}', 300, 66, ein='@Also'),
            n('@b = 200@: Anfangswert, bei x = 0', 450, 'orange', 42, ein='@Anfangswert'),
            n('@m = 15@: Änderung pro Minute', 540, 'blau', 42, ein='@Änderung'),
            graf(W_TANK, **TANK),
            ueber(W_TANK, [bew([[0, 15, 200]], yachse={'farbe': 2, 'beschriftung': False})], ein='@Also', **TANK)),
         sz('Allgemein',
            'Allgemein schreibst du y gleich m mal x plus b. Ihr Graph ist eine Gerade, darum heisst sie lineare Funktion. '
            'Nimmt der Wert ab, ist m negativ. Ein Tank mit zweihundert Litern, aus dem pro Minute zwanzig Liter abfliessen: '
            'y gleich minus zwanzig x plus zweihundert.',
            f(r'y = \fa{m} \cdot x + \fb{b}', 280, 72, ein='@Allgemein'),
            n('lineare Funktion: Graph ist eine Gerade', 420, 'blau', 42, ein='@lineare'),
            f(r'y = \fa{-20} \cdot x + \fb{200}', 560, 60, ein='@minus'),
            graf(W_TANK, [ger(15, 200)], **TANK),
            ueber(W_TANK, [ger(-20, 200, 1)], ein='@abfliessen', **TANK)),
         sz('Rückwärts',
            'Umgekehrt: Wann sind dreihundertfünfzig Liter im Tank? Setz y gleich dreihundertfünfzig und löse die Gleichung. '
            'Fünfzehn x ist hundertfünfzig, also x gleich zehn. Nach zehn Minuten.',
            f(r'15x + 200 = 350', 280, 58, ein='@Setz'),
            f(r'15x = 150', 400, 58, ein='@Fünfzehn'),
            f(r'\fc{x = 10}', 520, 62, ein='@zehn'),
            graf(W_TANK, [ger(15, 200)], **TANK),
            ueber(W_TANK, [ger(0, 350, 5, gestrichelt=True)], ein='@Wann', **TANK),
            ueber(W_TANK, punkte=[pt(10, 350, 3, '(10 | 350)', [9.6, 390], 'end')], ein='@zehn', **TANK)),
         sz('Fehler',
            'Häufiger Fehler: m und b vertauscht. y gleich zweihundert x plus fünfzehn startet mit fünfzehn Litern. '
            'Prüf mit x gleich null: Am Anfang müssen zweihundert Liter drin sein. Mit x gleich eins merkst du nichts, '
            'denn beide Gleichungen geben dort zweihundertfünfzehn.',
            f(r'\fd{y = 200x + 15}', 280, 62, ein='@vertauscht'),
            f(r'x = 0: \quad \fd{15} \neq 200', 420, 54, ein='@Prüf'),
            f(r'x = 1: \quad 215 = 215', 540, 54, ein='@nichts'),
            n('Probe mit x = 0, nicht mit x = 1', 680, 'rot', 42, ein='@beide')),
         merke('Zum Mitnehmen: y gleich m mal x plus b. b ist der Anfangswert bei x gleich null, m die Änderung pro Schritt. '
               'Nimmt der Wert ab, ist m negativ. Und die Probe machst du mit x gleich null.',
               'y = m · x + b|b: Anfangswert (bei x = 0)|m: Änderung pro Schritt, abnehmend negativ|Probe mit x = 0'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Wie viel Wasser ist nach 4 Minuten im Tank?', ['260 l', '215 l', '800 l'], 0,
              {0: 'Ja.', 1: 'So viel ist es nach 1 Minute. Bis 4 Minuten kommen viermal 15 l dazu.',
               2: 'Die 200 l sind nur einmal da, am Anfang. Vervielfacht wird, was pro Minute dazukommt.'},
              sprich='Wie viel Wasser ist nach vier Minuten im Tank?',
              rueck_sprich={1: 'So viel ist es nach einer Minute. Bis vier Minuten kommen viermal fünfzehn Liter dazu.',
                            2: 'Die zweihundert Liter sind nur einmal da, am Anfang. Vervielfacht wird, was pro Minute dazukommt.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
W_K1 = dict(xbereich=[-1, 11], ybereich=[-10, 150], xteilung=teil(0, 2, 4, 6, 8, 10), yteilung=teil(0, 40, 80, 120))
W_KERZE = dict(xbereich=[-1, 14], ybereich=[-2, 28], xteilung=teil(0, 4, 8, 12), yteilung=teil(0, 8, 16, 24))
clip('kontrolle-anfangswert', 2, 'Funktionen sehen: Kontrollfragen zu Anfangswert und Änderung',
     'Fünf Fragen: Tank 80 l + 5 l/min als Gleichung, y = −3x + 20 für x = 4, y = 6x + 9 rückwärts für y = 45, '
     'Gleichung aus der Tabelle 2, 5, 8, 11, Kerze 24 cm − 2 cm pro Stunde.',
     ['Anfangswert', 'Änderung', 'lineare Funktion', 'Kontrollfragen'], [
         sz('Frage 1',
            'Am Anfang achtzig, das ist b. Pro Minute fünf dazu, das ist m. Also y gleich fünf x plus achtzig.',
            f(r'y = \fa{5}x + \fb{80}', 330, 62, ein=1.0),
            graf(W_K1, [bew([[0, 5, 80]], yachse={'farbe': 2, 'beschriftung': False})], xname='x [min]', yname='y [l]')),
         sz('Frage 2',
            'Setz vier ein: minus drei mal vier ist minus zwölf, plus zwanzig gibt acht.',
            f(r'-3 \cdot 4 + 20 = -12 + 20 = \fc{8}', 330, 56, ein=1.0)),
         sz('Frage 3',
            'Hier ist y gegeben. Sechs x plus neun gleich fünfundvierzig. Minus neun: sechs x gleich sechsunddreissig, also x gleich sechs.',
            f(r'6x + 9 = 45', 280, 56, ein=1.0),
            f(r'6x = 36 \qquad \fc{x = 6}', 400, 56, ein=1.0)),
         sz('Frage 4',
            'Bei x gleich null steht zwei: b ist zwei. Bei jedem Schritt kommt drei dazu: m ist drei. Also y gleich drei x plus zwei.',
            f(r'\begin{array}{c|cccc} x & 0 & 1 & 2 & 3 \\ \hline y & 2 & 5 & 8 & 11 \end{array}', 280, 50, ein=0.05),
            f(r'\fc{y = 3x + 2}', 470, 62, ein=1.0)),
         sz('Frage 5',
            'Die Kerze startet mit vierundzwanzig Zentimetern, das ist b. Sie wird pro Stunde zwei Zentimeter kürzer, '
            'also ist m minus zwei: y gleich minus zwei x plus vierundzwanzig.',
            f(r'\fc{y = -2x + 24}', 330, 62, ein=1.0),
            graf(W_KERZE, [bew([[0, -2, 24]], yachse={'farbe': 2, 'beschriftung': False})], xname='x [h]', yname='y [cm]')),
         merke('Zum Mitnehmen: b ist der Wert am Anfang, bei x gleich null. m ist die Änderung pro Schritt, beim Abnehmen negativ. '
               'Ist y gegeben, löst du eine Gleichung.',
               'b: Wert bei x = 0|m: Änderung pro Schritt|y gegeben: Gleichung lösen'),
     ], [
         wahl('Frage 1', 'Ein Tank enthält am Anfang 80 l, pro Minute kommen 5 l dazu. Welche Gleichung passt?',
              ['y = 5x + 80', 'y = 80x + 5', 'y = 5x − 80'], 0,
              {0: 'Ja.', 1: 'Prüf mit x = 0: Am Anfang müssen 80 l drin sein.', 2: 'Am Anfang sind 80 l drin, nicht −80 l.'},
              sprich='Ein Tank enthält am Anfang achtzig Liter, pro Minute kommen fünf Liter dazu. Welche Gleichung passt?',
              rueck_sprich={1: 'Prüf mit x gleich null: Am Anfang müssen achtzig Liter drin sein.',
                            2: 'Am Anfang sind achtzig Liter drin, nicht minus achtzig.'}),
         wahl('Frage 2', 'y = −3x + 20. Wie gross ist y für x = 4?', ['8', '32', '17'], 0,
              {0: 'Ja.', 1: 'Achte auf das Minus: −3 · 4 = −12.', 2: 'Du hast x vergessen: −3 wird mit 4 multipliziert.'},
              sprich='y gleich minus drei x plus zwanzig. Wie gross ist y für x gleich vier?',
              rueck_sprich={1: 'Achte auf das Minus: minus drei mal vier ist minus zwölf.',
                            2: 'Du hast x vergessen: Minus drei wird mit vier multipliziert.'}),
         wahl('Frage 3', 'y = 6x + 9. Für welches x ist y = 45?', ['x = 6', 'x = 279', 'x = 7.5'], 0,
              {0: 'Ja.', 1: 'Du hast 45 für x eingesetzt. Gegeben ist hier y.', 2: 'Zuerst die 9 abziehen, dann durch 6 teilen.'},
              sprich='y gleich sechs x plus neun. Für welches x ist y gleich fünfundvierzig?',
              rueck_sprich={1: 'Du hast fünfundvierzig für x eingesetzt. Gegeben ist hier y.',
                            2: 'Zuerst die Neun abziehen, dann durch sechs teilen.'}),
         wahl('Frage 4', 'Welche Gleichung passt zur Tabelle?', ['y = 3x + 2', 'y = 2x + 3', 'y = 3x + 5'], 0,
              {0: 'Ja.', 1: 'Prüf mit x = 0: Die Tabelle zeigt dort 2.', 2: 'b ist der Wert bei x = 0, nicht bei x = 1.'},
              rueck_sprich={1: 'Prüf mit x gleich null: Die Tabelle zeigt dort zwei.',
                            2: 'b ist der Wert bei x gleich null, nicht bei x gleich eins.'}),
         wahl('Frage 5', 'Eine Kerze ist 24 cm hoch und brennt pro Stunde 2 cm ab. Welche Gleichung passt?',
              ['y = −2x + 24', 'y = 2x + 24', 'y = 24x − 2'], 0,
              {0: 'Ja.', 1: 'So würde die Kerze wachsen. Sie wird kürzer: m ist negativ.',
               2: 'Prüf mit x = 0: Am Anfang ist die Kerze 24 cm hoch.'},
              sprich='Eine Kerze ist vierundzwanzig Zentimeter hoch und brennt pro Stunde zwei Zentimeter ab. Welche Gleichung passt?',
              rueck_sprich={1: 'So würde die Kerze wachsen. Sie wird kürzer: m ist negativ.',
                            2: 'Prüf mit x gleich null: Am Anfang ist die Kerze vierundzwanzig Zentimeter hoch.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung: Die Steigung
clip('steigung', 3, 'Funktionen sehen: Die Steigung',
     'Steigung m = hinauf pro Schritt nach rechts; Steigungsdreieck auf y = 2x zwischen P(1 | 2) und Q(4 | 8): 6/3 = 2; '
     'kleineres Dreieck gibt dasselbe m; aus Koordinaten (8 − 2)/(4 − 1); Vorzeichen, waagrecht, steiler; Fehler Δx/Δy.',
     ['Steigung', 'Steigungsdreieck', 'Gerade', 'Delta'], [
         sz('Steil',
            'Diese zwei Geraden steigen beide, aber verschieden steil. Wie steil, sagt die Steigung m: um wie viel y zunimmt, '
            'wenn x um eins zunimmt.',
            graf(W_ST, [ger(2, 0), ger(0.5, 1, 5)]),
            n('Steigung m:|so viel hinauf|pro 1 nach rechts', 300, 'blau', 46, ein='@Steigung')),
         sz('Dreieck',
            'Geh auf der Geraden von P nach Q: zuerst nach rechts, dann hinauf. Das ist ein Steigungsdreieck. '
            'Drei nach rechts, sechs hinauf. Pro Schritt nach rechts also zwei hinauf: Die Steigung ist sechs durch drei, gleich zwei.',
            graf(W_ST, [bew([[0, 2, 0]], dreieck=dreieck(1, 3, ein='@Steigungsdreieck'))],
                 [pt(1, 2, 5, 'P(1 | 2)', [0.7, 2.4], 'end'), pt(4, 8, 5, 'Q(4 | 8)', [3.7, 8.4], 'end')]),
            f(r'm = \dfrac{\Delta y}{\Delta x} = \dfrac{6}{3} = \fa{2}', 320, 62, ein='@Steigung#2')),
         sz('Gleich',
            'Nimm ein kleineres Dreieck auf derselben Geraden: eins nach rechts, zwei hinauf. Wieder zwei. '
            'Jedes Steigungsdreieck einer Geraden gibt dieselbe Steigung.',
            graf(W_ST, [bew([[0, 2, 0]], dreieck=dreieck(None, None, [[0, 1, 3], ['@kleineres', 1, 3], ['@zwei', 2, 1]]))]),
            f(r'\dfrac{2}{1} = \dfrac{6}{3} = \fa{2}', 320, 62, ein='@hinauf+0.3'),
            n('jedes Steigungsdreieck:|dieselbe Steigung', 520, 'blau', 44, ein='@Jedes')),
         sz('Rechnen',
            'Ohne Bild rechnest du mit den Koordinaten. Für Δy rechnest du acht minus zwei, für Δx vier minus eins. '
            'Oben und unten nimmst du zuerst denselben Punkt, hier Q.',
            f(r'P(1 \mid 2), \quad Q(4 \mid 8)', 260, 54, ein=0.3),
            f(r'm = \dfrac{\fb{8} - 2}{\fb{4} - 1} = \dfrac{6}{3} = \fa{2}', 380, 60, ein='@Für+0.2'),
            n('oben und unten zuerst Q', 600, 'blau', 44, ein='@Oben'),
            graf(W_ST, [ger(2, 0)], [pt(1, 2, 5, 'P(1 | 2)'), pt(4, 8, 2, 'Q(4 | 8)')])),
         sz('Vorzeichen',
            'Fällt die Gerade, geht es hinunter: Δy ist negativ, also auch m. Bei m gleich null ist die Gerade waagrecht. '
            'Und je grösser der Betrag von m, desto steiler ist sie.',
            graf(W_MB, [bew([[0, 2, 1], ['@Fällt', 2, 1], ['@negativ', -1, 1], ['@Bei', -1, 1], ['@waagrecht', 0, 1],
                             ['@grösser', 0, 1], ['@steiler', 3, 1]], dreieck=dreieck(0, 1))]),
            f(r'm \lt 0: \text{ fällt}', 280, 54, ein='@negativ'),
            f(r'm = 0: \text{ waagrecht}', 390, 54, ein='@waagrecht'),
            n('grösserer Betrag: steiler', 520, 'blau', 44, ein='@steiler')),
         sz('Fehler',
            'Häufiger Fehler: den Bruch umgedreht. Δx durch Δy, also drei durch sechs, ist nicht die Steigung. '
            'Oben steht immer die Änderung in y.',
            f(r'\fd{\dfrac{\Delta x}{\Delta y} = \dfrac{3}{6}}', 300, 62, ein='@umgedreht'),
            f(r'm = \dfrac{\Delta y}{\Delta x} = \dfrac{6}{3} = \fc{2}', 540, 60, ein='@Oben')),
         merke('Zum Mitnehmen: Die Steigung m ist Δy durch Δx, hinauf geteilt durch nach rechts. Jedes Steigungsdreieck gibt '
               'dasselbe m. Positiv steigt, negativ fällt, null ist waagrecht.',
               'm = Δy / Δx|jedes Dreieck: dasselbe m|positiv steigt, negativ fällt, null waagrecht'),
         jetzt_du(),
     ], [
         wahl('Dreieck', 'Wie gross ist die Steigung der Geraden durch P und Q?', ['2', '1/2', '6'], 0,
              {0: 'Ja.', 1: 'Das ist «nach rechts» durch «hinauf». Gefragt ist, wie viel es pro Schritt nach rechts hinaufgeht.',
               2: 'So viel geht es von P nach Q hinauf, aber auf 3 Schritte nach rechts. Wie viel pro Schritt?'},
              sprich='Wie gross ist die Steigung der Geraden durch P und Q?',
              rueck_sprich={1: 'Das ist nach rechts durch hinauf. Gefragt ist, wie viel es pro Schritt nach rechts hinaufgeht.',
                            2: 'So viel geht es von P nach Q hinauf, aber auf drei Schritte nach rechts. Wie viel pro Schritt?'}),
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
W_K2A = dict(xbereich=[-1, 8], ybereich=[-1, 8])
W_K2C = dict(xbereich=[-2, 7], ybereich=[-2, 7])
FRAGEBILD.update({
    ('kontrolle-steigung', 'Frage 1'): (W_K2A, [], [pt(2, 1, 5, 'A(2 | 1)', [1.8, 1.4], 'end'), pt(5, 7, 5, 'B(5 | 7)')], {}),
    ('kontrolle-steigung', 'Frage 2'): (W_MB, [], [pt(-1, 3, 5, 'P(−1 | 3)', [-1.3, 3.4], 'end'), pt(1, -1, 5, 'Q(1 | −1)')], {}),
    ('kontrolle-steigung', 'Frage 3'): (W_K2C, [ger(-1 / 3, 2)], [pt(0, 2, 5), pt(3, 1, 5)], {}),
})
clip('kontrolle-steigung', 4, 'Funktionen sehen: Kontrollfragen zur Steigung',
     'Fünf Fragen: m durch (2 | 1) und (5 | 7), m durch (−1 | 3) und (1 | −1), m einer fallenden Geraden im Bild (−1/3), '
     'Bedeutung von m = 0, m bei 2 nach rechts und 3 hinunter.',
     ['Steigung', 'Steigungsdreieck', 'Kontrollfragen'], [
         sz('Frage 1',
            'Δy ist sieben minus eins, also sechs. Δx ist fünf minus zwei, also drei. Sechs durch drei gibt zwei.',
            f(r'm = \dfrac{7 - 1}{5 - 2} = \dfrac{6}{3} = \fc{2}', 330, 60, ein=1.0),
            graf(W_K2A, [bew([[0, 2, -3]], dreieck=dreieck(2, 3))], [pt(2, 1, 5), pt(5, 7, 5)])),
         sz('Frage 2',
            'Von P nach Q: Δy ist minus eins minus drei, also minus vier. Δx ist eins minus minus eins, also zwei. '
            'Minus vier durch zwei gibt minus zwei. Die Gerade fällt.',
            f(r'm = \dfrac{-1 - 3}{1 - (-1)} = \dfrac{-4}{2} = \fc{-2}', 330, 58, ein=1.0),
            graf(W_MB, [bew([[0, -2, 1]], dreieck=dreieck(-1, 2))], [pt(-1, 3, 5), pt(1, -1, 5)])),
         sz('Frage 3',
            'Von einem Gitterpunkt zum nächsten: drei nach rechts, eins hinunter. Die Steigung ist minus eins durch drei.',
            f(r'm = \dfrac{-1}{3} = \fc{-\tfrac{1}{3}}', 330, 60, ein=1.0),
            graf(W_K2C, [bew([[0, -1 / 3, 2]], dreieck=dreieck(0, 3))])),
         sz('Frage 4',
            'Bei m gleich null ändert sich y nicht, wenn du nach rechts gehst. Die Gerade ist waagrecht.',
            f(r'm = 0: \quad \Delta y = 0', 330, 58, ein=1.0),
            graf(W_MB, [ger(0, 2), ger(0, -1)])),
         sz('Frage 5',
            'Hinunter heisst Δy negativ: minus drei. Nach rechts zwei. Die Steigung ist minus drei durch zwei, minus eins Komma fünf.',
            f(r'm = \dfrac{-3}{2} = \fc{-1.5}', 330, 60, ein=1.0),
            graf(W_MB, [bew([[0, -1.5, 3]], dreieck=dreieck(0, 2))])),
         merke('Zum Mitnehmen: m ist Δy durch Δx. Oben und unten zuerst denselben Punkt. Hinunter ist negativ, und bei m gleich null '
               'ist die Gerade waagrecht.',
               'm = Δy / Δx|oben und unten dieselbe Reihenfolge|hinunter: negativ · m = 0: waagrecht'),
     ], [
         wahl('Frage 1', 'Wie gross ist die Steigung der Geraden durch A(2 | 1) und B(5 | 7)?', ['2', '1/2', '−2'], 0,
              {0: 'Ja.', 1: 'Oben steht die Änderung in y, unten die in x.', 2: 'Von A nach B geht es hinauf. Ist m dann negativ?'},
              sprich='Wie gross ist die Steigung der Geraden durch A mit zwei und eins und B mit fünf und sieben?',
              rueck_sprich={1: 'Oben steht die Änderung in y, unten die in x.', 2: 'Von A nach B geht es hinauf. Ist m dann negativ?'}),
         wahl('Frage 2', 'Wie gross ist die Steigung der Geraden durch P(−1 | 3) und Q(1 | −1)?', ['−2', '2', '−1/2'], 0,
              {0: 'Ja.', 1: 'Der Betrag stimmt. Aber geht es von P nach Q hinauf oder hinunter?',
               2: 'Oben steht Δy, unten Δx. Vertauscht?'},
              sprich='Wie gross ist die Steigung der Geraden durch P mit minus eins und drei und Q mit eins und minus eins?',
              rueck_sprich={1: 'Der Betrag stimmt. Aber geht es von P nach Q hinauf oder hinunter?',
                            2: 'Oben steht delta y, unten delta x. Vertauscht?'}),
         wahl('Frage 3', 'Wie gross ist die Steigung der Geraden im Bild?', ['−1/3', '−3', '1/3'], 0,
              {0: 'Ja.', 1: 'Zähl noch einmal: Was kommt in den Nenner, «nach rechts» oder «hinunter»?',
               2: 'Der Betrag stimmt. Steigt die Gerade, oder fällt sie?'},
              rueck_sprich={1: 'Zähl noch einmal: Was kommt in den Nenner, nach rechts oder hinunter?',
                            2: 'Der Betrag stimmt. Steigt die Gerade, oder fällt sie?'}),
         wahl('Frage 4', 'Eine Gerade hat die Steigung m = 0. Wie verläuft sie?', ['waagrecht', 'senkrecht', 'durch (0 | 0)'], 0,
              {0: 'Ja.', 1: 'Bei m = 0 ist Δy = 0: y ändert sich nicht. Ist das senkrecht?',
               2: 'Ob eine Gerade durch (0 | 0) geht, sagt b, nicht m.'},
              sprich='Eine Gerade hat die Steigung m gleich null. Wie verläuft sie?',
              rueck_sprich={1: 'Bei m gleich null ist delta y gleich null: y ändert sich nicht. Ist das senkrecht?',
                            2: 'Ob eine Gerade durch den Ursprung geht, sagt b, nicht m.'}),
         wahl('Frage 5', 'Eine Gerade geht pro 2 nach rechts 3 hinunter. Wie gross ist m?', ['−1.5', '−2/3', '1.5'], 0,
              {0: 'Ja.', 1: 'Oben steht die Änderung in y: −3. Unten steht 2.', 2: 'Hinunter heisst: Δy ist negativ.'},
              sprich='Eine Gerade geht pro zwei nach rechts drei hinunter. Wie gross ist m?',
              rueck_sprich={1: 'Oben steht die Änderung in y: minus drei. Unten steht zwei.', 2: 'Hinunter heisst: delta y ist negativ.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung: Geraden zeichnen
DREI_Z = [S((0, -1), (3, -1), 5, 4), S((3, -1), (3, 1), 5, 4), T(1.5, -1.75, '3 nach rechts', 5, g=28), T(3.25, -0.65, '2 hinauf', 5, 'start', g=28)]
clip('zeichnen', 5, 'Funktionen sehen: Geraden zeichnen',
     'y = 2/3 x − 1 zeichnen: Start (0 | −1) auf der y-Achse, Steigungsdreieck 3 nach rechts, 2 hinauf, Punkt (3 | 1), '
     'verbinden; Punktprobe (6 | 3); Nullstelle x = 1.5; Fehler: Dreieck im Ursprung, bei negativem m hinauf.',
     ['Gerade zeichnen', 'Steigungsdreieck', 'Punktprobe', 'Nullstelle'], [
         sz('Start',
            'Zeichne y gleich zwei Drittel x minus eins. Starte auf der y-Achse bei b. Hier ist b minus eins: der Punkt null, minus eins.',
            f(r'y = \fa{\tfrac{2}{3}}x \fb{- 1}', 300, 66, ein='@Zeichne'),
            graf(W_Z),
            ueber(W_Z, punkte=[pt(0, -1, 2, '(0 | −1)', [-0.25, -1.75], 'end')], ein='@Punkt')),
         sz('Dreieck',
            'Die Steigung zwei Drittel heisst: drei nach rechts, zwei hinauf. So kommst du zum Punkt drei, eins.',
            f(r'y = \fa{\tfrac{2}{3}}x \fb{- 1}', 300, 66, ein=0.05),
            f(r'\fa{\tfrac{2}{3}} = \dfrac{2 \text{ hinauf}}{3 \text{ nach rechts}}', 440, 54, ein='@Steigung'),
            graf(W_Z, punkte=[pt(0, -1, 2, '(0 | −1)', [-0.25, -1.75], 'end')]),
            dict(graf(W_Z, achsen=False, raster=False, ein='@drei'), figuren=DREI_Z),
            ueber(W_Z, punkte=[pt(3, 1, 1, '(3 | 1)')], ein='@Punkt')),
         sz('Verbinden',
            'Verbinde die beiden Punkte und verlängere die Linie über beide hinaus. Das ist die Gerade.',
            f(r'y = \fa{\tfrac{2}{3}}x \fb{- 1}', 300, 66, ein=0.05),
            graf(W_Z, punkte=[pt(0, -1, 2), pt(3, 1, 1)]),
            ueber(W_Z, [ger(2 / 3, -1)], ein='@Verbinde')),
         sz('Probe',
            'Liegt der Punkt sechs, drei auf der Geraden? Setz x gleich sechs ein: zwei Drittel mal sechs ist vier, minus eins gibt drei. '
            'Ja, er liegt darauf.',
            f(r'P(6 \mid 3)', 280, 56, ein='@Liegt'),
            f(r'\tfrac{2}{3} \cdot 6 - 1 = 4 - 1 = \fc{3}', 400, 56, ein='@Setz'),
            graf(W_Z, [ger(2 / 3, -1)]),
            ueber(W_Z, punkte=[pt(6, 3, 3, 'P(6 | 3)', [5.8, 3.5], 'end')], ein='@Liegt')),
         sz('Nullstelle',
            'Wo schneidet die Gerade die x-Achse? Dort ist y gleich null. Zwei Drittel x minus eins gleich null, '
            'also zwei Drittel x gleich eins und x gleich eins Komma fünf. Das ist die Nullstelle.',
            f(r'\tfrac{2}{3}x - 1 = 0', 280, 56, ein='@null'),
            f(r'\tfrac{2}{3}x = 1 \qquad \fc{x = 1.5}', 400, 56, ein='@also'),
            graf(W_Z, [ger(2 / 3, -1)]),
            ueber(W_Z, punkte=[pt(1.5, 0, 3, '(1.5 | 0)', [1.8, -0.7], 'start')], ein='@Nullstelle')),
         sz('Fehler',
            'Häufiger Fehler: Das Dreieck im Ursprung begonnen. Dann entsteht y gleich zwei Drittel x, eine verschobene Gerade. '
            'Und bei negativem m geht es hinunter, nicht hinauf.',
            f(r'\fd{y = \tfrac{2}{3}x}', 280, 62, ein='@Ursprung'),
            n('Start bei (0 ∣ b), nicht bei (0 ∣ 0)', 420, 'rot', 42, ein='@verschobene'),
            n('m negativ: hinunter', 540, 'rot', 42, ein='@negativem'),
            graf(W_Z, [ger(2 / 3, -1)]),
            ueber(W_Z, [ger(2 / 3, 0, 4, gestrichelt=True)], ein='@Ursprung')),
         merke('Zum Mitnehmen: Start bei b auf der y-Achse. Dann das Steigungsdreieck: nach rechts, und hinauf oder hinunter. '
               'Zwei Punkte verbinden. Die Punktprobe zeigt, ob ein Punkt darauf liegt.',
               'Start: (0 ∣ b)|Steigungsdreieck: nach rechts, hinauf oder hinunter|verbinden und verlängern|Punktprobe: einsetzen'),
         jetzt_du(),
     ], [
         wahl('Dreieck', 'Von (0 | −1) aus mit der Steigung 2/3: Zu welchem Punkt kommst du?', ['(3 | 1)', '(2 | 2)', '(3 | 2)'], 0,
              {0: 'Ja.', 1: 'Du bist 2 nach rechts und 3 hinauf gegangen. Unten im Bruch steht der Schritt nach rechts.',
               2: '3 nach rechts und 2 hinauf stimmt, aber von (0 | −1) aus, nicht von (0 | 0).'},
              sprich='Von null, minus eins aus mit der Steigung zwei Drittel: Zu welchem Punkt kommst du?',
              rueck_sprich={1: 'Du bist zwei nach rechts und drei hinauf gegangen. Unten im Bruch steht der Schritt nach rechts.',
                            2: 'Drei nach rechts und zwei hinauf stimmt, aber von null, minus eins aus, nicht vom Ursprung.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
W_K3A = dict(xbereich=[-1, 8], ybereich=[-1, 8])
W_K3B = dict(xbereich=[-2, 7], ybereich=[-2, 7])
W_K3N = dict(xbereich=[-5, 6], ybereich=[-9, 2], yteilung=teil(-8, -4, 0))
W_K3E = dict(xbereich=[-3, 6], ybereich=[-3, 6])
# Frage 4: drei Geraden, Namen gerechnet: A y = x + 2, B y = x − 2, C y = −x − 2; Name bei x = 2.5 neben der Geraden
DREI_G = [ger(1, 2, 5), ger(1, -2, 5), ger(-1, -2, 5)]
NAMEN_G = [T(1.9, 4.8, 'A', 5, g=40), T(3.9, 0.8, 'B', 5, g=40), T(-1.6, -1.0, 'C', 5, g=40)]
FRAGEBILD.update({
    ('kontrolle-zeichnen', 'Frage 2'): (W_K3B, [], [pt(2, 5, 5, 'P(2 | 5)')], {}),
    ('kontrolle-zeichnen', 'Frage 4'): (W_MB, DREI_G, [], {'figuren': NAMEN_G}),
})
clip('kontrolle-zeichnen', 6, 'Funktionen sehen: Kontrollfragen zum Zeichnen',
     'Fünf Fragen: zweiter Punkt von y = 3/4 x + 1, Punktprobe P(2 | 5) auf y = 3x − 1, Nullstelle von y = 2x − 8 tippen, '
     'welche von drei Geraden y = x − 2 ist, zweiter Punkt bei m = −2 und b = 3.',
     ['Gerade zeichnen', 'Punktprobe', 'Nullstelle', 'Kontrollfragen'], [
         sz('Frage 1',
            'Start bei null, eins. Drei Viertel heisst vier nach rechts und drei hinauf: Du kommst zu vier, vier.',
            f(r'(0 \mid 1) \;\to\; \fc{(4 \mid 4)}', 330, 58, ein=1.0),
            graf(W_K3A, [bew([[0, 0.75, 1]], dreieck=dreieck(0, 4))], [pt(0, 1, 2), pt(4, 4, 3)])),
         sz('Frage 2',
            'Setz zwei ein: drei mal zwei minus eins gibt fünf. Das ist die y-Koordinate von P. P liegt auf der Geraden.',
            f(r'3 \cdot 2 - 1 = \fc{5}', 330, 60, ein=1.0),
            graf(W_K3B, [ger(3, -1)], [pt(2, 5, 3)])),
         sz('Frage 3',
            'Setz y gleich null: zwei x minus acht gleich null, also x gleich vier. Die Nullstelle ist vier, null.',
            f(r'2x - 8 = 0 \qquad \fc{x = 4}', 330, 58, ein=1.0),
            graf(W_K3N, [ger(2, -8)], [pt(4, 0, 3, '(4 | 0)')])),
         sz('Frage 4',
            'y gleich x minus zwei startet bei minus zwei und steigt: eins nach rechts, eins hinauf. Das ist die Gerade B.',
            f(r'\fc{B}: \; y = x - 2', 330, 58, ein=1.0),
            dict(graf(W_MB, [ger(1, 2, 5), ger(1, -2, 3), ger(-1, -2, 5)]), figuren=NAMEN_G)),
         sz('Frage 5',
            'Start bei null, drei. m gleich minus zwei heisst eins nach rechts und zwei hinunter: Du kommst zu eins, eins.',
            f(r'(0 \mid 3) \;\to\; \fc{(1 \mid 1)}', 330, 58, ein=1.0),
            graf(W_K3E, [bew([[0, -2, 3]], dreieck=dreieck(0, 1))], [pt(0, 3, 2), pt(1, 1, 3)])),
         merke('Zum Mitnehmen: Start bei b, dann nach rechts und hinauf oder hinunter. Die Punktprobe ist Einsetzen. '
               'Für die Nullstelle setzt du y gleich null.',
               'Start bei (0 ∣ b)|Punktprobe: einsetzen|Nullstelle: y = 0 setzen'),
     ], [
         wahl('Frage 1', 'y = ¾x + 1: Start bei (0 | 1). Zu welchem Punkt führt das Steigungsdreieck?', ['(4 | 4)', '(3 | 5)', '(4 | 3)'], 0,
              {0: 'Ja.', 1: 'Du bist 3 nach rechts und 4 hinauf gegangen. Unten im Bruch steht der Schritt nach rechts.',
               2: '4 nach rechts und 3 hinauf stimmt, aber von (0 | 1) aus.'},
              sprich='y gleich drei Viertel x plus eins. Start bei null, eins. Zu welchem Punkt führt das Steigungsdreieck?',
              rueck_sprich={1: 'Du bist drei nach rechts und vier hinauf gegangen. Unten im Bruch steht der Schritt nach rechts.',
                            2: 'Vier nach rechts und drei hinauf stimmt, aber von null, eins aus.'}),
         wahl('Frage 2', 'Liegt P(2 | 5) auf der Geraden y = 3x − 1?', ['Ja', 'Nein', 'Das sieht man erst im Bild.'], 0,
              {0: 'Ja.', 1: 'Setz x = 2 ein und vergleich mit der y-Koordinate von P.',
               2: 'Ohne Bild geht es genauer: Setz x = 2 ein.'},
              sprich='Liegt P mit zwei und fünf auf der Geraden y gleich drei x minus eins?',
              rueck_sprich={1: 'Setz x gleich zwei ein und vergleich mit der y-Koordinate von P.',
                            2: 'Ohne Bild geht es genauer: Setz x gleich zwei ein.'}),
         klick('Frage 3', 'y = 2x − 8: Tipp die Nullstelle ins Bild.', [4, 0], 'Getroffen: (4 | 0).',
               [{'bei': [0, -8], 'text': 'Das ist der Punkt auf der y-Achse. Die Nullstelle liegt auf der x-Achse.',
                 'sprich': 'Das ist der Punkt auf der y-Achse. Die Nullstelle liegt auf der x-Achse.'},
                {'bei': [-4, 0], 'text': 'Achte auf das Vorzeichen: 2x − 8 = 0 gibt 2x = 8.',
                 'sprich': 'Achte auf das Vorzeichen: zwei x minus acht gleich null gibt zwei x gleich acht.'},
                {'bei': [2, 0], 'text': 'Das ist die Steigung. Setz y = 0 und löse nach x auf.',
                 'sprich': 'Das ist die Steigung. Setz y gleich null und löse nach x auf.'}],
               'Nicht ganz. Setz y = 0 und löse nach x auf.',
               sprich='y gleich zwei x minus acht: Tipp die Nullstelle ins Bild.',
               falsch_sprich='Nicht ganz. Setz y gleich null und löse nach x auf.'),
         wahl('Frage 4', 'Welche Gerade im Bild ist y = x − 2?', ['B', 'A', 'C'], 0,
              {0: 'Ja.', 1: 'A schneidet die y-Achse bei +2. Gesucht ist b = −2.',
               2: 'C startet bei −2, fällt aber. Bei m = 1 steigt die Gerade.'},
              sprich='Welche Gerade im Bild ist y gleich x minus zwei?',
              rueck_sprich={1: 'A schneidet die y-Achse bei plus zwei. Gesucht ist b gleich minus zwei.',
                            2: 'C startet bei minus zwei, fällt aber. Bei m gleich eins steigt die Gerade.'}),
         wahl('Frage 5', 'y = −2x + 3: Start bei (0 | 3). Zu welchem Punkt führt das Steigungsdreieck?', ['(1 | 1)', '(1 | 5)', '(2 | 2)'], 0,
              {0: 'Ja.', 1: 'm ist negativ: Es geht hinunter, nicht hinauf.', 2: 'm = −2 heisst 1 nach rechts und 2 hinunter.'},
              sprich='y gleich minus zwei x plus drei. Start bei null, drei. Zu welchem Punkt führt das Steigungsdreieck?',
              rueck_sprich={1: 'm ist negativ: Es geht hinunter, nicht hinauf.', 2: 'm gleich minus zwei heisst eins nach rechts und zwei hinunter.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung: Die Gleichung finden
INF1 = [S((0, 500), (250, 0), 1, 5)]
INF2 = [S((0, 500), (100, 300), 1, 5), S((100, 300), (400, 0), 1, 5)]
clip('gleichung', 7, 'Funktionen sehen: Die Gleichung finden',
     'Aus dem Graphen: b = 3 ablesen, Steigungsdreieck 2 nach rechts, 1 hinunter, y = −1/2 x + 3; aus zwei Punkten '
     'P(2 | 5), Q(6 | 7): m = 1/2, b = 4; Infusion 500 ml, 2 ml/min, leer nach 250 min; Wechsel nach 100 min auf 1 ml/min: '
     'Knick bei (100 | 300), leer nach 400 min; Fehler b mit y-Wert verwechselt.',
     ['Geradengleichung', 'zwei Punkte', 'Sachverhalt', 'Infusion'], [
         sz('Ablesen',
            'Welche Gleichung gehört zu dieser Geraden? Lies zuerst b ab. Die Gerade schneidet die y-Achse bei drei: b ist drei.',
            graf(W_GL, [ger(-0.5, 3)]),
            ueber(W_GL, punkte=[pt(0, 3, 2, '(0 | 3)', [0.3, 3.5], 'start')], ein='@schneidet'),
            f(r'b = \fb{3}', 300, 62, ein='@ist')),
         sz('Steigung',
            'Dann das Steigungsdreieck von null, drei aus: zwei nach rechts und eins hinunter. m ist minus eins durch zwei. '
            'Die Gleichung heisst y gleich minus eins durch zwei x plus drei.',
            graf(W_GL, [bew([[0, -0.5, 3]], dreieck=dreieck(0, 2, ein='@Steigungsdreieck'))], [pt(0, 3, 2)]),
            f(r'b = \fb{3}', 260, 56, ein=0.05),
            f(r'm = \dfrac{-1}{2} = \fa{-\tfrac{1}{2}}', 370, 56, ein='@m'),
            f(r'y = \fa{-\tfrac{1}{2}}x + \fb{3}', 560, 62, ein='@Gleichung')),
         sz('Zweipunkte',
            'Ohne Bild, nur zwei Punkte: P mit zwei und fünf, Q mit sechs und sieben. Zuerst m: sieben minus fünf durch sechs minus zwei, '
            'das gibt eins durch zwei. Dann setzt du P ein: fünf gleich eins durch zwei mal zwei plus b, also b gleich vier. '
            'Probe mit Q: drei plus vier gibt sieben.',
            f(r'P(2 \mid 5), \quad Q(6 \mid 7)', 230, 50, ein='@Punkte'),
            f(r'm = \dfrac{7 - 5}{6 - 2} = \fa{\tfrac{1}{2}}', 330, 50, ein='@Zuerst'),
            f(r'5 = \tfrac{1}{2} \cdot 2 + b \quad \Rightarrow \quad \fb{b = 4}', 490, 50, ein='@setzt'),
            f(r'y = \tfrac{1}{2}x + 4: \quad \tfrac{1}{2} \cdot 6 + 4 = \fc{7}', 610, 50, ein='@Probe'),
            graf(W_GL, punkte=[pt(2, 5, 5, 'P(2 | 5)'), pt(6, 7, 5, 'Q(6 | 7)')], mit_geraden=[(0.5, 4)]),
            ueber(W_GL, [ger(0.5, 4)], ein='@Probe')),
         sz('Infusion',
            'Eine Infusion enthält fünfhundert Milliliter und läuft mit zwei Millilitern pro Minute. Der Inhalt nach t Minuten: '
            'V gleich minus zwei t plus fünfhundert. Leer ist sie bei V gleich null, nach zweihundertfünfzig Minuten.',
            n('am Anfang: @500 ml@|pro Minute: @− 2 ml@', 240, 'blau', 42, ein='@enthält'),
            f(r'V = \fa{-2}t + \fb{500}', 420, 60, ein='@Inhalt'),
            f(r'-2t + 500 = 0 \qquad \fc{t = 250}', 540, 52, ein='@Leer'),
            graf(W_INF, **INF),
            dict(ueber(W_INF, ein='@Inhalt', **INF), figuren=INF1),
            ueber(W_INF, punkte=[pt(250, 0, 3, '(250 | 0)')], ein='@Minuten#2', **INF)),
         sz('Wechsel',
            'Nach hundert Minuten wird auf einen Milliliter pro Minute gestellt. Jetzt sind noch dreihundert Milliliter drin. '
            'Von dort läuft der Graph flacher weiter: Er knickt, er springt nicht. Leer ist die Infusion nach vierhundert Minuten.',
            f(r'500 - 2 \cdot 100 = \fb{300}', 260, 52, ein='@Jetzt'),
            f(r'300 : 1 = 300 \qquad 100 + 300 = \fc{400}', 380, 50, ein='@Leer'),
            n('Knick, kein Sprung', 520, 'blau', 44, ein='@knickt'),
            graf(W_INF, **INF),
            dict(ueber(W_INF, ein=0.05, **INF), figuren=[S((0, 500), (250, 0), 5, 3, gest=True)]),
            dict(ueber(W_INF, ein='@Jetzt', **INF), figuren=[S((0, 500), (100, 300), 1, 5)]),
            ueber(W_INF, punkte=[pt(100, 300, 2, '(100 | 300)', [118, 345], 'start')], ein='@Jetzt', **INF),
            dict(ueber(W_INF, ein='@flacher', **INF), figuren=[S((100, 300), (400, 0), 1, 5)]),
            ueber(W_INF, punkte=[pt(400, 0, 3, '(400 | 0)', [395, 45], 'start')], ein='@Infusion', **INF)),
         sz('Fehler',
            'Häufiger Fehler: b mit einem y-Wert verwechselt. Bei P mit zwei und fünf ist b nicht fünf. '
            'b ist der Wert bei x gleich null.',
            f(r'P(2 \mid 5): \quad \fd{b \neq 5}', 300, 58, ein='@verwechselt'),
            n('b = Wert bei x = 0', 440, 'blau', 44, ein='@Wert')),
         merke('Zum Mitnehmen: Aus dem Graphen liest du b ab und misst m mit einem Steigungsdreieck. Aus zwei Punkten berechnest du '
               'zuerst m und setzt dann einen Punkt ein. Ändert sich die Rate, knickt der Graph und springt nicht.',
               'Graph: b ablesen, m messen|zwei Punkte: zuerst m, dann einsetzen|neue Rate: Knick, kein Sprung'),
         jetzt_du(),
     ], [
         wahl('Steigung', 'b = 3. Wie gross ist die Steigung m dieser Geraden?', ['−1/2', '−2', '1/2'], 0,
              {0: 'Ja.', 1: 'Zähl nach: Was kommt in den Nenner, «nach rechts» oder «hinunter»?',
               2: 'Der Betrag stimmt. Steigt die Gerade, oder fällt sie?'},
              sprich='b ist drei. Wie gross ist die Steigung m dieser Geraden?',
              rueck_sprich={1: 'Zähl nach: Was kommt in den Nenner, nach rechts oder hinunter?',
                            2: 'Der Betrag stimmt. Steigt die Gerade, oder fällt sie?'}),
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
W_K4A = dict(xbereich=[-2, 7], ybereich=[-2, 7])
W_K4B = dict(xbereich=[-3, 6], ybereich=[-1, 11], yteilung=teil(0, 5, 10))
W_K4I = dict(xbereich=[-10, 110], ybereich=[-30, 450], xteilung=teil(0, 20, 40, 60, 80, 100), yteilung=teil(0, 100, 200, 300, 400))
W_K4W = dict(xbereich=[-20, 220], ybereich=[-25, 340], xteilung=teil(0, 50, 100, 150, 200), yteilung=teil(0, 100, 200, 300))
W_K4V = dict(xbereich=[-20, 220], ybereich=[-40, 680], xteilung=teil(0, 50, 100, 150, 200), yteilung=teil(0, 200, 400, 600))
FRAGEBILD.update({
    ('kontrolle-gleichung', 'Frage 1'): (W_K4A, [ger(2, 1)], [pt(0, 1, 5), pt(2, 5, 5)], {}),
})
clip('kontrolle-gleichung', 8, 'Funktionen sehen: Kontrollfragen zur Gleichung',
     'Fünf Fragen: Gleichung der Geraden durch (0 | 1) und (2 | 5) im Bild, Gerade durch (1 | 4) und (3 | 10), '
     'Infusion 400 ml mit 5 ml/min leer, Ratenwechsel nach 50 min bei 300 ml und 3 ml/min, Gleichung für 600 ml und 3 ml/min.',
     ['Geradengleichung', 'zwei Punkte', 'Infusion', 'Kontrollfragen'], [
         sz('Frage 1',
            'Die Gerade schneidet die y-Achse bei eins: b ist eins. Zwei nach rechts, vier hinauf: m ist zwei. y gleich zwei x plus eins.',
            f(r'\fc{y = 2x + 1}', 330, 62, ein=1.0),
            graf(W_K4A, [bew([[0, 2, 1]], dreieck=dreieck(0, 2), yachse={'farbe': 2, 'beschriftung': False})])),
         sz('Frage 2',
            'Zuerst m: zehn minus vier durch drei minus eins, das gibt drei. Dann einen Punkt einsetzen: vier gleich drei plus b, '
            'also b gleich eins.',
            f(r'm = \dfrac{10 - 4}{3 - 1} = 3', 280, 54, ein=1.0),
            f(r'4 = 3 \cdot 1 + b \qquad \fc{y = 3x + 1}', 440, 52, ein=1.0),
            graf(W_K4B, [ger(3, 1)], [pt(1, 4, 5, '(1 | 4)'), pt(3, 10, 5, '(3 | 10)')])),
         sz('Frage 3',
            'V gleich minus fünf t plus vierhundert. Leer bei null: vierhundert durch fünf gibt achtzig Minuten.',
            f(r'-5t + 400 = 0 \qquad \fc{t = 80}', 330, 54, ein=1.0),
            dict(graf(W_K4I, punkte=[pt(80, 0, 3, '(80 | 0)')], **INF), figuren=[S((0, 400), (80, 0), 1, 5)])),
         sz('Frage 4',
            'Nach fünfzig Minuten sind hundertfünfzig Milliliter weg. Es bleiben hundertfünfzig. Dort beginnt das neue Stück, '
            'bei fünfzig, hundertfünfzig.',
            f(r'300 - 3 \cdot 50 = \fc{150}', 330, 56, ein=1.0),
            dict(graf(W_K4W, punkte=[pt(50, 150, 3, '(50 | 150)', [62, 178], 'start')], **INF),
                 figuren=[S((0, 300), (50, 150), 1, 5), S((50, 150), (200, 0), 1, 5)])),
         sz('Frage 5',
            'Am Anfang sechshundert, das ist b. Pro Minute drei weniger, also m gleich minus drei: V gleich minus drei t plus sechshundert.',
            f(r'\fc{V = -3t + 600}', 330, 62, ein=1.0),
            dict(graf(W_K4V, **INF), figuren=[S((0, 600), (200, 0), 1, 5)])),
         merke('Zum Mitnehmen: b liest du bei x gleich null ab, m misst du mit dem Steigungsdreieck. Aus zwei Punkten zuerst m, '
               'dann einsetzen. Bei einer neuen Rate geht es dort weiter, wo der Graph gerade ist.',
               'b bei x = 0, m mit dem Dreieck|zwei Punkte: zuerst m, dann einsetzen|neue Rate: weiter, wo der Graph ist'),
     ], [
         wahl('Frage 1', 'Welche Gleichung hat die Gerade im Bild?', ['y = 2x + 1', 'y = ½x + 1', 'y = 2x + 5'], 0,
              {0: 'Ja.', 1: 'Oben steht, wie viel es hinaufgeht, unten der Schritt nach rechts.',
               2: 'b ist der Wert bei x = 0, nicht ein anderer y-Wert.'},
              rueck_sprich={1: 'Oben steht, wie viel es hinaufgeht, unten der Schritt nach rechts.',
                            2: 'b ist der Wert bei x gleich null, nicht ein anderer y-Wert.'}),
         wahl('Frage 2', 'Welche Gerade geht durch (1 | 4) und (3 | 10)?', ['y = 3x + 1', 'y = 3x + 4', 'y = 2x + 2'], 0,
              {0: 'Ja.', 1: 'm stimmt. Prüf mit (1 | 4): 3 · 1 + 4 ist nicht 4.', 2: 'Prüf mit (3 | 10): 2 · 3 + 2 ist nicht 10.'},
              sprich='Welche Gerade geht durch eins, vier und drei, zehn?',
              rueck_sprich={1: 'm stimmt. Prüf mit eins, vier: drei mal eins plus vier ist nicht vier.',
                            2: 'Prüf mit drei, zehn: zwei mal drei plus zwei ist nicht zehn.'}),
         wahl('Frage 3', 'Eine Infusion mit 400 ml läuft mit 5 ml pro Minute. Wann ist sie leer?', ['nach 80 min', 'nach 2000 min', 'nach 395 min'], 0,
              {0: 'Ja.', 1: 'Gesucht ist, wie oft 5 ml in 400 ml passen.', 2: 'Pro Minute laufen 5 ml, nicht insgesamt.'},
              sprich='Eine Infusion mit vierhundert Millilitern läuft mit fünf Millilitern pro Minute. Wann ist sie leer?',
              rueck_sprich={1: 'Gesucht ist, wie oft fünf Milliliter in vierhundert Milliliter passen.',
                            2: 'Pro Minute laufen fünf Milliliter, nicht insgesamt.'}),
         wahl('Frage 4', 'Infusion mit 300 ml, 3 ml pro Minute. Nach 50 min wird auf 1 ml pro Minute gestellt. Wo beginnt das neue Stück des Graphen?',
              ['(50 | 150)', '(50 | 300)', '(0 | 150)'], 0,
              {0: 'Ja.', 1: 'Beim Umstellen beginnt die Infusion nicht neu. Wie viel ist nach 50 min noch drin?',
               2: 'Umgestellt wird nach 50 min, nicht am Anfang.'},
              sprich='Infusion mit dreihundert Millilitern, drei Milliliter pro Minute. Nach fünfzig Minuten wird auf einen Milliliter pro Minute gestellt. Wo beginnt das neue Stück des Graphen?',
              rueck_sprich={1: 'Beim Umstellen beginnt die Infusion nicht neu. Wie viel ist nach fünfzig Minuten noch drin?',
                            2: 'Umgestellt wird nach fünfzig Minuten, nicht am Anfang.'}),
         wahl('Frage 5', 'Ein Beutel mit 600 ml läuft mit 3 ml pro Minute. Welche Gleichung passt?', ['V = −3t + 600', 'V = 3t + 600', 'V = −600t + 3'], 0,
              {0: 'Ja.', 1: 'Der Beutel wird leerer: m ist negativ.', 2: 'Prüf mit t = 0: Am Anfang sind 600 ml drin.'},
              sprich='Ein Beutel mit sechshundert Millilitern läuft mit drei Millilitern pro Minute. Welche Gleichung passt?',
              rueck_sprich={1: 'Der Beutel wird leerer: m ist negativ.', 2: 'Prüf mit t gleich null: Am Anfang sind sechshundert Milliliter drin.'}),
     ], art='Kontrollclip')

if FEHLT:
    print('ohne gemessene Wortzeit (geschätzt):', len(FEHLT), FEHLT)
