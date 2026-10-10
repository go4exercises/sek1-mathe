"""Baut leitprogramme/funktionstypen.html aus einer Kapitelbeschreibung (10.10.2026).

  python3 scripts/lp/funktionstypen/seite.py

Leitprogramm Funktionstypen und Graphen (Bereich Funktionen), Gerüst aus scripts/lp/darstellungen/.
Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026); vertieft wird auf den Themenseiten von
Mathe begreifbar (TALS). Alles kommt aus diesem Ordner: kopf.css, seite.css, basis.js (Thema, Fortschritt,
Schiene), seite.js (Koordinatensystem, Simulationen, Übungen mit Zahlen und Klickgitter). Nur der SEO-Block wird aus der bestehenden Seite
übernommen — ihn schreibt scripts/build-seo.py. Wiederholbar. Danach Pre-Flight und build-seo.py.
"""
import json
import os

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/funktionstypen.html'
NAME = 'Funktionstypen und Graphen'
STAND = 'Stand 10. Oktober 2026'
CLIP = 'typ-lp-'

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
V_TYPEN = tals('grundlagen/g3-1-grundlagen.html', 'Grundlagen zu Funktionen')
V_GRAPH = tals('grundlagen/g3-1-grundlagen.html', 'Darstellungen von Funktionen', '#darstellungen')


def bild(geraden='', punkte='', label='Gerade im Koordinatensystem'):
    return f'\n            <div class="mini-reihe"><svg class="mini-gerade" data-geraden="{geraden}" data-punkte="{punkte}" aria-label="{label}"></svg></div>'


# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1" aria-label="Graphen-Familien: Familie und Parameter einstellen">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Zielgraph gestrichelt und eigener Graph"></svg>
        <div class="sl-row">
          <label class="sim-schalter" for="s1-fam">Familie
            <select id="s1-fam" class="sim-wahl"><option value="g" selected>Gerade y = a · x + b</option><option value="q">Parabel y = a · x² + b</option><option value="w">Wurzelgraph y = a · √x + b</option><option value="k">Kehrwertgraph y = a / x + b</option></select></label>
        </div>
        <div class="sl-row">
          {regler('s1-a', 'a', 'blau', -4, 4, 1).replace('step="1"', 'step="0.5"')}
          {regler('s1-b', 'b', 'orange', -4, 4, 0)}
        </div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Vier Graphen-Familien</div>
          <table class="wt vergleich">
            <tr><th>Gleichung</th><th>Graph</th><th>Merkmal</th><th>\(x = 4\)</th></tr>
            <tr><td>\(y = x\)</td><td>Gerade</td><td>gleich viel mehr bei jedem Schritt</td><td>\(4\)</td></tr>
            <tr><td>\(y = x^2\)</td><td>Parabel</td><td>symmetrisch zur \(y\)-Achse, Scheitel \((0 \mid 0)\), wird immer steiler</td><td>\(16\)</td></tr>
            <tr><td>\(y = \sqrt{x}\)</td><td>Wurzelgraph</td><td>beginnt bei \((0 \mid 0)\), nur \(x \ge 0\), wird immer flacher</td><td>\(2\)</td></tr>
            <tr><td>\(y = \dfrac{1}{x}\)</td><td>Kehrwertgraph</td><td>zwei Äste, trifft keine Achse, \(x \neq 0\)</td><td>\(\tfrac{1}{4}\)</td></tr>
          </table>
          <p>Die Merkmale gelten für die Grundform ohne \(+ b\). Mit einer Zahl \(a\) davor wird der Graph gestreckt (\(a = 2\): doppelt so hoch), mit \(a \lt 0\) an der \(x\)-Achse gespiegelt. Ein \(+ b\) schiebt ihn um \(b\) nach oben, bei \(b \lt 0\) nach unten. Dann trifft zum Beispiel auch ein Kehrwertgraph eine Achse.</p>
          <p><b>Zuordnen mit Testpunkten:</b> Setz gut ablesbare \(x\)-Werte ein, zum Beispiel \(x = 0\), \(1\), \(4\) und einen negativen Wert.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Zu wenige Punkte:</b> \(y = x\) und \(y = x^2\) gehen beide durch \((0 \mid 0)\) und \((1 \mid 1)\). Ein dritter Punkt trennt sie, zum Beispiel \(x = 2\): \(2\) gegen \(4\).</p>
          <p><b>Wurzel und Kehrwert überall:</b> \(\sqrt{-4}\) gibt es nicht, und \(\dfrac{1}{0}\) auch nicht. Dort hat der Graph keinen Punkt.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 14, [
    ('1a', 3, r'Berechne für \(x = 9\): \(y = 2x\), \(y = x^2\), \(y = \sqrt{x}\), \(y = \dfrac{18}{x}\). Welche Gleichung gehört zu einer Parabel, welche zu einem Kehrwertgraphen?',
     r'<p>\(18\), \(81\), \(3\), \(2\). Parabel: \(y = x^2\). Kehrwertgraph: \(y = \dfrac{18}{x}\).</p>', ''),
    ('1b', 3, r'Fülle die Wertetabelle von \(y = 0.5x^2\) für \(x = -4, -2, 0, 2, 4\) und zeichne den Graphen. Was fällt dir auf?',
     r'<p>\(8,\ 2,\ 0,\ 2,\ 8\). Eine Parabel, symmetrisch zur \(y\)-Achse, Scheitel \((0 \mid 0)\), flacher als \(y = x^2\).</p>',
     '\n            <div class="mini-reihe"><svg class="leer-gitter" aria-label="leeres Koordinatensystem zum Zeichnen"></svg></div>'),
    ('1c', 2, r'Ein Graph geht durch \((1 \mid 3)\) und \((3 \mid 1)\) und trifft keine Achse. Welche Gleichung passt: \(y = -x + 4\), \(y = \dfrac{3}{x}\) oder \(y = 3x^2\)?',
     r'<p>\(y = \dfrac{3}{x}\): \(\tfrac{3}{1} = 3\), \(\tfrac{3}{3} = 1\), und ein Kehrwertgraph trifft keine Achse. \(y = -x + 4\) geht zwar durch beide Punkte, trifft aber die Achsen.</p>', ''),
    ('1d', 2, r'Fülle die Wertetabelle von \(y = \dfrac{6}{x}\) für \(x = 1, 2, 3, 6\) und skizziere den Graphen für \(x \gt 0\).',
     r'<p>\(6,\ 3,\ 2,\ 1\). Eine fallende Kurve, die sich den Achsen nähert, sie aber nie trifft: ein Ast eines Kehrwertgraphen.</p>',
     '\n            <div class="mini-reihe"><svg class="leer-gitter" aria-label="leeres Koordinatensystem zum Zeichnen"></svg></div>'),
    ('1e', 2, r'Für welche \(x\) hat \(y = 2\sqrt{x}\) keinen Punkt, für welche \(y = \dfrac{5}{x}\)? Begründe.',
     r'<p>\(y = 2\sqrt{x}\): für alle negativen \(x\), denn Quadrate sind nie negativ. \(y = \dfrac{5}{x}\): nur für \(x = 0\), denn durch null kann man nicht teilen.</p>', ''),
    ('1f', 2, r'Wie sieht der Graph von \(y = -0.5x^2\) aus? Berechne zwei Punkte und vergleiche mit \(y = x^2\).',
     r'<p>Eine nach unten offene Parabel mit Scheitel \((0 \mid 0)\): \((2 \mid -2)\), \((-2 \mid -2)\). Gespiegelt an der \(x\)-Achse und flacher als \(y = x^2\).</p>', ''),
])
k1 = kapitel(1, 'familien', 'Vier Graphen-Familien', 40,
             r'Du erkennst Gerade, Parabel, Wurzel- und Kehrwertgraph an ihrer Form und ordnest Gleichungen mit Testpunkten zu.',
             (CLIP + 'familien', 'Vier Graphen-Familien'), sim1,
             (CLIP + 'kontrolle-familien', 'Kontrollfragen zu den Familien'), fest1,
             [uebung('zuordnen', 'Welche Gleichung?'), uebung('werte', 'Werte berechnen')],
             auf1, V_TYPEN, komp='K1')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2" aria-label="Proportional, antiproportional oder linear mit Anfangswert">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Graph des Zusammenhangs mit Doppelt-Test"></svg>
        <div class="sl-row">
          <label class="sim-schalter" for="s2-typ">Typ
            <select id="s2-typ" class="sim-wahl"><option value="lin" selected>y = k · x + b</option><option value="anti">y = k / x</option></select></label>
        </div>
        <div class="sl-row">
          {regler('s2-k', 'k', 'blau', 0.5, 24, 1).replace('step="1"', 'step="0.5"')}
          {regler('s2-b', 'b', 'orange', 0, 10, 0)}
        </div>
        <div class="sl-row">
          {regler('s2-x', 'Doppelt-Test bei x', 'gruen', 1, 5, 1)}
        </div>
      </figure>'''
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Drei Zusammenhänge unterscheiden</div>
          <table class="wt vergleich">
            <tr><th></th><th>propor&shy;tional</th><th>linear mit Anfangswert</th><th>anti&shy;proportional</th></tr>
            <tr><th>Gleichung</th><td>\(y = k \cdot x\)</td><td>\(y = k \cdot x + b\), \(b \neq 0\)</td><td>\(y = \dfrac{k}{x}\)</td></tr>
            <tr><th>Graph</th><td>Gerade durch \((0 \mid 0)\)</td><td>Gerade, nicht durch \((0 \mid 0)\)</td><td>Kehrwertgraph</td></tr>
            <tr><th>Tabelle</th><td>\(y : x\) gleich</td><td>bei gleichen Schritten gleiche Differenzen</td><td>\(x \cdot y\) gleich</td></tr>
            <tr><th>\(x\) doppelt</th><td>\(y\) überall doppelt</td><td>\(y\) nicht überall doppelt oder halb</td><td>\(y\) überall halb</td></tr>
          </table>
          <p>Benzin \(1.80\) Fr. pro Liter: \(y = 1.8x\), proportional. Taxi \(6\) Fr. und \(2.50\) Fr. pro km: \(y = 2.5x + 6\), linear mit Anfangswert. \(36\) Fr. Pizza auf \(x\) Personen: \(y = \dfrac{36}{x}\), antiproportional.</p>
          <p><b>So prüfst du:</b> zuerst die Form (Gerade durch \((0 \mid 0)\), andere Gerade oder Kehrwertgraph), dann den Doppelt-Test an mehreren Stellen. \(k\) ist der Faktor; bei einer Geraden ist er die Steigung \(m\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>«Steigt, also proportional»:</b> Das Taxi wird teurer, je weiter du fährst, aber \(2\) km kosten \(11\) Fr. und \(4\) km \(16\) Fr., nicht \(22\) Fr. Der Anfangswert verhindert das Verdoppeln.</p>
          <p><b>«Fällt, also antiproportional»:</b> Eine fallende Gerade ist linear. Bei \(y = -x + 6\) wird \(y\) von \(x = 2\) zu \(x = 4\) zufällig halb so gross (\(4\) und \(2\)), von \(x = 1\) zu \(x = 2\) aber nicht (\(5\) und \(4\)). Antiproportional heisst: Das Produkt bleibt überall gleich.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 14, [
    ('2a', 3, r'Welcher Zusammenhang? (a) Äpfel zu \(4.50\) Fr. pro kg. (b) Velomiete \(10\) Fr. und \(3\) Fr. pro Stunde. (c) \(48\) Bonbons gleichmässig auf \(x\) Kinder verteilt. (d) Die Lufttemperatur ist am Boden \(20\) °C und sinkt pro \(100\) m Höhe um \(0.6\) °C.',
     r'<p>(a) proportional, \(y = 4.5x\). (b) linear mit Anfangswert, \(y = 3x + 10\). (c) antiproportional, \(y = \dfrac{48}{x}\). (d) linear mit Anfangswert, fallend: \(20\) °C bei \(0\) m, in \(1000\) m Höhe \(14\) °C.</p>', ''),
    ('2b', 2, r'Ordne zu: A \(x\): \(1, 2, 3\), \(y\): \(5, 10, 15\). B \(y\): \(7, 9, 11\). C \(y\): \(30, 15, 10\) (jeweils dieselben \(x\)).',
     r'<p>A proportional (\(y : x = 5\)). B linear mit Anfangswert (\(+2\) pro Schritt, \(y = 2x + 5\)). C antiproportional (\(x \cdot y = 30\)).</p>', ''),
    ('2c', 3, r'\(5\) Arbeiter brauchen für einen Auftrag \(12\) Tage. Wie lange brauchen \(6\) Arbeiter, wie lange \(3\) Arbeiter, wenn alle gleich schnell arbeiten?',
     r'<p>Antiproportional: \(5 \cdot 12 = 60\) Arbeitstage. \(6\) Arbeiter: \(10\) Tage. \(3\) Arbeiter: \(20\) Tage.</p>', ''),
    ('2d', 2, r'Ben sagt: «Bei \(y = 3x + 4\) ist \(y\) bei \(x = 4\) doppelt so gross wie bei \(x = 2\).» Prüfe.',
     r'<p>\(x = 2\): \(y = 10\). \(x = 4\): \(y = 16\), nicht \(20\). Wegen des Anfangswerts \(4\) verdoppelt sich \(y\) nicht.</p>', ''),
    ('2e', 2, r'Ein Graph geht durch \((4 \mid 10)\). Gib die Gleichung an, wenn der Zusammenhang (a) proportional, (b) antiproportional ist.',
     r'<p>(a) \(k = 10 : 4 = 2.5\), \(y = 2.5x\). (b) \(k = 4 \cdot 10 = 40\), \(y = \dfrac{40}{x}\).</p>', ''),
    ('2f', 2, r'Warum geht der Graph eines proportionalen Zusammenhangs wie «Preis für \(x\) kg Äpfel» immer durch \((0 \mid 0)\)?',
     r'<p>Für \(x = 0\) ist \(y = k \cdot 0 = 0\): Für null Kilogramm zahlst du nichts. Ein Anfangswert würde den Graphen nach oben schieben.</p>', ''),
])
k2 = kapitel(2, 'zusammenhaenge', 'Proportional, antiproportional, linear', 40,
             r'Du unterscheidest proportionale, antiproportionale und lineare Zusammenhänge mit Anfangswert an Text, Tabelle, Gleichung und Graph.',
             (CLIP + 'zusammenhaenge', 'Proportional, antiproportional, linear'), sim2,
             (CLIP + 'kontrolle-zusammenhaenge', 'Kontrollfragen zu den Zusammenhängen'), fest2,
             [uebung('situation', 'Welcher Zusammenhang?'), uebung('neuwert', 'Neuer Wert')],
             auf2, V_TYPEN, komp='K2')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3" aria-label="Weg-Zeit-Graph aus drei Abschnitten">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Weg-Zeit-Graph mit Zielgraph"></svg>
        <div class="sl-row">
          {regler('s3-v1', 'v₁ (0 bis 10 min)', 'blau', -100, 150, 50).replace('step="1"', 'step="10"')}
          {regler('s3-v2', 'v₂ (10 bis 20 min)', 'blau', -100, 150, 50).replace('step="1"', 'step="10"')}
          {regler('s3-v3', 'v₃ (20 bis 30 min)', 'blau', -100, 150, 50).replace('step="1"', 'step="10"')}
        </div>
      </figure>'''
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Weg-Zeit-Graphen lesen</div>
          <p>Anna geht \(10\) min zur Ampel (\(800\) m), wartet \(5\) min und rennt dann \(5\) min bis zur Schule (\(1400\) m). \(s\): Entfernung von zu Hause, \(t\): Zeit.</p>
          <ol class="weg">
            <li>\(0\) bis \(10\) min: \(v = \dfrac{800 - 0}{10} = 80\) m/min <span class="warum">Steigung = Geschwindigkeit</span></li>
            <li>\(10\) bis \(15\) min: waagrecht, \(v = 0\) <span class="warum">Pause, der Ort bleibt gleich</span></li>
            <li>\(15\) bis \(20\) min: \(v = \dfrac{1400 - 800}{5} = 120\) m/min <span class="warum">steiler = schneller</span></li>
          </ol>
          <p>Ein <b>Knick</b> heisst: Das Tempo ändert sich. <b>Fallend</b> heisst: Die Entfernung vom Start wird kleiner, es geht zurück. <b>Senkrecht</b> ist unmöglich: Weg ohne Zeit gibt es nicht.</p>
          <p>In der Simulation heisst eine negative Geschwindigkeit: zurück. \(-80\) m/min sind \(80\) m/min in Richtung zu Hause, der Graph fällt.</p>
          <p>Umrechnen: \(120\) m/min sind \(120 \cdot 60 = 7200\) m pro Stunde, also \(7.2\) km/h. Umgekehrt: \(6\) km/h sind \(6000\) m in \(60\) min, also \(100\) m/min.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Graph als Landschaft gelesen:</b> Steigt der Graph, heisst das nicht, dass es bergauf geht. Er zeigt die Entfernung, nicht die Höhe.</p>
          <p><b>Stand statt Steigung:</b> Bei \(t = 20\) ist \(s = 1400\) m. Die Geschwindigkeit ist aber \(\dfrac{\Delta s}{\Delta t}\) im Abschnitt, hier \(120\) m/min.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 14, [
    ('3a', 3, r'Ein Weg-Zeit-Graph verbindet die Punkte \((0 \mid 0)\), \((4 \mid 600)\), \((10 \mid 600)\), \((14 \mid 1400)\) (\(t\) in min, \(s\) in m). Berechne die Geschwindigkeit in jedem Abschnitt und beschreibe die Bewegung.',
     r'<p>\(\dfrac{600}{4} = 150\) m/min, dann \(0\) (Pause, \(6\) min), dann \(\dfrac{800}{4} = 200\) m/min. Zügig los, warten, am Schluss noch schneller.</p>', ''),
    ('3b', 2, r'Skizziere den Graphen der Entfernung von zu Hause: \(10\) min mit \(50\) m/min, \(5\) min Pause, \(5\) min mit \(100\) m/min zurück zum Start.',
     r'<p>Von \((0 \mid 0)\) bis \((10 \mid 500)\), waagrecht bis \((15 \mid 500)\), dann fallend bis \((20 \mid 0)\).</p>', ''),
    ('3c', 2, r'Zwei Velofahrer starten gleichzeitig. Im Weg-Zeit-Graphen ist der von Mia steiler als der von Tom. Was heisst das?',
     r'<p>Mia fährt schneller: Sie legt in derselben Zeit mehr Weg zurück.</p>', ''),
    ('3d', 2, r'Kai sagt zu einem steigenden Weg-Zeit-Graphen: «Hier geht es bergauf.» Was ist falsch?',
     r'<p>Der Graph zeigt die Entfernung über der Zeit, nicht die Höhe des Weges. Steigend heisst: Die Entfernung wird grösser, egal ob es bergauf oder bergab geht.</p>', ''),
    ('3e', 2, r'Rechne um: \(90\) m/min in km/h und \(12\) km/h in m/min.',
     r'<p>\(90 \cdot 60 = 5400\) m/h \(= 5.4\) km/h. \(12\) km/h \(= 12\,000\) m in \(60\) min \(= 200\) m/min.</p>', ''),
    ('3f', 3, r'Tim fährt \(6\) min mit \(200\) m/min von zu Hause weg, macht \(4\) min Pause und fährt dann mit \(100\) m/min zurück. Skizziere den Graphen der Entfernung von zu Hause. Wann ist er wieder zu Hause? Woran siehst du im Graphen, dass er zurück langsamer fährt?',
     r'<p>Von \((0 \mid 0)\) bis \((6 \mid 1200)\), waagrecht bis \((10 \mid 1200)\), fallend bis \((22 \mid 0)\): \(1200 : 100 = 12\) min zurück, also nach \(22\) min zu Hause. Das fallende Stück ist flacher als das steigende.</p>', ''),
])
k3 = kapitel(3, 'wegzeit', 'Weg-Zeit-Graphen lesen', 40,
             r'Du liest aus einem Weg-Zeit-Graphen Geschwindigkeiten, Pausen und Rückwege ab und wählst zu einer Beschreibung den passenden Graphen.',
             (CLIP + 'wegzeit', 'Weg-Zeit-Graphen lesen'), sim3,
             (CLIP + 'kontrolle-wegzeit', 'Kontrollfragen zu Weg-Zeit-Graphen'), fest3,
             [uebung('tempo', 'Geschwindigkeit ablesen'), uebung('beschreibung', 'Welche Beschreibung passt?')],
             auf3, V_TYPEN, komp='K3')

