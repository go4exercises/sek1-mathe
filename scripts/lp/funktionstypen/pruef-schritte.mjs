// Prüft, was pruef-leiste und pruef-uebungen nicht sehen (HOWTO-leitprogramme §14/§15):
//   1. Jede Aufgabe der Leisten in Sim 1–4 ist mit den Reglern lösbar → ✓, keine im Start erfüllt.
//   2. Sim 3 warnt, wenn der Graph hinter den Start fällt.
//   3. Verteilung: 20 000 Würfe je Übungstyp — wie viele verschiedene Aufgaben, wie viele gesperrt.
//
//   node scripts/lp/funktionstypen/pruef-schritte.mjs        (vom Repo-Root; Exit 1 bei Befund)
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const WURZEL = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..', '..');
const TYP = { html: 'text/html', js: 'text/javascript', css: 'text/css', svg: 'image/svg+xml', woff2: 'font/woff2', png: 'image/png' };
const server = http.createServer((req, res) => {
  const p = path.join(WURZEL, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(WURZEL) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYP[path.extname(p).slice(1)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const browser = await chromium.launch();
const page = await browser.newPage();
const jsFehler = [];
page.on('pageerror', e => jsFehler.push(e.message));
await page.route('**/vendor/mathjax/**', r => r.abort());
await page.goto(`http://localhost:${server.address().port}/leitprogramme/funktionstypen.html`);
await page.waitForTimeout(400);
let befunde = 0;
const melde = (ok, t) => { console.log((ok ? '[OK]     ' : '[FEHLER] ') + t); if (!ok) befunde++; };

// ---- 1. Leisten: Reglerwerte je Aufgabe (in dieser Reihenfolge gesetzt)
const LOES = {
  sim1: [[['s1-fam', 'g'], ['s1-a', 2], ['s1-b', -1]], [['s1-fam', 'q'], ['s1-a', 1], ['s1-b', -2]], [['s1-fam', 'w'], ['s1-a', 2], ['s1-b', 0]],
         [['s1-fam', 'k'], ['s1-a', 4], ['s1-b', 0]], [['s1-fam', 'q'], ['s1-a', -0.5], ['s1-b', 3]]],
  sim2: [[['s2-typ', 'lin'], ['s2-k', 3], ['s2-b', 0]], [['s2-typ', 'lin'], ['s2-k', 3], ['s2-b', 4]], [['s2-typ', 'anti'], ['s2-k', 12]],
         [['s2-typ', 'lin'], ['s2-k', 2], ['s2-b', 0]], [['s2-typ', 'anti'], ['s2-k', 18]]],
  sim3: [[['s3-v1', 60], ['s3-v2', 0], ['s3-v3', 120]], [['s3-v1', 100], ['s3-v2', 50], ['s3-v3', 0]], [['s3-v1', 80], ['s3-v2', 0], ['s3-v3', -80]],
         [['s3-v1', 40], ['s3-v2', 80], ['s3-v3', 120]], [['s3-v1', 120], ['s3-v2', -60], ['s3-v3', 30]]],
  sim4: [[['s4-L', 24], ['s4-v', 16], ['s4-t', 0.75]], [['s4-L', 20], ['s4-v', 8], ['s4-t', 2]], [['s4-L', 12], ['s4-v', 4], ['s4-t', 1.5]],
         [['s4-L', 30], ['s4-v', 12], ['s4-t', 2.5]], [['s4-L', 18], ['s4-v', 6], ['s4-t', 2]]],
};
for (const [sim, ziele] of Object.entries(LOES)) {
  const r = await page.evaluate(([sim, ziele]) => {
    const fig = document.getElementById(sim), L = fig.querySelector('.leiste'), bt = L.querySelector('.ls-weiter'), aus = [];
    ziele.forEach((z, i) => {
      const vorher = L.querySelector('.ls-ok').textContent.includes('✓');
      for (const [k, v] of z) { const e = fig.querySelector('#' + k); e.value = v; e.dispatchEvent(new Event('input')); }
      aus.push([i + 1, !vorher && L.querySelector('.ls-ok').textContent.includes('✓'), L.querySelector('.ls-text').textContent.slice(0, 60)]);
      bt.click();
    });
    aus.push(['Ende', /Alle/.test(L.querySelector('.ls-text').textContent), L.querySelector('.ls-text').textContent]);
    return aus;
  }, [sim, ziele]);
  for (const [i, ok, t] of r) melde(ok, `${sim} Aufgabe ${i}: ${t}`);
}

// ---- 2. Sim 3 meldet einen Graphen hinter dem Start
melde(await page.evaluate(() => {
  const fig = document.getElementById('sim3'), set = (k, v) => { const e = fig.querySelector('#' + k); e.value = v; e.dispatchEvent(new Event('input')); };
  set('s3-v1', -50); return /hinter dem Start/.test(fig.querySelector('[data-rolle="formel"]').textContent);
}), 'Sim 3: negativer Weg wird gemeldet');

// ---- 3. Verteilung
const V = await page.evaluate(() => {
  const aus = [];
  for (const [name, T] of Object.entries(window.__TYPEN)) {
    const schl = new Map(); let gesperrt = 0;
    for (let i = 0; i < 20000; i++) {
      // dieselbe Normierung wie die Seite (window.__gesperrt): unsortierte Paare zählen als gesperrt (Prüfung 10.10.2026)
      let A = T.neu(); for (let v = 0; v < 60 && window.__gesperrt(T, A); v++) A = T.neu();
      const k = T.schl(A); if (window.__gesperrt(T, A)) gesperrt++;
      schl.set(k, (schl.get(k) || 0) + 1);
    }
    const haeufigst = Math.max(...schl.values());
    aus.push([name, schl.size, gesperrt, haeufigst]);
  }
  return aus;
});
for (const [name, anz, ges, max] of V) melde(ges === 0 && anz >= 30 && max < 2000, `Verteilung ${name.padEnd(14)} ${anz} verschiedene Aufgaben in 20 000 Würfen, gesperrt gestellt: ${ges}, häufigste ${max}×`);

for (const e of jsFehler) melde(false, 'JS: ' + e);
await browser.close(); server.close();
console.log(befunde ? `\n${befunde} Befund(e).` : '\nALLES BESTANDEN');
process.exit(befunde ? 1 : 0);
