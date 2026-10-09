// Liest den sichtbaren Text jeder Clipzeile — zum Vergleich zweier Fassungen.
import { chromium } from 'playwright'; import fs from 'fs';
const b = await chromium.launch(); const aus = {};
for (const f of process.argv.slice(2)) {
  const p = await b.newPage({ viewport:{width:1920,height:1080} });
  await p.goto('file://' + fs.realpathSync(f) + '?render');
  await p.evaluate(() => window.MathJax?.startup?.promise ?? null);
  aus[f.split('/').pop()] = await p.evaluate(() =>
    [...document.querySelectorAll('.l:not(.step)')]
      .map(e => e.textContent.replace(/\s+/g, '').replace(/[⁢⁡]/g, '')));
  await p.close();
}
console.log(JSON.stringify(aus)); await b.close();
