"""Erzeugt die acht Drehbücher des Leitprogramms «Texte, Geschwindigkeit und Begegnung» (10.10.2026).

  python3 scripts/lp/bewegung/clips.py

Gerüst und Zeitlogik aus scripts/lp/funktionstypen/clips.py: Je Kapitel ein Einführungsclip (mit einer Vorhersagefrage)
und ein Kontrollclip (fünf Fragen mit neuen Zahlen). Gemessene `dauer` werden beim Neulauf gerettet; Einblendungen
stehen als «@wort» auf dem Wort, das sie nennen (wortzeiten.json, faster-whisper medium). Zahlwörter hört Whisper als
Ziffern: Anker darum auf Wörtern ohne Zahl.

Bild rechts (x 1010, y 175, 760 × 760), Rechnung links (x 150). Graphen hier nur als Strecken (`figuren`), nie als
ganze Geraden: Zeit und Anzahl sind nicht negativ.

Fragebild (HOWTO-leitprogramme §15): In den Kontrollclips zeigt das Bild beim Erscheinen einer Frage nur das Gegebene
(FRAGEBILD unten); die Auflösung erscheint ab 1.0 s, nach der Antwort.

Farben — gleich wie auf der Seite:
  1 blau   = A, erster Abschnitt                      \\fa{…}
  2 orange = B, zweiter Abschnitt                     \\fb{…}
  3 grün   = Treffer, Ergebnis, Probe                 \\fc{…}
  4 rot    = Fehler                                   \\fd{…}
  5 Tinte  = neutral, Durchschnitt (gestrichelt)
Gesprochen: Dezimalzahlen als «null Komma fünf», Geld als «Franken» und «Rappen», nie «ein Halb» (HOWTO §15).
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
PRAEFIX = 'bew-lp-'
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
         'schlagworte': schlag, 'themenbereich': 'Mathematisieren · Texte, Geschwindigkeit und Begegnung',
         'fach': 'Sekundarstufe I', 'lerngebiet': '4 · Mathematisieren',
         'lektion': ['lp-bewegung'], 'stufe': ['Sek I'], 'datum': '2026-10-10',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Mathematisieren', 'folge': folge,
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms bewegung; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
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
W_T = dict(xbereich=[-2.2, 21], ybereich=[-0.8, 14], xteilung=teil(5, 10, 15, 20), yteilung=teil(3, 6, 9, 12))
TZ = dict(xname='x [Zahlungen]', yname='Kosten [Fr.]')
W_Z = dict(xbereich=[-0.4, 3.3], ybereich=[-20, 380], xteilung=teil(1, 2, 3), yteilung=teil(120, 240, 360))
ZZ = dict(xname='t [h]', yname='s [km]')
W_V = dict(xbereich=[-0.5, 4.6], ybereich=[-3, 58], xteilung=teil(1, 2, 3, 4), yteilung=teil(10, 20, 30, 40, 50))
W_B = dict(xbereich=[-0.3, 2.65], ybereich=[-2, 42], xteilung=[[0.5, '0.5'], [1, '1'], [1.5, '1.5'], [2, '2']], yteilung=teil(12, 24, 36))
BZ = dict(xname='t [h]', yname='Ort [km]')
TOUR = [(0, 0), (1.5, 30), (2, 30), (4, 50)]


def tarif(a, b, farbe):
    return S((0, a), (20, a + 20 * b), farbe, 5)


# ════════════════════════════════════════════════ Kapitel 1 · Einführung: Vom Text zur Gleichung
clip('text', 1, 'Mathematisieren: Vom Text zur Gleichung',
     'Konto A 4 Fr. + 0.50 Fr. pro Zahlung, Konto B 7 Fr. + 0.20 Fr.: Hilfekarte Skizze → Variable → Beziehung → Gleichung → Prüfung; '
     'gleich teuer bei 10, Vorhersage «ab wann B günstiger», Probe mit 11, Antwortsatz; Fehler: Gleichstand als Antwort, Runden.',
     ['Textaufgabe', 'Gleichung', 'Variable', 'Antwortsatz', 'Probe'], [
         sz('Text',
            'Konto A kostet vier Franken im Monat und fünfzig Rappen pro Zahlung. Konto B kostet sieben Franken und zwanzig Rappen pro Zahlung. '
            'Ab wie vielen Zahlungen ist Konto B günstiger?',
            n('A: 4 Fr. + 0.50 Fr. pro Zahlung|B: 7 Fr. + 0.20 Fr. pro Zahlung', 300, 'blau', 44, ein='@Konto'),
            n('Ab wie vielen Zahlungen|ist B günstiger?', 470, 'orange', 44, ein='@günstiger')),
         sz('Plan',
            'So gehst du vor: zuerst eine Skizze oder Tabelle. Dann eine Variable mit Bedeutung, dann die Beziehung, dann die Gleichung. '
            'Am Schluss prüfst du und schreibst einen Antwortsatz.',
            n('① Skizze oder Tabelle|② Variable mit Einheit|③ Beziehung|④ Gleichung lösen|⑤ Prüfung und Antwortsatz', 260, 'blau', 46, ein='@Skizze')),
         sz('Variable',
            'x ist die Anzahl Zahlungen im Monat. Konto A kostet vier plus null Komma fünf x Franken, Konto B sieben plus null Komma zwei x.',
            f(r'x:\ \text{Anzahl Zahlungen}', 280, 50, ein='@Anzahl'),
            f(r'\fa{A = 4 + 0.5x}', 400, 54, ein='@kostet'),
            f(r'\fb{B = 7 + 0.2x}', 500, 54, ein='@sieben'),
            graf(W_T, **TZ),
            dict(ueber(W_T, ein='@kostet', **TZ), figuren=[tarif(4, 0.5, 1)]),
            dict(ueber(W_T, ein='@sieben', **TZ), figuren=[tarif(7, 0.2, 2)])),
         sz('Gleichung',
            'Gleich teuer heisst: beide Terme gleich. Null Komma drei x gleich drei, also x gleich zehn. Bei zehn Zahlungen kosten beide neun Franken.',
            f(r'4 + 0.5x = 7 + 0.2x', 280, 54, ein='@Gleich'),
            f(r'0.3x = 3 \;\Rightarrow\; x = \fc{10}', 390, 54, ein='@Terme+0.6'),
            dict(graf(W_T, **TZ), figuren=[tarif(4, 0.5, 1), tarif(7, 0.2, 2)]),
            ueber(W_T, punkte=[pt(10, 9, 3, '(10 | 9)')], ein='@kosten', **TZ)),
         sz('Vorhersage',
            'Zehn ist der Gleichstand. Die Probe mit elf zeigt: A kostet neun Franken fünfzig, B neun Franken zwanzig. Ab elf Zahlungen ist B günstiger.',
            f(r'x = 11:\ \ \fa{9.50} \text{ Fr.} \;>\; \fb{9.20} \text{ Fr.}', 300, 50, ein='@Probe'),
            n('Ab 11 Zahlungen ist B günstiger.', 430, 'gruen', 44, ein='@günstiger'),
            dict(graf(W_T, punkte=[pt(10, 9, 3, '(10 | 9)')], **TZ), figuren=[tarif(4, 0.5, 1), tarif(7, 0.2, 2)])),
         sz('Fehler',
            'Häufiger Fehler: x gleich zehn hinschreiben und fertig. Die Frage war, ab wann B günstiger ist. Und wo nur Ganzes geht, rundest du passend: '
            'Für zweiundsechzig Personen in Bussen mit zwölf Plätzen reichen fünf Busse nicht, es braucht sechs.',
            n('«x = 10» beantwortet die Frage nicht', 300, 'rot', 44, ein='@hinschreiben'),
            f(r'62 : 12 \approx 5.2 \;\Rightarrow\; 6\ \text{Busse}', 420, 50, ein='@Personen')),
         merke('Zum Mitnehmen: Gib der Variablen eine Bedeutung, stell die Gleichung auf und löse sie. Dann prüfst du, ob die Zahl die Frage beantwortet, und schreibst einen Antwortsatz.',
               'Variable mit Bedeutung · Gleichung|Probe: beantwortet es die Frage?|Antwortsatz mit Einheit'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Bei 10 Zahlungen kosten beide 9 Fr. Ab wie vielen Zahlungen ist B günstiger?', ['ab 11 Zahlungen', 'ab 10 Zahlungen', 'ab 9 Zahlungen'], 0,
              {0: 'Ja.', 1: 'Bei 10 sind beide gleich teuer. Günstiger heisst: weniger.', 2: 'Bei 9 Zahlungen: A 8.50 Fr., B 8.80 Fr. Welches ist billiger?'},
              sprich='Bei zehn Zahlungen kosten beide neun Franken. Ab wie vielen Zahlungen ist B günstiger?',
              rueck_sprich={1: 'Bei zehn sind beide gleich teuer. Günstiger heisst: weniger.', 2: 'Bei neun Zahlungen kostet A acht Franken fünfzig, B acht Franken achtzig. Welches ist billiger?'}),
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
clip('kontrolle-text', 2, 'Mathematisieren: Kontrollfragen zu Textaufgaben',
     'Fünf Fragen: Taxi 4 Fr. + 2 Fr./km für 30 Fr., Gleichstand 5 + 2x = 11 + x, drei Zahlen mit Summe 45, Antwortsatz, 46 Personen in Autos zu 8 Plätzen.',
     ['Textaufgabe', 'Gleichung', 'Kontrollfragen'], [
         sz('Frage 1',
            'Vier plus zwei x gleich dreissig. Zwei x gleich sechsundzwanzig, x gleich dreizehn Kilometer.',
            f(r'4 + 2x = 30 \;\Rightarrow\; x = \fc{13}', 330, 56, ein=1.0)),
         sz('Frage 2',
            'Fünf plus zwei x gleich elf plus x. Also x gleich sechs: Bei sechs Stück sind beide gleich teuer.',
            f(r'5 + 2x = 11 + x \;\Rightarrow\; x = \fc{6}', 330, 56, ein=1.0)),
         sz('Frage 3',
            'n plus n plus eins plus n plus zwei gleich fünfundvierzig. Drei n plus drei gleich fünfundvierzig, n gleich vierzehn. Die Zahlen sind vierzehn, fünfzehn, sechzehn.',
            f(r'3n + 3 = 45 \;\Rightarrow\; n = \fc{14}', 330, 56, ein=1.0)),
         sz('Frage 4',
            'Die Gleichung liefert nur eine Zahl. Der Antwortsatz sagt, was sie bedeutet: Ein Heft kostet fünf Franken.',
            n('Ein Heft kostet 5 Fr.', 330, 'gruen', 48, ein=1.0)),
         sz('Frage 5',
            'Sechsundvierzig durch acht gibt fünf Komma sieben fünf. Fünf Autos reichen nicht: Es braucht sechs.',
            f(r'46 : 8 = 5.75 \;\Rightarrow\; \fc{6}\ \text{Autos}', 330, 56, ein=1.0)),
         merke('Zum Mitnehmen: Variable festlegen, Gleichung aufstellen und lösen, dann prüfen: Beantwortet die Zahl die Frage, muss gerundet werden?',
               'Variable · Gleichung · Lösung|prüfen: passt es zur Frage?|runden, wo nur Ganzes geht'),
     ], [
         wahl('Frage 1', 'Ein Taxi kostet 4 Fr. plus 2 Fr. pro km. Du zahlst 30 Fr. Wie viele km bist du gefahren?', ['13 km', '15 km', '17 km'], 0,
              {0: 'Ja.', 1: 'Die 4 Fr. Grundtaxe gehen zuerst weg.', 2: 'Die Grundtaxe wird abgezählt, nicht dazugezählt.'},
              sprich='Ein Taxi kostet vier Franken plus zwei Franken pro Kilometer. Du zahlst dreissig Franken. Wie viele Kilometer bist du gefahren?',
              rueck_sprich={1: 'Die vier Franken Grundtaxe gehen zuerst weg.', 2: 'Die Grundtaxe wird abgezählt, nicht dazugezählt.'}),
         wahl('Frage 2', 'A kostet 5 Fr. plus 2 Fr. pro Stück, B 11 Fr. plus 1 Fr. pro Stück. Wann sind beide gleich teuer?', ['bei 6 Stück', 'bei 2 Stück', 'bei 16 Stück'], 0,
              {0: 'Ja.', 1: 'Setz 2 ein: A 9 Fr., B 13 Fr. Gleich?', 2: 'Setz die Terme gleich: 5 + 2x = 11 + x.'},
              sprich='A kostet fünf Franken plus zwei Franken pro Stück, B elf Franken plus einen Franken pro Stück. Wann sind beide gleich teuer?',
              rueck_sprich={1: 'Setz zwei ein: A kostet neun Franken, B dreizehn. Gleich?', 2: 'Setz die beiden Terme gleich.'}),
         wahl('Frage 3', 'Drei aufeinanderfolgende ganze Zahlen haben die Summe 45. Wie heisst die kleinste?', ['14', '15', '13'], 0,
              {0: 'Ja.', 1: '15 ist die mittlere: 14 + 15 + 16.', 2: '13 + 14 + 15 = 42, zu wenig.'},
              sprich='Drei aufeinanderfolgende ganze Zahlen haben die Summe fünfundvierzig. Wie heisst die kleinste?',
              rueck_sprich={1: 'Fünfzehn ist die mittlere.', 2: 'Dreizehn plus vierzehn plus fünfzehn ist zweiundvierzig, zu wenig.'}),
         wahl('Frage 4', '5 gleiche Hefte kosten 25 Fr. Jonas schreibt: «x = 5». Was fehlt?', ['der Antwortsatz: Ein Heft kostet 5 Fr.', 'nichts, x = 5 ist die Antwort', 'die Einheit km'], 0,
              {0: 'Ja.', 1: 'Was bedeutet die 5? Das sagt erst ein Satz.', 2: 'Es geht um Franken, nicht um Kilometer.'},
              sprich='Fünf gleiche Hefte kosten fünfundzwanzig Franken. Jonas schreibt: x gleich fünf. Was fehlt?',
              rueck_sprich={1: 'Was bedeutet die Fünf? Das sagt erst ein Satz.', 2: 'Es geht um Franken, nicht um Kilometer.'}),
         wahl('Frage 5', '46 Personen fahren in Autos mit je 8 Plätzen. Wie viele Autos braucht es?', ['6', '5', '5.75'], 0,
              {0: 'Ja.', 1: 'In 5 Autos haben nur 40 Personen Platz.', 2: 'Ein Viertelauto gibt es nicht.'},
              sprich='Sechsundvierzig Personen fahren in Autos mit je acht Plätzen. Wie viele Autos braucht es?',
              rueck_sprich={1: 'In fünf Autos haben nur vierzig Personen Platz.', 2: 'Ein Viertelauto gibt es nicht.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung: Weg, Geschwindigkeit, Zeit
clip('svt', 3, 'Mathematisieren: Weg, Geschwindigkeit, Zeit',
     'Zug 240 km in 2 h: 120 km/h; s = v · t in drei Formen; Vorhersage Velo 18 km/h während 20 min: 6 km; 45 min = 0.75 h, '
     '1 m/s = 3.6 km/h; Plausibilität; Fehler 18 · 20 = 360 km.',
     ['Geschwindigkeit', 'Weg', 'Zeit', 'Einheiten', 'km/h', 'Plausibilität'], [
         sz('Zug',
            'Ein Zug fährt zweihundertvierzig Kilometer in zwei Stunden. In jeder Stunde schafft er hundertzwanzig Kilometer: Seine Geschwindigkeit ist hundertzwanzig Kilometer pro Stunde.',
            f(r'v = \dfrac{240\ \text{km}}{2\ \text{h}} = \fc{120}\ \text{km/h}', 300, 52, ein='@Geschwindigkeit'),
            graf(W_Z, **ZZ),
            dict(ueber(W_Z, ein='@Zug', **ZZ), figuren=[S((0, 0), (2, 240), 1, 5)]),
            ueber(W_Z, punkte=[pt(2, 240, 5, '(2 | 240)')], ein='@Stunden', **ZZ)),
         sz('Formel',
            'Weg gleich Geschwindigkeit mal Zeit. Daraus folgen die beiden anderen Formen: Geschwindigkeit gleich Weg durch Zeit, Zeit gleich Weg durch Geschwindigkeit.',
            f(r's = v \cdot t', 280, 66, ein='@Weg'),
            f(r'v = \dfrac{s}{t} \qquad t = \dfrac{s}{v}', 400, 58, ein='@folgen'),
            dict(graf(W_Z, **ZZ), figuren=[S((0, 0), (3, 360), 1, 5)])),
         sz('Vorhersage',
            'Zwanzig Minuten sind ein Drittel Stunde. Achtzehn mal ein Drittel gibt sechs: Das Velo fährt sechs Kilometer.',
            f(r'20\ \text{min} = \tfrac{1}{3}\ \text{h}', 280, 54, ein='@Minuten'),
            f(r's = 18 \cdot \tfrac{1}{3} = \fc{6}\ \text{km}', 400, 56, ein='@Velo')),
         sz('Einheiten',
            'Minuten rechnest du in Stunden um, indem du durch sechzig teilst: Fünfundvierzig Minuten sind null Komma sieben fünf Stunden. '
            'Und ein Meter pro Sekunde sind drei Komma sechs Kilometer pro Stunde.',
            f(r'45\ \text{min} = \dfrac{45}{60}\ \text{h} = \fc{0.75}\ \text{h}', 280, 50, ein='@teilst'),
            f(r'1\ \text{m/s} = 3.6\ \text{km/h}', 420, 54, ein='@Meter')),
         sz('Plausibel',
            'Prüf jedes Ergebnis: Zu Fuss gehst du etwa fünf Kilometer pro Stunde, mit dem Velo fünfzehn bis fünfundzwanzig, ein Zug fährt über hundert.',
            n('zu Fuss ≈ 5 km/h|Velo 15 bis 25 km/h|Zug über 100 km/h', 300, 'blau', 46, ein='@Prüf')),
         sz('Fehler',
            'Häufiger Fehler: achtzehn mal zwanzig gleich dreihundertsechzig Kilometer. Ein Velo fährt in zwanzig Minuten nie so weit. Die Minuten müssen zuerst in Stunden.',
            f(r'\fd{18 \cdot 20 = 360\ \text{km}}', 300, 56, ein='@Fehler'),
            n('Minuten zuerst in Stunden umrechnen', 420, 'rot', 44, ein='@Minuten')),
         merke('Zum Mitnehmen: s gleich v mal t. Die Zeit in die Einheit der Geschwindigkeit umrechnen, Minuten durch sechzig. Dann prüfen, ob das Ergebnis plausibel ist.',
               's = v · t,  v = s : t,  t = s : v|Minuten : 60 = Stunden|plausibel?'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Ein Velo fährt 20 Minuten lang mit 18 km/h. Wie weit kommt es?', ['6 km', '360 km', '3.6 km'], 0,
              {0: 'Ja.', 1: 'Das Velo fährt keine 360 km in 20 Minuten. Die Minuten müssen zuerst in Stunden.', 2: '18 · 0.2 rechnet 20 min als 0.2 h. Wie viele Stunden sind 20 Minuten?'},
              sprich='Ein Velo fährt zwanzig Minuten lang mit achtzehn Kilometern pro Stunde. Wie weit kommt es?',
              rueck_sprich={1: 'Das Velo fährt keine dreihundertsechzig Kilometer in zwanzig Minuten. Die Minuten müssen zuerst in Stunden.', 2: 'Du hast zwanzig Minuten als null Komma zwei Stunden gerechnet. Wie viele Stunden sind zwanzig Minuten?'}),
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
clip('kontrolle-svt', 4, 'Mathematisieren: Kontrollfragen zu s = v · t',
     'Fünf Fragen: 120 km in 1.5 h, 15 min in h, 72 km/h in m/s, 30 min mit 50 km/h, 400 km mit 50 km/h.',
     ['Geschwindigkeit', 'Einheiten', 'Kontrollfragen'], [
         sz('Frage 1',
            'Eine Stunde dreissig Minuten sind eins Komma fünf Stunden. Hundertzwanzig durch eins Komma fünf gibt achtzig Kilometer pro Stunde.',
            f(r'v = \dfrac{120}{1.5} = \fc{80}\ \text{km/h}', 330, 56, ein=1.0)),
         sz('Frage 2',
            'Fünfzehn durch sechzig gibt null Komma zwei fünf Stunden.',
            f(r'\dfrac{15}{60} = \fc{0.25}\ \text{h}', 330, 56, ein=1.0)),
         sz('Frage 3',
            'Zweiundsiebzig durch drei Komma sechs gibt zwanzig Meter pro Sekunde.',
            f(r'72 : 3.6 = \fc{20}\ \text{m/s}', 330, 56, ein=1.0)),
         sz('Frage 4',
            'Dreissig Minuten sind eine halbe Stunde. Fünfzig mal null Komma fünf gibt fünfundzwanzig Kilometer.',
            f(r's = 50 \cdot 0.5 = \fc{25}\ \text{km}', 330, 56, ein=1.0)),
         sz('Frage 5',
            'Vierhundert durch fünfzig gibt acht Stunden. Plausibel: Für eine so lange Strecke mit fünfzig Kilometern pro Stunde braucht es einen ganzen Arbeitstag.',
            f(r't = \dfrac{400}{50} = \fc{8}\ \text{h}', 330, 56, ein=1.0)),
         merke('Zum Mitnehmen: Zeiten in Stunden umrechnen, dann mit s gleich v mal t rechnen. Kilometer pro Stunde durch drei Komma sechs gibt Meter pro Sekunde.',
               'erst die Einheiten, dann rechnen|km/h : 3.6 = m/s'),
     ], [
         wahl('Frage 1', 'Ein Bus fährt 120 km in 1 h 30 min. Wie schnell fährt er im Durchschnitt?', ['80 km/h', '92.3 km/h', '120 km/h'], 0,
              {0: 'Ja.', 1: '1 h 30 min sind nicht 1.30 h, sondern 1.5 h.', 2: 'Er braucht mehr als eine Stunde für die 120 km.'},
              sprich='Ein Bus fährt hundertzwanzig Kilometer in einer Stunde und dreissig Minuten. Wie schnell fährt er im Durchschnitt?',
              rueck_sprich={1: 'Eine Stunde dreissig sind nicht eins Komma drei null Stunden.', 2: 'Er braucht mehr als eine Stunde für die hundertzwanzig Kilometer.'}),
         wahl('Frage 2', 'Wie viele Stunden sind 15 Minuten?', ['0.25 h', '0.15 h', '4 h'], 0,
              {0: 'Ja.', 1: 'Eine Stunde hat 60 Minuten, nicht 100.', 2: 'Rechne 15 : 60, nicht 60 : 15.'},
              sprich='Wie viele Stunden sind fünfzehn Minuten?',
              rueck_sprich={1: 'Eine Stunde hat sechzig Minuten, nicht hundert.', 2: 'Teile fünfzehn durch sechzig, nicht umgekehrt.'}),
         wahl('Frage 3', 'Ein Auto fährt 72 km/h. Wie viele m/s sind das?', ['20 m/s', '259.2 m/s', '72 m/s'], 0,
              {0: 'Ja.', 1: 'Ein Auto ist keine 259 m pro Sekunde schnell. Teilen statt mal.', 2: 'Meter pro Sekunde ist eine andere Einheit.'},
              sprich='Ein Auto fährt zweiundsiebzig Kilometer pro Stunde. Wie viele Meter pro Sekunde sind das?',
              rueck_sprich={1: 'So schnell ist kein Auto. Teilen statt mal.', 2: 'Meter pro Sekunde ist eine andere Einheit.'}),
         wahl('Frage 4', 'Ein Auto fährt 30 Minuten lang 50 km/h. Wie weit kommt es?', ['25 km', '1500 km', '15 km'], 0,
              {0: 'Ja.', 1: 'Die Minuten müssen zuerst in Stunden.', 2: '30 min sind 0.5 h, nicht 0.3 h.'},
              sprich='Ein Auto fährt dreissig Minuten lang fünfzig Kilometer pro Stunde. Wie weit kommt es?',
              rueck_sprich={1: 'Die Minuten müssen zuerst in Stunden.', 2: 'Dreissig Minuten sind eine halbe Stunde.'}),
         wahl('Frage 5', 'Wie lange dauert eine Fahrt von 400 km mit 50 km/h?', ['8 h', '20000 h', '0.125 h'], 0,
              {0: 'Ja.', 1: 'Zeit ist Weg durch Geschwindigkeit, nicht mal.', 2: 'Rechne 400 : 50, nicht 50 : 400.'},
              sprich='Wie lange dauert eine Fahrt von vierhundert Kilometern mit fünfzig Kilometern pro Stunde?',
              rueck_sprich={1: 'Zeit ist Weg durch Geschwindigkeit, nicht mal.', 2: 'Teile den Weg durch die Geschwindigkeit, nicht umgekehrt.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung: Fahrt in Abschnitten
clip('abschnitte', 5, 'Mathematisieren: Fahrt in Abschnitten',
     'Velotour 30 km mit 20 km/h, 30 min Pause, 20 km mit 10 km/h: Tabelle, Gesamtzeit 4 h, Vorhersage Durchschnitt 12.5 km/h (gestrichelte Verbindung); '
     'Fehler: Geschwindigkeiten mitteln (15), Steigung falsch lesen.',
     ['Durchschnittsgeschwindigkeit', 'Abschnitte', 'Tabelle', 'Weg-Zeit-Graph'], [
         sz('Tour',
            'Eine Velotour: dreissig Kilometer mit zwanzig Kilometern pro Stunde, dann eine halbe Stunde Pause, dann zwanzig Kilometer bergauf mit zehn Kilometern pro Stunde.',
            n('30 km mit 20 km/h|30 min Pause|20 km mit 10 km/h', 300, 'blau', 46, ein='@Velotour')),
         sz('Tabelle',
            'Für jeden Abschnitt eine Zeile. Zeit gleich Weg durch Geschwindigkeit: eins Komma fünf Stunden, die Pause null Komma fünf, dann zwei Stunden. Zusammen vier Stunden für fünfzig Kilometer.',
            f(r'\begin{array}{l|c|c} & t\ [\text{h}] & s\ [\text{km}] \\ \hline \fa{1} & \fa{1.5} & \fa{30} \\ \text{Pause} & 0.5 & 0 \\ \fb{2} & \fb{2} & \fb{20} \\ \hline \text{total} & 4 & 50 \end{array}', 260, 46, ein='@Zeile'),
            graf(W_V, **ZZ),
            dict(ueber(W_V, ein='@Stunden', **ZZ), figuren=[S(TOUR[0], TOUR[1], 1, 5)]),
            dict(ueber(W_V, ein='@Pause', **ZZ), figuren=[S(TOUR[1], TOUR[2], 5, 5)]),
            dict(ueber(W_V, ein='@dann+0.8', **ZZ), figuren=[S(TOUR[2], TOUR[3], 2, 5)])),
         sz('Vorhersage',
            'Durchschnitt heisst: Gesamtweg durch Gesamtzeit. Fünfzig durch vier gibt zwölf Komma fünf Kilometer pro Stunde. Im Graphen ist das die gestrichelte Verbindung von Start und Ziel.',
            f(r'\dfrac{50\ \text{km}}{4\ \text{h}} = \fc{12.5}\ \text{km/h}', 300, 56, ein='@Gesamtweg'),
            dict(graf(W_V, **ZZ), figuren=[S(TOUR[0], TOUR[1], 1, 5), S(TOUR[1], TOUR[2], 5, 5), S(TOUR[2], TOUR[3], 2, 5)]),
            dict(ueber(W_V, ein='@gestrichelte', **ZZ), figuren=[S((0, 0), (4, 50), 3, 4, gest=True)])),
         sz('Fehler',
            'Häufiger Fehler: zwanzig plus zehn durch zwei gleich fünfzehn. Der langsame Abschnitt dauert länger und zählt darum mehr. Und die Pause gehört zur Zeit.',
            f(r'\fd{\dfrac{20 + 10}{2} = 15}', 300, 56, ein='@Fehler'),
            n('langsamer Abschnitt dauert länger|Pause zählt zur Gesamtzeit', 440, 'rot', 44, ein='@langsame')),
         sz('Steigung',
            'Im Weg-Zeit-Graphen ist der steilere Abschnitt der schnellere, nicht der längere. Der erste Abschnitt ist steiler als der dritte, die Pause ist waagrecht.',
            n('steiler = schneller|waagrecht = Pause', 300, 'blau', 46, ein='@steilere'),
            dict(graf(W_V, **ZZ), figuren=[S(TOUR[0], TOUR[1], 1, 5), S(TOUR[1], TOUR[2], 5, 5), S(TOUR[2], TOUR[3], 2, 5)])),
         merke('Zum Mitnehmen: Jeder Abschnitt bekommt eine Zeile. Durchschnitt ist Gesamtweg durch Gesamtzeit, mit Pausen. Geschwindigkeiten mitteln stimmt nur bei gleich langen Zeiten.',
               'Tabelle: eine Zeile pro Abschnitt|Durchschnitt = Gesamtweg : Gesamtzeit|nicht die Geschwindigkeiten mitteln'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Wie gross ist die Durchschnittsgeschwindigkeit der ganzen Tour?', ['12.5 km/h', '15 km/h', '14.3 km/h'], 0,
              {0: 'Ja.', 1: 'Das ist das Mittel aus 20 und 10. Der langsame Teil dauert aber länger.', 2: 'So wäre es ohne Pause. Die Pause gehört zur Zeit der Tour.'},
              sprich='Wie gross ist die Durchschnittsgeschwindigkeit der ganzen Tour?',
              rueck_sprich={1: 'Das ist das Mittel aus zwanzig und zehn. Der langsame Teil dauert aber länger.', 2: 'So wäre es ohne Pause. Die Pause gehört zur Zeit der Tour.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
W_K3 = dict(xbereich=[-0.4, 3.3], ybereich=[-6, 100], xteilung=teil(1, 2, 3), yteilung=teil(30, 60, 90))
FRAGEBILD.update({('kontrolle-abschnitte', 'Frage 5'): (W_K3, [], [], {'figuren': zug([(0, 0), (1, 30), (2, 90)]) +
                                                          [T(0.55, 25, 'I', 5, 'start', g=34), T(1.55, 70, 'II', 5, 'end', g=34)], **ZZ})})
clip('kontrolle-abschnitte', 6, 'Mathematisieren: Kontrollfragen zu Abschnitten',
     'Fünf Fragen: je 1 h mit 60 und 20 km/h, 120 km in 3 h plus 1 h Pause, 30 km hin mit 30 und zurück mit 15 km/h, Gesamtzeit 10 km mit 20 und 6 km mit 12 km/h, steilerer Abschnitt.',
     ['Durchschnittsgeschwindigkeit', 'Abschnitte', 'Kontrollfragen'], [
         sz('Frage 1',
            'Beide Abschnitte dauern gleich lang. Achtzig Kilometer in zwei Stunden: vierzig Kilometer pro Stunde. Hier stimmt sogar das Mittel.',
            f(r'\dfrac{60 + 20}{2} = \fc{40}\ \text{km/h}', 330, 56, ein=1.0)),
         sz('Frage 2',
            'Hundertzwanzig Kilometer in vier Stunden, die Pause mitgezählt: dreissig Kilometer pro Stunde.',
            f(r'\dfrac{120}{3 + 1} = \fc{30}\ \text{km/h}', 330, 56, ein=1.0)),
         sz('Frage 3',
            'Hin eine Stunde, zurück zwei Stunden. Sechzig Kilometer in drei Stunden: zwanzig Kilometer pro Stunde, nicht zweiundzwanzig Komma fünf.',
            f(r'\dfrac{60}{1 + 2} = \fc{20}\ \text{km/h}', 330, 56, ein=1.0)),
         sz('Frage 4',
            'Eine halbe Stunde und noch eine halbe Stunde: zusammen eine Stunde.',
            f(r'\dfrac{10}{20} + \dfrac{6}{12} = 0.5 + 0.5 = \fc{1}\ \text{h}', 330, 52, ein=1.0)),
         sz('Frage 5',
            'Abschnitt zwei ist steiler: In einer Stunde kommen sechzig Kilometer dazu, in Abschnitt eins nur dreissig.',
            n('II: steiler, also schneller', 330, 'gruen', 46, ein=1.0),
            dict(graf(W_K3, **ZZ), figuren=zug([(0, 0), (1, 30), (2, 90)]))),
         merke('Zum Mitnehmen: Durchschnitt ist Gesamtweg durch Gesamtzeit. Nur bei gleich langen Zeiten darf man die Geschwindigkeiten mitteln. Steiler heisst schneller.',
               'Gesamtweg : Gesamtzeit|Mittel nur bei gleichen Zeiten|steiler = schneller'),
     ], [
         wahl('Frage 1', 'Je eine Stunde mit 60 km/h und mit 20 km/h. Wie gross ist der Durchschnitt?', ['40 km/h', '80 km/h', '30 km/h'], 0,
              {0: 'Ja.', 1: '80 km ist der Weg. Wie lange hat es gedauert?', 2: 'Rechne den Weg aus: 60 + 20 km in 2 h.'},
              sprich='Je eine Stunde mit sechzig und mit zwanzig Kilometern pro Stunde. Wie gross ist der Durchschnitt?',
              rueck_sprich={1: 'Achtzig Kilometer ist der Weg. Wie lange hat es gedauert?', 2: 'Rechne zuerst den ganzen Weg aus.'}),
         wahl('Frage 2', '120 km Fahrt in 3 h, dazu 1 h Pause. Wie gross ist der Durchschnitt der Reise?', ['30 km/h', '40 km/h', '120 km/h'], 0,
              {0: 'Ja.', 1: 'Die Pause gehört zur Reise.', 2: 'Die Reise dauert mehr als eine Stunde.'},
              sprich='Hundertzwanzig Kilometer Fahrt in drei Stunden, dazu eine Stunde Pause. Wie gross ist der Durchschnitt der Reise?',
              rueck_sprich={1: 'Die Pause gehört zur Reise.', 2: 'Die Reise dauert mehr als eine Stunde.'}),
         wahl('Frage 3', '30 km hin mit 30 km/h, zurück mit 15 km/h. Wie gross ist der Durchschnitt?', ['20 km/h', '22.5 km/h', '45 km/h'], 0,
              {0: 'Ja.', 1: 'Das ist das Mittel. Der Rückweg dauert aber doppelt so lang.', 2: 'Rechne Gesamtweg durch Gesamtzeit.'},
              sprich='Dreissig Kilometer hin mit dreissig, zurück mit fünfzehn Kilometern pro Stunde. Wie gross ist der Durchschnitt?',
              rueck_sprich={1: 'Das ist das Mittel. Der Rückweg dauert aber doppelt so lang.', 2: 'Rechne Gesamtweg durch Gesamtzeit.'}),
         wahl('Frage 4', '10 km mit 20 km/h, dann 6 km mit 12 km/h. Wie lange dauert das?', ['1 h', '16 h', '0.5 h'], 0,
              {0: 'Ja.', 1: 'Zeit ist Weg durch Geschwindigkeit, je Abschnitt.', 2: 'Das ist erst der erste Abschnitt.'},
              sprich='Zehn Kilometer mit zwanzig, dann sechs Kilometer mit zwölf Kilometern pro Stunde. Wie lange dauert das?',
              rueck_sprich={1: 'Zeit ist Weg durch Geschwindigkeit, für jeden Abschnitt.', 2: 'Das ist erst der erste Abschnitt.'}),
         wahl('Frage 5', 'In welchem Abschnitt im Bild ist die Fahrt schneller?', ['in Abschnitt II', 'in Abschnitt I', 'beide gleich'], 0,
              {0: 'Ja.', 1: 'Beide dauern 1 h. Wo kommt mehr Weg dazu?', 2: 'Vergleich die Steilheit.'},
              sprich='In welchem Abschnitt im Bild ist die Fahrt schneller?',
              rueck_sprich={1: 'Beide dauern eine Stunde. Wo kommt mehr Weg dazu?', 2: 'Vergleich die Steilheit.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung: Begegnung und Einholen
clip('begegnung', 7, 'Mathematisieren: Begegnung und Einholen',
     'Zwei Velos 36 km auseinander, 14 und 10 km/h aufeinander zu: Abstand schrumpft mit 24 km/h, Vorhersage Treffen nach 1.5 h bei 21 km; '
     'Einholen mit Vorsprung 10 km, 15 gegen 10 km/h: 2 h; Rolltreppe 30 m: mit 20 s, dagegen 60 s; Modellannahmen; Fehler: gleiche Richtung addiert.',
     ['Begegnung', 'Einholen', 'Rolltreppe', 'Annäherungsgeschwindigkeit', 'Modell'], [
         sz('Lage',
            'Zwei Velofahrerinnen sind sechsunddreissig Kilometer voneinander entfernt und fahren gleichzeitig los, aufeinander zu. Anna fährt vierzehn, Bea zehn Kilometer pro Stunde.',
            n('Abstand 36 km|Anna 14 km/h →   ← Bea 10 km/h', 300, 'blau', 44, ein='@Velofahrerinnen'),
            graf(W_B, **BZ),
            dict(ueber(W_B, ein='@Anna', **BZ), figuren=[S((0, 0), (1, 14), 1, 5)]),
            dict(ueber(W_B, ein='@fährt+0.5', **BZ), figuren=[S((0, 36), (1, 26), 2, 5)])),
         sz('Annäherung',
            'In jeder Stunde kommen sie sich um vierzehn plus zehn, also vierundzwanzig Kilometer näher. Bei Begegnungen addierst du die Geschwindigkeiten.',
            f(r'14 + 10 = 24\ \text{km/h}', 300, 56, ein='@näher'),
            n('aufeinander zu: addieren', 420, 'blau', 44, ein='@Begegnungen'),
            dict(graf(W_B, **BZ), figuren=[S((0, 0), (1, 14), 1, 5), S((0, 36), (1, 26), 2, 5), S((1, 14), (1, 26), 5, 3, gest=True)])),
         sz('Vorhersage',
            'Sechsunddreissig durch vierundzwanzig gibt eins Komma fünf Stunden. Dann ist Anna einundzwanzig Kilometer gefahren, Bea fünfzehn. Der Treffpunkt liegt nicht in der Mitte.',
            f(r't = \dfrac{36}{24} = \fc{1.5}\ \text{h}', 280, 54, ein='@gibt'),
            f(r'\fa{14 \cdot 1.5 = 21} \qquad \fb{10 \cdot 1.5 = 15}', 420, 50, ein='@Anna'),
            dict(graf(W_B, **BZ), figuren=[S((0, 0), (1, 14), 1, 5), S((0, 36), (1, 26), 2, 5)]),
            dict(ueber(W_B, ein='@gibt', **BZ), figuren=[S((1, 14), (2.5, 35), 1, 5), S((1, 26), (2.5, 11), 2, 5)]),
            ueber(W_B, punkte=[pt(1.5, 21, 3, '(1.5 | 21)', [1.5, 9.5], 'middle')], ein='@Anna', **BZ)),
         sz('Einholen',
            'Anders beim Einholen. Bea startet eine Stunde früher mit zehn Kilometern pro Stunde, Anna folgt mit fünfzehn. Bea hat zehn Kilometer Vorsprung, Anna holt pro Stunde nur fünf auf: nach zwei Stunden.',
            f(r'\text{Vorsprung } 10\ \text{km}', 280, 50, ein='@Vorsprung'),
            f(r'15 - 10 = 5 \;\Rightarrow\; t = \dfrac{10}{5} = \fc{2}\ \text{h}', 390, 50, ein='@holt'),
            graf(W_B, **BZ),
            dict(ueber(W_B, ein='@startet', **BZ), figuren=[S((0, 10), (2.5, 35), 2, 5)]),
            dict(ueber(W_B, ein='@folgt', **BZ), figuren=[S((0, 0), (2.5, 37.5), 1, 5)]),
            ueber(W_B, punkte=[pt(2, 30, 3, '(2 | 30)')], ein='@nach', **BZ)),
         sz('Rolltreppe',
            'Auch eine Rolltreppe ist so eine Aufgabe. Sie ist dreissig Meter lang und fährt null Komma fünf Meter pro Sekunde, du gehst einen Meter pro Sekunde. '
            'Mit der Treppe bist du eins Komma fünf Meter pro Sekunde schnell und brauchst zwanzig Sekunden. Gegen die Treppe nur null Komma fünf: sechzig Sekunden.',
            f(r'\text{mit: } \dfrac{30}{1 + 0.5} = \fc{20}\ \text{s}', 280, 50, ein='@Mit'),
            f(r'\text{gegen: } \dfrac{30}{1 - 0.5} = \fc{60}\ \text{s}', 420, 50, ein='@Gegen')),
         sz('Modell',
            'Das ist ein Modell: Alle fahren gleichmässig schnell und starten genau gleichzeitig. Ampeln, Steigungen und Pausen lässt das Modell weg. Ob das passt, entscheidest du bei jeder Aufgabe.',
            n('Modell: gleichmässig schnell,|gleichzeitiger Start|Ampeln, Steigungen, Pausen weggelassen', 300, 'blau', 42, ein='@Modell')),
         sz('Fehler',
            'Häufiger Fehler: beim Einholen die Geschwindigkeiten addieren. Wer hinterherfährt, holt nur den Unterschied auf.',
            f(r'\fd{15 + 10 = 25}', 300, 56, ein='@addieren'),
            n('gleiche Richtung: subtrahieren', 420, 'rot', 44, ein='@Unterschied')),
         merke('Zum Mitnehmen: Aufeinander zu addierst du die Geschwindigkeiten, in gleicher Richtung subtrahierst du sie. Zeit gleich Abstand durch Annäherungsgeschwindigkeit.',
               'aufeinander zu: v₁ + v₂|gleiche Richtung: v₁ − v₂|t = Abstand : Annäherung'),
         jetzt_du(),
     ], [
         wahl('Vorhersage', 'Wann treffen sich Anna und Bea?', ['nach 1.5 h', 'nach 9 h', 'nach 3 h'], 0,
              {0: 'Ja.', 1: 'Sie fahren aufeinander zu. 14 − 10 wäre richtig, wenn Anna Bea einholen müsste.', 2: '36 : 12 nimmt an, dass beide 12 km/h fahren. Wie viel näher kommen sie sich pro Stunde?'},
              sprich='Wann treffen sich Anna und Bea?',
              rueck_sprich={1: 'Sie fahren aufeinander zu. Die Differenz wäre richtig, wenn Anna Bea einholen müsste.', 2: 'Wie viel näher kommen sie sich in einer Stunde?'}),
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
clip('kontrolle-begegnung', 8, 'Mathematisieren: Kontrollfragen zu Begegnung und Einholen',
     'Fünf Fragen: Annäherung bei 30 und 20 km/h aufeinander zu und in gleicher Richtung, Züge 100 km mit 60 und 40 km/h, Einholen mit 6 km Vorsprung bei 18 gegen 12 km/h, Rolltreppe gegen die Fahrrichtung.',
     ['Begegnung', 'Einholen', 'Rolltreppe', 'Kontrollfragen'], [
         sz('Frage 1',
            'Aufeinander zu addierst du: dreissig plus zwanzig gibt fünfzig Kilometer pro Stunde.',
            f(r'30 + 20 = \fc{50}\ \text{km/h}', 330, 56, ein=1.0)),
         sz('Frage 2',
            'In gleicher Richtung subtrahierst du: dreissig minus zwanzig gibt zehn Kilometer pro Stunde.',
            f(r'30 - 20 = \fc{10}\ \text{km/h}', 330, 56, ein=1.0)),
         sz('Frage 3',
            'Sechzig plus vierzig gibt hundert Kilometer pro Stunde. Hundert Kilometer schaffen sie zusammen in einer Stunde.',
            f(r'\dfrac{100}{60 + 40} = \fc{1}\ \text{h}', 330, 56, ein=1.0)),
         sz('Frage 4',
            'Pro Stunde holt das schnellere Velo sechs Kilometer auf. Für sechs Kilometer Vorsprung braucht es eine Stunde.',
            f(r'\dfrac{6}{18 - 12} = \fc{1}\ \text{h}', 330, 56, ein=1.0)),
         sz('Frage 5',
            'Gegen die Treppe zieht sie dich zurück: eins Komma fünf minus null Komma fünf gibt einen Meter pro Sekunde.',
            f(r'1.5 - 0.5 = \fc{1}\ \text{m/s}', 330, 56, ein=1.0)),
         merke('Zum Mitnehmen: Aufeinander zu addieren, in gleicher Richtung subtrahieren. Dann Abstand durch diese Annäherungsgeschwindigkeit.',
               'zu: addieren · gleich: subtrahieren|t = Abstand : Annäherung'),
     ], [
         wahl('Frage 1', 'Zwei Velos fahren mit 30 km/h und 20 km/h aufeinander zu. Um wie viel kommen sie sich pro Stunde näher?', ['50 km', '10 km', '25 km'], 0,
              {0: 'Ja.', 1: 'Sie fahren aufeinander zu, nicht hintereinander.', 2: 'Beide fahren, also kommen beide Wege zusammen.'},
              sprich='Zwei Velos fahren mit dreissig und zwanzig Kilometern pro Stunde aufeinander zu. Um wie viel kommen sie sich pro Stunde näher?',
              rueck_sprich={1: 'Sie fahren aufeinander zu, nicht hintereinander.', 2: 'Beide fahren, also kommen beide Wege zusammen.'}),
         wahl('Frage 2', 'Ein Velo mit 30 km/h fährt einem mit 20 km/h hinterher. Um wie viel kommt es pro Stunde näher?', ['10 km', '50 km', '0 km'], 0,
              {0: 'Ja.', 1: 'Das vordere fährt davon. Es zählt nur der Unterschied.', 2: 'Das hintere ist schneller, es kommt also näher.'},
              sprich='Ein Velo mit dreissig Kilometern pro Stunde fährt einem mit zwanzig hinterher. Um wie viel kommt es pro Stunde näher?',
              rueck_sprich={1: 'Das vordere fährt davon. Es zählt nur der Unterschied.', 2: 'Das hintere ist schneller, es kommt also näher.'}),
         wahl('Frage 3', 'Zwei Züge sind 100 km auseinander und fahren mit 60 km/h und 40 km/h aufeinander zu. Wann begegnen sie sich?', ['nach 1 h', 'nach 5 h', 'nach 2.5 h'], 0,
              {0: 'Ja.', 1: 'Das wäre in gleicher Richtung. Die Züge fahren aufeinander zu.', 2: 'Der zweite Zug fährt auch.'},
              sprich='Zwei Züge sind hundert Kilometer auseinander und fahren mit sechzig und vierzig Kilometern pro Stunde aufeinander zu. Wann begegnen sie sich?',
              rueck_sprich={1: 'Das wäre in gleicher Richtung. Die Züge fahren aufeinander zu.', 2: 'Der zweite Zug fährt auch.'}),
         wahl('Frage 4', 'Ein Velo hat 6 km Vorsprung und fährt 12 km/h. Ein zweites folgt mit 18 km/h. Wann holt es ein?', ['nach 1 h', 'nach 0.2 h', 'nach 0.5 h'], 0,
              {0: 'Ja.', 1: 'Gleiche Richtung: Es zählt nur der Unterschied.', 2: '6 : 12 benutzt nur ein Tempo. Wie viel holt das zweite pro Stunde auf?'},
              sprich='Ein Velo hat sechs Kilometer Vorsprung und fährt zwölf Kilometer pro Stunde. Ein zweites folgt mit achtzehn. Wann holt es ein?',
              rueck_sprich={1: 'Gleiche Richtung: Es zählt nur der Unterschied.', 2: 'Wie viel holt das zweite Velo pro Stunde auf?'}),
         wahl('Frage 5', 'Eine Rolltreppe fährt 0.5 m/s. Du gehst 1.5 m/s gegen die Fahrrichtung. Wie schnell kommst du voran?', ['1 m/s', '2 m/s', '0.5 m/s'], 0,
              {0: 'Ja.', 1: 'Das wäre mit der Treppe.', 2: 'Du bist schneller als die Treppe.'},
              sprich='Eine Rolltreppe fährt null Komma fünf Meter pro Sekunde. Du gehst eins Komma fünf Meter pro Sekunde gegen die Fahrrichtung. Wie schnell kommst du voran?',
              rueck_sprich={1: 'Das wäre mit der Treppe.', 2: 'Du bist schneller als die Treppe.'}),
     ], art='Kontrollclip')

if FEHLT:
    print('ohne gemessene Wortzeit (geschätzt):', len(FEHLT), FEHLT)
