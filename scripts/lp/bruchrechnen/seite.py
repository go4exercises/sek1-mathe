"""Baut leitprogramme/bruchrechnen.html aus einer Kapitelbeschreibung (09.10.2026).

  python3 scripts/lp/bruchrechnen/seite.py

Leitprogramm Bruchrechnen (Bereich Arithmetik/Algebra). Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026);
vertieft wird auf den Themenseiten von Mathe begreifbar (TALS). Alles kommt aus diesem
Ordner: kopf.css (Grundgerüst der Leitprogramme, aus TALS Mathe übernommen und auf Petrol
umgestellt), seite.css, basis.js (Thema, Fortschritt, Schiene), seite.js (Simulationen, Übungen).
Nur der SEO-Block wird aus der bestehenden Seite übernommen — ihn schreibt scripts/build-seo.py.
Wiederholbar: zweimal laufen lassen ergibt dieselbe Datei. Danach Pre-Flight und build-seo.py.
"""
import json
import os

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(SP, '..', '..', '..')) + '/'
ZIEL = R + 'leitprogramme/bruchrechnen.html'
NAME = 'Bruchrechnen'
STAND = 'Stand 9. Oktober 2026'

SEO_AUF = '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->'
SEO_ZU = '<!-- SEO:ENDE -->'
seo = SEO_AUF + '\n' + SEO_ZU
if os.path.exists(ZIEL):
    alt = open(ZIEL).read()
    if SEO_AUF in alt:
        seo = alt[alt.index(SEO_AUF):alt.index(SEO_ZU) + len(SEO_ZU)]

# Vertiefung: Themenseiten von Mathe begreifbar (Berufsmaturität), in neuem Tab
TALS = 'https://mathe.begreifbar.ch/grundlagen/'
def tals(seite, text, anker=''):
    return f'<a href="{TALS}{seite}{anker}" target="_blank" rel="noopener">{text} ↗</a>'
V_ZAHLEN = tals('g1-2-zahlen-grundoperationen.html', 'Zahlen und Grundoperationen')
V_TERME = tals('g1-3-algebraische-terme.html', 'Bruchterme', '#bruchterme')
V_HIER = tals('g1-1-grundlagen.html', 'Hierarchie der Operationen', '#hierarchie')
V_BAUM = tals('g1-1-grundlagen.html', 'Strukturbaum', '#strukturbaum')


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
    """Clipzeit aus dem Drehbuch (Summe der gemessenen Szenen, ohne Nachlauf — so rechnet die Bibliothek),
    abgerundet auf Sekunden (HOWTO-leitprogramme §7)."""
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


def streifen(spec, label):
    return f'\n            <div class="mini-reihe"><svg class="mini-bruch" data-streifen="{spec}" aria-label="{label}"></svg></div>'


# ------------------------------------------------------------------ Kapitel 1
sim1 = f'''      <figure class="sim sim-gross" id="sim1" aria-label="Bruchstreifen: denselben Anteil mit anderem Nenner darstellen">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 340 142" role="img" aria-label="Zwei Bruchstreifen übereinander: oben der feste Anteil, unten dein Bruch"></svg>
        <label class="sim-schalter"><input type="checkbox" checked> Hilfslinie: wo der Anteil oben endet</label>
        <div class="sl-row">
          {regler('s1-n', 'Nenner unten', 'orange', 1, 24, 2)}
          {regler('s1-k', 'Zähler unten', 'orange', 0, 24, 1)}
        </div>
      </figure>'''
