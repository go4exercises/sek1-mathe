"""Misst die Wortzeiten der vertonten Clips lin-lp-* (Leitprogramm Lineare Funktionen; Gerüst aus scripts/lp/bruchrechnen/) mit faster-whisper und schreibt wortzeiten.json
(je Clip und Szene: Wörter mit Beginn und Ende in Sekunden ab Szenenbeginn). clips.py legt damit
Einblendungen und Bewegungen auf das Wort, das sie nennt (HOWTO-leitprogramme §15: «Bewegungen nach
sprechzeiten.py legen, nicht nach Gefühl»).

  python3 scripts/lp/lineare-funktionen/wortzeiten.py [clip …]      # ohne Angabe: alle acht

Die mp3 dekodiert das System-python3 (soundfile); faster-whisper läuft in der eigenen venv
(~/.local/share/whisper-venv) und bekommt ein float32-Array mit 16 kHz — `av` ist dort nicht
benutzbar. Modell: medium (lokal im Cache; small verhörte Bruchwörter, 09.10.2026).
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf

HIER = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.abspath(os.path.join(HIER, '..', '..', '..')) + '/'
VENV = os.path.expanduser('~/.local/share/whisper-venv/bin/python')
NAMEN = ['anfangswert', 'kontrolle-anfangswert', 'steigung', 'kontrolle-steigung', 'zeichnen', 'kontrolle-zeichnen',
         'gleichung', 'kontrolle-gleichung']
spec = importlib.util.spec_from_file_location('bc', R + 'scripts/build-clips.py')
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)

WHISPER = r'''
import json, sys, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8")
aus = {}
for pfad in sys.argv[1:]:
    x = np.load(pfad).astype("float32")
    seg, _ = m.transcribe(x, language="de", word_timestamps=True, beam_size=5)
    aus[pfad] = [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for s in seg for w in s.words]
print(json.dumps(aus))
'''

ziel = HIER + 'wortzeiten.json'
alt = json.load(open(ziel)) if os.path.exists(ziel) else {}
namen = sys.argv[1:] or NAMEN
with tempfile.TemporaryDirectory() as tmp:
    pfade = {}
    for n in namen:
        ton = R + 'clips/ton/lin-lp-' + n + '.mp3'
        if not os.path.exists(ton):
            print('kein Ton:', n)
            continue
        x, sr = sf.read(ton, dtype='float32')
        if x.ndim > 1:
            x = x.mean(1)
        idx = np.arange(0, len(x), sr / 16000.0)
        x16 = np.interp(idx, np.arange(len(x)), x).astype('float32')
        p = os.path.join(tmp, n + '.npy')
        np.save(p, x16)
        pfade[n] = p
    if pfade:
        skript = os.path.join(tmp, 'w.py')
        open(skript, 'w').write(WHISPER)
        r = subprocess.run([VENV, skript] + list(pfade.values()), capture_output=True, text=True)
        if r.returncode:
            sys.exit(r.stderr[-2000:])
        woerter = json.loads(r.stdout.strip().splitlines()[-1])
        for n, p in pfade.items():
            dreh = json.load(open(R + 'clips/lin-lp-' + n + '.json'))
            plan, _ = bc.szenen_planen(dreh)
            je = {}
            for pl, s in zip(plan, dreh['szenen']):
                a, e = pl['start'], pl['start'] + pl['dauer']
                je[s['name']] = {'sprecher': s.get('sprecher', ''),
                                 'woerter': [[wt, round(t0 - a, 2), round(t1 - a, 2)] for wt, t0, t1 in woerter[p] if a <= t0 < e]}
            alt[n] = je
            print(n, sum(len(v['woerter']) for v in je.values()), 'Wörter')
json.dump(alt, open(ziel, 'w'), ensure_ascii=False, indent=1)
