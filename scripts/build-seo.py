#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
#  TALS Mathe — Auffindbarkeit: Seiten-Metadaten, sitemap.xml, robots.txt
#
#  Schreibt in jede Seite einen generierten Kopfblock zwischen den Marken
#      <!-- SEO:ANFANG … -->  …  <!-- SEO:ENDE -->
#  (Beschreibung, canonical, Favicons, Open Graph, JSON-LD nach schema.org).
#  Der Block wird bei jedem Lauf ersetzt — von Hand aendert man ihn nie,
#  sondern die Tabelle SEITEN weiter unten.
#
#  Die JSON-LD-Daten folgen schema.org/LearningResource (LRMI). Die
#  RLP-Kompetenzen werden direkt aus der Seite gelesen (.rlp-kompetenzen li),
#  damit Metadaten und sichtbarer Inhalt nicht auseinanderlaufen.
#
#  Schwesterprojekt: TALS Physik hat dieselbe Mechanik (Commit fc4ed40).
#  Aenderungen an Aufbau oder Feldern gehoeren dort ebenfalls hin —
#  Eintrag in TODO-schwesterprojekt.md.
#
#  Aufruf vom Repo-Root:
#      python3 scripts/build-seo.py             # schreiben
#      python3 scripts/build-seo.py --check     # Gatter: Exit 1, wenn veraltet
#      python3 scripts/build-seo.py --dry-run   # Trockenlauf: zeigt, was sich
#                                               # aendern wuerde; Exit immer 0
#      python3 scripts/build-seo.py --dry-run --diff   # dazu die Zeilen selbst
#
#  --check und --dry-run unterscheiden sich in der Absicht: --check ist das
#  Gatter fuer den Pre-Flight und interessiert sich nur fuer den Exit-Code,
#  --dry-run ist zum Hinschauen, bevor man 58 Dateien anfasst.
#
#  Unbekannte Schalter brechen ab, statt durchzufallen. Frueher schrieb ein
#  `--help` die Metadaten, weil nur auf '--check' in argv geprueft wurde.
#
#  Achtung, zwei Laeufe: dateModified und lastmod kommen aus dem Git-Datum der
#  jeweiligen Datei. Ein Commit, der eine Seite anfasst, macht damit deren
#  eigenen Block um eine Generation veraltet. Nach dem Commit also noch einmal
#  laufen lassen und die Datumsaenderung mitcommitten — danach ist es stabil.
# ─────────────────────────────────────────────────────────────

import argparse
import difflib
import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIS = 'https://sek1-mathe.begreifbar.ch/'
SEITENNAME = 'Sek1-Mathe begreifbar'
AUTOR = 'Raphael Arnold Kohler'
LIZENZ = 'https://creativecommons.org/licenses/by-nc/4.0/deed.de'
STAND = '2026-10-09'

# Bereiche — Quelle: nav.js (GROUPS)
BEREICHE = {'1': 'Bereich 1 Arithmetik/Algebra',
            '2': 'Bereich 2 Gleichungen',
            '3': 'Bereich 3 Geometrie'}

