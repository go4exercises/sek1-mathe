// Prüft die Umformer (figure.umformer) eines Leitprogramms — Kapitel 1–4 von
// leitprogramme/lineare-quadratische-gleichungen.html (scripts/lp/lineare-quadratische-gleichungen/README.md).
//
//   node .claude/tools/pruef-umformer.mjs leitprogramme/<name>.html
//
// 1. Statisch: alle Ziele vorhanden und erreichbar, keine Sackgasse, jeder Knoten mit einem gültigen Schritt.
// Knöpfe mit '!' sind Fehler (rote Rückmeldung), mit '?' gültige Umwege (grauer Hinweis).
// 2. Je Aufgabe zwei Durchgänge (erste bzw. letzte gültige Wahl an jedem Knoten): Jeder Fehlerknopf,
//    jede falsche Lücke (999) und jede falsche Lösungsmenge ({999}) gibt eine Rückmeldung, der Weg
//    endet mit ✓ in der Aufgabenleiste. Braucht die Testhaken fig.__aufgaben und fig.__U.
// Exit 1 bei einem Befund.
import { chromium } from 'playwright';
import path from 'node:path';
const WURZEL = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const b = await chromium.launch(); const p = await b.newPage();
const fehler = []; p.on('pageerror', e => fehler.push(e.message));
const seite = process.argv[2]; if (!seite) { console.error('Aufruf: node .claude/tools/pruef-umformer.mjs leitprogramme/<name>.html'); process.exit(2); }
await p.goto('file://' + path.resolve(WURZEL, seite));
await p.waitForTimeout(1500);
const statisch = await p.evaluate(() => {
  const aus = [];
  document.querySelectorAll('figure.umformer').forEach(fig => {
    fig.__aufgaben.forEach((A, t) => {
      const k = A.k, start = A.start || 'a', gesehen = new Set([start]), q = [start];
      while (q.length){ const id = q.shift(), K = k[id];
        if (!K){ aus.push(`${fig.id} A${t + 1}: Knoten ${id} fehlt`); continue; }
        const ziele = [];
        if (K.w) K.w.forEach(o => { if (typeof o[1] === 'string' && (o[1][0] === '!' || o[1][0] === '?')) { if (o[1].length < 15) aus.push(`${fig.id} A${t+1} ${id}: kurze Rückmeldung`); } else ziele.push(o[1]); });
        if (K.feld) ziele.push(K.feld.nach);
        if (!K.w && !K.feld && K.L == null) aus.push(`${fig.id} A${t + 1}: ${id} Sackgasse`);
        if (K.w && !ziele.length) aus.push(`${fig.id} A${t + 1}: ${id} ohne gültigen Schritt`);
        ziele.forEach(z => { if (!k[z]) aus.push(`${fig.id} A${t + 1}: Ziel ${z} fehlt`); else if (!gesehen.has(z)){ gesehen.add(z); q.push(z); } });
      }
      Object.keys(k).forEach(id => { if (!gesehen.has(id)) aus.push(`${fig.id} A${t + 1}: ${id} unerreichbar`); });
    });
  });
  return aus;
});
let befunde = statisch.length;
console.log('statisch:', statisch.length ? statisch : 'ok');
// dynamisch: jede Aufgabe auf zwei Wegen (erste bzw. letzte gültige Wahl)
const ids = await p.evaluate(() => [...document.querySelectorAll('figure.umformer')].map(f => f.id));
for (const id of ids){
  const n = await p.evaluate(id => document.getElementById(id).__aufgaben.length, id);
  for (const weg of ['erst', 'letzt']){
    for (let t = 0; t < n; t++){
      const r = await p.evaluate(async ({ id, t, weg }) => {
        const fig = document.getElementById(id), U = fig.__U, A = fig.__aufgaben[t], log = [];
        // Leiste auf Aufgabe t bringen: «von vorn» bzw. überspringen
        const L = fig.querySelector('.leiste'), bt = L.querySelector('.ls-weiter');
        let guard = 0; while (U.zustand().aufgabe !== A && guard++ < 30) bt.click();
        if (U.zustand().aufgabe !== A) return ['nicht erreicht'];
        const warte = () => new Promise(r => setTimeout(r, 5));
        for (let s = 0; s < 40 && !U.zustand().fertig; s++){
          const kid = U.knoten(), K = A.k[kid], rueck = fig.querySelector('.uf-rueck');
          if (K.w){
            const knoepfe = [...fig.querySelectorAll('.uf-knopf')];
            K.w.forEach((o, j) => { if (typeof o[1] === 'string' && (o[1][0] === '!' || o[1][0] === '?')){ knoepfe[j].click();
              const soll = o[1][0] === '!' ? 'falsch' : 'hinweis';   // '?': gültiger Umweg, grauer Hinweis
              if (!rueck.classList.contains(soll) || U.knoten() !== kid) log.push(kid + ': Knopf ' + j + ' ohne ' + soll + '-Rückmeldung'); } });
            const gut = K.w.map((o, j) => [o, j]).filter(x => !(typeof x[0][1] === 'string' && (x[0][1][0] === '!' || x[0][1][0] === '?')));
            const w = weg === 'erst' ? gut[0] : gut[gut.length - 1];
            fig.querySelectorAll('.uf-knopf')[w[1]].click();
          } else if (K.feld){
            const inp = [...fig.querySelectorAll('.uf-wahl input')];
            inp.forEach(i => i.value = '999'); fig.querySelector('.uf-pruefen').click();
            if (!rueck.classList.contains('falsch') || U.knoten() !== kid) log.push(kid + ': falsche Lücke ohne Rückmeldung');
            const soll = K.feld.soll || K.feld.beispiel;
            inp.forEach(i => i.value = String(soll[i.dataset.f])); fig.querySelector('.uf-pruefen').click();
            if (U.knoten() === kid) log.push(kid + ': richtige Lücke nicht angenommen ' + rueck.textContent);
          } else if (K.L != null){
            const i = fig.querySelector('.uf-menge');
            i.value = '{999}'; fig.querySelector('.uf-pruefen').click();
            if (!rueck.classList.contains('falsch')) log.push(kid + ': falsche Menge ohne Rückmeldung');
            const m = K.L === 'R' ? 'R' : '{' + K.L.slice().reverse().map(v => Math.abs(v - Math.round(v)) < 1e-9 ? v : (Math.abs(v*3 - Math.round(v*3)) < 1e-9 ? Math.round(v*3) + '/3' : v)).join('; ') + '}';
            i.value = m; fig.querySelector('.uf-pruefen').click();
            if (!U.zustand().fertig) log.push(kid + ': richtige Menge ' + m + ' nicht angenommen: ' + rueck.textContent);
          }
          await warte();
        }
        if (!U.zustand().fertig) log.push('nicht fertig');
        if (L.querySelector('.ls-ok').textContent !== '✓') log.push('Leiste ohne ✓');
        return log;
      }, { id, t, weg });
      befunde += r.length;
      console.log(id, 'A' + (t + 1), weg, r.length ? r : 'ok');
    }
  }
}
console.log('JS-Fehler:', fehler.length ? fehler : 'keine');
await b.close();
befunde += fehler.length;
console.log(befunde ? `\n${befunde} Befund(e).` : '\nALLE UMFORMER BESTANDEN');
process.exit(befunde ? 1 : 0);
