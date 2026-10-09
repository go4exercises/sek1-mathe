"""Baut leitprogramme/terme-faktorisieren.html aus einer Kapitelbeschreibung (09.10.2026).

  python3 scripts/lp/terme-faktorisieren/seite.py

Leitprogramm Terme und Faktorisieren (Bereich Arithmetik/Algebra), Gerüst aus scripts/lp/bruchrechnen/.
Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026); vertieft wird auf den Themenseiten von
Mathe begreifbar (TALS). Alles kommt aus diesem Ordner: kopf.css, seite.css, basis.js (Thema, Fortschritt,
Schiene), seite.js (Simulationen, Übungen mit Termeingabe). Nur der SEO-Block wird aus der bestehenden Seite
übernommen — ihn schreibt scripts/build-seo.py. Wiederholbar. Danach Pre-Flight und build-seo.py.
"""
import json
import os

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/terme-faktorisieren.html'
NAME = 'Terme und Faktorisieren'
STAND = 'Stand 9. Oktober 2026'
CLIP = 'terme-lp-'

SEO_AUF = '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->'
SEO_ZU = '<!-- SEO:ENDE -->'
seo = SEO_AUF + '\n' + SEO_ZU
if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
    if SEO_AUF in alt:
        seo = alt[alt.index(SEO_AUF):alt.index(SEO_ZU) + len(SEO_ZU)]

# Vertiefung: Themenseite von Mathe begreifbar (Berufsmaturität), in neuem Tab
TALS = 'https://mathe.begreifbar.ch/grundlagen/'
def tals(seite, text, anker=''):
    return f'<a href="{TALS}{seite}{anker}" target="_blank" rel="noopener">{text} ↗</a>'
TT = 'g1-3-algebraische-terme.html'
V_ZUS = tals(TT, 'Gleichartige Glieder zusammenfassen', '#zusammenfassen')
V_KL = tals(TT, 'Klammern auflösen', '#klammern')
V_BIN = tals(TT, 'Binomische Formeln', '#binomi')
V_FAK = tals(TT, 'Faktorisieren', '#faktorisieren')
V_BRT = tals(TT, 'Bruchterme', '#bruchterme')


def uebung(typ, titel):
    return f'''<div class="uebung" data-typ="{typ}">
          <div class="ue-kopf"><span class="ue-titel">🔁 {titel}</span><span class="ue-serie">0 in Folge</span></div>
          <p class="ue-aufgabe"></p>
          <div class="ue-zeile"><span class="ue-eingabe"></span><button type="button" class="ue-pruefen">Prüfen</button><button type="button" class="ue-tipp">💡 Tipp</button><button type="button" class="ue-neu">Neue Zahlen</button></div>
          <div class="ue-tipps" aria-live="polite"></div>
          <div class="ue-rueck" aria-live="polite"></div>
        </div>'''


def test(tid, titel, punkte, aufgaben, zwei=False):
    lis = []
    for nr, p, frage, loes, extra in aufgaben:
        lis.append(f'''          <li>
            <div class="frage"><span class="nr">{nr}</span><span class="pkt">({p} P)</span><span class="txt">{frage}</span></div>{extra}
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox">{loes}</div></details>
          </li>''')
    assert sum(a[1] for a in aufgaben) == punkte, (tid, punkte, sum(a[1] for a in aufgaben))
    return f'''<div class="test" data-test="{tid}">
        <div class="test-kopf">
          <h3>{titel} <span class="summe">· {punkte} P</span></h3>
          <span class="werkz"><button type="button" class="alle-loesungen">alle Lösungen</button><label title="Aufgaben auf Papier gelöst und mit den Lösungen verglichen — ob alles sitzt, zeigt der Gesamttest."><input type="checkbox" class="erledigt" aria-label="Aufgaben dieses Kapitels bearbeitet"> bearbeitet</label></span>
        </div>
        <ol class="aufg{' zwei' if zwei else ''}">
{chr(10).join(lis)}
        </ol>
      </div>'''


