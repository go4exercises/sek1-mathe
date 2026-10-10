<script>
/* Leitprogramm Flächen, Pythagoras und Ähnlichkeit (Geometrie) — Grundseite und Höhe (Sim 1), Satz des Pythagoras (Sim 2),
   Sehne im Kreis (Sim 3), ähnliche Dreiecke (Sim 4), Übungen mit Rückmeldung und Figuren.
   Notation: Längen in cm oder m, Flächen in cm², Zahlen mit Dezimalpunkt und echtem Minus.
   Farben: blau = Figur und Grundseite, orange = Höhe bzw. Bildfigur, grün = Hypotenuse und Ergebnis, rot = Fehler.
   Gerüst: scripts/lp/bewegung/seite.js. */
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
  function fr(v){ return Math.abs(v % 1) > 1e-9 ? v.toFixed(2) : String(Math.round(v)); }
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
    if (!o.ohneGitter){
      for (i = Math.ceil(x0 / sx) * sx; i <= x1 + 1e-9; i += sx) el(g, 'line', { x1: X(i), y1: 0, x2: X(i), y2: H, 'class': 'gitter' });
      for (i = Math.ceil(y0 / sy) * sy; i <= y1 + 1e-9; i += sy) el(g, 'line', { x1: 0, y1: Y(i), x2: W, y2: Y(i), 'class': 'gitter' });
    }
    var ax = Math.max(y0, Math.min(y1, 0)), ay = Math.max(x0, Math.min(x1, 0));
    if (!o.ohneAchsen){
      el(g, 'line', { x1: 0, y1: Y(ax), x2: W, y2: Y(ax), 'class': 'achse' });
      el(g, 'line', { x1: X(ay), y1: 0, x2: X(ay), y2: H, 'class': 'achse' });
      el(g, 'polygon', { points: W + ',' + Y(ax) + ' ' + (W - 7) + ',' + (Y(ax) - 3.5) + ' ' + (W - 7) + ',' + (Y(ax) + 3.5), 'class': 'pfeil' });
      el(g, 'polygon', { points: X(ay) + ',0 ' + (X(ay) - 3.5) + ',7 ' + (X(ay) + 3.5) + ',7', 'class': 'pfeil' });
      (o.xm || []).forEach(function(t){ el(g, 'text', { x: X(t), y: Y(ax) + 14, 'text-anchor': 'middle', 'class': 'skala' }, z(t)); });
      (o.ym || []).forEach(function(t){ el(g, 'text', { x: X(ay) - 5, y: Y(t) + 4, 'text-anchor': 'end', 'class': 'skala' }, z(t)); });
    }
    var ebene = el(svg, 'g', {});
    if (!o.ohneAchsen){
      el(svg, 'text', { x: W - 2, y: Y(ax) - 7, 'text-anchor': 'end', 'class': 'achsname' }, o.xname || 'x');
      el(svg, 'text', { x: X(ay) + 7, y: 10, 'text-anchor': 'start', 'class': 'achsname' }, o.yname != null ? o.yname : 'y');
    }
    return {
      X: X, Y: Y, o: o, ebene: ebene,
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

  /* ---------- Geometrie-Helfer: Vieleck, Kreis, rechter Winkel, Beschriftung (in Fensterkoordinaten) ---------- */
  function Geo(svg, o){
    o.ohneAchsen = true;
    var k = Achsen(svg, o), ebene = k.ebene;
    function pt(p){ return k.X(p[0]).toFixed(1) + ',' + k.Y(p[1]).toFixed(1); }
    k.vieleck = function(pk, cls){ return el(ebene, 'polygon', { points: pk.map(pt).join(' '), 'class': cls }); };
    k.kreis = function(m, r, cls){ return el(ebene, 'circle', { cx: k.X(m[0]), cy: k.Y(m[1]), r: Math.abs(k.X(r) - k.X(0)), 'class': cls }); };
    k.rechts = function(p, u, v, q){            /* Zeichen für den rechten Winkel an p, Richtungen u, v (Einheitsvektoren), q in Einheiten */
      var a = [p[0] + u[0] * q, p[1] + u[1] * q], b = [a[0] + v[0] * q, a[1] + v[1] * q], c = [p[0] + v[0] * q, p[1] + v[1] * q];
      el(ebene, 'polyline', { points: [a, b, c].map(pt).join(' '), 'class': 'linie grau', fill: 'none' }); };
    k.marke = function(p, s, cls, dx, dy){ el(ebene, 'text', { x: k.X(p[0]) + (dx || 0), y: k.Y(p[1]) + (dy || 0), 'text-anchor': 'middle', 'class': 'p-text ' + (cls || '') }, s); };
    return k;
  }
  function lang(p, q){ return Math.hypot(q[0] - p[0], q[1] - p[1]); }
  function mitte(p, q){ return [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2]; }
  /* Zahl für die Live-Anzeige: ganz oder auf eine Stelle mit ≈ */
  function ca(v){ return Math.abs(v - Math.round(v)) < 1e-9 ? '= ' + z(v) : '≈ ' + z(Math.round(v * 10) / 10); }

  /* ════════ Sim 1 — Grundseite und Höhe ════════
     Dreieck A(0|0), B(g|0), C(s|h) oder Parallelogramm A, B, B + (s|h), (s|h). Die Spitze verschieben ändert die
     schrägen Seiten, nicht die Fläche. Höhe gestrichelt, notfalls auf der verlängerten Grundseite. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]'), wahl = fig.querySelector('#s1-typ');
    var O = { w: 320, h: 176, rl: 4, x0: -5, x1: 15, y0: -1, y1: 10, sx: 1, sy: 1 };
    function zustand(){ return { typ: wahl.value, g: wertR(fig, 's1-g'), h: wertR(fig, 's1-h'), s: wertR(fig, 's1-s') }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's1-g', Z.g + ' cm'); zeigeWert(fig, 's1-h', Z.h + ' cm'); zeigeWert(fig, 's1-s', Z.s + ' cm');
      var k = Geo(svg, O), A = [0, 0], Bp = [Z.g, 0], C = [Z.s, Z.h], D = [Z.g + Z.s, Z.h];
      var pk = Z.typ === 'd' ? [A, Bp, C] : [A, Bp, D, C];
      k.vieleck(pk, 'flaeche blau');
      var fuss = [Z.s, 0];
      if (Z.s < 0 || Z.s > Z.g) k.strecke(Math.min(0, Z.s), 0, Math.max(Z.g, Z.s), 0, 'linie grau gestrichelt');
      k.strecke(Z.s, 0, Z.s, Z.h, 'linie orange gestrichelt'); k.rechts(fuss, [Z.s > Z.g / 2 ? -1 : 1, 0], [0, 1], 0.45);
      k.marke(mitte(A, Bp), 'g = ' + Z.g, 'blau', 0, 15);
      k.marke(mitte(fuss, C), 'h = ' + Z.h, 'orange', Z.s < Z.g / 2 ? 24 : -24, 4);
      var sl = lang(A, C);
      k.marke(mitte(A, C), z(Math.round(sl * 10) / 10), 'grau', Z.s < Z.g / 2 ? -20 : 0, Z.s < Z.g / 2 ? -2 : -10);
      var F = Z.typ === 'd' ? Z.g * Z.h / 2 : Z.g * Z.h;
      formel.innerHTML = (Z.typ === 'd' ? 'Dreieck: A = g · h : 2 = ' + Z.g + ' · ' + Z.h + ' : 2' : 'Parallelogramm: A = g · h = ' + Z.g + ' · ' + Z.h) + ' = <b>' + z(F) + ' cm²</b>'
        + ' <span class="grau">(schräge Seite links ≈ ' + z(Math.round(sl * 10) / 10) + ' cm)</span>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, [
      { text: 'Dreieck mit Grundseite 8 cm und Fläche 16 cm². Stell die passende Höhe ein.', ok: function(Z){ return Z.typ === 'd' && Z.g === 8 && Z.h === 4; } },
      { text: 'Dreieck, g = 6 cm, h = 4 cm. Schieb die Spitze, bis die rechte Seite senkrecht steht. Wie gross ist die Fläche jetzt?', ok: function(Z){ return Z.typ === 'd' && Z.g === 6 && Z.h === 4 && Z.s === 6; } },
      { text: 'Parallelogramm mit Grundseite 5 cm und Fläche 20 cm². Stell es ein.', ok: function(Z){ return Z.typ === 'p' && Z.g === 5 && Z.h === 4; } },
      { text: 'Dreieck, g = 10 cm, h = 3 cm, die Spitze liegt <b>neben</b> der Grundseite. Wo steht die Höhe jetzt?', ok: function(Z){ return Z.typ === 'd' && Z.g === 10 && Z.h === 3 && (Z.s < 0 || Z.s > 10); } },
      { text: 'Parallelogramm mit g = 4 cm, Fläche 24 cm² und um 3 cm verschobener Oberseite.', ok: function(Z){ return Z.typ === 'p' && Z.g === 4 && Z.h === 6 && Z.s === 3; } }
    ], sim);
    fig.querySelectorAll('input, select').forEach(function(i){ i.addEventListener('input', zeichnen); i.addEventListener('change', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 2 — Satz des Pythagoras ════════
     Katheten a (waagrecht) und b (senkrecht), Quadrate über allen drei Seiten. Massstab passt sich an. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    function zustand(){ return { a: wertR(fig, 's2-a'), b: wertR(fig, 's2-b') }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's2-a', Z.a + ' cm'); zeigeWert(fig, 's2-b', Z.b + ' cm');
      var a = Z.a, b = Z.b, c2 = a * a + b * b, c = Math.sqrt(c2);
      var L = -b - 1, R = a + b + 1, U = -a - 1, Ob = a + b + 1, sp = Math.max(R - L, Ob - U);
      var k = Geo(svg, { w: 300, h: 300, rl: 4, x0: L, x1: L + sp, y0: U, y1: U + sp, ohneGitter: true });
      var C = [0, 0], A = [a, 0], Bq = [0, b];
      k.vieleck([C, A, [a, -a], [0, -a]], 'flaeche blau');
      k.vieleck([C, Bq, [-b, b], [-b, 0]], 'flaeche orange');
      k.vieleck([A, Bq, [b, a + b], [a + b, a]], 'flaeche gruen');
      k.vieleck([C, A, Bq], 'flaeche tinte');
      k.rechts(C, [1, 0], [0, 1], Math.max(0.6, sp / 30));
      k.marke([a / 2, -a / 2], 'a² = ' + a * a, 'blau', 0, 4);
      k.marke([-b / 2, b / 2], 'b² = ' + b * b, 'orange', 0, 4);
      k.marke([(a + b) / 2 + a / 4, (a + b) / 2 + b / 4], 'c² = ' + c2, 'gruen', 0, 4);
      formel.innerHTML = 'a² + b² = ' + a * a + ' + ' + b * b + ' = ' + c2 + ' &nbsp;→&nbsp; <b>c ' + ca(c) + ' cm</b>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    function paar(x, y){ return function(Z){ return (Z.a === x && Z.b === y) || (Z.a === y && Z.b === x); }; }
    pr = Leiste(fig, [
      { text: 'Eine Kathete ist 9 cm lang. Wie lang muss die andere sein, damit c = 15 cm wird?', ok: paar(9, 12) },
      { text: 'c = 17 cm, eine Kathete 8 cm. Stell die andere ein.', ok: paar(8, 15) },
      { text: 'c = 20 cm, eine Kathete 12 cm. Stell die andere ein.', ok: paar(12, 16) },
      { text: 'c = 25 cm, eine Kathete 7 cm. Stell die andere ein.', ok: paar(7, 24) },
      { text: 'Finde ein rechtwinkliges Dreieck mit ganzzahligen Katheten und c = 29 cm.', ok: paar(20, 21) }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 3 — Sehne im Kreis ════════
     Kreis mit Radius r, waagrechte Sehne im Abstand d unter dem Mittelpunkt, darunter Wasser. Hilfsdreieck: d, s/2, r. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    function zustand(){ var r = wertR(fig, 's3-r'), d = Math.min(wertR(fig, 's3-d'), r); return { r: r, d: d }; }
    function zeichnen(){
      var Z = zustand(), r = Z.r, d = Z.d, hs = Math.sqrt(r * r - d * d), s = 2 * hs;
      zeigeWert(fig, 's3-r', r + ' cm'); zeigeWert(fig, 's3-d', d + ' cm');
      var k = Geo(svg, { w: 300, h: 300, rl: 4, x0: -16, x1: 16, y0: -16, y1: 16, ohneGitter: true });
      /* Wasser: Kreissegment unter der Sehne */
      var w0 = Math.atan2(-d, hs), w1 = Math.PI - w0, seg = [];
      for (var i = 0; i <= 80; i++){ var t = w1 + (2 * Math.PI - (w1 - w0)) * i / 80; seg.push([r * Math.cos(t), r * Math.sin(t)]); }
      k.vieleck(seg, 'flaeche wasser');
      k.kreis([0, 0], r, 'linie tinte');
      k.strecke(-hs, -d, hs, -d, 'linie blau');
      k.strecke(0, 0, 0, -d, 'linie orange'); k.strecke(0, 0, hs, -d, 'linie gruen');
      if (d > 0.5 && hs > 0.5) k.rechts([0, -d], [1, 0], [0, 1], 0.9);
      k.punkt(0, 0, 'pkt');
      k.marke([hs / 2, -d], 's/2', 'blau', 0, 16); k.marke([0, -d / 2], 'd', 'orange', -10, 4); k.marke([hs / 2, -d / 2], 'r', 'gruen', 10, -6);
      formel.innerHTML = '(s/2)² = r² − d² = ' + r * r + ' − ' + d * d + ' = ' + (r * r - d * d) + ' &nbsp;→&nbsp; s/2 ' + ca(hs) + ', <b>Sehne s ' + ca(s) + ' cm</b>'
        + ' &nbsp;·&nbsp; <span class="grau">Wassertiefe r − d = ' + (r - d) + ' cm</span>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, [
      { text: 'Kreis mit r = 13 cm. Schieb die Sehne, bis sie 24 cm lang ist.', ok: function(Z){ return Z.r === 13 && Z.d === 5; } },
      { text: 'r = 5 cm, Sehne 8 cm. Wie weit ist sie vom Mittelpunkt entfernt?', ok: function(Z){ return Z.r === 5 && Z.d === 3; } },
      { text: 'r = 15 cm, Sehne 18 cm. Stell den Abstand ein.', ok: function(Z){ return Z.r === 15 && Z.d === 12; } },
      { text: 'r = 10 cm, Abstand 8 cm. Wie lang ist die Sehne?', ok: function(Z){ return Z.r === 10 && Z.d === 8; } },
      { text: 'Ein Rohr mit r = 13 cm, der Wasserspiegel ist 10 cm breit. Wie tief ist das Wasser?', ok: function(Z){ return Z.r === 13 && Z.d === 12; } }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 4 — Ähnliche Dreiecke ════════
     Rechtwinkliges Dreieck mit Katheten 4 und 3, gestreckt von der Ecke A mit Faktor k. Längen × k, Fläche × k². */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    function zustand(){ return { k: wertR(fig, 's4-k') }; }
    function zeichnen(){
      var Z = zustand(), q = Z.k; zeigeWert(fig, 's4-k', z(q));
      var k = Geo(svg, { w: 320, h: 240, rl: 4, x0: -0.5, x1: 12.83, y0: -0.5, y1: 9.5, sx: 1, sy: 1 });
      k.vieleck([[0, 0], [4 * q, 0], [4 * q, 3 * q]], 'flaeche orange');
      k.vieleck([[0, 0], [4, 0], [4, 3]], 'flaeche blau');
      k.marke([2 * q, 0], z(4 * q), 'orange', 0, 15); k.marke([4 * q, 1.5 * q], z(3 * q), 'orange', 14, 4); k.marke([2 * q, 1.5 * q], z(5 * q), 'orange', -14, -6);
      k.marke([2, 0], '4', 'blau', 0, -4);
      formel.innerHTML = 'k = ' + z(q) + ': Seiten 4, 3, 5 → <b>' + z(4 * q) + ', ' + z(3 * q) + ', ' + z(5 * q) + '</b> &nbsp;·&nbsp; Fläche 6 cm² → <b>' + z(6 * q * q) + ' cm²</b> (mal ' + z(q * q) + ' = k²)';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, [
      { text: 'Bei welchem Streckfaktor k wird die Fläche 24 cm²?', ok: function(Z){ return Z.k === 2; } },
      { text: 'Die Fläche soll 9-mal so gross werden. Welches k?', ok: function(Z){ return Z.k === 3; } },
      { text: 'Die Kathete 3 cm soll 4.5 cm lang werden.', ok: function(Z){ return Z.k === 1.5; } },
      { text: 'Die Fläche soll ein Viertel so gross werden.', ok: function(Z){ return Z.k === 0.5; } },
      { text: 'Die Hypotenuse soll 12.5 cm lang werden.', ok: function(Z){ return Z.k === 2.5; } }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ---------- Minibilder (wie in den anderen Leitprogrammen) ---------- */
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
     Zahlenfelder exakt (2/3, −1.5, 4). Feld w: Auswahl (select). Fehlversuch → gezielte Diagnose. Tipps in drei Stufen.
     Testhaken: box.__aufgabe, box.__typ. Figuren stehen als fertiges SVG im Aufgabentext (figur()). */
  (function(){
    var ALLE = document.querySelectorAll('.uebung[data-typ]'); if (!ALLE.length) return;

    /* Figur als SVG-Text: Bereich aus allen Punkten, gleicher Massstab in x und y, Breite höchstens 230 px. */
    function figur(o, label){
      var alle = [];
      (o.vl || []).forEach(function(v){ alle = alle.concat(v[0]); });
      (o.st || []).forEach(function(s){ alle.push(s[0], s[1]); });
      (o.kr || []).forEach(function(c){ alle.push([c[0][0] - c[1], c[0][1] - c[1]], [c[0][0] + c[1], c[0][1] + c[1]]); });
      var xs = alle.map(function(p){ return p[0]; }), ys = alle.map(function(p){ return p[1]; });
      var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
      var m = 160 / Math.max(x1 - x0, (y1 - y0) * 1.35, 1e-9), R = 26, W = (x1 - x0) * m + 2 * R, H = (y1 - y0) * m + 2 * R;
      function X(x){ return (R + (x - x0) * m).toFixed(1); } function Y(y){ return (R + (y1 - y) * m).toFixed(1); }
      var s = '<svg class="mini-figur" viewBox="0 0 ' + W.toFixed(0) + ' ' + H.toFixed(0) + '" width="' + W.toFixed(0) + '" role="img" aria-label="' + label + '">';
      (o.vl || []).forEach(function(v){ s += '<polygon points="' + v[0].map(function(p){ return X(p[0]) + ',' + Y(p[1]); }).join(' ') + '" class="' + v[1] + '"/>'; });
      (o.kr || []).forEach(function(c){ s += '<circle cx="' + X(c[0][0]) + '" cy="' + Y(c[0][1]) + '" r="' + (c[1] * m).toFixed(1) + '" class="' + c[2] + '"/>'; });
      (o.st || []).forEach(function(t){ s += '<line x1="' + X(t[0][0]) + '" y1="' + Y(t[0][1]) + '" x2="' + X(t[1][0]) + '" y2="' + Y(t[1][1]) + '" class="' + t[2] + '"/>'; });
      (o.re || []).forEach(function(r){ var p = r[0], u = r[1], v = r[2], q = 9 / m;
        var a = [p[0] + u[0] * q, p[1] + u[1] * q], b = [a[0] + v[0] * q, a[1] + v[1] * q], c = [p[0] + v[0] * q, p[1] + v[1] * q];
        s += '<polyline points="' + [a, b, c].map(function(t){ return X(t[0]) + ',' + Y(t[1]); }).join(' ') + '" class="linie grau" fill="none"/>'; });
      (o.tx || []).forEach(function(t){ s += '<text x="' + (+X(t[0][0]) + (t[3] || 0)).toFixed(1) + '" y="' + (+Y(t[0][1]) + (t[4] || 0)).toFixed(1) + '" text-anchor="middle" class="p-text ' + (t[2] || '') + '">' + t[1] + '</text>'; });
      return '<span class="mini-reihe">' + s + '</svg></span>';
    }

    /* Feste Aufgaben (Clips, Festhalten, Erkundungen, Kapitelaufgaben, Gesamttest): nie als Zufallsübung. */
    var SPERRE = [
      'fl|d|6|4', 'fl|d|8|5', 'fl|p|7|4', 'fl|t|9|5|4', 'fl|d|10|3', 'fl|d|9|6', 'fl|p|12|5', 'fl|t|11|7|6', 'fl|d|12|8', 'fl|d|10|7', 'fl|p|9|4', 'fl|t|8|4|5',
      'fl|p|6|4', 'fl|t|14|8|5', 'fl|p|9|6',
      'zu|h|6|4|3', 'zu|l|8|6|3|2', 'zu|l|6|5|2|2', 'zu|h|10|6|4',
      'hy|6|8', 'hy|3|4', 'hy|9|12', 'hy|12|16', 'hy|20|21', 'hy|15|20', 'hy|5|12', 'hy|16|30', 'hy|8|15', 'hy|7|24',
      'ka|10|6', 'ka|17|8', 'ka|25|7', 'ka|26|10', 'ka|13|5', 'ka|41|9', 'ka|20|12', 'ka|15|9',
      'hd|r|20|21', 'hd|r|8|15', 'hd|r|12|35', 'hd|g|16|17', 'hd|g|30|25', 'hd|g|18|15', 'hd|g|42|29', 'hd|l|6.5|2.5', 'hd|l|5|1.4',
      'se|d|10|16', 'se|s|13|5', 'se|d|5|8', 'se|d|15|18', 'se|s|10|8', 'se|d|13|10', 'se|d|26|48', 'se|d|17|30', 'se|s|13|12', 'se|d|10|12', 'se|d|25|48', 'se|d|15|24',
      'ae|3|4|5|2', 'ae|4|6|8|12', 'ae|5|7|9|10',
      'ff|A|6|2', 'ff|A|10|3', 'ff|A|8|3', 'ff|k|16', 'ff|A|15|3'
    ];
    function gesperrt(T, A){ return !!T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }
    function d(v){ return bWert(bDez(v)); }
    function eing(a){ return bWert(a).replace('−', '-'); }
    var TRIPEL = [[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25], [20, 21, 29], [9, 40, 41], [12, 35, 37]];
    function tripel(max){
      var l = [];
      TRIPEL.forEach(function(t){ for (var f = 0.5; f * t[2] <= max; f += 0.5) if (f % 1 === 0 || t[2] <= 13) l.push([t[0] * f, t[1] * f, t[2] * f]); });
      return zufall(l);
    }

    var TYPEN = {
      /* ── Kapitel 1 ── */
      'flaeche': { felder: ['A'],
        schl: function(A){ return 'fl|' + A.art + '|' + A.g + '|' + (A.art === 't' ? A.c + '|' : '') + A.h; },
        eingabe: function(A){ return { A: eing(A.F) }; },
        neu: function(){
          var art = zufall(['d', 'd', 'p', 't']), g = zufallG(4, 14), h = zufallG(3, Math.max(4, Math.min(10, g))), c = art === 't' ? zufallG(2, g - 2) : 0, s = zufallG(1, 4);
          var F = art === 'd' ? B(g * h, 2) : art === 'p' ? B(g * h) : B((g + c) * h, 2), schraeg = Math.round(Math.hypot(s, h) * 10) / 10;
          if (F[1] > 2 || schraeg === h) return TYPEN.flaeche.neu();
          var pk = art === 'd' ? [[0, 0], [g, 0], [s, h]] : art === 'p' ? [[0, 0], [g, 0], [g + s, h], [s, h]] : [[0, 0], [g, 0], [s + c, h], [s, h]];
          var o = { vl: [[pk, 'flaeche blau']], st: [[[s, 0], [s, h], 'linie orange gestrichelt']], re: [[[s, 0], [1, 0], [0, 1]]],
                    tx: [[[g / 2, 0], g + ' cm', 'blau', 0, 15], [[s, h / 2], h + ' cm', 'orange', 22, 4], [[s / 2, h / 2], schraeg + ' cm', 'grau', -24, 0]] };
          if (art === 't') o.tx.push([[s + c / 2, h], c + ' cm', 'blau', 0, -7]);
          var name = { d: 'Dreieck', p: 'Parallelogramm', t: 'Trapez' }[art], gen = { d: 'Dreiecks', p: 'Parallelogramms', t: 'Trapezes' }[art];
          return { art: art, g: g, h: h, c: c, s: s, schraeg: schraeg, F: F, text: 'Wie gross ist die Fläche dieses ' + gen + ' (in cm²)?' + figur(o, name + ' mit Grundseite ' + g + ' cm, Höhe ' + h + ' cm, schräger Seite ' + schraeg + ' cm'), muster: 'A = {A} cm²' }; },
        richtig: function(A, e){ return bEq(e.A, A.F); },
        fehler: function(A){
          var f = [], mit = A.art === 'd' ? bDez(A.g * A.schraeg / 2) : A.art === 'p' ? bDez(A.g * A.schraeg) : bDez((A.g + A.c) * A.schraeg / 2);
          f.push([{ A: eing(mit) }, 'Höhe']);
          if (A.art === 'd') f.push([{ A: String(A.g * A.h) }, 'halb']);
          if (A.art === 't') f.push([{ A: String((A.g + A.c) * A.h) }, 'Mittel']);
          return f; },
        pruefen: function(A, e){
          if (bEq(e.A, bDez(A.art === 'd' ? A.g * A.schraeg / 2 : A.art === 'p' ? A.g * A.schraeg : (A.g + A.c) * A.schraeg / 2))) return 'Du hast mit der schrägen Seite gerechnet. Die <b>Höhe</b> steht senkrecht auf der Grundseite (gestrichelt).';
          if (A.art === 'd' && bEq(e.A, B(A.g * A.h))) return 'Das ist die Fläche eines Parallelogramms. Ein Dreieck ist nur <b>halb</b> so gross.';
          if (A.art === 't' && bEq(e.A, B((A.g + A.c) * A.h))) return 'Beim Trapez nimmst du das <b>Mittel</b> der beiden parallelen Seiten, also die Summe durch 2.';
          return 'Welche Formel gehört zu dieser Figur, und welche Strecke ist die Höhe?'; },
        tipps: function(A){ return [A.art === 'd' ? '\\(A = \\dfrac{g \\cdot h}{2}\\)' : A.art === 'p' ? '\\(A = g \\cdot h\\)' : '\\(A = \\dfrac{a + c}{2} \\cdot h\\)', 'Die Höhe ist \\(' + A.h + '\\) cm, nicht die schräge Seite.']; },
        loesung: function(A){ return A.art === 'd' ? '\\dfrac{' + A.g + ' \\cdot ' + A.h + '}{2} = ' + bWertTex(A.F) : A.art === 'p' ? A.g + ' \\cdot ' + A.h + ' = ' + bWertTex(A.F) : '\\dfrac{' + A.g + ' + ' + A.c + '}{2} \\cdot ' + A.h + ' = ' + bWertTex(A.F); } },

      'zusammen': { felder: ['A'],
        schl: function(A){ return 'zu|' + A.art + '|' + A.p.join('|'); },
        eingabe: function(A){ return { A: eing(A.F) }; },
        neu: function(){
          var art = zufall(['h', 'l']), o, F, p, text, f2;
          if (art === 'h'){
            var b = zufallG(4, 12), hr = zufallG(3, 8), hd = zufallG(2, 6); p = [b, hr, hd]; F = B(b * hr * 2 + b * hd, 2); f2 = B(b * hr + b * hd);
            if (F[1] > 2) return TYPEN.zusammen.neu();
            o = { vl: [[[[0, 0], [b, 0], [b, hr], [0, hr]], 'flaeche blau'], [[[0, hr], [b, hr], [b / 2, hr + hd]], 'flaeche orange']], st: [[[b / 2, hr], [b / 2, hr + hd], 'linie orange gestrichelt']],
                  tx: [[[b / 2, 0], b + ' cm', 'blau', 0, 15], [[b, hr / 2], hr + ' cm', 'blau', 20, 4], [[b / 2, hr + hd / 2], hd + ' cm', 'orange', 16, 4]] };
            text = 'Ein Haus aus Rechteck und Giebeldreieck. Wie gross ist die ganze Fläche (in cm²)?';
          } else {
            var a = zufallG(6, 12), bb = zufallG(5, 10), x = zufallG(2, a - 3), y = zufallG(2, bb - 2); p = [a, bb, x, y]; F = B(a * bb - x * y); f2 = B(a * bb + x * y);
            o = { vl: [[[[0, 0], [a, 0], [a, bb - y], [a - x, bb - y], [a - x, bb], [0, bb]], 'flaeche blau']], st: [[[a - x, bb], [a, bb], 'linie grau gestrichelt'], [[a, bb - y], [a, bb], 'linie grau gestrichelt']],
                  tx: [[[a / 2, 0], a + ' cm', 'blau', 0, 15], [[0, bb / 2], bb + ' cm', 'blau', -22, 4], [[a - x / 2, bb], x + ' cm', 'grau', 0, -7], [[a, bb - y / 2], y + ' cm', 'grau', 20, 4]] };
            text = 'Aus einem Rechteck ist eine Ecke ausgeschnitten. Wie gross ist die Fläche der Figur (in cm²)?';
          }
          return { art: art, p: p, F: F, f2: f2, text: text + figur(o, art === 'h' ? 'Haus aus Rechteck und Dreieck' : 'Rechteck mit ausgeschnittener Ecke'), muster: 'A = {A} cm²' }; },
        richtig: function(A, e){ return bEq(e.A, A.F); },
        fehler: function(A){ return [[{ A: eing(A.f2) }, A.art === 'h' ? 'Dreieck' : 'abziehen']]; },
        pruefen: function(A, e){
          if (bEq(e.A, A.f2)) return A.art === 'h' ? 'Das <b>Dreieck</b> ist nur halb so gross wie ein Rechteck mit gleicher Grundseite und Höhe.' : 'Die ausgeschnittene Ecke fehlt: Du musst sie <b>abziehen</b>, nicht dazuzählen.';
          return A.art === 'h' ? 'Zerlege: Rechteck plus Dreieck. Welche Masse gehören zu welchem Teil?' : 'Ergänze zum ganzen Rechteck und zieh die Ecke ab, oder zerlege in zwei Rechtecke.'; },
        tipps: function(A){ return A.art === 'h' ? ['Rechteck: \\(' + A.p[0] + ' \\cdot ' + A.p[1] + '\\)', 'Dreieck: \\(\\dfrac{' + A.p[0] + ' \\cdot ' + A.p[2] + '}{2}\\)'] : ['Ganzes Rechteck: \\(' + A.p[0] + ' \\cdot ' + A.p[1] + '\\)', 'Ecke: \\(' + A.p[2] + ' \\cdot ' + A.p[3] + '\\)']; },
        loesung: function(A){ return A.art === 'h' ? A.p[0] + ' \\cdot ' + A.p[1] + ' + \\dfrac{' + A.p[0] + ' \\cdot ' + A.p[2] + '}{2} = ' + bWertTex(A.F) : A.p[0] + ' \\cdot ' + A.p[1] + ' - ' + A.p[2] + ' \\cdot ' + A.p[3] + ' = ' + bWertTex(A.F); } },

      /* ── Kapitel 2 ── */
      'hypotenuse': { felder: ['c'],
        schl: function(A){ return 'hy|' + Math.min(A.a, A.b) + '|' + Math.max(A.a, A.b); },
        eingabe: function(A){ return { c: String(A.c) }; },
        neu: function(){
          var t = tripel(60), dreh = Math.random() < 0.5, a = dreh ? t[1] : t[0], b = dreh ? t[0] : t[1];
          var o = { vl: [[[[0, 0], [a, 0], [0, b]], 'flaeche blau']], re: [[[0, 0], [1, 0], [0, 1]]], tx: [[[a / 2, 0], a + ' cm', 'blau', 0, 15], [[0, b / 2], b + ' cm', 'blau', -22, 4], [[a / 2, b / 2], 'c', 'gruen', 10, -6]] };
          return { a: a, b: b, c: t[2], text: 'Wie lang ist die Hypotenuse c?' + figur(o, 'rechtwinkliges Dreieck mit Katheten ' + a + ' cm und ' + b + ' cm'), muster: 'c = {c} cm' }; },
        richtig: function(A, e){ return bEq(e.c, bDez(A.c)); },
        fehler: function(A){ return [[{ c: String(A.a + A.b) }, 'Quadrate'], [{ c: String(A.a * A.a + A.b * A.b) }, 'Wurzel']]; },
        pruefen: function(A, e){
          if (bEq(e.c, bDez(A.a + A.b))) return 'Die Seiten addieren sich nicht. Die <b>Quadrate</b> der Katheten ergeben das Quadrat der Hypotenuse.';
          if (bEq(e.c, bDez(A.a * A.a + A.b * A.b))) return 'Das ist \\(c^2\\). Zieh noch die <b>Wurzel</b>.';
          return 'Rechne \\(a^2 + b^2\\) und zieh dann die Wurzel.'; },
        tipps: function(A){ return ['\\(c^2 = ' + A.a + '^2 + ' + A.b + '^2\\)', '\\(c^2 = ' + (A.a * A.a + A.b * A.b) + '\\)']; },
        loesung: function(A){ return 'c = \\sqrt{' + A.a + '^2 + ' + A.b + '^2} = \\sqrt{' + (A.a * A.a + A.b * A.b) + '} = ' + A.c; } },

      'kathete': { felder: ['b'],
        schl: function(A){ return 'ka|' + A.c + '|' + Math.min(A.a, A.b); },
        eingabe: function(A){ return { b: String(A.b) }; },
        neu: function(){
          var t = tripel(60), dreh = Math.random() < 0.5, a = dreh ? t[1] : t[0], b = dreh ? t[0] : t[1], c = t[2];
          var o = { vl: [[[[0, 0], [b, 0], [0, a]], 'flaeche blau']], re: [[[0, 0], [1, 0], [0, 1]]], tx: [[[b / 2, 0], 'b', 'orange', 0, 15], [[0, a / 2], a + ' cm', 'blau', -22, 4], [[b / 2, a / 2], c + ' cm', 'gruen', 18, -6]] };
          return { a: a, b: b, c: c, text: 'Wie lang ist die Kathete b?' + figur(o, 'rechtwinkliges Dreieck mit Hypotenuse ' + c + ' cm und Kathete ' + a + ' cm'), muster: 'b = {b} cm' }; },
        richtig: function(A, e){ return bEq(e.b, bDez(A.b)); },
        fehler: function(A){ return [[{ b: String(A.c - A.a) }, 'Quadrate'], [{ b: String(A.c * A.c - A.a * A.a) }, 'Wurzel']]; },
        pruefen: function(A, e){
          if (bEq(e.b, bDez(A.c - A.a))) return 'Die Seiten subtrahieren sich nicht. Rechne mit den <b>Quadrate</b>n: \\(b^2 = c^2 - a^2\\).';
          if (bEq(e.b, bDez(A.c * A.c - A.a * A.a))) return 'Das ist \\(b^2\\). Zieh noch die <b>Wurzel</b>.';
          return 'Die Hypotenuse liegt gegenüber dem rechten Winkel. Für eine Kathete rechnest du \\(c^2 - a^2\\), nicht plus.'; },
        tipps: function(A){ return ['\\(b^2 = c^2 - a^2\\)', '\\(b^2 = ' + A.c + '^2 - ' + A.a + '^2 = ' + (A.c * A.c - A.a * A.a) + '\\)']; },
        loesung: function(A){ return 'b = \\sqrt{' + A.c + '^2 - ' + A.a + '^2} = \\sqrt{' + (A.c * A.c - A.a * A.a) + '} = ' + A.b; } },

      /* ── Kapitel 3 ── */
      'hilfsdreieck': { felder: ['x'],
        schl: function(A){ return 'hd|' + A.art + '|' + A.p.join('|'); },
        eingabe: function(A){ return { x: eing(A.x) }; },
        neu: function(){
          var art = zufall(['r', 'g', 'l']), t = tripel(50), o, text, x, p, f;
          if (art === 'r'){ p = [t[0], t[1]]; x = bDez(t[2]); f = bDez(t[0] + t[1]);
            o = { vl: [[[[0, 0], [t[0], 0], [t[0], t[1]], [0, t[1]]], 'flaeche blau']], st: [[[0, 0], [t[0], t[1]], 'linie gruen']], tx: [[[t[0] / 2, 0], t[0] + ' cm', 'blau', 0, 15], [[t[0], t[1] / 2], t[1] + ' cm', 'blau', 22, 4], [[t[0] / 2, t[1] / 2], 'd', 'gruen', -10, -6]] };
            text = 'Wie lang ist die Diagonale d des Rechtecks?'; }
          else if (art === 'g'){ p = [2 * t[0], t[2]]; x = bDez(t[1]); var ww = Math.sqrt(t[2] * t[2] - 4 * t[0] * t[0]); f = ww > 0 && (ww * 10) % 1 === 0 ? bDez(ww) : B(-1);
            o = { vl: [[[[0, 0], [2 * t[0], 0], [t[0], t[1]]], 'flaeche blau']], st: [[[t[0], 0], [t[0], t[1]], 'linie orange gestrichelt']], re: [[[t[0], 0], [1, 0], [0, 1]]],
                  tx: [[[t[0], 0], 2 * t[0] + ' cm', 'blau', 0, 15], [[t[0] / 2, t[1] / 2], t[2] + ' cm', 'blau', -22, 0], [[t[0], t[1] / 2], 'h', 'orange', 10, 4]] };
            text = 'Ein gleichschenkliges Dreieck. Wie lang ist die Höhe h?'; }
          else { var q = zufall([[1.5, 2, 2.5], [3, 4, 5], [1.2, 3.5, 3.7], [2.1, 2.8, 3.5], [1.8, 2.4, 3], [2.5, 6, 6.5], [0.7, 2.4, 2.5]]); p = [q[2], q[0]]; x = bDez(q[1]); f = bDez(q[2] - q[0]);
            o = { st: [[[0, 0], [0, q[1] * 1.15], 'linie tinte'], [[0, 0], [q[0] * 1.6, 0], 'linie tinte'], [[q[0], 0], [0, q[1]], 'linie blau']], re: [[[0, 0], [1, 0], [0, 1]]],
                  tx: [[[q[0] / 2, 0], d(q[0]) + ' m', 'blau', 0, 15], [[q[0] / 2, q[1] / 2], d(q[2]) + ' m', 'blau', 18, 0], [[0, q[1] / 2], 'h', 'orange', -10, 4]] };
            text = 'Eine Leiter lehnt an einer senkrechten Wand. Wie hoch reicht sie (h in m)?'; }
          return { art: art, p: p, x: x, f: f, text: text + figur(o, { r: 'Rechteck', g: 'gleichschenkliges Dreieck', l: 'Leiter an der Wand' }[art]), muster: (art === 'r' ? 'd' : 'h') + ' = {x} ' + (art === 'l' ? 'm' : 'cm') }; },
        richtig: function(A, e){ return bEq(e.x, A.x); },
        fehler: function(A){ return A.f[0] > 0 && !bEq(A.f, A.x) ? [[{ x: eing(A.f) }, A.art === 'r' ? 'Quadrate' : A.art === 'g' ? 'Hälfte' : 'Quadrate']] : []; },
        pruefen: function(A, e){
          if (A.art === 'g' && A.f[0] > 0 && bEq(e.x, A.f)) return 'Im Hilfsdreieck liegt nur die <b>Hälfte</b> der Grundseite, denn die Höhe teilt sie in der Mitte.';
          if (A.art !== 'g' && bEq(e.x, A.f)) return 'Längen addieren oder subtrahieren sich nicht. Rechne mit den <b>Quadrate</b>n.';
          return 'Such zuerst das rechtwinklige Hilfsdreieck: Wo ist der rechte Winkel, welche Seite ist die Hypotenuse?'; },
        tipps: function(A){ return A.art === 'r' ? ['Die Diagonale ist die Hypotenuse des halben Rechtecks.', '\\(d^2 = ' + A.p[0] + '^2 + ' + A.p[1] + '^2\\)'] : A.art === 'g' ? ['Die Höhe teilt die Grundseite in zwei Hälften von je \\(' + A.p[0] / 2 + '\\) cm.', '\\(h^2 = ' + A.p[1] + '^2 - ' + A.p[0] / 2 + '^2\\)'] : ['Die Leiter ist die Hypotenuse.', '\\(h^2 = ' + d(A.p[0]) + '^2 - ' + d(A.p[1]) + '^2\\)']; },
        loesung: function(A){ return A.art === 'r' ? 'd = \\sqrt{' + A.p[0] + '^2 + ' + A.p[1] + '^2} = ' + bWertTex(A.x) : A.art === 'g' ? 'h = \\sqrt{' + A.p[1] + '^2 - ' + A.p[0] / 2 + '^2} = ' + bWertTex(A.x) : 'h = \\sqrt{' + d(A.p[0]) + '^2 - ' + d(A.p[1]) + '^2} = ' + bWertTex(A.x); } },

      'sehne': { felder: ['x'],
        schl: function(A){ return 'se|' + A.ges + '|' + A.r + '|' + (A.ges === 's' ? A.dd : A.s); },
        eingabe: function(A){ return { x: String(A.x) }; },
        neu: function(){
          var t = tripel(40), r = t[2], dd = t[0], hs = t[1]; if (Math.random() < 0.5){ dd = t[1]; hs = t[0]; }
          var ges = zufall(['s', 'd']), x = ges === 's' ? 2 * hs : dd;
          var o = { kr: [[[0, 0], r, 'linie tinte']], st: [[[-hs, -dd], [hs, -dd], 'linie blau'], [[0, 0], [0, -dd], 'linie orange'], [[0, 0], [hs, -dd], 'linie gruen']], re: [[[0, -dd], [1, 0], [0, 1]]],
                    tx: [[[hs / 2, -dd / 2], 'r = ' + r, 'gruen', 18, -4], [[0, -dd / 2], ges === 'd' ? 'd' : 'd = ' + dd, 'orange', -24, 4], [[0, -dd], ges === 's' ? 's' : 's = ' + 2 * hs, 'blau', 0, 16]] };
          return { ges: ges, r: r, dd: dd, s: 2 * hs, x: x, text: (ges === 's' ? 'Kreis mit r = ' + r + ' cm, die Sehne hat den Abstand ' + dd + ' cm vom Mittelpunkt. Wie lang ist die Sehne s?' : 'Kreis mit r = ' + r + ' cm, die Sehne ist ' + 2 * hs + ' cm lang. Wie weit ist sie vom Mittelpunkt entfernt (d)?')
                   + figur(o, 'Kreis mit Sehne und Hilfsdreieck'), muster: (ges === 's' ? 's' : 'd') + ' = {x} cm' }; },
        richtig: function(A, e){ return bEq(e.x, bDez(A.x)); },
        fehler: function(A){ return A.ges === 's' ? [[{ x: String(A.s / 2) }, 'Hälfte']] : []; },
        pruefen: function(A, e){
          if (A.ges === 's' && bEq(e.x, bDez(A.s / 2))) return 'Das ist die <b>Hälfte</b> der Sehne. Das Hilfsdreieck enthält nur die halbe Sehne.';
          return A.ges === 's' ? 'Hilfsdreieck: Radius als Hypotenuse, Abstand und halbe Sehne als Katheten.' : 'Im Hilfsdreieck steht nur die <b>halbe</b> Sehne, \\(' + A.s / 2 + '\\) cm. Der Radius ist die Hypotenuse.'; },
        tipps: function(A){ return A.ges === 's' ? ['\\(\\left(\\tfrac{s}{2}\\right)^2 = r^2 - d^2\\)', '\\(' + A.r + '^2 - ' + A.dd + '^2 = ' + (A.r * A.r - A.dd * A.dd) + '\\)'] : ['halbe Sehne: \\(' + A.s / 2 + '\\) cm', '\\(d^2 = ' + A.r + '^2 - ' + A.s / 2 + '^2\\)']; },
        loesung: function(A){ return A.ges === 's' ? '\\tfrac{s}{2} = \\sqrt{' + A.r + '^2 - ' + A.dd + '^2} = ' + A.s / 2 + ', \\; s = ' + A.s : 'd = \\sqrt{' + A.r + '^2 - ' + A.s / 2 + '^2} = ' + A.dd; } },

      /* ── Kapitel 4 ── */
      'aehnlich': { felder: ['x'],
        schl: function(A){ return 'ae|' + A.s.join('|') + '|' + A.bild; },
        eingabe: function(A){ return { x: eing(A.x) }; },
        neu: function(){
          var s = zufall([[3, 4, 5], [4, 6, 8], [5, 7, 9], [6, 8, 9], [4, 5, 7], [2, 3, 4], [6, 9, 12]]), k = zufall([[3, 2], [2, 1], [5, 2], [3, 1], [1, 2], [4, 3]]);
          var i = zufallG(0, 2), j = (i + zufallG(1, 2)) % 3, bild = s[i] * k[0] / k[1], x = bMul(B(s[j]), B(k[0], k[1]));
          if (bild % 1 && (bild * 2) % 1) return TYPEN.aehnlich.neu();
          if (x[1] > 2) return TYPEN.aehnlich.neu();
          return { s: s, i: i, j: j, bild: bild, k: k, x: x, text: 'Ein Dreieck hat die Seiten ' + s.join(' cm, ') + ' cm. In einem dazu ähnlichen Dreieck ist die Seite, die zu ' + s[i] + ' cm gehört, ' + d(bild) + ' cm lang. Wie lang ist dort die Seite, die zu ' + s[j] + ' cm gehört?', muster: '{x} cm' }; },
        richtig: function(A, e){ return bEq(e.x, A.x); },
        fehler: function(A){ var f = bDez(A.s[A.j] + A.bild - A.s[A.i]); return bEq(f, A.x) ? [] : [[{ x: eing(f) }, 'Faktor']]; },
        pruefen: function(A, e){
          if (bEq(e.x, bDez(A.s[A.j] + A.bild - A.s[A.i]))) return 'Bei ähnlichen Figuren kommt nicht überall gleich viel dazu. Alle Längen werden mit demselben <b>Faktor</b> k multipliziert.';
          return 'Berechne zuerst den Streckfaktor \\(k = \\dfrac{\\text{Bild}}{\\text{Original}}\\).'; },
        tipps: function(A){ return ['\\(k = \\dfrac{' + d(A.bild) + '}{' + A.s[A.i] + '}\\)', 'Die gesuchte Seite: \\(' + A.s[A.j] + ' \\cdot k\\)']; },
        loesung: function(A){ return 'k = \\dfrac{' + d(A.bild) + '}{' + A.s[A.i] + '} = ' + bWertTex(B(A.k[0], A.k[1])) + ', \\quad ' + A.s[A.j] + ' \\cdot ' + bWertTex(B(A.k[0], A.k[1])) + ' = ' + bWertTex(A.x); } },

      'flaechenfaktor': { felder: ['y'],
        schl: function(A){ return 'ff|' + A.ges + '|' + (A.ges === 'A' ? A.A + '|' + A.k : A.q); },
        eingabe: function(A){ return { y: eing(A.y) }; },
        neu: function(){
          var ges = zufall(['A', 'A', 'k']), k = zufall([2, 3, 4, 5, 0.5, 1.5, 2.5, 10]), A = zufall([4, 6, 8, 10, 12, 15, 20, 24]);
          if (ges === 'A'){ var y = bMul(B(A), bMul(bDez(k), bDez(k))); if (y[1] > 2) return TYPEN.flaechenfaktor.neu();
            return { ges: 'A', A: A, k: k, y: y, text: 'Eine Figur hat die Fläche ' + A + ' cm². Sie wird mit dem Faktor k = ' + d(k) + ' gestreckt. Wie gross ist die Fläche der Bildfigur?', muster: '{y} cm²' }; }
          var kk = zufall([2, 3, 4, 5, 6, 10]);
          return { ges: 'k', q: kk * kk, k: kk, y: B(kk), text: 'Eine Figur wird gestreckt, ihre Fläche wird dabei ' + kk * kk + '-mal so gross. Mit welchem Faktor k werden die Längen gestreckt?', muster: 'k = {y}' }; },
        richtig: function(A, e){ return bEq(e.y, A.y); },
        fehler: function(A){ return A.ges === 'A' ? [[{ y: eing(bMul(B(A.A), bDez(A.k))) }, 'Quadrat']] : [[{ y: String(A.q) }, 'Wurzel']]; },
        pruefen: function(A, e){
          if (A.ges === 'A' && bEq(e.y, bMul(B(A.A), bDez(A.k)))) return 'Die Längen werden mal k gerechnet, die Fläche aber mal \\(k^2\\): Länge und Breite wachsen beide. Nimm k im <b>Quadrat</b>.';
          if (A.ges === 'k' && bEq(e.y, B(A.q))) return 'Das ist der Flächenfaktor \\(k^2\\). Für k ziehst du die <b>Wurzel</b>.';
          return A.ges === 'A' ? 'Flächenfaktor: \\(k^2\\).' : 'Welche Zahl gibt im Quadrat \\(' + A.q + '\\)?'; },
        tipps: function(A){ return A.ges === 'A' ? ['Flächen werden mit \\(k^2\\) multipliziert.', '\\(k^2 = ' + d(A.k * A.k) + '\\)'] : ['Die Fläche wächst mit \\(k^2\\).', '\\(k^2 = ' + A.q + '\\)']; },
        loesung: function(A){ return A.ges === 'A' ? A.A + ' \\cdot ' + d(A.k) + '^2 = ' + bWertTex(A.y) : 'k = \\sqrt{' + A.q + '} = ' + A.k; } }
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