fest1 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Erweitern, Kürzen, Vergleichen</div>
          <p><b>Erweitern:</b> Zähler und Nenner mit derselben Zahl multiplizieren. Jedes Stück wird in gleich viele kleinere Stücke zerlegt — der Anteil bleibt gleich: \(\tfrac{3}{4} = \tfrac{3 \cdot 5}{4 \cdot 5} = \tfrac{15}{20}\).</p>
          <p><b>Kürzen:</b> Zähler und Nenner durch dieselbe Zahl dividieren. Ein Bruch ist <b>vollständig gekürzt</b>, wenn Zähler und Nenner keinen gemeinsamen Teiler ausser \(1\) mehr haben. Am schnellsten geht es mit dem grössten gemeinsamen Teiler:</p>
          <p>\[ \frac{12}{18} = \frac{12 : 6}{18 : 6} = \frac{2}{3} \qquad \text{denn } \text{ggT}(12;\ 18) = 6 \]</p>
          <p><b>Vergleichen:</b> Brüche auf denselben Nenner bringen, dann zeigt der Zähler, welcher grösser ist: \(\tfrac{2}{3} = \tfrac{8}{12}\) und \(\tfrac{3}{4} = \tfrac{9}{12}\), also \(\tfrac{2}{3} \lt \tfrac{3}{4}\).</p>
          <p>Ganze Zahlen sind auch Brüche: \(2 = \tfrac{2}{1} = \tfrac{6}{3}\). Ein Ergebnis wie \(\tfrac{7}{3}\) bleibt in diesem Leitprogramm ein Bruch — die gemischte Schreibweise liest man leicht als Produkt.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Kürzen nur bei Faktoren, nie bei Summanden.</b> \(\tfrac{2 + 3}{2 + 5}\) ist \(\tfrac{5}{7}\), nicht \(\tfrac{3}{5}\). Zuerst ausrechnen, dann kürzen.</p>
          <p><b>Erweitern heisst multiplizieren, nicht addieren:</b> \(\tfrac{3 + 1}{4 + 1} = \tfrac{4}{5}\) ist ein anderer Anteil als \(\tfrac{3}{4}\).</p>
          <p><b>Nur teilweise gekürzt:</b> \(\tfrac{12}{18} = \tfrac{6}{9}\) stimmt, ist aber noch nicht fertig: \(6\) und \(9\) sind beide durch \(3\) teilbar.</p>
        </div>
      </div>'''
auf1 = test('t1', 'Aufgaben · Kapitel 1', 13, [
    ('1a', 2, r'Erweitere \(\tfrac{5}{6}\) auf den Nenner \(24\). Kürze \(\tfrac{45}{60}\) vollständig.',
     r'<p>\(\tfrac{5}{6} = \tfrac{5 \cdot 4}{6 \cdot 4} = \tfrac{20}{24}\). \(\text{ggT}(45;\ 60) = 15\): \(\tfrac{45}{60} = \tfrac{3}{4}\).</p>', ''),
    ('1b', 2, r'Welche Brüche sind gleich gross wie \(\tfrac{2}{5}\)? \(\;\tfrac{4}{10}\), \(\tfrac{6}{15}\), \(\tfrac{7}{10}\), \(\tfrac{10}{25}\), \(\tfrac{3}{6}\)',
     r'<p>\(\tfrac{4}{10}\), \(\tfrac{6}{15}\) und \(\tfrac{10}{25}\) — sie lassen sich alle auf \(\tfrac{2}{5}\) kürzen. \(\tfrac{7}{10}\) und \(\tfrac{3}{6} = \tfrac{1}{2}\) nicht.</p>', ''),
    ('1c', 3, r'Ordne der Grösse nach, beginne mit dem kleinsten: \(\;\tfrac{5}{6}\), \(\tfrac{4}{5}\), \(\tfrac{7}{10}\)',
     r'<p>Gemeinsamer Nenner \(30\): \(\tfrac{5}{6} = \tfrac{25}{30}\), \(\tfrac{4}{5} = \tfrac{24}{30}\), \(\tfrac{7}{10} = \tfrac{21}{30}\). Also \(\tfrac{7}{10} \lt \tfrac{4}{5} \lt \tfrac{5}{6}\).</p>', ''),
    ('1d', 2, r'Lea kürzt so: «\(\tfrac{6 + 4}{6 + 9}\) — die \(6\) streiche ich oben und unten, also \(\tfrac{4}{9}\).» Was ist falsch? Rechne richtig.',
     r'<p>Lea kürzt Summanden. Kürzen darf man nur Faktoren. Richtig: \(\tfrac{6 + 4}{6 + 9} = \tfrac{10}{15} = \tfrac{2}{3}\) — und \(\tfrac{4}{9}\) ist kleiner als \(\tfrac{2}{3}\).</p>', ''),
    ('1e', 2, r'Warum ändert sich der Wert eines Bruchs beim Erweitern nicht? Erkläre mit dem Bruchstreifen.',
     r'<p>Beim Erweitern mit \(5\) wird jedes Stück in \(5\) gleiche kleinere Stücke zerlegt. Es gibt fünfmal so viele Stücke, und fünfmal so viele davon sind gefärbt — die gefärbte Fläche bleibt dieselbe.</p>', ''),
    ('1f', 2, r'Welcher Anteil ist gefärbt? Gib ihn vollständig gekürzt an. Wie viele Teile wären gefärbt, wenn derselbe Streifen in \(16\) Teile geteilt wäre?',
     r'<p>\(6\) von \(8\) Teilen: \(\tfrac{6}{8} = \tfrac{3}{4}\). Bei \(16\) Teilen: \(\tfrac{3}{4} = \tfrac{12}{16}\), also \(12\) Teile.</p>', streifen('8,6', 'Streifen mit 8 Teilen, davon 6 gefärbt')),
])
k1 = kapitel(1, 'erweitern-kuerzen', 'Erweitern, Kürzen, Vergleichen', 40,
             r'Du erweiterst und kürzt Brüche, kürzt vollständig mit dem grössten gemeinsamen Teiler und vergleichst Brüche, indem du sie auf denselben Nenner bringst.',
             ('t1-4-lp-erweitern', 'Erweitern, Kürzen, Vergleichen'), sim1,
             ('t1-4-lp-kontrolle-erweitern', 'Kontrollfragen zum Erweitern und Kürzen'), fest1, [uebung('erweitern', 'Erweitern'), uebung('kuerzen', 'Vollständig kürzen')],
             auf1, V_ZAHLEN, komp='K1')

# ------------------------------------------------------------------ Kapitel 2
sim2 = f'''      <figure class="sim sim-gross" id="sim2" aria-label="Bruchstreifen: eine gemeinsame Unterteilung für zwei Brüche finden">
        <div class="leiste" aria-live="polite"></div>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 340 200" role="img" aria-label="Zwei Bruchstreifen mit einer gemeinsamen Unterteilung, darunter das Ergebnis"></svg>
        <label class="sim-schalter"><input type="checkbox"> roter Streifen: «Zähler plus Zähler, Nenner plus Nenner»</label>
        <div class="sl-row">
          {regler('s2-n', 'gemeinsame Unterteilung', 'orange', 1, 24, 4)}
        </div>
      </figure>'''
fest2 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Addieren und Subtrahieren</div>
          <p><b>Gleichnamige Brüche</b> (gleicher Nenner): Zähler addieren oder subtrahieren, der Nenner bleibt. Man zählt gleich grosse Stücke: \(\tfrac{3}{8} + \tfrac{1}{8} = \tfrac{4}{8} = \tfrac{1}{2}\).</p>
          <p><b>Ungleichnamige Brüche</b> zuerst gleichnamig machen. Der kleinste gemeinsame Nenner heisst <b>Hauptnenner</b>; er ist das kleinste gemeinsame Vielfache der Nenner. Das Produkt der Nenner geht immer, ist aber oft unnötig gross.</p>
          <ol class="weg">
            <li>\(\text{kgV}(12;\ 18) = 36\) <span class="warum">Vielfache von 18: 18, 36 — und 36 ist durch 12 teilbar</span></li>
            <li>\(\dfrac{5}{12} + \dfrac{7}{18} = \dfrac{15}{36} + \dfrac{14}{36}\) <span class="warum">erweitern mit 3 und mit 2</span></li>
            <li>\(= \dfrac{29}{36}\) <span class="warum">Zähler addieren; 29 und 36 haben keinen gemeinsamen Teiler</span></li>
          </ol>
          <p>Mit einer ganzen Zahl: \(2 - \tfrac{3}{4} = \tfrac{8}{4} - \tfrac{3}{4} = \tfrac{5}{4}\). Bei drei oder mehr Brüchen braucht es einen Nenner, in dem alle aufgehen.</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Nenner addieren:</b> \(\tfrac{1}{2} + \tfrac{1}{3}\) ist nicht \(\tfrac{2}{5}\). Die Kontrolle zeigt es sofort: \(\tfrac{2}{5}\) ist kleiner als \(\tfrac{1}{2}\) — eine Summe kann nicht kleiner sein als einer ihrer positiven Summanden. Richtig: \(\tfrac{3}{6} + \tfrac{2}{6} = \tfrac{5}{6}\).</p>
          <p><b>Am Schluss nicht kürzen:</b> \(\tfrac{1}{6} + \tfrac{1}{3} = \tfrac{1}{6} + \tfrac{2}{6} = \tfrac{3}{6}\) ist erst fertig als \(\tfrac{1}{2}\).</p>
        </div>
      </div>'''
