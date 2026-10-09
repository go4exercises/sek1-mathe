<script>
/* Leitprogramm Terme und Faktorisieren — Termkacheln (Sim 1), Flächenmodell und Rechteckschema (Sim 2),
   binomische Formeln am Quadrat (Sim 3), Faktorisierer (Sim 4), Übungen mit Rückmeldung, Minibilder.
   Polynome in einer Variablen als Liste ganzer Koeffizienten [c0, c1, c2, …]. Eingaben werden geparst
   (3x^2, 3x², 3·x·x, (x−3)(x+4), −(…)), gleichwertig geprüft, und getrennt davon: «zusammengefasst»
   (Ausmultiplizieren) und «Produktform, vollständig faktorisiert» (Faktorisieren).
   Farben: x² und x-Kacheln blau, Zahlen orange, negative Kacheln rot, Ergebnis grün. */
(function(){
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  function el(eltern, name, attr, text){
    var e = document.createElementNS(NS, name);
    for (var k in attr) e.setAttribute(k, attr[k]);
    if (text != null) e.textContent = text;
    eltern.appendChild(e); return e;
  }
  function setzen(e){ if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([e]).catch(function(){}); }
  function zufall(l){ return l[Math.floor(Math.random() * l.length)]; }
  function zufallG(a, b){ return a + Math.floor(Math.random() * (b - a + 1)); }
  function ggT(a, b){ a = Math.abs(a); b = Math.abs(b); while (b){ var t = a % b; a = b; b = t; } return a; }
  function mz(n){ return (n < 0 ? '−' : '') + Math.abs(n); }

  /* ---------- Polynome ---------- */
  function P(c){ c = (c || []).slice(); while (c.length > 1 && !c[c.length - 1]) c.pop(); return c.length ? c : [0]; }
  function pAdd(p, q){ var r = []; for (var i = 0; i < Math.max(p.length, q.length); i++) r[i] = (p[i] || 0) + (q[i] || 0); return P(r); }
  function pNeg(p){ return P(p.map(function(c){ return -c; })); }
  function pMul(p, q){ var r = []; for (var i = 0; i < p.length; i++) for (var j = 0; j < q.length; j++) r[i + j] = (r[i + j] || 0) + p[i] * q[j]; return P(r); }
  function pPow(p, n){ var r = [1]; for (var i = 0; i < n; i++) r = pMul(r, p); return r; }
  function pEq(p, q){ p = P(p); q = P(q); return p.length === q.length && p.every(function(c, i){ return c === q[i]; }); }
  function lin(a, b){ return P([b, a]); }                              // a·v + b
  function pInhalt(p){ return p.reduce(function(g, c){ return ggT(g, c); }, 0); }
  /* LaTeX eines Polynoms, absteigend: 3x^2 - 2x + 1 */
  function pTex(p, v){
    v = v || 'x'; p = P(p); var s = '';
    for (var i = p.length - 1; i >= 0; i--){
      var c = p[i]; if (!c) continue;
      var a = Math.abs(c), teil = i === 0 ? String(a) : (a === 1 ? '' : a) + v + (i > 1 ? '^' + i : '');
      s += s ? (c < 0 ? ' - ' : ' + ') + teil : (c < 0 ? '-' : '') + teil;
    }
    return s || '0';
  }
  /* So tippt man es ein: 3x^2-2x+1 */
  function pTxt(p, v){ return pTex(p, v).replace(/ /g, ''); }
  /* Lineare Klammer (a·v + b) als LaTeX, mit Klammern */
  function kl(a, b, v){ return '(' + pTex(lin(a, b), v) + ')'; }

  /* ---------- Termeingabe lesen ----------
     Baum: {t:'n', w} Zahl · {t:'v'} Variable · {t:'+'|'*', a:[…]} · {t:'neg', x} · {t:'^', x, e} · {t:'()', x}.
     Erlaubt: Ziffern, eine Variable, + − · * × ^ ² ³, Klammern, unsichtbares Mal (3x, 2(x+1), (x+1)(x−1)). */
  function termLesen(s, v){
    s = String(s == null ? '' : s).trim();
    if (!s) return { leer: true };
    s = s.replace(/[\u2212\u2013]/g, '-').replace(/[·×\u22c5]/g, '*').split(v.toUpperCase()).join(v).replace(/²/g, '^2').replace(/³/g, '^3').replace(/\s+/g, '');
    if (/\d,\d/.test(s)) return { kaputt: true, grund: 'Dezimalzahlen braucht es hier nicht.' };
    if (new RegExp(v + '\\d').test(s)) return { kaputt: true, grund: 'Hochzahlen mit <code>^</code> schreiben: <code>' + v + '^2</code> (oder ' + v + '²).' };
    var fremd = s.replace(/[0-9+\-*^()]/g, '').replace(new RegExp(v, 'g'), '');
    if (fremd) return { kaputt: true, grund: /[a-z]/i.test(fremd) ? 'Die Variable heisst hier \\(' + v + '\\).' : 'Zeichen «' + fremd[0] + '» verstehe ich nicht.' };
    var i = 0;
    function peek(){ return s[i]; }
    function summe(){
      var glieder = [], vz = 1;
      if (peek() === '+' || peek() === '-'){ vz = peek() === '-' ? -1 : 1; i++; }
      var g = produkt(); glieder.push(vz < 0 ? { t: 'neg', x: g } : g);
      while (peek() === '+' || peek() === '-'){
        var m = peek() === '-'; i++;
        g = produkt(); glieder.push(m ? { t: 'neg', x: g } : g);
      }
      return glieder.length === 1 ? glieder[0] : { t: '+', a: glieder };
    }
    function produkt(){
      var f = [potenz()];
      while (i < s.length && (peek() === '*' || peek() === '(' || /[0-9]/.test(peek()) || peek() === v)){
        if (peek() === '*') i++;
        f.push(potenz());
      }
      return f.length === 1 ? f[0] : { t: '*', a: f };
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
      if (c === v){ i++; return { t: 'v' }; }
      var m = s.slice(i).match(/^\d+/); if (m){ i += m[0].length; return { t: 'n', w: +m[0] }; }
      throw 'zeichen';
    }
    try {
      var baum = summe();
      if (i !== s.length) throw 'rest';
      return { baum: baum, p: wert(baum) };
    } catch (e){
      return { kaputt: true, grund: e === 'klammer' ? 'Eine Klammer ist nicht geschlossen.' : 'Schreib den Term zum Beispiel so: <code>3' + v + '^2 - 2' + v + ' + 1</code> oder <code>(' + v + '-3)(' + v + '+4)</code>.' };
    }
  }
  function wert(k){
    if (k.t === 'n') return [k.w];
    if (k.t === 'v') return [0, 1];
    if (k.t === '()') return wert(k.x);
    if (k.t === 'neg') return pNeg(wert(k.x));
    if (k.t === '^') return pPow(wert(k.x), k.e);
    if (k.t === '+') return k.a.reduce(function(r, g){ return pAdd(r, wert(g)); }, [0]);
    return k.a.reduce(function(r, g){ return pMul(r, wert(g)); }, [1]);
  }
  function ohneKl(k){ while (k.t === '()') k = k.x; return k; }
  /* Zusammengefasst: eine Summe von Monomen (Zahl, Variable, Potenzen, Produkte daraus), jeder Grad höchstens einmal. */
  function zusammengefasst(k){
    var grade = {}, ok = true;
    function monom(m){
      if (m.t === 'n' || m.t === 'v') return true;
      if (m.t === '^') return m.x.t === 'v';
      if (m.t === '*'){                       // 3x, 3x^2, x·3 — aber nicht 2·3x oder x·x (noch zusammenzufassen)
        var zahlen = 0, var_ = 0;
        return m.a.every(function(f){ if (f.t === 'n') zahlen++; else if (f.t === 'v' || (f.t === '^' && f.x.t === 'v')) var_++; else return false; return true; })
               && zahlen <= 1 && var_ <= 1;
      }
      return false;
    }
    function glied(g){
      if (g.t === 'neg') g = g.x;
      if (!monom(g)){ ok = false; return; }
      var d = wert(g).length - 1;
      if (grade[d]) ok = false; grade[d] = true;
    }
    k = ohneKl(k);
    (k.t === '+' ? k.a : [k]).forEach(glied);
    return ok;
  }
  /* Faktoren eines Produkts (Klammern und Vorzeichen weg); null, wenn die Wurzel kein Produkt ist. */
  function faktoren(k){
    k = ohneKl(k);
    if (k.t === 'neg') return faktoren(k.x);
    if (k.t === '^'){ var f = []; for (var j = 0; j < k.e; j++) f.push(k.x); return f.map(ohneKl); }
    if (k.t === '*'){ var out = []; k.a.forEach(function(g){ var f2 = faktoren(g); out = out.concat(f2 || [ohneKl(g)]); }); return out; }
    return null;
  }
  /* Ganzzahlig weiter zerlegbar? Inhalt > 1, gemeinsames v (Zahlglied 0 bei Grad ≥ 2), oder Quadratik mit ganzen Nullstellen. */
  function zerlegbar(p){
    p = P(p); var d = p.length - 1;
    if (d < 1) return false;
    if (pInhalt(p) > 1 && d >= 1 && p.filter(function(c){ return c; }).length > 1) return 'inhalt';
    if (d >= 2 && p[0] === 0) return 'variable';
    if (d === 2){
      var D = p[1] * p[1] - 4 * p[2] * p[0];
      if (D >= 0 && Math.round(Math.sqrt(D)) ** 2 === D) return 'quadratik';
    }
    return false;
  }
  /* Produktform-Befund: 'summe' (keine Produktform), 'unvollstaendig' (+ welcher Faktor), oder null (fertig). */
  function produktBefund(lese){
    var f = faktoren(lese.baum);
    if (!f || f.filter(function(g){ return wert(g).length > 1; }).length === 0) return { art: 'summe' };
    var zahl = 1;
    for (var j = 0; j < f.length; j++){
      var p = wert(f[j]);
      if (p.length === 1){ zahl *= p[0]; continue; }
      var z = zerlegbar(p);
      if (z) return { art: 'unvollstaendig', grund: z, p: p };
    }
    return null;
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

  /* ════════ Sim 1 — Termkacheln ════════
     Oben der Term der Aufgabe als Kacheln (x-Streifen blau, Einer orange, negative rot), Klammern als Rahmen —
     «3·( )» dreimal, «−( )» mit Minus davor. Unten baut man mit zwei Reglern den zusammengefassten Term a·x + b.
     Gleichwertig ist er, wenn beide Kachelsätze nach dem Wegheben der Nullpaare gleich sind; die Probe mit x = 2
     steht daneben. (Es gibt keine Themenseite: Diese Erkundung ist die einzige Darstellung im Lehrmittel.) */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    var S = null;
    function wertTerm(items){
      return items.reduce(function(r, it){
        if (it.gruppe) return pAdd(r, pMul([it.faktor], wertTerm(it.gruppe)));
        return pAdd(r, it.art === 'x' ? [0, it.k] : [it.k]);
      }, [0]);
    }
    function texTerm(items){
      var s = '';
      items.forEach(function(it, j){
        var t;
        if (it.gruppe){ t = (it.faktor === -1 ? '-' : it.faktor === 1 ? '' : it.faktor) + '(' + texTerm(it.gruppe) + ')'; }
        else t = it.art === 'x' ? (Math.abs(it.k) === 1 ? (it.k < 0 ? '-' : '') : it.k) + 'x' : String(it.k);
        if (j && t[0] !== '-') s += ' + ' + t; else if (j) s += ' - ' + t.slice(1); else s += t;
      });
      return s;
    }
    function zustand(){ return { a: wertR(fig, 's1-a'), b: wertR(fig, 's1-b'), p: S ? wertTerm(S) : [0] }; }
    function kacheln(g, items, x0, y0, neg){
      var x = x0;
      items.forEach(function(it){
        if (it.gruppe){
          var kopien = Math.abs(it.faktor);
          if (it.faktor < 0){ el(g, 'text', { x: x, y: y0 + 26, 'class': 'kl-vz' }, '−'); x += 12; }
          for (var c = 0; c < kopien; c++){
            var x1 = x; x += 4;
            x = kacheln(g, it.gruppe, x, y0 + 4, neg) + 4;
            el(g, 'rect', { x: x1, y: y0, width: x - x1, height: 48, rx: 6, 'class': 'kl-rahmen' + (it.faktor < 0 ? ' minus' : '') });
            x += 6;
          }
          return;
        }
        for (var j = 0; j < Math.abs(it.k); j++){
          var n = (it.k < 0) !== !!neg;
          if (it.art === 'x') el(g, 'rect', { x: x, y: y0 + 2, width: 9, height: 40, rx: 2, 'class': 'kachel ' + (n ? 'neg' : 'kx') });
          else el(g, 'rect', { x: x, y: y0 + 32, width: 9, height: 9, rx: 2, 'class': 'kachel ' + (n ? 'neg' : 'k1') });
          x += 11;
        }
        x += 8;
      });
      return x;
    }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's1-a'); zeigeWert(fig, 's1-b');
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      el(svg, 'text', { x: 10, y: 16, 'class': 'st-name' }, 'Term');
      if (S) kacheln(svg, S, 10, 24);
      el(svg, 'text', { x: 10, y: 100, 'class': 'st-name' }, 'dein Term');
      kacheln(svg, [{ art: 'x', k: Z.a }, { art: '1', k: Z.b }], 10, 108);
      var eigen = lin(Z.a, Z.b), gl = pEq(eigen, Z.p);
      if (gl) el(svg, 'rect', { x: 4, y: 104, width: 352, height: 56, rx: 8, 'class': 'treffer-rahmen' });
      var w = function(p){ return p.reduce(function(s, c, k){ return s + c * Math.pow(2, k); }, 0); };
      formel.innerHTML = 'dein Term: ' + hx(eigen) + (gl ? ' <span class="ok-text">gleichwertig</span>' : ' <span class="nein-text">noch nicht gleich</span>') +
        ' <span class="grau">(Probe mit x = 2: Term ' + mz(w(Z.p)) + '; dein Term ' + mz(w(eigen)) + ')</span>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    function A(items){ return function(){ S = items; }; }
    var aufg = [
      [{ art: 'x', k: 3 }, { art: '1', k: 2 }, { art: 'x', k: -1 }, { art: '1', k: 4 }],
      [{ art: 'x', k: 2 }, { art: '1', k: -5 }, { art: 'x', k: 4 }, { art: '1', k: 1 }],
      [{ gruppe: [{ art: 'x', k: 1 }, { art: '1', k: 2 }], faktor: 3 }],
      [{ gruppe: [{ art: 'x', k: 2 }, { art: '1', k: -1 }], faktor: 2 }, { art: 'x', k: 1 }],
      [{ art: 'x', k: 4 }, { gruppe: [{ art: 'x', k: 1 }, { art: '1', k: 3 }], faktor: -1 }]
    ];
    var hinweise = ['Fasse zusammen: Stell unten den kürzesten gleichwertigen Term ein.', 'Negative Kacheln heben positive auf (Nullpaare). Fasse zusammen.',
                    'Drei gleiche Klammern: Wie viele x-Kacheln, wie viele Einer sind es zusammen?', 'Zweimal die Klammer, dazu ein x. Fasse zusammen.',
                    'Das Minus gilt für die ganze Klammer — jede Kachel darin wird umgedreht. Fasse zusammen.'];
    pr = Leiste(fig, aufg.map(function(it, j){
      var ziel = (function(){ S = it; var p = zustand().p; S = null; return p; })();
      return { text: hinweise[j] + ' \\(' + texTerm(it) + '\\)', setup: A(it), ok: function(z){ return pEq(lin(z.a, z.b), ziel); } };
    }), sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    S = aufg[0]; zeichnen();
  })();

  /* ════════ Sim 2 — Klammer mal Klammer: Flächenmodell und Rechteckschema ════════
     (x + a)(x + b): Bei positiven a, b ist das Produkt ein Rechteck aus x² (blau), zwei x-Streifen (blau) und
     a·b Einerkacheln (orange). Das Rechteckschema darunter gilt für alle Vorzeichen. */
  function rechteckschema(tab, a, b, v){
    v = v || 'x';
    var z = function(n){ return (n < 0 ? '− ' : '+ ') + Math.abs(n); };
    var g = function(c){ return c === 0 ? '0' : (c < 0 ? '−' : '') + (Math.abs(c) === 1 ? '' : Math.abs(c)) + v; };
    tab.innerHTML = '<tr><th>·</th><th>' + v + '</th><th>' + z(b) + '</th></tr>' +
      '<tr><th>' + v + '</th><td class="t-q">' + v + '²</td><td class="t-x">' + g(b) + '</td></tr>' +
      '<tr><th>' + z(a) + '</th><td class="t-x">' + g(a) + '</td><td class="t-z">' + mz(a * b) + '</td></tr>';
  }
  function flaeche(svg, a, b, x0, y0, X){
    // X = Länge von x in px; Einheit 16 px. Nur für a, b ≥ 0.
    var E = 16;
    el(svg, 'rect', { x: x0, y: y0, width: X, height: X, 'class': 'fl-q' });
    for (var j = 0; j < b; j++) el(svg, 'rect', { x: x0 + X + j * E, y: y0, width: E, height: X, 'class': 'fl-x' });
    for (var k = 0; k < a; k++) el(svg, 'rect', { x: x0, y: y0 + X + k * E, width: X, height: E, 'class': 'fl-x' });
    for (j = 0; j < b; j++) for (k = 0; k < a; k++) el(svg, 'rect', { x: x0 + X + j * E, y: y0 + X + k * E, width: E, height: E, 'class': 'fl-1' });
    el(svg, 'rect', { x: x0, y: y0, width: X + b * E, height: X + a * E, 'class': 'rahmen' });
    el(svg, 'text', { x: x0 + X / 2, y: y0 - 6, 'class': 'st-name', 'text-anchor': 'middle' }, 'x');
    if (b) el(svg, 'text', { x: x0 + X + b * E / 2, y: y0 - 6, 'class': 'st-name', 'text-anchor': 'middle' }, String(b));
    el(svg, 'text', { x: x0 - 8, y: y0 + X / 2 + 4, 'class': 'st-name', 'text-anchor': 'end' }, 'x');
    if (a) el(svg, 'text', { x: x0 - 8, y: y0 + X + a * E / 2 + 4, 'class': 'st-name', 'text-anchor': 'end' }, String(a));
  }
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]'), tab = fig.querySelector('table');
    function zustand(){ return { a: wertR(fig, 's2-a'), b: wertR(fig, 's2-b') }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's2-a'); zeigeWert(fig, 's2-b');
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      if (Z.a >= 0 && Z.b >= 0) flaeche(svg, Z.a, Z.b, 40, 24, 110);
      else { el(svg, 'text', { x: 150, y: 100, 'text-anchor': 'middle', 'class': 'st-frage' }, 'Mit negativen Zahlen gibt es kein Rechteck.');
             el(svg, 'text', { x: 150, y: 120, 'text-anchor': 'middle', 'class': 'st-frage' }, 'Das Rechteckschema unten gilt immer.'); }
      rechteckschema(tab, Z.a, Z.b);
      var p = pMul(lin(1, Z.a), lin(1, Z.b));
      formel.innerHTML = '(x ' + (Z.a < 0 ? '− ' : '+ ') + Math.abs(Z.a) + ')(x ' + (Z.b < 0 ? '− ' : '+ ') + Math.abs(Z.b) + ') = ' + hx(p);
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    var paar = function(a, b){ return function(z){ return (z.a === a && z.b === b) || (z.a === b && z.b === a); }; };
    pr = Leiste(fig, [
      { text: 'Stell \\((x + 3)(x + 1)\\) ein. Zähle: Wie viele x-Streifen, wie viele Einerkacheln?', ok: paar(3, 1) },
      { text: 'Stell \\((x + 4)(x - 1)\\) ein. Welches Vorzeichen bekommt die Zahl am Schluss?', ok: paar(4, -1) },
      { text: 'Stell \\((x - 2)(x - 5)\\) ein. Warum ist die Zahl am Schluss positiv?', ok: paar(-2, -5) },
      { text: 'Finde ein Produkt, bei dem das x-Glied ganz wegfällt (und keine Zahl 0 ist).', ok: function(z){ return z.a === -z.b && z.a !== 0; } },
      { text: 'Finde die beiden Zahlen so, dass das Ergebnis \\(x^2 + 2x - 8\\) ist.', ok: paar(4, -2) }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 3 — Binomische Formeln am Quadrat ════════
     a und b sind Längen (Zahlen). (a+b)²: Quadrat mit a² (blau), zwei Rechtecken a·b (orange) und b² (grün).
     (a−b)²: im Quadrat a² bleibt nach dem Wegnehmen zweier Streifen a·b (rot gestrichelt) und Zurückgeben von b²
     das Quadrat (a−b)². (a+b)(a−b): das Rechteck hat dieselbe Fläche wie a² ohne b². */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]'), modus = fig.querySelector('select.sim-wahl');
    function korrigiere(){ var b = fig.querySelector('#s3-b'), a = wertR(fig, 's3-a'); b.max = Math.min(4, a - 1); if (+b.value > +b.max) b.value = b.max; }
    function zustand(){ return { m: modus.value, a: wertR(fig, 's3-a'), b: wertR(fig, 's3-b') }; }
    function zeichnen(){
      korrigiere();
      var Z = zustand(), a = Z.a, b = Z.b, E = 22, x0 = 40, y0 = 20;
      ['s3-a', 's3-b'].forEach(function(id){ zeigeWert(fig, id); });
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      var R = function(x, y, w, h, c){ el(svg, 'rect', { x: x0 + x * E, y: y0 + y * E, width: w * E, height: h * E, 'class': c }); };
      var L = function(name, w, breite){ return breite >= 3 ? name + ' = ' + w : String(w); };
      var T = function(x, y, t, c){ el(svg, 'text', { x: x0 + x * E, y: y0 + y * E + 4, 'text-anchor': 'middle', 'class': 'st-zahl' + (c ? ' ' + c : '') }, t); };
      if (Z.m === 'plus'){
        R(0, 0, a, a, 'fl-q'); R(a, 0, b, a, 'fl-x'); R(0, a, a, b, 'fl-x'); R(a, a, b, b, 'fl-1'); R(0, 0, a + b, a + b, 'rahmen');
        T(a / 2, a / 2, L('a²', a * a, a)); T(a + b / 2, a / 2, a * b); T(a / 2, a + b / 2, L('ab', a * b, a)); T(a + b / 2, a + b / 2, b * b);
        formel.innerHTML = '(' + a + ' + ' + b + ')² = ' + (a + b) * (a + b) + ' = ' + a * a + ' + 2 · ' + a * b + ' + ' + b * b +
          ' <span class="nein-text">≠ ' + a + '² + ' + b + '² = ' + (a * a + b * b) + '</span>';
      } else if (Z.m === 'minus'){
        R(0, 0, a, a, 'fl-leer'); R(0, 0, a - b, a - b, 'fl-q'); R(a - b, 0, b, a, 'fl-weg'); R(0, a - b, a, b, 'fl-weg'); R(a - b, a - b, b, b, 'fl-1');
        R(0, 0, a, a, 'rahmen');
        T((a - b) / 2, (a - b) / 2, L('(a−b)²', (a - b) * (a - b), a - b + 1)); T(a - b / 2, (a - b) / 2, a * b, 'grau-t'); T((a - b) / 2, a - b / 2, a * b, 'grau-t'); T(a - b / 2, a - b / 2, b * b);
        formel.innerHTML = '(' + a + ' − ' + b + ')² = ' + (a - b) * (a - b) + ' = ' + a * a + ' − 2 · ' + a * b + ' + ' + b * b +
          ' <span class="grau">(vom Quadrat a² zwei Streifen ab weg; das Eckquadrat b² war dabei doppelt weg, also einmal zurück)</span>';
      } else {
        var yo = a - b + 1;
        R(0, 0, a, a - b, 'fl-q'); R(a, 0, b, a - b, 'fl-x'); R(0, 0, a + b, a - b, 'rahmen');
        R(0, yo, a, a - b, 'fl-q'); R(0, yo + a - b, a - b, b, 'fl-x'); R(a - b, yo + a - b, b, b, 'fl-weg'); R(0, yo, a, a, 'rahmen duenn');
        T(a / 2, (a - b) / 2, L('(a+b)(a−b)', (a + b) * (a - b), a));
        T(a / 2, yo + (a - b) / 2, L('a² − b²', a * a - b * b, a));
        formel.innerHTML = '(' + a + ' + ' + b + ')(' + a + ' − ' + b + ') = ' + (a + b) * (a - b) + ' = ' + a * a + ' − ' + b * b +
          ' <span class="grau">(unten: a² ohne das Eckquadrat b²; das orange Stück wandert nach rechts, so entsteht das Rechteck oben)</span>';
      }
      svg.setAttribute('viewBox', '0 0 320 ' + (Z.m === 'produkt' ? 40 + (a - b + 1 + a) * E : 40 + (a + (Z.m === 'plus' ? b : 0)) * E));
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    function auf(m){ return function(){ modus.value = m; }; }
    pr = Leiste(fig, [
      { text: '«(a + b)²»: Stell \\(a = 5\\) und \\(b = 2\\) ein. Welche vier Teilflächen siehst du, und wie gross sind sie?', setup: auf('plus'),
        ok: function(z){ return z.m === 'plus' && z.a === 5 && z.b === 2; } },
      { text: 'Finde \\(a\\) und \\(b\\) mit \\((a + b)^2 = 64\\) und \\(a^2 + b^2 = 34\\). Wie gross ist der Unterschied?', setup: auf('plus'),
        ok: function(z){ return z.m === 'plus' && z.a === 5 && z.b === 3; } },
      { text: '«(a − b)²»: Bei \\(a = 7\\): Welches \\(b\\) gibt \\((a - b)^2 = 9\\)?', setup: auf('minus'),
        ok: function(z){ return z.m === 'minus' && z.a === 7 && z.b === 4; } },
      { text: '«(a + b)(a − b)»: Finde \\(a\\) und \\(b\\), sodass das Rechteck die Fläche \\(24\\) hat.', setup: auf('produkt'),
        ok: function(z){ return z.m === 'produkt' && z.a * z.a - z.b * z.b === 24; } }
    ], sim);
    fig.querySelectorAll('input, select').forEach(function(i){ i.addEventListener('input', zeichnen); i.addEventListener('change', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 4 — Faktorisierer: Zweiklammersatz ════════
     Ziel x² + px + q; mit zwei Reglern (x + m)(x + n) suchen. Das Rechteckschema zeigt, was herauskommt; daneben
     m · n und m + n. Unterschied zu Sim 2: Dort ist das Produkt gegeben, hier das Ergebnis. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var formel = fig.querySelector('[data-rolle="formel"]'), tab = fig.querySelector('table'), ziel = fig.querySelector('[data-rolle="ziel"]');
    var Q = [8, 6, 1];
    function zustand(){ return { m: wertR(fig, 's4-m'), n: wertR(fig, 's4-n') }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's4-m'); zeigeWert(fig, 's4-n');
      rechteckschema(tab, Z.m, Z.n);
      var p = pMul(lin(1, Z.m), lin(1, Z.n)), gl = pEq(p, Q);
      ziel.innerHTML = 'Ziel: ' + hx(Q) + ' <span class="grau">(Summe ' + mz(Q[1]) + '; Produkt ' + mz(Q[0]) + ')</span>';
      formel.innerHTML = 'dein Produkt: ' + hx(p) + ' <span class="grau">(Summe der Zahlen ' + mz(Z.m + Z.n) + '; Produkt ' + mz(Z.m * Z.n) + ')</span>' +
        (gl ? ' <span class="ok-text">✓ getroffen</span>' : '');
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    var ziele = [[8, 6, 1], [15, -8, 1], [-15, 2, 1], [9, -6, 1], [-16, 0, 1]];
    var texte = ['Faktorisiere: Produkt \\(8\\), Summe \\(6\\).', 'Produkt positiv, Summe negativ — welche Vorzeichen?', 'Produkt negativ: Die Zahlen haben verschiedene Vorzeichen.',
                 'Was fällt bei diesem Ergebnis auf?', 'Hier fehlt das x-Glied: Die Summe ist \\(0\\).'];
    pr = Leiste(fig, ziele.map(function(q, j){
      return { text: texte[j] + ' Ziel: \\(' + pTex(q) + '\\)', setup: function(){ Q = q; }, ok: function(z){ return pEq(pMul(lin(1, z.m), lin(1, z.n)), q); } };
    }), sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Übungen mit Rückmeldung ════════
     Termfelder (Name beginnt mit «t»): gleichwertig geprüft; bei Ausmultiplizieren muss das Ergebnis zusammengefasst
     sein, bei Faktorisieren in Produktform und vollständig. Beides ist ein eigener Hinweis und zählt als Versuch.
     Zahlenfelder: ganze Zahlen. Tipps in drei Stufen. Testhaken: box.__aufgabe, box.__typ. */
  (function(){
    var ALLE = document.querySelectorAll('.uebung[data-typ]'); if (!ALLE.length) return;
    function nz(a, b){ var r; do { r = zufallG(a, b); } while (!r); return r; }
    function kopfTerm(p, v){ return pTxt(p, v); }
    function kz(n){ return n < 0 ? '(' + n + ')' : String(n); }
    function vzTex(n){ return n < 0 ? '- ' + Math.abs(n) : '+ ' + n; }

    /* Feste Aufgaben (Erkundungen, Clips, Festhalten, Kapitelaufgaben, Vortest, Gesamttest): je Typ ein Schlüssel. */
    var SPERRE = [
      'bl|p|1|3', 'bl|p|1|6', 'bi|d|1|3', 'fz|d|1|5', 'kl|-2|3|-4', 'zs|1,4,-2,1', 'am|1,5|1,1', 'am|1,-2|1,7', 'ko|-2|7', 'ko|-2|4', 'fz|t|-2|4',
      'fz|k|3|b|1', 'fz|k|2|d|3', 'fz|k|5|d|2', 'fz|k|3|d|2', 'am|1,4|1,2',
      'zs|3,2,-1,4', 'zs|2,-5,4,1', 'zs|2,4,3,-1', 'zs|5,3,-2,7', 'zs|4,-7,2,3',
      'kl|3|1|2', 'kl|2|2|-1', 'kl|3|2|-4', 'kl|-2|1|-3', 'kl|4|3|-2', 'kl|-3|-1|2', 'kl|5|2|-3', 'km|7|2|-5', 'km|4|1|3', 'km|8|3|-5', 'km|1|-3|4', 'km|-1|3|-8',
      'am|1,2|1,3', 'am|3,-2|1,4', 'am|1,4|1,5', 'am|2,-3|1,6', 'am|1,-4|1,-7', 'am|1,5|1,-2', 'am|1,1|1,4', 'am|1,6|1,1', 'am|1,-3|1,5', 'am|2,1|1,-4', 'am|1,5|1,2', 'am|1,2|1,-1', 'am|2,5|1,-3',
      'ko|3|2', 'ko|1|3', 'ko|4|-1', 'ko|-2|-5', 'ko|4|-3', 'ko|2|3', 'ko|-3|5', 'ko|2|-1', 'ko|6|1', 'ko|5|2', 'ko|1|4', 'ko|3|-3',
      'bi|p|1|4', 'bi|m|2|3', 'bi|d|1|5', 'bi|p|1|6', 'bi|m|1|1', 'bi|m|3|2', 'bi|d|1|7', 'bi|d|1|4', 'bi|p|1|5', 'bi|p|1|9', 'bi|m|1|6', 'bi|d|2|5', 'bi|m|3|4', 'bi|p|1|3',
      'bl|p|1|4', 'bl|m|1|5', 'bl|p|1|7', 'bl|m|1|3', 'bl|p|1|5', 'bl|p|1|9', 'bl|m|1|6', 'bl|m|3|2', 'bl|m|2|3', 'bl|m|3|4', 'bl|m|1|1', 'bl|m|1|12',
      'ak|3|2|-3', 'ak|4|2|3', 'ak|5|1|-3', 'ak|7|2|-3', 'ak|6|2|3', 'ak|2|1|-9', 'ak|3|1|-4',
      'fz|t|2|3', 'fz|t|2|4', 'fz|t|-3|-5', 'fz|t|5|-3', 'fz|t|-3|-3', 'fz|t|4|-4', 'fz|t|-3|-4', 'fz|t|2|7', 'fz|t|-5|2', 'fz|t|-6|4', 'fz|t|4|-3', 'fz|t|-9|9',
      'fz|b|-5', 'fz|b|7', 'fz|b|5', 'fz|b|3', 'fz|b|-3', 'fz|d|3|5', 'fz|d|2|1', 'fz|d|1|9', 'fz|d|1|3', 'fz|d|1|2', 'fz|d|1|4'
    ];
    /* Schlüssel normieren: Zahlenpaare sortiert, Klammerpaare beim Ausmultiplizieren als Menge (Prüfung 10.10.2026:
       unsortierte Einträge sperrten nichts). */
    function norm(k){
      var p = k.split('|'), z = function(u, w){ return u - w; };
      if (p[0] === 'ko') return 'ko|' + [+p[1], +p[2]].sort(z).join('|');
      if (p[0] === 'fz' && p[1] === 't') return 'fz|t|' + [+p[2], +p[3]].sort(z).join('|');
      if (p[0] === 'am') return 'am|' + [p[1], p[2]].sort().join('|');
      return k;
    }
    SPERRE = SPERRE.map(norm);
    function gesperrt(T, A){ return !!T.schl && SPERRE.indexOf(norm(T.schl(A))) >= 0; }
    function paarSchl(m, n){ return [m, n].sort(function(u, w){ return u - w; }).join('|'); }

    var TYPEN = {
      /* ── Kapitel 1 ── */
      'zusammenfassen': { felder: ['t'],
        schl: function(A){ return 'zs|' + A.z.join(','); },
        eingabe: function(A){ return { t: kopfTerm(A.r) }; },
        neu: function(){
          var mitQ = Math.random() < 0.3, a = nz(-6, 7), b = nz(-9, 9), c = nz(-6, 7), d = nz(-9, 9);
          if (a + c === 0) c = c === -1 ? -2 : c + 1;
          var glieder = mitQ ? [[2, a], [1, b], [2, c], [1, d]] : [[1, a], [0, b], [1, c], [0, d]];
          var tex = '', r = [0];
          glieder.forEach(function(g, j){
            var t = pTex(g[0] === 0 ? [g[1]] : g[0] === 1 ? [0, g[1]] : [0, 0, g[1]]);
            tex += j === 0 ? t : (t[0] === '-' ? ' - ' + t.slice(1) : ' + ' + t);
            r = pAdd(r, g[0] === 0 ? [g[1]] : g[0] === 1 ? [0, g[1]] : [0, 0, g[1]]);
          });
          return { z: [a, b, c, d], q: mitQ, r: r, tex: tex, muster: '\\(' + tex + ' = \\) {t}', text: 'Fasse zusammen.' }; },
        falsche: function(A){
          var s = A.z.reduce(function(u, w){ return u + w; }, 0);
          var f = [[A.q ? [0, 0, s] : [0, s], 'gleichartige']];
          return f.filter(function(p){ return !pEq(p[0], A.r); }); },
        fehler: function(A){ return TYPEN.zusammenfassen.falsche(A).map(function(p){ return [{ t: kopfTerm(p[0]) }, p[1]]; }); },
        pruefen: function(A, e){
          var f = TYPEN.zusammenfassen.falsche(A);
          for (var j = 0; j < f.length; j++) if (pEq(e.t.p, f[j][0]))
            return 'Nur <b>gleichartige</b> Glieder zusammenfassen: ' + (A.q ? '\\(x^2\\)-Glieder mit \\(x^2\\)-Gliedern, \\(x\\)-Glieder mit \\(x\\)-Gliedern.' : '\\(x\\)-Glieder mit \\(x\\)-Gliedern, Zahlen mit Zahlen.');
          return 'Ordne zuerst: gleichartige Glieder untereinander, das Vorzeichen gehört zum Glied dahinter. Rechne nochmals nach.'; },
        tipps: function(A){ return ['Gleichartig sind Glieder mit derselben Variable und derselben Hochzahl.', A.q ? 'Sammle die \\(x^2\\)-Glieder und die \\(x\\)-Glieder getrennt.' : 'Sammle die \\(x\\)-Glieder und die Zahlen getrennt.']; },
        loesung: function(A){ return A.tex + ' = ' + pTex(A.r); } },

      'klammern': { felder: ['t'],
        schl: function(A){ return A.art === 'k' ? 'kl|' + A.k + '|' + A.a + '|' + A.b : 'km|' + A.m + '|' + A.a + '|' + A.b; },
        eingabe: function(A){ return { t: kopfTerm(A.r) }; },
        neu: function(){
          var art = Math.random() < 0.5 ? 'k' : 'm', a = nz(-4, 5), b = nz(-9, 9);
          if (art === 'k'){
            var k = zufall([-5, -4, -3, -2, 2, 3, 4, 5, 6]);
            return { art: art, k: k, a: a, b: b, r: pMul([k], lin(a, b)), tex: k + kl(a, b),
              muster: '\\(' + k + kl(a, b) + ' = \\) {t}', text: 'Löse die Klammer auf.' };
          }
          var m; do { m = nz(-6, 9); } while (m === a);
          return { art: art, m: m, a: a, b: b, r: pAdd([0, m], pNeg(lin(a, b))), tex: pTex([0, m]) + ' - ' + kl(a, b),
            muster: '\\(' + pTex([0, m]) + ' - ' + kl(a, b) + ' = \\) {t}', text: 'Löse die Klammer auf und fasse zusammen.' }; },
        falsche: function(A){
          var f = A.art === 'k' ? [[lin(A.k * A.a, A.b), 'jedem'], [lin(A.k * A.a, -A.k * A.b), 'Vorzeichen']]
                                : [[lin(A.m - A.a, A.b), 'Minus']];
          return f.filter(function(p){ return !pEq(p[0], A.r); }); },
        fehler: function(A){ return TYPEN.klammern.falsche(A).map(function(p){ return [{ t: kopfTerm(p[0]) }, p[1]]; }); },
        pruefen: function(A, e){
          var f = TYPEN.klammern.falsche(A);
          for (var j = 0; j < f.length; j++) if (pEq(e.t.p, f[j][0])){
            if (f[j][1] === 'jedem') return 'Die Zahl vor der Klammer wird mit <b>jedem</b> Glied in der Klammer multipliziert.';
            if (f[j][1] === 'Minus') return '<b>Minus</b> vor der Klammer dreht <b>jedes</b> Vorzeichen in der Klammer um, auch das zweite.';
            return '<b>Vorzeichen:</b> Rechne \\(' + kz(A.k) + ' \\cdot ' + kz(A.b) + '\\). Minus mal Minus gibt Plus, Minus mal Plus gibt Minus.';
          }
          return 'Klammer auflösen, dann gleichartige Glieder zusammenfassen. Rechne nochmals nach und mach die Probe mit \\(x = 2\\).'; },
        tipps: function(A){ return A.art === 'k' ? ['Distributivgesetz: \\(k(a + b) = ka + kb\\).', 'Rechne \\(' + kz(A.k) + ' \\cdot ' + (A.a < 0 ? '(' + pTex([0, A.a]) + ')' : pTex([0, A.a])) + '\\) und \\(' + kz(A.k) + ' \\cdot ' + kz(A.b) + '\\).']
                                                 : ['Minus vor der Klammer: Klammer weglassen und jedes Vorzeichen darin umdrehen.', '\\(-' + kl(A.a, A.b) + ' = ' + pTex(lin(-A.a, -A.b)) + '\\), dann zusammenfassen.']; },
        loesung: function(A){ return A.art === 'k' ? A.tex + ' = ' + pTex(A.r) : A.tex + ' = ' + pTex([0, A.m]) + (A.a > 0 ? ' - ' : ' + ') + pTex([0, Math.abs(A.a)]) + (A.b > 0 ? ' - ' : ' + ') + Math.abs(A.b) + ' = ' + pTex(A.r); } },

      /* ── Kapitel 2 ── */
      'ausmult': { felder: ['t'],
        schl: function(A){ return 'am|' + A.a + ',' + A.b + '|' + A.c + ',' + A.d; },
        eingabe: function(A){ return { t: kopfTerm(A.r) }; },
        neu: function(){
          var a = zufall([1, 1, 1, 2, 3]), c = zufall([1, 1, 2]), b = nz(-9, 9), d = nz(-9, 9);
          if (a * d + b * c === 0) d = d > 0 ? d + 1 : d - 1;
          return { a: a, b: b, c: c, d: d, r: pMul(lin(a, b), lin(c, d)), muster: '\\(' + kl(a, b) + kl(c, d) + ' = \\) {t}', text: 'Multipliziere aus und fasse zusammen.' }; },
        falsche: function(A){
          var f = [[[A.b * A.d, 0, A.a * A.c], 'jedes'], [[-A.b * A.d, A.a * A.d + A.b * A.c, A.a * A.c], 'Vorzeichen'], [[A.b * A.d, A.a * A.d - A.b * A.c, A.a * A.c], 'Vorzeichen']];
          return f.filter(function(p, i){ return !pEq(p[0], A.r) && !f.slice(0, i).some(function(q){ return pEq(q[0], p[0]); }); }); },
        fehler: function(A){ return TYPEN.ausmult.falsche(A).map(function(p){ return [{ t: kopfTerm(p[0]) }, p[1]]; }); },
        pruefen: function(A, e){
          var f = TYPEN.ausmult.falsche(A);
          for (var j = 0; j < f.length; j++) if (pEq(e.t.p, f[j][0]))
            return f[j][1] === 'jedes' ? 'Es fehlen die gemischten Glieder: <b>Jedes</b> Glied der ersten Klammer mal <b>jedes</b> der zweiten — vier Produkte.'
                                       : '<b>Vorzeichen</b> prüfen: Das Vorzeichen gehört zur Zahl dahinter. Schreib die vier Produkte einzeln auf.';
          return 'Vier Produkte bilden (Rechteckschema), dann die beiden \\(x\\)-Glieder zusammenfassen. Probe mit \\(x = 2\\).'; },
        tipps: function(A){ return ['Rechteckschema: jedes Glied der ersten Klammer mal jedes der zweiten.',
          'Die vier Produkte: \\(' + pTex([0, 0, A.a * A.c]) + '\\), \\(' + pTex([0, A.a * A.d]) + '\\), \\(' + pTex([0, A.b * A.c]) + '\\), \\(' + A.b * A.d + '\\).']; },
        loesung: function(A){ var g = function(c){ return (c < 0 ? ' - ' : ' + ') + pTex([0, Math.abs(c)]); };
          return kl(A.a, A.b) + kl(A.c, A.d) + ' = ' + pTex([0, 0, A.a * A.c]) + g(A.a * A.d) + g(A.b * A.c) + ' ' + vzTex(A.b * A.d) + ' = ' + pTex(A.r); } },

      'koeffizienten': { felder: ['p', 'q'],
        schl: function(A){ return 'ko|' + paarSchl(A.m, A.n); },
        neu: function(){
          var m = nz(-9, 9), n = nz(-9, 9); if (m + n === 0 || m === n && Math.random() < 0.7) n = n > 0 ? n - 1 || 2 : n + 1 || -2;
          return { m: m, n: n, p: m + n, q: m * n, muster: '\\(x^2 + \\) {p} \\(x + \\) {q}',
            text: 'Fülle aus: \\(' + kl(1, m) + kl(1, n) + ' = x^2 + \\square\\, x + \\square\\)' }; },
        fehler: function(A){
          var f = [];
          if (-A.q !== A.q) f.push([{ p: String(A.p), q: String(-A.q) }, 'Zahl am Schluss']);
          if (A.q !== A.p) f.push([{ p: String(A.q), q: String(A.p) }, 'vertauscht']);
          return f; },
        pruefen: function(A, e){
          if (e.p === A.q && e.q === A.p && A.p !== A.q) return 'Die beiden Werte sind vertauscht: Das <b>x-Glied</b> ist die <b>Summe</b> \\(' + kz(A.m) + ' + ' + kz(A.n) + '\\), die Zahl am Schluss das <b>Produkt</b>.';
          if (e.p === A.p && e.q !== A.q) return 'Das x-Glied stimmt. Die <b>Zahl am Schluss</b> ist das Produkt \\(' + kz(A.m) + ' \\cdot ' + kz(A.n) + '\\). Achte auf das Vorzeichen.';
          if (e.q === A.q && e.p !== A.p) return 'Die Zahl am Schluss stimmt. Das <b>x-Glied</b> ist die Summe der beiden Zahlen, mit Vorzeichen.';
          return 'Das x-Glied ist die Summe der Zahlen in den Klammern, die Zahl am Schluss ihr Produkt.'; },
        tipps: function(A){ return ['\\((x + m)(x + n) = x^2 + (m + n)x + m \\cdot n\\).', 'Hier: \\(m = ' + A.m + '\\), \\(n = ' + A.n + '\\).']; },
        loesung: function(A){ return kl(1, A.m) + kl(1, A.n) + ' = ' + pTex([A.q, A.p, 1]); } },

      /* ── Kapitel 3 ── */
      'binom': { felder: ['t'],
        schl: function(A){ return 'bi|' + A.art + '|' + A.a + '|' + A.b; },
        eingabe: function(A){ return { t: kopfTerm(A.r) }; },
        neu: function(){
          var art = zufall(['p', 'm', 'd']), a = zufall([1, 1, 2, 3, 4]), b = zufallG(1, 9);
          var r = art === 'p' ? pPow(lin(a, b), 2) : art === 'm' ? pPow(lin(a, -b), 2) : pMul(lin(a, b), lin(a, -b));
          var tex = art === 'p' ? kl(a, b) + '^2' : art === 'm' ? kl(a, -b) + '^2' : kl(a, b) + kl(a, -b);
          return { art: art, a: a, b: b, r: r, tex: tex, muster: '\\(' + tex + ' = \\) {t}', text: 'Rechne mit der binomischen Formel.' }; },
        falsche: function(A){
          var s = A.art === 'm' ? -1 : 1, f = [];
          if (A.art !== 'd'){
            f.push([[A.b * A.b, 0, A.a * A.a], 'mittlere']);
            f.push([[A.b * A.b, s * A.a * A.b, A.a * A.a], '2ab']);
            if (A.art === 'm'){ f.push([[-A.b * A.b, 0, A.a * A.a], 'mittlere']); f.push([[-A.b * A.b, -2 * A.a * A.b, A.a * A.a], 'Quadrat']); }
          } else f.push([[A.b * A.b, 0, -A.a * A.a], 'Vorzeichen']);
          if (A.a > 1) f.push([[A.art === 'd' ? -A.b * A.b : A.b * A.b, A.art === 'd' ? 0 : 2 * s * A.a * A.b, A.a], 'Zahl vor']);
          return f.filter(function(p, i){ return p[1] && !pEq(p[0], A.r) && !f.slice(0, i).some(function(q){ return pEq(q[0], p[0]); }); }); },
        fehler: function(A){ return TYPEN.binom.falsche(A).map(function(p){ return [{ t: kopfTerm(p[0]) }, p[1] === '2ab' ? 'zwei Rechtecke' : p[1]]; }); },
        pruefen: function(A, e){
          var f = TYPEN.binom.falsche(A);
          for (var j = 0; j < f.length; j++) if (pEq(e.t.p, f[j][0])){
            if (f[j][1] === 'mittlere') return 'Das <b>mittlere</b> Glied fehlt: ' + (A.art === 'm' ? '\\((a - b)^2 = a^2 - 2ab + b^2\\)' : '\\((a + b)^2 = a^2 + 2ab + b^2\\)') + ', nicht nur zwei Quadrate.';
            if (f[j][1] === '2ab') return 'Das mittlere Glied ist \\(2ab\\), nicht \\(ab\\): Im Quadrat-Bild gibt es zwei Rechtecke.';
            if (f[j][1] === 'Quadrat') return 'Am Schluss steht \\(b^2\\), und ein <b>Quadrat</b> ist nie negativ: \\((-' + A.b + ')^2 = +' + A.b * A.b + '\\).';
            if (f[j][1] === 'Zahl vor') return 'Auch die <b>Zahl vor</b> dem \\(x\\) wird quadriert: \\((' + A.a + 'x)^2 = ' + A.a * A.a + 'x^2\\).';
            return '<b>Vorzeichen:</b> \\((a + b)(a - b) = a^2 - b^2\\).';
          }
          return 'Setz \\(a\\) und \\(b\\) in die Formel ein und rechne jedes Glied einzeln. Probe mit \\(x = 2\\).'; },
        tipps: function(A){ var at = A.a === 1 ? 'x' : A.a + 'x';
          return [A.art === 'p' ? '\\((a + b)^2 = a^2 + 2ab + b^2\\)' : A.art === 'm' ? '\\((a - b)^2 = a^2 - 2ab + b^2\\)' : '\\((a + b)(a - b) = a^2 - b^2\\)',
                  'Hier ist \\(a = ' + at + '\\) und \\(b = ' + A.b + '\\).']; },
        loesung: function(A){ var at = A.a === 1 ? 'x' : '(' + A.a + 'x)';
          return A.tex + ' = ' + (A.art === 'd' ? at + '^2 - ' + A.b + '^2' : at + '^2 ' + (A.art === 'm' ? '-' : '+') + ' 2 \\cdot ' + (A.a === 1 ? 'x' : A.a + 'x') + ' \\cdot ' + A.b + ' + ' + A.b + '^2') + ' = ' + pTex(A.r); } },

      'binomluecke': { felder: ['m', 'q'],
        schl: function(A){ return 'bl|' + (A.s > 0 ? 'p' : 'm') + '|' + A.a + '|' + A.k; },
        neu: function(){
          var a = zufall([1, 1, 1, 2, 3]), k, s = zufall([1, -1]);
          do { k = zufallG(1, 12); } while (ggT(a, k) !== 1);
          var ax = a === 1 ? 'x' : a + 'x';
          return { a: a, k: k, s: s, m: k, q: k * k, ax: ax,
            muster: '\\((' + ax + ' ' + (s > 0 ? '+' : '-') + '\\) {m} \\()^2 = ' + pTex([0, 0, a * a]) + ' ' + (s > 0 ? '+' : '-') + ' ' + 2 * a * k + 'x + \\) {q}',
            text: 'Ergänze die Lücken.' }; },
        fehler: function(A){ var f = [[{ m: String(2 * A.a * A.k), q: String(4 * A.a * A.a * A.k * A.k) }, 'mittlere']];
          if (2 * A.k !== A.q) f.push([{ m: String(A.k), q: String(2 * A.k) }, 'Quadrat']); return f; },
        pruefen: function(A, e){
          if (e.m === 2 * A.a * A.k || (A.a > 1 && e.m === A.a * A.k)) return 'Das <b>mittlere</b> Glied ist \\(2 \\cdot ' + A.ax + ' \\cdot \\square\\). Teile \\(' + 2 * A.a * A.k + 'x\\) durch \\(2 \\cdot ' + A.ax + '\\).';
          if (e.m === A.k && e.q !== A.q) return 'Die Zahl in der Klammer stimmt. Am Schluss steht ihr <b>Quadrat</b>.';
          return 'Vergleiche mit ' + (A.s > 0 ? '\\((a + b)^2 = a^2 + 2ab + b^2\\)' : '\\((a - b)^2 = a^2 - 2ab + b^2\\)') + ': Hier ist \\(a = ' + A.ax + '\\), das mittlere Glied ist \\(2ab\\), am Schluss steht \\(b^2\\).'; },
        tipps: function(A){ return [(A.s > 0 ? '\\((a + b)^2 = a^2 + 2ab + b^2\\)' : '\\((a - b)^2 = a^2 - 2ab + b^2\\)') + ' mit \\(a = ' + A.ax + '\\): Das mittlere Glied verrät \\(b\\).',
          '\\(2 \\cdot ' + A.ax + ' \\cdot b = ' + 2 * A.a * A.k + 'x\\), also \\(b = ' + A.k + '\\).']; },
        loesung: function(A){ return '(' + A.ax + (A.s > 0 ? ' + ' : ' - ') + A.k + ')^2 = ' + pTex([A.k * A.k, 2 * A.s * A.a * A.k, A.a * A.a]); } },

      /* ── Kapitel 4 ── */
      'ausklammern': { felder: ['t'], produkt: true,
        schl: function(A){ return 'ak|' + A.g + '|' + A.p + '|' + A.q; },
        eingabe: function(A){ return { t: A.loes }; },
        neu: function(){
          var v = zufall(['x', 'a', 'y']), g = zufallG(2, 9), p, q, mitV = Math.random() < 0.5;
          do { p = zufallG(1, 6); q = nz(-9, 9); } while (ggT(p, q) !== 1);
          var inner = lin(p, q), faktor = mitV ? [0, g] : [g];
          var r = pMul(faktor, inner), gT = mitV ? g + v : String(g);
          return { v: v, g: g, p: p, q: q, mitV: mitV, r: r, loes: (mitV ? g + v : g) + '(' + pTxt(inner, v) + ')',
            muster: '\\(' + pTex(r, v) + ' = \\) {t}', text: 'Klammere so viel wie möglich aus (Produktform).', gT: gT }; },
        fehler: function(A){
          var f = [[{ t: pTxt(A.r, A.v) }, 'Produkt']];
          if (A.mitV) f.push([{ t: A.v + '(' + pTxt(lin(A.g * A.p, A.g * A.q), A.v) + ')' }, 'vollständig']);
          else if (A.g % 2 === 0 && A.g > 2) f.push([{ t: '2(' + pTxt(lin(A.g / 2 * A.p, A.g / 2 * A.q), A.v) + ')' }, 'vollständig']);
          f.push([{ t: A.gT.replace(/x|a|y/, A.v) + '(' + pTxt(lin(A.p, -A.q), A.v) + ')' }, 'Probe']);
          return f; },
        pruefen: function(A, e){ return 'Multipliziere zur <b>Probe</b> aus: Es muss \\(' + pTex(A.r, A.v) + '\\) herauskommen.'; },
        tipps: function(A){ return ['Suche den grössten gemeinsamen Faktor: den ggT der Zahlen' + (A.mitV ? ' und die gemeinsame Variable.' : '.'),
          'Gemeinsamer Faktor: \\(' + A.gT + '\\). Teile jedes Glied durch ihn.']; },
        loesung: function(A){ return pTex(A.r, A.v) + ' = ' + A.gT + kl(A.p, A.q, A.v); } },

      'faktorisieren': { felder: ['t'], produkt: true,
        schl: function(A){ return 'fz|' + A.art + '|' + (A.art === 't' ? paarSchl(A.m, A.n) : A.art === 'b' ? A.k : A.art === 'k' ? A.f + '|' + A.u + '|' + A.b : A.a + '|' + A.b); },
        eingabe: function(A){ return { t: A.loes }; },
        neu: function(){
          var art = zufall(['t', 't', 'b', 'd', 'k']), m, n, r, loes, k, a, b;
          if (art === 'k'){                    // erst ausklammern, dann binomische Formel (Prüfung 10.10.2026)
            var f_ = zufallG(2, 5), u = zufall(['b', 'd']); b = u === 'b' ? nz(-6, 6) : zufallG(1, 6);
            r = pMul([f_], u === 'b' ? pPow(lin(1, b), 2) : pMul(lin(1, -b), lin(1, b)));
            loes = f_ + (u === 'b' ? '(' + pTxt(lin(1, b)) + ')^2' : '(' + pTxt(lin(1, -b)) + ')(' + pTxt(lin(1, b)) + ')');
            return { art: art, f: f_, u: u, b: b, r: r, loes: loes, muster: '\\(' + pTex(r) + ' = \\) {t}', text: 'Faktorisiere vollständig.' }; }
          if (art === 't'){ do { m = nz(-9, 9); n = nz(-9, 9); } while (m === n || m === -n || Math.abs(m * n) > 60);
            r = pMul(lin(1, m), lin(1, n)); loes = '(' + pTxt(lin(1, m)) + ')(' + pTxt(lin(1, n)) + ')';
            return { art: art, m: m, n: n, r: r, loes: loes, muster: '\\(' + pTex(r) + ' = \\) {t}', text: 'Faktorisiere vollständig.' }; }
          if (art === 'b'){ k = nz(-9, 9); r = pPow(lin(1, k), 2); loes = '(' + pTxt(lin(1, k)) + ')^2';
            return { art: art, k: k, r: r, loes: loes, muster: '\\(' + pTex(r) + ' = \\) {t}', text: 'Faktorisiere vollständig.' }; }
          a = zufall([1, 1, 2, 3, 4, 5]); do { b = zufallG(1, 9); } while (ggT(a, b) !== 1);
          r = pMul(lin(a, b), lin(a, -b)); loes = '(' + pTxt(lin(a, b)) + ')(' + pTxt(lin(a, -b)) + ')';
          return { art: art, a: a, b: b, r: r, loes: loes, muster: '\\(' + pTex(r) + ' = \\) {t}', text: 'Faktorisiere vollständig.' }; },
        falsche: function(A){
          var f = [];
          if (A.art === 't'){ f.push([lin(1, -A.m), lin(1, -A.n), 'Vorzeichen']); if (A.m * A.n < 0) f.push([lin(1, A.m), lin(1, -A.n), 'Vorzeichen']); }
          if (A.art === 'b'){ f.push([lin(1, A.k), lin(1, -A.k), 'Formel']); f.push([lin(1, -A.k), lin(1, -A.k), 'Vorzeichen']); }
          if (A.art === 'd'){ f.push([lin(A.a, -A.b), lin(A.a, -A.b), 'Formel']); }
          if (A.art === 'k'){ f.push(A.u === 'b' ? [lin(A.f, A.f * A.b), lin(1, -A.b), 'Formel'] : [lin(A.f, -A.f * A.b), lin(1, -A.b), 'Formel']); }
          return f.filter(function(p){ return !pEq(pMul(p[0], p[1]), A.r); }); },
        fehler: function(A){
          var f = TYPEN.faktorisieren.falsche(A).map(function(p){ return [{ t: '(' + pTxt(p[0]) + ')(' + pTxt(p[1]) + ')' }, p[2]]; });
          f.push([{ t: pTxt(A.r) }, 'Produkt']);
          return f; },
        pruefen: function(A, e){
          var f = TYPEN.faktorisieren.falsche(A);
          for (var j = 0; j < f.length; j++) if (pEq(e.t.p, pMul(f[j][0], f[j][1]))){
            if (f[j][2] === 'Vorzeichen') return '<b>Vorzeichen</b> prüfen: Die beiden Zahlen müssen multipliziert \\(' + A.r[0] + '\\) und addiert \\(' + A.r[1] + '\\) ergeben.';
            var mitte = A.art === 'b' || (A.art === 'k' && A.u === 'b');
            return mitte ? 'Mit einem mittleren Glied ist es ein Quadrat \\((a + b)^2\\) oder \\((a - b)^2\\). Ein Produkt \\((a + b)(a - b)\\) hat kein mittleres Glied (binomische <b>Formel</b> verwechselt).'
                         : 'Ohne mittleres Glied ist es \\(a^2 - b^2 = (a + b)(a - b)\\), also kein Quadrat (binomische <b>Formel</b> verwechselt).';
          }
          return 'Multipliziere zur <b>Probe</b> aus: Es muss \\(' + pTex(A.r) + '\\) herauskommen.'; },
        tipps: function(A){
          if (A.art === 't') return ['Suche zwei Zahlen mit Produkt \\(' + A.r[0] + '\\) und Summe \\(' + A.r[1] + '\\).', 'Die Zahlenpaare mit Produkt \\(' + A.r[0] + '\\) aufschreiben, dann die Summe prüfen.'];
          if (A.art === 'k') return ['Zuerst den gemeinsamen Faktor \\(' + A.f + '\\) ausklammern.', 'In der Klammer steht \\(' + pTex(pMul([1], A.u === 'b' ? pPow(lin(1, A.b), 2) : pMul(lin(1, -A.b), lin(1, A.b)))) + '\\): binomische Formel rückwärts.'];
          if (A.art === 'b') return ['Erstes und letztes Glied sind Quadrate: binomische Formel rückwärts.', '\\(' + A.k * A.k + ' = ' + Math.abs(A.k) + '^2\\); das mittlere Glied entscheidet über das Vorzeichen.'];
          return ['Zwei Quadrate mit Minus dazwischen: \\(a^2 - b^2 = (a + b)(a - b)\\).', '\\(' + pTex([0, 0, A.a * A.a]) + ' = (' + (A.a === 1 ? 'x' : A.a + 'x') + ')^2\\) und \\(' + A.b * A.b + ' = ' + A.b + '^2\\).']; },
        loesung: function(A){ return pTex(A.r) + ' = ' + (A.art === 'k' ? A.f + '(' + pTex(A.u === 'b' ? pPow(lin(1, A.b), 2) : pMul(lin(1, -A.b), lin(1, A.b))) + ') = ' : '') + A.loes.replace(/\*/g, ''); } }
    };
    window.__TYPEN = TYPEN; window.__SPERRE = SPERRE; window.__gesperrt = gesperrt;
    window.__term = { termLesen: termLesen, produktBefund: produktBefund, zusammengefasst: zusammengefasst, pEq: pEq };

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
        var html = A.muster || T.muster;
        T.felder.forEach(function(f){
          html = html.replace('{' + f + '}', f === 't'
            ? '<input type="text" inputmode="text" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="Term" data-f="t" class="term" placeholder="' + (T.produkt ? 'z. B. 3' + (A.v || 'x') + '(' + (A.v || 'x') + '-2)' : 'z. B. 3x^2 - 2x + 1') + '">'
            : '<input type="text" inputmode="numeric" autocomplete="off" aria-label="Zahl" data-f="' + f + '">');
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
          var inp = felder[i], f = inp.dataset.f, roh = inp.value.trim().replace(/[\u2212\u2013]/g, '-');
          inp.classList.remove('falsch');
          if (!roh) return hinweis('Fülle das Feld aus.');
          if (f === 't'){
            var r = termLesen(roh, A.v || 'x');
            if (r.kaputt){ inp.classList.add('falsch'); return hinweis(r.grund); }
            if (pEq(r.p, A.r)){
              if (T.produkt){
                var bef = produktBefund(r);
                if (bef && bef.art === 'summe'){ versuche++; return hinweis('Gleichwertig — aber das ist eine Summe. Gesucht ist ein <b>Produkt</b> (Faktoren mit Klammern).'); }
                if (bef){ versuche++; return hinweis('Gleichwertig, aber noch nicht <b>vollständig</b> faktorisiert: Der Faktor \\(' + pTex(bef.p, A.v || 'x') + '\\) lässt sich weiter zerlegen' + (bef.grund === 'inhalt' ? ' — er hat noch einen gemeinsamen Faktor.' : bef.grund === 'variable' ? ' — jedes Glied enthält die Variable.' : '.')); }
              } else if (!zusammengefasst(r.baum)){ versuche++; return hinweis('Gleichwertig, aber noch nicht <b>zusammengefasst</b>: keine Klammern mehr, jede Art Glied nur einmal.'); }
            }
            e.t = r;
          } else {
            if (!/^[+-]?\d+$/.test(roh)){ inp.classList.add('falsch'); return hinweis('Gib eine ganze Zahl ein.'); }
            e[f] = +roh;
          }
        }
        versuche++;
        var ok = T.felder.every(function(f){ return f === 't' ? pEq(e.t.p, A.r) : e[f] === A[f]; });
        if (ok){
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

  /* ---------- Minibilder: <svg class="mini-term" data-rechteck="a,b"> Flächenmodell (x + a)(x + b);
       data-binom="a,b" Quadrat (a + b)² mit vier Teilflächen (ohne Zahlen). ---------- */
  document.querySelectorAll('svg.mini-term').forEach(function(svg){
    svg.setAttribute('role', 'img');
    if (svg.dataset.rechteck){
      var q = svg.dataset.rechteck.split(',').map(Number);
      svg.setAttribute('viewBox', '0 0 ' + (60 + 90 + q[1] * 16) + ' ' + (40 + 90 + q[0] * 16));
      flaeche(svg, q[0], q[1], 30, 22, 90);
    } else if (svg.dataset.binom){
      var E = 26, a = 4, b = 2;
      svg.setAttribute('viewBox', '0 0 ' + (30 + (a + b) * E) + ' ' + (30 + (a + b) * E));
      var R = function(x, y, w, h, c){ el(svg, 'rect', { x: 20 + x * E, y: 10 + y * E, width: w * E, height: h * E, 'class': c }); };
      R(0, 0, a, a, 'fl-q'); R(a, 0, b, a, 'fl-x'); R(0, a, a, b, 'fl-x'); R(a, a, b, b, 'fl-1'); R(0, 0, a + b, a + b, 'rahmen');
      el(svg, 'text', { x: 20 + a * E / 2, y: 8 + (a + b) * E + 18, 'text-anchor': 'middle', 'class': 'st-name' }, 'a');
      el(svg, 'text', { x: 20 + (a + b / 2) * E, y: 8 + (a + b) * E + 18, 'text-anchor': 'middle', 'class': 'st-name' }, 'b');
    }
  });
})();
</script>
