// 02/11/2026: nove cenários do desenho de Justiça e contratos do motor comum, sem substituir testes existentes.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),out=process.env.FUNDO_PROVAS;
const server=http.createServer((q,r)=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(q.url,'http://x').pathname).replace(/^\/lente/,''));if(!f.startsWith(root+path.sep)){r.writeHead(403);return r.end()}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');r.setHeader('content-type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.webp':'image/webp'})[path.extname(f)]||'application/octet-stream');r.end(fs.readFileSync(f))}catch{r.writeHead(404);r.end()}});
// 06/11/2026: decisão 170. A cena neutra (o desenho parado): alavanca a direito, lâminas encostadas, as duas vias acesas, nenhum sinal.
// 07/11/2026: decisão 175, os sinais saíram (a lista tem de vir vazia) e o elétrico fica no sítio onde descansa (sem transform).
const neutra=e=>({braco:getComputedStyle(e.querySelector('.jc-alavanca-braco')).transform,laminas:[...e.querySelectorAll('.jc-agulha>path')].map(n=>getComputedStyle(n).transform),vias:[...e.querySelectorAll('.jc-via')].map(n=>getComputedStyle(n).opacity),sinais:[...e.querySelectorAll('.jc-sinal')].map(n=>getComputedStyle(n).opacity),carro:getComputedStyle(e.querySelector('.jc-carro')).transform}),NEUTRA={braco:'none',laminas:['none','none'],vias:['1','1'],sinais:[],carro:'none'};
// 07/11/2026: decisão 175. O crédito atrás do «i»: fechado ou aberto, visível ou não, e «Parar o desenho» fora dele.
const credito=()=>{const d=document.querySelector('.jc-acoes details.info-i'),s=d.querySelector('summary'),t=d.querySelector('.info-i-texto'),b=document.querySelector('[data-fundo-botao="jc"]'),r=t.getBoundingClientRect(),rb=b.getBoundingClientRect();return {aberto:d.open,nome:s.getAttribute('aria-label'),textoVisivel:r.width>0&&r.height>0&&t.checkVisibility({visibilityProperty:true,opacityProperty:true}),texto:t.textContent,botaoFora:!d.contains(b),botaoVisivel:!b.hidden&&rb.width>0&&rb.height>0,iVisivel:s.getBoundingClientRect().width>0&&s.checkVisibility({visibilityProperty:true})}};
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
  if(mode==='projection'){assert.deepEqual(m.animations,[]);assert.ok(await button.isHidden());{const c=await p.evaluate(credito);assert.ok(!c.aberto&&!c.textoVisivel&&c.iVisivel,'07/11/2026: decisão 175, na projeção o «i» fica fechado e à vista')}assert.ok(!await f.evaluate(e=>e.classList.contains('jc-anda')));assert.deepEqual(await f.evaluate(neutra),NEUTRA,'projeção: cena neutra')}
  else{
   // 05/11/2026: decisão 142. A aproximação da fotografia e as duas vias, cada uma uma só vez, em 36 s.
   // 06/11/2026: decisão 170. Lista fechada: mais a alavanca, as duas lâminas e os quatro sinais de alerta, todos uma só vez em 36 s.
   // 07/11/2026: decisão 175, saem os quatro sinais de alerta e entra o elétrico que avança (jc-avanca), também uma só vez em 36 s.
   assert.deepEqual([...m.animations].sort((x,y)=>x.name.localeCompare(y.name)),['jc-agulha-longe','jc-agulha-perto','jc-alavanca','jc-aproxima','jc-avanca','jc-via-a','jc-via-b'].map(name=>({name,duration:36000,iterations:1})));assert.equal(await button.textContent(),'Parar o desenho');
   // 07/11/2026: decisão 175. O «i» fechado ao carregar; «Parar o desenho» à vista e fora dele enquanto o desenho anda; o «i»
   // abre com o teclado (Enter) e mostra o crédito inteiro; o botão continua à vista; Escape fecha e devolve o foco ao «i».
   {const c0=await p.evaluate(credito);assert.equal(c0.aberto,false,'o «i» fechado ao carregar');assert.equal(c0.textoVisivel,false);assert.equal(c0.nome,'Créditos da colagem');assert.ok(c0.botaoFora&&c0.botaoVisivel&&c0.iVisivel,'botão e «i» à vista, o botão fora do «i»: '+JSON.stringify(c0));
    await p.locator('.jc-acoes summary').focus();await p.keyboard.press('Enter');await p.waitForTimeout(250);const c1=await p.evaluate(credito);assert.ok(c1.aberto&&c1.textoVisivel,'o «i» abre com Enter');assert.match(c1.texto,/Philip Mallis/);assert.match(c1.texto,/CC BY-SA 4\.0/);assert.match(c1.texto,/Grafismo gerado com recurso a IA, EPI, 2026\./);assert.doesNotMatch(c1.texto,/sinais de alerta/);assert.ok(c1.botaoFora&&c1.botaoVisivel,'aberto o «i», «Parar o desenho» continua à vista e fora dele');
    assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth),0,'o crédito aberto não alarga a página');
    await p.keyboard.press('Escape');await p.waitForTimeout(150);assert.equal((await p.evaluate(credito)).aberto,false,'Escape fecha o «i»');assert.ok(await p.evaluate(()=>document.activeElement&&document.activeElement.matches('.jc-acoes summary')),'o foco volta ao «i»')}
   // O desenho não muda caixas nem atravessa a agulha em nenhum instante do movimento.
   // 05/11/2026: decisão 142. Na colagem, o elétrico (marcado a tracejado na fotografia) fica sempre acima da agulha, e as
   // duas vias acabam iguais: nenhuma fica escolhida.
   // 05/11/2026: amostras sem pause()/play(): dentro da mesma tarefa o relógio do documento não anda, por isso cada leitura é a do
   // instante pedido; com pause()/play(), o Chromium mantém as animações CSS vivas depois de a classe sair.
   // 07/11/2026: decisão 175. Sem o tracejado (jc-alvo), mede-se a própria fotografia do elétrico, no sentido em que ele anda (para
   // a esquerda): o lado esquerdo da imagem fica sempre à direita da agulha (nunca lá chega) e, nos limites e no repouso, parado.
   const samples=await f.evaluate(e=>{const anims=e.getAnimations({subtree:true});const data=[];for(const t of [0,3600,12000,21600,30000,35999,36000,36001,71999]){anims.forEach(a=>{a.currentTime=t});const foto=e.querySelector('.jc-foto').getBoundingClientRect(),ag=e.querySelector('.jc-agulha').getBoundingClientRect(),r=e.getBoundingClientRect();data.push({x:foto.left,y:foto.bottom,limit:ag.right,w:r.width,h:r.height,va:+getComputedStyle(e.querySelector('.jc-via-a')).opacity,vb:+getComputedStyle(e.querySelector('.jc-via-b')).opacity})}anims.forEach(a=>{a.currentTime=0});return data});
   // 03/11/2026: nos limites de 36 s e no repouso não há reinício nem salto.
   assert(samples.slice(-4).every(s=>Math.abs(s.x-samples[samples.length-1].x)<.01&&Math.abs(s.y-samples[samples.length-1].y)<.01));
   for(const s of samples){assert.ok(s.x>s.limit,'o elétrico chegou à agulha: '+s.x+' contra '+s.limit);assert.equal(s.w,m.width);assert.equal(s.h,m.height)}
   for(const s of samples.slice(-4)){assert.equal(s.va,1);assert.equal(s.vb,1)}
   // 06/11/2026: decisão 170. A alavanca vai à direita (a via a direito pisca, a outra fica a 0,25), volta ao meio, vai à esquerda
   // (pisca a via que curva) e acaba ao meio; o pé da haste fica sempre em cima da base; os sinais surgem e apagam-se; tudo o que
   // mexe fica dentro da faixa (no telemóvel, o recorte do meio da cena); no fim e no repouso, a cena neutra do desenho parado.
   const passos=await f.evaluate(e=>{const anims=e.getAnimations({subtree:true}),svg=e.querySelector('svg'),braco=e.querySelector('.jc-alavanca-braco'),haste=braco.querySelector('path'),base=e.querySelector('.jc-alavanca>path');const ponto=(el,x,y)=>{const q=svg.createSVGPoint();q.x=x;q.y=y;return q.matrixTransform(el.getScreenCTM())};const data=[];for(const t of [0,5000,7200,9000,9540,12000,15500,18180,18720,21000,24500,30000,36000,71999]){anims.forEach(a=>{a.currentTime=t});const r=e.getBoundingClientRect(),tr=getComputedStyle(braco).transform,mm=new DOMMatrix(tr==='none'?undefined:tr),pe=ponto(haste,563,548),pb=ponto(base,563,548),foto=e.querySelector('.jc-foto').getBoundingClientRect(),tc=getComputedStyle(e.querySelector('.jc-carro')).transform,carro=new DOMMatrix(tc==='none'?undefined:tc),fora=[...e.querySelectorAll('.jc-alavanca,.jc-agulha')].filter(n=>{const q=n.getBoundingClientRect();return q.left<r.left-.5||q.right>r.right+.5||q.top<r.top-.5||q.bottom>r.bottom+.5}).map(n=>n.getAttribute('class'));if(foto.left<r.left-.5||foto.left>r.right+.5)fora.push('frente do elétrico');data.push({t,tx:Math.round(carro.e*100)/100,ty:carro.f,ang:Math.round(Math.atan2(mm.b,mm.a)*1800/Math.PI)/10,va:+getComputedStyle(e.querySelector('.jc-via-a')).opacity,vb:+getComputedStyle(e.querySelector('.jc-via-b')).opacity,sinais:[...e.querySelectorAll('.jc-sinal')].map(n=>Math.round(+getComputedStyle(n).opacity*100)/100),pe:Math.hypot(pe.x-pb.x,pe.y-pb.y),fora})}anims.forEach(a=>{a.currentTime=0});return data});
   const em=t=>passos.find(x=>x.t===t),perto=(a,b,msg)=>assert.ok(Math.abs(a-b)<.02,msg+': '+a+' em vez de '+b);
   // 07/11/2026: decisão 175. Na lista do que tem de ficar dentro da faixa, os sinais dão lugar à frente do elétrico.
   for(const x of passos){assert.ok(x.pe<.5,'o pé da haste saiu da base aos '+x.t+' ms: '+x.pe);assert.deepEqual(x.fora,[],'fora da faixa aos '+x.t+' ms a '+width+' px')}
   // 07/11/2026: decisão 175. O elétrico começa 80 unidades atrás, fica quieto enquanto o desenho entra, avança devagar só para a
   // esquerda (nunca recua nem sobe ou desce) e chega ao sítio onde descansa quando a alavanca volta ao meio (24,5 s).
   perto(em(0).tx,80,'elétrico atrás no começo');assert.ok(em(5000).tx<80&&em(5000).tx>70,'a começar a andar aos 5 s: '+em(5000).tx);assert.ok(em(12000).tx<em(9540).tx&&em(9540).tx<em(5000).tx,'avança');
   for(const [a,b] of passos.slice(0,-1).map((x,i)=>[x,passos[i+1]]))assert.ok(b.tx<=a.tx+1e-6,'o elétrico recuou entre '+a.t+' e '+b.t+' ms');
   for(const x of passos){assert.equal(x.ty,0);assert.ok(x.tx>=0&&x.tx<=80,'fora do percurso: '+x.tx)}
   for(const t of [24500,30000,36000,71999])perto(em(t).tx,0,'elétrico no sítio onde descansa aos '+t);
   for(const t of [0,5000,15500,30000,36000,71999])perto(em(t).ang,0,'alavanca ao meio aos '+t);
   assert.ok(em(7200).ang>2&&em(7200).ang<24,'a alavanca a meio do gesto aos 7,2 s: '+em(7200).ang);
   for(const t of [9000,9540,12000]){perto(em(t).ang,26,'alavanca à direita aos '+t);perto(em(t).vb,.25,'via que curva a 0,25 aos '+t)}
   for(const t of [18180,18720,21000]){perto(em(t).ang,-26,'alavanca à esquerda aos '+t);perto(em(t).va,.25,'via a direito a 0,25 aos '+t)}
   perto(em(9000).va,1,'via a direito acesa');perto(em(9540).va,.4,'via a direito a piscar');perto(em(18180).vb,.4,'via que curva a piscar');perto(em(18720).vb,1,'via que curva acesa');
   // 07/11/2026: decisão 175, os sinais saíram: em nenhum instante há sinal nenhum.
   for(const x of passos)assert.deepEqual(x.sinais,[],'sinal de alerta aos '+x.t+' ms');
   for(const t of [30000,36000,71999]){perto(em(t).va,1,'via a direito no fim');perto(em(t).vb,1,'via que curva no fim')}
   // 06/11/2026: decisão 170. «Parar o desenho» pára logo e volta à cena neutra, a meio do gesto da alavanca.
   await f.evaluate(e=>e.getAnimations({subtree:true}).forEach(a=>{a.currentTime=9540}));
   await button.focus();await p.keyboard.press('Enter');assert.equal(await f.evaluate(e=>e.getAnimations({subtree:true}).length),0);assert.deepEqual(await f.evaluate(neutra),NEUTRA,'parado: cena neutra');assert.equal(await button.textContent(),'Pôr o desenho a andar');
   await button.click();await p.clock.fastForward(72001);assert.equal(await f.evaluate(e=>e.getAnimations({subtree:true}).length),0,'pára depois de dois ciclos');assert.equal(await button.textContent(),'Pôr o desenho a andar');
   await button.click();await p.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))});assert.ok(await f.evaluate(e=>e.classList.contains('fundo-pausa')));assert.equal(await p.locator('.jc-eletrico').evaluate(e=>getComputedStyle(e).animationPlayState),'paused');
   await p.evaluate(()=>{delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))});await p.locator('main>nav').scrollIntoViewIfNeeded();await p.evaluate(()=>scrollTo(0,document.documentElement.scrollHeight));await p.waitForTimeout(80);assert.ok(await f.evaluate(e=>e.classList.contains('fundo-pausa')),'pausa fora do ecrã');await f.scrollIntoViewIfNeeded();await p.waitForTimeout(80);await button.click();
  }
  assert.equal(await p.evaluate(()=>JSON.stringify({...localStorage})),storage,'desenho não altera progresso');assert.deepEqual(errors,[]);
  if(out){fs.mkdirSync(out,{recursive:true});await f.scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,`justica-${width}-${mode}.png`),fullPage:true})}
  await p.emulateMedia({media:'print'});assert.ok(await f.isHidden());assert.ok(await button.isHidden());
  // 07/11/2026: decisão 175. Na impressão, o desenho não sai, mas o crédito sai por extenso (sem o «i»), com o endereço da licença.
  {const c=await p.evaluate(credito);assert.ok(c.textoVisivel,'o crédito sai na impressão a '+width+' px ('+mode+')');assert.equal(c.iVisivel,false,'o «i» não sai na impressão');assert.match(await p.locator('.jc-acoes .info-i-texto').innerText(),/Philip Mallis[\s\S]*CC BY-SA 4\.0[\s\S]*Grafismo gerado com recurso a IA, EPI, 2026\./);assert.equal(await p.locator('.jc-acoes a[rel~=license]').evaluate(a=>getComputedStyle(a,'::after').content),'" (https://creativecommons.org/licenses/by-sa/4.0/deed.pt)"')}
  rows.push({width,mode,...m,errors});await ctx.close();console.log('PASS',width,mode);
 }
 for(const options of [{reducedMotion:'reduce'},{javaScriptEnabled:false}]){
  const ctx=await context({viewport:{width:390,height:844},...options}),p=await ctx.newPage();await p.goto(origin+'/lente/olhar-e-decidir/justica/');await p.locator('.jc-fundo').scrollIntoViewIfNeeded();assert.ok(await p.locator('.jc-fundo svg').isVisible());assert.ok(await p.locator('[data-fundo-botao="jc"]').isHidden());assert.equal(await p.locator('.jc-fundo').evaluate(e=>e.getAnimations({subtree:true}).length),0);assert.deepEqual(await p.locator('.jc-fundo').evaluate(neutra),NEUTRA,'cena neutra sem movimento');
  // 07/11/2026: decisão 175. Sem movimento e sem script, o «i» abre e fecha na mesma (é uma <details>) e mostra o crédito.
  {assert.equal((await p.evaluate(credito)).aberto,false);await p.locator('.jc-acoes summary').click();await p.waitForTimeout(250);const c=await p.evaluate(credito);assert.ok(c.aberto&&c.textoVisivel,'o «i» abre com '+JSON.stringify(options));assert.match(c.texto,/Philip Mallis/)}
  await ctx.close();
 }
 // 05/11/2026: revisão de 5/11 (lente-justica-4), com a revisão adversarial. Ao recomeçar depois de «Parar o desenho», não se vê
 // salto: a t=0 a fotografia está transparente (a troca de 1,04 para 1 fica escondida), a 1,44 s já se vê toda, e no fim volta ao
 // retângulo do estado parado (diferença < 0,01 px).
 {const caixa=async reducedMotion=>{const ctx=await context({viewport:{width:1366,height:900},reducedMotion}),p=await ctx.newPage();await p.goto(origin+'/lente/olhar-e-decidir/justica/',{waitUntil:'load'});await p.locator('.jc-fundo').scrollIntoViewIfNeeded();await p.waitForTimeout(120);const r=await p.locator('.jc-fundo').evaluate(e=>{const anims=e.getAnimations({subtree:true}),el=e.querySelector('.jc-eletrico'),med=t=>{anims.forEach(a=>{a.currentTime=t});const q=e.querySelector('.jc-foto').getBoundingClientRect();return {op:+getComputedStyle(el).opacity,l:q.left,t:q.top,r:q.right,b:q.bottom}};const ini=med(0),entra=med(1440),fim=med(36000);anims.forEach(a=>{a.currentTime=0});return {n:anims.length,ini,entra,fim,op:+getComputedStyle(el).opacity,...fim}});await ctx.close();return r};
  const parado=await caixa('reduce'),arranque=await caixa('no-preference');assert.equal(parado.n,0);assert.equal(arranque.n,7,'07/11/2026: decisão 175, sete animações (saem os quatro sinais, entra o elétrico que avança)');
  assert.equal(arranque.ini.op,0,'a t=0 a fotografia tem de estar transparente');assert.equal(arranque.entra.op,1,'a 1,44 s a fotografia já se vê toda');
  for(const k of ['l','t','r','b'])assert.ok(Math.abs(parado[k]-arranque.fim[k])<.01,'o fim da aproximação não coincide com o estado parado, '+k+': '+parado[k]+' contra '+arranque.fim[k]);console.log('PASS recomeço sem salto e uma só aproximação')}
 // 05/11/2026: revisão de 5/11 (lente-justica-5). Entre 406 e 639 px, a faixa (até 300 px) subia por baixo da apresentação.
 for(const width of [420,480,600,639]){const ctx=await context({viewport:{width,height:900},reducedMotion:'reduce'}),p=await ctx.newPage();await p.goto(origin+'/lente/olhar-e-decidir/justica/');const g=await p.evaluate(()=>({lead:document.querySelector('.jc-abertura .lead').getBoundingClientRect().bottom,fundo:document.querySelector('.jc-fundo').getBoundingClientRect().top,sw:document.documentElement.scrollWidth-innerWidth}));assert.ok(g.lead<=g.fundo,'apresentação sobre a faixa a '+width+' px: '+JSON.stringify(g));assert.equal(g.sw,0);await ctx.close()}
 console.log('PASS apresentação acima da faixa a 420, 480, 600 e 639 px')
 const ctx=await context({viewport:{width:768,height:900},reducedMotion:'reduce'}),p=await ctx.newPage();await p.goto(origin+'/lente/olhar-e-decidir/justica/');assert.equal((await p.locator('.jc-fundo').boundingBox()).height,340);await ctx.close();
 if(out)fs.writeFileSync(path.join(out,'medidas.json'),JSON.stringify(rows,null,2));console.log('PASS 9 cenários; teclado, aproximação única, repouso, pausa, estado parado, impressão e tablet.');
}finally{await b.close();server.closeAllConnections();server.close()}})().catch(e=>{console.error(e);process.exitCode=1});
