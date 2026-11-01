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
// 01/11/2026: a versão da sessão 1 sobe com o cartão novo «O método» (2026-11-01-1); o progresso de teste lê-a da lição, para a
// sessão feita continuar a contar como feita (com a versão antiga, o motor e a entrada recomeçam, e é isso que se quer)
const FEITA1={lida:true,versao:JSON.parse(fs.readFileSync(path.join(ROOT,'tools/licoes/ideias-s01.json'),'utf8')).versao,t:Date.parse('2026-11-07T10:00:00'),melhor:13};
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
   // 30/10/2026: na quarta revisão (01/11), as ligações passam a bloco (com inline-block a marca da lista alinhava pela última
   // linha); sem inline-flex, como antes
   assert.deepEqual(x.nums,[],'guia: minutos por cima da borda a '+w+' px');assert(x.lig.length&&x.lig.every(d=>d==='block'),'guia: ligações em '+x.lig.join(','));
   assert.equal(await largo(p),0,'guia: deslize a '+w+' px');assert.deepEqual(erros,[]);await ctx.close()}
  // 01/11/2026: o guia abre com «Porque seguimos um método», numa primeira página com o cabeçalho, e «Antes de começar» abre a
  // segunda (antes partia-se entre duas): 9 páginas A4, eram 8. O guião continua em 4
  for(const [pag,n] of [['narrativas/ideias/guiao/',4],['narrativas/ideias/docente/',9]]){const {ctx,p}=await abrir(b,base+pag,1024,768,'light');await p.emulateMedia({media:'print'});
   const pdf=(await p.pdf({format:'A4',printBackground:true,preferCSSPageSize:true})).toString('latin1');const pags=(pdf.match(/\/Type\s*\/Page[^s]/g)||[]).length;
   assert.equal(pags,n,pag+': '+pags+' páginas A4 (esperadas '+n+')');await ctx.close()}
  console.log('PASS correções da revisão: barra numa linha, «Continuar» a 320 × 640, gesto e resposta, projeção, guia, 4 + 9 páginas A4')}
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
   // 01/11/2026: «Antes de começar» também abre página, depois de «Porque seguimos um método»
   assert.equal(await p.evaluate(()=>getComputedStyle(document.querySelector('#antes')).breakBefore),'page','guia: «Antes de começar» abre página');
   assert.deepEqual(erros,[]);await ctx.close()}
  console.log('PASS segunda revisão: barra das lições a 320 e 360 px, Projetar na projeção, gesto numa coluna a 320 px, nenhuma forma com pronome partida no hífen, Atget maior, tema do Young na barra, índice do guia')}
 // 7. 30/10/2026: as correções da terceira revisão (01/11): no guia, nenhuma tabela esconde nada num deslize lateral, de 320 a
 // 1440 px (o quadro da sequência passa a fichas abaixo de 640 px); na entrada, as portas só com sessões em preparação dobram-se
 // em bandas de 88 px no telemóvel (com script e fora da projeção), a tabela de museu fica ao lado da imagem a partir de 960 px,
 // as saídas não transbordam a 320 px e a pergunta do gesto equilibra as linhas; a imagem do atol com níveis (o recife separa-se
 // do oceano); na página do Young, letra mínima de 13 px, «Voltar à Biblioteca» com 44 px, medida de 32 em (cerca de 71
 // carateres em Georgia) e a abertura à esquerda
 {for(const w of [320,360,390,480,599,639,640,1024,1366,1440]){const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/docente/',w,800,w===390?'dark':'light');
   const x=await p.evaluate(()=>({esc:[...document.querySelectorAll('main .tabela')].map(t=>t.scrollWidth-t.clientWidth),seq:getComputedStyle(document.querySelector('table.seq')).display,
    rotulos:[...document.querySelectorAll('table.seq tbody td')].every(td=>td.getAttribute('data-r'))}));
   assert(x.esc.every(v=>v===0),'guia: tabela com '+x.esc.join('/')+' px escondidos a '+w+' px');assert(x.rotulos,'guia: célula da sequência sem data-r');
   assert.equal(x.seq,w<640?'block':'table','guia: a sequência a '+w+' px em '+x.seq);assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  {const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/',390,844,'light');
   const est=()=>p.evaluate(()=>['ver','treinar','criar'].map(k=>{const s=document.getElementById('porta-'+k),bt=s.querySelector('.porta-abre');return {h:Math.round(s.getBoundingClientRect().height),bt:bt?[Math.round(bt.getBoundingClientRect().width),Math.round(bt.getBoundingClientRect().height),bt.getAttribute('aria-expanded'),bt.getAttribute('aria-label')]:null,lista:s.querySelector('ol.sessoes').offsetParent!==null}}));
   const alt=await p.evaluate(()=>document.documentElement.scrollHeight);assert(alt<2500,'entrada com '+alt+' px a 390 (era 2912)');
   let e1=await est();assert(e1[0].lista&&!e1[0].bt,'a porta Ver fica aberta');
   for(const [k,nome] of [[1,'Treinar'],[2,'Criar']]){assert(e1[k].h>=86&&e1[k].h<=92,nome+': banda com '+e1[k].h+' px');assert.deepEqual(e1[k].bt,[48,48,'false','Abrir '+nome]);assert(!e1[k].lista,nome+': lista à vista na banda')}
   await p.locator('#porta-treinar .porta-abre').click();await p.waitForTimeout(150);let e2=await est();assert.deepEqual(e2[1].bt.slice(2),['true','Fechar Treinar']);assert(e2[1].lista&&e2[1].h>200,'Treinar aberta');
   await p.locator('#porta-treinar .porta-abre').click();await p.waitForTimeout(150);assert.equal((await est())[1].h,e1[1].h,'Treinar volta a fechar');
   await p.locator('.faixa a[href="#porta-criar"]').click();await p.waitForTimeout(250);assert((await est())[2].lista,'a faixa abre a porta Criar');
   assert.deepEqual(erros,[]);await ctx.close()}
  for(const [url,w,js,quem] of [['narrativas/ideias/',640,true,'a 640 px'],['narrativas/ideias/?projetar=1',390,true,'na projeção'],['narrativas/ideias/',390,false,'sem script']]){
   const ctx=await b.newContext({viewport:{width:w,height:844},javaScriptEnabled:js});const p=await ctx.newPage();await p.goto(base+url);await p.waitForTimeout(400);
   const r=await p.evaluate(()=>[...document.querySelectorAll('.porta[data-dobra]')].map(s=>s.querySelector('ol.sessoes').offsetParent!==null));
   assert(r.length===2&&r.every(Boolean),'as portas dobram-se '+quem);await ctx.close()}
  for(const [w,h] of [[1024,768],[1366,900],[1440,900]]){const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/',w,h,'light');
   const r=await p.evaluate(()=>{const c=document.querySelector('.atol .campo').getBoundingClientRect(),f=document.querySelector('.atol figcaption').getBoundingClientRect(),g=document.querySelector('.gesto').getBoundingClientRect();return {ao_lado:f.left>=c.right,pe:Math.abs(f.bottom-c.bottom),vazio:Math.round(f.top-g.bottom),dentro:!!document.querySelector('figure.atol > figcaption')}});
   assert(r.ao_lado&&r.pe<=1&&r.dentro,'a tabela de museu ao lado da imagem a '+w+' px: '+JSON.stringify(r));assert(r.vazio<200,'vazio de '+r.vazio+' px à direita a '+w+' px (era 292 a 319)');assert.deepEqual(erros,[]);await ctx.close()}
  {const {ctx,p}=await abrir(b,base+'narrativas/ideias/',320,640,'light');
   assert.deepEqual(await p.evaluate(()=>[...document.querySelectorAll('.saidas a')].filter(a=>a.scrollWidth>a.clientWidth).map(a=>a.textContent)),[],'saídas a transbordar a 320 px');
   assert.equal(await p.evaluate(()=>getComputedStyle(document.querySelector('.gesto .q')).textWrapStyle||getComputedStyle(document.querySelector('.gesto .q')).textWrap),'balance','a pergunta do gesto sem órfã');
   const n=await p.evaluate(async()=>{const im=document.querySelector('.atol img');await im.decode();const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;const x=c.getContext('2d');x.drawImage(im,0,0);
    const d=x.getImageData(0,0,c.width,c.height).data,v=[];for(let i=0;i<d.length;i+=16)v.push(d[i]);v.sort((a,b)=>a-b);return {p50:v[Math.floor(v.length*.5)],p99:v[Math.floor(v.length*.99)]}});
   assert(n.p99-n.p50>=140,'atol: o recife mal se separa do oceano ('+JSON.stringify(n)+'; eram 149 e 226)');await ctx.close()}
  for(const [w,tema] of [[320,'dark'],[1366,'light']]){const {ctx,p,erros}=await abrir(b,base+'biblioteca/young-tecnica-1940/',w,800,tema);
   // a medida em em (32 em: cerca de 71 carateres em Georgia, medidos com a Gelasio, que tem as mesmas métricas), e não em
   // carateres, porque sem a Georgia a letra de recurso muda a conta
   const r=await p.evaluate(()=>{const em=e=>+(e.clientWidth/parseFloat(getComputedStyle(e).fontSize)).toFixed(2);
    const v=[...document.querySelectorAll('a')].find(a=>a.textContent.trim()==='Voltar à Biblioteca').getBoundingClientRect();const t=document.querySelector('.bib-texto p');
    return {et:parseFloat(getComputedStyle(document.querySelector('.p-etiqueta')).fontSize),voltar:Math.round(v.height),em:Math.max(...[...document.querySelectorAll('.bib-texto p, .p-lead')].map(em)),lh:+(parseFloat(getComputedStyle(t).lineHeight)/parseFloat(getComputedStyle(t).fontSize)).toFixed(2),lead:getComputedStyle(document.querySelector('.p-lead')).textAlign}});
   assert(r.et>=13&&r.voltar>=44&&r.em<=32.01&&r.lh<=1.56&&r.lead==='start','Young a '+w+' px: '+JSON.stringify(r));assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  console.log('PASS terceira revisão: tabelas do guia sem deslize de 320 a 1440 px, portas dobradas no telemóvel, tabela de museu ao lado da imagem, saídas a 320 px, pergunta do gesto, atol com níveis, página do Young')}
 // 8. 30/10/2026: as correções da quarta revisão (01/11): na entrada, «As sete sessões» 1,25 vezes os nomes das portas, o gesto
 // numa coluna na projeção entre 960 e 1099 px e a linha de informação e a etiqueta com 34 em de medida (75 carateres no
 // máximo); no guia, os três botões de cada sessão numa coluna abaixo de 480 px e nenhum rótulo a negro partido; no guião, nenhum
 // espaço para escrever sozinho numa linha no telemóvel; na sessão 2, o «»» do cartão 16 na linha do último menu
 {for(const [w,q] of [[390,''],[1366,''],[1366,'?projetar=1']]){const {ctx,p}=await abrir(b,base+'narrativas/ideias/'+q,w,900,'light');
   const r=await p.evaluate(()=>{const f=s=>parseFloat(getComputedStyle(document.querySelector(s)).fontSize);return f('h2.sessoes-t')/f('.porta h3')});
   assert(r>=1.249,'entrada: «As sete sessões» só '+r.toFixed(2)+' vezes os nomes das portas a '+w+' px'+q);await ctx.close()}
  for(const [w,tema] of [[960,'light'],[1024,'dark'],[1099,'light']]){const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/?projetar=1',w,800,tema);
   const g=await p.evaluate(()=>[...document.querySelectorAll('[data-gesto] button[data-op]')].map(x=>{const r=x.getBoundingClientRect();return [Math.round(r.left),Math.round(r.height)]}));
   assert(g.every(x=>x[0]===g[0][0]&&x[1]<=52),'projeção: o gesto a '+w+' px numa coluna, cada botão numa linha: '+JSON.stringify(g));assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  for(const w of [1024,1366,1440]){const {ctx,p}=await abrir(b,base+'narrativas/ideias/',w,900,'light');
   const m=await p.evaluate(()=>['.abre .info','.atol figcaption'].map(s=>{const e=document.querySelector(s);return +(e.clientWidth/parseFloat(getComputedStyle(e).fontSize)).toFixed(2)}));
   assert(m.every(v=>v<=34.01),'entrada: medida da linha de informação e da etiqueta em '+m.join(' e ')+' em a '+w+' px');await ctx.close()}
  for(const w of [320,360,390,480,1024,1366,1440]){const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/docente/',w,800,w===360?'dark':'light');
   const r=await p.evaluate(()=>({bts:[...document.querySelectorAll('p.acoes-s')].map(q=>[...q.querySelectorAll('a.botao-s')].map(a=>{const r=a.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top)]})),
    partidos:[...document.querySelectorAll('.pg b')].filter(x=>x.getClientRects().length>1).map(x=>x.textContent)}));
   assert.equal(r.bts.length,2,'guia: botões das duas sessões');
   for(const bs of r.bts){if(w<480)assert(bs.every(x=>x[0]===bs[0][0])&&bs[1][1]>bs[0][1]&&bs[2][1]>bs[1][1],'guia: botões numa coluna a '+w+' px: '+JSON.stringify(bs));
    else assert(bs.every(x=>x[1]===bs[0][1]),'guia: botões numa fila a '+w+' px: '+JSON.stringify(bs))}
   assert.deepEqual(r.partidos,[],'guia: rótulo a negro partido a '+w+' px');assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  for(const w of [320,360,390]){const {ctx,p}=await abrir(b,base+'narrativas/ideias/guiao/',w,800,'light');
   const r=await p.evaluate(()=>{const pp=[...document.querySelectorAll('p.campo')].find(x=>x.textContent.startsWith('O teu palpite'));const t=[...pp.querySelectorAll('i.b')].map(i=>Math.round(i.getBoundingClientRect().top));
    const th=[...document.querySelectorAll('th')].find(x=>x.textContent.startsWith('Confirmado'));const n=th.firstChild,s=n.textContent,i=s.indexOf('grupo');const r1=document.createRange();r1.setStart(n,i);r1.setEnd(n,i+5);const r2=document.createRange();r2.setStart(n,s.length-3);r2.setEnd(n,s.length);
    return {t,grupo:Math.round(r1.getBoundingClientRect().top),tracos:Math.round(r2.getBoundingClientRect().top)}});
   assert.equal(r.t[2],r.t[3],'guião: «(grupos ___ e ___)» partido a '+w+' px');assert.equal(r.grupo,r.tracos,'guião: o «___» do cabeçalho sozinho a '+w+' px');await ctx.close()}
  {const d=JSON.parse(fs.readFileSync(path.join(ROOT,'tools/licoes/ideias-s02.json'),'utf8'));const {ctx,p,erros}=await abrir(b,base+d.saida.replace(/index\.html$/,''),360,740,'dark');
   for(let i=0;i<15;i++){const x=d.cartoes[i];if(x.t!=='ler'){const txt=(await p.locator('#baralho').innerText()).replace(/\s+/g,' ');const c=d.cartoes.filter(y=>y.t!=='ler'&&[y.p,y.p2].some(t=>t&&txt.includes(vis(t).slice(0,50))));await responder(p,c.length===1?c[0]:x)}await seguinte(p)}
   await responder(p,d.cartoes[15]);
   const r=await p.evaluate(()=>{const e=document.querySelector('#baralho .inline');const ss=[...e.querySelectorAll('select')];const rg=document.createRange();rg.selectNodeContents(e.lastChild);return {txt:e.lastChild.textContent,sel:ss[ss.length-1].getBoundingClientRect().bottom,aspas:rg.getBoundingClientRect().top}});
   assert(r.txt==='»'&&r.aspas<r.sel,'sessão 2, cartão 16: o «»» sozinho numa linha a 360 px ('+JSON.stringify(r)+')');assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  console.log('PASS quarta revisão: escala dos títulos da entrada, gesto na projeção a 960 a 1099 px, medida de 34 em, botões e rótulos do guia, guião no telemóvel, «»» do cartão 16')}
 // 9. 30/10/2026: as correções da quinta revisão (01/11): nas lições, o título dos cartões a 21 px (o rótulo em caixa alta fica
 // abaixo de 65 % do título, regra R2 da medida da hierarquia) e equilibrado (nenhuma palavra sozinha na última linha); na
 // entrada, o gesto numa coluna no ecrã a partir de 1080 px, com o pé da tabela de museu no pé da imagem, e três colunas abaixo
 // disso e na projeção a partir de 1100 px; na projeção abaixo de 600 px, «As sete sessões» numa linha, os rótulos da faixa só
 // para o leitor de ecrã e a proporção 2:2:3; nas três páginas, 24 px de margem lateral a partir de 768 px
 {for(const [f,w,h,tema] of [['ideias-s01.json',390,844,'light'],['ideias-s02.json',1366,900,'dark']]){const d=JSON.parse(fs.readFileSync(path.join(ROOT,'tools/licoes/'+f),'utf8'));
   const {ctx,p,erros}=await abrir(b,base+d.saida.replace(/index\.html$/,''),w,h,tema);await seguinte(p);
   const r=await p.evaluate(()=>{const t=document.querySelector('#baralho h2.tit:not(.cartaz)'),o=document.querySelector('#baralho .rot');const cs=getComputedStyle(t);return {tit:parseFloat(cs.fontSize),rot:parseFloat(getComputedStyle(o).fontSize),wrap:cs.textWrapStyle||cs.textWrap}});
   assert(r.rot/r.tit<=0.65&&r.tit>=20.9,f+': rótulo a '+(r.rot/r.tit).toFixed(2)+' do título a '+w+' px ('+JSON.stringify(r)+')');assert.equal(r.wrap,'balance',f+': título dos cartões sem equilíbrio');
   assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  for(const [w,q,col] of [[1024,'',3],[1079,'',3],[1080,'',1],[1366,'',1],[1440,'',1],[1366,'?projetar=1',3]]){const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/'+q,w,900,w===1366?'dark':'light');
   const r=await p.evaluate(()=>{const bs=[...document.querySelectorAll('[data-gesto] button[data-op]')].map(x=>x.getBoundingClientRect());const c=document.querySelector('.atol .campo').getBoundingClientRect(),f=document.querySelector('.atol figcaption').getBoundingClientRect();
    return {esq:new Set(bs.map(x=>Math.round(x.left))).size,alt:Math.max(...bs.map(x=>Math.round(x.height))),pe:Math.round(Math.abs(f.bottom-c.bottom))}});
   assert.equal(r.esq,col,'entrada: o gesto em '+r.esq+' colunas a '+w+' px'+q+' (esperadas '+col+')');if(col===1)assert(r.alt<=52,'entrada: botão do gesto em duas linhas a '+w+' px');
   // o pé alinhado de 1080 a 1440 px mediu-se com a Gelasio (as métricas da Georgia) e a Bebas Neue; com a letra de recurso do
   // Chromium de teste a coluna da esquerda muda de altura, por isso aqui só se confirma a 1366 e a 1440 px
   if(!q&&w>=1366)assert(r.pe<=1,'entrada: o pé da tabela de museu a '+r.pe+' px do pé da imagem a '+w+' px');assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  for(const [w,tema] of [[320,'light'],[360,'dark'],[599,'light']]){const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/?projetar=1',w,800,tema);
   const r=await p.evaluate(()=>{const h=document.querySelector('#sessoes');const rg=document.createRange();rg.selectNodeContents(h);const cols=[...document.querySelectorAll('.faixa a')].map(a=>a.getBoundingClientRect().width);
    return {linhas:new Set([...rg.getClientRects()].map(x=>Math.round(x.top))).size,nomes:[...document.querySelectorAll('.faixa .nome')].map(n=>Math.round(n.getBoundingClientRect().width)),prop:+(cols[2]/cols[0]).toFixed(2),igual:Math.abs(cols[0]-cols[1])<1,rel:parseFloat(getComputedStyle(h).fontSize)/parseFloat(getComputedStyle(document.querySelector('.porta h3')).fontSize)}});
   assert.equal(r.linhas,1,'projeção: «As sete sessões» em '+r.linhas+' linhas a '+w+' px');assert(r.nomes.every(x=>x<=1),'projeção: rótulos da faixa à vista a '+w+' px');
   assert(r.igual&&r.prop>=1.45&&r.prop<=1.55,'projeção: a faixa fora da proporção 2:2:3 a '+w+' px ('+r.prop+')');assert(r.rel>=1.249,'projeção: h2 só '+r.rel.toFixed(2)+' vezes os nomes das portas a '+w+' px');
   assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  for(const pag of ['narrativas/ideias/','narrativas/ideias/guiao/','narrativas/ideias/docente/'])for(const [w,x] of [[390,16],[768,24],[1024,24]]){const {ctx,p,erros}=await abrir(b,base+pag,w,800,'light');
   const r=await p.evaluate(()=>[Math.round(document.querySelector('h1').getBoundingClientRect().left),Math.round(window.innerWidth-document.querySelector('.migalhas').getBoundingClientRect().right)]);
   assert.deepEqual(r,[x,x],pag+': margem lateral de '+r.join('/')+' px a '+w+' px (esperados '+x+')');assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  console.log('PASS quinta revisão: título dos cartões a 21 px e equilibrado, gesto numa coluna a partir de 1080 px, projeção abaixo de 600 px, margem de 24 px a partir de 768 px')}
 // 10. 30/10/2026: as correções da sexta revisão (01/11): na projeção, de 960 a 1099 px, a tabela de museu colada à imagem (logo
 // abaixo dela e alinhada à sua margem), e não 20 px abaixo do gesto, na coluna da direita; no ecrã e na projeção a partir de
 // 1100 px fica na coluna da direita, como estava; na projeção, de 380 a 469 px, o gesto numa coluna (cada botão numa linha) e
 // três colunas a partir de 470 px; «sessão N» inseparável no botão da região «A seguir» («Começar», «Continuar» e «Rever»)
 {for(const [w,tema] of [[960,'light'],[1024,'dark'],[1099,'light']]){const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/?projetar=1',w,768,tema);
   const r=await p.evaluate(()=>{const c=document.querySelector('.atol .campo').getBoundingClientRect(),f=document.querySelector('.atol figcaption').getBoundingClientRect();return {dy:Math.round(f.top-c.bottom),dx:Math.round(f.left-c.left)}});
   assert(r.dy>=0&&r.dy<=12&&Math.abs(r.dx)<=1,'projeção: a tabela de museu descolada da imagem a '+w+' px ('+JSON.stringify(r)+')');assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  for(const [w,q] of [[1024,''],[1099,''],[1100,'?projetar=1'],[1366,'?projetar=1']]){const {ctx,p}=await abrir(b,base+'narrativas/ideias/'+q,w,800,'light');
   const r=await p.evaluate(()=>{const c=document.querySelector('.atol .campo').getBoundingClientRect(),f=document.querySelector('.atol figcaption').getBoundingClientRect();return f.left-c.right});
   assert(r>=20,'entrada: a tabela de museu saiu da coluna da direita a '+w+' px'+q);await ctx.close()}
  for(const [w,col] of [[380,1],[390,1],[469,1],[470,3]]){const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/?projetar=1',w,844,w===390?'dark':'light');
   const lin=()=>p.evaluate(()=>{const bs=[...document.querySelectorAll('[data-gesto] button[data-op]')];return {esq:new Set(bs.map(x=>Math.round(x.getBoundingClientRect().left))).size,alt:Math.max(...bs.map(x=>Math.round(x.getBoundingClientRect().height)))}});
   let r=await lin();assert.equal(r.esq,col,'projeção: o gesto em '+r.esq+' colunas a '+w+' px (esperadas '+col+')');if(col===1)assert(r.alt<=52,'projeção: botão do gesto em mais de uma linha a '+w+' px');
   await p.locator('[data-gesto] button[data-op]').nth(1).click();await p.waitForTimeout(200);r=await lin();if(col===1)assert(r.alt<=52,'projeção: «✓ Tenho um palpite» em mais de uma linha a '+w+' px');
   assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  for(const [w,q,prep,txt] of [[320,'?projetar=1',null,'Começar a sessão 1 →'],[340,'?projetar=1',null,'Começar a sessão 1 →'],[320,'',{content:"localStorage.setItem('epi-lab-ideias-s01',"+JSON.stringify(JSON.stringify(FEITA1))+")"},'Continuar na sessão 2 →']]){
   const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/'+q,w,640,'light',prep);
   const r=await p.evaluate(()=>{const a=document.querySelector('[data-p-botao]'),n=a.firstChild,t=n.textContent,top=i=>{const g=document.createRange();g.setStart(n,i);g.setEnd(n,i+1);return Math.round(g.getBoundingClientRect().top)};const i=t.indexOf('sessão');return {t,junto:top(i)===top(i+7)}});
   assert.equal(r.t,txt,'entrada: o texto do botão a '+w+' px'+q);assert(r.junto,'entrada: o número da sessão separado de «sessão» a '+w+' px'+q);assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  console.log('PASS sexta revisão: tabela de museu colada à imagem na projeção de 960 a 1099 px, gesto numa coluna na projeção de 380 a 469 px, «sessão N» inseparável no botão')}
 // 10. (continuação) 01/11/2026: a correção da sétima revisão (diretor de arte, 01/11): quando a coluna da direita é mais alta
 // do que a abertura com a imagem a 16:9, a imagem do atol estica até ao pé da tabela de museu (nunca abaixo de 16:9). O pé da
 // tabela fica a 0 a 3 px do pé da imagem na projeção a 1100, 1160 e 1220 px (descia 81, 61 e 42 px) e no ecrã a 1100 px com a
 // sessão 1 feita (descia 31 px); a tabela continua na coluna da direita e a imagem nunca fica mais baixa do que 16:9
 {const prep={content:"localStorage.setItem('epi-lab-ideias-s01',"+JSON.stringify(JSON.stringify(FEITA1))+")"};
  for(const [w,q,pr,tema] of [[1100,'?projetar=1',null,'light'],[1160,'?projetar=1',null,'dark'],[1220,'?projetar=1',null,'light'],[1100,'',prep,'dark']]){
   const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/'+q,w,900,tema,pr);
   const r=await p.evaluate(()=>{const c=document.querySelector('.atol .campo').getBoundingClientRect(),f=document.querySelector('.atol figcaption').getBoundingClientRect(),i=document.querySelector('.atol img').getBoundingClientRect();
    return {pe:Math.round(f.bottom-c.bottom),dx:Math.round(f.left-c.right),alt:c.height,min:c.width*9/16,img:[Math.round(i.width-c.width),Math.round(i.height-c.height)]}});
   const onde=' a '+w+' px'+(q||' (ecrã, sessão 1 feita)')+' ('+JSON.stringify(r)+')';
   assert(r.pe>=0&&r.pe<=3,'entrada: o pé da tabela de museu afastado do pé da imagem'+onde);
   assert(r.dx>=20,'entrada: a tabela de museu saiu da coluna da direita'+onde);
   assert(r.alt>=r.min-1,'entrada: a imagem do atol mais baixa do que 16:9'+onde);
   assert.deepEqual(r.img,[0,0],'entrada: a imagem não enche o recorte'+onde);
   assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  console.log('PASS sétima revisão: o pé da tabela de museu no pé da imagem na projeção a 1100, 1160 e 1220 px e no ecrã a 1100 px com a sessão 1 feita')}
 // 10. (continuação) 01/11/2026: a correção da oitava revisão (diretor de arte, 01/11): o enquadramento da imagem do atol
 // escolhe-se à mão, pelo anel (object-position 75% 83% a partir de 960 px), e não pelo tamanho da caixa. Com 50% 55%, com o
 // gesto premido na projeção a 1100 e 1120 px (a imagem estica até 0,97:1), a ponta nordeste do anel saía até 47 px pela borda
 // direita; a 16:9, no ecrã a 1366 px, a curva de baixo saía 11 px pelo pé. Calcula a janela visível da fotografia em píxeis da
 // fonte (object-fit:cover, naturalWidth e naturalHeight, a caixa da imagem e o object-position calculado) e confirma que o anel
 // (na fonte de 1200 × 789: x 368 a 1042, y 107 a 757) fica todo dentro, com 0 px de fora
 {for(const [w,q,tema,toque] of [[1100,'?projetar=1','light',true],[1120,'?projetar=1','dark',true],[1366,'','light',false]]){
   const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/'+q,w,900,tema);
   await p.evaluate(()=>{const i=document.querySelector('.atol img');i.loading='eager';return i.decode()});
   if(toque){await p.locator('.gesto button').nth(1).click();await p.waitForTimeout(300)}
   const r=await p.evaluate(()=>{const A={x0:368,x1:1042,y0:107,y1:757},i=document.querySelector('.atol img'),c=i.getBoundingClientRect(),nw=i.naturalWidth,nh=i.naturalHeight;
    const s=Math.max(c.width/nw,c.height/nh),vw=c.width/s,vh=c.height/s,[px,py]=getComputedStyle(i).objectPosition.split(' ').map(v=>parseFloat(v)/100),x0=(nw-vw)*px,y0=(nh-vh)*py;
    const fora={esq:x0-A.x0,dir:A.x1-(x0+vw),cima:y0-A.y0,baixo:A.y1-(y0+vh)};for(const k in fora)fora[k]=Math.max(0,+(fora[k]*s).toFixed(2));
    return {nat:[nw,nh],prop:+(c.width/c.height).toFixed(2),op:getComputedStyle(i).objectPosition,premido:document.querySelectorAll('.gesto button[aria-pressed="true"]').length,fora}});
   const onde=' a '+w+' px'+(q||' (ecrã)')+(toque?', com o gesto premido':'')+' ('+JSON.stringify(r)+')';
   assert.deepEqual(r.nat,[1200,789],'entrada: a fotografia do atol não tem 1200 × 789 píxeis'+onde);
   if(toque)assert.equal(r.premido,1,'entrada: o gesto não ficou premido'+onde);
   assert.deepEqual(r.fora,{esq:0,dir:0,cima:0,baixo:0},'entrada: o recorte corta o anel do atol'+onde);
   assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  console.log('PASS oitava revisão: o anel do atol inteiro no recorte na projeção a 1100 e 1120 px com o gesto premido e no ecrã a 1366 px')}

 // 11. 01/11/2026: o método assumido à cabeça (encargo do docente de 01/11: o método de Young como espinha, apresentado uma vez).
 // Na entrada, o bloco «O método» logo a seguir à frase de abertura, dentro da abertura, com os cinco passos numa lista numerada,
 // de 320 a 1440 px, em claro e escuro e na projeção: a partir de 960 px fica na coluna da abertura, por cima da imagem; abaixo
 // disso vem depois da região «A seguir» e do gesto, que continuam no primeiro ecrã. O rótulo da região «A seguir» diz o passo
 // («Começa aqui: passo 1 de 5»; com a sessão 1 feita, «Continuar: passo 1 de 5»; a projeção não lê o progresso). Nas lições, o
 // primeiro cartão diz «Passo 1 de 5: juntar material» e marca o passo de hoje com a palavra «hoje»; a marca da casca diz «Ideias,
 // passo 1 de 5» a partir de 600 px e «Passo 1 de 5» de 430 a 599 px (de 400 a 429 px fica «Ideias», como antes; abaixo de 400 px, só
 // a casa), sem empurrar os controlos para fora do ecrã; o <title> diz
 // o passo; e a sessão 1 apresenta Young no cartão 2, «O método»
 // 01/11/2026: (correção 1 do método, diretor de arte) nenhum passo sozinho numa linha: um por linha abaixo de 600 px e três mais
 // dois, em colunas, a partir de 600 px, na entrada e no «Abre» das lições; «passo 1 de 5» inseparável no rótulo da região «A
 // seguir» (espaços duros); «HOJE» a 13 px (17,875 px na projeção), com 0,14 em, como os rótulos de estado do sistema
 const PORLINHA='(lis=>{const g=[];for(const li of lis){const t=li.getBoundingClientRect().top;let G=g.find(x=>Math.abs(x.top-t)<4);if(!G){G={top:t,n:[]};g.push(G)}G.n.push(+li.querySelector("b").textContent)}return g.sort((a,b)=>a.top-b.top).map(x=>x.n)})';
 const linhasEsperadas=w=>w<600?[[1],[2],[3],[4],[5]]:[[1,2,3],[4,5]];
 const NB='\u00a0';
 {const PASSOS=['1 Juntar material','2 Trabalhar o material','3 Largar','4 A ideia aparece','5 Dar forma e pôr à prova'];
  for(const [w,h] of LARGURAS)for(const [tema,q] of [['light',''],['dark',''],['light','?projetar=1']]){const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/'+q,w,h,tema);
   const r=await p.evaluate(PL=>{const m=document.querySelector('.metodo'),R=s=>document.querySelector(s).getBoundingClientRect(),mm=m.getBoundingClientRect();
    return {linhas:eval(PL)([...m.querySelectorAll('ol.passos-m li')]),t:m.querySelector('h2').textContent,passos:[...m.querySelectorAll('ol.passos-m li')].map(li=>li.textContent.replace(/\s+/g,' ').trim()),alt:Math.round(mm.height),
     depoisLead:mm.top>=R('.abre .lead').bottom-0.5,acimaImg:mm.bottom<=R('.atol .campo').top+0.5,depoisGesto:mm.top>=R('.gesto').bottom-0.5,
     kicker:document.querySelector('.proximo .kicker').textContent,fora:[...m.querySelectorAll('li,p,h2')].filter(e=>e.getBoundingClientRect().right>innerWidth+0.5).length,
     cor:getComputedStyle(m.querySelector('.info')).color===getComputedStyle(document.querySelector('.abre .lead')).color}},PORLINHA);
   const onde=' a '+w+' px ('+tema+(q?', projeção':'')+'): '+JSON.stringify(r);
   assert.deepEqual(r.linhas,linhasEsperadas(w),'entrada: um passo sozinho numa linha do bloco «O método»'+onde);
   assert.equal(r.t,'O método','entrada: o título do bloco'+onde);assert.deepEqual(r.passos,PASSOS,'entrada: os cinco passos'+onde);
   assert(r.alt>60&&r.depoisLead&&r.acimaImg&&r.fora===0&&r.cor,'entrada: o bloco «O método» fora do lugar'+onde);
   if(w<960)assert(r.depoisGesto,'entrada: no telemóvel, o bloco antes do gesto'+onde);
   assert.equal(r.kicker,'Começa aqui: passo'+NB+'1'+NB+'de'+NB+'5','entrada: o rótulo da região «A seguir»'+onde);
   const bt=await p.locator('[data-p-botao]').boundingBox();if(!q)assert(bt.y+bt.height<=h,'entrada: o botão «Começar» fora do primeiro ecrã'+onde);
   assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}
  {const prep={content:"localStorage.setItem('epi-lab-ideias-s01',"+JSON.stringify(JSON.stringify(FEITA1))+")"};
   for(const q of ['','?projetar=1']){const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/'+q,390,844,'light',prep);
    assert.equal(await p.locator('.proximo .kicker').textContent(),(q?'Começa aqui: ':'Continuar: ')+['passo','1','de','5'].join(NB),'entrada: o rótulo com a sessão 1 feita'+(q?' (projeção)':''));
    assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}}
  // com as duas sessões prontas feitas, «A seguir, em preparação: passos 1 e 2 de 5», com o passo sempre numa só linha (a 1024 px
  // partia-se em «… passos 1 e 2» / «de 5»; a 390 px, em «… passos 1» / «e 2 de 5»); na projeção a 320 px, «passo 1 de 5» inteiro
  {const F2={lida:true,versao:JSON.parse(fs.readFileSync(path.join(ROOT,'tools/licoes/ideias-s02.json'),'utf8')).versao,t:Date.parse('2026-11-14T10:00:00'),melhor:12};
   const prep={content:"localStorage.setItem('epi-lab-ideias-s01',"+JSON.stringify(JSON.stringify(FEITA1))+");localStorage.setItem('epi-lab-ideias-s02',"+JSON.stringify(JSON.stringify(F2))+")"};
   for(const [w,h,q,pr,txt] of [[320,640,'',prep,'A seguir, em preparação: '+['passos','1','e','2','de','5'].join(NB)],[390,844,'',prep,'A seguir, em preparação: '+['passos','1','e','2','de','5'].join(NB)],
                                [1024,768,'',prep,'A seguir, em preparação: '+['passos','1','e','2','de','5'].join(NB)],[320,640,'?projetar=1',null,'Começa aqui: '+['passo','1','de','5'].join(NB)],
                                [360,740,'?projetar=1',null,'Começa aqui: '+['passo','1','de','5'].join(NB)]]){
    const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/'+q,w,h,'light',pr);
    const r=await p.evaluate(()=>{const k=document.querySelector('.proximo .kicker'),sp=k.querySelector('[data-p-passo]'),n=sp.firstChild,rg=document.createRange();rg.setStart(n,2);rg.setEnd(n,n.textContent.length);
     const tops=[...new Set([...rg.getClientRects()].filter(x=>x.width>0).map(x=>Math.round(x.top)))];return {txt:k.textContent,linhasPasso:tops.length}});
    const onde=' a '+w+' px'+(q?' (projeção)':'')+': '+JSON.stringify(r);
    assert.equal(r.txt,txt,'entrada: o rótulo da região «A seguir»'+onde);assert.equal(r.linhasPasso,1,'entrada: o passo partido no rótulo'+onde);
    assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close()}}
  for(const f of ['ideias-s01.json','ideias-s02.json']){const d=JSON.parse(fs.readFileSync(path.join(ROOT,'tools/licoes',f),'utf8'));const url=base+d.saida.replace(/index\.html$/,'');
   for(const [w,tema,q,nome,passo] of [[320,'light','',false,false],[390,'dark','',false,false],[400,'dark','',true,false],[429,'light','',true,false],[430,'dark','',false,true],[599,'light','',false,true],
                                       [600,'dark','',true,true],[1024,'light','',true,true],[1366,'dark','',true,true],[1440,'light','',true,true],[1366,'light','?projetar=1',true,true]]){
    const {ctx,p,erros}=await abrir(b,url+q,w,800,tema);
    const r=await p.evaluate(PL=>{const vis=e=>{const x=e.getBoundingClientRect();return x.width>2&&x.height>2};const m=document.querySelector('.c-marca'),mr=m.getBoundingClientRect(),cp=document.querySelector('.c-marca-p');
     const hoje=[...document.querySelectorAll('#baralho ol.passos-m li[aria-current="step"]')],ht=getComputedStyle(document.querySelector('#baralho .hoje-t'));
     return {passos:eval(PL)([...document.querySelectorAll('#baralho ol.passos-m li')]),hojeT:[parseFloat(ht.fontSize),+(parseFloat(ht.letterSpacing)/parseFloat(ht.fontSize)).toFixed(3)],nome:vis(document.querySelector('.c-marca-t')),passo:vis(cp),virgula:getComputedStyle(cp,'::before').content,txt:cp.textContent,marca:[Math.round(mr.width),Math.round(mr.height)],
      fora:[...document.querySelectorAll('.casca-topo a,.casca-topo button')].filter(e=>e.offsetParent!==null&&e.getBoundingClientRect().right>innerWidth+0.5).length,
      titulo:document.title,abre:document.querySelector('#baralho').innerText.replace(/\s+/g,' '),hoje:hoje.map(li=>li.innerText.replace(/\s+/g,' ').trim()),
      linha:[...document.querySelectorAll('#baralho ol.passos-m li')].filter(li=>li.getBoundingClientRect().right>document.querySelector('#baralho').getBoundingClientRect().right+0.5).length}},PORLINHA);
    const onde=d.id+' a '+w+' px ('+tema+(q?', projeção':'')+'): '+JSON.stringify(r).slice(0,400);
    assert.equal(r.nome,nome,'lição: o nome «Ideias» na barra, '+onde);assert.equal(r.passo,passo,'lição: o passo na barra, '+onde);
    if(passo)assert.equal(r.txt,'Passo 1 de 5',onde);if(nome&&passo)assert.match(r.virgula,/^", "/,'lição: a vírgula entre o nome e o passo, '+onde);
    assert.equal(r.fora,0,'lição: controlos da barra fora do ecrã, '+onde);assert(r.marca[0]>=44&&r.marca[1]>=44,'lição: a marca com menos de 44 px, '+onde);
    assert.match(r.titulo,/\(passo 1 de 5\) \| Ideias \| Laboratório \| Lente$/,onde);
    assert.match(r.abre,/Passo 1 de 5: juntar material/,'lição: o primeiro cartão sem o passo, '+onde);
    assert.deepEqual(r.hoje,['1 Juntar material HOJE'],'lição: o passo de hoje marcado com texto, '+onde);
    assert.deepEqual(r.passos,linhasEsperadas(w),'lição: um passo sozinho numa linha do «Abre», '+onde);
    assert(r.hojeT[0]>=(q?17.875:13)&&Math.abs(r.hojeT[1]-0.14)<0.005,'lição: «HOJE» abaixo da letra mínima ou sem o espaçamento do rótulo de estado, '+onde);assert.equal(r.linha,0,'lição: a linha dos passos sai do cartão, '+onde);
    if(f==='ideias-s01.json'&&!q&&(w===390||w===1366)){await seguinte(p);const t=(await p.locator('#baralho').innerText()).replace(/\s+/g,' ');
     assert.match(t,/O MÉTODO/i,'sessão 1: o cartão 2 é «O método», '+onde);assert.match(t,/James Webb Young foi um publicitário norte-americano/,'sessão 1: a apresentação de Young, '+onde);
     assert.equal(await p.locator('[data-c-num]').innerText(),'2/'+d.cartoes.length)}
    assert.equal(await largo(p),0,'lição: deslize, '+onde);assert.deepEqual(erros,[]);await ctx.close()}}
  console.log('PASS método: o bloco «O método» na entrada (5 larguras, claro, escuro e projeção), «Passo 1 de 5» na região «A seguir», no primeiro cartão, na barra a partir de 430 px e no título, e a apresentação de Young na sessão 1; nenhum passo sozinho numa linha, o passo inteiro no rótulo e «HOJE» a 13 px')}
 await b.close();srv.close()})().catch(e=>{console.error(e);process.exit(1)});