# ── Seiten-Tabelle: hier wird gepflegt ───────────────────────────────
# beschreibung: 140–165 Zeichen, eigenstaendig lesbar, mit den Suchbegriffen,
#               die jemand tatsaechlich eingibt.
# themen:       Stichworte fuer schema.org/about
# titel:        nur setzen, wo der <title> der Seite mehrdeutig ist.
# Die Beschreibungen der Themenseiten sind Platzhalter, bis die Seite steht.
SEITEN = {
 'index.html': dict(
   typ='website',
   titel='Sek1-Mathe begreifbar — Leitprogramme Mathematik für die Sekundarstufe I',
   beschreibung='Kostenlose Leitprogramme Mathematik für die Sekundarstufe I: selbstständig lernen mit Clips, Animationen, Übungen mit Rückmeldung und Gesamttest — zuerst Bruchrechnen.',
   themen=['Mathematik', 'Sekundarstufe I', 'Leitprogramm', 'Bruchrechnen', 'Selbststudium']),
 'glossar.html': dict(
   typ='article', lrt='Glossar',
   titel='Glossar — mathematische Begriffe von A bis Z',
   beschreibung='Mathematik-Glossar für die Sekundarstufe I: die zentralen Begriffe von A bis Z kurz erklärt, jeweils mit Formel und Verweis auf das passende Leitprogramm.',
   themen=['Mathematik', 'Glossar', 'Fachbegriffe', 'Sekundarstufe I']),
 'clips.html': dict(
   typ='article', lrt='Erklärclip',
   titel='Clips — kurze Animationen zu den Rechenwegen',
   beschreibung='Kurze Animationen zur Mathematik der Sekundarstufe I: Ein Clip baut einen Rechenweg Zeile für Zeile auf, mit Farbführung und Text zum Mitlesen.',
   themen=['Mathematik', 'Erklärclip', 'Animation', 'Sekundarstufe I', 'Rechenweg']),
 'leitprogramme.html': dict(
   typ='article', lrt='Leitprogramm', noindex=True,       # seit 09.10.2026 Weiterleitung auf die Startseite
   titel='Leitprogramme — selbstständig durch ein Thema',
   beschreibung='Leitprogramme zur Mathematik der Sekundarstufe I: Ein Thema in Kapiteln zum selbstständigen Durcharbeiten, mit Vorwissenstest, Beispielen, Aufgaben und Gesamttest.',
   themen=['Mathematik', 'Leitprogramm', 'Selbststudium', 'Sekundarstufe I']),
 'formelsammlung.html': dict(
   typ='article', lrt='Formelsammlung',
   titel='Formelsammlung Mathematik Sek I — alle Formeln nach Bereichen',
   beschreibung='Alle Formeln der Mathematik für die Sekundarstufe I auf einer Seite: Arithmetik und Algebra, Gleichungen und Geometrie, geordnet nach den Bereichen.',
   themen=['Mathematik', 'Formelsammlung', 'Formeln', 'Sekundarstufe I']),
 'rechtliches.html': dict(
   typ='website',
   titel='Rechtliches & Datenschutz',
   beschreibung='Verantwortlichkeit, Haftung, Lizenz und Datenschutz von Sek1-Mathe begreifbar — ohne Cookies, ohne Tracking, alle Inhalte unter CC BY-NC 4.0.',
   themen=['Impressum', 'Datenschutz', 'Lizenz']),
 'feedback.html': dict(
   typ='website',
   titel='Kontakt & Feedback',
   beschreibung='Fehler melden, Verbesserungen vorschlagen oder Rückmeldung geben zu Sek1-Mathe begreifbar — ohne Anmeldung, Name und E-Mail freiwillig.',
   themen=['Kontakt', 'Feedback']),

 # ── Leitprogramme ─────────────────────────────────────────────────
 # Freigeschaltet am 09.10.2026 (Entscheid Auftraggeber; Hörprobe und KI-Test nach §15 folgen).
 'leitprogramme/bruchrechnen.html': dict(
   typ='article', lrt='Leitprogramm',
   titel='Leitprogramm Bruchrechnen — erweitern, kürzen, addieren, multiplizieren, dividieren',
   beschreibung='Leitprogramm Bruchrechnen, Sekundarstufe I: erweitern und kürzen, Hauptnenner, mal und durch mit dem Kehrwert, Rechenreihenfolge, negative Brüche — mit Übungen.',
   themen=['Mathematik', 'Bruchrechnen', 'Brüche', 'Kürzen', 'Hauptnenner', 'Kehrwert', 'Rechenreihenfolge', 'Leitprogramm', 'Sekundarstufe I']),
 'leitprogramme/terme-faktorisieren.html': dict(
   typ='article', lrt='Leitprogramm',
   titel='Leitprogramm Terme und Faktorisieren — vereinfachen, ausmultiplizieren, binomische Formeln',
   beschreibung='Leitprogramm Terme und Faktorisieren, Sekundarstufe I: zusammenfassen, Klammern auflösen, Klammer mal Klammer, binomische Formeln, ausklammern, Zweiklammersatz — mit Übungen.',
   themen=['Mathematik', 'Terme', 'Klammern', 'Ausmultiplizieren', 'Binomische Formeln', 'Faktorisieren', 'Ausklammern', 'Leitprogramm', 'Sekundarstufe I']),
 'leitprogramme/gleichungen-formeln.html': dict(
   typ='article', lrt='Leitprogramm',
   titel='Leitprogramm Bruchterme, Gleichungen und Formeln — kürzen, Hauptnenner, Gleichungen lösen, Formeln umstellen',
   beschreibung='Leitprogramm Sekundarstufe I: Bruchterme kürzen und berechnen, lineare Gleichungen mit Klammern und Brüchen lösen, Lösungsmenge und Probe, Formeln umstellen — mit Übungen.',
   themen=['Mathematik', 'Bruchterme', 'Kürzen', 'Hauptnenner', 'Lineare Gleichungen', 'Lösungsmenge', 'Formeln umstellen', 'Leitprogramm', 'Sekundarstufe I']),
 'leitprogramme/darstellungen.html': dict(
   typ='article', lrt='Leitprogramm',
   titel='Leitprogramm Darstellungen wechseln — Text, Gleichung, Tabelle und Graph, Definitionsbereich, antiproportional',
   beschreibung='Leitprogramm Sekundarstufe I, lineare Funktionen II: zwischen Text, Gleichung, Wertetabelle und Graph wechseln, konstanter Umfang, Definitionsbereich und Achsen, linear fallend oder antiproportional — mit Übungen.',
   themen=['Mathematik', 'Lineare Funktionen', 'Darstellungswechsel', 'Wertetabelle', 'Definitionsbereich', 'Achsen', 'Antiproportional', 'Leitprogramm', 'Sekundarstufe I']),
 'leitprogramme/lineare-funktionen.html': dict(
   typ='article', lrt='Leitprogramm',
   titel='Leitprogramm Lineare Funktionen — Anfangswert, Steigung, Geraden zeichnen, Gleichung aufstellen',
   beschreibung='Leitprogramm Sekundarstufe I: lineare Funktionen y = m·x + b mit Anfangswert und Änderung, Steigungsdreieck, Geraden zeichnen, Nullstelle, Gleichung aus Graph, zwei Punkten und Sachverhalt — mit Übungen.',
   themen=['Mathematik', 'Lineare Funktionen', 'Steigung', 'Steigungsdreieck', 'Gerade', 'Nullstelle', 'Geradengleichung', 'Leitprogramm', 'Sekundarstufe I']),

}

