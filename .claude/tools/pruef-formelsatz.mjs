// Setzt Aufgabentext, Rückmeldungen (aus fehler()) und Lösung der Zufallsübungen eines
// Leitprogramms mit dem echten MathJax und meldet Satzfehler und LaTeX, das als Text stehen
// bleibt. Ergänzt pruef-uebungen.mjs, das MathJax abschaltet (HOWTO-leitprogramme §15).
//
//   node .claude/tools/pruef-formelsatz.mjs leitprogramme/<name>.html [anzahl=60]
//
// Exit 1, wenn ein Übungstyp Fehler hat. Entstanden am Leitprogramm Elektrizität (03.10.2026).
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
import { chromium } from 'playwright';
const W = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const seite = process.argv[2], N = +(process.argv[3] || 60);
if (!seite) { console.error('Aufruf: node .claude/tools/pruef-formelsatz.mjs leitprogramme/<name>.html [anzahl=60]'); process.exit(2); }
const T = { html: 'text/html', js: 'text/javascript', css: 'text/css', woff2: 'font/woff2' };
const server = http.createServer((q, r) => { const p = path.join(W, decodeURIComponent(q.url.split('?')[0]));
  if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': T[path.extname(p).slice(1)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r); }).listen(0);
const b = await chromium.launch(); const page = await b.newPage();
await page.goto(`http://localhost:${server.address().port}/${seite}`);
await page.waitForTimeout(6000);
const r = await page.evaluate(async (N) => {
  const aus = [];
  const probe = document.createElement('div'); document.body.appendChild(probe);
  for (const box of document.querySelectorAll('.uebung[data-typ]')) {
    const typ = box.dataset.typ; let fehler = 0, beispiel = '';
    for (let k = 0; k < N; k++) {
      box.querySelector('.ue-neu').click();
      const A = box.__aufgabe, T = box.__typ;
      const stuecke = [A.text, '\\(' + T.loesung(A) + '\\)'];
      if (T.fehler) for (const [w] of T.fehler(A)) { const e = {}; for (const f in w) e[f] = isNaN(+w[f]) ? w[f] : +w[f]; const m = T.pruefen(A, e); if (m) stuecke.push(m); }
      probe.innerHTML = stuecke.map(x => '<p>' + x + '</p>').join('');
      await MathJax.typesetPromise([probe]);
      const err = probe.querySelectorAll('mjx-merror, [data-mjx-error]').length;
      const roh = [...probe.querySelectorAll('p')].map(p => { const c = p.cloneNode(true); c.querySelectorAll('mjx-container').forEach(m => m.remove()); return c.textContent; }).filter(t => /\\[a-zA-Z]/.test(t));
      if (err || roh.length) { fehler++; if (!beispiel) beispiel = (roh[0] || probe.innerHTML).slice(0, 160); }
    }
    aus.push(typ + ': ' + (fehler ? fehler + ' Fälle mit Fehler, z. B. ' + beispiel : 'ok'));
  }
  return aus;
}, N);
console.log(r.join('\n')); await b.close(); server.close();
process.exit(r.some(z => !z.endsWith(': ok')) ? 1 : 0);
