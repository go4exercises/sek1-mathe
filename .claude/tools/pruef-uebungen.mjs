// Prüft die Zufallsübungen eines Leitprogramms (.uebung[data-typ]) mit vielen Fällen.
//
//   node .claude/tools/pruef-uebungen.mjs leitprogramme/<name>.html [anzahl=1000]
//
// Je Übung und Fall: «Neue Zahlen», dann
//   1. Aufgabe und Rückmeldung ohne NaN, undefined, Infinity;
//   2. die richtige Eingabe wird als richtig gewertet;
//   3. jede gezielt falsche Eingabe wird als falsch gewertet, mit einer Meldung.
// Die richtige Eingabe ist A[feld] für jedes Feld; wo das nicht reicht, liefert der Typ
// sie selbst: TYPEN[typ].eingabe(A) → { feld: 'wert' }. Gezielte Fehler liefert
// TYPEN[typ].fehler(A) → [[{ feld: 'wert' }, 'Stichwort der Meldung' | null], …];
// ohne fehler() wird jedes Zahlenfeld um 1 verschoben und jedes Auswahlfeld umgestellt.
// Voraussetzung im Seitenskript: box.__aufgabe = A und box.__typ = T (Testhaken).
// Startet einen eigenen Server und lädt MathJax nicht (Formeln prüft pruef-mathjax.mjs). Exit 1 bei Fehlern.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const WURZEL = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const seite = process.argv[2];
const anzahl = +(process.argv[3] || 1000);
if (!seite) { console.error('Aufruf: node .claude/tools/pruef-uebungen.mjs leitprogramme/<name>.html [anzahl]'); process.exit(2); }

const TYP = { html: 'text/html', js: 'text/javascript', css: 'text/css', svg: 'image/svg+xml', json: 'application/json', woff2: 'font/woff2', png: 'image/png' };
const server = http.createServer((req, res) => {
  const p = path.join(WURZEL, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(WURZEL) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYP[path.extname(p).slice(1)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const port = server.address().port;

const browser = await chromium.launch();
const page = await browser.newPage();
const jsFehler = [];
page.on('pageerror', e => jsFehler.push(e.message));
await page.route('**/vendor/mathjax/**', r => r.abort());   // Formelsatz kostet je Aufgabe Zeit und prüft hier nichts
await page.goto(`http://localhost:${port}/${seite}`);
await page.waitForTimeout(500);

const ergebnis = await page.evaluate((N) => {
  const KAPUTT = /\bNaN\b|undefined|Infinity|\[object /;
  const aus = [];
  for (const box of document.querySelectorAll('.uebung[data-typ]')) {
    const typ = box.dataset.typ, r = { typ, faelle: 0, richtigOk: 0, fehlerOk: 0, fehlerFaelle: 0, meldungen: [] };
    const melde = m => { if (r.meldungen.length < 6) r.meldungen.push(m); };
    const neuKnopf = box.querySelector('.ue-neu'), pruef = box.querySelector('.ue-pruefen'), rueck = box.querySelector('.ue-rueck');
    if (!neuKnopf || !pruef || !rueck) { melde('Knöpfe .ue-neu/.ue-pruefen oder .ue-rueck fehlen'); aus.push(r); continue; }
    const setze = (werte) => {
      box.querySelectorAll('[data-f]').forEach(e => { if (e.tagName === 'INPUT') e.value = ''; });
      for (const k in werte) {
        const e = box.querySelector('[data-f="' + k + '"]'); if (!e) continue;
        e.value = werte[k];
        e.dispatchEvent(new Event(e.tagName === 'SELECT' ? 'change' : 'input', { bubbles: true }));
      }
    };
    const pruefe = (werte) => { setze(werte); pruef.disabled = false; pruef.click(); return [rueck.className, rueck.textContent]; };
    for (let k = 0; k < N; k++) {
      neuKnopf.click();
      const A = box.__aufgabe, T = box.__typ;
      if (!A || !T) { melde('Testhaken box.__aufgabe / box.__typ fehlt'); break; }
      r.faelle++;
      const txt = box.textContent;
      if (KAPUTT.test(txt)) melde('Aufgabe kaputt: ' + txt.slice(0, 120));
      const felder = [...box.querySelectorAll('[data-f]')].map(e => e.dataset.f);
      const soll = T.eingabe ? T.eingabe(A) : Object.fromEntries(felder.filter(f => A[f] !== undefined).map(f => [f, String(A[f])]));
      if (!T.eingabe && felder.some(f => A[f] === undefined)) { melde('Feld ohne A[feld] und ohne eingabe(): ' + felder.filter(f => A[f] === undefined).join(', ')); break; }
      let [kl, t] = pruefe(soll);
      if (kl.includes('richtig') && !KAPUTT.test(t)) r.richtigOk++;
      else melde('richtige Eingabe nicht angenommen: ' + JSON.stringify(soll) + ' → ' + t.slice(0, 120));
      neuKnopf.click(); const B = box.__aufgabe;     // nach ✓ ist «Prüfen» gesperrt: neue Aufgabe
      let proben;
      if (T.fehler) proben = T.fehler(B);
      else {
        const s2 = T.eingabe ? T.eingabe(B) : Object.fromEntries(felder.filter(f => B[f] !== undefined).map(f => [f, String(B[f])]));
        proben = Object.keys(s2).map(f => {
          const e = box.querySelector('[data-f="' + f + '"]'), w = { ...s2 };
          if (e.tagName === 'SELECT') { const o = [...e.options].map(o => o.value).filter(v => v && v !== s2[f]); if (!o.length) return null; w[f] = o[0]; }
          else w[f] = String(+s2[f] + 1);
          return [w, null];
        }).filter(Boolean);
      }
      for (const [w, stichwort] of proben) {
        r.fehlerFaelle++;
        [kl, t] = pruefe(w);
        const gut = !kl.includes('richtig') && t.trim().length > 3 && !KAPUTT.test(t) && (!stichwort || t.includes(stichwort));
        if (gut) r.fehlerOk++;
        else melde('falsche Eingabe ' + JSON.stringify(w) + ' (Aufgabe ' + JSON.stringify(B).slice(0, 100) + ') → ' + kl + ': ' + t.slice(0, 120) + (stichwort ? ' [erwartet: ' + stichwort + ']' : ''));
      }
    }
    aus.push(r);
  }
  return aus;
}, anzahl);

await browser.close(); server.close();
let fehler = jsFehler.length;
for (const e of jsFehler) console.log('[FEHLER] JS:', e);
if (!ergebnis.length) { console.log('[WARN] keine .uebung[data-typ] auf der Seite'); }
for (const r of ergebnis) {
  const ok = r.faelle > 0 && r.richtigOk === r.faelle && r.fehlerOk === r.fehlerFaelle && !r.meldungen.length;
  if (!ok) fehler++;
  console.log(`${ok ? '[OK]    ' : '[FEHLER]'} ${r.typ.padEnd(24)} ${r.faelle} Fälle · richtig ${r.richtigOk}/${r.faelle} · Fehler erkannt ${r.fehlerOk}/${r.fehlerFaelle}`);
  for (const m of r.meldungen) console.log('           ' + m);
}
console.log(fehler ? `\n${fehler} Problem(e).` : `\nALLE ÜBUNGEN BESTANDEN (${ergebnis.length} Typen × ${anzahl} Fälle)`);
process.exit(fehler ? 1 : 0);
