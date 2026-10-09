"""Erzeugt die acht Drehbücher des Leitprogramms Bruchrechnen (09.10.2026).

  python3 scripts/lp/bruchrechnen/clips.py

Je Kapitel ein Einführungsclip (zeigt alles, was das Kapitel bringt, in Bewegung, mit einer Vorhersagefrage) und ein
Kontrollclip (fünf Fragen mit neuen Zahlen, ohne Einleitungsszene). Das Skript rettet beim Neulauf die gemessenen
`dauer` (Szenenname und Sprechertext gleich); nur Szenen mit neuem Text müssen danach vertont werden
(build-clip-ton.py --szenen). Einblendungen und Bewegungen stehen als «@wort» auf dem Wort, das sie nennen:
wortzeiten.py misst die Wortzeiten der vertonten Clips mit faster-whisper (wortzeiten.json), dieses Skript setzt
daraus die Sekunden ein. Ohne Messung wird aus der Lage des Wortes im Sprechertext geschätzt.
Vorbild: scripts/lp/kreis-kreisteile/clips.py in TALS Mathe (Helfer und Zeitlogik übernommen).

Aufbau: Rechnung und Notizen links (x 150), das Bild rechts (x 1010, y 175, 760 × 760) — Bruchstreifen,
Flächenmodell, Zahlenstrahl der Vielfachen, Rechenbaum, gezeichnet mit `graf`, "figuren", "achsen": false, Fenster
0 … 10 in x und y (massstäblich).

Fragebild (HOWTO-leitprogramme §15): In den Kontrollclips zeigt das Bild beim Erscheinen einer Frage nur das Gegebene;
Rechnung und Auflösung erscheinen ab 1.0 s (nach der Antwort).

Farben — eine Farbe, eine Bedeutung, gleich wie auf der Seite:
  1 blau   = erster Bruch                      \\fa{…}
  2 orange = zweiter Bruch, Erweiterungsfaktor  \\fb{…}
  3 grün   = Ergebnis                          \\fc{…}
  4 rot    = Fehler                            \\fd{…}
  5 Tinte  = neutral (Teilstriche, Beschriftung)
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
PRAEFIX = 't1-4-lp-'
WZ = json.load(open(HIER + 'wortzeiten.json')) if os.path.exists(HIER + 'wortzeiten.json') else {}
FEHLT = []

# ---------------------------------------------------------------- Zeiten auf den Ton (aus TALS Mathe, Kreis und Kreisteile)
SPRECH = {}


# Whisper schreibt Zahlwörter oft als Ziffern («fünfzehn» → «15»): solche Wörter auch an der Ziffer erkennen.
ZAHLWORT = {'eins': '1', 'zwei': '2', 'drei': '3', 'vier': '4', 'fünf': '5', 'sechs': '6', 'sieben': '7', 'acht': '8',
            'neun': '9', 'zehn': '10', 'zwölf': '12', 'vierzehn': '14', 'fünfzehn': '15', 'zwanzig': '20',
            'neunundzwanzig': '29', 'sechsunddreissig': '36', 'sechsmal': '6'}
NENNERWORT = {'halb': '2', 'drittel': '3', 'viertel': '4', 'fünftel': '5', 'sechstel': '6', 'achtel': '8', 'neuntel': '9',
              'zehntel': '10', 'zwölftel': '12'}


def passt(wort, gehoert):
    g = re.sub(r'[^\wäöü]', '', gehoert.lower())
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
    return (len(w_) >= 5 and w_[0] == g[0] and abs(len(w_) - len(g)) <= 3
            and difflib.SequenceMatcher(None, w_, g).ratio() >= 0.7)


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


X0, BW, BH = 0.5, 9.0, 1.2      # Streifen: links 0.5, 9 Einheiten breit, 1.2 hoch


def streifen(y, n, k, farbe=1, ab=0, x0=X0, w=BW, h=BH, fu=0.35, striche=True, dicke=3):
    """Streifen in n gleiche Teile, Teile ab … k−1 gefärbt: Füllung, Teilstriche, Rahmen (in dieser Reihenfolge)."""
    f_ = []
    if k > ab:
        f_.append(RECHT(x0 + w * ab / n, y, w * (k - ab) / n, h, farbe, fu, dicke=0))
    if striche:
        f_ += [S((x0 + w * j / n, y), (x0 + w * j / n, y + h), 5, dicke=2) for j in range(1, n)]
    f_.append(RECHT(x0, y, w, h, 5, 0, dicke=dicke))
    return f_


def feinteilung(y, n, m, farbe=2, ein=None, schritt=0.04, x0=X0, w=BW, h=BH):
    """Jedes der n Teile in m Stücke: die neuen Striche (nicht auf alten), nacheinander von links."""
    out, i = [], 0
    for j in range(1, n * m):
        if j % m:
            d = S((x0 + w * j / (n * m), y), (x0 + w * j / (n * m), y + h), farbe, True, 2)
            if ein:
                d['ein'] = '%s+%.2f' % (ein, schritt * i) if isinstance(ein, str) else round(ein + schritt * i, 2)
            out.append(d)
            i += 1
    return out


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
         'schlagworte': schlag, 'themenbereich': 'Arithmetik/Algebra · Rechnen in ℚ',
         'fach': 'Sekundarstufe I', 'lerngebiet': '1 · Arithmetik/Algebra',
         'lektion': ['t1-4'], 'stufe': ['Sek I'], 'datum': '2026-10-09',
         'theme': 'begreifbar-schlicht', 'latex': True, 'reihe': 'Brüche sehen', 'folge': folge,
         'nachlauf': 2.6, 'probe': True,
         '_probe': '%s des Leitprogramms bruchrechnen; gehoert dorthin, nicht in die Clip-Bibliothek.' % art,
         'szenen': szenen}
    if fragen:
        d['fragen'] = fragen
    json.dump(d, open(R + 'clips/' + dname + '.json', 'w'), ensure_ascii=False, indent=1)
    print(dname, len(szenen), 'Szenen', len(fragen or []), 'Fragen')


Y1, Y2, Y3 = 7.0, 4.6, 2.2       # drei Streifenzeilen
OBEN = 6.0                        # ein einzelner Streifen


def mitte(y, x0=X0, w=BW, h=BH):
    """Klickziel: die Mittellinie eines Streifens als Strecke."""
    return [[r3(x0 + 0.3), r3(y + h / 2)], [r3(x0 + w - 0.3), r3(y + h / 2)]]


# ════════════════════════════════════════════════ Kapitel 1 · Einführung: Erweitern, Kürzen, Vergleichen
clip('erweitern', 1, 'Brüche sehen: Erweitern, Kürzen, Vergleichen',
     'Ein Bruch als Anteil am Streifen; Erweitern als feinere Einteilung (3/4 = 15/20), Addieren statt Multiplizieren als '
     'Fehler (4/5), Kürzen als gröbere Einteilung (12/18 = 2/3), vollständig gekürzt mit dem ggT, Vergleichen auf dem '
     'gemeinsamen Nenner (2/3 < 3/4).',
     ['Bruch', 'Erweitern', 'Kürzen', 'ggT', 'Vergleichen'], [
         sz('Anteil',
            'Ein Bruch beschreibt einen Anteil. Der Nenner sagt, in wie viele gleiche Teile das Ganze geteilt ist. '
            'Der Zähler sagt, wie viele Teile wir nehmen: hier drei von vier.',
            f(r'\dfrac{\fa{3}}{4}', 330, 96, ein='@Bruch'),
            n('Nenner: in wie viele gleiche Teile|Zähler: wie viele Teile genommen', 500, 'blau', 42, ein='@Nenner'),
            graf(streifen(OBEN, 4, 0), ein=0.3),
            graf([RECHT(X0, OBEN, BW * 3 / 4, BH, 1, 0.35, dicke=0), T(X0 + BW * 3 / 8, OBEN - 0.8, '3 von 4', 1)], ein='@drei',
                 raster=False)),
         sz('Erweitern',
            'Jetzt teilen wir jedes Viertel in fünf gleiche Stücke. Es gibt zwanzig Stücke, und fünfzehn davon sind gefärbt. '
            'Die gefärbte Fläche ist dieselbe geblieben: drei Viertel gleich fünfzehn Zwanzigstel.',
            f(r'\dfrac{3}{4} = \dfrac{3 \cdot \fb{5}}{4 \cdot \fb{5}} = \dfrac{15}{20}', 330, 66, ein='@fünfzehn'),
            n('gleiche Fläche, feinere Einteilung', 500, 'blau', 42, ein='@dieselbe'),
            graf(streifen(OBEN, 4, 3, dicke=4), ein=0.05),
            graf(feinteilung(OBEN, 4, 5, ein='@fünf'), ein=0.05),
            graf([T(X0 + BW * 3 / 8, OBEN - 0.8, '15 von 20', 1)], ein='@fünfzehn')),
         sz('Nicht addieren',
            'Erweitern heisst multiplizieren. Wer stattdessen zu Zähler und Nenner eins addiert, erhält vier Fünftel. '
            'Das ist ein grösserer Anteil als drei Viertel.',
            f(r'\dfrac{3 \fd{+ 1}}{4 \fd{+ 1}} = \fd{\dfrac{4}{5}} \neq \dfrac{3}{4}', 330, 66, ein='@addiert'),
            n('Erweitern heisst @\\cdot@, nicht @+@', 500, 'blau', 42, ein='@multiplizieren'),
            graf(streifen(Y1, 4, 3) + [T(X0, Y1 + 1.6, '3/4', 1, 'start')], ein=0.05),
            graf(streifen(Y2, 5, 4, 4) + [T(X0, Y2 + 1.6, '4/5', 4, 'start')], ein='@vier'),
            graf([S((X0 + BW * 0.75, Y2 - 0.4), (X0 + BW * 0.75, Y1 + BH + 0.4), 5, True, 3)], ein='@grösserer')),
         sz('Kürzen',
            'Kürzen ist der umgekehrte Weg. Bei zwölf Achtzehnteln fassen wir je sechs Stücke zusammen. '
            'Es bleiben drei Teile, zwei davon gefärbt: zwei Drittel.',
            f(r'\dfrac{12}{18} = \dfrac{12 : \fb{6}}{18 : \fb{6}} = \dfrac{2}{3}', 330, 66, ein='@zusammen'),
            f(r'\text{ggT}(12;\ 18) = \fb{6}', 480, 50, ein='@sechs'),
            graf([RECHT(X0, OBEN, BW * 12 / 18, BH, 1, 0.35, dicke=0)]
                 + [mit(S((X0 + BW * j / 18, OBEN), (X0 + BW * j / 18, OBEN + BH), 5, dicke=2), aus='@zusammen+0.6')
                    for j in range(1, 18) if j % 6]
                 + [S((X0 + BW * j / 18, OBEN), (X0 + BW * j / 18, OBEN + BH), 5, dicke=4) for j in (6, 12)]
                 + [RECHT(X0, OBEN, BW, BH, 5, 0, dicke=4), mit(T(X0 + BW / 3, OBEN - 0.8, '12 von 18', 1), aus='@bleiben'),
                    mit(T(X0 + BW / 3, OBEN - 0.8, '2 von 3', 1), ein='@bleiben')], ein=0.3)),
         sz('Vollständig',
            'Vollständig gekürzt ist ein Bruch erst, wenn Zähler und Nenner keinen gemeinsamen Teiler mehr haben. '
            'Sechs Neuntel stimmt zwar, ist aber noch nicht fertig: Sechs und neun sind beide durch drei teilbar.',
            f(r'\dfrac{12}{18} = \fb{\dfrac{6}{9}} = \fc{\dfrac{2}{3}}', 330, 66, ein='@Neuntel'),
            n('@6@ und @9@: beide durch @3@ teilbar', 490, 'orange', 42, ein='@teilbar'),
            n('am schnellsten: durch den ggT', 590, 'blau', 42, ein='@gemeinsamen'),
            graf(streifen(Y1, 9, 6, 2) + [T(X0, Y1 + 1.6, '6/9', 2, 'start')], ein='@Neuntel'),
            graf(streifen(Y2, 3, 2, 3) + [T(X0, Y2 + 1.6, '2/3', 3, 'start')], ein='@teilbar')),
         sz('Vergleichen',
            'Welcher Anteil ist grösser, zwei Drittel oder drei Viertel? Bringen wir beide auf den Nenner zwölf: '
            'acht Zwölftel gegen neun Zwölftel. Drei Viertel ist grösser.',
            f(r'\dfrac{2}{3} = \dfrac{8}{12}', 300, 58, ein='@acht'),
            f(r'\dfrac{3}{4} = \dfrac{9}{12}', 420, 58, ein='@neun'),
            f(r'\dfrac{2}{3} \lt \fc{\dfrac{3}{4}}', 560, 62, ein='@grösser#2'),
            graf(streifen(Y1, 3, 2, 1) + [T(X0, Y1 + 1.6, '2/3', 1, 'start')]
                 + streifen(Y2, 4, 3, 2) + [T(X0, Y2 + 1.6, '3/4', 2, 'start')], ein=0.05),
            graf(feinteilung(Y1, 3, 4, 5, ein='@zwölf') + feinteilung(Y2, 4, 3, 5, ein='@zwölf'), ein=0.05),
            graf([T(X0 + BW * 8 / 12 - 0.1, Y1 - 0.7, '8', 1, 'end'), T(X0 + BW * 9 / 12 - 0.1, Y2 - 0.7, '9', 2, 'end')],
                 ein='@acht'),
            graf([S((X0 + BW * 8 / 12, Y2 - 0.3), (X0 + BW * 8 / 12, Y1 + BH + 0.3), 3, True, 3)], ein='@grösser#2')),
         sz('Merke',
            'Zum Mitnehmen: Erweitern und Kürzen ändern den Wert nicht, nur die Einteilung. Vollständig gekürzt wird mit dem '
            'grössten gemeinsamen Teiler. Zum Vergleichen bringt man Brüche auf denselben Nenner.',
            titel('Zum Mitnehmen', 250, 76),
            n('Erweitern, Kürzen: gleicher Wert, andere Einteilung|vollständig kürzen: durch den ggT|vergleichen: auf denselben Nenner',
              400, 'blau', 42, ein=1.2)),
         jetzt_du(),
     ], [
         wahl('Erweitern', 'Jedes Viertel wird gleich in 5 Stücke geteilt. Wie viele der 20 Stücke sind dann gefärbt?',
              ['15', '8', '3'], 0,
              {0: 'Ja.', 1: '3 + 5 wäre addiert. Jedes der drei gefärbten Viertel zerfällt in 5 Stücke.',
               2: 'Die drei Viertel bleiben gefärbt — aber jedes besteht jetzt aus mehreren Stücken.'},
              sprich='Jedes Viertel wird gleich in fünf Stücke geteilt. Wie viele der zwanzig Stücke sind dann gefärbt?',
              rueck_sprich={1: 'Drei plus fünf wäre addiert. Jedes der drei gefärbten Viertel zerfällt in fünf Stücke.',
                            2: 'Die drei Viertel bleiben gefärbt, aber jedes besteht jetzt aus mehreren Stücken.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 1 · Kontrolle
clip('kontrolle-erweitern', 2, 'Brüche sehen: Kontrollfragen zum Erweitern und Kürzen',
     'Fünf Fragen: den Streifen mit demselben Anteil wie 2/3 antippen, 2/7 auf den Nenner 21 erweitern, 18/24 vollständig '
     'kürzen, 5/8 und 3/5 vergleichen, Summanden nicht kürzen.',
     ['Erweitern', 'Kürzen', 'Vergleichen', 'Kontrollfragen'], [
         sz('Frage 1',
            'Vier Sechstel: Kürzt man durch zwei, erhält man zwei Drittel. Drei Viertel ist mehr, drei Fünftel weniger.',
            f(r'\dfrac{4}{6} = \dfrac{4 : 2}{6 : 2} = \fc{\dfrac{2}{3}}', 320, 60, ein=1.0),
            graf(streifen(Y1, 4, 3, 1) + streifen(Y2, 6, 4, 1) + streifen(Y3, 5, 3, 1)
                 + [T(X0, Y1 + 1.6, 'A', 5, 'start'), T(X0, Y2 + 1.6, 'B', 5, 'start'), T(X0, Y3 + 1.6, 'C', 5, 'start')], ein=0.05),
            graf([RECHT(X0 - 0.15, Y2 - 0.15, BW + 0.3, BH + 0.3, 3, 0, dicke=5), T(X0 + BW, Y2 + 1.6, '4/6 = 2/3', 3, 'end'),
                  T(X0 + BW, Y1 + 1.6, '3/4', 5, 'end'), T(X0 + BW, Y3 + 1.6, '3/5', 5, 'end'),
                  S((X0 + BW * 2 / 3, Y3 - 0.3), (X0 + BW * 2 / 3, Y1 + BH + 0.3), 3, True, 3)], ein=1.0)),
         sz('Frage 2',
            'Von sieben zu einundzwanzig kommt man mit mal drei. Also auch der Zähler mal drei: sechs Einundzwanzigstel.',
            f(r'\dfrac{2}{7} = \dfrac{2 \cdot \fb{3}}{7 \cdot \fb{3}} = \fc{\dfrac{6}{21}}', 320, 64, ein=1.0),
            graf(streifen(OBEN, 7, 2, 1, dicke=4), ein=0.05),
            graf(feinteilung(OBEN, 7, 3, ein=1.0) + [T(X0 + BW * 3 / 21, OBEN - 0.8, '6 von 21', 3)], ein=1.0)),
         sz('Frage 3',
            'Der grösste gemeinsame Teiler von achtzehn und vierundzwanzig ist sechs. Also drei Viertel. '
            'Neun Zwölftel und sechs Achtel stimmen, sind aber noch kürzbar.',
            f(r'\text{ggT}(18;\ 24) = \fb{6}', 300, 54, ein=1.0),
            f(r'\dfrac{18}{24} = \dfrac{18 : 6}{24 : 6} = \fc{\dfrac{3}{4}}', 430, 62, ein=1.0),
            graf([RECHT(X0, OBEN, BW * 18 / 24, BH, 1, 0.35, dicke=0)]
                 + [mit(S((X0 + BW * j / 24, OBEN), (X0 + BW * j / 24, OBEN + BH), 5, dicke=2), aus=1.6) for j in range(1, 24) if j % 6]
                 + [S((X0 + BW * j / 24, OBEN), (X0 + BW * j / 24, OBEN + BH), 5, dicke=2) for j in (6, 12, 18)]
                 + [RECHT(X0, OBEN, BW, BH, 5, 0, dicke=4)], ein=0.05),
            graf([T(X0 + BW * 3 / 8, OBEN - 0.8, '3 von 4', 3)], ein=1.6)),
         sz('Frage 4',
            'Auf dem gemeinsamen Nenner vierzig: fünfundzwanzig Vierzigstel gegen vierundzwanzig Vierzigstel. Fünf Achtel ist grösser, '
            'wenn auch nur knapp.',
            f(r'\dfrac{5}{8} = \dfrac{25}{40}, \quad \dfrac{3}{5} = \dfrac{24}{40}', 320, 56, ein=1.0),
            f(r'\fc{\dfrac{5}{8}} \gt \dfrac{3}{5}', 460, 62, ein=1.0),
            graf(streifen(Y1, 8, 5, 1) + [T(X0, Y1 + 1.6, '5/8', 1, 'start')]
                 + streifen(Y2, 5, 3, 2) + [T(X0, Y2 + 1.6, '3/5', 2, 'start')]
                 + [S((X0 + BW * 5 / 8, Y2 - 0.3), (X0 + BW * 5 / 8, Y1 + BH + 0.3), 3, True, 3)], ein=1.0)),
         sz('Frage 5',
            'Kürzen darf man nur Faktoren. Die drei ist hier ein Summand. Zuerst ausrechnen: acht Zehntel. Gekürzt sind das vier Fünftel.',
            f(r'\dfrac{3 + 5}{3 + 7} = \dfrac{8}{10} = \fc{\dfrac{4}{5}}', 320, 64, ein=1.0),
            f(r'\fd{\neq \dfrac{5}{7}}', 450, 60, ein=1.0),
            n('kürzen: nur gemeinsame Faktoren', 570, 'blau', 42, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Zähler und Nenner mit derselben Zahl multiplizieren oder durch dieselbe Zahl dividieren. '
            'Vollständig kürzen mit dem ggT. Und nie Summanden kürzen.',
            titel('Zum Mitnehmen', 250, 76),
            n('erweitern: @\\cdot@ dieselbe Zahl|kürzen: @:@ dieselbe Zahl, am besten den ggT|nie Summanden kürzen', 400, 'blau', 44, ein=1.2)),
     ], [
         klick('Frage 1', 'Tipp den Streifen an, der denselben Anteil zeigt wie 2/3.', mitte(Y2),
               'Getroffen: 4/6 lässt sich auf 2/3 kürzen.',
               [{'bei': mitte(Y1), 'text': 'Das sind 3/4 — etwas mehr als 2/3.', 'sprich': 'Das sind drei Viertel, etwas mehr als zwei Drittel.'},
                {'bei': mitte(Y3), 'text': 'Das sind 3/5 — etwas weniger als 2/3.', 'sprich': 'Das sind drei Fünftel, etwas weniger als zwei Drittel.'}],
               'Nicht ganz. Grün siehst du den gesuchten Streifen.',
               sprich='Tipp den Streifen an, der denselben Anteil zeigt wie zwei Drittel.',
               falsch_sprich='Nicht ganz. Grün siehst du den gesuchten Streifen.'),
         wahl('Frage 2', '2/7 = ?/21 — welche Zahl gehört in den Zähler?', ['6', '16', '2'], 0,
              {0: 'Ja.', 1: 'Von 7 zu 21 kommst du mit mal 3, nicht mit plus 14.', 2: 'Der Nenner wurde mit 3 multipliziert — der Zähler auch?'},
              sprich='Zwei Siebtel sollen auf den Nenner einundzwanzig erweitert werden. Welche Zahl gehört in den Zähler?',
              rueck_sprich={1: 'Von sieben zu einundzwanzig kommst du mit mal drei, nicht mit plus vierzehn.',
                            2: 'Der Nenner wurde mit drei multipliziert. Der Zähler auch?'}),
         wahl('Frage 3', 'Kürze 18/24 vollständig.', ['3/4', '9/12', '6/8'], 0,
              {0: 'Ja.', 1: 'Stimmt, ist aber noch nicht fertig: 9 und 12 sind beide durch 3 teilbar.',
               2: 'Stimmt, ist aber noch nicht fertig: 6 und 8 sind beide durch 2 teilbar.'},
              sprich='Kürze achtzehn Vierundzwanzigstel vollständig.',
              rueck_sprich={1: 'Stimmt, ist aber noch nicht fertig: Neun und zwölf sind beide durch drei teilbar.',
                            2: 'Stimmt, ist aber noch nicht fertig: Sechs und acht sind beide durch zwei teilbar.'}),
         wahl('Frage 4', 'Welcher Bruch ist grösser: 5/8 oder 3/5?', ['5/8', '3/5', 'beide gleich gross'], 0,
              {0: 'Ja.', 1: 'Bring beide auf den Nenner 40 und vergleiche die Zähler.', 2: 'Sie liegen nahe beieinander — vergleiche sie auf dem Nenner 40.'},
              sprich='Welcher Bruch ist grösser: fünf Achtel oder drei Fünftel?',
              rueck_sprich={1: 'Bring beide auf den gemeinsamen Nenner vierzig und vergleiche die Zähler.',
                            2: 'Sie liegen nahe beieinander. Vergleiche sie auf dem Nenner vierzig.'}),
         wahl('Frage 5', 'Darf man in (3 + 5)/(3 + 7) die 3 oben und unten streichen?',
              ['Nein, die 3 ist ein Summand.', 'Ja, es bleibt 5/7.', 'Ja, weil die 3 oben und unten steht.'], 0,
              {0: 'Ja.', 1: 'Rechne nach: (3 + 5)/(3 + 7) = 8/10 = 4/5, nicht 5/7.', 2: 'Kürzen darf man nur gemeinsame Faktoren — hier wird addiert.'},
              sprich='Darf man in drei plus fünf durch drei plus sieben die Drei oben und unten streichen?',
              rueck_sprich={1: 'Rechne nach: acht Zehntel sind vier Fünftel, nicht fünf Siebtel.',
                            2: 'Kürzen darf man nur gemeinsame Faktoren. Hier wird addiert.'}),
     ], art='Kontrollclip')


# ════════════════════════════════════════════════ Kapitel 2 · Einführung: Addieren und Subtrahieren
def zahlstrahl(werte_a, werte_b, ziel, vmax, ein_a, ein_b, ein_z, y=5.0):
    """Zahlenstrahl der Vielfachen: oben die Vielfachen des einen Nenners (blau), unten des anderen (orange),
    das kleinste gemeinsame grün umkreist."""
    X = lambda v: X0 + BW * v / vmax
    f_ = [S((X0, y), (X0 + BW, y), 5, False, 3), T(X(0), y - 0.9, '0', 5)]
    for v in werte_a:
        f_.append(mit(S((X(v), y), (X(v), y + 0.7), 1, False, 5), ein=ein_a))
        f_.append(mit(T(X(v), y + 1.1, str(v), 1, g=30), ein=ein_a))
    for v in werte_b:
        f_.append(mit(S((X(v), y - 0.7), (X(v), y), 2, False, 5), ein=ein_b))
        f_.append(mit(T(X(v), y - 1.5, str(v), 2, g=30), ein=ein_b))
    f_.append(mit(KR((X(ziel), y), 0.55, 3, 0.15, 4), ein=ein_z))
    return f_


clip('addieren', 3, 'Brüche sehen: Addieren und Subtrahieren',
     'Gleichnamige Brüche zählen (3/8 + 1/8 = 1/2); Halbe und Drittel in Sechstel zerlegen (1/2 + 1/3 = 5/6); der Fehler '
     '«Nenner addieren» (2/5 < 1/2); Hauptnenner als kgV (5/12 + 7/18 = 29/36); am Schluss kürzen; 2 − 3/4 = 5/4.',
     ['Addieren', 'Subtrahieren', 'Hauptnenner', 'kgV', 'gleichnamig'], [
         sz('Gleichnamig',
            'Drei Achtel plus ein Achtel: Die Stücke sind gleich gross, also zählen wir sie. Vier Achtel, und gekürzt ein Halb.',
            f(r'\dfrac{\fa{3}}{8} + \dfrac{\fb{1}}{8} = \dfrac{4}{8} = \fc{\dfrac{1}{2}}', 330, 66, ein='@Vier'),
            graf(streifen(Y1, 8, 3, 1) + [T(X0, Y1 + 1.6, '3/8 + 1/8', 5, 'start')]
                 + [mit(RECHT(X0, Y2, BW / 8, BH, 2, 0.45, dicke=2),
                        bewegung=[['@zählen', {}], ['@zählen+1.2', {'punkte': [[r3(X0 + BW * 3 / 8), Y1], [r3(X0 + BW * 4 / 8), Y1],
                                                                                  [r3(X0 + BW * 4 / 8), Y1 + BH], [r3(X0 + BW * 3 / 8), Y1 + BH]]}]])],
                 ein=0.3),
            graf([S((X0 + BW / 2, Y1 - 0.3), (X0 + BW / 2, Y1 + BH + 0.3), 3, False, 6), T(X0 + BW / 4, Y1 - 0.8, '1/2', 3)],
                 ein='@Halb')),
         sz('Verschieden gross',
            'Ein Halb plus ein Drittel. Halbe und Drittel sind verschieden grosse Stücke. So kann man sie nicht einfach zählen.',
            f(r'\dfrac{\fa{1}}{2} + \dfrac{\fb{1}}{3} = \;?', 330, 70, ein=0.5),
            n('verschieden grosse Stücke', 480, 'blau', 42, ein='@verschieden'),
            graf(streifen(Y1, 2, 1, 1) + [T(X0, Y1 + 1.6, '1/2', 1, 'start')], ein=0.3),
            graf(streifen(Y2, 3, 1, 2) + [T(X0, Y2 + 1.6, '1/3', 2, 'start')], ein='@Drittel')),
         sz('Sechstel',
            'Teilen wir beide Streifen in Sechstel, passen beide genau. Ein Halb sind drei Sechstel, ein Drittel sind zwei '
            'Sechstel. Zusammen ergeben sie fünf Sechstel.',
            f(r'\dfrac{1}{2} = \dfrac{\fa{3}}{6}', 280, 56, ein='@drei'),
            f(r'\dfrac{1}{3} = \dfrac{\fb{2}}{6}', 400, 56, ein='@zwei'),
            f(r'\dfrac{3}{6} + \dfrac{2}{6} = \fc{\dfrac{5}{6}}', 540, 62, ein='@Zusammen'),
            graf(streifen(Y1, 2, 1, 1) + [T(X0, Y1 + 1.6, '1/2', 1, 'start')]
                 + streifen(Y2, 3, 1, 2) + [T(X0, Y2 + 1.6, '1/3', 2, 'start')], ein=0.05),
            graf(feinteilung(Y1, 2, 3, 5, ein='@Sechstel') + feinteilung(Y2, 3, 2, 5, ein='@Sechstel'), ein=0.05),
            graf(streifen(Y3, 6, 0) + [T(X0, Y3 + 1.6, 'Summe', 3, 'start')]
                 + [mit(RECHT(X0, Y1, BW / 2, BH, 1, 0.45, dicke=2),
                        bewegung=[['@Zusammen', {}], ['@Zusammen+0.7', {'punkte': [[X0, Y3], [r3(X0 + BW / 2), Y3], [r3(X0 + BW / 2), Y3 + BH], [X0, Y3 + BH]]}]]),
                    mit(RECHT(X0, Y2, BW / 3, BH, 2, 0.45, dicke=2),
                        bewegung=[['@Zusammen+0.25', {}], ['@Zusammen+0.95', {'punkte': [[r3(X0 + BW / 2), Y3], [r3(X0 + BW * 5 / 6), Y3],
                                                                                         [r3(X0 + BW * 5 / 6), Y3 + BH], [r3(X0 + BW / 2), Y3 + BH]]}]]),
                    mit(T(X0 + BW * 5 / 12, Y3 - 0.8, '5/6', 3), ein='@fünf')],
                 ein='@Zusammen-0.3')),
         sz('Fehler',
            'Wer Zähler und Nenner einzeln addiert, erhält zwei Fünftel. Das ist sogar weniger als ein Halb allein. '
            'Eine Summe kann nicht kleiner sein als einer ihrer Summanden.',
            f(r'\dfrac{1 + 1}{2 + 3} = \fd{\dfrac{2}{5}}', 320, 66, ein='@einzeln'),
            f(r'\fd{\dfrac{2}{5}} \lt \dfrac{1}{2}', 470, 62, ein='@weniger'),
            graf(streifen(Y1, 2, 1, 1) + [T(X0, Y1 + 1.6, '1/2', 1, 'start')], ein=0.05),
            graf(streifen(Y2, 5, 2, 4) + [T(X0, Y2 + 1.6, '2/5', 4, 'start')], ein='@zwei'),
            graf([S((X0 + BW / 2, Y2 - 0.3), (X0 + BW / 2, Y1 + BH + 0.3), 5, True, 3)], ein='@weniger')),
         sz('Hauptnenner',
            'Der kleinste gemeinsame Nenner heisst Hauptnenner: das kleinste gemeinsame Vielfache der Nenner. '
            'Bei fünf Zwölfteln plus sieben Achtzehnteln: Die Vielfachen von achtzehn sind achtzehn und sechsunddreissig. '
            'Sechsunddreissig ist auch durch zwölf teilbar.',
            n('Hauptnenner = kgV der Nenner', 290, 'blau', 46, ein='@Hauptnenner'),
            f(r'\dfrac{5}{\fa{12}} + \dfrac{7}{\fb{18}}', 420, 60, ein='@fünf'),
            f(r'\text{kgV}(12;\ 18) = \fc{36}', 560, 54, ein='@teilbar'),
            graf(zahlstrahl([12, 24, 36, 48], [18, 36], 36, 54, '@teilbar', '@Vielfachen', '@teilbar+0.4'), ein='@fünf')),
         sz('Erweitern auf 36',
            'Fünf Zwölftel erweitern wir mit drei, sieben Achtzehntel mit zwei. Fünfzehn Sechsunddreissigstel plus vierzehn '
            'Sechsunddreissigstel ergibt neunundzwanzig Sechsunddreissigstel.',
            f(r'\dfrac{5 \cdot \fb{3}}{12 \cdot \fb{3}} + \dfrac{7 \cdot \fb{2}}{18 \cdot \fb{2}}', 300, 56, ein='@erweitern'),
            f(r'= \dfrac{\fa{15}}{36} + \dfrac{\fb{14}}{36} = \fc{\dfrac{29}{36}}', 450, 60, ein='@Fünfzehn'),
            graf(streifen(OBEN, 36, 0, dicke=4), ein=0.3),
            graf([RECHT(X0, OBEN, BW * 15 / 36, BH, 1, 0.45, dicke=0)], ein='@Fünfzehn'),
            graf([RECHT(X0 + BW * 15 / 36, OBEN, BW * 14 / 36, BH, 2, 0.45, dicke=0)], ein='@vierzehn'),
            graf([T(X0 + BW * 29 / 72, OBEN - 0.8, '29 von 36', 3)], ein='@neunundzwanzig')),
         sz('Am Schluss kürzen',
            'Am Schluss immer prüfen, ob man kürzen kann. Ein Sechstel plus ein Drittel gibt drei Sechstel, also ein Halb. '
            'Und mit einer ganzen Zahl: zwei sind acht Viertel, also ist zwei minus drei Viertel gleich fünf Viertel.',
            f(r'\dfrac{1}{6} + \dfrac{1}{3} = \dfrac{1}{6} + \dfrac{2}{6} = \dfrac{3}{6} = \fc{\dfrac{1}{2}}', 320, 56, ein='@Sechstel'),
            f(r'2 - \dfrac{3}{4} = \dfrac{8}{4} - \dfrac{3}{4} = \fc{\dfrac{5}{4}}', 470, 56, ein='@ganzen')),
         sz('Merke',
            'Zum Mitnehmen: Addieren und subtrahieren nur mit gleichen Nennern. Als gemeinsamen Nenner nimmt man das kleinste '
            'gemeinsame Vielfache. Nie die Nenner addieren, und am Schluss kürzen.',
            titel('Zum Mitnehmen', 250, 76),
            n('nur gleichnamig addieren und subtrahieren|Hauptnenner = kgV der Nenner|Nenner nie addieren, am Schluss kürzen', 400, 'blau', 44, ein=1.2)),
         jetzt_du(),
     ], [
         wahl('Fehler', 'Jemand rechnet 1/2 + 1/3 = 2/5. Ist 2/5 mehr oder weniger als 1/2 allein?',
              ['weniger', 'mehr', 'gleich viel'], 0,
              {0: 'Ja.', 1: 'Schau gleich im Bild: Wie lang ist der rote Streifen im Vergleich zu 1/2?',
               2: 'Schau gleich im Bild: Endet der rote Streifen bei der Hälfte?'},
              sprich='Jemand rechnet ein Halb plus ein Drittel gleich zwei Fünftel. Ist zwei Fünftel mehr oder weniger als ein Halb allein?',
              rueck_sprich={1: 'Schau gleich im Bild: Wie lang ist der rote Streifen im Vergleich zu einem Halb?',
                            2: 'Schau gleich im Bild: Endet der rote Streifen bei der Hälfte?'}),
     ])

# ════════════════════════════════════════════════ Kapitel 2 · Kontrolle
clip('kontrolle-addieren', 4, 'Brüche sehen: Kontrollfragen zum Addieren und Subtrahieren',
     'Fünf Fragen: 3/10 + 1/10 gekürzt, Hauptnenner von 3/8 und 5/12, 1/4 + 1/5, 5/6 − 1/4, den Fehler 1/3 + 1/4 = 2/7 ohne '
     'Rechnung erkennen.',
     ['Addieren', 'Subtrahieren', 'Hauptnenner', 'Kontrollfragen'], [
         sz('Frage 1',
            'Gleich grosse Stücke zählen: vier Zehntel. Gekürzt durch zwei: zwei Fünftel.',
            f(r'\dfrac{3}{10} + \dfrac{1}{10} = \dfrac{4}{10} = \fc{\dfrac{2}{5}}', 320, 62, ein=1.0),
            graf(streifen(OBEN, 10, 3, 1) + [RECHT(X0 + BW * 3 / 10, OBEN, BW / 10, BH, 2, 0.45, dicke=0)], ein=0.05),
            graf([T(X0 + BW / 5, OBEN - 0.8, '4 von 10 = 2 von 5', 3)], ein=1.0)),
         sz('Frage 2',
            'Vielfache von zwölf: zwölf, vierundzwanzig. Vierundzwanzig ist auch durch acht teilbar. Das ist der kleinste gemeinsame Nenner.',
            f(r'\text{kgV}(8;\ 12) = \fc{24}', 320, 58, ein=1.0),
            graf(zahlstrahl([12, 24, 36, 48], [8, 16, 24, 32, 40, 48], 24, 54, 1.0, 1.0, 1.4), ein=1.0)),
         sz('Frage 3',
            'Gemeinsamer Nenner zwanzig: fünf Zwanzigstel plus vier Zwanzigstel ergibt neun Zwanzigstel.',
            f(r'\dfrac{1}{4} + \dfrac{1}{5} = \dfrac{\fa{5}}{20} + \dfrac{\fb{4}}{20} = \fc{\dfrac{9}{20}}', 320, 60, ein=1.0),
            graf(streifen(Y1, 4, 1, 1) + [T(X0, Y1 + 1.6, '1/4', 1, 'start')] + streifen(Y2, 5, 1, 2) + [T(X0, Y2 + 1.6, '1/5', 2, 'start')], ein=0.05),
            graf(streifen(Y3, 20, 5, 1) + [RECHT(X0 + BW * 5 / 20, Y3, BW * 4 / 20, BH, 2, 0.45, dicke=0), T(X0, Y3 + 1.6, '9/20', 3, 'start')],
                 ein=1.0)),
         sz('Frage 4',
            'Gemeinsamer Nenner zwölf: zehn Zwölftel minus drei Zwölftel ergibt sieben Zwölftel.',
            f(r'\dfrac{5}{6} - \dfrac{1}{4} = \dfrac{\fa{10}}{12} - \dfrac{\fb{3}}{12} = \fc{\dfrac{7}{12}}', 320, 60, ein=1.0)),
         sz('Frage 5',
            'Zwei Siebtel ist kleiner als ein Drittel. Die Summe muss aber grösser sein als jeder Summand. Richtig sind sieben Zwölftel.',
            f(r'\fd{\dfrac{2}{7}} \lt \dfrac{1}{3}', 320, 62, ein=1.0),
            f(r'\dfrac{1}{3} + \dfrac{1}{4} = \dfrac{4}{12} + \dfrac{3}{12} = \fc{\dfrac{7}{12}}', 460, 56, ein=1.0),
            graf(streifen(Y1, 3, 1, 1) + [T(X0, Y1 + 1.6, '1/3', 1, 'start')] + streifen(Y2, 7, 2, 4) + [T(X0, Y2 + 1.6, '2/7', 4, 'start')]
                 + [S((X0 + BW / 3, Y2 - 0.3), (X0 + BW / 3, Y1 + BH + 0.3), 5, True, 3)], ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Zuerst den kleinsten gemeinsamen Nenner suchen, dann Zähler und Nenner erweitern, dann die Zähler verrechnen und kürzen. '
            'Und eine schnelle Probe: Ist das Ergebnis überhaupt möglich?',
            titel('Zum Mitnehmen', 250, 76),
            n('Hauptnenner, erweitern, Zähler verrechnen, kürzen|Probe: Ist das Ergebnis möglich?', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', '3/10 + 1/10 = ?', ['2/5', '4/20', '4/10'], 0,
              {0: 'Ja.', 1: 'Gleich grosse Stücke werden gezählt — der Nenner bleibt 10.', 2: 'Richtig gerechnet — aber noch nicht gekürzt.'},
              sprich='Drei Zehntel plus ein Zehntel gleich?',
              rueck_sprich={1: 'Gleich grosse Stücke werden gezählt. Der Nenner bleibt zehn.', 2: 'Richtig gerechnet, aber noch nicht gekürzt.'}),
         wahl('Frage 2', 'Welches ist der Hauptnenner von 3/8 und 5/12?', ['24', '96', '48'], 0,
              {0: 'Ja.', 1: '96 = 8 · 12 geht, ist aber nicht der kleinste gemeinsame Nenner.', 2: '48 ist ein gemeinsamer Nenner — gibt es einen kleineren?'},
              sprich='Welches ist der kleinste gemeinsame Nenner von drei Achteln und fünf Zwölfteln?',
              rueck_sprich={1: 'Sechsundneunzig, also acht mal zwölf, geht, ist aber nicht der kleinste gemeinsame Nenner.',
                            2: 'Achtundvierzig ist ein gemeinsamer Nenner. Gibt es einen kleineren?'}),
         wahl('Frage 3', '1/4 + 1/5 = ?', ['9/20', '2/9', '2/20'], 0,
              {0: 'Ja.', 1: 'Nenner addiert: 2/9 ist sogar kleiner als 1/4.', 2: 'Der Hauptnenner 20 stimmt — beim Erweitern auch die Zähler multiplizieren.'},
              sprich='Ein Viertel plus ein Fünftel gleich?',
              rueck_sprich={1: 'Hier wurden die Nenner addiert. Zwei Neuntel ist sogar kleiner als ein Viertel.',
                            2: 'Der gemeinsame Nenner zwanzig stimmt. Beim Erweitern auch die Zähler multiplizieren.'}),
         wahl('Frage 4', '5/6 − 1/4 = ?', ['7/12', '4/2', '4/12'], 0,
              {0: 'Ja.', 1: 'Zähler minus Zähler, Nenner minus Nenner geht beim Subtrahieren genauso wenig.',
               2: 'Der Hauptnenner 12 stimmt — beim Erweitern auch die Zähler multiplizieren.'},
              sprich='Fünf Sechstel minus ein Viertel gleich?',
              rueck_sprich={1: 'Zähler minus Zähler, Nenner minus Nenner geht beim Subtrahieren genauso wenig.',
                            2: 'Der gemeinsame Nenner zwölf stimmt. Beim Erweitern auch die Zähler multiplizieren.'}),
         wahl('Frage 5', 'Jemand rechnet 1/3 + 1/4 = 2/7. Woran siehst du ohne Rechnen, dass das falsch ist?',
              ['2/7 ist kleiner als 1/3.', '2/7 ist nicht gekürzt.', '7 ist eine Primzahl.'], 0,
              {0: 'Ja.', 1: '2/7 ist vollständig gekürzt — der Fehler liegt woanders.', 2: 'Auch eine Primzahl darf im Nenner stehen.'},
              sprich='Jemand rechnet ein Drittel plus ein Viertel gleich zwei Siebtel. Woran siehst du ohne Rechnen, dass das falsch ist?',
              rueck_sprich={1: 'Zwei Siebtel ist vollständig gekürzt. Der Fehler liegt woanders.', 2: 'Auch eine Primzahl darf im Nenner stehen.'}),
     ], art='Kontrollclip')


# ════════════════════════════════════════════════ Kapitel 3 · Einführung: Multiplizieren und Dividieren
Q0, QS = 0.5, 9.0                 # Einheitsquadrat 0.5 … 9.5


def flaeche(a, b, c, d, ein_c=None, ein_a=None, ein_g=None, mit_zahlen=None):
    """Flächenmodell a/b · c/d: orange die unteren c von d Zeilen (Höhe), blau die linken a von b Spalten (Breite),
    grün das Rechteck, das zu beiden gehört. Sobald Grün erscheint, werden Blau und Orange dort ausgespart —
    sonst mischen sich drei Füllungen zu einem dunklen Fleck. Teilstriche erscheinen mit ihrer Farbe."""
    def zeit(fg, ein=None, aus=None):
        return mit(fg, ein=ein, aus=aus)
    f_ = []
    voll_o = RECHT(Q0, Q0, QS, QS * c / d, 2, 0.3, dicke=0)
    voll_b = RECHT(Q0, Q0, QS * a / b, QS, 1, 0.3, dicke=0)
    rest_o = RECHT(Q0 + QS * a / b, Q0, QS * (b - a) / b, QS * c / d, 2, 0.3, dicke=0)
    rest_b = RECHT(Q0, Q0 + QS * c / d, QS * a / b, QS * (d - c) / d, 1, 0.3, dicke=0)
    gruen = RECHT(Q0, Q0, QS * a / b, QS * c / d, 3, 0.35, dicke=4)
    if ein_g is None or isinstance(ein_g, (int, float)) and ein_g <= 0.05:
        f_ += [rest_o, rest_b, gruen]
    else:
        f_ += [zeit(voll_o, ein_c, ein_g), zeit(voll_b, ein_a, ein_g), zeit(rest_o, ein_g), zeit(rest_b, ein_g), zeit(gruen, ein_g)]
    f_ += [zeit(S((Q0, Q0 + QS * j / d), (Q0 + QS, Q0 + QS * j / d), 5, dicke=2), ein_c) for j in range(1, d)]
    f_ += [zeit(S((Q0 + QS * j / b, Q0), (Q0 + QS * j / b, Q0 + QS), 5, dicke=2), ein_a) for j in range(1, b)]
    f_.append(RECHT(Q0, Q0, QS, QS, 5, 0, dicke=4))
    if mit_zahlen:
        k = 0
        for j in range(c):
            for i in range(a):
                k += 1
                f_.append(mit(T(Q0 + QS * (i + 0.5) / b, Q0 + QS * (j + 0.5) / d - 0.25, str(k), 5, g=36), ein='%s+%.2f' % (mit_zahlen, 0.25 * (k - 1))))
    return f_


def messen(a, b, c, d, y=OBEN, ein=None, schritt=0.55, zahlen=True, start=0.0):
    """Wie oft passt c/d in a/b? Blau der Streifen a/b (Länge des Ganzen = 9), darunter c/d-Stücke nacheinander."""
    f_ = [RECHT(X0, y, BW, BH, 5, 0, dicke=2), RECHT(X0, y, BW * a / b, BH, 1, 0.35, dicke=3)]
    st, k, p = BW * c / d, 0, 0.0
    while p + 1e-9 < BW * a / b:
        br = min(st, BW * a / b - p)
        o = start + schritt * k
        z = ('%s%+.2f' % (ein, o)) if isinstance(ein, str) else round((ein or 0) + o, 2)
        f_.append(mit(RECHT(X0 + p, y - 1.6, br, BH, 2, 0.45 if br > st - 1e-9 else 0.15, dicke=3), ein=z))
        if zahlen and br > st - 1e-9:
            f_.append(mit(T(X0 + p + br / 2, y - 1.6 + 0.35, str(k + 1), 5, g=32), ein=z))
        p += st
        k += 1
    return f_


clip('malnehmen', 5, 'Brüche sehen: Multiplizieren und Dividieren',
     'Flächenmodell für 2/3 · 3/4 = 6/12 = 1/2; Zähler mal Zähler, Nenner mal Nenner; über Kreuz kürzen (4/9 · 3/8 = 1/6); '
     'ganze Zahl mal Bruch; 3/4 : 1/8 als «Wie oft passt?» (6) und der Kehrwert; Kehrwert vom falschen Bruch als Fehler.',
     ['Multiplizieren', 'Dividieren', 'Kehrwert', 'Flächenmodell', 'Kürzen'], [
         sz('Von',
            'Was sind zwei Drittel von drei Vierteln? Im Quadrat färben wir zuerst drei Viertel der Höhe, dann zwei Drittel '
            'der Breite. Das Rechteck, das zu beiden gehört, ist das Ergebnis.',
            f(r'\dfrac{\fa{2}}{\fa{3}} \cdot \dfrac{\fb{3}}{\fb{4}}', 330, 76, ein=0.5),
            n('«von» heisst «mal»', 480, 'blau', 44, ein='@Was'),
            graf(flaeche(2, 3, 3, 4, ein_c='@Höhe', ein_a='@Breite', ein_g='@beiden'), ein=0.3)),
         sz('Zählen',
            'Das Quadrat hat jetzt zwölf Kästchen, sechs davon sind grün. Zähler mal Zähler gibt sechs, Nenner mal Nenner '
            'gibt zwölf: sechs Zwölftel, gekürzt ein Halb.',
            f(r'\dfrac{2}{3} \cdot \dfrac{3}{4} = \dfrac{2 \cdot 3}{3 \cdot 4} = \dfrac{\fc{6}}{12} = \fc{\dfrac{1}{2}}', 330, 60, ein='@Zähler'),
            n('Zähler mal Zähler,|Nenner mal Nenner', 500, 'blau', 44, ein='@Nenner'),
            graf(flaeche(2, 3, 3, 4, mit_zahlen='@sechs'), ein=0.05)),
         sz('Vorher kürzen',
            'Vier Neuntel mal drei Achtel. Bevor wir ausrechnen, kürzen wir über Kreuz: vier und acht durch vier, drei und neun '
            'durch drei. Es bleibt ein Sechstel, und die Zahlen bleiben klein.',
            f(r'\dfrac{4}{9} \cdot \dfrac{3}{8} = \dfrac{\fa{4} \cdot \fb{3}}{\fb{9} \cdot \fa{8}}', 300, 60, ein='@Neuntel'),
            n('@4@ und @8@: durch @4@|@3@ und @9@: durch @3@', 440, 'blau', 42, ein='@Kreuz'),
            f(r'= \dfrac{\fa{1} \cdot \fb{1}}{\fb{3} \cdot \fa{2}} = \fc{\dfrac{1}{6}}', 600, 60, ein='@bleibt')),
         sz('Ganze Zahl',
            'Bei einer ganzen Zahl wird nur der Zähler multipliziert: drei mal zwei Fünftel sind sechs Fünftel, mehr als ein Ganzes. '
            'Und zwei Drittel von zwölf sind acht.',
            f(r'3 \cdot \dfrac{2}{5} = \dfrac{3 \cdot 2}{5} = \fc{\dfrac{6}{5}}', 320, 60, ein='@drei'),
            f(r'\dfrac{2}{3} \cdot 12 = \dfrac{24}{3} = \fc{8}', 470, 60, ein='@zwölf'),
            # Zahlenstrahl 0 … 1.5, das Ganze = 6 Einheiten: dreimal 2/5 = 2.4 hintereinander, zusammen 7.2 → 6/5
            graf([S((X0, OBEN - 0.5), (X0 + 9, OBEN - 0.5), 5, False, 3), T(X0, OBEN - 1.3, '0', 5),
                  S((X0 + 6, OBEN - 0.9), (X0 + 6, OBEN + BH + 0.5), 5, True, 3), T(X0 + 6, OBEN - 1.3, '1', 5)]
                 + [mit(RECHT(X0 + 2.4 * k, OBEN, 2.4, BH, 1, 0.35, dicke=3), ein='@mal+%.2f' % (0.4 * k)) for k in range(3)]
                 + [mit(T(X0 + 1.2 + 2.4 * k, OBEN + 0.4, '2/5', 1, g=30), ein='@mal+%.2f' % (0.4 * k)) for k in range(3)]
                 + [mit(T(X0 + 3.6, OBEN + 2.2, '6/5', 3), ein='@sechs')], ein=0.3)),
         sz('Messen',
            'Und das Teilen? Drei Viertel durch ein Achtel fragt: Wie oft passt ein Achtel in drei Viertel? Wir legen Achtel '
            'hinein. Es passt genau sechsmal.',
            f(r'\dfrac{\fa{3}}{\fa{4}} : \dfrac{\fb{1}}{\fb{8}} = \;?', 300, 66, ein=0.5),
            f(r'\dfrac{3}{4} : \dfrac{1}{8} = \fc{6}', 450, 66, ein='@sechsmal'),
            graf(messen(3, 4, 1, 8, ein='@hinein', schritt=0.45, start=-1.2) + [T(X0, OBEN + 1.6, '3/4', 1, 'start'), T(X0, OBEN - 2.4, 'Stücke zu 1/8', 2, 'start')],
                 ein=0.3)),
         sz('Kehrwert',
            'Und drei Viertel mal acht gibt ebenfalls sechs. Teilen durch einen Bruch heisst: mit seinem Kehrwert '
            'multiplizieren. Den Kehrwert erhält man, indem man Zähler und Nenner vertauscht.',
            f(r'\dfrac{3}{4} \cdot 8 = \dfrac{24}{4} = \fc{6}', 290, 58, ein='@acht'),
            f(r'\dfrac{a}{b} : \dfrac{c}{d} = \dfrac{a}{b} \cdot \dfrac{\fb{d}}{\fb{c}}', 430, 66, ein='@Kehrwert'),
            n('Kehrwert: Zähler und Nenner vertauscht|(@b, c, d \\neq 0@)', 580, 'blau', 42, ein='@vertauscht')),
         sz('Falscher Bruch',
            'Umgedreht wird der zweite Bruch, durch den man teilt. Wer den ersten umdreht, rechnet vier Drittel mal ein Achtel '
            'und erhält ein Sechstel. Das ist falsch.',
            f(r'\dfrac{3}{4} : \dfrac{1}{8} = \dfrac{3}{4} \cdot \dfrac{\fb{8}}{\fb{1}} = \fc{6}', 300, 58, ein='@zweite'),
            f(r'\fd{\dfrac{4}{3} \cdot \dfrac{1}{8} = \dfrac{1}{6}}', 450, 58, ein='@ersten'),
            n('Kehrwert vom zweiten Bruch', 590, 'blau', 44, ein='@falsch')),
         sz('Merke',
            'Zum Mitnehmen: Beim Multiplizieren Zähler mal Zähler und Nenner mal Nenner, vorher kürzen. Beim Dividieren mit dem '
            'Kehrwert des zweiten Bruchs multiplizieren. Teilen fragt: Wie oft passt es hinein?',
            titel('Zum Mitnehmen', 250, 76),
            n('mal: Zähler @\\cdot@ Zähler, Nenner @\\cdot@ Nenner|vorher über Kreuz kürzen|durch: mal Kehrwert des zweiten Bruchs',
              400, 'blau', 44, ein=1.2)),
         jetzt_du(),
     ], [
         wahl('Messen', 'Wie oft passt 1/8 in 3/4?', ['6-mal', '3-mal', '8-mal'], 0,
              {0: 'Ja.', 1: '3 ist der Zähler von 3/4. Zähl gleich mit, wie viele Achtel hineinpassen.',
               2: 'In ein Ganzes passen 8 Achtel — hier sind es aber nur drei Viertel.'},
              sprich='Wie oft passt ein Achtel in drei Viertel?',
              rueck_sprich={1: 'Drei ist der Zähler von drei Vierteln. Zähl gleich mit, wie viele Achtel hineinpassen.',
                            2: 'In ein Ganzes passen acht Achtel. Hier sind es aber nur drei Viertel.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 3 · Kontrolle
clip('kontrolle-malnehmen', 6, 'Brüche sehen: Kontrollfragen zum Multiplizieren und Dividieren',
     'Fünf Fragen: 2/5 · 3/4, eine Multiplikation am Flächenmodell ablesen, 4/5 : 2/3, wie oft 1/6 in 2/3 passt, 5 · 2/7.',
     ['Multiplizieren', 'Dividieren', 'Kehrwert', 'Kontrollfragen'], [
         sz('Frage 1',
            'Zähler mal Zähler und Nenner mal Nenner: sechs Zwanzigstel, gekürzt drei Zehntel.',
            f(r'\dfrac{2}{5} \cdot \dfrac{3}{4} = \dfrac{6}{20} = \fc{\dfrac{3}{10}}', 320, 64, ein=1.0),
            graf(flaeche(2, 5, 3, 4), ein=1.0)),
         sz('Frage 2',
            'Blau ist ein Drittel der Breite, orange drei Viertel der Höhe. Grün sind drei von zwölf Kästchen: ein Viertel.',
            f(r'\dfrac{1}{3} \cdot \dfrac{3}{4} = \dfrac{3}{12} = \fc{\dfrac{1}{4}}', 320, 64, ein=1.0),
            graf(flaeche(1, 3, 3, 4, ein_c=0.05, ein_a=0.05, ein_g=1.0), ein=0.05)),
         sz('Frage 3',
            'Mit dem Kehrwert des zweiten Bruchs: vier Fünftel mal drei Halbe, zwölf Zehntel, gekürzt sechs Fünftel.',
            f(r'\dfrac{4}{5} : \dfrac{2}{3} = \dfrac{4}{5} \cdot \dfrac{\fb{3}}{\fb{2}} = \dfrac{12}{10} = \fc{\dfrac{6}{5}}', 320, 58, ein=1.0)),
         sz('Frage 4',
            'Zwei Drittel sind vier Sechstel. Ein Sechstel passt also viermal hinein.',
            f(r'\dfrac{2}{3} : \dfrac{1}{6} = \dfrac{2}{3} \cdot 6 = \fc{4}', 320, 62, ein=1.0),
            graf(messen(2, 3, 1, 6, ein=1.0, schritt=0.3) + [T(X0, OBEN + 1.6, '2/3', 1, 'start')], ein=0.05)),
         sz('Frage 5',
            'Nur der Zähler wird mit fünf multipliziert: zehn Siebtel. Wer auch den Nenner multipliziert, hat nur erweitert.',
            f(r'5 \cdot \dfrac{2}{7} = \dfrac{5 \cdot 2}{7} = \fc{\dfrac{10}{7}}', 320, 62, ein=1.0),
            f(r'\fd{\dfrac{5 \cdot 2}{5 \cdot 7} = \dfrac{2}{7}}', 460, 56, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Mal heisst Zähler mal Zähler und Nenner mal Nenner. Durch heisst mal den Kehrwert des zweiten Bruchs.',
            titel('Zum Mitnehmen', 250, 76),
            n('mal: Zähler @\\cdot@ Zähler, Nenner @\\cdot@ Nenner|durch: mal Kehrwert des zweiten Bruchs', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', '2/5 · 3/4 = ?', ['3/10', '8/15', '5/9'], 0,
              {0: 'Ja.', 1: 'Das wäre geteilt (über Kreuz multipliziert). Mal: Zähler mal Zähler, Nenner mal Nenner.',
               2: 'Das wäre Zähler plus Zähler, Nenner plus Nenner — beim Multiplizieren wird multipliziert.'},
              sprich='Zwei Fünftel mal drei Viertel gleich?',
              rueck_sprich={1: 'Das wäre geteilt, über Kreuz multipliziert. Mal heisst: Zähler mal Zähler, Nenner mal Nenner.',
                            2: 'Das wäre Zähler plus Zähler, Nenner plus Nenner. Beim Multiplizieren wird multipliziert.'}),
         wahl('Frage 2', 'Welche Rechnung zeigt das Bild?', ['1/3 · 3/4 = 1/4', '1/3 + 3/4', '3/4 : 1/3'], 0,
              {0: 'Ja.', 1: 'Zwei Anteile, die sich überlappen — das ist das Flächenmodell für Mal.',
               2: 'Teilen fragt «Wie oft passt?» — im Bild überlappen sich zwei Anteile.'},
              sprich='Welche Rechnung zeigt das Bild?',
              rueck_sprich={1: 'Zwei Anteile, die sich überlappen: Das ist das Flächenmodell für Mal.',
                            2: 'Teilen fragt: Wie oft passt es? Im Bild überlappen sich zwei Anteile.'}),
         wahl('Frage 3', '4/5 : 2/3 = ?', ['6/5', '8/15', '5/6'], 0,
              {0: 'Ja.', 1: 'Kehrwert vergessen: Durch einen Bruch teilen heisst mit seinem Kehrwert multiplizieren.',
               2: 'Den Kehrwert vom zweiten Bruch nehmen, nicht vom ersten.'},
              sprich='Vier Fünftel durch zwei Drittel gleich?',
              rueck_sprich={1: 'Kehrwert vergessen. Durch einen Bruch teilen heisst mit seinem Kehrwert multiplizieren.',
                            2: 'Den Kehrwert vom zweiten Bruch nehmen, nicht vom ersten.'}),
         wahl('Frage 4', 'Wie oft passt 1/6 in 2/3?', ['4-mal', '3-mal', '1/9-mal'], 0,
              {0: 'Ja.', 1: 'Schreib 2/3 in Sechsteln: Wie viele Sechstel sind es?', 2: '1/9 wäre 2/3 · 1/6 — das ist mal, nicht durch.'},
              sprich='Wie oft passt ein Sechstel in zwei Drittel?',
              rueck_sprich={1: 'Schreib zwei Drittel in Sechsteln. Wie viele Sechstel sind es?', 2: 'Ein Neuntel wäre mal, nicht durch.'}),
         wahl('Frage 5', '5 · 2/7 = ?', ['10/7', '10/35', '7/10'], 0,
              {0: 'Ja.', 1: '10/35 = 2/7: Wer auch den Nenner mal 5 nimmt, hat nur erweitert.', 2: 'Das ist der Kehrwert des Ergebnisses — richtig ist mehr als 1.'},
              sprich='Fünf mal zwei Siebtel gleich?',
              rueck_sprich={1: 'Zehn Fünfunddreissigstel sind zwei Siebtel. Wer auch den Nenner mal fünf nimmt, hat nur erweitert.',
                            2: 'Das ist der Kehrwert des Ergebnisses. Richtig ist mehr als ein Ganzes.'}),
     ], art='Kontrollclip')


# ════════════════════════════════════════════════ Kapitel 4 · Einführung: Rechenreihenfolge und negative Brüche
# Rechenbaum für 1/2 − 1/3 · (3/4 − 1/4): Wurzel «−», links 1/2, rechts «·» mit 1/3 und der Klammer «( − )» mit 3/4 und 1/4.
KN = {'w': (3.8, 8.6), 'h': (1.2, 6.3), 'm': (6.0, 6.3), 'd': (4.2, 4.0), 'k': (7.6, 4.0), 'a': (6.4, 1.7), 'b': (8.8, 1.7)}


def baum(ein_k, ein_m, ein_w):
    """Rechenbaum: Rechenzeichen in Kreisen, Zahlen als Blätter. Was zuerst gerechnet wird, steht unten. Ist ein Knoten
    ausgerechnet, wird sein Kreis grün und das Ergebnis steht rechts daneben (frei von den Linien, in zahlen.py nicht nötig:
    reine Lage)."""
    f_ = []
    for p, q in (('w', 'h'), ('w', 'm'), ('m', 'd'), ('m', 'k'), ('k', 'a'), ('k', 'b')):
        # Linie vom Kreisrand des oberen Knotens bis knapp über das Blatt bzw. an den Kreisrand des unteren
        (x1, y1), (x2, y2) = KN[p], KN[q]
        lang = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        r1, r2 = 0.8, (0.8 if q in 'mk' else 0.5)
        f_.append(S((x1 + (x2 - x1) * r1 / lang, y1 + (y2 - y1) * r1 / lang), (x2 - (x2 - x1) * r2 / lang, y2 - (y2 - y1) * r2 / lang), 5, False, 2))
    for k_, t_, g_ in (('w', '−', 54), ('m', '·', 70), ('k', '(−)', 42)):
        f_.append(KR(KN[k_], 0.7, 5, 0.0, 3))
        f_.append(T(KN[k_][0], KN[k_][1] - 0.3, t_, 5, g=g_))
    for k_, t_ in (('h', '1/2'), ('d', '1/3'), ('a', '3/4'), ('b', '1/4')):
        f_.append(T(KN[k_][0], KN[k_][1] - 0.25, t_, 1, g=38))
    for k_, ein in (('k', ein_k), ('m', ein_m), ('w', ein_w)):
        f_.append(mit(KR(KN[k_], 0.8, 3, 0.0, 6), ein=ein))
    f_.append(mit(T(KN['k'][0] + 1.0, KN['k'][1] - 0.25, '= 1/2', 3, g=36, anker='start'), ein=ein_k))
    f_.append(mit(T(KN['m'][0] + 1.0, KN['m'][1] - 0.25, '= 1/6', 3, g=36, anker='start'), ein=ein_m))
    f_.append(mit(T(KN['w'][0] + 1.0, KN['w'][1] - 0.25, '= 1/3', 3, g=36, anker='start'), ein=ein_w))
    return f_


clip('reihenfolge', 7, 'Brüche sehen: Rechenreihenfolge und negative Brüche',
     'Klammer, Potenz, Punkt vor Strich, von links nach rechts am Rechenbaum von 1/2 − 1/3 · (3/4 − 1/4) = 1/3; '
     'Vorzeichen wie in ℤ ((−3/4) · (−2/9) = 1/6); (2/3)² = 4/9 im Flächenmodell; (−1/2)² gegen −(1/2)²; Minus vor der Klammer.',
     ['Rechenreihenfolge', 'Punkt vor Strich', 'Klammer', 'negative Brüche', 'Potenz'], [
         sz('Regeln',
            'In welcher Reihenfolge wird gerechnet? Zuerst die Klammern, dann die Potenzen, dann Punkt vor Strich. '
            'Was gleichrangig ist, von links nach rechts.',
            n('1  Klammern', 300, 'blau', 50, ein='@Klammern'),
            n('2  Potenzen', 400, 'blau', 50, ein='@Potenzen'),
            n('3  Punkt vor Strich: @\\cdot@ und @:@ vor @+@ und @-@', 500, 'blau', 50, ein='@Punkt'),
            n('4  gleichrangig: von links nach rechts', 600, 'blau', 50, ein='@gleichrangig')),
         sz('Beispiel',
            'Ein Halb minus ein Drittel mal die Klammer drei Viertel minus ein Viertel. Zuerst die Klammer: zwei Viertel, '
            'also ein Halb. Dann Punkt vor Strich: ein Drittel mal ein Halb ist ein Sechstel. Zuletzt ein Halb minus ein '
            'Sechstel: drei Sechstel minus ein Sechstel, und das ist ein Drittel.',
            # Fragebild: Die Frage «Was zuerst?» kommt bei 0.3 s — die Markierung der Klammer und der Baum erst danach.
            mit(f(r'\dfrac{1}{2} - \dfrac{1}{3} \cdot \left(\dfrac{3}{4} - \dfrac{1}{4}\right)', 280, 52, ein=0.05), aus='@Zuerst'),
            f(r'\dfrac{1}{2} - \dfrac{1}{3} \cdot \left(\fb{\dfrac{3}{4} - \dfrac{1}{4}}\right)', 280, 52, ein='@Zuerst'),
            f(r'= \dfrac{1}{2} - \fb{\dfrac{1}{3} \cdot \dfrac{1}{2}}', 400, 52, ein='@Dann'),
            f(r'= \dfrac{1}{2} - \dfrac{1}{6} = \dfrac{3}{6} - \dfrac{1}{6}', 520, 52, ein='@Zuletzt'),
            f(r'= \fc{\dfrac{1}{3}}', 640, 52, ein='@Drittel#3'),
            graf(baum('@zwei', '@Sechstel', '@Drittel#3'), ein='@Klammer')),
         sz('Vorzeichen',
            'Mit negativen Brüchen gelten dieselben Vorzeichenregeln wie bei ganzen Zahlen. Minus drei Viertel mal minus zwei '
            'Neuntel: Minus mal Minus gibt Plus. Sechs Sechsunddreissigstel, gekürzt ein Sechstel.',
            f(r'-\dfrac{2}{3} = \dfrac{-2}{3} = \dfrac{2}{-3}', 290, 54, ein='@negativen'),
            f(r'\left(-\dfrac{3}{4}\right) \cdot \left(-\dfrac{2}{9}\right) = +\dfrac{6}{36} = \fc{\dfrac{1}{6}}', 430, 52, ein='@Neuntel'),
            n('@-@ mal @-@ gibt @+@,  @-@ mal @+@ gibt @-@', 580, 'blau', 44, ein='@Plus')),
         sz('Potenz',
            'Bei einer Potenz werden Zähler und Nenner potenziert. Zwei Drittel im Quadrat ist zwei Drittel mal zwei Drittel, '
            'im Flächenmodell vier von neun Kästchen: vier Neuntel.',
            f(r'\left(\dfrac{2}{3}\right)^2 = \dfrac{2^2}{3^2} = \fc{\dfrac{4}{9}}', 330, 62, ein='@Quadrat'),
            graf(flaeche(2, 3, 2, 3, ein_c='@mal', ein_a='@mal', ein_g='@Flächenmodell'), ein=0.3)),
         sz('Klammer beim Minus',
            'Auf die Klammer kommt es an. Minus ein Halb in Klammern im Quadrat ist plus ein Viertel. Ohne Klammer wird zuerst '
            'quadriert und dann das Minus gesetzt: minus ein Viertel.',
            f(r'\left(-\dfrac{1}{2}\right)^2 = \fc{+\dfrac{1}{4}}', 300, 60, ein='@plus'),
            f(r'-\left(\dfrac{1}{2}\right)^2 = \fc{-\dfrac{1}{4}}', 440, 60, ein='@Ohne'),
            n('Potenz vor Strich', 580, 'blau', 44, ein='@quadriert')),
         sz('Minus vor der Klammer',
            'Vorsicht beim Minus vor einer Klammer. Drei Viertel minus die Klammer ein Halb minus ein Viertel: Zuerst die Klammer, '
            'ein Viertel. Das Ergebnis ist ein Halb. Wer die Klammer einfach weglässt, erhält null. Das ist falsch.',
            f(r'\dfrac{3}{4} - \left(\fb{\dfrac{1}{2} - \dfrac{1}{4}}\right) = \dfrac{3}{4} - \fb{\dfrac{1}{4}} = \fc{\dfrac{1}{2}}', 300, 50, ein='@Zuerst'),
            f(r'\fd{\dfrac{3}{4} - \dfrac{1}{2} - \dfrac{1}{4} = 0}', 450, 52, ein='@weglässt'),
            n('Ohne Klammer: @\\tfrac{3}{4} - \\tfrac{1}{2} + \\tfrac{1}{4}@', 590, 'blau', 44, ein='@falsch')),
         sz('Merke',
            'Zum Mitnehmen: Klammer, Potenz, Punkt vor Strich, sonst von links nach rechts. Vorzeichen wie bei den ganzen Zahlen. '
            'Und jeden Schritt in eine eigene Zeile.',
            titel('Zum Mitnehmen', 250, 76),
            n('Klammer, Potenz, Punkt vor Strich, links nach rechts|Vorzeichen wie in @\\mathbb{Z}@|jeder Schritt eine Zeile',
              400, 'blau', 44, ein=1.2)),
         jetzt_du('im Schrittwähler'),
     ], [
         wahl('Beispiel', 'Was wird hier zuerst gerechnet?', ['die Klammer', '1/2 − 1/3', '1/3 · (…)'], 0,
              {0: 'Ja.', 1: 'Punkt vor Strich — und noch vorher die Klammer.', 2: 'Fast: Bevor man mit der Klammer multipliziert, muss sie ausgerechnet sein.'},
              sprich='Was wird hier zuerst gerechnet?',
              rueck_sprich={1: 'Punkt vor Strich, und noch vorher die Klammer.', 2: 'Fast. Bevor man mit der Klammer multipliziert, muss sie ausgerechnet sein.'}),
     ])

# ════════════════════════════════════════════════ Kapitel 4 · Kontrolle
clip('kontrolle-reihenfolge', 8, 'Brüche sehen: Kontrollfragen zur Rechenreihenfolge',
     'Fünf Fragen: Punkt vor Strich bei 2/5 + 3/5 · 1/3, von links nach rechts bei 3/4 : 1/4 · 1/3, (−2/5) · (−5/6), −(3/4)², '
     'Minus vor der Klammer bei 2/3 − (1/2 − 1/6).',
     ['Rechenreihenfolge', 'Punkt vor Strich', 'negative Brüche', 'Kontrollfragen'], [
         sz('Frage 1',
            'Punkt vor Strich: zuerst drei Fünftel mal ein Drittel, das ist ein Fünftel. Dann zwei Fünftel plus ein Fünftel: drei Fünftel.',
            f(r'\dfrac{2}{5} + \fb{\dfrac{3}{5} \cdot \dfrac{1}{3}} = \dfrac{2}{5} + \dfrac{1}{5} = \fc{\dfrac{3}{5}}', 320, 56, ein=1.0)),
         sz('Frage 2',
            'Gleichrangig, also von links nach rechts: drei Viertel durch ein Viertel ist drei. Drei mal ein Drittel ist eins.',
            f(r'\fb{\dfrac{3}{4} : \dfrac{1}{4}} \cdot \dfrac{1}{3} = 3 \cdot \dfrac{1}{3} = \fc{1}', 320, 58, ein=1.0),
            f(r'\fd{\dfrac{3}{4} : \dfrac{1}{12} = 9}', 460, 54, ein=1.0)),
         sz('Frage 3',
            'Minus mal Minus gibt Plus. Zehn Dreissigstel, gekürzt ein Drittel.',
            f(r'\left(-\dfrac{2}{5}\right) \cdot \left(-\dfrac{5}{6}\right) = +\dfrac{10}{30} = \fc{\dfrac{1}{3}}', 320, 54, ein=1.0)),
         sz('Frage 4',
            'Zuerst wird quadriert: neun Sechzehntel. Dann kommt das Minus: minus neun Sechzehntel.',
            f(r'-\left(\dfrac{3}{4}\right)^2 = -\dfrac{9}{16}', 320, 60, ein=1.0),
            graf(flaeche(3, 4, 3, 4), ein=1.0)),
         sz('Frage 5',
            'Zuerst die Klammer: ein Halb minus ein Sechstel ist ein Drittel. Zwei Drittel minus ein Drittel ist ein Drittel.',
            f(r'\dfrac{2}{3} - \left(\fb{\dfrac{1}{2} - \dfrac{1}{6}}\right) = \dfrac{2}{3} - \fb{\dfrac{1}{3}} = \fc{\dfrac{1}{3}}', 320, 50, ein=1.0)),
         sz('Merke',
            'Zum Mitnehmen: Erst überlegen, was zuerst dran ist, dann rechnen. Und das Vorzeichen getrennt bestimmen.',
            titel('Zum Mitnehmen', 250, 76),
            n('zuerst: Was ist dran?|Vorzeichen getrennt bestimmen', 400, 'blau', 44, ein=1.2)),
     ], [
         wahl('Frage 1', 'Was rechnest du bei 2/5 + 3/5 · 1/3 zuerst?', ['3/5 · 1/3', '2/5 + 3/5', 'egal'], 0,
              {0: 'Ja.', 1: 'Punkt vor Strich: Das Mal kommt vor dem Plus.', 2: 'Nicht egal: (2/5 + 3/5) · 1/3 = 1/3, richtig ist 3/5.'},
              sprich='Was rechnest du bei zwei Fünftel plus drei Fünftel mal ein Drittel zuerst?',
              rueck_sprich={1: 'Punkt vor Strich: Das Mal kommt vor dem Plus.', 2: 'Nicht egal. Mit der falschen Reihenfolge kommt ein Drittel heraus, richtig sind drei Fünftel.'}),
         wahl('Frage 2', '3/4 : 1/4 · 1/3 = ?', ['1', '9', '1/9'], 0,
              {0: 'Ja.', 1: '9 entsteht, wenn zuerst 1/4 · 1/3 gerechnet wird. Gleichrangig heisst: von links nach rechts.',
               2: 'Rechne von links nach rechts: zuerst 3/4 : 1/4.'},
              sprich='Drei Viertel durch ein Viertel mal ein Drittel gleich?',
              rueck_sprich={1: 'Neun entsteht, wenn zuerst ein Viertel mal ein Drittel gerechnet wird. Gleichrangig heisst: von links nach rechts.',
                            2: 'Rechne von links nach rechts: zuerst drei Viertel durch ein Viertel.'}),
         wahl('Frage 3', '(−2/5) · (−5/6) = ?', ['1/3', '−1/3', '−10/11'], 0,
              {0: 'Ja.', 1: 'Vorzeichen: Minus mal Minus gibt Plus.', 2: 'Beim Multiplizieren: Zähler mal Zähler, Nenner mal Nenner — und Minus mal Minus gibt Plus.'},
              sprich='Minus zwei Fünftel mal minus fünf Sechstel gleich?',
              rueck_sprich={1: 'Vorzeichen: Minus mal Minus gibt Plus.', 2: 'Beim Multiplizieren Zähler mal Zähler, Nenner mal Nenner, und Minus mal Minus gibt Plus.'}),
         wahl('Frage 4', '−(3/4)² = ?', ['−9/16', '9/16', '−3/2'], 0,
              {0: 'Ja.', 1: 'Das Minus steht ausserhalb der Klammer: Erst quadrieren, dann das Minus.',
               2: 'Quadrieren heisst mit sich selbst multiplizieren, nicht mal 2.'},
              sprich='Minus Klammer drei Viertel im Quadrat gleich?',
              rueck_sprich={1: 'Das Minus steht ausserhalb der Klammer: Erst quadrieren, dann das Minus.',
                            2: 'Quadrieren heisst mit sich selbst multiplizieren, nicht mal zwei.'}),
         wahl('Frage 5', '2/3 − (1/2 − 1/6) = ?', ['1/3', '0', '1'], 0,
              {0: 'Ja.', 1: '0 entsteht, wenn man die Klammer einfach weglässt: 2/3 − 1/2 − 1/6. Das Minus gilt für die ganze Klammer.',
               2: 'Rechne zuerst die Klammer aus: 1/2 − 1/6.'},
              sprich='Zwei Drittel minus Klammer ein Halb minus ein Sechstel gleich?',
              rueck_sprich={1: 'Null entsteht, wenn man die Klammer einfach weglässt. Das Minus gilt für die ganze Klammer.',
                            2: 'Rechne zuerst die Klammer aus: ein Halb minus ein Sechstel.'}),
     ], art='Kontrollclip')

if FEHLT:
    print('ohne gemessene Wortzeit (geschätzt):', len(FEHLT))
