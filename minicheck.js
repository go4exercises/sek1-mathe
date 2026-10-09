/* minicheck.js — Mini-Check-Akkordeon: es ist immer höchstens ein
   Mini-Check (details.minicheck) geöffnet. Öffnet man den nächsten,
   schliesst der vorher offene. Die Lösungseinblendungen (.mc-loesung)
   innerhalb eines Mini-Checks bleiben davon unberührt. Kein Framework. */
(function(){
  function init(){
    var checks = document.querySelectorAll('details.minicheck');
    checks.forEach(function(d){
      d.addEventListener('toggle', function(){
        if(d.open){
          checks.forEach(function(o){ if(o !== d) o.open = false; });
        }
      });
    });
  }
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
