#!/usr/bin/env node
/**
 * scan-live.mjs — sucht den Malpunkt als Trennzeichen (STYLEGUIDE §2.1).
 *
 * In Rechen- und Wertanzeigen bedeutet `·` ausschliesslich Multiplikation.
 * Der Blick in den Quelltext genuegt dafuer nicht, aus zwei Gruenden:
 *
 *   1. Die meisten Anzeigen entstehen erst zur Laufzeit — aus JS-Stringliteralen,
 *      oft in Zweigen, die nur ein bestimmter Reglerwert oder Modus erreicht.
 *   2. Animationsbeschriftungen stehen auf einem **Canvas** und damit ueberhaupt
 *      nicht im DOM. In Physik lagen fuenf von sieben Fundstellen genau dort;
 *      ein Werkzeug, das nur `innerText` liest, sieht sie nicht.
 *
 * Darum liest dieses Skript beides: den sichtbaren Text des Inhaltsbereichs **und**
 * jeden `fillText`-Aufruf der Canvas — im Startzustand, nach jedem Umschaltknopf
 * und mit jedem Regler an beiden Anschlaegen.
 *
 *   node .claude/tools/scan-live.mjs grundlagen/*.html schwerpunkt/*.html
 *   node .claude/tools/scan-live.mjs grundlagen/g3-2-lineare-funktionen.html --alle
 *
 * Ohne `--alle` werden nur **Verdachtsfaelle** gemeldet (siehe verdacht() unten).
 * Mit `--alle` kommt jede Zeile mit `·` aus dem Inhaltsbereich — fuer die
 * gruendliche Sichtung, etwa beim Stichwort «Stilcheck».
 *
 * Exit 1, sobald ein Verdachtsfall gefunden wurde.
 */
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

// Wo Werte angezeigt werden. Titel, Navigation, Fusszeile und Bedienhinweise
// stehen bewusst NICHT hier: dort ist `·` etablierte Typografie (STYLEGUIDE §2.1).
// Mathe hat keine einheitliche Anzeigeklasse: Live-Formeln, Wertetabellen,
// Umformungsstapel, Quizkarten und Canvas-Legenden tragen je eigene, oft
// seitenspezifische Container. Eine Positivliste wie in Physik verfehlt darum
// die Hälfte (gemessen am 13.09.2026). Gelesen wird deshalb der ganze
// Inhaltsbereich — ausgeblendet nur die Zonen, in denen `·` etablierte
// Typografie ist (STYLEGUIDE §2.1): Titel, Widget-Köpfe, Linkkarten, Fusszeile.
const BEREICH = 'main';
const AUSSCHLUSS = 'footer, nav, h1, h2, h3, h4, .page-titel, .widget-header, '
  + '.widget-titelzeile, .anim-titel, .block-titel, .links-grid, .toc-wrap';
const KNOEPFE = '.typ-btn, .preset-btn, .zs-btn, .fall-btn, .btn-typ, .graf-btn, '
  + '[data-kuh], .kk-btn, .lt-weiter, [data-modus]';

const argv = process.argv.slice(2);
const alle = argv.includes('--alle');
const seiten = argv.filter(a => !a.startsWith('--'));

if (!seiten.length) {
  console.error('Aufruf: node .claude/tools/scan-live.mjs <seiten.html …> [--alle]');
  process.exit(2);
}

/**
 * Verdachtsfall? Multiplikation und Trennung lassen sich nicht sicher
 * auseinanderhalten. In Physik trägt «Zahl · Zahl ohne Gleichung» (Messwerte
 * wie «250 mA · 120 ms»); in Mathe nicht, weil Terme ohne `=` hier Alltag sind.
 * Die Mathe-Regel steht direkt in der Funktion.
 *
 * NICHT automatisch erkennbar und darum Sache von `--alle`:
 *   - Etikett-Wert-Paare ohne Gleichung davor («Amplitude 1 · Periode p = 2π»);
 *   - ein Trenner ohne Leerraum drumherum.
 * Das Skript ist damit ein Filter, kein Beweis: Die Sichtung mit `--alle`
 * ersetzt es nicht.
 */
