/* Dez sessões: desenho, condução, estado, tarefa protegida e projeção.
   27/10/2026, molde das sessões: abre-se com «Começar» (data-start) e avança-se um passo de cada vez
   (Recupera, Vê, Decide, Faz, Leva); o registo aparece no último passo. M1_OUT escolhe a pasta das capturas. */
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
const {chromium}=require('playwright');
const R=path.resolve(__dirname,'..'),OUT=process.env.M1_OUT||path.resolve(R,'../../outputs/revisao-dez-sessoes');fs.mkdirSync(OUT,{recursive:true});
const MIME={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.webp':'image/webp','.jpg':'image/jpeg','.png':'image/png','.pdf':'application/pdf'};
function file(url){let name=decodeURIComponent(new URL(url,'http://local').pathname).replace(/^\/lente\/?/,'');let p=path.resolve(R,name);if(!p.startsWith(R+path.sep)&&p!==R)throw Error('path');if(fs.existsSync(p)&&fs.statSync(p).isDirectory())p=path.join(p,'index.html');return p;}
const server=http.createServer((req,res)=>{try{const p=file(req.url);res.writeHead(fs.existsSync(p)?200:404,{'Content-Type':MIME[path.extname(p)]||'application/octet-stream'});res.end(fs.existsSync(p)?fs.readFileSync(p):'Not found')}catch(e){res.writeHead(400);res.end('Invalid path')}});
const results=[],KEY='lente-cidadania-m1-sessoes-v2';
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
const browser=await chromium.launch({headless:true,...(process.env.M1_CHROMIUM?{executablePath:process.env.M1_CHROMIUM}:{})});
async function context(width=1440,scheme='light'){
 const c=await browser.newContext({viewport:{width,height:1000},colorScheme:scheme,reducedMotion:'reduce'});
 await c.route('https://pedrohfernandes-klk.github.io/lente/**',async route=>{const p=file(route.request().url());await route.fulfill({status:fs.existsSync(p)?200:404,body:fs.existsSync(p)?fs.readFileSync(p):'',contentType:MIME[path.extname(p)]||'application/octet-stream'})});
 await c.route('https://fonts.googleapis.com/**',r=>r.abort());await c.route('https://fonts.gstatic.com/**',r=>r.abort());return c;
}
try{
 for(const width of [320,390,768,1440])for(const scheme of ['light','dark']){
  const ctx=await context(width,scheme),p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
  for(const route of ['','cidadania/','cidadania/m1/','cidadania/projeto/','cidadania/m1/biblioteca/','cidadania/m1/sessoes/03/','cidadania/m1/sessoes/04/','cidadania/m1/sessoes/06/','cidadania/m1/sessoes/09/','cidadania/m1/sessoes/']){
   assert.equal((await p.goto(origin+'/lente/'+route)).status(),200);await p.waitForTimeout(80);
   // 01/11/2026: conservar o limite e identificar os elementos que transbordam, incluindo fontes alternativas.
   const overflow = await p.evaluate(()=>({width:document.documentElement.scrollWidth,viewport:innerWidth,elements:[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,60)}))}));
   assert(overflow.width<=overflow.viewport,`${width} ${scheme} ${route}: ${JSON.stringify(overflow)}`);assert.deepEqual(errors,[],route);
   if(route==='cidadania/m1/'){assert.equal(await p.locator('[data-session-card]').count(),10);assert((await p.locator('[data-continue]').getAttribute('href')).includes('03/'));assert(await p.locator('.c10 .epi-projection-menu-link').isVisible());}
   if(width===1440&&scheme==='light'&&['cidadania/m1/','cidadania/m1/sessoes/03/','cidadania/m1/sessoes/06/'].includes(route))await p.screenshot({path:path.join(OUT,route==='cidadania/m1/'?'modulo.png':route.includes('03/')?'sessao-03.png':'sessao-06.png'),fullPage:true});
   if(width===390&&scheme==='dark'&&route==='cidadania/m1/sessoes/09/')await p.screenshot({path:path.join(OUT,'sessao-09-telemovel.png'),fullPage:true});
   results.push({route,width,scheme,overflow:false,errors:[]});
  }await ctx.close();
 }
 const ctx=await context(),p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));await p.goto(origin+'/lente/cidadania/m1/');
 const legacy={'epi-cidadania-m1':'{"feitas":{"passo-01":123}}','lente-justica-licao-1':'{"lida":true}','lente-cidadania-m1-v2':'{"version":2,"done":{"F01":true}}'};
 await p.evaluate(values=>{for(const [k,v]of Object.entries(values))localStorage.setItem(k,v)},legacy);
 /* 05/11/2026 (plano do molde da Cidadania, pedido 2; decisões 157 e 158): no endereço da sessão 01 está a lição no molde final
    (tools/licoes/cidadania-m1-s01.json), com a chave epi-cid-m1-s01, sem os cinco passos do molde publicado e sem registo; o
    seu percurso completo está em tests/browser_licoes_lente.cjs. As sessões 02 a 10 publicadas continuam com tudo o que se
    exigia, e as chaves antigas semeadas acima não se apagam ao abrir a 01. */
 {await p.goto(origin+'/lente/cidadania/m1/sessoes/01/');await p.waitForTimeout(300);
  assert.equal(await p.locator('h1').count(),1);assert(await p.evaluate(()=>document.body.classList.contains('molde-cidadania')));
  assert.equal(await p.locator('[data-stage]').count(),0);assert.equal(await p.locator('[data-session-done]').count(),0);
  assert.equal(await p.locator('[data-c-num]').innerText(),'1/23');
  for(const [k,v] of Object.entries(legacy))assert.equal(await p.evaluate(k=>localStorage.getItem(k),k),v,k);}
 /* 06/11/2026 (decisão 166): a sessão 02 passa também ao molde final, no mesmo endereço (tools/licoes/cidadania-m1-s02.json),
    com a chave epi-cid-m1-s02; exige-se o mesmo que à 01. As sessões 03 a 10 publicadas continuam com tudo o que se exigia. */
 {await p.goto(origin+'/lente/cidadania/m1/sessoes/02/');await p.waitForTimeout(300);
  assert.equal(await p.locator('h1').count(),1);assert(await p.evaluate(()=>document.body.classList.contains('molde-cidadania')));
  assert.equal(await p.locator('[data-stage]').count(),0);assert.equal(await p.locator('[data-session-done]').count(),0);
  assert.equal(await p.locator('[data-c-num]').innerText(),'1/23');
  for(const [k,v] of Object.entries(legacy))assert.equal(await p.evaluate(k=>localStorage.getItem(k),k),v,k);}
 /* 06/11/2026 (decisões 166 a 168): a sessão 03 passa também ao molde final, no mesmo endereço (tools/licoes/cidadania-m1-s03.json),
    com a chave epi-cid-m1-s03; exige-se o mesmo que à 01 e à 02. As sessões 04 a 10 publicadas continuam com tudo o que se exigia. */
 {await p.goto(origin+'/lente/cidadania/m1/sessoes/03/');await p.waitForTimeout(300);
  assert.equal(await p.locator('h1').count(),1);assert(await p.evaluate(()=>document.body.classList.contains('molde-cidadania')));
  assert.equal(await p.locator('[data-stage]').count(),0);assert.equal(await p.locator('[data-session-done]').count(),0);
  assert.equal(await p.locator('[data-c-num]').innerText(),'1/23');
  for(const [k,v] of Object.entries(legacy))assert.equal(await p.evaluate(k=>localStorage.getItem(k),k),v,k);}
 /* 06/11/2026 (decisões 166 a 168): a sessão 04 passa também ao molde final, no mesmo endereço (tools/licoes/cidadania-m1-s04.json),
    com a chave epi-cid-m1-s04; exige-se o mesmo que à 01, à 02 e à 03, e salta do ciclo abaixo. As 05 a 10 publicadas continuam
    com tudo o que se exigia. */
 {await p.goto(origin+'/lente/cidadania/m1/sessoes/04/');await p.waitForTimeout(300);
  assert.equal(await p.locator('h1').count(),1);assert(await p.evaluate(()=>document.body.classList.contains('molde-cidadania')));
  assert.equal(await p.locator('[data-stage]').count(),0);assert.equal(await p.locator('[data-session-done]').count(),0);
  assert.equal(await p.locator('[data-c-num]').innerText(),'1/23');
  for(const [k,v] of Object.entries(legacy))assert.equal(await p.evaluate(k=>localStorage.getItem(k),k),v,k);}
 /* 06/11/2026 (decisões 166 a 168): a sessão 05 passa também ao molde final, no mesmo endereço (tools/licoes/cidadania-m1-s05.json),
    com a chave epi-cid-m1-s05; exige-se o mesmo que às 01 a 04, e salta do ciclo abaixo. As 06 a 10 publicadas continuam com tudo
    o que se exigia. */
 {await p.goto(origin+'/lente/cidadania/m1/sessoes/05/');await p.waitForTimeout(300);
  assert.equal(await p.locator('h1').count(),1);assert(await p.evaluate(()=>document.body.classList.contains('molde-cidadania')));
  assert.equal(await p.locator('[data-stage]').count(),0);assert.equal(await p.locator('[data-session-done]').count(),0);
  assert.equal(await p.locator('[data-c-num]').innerText(),'1/23');
  for(const [k,v] of Object.entries(legacy))assert.equal(await p.evaluate(k=>localStorage.getItem(k),k),v,k);}
 /* 06/11/2026 (decisões 166 a 168): a sessão 06 passa também ao molde final, no mesmo endereço (tools/licoes/cidadania-m1-s06.json),
    com a chave epi-cid-m1-s06; exige-se o mesmo que às 01 a 05, e salta do ciclo abaixo. As 07 a 10 publicadas continuam com tudo
    o que se exigia. */
 {await p.goto(origin+'/lente/cidadania/m1/sessoes/06/');await p.waitForTimeout(300);
  assert.equal(await p.locator('h1').count(),1);assert(await p.evaluate(()=>document.body.classList.contains('molde-cidadania')));
  assert.equal(await p.locator('[data-stage]').count(),0);assert.equal(await p.locator('[data-session-done]').count(),0);
  assert.equal(await p.locator('[data-c-num]').innerText(),'1/23');
  for(const [k,v] of Object.entries(legacy))assert.equal(await p.evaluate(k=>localStorage.getItem(k),k),v,k);}
 /* 06/11/2026 (decisões 166 a 168): a sessão 07 passa também ao molde final, no mesmo endereço (tools/licoes/cidadania-m1-s07.json),
    com a chave epi-cid-m1-s07; exige-se o mesmo que às 01 a 06, e salta do ciclo abaixo. As 08 a 10 publicadas continuam com tudo
    o que se exigia. */
 {await p.goto(origin+'/lente/cidadania/m1/sessoes/07/');await p.waitForTimeout(300);
  assert.equal(await p.locator('h1').count(),1);assert(await p.evaluate(()=>document.body.classList.contains('molde-cidadania')));
  assert.equal(await p.locator('[data-stage]').count(),0);assert.equal(await p.locator('[data-session-done]').count(),0);
  assert.equal(await p.locator('[data-c-num]').innerText(),'1/23');
  for(const [k,v] of Object.entries(legacy))assert.equal(await p.evaluate(k=>localStorage.getItem(k),k),v,k);}
 /* 06/11/2026 (decisões 166 a 168): a sessão 08 passa também ao molde final, no mesmo endereço (tools/licoes/cidadania-m1-s08.json),
    com a chave epi-cid-m1-s08; exige-se o mesmo que às 01 a 07, e salta do ciclo abaixo. As 09 e 10 publicadas continuam com tudo
    o que se exigia. */
 {await p.goto(origin+'/lente/cidadania/m1/sessoes/08/');await p.waitForTimeout(300);
  assert.equal(await p.locator('h1').count(),1);assert(await p.evaluate(()=>document.body.classList.contains('molde-cidadania')));
  assert.equal(await p.locator('[data-stage]').count(),0);assert.equal(await p.locator('[data-session-done]').count(),0);
  assert.equal(await p.locator('[data-c-num]').innerText(),'1/23');
  for(const [k,v] of Object.entries(legacy))assert.equal(await p.evaluate(k=>localStorage.getItem(k),k),v,k);}
 /* 07/11/2026 (decisões 166 a 168): a sessão 10, a sessão de mostra, passa também ao molde final, no mesmo endereço
    (tools/licoes/cidadania-m1-s10.json, variante «mostra»), com a chave epi-cid-m1-s10; exige-se o mesmo que às 01 a 08, com os seus
    14 cartões, e sai do ciclo abaixo. A 09 publicada continua com tudo o que se exigia. */
 {await p.goto(origin+'/lente/cidadania/m1/sessoes/10/');await p.waitForTimeout(300);
  assert.equal(await p.locator('h1').count(),1);assert(await p.evaluate(()=>document.body.classList.contains('molde-cidadania')));
  assert.equal(await p.locator('[data-stage]').count(),0);assert.equal(await p.locator('[data-session-done]').count(),0);
  assert.equal(await p.locator('[data-c-num]').innerText(),'1/14');
  for(const [k,v] of Object.entries(legacy))assert.equal(await p.evaluate(k=>localStorage.getItem(k),k),v,k);}
 /* 06/11/2026 (fusão do main com as sessões 2 e 3 finais): a 03 e a 04 passaram ao molde final; o ciclo começa na 05. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 4 finais na sessão 5): a 05 também passou ao molde final; o ciclo começa na 06. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 5 finais na sessão 6): a 06 também passou ao molde final; o ciclo começa na 07. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 6 finais na sessão 7): a 07 também passou ao molde final; o ciclo começa na 08. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 7 finais na sessão 8): a 08 também passou ao molde final; o ciclo começa na 09. */
 /* 07/11/2026 (sessão 10 no molde): a 10 também passou ao molde final; o ciclo fica só com a 09. */
 for(let n=9;n<=9;n++){
  await p.goto(origin+'/lente/cidadania/m1/sessoes/'+String(n).padStart(2,'0')+'/');
  assert.equal(await p.locator('h1').count(),1);
  const links=await p.locator('.c10 a').evaluateAll(es=>es.map(e=>e.href).filter(h=>h.startsWith(location.origin)));
  for(const href of links)assert.equal((await ctx.request.get(href)).status(),200,href);
  assert.equal(await p.locator('[data-stage]').count(),5);assert.equal(await p.locator('[data-session-done]').count(),n<=2?0:1);
 }
 await p.goto(origin+'/lente/cidadania/m1/sessoes/');/* 05/11/2026: decisão 146 (discussões em turma, trabalhos individuais): os sete grupos da sessão 03 passam a mostras curtas individuais. */assert((await p.locator('.c10').innerText()).includes('Mostras curtas individuais'));
 /* 06/11/2026 (decisões 166 a 168): a condução por passos, o registo e a retoma provam-se na sessão 04, a primeira que continua no
    molde publicado (a 03 passou ao molde final, sem passos nem registo). Para que o «Continuar» do módulo mostre o efeito do registo
    como antes (passa à sessão seguinte), a 03 fica semeada como feita no registo do percurso publicado; a seguir à 04, «Continuar»
    tem de levar à 05. */
 /* 06/11/2026 (fusão do main com as sessões 2 e 3 finais na sessão 4): a 04 também passou ao molde final; o mesmo prova-se na 05,
    agora a primeira que continua no molde publicado, com a 03 e a 04 semeadas como feitas; a seguir à 05, «Continuar» tem de
    levar à 06. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 4 finais na sessão 5): a 05 também passou ao molde final; o mesmo prova-se na 06,
    agora a primeira que continua no molde publicado, com a 03, a 04 e a 05 semeadas como feitas; a seguir à 06, «Continuar» tem de
    levar à 07. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 5 finais na sessão 6): a 06 também passou ao molde final; o mesmo prova-se na 07,
    agora a primeira que continua no molde publicado, com as 03 a 06 semeadas como feitas; a seguir à 07, «Continuar» tem de levar
    à 08. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 6 finais na sessão 7): a 07 também passou ao molde final; o mesmo prova-se na 08,
    agora a primeira que continua no molde publicado, com as 03 a 07 semeadas como feitas; a seguir à 08, «Continuar» tem de levar
    à 09. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 7 finais na sessão 8): a 08 também passou ao molde final; o mesmo prova-se na 09,
    agora a primeira que continua no molde publicado, com as 03 a 08 semeadas como feitas; a seguir à 09, «Continuar» tem de levar
    à 10. */
 await p.evaluate(k=>{let d=null;try{d=JSON.parse(localStorage.getItem(k)||'null')}catch(e){}if(!d||d.version!==2||!d.sessions)d={version:2,sessions:{}};d.sessions['03']={done:true};d.sessions['04']={done:true};d.sessions['05']={done:true};d.sessions['06']={done:true};d.sessions['07']={done:true};d.sessions['08']={done:true};localStorage.setItem(k,JSON.stringify(d))},KEY);
 await p.goto(origin+'/lente/cidadania/m1/sessoes/09/');assert.equal(await p.locator('[data-stage]:visible').count(),0);
 await p.locator('[data-start]').click();assert.equal(await p.locator('[data-stage]:visible').count(),1);
 await p.locator('[data-stage]:visible').focus();await p.keyboard.press('ArrowRight');assert.equal(await p.locator('[data-stage]:visible').getAttribute('id'),'momento-2');
 await p.locator('[data-stage-link]').nth(2).click();await p.locator('[data-feedback]>summary').focus();await p.keyboard.press('Enter');assert(await p.locator('[data-feedback]').evaluate(e=>e.open));
 await p.locator('[data-stage-link]').nth(4).click();await p.locator('[data-session-done]').check();await p.reload();assert(await p.locator('[data-session-done]').isChecked());
 assert.deepEqual(await p.evaluate(keys=>Object.fromEntries(keys.map(k=>[k,localStorage.getItem(k)])),Object.keys(legacy)),legacy);
 await p.goto(origin+'/lente/cidadania/m1/');assert((await p.locator('[data-continue]').getAttribute('href')).includes('10/'));/* 06/11/2026: a seguir à 05 (era a seguir à 04, «05/») */ /* 06/11/2026 (fusão na sessão 5): a seguir à 06, «07/» */ /* 06/11/2026 (fusão na sessão 6): a seguir à 07, «08/» */ /* 06/11/2026 (fusão na sessão 7): a seguir à 08, «09/» */ /* 06/11/2026 (fusão na sessão 8): a seguir à 09, «10/» */
 /* 06/11/2026 (fusão do main com as sessões 2 a 4 finais na sessão 5): a impressão completa e a projeção provavam-se na 06, uma
    sessão ainda por fazer; a 06 fica agora feita e retomada no passo 5 (acima), e a projeção retomava-a aí, sem «Seguinte». Passam
    à 07, a sessão seguinte ainda por fazer, com as mesmas exigências. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 5 finais na sessão 6): pela mesma razão, a 07 fica agora feita e retomada no passo
    5 (acima); a impressão completa e a projeção passam à 08, a sessão seguinte ainda por fazer, com as mesmas exigências. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 6 finais na sessão 7): pela mesma razão, a 08 fica agora feita e retomada no passo
    5 (acima); a impressão completa e a projeção passam à 09, a sessão seguinte ainda por fazer, com as mesmas exigências. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 7 finais na sessão 8): pela mesma razão, a 09 fica agora feita e retomada no passo
    5 (acima); a impressão completa e a projeção passam à 10, a sessão seguinte ainda por fazer, com as mesmas exigências. */
 /* 07/11/2026 (sessão 10 no molde): a 10 também passou ao molde final, e não fica nenhuma sessão do M1 no molde publicado ainda por
    fazer (a 09 fica feita e retomada no passo 5, acima). A impressão completa e a projeção passam, com as mesmas exigências, a uma
    sessão do M2 com o mesmo motor de cinco passos (cidadania/m2/sessoes/02/, chave lente-cidadania-m2-sessoes-v1): cinco passos à
    vista ao imprimir e um depois; na projeção, o registo desativado, sem deslocamento lateral nos três tamanhos, e nada gravado no
    aparelho (confere-se todo o armazenamento das lições, não só a chave do M1). */
 await p.goto(origin+'/lente/cidadania/m2/sessoes/02/');await p.locator('[data-start]').click();
 await p.evaluate(()=>dispatchEvent(new Event('beforeprint')));assert.equal(await p.locator('[data-stage]:visible').count(),5);
 await p.emulateMedia({media:'print'});await p.pdf({path:path.join(OUT,'sessao-m2-02-impressao.pdf'),format:'A4',printBackground:true});await p.emulateMedia({media:'screen'});await p.evaluate(()=>dispatchEvent(new Event('afterprint')));assert.equal(await p.locator('[data-stage]:visible').count(),1);
 /* 07/11/2026: o tamanho de letra que o próprio lançador da projeção guarda (epi-projection-text-size) fica de fora; tudo o resto,
    incluindo a chave do M1 que se conferia antes e a do M2, tem de ficar igual. */
 const tudo=()=>p.evaluate(()=>JSON.stringify(Object.keys(localStorage).filter(k=>k!=='epi-projection-text-size').sort().map(k=>[k,localStorage.getItem(k)])));
 const before=await tudo();
 await p.goto(origin+'/lente/projetar/?pagina=/lente/cidadania/m2/sessoes/02/');const f=p.frameLocator('#lesson-frame');await f.locator('[data-session-done]').waitFor({state:'attached'});assert(await f.locator('[data-session-done]').isDisabled());
 for(const size of ['small','medium','large']){await p.locator(`[data-projection-size="${size}"]`).click();assert(await f.locator('html').evaluate(e=>e.scrollWidth<=e.clientWidth));}
 await f.locator('[data-start]').click();await f.locator('[data-next]').click();assert.equal(await tudo(),before);await p.screenshot({path:path.join(OUT,'projecao.png')});
 await p.goto(origin+'/lente/cidadania/m1/#unidade-3');await p.waitForURL('**/sessoes/06/');
 assert.deepEqual(errors,[]);results.push({functions:'condução por momentos; teclado; impressão completa; retomada; estado legado intacto; projeção 3 tamanhos; âncoras antigas',passed:true});await ctx.close();
 for(const seed of ['{invalid','{"version":2,"sessions":[]}']){const c=await context(),q=await c.newPage();await q.goto(origin+'/lente/cidadania/m1/');await q.evaluate(([key,s])=>localStorage.setItem(key,s),[KEY,seed]);await q.reload();assert((await q.locator('[data-continue]').getAttribute('href')).includes('03/'));await c.close()}
 /* 06/11/2026 (decisões 166 a 168): o armazenamento bloqueado e a página sem JavaScript provam-se na sessão 04, pela mesma razão. */
 /* 06/11/2026 (fusão do main com as sessões 2 e 3 finais na sessão 4): e passam à 05, pela mesma razão. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 4 finais na sessão 5): e passam à 06, pela mesma razão. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 5 finais na sessão 6): e passam à 07, pela mesma razão. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 6 finais na sessão 7): e passam à 08, pela mesma razão. */
 /* 06/11/2026 (fusão do main com as sessões 2 a 7 finais na sessão 8): e passam à 09, pela mesma razão. */
 const c=await context(),q=await c.newPage();await c.addInitScript(()=>{Storage.prototype.getItem=function(){throw Error('blocked')};Storage.prototype.setItem=function(){throw Error('blocked')}});await q.goto(origin+'/lente/cidadania/m1/sessoes/09/');await q.locator('[data-start]').click();await q.locator('[data-stage-link]').nth(4).click();await q.locator('[data-session-done]').check();assert((await q.locator('[data-live]').textContent()).includes('não permite guardar'));await c.close();
 const no=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}}),np=await no.newPage();await np.goto(origin+'/lente/cidadania/m1/sessoes/09/');assert.equal(await np.locator('[data-stage]:visible').count(),5);await np.locator('[data-feedback]>summary').click();assert(await np.locator('[data-feedback] p').isVisible());await no.close();
 results.push({fallbacks:'estado inválido; armazenamento bloqueado; sem JavaScript',passed:true});fs.writeFileSync(path.join(OUT,'qa-browser.json'),JSON.stringify(results,null,2));console.log(JSON.stringify({observations:results.length,passed:true,output:OUT}));
}finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);server.close();process.exitCode=1});
