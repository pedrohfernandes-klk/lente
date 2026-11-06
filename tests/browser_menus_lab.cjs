// 05/11/2026: decisão 163 (menus do Laboratório e das lições), em Chromium.
// Laboratório (entrada, porta, percurso) e menu ≡ (sessão do Ideias, sessão do piloto da Cidadania, M1 estática, peça do
// Laboratório), a 320, 390, 1024 e 1366 px, em claro, em escuro e na projeção: o caminho em frente à vista, sem deslocamento
// horizontal, alvos de 44 px, o menu todo pelo teclado (foco preso, Escape fecha e devolve o foco ao ≡), contraste do painel,
// «Sair da projeção» na projeção e o que se vê sem JavaScript. Com LENTE_SHOTS=<pasta>, guarda capturas pequenas.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),out=process.env.LENTE_SHOTS||'';if(out)fs.mkdirSync(out,{recursive:true});
const ABS='https://pedrohfernandes-klk.github.io/lente/';
const tipos={'.js':'application/javascript','.css':'text/css','.html':'text/html; charset=utf-8','.webp':'image/webp','.json':'application/json','.svg':'image/svg+xml','.jpg':'image/jpeg','.png':'image/png'};
const server=http.createServer((req,res)=>{let f=path.join(root,decodeURIComponent(new URL(req.url,'http://x').pathname));if(!f.startsWith(root)){res.writeHead(403).end();return;}if(fs.existsSync(f)&&fs.statSync(f).isDirectory())f=path.join(f,'index.html');if(!fs.existsSync(f)){res.writeHead(404).end();return;}res.setHeader('Content-Type',tipos[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));});
const LAB=['/narrativas/','/narrativas/ver/','/narrativas/percursos/olhar/','/narrativas/tudo/'];
const MENU=['/narrativas/ideias/sessao-01/','/cidadania/piloto/m1-s01/','/cidadania/m1/passo-01/','/narrativas/oficina-arco/'];
const lum=c=>{const m=c.match(/[\d.]+/g).map(Number);const [r,g,b]=m.slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:((v+.055)/1.055)**2.4});return .2126*r+.7152*g+.0722*b;};
const contraste=(a,b)=>{const [x,y]=[lum(a),lum(b)].sort((p,q)=>q-p);return (x+.05)/(y+.05);};
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port;const b=await chromium.launch();
 const novo=async(opts={})=>{const ctx=await b.newContext({viewport:{width:opts.width||390,height:opts.height||844},colorScheme:opts.tema||'light',reducedMotion:'reduce',javaScriptEnabled:opts.js!==false});
  await ctx.route(ABS+'**',async r=>{const u=new URL(r.request().url());const resp=await ctx.request.get(base+u.pathname.replace(/^\/lente/,'')+u.search);await r.fulfill({response:resp});});
  await ctx.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
  const p=await ctx.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));return {ctx,p,erros};};
 const semDeslocar=async(p,rot)=>assert.equal(await p.evaluate(()=>Math.max(0,document.documentElement.scrollWidth-innerWidth)),0,rot+': deslocamento horizontal');
 // alvos fora do texto (as ligações dentro de uma frase ficam de fora, como no WCAG 2.5.8); «Saltar para o conteúdo» só se vê com o foco
 const pequenos=async(p,escopo)=>p.evaluate(escopo=>{const fora=[];for(const el of document.querySelectorAll(escopo)){if(el.matches('.salta,.c-sr')||el.closest('[hidden],.c-sr'))continue;const r=el.getBoundingClientRect();if(!r.width||!r.height||getComputedStyle(el).visibility==='hidden')continue;const frase=el.closest('p,figcaption,.info-i-texto,.legenda');if(frase&&el.tagName==='A'&&frase.textContent.trim().length>el.textContent.trim().length+2)continue;if(r.height<43.5||r.width<43.5)fora.push((el.className||el.tagName)+' «'+el.textContent.trim().slice(0,30)+'» '+Math.round(r.width)+'x'+Math.round(r.height));}return fora;},escopo);
 try{
  // 1. Laboratório: sem deslocamento, alvos, caminho em frente, nos dois temas e na projeção
  for(const tema of ['light','dark'])for(const width of [320,390,1024,1366])for(const url of LAB){
   const {ctx,p,erros}=await novo({width,tema});await p.goto(base+url,{waitUntil:'load'});const rot=`${url} ${width} ${tema}`;
   await semDeslocar(p,rot);
   assert.deepEqual(await pequenos(p,'main a,main button,main summary,main label.repor,.lab-barra a,.lab-barra button,.lab-fio a'),[],rot+': alvos abaixo de 44 px');
   assert.equal(await p.locator('header.lab-barra').count(),1);assert.equal(await p.locator('.lab-barra').evaluate(e=>getComputedStyle(e).position),'sticky');
   assert.ok(await p.locator('.lab-barra').evaluate(e=>e.getBoundingClientRect().height<=60),rot+': barra numa linha');
   if(url==='/narrativas/'){
    // a ação principal (o Ideias) e as três portas; a 390, o botão dentro do primeiro ecrã de 844 px
    const bot=p.locator('[data-p-botao]');assert.ok(await bot.isVisible());if(width===390)assert.ok(await bot.evaluate(e=>e.getBoundingClientRect().bottom<=844),rot+': botão do Ideias no primeiro ecrã');
    assert.equal(await p.locator('.porta3').count(),3);for(const a of await p.locator('.porta3').all())assert.ok(await a.isVisible());
   }else{
    assert.equal(await p.locator('nav.lab-fio a').count(),4);
    if(url!=='/narrativas/tudo/'){const primeira=p.locator('.linha').first();assert.ok(await primeira.isVisible());if(width===390)assert.ok(await primeira.evaluate(e=>e.getBoundingClientRect().top<844),rot+': primeira peça no primeiro ecrã');
     // nenhum beco: «Daqui segues para» com o seguinte e o regresso
     assert.equal(await p.locator('nav.depois a').count(),2);}
   }
   if(out&&tema==='light'&&[390,1366].includes(width)&&url!=='/narrativas/tudo/')await p.screenshot({path:path.join(out,'lab'+url.replace(/\//g,'-')+width+'.jpg'),type:'jpeg',quality:50});
   assert.deepEqual(erros,[]);await ctx.close();
  }
  // projeção: barra estática, letra grande, sem estado pessoal
  for(const width of [390,1366]){const {ctx,p}=await novo({width});await p.addInitScript(()=>localStorage.setItem('epi-narrativas',JSON.stringify({feitas:{leonardo:Date.UTC(2026,10,1,12)}})));
   for(const url of LAB){await p.goto(base+url+'?projetar=1',{waitUntil:'load'});await semDeslocar(p,url+' projeção');assert.equal(await p.locator('.lab-barra').evaluate(e=>getComputedStyle(e).position),'static');
    assert.equal(await p.locator('main .etq:visible,main .contagem:visible,main .registos:visible').count(),0,url+': estado pessoal na projeção');
    assert.deepEqual(await p.locator('main').evaluate(m=>[...m.querySelectorAll('*')].filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())&&e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden'&&parseFloat(getComputedStyle(e).fontSize)<17.85).map(e=>e.textContent.trim().slice(0,40))),[],url+': letra abaixo de 17,9 px na projeção');}
   await ctx.close();}
  // estado: «A seguir» só com alguma peça feita
  {const {ctx,p}=await novo({width:390});await p.goto(base+'/narrativas/ver/',{waitUntil:'load'});assert.equal(await p.locator('.linha.seguir').count(),0,'A seguir sem nada feito');
   await p.evaluate(()=>localStorage.setItem('epi-narrativas',JSON.stringify({feitas:{leonardo:Date.UTC(2026,10,1,12)}})));await p.reload({waitUntil:'load'});
   assert.equal(await p.locator('.linha.seguir').count(),1);assert.equal(await p.locator('li.seguir [data-estado]').textContent(),'A seguir');assert.match(await p.locator('[data-estado="leonardo"]').textContent(),/^Feita \d\d\/\d\d$/);
   await p.goto(base+'/narrativas/',{waitUntil:'load'});assert.match(await p.locator('#ler-como-quem-escreve .cz-state').textContent(),/^1 de 9 feitas$/);
   // o Ideias na entrada: «A seguir» só com uma sessão feita; depois, o botão continua na sessão seguinte
   assert.equal(await p.locator('.ideias-sessoes li.seguir').count(),0);assert.match(await p.locator('[data-p-botao]').textContent(),/^Abrir Ideias\s→$/);
   await p.evaluate(()=>localStorage.setItem('epi-lab-ideias-s01',JSON.stringify({versao:'2026-11-01-1',lida:true,data:Date.UTC(2026,10,1,12)})));await p.reload({waitUntil:'load'});
   assert.match(await p.locator('[data-p-botao]').textContent(),/^Continuar na sessão\s2\s→$/);assert.ok((await p.locator('[data-p-botao]').getAttribute('href')).endsWith('ideias/sessao-02/'));assert.equal(await p.locator('.ideias-sessoes li.seguir [data-estado]').textContent(),'A seguir');assert.match(await p.locator('.ideias-sessoes li.feita [data-estado]').textContent(),/^Feita \d\d\/\d\d$/);
   await ctx.close();}

  // 2. Menu ≡: sem deslocamento, alvos, teclado, foco preso, Escape, contraste, projeção
  for(const tema of ['light','dark'])for(const width of [320,390,1024,1366])for(const url of MENU){
   const {ctx,p,erros}=await novo({width,tema});await p.goto(base+url,{waitUntil:'load'});const rot=`${url} ${width} ${tema}`;
   await p.waitForFunction(()=>{const b=document.querySelector('#baralho');return b&&b.children.length>0;},null,{timeout:10000});await semDeslocar(p,rot);
   const tres=p.locator('.casca-topo [data-c-menu]');assert.equal(await tres.getAttribute('aria-controls'),'c-menu');
   assert.deepEqual(await pequenos(p,'.casca-topo .c-marca,.casca-topo [data-c-menu],.casca-topo [data-c-som]'),[],rot+': alvos da barra');
   // abrir pelo teclado
   await tres.focus();await p.keyboard.press('Enter');const painel=p.locator('.casca-menu.m2');await painel.waitFor({state:'visible'});
   assert.equal(await tres.getAttribute('aria-expanded'),'true');await semDeslocar(p,rot+' menu aberto');
   assert.equal(await p.locator('#c-menu').getAttribute('aria-modal'),'true');
   const larg=await p.locator('#c-menu').evaluate(e=>e.getBoundingClientRect().width);assert.ok(Math.abs(larg-Math.min(360,width*.9))<=1,rot+': largura do painel '+larg);
   // «Estás em», depois «Voltar…» como primeira ação; o caminho em frente («Seguinte») quando existe
   assert.ok(await p.locator('#m-t').isVisible());assert.match(await p.locator('nav[aria-label="Menu"] a').first().innerText(),/^Voltar /);
   if(url==='/narrativas/oficina-arco/'||url==='/narrativas/ideias/sessao-01/'||url==='/cidadania/m1/passo-01/')assert.match(await p.locator('nav[aria-label="Menu"] a').nth(1).innerText(),/^Seguinte/);
   assert.deepEqual(await pequenos(p,'#c-menu a,#c-menu button,#c-menu summary'),[],rot+': alvos do menu');
   // foco preso: 15 Tab e 5 Shift+Tab nunca saem do painel; cada item do menu recebe o foco
   const vistos=new Set();for(let i=0;i<15;i++){await p.keyboard.press('Tab');const r=await p.evaluate(()=>{const a=document.activeElement;return {dentro:!!a.closest('#c-menu'),t:(a.textContent||a.getAttribute('aria-label')||'').trim().slice(0,30)}});assert.ok(r.dentro,rot+': o foco saiu do menu');vistos.add(r.t);}
   for(let i=0;i<5;i++){await p.keyboard.press('Shift+Tab');assert.ok(await p.evaluate(()=>!!document.activeElement.closest('#c-menu')),rot+': Shift+Tab saiu do menu');}
   const itens=await p.locator('#c-menu nav a:visible,#c-menu nav button:visible').evaluateAll(es=>es.map(e=>e.textContent.trim().slice(0,30)));for(const t of itens)assert.ok(vistos.has(t),rot+': item sem foco pelo teclado: '+t);
   // os itens com ligação levam a páginas que existem
   for(const h of await p.locator('#c-menu a[href]:visible').evaluateAll(es=>es.map(e=>e.href))){if(!h.startsWith(base)||h.includes('?'))continue;const st=(await ctx.request.get(h)).status();assert.equal(st,200,rot+': '+h);}
   // contraste: texto do painel 4,5:1 ou mais; o contorno do ✕ 3:1 ou mais
   const pares=await p.locator('#c-menu').evaluate(raiz=>{const fundo=el=>{for(let e=el;e;e=e.parentElement){const c=getComputedStyle(e).backgroundColor;if(c&&!/rgba\(0, 0, 0, 0\)|transparent/.test(c))return c;}return 'rgb(255, 255, 255)';};
    const t=[...raiz.querySelectorAll('*')].filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())&&e.getClientRects().length).map(e=>[getComputedStyle(e).color,fundo(e),e.textContent.trim().slice(0,20)]);
    const x=raiz.querySelector('[data-c-fecha-menu]');return {t,borda:[getComputedStyle(x).borderTopColor,fundo(x)]};});
   for(const [c,f,txt] of pares.t)assert.ok(contraste(c,f)>=4.5,rot+': contraste «'+txt+'» '+contraste(c,f).toFixed(2));
   assert.ok(contraste(...pares.borda)>=3,rot+': contorno do ✕');
   if(out&&width===390&&url==='/narrativas/oficina-arco/')await p.screenshot({path:path.join(out,'menu-390-'+tema+'.jpg'),type:'jpeg',quality:50});
   // Escape fecha e devolve o foco ao ≡; o ✕ pelo teclado também
   await p.keyboard.press('Escape');await painel.waitFor({state:'hidden'});assert.ok(await tres.evaluate(e=>document.activeElement===e),rot+': o foco não voltou ao ≡');assert.equal(await tres.getAttribute('aria-expanded'),'false');
   assert.equal(await p.locator('.casca-corpo[inert]').count(),0,rot+': corpo ficou inerte');
   await p.keyboard.press('Enter');await painel.waitFor({state:'visible'});assert.equal(await p.locator('.casca-corpo[inert]').count(),1);await p.locator('[data-c-fecha-menu]').focus();await p.keyboard.press('Enter');await painel.waitFor({state:'hidden'});assert.ok(await tres.evaluate(e=>document.activeElement===e));
   assert.deepEqual(erros,[]);await ctx.close();
  }
  // projeção: «Sair da projeção» à vista, «Projetar na aula» escondido; fora dela, o contrário
  for(const url of MENU){const {ctx,p}=await novo({width:1366});
   await p.goto(base+url+'?projetar=1',{waitUntil:'load'});await p.locator('.casca-topo [data-c-menu]').click();await p.locator('.casca-menu.m2').waitFor({state:'visible'});
   assert.ok(await p.locator('#c-menu .so-aula').isVisible(),url);assert.ok(await p.locator('#c-menu .so-normal').isHidden(),url);await semDeslocar(p,url+' projeção');
   if(out&&url==='/narrativas/ideias/sessao-01/')await p.screenshot({path:path.join(out,'menu-1366-projecao.jpg'),type:'jpeg',quality:50});
   await p.goto(base+url,{waitUntil:'load'});await p.locator('.casca-topo [data-c-menu]').click();assert.ok(await p.locator('#c-menu .so-normal').isVisible());assert.ok(await p.locator('#c-menu .so-aula').isHidden());
   // os cartões já feitos: o item só aparece com a barra de progresso ativa
   assert.equal(await p.locator('#c-menu [data-c-rever]').isVisible(),await p.locator('[data-c-barra]').evaluate(e=>!e.disabled&&!e.hidden));
   await ctx.close();}

  // 3. Sem JavaScript: a entrada, as portas e os percursos mostram tudo; as sessões e as peças dizem para onde ir
  {const {ctx,p}=await novo({width:390,js:false});
   await p.goto(base+'/narrativas/');assert.equal(await p.locator('.porta3:visible').count(),3);assert.equal(await p.locator('[data-p-botao]').getAttribute('href'),'ideias/');assert.equal(await p.locator('.ideias-sessoes a:visible').count(),2);
   for(const u of ['/narrativas/ver/','/narrativas/treinar/','/narrativas/criar/','/narrativas/percursos/olhar/']){await p.goto(base+u);const n=await p.locator('li[data-peca]').count();assert.ok(n>=4);assert.equal(await p.locator('li[data-peca]:visible').count(),n,u);}
   for(const u of MENU){await p.goto(base+u);assert.ok(await p.locator('.c-semjs').isVisible(),u);assert.ok(await p.locator('.c-semjs a').first().getAttribute('href'));}
   await ctx.close();}
  console.log('Menus do Laboratório e das lições: 320, 390, 1024 e 1366 px, claro, escuro, projeção, teclado e sem JavaScript.');
 }finally{await b.close();server.close();}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
