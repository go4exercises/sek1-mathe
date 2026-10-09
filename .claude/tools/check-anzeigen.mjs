// Laufzeit-Test: laedt jede geaenderte Seite, bewegt alle Regler und liest die
// Live-Anzeigen aus. Meldet JS-Fehler und jeden verbliebenen Trenn-Malpunkt.
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

const SEITEN = process.argv.slice(2);
const SEL = '.fl-eq, .ll-val, .lt-frage, .zs-formel, .formel-live, .fl-eval, #wg-eq, #pk-glg';

const browser = await chromium.launch();
let fehler = 0, seiten = 0;
for (const seite of SEITEN) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const konsole = [];
  page.on('pageerror', e => konsole.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') konsole.push('console: ' + m.text()); });
  await page.goto(pathToFileURL(resolve(seite)).href, { waitUntil: 'load' });
  await page.waitForTimeout(400);

  const vorher = await page.$$eval(SEL, els => els.map(e => e.innerText.replace(/\s+/g, ' ').trim()));

  // jeden Regler ein Stueck bewegen und jeden Knopf-Preset einmal klicken
  await page.evaluate(() => {
    document.querySelectorAll('input[type=range]').forEach(r => {
      const min = +r.min || 0, max = +r.max || 100, step = +r.step || 1;
      const neu = Math.min(max, Math.max(min, +r.value + step * 2));
      r.value = String(neu);
      r.dispatchEvent(new Event('input', { bubbles: true }));
      r.dispatchEvent(new Event('change', { bubbles: true }));
    });
  });
  await page.waitForTimeout(400);
  const nachher = await page.$$eval(SEL, els => els.map(e => e.innerText.replace(/\s+/g, ' ').trim()));

  const alle = [...vorher, ...nachher];
  // Trenner-Verdacht: '·' mit Relationszeichen links UND rechts
  const verdacht = alle.filter(t => {
    const teile = t.split('·');
    return teile.some((_, k) => k < teile.length - 1 &&
      /[=≤≥≈⇒→∈∉<>]/.test(teile[k].slice(-60)) && /[=≤≥≈⇒→∈∉<>]/.test(teile[k + 1].slice(0, 60)));
  });
  const tot = vorher.length && vorher.every((v, i) => v === nachher[i]);

  seiten++;
  const marker = (konsole.length || verdacht.length) ? '✗' : '✓';
  if (konsole.length || verdacht.length) fehler++;
  console.log(`${marker} ${seite}  (${vorher.length} Anzeigen${tot ? ', unveraendert' : ''})`);
  for (const t of nachher.filter(Boolean)) console.log(`     ${t.slice(0, 130)}`);
  for (const k of konsole.slice(0, 3)) console.log(`   !! ${k.slice(0, 160)}`);
  for (const v of verdacht) console.log(`   !! Trenner-Verdacht: ${v.slice(0, 130)}`);
  await page.close();
}
await browser.close();
console.log(`\n${seiten} Seiten geprueft, ${fehler} mit Befund`);
process.exit(fehler ? 1 : 0);
