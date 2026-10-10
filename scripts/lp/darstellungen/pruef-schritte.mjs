// Prüft, was pruef-leiste und pruef-uebungen nicht sehen (HOWTO-leitprogramme §14/§15):
//   1. Jede Aufgabe der Leisten in Sim 1–4 ist mit den Reglern lösbar → ✓, keine im Start erfüllt.
//   2. Ränder: Sim 2 meldet «kein Rechteck» bei x ≥ U/2, Sim 3 warnt bei negativen Werten.
//   3. Verteilung: 20 000 Würfe je Übungstyp — wie viele verschiedene Aufgaben, wie viele gesperrt.
//
//   node scripts/lp/darstellungen/pruef-schritte.mjs        (vom Repo-Root; Exit 1 bei Befund)
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
await page.goto(`http://localhost:${server.address().port}/leitprogramme/darstellungen.html`);
await page.waitForTimeout(400);
let befunde = 0;
const melde = (ok, t) => { console.log((ok ? '[OK]     ' : '[FEHLER] ') + t); if (!ok) befunde++; };

// ---- 1. Leisten: Reglerwerte je Aufgabe (in dieser Reihenfolge gesetzt)
const LOES = {
  sim1: [[['s1-b', 20], ['s1-m', 5]], [['s1-b', 30], ['s1-m', -3]], [['s1-b', 10], ['s1-m', 4]], [['s1-b', 14], ['s1-m', 7], ['s1-x', 4]], [['s1-b', 45], ['s1-m', -5]]],
  sim2: [[['s2-U', 20], ['s2-x', 3]], [['s2-U', 30], ['s2-x', 7.5]], [['s2-U', 24], ['s2-x', 4]], [['s2-U', 28], ['s2-x', 5]], [['s2-U', 16], ['s2-x', 6.5]]],
  sim3: [[['s3-von', 0], ['s3-bis', 12]], [['s3-von', 0], ['s3-bis', 10], ['s3-art', 'punkte']], [['s3-von', 0], ['s3-bis', 15]],
         [['s3-von', 0], ['s3-bis', 9], ['s3-art', 'punkte']], [['s3-von', 0], ['s3-bis', 12.5]]],
  sim4: [[['s4-S', 12], ['s4-P', 36], ['s4-x', 6]], [['s4-S', 10], ['s4-P', 24], ['s4-x', 4]], [['s4-P', 24], ['s4-x', 6]], [['s4-S', 12], ['s4-x', 7]],
         [['s4-S', 9], ['s4-P', 20], ['s4-x', 5]]],
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

// ---- 2. Ränder des Definitionsbereichs
melde(await page.evaluate(() => {
  const fig = document.getElementById('sim2'), set = (k, v) => { const e = fig.querySelector('#' + k); e.value = v; e.dispatchEvent(new Event('input')); };
  set('s2-U', 12); set('s2-x', 6); const a = /zu lang/.test(fig.querySelector('[data-rolle="formel"]').textContent) && /kein Rechteck/.test(fig.querySelector('svg.rechteck-bild').textContent);
  set('s2-x', 5.5); const b = !/zu lang/.test(fig.querySelector('[data-rolle="formel"]').textContent);
  return a && b;
}), 'Sim 2: x = U/2 gibt «kein Rechteck», x knapp darunter ein Rechteck');
melde(await page.evaluate(() => {
  const fig = document.getElementById('sim3'), set = (k, v) => { const e = fig.querySelector('#' + k); e.value = v; e.dispatchEvent(new Event('input')); };
  set('s3-von', 0); set('s3-bis', 18); return /negativ/.test(fig.querySelector('[data-rolle="formel"]').textContent);
}), 'Sim 3: ein Bereich über das Ende hinaus wird als negativ gemeldet');

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