MARKE_AUF = '<!-- SEO:ANFANG — generiert von scripts/build-seo.py, nicht von Hand ändern -->'
MARKE_ZU = '<!-- SEO:ENDE -->'

MAKROS = {'cdot': '·', 'Delta': 'Δ', 'delta': 'δ', 'lambda': 'λ', 'alpha': 'α',
          'beta': 'β', 'gamma': 'γ', 'rho': 'ρ', 'omega': 'ω', 'pi': 'π', 'mu': 'µ',
          'circ': '°', 'approx': '≈', 'cdots': '…', 'times': '×',
          'frac': '/', 'tfrac': '/', 'dfrac': '/',   # Rueckfall, s. bruch_auf()
          'mathbb': '', 'mathbf': '', 'longmapsto': '↦', 'longrightarrow': '→',
          'Longleftrightarrow': '⇔', 'Rightarrow': '⇒', 'leq': '≤', 'geq': '≥',
          'neq': '≠', 'in': '∈', 'sqrt': '√', 'varphi': 'φ', 'setminus': '\\',
          'log': 'log', 'ln': 'ln', 'lg': 'lg', 'sin': 'sin', 'cos': 'cos', 'tan': 'tan',
          'vec': '', 'text': '', 'mathrm': '', 'left': '', 'right': '', 'quad': ' '}


def bruch_auf(x):
    """\\frac{a}{b} zu a/b aufloesen, von innen nach aussen.

    Ohne das wird aus \\tfrac{1}{2} erst «/{1}{2}» und dann «12» — in
    Metadaten ist das eine falsche Zahl, kein Bruch.
    """
    muster = re.compile(r'\\[dt]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}')
    for _ in range(4):
        x, n = muster.subn(r'\1/\2', x)
        if not n:
            break
    return x


