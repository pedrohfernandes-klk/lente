// 02/11/2026: estado antigo semeado, migração imediata e retoma real; projeção não escreve.
const {chromium}=require('playwright'),fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'..'),BASE='https://pedrohfernandes-klk.github.io/lente/',K='epi-lab-ideias-s01';
const antiga={versao:'versao-antiga',lida:true,t:1700000000000,melhor:11,totalMelhor:13,tentativas:2,exposicoes:{0:2}};
(async()=>{const b=await chromium.launch();try{
for(const width of [390,1366])for(const proj of [false,true]){
 const c=await b.newContext({viewport:{width,height:900}}),p=await c.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));
 await c.route('**/*',r=>{const u=r.request().url();if(!u.startsWith(BASE))return r.abort();let rel=decodeURIComponent(u.slice(BASE.length).split('?')[0]);if(rel.endsWith('/'))rel+='index.html';const f=path.resolve(ROOT,rel);if(!f.startsWith(ROOT+path.sep)||!fs.existsSync(f))return r.fulfill({status:404,body:''});const mime={'.html':'text/html','.js':'application/javascript','.css':'text/css','.webp':'image/webp','.svg':'image/svg+xml','.png':'image/png'};return r.fulfill({contentType:mime[path.extname(f)]||'application/octet-stream',body:fs.readFileSync(f)});});
 await c.addInitScript(({K,antiga})=>{if(!sessionStorage.getItem('semeado')){localStorage.setItem(K,JSON.stringify(antiga));sessionStorage.setItem('semeado','1')}},{K,antiga});
 await p.goto(BASE+'narrativas/ideias/sessao-01/'+(proj?'?projetar=1':''));
 const st=await p.evaluate(K=>JSON.parse(localStorage.getItem(K)),K);
 if(proj)assert.deepEqual(st,antiga);else{assert.equal(st.antes.lida,true);assert.equal(st.antes.data,antiga.t);assert.equal(st.antes.melhor,11);assert.equal(st.exposicoes,undefined);assert.notEqual(st.versao,antiga.versao);}
 await p.goto(BASE+'narrativas/ideias/'+(proj?'?projetar=1':''));
 const li=p.locator('li[data-chave="'+K+'"]');
 if(proj){assert.equal(await li.locator('[data-estado]').textContent(),'A seguir');assert.deepEqual(await p.evaluate(K=>JSON.parse(localStorage.getItem(K)),K),antiga);}
 else{assert.match(await li.locator('[data-estado]').textContent(),/Feita 14\/11/);assert.match(await p.locator('[data-p-botao]').getAttribute('href'),/sessao-02/);}
 if(proj){
  await p.evaluate(url=>{const f=document.createElement('iframe');f.src=url;f.id='prova-moldura';f.style.cssText='position:fixed;inset:0;width:100vw;height:100vh;border:0;z-index:9999';document.body.appendChild(f)},BASE+'narrativas/ideias/sessao-01/');
  const frame=p.frameLocator('#prova-moldura');await frame.locator('[data-c-num]').waitFor();assert.match(await frame.locator('[data-c-num]').innerText(),/^1\//);
  await frame.locator('.casca-acoes button',{hasText:/Seguinte/}).click();
  assert.deepEqual(await p.evaluate(K=>JSON.parse(localStorage.getItem(K)),K),antiga,'moldura de projeção escreveu');
 }
 assert.deepEqual(erros,[]);assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await c.close();console.log('PASS migração e retoma '+width+' projeção '+proj);
}}finally{await b.close()}})().catch(e=>{console.error(e);process.exit(1)});
