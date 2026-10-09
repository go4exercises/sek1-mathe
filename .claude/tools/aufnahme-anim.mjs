// Nimmt Zustände einer Animation als Bild auf — für Clips, die eine
// Animation der Lektionsseite erklären (Element `bild` im Drehbuch).
//
//   node .claude/tools/aufnahme-anim.mjs <plan.json>
//
// plan.json:
// {
//   "seite": "themen/p6-2-elektrizitaet.html",
//   "breite": 1100,                 // Fensterbreite, Standard 1100
//   "zustaende": [
//     { "datei": "clips/bilder/p6-2-a5-reihe-1.jpg",
//       "element": "#a3-cv",        // was aufgenommen wird (Standard: canvas)
//       "aktionen": [
//         { "klick": "[data-fi='pe']" },
//         { "wert": ["#a3-R1", 200] },   // Regler setzen, input+change feuern
//         { "js": "a3Render()" },        // beliebiger Ausdruck auf der Seite
//         { "warte": 400 }
//       ] }
//   ]
// }
//
// Die Bilder entstehen mit doppelter Pixeldichte als JPEG (Qualität 88):
// scharf auf der 1920er-Bühne, aber klein genug, dass ein Clip mit vier
// Aufnahmen unter einem halben Megabyte bleibt. Aktionen wirken
// nacheinander auf derselben Seite — ein Zustand baut auf dem vorigen auf.
// Laufzeitfehler der Seite werden gemeldet (Exit 1).
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const plan = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const wurzel = process.cwd();
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: plan.breite || 1100, height: 1000 }, deviceScaleFactor: 2 });
const fehler = [];
p.on('pageerror', e => fehler.push(e.message));
await p.goto('file://' + path.join(wurzel, plan.seite));
await p.waitForTimeout(1500);
for (const z of plan.zustaende) {
  for (const a of z.aktionen || []) {
    if (a.klick) await p.click(a.klick);
    if (a.wert) await p.evaluate(([sel, v]) => {
      const e = document.querySelector(sel); e.value = v;
      e.dispatchEvent(new Event('input', { bubbles: true }));
      e.dispatchEvent(new Event('change', { bubbles: true }));
    }, a.wert);
    if (a.js) await p.evaluate(a.js);
    await p.waitForTimeout(a.warte ?? 250);
  }
  await p.waitForTimeout(z.warte ?? 600);
  const el = await p.$(z.element || plan.element || 'canvas');
  if (!el) { fehler.push('Element fehlt: ' + (z.element || plan.element)); continue; }
  await el.scrollIntoViewIfNeeded();
  fs.mkdirSync(path.dirname(z.datei), { recursive: true });
  await el.screenshot({ path: z.datei, type: 'jpeg', quality: 88 });
  const kb = Math.round(fs.statSync(z.datei).size / 1024);
  console.log(`${z.datei}  ${kb} kB`);
}
await b.close();
if (fehler.length) { console.log('FEHLER:\n  ' + fehler.join('\n  ')); process.exit(1); }
