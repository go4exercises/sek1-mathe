"""Erzeugt die acht Drehbücher des Leitprogramms Terme und Faktorisieren (09.10.2026).

  python3 scripts/lp/terme-faktorisieren/clips.py

Gerüst und Zeitlogik aus scripts/lp/bruchrechnen/clips.py: Je Kapitel ein Einführungsclip (mit einer
Vorhersagefrage) und ein Kontrollclip (fünf Fragen mit neuen Zahlen). Gemessene `dauer` werden beim Neulauf
gerettet; Einblendungen stehen als «@wort» auf dem Wort, das sie nennen (wortzeiten.json, faster-whisper medium).

Aufbau: Rechnung und Notizen links (x 150), das Bild rechts (x 1010, y 175, 760 × 760): Termkacheln, Flächenmodell,
Rechteckschema, Quadrat der binomischen Formeln, Paartabelle, gezeichnet mit `graf`, "figuren", Fenster 0 … 10.

Fragebild (HOWTO-leitprogramme §15): In den Kontrollclips zeigt das Bild beim Erscheinen einer Frage nur das Gegebene;
Rechnung und Auflösung erscheinen ab 1.0 s (nach der Antwort).

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite:
  1 blau   = x², x (Variable)                 \\fa{…}
  2 orange = Zahlen, gemeinsamer Faktor        \\fb{…}
  3 grün   = Ergebnis                          \\fc{…}
  4 rot    = negativ, Fehler                   \\fd{…}
  5 Tinte  = neutral
Im Quadrat der binomischen Formeln (wie Sim 3): a² blau, ab orange, b² grün.
Alle Zahlen in zahlen.py nachgerechnet.
"""
import difflib
import json
import os
import re
import zlib

R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
HIER = os.path.dirname(os.path.abspath(__file__)) + '/'
GX, GY, GB, GH, LX = 1010, 175, 760, 760, 150
PRAEFIX = 'terme-lp-'
WZ = json.load(open(HIER + 'wortzeiten.json')) if os.path.exists(HIER + 'wortzeiten.json') else {}
FEHLT = []

# ---------------------------------------------------------------- Zeiten auf den Ton (aus TALS Mathe, Kreis und Kreisteile)
SPRECH = {}


# Whisper schreibt Zahlwörter oft als Ziffern («fünfzehn» → «15»): solche Wörter auch an der Ziffer erkennen.
ZAHLWORT = {'eins': '1', 'zwei': '2', 'drei': '3', 'vier': '4', 'fünf': '5', 'sechs': '6', 'sieben': '7', 'acht': '8',
            'neun': '9', 'zehn': '10', 'zwölf': '12', 'vierzehn': '14', 'fünfzehn': '15', 'zwanzig': '20',
            'sechzehn': '16', 'achtzehn': '18', 'einundzwanzig': '21', 'fünfundzwanzig': '25', 'neunundvierzig': '49',
            'einundfünfzig': '51', 'einundachtzig': '81', 'vierzig': '40', 'einundvierzig': '41'}
NENNERWORT = {'halb': '2', 'drittel': '3', 'viertel': '4', 'fünftel': '5', 'sechstel': '6', 'achtel': '8', 'neuntel': '9',
              'zehntel': '10', 'zwölftel': '12'}


def passt(wort, gehoert):
    g = re.sub(r'[^\wäöü]', '', gehoert.lower().replace('ß', 'ss'))   # Whisper schreibt «größer»
    w_ = wort.lower()
    if not g:
        return False
    if w_ in ZAHLWORT and re.sub(r'\D', '', gehoert) == ZAHLWORT[w_]:
        return True
    if '\u2044' in gehoert:                    # Whisper schreibt Brüche als «1⁄3»: Zahlwort = Zähler, Bruchwort = Nenner
        z_, n_ = (re.sub(r'\D', '', t) for t in gehoert.split('\u2044', 1))
        return (w_ in ZAHLWORT and z_ == ZAHLWORT[w_]) or (w_ in NENNERWORT and n_ == NENNERWORT[w_])
    if g.isdigit():
        return False                       # «15» ist nicht «fünf»
    if g.startswith(w_) or (len(w_) >= 6 and w_ in g):
        return True
    # Ähnlich, aber nicht kürzer als das gesuchte Wort: sonst trifft «@Vielfachen» schon «Vielfache», «@quadriert»
    # schon «Quadrat» (Prüfung 09.10.2026).
    return (len(w_) >= 5 and w_[0] == g[0] and len(w_) <= len(g) <= len(w_) + 3
            and difflib.SequenceMatcher(None, w_, g).ratio() >= 0.8)   # 0.7 liess «quadriert» auf «Quadrat» fallen (Prüfung 09.10.2026)


def wann(clip_, szene, wort, nr=1, dazu=0.0):
    """Sekunde ab Szenenbeginn, zu der `wort` zum nr-ten Mal beginnt (Wortzeiten von faster-whisper).
    Ohne Messung geschätzt aus der Lage des Wortes im Sprechertext."""
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
    """Ersetzt `ein`/`aus` und Zeiten von `bewegung` der Form «@wort», «@wort#2», «@wort+0.3» durch Sekunden."""
    def los(sname, v):
        if isinstance(v, str) and v.startswith('@'):
            m = re.match(r'@([^#+\-]+)(?:#(\d+))?(?:([+\-])([\d.]+))?$', v)
            dazu = float(m.group(4) or 0) * (-1 if m.group(3) == '-' else 1)
            return wann(clip_, sname, m.group(1), int(m.group(2) or 1), dazu)
        return v
    for q in szenen:
        SPRECH[(clip_, q['name'])] = q['sprecher']
    for q in szenen:
        for el in q['elemente']:
            for z in ('ein', 'aus'):
                if z in el:
                    el[z] = los(q['name'], el[z])
            for k in el.get('figuren') or []:
                for z in ('ein', 'aus'):
                    if z in k:
                        k[z] = los(q['name'], k[z])
                if 'bewegung' in k:
                    k['bewegung'] = [[los(q['name'], b[0])] + b[1:] for b in k['bewegung']]


# ---------------------------------------------------------------- Figuren
W = dict(xbereich=[0, 10], ybereich=[0, 10], achsen=False)


def r3(v):
    return round(v, 3)


def V(pkte, farbe=1, fu=0.3, **kw):
    return dict(art='vieleck', punkte=[[r3(x), r3(y)] for x, y in pkte], farbe=farbe, fuellung=fu, **kw)


def RECHT(x0, y0, w, h, farbe=1, fu=0.3, **kw):
    return V([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], farbe, fu, **kw)


def S(a, b, farbe=5, gest=False, dicke=3, **kw):
    d = dict(art='strecke', von=[r3(a[0]), r3(a[1])], bis=[r3(b[0]), r3(b[1])], farbe=farbe, dicke=dicke, **kw)
    if gest:
        d['gestrichelt'] = True
    return d


def T(x, y, text, farbe=5, anker='middle', g=32, **kw):
    return dict(art='text', bei=[r3(x), r3(y)], text=text, farbe=farbe, anker=anker, groesse=g, kursiv=False, **kw)


def KR(m, r, farbe=5, fu=0.0, dicke=3, **kw):
    return dict(art='kreis', m=[r3(m[0]), r3(m[1])], r=r, farbe=farbe, fuellung=fu, dicke=dicke, **kw)


def mit(fg, **kw):
    d = dict(fg)
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def alle(figs, **kw):
    return [mit(f_, **kw) for f_ in figs]


def graf(figuren=(), ein=0.05, fenster=W, **kw):
    g = dict(typ='graf', x=GX, y=GY, breite=GB, hoehe=GH, abstand=0, anim='fade', ein=ein,
             kurven=[], geraden=[], punkte=[], figuren=list(figuren), pfeile=False, tippbar=True, raster=False, **fenster)
    g.update(kw)
    return g


# ---------------------------------------------------------------- Text und Szenen
def f(t, y, g=56, ein=0.8, x=LX):
    return dict(typ='formel', text=t, x=x, y=y, groesse=g, ein=ein)


def n(t, y, farbe='blau', g=44, ein=2.4):
    return dict(typ='notiz', text=t, x=LX, y=y, groesse=g, farbe=farbe, ein=ein)


def titel(t, y=280, g=86):
    return dict(typ='titel', text=t, x=LX, y=y, groesse=g)


def ypsilon(t):
    """Alleinstehendes «y» gesprochen als «Ypsilon»: Piper liest «y» sonst so, dass Whisper «Epsilon» hört (Hörprobe 10.10.2026).
    Wortteile wie «y-Glieder» bleiben."""
    return re.sub(r'(?<![\wäöüÄÖÜ-])y(?![\wäöüÄÖÜ-])', 'Ypsilon', t) if t else t


def sz(name, spr, *el):
    return dict(name=name, layout='zentriert', oben=200, sprecher=ypsilon(spr), elemente=list(el))


def wahl(szene, text, opt, richtig, rueck, sprich=None, rueck_sprich=None, bei=0.3):
    """Die richtige Antwort steht nicht immer zuoberst (deterministisch gedreht, wie in den Vorbildern)."""
    sprich = ypsilon(sprich)
    rueck_sprich = {i: ypsilon(v) for i, v in rueck_sprich.items()} if rueck_sprich else rueck_sprich
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


def klick(szene, text, ziel, richtig_text, fallen, falsch_text, sprich=None, falsch_sprich=None, tol=0.5, bei=0.3):
    # Ohne "eingabe": Die Streifen stehen ohne Achsen (wie die Figuren der Planimetrie).
    d = {'szene': szene, 'bei': bei, 'typ': 'klick', 'text': text, 'ziel': ziel, 'toleranz': tol,
         'richtig_text': richtig_text, 'fallen': fallen, 'falsch_text': falsch_text}
    if sprich:
        d['sprich'] = sprich
    if falsch_sprich:
        d['falsch_sprich'] = falsch_sprich
    return d


def jetzt_du(wo='in der Animation'):
    return sz('Jetzt du', 'Jetzt du: Erkunde diese Zusammenhänge %s unter dem Clip und löse die Aufgaben.' % wo,
              titel('Jetzt du', 280, 86),
              n('Erkunde diese Zusammenhänge|%s unter dem Clip|und löse die Aufgaben.' % wo, 430, 'blau', 50, ein=0.6))


def hoehe(el):
    """Geschätzte Höhe einer Zeile der linken Spalte in px: hohe Brüche (\\dfrac) brauchen gut das Doppelte."""
    g, t = el.get('groesse', 50), el.get('text', '')
    if el['typ'] == 'notiz':
        return 1.35 * g * (t.count('|') + 1)
    if '\\dfrac' in t:
        return (2.45 if '\\left(' in t else 2.25) * g
    return 1.35 * g


