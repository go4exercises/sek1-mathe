// Prüft, was pruef-leiste und pruef-uebungen nicht sehen (HOWTO-leitprogramme §14/§15):
//   1. Jede Aufgabe der Leisten in Sim 1–4 ist mit den Reglern lösbar → ✓, keine im Start erfüllt.
//   2. Sim 3 ohne Zeit und Sim 4 nach der Begegnung melden sich.
//   3. Verteilung: 20 000 Würfe je Übungstyp — wie viele verschiedene Aufgaben, wie viele gesperrt.
//
//   node scripts/lp/bewegung/pruef-schritte.mjs        (vom Repo-Root; Exit 1 bei Befund)
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
await page.goto(`http://localhost:${server.address().port}/leitprogramme/bewegung.html`);
await page.waitForTimeout(400);
let befunde = 0;
const melde = (ok, t) => { console.log((ok ? '[OK]     ' : '[FEHLER] ') + t); if (!ok) befunde++; };

// ---- 1. Leisten: Reglerwerte je Aufgabe (in dieser Reihenfolge gesetzt)
const LOES = {
  sim1: [[['s1-x', 5]], [['s1-x', 6]], [['s1-x', 20]], [['s1-x', 5]], [['s1-x', 4]]],
  sim2: [[['s2-v', 60], ['s2-t', 45]], [['s2-v', 45], ['s2-t', 40]], [['s2-v', 90], ['s2-t', 20]], [['s2-v', 10], ['s2-t', 30]], [['s2-v', 80], ['s2-t', 75]]],
  sim3: [[['s3-v1', 80], ['s3-t1', 1], ['s3-v2', 40], ['s3-t2', 1]], [['s3-v1', 40], ['s3-t1', 1], ['s3-v2', 80], ['s3-t2', 1]],
         [['s3-v1', 60], ['s3-t1', 1], ['s3-v2', 30], ['s3-t2', 2]], [['s3-v1', 30], ['s3-t1', 1], ['s3-v2', 90], ['s3-t2', 1]],
         [['s3-v1', 40], ['s3-t1', 1.5], ['s3-v2', 0], ['s3-t2', 0.5]]],
  sim4: [[['s4-D', 30], ['s4-a', 12], ['s4-b', 8], ['s4-r', 'ent'], ['s4-t', 1.5]], [['s4-D', 20], ['s4-a', 15], ['s4-b', 10], ['s4-r', 'gleich'], ['s4-t', 4]],
         [['s4-D', 42], ['s4-a', 20], ['s4-b', 15], ['s4-r', 'ent'], ['s4-t', 1.2]], [['s4-D', 10], ['s4-a', 20], ['s4-b', 15], ['s4-r', 'gleich'], ['s4-t', 2]],
         [['s4-D', 30], ['s4-a', 12], ['s4-b', 8], ['s4-r', 'ent'], ['s4-t', 1.2]]],
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

// ---- 2. Sim 3 ohne Zeit und Sim 4 nach der Begegnung melden sich
melde(await page.evaluate(() => {
  const fig = document.getElementById('sim3'), set = (k, v) => { const e = fig.querySelector('#' + k); e.value = v; e.dispatchEvent(new Event('input')); };
  set('s3-t1', 0); set('s3-t2', 0); return /Stell eine Zeit ein/.test(fig.querySelector('[data-rolle="formel"]').textContent);
}), 'Sim 3: ohne Zeit kein Durchschnitt (keine Division durch 0)');
melde(await page.evaluate(() => {
  const fig = document.getElementById('sim4'), set = (k, v) => { const e = fig.querySelector('#' + k); e.value = v; e.dispatchEvent(new Event('input')); };
  set('s4-D', 30); set('s4-a', 12); set('s4-b', 8); set('s4-r', 'ent'); set('s4-t', 2); return /schon vorbei/.test(fig.querySelector('[data-rolle="formel"]').textContent);
}), 'Sim 4: nach der Begegnung «schon vorbei»');

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
