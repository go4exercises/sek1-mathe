"""Baut leitprogramme/gleichungen-formeln.html aus einer Kapitelbeschreibung (10.10.2026).

  python3 scripts/lp/gleichungen-formeln/seite.py

Leitprogramm Bruchterme, Gleichungen und Formeln (Bereich Gleichungen), Gerüst aus scripts/lp/terme-faktorisieren/.
Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026); vertieft wird auf den Themenseiten von
Mathe begreifbar (TALS). Alles kommt aus diesem Ordner: kopf.css, seite.css, basis.js (Thema, Fortschritt,
Schiene), seite.js (Simulationen, Übungen mit Term-, Formel- und Lösungsmengen-Eingabe). Nur SEO-Block und Footer werden aus der bestehenden Seite
übernommen — beide schreibt scripts/build-seo.py. Wiederholbar. Danach Pre-Flight und build-seo.py.
"""
import json
import os

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/gleichungen-formeln.html'
NAME = 'Bruchterme, Gleichungen und Formeln'
CLIP = 'gleich-lp-'

SEO_AUF = '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->'
SEO_ZU = '<!-- SEO:ENDE -->'
FUSS_AUF = '<!-- FUSS:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->'
FUSS_ZU = '<!-- FUSS:ENDE -->'
# Den Footer schreibt scripts/build-seo.py (seit 10.10.2026, eine Version für das ganze Lehrmittel);
# SEO-Kopf und Footer werden aus der bestehenden Seite übernommen, neu gebaut nur leere Marken.
seo = SEO_AUF + '\n' + SEO_ZU
fussblock = FUSS_AUF + '\n' + FUSS_ZU
if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
    if SEO_AUF in alt:
        seo = alt[alt.index(SEO_AUF):alt.index(SEO_ZU) + len(SEO_ZU)]
    if FUSS_AUF in alt:
        fussblock = alt[alt.index(FUSS_AUF):alt.index(FUSS_ZU) + len(FUSS_ZU)]

# Vertiefung: Themenseiten von Mathe begreifbar (Berufsmaturität), in neuem Tab
TALS = 'https://mathe.begreifbar.ch/grundlagen/'
def tals(seite, text, anker=''):
    return f'<a href="{TALS}{seite}{anker}" target="_blank" rel="noopener">{text} ↗</a>'
V_BRT = tals('g1-3-algebraische-terme.html', 'Bruchterme', '#bruchterme')
V_AEQ = tals('g2-1-grundlagen.html', 'Äquivalenzumformungen', '#aequivalenz')
V_LIN = tals('g2-2a-lineare-gleichungen.html', 'Lineare Gleichungen', '#verfahren')
V_FAELLE = tals('g2-2a-lineare-gleichungen.html', 'Drei Lösungsfälle', '#spezialfaelle')
V_PROBE = tals('g2-1-grundlagen.html', 'Lösen und Probe', '#loesen-probe')
V_SACH = tals('g2-1-grundlagen.html', 'Sachverhalte als Gleichung', '#formulieren')


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



