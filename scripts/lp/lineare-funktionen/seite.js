<script>
/* Leitprogramm Lineare Funktionen — Anfangswert und Änderung (Sim 1, Fass), Steigung messen (Sim 2), m kippt und b schiebt
   (Sim 3), Infusion mit Ratenwechsel (Sim 4), Übungen mit Rückmeldung, Minibilder. Notation: y = m · x + b, Steigung m,
   y-Achsenabschnitt b, Punkte (x | y), Zahlen mit Dezimalpunkt und echtem Minus.
   Farben (eine Farbe, eine Bedeutung): blau = Gerade und m, orange = b, Punkte und Steigungsdreieck, grün = Treffer und
   Ergebnis, rot = Fehler. Koordinatensystem gekürzt aus dem Leitprogramm Lineare Funktionen von TALS Mathe. */
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
      text: function(x, y, s, cls, anker){ el(ebene, 'text', { x: X(x), y: Y(y), 'text-anchor': anker || 'middle', 'class': 'p-text ' + cls }, s); },
      zuWert: function(px, py){ return [x0 + px / W * (x1 - x0), y0 + (H - py) / H * (y1 - y0)]; }
    };
  }
  var GITTER = { w: 280, h: 280, rl: 18, x0: -7, x1: 7, y0: -7, y1: 7, xm: [-6, -4, -2, 2, 4, 6], ym: [-6, -4, -2, 2, 4, 6] };
  function wertR(fig, id){ return +fig.querySelector('#' + id).value; }
  function zeigeWert(fig, id, txt){ var i = fig.querySelector('#' + id); var v = i.parentNode.querySelector('.sl-val'); if (v) v.textContent = txt != null ? txt : z(+i.value); }
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

  /* ════════ Sim 1 — Anfangswert und Änderung (Fass) ════════
     V = m·t + b: b Liter am Anfang, m Liter pro Minute (negativ: es fliesst ab). Wertetabelle t = 0 … 5 und die Punkte im Graphen. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg'), tab = fig.querySelector('table.wt'), formel = fig.querySelector('[data-rolle="formel"]');
    var F1 = { w: 300, h: 200, rl: 30, x0: 0, x1: 10, y0: 0, y1: 200, sx: 1, sy: 20, xm: [2, 4, 6, 8, 10], ym: [40, 80, 120, 160, 200], xname: 't [min]', yname: 'V [l]' };
    function zustand(){ return { b: wertR(fig, 's1-b'), m: wertR(fig, 's1-m') }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's1-b', Z.b + ' l'); zeigeWert(fig, 's1-m', z(Z.m) + ' l/min');
      var k = Achsen(svg, F1);
      k.gerade(Z.m, Z.b, 'linie blau', 0, 10);
      for (var t = 0; t <= 5; t++) k.punkt(t, Z.m * t + Z.b, 'pkt orange');
      k.punkt(0, Z.b, 'pkt gruen', 'b = ' + Z.b, 8, -8);
      var h = '<tr><th>t [min]</th>', w = '<tr><th>V [l]</th>';
      for (t = 0; t <= 5; t++){ h += '<td>' + t + '</td>'; w += '<td>' + z(Z.m * t + Z.b) + '</td>'; }
      tab.innerHTML = h + '</tr>' + w + '</tr><tr><th></th>' + [1, 2, 3, 4, 5].map(function(){ return '<td class="dif">' + (Z.m >= 0 ? '+' : '−') + Math.abs(Z.m) + '</td>'; }).join('').replace(/^/, '<td></td>') + '</tr>';
      formel.innerHTML = linTxt(Z.m, Z.b, 't', 'V') + ' <span class="grau">(Anfangswert ' + Z.b + ' l, Änderung ' + z(Z.m) + ' l pro Minute)</span>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    var A = [[30, 10, 'Im Fass sind 30 l, pro Minute kommen 10 l dazu.'], [0, 15, 'Das Fass ist leer, pro Minute kommen 15 l dazu.'],
             [90, -10, 'Im Fass sind 90 l, pro Minute fliessen 10 l ab.'], [20, 20, 'Am Anfang sind 20 l drin, nach 4 Minuten 100 l.'],
             [15, 10, 'Nach 3 Minuten sind 45 l drin, nach 5 Minuten 65 l. Wie viel war es am Anfang?']];
    pr = Leiste(fig, A.map(function(a){ return { text: a[2] + ' Stell die Regler passend ein.', ok: function(Z){ return Z.b === a[0] && Z.m === a[1]; } }; }), sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 2 — Steigung messen ════════
     Gegeben ist eine Gerade (blau). Das Steigungsdreieck startet auf der Geraden bei x = −2; mit Δx und Δy einstellen,
     bis die Spitze wieder auf der Geraden liegt. Dann ist m = Δy / Δx. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    var ZIELE = [[[2, 1], -1], [[-1, 1], 2], [[1, 2], 0], [[-3, 2], 1], [[0, 1], 3]], G = ZIELE[0];
    function zustand(){ return { dx: wertR(fig, 's2-dx'), dy: wertR(fig, 's2-dy') }; }
    function zeichnen(){
      var Z = zustand(), m = G[0][0] / G[0][1], b = G[1], xa = -2, ya = m * xa + b;
      zeigeWert(fig, 's2-dx'); zeigeWert(fig, 's2-dy');
      var k = Achsen(svg, GITTER);
      k.gerade(m, b, 'linie blau');
      var trifft = Math.abs(ya + Z.dy - (m * (xa + Z.dx) + b)) < 1e-9;
      k.strecke(xa, ya, xa + Z.dx, ya, 'dreieck dx'); k.strecke(xa + Z.dx, ya, xa + Z.dx, ya + Z.dy, 'dreieck dy');
      k.strecke(xa, ya, xa + Z.dx, ya + Z.dy, 'dreieck hyp' + (trifft ? ' ok' : ''));
      k.punkt(xa, ya, 'pkt'); k.punkt(xa + Z.dx, ya + Z.dy, trifft ? 'pkt gruen' : 'pkt rot');
      k.text(xa + Z.dx / 2, ya - (Z.dy >= 0 ? 0.55 : -0.95), 'Δx = ' + Z.dx, 'orange');
      k.text(xa + Z.dx + 0.25, ya + Z.dy / 2, 'Δy = ' + z(Z.dy), 'orange', 'start');
      formel.innerHTML = trifft ? 'Die Spitze liegt auf der Geraden: <span class="ok-text">m = Δy / Δx = ' + z(Z.dy) + ' / ' + Z.dx + ' = ' + z(Z.dy / Z.dx) + '</span>'
                                : '<span class="grau">Die Spitze liegt noch nicht auf der Geraden.</span>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    var texte = ['Miss die Steigung: Die Spitze des Dreiecks soll auf der Geraden liegen.', 'Diese Gerade fällt. Welches Vorzeichen bekommt Δy?',
                 'Hier passt Δx = 1 nicht genau. Probier ein grösseres Δx.', 'Fallend und flach: Wie weit nach rechts für ganze Kästchen?', 'Eine waagrechte Gerade: Was ist Δy?'];
    pr = Leiste(fig, ZIELE.map(function(g, i){
      return { text: texte[i], setup: function(){ G = g; }, ok: function(Z){ return Z.dy * g[0][1] === g[0][0] * Z.dx; } };
    }), sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 3 — m kippt, b schiebt ════════
     Regler: b (−6 … 6) und m als Δy/Δx (Δy −6 … 6, Δx 1 … 4). Gesuchte Punkte grün. */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    var AUFG = [
      { text: 'Lass die Gerade durch \\((0 \\mid 2)\\) laufen und steigen: pro Schritt nach rechts 3 nach oben.', p: [[0, 2]], ok: function(Z){ return Z.b === 2 && Z.m === 3; } },
      { text: 'Stell die Gerade durch \\((0 \\mid -1)\\) und \\((2 \\mid 3)\\) ein.', p: [[0, -1], [2, 3]], ok: function(Z){ return Z.b === -1 && Z.m === 2; } },
      { text: 'Parallel zu \\(y = x\\), aber durch \\((0 \\mid 3)\\).', p: [[0, 3]], hilf: [1, 0], ok: function(Z){ return Z.b === 3 && Z.m === 1; } },
      { text: 'Eine fallende Gerade durch \\((2 \\mid 0)\\) und \\((0 \\mid 4)\\).', p: [[2, 0], [0, 4]], ok: function(Z){ return Z.b === 4 && Z.m === -2; } },
      { text: 'Eine Gerade durch \\((0 \\mid -3)\\) und \\((3 \\mid -1)\\). Wie gross ist \\(m\\) jetzt?', p: [[0, -3], [3, -1]], ok: function(Z){ return Z.b === -3 && Math.abs(Z.m - 2 / 3) < 1e-9; } }
    ], T = AUFG[0];
    function zustand(){ var dy = wertR(fig, 's3-dy'), dx = wertR(fig, 's3-dx'); return { b: wertR(fig, 's3-b'), dy: dy, dx: dx, m: dy / dx }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's3-b'); zeigeWert(fig, 's3-dy'); zeigeWert(fig, 's3-dx');
      var k = Achsen(svg, GITTER);
      if (T.hilf) k.gerade(T.hilf[0], T.hilf[1], 'linie grau gestrichelt');
      k.gerade(Z.m, Z.b, 'linie blau');
      k.punkt(0, Z.b, 'pkt orange');
      k.strecke(0, Z.b, Z.dx, Z.b, 'dreieck dx'); k.strecke(Z.dx, Z.b, Z.dx, Z.b + Z.dy, 'dreieck dy');
      T.p.forEach(function(p){ var drauf = Math.abs(Z.m * p[0] + Z.b - p[1]) < 1e-9; k.punkt(p[0], p[1], drauf ? 'pkt gruen' : 'pkt ziel', '(' + z(p[0]) + ' | ' + z(p[1]) + ')', 8, 16); });
      formel.innerHTML = linTxt(B(Z.dy, Z.dx), Z.b) + ' <span class="grau">(m = ' + z(Z.dy) + '/' + Z.dx + ', b = ' + z(Z.b) + ')</span>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, AUFG.map(function(a){ return { text: a.text, setup: function(){ T = a; }, ok: a.ok }; }), sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 4 — Infusion ════════
     V(t): Start V0, Rate r1 bis zum Wechsel bei T, dann r2. Der Graph knickt beim Wechsel, er springt nicht.
     Ein Zeitregler t zeigt V(t). */
  function infusion(V0, r1, T, r2, t){
    var v = t <= T ? V0 - r1 * t : V0 - r1 * T - r2 * (t - T);
    return Math.max(0, v);
  }
  function leerZeit(V0, r1, T, r2){ var vT = V0 - r1 * T; return vT <= 0 ? V0 / r1 : T + vT / r2; }
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    var F4 = { w: 320, h: 210, rl: 34, x0: 0, x1: 400, y0: 0, y1: 1000, sx: 50, sy: 100, xm: [100, 200, 300, 400], ym: [200, 400, 600, 800, 1000], xname: 't [min]', yname: 'V [ml]', r: 4 };
    function zustand(){ return { V0: wertR(fig, 's4-v'), r1: wertR(fig, 's4-r1'), T: wertR(fig, 's4-T'), r2: wertR(fig, 's4-r2'), t: wertR(fig, 's4-t') }; }
    function zeichnen(){
      var Z = zustand();
      zeigeWert(fig, 's4-v', Z.V0 + ' ml'); zeigeWert(fig, 's4-r1', Z.r1 + ' ml/min'); zeigeWert(fig, 's4-T', Z.T + ' min'); zeigeWert(fig, 's4-r2', Z.r2 + ' ml/min'); zeigeWert(fig, 's4-t', Z.t + ' min');
      var k = Achsen(svg, F4), te = leerZeit(Z.V0, Z.r1, Z.T, Z.r2), vT = infusion(Z.V0, Z.r1, Z.T, Z.r2, Z.T);
      var tw = Math.min(Z.T, te);
      k.strecke(0, Z.V0, tw, infusion(Z.V0, Z.r1, Z.T, Z.r2, tw), 'linie blau');
      if (te > Z.T){ k.strecke(Z.T, vT, te, 0, 'linie orange'); k.punkt(Z.T, vT, 'pkt orange'); }
      k.punkt(te, 0, 'pkt gruen');
      var vt = infusion(Z.V0, Z.r1, Z.T, Z.r2, Z.t);
      k.strecke(Z.t, 0, Z.t, vt, 'linie grau gestrichelt'); k.punkt(Z.t, vt, 'pkt');
      formel.innerHTML = 'bei t = ' + Z.t + ' min: noch <b>' + z(vt) + ' ml</b> <span class="grau">· leer nach ' + z(te) + ' min' + (te > Z.T && Z.r2 !== Z.r1 ? ' · Wechsel bei ' + Z.T + ' min' : '') + '</span>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    var gleich = function(Z){ return Z.r2 === Z.r1 || Z.T >= leerZeit(Z.V0, Z.r1, 1e9, Z.r1); };
    pr = Leiste(fig, [
      { text: 'Stell ein: 400 ml, 4 ml/min, ohne Wechsel (Rate danach gleich). Zieh den Zeitregler dorthin, wo der Beutel leer wird.',
        ok: function(Z){ return Z.V0 === 400 && Z.r1 === 4 && gleich(Z) && Z.t === 100; } },
      { text: '600 ml, 3 ml/min, ohne Wechsel. Wie viel ist nach 120 Minuten noch drin? Zieh den Zeitregler auf 120.',
        ok: function(Z){ return Z.V0 === 600 && Z.r1 === 3 && gleich(Z) && Z.t === 120; } },
      { text: '500 ml, 5 ml/min; nach 60 Minuten wird auf 2 ml/min gestellt. Wann ist der Beutel leer?',
        ok: function(Z){ return Z.V0 === 500 && Z.r1 === 5 && Z.T === 60 && Z.r2 === 2 && Z.t === 160; } },
      { text: '900 ml sollen ohne Wechsel genau 300 Minuten reichen. Welche Rate? Zieh den Zeitregler auf 300.',
        ok: function(Z){ return Z.V0 === 900 && Z.r1 === 3 && gleich(Z) && Z.t === 300; } },
      { text: '800 ml, 4 ml/min; nach 100 Minuten schneller, 8 ml/min. Wann leer? Beachte: Beim Wechsel knickt der Graph, er springt nicht.',
        ok: function(Z){ return Z.V0 === 800 && Z.r1 === 4 && Z.T === 100 && Z.r2 === 8 && Z.t === 150; } }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ---------- Minibilder: <svg class="mini-gerade" data-geraden="m,b;m,b" data-punkte="x,y;x,y"> ---------- */
  function miniBild(svg, geraden, punkte){
    var k = Achsen(svg, { w: 180, h: 180, rl: 14, x0: -6, x1: 6, y0: -6, y1: 6, xm: [-4, -2, 2, 4], ym: [-4, -2, 2, 4], r: 3.5 });
    geraden.forEach(function(g, i){ k.gerade(g[0], g[1], 'linie ' + (i ? 'orange' : 'blau')); });
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
  function wertR(fig, id){ return +fig.querySelector('#' + id).value; }
  function zeigeWert(fig, id){ var i = fig.querySelector('#' + id); var v = i.parentNode.querySelector('.sl-val'); if (v) v.textContent = mz(+i.value); }

  /* ════════ Übungen mit Rückmeldung ════════
     Zahlenfelder exakt als Bruch (2/3, −1.5, 4). Felder p1, p2: zwei Gitterpunkte, angeklickt im Koordinatensystem.
     Fehlversuch → gezielte Diagnose oder die Probe mit einem Punkt. Tipps in drei Stufen. Testhaken: box.__aufgabe, box.__typ. */
  (function(){
    var ALLE = document.querySelectorAll('.uebung[data-typ]'); if (!ALLE.length) return;
    function mTex(m){ return bTex(m); }
    function lnSchl(m, b){ return 'ln|' + m[0] + '/' + m[1] + '|' + b[0] + '/' + b[1]; }
    function ppSchl(p, q){ var a = [p, q].sort(function(u, w){ return u[0] - w[0]; }); return 'pp|' + a[0].join(',') + '|' + a[1].join(','); }
    function steil(){ var q = zufall([1, 1, 2, 3]), p; do { p = nz(-4, 4); } while (ggT(p, q) !== 1); return B(p, q); }
    function aufGitter(m, b){ return Math.abs(b) <= 5 && Math.abs(b + m[0]) <= 6 && m[1] <= 4; }
    function bild(m, b, pkte){ return '<span class="mini-reihe"><svg class="mini-gerade" data-geraden="' + m[0] + '/' + m[1] + ',' + b + '"' + (pkte ? ' data-punkte="' + pkte + '"' : '') + ' aria-label="Gerade im Koordinatensystem"></svg></span>'; }

    /* Feste Aufgaben: Geraden als «ln|m|b» (m und b als gekürzte Brüche), Punktpaare sortiert. */
    var SPERRE = [
      'ln|15/1|200/1', 'ln|3/1|8/1', 'ln|-2/1|5/1', 'ln|-4/1|50/1', 'ln|40/1|300/1', 'ln|5/1|80/1', 'ln|-3/1|20/1', 'ln|6/1|9/1', 'ln|-3/1|12/1',
      'ln|4/1|-7/1', 'ln|-6/1|80/1', 'ln|-3/1|750/1', 'ln|-2/1|500/1', 'ln|-6/1|240/1', 'ln|-3/1|600/1', 'ln|10/1|30/1', 'ln|15/1|0/1', 'ln|-10/1|90/1',
      'ln|20/1|20/1', 'ln|10/1|15/1', 'ln|2/3|-1/1', 'ln|2/1|-3/1', 'ln|-1/2|2/1', 'ln|3/4|-2/1', 'ln|3/4|1/1', 'ln|-2/1|1/1', 'ln|1/2|4/1',
      'ln|1/2|-2/1', 'ln|2/3|-2/1', 'ln|1/1|-2/1', 'ln|2/1|1/1', 'ln|3/1|1/1', 'ln|2/3|1/1', 'ln|3/1|-6/1', 'ln|2/1|-8/1', 'ln|3/1|2/1',
      'ln|2/1|-1/1', 'ln|1/1|3/1', 'ln|-2/1|4/1', 'ln|2/3|-3/1', 'ln|-1/2|5/1', 'ln|3/2|-2/1', 'ln|-1/3|0/1',
      'ln|-2/1|24/1', 'ln|-1/3|2/1', 'ln|-2/1|3/1', 'ln|-1/2|3/1', 'ln|3/1|-1/1', 'ln|-3/2|3/1', 'ln|1/1|2/1', 'ln|-1/1|-2/1', 'ln|0/1|2/1',   /* Clips 10.10.2026 */
      'pp|1,2|4,8', 'pp|2,3|6,11', 'pp|-1,4|3,-4', 'pp|2,1|4,5', 'pp|2,1|5,7', 'pp|-1,3|1,-1', 'pp|-1,5|3,-3', 'pp|2,5|6,7', 'pp|1,3|3,7',
      'pp|-2,6|4,3', 'pp|1,4|3,10', 'pp|2,1|6,7', 'pp|0,-1|2,3', 'pp|0,4|2,0', 'pp|0,-3|3,-1', 'pp|0,-2|4,0', 'pp|0,-2|3,0', 'pp|0,1|2,5', 'pp|0,1|4,4', 'pp|0,3|1,1'
    ];
    function gesperrt(T, A){ return !!T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }
    function probeTxt(m, b, x, y){ var w = bAdd(bMul(m, B(x)), b);
      return 'Probe mit dem Punkt \\((' + x + ' \\mid ' + y + ')\\): Deine Gerade gibt bei \\(x = ' + x + '\\) den Wert \\(' + bTex(w) + '\\), nicht \\(' + y + '\\).'; }

    var KONTEXT = [
      { t: 'Ein Wassertank enthält {b} l. Pro Minute fliessen {m} l dazu.', x: 't [min]', s: 1 },
      { t: 'Ein Wassertank enthält {b} l. Pro Minute fliessen {m} l ab.', x: 't [min]', s: -1 },
      { t: 'Auf dem Sparkonto liegen {b} Fr. Jede Woche kommen {m} Fr. dazu.', x: 'Wochen', s: 1 },
      { t: 'Eine Wanderung startet auf {b} m ü. M. Pro Stunde geht es {m} m hinauf.', x: 'Stunden', s: 1 },
      { t: 'Ein Ofen hat {b} °C. Pro Minute wird er {m} °C heisser.', x: 'Minuten', s: 1 },
      { t: 'Ein Heizöltank enthält {b} l. Pro Tag werden {m} l verbraucht.', x: 'Tage', s: -1 }
    ];

    var TYPEN = {
      /* ── Kapitel 1 ── */
      'wert': { felder: ['y', 'x'],
        schl: function(A){ return lnSchl(B(A.m), B(A.b)); },
        eingabe: function(A){ return { y: String(A.y1), x: String(A.x2) }; },
        neu: function(){
          var m = nz(-6, 6), b = nz(-12, 12), x1 = nz(-5, 6), x2 = nz(-6, 8);
          return { m: m, b: b, x1: x1, y1: m * x1 + b, x2: x2, y2: m * x2 + b,
            text: 'Gegeben ist \\(y = ' + linTex(B(m), b) + '\\).', muster: 'Für \\(x = ' + x1 + '\\): \\(y = \\) {y} &nbsp; Für \\(y = ' + (m * x2 + b) + '\\): \\(x = \\) {x}' }; },
        richtig: function(A, e){ return bEq(e.y, B(A.y1)) && bEq(e.x, B(A.x2)); },
        fehler: function(A){ var f = [];
          if (A.b * A.x1 + A.m !== A.y1) f.push([{ y: String(A.b * A.x1 + A.m), x: String(A.x2) }, 'vertauscht']);
          var xs = B(A.y2 + A.b, A.m); if (!bEq(xs, B(A.x2))) f.push([{ y: String(A.y1), x: bTxt(xs).replace('−', '-') }, 'Vorzeichen']);
          return f; },
        pruefen: function(A, e){
          var t = [];
          if (!bEq(e.y, B(A.y1))) t.push(bEq(e.y, B(A.b * A.x1 + A.m)) ? '\\(m\\) und \\(b\\) sind <b>vertauscht</b>: \\(m\\) wird mit \\(x\\) multipliziert, \\(b\\) dazugezählt.' : 'Setz \\(x = ' + A.x1 + '\\) ein: \\(' + A.m + ' \\cdot ' + (A.x1 < 0 ? '(' + A.x1 + ')' : A.x1) + ' + ' + (A.b < 0 ? '(' + A.b + ')' : A.b) + '\\).');
          if (!bEq(e.x, B(A.x2))) t.push(bEq(e.x, B(A.y2 + A.b, A.m)) ? '<b>Vorzeichen</b>: Rechne zuerst \\(' + (A.b < 0 ? '+ ' + (-A.b) : '- ' + A.b) + '\\) auf beiden Seiten, dann teile durch \\(' + A.m + '\\).' : 'Löse \\(' + linTex(B(A.m), A.b) + ' = ' + A.y2 + '\\) nach \\(x\\) auf.');
          return t.join(' '); },
        tipps: function(A){ return ['Den Wert für \\(x\\) einsetzen. Für das zweite Feld eine Gleichung lösen.', '\\(' + linTex(B(A.m), A.b) + ' = ' + A.y2 + '\\) \\(\\;\\Rightarrow\\; ' + A.m + 'x = ' + (A.y2 - A.b) + '\\)']; },
        loesung: function(A){ return 'y = ' + A.y1 + ', \\quad x = \\dfrac{' + A.y2 + ' - ' + (A.b < 0 ? '(' + A.b + ')' : A.b) + '}{' + A.m + '} = ' + A.x2; } },

      'kontext': { felder: ['m', 'b'],
        schl: function(A){ return lnSchl(B(A.m), B(A.b)); },
        eingabe: function(A){ return { m: String(A.m), b: String(A.b) }; },
        neu: function(){
          var K = zufall(KONTEXT), b = K.t.indexOf('m ü. M.') >= 0 ? 100 * zufallG(4, 20) : zufallG(2, 30) * 10, m = zufall([2, 3, 4, 5, 6, 8, 12, 15, 20, 25]);
          if (K.t.indexOf('°C') >= 0) b = zufall([18, 20, 22]); if (K.t.indexOf('Wanderung') >= 0) m = 100 * zufallG(2, 4);
          if (m === b) return TYPEN.kontext.neu();               // sonst ist «vertauscht» nicht zu erkennen
          var text = K.t.replace('{b}', b).replace('{m}', m);
          return { K: K, m: K.s * m, b: b, text: text + ' Stelle die Gleichung \\(y = m \\cdot x + b\\) auf (\\(x\\): ' + K.x + ').', muster: '\\(m = \\) {m} &nbsp; \\(b = \\) {b}' }; },
        richtig: function(A, e){ return bEq(e.m, B(A.m)) && bEq(e.b, B(A.b)); },
        fehler: function(A){ var f = [[{ m: String(A.b), b: String(A.m) }, 'vertauscht']]; if (A.m < 0) f.push([{ m: String(-A.m), b: String(A.b) }, 'Vorzeichen']); return f; },
        pruefen: function(A, e){
          if (bEq(e.m, B(A.b)) && bEq(e.b, B(A.m))) return '\\(m\\) und \\(b\\) sind <b>vertauscht</b>: \\(b\\) ist der Wert am Anfang (\\(x = 0\\)), \\(m\\) die Änderung pro Einheit.';
          if (bEq(e.m, B(-A.m))) return '<b>Vorzeichen</b>: Nimmt der Wert ab, ist \\(m\\) negativ.';
          return (bEq(e.b, B(A.b)) ? 'Der Anfangswert stimmt. ' : 'Der Anfangswert \\(b\\) ist der Wert bei \\(x = 0\\). ') + 'Die Änderung pro Einheit ist \\(m\\).'; },
        tipps: function(A){ return ['Was ist am Anfang? Das ist \\(b\\). Um wie viel ändert es sich pro Einheit? Das ist \\(m\\).', 'Anfang: \\(' + A.b + '\\). Pro Einheit: ' + (A.m < 0 ? 'weniger, also negativ.' : 'mehr, also positiv.')]; },
        loesung: function(A){ return 'y = ' + linTex(B(A.m), A.b); } },

      /* ── Kapitel 2 ── */
      'steigung': { felder: ['m'],
        schl: function(A){ return ppSchl(A.p, A.q); },
        eingabe: function(A){ return { m: bTxt(A.mm).replace('−', '-') }; },
        neu: function(){
          var p, q, dx, dy, s = 0;
          do { p = [nz(-5, 5), nz(-6, 6)]; dx = nz(-6, 6); dy = nz(-8, 8); q = [p[0] + dx, p[1] + dy]; s++; }
          while (s < 200 && (Math.abs(q[0]) > 7 || Math.abs(q[1]) > 9 || dx === dy || (Math.abs(dy) % Math.abs(dx) && Math.abs(dx) > 4)));
          return { p: p, q: q, mm: B(dy, dx), text: 'Berechne die Steigung der Geraden durch \\(P(' + p[0] + ' \\mid ' + p[1] + ')\\) und \\(Q(' + q[0] + ' \\mid ' + q[1] + ')\\).', muster: '\\(m = \\) {m}' }; },
        richtig: function(A, e){ return bEq(e.m, A.mm); },
        fehler: function(A){ var f = [], dx = A.q[0] - A.p[0], dy = A.q[1] - A.p[1];
          if (dy && !bEq(B(dx, dy), A.mm)) f.push([{ m: bTxt(B(dx, dy)).replace('−', '-') }, 'vertauscht']);
          if (!bEq(B(-dy, dx), A.mm)) f.push([{ m: bTxt(B(-dy, dx)).replace('−', '-') }, 'Reihenfolge']);
          return f; },
        pruefen: function(A, e){
          var dx = A.q[0] - A.p[0], dy = A.q[1] - A.p[1];
          if (dy && bEq(e.m, B(dx, dy))) return 'Bruch <b>vertauscht</b>: \\(m = \\dfrac{\\Delta y}{\\Delta x}\\), die \\(y\\)-Differenz kommt oben hin.';
          if (bEq(e.m, B(-dy, dx))) return 'Gleiche <b>Reihenfolge</b> oben und unten: \\(\\dfrac{' + A.q[1] + ' - ' + (A.p[1] < 0 ? '(' + A.p[1] + ')' : A.p[1]) + '}{' + A.q[0] + ' - ' + (A.p[0] < 0 ? '(' + A.p[0] + ')' : A.p[0]) + '}\\), beide Male \\(Q\\) minus \\(P\\).';
          return '\\(m = \\dfrac{\\Delta y}{\\Delta x} = \\dfrac{y_Q - y_P}{x_Q - x_P}\\). Achte auf die Vorzeichen und kürze.'; },
        tipps: function(A){ return ['\\(m = \\dfrac{y_Q - y_P}{x_Q - x_P}\\)', '\\(\\Delta y = ' + (A.q[1] - A.p[1]) + '\\), \\(\\Delta x = ' + (A.q[0] - A.p[0]) + '\\)']; },
        loesung: function(A){ return 'm = \\dfrac{' + (A.q[1] - A.p[1]) + '}{' + (A.q[0] - A.p[0]) + '} = ' + bTex(A.mm); } },

      'ablesen': { felder: ['m'],
        schl: function(A){ return lnSchl(A.mm, B(A.b)); },
        eingabe: function(A){ return { m: bTxt(A.mm).replace('−', '-') }; },
        neu: function(){ var m, b; do { m = steil(); b = nz(-4, 4); } while (!aufGitter(m, b));
          return { mm: m, b: b, text: 'Lies die Steigung der Geraden ab.' + bild(m, b, '0,' + b + ';' + m[1] + ',' + (b + m[0])), muster: '\\(m = \\) {m}' }; },
        richtig: function(A, e){ return bEq(e.m, A.mm); },
        fehler: function(A){ var f = [[{ m: bTxt(B(-A.mm[0], A.mm[1])).replace('−', '-') }, 'Vorzeichen']]; if (Math.abs(A.mm[0]) !== A.mm[1]) f.push([{ m: bTxt(B(A.mm[1], A.mm[0])).replace('−', '-') }, 'vertauscht']); return f; },
        pruefen: function(A, e){
          if (bEq(e.m, B(-A.mm[0], A.mm[1]))) return '<b>Vorzeichen</b>: ' + (A.mm[0] < 0 ? 'Die Gerade fällt von links nach rechts, also ist \\(m\\) negativ.' : 'Die Gerade steigt, also ist \\(m\\) positiv.');
          if (bEq(e.m, B(A.mm[1], A.mm[0]))) return 'Bruch <b>vertauscht</b>: oben das \\(\\Delta y\\) (wie viel hinauf oder hinunter), unten das \\(\\Delta x\\) (wie viel nach rechts).';
          return 'Zeichne ein Steigungsdreieck zwischen zwei Gitterpunkten der Geraden: \\(m = \\dfrac{\\Delta y}{\\Delta x}\\).'; },
        tipps: function(A){ return ['Suche zwei Punkte der Geraden, die genau auf Gitterkreuzungen liegen (die Punkte im Bild).', 'Von \\((0 \\mid ' + A.b + ')\\) aus: \\(' + A.mm[1] + '\\) nach rechts, dann \\(' + Math.abs(A.mm[0]) + '\\) ' + (A.mm[0] > 0 ? 'hinauf' : 'hinunter') + '.']; },
        loesung: function(A){ return 'm = \\dfrac{' + A.mm[0] + '}{' + A.mm[1] + '}' + (A.mm[1] === 1 ? ' = ' + A.mm[0] : ''); } },

      /* ── Kapitel 3 ── */
      'zeichnen': { felder: ['p1', 'p2'],
        schl: function(A){ return lnSchl(A.mm, B(A.b)); },
        eingabe: function(A){ return { p1: '0|' + A.b, p2: A.mm[1] + '|' + (A.b + A.mm[0]) }; },
        neu: function(){ var m, b; do { m = steil(); b = nz(-4, 4); } while (!aufGitter(m, b));
          return { mm: m, b: b, text: 'Zeichne die Gerade \\(y = ' + linTex(m, b) + '\\): Klicke zwei ihrer Punkte im Gitter an.', muster: '<span class="klick-feld"><svg class="klick-gitter" aria-label="Koordinatengitter zum Anklicken"></svg><span class="klick-info"></span></span>{p1}{p2}' }; },
        aufbau: function(A, ein){
          var svg = ein.querySelector('.klick-gitter'), info = ein.querySelector('.klick-info'), i1 = ein.querySelector('[data-f="p1"]'), i2 = ein.querySelector('[data-f="p2"]');
          function malen(){
            var k = Achsen(svg, GITTER), p = [i1.value, i2.value].filter(Boolean).map(function(v){ return v.split('|').map(Number); });
            if (p.length === 2 && (p[0][0] !== p[1][0])) k.gerade((p[1][1] - p[0][1]) / (p[1][0] - p[0][0]), p[0][1] - (p[1][1] - p[0][1]) / (p[1][0] - p[0][0]) * p[0][0], 'linie blau');
            p.forEach(function(q){ k.punkt(q[0], q[1], 'pkt orange', '(' + z(q[0]) + ' | ' + z(q[1]) + ')', 8, -8); });
            info.textContent = p.length < 2 ? 'Klicke ' + (p.length ? 'noch einen Punkt' : 'zwei Punkte') + ' an.' : 'Zwei Punkte gewählt. Nochmals klicken ersetzt den ersten.';
          }
          svg.addEventListener('click', function(ev){
            var r = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal, px = (ev.clientX - r.left) / r.width * vb.width + vb.x, py = (ev.clientY - r.top) / r.height * vb.height + vb.y;
            var w = Achsen(document.createElementNS(NS, 'svg'), GITTER).zuWert(px, py), x = Math.round(w[0]), y = Math.round(w[1]);
            if (Math.abs(x) > 7 || Math.abs(y) > 7) return;
            var v = x + '|' + y;
            if (!i1.value) i1.value = v; else if (!i2.value) i2.value = v; else { i1.value = i2.value; i2.value = v; }
            malen();
          });
          malen();
        },
        richtig: function(A, e){ var drauf = function(p){ return bEq(bAdd(bMul(A.mm, B(p[0])), B(A.b)), B(p[1])); };
          return e.p1[0] !== e.p2[0] && drauf(e.p1) && drauf(e.p2); },
        gewaehlt: function(e){ var m = B(e.p2[1] - e.p1[1], e.p2[0] - e.p1[0]); return { m: m, b: bSub(B(e.p1[1]), bMul(m, B(e.p1[0]))) }; },
        fehler: function(A){ return [[{ p1: '0|' + A.b, p2: A.mm[1] + '|' + (A.b - A.mm[0]) }, 'Vorzeichen'], [{ p1: '0|0', p2: A.mm[1] + '|' + A.mm[0] }, 'y-Achse']]; },
        pruefen: function(A, e){
          if (e.p1[0] === e.p2[0]) return 'Die beiden Punkte liegen senkrecht übereinander. Wähle zwei Punkte mit verschiedenem \\(x\\).';
          var g = TYPEN.zeichnen.gewaehlt(e);
          if (bEq(g.b, B(A.b)) && bEq(g.m, B(-A.mm[0], A.mm[1]))) return 'Der Start auf der \\(y\\)-Achse stimmt. <b>Vorzeichen</b>: Bei \\(m ' + (A.mm[0] < 0 ? '\\lt' : '\\gt') + ' 0\\) geht das Dreieck ' + (A.mm[0] < 0 ? 'hinunter' : 'hinauf') + '.';
          if (bEq(g.m, A.mm) && !bEq(g.b, B(A.b))) return 'Die Steigung stimmt, aber die Gerade schneidet die <b>y-Achse</b> nicht bei \\(' + A.b + '\\). Starte bei \\((0 \\mid ' + A.b + ')\\).';
          if (bEq(g.b, B(A.b))) return 'Der Start bei \\((0 \\mid ' + A.b + ')\\) stimmt, die Steigung nicht: \\(' + A.mm[1] + '\\) nach rechts, \\(' + Math.abs(A.mm[0]) + '\\) ' + (A.mm[0] > 0 ? 'hinauf' : 'hinunter') + '.';
          return 'Starte auf der \\(y\\)-Achse bei \\(b = ' + A.b + '\\), dann mit dem Steigungsdreieck zum zweiten Punkt.'; },
        tipps: function(A){ return ['Erster Punkt: auf der \\(y\\)-Achse bei \\(b = ' + A.b + '\\).', 'Zweiter Punkt: von dort \\(' + A.mm[1] + '\\) nach rechts und \\(' + Math.abs(A.mm[0]) + '\\) ' + (A.mm[0] > 0 ? 'hinauf' : 'hinunter') + '.']; },
        loesung: function(A){ return '(0 \\mid ' + A.b + ') \\text{ und } (' + A.mm[1] + ' \\mid ' + (A.b + A.mm[0]) + ')'; } },

      'nullstelle': { felder: ['x'],
        schl: function(A){ return lnSchl(A.mm, B(A.b)); },
        eingabe: function(A){ return { x: bTxt(A.x0).replace('−', '-') }; },
        neu: function(){ var m, b, x0; do { m = zufall([B(nz(-6, 6)), steil()]); b = nz(-9, 9); x0 = bDiv(B(-b), m); } while (x0[1] > 2 || Math.abs(bZahl(x0)) > 12);
          return { mm: m, b: b, x0: x0, text: 'Wo schneidet \\(y = ' + linTex(m, b) + '\\) die \\(x\\)-Achse?', muster: '\\(x = \\) {x}' }; },
        richtig: function(A, e){ return bEq(e.x, A.x0); },
        fehler: function(A){ var f = []; var v = bDiv(B(A.b), A.mm); if (!bEq(v, A.x0)) f.push([{ x: bTxt(v).replace('−', '-') }, 'Vorzeichen']);
          var w = bMul(B(-A.b), A.mm); if (!bEq(w, A.x0) && !bEq(w, v)) f.push([{ x: bTxt(w).replace('−', '-') }, 'teilen']); return f; },
        pruefen: function(A, e){
          if (bEq(e.x, bDiv(B(A.b), A.mm))) return '<b>Vorzeichen</b>: Aus \\(' + linTex(A.mm, A.b) + ' = 0\\) folgt zuerst \\(' + linTex(A.mm, 0) + ' = ' + (-A.b) + '\\).';
          if (bEq(e.x, bMul(B(-A.b), A.mm))) return 'Durch \\(m\\) <b>teilen</b>, nicht multiplizieren.';
          var w = bAdd(bMul(A.mm, e.x), B(A.b));
          return 'Setz deinen Wert ein: \\(y = ' + bTex(w) + '\\), nicht \\(0\\). Setz \\(y = 0\\) und löse nach \\(x\\).'; },
        tipps: function(A){ return ['Auf der \\(x\\)-Achse ist \\(y = 0\\).', '\\(' + linTex(A.mm, A.b) + ' = 0\\) nach \\(x\\) auflösen.']; },
        loesung: function(A){ return linTex(A.mm, A.b) + ' = 0 \\;\\Rightarrow\\; x = ' + bTex(A.x0); } },

      /* ── Kapitel 4 ── */
      'gleichung': { felder: ['m', 'b'],
        schl: function(A){ return lnSchl(A.mm, B(A.b)); },
        eingabe: function(A){ return { m: bTxt(A.mm).replace('−', '-'), b: String(A.b) }; },
        neu: function(){ var m, b; do { m = steil(); b = nz(-4, 4); } while (!aufGitter(m, b));
          return { mm: m, b: b, text: 'Stelle die Gleichung der Geraden auf: \\(y = m \\cdot x + b\\).' + bild(m, b), muster: '\\(m = \\) {m} &nbsp; \\(b = \\) {b}' }; },
        richtig: function(A, e){ return bEq(e.m, A.mm) && bEq(e.b, B(A.b)); },
        fehler: function(A){ var f = [[{ m: bTxt(B(-A.mm[0], A.mm[1])).replace('−', '-'), b: String(A.b) }, 'Vorzeichen']];
          var x0 = bDiv(B(-A.b), A.mm); if (x0[1] === 1 && x0[0] !== A.b) f.push([{ m: bTxt(A.mm).replace('−', '-'), b: String(x0[0]) }, 'y-Achse']); return f; },
        pruefen: function(A, e){
          var t = [];
          if (!bEq(e.b, B(A.b))) t.push(bEq(e.b, bDiv(B(-A.b), A.mm)) ? '\\(b\\) liest du auf der <b>y-Achse</b> ab, nicht auf der \\(x\\)-Achse.' : '\\(b\\) ist der Wert, wo die Gerade die \\(y\\)-Achse schneidet.');
          if (!bEq(e.m, A.mm)) t.push(bEq(e.m, B(-A.mm[0], A.mm[1])) ? '<b>Vorzeichen</b> von \\(m\\): ' + (A.mm[0] < 0 ? 'Die Gerade fällt.' : 'Die Gerade steigt.') : 'Miss \\(m\\) mit einem Steigungsdreieck zwischen zwei Gitterpunkten.');
          return t.join(' '); },
        tipps: function(A){ return ['Zuerst \\(b\\): Wo schneidet die Gerade die \\(y\\)-Achse? Dann \\(m\\) mit einem Steigungsdreieck.', '\\(b = ' + A.b + '\\). Von \\((0 \\mid ' + A.b + ')\\) aus \\(' + A.mm[1] + '\\) nach rechts.']; },
        loesung: function(A){ return 'y = ' + linTex(A.mm, A.b); } },

      'zweipunkte': { felder: ['m', 'b'],
        schl: function(A){ return ppSchl(A.p, A.q); },
        eingabe: function(A){ return { m: bTxt(A.mm).replace('−', '-'), b: bTxt(A.bb).replace('−', '-') }; },
        neu: function(){
          var m, b, x1, x2, s = 0;
          do { m = steil(); b = nz(-6, 6); x1 = nz(-4, 4); x2 = x1 + m[1] * zufall([1, 2]); s++; }
          while (s < 100 && (x1 === 0 || x2 === 0 || Math.abs(x2) > 8));
          var p = [x1, bZahl(bAdd(bMul(m, B(x1)), B(b)))], q = [x2, bZahl(bAdd(bMul(m, B(x2)), B(b)))];
          if (p[1] % 1 || q[1] % 1) return TYPEN.zweipunkte.neu();
          return { mm: m, bb: B(b), p: p, q: q, text: 'Stelle die Gleichung der Geraden durch \\(A(' + p[0] + ' \\mid ' + p[1] + ')\\) und \\(B(' + q[0] + ' \\mid ' + q[1] + ')\\) auf.', muster: '\\(m = \\) {m} &nbsp; \\(b = \\) {b}' }; },
        richtig: function(A, e){ return bEq(e.m, A.mm) && bEq(e.b, A.bb); },
        fehler: function(A){ var f = []; if (A.p[1] !== A.bb[0] || A.bb[1] !== 1) f.push([{ m: bTxt(A.mm).replace('−', '-'), b: String(A.p[1]) }, 'Wert bei']);
          var k = B(A.q[0] - A.p[0], A.q[1] - A.p[1]); if (A.q[1] !== A.p[1] && !bEq(k, A.mm)) f.push([{ m: bTxt(k).replace('−', '-'), b: bTxt(A.bb).replace('−', '-') }, 'vertauscht']); return f; },
        pruefen: function(A, e){
          var t = [];
          if (!bEq(e.m, A.mm)) t.push(bEq(e.m, B(A.q[0] - A.p[0], A.q[1] - A.p[1])) ? 'Bruch <b>vertauscht</b>: \\(m = \\dfrac{\\Delta y}{\\Delta x}\\).' : 'Zuerst \\(m = \\dfrac{\\Delta y}{\\Delta x}\\) aus den beiden Punkten.');
          else if (!bEq(e.b, A.bb)) t.push(bEq(e.b, B(A.p[1])) ? '\\(b\\) ist der <b>Wert bei</b> \\(x = 0\\), nicht der \\(y\\)-Wert von \\(A\\). Setz \\(A\\) in \\(y = m x + b\\) ein und löse nach \\(b\\).' : 'Setz einen Punkt in \\(y = ' + bTex(A.mm) + ' \\cdot x + b\\) ein und löse nach \\(b\\).');
          t.push(probeTxt(e.m, e.b, A.q[0], A.q[1]));
          return t.join(' '); },
        tipps: function(A){ return ['1. \\(m = \\dfrac{y_B - y_A}{x_B - x_A}\\). 2. Einen Punkt einsetzen und \\(b\\) ausrechnen.', '\\(m = ' + bTex(A.mm) + '\\); \\(' + A.p[1] + ' = ' + bTex(A.mm) + ' \\cdot ' + (A.p[0] < 0 ? '(' + A.p[0] + ')' : A.p[0]) + ' + b\\)']; },
        loesung: function(A){ return 'm = ' + bTex(A.mm) + ', \\quad b = ' + bTex(A.bb) + ', \\quad y = ' + linTex(A.mm, bZahl(A.bb)); } }
    };
    window.__TYPEN = TYPEN; window.__SPERRE = SPERRE; window.__gesperrt = gesperrt;
    /* Rohe Eingaben selbst einlesen (für .claude/tools/pruef-formelsatz.mjs, das pruefen() mit den Werten aus fehler() ruft). */
    Object.keys(TYPEN).forEach(function(n){ var T = TYPEN[n], roh = T.pruefen; T.pruefen = function(A, e){
      var aus = {}; for (var f in e){ var w = e[f]; aus[f] = (w && typeof w === 'object') ? w : f[0] === 'p' ? String(w).split('|').map(Number) : zahlLesen(String(w)).w; }
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
        auf.querySelectorAll('svg.mini-gerade').forEach(function(svg){
          var g = svg.dataset.geraden.split(',').map(function(v){ return v.indexOf('/') >= 0 ? +v.split('/')[0] / +v.split('/')[1] : +v; });
          var p = (svg.dataset.punkte || '').split(';').filter(Boolean).map(function(t){ return t.split(',').map(Number); });
          svg.setAttribute('role', 'img'); miniBild(svg, [g], p);
        });
        var html = A.muster;
        T.felder.forEach(function(f){
          html = html.replace('{' + f + '}', f[0] === 'p'
            ? '<input type="hidden" data-f="' + f + '">'
            : '<input type="text" inputmode="text" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="Zahl" data-f="' + f + '" placeholder="z. B. 2/3">');
        });
        ein.innerHTML = html; rueck.className = 'ue-rueck'; rueck.innerHTML = '';
        if (T.aufbau) T.aufbau(A, ein);
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
          if (!roh) return hinweis(f[0] === 'p' ? 'Klicke zwei Punkte im Gitter an.' : 'Fülle das Feld aus.');
          if (f[0] === 'p'){ e[f] = roh.split('|').map(Number); continue; }
          var z = zahlLesen(roh);
          if (z.kaputt){ inp.classList.add('falsch'); return hinweis(z.kaputt); }
          e[f] = z.w;
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
