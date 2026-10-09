// TALS-Mathematik JS-Laufzeit-Verifikation (portiert aus TALS-Physik P2-3) · benoetigt: npm install jsdom · Aufruf: NODE_PATH=node_modules node scripts/verify_js_runtime.js grundlagen/*.html schwerpunkt/*.html
const fs=require('fs'), path=require('path');
const {JSDOM, VirtualConsole}=require('jsdom');
const ROOT=process.env.TALS_ROOT||'.';
const libs={};
for(const l of ['nav.js','mathlib.js','minicheck.js','anim-hinweise.js'])
  // </script> in JS escapen, damit der HTML-Parser das Inline-Script nicht zu früh schliesst
  libs[l]=fs.readFileSync(path.join(ROOT,l),'utf8').replace(/<\/script>/gi,'<\\/script>');

const bootstrap=`
HTMLCanvasElement.prototype.getContext=function(){return new Proxy(function(){},{get:function(t,p){
  if(p==='createLinearGradient'||p==='createRadialGradient'||p==='createPattern')return function(){return {addColorStop:function(){}};};
  if(p==='measureText')return function(){return {width:10};};
  if(p==='getImageData')return function(){return {data:[],width:0,height:0};};
  if(p==='canvas')return {width:300,height:150};
  return function(){};},apply:function(){}});};
window.requestAnimationFrame=function(){return 0;};window.cancelAnimationFrame=function(){};
window.matchMedia=window.matchMedia||function(){return {matches:false,addListener:function(){},removeListener:function(){},addEventListener:function(){},removeEventListener:function(){}};};
window.IntersectionObserver=function(){this.observe=function(){};this.unobserve=function(){};this.disconnect=function(){};};
window.speechSynthesis={speak:function(){},cancel:function(){},getVoices:function(){return [];}};
window.SpeechSynthesisUtterance=function(){};
window.MathJax={typesetPromise:function(){return Promise.resolve();},typeset:function(){},startup:{promise:Promise.resolve()}};
`;
function prep(html){
  html=html.replace(/<script\s+src="\.\.\/(nav|mathlib|minicheck|anim-hinweise)\.js"\s*><\/script>/g,(m,n)=>'<script>'+libs[n+'.js']+'</script>');
  html=html.replace(/<script[^>]*\ssrc="https?:\/\/[^"]*"[^>]*><\/script>/g,'');
  html=html.replace(/<head[^>]*>/i,m=>m+'<script>'+bootstrap+'</script>');
  return html;
}
let bad=0;
for(const f of process.argv.slice(2)){
  const errs=[]; const vc=new VirtualConsole();
  vc.on('jsdomError',e=>errs.push((e.detail&&e.detail.message)||e.message||String(e)));
  const dom=new JSDOM(prep(fs.readFileSync(f,'utf8')),{runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,url:'file://'+f});
  const w=dom.window;
  w.addEventListener('error',ev=>errs.push((ev.error&&ev.error.message)||ev.message));
  try{ w.document.dispatchEvent(new w.Event('DOMContentLoaded',{bubbles:true})); }catch(e){errs.push('DCL:'+e.message);}
  try{ w.dispatchEvent(new w.Event('load')); }catch(e){errs.push('load:'+e.message);}
  try{ w.dispatchEvent(new w.Event('resize')); }catch(e){errs.push('resize:'+e.message);}
  const sane=(typeof w.buildNav==='function')&&(typeof w.initCanvas==='function')&&(typeof w.toggleL==='function');
  const navEl=w.document.querySelector('#nav-root');
  const navRendered=!!(navEl&&navEl.children.length>0);
  const tocEl=w.document.querySelector('#toc');
  const tocRendered=!!(tocEl&&tocEl.children.length>0);
  const real=errs.filter(e=>!/Not implemented|Could not load|Could not parse CSS|HTMLCanvasElement/i.test(e));
  const name=f.split('/').pop();
  console.log(name.padEnd(28)+(real.length?'JS-FEHLER('+real.length+')':'ok')
    +'  libs='+(sane?'ok':'FEHLEN')+'  nav='+(navRendered?'ok':'nein')+'  toc='+(tocRendered?'ok':'nein'));
  real.slice(0,4).forEach(e=>console.log('     '+String(e).slice(0,140)));
  if(real.length||!sane||!navRendered) bad++;
}
console.log('\nProblematische Seiten: '+bad);
