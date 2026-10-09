// Prüft, was pruef-leiste und pruef-uebungen nicht sehen (HOWTO-leitprogramme §14/§15):
//   1. Jede Aufgabe der Leisten in Sim 1–3 ist lösbar: Zielwerte einstellen → ✓.
//   2. Schrittwähler (Sim 4): Jede Aufgabe wird durch Antippen des richtigen Zeichens und Eingabe
//      der Teilergebnisse gelöst; ein falsch gewähltes Zeichen gibt die erwartete Regel-Meldung.
//   3. Verteilung: 20 000 Würfe je Übungstyp — wie viele verschiedene Aufgaben, wie viele gesperrt.
//
//   node scripts/lp/bruchrechnen/pruef-schritte.mjs        (vom Repo-Root; Exit 1 bei Befund)
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
await page.goto(`http://localhost:${server.address().port}/leitprogramme/bruchrechnen.html`);
await page.waitForTimeout(400);
let befunde = 0;
const melde = (ok, t) => { console.log((ok ? '[OK]     ' : '[FEHLER] ') + t); if (!ok) befunde++; };

// ---- 1. Leisten Sim 1–3: Zielwerte (Regler-ID → Wert, Schalter, Modus)
const ZIELE = {
  sim1: [{ 's1-n': 10, 's1-k': 6 }, { 's1-n': 20, 's1-k': 12 }, { 's1-n': 8, 's1-k': 5 }, { 's1-n': 12, 's1-k': 10 }, { 's1-n': 24, 's1-k': 8 }],
  sim2: [{ 's2-n': 24 }, { 's2-n': 12 }, { schalter: true }, { 's2-n': 24 }, { 's2-n': 18 }, { 's2-n': 15 }],
  sim3: [{ 's3-b': 5, 's3-a': 3, 's3-d': 3, 's3-c': 2 }, { 's3-b': 3, 's3-a': 1, 's3-d': 4, 's3-c': 3 }, { 's3-b': 6, 's3-a': 5, 's3-d': 6, 's3-c': 5 },
         { 's3-b': 2, 's3-a': 1, 's3-d': 6, 's3-c': 1 }, { 's3-b': 3, 's3-a': 2, 's3-d': 2, 's3-c': 1 }, { 's3-b': 2, 's3-a': 1, 's3-d': 4, 's3-c': 1 }],
};
for (const [sim, ziele] of Object.entries(ZIELE)) {
  const r = await page.evaluate(([sim, ziele]) => {
    const fig = document.getElementById(sim), L = fig.querySelector('.leiste'), bt = L.querySelector('.ls-weiter'), aus = [];
    ziele.forEach((z, i) => {
      for (const [k, v] of Object.entries(z)) {
        if (k === 'schalter') { const s = fig.querySelector('.sim-schalter input'); s.checked = v; s.dispatchEvent(new Event('change')); continue; }
        const e = fig.querySelector('#' + k); e.max = 24; e.value = v; e.dispatchEvent(new Event('input'));
      }
      aus.push([i + 1, L.querySelector('.ls-ok').textContent.includes('✓'), L.querySelector('.ls-text').textContent.slice(0, 60)]);
      bt.click();
    });
    aus.push(['Ende', /Alle/.test(L.querySelector('.ls-text').textContent), L.querySelector('.ls-text').textContent]);
    return aus;
  }, [sim, ziele]);
  for (const [i, ok, t] of r) melde(ok, `${sim} Aufgabe ${i}: ${t}`);
}

// ---- 2. Schrittwähler
const SW = await page.evaluate(() => {
  const fig = document.getElementById('sim4'), L = fig.querySelector('.leiste'), bt = L.querySelector('.ls-weiter'), aus = [];
  const n = fig.__AUFG.length;
  function bereit(k){ return (k.t === 'op' && k.l.t === 'z' && k.r.t === 'z') || (k.t === 'p' && k.x.t === 'z'); }
  for (let i = 0; i < n; i++) {
    let falschGeprueft = false;
    for (let schritt = 0; schritt < 10; schritt++) {
      const knoepfe = [...fig.querySelectorAll('.sw-verlauf .aktuell .sw-op')];
      if (!knoepfe.length) break;
      // einmal je Aufgabe ein nicht bereites Zeichen antippen → Regelmeldung erwartet
      const rueck = fig.querySelector('.sw-rueck');
      if (!falschGeprueft && knoepfe.length > 1) {
        for (const b of knoepfe) { b.click(); if (rueck.classList.contains('falsch')) { falschGeprueft = rueck.textContent; break; } }
        if (!falschGeprueft) falschGeprueft = 'keine';
      }
      // bereites Zeichen finden: das, nach dessen Klick ein Eingabefeld erscheint
      let ok = false;
      for (const b of [...fig.querySelectorAll('.sw-verlauf .aktuell .sw-op')]) {
        b.click();
        const inp = fig.querySelector('.sw-feld input');
        if (inp) {
          inp.value = fig.__soll();
          fig.querySelector('.sw-pruefen').click();
          ok = !fig.querySelector('.sw-feld input');
          if (!ok) aus.push(['Schritt ' + (i + 1), false, 'Teilergebnis ' + inp.value + ' nicht angenommen: ' + rueck.textContent]);
          break;
        }
      }
      if (!ok) break;
    }
    const fertig = L.querySelector('.ls-ok').textContent.includes('✓');
    const SOLL = ['1/2', '2/3', '3/4', '5/18', '-1/2'];   // = zahlen.py, Sim4.1–5
    aus.push(['Aufgabe ' + (i + 1), fertig && fig.__ergebnis() === SOLL[i] && falschGeprueft && falschGeprueft !== 'keine', fig.__ergebnis() + ' (soll ' + SOLL[i] + ') · Fehlklick: ' + String(falschGeprueft).slice(0, 70)]);
    bt.click();
  }
  return aus;
});
for (const [i, ok, t] of SW) melde(ok, `sim4 ${i}: ${t}`);

// ---- 3. Verteilung
const V = await page.evaluate(() => {
  const aus = [];
  for (const [name, T] of Object.entries(window.__TYPEN)) {
    const schl = new Map(); let gesperrt = 0;
    for (let i = 0; i < 20000; i++) {
      let A = T.neu(); for (let v = 0; v < 60 && window.__SPERRE.indexOf(T.schl(A)) >= 0; v++) A = T.neu();
      const k = T.schl(A); if (window.__SPERRE.indexOf(k) >= 0) gesperrt++;
      schl.set(k, (schl.get(k) || 0) + 1);
    }
    const haeufigst = Math.max(...schl.values());
    aus.push([name, schl.size, gesperrt, haeufigst]);
  }
  return aus;
});
for (const [name, anz, ges, max] of V) melde(ges === 0 && anz >= 60 && max < 2000, `Verteilung ${name.padEnd(12)} ${anz} verschiedene Aufgaben in 20 000 Würfen, gesperrt gestellt: ${ges}, häufigste ${max}×`);

for (const e of jsFehler) melde(false, 'JS: ' + e);
await browser.close(); server.close();
console.log(befunde ? `\n${befunde} Befund(e).` : '\nALLES BESTANDEN');
process.exit(befunde ? 1 : 0);
