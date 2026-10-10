"""Baut leitprogramme/pythagoras.html aus einer Kapitelbeschreibung (10.10.2026).

  python3 scripts/lp/pythagoras/seite.py

Leitprogramm Flächen, Pythagoras und Ähnlichkeit (Bereich Geometrie), Gerüst aus scripts/lp/bewegung/.
Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026); vertieft wird auf den Themenseiten von
Mathe begreifbar (TALS). Alles kommt aus diesem Ordner: kopf.css, seite.css, basis.js (Thema, Fortschritt,
Schiene), seite.js (Geometrie-Simulationen, Übungen mit Figuren). Nur der SEO-Block wird aus der bestehenden Seite
übernommen — ihn schreibt scripts/build-seo.py. Wiederholbar. Danach Pre-Flight und build-seo.py.
"""
import json
import os

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/pythagoras.html'
NAME = 'Flächen, Pythagoras und Ähnlichkeit'
STAND = 'Stand 10. Oktober 2026'
CLIP = 'pyt-lp-'

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
V_DREI = tals('grundlagen/g5-2a-dreiecke.html', 'Dreiecke und Pythagoras')
V_VIER = tals('grundlagen/g5-2b-vierecke.html', 'Vierecke')
V_KREIS = tals('grundlagen/g5-2c-kreis-und-kreisteile.html', 'Kreis und Kreisteile')
V_AEHN = tals('grundlagen/g5-2d-zentrische-streckung-aehnlichkeit.html', 'Zentrische Streckung und Ähnlichkeit')


def svg(inhalt, label, vb='0 0 240 150', breite=240):
    return f'<svg class="fest-figur" viewBox="{vb}" width="{breite}" role="img" aria-label="{label}">{inhalt}</svg>'


# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1" aria-label="Dreieck oder Parallelogramm mit Grundseite, Höhe und verschiebbarer Spitze">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Figur mit Grundseite g und gestrichelter Höhe h"></svg>
        <div class="sl-row">
          <label class="sim-schalter" for="s1-typ">Figur
            <select id="s1-typ" class="sim-wahl"><option value="d" selected>Dreieck</option><option value="p">Parallelogramm</option></select></label>
        </div>
        <div class="sl-row">
          {regler('s1-g', 'Grundseite g', 'blau', 2, 12, 6)}
          {regler('s1-h', 'Höhe h', 'orange', 1, 8, 3)}
        </div>
        <div class="sl-row">
          {regler('s1-s', 'Spitze verschieben', 'grau', -4, 14, 2)}
        </div>
      </figure>'''
FIG1 = svg('<polygon points="20,120 140,120 70,40" class="flaeche blau"/><line x1="70" y1="120" x2="70" y2="40" class="linie orange gestrichelt"/>'
           '<polyline points="79,120 79,111 70,111" class="linie grau" fill="none"/><text x="80" y="138" class="p-text blau" text-anchor="middle">g</text>'
           '<text x="80" y="85" class="p-text orange">h</text><text x="34" y="75" class="p-text grau">schräg</text>', 'Dreieck mit Grundseite g, Höhe h und schräger Seite')
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Fläche aus Grundseite und Höhe</div>
          <p class="mini-reihe">''' + FIG1 + r'''</p>
          <ul class="kurz">
            <li><b>Dreieck:</b> \(A = \dfrac{g \cdot h}{2}\), zum Beispiel \(g = 8\) cm, \(h = 5\) cm: \(A = 20\) cm².</li>
            <li><b>Parallelogramm:</b> \(A = g \cdot h\), zum Beispiel \(7 \cdot 4 = 28\) cm².</li>
            <li><b>Trapez:</b> \(A = \dfrac{a + c}{2} \cdot h\) mit den parallelen Seiten \(a\) und \(c\): \(\dfrac{9 + 5}{2} \cdot 4 = 28\) cm².</li>
            <li><b>Zusammengesetzte Figuren:</b> zerlegen (Rechteck plus Dreieck) oder ergänzen (ganzes Rechteck minus Ecke): \(8 \cdot 6 - 3 \cdot 2 = 42\) cm².</li>
          </ul>
          <p>Die <b>Höhe</b> steht senkrecht auf der Grundseite, notfalls auf ihrer Verlängerung. Verschiebst du die Spitze parallel zur Grundseite, bleibt die Fläche gleich.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Schräge Seite statt Höhe:</b> Die schräge Seite ist länger als die Höhe. Mit ihr wird die Fläche zu gross.</p>
          <p><b>Halbieren vergessen:</b> Ein Dreieck ist halb so gross wie das Parallelogramm mit gleicher Grundseite und Höhe.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 14, [
    ('1a', 3, r'Berechne die Fläche: (a) Dreieck mit \(g = 9\) cm, \(h = 6\) cm. (b) Parallelogramm mit \(g = 12\) cm, Höhe \(5\) cm und schräger Seite \(7\) cm.',
     r'<p>(a) \(\dfrac{9 \cdot 6}{2} = 27\) cm². (b) \(12 \cdot 5 = 60\) cm². Die schräge Seite \(7\) cm brauchst du nicht.</p>', ''),
    ('1b', 2, r'Ein Trapez hat die parallelen Seiten \(11\) cm und \(7\) cm und die Höhe \(6\) cm. Wie gross ist seine Fläche?',
     r'<p>\(\dfrac{11 + 7}{2} \cdot 6 = 9 \cdot 6 = 54\) cm².</p>', ''),
    ('1c', 3, r'Aus einem Rechteck \(10\) cm \(\times\) \(8\) cm wird ein rechtwinkliges Dreieck mit den Katheten \(4\) cm und \(3\) cm ausgeschnitten. Wie gross ist die Restfläche?',
     r'<p>\(10 \cdot 8 - \dfrac{4 \cdot 3}{2} = 80 - 6 = 74\) cm².</p>', ''),
    ('1d', 2, r'Mia berechnet ein Dreieck mit Grundseite \(12\) cm, Höhe \(8\) cm und schräger Seite \(10\) cm so: \(\dfrac{12 \cdot 10}{2} = 60\) cm². Was ist falsch?',
     r'<p>Sie hat die schräge Seite statt der Höhe genommen. Richtig: \(\dfrac{12 \cdot 8}{2} = 48\) cm².</p>', ''),
    ('1e', 2, r'Ein Dreieck hat die Fläche \(30\) cm² und die Grundseite \(12\) cm. Wie hoch ist es?',
     r'<p>\(\dfrac{12 \cdot h}{2} = 30\), also \(6h = 30\), \(h = 5\) cm.</p>', ''),
    ('1f', 2, r'Warum ändert sich die Fläche eines Dreiecks nicht, wenn du die Spitze parallel zur Grundseite verschiebst?',
     r'<p>Grundseite und Höhe bleiben gleich, und nur sie stehen in der Formel \(A = \dfrac{g \cdot h}{2}\). Die schrägen Seiten ändern sich, zählen aber nicht.</p>', ''),
])
k1 = kapitel(1, 'flaechen', 'Grundseite und Höhe', 40,
             r'Du berechnest Flächen von Dreieck, Parallelogramm und Trapez mit Grundseite und Höhe und zerlegst oder ergänzt zusammengesetzte Figuren.',
             (CLIP + 'flaechen', 'Grundseite und Höhe'), sim1,
             (CLIP + 'kontrolle-flaechen', 'Kontrollfragen zu Flächen'), fest1,
             [uebung('flaeche', 'Fläche berechnen'), uebung('zusammen', 'Zusammengesetzte Figuren')],
             auf1, V_VIER, komp='K1')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2" aria-label="Rechtwinkliges Dreieck mit Quadraten über allen Seiten">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Quadrate über den Katheten a und b und über der Hypotenuse c"></svg>
        <div class="sl-row">
          {regler('s2-a', 'Kathete a', 'blau', 1, 24, 3)}
          {regler('s2-b', 'Kathete b', 'orange', 1, 24, 4)}
        </div>
      </figure>'''
