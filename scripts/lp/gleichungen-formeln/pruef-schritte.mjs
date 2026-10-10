// Prüft, was pruef-leiste und pruef-uebungen nicht sehen (HOWTO-leitprogramme §14/§15):
//   1. Jede Aufgabe der Leisten in Sim 1–4 ist lösbar (Chips streichen, Regler, Kette) → ✓; falsches Paar abgelehnt.
//   2. Eingabe: Bruchterme (gleichwertig, gekürzt, ein Bruchstrich), Lösungsmengen, Zahlen, Formeln.
//   3. Verteilung: 20 000 Würfe je Übungstyp — wie viele verschiedene Aufgaben, wie viele gesperrt.
//
//   node scripts/lp/gleichungen-formeln/pruef-schritte.mjs        (vom Repo-Root; Exit 1 bei Befund)
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
await page.goto(`http://localhost:${server.address().port}/leitprogramme/gleichungen-formeln.html`);
await page.waitForTimeout(400);
let befunde = 0;
const melde = (ok, t) => { console.log((ok ? '[OK]     ' : '[FEHLER] ') + t); if (!ok) befunde++; };

// ---- 1. Leisten: Aktionen je Aufgabe
const LOES = {
  sim1: [{ paare: true }, { paare: true }, { paare: true }, { paare: true }, { fertig: true }],
  sim2: [{ 's2-k': 6, 's2-e': 1 }, { 's2-k': 3, 's2-e': 2 }, { 's2-k': 1, 's2-e': 1, p: true }, { 's2-k': 1, 's2-e': 0, p: true, q: true }, { 's2-k': 12, 's2-e': 1 }],
  sim3: [{ 's3-k': -1, 's3-m': -3, t: 3 }, { 's3-k': -3, 's3-m': 2, t: 4 }, { 's3-k': -2, 's3-m': 0, t: 3 }, { 's3-k': -3 }, { 's3-k': 2, 's3-m': 9, t: 3 }],
  sim4: [{ ops: [': v'] }, { ops: [': I'] }, { ops: ['+ 5', ': 4'] }, { ops: ['· 2', ': b'] }, { ops: [': 2', '− a'] }],
};
for (const [sim, ziele] of Object.entries(LOES)) {
  const r = await page.evaluate(([sim, ziele]) => {
    const fig = document.getElementById(sim), L = fig.querySelector('.leiste'), bt = L.querySelector('.ls-weiter'), aus = [];
    ziele.forEach((z, i) => {
      const vorher = L.querySelector('.ls-ok').textContent.includes('✓');
      if (z.paare) {                          // Sim 1: jeden Zähler-Faktor mit einem gleichen Nenner-Faktor streichen
        for (let runde = 0; runde < 6; runde++) {
          const oben = [...fig.querySelectorAll('.chip.zaehler:not(.weg)')];
          let getan = false;
          for (const o of oben) { const u = [...fig.querySelectorAll('.chip.nenner:not(.weg)')].find(c => c.textContent === o.textContent);
            if (u) { o.click(); fig.querySelector('.chip.nenner:not(.weg)[data-u="' + u.dataset.u + '"]').click(); getan = true; break; } }
          if (!getan) break;
        }
      }
      if (z.fertig) fig.querySelector('.kuerz-fertig').click();
      if (z.ops) z.ops.forEach(o => fig.querySelector('.kette-knoepfe [data-op="' + o + '"]').click());
      for (const [k, v] of Object.entries(z)) {
        if (k === 'p' || k === 'q') { const c = fig.querySelector('#s2-' + k); c.checked = v; c.dispatchEvent(new Event('change')); continue; }
        if (k === 't') { const s = fig.querySelector('select.sim-wahl'); s.value = String(v); s.dispatchEvent(new Event('change')); continue; }
        if (['paare', 'fertig', 'ops'].includes(k)) continue;
        const e = fig.querySelector('#' + k); e.value = v; e.dispatchEvent(new Event('input'));
      }
      aus.push([i + 1, !vorher && L.querySelector('.ls-ok').textContent.includes('✓'), L.querySelector('.ls-text').textContent.slice(0, 60)]);
      bt.click();
    });
    aus.push(['Ende', /Alle/.test(L.querySelector('.ls-text').textContent), L.querySelector('.ls-text').textContent]);
    return aus;
  }, [sim, ziele]);
  for (const [i, ok, t] of r) melde(ok, `${sim} Aufgabe ${i}: ${t}`);
}
// Sim 1: falsches Paar wird abgelehnt
melde(await page.evaluate(() => { const fig = document.getElementById('sim1'); fig.querySelector('.ls-neu') && fig.querySelector('.ls-neu').click();
  const o = fig.querySelector('.chip.zaehler'), text = o.textContent; o.click();     // Chips werden nach jedem Klick neu gezeichnet
  const u = [...fig.querySelectorAll('.chip.nenner')].find(c => c.textContent !== text); u.click();
  return /verschiedene Faktoren/.test(fig.textContent) && !fig.querySelector('.chip.weg'); }), 'sim1: ungleiche Faktoren lassen sich nicht streichen');

// ---- 2. Eingabe
const E = await page.evaluate(() => {
  const T = window.__term, aus = [];
  const r = (s) => T.termLesen(s, 'x');
  aus.push(['(x-3)/(x+3) gleich (3-x)/(-x-3)', T.rEq(r('(x-3)/(x+3)').r, r('(3-x)/(-x-3)').r)]);
  aus.push(['3/(2x) = 1.5/x', T.rEq(r('3/(2x)').r, r('1.5/x').r)]);
  aus.push(['3/2x abgelehnt', !!r('3/2x').kaputt]);
  aus.push(['x/3-2/3 nicht auf einem Bruchstrich', !T.einBruch(r('x/3-2/3').baum)]);
  aus.push(['-(x-2)/3 auf einem Bruchstrich', T.einBruch(r('-(x-2)/3').baum)]);
  aus.push(['(x^2-9)/(2x+6) nicht gekürzt', !!T.gemeinsam(r('(x^2-9)/(2x+6)').r)]);
  aus.push(['(2x+4)/(4x) nicht gekürzt (Zahl 2)', !!T.gemeinsam(r('(2x+4)/(4x)').r)]);
  aus.push(['(x-3)/(x+3) gekürzt', !T.gemeinsam(r('(x-3)/(x+3)').r)]);
  aus.push(['(2x+1)/(4x^2-1) nicht gekürzt (Nullstelle −1/2)', !!T.gemeinsam(r('(2x+1)/(4x^2-1)').r)]);
  aus.push(['Menge {} leer', T.mengeLesen('{ }').art === 'leer' && T.mengeLesen('leer').art === 'leer']);
  aus.push(['Menge Q alle', T.mengeLesen('Q').art === 'alle' && T.mengeLesen('ℚ').art === 'alle']);
  aus.push(['Menge {5}, x=5, 7/3, -2.5', T.mengeLesen('{5}').w[0] === 5 && T.mengeLesen('x=5').w[0] === 5 && T.mengeLesen('7/3').w[1] === 3 && T.mengeLesen('-2.5').w[0] === -5]);
  aus.push(['Dezimalkomma abgelehnt', !!T.zahlLesen('2,5').kaputt]);
  aus.push(['Formel: t= vorne erlaubt', !T.termLesen('t=s/v', 'stv', 't').kaputt]);
  aus.push(['Formel: fremde Grösse abgelehnt', !!T.termLesen('s/w', 'stv', 't').kaputt]);
  return aus;
});
for (const [t, ok] of E) melde(ok, 'Eingabe: ' + t);

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
