"""Baut leitprogramme/bewegung.html aus einer Kapitelbeschreibung (10.10.2026).

  python3 scripts/lp/bewegung/seite.py

Leitprogramm Texte, Geschwindigkeit und Begegnung (Bereich Mathematisieren), Gerüst aus scripts/lp/funktionstypen/.
Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026); vertieft wird auf den Themenseiten von
Mathe begreifbar (TALS). Alles kommt aus diesem Ordner: kopf.css, seite.css, basis.js (Thema, Fortschritt,
Schiene), seite.js (Koordinatensystem, Simulationen, Übungen). Nur der SEO-Block wird aus der bestehenden Seite
übernommen — ihn schreibt scripts/build-seo.py. Wiederholbar. Danach Pre-Flight und build-seo.py.
"""
import json
import os

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/bewegung.html'
NAME = 'Texte, Geschwindigkeit und Begegnung'
STAND = 'Stand 10. Oktober 2026'
CLIP = 'bew-lp-'

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
V_MOD = tals('grundlagen/g2-modellieren.html', 'Textaufgaben modellieren')
V_LIN = tals('grundlagen/g3-2-lineare-funktionen.html', 'Lineare Funktionen')


HILFE = '''<p class="hilfekarte"><span>① gegeben, gesucht, Skizze</span><i>→</i><span>② Variable mit Einheit</span><i>→</i><span>③ Beziehung</span><i>→</i><span>④ Gleichung lösen</span><i>→</i><span>⑤ Prüfung und Antwortsatz</span></p>'''

# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1" aria-label="Zwei Tarife vergleichen">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Kosten von Angebot A und B in Abhängigkeit der Anzahl"></svg>
        <div class="sl-row">
          {regler('s1-x', 'Anzahl x', 'gruen', 0, 30, 0)}
        </div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Vom Text zur Gleichung</div>
          ''' + HILFE + r'''
          <p>Konto A kostet \(4\) Fr. im Monat und \(0.50\) Fr. pro Zahlung, Konto B \(7\) Fr. und \(0.20\) Fr. pro Zahlung. Ab wie vielen Zahlungen ist B günstiger?</p>
          <ol class="weg">
            <li>gegeben: Grundbeträge \(4\) und \(7\) Fr., Preise \(0.50\) und \(0.20\) Fr. pro Zahlung; gesucht: die Anzahl, ab der B billiger ist <span class="warum">markieren</span></li>
            <li>\(x\): Anzahl Zahlungen pro Monat <span class="warum">Variable mit Bedeutung</span></li>
            <li>Kosten A: \(4 + 0.5x\), Kosten B: \(7 + 0.2x\) <span class="warum">Beziehung in Franken</span></li>
            <li>\(4 + 0.5x = 7 + 0.2x\), \(0.3x = 3\), \(x = 10\) <span class="warum">gleich teuer</span></li>
            <li>Probe: \(x = 10\): je \(9\) Fr. \(x = 11\): A \(9.50\) Fr., B \(9.20\) Fr. <span class="warum">B ist jetzt billiger</span></li>
          </ol>
          <p><b>Antwortsatz:</b> Ab \(11\) Zahlungen pro Monat ist Konto B günstiger.</p>
          <p><b>Plausibel?</b> Passt die Antwort zur Frage, ist sie ganzzahlig, wo nur ganze Dinge möglich sind, und hat sie die richtige Grössenordnung?</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Gleichstand als Antwort:</b> Bei \(10\) Zahlungen sind beide gleich teuer. Günstiger wird B erst ab \(11\).</p>
          <p><b>Nur eine Zahl:</b> «\(x = 10\)» beantwortet die Frage nicht. Ein Antwortsatz mit Einheit gehört dazu, und manchmal muss gerundet werden: \(4.2\) Busse heisst \(5\) Busse, hier wird immer aufgerundet.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 14, [
    ('1a', 3, r'Velomiete A kostet \(20\) Fr. plus \(3\) Fr. pro Stunde, B kostet \(32\) Fr. plus \(1\) Fr. pro Stunde. Ab wie vielen ganzen Stunden ist B günstiger? Geh nach der Hilfekarte vor.',
     r'<p>\(x\): Stunden. \(20 + 3x = 32 + x\), \(2x = 12\), \(x = 6\): gleich teuer (\(38\) Fr.). Bei \(7\) Stunden: A \(41\) Fr., B \(39\) Fr. Ab \(7\) Stunden ist B günstiger.</p>', ''),
    ('1b', 2, r'Drei aufeinanderfolgende <b>ungerade</b> Zahlen haben die Summe \(45\). Welche Zahlen sind es?',
     r'<p>Ungerade Zahlen liegen \(2\) auseinander: \(n + (n + 2) + (n + 4) = 45\), \(3n + 6 = 45\), \(n = 13\): \(13,\ 15,\ 17\). Probe: \(45\).</p>', ''),
    ('1c', 2, r'Lara ist \(5\) Jahre älter als ihr Bruder. Zusammen sind sie \(41\) Jahre alt. Wie alt sind beide?',
     r'<p>Bruder \(x\), Lara \(x + 5\): \(2x + 5 = 41\), \(x = 18\). Der Bruder ist \(18\), Lara \(23\) Jahre alt.</p>', ''),
    ('1d', 2, r'\(75\) Personen fahren mit Kleinbussen zu je \(9\) Plätzen. Wie viele Busse braucht es?',
     r'<p>\(75 : 9 \approx 8.3\). Acht Busse reichen nicht (nur \(72\) Plätze): Es braucht \(9\) Busse. Hier wird aufgerundet, obwohl die erste Stelle nach dem Punkt klein ist.</p>', ''),
    ('1e', 3, r'Vier Hefte und ein Lineal zu \(3\) Fr. kosten zusammen \(31\) Fr. Tim rechnet \(4x + 3 = 31\) und erhält \(x = 7\). Mach die Probe und schreib einen Antwortsatz.',
     r'<p>Probe: \(4 \cdot 7 + 3 = 31\). Antwortsatz: Ein Heft kostet \(7\) Fr.</p>', ''),
    ('1f', 2, r'Warum gehört zu jeder Lösung einer Textaufgabe ein Antwortsatz?',
     r'<p>Die Gleichung liefert eine Zahl für \(x\). Erst der Satz sagt, was die Zahl bedeutet und ob sie die Frage beantwortet, etwa «ab 11» statt «bei 10», oder dass gerundet werden muss.</p>', ''),
])
k1 = kapitel(1, 'text', 'Vom Text zur Gleichung', 40,
             r'Du übersetzt eine Textaufgabe Schritt für Schritt in eine Gleichung: gegeben, gesucht, Variable mit Einheit, Beziehung, Gleichung, Prüfung und Antwortsatz.',
             (CLIP + 'text', 'Vom Text zur Gleichung'), sim1,
             (CLIP + 'kontrolle-text', 'Kontrollfragen zu Textaufgaben'), fest1,
             [uebung('tarif', 'Tarife vergleichen'), uebung('raetsel', 'Zahlenrätsel')],
             auf1, V_MOD, komp='K1')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2" aria-label="Weg aus Geschwindigkeit und Zeit">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Weg in Abhängigkeit der Zeit"></svg>
        <div class="sl-row">
          {regler('s2-v', 'Geschwindigkeit v', 'blau', 5, 120, 50).replace('step="1"', 'step="5"')}
          {regler('s2-t', 'Zeit t', 'gruen', 5, 180, 60).replace('step="1"', 'step="5"')}
        </div>
      </figure>'''
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Weg, Geschwindigkeit, Zeit</div>
          <p>\[ s = v \cdot t \qquad v = \dfrac{s}{t} \qquad t = \dfrac{s}{v} \]</p>
          <ul class="kurz">
            <li>Ein Zug fährt \(240\) km in \(2\) h: \(v = \dfrac{240}{2} = 120\) km/h.</li>
            <li>Ein Velo fährt \(20\) min mit \(18\) km/h: \(20\) min \(= \tfrac{1}{3}\) h, \(s = 18 \cdot \tfrac{1}{3} = 6\) km.</li>
            <li><b>Minuten in Stunden:</b> durch \(60\): \(45\) min \(= 0.75\) h.</li>
            <li><b>km/h und m/s:</b> \(1\) m/s \(= 3.6\) km/h. \(36\) km/h \(= 36 : 3.6 = 10\) m/s.</li>
          </ul>
          <p><b>Plausibel?</b> Ein Mensch geht etwa \(5\) km/h, ein Velo fährt \(15\) bis \(25\) km/h, ein Zug \(60\) bis \(200\) km/h.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Minuten als Stunden:</b> \(18\) km/h mal \(20\) min ist nicht \(360\) km. Zuerst \(20\) min \(= \tfrac{1}{3}\) h.</p>
          <p><b>Minuten hinter den Punkt geschrieben:</b> \(45\) min sind nicht \(0.45\) h, sondern \(45 : 60 = 0.75\) h. Und \(1\) h \(30\) min sind \(1.5\) h, nicht \(1.30\) h.</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 14, [
    ('2a', 3, r'Ein Zug fährt \(150\) km in \(2\) h \(30\) min. Wie schnell fährt er? Wie weit kommt er mit diesem Tempo in \(40\) min?',
     r'<p>\(2\) h \(30\) min \(= 2.5\) h, \(v = 150 : 2.5 = 60\) km/h. \(40\) min \(= \tfrac{2}{3}\) h, \(s = 60 \cdot \tfrac{2}{3} = 40\) km.</p>', ''),
    ('2b', 2, r'Rechne um: \(5\) m/s in km/h und \(90\) km/h in m/s.',
     r'<p>\(5 \cdot 3.6 = 18\) km/h. \(90 : 3.6 = 25\) m/s.</p>', ''),
    ('2c', 2, r'Wie lange braucht ein Velo für \(12\) km mit \(15\) km/h? Gib die Zeit in Minuten an.',
     r'<p>\(t = 12 : 15 = 0.8\) h \(= 48\) min.</p>', ''),
    ('2d', 2, r'Lia wandert \(2\) h \(15\) min mit \(4\) km/h und rechnet \(4 \cdot 2.15 = 8.6\) km. Was ist falsch?',
     r'<p>\(15\) min sind \(15 : 60 = 0.25\) h, also \(2.25\) h, nicht \(2.15\) h. Richtig: \(4 \cdot 2.25 = 9\) km.</p>', ''),
    ('2e', 3, r'Nach einem Blitz hörst du den Donner \(3\) Sekunden später. Schall ist \(340\) m/s schnell. Wie weit ist das Gewitter entfernt? Ist die Antwort plausibel?',
     r'<p>\(s = 340 \cdot 3 = 1020\) m, also gut \(1\) km. Plausibel: Das Licht kommt fast sofort, der Schall braucht etwa \(3\) s pro km.</p>', ''),
    ('2f', 2, r'Warum teilt man durch \(3.6\), um km/h in m/s umzurechnen?',
     r'<p>\(1\) km/h heisst \(1000\) m in \(3600\) s, also \(\tfrac{1000}{3600} = \tfrac{1}{3.6}\) m/s. Darum ist der Wert in m/s \(3.6\)-mal kleiner.</p>', ''),
])
k2 = kapitel(2, 'svt', 'Weg, Geschwindigkeit, Zeit', 40,
             r'Du rechnest mit \(s = v \cdot t\) in allen drei Formen, wandelst Minuten in Stunden und km/h in m/s um und prüfst, ob das Ergebnis plausibel ist.',
             (CLIP + 'svt', 'Weg, Geschwindigkeit, Zeit'), sim2,
             (CLIP + 'kontrolle-svt', 'Kontrollfragen zu s = v · t'), fest2,
             [uebung('svt', 'Weg, Tempo oder Zeit'), uebung('umrechnen', 'Einheiten umrechnen')],
             auf2, V_MOD, komp='K2')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3" aria-label="Fahrt aus zwei Abschnitten">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg role="img" aria-label="Weg-Zeit-Graph aus zwei Abschnitten, gestrichelt der Durchschnitt"></svg>
        <table class="wt" aria-label="Tabelle der Abschnitte"></table>
        <div class="sl-row">
          {regler('s3-v1', 'v₁', 'blau', 0, 120, 50).replace('step="1"', 'step="10"')}
          {regler('s3-t1', 't₁', 'blau', 0, 3, 1).replace('step="1"', 'step="0.25"')}
        </div>
        <div class="sl-row">
          {regler('s3-v2', 'v₂', 'orange', 0, 120, 50).replace('step="1"', 'step="10"')}
          {regler('s3-t2', 't₂', 'orange', 0, 3, 1).replace('step="1"', 'step="0.25"')}
        </div>
      </figure>'''
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Fahrt in Abschnitten</div>
          <p>Velotour: \(30\) km mit \(20\) km/h, \(30\) min Pause, dann \(20\) km bergauf mit \(10\) km/h.</p>
          <table class="wt">
            <tr><th>Abschnitt</th><th>\(v\) [km/h]</th><th>\(t\) [h]</th><th>\(s\) [km]</th></tr>
            <tr><td>1</td><td>\(20\)</td><td>\(30 : 20 = 1.5\)</td><td>\(30\)</td></tr>
            <tr><td>Pause</td><td>\(0\)</td><td>\(0.5\)</td><td>\(0\)</td></tr>
            <tr><td>2</td><td>\(10\)</td><td>\(20 : 10 = 2\)</td><td>\(20\)</td></tr>
            <tr><th>total</th><td></td><td>\(4\)</td><td>\(50\)</td></tr>
          </table>
          <p>\[ \text{Durchschnitt} = \dfrac{\text{Gesamtweg}}{\text{Gesamtzeit}} = \dfrac{50}{4} = 12.5\ \text{km/h} \]</p>
          <p>Die Pause zählt zur Gesamtzeit. Im Weg-Zeit-Graphen ist der Durchschnitt die Steigung der Verbindung von Anfang und Ende.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Geschwindigkeiten gemittelt:</b> \(\dfrac{20 + 10}{2} = 15\) km/h ist falsch. Der langsame Abschnitt dauert länger und zählt darum mehr. Das Mittel stimmt nur bei gleich langen Zeiten.</p>
          <p><b>Pause vergessen:</b> Ohne Pause gäbe es \(50 : 3.5 \approx 14.3\) km/h, das ist der Schnitt nur während der Fahrt, nicht der Durchschnitt der ganzen Tour.</p>
          <p><b>Steigung falsch gelesen:</b> Im Weg-Zeit-Graphen ist der steilere Abschnitt der schnellere, nicht der längere. Die Pause ist waagrecht.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 14, [
    ('3a', 3, r'Eine Wanderung: \(12\) km mit \(4\) km/h, \(1\) h Pause, dann \(6\) km mit \(3\) km/h. Mach eine Tabelle. Wie lange dauert sie, und wie gross ist der Durchschnitt?',
     r'<p>\(3\) h, \(1\) h, \(2\) h: total \(6\) h für \(18\) km. Durchschnitt \(18 : 6 = 3\) km/h.</p>', ''),
    ('3b', 3, r'Ein Auto fährt \(60\) km mit \(120\) km/h und dann \(60\) km mit \(60\) km/h. Wie gross ist der Durchschnitt? Warum nicht \(90\) km/h?',
     r'<p>\(0.5\) h und \(1\) h, total \(120\) km in \(1.5\) h: \(80\) km/h. Der langsame Abschnitt dauert doppelt so lang und zählt darum mehr.</p>', ''),
    ('3c', 2, r'\(2\) h mit \(50\) km/h, dann \(1\) h mit \(80\) km/h. Durchschnitt?',
     r'<p>\(100 + 80 = 180\) km in \(3\) h: \(60\) km/h.</p>', ''),
    ('3d', 2, r'Eine Velotour von \(42\) km dauert \(3\) h \(30\) min. Wie gross ist die Durchschnittsgeschwindigkeit?',
     r'<p>\(42 : 3.5 = 12\) km/h.</p>', ''),
    ('3e', 2, r'Ben fährt \(120\) km hin mit \(60\) km/h und zurück mit \(40\) km/h. Er sagt: «Im Schnitt \(50\) km/h.» Prüfe.',
     r'<p>Hin \(2\) h, zurück \(3\) h: \(240\) km in \(5\) h, also \(48\) km/h. Ben hat die Geschwindigkeiten gemittelt.</p>', ''),
    ('3f', 2, r'Ein Weg-Zeit-Graph verbindet \((0 \mid 0)\), \((2 \mid 24)\), \((3 \mid 24)\) und \((4 \mid 40)\) (\(t\) in h, \(s\) in km). In welchem Abschnitt ist die Fahrt schneller? Wie gross ist der Durchschnitt, und wie siehst du ihn im Graphen?',
     r'<p>Erst \(24 : 2 = 12\) km/h, nach der Pause \(16 : 1 = 16\) km/h: Der letzte Abschnitt ist steiler, also schneller. Durchschnitt \(40 : 4 = 10\) km/h, die Steigung der Verbindung von \((0 \mid 0)\) nach \((4 \mid 40)\).</p>', ''),
])
k3 = kapitel(3, 'abschnitte', 'Fahrt in Abschnitten', 40,
             r'Du erfasst eine Bewegung mit verschiedenen Abschnitten in einer Tabelle, berechnest Gesamtzeit und Durchschnittsgeschwindigkeit und erkennst den Fehler «Geschwindigkeiten mitteln».',
             (CLIP + 'abschnitte', 'Fahrt in Abschnitten'), sim3,
             (CLIP + 'kontrolle-abschnitte', 'Kontrollfragen zu Abschnitten'), fest3,
             [uebung('durchschnitt', 'Durchschnittsgeschwindigkeit'), uebung('gesamtzeit', 'Dauer mit Pause')],
             auf3, V_MOD, komp='K3')

