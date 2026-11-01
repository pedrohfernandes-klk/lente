// 30/10/2026: coração do Laboratório, «Ideias» (narrativas/ideias/), piloto escondido construído a 31/10. Mede no Chromium as
// páginas novas como no sítio público (servidas em /lente/, para o botão de projeção aparecer): a 320, 390, 1024, 1366 e
// 1440 px, em claro e escuro, e na projeção (?projetar=1). Confirma: nenhum erro de JavaScript, nenhum deslize horizontal, a
// primeira ação da entrada no primeiro ecrã, a entrada abaixo de 3000 px a 390, o gesto das escadas (responde, marca
// «Começa aqui», desfaz-se ao segundo toque, não grava nada), o «Continuar» com progresso, e a projeção sem ler o progresso.
// Percorre também as duas lições a responder certo a 320 px (claro) e a 1440 px (escuro), sem deslize em nenhum cartão;
// o percurso a 390 e 1366 px, com o progresso e a projeção, está em tests/browser_licoes_lente.cjs.
const {chromium}=require('playwright');const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
const ROOT=path.resolve(__dirname,'..');
const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript','.json':'application/json','.css':'text/css','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.jpg':'image/jpeg'};
const srv=http.createServer((q,r)=>{let u=decodeURIComponent(q.url.split('?')[0]);if(u.startsWith('/lente/'))u=u.slice(6);if(u.endsWith('/'))u+='index.html';const f=path.join(ROOT,u);if(!f.startsWith(ROOT)||!fs.existsSync(f)){r.writeHead(404);r.end();return}r.writeHead(200,{'content-type':mime[path.extname(f)]||'application/octet-stream'});fs.createReadStream(f).pipe(r)});
const LARGURAS=[[320,640],[390,844],[1024,768],[1366,900],[1440,900]];
const PAGINAS=['narrativas/ideias/','narrativas/ideias/guiao/','narrativas/ideias/docente/','biblioteca/young-tecnica-1940/'];
const FEITA1={lida:true,versao:'2026-10-31-1',t:Date.parse('2026-11-07T10:00:00'),melhor:13};
const vis=s=>String(s).replace(/\*\*|_/g,'');
async function abrir(b,url,w,h,tema,prep){const ctx=await b.newContext({viewport:{width:w,height:h},colorScheme:tema});const p=await ctx.newPage();const erros=[];
 p.on('pageerror',e=>erros.push(e.message));p.on('console',m=>{if(m.type()==='error'&&!/Failed to load resource|net::ERR/.test(m.text()))erros.push(m.text())});
 if(prep)await p.addInitScript(prep);await p.goto(url);await p.waitForTimeout(500);return {ctx,p,erros}}
const largo=p=>p.evaluate(()=>document.documentElement.scrollWidth-window.innerWidth);
async function seguinte(p){const s=p.locator('.casca-folha:not([hidden]) button, .casca-acoes button',{hasText:/Seguinte|Continuar|Ver o resultado|Terminar/});await s.first().click();await p.waitForTimeout(250)}
async function tocarZona(p,j){const box=await p.locator('#baralho .op-m[data-j="'+j+'"] circle.anel').boundingBox();await p.mouse.click(box.x+box.width/2,box.y+box.height/2);await p.waitForTimeout(250)}
async function responder(p,x){
 if(x.t==='escolha')await p.locator('#baralho button.op',{hasText:vis(x.o[x.c])}).first().click();
 else if(x.t==='mapa'){await tocarZona(p,x.c);if(await p.locator('#baralho .mapa-q svg.lupa').count())await tocarZona(p,x.c)}
 else if(x.t==='vf')await p.locator('#baralho button.op',{hasText:x.v?'Verdadeiro':'Falso'}).click();
 else if(x.t==='emparelhar'){for(const [a,c] of x.pares){await p.locator('#baralho button',{hasText:vis(a)}).first().click();await p.waitForTimeout(80);await p.locator('#baralho button',{hasText:vis(c)}).first().click();await p.waitForTimeout(120)}}
 else if(x.t==='sublinhar'){for(const j of x.certas)await p.locator('#baralho button.pal[data-j="'+j+'"]').click()}
 else if(x.t==='ordenar'){for(const t of x.passos){await p.locator('#baralho .soltos button',{hasText:vis(t)}).first().click();await p.waitForTimeout(80)}}
 else if(x.t==='completar'){for(let k=0;k<x.lacunas.length;k++){await p.locator('#baralho select[data-k="'+k+'"]').selectOption(String(x.lacunas[k].c));await p.waitForTimeout(80)}}
 await p.waitForTimeout(300);const conf=p.locator('.casca-acoes [data-confirmar]');if(await conf.count()&&await conf.isVisible()&&await conf.isEnabled())await conf.click();await p.waitForTimeout(250)}
