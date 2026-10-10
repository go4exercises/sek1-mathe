"""Baut leitprogramme/darstellungen.html aus einer Kapitelbeschreibung (10.10.2026).

  python3 scripts/lp/darstellungen/seite.py

Leitprogramm Darstellungen wechseln (Lineare Funktionen II, Bereich Funktionen), Gerüst aus scripts/lp/lineare-funktionen/.
Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026); vertieft wird auf den Themenseiten von
Mathe begreifbar (TALS). Alles kommt aus diesem Ordner: kopf.css, seite.css, basis.js (Thema, Fortschritt,
Schiene), seite.js (Koordinatensystem, Simulationen, Übungen mit Zahlen und Klickgitter). Nur SEO-Block und Footer werden aus der bestehenden Seite
übernommen — beide schreibt scripts/build-seo.py. Wiederholbar. Danach Pre-Flight und build-seo.py.
"""
import json
import os

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/darstellungen.html'
NAME = 'Darstellungen wechseln'
CLIP = 'dar-lp-'

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
V_DARST = tals('grundlagen/g3-2-lineare-funktionen.html', 'Darstellungen einer linearen Funktion', '#darstellungen')
V_BER = tals('grundlagen/g3-1-grundlagen.html', 'Definitions- und Wertemenge', '#bereiche')
V_MOD = tals('grundlagen/g2-modellieren.html', 'Modellieren')
V_GRAPH = tals('grundlagen/g3-1-grundlagen.html', 'Darstellungen von Funktionen', '#darstellungen')


def bild(geraden='', punkte='', label='Gerade im Koordinatensystem'):
    return f'\n            <div class="mini-reihe"><svg class="mini-gerade" data-geraden="{geraden}" data-punkte="{punkte}" aria-label="{label}"></svg></div>'


# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1" aria-label="Eine Situation als Satz, Gleichung, Tabelle und Graph">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <p class="sim-satz" data-rolle="satz" aria-live="polite"></p>
        <svg role="img" aria-label="Graph der Geraden mit markiertem Wertepaar"></svg>
        <table class="wt" aria-label="Wertetabelle"></table>
        <div class="sl-row">
          {regler('s1-b', 'Anfangswert b', 'orange', 0, 60, 10)}
          {regler('s1-m', 'Änderung m', 'blau', -10, 10, 2)}
        </div>
        <div class="sl-row">
          {regler('s1-x', 'Stelle x', 'gruen', 0, 10, 0)}
        </div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Eine Situation, vier Darstellungen</div>
          <p>Kletterhalle: Jahresbeitrag \(40\) Fr., dazu \(6\) Fr. für jeden Eintritt.</p>
          <ul class="kurz">
            <li><b>Text:</b> «\(40\) Fr. im Jahr, dazu \(6\) Fr. pro Eintritt.»</li>
            <li><b>Gleichung:</b> \(y = 6x + 40\) mit \(x\): Anzahl Eintritte, \(y\): Kosten in Fr.</li>
            <li><b>Tabelle:</b> \(x = 0, 1, 2, 3, 4\) gibt \(y = 40, 46, 52, 58, 64\).</li>
            <li><b>Graph:</b> einzelne Punkte \((0 \mid 40)\), \((1 \mid 46)\), …, denn es gibt nur ganze Eintritte.</li>
            <li><b>Aussage:</b> Der Punkt \((5 \mid 70)\) heisst: \(5\) Eintritte kosten zusammen \(70\) Fr.</li>
          </ul>
          <p><b>Tabelle → Gleichung</b>, auch wenn die Tabelle nicht bei \(x = 0\) beginnt:</p>
          <ol class="weg">
            <li>\(x\): \(2, 4, 6\) und \(y\): \(52, 64, 76\)</li>
            <li>\(m = \dfrac{\Delta y}{\Delta x} = \dfrac{12}{2} = 6\) <span class="warum">die Tabelle springt um 2</span></li>
            <li>\(52 = 6 \cdot 2 + b\), also \(b = 40\) <span class="warum">ein Wertepaar einsetzen</span></li>
          </ol>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Schritt in \(x\) vergessen:</b> Aus \(52, 64, 76\) folgt nicht \(m = 12\). Die \(12\) gehört zu \(2\) Schritten, \(m = 6\).</p>
          <p><b>Punkt falsch gelesen:</b> \((5 \mid 70)\) heisst nicht «ein Eintritt kostet \(70\) Fr.». Der \(y\)-Wert ist das Ganze bei diesem \(x\).</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 14, [
    ('1a', 3, r'Ein Handy-Abo kostet \(15\) Fr. im Monat, dazu \(4\) Fr. für jedes GB Daten. Schreib die Gleichung (\(x\): GB, \(y\): Fr.), die Tabelle für \(0\) bis \(3\) GB, und berechne, wie viele GB \(39\) Fr. kosten.',
     r'<p>\(y = 4x + 15\); Tabelle \(15, 19, 23, 27\). \(4x + 15 = 39\), \(4x = 24\), \(x = 6\) GB.</p>', ''),
    ('1b', 3, r'In einem Planschbecken ist nach \(x\) Minuten noch so viel Wasser (in Litern): \(x\): \(0, 5, 10\) und \(y\): \(200, 175, 150\). Stelle die Gleichung auf. Was bedeutet \(m\) hier? Wann ist das Becken leer?',
     r'<p>\(m = \dfrac{-25}{5} = -5\), \(b = 200\): \(y = -5x + 200\). Pro Minute fliessen \(5\) l ab. Leer bei \(-5x + 200 = 0\), nach \(40\) Minuten.</p>', ''),
    ('1c', 2, r'Der Graph zeigt die Parkgebühr \(y\) in Fr. für \(x\) Stunden. Schreib in Worten, wie die Gebühr berechnet wird, und die Gleichung.',
     r'<p>Durch \((0 \mid 2)\) und \((4 \mid 6)\): \(2\) Fr. Grundgebühr, dazu \(1\) Fr. pro Stunde. \(y = x + 2\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini-gerade" data-geraden="1/1,2" data-punkte="0,2;4,6" data-fenster="0,7,0,9" data-xname="x [h]" data-yname="y [Fr.]" aria-label="Parkgebühr: Strecke ab (0 | 2) durch (4 | 6)"></svg></div>'),
    ('1d', 2, r'Lia liest aus der Tabelle \(x\): \(2, 4, 6\) und \(y\): \(9, 15, 21\) ab: «\(m = 6\)». Was ist falsch? Gib die richtige Gleichung an.',
     r'<p>Die \(6\) gehört zu \(2\) Schritten in \(x\): \(m = \dfrac{6}{2} = 3\). \(9 = 3 \cdot 2 + b\), \(b = 3\): \(y = 3x + 3\).</p>', ''),
    ('1e', 2, r'Ein Taxi kostet \(y = 2.5x + 6\) Franken für \(x\) Kilometer. Was bedeuten \(2.5\), \(6\) und der Punkt \((8 \mid 26)\)? Wie weit kommst du mit \(31\) Fr.?',
     r'<p>\(2.5\): Jeder Kilometer kostet \(2.50\) Fr. \(6\): Beim Einsteigen bezahlt man \(6\) Fr. \((8 \mid 26)\): Eine Fahrt über \(8\) km kostet \(26\) Fr. Mit \(31\) Fr.: \(2.5x = 25\), \(x = 25 : 2.5 = 10\) km.</p>', ''),
    ('1f', 2, r'Warum genügen zwei Wertepaare einer Tabelle, um die Gleichung einer linearen Funktion zu finden?',
     r'<p>Durch zwei Punkte geht genau eine Gerade. Aus den beiden Paaren bekommst du \(m = \dfrac{\Delta y}{\Delta x}\), mit einem Paar dann \(b\). Ein drittes Paar ist eine gute Probe.</p>', ''),
])
k1 = kapitel(1, 'darstellungen', 'Vier Darstellungen', 40,
             r'Du wechselst zwischen Text, Gleichung, Wertetabelle und Graph und sagst in Worten, was ein Punkt, \(m\) und \(b\) in einer Situation bedeuten.',
             (CLIP + 'darstellungen', 'Vier Darstellungen'), sim1,
             (CLIP + 'kontrolle-darstellungen', 'Kontrollfragen zu den Darstellungen'), fest1,
             [uebung('tabelle', 'Gleichung aus der Tabelle'), uebung('deuten', 'Was bedeutet das?')],
             auf1, V_DARST, komp='K1')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2" aria-label="Rechteck mit festem Umfang">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <div class="sim-paar">
          <svg class="rechteck-bild" role="img" aria-label="Rechteck mit den Seiten x und y"></svg>
          <svg class="graf" role="img" aria-label="y in Abhängigkeit von x"></svg>
        </div>
        <div class="sl-row">
          {regler('s2-U', 'Umfang U', 'orange', 8, 40, 12).replace('step="1"', 'step="2"')}
          {regler('s2-x', 'Seite x', 'gruen', 0.5, 20, 1).replace('step="1"', 'step="0.5"')}
        </div>
      </figure>'''
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Die Summe bleibt gleich</div>
          <p>Ein Rechteck hat den Umfang \(24\) cm. Seiten \(x\) und \(y\):</p>
          <ol class="weg">
            <li>\(2x + 2y = 24\) <span class="warum">jede Seite kommt zweimal vor</span></li>
            <li>\(x + y = 12\) <span class="warum">durch 2</span></li>
            <li>\(y = 12 - x = -x + 12\) <span class="warum">\(-x\) auf beiden Seiten</span></li>
          </ol>
          <p>Allgemein: \(y = \tfrac{U}{2} - x\). Die Steigung ist \(-1\): Wird \(x\) um \(1\) cm länger, wird \(y\) um \(1\) cm kürzer. Die Summe \(x + y\) bleibt gleich, darum <b>fällt</b> der Graph.</p>
          <p>Jede Gleichung \(a \cdot x + c \cdot y = S\) mit \(c \neq 0\) löst du so nach \(y\) auf: zuerst \(-a \cdot x\), dann durch \(c\). Zum Beispiel \(3x + 2y = 30\): \(2y = 30 - 3x\), \(y = 15 - 1.5x\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Nur teilweise geteilt:</b> Aus \(2x + 2y = 24\) wird nicht \(y = 24 - 2x\). Probe mit \(x = 2\): Dann wäre \(y = 20\) und der Umfang \(2 \cdot 2 + 2 \cdot 20 = 44\), nicht \(24\).</p>
          <p><b>Vorzeichen:</b> \(y = x + 12\) steigt. Bei gleicher Summe muss \(y\) kleiner werden, wenn \(x\) wächst.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 14, [
    ('2a', 2, r'In einem Saal gibt es \(50\) Plätze. \(x\) sind besetzt, \(y\) frei. Schreib \(y\) in Abhängigkeit von \(x\). Was bedeutet die Steigung?',
     r'<p>\(x + y = 50\), also \(y = 50 - x\). Steigung \(-1\): Jede Person, die sich setzt, macht einen Platz weniger frei.</p>', ''),
    ('2b', 3, r'Löse nach \(y\) auf: \(3x + y = 21\) und \(6x + 3y = 24\).',
     r'<p>\(y = -3x + 21\). \(3y = 24 - 6x\), \(y = -2x + 8\).</p>', ''),
    ('2c', 3, r'Ein gleichschenkliges Dreieck hat den Umfang \(30\) cm: zwei Schenkel je \(x\), die Basis \(y\). Schreib \(y\) in Abhängigkeit von \(x\) und berechne \(y\) für \(x = 10\) und \(x = 12\).',
     r'<p>\(2x + y = 30\), \(y = 30 - 2x\). Für \(x = 10\): \(y = 10\) (gleichseitig). Für \(x = 12\): \(y = 6\).</p>', ''),
    ('2d', 2, r'Ben schreibt für ein Rechteck mit Umfang \(40\) cm: \(y = 40 - 2x\). Prüfe mit \(x = 5\) und korrigiere.',
     r'<p>Mit \(x = 5\) gäbe es \(y = 30\) und den Umfang \(2 \cdot 5 + 2 \cdot 30 = 70\). Ben hat nur \(2x\) abgezogen, aber nicht durch \(2\) geteilt. Richtig: \(y = 20 - x\).</p>', ''),
    ('2e', 2, r'Du hast \(24\) Fr. für Hefte (\(3\) Fr.) und Stifte (\(2\) Fr.) und gibst alles aus. Schreib die Anzahl Stifte \(y\) in Abhängigkeit der Anzahl Hefte \(x\). Was bedeutet die Steigung? Welche Paare sind möglich?',
     r'<p>\(3x + 2y = 24\), \(y = 12 - 1.5x\). Steigung \(-1.5\): Ein Heft mehr heisst \(1.5\) Stifte weniger, also \(2\) Hefte mehr, \(3\) Stifte weniger. Nur ganze Anzahlen: \((0 \mid 12)\), \((2 \mid 9)\), \((4 \mid 6)\), \((6 \mid 3)\), \((8 \mid 0)\).</p>', ''),
    ('2f', 2, r'Warum hat \(y\) bei \(x + y = S\) immer die Steigung \(-1\), egal wie gross \(S\) ist?',
     r'<p>Die Summe bleibt gleich: Was \(x\) dazubekommt, verliert \(y\). Wird \(x\) um \(1\) grösser, wird \(y\) um \(1\) kleiner. \(S\) verschiebt die Gerade nur.</p>', ''),
])
k2 = kapitel(2, 'summe', 'Wenn die Summe gleich bleibt', 40,
             r'Du bildest aus einem festen Gesamtwert, zum Beispiel einem Umfang, eine lineare Gleichung \(y = m \cdot x + b\) und deutest ihre fallende Steigung.',
             (CLIP + 'summe', 'Wenn die Summe gleich bleibt'), sim2,
             (CLIP + 'kontrolle-summe', 'Kontrollfragen zur festen Summe'), fest2,
             [uebung('aufloesen', 'Nach y auflösen'), uebung('umfang', 'Umfang und Seiten')],
             auf2, V_MOD, komp='K2')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3" aria-label="Sinnvoller Bereich und Darstellung eines Sachgraphen">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Sachgraph mit gewähltem Bereich"></svg>
        <div class="sl-row">
          {regler('s3-von', 'von x =', 'gruen', 0, 20, 2).replace('step="1"', 'step="0.5"')}
          {regler('s3-bis', 'bis x =', 'gruen', 0, 20, 18).replace('step="1"', 'step="0.5"')}
        </div>
        <div class="sl-row">
          <label class="sim-schalter" for="s3-art">Darstellung
            <select id="s3-art" class="sim-wahl"><option value="strecke" selected>Strecke</option><option value="punkte">einzelne Punkte</option></select></label>
        </div>
      </figure>'''
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Ein Graph zum Sachverhalt</div>
          <p>Treppe: \(2h + a = 63\) (in cm, \(h\) Stufenhöhe, \(a\) Auftrittsbreite), also \(a = 63 - 2h\). Erlaubt seien Stufen von \(15\) bis \(20\) cm.</p>
          <ol class="weg">
            <li><b>Definitionsbereich</b> (auch Definitionsmenge) aus dem Text: \(15 \le h \le 20\) <span class="warum">nur sinnvolle Werte</span></li>
            <li><b>Endpunkte</b> rechnen: \(h = 15\): \(a = 33\); \(h = 20\): \(a = 23\) <span class="warum">Wertebereich \(23 \le a \le 33\)</span></li>
            <li><b>Achsen</b>: Grösse und Einheit, gleichmässige Skala, bequeme Einteilung <span class="warum">grösster Wert : Häuschen, aufrunden auf 1, 2, 5, 10, 20, 25, 50, …</span></li>
            <li><b>Zeichnen</b>: eine Strecke zwischen den Endpunkten <span class="warum">Längen gibt es auch dazwischen</span></li>
          </ol>
          <p>Bei <b>Anzahlen</b> (Eintritte, Tickets, Personen) zeichnest du nur <b>einzelne Punkte</b>: \(2.5\) Eintritte gibt es nicht.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Ungleichmässige Skala:</b> \(0, 10, 20, 50\) in gleichen Abständen. Die Gerade sieht dann geknickt aus.</p>
          <p><b>Ganze Gerade gezeichnet:</b> \(h = 30\) cm gäbe \(a = 3\) cm. Ausserhalb des Definitionsbereichs hat der Graph keinen Sinn. Und ohne Einheit an der Achse weiss niemand, was gemeint ist.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 14, [
    ('3a', 3, r'Treppenregel \(2h + a = 63\) (in cm). Löse nach \(h\) auf. Eine Treppe soll Auftrittsbreiten \(a\) von \(25\) bis \(31\) cm haben: Welche Stufenhöhen gehören dazu? Gib Definitions- und Wertebereich an.',
     r'<p>\(2h = 63 - a\), \(h = \dfrac{63 - a}{2}\). \(a = 25\): \(h = 19\); \(a = 31\): \(h = 16\). Definitionsbereich \(25 \le a \le 31\), Wertebereich \(16 \le h \le 19\) cm. Je breiter der Auftritt, desto niedriger die Stufe.</p>', ''),
    ('3b', 2, r'Wie viel soll ein Häuschen bedeuten? (a) Werte bis \(450\), \(9\) Häuschen. (b) Werte bis \(70\), \(8\) Häuschen.',
     r'<p>(a) \(450 : 9 = 50\), also \(50\). (b) \(70 : 8 = 8.75\), aufgerundet auf die bequeme Zahl \(10\).</p>', ''),
    ('3c', 2, r'Strecke oder einzelne Punkte? (a) Preis einer Taxifahrt nach \(x\) km. (b) Kosten für \(x\) Konzerttickets. (c) Ein Lift ist mit \(8\) Personen voll: Erwachsene \(y\) in Abhängigkeit der Kinder \(x\). (d) Wasser in einer Wanne nach \(x\) Minuten.',
     r'<p>(a) Strecke. (b) Punkte. (c) Punkte (nur ganze Personen). (d) Strecke.</p>', ''),
    ('3d', 3, r'Ein Taxi kostet \(6\) Fr. Grundtaxe und \(3\) Fr. pro km, für Fahrten bis \(10\) km. Zeichne den Graphen auf Häuschenpapier, die \(y\)-Achse hat \(8\) Häuschen: Achsen mit Grösse, Einheit und Einteilung.',
     r'<p>\(y = 3x + 6\), Endpunkte \((0 \mid 6)\) und \((10 \mid 36)\). Zum Beispiel \(x\)-Achse «Strecke [km]», \(1\) Häuschen \(= 1\) km; \(y\)-Achse «Preis [Fr.]», \(1\) Häuschen \(= 5\) Fr. (\(36 : 8 = 4.5\), bequem \(5\)). Strecke von \((0 \mid 6)\) bis \((10 \mid 36)\).</p>', ''),
    ('3e', 2, r'Mia beschriftet die \(y\)-Achse in gleichen Abständen mit \(0, 10, 20, 50, 100\). Was ist falsch, und was sieht man dann im Graphen?',
     r'<p>Die Abstände stehen für verschiedene Schritte (\(10\), \(10\), \(30\), \(50\)). Die Skala ist nicht gleichmässig: Eine Gerade sieht geknickt aus, und Steigungen kann man nicht vergleichen.</p>', ''),
    ('3f', 2, r'Warum endet der Graph einer abbrennenden Kerze bei \(y = 0\)?',
     r'<p>Eine Kerze kann nicht weniger als \(0\) cm hoch sein. Danach gibt es nichts mehr zu messen; die Gleichung würde negative Höhen liefern.</p>', ''),
])
k3 = kapitel(3, 'achsen', 'Sinnvolle Werte, saubere Achsen', 40,
             r'Du wählst den sinnvollen Bereich einer Grösse, skalierst und beschriftest die Achsen und entscheidest, ob der Graph eine Strecke ist oder aus Punkten besteht.',
             (CLIP + 'achsen', 'Sinnvolle Werte, saubere Achsen'), sim3,
             (CLIP + 'kontrolle-achsen', 'Kontrollfragen zu Bereich und Achsen'), fest3,
             [uebung('bereich', 'Sinnvoller Bereich'), uebung('skala', 'Achse einteilen')],
             auf3, V_BER, komp='K3')

