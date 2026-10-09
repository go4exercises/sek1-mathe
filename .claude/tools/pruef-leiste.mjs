// Prüft die Aufgabenleisten (.leiste) in den Simulationen eines Leitprogramms.
//
//   node .claude/tools/pruef-leiste.mjs leitprogramme/<name>.html
//
// Je Leiste werden alle Aufgaben übersprungen, ohne einen Regler zu bewegen:
//   1. Keine Aufgabe ist schon gelöst, wenn sie erscheint (Ziel ≠ Startzustand).
//   2. Am Ende steht nicht «Alle … gelöst», sondern der Stand mit «übersprungen».
//   3. «zu den offenen» führt zurück zur ersten Aufgabe.
// Ob jede Aufgabe lösbar ist, sieht das Werkzeug nicht — das braucht den Durchgang von
// Hand oder ein Skript mit den Zielwerten (HOWTO-leitprogramme §14). Exit 1 bei Fehlern.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const WURZEL = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const seite = process.argv[2];
if (!seite) { console.error('Aufruf: node .claude/tools/pruef-leiste.mjs leitprogramme/<name>.html'); process.exit(2); }

const TYP = { html: 'text/html', js: 'text/javascript', css: 'text/css', svg: 'image/svg+xml', json: 'application/json', woff2: 'font/woff2', png: 'image/png' };
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
await page.goto(`http://localhost:${server.address().port}/${seite}`);
await page.waitForTimeout(500);

const ergebnis = await page.evaluate(() => {
  const aus = [];
  document.querySelectorAll('.leiste').forEach((L, k) => {
    const fig = L.closest('figure, .sim, section') || L.parentElement;
    const name = (fig && fig.id) || ('Leiste ' + (k + 1));
    const r = { name, aufgaben: 0, meldungen: [] };
    const nr = () => L.querySelector('.ls-nr')?.textContent || '', tx = () => L.querySelector('.ls-text')?.textContent || '';
    const ok = () => (L.querySelector('.ls-ok')?.textContent || '').includes('✓');
    const bt = L.querySelector('.ls-weiter');
    if (!bt) { r.meldungen.push('Knopf .ls-weiter fehlt'); aus.push(r); return; }
    const m = nr().match(/^(\d+)\/(\d+)$/);
    if (!m) { r.meldungen.push('Zähler «i/n» fehlt: ' + nr()); aus.push(r); return; }
    const n = +m[2]; r.aufgaben = n;
    for (let i = 0; i < n; i++) {
      if (ok()) r.meldungen.push(`Aufgabe ${i + 1} ist gelöst, sobald sie erscheint: «${tx().slice(0, 70)}»`);
      bt.click();
    }
    const ende = tx();
    if (/alle/i.test(ende) && !/übersprungen/.test(ende)) r.meldungen.push('nach reinem Überspringen steht: «' + ende.slice(0, 80) + '»');
    else if (!/übersprungen/.test(ende)) r.meldungen.push('Schluss ohne Stand «… übersprungen»: «' + ende.slice(0, 80) + '»');
    bt.click();
    if (nr() !== '1/' + n) r.meldungen.push('«zu den offenen» führt nicht zu Aufgabe 1, sondern zu «' + nr() + '»');
    aus.push(r);
  });
  return aus;
});

await browser.close(); server.close();
let fehler = jsFehler.length;
for (const e of jsFehler) console.log('[FEHLER] JS:', e);
if (!ergebnis.length) console.log('[WARN] keine .leiste auf der Seite');
for (const r of ergebnis) {
  if (r.meldungen.length) fehler++;
  console.log(`${r.meldungen.length ? '[FEHLER]' : '[OK]    '} ${r.name.padEnd(16)} ${r.aufgaben} Aufgaben`);
  for (const m of r.meldungen) console.log('           ' + m);
}
console.log(fehler ? `\n${fehler} Problem(e).` : `\nALLE LEISTEN BESTANDEN (${ergebnis.length})`);
process.exit(fehler ? 1 : 0);
