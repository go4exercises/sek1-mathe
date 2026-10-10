"""Baut leitprogramme/lineare-funktionen.html aus einer Kapitelbeschreibung (10.10.2026).

  python3 scripts/lp/lineare-funktionen/seite.py

Leitprogramm Lineare Funktionen (Bereich Funktionen), Gerüst aus scripts/lp/gleichungen-formeln/.
Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026); vertieft wird auf den Themenseiten von
Mathe begreifbar (TALS). Alles kommt aus diesem Ordner: kopf.css, seite.css, basis.js (Thema, Fortschritt,
Schiene), seite.js (Koordinatensystem, Simulationen, Übungen mit Zahlen und Klickgitter). Nur der SEO-Block wird aus der bestehenden Seite
übernommen — ihn schreibt scripts/build-seo.py. Wiederholbar. Danach Pre-Flight und build-seo.py.
"""
import json
import os

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/lineare-funktionen.html'
NAME = 'Lineare Funktionen'
STAND = 'Stand 10. Oktober 2026'
CLIP = 'lin-lp-'

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
V_DEF = tals('grundlagen/g3-2-lineare-funktionen.html', 'Lineare Funktionen', '#definition')
V_STEIG = tals('grundlagen/g3-2-lineare-funktionen.html', 'Steigung, Achsenabschnitt, Nullstelle', '#steigung')
V_ACHS = tals('grundlagen/g3-1-grundlagen.html', 'Schnittpunkte mit den Achsen', '#achsenschnitte')
V_LP = tals('leitprogramme/lineare-funktionen.html', 'Leitprogramm Lineare Funktionen (lang)')


def bild(geraden='', punkte='', label='Gerade im Koordinatensystem'):
    return f'\n            <div class="mini-reihe"><svg class="mini-gerade" data-geraden="{geraden}" data-punkte="{punkte}" aria-label="{label}"></svg></div>'


# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1" aria-label="Fass: Anfangswert und Änderung pro Minute">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Wasser im Fass in Abhängigkeit der Zeit"></svg>
        <table class="wt" aria-label="Wertetabelle"></table>
        <div class="sl-row">
          {regler('s1-b', 'am Anfang b', 'orange', 0, 100, 50).replace('step="1"', 'step="5"')}
          {regler('s1-m', 'pro Minute m', 'blau', -20, 20, 5).replace('step="1"', 'step="5"')}
        </div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Anfangswert und Änderung</div>
          <p>Ein Wassertank enthält am Anfang \(200\) l, pro Minute fliessen \(15\) l dazu. Nach \(x\) Minuten sind es</p>
          <p>\[ y = 15 \cdot x + 200 \]</p>
          <p>Allgemein: \(\;y = m \cdot x + b\;\) mit dem <b>Anfangswert</b> \(b\) (der Wert bei \(x = 0\); im Graphen heisst er <b>\(y\)-Achsenabschnitt</b>) und der <b>Änderung pro Einheit</b> \(m\). Nimmt der Wert ab, ist \(m\) negativ. So ein Zusammenhang heisst <b>lineare Funktion</b>, ihr Graph ist eine Gerade.</p>
          <p>In der Wertetabelle ändert sich \(y\) bei jedem Schritt \(x \to x + 1\) um dasselbe \(m\): \(200,\ 215,\ 230,\ 245, \dots\)</p>
          <ol class="weg">
            <li>\(y\) für \(x = 6\): \(15 \cdot 6 + 200 = 290\) <span class="warum">einsetzen</span></li>
            <li>Wann sind es \(350\) l? \(15x + 200 = 350\), \(15x = 150\), \(x = 10\) <span class="warum">Gleichung lösen</span></li>
          </ol>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>\(m\) und \(b\) vertauscht:</b> \(y = 200 \cdot x + 15\) beschreibt einen Tank, der mit \(15\) l startet und pro Minute \(200\) l gewinnt. Probe mit \(x = 0\): Am Anfang müssen \(200\) l drin sein.</p>
          <p><b>Probe nicht mit \(x = 1\):</b> Bei \(x = 1\) geben \(15x + 200\) und \(200x + 15\) beide \(215\). Nimm \(x = 0\) oder \(x = 2\).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 15, [
    ('1a', 3, r'Ein Velo kostet \(8\) Fr. Grundgebühr und \(3\) Fr. pro Stunde. Stelle die Gleichung auf (\(x\): Stunden, \(y\): Kosten in Fr.). Was kosten \(5\) Stunden? Wie lange kannst du für \(32\) Fr. fahren?',
     r'<p>\(y = 3x + 8\). Für \(x = 5\): \(23\) Fr. \(3x + 8 = 32\), \(3x = 24\), \(x = 8\) Stunden.</p>', ''),
    ('1b', 3, r'Ergänze die Wertetabelle von \(y = -2x + 5\) für \(x = -1,\ 0,\ 1,\ 2,\ 3\) und trag die Punkte ins Koordinatensystem ein. Was fällt dir auf?',
     r'<p>\(7,\ 5,\ 3,\ 1,\ -1\): die Punkte \((-1 \mid 7)\), \((0 \mid 5)\), \((1 \mid 3)\), \((2 \mid 1)\), \((3 \mid -1)\). Sie liegen auf einer fallenden Geraden; bei jedem Schritt nach rechts geht es \(2\) hinunter.</p>',
     '\n            <div class=\"mini-reihe\"><svg class=\"leer-gitter\" aria-label=\"leeres Koordinatensystem zum Eintragen\"></svg></div>'),
    ('1c', 2, r'Ist der Zusammenhang linear? Tabelle 1: \(x = 0, 1, 2, 3\) und \(y = 4, 7, 10, 13\). Tabelle 2: \(x = 0, 1, 2, 3\) und \(y = 1, 2, 4, 8\).',
     r'<p>Tabelle 1: ja, immer \(+3\): \(y = 3x + 4\). Tabelle 2: nein, die Zunahme ist \(1, 2, 4\), nicht gleich.</p>', ''),
    ('1d', 2, r'Lea schreibt für «Ein Tank mit \(50\) l verliert pro Minute \(4\) l»: \(y = 50x - 4\). Prüfe mit \(x = 0\) und schreib die richtige Gleichung.',
     r'<p>Mit \(x = 0\) gibt Leas Gleichung \(-4\) l, am Anfang sind aber \(50\) l drin. Richtig: \(y = -4x + 50\).</p>', ''),
    ('1e', 3, r'Ein Ballon startet auf \(300\) m ü. M. und steigt pro Minute \(40\) m. Gleichung? Nach wie vielen Minuten ist er auf \(1100\) m?',
     r'<p>\(y = 40x + 300\). \(40x + 300 = 1100\), \(40x = 800\), \(x = 20\) Minuten.</p>', ''),
    ('1f', 2, r'Warum ist \(b\) der Wert bei \(x = 0\)?',
     r'<p>Setzt man \(x = 0\) ein, wird \(m \cdot 0 = 0\), und es bleibt \(y = b\). \(b\) ist also der Startwert, bevor sich etwas geändert hat.</p>', ''),
])
k1 = kapitel(1, 'anfangswert', 'Anfangswert und Änderung', 40,
             r'Du beschreibst einen linearen Zusammenhang mit \(y = m \cdot x + b\): \(b\) als Anfangswert, \(m\) als Änderung pro Einheit. Du berechnest Werte und findest umgekehrt das passende \(x\).',
             (CLIP + 'anfangswert', 'Anfangswert und Änderung'), sim1,
             (CLIP + 'kontrolle-anfangswert', 'Kontrollfragen zu Anfangswert und Änderung'), fest1,
             [uebung('wert', 'Werte berechnen'), uebung('kontext', 'Gleichung aus dem Text')],
             auf1, V_DEF, komp='K1')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2" aria-label="Steigung mit dem Steigungsdreieck messen">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Gerade mit Steigungsdreieck"></svg>
        <div class="sl-row">
          {regler('s2-dx', 'Δx nach rechts', 'blau', 1, 6, 1)}
          {regler('s2-dy', 'Δy hinauf (+) oder hinunter (−)', 'blau', -6, 6, 1)}
        </div>
      </figure>'''
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Steigung</div>
          <p>Die <b>Steigung</b> \(m\) sagt, um wie viel \(y\) zunimmt, wenn \(x\) um \(1\) zunimmt. Mit einem <b>Steigungsdreieck</b> zwischen zwei Punkten der Geraden:</p>
          <p>\[ m = \frac{\Delta y}{\Delta x} = \frac{\text{hinauf (+) oder hinunter (−)}}{\text{nach rechts}} \]</p>
          <ol class="weg">
            <li>\(P(1 \mid 2)\) und \(Q(4 \mid 8)\) <span class="warum">zwei Punkte der Geraden</span></li>
            <li>\(m = \dfrac{8 - 2}{4 - 1} = \dfrac{6}{3} = 2\) <span class="warum">oben und unten dieselbe Reihenfolge: \(Q\) minus \(P\)</span></li>
          </ol>
          <p>\(m \gt 0\): die Gerade steigt. \(m \lt 0\): sie fällt. \(m = 0\): sie ist waagrecht. Je grösser der Betrag von \(m\), desto steiler.</p>
          <p>Eine Steigung als Bruch: \(m = \tfrac{2}{3}\) heisst \(3\) nach rechts und \(2\) hinauf.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Bruch vertauscht:</b> \(\dfrac{\Delta x}{\Delta y} = \dfrac{3}{6}\) ist nicht die Steigung. Oben steht die Änderung in \(y\).</p>
          <p><b>Reihenfolge gemischt:</b> \(\dfrac{8 - 2}{1 - 4} = -2\) hat das falsche Vorzeichen. Oben und unten zuerst denselben Punkt.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 14, [
    ('2a', 2, r'Berechne die Steigung der Geraden durch \(P(2 \mid 3)\) und \(Q(6 \mid 11)\).',
     r'<p>\(m = \dfrac{11 - 3}{6 - 2} = \dfrac{8}{4} = 2\).</p>', ''),
    ('2b', 2, r'Berechne die Steigung durch \(P(-1 \mid 4)\) und \(Q(3 \mid -4)\). Steigt oder fällt die Gerade?',
     r'<p>\(m = \dfrac{-4 - 4}{3 - (-1)} = \dfrac{-8}{4} = -2\). Sie fällt.</p>', ''),
    ('2c', 3, r'Lies die Steigung der Geraden ab. Zeichne dazu ein Steigungsdreieck zwischen den beiden markierten Punkten.',
     r'<p>Von \((0 \mid 1)\) nach \((3 \mid 3)\): \(3\) nach rechts, \(2\) hinauf, also \(m = \dfrac{2}{3}\).</p>', bild('2/3,1', '0,1;3,3', 'Gerade durch (0 | 1) und (3 | 3)')),
    ('2d', 2, r'Tim rechnet für \(P(2 \mid 1)\) und \(Q(4 \mid 5)\): \(m = \dfrac{5 - 1}{2 - 4} = -2\). Was ist falsch?',
     r'<p>Oben rechnet Tim \(Q\) minus \(P\), unten \(P\) minus \(Q\). Richtig: \(\dfrac{5 - 1}{4 - 2} = 2\). Die Gerade steigt ja von \(P\) nach \(Q\).</p>', ''),
    ('2e', 3, r'Ordne nach Steilheit, die steilste zuerst: \(y = 3x\), \(\;y = -4x + 1\), \(\;y = 0.5x\), \(\;y = -x\).',
     r'<p>Massgebend ist der Betrag von \(m\): \(y = -4x + 1\) (\(4\)), \(y = 3x\) (\(3\)), \(y = -x\) (\(1\)), \(y = 0.5x\) (\(0.5\)). Das Vorzeichen sagt nur, ob sie steigt oder fällt.</p>', ''),
    ('2f', 2, r'Warum hat eine waagrechte Gerade die Steigung \(0\)?',
     r'<p>Geht man nach rechts, ändert sich \(y\) nicht: \(\Delta y = 0\), also \(m = \dfrac{0}{\Delta x} = 0\).</p>', ''),
])
k2 = kapitel(2, 'steigung', 'Die Steigung', 40,
             r'Du bestimmst die Steigung mit einem Steigungsdreieck und aus zwei Punkten, und du deutest ihr Vorzeichen.',
             (CLIP + 'steigung', 'Die Steigung'), sim2,
             (CLIP + 'kontrolle-steigung', 'Kontrollfragen zur Steigung'), fest2,
             [uebung('steigung', 'Steigung aus zwei Punkten'), uebung('ablesen', 'Steigung ablesen')],
             auf2, V_STEIG, komp='K2')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3" aria-label="Gerade einstellen: b schiebt, m kippt">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Gerade im Koordinatensystem mit gesuchten Punkten"></svg>
        <div class="sl-row">
          {regler('s3-b', 'b (Start auf der y-Achse)', 'orange', -6, 6, 0)}
        </div>
        <div class="sl-row">
          {regler('s3-dy', 'Δy', 'blau', -6, 6, 1)}
          {regler('s3-dx', 'Δx', 'blau', 1, 4, 1)}
        </div>
      </figure>'''
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Eine Gerade zeichnen</div>
          <ol class="weg">
            <li>\(y = \tfrac{2}{3}x - 1\): Punkt \((0 \mid -1)\) auf der \(y\)-Achse <span class="warum">\(b = -1\)</span></li>
            <li>von dort \(3\) nach rechts, \(2\) hinauf: \((3 \mid 1)\) <span class="warum">Steigungsdreieck \(m = \tfrac{2}{3}\)</span></li>
            <li>beide Punkte verbinden und verlängern <span class="warum">zwei Punkte bestimmen eine Gerade</span></li>
          </ol>
          <p>Ebenso gut: eine Wertetabelle mit zwei Werten von \(x\).</p>
          <p><b>Punktprobe:</b> Liegt \(P(6 \mid 3)\) auf der Geraden? \(\tfrac{2}{3} \cdot 6 - 1 = 3\): ja.</p>
          <p><b>Nullstelle</b> (Schnitt mit der \(x\)-Achse): \(y = 0\) setzen, \(\tfrac{2}{3}x - 1 = 0\), also \(\tfrac{2}{3}x = 1\). Mal \(3\): \(2x = 3\), durch \(2\): \(x = 1.5\). Eine waagrechte Gerade (\(m = 0\), \(b \neq 0\)) hat keine Nullstelle.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Dreieck im Ursprung begonnen:</b> Das Steigungsdreieck startet bei \((0 \mid b)\), nicht bei \((0 \mid 0)\). Sonst entsteht \(y = \tfrac{2}{3}x\).</p>
          <p><b>Bei negativem \(m\) hinauf gezeichnet:</b> \(m = -2\) heisst \(1\) nach rechts und \(2\) <b>hinunter</b>.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 14, [
    ('3a', 3, r'Zeichne die Geraden \(y = 2x - 3\) und \(y = -\tfrac{1}{2}x + 2\) ins gleiche Koordinatensystem.',
     r'<p>\(y = 2x - 3\): von \((0 \mid -3)\) aus \(1\) nach rechts, \(2\) hinauf, also durch \((1 \mid -1)\) und \((2 \mid 1)\). \(y = -\tfrac{1}{2}x + 2\): von \((0 \mid 2)\) aus \(2\) nach rechts, \(1\) hinunter, also durch \((2 \mid 1)\) und \((4 \mid 0)\).</p>',
     '\n            <div class="mini-reihe"><svg class="leer-gitter" aria-label="leeres Koordinatensystem zum Zeichnen"></svg></div>'),
    ('3b', 2, r'Liegen \(A(4 \mid 5)\) und \(B(-2 \mid -6)\) auf \(y = 2x - 3\)?',
     r'<p>\(A\): \(2 \cdot 4 - 3 = 5\), ja. \(B\): \(2 \cdot (-2) - 3 = -7 \neq -6\), nein.</p>', ''),
    ('3c', 2, r'Wo schneiden \(y = 3x - 6\) und \(y = -\tfrac{1}{2}x + 2\) die \(x\)-Achse?',
     r'<p>\(3x - 6 = 0\): \(x = 2\). \(-\tfrac{1}{2}x + 2 = 0\): \(x = 4\).</p>', ''),
    ('3d', 2, r'Nina zeichnet \(y = -2x + 1\): von \((0 \mid 1)\) aus \(1\) nach rechts und \(2\) hinauf. Was ist falsch?',
     r'<p>Bei \(m = -2\) geht es \(2\) hinunter: zweiter Punkt \((1 \mid -1)\). Ninas Gerade steigt, die richtige fällt.</p>', ''),
    ('3e', 3, r'Lies im Bild aus 3a den Schnittpunkt der beiden Geraden ab und prüfe ihn mit beiden Gleichungen.',
     r'<p>Schnittpunkt \((2 \mid 1)\): \(2 \cdot 2 - 3 = 1\) und \(-\tfrac{1}{2} \cdot 2 + 2 = 1\). Er liegt auf beiden Geraden.</p>', ''),
    ('3f', 2, r'Warum genügen zwei Punkte, um eine Gerade zu zeichnen?',
     r'<p>Durch zwei verschiedene Punkte geht genau eine Gerade. Ein dritter Punkt ist eine gute Kontrolle: Liegt er nicht darauf, ist etwas falsch.</p>', ''),
])
k3 = kapitel(3, 'zeichnen', 'Geraden zeichnen', 40,
             r'Du zeichnest eine Gerade aus ihrer Gleichung: zuerst \(b\) auf der \(y\)-Achse, dann das Steigungsdreieck. Du prüfst, ob ein Punkt auf der Geraden liegt, und bestimmst die Nullstelle.',
             (CLIP + 'zeichnen', 'Geraden zeichnen'), sim3,
             (CLIP + 'kontrolle-zeichnen', 'Kontrollfragen zum Zeichnen'), fest3,
             [uebung('zeichnen', 'Gerade zeichnen'), uebung('nullstelle', 'Nullstelle')],
             auf3, V_ACHS, komp='K3')