FIG2 = svg('<polygon points="30,120 150,120 30,40" class="flaeche blau"/><polyline points="39,120 39,111 30,111" class="linie grau" fill="none"/>'
           '<text x="90" y="138" class="p-text blau" text-anchor="middle">a (Kathete)</text><text x="24" y="84" class="p-text orange" text-anchor="end">b</text>'
           '<text x="100" y="72" class="p-text gruen">c (Hypotenuse)</text>', 'rechtwinkliges Dreieck mit Katheten a und b und Hypotenuse c', '0 0 260 150', 260)
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Satz des Pythagoras</div>
          <p class="mini-reihe">''' + FIG2 + r'''</p>
          <p>Im rechtwinkligen Dreieck liegt die <b>Hypotenuse</b> \(c\) gegenüber dem rechten Winkel, sie ist die längste Seite. Die beiden anderen Seiten sind die <b>Katheten</b>.</p>
          <p>\[ a^2 + b^2 = c^2 \]</p>
          <ul class="kurz">
            <li>Hypotenuse gesucht: \(a = 6\), \(b = 8\): \(c^2 = 36 + 64 = 100\), \(c = 10\).</li>
            <li>Kathete gesucht: \(c = 10\), \(a = 6\): \(b^2 = 100 - 36 = 64\), \(b = 8\).</li>
            <li>Rechtwinklig? Gilt für die Seiten \(a^2 + b^2 = c^2\) (mit \(c\) der längsten Seite), dann ja.</li>
          </ul>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Bei der Kathete addiert:</b> Für eine Kathete rechnest du \(c^2 - a^2\), nicht \(c^2 + a^2\). Das Ergebnis muss kürzer als die Hypotenuse sein.</p>
          <p><b>Seiten statt Quadrate:</b> \(6 + 8 = 14\) ist nicht die Hypotenuse. Und \(c^2 = 100\) ist erst \(c^2\): Wurzel ziehen.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 14, [
    ('2a', 2, r'Die Katheten eines rechtwinkligen Dreiecks sind \(15\) cm und \(20\) cm lang. Wie lang ist die Hypotenuse?',
     r'<p>\(c^2 = 225 + 400 = 625\), \(c = 25\) cm.</p>', ''),
    ('2b', 3, r'Die Hypotenuse ist \(26\) cm, eine Kathete \(10\) cm lang. Wie lang ist die andere Kathete?',
     r'<p>\(b^2 = 676 - 100 = 576\), \(b = 24\) cm.</p>', ''),
    ('2c', 2, r'Sind die Dreiecke rechtwinklig? (a) Seiten \(7\), \(24\), \(25\) cm. (b) Seiten \(6\), \(7\), \(9\) cm.',
     r'<p>(a) \(49 + 576 = 625 = 25^2\): ja. (b) \(36 + 49 = 85 \neq 81\): nein.</p>', ''),
    ('2d', 2, r'Ben rechnet für \(c = 13\) cm und \(a = 5\) cm: \(b^2 = 169 + 25 = 194\). Was ist falsch?',
     r'<p>Für eine Kathete wird subtrahiert: \(b^2 = 169 - 25 = 144\), \(b = 12\) cm. Mit \(+\) wäre \(b\) länger als die Hypotenuse.</p>', ''),
    ('2e', 3, r'Ein rechtwinkliges Dreieck hat die Seiten \(x\), \(40\) cm und \(41\) cm. Der rechte Winkel liegt zwischen \(x\) und der Seite \(40\) cm. Welche Seite ist die Hypotenuse? Berechne \(x\).',
     r'<p>Die Hypotenuse liegt gegenüber dem rechten Winkel: die Seite \(41\) cm. \(x^2 = 1681 - 1600 = 81\), \(x = 9\) cm.</p>', ''),
    ('2f', 2, r'Warum ist die Hypotenuse immer die längste Seite eines rechtwinkligen Dreiecks?',
     r'<p>\(c^2 = a^2 + b^2\) ist grösser als \(a^2\) und grösser als \(b^2\). Darum ist auch \(c\) länger als \(a\) und als \(b\).</p>', ''),
])
k2 = kapitel(2, 'pythagoras', 'Der Satz des Pythagoras', 40,
             r'Du erkennst Hypotenuse und Katheten, berechnest mit \(a^2 + b^2 = c^2\) eine fehlende Seite und prüfst, ob ein Dreieck rechtwinklig ist.',
             (CLIP + 'pythagoras', 'Der Satz des Pythagoras'), sim2,
             (CLIP + 'kontrolle-pythagoras', 'Kontrollfragen zu Pythagoras'), fest2,
             [uebung('hypotenuse', 'Hypotenuse berechnen'), uebung('kathete', 'Kathete berechnen')],
             auf2, V_DREI, komp='K2')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3" aria-label="Kreis mit Sehne und Hilfsdreieck">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Kreis mit waagrechter Sehne, darunter Wasser, Hilfsdreieck aus Abstand, halber Sehne und Radius"></svg>
        <div class="sl-row">
          {regler('s3-r', 'Radius r', 'gruen', 2, 15, 10)}
          {regler('s3-d', 'Abstand d', 'orange', 0, 15, 6)}
        </div>
      </figure>'''
FIG3 = svg('<circle cx="80" cy="75" r="60" class="linie tinte"/><line x1="32" y1="111" x2="128" y2="111" class="linie blau"/>'
           '<line x1="80" y1="75" x2="80" y2="111" class="linie orange"/><line x1="80" y1="75" x2="128" y2="111" class="linie gruen"/>'
           '<polyline points="89,111 89,102 80,102" class="linie grau" fill="none"/><circle cx="80" cy="75" r="3" class="pkt"/>'
           '<text x="104" y="126" class="p-text blau" text-anchor="middle">s/2</text><text x="74" y="96" class="p-text orange" text-anchor="end">d</text>'
           '<text x="108" y="88" class="p-text gruen">r</text>', 'Kreis mit Sehne s, Abstand d und Radius r', '0 0 170 150', 170)
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Das Hilfsdreieck finden</div>
          <ol class="weg">
            <li>Rechten Winkel suchen oder einzeichnen (Höhe, Diagonale, Abstand). <span class="warum">wo ist 90°?</span></li>
            <li>Hilfsdreieck markieren, Hypotenuse bestimmen. <span class="warum">gegenüber dem rechten Winkel</span></li>
            <li>Bekannte Längen eintragen, oft halbiert. <span class="warum">halbe Grundseite, halbe Sehne</span></li>
            <li>Pythagoras anwenden. <span class="warum">plus für c, minus für eine Kathete</span></li>
          </ol>
          <ul class="kurz">
            <li>Rechteck \(20 \times 21\) cm: Diagonale \(\sqrt{400 + 441} = \sqrt{841} = 29\) cm.</li>
            <li>Gleichschenkliges Dreieck, Basis \(16\), Schenkel \(17\): Höhe \(\sqrt{17^2 - 8^2} = 15\).</li>
          </ul>
          <p class="mini-reihe">''' + FIG3 + r'''</p>
          <p><b>Kreis:</b> Radius \(r\), Durchmesser \(2r\). Eine <b>Sehne</b> verbindet zwei Punkte des Kreises. Der Abstand \(d\) vom Mittelpunkt steht senkrecht auf ihr und halbiert sie: \(\left(\tfrac{s}{2}\right)^2 + d^2 = r^2\). Beispiel \(r = 10\), \(s = 16\): \(d = \sqrt{100 - 64} = 6\).</p>
          <p><b>Rohr:</b> Durchmesser \(50\) cm, Wasserspiegel \(48\) cm breit: \(d = \sqrt{625 - 576} = 7\) cm, Wassertiefe \(25 - 7 = 18\) cm (Wasser unter der Mitte).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Ganze statt halbe Strecke:</b> Die Höhe halbiert die Basis, der Abstand halbiert die Sehne. Ins Hilfsdreieck gehört die Hälfte.</p>
          <p><b>Falsche Hypotenuse:</b> Im Kreis ist der Radius die Hypotenuse, nicht die Sehne.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 14, [
    ('3a', 2, r'Ein Rechteck ist \(15\) cm lang und \(8\) cm breit. Wie lang ist seine Diagonale?',
     r'<p>\(\sqrt{225 + 64} = \sqrt{289} = 17\) cm.</p>', ''),
    ('3b', 3, r'Ein gleichschenkliges Dreieck hat die Basis \(30\) cm und Schenkel von \(25\) cm. Berechne die Höhe und die Fläche.',
     r'<p>Halbe Basis \(15\) cm: \(h = \sqrt{625 - 225} = \sqrt{400} = 20\) cm. Fläche \(\dfrac{30 \cdot 20}{2} = 300\) cm².</p>', ''),
    ('3c', 2, r'Eine \(5\) m lange Leiter lehnt an einer senkrechten Wand. Ihr Fuss steht \(1.4\) m von der Wand entfernt. Wie hoch reicht sie?',
     r'<p>\(h^2 = 25 - 1.96 = 23.04\), \(h = 4.8\) m.</p>', ''),
    ('3d', 2, r'Ein Kreis hat den Radius \(26\) cm. Eine Sehne ist \(48\) cm lang. Wie weit ist sie vom Mittelpunkt entfernt?',
     r'<p>Halbe Sehne \(24\) cm: \(d = \sqrt{676 - 576} = \sqrt{100} = 10\) cm.</p>', ''),
    ('3e', 3, r'Ein Rohr hat den Innendurchmesser \(34\) cm. Der Wasserspiegel ist \(30\) cm breit, das Wasser steht weniger als halb hoch. Wie tief ist das Wasser?',
     r'<p>\(r = 17\), halbe Breite \(15\): \(d = \sqrt{289 - 225} = 8\) cm. Wassertiefe \(17 - 8 = 9\) cm.</p>', ''),
    ('3f', 2, r'Wie weit sind die Punkte \(A(1 \mid 2)\) und \(B(7 \mid 10)\) im Koordinatensystem voneinander entfernt (Einheit cm)?',
     r'<p>Hilfsdreieck mit den Katheten \(7 - 1 = 6\) und \(10 - 2 = 8\): \(\sqrt{36 + 64} = 10\) cm.</p>', ''),
])
k3 = kapitel(3, 'hilfsdreieck', 'Hilfsdreiecke und Kreis', 40,
             r'Du findest in Rechteck, gleichschenkligem Dreieck und Kreis das rechtwinklige Hilfsdreieck und berechnest Diagonalen, Höhen, Sehnen und die Wassertiefe in einem Rohr.',
             (CLIP + 'hilfsdreieck', 'Hilfsdreiecke und Kreis'), sim3,
             (CLIP + 'kontrolle-hilfsdreieck', 'Kontrollfragen zu Hilfsdreiecken'), fest3,
             [uebung('hilfsdreieck', 'Hilfsdreieck finden'), uebung('sehne', 'Sehne und Abstand')],
             auf3, V_KREIS, komp='K3')

# ------------------------------------------------------------------ Kapitel 4
sim4 = f'''      <figure class="sim sim-gross" id="sim4" aria-label="Rechtwinkliges Dreieck und ähnliches Bilddreieck mit Streckfaktor k">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Original blau mit Katheten 4 und 3, Bild orange mit k-fachen Seiten"></svg>
        <div class="sl-row">
          {regler('s4-k', 'Streckfaktor k', 'orange', 0.5, 3, 1).replace('step="1"', 'step="0.25"')}
        </div>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Ähnliche Figuren</div>
          <p>Zwei Figuren sind <b>ähnlich</b>, wenn alle Winkel gleich sind und alle Längen mit demselben <b>Streckfaktor</b> \(k\) multipliziert werden: \(k = \dfrac{\text{Bildlänge}}{\text{Originallänge}}\).</p>
          <ul class="kurz">
            <li>Dreieck \(3, 4, 5\) mit \(k = 2\): \(6, 8, 10\).</li>
            <li><b>Flächen</b> wachsen mit \(k^2\): Fläche \(6\) cm² wird \(6 \cdot 2^2 = 24\) cm².</li>
            <li><b>Verhältnisse</b> (Strahlensatz): Stab \(2\) m wirft \(3\) m Schatten, der Baum \(15\) m: Baum \(\dfrac{2}{3} \cdot 15 = 10\) m.</li>
            <li><b>Regal:</b> grosses Dreieck \(60 \times 40\) (Fläche \(1200\)), darin ein ähnliches mit \(k = \tfrac{1}{2}\): Fläche \(1200 \cdot \tfrac{1}{4} = 300\). Differenz \(900\).</li>
          </ul>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Flächenfaktor = Längenfaktor:</b> Bei \(k = 3\) wird die Fläche nicht dreimal, sondern \(9\)-mal so gross.</p>
          <p><b>Gleich viel addiert:</b> Ähnlich heisst «mal \(k\)», nicht «überall gleich viel länger».</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 14, [
    ('4a', 3, r'Ein Dreieck hat die Seiten \(4\), \(6\) und \(8\) cm. Im ähnlichen Bilddreieck ist die längste Seite \(12\) cm. Berechne \(k\) und die anderen Seiten.',
     r'<p>\(k = \dfrac{12}{8} = 1.5\). Seiten \(4 \cdot 1.5 = 6\) cm und \(6 \cdot 1.5 = 9\) cm.</p>', ''),
    ('4b', 2, r'Eine Figur mit \(10\) cm² wird mit \(k = 3\) gestreckt. Wie gross ist die Bildfläche?',
     r'<p>\(10 \cdot 3^2 = 90\) cm².</p>', ''),
    ('4c', 3, r'Ein \(1.5\) m langer Stab wirft einen \(2\) m langen Schatten. Ein Haus wirft gleichzeitig einen \(12\) m langen Schatten. Wie hoch ist das Haus?',
     r'<p>Die Dreiecke aus Gegenstand und Schatten sind ähnlich: \(\dfrac{1.5}{2} = \dfrac{x}{12}\), \(x = 9\) m.</p>', ''),
    ('4d', 2, r'Lea verdreifacht alle Seiten eines Dreiecks mit \(15\) cm² Fläche und sagt: «Die Fläche ist jetzt \(45\) cm².» Stimmt das?',
     r'<p>Nein. Die Fläche wird mit \(k^2 = 9\) multipliziert: \(135\) cm².</p>', ''),
    ('4e', 2, r'Ein rechtwinkliges Brett hat die Katheten \(80\) cm und \(60\) cm. In einer Ecke wird ein ähnliches Dreieck mit \(k = \tfrac{1}{4}\) ausgesägt. Wie gross ist die Restfläche?',
     r'<p>\(\dfrac{80 \cdot 60}{2} = 2400\) cm². Ausgesägt: \(2400 \cdot \tfrac{1}{16} = 150\) cm² (Katheten \(20\) und \(15\)). Rest \(2250\) cm².</p>', ''),
    ('4f', 2, r'Eine Figur wird mit \(k = 0.5\) verkleinert. Warum ist die neue Fläche nur ein Viertel so gross?',
     r'<p>Länge und Breite werden beide halbiert: \(0.5 \cdot 0.5 = 0.25\), also ein Viertel.</p>', ''),
])
k4 = kapitel(4, 'aehnlichkeit', 'Ähnliche Figuren', 40,
             r'Du erkennst ähnliche Figuren, berechnest Streckfaktor und fehlende Längen, nutzt Verhältnisse (Strahlensatz) und unterscheidest den Längenfaktor \(k\) vom Flächenfaktor \(k^2\).',
             (CLIP + 'aehnlichkeit', 'Ähnliche Figuren'), sim4,
             (CLIP + 'kontrolle-aehnlichkeit', 'Kontrollfragen zur Ähnlichkeit'), fest4,
             [uebung('aehnlich', 'Fehlende Seite'), uebung('flaechenfaktor', 'Längen- und Flächenfaktor')],
             auf4, V_AEHN, komp='K4')