# ------------------------------------------------------------------ Kapitel 4
sim4 = f'''      <figure class="sim sim-gross" id="sim4" aria-label="Zwei Fahrzeuge: Begegnung oder Einholen">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <div class="sim-paar">
          <svg class="bahn" role="img" aria-label="Strecke mit den Orten von A und B"></svg>
          <svg class="graf" role="img" aria-label="Abstand der beiden über der Zeit"></svg>
        </div>
        <div class="sl-row">
          {regler('s4-D', 'Abstand am Start', 'grau', 10, 60, 40).replace('step="1"', 'step="2"')}
          <label class="sim-schalter" for="s4-r">B fährt
            <select id="s4-r" class="sim-wahl"><option value="ent" selected>auf A zu</option><option value="gleich">voraus, in dieselbe Richtung</option></select></label>
        </div>
        <div class="sl-row">
          {regler('s4-a', 'Tempo A', 'blau', 2, 30, 10)}
          {regler('s4-b', 'Tempo B', 'orange', 2, 30, 10)}
        </div>
        <div class="sl-row">
          {regler('s4-t', 'Zeit t', 'gruen', 0, 5, 0).replace('step="1"', 'step="0.1"')}
        </div>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Begegnung und Einholen</div>
          <ul class="kurz">
            <li><b>Annäherungsgeschwindigkeit:</b> um wie viel der Abstand pro Stunde kleiner wird. Dann gilt \(t = \text{Abstand} : \text{Annäherungsgeschwindigkeit}\). \(v_1\) und \(v_2\) sind die beiden Geschwindigkeiten.</li>
            <li><b>Aufeinander zu:</b> Der Abstand schrumpft mit \(v_1 + v_2\). \(36\) km, \(14\) und \(10\) km/h: \(36 : 24 = 1.5\) h. A fährt \(14 \cdot 1.5 = 21\) km.</li>
            <li><b>Einholen:</b> Ist der Hintere schneller, schrumpft der Abstand mit schneller minus langsamer. Ist er langsamer, holt er nie auf. B startet \(1\) h früher mit \(10\) km/h, A folgt mit \(15\) km/h: Vorsprung \(10\) km, \(10 : 5 = 2\) h.</li>
            <li><b>Rolltreppe</b> (\(30\) m, \(0.5\) m/s), gehen \(1\) m/s: Hier zählt die Geschwindigkeit gegenüber dem Boden: Du und die Treppe in derselben Richtung, \(1 + 0.5 = 1.5\) m/s, \(20\) s. Stehst du, sind es \(30 : 0.5 = 60\) s.</li>
          </ul>
          <p><b>Modell:</b> Gleichbleibende Geschwindigkeiten; wer später startet, lässt dem anderen einen Vorsprung. Ampeln, Steigungen und Pausen lässt das Modell weg. Ob das passt, entscheidest du für jede Aufgabe.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Bei gleicher Richtung addiert:</b> Wer \(15\) km/h fährt, holt einen mit \(10\) km/h nur mit \(5\) km/h ein, nicht mit \(25\).</p>
          <p><b>Treffpunkt in der Mitte:</b> Nur wenn beide gleichzeitig starten und gleich schnell sind. Sonst kommt der Schnellere weiter.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 14, [
    ('4a', 3, r'Zwei Orte sind \(60\) km voneinander entfernt. Von A fährt eine Velofahrerin mit \(18\) km/h los, gleichzeitig von B eine mit \(12\) km/h, aufeinander zu. Wann und wo treffen sie sich?',
     r'<p>\(60 : (18 + 12) = 2\) h. Treffpunkt \(18 \cdot 2 = 36\) km von A, also \(24\) km von B.</p>', ''),
    ('4b', 3, r'Tim startet mit \(12\) km/h. \(30\) min später fährt Lea mit \(20\) km/h hinterher. Wann holt sie ihn ein, und wie weit ist sie dann gefahren?',
     r'<p>Vorsprung \(12 \cdot 0.5 = 6\) km, Lea holt \(8\) km/h auf: \(6 : 8 = 0.75\) h nach ihrem Start. Sie ist \(20 \cdot 0.75 = 15\) km gefahren.</p>', ''),
    ('4c', 2, r'Eine Rolltreppe ist \(48\) m lang und fährt \(0.5\) m/s. Wie lange brauchst du, wenn du stehst, und wie lange, wenn du mit \(1.5\) m/s mitgehst?',
     r'<p>Stehen: \(48 : 0.5 = 96\) s. Mitgehen: \(48 : 2 = 24\) s.</p>', ''),
    ('4d', 2, r'Zwei Züge sind \(450\) km voneinander entfernt und fahren mit \(80\) km/h und \(100\) km/h aufeinander zu. Wann begegnen sie sich?',
     r'<p>\(450 : 180 = 2.5\) h.</p>', ''),
    ('4e', 2, r'Mia rechnet für «B ist \(12\) km voraus mit \(14\) km/h, A folgt mit \(18\) km/h»: \(12 : 32\) h. Was ist falsch?',
     r'<p>Beide fahren in die gleiche Richtung: A holt nur \(18 - 14 = 4\) km/h auf. Richtig: \(12 : 4 = 3\) h.</p>', ''),
    ('4f', 2, r'Zwei Velos starten gleichzeitig \(30\) km voneinander entfernt und fahren mit \(15\) und \(10\) km/h aufeinander zu. Die Rechnung gibt \(1.2\) h. Nenne zwei Annahmen des Modells und je einen Grund, warum es in Wirklichkeit anders dauern kann.',
     r'<p>Zum Beispiel: gleichbleibendes Tempo (Steigungen, Gegenwind, Ampeln bremsen), genau gleichzeitiger Start (eine wartet noch), gerade Strecke von \(30\) km (Umwege). Die echte Zeit ist darum eher länger.</p>', ''),
])
k4 = kapitel(4, 'begegnung', 'Begegnung und Einholen', 40,
             r'Du löst Begegnungs- und Einholaufgaben mit der Annäherungsgeschwindigkeit, rechnest bei der Rolltreppe mit der Geschwindigkeit gegenüber dem Boden und begründest deine Modellannahmen.',
             (CLIP + 'begegnung', 'Begegnung und Einholen'), sim4,
             (CLIP + 'kontrolle-begegnung', 'Kontrollfragen zu Begegnung und Einholen'), fest4,
             [uebung('begegnung', 'Wann und wo treffen sie sich?'), uebung('einholen', 'Einholen')],
             auf4, V_LIN, komp='K4')

# ------------------------------------------------------------------ Vorwissen
k0 = f'''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-th">Vorwissen</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Zeiten umrechnen, Gleichungen lösen, Geschwindigkeit. Zuerst kurz wiederholen, dann der Vortest.</p>
''' + r'''      <details class="anleitung">
        <summary><h3>Kurz wiederholt</h3></summary>
        <ul class="kurz">
          <li><b>Zeiten:</b> \(1\) h \(= 60\) min, \(1\) min \(= 60\) s. \(30\) min \(= 0.5\) h.</li>
          <li><b>Gleichung lösen:</b> \(3x + 5 = 17\): minus \(5\), dann durch \(3\): \(x = 4\) (Leitprogramm <a href="gleichungen-formeln.html">Bruchterme, Gleichungen und Formeln</a>).</li>
          <li><b>Geschwindigkeit:</b> Weg durch Zeit: \(120\) km in \(2\) h sind \(60\) km/h.</li>
          <li><b>Längen:</b> \(1\) km \(= 1000\) m.</li>
        </ul>
      </details>
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Wie viele Minuten sind \(0.75\) h? Wie viele Stunden sind \(90\) min?', r'<p>\(45\) min und \(1.5\) h.</p>', ''),
    ('0b', 2, r'Löse: \(4x - 3 = 21\).', r'<p>\(4x = 24\), \(x = 6\).</p>', ''),
    ('0c', 2, r'Ein Auto fährt \(150\) km in \(3\) h. Wie schnell? Wie lange braucht es für \(100\) km mit \(50\) km/h?', r'<p>\(50\) km/h und \(2\) h.</p>', ''),
    ('0d', 2, r'Berechne \(2x + 1\) für \(x = 2.5\).', r'<p>\(6\).</p>', ''),
    ('0e', 2, r'Wie viele Meter sind \(2.4\) km? Wie viele Sekunden hat eine Stunde?', r'<p>\(2400\) m und \(3600\) s.</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: «Kurz wiederholt» nochmals lesen und die Lösungen nachrechnen.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest (nur PDF)
PDF = '../downloads/leitprogramme/bewegung/'
gt = f'''
    <section class="kap" id="gesamttest">
      <div class="gesamt">
        <div class="gesamt-kopf">
          <div class="kap-meta"><span class="marker">Abschluss</span><span class="abz abz-th">Kapitel 1–4</span><span class="zeit">≈ 30 min · 25 Punkte</span></div>
          <h2 id="gesamttest-titel">Gesamttest</h2>
          <div class="pdf-weg">
            <div class="pdf-schritt"><span class="nr">1</span><div><b>Lösen</b> — auf Papier, mit Rechenweg und Antwortsätzen, ohne Taschenrechner.<br>
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
            <div class="frage"><span class="nr">V1</span><span class="txt">Ein Zug ist \(200\) m lang und fährt \(72\) km/h. Wie lange dauert es, bis er einen \(400\) m langen Tunnel ganz durchfahren hat?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\(72\) km/h \(= 20\) m/s. Die Spitze muss \(400 + 200 = 600\) m fahren, bis das Ende draussen ist: \(600 : 20 = 30\) s.</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V2</span><span class="txt">Zwei Wanderer sind \(12\) km auseinander und gehen mit je \(3\) km/h aufeinander zu. Ein Hund rennt mit \(15\) km/h zwischen ihnen hin und her, bis sie sich treffen. Wie weit rennt er?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>Sie treffen sich nach \(12 : 6 = 2\) h. So lange rennt der Hund: \(15 \cdot 2 = 30\) km. Die vielen Teilstrecken braucht es nicht.</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V3</span><span class="txt">Ein Boot fährt im stillen Wasser \(12\) km/h, der Fluss fliesst \(3\) km/h. Wie lange braucht es für \(18\) km flussabwärts und wieder zurück?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>Abwärts \(15\) km/h: \(1.2\) h. Aufwärts \(9\) km/h: \(2\) h. Zusammen \(3.2\) h, länger als ohne Strömung (\(36 : 12 = 3\) h).</p></div></details>
          </li>
        </ol>
      </div>
      <p class="ausf weiter">Weiter: Modellieren bei Mathe begreifbar: ''' + V_MOD + r'''.</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Texte, Geschwindigkeit und Begegnung, Version 1.0 (10.10.2026). Gebaut aus scripts/lp/bewegung/seite.py —
     Änderungen dort, nicht in dieser Datei. Grundlagen: HOWTO-leitprogramme.md (Kapitelmuster) und
     ~/TODO-BM-Vorkurs-LP03-15.md, Abschnitt 5 (LP 07, Mathematisieren: Texte, Geschwindigkeit und Begegnung), für die Sek I umgesetzt.

     Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026): Das Leitprogramm ist selbst die fachliche Quelle;
     Vertiefung bei Mathe begreifbar. Baut auf den Leitprogrammen Bruchterme, Gleichungen und Formeln und Funktionstypen auf.
     Notation: s = v · t, Weg s in km oder m, Zeit t in h, min oder s, Geschwindigkeit v in km/h oder m/s, Dezimalpunkt.

     Kompetenzen — eigene Formulierung, ohne Lehrplan-Nummern (CLAUDE.md: keine erfundenen Lehrplan-Stellen):
       K1  Textaufgaben strukturiert übersetzen: gegeben, gesucht, Variable mit Einheit, Gleichung, Probe, Antwortsatz
       K2  Mit s = v · t, v = s / t, t = s / v rechnen, Zeiten und km/h–m/s umrechnen, Ergebnisse plausibilisieren
       K3  Mehrteilige Bewegungen in einer Tabelle erfassen, Gesamtzeit und Durchschnittsgeschwindigkeit berechnen
       K4  Begegnung und Einholen mit der Annäherungsgeschwindigkeit lösen, Rolltreppe gegenüber dem Boden, Modellannahmen nennen

     Kompetenzmatrix (Kompetenz | Kapitel | Simulation | Übungen | Kapitelaufgaben | Gesamttest):
       K1 | 1 | Sim 1 Tarife          | tarif, raetsel           | 1a–1f | G1, G2
       K2 | 2 | Sim 2 s = v · t       | svt, umrechnen           | 2a–2f | G3, G4
       K3 | 3 | Sim 3 zwei Abschnitte | durchschnitt, gesamtzeit | 3a–3f | G5, G6
       K4 | 4 | Sim 4 Begegnung       | begegnung, einholen      | 4a–4f | G7, G8

     Planung (Kapitel | Lernziel | Erkundung | Beispiel | Häufiger Fehler | min):
       0 | Vorwissen     | –                | –                             | –                                       | 10
       1 | Text → Gl.    | Tarife vergleichen| Konto A/B, ab 11 Zahlungen   | Gleichstand als Antwort; nur eine Zahl  | 40
       2 | s = v · t     | v und t einstellen| Zug 240 km/2 h; Velo 20 min  | Minuten als Stunden; 1 h 30 = 1.30 h    | 40
       3 | Abschnitte    | zwei Abschnitte   | Velotour 12.5 km/h           | Geschwindigkeiten gemittelt; Steigung   | 40
       4 | Begegnung     | Begegnung/Einholen| 36 km 14/10; Vorsprung; Treppe| gleiche Richtung addiert; Mitte        | 40
       Gesamttest (PDF) 30 · Summe 200 min ≈ 4.4 Lektionen. Vertiefung V1–V3 freiwillig, nicht eingerechnet.

     Aus der Vorlage umgesetzt: gegeben/gesucht, Variable und Einheit, Gleichung aus Text (Kapitel 1, Hilfekarte
     Skizze → Variable → Beziehung → Gleichung → Prüfung, G1, G2), s = v · t in drei Formen (Kapitel 2, G3, G4),
     Abschnitte tabellarisch (Kapitel 3, G5, G6), Annäherungsgeschwindigkeit, Begegnung zweier Velofahrer, Rolltreppe in
     Fahrrichtung und stehend (gegen die Fahrrichtung bewusst nicht: verboten), Einholen, Modellannahmen (Kapitel 4, G7, G8), Plausibilität in jedem Kapitel. Die drei typischen
     Fehler: Zeit/Einheit (Kapitel 2), Annäherung gegen gleiche Richtung (Kapitel 4), falsche Diagrammsteigung (Kapitel 3).
     Bewusst nicht übernommen: Teams-Ablauf, Lehrpersonenteil, Prüfungsnummern.

     Clips: je Kapitel ein Einführungsclip (mit einer Vorhersagefrage) und ein Kontrollclip mit fünf Fragen,
     Reihe «Mathematisieren», bew-lp-*.json, erzeugt mit scripts/lp/bewegung/clips.py.

     Farben: A und erster Abschnitt blau, B und zweiter Abschnitt orange, Treffpunkt und Ergebnis grün, Fehler rot; Bereichsfarbe Petrol.
     Gesamttest und Bewertungspaket nur als PDF (downloads/leitprogramme/bewegung/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Sek1-Mathe begreifbar · Leitprogramm</p>
      <h1>Texte, Geschwindigkeit und Begegnung</h1>
      <p class="unter">Textaufgaben in Gleichungen übersetzen, mit Weg, Zeit und Geschwindigkeit rechnen, Begegnungen lösen. Vier Kapitel zu je einer Lektion, dazu Vorwissen und Gesamttest.</p>
    </div>
    <div class="kopf-rechts">
      <button class="themenschalter" type="button" id="themenschalter">Dunkel / Hell</button>
      <span>Mathematisieren</span>
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
      <li><a href="#k1"><span class="nr">1</span><span>Text → Gleichung</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>s = v · t</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Abschnitte</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Begegnung</span></a></li>
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
          <li>Zum Schluss der <b>Gesamttest</b> auf Papier. Alles ohne Taschenrechner.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">Das kannst du danach, alles <span class="ohm">ohne Taschenrechner</span>:</p>
        <ul>
          <li><b>K1</b> Textaufgaben Schritt für Schritt in Gleichungen übersetzen, lösen, prüfen und mit einem Antwortsatz beantworten (Kapitel 1)</li>
          <li><b>K2</b> mit \\(s = v \\cdot t\\) Weg, Geschwindigkeit oder Zeit berechnen, Einheiten umrechnen und das Ergebnis plausibilisieren (Kapitel 2)</li>
          <li><b>K3</b> Fahrten mit mehreren Abschnitten in einer Tabelle erfassen und die Durchschnittsgeschwindigkeit berechnen (Kapitel 3)</li>
          <li><b>K4</b> Begegnungs- und Einholaufgaben mit der Annäherungsgeschwindigkeit lösen und die Modellannahmen nennen (Kapitel 4)</li>
        </ul>
        <p class="rlp-quelle">Baut auf den Leitprogrammen «Bruchterme, Gleichungen und Formeln» und «Funktionstypen und Graphen» auf. Nicht in diesem Leitprogramm: beschleunigte Bewegungen, Gleichungssysteme. Zum Vertiefen bei Mathe begreifbar: ''' + V_MOD + '''.</p>
      </details>

    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Texte, Geschwindigkeit und Begegnung · Sek1-Mathe begreifbar</span>
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
<script>buildNav({{ bereich: 'lp', id: 'lp-bewegung' }});</script>
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
