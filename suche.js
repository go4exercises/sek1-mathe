// ─────────────────────────────────────────────────────────────
//  Mathe begreifbar — Volltextsuche über die ganze Site (suche.js)
//
//  Einbindung: <script src="../suche.js"></script>  (nach nav.js)
//              <script src="suche.js"></script>     (Root-Seiten)
//  Das Suchfeld baut nav.js in den Header (rechts); dieses Skript
//  hängt sich daran und lädt den Index beim ersten Gebrauch nach.
//
//  Der Index (suchindex.js, generiert aus den Seiten) wird bewusst erst
//  bei der ersten Sucheingabe geladen — wer nicht sucht, lädt nichts.
//  Neu bauen: python3 scripts/build-suchindex.py
// ─────────────────────────────────────────────────────────────

(function () {
  'use strict';

  // Pfad zum Index aus dem eigenen <script src="…"> ableiten —
  // funktioniert von Root-Seiten wie von grundlagen/ und schwerpunkt/ aus.
  const eigenerPfad = (document.currentScript && document.currentScript.src) || 'suche.js';
  const INDEX_URL = eigenerPfad.replace(/suche\.js(\?.*)?$/, 'suchindex.js');
  const BASIS = eigenerPfad.replace(/suche\.js(\?.*)?$/, '');

  let idx = null;          // {seiten, eintraege}
  let ladend = false;
  let letzteQuery = '';
  let markiert = -1;       // Tastatur-Auswahl im Trefferpanel

  // ── Normalisierung ────────────────────────────────────────
  // 1:1 in der Länge (ä→a, nicht ä→ae), damit gefundene Positionen
  // direkt auf den Originaltext passen und der Ausschnitt stimmt.
  const UML = { 'ä': 'a', 'ö': 'o', 'ü': 'u', 'ß': 's', 'à': 'a', 'á': 'a', 'â': 'a',
                'è': 'e', 'é': 'e', 'ê': 'e', 'ï': 'i', 'î': 'i', 'ô': 'o', 'û': 'u' };
  function falte(s) {
    return s.toLowerCase().replace(/[äöüßàáâèéêïîôû]/g, c => UML[c] || c);
  }
  // Wer „flaeche" tippt, meint „Fläche" — zweite Variante mitprüfen.
  function varianten(tok) {
    const a = falte(tok);
    const b = a.replace(/ae/g, 'a').replace(/oe/g, 'o').replace(/ue/g, 'u');
    return b !== a ? [a, b] : [a];
  }
  function istWortanfang(text, pos) {
    if (pos === 0) return true;
    return !/[a-zäöüß0-9]/i.test(text.charAt(pos - 1));
  }

  // ── Index laden ───────────────────────────────────────────
  function ladeIndex(dann) {
    if (idx) { dann(); return; }
    if (ladend) { document.addEventListener('suchindex-bereit', dann, { once: true }); return; }
    ladend = true;
    const s = document.createElement('script');
    s.src = INDEX_URL;
    s.onload = function () {
      idx = window.SUCHINDEX || { seiten: [], eintraege: [] };
      idx.eintraege.forEach(e => { e._t = falte(e.t); e._x = falte(e.x); });
      idx.seiten.forEach(s => { s._t = falte(s.t); });
      ladend = false;
      document.dispatchEvent(new Event('suchindex-bereit'));
      dann();
    };
    s.onerror = function () {
      ladend = false;
      zeigePanel('<div class="sr-leer">Der Suchindex konnte nicht geladen werden.</div>');
    };
    document.head.appendChild(s);
  }

  // ── Suche ─────────────────────────────────────────────────
  function suche(q) {
    const tokens = q.trim().split(/\s+/).filter(t => t.length >= 2).map(varianten);
    if (!tokens.length) return [];

    const treffer = [];
    for (const e of idx.eintraege) {
      let score = 0, ok = true, ersteStelle = -1;

      for (const vars of tokens) {
        let bestes = 0, stelle = -1;

        for (const v of vars) {
          let p = e._t.indexOf(v);
          if (p >= 0) bestes = Math.max(bestes, istWortanfang(e._t, p) ? 45 : 22);
          if (e._t === v) bestes = Math.max(bestes, 80);

          p = e._x.indexOf(v);
          if (p >= 0) {
            let n = 0, k = p;
            while (k >= 0 && n < 6) { n++; k = e._x.indexOf(v, k + v.length); }
            bestes = Math.max(bestes, (istWortanfang(e._x, p) ? 10 : 3) + n);
            if (stelle < 0) stelle = p;
          }
        }
        if (!bestes) { ok = false; break; }
        score += bestes;
        if (ersteStelle < 0) ersteStelle = stelle;
      }
      if (!ok) continue;
      const seite = idx.seiten[e.p];
      // Wer „Logarithmen" sucht, will zuerst das Kapitel 1.3 sehen, nicht dessen
      // Unterabschnitte: Kapitel-Einstieg (Anker leer) mit Titeltreffer hochziehen.
      if (seite && !e.a) {
        for (const vars of tokens) {
          for (const v of vars) {
            if (seite._t === v) score += 45;
            else if (seite._t.indexOf(v) === 0) score += 22;
          }
        }
      }
      // Glossar-Einträge sind kurz und auf den Punkt — leicht bevorzugen.
      if (seite && seite.u === 'glossar.html') score += 3;
      treffer.push({ e: e, score: score, pos: ersteStelle });
    }
    treffer.sort((a, b) => b.score - a.score || a.e.p - b.e.p);
    return treffer.slice(0, 20);
  }

  // ── Darstellung ───────────────────────────────────────────
  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function ausschnitt(text, gefaltet, pos, tokens) {
    if (pos < 0) pos = 0;
    let von = Math.max(0, pos - 55);
    if (von > 0) { const l = text.indexOf(' ', von); if (l > 0 && l < von + 20) von = l + 1; }
    let stueck = text.slice(von, von + 190);
    const off = von;
    // Alle Treffer im Ausschnitt markieren
    const stellen = [];
    for (const vars of tokens) {
      for (const v of vars) {
        let p = gefaltet.indexOf(v, off);
        while (p >= 0 && p < off + stueck.length) {
          stellen.push([p - off, v.length]);
          p = gefaltet.indexOf(v, p + v.length);
        }
      }
    }
    stellen.sort((a, b) => a[0] - b[0]);
    let out = '', letzte = 0;
    for (const [p, len] of stellen) {
      if (p < letzte) continue;
      out += esc(stueck.slice(letzte, p)) + '<mark>' + esc(stueck.slice(p, p + len)) + '</mark>';
      letzte = p + len;
    }
    out += esc(stueck.slice(letzte));
    return (von > 0 ? '… ' : '') + out + (von + 190 < text.length ? ' …' : '');
  }

  function zeigePanel(html) {
    const p = document.getElementById('such-panel');
    if (!p) return;
    p.innerHTML = html;
    p.classList.add('offen');
  }
  function schliessePanel() {
    const p = document.getElementById('such-panel');
    if (p) { p.classList.remove('offen'); p.innerHTML = ''; }
    markiert = -1;
  }
  // Mobil: Panel zu UND das über der Seite liegende Feld wieder einklappen
  function schliesseAlles() {
    schliessePanel();
    const s = document.getElementById('suche');
    if (s) s.classList.remove('offen');
  }

  function rendere(q) {
    const tokens = q.trim().split(/\s+/).filter(t => t.length >= 2).map(varianten);
    const res = suche(q);
    if (!res.length) {
      zeigePanel('<div class="sr-leer">Keine Treffer für <strong>' + esc(q) + '</strong></div>');
      return;
    }
    const html = res.map((r, i) => {
      const seite = idx.seiten[r.e.p] || { u: '', nr: '', t: '' };
      const ziel = BASIS + seite.u + (r.e.a ? '#' + r.e.a : '');
      return '<a class="sr" href="' + ziel + '" data-i="' + i + '">' +
             '<span class="sr-nr">' + esc(seite.nr) + '</span>' +
             '<span class="sr-body">' +
               '<span class="sr-t">' + esc(r.e.t) + '</span>' +
               '<span class="sr-q">' + esc(seite.t) + '</span>' +
               '<span class="sr-x">' + ausschnitt(r.e.x, r.e._x, r.pos, tokens) + '</span>' +
             '</span></a>';
    }).join('');
    zeigePanel(html + '<div class="sr-fuss">' + res.length +
               (res.length === 20 ? '+' : '') + ' Treffer · ↑ ↓ wählen · ⏎ öffnen · Esc schliesst</div>');
    markiert = -1;
  }

  function markiere(delta) {
    const items = [...document.querySelectorAll('#such-panel .sr')];
    if (!items.length) return;
    items.forEach(a => a.classList.remove('sr-aktiv'));
    markiert += delta;
    if (markiert < 0) markiert = items.length - 1;
    if (markiert >= items.length) markiert = 0;
    items[markiert].classList.add('sr-aktiv');
    if (items[markiert].scrollIntoView) items[markiert].scrollIntoView({ block: 'nearest' });
  }

  // ── Verdrahtung ───────────────────────────────────────────
  function init() {
    const feld = document.getElementById('such-feld');
    if (!feld) return;

    feld.addEventListener('input', function () {
      const q = feld.value;
      if (q.trim().length < 2) { schliessePanel(); letzteQuery = ''; return; }
      if (q === letzteQuery) return;
      letzteQuery = q;
      ladeIndex(() => { if (feld.value === q) rendere(q); });
    });

    feld.addEventListener('focus', function () {
      ladeIndex(() => {});                       // vorladen, sobald jemand hineinklickt
      if (feld.value.trim().length >= 2) rendere(feld.value);
    });

    feld.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowDown') { ev.preventDefault(); markiere(1); }
      else if (ev.key === 'ArrowUp') { ev.preventDefault(); markiere(-1); }
      else if (ev.key === 'Enter') {
        const items = [...document.querySelectorAll('#such-panel .sr')];
        const ziel = items[markiert >= 0 ? markiert : 0];
        if (ziel) { ev.preventDefault(); ziel.click(); }
      } else if (ev.key === 'Escape') { feld.blur(); schliesseAlles(); }
    });

    // Klick auf einen Treffer der *aktuellen* Seite: nur springen, nicht neu laden
    document.addEventListener('click', function (ev) {
      const a = ev.target.closest && ev.target.closest('#such-panel .sr');
      if (a) { schliesseAlles(); return; }
      if (!ev.target.closest || !ev.target.closest('.suche')) schliesseAlles();
    });

    // Burger und Suche sollen sich auf schmalen Schirmen nicht überlagern
    const burger = document.querySelector('.burger');
    if (burger) burger.addEventListener('click', schliesseAlles);

    // Tastenkürzel: „/" oder Strg/Cmd + K
    document.addEventListener('keydown', function (ev) {
      const t = ev.target.tagName;
      const tippt = t === 'INPUT' || t === 'TEXTAREA' || ev.target.isContentEditable;
      if ((ev.key === '/' && !tippt) || ((ev.ctrlKey || ev.metaKey) && ev.key === 'k')) {
        ev.preventDefault();
        feld.focus();
        feld.select();
      }
    });

    // Direkteinstieg per Adresse: …/?q=parabel  (so verlangt es auch die
    // SearchAction in den strukturierten Daten der Startseite)
    const vorgabe = new URLSearchParams(location.search).get('q');
    if (vorgabe && vorgabe.trim().length >= 2) {
      feld.value = vorgabe;
      letzteQuery = vorgabe;
      const s = document.getElementById('suche');
      if (s) s.classList.add('offen');
      ladeIndex(() => rendere(vorgabe));
    }

    // Mobile: Lupe klappt das Feld auf
    const lupe = document.getElementById('such-lupe');
    if (lupe) lupe.addEventListener('click', function () {
      document.getElementById('suche').classList.toggle('offen');
      if (document.getElementById('suche').classList.contains('offen')) feld.focus();
      else schliessePanel();
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