# ------------------------------------------------------------------ Kapitel 4
sim4 = f'''      <figure class="sim sim-gross" id="sim4" aria-label="Summe gleich oder Produkt gleich">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Gerade y = S − x und Kurve y = P / x"></svg>
        <div class="sl-row">
          {regler('s4-S', 'Summe S', 'blau', 4, 20, 8)}
          {regler('s4-P', 'Produkt P', 'grau', 4, 40, 12)}
        </div>
        <div class="sl-row">
          {regler('s4-x', 'Stelle x', 'gruen', 0.5, 20, 1).replace('step="1"', 'step="0.5"')}
        </div>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Linear fallend oder antiproportional</div>
          <table class="wt vergleich">
            <tr><th></th><th>Summe gleich: \(x + y = S\)</th><th>Produkt gleich: \(x \cdot y = P\)</th></tr>
            <tr><th>Name</th><td>linear fallend, \(y = S - x\)</td><td>antiproportional, \(y = \dfrac{P}{x}\)</td></tr>
            <tr><th>Tabelle</th><td>\(\Delta y : \Delta x\) gleich; bei gleichen Schritten in \(x\) also gleiche Differenzen</td><td>gleiche Produkte</td></tr>
            <tr><th>\(x\) verdoppeln</th><td>\(y\) wird um so viel kleiner, wie \(x\) grösser wird, nicht halbiert</td><td>\(y\) wird halbiert</td></tr>
            <tr><th>Graph</th><td>fallende Gerade; verlängert trifft sie beide Achsen</td><td>Kurve, trifft keine Achse</td></tr>
          </table>
          <p>Velo, \(30\) km: Der Restweg bei \(15\) km/h ist \(s = 30 - 15t\), linear fallend. Die Fahrzeit bei \(v\) km/h ist \(t = \dfrac{30}{v}\), antiproportional: doppelt so schnell, halb so lang.</p>
          <p><b>Aussagen prüfen:</b> Ein Gegenbeispiel genügt, um eine Aussage zu widerlegen. Ein Beispiel, das passt, beweist sie nicht.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>«Fällt, also antiproportional»:</b> \(y = 12 - x\) fällt, aber \(2 \cdot 10 = 20\) und \(4 \cdot 8 = 32\): Das Produkt ändert sich.</p>
          <p><b>«Gleicher Umfang, gleiche Fläche»:</b> Beide Rechtecke \(2 \times 10\) und \(6 \times 6\) haben den Umfang \(24\) cm, aber die Flächen \(20\) und \(36\) cm².</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 14, [
    ('4a', 3, r'Welche Tabelle ist linear fallend, welche antiproportional, welche proportional? Begründe. A: \(x\): \(1, 2, 4, 5\), \(y\): \(20, 10, 5, 4\). B: \(y\): \(18, 15, 9, 6\). C: \(y\): \(2, 4, 8, 10\) (jeweils dieselben \(x\)).',
     r'<p>A antiproportional: \(x \cdot y = 20\) immer. B linear fallend: pro Schritt in \(x\) um \(1\) wird \(y\) um \(3\) kleiner, \(y = -3x + 21\). C proportional: \(y : x = 2\) immer.</p>', ''),
    ('4b', 3, r'Für eine Fahrt von \(120\) km: Wie lange dauert sie bei \(40\), \(60\) und \(80\) km/h? Schreib die Gleichung und benenne den Zusammenhang.',
     r'<p>\(3\) h, \(2\) h, \(1.5\) h. \(t = \dfrac{120}{v}\), antiproportional: \(v \cdot t = 120\).</p>', ''),
    ('4c', 2, r'Auf derselben Fahrt mit \(60\) km/h: Wie weit ist es nach \(t\) Stunden noch? Wie weit nach \(1.5\) h?',
     r'<p>\(s = 120 - 60t\), linear fallend. Nach \(1.5\) h: \(120 - 90 = 30\) km.</p>', ''),
    ('4d', 2, r'Behauptung: «Wenn \(y\) kleiner wird, während \(x\) wächst, ist der Zusammenhang antiproportional.» Widerlege sie mit einem Gegenbeispiel.',
     r'<p>Zum Beispiel \(y = 10 - x\): \(x = 1\), \(y = 9\), Produkt \(9\); \(x = 2\), \(y = 8\), Produkt \(16\). Das Produkt bleibt nicht gleich.</p>', ''),
    ('4e', 2, r'Rechtecke mit der Fläche \(24\) cm² und Rechtecke mit dem Umfang \(20\) cm: Berechne \(y\) für \(x = 2, 4, 6\) cm. Welcher Zusammenhang ist linear?',
     r'<p>Fläche \(24\): \(y = \dfrac{24}{x}\): \(12, 6, 4\), antiproportional. Umfang \(20\): \(y = 10 - x\): \(8, 6, 4\), linear fallend.</p>', ''),
    ('4f', 2, r'Warum trifft der Graph von \(y = \dfrac{12}{x}\) die \(x\)-Achse nie?',
     r'<p>Für \(y = 0\) müsste \(x \cdot 0 = 12\) sein. Das geht nicht: Ein Bruch mit Zähler \(12\) ist nie null. Je grösser \(x\), desto näher kommt die Kurve der Achse, ohne sie zu treffen.</p>', ''),
])
k4 = kapitel(4, 'antiproportional', 'Linear fallend oder antiproportional?', 40,
             r'Du unterscheidest einen linear fallenden von einem antiproportionalen Zusammenhang an Tabelle, Gleichung und Graph und widerlegst falsche Aussagen mit einem Gegenbeispiel.',
             (CLIP + 'antiproportional', 'Linear fallend oder antiproportional?'), sim4,
             (CLIP + 'kontrolle-antiproportional', 'Kontrollfragen: linear oder antiproportional'), fest4,
             [uebung('art', 'Welcher Zusammenhang?'), uebung('gegenbeispiel', 'Gegenbeispiel finden')],
             auf4, V_GRAPH, komp='K4')

# ------------------------------------------------------------------ Vorwissen
k0 = f'''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-th">Vorwissen</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Lineare Funktionen aus dem Leitprogramm 4, nach \\(y\\) auflösen, proportional und antiproportional, Zeiten. Zuerst kurz wiederholen, dann der Vortest.</p>
''' + r'''      <details class="anleitung">
        <summary><h3>Kurz wiederholt</h3></summary>
        <ul class="kurz">
          <li><b>Lineare Funktion:</b> \(y = m \cdot x + b\) mit Anfangswert \(b\) (bei \(x = 0\)) und Änderung \(m\), wenn \(x\) um \(1\) grösser wird.</li>
          <li><b>Nach \(y\) auflösen:</b> \(x + y = 25\) gibt \(y = 25 - x\).</li>
          <li><b>Proportional:</b> \(y : x\) bleibt gleich (\(1, 2, 3\) Stück kosten \(4, 8, 12\) Fr.). <b>Antiproportional</b> (umgekehrt proportional): \(x \cdot y\) bleibt gleich (\(2\) Personen brauchen \(6\) h, \(4\) Personen \(3\) h).</li>
          <li><b>Zeiten:</b> \(1\) h \(= 60\) min, also \(30\) min \(= 0.5\) h.</li>
        </ul>
      </details>
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Setze ein: \(y = 4x + 10\) für \(x = 0\) und für \(x = 3\).',
     r'<p>\(10\) und \(22\).</p>', ''),
    ('0b', 2, r'Löse nach \(y\) auf: \(x + y = 25\) und \(3x + y = 12\).',
     r'<p>\(y = 25 - x\) und \(y = -3x + 12\).</p>', ''),
    ('0c', 2, r'Welche Steigung hat die Gerade durch \((1 \mid 5)\) und \((4 \mid 14)\)?',
     r'<p>\(m = \dfrac{14 - 5}{4 - 1} = 3\).</p>', ''),
    ('0d', 2, r'Proportional oder antiproportional? A: \(x\): \(1, 2, 4\), \(y\): \(12, 6, 3\). B: \(x\): \(1, 2, 4\), \(y\): \(3, 6, 12\).',
     r'<p>A antiproportional (\(x \cdot y = 12\)), B proportional (\(y : x = 3\)).</p><p class="komm">Das brauchst du in Kapitel 4.</p>', ''),
    ('0e', 2, r'Schreib in Stunden: \(2\) h \(30\) min und \(90\) min.',
     r'<p>\(2.5\) h und \(1.5\) h.</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: «Kurz wiederholt» nochmals lesen und die Lösungen nachrechnen; lineare Funktionen übst du im Leitprogramm <a href="lineare-funktionen.html">Lineare Funktionen</a>.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest (nur PDF)
PDF = '../downloads/leitprogramme/darstellungen/'
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
            <div class="frage"><span class="nr">V1</span><span class="txt">Rechtecke mit dem Umfang \(20\) cm: Für welche Länge \(x\) ist die Fläche am grössten? Probiere mit einer Tabelle für \(x = 1, 2, \dots, 9\).</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\(y = 10 - x\), Fläche \(x(10 - x)\): \(9, 16, 21, 24, 25, 24, 21, 16, 9\). Am grössten beim Quadrat \(5 \times 5\) mit \(25\) cm². Die Fläche ist nicht linear: Sie steigt und fällt wieder.</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V2</span><span class="txt">Treppe mit \(2h + a = 63\): Bei welcher Stufenhöhe wären \(h\) und \(a\) gleich gross? Wäre das eine bequeme Treppe?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\(2h + h = 63\), \(h = 21\) cm und \(a = 21\) cm. Das liegt ausserhalb von \(15\) bis \(20\) cm: sehr steil, eher eine Leitertreppe.</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V3</span><span class="txt">\(4\) Personen streichen einen Zaun in \(6\) Stunden. Wie lange brauchen \(3\) Personen, wenn alle gleich schnell arbeiten? Gilt das auch für \(100\) Personen?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\(4 \cdot 6 = 24\) Personenstunden, also \(24 : 3 = 8\) h. Mit \(100\) Personen wären es \(0.24\) h, etwa \(14\) Minuten. In Wirklichkeit stehen sich so viele im Weg: Das Modell «antiproportional» gilt nur in einem sinnvollen Bereich.</p></div></details>
          </li>
        </ol>
      </div>
      <p class="ausf weiter">Weiter: Funktionen und ihre Darstellungen bei Mathe begreifbar: ''' + V_GRAPH + r'''.</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Darstellungen wechseln (Lineare Funktionen II), Version 1.0 (10.10.2026). Gebaut aus
     scripts/lp/darstellungen/seite.py — Änderungen dort, nicht in dieser Datei. Grundlagen: HOWTO-leitprogramme.md
     (Kapitelmuster) und ~/TODO-BM-Vorkurs-LP03-15.md, Abschnitt 3 (LP 05, Darstellungswechsel), für die Sek I umgesetzt.

     Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026): Das Leitprogramm ist selbst die fachliche Quelle;
     Vertiefung bei Mathe begreifbar. Baut auf dem Leitprogramm Lineare Funktionen (LP 4) auf.
     Notation: y = m · x + b, Punkte (x | y), Grösse [Einheit] an den Achsen, Dezimalpunkt.

     Kompetenzen — eigene Formulierung, ohne Lehrplan-Nummern (CLAUDE.md: keine erfundenen Lehrplan-Stellen):
       K1  Zwischen Text, Gleichung, Wertetabelle und Graph wechseln; Punkte, m und b in Worten deuten
       K2  Aus einem festen Gesamtwert (Summe, Umfang) eine lineare Gleichung bilden und nach y auflösen
       K3  Sinnvollen Definitionsbereich wählen, Achsen skalieren und beschriften, Strecke oder Punkte zeichnen
       K4  Linear fallend und antiproportional unterscheiden; Aussagen mit Gegenbeispiel widerlegen

     Kompetenzmatrix (Kompetenz | Kapitel | Simulation | Übungen | Kapitelaufgaben | Gesamttest):
       K1 | 1 | Sim 1 vier Darstellungen | tabelle, deuten        | 1a–1f | G1, G2
       K2 | 2 | Sim 2 Rechteck           | aufloesen, umfang      | 2a–2f | G3, G4
       K3 | 3 | Sim 3 Bereich            | bereich, skala         | 3a–3f | G5, G6
       K4 | 4 | Sim 4 Summe/Produkt      | art, gegenbeispiel     | 4a–4f | G7, G8

     Planung (Kapitel | Lernziel | Erkundung | Beispiel | Häufiger Fehler | min):
       0 | Vorwissen       | –                  | –                              | –                                  | 10
       1 | Darstellungen   | gekoppelt          | Kletterhalle 40 + 6 Fr.        | Δx vergessen; Punkt falsch gelesen | 40
       2 | feste Summe     | Rechteck, Umfang   | U = 24 cm; 3x + 2y = 30        | nicht ganz geteilt; Vorzeichen     | 40
       3 | Bereich, Achsen | Definitionsbereich | Treppe 2h + a = 63             | Skala ungleich; ganze Gerade       | 40
       4 | antiproportional| Summe oder Produkt | Velo 30 km; Rechteck           | «fällt, also anti»; Fläche gleich  | 40
       Gesamttest (PDF) 30 · Summe 200 min ≈ 4.4 Lektionen. Vertiefung V1–V3 freiwillig, nicht eingerechnet.

     Aus der Vorlage umgesetzt: Text ↔ Term ↔ Tabelle ↔ Graph ↔ Aussage (Kapitel 1), 2x + 2y = U → y = U/2 − x
     (Kapitel 2), Definitionsbereich, Achsenskalierung mit Einheit (Kapitel 3), linear fallend ≠ antiproportional mit
     Rechteck konstanten Umfangs und Velofahrt (Kapitel 4), falsche Aussagen mit Gegenbeispiel (Übung, 4d, G8).
     Bewusst nicht übernommen: Teams-Ablauf, Lehrpersonenteil, Prüfungsnummern.

     Clips: je Kapitel ein Einführungsclip (mit einer Vorhersagefrage) und ein Kontrollclip mit fünf Fragen,
     Reihe «Funktionen sehen», dar-lp-*.json, erzeugt mit scripts/lp/darstellungen/clips.py.

     Farben: Gerade und m blau, b orange, antiproportionale Kurve Tinte, Treffer grün, Fehler rot; Bereichsfarbe Petrol.
     Gesamttest und Bewertungspaket nur als PDF (downloads/leitprogramme/darstellungen/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Sek1-Mathe begreifbar · Leitprogramm</p>
      <h1>Darstellungen wechseln</h1>
      <p class="unter">Lineare Funktionen II: Text, Gleichung, Tabelle und Graph. Vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
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
      <li><a href="#k1"><span class="nr">1</span><span>Darstellungen</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Feste Summe</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Bereich, Achsen</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Antiproportional</span></a></li>
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
          <li><b>K1</b> zwischen Text, Gleichung, Wertetabelle und Graph wechseln und in Worten sagen, was ein Punkt, \\(m\\) und \\(b\\) bedeuten (Kapitel 1)</li>
          <li><b>K2</b> aus einem festen Gesamtwert, zum Beispiel einem Umfang, eine lineare Gleichung bilden und nach \\(y\\) auflösen (Kapitel 2)</li>
          <li><b>K3</b> einen sinnvollen Bereich wählen, Achsen mit Grösse, Einheit und Einteilung zeichnen und entscheiden, ob Strecke oder Punkte (Kapitel 3)</li>
          <li><b>K4</b> linear fallend und antiproportional unterscheiden und falsche Aussagen mit einem Gegenbeispiel widerlegen (Kapitel 4)</li>
        </ul>
        <p class="rlp-quelle">Baut auf dem Leitprogramm «Lineare Funktionen» auf. Nicht in diesem Leitprogramm: Gleichungssysteme, quadratische Funktionen. Zum Vertiefen bei Mathe begreifbar: ''' + V_DARST + ' · ' + V_BER + '''.</p>
      </details>

    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Darstellungen wechseln · Sek1-Mathe begreifbar</span>
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
<script>buildNav({{ bereich: 'lp', id: 'lp-darstellungen' }});</script>
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