# ------------------------------------------------------------------ Kapitel 4
sim4 = f'''      <figure class="sim sim-gross" id="sim4" aria-label="Infusion: Inhalt abhängig von der Zeit, mit Ratenwechsel">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Inhalt des Infusionsbeutels über der Zeit"></svg>
        <div class="sl-row">
          {regler('s4-v', 'am Anfang', 'orange', 200, 1000, 300).replace('step="1"', 'step="50"')}
          {regler('s4-r1', 'Rate', 'blau', 1, 10, 2)}
        </div>
        <div class="sl-row">
          {regler('s4-T', 'Wechsel nach', 'grau', 0, 400, 400).replace('step="1"', 'step="10"')}
          {regler('s4-r2', 'Rate danach', 'blau', 1, 10, 2)}
        </div>
        <div class="sl-row">
          {regler('s4-t', 'Zeit t', 'gruen', 0, 400, 0).replace('step="1"', 'step="10"')}
        </div>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Die Gleichung finden</div>
          <p><b>Aus dem Graphen:</b> \(b\) auf der \(y\)-Achse ablesen, \(m\) mit einem Steigungsdreieck zwischen zwei Gitterpunkten.</p>
          <p><b>Aus zwei Punkten:</b> zuerst \(m\), dann einen Punkt einsetzen und \(b\) ausrechnen.</p>
          <ol class="weg">
            <li>\(P(2 \mid 5)\), \(Q(6 \mid 7)\): \(m = \dfrac{7 - 5}{6 - 2} = \dfrac{1}{2}\)</li>
            <li>\(5 = \tfrac{1}{2} \cdot 2 + b\), also \(b = 4\) <span class="warum">\(P\) eingesetzt</span></li>
            <li>\(y = \tfrac{1}{2}x + 4\) <span class="warum">Probe mit \(Q\): \(\tfrac{1}{2} \cdot 6 + 4 = 7\)</span></li>
          </ol>
          <p><b>Aus dem Sachverhalt:</b> Eine Infusion enthält \(500\) ml und läuft mit \(2\) ml pro Minute: \(V = -2t + 500\). Leer ist sie bei \(V = 0\): \(t = 250\) Minuten.</p>
          <p><b>Rate ändert sich:</b> Wird nach \(100\) Minuten auf \(1\) ml pro Minute gestellt, sind noch \(300\) ml drin. Der Graph läuft von \((100 \mid 300)\) mit der neuen Steigung \(-1\) weiter: Er <b>knickt</b>, er springt nicht. Leer nach \(100 + 300 = 400\) Minuten.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>\(b\) mit einem \(y\)-Wert verwechselt:</b> Bei \(P(2 \mid 5)\) ist nicht \(b = 5\). \(b\) ist der Wert bei \(x = 0\).</p>
          <p><b>Nach dem Wechsel neu angefangen:</b> Wer nach \(100\) Minuten wieder bei \(500\) ml beginnt, lässt den Graphen springen. Der Inhalt ändert sich beim Umstellen nicht.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 16, [
    ('4a', 3, r'Stelle die Gleichung der abgebildeten Geraden auf.',
     r'<p>Sie schneidet die \(y\)-Achse bei \(-2\), also \(b = -2\). Von \((0 \mid -2)\) nach \((4 \mid 0)\): \(m = \dfrac{2}{4} = \dfrac{1}{2}\). \(y = \tfrac{1}{2}x - 2\).</p>', bild('1/2,-2', '0,-2;4,0', 'Gerade durch (0 | −2) und (4 | 0)')),
    ('4b', 2, r'Gerade durch \(A(1 \mid 3)\) und \(B(3 \mid 7)\): Gleichung?',
     r'<p>\(m = \dfrac{7 - 3}{3 - 1} = 2\); \(3 = 2 \cdot 1 + b\), \(b = 1\). \(y = 2x + 1\).</p>', ''),
    ('4c', 3, r'Gerade durch \(C(-2 \mid 6)\) und \(D(4 \mid 3)\): Gleichung?',
     r'<p>\(m = \dfrac{3 - 6}{4 - (-2)} = \dfrac{-3}{6} = -\dfrac{1}{2}\); \(3 = -\tfrac{1}{2} \cdot 4 + b\), \(b = 5\). \(y = -\tfrac{1}{2}x + 5\).</p>', ''),
    ('4d', 2, r'Max bestimmt die Gerade durch \(P(3 \mid 4)\) und \(Q(5 \mid 8)\): «\(m = 2\), \(b = 4\)». Prüfe mit \(P\) und korrigiere.',
     r'<p>Mit \(x = 3\) gibt \(y = 2x + 4\) den Wert \(10\), nicht \(4\). Max hat den \(y\)-Wert von \(P\) als \(b\) genommen. Richtig: \(4 = 2 \cdot 3 + b\), \(b = -2\), \(y = 2x - 2\).</p>', ''),
    ('4e', 4, r'Ein Gartentank enthält \(240\) l, eine Pumpe pumpt \(6\) l pro Minute ab. (a) Gleichung? Was bedeuten \(-6\) und \(240\)? (b) Wann ist er leer? (c) Nach \(10\) Minuten wird auf \(4\) l pro Minute gedrosselt: Wann ist er jetzt leer? (d) Zeichne den Graphen von (c) auf Häuschenpapier: \(1\) Häuschen für \(10\) min nach rechts und für \(40\) l nach oben.',
     r'<p>(a) \(V = -6t + 240\): \(240\) l sind am Anfang drin, \(-6\) heisst: pro Minute \(6\) l weniger. (b) \(-6t + 240 = 0\), leer nach \(40\) Minuten. (c) Nach \(10\) Minuten sind \(180\) l übrig, \(180 : 4 = 45\), leer nach \(55\) Minuten. (d) Strecke von \((0 \mid 240)\) bis \((10 \mid 180)\), dann flacher bis \((55 \mid 0)\): ein Knick bei \((10 \mid 180)\), kein Sprung. In Häuschen: von \((0 \mid 6)\) über \((1 \mid 4.5)\) nach \((5.5 \mid 0)\).</p>', ''),
    ('4f', 2, r'Warum springt der Graph beim Wechsel der Rate nicht?',
     r'<p>Beim Umstellen ändert sich nur, wie schnell es weiterläuft. Was im Beutel ist, bleibt im Moment des Wechsels gleich. Darum beginnt das neue Stück dort, wo das alte aufhört.</p>', ''),
])
k4 = kapitel(4, 'gleichung', 'Die Gleichung finden', 45,
             r'Du stellst die Gleichung einer Geraden auf, aus dem Graphen, aus zwei Punkten oder aus einem Sachverhalt, und setzt einen Graphen bei einer neuen Rate ohne Sprung fort.',
             (CLIP + 'gleichung', 'Die Gleichung finden'), sim4,
             (CLIP + 'kontrolle-gleichung', 'Kontrollfragen zur Gleichung'), fest4,
             [uebung('gleichung', 'Gleichung aus dem Graphen'), uebung('zweipunkte', 'Gleichung aus zwei Punkten')],
             auf4, V_LP, komp='K4')

# ------------------------------------------------------------------ Vorwissen
k0 = f'''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-th">Vorwissen</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Koordinaten, Einsetzen, einfache Gleichungen, Brüche mit Minus, Bruch mal Zahl. Zuerst kurz wiederholen, dann der Vortest.</p>
''' + r'''      <details class="anleitung">
        <summary><h3>Kurz wiederholt</h3></summary>
        <ul class="kurz">
          <li><b>Koordinaten:</b> \(P(4 \mid -1)\) heisst \(4\) nach rechts, \(1\) hinunter. Zuerst \(x\), dann \(y\).</li>
          <li><b>Einsetzen:</b> Für \(x = 2\) ist \(5x - 3 = 7\).</li>
          <li><b>Gleichung lösen:</b> \(2x + 3 = 11\) gibt \(2x = 8\), \(x = 4\).</li>
          <li><b>Brüche mit Minus:</b> \(\dfrac{-6}{3} = -2\) und \(\dfrac{-4}{-2} = 2\).</li>
          <li><b>Bruch mal Zahl:</b> \(\tfrac{2}{3} \cdot 6 = \tfrac{12}{3} = 4\). Und \(\tfrac{2}{3}x = 4\) löst du mit «mal \(3\), durch \(2\)»: \(2x = 12\), \(x = 6\).</li>
        </ul>
      </details>
