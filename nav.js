// ─────────────────────────────────────────────────────────────
//  Sek1-Mathe begreifbar — Shared Navigation (nav.js)
//  Version 1.0 · 11 Themen in 3 Bereichen
//
//  Einbindung: <script src="../nav.js"></script> (von Themenseiten)
//              <script src="nav.js"></script>    (von index.html)
//  Aufruf:     buildNav({ bereich, id, kapitelNr, kapitelTitel, prev, next, homepage })
// ─────────────────────────────────────────────────────────────

const SITE = {
  themen: [
    { id:'t1-1', nr:'1.1', titel:'Zahlenmengen und Zahlenarten', url:'themen/t1-1-zahlenmengen-zahlenarten.html' },
    { id:'t1-2', nr:'1.2', titel:'Rechnen in ℤ, Potenzen mit positiven ganzen Exponenten', url:'themen/t1-2-rechnen-in-z-potenzen.html' },
    { id:'t1-3', nr:'1.3', titel:'Rechnen in ℤ repetieren, Übergang zum Rechnen in ℚ', url:'themen/t1-3-uebergang-z-q.html' },
    { id:'t1-4', nr:'1.4', titel:'Rechnen in ℚ', url:'themen/t1-4-rechnen-in-q.html' },
    { id:'t2-1', nr:'2.1', titel:'Lineare Gleichungen', url:'themen/t2-1-lineare-gleichungen.html' },
    { id:'t2-2', nr:'2.2', titel:'Textaufgaben zu den linearen Gleichungen', url:'themen/t2-2-textaufgaben-lineare-gleichungen.html' },
    { id:'t3-1', nr:'3.1', titel:'Geometrische Grundbegriffe', url:'themen/t3-1-geometrische-grundbegriffe.html' },
    { id:'t3-2', nr:'3.2', titel:'Flächen geradlinig begrenzter Figuren', url:'themen/t3-2-flaechen-geradlinig-begrenzter-figuren.html' },
    { id:'t3-3', nr:'3.3', titel:'Pythagoras', url:'themen/t3-3-pythagoras.html' },
    { id:'t3-4', nr:'3.4', titel:'Berechnungen am Kreis, Kreisteile', url:'themen/t3-4-kreis-kreisteile.html' },
    { id:'t3-5', nr:'3.5', titel:'Volumen und Oberflächen von Quader, Prisma und Zylinder', url:'themen/t3-5-quader-prisma-zylinder.html' },
  ]
};

// Themenbereich-Gruppen für die Dropdown-Anzeige
const GROUPS = {
  themen: [
    { nr:'1', titel:'Arithmetik/Algebra', ids:['t1-1', 't1-2', 't1-3', 't1-4'] },
    { nr:'2', titel:'Gleichungen', ids:['t2-1', 't2-2'] },
    { nr:'3', titel:'Geometrie', ids:['t3-1', 't3-2', 't3-3', 't3-4', 't3-5'] }
  ]
};

