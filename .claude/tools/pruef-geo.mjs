// Prüft die Geometrie-Arbeitsbereiche (figure.geo) eines Leitprogramms — leitprogramme/planimetrie.html.
//
//   node .claude/tools/pruef-geo.mjs leitprogramme/<name>.html
//
// Je Aufgabe der Leiste: nicht schon beim Erscheinen gelöst; bei «Linie antippen» gibt jede falsche
// Linie eine Rückmeldung und die richtige ✓; bei «Grösse eingeben» gibt jeder bekannte Fehlwert eine
// Rückmeldung und der Sollwert ✓; bei Reglerzielen löst der Beispielzustand `probe` die Aufgabe.
// Kandidatenlinien, die übereinanderliegen, sind ein Befund (mit der Maus nicht unterscheidbar).
// Braucht die Testhaken fig.__aufgaben (seite.js). Exit 1 bei einem Befund.
import path from 'node:path';
const WURZEL = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage(); const fe = []; p.on('pageerror', e => fe.push(e.message));
const seite = process.argv[2]; if (!seite){ console.error('Aufruf: node .claude/tools/pruef-geo.mjs leitprogramme/<name>.html'); process.exit(2); }
await p.goto('file://' + path.resolve(WURZEL, seite)); await p.waitForTimeout(1500);
const ids = await p.evaluate(() => [...document.querySelectorAll('figure.geo')].map(f => f.id));
let befunde = 0;
for (const id of ids){
  const r = await p.evaluate(({ id }) => {
    const fig = document.getElementById(id), A = fig.__aufgaben, L = fig.querySelector('.leiste'), log = [];
    const ok = () => L.querySelector('.ls-ok').textContent === '✓', rueck = fig.querySelector('.g-rueck');
    for (let i = 0; i < A.length; i++){
      const a = A[i];
      if (ok()) log.push('A' + (i + 1) + ' schon gelöst beim Erscheinen');
      if (a.wahl){
        const ids = [...fig.querySelectorAll('.kandidat')].map(k => k.dataset.id);
        // Deckungsgleiche Kandidaten (Prüfung Planimetrie 06.10.2026, H1): Liegen zwei Linien auf
        // wenigen Pixeln aufeinander, trifft der Tipp nur die obere — die Aufgabe ist mit der Maus unlösbar.
        const lin = [...fig.querySelectorAll('.kandidat .k-sicht')].map(l => ['x1', 'y1', 'x2', 'y2'].map(k => +l.getAttribute(k)));
        const nahe = (p, q) => Math.hypot(p[0] - q[0], p[1] - q[1]) < 6;
        for (let u = 0; u < lin.length; u++) for (let v = u + 1; v < lin.length; v++){
          const a1 = [lin[u][0], lin[u][1]], a2 = [lin[u][2], lin[u][3]], b1 = [lin[v][0], lin[v][1]], b2 = [lin[v][2], lin[v][3]];
          if ((nahe(a1, b1) && nahe(a2, b2)) || (nahe(a1, b2) && nahe(a2, b1))) log.push('A' + (i + 1) + ' Linien ' + ids[u] + ' und ' + ids[v] + ' liegen übereinander');
        }
        if (!ids.includes(a.wahl.richtig)) log.push('A' + (i + 1) + ' richtige Linie fehlt');
        ids.filter(k => k !== a.wahl.richtig).forEach(k => { fig.querySelector('.kandidat[data-id="' + k + '"]').dispatchEvent(new MouseEvent('click', { bubbles: true }));
          if (!rueck.classList.contains('falsch') || ok()) log.push('A' + (i + 1) + ' falsche Linie ' + k + ' ohne Rückmeldung'); });
        fig.querySelector('.kandidat[data-id="' + a.wahl.richtig + '"]').dispatchEvent(new MouseEvent('click', { bubbles: true }));
      } else if (a.frage){
        const inp = [...fig.querySelectorAll('.g-eingabe input')];
        a.frage.forEach((f, j) => (f.fehler || []).forEach(fe => { inp.forEach((x, q) => x.value = q === j ? fe[0] : a.frage[q].soll);
          fig.querySelector('.g-pruefen').click(); if (!rueck.classList.contains('falsch') || ok()) log.push('A' + (i + 1) + ' Fehler ' + fe[0] + ' → ' + rueck.textContent.slice(0, 60)); }));
        inp.forEach((x, q) => x.value = String(a.frage[q].soll)); fig.querySelector('.g-pruefen').click();
      } else {
        const z = a.probe || {}; for (const k in z){ const s = fig.querySelector('input[data-p="' + k + '"]'); s.value = z[k]; s.dispatchEvent(new Event('input')); }
      }
      if (!ok()) log.push('A' + (i + 1) + ' NICHT gelöst: ' + rueck.textContent.slice(0, 80) + ' | ' + fig.querySelector('[data-rolle=formel]').textContent.slice(0, 80));
      L.querySelector('.ls-weiter').click();
    }
    return log;
  }, { id });
  befunde += r.length; console.log(r.length ? '[FEHLER] ' + id + '\n   ' + r.join('\n   ') : '[OK]     ' + id + '  ' + (await p.evaluate(id => document.getElementById(id).__aufgaben.length, id)) + ' Aufgaben');
}
await b.close();
befunde += fe.length; if (fe.length) console.log('JS-Fehler:', fe);
console.log(befunde ? `\n${befunde} Befund(e).` : '\nALLE ARBEITSBEREICHE BESTANDEN');
process.exit(befunde ? 1 : 0);
