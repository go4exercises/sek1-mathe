/* anim-hinweise.js — gemeinsame Logik für die Animations-Hinweise
   (Rollover "Worauf achten?" / "Erkenntnis").
   Markup pro Animation (in style.css gestaltet):
     <div class="widget-titelzeile">
       <h3>…Titel…</h3>
       <div class="anim-hinweis links">  …Auslöser + .ah-pop…  </div>
       <div class="anim-hinweis rechts"> …Auslöser + .ah-pop…  </div>
     </div>
   Klick/Tap auf den Auslöser fixiert das Rollover, damit es beim Lesen
   offen bleibt; Klick daneben oder Escape schliesst es wieder. */
(function(){
  function init(){
    function entfixieren(ausser){
      document.querySelectorAll('.anim-hinweis.fixiert').forEach(function(x){
        if(x!==ausser) x.classList.remove('fixiert');
      });
    }

    // Klick/Tap auf den Auslöser fixiert das Rollover
    document.querySelectorAll('.anim-hinweis .ah-trigger').forEach(function(tr){
      tr.addEventListener('click', function(e){
        e.stopPropagation();
        var h = tr.closest('.anim-hinweis');
        var war = h.classList.contains('fixiert');
        entfixieren(h);
        h.classList.toggle('fixiert', !war);
      });
    });

    // Klick ausserhalb schliesst fixierte Hinweise
    document.addEventListener('click', function(e){
      if(!e.target.closest('.anim-hinweis')) entfixieren(null);
    });
    // Escape schliesst ebenfalls
    document.addEventListener('keydown', function(e){
      if(e.key==='Escape') entfixieren(null);
    });
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