(async()=>{await new Promise(r=>srv.listen(0,r));const base='http://localhost:'+srv.address().port+'/lente/';const b=await chromium.launch();
 // 1. as quatro páginas, nas cinco larguras e nos dois temas
 for(const pag of PAGINAS)for(const [w,h] of LARGURAS)for(const tema of ['light','dark']){
  const {ctx,p,erros}=await abrir(b,base+pag,w,h,tema);
  assert.equal(await largo(p),0,pag+': deslize horizontal a '+w+' px ('+tema+')');
  if(pag==='narrativas/ideias/'){
   const bt=await p.locator('[data-p-botao]').boundingBox();assert(bt&&bt.y+bt.height<=h,'entrada: o botão «Começar» fora do primeiro ecrã a '+w+' px');
   assert.equal(await p.locator('.inverso').count(),1,'uma só região invertida');
   if(w===390){const alt=await p.evaluate(()=>document.documentElement.scrollHeight);assert(alt<3000,'entrada com '+alt+' px a 390')}
   if(pag==='narrativas/ideias/'&&w>=768)assert.equal(await p.locator('.epi-projection-launcher').count(),1,'botão de projeção na barra a '+w+' px');
  }
  assert.deepEqual(erros,[],pag+' a '+w+' px ('+tema+')');await ctx.close();
 }
 console.log('PASS páginas: '+PAGINAS.length+' páginas × 5 larguras × 2 temas, sem deslize nem erros');
 // 2. o gesto das escadas
 {const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/',390,844,'light');const g=p.locator('[data-gesto] button[data-op]');
  await g.nth(1).click();await p.waitForTimeout(200);
  assert.equal(await g.nth(1).getAttribute('aria-pressed'),'true');assert.match(await p.locator('[data-resposta]').innerText(),/dezassete/);
  assert.match(await p.locator('li[data-n="1"] [data-estado]').textContent(),/Começa aqui/);
  await g.nth(1).click();await p.waitForTimeout(200);
  assert.equal(await g.nth(1).getAttribute('aria-pressed'),'false');assert.equal(await p.locator('[data-resposta]').textContent(),'');
  assert.match(await p.locator('li[data-n="1"] [data-estado]').textContent(),/A seguir/);
  assert.equal(await p.evaluate(()=>localStorage.length),0,'o gesto não grava nada');
  assert.deepEqual(erros,[]);await ctx.close();console.log('PASS gesto: responde, marca «Começa aqui», desfaz-se e não grava')}
 // 3. com a sessão 1 feita: «Continuar» na sessão 2; o gesto sai do telemóvel; a projeção não lê o progresso
 {const prep=f=>localStorage.setItem('epi-lab-ideias-s01',JSON.stringify(f));
  const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/',390,844,'dark',{content:'('+prep+')('+JSON.stringify(FEITA1)+')'});
  assert.match(await p.locator('[data-p-k]').textContent(),/Continuar/);assert.equal(await p.locator('[data-p-botao]').getAttribute('href'),'sessao-02/');
  assert.match(await p.locator('[data-p-feito]').textContent(),/Feita: sessão 1, 07\/11/);
  assert.match(await p.locator('li[data-n="1"] [data-estado]').textContent(),/Feita 07\/11/);
  assert.equal(await p.locator('[data-gesto]').isVisible(),false,'o gesto sai do telemóvel depois da sessão 1');
  assert.deepEqual(erros,[]);await ctx.close();
  const q=await abrir(b,base+'narrativas/ideias/?projetar=1',1366,900,'light',{content:'('+prep+')('+JSON.stringify(FEITA1)+')'});
  assert.match(await q.p.locator('[data-p-k]').textContent(),/Começa aqui/);assert.equal(await q.p.locator('[data-p-botao]').getAttribute('href'),'sessao-01/');
  assert(await q.p.locator('.sala').isVisible(),'na projeção, a nota de sala do gesto');assert.equal(await q.p.evaluate(()=>document.documentElement.classList.contains('em-projecao')),true);
  assert.equal(await largo(q.p),0);assert.deepEqual(q.erros,[]);await q.ctx.close();
  const r=await abrir(b,base+'narrativas/ideias/?projetar=1',390,844,'dark');assert.equal(await largo(r.p),0,'projeção a 390');const bt=await r.p.locator('[data-p-botao]').boundingBox();assert(bt.y+bt.height<=844,'projeção: botão no primeiro ecrã a 390');assert.deepEqual(r.erros,[]);await r.ctx.close();
  console.log('PASS progresso e projeção: «Continuar» na sessão 2; a projeção mostra «Começa aqui: 1»')}
 // 4. as duas lições a responder certo, a 320 px (claro) e a 1440 px (escuro), sem deslize em nenhum cartão
 for(const f of ['ideias-s01.json','ideias-s02.json']){const d=JSON.parse(fs.readFileSync(path.join(ROOT,'tools/licoes',f),'utf8'));
  for(const [w,h,tema] of [[320,640,'light'],[1440,900,'dark']]){
   const {ctx,p,erros}=await abrir(b,base+d.saida.replace(/index\.html$/,''),w,h,tema);
   for(let i=0;i<d.cartoes.length;i++){const x=d.cartoes[i];
    assert.equal(await largo(p),0,f+' cartão '+(i+1)+' a '+w+' px');
    if(x.t!=='ler'){await responder(p,x);assert.match(await p.locator('.casca-folha').innerText(),/Certo/,f+' cartão '+(i+1)+' ('+x.t+') a '+w+' px');assert.equal(await largo(p),0,f+' folha do cartão '+(i+1)+' a '+w+' px')}
    if(i<d.cartoes.length-1)await seguinte(p)}
   assert.deepEqual(erros,[],f+' a '+w+' px');await ctx.close();
   console.log('PASS '+d.id+': '+d.cartoes.length+' cartões a responder certo a '+w+' px ('+tema+'), sem deslize')}}
 // 5. 30/10/2026: as correções da primeira revisão (diretor de arte, 31/10): a barra numa linha no telemóvel; «Continuar» no
 // primeiro ecrã a 320 × 640 com progresso; o gesto em três colunas e a resposta à vista; na projeção, a letra cresce na raiz e
 // o botão Projetar some; no guia, os minutos cabem na coluna e as ligações não se partem em colunas; o guião em 4 páginas A4
 // e o guia em 8
 {const prep=f=>localStorage.setItem('epi-lab-ideias-s01',JSON.stringify(f));
  for(const pag of ['narrativas/ideias/','narrativas/ideias/guiao/','narrativas/ideias/docente/'])for(const w of [320,360]){
   const {ctx,p,erros}=await abrir(b,base+pag,w,740,'light');const mh=await p.evaluate(()=>document.querySelector('.migalhas').getBoundingClientRect().height);
   assert(mh<=60,pag+': a barra em mais de uma linha a '+w+' px ('+mh+' px)');assert.deepEqual(erros,[]);await ctx.close()}
  {const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/',320,640,'light',{content:'('+prep+')('+JSON.stringify(FEITA1)+')'});
   const bt=await p.locator('[data-p-botao]').boundingBox();assert(bt.y+bt.height<=640,'com progresso, «Continuar» fora do primeiro ecrã a 320 × 640 ('+(bt.y+bt.height)+')');assert.deepEqual(erros,[]);await ctx.close()}
  // 30/10/2026: segunda correção (diretor de arte, 01/11): abaixo de 380 px o gesto passa a uma coluna (os rótulos partiam-se
  // palavra a palavra); a 390 px continua numa linha
  for(const [w,h,filas] of [[360,740,3],[390,844,1]]){const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/',w,h,'light');
   const tops=await p.evaluate(()=>[...new Set([...document.querySelectorAll('[data-gesto] button[data-op]')].map(x=>Math.round(x.getBoundingClientRect().top)))].length);
   assert.equal(tops,filas,'o gesto em '+tops+' filas a '+w+' px (esperadas '+filas+')');
   await p.evaluate(()=>document.querySelectorAll('[data-gesto] button[data-op]')[1].click());await p.waitForTimeout(900);
   const r=await p.evaluate(()=>document.querySelector('[data-resposta]').getBoundingClientRect().bottom);assert(r<=h,'a resposta do gesto cortada a '+w+' × '+h+' ('+Math.round(r)+')');
   assert.deepEqual(erros,[]);await ctx.close()}
  for(const w of [390,1366]){const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/?projetar=1',w,900,'light');
   const x=await p.evaluate(()=>{const l=document.querySelector('.epi-projection-launcher');return {raiz:getComputedStyle(document.documentElement).fontSize,botao:l?getComputedStyle(l).display:'none',rot:getComputedStyle(document.querySelector('.rotulo')).fontSize}});
   assert.equal(x.raiz,'22px','projeção: a letra da raiz a '+w+' px');assert.equal(x.botao,'none','projeção: o botão Projetar à vista a '+w+' px');assert(parseFloat(x.rot)>=17.8,'projeção: rótulo a '+x.rot);
   assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  for(const w of [320,1366]){const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/docente/',w,800,'light');
   const x=await p.evaluate(()=>({nums:[...document.querySelectorAll('td.num')].filter(td=>{const rg=document.createRange();rg.selectNodeContents(td);return rg.getBoundingClientRect().right>td.getBoundingClientRect().right+0.5}).map(td=>td.textContent),lig:[...document.querySelectorAll('ul.ligacoes a')].map(a=>getComputedStyle(a).display)}));
   assert.deepEqual(x.nums,[],'guia: minutos por cima da borda a '+w+' px');assert(x.lig.length&&x.lig.every(d=>d==='inline-block'),'guia: ligações em '+x.lig.join(','));
   assert.equal(await largo(p),0,'guia: deslize a '+w+' px');assert.deepEqual(erros,[]);await ctx.close()}
  for(const [pag,n] of [['narrativas/ideias/guiao/',4],['narrativas/ideias/docente/',8]]){const {ctx,p}=await abrir(b,base+pag,1024,768,'light');await p.emulateMedia({media:'print'});
   const pdf=(await p.pdf({format:'A4',printBackground:true,preferCSSPageSize:true})).toString('latin1');const pags=(pdf.match(/\/Type\s*\/Page[^s]/g)||[]).length;
   assert.equal(pags,n,pag+': '+pags+' páginas A4 (esperadas '+n+')');await ctx.close()}
  console.log('PASS correções da revisão: barra numa linha, «Continuar» a 320 × 640, gesto e resposta, projeção, guia, 4 + 8 páginas A4')}
  // 6. 30/10/2026: as correções da segunda revisão (01/11): nas lições, a barra de cima cabe a 320 e 360 px (o botão Menu saía do
 // ecrã) e o botão Projetar some na projeção; o gesto numa coluna a 320 px; as formas verbais com pronome sem quebra no hífen;
 // as imagens que se observam maiores; na página do Young, o tema na barra e não por cima do texto; no guia, o índice à direita
 // a partir de 1100 px sem tapar o conteúdo, e em papel sem o índice e com o título de cada secção junto do texto
 {for(const f of ['ideias-s01.json','ideias-s02.json']){const d=JSON.parse(fs.readFileSync(path.join(ROOT,'tools/licoes',f),'utf8'));const url=base+d.saida.replace(/index\.html$/,'');
   for(const w of [320,360]){const {ctx,p,erros}=await abrir(b,url,w,700,'dark');
    const fora=await p.evaluate(()=>[...document.querySelectorAll('.casca-topo a,.casca-topo button')].filter(e=>e.offsetParent!==null&&e.getBoundingClientRect().right>innerWidth+0.5).map(e=>e.getAttribute('aria-label')||e.textContent.trim()));
    assert.deepEqual(fora,[],d.id+': controlos da barra fora do ecrã a '+w+' px');
    const m=await p.evaluate(()=>{const r=document.querySelector('.c-marca').getBoundingClientRect();return [r.width,r.height]});assert(m[0]>=44&&m[1]>=44,d.id+': a marca com '+m.join('×'));
    assert.deepEqual(erros,[]);await ctx.close()}
   const q=await abrir(b,url+'?projetar=1',1366,768,'light');await q.p.waitForTimeout(300);
   assert.equal(await q.p.evaluate(()=>{const l=document.querySelector('.epi-projection-launcher');return l?getComputedStyle(l).display:'none'}),'none',d.id+': o botão Projetar na projeção');
   assert.deepEqual(q.erros,[]);await q.ctx.close()}
  {const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/',320,640,'light');
   const g=await p.evaluate(()=>[...document.querySelectorAll('[data-gesto] button[data-op]')].map(x=>{const r=x.getBoundingClientRect();return [Math.round(r.left),Math.round(r.height)]}));
   assert(g.every(x=>x[0]===g[0][0]&&x[1]<=52),'o gesto a 320 px numa coluna, cada botão numa linha: '+JSON.stringify(g));
   await p.evaluate(()=>document.querySelectorAll('[data-gesto] button[data-op]')[1].click());await p.waitForTimeout(300);
   assert.equal(await p.locator('[data-resposta] .nq').count(),1,'a resposta do gesto com «subiu-lhe» sem quebra');
   const bt=await p.locator('[data-p-botao]').boundingBox();assert(bt.y+bt.height<=640,'o botão «Começar» fora do primeiro ecrã a 320 × 640');
   assert.deepEqual(erros,[]);await ctx.close()}
  for(const pag of ['narrativas/ideias/','narrativas/ideias/guiao/','narrativas/ideias/docente/'])for(const w of [320,390,1366]){const {ctx,p}=await abrir(b,base+pag,w,800,'light');
   const q=await p.evaluate(()=>{const out=[];const tw=document.createTreeWalker(document.querySelector('main'),NodeFilter.SHOW_TEXT);let n;
    while(n=tw.nextNode()){if(!n.parentElement||n.parentElement.closest('.nq'))continue;const re=/[a-zà-ÿ]-(?:lo|la|los|las|lhe|lhes|se|me|te|nos|vos|o|a|os|as)(?![a-zà-ÿ-])/gi;if(re.test(n.textContent))out.push(n.textContent.trim().slice(0,40))}return out});
   assert.deepEqual(q,[],pag+': forma verbal com pronome fora de .nq a '+w+' px');await ctx.close()}
  for(const [f,n] of [['ideias-s02.json',11]]){const d=JSON.parse(fs.readFileSync(path.join(ROOT,'tools/licoes',f),'utf8'));
   const {ctx,p}=await abrir(b,base+d.saida.replace(/index\.html$/,''),1366,900,'light');
   for(let i=0;i<n-1;i++){const x=d.cartoes[i];if(x.t!=='ler'){const txt=(await p.locator('#baralho').innerText()).replace(/\s+/g,' ');const c=d.cartoes.filter(y=>y.t!=='ler'&&[y.p,y.p2].some(t=>t&&txt.includes(vis(t).slice(0,50))));await responder(p,c.length===1?c[0]:x)}await seguinte(p)}
   const h=await p.evaluate(()=>{const im=[...document.querySelectorAll('#baralho img')].find(i=>i.offsetParent!==null);return im?im.getBoundingClientRect().height:0});
   assert(h>=500,'a fotografia de Atget com '+Math.round(h)+' px de altura a 1366 × 900 (era 361)');await ctx.close()}
  for(const w of [320,390]){const {ctx,p,erros}=await abrir(b,base+'biblioteca/young-tecnica-1940/',w,700,'light');
   const t=await p.evaluate(()=>{const e=document.querySelector('.epi-appearance-toggle');return e?{naBarra:!!e.closest('nav.migalhas'),flutua:!!e.closest('[data-appearance-floating]')}:null});
   assert(t&&t.naBarra&&!t.flutua,'Young: o botão do tema na barra a '+w+' px');assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  {const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/docente/',1366,900,'light');await p.evaluate(()=>window.scrollTo(0,4000));await p.waitForTimeout(300);
   const r=await p.evaluate(()=>{const nav=document.querySelector('nav.indice-nav');const nr=nav.getBoundingClientRect();const sobre=[...document.querySelectorAll('main > section, main > header')].filter(e=>{const q=e.getBoundingClientRect();return q.right>nr.left&&q.left<nr.right&&q.bottom>nr.top&&q.top<nr.bottom}).length;return {pos:getComputedStyle(nav).position,top:Math.round(nr.top),sobre}});
   assert.equal(r.pos,'sticky','guia: o índice à direita');assert(r.top>=0&&r.top<=40,'guia: o índice à vista depois de rolar ('+r.top+')');assert.equal(r.sobre,0,'guia: o índice por cima do conteúdo');
   await p.emulateMedia({media:'print'});assert.equal(await p.evaluate(()=>getComputedStyle(document.querySelector('ul.indice')).display),'none','guia: o índice em papel');
   assert.equal(await p.evaluate(()=>getComputedStyle(document.querySelector('#sequencia')).breakBefore),'page','guia: «A sequência» abre página');
   assert.deepEqual(erros,[]);await ctx.close()}
  console.log('PASS segunda revisão: barra das lições a 320 e 360 px, Projetar na projeção, gesto numa coluna a 320 px, nenhuma forma com pronome partida no hífen, Atget maior, tema do Young na barra, índice do guia')}
 await b.close();srv.close()})().catch(e=>{console.error(e);process.exit(1)});