# ------------------------------------------------------------------ Vorwissen
k0 = f'''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-th">Vorwissen</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Rechteck, Quadratzahlen und Wurzeln, Einheiten, Verhältnisse. Zuerst kurz wiederholen, dann der Vortest.</p>
''' + r'''      <details class="anleitung">
        <summary><h3>Kurz wiederholt</h3></summary>
        <ul class="kurz">
          <li><b>Rechteck:</b> Fläche Länge mal Breite, Umfang zweimal Länge plus Breite: \(5 \times 3\) cm hat \(15\) cm² und \(16\) cm.</li>
          <li><b>Quadratzahlen und Wurzeln:</b> \(1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225\). \(\sqrt{49} = 7\), weil \(7^2 = 49\).</li>
          <li><b>Flächeneinheiten:</b> \(1\) m² \(= 100 \cdot 100\) cm² \(= 10\,000\) cm².</li>
          <li><b>Verhältnisse:</b> \(2 : 5 = 4 : 10\), beide Zahlen mal \(2\).</li>
        </ul>
      </details>
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Ein Rechteck ist \(7\) cm lang und \(4\) cm breit. Wie gross sind Fläche und Umfang?', r'<p>\(28\) cm² und \(22\) cm.</p>', ''),
    ('0b', 2, r'Berechne \(7^2\), \(12^2\), \(\sqrt{81}\) und \(\sqrt{144}\).', r'<p>\(49\), \(144\), \(9\), \(12\).</p>', ''),
    ('0c', 2, r'Welche positive Zahl \(x\) erfüllt \(x^2 = 64\)?', r'<p>\(x = 8\).</p>', ''),
    ('0d', 2, r'Wie viele cm² sind \(1\) m²? Wie viele cm sind \(3.5\) m?', r'<p>\(10\,000\) cm² und \(350\) cm.</p>', ''),
    ('0e', 2, r'Ergänze: \(6 : 4 = 9 : \ ?\)', r'<p>\(6\), denn beide Zahlen werden mit \(1.5\) multipliziert.</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: «Kurz wiederholt» nochmals lesen und die Lösungen nachrechnen.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest (nur PDF)
PDF = '../downloads/leitprogramme/pythagoras/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-th">Kapitel 1–4</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Skizze und Rechenweg, ohne Taschenrechner.<br>
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
            <div class="frage"><span class="nr">V1</span><span class="txt">Eine Schachtel ist \(4\) cm lang, \(3\) cm breit und \(12\) cm hoch. Wie lang ist ein Stab, der genau von einer unteren Ecke zur gegenüberliegenden oberen Ecke passt?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>Bodendiagonale \(\sqrt{16 + 9} = 5\) cm, dann \(\sqrt{25 + 144} = 13\) cm. Zweimal Pythagoras, zweimal ein Hilfsdreieck.</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V2</span><span class="txt">Ein Quadrat liegt so in einem Kreis mit Radius \(5\) cm, dass alle vier Ecken auf dem Kreis liegen. Wie gross ist die Fläche des Quadrats?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>Die Diagonale ist ein Durchmesser, \(10\) cm. Für die Seite \(a\): \(a^2 + a^2 = 100\), also \(a^2 = 50\). Die Fläche ist \(a^2 = 50\) cm², ohne dass du \(a\) kennen musst.</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V3</span><span class="txt">Auf Karopapier (Kästchen \(1\) cm) verbindest du zwei Gitterpunkte, die \(5\) Kästchen nach rechts und \(12\) nach oben auseinander liegen. Wie lang ist die Strecke? Findest du zwei Gitterpunkte mit genau \(25\) cm Abstand, die nicht auf einer Gitterlinie liegen?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\(\sqrt{25 + 144} = 13\) cm. Für \(25\) cm: \(7\) und \(24\) Kästchen (\(49 + 576 = 625\)) oder \(15\) und \(20\).</p></div></details>
          </li>
        </ol>
      </div>
      <p class="ausf weiter">Weiter: Dreiecke und Pythagoras bei Mathe begreifbar: ''' + V_DREI + r'''.</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Flächen, Pythagoras und Ähnlichkeit, Version 1.0 (10.10.2026). Gebaut aus scripts/lp/pythagoras/seite.py —
     Änderungen dort, nicht in dieser Datei. Grundlagen: HOWTO-leitprogramme.md (Kapitelmuster) und
     ~/TODO-BM-Vorkurs-LP03-15.md, Abschnitt 6 (LP 08, Ebene Geometrie: Flächen, Pythagoras, Ähnlichkeit), für die Sek I umgesetzt.

     Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026): Das Leitprogramm ist selbst die fachliche Quelle;
     Vertiefung bei Mathe begreifbar. Ohne Taschenrechner: alle Wurzeln gehen auf (pythagoreische Tripel).
     Notation: Grundseite g, Höhe h, Katheten a, b, Hypotenuse c, Radius r, Sehne s, Abstand d, Streckfaktor k, Dezimalpunkt.

     Kompetenzen — eigene Formulierung, ohne Lehrplan-Nummern (CLAUDE.md: keine erfundenen Lehrplan-Stellen):
       K1  Flächen von Dreieck, Parallelogramm und Trapez mit Grundseite und Höhe; zusammengesetzte Figuren zerlegen oder ergänzen
       K2  Satz des Pythagoras: Hypotenuse und Katheten erkennen, fehlende Seite berechnen, Rechtwinkligkeit prüfen
       K3  Hilfsdreieck finden (Diagonale, Höhe, Leiter, Sehne im Kreis, Wasser im Rohr) und Pythagoras anwenden
       K4  Ähnliche Figuren: Streckfaktor, fehlende Längen, Verhältnisse; Längenfaktor k gegen Flächenfaktor k²

     Kompetenzmatrix (Kompetenz | Kapitel | Simulation | Übungen | Kapitelaufgaben | Gesamttest):
       K1 | 1 | Sim 1 Grundseite, Höhe | flaeche, zusammen       | 1a–1f | G1, G2
       K2 | 2 | Sim 2 Quadrate          | hypotenuse, kathete     | 2a–2f | G3, G4
       K3 | 3 | Sim 3 Sehne im Kreis    | hilfsdreieck, sehne     | 3a–3f | G5, G6
       K4 | 4 | Sim 4 Streckfaktor      | aehnlich, flaechenfaktor| 4a–4f | G7, G8

     Planung (Kapitel | Lernziel | Erkundung | Beispiel | Häufiger Fehler | min):
       0 | Vorwissen     | –                 | –                               | –                                 | 10
       1 | Flächen       | Spitze verschieben| Dreieck 6/4, Haus, L-Form       | schräge Seite statt Höhe; halbieren| 40
       2 | Pythagoras    | Quadrate          | 3-4-5, 6-8-10, Kathete 10/6     | Kathete addiert; Seiten statt Quadrate| 40
       3 | Hilfsdreieck  | Sehne verschieben | Rechteck 20×21, 16/17, Rohr     | ganze statt halbe Strecke         | 40
       4 | Ähnlichkeit   | k einstellen      | 3-4-5 × 2, Schatten, Regal      | Flächenfaktor = Längenfaktor      | 40
       Gesamttest (PDF) 30 · Summe 200 min ≈ 4.4 Lektionen. Vertiefung V1–V3 freiwillig, nicht eingerechnet.

     Aus der Vorlage umgesetzt: Grundseite und Höhe, Zerlegen (Kapitel 1, G1, G2), Pythagoras mit «Hilfsdreieck zuerst finden»
     (Kapitel 2 und 3, schrittweise im Clip eingeblendet), Kreisgrundlagen Radius, Durchmesser, Sehne mit Wasserspiegel im Rohr
     (Kapitel 3, G6), ähnliche Dreiecke, Verhältnisse, k gegen k² und Regal mit Differenzfläche (Kapitel 4, G7, G8).
     Fehlermodule «Höhe ≠ schräge Seite» (Kapitel 1, Übung flaeche) und «Flächenfaktor ≠ Längenfaktor» (Kapitel 4, Übung flaechenfaktor).
     Bewusst nicht übernommen: Teams-Ablauf, Lehrpersonenteil, Prüfungsnummern, Kreissektoren (kommen später).

     Clips: je Kapitel ein Einführungsclip (mit einer Vorhersagefrage) und ein Kontrollclip mit fünf Fragen,
     Reihe «Geometrie», pyt-lp-*.json, erzeugt mit scripts/lp/pythagoras/clips.py.

     Farben: Figur und Grundseite blau, Höhe, Abstand und Bildfigur orange, Hypotenuse, Radius und Ergebnis grün, Fehler rot; Bereichsfarbe Petrol.
     Gesamttest und Bewertungspaket nur als PDF (downloads/leitprogramme/pythagoras/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Sek1-Mathe begreifbar · Leitprogramm</p>
      <h1>Flächen, Pythagoras und Ähnlichkeit</h1>
      <p class="unter">Flächen mit Grundseite und Höhe, Satz des Pythagoras, Hilfsdreiecke im Kreis und ähnliche Figuren. Vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
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
      <li><a href="#k1"><span class="nr">1</span><span>Flächen</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Pythagoras</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Hilfsdreieck</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Ähnlichkeit</span></a></li>
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
          <li>Zum Schluss der <b>Gesamttest</b> auf Papier, mit Lineal. Alles ohne Taschenrechner: Die Wurzeln gehen auf.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">Das kannst du danach, alles <span class="ohm">ohne Taschenrechner</span>:</p>
        <ul>
          <li><b>K1</b> Flächen von Dreieck, Parallelogramm und Trapez mit Grundseite und Höhe berechnen und zusammengesetzte Figuren zerlegen oder ergänzen (Kapitel 1)</li>
          <li><b>K2</b> im rechtwinkligen Dreieck mit dem Satz des Pythagoras eine fehlende Seite berechnen und prüfen, ob ein Dreieck rechtwinklig ist (Kapitel 2)</li>
          <li><b>K3</b> in Figuren und im Kreis das rechtwinklige Hilfsdreieck finden und damit Diagonalen, Höhen und Sehnen berechnen (Kapitel 3)</li>
          <li><b>K4</b> ähnliche Figuren erkennen, fehlende Längen mit dem Streckfaktor berechnen und den Flächenfaktor \\(k^2\\) anwenden (Kapitel 4)</li>
        </ul>
        <p class="rlp-quelle">Baut auf Rechteck, Quadratzahlen und Verhältnissen auf (Vorwissen) und auf dem Leitprogramm «Bruchterme, Gleichungen und Formeln». Nicht in diesem Leitprogramm: Kreisumfang, Kreissektoren, Trigonometrie. Zum Vertiefen bei Mathe begreifbar: ''' + V_DREI + '''.</p>
      </details>

    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Flächen, Pythagoras und Ähnlichkeit · Sek1-Mathe begreifbar</span>
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
<script>buildNav({{ bereich: 'lp', id: 'lp-pythagoras' }});</script>
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
