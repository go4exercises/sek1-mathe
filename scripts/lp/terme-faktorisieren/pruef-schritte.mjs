// Prüft, was pruef-leiste und pruef-uebungen nicht sehen (HOWTO-leitprogramme §14/§15):
//   1. Jede Aufgabe der Leisten in Sim 1–4 ist lösbar: Zielwerte einstellen → ✓.
//   2. Termeingabe: gleichwertige Schreibweisen werden angenommen, Summen beim Faktorisieren und
//      nicht vollständig faktorisierte Produkte bekommen ihren eigenen Hinweis.
//   3. Verteilung: 20 000 Würfe je Übungstyp — wie viele verschiedene Aufgaben, wie viele gesperrt.
//
//   node scripts/lp/terme-faktorisieren/pruef-schritte.mjs        (vom Repo-Root; Exit 1 bei Befund)
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
await page.goto(`http://localhost:${server.address().port}/leitprogramme/terme-faktorisieren.html`);
await page.waitForTimeout(400);
let befunde = 0;
const melde = (ok, t) => { console.log((ok ? '[OK]     ' : '[FEHLER] ') + t); if (!ok) befunde++; };

// ---- 1. Leisten: Zielwerte (Regler-ID → Wert, in dieser Reihenfolge gesetzt)
const ZIELE = {
  sim1: [[['s1-a', 2], ['s1-b', 6]], [['s1-a', 6], ['s1-b', -4]], [['s1-a', 3], ['s1-b', 6]], [['s1-a', 5], ['s1-b', -2]], [['s1-a', 3], ['s1-b', -3]]],
  sim2: [[['s2-a', 3], ['s2-b', 1]], [['s2-a', 4], ['s2-b', -1]], [['s2-a', -2], ['s2-b', -5]], [['s2-a', 3], ['s2-b', -3]], [['s2-a', 4], ['s2-b', -2]]],
  sim3: [[['s3-a', 5], ['s3-b', 2]], [['s3-a', 5], ['s3-b', 3]], [['s3-a', 7], ['s3-b', 4]], [['s3-a', 5], ['s3-b', 1]]],
  sim4: [[['s4-m', 2], ['s4-n', 4]], [['s4-m', -3], ['s4-n', -5]], [['s4-m', 5], ['s4-n', -3]], [['s4-m', -3], ['s4-n', -3]], [['s4-m', 4], ['s4-n', -4]]],
};
for (const [sim, ziele] of Object.entries(ZIELE)) {
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

// ---- 2. Termeingabe
const E = await page.evaluate(() => {
  const T = window.__term, aus = [];
  const gleich = (s, p, v) => { const l = T.termLesen(s, v || 'x'); return !l.kaputt && T.pEq(l.p, p); };
  aus.push(['3x^2-2x+1 = 3x²−2x+1', gleich('3x²−2x+1', [1, -2, 3]) && gleich('3x^2-2x+1', [1, -2, 3])]);
  aus.push(['(x-3)(x+4), (x+4)(x-3), -(3-x)(x+4)', ['(x-3)(x+4)', '(x+4)(x-3)', '-(3-x)(x+4)'].every(s => gleich(s, [-12, 1, 1]))]);
  aus.push(['3a(2a-3) mit Variable a', gleich('3a(2a-3)', [0, -9, 6], 'a')]);
  aus.push(['(x+3)^2 = (x+3)(x+3), beide Produkt', ['(x+3)^2', '(x+3)(x+3)'].every(s => { const l = T.termLesen(s, 'x'); return T.produktBefund(l) === null; })]);
  aus.push(['x(x+6)+9 ist Summe', T.produktBefund(T.termLesen('x(x+6)+9', 'x')).art === 'summe']);
  aus.push(['a(6a-9) unvollständig', T.produktBefund(T.termLesen('a(6a-9)', 'a')).art === 'unvollstaendig']);
  aus.push(['2(x^2-9) unvollständig', T.produktBefund(T.termLesen('2(x^2-9)', 'x')).art === 'unvollstaendig']);
  aus.push(['2(x-3)(x+3) fertig', T.produktBefund(T.termLesen('2(x-3)(x+3)', 'x')) === null]);
  aus.push(['2x+3x nicht zusammengefasst', !T.zusammengefasst(T.termLesen('2x+3x', 'x').baum)]);
  aus.push(['x(x+5) nicht zusammengefasst', !T.zusammengefasst(T.termLesen('x(x+5)', 'x').baum)]);
  aus.push(['-x^2+5x zusammengefasst', T.zusammengefasst(T.termLesen('-x^2+5x', 'x').baum)]);
  aus.push(['3x2 abgelehnt (Hochzahl)', !!T.termLesen('3x2', 'x').kaputt]);
  aus.push(['y in x-Aufgabe abgelehnt', !!T.termLesen('y^2', 'x').kaputt]);
  aus.push(['offene Klammer abgelehnt', !!T.termLesen('(x+1', 'x').kaputt]);
  return aus;
});
for (const [t, ok] of E) melde(ok, 'Termeingabe: ' + t);

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
