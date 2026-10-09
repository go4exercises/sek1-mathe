// Clip-Prüfung: springt in den Renderzustand einzelner Sekunden, misst die
// sichtbaren Zeilen und meldet Überlappungen sowie alles, was über die Bühne
// hinausragt. Bruchstriche machen eine Zeile doppelt hoch — das sieht man in
// der Zahlenliste des Drehbuchs nicht, hier schon.
//
//   node .claude/tools/pruef-clip.mjs clips/<name>.html 10.5 22.5 34 …
//
// Bilder landen in $SP (Standard: neben dem Clip).
import { chromium } from 'playwright';
import fs from 'fs';
const datei = process.argv[2];
const marken = process.argv.slice(3).map(Number);   // Sekunden zum Prüfen
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
const fehler = [];
await p.goto('file://' + fs.realpathSync(datei) + '?render');
// Setzt der Clip mit MathJax (Drehbuch "latex": true), stehen die Formeln
// erst nach dem Satz an ihrem Platz — vorher misst man den Rohtext.
await p.evaluate(() => window.MathJax?.startup?.promise ?? null);
await p.waitForTimeout(200);
for (const t of marken) {
  await p.evaluate(s => window.__seek(s), t);
  await p.waitForTimeout(60);
  const r = await p.evaluate(() => {
    // .step sind die Einträge der Merkschiene links. Sie stehen in einer
    // eigenen Spalte und dürfen sich berühren — sonst meldet jede Schiene
    // sich selbst als Überlappung.
    const sichtbar = [...document.querySelectorAll('.l:not(.step)')]
      .filter(el => parseFloat(getComputedStyle(el).opacity) > 0.5)
      .filter(el => !el.closest('.step'))
      // Der Kasten *um* die Schiene traegt keine eigene Klasse, nur .l. Er
      // ist 470px breit und ragt damit in jede zentrierte Zeile hinein,
      // ohne dass sich im Bild etwas beruehrt.
      .filter(el => !el.querySelector('.step'))
      // Gemessen wird nicht der Container, sondern was tatsaechlich im Bild
      // steht. Eine zentrierte Zeile spannt sich ueber die ganze Buehne
      // (left:0;right:0), ihr Inhalt traegt aber `white-space:nowrap`: Er
      // laeuft im Zweifel ueber den Rand hinaus, ohne dass der Container
      // breiter wird. Die Pruefung sah davon bis zum 07.09.2026 nichts.
      // Uebernommen aus TALS Physik, wo derselbe blinde Fleck zehn
      // abgeschnittene Zeilen in fuenf Clips verdeckt hatte.
      .map(el => {
        const k = el.children.length ? [...el.children] : [el];
        const rr = [el.getBoundingClientRect(), ...k.map(x => x.getBoundingClientRect())];
        return { t: el.textContent.trim().slice(0, 42), r: {
          left:   Math.min(...rr.map(x => x.left)),
          right:  Math.max(...rr.map(x => x.right)),
          top:    Math.min(...rr.map(x => x.top)),
          bottom: Math.max(...rr.map(x => x.bottom)),
          get width()  { return this.right - this.left; },
        } };
      });
    const t = [];
    for (let i = 0; i < sichtbar.length; i++)
      for (let j = i + 1; j < sichtbar.length; j++) {
        const a = sichtbar[i].r, c = sichtbar[j].r;
        const ux = Math.min(a.right, c.right) - Math.max(a.left, c.left);
        const uy = Math.min(a.bottom, c.bottom) - Math.max(a.top, c.top);
        // Deckungsgleiche Kaesten sind kein Zusammenstoss, sondern ein
        // Stapel: So wird eine Tastenfolge gebaut — jede neue Anzeige legt
        // sich ueber die vorige, die alte bleibt darunter stehen.
        const stapel = Math.abs(a.left - c.left) < 3 && Math.abs(a.top - c.top) < 3
                    && Math.abs(a.width - c.width) < 3;
        if (ux > 2 && uy > 2 && !stapel) t.push([sichtbar[i].t, sichtbar[j].t, Math.round(uy)]);
      }
    const raus = sichtbar.filter(s => s.r.bottom > 1080 || s.r.top < 0
                                   || s.r.left < 0 || s.r.right > 1920)
                         .map(s => [s.t, Math.round(s.r.top), Math.round(s.r.bottom),
                                    Math.round(s.r.left), Math.round(s.r.right)]);
    const unten = Math.max(0, ...sichtbar.map(s => s.r.bottom));
    return { t, raus, unten: Math.round(unten), n: sichtbar.length };
  });
  console.log(`t=${t}s  ${r.n} sichtbar, unterste Kante ${r.unten}px`);
  r.t.forEach(x => { fehler.push(t); console.log('   ÜBERLAPP:', x[0], '×', x[1], `(${x[2]}px)`); });
  r.raus.forEach(x => { fehler.push(t); console.log('   AUSSERHALB:', x[0], 'y', x[1], '-', x[2], 'x', x[3], '-', x[4]); });
  await p.screenshot({ path: `${process.env.SP || '.'}/szene-${String(t).replace('.', '_')}.png` });
}
await b.close();
console.log(fehler.length ? `\n${fehler.length} Beanstandungen` : '\nkeine Überlappungen, nichts ausserhalb der Bühne');
