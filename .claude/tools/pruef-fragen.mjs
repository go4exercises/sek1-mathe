// Prüft die Fragen im Clip («fragen» im Drehbuch, HOWTO-clips «Fragen im Clip») im echten Abspieler.
//
//   node .claude/tools/pruef-fragen.mjs <clip> [<clip> …]        (Name ohne .html, z. B. g3-3-lp-kontrolle-formen)
//
// Fälle, je Clip:
//   A  normaler Start: Frage 1 erscheint
//   B  erstes Bild 1.5 s verspätet (langsames Laden): Frage 1 erscheint trotzdem, an ihrer Stelle
//   B2 erstes Bild 6 s verspätet (Hintergrund-Tab): Frage 1 erscheint
//   C  R nach beantworteter Frage 1: Frage 1 kommt wieder
//   C2 R bei offener Frage: die Frage geht zu und kommt neu
//   D  Klick auf die Zeitleiste hinter Frage 2: keine Frage (bewusst gespult)
//   E  Sprung kurz vor Frage 2: Frage 2 erscheint
//   F  richtig beantwortet, sofort R: Frage 1 bleibt offen (altes Auto-Weiter schliesst sie nicht)
//   H  ganzer Durchlauf nach R, Start verspätet: jede Frage genau einmal, an ihrer Stelle
// Steht Frage 1 mitten im Clip (Strategiefrage nach einer Einführung, später als 2.5 s), springt
// jeder Fall zuerst per Zeitleiste kurz vor sie, und nach R ebenso; B und B2 (verspäteter Start)
// entfallen dann — sie prüfen den Clipanfang.
// Ton wird abgeschaltet (play() abgelehnt). Startet einen eigenen Server. Exit 1 bei Fehlern.
// Dauer: rund eine Minute je Clip (H spielt den ganzen Clip ab, bei später Frage entsprechend länger).
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const WURZEL = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const clips = process.argv.slice(2).map(c => c.replace(/^clips\//, '').replace(/\.(html|json)$/, ''));
if (!clips.length) { console.error('Aufruf: node .claude/tools/pruef-fragen.mjs <clip> [<clip> …]'); process.exit(2); }

const TYP = { html: 'text/html', js: 'text/javascript', css: 'text/css', svg: 'image/svg+xml', json: 'application/json', woff2: 'font/woff2', png: 'image/png', mp3: 'audio/mpeg' };
const server = http.createServer((req, res) => {
  const p = path.join(WURZEL, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(WURZEL) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYP[path.extname(p).slice(1)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const port = server.address().port;
const b = await chromium.launch();
const VERSPAETET = (ms) => `(() => { const o = window.requestAnimationFrame.bind(window); let n = 0;
  window.requestAnimationFrame = cb => (n++ === 0 ? setTimeout(() => o(cb), ${ms}) : o(cb)); })()`;
let fehlerGesamt = 0;

for (const clip of clips) {
  const URL = `http://localhost:${port}/clips/${clip}.html`;
  const ergebnisse = [];
  const pruefe = (fall, gut, info) => { ergebnisse.push([fall, gut, info]); if (!gut) fehlerGesamt++; };
  async function neu(init) {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 720 } });
    const p = await ctx.newPage();
    await p.addInitScript(() => { HTMLMediaElement.prototype.play = function () { return Promise.reject(new Error('stumm')); }; });
    if (init) await p.addInitScript(init);
    await p.goto(URL);
    return p;
  }
  const zustand = p => p.evaluate(() => ({
    t: +document.getElementById('tt').textContent.split(' ')[0],
    offen: document.getElementById('frage').style.display === 'block',
    text: document.querySelector('#frage .fr-text')?.textContent?.slice(0, 40) || '' }));
  const warte = async (p, ms = 4000) => { try { await p.waitForFunction(() => document.getElementById('frage').style.display === 'block', null, { timeout: ms }); return true; } catch { return false; } };
  const zu = p => p.waitForFunction(() => document.getElementById('frage').style.display !== 'block', null, { timeout: 5000 }).catch(() => {});
  const antworte = p => p.evaluate(() => {
    const F = FRAGEN.find(F => F.text.startsWith(document.querySelector('#frage .fr-text').textContent.slice(0, 20)));
    if (F.typ === 'wahl') { document.querySelectorAll('#frage .fr-knoepfe button')[F.richtig].click(); return; }
    const L = document.querySelector('.fr-tippbar'), svg = L.querySelector('svg');
    const [x0, x1, y0, y1, bb, h, rd] = L.querySelector('[data-fenster]').dataset.fenster.split(',').map(Number);
    const r = svg.getBoundingClientRect();
    // Ziel als Strecke [[x1, y1], [x2, y2]] (seit 08.10.2026): ihre Mitte antippen
    const z = Array.isArray(F.ziel[0]) ? [(F.ziel[0][0] + F.ziel[1][0]) / 2, (F.ziel[0][1] + F.ziel[1][1]) / 2] : F.ziel;
    const sx = rd + (z[0] - x0) / (x1 - x0) * (bb - 2 * rd), sy = h - rd - (z[1] - y0) / (y1 - y0) * (h - 2 * rd);
    document.getElementById('stage').dispatchEvent(new MouseEvent('click', { clientX: r.left + sx / bb * r.width, clientY: r.top + sy / h * r.height, bubbles: true }));
  });
  const nah = (t, soll) => Math.abs(t - soll) < 0.3;
  const zeitleiste = async (p, t) => {
    const r = await p.evaluate(() => { const r = document.getElementById('bar').getBoundingClientRect(); return [r.left, r.width, r.top + r.height / 2]; });
    const dur = await p.evaluate(() => DUR);
    await p.mouse.click(r[0] + t / dur * r[1], r[2]);
  };

  let p = await neu();
  const ft = await p.evaluate(() => (typeof FRAGEN === 'undefined' ? null : FRAGEN.map(F => F.t)));
  if (!ft || !ft.length) { console.log(`[WARN]   ${clip}: keine Fragen im Clip`); await p.context().close(); continue; }
  const mitte = ft[0] > 2.5;
  const vorFrage1 = async p => { if (mitte) { await p.waitForTimeout(300); await zeitleiste(p, ft[0] - 1.5); } };
  const nachR = async p => { await p.keyboard.press('r'); await vorFrage1(p); };
  await vorFrage1(p);
  pruefe(mitte ? 'A  Sprung vor Frage 1: Frage 1' : 'A  normaler Start: Frage 1', await warte(p, 3000), await zustand(p));
  await p.context().close();

  if (!mitte) {
  p = await neu(VERSPAETET(1500));
  { const ok = await warte(p, 3000), z = await zustand(p); pruefe('B  Start 1.5 s verspätet: Frage 1 an ihrer Stelle', ok && nah(z.t, ft[0]), z); }
  await p.context().close();

  p = await neu(VERSPAETET(6000));
  { const ok = await warte(p, 8000), z = await zustand(p); pruefe('B2 Start 6 s verspätet: Frage 1', ok && nah(z.t, ft[0]), z); }
  await p.context().close();
  }

  p = await neu(); await vorFrage1(p); await warte(p); await antworte(p); await zu(p); await p.waitForTimeout(800); await nachR(p);
  pruefe('C  R nach Frage 1: Frage 1 wieder', await warte(p, 3000), await zustand(p));
  await p.context().close();

  p = await neu(); await vorFrage1(p); await warte(p); await nachR(p);
  pruefe('C2 R bei offener Frage: Frage neu', await warte(p, 3000), await zustand(p));
  await p.context().close();

  if (ft.length > 1) {
    p = await neu(); await vorFrage1(p); await warte(p); await antworte(p); await zu(p);
    await zeitleiste(p, Math.min(ft[1] + 1.5, ft[2] !== undefined ? ft[2] - 0.5 : ft[1] + 1.5)); await p.waitForTimeout(600);
    { const z = await zustand(p); pruefe('D  gespult hinter Frage 2: keine Frage', !z.offen, z); }
    await p.context().close();

    p = await neu(); await vorFrage1(p); await warte(p); await antworte(p); await zu(p);
    await zeitleiste(p, ft[1] - 0.8);
    { const ok = await warte(p, 3000), z = await zustand(p); pruefe('E  Sprung kurz vor Frage 2: Frage 2', ok && nah(z.t, ft[1]), z); }
    await p.context().close();
  }

  p = await neu(); await vorFrage1(p); await warte(p); await antworte(p); await p.waitForTimeout(100); await nachR(p);
  await warte(p, 2000); await p.waitForTimeout(1800);
  { const z = await zustand(p); pruefe('F  richtig, sofort R: Frage 1 bleibt offen', z.offen, z); }
  await p.context().close();

  p = await neu(VERSPAETET(1500)); await p.keyboard.press('r');
  { const gesehen = [];
    for (let k = 0; k <= ft.length; k++) {
      if (!(await warte(p, 20000 + 1000 * ((ft[k] ?? (ft[k - 1] || 0)) - (ft[k - 1] || 0))))) break;
      gesehen.push((await zustand(p)).t); await antworte(p); await zu(p);
    }
    pruefe('H  Durchlauf: jede Frage genau einmal', gesehen.length === ft.length && gesehen.every((t, i) => nah(t, ft[i])), { gesehen, soll: ft }); }
  await p.context().close();

  const schlecht = ergebnisse.filter(e => !e[1]).length;
  console.log(`${schlecht ? '[FEHLER]' : '[OK]    '} ${clip}: ${ergebnisse.length - schlecht}/${ergebnisse.length} Fälle`);
  for (const [fall, gut, info] of ergebnisse) if (!gut) console.log(`           ${fall} — ${JSON.stringify(info)}`);
}
await b.close(); server.close();
console.log(fehlerGesamt ? `\n${fehlerGesamt} Fall/Fälle fehlgeschlagen.` : '\nALLE FRAGEN BESTANDEN');
process.exit(fehlerGesamt ? 1 : 0);
