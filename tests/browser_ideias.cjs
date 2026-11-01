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
   // 30/10/2026: na quarta revisão (01/11), as ligações passam a bloco (com inline-block a marca da lista alinhava pela última
   // linha); sem inline-flex, como antes
   assert.deepEqual(x.nums,[],'guia: minutos por cima da borda a '+w+' px');assert(x.lig.length&&x.lig.every(d=>d==='block'),'guia: ligações em '+x.lig.join(','));
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
 await b.close();srv.close()})().catch(e=>{console.error(e);process.exit(1)});
