// Prüft, was pruef-leiste und pruef-uebungen nicht sehen (HOWTO-leitprogramme §14/§15):
//   1. Jede Aufgabe der Leisten in Sim 1–4 ist mit den Reglern lösbar → ✓, keine im Start erfüllt.
//   2. Sim 3 bleibt bei d > r rechnerisch gültig.
//   3. Verteilung: 20 000 Würfe je Übungstyp — wie viele verschiedene Aufgaben, wie viele gesperrt.
//
//   node scripts/lp/pythagoras/pruef-schritte.mjs        (vom Repo-Root; Exit 1 bei Befund)
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
await page.goto(`http://localhost:${server.address().port}/leitprogramme/pythagoras.html`);
await page.waitForTimeout(400);
let befunde = 0;
const melde = (ok, t) => { console.log((ok ? '[OK]     ' : '[FEHLER] ') + t); if (!ok) befunde++; };

// ---- 1. Leisten: Reglerwerte je Aufgabe (in dieser Reihenfolge gesetzt)
const LOES = {
  sim1: [[['s1-typ', 'd'], ['s1-g', 8], ['s1-h', 4]], [['s1-typ', 'd'], ['s1-g', 6], ['s1-h', 4], ['s1-s', 6]], [['s1-typ', 'p'], ['s1-g', 5], ['s1-h', 4]],
         [['s1-typ', 'd'], ['s1-g', 10], ['s1-h', 3], ['s1-s', 12]], [['s1-typ', 'p'], ['s1-g', 4], ['s1-h', 6], ['s1-s', 3]]],
  sim2: [[['s2-a', 9], ['s2-b', 12]], [['s2-a', 8], ['s2-b', 15]], [['s2-a', 12], ['s2-b', 16]], [['s2-a', 7], ['s2-b', 24]], [['s2-a', 21], ['s2-b', 20]]],
  sim3: [[['s3-r', 13], ['s3-d', 5]], [['s3-r', 5], ['s3-d', 3]], [['s3-r', 15], ['s3-d', 12]], [['s3-r', 10], ['s3-d', 8]], [['s3-r', 13], ['s3-d', 12]]],
  sim4: [[['s4-k', 2]], [['s4-k', 3]], [['s4-k', 1.5]], [['s4-k', 0.5]], [['s4-k', 2.5]]],
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

// ---- 2. Sim 3: Abstand grösser als der Radius wird auf r begrenzt (keine Wurzel aus einer negativen Zahl)
melde(await page.evaluate(() => {
  const fig = document.getElementById('sim3'), set = (k, v) => { const e = fig.querySelector('#' + k); e.value = v; e.dispatchEvent(new Event('input')); };
  set('s3-r', 4); set('s3-d', 12); return !/NaN/.test(fig.querySelector('[data-rolle="formel"]').textContent);
}), 'Sim 3: d > r ohne NaN');

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
