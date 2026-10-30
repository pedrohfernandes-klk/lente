// 30/10/2026: opções equilibradas (pedido do docente).
// Carrega as páginas reais e monta cada escolha alterada no respetivo motor.
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict'),vm=require('node:vm');
const ROOT=path.resolve(__dirname,'..'),trocas=require('../tools/trocas/opcoes-lente-20261030.json');
const paginas=[...new Set(trocas.map(t=>t.ficheiro))];
const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript','.css':'text/css','.json':'application/json','.webp':'image/webp','.png':'image/png','.svg':'image/svg+xml'};
function fileFor(url){let name=decodeURIComponent(new URL(url,'http://localhost').pathname).replace(/^\/lente\//,'/');let f=path.resolve(ROOT,'.'+name);if(!f.startsWith(ROOT+path.sep))return null;try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');return f;}catch{return null;}}
// 30/10/2026: revisão do #72 (opções equilibradas): as trocas que não são «escolha» (lacunas soltas e «completar»
// inteiros) também se montam; qualquer outro tipo faz o teste falhar em vez de o saltar em silêncio.
function arrayEm(s,i){let d=0,str=false,esc=false;for(let j=i;j<s.length;j++){const ch=s[j];if(str){if(esc)esc=false;else if(ch==='\\')esc=true;else if(ch==='"')str=false;continue;}if(ch==='"')str=true;else if(ch==='['||ch==='{')d++;else if(ch===']'||ch==='}'){d--;if(d===0)return JSON.parse(s.slice(i,j+1));}}throw new Error('itens sem fim');}
function itensDe(pagina){const s=fs.readFileSync(path.join(ROOT,pagina),'utf8');const k=s.indexOf('itens:',s.indexOf('EPIJogo.montar('));return arrayEm(s,s.indexOf('[',k));}
function itemDe(t){const q=JSON.parse(t.novo);if(q.t==='escolha'||q.t==='completar')return q;
 if(!q.t&&Array.isArray(q.o)&&Number.isInteger(q.c)){const pai=itensDe(t.ficheiro).filter(x=>x.t==='completar'&&(x.lacunas||[]).some(L=>JSON.stringify(L)===JSON.stringify(q)));assert.equal(pai.length,1,t.ficheiro+' '+t.local+': lacuna sem «completar»');return pai[0];}
 throw new Error('troca não coberta pelo teste: '+t.ficheiro+' '+t.local+' ('+(q.t||'sem tipo')+')');}
const montagens=trocas.map(t=>({t,q:itemDe(t)}));
const server=http.createServer((req,res)=>{const f=fileFor(req.url);if(!f){res.writeHead(404).end();return;}res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));});
for(const pagina of paginas){
 const s=fs.readFileSync(path.join(ROOT,pagina),'utf8');
 for(const m of s.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)){
  if(/\bsrc=|type=["']application\//i.test(m[1]))continue;
  new vm.Script(m[2],{filename:pagina});
 }
}
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const base='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true});let escolhas=0,completares=0;
 try{
  for(const width of [320,390,1366]){
   const ctx=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});
   await ctx.route('https://**/*',route=>{const u=route.request().url();const f=u.startsWith('https://pedrohfernandes-klk.github.io/lente/')?fileFor(u):null;return f?route.fulfill({path:f,contentType:mime[path.extname(f)]||'application/octet-stream'}):route.abort();});
   const page=await ctx.newPage(),erros=[];page.on('pageerror',e=>erros.push(e.message));
   for(const pagina of paginas){
    await page.goto(base+'/'+pagina,{waitUntil:'load'});
    assert.deepEqual(erros,[],pagina);
    for(const {q} of montagens.filter(x=>x.t.ficheiro===pagina)){
     await page.evaluate(q=>{window.qaCasca=EPICasca.abrir({marca:'Verificação'});qaCasca.raiz.setAttribute('data-qa','');EPIJogo.montar({casca:qaCasca,itens:[q],chave:'qa-opcoes',variar:false,mostrarAnterior:false});},q);
     const alvo=page.locator('[data-qa]');
     if(q.t==='completar'){
      for(let k=0;k<q.lacunas.length;k++){const L=q.lacunas[k],sel=alvo.locator('select[data-k="'+k+'"]');
       const vistos=await sel.locator('option').evaluateAll(os=>os.filter(o=>o.value!=='').map(o=>[Number(o.value),o.textContent.replace(/\s+/g,' ').trim()]));
       assert(vistos.some(([j])=>j===L.c),pagina+' certa da lacuna presente');
       for(const [j,txt] of vistos)assert.equal(txt,L.o[j].replace(/_/g,'').replace(/\s+/g,' ').trim(),pagina);
       await sel.selectOption(String(L.c));}
      if(!(await alvo.locator('.casca-folha.aberta').count()))await alvo.locator('button.c-prim:visible').last().click();
      await alvo.locator('.casca-folha.ok').waitFor({state:'visible'});
      assert((await alvo.locator('.c-expl').innerText()).length>0,pagina+' explicação');
      assert(await alvo.evaluate(el=>el.scrollWidth<=el.clientWidth),pagina+' cartão '+width);
      await page.evaluate(()=>qaCasca.fechar());completares++;continue;}
     const indices=await alvo.locator('[data-j]').evaluateAll(bs=>bs.map(b=>Number(b.dataset.j)));
     assert(indices.includes(q.c),pagina+' certa presente');
     for(const j of indices){assert.equal((await alvo.locator('[data-j="'+j+'"]').innerText()).replace(/\s+/g,' ').trim(),q.o[j].replace(/[_*]/g,'').replace(/\s+/g,' ').trim(),pagina);}
     assert(await alvo.evaluate(el=>el.scrollWidth<=el.clientWidth),pagina+' cartão '+width);
     await alvo.locator('[data-j="'+q.c+'"]').click();
     await alvo.locator('.casca-folha.ok').waitFor({state:'visible'});
     assert((await alvo.locator('.c-expl').innerText()).length>0,pagina+' explicação');
     await page.evaluate(()=>qaCasca.fechar());escolhas++;
    }
    assert.deepEqual(erros,[],pagina);
   }
   await ctx.close();console.log(width+' px: '+paginas.length+' páginas sem erros de JavaScript; escolhas e feedback verificados.');
  }
  assert.equal(escolhas+completares,3*montagens.length,'todas as trocas montadas nas três larguras');
  console.log('OK: '+escolhas+' montagens de escolhas e '+completares+' de lacunas; '+montagens.length+' trocas cobertas; sintaxe de '+paginas.length+' páginas.');
 }finally{await browser.close();server.close();}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
