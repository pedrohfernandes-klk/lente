const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'..'),D=require('../assets/formas/corpus.json');
const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript','.json':'application/json','.css':'text/css','.png':'image/png','.webp':'image/webp','.woff2':'font/woff2'};
function fileFor(url){let name=decodeURIComponent(new URL(url,'http://localhost').pathname).replace(/^\/lente\//,'/');let f=path.resolve(ROOT,'.'+name);if(!f.startsWith(ROOT+path.sep))return null;try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');return f;}catch{return null;}}
const server=http.createServer((req,res)=>{const f=fileFor(req.url);if(!f){res.writeHead(404).end();return;}res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));});
async function run(){await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port;let b;
try{b=await chromium.launch({headless:true,...(process.env.PT_BROWSER_CHANNEL?{channel:process.env.PT_BROWSER_CHANNEL}:{})});
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
 await page.locator('[data-case="kafka"][data-answer="0"]').click();await page.locator('[data-check="kafka"]').click();assert.match(await page.locator('#kafka').innerText(),/Leitura sustentada/);
 await page.locator('[data-compare="kafka"]').click();assert.match(await page.locator('#kafka').innerText(),/nenhuma das duas frases é de Kafka/);
 await page.locator('#draft-kafka').fill('A minha tentativa <img src=x>');await page.locator('[data-filter="all"]').click();assert.equal(await page.locator('.lf-case').count(),10);assert.equal(await page.locator('#draft-kafka').inputValue(),'A minha tentativa <img src=x>');
 await page.locator('[data-filter="pt"]').click();assert.equal(await page.locator('.lf-case details[open]').count(),10);
 await page.locator('#projection').click();assert(await page.locator('#draft-kafka').isHidden());await page.locator('#projection').click();
 await page.goto(base+'/narrativas/formas/?mesa=pt');await page.locator('#gogol').waitFor();assert.equal(await page.locator('[data-filter="pt"]').getAttribute('aria-pressed'),'true');
 await page.goto(base+'/narrativas/');assert.match(await page.locator('h1').innerText(),/Laboratório de formas/);assert.equal(await page.locator('section.lab-set').count(),3);assert.match(await page.locator('[data-formas-progress]').innerText(),/4 de 4/);
 await page.goto(base+'/narrativas/corta/');assert.equal(await page.locator('.missoes a[data-id]').count(),8);
 if(process.env.LENTE_SHOTS){fs.mkdirSync(process.env.LENTE_SHOTS,{recursive:true});await page.goto(base+'/narrativas/');await page.screenshot({path:path.join(process.env.LENTE_SHOTS,'lente-entrada.png'),fullPage:true,animations:'disabled'});await page.goto(base+'/narrativas/corta/mesa/');await page.screenshot({path:path.join(process.env.LENTE_SHOTS,'lente-corta.png'),fullPage:true,animations:'disabled'});await page.locator('[data-phase="1"]').click();await page.locator('[data-preset]').click();await page.locator('#compare').click();await page.screenshot({path:path.join(process.env.LENTE_SHOTS,'lente-comparar.png'),fullPage:true,animations:'disabled'});await page.goto(base+'/narrativas/formas/');await page.locator('#kafka').waitFor();await page.screenshot({path:path.join(process.env.LENTE_SHOTS,'lente-obras.png'),fullPage:true,animations:'disabled'});}
 assert.deepEqual(errors,[]);assert.equal(D.items.filter(x=>x.status==='excerto-consultado').length,3);console.log('PASS source-backed reading experiments, drafts retained across filters, 10-source corpus, PT bridges, original routes and legacy progress; no browser errors');
 await ctx.close();
}finally{if(b)await b.close();await new Promise(r=>server.close(r));}}
run().catch(e=>{console.error(e);process.exitCode=1;});
