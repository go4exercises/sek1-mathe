#!/usr/bin/env node
/**
 * render-check.mjs — Render-Kontrolle der Themenseiten bei 1280 und 360 px.
 *
 * Prueft, was der Pre-Flight prinzipiell nicht pruefen kann: jsdom hat kein
 * Layout, MathJax-SVG-Breiten existieren dort nicht. Hier laeuft ein echter
 * Chromium, MathJax rendert, danach wird gemessen.
 *
 * Drei Befunde:
 *   1. OVERFLOW   — body.scrollWidth > clientWidth (Seite laesst sich seitlich ziehen)
 *   2. GECLIPPT   — Formel/Tabelle ragt hinaus UND ein Vorfahr hat overflow:hidden.
 *                   Das ist der gefaehrliche Fall: unsichtbar, weil ein Vorfahr
 *                   kappt — der Inhalt fehlt einfach.
 * Alle <details> werden vor der Messung geoeffnet — die Mini-Check-Loesungen
 * sind sonst zu und ihre Formeln ungemessen. Achtung: minicheck.js ist ein
 * Akkordeon und laesst hoechstens ein details.minicheck offen. Ein blosses
 * «alle oeffnen» klappt sich also selbst wieder zu und misst pro Seite nur
 * einen Mini-Check. Deshalb wird jeder einzeln geoeffnet und gemessen.
 *
 * Dazu ein Vorher/Nachher-Vergleich fuer Eingriffe an der Formel-Darstellung:
 * overflow != visible auf einem inline-block verschiebt dessen Baseline. Ein
 * Absolutwert sagt darueber nichts (mehrzeilige Elternelemente verrauschen ihn),
 * die Differenz gegen einen frueheren Stand dagegen schon.
 *
 * Aufruf (vom Repo-Root):
 *   npm run render-check                 alle Themenseiten (grundlagen/ und schwerpunkt/)
 *   node .claude/tools/render-check.mjs grundlagen/g1-4-zehnerpotenzen-quadratwurzeln.html
 *   node .claude/tools/render-check.mjs --shots            zusaetzlich check_*.png
 *   node .claude/tools/render-check.mjs --snapshot vorher.json    Geometrie sichern
 *   node .claude/tools/render-check.mjs --vergleich vorher.json   dagegen pruefen
 *
 * Exit-Code 1, sobald Overflow oder geclippter Inhalt gefunden wird.
 */
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const argv = process.argv.slice(2);
const shots = argv.includes('--shots');
const flagWert = (name) => { const i = argv.indexOf(name); return i >= 0 ? argv[i + 1] : null; };
const snapshotZiel = flagWert('--snapshot');
const vergleichQuelle = flagWert('--vergleich');
const dateien = argv.filter((a, i) =>
  !a.startsWith('--') && argv[i - 1] !== '--snapshot' && argv[i - 1] !== '--vergleich');
const root = process.cwd();

const seiten = dateien.length
  ? dateien.map(f => path.relative(root, path.resolve(root, f)))
  : ['grundlagen', 'schwerpunkt'].flatMap(d => fs.readdirSync(path.join(root, d))
      .filter(f => f.endsWith('.html')).sort().map(f => d + '/' + f));

const BREITEN = [1280, 360];

/* Im Seitenkontext: alles messen, was nicht umbrechen kann.
   mcIndex begrenzt die Messung auf einen einzelnen Mini-Check — sonst wuerde
   der uebrige Seiteninhalt bei jedem Durchgang erneut gezaehlt. */
function messen(mcIndex) {
  const cw = document.documentElement.clientWidth;
  const befund = { sw: document.body.scrollWidth, cw, geclippt: [], geometrie: [] };
  const wurzel = mcIndex == null
    ? document.querySelector('main') || document.body
    : document.querySelectorAll('details.minicheck')[mcIndex];
  if (!wurzel) return befund;

  for (const e of wurzel.querySelectorAll('mjx-container, table, pre, img')) {
    if (e.closest('mjx-assistive-mml')) continue;   // unsichtbare Screenreader-Kopie
    /* Chromium legt den Inhalt eines geschlossenen <details> bereits aus (fuer
       Suchen-auf-der-Seite). Im Seiten-Durchgang wuerden die Mini-Checks damit
       doppelt gezaehlt — sie kommen weiter unten einzeln und im geoeffneten
       Zustand dran. */
    if (mcIndex == null && e.closest('details.minicheck')) continue;
    const b = e.getBoundingClientRect();
    if (b.width === 0 || b.right <= cw + 1) continue;

    let a = e.parentElement, kappt = null;
    while (a) {
      const ov = getComputedStyle(a).overflowX;
      if (ov === 'hidden' || ov === 'clip') { kappt = a.tagName.toLowerCase() + '.' + String(a.className).split(' ')[0]; break; }
      if (ov === 'auto' || ov === 'scroll') break;   // scrollt in sich selbst — in Ordnung
      a = a.parentElement;
    }
    if (kappt) befund.geclippt.push({
      ueber: Math.round(b.right - cw), kappt,
      txt: (e.textContent || '').replace(/\s+/g, ' ').slice(0, 60)
    });
  }

  /* Lage jeder Inline-Formel relativ zu ihrem Elternelement — als Vergleichsbasis.
     Absolut ist der Wert nichtssagend, die Differenz gegen einen frueheren Stand
     zeigt dagegen genau, ob ein CSS-Eingriff die Formeln verschoben hat. */
  let i = 0;
  for (const e of wurzel.querySelectorAll('mjx-container:not([display="true"])')) {
    const p = e.parentElement;
    if (!p || e.closest('mjx-assistive-mml')) continue;
    if (mcIndex == null && e.closest('details.minicheck')) continue;
    const b = e.getBoundingClientRect(), pb = p.getBoundingClientRect();
    if (b.height === 0) continue;
    befund.geometrie.push({
      k: i++ + '|' + (e.textContent || '').replace(/\s+/g, '').slice(0, 24),
      dy: Math.round((b.top - pb.top) * 10) / 10,
      h: Math.round(b.height * 10) / 10
    });
  }
  return befund;
}