function buildNav(cfg) {
  // cfg = { bereich, id, kapitelNr, kapitelTitel, prev, next, homepage }
  window.__navCfg = cfg;   // Damit buildToC kapitelNr/prev/next nutzen kann.
  const prefix    = cfg.homepage ? '' : '../';
  const indexHref = cfg.homepage ? 'index.html' : '../index.html';

  // Lookup: id → page-Objekt (für Dropdown-Highlight)
  const pageById = {};
  SITE.themen.forEach(p => pageById[p.id] = p);

  // Dropdown-HTML mit Lerngebiet-Gruppierung
  function renderDropdown(bereich, ddId) {
    const groups = GROUPS[bereich];
    return groups.map(g => {
      const items = g.ids.map(id => {
        const p = pageById[id];
        return `<a href="${prefix}${p.url}" class="${p.id===cfg.id?'dd-aktiv':''}">
          <span class="dd-nr">${p.nr}</span>
          <span class="dd-tit">${p.titel}</span>
        </a>`;
      }).join('');
      return `<div class="dd-gruppe">
        <div class="dd-gruppe-titel">${g.nr} · ${g.titel}</div>
        ${items}
      </div>`;
    }).join('');
  }

  // Mobile-Nav: je Lerngebiet eine Klappe — nur die des aktuellen Kapitels
  // startet offen, damit das Menü nicht wieder als 55-zeilige Liste aufgeht.
  function renderMobileGroup(bereich) {
    const groups = GROUPS[bereich];
    return groups.map(g => {
      const items = g.ids.map(id => {
        const p = pageById[id];
        return `<a href="${prefix}${p.url}" class="${p.id===cfg.id?'mn-aktiv':''}">${p.nr} · ${p.titel}</a>`;
      }).join('');
      return `<details class="mn-lg"${g.ids.indexOf(cfg.id) !== -1 ? ' open' : ''}>
        <summary>${g.nr} · ${g.titel}</summary>
        <div class="mn-lg-body">${items}</div>
      </details>`;
    }).join('');
  }

  // Welche Sektion beim Öffnen aufgeklappt ist: genau der Bereich der aktuellen
  // Seite, auf Glossar/Formelsammlung «Nachschlagen». Beide Bereiche werden
  // gleich behandelt — auf der Startseite und den übrigen Seiten bleibt alles
  // zu und wird erst per Klick geöffnet.
  const refAktiv = (cfg.id === 'glossar' || cfg.id === 'formeln' ||
                    cfg.id === 'clips' || cfg.id === 'leitprogramme');
  const thOffen  = (cfg.bereich === 'themen');

  // ── META-DROPDOWN-INHALTE (Autor, Ausblick, Lizenz) ──
  // Drei kleine Info-Panels rechts im Header, auf jeder Seite identisch.
  const metaAutorHTML = `
    <div class="meta-titel">Autor</div>
    <img class="meta-portrait" src="${prefix}autor.jpg" width="112" height="112" loading="lazy"
         alt="Porträt von Raphael Arnold Kohler (Aquarell)">
    <p><strong>Autor:</strong> Raphael Arnold Kohler, Elektroingenieur und BM-Fachlehrperson
       für Mathematik und Physik mit über 30 Jahren Unterrichtserfahrung.</p>
    <p>Sek1-Mathe begreifbar ist ein unabhängiges, kostenlos zugängliches Lernangebot für die
       Sekundarstufe I. Es ergänzt Unterricht und Lehrmittel, ersetzt sie aber nicht.
       Das Angebot ist <strong>keine offizielle Publikation</strong> eines Kantons,
       einer Schule oder einer Prüfungsorganisation.</p>
    <p>Bei der Erstellung und technischen Umsetzung wurden KI-Werkzeuge eingesetzt.
       Alle veröffentlichten Inhalte werden redaktionell geprüft; die Verantwortung
       für die Veröffentlichung liegt bei Raphael Arnold Kohler.</p>`;

  const metaAusblickHTML = `
    <div class="meta-titel">Ausblick</div>
    <div class="meta-sub">Erstellt</div>
    <ul>
      <li>Gerüst mit 11 Themen in den Bereichen Arithmetik/Algebra, Gleichungen und Geometrie</li>
      <li>Schwesterprojekte: <a href="https://mathe.begreifbar.ch/" target="_blank" rel="noopener" class="meta-link">Mathe begreifbar</a> (Berufsmaturität) und <a href="https://physik.begreifbar.ch/" target="_blank" rel="noopener" class="meta-link">Physik begreifbar</a> — gleicher Aufbau</li>
    </ul>
    <div class="meta-sub">Im Aufbau</div>
    <ul>
      <li>Je Thema: interaktive Animationen, Aufgaben, Zusammenfassung, Druckseiten und externe Ressourcen</li>
      <li>Nachschlagen: Glossar, Formelsammlung, Clips und Leitprogramme</li>
    </ul>`;

  const metaLizenzHTML = `
    <div class="meta-titel">Lizenz</div>
    <p><strong>Autor:</strong> Raphael Arnold Kohler. Soweit nicht anders angegeben, stehen
       die von ihm erstellten Lerninhalte unter der Lizenz <strong>Creative Commons
       Namensnennung – Nicht kommerziell 4.0 International (CC BY-NC 4.0)</strong>.</p>
    <p>Die Inhalte dürfen für nicht-kommerzielle Zwecke geteilt und bearbeitet werden.
       Dabei sind Raphael Arnold Kohler als Urheber zu nennen, die Lizenz zu verlinken
       und Änderungen kenntlich zu machen. Inhalte Dritter und verlinkte externe
       Angebote unterliegen ihren eigenen Rechten und Nutzungsbedingungen.</p>
    <p><em>Empfohlene Namensnennung:</em> Raphael Arnold Kohler, Sek1-Mathe begreifbar,
       https://sek1-mathe.begreifbar.ch/, CC BY-NC 4.0.</p>
    <p><a href="https://creativecommons.org/licenses/by-nc/4.0/deed.de" target="_blank" rel="noopener" class="meta-link">
       → Lizenztext (CC BY-NC 4.0)</a></p>
    <p><a href="https://github.com/go4exercises/sek1-mathe" target="_blank" rel="noopener" class="meta-link">
       → Quelltext und Inhalte des Lehrmittels (GitHub)</a></p>`;

  // ── HEADER ──────────────────────────────────────────────────
  const headerHTML = `
<header class="site-hdr">
  <a href="${indexHref}" class="logo">
    Mathematik Sek I
  </a>
  <nav class="site-nav">
    <div class="dropdown">
      <button class="nav-btn${cfg.bereich==='themen' ? ' aktiv':''}" onclick="toggleDD('dd-th')">
        Themen ▾
      </button>
      <div class="dd-menu dd-menu-gross" id="dd-th">
        ${renderDropdown('themen','dd-th')}
      </div>
    </div>
    <div class="dropdown">
      <button class="nav-btn${(cfg.id==='glossar'||cfg.id==='formeln'||cfg.id==='clips') ? ' aktiv':''}" onclick="toggleDD('dd-ref')">
        Nachschlagen ▾
      </button>
      <div class="dd-menu" id="dd-ref">
        <div class="dd-gruppe">
          <div class="dd-gruppe-titel">In diesem Lehrmittel</div>
          <a href="${prefix}glossar.html" class="${cfg.id==='glossar'?'dd-aktiv':''}">
            <span class="dd-nr">A–Z</span><span class="dd-tit">Glossar</span>
          </a>
          <a href="${prefix}formelsammlung.html" class="${cfg.id==='formeln'?'dd-aktiv':''}">
            <span class="dd-nr">∑</span><span class="dd-tit">Formelsammlung</span>
          </a>
          <a href="${prefix}clips.html" class="${cfg.id==='clips'?'dd-aktiv':''}">
            <span class="dd-nr">▶</span><span class="dd-tit">Clips</span>
          </a>
          <a href="${prefix}leitprogramme.html" class="${cfg.id==='leitprogramme'?'dd-aktiv':''}">
            <span class="dd-nr">▤</span><span class="dd-tit">Leitprogramme</span>
          </a>
        </div>
      </div>
    </div>
    <a href="https://mathe.begreifbar.ch/" target="_blank" rel="noopener">Mathe BM ↗</a>

    <span class="nav-sep" aria-hidden="true"></span>

    <div class="dropdown">
      <button class="nav-btn nav-meta" onclick="toggleDD('dd-ueber')">
        Über ▾
      </button>
      <div class="dd-menu dd-menu-ueber" id="dd-ueber">
        <div class="ueber-tabs" role="tablist">
          <button class="ueber-tab aktiv" role="tab" data-target="ueber-autor">Autor</button>
          <button class="ueber-tab"        role="tab" data-target="ueber-ausblick">Ausblick</button>
          <button class="ueber-tab"        role="tab" data-target="ueber-lizenz">Lizenz</button>
        </div>
        <div class="ueber-panels">
          <div class="ueber-panel aktiv" id="ueber-autor"   role="tabpanel">${metaAutorHTML}</div>
          <div class="ueber-panel"        id="ueber-ausblick" role="tabpanel">${metaAusblickHTML}</div>
          <div class="ueber-panel"        id="ueber-lizenz"   role="tabpanel">${metaLizenzHTML}</div>
        </div>
      </div>
    </div>
    <a href="${prefix}feedback.html" class="nav-btn nav-meta${cfg.id==='feedback' ? ' aktiv':''}">Kontakt &amp; Feedback</a>
  </nav>
  <div class="suche" id="suche">
    <button class="such-lupe" id="such-lupe" aria-label="Suche öffnen">🔍</button>
    <input type="search" class="such-feld" id="such-feld" autocomplete="off" spellcheck="false"
           placeholder="Suchen …  /" aria-label="Lehrmittel durchsuchen">
    <div class="such-panel" id="such-panel" role="listbox"></div>
  </div>
  <button class="burger" onclick="toggleMobileNav()" aria-label="Navigation">☰</button>
</header>
<div class="mobile-nav" id="mobile-nav">
  <a href="${indexHref}" class="mn-direkt">← Übersicht</a>
  <details class="mn-sektion"${thOffen ? ' open' : ''}>
    <summary>Themen</summary>
    <div class="mn-sektion-body">${renderMobileGroup('themen')}</div>
  </details>
  <details class="mn-sektion"${refAktiv ? ' open' : ''}>
    <summary>Nachschlagen</summary>
    <div class="mn-sektion-body">
      <a href="${prefix}glossar.html" class="${cfg.id==='glossar'?'mn-aktiv':''}">A–Z · Glossar</a>
      <a href="${prefix}formelsammlung.html" class="${cfg.id==='formeln'?'mn-aktiv':''}">∑ · Formelsammlung</a>
      <a href="${prefix}clips.html" class="${cfg.id==='clips'?'mn-aktiv':''}">▶ · Clips</a>
      <a href="${prefix}leitprogramme.html" class="${cfg.id==='leitprogramme'?'mn-aktiv':''}">▤ · Leitprogramme</a>
    </div>
  </details>
  <a href="https://mathe.begreifbar.ch/" target="_blank" rel="noopener" class="mn-direkt">Mathe BM ↗</a>
  <details class="mn-sektion">
    <summary>Über dieses Lehrmittel</summary>
    <div class="mn-sektion-body">
      <details class="mn-meta"><summary>Autor</summary><div class="mn-meta-body">${metaAutorHTML}</div></details>
      <details class="mn-meta"><summary>Ausblick</summary><div class="mn-meta-body">${metaAusblickHTML}</div></details>
      <details class="mn-meta"><summary>Lizenz</summary><div class="mn-meta-body">${metaLizenzHTML}</div></details>
    </div>
  </details>
  <a href="${prefix}feedback.html" class="mn-direkt">Kontakt &amp; Feedback</a>
</div>`;

  // ── INJECT ───────────────────────────────────────────────────
  document.getElementById('nav-root').innerHTML = headerHTML;

  // Close dropdowns on outside click
  document.addEventListener('click', e => {
    if (!e.target.closest('.dropdown') && !e.target.closest('.nav-btn')) {
      document.querySelectorAll('.dd-menu').forEach(m => m.classList.remove('open'));
    }
  });
}

