#!/usr/bin/env python3
"""Vertont die Fragen eines Clips («fragen» im Drehbuch, HOWTO-clips.md).

Jede Frage und jede Rückmeldung bekommt eine eigene kurze Tondatei mit
derselben Stimme wie der Clip: clips/ton/<clip>-f<i>-<schluessel>.mp3.
Der Abspieler spielt sie, wenn die Frage erscheint bzw. geantwortet wird —
und nur, wenn der Ton des Clips an ist. Die Haupttonspur bleibt unberührt.

Nur in TALS-Mathe. Benutzt sprich() und aussprache() aus build-clip-ton.py
(geteiltes Werkzeug, darum nicht dort eingebaut) und fragen_texte() aus
build-clips.py, damit Dateinamen und Abspieler immer zusammenpassen.

  export PATH="$HOME/.local/bin:$PATH" PIPER_MODELL=$HOME/piper-stimmen/de_DE-thorsten-high.onnx
  python3 scripts/build-clip-fragen-ton.py g3-3-lp-verschieben
  python3 scripts/build-clips.py g3-3-lp-verschieben      # danach, damit der Clip die Dateien kennt

Nur einzelne Fragen neu: `--fragen 2,5:r1` spricht alle Toene von Frage 2 und
nur den Ton r1 von Frage 5 (Fragen ab 1 wie in der Ausgabe; die Datei heisst
-f1-, -f4-r1). Alle anderen Dateien bleiben, wie sie sind. Ohne den Schalter
werden alle Fragetoene des Clips geloescht und neu gesprochen.
"""
import argparse
import importlib.util
import json
import os
import sys
import tempfile

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TON = os.path.join(WURZEL, "clips", "ton")


def lade(datei, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(WURZEL, "scripts", datei))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip", help="Drehbuch ohne .json")
    ap.add_argument("--modell", default=os.environ.get("PIPER_MODELL", ""))
    ap.add_argument("--piper", default=os.environ.get("PIPER_CMD", "piper"))
    ap.add_argument("--qualitaet", type=float, default=0.5)
    ap.add_argument("--fragen", default="",
                    help="nur diese Fragen neu, z. B. 2,5:r1 (ab 1; :schluessel nur diesen Ton)")
    a = ap.parse_args()
    if not a.modell or not os.path.exists(a.modell):
        sys.exit("Stimmmodell fehlt — --modell setzen oder PIPER_MODELL exportieren.")
    import numpy as np
    import soundfile as sf

    ton = lade("build-clip-ton.py", "clipton")
    bc = lade("build-clips.py", "buildclips")
    dreh = json.load(open(os.path.join(WURZEL, "clips", a.clip.removesuffix(".json") + ".json"), encoding="utf-8"))
    if not dreh.get("fragen"):
        sys.exit("Das Drehbuch hat keine «fragen».")
    os.makedirs(TON, exist_ok=True)
    piper = a.piper.split()

    # --fragen: {Frage (ab 0): Schluessel oder None fuer alle Toene der Frage}
    wahl = {}
    for t in filter(None, (t.strip() for t in a.fragen.split(","))):
        nr, _, schl = t.partition(":")
        if not nr.isdigit() or not 1 <= int(nr) <= len(dreh["fragen"]):
            sys.exit(f"--fragen: «{t}» — Fragen von 1 bis {len(dreh['fragen'])}, z. B. 2 oder 2:r1.")
        wahl.setdefault(int(nr) - 1, set()).add(schl or None)

    # Alte Fragetoene dieses Clips entfernen: sonst bleiben Dateien gestrichener
    # Rueckmeldungen liegen, und der Abspieler wuerde sie noch finden. Mit
    # --fragen nur die der ganz gewaehlten Fragen.
    for alt in os.listdir(TON):
        if alt.startswith(dreh["dateiname"] + "-f") and alt.endswith(".mp3"):
            if wahl and not any(None in v and alt.startswith(f"{dreh['dateiname']}-f{i}-")
                                for i, v in wahl.items()):
                continue
            os.remove(os.path.join(TON, alt))

    with tempfile.TemporaryDirectory() as tmp:
        for i, F in enumerate(dreh["fragen"]):
            for schl, _, gesprochen in bc.fragen_texte(F):
                if wahl and not (i in wahl and (None in wahl[i] or schl in wahl[i])):
                    continue
                w = os.path.join(tmp, "s.wav")
                ton.sprich(piper, a.modell, ton.aussprache(gesprochen), w)
                daten, rate = sf.read(w, dtype="float32")
                spitze = float(np.abs(daten).max()) if len(daten) else 0
                if spitze > 0.95:
                    daten *= 0.95 / spitze
                ziel = os.path.join(TON, bc.fragen_tondatei(dreh["dateiname"], i, schl))
                sf.write(ziel, daten, rate, format="MP3", compression_level=a.qualitaet)
                print(f"  Frage {i + 1} {schl:<7} {len(daten) / rate:5.1f} s  {gesprochen[:60]}")
    print(f"\n  Jetzt: python3 scripts/build-clips.py {dreh['dateiname']}")


if __name__ == "__main__":
    main()
