"""
Bibliotheksseite clips.html — Mathe-Fassung (Auftrag 06.10.2026).

Grundstruktur wie bisher: Fach, darin Lerngebiet als aufklappbare Gruppe.
Innerhalb eines Lerngebiets je Themenseite eine dreispaltige Tabelle:

    Animationen          Clips mit `animation` (erklären eine Animation der Themenseite)
    Leitprogramm         die eigenen Clips der sichtbaren Leitprogramme ("probe": true,
                         nicht in clips.json), in der Reihenfolge des Leitprogramms
    Weitere Clips        alle übrigen Clips der Themenseite

Ein Clip der Bibliothek, den ein Leitprogramm mitbenutzt, bleibt in Spalte 1 oder 3:
Spalte 2 zeigt nur, was es ausserhalb der Leitprogramme sonst nirgends gibt.

Sichtbar sind die Leitprogramme, die leitprogramme.html vor dem Abschnitt der alten
Leitprogramme verlinkt; deren Prüfungsclips (Übungsprüfung, Trigo 2) bleiben draussen.

Aufgerufen von scripts/build-clips-einbau.py (Funktion block_bibliothek). Dieses
Modul gibt es nur in Mathe; build-clips-einbau.py bleibt dadurch nahe an der
Physik-Fassung (scripts/abgleich.py, KERN).
"""

import html
import json
import os
import re


# Reihen, die vor der Liste REIHEN in build-clips-einbau.py stehen — ihre Ordnung folgt dem
# Aufbau der Themenseite, nicht dem Alphabet (sonst «Binome» vor «Klammern»). Gilt für die
# Bibliothek und die Clipblöcke der Themenseiten.
REIHEN_VORN = ["Mengen", "Zahlenmengen", "Zahlformen", "Zahlenbrüche", "Prozent",   # 1.2
               "Klammern", "Binome", "Faktorisieren", "Bruchterme",                   # 1.3
               "Zehnerpotenzen", "Einheiten", "Runden", "Potenzen"]                   # 1.4

def sichtbare_leitprogramme(wurzel):
    """Leitprogramm-Dateien in der Reihenfolge von leitprogramme.html, ohne die alten."""
    text = open(os.path.join(wurzel, "leitprogramme.html"), encoding="utf-8").read()
    ende = text.find("<!-- ALTE LEITPROGRAMME")
    if ende > 0:
        text = text[:ende]
    aus = []
    for name in re.findall(r'href="leitprogramme/([a-z0-9-]+\.html)"', text):
        if name not in aus:
            aus.append(name)
    return aus


def lp_clips(wurzel, clipsdir):
    """Eigene Clips der sichtbaren Leitprogramme: Liste von Einträgen wie in clips.json,
    dazu `lp` (Datei des Leitprogramms) und `folge` = Platz im Leitprogramm."""
    aus, gesehen = [], set()
    for lp in sichtbare_leitprogramme(wurzel):
        pfad = os.path.join(wurzel, "leitprogramme", lp)
        if not os.path.exists(pfad):
            continue
        platz = 0
        text = open(pfad, encoding="utf-8").read()
        # Je Clip die Animation seines Kapitels: die Simulation (figure.sim#simN) im selben
        # <section class="kap">; ohne Simulation der Anfang des Kapitels.
        ziel = {}
        for teil in re.split(r'(?=<section class="kap" id=")', text):
            m = re.match(r'<section class="kap" id="([^"]+)"', teil)
            if not m:
                continue
            sim = re.search(r'<figure class="sim[^"]*" id="([^"]+)"', teil)
            for st in re.findall(r'clips/([A-Za-z0-9-]+)\.html', teil):
                ziel.setdefault(st, sim.group(1) if sim else m.group(1))
        for stamm in re.findall(r'clips/([A-Za-z0-9-]+)\.html', text):
            if stamm in gesehen:
                continue
            dreh_pfad = os.path.join(clipsdir, stamm + ".json")
            if not os.path.exists(dreh_pfad):
                continue
            dreh = json.load(open(dreh_pfad, encoding="utf-8"))
            gesehen.add(stamm)
            if not dreh.get("probe"):
                continue                       # Bibliotheksclip: steht in Spalte 1 oder 3
            platz += 1
            lek = dreh.get("lektion") or []
            aus.append({
                "datei": stamm + ".html",
                "titel": dreh.get("titel", ""),
                "lektion": [lek] if isinstance(lek, str) else list(lek),
                "reihe": dreh.get("reihe", ""),
                "folge": platz,
                # so rechnet build-clips.py `dauer_s`: Summe der Szenen, gerundet
                "dauer_s": round(sum(s.get("dauer") or 0 for s in dreh.get("szenen", []))),
                "lp": lp,
                "lplink": f"leitprogramme/{lp}#{ziel.get(stamm, '')}".rstrip("#"),
            })
    return aus