def dauer(name):
    """Clipzeit aus dem Drehbuch (Summe der gemessenen Szenen, ohne Nachlauf), abgerundet (HOWTO-leitprogramme §7)."""
    p = R + 'clips/' + name + '.json'
    if not os.path.exists(p):
        return '0:00'
    t = int(sum(q.get('dauer', 0) for q in json.load(open(p))['szenen']))
    return '%d:%02d' % (t // 60, t % 60)


def clipkarte(datei, titel):
    return f'''<div class="clipkarte kap-clip" data-clip="clips/{datei}.html" data-titel="{titel}">
        <button class="clip-start" type="button">
          <span class="clip-play" aria-hidden="true">▶</span>
          <span class="clip-txt"><span class="clip-titel">{titel}</span></span>
          <span class="clip-zeit">{dauer(datei)}</span>
        </button>
      </div>'''


def kapitel(n, kid, titel, zeit, ziel, clip1, sim, clip2, festhalten, uebungen, aufgaben, mehr, komp):
    ue = '\n        '.join(uebungen)
    return f'''
    <section class="kap" id="k{n}">
      <div class="kap-meta"><span class="marker">Kapitel {n}</span><span class="abz abz-th">{komp}</span><span class="zeit">≈ {zeit} min</span></div>
      <h2 id="{kid}">{titel}</h2>
      <p class="ziel">{ziel}</p>

      <p class="phase"><span>①</span> Clip</p>
      {clipkarte(*clip1)}

      <p class="phase"><span>②</span> Tüfteln</p>
{sim}

      <p class="phase"><span>③</span> Kontrollfragen</p>
      {clipkarte(*clip2)}

      <h3>Festhalten</h3>
{festhalten}

      <p class="phase"><span>④</span> Üben mit Rückmeldung</p>
      <div class="duo">
        {ue}
      </div>

      <p class="phase"><span>⑤</span> Aufgaben mit Lösungen</p>
{aufgaben}
      <p class="ausf">Vertiefung bei Mathe begreifbar (Berufsmaturität): {mehr}</p>
    </section>'''


def regler(sid, name, akz, mn, mx, wert):
    return (f'<div class="sl-grp akz-{akz}"><label for="{sid}"><span class="var">{name}</span></label>'
            f'<input type="range" id="{sid}" min="{mn}" max="{mx}" step="1" value="{wert}"><span class="sl-val"></span></div>')


def rechteck(a, b, label):
    return f'\n            <div class="mini-reihe"><svg class="mini-term" data-rechteck="{a},{b}" aria-label="{label}"></svg></div>'



# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1" aria-label="Termkacheln: einen Term zusammenfassen">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 360 165" role="img" aria-label="Oben der Term der Aufgabe als Kacheln, unten dein Term"></svg>
        <div class="sl-row">
          {regler('s1-a', 'x-Kacheln', 'blau', -6, 8, 1)}
          {regler('s1-b', 'Einer', 'orange', -9, 9, 0)}
        </div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Terme vereinfachen</div>
          <p><b>Zusammenfassen:</b> Nur <b>gleichartige</b> Glieder lassen sich addieren, also Glieder mit derselben Variable und derselben Hochzahl. \(3x + 5x = 8x\), aber \(3x + 5\) bleibt, wie es ist. Das Vorzeichen gehört zum Glied dahinter.</p>
          <p><b>Zahl vor der Klammer:</b> Sie wird mit <b>jedem</b> Glied in der Klammer multipliziert (Distributivgesetz):</p>
          <p>\[ 3(2x - 4) = 6x - 12 \qquad -2(x - 3) = -2x + 6 \]</p>
          <p><b>Minus vor der Klammer:</b> Klammer weglassen und <b>jedes</b> Vorzeichen darin umdrehen:</p>
          <ol class="weg">
            <li>\(7x - (2x - 5) = 7x - 2x + 5\) <span class="warum">aus \(-5\) wird \(+5\)</span></li>
            <li>\(= 5x + 5\) <span class="warum">gleichartige Glieder zusammenfassen</span></li>
          </ol>
          <p><b>Verschachtelte Klammern:</b> innen beginnen. \(4x - (2x - 3(1 - x)) = 4x - (2x - 3 + 3x) = 4x - (5x - 3) = 3 - x\).</p>
          <p><b>Probe:</b> Für \(x\) eine Zahl einsetzen, zum Beispiel \(x = 2\). Gleichwertige Terme geben dasselbe: \(7 \cdot 2 - (2 \cdot 2 - 5) = 15\) und \(5 \cdot 2 + 5 = 15\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Minus nur beim ersten Glied:</b> \(7x - (2x - 5)\) ist nicht \(7x - 2x - 5\). Das Minus gilt für die ganze Klammer.</p>
          <p><b>Nur das erste Glied multipliziert:</b> \(3(x + 4)\) ist nicht \(3x + 4\), sondern \(3x + 12\).</p>
          <p><b>Ungleichartiges zusammengezählt:</b> \(3x + 2\) ist nicht \(5x\). Probe mit \(x = 2\): \(8\) gegen \(10\).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 14, [
    ('1a', 2, r'Fasse zusammen: \(5a + 3 - 2a + 7\) und \(x^2 + 4x - 2x^2 + x\)',
     r'<p>\(5a - 2a = 3a\) und \(3 + 7 = 10\): \(3a + 10\). Bei der zweiten: \(x^2 - 2x^2 = -x^2\) und \(4x + x = 5x\): \(-x^2 + 5x\).</p>', ''),
    ('1b', 2, r'Löse die Klammer auf: \(4(3x - 2)\) und \(-3(2 - x)\)',
     r'<p>\(4 \cdot 3x - 4 \cdot 2 = 12x - 8\). \(-3 \cdot 2 + (-3) \cdot (-x) = -6 + 3x\).</p>', ''),
    ('1c', 3, r'Vereinfache: \(6x - (4 - 2x) + 3(x - 1)\)',
     r'<p>\(6x - 4 + 2x + 3x - 3 = 11x - 7\).</p><p class="komm">Probe mit \(x = 1\): \(6 - 2 + 0 = 4\) und \(11 - 7 = 4\).</p>', ''),
    ('1d', 3, r'Vereinfache, von innen nach aussen: \(2x - (x - 2(3 - x))\)',
     r'<p>Innen: \(x - 2(3 - x) = x - 6 + 2x = 3x - 6\). Dann \(2x - (3x - 6) = 2x - 3x + 6 = -x + 6\).</p>', ''),
    ('1e', 2, r'Ben rechnet: \(8x - (3x - 5) = 5x - 5\). Prüfe mit \(x = 1\), finde den Fehler und rechne richtig.',
     r'<p>Mit \(x = 1\): links \(8 - (3 - 5) = 10\), Bens Ergebnis \(5 - 5 = 0\). Ben hat das Minus nur auf \(3x\) angewendet. Richtig: \(8x - 3x + 5 = 5x + 5\).</p>', ''),
    ('1f', 2, r'Mit \(x = 1\) ist \(3x + 2 = 5\) und \(5x = 5\). Sind \(3x + 2\) und \(5x\) also gleichwertig? Begründe.',
     r'<p>Nein. Gleichwertig heisst: gleich für <b>jede</b> Zahl. Mit \(x = 2\) ist \(3x + 2 = 8\), aber \(5x = 10\). Ein einziges Gegenbeispiel genügt. \(3x\) und \(2\) sind nicht gleichartig.</p>', ''),
])
k1 = kapitel(1, 'vereinfachen', 'Terme vereinfachen', 40,
             r'Du fasst gleichartige Glieder zusammen, löst Klammern auf, auch mit Minus davor und verschachtelt, und prüfst dein Ergebnis durch Einsetzen.',
             (CLIP + 'zusammenfassen', 'Terme vereinfachen'), sim1,
             (CLIP + 'kontrolle-zusammenfassen', 'Kontrollfragen zum Vereinfachen'), fest1,
             [uebung('zusammenfassen', 'Zusammenfassen'), uebung('klammern', 'Klammern auflösen')],
             auf1, V_ZUS + ' · ' + V_KL, komp='K1')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2" aria-label="Klammer mal Klammer: Flächenmodell und Rechteckschema">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 240" role="img" aria-label="Rechteck aus einem x-Quadrat, x-Streifen und Einerkacheln"></svg>
        <table class="schema" aria-label="Rechteckschema"></table>
        <div class="sl-row">
          {regler('s2-a', 'Zahl links', 'blau', -6, 6, 1)}
          {regler('s2-b', 'Zahl oben', 'orange', -6, 6, 1)}
        </div>
      </figure>'''
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Klammer mal Klammer</div>
          <p><b>Jedes</b> Glied der ersten Klammer wird mit <b>jedem</b> Glied der zweiten multipliziert. Das gibt vier Produkte, danach wird zusammengefasst.</p>
          <p><b>Flächenmodell:</b> Ein Rechteck mit den Seiten \(x + 2\) und \(x + 3\) besteht aus vier Teilen: \(x^2\), \(3x\), \(2x\) und \(6\).</p>''' + rechteck(2, 3, 'Rechteck mit Seiten x plus 2 und x plus 3, aufgeteilt in x-Quadrat, fünf x-Streifen und sechs Einerkacheln') + r'''
          <p>\[ (x + 2)(x + 3) = x^2 + 3x + 2x + 6 = x^2 + 5x + 6 \]</p>
          <p><b>Rechteckschema:</b> Es funktioniert auch mit Minus. Das Vorzeichen gehört zur Zahl dahinter.</p>
          <table class="schema"><tr><th>·</th><th>\(3x\)</th><th>\(-2\)</th></tr><tr><th>\(x\)</th><td class="t-q">\(3x^2\)</td><td class="t-x">\(-2x\)</td></tr><tr><th>\(+4\)</th><td class="t-x">\(12x\)</td><td class="t-z">\(-8\)</td></tr></table>
          <p>\[ (3x - 2)(x + 4) = 3x^2 + 12x - 2x - 8 = 3x^2 + 10x - 8 \]</p>
          <p><b>Probe</b> mit \(x = 1\): \((1 + 2)(1 + 3) = 12\) und \(1 + 5 + 6 = 12\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Nur «vorne mal vorne, hinten mal hinten»:</b> \((x + 2)(x + 3)\) ist nicht \(x^2 + 6\). Im Flächenmodell fehlen die beiden Streifen. Probe mit \(x = 1\): \(12\) gegen \(7\).</p>
          <p><b>Vorzeichen verloren:</b> Bei \((3x - 2)(x + 4)\) ist das letzte Produkt \((-2) \cdot 4 = -8\), nicht \(+8\).</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 14, [
    ('2a', 2, r'Multipliziere aus: \((x + 4)(x + 5)\)',
     r'<p>\(x^2 + 5x + 4x + 20 = x^2 + 9x + 20\).</p>', ''),
    ('2b', 3, r'Multipliziere aus: \((2x - 3)(x + 6)\)',
     r'<p>\(2x^2 + 12x - 3x - 18 = 2x^2 + 9x - 18\).</p><p class="komm">Probe mit \(x = 1\): \((-1) \cdot 7 = -7\) und \(2 + 9 - 18 = -7\).</p>', ''),
    ('2c', 2, r'Multipliziere aus: \((a - 4)(a - 7)\)',
     r'<p>\(a^2 - 7a - 4a + 28 = a^2 - 11a + 28\). Minus mal Minus gibt \(+28\).</p>', ''),
    ('2d', 2, r'Lara rechnet: \((x + 5)(x - 2) = x^2 - 10\). Was hat sie vergessen? Rechne richtig.',
     r'<p>Sie hat nur die ersten und die letzten Glieder multipliziert. Es fehlen \(-2x\) und \(5x\). Richtig: \(x^2 - 2x + 5x - 10 = x^2 + 3x - 10\).</p>', ''),
    ('2e', 2, r'Welches Produkt zeigt das Flächenmodell? Schreib es als Produkt und als Summe.',
     r'<p>Seiten \(x + 1\) und \(x + 4\): \((x + 1)(x + 4) = x^2 + 5x + 4\). Im Bild: ein \(x^2\), fünf x-Streifen, vier Einer.</p>',
     rechteck(1, 4, 'Rechteck: ein x-Quadrat, fünf x-Streifen, vier Einerkacheln')),
    ('2f', 3, r'Multipliziere \((x + 3)(x - 3)\) aus. Warum kommt kein Glied mit \(x\) vor?',
     r'<p>\(x^2 - 3x + 3x - 9 = x^2 - 9\). Die beiden gemischten Produkte sind \(-3x\) und \(+3x\). Sie heben sich auf, weil die Zahlen \(3\) und \(-3\) Gegenzahlen sind.</p>', ''),
])
k2 = kapitel(2, 'ausmultiplizieren', 'Klammer mal Klammer', 40,
             r'Du multiplizierst zwei Klammern aus, mit dem Flächenmodell oder dem Rechteckschema, fasst zusammen und machst die Probe durch Einsetzen.',
             (CLIP + 'ausmultiplizieren', 'Klammer mal Klammer'), sim2,
             (CLIP + 'kontrolle-ausmultiplizieren', 'Kontrollfragen zum Ausmultiplizieren'), fest2,
             [uebung('ausmult', 'Ausmultiplizieren'), uebung('koeffizienten', 'Summe und Produkt')],
             auf2, V_KL, komp='K2')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3" aria-label="Binomische Formeln am Quadrat">
        <div class="leiste" aria-live="polite"></div>
        <label class="sim-schalter">Formel <select class="sim-wahl" aria-label="Binomische Formel">
          <option value="plus" selected>(a + b)²</option>
          <option value="minus">(a − b)²</option>
          <option value="produkt">(a + b)(a − b)</option>
        </select></label>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 300 300" role="img" aria-label="Quadrat oder Rechteck, aufgeteilt in Teilflächen"></svg>
        <div class="sl-row">
          {regler('s3-a', 'a', 'blau', 2, 8, 4)}
          {regler('s3-b', 'b', 'orange', 1, 4, 1)}
        </div>
      </figure>'''
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Binomische Formeln</div>
          <p>\[ (a + b)^2 = a^2 + 2ab + b^2 \]</p>
          <p>\[ (a - b)^2 = a^2 - 2ab + b^2 \]</p>
          <p>\[ (a + b)(a - b) = a^2 - b^2 \]</p>
          <p>Im Quadrat mit der Seite \(a + b\) siehst du die vier Teile: \(a^2\), zweimal \(ab\) und \(b^2\). Darum steht in der Mitte <b>\(2ab\)</b>.</p>
          <div class="mini-reihe"><svg class="mini-term" data-binom="1" aria-label="Quadrat mit Seite a plus b: Quadrat a mal a, zwei Rechtecke a mal b, Quadrat b mal b"></svg></div>
          <p>Für \(a\) und \(b\) darf alles stehen, auch \(2y\) oder eine Zahl:</p>
          <p>\[ (x + 4)^2 = x^2 + 8x + 16 \qquad (2y - 3)^2 = 4y^2 - 12y + 9 \qquad (5 + x)(5 - x) = 25 - x^2 \]</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Das mittlere Glied vergessen:</b> \((a + b)^2\) ist nicht \(a^2 + b^2\). Mit Zahlen: \((3 + 4)^2 = 49\), aber \(3^2 + 4^2 = 25\).</p>
          <p><b>\(ab\) statt \(2ab\):</b> Es sind zwei Rechtecke. \((x + 4)^2\) hat in der Mitte \(8x\), nicht \(4x\).</p>
          <p><b>Die Zahl vor der Variable nicht quadriert:</b> \((2y)^2 = 4y^2\), nicht \(2y^2\).</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 14, [
    ('3a', 2, r'Rechne mit der binomischen Formel: \((x + 6)^2\) und \((x - 1)^2\)',
     r'<p>\(x^2 + 12x + 36\) und \(x^2 - 2x + 1\).</p>', ''),
    ('3b', 2, r'Rechne: \((3a - 2)^2\)',
     r'<p>\((3a)^2 - 2 \cdot 3a \cdot 2 + 2^2 = 9a^2 - 12a + 4\).</p>', ''),
    ('3c', 2, r'Rechne: \((x + 7)(x - 7)\) und \((4 - y)(4 + y)\)',
     r'<p>\(x^2 - 49\) und \(16 - y^2\).</p>', ''),
    ('3d', 2, r'Tom schreibt \((x + 5)^2 = x^2 + 25\). Zeige mit \(x = 1\), dass das falsch ist, und rechne richtig.',
     r'<p>Mit \(x = 1\): \((1 + 5)^2 = 36\), aber \(1 + 25 = 26\). Es fehlt das mittlere Glied: \((x + 5)^2 = x^2 + 10x + 25\).</p>', ''),
    ('3e', 3, r'Kopfrechnen mit den Formeln: \(21^2\) und \(19 \cdot 21\)',
     r'<p>\(21^2 = (20 + 1)^2 = 400 + 40 + 1 = 441\). \(19 \cdot 21 = (20 - 1)(20 + 1) = 400 - 1 = 399\).</p>', ''),
    ('3f', 3, r'Das Quadrat hat die Seite \(a + b\). Benenne die vier Teilflächen und erkläre damit, warum \((a + b)^2\) grösser ist als \(a^2 + b^2\).',
     r'<p>Oben links \(a^2\), unten rechts \(b^2\), dazu zwei Rechtecke mit je \(ab\). Zusammen \(a^2 + 2ab + b^2\). In \(a^2 + b^2\) fehlen die beiden Rechtecke, also \(2ab\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini-term" data-binom="1" aria-label="Quadrat mit Seite a plus b, in vier Teile geteilt"></svg></div>'),
])
k3 = kapitel(3, 'binome', 'Binomische Formeln', 40,
             r'Du wendest die drei binomischen Formeln an, auch mit Zahlen vor der Variable, erklärst das mittlere Glied am Quadrat und rechnest damit im Kopf.',
             (CLIP + 'binome', 'Binomische Formeln'), sim3,
             (CLIP + 'kontrolle-binome', 'Kontrollfragen zu den binomischen Formeln'), fest3,
             [uebung('binom', 'Binomische Formeln'), uebung('binomluecke', 'Lücken füllen')],
             auf3, V_BIN, komp='K3')