auf2 = test('t2', 'Aufgaben · Kapitel 2', 15, [
    ('2a', 3, r'Berechne und kürze: \(\tfrac{5}{12} + \tfrac{1}{12}\); \(\;\tfrac{9}{10} - \tfrac{3}{10}\); \(\;3 - \tfrac{5}{7}\)',
     r'<p>\(\tfrac{6}{12} = \tfrac{1}{2}\); \(\tfrac{6}{10} = \tfrac{3}{5}\); \(3 = \tfrac{21}{7}\), also \(\tfrac{21}{7} - \tfrac{5}{7} = \tfrac{16}{7}\).</p>', ''),
    ('2b', 3, r'Berechne: \(\tfrac{3}{4} + \tfrac{5}{6}\)',
     r'<p>Hauptnenner \(12\): \(\tfrac{9}{12} + \tfrac{10}{12} = \tfrac{19}{12}\). Vollständig gekürzt, denn \(19\) ist eine Primzahl.</p>', ''),
    ('2c', 3, r'Berechne: \(\tfrac{11}{12} - \tfrac{4}{9}\)',
     r'<p>\(\text{kgV}(12;\ 9) = 36\): \(\tfrac{33}{36} - \tfrac{16}{36} = \tfrac{17}{36}\).</p><p class="komm">Mit dem Produkt \(108\) als Nenner geht es auch, aber dann muss am Schluss gekürzt werden: \(\tfrac{51}{108} = \tfrac{17}{36}\).</p>', ''),
    ('2d', 2, r'Tim rechnet \(\tfrac{2}{3} + \tfrac{1}{4} = \tfrac{3}{7}\). Zeige ohne Rechnung, dass das nicht stimmen kann. Rechne dann richtig.',
     r'<p>\(\tfrac{3}{7}\) ist kleiner als \(\tfrac{1}{2}\), also auch kleiner als \(\tfrac{2}{3}\) allein — die Summe zweier positiver Brüche muss aber grösser sein als \(\tfrac{2}{3}\). Richtig: \(\tfrac{8}{12} + \tfrac{3}{12} = \tfrac{11}{12}\).</p>', ''),
    ('2e', 2, r'Die Streifen zeigen \(\tfrac{1}{3}\) und \(\tfrac{1}{5}\). Warum darf man bei \(\tfrac{2}{15} + \tfrac{4}{15}\) die Zähler direkt addieren, bei \(\tfrac{1}{3} + \tfrac{1}{5}\) aber nicht?',
     r'<p>Fünfzehntel sind gleich grosse Stücke — man zählt einfach, wie viele es sind. Drittel und Fünftel sind verschieden gross; erst wenn beide in Fünfzehntel zerlegt sind (\(\tfrac{5}{15}\) und \(\tfrac{3}{15}\)), darf man zählen: \(\tfrac{8}{15}\).</p>',
     streifen('3,1;5,1', 'Zwei Streifen: einer in Drittel geteilt mit einem gefärbten Teil, einer in Fünftel geteilt mit einem gefärbten Teil')),
    ('2f', 2, r'Drei Brüche: \(\tfrac{1}{2} + \tfrac{2}{3} - \tfrac{3}{4}\)',
     r'<p>Hauptnenner \(\text{kgV}(2;\ 3;\ 4) = 12\): \(\tfrac{6}{12} + \tfrac{8}{12} - \tfrac{9}{12} = \tfrac{5}{12}\).</p><p class="komm">Bei drei Brüchen geht es gleich: ein Nenner, in dem alle drei aufgehen.</p>', ''),
])
k2 = kapitel(2, 'addieren', 'Addieren und Subtrahieren', 45,
             r'Du addierst und subtrahierst Brüche, indem du sie mit dem Hauptnenner gleichnamig machst, und gibst das Ergebnis vollständig gekürzt an.',
             ('t1-4-lp-addieren', 'Addieren und Subtrahieren'), sim2,
             ('t1-4-lp-kontrolle-addieren', 'Kontrollfragen zum Addieren und Subtrahieren'), fest2, [uebung('hauptnenner', 'Hauptnenner finden'), uebung('addsub', 'Addieren und Subtrahieren')],
             auf2, V_ZAHLEN + ' · ' + V_TERME, komp='K2')

# ------------------------------------------------------------------ Kapitel 3
sim3 = f'''      <figure class="sim sim-gross" id="sim3" aria-label="Multiplizieren im Flächenmodell, Dividieren durch Messen">
        <div class="leiste" aria-live="polite"></div>
        <label class="sim-schalter">Modell <select class="sim-wahl" aria-label="Rechenart">
          <option value="mal" selected>Mal: Flächenmodell</option>
          <option value="durch">Durch: Wie oft passt es?</option>
        </select></label>
        <div class="sim-formel" data-rolle="formel" aria-live="polite"></div>
        <svg viewBox="0 0 340 250" role="img" aria-label="Einheitsquadrat mit zwei gefärbten Anteilen oder Streifen mit gemessenen Stücken"></svg>
        <div class="sl-row">
          {regler('s3-a', 'Zähler 1', 'blau', 1, 8, 1)}
          {regler('s3-b', 'Nenner 1', 'blau', 1, 8, 2)}
        </div>
        <div class="sl-row">
          {regler('s3-c', 'Zähler 2', 'orange', 1, 8, 1)}
          {regler('s3-d', 'Nenner 2', 'orange', 1, 8, 3)}
        </div>
      </figure>'''
