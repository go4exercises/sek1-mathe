#!/usr/bin/env python3
"""
Ersetzt den Aufruf an Google Fonts durch lokal ausgelieferte Schriften.

Warum: Jeder Seitenaufruf lädt die Schriften sonst bei einem Dritten und
überträgt dabei die IP-Adresse der Besucherin. Der Fussbereich der Site sagt
«Keine Cookies · Kein Tracking» — mit lokalen Schriften stimmt das vollständig.
Nebenbei wird die Seite schneller: kein zweiter DNS-Aufschlag, keine zweite
Verbindung.

Voraussetzung: schriften.css und der Ordner schriften/ liegen im Wurzel-
verzeichnis des Repos.

    python3 scripts/schriften-lokal.py            # zeigt nur, was geändert würde
    python3 scripts/schriften-lokal.py --schreiben

Das Skript ist wiederholbar: bereits umgestellte Dateien bleiben unberührt.
"""

import argparse
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# <link ...fonts.googleapis.com/css2...> — der Stylesheet-Aufruf
GOOGLE_CSS = re.compile(
    r'[ \t]*<link[^>]*fonts\.googleapis\.com/css2[^>]*>[ \t]*\n?', re.I)
# preconnect-Zeilen zu Google, die dann nichts mehr tun
GOOGLE_PRECONNECT = re.compile(
    r'[ \t]*<link[^>]*rel=["\']preconnect["\'][^>]*fonts\.(googleapis|gstatic)\.com[^>]*>[ \t]*\n?', re.I)
SCHON_LOKAL = re.compile(r'href=["\'][^"\']*schriften\.css["\']', re.I)


def relativer_pfad(htmldatei):
    """Wie viele Ebenen tief liegt die Datei? Daraus wird ../ je Ebene."""
    tiefe = os.path.relpath(htmldatei, WURZEL).count(os.sep)
    return "../" * tiefe + "schriften.css"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schreiben", action="store_true",
                    help="Änderungen wirklich speichern")
    a = ap.parse_args()

    if not os.path.exists(os.path.join(WURZEL, "schriften.css")):
        sys.exit("schriften.css fehlt im Wurzelverzeichnis — Paket unvollständig.")

    geaendert, schon, ohne = [], [], 0
    for ordner, unter, dateien in os.walk(WURZEL):
        unter[:] = [u for u in unter
                       if u not in (".git", "node_modules", "schriften")]
        for d in sorted(dateien):
            if not d.endswith(".html"):
                continue
            pfad = os.path.join(ordner, d)
            text = open(pfad, encoding="utf-8").read()

            if not GOOGLE_CSS.search(text):
                if SCHON_LOKAL.search(text):
                    schon.append(pfad)
                else:
                    ohne += 1
                continue

            ersatz = '<link rel="stylesheet" href="%s">\n' % relativer_pfad(pfad)
            neu = GOOGLE_CSS.sub(ersatz, text, count=1)
            neu = GOOGLE_CSS.sub("", neu)          # weitere Aufrufe entfernen
            neu = GOOGLE_PRECONNECT.sub("", neu)
            geaendert.append((pfad, neu))

    print(f"{len(geaendert)} Dateien mit Google-Fonts-Aufruf")
    print(f"{len(schon)} bereits lokal")
    print(f"{ohne} ohne Schriftaufruf")

    if not geaendert:
        print("Nichts zu tun.")
        return

    for pfad, _ in geaendert[:12]:
        print("   ", os.path.relpath(pfad, WURZEL))
    if len(geaendert) > 12:
        print(f"    … und {len(geaendert) - 12} weitere")

    if not a.schreiben:
        print("\nProbelauf. Mit --schreiben werden die Änderungen gespeichert.")
        print("Vorher committen, dann siehst du im Diff genau, was passiert ist.")
        return

    for pfad, neu in geaendert:
        open(pfad, "w", encoding="utf-8").write(neu)
    print(f"\n{len(geaendert)} Dateien umgestellt.")
    print("Jetzt im Browser prüfen: Netzwerk-Tab öffnen, neu laden — es darf")
    print("keine Anfrage mehr an fonts.googleapis.com oder fonts.gstatic.com geben.")


if __name__ == "__main__":
    main()
