// Prüft, was pruef-leiste und pruef-uebungen nicht sehen (HOWTO-leitprogramme §14/§15):
//   1. Jede Aufgabe der Leisten in Sim 1–4 ist mit den Reglern lösbar → ✓, keine im Start erfüllt.
//   2. Klickgitter: Punkte rasten auf Gitterpunkten ein, der dritte Klick ersetzt den ersten.
//   3. Verteilung: 20 000 Würfe je Übungstyp — wie viele verschiedene Aufgaben, wie viele gesperrt.
//
//   node scripts/lp/lineare-funktionen/pruef-schritte.mjs        (vom Repo-Root; Exit 1 bei Befund)
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
await page.goto(`http://localhost:${server.address().port}/leitprogramme/lineare-funktionen.html`);
await page.waitForTimeout(400);
let befunde = 0;
const melde = (ok, t) => { console.log((ok ? '[OK]     ' : '[FEHLER] ') + t); if (!ok) befunde++; };

// ---- 1. Leisten: Reglerwerte je Aufgabe (in dieser Reihenfolge gesetzt)
const LOES = {
  sim1: [[['s1-b', 30], ['s1-m', 10]], [['s1-b', 0], ['s1-m', 15]], [['s1-b', 90], ['s1-m', -10]], [['s1-b', 20], ['s1-m', 20]], [['s1-b', 15], ['s1-m', 10]]],
  sim2: [[['s2-dx', 1], ['s2-dy', 2]], [['s2-dx', 1], ['s2-dy', -1]], [['s2-dx', 2], ['s2-dy', 1]], [['s2-dx', 2], ['s2-dy', -3]], [['s2-dx', 1], ['s2-dy', 0]]],
  sim3: [[['s3-b', 2], ['s3-dy', 3], ['s3-dx', 1]], [['s3-b', -1], ['s3-dy', 2], ['s3-dx', 1]], [['s3-b', 3], ['s3-dy', 1], ['s3-dx', 1]],
         [['s3-b', 4], ['s3-dy', -2], ['s3-dx', 1]], [['s3-b', -3], ['s3-dy', 2], ['s3-dx', 3]]],
  sim4: [[['s4-v', 400], ['s4-r1', 4], ['s4-r2', 4], ['s4-t', 100]], [['s4-v', 600], ['s4-r1', 3], ['s4-r2', 3], ['s4-t', 120]],
         [['s4-v', 500], ['s4-r1', 5], ['s4-T', 60], ['s4-r2', 2], ['s4-t', 160]], [['s4-v', 900], ['s4-r1', 3], ['s4-r2', 3], ['s4-t', 300]],
         [['s4-v', 800], ['s4-r1', 4], ['s4-T', 100], ['s4-r2', 8], ['s4-t', 150]]],
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

// ---- 2. Klickgitter: zwei Klicks setzen zwei Punkte, ein dritter ersetzt den ersten
melde(await page.evaluate(() => {
  const box = document.querySelector('.uebung[data-typ="zeichnen"]'), svg = box.querySelector('svg.klick-gitter');
  const r = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal;
  const klick = (x, y) => { const px = (x + 7) / 14 * 280, py = (7 - y) / 14 * 280;
    svg.dispatchEvent(new MouseEvent('click', { bubbles: true, clientX: r.left + (px - vb.x) / vb.width * r.width, clientY: r.top + (py - vb.y) / vb.height * r.height })); };
  klick(0, 1); klick(3, 3); const a = [box.querySelector('[data-f="p1"]').value, box.querySelector('[data-f="p2"]').value];
  klick(-2, -1); const b = [box.querySelector('[data-f="p1"]').value, box.querySelector('[data-f="p2"]').value];
  return a.join(';') === '0|1;3|3' && b.join(';') === '3|3;-2|-1';
}), 'Klickgitter: Punkte werden auf Gitterpunkte gesetzt und ersetzt');

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