def tex_weg(t):
    """LaTeX aus Fliesstext in lesbaren Klartext ueberfuehren."""
    def innen(m):
        x = bruch_auf(m.group(1))
        x = re.sub(r'\\[ ,;:!]', ' ', x)            # LaTeX-Abstaende
        x = re.sub(r'\^\s*\\circ', '°', x)         # ^\circ C -> °C, nicht ^°C
        x = re.sub(r'\\([a-zA-Z]+)', lambda k: MAKROS.get(k.group(1), ' '), x)
        # ^ und _ bleiben stehen: ohne sie wird aus a^x ein «ax» und aus
        # log_a(b) ein «a(b)» — in Metadaten waere das schlicht falsch.
        return re.sub(r'[{}$]', '', x).replace('\\', '')
    t = re.sub(r'\\\((.*?)\\\)', innen, t, flags=re.S)
    t = re.sub(r'<[^>]+>', '', t)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()


def kompetenzen(seite_html):
    # bis zum Ende der Liste lesen — das erste </div> schliesst nur .rlp-titel
    m = re.search(r'<div class="rlp-kompetenzen">(.*?)</ul>', seite_html, re.S)
    if not m:
        return []
    return [tex_weg(li) for li in re.findall(r'<li>(.*?)</li>', m.group(1), re.S)]


def titel_von(seite_html):
    m = re.search(r'<title>(.*?)</title>', seite_html, re.S)
    return html.unescape(re.sub(r'\s+', ' ', m.group(1))).strip() if m else ''


def git_datum(pfad):
    try:
        d = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', pfad],
                           cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return d or STAND
    except Exception:
        return STAND


def fach_lg(datei):
    """Bereich aus dem Dateinamen ableiten (themen/t<Bereich>-…)."""
    name = os.path.basename(datei)
    if datei.startswith('themen/'):
        return 'Mathematik Sekundarstufe I', BEREICHE.get(name[1], '')
    return '', ''


def jsonld(url, cfg, titel, komp, ist_thema):
    person = {'@type': 'Person', 'name': AUTOR}
    knoten = {
        '@type': ['LearningResource', 'WebPage'] if ist_thema else 'WebPage',
        '@id': url + '#inhalt',
        'url': url,
        'name': titel,
        'description': cfg['beschreibung'],
        'inLanguage': 'de-CH',
        'isAccessibleForFree': True,
        'license': LIZENZ,
        'creator': person,
        'publisher': person,
        'dateModified': cfg['datum'],
        'isPartOf': {'@id': BASIS + '#website'},
    }
    if cfg.get('themen'):
        knoten['about'] = [{'@type': 'DefinedTerm', 'name': t} for t in cfg['themen']]
        knoten['keywords'] = ', '.join(cfg['themen'])
    if ist_thema or cfg.get('lrt'):
        knoten['learningResourceType'] = cfg.get('lrt', ['Lerneinheit', 'interaktive Simulation', 'Aufgabensammlung'])
        knoten['educationalLevel'] = 'Sekundarstufe I (Schweiz)'
        knoten['typicalAgeRange'] = '12-16'
        knoten['audience'] = {'@type': 'EducationalAudience',
                              'educationalRole': ['student', 'teacher']}
        knoten['interactivityType'] = 'active'
    if komp:
        knoten['teaches'] = komp
    if cfg.get('tg'):
        knoten['educationalAlignment'] = [{
            '@type': 'AlignmentObject',
            'alignmentType': 'teaches',
            'educationalFramework': SEITENNAME,
            'targetName': f"{cfg['fach']} · {cfg['lg']} · {cfg['tg']}",
        }]
    graph = [knoten]

    if cfg['datei'] == 'index.html':
        graph.append({
            '@type': 'WebSite', '@id': BASIS + '#website', 'url': BASIS,
            'name': SEITENNAME, 'inLanguage': 'de-CH', 'license': LIZENZ,
            'publisher': person,
            'potentialAction': {
                '@type': 'SearchAction',
                'target': {'@type': 'EntryPoint', 'urlTemplate': BASIS + '?q={search_term_string}'},
                'query-input': 'required name=search_term_string',
            },
        })
    else:
        graph.append({'@type': 'WebSite', '@id': BASIS + '#website', 'url': BASIS, 'name': SEITENNAME})

    if ist_thema:
        graph.append({
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': SEITENNAME, 'item': BASIS},
                {'@type': 'ListItem', 'position': 2, 'name': cfg['fach']},
                {'@type': 'ListItem', 'position': 3, 'name': cfg['lg']},
                {'@type': 'ListItem', 'position': 4, 'name': cfg.get('tg', titel), 'item': url},
            ],
        })
    return {'@context': 'https://schema.org', '@graph': graph}


