<script>
/* Leitprogramm Darstellungen wechseln (Lineare Funktionen II) — vier Darstellungen gekoppelt (Sim 1), Rechteck mit festem
   Umfang (Sim 2), Definitionsbereich und Darstellung (Sim 3), Summe oder Produkt (Sim 4), Übungen mit Rückmeldung.
   Notation: y = m · x + b, Punkte (x | y), Zahlen mit Dezimalpunkt und echtem Minus.
   Farben (eine Farbe, eine Bedeutung): blau = Gerade, m und der lineare Zusammenhang, orange = b, grün = Treffer und
   Ergebnis, rot = Fehler, Tinte = die antiproportionale Kurve. Gerüst: scripts/lp/lineare-funktionen/seite.js. */
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

  /* ════════ Sim 1 — Vier Darstellungen ════════
     Eine Situation, gleichzeitig als Satz, Gleichung, Wertetabelle und Graph. Der Regler x markiert ein Wertepaar,
     das die Zeile darunter in Worten sagt. */
  (function(){
    var fig = document.getElementById('sim1'); if (!fig) return;
    var svg = fig.querySelector('svg'), tab = fig.querySelector('table.wt'), formel = fig.querySelector('[data-rolle="formel"]'),
        satz = fig.querySelector('[data-rolle="satz"]');
    var F1 = { w: 300, h: 220, rl: 30, x0: 0, x1: 10, y0: -40, y1: 160, sx: 1, sy: 20, xm: [2, 4, 6, 8, 10], ym: [-40, -20, 20, 40, 60, 80, 100, 120, 140, 160] };
    function zustand(){ return { b: wertR(fig, 's1-b'), m: wertR(fig, 's1-m'), x: wertR(fig, 's1-x') }; }
    function zeichnen(){
      var Z = zustand(), yx = Z.m * Z.x + Z.b; zeigeWert(fig, 's1-b'); zeigeWert(fig, 's1-m'); zeigeWert(fig, 's1-x');
      var k = Achsen(svg, F1);
      k.gerade(Z.m, Z.b, 'linie blau', 0, 10);
      k.punkt(0, Z.b, 'pkt orange');
      k.strecke(Z.x, 0, Z.x, yx, 'linie grau gestrichelt');
      k.punkt(Z.x, yx, 'pkt gruen', '(' + Z.x + ' | ' + z(yx) + ')', 8, -8);
      var h = '<tr><th>x</th>', w = '<tr><th>y</th>';
      for (var t = 0; t <= 5; t++){ h += '<td' + (t === Z.x ? ' class="an"' : '') + '>' + t + '</td>'; w += '<td' + (t === Z.x ? ' class="an"' : '') + '>' + z(Z.m * t + Z.b) + '</td>'; }
      tab.innerHTML = h + '</tr>' + w + '</tr><tr><th></th><td></td>' + [1, 2, 3, 4, 5].map(function(){ return '<td class="dif">' + (Z.m >= 0 ? '+' : '−') + Math.abs(Z.m) + '</td>'; }).join('') + '</tr>';
      formel.innerHTML = linTxt(Z.m, Z.b);
      satz.innerHTML = 'Am Anfang (x = 0) ist y = <b class="orange">' + z(Z.b) + '</b>. Wird x um 1 grösser, ' + (Z.m ? 'ändert sich y um <b class="blau">' + (Z.m > 0 ? '+' : '−') + Math.abs(Z.m) + '</b>' : 'bleibt y gleich') + '. '
        + '<span class="grau">Der Punkt (' + Z.x + ' | ' + z(yx) + ') sagt: Bei x = ' + Z.x + ' ist y = ' + z(yx) + '.</span>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, [
      { text: 'Text: «Am Anfang 20, wird \\(x\\) um 1 grösser, kommen 5 dazu.» Stell \\(b\\) und \\(m\\) passend ein.',
        ok: function(Z){ return Z.b === 20 && Z.m === 5; } },
      { text: 'Tabelle: \\(x\\): 0, 1, 2 und \\(y\\): 30, 27, 24. Stell die passende Gerade ein.',
        ok: function(Z){ return Z.b === 30 && Z.m === -3; } },
      { text: 'Tabelle: \\(x\\): 2, 4, 6 und \\(y\\): 18, 26, 34. Achtung, die Schritte sind 2 breit.',
        ok: function(Z){ return Z.b === 10 && Z.m === 4; } },
      { text: 'Aussage: «Bei \\(x = 4\\) ist \\(y = 42\\), und pro 1 in \\(x\\) kommen 7 dazu.» Stell die Gerade ein und zieh \\(x\\) auf 4.',
        ok: function(Z){ return Z.b === 14 && Z.m === 7 && Z.x === 4; } },
      { text: 'Zwei Punkte: Die Gerade geht durch \\((2 \\mid 35)\\) und \\((6 \\mid 15)\\). Stell sie ein.',
        ok: function(Z){ return Z.b === 45 && Z.m === -5; } }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 2 — Rechteck mit festem Umfang ════════
     2x + 2y = U, also y = U/2 − x. Links das Rechteck, rechts der Punkt (x | y) auf der fallenden Geraden.
     Ist x ≥ U/2, gibt es kein Rechteck mehr (y ≤ 0): Das ist der Rand des Definitionsbereichs. */
  (function(){
    var fig = document.getElementById('sim2'); if (!fig) return;
    var bild = fig.querySelector('svg.rechteck-bild'), svg = fig.querySelector('svg.graf'), formel = fig.querySelector('[data-rolle="formel"]');
    var F2 = { w: 260, h: 260, rl: 22, x0: 0, x1: 20, y0: 0, y1: 20, sx: 1, sy: 1, xm: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20], ym: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20], xname: 'x [cm]', yname: 'y [cm]', r: 4 };
    function zustand(){ var U = wertR(fig, 's2-U'), x = wertR(fig, 's2-x'); return { U: U, x: x, y: U / 2 - x }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's2-U', Z.U + ' cm'); zeigeWert(fig, 's2-x', z(Z.x) + ' cm');
      var k = Achsen(svg, F2);
      k.strecke(0, Z.U / 2, Z.U / 2, 0, 'linie blau');
      k.punkt(0, Z.U / 2, 'pkt leer'); k.punkt(Z.U / 2, 0, 'pkt leer');   /* Ränder: x = 0 oder y = 0 ist kein Rechteck */
      var geht = Z.y > 0;
      if (geht) k.punkt(Z.x, Z.y, 'pkt gruen', '(' + z(Z.x) + ' | ' + z(Z.y) + ')', Z.x > 14 ? -8 : 8, Z.y > 15 ? 16 : -8, Z.x > 14 ? 'end' : 'start');
      while (bild.firstChild) bild.removeChild(bild.firstChild);
      bild.setAttribute('viewBox', '0 0 220 220');
      if (geht){
        var s = 190 / Math.max(Z.x, Z.y, 10), w = Z.x * s, h = Z.y * s;
        el(bild, 'rect', { x: 15, y: 205 - h, width: w, height: h, 'class': 'rechteck' });
        el(bild, 'text', { x: 15 + w / 2, y: 218, 'text-anchor': 'middle', 'class': 'p-text' }, 'x = ' + z(Z.x));
        el(bild, 'text', { x: 19 + w, y: 205 - h / 2, 'text-anchor': 'start', 'class': 'p-text' }, 'y = ' + z(Z.y));
      } else el(bild, 'text', { x: 110, y: 110, 'text-anchor': 'middle', 'class': 'p-text rot' }, 'kein Rechteck');
      formel.innerHTML = geht
        ? '2x + 2y = ' + Z.U + ' → y = ' + z(Z.U / 2) + ' − x = <b>' + z(Z.y) + '</b> <span class="grau">· Fläche ' + z(Z.x * Z.y) + ' cm²</span>'
        : '<span class="nein-text">x = ' + z(Z.x) + ' ist zu lang: y = ' + z(Z.U / 2) + ' − ' + z(Z.x) + ' = ' + z(Z.y) + ' ist keine Seitenlänge.</span>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, [
      { text: 'Umfang 20 cm. Wie lang muss \\(x\\) sein, damit \\(y = 7\\) cm ist?', ok: function(Z){ return Z.U === 20 && Z.x === 3; } },
      { text: 'Umfang 30 cm. Mach ein Quadrat.', ok: function(Z){ return Z.U === 30 && Z.x === 7.5; } },
      { text: 'Umfang 24 cm. Die Seite \\(y\\) soll doppelt so lang sein wie \\(x\\).', ok: function(Z){ return Z.U === 24 && Z.x === 4; } },
      { text: 'Ein Rechteck hat \\(x = 5\\) cm und \\(y = 9\\) cm. Welcher Umfang? Stell ihn ein, dazu \\(x = 5\\).', ok: function(Z){ return Z.U === 28 && Z.x === 5; } },
      { text: 'Umfang 16 cm. Welches \\(x\\) gibt \\(y = 1.5\\) cm?', ok: function(Z){ return Z.U === 16 && Z.x === 6.5; } }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 3 — Sinnvolle Werte: Definitionsbereich ════════
     Jede Aufgabe der Leiste bringt ihre Situation mit (Gleichung, Achsen mit Grösse und Einheit). Eingestellt werden
     der Bereich von … bis … und ob der Graph eine Strecke ist oder aus einzelnen Punkten besteht. */
  var SIT3 = [
    { text: 'Eine Kerze ist 30 cm hoch und brennt pro Stunde 2.5 cm ab. Zeichne den sinnvollen Teil des Graphen.',
      m: -2.5, b: 30, art: 'strecke', von: 0, bis: 12, F: { y1: 32, sy: 4, ym: [8, 16, 24, 32], xname: 'x [h]', yname: 'y [cm]' } },
    { text: 'Eine 10er-Karte fürs Kino: Nach \\(x\\) Besuchen sind noch \\(y = 10 - x\\) Eintritte übrig.',
      m: -1, b: 10, art: 'punkte', von: 0, bis: 10, F: { y1: 12, sy: 2, ym: [2, 4, 6, 8, 10, 12], xname: 'x [Besuche]', yname: 'y [Eintritte]' } },
    { text: 'Ein Tank enthält 120 l, eine Pumpe holt 8 l pro Minute heraus.',
      m: -8, b: 120, art: 'strecke', von: 0, bis: 15, F: { y1: 128, sy: 16, ym: [32, 64, 96, 128], xname: 'x [min]', yname: 'y [l]' } },
    { text: 'Du hast 18 Fr. für Glace, eine Kugel kostet 2 Fr. Nach \\(x\\) Kugeln bleiben \\(y = 18 - 2x\\) Franken.',
      m: -2, b: 18, art: 'punkte', von: 0, bis: 9, F: { y1: 20, sy: 2, ym: [4, 8, 12, 16, 20], xname: 'x [Kugeln]', yname: 'y [Fr.]' } },
    { text: 'Ein Regenfass enthält 20 l und fasst 80 l. Pro Minute kommen 4 l dazu, bis es voll ist: \\(y = 4x + 20\\).',
      m: 4, b: 20, art: 'strecke', von: 0, bis: 15, F: { y1: 96, sy: 16, ym: [16, 32, 48, 64, 80, 96], xname: 'x [min]', yname: 'y [l]' } }
  ];
  (function(){
    var fig = document.getElementById('sim3'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]'), wahl = fig.querySelector('#s3-art');
    var S = SIT3[0];
    function zustand(){ return { von: wertR(fig, 's3-von'), bis: wertR(fig, 's3-bis'), art: wahl.value }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's3-von', z(Z.von)); zeigeWert(fig, 's3-bis', z(Z.bis));
      var o = { w: 300, h: 220, rl: 30, x0: 0, x1: 20, y0: 0, sx: 1, xm: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20], r: 3.5 };
      for (var q in S.F) o[q] = S.F[q];
      var k = Achsen(svg, o), a = Math.min(Z.von, Z.bis), c = Math.max(Z.von, Z.bis), f = function(x){ return S.m * x + S.b; };
      k.gerade(S.m, S.b, 'linie grau gestrichelt');
      if (Z.art === 'strecke'){ k.strecke(a, f(a), c, f(c), 'linie blau'); k.punkt(a, f(a), 'pkt'); k.punkt(c, f(c), 'pkt'); }
      else for (var x = Math.ceil(a); x <= c + 1e-9; x++) k.punkt(x, f(x), 'pkt blau');
      var neg = f(c) < -1e-9, voll = S.m > 0 && f(c) > 80 + 1e-9;
      formel.innerHTML = linTxt(S.m, S.b) + ' &nbsp;·&nbsp; von x = ' + z(a) + ' bis x = ' + z(c) + ': y von ' + z(f(a)) + ' bis ' + z(f(c))
        + (neg ? ' <span class="nein-text">(negativ: Geht das?)</span>' : voll ? ' <span class="nein-text">(mehr als 80 l: Geht das?)</span>' : '');
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, SIT3.map(function(s){
      return { text: s.text + ' Stell den Bereich und die Darstellung ein.', setup: function(){ S = s; },
               ok: function(Z){ return Z.von === s.von && Z.bis === s.bis && Z.art === s.art; } };
    }), sim);
    fig.querySelectorAll('input, select').forEach(function(i){ i.addEventListener('input', zeichnen); i.addEventListener('change', zeichnen); });
    zeichnen();
  })();

  /* ════════ Sim 4 — Summe oder Produkt ════════
     x + y = S (linear fallend, Gerade) und x · y = P (antiproportional, Kurve) im selben Bild. Der Regler x zeigt
     auf beiden die Werte; die Zeile rechnet Summe und Produkt aus. */
  (function(){
    var fig = document.getElementById('sim4'); if (!fig) return;
    var svg = fig.querySelector('svg'), formel = fig.querySelector('[data-rolle="formel"]');
    var F4 = { w: 280, h: 280, rl: 22, x0: 0, x1: 20, y0: 0, y1: 20, sx: 1, sy: 1, xm: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20], ym: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20], r: 4 };
    function zustand(){ return { S: wertR(fig, 's4-S'), P: wertR(fig, 's4-P'), x: wertR(fig, 's4-x') }; }
    function zeichnen(){
      var Z = zustand(); zeigeWert(fig, 's4-S'); zeigeWert(fig, 's4-P'); zeigeWert(fig, 's4-x', z(Z.x));
      var k = Achsen(svg, F4), yl = Z.S - Z.x, ya = Z.P / Z.x;
      k.strecke(0, Z.S, Z.S, 0, 'linie blau');
      k.kurve(function(x){ return Z.P / x; }, Z.P / 20, 20, 'linie tinte');
      k.strecke(Z.x, 0, Z.x, 20, 'linie grau gestrichelt');
      if (yl >= 0) k.punkt(Z.x, yl, 'pkt blau');
      k.punkt(Z.x, ya, 'pkt');
      formel.innerHTML = '<span class="blau">Summe x + y = ' + Z.S + ': y = ' + (yl >= 0 ? z(yl) : '—') + '</span> &nbsp;·&nbsp; '
        + '<span>Produkt x · y = ' + Z.P + ': y = ' + z(ya) + (Math.abs(ya - Math.round(ya * 100) / 100) > 1e-9 ? ' (gerundet)' : '') + '</span>';
      if (pr) pr();
    }
    var pr = null, sim = { zustand: zustand, zeichnen: zeichnen };
    pr = Leiste(fig, [
      { text: 'Summe 12, Produkt 36. Wo treffen sich Gerade und Kurve? Zieh \\(x\\) dorthin.',
        ok: function(Z){ return Z.S === 12 && Z.P === 36 && Z.x === 6; } },
      { text: 'Summe 10, Produkt 24. Finde eine Stelle, an der beide dasselbe \\(y\\) haben.',
        ok: function(Z){ return Z.S === 10 && Z.P === 24 && (Z.x === 4 || Z.x === 6); } },
      { text: 'Produkt 24: Bei \\(x = 3\\) ist \\(y = 8\\). Wo ist \\(y\\) auf der Kurve halb so gross?',
        ok: function(Z){ return Z.P === 24 && Z.x === 6; } },
      { text: 'Summe 12: Bei \\(x = 2\\) ist \\(y = 10\\). Wo ist \\(y\\) auf der Geraden halb so gross? Vergleiche mit der Aufgabe davor.',
        ok: function(Z){ return Z.S === 12 && Z.x === 7; } },
      { text: 'Summe 9, Produkt 20. Wo treffen sich die beiden?',
        ok: function(Z){ return Z.S === 9 && Z.P === 20 && (Z.x === 4 || Z.x === 5); } }
    ], sim);
    fig.querySelectorAll('input').forEach(function(i){ i.addEventListener('input', zeichnen); });
    zeichnen();
  })();

  /* ---------- Minibilder: <svg class="mini-gerade" data-geraden="m,b;m,b" data-punkte="x,y;x,y"> ---------- */
  function miniBild(svg, geraden, punkte){
    var d = svg.dataset, sach = !!d.fenster;
    var o = { w: 180, h: 180, rl: 14, x0: -6, x1: 6, y0: -6, y1: 6, xm: [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], ym: [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], r: 3.5 };   /* jede ganze Zahl beschriftet */
    if (sach){ var f = d.fenster.split(',').map(Number), ganz = function(a, b){ var l = []; for (var i = Math.max(1, a); i <= b; i++) l.push(i); return l; };
      o.x0 = f[0]; o.x1 = f[1]; o.y0 = f[2]; o.y1 = f[3]; o.xm = ganz(f[0], f[1]); o.ym = ganz(f[2], f[3]); o.xname = d.xname; o.yname = d.yname; }
    var k = Achsen(svg, o);
    geraden.forEach(function(g, i){ k.gerade(g[0], g[1], 'linie ' + (i ? 'orange' : 'blau'), sach ? 0 : null); });   /* Sachgraph: erst ab x = 0 */
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
     Zahlenfelder exakt als Bruch (2/3, −1.5, 4). Feld w: Auswahl (select). Fehlversuch → gezielte Diagnose oder
     die Probe. Tipps in drei Stufen. Testhaken: box.__aufgabe, box.__typ. */
  (function(){
    var ALLE = document.querySelectorAll('.uebung[data-typ]'); if (!ALLE.length) return;
    function lnSchl(m, b){ return 'ln|' + m[0] + '/' + m[1] + '|' + b[0] + '/' + b[1]; }
    function tab(xs, ys){ return '\\[\\begin{array}{c|' + xs.map(function(){ return 'c'; }).join('') + '} x & ' + xs.join(' & ') + ' \\\\ \\hline y & ' + ys.join(' & ') + ' \\end{array}\\]'; }
    function mischen(l){ var a = l.slice(); for (var i = a.length - 1; i > 0; i--){ var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    function zt(a){ return bWertTex(a); }
    function kl(v){ return v < 0 ? '(' + v + ')' : String(v); }

    /* Feste Aufgaben (Clips, Festhalten, Erkundungen, Kapitelaufgaben, Gesamttest): nie als Zufallsübung. */
    var SPERRE = [
      'ln|6/1|40/1', 'ln|-3/1|30/1', 'ln|4/1|10/1', 'ln|7/1|14/1', 'ln|-5/1|45/1', 'ln|4/1|15/1', 'ln|-5/1|200/1', 'ln|1/1|2/1', 'ln|3/1|3/1',
      'ln|5/2|6/1', 'ln|-1/1|12/1', 'ln|-3/2|15/1', 'ln|-3/1|21/1', 'ln|-2/1|8/1', 'ln|-2/1|30/1', 'ln|-1/1|20/1', 'ln|-3/2|12/1', 'ln|2/1|5/1',
      'ln|3/1|7/1', 'ln|-2/1|12/1', 'ln|1/2|3/1', 'ln|-1/1|15/1', 'ln|-2/1|10/1', 'ln|-1/1|7/1', 'ln|-2/1|40/1', 'ln|3/10|3/2', 'ln|4/1|5/1',
      'ln|-1/1|18/1', 'ln|-3/2|15/2', 'ln|15/1|40/1', 'ln|-5/1|30/1', 'ln|-3/1|21/1', 'ln|3/1|6/1', 'ln|-1/1|10/1',
      'um|R|24', 'um|R|30', 'um|R|36', 'um|R|20', 'um|R|40', 'um|D|30', 'um|Z|40', 'ge|16', 'ge|20', 'ge|24',
      'be|0|30|2.5|0', 'be|0|18|3|0', 'be|0|20|2.5|0', 'be|1|60|4|0', 'be|1|120|8|0', 'be|1|60|4|0', 'be|4|160|15|40', 'be|4|80|4|20',
      'sk|170|9', 'sk|450|9', 'sk|70|8', 'sk|180|9',
      'ar|18,9,6,3', 'ar|16,8,4,2', 'ar|20,10,5,4', 'ar|18,15,9,6', 'ar|2,4,8,10', 'ar|30,15,10,5', 'ar|25,20,15,0', 'ar|12,9,6,3',
      'de|3|4|15|P', 'de|3|4|15|M', 'de|3|4|15|B', 'ge|28', 'ge|30'
    ];
    function gesperrt(T, A){ return !!T.schl && SPERRE.indexOf(T.schl(A)) >= 0; }

    /* Situationen zum Deuten: x und y mit Einheit, Sätze für Punkt, Steigung und Anfangswert. */
    var DEUT = [
      { t: function(m, b){ return 'Ein Taxi kostet \\(y = ' + zt(m) + 'x + ' + b + '\\) Franken für eine Fahrt über \\(x\\) Kilometer.'; }, fallend: false,
        P: function(x, y){ return 'Eine Fahrt über ' + x + ' km kostet ' + y + ' Fr.'; }, Pv: function(x, y){ return 'Eine Fahrt über ' + y + ' km kostet ' + x + ' Fr.'; },
        Pe: function(x, y){ return 'Jeder Kilometer kostet ' + y + ' Fr.'; },
        M: function(m){ return 'Jeder weitere Kilometer kostet ' + m + ' Fr.'; }, Mg: function(m){ return 'Die ganze Fahrt kostet ' + m + ' Fr.'; },
        Mb: function(m){ return 'Beim Einsteigen bezahlt man ' + m + ' Fr.'; },
        Bk: function(b){ return 'Beim Einsteigen, noch vor dem ersten Kilometer, bezahlt man ' + b + ' Fr.'; }, Bm: function(b){ return 'Jeder Kilometer kostet ' + b + ' Fr.'; },
        Bx: function(b){ return 'Nach ' + b + ' km ist die Fahrt gratis.'; } },
      { t: function(m, b){ return 'Ein Pool wird gefüllt: Nach \\(x\\) Stunden steht das Wasser \\(y = ' + zt(m) + 'x + ' + b + '\\) cm hoch.'; }, fallend: false,
        P: function(x, y){ return 'Nach ' + x + ' Stunden steht das Wasser ' + y + ' cm hoch.'; }, Pv: function(x, y){ return 'Nach ' + y + ' Stunden steht das Wasser ' + x + ' cm hoch.'; },
        Pe: function(x, y){ return 'Pro Stunde steigt das Wasser um ' + y + ' cm.'; },
        M: function(m){ return 'Pro Stunde steigt das Wasser um ' + m + ' cm.'; }, Mg: function(m){ return 'Am Ende steht das Wasser ' + m + ' cm hoch.'; },
        Mb: function(m){ return 'Am Anfang steht das Wasser ' + m + ' cm hoch.'; },
        Bk: function(b){ return 'Am Anfang, bevor gefüllt wird, steht das Wasser schon ' + b + ' cm hoch.'; }, Bm: function(b){ return 'Pro Stunde steigt das Wasser um ' + b + ' cm.'; },
        Bx: function(b){ return 'Nach ' + b + ' Stunden ist der Pool voll.'; } },
      { t: function(m, b){ return 'Eine Kerze ist nach \\(x\\) Stunden noch \\(y = -' + zt(m) + 'x + ' + b + '\\) cm hoch.'; }, fallend: true,
        P: function(x, y){ return 'Nach ' + x + ' Stunden ist die Kerze noch ' + y + ' cm hoch.'; }, Pv: function(x, y){ return 'Nach ' + y + ' Stunden ist die Kerze noch ' + x + ' cm hoch.'; },
        Pe: function(x, y){ return 'Pro Stunde wird die Kerze ' + y + ' cm kürzer.'; },
        M: function(m){ return 'Pro Stunde wird die Kerze ' + m + ' cm kürzer.'; }, Mg: function(m){ return 'Am Schluss ist die Kerze noch ' + m + ' cm hoch.'; },
        Mb: function(m){ return 'Am Anfang ist die Kerze ' + m + ' cm hoch.'; },
        Bk: function(b){ return 'Vor dem Anzünden ist die Kerze ' + b + ' cm hoch.'; }, Bm: function(b){ return 'Pro Stunde wird die Kerze ' + b + ' cm kürzer.'; },
        Bx: function(b){ return 'Die Kerze brennt ' + b + ' Stunden lang.'; } },
      { t: function(m, b){ return 'Ein Handy-Abo kostet im Monat \\(y = ' + zt(m) + 'x + ' + b + '\\) Franken, wenn man \\(x\\) GB Daten braucht.'; }, fallend: false,
        P: function(x, y){ return 'Mit ' + x + ' GB kostet der Monat ' + y + ' Fr.'; }, Pv: function(x, y){ return 'Mit ' + y + ' GB kostet der Monat ' + x + ' Fr.'; },
        Pe: function(x, y){ return 'Jedes GB kostet ' + y + ' Fr.'; },
        M: function(m){ return 'Jedes weitere GB kostet ' + m + ' Fr.'; }, Mg: function(m){ return 'Der ganze Monat kostet ' + m + ' Fr.'; },
        Mb: function(m){ return 'Die Grundgebühr beträgt ' + m + ' Fr.'; },
        Bk: function(b){ return 'Auch ohne Daten (0 GB) kostet der Monat ' + b + ' Fr.'; }, Bm: function(b){ return 'Jedes GB kostet ' + b + ' Fr.'; },
        Bx: function(b){ return 'Ab ' + b + ' GB ist das Abo gratis.'; } }
    ];

    var TYPEN = {
      /* ── Kapitel 1 ── */
      'tabelle': { felder: ['m', 'b'],
        schl: function(A){ return lnSchl(B(A.m), B(A.b)); },
        eingabe: function(A){ return { m: String(A.m), b: String(A.b) }; },
        neu: function(){
          var m = nz(-9, 9), b = zufallG(-10, 40), x0 = zufall([0, 1, 2, 3, 4]), d = zufall([1, 2, 2, 3, 5]);
          if (x0 === 0 && d === 1) return TYPEN.tabelle.neu();
          var xs = [x0, x0 + d, x0 + 2 * d], ys = xs.map(function(x){ return m * x + b; });
          return { m: m, b: b, xs: xs, ys: ys, d: d, text: 'Die Tabelle gehört zu einer Geraden \\(y = m \\cdot x + b\\). Bestimme \\(m\\) und \\(b\\).' + tab(xs, ys),
                   muster: '\\(m = \\) {m} &nbsp; \\(b = \\) {b}' }; },
        richtig: function(A, e){ return bEq(e.m, B(A.m)) && bEq(e.b, B(A.b)); },
        fehler: function(A){ var f = [];
          if (A.d > 1) f.push([{ m: String(A.m * A.d), b: String(A.b) }, 'springt']);
          if (A.xs[0] !== 0 && A.ys[0] !== A.b) f.push([{ m: String(A.m), b: String(A.ys[0]) }, 'x = 0']);
          return f; },
        pruefen: function(A, e){
          var t = [];
          if (!bEq(e.m, B(A.m))) t.push(A.d > 1 && bEq(e.m, B(A.m * A.d)) ? 'Die Tabelle springt um \\(\\Delta x = ' + A.d + '\\), nicht um 1: \\(m = \\dfrac{\\Delta y}{\\Delta x}\\).'
                                                                         : '\\(m = \\dfrac{\\Delta y}{\\Delta x}\\): Um wie viel ändert sich \\(y\\), und um wie viel \\(x\\)?');
          if (!bEq(e.b, B(A.b))) t.push(A.xs[0] !== 0 && bEq(e.b, B(A.ys[0])) ? '\\(b\\) ist der Wert bei \\(x = 0\\). Die Tabelle beginnt aber bei \\(x = ' + A.xs[0] + '\\): Rechne zurück bis \\(x = 0\\).'
                                                                              : 'Setz ein Wertepaar ein: \\(' + A.ys[0] + ' = m \\cdot ' + kl(A.xs[0]) + ' + b\\).');
          return t.join(' '); },
        tipps: function(A){ return ['Zuerst \\(m\\): Wie viel ändert sich \\(y\\) von Spalte zu Spalte, und wie viel \\(x\\)?',
          '\\(m = \\dfrac{' + (A.ys[1] - A.ys[0]) + '}{' + A.d + '}\\). ' + (A.xs[0] ? 'Dann von \\(x = ' + A.xs[0] + '\\) zurück bis \\(x = 0\\).' : 'Und \\(b\\) steht schon in der Tabelle, bei \\(x = 0\\).')]; },
        loesung: function(A){ return 'm = \\dfrac{' + (A.ys[1] - A.ys[0]) + '}{' + A.d + '} = ' + A.m + ', \\quad b = ' + A.ys[0] + ' - ' + kl(A.m) + ' \\cdot ' + A.xs[0] + ' = ' + A.b; } },

      'deuten': { felder: ['w'],
        schl: function(A){ return 'de|' + A.k + '|' + A.m + '|' + A.b + '|' + A.art; },
        eingabe: function(A){ return { w: 'r' }; },
        neu: function(){
          var k = zufallG(0, DEUT.length - 1), D = DEUT[k], m = zufall([2, 3, 4, 5, 6]), b = zufall([8, 10, 12, 15, 20, 24, 30]), art = zufall(['P', 'M', 'B']);
          if (D.fallend && m * 6 > b) return TYPEN.deuten.neu();
          var x = zufallG(2, D.fallend ? Math.floor((b - 1) / m) : 9), y = (D.fallend ? -m : m) * x + b, frage, o;
          if (m === b || x === y || y === m || y === b) return TYPEN.deuten.neu();
          if (art === 'P'){ frage = 'Was bedeutet der Punkt \\((' + x + ' \\mid ' + y + ')\\)?'; o = [['r', D.P(x, y)], ['v', D.Pv(x, y)], ['e', D.Pe(x, y)]]; }
          else if (art === 'M'){ frage = 'Was bedeutet die Zahl \\(' + (D.fallend ? '-' : '') + m + '\\) in der Gleichung?'; o = [['r', D.M(m)], ['g', D.Mg(m)], ['a', D.Mb(m)]]; }
          else { frage = 'Was bedeutet die Zahl \\(' + b + '\\) in der Gleichung?'; o = [['r', D.Bk(b)], ['s', D.Bm(b)], ['x', D.Bx(b)]]; }
          return { k: k, m: m, b: b, x: x, y: y, art: art, optionen: mischen(o), text: D.t(B(m), b) + ' ' + frage, muster: '{w}' }; },
        richtig: function(A, e){ return e.w === 'r'; },
        fehler: function(A){ return A.optionen.filter(function(o){ return o[0] !== 'r'; }).map(function(o){
          return [{ w: o[0] }, { v: 'vertauscht', e: 'ganz', g: 'pro', a: 'Anfang', s: 'Anfang', x: 'Anfang' }[o[0]]]; }); },
        pruefen: function(A, e){
          return {
            v: '\\(x\\) und \\(y\\) <b>vertauscht</b>: Im Punkt steht zuerst \\(x = ' + A.x + '\\), dann \\(y = ' + A.y + '\\).',
            e: 'Ein Punkt sagt, wie viel es <b>ganz</b> ist, nicht wie viel pro Einheit dazukommt.',
            g: '\\(m\\) steht vor dem \\(x\\): Es ist die Änderung <b>pro</b> Einheit, nicht das Ganze.',
            a: '\\(m\\) steht vor dem \\(x\\). Was am <b>Anfang</b> ist, sagt \\(b\\).',
            s: 'Die Zahl ohne \\(x\\) ist \\(b\\), der Wert am <b>Anfang</b> bei \\(x = 0\\).',
            x: 'Setz \\(x = 0\\) ein: Dann bleibt \\(y = ' + A.b + '\\). Das ist der Wert am <b>Anfang</b>.'
          }[e.w] || 'Wähle eine der Aussagen.'; },
        tipps: function(A){ return [A.art === 'P' ? 'Im Punkt \\((x \\mid y)\\) steht zuerst \\(x\\), dann \\(y\\). Was ist hier \\(x\\), was \\(y\\)?'
          : 'In \\(y = m \\cdot x + b\\): \\(m\\) ist die Änderung pro Einheit von \\(x\\), \\(b\\) der Wert bei \\(x = 0\\).',
          A.art === 'P' ? 'Setz \\(x = ' + A.x + '\\) ein: Es kommt \\(y = ' + A.y + '\\) heraus, das Ganze bei diesem \\(x\\).' : 'Steht die Zahl vor dem \\(x\\) oder allein?']; },
        loesung: function(A){ var D = DEUT[A.k]; return '\\text{' + (A.art === 'P' ? D.P(A.x, A.y) : A.art === 'M' ? D.M(A.m) : D.Bk(A.b)) + '}'; } },

      /* ── Kapitel 2 ── */
      'aufloesen': { felder: ['m', 'b'],
        schl: function(A){ return lnSchl(A.mm, B(A.b)); },
        eingabe: function(A){ return { m: bTxt(A.mm).replace('−', '-'), b: String(A.b) }; },
        neu: function(){
          var a = zufallG(1, 6), c = zufall([1, 2, 2, 3, 4, 5]), b = zufallG(2, 12), halb = c % 2 === 0 && Math.random() < 0.35;   /* auch b = 7.5 (Gesamttest G4) */
          if (a === c && c === 1) return TYPEN.aufloesen.neu();
          var S = c * b + (halb ? c / 2 : 0); b = S / c;
          return { a: a, c: c, S: S, b: b, mm: B(-a, c),
                   text: 'Löse nach \\(y\\) auf: \\(' + (a === 1 ? '' : a) + 'x + ' + (c === 1 ? '' : c) + 'y = ' + (c * b) + '\\). Schreib als \\(y = m \\cdot x + b\\).',
                   muster: '\\(m = \\) {m} &nbsp; \\(b = \\) {b}' }; },
        richtig: function(A, e){ return bEq(e.m, A.mm) && bEq(e.b, B(A.b)); },
        fehler: function(A){ var f = [[{ m: bTxt(B(A.a, A.c)).replace('−', '-'), b: String(A.b) }, 'Vorzeichen']];
          if (A.c > 1) f.push([{ m: String(-A.a), b: String(A.S) }, 'durch ' + A.c]); return f; },
        pruefen: function(A, e){
          if (A.c > 1 && bEq(e.b, B(A.S))) return 'Nach \\(' + A.c + 'y = \\dots\\) teilst du <b>durch ' + A.c + '</b>, und zwar beide Glieder rechts.';
          if (bEq(e.m, B(A.a, A.c))) return '<b>Vorzeichen</b>: \\(' + (A.a === 1 ? '' : A.a) + 'x\\) wechselt die Seite, also \\(-' + (A.a === 1 ? '' : A.a) + 'x\\).';
          var xp = [2, 3, 1, 4].filter(function(x){ return !bEq(bAdd(bMul(e.m, B(x)), e.b), B(A.S - x * A.a, A.c)); })[0] || 2;
          var p = bAdd(bMul(e.m, B(xp)), e.b), soll = B(A.S - xp * A.a, A.c);
          return 'Probe mit \\(x = ' + xp + '\\): Aus der Gleichung folgt \\(y = ' + zt(soll) + '\\), deine Gerade gibt \\(' + zt(p) + '\\). Zuerst \\(-' + (A.a === 1 ? '' : A.a) + 'x\\) auf beiden Seiten' + (A.c > 1 ? ', dann durch \\(' + A.c + '\\).' : '.'); },
        tipps: function(A){ return ['Bring \\(' + (A.a === 1 ? '' : A.a) + 'x\\) auf die rechte Seite' + (A.c > 1 ? ', dann teile durch \\(' + A.c + '\\).' : '.'),
          '\\(' + (A.c === 1 ? '' : A.c) + 'y = ' + A.S + ' - ' + (A.a === 1 ? '' : A.a) + 'x\\)']; },
        loesung: function(A){ return (A.c === 1 ? '' : A.c) + 'y = ' + A.S + ' - ' + (A.a === 1 ? '' : A.a) + 'x' + (A.c > 1 ? ' \\;\\Rightarrow\\; y = ' + A.b + ' - ' + zt(B(A.a, A.c)) + 'x' : '') + ', \\quad m = ' + zt(A.mm) + ', \\; b = ' + A.b; } },

      'umfang': { felder: ['y', 'm'],
        schl: function(A){ return 'um|' + A.k + '|' + A.U; },
        eingabe: function(A){ return { y: String(A.y), m: String(A.m) }; },
        neu: function(){
          var k = zufall(['R', 'R', 'D', 'Z']), U, x, y, m, text;
          if (k === 'R'){ U = 2 * zufallG(6, 30); x = zufallG(1, U / 2 - 1); y = U / 2 - x; m = -1;
            text = 'Ein Rechteck hat den Umfang \\(' + U + '\\) cm. Die eine Seite ist \\(x\\), die andere \\(y\\). Wie lang ist \\(y\\) für \\(x = ' + x + '\\) cm? Und welche Steigung hat \\(y\\) in Abhängigkeit von \\(x\\)?'; }
          else if (k === 'D'){ U = zufallG(20, 60); x = zufallG(Math.floor(U / 4) + 1, Math.ceil(U / 2) - 1); y = U - 2 * x; m = -2;
            if (y <= 0 || y >= 2 * x) return TYPEN.umfang.neu();
            text = 'Ein gleichschenkliges Dreieck hat den Umfang \\(' + U + '\\) cm, zwei Seiten (Schenkel) sind je \\(x\\) lang, die Basis \\(y\\). Wie lang ist \\(y\\) für \\(x = ' + x + '\\) cm? Welche Steigung hat \\(y\\) in Abhängigkeit von \\(x\\)?'; }
          else { U = 2 * zufallG(10, 40); x = zufallG(2, U / 2 - 1); y = U - 2 * x; m = -2;
            text = 'Mit \\(' + U + '\\) m Zaun wird an einer Hausmauer ein Rechteck abgesteckt: zwei Seiten \\(x\\), eine Seite \\(y\\), die Mauer braucht keinen Zaun. Wie lang ist \\(y\\) für \\(x = ' + x + '\\) m? Welche Steigung hat \\(y\\) in Abhängigkeit von \\(x\\)?'; }
          if (y === x || (k !== 'R' && 3 * x === U)) return TYPEN.umfang.neu();
          return { k: k, U: U, x: x, y: y, m: m, text: text, muster: '\\(y = \\) {y} &nbsp; \\(m = \\) {m}' }; },
        richtig: function(A, e){ return bEq(e.y, B(A.y)) && bEq(e.m, B(A.m)); },
        fehler: function(A){ var f = [[{ y: String(A.y), m: String(-A.m) }, 'Vorzeichen']];
          if (A.k === 'R') f.push([{ y: String(A.U - A.x), m: String(A.m) }, 'zweimal']);
          else f.push([{ y: String((A.U - A.x) / 2), m: String(A.m) }, 'zweimal']);
          return f; },
        pruefen: function(A, e){
          var t = [];
          if (!bEq(e.y, B(A.y))){
            if (A.k === 'R' && bEq(e.y, B(A.U - A.x))) t.push('Im Umfang kommt jede Seite <b>zweimal</b> vor: \\(2x + 2y = ' + A.U + '\\), also \\(x + y = ' + A.U / 2 + '\\).');
            else if (A.k !== 'R' && bEq(e.y, B(A.U - A.x, 2))) t.push('Hier kommt \\(x\\) <b>zweimal</b> vor, \\(y\\) nur einmal: \\(2x + y = ' + A.U + '\\).');
            else t.push('Schreib den Umfang als Gleichung mit \\(x\\) und \\(y\\) und setz \\(x = ' + A.x + '\\) ein.');
          }
          if (!bEq(e.m, B(A.m))) t.push(bEq(e.m, B(-A.m)) ? '<b>Vorzeichen</b>: Wird \\(x\\) länger, bleibt für \\(y\\) weniger, \\(m\\) ist negativ.' : 'Um wie viel ändert sich \\(y\\), wenn \\(x\\) um 1 länger wird?');
          return t.join(' '); },
        tipps: function(A){ return [A.k === 'R' ? 'Umfang: \\(2x + 2y = ' + A.U + '\\). Teile zuerst durch 2.' : 'Umfang: \\(2x + y = ' + A.U + '\\).',
          A.k === 'R' ? '\\(y = ' + A.U / 2 + ' - x\\)' : '\\(y = ' + A.U + ' - 2x\\)']; },
        loesung: function(A){ return (A.k === 'R' ? 'y = ' + A.U / 2 + ' - x = ' + A.U / 2 + ' - ' + A.x : 'y = ' + A.U + ' - 2x = ' + A.U + ' - ' + 2 * A.x) + ' = ' + A.y + ', \\quad m = ' + A.m; } },

      /* ── Kapitel 3 ── */
      'bereich': { felder: ['von', 'bis'],
        schl: function(A){ return 'be|' + A.k + '|' + A.L + '|' + A.r + '|' + A.a; },
        eingabe: function(A){ return { von: '0', bis: bWert(A.ende).replace('−', '-') }; },
        neu: function(){
          /* fallend bis 0 (Kerze, Tank, Akku, Geld) oder steigend bis voll (Becken): Der Bereich endet, wo die Situation aufhört. */
          var k = zufallG(0, 4), r, L, a = 0, text;
          if (k === 0){ r = zufall([1.5, 2, 2.5, 3]); L = r * zufall([4, 6, 8, 10, 12]); text = 'Eine Kerze ist ' + L + ' cm hoch und wird pro Stunde ' + r + ' cm kürzer: \\(y = ' + L + ' - ' + r + 'x\\) (\\(x\\) in Stunden).'; }
          else if (k === 1){ r = zufall([4, 5, 6, 10]); L = r * zufall([10, 12, 20, 25]); text = 'Ein Tank enthält ' + L + ' l, pro Minute fliessen ' + r + ' l ab: \\(y = ' + L + ' - ' + r + 'x\\) (\\(x\\) in Minuten).'; }
          else if (k === 2){ r = zufall([5, 10, 20]); L = 100; text = 'Ein Akku zeigt 100 % und verliert pro Stunde ' + r + ' Prozentpunkte: \\(y = 100 - ' + r + 'x\\) (\\(x\\) in Stunden).'; }
          else if (k === 3){ r = zufall([2, 3, 4, 5]); L = r * zufall([6, 7, 8, 9, 10]); text = 'Du hast ' + L + ' Fr., ein Heft kostet ' + r + ' Fr. Nach \\(x\\) Heften bleiben \\(y = ' + L + ' - ' + r + 'x\\) Franken.'; }
          else { r = zufall([5, 10, 15, 20]); a = zufall([10, 20, 30, 40]); L = a + r * zufall([4, 5, 6, 8, 10]);
            text = 'In einem Becken stehen ' + a + ' cm Wasser. Pro Stunde steigt es um ' + r + ' cm, bis das Becken mit ' + L + ' cm voll ist: \\(y = ' + r + 'x + ' + a + '\\).'; }
          var ende = bDiv(bSub(bDez(L), B(a)), bDez(r));
          return { k: k, r: r, L: L, a: a, ende: ende, text: text + ' Welche Werte von \\(x\\) sind sinnvoll?', muster: 'von \\(x = \\) {von} &nbsp; bis \\(x = \\) {bis}' }; },
        richtig: function(A, e){ return bEq(e.von, B(0)) && bEq(e.bis, A.ende); },
        fehler: function(A){ var f = [[{ von: '-1', bis: bWert(A.ende).replace('−', '-') }, 'Anfang']];
          if (A.k === 4) f.push([{ von: '0', bis: bWert(bDiv(bDez(A.L), bDez(A.r))).replace('−', '-') }, 'schon']);
          else f.push([{ von: '0', bis: String(A.L) }, 'teilen'], [{ von: '0', bis: bWert(bMul(bDez(A.L), bDez(A.r))).replace('−', '-') }, 'teilen']);
          return f; },
        pruefen: function(A, e){
          var t = [];
          if (!bEq(e.von, B(0))) t.push(bZahl(e.von) < 0 ? 'Vor dem <b>Anfang</b> gibt es nichts: Der Bereich beginnt bei \\(x = 0\\).' : 'Schon bei \\(x = 0\\) ist die Situation sinnvoll: Das ist der <b>Anfang</b>.');
          if (!bEq(e.bis, A.ende)){
            if (A.k === 4) t.push(bEq(e.bis, bDiv(bDez(A.L), bDez(A.r))) ? 'Es steht <b>schon</b> Wasser im Becken: Bis voll fehlen nur \\(' + A.L + ' - ' + A.a + '\\) cm.' : 'Wann ist das Becken voll? Setz \\(y = ' + A.L + '\\) und löse nach \\(x\\) auf.');
            else t.push(bEq(e.bis, bDez(A.L)) || bEq(e.bis, bMul(bDez(A.L), bDez(A.r))) ? 'Bis \\(y = 0\\): \\(' + A.L + ' - ' + A.r + 'x = 0\\). Dazu <b>teilen</b>: \\(x = ' + A.L + ' : ' + A.r + '\\).'
              : 'Wann ist nichts mehr übrig? Setz \\(y = 0\\) und löse nach \\(x\\) auf.');
          }
          return t.join(' '); },
        tipps: function(A){ return ['Der Bereich beginnt beim Anfang \\(x = 0\\) und endet dort, wo die Situation aufhört: ' + (A.k === 4 ? 'wenn das Becken voll ist.' : 'wenn nichts mehr übrig ist.'),
          A.k === 4 ? '\\(' + A.r + 'x + ' + A.a + ' = ' + A.L + '\\)' : '\\(' + A.L + ' - ' + A.r + 'x = 0\\)']; },
        loesung: function(A){ return '0 \\le x \\le ' + (A.k === 4 ? '(' + A.L + ' - ' + A.a + ') : ' + A.r : A.L + ' : ' + A.r) + ' = ' + bWertTex(A.ende) + (A.k === 3 ? '\\text{, nur ganze Zahlen}' : ''); } },

      'skala': { felder: ['k'],
        schl: function(A){ return 'sk|' + A.M + '|' + A.n; },
        eingabe: function(A){ return { k: String(A.k) }; },
        neu: function(){
          var BEQ = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500], n = zufallG(5, 10), i = zufallG(2, BEQ.length - 1), k = BEQ[i], vor = BEQ[i - 1];
          var M = zufallG(vor * n + 1, k * n); M = Math.ceil(M / (k >= 10 ? 5 : 1)) * (k >= 10 ? 5 : 1);
          if (M <= vor * n || M > k * n || M % n === 0 && BEQ.indexOf(M / n) >= 0 && M / n !== k) return TYPEN.skala.neu();
          return { M: M, n: n, k: k, vor: vor, text: 'Die \\(y\\)-Werte gehen von 0 bis ' + M + '. Auf der \\(y\\)-Achse hast du ' + n + ' Häuschen. Wie viel soll ein Häuschen bedeuten? Wähle eine bequeme Zahl (1, 2, 5, 10, 20, 25, 50, 100, …), die gerade reicht.',
                   muster: '1 Häuschen \\(=\\) {k}' }; },
        richtig: function(A, e){ return bEq(e.k, B(A.k)); },
        fehler: function(A){ var f = [[{ k: String(A.vor) }, 'reicht']]; var q = B(A.M, A.n); if (!bEq(q, B(A.k))) f.push([{ k: bWert(q).replace('−', '-') }, 'bequem']); f.push([{ k: String(A.M) }, 'Häuschen']); return f; },
        pruefen: function(A, e){
          var w = bZahl(e.k);
          if (bZahl(bSub(bMul(e.k, B(A.n)), B(A.M))) < 0) return 'Das <b>reicht</b> nicht: ' + A.n + ' Häuschen zu ' + bWert(e.k) + ' gehen nur bis ' + z(w * A.n) + '.';
          if (w * A.n >= A.M * 4) return 'Ein ' + A.n + '-Häuschen-Bild reicht dann bis ' + z(w * A.n) + ': Die Werte füllen nur einen kleinen Teil. Ein <b>Häuschen</b> soll weniger bedeuten.';
          if ([1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500].indexOf(w) < 0) return 'Das reicht, ist aber keine <b>bequeme</b> Zahl zum Ablesen. Runde auf die nächste bequeme Zahl auf.';
          return 'Das geht, aber eine kleinere bequeme Zahl reicht auch, und das Bild wird grösser.'; },
        tipps: function(A){ return ['Teile den grössten Wert durch die Anzahl Häuschen.', A.M + ' : ' + A.n + (A.M % A.n ? ' ≈ ' : ' = ') + z(A.M / A.n) + '. Runde auf eine bequeme Zahl auf.']; },
        loesung: function(A){ return A.M + ' : ' + A.n + ' = ' + bWertTex(B(A.M, A.n)) + ' \\;\\Rightarrow\\; ' + A.k; } },

      /* ── Kapitel 4 ── */
      'art': { felder: ['w'],
        schl: function(A){ return 'ar|' + A.ys.join(','); },
        eingabe: function(A){ return { w: A.art }; },
        neu: function(){
          var art = zufall(['steigend', 'fallend', 'prop', 'anti', 'anti', 'keines']), xs, ys, P;
          /* Die x-Schritte verraten nichts: gleich oder ungleich bei jeder Art (Prüfung 10.10.2026) */
          if (art === 'anti'){ P = zufall([12, 18, 20, 24, 30, 36, 48, 60, 120]); var t = []; for (var d = 1; d <= P; d++) if (P % d === 0) t.push(d);
            var reihen = [1, 2, 3].map(function(x0){ return [x0, x0 + 1, x0 + 2, x0 + 3]; }).filter(function(r){ return r.every(function(x){ return P % x === 0; }); });
            xs = reihen.length && Math.random() < 0.5 ? zufall(reihen) : mischen(t).slice(0, 4).sort(function(a, b){ return a - b; }); ys = xs.map(function(x){ return P / x; }); }
          else { var s = zufall([1, 2]), x0 = zufallG(0, 2); xs = [0, 1, 2, 3].map(function(i){ return x0 + s * i; });
            if (art !== 'keines' && Math.random() < 0.5) xs = mischen([0, 1, 2, 3, 4, 5, 6, 7, 8]).slice(0, 4).sort(function(a, b){ return a - b; });
            var k = zufallG(2, 6), c = zufallG(3, 20);
            ys = xs.map(function(x){ return art === 'steigend' ? k * x + c : art === 'fallend' ? 6 * k + 20 - k * x : art === 'prop' ? k * x : x * x + c; });
            if (art === 'prop' && xs[0] === 0) return TYPEN.art.neu(); }
          return { art: art, xs: xs, ys: ys, text: 'Welcher Zusammenhang passt zur Tabelle?' + tab(xs, ys), muster: '{w}',
                   optionen: [['steigend', 'linear steigend, nicht proportional'], ['fallend', 'linear fallend'], ['prop', 'proportional'], ['anti', 'antiproportional'], ['keines', 'keines davon']] }; },
        richtig: function(A, e){ return e.w === A.art; },
        fehler: function(A){ return { anti: [[{ w: 'fallend' }, 'Differenzen']], fallend: [[{ w: 'anti' }, 'Produkt']], prop: [[{ w: 'steigend' }, 'Quotient']],
                                      steigend: [[{ w: 'prop' }, 'Quotient']], keines: [[{ w: 'steigend' }, 'Differenzen']] }[A.art]; },
        pruefen: function(A, e){
          var q = A.ys.slice(1).map(function(v, i){ return bWert(B(v - A.ys[i], A.xs[i + 1] - A.xs[i])); }), p = A.xs.map(function(x, i){ return mz(x * A.ys[i]); });
          var info = ' Die <b>Differenzen</b> \\(\\Delta y : \\Delta x\\) von Spalte zu Spalte: ' + q.join(', ') + '. Die <b>Produkte</b> \\(x \\cdot y\\): ' + p.join(', ') + '.';
          if ((e.w === 'fallend' && A.art === 'steigend') || (e.w === 'steigend' && A.art === 'fallend')) return 'Linear stimmt, aber die Richtung nicht: Die <b>Differenzen</b> sind ' + (A.art === 'steigend' ? 'positiv, \\(y\\) wächst.' : 'negativ, \\(y\\) fällt.') + info;
          if (e.w === 'keines' && A.art === 'prop') return 'Rechne den <b>Quotienten</b> \\(y : x\\): Er bleibt gleich.' + info;
          if (e.w === 'anti') return 'Antiproportional heisst: Das <b>Produkt</b> \\(x \\cdot y\\) bleibt gleich.' + info;
          if (e.w === 'prop') return 'Proportional heisst: Der <b>Quotient</b> \\(y : x\\) bleibt gleich, die Gerade geht durch \\((0 \\mid 0)\\).' + info;
          if (e.w === 'steigend' && A.art === 'prop') return 'Linear steigt es schon, und zusätzlich bleibt der <b>Quotient</b> \\(y : x\\) gleich.' + info;
          if (e.w === 'fallend' || e.w === 'steigend') return 'Linear heisst: \\(\\Delta y : \\Delta x\\) bleibt gleich; bei gleichen Schritten in \\(x\\) also gleiche <b>Differenzen</b>.' + info;
          return 'Prüfe zuerst die Differenzen, dann die Produkte.' + info; },
        tipps: function(A){ return ['Rechne \\(\\Delta y : \\Delta x\\) von Spalte zu Spalte und die Produkte \\(x \\cdot y\\).', '\\(\\Delta y : \\Delta x\\) gleich: linear. Produkte gleich: antiproportional. Quotient \\(y : x\\) gleich: proportional.']; },
        loesung: function(A){ return '\\text{' + { steigend: 'linear steigend', fallend: 'linear fallend', prop: 'proportional', anti: 'antiproportional', keines: 'keines davon' }[A.art] + '}'; } },

      'gegenbeispiel': { felder: ['x1', 'x2'],
        schl: function(A){ return 'ge|' + A.U; },
        eingabe: function(A){ return { x1: '1', x2: '2' }; },
        neu: function(){ var U = 2 * zufallG(5, 40);
          return { U: U, h: U / 2, text: 'Behauptung: «Alle Rechtecke mit dem Umfang ' + U + ' cm haben denselben Flächeninhalt.» Widerlege sie mit zwei Rechtecken: Gib die Länge \\(x\\) von zwei passenden Rechtecken an.',
                   muster: '\\(x_1 = \\) {x1} &nbsp; \\(x_2 = \\) {x2}' }; },
        richtig: function(A, e){ var a = bZahl(e.x1), c = bZahl(e.x2), ok = function(x){ return x > 0 && x < A.h; };
          return ok(a) && ok(c) && Math.abs(a * (A.h - a) - c * (A.h - c)) > 1e-9; },
        fehler: function(A){ return [[{ x1: '1', x2: '1' }, 'dasselbe'], [{ x1: '1', x2: String(A.h - 1) }, 'gedreht'], [{ x1: String(A.h), x2: '1' }, 'Umfang']]; },
        pruefen: function(A, e){ var a = bZahl(e.x1), c = bZahl(e.x2), aus = function(x){ return !(x > 0 && x < A.h); };
          if (aus(a) || aus(c)) return 'Bei ' + A.U + ' cm <b>Umfang</b> ist \\(x + y = ' + A.h + '\\): \\(x\\) muss zwischen 0 und ' + A.h + ' liegen, sonst gibt es kein Rechteck.';
          if (Math.abs(a - c) < 1e-9) return 'Das ist zweimal <b>dasselbe</b> Rechteck. Wähle zwei verschiedene Längen.';
          return 'Das ist dasselbe Rechteck, nur <b>gedreht</b>: \\(' + bWert(e.x1) + ' \\cdot ' + z(A.h - a) + ' = ' + z(c) + ' \\cdot ' + z(A.h - c) + '\\). Wähle ein anderes.'; },
        tipps: function(A){ return ['Für jedes \\(x\\) ist die andere Seite \\(y = ' + A.h + ' - x\\). Rechne für zwei Längen die Fläche \\(x \\cdot y\\) aus.', 'Zum Beispiel \\(x = 1\\): \\(1 \\cdot ' + (A.h - 1) + ' = ' + (A.h - 1) + '\\). Und ein anderes \\(x\\)?']; },
        loesung: function(A){ return 'x = 1: \\; 1 \\cdot ' + (A.h - 1) + ' = ' + (A.h - 1) + ', \\qquad x = 2: \\; 2 \\cdot ' + (A.h - 2) + ' = ' + 2 * (A.h - 2); } }
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
