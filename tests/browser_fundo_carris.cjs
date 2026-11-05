// 02/11/2026: nove cenários do desenho de Justiça e contratos do motor comum, sem substituir testes existentes.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),out=process.env.FUNDO_PROVAS;
const server=http.createServer((q,r)=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(q.url,'http://x').pathname).replace(/^\/lente/,''));if(!f.startsWith(root+path.sep)){r.writeHead(403);return r.end()}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');r.setHeader('content-type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.webp':'image/webp'})[path.extname(f)]||'application/octet-stream');r.end(fs.readFileSync(f))}catch{r.writeHead(404);r.end()}});
const measure=()=>{const f=document.querySelector('.jc-fundo'),r=f.getBoundingClientRect();return {height:r.height,width:r.width,left:r.left,overflow:Math.max(0,document.documentElement.scrollWidth-innerWidth),animations:f.getAnimations({subtree:true}).map(a=>({name:a.animationName,duration:a.effect.getTiming().duration,iterations:a.effect.getTiming().iterations})),background:getComputedStyle(f).backgroundColor,ink:getComputedStyle(f).color}};
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port,b=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})}),rows=[];
async function context(options){const ctx=await b.newContext(options);await ctx.route('**/*',async r=>{const u=new URL(r.request().url());if(u.origin===origin)return r.continue();if(u.hostname==='pedrohfernandes-klk.github.io'&&u.pathname.startsWith('/lente/'))return r.fulfill({response:await ctx.request.get(origin+u.pathname+u.search)});return r.abort()});return ctx}
try{
 for(const width of [320,390,1366])for(const mode of ['light','dark','projection']){
  const ctx=await context({viewport:{width,height:900},colorScheme:mode==='dark'?'dark':'light',reducedMotion:'no-preference'}),p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.clock.install();await p.goto(origin+'/lente/olhar-e-decidir/justica/'+(mode==='projection'?'?projetar=1':''),{waitUntil:'load'});
  const f=p.locator('.jc-fundo'),button=p.locator('[data-fundo-botao="jc"]');await f.scrollIntoViewIfNeeded();await p.waitForTimeout(80);
  const m=await p.evaluate(measure);assert.equal(m.overflow,0);assert.ok(m.height>=(width<640?232:360)&&m.height<=(width<640?300:440));
  if(width<640){assert.ok(Math.abs(m.width-width)<1);assert.ok(Math.abs(m.left)<1)}
  if(mode==='dark'){assert.equal(m.background,'rgba(0, 0, 0, 0)','fundo transparente integrado no tema')}
  const storage=await p.evaluate(()=>JSON.stringify({...localStorage}));
  if(mode==='projection'){assert.deepEqual(m.animations,[]);assert.ok(await button.isHidden());assert.ok(!await f.evaluate(e=>e.classList.contains('jc-anda')))}
  else{
   // 05/11/2026: decisão 142. A aproximação da fotografia e as duas vias, cada uma uma só vez, em 36 s.
   assert.deepEqual([...m.animations].sort((x,y)=>x.name.localeCompare(y.name)),[{name:'jc-aproxima',duration:36000,iterations:1},{name:'jc-via-a',duration:36000,iterations:1},{name:'jc-via-b',duration:36000,iterations:1}]);assert.equal(await button.textContent(),'Parar o desenho');
   // O desenho não muda caixas nem atravessa a agulha em nenhum instante do movimento.
   // 05/11/2026: decisão 142. Na colagem, o elétrico (marcado a tracejado na fotografia) fica sempre acima da agulha, e as
   // duas vias acabam iguais: nenhuma fica escolhida.
   // 05/11/2026: amostras sem pause()/play(): dentro da mesma tarefa o relógio do documento não anda, por isso cada leitura é a do
   // instante pedido; com pause()/play(), o Chromium mantém as animações CSS vivas depois de a classe sair.
   const samples=await f.evaluate(e=>{const anims=e.getAnimations({subtree:true});const data=[];for(const t of [0,3600,12000,21600,30000,35999,36000,36001,71999]){anims.forEach(a=>{a.currentTime=t});const alvo=e.querySelector('.jc-alvo').getBoundingClientRect(),ag=e.querySelector('.jc-agulha').getBoundingClientRect(),r=e.getBoundingClientRect();data.push({x:alvo.bottom,limit:ag.top,w:r.width,h:r.height,va:+getComputedStyle(e.querySelector('.jc-via-a')).opacity,vb:+getComputedStyle(e.querySelector('.jc-via-b')).opacity})}anims.forEach(a=>{a.currentTime=0});return data});
   // 03/11/2026: nos limites de 36 s e no repouso não há reinício nem salto.
   assert(samples.slice(-4).every(s=>Math.abs(s.x-samples[samples.length-1].x)<.01));
   for(const s of samples){assert.ok(s.x<s.limit);assert.equal(s.w,m.width);assert.equal(s.h,m.height)}
   for(const s of samples.slice(-4)){assert.equal(s.va,1);assert.equal(s.vb,1)}
   await button.focus();await p.keyboard.press('Enter');assert.equal(await f.evaluate(e=>e.getAnimations({subtree:true}).length),0);assert.equal(await button.textContent(),'Pôr o desenho a andar');
   await button.click();await p.clock.fastForward(72001);assert.equal(await f.evaluate(e=>e.getAnimations({subtree:true}).length),0,'pára depois de dois ciclos');assert.equal(await button.textContent(),'Pôr o desenho a andar');
   await button.click();await p.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))});assert.ok(await f.evaluate(e=>e.classList.contains('fundo-pausa')));assert.equal(await p.locator('.jc-eletrico').evaluate(e=>getComputedStyle(e).animationPlayState),'paused');
   await p.evaluate(()=>{delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))});await p.locator('main>nav').scrollIntoViewIfNeeded();await p.evaluate(()=>scrollTo(0,document.documentElement.scrollHeight));await p.waitForTimeout(80);assert.ok(await f.evaluate(e=>e.classList.contains('fundo-pausa')),'pausa fora do ecrã');await f.scrollIntoViewIfNeeded();await p.waitForTimeout(80);await button.click();
  }
  assert.equal(await p.evaluate(()=>JSON.stringify({...localStorage})),storage,'desenho não altera progresso');assert.deepEqual(errors,[]);
  if(out){fs.mkdirSync(out,{recursive:true});await f.scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,`justica-${width}-${mode}.png`),fullPage:true})}
  await p.emulateMedia({media:'print'});assert.ok(await f.isHidden());assert.ok(await button.isHidden());rows.push({width,mode,...m,errors});await ctx.close();console.log('PASS',width,mode);
 }
 for(const options of [{reducedMotion:'reduce'},{javaScriptEnabled:false}]){
  const ctx=await context({viewport:{width:390,height:844},...options}),p=await ctx.newPage();await p.goto(origin+'/lente/olhar-e-decidir/justica/');await p.locator('.jc-fundo').scrollIntoViewIfNeeded();assert.ok(await p.locator('.jc-fundo svg').isVisible());assert.ok(await p.locator('[data-fundo-botao="jc"]').isHidden());assert.equal(await p.locator('.jc-fundo').evaluate(e=>e.getAnimations({subtree:true}).length),0);await ctx.close();
 }
 // 05/11/2026: revisão de 5/11 (lente-justica-4). Ao recomeçar, a colagem parte do estado parado: a t=0 a fotografia ocupa o
 // mesmo retângulo que sem movimento (diferença < 0,01 px); antes encolhia de repente de 1,04 para 1.
 {const caixa=async reducedMotion=>{const ctx=await context({viewport:{width:1366,height:900},reducedMotion}),p=await ctx.newPage();await p.goto(origin+'/lente/olhar-e-decidir/justica/',{waitUntil:'load'});await p.locator('.jc-fundo').scrollIntoViewIfNeeded();await p.waitForTimeout(120);const r=await p.locator('.jc-fundo').evaluate(e=>{const anims=e.getAnimations({subtree:true});anims.forEach(a=>{a.currentTime=0});const q=e.querySelector('.jc-foto').getBoundingClientRect();return {n:anims.length,l:q.left,t:q.top,r:q.right,b:q.bottom}});await ctx.close();return r};
  const parado=await caixa('reduce'),arranque=await caixa('no-preference');assert.equal(parado.n,0);assert.equal(arranque.n,3);
  for(const k of ['l','t','r','b'])assert.ok(Math.abs(parado[k]-arranque[k])<.01,'salto ao recomeçar, '+k+': '+parado[k]+' contra '+arranque[k]);console.log('PASS recomeço sem salto')}
 // 05/11/2026: revisão de 5/11 (lente-justica-5). Entre 406 e 639 px, a faixa (até 300 px) subia por baixo da apresentação.
 for(const width of [420,480,600,639]){const ctx=await context({viewport:{width,height:900},reducedMotion:'reduce'}),p=await ctx.newPage();await p.goto(origin+'/lente/olhar-e-decidir/justica/');const g=await p.evaluate(()=>({lead:document.querySelector('.jc-abertura .lead').getBoundingClientRect().bottom,fundo:document.querySelector('.jc-fundo').getBoundingClientRect().top,sw:document.documentElement.scrollWidth-innerWidth}));assert.ok(g.lead<=g.fundo,'apresentação sobre a faixa a '+width+' px: '+JSON.stringify(g));assert.equal(g.sw,0);await ctx.close()}
 console.log('PASS apresentação acima da faixa a 420, 480, 600 e 639 px')
 const ctx=await context({viewport:{width:768,height:900},reducedMotion:'reduce'}),p=await ctx.newPage();await p.goto(origin+'/lente/olhar-e-decidir/justica/');assert.equal((await p.locator('.jc-fundo').boundingBox()).height,340);await ctx.close();
 if(out)fs.writeFileSync(path.join(out,'medidas.json'),JSON.stringify(rows,null,2));console.log('PASS 9 cenários; teclado, aproximação única, repouso, pausa, estado parado, impressão e tablet.');
}finally{await b.close();server.closeAllConnections();server.close()}})().catch(e=>{console.error(e);process.exitCode=1});
