<script>
/* Leitprogramm Funktionstypen und Graphen — vier Graphen-Familien (Sim 1), proportional, antiproportional, linear (Sim 2),
   Weg-Zeit-Graph aus drei Abschnitten (Sim 3), zurückgelegt und noch entfernt (Sim 4), Übungen mit Rückmeldung.
   Notation: y = a · x² usw., Punkte (x | y), Zahlen mit Dezimalpunkt und echtem Minus.
   Farben: blau = der eigene Graph und der zurückgelegte Weg, orange = Anfangswert und der Rest bis zum Ziel, grün = Treffer,
   grau gestrichelt = Ziel, rot = Fehler. Gerüst: scripts/lp/darstellungen/seite.js. */
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


  /* ---------- Koordinatensystem (aus dem Leitprogramm Lineare Funktionen von TALS Mathe, gekürzt) ---------- */
  var NS = 'http://www.w3.org/2000/svg';
  function el(eltern, name, attr, text){
    var e = document.createElementNS(NS, name);
    for (var k in attr) e.setAttribute(k, attr[k]);
    if (text != null) e.textContent = text;
    eltern.appendChild(e); return e;
  }
  function z(n){ var r = Math.round(n * 100) / 100; if (Object.is(r, -0)) r = 0; return (r < 0 ? '−' : '') + String(Math.abs(r)); }
  function Achsen(svg, o){
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var W = o.w, H = o.h, x0 = o.x0, x1 = o.x1, y0 = o.y0, y1 = o.y1;
    svg.setAttribute('viewBox', (-o.rl) + ' ' + (-12) + ' ' + (W + o.rl + 12) + ' ' + (H + 34));
    var id = 'k' + Math.random().toString(36).slice(2, 8);
    function X(x){ return (x - x0) / (x1 - x0) * W; }
    function Y(y){ return H - (y - y0) / (y1 - y0) * H; }
    var g = el(svg, 'g', {});
    var cp = el(g, 'clipPath', { id: id }); el(cp, 'rect', { x: 0, y: 0, width: W, height: H });
    var sx = o.sx || 1, sy = o.sy || 1, i;
    for (i = Math.ceil(x0 / sx) * sx; i <= x1 + 1e-9; i += sx) el(g, 'line', { x1: X(i), y1: 0, x2: X(i), y2: H, 'class': 'gitter' });
    for (i = Math.ceil(y0 / sy) * sy; i <= y1 + 1e-9; i += sy) el(g, 'line', { x1: 0, y1: Y(i), x2: W, y2: Y(i), 'class': 'gitter' });
    var ax = Math.max(y0, Math.min(y1, 0)), ay = Math.max(x0, Math.min(x1, 0));
    el(g, 'line', { x1: 0, y1: Y(ax), x2: W, y2: Y(ax), 'class': 'achse' });
    el(g, 'line', { x1: X(ay), y1: 0, x2: X(ay), y2: H, 'class': 'achse' });
    el(g, 'polygon', { points: W + ',' + Y(ax) + ' ' + (W - 7) + ',' + (Y(ax) - 3.5) + ' ' + (W - 7) + ',' + (Y(ax) + 3.5), 'class': 'pfeil' });
    el(g, 'polygon', { points: X(ay) + ',0 ' + (X(ay) - 3.5) + ',7 ' + (X(ay) + 3.5) + ',7', 'class': 'pfeil' });
    (o.xm || []).forEach(function(t){ el(g, 'text', { x: X(t), y: Y(ax) + 14, 'text-anchor': 'middle', 'class': 'skala' }, z(t)); });
    (o.ym || []).forEach(function(t){ el(g, 'text', { x: X(ay) - 5, y: Y(t) + 4, 'text-anchor': 'end', 'class': 'skala' }, z(t)); });
    var ebene = el(svg, 'g', {});
    el(svg, 'text', { x: W - 2, y: Y(ax) - 7, 'text-anchor': 'end', 'class': 'achsname' }, o.xname || 'x');
    el(svg, 'text', { x: X(ay) + 7, y: 10, 'text-anchor': 'start', 'class': 'achsname' }, o.yname || 'y');
    return {
      X: X, Y: Y, o: o,
      gerade: function(m, b, cls, a, c){ var A = a == null ? x0 : a, C = c == null ? x1 : c;
        return el(ebene, 'line', { x1: X(A), y1: Y(m * A + b), x2: X(C), y2: Y(m * C + b), 'class': cls, 'clip-path': 'url(#' + id + ')' }); },
      strecke: function(xa, ya, xb, yb, cls){ return el(ebene, 'line', { x1: X(xa), y1: Y(ya), x2: X(xb), y2: Y(yb), 'class': cls, 'clip-path': 'url(#' + id + ')' }); },
      punkt: function(x, y, cls, text, dx, dy, anker){
        if (x < x0 || x > x1 || y < y0 || y > y1) return;
        el(ebene, 'circle', { cx: X(x), cy: Y(y), r: o.r || 4.5, 'class': cls });
        if (text) el(ebene, 'text', { x: X(x) + (dx == null ? 8 : dx), y: Y(y) + (dy == null ? -8 : dy), 'text-anchor': anker || 'start', 'class': 'p-text ' + cls }, text);
      },
      kurve: function(f, a, c, cls){ var pk = [], n = 160; for (var k = 0; k <= n; k++){ var x = a + (c - a) * k / n, w = f(x); if (isFinite(w)) pk.push(X(x).toFixed(1) + ',' + Y(Math.max(y0 - 1, Math.min(y1 + 1, w))).toFixed(1)); }
        return el(ebene, 'polyline', { points: pk.join(' '), 'class': cls, fill: 'none', 'clip-path': 'url(#' + id + ')' }); },
      text: function(x, y, s, cls, anker){ el(ebene, 'text', { x: X(x), y: Y(y), 'text-anchor': anker || 'middle', 'class': 'p-text ' + cls }, s); },
      zuWert: function(px, py){ return [x0 + px / W * (x1 - x0), y0 + (H - py) / H * (y1 - y0)]; }
    };
  }
  var GITTER = { w: 280, h: 280, rl: 18, x0: -7, x1: 7, y0: -7, y1: 7, xm: [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6], ym: [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6] };
  function wertR(fig, id){ return +fig.querySelector('#' + id).value; }
  function zeigeWert(fig, id, txt){ var i = fig.querySelector('#' + id); var v = i.parentNode.querySelector('.sl-val'); if (v) v.textContent = txt != null ? txt : mz(+i.value); }   /* einmal definiert: eine zweite Fassung ohne txt überschrieb die Einheiten (Prüfung 10.10.2026) */
  /* y = m·x + b als HTML-Text (Live-Anzeige ohne MathJax); m als Bruch [z, n] oder Zahl */
  function linTxt(m, b, xn, yn){
    xn = xn || 'x'; yn = yn || 'y';
    var mm = Array.isArray(m) ? m : bDez(m), s;
    var mt = mm[1] === 1 ? z(mm[0]) : (mm[0] < 0 ? '−' : '') + Math.abs(mm[0]) + '/' + mm[1];
    if (!mm[0]) s = z(b);
    else {
      s = (mt === '1' ? '' : mt === '−1' ? '−' : mt + ' · ') + xn;
      if (b) s += (b > 0 ? ' + ' : ' − ') + z(Math.abs(b));
    }
    return yn + ' = ' + s;
  }
  /* y = m x + b als LaTeX; m als Bruch [z, n] */
  function linTex(m, b, xn){
    xn = xn || 'x';
    var s;
    if (!m[0]) return String(b);
    s = m[1] === 1 ? (m[0] === 1 ? '' : m[0] === -1 ? '-' : m[0]) : (m[0] < 0 ? '-' : '') + '\\tfrac{' + Math.abs(m[0]) + '}{' + m[1] + '}';
    s += xn;
    if (b) s += (b > 0 ? ' + ' : ' - ') + Math.abs(b);
    return s;
  }

  /* y-Wert einer Familie: g Gerade a·x + b, q Parabel a·x² + b, w Wurzel a·√x + b, k Kehrwert a/x + b */
  function fam(typ, a, b, x){
    if (typ === 'g') return a * x + b;
    if (typ === 'q') return a * x * x + b;
    if (typ === 'w') return x < 0 ? NaN : a * Math.sqrt(x) + b;
    return x === 0 ? NaN : a / x + b;
  }
  function famTxt(typ, a, b){
    var at = a === 1 ? '' : a === -1 ? '−' : z(a) + ' · ', bt = b ? (b > 0 ? ' + ' : ' − ') + z(Math.abs(b)) : '';
    if (typ === 'g') return 'y = ' + at + 'x' + bt;
    if (typ === 'q') return 'y = ' + at + 'x²' + bt;
    if (typ === 'w') return 'y = ' + at + '√x' + bt;
    return 'y = ' + z(a) + ' / x' + bt;
  }
  function famZeichnen(k, typ, a, b, cls, x0, x1){
    if (typ === 'k'){ k.kurve(function(x){ return fam(typ, a, b, x); }, x0, -0.02, cls); k.kurve(function(x){ return fam(typ, a, b, x); }, 0.02, x1, cls); }
    else k.kurve(function(x){ return fam(typ, a, b, x); }, typ === 'w' ? 0 : x0, x1, cls);
  }
  var FAMNAME = { g: 'Gerade', q: 'Parabel', w: 'Wurzelgraph', k: 'Kehrwertgraph' };

  /* ════════ Sim 1 — Vier Graphen-Familien ════════
     Ein Zielgraph (gestrichelt) aus einer der vier Familien; eingestellt werden Familie, a und b. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]'), wahl = fig.querySelector('#s1-fam');
    var ZIEL = ['g', 2, -1];
    function zustand(){ return { typ: wahl.value, a: wertR(fig, 's1-a'), b: wertR(fig, 's1-b') }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's1-a', z(Z.a)); zeigeWert(fig, 's1-b');
      var k = Achsen(svg, GITTER);
      famZeichnen(k, ZIEL[0], ZIEL[1], ZIEL[2], 'linie grau gestrichelt', -7, 7);
      famZeichnen(k, Z.typ, Z.a, Z.b, 'linie blau', -7, 7);
      formel.innerHTML = FAMNAME[Z.typ] + ': <b>' + famTxt(Z.typ, Z.a, Z.b) + '</b>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    var A = [
      [['g', 2, -1], 'Der gestrichelte Graph ist gerade und steigt. Bring deinen Graphen darauf.'],
      [['q', 1, -2], 'Der gestrichelte Graph ist symmetrisch zur y-Achse und hat unten einen Scheitel. Welche Familie?'],
      [['w', 2, 0], 'Dieser Graph beginnt bei (0 | 0) und wird immer flacher. Links von der y-Achse gibt es nichts.'],
      [['k', 4, 0], 'Zwei Äste, die die Achsen nie treffen. Tipp: Er geht durch (2 | 2).'],
      [['q', -0.5, 3], 'Wieder eine Parabel, aber nach unten offen, mit Scheitel bei (0 | 3).']
    ];
    pr = Leiste(fig, A.map(function(t){
      return { text: t[1], setup: function(){ ZIEL = t[0]; }, ok: function(Z){ return Z.typ === t[0][0] && Z.a === t[0][1] && Z.b === t[0][2]; } };
    }), sim);
    fig.querySelectorAll('input, select').forEach(function(i){ i.addEventListener('input', zeichnen); i.addEventListener('change', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 2 — Proportional, antiproportional, linear ════════
     y = k·x + b (b = 0: proportional) oder y = k/x (antiproportional). Der Regler x zeigt den Doppelt-Test. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]'), wahl = fig.querySelector('#s2-typ');
    var F2 = { w: 300, h: 260, rl: 26, x0: 0, x1: 10, y0: 0, y1: 24, sx: 1, sy: 2, xm: [2, 4, 6, 8, 10], ym: [4, 8, 12, 16, 20, 24], r: 4 };
    var P = [];
    function zustand(){ return { typ: wahl.value, k: wertR(fig, 's2-k'), b: wertR(fig, 's2-b'), x: wertR(fig, 's2-x') }; }
    function y(Z, x){ return Z.typ === 'anti' ? Z.k / x : Z.k * x + Z.b; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's2-k', z(Z.k)); zeigeWert(fig, 's2-b'); zeigeWert(fig, 's2-x');
      fig.querySelector('#s2-b').disabled = Z.typ === 'anti';
      var k = Achsen(svg, F2);
      if (Z.typ === 'anti') k.kurve(function(x){ return Z.k / x; }, Math.max(0.05, Z.k / 26), 10, 'linie blau');
      else k.gerade(Z.k, Z.b, 'linie blau', 0, 10);
      P.forEach(function(p){ k.punkt(p[0], p[1], Math.abs(y(Z, p[0]) - p[1]) < 1e-9 ? 'pkt gruen' : 'pkt ziel', '(' + p[0] + ' | ' + p[1] + ')', 8, 16); });
      var y1 = y(Z, Z.x), y2 = y(Z, 2 * Z.x);
      k.punkt(Z.x, y1, 'pkt'); k.punkt(2 * Z.x, y2, 'pkt');
      var q = y2 / y1, wort = Math.abs(q - 2) < 1e-9 ? 'doppelt so gross' : Math.abs(q - 0.5) < 1e-9 ? 'halb so gross' : 'weder doppelt noch halb so gross';
      formel.innerHTML = '<b>' + (Z.typ === 'anti' ? 'y = ' + z(Z.k) + ' / x' : linTxt(Z.k, Z.b)) + '</b> &nbsp;·&nbsp; x = ' + Z.x + ': y = ' + z(y1) + ' &nbsp;→&nbsp; x = ' + 2 * Z.x + ': y = ' + z(y2) + ' <span class="grau">(' + wort + ')</span>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    var A = [
      ['Proportional durch \\((2 \\mid 6)\\): Stell den Zusammenhang ein.', [[2, 6]], function(Z){ return Z.typ === 'lin' && Z.k === 3 && Z.b === 0; }],
      ['Linear mit Anfangswert 4 durch \\((2 \\mid 10)\\).', [[2, 10]], function(Z){ return Z.typ === 'lin' && Z.k === 3 && Z.b === 4; }],
      ['Antiproportional durch \\((3 \\mid 4)\\).', [[3, 4]], function(Z){ return Z.typ === 'anti' && Z.k === 12; }],
      ['Bei welchem Typ wird \\(y\\) doppelt so gross, wenn \\(x\\) doppelt so gross wird? Stell ihn mit \\(k = 2\\) ein.', [], function(Z){ return Z.typ === 'lin' && Z.k === 2 && Z.b === 0; }],
      ['Antiproportional durch \\((2 \\mid 9)\\). Prüf mit dem Regler \\(x\\): Was passiert beim Verdoppeln?', [[2, 9]], function(Z){ return Z.typ === 'anti' && Z.k === 18; }]
    ];
    pr = Leiste(fig, A.map(function(t){ return { text: t[0], setup: function(){ P = t[1]; }, ok: t[2] }; }), sim);
    fig.querySelectorAll('input, select').forEach(function(i){ i.addEventListener('input', zeichnen); i.addEventListener('change', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 3 — Weg-Zeit-Graph aus drei Abschnitten ════════
     Je 10 Minuten mit der Geschwindigkeit v1, v2, v3 (m/min, negativ: zurück). Ziel gestrichelt. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    var F3 = { w: 300, h: 240, rl: 34, x0: 0, x1: 30, y0: 0, y1: 2500, sx: 5, sy: 250, xm: [5, 10, 15, 20, 25, 30], ym: [500, 1000, 1500, 2000, 2500], xname: 't [min]', yname: 's [m]', r: 3.5 };
    var ZIEL = [60, 0, 120];
    function zustand(){ return { v: [wertR(fig, 's3-v1'), wertR(fig, 's3-v2'), wertR(fig, 's3-v3')] }; }
    function stand(v){ var s = [0]; v.forEach(function(w, i){ s.push(s[i] + 10 * w); }); return s; }
    function zeichnen(){
      var Z = zustand(); ['s3-v1', 's3-v2', 's3-v3'].forEach(function(id, i){ zeigeWert(fig, id, z(Z.v[i]) + ' m/min'); });
      var k = Achsen(svg, F3), sz = stand(ZIEL), s = stand(Z.v);
      for (var i = 0; i < 3; i++) k.strecke(10 * i, sz[i], 10 * i + 10, sz[i + 1], 'linie grau gestrichelt');
      for (i = 0; i < 3; i++) k.strecke(10 * i, s[i], 10 * i + 10, s[i + 1], 'linie blau');
      for (i = 0; i < 4; i++) k.punkt(10 * i, s[i], 'pkt');
      var neg = s.some(function(w){ return w < 0; });
      formel.innerHTML = 'nach 10, 20, 30 min: ' + s.slice(1).map(function(w){ return z(w) + ' m'; }).join(', ') + (neg ? ' <span class="nein-text">(hinter dem Start?)</span>' : '');
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    var A = [
      [[60, 0, 120], 'Bring deinen Graphen auf den gestrichelten. Was passiert im mittleren Abschnitt?'],
      [[100, 50, 0], 'Zuerst schnell, dann langsamer, am Schluss steht die Person.'],
      [[80, 0, -80], 'Hin, Pause, und zurück zum Start.'],
      [[40, 80, 120], 'Jeder Abschnitt steiler als der vorherige.'],
      [[120, -60, 30], 'Schnell hin, ein Stück zurück, dann langsam weiter.']
    ];
    pr = Leiste(fig, A.map(function(t){ return { text: t[1], setup: function(){ ZIEL = t[0]; },
      ok: function(Z){ return Z.v[0] === t[0][0] && Z.v[1] === t[0][1] && Z.v[2] === t[0][2]; } }; }), sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 4 — Zurückgelegt und noch entfernt ════════
     Strecke L km, Tempo v km/h: zurückgelegt s = v·t (blau), noch entfernt L − v·t (orange), beide bis zur Ankunft. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    var F4 = { w: 300, h: 240, rl: 26, x0: 0, x1: 3, y0: 0, y1: 36, sx: 0.5, sy: 4, xm: [0.5, 1, 1.5, 2, 2.5, 3], ym: [6, 12, 18, 24, 30, 36], xname: 't [h]', yname: '[km]', r: 4 };
    function zustand(){ return { L: wertR(fig, 's4-L'), v: wertR(fig, 's4-v'), t: wertR(fig, 's4-t') }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's4-L', Z.L + ' km'); zeigeWert(fig, 's4-v', Z.v + ' km/h'); zeigeWert(fig, 's4-t', z(Z.t) + ' h');
      var k = Achsen(svg, F4), ta = Math.min(3, Z.L / Z.v), zr = Math.min(Z.L, Z.v * Z.t);
      k.strecke(0, 0, ta, Z.v * ta, 'linie blau'); k.strecke(0, Z.L, ta, Z.L - Z.v * ta, 'linie orange');
      k.strecke(Z.t, 0, Z.t, 36, 'linie grau gestrichelt');
      k.punkt(Z.t, zr, 'pkt blau'); k.punkt(Z.t, Z.L - zr, 'pkt orange');
      formel.innerHTML = 'nach ' + z(Z.t) + ' h: <span class="blau">zurückgelegt ' + z(zr) + ' km</span> &nbsp;·&nbsp; <span class="orange">noch entfernt ' + z(Z.L - zr) + ' km</span>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, [
      { text: '24 km mit 16 km/h. Wann ist die Hälfte geschafft? Zieh \\(t\\) dorthin.', ok: function(Z){ return Z.L === 24 && Z.v === 16 && Z.t === 0.75; } },
      { text: '20 km mit 8 km/h. Wann sind es noch 4 km?', ok: function(Z){ return Z.L === 20 && Z.v === 8 && Z.t === 2; } },
      { text: '12 km mit 4 km/h. Wann sind noch 6 km übrig?', ok: function(Z){ return Z.L === 12 && Z.v === 4 && Z.t === 1.5; } },
      { text: '30 km mit 12 km/h. Wann kommst du an?', ok: function(Z){ return Z.L === 30 && Z.v === 12 && Z.t === 2.5; } },
      { text: '18 km mit 6 km/h. Wann ist der zurückgelegte Weg doppelt so lang wie der Rest?', ok: function(Z){ return Z.L === 18 && Z.v === 6 && Z.t === 2; } }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ---------- Minibilder: Geraden (data-geraden), Familien (data-kurven="typ,a,b"), Streckenzug (data-linie="x,y;x,y") ---------- */
  function miniBild(svg, geraden, punkte){
    var d = svg.dataset, sach = !!d.fenster;
    var o = { w: 180, h: 180, rl: 14, x0: -6, x1: 6, y0: -6, y1: 6, xm: [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], ym: [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], r: 3.5 };
    if (sach){ var f = d.fenster.split(',').map(Number), sch = (d.schritte || '1,1').split(',').map(Number), reihe = function(a, b, s){ var l = []; for (var i = s; i <= b + 1e-9; i += s) if (i >= a) l.push(+i.toFixed(6)); return l; };
      var ras = (d.raster || sch.join(',')).split(',').map(Number);
      o.x0 = f[0]; o.x1 = f[1]; o.y0 = f[2]; o.y1 = f[3]; o.sx = ras[0]; o.sy = ras[1]; o.xm = reihe(f[0], f[1], sch[0]); o.ym = reihe(f[2], f[3], sch[1]); o.xname = d.xname; o.yname = d.yname; o.w = 220; o.h = 170; o.rl = 30; }
    var k = Achsen(svg, o);
    geraden.forEach(function(g, i){ k.gerade(g[0], g[1], 'linie ' + (i ? 'orange' : 'blau'), sach ? 0 : null); });
    (d.kurven || '').split(';').filter(Boolean).forEach(function(t){ var p = t.split(','); famZeichnen(k, p[0], +p[1], +p[2], 'linie blau', o.x0, o.x1); });
    if (d.linie){ var L = d.linie.split(';').map(function(t){ return t.split(',').map(Number); });
      for (var i = 1; i < L.length; i++) k.strecke(L[i - 1][0], L[i - 1][1], L[i][0], L[i][1], 'linie blau'); }
    punkte.forEach(function(p){ k.punkt(p[0], p[1], 'pkt'); });
    return k;
  }
  document.querySelectorAll('svg.mini-gerade').forEach(function(svg){
    var lies = function(s){ return (s || '').split(';').filter(Boolean).map(function(t){ return t.split(',').map(function(v){ return v.indexOf('/') >= 0 ? +v.split('/')[0] / +v.split('/')[1] : +v; }); }); };
    svg.setAttribute('role', 'img');
    miniBild(svg, lies(svg.dataset.geraden), lies(svg.dataset.punkte));
  });
  document.querySelectorAll('svg.leer-gitter').forEach(function(svg){ svg.setAttribute('role', 'img'); Achsen(svg, GITTER); });

  /* ---------- Aufgabenleiste (wie in den anderen Leitprogrammen) ---------- */
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

  /* ════════ Übungen mit Rückmeldung ════════
     Zahlenfelder exakt als Bruch (2/3, −1.5, 4). Feld w: Auswahl (select). Fehlversuch → gezielte Diagnose. Tipps in drei
     Stufen. Testhaken: box.__aufgabe, box.__typ. Minigraphen im Aufgabentext (svg.mini-gerade) werden beim Würfeln gezeichnet. */
  (function(){
    var ALLE = document.querySelectorAll('.uebung[data-typ]'); if (!ALLE.length) return;
    function mischen(l){ var a = l.slice(); for (var i = a.length - 1; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    function kl(v){ return v < 0 ? '(' + mz(v) + ')' : z(v); }
    function famTex(typ, a, b){
      var at = a === 1 ? '' : a === -1 ? '-' : String(a).replace('-', '-'), bt = b ? (b > 0 ? ' + ' : ' - ') + Math.abs(b) : '';
      if (typ === 'g') return 'y = ' + at + 'x' + bt;
      if (typ === 'q') return 'y = ' + at + 'x^2' + bt;
      if (typ === 'w') return 'y = ' + at + '\\sqrt{x}' + bt;
      return 'y = \\dfrac{' + a + '}{x}' + bt;
    }
    function mini(attr, label){ return '<span class="mini-reihe"><svg class="mini-gerade" ' + attr + ' aria-label="' + label + '"></svg></span>'; }

    /* Feste Aufgaben (Clips, Festhalten, Erkundungen, Kapitelaufgaben, Gesamttest): nie als Zufallsübung. */
    var SPERRE = [
      'zu|g|2|-1', 'zu|q|1|-2', 'zu|w|2|0', 'zu|k|4|0', 'zu|q|-0.5|3', 'zu|g|2|1', 'zu|q|0.5|0', 'zu|k|8|0', 'zu|k|3|0', 'zu|q|1|0', 'zu|w|1|0', 'zu|k|1|0',
      'we|k|3|6', 'we|w|2|9', 'we|q|0.5|4', 'we|w|2|4', 'we|k|4|4', 'we|k|6|4',
      'nw|anti|6|10', 'nw|anti|5|12', 'nw|anti|2|12', 'nw|anti|3|4', 'nw|prop|4|10', 'nw|anti|4|10',
      'te|0,0;10,800;15,800;20,1400', 'te|0,0;4,600;10,600;14,1400', 'te|0,0;10,600;15,600;25,1800',
      're|24|16', 're|36|12', 're|12|4', 're|30|20', 're|20|8', 're|18|6'
    ];
    function gesperrt(T, A){ return !!T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }

    var SIT = {
      prop: [['Ein Kilogramm Äpfel kostet {k} Fr. Preis für \\(x\\) kg.', [3, 4, 5]], ['Ein Auto fährt mit {k} km/h. Weg nach \\(x\\) Stunden.', [60, 80, 90]],
             ['Ein Kinoeintritt kostet {k} Fr. Preis für \\(x\\) Personen.', [12, 18, 20]], ['Ein Wasserhahn liefert {k} l pro Minute. Wasser nach \\(x\\) Minuten.', [6, 8, 12]]],
      anti: [['{k} Bonbons werden gleichmässig auf \\(x\\) Kinder verteilt. Bonbons pro Kind.', [24, 36, 48]], ['Eine Strecke von {k} km. Fahrzeit bei \\(x\\) km/h.', [120, 180, 240]],
             ['{k} Fr. Miete werden auf \\(x\\) Personen aufgeteilt. Betrag pro Person.', [600, 900, 1200]], ['Ein Becken mit {k} l wird mit \\(x\\) gleichen Pumpen geleert. Zeit in Minuten.', [600, 900, 1200]]],
      lin:  [['Ein Taxi kostet {b} Fr. Grundtaxe und {k} Fr. pro km. Preis für \\(x\\) km.', [2, 3, 4]], ['Ein Fitnessabo kostet {b} Fr. und {k} Fr. pro Besuch. Kosten für \\(x\\) Besuche.', [5, 6, 8]],
             ['Eine Kerze ist {b} cm hoch und wird pro Stunde {k} cm kürzer. Höhe nach \\(x\\) Stunden.', [1, 2, 3]], ['Ein Tank enthält {b} l, pro Minute kommen {k} l dazu. Inhalt nach \\(x\\) Minuten.', [4, 5, 10]]]
    };

    var TYPEN = {
      /* ── Kapitel 1 ── */
      'zuordnen': { felder: ['w'],
        schl: function(A){ return 'zu|' + A.typ + '|' + A.a + '|' + A.b; },
        eingabe: function(A){ return { w: A.typ }; },
        neu: function(){
          var typ = zufall(['g', 'q', 'w', 'k']), a = zufall(typ === 'k' ? [1, 2, 3, 4, 6] : typ === 'q' ? [0.5, 1, 2, -1, -0.5] : [0.5, 1, 2, 3, -1]), b = typ === 'k' || typ === 'w' ? 0 : zufall([-2, -1, 0, 1, 2]);
          var andere = mischen(['g', 'q', 'w', 'k'].filter(function(t){ return t !== typ; })).slice(0, 2), alle = mischen([typ].concat(andere));
          return { typ: typ, a: a, b: b, text: 'Welche Gleichung gehört zum Graphen?' + mini('data-kurven="' + typ + ',' + a + ',' + b + '"', 'Graph einer Funktion'),
                   optionen: alle.map(function(t){ return [t, famTxt(t, t === 'k' && a < 0 ? -a : a, t === 'k' || t === 'w' ? 0 : b)]; }), muster: '{w}' }; },
        richtig: function(A, e){ return e.w === A.typ; },
        fehler: function(A){ return A.optionen.filter(function(o){ return o[0] !== A.typ; }).map(function(o){ return [{ w: o[0] }, FAMNAME[o[0]]]; }); },
        pruefen: function(A, e){ return {
            g: 'Eine <b>Gerade</b> ändert sich bei jedem Schritt nach rechts um gleich viel. Ist der Graph gerade?',
            q: 'Eine <b>Parabel</b> ist symmetrisch zur \\(y\\)-Achse: Links und rechts liegen gleich hohe Punkte. Siehst du das?',
            w: 'Ein <b>Wurzelgraph</b> beginnt bei \\(x = 0\\) und hat links von der \\(y\\)-Achse keine Punkte.',
            k: 'Ein <b>Kehrwertgraph</b> hat zwei Äste und trifft keine Achse.' }[e.w] + ' Prüf mit einem Gitterpunkt des Graphen.'; },
        tipps: function(A){ return ['Achte auf die Form: gerade, symmetrisch mit Scheitel, Start bei 0 und immer flacher, oder zwei Äste ohne Achse?', 'Setz einen gut ablesbaren Punkt des Graphen in die Gleichungen ein.']; },
        loesung: function(A){ return '\\text{' + FAMNAME[A.typ] + '}: \\; ' + famTex(A.typ, A.a, A.b); } },

      'werte': { felder: ['y'],
        schl: function(A){ return 'we|' + A.typ + '|' + A.a + '|' + A.x; },
        eingabe: function(A){ return { y: bWert(A.y).replace('−', '-') }; },
        neu: function(){
          var typ = zufall(['q', 'w', 'k']), a, x;
          if (typ === 'q'){ a = zufall([2, 3, 0.5]); x = zufall([-3, -2, 2, 3, 4]); }
          else if (typ === 'w'){ a = zufall([2, 3, 5]); x = zufall([4, 9, 16, 25]); }
          else { a = zufall([6, 8, 12, 24]); x = zufall([2, 3, 4, 0.5]); }
          var y = typ === 'q' ? bMul(bDez(a), B(x * x)) : typ === 'w' ? B(a * Math.sqrt(x)) : bDiv(B(a), bDez(x));
          return { typ: typ, a: a, x: x, y: y, text: 'Berechne \\(y\\) für \\(x = ' + x + '\\): \\(' + famTex(typ, a, 0) + '\\).', muster: '\\(y = \\) {y}' }; },
        richtig: function(A, e){ return bEq(e.y, A.y); },
        fehler: function(A){
          if (A.typ === 'q'){ var w = bMul(bDez(A.a), bDez(A.a)); return bEq(bMul(w, B(A.x * A.x)), A.y) ? [] : [[{ y: bWert(bMul(w, B(A.x * A.x))).replace('−', '-') }, 'zuerst']]; }
          if (A.typ === 'k') return bEq(bDiv(bDez(A.x), B(A.a)), A.y) ? [] : [[{ y: bWert(bDiv(bDez(A.x), B(A.a))).replace('−', '-') }, 'Bruch']];
          return [[{ y: String(A.a * A.x) }, 'Wurzel']]; },
        pruefen: function(A, e){
          if (A.typ === 'q' && bEq(e.y, bMul(bMul(bDez(A.a), bDez(A.a)), B(A.x * A.x)))) return 'Quadriert wird nur \\(x\\), <b>zuerst</b> \\(x^2\\), dann mal \\(' + A.a + '\\).';
          if (A.typ === 'k' && bEq(e.y, bDiv(bDez(A.x), B(A.a)))) return 'Im <b>Bruch</b> steht \\(x\\) unten: \\(' + A.a + ' : ' + A.x + '\\), nicht umgekehrt.';
          if (A.typ === 'w' && bEq(e.y, B(A.a * A.x))) return 'Zuerst die <b>Wurzel</b> aus \\(' + A.x + '\\), dann mal \\(' + A.a + '\\).';
          return 'Setz \\(x = ' + A.x + '\\) ein und rechne Schritt für Schritt.' + (A.x < 0 ? ' Achtung: \\((' + A.x + ')^2\\) ist positiv.' : ''); },
        tipps: function(A){ return ['Setz \\(x = ' + A.x + '\\) in die Gleichung ein.', A.typ === 'q' ? '\\(' + kl(A.x) + '^2 = ' + A.x * A.x + '\\)' : A.typ === 'w' ? '\\(\\sqrt{' + A.x + '} = ' + Math.sqrt(A.x) + '\\)' : '\\(' + A.a + ' : ' + A.x + '\\)']; },
        loesung: function(A){ return 'y = ' + (A.typ === 'q' ? A.a + ' \\cdot ' + kl(A.x) + '^2' : A.typ === 'w' ? A.a + ' \\cdot \\sqrt{' + A.x + '}' : '\\dfrac{' + A.a + '}{' + A.x + '}') + ' = ' + bWertTex(A.y); } },

      /* ── Kapitel 2 ── */
      'situation': { felder: ['w'],
        schl: function(A){ return 'si|' + A.text; },
        eingabe: function(A){ return { w: A.art }; },
        neu: function(){
          var art = zufall(['prop', 'anti', 'lin']), s = zufall(SIT[art]), k = zufall(s[1]), b = zufall([10, 20, 40]);   /* nicht 30 + 5 (Kontrollclip) */
          return { art: art, text: s[0].replace('{k}', k).replace('{b}', b) + ' Welcher Zusammenhang ist das?', muster: '{w}',
                   optionen: [['prop', 'proportional'], ['anti', 'antiproportional'], ['lin', 'linear mit Anfangswert']] }; },
        richtig: function(A, e){ return e.w === A.art; },
        fehler: function(A){ return { prop: [[{ w: 'lin' }, 'null']], anti: [[{ w: 'lin' }, 'halb']], lin: [[{ w: 'prop' }, 'Anfang']] }[A.art]; },
        pruefen: function(A, e){
          if (A.art === 'lin') return 'Hier gibt es schon bei \\(x = 0\\) einen Wert, einen <b>Anfangswert</b>. Proportional geht durch \\((0 \\mid 0)\\).';
          if (A.art === 'anti') return 'Mach den Doppelt-Test: Wird \\(x\\) doppelt so gross, wird \\(y\\) <b>halb</b> so gross. Das Produkt bleibt gleich.';
          return 'Für \\(x = 0\\) ist \\(y\\) hier <b>null</b>, und doppeltes \\(x\\) gibt doppeltes \\(y\\).'; },
        tipps: function(A){ return ['Doppelt-Test: Was passiert mit \\(y\\), wenn \\(x\\) doppelt so gross wird?', 'Und was ist bei \\(x = 0\\)?']; },
        loesung: function(A){ return '\\text{' + { prop: 'proportional', anti: 'antiproportional', lin: 'linear mit Anfangswert' }[A.art] + '}'; } },

      'neuwert': { felder: ['y'],
        schl: function(A){ return 'nw|' + A.art + '|' + A.x0 + '|' + A.y0; },
        eingabe: function(A){ return { y: bWert(A.y1).replace('−', '-') }; },
        neu: function(){
          var art = zufall(['prop', 'anti']), x0 = zufall([2, 3, 4, 5, 6]), y0 = zufall([4, 6, 8, 10, 12, 15]), x1 = zufall([1, 2, 3, 4, 6, 8, 10, 12]);
          if (x1 === x0) return TYPEN.neuwert.neu();
          var y1 = art === 'prop' ? bDiv(B(y0 * x1), B(x0)) : bDiv(B(y0 * x0), B(x1));
          if (y1[1] > 2) return TYPEN.neuwert.neu();
          return { art: art, x0: x0, y0: y0, x1: x1, y1: y1, text: 'Der Zusammenhang ist <b>' + (art === 'prop' ? 'proportional' : 'antiproportional') + '</b>. Bei \\(x = ' + x0 + '\\) ist \\(y = ' + y0 + '\\). Wie gross ist \\(y\\) bei \\(x = ' + x1 + '\\)?', muster: '\\(y = \\) {y}' }; },
        richtig: function(A, e){ return bEq(e.y, A.y1); },
        fehler: function(A){ var w = A.art === 'prop' ? bDiv(B(A.y0 * A.x0), B(A.x1)) : bDiv(B(A.y0 * A.x1), B(A.x0)); return bEq(w, A.y1) ? [] : [[{ y: bWert(w).replace('−', '-') }, A.art === 'prop' ? 'Quotient' : 'Produkt']]; },
        pruefen: function(A, e){
          if (A.art === 'anti') return 'Antiproportional: Das <b>Produkt</b> bleibt gleich, \\(' + A.x0 + ' \\cdot ' + A.y0 + ' = ' + A.x0 * A.y0 + '\\). Wird \\(x\\) grösser, wird \\(y\\) kleiner.';
          return 'Proportional: Der <b>Quotient</b> \\(y : x = ' + bWertTex(B(A.y0, A.x0)) + '\\) bleibt gleich. Wird \\(x\\) grösser, wird auch \\(y\\) grösser.'; },
        tipps: function(A){ return [A.art === 'prop' ? 'Rechne zuerst \\(y\\) für \\(x = 1\\): \\(' + A.y0 + ' : ' + A.x0 + '\\).' : 'Rechne das Produkt \\(x \\cdot y\\) aus. Es bleibt gleich.',
          A.art === 'prop' ? 'Dann mal \\(' + A.x1 + '\\).' : '\\(' + A.x0 * A.y0 + ' : ' + A.x1 + '\\)']; },
        loesung: function(A){ return A.art === 'prop' ? 'y = \\dfrac{' + A.y0 + '}{' + A.x0 + '} \\cdot ' + A.x1 + ' = ' + bWertTex(A.y1) : 'y = \\dfrac{' + A.x0 + ' \\cdot ' + A.y0 + '}{' + A.x1 + '} = ' + bWertTex(A.y1); } },

      /* ── Kapitel 3 ── */
      'tempo': { felder: ['v'],
        schl: function(A){ return 'te|' + A.L.map(function(p){ return p.join(','); }).join(';'); },
        eingabe: function(A){ return { v: String(A.v[A.k]) }; },
        neu: function(){
          var t = [0], s = [0], v = [], d;
          for (var i = 0; i < 3; i++){ d = zufall([2, 4, 6]); var w = zufall([0, 25, 50, 75, 100, 150]); if (i && w === v[i - 1]) w = w === 0 ? 50 : 0; t.push(t[i] + d); s.push(s[i] + d * w); v.push(w); }   /* jeder Knick auf einer Gitterlinie (50 m) */
          var k = zufallG(0, 2); if (!v[k]) return TYPEN.tempo.neu();
          var L = t.map(function(x, i){ return [x, s[i]]; }), smax = Math.max.apply(null, s), ys = smax > 1000 ? 200 : 100;
          return { L: L, v: v, k: k, t: t, s: s, text: 'Der Graph zeigt einen Weg. Wie schnell (in m/min) ist die Person im <b>' + ['ersten', 'zweiten', 'dritten'][k] + '</b> Abschnitt?'
                   + mini('data-linie="' + L.map(function(p){ return p.join(','); }).join(';') + '" data-fenster="0,' + Math.max(10, t[3]) + ',0,' + (Math.ceil(smax / ys) * ys || ys) + '" data-schritte="2,' + ys + '" data-raster="1,50" data-xname="t [min]" data-yname="s [m]"', 'Weg-Zeit-Graph aus drei Abschnitten'),
                   muster: '\\(v = \\) {v} m/min' }; },
        richtig: function(A, e){ return bEq(e.v, B(A.v[A.k])); },
        fehler: function(A){ var ds = A.s[A.k + 1] - A.s[A.k], f = []; if (ds !== A.v[A.k]) f.push([{ v: String(ds) }, 'Zeit']); if (A.s[A.k + 1] !== ds && A.s[A.k + 1] !== A.v[A.k]) f.push([{ v: String(A.s[A.k + 1]) }, 'Δs']); return f; },
        pruefen: function(A, e){
          var ds = A.s[A.k + 1] - A.s[A.k], dt = A.t[A.k + 1] - A.t[A.k];
          if (bEq(e.v, B(ds))) return 'Das ist der Weg im Abschnitt. Er dauert aber \\(' + dt + '\\) Minuten: Teile durch die <b>Zeit</b>.';
          if (bEq(e.v, B(A.s[A.k + 1]))) return 'Das ist der Stand am Ende. Gesucht ist die Steigung in diesem Abschnitt: <b>Δs</b> geteilt durch Δt.';
          return 'Lies Anfang und Ende des Abschnitts ab und rechne \\(\\dfrac{\\Delta s}{\\Delta t}\\).'; },
        tipps: function(A){ return ['Geschwindigkeit = Steigung = \\(\\dfrac{\\Delta s}{\\Delta t}\\).', 'Abschnitt von \\(t = ' + A.t[A.k] + '\\) bis \\(t = ' + A.t[A.k + 1] + '\\) min.']; },
        loesung: function(A){ return 'v = \\dfrac{' + A.s[A.k + 1] + ' - ' + A.s[A.k] + '}{' + A.t[A.k + 1] + ' - ' + A.t[A.k] + '} = ' + A.v[A.k] + '\\ \\text{m/min}'; } },

      'beschreibung': { felder: ['w'],
        schl: function(A){ return 'be|' + A.arten.join(',') + '|' + A.t.join(','); },
        eingabe: function(A){ return { w: 'r' }; },
        neu: function(){
          var W = { s: ['schnell', 120], l: ['langsam', 40], p: ['Pause', 0], z: ['zurück', -80] }, arten;
          do { arten = [zufall(['s', 'l']), zufall(['s', 'l', 'p', 'z']), zufall(['s', 'l', 'p', 'z'])]; } while (arten[1] === arten[2] || arten[0] === arten[1] || (arten[1] === 'z' && arten[2] === 'z'));
          var t = [0], s = [0]; arten.forEach(function(a, i){ var d = zufall([3, 4, 5, 6]); t.push(t[i] + d); s.push(s[i] + d * W[a][1]); });   /* Dauer je Abschnitt verschieden */
          if (Math.min.apply(null, s) < 0) return TYPEN.beschreibung.neu();
          var satz = function(l){ return l.map(function(a, i){ return (i ? (i === 2 ? ', zum Schluss ' : ', dann ') : 'Zuerst ') + W[a][0]; }).join('') + '.'; };
          var falsch1 = arten.slice().reverse(), falsch2 = arten.map(function(a){ return a === 'z' ? 'l' : a === 'p' ? 's' : a === 'l' ? 'p' : 'l'; });
          return { arten: arten, t: t, text: 'Welche Beschreibung passt zum Weg-Zeit-Graphen? (\\(s\\): Entfernung vom Start)'
                   + mini('data-linie="' + t.map(function(x, i){ return x + ',' + s[i]; }).join(';') + '" data-fenster="0,' + Math.max(15, t[3]) + ',0,' + Math.max(1000, Math.ceil(Math.max.apply(null, s) / 200) * 200) + '" data-schritte="5,200" data-xname="t [min]" data-yname="s [m]"', 'Weg-Zeit-Graph'),
                   optionen: mischen([['r', satz(arten)], ['u', satz(falsch1)], ['f', satz(falsch2)]].filter(function(o, i, l){ return l.findIndex(function(p){ return p[1] === o[1]; }) === i; })), muster: '{w}' }; },
        richtig: function(A, e){ return e.w === 'r'; },
        fehler: function(A){ return A.optionen.filter(function(o){ return o[0] !== 'r'; }).map(function(o){ return [{ w: o[0] }, o[0] === 'u' ? 'Reihenfolge' : 'Steigung']; }); },
        pruefen: function(A, e){
          if (e.w === 'u') return 'Die <b>Reihenfolge</b> stimmt nicht: Der Graph wird von links nach rechts gelesen, wie die Zeit läuft.';
          return 'Lies die <b>Steigung</b> jedes Abschnitts: steil = schnell, flach = langsam, waagrecht = Pause, fallend = zurück zum Start.'; },
        tipps: function(A){ return ['Lies den Graphen von links nach rechts, Abschnitt für Abschnitt.', 'Waagrecht heisst: Die Entfernung bleibt gleich. Fallend heisst: näher zum Start.']; },
        loesung: function(A){ return '\\text{' + A.optionen.filter(function(o){ return o[0] === 'r'; })[0][1] + '}'; } },

      /* ── Kapitel 4 ── */
      'restweg': { felder: ['z', 'r'],
        schl: function(A){ return 're|' + A.L + '|' + A.v; },
        eingabe: function(A){ return { z: bWert(A.z).replace('−', '-'), r: bWert(A.r).replace('−', '-') }; },
        neu: function(){
          var v = zufall([4, 5, 6, 8, 10, 12, 15, 16, 20]), T = zufall([2, 3, 4]), L = v * T + zufall([0, v, 2 * v]), t = zufall([0.5, 1, 1.5, 2, 2.5]);
          if (t >= L / v) return TYPEN.restweg.neu();
          var zz = bMul(B(v), bDez(t));
          return { L: L, v: v, t: t, z: zz, r: bSub(B(L), zz), text: 'Eine Velotour ist ' + L + ' km lang. Du fährst gleichmässig ' + v + ' km/h. Wie weit bist du nach ' + t + ' h gefahren, und wie weit ist es dann noch bis zum Ziel?',
                   muster: 'zurückgelegt {z} km &nbsp; noch {r} km' }; },
        richtig: function(A, e){ return bEq(e.z, A.z) && bEq(e.r, A.r); },
        fehler: function(A){ return bEq(A.z, A.r) ? [[{ z: String(A.L), r: '0' }, 'Ziel']] : [[{ z: bWert(A.r).replace('−', '-'), r: bWert(A.z).replace('−', '-') }, 'Vertauscht']]; },
        pruefen: function(A, e){
          if (bEq(e.z, A.r) && bEq(e.r, A.z)) return '<b>Vertauscht</b>: Zurückgelegt ist \\(v \\cdot t\\), noch entfernt ist der Rest bis zum Ziel.';
          var t = [];
          if (!bEq(e.z, A.z)) t.push('Zurückgelegt: \\(s = v \\cdot t = ' + A.v + ' \\cdot ' + A.t + '\\).');
          if (!bEq(e.r, A.r)) t.push('Noch entfernt: die ganze Strecke minus das Gefahrene; zurückgelegt plus noch entfernt gibt immer \\(' + A.L + '\\) km bis zum <b>Ziel</b>.');
          return t.join(' '); },
        tipps: function(A){ return ['Zurückgelegt: \\(v \\cdot t\\). Noch entfernt: Strecke minus zurückgelegt.', '\\(' + A.v + ' \\cdot ' + A.t + ' = ' + bWertTex(A.z) + '\\)']; },
        loesung: function(A){ return A.v + ' \\cdot ' + A.t + ' = ' + bWertTex(A.z) + '\\ \\text{km}, \\quad ' + A.L + ' - ' + bWertTex(A.z) + ' = ' + bWertTex(A.r) + '\\ \\text{km}'; } },

      'kritik': { felder: ['w'],
        schl: function(A){ return 'kr|' + A.art + '|' + A.L.join(';'); },
        eingabe: function(A){ return { w: A.art }; },
        neu: function(){
          var art = zufall(['senk', 'zeit', 'faellt', 'ok']), a = zufall([4, 5, 6]), h = zufall([400, 600, 800]), L, y = art === 'faellt' ? 'zurückgelegter Weg [m]' : 'Entfernung von zu Hause [m]';
          if (art === 'senk') L = [[0, 0], [a, h], [a, h + 400], [a + 5, h + 400]];
          else if (art === 'zeit') L = [[0, 0], [a + 4, h], [a + 2, h + 300], [a + 6, h + 400]];
          else if (art === 'faellt') L = [[0, 0], [a, h], [a + 3, h], [a + 7, h - 300]];
          else L = [[0, 0], [a, h], [a + 3, h], [a + 7, 0]];
          L = L.map(function(p){ return p.map(String); });
          return { art: art, L: L, text: 'Was ist an diesem Diagramm falsch? Die \\(y\\)-Achse zeigt: <b>' + y + '</b>.'
                   + mini('data-linie="' + L.map(function(p){ return p.join(','); }).join(';') + '" data-fenster="0,14,0,1400" data-schritte="2,200" data-xname="t [min]" data-yname="' + y.replace(' [m]', '') + '"', 'Bewegungsdiagramm'),
                   optionen: [['senk', 'Ein Stück ist senkrecht: Weg ohne Zeit geht nicht.'], ['zeit', 'Ein Stück läuft nach links: Die Zeit läuft nie rückwärts.'],
                              ['faellt', 'Der zurückgelegte Weg kann nicht kleiner werden.'], ['ok', 'Nichts, das Diagramm ist möglich.']], muster: '{w}' }; },
        richtig: function(A, e){ return e.w === A.art; },
        fehler: function(A){ return [[{ w: A.art === 'ok' ? 'faellt' : 'ok' }, A.art === 'ok' ? 'Entfernung' : 'Schau']]; },
        pruefen: function(A, e){
          if (A.art === 'ok') return 'Die <b>Entfernung</b> von zu Hause darf kleiner werden: auf dem Rückweg. Dieses Diagramm ist möglich.';
          return '<b>Schau</b> jedes Stück an: Ist es senkrecht? Läuft es nach links? Und darf die Grösse auf der \\(y\\)-Achse kleiner werden?'; },
        tipps: function(A){ return ['Die Zeit läuft nach rechts, nie zurück, und nie ohne Weg weiter: keine senkrechten Stücke.', 'Der zurückgelegte Weg kann nur wachsen oder gleich bleiben. Eine Entfernung darf auch kleiner werden.']; },
        loesung: function(A){ return '\\text{' + { senk: 'senkrechtes Stück', zeit: 'Stück nach links', faellt: 'zurückgelegter Weg fällt', ok: 'möglich' }[A.art] + '}'; } }
    };
    window.__TYPEN = TYPEN; window.__SPERRE = SPERRE; window.__gesperrt = gesperrt;
    /* Rohe Eingaben selbst einlesen (für .claude/tools/pruef-formelsatz.mjs, das pruefen() mit den Werten aus fehler() ruft). */
    Object.keys(TYPEN).forEach(function(n){ var T = TYPEN[n], roh = T.pruefen; T.pruefen = function(A, e){
      var aus = {}; for (var f in e){ var w = e[f]; aus[f] = (w && typeof w === 'object') || f === 'w' ? w : zahlLesen(String(w)).w; }
      return roh(A, aus); }; });

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
        auf.querySelectorAll('svg.mini-gerade').forEach(function(svg){ svg.setAttribute('role', 'img'); miniBild(svg, [], []); });
        var html = A.muster;
        T.felder.forEach(function(f){
          html = html.replace('{' + f + '}', f === 'w'
            ? '<select class="ue-wahl" data-f="w" aria-label="Auswahl"><option value="">– wählen –</option>' + A.optionen.map(function(o){ return '<option value="' + o[0] + '">' + o[1] + '</option>'; }).join('') + '</select>'
            : '<input type="text" inputmode="text" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="Zahl" data-f="' + f + '" placeholder="z. B. 2/3">');
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
        var e = {}, felder = ein.querySelectorAll('[data-f]');
        for (var i = 0; i < felder.length; i++){
          var inp = felder[i], f = inp.dataset.f, roh = inp.value.trim();
          inp.classList.remove('falsch');
          if (!roh) return hinweis(f === 'w' ? 'Wähle eine Aussage.' : 'Fülle das Feld aus.');
          if (f === 'w'){ e[f] = roh; continue; }
          var zl = zahlLesen(roh);
          if (zl.kaputt){ inp.classList.add('falsch'); return hinweis(zl.kaputt); }
          e[f] = zl.w;
        }
        var gleichwertig = T.richtig(A, e);
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