def abstaende(szenen, luft=26):
    """Schiebt Zeilen der linken Spalte nach unten, bis keine die nächste berührt (pruef-clip meldete Überlapp)."""
    for q in szenen:
        zeilen = sorted((el for el in q['elemente'] if el['typ'] in ('formel', 'notiz', 'titel') and el.get('x') == LX
                         and 'aus' not in el),          # eine Zeile mit «aus» wird an derselben Stelle ersetzt
                        key=lambda el: el['y'])
        for a_, b_ in zip(zeilen, zeilen[1:]):
            unten = a_['y'] + hoehe(a_) + luft
            if b_['y'] < unten:
                b_['y'] = int(round(unten))
        if zeilen and zeilen[-1]['y'] + hoehe(zeilen[-1]) > 1020:
            print('  zu tief:', q['name'], zeilen[-1]['y'])


def clip(name, folge, titel_, kurz, schlag, szenen, fragen=None, art='Einfuehrungsclip'):
    dname = PRAEFIX + name
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
         'schlagworte': schlag, 'themenbereich': 'Arithmetik/Algebra · Terme und Faktorisieren',
         'fach': 'Sekundarstufe I', 'lerngebiet': '1 · Arithmetik/Algebra',
         'lektion': ['lp-terme'], 'stufe': ['Sek I'], 'datum': '2026-10-09',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Terme sehen', 'folge': folge,
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms terme-faktorisieren; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + dname + '.json', 'w'), ensure_ascii=False, indent=1)
    print(dname, len(szenen), 'Szenen', len(fragen or []), 'Fragen')




# ---------------------------------------------------------------- Bausteine der Bilder
XW, XH, U = 0.4, 2.0, 0.4          # x-Kachel (Streifen) 0.4 × 2.0, Einerkachel 0.4 × 0.4
SCHRITT, LUECKE = 0.55, 0.35


def kx(x, y, farbe=1, **kw):
    return RECHT(x, y, XW, XH, farbe, 0.35, dicke=2, **kw)


def k1(x, y, farbe=2, **kw):
    return RECHT(x, y, U, U, farbe, 0.35, dicke=2, **kw)


def reihe(x, y, nx, n1, fx=1, f1=2, **kw):
    """nx Streifen, dann n1 Einer, unten bündig bei y. Gibt (Figuren, Liste der x-Lagen der Einer) zurück."""
    figs, lagen = [], []
    for j in range(nx):
        figs.append(kx(x + j * SCHRITT, y, fx, **kw))
    x1 = x + nx * SCHRITT + (LUECKE if nx else 0)
    for j in range(n1):
        figs.append(k1(x1 + j * SCHRITT, y, f1, **kw))
        lagen.append(x1 + j * SCHRITT)
    return figs, lagen


def flaeche(a, b, X=4.5, E=0.75, x0=1.5, oben=9.2, namen=None):
    """Flächenmodell (x + a)(x + b), a ≥ 0 Zeilen unten, b ≥ 0 Spalten rechts. Teile als Wörterbuch."""
    u = oben - X
    q = [RECHT(x0, u, X, X, 1, 0.35, dicke=2)]
    xv = [RECHT(x0 + X + j * E, u, E, X, 1, 0.18, dicke=2) for j in range(b)]
    xh = [RECHT(x0, u - (k + 1) * E, X, E, 1, 0.18, dicke=2) for k in range(a)]
    ei = [RECHT(x0 + X + j * E, u - (k + 1) * E, E, E, 2, 0.35, dicke=2) for j in range(b) for k in range(a)]
    rahmen = [RECHT(x0, u - a * E, X + b * E, X + a * E, 5, 0, dicke=4)]
    seiten = [T(x0 + X / 2, oben + 0.35, 'x', 1), T(x0 - 0.45, u + X / 2 - 0.15, 'x', 1)]
    if b:
        seiten.append(T(x0 + X + b * E / 2, oben + 0.35, str(b), 2))
    if a:
        seiten.append(T(x0 - 0.45, u - a * E / 2 - 0.15, str(a), 2))
    linien = [S((x0 + X, oben), (x0 + X, u - a * E), 5, True, 2), S((x0, u), (x0 + X + b * E, u), 5, True, 2)]
    return dict(q=q, xv=xv, xh=xh, ei=ei, rahmen=rahmen, seiten=seiten, linien=linien,
                mitte=dict(q=(x0 + X / 2, u + X / 2), xv=(x0 + X + b * E / 2, u + X / 2), xh=(x0 + X / 2, u - a * E / 2),
                           ei=(x0 + X + b * E / 2, u - a * E / 2)))


def schema(oben_, links_, zellen, x0=1.0, top=9.0, bk=2.0, bz=3.0, hk=1.4, hz=2.0, farben=None):
    """Rechteckschema: Kopfzeile «·», oben_[0], oben_[1]; Kopfspalte links_; zellen[i][j] als Text.
    Gibt (Gitter mit Köpfen, Zellentexte [[…]], Zellenflächen [[…]]) zurück."""
    xs = [x0, x0 + bk, x0 + bk + bz, x0 + bk + 2 * bz]
    ys = [top, top - hk, top - hk - hz, top - hk - 2 * hz]
    gitter = [RECHT(xs[0], ys[3], xs[3] - xs[0], ys[0] - ys[3], 5, 0, dicke=3)]
    gitter += [S((xs[i], ys[0]), (xs[i], ys[3]), 5, dicke=2) for i in (1, 2)]
    gitter += [S((xs[0], ys[i]), (xs[3], ys[i]), 5, dicke=2) for i in (1, 2)]
    gitter.append(T((xs[0] + xs[1]) / 2, ys[0] - hk / 2 - 0.15, '·', 5, g=36))
    for j in range(2):
        gitter.append(T((xs[j + 1] + xs[j + 2]) / 2, ys[0] - hk / 2 - 0.15, oben_[j], 2 if j else 1, g=36))
        gitter.append(T((xs[0] + xs[1]) / 2, ys[j + 1] - hz / 2 - 0.15, links_[j], 2 if j else 1, g=36))
    texte, flaechen = [], []
    for i in range(2):
        zt, zf = [], []
        for j in range(2):
            f_ = (farben or [[1, 1], [1, 2]])[i][j]
            zf.append(RECHT(xs[j + 1], ys[i + 2], bz, hz, f_, 0.2, dicke=0))
            zt.append(T((xs[j + 1] + xs[j + 2]) / 2, ys[i + 1] - hz / 2 - 0.15, zellen[i][j], f_, g=40))
        texte.append(zt)
        flaechen.append(zf)
    return gitter, texte, flaechen


def quadrat(a, b, x0=1.5, oben=9.0, namen=('a', 'b'), werte=None):
    """Quadrat (a + b)²: a² blau oben links, zwei Rechtecke ab orange, b² grün unten rechts."""
    u = oben - a
    teile = dict(aa=RECHT(x0, u, a, a, 1, 0.35, dicke=2), ab1=RECHT(x0 + a, u, b, a, 2, 0.35, dicke=2),
                 ab2=RECHT(x0, u - b, a, b, 2, 0.35, dicke=2), bb=RECHT(x0 + a, u - b, b, b, 3, 0.35, dicke=2))
    rahmen = RECHT(x0, u - b, a + b, a + b, 5, 0, dicke=4)
    seiten = [T(x0 + a / 2, oben + 0.35, namen[0], 1), T(x0 + a + b / 2, oben + 0.35, namen[1], 2),
              T(x0 - 0.45, u + a / 2 - 0.15, namen[0], 1), T(x0 - 0.45, u - b / 2 - 0.15, namen[1], 2)]
    w = werte or ['a²', 'ab', 'ab', 'b²']
    texte = dict(aa=T(x0 + a / 2, u + a / 2 - 0.2, w[0], 1, g=40), ab1=T(x0 + a + b / 2, u + a / 2 - 0.2, w[1], 2, g=36),
                 ab2=T(x0 + a / 2, u - b / 2 - 0.2, w[2], 2, g=36), bb=T(x0 + a + b / 2, u - b / 2 - 0.2, w[3], 3, g=36))
    return teile, rahmen, seiten, texte


def gross(text, y=5.5, farbe=5, g=48):
    """Der gegebene Term gross im Bild (Kontrollfragen)."""
    return T(5, y, text, farbe, g=g)


# ════════════════════════════════════════════════ Kapitel 1 · Einführung: Terme vereinfachen
r1a, e1a = reihe(0.8, 7.0, 2, 4)
r1b, e1b = reihe(0.8, 4.0, 3, 1, f1=4)
r1c, _ = reihe(0.8, 0.8, 5, 3)
r_pl, _ = reihe(0.8, 6.0, 3, 2)
r_falsch, _ = reihe(0.8, 2.2, 5, 0, fx=4)
gruppen = []
for i, y in enumerate((7.2, 4.4, 1.6)):
    g_, _ = reihe(1.0, y, 2, 4, f1=4)
    gruppen.append([RECHT(0.75, y - 0.25, 4.45, 2.5, 5, 0, dicke=2)] + g_ + [T(7.4, y + 0.8, '2x − 4', 5, g=34)])
r_m1, _ = reihe(0.8, 7.0, 7, 0)
r_m2, _ = reihe(1.2, 3.8, 2, 5, f1=4)
r_m3, _ = reihe(1.2, 3.8, 2, 5, fx=4, f1=2)