fest3 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Multiplizieren und Dividieren</div>
          <p><b>Multiplizieren:</b> Zähler mal Zähler, Nenner mal Nenner. Im Flächenmodell ist das Produkt das grüne Rechteck: \(\tfrac{2}{3} \cdot \tfrac{3}{4} = \tfrac{6}{12} = \tfrac{1}{2}\).</p>
          <p><b>Vor dem Ausrechnen kürzen</b> spart Arbeit — auch über Kreuz, also Zähler des einen mit Nenner des anderen Bruchs:</p>
          <p>\[ \frac{4}{9} \cdot \frac{3}{8} = \frac{\cancel{4}^{\,1} \cdot \cancel{3}^{\,1}}{\cancel{9}_{\,3} \cdot \cancel{8}_{\,2}} = \frac{1}{6} \]</p>
          <p>Ganze Zahl mal Bruch: Nur der Zähler wird multipliziert, \(3 \cdot \tfrac{2}{5} = \tfrac{6}{5}\). «\(\tfrac{2}{3}\) von \(12\)» heisst \(\tfrac{2}{3} \cdot 12 = 8\).</p>
          <p><b>Dividieren:</b> Mit dem <b>Kehrwert</b> des zweiten Bruchs multiplizieren (Zähler und Nenner vertauscht):</p>
          <p>\[ \frac{a}{b} : \frac{c}{d} = \frac{a}{b} \cdot \frac{d}{c} \qquad (b,\ c,\ d \neq 0) \]</p>
          <p>Auch eine ganze Zahl hat einen Kehrwert: \(2 = \tfrac{2}{1}\), Kehrwert \(\tfrac{1}{2}\). Also \(\tfrac{4}{5} : 2 = \tfrac{4}{5} \cdot \tfrac{1}{2} = \tfrac{2}{5}\).</p>
          <p>Warum: \(\tfrac{3}{4} : \tfrac{1}{8}\) fragt «Wie oft passt \(\tfrac{1}{8}\) in \(\tfrac{3}{4}\)?» — sechsmal, denn \(\tfrac{3}{4} = \tfrac{6}{8}\). Und \(\tfrac{3}{4} \cdot 8 = 6\): Teilen durch \(\tfrac{1}{8}\) ist dasselbe wie mal \(8\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Kehrwert vom falschen Bruch:</b> Bei \(\tfrac{3}{4} : \tfrac{1}{8}\) wird \(\tfrac{1}{8}\) umgedreht. Wer \(\tfrac{4}{3} \cdot \tfrac{1}{8} = \tfrac{1}{6}\) rechnet, hat den ersten umgedreht.</p>
          <p><b>Über Kreuz kürzen nur beim Multiplizieren.</b> Bei \(\tfrac{4}{9} + \tfrac{3}{8}\) darf man nicht über Kreuz kürzen — dort braucht es den Hauptnenner.</p>
          <p><b>Beim Multiplizieren braucht es keinen gemeinsamen Nenner</b> — gleichnamig machen ist nur beim Addieren und Subtrahieren nötig.</p>
        </div>
      </div>'''
auf3 = test('t3', 'Aufgaben · Kapitel 3', 16, [
    ('3a', 4, r'Berechne und kürze vollständig: \(\tfrac{5}{6} \cdot \tfrac{3}{10}\) und \(\tfrac{3}{5} : \tfrac{9}{10}\)',
     r'<p>Über Kreuz: \(5\) und \(10\) durch \(5\), \(3\) und \(6\) durch \(3\): \(\tfrac{1 \cdot 1}{2 \cdot 2} = \tfrac{1}{4}\). Und \(\tfrac{3}{5} \cdot \tfrac{10}{9} = \tfrac{30}{45} = \tfrac{2}{3}\).</p>', ''),
    ('3b', 4, r'Ganze Zahlen und Brüche: \(4 \cdot \tfrac{5}{6}\); \(\;\tfrac{2}{3}\) von \(15\); \(\;\tfrac{7}{8} : 7\); \(\;6 : \tfrac{3}{4}\)',
     r'<p>\(\tfrac{20}{6} = \tfrac{10}{3}\); \(\tfrac{2}{3} \cdot 15 = \tfrac{30}{3} = 10\); \(\tfrac{7}{8} \cdot \tfrac{1}{7} = \tfrac{1}{8}\); \(6 \cdot \tfrac{4}{3} = 8\).</p><p class="komm">Kontrolle zur letzten: \(\tfrac{3}{4}\) passt achtmal in \(6\), denn \(8 \cdot \tfrac{3}{4} = 6\).</p>', ''),
    ('3c', 2, r'Nora rechnet \(\tfrac{2}{5} : \tfrac{4}{7} = \tfrac{5}{2} \cdot \tfrac{4}{7} = \tfrac{20}{14} = \tfrac{10}{7}\). Finde den Fehler und rechne richtig.',
     r'<p>Nora hat den Kehrwert vom ersten Bruch genommen. Umgedreht wird der zweite: \(\tfrac{2}{5} \cdot \tfrac{7}{4} = \tfrac{14}{20} = \tfrac{7}{10}\).</p><p class="komm">Ihr Ergebnis \(\tfrac{10}{7}\) ist genau der Kehrwert des richtigen — ein typisches Zeichen für diesen Fehler.</p>', ''),
    ('3d', 2, r'Warum ist \(\tfrac{5}{6} \cdot \tfrac{3}{5}\) kleiner als \(\tfrac{5}{6}\), aber \(\tfrac{5}{6} : \tfrac{3}{5}\) grösser als \(\tfrac{5}{6}\)?',
     r'<p>Mal \(\tfrac{3}{5}\) heisst: \(\tfrac{3}{5}\) von \(\tfrac{5}{6}\) nehmen — das ist nur ein Teil davon: \(\tfrac{1}{2}\). Durch \(\tfrac{3}{5}\) fragt, wie oft \(\tfrac{3}{5}\) in \(\tfrac{5}{6}\) passt; das Stück ist kleiner, also passt es mehr als einmal: \(\tfrac{25}{18}\).</p>', ''),
    ('3e', 2, r'Welche Multiplikation zeigt das Flächenmodell? Lies das Ergebnis ab und kürze.',
     r'<p>Blau sind \(\tfrac{3}{4}\) der Breite, orange \(\tfrac{2}{5}\) der Höhe: \(\tfrac{3}{4} \cdot \tfrac{2}{5}\). Grün sind \(6\) von \(20\) Kästchen: \(\tfrac{6}{20} = \tfrac{3}{10}\).</p>',
     '\n            <div class="mini-reihe"><svg class="mini-bruch" data-flaeche="3,4,2,5" aria-label="Quadrat: 3 von 4 Spalten blau, 2 von 5 Zeilen orange, Überlappung grün"></svg></div>'),
    ('3f', 2, r'Lena hat \(\tfrac{5}{4}\) kg Mehl. Ein Rezept braucht \(\tfrac{3}{8}\) kg. (a) Für wie viele ganze Rezepte reicht das Mehl? Zeichne dazu einen Streifen in Achteln. (b) Wie viel Mehl sind \(\tfrac{2}{5}\) ihres Vorrats?',
     r'<p>(a) Wie oft passt \(\tfrac{3}{8}\) in \(\tfrac{5}{4}\)? \(\tfrac{5}{4} : \tfrac{3}{8} = \tfrac{5}{4} \cdot \tfrac{8}{3} = \tfrac{10}{3}\) — dreimal ganz (es bleiben \(\tfrac{1}{8}\) kg). Im Streifen: \(\tfrac{5}{4} = \tfrac{10}{8}\), also zehn Achtel; je drei Achtel sind ein Rezept — drei Gruppen, ein Achtel bleibt. (b) «von» heisst mal: \(\tfrac{2}{5} \cdot \tfrac{5}{4} = \tfrac{1}{2}\) kg.</p>', ''),
])
k3 = kapitel(3, 'multiplizieren', 'Multiplizieren und Dividieren', 45,
             r'Du multiplizierst Brüche, dividierst mit dem Kehrwert, kürzt vor dem Ausrechnen und erklärst beides am Bild.',
             ('t1-4-lp-malnehmen', 'Multiplizieren und Dividieren'), sim3,
             ('t1-4-lp-kontrolle-malnehmen', 'Kontrollfragen zum Multiplizieren und Dividieren'), fest3, [uebung('mal', 'Multiplizieren'), uebung('durch', 'Dividieren')],
             auf3, V_ZAHLEN + ' · ' + V_TERME, komp='K3')

# ------------------------------------------------------------------ Kapitel 4
sim4 = '''      <figure class="sim schrittwaehler" id="sim4" aria-label="Schrittwähler: das Rechenzeichen wählen, das zuerst dran ist, und den Schritt ausrechnen">
        <div class="leiste" aria-live="polite"></div>
        <div class="sw-verlauf" aria-live="polite"></div>
        <p class="sw-frage"></p>
        <div class="sw-feld"></div>
        <div class="sw-rueck" aria-live="polite"></div>
        <div class="sw-werkzeug"><button type="button" class="sw-neu">↶ von vorn</button></div>
      </figure>'''
fest4 = r'''      <div class="festhalten">
        <div class="merk">
          <div class="titel">Rechenreihenfolge und Vorzeichen</div>
          <ol>
            <li><b>Klammern</b> zuerst, innere vor äusseren.</li>
            <li><b>Potenzen</b>.</li>
            <li><b>Punkt vor Strich:</b> \(\cdot\) und \(:\) vor \(+\) und \(-\).</li>
            <li>Gleichrangiges <b>von links nach rechts</b>.</li>
          </ol>
          <p>Eine Rechnung, eine Kette — jeder Schritt eine Zeile:</p>
          <p>\[ \frac{1}{2} - \frac{1}{3} \cdot \left(\frac{3}{4} - \frac{1}{4}\right) = \frac{1}{2} - \frac{1}{3} \cdot \frac{1}{2} = \frac{1}{2} - \frac{1}{6} = \frac{3}{6} - \frac{1}{6} = \frac{2}{6} = \frac{1}{3} \]</p>
          <h4>Negative Brüche</h4>
          <p>Das Minus darf vor dem Bruch, im Zähler oder im Nenner stehen: \(-\tfrac{2}{3} = \tfrac{-2}{3} = \tfrac{2}{-3}\). Gerechnet wird mit den Vorzeichenregeln aus ℤ: \(\left(-\tfrac{3}{4}\right) \cdot \left(-\tfrac{2}{9}\right) = +\tfrac{6}{36} = \tfrac{1}{6}\).</p>
          <p>Minus einer negativen Zahl heisst plus: \(\tfrac{1}{2} - \left(-\tfrac{1}{4}\right) = \tfrac{1}{2} + \tfrac{1}{4} = \tfrac{3}{4}\).</p>
          <h4>Potenzen von Brüchen</h4>
          <p>Zähler und Nenner werden potenziert: \(\left(\tfrac{2}{3}\right)^2 = \tfrac{4}{9}\). Auf die Klammer kommt es an: \(\left(-\tfrac{1}{2}\right)^2 = \tfrac{1}{4}\), aber \(-\left(\tfrac{1}{2}\right)^2 = -\tfrac{1}{4}\).</p>
        </div>
        <div class="warn">
          <div class="titel">Häufiger Fehler</div>
          <p><b>Minus vor der Klammer:</b> \(\tfrac{3}{4} - \left(\tfrac{1}{2} - \tfrac{1}{4}\right) = \tfrac{3}{4} - \tfrac{1}{4} = \tfrac{1}{2}\). Wer die Klammer einfach weglässt, rechnet \(\tfrac{3}{4} - \tfrac{1}{2} - \tfrac{1}{4} = 0\) — falsch. Ohne Klammer: \(\tfrac{3}{4} - \tfrac{1}{2} + \tfrac{1}{4}\).</p>
          <p><b>Von links nach rechts</b> gilt auch für \(:\) und \(\cdot\): \(1 : \tfrac{1}{2} \cdot \tfrac{1}{2} = 2 \cdot \tfrac{1}{2} = 1\), nicht \(1 : \tfrac{1}{4} = 4\).</p>
          <p><b>Ergebnis nicht gekürzt</b> — auch im Zwischenschritt lohnt sich das Kürzen, die Zahlen bleiben kleiner.</p>
        </div>
      </div>'''
auf4 = test('t4', 'Aufgaben · Kapitel 4', 16, [
    ('4a', 3, r'Berechne: \(\tfrac{7}{12} - \tfrac{1}{4} \cdot \tfrac{2}{3}\)',
     r'<p>Punkt vor Strich: \(\tfrac{1}{4} \cdot \tfrac{2}{3} = \tfrac{2}{12} = \tfrac{1}{6}\). Dann \(\tfrac{7}{12} - \tfrac{2}{12} = \tfrac{5}{12}\).</p>', ''),
    ('4b', 3, r'Berechne: \(\left(\tfrac{3}{4} - \tfrac{1}{3}\right) : \tfrac{5}{6}\)',
     r'<p>Klammer: \(\tfrac{9}{12} - \tfrac{4}{12} = \tfrac{5}{12}\). Dann \(\tfrac{5}{12} \cdot \tfrac{6}{5} = \tfrac{30}{60} = \tfrac{1}{2}\).</p>', ''),
    ('4c', 3, r'Berechne: \(-\tfrac{2}{5} + \tfrac{3}{10} \cdot \left(-\tfrac{4}{3}\right)\)',
     r'<p>Punkt vor Strich: \(\tfrac{3}{10} \cdot \left(-\tfrac{4}{3}\right) = -\tfrac{12}{30} = -\tfrac{2}{5}\). Dann \(-\tfrac{2}{5} + \left(-\tfrac{2}{5}\right) = -\tfrac{4}{5}\).</p>', ''),
    ('4d', 2, r'Berechne beide und vergleiche: \(\left(-\tfrac{3}{2}\right)^2 - \tfrac{3}{4}\) und \(-\left(\tfrac{3}{2}\right)^2 + \tfrac{3}{4}\)',
     r'<p>\(\tfrac{9}{4} - \tfrac{3}{4} = \tfrac{6}{4} = \tfrac{3}{2}\) und \(-\tfrac{9}{4} + \tfrac{3}{4} = -\tfrac{6}{4} = -\tfrac{3}{2}\). Die beiden Ergebnisse sind Gegenzahlen.</p>', ''),
    ('4e', 3, r'Mia rechnet: \(\tfrac{3}{4} : \tfrac{3}{8} \cdot \tfrac{1}{2} = \tfrac{3}{4} : \tfrac{3}{16} = 4\). Welche Regel hat sie verletzt? Rechne richtig.',
     r'<p>\(:\) und \(\cdot\) sind gleichrangig — von links nach rechts. Mia hat zuerst multipliziert. Richtig: \(\tfrac{3}{4} : \tfrac{3}{8} = \tfrac{3}{4} \cdot \tfrac{8}{3} = 2\), dann \(2 \cdot \tfrac{1}{2} = 1\).</p>', ''),
    ('4f', 2, r'Warum ist \(\left(-\tfrac{2}{3}\right) \cdot \left(-\tfrac{3}{4}\right)\) positiv, \(-\tfrac{2}{3} + \left(-\tfrac{3}{4}\right)\) aber negativ?',
     r'<p>Beim Multiplizieren gilt: Minus mal Minus gibt Plus, also \(+\tfrac{6}{12} = \tfrac{1}{2}\). Beim Addieren kommt zu einer negativen Zahl noch eine negative dazu — man geht zweimal in die Minusrichtung: \(-\tfrac{8}{12} - \tfrac{9}{12} = -\tfrac{17}{12}\).</p>', ''),
])
k4 = kapitel(4, 'reihenfolge', 'Rechenreihenfolge und negative Brüche', 45,
             r'Du berechnest Terme mit Brüchen und negativen Zahlen in der richtigen Reihenfolge — Klammern, Potenzen, Punkt vor Strich, von links nach rechts —, schreibst jeden Schritt auf und gibst das Ergebnis vollständig gekürzt an.',
             ('t1-4-lp-reihenfolge', 'Rechenreihenfolge und negative Brüche'), sim4,
             ('t1-4-lp-kontrolle-reihenfolge', 'Kontrollfragen zur Rechenreihenfolge'), fest4, [uebung('reihenfolge', 'Was kommt zuerst?'), uebung('vorzeichen', 'Negative Brüche')],
             auf4, V_HIER + ' · ' + V_BAUM, komp='K4')

# ------------------------------------------------------------------ Vorwissen
k0 = f'''
    <section class="kap" id="k0">
      <div class="kap-meta"><span class="marker">Kapitel 0</span><span class="abz abz-th">Vorwissen</span><span class="zeit">≈ 10 min</span></div>
      <h2 id="vorwissen">Vorwissen</h2>
      <p class="ziel">Teiler und Vielfache, Rechnen mit negativen Zahlen, Punkt vor Strich, Potenzen. Zuerst kurz wiederholen, dann der Vortest.</p>
''' + r'''      <details class="anleitung">
        <summary><h3>Kurz wiederholt</h3></summary>
        <ul class="kurz">
          <li><b>ggT</b> (grösster gemeinsamer Teiler): die grösste Zahl, durch die beide teilbar sind, zum Beispiel \(\text{ggT}(12;\ 18) = 6\). Braucht es zum Kürzen.</li>
          <li><b>kgV</b> (kleinstes gemeinsames Vielfaches): die kleinste Zahl, die durch beide teilbar ist, zum Beispiel \(\text{kgV}(4;\ 6) = 12\). Braucht es zum Addieren.</li>
          <li><b>Vorzeichen:</b> Plus mal Plus und Minus mal Minus gibt Plus, verschiedene Vorzeichen geben Minus; gleich beim Dividieren. Minus einer negativen Zahl ist plus: \(5 - (-2) = 7\).</li>
          <li><b>Reihenfolge:</b> Klammern, Potenzen, Punkt vor Strich, sonst von links nach rechts.</li>
          <li><b>Potenz:</b> \(2^3 = 2 \cdot 2 \cdot 2\). Bei \(-3^2\) gehört das Quadrat nur zur \(3\): \(-9\).</li>
        </ul>
      </details>
''' + test('t0', 'Vortest', 10, [
    ('0a', 2, r'Bestimme den grössten gemeinsamen Teiler von \(16\) und \(40\) und das kleinste gemeinsame Vielfache von \(6\) und \(10\).',
     r'<p>\(\text{ggT}(16;\ 40) = 8\); \(\text{kgV}(6;\ 10) = 30\).</p><p class="komm">ggT braucht Kapitel 1 (Kürzen), kgV Kapitel 2 (Hauptnenner).</p>', ''),
    ('0b', 2, r'Berechne: \((-2) \cdot 3\); \(\;(-12) : (-4)\); \(\;-5 + 8\); \(\;3 - 7\); \(\;3 - (-7)\)',
     r'<p>\(-6\); \(3\); \(3\); \(-4\); \(10\).</p><p class="komm">Dieselben Vorzeichenregeln gelten in Kapitel 4 für Brüche.</p>', ''),
    ('0c', 2, r'Berechne: \(12 : 3 \cdot 2\) und \(2 + 3 \cdot 4\)',
     r'<p>\(12 : 3 \cdot 2 = 4 \cdot 2 = 8\) (von links nach rechts); \(2 + 3 \cdot 4 = 2 + 12 = 14\) (Punkt vor Strich).</p>', ''),
    ('0d', 2, r'Welcher Anteil des Streifens ist gefärbt, welcher nicht?',
     r'<p>Gefärbt \(\tfrac{3}{8}\), nicht gefärbt \(\tfrac{5}{8}\) — zusammen \(\tfrac{8}{8} = 1\), das Ganze.</p>', streifen('8,3', 'Streifen mit 8 Teilen, davon 3 gefärbt')),
    ('0e', 2, r'Berechne: \(2^3\); \(\;(-3)^2\); \(\;-3^2\)',
     r'<p>\(8\); \(9\); \(-9\).</p><p class="komm">Bei \(-3^2\) gehört das Quadrat nur zur \(3\) — Potenz vor Strich.</p>', ''),
]) + '''
      <p class="komm">Weniger als 7 von 10 Punkten: «Kurz wiederholt» nochmals lesen, die Lösungen des Vortests Schritt für Schritt nachrechnen, dann Kapitel 1.</p>
    </section>'''

# ------------------------------------------------------------------ Gesamttest
PDF = '../downloads/leitprogramme/bruchrechnen/'
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
            <tr><td>17 – 21 P</td><td>Den schwächsten Teil nochmals — gemessen am Anteil (Teil A 7, B 6, C 12 P): Tüfteln und Übungen der Kapitel dieses Teils.</td></tr>
            <tr><td>11 – 16 P</td><td>Zurück zu den Kapiteln aller Aufgaben, in denen du Punkte verloren hast.</td></tr>
            <tr><td>0 – 10 P</td><td>Zurück zu den Kapiteln jedes Teils, in dem du weniger als die Hälfte erreicht hast; sind es alle drei, zum Vortest und zu Kapitel 1.</td></tr>
          </table>
          <p>Aufgabe → Kapitel: G1 → 1; G2 → 2; G3 → 1 und 2; G4, G5 → 3; G6 bis G9 → 4</p>
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
            <div class="frage"><span class="nr">V1</span><span class="txt">Berechne \(\tfrac{1}{2} + \tfrac{1}{4} + \tfrac{1}{8} + \tfrac{1}{16}\). Wie viel fehlt bis \(1\)? Was fehlt, wenn du so immer weiter addierst?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\(\tfrac{8}{16} + \tfrac{4}{16} + \tfrac{2}{16} + \tfrac{1}{16} = \tfrac{15}{16}\); es fehlt \(\tfrac{1}{16}\) — genau der letzte Summand. Mit jedem weiteren Summanden halbiert sich der Rest; er wird beliebig klein, aber nie null.</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V2</span><span class="txt">Finde zwei verschiedene Stammbrüche (Zähler \(1\)), deren Summe \(\tfrac{1}{2}\) ist. Gibt es mehr als eine Möglichkeit?</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\(\tfrac{1}{3} + \tfrac{1}{6} = \tfrac{2}{6} + \tfrac{1}{6} = \tfrac{1}{2}\). Das ist die einzige Möglichkeit: Der grössere Stammbruch muss grösser als \(\tfrac{1}{4}\) und kleiner als \(\tfrac{1}{2}\) sein — es bleibt nur \(\tfrac{1}{3}\). (\(\tfrac{1}{4} + \tfrac{1}{4}\) sind nicht verschieden.)</p></div></details>
          </li>
          <li>
            <div class="frage"><span class="nr">V3</span><span class="txt">Welcher Bruch ist grösser: \(\tfrac{2025}{2026}\) oder \(\tfrac{2026}{2027}\)? Begründe ohne den gemeinsamen Nenner auszurechnen.</span></div>
            <details class="loes"><summary>Lösung</summary><div class="inhaltbox"><p>\(\tfrac{2025}{2026} = 1 - \tfrac{1}{2026}\) und \(\tfrac{2026}{2027} = 1 - \tfrac{1}{2027}\). Weil \(\tfrac{1}{2027}\) kleiner ist als \(\tfrac{1}{2026}\), fehlt dem zweiten Bruch weniger bis \(1\): \(\tfrac{2026}{2027}\) ist grösser.</p></div></details>
          </li>
        </ol>
      </div>
      <p class="ausf weiter">Weiter: Was hier bewusst fehlt — Brüche und Dezimalzahlen umwandeln, periodische Dezimalzahlen — steht bei Mathe begreifbar unter ''' + V_ZAHLEN + r'''. Brüche mit Variablen: ''' + V_TERME + r'''.</p>
    </section>'''

oben = '''<div id="nav-root"></div>
<!-- Leitprogramm Bruchrechnen, Version 1.0 (09.10.2026, freigeschaltet am selben Tag). Gebaut aus scripts/lp/bruchrechnen/seite.py —
     Änderungen dort, nicht in dieser Datei. Grundlagen: HOWTO-leitprogramme.md (Kapitelmuster) und
     ~/HOWTO-TODO-BM-Vorkurs-LP01-02.md, Abschnitt 4 (LP 01 Bruchrechnen), für die Sek I umgesetzt.

     Sek1-Mathe hat keine Themenseiten (Entscheid 09.10.2026): Das Leitprogramm ist selbst die fachliche Quelle;
     Vertiefungslinks zeigen auf Mathe begreifbar (TALS). Notation nach STYLEGUIDE.md und CLAUDE.md: Dezimalpunkt, ggT/kgV mit Strichpunkt, Kehrwert,
     Hauptnenner, «vollständig gekürzt», negative Brüche mit Minus vor dem Bruch, Ergebnisse als
     (unechter) Bruch statt gemischter Zahl.

     Kompetenzen — eigene Formulierung, ohne Lehrplan-Nummern (CLAUDE.md: keine erfundenen Lehrplan-Stellen):
       K1  Brüche erweitern, vollständig kürzen und vergleichen
       K2  Brüche addieren und subtrahieren (Hauptnenner)
       K3  Brüche multiplizieren und dividieren (Kehrwert, vorher kürzen)
       K4  Terme mit Brüchen und negativen Zahlen in der richtigen Reihenfolge berechnen,
           Ergebnis vollständig gekürzt, Schritte begründen und Fehler finden
     Alles ohne Taschenrechner.

     Kompetenzmatrix (Kompetenz | Kapitel | Simulation | Übungen | Kapitelaufgaben | Gesamttest):
       K1 | 1 | Sim 1 | erweitern, kuerzen      | 1a–1f | G1, G3
       K2 | 2 | Sim 2 | hauptnenner, addsub     | 2a–2f | G2, G3
       K3 | 3 | Sim 3 | mal, durch              | 3a–3f | G4, G5
       K4 | 4 | Sim 4 | reihenfolge, vorzeichen | 4a–4f | G6–G9

     Planung (Kapitel | Lernziel | Erkundung | Beispiel | Häufiger Fehler | min):
       0 | Vorwissen          | –                          | –                    | –                               | 10
       1 | erweitern/kürzen   | Bruchstreifen nachbauen    | 12/18 = 2/3          | Summanden kürzen; addieren      | 40
       2 | addieren           | gemeinsame Unterteilung    | 5/12 + 7/18 = 29/36  | Nenner addieren (1/2+1/3 ≠ 2/5) | 45
       3 | mal/durch          | Flächenmodell, Messen      | 4/9 · 3/8 = 1/6      | Kehrwert vom falschen Bruch     | 45
       4 | Reihenfolge        | Schrittwähler              | Kette mit Klammer    | Minus vor Klammer; links→rechts | 45
       Gesamttest (PDF) 30 · Summe 215 min ≈ 4.8 Lektionen: vier Kapitel zu je einer Lektion, dazu
       Vorwissen und Gesamttest. Vertiefung V1–V3 freiwillig, nicht eingerechnet.

     Aus der BM-Vorlage übernommen: Kompetenzen «Das kannst du danach», Vorwissen mit Verweisen,
     Erkundung mit Entscheidung statt Lesen, Fehlerbeispiel mit Diagnosefrage je Kapitel (1d, 2d, 3c, 4e),
     Feedback nach Fehlertyp, Tipps in drei Stufen (Impuls → nächster Schritt → Lösungsweg),
     «vollständig gekürzt» getrennt bewertet, Vertiefung getrennt vom Pflichtpfad.
     Bewusst nicht übernommen: Teams-/Flipped-Classroom-Ablauf, Kernpfad für die erste Doppellektion,
     Prüfungsanker der BM-Aufnahmeprüfung, Dezimalkomma als Alternative, Lehrpersonenmaterial.

     Clips: je Kapitel ein Einführungsclip (mit einer Vorhersagefrage) und ein Kontrollclip mit fünf Fragen,
     Reihe «Brüche sehen», t1-4-lp-*.json, erzeugt mit scripts/lp/bruchrechnen/clips.py (probe: nicht in der
     Bibliothek). Die Erkundungen benutzen andere Zahlen als Clip und Festhalten (HOWTO §15).
     Muster je Kapitel: ① Clip → ② Tüfteln (Aufgabenleiste) → ③ Kontrollclip → Festhalten → ④ Üben → ⑤ Aufgaben.

     Farben: erster Bruch blau, zweiter Bruch orange, Ergebnis grün, Fehler rot; Bereichsfarbe Petrol.
     Gesamttest und Bewertungspaket nur als PDF (downloads/leitprogramme/bruchrechnen/*.tex). -->
<header class="kopf">
  <div class="kopf-innen">
    <div>
      <p class="marke">Sek1-Mathe begreifbar · Leitprogramm</p>
      <h1>Bruchrechnen</h1>
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
      <li><a href="#k1"><span class="nr">1</span><span>Erweitern, Kürzen</span></a></li>
      <li><a href="#k2"><span class="nr">2</span><span>Addieren</span></a></li>
      <li><a href="#k3"><span class="nr">3</span><span>Mal und durch</span></a></li>
      <li><a href="#k4"><span class="nr">4</span><span>Reihenfolge</span></a></li>
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
          <li><b>④ Üben</b> mit Rückmeldung, bis drei in Folge sitzen. Mit <b>💡 Tipp</b> bekommst du Hilfe in drei Stufen.</li>
          <li><b>⑤ Aufgaben</b> auf Papier mit Rechenweg, dann Lösung aufklappen und abhaken.</li>
          <li>Zum Schluss der <b>Gesamttest</b> auf Papier. Alles ohne Taschenrechner.</li>
        </ol>
      </details>
      <details class="anleitung kompetenzen">
        <summary><h2 id="kompetenzen">Kompetenzen</h2></summary>
        <p class="rlp-quelle">Das kannst du danach — alles <span class="ohm">ohne Taschenrechner</span>:</p>
        <ul>
          <li><b>K1</b> Brüche erweitern, vollständig kürzen und der Grösse nach vergleichen — Kapitel 1</li>
          <li><b>K2</b> Brüche addieren und subtrahieren, mit dem Hauptnenner — Kapitel 2</li>
          <li><b>K3</b> Brüche multiplizieren und dividieren, mit dem Kehrwert und Kürzen vor dem Ausrechnen — Kapitel 3</li>
          <li><b>K4</b> Terme mit Brüchen und negativen Zahlen in der richtigen Reihenfolge berechnen, jeden Schritt begründen und Fehler in fremden Lösungen finden — Kapitel 4</li>
        </ul>
        <p class="rlp-quelle">Nicht in diesem Leitprogramm: Brüche und Dezimalzahlen umwandeln, periodische Dezimalzahlen, Doppelbrüche — zum Vertiefen bei Mathe begreifbar: ''' + V_ZAHLEN + '''.</p>
      </details>
    </div>
'''
unten = '''
    <div class="fuss">
      <span>Leitprogramm Bruchrechnen · Sek1-Mathe begreifbar</span>
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
    tex: { inlineMath: [['\\(','\\)']], displayMath: [['\\[','\\]']], packages: {'[+]': ['cancel']} },
    loader: { load: ['[tex]/cancel'] },
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
<script>buildNav({{ bereich: 'lp', id: 'lp-bruchrechnen' }});</script>
</body>
</html>
'''
# Zeiten (09.10.2026, mit Clips, nach der Prüfung): Vorwissen 10 · K1 40 · K2 45 · K3 45 · K4 45 · Gesamttest 30 = 215 min
body = oben + k0 + k1 + k2 + k3 + k4 + gt + vt + unten
seite = (kopf + open(SP + 'kopf.css').read() + open(SP + 'seite.css').read() + '</style>\n</head>\n<body>\n' + body + '\n'
         + mathjax + open(SP + 'basis.js').read() + '\n</script>\n' + open(SP + 'seite.js').read() + '\n' + fuss)
os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
open(ZIEL, 'w').write(seite)
print('geschrieben', ZIEL, len(seite.splitlines()), 'Zeilen')
