#!/usr/bin/env python3
"""Misst, wann in einem vertonten Clip gesprochen wird — je Szene, in Sekunden ab Szenenbeginn.

  python3 .claude/tools/sprechzeiten.py <clip> [<szene> …]

Wofür: Stützpunkte einer `bewegung` und Einblendungen auf den Ton legen. Die Zeiten im
Drehbuch gelten ab Szenenbeginn; nach einer Neuvertonung verschieben sie sich. Ausgabe je
Szene: die Sprechstücke (laut, Pausen unter 0.15 s zusammengefasst) und der Sprechertext.
Ordnet man die Stücke den Satzteilen zu, sieht man, wann «a = 0.5» gesagt wird und wann die
Parabel dort ankommen muss. Braucht numpy und soundfile; liest clips/ton/<clip>.mp3.
"""
import importlib.util
import json
import os
import sys

import numpy as np
import soundfile as sf

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if len(sys.argv) < 2:
    sys.exit(__doc__)
spec = importlib.util.spec_from_file_location("bc", os.path.join(WURZEL, "scripts", "build-clips.py"))
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)

name = sys.argv[1].replace("clips/", "").replace(".json", "").replace(".html", "")
dreh = json.load(open(os.path.join(WURZEL, "clips", name + ".json"), encoding="utf-8"))
plan, _ = bc.szenen_planen(dreh)
x, sr = sf.read(os.path.join(WURZEL, "clips", "ton", name + ".mp3"), dtype="float32")
if x.ndim > 1:
    x = x.mean(1)
for p, s in zip(plan, dreh["szenen"]):
    if len(sys.argv) > 2 and s.get("name") not in sys.argv[2:]:
        continue
    seg = x[int(p["start"] * sr):int((p["start"] + s["dauer"]) * sr)]
    fr = int(0.02 * sr)
    if len(seg) <= fr:
        continue
    env = np.array([np.abs(seg[k:k + fr]).max() for k in range(0, len(seg) - fr, fr)])
    laut = env > 0.02 * env.max()
    stuecke, start = [], None
    for k, l in enumerate(laut):
        if l and start is None:
            start = k
        if not l and start is not None:
            stuecke.append((start * 0.02, k * 0.02))
            start = None
    if start is not None:
        stuecke.append((start * 0.02, len(laut) * 0.02))
    zus = []
    for a, b in stuecke:
        if zus and a - zus[-1][1] < 0.15:
            zus[-1] = (zus[-1][0], b)
        else:
            zus.append((a, b))
    print(f"{s.get('name', '?'):14s} ab {p['start']:.2f} s, dauer {s['dauer']}: " + " ".join(f"{a:.2f}–{b:.2f}" for a, b in zus))
    print("    ", s.get("sprecher", ""))