# ------------------------------------------------------------------ Kapitel 1
sim1 = '''      <figure class="sim sim-gross" id="sim1" aria-label="Faktoren kürzen: gleiche Faktoren oben und unten streichen">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-mitte"><div class="kuerz-feld" role="group" aria-label="Zähler und Nenner als Faktoren"></div></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <div class="sim-mitte"><button type="button" class="kuerz-fertig">nichts mehr zu kürzen</button></div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Bruchterme kürzen</div>
          <p>Ein <b>Bruchterm</b> hat eine Variable im Nenner. Der Nenner darf nie \(0\) werden: Bei \(\dfrac{5}{x - 3}\) ist \(x = 3\) nicht erlaubt.</p>
          <p><b>Kürzen</b> heisst wie bei Zahlenbrüchen: Zähler und Nenner durch denselben <b>Faktor</b> teilen. Darum zuerst Zähler und Nenner in Faktoren zerlegen (ausklammern, binomische Formel, Zweiklammersatz), dann gleiche Faktoren streichen.</p>
          <ol class="weg">
            <li>\(\dfrac{x^2 - 9}{2x + 6} = \dfrac{(x - 3)(x + 3)}{2(x + 3)}\) <span class="warum">Zähler: binomische Formel; Nenner: \(2\) ausklammern</span></li>
            <li>\(= \dfrac{x - 3}{2}\) <span class="warum">\((x + 3)\) gestrichen; \(x \neq -3\)</span></li>
          </ol>
          <p>Weitere Beispiele: \(\dfrac{6x}{9x^2} = \dfrac{3x \cdot 2}{3x \cdot 3x} = \dfrac{2}{3x}\) für \(x \neq 0\), und \(\dfrac{x^2 + 4x + 4}{x^2 - 4} = \dfrac{(x + 2)^2}{(x + 2)(x - 2)} = \dfrac{x + 2}{x - 2}\) für \(x \neq 2\) und \(x \neq -2\). Die Bedingungen kommen aus dem <b>ursprünglichen</b> Nenner: \(x = -2\) bleibt verboten, auch wenn der Faktor \(x + 2\) gestrichen ist.</p>
          <p><b>Gegenzahlen:</b> \(3 - x = -(x - 3)\). Darum ist \(\dfrac{x - 3}{3 - x} = -1\) für \(x \neq 3\).</p>
          <p><b>Ist das ein Faktor?</b> Steht unten \(x + 1\), dann müsste der Zähler für \(x = -1\) null sein. Bei \(\dfrac{x^2 + 1}{x + 1}\) gibt der Zähler für \(x = -1\) aber \(2\): Der Bruch lässt sich nicht kürzen.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Summanden kürzen:</b> \(\dfrac{x + 3}{x + 5}\) ist nicht \(\dfrac{3}{5}\). Probe mit \(x = 1\): \(\dfrac{4}{6} = \dfrac{2}{3}\), aber \(\dfrac{3}{5}\) ist kleiner. Das \(x\) ist hier ein Summand, kein Faktor. Der Bruch lässt sich nicht kürzen.</p>
          <p><b>Nicht zuerst zerlegt:</b> Bei \(\dfrac{x^2 - 9}{2x + 6}\) sieht man den gemeinsamen Faktor erst nach dem Faktorisieren.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 14, [
    ('1a', 2, r'Kürze: \(\dfrac{12a^2}{18a}\)',
     r'<p>\(\dfrac{6a \cdot 2a}{6a \cdot 3} = \dfrac{2a}{3}\), für \(a \neq 0\).</p>', ''),
    ('1b', 3, r'Kürze: \(\dfrac{5x - 10}{x - 2}\) und \(\dfrac{x^2 - 16}{x + 4}\)',
     r'<p>\(\dfrac{5(x - 2)}{x - 2} = 5\) (\(x \neq 2\)). \(\dfrac{(x - 4)(x + 4)}{x + 4} = x - 4\) (\(x \neq -4\)).</p>', ''),
    ('1c', 3, r'Kürze: \(\dfrac{x^2 - 6x + 9}{x^2 - 9}\)',
     r'<p>\(\dfrac{(x - 3)^2}{(x - 3)(x + 3)} = \dfrac{x - 3}{x + 3}\), für \(x \neq 3\) und \(x \neq -3\).</p>', ''),
    ('1d', 2, r'Nina kürzt: \(\dfrac{x + 6}{x + 2} = \dfrac{6}{2} = 3\). Zeige mit \(x = 1\), dass das nicht stimmt. Was ist falsch?',
     r'<p>Mit \(x = 1\): \(\dfrac{7}{3}\), nicht \(3\). Nina hat Summanden gekürzt. Zähler und Nenner haben keinen gemeinsamen Faktor; der Bruch lässt sich nicht kürzen.</p>', ''),
    ('1e', 2, r'Für welche Zahlen ist \(\dfrac{x + 1}{x^2 - 4x}\) nicht definiert?',
     r'<p>\(x^2 - 4x = x(x - 4)\) ist \(0\) für \(x = 0\) und für \(x = 4\). Diese beiden Zahlen sind nicht erlaubt.</p>', ''),
    ('1f', 2, r'Warum ist \(\dfrac{2 - x}{x - 2} = -1\) für \(x \neq 2\)? Erkläre und prüfe mit \(x = 5\).',
     r'<p>\(2 - x = -(x - 2)\): Zähler und Nenner sind Gegenzahlen, ihr Quotient ist \(-1\). Mit \(x = 5\): \(\dfrac{-3}{3} = -1\).</p>', ''),
])
k1 = kapitel(1, 'kuerzen', 'Bruchterme kürzen', 40,
             r'Du kürzt Bruchterme, indem du Zähler und Nenner zuerst in Faktoren zerlegst, und gibst an, welche Zahlen die Variable nicht annehmen darf.',
             (CLIP + 'kuerzen', 'Bruchterme kürzen'), sim1,
             (CLIP + 'kontrolle-kuerzen', 'Kontrollfragen zum Kürzen'), fest1,
             [uebung('kuerzen', 'Kürzen'), uebung('ausschluss', 'Nicht erlaubte Zahlen')],
             auf1, V_BRT, komp='K1')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2" aria-label="Hauptnenner aus Bausteinen bauen">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <table class="hn-tab" aria-label="Erweitern auf den gewählten Nenner"></table>
        <div class="sl-row">
          {regler('s2-k', 'Zahl', 'orange', 1, 12, 1)}
          {regler('s2-e', 'Hochzahl von x', 'orange', 0, 3, 0)}
        </div>
        <div class="sim-schalter reihe"><label><input type="checkbox" id="s2-p"> Faktor \\(x + 1\\)</label><label><input type="checkbox" id="s2-q"> Faktor \\(x - 1\\)</label></div>
      </figure>'''
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Rechnen mit Bruchtermen</div>
          <p>Es gelten dieselben Regeln wie bei Zahlenbrüchen.</p>
          <p><b>Multiplizieren:</b> Zähler mal Zähler, Nenner mal Nenner, vorher kürzen: \(\dfrac{3x}{4} \cdot \dfrac{8}{9x^2} = \dfrac{3x \cdot 8}{4 \cdot 9x^2} = \dfrac{2}{3x}\).</p>
          <p><b>Dividieren:</b> mit dem Kehrwert multiplizieren: \(\dfrac{5}{x} : \dfrac{10}{x^2} = \dfrac{5}{x} \cdot \dfrac{x^2}{10} = \dfrac{x}{2}\).</p>
          <p><b>Addieren und Subtrahieren:</b> zuerst gleichnamig machen. Der <b>Hauptnenner</b> enthält jeden Faktor der Nenner so oft, wie er höchstens vorkommt.</p>
          <ol class="weg">
            <li>\(\dfrac{5}{x} + \dfrac{2}{x} = \dfrac{7}{x}\) <span class="warum">gleiche Nenner: Zähler addieren</span></li>
            <li>\(\dfrac{1}{x} + \dfrac{1}{2x} = \dfrac{2}{2x} + \dfrac{1}{2x} = \dfrac{3}{2x}\) <span class="warum">Hauptnenner \(2x\)</span></li>
            <li>\(\dfrac{2}{x} - \dfrac{1}{x + 1} = \dfrac{2(x + 1) - x}{x(x + 1)} = \dfrac{x + 2}{x(x + 1)}\) <span class="warum">Hauptnenner \(x(x + 1)\), Zähler in Klammern</span></li>
          </ol>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Nenner addieren:</b> \(\dfrac{1}{x} + \dfrac{1}{2}\) ist nicht \(\dfrac{2}{x + 2}\). Probe mit \(x = 2\): links \(1\), rechts \(\dfrac{1}{2}\). Richtig: \(\dfrac{2 + x}{2x}\).</p>
          <p><b>Minus vor dem Bruchstrich:</b> Der ganze Zähler wird abgezogen. \(1 - \dfrac{x - 1}{x} = \dfrac{x - (x - 1)}{x} = \dfrac{1}{x}\), nicht \(\dfrac{x - x - 1}{x}\).</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 14, [
    ('2a', 3, r'Multipliziere und kürze: \(\dfrac{2x}{3} \cdot \dfrac{9}{4x^2}\). Dividiere: \(\dfrac{6}{x} : \dfrac{3}{x^2}\)',
     r'<p>\(\dfrac{2x \cdot 9}{3 \cdot 4x^2} = \dfrac{18x}{12x^2} = \dfrac{3}{2x}\). Mit dem Kehrwert: \(\dfrac{6}{x} \cdot \dfrac{x^2}{3} = \dfrac{6x^2}{3x} = 2x\) (\(x \neq 0\)).</p>', ''),
    ('2b', 2, r'Multipliziere und kürze: \(\dfrac{x^2 - 1}{x} \cdot \dfrac{3x}{x + 1}\)',
     r'<p>\(\dfrac{(x - 1)(x + 1) \cdot 3x}{x \cdot (x + 1)} = 3(x - 1)\), für \(x \neq 0\) und \(x \neq -1\).</p>', ''),
    ('2c', 2, r'Addiere: \(\dfrac{3}{2a} + \dfrac{5}{6a}\)',
     r'<p>Hauptnenner \(6a\): \(\dfrac{9}{6a} + \dfrac{5}{6a} = \dfrac{14}{6a} = \dfrac{7}{3a}\).</p>', ''),
    ('2d', 3, r'Subtrahiere: \(\dfrac{4}{x} - \dfrac{3}{x + 2}\)',
     r'<p>Hauptnenner \(x(x + 2)\): \(\dfrac{4(x + 2) - 3x}{x(x + 2)} = \dfrac{x + 8}{x(x + 2)}\).</p>', ''),
    ('2e', 2, r'Tim rechnet \(\dfrac{1}{x} + \dfrac{1}{3} = \dfrac{2}{x + 3}\). Prüfe mit \(x = 3\) und rechne richtig.',
     r'<p>Mit \(x = 3\): links \(\dfrac{1}{3} + \dfrac{1}{3} = \dfrac{2}{3}\), Tims Ergebnis \(\dfrac{2}{6} = \dfrac{1}{3}\). Tim hat die Nenner addiert. Richtig: \(\dfrac{3}{3x} + \dfrac{x}{3x} = \dfrac{3 + x}{3x}\).</p>', ''),
    ('2f', 2, r'Warum braucht es beim Multiplizieren keinen gemeinsamen Nenner, beim Addieren aber schon?',
     r'<p>Beim Multiplizieren nimmt man einen Teil von einem Teil: Zähler mal Zähler, Nenner mal Nenner, das geht immer. Addieren kann man nur gleich grosse Teile; gleich gross sind sie erst mit demselben Nenner.</p>', ''),
])
k2 = kapitel(2, 'rechnen', 'Rechnen mit Bruchtermen', 45,
             r'Du multiplizierst und dividierst Bruchterme, addierst und subtrahierst sie mit dem Hauptnenner und gibst das Ergebnis gekürzt auf einem Bruchstrich an.',
             (CLIP + 'rechnen', 'Rechnen mit Bruchtermen'), sim2,
             (CLIP + 'kontrolle-rechnen', 'Kontrollfragen zum Rechnen mit Bruchtermen'), fest2,
             [uebung('malbruch', 'Mal und durch'), uebung('plusbruch', 'Plus und minus')],
             auf2, V_BRT, komp='K2')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3" aria-label="Gleichung umformen: auf beiden Seiten dasselbe tun">
        <div class="leiste" aria-live="polite"></div>
        <div class="gl-verlauf" aria-live="polite"></div>
        <div class="sl-row">
          {regler('s3-k', 'beide Seiten + k·x', 'blau', -6, 6, 0)}
          {regler('s3-m', 'beide Seiten + Zahl', 'orange', -15, 15, 0)}
        </div>
        <label class="sim-schalter">beide Seiten teilen durch <select class="sim-wahl" aria-label="teilen durch">
          <option value="1" selected>1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option>
          <option value="-1">−1</option><option value="-2">−2</option><option value="-3">−3</option><option value="-4">−4</option><option value="-5">−5</option><option value="-6">−6</option>
        </select></label>
      </figure>'''
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Lineare Gleichungen lösen</div>
          <p>Eine Gleichung ist wie eine Waage im Gleichgewicht. Sie bleibt im Gleichgewicht, wenn du auf <b>beiden Seiten dasselbe</b> tust: dieselbe Zahl oder dasselbe Vielfache von \(x\) addieren oder subtrahieren, mit derselben Zahl (nicht 0) multiplizieren oder durch sie dividieren.</p>
          <ol class="weg">
            <li>\(5x - 7 = 2x + 8\) <span class="warum">\(-2x\) auf beiden Seiten</span></li>
            <li>\(3x - 7 = 8\) <span class="warum">\(+7\)</span></li>
            <li>\(3x = 15\) <span class="warum">\(: 3\)</span></li>
            <li>\(x = 5\), also \(L = \{5\}\) <span class="warum">Probe: \(5 \cdot 5 - 7 = 18\) und \(2 \cdot 5 + 8 = 18\)</span></li>
          </ol>
          <p><b>Klammern</b> zuerst auflösen, jede Seite zusammenfassen. <b>Brüche</b> wegschaffen: beide Seiten mit dem Hauptnenner multiplizieren, jeder Zähler in Klammern:</p>
          <p>\[ \frac{x + 1}{3} - \frac{x - 2}{4} = 1 \quad | \cdot 12 \qquad 4(x + 1) - 3(x - 2) = 12 \qquad x + 10 = 12 \qquad x = 2 \]</p>
          <p><b>Drei Ausgänge:</b> genau eine Lösung; keine Lösung, wenn eine falsche Aussage übrig bleibt (\(2(x + 1) = 2x + 5\) gibt \(2 = 5\), \(L = \{\,\}\)); alle Zahlen, wenn eine wahre Aussage übrig bleibt (\(3(x - 2) - (x + 4) = 2x - 10\) gibt \(-10 = -10\), \(L = \mathbb{Q}\)).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Nur eine Seite umgeformt:</b> Wer bei \(5x - 7 = 2x + 8\) nur links \(+7\) rechnet, zerstört das Gleichgewicht.</p>
          <p><b>Minus vor dem Bruch:</b> \(-\dfrac{x - 2}{4} \cdot 12 = -3(x - 2) = -3x + 6\), nicht \(-3x - 6\).</p>
          <p><b>Ohne Probe:</b> Setz die Lösung in die ursprüngliche Gleichung ein. Beide Seiten müssen gleich sein.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 14, [
    ('3a', 2, r'Löse und mach die Probe: \(8x - 5 = 3x + 20\)',
     r'<p>\(5x = 25\), \(x = 5\), \(L = \{5\}\). Probe: \(40 - 5 = 35\) und \(15 + 20 = 35\).</p>', ''),
    ('3b', 2, r'Löse: \(4(x - 3) = 2(x + 1)\)',
     r'<p>\(4x - 12 = 2x + 2\), \(2x = 14\), \(x = 7\), \(L = \{7\}\).</p>', ''),
    ('3c', 2, r'Löse: \(\dfrac{x}{2} + \dfrac{x}{3} = 10\)',
     r'<p>Mal \(6\): \(3x + 2x = 60\), \(5x = 60\), \(x = 12\), \(L = \{12\}\).</p>', ''),
    ('3d', 3, r'Löse: \(\dfrac{2x - 1}{5} = \dfrac{x + 4}{3}\)',
     r'<p>Mal \(15\): \(3(2x - 1) = 5(x + 4)\), \(6x - 3 = 5x + 20\), \(x = 23\), \(L = \{23\}\). Probe: \(\dfrac{45}{5} = 9\) und \(\dfrac{27}{3} = 9\).</p>', ''),
    ('3e', 3, r'Lea löst \(5 - (x + 2) = 2x\) so: \(5 - x + 2 = 2x\), also \(7 = 3x\). Finde den Fehler und löse richtig.',
     r'<p>Das Minus vor der Klammer gilt für beide Glieder: \(5 - x - 2 = 2x\), also \(3 = 3x\), \(x = 1\), \(L = \{1\}\). Probe: \(5 - 3 = 2\) und \(2 \cdot 1 = 2\).</p>', ''),
    ('3f', 2, r'Gib die Lösungsmengen an und begründe: \(2(x + 3) = 2x + 6\) und \(2(x + 3) = 2x + 3\)',
     r'<p>Links steht beide Male \(2x + 6\). Die erste Gleichung wird zu \(6 = 6\), wahr für jedes \(x\): \(L = \mathbb{Q}\). Die zweite wird zu \(6 = 3\), nie wahr: \(L = \{\,\}\).</p>', ''),
])
k3 = kapitel(3, 'gleichungen', 'Lineare Gleichungen lösen', 45,
             r'Du löst lineare Gleichungen mit der Variablen auf beiden Seiten, mit Klammern und mit Brüchen, gibst die Lösungsmenge an und prüfst durch Einsetzen.',
             (CLIP + 'gleichungen', 'Lineare Gleichungen lösen'), sim3,
             (CLIP + 'kontrolle-gleichungen', 'Kontrollfragen zu Gleichungen'), fest3,
             [uebung('gleichung', 'Gleichungen'), uebung('bruchgleichung', 'Gleichungen mit Brüchen')],
             auf3, V_LIN + ' · ' + V_FAELLE, komp='K3')

# ------------------------------------------------------------------ Kapitel 4
sim4 = '''      <figure class="sim sim-gross" id="sim4" aria-label="Formel umstellen: die Rechenkette rückwärts gehen">
        <div class="leiste" aria-live="polite"></div>
        <div class="kette kette-vor" aria-live="polite"></div>
        <div class="kette kette-rueck" aria-live="polite"></div>
        <div class="kette-knoepfe" role="group" aria-label="Umkehrungen"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Formeln umstellen</div>
          <p>Eine Formel ist eine Gleichung mit mehreren Grössen. <b>Umstellen</b> heisst: sie nach der gesuchten Grösse auflösen, mit denselben Umformungen wie bei Gleichungen. Was mit der gesuchten Grösse <b>zuletzt</b> gerechnet wird, machst du <b>zuerst</b> rückgängig.</p>
          <p>\[ v = \frac{s}{t} \quad | \cdot t \qquad s = v \cdot t \quad | : v \qquad t = \frac{s}{v} \]</p>
          <ol class="weg">
            <li>\(F = 1.8 \cdot C + 32\) <span class="warum">zuletzt wird \(+32\) gerechnet</span></li>
            <li>\(F - 32 = 1.8 \cdot C\) <span class="warum">\(-32\) auf beiden Seiten</span></li>
            <li>\(C = \dfrac{F - 32}{1.8}\) <span class="warum">\(: 1.8\); Probe: \(F = 212\) gibt \(C = 100\)</span></li>
          </ol>
          <p>Trapez: \(A = \dfrac{a + c}{2} \cdot h\) gibt \(h = \dfrac{2A}{a + c}\). Geteilt wird durch die ganze Summe \(a + c\); auf einer Zeile geschrieben braucht sie Klammern: \(h = 2A : (a + c)\).</p>
          <p><b>Einsetzen</b> erst nach dem Umstellen, mit passenden Einheiten: \(s\) in km und \(v\) in km/h gibt \(t\) in h.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Nur durch einen Teil geteilt:</b> \(h = \dfrac{2A}{a} + c\) ist falsch, richtig ist \(h = \dfrac{2A}{a + c}\).</p>
          <p><b>Umkehrung verwechselt:</b> Aus \(s = v \cdot t\) folgt \(t = \dfrac{s}{v}\), nicht \(t = \dfrac{v}{s}\). Probe mit Zahlen: \(s = 120\), \(v = 60\) gibt \(t = 2\).</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 15, [
    ('4a', 2, r'Stelle \(P = U \cdot I\) nach \(I\) um.',
     r'<p>\(I = \dfrac{P}{U}\).</p>', ''),
    ('4b', 2, r'Dreieck: Stelle \(A = \dfrac{g \cdot h}{2}\) nach \(h\) um.',
     r'<p>Mal \(2\): \(2A = g \cdot h\); durch \(g\): \(h = \dfrac{2A}{g}\).</p>', ''),
    ('4c', 3, r'Taxi: \(P = 6 + 2.5 \cdot s\) (\(P\) in Fr., \(s\) in km). Stelle nach \(s\) um. Wie weit kommt man für \(31\) Fr.?',
     r'<p>\(P - 6 = 2.5 \cdot s\), also \(s = \dfrac{P - 6}{2.5}\). Mit \(P = 31\): \(s = \dfrac{25}{2.5} = 10\) km.</p>', ''),
    ('4d', 3, r'Rechteck: \(u = 2(l + b)\). Stelle nach \(b\) um und berechne \(b\) für \(u = 24\) cm und \(l = 7\) cm.',
     r'<p>Durch \(2\): \(\dfrac{u}{2} = l + b\), dann \(-l\): \(b = \dfrac{u}{2} - l\). Mit Zahlen: \(b = 12 - 7 = 5\) cm.</p>', ''),
    ('4e', 3, r'Max stellt \(V = a \cdot b \cdot h\) nach \(h\) um und schreibt \(h = V - a \cdot b\). Prüfe mit \(a = 3\), \(b = 4\), \(h = 5\) und stelle richtig um.',
     r'<p>Mit diesen Zahlen ist \(V = 60\). Max erhält \(60 - 12 = 48\), nicht \(5\). Rückgängig gemacht wird ein «mal», also durch: \(h = \dfrac{V}{a \cdot b}\), Probe \(\dfrac{60}{12} = 5\).</p>', ''),
    ('4f', 2, r'Eine Kerze ist \(20\) cm lang und brennt pro Stunde \(0.5\) cm ab: \(L = 20 - 0.5 \cdot t\) (\(L\) in cm, \(t\) in h). Stelle nach \(t\) um. Nach wie vielen Stunden ist sie noch \(12\) cm lang?',
     r'<p>\(L - 20 = -0.5 \cdot t\), also \(t = \dfrac{20 - L}{0.5} = 2(20 - L)\). Mit \(L = 12\): \(t = 16\) h. Probe: \(20 - 0.5 \cdot 16 = 12\).</p>', ''),
])
k4 = kapitel(4, 'formeln', 'Formeln umstellen', 40,
             r'Du stellst Formeln nach einer gesuchten Grösse um, rechnest dabei rückwärts in der richtigen Reihenfolge und setzt erst danach Zahlen ein.',
             (CLIP + 'formeln', 'Formeln umstellen'), sim4,
             (CLIP + 'kontrolle-formeln', 'Kontrollfragen zu Formeln'), fest4,
             [uebung('umstellen', 'Umstellen'), uebung('formelwert', 'Umstellen und berechnen')],
             auf4, V_AEQ + ' · ' + V_SACH, komp='K4')

