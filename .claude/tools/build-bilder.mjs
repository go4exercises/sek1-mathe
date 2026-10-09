// build-bilder.mjs — erzeugt die Bild-Assets fuer die Auffindbarkeit:
//   favicon-32.png (32x32), apple-touch-icon.png (180x180)  aus favicon.svg
//   og-bild.png (1200x630)                                   aus einer HTML-Vorlage
//
// Aufruf vom Repo-Root (Chromium kommt aus devDependencies playwright):
//   node .claude/tools/build-bilder.mjs
//
// Laeuft nur bei Bedarf — die PNGs sind versioniert und aendern sich nur,
// wenn Farben, Wortlaut oder Schrift der Vorlage angepasst werden.
// Die Schriften kommen von Google Fonts (wie auf den Seiten selbst), das
// Skript braucht also einmalig eine Netzverbindung.

import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const REPO = process.cwd();
const svg = readFileSync(resolve(REPO, 'favicon.svg'), 'utf8');

const FONTS = 'https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,700&family=JetBrains+Mono:wght@400;700&display=swap';

const OG = `<!doctype html><html><head><meta charset="utf-8">
<link href="${FONTS}" rel="stylesheet">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { width:1200px; height:630px; background:#f8f6f1; font-family:'Source Serif 4',serif;
         display:flex; align-items:center; }
  .balken { width:22px; height:100%; background:#0f6b6b; }
  .inhalt { padding:0 70px; }
  .ew  { font-family:'JetBrains Mono',monospace; font-size:23px; letter-spacing:1.5px;
         color:#5c5850; margin-bottom:26px; }
  .ew b { color:#0f6b6b; font-weight:700; }
  h1   { font-size:92px; font-weight:700; line-height:1.06; color:#1c1a17; letter-spacing:-1px; }
  h1 span { color:#0f6b6b; display:block; }   /* Zusatz auf eigene Zeile  */
  .ut  { font-size:38px; color:#3d3a35; margin-top:34px; line-height:1.3; }
  .url { font-family:'JetBrains Mono',monospace; font-size:22px; color:#5c5850; margin-top:30px; }
</style></head><body>
<div class="balken"></div>
<div class="inhalt">
  <div class="ew">Mathematik für die <b>Sekundarstufe I</b></div>
  <h1>Sek1-Mathe <span>begreifbar</span></h1>
  <div class="ut">Interaktives Lehrmittel mit Animationen, Aufgaben und Formelsammlung</div>
  <div class="url">sek1-mathe.begreifbar.ch · CC BY-NC 4.0</div>
</div>
</body></html>`;

const IKON = (px) => `<!doctype html><html><head><meta charset="utf-8"><style>
  * { margin:0; padding:0; } html,body { width:${px}px; height:${px}px; }
  svg { width:${px}px; height:${px}px; display:block; }
</style></head><body>${svg}</body></html>`;

const browser = await chromium.launch();

for (const [datei, px] of [['favicon-32.png', 32], ['apple-touch-icon.png', 180]]) {
  const ctx = await browser.newContext({ viewport: { width: px, height: px }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.setContent(IKON(px));
  await page.screenshot({ path: resolve(REPO, datei), omitBackground: false });
  await ctx.close();
  console.log(`  ${datei.padEnd(22)} ${px}x${px}`);
}

{
  const ctx = await browser.newContext({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.setContent(OG, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  // Kontrolle: die Schrift muss wirklich geladen sein, sonst faellt das Bild
  // stillschweigend auf eine Systemschrift zurueck.
  const ok = await page.evaluate(() => document.fonts.check("700 92px 'Source Serif 4'"));
  if (!ok) { console.error('FEHLER: Source Serif 4 nicht geladen — Netzverbindung?'); process.exit(1); }
  await page.screenshot({ path: resolve(REPO, 'og-bild.png') });
  await ctx.close();
  console.log('  og-bild.png            1200x630');
}

await browser.close();
console.log('Bild-Assets geschrieben.');
