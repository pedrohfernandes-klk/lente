// 01/11/2026: contratos das famílias migradas em navegador real.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..');
const lab=fs.existsSync(path.join(root,'assets/laboratorio/cartaz.js'));
const entry=fs.readFileSync(path.join(root,'index.html'),'utf8').includes('data-cartaz-entrada');
const pages=[...(entry?['']:[]),...(lab?['narrativas/','narrativas/ver/','narrativas/treinar/','narrativas/criar/']:[])];
const server=http.createServer((req,res)=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname).replace(/^\/lente/,''));if(!f.startsWith(root+path.sep)&&f!==root){res.writeHead(403);return res.end();}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
// 02/11/2026: inclui o limite largo apontado na confirmação, sem retirar larguras anteriores.
try{for(const theme of ['light','dark'])for(const width of [320,390,1024,1366,1440])for(const pagePath of pages){
 const ctx=await browser.newContext({viewport:{width,height:900},colorScheme:theme});const page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.route('https://pedrohfernandes-klk.github.io/lente/**',async route=>{const u=new URL(route.request().url());const response=await ctx.request.get(origin+u.pathname+u.search);await route.fulfill({response});});
 await page.goto(origin+'/lente/'+pagePath,{waitUntil:'networkidle'});
 // 01/11/2026: 320 e 1024 px, títulos sem transbordo e retoma completa.
 assert.deepEqual(errors,[]);assert.equal(await page.locator('.cz-next').count(),1);
 assert.equal(await page.evaluate(()=>Math.max(0,document.documentElement.scrollWidth-innerWidth)),0,pagePath);
 for(const sel of ['.cz-next .cz-button','.cz-fold>summary'])for(const box of await page.locator(sel).all()){const r=await box.boundingBox();assert.ok(r.height>=(sel.includes('summary')?88:48),`${pagePath} ${sel}: ${r.height}`);}
 const clipped=await page.locator('.modulo h3').evaluateAll(es=>es.filter(e=>e.scrollWidth>e.clientWidth).map(e=>e.textContent));assert.deepEqual(clipped,[],'títulos dos percursos');
 if(entry&&pagePath===''&&width===390)assert.ok(await page.evaluate(()=>document.documentElement.scrollHeight)<3000,'entrada abaixo de 3000 px');
 if(pagePath.startsWith('narrativas/')){assert.ok(await page.locator('.cz-fold[open]').count()>=1,'banda do próximo passo aberta');assert.equal(await page.locator('.cz-state').filter({hasText:'por fazer'}).count(),0);}
 // 02/11/2026: regressões da confirmação, imagem sem caixa 3:2 e largura útil da legenda.
 if(pagePath==='narrativas/'&&width===390)assert.ok(await page.evaluate(()=>document.documentElement.scrollHeight)<3000,'Laboratório abaixo de 3000 px');
 if(pagePath.startsWith('narrativas/')&&width>=1024){
  const layout=await page.evaluate(()=>{const r=s=>document.querySelector(s).getBoundingClientRect();return {main:r('main').width,next:r('.cz-next').width,x:r('.cz-next').x,top:r('.topo').right,title:getComputedStyle(document.querySelector('.cz-next h2')).fontSize,folds:[...document.querySelectorAll('.unidade.cz-fold')].map(e=>e.getBoundingClientRect().width)};});
  assert.equal(layout.title,'25px');assert.ok(layout.x>=layout.top+23,'A seguir à direita da abertura');
  for(const w of layout.folds)assert.ok(Math.abs(w-(layout.main-32))<=1,'dobras ocupam toda a largura útil');
  if(pagePath!=='narrativas/'){
   const museum=await page.locator('main>.cz-museum').evaluate(e=>({height:e.getBoundingClientRect().height,caption:e.querySelector('figcaption').getBoundingClientRect().width,ratio:getComputedStyle(e.querySelector('img')).aspectRatio}));
   assert.ok(museum.caption>=240,JSON.stringify(museum));assert.ok(museum.height<=400,JSON.stringify(museum));assert.equal(museum.ratio,'auto');
  }
 }
 if(process.env.CARTAZ_CAPTURAS){await page.evaluate(async()=>{await Promise.all([...document.images].map(im=>{im.loading='eager';return im.decode().catch(()=>{});}));});fs.mkdirSync(process.env.CARTAZ_CAPTURAS,{recursive:true});await page.screenshot({path:path.join(process.env.CARTAZ_CAPTURAS,(pagePath.replaceAll('/','-')||'entrada')+width+'-'+theme+'.png'),fullPage:true});}
 await page.goto(origin+'/lente/'+pagePath+'?projetar=1',{waitUntil:'networkidle'});
 assert.equal(await page.locator('.cz-fold:not([open])').count(),0,'projeção');assert.deepEqual(errors,[]);assert.equal(await page.evaluate(()=>Math.max(0,document.documentElement.scrollWidth-innerWidth)),0,'projeção');
 // 02/11/2026: mede texto efetivamente visível, incluindo o lead e os rótulos das dobras.
 if(pagePath.startsWith('narrativas/'))assert.deepEqual(await page.locator('main').evaluate(main=>[...main.querySelectorAll('*')].filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())&&e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden').filter(e=>parseFloat(getComputedStyle(e).fontSize)<17.85).map(e=>({text:e.textContent.trim(),size:getComputedStyle(e).fontSize}))),[],'projeção sem texto abaixo de 17,9 px arredondados');
 await page.evaluate(()=>dispatchEvent(new Event('beforeprint')));await page.emulateMedia({media:'print'});
 assert.equal(await page.locator('.cz-fold:not([open])').count(),0,'impressão');
 await ctx.close();
 }
 const ctx=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}}),p=await ctx.newPage();
 for(const route of pages){await p.goto(origin+'/lente/'+route);assert.equal(await p.locator('.cz-fold:not([open])').count(),0,'sem JavaScript');
 // 02/11/2026: o botão sem JavaScript não repete o título, mas conserva o destino.
 if(route.startsWith('narrativas/'))assert.equal((await p.locator('.cz-next .continuar').textContent()).replace(/\s+/g,' '),'Começar →');}
 await ctx.close();
 if(lab){const ctx=await browser.newContext({viewport:{width:390,height:900}});const data=JSON.parse(fs.readFileSync(path.join(root,'assets/laboratorio/percursos.json'),'utf8')),item=data.pieces.find(p=>p.progress.kind==='feitas'),key=item.progress.key,id=item.progress.id;
 const value={feitas:{[id]:Date.UTC(2026,10,1,12)}};await ctx.addInitScript(({key,value})=>localStorage.setItem(key,JSON.stringify(value)),{key,value});
 const p=await ctx.newPage();await p.goto(origin+'/lente/narrativas/ver/#montagem',{waitUntil:'networkidle'});
 const label=p.locator('[data-estado="'+item.id+'"]');if(await label.count())assert.equal(await label.first().textContent(),'Feita 01/11');
 assert.equal(await p.evaluate(k=>localStorage.getItem(k),key),JSON.stringify(value));
 assert.equal(await p.locator('#montagem').count(),1);
 const closedAnchor=await p.evaluate(()=>{const target=document.getElementById(location.hash.slice(1));return target&&target.matches('details')&&!target.open;});assert.ok(!closedAnchor);
 await p.goto(origin+'/lente/narrativas/#criar',{waitUntil:'networkidle'});assert.ok(await p.locator('#criar .cz-fold').evaluate(e=>e.open));
 await ctx.close();}
 // 02/11/2026: o percurso atual recebe filete e quadrado, também na entrada geral.
 if(lab){for(const theme of ['light','dark']){const ctx=await browser.newContext({viewport:{width:1366,height:900},colorScheme:theme});await ctx.addInitScript(()=>localStorage.setItem('epi-narrativas',JSON.stringify({feitas:{'aula-forma':Date.UTC(2026,10,1,12),piramide:Date.UTC(2026,10,1,12)}})));const p=await ctx.newPage();await p.goto(origin+'/lente/narrativas/',{waitUntil:'networkidle'});const row=p.locator('.blocos .cz-row.current');assert.equal(await row.count(),1);assert.equal(await row.evaluate(e=>getComputedStyle(e).borderLeftWidth),'4px');assert.equal(await row.locator('.cz-state.current').textContent(),'A seguir');assert.equal(await row.locator('.cz-state').evaluate(e=>getComputedStyle(e,'::before').backgroundColor),await row.evaluate(e=>getComputedStyle(e).borderLeftColor));assert.deepEqual(await p.evaluate(()=>Object.keys(JSON.parse(localStorage.getItem('epi-narrativas')).feitas)),['aula-forma','piramide']);await ctx.close();}}
 if(entry){const ctx=await browser.newContext();await ctx.addInitScript(()=>localStorage.setItem('epi-narrativas',JSON.stringify({feitas:{'aula-forma':Date.UTC(2026,10,1,12)}})));const p=await ctx.newPage();await p.goto(origin+'/lente/',{waitUntil:'networkidle'});await p.waitForFunction(()=>document.querySelector('[data-cz-retoma]').textContent==='Continuar →');assert.ok((await p.locator('[data-cz-retoma]').getAttribute('href')).endsWith('narrativas/piramide/'));assert.deepEqual(await p.evaluate(()=>Object.keys(JSON.parse(localStorage.getItem('epi-narrativas')).feitas)),['aula-forma']);await ctx.close();}
 console.log('Família Cartaz: temas, alvos, dobras, projeção, impressão, sem JavaScript e progresso verificados.');
}finally{await browser.close();server.closeAllConnections();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