# ------------------------------------------------------------------ Kapitel 4
sim4 = f'''      <figure class="sim sim-gross" id="sim4" aria-label="Faktorisierer: zwei Klammern zu einem Ergebnis finden">
        <div class="leiste" aria-live="polite"></div>
        <p class="sim-ziel" data-rolle="ziel" aria-live="polite"></p>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <table class="schema" aria-label="Rechteckschema"></table>
        <div class="sl-row">
          {regler('s4-m', 'Zahl links', 'blau', -9, 9, 1)}
          {regler('s4-n', 'Zahl oben', 'orange', -9, 9, 1)}
        </div>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Faktorisieren</div>
          <p><b>Faktorisieren</b> heisst: eine Summe als <b>Produkt</b> schreiben. Es ist das Ausmultiplizieren rückwärts. Prüfe in dieser Reihenfolge:</p>
          <ol>
            <li><b>Ausklammern:</b> den grössten gemeinsamen Faktor vor die Klammer. \(6a^2 - 9a = 3a(2a - 3)\), denn \(\text{ggT}(6;\ 9) = 3\) und jedes Glied enthält \(a\).</li>
            <li><b>Binomische Formel rückwärts:</b> \(y^2 - 10y + 25 = (y - 5)^2\) und \(9y^2 - 25 = (3y - 5)(3y + 5)\).</li>
            <li><b>Zweiklammersatz:</b> Bei \(x^2 + px + q\) zwei Zahlen suchen, deren <b>Produkt</b> \(q\) und deren <b>Summe</b> \(p\) ist.</li>
          </ol>
          <ol class="weg">
            <li>\(x^2 - 7x + 12\) <span class="warum">Produkt \(12\), Summe \(-7\)</span></li>
            <li>Paare mit Produkt \(12\): \(1 \cdot 12\), \(2 \cdot 6\), \(3 \cdot 4\) und dieselben negativ <span class="warum">Summe \(-7\) hat nur \(-3\) und \(-4\)</span></li>
            <li>\(= (x - 3)(x - 4)\) <span class="warum">Probe: ausmultiplizieren</span></li>
          </ol>
          <p><b>Vollständig</b> faktorisiert ist ein Term, wenn sich kein Faktor weiter zerlegen lässt: \(5x^2 - 20 = 5(x^2 - 4) = 5(x - 2)(x + 2)\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Nicht alles ausgeklammert:</b> \(6a^2 - 9a = a(6a - 9)\) stimmt, ist aber nicht fertig. \(6\) und \(9\) haben noch den Faktor \(3\).</p>
          <p><b>Summe statt Produkt gesucht:</b> Bei \(x^2 - 7x + 12\) bestimmt das <b>Produkt</b> die Zahl am Schluss, die <b>Summe</b> das Glied mit \(x\).</p>
          <p><b>Vorzeichen:</b> \((x + 3)(x + 4)\) gibt \(x^2 + 7x + 12\), nicht \(x^2 - 7x + 12\). Probe machen!</p>
          <p><b>Faktorisieren ist kein Gleichungslösen:</b> Bei «Faktorisiere \(x^2 - 25\)» ist \((x - 5)(x + 5)\) die Antwort, nicht «\(x = 5\)».</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 15, [
    ('4a', 2, r'Klammere so viel wie möglich aus: \(8x + 12\) und \(5y^2 - 15y\)',
     r'<p>\(4(2x + 3)\), denn \(\text{ggT}(8;\ 12) = 4\). \(5y(y - 3)\), denn \(5\) und \(y\) stecken in beiden Gliedern.</p>', ''),
    ('4b', 3, r'Faktorisiere mit einer binomischen Formel: \(x^2 + 14x + 49\) und \(4a^2 - 1\)',
     r'<p>\(49 = 7^2\) und \(14x = 2 \cdot x \cdot 7\): \((x + 7)^2\). \(4a^2 = (2a)^2\) und \(1 = 1^2\): \((2a - 1)(2a + 1)\).</p>', ''),
    ('4c', 3, r'Faktorisiere: \(x^2 + 9x + 14\) und \(x^2 - 3x - 10\)',
     r'<p>Produkt \(14\), Summe \(9\): \(2\) und \(7\), also \((x + 2)(x + 7)\). Produkt \(-10\), Summe \(-3\): \(-5\) und \(2\), also \((x - 5)(x + 2)\).</p>', ''),
    ('4d', 2, r'Mia soll \(x^2 - 9\) faktorisieren und schreibt «\(x = 3\)». Was hat sie falsch verstanden? Gib die richtige Antwort.',
     r'<p>Mia hat eine Gleichung gelöst. Gesucht ist aber ein Produkt, das gleichwertig zu \(x^2 - 9\) ist: \((x - 3)(x + 3)\).</p>', ''),
    ('4e', 3, r'Faktorisiere vollständig: \(2x^2 - 18\)',
     r'<p>Zuerst ausklammern: \(2(x^2 - 9)\). Dann die dritte binomische Formel: \(2(x - 3)(x + 3)\).</p>', ''),
    ('4f', 2, r'Warum lässt sich \(x^2 + 4\) nicht als \((x + m)(x + n)\) mit ganzen Zahlen schreiben?',
     r'<p>Es bräuchte \(m + n = 0\) (kein Glied mit \(x\)) und \(m \cdot n = 4\). Aus \(m + n = 0\) folgt \(n = -m\), dann ist \(m \cdot n = -m^2\) nie positiv. Eine Summe von zwei Quadraten zerfällt nicht.</p>', ''),
])
k4 = kapitel(4, 'faktorisieren', 'Faktorisieren', 45,
             r'Du schreibst Summen als Produkte: durch Ausklammern, mit den binomischen Formeln rückwärts und mit dem Zweiklammersatz. Du faktorisierst vollständig und prüfst durch Ausmultiplizieren.',
             (CLIP + 'faktorisieren', 'Faktorisieren'), sim4,
             (CLIP + 'kontrolle-faktorisieren', 'Kontrollfragen zum Faktorisieren'), fest4,
             [uebung('ausklammern', 'Ausklammern'), uebung('faktorisieren', 'Faktorisieren')],
             auf4, V_FAK, komp='K4')

# ------------------------------------------------------------------ Vorwissen
k0 = f'''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-th">Vorwissen</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Rechnen mit negativen Zahlen, Distributivgesetz, Potenzen, Einsetzen, grösster gemeinsamer Teiler. Zuerst kurz wiederholen, dann der Vortest.</p>
''' + r'''      <details class="anleitung">
        <summary><h3>Kurz wiederholt</h3></summary>
        <ul class="kurz">
          <li><b>Vorzeichen:</b> Minus mal Minus gibt Plus, verschiedene Vorzeichen geben Minus: \((-3) \cdot (-2) = 6\), \((-3) \cdot 2 = -6\).</li>
          <li><b>Distributivgesetz:</b> \(3 \cdot (4 + 5) = 3 \cdot 4 + 3 \cdot 5\). Die Zahl vor der Klammer wird mit jedem Summanden multipliziert.</li>
          <li><b>Variable:</b> Ein Buchstabe steht für eine Zahl. \(3x\) heisst \(3 \cdot x\), \(x^2\) heisst \(x \cdot x\).</li>
          <li><b>Einsetzen:</b> Für \(x = 3\) ist \(2x^2 = 2 \cdot 3^2 = 18\). Potenz vor Punkt.</li>
          <li><b>ggT</b> (grösster gemeinsamer Teiler): die grösste Zahl, durch die beide teilbar sind, zum Beispiel \(\text{ggT}(12;\ 18) = 6\). Braucht es zum Ausklammern.</li>
        </ul>
      </details>
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Berechne: \((-3) \cdot (-4)\); \(\;-2 \cdot 5\); \(\;-7 + 3\); \(\;-4 - 6\)',
     r'<p>\(12\); \(-10\); \(-4\); \(-10\).</p>', ''),
    ('0b', 2, r'Berechne \(3 \cdot (4 + 5)\) auf zwei Arten.',
     r'<p>Klammer zuerst: \(3 \cdot 9 = 27\). Ausmultipliziert: \(12 + 15 = 27\).</p><p class="komm">Das zweite ist das Distributivgesetz, die Grundlage von Kapitel 1 und 2.</p>', ''),
    ('0c', 2, r'Schreib kürzer: \(x \cdot x\); \(\;3x \cdot 2x\); \(\;(-2x) \cdot 5\)',
     r'<p>\(x^2\); \(6x^2\); \(-10x\).</p>', ''),
    ('0d', 2, r'Setze \(x = 3\) ein: \(2x^2 - x\)',
     r'<p>\(2 \cdot 9 - 3 = 15\).</p><p class="komm">Einsetzen ist die Probe in allen Kapiteln.</p>', ''),
    ('0e', 2, r'Bestimme \(\text{ggT}(12;\ 18)\) und \(\text{ggT}(8;\ 20)\).',
     r'<p>\(6\) und \(4\).</p><p class="komm">Braucht es in Kapitel 4 zum Ausklammern.</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: «Kurz wiederholt» nochmals lesen, die Lösungen des Vortests Schritt für Schritt nachrechnen, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/terme-faktorisieren/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-th">Kapitel 1–4</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg, ohne Taschenrechner.<br>
              <a class="pdf-knopf" href="{PDF}gesamttest.pdf" download>⬇ Gesamttest (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">2</span><div><b>Bewerten</b> — selbst mit dem Punkteraster oder mit einer KI: Lösung scannen oder fotografieren (ohne Namen und Standort). Das Paket enthält die Musterlösung: erst danach öffnen.<br>
              <a class="pdf-knopf" href="{PDF}bewertungspaket.pdf" download>⬇ Bewertungspaket (PDF)</a></div></div>
            <div class="pdf-schritt"><span class="nr">3</span><div><b>Gezielt wiederholen</b> — nach der Tabelle unten.</div></div>
          </div>
        </div>
        <div class="bewertung">
          <b>Selbsteinschätzung</b>
          <table>
            <tr><td>22 – 25 P</td><td>Die geprüften Teile sitzen. Wo du Punkte verloren hast: das Kapitel dieser Aufgabe nochmals (Zuordnung unten).</td></tr>
            <tr><td>17 – 21 P</td><td>Den schwächsten Teil nochmals — gemessen am Anteil (Teil A 5, B 8, C 12 P): Tüfteln und Übungen der Kapitel dieses Teils.</td></tr>
            <tr><td>11 – 16 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 10 P</td><td>Zurück zu den Kapiteln jedes Teils, in dem du weniger als die Hälfte erreicht hast; sind es alle drei, zum Vortest und zu Kapitel 1.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1, G2 → 1; G3 → 2; G4, G5 → 3; G6 bis G9 → 4</p>
        </div>
      </div>
    </section>'''

# ------------------------------------------------------------------ Vertiefung (freiwillig, ohne Punkte)
vt = r'''
    <section class="kap" id="vertiefung">
      <div class="vertiefung">
        <h2 id="vertiefung-titel">Vertiefung — zum Knobeln</h2>
        <p class="komm">Freiwillig, ohne Punkte. Für alle, die nach dem Gesamttest weiterdenken möchten.</p>
        <ol class="aufg">
          <li>
            <div class="frage"><span class="nr">V1</span><span class="txt">Berechne \(4^2 - 3^2\), \(5^2 - 4^2\), \(6^2 - 5^2\). Was fällt auf? Begründe mit \((n + 1)^2 - n^2\).</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\(7\), \(9\), \(11\): immer ungerade, und zwar die Summe der beiden Zahlen. \((n + 1)^2 - n^2 = n^2 + 2n + 1 - n^2 = 2n + 1\).</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V2</span><span class="txt">Zahlen mit \(5\) am Ende quadrieren: \(35^2 = 1225\), denn \(3 \cdot 4 = 12\), dann \(25\) anhängen. Prüfe den Trick an \(45^2\) und erkläre ihn mit \((10a + 5)^2\).</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\(45^2 = 2025\), und \(4 \cdot 5 = 20\), dann \(25\). Allgemein: \((10a + 5)^2 = 100a^2 + 100a + 25 = 100 \cdot a(a + 1) + 25\).</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V3</span><span class="txt">Setze \(x = 10\) in \(x^2 + 5x + 6\) und in \((x + 2)(x + 3)\) ein. Zerlege damit \(156\) in zwei Faktoren.</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\(100 + 50 + 6 = 156\) und \(12 \cdot 13 = 156\). Faktorisieren zerlegt also auch Zahlen.</p></div></details>
          </li>
        </ol>
      </div>
      <p class="ausf weiter">Weiter: Was hier bewusst fehlt (Terme mit mehreren Variablen, Bruchterme kürzen) steht bei Mathe begreifbar unter ''' + V_FAK + ' und ' + V_BRT + r'''.</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Terme und Faktorisieren, Version 1.0 (09.10.2026). Gebaut aus scripts/lp/terme-faktorisieren/seite.py —
     Änderungen dort, nicht in dieser Datei. Grundlagen: HOWTO-leitprogramme.md (Kapitelmuster) und
     ~/HOWTO-TODO-BM-Vorkurs-LP01-02.md, Abschnitt LP 02 (Terme und Faktorisieren), für die Sek I umgesetzt.

     Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026): Das Leitprogramm ist selbst die fachliche Quelle;
     Vertiefungslinks zeigen auf Mathe begreifbar (TALS). Notation nach STYLEGUIDE.md und CLAUDE.md: Dezimalpunkt,
     ggT mit Strichpunkt, «gleichartige Glieder», «Zweiklammersatz» (wie TALS), «vollständig faktorisiert».

     Kompetenzen — eigene Formulierung, ohne Lehrplan-Nummern (CLAUDE.md: keine erfundenen Lehrplan-Stellen):
       K1  Terme vereinfachen: zusammenfassen, Klammern auflösen (auch Minus davor, verschachtelt), Probe
       K2  Klammer mal Klammer ausmultiplizieren (Flächenmodell, Rechteckschema)
       K3  Die drei binomischen Formeln anwenden und am Quadrat begründen
       K4  Faktorisieren: ausklammern, binomisch rückwärts, Zweiklammersatz, vollständig; Fehler finden
     Alles ohne Taschenrechner.

     Kompetenzmatrix (Kompetenz | Kapitel | Simulation | Übungen | Kapitelaufgaben | Gesamttest):
       K1 | 1 | Sim 1 | zusammenfassen, klammern     | 1a–1f | G1, G2
       K2 | 2 | Sim 2 | ausmult, koeffizienten       | 2a–2f | G3
       K3 | 3 | Sim 3 | binom, binomluecke           | 3a–3f | G4, G5
       K4 | 4 | Sim 4 | ausklammern, faktorisieren   | 4a–4f | G6–G9

     Planung (Kapitel | Lernziel | Erkundung | Beispiel | Häufiger Fehler | min):
       0 | Vorwissen       | –                     | –                       | –                                | 10
       1 | vereinfachen    | Termkacheln           | 7x − (2x − 5) = 5x + 5  | Minus nur beim ersten Glied      | 40
       2 | ausmultiplizieren | Flächenmodell/Schema | (x + 2)(x + 3)         | (x + 2)(x + 3) = x² + 6          | 40
       3 | binomische Formeln | Quadrat             | (x + 4)²                | mittleres Glied fehlt            | 40
       4 | faktorisieren   | Faktorisierer         | x² − 7x + 12            | unvollständig; Gleichung gelöst  | 45
       Gesamttest (PDF) 30 · Summe 205 min ≈ 4.6 Lektionen. Vertiefung V1–V3 freiwillig, nicht eingerechnet.

     Clips: je Kapitel ein Einführungsclip (mit einer Vorhersagefrage) und ein Kontrollclip mit fünf Fragen,
     Reihe «Terme sehen», terme-lp-*.json, erzeugt mit scripts/lp/terme-faktorisieren/clips.py (probe: nicht
     in der Bibliothek). Die Erkundungen benutzen andere Zahlen als Clip und Festhalten (HOWTO §15).

     Farben: x² und x blau, Zahlen orange, negative Kacheln und Fehler rot, Ergebnis grün; Bereichsfarbe Petrol.
     Gesamttest und Bewertungspaket nur als PDF (downloads/leitprogramme/terme-faktorisieren/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Sek1-Mathe begreifbar · Leitprogramm</p>
      <h1>Terme und Faktorisieren</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Arithmetik/Algebra</span>
    </div>
  </div>
</header>

<div class="huelle">
<div class="raster">

  <nav class="schiene" aria-label="Kapitelnavigation">
    <h2 id="ablauf">Ablauf</h2>
    <p class="lekt">Vorab</p>
    <ol>
      <li><a href="#k0"><span class="nr">0</span><span>Vorwissen</span></a></li>
    </ol>
    <p class="lekt">Kapitel</p>
    <ol>
      <li><a href="#k1"><span class="nr">1</span><span>Vereinfachen</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Klammer mal Klammer</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Binomische Formeln</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Faktorisieren</span></a></li>
    </ol>
    <p class="lekt">Abschluss</p>
    <ol>
      <li><a href="#gesamttest"><span class="nr">✓</span><span>Gesamttest</span></a></li>
      <li><a href="#vertiefung"><span class="nr">★</span><span>Vertiefung</span></a></li>
    </ol>
    <div class="fortschritt">
      <div class="balken"><i id="balken-fuellung"></i></div>
      <p id="fortschritt-text">0 von 5 Aufgabenblöcken bearbeitet</p>
      <button type="button" id="fortschritt-reset">zurücksetzen</button>
    </div>
  </nav>

  <main class="inhalt">

    <div class="duo">
      <details class="anleitung">
        <summary><h2 id="so-arbeitest-du">So arbeitest du</h2></summary>
        <ol>
          <li><b>① Clip</b> anschauen. Er hält einmal an und fragt nach deiner Vorhersage.</li>
          <li><b>② Tüfteln:</b> Löse die Aufgaben in der orangen Leiste über dem Bild. Sie zeigt ✓, sobald es stimmt. Überspringen geht immer.</li>
          <li><b>③ Kontrollfragen:</b> Der Clip hält an. Erst antworten. Danach <b>Festhalten</b>: Regel und häufigen Fehler ins Heft.</li>
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen. Mit <b>💡 Tipp</b> bekommst du Hilfe in drei Stufen. Terme tippst du so ein: <code>3x^2-2x+1</code> oder <code>(x-3)(x+4)</code>.</li>
          <li><b>⑤ Aufgaben</b> auf Papier mit Rechenweg, dann Lösung aufklappen und abhaken.</li>
          <li>Zum Schluss der <b>Gesamttest</b> auf Papier. Alles ohne Taschenrechner.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">Das kannst du danach, alles <span class="ohm">ohne Taschenrechner</span>:</p>
        <ul>
          <li><b>K1</b> Terme vereinfachen: gleichartige Glieder zusammenfassen, Klammern auflösen, auch mit Minus davor und verschachtelt, und durch Einsetzen prüfen (Kapitel 1)</li>
          <li><b>K2</b> zwei Klammern ausmultiplizieren und das Ergebnis am Flächenmodell erklären (Kapitel 2)</li>
          <li><b>K3</b> die drei binomischen Formeln anwenden, am Quadrat begründen und zum Kopfrechnen nutzen (Kapitel 3)</li>
          <li><b>K4</b> Summen vollständig faktorisieren: ausklammern, binomische Formel rückwärts, Zweiklammersatz, und Fehler in fremden Lösungen finden (Kapitel 4)</li>
        </ul>
        <p class="rlp-quelle">Nicht in diesem Leitprogramm: Terme mit mehreren Variablen faktorisieren, Bruchterme. Zum Vertiefen bei Mathe begreifbar: ''' + V_FAK + ' · ' + V_BRT + '''.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Terme und Faktorisieren · Sek1-Mathe begreifbar</span>
      <span>Raphael Arnold Kohler</span>
    </div>

  </main>
</div>
</div>
'''

kopf = f'''<!DOCTYPE html>
<html lang="de-CH">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Leitprogramm {NAME}</title>
{seo}
<link rel="stylesheet" href="../schriften.css">
<!-- Die Seite erbt Farben, Karten und Kopf von der Site. Reihenfolge zählt: der eigene <style> unten
     gewinnt bei gleichem Gewicht, das Leitprogramm behält also sein Layout. -->
<link rel="stylesheet" href="../style.css">
<style>
'''
mathjax = r'''<script>
  window.MathJax = {
    tex: { inlineMath: [['\\(','\\)']], displayMath: [['\\[','\\]']] },
    svg: { fontCache: 'global' },
    options: { skipHtmlTags: ['script','noscript','style','textarea','pre'] }
  };
</script>
<script src="../vendor/mathjax/tex-svg.js"></script>

<script>
'''
fuss = f'''
<footer class="site-footer">
  <p><strong>Sek1-Mathe begreifbar</strong> — Lernmaterial Mathematik für die Sekundarstufe I</p>
  <p>Leitprogramm · {NAME}</p>
  <p>© 2026 Raphael Arnold Kohler · <a href="https://creativecommons.org/licenses/by-nc/4.0/deed.de" target="_blank" rel="noopener">CC BY-NC 4.0</a></p>
  <p><a href="../feedback.html">Kontakt &amp; Feedback</a> · <a href="../rechtliches.html">Rechtliches &amp; Datenschutz</a></p>
  <p>Keine Cookies · Kein Tracking · Version 1.0 · {STAND}</p>
</footer>

<script src="../mathlib.js"></script>
<script src="../nav.js"></script>
<script src="../suche.js"></script>
<script>buildNav({{ bereich: 'lp', id: 'lp-terme' }});</script>
</body>
</html>
'''
# Zeiten: Vorwissen 10 · K1 40 · K2 40 · K3 40 · K4 45 · Gesamttest 30 = 205 min
body = oben + k0 + k1 + k2 + k3 + k4 + gt + vt + unten
seite = (kopf + open(SP + 'kopf.css').read() + open(SP + 'seite.css').read() + '</style>\n</head>\n<body>\n' + body + '\n'
         + mathjax + open(SP + 'basis.js').read() + '\n</script>\n' + open(SP + 'seite.js').read() + '\n' + fuss)
os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
open(ZIEL, 'w').write(seite)
print('geschrieben', ZIEL, len(seite.splitlines()), 'Zeilen')
