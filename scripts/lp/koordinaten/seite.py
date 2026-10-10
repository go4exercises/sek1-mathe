"""Baut leitprogramme/koordinaten.html aus einer Kapitelbeschreibung (10.10.2026).

  python3 scripts/lp/koordinaten/seite.py

Leitprogramm Abbildungen und Geraden im Koordinatensystem (Bereich Geometrie), Gerüst aus scripts/lp/pythagoras/.
Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026); vertieft wird auf den Themenseiten von
Mathe begreifbar (TALS). Alles kommt aus diesem Ordner: kopf.css, seite.css, basis.js (Thema, Fortschritt,
Schiene), seite.js (Simulationen im Koordinatensystem, Übungen). Nur der SEO-Block wird aus der bestehenden Seite
übernommen — ihn schreibt scripts/build-seo.py. Wiederholbar. Danach Pre-Flight und build-seo.py.
"""
import json
import os

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/koordinaten.html'
NAME = 'Abbildungen und Geraden im Koordinatensystem'
STAND = 'Stand 10. Oktober 2026'
CLIP = 'koo-lp-'

SEO_AUF = '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->'
SEO_ZU = '<!-- SEO:ENDE -->'
seo = SEO_AUF + '\n' + SEO_ZU
if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
    if SEO_AUF in alt:
        seo = alt[alt.index(SEO_AUF):alt.index(SEO_ZU) + len(SEO_ZU)]

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




# Vertiefung: Mathe begreifbar (Berufsmaturität), in neuem Tab
TALS = 'https://mathe.begreifbar.ch/'
def tals(seite, text, anker=''):
    return f'<a href="{TALS}{seite}{anker}" target="_blank" rel="noopener">{text} ↗</a>'
V_ABB = tals('grundlagen/g5-1-grundlagen.html', 'Grundlagen der Geometrie')
V_STR = tals('grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html', 'Zentrische Streckung und Ähnlichkeit')
V_LIN = tals('grundlagen/g3-2-lineare-funktionen.html', 'Lineare Funktionen')


def reg(sid, name, akz, mn, mx, wert):
    return regler(sid, name, akz, mn, mx, wert)


# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1" aria-label="Punktspiegelung im Koordinatensystem">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Punkt P, Zentrum Z und Bildpunkt P' mit gestrichelter Verbindung"></svg>
        <div class="sl-row">
          {reg('s1-px', 'P: x', 'blau', -6, 6, 4)}
          {reg('s1-py', 'P: y', 'blau', -6, 6, 2)}
        </div>
        <div class="sl-row">
          {reg('s1-zx', 'Z: x', 'gruen', -6, 6, 0)}
          {reg('s1-zy', 'Z: y', 'gruen', -6, 6, 0)}
        </div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Punktspiegelung</div>
          <p>Bei der Spiegelung an einem Punkt \(Z\) liegt \(Z\) genau in der <b>Mitte</b> zwischen \(P\) und seinem Bild \(P'\). Du gehst von \(P\) bis \(Z\) und dann nochmals gleich weit.</p>
          <p>\[ P' = 2Z - P \quad\text{für jede Koordinate einzeln} \]</p>
          <ul class="kurz">
            <li>\(Z(1 \mid 2)\), \(P(4 \mid 3)\): \(P' = (2 - 4 \mid 4 - 3) = (-2 \mid 1)\).</li>
            <li>Zentrum gesucht: \(Z\) ist der Mittelpunkt, \(Z = \left(\dfrac{x_P + x_{P'}}{2} \mid \dfrac{y_P + y_{P'}}{2}\right)\).</li>
            <li>Figuren: jede Ecke einzeln spiegeln. Am Ursprung \(Z(0 \mid 0)\) wechseln beide Vorzeichen: \(A(2 \mid 1) \to A'(-2 \mid -1)\).</li>
          </ul>
          <p>Die Punktspiegelung ist eine Drehung um \(180^\circ\). Längen, Winkel und Flächen bleiben gleich.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Addiert statt gespiegelt:</b> \(P + Z\) oder \(Z - P\) ist nicht die Rechnung für das Bild, auch wenn es manchmal zufällig passt (am Ursprung ist \(Z - P = -P\)). Rechne \(2Z - P\). Probe: Liegt \(Z\) in der Mitte zwischen \(P\) und \(P'\)?</p>
          <p><b>Nur eine Koordinate:</b> Beide Koordinaten werden gespiegelt, jede für sich.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 14, [
    ('1a', 3, r'Spiegle \(A(5 \mid 2)\) und \(B(3 \mid -1)\) am Zentrum \(Z(1 \mid 1)\). Zeichne die Strecke \(AB\) und ihr Bild.',
     r"<p>\(A'(-3 \mid 0)\), \(B'(-1 \mid 3)\). Die Bildstrecke ist gleich lang und parallel zur Originalstrecke.</p>",
     '\n            <div class="mini-reihe"><svg class="leer-gitter" aria-label="leeres Koordinatensystem zum Zeichnen"></svg></div>'),
    ('1b', 2, r'Spiegle \(P(1 \mid 5)\) am Zentrum \(Z(-2 \mid 3)\).',
     r"<p>\(P' = (2 \cdot (-2) - 1 \mid 2 \cdot 3 - 5) = (-5 \mid 1)\).</p>", ''),
    ('1c', 3, r'Spiegle das Dreieck \(A(1 \mid 1)\), \(B(4 \mid 1)\), \(C(1 \mid 3)\) an \(Z(0 \mid 2)\). Wie gross sind die Flächen von Original und Bild?',
     r"<p>\(A'(-1 \mid 3)\), \(B'(-4 \mid 3)\), \(C'(-1 \mid 1)\). Beide Flächen: \(\dfrac{3 \cdot 2}{2} = 3\).</p>", ''),
    ('1d', 2, r'Tim spiegelt \(P(4 \mid 1)\) an \(Z(2 \mid 3)\) und rechnet \(P + Z = (6 \mid 4)\). Was ist falsch?',
     r"<p>\(Z\) muss in der Mitte liegen. Richtig: \(P' = (4 - 4 \mid 6 - 1) = (0 \mid 5)\). Probe: Mitte von \((4 \mid 1)\) und \((0 \mid 5)\) ist \((2 \mid 3)\).</p>", ''),
    ('1e', 2, r"\(P(7 \mid 2)\) wird an einem Punkt auf \(P'(-1 \mid 6)\) gespiegelt. Wo liegt das Zentrum?",
     r'<p>Mittelpunkt: \(\left(\tfrac{7 - 1}{2} \mid \tfrac{2 + 6}{2}\right) = (3 \mid 4)\).</p>', ''),
    ('1f', 2, r'Warum ist ein punktgespiegeltes Dreieck gleich gross wie das Original?',
     r'<p>Die Punktspiegelung ist eine Drehung um \(180^\circ\). Sie verändert weder Längen noch Winkel, darum auch nicht die Fläche.</p>', ''),
])
k1 = kapitel(1, 'punktspiegelung', 'Punktspiegelung', 40,
             r"Du spiegelst Punkte und Figuren an einem Zentrum, rechnerisch mit \(P' = 2Z - P\), und findest das Zentrum als Mittelpunkt.",
             (CLIP + 'punktspiegelung', 'Punktspiegelung'), sim1,
             (CLIP + 'kontrolle-punktspiegelung', 'Kontrollfragen zur Punktspiegelung'), fest1,
             [uebung('punktbild', 'Bildpunkt berechnen'), uebung('zentrum', 'Zentrum finden')],
             auf1, V_ABB, komp='K1')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2" aria-label="Achsenspiegelung im Koordinatensystem">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Punkt P, Spiegelachse grün und Bildpunkt P' mit senkrechter Verbindung"></svg>
        <div class="sl-row">
          <label class="sim-schalter" for="s2-ach">Achse
            <select id="s2-ach" class="sim-wahl"><option value="x" selected>x-Achse</option><option value="y">y-Achse</option><option value="xa">senkrecht x = a</option><option value="yb">waagrecht y = b</option><option value="d">y = x</option></select></label>
          {reg('s2-a', 'a bzw. b', 'gruen', -5, 5, 0)}
        </div>
        <div class="sl-row">
          {reg('s2-px', 'P: x', 'blau', -6, 6, 2)}
          {reg('s2-py', 'P: y', 'blau', -6, 6, 3)}
        </div>
      </figure>'''
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Achsenspiegelung</div>
          <p>\(P\) und \(P'\) liegen gleich weit von der Achse entfernt, ihre Verbindung steht <b>senkrecht</b> auf der Achse.</p>
          <table class="wt">
            <tr><th>Achse</th><th>Bild von \((x \mid y)\)</th><th>\(P(5 \mid -1)\)</th></tr>
            <tr><td>x-Achse</td><td>\((x \mid -y)\)</td><td>\((5 \mid 1)\)</td></tr>
            <tr><td>y-Achse</td><td>\((-x \mid y)\)</td><td>\((-5 \mid -1)\)</td></tr>
            <tr><td>\(x = a\)</td><td>\((2a - x \mid y)\)</td><td>\(x = 2\): \((-1 \mid -1)\)</td></tr>
            <tr><td>\(y = b\)</td><td>\((x \mid 2b - y)\)</td><td>\(y = 2\): \((5 \mid 5)\)</td></tr>
            <tr><td>\(y = x\)</td><td>\((y \mid x)\)</td><td>\((-1 \mid 5)\)</td></tr>
          </table>
          <p><b>Schräge Achse:</b> Senkrechte zur Achse durch \(P\) zeichnen (Geodreieck), Abstand bis zur Achse messen und auf der anderen Seite gleich weit abtragen. An \(y = x\) heisst das: Koordinaten tauschen.</p>
          <p><b>Achse gesucht:</b> Sie geht durch die Mitte von \(P\) und \(P'\) und steht senkrecht auf der Verbindung. \(P(-3 \mid 1)\), \(P'(5 \mid 1)\): Mitte \(\tfrac{-3 + 5}{2} = 1\), Achse \(x = 1\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Falsche Koordinate:</b> An der x-Achse ändert sich y, nicht x. Merke: An einer waagrechten Achse (x-Achse, \(y = b\)) bleibt x, an einer senkrechten (y-Achse, \(x = a\)) bleibt y.</p>
          <p><b>Am Ursprung statt an der Achse:</b> Beide Vorzeichen zu ändern ist eine Punktspiegelung, keine Achsenspiegelung.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 14, [
    ('2a', 3, r'Spiegle \(P(4 \mid -3)\) an der x-Achse, an der y-Achse und an der Geraden \(y = x\).',
     r'<p>\((4 \mid 3)\), \((-4 \mid -3)\), \((-3 \mid 4)\).</p>', ''),
    ('2b', 2, r'Spiegle \(P(-2 \mid 5)\) an der Geraden \(x = 3\).',
     r'<p>\(P\) ist \(5\) links der Achse, das Bild \(5\) rechts: \((8 \mid 5)\). Rechnerisch \(2 \cdot 3 - (-2) = 8\).</p>', ''),
    ('2c', 2, r"Zeichne die Gerade \(y = -x + 3\) ins Gitter und konstruiere mit dem Geodreieck das Bild von \(P(4 \mid 3)\). Lies \(P'\) ab.",
     r"<p>Senkrechte durch \(P\) trifft die Achse in \((2 \mid 1)\), gleich weit dahinter: \(P'(0 \mid -1)\). Probe: Die Mitte von \(P\) und \(P'\) ist \((2 \mid 1)\) und liegt auf der Achse.</p>",
     '\n            <div class="mini-reihe"><svg class="leer-gitter" aria-label="leeres Koordinatensystem zum Zeichnen"></svg></div>'),
    ('2d', 3, r'Spiegle das Dreieck \(A(1 \mid 2)\), \(B(4 \mid 2)\), \(C(4 \mid 5)\) an der Geraden \(y = x\) und zeichne beide Dreiecke.',
     r"<p>\(A'(2 \mid 1)\), \(B'(2 \mid 4)\), \(C'(5 \mid 4)\): Koordinaten tauschen. Jede Verbindung \(PP'\) steht senkrecht auf \(y = x\).</p>",
     '\n            <div class="mini-reihe"><svg class="leer-gitter" aria-label="leeres Koordinatensystem zum Zeichnen"></svg></div>'),
    ('2e', 2, r'Lea spiegelt \(P(3 \mid 5)\) an der x-Achse und erhält \((-3 \mid 5)\). Was ist falsch?',
     r'<p>Sie hat an der y-Achse gespiegelt. An der x-Achse bleibt x gleich: \((3 \mid -5)\).</p>', ''),
    ('2f', 2, r"Warum steht die Verbindung von \(P\) und \(P'\) immer senkrecht auf der Spiegelachse?",
     r'<p>Spiegeln heisst: auf kürzestem Weg zur Achse und gleich weit dahinter. Der kürzeste Weg zu einer Geraden ist der senkrechte.</p>', ''),
])
k2 = kapitel(2, 'achsenspiegelung', 'Achsenspiegelung', 40,
             r'Du spiegelst an den Koordinatenachsen, an Parallelen dazu und an \(y = x\), konstruierst an einer schrägen Achse und findest die Achse aus Punkt und Bild.',
             (CLIP + 'achsenspiegelung', 'Achsenspiegelung'), sim2,
             (CLIP + 'kontrolle-achsenspiegelung', 'Kontrollfragen zur Achsenspiegelung'), fest2,
             [uebung('achsbild', 'Bildpunkt berechnen'), uebung('achsefinden', 'Spiegelachse finden')],
             auf2, V_ABB, komp='K2')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3" aria-label="Zentrische Streckung eines Dreiecks">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Dreieck ABC blau, Bilddreieck orange, Strahlen vom Zentrum Z"></svg>
        <div class="sl-row">
          {reg('s3-zx', 'Z: x', 'gruen', -3, 5, -2)}
          {reg('s3-zy', 'Z: y', 'gruen', -3, 3, -1)}
        </div>
        <div class="sl-row">
          {reg('s3-k', 'Faktor k', 'orange', 0.5, 3, 1).replace('step="1"', 'step="0.5"')}
        </div>
      </figure>'''
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Zentrische Streckung und Flächen</div>
          <p>Vom Zentrum \(Z\) aus wird jeder Weg zu einem Punkt mit \(k\) multipliziert:</p>
          <p>\[ P' = Z + k \cdot (P - Z) \quad\text{für jede Koordinate einzeln, } k > 0 \]</p>
          <p>\(k > 1\) vergrössert, \(0 < k < 1\) verkleinert: Bei \(k = 0.5\) ist der Weg ab \(Z\) nur noch halb so lang. Den Faktor findest du als \(k = \dfrac{\text{Weg } ZP'}{\text{Weg } ZP}\).</p>
          <ul class="kurz">
            <li>\(Z(0 \mid 0)\), \(k = 2\): \(A(1 \mid 1) \to (2 \mid 2)\), alle Koordinaten mal \(2\).</li>
            <li>\(Z(1 \mid 1)\), \(k = 3\), \(P(2 \mid 3)\): Weg \((1 \mid 2)\), mal \(3\) gibt \((3 \mid 6)\), ab \(Z\): \(P'(4 \mid 7)\).</li>
            <li>Längen \(\cdot k\), Flächen \(\cdot k^2\): Dreieck mit Fläche \(1\) wird bei \(k = 2\) zur Fläche \(4\).</li>
            <li><b>Fläche aus Koordinaten:</b> umschliessendes Rechteck minus die rechtwinkligen Randdreiecke (wenn jede Ecke auf dem Rand des Rechtecks liegt). \(A(1 \mid 1)\), \(B(5 \mid 2)\), \(C(2 \mid 4)\): \(4 \cdot 3 - 2 - 1.5 - 3 = 5.5\).</li>
          </ul>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Zentrum vergessen:</b> «Koordinaten mal \(k\)» stimmt nur für \(Z(0 \mid 0)\). Sonst den Weg ab \(Z\) strecken.</p>
          <p><b>Flächenfaktor = Längenfaktor:</b> Bei \(k = 3\) wird die Fläche \(9\)-mal so gross.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 14, [
    ('3a', 3, r'Strecke das Dreieck \(A(1 \mid 0)\), \(B(2 \mid 0)\), \(C(1 \mid 1)\) von \(Z(0 \mid 0)\) aus mit \(k = 3\). Zeichne beide Dreiecke und vergleiche die Flächen.',
     r"<p>\(A'(3 \mid 0)\), \(B'(6 \mid 0)\), \(C'(3 \mid 3)\). Flächen \(0.5\) und \(4.5 = 0.5 \cdot 3^2\).</p>",
     '\n            <div class="mini-reihe"><svg class="leer-gitter" aria-label="leeres Koordinatensystem zum Zeichnen"></svg></div>'),
    ('3b', 2, r'Strecke \(P(5 \mid 3)\) von \(Z(2 \mid 1)\) aus mit \(k = 2\).',
     r"<p>Weg \((3 \mid 2)\), mal \(2\): \((6 \mid 4)\), ab \(Z\): \(P'(8 \mid 5)\).</p>", ''),
    ('3c', 3, r'Berechne die Fläche des Dreiecks \(A(0 \mid 0)\), \(B(6 \mid 1)\), \(C(2 \mid 5)\).',
     r'<p>Rechteck \(6 \cdot 5 = 30\), Randdreiecke \(\tfrac{6 \cdot 1}{2} = 3\), \(\tfrac{4 \cdot 4}{2} = 8\), \(\tfrac{2 \cdot 5}{2} = 5\). Fläche \(30 - 16 = 14\).</p>', ''),
    ('3d', 2, r'Ben streckt \(P(4 \mid 3)\) von \(Z(1 \mid 1)\) aus mit \(k = 2\) und erhält \((8 \mid 6)\). Was ist falsch?',
     r'<p>Er hat das Zentrum vergessen. Weg \((3 \mid 2)\), mal \(2\) gibt \((6 \mid 4)\), ab \(Z\): \((7 \mid 5)\).</p>', ''),
    ('3e', 2, r'Ein Viereck mit Fläche \(5\) wird mit \(k = 4\) gestreckt. Wie gross ist die Bildfläche?',
     r'<p>\(5 \cdot 4^2 = 80\).</p>', ''),
    ('3f', 2, r'Warum wächst bei einer Streckung mit \(k\) die Fläche mit \(k^2\)?',
     r'<p>Jede Länge wird mit \(k\) multipliziert, also Breite und Höhe. Beim Rechteck: Fläche \(= k \cdot \text{Breite} \cdot k \cdot \text{Höhe}\). Beim Dreieck kommt das \(\tfrac{1}{2}\) dazu, der Faktor \(k^2\) bleibt.</p>', ''),
])
k3 = kapitel(3, 'streckung', 'Zentrische Streckung und Flächen', 40,
             r'Du streckst Punkte und Figuren von einem Zentrum aus, berechnest Bildkoordinaten, Flächen aus Koordinaten und den Flächenfaktor \(k^2\).',
             (CLIP + 'streckung', 'Zentrische Streckung und Flächen'), sim3,
             (CLIP + 'kontrolle-streckung', 'Kontrollfragen zur Streckung'), fest3,
             [uebung('streckbild', 'Bildpunkt einer Streckung'), uebung('koordflaeche', 'Fläche aus Koordinaten')],
             auf3, V_STR, komp='K3')

# ------------------------------------------------------------------ Kapitel 4
sim4 = f'''      <figure class="sim sim-gross" id="sim4" aria-label="Gerade durch zwei Punkte">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Punkte A und B und die Gerade durch beide"></svg>
        <div class="sl-row">
          {reg('s4-ax', 'A: x', 'blau', -6, 6, -2)}
          {reg('s4-ay', 'A: y', 'blau', -6, 6, -3)}
        </div>
        <div class="sl-row">
          {reg('s4-bx', 'B: x', 'blau', -6, 6, 2)}
          {reg('s4-by', 'B: y', 'blau', -6, 6, -1)}
        </div>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Gerade durch zwei Punkte, Punktprobe</div>
          <ol class="weg">
            <li>\(A(1 \mid 3)\), \(B(4 \mid 9)\): \(m = \dfrac{9 - 3}{4 - 1} = \dfrac{6}{3} = 2\) <span class="warum">\(\Delta y : \Delta x\)</span></li>
            <li>\(A\) einsetzen: \(3 = 2 \cdot 1 + b\), \(b = 1\) <span class="warum">nach b auflösen</span></li>
            <li>\(y = 2x + 1\), Probe mit \(B\): \(2 \cdot 4 + 1 = 9\) <span class="warum">stimmt</span></li>
          </ol>
          <p>Das geht, solange \(x_A \neq x_B\); sonst ist die Gerade senkrecht und hat keine Gleichung \(y = m \cdot x + b\).</p>
          <p><b>Punktprobe:</b> Liegt \(C(100 \mid 201)\) auf der Geraden? Einsetzen: \(2 \cdot 100 + 1 = 201\), ja. \(D(50 \mid 102)\): \(2 \cdot 50 + 1 = 101 \neq 102\), nein. So prüfst du auch Punkte weit ausserhalb jeder Zeichnung.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Bruch auf dem Kopf:</b> \(\dfrac{\Delta x}{\Delta y} = \dfrac{3}{6}\) ist nicht die Steigung. \(m = \dfrac{\Delta y}{\Delta x}\).</p>
          <p><b>Ablesen statt einsetzen:</b> Ein Punkt «sieht» auf der Geraden aus, liegt aber knapp daneben. Nur das Einsetzen entscheidet.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 14, [
    ('4a', 3, r'Bestimme die Gleichung der Geraden durch \(A(1 \mid -2)\) und \(B(3 \mid 4)\) und zeichne die Gerade.',
     r'<p>\(m = \dfrac{4 - (-2)}{3 - 1} = \dfrac{6}{2} = 3\), \(-2 = 3 \cdot 1 + b\), \(b = -5\): \(y = 3x - 5\).</p>',
     '\n            <div class="mini-reihe"><svg class="leer-gitter" aria-label="leeres Koordinatensystem zum Zeichnen"></svg></div>'),
    ('4b', 2, r'Liegen \(P(30 \mid -55)\) und \(Q(-12 \mid 30)\) auf der Geraden \(y = -2x + 5\)?',
     r'<p>\(-2 \cdot 30 + 5 = -55\): \(P\) ja. \(-2 \cdot (-12) + 5 = 29 \neq 30\): \(Q\) nein.</p>', ''),
    ('4c', 3, r'Bestimme die Gleichung der Geraden durch \(A(-2 \mid 5)\) und \(B(4 \mid -1)\).',
     r'<p>\(m = \dfrac{-1 - 5}{4 - (-2)} = \dfrac{-6}{6} = -1\), \(5 = -1 \cdot (-2) + b\), \(b = 3\): \(y = -x + 3\).</p>', ''),
    ('4d', 2, r'Mia berechnet die Steigung durch \(A(2 \mid 1)\) und \(B(5 \mid 10)\) als \(\dfrac{5 - 2}{10 - 1} = \dfrac{1}{3}\). Was ist falsch?',
     r'<p>Der Bruch steht auf dem Kopf. \(m = \dfrac{10 - 1}{5 - 2} = \dfrac{9}{3} = 3\).</p>', ''),
    ('4e', 2, r"\(P(1 \mid 2)\) wird an \(Z(3 \mid 3)\) gespiegelt. Bestimme die Gerade durch \(P\) und \(P'\) und prüfe, ob \(Z\) darauf liegt.",
     r"<p>\(P'(5 \mid 4)\), \(m = \dfrac{2}{4} = \dfrac{1}{2}\), \(b = \dfrac{3}{2}\): \(y = \tfrac{1}{2}x + \tfrac{3}{2}\). Probe \(Z\): \(\tfrac{3}{2} + \tfrac{3}{2} = 3\), ja. Das Zentrum liegt immer auf der Geraden \(PP'\).</p>", ''),
    ('4f', 2, r'Warum genügt ein Einsetzen, um zu entscheiden, ob ein Punkt auf einer Geraden liegt?',
     r'<p>Die Gleichung beschreibt genau alle Punkte der Geraden. Erfüllen die Koordinaten sie, liegt der Punkt darauf, sonst nicht.</p>', ''),
])
k4 = kapitel(4, 'gerade', 'Gerade durch zwei Punkte', 40,
             r'Du bestimmst die Gleichung einer Geraden durch zwei Punkte und prüfst durch Einsetzen, ob ein Punkt auf ihr liegt, auch weit ausserhalb der Zeichnung.',
             (CLIP + 'gerade', 'Gerade durch zwei Punkte'), sim4,
             (CLIP + 'kontrolle-gerade', 'Kontrollfragen zu Geraden'), fest4,
             [uebung('gerade2', 'Gleichung aus zwei Punkten'), uebung('punktprobe', 'Punktprobe')],
             auf4, V_LIN, komp='K4')

# ------------------------------------------------------------------ Vorwissen
k0 = f'''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-th">Vorwissen</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Koordinaten, Mittelpunkt, negative Zahlen, Rechteck, Einsetzen. Zuerst kurz wiederholen, dann der Vortest.</p>
''' + r'''      <details class="anleitung">
        <summary><h3>Kurz wiederholt</h3></summary>
        <ul class="kurz">
          <li><b>Koordinaten:</b> \(P(3 \mid -2)\) heisst \(3\) nach rechts, \(2\) nach unten.</li>
          <li><b>Mittelpunkt:</b> von \((1 \mid 3)\) und \((5 \mid 7)\) ist \((3 \mid 5)\): je die Koordinaten addieren und halbieren.</li>
          <li><b>Rechteck im Gitter:</b> Breite = Unterschied der x-Werte, Höhe = Unterschied der y-Werte. Ecken \((0 \mid 1)\) und \((4 \mid 3)\): \(4 \cdot 2 = 8\).</li>
          <li><b>Negative Zahlen:</b> \(2 \cdot (-3) - 4 = -10\), \(-(-5) = 5\).</li>
          <li><b>Gerade:</b> \(y = m \cdot x + b\), Steigung \(m\), \(y\)-Achsenabschnitt \(b\) (Leitprogramm <a href="lineare-funktionen.html">Lineare Funktionen</a>). Steigung aus zwei Punkten: \(m = \dfrac{\Delta y}{\Delta x}\), von \((0 \mid 1)\) nach \((2 \mid 5)\) also \(\tfrac{4}{2} = 2\).</li>
        </ul>
      </details>
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Wo liegt der Mittelpunkt der Strecke von \(A(2 \mid 6)\) nach \(B(8 \mid 2)\)?', r'<p>\((5 \mid 4)\).</p>', ''),
    ('0b', 2, r'Berechne \(2 \cdot 3 - 7\) und \(2 \cdot (-1) - 4\).', r'<p>\(-1\) und \(-6\).</p>', ''),
    ('0c', 2, r'Ein Rechteck hat die Ecken \((1 \mid 1)\), \((6 \mid 1)\), \((6 \mid 4)\), \((1 \mid 4)\). Wie gross ist seine Fläche?', r'<p>\(5 \cdot 3 = 15\).</p>', ''),
    ('0d', 2, r'Berechne \(y\) für \(y = 2x - 3\) bei \(x = 4\). Liegt \((1 \mid -1)\) auf dieser Geraden?', r'<p>\(y = 5\). Ja: \(2 \cdot 1 - 3 = -1\).</p>', ''),
    ('0e', 2, r'Welche Steigung hat die Gerade durch \((1 \mid 2)\) und \((3 \mid 8)\)?', r'<p>\(\dfrac{6}{2} = 3\).</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: «Kurz wiederholt» nochmals lesen und die Lösungen nachrechnen.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest (nur PDF)
PDF = '../downloads/leitprogramme/koordinaten/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-th">Kapitel 1–4</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg und Zeichnung im Koordinatensystem, ohne Taschenrechner.<br>
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
            <tr><td>17 – 21 P</td><td>Den schwächsten Teil nochmals, gemessen am Anteil (Teil A 6, B 6, C 7, D 6 P): Tüfteln und Übungen des Kapitels dieses Teils.</td></tr>
            <tr><td>11 – 16 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 10 P</td><td>Zurück zu den Kapiteln jedes Teils, in dem du weniger als die Hälfte erreicht hast; sind es alle vier, zum Vortest und zu Kapitel 1.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1, G2 → 1; G3, G4 → 2; G5, G6 → 3; G7, G8 → 4</p>
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
            <div class="frage"><span class="nr">V1</span><span class="txt">Spiegle \(P(2 \mid 1)\) zuerst an \(Z_1(0 \mid 0)\) und das Bild an \(Z_2(3 \mid 0)\). Wo landet \(P\)? Was fällt dir auf, wenn du es mit anderen Punkten wiederholst?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\((-2 \mid -1)\), dann \((8 \mid 1)\). Jeder Punkt wird um \((6 \mid 0)\) verschoben, das Doppelte des Wegs von \(Z_1\) nach \(Z_2\). Zwei Punktspiegelungen ergeben eine Verschiebung.</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V2</span><span class="txt">Wohin kommt \(P(5 \mid 3)\) bei der Spiegelung an der Geraden \(y = -x\)? Finde eine Regel.</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\((-3 \mid -5)\): Koordinaten tauschen und beide Vorzeichen ändern, \((x \mid y) \to (-y \mid -x)\).</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V3</span><span class="txt">Was passiert bei einer «Streckung» mit \(k = -1\)? Probiere es mit \(P(4 \mid 2)\) und \(Z(1 \mid 1)\).</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\(P' = (1 - 3 \mid 1 - 1) = (-2 \mid 0)\), dasselbe wie die Punktspiegelung an \(Z\). Mit \(k = -1\) ist die Streckung eine Punktspiegelung.</p></div></details>
          </li>
        </ol>
      </div>
      <p class="ausf weiter">Weiter: Zentrische Streckung bei Mathe begreifbar: ''' + V_STR + r'''.</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Abbildungen und Geraden im Koordinatensystem, Version 1.0 (10.10.2026). Gebaut aus scripts/lp/koordinaten/seite.py —
     Änderungen dort, nicht in dieser Datei. Grundlagen: HOWTO-leitprogramme.md (Kapitelmuster) und
     ~/TODO-BM-Vorkurs-LP03-15.md, Abschnitt 7 (LP 09, Koordinatengeometrie: Abbildungen und Geraden), für die Sek I umgesetzt.

     Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026): Das Leitprogramm ist selbst die fachliche Quelle;
     Vertiefung bei Mathe begreifbar. Baut auf den Leitprogrammen Lineare Funktionen und Flächen, Pythagoras und Ähnlichkeit auf.
     Notation: Punkte (x | y), Bild mit Strich P', Zentrum Z, Faktor k, Gerade y = m · x + b, Dezimalpunkt.

     Kompetenzen — eigene Formulierung, ohne Lehrplan-Nummern (CLAUDE.md: keine erfundenen Lehrplan-Stellen):
       K1  Punktspiegelung rechnerisch (P' = 2Z − P) und zeichnerisch, Zentrum als Mittelpunkt finden
       K2  Achsenspiegelung an Koordinatenachsen, Parallelen und y = x; schräge Achse konstruieren; Achse finden
       K3  Zentrische Streckung im Koordinatensystem, Fläche aus Koordinaten, Flächenfaktor k²
       K4  Geradengleichung aus zwei Punkten und Punktprobe durch Einsetzen, auch ausserhalb der Zeichnung

     Kompetenzmatrix (Kompetenz | Kapitel | Simulation | Übungen | Kapitelaufgaben | Gesamttest):
       K1 | 1 | Sim 1 Punktspiegelung  | punktbild, zentrum        | 1a–1f | G1, G2
       K2 | 2 | Sim 2 Achsenspiegelung | achsbild, achsefinden     | 2a–2f | G3, G4
       K3 | 3 | Sim 3 Streckung        | streckbild, koordflaeche  | 3a–3f | G5, G6
       K4 | 4 | Sim 4 zwei Punkte      | gerade2, punktprobe       | 4a–4f | G7, G8

     Planung (Kapitel | Lernziel | Erkundung | Beispiel | Häufiger Fehler | min):
       0 | Vorwissen        | –               | –                          | –                                  | 10
       1 | Punktspiegelung  | Z und P ziehen  | P(5|3) an Z(2|1)           | P + Z statt 2Z − P                 | 40
       2 | Achsenspiegelung | Achse wählen    | P(3|2) an x, y, x = 1, y = x| falsche Koordinate geändert        | 40
       3 | Streckung        | Z und k         | k = 2 ab Ursprung, Z(1|1)  | Zentrum vergessen; Fläche · k      | 40
       4 | Geraden          | A und B ziehen  | A(1|3), B(4|9), C(100|201) | Δx : Δy; ablesen statt einsetzen   | 40
       Gesamttest (PDF) 30 · Summe 200 min ≈ 4.4 Lektionen. Vertiefung V1–V3 freiwillig, nicht eingerechnet.

     Aus der Vorlage umgesetzt: Koordinaten im Raster, P' = 2Z − P komponentenweise (Kapitel 1, G1, G2), Achsenspiegelung mit
     gleichem senkrechtem Abstand, schräge Achse kontrolliert konstruiert (Kapitel 2, G3, G4), Streckung im Koordinatensystem mit
     Flächenfaktor und Fläche einer Figur aus Koordinaten (Kapitel 3, G5, G6), Gerade aus zwei Punkten und Punkttest eines Punktes
     ausserhalb der Zeichnung (Kapitel 4, G7, G8). Rechenweg und Konstruktion getrennt bewertbar (Raster). Visualisierung nur mit
     Mehrwert: je Kapitel eine Simulation. Bewusst nicht übernommen: Teams-Ablauf, Lehrpersonenteil, Prüfungsnummern.

     Clips: je Kapitel ein Einführungsclip (mit einer Vorhersagefrage) und ein Kontrollclip mit fünf Fragen,
     Reihe «Geometrie», koo-lp-*.json, erzeugt mit scripts/lp/koordinaten/clips.py.

     Farben: Original blau, Bild orange, Zentrum, Achse und Gerade grün, Fehler rot; Bereichsfarbe Petrol.
     Gesamttest und Bewertungspaket nur als PDF (downloads/leitprogramme/koordinaten/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Sek1-Mathe begreifbar · Leitprogramm</p>
      <h1>Abbildungen und Geraden im Koordinatensystem</h1>
      <p class="unter">Punkt- und Achsenspiegelung, zentrische Streckung und Geraden durch zwei Punkte, alles mit Koordinaten. Vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Geometrie</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Punktspiegelung</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Achsenspiegelung</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Streckung</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Geraden</span></a></li>
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
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen. Mit <b>💡 Tipp</b> bekommst du Hilfe in drei Stufen. Zahlen tippst du als <code>2</code>, <code>-1.5</code> oder Bruch <code>2/3</code>; bei Aussagen wählst du aus einer Liste.</li>
          <li><b>⑤ Aufgaben</b> auf Papier mit Rechenweg, dann Lösung aufklappen und abhaken.</li>
          <li>Zum Schluss der <b>Gesamttest</b> auf Papier, mit Lineal und Geodreieck. Alles ohne Taschenrechner.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">Das kannst du danach, alles <span class="ohm">ohne Taschenrechner</span>:</p>
        <ul>
          <li><b>K1</b> Punkte und Figuren an einem Zentrum spiegeln und das Zentrum aus Punkt und Bild bestimmen (Kapitel 1)</li>
          <li><b>K2</b> an den Achsen, an Parallelen dazu und an \\(y = x\\) spiegeln, an einer schrägen Achse konstruieren und die Spiegelachse finden (Kapitel 2)</li>
          <li><b>K3</b> Figuren zentrisch strecken, Flächen aus Koordinaten berechnen und den Flächenfaktor \\(k^2\\) anwenden (Kapitel 3)</li>
          <li><b>K4</b> die Gleichung einer Geraden durch zwei Punkte bestimmen und mit einer Punktprobe prüfen, ob ein Punkt auf ihr liegt (Kapitel 4)</li>
        </ul>
        <p class="rlp-quelle">Baut auf den Leitprogrammen «Lineare Funktionen» und «Flächen, Pythagoras und Ähnlichkeit» auf. Nicht in diesem Leitprogramm: Drehungen um beliebige Winkel, Vektoren, Abbildungsmatrizen. Zum Vertiefen bei Mathe begreifbar: ''' + V_STR + '''.</p>
      </details>

    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Abbildungen und Geraden im Koordinatensystem · Sek1-Mathe begreifbar</span>
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
<script>buildNav({{ bereich: 'lp', id: 'lp-koordinaten' }});</script>
</body>
</html>
'''
# Zeiten: Vorwissen 10 · K1 40 · K2 40 · K3 40 · K4 40 · Gesamttest 30 = 200 min
body = oben + k0 + k1 + k2 + k3 + k4 + gt + vt + unten
seite = (kopf + open(SP + 'kopf.css').read() + open(SP + 'seite.css').read() + '</style>\n</head>\n<body>\n' + body + '\n'
         + mathjax + open(SP + 'basis.js').read() + '\n</script>\n' + open(SP + 'seite.js').read() + '\n' + fuss)
os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
open(ZIEL, 'w').write(seite)
print('geschrieben', ZIEL, len(seite.splitlines()), 'Zeilen')
