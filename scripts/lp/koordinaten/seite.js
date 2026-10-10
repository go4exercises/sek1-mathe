<script>
/* Leitprogramm Abbildungen und Geraden im Koordinatensystem (Geometrie) — Punktspiegelung (Sim 1), Achsenspiegelung (Sim 2),
   zentrische Streckung (Sim 3), Gerade durch zwei Punkte (Sim 4), Übungen mit Rückmeldung.
   Notation: Punkte (x | y), Bildpunkte mit Strich, Zahlen mit Dezimalpunkt und echtem Minus.
   Farben: blau = Original, orange = Bild, grün = Zentrum, Achse und Gerade, rot = Fehler.
   Gerüst: scripts/lp/pythagoras/seite.js. */
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

  function kl(v){ return v < 0 ? '(' + mz(v) + ')' : z(v); }
  function pk(x, y){ return '(' + z(x) + ' | ' + z(y) + ')'; }
  var KS = { w: 280, h: 280, rl: 18, x0: -7, x1: 7, y0: -7, y1: 7, xm: [-6, -4, -2, 2, 4, 6], ym: [-6, -4, -2, 2, 4, 6] };

  /* ════════ Sim 1 — Punktspiegelung ════════
     P und Zentrum Z einstellen; P' = 2Z − P. Gestrichelt die Strecke PP', Z in ihrer Mitte. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    function zustand(){ return { px: wertR(fig, 's1-px'), py: wertR(fig, 's1-py'), zx: wertR(fig, 's1-zx'), zy: wertR(fig, 's1-zy') }; }
    function zeichnen(){
      var Z = zustand(); ['s1-px', 's1-py', 's1-zx', 's1-zy'].forEach(function(i){ zeigeWert(fig, i); });
      var qx = 2 * Z.zx - Z.px, qy = 2 * Z.zy - Z.py, k = Achsen(svg, KS);
      k.strecke(Z.px, Z.py, qx, qy, 'linie grau gestrichelt');
      k.punkt(Z.px, Z.py, 'pkt blau', 'P', 8, -8); k.punkt(qx, qy, 'pkt orange', "P'", 8, -8); k.punkt(Z.zx, Z.zy, 'pkt gruen', 'Z', 8, 14);
      formel.innerHTML = "P' = 2Z − P = (2 · " + kl(Z.zx) + ' − ' + kl(Z.px) + ' | 2 · ' + kl(Z.zy) + ' − ' + kl(Z.py) + ') = <b>' + pk(qx, qy) + '</b>'
        + (Math.abs(qx) > 7 || Math.abs(qy) > 7 ? ' <span class="grau">(ausserhalb des Bildes)</span>' : '');
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    function ist(px, py, zx, zy){ return function(Z){ return Z.px === px && Z.py === py && Z.zx === zx && Z.zy === zy; }; }
    pr = Leiste(fig, [
      { text: 'P(3 | 1) soll auf P\'(−1 | 5) fallen. Stell P ein und such das Zentrum Z.', ok: ist(3, 1, 1, 3) },
      { text: 'Z(0 | 0). Welcher Punkt P hat das Bild P\'(2 | −3)?', ok: ist(-2, 3, 0, 0) },
      { text: 'Z(2 | 2). Stell P so ein, dass P\' genau auf P fällt.', ok: ist(2, 2, 2, 2) },
      { text: 'A(−4 | 1) wird auf A\'(2 | −3) gespiegelt. Wo liegt Z?', ok: ist(-4, 1, -1, -1) },
      { text: 'Z(−1 | 2), das Bild ist P\'(−5 | 0). Wo liegt P?', ok: ist(3, 4, -1, 2) }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 2 — Achsenspiegelung ════════
     Achse: x-Achse, y-Achse, x = a, y = b, y = x. Senkrechte Verbindung gestrichelt, gleich weit auf beiden Seiten. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]'), wahl = fig.querySelector('#s2-ach');
    function zustand(){ return { typ: wahl.value, a: wertR(fig, 's2-a'), px: wertR(fig, 's2-px'), py: wertR(fig, 's2-py') }; }
    function bild(Z){ var x = Z.px, y = Z.py;
      return { x: [x, -y], y: [-x, y], xa: [2 * Z.a - x, y], yb: [x, 2 * Z.a - y], d: [y, x] }[Z.typ]; }
    function zeichnen(){
      var Z = zustand(); ['s2-a', 's2-px', 's2-py'].forEach(function(i){ zeigeWert(fig, i); });
      var q = bild(Z), k = Achsen(svg, KS), name;
      if (Z.typ === 'x') { k.strecke(-7, 0, 7, 0, 'linie gruen'); name = 'x-Achse'; }
      else if (Z.typ === 'y') { k.strecke(0, -7, 0, 7, 'linie gruen'); name = 'y-Achse'; }
      else if (Z.typ === 'xa') { k.strecke(Z.a, -7, Z.a, 7, 'linie gruen'); name = 'Gerade x = ' + z(Z.a); }
      else if (Z.typ === 'yb') { k.strecke(-7, Z.a, 7, Z.a, 'linie gruen'); name = 'Gerade y = ' + z(Z.a); }
      else { k.strecke(-7, -7, 7, 7, 'linie gruen'); name = 'Gerade y = x'; }
      k.strecke(Z.px, Z.py, q[0], q[1], 'linie grau gestrichelt');
      k.punkt(Z.px, Z.py, 'pkt blau', 'P', 8, -8); k.punkt(q[0], q[1], 'pkt orange', "P'", 8, -8);
      formel.innerHTML = 'Spiegelung an der ' + name + ': P' + pk(Z.px, Z.py) + " → <b>P'" + pk(q[0], q[1]) + '</b>';
      fig.querySelector('#s2-a').disabled = !(Z.typ === 'xa' || Z.typ === 'yb');
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, [
      { text: 'P(5 | 1) soll an einer senkrechten Achse x = a auf P\'(−1 | 1) fallen. Stell P und die Achse ein.', ok: function(Z){ return Z.typ === 'xa' && Z.a === 2 && Z.px === 5 && Z.py === 1; } },
      { text: 'Spiegelung an der y-Achse, das Bild ist P\'(3 | −2). Stell P ein.', ok: function(Z){ return Z.typ === 'y' && Z.px === -3 && Z.py === -2; } },
      { text: 'P(2 | 4) und P\'(2 | −2): Welche waagrechte Achse y = b?', ok: function(Z){ return Z.typ === 'yb' && Z.a === 1 && Z.px === 2 && Z.py === 4; } },
      { text: 'Spiegelung an y = x, das Bild ist P\'(−1 | 4). Stell P ein.', ok: function(Z){ return Z.typ === 'd' && Z.px === 4 && Z.py === -1; } },
      { text: 'Q(−3 | 2) soll auf Q\'(−3 | −4) fallen. Stell Q als P ein und such die Achse.', ok: function(Z){ return Z.typ === 'yb' && Z.a === -1 && Z.px === -3 && Z.py === 2; } }
    ], sim);
    fig.querySelectorAll('input, select').forEach(function(i){ i.addEventListener('input', zeichnen); i.addEventListener('change', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 3 — Zentrische Streckung ════════
     Dreieck A(2 | 1), B(5 | 1), C(3 | 3) (Fläche 3), Zentrum Z, Faktor k: P' = Z + k · (P − Z). */
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    var D = [[2, 1], [5, 1], [3, 3]], N = ['A', 'B', 'C'];
    var O = { w: 300, h: 240, rl: 18, x0: -4, x1: 16, y0: -4, y1: 12, sx: 1, sy: 1, xm: [-2, 2, 4, 6, 8, 10, 12, 14], ym: [-2, 2, 4, 6, 8, 10] };
    function zustand(){ return { zx: wertR(fig, 's3-zx'), zy: wertR(fig, 's3-zy'), k: wertR(fig, 's3-k') }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's3-zx'); zeigeWert(fig, 's3-zy'); zeigeWert(fig, 's3-k', z(Z.k));
      var k = Achsen(svg, O), B_ = D.map(function(p){ return [Z.zx + Z.k * (p[0] - Z.zx), Z.zy + Z.k * (p[1] - Z.zy)]; });
      D.forEach(function(p, i){ k.strecke(Z.zx, Z.zy, B_[i][0], B_[i][1], 'linie grau gestrichelt'); });
      [[D, 'linie blau'], [B_, 'linie orange']].forEach(function(t){ var q = t[0];
        for (var i = 0; i < 3; i++) k.strecke(q[i][0], q[i][1], q[(i + 1) % 3][0], q[(i + 1) % 3][1], t[1]); });
      D.forEach(function(p, i){ k.punkt(p[0], p[1], 'pkt blau', N[i], -12, -6); k.punkt(B_[i][0], B_[i][1], 'pkt orange', N[i] + "'", 8, -6); });
      k.punkt(Z.zx, Z.zy, 'pkt gruen', 'Z', 8, 14);
      formel.innerHTML = "A' = Z + k · (A − Z) = <b>" + pk(B_[0][0], B_[0][1]) + '</b> &nbsp;·&nbsp; Fläche 3 → <b>' + z(3 * Z.k * Z.k) + '</b> (mal k² = ' + z(Z.k * Z.k) + ')';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, [
      { text: 'Z(0 | 0). Bei welchem k fällt A(2 | 1) auf A\'(4 | 2)?', ok: function(Z){ return Z.zx === 0 && Z.zy === 0 && Z.k === 2; } },
      { text: 'k = 2. Wo muss Z liegen, damit A(2 | 1) auf A\'(3 | 1) fällt?', ok: function(Z){ return Z.zx === 1 && Z.zy === 1 && Z.k === 2; } },
      { text: 'Z(0 | 0). Die Fläche soll 9-mal so gross werden.', ok: function(Z){ return Z.zx === 0 && Z.zy === 0 && Z.k === 3; } },
      { text: 'Z(0 | 0). Das Bild soll halb so lange Seiten haben.', ok: function(Z){ return Z.zx === 0 && Z.zy === 0 && Z.k === 0.5; } },
      { text: 'k = 2. Wähle Z so, dass B selbst liegen bleibt.', ok: function(Z){ return Z.zx === 5 && Z.zy === 1 && Z.k === 2; } }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 4 — Gerade durch zwei Punkte ════════
     A und B einstellen; m = (yB − yA) : (xB − xA), b aus y = m · x + b mit A. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    function zustand(){ return { ax: wertR(fig, 's4-ax'), ay: wertR(fig, 's4-ay'), bx: wertR(fig, 's4-bx'), by: wertR(fig, 's4-by') }; }
    function mb(Z){ if (Z.ax === Z.bx) return null; var m = B(Z.by - Z.ay, Z.bx - Z.ax); return { m: m, b: bSub(B(Z.ay), bMul(m, B(Z.ax))) }; }
    function zeichnen(){
      var Z = zustand(); ['s4-ax', 's4-ay', 's4-bx', 's4-by'].forEach(function(i){ zeigeWert(fig, i); });
      var k = Achsen(svg, KS), g = mb(Z);
      if (g) k.gerade(bZahl(g.m), bZahl(g.b), 'linie gruen');
      else if (Z.ay !== Z.by) k.strecke(Z.ax, -7, Z.ax, 7, 'linie gruen');
      k.punkt(Z.ax, Z.ay, 'pkt blau', 'A', 8, -8); k.punkt(Z.bx, Z.by, 'pkt orange', 'B', 8, -8);
      if (!g) formel.innerHTML = Z.ay === Z.by ? 'A und B fallen zusammen: Durch einen Punkt gehen viele Geraden.' : 'Senkrechte Gerade x = ' + z(Z.ax) + ': keine Funktion, keine Steigung.';
      else formel.innerHTML = 'm = (' + kl(Z.by) + ' − ' + kl(Z.ay) + ') : (' + kl(Z.bx) + ' − ' + kl(Z.ax) + ') = ' + bTxt(g.m) + ' &nbsp;·&nbsp; <b>' + linTxt(g.m, bZahl(g.b)) + '</b>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    function gl(m, b){ return function(Z){ var g = mb(Z); return g && bEq(g.m, m) && bEq(g.b, b); }; }
    pr = Leiste(fig, [
      { text: 'A(0 | −2). Stell B auf die Gerade x = 4, so dass die Steigung 1.5 ist.', ok: function(Z){ return Z.ax === 0 && Z.ay === -2 && Z.bx === 4 && Z.by === 4; } },
      { text: 'Stell A und B so ein, dass beide auf y = −x + 5 liegen.', ok: gl(B(-1), B(5)) },
      { text: 'A(1 | 1). Stell B so ein, dass die Gerade parallel zu y = 2x ist.', ok: function(Z){ return Z.ax === 1 && Z.ay === 1 && gl(B(2), B(-1))(Z); } },
      { text: 'Stell eine waagrechte Gerade durch y = 3 ein.', ok: gl(B(0), B(3)) },
      { text: 'A(−3 | 0). B liegt auf x = 3, die Gerade schneidet die y-Achse bei 2.', ok: function(Z){ return Z.ax === -3 && Z.ay === 0 && Z.bx === 3 && Z.by === 4; } }
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
     Zahlenfelder exakt (2/3, −1.5, 4). Feld w: Auswahl (select). Fehlversuch → gezielte Diagnose nach der Eingabe.
     Tipps in drei Stufen. Testhaken: box.__aufgabe, box.__typ. */
  (function(){
    var ALLE = document.querySelectorAll('.uebung[data-typ]'); if (!ALLE.length) return;

    /* Feste Aufgaben (Clips, Festhalten, Erkundungen, Kapitelaufgaben, Gesamttest): nie als Zufallsübung. */
    var SPERRE = [
      'pb|5|3|2|1', 'pb|3|4|2|1', 'pb|4|3|1|2', 'pb|5|2|1|1', 'pb|3|-1|1|1', 'pb|1|5|-2|3', 'pb|4|1|2|3', 'pb|3|-4|0|0', 'pb|4|6|1|2',
      'pb|2|1|1|0', 'pb|5|2|1|0', 'pb|3|4|1|0', 'pb|1|2|3|3',
      'zt|3|1|-1|5', 'zt|-4|1|2|-3', 'zt|7|2|-1|6', 'zt|2|5|6|1', 'zt|-3|4|5|0', 'zt|-5|0|-1|2',
      'ab|3|2|x', 'ab|3|2|y', 'ab|3|2|xa|1', 'ab|3|2|d', 'ab|4|1|xa|2', 'ab|5|-1|x', 'ab|5|-1|y', 'ab|5|-1|xa|2', 'ab|5|-1|yb|2', 'ab|5|-1|d',
      'ab|4|-3|x', 'ab|4|-3|y', 'ab|4|-3|d', 'ab|-2|5|xa|3', 'ab|1|-2|yb|2', 'ab|3|5|x', 'ab|-4|1|y', 'ab|2|3|xa|5', 'ab|6|-1|d', 'ab|0|4|yb|1',
      'ab|4|-1|x', 'ab|4|-1|y', 'ab|4|-1|d', 'ab|1|-1|xa|2',
      'af|5|1|-1|1', 'af|2|4|2|-2', 'af|-3|2|-3|-4', 'af|2|7|2|-1', 'af|-2|3|6|3',
      'sb|1|1|0|0|2', 'sb|2|3|1|1|3', 'sb|5|3|2|1|2', 'sb|4|3|1|1|2', 'sb|2|-1|0|0|3', 'sb|3|3|1|2|2', 'sb|2|1|1|1|2',
      'kf|1|1|5|2|2|4', 'kf|0|0|6|1|2|5', 'kf|1|1|5|1|3|4', 'kf|0|0|8|2|3|6',
      'g2|1|3|4|9', 'g2|2|1|6|9', 'g2|-2|5|4|-1', 'g2|1|2|3|8', 'g2|0|1|2|7', 'g2|-1|-5|3|7', 'g2|1|2|5|4',
      'pp|2|1|10|21', 'pp|2|1|50|102', 'pp|2|1|100|201', 'pp|2|-3|40|77', 'pp|2|-3|25|46', 'pp|3|-5|10|25', 'pp|2|5|20|50', 'pp|3|-2|50|148', 'pp|3|-2|-20|-61'
    ];
    function d(v){ return bWert(bDez(v)); }
    function eing(a){ return bWert(a).replace('−', '-'); }
    function gesperrt(T, A){ return !!T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }
    function pt(x, y){ return '\\((' + mz(x).replace('−', '-') + ' \\mid ' + mz(y).replace('−', '-') + ')\\)'; }
    function ptx(x, y){ return '(' + mz(x).replace('−', '-') + ' \\mid ' + mz(y).replace('−', '-') + ')'; }
    function nz2(a, b, ohne){ var r; do { r = zufallG(a, b); } while (r === ohne); return r; }
    var ACHSE = { x: 'an der x-Achse', y: 'an der y-Achse', d: 'an der Geraden y = x' };

    var TYPEN = {
      /* ── Kapitel 1 ── */
      'punktbild': { felder: ['x', 'y'],
        schl: function(A){ return 'pb|' + A.px + '|' + A.py + '|' + A.zx + '|' + A.zy; },
        eingabe: function(A){ return { x: String(A.qx), y: String(A.qy) }; },
        neu: function(){
          var px = nz(-6, 6), py = nz(-6, 6), zx = zufallG(-4, 4), zy = zufallG(-4, 4);
          if ((px === zx && py === zy) || Math.abs(2 * zx - px) > 9 || Math.abs(2 * zy - py) > 9) return TYPEN.punktbild.neu();
          return { px: px, py: py, zx: zx, zy: zy, qx: 2 * zx - px, qy: 2 * zy - py, text: 'Spiegle den Punkt P' + pt(px, py) + ' am Zentrum Z' + pt(zx, zy) + '.', muster: "P'( {x} | {y} )" }; },
        richtig: function(A, e){ return bEq(e.x, B(A.qx)) && bEq(e.y, B(A.qy)); },
        fehler: function(A){ var f = [];
          if (A.px + A.zx !== A.qx || A.py + A.zy !== A.qy) f.push([{ x: String(A.px + A.zx), y: String(A.py + A.zy) }, 'Mitte']);
          if (A.zx - A.px !== A.qx || A.zy - A.py !== A.qy) f.push([{ x: String(A.zx - A.px), y: String(A.zy - A.py) }, 'Mitte']);
          return f; },
        pruefen: function(A, e){
          var gx = bEq(e.x, B(A.qx)), gy = bEq(e.y, B(A.qy));
          var summe = bEq(e.x, B(A.px + A.zx)) && bEq(e.y, B(A.py + A.zy)), diff = bEq(e.x, B(A.zx - A.px)) && bEq(e.y, B(A.zy - A.py));
          if (!summe && !diff && gx !== gy) return 'Eine Koordinate stimmt. Prüf die ' + (gx ? 'y' : 'x') + '-Koordinate: Auch sie geht von P aus über Z gleich weit weiter.';
          return 'Z ist die <b>Mitte</b> zwischen P und P\'. Geh von P bis Z und dann nochmals gleich weit: \\(P\' = 2Z - P\\).'; },
        tipps: function(A){ return ['Von P nach Z: \\(' + kl(A.zx - A.px) + '\\) nach rechts, \\(' + kl(A.zy - A.py) + '\\) nach oben. Dasselbe nochmals ab Z.', '\\(x\' = 2 \\cdot ' + kl(A.zx) + ' - ' + kl(A.px) + '\\)']; },
        loesung: function(A){ return "P' = (2 \\cdot " + kl(A.zx) + ' - ' + kl(A.px) + ' \\mid 2 \\cdot ' + kl(A.zy) + ' - ' + kl(A.py) + ') = ' + ptx(A.qx, A.qy); } },

      'zentrum': { felder: ['x', 'y'],
        schl: function(A){ return 'zt|' + A.px + '|' + A.py + '|' + A.qx + '|' + A.qy; },
        eingabe: function(A){ return { x: String(A.zx), y: String(A.zy) }; },
        neu: function(){
          var zx = zufallG(-3, 3), zy = zufallG(-3, 3), px = nz(-6, 6), py = nz(-6, 6), qx = 2 * zx - px, qy = 2 * zy - py;
          if (Math.abs(qx) > 7 || Math.abs(qy) > 7 || (px === qx && py === qy)) return TYPEN.zentrum.neu();
          return { px: px, py: py, qx: qx, qy: qy, zx: zx, zy: zy, text: 'Bei einer Punktspiegelung wird P' + pt(px, py) + ' auf P\'' + pt(qx, qy) + ' abgebildet. Wo liegt das Zentrum Z?', muster: 'Z( {x} | {y} )' }; },
        richtig: function(A, e){ return bEq(e.x, B(A.zx)) && bEq(e.y, B(A.zy)); },
        fehler: function(A){ return A.qx - A.px === A.zx && A.qy - A.py === A.zy ? [] : [[{ x: String(A.qx - A.px), y: String(A.qy - A.py) }, 'Mitte']]; },
        pruefen: function(A, e){
          if (bEq(e.x, B(A.qx - A.px)) && bEq(e.y, B(A.qy - A.py))) return 'Das ist der Weg von P nach P\'. Z liegt in der <b>Mitte</b> dieses Weges.';
          return 'Z ist die <b>Mitte</b> von P und P\': je die beiden Koordinaten addieren und durch 2 teilen.'; },
        tipps: function(A){ return ['Z ist der Mittelpunkt der Strecke PP\'.', '\\(x_Z = \\dfrac{' + A.px + ' + ' + kl(A.qx) + '}{2}\\)']; },
        loesung: function(A){ return 'Z = \\left(\\dfrac{' + A.px + ' + ' + kl(A.qx) + '}{2} \\mid \\dfrac{' + A.py + ' + ' + kl(A.qy) + '}{2}\\right) = ' + ptx(A.zx, A.zy); } },

      /* ── Kapitel 2 ── */
      'achsbild': { felder: ['x', 'y'],
        schl: function(A){ return 'ab|' + A.px + '|' + A.py + '|' + A.art + (A.art === 'xa' || A.art === 'yb' ? '|' + A.a : ''); },
        eingabe: function(A){ return { x: String(A.q[0]), y: String(A.q[1]) }; },
        neu: function(){
          var art = zufall(['x', 'y', 'xa', 'yb', 'd']), px = nz(-6, 6), py = nz(-6, 6), a = nz(-3, 3), q;
          q = { x: [px, -py], y: [-px, py], xa: [2 * a - px, py], yb: [px, 2 * a - py], d: [py, px] }[art];
          if (Math.abs(q[0]) > 9 || Math.abs(q[1]) > 9 || (q[0] === px && q[1] === py)) return TYPEN.achsbild.neu();
          var wo = art === 'xa' ? 'an der Geraden x = ' + a : art === 'yb' ? 'an der Geraden y = ' + a : ACHSE[art];
          return { art: art, a: a, px: px, py: py, q: q, text: 'Spiegle P' + pt(px, py) + ' ' + wo.replace('-', '−') + '.', muster: "P'( {x} | {y} )" }; },
        richtig: function(A, e){ return bEq(e.x, B(A.q[0])) && bEq(e.y, B(A.q[1])); },
        fehler: function(A){
          var f = { x: [-A.px, A.py], y: [A.px, -A.py], xa: [A.px, 2 * A.a - A.py], yb: [2 * A.a - A.px, A.py], d: [-A.px, -A.py] }[A.art];
          return f[0] === A.q[0] && f[1] === A.q[1] ? [] : [[{ x: String(f[0]), y: String(f[1]) }, 'Achse']]; },
        pruefen: function(A, e){
          var gx = bEq(e.x, B(A.q[0])), gy = bEq(e.y, B(A.q[1]));
          if (A.art === 'd') return 'An der <b>Achse</b> y = x tauschen x und y ihre Plätze. Keine Vorzeichen ändern.';
          return 'Welche Koordinate ändert sich? Bei einer waagrechten <b>Achse</b> ändert sich y, bei einer senkrechten x. Die andere bleibt.' + (gx !== gy ? ' Eine Koordinate stimmt schon.' : ''); },
        tipps: function(A){ return [A.art === 'x' || A.art === 'yb' ? 'Die Achse ist waagrecht: x bleibt gleich.' : A.art === 'd' ? 'An y = x werden die Koordinaten vertauscht.' : 'Die Achse ist senkrecht: y bleibt gleich.',
          A.art === 'xa' ? 'P ist ' + Math.abs(A.px - A.a) + ' von der Achse entfernt. Gleich weit auf die andere Seite.' : A.art === 'yb' ? 'P ist ' + Math.abs(A.py - A.a) + ' von der Achse entfernt. Gleich weit auf die andere Seite.' : 'Gleicher Abstand zur Achse, auf der anderen Seite.']; },
        loesung: function(A){ return "P' = " + ptx(A.q[0], A.q[1]); } },

      'achsefinden': { felder: ['w', 'a'],
        schl: function(A){ return 'af|' + A.px + '|' + A.py + '|' + A.qx + '|' + A.qy; },
        eingabe: function(A){ return { w: A.art, a: String(A.a) }; },
        neu: function(){
          var art = zufall(['x', 'y']), a = zufallG(-3, 3), px = nz(-6, 6), py = nz(-6, 6), qx = px, qy = py;
          if (art === 'x'){ qx = 2 * a - px; } else { qy = 2 * a - py; }
          if (Math.abs(qx) > 9 || Math.abs(qy) > 9 || (qx === px && qy === py)) return TYPEN.achsefinden.neu();
          return { art: art, a: a, px: px, py: py, qx: qx, qy: qy, text: 'P' + pt(px, py) + ' wird an einer Achse auf P\'' + pt(qx, qy) + ' gespiegelt. Welche Gerade ist die Spiegelachse?',
                   muster: '{w} = {a}', optionen: [['x', 'x'], ['y', 'y']] }; },
        richtig: function(A, e){ return e.w === A.art && bEq(e.a, B(A.a)); },
        fehler: function(A){ return [[{ w: A.art === 'x' ? 'y' : 'x', a: String(A.a) }, 'senkrecht']]; },
        pruefen: function(A, e){
          if (e.w !== A.art) return 'Die Verbindung PP\' steht <b>senkrecht</b> auf der Achse. Welche Koordinate ändert sich, welche bleibt?';
          return 'Die Achse liegt in der Mitte zwischen P und P\'.'; },
        tipps: function(A){ return [A.art === 'x' ? 'Nur x ändert sich: Die Achse ist senkrecht, x = …' : 'Nur y ändert sich: Die Achse ist waagrecht, y = …', 'Mitte: \\(\\dfrac{' + (A.art === 'x' ? A.px + ' + ' + kl(A.qx) : A.py + ' + ' + kl(A.qy)) + '}{2}\\)']; },
        loesung: function(A){ return A.art + ' = ' + A.a; } },

      /* ── Kapitel 3 ── */
      'streckbild': { felder: ['x', 'y'],
        schl: function(A){ return 'sb|' + A.px + '|' + A.py + '|' + A.zx + '|' + A.zy + '|' + A.k; },
        eingabe: function(A){ return { x: eing(A.qx), y: eing(A.qy) }; },
        neu: function(){
          var k = zufall([2, 3, 0.5, 1.5, 2, 3]), zx = zufallG(-3, 3), zy = zufallG(-3, 3), px = zufallG(-4, 5), py = zufallG(-4, 5);
          if (px === zx && py === zy) return TYPEN.streckbild.neu();
          var qx = bAdd(B(zx), bMul(bDez(k), B(px - zx))), qy = bAdd(B(zy), bMul(bDez(k), B(py - zy)));
          if (qx[1] > 2 || qy[1] > 2 || (zx === 0 && zy === 0 && Math.random() < 0.6)) return TYPEN.streckbild.neu();
          return { px: px, py: py, zx: zx, zy: zy, k: k, qx: qx, qy: qy, text: 'Strecke P' + pt(px, py) + ' vom Zentrum Z' + pt(zx, zy) + ' aus mit dem Faktor k = ' + d(k) + '.', muster: "P'( {x} | {y} )" }; },
        richtig: function(A, e){ return bEq(e.x, A.qx) && bEq(e.y, A.qy); },
        fehler: function(A){ var fx = bMul(bDez(A.k), B(A.px)), fy = bMul(bDez(A.k), B(A.py)); return bEq(fx, A.qx) && bEq(fy, A.qy) ? [] : [[{ x: eing(fx), y: eing(fy) }, 'Zentrum']]; },
        pruefen: function(A, e){
          if (bEq(e.x, bMul(bDez(A.k), B(A.px))) && bEq(e.y, bMul(bDez(A.k), B(A.py)))) return 'So wäre es mit dem <b>Zentrum</b> im Ursprung. Rechne den Weg von Z nach P mal k und geh ihn ab Z.';
          return 'Weg von Z nach P: \\((' + kl(A.px - A.zx) + ' \\mid ' + kl(A.py - A.zy) + ')\\). Mal k, dann ab Z abtragen.'; },
        tipps: function(A){ return ['Weg von Z nach P: \\((' + kl(A.px - A.zx) + ' \\mid ' + kl(A.py - A.zy) + ')\\)', 'mal \\(' + d(A.k) + '\\), dann zu Z addieren']; },
        loesung: function(A){ return "P' = (" + kl(A.zx) + ' + ' + d(A.k) + ' \\cdot ' + kl(A.px - A.zx) + ' \\mid ' + kl(A.zy) + ' + ' + d(A.k) + ' \\cdot ' + kl(A.py - A.zy) + ') = (' + bWertTex(A.qx) + ' \\mid ' + bWertTex(A.qy) + ')'; } },

      'koordflaeche': { felder: ['A'],
        schl: function(A){ return 'kf|' + A.p.join('|'); },
        eingabe: function(A){ return { A: eing(A.F) }; },
        neu: function(){
          var w = zufallG(4, 8), h = zufallG(3, 7), u = zufallG(1, w - 1), v = zufallG(1, h - 1), x0 = zufallG(0, 2), y0 = zufallG(0, 2);
          var P1 = [x0, y0], P2 = [x0 + w, y0 + v], P3 = [x0 + u, y0 + h];
          var F = B(Math.abs(P1[0] * (P2[1] - P3[1]) + P2[0] * (P3[1] - P1[1]) + P3[0] * (P1[1] - P2[1])), 2);
          if (F[1] > 2) return TYPEN.koordflaeche.neu();
          return { p: [P1[0], P1[1], P2[0], P2[1], P3[0], P3[1]], w: w, h: h, F: F, R: w * h,
                   text: 'Wie gross ist die Fläche des Dreiecks mit den Ecken A' + pt(P1[0], P1[1]) + ', B' + pt(P2[0], P2[1]) + ' und C' + pt(P3[0], P3[1]) + '? (Einheit: Kästchen)', muster: 'A = {A}' }; },
        richtig: function(A, e){ return bEq(e.A, A.F); },
        fehler: function(A){ return [[{ A: String(A.R) }, 'abziehen']]; },
        pruefen: function(A, e){
          if (bEq(e.A, B(A.R))) return 'Das ist das ganze umschliessende Rechteck. Die drei rechtwinkligen Dreiecke rundherum musst du noch <b>abziehen</b>.';
          return 'Zeichne das kleinste Rechteck um das Dreieck. Rechteck minus die drei rechtwinkligen Randdreiecke.'; },
        tipps: function(A){ return ['Umschliessendes Rechteck: \\(' + A.w + ' \\cdot ' + A.h + ' = ' + A.R + '\\)', 'Die drei Randdreiecke haben je die Hälfte von Breite mal Höhe.']; },
        loesung: function(A){ return A.R + ' - \\text{Randdreiecke} = ' + bWertTex(A.F); } },

      /* ── Kapitel 4 ── */
      'gerade2': { felder: ['m', 'b'],
        schl: function(A){ return 'g2|' + A.ax + '|' + A.ay + '|' + A.bx + '|' + A.by; },
        eingabe: function(A){ return { m: eing(A.m), b: eing(A.b) }; },
        neu: function(){
          var m = zufall([[1, 1], [2, 1], [3, 1], [-1, 1], [-2, 1], [1, 2], [-1, 2], [3, 2], [-3, 1], [2, 3]]), b = nz(-6, 6), ax = zufallG(-4, 3), dx = m[1] * zufallG(1, 2);
          var M = B(m[0], m[1]), ay = bAdd(bMul(M, B(ax)), B(b)), bx = ax + dx, by = bAdd(bMul(M, B(bx)), B(b));
          if (ay[1] !== 1 || by[1] !== 1 || Math.abs(ay[0]) > 12 || Math.abs(by[0]) > 12) return TYPEN.gerade2.neu();
          return { ax: ax, ay: ay[0], bx: bx, by: by[0], m: M, b: B(b), text: 'Die Gerade geht durch A' + pt(ax, ay[0]) + ' und B' + pt(bx, by[0]) + '. Bestimme die Gleichung y = m · x + b.', muster: 'm = {m} &nbsp; b = {b}' }; },
        richtig: function(A, e){ return bEq(e.m, A.m) && bEq(e.b, A.b); },
        fehler: function(A){ var f = B(A.bx - A.ax, A.by - A.ay); return A.by === A.ay || bEq(f, A.m) ? [] : [[{ m: eing(f), b: eing(bSub(B(A.ay), bMul(f, B(A.ax)))) }, 'Kopf']]; },
        pruefen: function(A, e){
          if (A.by !== A.ay && bEq(e.m, B(A.bx - A.ax, A.by - A.ay))) return 'Der Bruch steht auf dem Kopf: \\(m = \\dfrac{\\Delta y}{\\Delta x}\\), Unterschied der y-Werte durch Unterschied der x-Werte.';
          if (bEq(e.m, A.m)) return 'm stimmt. Für b setzt du einen Punkt ein: \\(' + A.ay + ' = ' + bTex(A.m) + ' \\cdot ' + kl(A.ax) + ' + b\\).';
          return 'Steigung: \\(m = \\dfrac{\\Delta y}{\\Delta x}\\). Dann einen Punkt einsetzen und nach b auflösen.'; },
        tipps: function(A){ return ['\\(m = \\dfrac{' + A.by + ' - ' + kl(A.ay) + '}{' + A.bx + ' - ' + kl(A.ax) + '}\\)', 'A einsetzen: \\(' + A.ay + ' = m \\cdot ' + kl(A.ax) + ' + b\\)']; },
        loesung: function(A){ return 'm = ' + bTex(A.m) + ', \\quad b = ' + bTex(A.b) + ', \\quad y = ' + linTex(A.m, A.b[0]); } },

      'punktprobe': { felder: ['w'],
        schl: function(A){ return 'pp|' + A.m + '|' + A.b + '|' + A.x + '|' + A.y; },
        eingabe: function(A){ return { w: A.auf ? 'ja' : 'nein' }; },
        neu: function(){
          var m = nz(-4, 4), b = nz(-9, 9), x = zufall([zufallG(12, 60), -zufallG(10, 40), zufallG(100, 300)]), auf = Math.random() < 0.5;
          var y = m * x + b + (auf ? 0 : zufall([-2, -1, 1, 2]));
          return { m: m, b: b, x: x, y: y, auf: auf, text: 'Liegt der Punkt P' + pt(x, y) + ' auf der Geraden \\(y = ' + linTex(B(m), b) + '\\)? (Er liegt weit ausserhalb jeder Zeichnung.)',
                   muster: '{w}', optionen: [['ja', 'ja, er liegt darauf'], ['nein', 'nein, er liegt nicht darauf']] }; },
        richtig: function(A, e){ return e.w === (A.auf ? 'ja' : 'nein'); },
        fehler: function(A){ return [[{ w: A.auf ? 'nein' : 'ja' }, 'einsetzen']]; },
        pruefen: function(A, e){ return 'Setz x = ' + A.x + ' ein und vergleiche mit dem y-Wert des Punktes: Stimmt die Gleichung genau, liegt er darauf. Prüf nochmals mit <b>einsetzen</b>.'; },
        tipps: function(A){ return ['\\(' + A.m + ' \\cdot ' + kl(A.x) + ' + ' + kl(A.b) + ' = \\;?\\)', 'Vergleiche mit \\(y = ' + A.y + '\\).']; },
        loesung: function(A){ return A.m + ' \\cdot ' + kl(A.x) + ' + ' + kl(A.b) + ' = ' + (A.m * A.x + A.b) + (A.auf ? ' = ' : ' \\neq ') + A.y + ' \\;\\Rightarrow\\; \\text{' + (A.auf ? 'liegt darauf' : 'liegt nicht darauf') + '}'; } }
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
