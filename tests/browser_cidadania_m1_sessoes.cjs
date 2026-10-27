/* Dez sessões: desenho, condução, estado, tarefa protegida e projeção. */
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
const {chromium}=require('playwright');
const R=path.resolve(__dirname,'..'),OUT=path.resolve(R,'../../outputs/revisao-dez-sessoes');fs.mkdirSync(OUT,{recursive:true});
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
   assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${width} ${scheme} ${route}`);assert.deepEqual(errors,[],route);
   if(route==='cidadania/m1/'){assert.equal(await p.locator('[data-session-card]').count(),10);assert((await p.locator('[data-continue]').getAttribute('href')).includes('03/'));assert(await p.locator('.c10 .epi-projection-menu-link').isVisible());}
   if(width===1440&&scheme==='light'&&['cidadania/m1/','cidadania/m1/sessoes/03/','cidadania/m1/sessoes/06/'].includes(route))await p.screenshot({path:path.join(OUT,route==='cidadania/m1/'?'modulo.png':route.includes('03/')?'sessao-03.png':'sessao-06.png'),fullPage:true});
   if(width===390&&scheme==='dark'&&route==='cidadania/m1/sessoes/09/')await p.screenshot({path:path.join(OUT,'sessao-09-telemovel.png'),fullPage:true});
   results.push({route,width,scheme,overflow:false,errors:[]});
  }await ctx.close();
 }
 const ctx=await context(),p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));await p.goto(origin+'/lente/cidadania/m1/');
 const legacy={'epi-cidadania-m1':'{"feitas":{"passo-01":123}}','lente-justica-licao-1':'{"lida":true}','lente-cidadania-m1-v2':'{"version":2,"done":{"F01":true}}'};
 await p.evaluate(values=>{for(const [k,v]of Object.entries(values))localStorage.setItem(k,v)},legacy);
 for(let n=1;n<=10;n++){
  await p.goto(origin+'/lente/cidadania/m1/sessoes/'+String(n).padStart(2,'0')+'/');
  assert.equal(await p.locator('h1').count(),1);
  const links=await p.locator('.c10 a').evaluateAll(es=>es.map(e=>e.href).filter(h=>h.startsWith(location.origin)));
  for(const href of links)assert.equal((await ctx.request.get(href)).status(),200,href);
  assert.equal(await p.locator('[data-stage]').count(),n<=2?0:5);
 }
 await p.goto(origin+'/lente/cidadania/m1/sessoes/03/');assert((await p.locator('.c10').innerText()).includes('sete grupos'));
 await p.locator('[data-focus-mode]').click();assert.equal(await p.locator('[data-stage]:visible').count(),1);
 await p.locator('[data-stage]:visible').focus();await p.keyboard.press('ArrowRight');assert.equal(await p.locator('[data-stage]:visible').getAttribute('id'),'momento-2');
 await p.locator('[data-stage-link]').nth(2).click();await p.locator('[data-feedback]>summary').focus();await p.keyboard.press('Enter');assert(await p.locator('[data-feedback]').evaluate(e=>e.open));
 await p.locator('[data-session-done]').check();await p.reload();assert(await p.locator('[data-session-done]').isChecked());
 assert.deepEqual(await p.evaluate(keys=>Object.fromEntries(keys.map(k=>[k,localStorage.getItem(k)])),Object.keys(legacy)),legacy);
 await p.goto(origin+'/lente/cidadania/m1/');assert((await p.locator('[data-continue]').getAttribute('href')).includes('04/'));
 await p.goto(origin+'/lente/cidadania/m1/sessoes/06/');await p.locator('[data-focus-mode]').click();
 await p.evaluate(()=>dispatchEvent(new Event('beforeprint')));assert.equal(await p.locator('[data-stage]:visible').count(),5);
 await p.emulateMedia({media:'print'});await p.pdf({path:path.join(OUT,'sessao-06-impressao.pdf'),format:'A4',printBackground:true});await p.emulateMedia({media:'screen'});await p.evaluate(()=>dispatchEvent(new Event('afterprint')));assert.equal(await p.locator('[data-stage]:visible').count(),1);
 const before=await p.evaluate(k=>localStorage.getItem(k),KEY);
 await p.goto(origin+'/lente/projetar/?pagina=/lente/cidadania/m1/sessoes/06/');const f=p.frameLocator('#lesson-frame');await f.locator('[data-session-done]').waitFor();assert(await f.locator('[data-session-done]').isDisabled());
 for(const size of ['small','medium','large']){await p.locator(`[data-projection-size="${size}"]`).click();assert(await f.locator('html').evaluate(e=>e.scrollWidth<=e.clientWidth));}
 await f.locator('[data-focus-mode]').click();await f.locator('[data-next]').click();assert.equal(await p.evaluate(k=>localStorage.getItem(k),KEY),before);await p.screenshot({path:path.join(OUT,'projecao.png')});
 await p.goto(origin+'/lente/cidadania/m1/#unidade-3');await p.waitForURL('**/sessoes/06/');
 assert.deepEqual(errors,[]);results.push({functions:'condução por momentos; teclado; impressão completa; retomada; estado legado intacto; projeção 3 tamanhos; âncoras antigas',passed:true});await ctx.close();
 for(const seed of ['{invalid','{"version":2,"sessions":[]}']){const c=await context(),q=await c.newPage();await q.goto(origin+'/lente/cidadania/m1/');await q.evaluate(([key,s])=>localStorage.setItem(key,s),[KEY,seed]);await q.reload();assert((await q.locator('[data-continue]').getAttribute('href')).includes('03/'));await c.close()}
 const c=await context(),q=await c.newPage();await c.addInitScript(()=>{Storage.prototype.getItem=function(){throw Error('blocked')};Storage.prototype.setItem=function(){throw Error('blocked')}});await q.goto(origin+'/lente/cidadania/m1/sessoes/03/');await q.locator('[data-session-done]').check();assert((await q.locator('[data-live]').textContent()).includes('não permite guardar'));await c.close();
 const no=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}}),np=await no.newPage();await np.goto(origin+'/lente/cidadania/m1/sessoes/03/');assert.equal(await np.locator('[data-stage]:visible').count(),5);await np.locator('[data-feedback]>summary').click();assert(await np.locator('[data-feedback] p').isVisible());await no.close();
 results.push({fallbacks:'estado inválido; armazenamento bloqueado; sem JavaScript',passed:true});fs.writeFileSync(path.join(OUT,'qa-browser.json'),JSON.stringify(results,null,2));console.log(JSON.stringify({observations:results.length,passed:true,output:OUT}));
}finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);server.close();process.exitCode=1});