function toggleDD(id) {
  const el = document.getElementById(id);
  const wasOpen = el.classList.contains('open');
  document.querySelectorAll('.dd-menu').forEach(m => m.classList.remove('open'));
  if (!wasOpen) el.classList.add('open');
}

// Tabs innerhalb des "Über"-Dropdowns (Autor / Ausblick / Lizenz)
document.addEventListener('click', e => {
  const tab = e.target.closest('.ueber-tab');
  if (!tab) return;
  const wrap = tab.closest('.dd-menu-ueber');
  if (!wrap) return;
  wrap.querySelectorAll('.ueber-tab').forEach(t => t.classList.remove('aktiv'));
  wrap.querySelectorAll('.ueber-panel').forEach(p => p.classList.remove('aktiv'));
  tab.classList.add('aktiv');
  const target = wrap.querySelector('#' + tab.dataset.target);
  if (target) target.classList.add('aktiv');
});

function toggleMobileNav() {
  document.getElementById('mobile-nav').classList.toggle('open');
}

// ── Sticky ToC ────────────────────────────────────────────────
// Kurz-Labels für die wiederkehrenden Standard-Slots. Bei nicht
// gelisteten IDs bleibt der originale h2/h3-Text der Seite stehen.
const TOC_KURZ = {
  einstieg:       'Einstieg',
  definition:     'Definition',
  darstellungen:  'Darstellungen',
  typen:          'Typen',
  theorie:        'Theorie',
  aufgaben:       'Aufgaben',
  zusammenfassung:'Zusammenfassung',
  downloads:      'Zusatzmaterial',
  ressourcen:     'Externe V&AS',
  // rechtliches.html
  'datenschutz-aufruf':   'DS Seitenaufruf',
  'datenschutz-feedback': 'DS Feedback',
  // formelsammlung.html
  lg1:            '1 Arithmetik/Algebra',
  lg2:            '2 Gleichungen',
  lg3:            '3 Geometrie'
};

