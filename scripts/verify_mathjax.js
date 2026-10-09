// TALS-Mathematik MathJax-Verifikation (portiert aus TALS-Physik P2-3) · benoetigt: npm install mathjax-full · Aufruf: NODE_PATH=node_modules node scripts/verify_mathjax.js grundlagen/*.html schwerpunkt/*.html ...
const fs=require('fs'), path=require('path');
const {mathjax}=require('mathjax-full/js/mathjax.js');
const {TeX}=require('mathjax-full/js/input/tex.js');
const {SVG}=require('mathjax-full/js/output/svg.js');
const {liteAdaptor}=require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler}=require('mathjax-full/js/handlers/html.js');
const {AllPackages}=require('mathjax-full/js/input/tex/AllPackages.js');
const adaptor=liteAdaptor(); RegisterHTMLHandler(adaptor);
const texIn=new TeX({packages:AllPackages});
const svgOut=new SVG({fontCache:'none'});
const doc=mathjax.document('',{InputJax:texIn,OutputJax:svgOut});

function errs(expr,display){
  try{
    const node=doc.convert(expr,{display});
    const html=adaptor.outerHTML(node);
    if(html.includes('data-mjx-error')||html.includes('merror')){
      const m=html.match(/data-mjx-error="([^"]*)"/);
      return m?m[1]:'merror';
    }
    return null;
  }catch(e){ return 'EXCEPTION: '+e.message; }
}
function extract(html){
  html=html.replace(/<script[\s\S]*?<\/script>/g,'').replace(/<style[\s\S]*?<\/style>/g,'');
  // HTML-Entities dekodieren: der Browser liefert MathJax den DOM-Text, nicht das rohe HTML.
  // Ohne Dekodierung meldet die TeX-Engine bei &lt;/&gt; faelschlich "Misplaced &".
  html=html.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&nbsp;/g,' ')
           .replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&amp;/g,'&');
  const out=[];
  let re=/\\\(([\s\S]*?)\\\)/g,m;
  while((m=re.exec(html))) out.push([m[1],false]);
  re=/\\\[([\s\S]*?)\\\]/g;
  while((m=re.exec(html))) out.push([m[1],true]);
  return out;
}
const files=process.argv.slice(2);
let gExpr=0,gErr=0,badfiles=0;
for(const f of files){
  const html=fs.readFileSync(f,'utf8');
  const exprs=extract(html);
  let fe=0; const details=[];
  for(const [e,d] of exprs){
    const err=errs(e,d);
    if(err){fe++; details.push((d?'[\\[]':'[\\(]')+' '+e.slice(0,50).replace(/\n/g,' ')+'  -> '+err);}
  }
  gExpr+=exprs.length; gErr+=fe; if(fe)badfiles++;
  const name=f.replace(process.cwd()+'/','');
  console.log(name.padEnd(46)+' expr='+String(exprs.length).padStart(4)+' fehler='+fe);
  details.slice(0,5).forEach(d=>console.log('     '+d));
}
console.log('\nSUMME: '+gExpr+' Ausdrücke, '+gErr+' Fehler in '+badfiles+' Dateien');
