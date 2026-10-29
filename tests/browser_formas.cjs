const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'..'),D=require('../assets/formas/corpus.json');
const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript','.json':'application/json','.css':'text/css','.png':'image/png','.webp':'image/webp','.woff2':'font/woff2'};
function fileFor(url){let name=decodeURIComponent(new URL(url,'http://localhost').pathname).replace(/^\/lente\//,'/');let f=path.resolve(ROOT,'.'+name);if(!f.startsWith(ROOT+path.sep))return null;try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');return f;}catch{return null;}}
const server=http.createServer((req,res)=>{const f=fileFor(req.url);if(!f){res.writeHead(404).end();return;}res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));});
global.window={};require('../assets/formas/leituras.js');for(const [id,g] of Object.entries(window.LenteLeituras)){const source=D.items.find(x=>x.id===id);assert.equal(source.status,'excerto-consultado');for(const [anchor] of g.anchors)assert(source.quote.includes(anchor));}
async function run(){await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port;let b;
try{b=await chromium.launch({headless:true,...(process.env.PT_BROWSER_EXECUTABLE?{executablePath:process.env.PT_BROWSER_EXECUTABLE}:{}),...(process.env.PT_BROWSER_CHANNEL?{channel:process.env.PT_BROWSER_CHANNEL}:{})});
 const ctx=await b.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
 await ctx.route('https://fonts.googleapis.com/**',r=>r.abort());await ctx.route('https://fonts.gstatic.com/**',r=>r.abort());
 await ctx.route('https://pedrohfernandes-klk.github.io/lente/**',route=>{const f=fileFor(route.request().url());if(f)route.fulfill({path:f,contentType:mime[path.extname(f)]||'application/octet-stream'});else route.abort();});
 const page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 for(const width of [360,1440]){
  await page.setViewportSize({width,height:1000});await page.goto(base+'/narrativas/corta/mesa/');await page.evaluate(()=>{window.print=()=>{};localStorage.setItem('epi-corta',JSON.stringify({feitas:{maias:123},nota:'preservar'}));});
  for(let mission=0;mission<4;mission++){
   await page.locator(`[data-mission="${mission}"]`).click();
   assert.equal(await page.locator('#mesa h2').innerText(),['Curiosidade','Suspense','Surpresa','Julgamento'][mission]);
   if(mission===0){const a=await page.locator('figcaption').innerText();await page.locator('[data-frame="A"][data-dir="1"]').click();assert.notEqual(await page.locator('figcaption').innerText(),a);await page.locator('#prediction').fill('<script>hipótese privada</script>');}
   await page.locator('[data-phase="1"]').click();assert(await page.locator('#compare').isDisabled());
   await page.locator('[data-add="0"]').click();await page.locator('[data-remove="0"]').click();assert.equal(await page.locator('.lf-cutlist li').count(),0);
   await page.locator('[data-preset]').click();
   if(mission===0){await page.locator('[data-move="0"][data-dir="1"]').click();await page.locator('#compare').click();assert(await page.getByRole('alert').isVisible());await page.locator('[data-preset]').click();}
   await page.locator('#compare').click();assert.equal(await page.locator('.lf-compare .lf-frame').count(),2);
   await page.locator('#knowledge').click();assert(await page.locator('.lf-knowledge dl').isVisible());const known=await page.locator('.lf-knowledge dd').nth(1).innerText();assert.match(known,mission===0?/Já viste a entrega/:mission===2?/Ainda não viste a perda/:/Viste a perda/);
   const before=await page.locator('.lf-compare section').nth(1).innerText();await page.locator('#omit').selectOption({index:1});assert.equal(await page.locator('.lf-countercut .lf-frame').count(),1);await page.locator('[data-frame="C"][data-dir="1"]').click();assert.equal(await page.locator('.lf-compare section').nth(1).innerText(),before);

   await page.locator('[data-choice="1"]').focus();await page.keyboard.press('Space');await page.locator('#explain').click();assert.match(await page.locator('#discovery').innerText(),/Testa esta distinção/);
   await page.locator('[data-choice="0"]').click();await page.locator('#explain').click();assert.match(await page.locator('#discovery').innerText(),/Uma leitura sustentada/);
   await page.locator('[data-phase="3"]').click();assert(await page.locator('#finish').isDisabled());
   await page.locator('#transfer').fill('<b>tentativa privada</b>');await page.locator('#reflection').fill('Mudei a informação disponível antes do mesmo gesto.');
   await page.locator('#projection').click();assert(await page.locator('#transfer').isHidden());assert(await page.locator('#reflection').isHidden());await page.locator('#projection').click();
   await page.locator('#print').click();assert(!/privada|Mudei a informação/.test(await page.locator('#print-sheet').innerText()));
   await page.locator('#finish').click();assert(await page.locator('#registered').isVisible());
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   const saved=await page.evaluate(()=>JSON.parse(localStorage.getItem('lente-formas-corta-v1')));assert(!JSON.stringify(saved).includes('privada'));
  }
  assert.match(await page.locator('#progress-label').innerText(),/4 de 4/);await page.reload();assert.match(await page.locator('#progress-label').innerText(),/4 de 4/);
  assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('epi-corta')).nota),'preservar');
  console.log('PASS four complete montage missions, rules, compare, reflection, print/projection privacy, persistent practice stamps, keyboard and layout at '+width+'px');
 }
 await page.goto(base+'/narrativas/corta/mesa/?experiencia=suspense&projetar=1');assert.equal(await page.locator('#mesa h2').innerText(),'Suspense');assert.equal(await page.locator('#projection').getAttribute('aria-pressed'),'true');
 await page.goto(base+'/narrativas/formas/');await page.locator('#kafka').waitFor();assert.equal(await page.locator('.lf-case').count(),3);
 for(const width of [360,1440]){
 await page.setViewportSize({width,height:1000});await page.goto(base+'/narrativas/formas/');await page.locator('#kafka').waitFor();
 for(const id of ['kafka','mia','cesariny']){
  await page.locator('[data-open="'+id+'"]').click();const c=page.locator('#'+id);
  await c.locator('[data-anchor="0"]').focus();await page.keyboard.press('Space');assert.equal(await c.locator('[data-anchor="0"]').getAttribute('aria-pressed'),'true');
  await c.locator('.lf-levels [data-level="1"]').click();await c.locator('[data-hypothesis="1"]').click();await c.locator('[data-write="reason"]').fill('Leio assim porque encontro esta expressão.');await c.locator('select').selectOption('com apoio');
  await c.locator('.lf-levels [data-level="2"]').click();await c.locator('[data-write="counter"]').fill('A objeção é possível, mas tem limites.');await c.locator('[data-model]').click();assert.equal(await c.locator('[data-model]').getAttribute('aria-expanded'),'true');
  await c.locator('.lf-levels [data-level="3"]').click();await c.locator('[data-compare]').click();const original=await c.locator('.lf-original').innerText();await c.locator('[data-version="1"]').click();assert.notEqual(await c.locator('.lf-original').innerText(),original);
  await c.locator('[data-write="draft"]').fill('Primeira tentativa <img src=x>');await c.locator('[data-keep]').click();await c.locator('[data-write="draft"]').fill('Versão revista');page.once('dialog',d=>d.dismiss());await c.locator('[data-reset]').click();assert.equal(await c.locator('[data-write="draft"]').inputValue(),'Versão revista');assert.match(await c.locator('.lf-first').innerText(),/<img src=x>/);assert.equal(await c.locator('.lf-first img').count(),0);
  await c.locator('[data-write="reflection"]').fill('Mudei o ponto de vista.');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.locator('#projection').click();assert(await c.locator('.lf-first').isHidden());assert(await c.locator('[data-write="draft"]').isHidden());await page.locator('#projection').click();
  await c.locator('.lf-levels [data-level="1"]').click();assert.equal(await c.locator('[data-write="reason"]').inputValue(),'Leio assim porque encontro esta expressão.');await c.locator('.lf-levels [data-level="3"]').click();assert.equal(await c.locator('[data-write="draft"]').inputValue(),'Versão revista');
 }
 await page.locator('[data-filter="all"]').click();assert.equal(await page.locator('.lf-case').count(),10);await page.locator('[data-filter="pt"]').click();assert.equal(await page.locator('.lf-case .lf-pt[open]').count(),10);assert.equal(await page.locator('#cesariny [data-write="draft"]').inputValue(),'Versão revista');
 console.log('PASS four interpretation levels, evidence, competing hypotheses, counter-reading and draft revision at '+width+'px');
 }
 await page.reload();await page.locator('#kafka').waitFor();assert.equal(await page.locator('[data-write="draft"]').count(),0);
 await page.goto(base+'/narrativas/formas/?mesa=pt');await page.locator('#gogol').waitFor();assert.equal(await page.locator('[data-filter="pt"]').getAttribute('aria-pressed'),'true');
 await page.goto(base+'/narrativas/');assert.match(await page.locator('h1').innerText(),/Laboratório de formas/);assert.equal(await page.locator('section.lab-set').count(),3);assert.match(await page.locator('[data-formas-progress]').innerText(),/4 de 4/);
 await page.goto(base+'/narrativas/corta/');assert.equal(await page.locator('.missoes a[data-id]').count(),8);
 if(process.env.LENTE_SHOTS){fs.mkdirSync(process.env.LENTE_SHOTS,{recursive:true});await page.goto(base+'/narrativas/');await page.screenshot({path:path.join(process.env.LENTE_SHOTS,'lente-entrada.png'),fullPage:true,animations:'disabled'});await page.goto(base+'/narrativas/corta/mesa/');await page.screenshot({path:path.join(process.env.LENTE_SHOTS,'lente-corta.png'),fullPage:true,animations:'disabled'});await page.locator('[data-phase="1"]').click();await page.locator('[data-preset]').click();await page.locator('#compare').click();await page.screenshot({path:path.join(process.env.LENTE_SHOTS,'lente-comparar.png'),fullPage:true,animations:'disabled'});await page.goto(base+'/narrativas/formas/');await page.locator('#kafka').waitFor();await page.screenshot({path:path.join(process.env.LENTE_SHOTS,'lente-obras.png'),fullPage:true,animations:'disabled'});}
 if(process.env.LENTE_PREVIEW_DIR){
  const {pathToFileURL}=require('node:url');await page.goto(pathToFileURL(path.join(process.env.LENTE_PREVIEW_DIR,'obras-para-experimentar.html')).href);await page.locator('#kafka').waitFor();await page.locator('#kafka [data-anchor="0"]').click();await page.locator('#kafka .lf-levels [data-level="3"]').click();await page.locator('#kafka [data-compare]').click();assert(await page.locator('.lf-original').isVisible());await page.goto(pathToFileURL(path.join(process.env.LENTE_PREVIEW_DIR,'corta.html')).href);await page.locator('[data-phase="1"]').click();await page.locator('[data-preset]').click();await page.locator('#compare').click();await page.locator('#omit').selectOption({index:1});assert(await page.locator('[data-frame="C"]').first().isVisible());console.log('PASS standalone file previews without a server');
 }
 assert.deepEqual(errors,[]);assert.equal(D.items.filter(x=>x.status==='excerto-consultado').length,3);console.log('PASS source-backed reading experiments, drafts retained across filters, 10-source corpus, PT bridges, original routes and legacy progress; no browser errors');
 await ctx.close();
}finally{if(b)await b.close();await new Promise(r=>server.close(r));}}
run().catch(e=>{console.error(e);process.exitCode=1;});