def block_bibliothek(alle, seiten, e):
    """e = das Modul build-clips-einbau (Hilfsfunktionen und Marken)."""
    wurzel = e.WURZEL
    lpc = lp_clips(wurzel, e.CLIPS)
    gruppen = e.lerngebiete()
    nach_lektion = {}
    for c in list(alle) + lpc:
        for code in e.codes(c):
            nach_lektion.setdefault(code, []).append(c)

    aus = [e.BIB_AUF]
    benannt = set()
    fach_titel = {"grundlagen": "Grundlagenfach", "schwerpunkt": "Schwerpunktfach"}
    offen = None
    gesamt = 0
    for bereich, nr, titel, ids in gruppen:
        # je Clip eine Themenseite in diesem Lerngebiet: die erste eigene
        je_seite, gesehen = {}, set()
        for code in ids:
            for c in nach_lektion.get(code, []):
                if c["datei"] in gesehen:
                    continue
                gesehen.add(c["datei"])
                je_seite.setdefault(code, []).append(c)
        drin = [c for code in ids for c in je_seite.get(code, [])]
        if not drin:
            continue
        if offen != bereich:
            if offen is not None:
                aus.append("</div>")
            anker = fach_titel[bereich].lower().replace("ü", "ue")
            aus.append(f'<h2 id="{anker}">{fach_titel[bereich]}</h2>')
            kl = "cl-liste" + (" cl-sp" if bereich == "schwerpunkt" else "")
            aus.append(f'<div class="{kl}">')
            offen = bereich
        dauer = sum(c.get("dauer_s", 0) for c in drin)
        gesamt += len(drin)
        kid = f"{bereich[0]}{nr}"
        aus += [
            '<div class="cl-kap">',
            f'  <button class="cl-hdr" type="button" aria-expanded="false"'
            f' aria-controls="cl-{kid}" onclick="togClips(\'{kid}\')">',
            f'    <span class="cl-nr">{nr}</span>',
            f'    <span class="cl-name">{html.escape(titel)}</span>',
            f'    <span class="cl-anz">{len(drin)} '
            f'{"Clip" if len(drin) == 1 else "Clips"} · {e.mmss(dauer)}</span>',
            '    <span class="cl-tog" aria-hidden="true">▼</span>',
            '  </button>',
            f'  <div class="cl-body" id="cl-{kid}" hidden>',
        ]
        for code in ids:
            clips = je_seite.get(code)
            if not clips:
                continue
            seite = seiten.get(code, {})
            anim = sorted([c for c in clips if c.get("animation")], key=e.ordnung)
            lp = [c for c in clips if c.get("lp")]
            rest = sorted([c for c in clips if not c.get("animation") and not c.get("lp")],
                          key=e.ordnung)
            nuance = e.nuancen_zuteilen(anim + lp + rest)
            lps = sorted({c["lp"] for c in lp})
            lp_kopf = ("Leitprogramm" if len(lps) != 1 else
                       f'<a href="leitprogramme/{lps[0]}">Leitprogramm</a>')
            aus.append('    <div class="cl-seite">')
            aus.append('      <h3 class="cl-gt"><span class="cl-gnr">'
                       + e.lektionsnummer(code) + '</span>'
                       + (f'<a href="{seite["url"]}">{html.escape(seite["titel"])}</a>'
                          if seite else html.escape(code)) + '</h3>')
            aus.append('      <div class="cl-tabelle">')
            for kopf, spalte in (("Animationen", anim), (lp_kopf, lp), ("Weitere Clips", rest)):
                aus.append('        <div class="cl-spalte">')
                aus.append(f'          <p class="cl-sk">{kopf}</p>')
                if not spalte:
                    aus.append('          <p class="cl-keine">—</p>')
                for c in spalte:
                    stamm = c["datei"].replace(".html", "")
                    anker = None if stamm in benannt else "clip-" + stamm
                    benannt.add(stamm)
                    zz = e.zeile(c, "", nuance[c.get("reihe") or c["titel"]], anker=anker,
                                 animlink=(seite["url"] + "#" + c["animation"])
                                 if c.get("animation") and seite else None)
                    if c.get("lplink"):
                        # wie «Anim» bei den Clips der Themenseiten: Link auf die Animation
                        # des Kapitels im Leitprogramm, die nach dem Clip folgt
                        zz[0] = zz[0].replace('<div class="clip ', '<div class="clip cl-lp ', 1)
                        zz.insert(1, f'  <a class="cl-lplink" href="{c["lplink"]}"'
                                     f' aria-label="Zur Animation im Leitprogramm: {html.escape(c["titel"])}">LP</a>')
                    if c.get("werkzeug"):
                        # Taschenrechner-Clips sollen herausstechen: dunkle Zeile mit Marke «TR»
                        zz[0] = zz[0].replace('<div class="clip cl-tr', '<div class="clip cl-tr cl-trz', 1)
                        zz.insert(1, '  <span class="cl-trmarke" aria-hidden="true">TR</span>')
                    aus += ["          " + z for z in zz]
                aus.append('        </div>')
            aus += ['      </div>', '    </div>']
        aus += ['  </div>', '</div>']
    if offen is not None:
        aus.append("</div>")
    if not gesamt:
        aus.append('<p class="cl-leer">Noch keine Clips.</p>')
    aus.append(e.BIB_ZU)
    return "\n".join(aus)