# ------------------------------------------------------------------ Vorwissen
k0 = f'''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-th">Vorwissen</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Faktorisieren, Zahlenbrüche kürzen, Gleichungen mit einem Schritt, Einsetzen. Zuerst kurz wiederholen, dann der Vortest.</p>
''' + r'''      <details class="anleitung">
        <summary><h3>Kurz wiederholt</h3></summary>
        <ul class="kurz">
          <li><b>Faktorisieren:</b> gemeinsamen Faktor ausklammern, \(6x + 9 = 3(2x + 3)\); binomische Formeln rückwärts, \(x^2 - 1 = (x - 1)(x + 1)\); Zweiklammersatz, \(x^2 + 2x - 15 = (x + 5)(x - 3)\): zwei Zahlen mit Produkt \(-15\) und Summe \(2\).</li>
          <li><b>Brüche kürzen:</b> Zähler und Nenner durch dieselbe Zahl teilen, \(\dfrac{10}{15} = \dfrac{2}{3}\).</li>
          <li><b>Gleichung umformen:</b> auf beiden Seiten dasselbe tun. \(x + 4 = 9\) gibt mit \(-4\): \(x = 5\).</li>
          <li><b>Einsetzen:</b> Für \(a = 2\) ist \(3a - 1 = 5\).</li>
        </ul>
      </details>
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Faktorisiere: \(4x - 12\) und \(x^2 - x - 12\)',
     r'<p>\(4(x - 3)\) und \((x - 4)(x + 3)\), denn \(-4 \cdot 3 = -12\) und \(-4 + 3 = -1\).</p><p class="komm">Faktorisieren braucht Kapitel 1 und 2.</p>', ''),
    ('0b', 2, r'Kürze: \(\dfrac{18}{24}\) und \(\dfrac{3 \cdot 5}{5 \cdot 7}\)',
     r'<p>\(\dfrac{3}{4}\) und \(\dfrac{3}{7}\).</p>', ''),
    ('0c', 2, r'Für welche Zahl \(x\) wird der Nenner von \(\dfrac{5}{x - 4}\) gleich \(0\)?',
     r'<p>Für \(x = 4\).</p>', ''),
    ('0d', 2, r'Löse: \(3x + 5 = 20\)',
     r'<p>\(3x = 15\), \(x = 5\).</p>', ''),
    ('0e', 2, r'Setze \(a = 3\) und \(b = -4\) ein: \(2a - b\)',
     r'<p>\(6 - (-4) = 10\).</p><p class="komm">Einsetzen ist die Probe in Kapitel 3 und 4.</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: «Kurz wiederholt» nochmals lesen, die Lösungen des Vortests nachrechnen; fürs Faktorisieren hilft das Leitprogramm «Terme und Faktorisieren».</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/gleichungen-formeln/'
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
            <tr><td>17 – 21 P</td><td>Den schwächsten Teil nochmals, gemessen am Anteil (Teil A 9, B 8, C 8 P): Tüfteln und Übungen der Kapitel dieses Teils.</td></tr>
            <tr><td>11 – 16 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 10 P</td><td>Zurück zu den Kapiteln jedes Teils, in dem du weniger als die Hälfte erreicht hast; sind es alle drei, zum Vortest und zu Kapitel 1.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1, G3 → 1; G2 → 2; G4 bis G6 → 3; G7 bis G9 → 4</p>
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
            <div class="frage"><span class="nr">V1</span><span class="txt">Zeige: \(\dfrac{1}{x} - \dfrac{1}{x + 1} = \dfrac{1}{x(x + 1)}\). Berechne damit \(\dfrac{1}{1 \cdot 2} + \dfrac{1}{2 \cdot 3} + \dots + \dfrac{1}{9 \cdot 10}\).</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\(\dfrac{(x + 1) - x}{x(x + 1)} = \dfrac{1}{x(x + 1)}\). Jeder Summand ist eine Differenz: \(\left(1 - \tfrac{1}{2}\right) + \left(\tfrac{1}{2} - \tfrac{1}{3}\right) + \dots + \left(\tfrac{1}{9} - \tfrac{1}{10}\right) = 1 - \tfrac{1}{10} = \tfrac{9}{10}\).</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V2</span><span class="txt">Für welche Zahl \(a\) hat \(ax + 3 = 2x + 7\) keine Lösung? Was passiert für alle anderen \(a\)?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\((a - 2)x = 4\). Für \(a = 2\) steht \(0 = 4\): keine Lösung. Sonst gibt es genau eine: \(x = \dfrac{4}{a - 2}\).</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V3</span><span class="txt">Der Durchschnitt dreier Noten ist \(m = \dfrac{a + b + c}{3}\). Stelle nach \(c\) um. Welche dritte Note braucht es nach \(4.5\) und \(5\) für den Schnitt \(5\)?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\(c = 3m - a - b = 15 - 4.5 - 5 = 5.5\).</p></div></details>
          </li>
        </ol>
      </div>
      <p class="ausf weiter">Weiter: Gleichungen mit Parametern und Ungleichungen stehen bei Mathe begreifbar unter ''' + V_LIN + ''' und ''' + V_FAELLE + r'''.</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Bruchterme, Gleichungen und Formeln, Version 1.0 (10.10.2026). Gebaut aus scripts/lp/gleichungen-formeln/seite.py —
     Änderungen dort, nicht in dieser Datei. Grundlagen: HOWTO-leitprogramme.md (Kapitelmuster) und
     ~/TODO-BM-Vorkurs-LP03-15.md, Abschnitt 1 (LP 03), für die Sek I umgesetzt.

     Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026): Das Leitprogramm ist selbst die fachliche Quelle;
     Vertiefungslinks zeigen auf Mathe begreifbar (TALS). Notation nach STYLEGUIDE.md und CLAUDE.md: Dezimalpunkt,
     Lösungsmenge L = {…}, leere Menge \\{\\,\\}, alle Zahlen \\mathbb{Q}, «nicht erlaubt: x ≠ …» statt Definitionsmenge.

     Kompetenzen — eigene Formulierung, ohne Lehrplan-Nummern (CLAUDE.md: keine erfundenen Lehrplan-Stellen):
       K1  Bruchterme kürzen (nur Faktoren, zuerst zerlegen), nicht erlaubte Zahlen angeben
       K2  Bruchterme multiplizieren, dividieren, addieren und subtrahieren (Hauptnenner)
       K3  Lineare Gleichungen lösen (Variable beidseitig, Klammern, Brüche), Lösungsmenge, Probe
       K4  Formeln nach einer Grösse umstellen, danach Werte mit Einheiten einsetzen
     Alles ohne Taschenrechner.

     Kompetenzmatrix (Kompetenz | Kapitel | Simulation | Übungen | Kapitelaufgaben | Gesamttest):
       K1 | 1 | Sim 1 | kuerzen, ausschluss          | 1a–1f | G1, G3
       K2 | 2 | Sim 2 | malbruch, plusbruch          | 2a–2f | G2
       K3 | 3 | Sim 3 | gleichung, bruchgleichung    | 3a–3f | G4–G6
       K4 | 4 | Sim 4 | umstellen, formelwert        | 4a–4f | G7–G9

     Planung (Kapitel | Lernziel | Erkundung | Beispiel | Häufiger Fehler | min):
       0 | Vorwissen     | –                       | –                          | –                              | 10
       1 | kürzen        | Faktoren streichen      | (x² − 9)/(2x + 6)          | Summanden gekürzt              | 40
       2 | rechnen       | Hauptnenner bauen       | 2/x − 1/(x + 1)            | Nenner addiert                 | 45
       3 | Gleichungen   | Waage: beidseitig       | 5x − 7 = 2x + 8, Brüche    | nur eine Seite; Minus vor Bruch| 45
       4 | Formeln       | Rechenkette rückwärts   | F = 1.8C + 32, Trapez      | nur durch einen Teil geteilt   | 40
       Gesamttest (PDF) 30 · Summe 210 min ≈ 4.7 Lektionen. Vertiefung V1–V3 freiwillig, nicht eingerechnet.

     Aus der Vorlage übernommen: Fehlermodul «Kürzen von Summanden» (Festhalten, Clip, Übung mit Diagnose), Antwortprüfung
     mit gleichwertigen Termen und nicht erlaubten Zahlen, Vortest mit einer Gleichung und einer Kürzungsaufgabe,
     Selbstcheck (Gesamttest) mit Bruchterm, Gleichung und Formel; Treppenmodell (Schrittmassregel) als Prüfungsanker.
     Bewusst nicht übernommen: Teams-Ablauf, Lehrpersonenteil, Prüfungsnummern.

     Clips: je Kapitel ein Einführungsclip (mit einer Vorhersagefrage) und ein Kontrollclip mit fünf Fragen,
     Reihe «Gleichungen sehen», gleich-lp-*.json, erzeugt mit scripts/lp/gleichungen-formeln/clips.py.

     Farben: Zähler blau, Nenner orange, Gekürztes und Ergebnis grün, Fehler rot; Bereichsfarbe Petrol.
     Gesamttest und Bewertungspaket nur als PDF (downloads/leitprogramme/gleichungen-formeln/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Sek1-Mathe begreifbar · Leitprogramm</p>
      <h1>Bruchterme, Gleichungen und Formeln</h1>
      <p class="unter">Zuschauen, tüfteln, kontrollieren, üben. Vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Gleichungen</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Kürzen</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Rechnen</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Gleichungen</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Formeln</span></a></li>
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
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen. Mit <b>💡 Tipp</b> bekommst du Hilfe in drei Stufen. Brüche tippst du mit <code>/</code> und Klammern: <code>(x-3)/(x+3)</code>, <code>3/(2x)</code>; Lösungsmengen als Zahl, <code>{}</code> (keine Lösung) oder <code>Q</code> (alle Zahlen).</li>
          <li><b>⑤ Aufgaben</b> auf Papier mit Rechenweg, dann Lösung aufklappen und abhaken.</li>
          <li>Zum Schluss der <b>Gesamttest</b> auf Papier. Alles ohne Taschenrechner.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">Das kannst du danach, alles <span class="ohm">ohne Taschenrechner</span>:</p>
        <ul>
          <li><b>K1</b> Bruchterme kürzen, indem du zuerst in Faktoren zerlegst, und angeben, welche Zahlen nicht erlaubt sind (Kapitel 1)</li>
          <li><b>K2</b> Bruchterme multiplizieren, dividieren, addieren und subtrahieren, mit dem Hauptnenner (Kapitel 2)</li>
          <li><b>K3</b> lineare Gleichungen mit Klammern und Brüchen lösen, die Lösungsmenge angeben und die Probe machen (Kapitel 3)</li>
          <li><b>K4</b> Formeln nach einer Grösse umstellen und damit Werte berechnen (Kapitel 4)</li>
        </ul>
        <p class="rlp-quelle">Nicht in diesem Leitprogramm: quadratische Gleichungen, Ungleichungen, Gleichungen mit Parametern. Zum Vertiefen bei Mathe begreifbar: ''' + V_LIN + ' · ' + V_FAELLE + '''.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Bruchterme, Gleichungen und Formeln · Sek1-Mathe begreifbar</span>
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
{fussblock}

<script src="../mathlib.js"></script>
<script src="../nav.js"></script>
<script src="../suche.js"></script>
<script>buildNav({{ bereich: 'lp', id: 'lp-gleichungen' }});</script>
</body>
</html>
'''
# Zeiten: Vorwissen 10 · K1 40 · K2 45 · K3 45 · K4 40 · Gesamttest 30 = 210 min
body = oben + k0 + k1 + k2 + k3 + k4 + gt + vt + unten
seite = (kopf + open(SP + 'kopf.css').read() + open(SP + 'seite.css').read() + '</style>\n</head>\n<body>\n' + body + '\n'
         + mathjax + open(SP + 'basis.js').read() + '\n</script>\n' + open(SP + 'seite.js').read() + '\n' + fuss)
os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
open(ZIEL, 'w').write(seite)
print('geschrieben', ZIEL, len(seite.splitlines()), 'Zeilen')