# ------------------------------------------------------------------ Kapitel 4
sim4 = f'''      <figure class="sim sim-gross" id="sim4" aria-label="Zurückgelegter Weg und noch verbleibende Entfernung">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="zwei Graphen: zurückgelegt steigt, noch entfernt fällt"></svg>
        <div class="sl-row">
          {regler('s4-L', 'Strecke', 'orange', 6, 36, 10).replace('step="1"', 'step="2"')}
          {regler('s4-v', 'Tempo', 'blau', 2, 20, 5)}
        </div>
        <div class="sl-row">
          {regler('s4-t', 'Zeit t', 'gruen', 0, 3, 0).replace('step="1"', 'step="0.25"')}
        </div>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Zurückgelegt oder noch entfernt</div>
          <p>Velotour, \(24\) km mit \(16\) km/h:</p>
          <ul class="kurz">
            <li><b>zurückgelegt:</b> \(s = 16t\), steigt, proportional</li>
            <li><b>noch entfernt:</b> \(d = 24 - 16t\), fällt, linear mit Anfangswert \(24\)</li>
            <li>beide zusammen immer \(24\) km; gleich gross bei der Hälfte: \(16t = 12\), \(t = 0.75\) h</li>
            <li>beide Graphen enden bei der Ankunft, \(t = 24 : 16 = 1.5\) h</li>
          </ul>
          <p><b>Ein Bewegungsdiagramm prüfen:</b> Was steht an der \(y\)-Achse? Der zurückgelegte Weg kann nur wachsen oder gleich bleiben. Eine Entfernung (von zu Hause, zum Ziel) darf auch kleiner werden. Kein Stück ist senkrecht, keines läuft nach links.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Zurückgelegt und Entfernung verwechselt:</b> Auf dem Heimweg wächst der zurückgelegte Weg weiter, die Entfernung von zu Hause wird kleiner.</p>
          <p><b>Fallend heisst nicht langsamer:</b> Fällt die Entfernung <b>von zu Hause</b>, fährst du zurück. Fällt die Entfernung <b>zum Ziel</b>, kommst du näher. Langsamer heisst in beiden Fällen: flacher.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 14, [
    ('4a', 3, r'Eine Velotour ist \(36\) km lang, du fährst \(12\) km/h. Schreib den zurückgelegten Weg und die Entfernung zum Ziel als Gleichung. Wie gross sind beide nach \(2\) h?',
     r'<p>\(s = 12t\), \(d = 36 - 12t\). Nach \(2\) h: \(24\) km gefahren, noch \(12\) km.</p>', ''),
    ('4b', 2, r'Welcher der beiden Graphen aus 4a fällt, welcher ist proportional? Wo schneiden sie sich?',
     r'<p>\(d\) fällt, \(s\) ist proportional. Sie schneiden sich bei der Hälfte: \(12t = 18\), \(t = 1.5\) h, beide \(18\) km.</p>', ''),
    ('4c', 2, r'Wann bist du in 4a noch \(6\) km vom Ziel entfernt?',
     r'<p>\(36 - 12t = 6\), \(12t = 30\), \(t = 2.5\) h.</p>', ''),
    ('4d', 2, r'Ein Graph zeigt die Entfernung zum Ziel einer Wanderung: Er fällt gleichmässig von \(15\) km auf \(0\) km in \(5\) h. Jonas sagt: «Fallend heisst, die Wanderer gehen zurück.» Stimmt das? Wie schnell gehen sie?',
     r'<p>Nein. Die Entfernung <b>zum Ziel</b> wird kleiner, weil sie vorwärts gehen. Tempo: \(15 : 5 = 3\) km/h.</p>', ''),
    ('4e', 3, r'Lea zeichnet den zurückgelegten Weg einer Wanderung. In einem Abschnitt fällt ihr Graph, in einem anderen ist er senkrecht. Was ist an beiden Stellen falsch?',
     r'<p>Der zurückgelegte Weg kann nicht kleiner werden, auch auf dem Rückweg nicht: Fallen ist unmöglich. Senkrecht hiesse Weg ohne Zeit: ebenfalls unmöglich.</p>', ''),
    ('4f', 2, r'Von einer \(40\) km langen Velotour hast du nach \(1.5\) h gleichmässig \(27\) km zurückgelegt. Wie weit ist das Ziel noch, und wie schnell fährst du?',
     r'<p>\(40 - 27 = 13\) km, denn zurückgelegt und noch entfernt ergeben zusammen die ganze Strecke. Tempo: \(27 : 1.5 = 18\) km/h.</p>', ''),
])
k4 = kapitel(4, 'rest', 'Zurückgelegt oder noch entfernt', 40,
             r'Du unterscheidest den zurückgelegten Weg von der noch verbleibenden Entfernung, beschreibst beide als Gleichung und Graph und kritisierst fehlerhafte Bewegungsdiagramme.',
             (CLIP + 'rest', 'Zurückgelegt oder noch entfernt'), sim4,
             (CLIP + 'kontrolle-rest', 'Kontrollfragen: zurückgelegt oder entfernt'), fest4,
             [uebung('restweg', 'Gefahren und noch vor dir'), uebung('kritik', 'Diagramm prüfen')],
             auf4, V_TYPEN, komp='K4')

# ------------------------------------------------------------------ Vorwissen
k0 = f'''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-th">Vorwissen</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Quadrieren, Wurzeln, Brüche mit \\(x\\) im Nenner, Steigung, Geschwindigkeit. Zuerst kurz wiederholen, dann der Vortest.</p>
''' + r'''      <details class="anleitung">
        <summary><h3>Kurz wiederholt</h3></summary>
        <ul class="kurz">
          <li><b>Quadrat:</b> \(3^2 = 9\) und \((-3)^2 = 9\): Ein Quadrat ist nie negativ.</li>
          <li><b>Wurzel:</b> \(\sqrt{16} = 4\), weil \(4^2 = 16\). Aus negativen Zahlen gibt es keine Wurzel.</li>
          <li><b>Lineare Funktion:</b> \(y = m \cdot x + b\), Steigung \(m = \dfrac{\Delta y}{\Delta x}\) (Leitprogramm <a href="lineare-funktionen.html">Lineare Funktionen</a>).</li>
          <li><b>Antiproportional:</b> \(x \cdot y\) bleibt gleich (Leitprogramm <a href="darstellungen.html">Darstellungen wechseln</a>).</li>
          <li><b>Geschwindigkeit:</b> Weg durch Zeit: \(30\) km in \(2\) h sind \(15\) km/h.</li>
        </ul>
      </details>
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Berechne \(3^2\), \((-3)^2\) und \(0.5^2\).', r'<p>\(9\), \(9\), \(0.25\).</p>', ''),
    ('0b', 2, r'Berechne \(\sqrt{16}\) und \(\sqrt{49}\).', r'<p>\(4\) und \(7\).</p>', ''),
    ('0c', 2, r'Berechne \(\dfrac{12}{x}\) für \(x = 3\) und für \(x = 0.5\).', r'<p>\(4\) und \(24\).</p>', ''),
    ('0d', 2, r'Welche Steigung hat die Gerade durch \((0 \mid 2)\) und \((2 \mid 8)\)?', r'<p>\(m = \dfrac{8 - 2}{2 - 0} = 3\).</p>', ''),
    ('0e', 2, r'Ein Velo fährt \(30\) km in \(2\) Stunden. Wie schnell im Durchschnitt?', r'<p>\(15\) km/h.</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: «Kurz wiederholt» nochmals lesen und die Lösungen nachrechnen.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest (nur PDF)
PDF = '../downloads/leitprogramme/funktionstypen/'
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
            <tr><td>17 – 21 P</td><td>Den schwächsten Teil nochmals, gemessen am Anteil (Teil A 7, B 6, C 6, D 6 P): Tüfteln und Übungen des Kapitels dieses Teils.</td></tr>
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
            <div class="frage"><span class="nr">V1</span><span class="txt">Wo schneiden sich die Graphen von \(y = x^2\) und \(y = \sqrt{x}\)? Probiere mit einer Tabelle.</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>Bei \((0 \mid 0)\) und \((1 \mid 1)\). Dazwischen liegt \(\sqrt{x}\) oben (\(x = 0.25\): \(0.5\) gegen \(0.0625\)), danach \(x^2\).</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V2</span><span class="txt">Ein Auto fährt \(1\) h mit \(60\) km/h und \(1\) h mit \(100\) km/h. Zeichne den Weg-Zeit-Graphen. Wie gross ist die Durchschnittsgeschwindigkeit?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>Von \((0 \mid 0)\) über \((1 \mid 60)\) nach \((2 \mid 160)\). Durchschnitt: \(160 : 2 = 80\) km/h, die Steigung der Verbindung von Anfang und Ende.</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V3</span><span class="txt">Für welches \(x\) ist \(\dfrac{1}{x}\) grösser als \(100\)?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>Für \(0 \lt x \lt 0.01\): Je näher \(x\) bei \(0\) liegt, desto grösser wird \(\dfrac{1}{x}\). Der Graph schmiegt sich an die \(y\)-Achse.</p></div></details>
          </li>
        </ol>
      </div>
      <p class="ausf weiter">Weiter: Funktionen und ihre Graphen bei Mathe begreifbar: ''' + V_GRAPH + r'''.</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Funktionstypen und Graphen, Version 1.0 (10.10.2026). Gebaut aus scripts/lp/funktionstypen/seite.py —
     Änderungen dort, nicht in dieser Datei. Grundlagen: HOWTO-leitprogramme.md (Kapitelmuster) und
     ~/TODO-BM-Vorkurs-LP03-15.md, Abschnitt 4 (LP 06, Funktionstypen und Graphen interpretieren), für die Sek I umgesetzt.

     Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026): Das Leitprogramm ist selbst die fachliche Quelle;
     Vertiefung bei Mathe begreifbar. Baut auf den Leitprogrammen Lineare Funktionen und Darstellungen wechseln auf.
     Notation: y = a · x², y = a · √x, y = a / x, Punkte (x | y), Weg s in m oder km, Zeit t in min oder h, Dezimalpunkt.

     Kompetenzen — eigene Formulierung, ohne Lehrplan-Nummern (CLAUDE.md: keine erfundenen Lehrplan-Stellen):
       K1  Gerade, Parabel, Wurzel- und Kehrwertgraph unterscheiden, Gleichungen mit Testpunkten zuordnen
       K2  Proportional, antiproportional und linear mit Anfangswert unterscheiden (Text, Tabelle, Gleichung, Graph)
       K3  Weg-Zeit-Graphen lesen: Geschwindigkeit als Steigung, Pause, Knick, Rückweg; Graph zu einer Beschreibung wählen
       K4  Zurückgelegten Weg und verbleibende Entfernung unterscheiden; fehlerhafte Bewegungsdiagramme kritisieren

     Kompetenzmatrix (Kompetenz | Kapitel | Simulation | Übungen | Kapitelaufgaben | Gesamttest):
       K1 | 1 | Sim 1 Familien        | zuordnen, werte        | 1a–1f | G1, G2
       K2 | 2 | Sim 2 Doppelt-Test    | situation, neuwert     | 2a–2f | G3, G4
       K3 | 3 | Sim 3 drei Abschnitte | tempo, beschreibung    | 3a–3f | G5, G6
       K4 | 4 | Sim 4 Weg und Rest    | restweg, kritik        | 4a–4f | G7, G8

     Planung (Kapitel | Lernziel | Erkundung | Beispiel | Häufiger Fehler | min):
       0 | Vorwissen        | –                 | –                           | –                                     | 10
       1 | Familien         | Familie einstellen| y = x, x², √x, 1/x; x = 4   | zu wenige Punkte; √ und 1/x überall   | 40
       2 | Zusammenhänge    | Doppelt-Test      | Benzin, Taxi, Pizza         | «steigt, also prop»; «fällt, also anti»| 40
       3 | Weg-Zeit         | drei Abschnitte   | Anna 80, Pause, 120 m/min   | Landschaft gelesen; Stand statt Tempo | 40
       4 | Weg und Rest     | Weg und Rest      | Velo 24 km mit 16 km/h      | zurückgelegt/Entfernung; fallend=lang.| 40
       Gesamttest (PDF) 30 · Summe 200 min ≈ 4.4 Lektionen. Vertiefung V1–V3 freiwillig, nicht eingerechnet.

     Aus der Vorlage umgesetzt: vier Familien qualitativ und mit Testpunkten (Kapitel 1, G1, G2), proportional,
     antiproportional, linear mit Anfangswert (Kapitel 2, G3, G4), Steigung und Knicke in Weg-Zeit-Graphen und Graph zu
     einer Beschreibung (Kapitel 3, G5, G6), zurückgelegte Strecke gegen verbleibende Entfernung und fehlerhaftes
     Bewegungsdiagramm kritisieren (Kapitel 4, G7, G8). Achsen überall mit Grösse und Einheit, Bilder mit Textalternative.
     Bewusst nicht übernommen: Teams-Ablauf, Lehrpersonenteil, Prüfungsnummern.

     Clips: je Kapitel ein Einführungsclip (mit einer Vorhersagefrage) und ein Kontrollclip mit fünf Fragen,
     Reihe «Funktionen sehen», typ-lp-*.json, erzeugt mit scripts/lp/funktionstypen/clips.py.

     Farben: eigener Graph und zurückgelegter Weg blau, Anfangswert und Rest orange, Treffer grün, Fehler rot; Bereichsfarbe Petrol.
     Gesamttest und Bewertungspaket nur als PDF (downloads/leitprogramme/funktionstypen/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Sek1-Mathe begreifbar · Leitprogramm</p>
      <h1>Funktionstypen und Graphen</h1>
      <p class="unter">Gerade, Parabel, Wurzel und Kehrwert, Zusammenhänge und Weg-Zeit-Graphen. Vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
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
      <li><a href="#k1"><span class="nr">1</span><span>Familien</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Zusammenhänge</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Weg-Zeit</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Weg und Rest</span></a></li>
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
          <li>Zum Schluss der <b>Gesamttest</b> auf Papier, mit Lineal. Alles ohne Taschenrechner.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">Das kannst du danach, alles <span class="ohm">ohne Taschenrechner</span>:</p>
        <ul>
          <li><b>K1</b> Gerade, Parabel, Wurzel- und Kehrwertgraph an der Form erkennen und Gleichungen mit Testpunkten zuordnen (Kapitel 1)</li>
          <li><b>K2</b> proportionale, antiproportionale und lineare Zusammenhänge mit Anfangswert unterscheiden (Kapitel 2)</li>
          <li><b>K3</b> aus Weg-Zeit-Graphen Geschwindigkeit, Pausen und Rückwege ablesen und zu einer Beschreibung den passenden Graphen wählen (Kapitel 3)</li>
          <li><b>K4</b> zurückgelegten Weg und verbleibende Entfernung unterscheiden und fehlerhafte Bewegungsdiagramme begründet kritisieren (Kapitel 4)</li>
        </ul>
        <p class="rlp-quelle">Baut auf den Leitprogrammen «Lineare Funktionen» und «Darstellungen wechseln» auf. Nicht in diesem Leitprogramm: Scheitelform der Parabel, Potenzfunktionen allgemein. Zum Vertiefen bei Mathe begreifbar: ''' + V_TYPEN + '''.</p>
      </details>

    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Funktionstypen und Graphen · Sek1-Mathe begreifbar</span>
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
<script>buildNav({{ bereich: 'lp', id: 'lp-funktionstypen' }});</script>
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
