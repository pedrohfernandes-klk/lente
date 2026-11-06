// 30/10/2026: lições do Lente no motor único (assets/licoes/), a começar pela sessão 01 do M1 de Cidadania (piloto).
// 30/10/2026: cobre também as lições do coração do Laboratório («Ideias», narrativas/ideias/, 31/10), com os cartões «mapa»
// sobre o quadro de La Tour (a lupa incluída) e o leitor do vídeo, que só se liga ao toque.
// Percorre cada lição de tools/licoes/*.json a responder certo a todos os cartões, em 390 e 1366 px, e confirma: nenhum
// erro, nenhum deslocamento horizontal, o fim com todas as certas, o progresso gravado na chave da lição, e a projeção a
// não gravar nada.
// 05/11/2026: plano do molde da Cidadania, pedido 1 (motor, casca e progresso). Nas sessões da Cidadania (cfg da família): a
// ordem das opções de cada escolha é a da semente do motor (tools/licoes_lente.py --ordem), igual em todos os ecrãs; recarregar
// a meio volta ao mesmo cartão; o fim diz «Sessão feita.» e «O módulo já a marca.», sem pontos (a contagem guardada continua a
// ser exigida). Um estado antigo semeado no localStorage continua «Feita» na página do módulo, antes e depois de abrir a sessão
// com outra versão. A lição de ensaio do molde (tests/fixtures/molde_ensaio.py, servida só neste teste, nunca publicada) prova
// as peças novas: posições e artefactos (copiar), o «i» e a ampliação com o teclado, a retoma, a projeção sem gravar nada.
const {chromium}=require('playwright');const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert'),{spawnSync}=require('child_process');
const ROOT=path.resolve(__dirname,'..');
const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript','.json':'application/json','.css':'text/css','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.jpg':'image/jpeg'};
function py(args){const r=spawnSync('python3',args,{cwd:ROOT,encoding:'utf8',maxBuffer:1<<26});if(r.status!==0)throw new Error(r.stderr);return r.stdout}
const ENSAIO_URL='/cidadania/piloto/ensaio-molde/';
const ENSAIO=JSON.parse(py(['-c','import sys,json;sys.path.insert(0,"tests/fixtures");import molde_ensaio as E;d=E.licao();print(json.dumps({"d":d,"html":E.L.pagina(d)}))']));
const CAPTURAS=process.env.MOLDE_CAPTURAS||'';
const srv=http.createServer((q,r)=>{let u=decodeURIComponent(q.url.split('?')[0]);if(u===ENSAIO_URL){r.writeHead(200,{'content-type':mime['.html']});r.end(ENSAIO.html);return}if(u.endsWith('/'))u+='index.html';const f=path.join(ROOT,u);if(!f.startsWith(ROOT)||!fs.existsSync(f)){r.writeHead(404);r.end();return}r.writeHead(200,{'content-type':mime[path.extname(f)]||'application/octet-stream'});fs.createReadStream(f).pipe(r)});
async function seguinte(p){const s=p.locator('.casca-folha:not([hidden]) button, .casca-acoes button',{hasText:/Seguinte|Continuar|Ver o resultado|Terminar/});await s.first().click();await p.waitForTimeout(250)}
// 30/10/2026: o texto dos botões é o das opções sem as marcas de itálico e negrito (_…_ e **…**), que o motor converte
// (coração do Laboratório, 31/10: «_Time Transfixed_, de René Magritte.»).
const vis=s=>String(s).replace(/\*\*|_/g,'');
// 30/10/2026: o cartão «mapa» (coração do Laboratório, 31/10: «Toca no quadro»). Toca-se no centro do anel da zona certa,
// como um dedo: o motor procura a zona mais próxima do toque. Se duas zonas ficam a menos de 44 px no ecrã, o primeiro toque
// abre a lupa (a figura amplia-se à volta do dedo) e é preciso tocar outra vez; o «Confirmar» fica para o fim de responder().
async function tocarZona(p,j){const box=await p.locator('#baralho .op-m[data-j="'+j+'"] circle.anel').boundingBox();await p.mouse.click(box.x+box.width/2,box.y+box.height/2);await p.waitForTimeout(250)}
async function responder(p,x){
 if(x.t==='escolha'){await p.locator('#baralho button.op',{hasText:vis(x.o[x.c])}).first().click()}
 else if(x.t==='mapa'){await tocarZona(p,x.c);if(await p.locator('#baralho .mapa-q svg.lupa').count())await tocarZona(p,x.c);assert.match(await p.locator('#baralho .mapa-esc').innerText(),new RegExp(x.o[x.c].replace(/[.*+?^${}()|[\]\\]/g,'\\$&')),'zona escolhida: '+x.o[x.c])}
 else if(x.t==='vf'){await p.locator('#baralho button.op',{hasText:x.v?'Verdadeiro':'Falso'}).click()}
 else if(x.t==='emparelhar'){for(const [a,b] of x.pares){await p.locator('#baralho button',{hasText:vis(a)}).first().click();await p.waitForTimeout(80);await p.locator('#baralho button',{hasText:vis(b)}).first().click();await p.waitForTimeout(120)}}
 else if(x.t==='sublinhar'){for(const j of x.certas)await p.locator('#baralho button.pal[data-j="'+j+'"]').click();await p.locator('.casca-acoes [data-confirmar]').click()}
 else if(x.t==='ordenar'){for(const t of x.passos){await p.locator('#baralho .soltos button',{hasText:vis(t)}).first().click();await p.waitForTimeout(80)}}
 // 30/10/2026: as sessões 02 a 10 do M1 (pilotos de 31/10) têm cartões de completar; em cada lacuna escolhe-se o valor da
 // opção certa, como o motor o guarda (o valor é o índice da opção em lacunas[k].o; data-k é a ordem da lacuna na frase).
 else if(x.t==='completar'){for(let k=0;k<x.lacunas.length;k++){await p.locator('#baralho select[data-k="'+k+'"]').selectOption(String(x.lacunas[k].c));await p.waitForTimeout(80)}}
 else throw new Error('tipo sem resposta automática: '+x.t);
 await p.waitForTimeout(350);
 const conf=p.locator('.casca-acoes [data-confirmar]');if(await conf.count()&&await conf.isVisible()&&await conf.isEnabled())await conf.click();
 await p.waitForTimeout(250);
}
(async()=>{await new Promise(r=>srv.listen(0,r));const base='http://localhost:'+srv.address().port;const b=await chromium.launch();
 // 05/11/2026: LICOES_FILTRO (expressão regular sobre o nome do .json) escolhe as lições, para ensaiar; sem ela, correm todas.
 const FILTRO=new RegExp(process.env.LICOES_FILTRO||'.');
 for(const f of fs.readdirSync(path.join(ROOT,'tools/licoes')).filter(f=>f.endsWith('.json')&&FILTRO.test(f))){
  const d=JSON.parse(fs.readFileSync(path.join(ROOT,'tools/licoes',f),'utf8'));const url=base+'/'+d.saida.replace(/index\.html$/,'');
  const fazer=d.cartoes.filter(x=>x.t!=='ler').length;
  // 05/11/2026: na Cidadania, a ordem fixa das opções (cfg.aula), calculada com a semente do motor pelo gerador
  const cid=d.familia!=='laboratorio',ORDEM=cid?new Map(JSON.parse(py(['tools/licoes_lente.py','--ordem','tools/licoes/'+f]))[d.chave]):new Map();
  for(const [w,h] of [[390,844],[1366,900]]){
   const ctx=await b.newContext({viewport:{width:w,height:h}});const p=await ctx.newPage();const erros=[];p.on('pageerror',e=>erros.push(e.message));
   await p.goto(url);await p.waitForTimeout(500);
   // o motor baralha os cartões de fazer do mesmo grupo «g» e alterna p/p2: o cartão do ecrã identifica-se pelo enunciado
   const norm=t=>String(t||'').replace(/<[^>]+>/g,' ').replace(/[*_]/g,'').replace(/\s+/g,' ').trim();
   async function atual(i){const txt=norm(await p.locator('#baralho').innerText());const c=d.cartoes.filter(x=>x.t!=='ler'&&[x.p,x.p2].some(q=>q&&txt.includes(norm(q).slice(0,60))));return c.length===1?c[0]:d.cartoes[i]}
   for(let i=0;i<d.cartoes.length;i++){
    // 05/11/2026: retoma a meio. No 5.º cartão, a 390 px, recarrega-se a página: volta ao mesmo cartão, com o aviso.
    if(cid&&w===390&&i===4){await p.reload();await p.waitForTimeout(600);assert.match(await p.locator('#aviso').innerText(),/Continuas no cartão 5\./,f+': aviso da retoma')}
    const x=d.cartoes[i].t==='ler'?d.cartoes[i]:await atual(i);
    assert.equal(await p.locator('[data-c-num]').innerText(),(i+1)+'/'+d.cartoes.length,f+' cartão '+(i+1));
    assert(await p.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),'deslocamento horizontal no cartão '+(i+1)+' a '+w+' px');
    if(cid&&x.t==='escolha'){const j=await p.$$eval('#baralho .ops button.op',bs=>bs.map(b=>+b.dataset.j));assert.deepEqual(j,ORDEM.get(d.cartoes.indexOf(x)),f+' cartão '+(i+1)+': a ordem das opções é a da semente do motor')}
    // 05/11/2026: correções da revisão da s01 (06/11/2026). No molde, cada exercício mostra a sua pista (nunca a escolhida por
    // palavras) e nenhum passo de um ordenar aparece no seu lugar.
    if(cid&&d.molde&&x.t!=='ler'&&w===390){const b=p.locator('.casca-acoes [data-pista-ess]');assert.equal(await b.count(),1,f+' cartão '+(i+1)+': botão «Pista»');await b.click();await p.waitForTimeout(150);
     assert.equal(norm(await p.locator('#baralho .pista').innerText()),norm('Pista: '+vis(x.pista)),f+' cartão '+(i+1)+': a pista do cartão')}
    if(cid&&d.molde&&x.t==='ordenar'){const j=await p.$$eval('#baralho .soltos button.op',bs=>bs.map(b=>+b.dataset.j));assert(j.length===x.passos.length&&j.every((v,q)=>v!==q),f+' cartão '+(i+1)+': nenhum passo no seu lugar '+j)}
    if(x.t!=='ler'){await responder(p,x);assert.match(await p.locator('.casca-folha').innerText(),/Certo/,f+' cartão '+(i+1)+' ('+x.t+')')}
    if(i<d.cartoes.length-1)await seguinte(p);
   }
   await seguinte(p).catch(()=>{});await p.waitForTimeout(1400); // o «x de y» do fim anima durante cerca de 900 ms
   const fim=await p.locator('#baralho').innerText();
   // 02/11/2026: sem pontos no Laboratório; mantém-se abaixo a prova da contagem guardada.
   if(d.familia==='laboratorio'){assert.match(fim,/Lição feita/);assert.doesNotMatch(fim,/\d+\s+(?:pontos|de\s+\d+)/)}
   // 05/11/2026: plano do molde da Cidadania, pedido 1. A Cidadania também deixa de mostrar pontos (cfg.semPontos): o fim diz
   // «Sessão feita.» e «O módulo já a marca.»; a prova de que tudo ficou certo passa a ser só a contagem guardada, logo abaixo
   // (st.melhor igual ao número de cartões de fazer), que continua obrigatória.
   // 05/11/2026: correções da revisão da s01 (06/11/2026): nas sessões no molde, o fim diz «A página do módulo já a marca como feita.»
   else{assert.match(fim,/Sessão feita\./,f+': o fim diz «Sessão feita.»');assert.match(fim,d.molde?/A página do módulo já a marca como feita\./:/O módulo já a marca\./,f+': o fim diz que o módulo já a conta');assert.doesNotMatch(fim,/\d+\s+(?:pontos|de\s+\d+)/,f+': sem pontos')}
   const st=await p.evaluate(k=>JSON.parse(localStorage.getItem(k)||'null'),d.chave);assert(st&&st.melhor===fazer,f+': progresso gravado em '+d.chave);
   if(cid)assert.equal(st.curso,undefined,f+': o fim apaga a retoma');
   if(w===390)await p.screenshot({path:path.join(require('os').tmpdir(),'licao-'+d.id+'-fim-390.png')});
   assert.deepEqual(erros,[],f+' a '+w+' px');await ctx.close();
   // projeção (?projetar=1): começa do início e não grava nada neste aparelho
   const c2=await b.newContext({viewport:{width:w,height:h}});const p2=await c2.newPage();await p2.goto(url+'?projetar=1');await p2.waitForTimeout(500);
   assert.equal(await p2.locator('[data-c-num]').innerText(),'1/'+d.cartoes.length,f+': a projeção começa no primeiro cartão');
   for(let i=0;i<4;i++){const s=p2.locator('.casca-acoes button',{hasText:/Seguinte/});if(await s.count()&&await s.first().isEnabled()){await s.first().click();await p2.waitForTimeout(200)}}
   assert.equal(await p2.evaluate(k=>localStorage.getItem(k),d.chave),null,f+': a projeção não grava progresso');await c2.close();
   console.log('PASS '+d.id+': '+d.cartoes.length+' cartões, '+fazer+' de fazer, todos certos, fim e progresso a '+w+' px');
  }
 }
 // 05/11/2026: plano do molde da Cidadania, pedido 1. Estado antigo semeado (outra versão, concluída): a página do módulo
 // mostra «Feita»; abrir a sessão leva a conclusão para «antes» (preservarAnterior) e a página continua a mostrá-la; na
 // projeção, a página não lê nada e a sessão não grava nada.
 {const K='epi-cid-m1-s01',antiga={versao:'versao-antiga',lida:true,t:1700000000000,melhor:11,totalMelhor:12,tentativas:2,exposicoes:{3:2}};
  for(const proj of [false,true]){
   const c=await b.newContext({viewport:{width:390,height:844}}),p=await c.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));
   await c.addInitScript(([K,v])=>{if(!sessionStorage.getItem('semeado')){localStorage.setItem(K,JSON.stringify(v));sessionStorage.setItem('semeado','1')}},[K,antiga]);
   const q=proj?'?projetar=1':'';
   await p.goto(base+'/cidadania/piloto/m1/'+q);await p.waitForTimeout(300);
   const estado=()=>p.locator('li[data-chave="'+K+'"] [data-estado]').textContent(); // o texto do DOM (o CSS põe-no em maiúsculas)
   if(proj)assert.equal(await estado(),'A seguir','projeção: a página do módulo não lê o progresso');
   else{assert.match(await estado(),/^Feita 14\/11$/,'estado antigo: «Feita» com a data da conclusão');assert.match(await p.locator('[data-contagem]').textContent(),/^1 de 10/)}
   // 05/11/2026 (plano do molde, pedido 2): a sessão 01 passou à versão final, no endereço que a turma já usa
   // (cidadania/m1/sessoes/01/), com a mesma chave; é para lá que a página do módulo leva, e é lá que a migração se prova.
   await p.goto(base+'/cidadania/m1/sessoes/01/'+q);await p.waitForTimeout(500);
   const st=await p.evaluate(K=>JSON.parse(localStorage.getItem(K)),K);
   if(proj)assert.deepEqual(st,antiga,'projeção: a sessão não grava');
   else{assert.equal(st.antes.lida,true);assert.equal(st.antes.data,antiga.t);assert.equal(st.exposicoes,undefined);assert.notEqual(st.versao,antiga.versao)}
   await p.goto(base+'/cidadania/piloto/m1/'+q);await p.waitForTimeout(300);
   if(!proj)assert.match(await estado(),/^Feita 14\/11$/,'depois de abrir a sessão com outra versão, continua «Feita»');
   assert.deepEqual(erros,[]);await c.close();console.log('PASS estado antigo semeado: «Feita» na página do módulo'+(proj?' (projeção: nada lido nem gravado)':''));
  }}
 // 06/11/2026 (decisão 166): o mesmo para a sessão 02, que passou à versão final em cidadania/m1/sessoes/02/ com a chave do
 // piloto (epi-cid-m1-s02): um estado antigo concluído (a versão do piloto, 2026-10-31-2) continua «Feita» depois de abrir a
 // sessão nova; na projeção, nada se lê nem se grava (a s02 não é a próxima por fazer, por isso o estado fica vazio).
 {const K='epi-cid-m1-s02',antiga={versao:'2026-10-31-2',lida:true,t:1700000000000,melhor:15,totalMelhor:16,tentativas:1,exposicoes:{4:1}};
  for(const proj of [false,true]){
   const c=await b.newContext({viewport:{width:390,height:844}}),p=await c.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));
   await c.addInitScript(([K,v])=>{if(!sessionStorage.getItem('semeado')){localStorage.setItem(K,JSON.stringify(v));sessionStorage.setItem('semeado','1')}},[K,antiga]);
   const q=proj?'?projetar=1':'';
   await p.goto(base+'/cidadania/piloto/m1/'+q);await p.waitForTimeout(300);
   const estado=()=>p.locator('li[data-chave="'+K+'"] [data-estado]').textContent();
   assert.equal(await p.locator('li[data-chave="'+K+'"] a').getAttribute('href'),'../../m1/sessoes/02/','a página do módulo leva à s02 nova');
   if(proj)assert.equal(await estado(),'','projeção: a página do módulo não lê o progresso');
   else assert.match(await estado(),/^Feita 14\/11$/,'s02, estado antigo: «Feita» com a data da conclusão');
   await p.goto(base+'/cidadania/m1/sessoes/02/'+q);await p.waitForTimeout(500);
   const st=await p.evaluate(K=>JSON.parse(localStorage.getItem(K)),K);
   if(proj)assert.deepEqual(st,antiga,'projeção: a s02 não grava');
   else{assert.equal(st.antes.lida,true);assert.equal(st.antes.data,antiga.t);assert.equal(st.exposicoes,undefined);assert.notEqual(st.versao,antiga.versao)}
   await p.goto(base+'/cidadania/piloto/m1/'+q);await p.waitForTimeout(300);
   if(!proj)assert.match(await estado(),/^Feita 14\/11$/,'s02: depois de abrir a sessão nova, continua «Feita»');
   assert.deepEqual(erros,[]);await c.close();console.log('PASS s02, estado antigo semeado: «Feita» na página do módulo'+(proj?' (projeção: nada lido nem gravado)':''));
  }}
 // 06/11/2026 (s02): na projeção a 1366 x 768, a fotografia ao alto do Olha (Hine, 640 x 811; 06/11/2026, revisão: 825 x 1024, do negativo de vidro) e a legenda ficam acima da barra.
 {const c=await b.newContext({viewport:{width:1366,height:768}}),p=await c.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));
  await p.goto(base+'/cidadania/m1/sessoes/02/?projetar=1');await p.waitForTimeout(500);await seguinte(p);
  await p.locator('#baralho .pos-op',{hasText:'Não'}).click();await p.waitForTimeout(200);
  for(let i=0;i<3;i++){const s=p.locator('.casca-acoes button',{hasText:/Seguinte|Mostrar resposta/}).first();await s.click();await p.waitForTimeout(250);const g=p.locator('.casca-folha [data-seguinte]');if(await g.count())await g.first().click();await p.waitForTimeout(200)}
  assert.equal(await p.locator('[data-c-num]').innerText(),'5/23');
  const im=await p.locator('#baralho .fig img').boundingBox(),fc=await p.locator('#baralho .fig figcaption').boundingBox(),ac=await p.locator('.casca-acoes').boundingBox();
  assert(im.y+im.height<=ac.y+1&&fc.y+fc.height<=ac.y+1,'s02, projeção: imagem e legenda acima da barra '+JSON.stringify([im,fc,ac]));
  assert.deepEqual(erros,[]);await c.close();console.log('PASS s02 na projeção: o Olha acima da barra');}
 // 06/11/2026 (decisões 166 a 168): o mesmo para a sessão 03, que passou à versão final em cidadania/m1/sessoes/03/ com a chave do
 // piloto (epi-cid-m1-s03): um estado antigo concluído (a versão do piloto, 2026-10-31-2) continua «Feita» depois de abrir a sessão
 // nova; na projeção, nada se lê nem se grava.
 {const K='epi-cid-m1-s03',antiga={versao:'2026-10-31-2',lida:true,t:1700000000000,melhor:15,totalMelhor:16,tentativas:1,exposicoes:{4:1}};
  for(const proj of [false,true]){
   const c=await b.newContext({viewport:{width:390,height:844}}),p=await c.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));
   await c.addInitScript(([K,v])=>{if(!sessionStorage.getItem('semeado')){localStorage.setItem(K,JSON.stringify(v));sessionStorage.setItem('semeado','1')}},[K,antiga]);
   const q=proj?'?projetar=1':'';
   await p.goto(base+'/cidadania/piloto/m1/'+q);await p.waitForTimeout(300);
   const estado=()=>p.locator('li[data-chave="'+K+'"] [data-estado]').textContent();
   assert.equal(await p.locator('li[data-chave="'+K+'"] a').getAttribute('href'),'../../m1/sessoes/03/','a página do módulo leva à s03 nova');
   if(proj)assert.equal(await estado(),'','projeção: a página do módulo não lê o progresso');
   else assert.match(await estado(),/^Feita 14\/11$/,'s03, estado antigo: «Feita» com a data da conclusão');
   await p.goto(base+'/cidadania/m1/sessoes/03/'+q);await p.waitForTimeout(500);
   const st=await p.evaluate(K=>JSON.parse(localStorage.getItem(K)),K);
   if(proj)assert.deepEqual(st,antiga,'projeção: a s03 não grava');
   else{assert.equal(st.antes.lida,true);assert.equal(st.antes.data,antiga.t);assert.equal(st.exposicoes,undefined);assert.notEqual(st.versao,antiga.versao)}
   await p.goto(base+'/cidadania/piloto/m1/'+q);await p.waitForTimeout(300);
   if(!proj)assert.match(await estado(),/^Feita 14\/11$/,'s03: depois de abrir a sessão nova, continua «Feita»');
   assert.deepEqual(erros,[]);await c.close();console.log('PASS s03, estado antigo semeado: «Feita» na página do módulo'+(proj?' (projeção: nada lido nem gravado)':''));
  }}
 // 06/11/2026 (s03): na projeção a 1366 x 768, a fotografia quase quadrada do Olha (Bubley, 640 x 671) e a legenda ficam acima da barra.
 {const c=await b.newContext({viewport:{width:1366,height:768}}),p=await c.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));
  await p.goto(base+'/cidadania/m1/sessoes/03/?projetar=1');await p.waitForTimeout(500);await seguinte(p);
  await p.locator('#baralho .pos-op',{hasText:'Não'}).click();await p.waitForTimeout(200);
  for(let i=0;i<3;i++){const s=p.locator('.casca-acoes button',{hasText:/Seguinte|Mostrar resposta/}).first();await s.click();await p.waitForTimeout(250);const g=p.locator('.casca-folha [data-seguinte]');if(await g.count())await g.first().click();await p.waitForTimeout(200)}
  assert.equal(await p.locator('[data-c-num]').innerText(),'5/23');
  const im=await p.locator('#baralho .fig img').boundingBox(),fc=await p.locator('#baralho .fig figcaption').boundingBox(),ac=await p.locator('.casca-acoes').boundingBox();
  assert(im.y+im.height<=ac.y+1&&fc.y+fc.height<=ac.y+1,'s03, projeção: imagem e legenda acima da barra '+JSON.stringify([im,fc,ac]));
  assert.deepEqual(erros,[]);await c.close();console.log('PASS s03 na projeção: o Olha acima da barra');}
 // 06/11/2026 (decisões 166 a 168): o mesmo para a sessão 04, que passou à versão final em cidadania/m1/sessoes/04/ com a chave do
 // piloto (epi-cid-m1-s04): um estado antigo concluído (a versão do piloto, 2026-10-31-2) continua «Feita» depois de abrir a
 // sessão nova; na projeção, nada se lê nem se grava (a s04 não é a próxima por fazer, por isso o estado fica vazio).
 {const K='epi-cid-m1-s04',antiga={versao:'2026-10-31-2',lida:true,t:1700000000000,melhor:15,totalMelhor:16,tentativas:1,exposicoes:{4:1}};
  for(const proj of [false,true]){
   const c=await b.newContext({viewport:{width:390,height:844}}),p=await c.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));
   await c.addInitScript(([K,v])=>{if(!sessionStorage.getItem('semeado')){localStorage.setItem(K,JSON.stringify(v));sessionStorage.setItem('semeado','1')}},[K,antiga]);
   const q=proj?'?projetar=1':'';
   await p.goto(base+'/cidadania/piloto/m1/'+q);await p.waitForTimeout(300);
   const estado=()=>p.locator('li[data-chave="'+K+'"] [data-estado]').textContent();
   assert.equal(await p.locator('li[data-chave="'+K+'"] a').getAttribute('href'),'../../m1/sessoes/04/','a página do módulo leva à s04 nova');
   if(proj)assert.equal(await estado(),'','projeção: a página do módulo não lê o progresso');
   else assert.match(await estado(),/^Feita 14\/11$/,'s04, estado antigo: «Feita» com a data da conclusão');
   await p.goto(base+'/cidadania/m1/sessoes/04/'+q);await p.waitForTimeout(500);
   const st=await p.evaluate(K=>JSON.parse(localStorage.getItem(K)),K);
   if(proj)assert.deepEqual(st,antiga,'projeção: a s04 não grava');
   else{assert.equal(st.antes.lida,true);assert.equal(st.antes.data,antiga.t);assert.equal(st.exposicoes,undefined);assert.notEqual(st.versao,antiga.versao)}
   await p.goto(base+'/cidadania/piloto/m1/'+q);await p.waitForTimeout(300);
   if(!proj)assert.match(await estado(),/^Feita 14\/11$/,'s04: depois de abrir a sessão nova, continua «Feita»');
   assert.deepEqual(erros,[]);await c.close();console.log('PASS s04, estado antigo semeado: «Feita» na página do módulo'+(proj?' (projeção: nada lido nem gravado)':''));
  }}
 // 06/11/2026 (s04): na projeção a 1366 x 768, as quatro peras do Olha (640 x 626) e a legenda ficam acima da barra; o «i» abre-se
 // pelo teclado e mostra a licença. 06/11/2026 (revisão da s04): o Olha passa a mostrar a página inteira (1100 x 1818); a mesma conta.
 {const c=await b.newContext({viewport:{width:1366,height:768}}),p=await c.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));
  await p.goto(base+'/cidadania/m1/sessoes/04/?projetar=1');await p.waitForTimeout(500);await seguinte(p);
  await p.locator('#baralho .pos-op',{hasText:'Não'}).click();await p.waitForTimeout(200);
  for(let i=0;i<3;i++){const s=p.locator('.casca-acoes button',{hasText:/Seguinte|Mostrar resposta/}).first();await s.click();await p.waitForTimeout(250);const g=p.locator('.casca-folha [data-seguinte]');if(await g.count())await g.first().click();await p.waitForTimeout(200)}
  assert.equal(await p.locator('[data-c-num]').innerText(),'5/23');
  const im=await p.locator('#baralho .fig img').boundingBox(),fc=await p.locator('#baralho .fig figcaption').boundingBox(),ac=await p.locator('.casca-acoes').boundingBox();
  assert(im.y+im.height<=ac.y+1&&fc.y+fc.height<=ac.y+1,'s04, projeção: imagem e legenda acima da barra '+JSON.stringify([im,fc,ac]));
  await p.locator('#baralho details.info-i > summary').focus();await p.keyboard.press('Enter');await p.waitForTimeout(200);
  assert(await p.locator('#baralho details.info-i').evaluate(e=>e.open),'s04: o «i» abre-se pelo teclado');
  assert.match(await p.locator('#baralho .info-i-texto').innerText(),/Domínio público/);
  assert.deepEqual(erros,[]);await c.close();console.log('PASS s04 na projeção: o Olha acima da barra e o «i» pelo teclado');}
 // 06/11/2026 (decisões 166 a 168): o mesmo para a sessão 05, que passou à versão final em cidadania/m1/sessoes/05/ com a chave do
 // piloto (epi-cid-m1-s05): um estado antigo concluído (a versão do piloto, 2026-10-31-2) continua «Feita» depois de abrir a
 // sessão nova; na projeção, nada se lê nem se grava.
 {const K='epi-cid-m1-s05',antiga={versao:'2026-10-31-2',lida:true,t:1700000000000,melhor:14,totalMelhor:16,tentativas:1,exposicoes:{3:1}};
  for(const proj of [false,true]){
   const c=await b.newContext({viewport:{width:390,height:844}}),p=await c.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));
   await c.addInitScript(([K,v])=>{if(!sessionStorage.getItem('semeado')){localStorage.setItem(K,JSON.stringify(v));sessionStorage.setItem('semeado','1')}},[K,antiga]);
   const q=proj?'?projetar=1':'';
   await p.goto(base+'/cidadania/piloto/m1/'+q);await p.waitForTimeout(300);
   const estado=()=>p.locator('li[data-chave="'+K+'"] [data-estado]').textContent();
   assert.equal(await p.locator('li[data-chave="'+K+'"] a').getAttribute('href'),'../../m1/sessoes/05/','a página do módulo leva à s05 nova');
   if(proj)assert.equal(await estado(),'','projeção: a página do módulo não lê o progresso');
   else assert.match(await estado(),/^Feita 14\/11$/,'s05, estado antigo: «Feita» com a data da conclusão');
   await p.goto(base+'/cidadania/m1/sessoes/05/'+q);await p.waitForTimeout(500);
   const st=await p.evaluate(K=>JSON.parse(localStorage.getItem(K)),K);
   if(proj)assert.deepEqual(st,antiga,'projeção: a s05 não grava');
   else{assert.equal(st.antes.lida,true);assert.equal(st.antes.data,antiga.t);assert.equal(st.exposicoes,undefined);assert.notEqual(st.versao,antiga.versao)}
   await p.goto(base+'/cidadania/piloto/m1/'+q);await p.waitForTimeout(300);
   if(!proj)assert.match(await estado(),/^Feita 14\/11$/,'s05: depois de abrir a sessão nova, continua «Feita»');
   assert.deepEqual(erros,[]);await c.close();console.log('PASS s05, estado antigo semeado: «Feita» na página do módulo'+(proj?' (projeção: nada lido nem gravado)':''));
  }}
 // 06/11/2026 (s05): na projeção a 1366 x 768, a gravura deitada do Olha (1400 x 1138) e a legenda ficam acima da barra; o «i» abre
 // e fecha com o teclado.
 {const c=await b.newContext({viewport:{width:1366,height:768}}),p=await c.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));
  await p.goto(base+'/cidadania/m1/sessoes/05/?projetar=1');await p.waitForTimeout(500);await seguinte(p);
  await p.locator('#baralho .pos-op',{hasText:'Não'}).click();await p.waitForTimeout(200);
  for(let i=0;i<3;i++){const s=p.locator('.casca-acoes button',{hasText:/Seguinte|Mostrar resposta/}).first();await s.click();await p.waitForTimeout(250);const g=p.locator('.casca-folha [data-seguinte]');if(await g.count())await g.first().click();await p.waitForTimeout(200)}
  assert.equal(await p.locator('[data-c-num]').innerText(),'5/23');
  const im=await p.locator('#baralho .fig img').boundingBox(),fc=await p.locator('#baralho .fig figcaption').boundingBox(),ac=await p.locator('.casca-acoes').boundingBox();
  assert(im.y+im.height<=ac.y+1&&fc.y+fc.height<=ac.y+1,'s05, projeção: imagem e legenda acima da barra '+JSON.stringify([im,fc,ac]));
  const sm=p.locator('#baralho details.info-i > summary');await sm.focus();await p.keyboard.press('Enter');await p.waitForTimeout(200);
  assert(await p.locator('#baralho details.info-i').evaluate(e=>e.open),'s05: o «i» abre com o teclado');
  assert.match(await p.locator('#baralho .info-i-texto').innerText(),/Domínio público/);
  await p.keyboard.press('Enter');await p.waitForTimeout(200);assert(!(await p.locator('#baralho details.info-i').evaluate(e=>e.open)),'s05: o «i» fecha com o teclado');
  assert.deepEqual(erros,[]);await c.close();console.log('PASS s05 na projeção: o Olha acima da barra e o «i» pelo teclado');}
 // 05/11/2026: plano do molde da Cidadania, pedido 1. A lição de ensaio do molde, de ponta a ponta.
 {const d=ENSAIO.d,url=base+ENSAIO_URL,AK='epi-cid-m1-artefactos';
  const arte=p=>p.evaluate(k=>JSON.parse(localStorage.getItem(k)||'null'),AK);
  for(const [w,h,tema] of [[390,844,'light'],[1366,900,'dark'],[320,640,'light']]){
   const c=await b.newContext({viewport:{width:w,height:h},colorScheme:tema}),p=await c.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));p.on('console',m=>{if(m.type()==='error')erros.push(m.text())});
   await p.goto(url);await p.waitForTimeout(500);
   assert(await p.evaluate(()=>document.body.classList.contains('molde-cidadania')));
   const cap=async n=>{if(CAPTURAS&&w!==320)await p.screenshot({path:path.join(CAPTURAS,'ensaio-'+w+'-'+tema+'-'+n+'.png')})};
   for(let i=0;i<d.cartoes.length;i++){const x=d.cartoes[i];
    if(w===390&&i===9){await p.reload();await p.waitForTimeout(600);assert.equal(await p.locator('[data-c-num]').innerText(),'10/'+d.cartoes.length,'retoma no cartão 10')}
    assert.equal(await p.locator('[data-c-num]').innerText(),(i+1)+'/'+d.cartoes.length,'ensaio, cartão '+(i+1));
    assert(await p.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),'ensaio: deslocamento horizontal no cartão '+(i+1)+' a '+w+' px');
    if(x.rot==='Abre'){assert.match(await p.locator('#baralho .aula-linha').innerText(),/^HOJE/i);assert.match(await p.locator('#baralho .guardaste').innerText(),/Guardaste: a pergunta da sessão\./);await cap('01-abre')}
    if(x.rot==='Decide'||x.rot==='Em turma'){const ident=x.rot==='Decide'?'posicao-inicio':'posicao-depois',v=x.rot==='Decide'?'Depende':'Sim';
     assert(await p.locator('#baralho .pos-lados').isHidden(),'os lados só abrem depois de escolher');
     await p.locator('#baralho .pos-op',{hasText:v}).click();await p.waitForTimeout(250);
     assert.equal(await p.locator('#baralho .pos-op[aria-pressed="true"]').innerText(),v);assert(await p.locator('#baralho .pos-lados').isVisible());
     assert.match(await p.locator('#baralho .posicao .guardaste').innerText(),new RegExp('Guardaste: a tua posição .*«'+v+'»'));
     const a=await arte(p);assert.equal(a.sessoes[d.chave].itens.find(t=>t.id===ident).texto,v);
     if(x.rot==='Em turma')assert.equal(await p.locator('#baralho [data-modelo]').innerText(),'No início, a tua posição foi: depende.');
     await cap(x.rot==='Decide'?'02-decide':'18-em-turma')}
    if(x.rot==='Olha'){const s=p.locator('#baralho details.info-i > summary');
     assert.equal(await p.locator('#baralho details.info-i').getAttribute('open'),null,'o «i» fechado ao carregar');
     const bx=await s.boundingBox(),im=await p.locator('#baralho .fig img').boundingBox();assert(bx.width>=44&&bx.height>=44,'alvo do «i» de 44 px');
     assert(bx.x>=im.x-1&&bx.x+bx.width<=im.x+im.width+1&&bx.y>=im.y-1&&bx.y+bx.height<=im.y+im.height+1,'o «i» dentro da imagem');
     await cap('05-olha');
     await s.focus();await p.keyboard.press('Enter');await p.waitForTimeout(250);assert.notEqual(await p.locator('#baralho details.info-i').getAttribute('open'),null,'Enter abre o «i»');
     assert(await p.locator('#baralho .info-i-texto').isVisible());assert.match(await p.locator('#baralho .info-i-texto').innerText(),/CC BY 2\.0/);await cap('05-olha-i');
     await p.keyboard.press('Escape');await p.waitForTimeout(150);assert.equal(await p.locator('#baralho details.info-i').getAttribute('open'),null,'Escape fecha o «i»');
     assert(await p.evaluate(()=>document.activeElement&&document.activeElement.matches('details.info-i > summary')),'o foco volta ao «i»');
     await p.locator('#baralho .fig img').focus();await p.keyboard.press('Enter');await p.waitForTimeout(300);assert(await p.locator('.amp-ov').isVisible(),'Enter na imagem amplia');
     await p.keyboard.press('Escape');await p.waitForTimeout(200);assert.equal(await p.locator('.amp-ov').count(),0,'Escape fecha a ampliação');
     assert.equal((await arte(p)).sessoes[d.chave].itens.find(t=>t.id==='imagem').texto,'Eleanor Roosevelt com o cartaz da Declaração, 1949')}
    if(x.rot==='Lê'||x.rot==='Conceito')await cap(x.rot==='Lê'?'08-le':'13-conceito');
    if(x.rot==='Agora, em papel')await cap('22-papel');
    if(x.rot==='Para levar'){await p.waitForTimeout(1900);
     assert.equal(await p.locator('#baralho [data-modelo]').innerText(),'No início decidiste depende; depois, sim.');
     const lista=await p.locator('#baralho [data-recolha-lista]').innerText();
     for(const t of ['Os teus artefactos','A pergunta da sessão','A tua posição no início','A imagem vista','O conceito','A tua posição depois','A frase da sessão','Copiar para as notas'])assert(lista.includes(t)||lista.toUpperCase().includes(t.toUpperCase()),'lista dos artefactos: '+t);
     await c.grantPermissions(['clipboard-read','clipboard-write']).catch(()=>{});
     await p.locator('#baralho [data-recolha-copiar]').click();await p.waitForTimeout(300);assert.match(await p.locator('#baralho .recolha-nota').innerText(),/Copiado|copiar/);
     await cap('23-levar')}
    if(x.t!=='ler'){if(x.t==='escolha'){const j=await p.$$eval('#baralho .ops button.op',bs=>bs.map(b=>+b.dataset.j));assert.equal(j.indexOf(x.c),[0,2,1,0,1,2][d.cartoes.filter(y=>y.t==='escolha').indexOf(x)],'lugar da certa')}
     await responder(p,x);assert.match(await p.locator('.casca-folha').innerText(),/Certo/,'ensaio, cartão '+(i+1));if(i===5)await cap('06-retorno')}
    if(i<d.cartoes.length-1)await seguinte(p);
   }
   await seguinte(p).catch(()=>{});await p.waitForTimeout(600);
   // 05/11/2026: correções da revisão da s01 (06/11/2026): o ensaio está no molde, e o fim do molde diz onde fica marcada a sessão
   const fim=await p.locator('#baralho').innerText();assert.match(fim,/A aula acaba aqui/i);assert.match(fim,/Sessão feita\./);assert.match(fim,/A página do módulo já a marca como feita\./);assert.match(fim,/Ensaio do passo/);
   await cap('24-fim');
   const st=await p.evaluate(k=>JSON.parse(localStorage.getItem(k)),d.chave);assert.equal(st.lida,true);assert.equal(st.curso,undefined);
   assert.deepEqual(erros,[],'ensaio a '+w+' px');await c.close();console.log('PASS ensaio do molde a '+w+' px ('+tema+'): posições, artefactos, «i», ampliação, retoma e fim');
  }
  // projeção: nada se lê nem se grava; as posições abrem os lados, sem guardar
  const c=await b.newContext({viewport:{width:1366,height:768}}),p=await c.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));
  await p.goto(url+'?projetar=1');await p.waitForTimeout(500);await seguinte(p);
  await p.locator('#baralho .pos-op',{hasText:'Não'}).click();await p.waitForTimeout(200);assert(await p.locator('#baralho .pos-lados').isVisible());
  for(let i=0;i<3;i++){const s=p.locator('.casca-acoes button',{hasText:/Seguinte|Mostrar resposta/}).first();await s.click();await p.waitForTimeout(250);const g=p.locator('.casca-folha [data-seguinte]');if(await g.count())await g.first().click();await p.waitForTimeout(200)}
  assert.equal(await p.locator('[data-c-num]').innerText(),'5/'+d.cartoes.length);
  // na projeção a 1366 x 768, a imagem do Olha e a legenda ficam acima da barra de ações
  const im=await p.locator('#baralho .fig img').boundingBox(),fc=await p.locator('#baralho .fig figcaption').boundingBox(),ac=await p.locator('.casca-acoes').boundingBox();
  assert(im.y+im.height<=ac.y+1&&fc.y+fc.height<=ac.y+1,'projeção: imagem e legenda acima da barra');if(CAPTURAS)await p.screenshot({path:path.join(CAPTURAS,'ensaio-projecao-1366x768-olha.png')});
  assert.equal(await p.evaluate(k=>localStorage.getItem(k),AK),null,'projeção: nenhum artefacto gravado');assert.equal(await p.evaluate(k=>localStorage.getItem(k),d.chave),null,'projeção: nenhum progresso');
  assert.deepEqual(erros,[]);await c.close();console.log('PASS ensaio do molde na projeção: nada gravado, Olha acima da barra');}
 await b.close();srv.close();})().catch(e=>{console.error(e);process.exit(1)});
