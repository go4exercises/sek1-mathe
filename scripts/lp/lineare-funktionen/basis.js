(function(){
  'use strict';
  // Relativ, nicht absolut: Im Repo liegt die Datei eine Ebene tief, und die
  // Clips sollen von hier kommen — sonst zeigt eine lokale Vorschau den Stand
  // der Live-Site und ohne Netz gar nichts.
  var BASIS = '../';

  /* ---- Theme ---- */
  var schalter = document.getElementById('themenschalter');
  function themaLesen(){ try { return localStorage.getItem('lp-linear-thema'); } catch(e){ return null; } }
  var gespeichert = themaLesen();
  if (gespeichert === 'dark' || gespeichert === 'light') document.documentElement.setAttribute('data-theme', gespeichert);
  schalter.addEventListener('click', function(){
    var jetzt = document.documentElement.getAttribute('data-theme');
    if (!jetzt) jetzt = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    var neu = jetzt === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', neu);
    try { localStorage.setItem('lp-linear-thema', neu); } catch(e){}
  });

  /* ---- Clip-Buehne (nach clipBuehne/clipZu von mathe.begreifbar.ch) ---- */

  /* Clip-Buehne kommt aus ../mathlib.js — clipBuehne(quelle, titel).
     Vorher stand hier eine Kopie; Scrollsperre und Fokusrueckgabe
     sind dabei nach mathlib.js gewandert und gelten jetzt ueberall. */

  document.querySelectorAll('.clipkarte').forEach(function(karte){
    var knopf = karte.querySelector('.clip-start');
    knopf.addEventListener('click', function(){
      if (document.querySelector('.clip-buehne')) return;
      clipBuehne(BASIS + karte.dataset.clip, karte.dataset.titel || 'Clip');
    });
  });

  /* ---- Lösungen: alle auf/zu ---- */
  document.querySelectorAll('.alle-loesungen').forEach(function(knopf){
    knopf.addEventListener('click', function(){
      var test = knopf.closest('.test') || knopf.closest('.gesamt');
      var alle = test.querySelectorAll('details.loes');
      var oeffnen = Array.prototype.some.call(alle, function(d){ return !d.open; });
      alle.forEach(function(d){ d.open = oeffnen; });
      knopf.textContent = oeffnen ? 'Lösungen zuklappen' : 'alle Lösungen';
    });
  });

  /* ---- Fortschritt ---- */
  var tests = Array.prototype.slice.call(document.querySelectorAll('.test'));
  var fuellung = document.getElementById('balken-fuellung');
  var text = document.getElementById('fortschritt-text');
  function standLesen(){
    try { return JSON.parse(localStorage.getItem('lp-linear-stand') || '{}'); } catch(e){ return {}; }
  }
  function standSchreiben(s){ try { localStorage.setItem('lp-linear-stand', JSON.stringify(s)); } catch(e){} }
  function zeichnen(){
    var fertig = tests.filter(function(t){ return t.querySelector('.erledigt').checked; }).length;
    fuellung.style.width = (fertig / tests.length * 100) + '%';
    text.textContent = fertig + ' von ' + tests.length + ' Aufgabenblöcken bearbeitet';
  }
  var stand = standLesen();
  tests.forEach(function(t){
    var box = t.querySelector('.erledigt');
    if (stand[t.dataset.test]) box.checked = true;
    box.addEventListener('change', function(){
      var s = standLesen();
      s[t.dataset.test] = box.checked;
      standSchreiben(s);
      zeichnen();
    });
  });
  zeichnen();
  document.getElementById('fortschritt-reset').addEventListener('click', function(){
    tests.forEach(function(t){ t.querySelector('.erledigt').checked = false; });
    standSchreiben({});
    zeichnen();
  });

  /* ---- aktives Kapitel in der Schiene ---- */
  var links = Array.prototype.slice.call(document.querySelectorAll('.schiene a'));
  var ziele = links.map(function(a){ return document.querySelector(a.getAttribute('href')); }).filter(Boolean);
  if ('IntersectionObserver' in window && ziele.length){
    var beobachter = new IntersectionObserver(function(eintraege){
      eintraege.forEach(function(e){
        if (!e.isIntersecting) return;
        links.forEach(function(a){ a.classList.toggle('aktiv', a.getAttribute('href') === '#' + e.target.id); });
      });
    }, { rootMargin: '-15% 0px -70% 0px' });
    ziele.forEach(function(z){ beobachter.observe(z); });
  }
})();