function verdacht(zeile) {
  // Mathe: Terme ohne Gleichheitszeichen sind hier Alltag («4·x + 3·x + 5»), die
  // Physik-Regel «Zahl · Zahl ohne Gleichung» schlüge dort dauernd an. Der Trenner
  // sieht in Mathe anders aus: zwei Aussagen, verkettet mit einem freistehenden `·`
  // — «|−3| = 3 · |−3 − 2| = 5», «Anna = 4 · Dario = 5», «2·x + y = 4 · 2·x + y = 4».
  // Gemeldet wird darum ein `·` mit Leerraum auf beiden Seiten, vor dem eine
  // Gleichung mit einem Wert endet und nach dem eine neue Gleichung mit eigenem
  // linkem Term beginnt. Eine Kette wie «Fläche = 1 · 6 = 6» bleibt still: rechts
  // vor dem `=` steht nur eine Zahl.
  for (const m of zeile.matchAll(/·/g)) {
    const vor = zeile.slice(0, m.index), nach = zeile.slice(m.index + 1);
    if (!/\s$/.test(vor) || !/^\s/.test(nach)) continue;
    const iv = Math.max(vor.lastIndexOf('='), vor.lastIndexOf('≈'));
    const in_ = nach.search(/[=≈]/);
    if (iv < 0 || in_ < 0) continue;
    const links = vor.slice(iv + 1).trim(), rechts = nach.slice(0, in_).trim();
    if (!/^[−-]?\d[\d.\s]*[a-zA-Zµ°%²³]*$/.test(links)) continue;
    // Beginnt der rechte Teil mit Klammer oder Wurzel oder steckt ein Funktionsname
    // darin, ist er ein Faktor: «t = 5730 · log(0.5)(0.25) = …», «W = 50 · 8 · cos(30°) ≈ …».
    if (/^[(√]/.test(rechts) || /\b(log|ln|lg|sin|cos|tan|exp)\b/.test(rechts)) continue;
    if (/[a-zA-Zα-ωÄÖÜäöü|]/.test(rechts)) return 'zwei Aussagen mit · verkettet';
  }
  return null;
}
const browser = await chromium.launch();
let verdachtsfaelle = 0;

for (const seite of seiten) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const jsFehler = [];
  page.on('pageerror', e => jsFehler.push(String(e).slice(0, 120)));

  // Canvas-Beschriftungen mitschneiden — sie stehen in keinem DOM-Knoten.
  await page.addInitScript(() => {
    window.__cvText = [];
    const orig = CanvasRenderingContext2D.prototype.fillText;
    CanvasRenderingContext2D.prototype.fillText = function (t) {
      try { window.__cvText.push(String(t)); } catch (e) { /* Zeichnen nie brechen */ }
      return orig.apply(this, arguments);
    };
  });

  await page.goto(pathToFileURL(resolve(seite)).href, { waitUntil: 'load' });
  await page.waitForTimeout(400);

  // Bedienzustaende durchfahren und nach JEDEM Zustand einsammeln. Einmal am
  // Ende genuegt nicht: Teile der Seite sind nur in einem Modus sichtbar (im
  // Einheitentrainer erscheint «Lernen starten» erst im Lernmodus), und der
  // DOM-Text des vorigen Zustands ist dann schon ueberschrieben. Die
  // Canvas-Texte sammelt der fillText-Haken ohnehin durchgehend.
  const gesammelt = new Map();

  const sammle = async () => {
    const neu = await page.evaluate(([bereich, ausschluss]) => {
      // Ausgeschlossene Zonen kurz verbergen, den Bereich als Text lesen und
      // sofort wiederherstellen. innerText beachtet display:none, und die
      // Zeilen bleiben so zusammen, wie sie auf dem Schirm stehen.
      const verborgen = [];
      for (const el of document.querySelectorAll(ausschluss)) {
        verborgen.push([el, el.style.getPropertyValue('display'), el.style.getPropertyPriority('display')]);
        el.style.setProperty('display', 'none', 'important');
      }
      const text = (document.querySelector(bereich) || document.body).innerText || '';
      for (const [el, wert, prio] of verborgen) {
        if (wert) el.style.setProperty('display', wert, prio); else el.style.removeProperty('display');
      }
      const raus = [];
      for (const z of text.split('\n')) {
        const t = z.replace(/\s+/g, ' ').trim();
        if (t.includes('·')) raus.push(t);
      }
      return raus;
    }, [BEREICH, AUSSCHLUSS]);
    for (const t of neu) if (!gesammelt.has(t)) gesammelt.set(t, 'DOM');
  };

  // Was ein Mensch nach einem Moduswechsel tut: die Uebung starten, etwas
  // Ungueltiges und etwas Gueltiges eintippen, pruefen lassen. Erst dann
  // stehen Rueckmeldungstexte wie «Erlaubt sind …» ueberhaupt auf der Seite.
  const nachfassen = wert => page.evaluate(async (wert) => {
    const warte = ms => new Promise(r => setTimeout(r, ms));
    const sicht = sel => [...document.querySelectorAll(sel)].filter(e => e.offsetParent);
    const knopf = re => sicht('button').filter(b => re.test(b.textContent || ''));
    // Frueher Ausstieg: die meisten Themenseiten haben weder Eingabefeld noch
    // Startknopf. Ohne diese Pruefung wartet das Skript dort nach jedem der bis
    // zu 24 Umschalter rund anderthalb Sekunden ins Leere.
    if (!sicht('input[type=text], input[type=number]').length
        && !knopf(/starten|beginnen/i).length) return;
    for (const b of knopf(/starten|beginnen/i).slice(0, 3)) {
      try { b.click(); } catch (e) { /* egal */ }
      await warte(300);
    }
    for (const feld of sicht('input[type=text], input[type=number]').slice(0, 3)) {
      feld.value = wert;
      feld.dispatchEvent(new Event('input', { bubbles: true }));
      feld.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
      feld.dispatchEvent(new Event('change', { bubbles: true }));
      await warte(120);
      for (const b of knopf(/prüfen|antwort/i).slice(0, 2)) {
        try { b.click(); } catch (e) { /* egal */ }
        await warte(200);
      }
    }
  }, wert);

  await sammle();
  for (const v of ['xyz', '1']) { await nachfassen(v); await sammle(); }

  const knoepfe = await page.$$(KNOEPFE);
  for (const k of knoepfe.slice(0, 24)) {
    try { await k.click({ timeout: 1500 }); } catch (e) { continue; }
    await page.waitForTimeout(120);
    await sammle();
    for (const v of ['xyz', '1']) { await nachfassen(v); await sammle(); }
  }

  await page.evaluate(async () => {
    const warte = ms => new Promise(r => setTimeout(r, ms));
    for (const r of document.querySelectorAll('input[type=range]')) {
      for (const v of [r.min, r.max, r.defaultValue]) {
        r.value = v;
        r.dispatchEvent(new Event('input', { bubbles: true }));
        await warte(60);
      }
    }
  });
  await page.waitForTimeout(200);
  await sammle();

  const cvTexte = await page.evaluate(() => window.__cvText || []);
  for (const t of cvTexte) {
    const z = t.replace(/\s+/g, ' ').trim();
    if (z.includes('·') && !gesammelt.has(z)) gesammelt.set(z, 'Canvas');
  }

  const funde = [...gesammelt].map(([t, h]) => ({ t, h }));

  const gemeldet = funde
    .map(f => ({ ...f, grund: verdacht(f.t) }))
    .filter(f => alle || f.grund);

  if (gemeldet.length || jsFehler.length) {
    console.log(`\n${seite}`);
    for (const f of gemeldet) {
      const marke = f.grund ? '!!' : '  ';
      console.log(`  ${marke} [${f.h.padEnd(6)}] ${f.t}`);
      if (f.grund) console.log(`         ^ ${f.grund}`);
    }
    for (const e of jsFehler) console.log(`  !! JS-Fehler: ${e}`);
  }
  verdachtsfaelle += gemeldet.filter(f => f.grund).length;
  await page.close();
}

await browser.close();
console.log(`\n${seiten.length} Seite(n) geprüft — ${verdachtsfaelle} Verdachtsfall/-fälle.`);
if (!alle && !verdachtsfaelle) {
  console.log('Für die vollständige Sichtung aller `·` in Wertanzeigen: --alle');
}
process.exit(verdachtsfaelle ? 1 : 0);
