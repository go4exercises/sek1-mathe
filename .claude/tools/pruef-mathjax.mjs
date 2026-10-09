// Prueft eine ausgelieferte Seite im Browser auf Formelsatz.
//
//   python3 -m http.server 8899 &
//   node .claude/tools/pruef-mathjax.mjs http://localhost:8899/grundlagen/g1-2-….html
//
// Meldet: Zahl der gesetzten Ausdruecke (mjx-container), Fehlerboxen und
// jede fehlgeschlagene Anfrage. Nicht ersetzbar durch verify_mathjax.js:
// jenes setzt mit mathjax-full aus node_modules und sieht darum nicht,
// ob unter vendor/mathjax/ eine nachgeladene Erweiterung fehlt.
import { chromium } from 'playwright';
const b = await chromium.launch();
const p = await b.newPage();
const f = [];
p.on('requestfailed', r => f.push('FEHLGESCHLAGEN ' + r.url().split('/').slice(-3).join('/')));
p.on('response', r => { if (r.status() >= 400) f.push(r.status() + ' ' + r.url().split('/').slice(-3).join('/')); });
p.on('console', m => { if (m.type() === 'error') f.push('KONSOLE ' + m.text().slice(0, 160)); });
await p.goto(process.argv[2], { waitUntil: 'networkidle' });
await p.waitForTimeout(1500);
const r = await p.evaluate(() => {
  const merr = [...document.querySelectorAll('mjx-merror, [data-mjx-error]')].map(e => e.textContent.trim().slice(0,80));
  const tc = [...document.querySelectorAll('mjx-container')].length;
  return { merr, tc };
});
console.log('mjx-container:', r.tc, '| merror:', r.merr.length, r.merr.slice(0,5));
console.log(f.length ? f.join('\n') : 'keine Netz-/Konsolenfehler');
await b.close();
