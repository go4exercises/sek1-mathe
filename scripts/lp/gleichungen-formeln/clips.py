"""Erzeugt die acht Drehbücher des Leitprogramms «Bruchterme, Gleichungen und Formeln» (10.10.2026).

  python3 scripts/lp/gleichungen-formeln/clips.py

Gerüst und Zeitlogik aus scripts/lp/terme-faktorisieren/clips.py: Je Kapitel ein Einführungsclip (mit einer
Vorhersagefrage) und ein Kontrollclip (fünf Fragen mit neuen Zahlen). Gemessene `dauer` werden beim Neulauf
gerettet; Einblendungen stehen als «@wort» auf dem Wort, das sie nennen (wortzeiten.json, faster-whisper medium).

Aufbau: Rechnung links (x 150), das Bild rechts (x 1010, y 175, 760 × 760): Faktor-Chips über und unter dem
Bruchstrich, Waage, Rechenkette — `graf` mit "figuren", Fenster 0 … 10.

Fragebild (HOWTO-leitprogramme §15): In den Kontrollclips zeigt das Bild beim Erscheinen einer Frage nur das Gegebene;
Rechnung und Auflösung erscheinen ab 1.0 s (nach der Antwort).

Farben — gleich wie auf der Seite:
  1 blau   = Zähler, x-Glieder        \\fa{…}
  2 orange = Nenner, Zahlen, Umformung \\fb{…}
  3 grün   = gekürzt, Ergebnis         \\fc{…}
  4 rot    = Fehler                    \\fd{…}
  5 Tinte  = neutral
Gesprochen: Klammerprodukte als «Klammer … mal Klammer …», Brüche als «… durch …» (HOWTO §15).
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
PRAEFIX = 'gleich-lp-'
WZ = json.load(open(HIER + 'wortzeiten.json')) if os.path.exists(HIER + 'wortzeiten.json') else {}
FEHLT = []

# ---------------------------------------------------------------- Zeiten auf den Ton (aus TALS Mathe, Kreis und Kreisteile)
SPRECH = {}


# Whisper schreibt Zahlwörter oft als Ziffern («fünfzehn» → «15»): solche Wörter auch an der Ziffer erkennen.
ZAHLWORT = {'eins': '1', 'zwei': '2', 'drei': '3', 'vier': '4', 'fünf': '5', 'sechs': '6', 'sieben': '7', 'acht': '8',
            'neun': '9', 'zehn': '10', 'zwölf': '12', 'vierzehn': '14', 'fünfzehn': '15', 'zwanzig': '20',
            'sechzehn': '16', 'achtzehn': '18', 'einundzwanzig': '21', 'fünfundzwanzig': '25', 'neunundvierzig': '49',
            'einundfünfzig': '51', 'einundachtzig': '81', 'vierzig': '40', 'einundvierzig': '41',
            'achtzehn': '18', 'dreissig': '30', 'sechzig': '60', 'hundert': '100', 'dreizehn': '13', 'elf': '11'}
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


def sz(name, spr, *el):
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
         'schlagworte': schlag, 'themenbereich': 'Gleichungen · Bruchterme, Gleichungen und Formeln',
         'fach': 'Sekundarstufe I', 'lerngebiet': '2 · Gleichungen',
         'lektion': ['lp-gleichungen'], 'stufe': ['Sek I'], 'datum': '2026-10-09',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Gleichungen sehen', 'folge': folge,
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms gleichungen-formeln; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + dname + '.json', 'w'), ensure_ascii=False, indent=1)
    print(dname, len(szenen), 'Szenen', len(fragen or []), 'Fragen')





# ---------------------------------------------------------------- Bausteine der Bilder
def chip(x, y, text, farbe, w=1.5, weg=None, ein=None, **kw):
    """Faktor-Chip: Kasten mit Text; `weg` = Zeitpunkt, ab dem er grün gestrichen ist."""
    f = [RECHT(x, y, w, 1.1, farbe, 0.25, dicke=2), T(x + w / 2, y + 0.33, text, farbe, g=44)]
    if weg is not None:
        f.append(S((x - 0.1, y - 0.1), (x + w + 0.1, y + 1.2), 3, False, 5, ein=weg))
    if ein is not None:
        f = [mit(g_, ein=ein) if 'ein' not in g_ else g_ for g_ in f]
    return f


def bruchbild(oben, unten, y=4.5, x0=1.0, breite=8.0):
    """Chips über und unter einem Bruchstrich; oben/unten: Listen (text, w, weg)."""
    f = [S((x0, y), (x0 + breite, y), 5, False, 4)]
    def reihe_(liste, yy, farbe):
        ges = sum(w for _, w, _ in liste) + 0.4 * (len(liste) - 1)
        x = x0 + (breite - ges) / 2
        out = []
        for text, w, weg in liste:
            out += chip(x, yy, text, farbe, w, weg)
            x += w + 0.4
        return out
    return f + reihe_(oben, y + 0.4, 1) + reihe_(unten, y - 1.5, 2)


def kette(schritte, y, ein=None, gruen=0):
    """Rechenkette: Kästen mit Pfeilen dazwischen; schritte = [kasten, pfeil, kasten, pfeil, …]."""
    f, x = [], 0.6
    for i, t in enumerate(schritte):
        if i % 2 == 0:
            w = 0.35 * len(t) + 0.8
            f += [RECHT(x, y, w, 0.9, 3 if i == gruen else 5, 0.15 if i == gruen else 0, dicke=2), T(x + w / 2, y + 0.3, t, 5, g=32)]
            x += w + 0.2
        else:
            f += [T(x + 0.75, y + 0.55, t, 2, g=28), S((x, y + 0.35), (x + 1.5, y + 0.35), 2, False, 3), T(x + 1.45, y + 0.2, '›', 2, g=40)]
            x += 1.7
    return [mit(g_, ein=ein) for g_ in f] if ein is not None else f


def waage(links, rechts, neig=0.0):
    """Waagbalken mit zwei Schalen; Texte darauf."""
    return [S((5, 2.0), (5, 5.0), 5, False, 5), V([(4.4, 1.6), (5.6, 1.6), (5, 2.0)], 5, 0.4, dicke=2),
            S((1.2, 5.0 + neig), (8.8, 5.0 - neig), 5, False, 5),
            S((1.2, 5.0 + neig), (1.2, 5.6 + neig), 5, False, 2), S((8.8, 5.0 - neig), (8.8, 5.6 - neig), 5, False, 2),
            RECHT(0.4, 5.6 + neig, 3.6, 0.15, 5, 0.6, dicke=0), RECHT(6.0, 5.6 - neig, 3.6, 0.15, 5, 0.6, dicke=0),
            T(2.2, 6.1 + neig, links, 1, g=38), T(7.8, 6.1 - neig, rechts, 1, g=38)]


def gross(text, y=5.5, farbe=5, g=48):
    return T(5, y, text, farbe, g=g)


# ════════════════════════════════════════════════ Kapitel 1 · Einführung: Bruchterme kürzen
clip('kuerzen', 1, 'Gleichungen sehen: Bruchterme kürzen',
     'Bruchterm und verbotene Zahl (5/(x − 3), x ≠ 3); Kürzen heisst gleiche Faktoren streichen (12/18 = 2/3); zuerst '
     'zerlegen: (x² − 9)/(2x + 6) = (x − 3)/2; Summanden nicht kürzen: (x + 3)/(x + 5) ≠ 3/5 mit Probe; Gegenzahlen.',
     ['Bruchterm', 'kürzen', 'Faktor', 'Summand', 'Nenner null'], [
         sz('Bruchterm',
            'Ein Bruchterm hat eine Variable im Nenner. Der Nenner darf nie null werden. Bei fünf durch Klammer x minus drei '
            'ist darum x gleich drei nicht erlaubt: Dann stünde unten null.',
            f(r'\dfrac{5}{\fb{x - 3}}', 330, 90, ein='@Bruchterm'),
            f(r'x \neq 3', 500, 64, ein='@erlaubt'),
            graf([gross('x = 3:   5 / 0', 6.2, 4, 46), gross('durch 0 geht nicht', 4.6, 4, 36)], ein='@null#2')),
         sz('Faktoren',
            'Kürzen kennst du von Zahlenbrüchen. Zerlege Zähler und Nenner in Faktoren: zwölf ist zwei mal sechs, achtzehn ist '
            'drei mal sechs. Der gleiche Faktor sechs wird gestrichen. Es bleiben zwei Drittel.',
            f(r'\dfrac{12}{18} = \dfrac{2 \cdot \fc{6}}{3 \cdot \fc{6}}', 330, 70, ein='@Zerlege'),
            f(r'= \dfrac{2}{3}', 500, 70, ein='@bleiben'),
            graf(bruchbild([('2', 1.2, None), ('6', 1.2, '@gestrichen')], [('3', 1.2, None), ('6', 1.2, '@gestrichen')]), ein='@Zerlege')),
         sz('Zerlegen',
            'Bei x Quadrat minus neun durch zwei x plus sechs siehst du zuerst nichts zum Kürzen. Zerlege den Zähler mit der '
            'binomischen Formel: Klammer x minus drei mal Klammer x plus drei. Im Nenner klammerst du zwei aus. Jetzt steht oben '
            'und unten der Faktor x plus drei. Es bleibt x minus drei durch zwei, für x ungleich minus drei.',
            f(r'\dfrac{x^2 - 9}{2x + 6}', 280, 66, ein=0.4),
            f(r'= \dfrac{(x - 3)\fc{(x + 3)}}{2\fc{(x + 3)}}', 430, 62, ein='@binomischen'),
            f(r'= \dfrac{x - 3}{2} \quad (x \neq -3)', 650, 62, ein='@bleibt'),
            graf(bruchbild([('(x − 3)', 2.8, None), ('(x + 3)', 2.8, '@Faktor')], [('2', 1.2, None), ('(x + 3)', 2.8, '@Faktor')]), ein='@Nenner')),
         sz('Summanden',
            'Bei Klammer x plus drei durch Klammer x plus fünf ist x ein Summand, kein Faktor. Wer das x streicht, erhält drei Fünftel. Probe '
            'mit x gleich eins: vier Sechstel, also zwei Drittel. Das ist nicht drei Fünftel. Dieser Bruch lässt sich nicht kürzen.',
            f(r'\dfrac{x + 3}{x + 5}', 300, 70, ein=0.05),
            f(r'\fd{\neq \dfrac{3}{5}}', 440, 62, ein='@streicht'),
            f(r'x = 1: \quad \dfrac{4}{6} = \dfrac{2}{3} \neq \dfrac{3}{5}', 580, 52, ein='@Probe'),
            graf(bruchbild([('x + 3', 2.8, None)], [('x + 5', 2.8, None)]), ein=0.05),
            graf([T(5, 7.6, 'oben und unten je eine Summe', 5, g=30), T(5, 1.8, 'nicht kürzbar', 4, g=38)], ein='@nicht#2')),
         sz('Gegenzahlen',
            'Achtung bei Gegenzahlen: drei minus x ist minus Klammer x minus drei. Darum gibt x minus drei durch drei minus x '
            'genau minus eins.',
            f(r'3 - x = -(x - 3)', 320, 62, ein='@Gegenzahlen'),
            f(r'\dfrac{x - 3}{3 - x} = \dfrac{x - 3}{-(x - 3)} = \fc{-1}', 470, 60, ein='@Darum')),
         sz('Merke',
            'Zum Mitnehmen: Der Nenner darf nie null sein. Gekürzt werden nur Faktoren, nie Summanden. Darum zuerst Zähler '
            'und Nenner zerlegen, dann gleiche Faktoren streichen.',
            titel('Zum Mitnehmen', 250, 76),
            n('Nenner nie null|nur Faktoren kürzen, nie Summanden|zuerst zerlegen, dann streichen', 400, 'blau', 44, ein=1.2)),
         jetzt_du(),
     ], [
         wahl('Summanden', 'Darf man in (x + 3)/(x + 5) das x oben und unten streichen?',
              ['Nein, x ist hier ein Summand.', 'Ja, es bleibt 3/5.', 'Ja, weil x oben und unten steht.'], 0,
              {0: 'Ja.', 1: 'Prüf mit einer Zahl: Für x = 1 ist der Bruch 4/6, also nicht 3/5.',
               2: 'Gekürzt werden nur gemeinsame Faktoren. Hier wird addiert.'},
              sprich='Darf man in Klammer x plus drei durch Klammer x plus fünf das x oben und unten streichen?',
              rueck_sprich={1: 'Prüf mit einer Zahl: Für x gleich eins ist der Bruch vier Sechstel, also nicht drei Fünftel.',
                            2: 'Gekürzt werden nur gemeinsame Faktoren. Hier wird addiert.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
clip('kontrolle-kuerzen', 2, 'Gleichungen sehen: Kontrollfragen zum Kürzen',
     'Fünf Fragen: 9x/(12x²) kürzen, (x² − 4)/(x + 2), verbotene Zahlen von (x − 1)/(x(x + 5)), ist (x + 7)/(x + 1) kürzbar, (5 − x)/(x − 5).',
     ['kürzen', 'Bruchterm', 'Nenner null', 'Kontrollfragen'], [
         sz('Frage 1',
            'Zerlege: neun x ist drei x mal drei, zwölf x Quadrat ist drei x mal vier x. Gestrichen wird drei x. Es bleibt drei durch vier x, für x ungleich null.',
            f(r'\dfrac{9x}{12x^2} = \dfrac{\fc{3x} \cdot 3}{\fc{3x} \cdot 4x} = \fc{\dfrac{3}{4x}}', 330, 62, ein=1.0),
            graf([gross('9x / (12x²)')], ein=0.05)),
         sz('Frage 2',
            'Der Zähler ist Klammer x minus zwei mal Klammer x plus zwei. Mit dem Nenner x plus zwei gekürzt bleibt x minus zwei, für x ungleich minus zwei.',
            f(r'\dfrac{(x - 2)\fc{(x + 2)}}{\fc{x + 2}} = \fc{x - 2}', 330, 62, ein=1.0),
            graf([gross('(x² − 4) / (x + 2)')], ein=0.05)),
         sz('Frage 3',
            'Der Nenner ist x mal Klammer x plus fünf. Er wird null für x gleich null und für x gleich minus fünf. Der Zähler darf null sein.',
            f(r'x(x + 5) = 0', 300, 58, ein=1.0),
            f(r'\fc{x = 0} \;\text{ und }\; \fc{x = -5}', 420, 58, ein=1.0),
            graf([gross('(x − 1) / (x(x + 5))')], ein=0.05)),
         sz('Frage 4',
            'Nein. Zähler und Nenner sind Summen ohne gemeinsamen Faktor. Probe mit x gleich eins: acht Halbe, also vier, nicht sieben.',
            f(r'x = 1: \quad \dfrac{8}{2} = 4 \neq 7', 330, 56, ein=1.0),
            graf([gross('(x + 7) / (x + 1)')], ein=0.05)),
         sz('Frage 5',
            'Fünf minus x ist minus Klammer x minus fünf. Gegenzahlen geteilt ergeben minus eins, für x ungleich fünf.',
            f(r'\dfrac{5 - x}{x - 5} = \dfrac{-(x - 5)}{x - 5} = \fc{-1}', 330, 60, ein=1.0),
            graf([gross('(5 − x) / (x − 5)')], ein=0.05)),
         sz('Merke',
            'Zum Mitnehmen: zuerst in Faktoren zerlegen, dann nur gleiche Faktoren streichen. Nicht erlaubt sind die Zahlen, für die der Nenner null wird.',
            titel('Zum Mitnehmen', 250, 76),
            n('zuerst zerlegen|nur gleiche Faktoren streichen|nicht erlaubt: Nenner wird null', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Kürze vollständig: 9x/(12x²)', ['3/(4x)', '3x/4', '9/(12x)'], 0,
              {0: 'Ja.', 1: 'Unten steht x², oben nur x: Nach dem Kürzen bleibt ein x im Nenner.', 2: 'Stimmt, ist aber noch nicht fertig: 9 und 12 haben den Faktor 3.'},
              sprich='Kürze vollständig: neun x durch zwölf x Quadrat.',
              rueck_sprich={1: 'Unten steht x Quadrat, oben nur x: Nach dem Kürzen bleibt ein x im Nenner.', 2: 'Stimmt, ist aber noch nicht fertig: Neun und zwölf haben den Faktor drei.'}),
         wahl('Frage 2', 'Kürze: (x² − 4)/(x + 2)', ['x − 2', 'x² − 2', 'nicht kürzbar'], 0,
              {0: 'Ja.', 1: 'Kürzen geht nur mit Faktoren: Zerlege zuerst x² − 4.', 2: 'x² − 4 lässt sich mit der binomischen Formel zerlegen.'},
              sprich='Kürze: x Quadrat minus vier, durch x plus zwei.',
              rueck_sprich={1: 'Kürzen geht nur mit Faktoren: Zerlege zuerst x Quadrat minus vier.', 2: 'x Quadrat minus vier lässt sich mit der binomischen Formel zerlegen.'}),
         wahl('Frage 3', 'Welche Zahlen sind für (x − 1)/(x(x + 5)) nicht erlaubt?', ['0 und −5', '1', '0 und 5'], 0,
              {0: 'Ja.', 1: 'Mit x = 1 wird der Zähler null, das ist erlaubt.', 2: 'Setz x = 5 ein: Der Nenner ist 50, nicht null.'},
              sprich='Welche Zahlen sind für Klammer x minus eins durch x mal Klammer x plus fünf nicht erlaubt?',
              rueck_sprich={1: 'Mit x gleich eins wird der Zähler null, das ist erlaubt.', 2: 'Setz x gleich fünf ein: Der Nenner ist fünfzig, nicht null.'}),
         wahl('Frage 4', 'Lässt sich (x + 7)/(x + 1) kürzen?', ['Nein', 'Ja, es gibt 7.', 'Ja, es gibt x + 7.'], 0,
              {0: 'Ja, richtig: nicht kürzbar.', 1: 'Prüf mit x = 1: 8/2 = 4, nicht 7.', 2: 'Prüf mit x = 1: 8/2 = 4, nicht 8.'},
              sprich='Lässt sich Klammer x plus sieben durch Klammer x plus eins kürzen?',
              rueck_sprich={0: 'Richtig: nicht kürzbar.', 1: 'Prüf mit x gleich eins: acht Halbe sind vier, nicht sieben.', 2: 'Prüf mit x gleich eins: acht Halbe sind vier, nicht acht.'}),
         wahl('Frage 5', 'Was ergibt (5 − x)/(x − 5)?', ['−1', '1', '0'], 0,
              {0: 'Ja.', 1: 'Zähler und Nenner sind Gegenzahlen, nicht gleich.', 2: 'Der Zähler ist nur für x = 5 null, und dann ist auch der Nenner null. Setz eine erlaubte Zahl ein, etwa x = 7.'},
              sprich='Was ergibt fünf minus x durch x minus fünf?',
              rueck_sprich={1: 'Zähler und Nenner sind Gegenzahlen, nicht gleich.', 2: 'Der Zähler ist nur für x gleich fünf null, und dann ist auch der Nenner null. Setz eine erlaubte Zahl ein, etwa x gleich sieben.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 2 · Einführung: Rechnen mit Bruchtermen
clip('rechnen', 3, 'Gleichungen sehen: Rechnen mit Bruchtermen',
     'Multiplizieren mit Kürzen vorher (3x/4 · 8/(9x²) = 2/(3x)), Dividieren mit dem Kehrwert, Hauptnenner aus Faktoren '
     '(1/x + 1/(2x) = 3/(2x)), 2/x − 1/(x + 1) mit Klammern, Fehler «Nenner addieren».',
     ['Bruchterm', 'multiplizieren', 'dividieren', 'Hauptnenner', 'addieren'], [
         sz('Mal',
            'Du rechnest mit Bruchtermen wie mit Zahlenbrüchen. Beim Multiplizieren: Zähler mal Zähler, Nenner mal Nenner. Vorher kürzen: '
            'drei mit neun, vier mit acht, x mit x Quadrat. Es bleibt zwei durch drei x.',
            f(r'\dfrac{3x}{4} \cdot \dfrac{8}{9x^2}', 280, 66, ein=0.4),
            f(r'= \dfrac{3x \cdot 8}{4 \cdot 9x^2}', 410, 62, ein='@Zähler'),
            n('kürzen: @3@ mit @9@, @4@ mit @8@, @x@ mit @x^2@', 550, 'blau', 42, ein='@Vorher'),
            f(r'= \fc{\dfrac{2}{3x}}', 680, 66, ein='@bleibt')),
         sz('Durch',
            'Dividieren heisst: mit dem Kehrwert multiplizieren. Fünf durch x geteilt durch zehn durch x Quadrat ist fünf durch x '
            'mal x Quadrat durch zehn. Gekürzt: x Halbe.',
            f(r'\dfrac{5}{x} : \dfrac{10}{x^2}', 280, 66, ein=0.4),
            f(r'= \dfrac{5}{x} \cdot \dfrac{\fb{x^2}}{\fb{10}}', 410, 62, ein='@Kehrwert'),
            f(r'= \fc{\dfrac{x}{2}}', 550, 66, ein='@Gekürzt')),
         sz('Hauptnenner',
            'Zum Addieren brauchen die Brüche denselben Nenner. Bei eins durch x und eins durch zwei x reicht zwei x: Er enthält '
            'jeden Faktor der beiden Nenner. Eins durch x wird zu zwei durch zwei x. Zusammen drei durch zwei x.',
            f(r'\dfrac{1}{x} + \dfrac{1}{2x}', 280, 66, ein=0.05),
            f(r'= \dfrac{\fb{2}}{\fb{2}x} + \dfrac{1}{2x}', 410, 62, ein='@wird'),
            f(r'= \fc{\dfrac{3}{2x}}', 550, 66, ein='@Zusammen'),
            graf([T(2.0, 7.5, 'Nenner 1:', 5, g=30, anker='start')] + chip(4.2, 7.1, 'x', 2, 1.0)
                 + [T(2.0, 5.9, 'Nenner 2:', 5, g=30, anker='start')] + chip(4.2, 5.5, '2', 2, 1.0) + chip(5.6, 5.5, 'x', 2, 1.0), ein=0.05),
            graf([T(2.0, 3.9, 'Hauptnenner:', 3, g=30, anker='start')] + chip(5.0, 3.5, '2', 3, 1.0) + chip(6.4, 3.5, 'x', 3, 1.0), ein='@enthält')),
         sz('Verschiedene Nenner',
            'Bei zwei durch x minus eins durch Klammer x plus eins ist der gemeinsame Nenner x mal Klammer x plus eins. Erweitere beide '
            'Brüche. Setz die Zähler in Klammern: zwei mal Klammer x plus eins, minus x. Es bleibt x plus zwei durch x mal Klammer x plus eins.',
            f(r'\dfrac{2}{x} - \dfrac{1}{x + 1}', 260, 62, ein=0.4),
            f(r'= \dfrac{2\fb{(x + 1)}}{x\fb{(x + 1)}} - \dfrac{1 \cdot \fb{x}}{(x + 1)\fb{x}}', 390, 54, ein='@Erweitere'),
            f(r'= \dfrac{2(x + 1) - x}{x(x + 1)}', 605, 56, ein='@Klammern'),
            f(r'= \fc{\dfrac{x + 2}{x(x + 1)}}', 770, 60, ein='@bleibt')),
         sz('Fehler',
            'Häufiger Fehler: die Nenner addieren. Eins durch x plus eins durch zwei ist nicht zwei durch Klammer x plus zwei. Probe mit '
            'x gleich zwei: eins durch zwei plus eins durch zwei ist eins, aber zwei durch vier ist nur eins durch zwei. Richtig ist '
            'Klammer zwei plus x durch zwei x.',
            f(r'\dfrac{1}{x} + \dfrac{1}{2} \fd{\neq \dfrac{2}{x + 2}}', 300, 60, ein='@Eins'),
            f(r'x = 2: \quad \dfrac{1}{2} + \dfrac{1}{2} = 1, \quad \dfrac{2}{4} = \fd{\dfrac{1}{2}}', 450, 52, ein='@Probe'),
            f(r'\text{richtig: } \dfrac{2 + x}{2x}', 600, 56, ein='@Richtig')),
         sz('Merke',
            'Zum Mitnehmen: Mal und durch wie bei Zahlenbrüchen, vorher kürzen. Plus und minus nur mit gleichem Nenner: '
            'gemeinsamer Nenner aus allen Faktoren, Zähler in Klammern.',
            titel('Zum Mitnehmen', 250, 76),
            n('mal: Zähler mal Zähler, Nenner mal Nenner|durch: mit dem Kehrwert mal|plus, minus: Hauptnenner, Zähler in Klammern', 400, 'blau', 44, ein=1.2)),
         jetzt_du(),
     ], [
         wahl('Hauptnenner', 'Welcher Nenner ist der kleinste gemeinsame von 1/x und 1/(2x)?', ['2x', '2x²', 'x + 2x'], 0,
              {0: 'Ja.', 1: '2x² ist gemeinsam, aber nicht der kleinste: 2x reicht schon.', 2: 'Nenner werden nicht addiert. Gesucht ist ein Vielfaches beider Nenner.'},
              sprich='Welcher Nenner ist der kleinste gemeinsame von eins durch x und eins durch zwei x?',
              rueck_sprich={1: 'Zwei x Quadrat ist gemeinsam, aber nicht der kleinste: Zwei x reicht schon.', 2: 'Nenner werden nicht addiert. Gesucht ist ein Vielfaches beider Nenner.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
clip('kontrolle-rechnen', 4, 'Gleichungen sehen: Kontrollfragen zum Rechnen mit Bruchtermen',
     'Fünf Fragen: 2/x · x²/6, 4/x : 2/x², 3/x + 4/x, Hauptnenner von 1/(3x) und 1/(2x²), 1/x + 1/(x − 1).',
     ['Bruchterm', 'Hauptnenner', 'Kehrwert', 'Kontrollfragen'], [
         sz('Frage 1',
            'Zähler mal Zähler: zwei x Quadrat. Nenner mal Nenner: sechs x. Gekürzt mit zwei x bleibt x Drittel.',
            f(r'\dfrac{2 \cdot x^2}{x \cdot 6} = \dfrac{2x^2}{6x} = \fc{\dfrac{x}{3}}', 330, 60, ein=1.0),
            graf([gross('2/x · x²/6')], ein=0.05)),
         sz('Frage 2',
            'Mit dem Kehrwert: vier durch x mal x Quadrat durch zwei. Das gibt vier x Quadrat durch zwei x, also zwei x.',
            f(r'\dfrac{4}{x} \cdot \dfrac{x^2}{2} = \dfrac{4x^2}{2x} = \fc{2x}', 330, 60, ein=1.0),
            graf([gross('4/x : 2/x²')], ein=0.05)),
         sz('Frage 3',
            'Gleiche Nenner: Nur die Zähler werden addiert. Drei plus vier ist sieben, der Nenner x bleibt.',
            f(r'\dfrac{3 + 4}{x} = \fc{\dfrac{7}{x}}', 330, 62, ein=1.0),
            graf([gross('3/x + 4/x')], ein=0.05)),
         sz('Frage 4',
            'Der kleinste gemeinsame Nenner braucht die Zahl sechs, das kleinste gemeinsame Vielfache von drei und zwei, und x Quadrat. Also sechs x Quadrat.',
            f(r'\text{kgV}(3;\ 2) = 6, \quad x^2 \quad \Rightarrow \quad \fc{6x^2}', 330, 56, ein=1.0),
            graf([gross('1/(3x)   und   1/(2x²)')], ein=0.05)),
         sz('Frage 5',
            'Gemeinsamer Nenner: x mal Klammer x minus eins. Zähler: x minus eins plus x, das ist zwei x minus eins. Ergebnis: Klammer zwei x minus eins durch x mal Klammer x minus eins.',
            f(r'\dfrac{(x - 1) + x}{x(x - 1)} = \fc{\dfrac{2x - 1}{x(x - 1)}}', 330, 60, ein=1.0),
            graf([gross('1/x + 1/(x − 1)')], ein=0.05)),
         sz('Merke',
            'Zum Mitnehmen: Beim Multiplizieren und Dividieren braucht es keinen gemeinsamen Nenner. Beim Addieren und Subtrahieren immer einen gemeinsamen Nenner.',
            titel('Zum Mitnehmen', 250, 76),
            n('mal und durch: ohne gemeinsamen Nenner|plus und minus: mit dem Hauptnenner', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Rechne und kürze vollständig: 2/x · x²/6', ['x/3', '2x²/(6x)', '2x/6'], 0,
              {0: 'Ja.', 1: 'Stimmt, ist aber noch nicht gekürzt.', 2: 'Stimmt, ist aber noch nicht gekürzt.'},
              sprich='Rechne und kürze vollständig: zwei durch x mal x Quadrat durch sechs.',
              rueck_sprich={1: 'Stimmt, ist aber noch nicht gekürzt.', 2: 'Stimmt, ist aber noch nicht gekürzt.'}),
         wahl('Frage 2', 'Rechne: 4/x : 2/x²', ['2x', '8/x³', '2/x'], 0,
              {0: 'Ja.', 1: 'Beim Dividieren wird der zweite Bruch umgedreht, nicht mit ihm multipliziert.', 2: 'Der Kehrwert von 2/x² ist x²/2.'},
              sprich='Rechne: vier durch x, geteilt durch zwei durch x Quadrat.',
              rueck_sprich={1: 'Beim Dividieren wird der zweite Bruch umgedreht, nicht mit ihm multipliziert.', 2: 'Der Kehrwert von zwei durch x Quadrat ist x Quadrat durch zwei.'}),
         wahl('Frage 3', 'Rechne: 3/x + 4/x', ['7/x', '7/(2x)', '12/x'], 0,
              {0: 'Ja.', 1: 'Bei gleichen Nennern bleibt der Nenner, nur die Zähler werden addiert.', 2: 'Addiert wird, nicht multipliziert.'},
              sprich='Rechne: drei durch x plus vier durch x.',
              rueck_sprich={1: 'Bei gleichen Nennern bleibt der Nenner, nur die Zähler werden addiert.', 2: 'Addiert wird, nicht multipliziert.'}),
         wahl('Frage 4', 'Hauptnenner von 1/(3x) und 1/(2x²)?', ['6x²', '6x³', '5x²'], 0,
              {0: 'Ja.', 1: 'x² reicht: Darin steckt auch x.', 2: 'Die Zahlen werden nicht addiert: gesucht ist das kleinste gemeinsame Vielfache von 3 und 2.'},
              sprich='Was ist der kleinste gemeinsame Nenner von eins durch drei x und eins durch zwei x Quadrat?',
              rueck_sprich={1: 'x Quadrat reicht: Darin steckt auch x.', 2: 'Die Zahlen werden nicht addiert: Gesucht ist das kleinste gemeinsame Vielfache von drei und zwei.'}),
         wahl('Frage 5', 'Rechne: 1/x + 1/(x − 1)', ['(2x − 1)/(x(x − 1))', '2/(2x − 1)', '1/(x(x − 1))'], 0,
              {0: 'Ja.', 1: 'Die Nenner werden nicht addiert. Mach zuerst gleichnamig.', 2: 'Beim Erweitern wird auch der Zähler erweitert: (x − 1) + x.'},
              sprich='Rechne: eins durch x plus eins durch Klammer x minus eins.',
              rueck_sprich={1: 'Die Nenner werden nicht addiert. Mach zuerst gleichnamig.', 2: 'Beim Erweitern wird auch der Zähler erweitert: x minus eins plus x.'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 3 · Einführung: Lineare Gleichungen
clip('gleichungen', 5, 'Gleichungen sehen: Lineare Gleichungen lösen',
     'Gleichung als Waage; 5x − 7 = 2x + 8 Schritt für Schritt mit Probe; Gleichung mit Brüchen bruchfrei machen '
     '((x + 1)/3 − (x − 2)/4 = 1); drei Ausgänge: eine Lösung, keine, alle.',
     ['Gleichung', 'Äquivalenzumformung', 'Waage', 'Probe', 'Lösungsmenge'], [
         sz('Waage',
            'Eine Gleichung ist wie eine Waage im Gleichgewicht. Links steht fünf x minus sieben, rechts zwei x plus acht. Tust '
            'du auf beiden Seiten dasselbe, bleibt sie im Gleichgewicht.',
            f(r'5x - 7 = 2x + 8', 330, 72, ein='@Links'),
            n('auf beiden Seiten dasselbe', 480, 'blau', 44, ein='@beiden'),
            graf(waage('5x − 7', '2x + 8'), ein='@Waage')),
         sz('Schritte',
            'Zieh auf beiden Seiten zwei x ab: drei x minus sieben gleich acht. Dann rechnest du plus sieben: drei x gleich '
            'fünfzehn. Und durch drei: x gleich fünf.',
            f(r'5x - 7 = 2x + 8', 260, 56, ein=0.05),
            f(r'3x - 7 = 8 \qquad \fb{(-2x)}', 370, 56, ein='@beiden'),
            f(r'3x = 15 \qquad \fb{(+7)}', 480, 56, ein='@rechnest'),
            f(r'\fc{x = 5} \qquad \fb{(: 3)}', 590, 62, ein='@Und'),
            graf(alle(waage('5x − 7', '2x + 8'), aus='@beiden'), ein=0.05),
            graf(alle(waage('3x − 7', '8'), ein='@beiden', aus='@rechnest'), ein='@beiden'),
            graf(alle(waage('3x', '15'), ein='@rechnest', aus='@Und'), ein='@rechnest'),
            graf(alle(waage('x', '5'), ein='@Und'), ein='@Und')),
         sz('Probe',
            'Prüfe durch Einsetzen. Fünf mal fünf minus sieben ist achtzehn. Zwei mal fünf plus acht ist auch achtzehn. Die '
            'Lösungsmenge ist L gleich die Menge mit der Zahl fünf.',
            f(r'5 \cdot 5 - 7 = 18', 300, 58, ein='@Fünf'),
            f(r'2 \cdot 5 + 8 = 18 \;\fc{\checkmark}', 410, 58, ein='@auch'),
            f(r'L = \{5\}', 540, 62, ein='@Lösungsmenge')),
         sz('Brüche',
            'Mit Brüchen: Klammer x plus eins durch drei minus Klammer x minus zwei durch vier gleich eins. Multipliziere beide '
            'Seiten mit zwölf und setz jeden Zähler in Klammern. Achtung: minus drei mal minus zwei gibt plus sechs. Es bleibt '
            'x plus zehn gleich zwölf, also x gleich zwei.',
            f(r'\dfrac{x + 1}{3} - \dfrac{x - 2}{4} = 1 \qquad | \fb{\cdot 12}', 250, 52, ein=0.4),
            f(r'4(x + 1) - 3(x - 2) = 12', 380, 54, ein='@Multipliziere'),
            f(r'4x + 4 - 3x \fb{+ 6} = 12', 480, 54, ein='@Achtung'),
            f(r'x + 10 = 12 \quad \Rightarrow \quad \fc{x = 2}', 580, 54, ein='@bleibt')),
         sz('Drei Ausgänge',
            'Nicht jede Gleichung hat genau eine Lösung. Bei zwei mal Klammer x plus eins gleich zwei x plus fünf fallen die x '
            'weg, und es bleibt zwei gleich fünf: falsch für jedes x. Es gibt keine Lösung, die Lösungsmenge ist leer. Bleibt eine '
            'wahre Aussage übrig, ist jede Zahl eine Lösung.',
            f(r'2(x + 1) = 2x + 5', 260, 58, ein='@Bei'),
            f(r'2x + 2 = 2x + 5 \quad \Rightarrow \quad \fd{2 = 5}', 370, 54, ein='@fallen'),
            f(r'L = \{\,\}', 480, 58, ein='@leer'),
            f(r'\text{wahr, z. B. } 0 = 0: \quad L = \mathbb{Q}', 600, 52, ein='@wahre')),
         sz('Merke',
            'Zum Mitnehmen: Auf beiden Seiten dasselbe tun. Zuerst Klammern auflösen, Brüche mit einem gemeinsamen Nenner wegschaffen, '
            'dann die x auf eine Seite. Am Schluss die Probe und die Lösungsmenge.',
            titel('Zum Mitnehmen', 250, 76),
            n('auf beiden Seiten dasselbe|Klammern auflösen, Brüche wegschaffen|x auf eine Seite, dann teilen|Probe und Lösungsmenge', 400, 'blau', 44, ein=1.2)),
         jetzt_du(),
     ], [
         wahl('Schritte', 'Was ist bei 5x − 7 = 2x + 8 ein sinnvoller erster Schritt?', ['auf beiden Seiten −2x', 'nur links +7', 'beide Seiten durch x'], 0,
              {0: 'Ja.', 1: 'Was du links tust, musst du auch rechts tun, sonst kippt die Waage.', 2: 'Durch x teilen hilft nicht: Das x soll allein auf eine Seite.'},
              sprich='Was ist bei fünf x minus sieben gleich zwei x plus acht ein sinnvoller erster Schritt?',
              rueck_sprich={1: 'Was du links tust, musst du auch rechts tun, sonst kippt die Waage.', 2: 'Durch x teilen hilft nicht: Das x soll allein auf eine Seite.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
clip('kontrolle-gleichungen', 6, 'Gleichungen sehen: Kontrollfragen zu Gleichungen',
     'Fünf Fragen: 6x + 4 = 2x + 24, 3(x − 2) = x + 8, x/3 + x/6 = 4, 2(x + 4) = 2x + 8, x + 5 = x + 2.',
     ['Gleichung', 'Lösungsmenge', 'Probe', 'Kontrollfragen'], [
         sz('Frage 1',
            'Minus zwei x: vier x plus vier gleich vierundzwanzig. Minus vier: vier x gleich zwanzig. Durch vier: x gleich fünf.',
            f(r'4x + 4 = 24', 280, 58, ein=1.0),
            f(r'4x = 20', 390, 58, ein=1.0),
            f(r'\fc{x = 5}', 500, 62, ein=1.0),
            graf([gross('6x + 4 = 2x + 24')], ein=0.05)),
         sz('Frage 2',
            'Zuerst die Klammer: drei x minus sechs gleich x plus acht. Minus x, plus sechs: zwei x gleich vierzehn. Also x gleich sieben.',
            f(r'3x - 6 = x + 8', 280, 58, ein=1.0),
            f(r'2x = 14', 390, 58, ein=1.0),
            f(r'\fc{x = 7}', 500, 62, ein=1.0),
            graf([gross('3(x − 2) = x + 8')], ein=0.05)),
         sz('Frage 3',
            'Mal sechs: zwei x plus x gleich vierundzwanzig. Drei x gleich vierundzwanzig, also x gleich acht.',
            f(r'2x + x = 24 \quad \Rightarrow \quad \fc{x = 8}', 330, 56, ein=1.0),
            graf([gross('x/3 + x/6 = 4')], ein=0.05)),
         sz('Frage 4',
            'Links steht ausmultipliziert zwei x plus acht, genau wie rechts. Jede Zahl erfüllt die Gleichung: L gleich alle Zahlen.',
            f(r'2x + 8 = 2x + 8 \quad \Rightarrow \quad \fc{L = \mathbb{Q}}', 330, 54, ein=1.0),
            graf([gross('2(x + 4) = 2x + 8')], ein=0.05)),
         sz('Frage 5',
            'Minus x auf beiden Seiten: fünf gleich zwei. Das ist nie wahr. Keine Lösung, die Lösungsmenge ist leer.',
            f(r'5 = 2 \quad \Rightarrow \quad \fc{L = \{\,\}}', 330, 58, ein=1.0),
            graf([gross('x + 5 = x + 2')], ein=0.05)),
         sz('Merke',
            'Zum Mitnehmen: Klammern auflösen, Brüche wegschaffen, auf beiden Seiten dasselbe tun. Fallen die x weg, entscheidet die übrige Aussage: wahr heisst alle Zahlen, falsch heisst keine Lösung.',
            titel('Zum Mitnehmen', 250, 76),
            n('auf beiden Seiten dasselbe|x fallen weg: wahr → alle Zahlen|falsch → keine Lösung', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Löse: 6x + 4 = 2x + 24', ['x = 5', 'x = 7', 'x = 2.5'], 0,
              {0: 'Ja.', 1: 'Mach die Probe: Mit x = 7 ist links 46, rechts 38.', 2: 'Mach die Probe: Mit x = 2.5 ist links 19, rechts 29.'},
              sprich='Löse: sechs x plus vier gleich zwei x plus vierundzwanzig.',
              rueck_sprich={1: 'Mach die Probe: Mit x gleich sieben ist links sechsundvierzig, rechts achtunddreissig.', 2: 'Mach die Probe: Mit x gleich zwei Komma fünf ist links neunzehn, rechts neunundzwanzig.'}),
         wahl('Frage 2', 'Löse: 3(x − 2) = x + 8', ['x = 7', 'x = 5', 'x = 1'], 0,
              {0: 'Ja.', 1: 'Die 3 gilt für beide Glieder der Klammer: 3x − 6, nicht 3x − 2.', 2: 'Mach die Probe: Mit x = 1 ist links −3, rechts 9.'},
              sprich='Löse: drei mal Klammer x minus zwei gleich x plus acht.',
              rueck_sprich={1: 'Die Drei gilt für beide Glieder der Klammer: drei x minus sechs, nicht drei x minus zwei.', 2: 'Mach die Probe: Mit x gleich eins ist links minus drei, rechts neun.'}),
         wahl('Frage 3', 'Löse: x/3 + x/6 = 4', ['x = 8', 'x = 36', 'x = 2'], 0,
              {0: 'Ja.', 1: 'Die Nenner werden nicht addiert: x/3 + x/6 ist nicht x/9.', 2: 'Mach die Probe: 2/3 + 2/6 = 1, nicht 4.'},
              sprich='Löse: x durch drei plus x durch sechs gleich vier.',
              rueck_sprich={1: 'Die Nenner werden nicht addiert: x durch drei plus x durch sechs ist nicht x durch neun.', 2: 'Mach die Probe: zwei Drittel plus zwei Sechstel ist eins, nicht vier.'}),
         wahl('Frage 4', 'Lösungsmenge von 2(x + 4) = 2x + 8?', ['alle Zahlen', 'keine Lösung', 'x = 0'], 0,
              {0: 'Ja.', 1: 'Setz eine Zahl ein, etwa x = 3: Stimmt die Gleichung?', 2: 'x = 0 passt, aber nicht nur: Setz x = 3 ein.'},
              sprich='Welche Lösungsmenge hat zwei mal Klammer x plus vier gleich zwei x plus acht?',
              rueck_sprich={1: 'Setz eine Zahl ein, etwa x gleich drei: Stimmt die Gleichung?', 2: 'x gleich null passt, aber nicht nur: Setz x gleich drei ein.'}),
         wahl('Frage 5', 'Lösungsmenge von x + 5 = x + 2?', ['keine Lösung', 'x = 0', 'alle Zahlen'], 0,
              {0: 'Ja.', 1: 'Setz x = 0 ein: Stimmt die Gleichung?', 2: 'Setz eine Zahl ein, etwa x = 1: Stimmt die Gleichung?'},
              sprich='Welche Lösungsmenge hat x plus fünf gleich x plus zwei?',
              rueck_sprich={1: 'Setz x gleich null ein: Stimmt die Gleichung?', 2: 'Setz eine Zahl ein, etwa x gleich eins: Stimmt die Gleichung?'}),
     ], art='Kontrollclip')

# ════════════════════════════════════════════════ Kapitel 4 · Einführung: Formeln umstellen
clip('formeln', 7, 'Gleichungen sehen: Formeln umstellen',
     'Formel als Gleichung mit Grössen; v = s/t nach t; F = 1.8·C + 32 rückwärts: −32, dann : 1.8 (212 °F = 100 °C); '
     'Trapez h = 2A/(a + c) mit Klammer; Fehler «nur durch a teilen».',
     ['Formel', 'umstellen', 'Rechenkette', 'Einheiten'], [
         sz('Formel',
            'Eine Formel ist eine Gleichung mit mehreren Grössen. v gleich s durch t: Die Geschwindigkeit ist der Weg durch die '
            'Zeit. Suchst du die Zeit, stellst du die Formel nach t um.',
            f(r'v = \dfrac{s}{t}', 330, 86, ein='@Formel'),
            n('gesucht: @t@', 500, 'orange', 46, ein='@Suchst')),
         sz('Umstellen',
            'Mal t auf beiden Seiten: s gleich v mal t. Dann durch v: t gleich s durch v. Probe mit Zahlen: hundertzwanzig '
            'Kilometer mit sechzig Kilometern pro Stunde dauern zwei Stunden.',
            f(r'v = \dfrac{s}{t} \qquad | \fb{\cdot t}', 260, 60, ein=0.3),
            f(r's = v \cdot t \qquad | \fb{: v}', 390, 60, ein='@Mal'),
            f(r'\fc{t = \dfrac{s}{v}}', 520, 66, ein='@Dann'),
            f(r't = \dfrac{120\ \text{km}}{60\ \text{km/h}} = 2\ \text{h}', 660, 52, ein='@Probe')),
         sz('Rückwärts',
            'Mit C wird zuerst mal eins Komma acht gerechnet, zuletzt plus zweiunddreissig. Rückwärts machst du das Letzte zuerst '
            'rückgängig: minus zweiunddreissig, dann durch eins Komma acht. Probe: zweihundertzwölf Grad Fahrenheit sind hundert Grad Celsius.',
            f(r'F = 1.8 \cdot C + 32', 260, 62, ein=0.05),
            f(r'F - 32 = 1.8 \cdot C', 380, 58, ein='@minus'),
            f(r'\fc{C = \dfrac{F - 32}{1.8}}', 510, 62, ein='@dann'),
            f(r'\dfrac{212 - 32}{1.8} = 100', 650, 54, ein='@Probe'),
            graf(kette(['C', '· 1.8', '', '+ 32', 'F'], 7.0) + [T(0.6, 8.3, 'vorwärts', 5, g=28, anker='start')], ein=0.05),
            graf(kette(['F', '− 32', '', ': 1.8', 'C'], 4.0, gruen=4) + [T(0.6, 5.3, 'rückwärts', 5, g=28, anker='start')], ein='@Rückwärts')),
         sz('Trapez',
            'Beim Trapez ist A gleich Klammer a plus c durch zwei, mal h. Nach h: mal zwei, dann durch die ganze Summe a plus c. '
            'Der Bruchstrich gilt für die ganze Summe: h gleich zwei A durch Klammer a plus c.',
            f(r'A = \dfrac{a + c}{2} \cdot h \qquad | \fb{\cdot 2}', 260, 56, ein=0.3),
            f(r'2A = (a + c) \cdot h \qquad | \fb{: (a + c)}', 390, 56, ein='@zwei#2'),
            f(r'\fc{h = \dfrac{2A}{a + c}}', 520, 62, ein='@Bruchstrich')),
         sz('Fehler',
            'Häufiger Fehler: nur durch a teilen und das c dazuzählen. Mit A gleich dreissig, a gleich fünf und c gleich sieben '
            'gibt die richtige Formel fünf. Die falsche gibt neunzehn.',
            f(r'h \fd{\neq \dfrac{2A}{a} + c}', 300, 62, ein='@Fehler'),
            f(r'\dfrac{60}{5 + 7} = \fc{5}, \qquad \dfrac{60}{5} + 7 = \fd{19}', 450, 54, ein='@richtige')),
         sz('Merke',
            'Zum Mitnehmen: Umstellen heisst rückwärts rechnen. Was zuletzt gerechnet wird, machst du zuerst rückgängig. '
            'Klammern bleiben, und erst am Schluss setzt du Zahlen mit Einheiten ein.',
            titel('Zum Mitnehmen', 250, 76),
            n('rückwärts rechnen: das Letzte zuerst|Klammern bleiben|erst dann Zahlen mit Einheiten', 400, 'blau', 44, ein=1.2)),
         jetzt_du(),
     ], [
         wahl('Rückwärts', 'F = 1.8·C + 32: Was machst du zuerst, um nach C umzustellen?', ['− 32', ': 1.8', '· 1.8'], 0,
              {0: 'Ja.', 1: 'Zuletzt wird + 32 gerechnet. Das machst du zuerst rückgängig.', 2: 'Rückgängig gemacht wird mit der Umkehrung, und zwar zuerst das Letzte.'},
              sprich='F gleich eins Komma acht mal C plus zweiunddreissig: Was machst du zuerst, um nach C umzustellen?',
              rueck_sprich={1: 'Zuletzt wird plus zweiunddreissig gerechnet. Das machst du zuerst rückgängig.', 2: 'Rückgängig gemacht wird mit der Umkehrung, und zwar zuerst das Letzte.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
clip('kontrolle-formeln', 8, 'Gleichungen sehen: Kontrollfragen zu Formeln',
     'Fünf Fragen: U = R·I nach I, A = a·b nach b, y = 3x + 6 nach x, M = (a + b)/2 nach a, Fahrzeit für 45 km bei 30 km/h.',
     ['Formel', 'umstellen', 'Kontrollfragen'], [
         sz('Frage 1',
            'Durch R auf beiden Seiten: I gleich U durch R.',
            f(r'U = R \cdot I \quad | : R \qquad \fc{I = \dfrac{U}{R}}', 330, 56, ein=1.0),
            graf([gross('U = R · I')], ein=0.05)),
         sz('Frage 2',
            'Durch a auf beiden Seiten: b gleich A durch a.',
            f(r'A = a \cdot b \quad | : a \qquad \fc{b = \dfrac{A}{a}}', 330, 56, ein=1.0),
            graf([gross('A = a · b')], ein=0.05)),
         sz('Frage 3',
            'Zuerst minus sechs, dann durch drei: x gleich Klammer y minus sechs durch drei.',
            f(r'y - 6 = 3x \qquad \fc{x = \dfrac{y - 6}{3}}', 330, 56, ein=1.0),
            graf([gross('y = 3x + 6')], ein=0.05)),
         sz('Frage 4',
            'Zuerst mal zwei, dann minus b: a gleich zwei M minus b.',
            f(r'2M = a + b \qquad \fc{a = 2M - b}', 330, 56, ein=1.0),
            graf([gross('M = (a + b) / 2')], ein=0.05)),
         sz('Frage 5',
            'Umgestellt: t gleich s durch v. Fünfundvierzig durch dreissig gibt eins Komma fünf Stunden.',
            f(r't = \dfrac{s}{v} = \dfrac{45}{30} = \fc{1.5\ \text{h}}', 330, 56, ein=1.0),
            graf([gross('s = 45 km,  v = 30 km/h', 5.5, 5, 40)], ein=0.05)),
         sz('Merke',
            'Zum Mitnehmen: Rückwärts rechnen, das Letzte zuerst. Klammern behalten. Und mit einer Probe in Zahlen siehst du sofort, ob die Formel stimmt.',
            titel('Zum Mitnehmen', 250, 76),
            n('rückwärts: das Letzte zuerst|Klammern behalten|Probe mit Zahlen', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Stelle U = R·I nach I um.', ['I = U/R', 'I = U·R', 'I = R/U'], 0,
              {0: 'Ja.', 1: 'Rückgängig gemacht wird «mal R» mit «durch R».', 2: 'Probe: Mit R = 2 und I = 3 ist U = 6. Deine Formel gibt 1/3.'},
              sprich='Stelle U gleich R mal I nach I um.',
              rueck_sprich={1: 'Rückgängig gemacht wird mal R mit durch R.', 2: 'Probe: Mit R gleich zwei und I gleich drei ist U gleich sechs. Deine Formel gibt ein Drittel.'}),
         wahl('Frage 2', 'Stelle A = a·b nach b um.', ['b = A/a', 'b = A − a', 'b = a/A'], 0,
              {0: 'Ja.', 1: 'a und b werden multipliziert, nicht addiert: rückgängig mit «durch a».', 2: 'Probe: Mit a = 2 und b = 5 ist A = 10. Deine Formel gibt 0.2.'},
              sprich='Stelle A gleich a mal b nach b um.',
              rueck_sprich={1: 'a und b werden multipliziert, nicht addiert: rückgängig mit durch a.', 2: 'Probe: Mit a gleich zwei und b gleich fünf ist A gleich zehn. Deine Formel gibt null Komma zwei.'}),
         wahl('Frage 3', 'Stelle y = 3x + 6 nach x um.', ['x = (y − 6)/3', 'x = y/3 − 6', 'x = (y + 6)/3'], 0,
              {0: 'Ja.', 1: 'Zuerst wird + 6 rückgängig gemacht, dann : 3 auf die ganze Differenz.', 2: 'Rückgängig gemacht wird + 6 mit − 6.'},
              sprich='Stelle y gleich drei x plus sechs nach x um.',
              rueck_sprich={1: 'Zuerst wird plus sechs rückgängig gemacht, dann durch drei auf die ganze Differenz.', 2: 'Rückgängig gemacht wird plus sechs mit minus sechs.'}),
         wahl('Frage 4', 'Stelle M = (a + b)/2 nach a um.', ['a = 2M − b', 'a = M/2 − b', 'a = 2(M − b)'], 0,
              {0: 'Ja.', 1: 'Rückgängig gemacht wird «durch 2» mit «mal 2».', 2: 'Probe mit a = 3, b = 5: M = 4, deine Formel gibt −2.'},
              sprich='Stelle M gleich Klammer a plus b durch zwei nach a um.',
              rueck_sprich={1: 'Rückgängig gemacht wird durch zwei mit mal zwei.', 2: 'Probe mit a gleich drei und b gleich fünf: M ist vier, deine Formel gibt minus zwei.'}),
         wahl('Frage 5', 'Wie lange dauern 45 km bei 30 km/h?', ['1.5 h', '1350 h', '2/3 h'], 0,
              {0: 'Ja.', 1: 'Aus s = v·t folgt t = s/v, nicht s·v.', 2: 'Das ist v/s. Gesucht ist t = s/v.'},
              sprich='Wie lange dauern fünfundvierzig Kilometer bei dreissig Kilometern pro Stunde?',
              rueck_sprich={1: 'Aus s gleich v mal t folgt t gleich s durch v, nicht s mal v.', 2: 'Das ist v durch s. Gesucht ist t gleich s durch v.'}),
     ], art='Kontrollclip')

if FEHLT:
    print('ohne gemessene Wortzeit (geschätzt):', len(FEHLT))