const alt = vergleichQuelle ? JSON.parse(fs.readFileSync(vergleichQuelle, 'utf8')) : null;
const neu = {};

const browser = await chromium.launch();
let fehler = 0, geclipptGes = 0, verschobenGes = 0;

for (const breite of BREITEN) {
  const ctx = await browser.newContext({ viewport: { width: breite, height: 900 } });
  console.log(`\n════ ${breite} px ${'═'.repeat(52)}`);

  for (const s of seiten) {
    const page = await ctx.newPage();
    await page.goto('file://' + path.join(root, s));
    await page.waitForTimeout(1000);

    /* Erst alles ausser den Mini-Check-Akkordeons oeffnen (Loesungswege,
       Herleitungen). Die bleiben offen, das Akkordeon greift nur auf
       details.minicheck. */
    await page.evaluate(() => document.querySelectorAll('details:not(.minicheck)')
      .forEach(d => (d.open = true)));
    await page.waitForTimeout(1500);

    const r = await page.evaluate(messen, null);

    /* Dann jeden Mini-Check einzeln — das Akkordeon schliesst den vorigen. */
    const anzahlMc = await page.evaluate(() => document.querySelectorAll('details.minicheck').length);
    for (let i = 0; i < anzahlMc; i++) {
      await page.evaluate(k => {
        const d = document.querySelectorAll('details.minicheck')[k];
        d.open = true;
        d.querySelectorAll('details').forEach(x => (x.open = true));
      }, i);
      await page.waitForTimeout(700);   // MathJax rendert das Aufgeklappte nach
      const t = await page.evaluate(messen, i);
      r.sw = Math.max(r.sw, t.sw);
      r.geclippt.push(...t.geclippt);
      r.geometrie.push(...t.geometrie.map(g => ({ ...g, k: 'mc' + i + '-' + g.k })));
    }
    const name = path.basename(s);
    const schluessel = breite + ' ' + s;
    neu[schluessel] = r.geometrie;

    /* Verschiebungen gegen den gesicherten Stand */
    const verschoben = [];
    if (alt && alt[schluessel]) {
      const vorher = new Map(alt[schluessel].map(g => [g.k, g]));
      for (const g of r.geometrie) {
        const v = vorher.get(g.k);
        if (v && Math.abs(g.dy - v.dy) > 1) verschoben.push({ k: g.k, von: v.dy, auf: g.dy });
      }
    }

    const ok = r.sw <= r.cw && r.geclippt.length === 0 && verschoben.length === 0;
    console.log(`${ok ? '  ok  ' : '  !!  '}${name.padEnd(40)} scrollWidth=${r.sw} clientWidth=${r.cw}`);

    if (r.sw > r.cw) { console.log(`        OVERFLOW ${r.sw - r.cw} px`); fehler++; }
    for (const g of r.geclippt) {
      console.log(`        GECLIPPT ${String(g.ueber).padStart(3)} px von ${g.kappt}  « ${g.txt} »`);
      geclipptGes++; fehler++;
    }
    for (const v of verschoben.slice(0, 5)) {
      console.log(`        VERSCHOBEN ${v.von} → ${v.auf} px  « ${v.k.split('|')[1]} »`);
    }
    if (verschoben.length > 5) console.log(`        … und ${verschoben.length - 5} weitere`);
    verschobenGes += verschoben.length;
    if (shots) await page.screenshot({ path: `check_${name.replace(/\.html$/, '')}_${breite}.png`, fullPage: true });
    await page.close();
  }
  await ctx.close();
}
await browser.close();

if (snapshotZiel) {
  fs.writeFileSync(snapshotZiel, JSON.stringify(neu));
  console.log(`\nGeometrie gesichert: ${snapshotZiel}`);
}

console.log('\n' + '─'.repeat(70));
console.log(`geclippte Formeln/Tabellen: ${geclipptGes}`);
if (alt) console.log(`vertikal verschobene Inline-Formeln: ${verschobenGes}`);
console.log(fehler === 0 ? 'RENDER-CHECK BESTANDEN' : `RENDER-CHECK FEHLGESCHLAGEN (${fehler} Befunde)`);
process.exit(fehler === 0 ? 0 : 1);
