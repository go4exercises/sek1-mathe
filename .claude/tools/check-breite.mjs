// Prueft bei 360 px, ob eine Live-Anzeige aus ihrem Kasten laeuft.
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
const browser = await chromium.launch();
let n = 0;
for (const seite of process.argv.slice(2)) {
  const page = await browser.newPage({ viewport: { width: 360, height: 800 } });
  await page.goto(pathToFileURL(resolve(seite)).href, { waitUntil: 'load' });
  await page.waitForTimeout(300);
  const ueber = await page.$$eval('.fl-eq, .ll-val, .lt-frage, .zs-formel',
    els => els.filter(e => e.scrollWidth > e.clientWidth + 2)
              .map(e => (e.id || e.className) + ' :: ' + e.innerText.replace(/\s+/g,' ').trim().slice(0,80)
                      + ` (${e.scrollWidth}>${e.clientWidth})`));
  const body = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 2);
  if (ueber.length || body) { n++; console.log(`✗ ${seite}${body ? '  [Seite scrollt horizontal]' : ''}`); ueber.forEach(u => console.log('   ' + u)); }
  await page.close();
}
await browser.close();
console.log(n ? `\n${n} Seiten mit Ueberlauf` : '\nkein Ueberlauf bei 360 px');