// Aktive Überschrift rein aus den Positionen bestimmen: die letzte, die oberhalb
// des oberen Fensterdrittels steht. Robust auch bei Sprungmarken und schnellem
// Scrollen, wo ein IntersectionObserver keine Meldung liefert.
function markiereTocAktiv() {
  const toc = document.getElementById('toc');
  if (!toc) return;
  const headings = [...document.querySelectorAll('.content h2[id]')];
  if (!headings.length) return;
  const grenze = window.innerHeight * 0.3;
  let aktiv = headings[0];
  headings.forEach(h => { if (h.getBoundingClientRect().top <= grenze) aktiv = h; });
  toc.querySelectorAll('.toc-link').forEach(l => l.classList.remove('toc-aktiv'));
  toc.querySelector(`[href="#${aktiv.id}"]`)?.classList.add('toc-aktiv');
}
let tocFrame = 0;
function tocScrollHorcher() {
  if (tocFrame) return;                       // höchstens einmal je Bild
  tocFrame = requestAnimationFrame(() => { tocFrame = 0; markiereTocAktiv(); });
}
function tocHashHorcher() { markiereTocAktiv(); }

function buildToC() {
  const toc = document.getElementById('toc');
  if (!toc) return;
  const headings = document.querySelectorAll('.content h2[id]');
  if (headings.length < 2) { toc.closest('.toc-wrap')?.remove(); return; }

  // Aus buildNav-Aufruf: Kapitelnummer + Prev/Next
  const cfg = window.__navCfg || {};
  const kapitel = cfg.kapitelNr
    ? `Kapitel <span class="toc-kapnr">${cfg.kapitelNr}</span>`
    : 'Auf dieser Seite';
  const prevLink = cfg.prev
    ? `<a href="${cfg.prev.url}" class="toc-prev" title="${cfg.prev.titel}">← ${cfg.prev.nr}</a>`
    : '';
  const nextLink = cfg.next
    ? `<a href="${cfg.next.url}" class="toc-next" title="${cfg.next.titel}">${cfg.next.nr} →</a>`
    : '';

  toc.innerHTML =
    (prevLink ? `<div class="toc-nav toc-nav-oben">${prevLink}</div>` : '') +
    `<button type="button" class="toc-title" title="Zum Seitenanfang">${kapitel}<span class="toc-title-pfeil" aria-hidden="true">↑</span></button>` +
    [...headings].map(h => {
      const label = TOC_KURZ[h.id] || h.textContent;
      return `
      <a href="#${h.id}" class="toc-link toc-${h.tagName.toLowerCase()}" title="${h.textContent.trim()}">
        ${label}
      </a>`;
    }).join('') +
    (nextLink ? `<div class="toc-nav toc-nav-unten">${nextLink}</div>` : '');

  // Markierung sofort setzen und beim Scrollen nachführen. Früher lief das über
  // einen IntersectionObserver mit dem Band 20–30 % der Fensterhöhe: der meldet
  // nur, wenn eine Überschrift dieses Band durchquert — beim Laden, nach einem
  // Ansichtswechsel und nach Sprungmarken blieb darum gar nichts markiert.
  markiereTocAktiv();
  window.removeEventListener('scroll', tocScrollHorcher);
  window.addEventListener('scroll', tocScrollHorcher, { passive: true });
  window.removeEventListener('hashchange', tocHashHorcher);
  window.addEventListener('hashchange', tocHashHorcher);

  // Sofortige, konsistente Markierung beim Klick;
  // Sprünge sind instant (kein Smooth-Scroll), wie bei der Titelwahl.
  toc.querySelectorAll('.toc-link').forEach(link => {
    link.addEventListener('click', () => {
      document.querySelectorAll('.toc-link').forEach(l => l.classList.remove('toc-aktiv'));
      link.classList.add('toc-aktiv');
    });
  });
  // Kapiteltitel = Sprung an den Seitenanfang (instant), Markierung zurücksetzen.
  const titelEl = toc.querySelector('.toc-title');
  if (titelEl) titelEl.addEventListener('click', () => {
    window.scrollTo(0, 0);
    history.replaceState(null, '', location.pathname + location.search);
    document.querySelectorAll('.toc-link').forEach(l => l.classList.remove('toc-aktiv'));
  });
}

document.addEventListener('DOMContentLoaded', buildToC);
