<script>
/* Leitprogramm Bruchterme, Gleichungen und Formeln — Faktoren kürzen (Sim 1), Hauptnenner bauen (Sim 2),
   Gleichung umformen (Sim 3), Formel rückwärts rechnen (Sim 4), Übungen mit Rückmeldung.
   Eingaben werden geparst: Bruchterme in x (als Bruch zweier Polynome mit ganzen Koeffizienten: gleichwertig,
   vollständig gekürzt, auf einem Bruchstrich), Formeln in mehreren Grössen (gleichwertig an Zufallsstellen,
   nach der gesuchten Grösse aufgelöst), Zahlen exakt als Bruch (7/3, 2.5, −4), Lösungsmengen ({ } und Q).
   Farben: Zähler blau, Nenner orange, Gekürztes und Ergebnis grün, Fehler rot. */
(function(){
  'use strict';
  function setzen(e){ if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([e]).catch(function(){}); }
  function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
  function zufallG(a, b){ return a + Math.floor(Math.random() * (b - a + 1)); }
  function nz(a, b){ var r; do { r = zufallG(a, b); } while (!r); return r; }
  function ggT(a, b){ a = Math.abs(a); b = Math.abs(b); while (b){ var t = a % b; a = b; b = t; } return a; }
  function kgV(a, b){ return Math.abs(a * b) / ggT(a, b); }
  function mz(n){ return (n < 0 ? '−' : '') + Math.abs(n); }

  /* ---------- Brüche exakt: [z, n], n > 0, gekürzt ---------- */
  function B(z, n){ n = n == null ? 1 : n; if (n < 0){ z = -z; n = -n; } var g = ggT(z, n) || 1; return [z / g, n / g]; }
  function bAdd(a, b){ return B(a[0] * b[1] + b[0] * a[1], a[1] * b[1]); }
  function bSub(a, b){ return B(a[0] * b[1] - b[0] * a[1], a[1] * b[1]); }
  function bMul(a, b){ return B(a[0] * b[0], a[1] * b[1]); }
  function bDiv(a, b){ return B(a[0] * b[1], a[1] * b[0]); }
  function bEq(a, b){ return a[0] * b[1] === b[0] * a[1]; }
  function bDez(x){ var s = String(x), k = s.indexOf('.') < 0 ? 0 : s.length - s.indexOf('.') - 1, f = Math.pow(10, k); return B(Math.round(x * f), f); }
  function bTex(a){ return a[1] === 1 ? String(a[0]) : (a[0] < 0 ? '-' : '') + '\\tfrac{' + Math.abs(a[0]) + '}{' + a[1] + '}'; }
  function bTxt(a){ return a[1] === 1 ? mz(a[0]) : mz(a[0]) + '/' + a[1]; }
  function bZahl(a){ return a[0] / a[1]; }
  /* Zahl als Dezimalzahl, wenn sie abbricht (Grössen), sonst als Bruch */
  function bWert(a){ var n = a[1]; while (n % 2 === 0) n /= 2; while (n % 5 === 0) n /= 5; return n === 1 ? String(+(a[0] / a[1]).toFixed(6)).replace('-', '−') : bTxt(a); }
  function bWertTex(a){ var n = a[1]; while (n % 2 === 0) n /= 2; while (n % 5 === 0) n /= 5; return n === 1 ? String(+(a[0] / a[1]).toFixed(6)) : bTex(a); }

  /* Zahleingabe: −4, 2.5, 7/3, −7/3, (−7)/3. Dezimalkomma abgelehnt. */
  function zahlLesen(s){
    s = String(s).trim().replace(/[−–]/g, '-').replace(/\s+/g, '').replace(/^\((-?\d+)\)/, '$1');
    if (/\d,\d/.test(s)) return { kaputt: 'Dezimalpunkt statt Komma: 2.5' };
    var m = s.match(/^([+-]?\d+(?:\.\d+)?)(?:\/(\d+))?$/);
    if (!m) return { kaputt: 'Gib eine Zahl ein, zum Beispiel 4, −2.5 oder 7/3.' };
    var a = bDez(parseFloat(m[1]));
    if (m[2]){ if (+m[2] === 0) return { kaputt: 'Durch 0 teilen geht nicht.' }; a = bDiv(a, B(+m[2])); }
    return { w: a };
  }

  /* ---------- Polynome (ganze Koeffizienten) ---------- */
  function P(c){ c = (c || []).slice(); while (c.length > 1 && !c[c.length - 1]) c.pop(); return c.length ? c : [0]; }
  function pAdd(p, q){ var r = []; for (var i = 0; i < Math.max(p.length, q.length); i++) r[i] = (p[i] || 0) + (q[i] || 0); return P(r); }
  function pNeg(p){ return P(p.map(function(c){ return -c; })); }
  function pMul(p, q){ var r = []; for (var i = 0; i < p.length; i++) for (var j = 0; j < q.length; j++) r[i + j] = (r[i + j] || 0) + p[i] * q[j]; return P(r); }
  function pEq(p, q){ p = P(p); q = P(q); return p.length === q.length && p.every(function(c, i){ return c === q[i]; }); }
  function pNull(p){ return P(p).length === 1 && !P(p)[0]; }
  function lin(a, b){ return P([b, a]); }
  function mon(k, e){ var c = []; for (var i = 0; i < e; i++) c.push(0); c.push(k); return P(c); }
  function pInhalt(p){ return p.reduce(function(g, c){ return ggT(g, c); }, 0); }
  function pTex(p, v){
    v = v || 'x'; p = P(p); var s = '';
    for (var i = p.length - 1; i >= 0; i--){
      var c = p[i]; if (!c) continue;
      var a = Math.abs(c), teil = i === 0 ? String(a) : (a === 1 ? '' : a) + v + (i > 1 ? '^' + i : '');
      s += s ? (c < 0 ? ' - ' : ' + ') + teil : (c < 0 ? '-' : '') + teil;
    }
    return s || '0';
  }
  function pTxt(p, v){ return pTex(p, v).replace(/ /g, ''); }
  /* p(r) für r = [z, n] als ganze Zahl n^grad · p(z/n) — 0 genau dann, wenn r Nullstelle ist */
  function pNullAn(p, r){ p = P(p); var d = p.length - 1, s = 0; for (var i = 0; i <= d; i++) s += p[i] * Math.pow(r[0], i) * Math.pow(r[1], d - i); return s === 0; }
  function pWert(p, x){ var s = [0, 1]; for (var i = P(p).length - 1; i >= 0; i--) s = bAdd(bMul(s, x), B(P(p)[i])); return s; }

  /* ---------- Bruchterme {z, n} ---------- */
  function R(z, n){ return { z: P(z), n: P(n == null ? [1] : n) }; }
  function rAdd(a, b){ return R(pAdd(pMul(a.z, b.n), pMul(b.z, a.n)), pMul(a.n, b.n)); }
  function rNeg(a){ return R(pNeg(a.z), a.n); }
  function rMul(a, b){ return R(pMul(a.z, b.z), pMul(a.n, b.n)); }
  function rDiv(a, b){ return R(pMul(a.z, b.n), pMul(a.n, b.z)); }
  function rEq(a, b){ return pEq(pMul(a.z, b.n), pMul(b.z, a.n)); }
  function rTex(a, v){
    if (pEq(a.n, [1])) return pTex(a.z, v);
    if (P(a.z).every(function(c){ return c <= 0; })) return '-\\dfrac{' + pTex(pNeg(a.z), v) + '}{' + pTex(a.n, v) + '}';
    return '\\dfrac{' + pTex(a.z, v) + '}{' + pTex(a.n, v) + '}';
  }
  /* Gemeinsamer Faktor von Zähler und Nenner? Zahl (ggT der Koeffizienten) oder Nullstelle p/q (|p| ≤ 30, q ≤ 6). */
  function gemeinsam(a){
    if (pNull(a.z)) return null;
    var g = ggT(pInhalt(a.z), pInhalt(a.n));
    if (g > 1) return { art: 'zahl', g: g };
    if (P(a.z).length < 2 || P(a.n).length < 2) return null;
    for (var q = 1; q <= 6; q++) for (var p = -30; p <= 30; p++){
      if (ggT(p, q) !== 1) continue;
      if (pNullAn(a.z, [p, q]) && pNullAn(a.n, [p, q])) return { art: 'faktor', f: lin(q, -p) };
    }
    return null;
  }
  /* Kürzen bis zum Ende (für Musterlösungen): gemeinsame Faktoren heraus, Nenner mit positivem Leitkoeffizienten. */
  function pDivLin(p, f){                     // p : (a x + b), exakt; nur bei Nullstelle aufgerufen
    p = P(p); var a = f[1], b = f[0], d = p.length - 1, q = [], r = p.slice();
    for (var i = d; i >= 1; i--){ var c = r[i] / a; q[i - 1] = c; r[i] -= c * a; r[i - 1] -= c * b; }
    return P(q);
  }
  function rKurz(a){
    var g, s = 0;
    a = R(a.z, a.n);
    while ((g = gemeinsam(a)) && s++ < 20){
      if (g.art === 'zahl') a = R(a.z.map(function(c){ return c / g.g; }), a.n.map(function(c){ return c / g.g; }));
      else a = R(pDivLin(a.z, g.f), pDivLin(a.n, g.f));
    }
    if (P(a.n)[P(a.n).length - 1] < 0) a = R(pNeg(a.z), pNeg(a.n));
    return a;
  }

  /* ---------- Termeingabe ----------
     Baum: n (Zahl, auch Dezimal) · v (Grösse) · + (Glieder) · * und / (binär) · neg · ^ · (). Erlaubt: Ziffern, die Grössen
     aus `namen`, + − · * × / ^ ² ³, Klammern, unsichtbares Mal (3x, 2(x+1)). Nach «/» braucht ein zusammengesetzter
     Nenner Klammern: 3/(2x) — «3/2x» wird abgelehnt, weil es sich auf zwei Arten lesen lässt. */
  function termLesen(s, namen, ziel){
    s = String(s == null ? '' : s).trim();
    if (!s) return { leer: true };
    s = s.replace(/[−–]/g, '-').replace(/[·×⋅]/g, '*').replace(/:/g, '/').replace(/²/g, '^2').replace(/³/g, '^3').replace(/\s+/g, '');
    if (namen.length === 1) s = s.split(namen.toUpperCase()).join(namen);
    if (ziel && s.indexOf(ziel + '=') === 0) s = s.slice(ziel.length + 1);
    if (s.indexOf('=') >= 0) return { kaputt: true, grund: 'Schreib nur den Term' + (ziel ? ' rechts von «' + ziel + ' =»' : '') + ', ohne Gleichheitszeichen.' };
    if (/\d,\d/.test(s)) return { kaputt: true, grund: 'Dezimalpunkt statt Komma: 2.5' };
    var fremd = s.replace(/[0-9.+\-*/^()]/g, '');
    for (var j = 0; j < namen.length; j++) fremd = fremd.split(namen[j]).join('');
    if (fremd) return { kaputt: true, grund: /[a-z]/i.test(fremd) ? 'Hier kommen nur ' + namen.split('').map(function(c){ return '\\(' + c + '\\)'; }).join(', ') + ' vor.' : 'Zeichen «' + fremd[0] + '» verstehe ich nicht.' };
    var i = 0;
    function peek(){ return s[i]; }
    function istName(c){ return c != null && namen.indexOf(c) >= 0; }
    function startFaktor(c){ return c === '(' || /[0-9]/.test(c || '') || istName(c); }
    function summe(){
      var glieder = [], vz = 1;
      if (peek() === '+' || peek() === '-'){ vz = peek() === '-' ? -1 : 1; i++; }
      var g = produkt(); glieder.push(vz < 0 ? { t: 'neg', x: g } : g);
      while (peek() === '+' || peek() === '-'){ var m = peek() === '-'; i++; g = produkt(); glieder.push(m ? { t: 'neg', x: g } : g); }
      return glieder.length === 1 ? glieder[0] : { t: '+', a: glieder };
    }
    function produkt(){
      var f = potenz();
      while (i < s.length && (peek() === '*' || peek() === '/' || startFaktor(peek()))){
        if (peek() === '/'){ i++; var nn = potenz(); if (startFaktor(peek())) throw 'nenner'; f = { t: '/', a: [f, nn] }; continue; }
        if (peek() === '*') i++;
        f = { t: '*', a: [f, potenz()] };
      }
      return f;
    }
    function potenz(){
      var b = basis();
      if (peek() === '^'){ i++; var m = s.slice(i).match(/^\d+/); if (!m) throw 'hoch'; i += m[0].length; return { t: '^', x: b, e: +m[0] }; }
      return b;
    }
    function basis(){
      var c = peek();
      if (c === '('){ i++; var x = summe(); if (peek() !== ')') throw 'klammer'; i++; return { t: '()', x: x }; }
      if (c === '-'){ i++; return { t: 'neg', x: potenz() }; }
      if (istName(c)){ i++; if (/[0-9]/.test(peek() || '')) throw 'hochzahl'; return { t: 'v', n: c }; }
      var m = s.slice(i).match(/^\d+(\.\d+)?/); if (m){ i += m[0].length; return { t: 'n', w: +m[0] }; }
      throw 'zeichen';
    }
    try {
      var baum = summe();
      if (i !== s.length) throw 'rest';
      var aus = { baum: baum };
      if (namen.length === 1) aus.r = rat(baum);
      return aus;
    } catch (e){
      return { kaputt: true, grund: e === 'klammer' ? 'Eine Klammer ist nicht geschlossen.'
        : e === 'nenner' ? 'Setz einen zusammengesetzten Nenner in Klammern, zum Beispiel <code>3/(2x)</code>.'
        : e === 'hochzahl' ? 'Hochzahlen mit <code>^</code> schreiben: <code>x^2</code> (oder x²).'
        : e === 'null' ? 'Durch 0 teilen geht nicht.'
        : 'Schreib den Term zum Beispiel so: <code>(x-3)/(x+3)</code> oder <code>3/(2x)</code>.' };
    }
  }
  function rat(k){
    if (k.t === 'n') { var b = bDez(k.w); return R([b[0]], [b[1]]); }
    if (k.t === 'v') return R([0, 1]);
    if (k.t === '()') return rat(k.x);
    if (k.t === 'neg') return rNeg(rat(k.x));
    if (k.t === '^'){ var r = R([1]); for (var j = 0; j < k.e; j++) r = rMul(r, rat(k.x)); return r; }
    if (k.t === '+') return k.a.reduce(function(r, g){ return rAdd(r, rat(g)); }, R([0]));
    if (k.t === '*') return rMul(rat(k.a[0]), rat(k.a[1]));
    var nn = rat(k.a[1]); if (pNull(nn.z)) throw 'null';
    return rDiv(rat(k.a[0]), nn);
  }
  function zahlwert(k, w){
    if (k.t === 'n') return k.w;
    if (k.t === 'v') return w[k.n];
    if (k.t === '()') return zahlwert(k.x, w);
    if (k.t === 'neg') return -zahlwert(k.x, w);
    if (k.t === '^') return Math.pow(zahlwert(k.x, w), k.e);
    if (k.t === '+') return k.a.reduce(function(s, g){ return s + zahlwert(g, w); }, 0);
    if (k.t === '*') return zahlwert(k.a[0], w) * zahlwert(k.a[1], w);
    return zahlwert(k.a[0], w) / zahlwert(k.a[1], w);
  }
  function enthaelt(k, n){
    if (k.t === 'v') return k.n === n;
    if (k.t === 'n') return false;
    if (k.x) return enthaelt(k.x, n);
    return k.a.some(function(g){ return enthaelt(g, n); });
  }
  function ohneKl(k){ while (k.t === '()') k = k.x; return k; }
  function hatBruch(k){ if (k.t === '/') return true; if (k.x) return hatBruch(k.x); if (k.a) return k.a.some(hatBruch); return false; }
  /* «auf einem Bruchstrich»: höchstens ein Bruchstrich, ganz aussen (Vorzeichen davor erlaubt). */
  function einBruch(k){
    k = ohneKl(k); if (k.t === 'neg') k = ohneKl(k.x);
    if (k.t === '/') return !hatBruch(k.a[0]) && !hatBruch(k.a[1]);
    return !hatBruch(k);
  }
  /* Formeln vergleichen: an 8 Zufallsstellen (positive Werte) gleich, relativ 1e-9 */
  function formelGleich(k, f, namen){
    for (var j = 0; j < 8; j++){
      var w = {}; for (var q = 0; q < namen.length; q++) w[namen[q]] = 1 + Math.round(Math.random() * 80) / 9;
      var a = zahlwert(k, w), b = f(w);
      if (!isFinite(a) || !isFinite(b)) continue;
      if (Math.abs(a - b) > 1e-9 * Math.max(1, Math.abs(b))) return false;
    }
    return true;
  }
  /* Lösungsmenge: «{}», «{ }», «leer», «keine» → leer; «Q», «ℚ», «alle» → alle; «5», «{5}», «x=5», «7/3» → Zahl */
  function mengeLesen(s){
    s = String(s).trim().replace(/[−–]/g, '-').replace(/\s+/g, '').replace(/^L=/i, '').replace(/^x=/i, '');
    if (/^(\{\}|leer|keine|keineLösung|∅)$/i.test(s)) return { art: 'leer' };
    if (/^(Q|ℚ|\\mathbb\{Q\}|alle|alleZahlen)$/i.test(s)) return { art: 'alle' };
    s = s.replace(/^\{(.*)\}$/, '$1');
    var z = zahlLesen(s);
    return z.kaputt ? { kaputt: z.kaputt + ' Keine Lösung: <code>{}</code>, alle Zahlen: <code>Q</code>.' } : { art: 'zahl', w: z.w };
  }

  /* ---------- Aufgabenleiste (wie in den anderen Leitprogrammen) ---------- */
  function Leiste(fig, aufgaben, sim){
    var box = fig.querySelector('.leiste'); if (!box) return function(){};
    var n = aufgaben.length, i = 0, erledigt = {};
    box.innerHTML = '<span class="ls-nr"></span><span class="ls-text"></span><span class="ls-ok" aria-live="polite"></span><button type="button" class="ls-weiter"></button><button type="button" class="ls-neu" hidden>von vorn</button>';
    var nr = box.querySelector('.ls-nr'), tx = box.querySelector('.ls-text'), ok = box.querySelector('.ls-ok'),
        bt = box.querySelector('.ls-weiter'), bv = box.querySelector('.ls-neu');
    function anzahl(){ var k = 0; for (var j = 0; j < n; j++) if (erledigt[j]) k++; return k; }
    function offen(ab){ for (var j = ab; j < n; j++) if (!erledigt[j]) return j; return n; }
    function zeigen(){
      if (i >= n){
        var k = anzahl();
        ok.textContent = ''; box.classList.remove('geloest');
        if (k === n){ nr.textContent = '✓'; tx.innerHTML = 'Alle ' + n + ' Aufgaben gelöst — weiter mit dem Kontrollclip.'; bt.textContent = 'nochmals'; bv.hidden = true; box.classList.add('fertig'); }
        else { nr.textContent = k + '/' + n; tx.innerHTML = k + ' von ' + n + ' gelöst, ' + (n - k) + ' übersprungen.'; bt.textContent = 'zu den offenen ▶'; bv.hidden = false; box.classList.remove('fertig'); }
        return;
      }
      box.classList.remove('fertig'); bv.hidden = true;
      nr.textContent = (i + 1) + '/' + n; tx.innerHTML = aufgaben[i].text; setzen(tx);
      if (aufgaben[i].setup) aufgaben[i].setup(sim);
      if (sim.zeichnen) sim.zeichnen();
      pruefen();
    }
    function pruefen(){
      if (i >= n) return;
      var gut = !!aufgaben[i].ok(sim.zustand());
      if (gut) erledigt[i] = true;
      ok.textContent = erledigt[i] ? '✓' : '';
      bt.textContent = erledigt[i] ? 'Nächste ▶' : 'überspringen';
      box.classList.toggle('geloest', !!erledigt[i]);
    }
    function gehe(j){
      i = j;
      fig.querySelectorAll('input[type=range]').forEach(function(inp){ inp.value = inp.defaultValue; });
      fig.querySelectorAll('.sim-schalter input').forEach(function(inp){ inp.checked = inp.defaultChecked; });
      fig.querySelectorAll('select.sim-wahl').forEach(function(s){ s.value = s.querySelector('option[selected]').value; });
      zeigen(); if (sim.zeichnen) sim.zeichnen();
    }
    bt.addEventListener('click', function(){
      if (i >= n){ if (anzahl() === n){ erledigt = {}; gehe(0); } else gehe(offen(0)); }
      else gehe(offen(i + 1));
    });
    bv.addEventListener('click', function(){ erledigt = {}; gehe(0); });
    setTimeout(zeigen, 0);
    return pruefen;
  }
  function wertR(fig, id){ return +fig.querySelector('#' + id).value; }
  function zeigeWert(fig, id){ var i = fig.querySelector('#' + id); var v = i.parentNode.querySelector('.sl-val'); if (v) v.textContent = mz(+i.value); }
  function hx(p){ return pTex(p).replace(/\^2/g, '²').replace(/-/g, '−'); }      // Live-Anzeige ohne MathJax

  /* ════════ Sim 1 — Faktoren kürzen ════════
     Zähler und Nenner stehen schon als Faktoren da (Chips). Antippen: erst ein Faktor oben, dann ein gleicher unten —
     beide werden gestrichen. Ungleiche Faktoren oder eine Summe lassen sich nicht streichen. Unten: welche Zahlen x
     nicht annehmen darf (aus dem ursprünglichen Nenner) und die Werteprobe bei x = 2. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var feld = fig.querySelector('.kuerz-feld'), formel = fig.querySelector('[data-rolle="formel"]'), knopf = fig.querySelector('.kuerz-fertig');
    var AUFG = [
      { z: ['2', '3', 'x'], n: ['3', '5', 'x'], text: 'Kürze \\(\\dfrac{6x}{15x}\\). Tipp oben einen Faktor an, dann den gleichen unten.', ex: 'x ≠ 0' },
      { z: ['2', '2', '(x + 1)'], n: ['2', '3', '(x + 1)'], text: 'Kürze \\(\\dfrac{4(x + 1)}{6(x + 1)}\\) vollständig.', ex: 'x ≠ −1' },
      { z: ['x', '(x − 2)'], n: ['3', 'x'], text: 'Kürze \\(\\dfrac{x(x - 2)}{3x}\\). Darf das \\(x\\) in der Klammer mit?', ex: 'x ≠ 0' },
      { z: ['(x + 1)', '(x − 1)'], n: ['(x − 1)', '(x + 4)'], text: 'Kürze \\(\\dfrac{(x + 1)(x - 1)}{(x - 1)(x + 4)}\\).', ex: 'x ≠ 1 und x ≠ −4' },
      { z: ['(x + 2)'], n: ['(x + 6)'], text: 'Und \\(\\dfrac{x + 2}{x + 6}\\)? Wenn nichts geht, drück «nichts mehr zu kürzen».', ex: 'x ≠ −6' }
    ];
    var S = null, wahl = null, meldung = '';
    function wert(f){ if (/^\d+$/.test(f)) return B(+f); var m = f.replace(/[()\s]/g, '').replace('−', '-'); if (m === 'x') return B(2);
      var t = m.match(/^x([+-]\d+)$/); return B(2 + +t[1]); }
    function produkt(l){ return l.reduce(function(p, f){ return bMul(p, wert(f)); }, B(1)); }
    function offen(){ var zl = [], k = 0;
      S.z.forEach(function(f, i){ if (!S.zw[i]) zl.push(f); });
      var nl = S.n.filter(function(f, j){ return !S.nw[j]; });
      zl.forEach(function(f){ var j = nl.indexOf(f); if (j >= 0){ k++; nl.splice(j, 1); } });
      return k; }
    function setup(i){ return function(){ var a = AUFG[i]; S = { z: a.z, n: a.n, zw: a.z.map(function(){ return false; }), nw: a.n.map(function(){ return false; }), ex: a.ex, fertig: false }; wahl = null; meldung = ''; }; }
    function zustand(){ return S ? { offen: offen(), fertig: S.fertig } : { offen: 1, fertig: false }; }
    function zeichnen(){
      if (!S) return;
      var h = '<div class="kz-zeile kz-oben">';
      S.z.forEach(function(f, i){ h += '<button type="button" class="chip zaehler' + (S.zw[i] ? ' weg' : '') + (wahl === i ? ' gewaehlt' : '') + '" data-o="' + i + '"' + (S.zw[i] ? ' disabled' : '') + '>' + f + '</button>'; });
      h += '</div><div class="kz-strich"></div><div class="kz-zeile kz-unten">';
      S.n.forEach(function(f, j){ h += '<button type="button" class="chip nenner' + (S.nw[j] ? ' weg' : '') + '" data-u="' + j + '"' + (S.nw[j] ? ' disabled' : '') + '>' + f + '</button>'; });
      feld.innerHTML = h + '</div>';
      var zr = S.z.filter(function(f, i){ return !S.zw[i]; }), nr = S.n.filter(function(f, j){ return !S.nw[j]; });
      var bleibt = (zr.length ? zr.join(' · ') : '1') + ' / ' + (nr.length ? nr.join(' · ') : '1');
      formel.innerHTML = 'jetzt: ' + bleibt + ' <span class="grau">(Probe mit x = 2: vorher ' + bTxt(bDiv(produkt(S.z), produkt(S.n))) + ', jetzt ' +
        bTxt(bDiv(produkt(zr), produkt(nr))) + ')</span><br><span class="grau">nicht erlaubt: ' + S.ex + '</span>' + (meldung ? '<br><span class="nein-text">' + meldung + '</span>' : '');
      if (pr) pr();
    }
    feld.addEventListener('click', function(ev){
      var b = ev.target.closest('button'); if (!b) return;
      meldung = '';
      if (b.dataset.o != null){ wahl = +b.dataset.o; }
      else if (b.dataset.u != null){
        var j = +b.dataset.u;
        if (wahl == null) meldung = 'Tipp zuerst oben einen Faktor an.';
        else if (S.z[wahl] !== S.n[j]) meldung = S.z[wahl] + ' und ' + S.n[j] + ' sind verschiedene Faktoren: Kürzen geht nur mit gleichen.';
        else { S.zw[wahl] = true; S.nw[j] = true; wahl = null; }
      }
      zeichnen();
    });
    knopf.addEventListener('click', function(){
      meldung = offen() ? 'Da steht oben und unten noch ein gleicher Faktor.' : ''; if (!offen()) S.fertig = true; zeichnen();
    });
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, AUFG.map(function(a, i){
      return { text: a.text, setup: setup(i), ok: i === 4 ? function(z){ return z.fertig; } : function(z){ return z.offen === 0; } };
    }), sim);
    setup(0)(); zeichnen();
    fig.__sim = { AUFG: AUFG };
  })();

  /* ════════ Sim 2 — Hauptnenner bauen ════════
     Hauptnenner = Zahl · x^k · (x + 1)^p · (x − 1)^q. Für jeden Nenner der Aufgabe steht daneben, womit erweitert
     werden muss — oder «geht nicht auf». Gelöst, wenn der Hauptnenner das kleinste gemeinsame Vielfache ist. */
  function nTex(d){
    var t = (d.k !== 1 || (!d.e && !d.p && !d.q) ? String(d.k) : '') + (d.e ? 'x' + (d.e > 1 ? '^' + d.e : '') : '');
    if (d.p) t += '(x + 1)'; if (d.q) t += '(x - 1)';
    return t;
  }
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var formel = fig.querySelector('[data-rolle="formel"]'), tab = fig.querySelector('.hn-tab');
    var AUFG = [
      { a: { k: 2, e: 1 }, b: { k: 3, e: 1 }, za: 1, zb: 1 },
      { a: { k: 3, e: 1 }, b: { k: 1, e: 2 }, za: 2, zb: 1 },
      { a: { k: 1, e: 1 }, b: { k: 1, e: 0, p: 1 }, za: 1, zb: 1 },
      { a: { k: 1, e: 0, q: 1 }, b: { k: 1, e: 0, p: 1, q: 1 }, za: 1, zb: 1 },
      { a: { k: 4, e: 0 }, b: { k: 6, e: 1 }, za: 5, zb: 1 }
    ];
    AUFG.forEach(function(t){ ['a', 'b'].forEach(function(s){ t[s].p = t[s].p || 0; t[s].q = t[s].q || 0; }); });
    var T = AUFG[0];
    function zustand(){ return { k: wertR(fig, 's2-k'), e: wertR(fig, 's2-e'), p: fig.querySelector('#s2-p').checked ? 1 : 0, q: fig.querySelector('#s2-q').checked ? 1 : 0 }; }
    function teilt(d, h){ return h.k % d.k === 0 && h.e >= d.e && h.p >= d.p && h.q >= d.q; }
    function kgVN(a, b){ return { k: kgV(a.k, b.k), e: Math.max(a.e, b.e), p: Math.max(a.p, b.p), q: Math.max(a.q, b.q) }; }
    function gleich(a, b){ return a.k === b.k && a.e === b.e && a.p === b.p && a.q === b.q; }
    function faktor(d, h){ return { k: h.k / d.k, e: h.e - d.e, p: h.p - d.p, q: h.q - d.q }; }
    function zeichnen(){
      var H = zustand(); zeigeWert(fig, 's2-k'); zeigeWert(fig, 's2-e');
      var zeile = function(z, d){
        var ok = teilt(d, H), f = ok ? faktor(d, H) : null;
        return '<tr><td>\\(\\dfrac{' + z + '}{' + nTex(d) + '}\\)</td><td>' + (ok ? 'erweitern mit \\(' + nTex(f) + '\\)' : '<span class="nein-text">geht nicht auf</span>') + '</td></tr>';
      };
      tab.innerHTML = zeile(T.za, T.a) + zeile(T.zb, T.b);
      var beide = teilt(T.a, H) && teilt(T.b, H), klein = gleich(H, kgVN(T.a, T.b));
      formel.innerHTML = 'dein Nenner: \\(' + nTex(H) + '\\) ' + (klein ? '<span class="ok-text">Hauptnenner</span>' : beide ? '<span class="grau">gemeinsam, aber nicht der kleinste</span>' : '<span class="nein-text">nicht gemeinsam</span>');
      setzen(tab); setzen(formel);
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, AUFG.map(function(t){
      return { text: 'Bau den Hauptnenner von \\(\\dfrac{' + t.za + '}{' + nTex(t.a) + '}\\) und \\(\\dfrac{' + t.zb + '}{' + nTex(t.b) + '}\\).',
        setup: function(){ T = t; }, ok: function(h){ return gleich(h, kgVN(t.a, t.b)); } };
    }), sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); i.addEventListener('change', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 3 — Gleichung umformen ════════
     a·x + b = c·x + d. Drei Umformungen, auf beiden Seiten gleich: + k·x, + m, : t. Die Zeilen zeigen jeden Schritt.
     Gelöst, wenn auf einer Seite nur x steht und auf der anderen eine Zahl — oder (keine Lösung) die x weg sind. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var verlauf = fig.querySelector('.gl-verlauf');
    var AUFG = [[4, 3, 1, 15], [7, -2, 3, 10], [2, 9, 5, 0], [3, 1, 3, 4], [-2, 6, 1, -9]];
    var G = AUFG[0];
    function seite(a, b){                       // a, b als Brüche
      var s = '';
      if (a[0]) s = (bEq(a, B(1)) ? '' : bEq(a, B(-1)) ? '-' : bTex(a)) + 'x';
      if (b[0] || !s) s += s ? (b[0] < 0 ? ' - ' + bTex(B(-b[0], b[1])) : ' + ' + bTex(b)) : bTex(b);
      return s;
    }
    function zustand(){
      var k = wertR(fig, 's3-k'), m = wertR(fig, 's3-m'), t = +fig.querySelector('select.sim-wahl').value;
      var a = B(G[0] + k), b = B(G[1] + m), c = B(G[2] + k), d = B(G[3] + m);
      a = bDiv(a, B(t)); b = bDiv(b, B(t)); c = bDiv(c, B(t)); d = bDiv(d, B(t));
      return { k: k, m: m, t: t, a: a, b: b, c: c, d: d,
        geloest: (bEq(a, B(1)) && !b[0] && !c[0]) || (bEq(c, B(1)) && !d[0] && !a[0]),
        xweg: !a[0] && !c[0] };
    }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's3-k'); zeigeWert(fig, 's3-m');
      var z = [];
      z.push(['\\(' + seite(B(G[0]), B(G[1])) + ' = ' + seite(B(G[2]), B(G[3])) + '\\)', 'Start']);
      if (Z.k) z.push(['\\(' + seite(B(G[0] + Z.k), B(G[1])) + ' = ' + seite(B(G[2] + Z.k), B(G[3])) + '\\)', (Z.k > 0 ? '+ ' : '− ') + (Math.abs(Z.k) === 1 ? '' : Math.abs(Z.k)) + 'x auf beiden Seiten']);
      if (Z.m) z.push(['\\(' + seite(B(G[0] + Z.k), B(G[1] + Z.m)) + ' = ' + seite(B(G[2] + Z.k), B(G[3] + Z.m)) + '\\)', (Z.m > 0 ? '+ ' : '− ') + Math.abs(Z.m) + ' auf beiden Seiten']);
      if (Z.t !== 1) z.push(['\\(' + seite(Z.a, Z.b) + ' = ' + seite(Z.c, Z.d) + '\\)', 'beide Seiten : ' + mz(Z.t)]);
      var schluss = '';
      if (Z.geloest) schluss = '<span class="ok-text">gelöst</span>';
      else if (Z.xweg) schluss = bEq(Z.b, Z.d) ? '<span class="ok-text">immer wahr: alle Zahlen sind Lösungen</span>' : '<span class="ok-text">immer falsch: keine Lösung</span>';
      verlauf.innerHTML = z.map(function(r){ return '<div class="gl-zeile"><span class="gl-term">' + r[0] + '</span><span class="gl-notiz">' + r[1] + '</span></div>'; }).join('') +
        (schluss ? '<div class="gl-zeile"><span class="gl-term">' + schluss + '</span><span class="gl-notiz"></span></div>' : '');
      setzen(verlauf);
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    var texte = ['Löse: Stell die Regler so, dass am Schluss «x = Zahl» steht.', 'Löse. Bring zuerst alle x auf die linke Seite.',
                 'Löse. Das x darf auch rechts allein stehen.', 'Bring alle x auf eine Seite. Was bleibt übrig?', 'Löse. Achtung: Links steht −2x.'];
    pr = Leiste(fig, AUFG.map(function(g, i){
      return { text: texte[i] + ' \\(' + seite(B(g[0]), B(g[1])) + ' = ' + seite(B(g[2]), B(g[3])) + '\\)', setup: function(){ G = g; },
        ok: i === 3 ? function(z){ return z.xweg; } : function(z){ return z.geloest; } };
    }), sim);
    fig.querySelectorAll('input, select').forEach(function(i){ i.addEventListener('input', zeichnen); i.addEventListener('change', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 4 — Formel rückwärts rechnen ════════
     Die Formel als Rechenkette vorwärts (wie die gesuchte Grösse zum Ergebnis wird). Rückwärts: die Umkehrungen in
     umgekehrter Reihenfolge antippen. Die Probe mit Zahlen zeigt sofort, ob die Kette stimmt. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var vor = fig.querySelector('.kette-vor'), rueck = fig.querySelector('.kette-rueck'), knoepfe = fig.querySelector('.kette-knoepfe'), formel = fig.querySelector('[data-rolle="formel"]');
    var AUFG = [
      { f: 's = v \\cdot t', nach: 't', erg: 's', vor: ['· v'], soll: [': v'], knoepfe: [': v', '· v', '− v'], w: { v: 4, t: 3 }, form: function(l){ return l.length ? 's : v' : 's'; } },
      { f: 'U = R \\cdot I', nach: 'R', erg: 'U', vor: ['· I'], soll: [': I'], knoepfe: [': I', '· I', ': R'], w: { R: 5, I: 2 } },
      { f: 'y = 4x - 5', nach: 'x', erg: 'y', vor: ['· 4', '− 5'], soll: ['+ 5', ': 4'], knoepfe: ['+ 5', '− 5', ': 4', '· 4'], w: { x: 3 } },
      { f: 'A = \\dfrac{a \\cdot b}{2}', nach: 'a', erg: 'A', vor: ['· b', ': 2'], soll: ['· 2', ': b'], knoepfe: ['· 2', ': 2', ': b', '· b'], w: { a: 6, b: 5 } },
      { f: 'U = 2(a + b)', nach: 'b', erg: 'U', vor: ['+ a', '· 2'], soll: [': 2', '− a'], knoepfe: [': 2', '− a', '· 2', '+ a'], w: { a: 4, b: 3 } }
    ];
    var T = AUFG[0], weg = [];
    function op(x, o){                    // o: «· v», «+ 5», …; Werte aus T.w
      var z = o.split(' '), w = z[1], y = /^\d+$/.test(w) ? +w : T.w[w];
      return z[0] === '·' ? x * y : z[0] === ':' ? x / y : z[0] === '+' ? x + y : x - y;
    }
    function zustand(){ return { weg: weg.slice(), soll: T.soll }; }
    function zeichnen(){
      var start = T.w[T.nach], x = start, h = '<span class="kt-box gesucht">' + T.nach + ' = ' + start + '</span>';
      T.vor.forEach(function(o){ x = op(x, o); h += '<span class="kt-pfeil">' + o + ' →</span><span class="kt-box">' + +x.toFixed(4) + '</span>'; });
      vor.innerHTML = '<span class="kt-name">vorwärts</span>' + h + '<span class="kt-name">= ' + T.erg + '</span>';
      var y = x, r = '<span class="kt-name">rückwärts</span><span class="kt-box">' + T.erg + ' = ' + +x.toFixed(4) + '</span>';
      weg.forEach(function(o){ y = op(y, o); r += '<span class="kt-pfeil">' + o + ' →</span><span class="kt-box">' + +y.toFixed(4) + '</span>'; });
      rueck.innerHTML = r;
      var richtig = weg.length === T.soll.length && weg.every(function(o, i){ return o === T.soll[i]; });
      formel.innerHTML = weg.length ? (Math.abs(y - start) < 1e-9 && weg.length === T.soll.length
        ? '<span class="ok-text">Probe stimmt: wieder ' + T.nach + ' = ' + start + '</span>'
        : '<span class="grau">Probe: ' + +y.toFixed(4) + (weg.length < T.soll.length ? ' … noch nicht fertig' : ' ≠ ' + start) + '</span>') : '<span class="grau">Tipp die Umkehrungen in der richtigen Reihenfolge an.</span>';
      knoepfe.innerHTML = T.knoepfe.map(function(o){ return '<button type="button" class="chip" data-op="' + o + '">' + o + '</button>'; }).join('') +
        '<button type="button" class="chip zurueck">↶ zurück</button>';
      if (pr) pr();
    }
    knoepfe.addEventListener('click', function(ev){
      var b = ev.target.closest('button'); if (!b) return;
      if (b.classList.contains('zurueck')) weg.pop(); else if (weg.length < 3) weg.push(b.dataset.op);
      zeichnen();
    });
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, AUFG.map(function(t){
      return { text: 'Stelle \\(' + t.f + '\\) nach \\(' + t.nach + '\\) um: Welche Umkehrungen, in welcher Reihenfolge?',
        setup: function(){ T = t; weg = []; }, ok: function(z){ return z.weg.length === t.soll.length && z.weg.every(function(o, i){ return o === t.soll[i]; }); } };
    }), sim);
    zeichnen();
  })();

  /* ════════ Übungen mit Rückmeldung ════════
     Feldarten: t = Bruchterm in x (gleichwertig; T.form prüft gekürzt / ein Bruchstrich), f = Formel in mehreren Grössen
     (gleichwertig an Zufallsstellen, gesuchte Grösse kommt nicht vor), L = Lösungsmenge, sonst Zahl (exakt, auch 7/3, 2.5).
     Fehlversuch → gezielte Diagnose oder die Probe mit einer Zahl. Tipps in drei Stufen. Testhaken: box.__aufgabe, box.__typ. */
  (function(){
    var ALLE = document.querySelectorAll('.uebung[data-typ]'); if (!ALLE.length) return;
    function kz(n){ return n < 0 ? '(' + n + ')' : String(n); }
    function txt(r){ return pEq(r.n, [1]) ? pTxt(r.z) : (P(r.z).length > 1 || r.z[0] < 0 ? '(' + pTxt(r.z) + ')' : pTxt(r.z)) + '/' + (P(r.n).length > 1 || pInhalt(r.n) !== Math.abs(P(r.n)[P(r.n).length - 1]) ? '(' + pTxt(r.n) + ')' : pTxt(r.n)); }
    function frei(r, A){ return !A.pole.some(function(p){ return pNullAn(r.n, p); }); }
    /* Probe mit Zahl: Wert des eigenen und des richtigen Terms an einer Stelle, an der beide definiert sind */
    function probeTerm(eigen, A){
      var stellen = [B(2), B(3), B(5), B(-3), B(7)];
      for (var j = 0; j < stellen.length; j++){
        var s = stellen[j]; if (pNullAn(eigen.n, s) || pNullAn(A.r.n, s) || pNullAn(A.o.n, s)) continue;
        return 'Probe mit \\(x = ' + s[0] + '\\): Deiner gibt \\(' + bTex(bDiv(pWert(eigen.z, s), pWert(eigen.n, s))) + '\\), der Term der Aufgabe \\(' + bTex(bDiv(pWert(A.o.z, s), pWert(A.o.n, s))) + '\\).';
      }
      return '';
    }
    function formBruch(r, baum){
      if (!einBruch(baum)) return 'Gleichwertig, aber schreib das Ergebnis auf <b>einen Bruchstrich</b>.';
      var g = gemeinsam(r.r);
      if (g) return 'Gleichwertig, aber noch nicht vollständig <b>gekürzt</b>: Zähler und Nenner haben noch den gemeinsamen Faktor \\(' + (g.art === 'zahl' ? g.g : pTex(g.f)) + '\\).';
      return null;
    }
    function rSchl(o){ return pTxt(o.z) + '|' + pTxt(o.n); }

    /* Feste Aufgaben (Festhalten, Clips, Erkundungen, Kapitelaufgaben, Gesamttest) in Normalform:
       Bruchterme als «Zähler|Nenner» ausmultipliziert (ungekürzt), Gleichungen als «links|rechts» zusammengefasst. */
    var SPERRE = [
      'ku|6x|9x^2', 'ku|x^2-9|2x+6', 'ku|x^2+4x+4|x^2-4', 'ku|x+3|x+5', 'ku|x-3|-x+3', 'ku|6x|15x', 'ku|4x+4|6x+6', 'ku|x^2-2x|3x',
      'ku|x^2-1|x^2+3x-4', 'ku|x+2|x+6', 'ku|12x^2|18x', 'ku|5x-10|x-2', 'ku|x^2-16|x+4', 'ku|x^2-6x+9|x^2-9', 'ku|x+6|x+2', 'ku|8x|12x^2',
      'ku|x^2-4|x+2', 'ku|x+7|x+1', 'ku|-x+5|x-5', 'ku|x^2-10x+25|3x-15', 'ku|-x+2|x-2',
      'au|0|4', 'au|-5|0',
      'mb|24x|36x^2', 'mb|5x^2|10x', 'mb|18x|12x^2', 'mb|3x^3-3x|x^2+x', 'mb|2x^2|6x', 'mb|4x^2|2x',
      'pb|7x|x^2', 'pb|3x|2x^2', 'pb|x+2|x^2+x', 'pb|28x|12x^2', 'pb|x+8|x^2+2x', 'pb|1|x^2+x', 'pb|5x-3|x^2-x', 'pb|5x|6x^2', 'pb|2x^2+3x|3x^3', 'pb|2x+1|x^2+x',
      'gl|5x-7|2x+8', 'gl|2x-10|2x-10', 'gl|2x+2|2x+5', 'gl|4x+3|x+15', 'gl|7x-2|3x+10', 'gl|2x+9|5x', 'gl|3x+1|3x+4', 'gl|-2x+6|x-9',
      'gl|8x-5|3x+20', 'gl|4x-12|2x+2', 'gl|2x+6|2x+6', 'gl|2x+6|2x+3', 'gl|-x+3|2x', 'gl|6x+4|2x+24', 'gl|3x-6|x+8', 'gl|2x+8|2x+8',
      'gl|x+5|x+2', 'gl|4x+6|2x+14', 'gl|4x+2|4x+2',
      'bg|kl|3|4|1|-2|1', 'bg|xx|2|3|1|10', 'bg|xx|3|6|1|4', 'bg|kl|4|6|3|-1|2',
      'fw|taxi|6|2.5|10', 'fw|rechteck|7|5', 'fw|treppe|a|25', 'fw|weg|60|2.5', 'fw|temp|100'
    ];
    function gesperrt(T, A){ return !!T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }

    /* ---- Formelbank für «umstellen»: Formel, Grössen, gesuchte Grösse, Lösung, typische Fehler ---- */
    var FORMELN = [
      { id: 'Fma', tex: 'F = m \\cdot a', g: 'Fma', z: 'm', l: 'F/a', lt: '\\dfrac{F}{a}', fn: function(w){ return w.F / w.a; }, f: [[function(w){ return w.F * w.a; }, 'Umkehrung'], [function(w){ return w.a / w.F; }, 'Umkehrung']] },
      { id: 'Fma', tex: 'F = m \\cdot a', g: 'Fma', z: 'a', l: 'F/m', lt: '\\dfrac{F}{m}', fn: function(w){ return w.F / w.m; }, f: [[function(w){ return w.F * w.m; }, 'Umkehrung'], [function(w){ return w.m / w.F; }, 'Umkehrung']] },
      { id: 'Emgh', tex: 'E = m \\cdot g \\cdot h', g: 'Emgh', z: 'm', l: 'E/(g*h)', lt: '\\dfrac{E}{g \\cdot h}', fn: function(w){ return w.E / (w.g * w.h); }, f: [[function(w){ return w.E / w.g * w.h; }, 'Klammer'], [function(w){ return w.E - w.g * w.h; }, 'Umkehrung']] },
      { id: 'PUI', tex: 'P = U \\cdot I', g: 'PUI', z: 'U', l: 'P/I', lt: '\\dfrac{P}{I}', fn: function(w){ return w.P / w.I; }, f: [[function(w){ return w.P * w.I; }, 'Umkehrung'], [function(w){ return w.I / w.P; }, 'Umkehrung']] },
      { id: 'Agh', tex: 'A = \\dfrac{g \\cdot h}{2}', g: 'Agh', z: 'g', l: '2A/h', lt: '\\dfrac{2A}{h}', fn: function(w){ return 2 * w.A / w.h; }, f: [[function(w){ return w.A * w.h / 2; }, 'Umkehrung'], [function(w){ return w.A / (2 * w.h); }, 'Umkehrung'], [function(w){ return 2 * w.A * w.h; }, 'Umkehrung']] },
      { id: 'Mab', tex: 'M = \\dfrac{a + b}{2}', g: 'Mab', z: 'b', l: '2M-a', lt: '2M - a', fn: function(w){ return 2 * w.M - w.a; }, f: [[function(w){ return w.M / 2 - w.a; }, 'Umkehrung'], [function(w){ return 2 * (w.M - w.a); }, 'Reihenfolge'], [function(w){ return 2 * w.M + w.a; }, 'Vorzeichen']] },
      { id: 'Uabc', tex: 'U = a + b + c', g: 'Uabc', z: 'c', l: 'U-a-b', lt: 'U - a - b', fn: function(w){ return w.U - w.a - w.b; }, f: [[function(w){ return w.U - w.a + w.b; }, 'Vorzeichen'], [function(w){ return w.U + w.a + w.b; }, 'Vorzeichen']] },
      { id: 'Vabh', tex: 'V = a \\cdot b \\cdot h', g: 'Vabh', z: 'a', l: 'V/(b*h)', lt: '\\dfrac{V}{b \\cdot h}', fn: function(w){ return w.V / (w.b * w.h); }, f: [[function(w){ return w.V / w.b * w.h; }, 'Klammer'], [function(w){ return w.V - w.b * w.h; }, 'Umkehrung']] },
      { id: 'ZKp', tex: 'Z = \\dfrac{K \\cdot p}{100}', g: 'ZKp', z: 'K', l: '100Z/p', lt: '\\dfrac{100 Z}{p}', fn: function(w){ return 100 * w.Z / w.p; }, f: [[function(w){ return w.Z * w.p / 100; }, 'Umkehrung'], [function(w){ return w.Z / (100 * w.p); }, 'Umkehrung']] },
      { id: 'Aach', tex: 'A = \\dfrac{a + c}{2} \\cdot h', g: 'Aach', z: 'a', l: '2A/h-c', lt: '\\dfrac{2A}{h} - c', fn: function(w){ return 2 * w.A / w.h - w.c; }, f: [[function(w){ return 2 * w.A / (w.h - w.c); }, 'Reihenfolge'], [function(w){ return (2 * w.A - w.c) / w.h; }, 'Reihenfolge'], [function(w){ return 2 * w.A / w.h + w.c; }, 'Vorzeichen']] },
      { id: 'ymq', tex: 'y = m \\cdot x + q', g: 'ymxq', z: 'q', l: 'y-m*x', lt: 'y - mx', fn: function(w){ return w.y - w.m * w.x; }, f: [[function(w){ return w.y + w.m * w.x; }, 'Vorzeichen'], [function(w){ return w.y / (w.m * w.x); }, 'Umkehrung']] },
      { id: 'ymq', tex: 'y = m \\cdot x + q', g: 'ymxq', z: 'm', l: '(y-q)/x', lt: '\\dfrac{y - q}{x}', fn: function(w){ return (w.y - w.q) / w.x; }, f: [[function(w){ return w.y / w.x - w.q; }, 'Reihenfolge'], [function(w){ return (w.y + w.q) / w.x; }, 'Vorzeichen']] }
    ];

    var TYPEN = {
      /* ── Kapitel 1 ── */
      'kuerzen': { felder: ['t'],
        schl: function(A){ return 'ku|' + rSchl(A.o); },
        eingabe: function(A){ return { t: A.loes }; },
        neu: function(){
          var art = zufall(['mono', 'mono', 'lin', 'dq', 'quad', 'quad', 'frei']), o, r, fak, k, loes;
          if (art === 'mono'){
            var g = zufallG(2, 6), p, q, e1, e2;
            do { p = zufallG(1, 6); q = zufallG(1, 6); } while (ggT(p, q) !== 1 || (p === 1 && q === 1));
            do { e1 = zufallG(0, 2); e2 = zufallG(0, 2); } while (e1 + e2 === 0);
            o = R(mon(g * p, e1), mon(g * q, e2));
            r = e1 >= e2 ? R(mon(p, e1 - e2), [q]) : R([p], mon(q, e2 - e1));
            var gx = g + (Math.min(e1, e2) ? 'x' + (Math.min(e1, e2) > 1 ? '^' + Math.min(e1, e2) : '') : '');
            fak = '\\dfrac{' + gx + ' \\cdot ' + pTex(mon(p, e1 - Math.min(e1, e2))) + '}{' + gx + ' \\cdot ' + pTex(mon(q, e2 - Math.min(e1, e2))) + '}';
            k = [g * p, e1, g * q, e2, g, p];
          } else if (art === 'lin'){
            var c, d, a = nz(-9, 9);
            do { c = zufallG(1, 6); d = zufallG(1, 6); } while (ggT(c, d) !== 1 || c === d);
            o = R(pMul([c], lin(1, a)), pMul([d], lin(1, a))); r = R([c], [d]);
            fak = '\\dfrac{' + c + '(' + pTex(lin(1, a)) + ')}{' + (d === 1 ? '' : d) + '(' + pTex(lin(1, a)) + ')}';
            k = [c, d, a];
          } else if (art === 'dq'){
            var b = zufallG(1, 9), kk = zufallG(1, 4), s = zufall([1, -1]);
            o = R([-b * b, 0, 1], pMul([kk], lin(1, s * b))); r = R(lin(1, -s * b), [kk]);
            fak = '\\dfrac{(' + pTex(lin(1, -s * b)) + ')(' + pTex(lin(1, s * b)) + ')}{' + (kk === 1 ? '' : kk) + '(' + pTex(lin(1, s * b)) + ')}';
            k = [b, kk, s];
          } else if (art === 'quad'){
            var aa, bb, cc;
            do { aa = nz(-7, 7); bb = nz(-7, 7); cc = nz(-7, 7); } while (aa === bb || aa === cc || bb === cc);
            o = R(pMul(lin(1, aa), lin(1, bb)), pMul(lin(1, aa), lin(1, cc))); r = R(lin(1, bb), lin(1, cc));
            fak = '\\dfrac{(' + pTex(lin(1, aa)) + ')(' + pTex(lin(1, bb)) + ')}{(' + pTex(lin(1, aa)) + ')(' + pTex(lin(1, cc)) + ')}';
            k = [aa, bb, cc];
          } else {
            var u, v;
            do { u = nz(-9, 9); v = nz(-9, 9); } while (u === v);
            o = R(lin(1, u), lin(1, v)); r = o; fak = '\\dfrac{' + pTex(lin(1, u)) + '}{' + pTex(lin(1, v)) + '}';
            k = [u, v];
          }
          return { art: art, k: k, o: o, r: r, fak: fak, loes: txt(r), pole: [],
            muster: '\\(' + rTex(o) + ' = \\) {t}', text: 'Kürze so weit wie möglich.' }; },
        falsche: function(A){
          var f = [];
          if (A.art === 'frei' || A.art === 'quad'){
            var z = A.o.z.slice(0, -1), n = A.o.n.slice(0, -1);          // Summand mit der höchsten Potenz «weggekürzt»
            if (!pNull(n)) f.push([R(z, n), 'Summanden']);
          }
          if (A.art === 'dq') f.push([R(lin(1, -A.k[2] * -A.k[0]), [A.k[1]]), 'Vorzeichen']);
          return f.filter(function(p){ return !rEq(p[0], A.r); }); },
        fehler: function(A){
          var f = TYPEN.kuerzen.falsche(A).map(function(p){ return [{ t: txt(p[0]) }, p[1]]; });
          if (A.art !== 'frei') f.push([{ t: txt(A.o) }, 'gekürzt']);
          return f; },
        form: function(A, r){ return formBruch(r, r.baum); },
        pruefen: function(A, e){
          var f = TYPEN.kuerzen.falsche(A);
          for (var j = 0; j < f.length; j++) if (rEq(e.t.r, f[j][0])){
            if (f[j][1] === 'Summanden') return '<b>Summanden</b> darfst du nicht kürzen, nur Faktoren. ' + probeTerm(e.t.r, A);
            return '<b>Vorzeichen</b> prüfen: Welche Klammer steht oben und unten gleich? ' + probeTerm(e.t.r, A);
          }
          return 'Zerlege Zähler und Nenner in Faktoren, dann kürze nur gleiche Faktoren. ' + probeTerm(e.t.r, A); },
        tipps: function(A){ return ['Zerlege Zähler und Nenner zuerst in Faktoren (ausklammern, binomische Formel, Zweiklammersatz).',
          A.art === 'frei' ? 'Zähler und Nenner sind Summen ohne gemeinsamen Faktor.' : 'In Faktoren: \\(' + A.fak + '\\)']; },
        loesung: function(A){ return rTex(A.o) + ' = ' + A.fak + (A.art === 'frei' ? '' : ' = ' + rTex(A.r)); } },

      'ausschluss': { felder: ['u', 'v'],
        schl: function(A){ return 'au|' + A.w.slice().sort(function(a, b){ return a - b; }).join('|'); },
        eingabe: function(A){ return { u: String(A.w[0]), v: String(A.w[1]) }; },
        neu: function(){
          var art = zufall(['x', 'ab', 'qq']), w, n;
          if (art === 'x'){ var a = nz(-9, 9); w = [0, a]; n = pMul([0, 1], lin(1, -a)); }
          else if (art === 'ab'){ var p, q; do { p = nz(-7, 7); q = nz(-7, 7); } while (p === q || p === -q); w = [p, q]; n = pMul(lin(1, -p), lin(1, -q)); }
          else { var b = zufallG(1, 9); w = [-b, b]; n = [-b * b, 0, 1]; }
          var c; do { c = nz(-9, 9); } while (w.indexOf(-c) >= 0 || w.indexOf(c) >= 0);
          return { art: art, w: w, n: n, c: c, z: lin(1, c),
            muster: 'nicht erlaubt: \\(x = \\) {u} und \\(x = \\) {v}', text: 'Für welche Zahlen ist \\(' + rTex(R(lin(1, c), n)) + '\\) nicht definiert?' }; },
        richtig: function(A, e){ var s = [bZahl(e.u), bZahl(e.v)].sort(function(a, b){ return a - b; }), t = A.w.slice().sort(function(a, b){ return a - b; }); return s[0] === t[0] && s[1] === t[1]; },
        fehler: function(A){ var f = [];
          if (A.art !== 'qq') f.push([{ u: String(-A.w[0]), v: String(-A.w[1]) }, 'Vorzeichen']);
          f.push([{ u: String(-A.c), v: String(A.w[1]) }, 'Zähler']);
          return f.filter(function(p){ var s = [+p[0].u, +p[0].v].sort(), t = A.w.slice().sort(); return s[0] !== t[0] || s[1] !== t[1]; }); },
        pruefen: function(A, e){
          var u = bZahl(e.u), v = bZahl(e.v);
          if (u === -A.c || v === -A.c) return 'Mit \\(x = ' + (-A.c) + '\\) wird der <b>Zähler</b> 0, und dann ist der Bruch einfach 0. Verboten ist nur ein Nenner 0.';
          var n0 = function(x){ return bZahl(pWert(A.n, B(x))); };
          var falsch = [u, v].filter(function(x){ return n0(x) !== 0; });
          if (falsch.length) return 'Setz ein: Mit \\(x = ' + falsch[0] + '\\) ist der Nenner \\(' + n0(falsch[0]) + '\\), nicht 0. ' + (A.art !== 'qq' ? 'Achte auf das <b>Vorzeichen</b>: \\(x - 3 = 0\\) gilt für \\(x = 3\\).' : '');
          return 'Es braucht zwei verschiedene Zahlen.'; },
        tipps: function(A){ return ['Der Nenner darf nicht 0 sein. Zerlege ihn in Faktoren: Ein Produkt ist 0, wenn ein Faktor 0 ist.',
          '\\(' + pTex(A.n) + ' = ' + (A.art === 'x' ? 'x(' + pTex(lin(1, -A.w[1])) + ')' : '(' + pTex(lin(1, -A.w[0])) + ')(' + pTex(lin(1, -A.w[1])) + ')') + '\\)']; },
        loesung: function(A){ return pTex(A.n) + ' = 0 \\text{ für } x = ' + A.w[0] + ' \\text{ und } x = ' + A.w[1]; } },

      /* ── Kapitel 2 ── */
      'malbruch': { felder: ['t'],
        schl: function(A){ return 'mb|' + rSchl(A.o); },
        eingabe: function(A){ return { t: A.loes }; },
        neu: function(){
          var art = zufall(['mal', 'mal', 'durch', 'durch', 'bin']), o, r, k, tex;
          function bruch(){ var p, q, e = zufallG(0, 2), oben = Math.random() < 0.5; do { p = zufallG(1, 9); q = zufallG(1, 9); } while (ggT(p, q) !== 1 || (p === 1 && q === 1));
            return { p: p, q: q, e: e, oben: oben, r: oben ? R(mon(p, e), [q]) : R([p], mon(q, e)) }; }
          if (art === 'bin'){
            var a = zufallG(1, 9), kk = zufallG(2, 6), m = zufallG(2, 9);
            o = rMul(R([-a * a, 0, 1], [0, kk]), R([0, m], lin(1, a))); r = rKurz(R(pMul([m], lin(1, -a)), [kk]));
            tex = '\\dfrac{' + pTex([-a * a, 0, 1]) + '}{' + kk + 'x} \\cdot \\dfrac{' + m + 'x}{' + pTex(lin(1, a)) + '}'; k = [a, kk, m];
            var weg = '\\dfrac{(' + pTex(lin(1, -a)) + ')(' + pTex(lin(1, a)) + ') \\cdot ' + m + 'x}{' + kk + 'x \\cdot (' + pTex(lin(1, a)) + ')}';
          } else {
            var f1, f2, s = 0;
            do { f1 = bruch(); f2 = bruch(); o = art === 'mal' ? rMul(f1.r, f2.r) : rDiv(f1.r, f2.r); r = rKurz(o); s++; }
            while (s < 80 && (f1.e + f2.e === 0 || (pEq(r.n, [1]) && P(r.z).length === 1) || !gemeinsam(o)));
            tex = rTex(f1.r) + (art === 'mal' ? ' \\cdot ' : ' : ') + rTex(f2.r);
            k = [f1.p, f1.q, f1.oben ? 1 : 0, f1.e, f2.p, f2.q, f2.oben ? 1 : 0, f2.e]; var paar = [f1, f2];
          }
          var aus = { art: art, k: k, o: o, r: r, tex: tex, loes: txt(r), pole: [], weg: art === 'bin' ? weg : rTex(o), muster: '\\(' + tex + ' = \\) {t}', text: 'Rechne und kürze vollständig.' };
          if (art !== 'bin') aus.f = paar;
          return aus; },
        falsche: function(A){
          var f = [];
          if (A.art === 'durch'){ f.push([rMul(A.f[0].r, A.f[1].r), 'Kehrwert']); f.push([rMul(R(A.f[0].r.n, A.f[0].r.z), A.f[1].r), 'Kehrwert']); }
          return f.filter(function(p, i){ return !rEq(p[0], A.r) && !f.slice(0, i).some(function(q){ return rEq(q[0], p[0]); }); }); },
        fehler: function(A){ var f = TYPEN.malbruch.falsche(A).map(function(p){ return [{ t: txt(p[0]) }, p[1]]; }); if (gemeinsam(A.o)) f.push([{ t: txt(A.o) }, 'gekürzt']); return f; },
        form: function(A, r){ return formBruch(r, r.baum); },
        pruefen: function(A, e){
          var f = TYPEN.malbruch.falsche(A);
          for (var j = 0; j < f.length; j++) if (rEq(e.t.r, f[j][0])) return '<b>Kehrwert</b>: Beim Dividieren wird der zweite Bruch umgedreht und dann multipliziert. ' + probeTerm(e.t.r, A);
          return 'Zähler mal Zähler, Nenner mal Nenner, dann kürzen. ' + probeTerm(e.t.r, A); },
        tipps: function(A){ return [A.art === 'durch' ? 'Dividieren heisst: mit dem Kehrwert des zweiten Bruchs multiplizieren.' : 'Zähler mal Zähler, Nenner mal Nenner. Vor dem Ausrechnen kürzen spart Arbeit.',
          A.art === 'bin' ? 'Zerlege \\(' + pTex([-A.k[0] * A.k[0], 0, 1]) + ' = (' + pTex(lin(1, -A.k[0])) + ')(' + pTex(lin(1, A.k[0])) + ')\\), dann über Kreuz kürzen.' : 'Zuerst die Zahlen kürzen, dann die Potenzen von \\(x\\).']; },
        loesung: function(A){ return A.tex + ' = ' + A.weg + ' = ' + rTex(A.r); } },

      'plusbruch': { felder: ['t'],
        schl: function(A){ return 'pb|' + rSchl(A.o); },
        eingabe: function(A){ return { t: A.loes }; },
        neu: function(){
          var art = zufall(['gleich', 'mono', 'mono', 'lin', 'lin']), s = zufall([1, -1]), o, r, k, tex, hn, nenner;
          if (art === 'gleich'){
            var kk = zufallG(1, 6), a, b; do { a = zufallG(1, 9); b = zufallG(1, 9); } while (a + s * b === 0 || ggT(a, kk) !== 1 || ggT(b, kk) !== 1);
            var n = mon(kk, 1); o = rAdd(R([a], n), R([s * b], n)); k = [a, b, kk, s];
            tex = '\\dfrac{' + a + '}{' + pTex(n) + '} ' + (s > 0 ? '+' : '-') + ' \\dfrac{' + b + '}{' + pTex(n) + '}';
          } else if (art === 'mono'){
            var p, q, i, j, a2, b2;
            do { p = zufallG(1, 6); q = zufallG(1, 6); i = zufallG(1, 2); j = zufallG(1, 2); } while (p === q && i === j);
            do { a2 = zufallG(1, 9); b2 = zufallG(1, 9); } while (ggT(a2, p) !== 1 || ggT(b2, q) !== 1);
            o = rAdd(R([a2], mon(p, i)), R([s * b2], mon(q, j))); k = [a2, p, i, s, b2, q, j];
            tex = '\\dfrac{' + a2 + '}{' + pTex(mon(p, i)) + '} ' + (s > 0 ? '+' : '-') + ' \\dfrac{' + b2 + '}{' + pTex(mon(q, j)) + '}';
            hn = mon(kgV(p, q), Math.max(i, j));
          } else {
            var a3 = zufallG(1, 6), b3 = zufallG(1, 6), c = nz(-6, 6);
            o = rAdd(R([a3], [0, 1]), R([s * b3], lin(1, c))); k = [a3, b3, c, s];
            tex = '\\dfrac{' + a3 + '}{x} ' + (s > 0 ? '+' : '-') + ' \\dfrac{' + b3 + '}{' + pTex(lin(1, c)) + '}';
            nenner = 'x(' + pTex(lin(1, c)) + ')';
          }
          r = rKurz(o);
          var loes = art === 'lin' ? '(' + pTxt(r.z) + ')/(x(' + pTxt(lin(1, k[2])) + '))' : txt(r);
          return { art: art, k: k, s: s, o: o, r: r, tex: tex, loes: loes, hn: hn, nenner: nenner, pole: [], muster: '\\(' + tex + ' = \\) {t}', text: 'Rechne und schreib das Ergebnis auf einen Bruchstrich.' }; },
        falsche: function(A){
          var f = [];
          if (A.art === 'mono') f.push([R([A.k[0] + A.s * A.k[4]], pAdd(mon(A.k[1], A.k[2]), mon(A.k[5], A.k[6]))), 'Nenner']);
          if (A.art === 'lin') f.push([R([A.k[0] + A.s * A.k[1]], lin(2, A.k[2])), 'Nenner']);
          if (A.art === 'mono') f.push([R([A.k[0] + A.s * A.k[4]], A.hn), 'erweitert']);
          return f.filter(function(p, i){ return !pNull(p[0].n) && !rEq(p[0], A.r) && !f.slice(0, i).some(function(q){ return rEq(q[0], p[0]); }); }); },
        fehler: function(A){ var f = TYPEN.plusbruch.falsche(A).map(function(p){ return [{ t: txt(p[0]) }, p[1]]; });
          f.push([{ t: A.tex.replace(/\\dfrac\{([^}]*)\}\{([^}]*)\}/g, '($1)/($2)').replace(/\s/g, '') }, 'Bruchstrich']);
          return f; },
        form: function(A, r){ return formBruch(r, r.baum); },
        pruefen: function(A, e){
          var f = TYPEN.plusbruch.falsche(A);
          for (var j = 0; j < f.length; j++) if (rEq(e.t.r, f[j][0]))
            return f[j][1] === 'Nenner' ? 'Die <b>Nenner</b> werden nicht addiert: Erst gleichnamig machen, dann nur die Zähler addieren. ' + probeTerm(e.t.r, A)
                                        : 'Beim Gleichnamig-Machen wird auch der Zähler <b>erweitert</b>, mit demselben Faktor wie der Nenner. ' + probeTerm(e.t.r, A);
          return 'Hauptnenner suchen, beide Brüche erweitern, Zähler zusammenfassen. ' + probeTerm(e.t.r, A); },
        tipps: function(A){ return ['Zuerst gleichnamig machen: der Hauptnenner enthält jeden Faktor der beiden Nenner.',
          A.art === 'gleich' ? 'Die Nenner sind schon gleich: Zähler ' + (A.s > 0 ? 'addieren' : 'subtrahieren') + ', dann kürzen.' :
          A.art === 'mono' ? 'Hauptnenner: \\(' + pTex(A.hn) + '\\).' : 'Hauptnenner: \\(' + A.nenner + '\\).']; },
        loesung: function(A){ return A.tex + ' = ' + (A.art === 'lin' ? '\\dfrac{' + pTex(A.r.z) + '}{' + A.nenner + '}' : rTex(A.r)); } },

      /* ── Kapitel 3 ── */
      'gleichung': { felder: ['L'],
        schl: function(A){ return 'gl|' + pTxt(A.links.z) + '|' + pTxt(A.rechts.z); },
        eingabe: function(A){ return { L: A.L === 'zahl' ? bTxt(A.x).replace('−', '-') : A.L === 'leer' ? '{}' : 'Q' }; },
        neu: function(){
          var art = zufall(['beid', 'beid', 'klam', 'klam', 'spez']), x0 = nz(-9, 9), a, b, c, d, k, tex, links, rechts;
          if (art === 'beid'){
            do { a = nz(-6, 9); c = nz(-6, 9); } while (a === c);
            b = nz(-15, 15); d = (a - c) * x0 + b;
            links = R(lin(a, b)); rechts = R(lin(c, d)); tex = pTex(lin(a, b)) + ' = ' + pTex(lin(c, d)); k = [a, b, c, d];
          } else if (art === 'klam'){
            var kk = zufallG(2, 6), m = nz(-6, 6), q = nz(-6, 6);
            a = kk - 1; b = kk * m - q;
            do { c = nz(-5, 8); } while (c === a);
            d = (a - c) * x0 + b;
            links = R(lin(a, b)); rechts = R(lin(c, d)); tex = kk + '(' + pTex(lin(1, m)) + ') - (' + pTex(lin(1, q)) + ') = ' + pTex(lin(c, d)); k = [kk, m, q, c, d];
          } else {
            var aa = zufallG(2, 6), mm = nz(-6, 6), s = zufall([0, nz(-5, 5)]);
            links = R(lin(aa, aa * mm)); rechts = R(lin(aa, aa * mm + s)); tex = aa + '(' + pTex(lin(1, mm)) + ') = ' + pTex(lin(aa, aa * mm + s)); k = [aa, mm, s];
            return { art: art, k: k, L: s ? 'leer' : 'alle', links: links, rechts: rechts, tex: tex, muster: '\\(L = \\) {L}', text: 'Löse: \\(' + tex + '\\)' };
          }
          return { art: art, k: k, L: 'zahl', x: B(x0), links: links, rechts: rechts, tex: tex, muster: '\\(L = \\) {L}', text: 'Löse: \\(' + tex + '\\)' }; },
        richtig: function(A, e){ return e.L.art === A.L && (A.L !== 'zahl' || bEq(e.L.w, A.x)); },
        fehlerwerte: function(A){
          var f = [];
          if (A.art === 'beid'){ var a = A.k[0], b = A.k[1], c = A.k[2], d = A.k[3]; if ((d + b) % (a - c) === 0) f.push([B(d + b, a - c), 'Vorzeichen']); }
          if (A.art === 'klam'){ var kk = A.k[0], m = A.k[1], q = A.k[2], c2 = A.k[3], d2 = A.k[4], a2 = kk - 1, b2 = kk * m + q; if (a2 !== c2) f.push([B(d2 - b2, a2 - c2), 'Minus']); }
          return f.filter(function(p){ return !bEq(p[0], A.x); }); },
        fehler: function(A){
          if (A.L !== 'zahl') return [[{ L: A.L === 'leer' ? 'Q' : '{}' }, null], [{ L: '0' }, null]];
          return TYPEN.gleichung.fehlerwerte(A).map(function(p){ return [{ L: bTxt(p[0]).replace('−', '-') }, p[1]]; }).concat([[{ L: '{}' }, 'genau eine']]); },
        pruefen: function(A, e){
          if (A.L !== 'zahl'){
            if (e.L.art === 'zahl') return 'Bring alle \\(x\\) auf eine Seite: Sie fallen ganz weg. Was bleibt übrig, eine wahre oder eine falsche Aussage?';
            return A.L === 'leer' ? 'Übrig bleibt eine <b>falsche</b> Aussage, zum Beispiel \\(0 = ' + A.k[2] + '\\): keine Zahl passt.' : 'Übrig bleibt eine <b>wahre</b> Aussage, \\(0 = 0\\): jede Zahl passt.';
          }
          if (e.L.art !== 'zahl') return 'Diese Gleichung hat <b>genau eine</b> Lösung: Die \\(x\\) fallen nicht weg.';
          var l = pWert(A.links.z, e.L.w), r = pWert(A.rechts.z, e.L.w);
          var probe = '<b>Probe</b> mit \\(x = ' + bTex(e.L.w) + '\\): links \\(' + bTex(l) + '\\), rechts \\(' + bTex(r) + '\\). ';
          var f = TYPEN.gleichung.fehlerwerte(A);
          for (var j = 0; j < f.length; j++) if (bEq(e.L.w, f[j][0]))
            return probe + (f[j][1] === 'Vorzeichen' ? 'Beim Hinüberbringen wechselt das <b>Vorzeichen</b>: Du rechnest auf beiden Seiten minus dieselbe Zahl.' : 'Das <b>Minus</b> vor der Klammer dreht jedes Vorzeichen in der Klammer um.');
          return probe + 'Rechne Schritt für Schritt: Klammern auflösen, x auf eine Seite, Zahlen auf die andere, dann teilen.'; },
        tipps: function(A){ return ['Löse zuerst die Klammern auf und fasse jede Seite zusammen.',
          'Zusammengefasst: \\(' + pTex(A.links.z) + ' = ' + pTex(A.rechts.z) + '\\). Bring alle \\(x\\) auf eine Seite.']; },
        loesung: function(A){ var a = A.links.z[1] - A.rechts.z[1], d = A.rechts.z[0] - A.links.z[0];
          return A.tex + (A.art === 'beid' ? '' : ' \\;\\Rightarrow\\; ' + pTex(A.links.z) + ' = ' + pTex(A.rechts.z)) + ' \\;\\Rightarrow\\; ' +
            (A.L === 'zahl' ? pTex([0, a]) + ' = ' + d + ' \\;\\Rightarrow\\; L = \\{' + bTex(A.x) + '\\}' : '0 = ' + d + ' \\;\\Rightarrow\\; L = ' + (A.L === 'leer' ? '\\{\\,\\}' : '\\mathbb{Q}')); } },

      'bruchgleichung': { felder: ['L'],
        schl: function(A){ return 'bg|' + A.art + '|' + A.k.join('|'); },
        eingabe: function(A){ return { L: bTxt(A.x).replace('−', '-') }; },
        neu: function(){
          var art = zufall(['xx', 'kl', 'kl', 'gl']), p, q, x0, k, tex, f, s, hn;
          for (s = 0; s < 400; s++){
            do { p = zufallG(2, 6); q = zufallG(2, 6); } while (p === q);
            hn = kgV(p, q);
            if (art === 'xx'){ var t = nz(-3, 4); x0 = t * hn; var sg = zufall([1, -1]); if (sg < 0 && p > q){ var h = p; p = q; q = h; }
              var r = x0 / p + sg * x0 / q; if (r === 0) continue;
              tex = '\\dfrac{x}{' + p + '} ' + (sg > 0 ? '+' : '-') + ' \\dfrac{x}{' + q + '} = ' + r; k = [p, q, sg];
              f = function(x){ return [bAdd(bDiv(x, B(p)), bMul(B(sg), bDiv(x, B(q)))), B(r)]; };
              return { art: art, k: k.concat([r]), x: B(x0), f: f, tex: tex, hn: hn, muster: '\\(L = \\) {L}', text: 'Löse: \\(' + tex + '\\)' }; }
            if (art === 'kl'){ var a = nz(-6, 6), b = nz(-6, 6); x0 = zufallG(-10, 15);
              if ((x0 + a) % p || (x0 + b) % q) continue; var r2 = (x0 + a) / p - (x0 + b) / q;
              tex = '\\dfrac{' + pTex(lin(1, a)) + '}{' + p + '} - \\dfrac{' + pTex(lin(1, b)) + '}{' + q + '} = ' + r2; k = [p, q, a, b, r2];
              f = function(x){ return [bSub(bDiv(bAdd(x, B(a)), B(p)), bDiv(bAdd(x, B(b)), B(q))), B(r2)]; };
              return { art: art, k: k, x: B(x0), f: f, tex: tex, hn: hn, muster: '\\(L = \\) {L}', text: 'Löse: \\(' + tex + '\\)' }; }
            var a3 = nz(-6, 6), b3 = nz(-6, 6), z = p * b3 - q * a3; if (z % (q - p)) continue; x0 = z / (q - p);
            tex = '\\dfrac{' + pTex(lin(1, a3)) + '}{' + p + '} = \\dfrac{' + pTex(lin(1, b3)) + '}{' + q + '}'; k = [p, q, a3, b3];
            f = function(x){ return [bDiv(bAdd(x, B(a3)), B(p)), bDiv(bAdd(x, B(b3)), B(q))]; };
            return { art: art, k: k, x: B(x0), f: f, tex: tex, hn: hn, muster: '\\(L = \\) {L}', text: 'Löse: \\(' + tex + '\\)' };
          }
          return TYPEN.bruchgleichung.neu(); },
        richtig: function(A, e){ return e.L.art === 'zahl' && bEq(e.L.w, A.x); },
        fehlerwerte: function(A){
          var f = [], p = A.k[0], q = A.k[1], hn = A.hn;
          if (A.art === 'xx'){ var c = hn / p + A.k[2] * hn / q; if (c) f.push([B(A.k[3], c), 'rechts']); }
          if (A.art === 'kl'){ var a = A.k[2], b = A.k[3], r = A.k[4], c1 = hn / p - hn / q;
            if (c1){ f.push([B(hn * r - (hn / p) * a - (hn / q) * b, c1), 'Minus']); f.push([B(r - (hn / p) * a + (hn / q) * b, c1), 'rechts']); } }
          return f.filter(function(p2, i){ return !bEq(p2[0], A.x) && !f.slice(0, i).some(function(q2){ return bEq(q2[0], p2[0]); }); }); },
        fehler: function(A){ return TYPEN.bruchgleichung.fehlerwerte(A).map(function(p){ return [{ L: bTxt(p[0]).replace('−', '-') }, p[1]]; }).concat([[{ L: String(bZahl(A.x) + 1) }, 'Probe']]); },
        pruefen: function(A, e){
          if (e.L.art !== 'zahl') return 'Diese Gleichung hat <b>genau eine</b> Lösung.';
          var w = A.f(e.L.w), probe = '<b>Probe</b> mit \\(x = ' + bTex(e.L.w) + '\\): links \\(' + bTex(w[0]) + '\\), rechts \\(' + bTex(w[1]) + '\\). ';
          var f = TYPEN.bruchgleichung.fehlerwerte(A);
          for (var j = 0; j < f.length; j++) if (bEq(e.L.w, f[j][0]))
            return probe + (f[j][1] === 'rechts' ? 'Multipliziere <b>beide Seiten</b> mit \\(' + A.hn + '\\), auch die rechte.' : 'Setz den Zähler in Klammern: Das <b>Minus</b> vor dem Bruch gilt für den ganzen Zähler.');
          return probe + 'Multipliziere zuerst beide Seiten mit dem Hauptnenner \\(' + A.hn + '\\), mit Klammern um jeden Zähler.'; },
        tipps: function(A){ return ['Mach die Gleichung bruchfrei: beide Seiten mal den Hauptnenner \\(' + A.hn + '\\).', 'Setz jeden Zähler in Klammern, bevor du ihn multiplizierst.']; },
        loesung: function(A){
          var p = A.k[0], q = A.k[1], hn = A.hn, m;
          if (A.art === 'xx') m = (hn / p) + 'x ' + (A.k[2] > 0 ? '+ ' : '- ') + (hn / q) + 'x = ' + hn * A.k[3];
          else if (A.art === 'kl') m = (hn / p) + '(' + pTex(lin(1, A.k[2])) + ') - ' + (hn / q) + '(' + pTex(lin(1, A.k[3])) + ') = ' + hn * A.k[4];
          else m = q + '(' + pTex(lin(1, A.k[2])) + ') = ' + p + '(' + pTex(lin(1, A.k[3])) + ')';
          return A.tex + ' \\quad | \\cdot ' + hn + ' \\;\\Rightarrow\\; ' + m + ' \\;\\Rightarrow\\; L = \\{' + bTex(A.x) + '\\}'; } },

      /* ── Kapitel 4 ── */
      'umstellen': { felder: ['f'],
        schl: function(A){ return 'um|' + (A.F.id === 'lin' ? 'lin|' + A.F.k.join('|') + '|' : '') + A.F.g + '|' + A.F.z; },
        eingabe: function(A){ return { f: A.F.l }; },
        neu: function(){
          if (Math.random() < 0.35){                       // lineare Formel mit Zahlen: K = g + k·n
            var g = zufallG(2, 30), k = zufallG(2, 9), n = zufall(['n', 't', 'm']), K = zufall(['K', 'P', 'y']);
            var F = { id: 'lin', tex: K + ' = ' + g + ' + ' + k + ' \\cdot ' + n, g: K + n, z: n, l: '(' + K + '-' + g + ')/' + k, lt: '\\dfrac{' + K + ' - ' + g + '}{' + k + '}',
              fn: function(w){ return (w[K] - g) / k; }, f: [[function(w){ return w[K] / k - g; }, 'Reihenfolge'], [function(w){ return (w[K] + g) / k; }, 'Vorzeichen'], [function(w){ return w[K] - g / k; }, 'Reihenfolge']], k: [g, k] };
            return { F: F, muster: '\\(' + n + ' = \\) {f}', text: 'Stelle \\(' + F.tex + '\\) nach \\(' + n + '\\) um.' };
          }
          var F2 = zufall(FORMELN);
          return { F: F2, muster: '\\(' + F2.z + ' = \\) {f}', text: 'Stelle \\(' + F2.tex + '\\) nach \\(' + F2.z + '\\) um.' }; },
        form: function(A, r){ return enthaelt(r.baum, A.F.z) ? 'Die gesuchte Grösse \\(' + A.F.z + '\\) darf rechts nicht mehr vorkommen.' : null; },
        richtig: function(A, e){ return formelGleich(e.f.baum, A.F.fn, A.F.g.replace(A.F.z, '')); },
        fehler: function(A){
          var bsp = { 'Umkehrung': null };
          return A.F.f.map(function(p){ return [{ f: TYPEN.umstellen.falschText(A, p[0]) }, null]; }).filter(function(p){ return p[0].f; }); },
        falschText: function(A, fn){                        // für den Test: einen falschen Term in Textform finden
          var kand = ['F*a', 'a/F', 'E/g*h', 'E-g*h', 'P*I', 'I/P', 'A*h/2', 'A/(2h)', '2A*h', 'M/2-a', '2(M-a)', '2M+a', 'U-a+b', 'U+a+b', 'V/b*h', 'V-b*h',
            'Z*p/100', 'Z/(100p)', '2A/(h-c)', '(2A-c)/h', '2A/h+c', 'y+m*x', 'y/(m*x)', 'y/x-q', '(y+q)/x', 'F*m', 'm/F'];
          var namen = A.F.g.replace(A.F.z, '');
          if (A.F.id === 'lin'){ var K = A.F.g[0], n = A.F.z, g = A.F.k[0], k = A.F.k[1]; kand = [K + '/' + k + '-' + g, '(' + K + '+' + g + ')/' + k, K + '-' + g + '/' + k]; }
          for (var i = 0; i < kand.length; i++){
            var r = termLesen(kand[i], namen); if (r.kaputt) continue;
            if (formelGleich(r.baum, fn, namen) && !formelGleich(r.baum, A.F.fn, namen)) return kand[i];
          }
          return null; },
        pruefen: function(A, e){
          var namen = A.F.g.replace(A.F.z, '');
          for (var j = 0; j < A.F.f.length; j++) if (formelGleich(e.f.baum, A.F.f[j][0], namen)){
            var a = A.F.f[j][1];
            return a === 'Umkehrung' ? 'Mach rückwärts das <b>Gegenteil</b>: Aus «mal» wird «durch», aus «durch» wird «mal». Prüfe mit Zahlen.'
                 : a === 'Reihenfolge' ? 'Die <b>Reihenfolge</b> rückwärts: Was zuletzt gerechnet wurde, machst du zuerst rückgängig. Setz Klammern.'
                 : a === 'Klammer' ? 'Teile durch das <b>ganze</b> Produkt: Klammer um den Nenner.'
                 : 'Beim Hinüberbringen wechselt das <b>Vorzeichen</b>.';
          }
          return 'Setz Zahlen ein und prüfe: Stimmt deine Formel mit der ursprünglichen überein? Rückwärts in umgekehrter Reihenfolge rechnen.'; },
        tipps: function(A){ return ['Rechne rückwärts: Was mit \\(' + A.F.z + '\\) zuletzt passiert, machst du zuerst rückgängig.', 'Ergebnis-Form: \\(' + A.F.z + ' = \\ldots\\) ohne \\(' + A.F.z + '\\) auf der rechten Seite.']; },
        loesung: function(A){ return A.F.tex + ' \\;\\Rightarrow\\; ' + A.F.z + ' = ' + A.F.lt; } },

      'formelwert': { felder: ['z'],
        schl: function(A){ return 'fw|' + A.art + '|' + A.k.join('|'); },
        eingabe: function(A){ return { z: bWert(A.w).replace('−', '-') }; },
        neu: function(){
          var art = zufall(['taxi', 'temp', 'ohm', 'weg', 'rechteck', 'treppe']), w, k, text, fn, einheit, falsch;
          if (art === 'taxi'){ var g = zufall([4, 5, 6, 8]), kk = zufall([2, 2.5, 3, 3.5]), s = zufallG(3, 20), P0 = g + kk * s;
            k = [g, kk, s]; w = B(s); einheit = 'km';
            text = 'Taxi: \\(P = ' + g + ' + ' + kk + ' \\cdot s\\) (\\(P\\) in Fr., \\(s\\) in km). Wie weit kommt man für \\(P = ' + P0 + '\\) Fr.?';
            fn = function(x){ return bAdd(B(g), bMul(bDez(kk), x)); }; falsch = [[bSub(bDiv(bDez(P0), bDez(kk)), B(g)), 'Reihenfolge'], [bDiv(bAdd(bDez(P0), B(g)), bDez(kk)), 'Vorzeichen']];
            return { art: art, k: k, w: w, text: text, fn: fn, einheit: einheit, falsch: falsch, gr: 's', ziel: P0, muster: '\\(s = \\) {z} km' }; }
          if (art === 'temp'){ var C = 5 * zufallG(-4, 8), F = 9 * C / 5 + 32; k = [C]; w = B(C);
            text = 'Temperatur: \\(F = 1.8 \\cdot C + 32\\) (\\(F\\) in °F, \\(C\\) in °C). Wie viele °C sind \\(' + F + '\\) °F?';
            fn = function(x){ return bAdd(bMul(B(9, 5), x), B(32)); }; falsch = [[bSub(bDiv(B(F), B(9, 5)), B(32)), 'Reihenfolge'], [bDiv(B(F + 32), B(9, 5)), 'Vorzeichen']];
            return { art: art, k: k, w: w, text: text, fn: fn, falsch: falsch, gr: 'C', ziel: F, muster: '\\(C = \\) {z} °C' }; }
          if (art === 'ohm'){ var Rr = zufall([10, 20, 40, 50, 100]), I = zufall([0.2, 0.5, 1.5, 2, 3]), U = +(Rr * I).toFixed(4); k = [Rr, I]; w = bDez(I);
            text = 'Strom: \\(U = R \\cdot I\\). Bei \\(U = ' + U + '\\) V und \\(R = ' + Rr + '\\) Ω: Wie gross ist \\(I\\)?';
            fn = function(x){ return bMul(B(Rr), x); }; falsch = [[B(U * Rr), 'Umkehrung'], [B(Rr, U), 'Umkehrung']];
            return { art: art, k: k, w: w, text: text, fn: fn, falsch: falsch, gr: 'I', ziel: U, muster: '\\(I = \\) {z} A' }; }
          if (art === 'weg'){ var v = zufall([40, 50, 60, 80, 90, 120]), t = zufall([0.5, 1.5, 2, 2.5, 3]), s2 = v * t; k = [v, t]; w = bDez(t);
            text = 'Fahrt: \\(s = v \\cdot t\\). Wie lange dauert eine Fahrt von \\(' + s2 + '\\) km mit \\(' + v + '\\) km/h?';
            fn = function(x){ return bMul(B(v), x); }; falsch = [[B(s2 * v), 'Umkehrung'], [B(v, s2), 'Umkehrung']];
            return { art: art, k: k, w: w, text: text, fn: fn, falsch: falsch, gr: 't', ziel: s2, muster: '\\(t = \\) {z} h' }; }
          if (art === 'rechteck'){ var l = zufallG(4, 15), b = zufallG(2, 12), u = 2 * (l + b); k = [l, b]; w = B(b);
            text = 'Rechteck: \\(u = 2(l + b)\\). Wie breit ist ein Rechteck mit \\(u = ' + u + '\\) cm und \\(l = ' + l + '\\) cm?';
            fn = function(x){ return bMul(B(2), bAdd(B(l), x)); }; falsch = [[B(u - 2 * l), 'Reihenfolge'], [B(u - l, 2), 'Reihenfolge']];
            return { art: art, k: k, w: w, text: text, fn: fn, falsch: falsch, gr: 'b', ziel: u, muster: '\\(b = \\) {z} cm' }; }
          var a = zufall([23, 27, 29, 31, 33]), h = (63 - a) / 2; k = ['a', a]; w = B(h);
          text = 'Treppe: Schrittmassregel \\(2h + a = 63\\) (cm). Wie hoch ist eine Stufe mit der Auftrittsbreite \\(a = ' + a + '\\) cm?';
          fn = function(x){ return bAdd(bMul(B(2), x), B(a)); }; falsch = [[B(63 - a * 2), 'Reihenfolge'], [B(63 + a, 2), 'Vorzeichen'], [B(63, 2).map(function(c){ return c; }), null]];
          return { art: 'treppe', k: k, w: w, text: text, fn: fn, falsch: falsch.slice(0, 2), gr: 'h', ziel: 63, muster: '\\(h = \\) {z} cm' }; },
        richtig: function(A, e){ return bEq(e.z, A.w); },
        fehler: function(A){ return A.falsch.filter(function(p){ return !bEq(p[0], A.w); }).map(function(p){ return [{ z: bWert(p[0]).replace('−', '-') }, 'Probe']; }); },
        pruefen: function(A, e){
          var x = A.fn(e.z);
          return '<b>Probe</b>: Mit \\(' + A.gr + ' = ' + bWertTex(e.z) + '\\) gibt die Formel \\(' + bWertTex(x) + '\\), verlangt ist \\(' + A.ziel + '\\). Stelle zuerst nach \\(' + A.gr + '\\) um, dann setz ein.'; },
        tipps: function(A){ return ['Stelle die Formel zuerst nach \\(' + A.gr + '\\) um, dann setz die Zahlen ein.', 'Rückwärts rechnen: Was zuletzt gerechnet wird, machst du zuerst rückgängig.']; },
        loesung: function(A){ return A.gr + ' = ' + bWertTex(A.w); } }
    };
    /* Rohe Eingaben (Text oder Zahl) selbst einlesen — so kann ein Prüfwerkzeug pruefen() direkt mit den Werten aus
       fehler() aufrufen (.claude/tools/pruef-formelsatz.mjs). */
    function einlesen(A, e){
      var aus = {};
      for (var f in e){
        var w = e[f];
        if (w && typeof w === 'object'){ aus[f] = w; continue; }
        if (f === 't' || f === 'f') aus[f] = termLesen(String(w), f === 't' ? 'x' : A.F.g, f === 'f' ? A.F.z : null);
        else if (f === 'L') aus[f] = mengeLesen(String(w));
        else aus[f] = zahlLesen(String(w)).w;
      }
      return aus;
    }
    Object.keys(TYPEN).forEach(function(n){ var T = TYPEN[n], roh = T.pruefen; T.pruefen = function(A, e){ return roh(A, einlesen(A, e)); }; });
    window.__TYPEN = TYPEN; window.__SPERRE = SPERRE; window.__gesperrt = gesperrt;
    window.__term = { termLesen: termLesen, gemeinsam: gemeinsam, einBruch: einBruch, rEq: rEq, mengeLesen: mengeLesen, zahlLesen: zahlLesen };

    ALLE.forEach(function(box){
      var T = TYPEN[box.dataset.typ]; if (!T) return;
      var A, serie = 0, versuche = 0, geloest = false, stufe = 0;
      var auf = box.querySelector('.ue-aufgabe'), ein = box.querySelector('.ue-eingabe'), rueck = box.querySelector('.ue-rueck'),
          zaehler = box.querySelector('.ue-serie'), tippK = box.querySelector('.ue-tipp'), tippBox = box.querySelector('.ue-tipps');
      function neu(){
        A = T.neu();
        for (var v = 0; v < 60 && gesperrt(T, A); v++) A = T.neu();
        versuche = 0; geloest = false; stufe = 0; box.__aufgabe = A; box.__typ = T;   // Testhaken (.claude/tools/pruef-uebungen.mjs)
        auf.innerHTML = A.text;
        var html = A.muster;
        T.felder.forEach(function(f){
          var platz = f === 't' ? 'z. B. (x-3)/(x+3)' : f === 'f' ? 'z. B. (P-6)/2' : f === 'L' ? 'z. B. 4, 7/3, {} oder Q' : 'Zahl';
          html = html.replace('{' + f + '}', '<input type="text" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="' + (f === 't' || f === 'f' ? 'Term' : f === 'L' ? 'Lösungsmenge' : 'Zahl') + '" data-f="' + f + '" class="' + (f === 't' || f === 'f' || f === 'L' ? 'term' : '') + '" placeholder="' + platz + '">');
        });
        ein.innerHTML = html; rueck.className = 'ue-rueck'; rueck.innerHTML = '';
        tippBox.innerHTML = ''; tippK.textContent = '💡 Tipp'; tippK.disabled = false;
        setzen(auf); setzen(ein);
      }
      function tipp(){
        var t = T.tipps(A);
        if (stufe < t.length) tippBox.innerHTML += '<p class="ue-stufe"><b>' + (stufe === 0 ? 'Impuls' : 'Nächster Schritt') + ':</b> ' + t[stufe] + '</p>';
        else tippBox.innerHTML += '<p class="ue-stufe"><b>Lösungsweg:</b> \\(' + T.loesung(A) + '\\)</p>';
        stufe++;
        if (stufe > t.length){ tippK.disabled = true; tippK.textContent = '💡 alle Tipps'; } else tippK.textContent = '💡 Tipp ' + (stufe + 1) + '/' + (t.length + 1);
        setzen(tippBox);
      }
      function hinweis(h){ rueck.className = 'ue-rueck hinweis'; rueck.innerHTML = h; setzen(rueck); }
      function pruefen(){
        if (geloest) return;
        var e = {}, felder = ein.querySelectorAll('input');
        for (var i = 0; i < felder.length; i++){
          var inp = felder[i], f = inp.dataset.f, roh = inp.value.trim();
          inp.classList.remove('falsch');
          if (!roh) return hinweis('Fülle das Feld aus.');
          if (f === 't' || f === 'f'){
            var r = termLesen(roh, f === 't' ? 'x' : A.F.g, f === 'f' ? A.F.z : null);
            if (r.kaputt){ inp.classList.add('falsch'); return hinweis(r.grund); }
            e[f] = r;
          } else if (f === 'L'){
            var m = mengeLesen(roh);
            if (m.kaputt){ inp.classList.add('falsch'); return hinweis(m.kaputt); }
            e.L = m;
          } else {
            var z = zahlLesen(roh);
            if (z.kaputt){ inp.classList.add('falsch'); return hinweis(z.kaputt); }
            e[f] = z.w;
          }
        }
        var gleichwertig = T.richtig ? T.richtig(A, e) : rEq(e.t.r, A.r);
        if (gleichwertig && T.form){
          var h = T.form(A, e.t || e.f);
          if (h){ versuche++; return hinweis(h); }
        }
        versuche++;
        if (gleichwertig){
          serie = versuche === 1 && stufe === 0 ? serie + 1 : 0; geloest = true;
          rueck.className = 'ue-rueck richtig';
          rueck.innerHTML = '✓ Richtig <button type="button" class="ue-weiter">Nächste</button>';
          rueck.querySelector('.ue-weiter').addEventListener('click', neu);
        } else {
          serie = 0; rueck.className = 'ue-rueck falsch';
          rueck.innerHTML = T.pruefen(A, e) + (versuche >= 2 ? ' <details class="ue-loes"><summary>Lösung</summary>\\(' + T.loesung(A) + '\\)</details>' : '');
        }
        zaehler.textContent = serie + ' in Folge' + (serie >= 3 ? ' ✓' : '');
        setzen(rueck);
      }
      box.querySelector('.ue-pruefen').addEventListener('click', pruefen);
      box.querySelector('.ue-neu').addEventListener('click', neu);
      tippK.addEventListener('click', tipp);
      ein.addEventListener('keydown', function(ev){ if (ev.key === 'Enter') pruefen(); });
      neu();
    });
  })();
})();
</script>