def block(datei, cfg, seite_html):
    tief = datei.count('/')
    auf = '../' * tief
    url = BASIS + datei
    titel = cfg.get('titel') or titel_von(seite_html)
    ist_thema = datei.startswith('themen/')
    komp = kompetenzen(seite_html) if ist_thema else []
    fach, lg = fach_lg(datei)
    cfg = dict(cfg, datei=datei, datum=git_datum(datei), fach=fach, lg=lg)
    b = cfg['beschreibung']
    z = [MARKE_AUF,
         f'<meta name="description" content="{html.escape(b, quote=True)}">',
         f'<meta name="author" content="{AUTOR}">']
    # Unverlinkte Seite: nur ueber den Direktlink erreichbar. Das Weglassen aus
    # der Sitemap allein genuegt dafuer nicht — eine Suchmaschine, die die URL
    # anderswoher kennt (geteilter Link, Referrer, Browserleiste), indexiert sie
    # trotzdem. Erst das robots-Meta haelt sie draussen. "nofollow" dazu, damit
    # von hier aus auch die eingebetteten Clipdateien nicht aufgenommen werden;
    # die stehen aus demselben Grund nicht in der Sitemap.
    if cfg.get('noindex'):
        z.append('<meta name="robots" content="noindex, nofollow">')
    z += [
         f'<link rel="canonical" href="{url}">',
         f'<link rel="icon" href="{auf}favicon.svg" type="image/svg+xml">',
         f'<link rel="icon" href="{auf}favicon-32.png" sizes="32x32" type="image/png">',
         f'<link rel="apple-touch-icon" href="{auf}apple-touch-icon.png">',
         f'<meta property="og:type" content="{cfg.get("typ", "article")}">',
         f'<meta property="og:site_name" content="{SEITENNAME}">',
         '<meta property="og:locale" content="de_CH">',
         f'<meta property="og:title" content="{html.escape(titel, quote=True)}">',
         f'<meta property="og:description" content="{html.escape(b, quote=True)}">',
         f'<meta property="og:url" content="{url}">',
         f'<meta property="og:image" content="{BASIS}og-bild.png">',
         '<meta name="twitter:card" content="summary_large_image">',
         '<script type="application/ld+json">',
         json.dumps(jsonld(url, cfg, titel, komp, ist_thema), ensure_ascii=False, indent=1),
         '</script>',
         MARKE_ZU]
    return '\n'.join(z)


def einsetzen(datei, cfg):
    pfad = os.path.join(ROOT, datei)
    s = open(pfad, encoding='utf-8').read()
    neu = block(datei, cfg, s)
    if MARKE_AUF in s:
        s2 = re.sub(re.escape(MARKE_AUF) + r'.*?' + re.escape(MARKE_ZU), lambda _: neu, s, flags=re.S)
    else:
        m = re.search(r'</title>\n?', s)
        assert m, f'{datei}: kein <title>'
        s2 = s[:m.end()] + neu + '\n' + s[m.end():]
    return s, s2


def zeilenbilanz(alt, neu):
    """Wie viele Zeilen kaemen dazu, wie viele fielen weg."""
    plus = minus = 0
    for z in difflib.unified_diff(alt.splitlines(), neu.splitlines(), lineterm='', n=0):
        if z.startswith('+') and not z.startswith('+++'):
            plus += 1
        elif z.startswith('-') and not z.startswith('---'):
            minus += 1
    return plus, minus