clip('zusammenfassen', 1, 'Terme sehen: Terme vereinfachen',
     'Terme als Kacheln: x als Streifen, 1 als kleines Quadrat. Gleichartige Glieder zusammenfassen (2x + 4 + 3x − 1 = 5x + 3), '
     '3x + 2 ist nicht 5x, Zahl vor der Klammer (3(2x − 4) = 6x − 12), Minus vor der Klammer dreht jede Kachel um '
     '(7x − (2x − 5) = 5x + 5), verschachtelte Klammern von innen, Probe mit x = 2.',
     ['Term', 'zusammenfassen', 'gleichartige Glieder', 'Klammer', 'Minus vor der Klammer', 'Probe'], [
         sz('Kacheln',
            'Stell dir x als langen Streifen vor und die Zahl eins als kleines Quadrat. Dann besteht der Term zwei x plus vier '
            'aus zwei Streifen und vier kleinen Quadraten.',
            f(r'\fa{2x} + \fb{4}', 330, 86, ein='@Term'),
            n('@x@: langer Streifen|@1@: kleines Quadrat', 500, 'blau', 44, ein='@Streifen'),
            graf([kx(1.5, 6.5), T(3.0, 7.3, 'x', 1, g=40)], ein='@Streifen'),
            graf([k1(5.5, 6.5), T(6.6, 6.55, '1', 2, g=40)], ein='@Quadrat'),
            graf(reihe(1.5, 2.0, 2, 4)[0] + [T(7.6, 2.8, '2x + 4', 5, g=36)], ein='@Term')),
         sz('Zusammenfassen',
            'Kommt drei x minus eins dazu, legst du gleiche Kacheln zueinander. Die Streifen ergeben fünf x. Eine rote Kachel '
            'steht für minus eins, sie hebt ein kleines Quadrat auf. Es bleiben drei. Das Ergebnis: fünf x plus drei.',
            f(r'2x + 4 + 3x - 1', 300, 66, ein=0.5),
            f(r'= \fa{5x} + \fb{3}', 430, 66, ein='@Ergebnis'),
            n('gleiche Kacheln zueinander', 560, 'blau', 42, ein='@legst'),
            graf([mit(f_, aus='@bleiben') if i == len(r1a) - 1 else f_ for i, f_ in enumerate(r1a)]
                 + [T(7.6, 7.8, '2x + 4', 5, g=34)], ein=0.3),
            graf([mit(f_, aus='@bleiben') if i == len(r1b) - 1 else f_ for i, f_ in enumerate(r1b)]
                 + [T(7.6, 4.8, '3x − 1', 5, g=34)], ein=0.6),
            graf([KR((e1a[-1] + U / 2, 7.0 + U / 2), 0.42, 4, 0, 3, aus='@bleiben'),
                  KR((e1b[-1] + U / 2, 4.0 + U / 2), 0.42, 4, 0, 3, aus='@bleiben'),
                  S((e1a[-1] + U / 2, 6.6), (e1b[-1] + U / 2, 4.85), 4, True, 3, aus='@bleiben')], ein='@hebt'),
            graf(r1c[:5], ein='@ergeben'), graf(r1c[5:], ein='@bleiben'), graf([T(7.6, 1.6, '5x + 3', 3, g=36)], ein='@Ergebnis')),
         sz('Nicht gleichartig',
            'Streifen und kleine Quadrate lassen sich nicht zusammenzählen. Drei x plus zwei bleibt drei x plus zwei. '
            'Fünf x wäre falsch. Setz zur Probe x gleich zwei ein: Der Term ergibt acht, fünf x aber zehn.',
            f(r'3x + 2', 300, 76, ein=0.4),
            f(r'\fd{\neq 5x}', 430, 70, ein='@falsch'),
            f(r'x = 2: \quad 8 \neq 10', 560, 56, ein='@Probe'),
            graf(r_pl + [T(7.6, 6.8, '3x + 2', 5, g=36)], ein=0.3),
            graf(r_falsch + [T(7.6, 3.0, '5x', 4, g=36), S((0.6, 2.0), (3.8, 4.4), 4, False, 4)], ein='@falsch')),
         sz('Zahl vor der Klammer',
            'Drei mal die Klammer zwei x minus vier heisst: Die Klammer kommt dreimal vor. Das sind sechs Streifen und zwölf '
            'rote Kacheln, also sechs x minus zwölf. Die Drei wird mit jedem Glied in der Klammer multipliziert.',
            f(r'\fb{3}(2x - 4)', 300, 76, ein=0.4),
            f(r'= \fa{6x} \fd{- 12}', 430, 70, ein='@also'),
            n('die Zahl vor der Klammer|mal jedes Glied', 570, 'blau', 42, ein='@jedem'),
            graf(gruppen[0], ein='@kommt+0.3'), graf(gruppen[1], ein='@kommt+0.7'), graf(gruppen[2], ein='@kommt+1.1')),
         sz('Minus vor der Klammer',
            'Sieben x minus die Klammer zwei x minus fünf. Das Minus gilt für die ganze Klammer: Jede Kachel darin wird '
            'umgedreht. Aus zwei x wird minus zwei x, aus minus fünf wird plus fünf. Zwei rote Streifen heben zwei blaue auf. '
            'Es bleibt fünf x plus fünf.',
            f(r'7x - (2x - 5)', 300, 70, ein=0.05),
            f(r'= 7x \fd{- 2x} \fb{+ 5}', 430, 66, ein='@Aus'),
            f(r'= \fa{5x} + \fb{5}', 560, 66, ein='@bleibt'),
            graf([mit(f_, aus='@bleibt') if i < 2 else f_ for i, f_ in enumerate(r_m1)] + [T(6.0, 7.8, '7x', 5, g=34, aus='@bleibt')], ein=0.05),
            graf([T(0.75, 4.6, '−', 4, g=64, aus='@umgedreht+0.3'), RECHT(1.0, 3.55, 4.4, 2.5, 4, 0, dicke=3, gestrichelt=True, aus='@umgedreht+0.3')], ein=0.05),
            graf(alle(r_m2, aus='@umgedreht+0.3'), ein=0.05),
            graf([mit(f_, aus='@bleibt') if i < 2 else f_ for i, f_ in enumerate(r_m3)], ein='@umgedreht+0.3'),
            graf([T(6.8, 1.6, '5x + 5', 3, g=40)], ein='@bleibt')),
         sz('Verschachtelt',
            'Bei verschachtelten Klammern beginnst du innen. Innen steht minus drei mal die Klammer eins minus x, das gibt '
            'minus drei plus drei x. Die mittlere Klammer wird damit fünf x minus drei. Dann löst du die äussere Klammer auf: '
            'vier x minus fünf x plus drei, also drei minus x.',
            f(r'4x - (2x \fb{- 3(1 - x)})', 280, 58, ein=0.4),
            f(r'= 4x - (2x \fb{- 3 + 3x})', 390, 58, ein='@gibt'),
            f(r'= 4x - (5x - 3)', 500, 58, ein='@mittlere'),
            f(r'= 4x - 5x + 3 = \fc{3 - x}', 610, 58, ein='@äussere'),
            graf([RECHT(2.2, 3.0, 5.6, 2.2, 1, 0.15, dicke=3), T(5, 3.9, '1. innen: 1 − x', 1, g=34)], ein='@beginnst'),
            graf([RECHT(1.3, 2.2, 7.4, 4.8, 2, 0.06, dicke=3), T(5, 6.0, '2. Mitte: 2x − 3( … )', 2, g=34)], ein='@mittlere'),
            graf([RECHT(0.5, 1.2, 9.0, 7.6, 5, 0, dicke=3), T(5, 7.7, '3. aussen: 4x − ( … )', 5, g=34)], ein='@äussere')),
         sz('Probe',
            'Ob du richtig vereinfacht hast, prüfst du mit einer Zahl. Setz x gleich zwei ein. Sieben mal zwei minus die Klammer '
            'vier minus fünf gibt fünfzehn. Fünf mal zwei plus fünf gibt auch fünfzehn. So muss es sein.',
            f(r'x = 2', 280, 64, ein='@Setz'),
            f(r'7 \cdot 2 - (2 \cdot 2 - 5) = 14 + 1 = 15', 400, 54, ein='@Sieben'),
            f(r'5 \cdot 2 + 5 = 15', 520, 54, ein='@auch'),
            f(r'\fc{15 = 15}', 640, 64, ein='@muss'),
            graf([T(5, 6.5, '7x − (2x − 5)', 5, g=44), T(5, 4.6, '5x + 5', 3, g=44)], ein=0.3),
            graf([T(5, 2.6, 'x = 2:  15 und 15', 3, g=38)], ein='@auch')),
         sz('Merke',
            'Zum Mitnehmen: Nur gleichartige Glieder zusammenfassen. Die Zahl vor der Klammer mal jedes Glied. Ein Minus vor '
            'der Klammer dreht jedes Vorzeichen um. Verschachtelt: innen beginnen. Und am Schluss die Probe mit einer Zahl.',
            titel('Zum Mitnehmen', 250, 76),
            n('nur gleichartige Glieder zusammenfassen|Zahl vor der Klammer: mal jedes Glied|Minus vor der Klammer: '
              'jedes Vorzeichen um|verschachtelt: innen beginnen|Probe mit einer Zahl', 400, 'blau', 42, ein=1.2)),
         jetzt_du(),
     ], [
         wahl('Minus vor der Klammer', 'Was wird aus −5, wenn du in 7x − (2x − 5) die Klammer weglässt?',
              ['+5', '−5', '5x'], 0,
              {0: 'Ja.', 1: 'Das Minus vor der Klammer dreht jedes Vorzeichen in der Klammer um, auch das von −5.',
               2: 'Aus einer Zahl wird kein x-Glied. Nur das Vorzeichen ändert sich.'},
              sprich='Was wird aus minus fünf, wenn du die Klammer weglässt?',
              rueck_sprich={1: 'Das Minus vor der Klammer dreht jedes Vorzeichen in der Klammer um, auch das von minus fünf.',
                            2: 'Aus einer Zahl wird kein x-Glied. Nur das Vorzeichen ändert sich.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
k1f1a, _ = reihe(0.8, 6.0, 4, 7, f1=4)
k1f1b, _ = reihe(0.8, 2.6, 2, 3)
clip('kontrolle-zusammenfassen', 2, 'Terme sehen: Kontrollfragen zum Vereinfachen',
     'Fünf Fragen: 4y − 7 + 2y + 3 zusammenfassen, −(3x − 8), 5(2a − 3), ist 2x + 3x² dasselbe wie 5x³, x − (4 − 3x).',
     ['zusammenfassen', 'Klammer', 'Minus vor der Klammer', 'Kontrollfragen'], [
         sz('Frage 1',
            'Gleichartig sind vier y und zwei y, das gibt sechs y. Minus sieben plus drei gibt minus vier. Also sechs y minus vier.',
            f(r'4y + 2y = \fa{6y}', 300, 60, ein=1.0),
            f(r'-7 + 3 = \fd{-4}', 420, 60, ein=1.0),
            f(r'= \fc{6y - 4}', 540, 66, ein=1.0),
            graf(k1f1a + [T(5, 9.4, '4y − 7 + 2y + 3', 5, g=40)] + k1f1b, ein=0.05)),
         sz('Frage 2',
            'Das Minus vor der Klammer dreht jedes Vorzeichen um: Aus drei x wird minus drei x, aus minus acht wird plus acht.',
            f(r'-(3x - 8) = \fc{-3x + 8}', 320, 66, ein=1.0),
            graf([gross('−(3x − 8)')], ein=0.05)),
         sz('Frage 3',
            'Die Fünf wird mit beiden Gliedern multipliziert: fünf mal zwei a ist zehn a, fünf mal minus drei ist minus fünfzehn.',
            f(r'\fb{5} \cdot 2a + \fb{5} \cdot (-3)', 300, 60, ein=1.0),
            f(r'= \fc{10a - 15}', 430, 66, ein=1.0),
            graf([gross('5(2a − 3)')], ein=0.05)),
         sz('Frage 4',
            'Nein. Zwei x und drei x Quadrat sind nicht gleichartig, du kannst sie nicht zusammenfassen. Probe mit x gleich zwei: '
            'links vier plus zwölf, also sechzehn, rechts fünf mal acht, also vierzig.',
            f(r'x = 2: \quad 4 + 12 = 16', 300, 56, ein=1.0),
            f(r'5 \cdot 8 = 40 \quad \fd{16 \neq 40}', 420, 56, ein=1.0),
            graf([gross('2x + 3x²  =  5x³ ?')], ein=0.05)),
         sz('Frage 5',
            'Klammer weg, jedes Vorzeichen umdrehen: x minus vier plus drei x. Zusammengefasst vier x minus vier.',
            f(r'x - 4 + 3x', 300, 62, ein=1.0),
            f(r'= \fc{4x - 4}', 420, 66, ein=1.0),
            graf([gross('x − (4 − 3x)')], ein=0.05)),
         sz('Merke',
            'Zum Mitnehmen: Nur Gleichartiges zusammenfassen, die Zahl vor der Klammer mal jedes Glied, und ein Minus vor der '
            'Klammer dreht alle Vorzeichen um.',
            titel('Zum Mitnehmen', 250, 76),
            n('nur Gleichartiges zusammenfassen|Zahl vor der Klammer: mal jedes Glied|Minus vor der Klammer: alle Vorzeichen um',
              400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Fasse zusammen: 4y − 7 + 2y + 3', ['6y − 4', '2y', '6y − 10'], 0,
              {0: 'Ja.', 1: 'y-Glieder und Zahlen sind nicht gleichartig. Sie bleiben getrennt.',
               2: 'Achte auf das Vorzeichen: −7 + 3 = −4.'},
              sprich='Fasse zusammen: vier y minus sieben plus zwei y plus drei.',
              rueck_sprich={1: 'y-Glieder und Zahlen sind nicht gleichartig. Sie bleiben getrennt.',
                            2: 'Achte auf das Vorzeichen: minus sieben plus drei ist minus vier.'}),
         wahl('Frage 2', 'Löse die Klammer auf: −(3x − 8)', ['−3x + 8', '−3x − 8', '3x − 8'], 0,
              {0: 'Ja.', 1: 'Auch das Vorzeichen von −8 dreht sich um.', 2: 'Das Minus vor der Klammer gilt auch für 3x.'},
              sprich='Löse die Klammer auf: minus Klammer drei x minus acht.',
              rueck_sprich={1: 'Auch das Vorzeichen von minus acht dreht sich um.', 2: 'Das Minus vor der Klammer gilt auch für drei x.'}),
         wahl('Frage 3', 'Löse die Klammer auf: 5(2a − 3)', ['10a − 15', '10a − 3', '2a − 15'], 0,
              {0: 'Ja.', 1: 'Die 5 gilt auch für −3.', 2: 'Die 5 gilt auch für 2a.'},
              sprich='Löse die Klammer auf: fünf mal Klammer zwei a minus drei.',
              rueck_sprich={1: 'Die Fünf gilt auch für minus drei.', 2: 'Die Fünf gilt auch für zwei a.'}),
         wahl('Frage 4', 'Ist 2x + 3x² dasselbe wie 5x³?',
              ['Nein, 2x und 3x² sind nicht gleichartig.', 'Ja, 2 + 3 = 5 und die Hochzahlen werden addiert.', 'Ja, weil beide Glieder x enthalten.'], 0,
              {0: 'Ja.', 1: 'Beim Addieren bleibt die Hochzahl, und nur gleichartige Glieder lassen sich addieren. Probe mit x = 2: 16 gegen 40.',
               2: 'x und x² sind verschiedene Arten von Gliedern: Sie lassen sich nicht zusammenfassen.'},
              sprich='Ist zwei x plus drei x Quadrat dasselbe wie fünf x hoch drei?',
              rueck_sprich={1: 'Beim Addieren bleibt die Hochzahl, und nur gleichartige Glieder lassen sich addieren. Probe mit x gleich zwei: sechzehn gegen vierzig.',
                            2: 'x und x Quadrat sind verschiedene Arten von Gliedern: Sie lassen sich nicht zusammenfassen.'}),
         wahl('Frage 5', 'Vereinfache: x − (4 − 3x)', ['4x − 4', '−2x − 4', '4x + 4'], 0,
              {0: 'Ja.', 1: 'Das Minus vor der Klammer dreht auch −3x um: Es wird +3x.', 2: 'Die 4 in der Klammer wird zu −4.'},
              sprich='Vereinfache: x minus Klammer vier minus drei x.',
              rueck_sprich={1: 'Das Minus vor der Klammer dreht auch minus drei x um: Es wird plus drei x.',
                            2: 'Die Vier in der Klammer wird zu minus vier.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung: Klammer mal Klammer
F23 = flaeche(2, 3)
ux, uy = 1.5, 9.2 - 4.5          # Ecke des x-Quadrats unten links
SCH = schema(['3x', '−2'], ['x', '+4'], [['3x²', '−2x'], ['12x', '−8']], farben=[[1, 1], [1, 4]])
SCH2 = schema(['x', '−4'], ['x', '−3'], [['x²', '−4x'], ['−3x', '+12']], farben=[[1, 1], [1, 2]])

clip('ausmultiplizieren', 3, 'Terme sehen: Klammer mal Klammer',
     'Flächenmodell für (x + 2)(x + 3): vier Teilflächen x², 3x, 2x, 6; zusammengefasst x² + 5x + 6. Der Fehler x² + 6 '
     '(Streifen fehlen, Probe mit x = 1). Rechteckschema für (3x − 2)(x + 4) = 3x² + 10x − 8, Vorzeichen zur Zahl dahinter.',
     ['ausmultiplizieren', 'Klammer mal Klammer', 'Flächenmodell', 'Rechteckschema', 'Probe'], [
         sz('Rechteck',
            'Ein Rechteck hat die Seiten x plus drei und x plus zwei. Seine Fläche ist das Produkt der beiden Klammern.',
            f(r'(x + 2)(x + 3)', 330, 76, ein='@Fläche'),
            graf(F23['rahmen'] + [T(1.5 + 6.75 / 2, 9.6, 'x + 3', 5, g=36), T(0.9, 6.0, 'x + 2', 5, g=36, anker='end')], ein='@Seiten')),
         sz('Vier Teile',
            'Unterteile beide Seiten bei x. Es entstehen vier Teile: das Quadrat x Quadrat, ein Streifen mit drei x, ein '
            'Streifen mit zwei x und ein Rechteck aus sechs kleinen Quadraten.',
            f(r'(x + 2)(x + 3)', 280, 66, ein=0.05),
            f(r'= \fa{x^2} + \fa{3x} + \fa{2x} + \fb{6}', 400, 60, ein='@Quadraten'),
            graf(F23['rahmen'], ein=0.05),
            graf(F23['seiten'] + F23['linien'], ein='@Unterteile'),
            graf(F23['q'] + [T(*F23['mitte']['q'], 'x²', 1, g=44)], ein='@Quadrat'),
            graf(F23['xv'] + [T(*F23['mitte']['xv'], '3x', 1, g=36)], ein='@drei'),
            graf(F23['xh'] + [T(*F23['mitte']['xh'], '2x', 1, g=36)], ein='@zwei'),
            graf(F23['ei'] + [T(F23['mitte']['ei'][0], F23['mitte']['ei'][1] - 0.15, '6', 2, g=36)], ein='@sechs')),
         sz('Zusammenfassen',
            'Die beiden Streifen sind gleichartig: drei x plus zwei x gibt fünf x. Also ist Klammer x plus zwei mal Klammer x plus drei gleich '
            'x Quadrat plus fünf x plus sechs.',
            f(r'= x^2 + \fa{3x + 2x} + 6', 300, 60, ein=0.3),
            f(r'= \fc{x^2 + 5x + 6}', 430, 66, ein='@Also'),
            graf(F23['q'] + F23['xv'] + F23['xh'] + F23['ei'] + F23['rahmen'] + F23['seiten'], ein=0.05),
            graf([RECHT(6.0, 4.7, 2.25, 4.5, 3, 0, dicke=5), RECHT(1.5, 3.2, 4.5, 1.5, 3, 0, dicke=5)], ein='@gleichartig')),
         sz('Fehler',
            'Häufiger Fehler: nur vorne mal vorne und hinten mal hinten. Das gibt x Quadrat plus sechs. Im Bild fehlen dann die '
            'beiden Streifen. Probe mit x gleich zwei: vier mal fünf ist zwanzig, aber vier plus sechs ist nur zehn.',
            f(r'(x + 2)(x + 3) \fd{\neq x^2 + 6}', 300, 58, ein='@Das'),
            f(r'x = 2: \quad 4 \cdot 5 = 20, \quad 4 + 6 = \fd{10}', 440, 50, ein='@Probe'),
            graf(F23['q'] + F23['ei'] + F23['rahmen'] + F23['seiten'], ein=0.05),
            graf([RECHT(6.0, 4.7, 2.25, 4.5, 4, 0.12, dicke=3), RECHT(1.5, 3.2, 4.5, 1.5, 4, 0.12, dicke=3),
                  T(7.125, 6.8, 'fehlt', 4, g=30), T(3.75, 3.8, 'fehlt', 4, g=30)], ein='@Streifen')),
         sz('Rechteckschema',
            'Mit Minuszeichen gibt es kein Rechteck mehr. Das Rechteck-Schema funktioniert aber immer. Bei drei x minus zwei mal '
            'x plus vier schreibst du oben drei x und minus zwei, links x und plus vier. In jedes Feld kommt das Produkt.',
            f(r'(3x - 2)(x + 4)', 330, 70, ein=0.4),
            graf(SCH[0][:5], ein='@funktioniert'),
            graf([SCH[0][6], SCH[0][8]], ein='@oben'),
            graf([SCH[0][5], SCH[0][7], SCH[0][9]], ein='@links'),
            graf(SCH[2][0] + SCH[2][1] + SCH[1][0] + SCH[1][1], ein='@Feld')),
         sz('Ergebnis',
            'Die vier Produkte: drei x Quadrat, minus zwei x, zwölf x und minus acht. Das Vorzeichen gehört immer zur Zahl '
            'dahinter: minus zwei mal vier gibt minus acht. Zusammengefasst: drei x Quadrat plus zehn x minus acht.',
            f(r'= 3x^2 - 2x + 12x - 8', 300, 58, ein='@Produkte'),
            f(r'= \fc{3x^2 + 10x - 8}', 430, 62, ein='@Zusammengefasst'),
            n('das Vorzeichen gehört|zur Zahl dahinter', 560, 'orange', 42, ein='@Vorzeichen'),
            graf(SCH[0] + SCH[2][0] + SCH[2][1] + SCH[1][0] + SCH[1][1], ein=0.05),
            graf([RECHT(6.0, 3.6, 3.0, 2.0, 4, 0, dicke=5)], ein='@Vorzeichen')),
         sz('Merke',
            'Zum Mitnehmen: Jedes Glied der ersten Klammer mal jedes Glied der zweiten. Das gibt vier Produkte. Dann gleichartige '
            'Glieder zusammenfassen und mit einer Zahl die Probe machen.',
            titel('Zum Mitnehmen', 250, 76),
            n('jedes Glied mal jedes Glied: vier Produkte|gleichartige Glieder zusammenfassen|Probe mit einer Zahl', 400, 'blau', 44, ein=1.2)),
         jetzt_du(),
     ], [
         wahl('Vier Teile', 'In wie viele Teilflächen zerfällt das Rechteck, wenn du jede Seite bei x unterteilst?',
              ['4', '2', '6'], 0,
              {0: 'Ja.', 1: 'Jede Seite hat zwei Abschnitte. Zwei mal zwei Abschnitte geben mehr als zwei Felder.',
               2: 'Zähle nur die grossen Teilflächen, die durch das Unterteilen der beiden Seiten entstehen.'},
              sprich='In wie viele Teilflächen zerfällt das Rechteck, wenn du jede Seite bei x unterteilst?',
              rueck_sprich={1: 'Jede Seite hat zwei Abschnitte. Zwei mal zwei Abschnitte geben mehr als zwei Felder.',
                            2: 'Zähle nur die grossen Teilflächen, die durch das Unterteilen der beiden Seiten entstehen.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
F52 = flaeche(2, 5, X=4.0, E=0.75, x0=1.5, oben=9.0)
F61 = flaeche(1, 6, X=4.0, E=0.75, x0=1.2, oben=9.0)
clip('kontrolle-ausmultiplizieren', 4, 'Terme sehen: Kontrollfragen zum Ausmultiplizieren',
     'Fünf Fragen: (x + 6)(x + 1), die Zahl am Schluss von (x − 2)(x + 7), (2a + 1)(a − 4), ein Flächenmodell lesen, '
     'Probe mit x = 3.',
     ['ausmultiplizieren', 'Flächenmodell', 'Probe', 'Kontrollfragen'], [
         sz('Frage 1',
            'Vier Produkte: x Quadrat, x, sechs x und sechs. Zusammen x Quadrat plus sieben x plus sechs.',
            f(r'x^2 + x + 6x + 6', 300, 60, ein=1.0),
            f(r'= \fc{x^2 + 7x + 6}', 420, 66, ein=1.0),
            graf(F61['rahmen'] + [T(1.2 + 4.0 / 2 + 2.25, 9.4, 'x + 6', 5, g=36), T(0.9, 5.9, 'x + 1', 5, g=36, anker='end')], ein=0.05),
            graf(F61['q'] + F61['xv'] + F61['xh'] + F61['ei'] + F61['rahmen'], ein=1.0)),
         sz('Frage 2',
            'Die Zahl am Schluss ist das Produkt der beiden Zahlen: minus zwei mal sieben gibt minus vierzehn. Die Summe, fünf, '
            'gehört zum x-Glied: x Quadrat plus fünf x minus vierzehn.',
            f(r'(-2) \cdot 7 = \fc{-14}', 300, 62, ein=1.0),
            f(r'(x - 2)(x + 7) = x^2 + 5x - 14', 430, 54, ein=1.0),
            graf([gross('(x − 2)(x + 7)')], ein=0.05)),
         sz('Frage 3',
            'Zwei a mal a ist zwei a Quadrat, zwei a mal minus vier ist minus acht a, eins mal a ist a, eins mal minus vier ist '
            'minus vier. Zusammen: zwei a Quadrat minus sieben a minus vier.',
            f(r'2a^2 - 8a + a - 4', 300, 60, ein=1.0),
            f(r'= \fc{2a^2 - 7a - 4}', 420, 66, ein=1.0),
            graf([gross('(2a + 1)(a − 4)')], ein=0.05)),
         sz('Frage 4',
            'Ein x Quadrat, sieben Streifen und zehn Einer: x Quadrat plus sieben x plus zehn. Die Seiten sind x plus fünf und '
            'x plus zwei.',
            f(r'(x + 2)(x + 5) = \fc{x^2 + 7x + 10}', 320, 56, ein=1.0),
            graf(F52['q'] + F52['xv'] + F52['xh'] + F52['ei'] + F52['rahmen'], ein=0.05),
            graf(F52['seiten'], ein=1.0)),
         sz('Frage 5',
            'Links: Klammer drei plus zwei mal Klammer drei minus eins, also fünf mal zwei gleich zehn. Rechts: neun plus drei minus zwei, '
            'auch zehn. Die Probe stimmt.',
            f(r'(3 + 2)(3 - 1) = 5 \cdot 2 = 10', 300, 56, ein=1.0),
            f(r'9 + 3 - 2 = 10 \quad \fc{\checkmark}', 420, 56, ein=1.0),
            graf([gross('(x + 2)(x − 1)  =  x² + x − 2', 6.0, g=40), gross('x = 3', 4.2, 2, g=44)], ein=0.05)),
         sz('Merke',
            'Zum Mitnehmen: Jedes Glied mal jedes Glied, dann zusammenfassen. Bei Klammer x plus m mal Klammer x plus n ist die Zahl am Schluss das Produkt, das x-Glied die '
            'Summe. Und die Probe mit einer Zahl wie zwei zeigt viele Fehler. Nimm dafür nicht null oder eins.',
            titel('Zum Mitnehmen', 250, 76),
            n('jedes Glied mal jedes Glied|bei @(x + m)(x + n)@: Zahl am Schluss Produkt, x-Glied Summe|Probe mit einer Zahl wie @2@, nicht @0@ oder @1@', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Multipliziere aus: (x + 6)(x + 1)', ['x² + 7x + 6', 'x² + 6', 'x² + 6x + 7'], 0,
              {0: 'Ja.', 1: 'Es fehlen die gemischten Glieder x und 6x.', 2: 'Das x-Glied ist x + 6x, die Zahl am Schluss 6 · 1.'},
              sprich='Multipliziere aus: Klammer x plus sechs mal Klammer x plus eins.',
              rueck_sprich={1: 'Es fehlen die gemischten Glieder x und sechs x.', 2: 'Das x-Glied ist x plus sechs x, die Zahl am Schluss sechs mal eins.'}),
         wahl('Frage 2', 'Welche Zahl steht am Schluss, wenn du (x − 2)(x + 7) ausmultiplizierst?', ['−14', '14', '5'], 0,
              {0: 'Ja.', 1: 'Minus mal Plus gibt Minus.', 2: '−2 + 7 = 5 gehört zum x-Glied. Am Schluss steht das Produkt.'},
              sprich='Welche Zahl steht am Schluss, wenn du Klammer x minus zwei mal Klammer x plus sieben ausmultiplizierst?',
              rueck_sprich={1: 'Minus mal Plus gibt Minus.', 2: 'Minus zwei plus sieben gehört zum x-Glied. Am Schluss steht das Produkt.'}),
         wahl('Frage 3', 'Multipliziere aus: (2a + 1)(a − 4)', ['2a² − 7a − 4', '2a² − 4', '2a² + 9a − 4'], 0,
              {0: 'Ja.', 1: 'Es fehlen die gemischten Glieder −8a und a.', 2: 'Achte auf das Vorzeichen: 2a · (−4) = −8a.'},
              sprich='Multipliziere aus: Klammer zwei a plus eins mal Klammer a minus vier.',
              rueck_sprich={1: 'Es fehlen die gemischten Glieder minus acht a und a.', 2: 'Achte auf das Vorzeichen: zwei a mal minus vier ist minus acht a.'}),
         wahl('Frage 4', 'Welcher Term gehört zum Flächenmodell?', ['x² + 7x + 10', 'x² + 10', 'x² + 7x + 7'], 0,
              {0: 'Ja.', 1: 'Zähle auch die Streifen.', 2: 'Zähle die Einer unten rechts nochmals: Sie bilden ein Rechteck.'},
              sprich='Welcher Term gehört zum Flächenmodell?',
              rueck_sprich={1: 'Zähle auch die Streifen.', 2: 'Zähle die Einer unten rechts nochmals: Sie bilden ein Rechteck.'}),
         wahl('Frage 5', 'Probe mit x = 3: Was ergeben die beiden Seiten?', ['10 und 10', '10 und 8', '5 und 10'], 0,
              {0: 'Ja.', 1: 'Rechne rechts nochmals: 9 + 3 − 2.', 2: 'Links: (3 + 2)(3 − 1) = 5 · 2.'},
              sprich='Probe mit x gleich drei: Was ergeben die beiden Seiten?',
              rueck_sprich={1: 'Rechne rechts nochmals: neun plus drei minus zwei.', 2: 'Links: Klammer drei plus zwei mal Klammer drei minus eins, also fünf mal zwei.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung: Binomische Formeln
Q34 = quadrat(3, 4, x0=1.5, oben=9.0, namen=('3', '4'), werte=['9', '12', '12', '16'])
QAB = quadrat(5, 2.5, x0=1.5, oben=9.2)
QX4 = quadrat(5, 2.5, x0=1.5, oben=9.2, namen=('x', '4'), werte=['x²', '4x', '4x', '16'])
A7, B7 = 7.0, 2.5
QM = [RECHT(1.5, 1.5, A7, A7, 5, 0, dicke=0), RECHT(1.5, 1.5 + B7, A7 - B7, A7 - B7, 1, 0.35, dicke=2),
      RECHT(1.5 + A7 - B7, 1.5, B7, A7, 4, 0.1, dicke=3, gestrichelt=True), RECHT(1.5, 1.5, A7, B7, 4, 0.1, dicke=3, gestrichelt=True),
      RECHT(1.5 + A7 - B7, 1.5, B7, B7, 3, 0.4, dicke=2), RECHT(1.5, 1.5, A7, A7, 5, 0, dicke=4),
      T(1.5 + (A7 - B7) / 2, 1.5 + B7 + (A7 - B7) / 2 - 0.2, '(a − b)²', 1, g=36),
      T(1.5 + A7 - B7 / 2, 6.0, 'ab', 4, g=32), T(3.75, 1.5 + B7 / 2 - 0.2, 'ab', 4, g=32),
      T(1.5 + A7 - B7 / 2, 1.5 + B7 / 2 - 0.2, 'b²', 3, g=32),
      T(1.5 + A7 / 2, 8.85, 'a', 5), T(1.05, 5.0, 'a', 5), T(1.5 + A7 - B7 / 2, 8.85, 'b', 2), T(1.05, 1.5 + B7 / 2 - 0.15, 'b', 2)]
STUECK = [[1.0, 0.5], [4.0, 0.5], [4.0, 2.0], [1.0, 2.0]]
ZIEL = [[5.5, 5.0], [5.5, 2.0], [7.0, 2.0], [7.0, 5.0]]

clip('binome', 5, 'Terme sehen: Binomische Formeln',
     '(3 + 4)² = 49, aber 3² + 4² = 25: Es fehlen zwei Rechtecke. Das Quadrat (a + b)² = a² + 2ab + b²; mit x: '
     '(x + 4)² = x² + 8x + 16; (a − b)² und (2y − 3)² = 4y² − 12y + 9; (a + b)(a − b) = a² − b² als umgelegtes Rechteck; '
     'Kopfrechnen 51² und 49 · 51.',
     ['binomische Formeln', 'Quadrat', 'mittleres Glied', 'Kopfrechnen'], [
         sz('Zahlen',
            'Rechne nach: Sieben im Quadrat ist neunundvierzig. Drei Quadrat plus vier Quadrat ist neun plus sechzehn, also nur '
            'fünfundzwanzig. Es fehlen vierundzwanzig. Wo stecken sie?',
            f(r'(3 + 4)^2 \;\overset{?}{=}\; 3^2 + 4^2', 300, 60, ein=0.05),
            f(r'7^2 = 49', 430, 58, ein='@Sieben'),
            f(r'9 + 16 = 25', 540, 58, ein='@Drei'),
            f(r'\fd{49 - 25 = 24}', 650, 58, ein='@fehlen'),
            graf([Q34[1]] + Q34[2], ein='@Sieben'),
            graf([Q34[0]['aa'], Q34[0]['bb'], Q34[3]['aa'], Q34[3]['bb']], ein='@Drei'),
            graf([Q34[0]['ab1'], Q34[0]['ab2'], Q34[3]['ab1'], Q34[3]['ab2']], ein='@stecken')),
         sz('Quadrat',
            'Allgemein: Ein Quadrat mit der Seite a plus b besteht aus vier Teilen. Oben links a Quadrat, unten rechts b Quadrat '
            'und dazu zwei Rechtecke, jedes a mal b. Darum steht in der Mitte zwei a b.',
            f(r'(a + b)^2 = \fa{a^2} + \fb{2ab} + \fc{b^2}', 330, 62, ein='@Darum'),
            graf([QAB[1]] + QAB[2], ein=0.3),
            graf([QAB[0]['aa'], QAB[3]['aa']], ein='@links'),
            graf([QAB[0]['bb'], QAB[3]['bb']], ein='@rechts'),
            graf([QAB[0]['ab1'], QAB[0]['ab2'], QAB[3]['ab1'], QAB[3]['ab2']], ein='@Rechtecke')),
         sz('Mit x',
            'Für a und b darf auch x und eine Zahl stehen. Klammer x plus vier im Quadrat: x Quadrat, dann zwei mal x mal vier, also '
            'acht x, und am Schluss vier Quadrat, also sechzehn.',
            f(r'(x + 4)^2', 280, 64, ein=0.3),
            f(r'= x^2 + 2 \cdot x \cdot 4 + 4^2', 400, 58, ein='@dann'),
            f(r'= \fc{x^2 + 8x + 16}', 520, 62, ein='@Schluss'),
            graf([QX4[1]] + QX4[2] + list(QX4[0].values()) + list(QX4[3].values()), ein=0.3)),
         sz('Minus',
            'Mit Minus ändert sich nur das mittlere Glied: Klammer a minus b im Quadrat ist a Quadrat minus zwei a b plus b Quadrat. '
            'Im Bild nimmst du vom Quadrat a Quadrat zwei Streifen a b weg. Das Eckquadrat b Quadrat war dabei doppelt weg, darum '
            'kommt es einmal dazu. Bei Klammer zwei y minus drei im Quadrat wird auch die Zwei quadriert: vier y Quadrat minus '
            'zwölf y plus neun.',
            f(r'(a - b)^2 = a^2 \fd{- 2ab} + b^2', 280, 58, ein='@mittlere'),
            f(r'(2y - 3)^2 = \fb{4}y^2 - 12y + 9', 420, 58, ein='@quadriert'),
            n('@(2y)^2 = 4y^2@, nicht @2y^2@', 560, 'orange', 42, ein='@quadriert+0.8'),
            graf(QM, ein='@Bild')),
         sz('Dritte Formel',
            'Die dritte Formel: Klammer a plus b mal Klammer a minus b ist a Quadrat minus b Quadrat. Die beiden gemischten Glieder heben sich '
            'auf. Zum Beispiel ist Klammer fünf plus x mal Klammer fünf minus x gleich fünfundzwanzig minus x Quadrat. Im Bild fehlt beim '
            'Quadrat a Quadrat die Ecke b Quadrat. Das orange Stück legst du rechts an, und es entsteht ein Rechteck mit den '
            'Seiten a plus b und a minus b.',
            f(r'(a + b)(a - b) = a^2 - b^2', 280, 58, ein='@dritte'),
            f(r'(5 + x)(5 - x) = 25 - x^2', 400, 56, ein='@Beispiel'),
            graf([RECHT(1.0, 2.0, 4.5, 3.0, 1, 0.35, dicke=2), RECHT(1.0, 0.5, 4.5, 4.5, 5, 0, dicke=3, aus='@Rechteck'),
                  T(3.25, 5.3, 'a', 5, aus='@Rechteck'), T(0.6, 2.6, 'a', 5, aus='@Rechteck')], ein='@Bild'),
            graf([RECHT(4.0, 0.5, 1.5, 1.5, 4, 0.12, dicke=3, gestrichelt=True), T(4.75, 1.0, 'b²', 4, g=30)], ein='@Ecke'),
            graf([mit(V(STUECK, 2, 0.4, dicke=2), bewegung=[['@legst', {}], ['@legst+1.4', {'punkte': ZIEL}]])], ein='@Bild'),
            graf([RECHT(1.0, 2.0, 6.0, 3.0, 5, 0, dicke=4),
                  T(4.0, 5.3, 'a + b', 5, g=32), T(7.3, 3.4, 'a − b', 5, g=32, anker='start')], ein='@Rechteck')),
         sz('Kopfrechnen',
            'Die Formeln helfen auch beim Kopfrechnen. Einundfünfzig im Quadrat ist Klammer fünfzig plus eins im Quadrat: '
            'zweitausend fünfhundert plus hundert plus eins, also zweitausend sechshundert eins. Und neunundvierzig mal '
            'einundfünfzig ist fünfzig Quadrat minus eins: zweitausend vierhundert neunundneunzig.',
            f(r'51^2 = (50 + 1)^2 = 2500 + 100 + 1 = \fc{2601}', 330, 52, ein='@Einundfünfzig'),
            f(r'49 \cdot 51 = (50 - 1)(50 + 1) = 2500 - 1 = \fc{2499}', 480, 52, ein='@neunundvierzig')),
         sz('Merke',
            'Zum Mitnehmen: Klammer a plus b im Quadrat ist a Quadrat plus zwei a b plus b Quadrat, mit Minus wird nur das mittlere Glied '
            'negativ. Klammer a plus b mal Klammer a minus b ist a Quadrat minus b Quadrat. Nie das mittlere Glied vergessen.',
            titel('Zum Mitnehmen', 250, 76),
            f(r'(a + b)^2 = a^2 + 2ab + b^2', 400, 52, ein=1.2),
            f(r'(a - b)^2 = a^2 - 2ab + b^2', 500, 52, ein=1.6),
            f(r'(a + b)(a - b) = a^2 - b^2', 600, 52, ein=2.0)),
         jetzt_du(),
     ], [
         wahl('Zahlen', 'Ist (3 + 4)² dasselbe wie 3² + 4²?', ['Nein', 'Ja, man darf jede Zahl einzeln quadrieren.', 'Ja, beides ist 49.'], 0,
              {0: 'Richtig: Es ist nicht dasselbe.', 1: 'Rechne nach: (3 + 4)² = 7² = 49, aber 3² + 4² = 9 + 16 = 25.',
               2: '3² + 4² = 9 + 16 = 25, nicht 49.'},
              sprich='Ist drei plus vier im Quadrat dasselbe wie drei Quadrat plus vier Quadrat?',
              rueck_sprich={0: 'Richtig: Es ist nicht dasselbe.', 1: 'Rechne nach: Sieben im Quadrat ist neunundvierzig, aber neun plus sechzehn ist fünfundzwanzig.',
                            2: 'Drei Quadrat plus vier Quadrat ist neun plus sechzehn, also fünfundzwanzig.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
Q91 = quadrat(5, 3, x0=1.5, oben=9.0, namen=('x', '9'), werte=['', '', '', ''])
clip('kontrolle-binome', 6, 'Terme sehen: Kontrollfragen zu den binomischen Formeln',
     'Fünf Fragen: (x + 9)², (y − 6)², (2x + 5)(2x − 5), (3y)², 41² im Kopf.',
     ['binomische Formeln', 'Kopfrechnen', 'Kontrollfragen'], [
         sz('Frage 1',
            'Erste Formel: x Quadrat plus zwei mal x mal neun plus neun Quadrat, also x Quadrat plus achtzehn x plus einundachtzig.',
            f(r'x^2 + 2 \cdot x \cdot 9 + 9^2', 300, 58, ein=1.0),
            f(r'= \fc{x^2 + 18x + 81}', 420, 64, ein=1.0),
            graf([Q91[1]] + Q91[2] + [gross('(x + 9)²', 0.4, 5, 40)], ein=0.05),
            graf([Q91[0]['aa'], Q91[0]['ab1'], Q91[0]['ab2'], Q91[0]['bb'],
                  T(4.0, 6.3, 'x²', 1, g=40), T(8.0, 6.3, '9x', 2, g=34), T(4.0, 2.3, '9x', 2, g=34), T(8.0, 2.3, '81', 3, g=34)], ein=1.0)),
         sz('Frage 2',
            'Zweite Formel: y Quadrat minus zwölf y plus sechsunddreissig. Am Schluss steht plus, weil minus sechs mal minus sechs '
            'positiv ist.',
            f(r'(y - 6)^2 = y^2 - 2 \cdot y \cdot 6 + 6^2', 300, 54, ein=1.0),
            f(r'= \fc{y^2 - 12y + 36}', 420, 64, ein=1.0),
            graf([gross('(y − 6)²')], ein=0.05)),
         sz('Frage 3',
            'Dritte Formel: zwei x im Quadrat minus fünf im Quadrat, also vier x Quadrat minus fünfundzwanzig.',
            f(r'(2x)^2 - 5^2', 300, 60, ein=1.0),
            f(r'= \fc{4x^2 - 25}', 420, 64, ein=1.0),
            graf([gross('(2x + 5)(2x − 5)')], ein=0.05)),
         sz('Frage 4',
            'Drei y mal drei y: drei mal drei ist neun, y mal y ist y Quadrat. Also neun y Quadrat.',
            f(r'3y \cdot 3y = \fc{9y^2}', 320, 66, ein=1.0),
            graf([gross('(3y)²')], ein=0.05)),
         sz('Frage 5',
            'Einundvierzig ist vierzig plus eins. Vierzig Quadrat ist sechzehnhundert, das mittlere Glied zwei mal vierzig mal '
            'eins ist achtzig, dazu eins. Zusammen sechzehnhunderteinundachtzig.',
            f(r'(40 + 1)^2 = 1600 + 80 + 1', 300, 56, ein=1.0),
            f(r'= \fc{1681}', 420, 64, ein=1.0),
            graf([gross('41²')], ein=0.05)),
         sz('Merke',
            'Zum Mitnehmen: Bei Klammer a plus b im Quadrat und Klammer a minus b im Quadrat nie das mittlere Glied vergessen. Bei Klammer a plus b mal '
            'Klammer a minus b fällt es weg. Und eine Zahl vor der Variable wird mitquadriert.',
            titel('Zum Mitnehmen', 250, 76),
            n('mittleres Glied @2ab@ nie vergessen|@(a + b)(a - b)@: kein mittleres Glied|Zahl vor der Variable mitquadrieren',
              400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Rechne: (x + 9)²', ['x² + 18x + 81', 'x² + 81', 'x² + 9x + 81'], 0,
              {0: 'Ja.', 1: 'Das mittlere Glied fehlt.', 2: 'Das mittlere Glied ist 2ab, also zweimal 9x.'},
              sprich='Rechne: Klammer x plus neun im Quadrat.',
              rueck_sprich={1: 'Das mittlere Glied fehlt.', 2: 'Das mittlere Glied ist zwei a b, also zweimal neun x.'}),
         wahl('Frage 2', 'Rechne: (y − 6)²', ['y² − 12y + 36', 'y² − 36', 'y² + 12y + 36'], 0,
              {0: 'Ja.', 1: 'Hier steht ein Quadrat einer Klammer. Es gibt ein mittleres Glied.', 2: 'Bei (a − b)² ist das mittlere Glied negativ.'},
              sprich='Rechne: Klammer y minus sechs im Quadrat.',
              rueck_sprich={1: 'Hier steht ein Quadrat einer Klammer. Es gibt ein mittleres Glied.',
                            2: 'Bei Klammer a minus b im Quadrat ist das mittlere Glied negativ.'}),
         wahl('Frage 3', 'Rechne: (2x + 5)(2x − 5)', ['4x² − 25', '2x² − 25', '4x² − 20x − 25'], 0,
              {0: 'Ja.', 1: 'Auch die 2 wird quadriert: (2x)² = 4x².', 2: 'Die gemischten Glieder +10x und −10x heben sich auf.'},
              sprich='Rechne: Klammer zwei x plus fünf mal Klammer zwei x minus fünf.',
              rueck_sprich={1: 'Auch die Zwei wird quadriert: zwei x im Quadrat ist vier x Quadrat.',
                            2: 'Die gemischten Glieder plus zehn x und minus zehn x heben sich auf.'}),
         wahl('Frage 4', 'Was ist (3y)²?', ['9y²', '3y²', '6y'], 0,
              {0: 'Ja.', 1: 'Auch die 3 wird quadriert: 3y · 3y.', 2: 'Quadrieren heisst mal sich selbst, nicht mal 2.'},
              sprich='Was ist drei y im Quadrat?',
              rueck_sprich={1: 'Auch die Drei wird quadriert: drei y mal drei y.', 2: 'Quadrieren heisst mal sich selbst, nicht mal zwei.'}),
         wahl('Frage 5', 'Rechne im Kopf: 41²', ['1681', '1601', '1641'], 0,
              {0: 'Ja.', 1: 'Es fehlt das mittlere Glied 2 · 40 · 1.', 2: 'Das mittlere Glied ist 2 · 40 · 1, also 80.'},
              sprich='Rechne im Kopf: einundvierzig im Quadrat.',
              rueck_sprich={1: 'Es fehlt das mittlere Glied zwei mal vierzig mal eins.', 2: 'Das mittlere Glied ist zwei mal vierzig mal eins, also achtzig.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung: Faktorisieren
PAARE = [('1 · 12', '13'), ('2 · 6', '8'), ('3 · 4', '7'), ('(−1) · (−12)', '−13'), ('(−2) · (−6)', '−8'), ('(−3) · (−4)', '−7')]
def paarzeile(i):
    y = 7.9 - 1.05 * i
    return [T(3.2, y, PAARE[i][0], 2 if i < 3 else 4, g=36), T(7.4, y, PAARE[i][1], 5, g=36)]

clip('faktorisieren', 7, 'Terme sehen: Faktorisieren',
     'Faktorisieren als Ausmultiplizieren rückwärts; ausklammern (6a² − 9a = 3a(2a − 3)), binomische Formeln rückwärts '
     '(y² − 10y + 25, 9y² − 25), Zweiklammersatz mit Paartabelle (x² − 7x + 12 = (x − 3)(x − 4)), Probe, kein '
     'Gleichungslösen (x² − 25), vollständig faktorisieren (5x² − 20).',
     ['faktorisieren', 'ausklammern', 'binomische Formeln', 'Zweiklammersatz', 'vollständig'], [
         sz('Rückwärts',
            'Faktorisieren heisst: eine Summe als Produkt schreiben. Es ist das Ausmultiplizieren rückwärts. Aus x Quadrat plus '
            'fünf x plus sechs wird wieder Klammer x plus zwei mal Klammer x plus drei.',
            f(r'x^2 + 5x + 6', 300, 66, ein='@Summe'),
            f(r'= \fc{(x + 2)(x + 3)}', 430, 66, ein='@wieder'),
            n('Summe → Produkt', 570, 'blau', 44, ein='@Produkt'),
            graf(F23['q'] + F23['xv'] + F23['xh'] + F23['ei'] + F23['rahmen'], ein='@rückwärts'),
            graf([T(1.5 + 6.75 / 2, 9.6, 'x + 3', 3, g=38), T(0.9, 6.0, 'x + 2', 3, g=38, anker='end')], ein='@wieder')),
         sz('Ausklammern',
            'Zuerst suchst du einen gemeinsamen Faktor. In sechs a Quadrat und in neun a steckt beide Male drei a. Klammere ihn '
            'aus: drei a mal die Klammer zwei a minus drei. Nur a auszuklammern reicht nicht: In sechs a minus neun steckt noch '
            'die Drei.',
            f(r'6a^2 - 9a', 280, 64, ein=0.3),
            f(r'= \fb{3a} \cdot 2a - \fb{3a} \cdot 3', 390, 58, ein='@steckt'),
            f(r'= \fc{\fb{3a}(2a - 3)}', 500, 62, ein='@Klammere'),
            f(r'\fd{a(6a - 9)}: \text{ nicht fertig}', 620, 52, ein='@reicht'),
            graf([T(5, 7.4, 'ggT(6; 9) = 3', 2, g=42)], ein='@steckt'),
            graf([T(5, 5.6, 'in beiden Gliedern: a', 1, g=40)], ein='@steckt+0.8'),
            graf([T(5, 3.8, 'gemeinsam: 3a', 2, g=46)], ein='@Klammere')),
         sz('Binomisch rückwärts',
            'Dann prüfst du, ob eine binomische Formel passt. Bei y Quadrat minus zehn y plus fünfundzwanzig ist fünfundzwanzig '
            'gleich fünf im Quadrat und zehn y gleich zwei mal y mal fünf. Also Klammer y minus fünf im Quadrat. Neun y Quadrat minus '
            'fünfundzwanzig sind zwei Quadrate mit Minus dazwischen: Klammer drei y minus fünf mal Klammer drei y plus fünf.',
            f(r'y^2 - 10y + 25', 280, 56, ein='@Bei'),
            n(r'@25 = 5^2@, @10y = 2 \cdot y \cdot 5@', 380, 'orange', 40, ein='@gleich'),
            f(r'= \fc{(y - 5)^2}', 460, 56, ein='@Also'),
            f(r'9y^2 - 25', 580, 56, ein='@Neun'),
            f(r'= \fc{(3y - 5)(3y + 5)}', 680, 56, ein='@dazwischen'),
            graf([T(5, 7.4, 'a² − 2ab + b² = (a − b)²', 1, g=36)], ein='@binomische'),
            graf([T(5, 4.4, 'a² − b² = (a + b)(a − b)', 1, g=36)], ein='@Quadrate')),
         sz('Zweiklammersatz',
            'Schreib die Zahlenpaare mit dem Produkt zwölf auf: eins und zwölf, zwei und sechs, drei und vier, und dieselben '
            'negativ. Die Summe minus sieben haben nur minus drei und minus vier. Also Klammer x minus drei mal Klammer x minus vier.',
            f(r'x^2 \fa{- 7}x \fb{+ 12}', 300, 66, ein=0.05),
            n('Produkt @12@, Summe @-7@', 430, 'orange', 44, ein=0.05),
            f(r'= \fc{(x - 3)(x - 4)}', 560, 66, ein='@Also'),
            graf([T(3.2, 9.1, 'Produkt 12', 5, g=34), T(7.4, 9.1, 'Summe', 5, g=34), S((0.8, 8.65), (9.2, 8.65), 5, dicke=2)], ein='@Zahlenpaare'),
            graf(paarzeile(0), ein='@eins'), graf(paarzeile(1), ein='@zwei'), graf(paarzeile(2), ein='@drei'),
            graf(paarzeile(3) + paarzeile(4) + paarzeile(5), ein='@negativ'),
            graf([RECHT(0.8, 7.9 - 1.05 * 5 - 0.35, 8.4, 0.95, 3, 0.15, dicke=4)], ein='@nur')),
         sz('Probe',
            'Prüfe, indem du ausmultiplizierst: x Quadrat minus vier x minus drei x plus zwölf, also wieder x Quadrat minus sieben x '
            'plus zwölf.',
            f(r'(x - 3)(x - 4) = x^2 - 4x - 3x + 12', 300, 52, ein='@Prüfe'),
            f(r'= \fc{x^2 - 7x + 12}', 420, 62, ein='@wieder'),
            graf(SCH2[0] + SCH2[2][0] + SCH2[2][1] + SCH2[1][0] + SCH2[1][1], ein='@Prüfe')),
         sz('Kein Gleichungslösen',
            'Achtung: Faktorisieren ist kein Gleichungslösen. Bei der Aufgabe, x Quadrat minus fünfundzwanzig zu faktorisieren, '
            'ist die Antwort ein Produkt: Klammer x minus fünf mal Klammer x plus fünf. Ein Ergebnis wie x gleich fünf beantwortet eine andere Frage.',
            f(r'x^2 - 25 = \fc{(x - 5)(x + 5)}', 320, 60, ein='@Antwort'),
            f(r'\fd{x = 5}: \text{ eine andere Frage}', 460, 52, ein='@Ergebnis')),
         sz('Vollständig',
            'Vollständig faktorisiert ist ein Term erst, wenn sich kein Faktor mehr mit ganzen Zahlen zerlegen lässt. Fünf x Quadrat minus zwanzig: '
            'zuerst fünf ausklammern, dann bleibt x Quadrat minus vier, und das ist Klammer x minus zwei mal Klammer x plus zwei.',
            f(r'5x^2 - 20 = \fb{5}(x^2 - 4)', 300, 58, ein='@ausklammern'),
            f(r'= \fc{5(x - 2)(x + 2)}', 420, 62, ein='@bleibt')),
         sz('Merke',
            'Zum Mitnehmen: Faktorisieren macht aus einer Summe ein Produkt. Zuerst ausklammern, dann eine binomische Formel '
            'prüfen, dann der Zweiklammersatz mit Produkt und Summe. Vollständig faktorisieren und am Schluss ausmultiplizieren, als Probe.',
            titel('Zum Mitnehmen', 250, 76),
            n('1. ausklammern|2. binomische Formel rückwärts|3. Zweiklammersatz: Produkt und Summe|vollständig, dann Probe',
              400, 'blau', 44, ein=1.2)),
         jetzt_du(),
     ], [
         wahl('Zweiklammersatz', 'x² − 7x + 12: Welche zwei Zahlen haben das Produkt 12 und die Summe −7?',
              ['−3 und −4', '3 und 4', '−2 und −6'], 0,
              {0: 'Ja.', 1: '3 · 4 = 12 stimmt, aber 3 + 4 = +7, nicht −7.', 2: '(−2) · (−6) = 12 stimmt, aber die Summe ist −8.'},
              sprich='x Quadrat minus sieben x plus zwölf: Welche zwei Zahlen haben das Produkt zwölf und die Summe minus sieben?',
              rueck_sprich={1: 'Drei mal vier ist zwölf, aber drei plus vier ist plus sieben, nicht minus sieben.',
                            2: 'Minus zwei mal minus sechs ist zwölf, aber die Summe ist minus acht.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
clip('kontrolle-faktorisieren', 8, 'Terme sehen: Kontrollfragen zum Faktorisieren',
     'Fünf Fragen: 14x − 21 ausklammern, x² − 81, x² + 10x + 25, x² + x − 12, ist 5a(a + 2) + 1 faktorisiert?',
     ['faktorisieren', 'ausklammern', 'Zweiklammersatz', 'Kontrollfragen'], [
         sz('Frage 1',
            'Der grösste gemeinsame Teiler von vierzehn und einundzwanzig ist sieben. Vierzehn x durch sieben ist zwei x, '
            'einundzwanzig durch sieben ist drei: sieben mal die Klammer zwei x minus drei.',
            f(r'\text{ggT}(14;\ 21) = \fb{7}', 300, 56, ein=1.0),
            f(r'14x - 21 = \fc{\fb{7}(2x - 3)}', 420, 60, ein=1.0),
            graf([gross('14x − 21')], ein=0.05)),
         sz('Frage 2',
            'Zwei Quadrate mit Minus dazwischen: x Quadrat und neun Quadrat. Dritte Formel rückwärts: Klammer x minus neun mal Klammer x plus neun.',
            f(r'x^2 - 9^2 = \fc{(x - 9)(x + 9)}', 320, 60, ein=1.0),
            graf([gross('x² − 81')], ein=0.05)),
         sz('Frage 3',
            'Fünfundzwanzig ist fünf Quadrat, und zehn x ist zwei mal x mal fünf. Erste Formel rückwärts: Klammer x plus fünf im Quadrat.',
            f(r'25 = 5^2, \quad 10x = 2 \cdot x \cdot 5', 300, 54, ein=1.0),
            f(r'x^2 + 10x + 25 = \fc{(x + 5)^2}', 420, 60, ein=1.0),
            graf([gross('x² + 10x + 25')], ein=0.05)),
         sz('Frage 4',
            'Gesucht: Produkt minus zwölf, Summe plus eins. Vier und minus drei: Vier mal minus drei ist minus zwölf, vier '
            'minus drei ist eins. Also Klammer x plus vier mal Klammer x minus drei.',
            f(r'4 \cdot (-3) = -12, \quad 4 + (-3) = 1', 300, 54, ein=1.0),
            f(r'x^2 + x - 12 = \fc{(x + 4)(x - 3)}', 420, 60, ein=1.0),
            graf([gross('x² + x − 12')], ein=0.05)),
         sz('Frage 5',
            'Nein. Zuletzt wird plus eins gerechnet, also ist der ganze Term eine Summe. Faktorisiert ist ein Term erst, wenn er '
            'als Ganzes ein Produkt ist.',
            f(r'5a(a + 2) \fd{+ 1}', 320, 64, ein=1.0),
            n('zuletzt @+@: eine Summe', 460, 'orange', 44, ein=1.0),
            graf([gross('5a(a + 2) + 1')], ein=0.05)),
         sz('Merke',
            'Zum Mitnehmen: Zuerst ausklammern, dann binomische Formeln prüfen, dann Produkt und Summe suchen. Am Ende muss ein '
            'Produkt stehen. Ob es stimmt, zeigt die Probe: wieder ausmultiplizieren.',
            titel('Zum Mitnehmen', 250, 76),
            n('ausklammern, binomisch, Zweiklammersatz|am Ende ein Produkt|Probe durch Ausmultiplizieren', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Klammere aus: 14x − 21', ['7(2x − 3)', '7(2x − 21)', '2(7x − 10)'], 0,
              {0: 'Ja.', 1: 'Multipliziere zur Probe aus: 7 · 21 ist nicht 21.', 2: 'Ausmultipliziert gibt das 14x − 20.'},
              sprich='Klammere aus: vierzehn x minus einundzwanzig.',
              rueck_sprich={1: 'Multipliziere zur Probe aus: sieben mal einundzwanzig ist nicht einundzwanzig.',
                            2: 'Ausmultipliziert gibt das vierzehn x minus zwanzig.'}),
         wahl('Frage 2', 'Faktorisiere: x² − 81', ['(x − 9)(x + 9)', '(x − 9)²', '(x − 81)(x + 1)'], 0,
              {0: 'Ja.', 1: '(x − 9)² hat ein mittleres Glied −18x. Hier fehlt es.', 2: 'Ausmultipliziert gibt das x² − 80x − 81.'},
              sprich='Faktorisiere: x Quadrat minus einundachtzig.',
              rueck_sprich={1: 'Klammer x minus neun im Quadrat hat ein mittleres Glied, minus achtzehn x. Hier fehlt es.',
                            2: 'Ausmultipliziert gibt das x Quadrat minus achtzig x minus einundachtzig.'}),
         wahl('Frage 3', 'Faktorisiere: x² + 10x + 25', ['(x + 5)²', '(x + 5)(x − 5)', '(x + 10)(x + 25)'], 0,
              {0: 'Ja.', 1: '(x + 5)(x − 5) = x² − 25. Hier gibt es ein mittleres Glied.', 2: 'Ausmultipliziert gibt das x² + 35x + 250.'},
              sprich='Faktorisiere: x Quadrat plus zehn x plus fünfundzwanzig.',
              rueck_sprich={1: 'Klammer x plus fünf mal Klammer x minus fünf ist x Quadrat minus fünfundzwanzig. Hier gibt es ein mittleres Glied.',
                            2: 'Ausmultipliziert gibt das x Quadrat plus fünfunddreissig x plus zweihundertfünfzig.'}),
         wahl('Frage 4', 'Faktorisiere: x² + x − 12', ['(x + 4)(x − 3)', '(x − 4)(x + 3)', '(x + 6)(x − 2)'], 0,
              {0: 'Ja.', 1: 'Das Produkt stimmt, aber −4 + 3 = −1, nicht +1.', 2: '6 · (−2) = −12 stimmt, aber 6 + (−2) = 4.'},
              sprich='Faktorisiere: x Quadrat plus x minus zwölf.',
              rueck_sprich={1: 'Das Produkt stimmt, aber minus vier plus drei ist minus eins, nicht plus eins.',
                            2: 'Sechs mal minus zwei ist minus zwölf, aber sechs minus zwei ist vier.'}),
         wahl('Frage 5', 'Ist 5a(a + 2) + 1 faktorisiert?', ['Nein, es ist eine Summe.', 'Ja, es kommen Klammern vor.', 'Ja, 5a ist ausgeklammert.'], 0,
              {0: 'Ja.', 1: 'Am Schluss steht + 1: Der ganze Term ist eine Summe, kein Produkt.',
               2: 'Der Faktor 5a gilt nur für das erste Glied. Das + 1 steht ausserhalb.'},
              sprich='Ist fünf a mal Klammer a plus zwei, plus eins, faktorisiert?',
              rueck_sprich={1: 'Am Schluss steht plus eins: Der ganze Term ist eine Summe, kein Produkt.',
                            2: 'Der Faktor fünf a gilt nur für das erste Glied. Das plus eins steht ausserhalb.'}),
     ], art='Kontrollclip')

if FEHLT:
    print('ohne gemessene Wortzeit (geschätzt):', len(FEHLT))
