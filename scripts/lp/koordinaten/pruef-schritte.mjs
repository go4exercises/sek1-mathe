// Prüft, was pruef-leiste und pruef-uebungen nicht sehen (HOWTO-leitprogramme §14/§15):
//   1. Jede Aufgabe der Leisten in Sim 1–4 ist mit den Reglern lösbar → ✓, keine im Start erfüllt.
//   2. Sim 4 bei senkrechter Geraden und bei A = B.
//   3. Verteilung: 20 000 Würfe je Übungstyp — wie viele verschiedene Aufgaben, wie viele gesperrt.
//
//   node scripts/lp/koordinaten/pruef-schritte.mjs        (vom Repo-Root; Exit 1 bei Befund)
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
await page.goto(`http://localhost:${server.address().port}/leitprogramme/koordinaten.html`);
await page.waitForTimeout(400);
let befunde = 0;
const melde = (ok, t) => { console.log((ok ? '[OK]     ' : '[FEHLER] ') + t); if (!ok) befunde++; };

// ---- 1. Leisten: Reglerwerte je Aufgabe (in dieser Reihenfolge gesetzt)
const LOES = {
  sim1: [[['s1-px', 3], ['s1-py', 1], ['s1-zx', 1], ['s1-zy', 3]], [['s1-px', -2], ['s1-py', 3], ['s1-zx', 0], ['s1-zy', 0]], [['s1-px', 2], ['s1-py', 2], ['s1-zx', 2], ['s1-zy', 2]],
         [['s1-px', -4], ['s1-py', 1], ['s1-zx', -1], ['s1-zy', -1]], [['s1-px', 3], ['s1-py', 4], ['s1-zx', -1], ['s1-zy', 2]]],
  sim2: [[['s2-ach', 'xa'], ['s2-a', 2], ['s2-px', 5], ['s2-py', 1]], [['s2-ach', 'y'], ['s2-px', -3], ['s2-py', -2]], [['s2-ach', 'yb'], ['s2-a', 1], ['s2-px', 2], ['s2-py', 4]],
         [['s2-ach', 'd'], ['s2-px', 4], ['s2-py', -1]], [['s2-ach', 'yb'], ['s2-a', -1], ['s2-px', -3], ['s2-py', 2]]],
  sim3: [[['s3-zx', 0], ['s3-zy', 0], ['s3-k', 2]], [['s3-zx', 1], ['s3-zy', 1], ['s3-k', 2]], [['s3-zx', 0], ['s3-zy', 0], ['s3-k', 3]], [['s3-zx', 0], ['s3-zy', 0], ['s3-k', 0.5]],
         [['s3-zx', 5], ['s3-zy', 1], ['s3-k', 2]]],
  sim4: [[['s4-ax', 0], ['s4-ay', -2], ['s4-bx', 4], ['s4-by', 4]], [['s4-ax', 0], ['s4-ay', 5], ['s4-bx', 3], ['s4-by', 2]], [['s4-ax', 1], ['s4-ay', 1], ['s4-bx', 3], ['s4-by', 5]],
         [['s4-ax', -2], ['s4-ay', 3], ['s4-bx', 4], ['s4-by', 3]], [['s4-ax', -3], ['s4-ay', 0], ['s4-bx', 3], ['s4-by', 4]]],
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

// ---- 2. Sim 4: A = B und senkrechte Gerade melden sich, statt durch 0 zu teilen
melde(await page.evaluate(() => {
  const fig = document.getElementById('sim4'), set = (k, v) => { const e = fig.querySelector('#' + k); e.value = v; e.dispatchEvent(new Event('input')); };
  set('s4-ax', 2); set('s4-bx', 2); set('s4-ay', 1); set('s4-by', 4); const a = fig.querySelector('[data-rolle="formel"]').textContent;
  set('s4-by', 1); const b = fig.querySelector('[data-rolle="formel"]').textContent;
  return /Senkrechte/.test(a) && /zusammen/.test(b) && !/NaN|Infinity/.test(a + b);
}), 'Sim 4: senkrecht und A = B ohne Division durch 0');

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
