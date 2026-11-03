// 03/11/2026: projeção não consulta nem expõe o estado pessoal, incluindo estado prévio.
const fs=require('fs'),path=require('path'),assert=require('node:assert/strict'),{chromium}=require('playwright');
const root=path.resolve(__dirname,'..'),base='https://pedrohfernandes-klk.github.io/lente/',key='lente-cidadania-m2-sessoes-v1';
const seed=JSON.stringify({version:1,sessions:{'01':{done:true,stage:4},'02':{done:true,stage:3},'03':{done:false,stage:2}}});
(async()=>{const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});let count=0;
try{for(const width of [320,1366])for(const mode of ['normal','parametro','visor']){
 const c=await browser.newContext({viewport:{width,height:900}});
 await c.route('**/*',r=>{const u=r.request().url();if(!u.startsWith(base))return r.abort();let f=decodeURIComponent(u.slice(base.length).split(/[?#]/)[0]);if(!f||f.endsWith('/'))f+='index.html';f=path.resolve(root,f);if(!f.startsWith(root+path.sep)||!fs.existsSync(f))return r.fulfill({status:404,body:''});return r.fulfill({body:fs.readFileSync(f),contentType:({'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml'})[path.extname(f)]||'application/octet-stream'});});
 await c.addInitScript(({key,seed})=>{if(!sessionStorage.getItem('qa-iniciado')){localStorage.setItem(key,seed);sessionStorage.setItem('qa-iniciado','1');}window.qaAcessos=[];window.qaLerOriginal=Storage.prototype.getItem;for(const method of ['getItem','setItem','removeItem','clear']){const original=Storage.prototype[method];Storage.prototype[method]=function(...args){if(this===localStorage&&(args[0]===key||method==='clear'))qaAcessos.push({method,key:args[0]});return original.apply(this,args);};}},{key,seed});
 const p=await c.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
 for(const route of ['cidadania/m2/','cidadania/m2/sessoes/01/']){
  await p.goto(mode==='visor'?base+'projetar/?pagina=/lente/'+route:base+route+(mode==='parametro'?'?projetar=1':''));
  let surface=p;if(mode==='visor'){await p.frameLocator('#lesson-frame').locator('[data-c10]').waitFor();surface=p.frames().find(f=>f!==p.mainFrame()&&f.url().includes(route));}
  await surface.locator('[data-c10]').waitFor();
  const projected=mode!=='normal';const start=surface.locator('[data-start]');
  const observed={mode,width,route,access:await surface.evaluate(()=>qaAcessos),start:await start.count()?await start.textContent():null,count:await surface.locator('[data-count]').count()?await surface.locator('[data-count]').textContent():null};
  if(projected)assert.deepEqual(observed.access,[],JSON.stringify(observed));
  if(await start.count()){
   assert.equal(await start.textContent(),projected?'Começar':'Retomar no passo 5');
   await start.click();assert.equal(await surface.locator('[data-position]').textContent(),projected?'1 / 5':'5 / 5');
   if(projected){await surface.locator('[data-next]').click();assert.equal(await surface.locator('[data-position]').textContent(),'2 / 5');}
   else{await surface.locator('[data-prev]').click();await p.reload();assert.equal(await p.locator('[data-start]').textContent(),'Retomar no passo 4');}
  }else{
   assert.equal(await surface.locator('[data-count]').textContent(),projected?'':'2 registos de trabalho');
   assert.equal(await surface.locator('[data-continue]').textContent(),projected?'Começar na sessão 01':'Continuar na sessão 03');
   assert.equal(await surface.locator('[data-session-card][data-complete="true"]').count(),projected?0:2);
  }
  if(projected){await surface.evaluate(key=>{dispatchEvent(new StorageEvent('storage',{key}));dispatchEvent(new Event('pageshow'));},key);assert.deepEqual(await surface.evaluate(()=>qaAcessos),[]);assert.equal(await surface.evaluate(key=>qaLerOriginal.call(localStorage,key),key),seed);}
  assert.deepEqual(errors,[]);count++;
 }
 await c.close();
}console.log('PASS',count,'contextos: estado prévio, projeção sem leitura/escrita/exposição e retoma normal');}
finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