''' + test('t0', 'Vortest', 12, [
    ('0a', 2, r'Lies die Koordinaten der beiden Punkte ab.',
     r'<p>\((3 \mid 2)\) und \((-2 \mid -4)\).</p>', bild('', '3,2;-2,-4', 'Zwei Punkte im Koordinatensystem')),
    ('0b', 2, r'Setze ein: \(y = 4x - 7\) für \(x = 3\) und für \(x = -2\).',
     r'<p>\(5\) und \(-15\).</p>', ''),
    ('0c', 2, r'Löse: \(3x + 6 = 0\) und \(5x - 4 = 11\).',
     r'<p>\(x = -2\) und \(x = 3\).</p>', ''),
    ('0d', 2, r'Berechne: \(\dfrac{9 - 1}{6 - 2}\) und \(\dfrac{2 - 8}{4 - 1}\).',
     r'<p>\(2\) und \(-2\).</p><p class="komm">So berechnest du in Kapitel 2 die Steigung.</p>', ''),
    ('0e', 2, r'Ein Liter kostet \(2\) Fr. Fülle die Tabelle: \(0, 1, 2, 3\) Liter kosten …',
     r'<p>\(0,\ 2,\ 4,\ 6\) Fr. Bei jedem Liter mehr kommen \(2\) Fr. dazu.</p>', ''),
    ('0f', 2, r'Berechne \(\tfrac{3}{4} \cdot 8\) und löse \(\tfrac{3}{4}x = 6\).',
     r'<p>\(6\) und \(x = 8\) (mal \(4\): \(3x = 24\), durch \(3\)).</p><p class=\"komm\">Das brauchst du ab Kapitel 3.</p>', ''),
]) + '''
      <p class="komm">Weniger als 8 von 12 Punkten: «Kurz wiederholt» nochmals lesen und die Lösungen nachrechnen; Gleichungen übst du im Leitprogramm «Bruchterme, Gleichungen und Formeln».</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/lineare-funktionen/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-th">Kapitel 1–4</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg, ohne Taschenrechner. Lineal mitnehmen.<br>
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
            <tr><td>17 – 21 P</td><td>Den schwächsten Teil nochmals, gemessen am Anteil (Teil A 6, B 10, C 9 P): Tüfteln und Übungen der Kapitel dieses Teils.</td></tr>
            <tr><td>11 – 16 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 10 P</td><td>Zurück zu den Kapiteln jedes Teils, in dem du weniger als die Hälfte erreicht hast; sind es alle drei, zum Vortest und zu Kapitel 1.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1, G2 → 1; G3 → 2; G4 → 3; G5 bis G8 → 4</p>
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
            <div class="frage"><span class="nr">V1</span><span class="txt">Zwei Velovermietungen: A kostet \(5\) Fr. plus \(4\) Fr. pro Stunde, B \(17\) Fr. plus \(1\) Fr. pro Stunde. Ab wie vielen Stunden ist B günstiger?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>Gleich teuer bei \(4x + 5 = x + 17\), also \(x = 4\) Stunden (je \(21\) Fr.). Ab mehr als \(4\) Stunden ist B günstiger: Seine Gerade ist flacher.</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V2</span><span class="txt">Liegen \(A(0 \mid 1)\), \(B(2 \mid 4)\) und \(C(6 \mid 10)\) auf einer Geraden? Begründe mit Steigungen.</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>Von \(A\) nach \(B\): \(m = \tfrac{3}{2}\). Von \(B\) nach \(C\): \(m = \tfrac{6}{4} = \tfrac{3}{2}\). Gleiche Steigung und ein gemeinsamer Punkt: ja.</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V3</span><span class="txt">Eine Gerade hat die Nullstelle \(3\) und schneidet die \(y\)-Achse bei \(-6\). Wie lautet ihre Gleichung?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>Punkte \((3 \mid 0)\) und \((0 \mid -6)\): \(m = \dfrac{0 - (-6)}{3 - 0} = 2\), \(b = -6\). \(y = 2x - 6\).</p></div></details>
          </li>
        </ol>
      </div>
      <p class="ausf weiter">Weiter: Lagebeziehungen von Geraden, Schnittpunkte und Modellieren im ''' + V_LP + r''' von Mathe begreifbar.</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Lineare Funktionen, Version 1.0 (10.10.2026). Gebaut aus scripts/lp/lineare-funktionen/seite.py —
     Änderungen dort, nicht in dieser Datei. Grundlagen: HOWTO-leitprogramme.md (Kapitelmuster) und
     ~/TODO-BM-Vorkurs-LP03-15.md, Abschnitt 2 (LP 04, Lineare Funktionen I), für die Sek I umgesetzt.

     Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026): Das Leitprogramm ist selbst die fachliche Quelle;
     Vertiefung bei Mathe begreifbar, auch das lange Leitprogramm Lineare Funktionen (verlinkt, nicht übernommen).
     Notation: y = m · x + b, Steigung m, y-Achsenabschnitt b (Anfangswert), Punkte (x | y), Dezimalpunkt.

     Kompetenzen — eigene Formulierung, ohne Lehrplan-Nummern (CLAUDE.md: keine erfundenen Lehrplan-Stellen):
       K1  Linearen Zusammenhang als y = m · x + b beschreiben (Anfangswert, Änderung pro Einheit), Werte berechnen
       K2  Steigung aus Steigungsdreieck und aus zwei Punkten bestimmen, Vorzeichen deuten
       K3  Gerade aus der Gleichung zeichnen, Punktprobe, Nullstelle
       K4  Gleichung aus Graph, zwei Punkten oder Sachverhalt aufstellen; Ratenwechsel ohne Sprung fortsetzen

     Kompetenzmatrix (Kompetenz | Kapitel | Simulation | Übungen | Kapitelaufgaben | Gesamttest):
       K1 | 1 | Sim 1 Fass        | wert, kontext          | 1a–1f | G1, G2
       K2 | 2 | Sim 2 Dreieck     | steigung, ablesen      | 2a–2f | G3
       K3 | 3 | Sim 3 m und b     | zeichnen, nullstelle   | 3a–3f | G4
       K4 | 4 | Sim 4 Infusion    | gleichung, zweipunkte  | 4a–4f | G5–G8

     Planung (Kapitel | Lernziel | Erkundung | Beispiel | Häufiger Fehler | min):
       0 | Vorwissen     | –                    | –                          | –                                   | 10
       1 | Anfangswert   | Fass                 | Tank 200 l + 15 l/min      | m und b vertauscht; Probe mit x = 1 | 40
       2 | Steigung      | Steigungsdreieck     | P(1 | 2), Q(4 | 8)         | Bruch vertauscht; Reihenfolge       | 40
       3 | zeichnen      | m kippt, b schiebt   | y = 2/3 x − 1              | Dreieck im Ursprung; Vorzeichen     | 40
       4 | Gleichung     | Infusion             | P(2 | 5), Q(6 | 7); 500 ml | b = y-Wert; Sprung beim Wechsel     | 45
       Gesamttest (PDF) 30 · Summe 205 min ≈ 4.6 Lektionen. Vertiefung V1–V3 freiwillig, nicht eingerechnet.

     Aus der Vorlage umgesetzt: m/b-Geradenexperiment (Sim 3), Infusion mit Anfangswert, Abnahmerate und Ratenwechsel
     (Sim 4, Festhalten 4, Gesamttest G6/G8), zwei Graph-/Gleichungswechsel und eine Kontextaufgabe im Selbstcheck.
     Bewusst nicht übernommen: Teams-Ablauf, Lehrpersonenteil, Prüfungsnummern.

     Clips: je Kapitel ein Einführungsclip (mit einer Vorhersagefrage) und ein Kontrollclip mit fünf Fragen,
     Reihe «Funktionen sehen», lin-lp-*.json, erzeugt mit scripts/lp/lineare-funktionen/clips.py.

     Farben: Gerade und m blau, b, Punkte und Steigungsdreieck orange, Treffer grün, Fehler rot; Bereichsfarbe Petrol.
     Gesamttest und Bewertungspaket nur als PDF (downloads/leitprogramme/lineare-funktionen/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Sek1-Mathe begreifbar · Leitprogramm</p>
      <h1>Lineare Funktionen</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Funktionen</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Anfangswert</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Steigung</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Zeichnen</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Gleichung finden</span></a></li>
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
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen. Mit <b>💡 Tipp</b> bekommst du Hilfe in drei Stufen. Zahlen tippst du als <code>2</code>, <code>-1.5</code> oder Bruch <code>2/3</code>; beim Zeichnen klickst du zwei Punkte im Gitter an.</li>
          <li><b>⑤ Aufgaben</b> auf Papier mit Rechenweg, dann Lösung aufklappen und abhaken.</li>
          <li>Zum Schluss der <b>Gesamttest</b> auf Papier, mit Lineal. Alles ohne Taschenrechner.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">Das kannst du danach, alles <span class="ohm">ohne Taschenrechner</span>:</p>
        <ul>
          <li><b>K1</b> einen linearen Zusammenhang als \\(y = m \\cdot x + b\\) beschreiben: \\(b\\) als Anfangswert, \\(m\\) als Änderung pro Einheit, und damit Werte berechnen (Kapitel 1)</li>
          <li><b>K2</b> die Steigung mit einem Steigungsdreieck und aus zwei Punkten bestimmen und ihr Vorzeichen deuten (Kapitel 2)</li>
          <li><b>K3</b> eine Gerade aus ihrer Gleichung zeichnen, Punkte prüfen und die Nullstelle bestimmen (Kapitel 3)</li>
          <li><b>K4</b> die Gleichung aus dem Graphen, aus zwei Punkten oder aus einem Sachverhalt aufstellen und einen Ratenwechsel ohne Sprung fortsetzen (Kapitel 4)</li>
        </ul>
        <p class="rlp-quelle">Nicht in diesem Leitprogramm: Lagebeziehungen, Schnittpunkte rechnerisch, Darstellungswechsel mit Definitionsbereich. Zum Vertiefen bei Mathe begreifbar: ''' + V_LP + ' · ' + V_DEF + '''.</p>
      </details>

    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Lineare Funktionen · Sek1-Mathe begreifbar</span>
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
<script>buildNav({{ bereich: 'lp', id: 'lp-linear' }});</script>
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