def sitemap():
    eintraege = []
    for datei in SEITEN:
        if SEITEN[datei].get('noindex'):
            continue
        eintraege.append((BASIS + datei, git_datum(datei),
                          '1.0' if datei == 'index.html' else
                          '0.8' if datei.startswith('leitprogramme/') else '0.5'))   # Leitprogramme sind die Inhaltsseiten
    z = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, datum, prio in eintraege:
        z += ['  <url>', f'    <loc>{url}</loc>', f'    <lastmod>{datum}</lastmod>',
              f'    <priority>{prio}</priority>', '  </url>']
    z.append('</urlset>')
    return '\n'.join(z) + '\n'


ROBOTS = f"""# {SEITENNAME} — alles darf indexiert werden.
User-agent: *
Allow: /

Sitemap: {BASIS}sitemap.xml
"""


def main(argv):
    ap = argparse.ArgumentParser(
        prog='build-seo.py',
        description='Setzt die generierten Kopfbloecke in die Seiten und schreibt '
                    'sitemap.xml und robots.txt. Gepflegt wird die Tabelle SEITEN '
                    'im Skript, nie der Block in der Seite.',
        epilog='Ohne Schalter wird geschrieben.')
    modus = ap.add_mutually_exclusive_group()
    modus.add_argument('--check', action='store_true',
                       help='nur pruefen, nichts schreiben; Exit 1, wenn etwas veraltet ist '
                            '(so ruft der Pre-Flight das Skript auf)')
    modus.add_argument('--dry-run', action='store_true',
                       help='Trockenlauf: zeigt, was sich aendern wuerde, und schreibt nichts')
    ap.add_argument('--diff', action='store_true',
                    help='nur mit --dry-run: zusaetzlich die betroffenen Zeilen zeigen')
    a = ap.parse_args(argv)
    if a.diff and not a.dry_run:
        ap.error('--diff gibt es nur zusammen mit --dry-run')

    schreiben = not (a.check or a.dry_run)
    aenderungen = []                         # (Name, alter Stand, neuer Stand)

    for datei, cfg in SEITEN.items():
        alt, neu = einsetzen(datei, cfg)
        if alt != neu:
            aenderungen.append((datei, alt, neu))
            if schreiben:
                open(os.path.join(ROOT, datei), 'w', encoding='utf-8').write(neu)

    for name, inhalt in (('sitemap.xml', sitemap()), ('robots.txt', ROBOTS)):
        pfad = os.path.join(ROOT, name)
        alt = open(pfad, encoding='utf-8').read() if os.path.exists(pfad) else ''
        if alt != inhalt:
            aenderungen.append((name, alt, inhalt))
            if schreiben:
                open(pfad, 'w', encoding='utf-8').write(inhalt)

    namen = [n for n, _, _ in aenderungen]

    if a.check:
        if aenderungen:
            print('SEO-Metadaten VERALTET:', ', '.join(namen))
            return 1
        print(f'SEO-Metadaten aktuell ({len(SEITEN)} Seiten).')
        return 0

    if a.dry_run:
        if not aenderungen:
            print(f'[Trockenlauf] nichts zu tun — {len(SEITEN)} Seiten, sitemap.xml '
                  f'und robots.txt sind aktuell.')
            return 0
        print(f'[Trockenlauf] nichts geschrieben. {len(aenderungen)} Datei(en) '
              f'wuerden sich aendern:')
        for name, alt, neu in aenderungen:
            plus, minus = zeilenbilanz(alt, neu)
            print(f'  {name:<52s} +{plus} / -{minus} Zeilen')
            if a.diff:
                for z in difflib.unified_diff(
                        alt.splitlines(), neu.splitlines(),
                        fromfile=name + '  (jetzt)', tofile=name + '  (neu)',
                        lineterm='', n=1):
                    print('    ' + z)
        return 0

    print(f'{len(SEITEN)} Seiten mit Metadaten versehen, sitemap.xml und robots.txt geschrieben.')
    if aenderungen:
        print('  geändert:', ', '.join(namen))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
