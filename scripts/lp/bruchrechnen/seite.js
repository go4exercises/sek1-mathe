<script>
/* Leitprogramm Bruchrechnen — Bruchstreifen (Sim 1, 2), Flächen- und Messmodell (Sim 3),
   Schrittwähler für die Rechenreihenfolge (Sim 4), Übungen mit Rückmeldung, Minibilder.
   Alles mit ganzen Zahlen gerechnet (Zähler/Nenner), nie mit Gleitkomma — ein Bruch ist
   {z, n} mit n > 0. Eine Farbe, eine Bedeutung: blau = erster Bruch, orange = zweiter Bruch,
   grün = Ergebnis, rot = Fehler. Zahlen mit echtem Minus; Brüche im Bild als HTML-Bruch. */
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
  function mz(n){ return (n < 0 ? '−' : '') + Math.abs(n); }           // echtes Minus

  /* ---------- Bruchrechnung, exakt ---------- */
  function ggT(a, b){ a = Math.abs(a); b = Math.abs(b); while (b){ var t = a % b; a = b; b = t; } return a; }
  function kgV(a, b){ return a / ggT(a, b) * b; }
  function B(z, n){
    if (n === undefined) n = 1;
    if (n < 0){ z = -z; n = -n; }
    var g = ggT(z, n) || 1; return { z: z / g, n: n / g };
  }
  function plus(x, y){ return B(x.z * y.n + y.z * x.n, x.n * y.n); }
  function minus(x, y){ return B(x.z * y.n - y.z * x.n, x.n * y.n); }
  function mal(x, y){ return B(x.z * y.z, x.n * y.n); }
  function durch(x, y){ return B(x.z * y.n, x.n * y.z); }
  function hoch(x, e){ var r = B(1); for (var i = 0; i < e; i++) r = mal(r, x); return r; }
  function rechne(o, x, y){ return o === '+' ? plus(x, y) : o === '−' ? minus(x, y) : o === '·' ? mal(x, y) : o === ':' ? durch(x, y) : hoch(x, y); }
  function gleich(x, y){ return x.z * y.n === y.z * x.n; }
  function txt(b){ return b.n === 1 ? String(b.z) : b.z + '/' + b.n; }   // so tippt man es ein

  /* Bruch als LaTeX; kl: negative Zahl in Klammern (nach einem Rechenzeichen). */
  function tb(b, kl, gross){
    var f = gross ? '\\dfrac' : '\\tfrac';
    var s = b.n === 1 ? String(Math.abs(b.z)) : f + '{' + Math.abs(b.z) + '}{' + b.n + '}';
    if (b.z < 0) s = '-' + s;
    return b.z < 0 && kl ? '\\left(' + s + '\\right)' : s;
  }
  /* Bruch als HTML (ohne MathJax: Bilder und Schrittwähler setzen sich sofort). */
  function hb(b, kl){
    var a = Math.abs(b.z);
    var inner = b.n === 1 ? '<span class="bz-g">' + a + '</span>'
      : '<span class="bz" role="img" aria-label="' + mz(b.z) + ' durch ' + b.n + '"><span class="bz-z" aria-hidden="true">' + a + '</span><span class="bz-n" aria-hidden="true">' + b.n + '</span></span>';
    var s = (b.z < 0 ? '−' : '') + inner;
    return b.z < 0 && kl ? '(' + s + ')' : s;
  }

  /* ---------- Eingabe lesen ----------
     «3/4», «-3/4», «−3/4», «(-3)/4», «3/-4», «-(3/4)», ganze Zahlen «5», «-2».
     Dezimalzahlen werden verstanden (gleicher Wert → «als Bruch angeben»), gemischte Zahlen
     («2 1/3») erkannt und abgelehnt — sie liest man leicht als Produkt. Die rohe Eingabe bleibt
     erhalten (z, n ungekürzt), damit «noch nicht vollständig gekürzt» erkannt wird. */
  function bruchLesen(s){
    s = String(s == null ? '' : s).trim().replace(/[\u2212\u2013]/g, '-');
    if (!s) return { leer: true };
    if (/^-?\d+\s+\d+\s*\/\s*\d+$/.test(s)) return { gemischt: true };
    var komma = /\d,\d/.test(s);
    s = s.replace(/\s+/g, '').replace(/(\d),(\d)/g, '$1.$2').replace(/^\+/, '');
    var m, z, n, strich = false, dez = false;
    if ((m = s.match(/^-\((\d+)\/(\d+)\)$/))){ z = -(+m[1]); n = +m[2]; strich = true; }
    else if ((m = s.match(/^\(?([+-]?\d+)\)?\/\(?([+-]?\d+)\)?$/))){ z = +m[1]; n = +m[2]; strich = true; }
    else if (/^-?\d+$/.test(s)){ z = +s; n = 1; }
    else if ((m = s.match(/^(-?)(\d*)\.(\d+)$/))){ n = Math.pow(10, m[3].length); z = (+(m[2] || 0) * n + (+m[3])) * (m[1] ? -1 : 1); dez = true; }
    else return { kaputt: true };
    if (n === 0) return { kaputt: true, null: true };
    if (n < 0){ z = -z; n = -n; }
    return { z: z, n: n, strich: strich, dez: dez, komma: komma };
  }
  function gekuerzt(r){ return ggT(r.z, r.n) === 1 && !(r.strich && r.n === 1); }

  /* ---------- Aufgabenleiste (wie in den anderen Leitprogrammen) ----------
     Eine Aufgabe nach der anderen; ✓ sobald der Zustand stimmt. «überspringen» geht immer. */
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
        if (sim.ende) sim.ende();
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
    // Beim Wechsel alles auf den Startwert, sonst erfüllt der Endzustand der vorigen Aufgabe die
    // nächste schon (HOWTO §15).
    function gehe(j){
      i = j;
      fig.querySelectorAll('input[type=range]').forEach(function(inp){ inp.value = inp.defaultValue; });
      fig.querySelectorAll('.sim-schalter input').forEach(function(inp){ inp.checked = inp.defaultChecked; });
      fig.querySelectorAll('select.sim-wahl').forEach(function(s){ s.value = s.querySelector('option[selected]').value; });
      if (sim.aufraeumen) sim.aufraeumen(); zeigen(); if (sim.zeichnen) sim.zeichnen();
    }
    bt.addEventListener('click', function(){
      if (i >= n){ if (anzahl() === n){ erledigt = {}; gehe(0); } else gehe(offen(0)); }
      else gehe(offen(i + 1));
    });
    bv.addEventListener('click', function(){ erledigt = {}; gehe(0); });
    setTimeout(zeigen, 0);
    return pruefen;
  }
  function wert(fig, id){ return +fig.querySelector('#' + id).value; }
  function zeigeWert(fig, id){ var i = fig.querySelector('#' + id); var v = i.parentNode.querySelector('.sl-val'); if (v) v.textContent = i.value; }

  /* Ein Streifen (Rechteck aus n gleichen Teilen, die ersten k gefärbt). */
  function streifen(g, x, y, w, h, n, k, cls, ab){
    var dx = w / n;
    for (var j = 0; j < n; j++){
      el(g, 'rect', { x: x + j * dx, y: y, width: dx, height: h, 'class': (j >= (ab || 0) && j < k ? 'zelle ' + cls : 'zelle leer') });
    }
    el(g, 'rect', { x: x, y: y, width: w, height: h, 'class': 'rahmen' });
  }

  /* ════════ Sim 1 — Erweitern und Kürzen am Bruchstreifen ════════
     Unterschied zur Themenseite (dort noch keine Animation, Stand 09.10.2026): Hier ist der obere
     Streifen fest (Ziel), der untere wird mit Nenner und Zähler nachgebaut; die gestrichelte
     Hilfslinie zeigt, wo der Ziel-Anteil endet. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    var hilfe = fig.querySelector('.sim-schalter input');
    var S = { a: 3, b: 4 };
    var X0 = 20, W = 300;
    function korrigiere(){                     // Zähler höchstens Nenner — vor dem Zeichnen
      var kn = fig.querySelector('#s1-k'), n = wert(fig, 's1-n');
      kn.max = n; if (+kn.value > n) kn.value = n;
    }
    function zustand(){ return { a: S.a, b: S.b, n: wert(fig, 's1-n'), k: wert(fig, 's1-k') }; }
    function zeichnen(){
      korrigiere();
      var Z = zustand(); zeigeWert(fig, 's1-n'); zeigeWert(fig, 's1-k');
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      el(svg, 'text', { x: X0, y: 16, 'class': 'st-name' }, 'oben');
      streifen(svg, X0, 22, W, 34, Z.b, Z.a, 'f1');
      el(svg, 'text', { x: X0, y: 86, 'class': 'st-name' }, 'unten');
      streifen(svg, X0, 92, W, 34, Z.n, Z.k, 'f2');
      var gl = Z.k * Z.b === Z.a * Z.n;
      if (gl) el(svg, 'rect', { x: X0 - 3, y: 89, width: W + 6, height: 40, 'class': 'treffer-rahmen' });
      if (hilfe.checked){
        var xs = X0 + W * Z.a / Z.b;
        el(svg, 'line', { x1: xs, y1: 18, x2: xs, y2: 134, 'class': 'hilfslinie' });
      }
      formel.innerHTML = 'oben ' + hb({ z: Z.a, n: Z.b }) + '; unten ' + hb({ z: Z.k, n: Z.n }) +
        (gl ? ' <span class="ok-text">gleich gross</span>' : ' <span class="nein-text">nicht gleich gross</span>');
      if (pr) pr();
    }
    var sim = { zustand: zustand, zeichnen: zeichnen };
    var pr = null;
    pr = Leiste(fig, [
      // Andere Zahlen als Clip und Festhalten (3/4 = 15/20, 12/18 = 2/3, 2/3 < 3/4): HOWTO §15.
      { text: 'Stell unten denselben Anteil dar wie oben — aber mit dem Nenner 10.', setup: function(){ S = { a: 3, b: 5 }; },
        ok: function(z){ return z.n === 10 && z.k === 6; } },
      { text: 'Jetzt mit dem Nenner 20. Wie viele Teile musst du färben?', setup: function(){ S = { a: 3, b: 5 }; },
        ok: function(z){ return z.n === 20 && z.k === 12; } },
      { text: 'Oben sind 10 von 16 Teilen gefärbt. Stell denselben Anteil mit möglichst wenigen Teilen dar.', setup: function(){ S = { a: 10, b: 16 }; },
        ok: function(z){ return z.n === 8 && z.k === 5; } },
      { text: 'Geht \\(\\tfrac{5}{6}\\) mit dem Nenner 4? Probier es. Stell dann den kleinsten Nenner über 6 ein, mit dem es geht.', setup: function(){ S = { a: 5, b: 6 }; },
        ok: function(z){ return z.n === 12 && z.k === 10; } },
      { text: 'Oben steht \\(\\tfrac{3}{8}\\). Stell unten \\(\\tfrac{1}{3}\\) dar, und zwar mit dem kleinsten Nenner, den auch \\(\\tfrac{3}{8}\\) haben kann. Welcher Bruch ist grösser?', setup: function(){ S = { a: 3, b: 8 }; },
        ok: function(z){ return z.n === 24 && z.k === 8; } }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); i.addEventListener('change', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 2 — Addieren und Subtrahieren: gemeinsame Unterteilung ════════
     Zwei Streifen, eine Unterteilung N für beide. Passt N zu beiden Nennern, erscheint das Ergebnis
     in N-teln. Der Schalter zeigt den Fehler «Zähler plus Zähler, Nenner plus Nenner» als roten
     Streifen — er ist kleiner als der erste Summand allein. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    var falschS = fig.querySelector('.sim-schalter input');
    var S = { a: 1, b: 2, o: '+', c: 1, d: 3 };
    var X0 = 44, W = 280;
    function zustand(){ return { N: wert(fig, 's2-n'), falsch: falschS.checked, b: S.b, d: S.d }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's2-n');
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      var N = Z.N, p1 = N % S.b === 0, p2 = N % S.d === 0;
      function zeile(y, n, k, cls, passt, name){
        el(svg, 'text', { x: 4, y: y + 22, 'class': 'st-name' }, name);
        streifen(svg, X0, y, W, 30, n, k, cls);
        for (var j = 1; j < N; j++){ var x = X0 + W * j / N; el(svg, 'line', { x1: x, y1: y - 4, x2: x, y2: y + 34, 'class': passt ? 'teilung' : 'teilung schief' }); }
      }
      zeile(14, S.b, S.a, 'f1', p1, S.a + '/' + S.b);
      zeile(64, S.d, S.c, 'f2', p2, S.c + '/' + S.d);
      var r = rechne(S.o, B(S.a, S.b), B(S.c, S.d));
      var t = 'Unterteilung in ' + N + ' Teile: ' + hb({ z: S.a, n: S.b }) + ' = ' + (p1 ? hb({ z: S.a * N / S.b, n: N }) + ' <span class="ok-text">✓</span>' : '<span class="nein-text">passt nicht</span>') +
              '; ' + hb({ z: S.c, n: S.d }) + ' = ' + (p2 ? hb({ z: S.c * N / S.d, n: N }) + ' <span class="ok-text">✓</span>' : '<span class="nein-text">passt nicht</span>');
      if (p1 && p2){
        var k1 = S.a * N / S.b, k2 = S.c * N / S.d;
        el(svg, 'text', { x: 4, y: 136, 'class': 'st-name' }, S.o === '+' ? 'Summe' : 'Differenz');
        if (S.o === '+'){ streifen(svg, X0, 114, W, 30, N, k1, 'f1'); for (var j = k1; j < k1 + k2; j++) el(svg, 'rect', { x: X0 + W * j / N, y: 114, width: W / N, height: 30, 'class': 'zelle f2' }); }
        else { streifen(svg, X0, 114, W, 30, N, k1 - k2, 'f1'); for (var q = k1 - k2; q < k1; q++) el(svg, 'rect', { x: X0 + W * q / N, y: 114, width: W / N, height: 30, 'class': 'zelle weg' }); }
        el(svg, 'rect', { x: X0, y: 114, width: W, height: 30, 'class': 'rahmen' });
        var roh = { z: S.o === '+' ? k1 + k2 : k1 - k2, n: N };
        t += '<br>' + hb({ z: k1, n: N }) + ' ' + S.o + ' ' + hb({ z: k2, n: N }) + ' = ' + hb(roh) + (gleich(roh, r) && (roh.n !== r.n) ? ' = ' + hb(r) : '');
      } else {
        el(svg, 'text', { x: X0 + W / 2, y: 134, 'text-anchor': 'middle', 'class': 'st-frage' }, 'Ergebnis erst, wenn beide Streifen in die Unterteilung passen');
      }
      if (Z.falsch){
        el(svg, 'text', { x: 4, y: 186, 'class': 'st-name falsch' }, (S.a + S.c) + '/' + (S.b + S.d));
        if (S.o === '+') streifen(svg, X0, 164, W, 30, S.b + S.d, S.a + S.c, 'f4');
        else el(svg, 'text', { x: X0, y: 184, 'class': 'st-frage' }, 'Der Fehler-Streifen gehört zur Addition.');
      }
      formel.innerHTML = t;
      if (pr) pr();
    }
    var sim = { zustand: zustand, zeichnen: zeichnen };
    var pr = null;
    function setze(a, b, o, c, d){ return function(){ S = { a: a, b: b, o: o, c: c, d: d }; }; }
    pr = Leiste(fig, [
      // Andere Zahlen als Clip und Festhalten (1/2 + 1/3, 5/12 + 7/18): HOWTO §15.
      { text: '\\(\\tfrac{1}{4} + \\tfrac{1}{6}\\): Stell eine Unterteilung ein, in die beide Streifen genau passen.', setup: setze(1, 4, '+', 1, 6),
        ok: function(z){ return z.N % 4 === 0 && z.N % 6 === 0; } },
      { text: 'Und jetzt die <b>kleinste</b> Unterteilung, die für beide passt.', setup: setze(1, 4, '+', 1, 6),
        ok: function(z){ return z.N === 12; } },
      { text: 'Schalte den roten Streifen ein: So rechnet, wer Zähler plus Zähler und Nenner plus Nenner nimmt. Ist \\(\\tfrac{2}{10}\\) grösser als \\(\\tfrac{1}{4}\\) allein?', setup: setze(1, 4, '+', 1, 6),
        ok: function(z){ return z.falsch; } },
      { text: '\\(\\tfrac{3}{8} + \\tfrac{1}{6}\\): Finde die kleinste gemeinsame Unterteilung.', setup: setze(3, 8, '+', 1, 6),
        ok: function(z){ return z.N === 24; } },
      { text: '\\(\\tfrac{7}{9} - \\tfrac{1}{6}\\): Wieder die kleinste gemeinsame Unterteilung. Wie viele \\(\\tfrac{1}{18}\\) bleiben?', setup: setze(7, 9, '−', 1, 6),
        ok: function(z){ return z.N === 18; } },
      { text: '\\(\\tfrac{2}{5} + \\tfrac{1}{3}\\): Ist hier das Produkt der Nenner schon die kleinste gemeinsame Unterteilung?', setup: setze(2, 5, '+', 1, 3),
        ok: function(z){ return z.N === 15; } }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); i.addEventListener('change', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 3 — Multiplizieren (Flächenmodell) und Dividieren (Messen) ════════
     «Mal»: Im Einheitsquadrat sind a/b der Breite (blau) und c/d der Höhe (orange) gefärbt; das
     Rechteck, das beide trifft (grün), ist das Produkt. «Durch»: Wie oft passt c/d in a/b? */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]'), modus = fig.querySelector('select.sim-wahl');
    function korrigiere(){
      [['s3-a', 's3-b'], ['s3-c', 's3-d']].forEach(function(p){
        var z = fig.querySelector('#' + p[0]), n = wert(fig, p[1]); z.max = n; if (+z.value > n) z.value = n; });
    }
    function zustand(){ return { m: modus.value, a: wert(fig, 's3-a'), b: wert(fig, 's3-b'), c: wert(fig, 's3-c'), d: wert(fig, 's3-d') }; }
    function zeichnen(){
      korrigiere();
      var Z = zustand(); ['s3-a', 's3-b', 's3-c', 's3-d'].forEach(function(id){ zeigeWert(fig, id); });
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      var x = { z: Z.a, n: Z.b }, y = { z: Z.c, n: Z.d }, i, j;
      if (Z.m === 'mal'){
        svg.setAttribute('viewBox', '0 0 340 250');
        var X0 = 80, Y0 = 30, S = 200;
        for (i = 0; i < Z.b; i++) for (j = 0; j < Z.d; j++){
          var cls = (i < Z.a && j < Z.c) ? 'f3' : i < Z.a ? 'f1' : j < Z.c ? 'f2' : 'leer';
          el(svg, 'rect', { x: X0 + S * i / Z.b, y: Y0 + S * j / Z.d, width: S / Z.b, height: S / Z.d, 'class': 'zelle ' + cls });
        }
        el(svg, 'rect', { x: X0, y: Y0, width: S, height: S, 'class': 'rahmen' });
        el(svg, 'line', { x1: X0, y1: Y0 - 8, x2: X0 + S * Z.a / Z.b, y2: Y0 - 8, 'class': 'mass f1' });
        el(svg, 'text', { x: X0 + S * Z.a / Z.b / 2, y: Y0 - 13, 'text-anchor': 'middle', 'class': 'st-name blau' }, Z.a + '/' + Z.b);
        el(svg, 'line', { x1: X0 - 8, y1: Y0, x2: X0 - 8, y2: Y0 + S * Z.c / Z.d, 'class': 'mass f2' });
        el(svg, 'text', { x: X0 - 13, y: Y0 + S * Z.c / Z.d / 2 + 4, 'text-anchor': 'end', 'class': 'st-name orange' }, Z.c + '/' + Z.d);
        el(svg, 'text', { x: X0 + S + 8, y: Y0 + S, 'class': 'st-frage' }, '1');
        var roh = { z: Z.a * Z.c, n: Z.b * Z.d }, r = mal(x, y);
        formel.innerHTML = hb(x) + ' · ' + hb(y) + ' = ' + hb(roh) + (roh.n !== r.n ? ' = ' + hb(r) : '') +
          ' <span class="grau">(grün: ' + roh.z + ' von ' + roh.n + ' Kästchen)</span>';
      } else {
        svg.setAttribute('viewBox', '0 0 340 170');
        var A0 = 20, L = 300, q = durch(x, y), ganz = Math.floor(q.z / q.n);
        el(svg, 'text', { x: A0, y: 18, 'class': 'st-name blau' }, Z.a + '/' + Z.b);
        el(svg, 'rect', { x: A0, y: 24, width: L * Z.a / Z.b, height: 30, 'class': 'zelle f1' });
        el(svg, 'rect', { x: A0, y: 24, width: L, height: 30, 'class': 'rahmen duenn' });
        var st = L * Z.c / Z.d, k = 0;
        for (var p = 0; p + 1e-9 < L * Z.a / Z.b; p += st, k++){
          var breite = Math.min(st, L * Z.a / Z.b - p), voll = breite > st - 1e-9;
          el(svg, 'rect', { x: A0 + p, y: 66, width: breite, height: 30, 'class': 'zelle ' + (voll ? (k % 2 ? 'f2' : 'f2b') : 'f2 rest') });
          if (voll) el(svg, 'text', { x: A0 + p + breite / 2, y: 86, 'text-anchor': 'middle', 'class': 'st-zahl' }, String(k + 1));
        }
        el(svg, 'text', { x: A0, y: 118, 'class': 'st-name orange' }, 'Stück: ' + Z.c + '/' + Z.d);
        for (i = 0; i <= 4; i++){ var xx = A0 + L * i / 4; el(svg, 'line', { x1: xx, y1: 128, x2: xx, y2: 134, 'class': 'achse' }); }
        el(svg, 'line', { x1: A0, y1: 131, x2: A0 + L, y2: 131, 'class': 'achse' });
        el(svg, 'text', { x: A0, y: 150, 'text-anchor': 'middle', 'class': 'skala' }, '0');
        el(svg, 'text', { x: A0 + L, y: 150, 'text-anchor': 'middle', 'class': 'skala' }, '1');
        var rest = minus(q, B(ganz));
        formel.innerHTML = hb(x) + ' : ' + hb(y) + ' = ' + hb(x) + ' · ' + hb({ z: Z.d, n: Z.c }) + ' = ' + hb(q) +
          ' <span class="grau">(' + (rest.z === 0 ? 'passt genau ' + ganz + '-mal' : ganz === 0 ? 'passt nicht ganz: nur ' + hb(rest) + ' des Stücks' : 'passt ' + ganz + '-mal ganz, dazu ' + hb(rest) + ' des Stücks') + ')</span>';
      }
      if (pr) pr();
    }
    var sim = { zustand: zustand, zeichnen: zeichnen };
    var pr = null;
    function auf(m){ return function(){ modus.value = m; }; }
    pr = Leiste(fig, [
      { text: '«Mal»: Stell \\(\\tfrac{3}{5} \\cdot \\tfrac{2}{3}\\) ein. Wie viele Kästchen hat das Quadrat, wie viele sind grün?', setup: auf('mal'),
        ok: function(z){ return z.m === 'mal' && z.a === 3 && z.b === 5 && z.c === 2 && z.d === 3; } },
      { text: 'Stell zwei Brüche kleiner als 1 ein, deren Produkt genau \\(\\tfrac{1}{4}\\) ist — aber nicht \\(\\tfrac{1}{2} \\cdot \\tfrac{1}{2}\\).', setup: auf('mal'),
        ok: function(z){ return z.m === 'mal' && z.a < z.b && z.c < z.d && 4 * z.a * z.c === z.b * z.d && !(z.a * 2 === z.b && z.c * 2 === z.d); } },
      { text: 'Mal einen positiven Bruch kleiner als 1 gibt weniger. Finde trotzdem ein Produkt, das grösser als \\(\\tfrac{1}{2}\\) ist — beide Brüche kleiner als 1.', setup: auf('mal'),
        ok: function(z){ return z.m === 'mal' && z.a < z.b && z.c < z.d && 2 * z.a * z.c > z.b * z.d; } },
      { text: '«Durch»: Wie oft passt \\(\\tfrac{1}{6}\\) in \\(\\tfrac{1}{2}\\)? Stell \\(\\tfrac{1}{2} : \\tfrac{1}{6}\\) ein.', setup: auf('durch'),
        ok: function(z){ return z.m === 'durch' && z.a === 1 && z.b === 2 && z.c === 1 && z.d === 6; } },
      { text: 'Stell \\(\\tfrac{2}{3} : \\tfrac{1}{2}\\) ein. Passt \\(\\tfrac{1}{2}\\) mehr oder weniger als zweimal?', setup: auf('durch'),
        ok: function(z){ return z.m === 'durch' && z.a === 2 && z.b === 3 && z.c === 1 && z.d === 2; } },
      { text: 'Stell eine Division ein, deren Ergebnis genau 2 ist.', setup: auf('durch'),
        ok: function(z){ return z.m === 'durch' && z.a * z.d === 2 * z.b * z.c; } }
    ], sim);
    fig.querySelectorAll('input, select').forEach(function(i){ i.addEventListener('input', zeichnen); i.addEventListener('change', zeichnen); });
    zeichnen();
  })();

  /* ════════ Terme als Baum (Sim 4 und Übung «Reihenfolge») ════════
     { t:'z', b } Zahl · { t:'op', o:'+|−|·|:', l, r } · { t:'k', x } Klammer · { t:'p', x, e } Potenz.
     Die Klammern stehen im Baum, nicht in einer Vorrangregel: Was zuerst kommt, sagt der Baum. */
  function Z(z, n){ return { t: 'z', b: B(z, n) }; }
  function O(o, l, r){ return { t: 'op', o: o, l: l, r: r }; }
  function K(x){ return { t: 'k', x: x }; }
  function P(x, e){ return { t: 'p', x: x, e: e }; }
  function wertVon(k){
    if (k.t === 'z') return k.b;
    if (k.t === 'k') return wertVon(k.x);
    if (k.t === 'p') return hoch(wertVon(k.x), k.e);
    return rechne(k.o, wertVon(k.l), wertVon(k.r));
  }
  var TEXOP = { '+': '+', '−': '-', '·': '\\cdot', ':': ':' };
  function texVon(k, erst){
    if (k.t === 'z') return tb(k.b, !erst);
    if (k.t === 'x') return erst ? k.s : '\\left(' + k.s + '\\right)';   // Zwischenschritt im Lösungsweg
    if (k.t === 'k') return '\\left(' + texVon(k.x, true) + '\\right)';
    if (k.t === 'p'){ var b = k.x.t === 'z' && (k.x.b.n !== 1 || k.x.b.z < 0) ? '\\left(' + tb(k.x.b, false) + '\\right)' : texVon(k.x, true); return b + '^{' + k.e + '}'; }
    return texVon(k.l, erst) + ' ' + TEXOP[k.o] + ' ' + texVon(k.r, false);
  }
  /* Teilschritte einer einzelnen Rechnung als LaTeX, für die Lösungswege der Übungen (Prüfung 09.10.2026: «kleinschrittig»):
     + und −: gleichnamig machen → Zähler verrechnen → kürzen;  ·: Produkt → kürzen;  ':': mal Kehrwert → Produkt → kürzen. */
  function frT(z, n, kl){ return tb({ z: z, n: n }, kl); }
  function stufen(o, x, y){
    var out = [], r, roh;
    if (o === '+' || o === '−'){
      var h = kgV(x.n, y.n), z1 = x.z * h / x.n, z2 = y.z * h / y.n;
      if (h !== x.n || h !== y.n) out.push(frT(z1, h) + ' ' + TEXOP[o] + ' ' + frT(z2, h, true));
      roh = { z: o === '+' ? z1 + z2 : z1 - z2, n: h };
    } else if (o === ':'){
      var kw = B(y.n, y.z);
      out.push(tb(x) + ' \\cdot ' + tb(kw, true));
      roh = { z: x.z * kw.z, n: x.n * kw.n };
    } else if (o === '·'){
      roh = { z: x.z * y.z, n: x.n * y.n };
    } else {                                              // Potenz (nur Quadrat)
      out.push(tb(x, true) + ' \\cdot ' + tb(x, true));
      roh = { z: x.z * x.z, n: x.n * x.n };
    }
    r = B(roh.z, roh.n);
    if (roh.n !== r.n) out.push(frT(roh.z, roh.n));
    out.push(tb(r));
    return out;
  }

  function schluessel(k){
    if (k.t === 'z') return txt(k.b);
    if (k.t === 'k') return '(' + schluessel(k.x) + ')';
    if (k.t === 'p') return schluessel(k.x) + '^' + k.e;
    return schluessel(k.l) + k.o + schluessel(k.r);
  }

  /* ════════ Sim 4 — Schrittwähler: Was kommt zuerst? ════════
     Die Lernenden tippen auf das Rechenzeichen, das zuerst dran ist, und rechnen diesen Schritt
     selbst aus. Falsche Wahl → Rückmeldung zur Regel (Klammer, Potenz, Punkt vor Strich, von links
     nach rechts); falsches Teilergebnis → Rückmeldung zum Fehlertyp; nach zwei Fehlversuchen steht
     das Teilergebnis da. Jede Zeile bleibt stehen wie im Heft. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var verl = fig.querySelector('.sw-verlauf'), frage = fig.querySelector('.sw-frage'), feld = fig.querySelector('.sw-feld'), rueck = fig.querySelector('.sw-rueck');
    var AUFG = [
      function(){ return O('+', Z(1, 4), O('·', Z(2, 3), Z(3, 8))); },
      function(){ return O('−', Z(5, 6), K(O(':', Z(1, 4), Z(3, 2)))); },
      function(){ return O('·', O(':', Z(2, 3), Z(4, 9)), Z(1, 2)); },
      function(){ return O('−', P(Z(-2, 3), 2), O('·', Z(1, 3), Z(1, 2))); },
      function(){ return O('−', Z(-3, 4), O(':', K(O('−', Z(1, 2), Z(5, 4))), Z(3))); }
    ];
    var baum, zeilen, gewaehlt, versuche, nextId;
    function ids(k){ if (k.t !== 'z'){ k.id = nextId++; ['l', 'r', 'x'].forEach(function(s){ if (k[s]) ids(k[s]); }); } }
    function bereit(k){ return (k.t === 'op' && k.l.t === 'z' && k.r.t === 'z') || (k.t === 'p' && k.x.t === 'z'); }
    function html(k, erst){
      if (k.t === 'z') return hb(k.b, !erst);
      if (k.t === 'k') return '<span class="sw-kl">(</span>' + html(k.x, true) + '<span class="sw-kl">)</span>';
      if (k.t === 'p'){
        var basis = k.x.t === 'z' ? '(' + hb(k.x.b) + ')' : html(k.x, true);
        return basis + '<sup><button type="button" class="sw-op' + (gewaehlt === k ? ' aktiv' : '') + '" data-knoten="' + k.id + '" aria-label="hoch ' + k.e + '">' + k.e + '</button></sup>';
      }
      return html(k.l, erst) + ' <button type="button" class="sw-op' + (gewaehlt === k ? ' aktiv' : '') + '" data-knoten="' + k.id + '" aria-label="Rechenzeichen ' + k.o + '">' + k.o + '</button> ' + html(k.r, false);
    }
    function htmlStatisch(k, erst){ return html(k, erst).replace(/<button[^>]*>([^<]*)<\/button>/g, '<span class="sw-op-st">$1</span>'); }
    function finde(k, id){ if (k.id === id) return k; var r = null; ['l', 'r', 'x'].forEach(function(s){ if (!r && k[s]) r = finde(k[s], id); }); return r; }
    function ersetze(k, alt, neu){
      if (k === alt) return neu;
      ['l', 'r', 'x'].forEach(function(s){ if (k[s]) k[s] = ersetze(k[s], alt, neu); });
      if (k.t === 'k' && k.x.t === 'z') return k.x;            // Klammer um eine Zahl fällt weg
      return k;
    }
    function meldung(cls, h){ rueck.className = 'sw-rueck ' + cls; rueck.innerHTML = h; }
    function zeichnen(){
      var h = '';
      zeilen.forEach(function(z, i){ h += '<div class="sw-zeile"><span class="sw-term">' + (i ? '= ' : '') + z.term + '</span><span class="sw-notiz">' + (z.notiz || '') + '</span></div>'; });
      var fertig = baum.t === 'z';
      h += '<div class="sw-zeile aktuell"><span class="sw-term">' + (zeilen.length ? '= ' : '') + (fertig ? '<b class="sw-erg">' + hb(baum.b) + '</b>' : html(baum, true)) + '</span><span class="sw-notiz"></span></div>';
      verl.innerHTML = h;
      verl.querySelectorAll('.sw-op').forEach(function(b){ b.addEventListener('click', function(){ waehle(+b.dataset.knoten); }); });
      if (fertig){ frage.textContent = 'Fertig — das Ergebnis ist vollständig gekürzt.'; feld.innerHTML = ''; }
      else if (!gewaehlt){ frage.textContent = 'Tippe auf das Rechenzeichen, das zuerst dran ist.'; feld.innerHTML = ''; }
      if (pr) pr();
    }
    function warum(k){
      var kinder = k.t === 'p' ? [k.x] : [k.l, k.r];
      if (kinder.some(function(c){ return c.t === 'k'; })) return 'Zuerst die <b>Klammer</b> ausrechnen.';
      if (kinder.some(function(c){ return c.t === 'p'; })) return 'Zuerst die <b>Potenz</b> ausrechnen.';
      var c = kinder.filter(function(c){ return c.t === 'op'; })[0];
      if ((k.o === '+' || k.o === '−') && (c.o === '·' || c.o === ':')) return '<b>Punkt vor Strich:</b> Zuerst \u00ab' + c.o + '\u00bb, dann \u00ab' + k.o + '\u00bb.';
      return 'Gleichrangige Rechenarten <b>von links nach rechts</b>: Zuerst das \u00ab' + c.o + '\u00bb links.';
    }
    function waehle(id){
      var k = finde(baum, id); if (!k) return;
      if (!bereit(k)){ meldung('falsch', warum(k)); return; }
      gewaehlt = k; versuche = 0; meldung('', '');
      var links = k.t === 'p' ? '(' + hb(k.x.b) + ')<sup>' + k.e + '</sup>' : hb(k.l.b) + ' ' + k.o + ' ' + hb(k.r.b, true);
      frage.textContent = 'Richtig gewählt. Rechne diesen Schritt aus (zum Beispiel 3/4 oder -2/3):';
      feld.innerHTML = '<span class="sw-schritt">' + links + ' =</span> <input type="text" autocomplete="off" aria-label="Teilergebnis"> <button type="button" class="sw-pruefen">Prüfen</button>';
      var inp = feld.querySelector('input');
      feld.querySelector('.sw-pruefen').addEventListener('click', schritt);
      inp.addEventListener('keydown', function(ev){ if (ev.key === 'Enter') schritt(); });
      zeichnen(); setTimeout(function(){ try { inp.focus({ preventScroll: true }); } catch(e){} }, 0);
    }
    function schrittFehler(k, e){
      var r = k.t === 'p' ? hoch(k.x.b, k.e) : rechne(k.o, k.l.b, k.r.b);
      var x = k.t === 'p' ? k.x.b : k.l.b, y = k.t === 'p' ? null : k.r.b;
      if (gleich(e, { z: -r.z, n: r.n })) return 'Vorzeichen prüfen' + (k.o === '·' || k.o === ':' || k.t === 'p' ? ': Minus mal Minus gibt Plus, Minus mal Plus gibt Minus.' : '.');
      if (k.t === 'p'){ if (e.n === x.n && e.z === x.z * x.z) return 'Auch den Nenner quadrieren: \\(\\left(\\tfrac{a}{b}\\right)^2 = \\tfrac{a^2}{b^2}\\).';
        return 'Quadrieren heisst: den Bruch mit sich selbst multiplizieren.'; }
      if (k.o === '−' && y.z < 0 && gleich(e, minus(x, B(-y.z, y.n)))) return '<b>Minus einer negativen Zahl</b> heisst plus: \\(a - (-b) = a + b\\).';
      if ((k.o === '+' || k.o === '−') && x.n !== y.n && e.n === x.n + y.n) return 'Nenner nicht addieren — zuerst <b>gleichnamig</b> machen, dann die Zähler verrechnen.';
      if (k.o === '·' && gleich(e, durch(x, y))) return 'Das wäre geteilt. Mal: Zähler mal Zähler, Nenner mal Nenner.';
      if (k.o === ':' && gleich(e, mal(x, y))) return '<b>Kehrwert</b> vergessen: Durch einen Bruch teilen heisst mit seinem Kehrwert multiplizieren.';
      if (k.o === ':' && gleich(e, durch(y, x))) return 'Kehrwert vom <b>zweiten</b> Bruch nehmen, nicht vom ersten.';
      // (Die Diagnose «links minus rechts» entfiel: y − x = −r fängt schon die Vorzeichenprüfung oben ab.)
      if ((k.o === '+' || k.o === '−') && x.n === y.n) return 'Die Brüche sind schon gleichnamig: Zähler verrechnen, der Nenner bleibt. Achte auf die Vorzeichen.';
      return k.o === '+' || k.o === '−' ? 'Gleichnamig machen, dann die Zähler verrechnen. Rechne nochmals nach.' : 'Rechne nochmals nach.';
    }
    function uebernehmen(r, roh){
      var k = gewaehlt;
      var notiz = (k.t === 'p' ? '(' + hb(k.x.b) + ')<sup>' + k.e + '</sup>' : hb(k.l.b) + ' ' + k.o + ' ' + hb(k.r.b, true)) + ' = ' + (roh && roh.n !== r.n ? hb(roh) + ' = ' : '') + hb(r);
      zeilen.push({ term: htmlStatisch(baum, true), notiz: notiz });
      baum = ersetze(baum, k, { t: 'z', b: r });
      gewaehlt = null; zeichnen();
    }
    function schritt(){
      var k = gewaehlt; if (!k) return;
      var inp = feld.querySelector('input'), e = bruchLesen(inp.value);
      if (e.leer){ meldung('hinweis', 'Gib das Teilergebnis ein, zum Beispiel <code>3/4</code>.'); return; }
      if (e.gemischt){ meldung('hinweis', 'Schreib es als Bruch, zum Beispiel <code>7/3</code> statt «2 1/3».'); return; }
      if (e.kaputt){ meldung('hinweis', 'Brüche wie <code>3/4</code> oder <code>-2/3</code>, ganze Zahlen wie <code>2</code>.'); return; }
      var r = k.t === 'p' ? hoch(k.x.b, k.e) : rechne(k.o, k.l.b, k.r.b);
      if (gleich(e, r) && !e.dez){
        meldung('richtig', '✓' + (gekuerzt(e) ? '' : ' Stimmt — gekürzt: ' + hb(r) + '.'));
        uebernehmen(r, { z: e.z, n: e.n }); return;
      }
      if (gleich(e, r)){ meldung('hinweis', 'Gleicher Wert — gib ihn als Bruch an.'); return; }
      versuche++;
      if (versuche >= 2){
        meldung('falsch', schrittFehler(k, e) + ' <button type="button" class="sw-uebernehmen">Teilergebnis ' + txt(r).replace('-', '−') + ' übernehmen</button>');
        rueck.querySelector('.sw-uebernehmen').addEventListener('click', function(){ meldung('', ''); uebernehmen(r, null); });
      } else meldung('falsch', schrittFehler(k, e));
      setzen(rueck);
    }
    var aktuell = 0;
    function laden(i){ aktuell = i; nextId = 1; baum = AUFG[i](); ids(baum); zeilen = []; gewaehlt = null; meldung('', ''); feld.innerHTML = ''; }
    var sim = { zustand: function(){ return { fertig: baum.t === 'z', i: aktuell }; }, zeichnen: zeichnen,
                aufraeumen: function(){ laden(aktuell); } };
    fig.__AUFG = AUFG;                                       // Testhaken (scripts/lp/bruchrechnen/pruef-schritte.mjs)
    fig.__soll = function(){ var k = gewaehlt; return k ? txt(k.t === 'p' ? hoch(k.x.b, k.e) : rechne(k.o, k.l.b, k.r.b)) : null; };
    fig.__ergebnis = function(){ return baum.t === 'z' ? txt(baum.b) : null; };
    var pr = null;
    laden(0);
    pr = Leiste(fig, AUFG.map(function(f, i){
      var t = f();
      return { text: 'Berechne \\(' + texVon(t, true) + '\\).', setup: function(){ laden(i); }, ok: function(z){ return z.fertig && z.i === i; } };
    }), sim);
    fig.querySelector('.sw-neu').addEventListener('click', function(){ laden(aktuell); zeichnen(); });
    zeichnen();
  })();

  /* ════════ Übungen mit Rückmeldung ════════
     Jede Aufgabe würfelt neue Zahlen. Bruchfelder (Name beginnt mit «b») werden exakt verglichen:
     gleicher Wert, aber nicht vollständig gekürzt → eigener Hinweis, kein Fehlversuch; gleicher Wert
     als Dezimalzahl → «als Bruch angeben». Hinweise in drei Stufen über «💡 Tipp»: Impuls →
     nächster Schritt → Lösungsweg. Die Lösung erscheint ausserdem nach dem zweiten Fehlversuch.
     Nichts wird gespeichert. Testhaken: box.__aufgabe, box.__typ (pruef-uebungen.mjs). */
  (function(){
    var ALLE = document.querySelectorAll('.uebung[data-typ]'); if (!ALLE.length) return;
    function bz(b){ return b.n === 1 ? String(b.z) : b.z + '/' + b.n; }
    function echt(n, max){ var z; do { z = zufallG(1, max || n - 1); } while (ggT(z, n) !== 1); return z; }
    function F(z, n){ return B(z, n); }
    function gT(b, gross){ return tb(b, false, gross); }
    function chain(arr){ return arr.join(' = '); }

    /* Feste Aufgaben des Leitprogramms (Simulationen, Festhalten, Kapitelaufgaben, Vortest, Gesamttest,
       Vertiefung): Kein Wurf darf eine davon stellen. Schlüssel je Typ, kommutative Rechnungen sortiert. */
    var SPERRE = [
      // erweitern: er|a/b|N
      'er|3/4|8', 'er|3/4|20', 'er|5/6|24', 'er|2/3|12', 'er|5/6|12', 'er|3/4|12', 'er|1/2|6', 'er|1/3|6',
      // kürzen: kz|Z/N
      'kz|12/18', 'kz|45/60', 'kz|84/126', 'kz|6/8', 'kz|10/15', 'kz|14/35', 'kz|6/15', 'kz|8/12', 'kz|9/12', 'kz|6/12', 'kz|15/20', 'kz|4/10', 'kz|10/25', 'kz|3/6',
      // hauptnenner: hn|b|d (sortiert)
      'hn|2|3', 'hn|4|6', 'hn|6|8', 'hn|6|9', 'hn|12|18', 'hn|4|8', 'hn|9|12', 'hn|3|4', 'hn|6|15',
      // addieren/subtrahieren: as|o|x|y
      'as|+|1/2|1/3', 'as|+|1/6|3/4', 'as|−|7/8|1/6', 'as|+|1/6|2/9', 'as|+|5/12|7/18', 'as|+|1/3|1/6', 'as|+|3/4|5/6', 'as|−|11/12|4/9',
      'as|+|1/4|2/3', 'as|+|1/8|3/8', 'as|−|7/10|3/10', 'as|+|5/6|7/15', 'as|−|3|5/7', 'as|−|2|3/4', 'as|−|9/10|1/2', 'as|+|1/2|1/4',
      // mal: ml|x|y (sortiert)
      'ml|2/3|3/4', 'ml|3/8|4/9', 'ml|3/10|5/6', 'ml|2/5|3/4', 'ml|7/12|9/14', 'ml|4|5/6', 'ml|2/5|3', 'ml|12|2/3', 'ml|15|2/3', 'ml|1/2|1/3', 'ml|1/2|1/2', 'ml|1/3|1/2',
      // durch: dv|x|y
      'dv|3/4|1/8', 'dv|3/4|1/2', 'dv|3/5|9/10', 'dv|7/8|7', 'dv|6|3/4', 'dv|2/5|4/7', 'dv|3/4|2/3', 'dv|3/2|1/4', 'dv|1/4|3/2', 'dv|2/3|4/9', 'dv|5/12|5/6', 'dv|3/8|3/8',
      'dv|4/9|8/9', 'dv|3/4|3/8',
      // vorzeichen: vz|Term
      'vz|-2/9·-3/4', 'vz|-2/5+-2/5', 'vz|-3/2^2', 'vz|-2/3^2', 'vz|2/3:-4/9', 'vz|-2/3·-3/4', 'vz|-1/2--1/4', 'vz|1/2−--1/4',
      // reihenfolge: rf|Term
      'rf|1/4+2/3·3/8', 'rf|5/6−(1/4:3/2)', 'rf|2/3:4/9·1/2', 'rf|7/12−1/4·2/3', 'rf|(3/4−1/3):5/6', 'rf|3/4:3/8·1/2', 'rf|3/4−1/2·(5/6−1/3)',
      'rf|1/3+1/6·4', 'rf|1/2−1/3·(3/4−1/4)', 'rf|3/4−(1/2−1/4)', 'rf|1:1/2·1/2', 'rf|9/14·7/12:3/8', 'rf|7/15+5/6−1/2',
      // Erkundungen und Clips (09.10.2026, mit den Clips)
      'er|3/5|10', 'er|3/5|20', 'er|1/3|24', 'er|3/8|24', 'er|2/7|21', 'er|2/3|12', 'kz|10/16', 'kz|18/24', 'kz|6/9', 'kz|4/6', 'kz|8/10', 'kz|6/20', 'kz|3/12',
      'hn|3|5', 'hn|8|12', 'hn|4|5', 'hn|4|6', 'hn|6|8', 'hn|6|9', 'hn|3|4',
      'as|+|1/4|1/6', 'as|+|1/6|3/8', 'as|−|7/9|1/6', 'as|+|1/3|2/5', 'as|+|1/10|3/10', 'as|+|1/4|1/5', 'as|−|5/6|1/4', 'as|+|1/3|1/4',
      'ml|2/3|3/5', 'ml|2/5|3/4', 'ml|1/3|3/4', 'ml|2/7|5', 'ml|2/3|2/3', 'ml|3/4|3/4',
      'dv|1/2|1/6', 'dv|2/3|1/2', 'dv|4/5|2/3', 'dv|2/3|1/6', 'dv|1/2|1/3',
      'vz|-2/5·-5/6', 'vz|-1/2^2', 'vz|-3/4^2',
      'rf|2/5+3/5·1/3', 'rf|3/4:1/4·1/3', 'rf|2/3−(1/2−1/6)',
      // Nachprüfung 09.10.2026: Teilschritte fester Aufgaben, neue Aufgaben (2a, 2f, 2g, 3e, 3g, 4f, G1, G3, G4, G6, G7)
      'er|3/4|16', 'er|3/4|24', 'er|5/8|24', 'er|2/3|24', 'er|5/6|36', 'er|7/9|36', 'er|3/4|36', 'er|1/2|12', 'er|2/3|12', 'er|3/4|12',
      'kz|4/8', 'kz|6/10', 'kz|21/28', 'kz|15/20', 'kz|6/12', 'kz|15/30', 'kz|10/12',
      'hn|12|18', 'hn|9|12', 'hn|3|5', 'hn|2|3', 'hn|4|6', 'hn|6|15',
      'as|+|1/12|5/12', 'as|−|9/10|3/10', 'as|+|2/15|4/15', 'as|+|1/3|1/5', 'as|+|1/2|2/3', 'as|−|7/6|3/4', 'as|−|3/4|1/3',
      'as|−|5/6|1/3', 'as|−|13/10|1/2', 'as|−|7/9|3/4', 'as|+|1/8|3/8', 'as|−|7/12|1/6',
      'ml|1/4|2/3', 'ml|1/6|4', 'ml|1/2|3/4', 'ml|3/5|5/6', 'ml|2/5|5/4', 'ml|7/12|9/14', 'ml|9/16|8/9', 'ml|1/2|4/5',
      'dv|3/8|3/4', 'dv|9/16|9/8', 'dv|5/6|3/5', 'dv|5/4|3/8', 'dv|4/5|2',
      'rf|9/14·7/12:3/4', 'rf|(5/6−1/3)·3/4+1/8', 'rf|1/2+2/3−3/4'
    ];
    function gesperrt(T, A){ return T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }
    window.__SPERRE = SPERRE;                                  // Testhaken (pruef-schritte.mjs: Verteilung)
    function sortiert(a, b){ return [a, b].sort().join('|'); }

    /* Grösster Hauptnenner, den ein Term beim Ausrechnen in einem Plus- oder Minus-Schritt braucht. */
    function hnMax(k){
      var m = 0;
      (function w(n){
        if (n.t === 'z') return n.b;
        if (n.t === 'k') return w(n.x);
        if (n.t === 'p') return hoch(w(n.x), n.e);
        var a = w(n.l), b = w(n.r);
        if (n.o === '+' || n.o === '−') m = Math.max(m, kgV(a.n, b.n));
        return rechne(n.o, a, b);
      })(k);
      return m;
    }
    /* Lösungsweg eines Terms: Schritt für Schritt, jede Rechnung mit ihren Teilschritten (stufen). */
    function weg(t0){
      var k = [texVon(t0, true)], t = JSON.parse(JSON.stringify(t0));
      function schritt(n){                                  // innerster bereiter Knoten, links zuerst
        if (n.t === 'z') return null;
        if (n.t === 'k') return schritt(n.x);
        if (n.t === 'p') return n.x.t === 'z' ? n : schritt(n.x);
        var a = schritt(n.l); if (a) return a;
        var b = schritt(n.r); if (b) return b;
        return n.l.t === 'z' && n.r.t === 'z' ? n : null;
      }
      function ers(n, alt, neu){ if (n === alt) return neu; ['l', 'r', 'x'].forEach(function(s_){ if (n[s_]) n[s_] = ers(n[s_], alt, neu); }); if (n.t === 'k' && n.x.t === 'z') return n.x; return n; }
      for (var i = 0; i < 12 && t.t !== 'z'; i++){
        var s = schritt(t); if (!s) break;
        var teil = s.t === 'p' ? stufen('^', s.x.b) : stufen(s.o, s.l.b, s.r.b), alt = s.t;
        teil.slice(0, -1).forEach(function(m){ s.t = 'x'; s.s = m; k.push(texVon(t, true)); s.t = alt; });
        t = ers(t, s, { t: 'z', b: s.t === 'p' ? hoch(s.x.b, s.e) : rechne(s.o, s.l.b, s.r.b) });
        k.push(texVon(t, true));
      }
      return chain(k);
    }

    var TYPEN = {
      /* ── Kapitel 1 ─────────────────────────────────────────────── */
      'erweitern': { felder: ['x'],
        schl: function(A){ return 'er|' + A.a + '/' + A.b + '|' + A.N; },
        neu: function(){
          var b = zufallG(2, 12), a = echt(b), f = zufallG(2, 8);
          if (b * f > 72) f = Math.max(2, Math.floor(72 / b));
          var art = Math.random() < 0.7 ? 'z' : 'n', N = b * f;
          return { a: a, b: b, f: f, N: N, art: art, x: art === 'z' ? a * f : N,
            muster: '\\(\\square = \\) {x}',
            text: art === 'z' ? 'Erweitere \\(' + gT(F(a, b), true) + '\\) auf den Nenner \\(' + N + '\\): \\(\\;' + gT(F(a, b), true) + ' = \\dfrac{\\square}{' + N + '}\\)'
                              : 'Ergänze: \\(\\;' + gT(F(a, b), true) + ' = \\dfrac{' + a * f + '}{\\square}\\)' }; },
        fehler: function(A){ return [[{ x: String(A.art === 'z' ? A.a + A.N - A.b : A.b + A.a * A.f - A.a) }, 'multiplizieren']]; },
        pruefen: function(A, e){
          var add = A.art === 'z' ? A.a + A.N - A.b : A.b + A.a * A.f - A.a;
          if (e.x === add) return 'Erweitern heisst <b>multiplizieren</b>, nicht addieren: Zähler und Nenner mit derselben Zahl malnehmen.';
          return A.art === 'z' ? 'Mit welcher Zahl wurde der Nenner \\(' + A.b + '\\) multipliziert, damit \\(' + A.N + '\\) herauskommt? Mit derselben Zahl auch den Zähler.'
                               : 'Mit welcher Zahl wurde der Zähler \\(' + A.a + '\\) multipliziert? Mit derselben Zahl auch den Nenner.'; },
        tipps: function(A){ return ['Der Wert bleibt gleich, wenn du Zähler <b>und</b> Nenner mit derselben Zahl multiplizierst.',
          A.art === 'z' ? '\\(' + A.b + ' \\cdot \\square = ' + A.N + '\\), also ist der Faktor \\(' + A.f + '\\).' : '\\(' + A.a + ' \\cdot \\square = ' + A.a * A.f + '\\), also ist der Faktor \\(' + A.f + '\\).']; },
        loesung: function(A){ return gT(F(A.a, A.b), true) + ' = \\dfrac{' + A.a + ' \\cdot ' + A.f + '}{' + A.b + ' \\cdot ' + A.f + '} = \\dfrac{' + A.a * A.f + '}{' + A.N + '}'; } },

      'kuerzen': { felder: ['b'],
        schl: function(A){ return 'kz|' + A.Z + '/' + A.N; },
        eingabe: function(A){ return { b: bz(A.r) }; },
        neu: function(){
          var q = zufallG(2, 12), p; do { p = zufallG(1, 2 * q); } while (ggT(p, q) !== 1 || p === q);
          var g = Math.random() < 0.8 ? zufall([4, 6, 8, 9, 10, 12, 14, 15, 16, 18]) : zufall([2, 3, 5, 7]);
          while (p * g > 150 || q * g > 150) g = Math.max(2, g - 2);
          var Zz = p * g, N = q * g;
          return { p: p, q: q, g: g, Z: Zz, N: N, r: B(p, q), muster: '\\(\\dfrac{' + Zz + '}{' + N + '} = \\) {b}',
            text: 'Kürze vollständig.' }; },
        fehler: function(A){
          var f = [[{ b: (A.p + 1) + '/' + A.q }, null]];
          for (var d = 2; d < A.g; d++) if (A.g % d === 0){ f.push([{ b: (A.Z / d) + '/' + (A.N / d) }, 'gekürzt']); break; }
          return f; },
        pruefen: function(A, e){
          if (e.b.n < A.N && e.b.z < A.Z && e.b.n - e.b.z === A.N - A.Z) return 'Kürzen heisst <b>dividieren</b>: Zähler und Nenner durch dieselbe Zahl teilen, nicht etwas abziehen.';
          return 'Der Wert hat sich verändert. Teile Zähler und Nenner durch <b>dieselbe</b> Zahl.'; },
        tipps: function(A){ return ['Suche eine Zahl, durch die \\(' + A.Z + '\\) und \\(' + A.N + '\\) beide teilbar sind — am besten die grösste.',
          'Der grösste gemeinsame Teiler ist \\(\\text{ggT}(' + A.Z + ';\\ ' + A.N + ') = ' + A.g + '\\).']; },
        loesung: function(A){ return '\\dfrac{' + A.Z + '}{' + A.N + '} = \\dfrac{' + A.Z + ' : ' + A.g + '}{' + A.N + ' : ' + A.g + '} = ' + gT(A.r, true); } },

      /* ── Kapitel 2 ─────────────────────────────────────────────── */
      'hauptnenner': { felder: ['h'],
        schl: function(A){ return 'hn|' + Math.min(A.b, A.d) + '|' + Math.max(A.b, A.d); },
        neu: function(){
          var b, d, h;
          do { b = zufallG(2, 15); d = zufallG(2, 18); h = kgV(b, d); }
          while (b === d || h > 72 || b % d === 0 || d % b === 0 && Math.random() < 0.6 || (h === b * d && Math.random() < 0.65));
          var a = echt(b), c = echt(d);
          return { a: a, b: b, c: c, d: d, h: h, muster: 'Hauptnenner: {h}',
            text: 'Bestimme den Hauptnenner von \\(' + gT(F(a, b), true) + '\\) und \\(' + gT(F(c, d), true) + '\\).' }; },
        fehler: function(A){ var f = [[{ h: String(A.h + 1) }, 'aufgehen']]; if (A.b * A.d !== A.h) f.push([{ h: String(A.b * A.d) }, 'kleinste']); return f; },
        pruefen: function(A, e){
          if (e.h > 0 && e.h % A.b === 0 && e.h % A.d === 0) return 'Ein gemeinsamer Nenner ist \\(' + e.h + '\\) schon — aber nicht der <b>kleinste</b>. Gesucht ist das kleinste gemeinsame Vielfache.';
          return '\\(' + e.h + '\\) geht nicht: Beide Nenner \\(' + A.b + '\\) und \\(' + A.d + '\\) müssen im Hauptnenner <b>aufgehen</b>.'; },
        tipps: function(A){ var m = Math.max(A.b, A.d), k = Math.min(A.b, A.d), v = [];
          for (var i = 1; i <= 3; i++) v.push(m * i);         // nur der Anfang: Die Liste soll nicht vor dem kgV abbrechen
          return ['Zähle die Vielfachen des grösseren Nenners auf, bis eines durch den kleineren teilbar ist.',
            'Vielfache von \\(' + m + '\\): \\(' + v.join(';\\ ') + ';\\ \\ldots\\) — zähl weiter, bis eines durch \\(' + k + '\\) teilbar ist.']; },
        loesung: function(A){ return '\\text{kgV}(' + A.b + ';\\ ' + A.d + ') = ' + A.h; } },

      'addsub': { felder: ['b'],
        schl: function(A){ var x = bz(A.x), y = bz(A.y); return 'as|' + A.o + '|' + (A.o === '+' ? sortiert(x, y) : x + '|' + y); },
        eingabe: function(A){ return { b: bz(A.r) }; },
        neu: function(){
          var o = Math.random() < 0.5 ? '+' : '−', x, y, r, h;
          for (;;){
            if (Math.random() < 0.12){ x = B(zufallG(1, 4)); var d0 = zufallG(2, 9); y = B(echt(d0), d0); }
            else { var b = zufallG(2, 12), d = zufallG(2, 12); if (b === d && Math.random() < 0.7) continue; x = B(echt(b, Math.min(b * 2, 20)), b); y = B(echt(d, Math.min(d * 2, 20)), d); }
            if (o === '−' && !(x.z * y.n > y.z * x.n)){ var t = x; x = y; y = t; }
            r = rechne(o, x, y); h = kgV(x.n, y.n);
            // Sonderwert (Prüfung 09.10.2026): 2/3 − 1/2 ergäbe auch mit nicht erweiterten Zählern (2 − 1)/6 = 1/6 — verwerfen.
            var nichtErw = { z: o === '+' ? x.z + y.z : x.z - y.z, n: h };
            if (!gleich(x, y) && h <= 48 && r.z > 0 && Math.abs(r.z) <= 60 && (x.n === y.n || !gleich(nichtErw, r))) break;
          }
          return { x: x, y: y, o: o, r: r, h: h, muster: '\\(' + gT(x, true) + ' ' + TEXOP[o] + ' ' + gT(y, true) + ' = \\) {b}',
            text: 'Berechne und kürze vollständig.' }; },
        falsche: function(A){
          var f = [], x = A.x, y = A.y, s = A.o === '+' ? 1 : -1;
          if (x.n !== y.n && x.n + s * y.n > 0) f.push([{ z: x.z + s * y.z, n: x.n + s * y.n }, 'gleichnamig']);
          if (A.o === '−') f.push([minus(y, x), 'Reihenfolge']);
          if (x.n !== y.n) f.push([{ z: x.z + s * y.z, n: A.h }, 'Zähler']);
          // Fallen derselbe falsche Wert aus zwei Fehlern, zählt die erste Diagnose (1 − 5/9: «−4/9»).
          return f.filter(function(p, i){ return p[0].z !== 0 && !gleich(p[0], A.r) && !f.slice(0, i).some(function(q){ return gleich(q[0], p[0]); }); }); },
        fehler: function(A){
          var f = TYPEN.addsub.falsche(A).map(function(p){ return [{ b: bz(p[0]) }, p[1]]; });
          if (A.r.n * 2 <= 96) f.push([{ b: (A.r.z * 2) + '/' + (A.r.n * 2) }, 'gekürzt']);
          return f; },
        pruefen: function(A, e){
          var f = TYPEN.addsub.falsche(A);
          for (var i = 0; i < f.length; i++) if (gleich(e.b, f[i][0])){
            if (f[i][1] === 'gleichnamig') return (A.o === '+' ? 'Zähler plus Zähler und Nenner plus Nenner' : 'Zähler minus Zähler und Nenner minus Nenner') + ' geht nicht: Die Stücke sind verschieden gross. Zuerst <b>gleichnamig</b> machen.';
            if (f[i][1] === 'Zähler') return 'Der Hauptnenner \\(' + A.h + '\\) stimmt. Beim Erweitern wird aber auch der <b>Zähler</b> multipliziert.';
            if (f[i][1] === 'Reihenfolge') return 'Vorzeichen falsch: Rechne «erster Bruch minus zweiter» — die <b>Reihenfolge</b> zählt beim Subtrahieren.';
          }
          return 'Erweitere beide Brüche auf den Hauptnenner \\(' + A.h + '\\), verrechne die Zähler und kürze. Rechne nochmals nach.'; },
        tipps: function(A){ return ['Zuerst gleichnamig machen: Der Hauptnenner ist das kgV der Nenner.',
          'Hauptnenner \\(' + A.h + '\\): \\(' + gT(A.x) + ' = \\tfrac{' + A.x.z * A.h / A.x.n + '}{' + A.h + '}\\) und \\(' + gT(A.y) + ' = \\tfrac{' + A.y.z * A.h / A.y.n + '}{' + A.h + '}\\).']; },
        loesung: function(A){
          var z1 = A.x.z * A.h / A.x.n, z2 = A.y.z * A.h / A.y.n, roh = A.o === '+' ? z1 + z2 : z1 - z2;
          var k = [gT(A.x) + ' ' + TEXOP[A.o] + ' ' + gT(A.y), '\\tfrac{' + z1 + '}{' + A.h + '} ' + TEXOP[A.o] + ' \\tfrac{' + z2 + '}{' + A.h + '}', '\\tfrac{' + roh + '}{' + A.h + '}'];
          if (A.r.n !== A.h) k.push(gT(A.r));
          return chain(k); } },

      /* ── Kapitel 3 ─────────────────────────────────────────────── */
      'mal': { felder: ['b'],
        schl: function(A){ return 'ml|' + sortiert(bz(A.x), bz(A.y)); },
        eingabe: function(A){ return { b: bz(A.r) }; },
        neu: function(){
          var x, y, r;
          for (;;){
            if (Math.random() < 0.2){ x = B(zufallG(2, 9)); var d = zufallG(3, 12); y = B(echt(d), d); if (Math.random() < 0.5){ var t = x; x = y; y = t; } }
            else {
              var b = zufallG(2, 12), dd = zufallG(2, 12);
              x = B(echt(b, Math.min(2 * b, 15)), b); y = B(echt(dd, Math.min(2 * dd, 15)), dd);
              if (Math.random() < 0.7 && ggT(x.z, y.n) === 1 && ggT(y.z, x.n) === 1) continue;   // meist mit Kürzen über Kreuz
            }
            r = mal(x, y);
            if (r.n <= 60 && r.z <= 60 && !(r.n === 1 && r.z === 1) && !(x.n === 1 && y.n === 1)) break;
          }
          return { x: x, y: y, r: r, muster: '\\(' + gT(x, true) + ' \\cdot ' + gT(y, true) + ' = \\) {b}',
            text: 'Berechne und kürze vollständig.' }; },
        falsche: function(A){
          var f = [[durch(A.x, A.y), 'geteilt']];
          if (A.x.n === 1) f.push([{ z: A.x.z * A.y.z, n: A.x.z * A.y.n }, 'Nur den Zähler']);
          if (A.y.n === 1) f.push([{ z: A.x.z * A.y.z, n: A.x.n * A.y.z }, 'Nur den Zähler']);
          return f.filter(function(p){ return !gleich(p[0], A.r); }); },
        fehler: function(A){
          var f = TYPEN.mal.falsche(A).map(function(p){ return [{ b: p[0].z + '/' + p[0].n }, p[1]]; });
          var rz = A.x.z * A.y.z, rn = A.x.n * A.y.n;
          if (ggT(rz, rn) > 1) f.push([{ b: rz + '/' + rn }, 'gekürzt']);
          return f; },
        pruefen: function(A, e){
          var f = TYPEN.mal.falsche(A);
          for (var i = 0; i < f.length; i++) if (gleich(e.b, f[i][0])){
            if (f[i][1] === 'geteilt') return 'Das wäre <b>geteilt</b> (mit dem Kehrwert multipliziert). Mal: Zähler mal Zähler, Nenner mal Nenner.';
            return 'Nur den Zähler mit der ganzen Zahl multiplizieren: \\(n \\cdot \\tfrac{a}{b} = \\tfrac{n \\cdot a}{b}\\). Wer auch den Nenner mitnimmt, hat nur erweitert.';
          }
          return 'Zähler mal Zähler, Nenner mal Nenner — und kürzen. Rechne nochmals nach.'; },
        tipps: function(A){
          var g1 = ggT(A.x.z, A.y.n), g2 = ggT(A.y.z, A.x.n);
          return ['Zähler mal Zähler, Nenner mal Nenner. Kürze am besten <b>vor</b> dem Ausrechnen.',
            g1 > 1 || g2 > 1 ? 'Über Kreuz kürzen: ' + (g1 > 1 ? '\\(' + A.x.z + '\\) und \\(' + A.y.n + '\\) durch \\(' + g1 + '\\)' : '') + (g1 > 1 && g2 > 1 ? '; ' : '') + (g2 > 1 ? '\\(' + A.y.z + '\\) und \\(' + A.x.n + '\\) durch \\(' + g2 + '\\)' : '') + '.'
                             : 'Hier lässt sich nicht über Kreuz kürzen: \\(\\tfrac{' + A.x.z + ' \\cdot ' + A.y.z + '}{' + A.x.n + ' \\cdot ' + A.y.n + '}\\) ausrechnen und am Schluss kürzen.']; },
        loesung: function(A){
          // wie Tipp und Festhalten: zuerst über Kreuz kürzen, dann multiplizieren
          var g1 = ggT(A.x.z, A.y.n), g2 = ggT(A.y.z, A.x.n);
          var k = [gT(A.x) + ' \\cdot ' + gT(A.y), '\\tfrac{' + A.x.z + ' \\cdot ' + A.y.z + '}{' + A.x.n + ' \\cdot ' + A.y.n + '}'];
          if (g1 > 1 || g2 > 1) k.push('\\tfrac{' + A.x.z / g1 + ' \\cdot ' + A.y.z / g2 + '}{' + A.x.n / g2 + ' \\cdot ' + A.y.n / g1 + '}');
          var roh = { z: (A.x.z / g1) * (A.y.z / g2), n: (A.x.n / g2) * (A.y.n / g1) };
          if (roh.n !== A.r.n) k.push('\\tfrac{' + roh.z + '}{' + roh.n + '}');
          k.push(gT(A.r));
          return chain(k); } },

      'durch': { felder: ['b'],
        schl: function(A){ return 'dv|' + bz(A.x) + '|' + bz(A.y); },
        eingabe: function(A){ return { b: bz(A.r) }; },
        neu: function(){
          var x, y, r, art = Math.random();
          do {
            if (art < 0.15){ x = B(zufallG(2, 9)); var d = zufallG(2, 10); y = B(echt(d, Math.min(2 * d, 12)), d); }
            else if (art < 0.3){ var b = zufallG(2, 12); x = B(echt(b, Math.min(2 * b, 15)), b); y = B(zufallG(2, 6)); }
            else { var b2 = zufallG(2, 12), d2 = zufallG(2, 12); x = B(echt(b2, Math.min(2 * b2, 15)), b2); y = B(echt(d2, Math.min(2 * d2, 15)), d2); }
            r = durch(x, y);
          } while (gleich(x, y) || y.z === y.n || r.n > 60 || r.z > 60 || x.z === x.n || gleich(mal(x, y), r) || gleich(durch(y, x), mal(x, y)));
          return { x: x, y: y, r: r, muster: '\\(' + gT(x, true) + ' : ' + gT(y, true) + ' = \\) {b}',
            text: 'Berechne und kürze vollständig.' }; },
        falsche: function(A){
          return [[mal(A.x, A.y), 'Kehrwert'], [durch(A.y, A.x), 'zweiten']].filter(function(p){ return !gleich(p[0], A.r); }); },
        fehler: function(A){ return TYPEN.durch.falsche(A).map(function(p){ return [{ b: bz(p[0]) }, p[1]]; }); },
        pruefen: function(A, e){
          var f = TYPEN.durch.falsche(A);
          for (var i = 0; i < f.length; i++) if (gleich(e.b, f[i][0]))
            return f[i][1] === 'Kehrwert' ? '<b>Kehrwert</b> vergessen: Durch einen Bruch teilen heisst mit seinem Kehrwert multiplizieren.'
                                          : 'Den Kehrwert vom <b>zweiten</b> Bruch nehmen (dem, durch den du teilst), nicht vom ersten.';
          return 'Mit dem Kehrwert des zweiten Bruchs multiplizieren, dann kürzen. Rechne nochmals nach.'; },
        tipps: function(A){ var k = B(A.y.n, A.y.z);
          return ['Teilen durch einen Bruch heisst: mit seinem <b>Kehrwert</b> multiplizieren.',
            'Der Kehrwert von \\(' + gT(A.y) + '\\) ist \\(' + gT(k) + '\\): Rechne \\(' + gT(A.x) + ' \\cdot ' + gT(k) + '\\).']; },
        loesung: function(A){ var k = B(A.y.n, A.y.z), roh = { z: A.x.z * k.z, n: A.x.n * k.n };
          var c = [gT(A.x) + ' : ' + gT(A.y), gT(A.x) + ' \\cdot ' + gT(k), roh.n === 1 ? String(roh.z) : '\\tfrac{' + roh.z + '}{' + roh.n + '}'];
          if (roh.n !== A.r.n) c.push(gT(A.r));
          return chain(c); } },

      /* ── Kapitel 4 ─────────────────────────────────────────────── */
      'reihenfolge': { felder: ['b'],
        // (hnMax und weg stehen vor TYPEN)
        schl: function(A){ return 'rf|' + schluessel(A.t); },
        eingabe: function(A){ return { b: bz(A.r) }; },
        neu: function(){
          var NN = [2, 3, 4, 5, 6, 8, 9, 10, 12];
          function q(){ var n = zufall(NN); return Z(echt(n, Math.min(n + 2, 2 * n - 1)), n); }
          var t, r, w, regel, form;
          for (var v = 0; v < 400; v++){
            form = zufallG(1, 6);
            var x = q(), y = q(), z = q(), s = zufall(['+', '−']), p = zufall(['·', ':']), s2 = zufall(['+', '−']);
            if (form === 1){ t = O(s, x, O(p, y, z)); w = rechne(p, rechne(s, x.b, y.b), z.b); regel = 'Punkt vor Strich'; }
            else if (form === 2){ t = O(s, O(p, x, y), z); w = rechne(p, x.b, rechne(s, y.b, z.b)); regel = 'Punkt vor Strich'; }
            else if (form === 3){ t = O(p, K(O(s, x, y)), z); w = rechne(s, x.b, rechne(p, y.b, z.b)); regel = 'Klammer'; }
            else if (form === 4){ t = O('−', x, K(O(s2, y, z)));                 // Fehler: Minus nur aufs erste Glied
              w = rechne(s2, minus(x.b, y.b), z.b); regel = 'Minus vor der Klammer'; }
            else if (form === 5){ t = O('·', O(':', x, y), z); w = durch(x.b, mal(y.b, z.b)); regel = 'links nach rechts'; }
            else { t = O('+', O('−', x, y), z); w = minus(x.b, plus(y.b, z.b)); regel = 'links nach rechts'; }
            r = wertVon(t);
            if (r.n > 36 || Math.abs(r.z) > 40 || r.z === 0 || w.n === 0 || gleich(w, r) || w.n > 200) continue;
            if (hnMax(t) > 48) continue;                       // auch kein Zwischenschritt mit Hauptnenner über 48 (Prüfung 09.10.2026)
            if (SPERRE.indexOf('rf|' + schluessel(t)) >= 0) continue;
            break;
          }
          return { t: t, r: r, w: w, regel: regel, muster: '\\(' + texVon(t, true) + ' = \\) {b}',
            text: 'Berechne in der richtigen Reihenfolge und kürze vollständig.' }; },
        fehler: function(A){ return [[{ b: bz(A.w) }, A.regel === 'Minus vor der Klammer' ? 'Minus' : A.regel === 'Klammer' ? 'Klammer' : A.regel]]; },
        pruefen: function(A, e){
          if (gleich(e.b, A.w)){
            if (A.regel === 'Punkt vor Strich') return '<b>Punkt vor Strich:</b> Zuerst · oder :, dann + oder −.';
            if (A.regel === 'Klammer') return 'Die <b>Klammer</b> kommt zuerst — auch vor Punkt vor Strich.';
            if (A.regel === 'Minus vor der Klammer') return '<b>Minus</b> vor der Klammer: Rechne die Klammer zuerst aus — oder dreh beim Weglassen beide Vorzeichen in der Klammer.';
            return 'Gleichrangige Rechenarten <b>von links nach rechts</b>.';
          }
          return 'Arbeite Schritt für Schritt: Klammer, Potenz, Punkt vor Strich, sonst von links nach rechts. Rechne nochmals nach.'; },
        tipps: function(A){ return ['Was kommt zuerst? Klammern, dann Potenzen, dann Punkt vor Strich, sonst von links nach rechts.',
          'Hier gilt besonders: ' + (A.regel === 'Minus vor der Klammer' ? 'zuerst die Klammer ausrechnen.' : A.regel === 'Klammer' ? 'die Klammer zuerst.' : A.regel === 'Punkt vor Strich' ? 'Punkt vor Strich.' : 'von links nach rechts.')]; },
        loesung: function(A){ return weg(A.t); } },

      'vorzeichen': { felder: ['b'],
        schl: function(A){ return 'vz|' + A.k; },
        eingabe: function(A){ return { b: bz(A.r) }; },
        neu: function(){
          var NN = [2, 3, 4, 5, 6, 8, 9, 10];
          function q(){ var n = zufall(NN); return B(echt(n, Math.min(n + 2, 2 * n - 1)), n); }
          var x, y, art, r, w, tex, k, msg;
          for (var v = 0; v < 400; v++){
            x = q(); y = q(); art = zufallG(1, 5);
            if (art === 1){ var sx = zufall([-1, 1]), sy = sx === 1 ? -1 : zufall([-1, 1]); x = B(sx * x.z, x.n); y = B(sy * y.z, y.n);
              r = mal(x, y); w = B(-r.z, r.n); tex = tb(x, false) + ' \\cdot ' + tb(y, true); k = [txt(x), txt(y)].sort().join('·'); msg = 'mal'; }   // sortiert: Produkt in beiden Reihenfolgen gesperrt
            else if (art === 2){ var sx2 = zufall([-1, 1]), sy2 = sx2 === 1 ? -1 : zufall([-1, 1]); x = B(sx2 * x.z, x.n); y = B(sy2 * y.z, y.n);
              r = durch(x, y); w = B(-r.z, r.n); tex = tb(x, false) + ' : ' + tb(y, true); k = txt(x) + ':' + txt(y); msg = 'mal'; }
            else if (art === 3){ x = B(-x.z, x.n); r = plus(x, y); w = B(-r.z, r.n); tex = tb(x, false) + ' + ' + tb(y, false); k = txt(x) + '+' + txt(y); msg = 'plus'; }
            else if (art === 4){ r = minus(x, B(-y.z, y.n)); w = minus(x, y); tex = tb(x, false) + ' - ' + tb(B(-y.z, y.n), true); k = txt(x) + '−-' + txt(y); msg = 'minusminus'; }
            else { x = B(-x.z, x.n); r = hoch(x, 2); w = B(-r.z, r.n); tex = '\\left(' + tb(x, false) + '\\right)^2'; k = txt(x) + '^2'; msg = 'quadrat'; }
            if (r.z === 0 || gleich(r, w) || r.n > 60 || Math.abs(r.z) > 60) continue;
            if (SPERRE.indexOf('vz|' + k) >= 0) continue;
            break;
          }
          return { x: x, y: y, art: art, r: r, w: w, k: k, msg: msg, tex: tex, muster: '\\(' + tex + ' = \\) {b}',
            text: 'Berechne und kürze vollständig.' }; },
        fehler: function(A){ return [[{ b: bz(A.w) }, A.msg === 'minusminus' ? 'Minus' : 'Vorzeichen']]; },
        pruefen: function(A, e){
          if (gleich(e.b, A.w)){
            if (A.msg === 'minusminus') return '<b>Minus</b> einer negativen Zahl heisst plus: \\(a - (-b) = a + b\\).';
            if (A.msg === 'quadrat') return '<b>Vorzeichen:</b> Das Quadrat einer negativen Zahl ist positiv — Minus mal Minus gibt Plus.';
            if (A.msg === 'plus') return '<b>Vorzeichen:</b> Bei verschiedenen Vorzeichen gewinnt das der Zahl mit dem grösseren Betrag.';
            return '<b>Vorzeichen:</b> Gleiche Vorzeichen geben Plus, verschiedene Minus — wie in ℤ.';
          }
          return 'Zuerst das Vorzeichen bestimmen, dann mit den Beträgen rechnen und kürzen.'; },
        tipps: function(A){ return ['Rechne mit den Beträgen wie mit positiven Brüchen und bestimme das Vorzeichen getrennt — nach den Regeln aus ℤ.',
          A.msg === 'minusminus' ? 'Aus «minus minus» wird plus: \\(' + tb(A.x) + ' + ' + tb(A.y) + '\\).' : A.msg === 'plus' ? 'Gleichnamig machen; das Ergebnis hat das Vorzeichen der Zahl mit dem grösseren Betrag.' : A.msg === 'quadrat' ? 'Quadrat: mit sich selbst multiplizieren — Minus mal Minus.' : 'Vorzeichen des Ergebnisses: ' + (A.r.z > 0 ? 'plus' : 'minus') + '.']; },
        loesung: function(A){
          var t = A.art === 1 ? stufen('·', A.x, A.y) : A.art === 2 ? stufen(':', A.x, A.y) : A.art === 3 ? stufen('+', A.x, A.y)
                : A.art === 4 ? [tb(A.x) + ' + ' + tb(A.y)].concat(stufen('+', A.x, A.y)) : stufen('^', A.x);
          return [A.tex].concat(t).join(' = '); } }
    };
    window.__TYPEN = TYPEN;

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
          html = html.replace('{' + f + '}', '<input type="text" inputmode="text" autocomplete="off" aria-label="' + (f[0] === 'b' ? 'Ergebnis als Bruch' : 'Zahl') + '" data-f="' + f + '"' + (f[0] === 'b' ? ' class="bruch" placeholder="z. B. 3/4"' : '') + '>');
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
        var e = {}, komma = false;
        var felder = ein.querySelectorAll('input');
        for (var i = 0; i < felder.length; i++){
          var inp = felder[i], r = bruchLesen(inp.value), f = inp.dataset.f;
          inp.classList.remove('falsch');
          if (r.leer) return hinweis('Fülle das Feld aus.');
          if (r.gemischt) return hinweis('Schreib das Ergebnis als Bruch, zum Beispiel <code>7/3</code> statt «2 1/3» — gemischte Zahlen liest man leicht als Produkt.');
          if (r.kaputt){ inp.classList.add('falsch'); return hinweis(r.null ? 'Durch \\(0\\) teilen geht nicht.' : f[0] === 'b' ? 'Brüche wie <code>3/4</code> oder <code>-2/3</code>, ganze Zahlen wie <code>5</code>.' : 'Gib eine ganze Zahl ein.'); }
          if (r.komma) komma = true;
          if (f[0] === 'b'){
            if (gleich(r, A.r)){
              if (r.dez) return hinweis(A.r.n === 1 ? 'Gleicher Wert — schreib die ganze Zahl ohne Komma und Nachkommastellen: <code>' + A.r.z + '</code>.' : 'Gleicher Wert — gib das Ergebnis aber als <b>Bruch</b> an.');
              if (!gekuerzt(r)){ versuche++;                       // nicht fertig gekürzt: zählt als Versuch, «in Folge» bricht ab
                return hinweis(r.n === 1 ? 'Richtig gerechnet — schreib ganze Zahlen ohne Nenner: <code>' + r.z + '</code> statt <code>' + r.z + '/1</code>.'
                : 'Richtiger Wert, aber noch nicht vollständig <b>gekürzt</b>: \\(' + Math.abs(r.z) + '\\) und \\(' + r.n + '\\) sind beide durch \\(' + ggT(r.z, r.n) + '\\) teilbar.'); }
            }
            e[f] = r;
          } else {
            if (r.n !== 1 || r.dez){ inp.classList.add('falsch'); return hinweis('Gesucht ist eine ganze Zahl.'); }
            e[f] = r.z;
          }
        }
        versuche++;
        var ok = T.felder.every(function(f){ return f[0] === 'b' ? gleich(e[f], A.r) : e[f] === A[f]; });
        if (ok){
          serie = versuche === 1 && stufe === 0 ? serie + 1 : 0; geloest = true;
          rueck.className = 'ue-rueck richtig';
          rueck.innerHTML = '✓ Richtig' + (komma ? ' (Hier schreibt man den Dezimalpunkt.)' : '') + ' <button type="button" class="ue-weiter">Nächste</button>';
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

  /* ---------- Minibilder zu den Aufgaben ----------
     <svg class="mini-bruch" data-streifen="n,k;n,k"> Streifen (k von n gefärbt, mehrere übereinander)
     <svg class="mini-bruch" data-flaeche="a,b,c,d">   Flächenmodell a/b · c/d */
  document.querySelectorAll('svg.mini-bruch').forEach(function(svg){
    var i, j;
    if (svg.dataset.streifen){
      var teile = svg.dataset.streifen.split(';');
      svg.setAttribute('viewBox', '0 0 220 ' + (teile.length * 34 + 4));
      teile.forEach(function(t, z){ var p = t.split(',').map(Number); streifen(svg, 6, 6 + z * 34, 208, 24, p[0], p[1], z ? 'f2' : 'f1'); });
      svg.setAttribute('role', 'img');
    } else if (svg.dataset.flaeche){
      var q = svg.dataset.flaeche.split(',').map(Number), a = q[0], b = q[1], c = q[2], d = q[3], S = 140;
      svg.setAttribute('viewBox', '0 0 152 152'); svg.setAttribute('role', 'img');
      for (i = 0; i < b; i++) for (j = 0; j < d; j++)
        el(svg, 'rect', { x: 6 + S * i / b, y: 6 + S * j / d, width: S / b, height: S / d, 'class': 'zelle ' + ((i < a && j < c) ? 'f3' : i < a ? 'f1' : j < c ? 'f2' : 'leer') });
      el(svg, 'rect', { x: 6, y: 6, width: S, height: S, 'class': 'rahmen' });
    }
  });
})();
</script>
