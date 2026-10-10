<script>
/* Leitprogramm Bewegung und Begegnung (Mathematisieren) — Tarife vergleichen (Sim 1), s = v · t (Sim 2), zwei Abschnitte mit
   Durchschnitt (Sim 3), Begegnung und Einholen (Sim 4), Übungen mit Rückmeldung.
   Notation: s in km oder m, t in h oder min, v in km/h oder m/s, Zahlen mit Dezimalpunkt und echtem Minus.
   Farben: blau = A bzw. erster Abschnitt, orange = B bzw. zweiter Abschnitt, grün = Treffer, rot = Fehler.
   Gerüst: scripts/lp/funktionstypen/seite.js. */
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
    el(svg, 'text', { x: X(ay) + 7, y: 10, 'text-anchor': 'start', 'class': 'achsname' }, o.yname != null ? o.yname : 'y');
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

  /* ════════ Sim 1 — Tarife vergleichen ════════
     Zwei Angebote: Grundbetrag plus Preis pro Stück. Der Regler x zeigt beide Kosten; gesucht ist, wo sie gleich sind
     und ab wann eines günstiger ist. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    var T = { A: [15, 2], B: [5, 4], name: 'Stunden', y1: 80 };
    function zustand(){ return { x: wertR(fig, 's1-x') }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's1-x', Z.x + ' ' + T.name);
      var o = { w: 300, h: 230, rl: 30, x0: 0, x1: 30, y0: 0, y1: T.y1, sx: 2, sy: T.y1 / 8, xm: [5, 10, 15, 20, 25, 30], ym: [1, 2, 3, 4, 5, 6, 7, 8].map(function(i){ return i * T.y1 / 8; }), xname: 'x [' + T.name + ']', yname: 'Kosten [Fr.]', r: 4 };
      var k = Achsen(svg, o), a = T.A[0] + T.A[1] * Z.x, b = T.B[0] + T.B[1] * Z.x;
      k.gerade(T.A[1], T.A[0], 'linie blau', 0, 30); k.gerade(T.B[1], T.B[0], 'linie orange', 0, 30);
      k.strecke(Z.x, 0, Z.x, T.y1, 'linie grau gestrichelt'); k.punkt(Z.x, a, 'pkt blau'); k.punkt(Z.x, b, 'pkt orange');
      formel.innerHTML = 'bei ' + Z.x + ' ' + T.name + ': <span class="blau">A kostet ' + fr(a) + ' Fr.</span> &nbsp;·&nbsp; <span class="orange">B kostet ' + fr(b) + ' Fr.</span>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    var A = [
      [{ A: [15, 2], B: [5, 4], name: 'Stunden', y1: 80 }, 'Velomiete: A kostet 15 Fr. plus 2 Fr. pro Stunde, B 5 Fr. plus 4 Fr. pro Stunde. Bei wie vielen Stunden sind beide gleich teuer?', 5],
      [{ A: [15, 2], B: [5, 4], name: 'Stunden', y1: 80 }, 'Dieselben Angebote: Bei wie vielen ganzen Stunden ist A zum ersten Mal günstiger?', 6],
      [{ A: [40, 5], B: [100, 2], name: 'Besuche', y1: 200 }, 'Fitness: A 40 Fr. plus 5 Fr. pro Besuch, B 100 Fr. plus 2 Fr. pro Besuch. Wann gleich teuer?', 20],
      [{ A: [8, 2], B: [4, 3], name: 'km', y1: 80 }, 'Taxi: A 8 Fr. plus 2 Fr. pro km, B 4 Fr. plus 3 Fr. pro km. Ab wie vielen ganzen km ist A günstiger?', 5],
      [{ A: [3, 1.5], B: [6, 0.75], name: 'Stunden', y1: 48 }, 'Parkhaus: A 3 Fr. plus 1.50 Fr. pro Stunde, B 6 Fr. plus 0.75 Fr. pro Stunde. Wann gleich teuer?', 4]
    ];
    pr = Leiste(fig, A.map(function(t){ return { text: t[1], setup: function(){ T = t[0]; }, ok: function(Z){ return Z.x === t[2]; } }; }), sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 2 — s = v · t ════════
     Geschwindigkeit v in km/h, Zeit t in Minuten: s = v · t/60. Der Graph zeigt den Weg über der Zeit. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    function zustand(){ return { v: wertR(fig, 's2-v'), t: wertR(fig, 's2-t') }; }
    function zeichnen(){
      var Z = zustand(), s = Z.v * Z.t / 60; zeigeWert(fig, 's2-v', Z.v + ' km/h'); zeigeWert(fig, 's2-t', Z.t + ' min');
      var y1 = Math.max(10, Math.ceil(Z.v * 3 / 50) * 50);
      var k = Achsen(svg, { w: 300, h: 220, rl: 30, x0: 0, x1: 180, y0: 0, y1: y1, sx: 15, sy: y1 / 10, xm: [30, 60, 90, 120, 150, 180], ym: [1, 2, 3, 4, 5].map(function(i){ return i * y1 / 5; }), xname: 't [min]', yname: 's [km]', r: 4 });
      k.strecke(0, 0, 180, Z.v * 3, 'linie blau'); k.strecke(Z.t, 0, Z.t, s, 'linie grau gestrichelt'); k.punkt(Z.t, s, 'pkt gruen', z(s) + ' km', 8, -8);
      formel.innerHTML = 's = v · t = ' + Z.v + ' km/h · ' + Z.t + ' min = ' + Z.v + ' km/h · ' + Z.t + '/60 h ' + (Math.abs(s * 100 - Math.round(s * 100)) < 1e-9 ? '=' : '≈') + ' <b>' + z(s) + ' km</b>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, [
      { text: 'Ein Auto fährt 60 km/h. Wie lange braucht es für 45 km? Stell beides ein.', ok: function(Z){ return Z.v === 60 && Z.t === 45; } },
      { text: 'Ein Bus schafft 30 km in 40 Minuten. Wie schnell fährt er?', ok: function(Z){ return Z.v === 45 && Z.t === 40; } },
      { text: 'Ein Zug fährt 20 Minuten mit 90 km/h. Wie weit kommt er?', ok: function(Z){ return Z.v === 90 && Z.t === 20; } },
      { text: 'Eine Läuferin läuft 10 km/h. Wie lange braucht sie für 5 km?', ok: function(Z){ return Z.v === 10 && Z.t === 30; } },
      { text: '100 km in 1 h 15 min: Wie schnell im Durchschnitt?', ok: function(Z){ return Z.v === 80 && Z.t === 75; } }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 3 — Zwei Abschnitte ════════
     Abschnitt 1: v1 während t1, Abschnitt 2: v2 während t2 (v2 = 0: Pause). Tabelle und Durchschnitt = Gesamtweg : Gesamtzeit. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]'), tab = fig.querySelector('table.wt');
    function zustand(){ return { v1: wertR(fig, 's3-v1'), t1: wertR(fig, 's3-t1'), v2: wertR(fig, 's3-v2'), t2: wertR(fig, 's3-t2') }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's3-v1', Z.v1 + ' km/h'); zeigeWert(fig, 's3-v2', Z.v2 + ' km/h'); zeigeWert(fig, 's3-t1', z(Z.t1) + ' h'); zeigeWert(fig, 's3-t2', z(Z.t2) + ' h');
      var s1 = Z.v1 * Z.t1, s2 = Z.v2 * Z.t2, T = Z.t1 + Z.t2, S = s1 + s2;
      var k = Achsen(svg, { w: 300, h: 210, rl: 30, x0: 0, x1: 6, y0: 0, y1: 300, sx: 0.5, sy: 25, xm: [1, 2, 3, 4, 5, 6], ym: [50, 100, 150, 200, 250, 300], xname: 't [h]', yname: 's [km]', r: 4 });
      k.strecke(0, 0, Z.t1, s1, 'linie blau'); k.strecke(Z.t1, s1, T, S, 'linie orange'); k.punkt(T, S, 'pkt');
      if (T > 0) k.strecke(0, 0, T, S, 'linie grau gestrichelt');
      tab.innerHTML = '<tr><th>Abschnitt</th><th>v [km/h]</th><th>t [h]</th><th>s [km]</th></tr><tr><td>1</td><td>' + Z.v1 + '</td><td>' + z(Z.t1) + '</td><td>' + z(s1) + '</td></tr>'
        + '<tr><td>2</td><td>' + Z.v2 + '</td><td>' + z(Z.t2) + '</td><td>' + z(s2) + '</td></tr><tr><th>total</th><td></td><td><b>' + z(T) + '</b></td><td><b>' + z(S) + '</b></td></tr>';
      formel.innerHTML = T > 0 ? 'Durchschnitt = Gesamtweg : Gesamtzeit = ' + z(S) + ' : ' + z(T) + ' = <b>' + z(S / T) + ' km/h</b>' : '<span class="grau">Stell eine Zeit ein.</span>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, [
      { text: '120 km in 2 h. Die erste Stunde fährst du 80 km/h. Stell beide Abschnitte ein.', ok: function(Z){ return Z.v1 === 80 && Z.t1 === 1 && Z.v2 === 40 && Z.t2 === 1; } },
      { text: 'Durchschnitt 60 km/h über 2 h, die erste Stunde mit 40 km/h. Wie schnell in der zweiten?', ok: function(Z){ return Z.v1 === 40 && Z.t1 === 1 && Z.v2 === 80 && Z.t2 === 1; } },
      { text: '60 km mit 60 km/h, dann 60 km mit 30 km/h. Stell die Zeiten ein. Ist der Durchschnitt 45 km/h?', ok: function(Z){ return Z.v1 === 60 && Z.t1 === 1 && Z.v2 === 30 && Z.t2 === 2; } },
      { text: 'Je 1 h mit 30 km/h und mit 90 km/h. Stell ein und vergleiche: Hier stimmt das Mittel der Geschwindigkeiten. Warum?', ok: function(Z){ return Z.v1 === 30 && Z.t1 === 1 && Z.v2 === 90 && Z.t2 === 1; } },
      { text: '1.5 h mit 40 km/h, dann 30 min Pause. Wie gross ist der Durchschnitt mit Pause?', ok: function(Z){ return Z.v1 === 40 && Z.t1 === 1.5 && Z.v2 === 0 && Z.t2 === 0.5; } }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 4 — Begegnung und Einholen ════════
     A startet bei 0, B bei D. Entgegen: Abstand D − (vA + vB)·t. Gleiche Richtung (B fährt voraus): D − (vA − vB)·t. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var bahn = fig.querySelector('svg.bahn'), svg = fig.querySelector('svg.graf'), formel = fig.querySelector('[data-rolle="formel"]'), wahl = fig.querySelector('#s4-r');
    function zustand(){ return { D: wertR(fig, 's4-D'), a: wertR(fig, 's4-a'), b: wertR(fig, 's4-b'), r: wahl.value, t: wertR(fig, 's4-t') }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's4-D', Z.D + ' km'); zeigeWert(fig, 's4-a', Z.a + ' km/h'); zeigeWert(fig, 's4-b', Z.b + ' km/h'); zeigeWert(fig, 's4-t', z(Z.t) + ' h');
      var nah = Z.r === 'ent' ? Z.a + Z.b : Z.a - Z.b, xa = Z.a * Z.t, xb = Z.r === 'ent' ? Z.D - Z.b * Z.t : Z.D + Z.b * Z.t, ab = xb - xa;
      var kb = Achsen(bahn, { w: 300, h: 40, rl: 20, x0: 0, x1: 120, y0: -1, y1: 1, sx: 10, sy: 2, xm: [20, 40, 60, 80, 100, 120], ym: [], xname: 'Ort [km]', yname: '', r: 6 });
      var am = function(x){ return Math.max(0, Math.min(120, x)); };
      kb.punkt(am(xa), 0, 'pkt blau', 'A', -4, -12); kb.punkt(am(xb), 0, 'pkt orange', 'B', -4, -12);
      var k = Achsen(svg, { w: 300, h: 180, rl: 26, x0: 0, x1: 5, y0: 0, y1: 60, sx: 0.5, sy: 10, xm: [1, 2, 3, 4, 5], ym: [10, 20, 30, 40, 50, 60], xname: 't [h]', yname: 'Abstand [km]', r: 4 });
      k.kurve(function(t){ return Math.abs(Z.D - nah * t); }, 0, 5, 'linie tinte');
      if (Math.abs(ab) <= 60) k.punkt(Z.t, Math.abs(ab), 'pkt');
      formel.innerHTML = 'Abstand nach ' + z(Z.t) + ' h: <b>' + z(Math.abs(ab)) + ' km</b> <span class="grau">(A bei ' + z(xa) + ' km, B bei ' + z(xb) + ' km)</span>' + (ab < 0 ? ' <span class="nein-text">(schon vorbei)</span>' : '');
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, [
      { text: 'A und B sind 30 km auseinander und fahren aufeinander zu, A mit 12 km/h, B mit 8 km/h. Wann treffen sie sich?', ok: function(Z){ return Z.D === 30 && Z.a === 12 && Z.b === 8 && Z.r === 'ent' && Math.abs(Z.t - 1.5) < 1e-9; } },
      { text: 'B ist 20 km voraus und fährt 10 km/h, A fährt 15 km/h hinterher. Wann holt A ihn ein?', ok: function(Z){ return Z.D === 20 && Z.a === 15 && Z.b === 10 && Z.r === 'gleich' && Math.abs(Z.t - 4) < 1e-9; } },
      { text: '42 km auseinander, A 20 km/h, B 15 km/h, aufeinander zu. Wann treffen sie sich?', ok: function(Z){ return Z.D === 42 && Z.a === 20 && Z.b === 15 && Z.r === 'ent' && Math.abs(Z.t - 1.2) < 1e-9; } },
      { text: 'B ist 10 km voraus mit 15 km/h, A fährt 20 km/h. Wann holt A ihn ein?', ok: function(Z){ return Z.D === 10 && Z.a === 20 && Z.b === 15 && Z.r === 'gleich' && Math.abs(Z.t - 2) < 1e-9; } },
      { text: 'Wieder 30 km, 12 km/h und 8 km/h aufeinander zu: Wann sind sie vor dem Treffen noch 6 km auseinander?', ok: function(Z){ return Z.D === 30 && Z.a === 12 && Z.b === 8 && Z.r === 'ent' && Math.abs(Z.t - 1.2) < 1e-9; } }
    ], sim);
    fig.querySelectorAll('input, select').forEach(function(i){ i.addEventListener('input', zeichnen); i.addEventListener('change', zeichnen); });
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
      'ta|4|0.5|7|0.2', 'ta|15|2|5|4', 'ta|40|5|100|2', 'ta|8|2|4|3', 'ta|3|1.5|6|0.75', 'ta|20|3|32|1', 'ta|12|3|30|0', 'ta|5|2|11|1',
      'ra|k|72', 'ra|k|84', 'ra|k|45', 'ra|a|41|5', 'ra|a|30|4',
      'sv|s|240|120', 'sv|t|45|60', 'sv|v|30|40', 'sv|s|90|20', 'sv|t|3|12', 'sv|v|100|75', 'sv|v|150|150', 'sv|t|12|15', 'sv|v|135|90', 'sv|t|60|90', 'sv|v|120|90', 'sv|s|50|30',
      'du|60|60|60|30', 'du|30|20|20|10', 'du|60|120|60|60', 'du|120|60|120|30', 'du|10|20|6|12',
      'gz|12|4|6|3|60', 'gz|30|20|20|10|30', 'gz|6|4|4|2|30',
      'bg|36|14|10', 'bg|30|12|8', 'bg|42|20|15', 'bg|60|18|12', 'bg|45|16|14', 'bg|100|60|40', 'bg|450|80|100',
      'eh|10|15|10', 'eh|20|15|10', 'eh|10|20|15', 'eh|6|20|12', 'eh|6|18|12',
      'um|h|45', 'um|h|15', 'um|h|20', 'um|ms|36', 'um|ms|72', 'um|ms|90', 'um|ms|54', 'um|kmh|5', 'um|min|0.75'
    ];
    SPERRE.push('sv|s|18|20', 'sv|v|6|20', 'sv|t|6|18', 'sv|v|240|120', 'sv|s|120|120', 'sv|s|60|40', 'du|120|60|120|40', 'du|30|30|30|15', 'du|60|30|60|60',
      'bg|50|18|12', 'eh|30|90|60', 'eh|12|18|14', 'ra|g|84', 'ta|9|3|30|0');
    /* Vertauschte Rollen zählen als dieselbe Aufgabe (A/B, Abschnitte, Tarife) */
    function varianten(k){ var p = k.split('|');
      if (p[0] === 'bg') return [k, [p[0], p[1], p[3], p[2]].join('|')];
      if (p[0] === 'ta' || p[0] === 'du') return [k, [p[0], p[3], p[4], p[1], p[2]].join('|')];
      return [k]; }
    function gesperrt(T, A){ return !!T.schl && varianten(T.schl(A)).some(function(k){ return SPERRE.indexOf(k) >= 0; }); }
    function d(v){ return bWert(bDez(v)); }
    function dt(v){ return bWertTex(bDez(v)); }
    function eing(a){ return bWert(a).replace('−', '-'); }

    var TARIF = [
      ['Velomiete', 'Stunden', 'Stunde', 'A kostet {a1} Fr. plus {m1} Fr. pro Stunde, B {a2} Fr. plus {m2} Fr. pro Stunde.', 'Stunden', 10],
      ['Handy-Abo', 'GB', 'GB', 'A kostet {a1} Fr. im Monat plus {m1} Fr. pro GB, B {a2} Fr. plus {m2} Fr. pro GB.', 'GB', 20],
      ['Druckerei', 'Plakate', 'Plakat', 'A verlangt {a1} Fr. fürs Einrichten plus {m1} Fr. pro Plakat, B {a2} Fr. plus {m2} Fr. pro Plakat.', 'Plakaten', 20]
    ];

    var TYPEN = {
      /* ── Kapitel 1 ── */
      'tarif': { felder: ['x', 'ab'],
        schl: function(A){ return 'ta|' + A.a1 + '|' + A.m1 + '|' + A.a2 + '|' + A.m2; },
        eingabe: function(A){ return { x: String(A.x0), ab: String(A.x0 + 1) }; },
        neu: function(){
          var K = zufall(TARIF), m2 = zufall([0.5, 1, 1.5, 2, 3]), dm = zufall([0.5, 1, 1.5, 2]), m1 = m2 + dm, x0 = zufallG(4, 20), a1 = zufall([5, 10, 12, 15, 20]), a2 = a1 + dm * x0;
          if (a2 % 1 || x0 > K[5]) return TYPEN.tarif.neu();
          return { K: K, a1: a1, m1: m1, a2: a2, m2: m2, x0: x0, text: K[0] + ': ' + K[3].replace('{a1}', fr(a1)).replace('{m1}', fr(m1)).replace('{a2}', fr(a2)).replace('{m2}', fr(m2))
                   + ' Bei wie vielen ' + K[4] + ' kosten beide gleich viel? Ab wie vielen ' + K[4] + ' ist B günstiger?', muster: 'gleich bei {x} &nbsp; B günstiger ab {ab}' }; },
        richtig: function(A, e){ return bEq(e.x, B(A.x0)) && bEq(e.ab, B(A.x0 + 1)); },
        fehler: function(A){ return [[{ x: String(A.x0), ab: String(A.x0) }, 'gleich'], [{ x: String(A.x0 + 1), ab: String(A.x0 + 1) }, 'Gleichung']]; },
        pruefen: function(A, e){
          var t = [];
          if (!bEq(e.x, B(A.x0))) t.push('Setz die Kosten gleich (<b>Gleichung</b>): \\(' + dt(A.a1) + ' + ' + dt(A.m1) + 'x = ' + dt(A.a2) + ' + ' + dt(A.m2) + 'x\\).');
          if (!bEq(e.ab, B(A.x0 + 1))) t.push(bEq(e.ab, B(A.x0)) ? 'Bei \\(' + A.x0 + '\\) sind beide <b>gleich</b> teuer. Günstiger ist B erst danach.' : 'Prüf mit einer Zahl knapp über dem Gleichstand: Welches Angebot ist dann billiger?');
          return t.join(' '); },
        tipps: function(A){ return ['Variable: \\(x\\) = Anzahl ' + A.K[1] + '. Kosten A: \\(' + dt(A.a1) + ' + ' + dt(A.m1) + 'x\\), Kosten B: \\(' + dt(A.a2) + ' + ' + dt(A.m2) + 'x\\).',
          '\\(' + dt(A.m1) + 'x - ' + dt(A.m2) + 'x = ' + dt(A.a2) + ' - ' + dt(A.a1) + '\\)']; },
        loesung: function(A){ return dt(A.m1 - A.m2) + 'x = ' + dt(A.a2 - A.a1) + ' \\;\\Rightarrow\\; x = ' + A.x0 + ', \\quad \\text{B günstiger ab } ' + (A.x0 + 1); } },

      'raetsel': { felder: ['z'],
        schl: function(A){ return 'ra|' + A.art + '|' + A.S + (A.art === 'a' ? '|' + A.dd : ''); },
        eingabe: function(A){ return { z: String(A.z) }; },
        neu: function(){
          var art = zufall(['k', 'g', 'a', 'd']), n, S, dd = 0, text;
          if (art === 'g'){ n = 2 * zufallG(4, 20); S = 3 * n + 6; text = 'Drei aufeinanderfolgende <b>gerade</b> Zahlen haben zusammen die Summe ' + S + '. Wie heisst die kleinste?'; }
          else if (art === 'k'){ n = zufallG(8, 40); S = 3 * n + 3; text = 'Drei aufeinanderfolgende ganze Zahlen haben zusammen die Summe ' + S + '. Wie heisst die kleinste?'; }
          else if (art === 'a'){ n = zufallG(8, 30); dd = zufallG(2, 9); S = 2 * n + dd; text = 'Lara ist ' + dd + ' Jahre älter als ihr Bruder. Zusammen sind sie ' + S + ' Jahre alt. Wie alt ist der Bruder?'; }
          else { n = zufallG(5, 40) * 5; S = 3 * n; text = 'Mia hat doppelt so viel Geld wie Tom, zusammen haben sie ' + S + ' Fr. Wie viel hat Tom?'; }
          return { art: art, z: n, S: S, dd: dd, text: text, muster: '{z}' }; },
        richtig: function(A, e){ return bEq(e.z, B(A.z)); },
        fehler: function(A){
          if (A.art === 'k') return [[{ z: String(A.z + 1) }, 'kleinste']];
          if (A.art === 'g') return [[{ z: String(A.z + 1) }, 'gerade']];
          if (A.art === 'a') return A.S % 2 ? [] : [[{ z: String(A.S / 2) }, 'älter']];
          return A.S % 2 ? [] : [[{ z: String(A.S / 2) }, 'doppelt']]; },
        pruefen: function(A, e){
          if (A.art === 'g') return bEq(e.z, B(A.z + 1)) ? 'Aufeinanderfolgende <b>gerade</b> Zahlen liegen \\(2\\) auseinander: \\(n\\), \\(n + 2\\), \\(n + 4\\). Ist deine Zahl überhaupt gerade?' : 'Nenn die kleinste Zahl \\(n\\). Die nächsten <b>geraden</b> Zahlen sind \\(n + 2\\) und \\(n + 4\\). Probe: Summe nachrechnen.';
          if (A.art === 'k') return bEq(e.z, B(A.z + 1)) ? 'Das ist die mittlere Zahl. Gesucht ist die <b>kleinste</b>: \\(n + (n + 1) + (n + 2) = ' + A.S + '\\).' : 'Nenn die kleinste Zahl \\(n\\). Die anderen sind \\(n + 1\\) und \\(n + 2\\). Probe: Summe nachrechnen.';
          if (A.art === 'a') return 'Lara ist ' + A.dd + ' Jahre <b>älter</b>: Bruder \\(x\\), Lara \\(x + ' + A.dd + '\\), zusammen \\(2x + ' + A.dd + ' = ' + A.S + '\\).';
          return 'Mia hat <b>doppelt</b> so viel: Tom \\(x\\), Mia \\(2x\\), zusammen \\(3x = ' + A.S + '\\).'; },
        tipps: function(A){ return ['Leg fest, was \\(x\\) ist, und schreib die anderen Grössen mit \\(x\\).', A.art === 'k' ? '\\(3n + 3 = ' + A.S + '\\)' : A.art === 'g' ? '\\(3n + 6 = ' + A.S + '\\)' : A.art === 'a' ? '\\(2x + ' + A.dd + ' = ' + A.S + '\\)' : '\\(3x = ' + A.S + '\\)']; },
        loesung: function(A){ return A.art === 'k' ? '3n + 3 = ' + A.S + ' \\;\\Rightarrow\\; n = ' + A.z : A.art === 'g' ? 'n + (n + 2) + (n + 4) = ' + A.S + ' \\;\\Rightarrow\\; n = ' + A.z : A.art === 'a' ? '2x + ' + A.dd + ' = ' + A.S + ' \\;\\Rightarrow\\; x = ' + A.z : '3x = ' + A.S + ' \\;\\Rightarrow\\; x = ' + A.z; } },

      /* ── Kapitel 2 ── */
      'svt': { felder: ['y'],
        schl: function(A){ return 'sv|' + A.ges + '|' + A.k1 + '|' + A.k2; },
        eingabe: function(A){ return { y: eing(A.w) }; },
        neu: function(){
          var v = zufall([12, 15, 18, 20, 24, 30, 45, 60, 72, 80, 90, 120]), tm = zufall([10, 12, 15, 20, 30, 40, 45, 50, 75, 90, 120]), s = bMul(B(v), B(tm, 60)), ges = zufall(['s', 'v', 't']), text, w, k1, k2, einh;
          if (s[1] !== 1 && s[1] !== 2) return TYPEN.svt.neu();
          if (ges === 's'){ text = 'Wie weit kommt man in ' + tm + ' Minuten mit ' + v + ' km/h?'; w = s; einh = 'km'; k1 = v; k2 = tm; }
          else if (ges === 'v'){ text = 'Jemand legt ' + bWert(s) + ' km in ' + tm + ' Minuten zurück. Wie schnell ist das in km/h?'; w = B(v); einh = 'km/h'; k1 = bWert(s); k2 = tm; }
          else { text = 'Wie lange (in Minuten) braucht man für ' + bWert(s) + ' km mit ' + v + ' km/h?'; w = B(tm); einh = 'min'; k1 = bWert(s); k2 = v; }
          return { ges: ges, v: v, tm: tm, s: s, w: w, k1: k1, k2: k2, text: text, muster: '{y} ' + einh }; },
        richtig: function(A, e){ return bEq(e.y, A.w); },
        fehler: function(A){
          if (A.ges === 's') return [[{ y: String(A.v * A.tm) }, 'Minuten']];
          if (A.ges === 'v') return bEq(bDiv(A.s, B(A.tm)), A.w) ? [] : [[{ y: eing(bDiv(A.s, B(A.tm))) }, 'Minuten']];
          return [[{ y: eing(bDiv(B(A.v), A.s)) }, 'umgekehrt']]; },
        pruefen: function(A, e){
          if (A.ges === 's' && bEq(e.y, B(A.v * A.tm))) return 'Die Geschwindigkeit gilt pro Stunde. Rechne die <b>Minuten</b> zuerst in Stunden um: \\(' + A.tm + '\\) min \\(= ' + bWertTex(B(A.tm, 60)) + '\\) h.';
          if (A.ges === 'v' && bEq(e.y, bDiv(A.s, B(A.tm)))) return 'Das sind km pro <b>Minute</b>. Für km/h: \\(' + A.tm + '\\) <b>Minuten</b> in Stunden umrechnen oder mal \\(60\\).';
          if (A.ges === 't' && bEq(e.y, bDiv(B(A.v), A.s))) return 'Der Bruch ist <b>umgekehrt</b>: \\(t = \\dfrac{s}{v}\\), dann in Minuten umrechnen.';
          return 'Schreib zuerst die Formel: \\(s = v \\cdot t\\), \\(v = \\dfrac{s}{t}\\) oder \\(t = \\dfrac{s}{v}\\). Achte auf Stunden und Minuten.'; },
        tipps: function(A){ return ['Rechne mit Stunden: \\(' + A.tm + '\\) min \\(= ' + bWertTex(B(A.tm, 60)) + '\\) h.', A.ges === 's' ? '\\(s = v \\cdot t\\)' : A.ges === 'v' ? '\\(v = \\dfrac{s}{t}\\)' : '\\(t = \\dfrac{s}{v}\\), danach mal \\(60\\)']; },
        loesung: function(A){ var th = bWertTex(B(A.tm, 60));
          return A.ges === 's' ? 's = ' + A.v + ' \\cdot ' + th + ' = ' + bWertTex(A.s) + '\\ \\text{km}' : A.ges === 'v' ? 'v = ' + bWertTex(A.s) + ' : ' + th + ' = ' + A.v + '\\ \\text{km/h}' : 't = ' + bWertTex(A.s) + ' : ' + A.v + ' = ' + th + '\\ \\text{h} = ' + A.tm + '\\ \\text{min}'; } },

      'umrechnen': { felder: ['y'],
        schl: function(A){ return 'um|' + A.art + '|' + A.g; },
        eingabe: function(A){ return { y: eing(A.w) }; },
        neu: function(){
          var art = zufall(['ms', 'kmh', 'h', 'min']), g, w, text, einh;
          if (art === 'ms'){ g = 18 * zufall([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]); w = B(g * 10, 36); text = 'Rechne ' + g + ' km/h in m/s um.'; einh = 'm/s'; }
          else if (art === 'kmh'){ g = zufall([2, 4, 5, 8, 10, 12, 15, 20, 25, 30, 35, 40]); w = bMul(B(g), B(36, 10)); text = 'Rechne ' + g + ' m/s in km/h um.'; einh = 'km/h'; }
          else if (art === 'h'){ g = 3 * zufall([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]); w = B(g, 60); text = 'Schreib ' + g + ' Minuten als Dezimalzahl in Stunden.'; einh = 'h'; }
          else { g = zufall([0.1, 0.2, 0.25, 0.3, 0.4, 0.45, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 1.2, 1.25, 1.5, 1.75, 2.4]); w = B(Math.round(g * 60)); text = 'Wie viele Minuten sind ' + d(g) + ' h?'; einh = 'min'; }
          return { art: art, g: g, w: w, text: text, muster: '{y} ' + einh }; },
        richtig: function(A, e){ return bEq(e.y, A.w); },
        fehler: function(A){
          if (A.art === 'ms') return [[{ y: eing(bMul(B(A.g), B(36, 10))) }, '3.6']];
          if (A.art === 'kmh') return [[{ y: eing(B(A.g * 10, 36)) }, '3.6']];
          if (A.art === 'min') return bEq(B(Math.round(A.g * 100)), A.w) ? [] : [[{ y: String(Math.round(A.g * 100)) }, '60']];
          return bEq(B(A.g, 100), A.w) ? [] : [[{ y: eing(B(A.g, 100)) }, '60']]; },
        pruefen: function(A, e){
          if (A.art === 'min') return bEq(e.y, B(Math.round(A.g * 100))) ? 'Eine Stunde hat <b>60</b> Minuten, nicht 100: \\(' + d(A.g) + ' \\cdot 60\\).' : 'Rechne mal <b>60</b>: \\(' + d(A.g) + ' \\cdot 60\\).';
          if (A.art === 'h') return bEq(e.y, B(A.g, 100)) ? 'Eine Stunde hat <b>60</b> Minuten, nicht 100: \\(' + A.g + ' : 60\\).' : 'Teile durch <b>60</b>: \\(' + A.g + ' : 60\\).';
          return A.art === 'ms' ? 'Von km/h nach m/s wird die Zahl kleiner: durch <b>3.6</b>. (1 m/s = 3.6 km/h)' : 'Von m/s nach km/h wird die Zahl grösser: mal <b>3.6</b>. (1 m/s = 3.6 km/h)'; },
        tipps: function(A){ return [A.art === 'h' || A.art === 'min' ? 'Eine Stunde hat 60 Minuten.' : '1 m/s sind 3600 m pro Stunde, also 3.6 km/h.', A.art === 'h' ? '\\(' + A.g + ' : 60\\)' : A.art === 'min' ? '\\(' + d(A.g) + ' \\cdot 60\\)' : A.art === 'ms' ? '\\(' + A.g + ' : 3.6\\)' : '\\(' + A.g + ' \\cdot 3.6\\)']; },
        loesung: function(A){ return (A.art === 'h' ? A.g + ' : 60' : A.art === 'min' ? d(A.g) + ' \\cdot 60' : A.art === 'ms' ? A.g + ' : 3.6' : A.g + ' \\cdot 3.6') + ' = ' + bWertTex(A.w); } },

      /* ── Kapitel 3 ── */
      'durchschnitt': { felder: ['y'],
        schl: function(A){ return 'du|' + A.s1 + '|' + A.v1 + '|' + A.s2 + '|' + A.v2; },
        eingabe: function(A){ return { y: eing(A.w) }; },
        neu: function(){
          var KL = zufall([[10, 12, 15, 18, 20, 24, 30], [40, 50, 60, 80, 90, 100, 120]]), v1 = zufall(KL), v2 = zufall(KL), t1 = zufall([0.5, 1, 1.5, 2]), t2 = zufall([0.5, 1, 1.5, 2, 3]);
          if (v1 === v2 || t1 === t2) return TYPEN.durchschnitt.neu();
          var s1 = v1 * t1, s2 = v2 * t2, w = bDiv(bDez(s1 + s2), bDez(t1 + t2));
          if (w[1] > 2) return TYPEN.durchschnitt.neu();
          return { v1: v1, v2: v2, s1: s1, s2: s2, t1: t1, t2: t2, w: w, text: 'Eine Fahrt: ' + d(s1) + ' km mit ' + v1 + ' km/h, dann ' + d(s2) + ' km mit ' + v2 + ' km/h. Wie gross ist die Durchschnittsgeschwindigkeit?', muster: '{y} km/h' }; },
        richtig: function(A, e){ return bEq(e.y, A.w); },
        fehler: function(A){ var m = B(A.v1 + A.v2, 2); return bEq(m, A.w) ? [] : [[{ y: eing(m) }, 'Mittel']]; },
        pruefen: function(A, e){
          if (bEq(e.y, B(A.v1 + A.v2, 2))) return 'Das <b>Mittel</b> der Geschwindigkeiten stimmt nur bei gleich langen Zeiten. Hier: Gesamtweg durch Gesamtzeit.';
          return 'Rechne zuerst die Zeiten: \\(t = \\dfrac{s}{v}\\) für jeden Abschnitt, dann Gesamtweg durch Gesamtzeit.'; },
        tipps: function(A){ return ['Zeiten: \\(' + dt(A.s1) + ' : ' + A.v1 + '\\) und \\(' + dt(A.s2) + ' : ' + A.v2 + '\\) Stunden.', 'Gesamtweg \\(' + dt(A.s1 + A.s2) + '\\) km, Gesamtzeit \\(' + dt(A.t1 + A.t2) + '\\) h.']; },
        loesung: function(A){ return '\\dfrac{' + dt(A.s1) + ' + ' + dt(A.s2) + '}{' + dt(A.t1) + ' + ' + dt(A.t2) + '} = \\dfrac{' + dt(A.s1 + A.s2) + '}{' + dt(A.t1 + A.t2) + '} = ' + bWertTex(A.w) + '\\ \\text{km/h}'; } },

      'gesamtzeit': { felder: ['y'],
        schl: function(A){ return 'gz|' + A.s1 + '|' + A.v1 + '|' + A.s2 + '|' + A.v2 + '|' + A.p; },
        eingabe: function(A){ return { y: eing(A.w) }; },
        neu: function(){
          var v1 = zufall([4, 5, 6, 10, 12, 15, 20]), v2 = zufall([3, 4, 5, 8, 10, 12]), t1 = zufall([0.5, 1, 1.5, 2]), t2 = zufall([0.5, 1, 1.5, 2]), p = zufall([15, 30, 45, 60]);
          var s1 = v1 * t1, s2 = v2 * t2, w = bAdd(bDez(t1 + t2), B(p, 60));
          return { v1: v1, v2: v2, s1: s1, s2: s2, t1: t1, t2: t2, p: p, w: w, text: 'Eine Tour: ' + d(s1) + ' km mit ' + v1 + ' km/h, dann ' + p + ' Minuten Pause, dann ' + d(s2) + ' km mit ' + v2 + ' km/h. Wie lange dauert sie insgesamt (in Stunden)?', muster: '{y} h' }; },
        richtig: function(A, e){ return bEq(e.y, A.w); },
        fehler: function(A){ return [[{ y: eing(bDez(A.t1 + A.t2)) }, 'Pause']]; },
        pruefen: function(A, e){
          if (bEq(e.y, bDez(A.t1 + A.t2))) return 'Die <b>Pause</b> gehört auch zur Dauer: \\(' + A.p + '\\) min \\(= ' + bWertTex(B(A.p, 60)) + '\\) h.';
          return 'Für jeden Abschnitt \\(t = \\dfrac{s}{v}\\), dazu die Pause in Stunden.'; },
        tipps: function(A){ return ['\\(t_1 = ' + dt(A.s1) + ' : ' + A.v1 + '\\), \\(t_2 = ' + dt(A.s2) + ' : ' + A.v2 + '\\).', 'Pause: \\(' + A.p + '\\) min \\(= ' + bWertTex(B(A.p, 60)) + '\\) h.']; },
        loesung: function(A){ return dt(A.t1) + ' + ' + bWertTex(B(A.p, 60)) + ' + ' + dt(A.t2) + ' = ' + bWertTex(A.w) + '\\ \\text{h}'; } },

      /* ── Kapitel 4 ── */
      'begegnung': { felder: ['t', 'x'],
        schl: function(A){ return 'bg|' + A.D + '|' + A.a + '|' + A.b; },
        eingabe: function(A){ return { t: eing(A.t), x: eing(A.x) }; },
        neu: function(){
          var a = zufall([8, 10, 12, 14, 15, 16, 18, 20, 25, 30]), b = zufall([6, 8, 10, 12, 15, 20]), t = zufall([0.5, 1, 1.5, 2, 2.5, 3]), D = (a + b) * t;
          if (a === b || D % 1) return TYPEN.begegnung.neu();
          return { a: a, b: b, D: D, t: bDez(t), x: bDez(a * t), text: 'A und B sind ' + D + ' km auseinander und fahren gleichzeitig aufeinander zu, A mit ' + a + ' km/h, B mit ' + b + ' km/h. Nach wie vielen Stunden treffen sie sich, und wie weit ist A dann gefahren?',
                   muster: 'nach {t} h &nbsp; A ist {x} km gefahren' }; },
        richtig: function(A, e){ return bEq(e.t, A.t) && bEq(e.x, A.x); },
        fehler: function(A){ var t2 = B(A.D, A.a - A.b); return bEq(t2, A.t) ? [] : [[{ t: eing(t2), x: eing(bMul(B(A.a), t2)) }, 'entgegen']]; },
        pruefen: function(A, e){
          if (!bEq(e.t, A.t)) return bEq(e.t, B(A.D, A.a - A.b)) ? 'Sie fahren <b>entgegen</b>: Der Abstand schrumpft mit \\(' + A.a + ' + ' + A.b + '\\) km/h, nicht mit der Differenz.' : 'Um wie viele km wird der Abstand pro Stunde kleiner? Teile den Abstand durch diese Annäherungsgeschwindigkeit.';
          return 'Die Zeit stimmt. A fährt in dieser Zeit \\(' + A.a + ' \\cdot t\\) km.'; },
        tipps: function(A){ return ['Pro Stunde wird der Abstand um \\(' + A.a + ' + ' + A.b + '\\) km kleiner.', '\\(t = ' + A.D + ' : ' + (A.a + A.b) + '\\)']; },
        loesung: function(A){ return 't = \\dfrac{' + A.D + '}{' + A.a + ' + ' + A.b + '} = ' + bWertTex(A.t) + '\\ \\text{h}, \\quad ' + A.a + ' \\cdot ' + bWertTex(A.t) + ' = ' + bWertTex(A.x) + '\\ \\text{km}'; } },

      'einholen': { felder: ['t'],
        schl: function(A){ return 'eh|' + A.V + '|' + A.a + '|' + A.b; },
        eingabe: function(A){ return { t: eing(A.t) }; },
        neu: function(){
          var b = zufall([8, 10, 12, 15]), dv = zufall([2, 3, 4, 5, 6, 10]), a = b + dv, h = zufall([0.5, 1, 1.5, 2]), V = b * h, t = bDiv(bDez(V), B(dv));
          if (t[1] > 4 || V % 1) return TYPEN.einholen.neu();
          return { a: a, b: b, h: h, V: V, t: t, text: 'Tom fährt mit ' + b + ' km/h los. ' + (h * 60) + ' min später fährt Lea auf demselben Weg hinterher, mit ' + a + ' km/h. Nach wie vielen Stunden (ab Leas Start) holt sie ihn ein?', muster: '{t} h' }; },
        richtig: function(A, e){ return bEq(e.t, A.t); },
        fehler: function(A){ var t2 = bDiv(bDez(A.V), B(A.a + A.b)); return bEq(t2, A.t) ? [] : [[{ t: eing(t2) }, 'gleiche Richtung']]; },
        pruefen: function(A, e){
          if (bEq(e.t, bDiv(bDez(A.V), B(A.a + A.b)))) return 'Beide fahren in die <b>gleiche Richtung</b>: Lea holt pro Stunde nur \\(' + A.a + ' - ' + A.b + '\\) km auf.';
          return 'Wie viele km Vorsprung hat Tom, wenn Lea startet? Und um wie viel kommt Lea ihm pro Stunde näher?'; },
        tipps: function(A){ return ['Vorsprung beim Start von Lea: \\(' + A.b + ' \\cdot ' + dt(A.h) + '\\) km.', 'Aufholen pro Stunde: \\(' + A.a + ' - ' + A.b + '\\) km.']; },
        loesung: function(A){ return '\\dfrac{' + dt(A.V) + '}{' + A.a + ' - ' + A.b + '} = ' + bWertTex(A.t) + '\\ \\text{h}'; } }
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
