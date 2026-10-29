const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'..'),D=require('../assets/formas/corpus.json');
const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript','.json':'application/json','.css':'text/css','.png':'image/png','.webp':'image/webp','.woff2':'font/woff2'};
function fileFor(url){let name=decodeURIComponent(new URL(url,'http://localhost').pathname).replace(/^\/lente\//,'/');let f=path.resolve(ROOT,'.'+name);if(!f.startsWith(ROOT+path.sep))return null;try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');return f;}catch{return null;}}
const server=http.createServer((req,res)=>{const f=fileFor(req.url);if(!f){res.writeHead(404).end();return;}res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));});
global.window={};require('../assets/formas/leituras.js');for(const [id,g] of Object.entries(window.LenteLeituras)){const source=D.items.find(x=>x.id===id);assert.equal(source.status,'excerto-consultado');for(const [anchor] of g.anchors)assert(source.quote.includes(anchor));}
// ── 29/10/2026: frase de Kafka da RTP Ensina e os dois protótipos em cartões curtos («Certa manhã» e «A cena que falta») ──
const FRASE='Certa manhã, ao acordar de sonhos inquietos, Gregor Samsa viu-se transformado num gigantesco inseto.';
global.window=global.window||{};require('../assets/formas/certa-manha.js');require('../assets/formas/cena-que-falta.js');
const KM=window.LenteCertaManha,CQ=window.LenteCenaQueFalta;
assert.equal(D.items.find(x=>x.id==='kafka').quote,FRASE);assert.equal(KM.frase,FRASE);assert.equal(KM.segmentos.map(s=>s.t).join(' '),FRASE);
async function novoCtx(b,opts){const c=await b.newContext(Object.assign({viewport:{width:360,height:740},reducedMotion:'reduce'},opts||{}));
 await c.route('https://fonts.googleapis.com/**',r=>r.abort());await c.route('https://fonts.gstatic.com/**',r=>r.abort());
 await c.route('https://pedrohfernandes-klk.github.io/lente/**',route=>{const f=fileFor(route.request().url());if(f)route.fulfill({path:f,contentType:mime[path.extname(f)]||'application/octet-stream'});else route.abort();});return c;}
const semRolar=page=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
const cartao=page=>page.locator('.lf-cartao').getAttribute('data-cartao');
const seguinte=page=>page.locator('.casca-acoes [data-seguinte]').click();
const painelT=page=>page.locator('.casca-folha .c-folha-in').innerText();
const ls=(page,k)=>page.evaluate(k=>JSON.parse(localStorage.getItem(k)||'null'),k);
// «A cena que falta»: o plano entra; o aluno marca o que ele faz às hipóteses; só «Verificar» mostra a leitura do Lente
async function montar(pg,p,marcas){await pg.locator('[data-cand="'+p+'"]').click();assert.equal(await pg.locator('.lf-hips .lf-est').count(),0);assert.equal(await pg.locator('.casca-folha:not([hidden])').count(),0);
 for(const [h,s] of Object.entries(marcas))await pg.locator('[data-marcah="'+h+'"][data-s="'+s+'"]').click();await pg.locator('.casca-acoes [data-lf-verificar]').click();}
async function prototipos(b,base){
 const erros=[];const vigiar=page=>page.on('pageerror',e=>erros.push(e.message));
 for(const width of [360,1440]){
  // Certa manhã, percurso completo com cliques e teclado (sem atalhos de teste)
  const ctx=await novoCtx(b,{viewport:{width,height:width===360?740:900}}),page=await ctx.newPage();vigiar(page);
  await page.goto(base+'/narrativas/formas/certa-manha/');
  await page.evaluate(()=>{localStorage.setItem('lente-formas-corta-v1',JSON.stringify({version:1,done:['curiosidade']}));localStorage.setItem('epi-corta',JSON.stringify({feitas:{maias:123},nota:'preservar'}));});
  const antigas=await page.evaluate(()=>[localStorage.getItem('lente-formas-corta-v1'),localStorage.getItem('epi-corta')]);
  await page.reload();assert.equal(await cartao(page),'abre');
  assert.equal((await page.locator('.lf-prosa p').innerText()).trim(),FRASE);
  assert.match(await page.locator('.lf-credito').first().innerText(),/RTP Ensina[\s\S]*não identifica a tradução/);
  assert.equal(await page.locator('.lf-credito a').first().getAttribute('href'),'https://ensina.rtp.pt/artigo/a-metamorfose-ou-a-parabola-do-homem-inseto-de-franz-kafka/');
  await seguinte(page);assert.equal(await cartao(page),'a1');assert(await page.locator('[data-seguinte]').isDisabled());
  assert.equal(await page.locator('.lf-final').count(),0);  // a descoberta não aparece antes do toque
  await page.locator('[data-seg="t4"]').click();const fim4=await page.locator('.lf-final').innerText(),exp4=await painelT(page);
  assert.match(fim4,/viu-se transformado num homem cansado\./);await page.locator('.casca-folha .c-sec').click();
  await page.locator('[data-seg="t5"]').focus();await page.keyboard.press('Enter');const fim5=await page.locator('.lf-final').innerText(),exp5=await painelT(page);
  assert.notEqual(fim4,fim5);assert.notEqual(exp4,exp5);assert.match(fim5,/não encontrou final comum/);assert(!/inseto/.test(fim5));assert.equal(await page.locator('.lf-corte-ant').count(),1);
  // o rótulo «1.º corte» fica no primeiro corte, não no anterior
  for(const s of ['t1','t2']){await page.locator('[data-seg="'+s+'"]').click();await page.locator('.casca-folha .c-sec').click();}
  assert.deepEqual(await page.$$eval('.lf-seg',bs=>bs.filter(b=>b.querySelector('.lf-c1')).map(b=>b.dataset.seg)),['t4']);
  assert.match(await page.locator('.lf-final').innerText(),/^Certa manhã, ao acordar de sonhos inquietos, Gregor Samsa abriu a janela\.$/);
  await page.locator('[data-seg="t5"]').click();
  assert(await semRolar(page));await page.locator('.casca-folha .c-prim').click();
  // A2: a pauta só aparece depois da resposta; a mesma resposta dá explicações diferentes para variantes diferentes
  assert.equal(await cartao(page),'a2');assert.equal(await page.locator('.lf-pauta').count(),0);
  await page.locator('[data-resp="original"]').click();assert.equal(await page.locator('.lf-pauta').count(),1);const v1=await painelT(page);
  assert.equal(await page.locator('.lf-pauta .lf-difere').count(),1);
  await page.locator('.casca-folha .c-sec').click();assert.equal(await page.locator('[data-var="1"]').getAttribute('aria-pressed'),'true');
  await page.locator('[data-resp="original"]').click();const v2=await painelT(page);assert.notEqual(v1,v2);assert.match(v2,/a diferença está no «talvez»/);assert(!/nunca sai do «não»/.test(v2));assert(!/Compara as duas pautas/.test(v1));  // o fecho só depois de duas variantes, e cada uma com o seu
  await page.locator('.casca-folha .c-prim').click();
  // A3: restrições formais verificáveis (✗) separadas das dúvidas (◐); a primeira versão fica conservada
  assert.equal(await cartao(page),'a3');await page.locator('#a3-texto').fill('De repente, ao abrir a porta, vi um inseto!');await page.locator('[data-lf-verificar]').click();
  assert.equal(await page.locator('.lf-avisos .lf-x').count(),2);assert.equal(await page.locator('.lf-avisos .lf-meio').count(),1);
  assert.match(await page.locator('.lf-first').innerText(),/De repente, ao abrir a porta/);await page.locator('[data-outra]').click();
  await page.locator('#a3-texto').fill('Segunda tentativa, já sem bicho.');await page.locator('[data-lf-verificar]').click();await page.locator('[data-outra]').click();
  assert.match(await page.locator('.lf-first').innerText(),/De repente, ao abrir a porta/);assert(!/Segunda tentativa/.test(await page.locator('.lf-first').innerText()));
  await page.locator('#a3-texto').fill('Numa terça, ao abrir a porta, a Rita ficou horrorizada com a transformação.');await page.locator('[data-lf-verificar]').click();
  assert.match(await page.locator('.lf-avisos').innerText(),/«transformação»[\s\S]*não uses o verbo «transformar»[\s\S]*«horrorizada»: é a reação que a variante 1 juntava/);assert.match(await page.locator('.lf-consequencia').innerText(),/procura só: «!»/);
  await page.locator('#a3-texto').fill('Numa terça-feira, ao abrir a gaveta, a Rita encontrou o domingo passado dobrado em quatro.');await page.locator('[data-lf-verificar]').click();
  assert.equal(await page.locator('.lf-avisos').count(),0);await seguinte(page);
  // B1: arrumar com as teclas 1, 2 e 3; a primeira leitura guarda-se no primeiro «Verificar», antes de qualquer marca
  assert.equal(await cartao(page),'b1');assert(await page.locator('[data-lf-verificar]').isDisabled());
  for(const k of ['1','1','2','2','2','3','3','3','3'])await page.keyboard.press(k);
  assert.equal(await page.locator('.lf-quadro .lf-marca-j').count(),0);assert.equal(await ls(page,'lente-formas-v1'),null);
  await page.locator('[data-lf-verificar]').click();
  const arr={manha:'mostra',corpo:'mostra',identidade:'infiro',dormiu:'infiro',cama:'infiro',emprego:'falta',sozinho:'falta',repulsa:'falta',intencao:'falta'};
  let reg=await ls(page,'lente-formas-v1');assert.deepEqual(reg.itens['certa-manha'].primeira.arrumacao,arr);assert(reg.itens['certa-manha'].experimentei>0);
  for(const t of await page.locator('.lf-quadro .lf-marca-j').allInnerTexts())assert.match(t,/Sustenta-se|Também se defende|Difícil de sustentar/);
  assert.equal(await page.locator('.lf-quadro .lf-marca-j').count(),9);
  assert.equal(await page.locator('.casca-folha .c-sec').innerText(),'Ler as explicações');await page.locator('.casca-folha .c-sec').click();await page.locator('[data-tag="repulsa"]').click();const e1=await page.locator('.lf-explica').innerText();
  await page.locator('[data-mover="infiro"]').click();await page.locator('[data-tag="repulsa"]').click();const e2=await page.locator('.lf-explica').innerText();
  assert.notEqual(e1,e2);assert.match(e2,/1\.ª escolha: Preciso de mais contexto/);assert.match(await page.locator('[data-tag="repulsa"]').innerText(),/mudou depois da explicação/i);
  reg=await ls(page,'lente-formas-v1');assert.equal(reg.itens['certa-manha'].primeira.arrumacao.repulsa,'falta');assert.equal(reg.itens['certa-manha'].depoisExplicacao.repulsa,'infiro');
  await seguinte(page);assert.equal(await cartao(page),'b2');await page.locator('[data-falta="intencao"][data-tipo="autor"]').click();assert.match(await page.locator('.lf-faltava .lf-consequencia').nth(2).innerText(),/testemunho/);
  await seguinte(page);assert.equal(await cartao(page),'b3');assert.match(await page.locator('.lf-carimbo').innerText(),/Primeira leitura guardada às \d\dh\d\d/);
  await page.locator('#b3-texto').fill('Leio uma manhã estranha porque a frase diz viu-se.');
  // recarga no mesmo separador: o trabalho e a primeira leitura continuam
  await page.reload();assert.equal(await cartao(page),'b3');assert.equal(await page.locator('#b3-texto').inputValue(),'Leio uma manhã estranha porque a frase diz viu-se.');
  await seguinte(page);assert.equal(await cartao(page),'original');for(const g of ['bett','ungeheuer','ungeziefer'])await page.locator('[data-glosa="'+g+'"]').click();
  assert.equal(await page.locator('.lf-glosas li').count(),3);assert(!(await page.content()).includes('Als Gregor Samsa'));
  await seguinte(page);assert.equal(await page.locator('.lf-passagens li').count(),5);assert.match(await page.locator('.lf-passagens li').first().innerText(),/§ 1[\s\S]*carapaça/);await seguinte(page);
  // F1: rever sem apagar a primeira leitura (a tracejado) e com uma quarta coluna
  assert.equal(await cartao(page),'f1');assert.equal(await page.locator('.lf-quadro .lf-col').count(),4);assert.equal(await page.locator('.lf-fantasma').count(),1);
  assert.equal(await page.locator('.lf-quadro .lf-marca-j').count(),0);assert.equal(await page.locator('.casca-acoes [data-seguinte]').count(),0);
  await page.locator('[data-tag="sozinho"]').click();assert(!/irmã/.test(await page.locator('.lf-explica').innerText()));await page.keyboard.press('4');
  assert.match(await page.locator('.lf-col[data-col="desmente"]').innerText(),/sozinho/);assert.match(await page.locator('.lf-estado').innerText(),/Mudaste 2 de 9/);
  await page.locator('.casca-acoes [data-lf-verificar]').click();assert.match(await painelT(page),/Revisão guardada/);await page.locator('.casca-folha .c-sec').click();
  assert.equal(await page.locator('.lf-quadro .lf-marca-j').count(),9);await page.locator('[data-tag="sozinho"]').click();assert.match(await page.locator('.lf-explica').innerText(),/irmã/);
  await page.locator('[data-tag="emprego"]').click();await page.keyboard.press('1');assert.match(await page.locator('[data-tag="emprego"]').innerText(),/mudou depois da explicação/i);await seguinte(page);
  // F2: que informação fez diferença (a explicação depende do que mudou)
  assert.equal(await cartao(page),'f2');assert.match(await page.locator('.lf-duas').innerText(),/sozinho/);
  await page.locator('[data-info="familia"]').click();assert.match(await painelT(page),/desfez esse silêncio/);await page.locator('.casca-folha .c-sec').click();
  await page.locator('[data-info="cama"]').click();assert.match(await painelT(page),/Escolheste a cama, mas/);await page.locator('.casca-folha .c-prim').click();
  // F3: lado a lado; a mudança vinda da explicação distingue-se da que veio da informação nova
  assert.equal(await cartao(page),'f3');assert(await page.locator('[data-seguinte]').isDisabled());
  await page.locator('[data-lado="sozinho"]').click();assert.match(await painelT(page),/perdeu-o/);await page.locator('.casca-folha .c-sec').click();
  await page.locator('[data-lado="repulsa"]').click();assert.match(await painelT(page),/explicação do cartão «Arruma»/);await page.locator('.casca-folha .c-sec').click();
  await page.locator('[data-lado="emprego"]').click();assert.match(await painelT(page),/depois da explicação do cartão «Revê»/);
  assert.match(await page.locator('.lf-lado-col').first().innerText(),/repulsa\s+Preciso de mais contexto/);
  await page.locator('.casca-folha .c-prim').click();assert.equal(await cartao(page),'fim');assert.match(await page.locator('[data-registo]').innerText(),/experimentei, revi/);
  reg=await ls(page,'lente-formas-v1');assert(reg.itens['certa-manha'].revi>0);
  const tudo=await page.evaluate(()=>JSON.stringify(localStorage));assert(!/Leio uma manhã|De repente|Rita encontrou/.test(tudo));
  assert.deepEqual(await page.evaluate(()=>[localStorage.getItem('lente-formas-corta-v1'),localStorage.getItem('epi-corta')]),antigas);
  assert(await semRolar(page));await ctx.close();
  console.log('PASS Certa manhã: frase e crédito RTP, cortes distintos, pauta depois da resposta, restrições formais, primeira leitura antes das marcas, revisão em quatro colunas, recarga e registo experimentei/revi at '+width+'px');

  // A cena que falta: cada plano dá um vetor de estados e um título diferentes; o plano entra no lugar 04
  const titulos=new Set(),vetores=new Set();
  for(const p of CQ.candidatos){const c2=await novoCtx(b,{viewport:{width,height:900}}),pg=await c2.newPage();vigiar(pg);
   await pg.goto(base+'/narrativas/corta/cena-que-falta/');await seguinte(pg);assert(await pg.locator('[data-seguinte]').isDisabled());
   await pg.locator('[data-inicial="H2"]').click();await seguinte(pg);assert(await pg.locator('.casca-acoes [data-lf-verificar]').isDisabled());
   await pg.locator('[data-cand="'+p+'"]').click();assert(await pg.locator('.casca-acoes [data-lf-verificar]').isDisabled());await pg.locator('[data-marcah="H2"][data-s="ganha"]').click();await pg.locator('.casca-acoes [data-lf-verificar]').click();
   assert.match(await painelT(pg),CQ.estados[p].H2.estado==='ganha'?/tu e o Lente marcam ▲ ganha apoio/:/tu marcaste ▲ ganha apoio; o Lente lê/);assert(await pg.locator('.casca-folha .lf-apoio-c').isHidden());
   const v=await pg.$$eval('.lf-hips .lf-h .lf-est',els=>els.map(x=>x.dataset.estado));assert.deepEqual(v,CQ.hipoteses.map(h=>CQ.estados[p][h.id].estado));
   vetores.add(v.join());titulos.add(await pg.locator('.casca-folha .c-veredito').innerText());
   assert.match(await pg.locator('[data-mini="3"]').getAttribute('aria-label'),new RegExp(CQ.quadros[p].titulo));assert.equal(await pg.locator('.lf-tira .lf-novo').count(),1);
   assert(await semRolar(pg));await c2.close();}
  assert.equal(titulos.size,3);assert.equal(vetores.size,3);
  // comparação: «A mesma imagem, duas legendas»; «experimentei» só com duas montagens; revisão sem perder a escolha inicial
  const c3=await novoCtx(b,{viewport:{width,height:900}}),pg=await c3.newPage();vigiar(pg);
  await pg.goto(base+'/narrativas/corta/cena-que-falta/');const antes=await pg.evaluate(()=>localStorage.getItem('lente-formas-corta-v1'));
  await seguinte(pg);await pg.locator('[data-inicial="H2"]').click();await seguinte(pg);
  await montar(pg,'bolso',{H2:'perde'});assert(!/câmara olha para outro lado|sem efeito/.test(await painelT(pg)));await pg.locator('.casca-folha .c-sec').click();assert.equal(await cartao(pg),'compara');
  assert.match(await pg.locator('.lf-estado').innerText(),/duas montagens diferentes/);assert.equal(await ls(pg,'lente-formas-v1'),null);
  await pg.locator('[data-voltar-escolhe]').click();assert.match(await pg.locator('.lf-q').innerText(),/O que fará à hipótese «Quem a encontrou foi à procura da dona»\?/);
  await montar(pg,'cartao',{H2:'ganha'});assert.match(await painelT(pg),/ganha apoio/);await pg.locator('.casca-folha .c-prim').click();
  assert.equal(await cartao(pg),'compara');assert(await pg.locator('[data-lf-verificar]').isDisabled());
  await pg.locator('[data-leg="l1"][data-l="afinal"]').click();await pg.locator('[data-leg="l2"][data-l="retrato"]').click();await pg.locator('[data-lf-verificar]').click();
  assert.match(await pg.locator('.casca-folha .c-veredito').innerText(),/A mesma imagem, duas legendas/);assert.match(await painelT(pg),/Supões, com apoio no plano do meio/);assert(!/Vês:/.test(await painelT(pg)));
  assert((await ls(pg,'lente-formas-v1')).itens['cena-que-falta'].experimentei>0);
  await pg.locator('.casca-folha .c-sec').click();await pg.locator('[data-leg="l2"][data-l="afinal"]').click();await pg.locator('[data-lf-verificar]').click();
  assert.match(await pg.locator('.casca-folha .c-veredito').innerText(),/A mesma legenda nas duas/);assert.match(await painelT(pg),/Supões sem apoio nesta montagem/);
  await pg.locator('.casca-folha .c-sec').click();await pg.locator('[data-leg="l1"][data-l="neutra"]').click();await pg.locator('[data-leg="l2"][data-l="neutra"]').click();await pg.locator('[data-lf-verificar]').click();
  assert.match(await pg.locator('.casca-folha .c-veredito').innerText(),/A legenda mais prudente/);assert.match(await painelT(pg),/Sustenta-se «Devolve o que encontrou»/);
  await pg.locator('.casca-folha .c-sec').click();await pg.locator('[data-hpar="H2"]').click();assert.match(await pg.locator('.lf-par-texto').innerText(),/parada numa montagem/);
  await pg.locator('[data-hpar="H3"]').click();assert.match(await pg.locator('.lf-par-texto').innerText(),/ficou igual nas duas montagens/);
  await seguinte(pg);assert.equal(await cartao(pg),'reve');assert.match(await pg.locator('.lf-cartao').innerText(),/Quem a encontrou foi à procura da dona/);
  await pg.locator('[data-rev="aberto"]').click();await pg.locator('[data-plano="cartao"]').click();
  assert.match(await painelT(pg),/Deixas «Quem a encontrou foi à procura da dona» em aberto, embora «O cartão» a reforce/);assert((await ls(pg,'lente-formas-v1')).itens['cena-que-falta'].revi>0);
  await pg.locator('.casca-folha .c-prim').click();assert.equal(await cartao(pg),'escreve');
  await pg.locator('#f5-texto').fill('Senta-se ao lado de um homem e pousa o vaso no chão.');await pg.locator('[data-lf-verificar]').click();assert.equal(await pg.locator('.lf-avisos').count(),0);
  assert.equal(await pg.locator('.casca-folha:not([hidden])').count(),0);  // o painel só abre com as três marcas
  for(const [i,s] of [['0','igual'],['1','ganha'],['2','perde']])await pg.locator('[data-marca5="'+i+'"][data-s="'+s+'"]').click();
  assert.match(await painelT(pg),/marcaste: «Esqueceu-se do vaso» = não muda; «Deu o vaso a alguém» ▲ ganha apoio; «O vaso nunca foi dela» ▼ perde apoio/);await pg.locator('.casca-folha .c-sec').click();
  await pg.locator('#f5-texto').fill('Pensou que ninguém via e deixou o vaso porque estava cansada.');await pg.locator('[data-lf-verificar]').click();const avs=await pg.locator('.lf-avisos').innerText();assert.match(avs,/«pensou»: é uma ação que se vê ou um pensamento/);assert.match(avs,/«porque»: explica; uma câmara mostra o que acontece, não porquê/);
  assert.equal(await pg.evaluate(()=>localStorage.getItem('lente-formas-corta-v1')),antes);assert(!(await pg.evaluate(()=>JSON.stringify(localStorage))).includes('ninguém via'));
  assert(await semRolar(pg));await c3.close();
  console.log('PASS A cena que falta: três vetores e três explicações distintas, plano no lugar 04, duas legendas, experimentei só com duas montagens, revisão e transferência at '+width+'px');
 }
 // a cena que falta com ganho e perda na mesma hipótese («ambos»)
 {const c=await novoCtx(b),pg=await c.newPage();vigiar(pg);await pg.goto(base+'/narrativas/corta/cena-que-falta/');await seguinte(pg);await pg.locator('[data-inicial="H2"]').click();await seguinte(pg);
  await montar(pg,'cartao',{H2:'ganha'});await pg.locator('.casca-folha .c-prim').click();await montar(pg,'regresso',{H2:'igual'});assert.match(await painelT(pg),/◐ Também se defende outra leitura/);await pg.locator('.casca-folha .c-prim').click();
  await pg.locator('[data-leg="l1"][data-l="retrato"]').click();await pg.locator('[data-leg="l2"][data-l="tempo"]').click();await pg.locator('[data-lf-verificar]').click();await pg.locator('.casca-folha .c-prim').click();
  await pg.locator('[data-rev="aberto"]').click();await pg.locator('[data-plano="regresso"]').click();assert.match(await painelT(pg),/viste um plano reforçá-la e outro enfraquecê-la/);await pg.locator('.casca-folha .c-sec').click();
  await pg.locator('[data-rev="mantenho"]').click();assert.match(await painelT(pg),/«O cartão» deu-lhe apoio e «O regresso» tirou-lho/);await pg.locator('.casca-folha .c-sec').click();
  await pg.locator('[data-rev="corrijo"]').click();assert.match(await painelT(pg),/«O regresso» tirou-lhe apoio, embora «O cartão» lho tenha dado/);
  // «Nenhuma me parece mais forte» também é uma posição e permite «revi»
  await pg.locator('.casca-folha .c-prim').click();await c.close();}
 {const c=await novoCtx(b),pg=await c.newPage();vigiar(pg);await pg.goto(base+'/narrativas/corta/cena-que-falta/');await seguinte(pg);await pg.locator('[data-inicial="nenhuma"]').click();await seguinte(pg);
  await pg.locator('[data-cand="regresso"]').click();assert(await pg.locator('.casca-acoes [data-lf-verificar]').isDisabled());await pg.locator('[data-marcah="H3"][data-s="ganha"]').click();await pg.locator('.casca-acoes [data-lf-verificar]').click();assert.match(await painelT(pg),/«A dona voltou para a procurar»: tu e o Lente marcam ▲ ganha apoio/);await pg.locator('.casca-folha .c-prim').click();
  await montar(pg,'bolso',{H1:'ganha'});await pg.locator('.casca-folha .c-prim').click();
  await pg.locator('[data-leg="l1"][data-l="tempo"]').click();await pg.locator('[data-leg="l2"][data-l="afinal"]').click();await pg.locator('[data-lf-verificar]').click();await pg.locator('.casca-folha .c-prim').click();
  await pg.locator('[data-rev="continua"]').click();await pg.locator('[data-plano="nenhum"]').click();assert.match(await painelT(pg),/juízo suspenso/);assert((await ls(pg,'lente-formas-v1')).itens['cena-que-falta'].revi>0);await c.close();}
 // sequência: com movimento reduzido não arranca sozinha; sem ele, corre com o relógio e anuncia só o princípio e o fim
 {const c=await novoCtx(b),pg=await c.newPage();vigiar(pg);await pg.goto(base+'/narrativas/corta/cena-que-falta/');await seguinte(pg);
  assert.equal(await pg.locator('[data-seq]').count(),0);await pg.locator('[data-passo="1"]').click();assert.match(await pg.locator('[data-anuncio]').innerText(),/Plano 2 de 5: Uma pessoa de casaco verde/);
  assert.match(await pg.locator('.lf-visor figcaption').innerText(),/O olhar/);await c.close();}
 {const c=await novoCtx(b,{reducedMotion:'no-preference'}),pg=await c.newPage();vigiar(pg);await pg.clock.install();await pg.goto(base+'/narrativas/corta/cena-que-falta/');await seguinte(pg);
  await pg.locator('[data-seq]').click();assert.equal(await pg.locator('[data-anuncio]').innerText(),'A sequência começou.');await pg.clock.runFor(4100);assert.equal(await pg.locator('[data-anuncio]').innerText(),'A sequência começou.');
  await pg.clock.runFor(8000);assert.match(await pg.locator('[data-anuncio]').innerText(),/A sequência acabou/);assert.equal(await pg.locator('[data-seq]').innerText(),'Ver outra vez');
  await pg.locator('[data-seq]').click();await pg.clock.runFor(2100);await pg.locator('[data-inicial="H3"]').click();await pg.clock.runFor(4200);
  assert.equal(await pg.$$eval('[data-mini]',ms=>ms.findIndex(m=>m.classList.contains('lf-sel'))),0);assert.equal(await pg.locator('[data-seq]').innerText(),'Ver a sequência');
  await pg.locator('[data-seq]').click();assert.equal(await pg.locator('[data-seq]').innerText(),'Pausa');await c.close();}
 // projeção: nada se grava, o pessoal não aparece, as explicações e as marcas ficam veladas até se pedirem
 {const c=await novoCtx(b,{viewport:{width:1440,height:900}}),pg=await c.newPage();vigiar(pg);await pg.goto(base+'/narrativas/formas/certa-manha/');
  await pg.evaluate(()=>localStorage.setItem('lente-formas-v1',JSON.stringify({version:1,itens:{'certa-manha':{primeira:{em:1,arrumacao:{corpo:'falta'}}}}})));const antes=await pg.evaluate(()=>JSON.stringify(localStorage));
  await pg.goto(base+'/narrativas/formas/certa-manha/?projetar=1');assert(await pg.locator('body.lf-projetar').count());assert.equal(await pg.locator('.lf-aparelho').count(),0);
  await seguinte(pg);await pg.locator('[data-seg="t5"]').click();assert(await pg.locator('.lf-revelar').isVisible());assert(await pg.locator('.lf-velado').isHidden());assert(await pg.locator('.casca-folha .c-veredito').isHidden());
  await pg.locator('.lf-revelar').click();assert(await pg.locator('.lf-velado').isVisible());assert.match(await pg.locator('.lf-velado').innerText(),/Tocaste em «num gigantesco inseto»/);await pg.locator('.casca-folha .c-prim').click();
  await pg.locator('[data-resp="igual"]').click();await pg.locator('.casca-folha .c-prim').click();assert(await pg.locator('#a3-texto').isHidden());await seguinte(pg);
  for(const k of ['1','1','2','2','2','3','3','3','3'])await pg.keyboard.press(k);await pg.locator('[data-lf-verificar]').click();assert.equal(await pg.locator('.lf-quadro .lf-marca-j').count(),0);
  await pg.locator('.lf-revelar').click();assert.equal(await pg.locator('.lf-quadro .lf-marca-j').count(),9);
  await pg.locator('.casca-folha .c-prim').click();assert.equal(await cartao(pg),'b2');await seguinte(pg);assert.match(await pg.locator('.lf-carimbo').innerText(),/Leitura da turma/);
  assert.equal(await pg.evaluate(()=>JSON.stringify(localStorage)),antes);assert.match(await pg.locator('.lf-aviso-proj').innerText(),/nada do que se faz aqui fica guardado/);await c.close();}
 // aparelho partilhado: a primeira leitura guardada não passa a ser de quem chega sem perguntar
 for(const resp of ['sim','nao']){const c=await novoCtx(b),pg=await c.newPage();vigiar(pg);await pg.goto(base+'/narrativas/formas/certa-manha/');
  await pg.evaluate(()=>localStorage.setItem('lente-formas-v1',JSON.stringify({version:1,itens:{'certa-manha':{experimentei:5,primeira:{em:1793260000000,arrumacao:{manha:'mostra',corpo:'mostra',identidade:'infiro',dormiu:'infiro',cama:'infiro',emprego:'falta',sozinho:'falta',repulsa:'falta',intencao:'falta'}}}}})));await pg.reload();
  assert.match(await pg.locator('.lf-aparelho').innerText(),/Neste aparelho há uma primeira leitura guardada a .*É tua\?/s);await pg.locator('[data-aparelho="'+resp+'"]').click();
  for(let i=0;i<4;i++){if(await cartao(pg)==='b1')break;if(await cartao(pg)==='a1')await pg.locator('[data-seg="t1"]').click(),await pg.locator('.casca-folha .c-prim').click();else if(await cartao(pg)==='a2')await pg.locator('[data-resp="igual"]').click(),await pg.locator('.casca-folha .c-prim').click();else await seguinte(pg);}
  assert.equal(await cartao(pg),'b1');assert.equal(await pg.locator('.lf-quadro .lf-marca-j').count(),resp==='sim'?9:0);assert.equal(await pg.locator('[data-seguinte]').count(),resp==='sim'?1:0);
  // «Recomeçar» limpa o separador e não apaga a primeira leitura guardada no aparelho
  pg.once('dialog',d=>d.accept());await pg.evaluate(()=>{document.querySelector('[data-c-menu]').click();document.querySelector('[data-lf-menu="recomecar"]').click();});
  assert((await ls(pg,'lente-formas-v1')).itens['certa-manha'].primeira);assert.equal(await cartao(pg),'abre');assert.equal(await pg.locator('.lf-aparelho').count(),1);await c.close();}
 // uma primeira leitura incompleta (chave antiga) não se oferece
 {const c=await novoCtx(b),pg=await c.newPage();vigiar(pg);await pg.goto(base+'/narrativas/formas/certa-manha/');
  await pg.evaluate(()=>localStorage.setItem('lente-formas-v1',JSON.stringify({version:1,itens:{'certa-manha':{primeira:{em:1,arrumacao:{corpo:'falta',outra:'coisa'}}}}})));await pg.reload();assert.equal(await pg.locator('.lf-aparelho').count(),0);await c.close();}
 // papel: o bloco compõe-se uma vez ao carregar e não leva o que o aluno escreveu; o modo (enunciado ou apoios) muda por classe; os desenhos chegam ao PDF
 {const c=await novoCtx(b),pg=await c.newPage();vigiar(pg);await pg.goto(base+'/narrativas/formas/certa-manha/');await pg.evaluate(()=>{window.print=()=>{};});
  await seguinte(pg);await pg.locator('[data-seg="t2"]').click();await pg.locator('.casca-folha .c-prim').click();await pg.locator('[data-resp="variante"]').click();await pg.locator('.casca-folha .c-prim').click();
  await pg.locator('#a3-texto').fill('Texto privado da abertura');const imprime=async()=>{await pg.emulateMedia({media:'print'});await pg.evaluate(()=>window.dispatchEvent(new Event('beforeprint')));const x=await pg.locator('#lf-print').innerText();await pg.emulateMedia({media:'screen'});return x;};
  let imp=await imprime();assert(imp.includes(FRASE));assert(!imp.includes('Texto privado'));assert(imp.includes('Enunciado'));assert(!imp.includes('Apoios para depois'));assert.match(imp,/Vira a página só depois de preencheres o 4\./);
  await pg.evaluate(()=>{document.querySelector('[data-c-menu]').click();document.querySelector('[data-lf-menu="apoios"]').click();});imp=await imprime();assert.match(imp,/Apoios para depois da discussão[\s\S]*Sustenta-se/);assert(!/Vira a página/.test(imp));
  await pg.evaluate(()=>window.dispatchEvent(new Event('afterprint')));assert(!(await imprime()).includes('Apoios para depois'));
  const pdfK=(await pg.pdf({format:'A4'})).toString('latin1');assert(pdfK.length>1000);
  await pg.goto(base+'/narrativas/corta/cena-que-falta/');await pg.waitForLoadState('networkidle');assert.match(await imprime(),/O bolso[\s\S]*O cartão[\s\S]*O regresso/);
  const imagens=buf=>(buf.toString('latin1').match(/\/Subtype\s*\/Image/g)||[]).length;
  assert.equal(imagens(await pg.pdf({format:'A4'})),4,'enunciado com os quatro desenhos');
  await pg.evaluate(()=>{window.print=()=>{};document.querySelector('[data-c-menu]').click();document.querySelector('[data-lf-menu="apoios"]').click();});assert.equal(imagens(await pg.pdf({format:'A4'})),4,'apoios com os quatro desenhos');await c.close();}
 // entrada do laboratório: selos novos e antigos, só lidos
 {const c=await novoCtx(b,{viewport:{width:1440,height:900}}),pg=await c.newPage();vigiar(pg);await pg.goto(base+'/narrativas/');
  await pg.evaluate(()=>{localStorage.setItem('lente-formas-v1',JSON.stringify({version:1,itens:{'certa-manha':{experimentei:1,revi:2}}}));localStorage.setItem('lente-formas-corta-v1',JSON.stringify({version:1,done:['curiosidade']}));});const antes=await pg.evaluate(()=>JSON.stringify(localStorage));
  await pg.reload();assert.deepEqual(await pg.locator('[data-lf-selos="certa-manha"] .lf-selo').allInnerTexts(),['Experimentei','Revi']);assert(await pg.locator('[data-lf-selos="cena-que-falta"]').isHidden());
  assert.equal(await pg.locator('[data-lf-registo]').innerText(),'Experimentaste 1 de 2.');assert.match(await pg.locator('[data-lf-proxima]').getAttribute('href'),/corta\/cena-que-falta\/$/);
  assert.match(await pg.locator('.lf-entry [data-formas-progress]').innerText(),/1 de 4/);assert.equal(await pg.evaluate(()=>JSON.stringify(localStorage)),antes);
  assert.equal(await pg.locator('.lp-1 .lp-credit').innerText(),'Espiar os mestres. Sem lhes copiar os tiques.');
  await pg.goto(base+'/narrativas/corta/mesa/');await pg.locator('a[href="../cena-que-falta/"]').first().click();assert.equal(await cartao(pg),'abre');
  await pg.goto(base+'/narrativas/corta/');await pg.locator('.lf-novo-corta a').click();assert.equal(await cartao(pg),'abre');await c.close();}
 // entrada: um registo só com «revi» também conta; a porta das obras abre a mesa com as pontes (Gógol, Vian, Pacheco, Borges, cinema)
 {const c=await novoCtx(b,{viewport:{width:1440,height:900}}),pg=await c.newPage();vigiar(pg);await pg.goto(base+'/narrativas/');
  await pg.evaluate(()=>localStorage.setItem('lente-formas-v1',JSON.stringify({version:1,itens:{'certa-manha':{revi:2}}})));await pg.reload();
  assert.equal(await pg.locator('[data-lf-registo]').innerText(),'Experimentaste 1 de 2.');assert.equal(await pg.locator('.lf-entry-grid a').nth(2).getAttribute('href'),'formas/?mesa=pt');await c.close();}
 // obras: a frase nova com expressões selecionáveis, ligação clara para a RTP, glosas só depois da hipótese e a primeira leitura que já não se apaga
 {const c=await novoCtx(b,{viewport:{width:1440,height:900}}),pg=await c.newPage();vigiar(pg);await pg.goto(base+'/narrativas/formas/');await pg.locator('#kafka').waitFor();const k=pg.locator('#kafka');
  assert.equal(await k.locator('.lf-route').getAttribute('href'),'certa-manha/');assert.match(await k.locator('.lf-credit-line').innerText(),/RTP Ensina/);assert.match(await k.locator('.lf-credit-line a').innerText(),/Ver na RTP Ensina/);
  assert.equal(await k.locator('[data-anchor]').count(),3);assert.deepEqual(await k.locator('[data-anchor]').allInnerTexts(),['Certa manhã','viu-se transformado','gigantesco inseto']);
  await k.locator('summary').first().click();const fonte=await k.locator('.lf-source').innerText();assert.match(fonte,/Tradução não identificada/);assert(!/Helena Topa|Penguin/.test(fonte));
  await k.locator('[data-anchor="2"]').click();assert(!(await k.locator('.lf-evidence').innerText()).includes('O nome dá um tipo de bicho'));
  await k.locator('.lf-levels [data-level="1"]').click();await k.locator('.lf-levels [data-level="2"]').click();await k.locator('.lf-levels [data-level="1"]').click();
  await k.locator('[data-hypothesis="0"]').click();assert.match(await k.locator('.lf-evidence').innerText(),/O nome dá um tipo de bicho/);
  await k.locator('[data-write="reason"]').fill('Leio X porque Y.');await k.locator('select').selectOption('com apoio');await k.locator('.lf-levels [data-level="3"]').click();
  await k.locator('details.lf-personal summary').click();const ini=await k.locator('details.lf-personal').innerText();assert.match(ini,/Leio X porque Y\./);assert.match(ini,/com apoio/);assert.match(ini,/«gigantesco inseto»/);
  // contraste do botão principal ao passar o rato, nos dois temas
  for(const tema of ['light','dark']){await pg.evaluate(t=>localStorage.setItem('epi-theme',t),tema);await pg.reload();await pg.locator('#kafka .lf-primary').hover();
   const ratio=await pg.locator('#kafka .lf-primary').evaluate(el=>{const cs=getComputedStyle(el),rgb=s=>s.match(/\d+(\.\d+)?/g).slice(0,3).map(Number),L=([r,g,b])=>{const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4);};return .2126*f(r)+.7152*f(g)+.0722*f(b);},a=L(rgb(cs.color)),b2=L(rgb(cs.backgroundColor));return (Math.max(a,b2)+.05)/(Math.min(a,b2)+.05);});
   assert(ratio>=4.5,tema+' '+ratio);}
  await c.close();}
 // 320 px: nada sai para o lado
 {const c=await novoCtx(b,{viewport:{width:320,height:640}}),pg=await c.newPage();vigiar(pg);
  for(const u of ['/narrativas/formas/certa-manha/','/narrativas/corta/cena-que-falta/']){await pg.goto(base+u);for(let i=0;i<3;i++){assert(await semRolar(pg),u+' '+i);const b2=pg.locator('.casca-acoes [data-seguinte]');if(await b2.isDisabled())break;await b2.click();}}
  await c.close();const c4=await novoCtx(b,{viewport:{width:320,height:640}}),p4=await c4.newPage();vigiar(p4);
  await p4.goto(base+'/narrativas/corta/cena-que-falta/');await seguinte(p4);await p4.locator('[data-inicial="H1"]').click();await seguinte(p4);await p4.locator('[data-cand="cartao"]').click();assert(await semRolar(p4));await c4.close();}
 assert.deepEqual(erros,[]);console.log('PASS protótipos: combinações «ambos» e «nenhuma», sequência com e sem movimento, projeção velada e sem gravar, aparelho partilhado, recomeçar sem apagar a primeira leitura, papel com os quatro desenhos no PDF, entrada e selos, obras com a frase nova, contraste e 320 px');
}
async function run(){await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port;let b;
try{b=await chromium.launch({headless:true,...(process.env.PT_BROWSER_EXECUTABLE?{executablePath:process.env.PT_BROWSER_EXECUTABLE}:{}),...(process.env.PT_BROWSER_CHANNEL?{channel:process.env.PT_BROWSER_CHANNEL}:{})});
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
   await page.locator('#knowledge').click();assert(await page.locator('.lf-knowledge dl').isVisible());const known=await page.locator('.lf-knowledge dd').nth(1).innerText();assert.match(known,mission===0?/Já viste a entrega/:mission===2?/Ainda não viste a perda/:/Viste a perda/);
   const before=await page.locator('.lf-compare section').nth(1).innerText();await page.locator('#omit').selectOption({index:1});assert.equal(await page.locator('.lf-countercut .lf-frame').count(),1);await page.locator('[data-frame="C"][data-dir="1"]').click();assert.equal(await page.locator('.lf-compare section').nth(1).innerText(),before);

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
 for(const width of [360,1440]){
 await page.setViewportSize({width,height:1000});await page.goto(base+'/narrativas/formas/');await page.locator('#kafka').waitFor();
 for(const id of ['kafka','mia','cesariny']){
  await page.locator('[data-open="'+id+'"]').click();const c=page.locator('#'+id);
  await c.locator('[data-anchor="0"]').focus();await page.keyboard.press('Space');assert.equal(await c.locator('[data-anchor="0"]').getAttribute('aria-pressed'),'true');
  await c.locator('.lf-levels [data-level="1"]').click();await c.locator('[data-hypothesis="1"]').click();await c.locator('[data-write="reason"]').fill('Leio assim porque encontro esta expressão.');await c.locator('select').selectOption('com apoio');
  await c.locator('.lf-levels [data-level="2"]').click();await c.locator('[data-write="counter"]').fill('A objeção é possível, mas tem limites.');await c.locator('[data-model]').click();assert.equal(await c.locator('[data-model]').getAttribute('aria-expanded'),'true');
  await c.locator('.lf-levels [data-level="3"]').click();await c.locator('[data-compare]').click();const original=await c.locator('.lf-original').innerText();await c.locator('[data-version="1"]').click();assert.notEqual(await c.locator('.lf-original').innerText(),original);
  await c.locator('[data-write="draft"]').fill('Primeira tentativa <img src=x>');await c.locator('[data-keep]').click();await c.locator('[data-write="draft"]').fill('Versão revista');page.once('dialog',d=>d.dismiss());await c.locator('[data-reset]').click();assert.equal(await c.locator('[data-write="draft"]').inputValue(),'Versão revista');assert.match(await c.locator('.lf-first').innerText(),/<img src=x>/);assert.equal(await c.locator('.lf-first img').count(),0);
  await c.locator('[data-write="reflection"]').fill('Mudei o ponto de vista.');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.locator('#projection').click();assert(await c.locator('.lf-first').isHidden());assert(await c.locator('[data-write="draft"]').isHidden());await page.locator('#projection').click();
  await c.locator('.lf-levels [data-level="1"]').click();assert.equal(await c.locator('[data-write="reason"]').inputValue(),'Leio assim porque encontro esta expressão.');await c.locator('.lf-levels [data-level="3"]').click();assert.equal(await c.locator('[data-write="draft"]').inputValue(),'Versão revista');
 }
 await page.locator('[data-filter="all"]').click();assert.equal(await page.locator('.lf-case').count(),10);await page.locator('[data-filter="pt"]').click();assert.equal(await page.locator('.lf-case .lf-pt[open]').count(),10);assert.equal(await page.locator('#cesariny [data-write="draft"]').inputValue(),'Versão revista');
 console.log('PASS four interpretation levels, evidence, competing hypotheses, counter-reading and draft revision at '+width+'px');
 }
 await page.reload();await page.locator('#kafka').waitFor();assert.equal(await page.locator('[data-write="draft"]').count(),0);
 await page.goto(base+'/narrativas/formas/?mesa=pt');await page.locator('#gogol').waitFor();assert.equal(await page.locator('[data-filter="pt"]').getAttribute('aria-pressed'),'true');
 await page.goto(base+'/narrativas/');assert.match(await page.locator('h1').innerText(),/Laboratório de formas/);assert.equal(await page.locator('section.lab-set').count(),3);assert.match(await page.locator('[data-formas-progress]').innerText(),/4 de 4/);
 await page.goto(base+'/narrativas/corta/');assert.equal(await page.locator('.missoes a[data-id]').count(),8);
 if(process.env.LENTE_SHOTS){fs.mkdirSync(process.env.LENTE_SHOTS,{recursive:true});await page.goto(base+'/narrativas/');await page.screenshot({path:path.join(process.env.LENTE_SHOTS,'lente-entrada.png'),fullPage:true,animations:'disabled'});await page.goto(base+'/narrativas/corta/mesa/');await page.screenshot({path:path.join(process.env.LENTE_SHOTS,'lente-corta.png'),fullPage:true,animations:'disabled'});await page.locator('[data-phase="1"]').click();await page.locator('[data-preset]').click();await page.locator('#compare').click();await page.screenshot({path:path.join(process.env.LENTE_SHOTS,'lente-comparar.png'),fullPage:true,animations:'disabled'});await page.goto(base+'/narrativas/formas/');await page.locator('#kafka').waitFor();await page.screenshot({path:path.join(process.env.LENTE_SHOTS,'lente-obras.png'),fullPage:true,animations:'disabled'});}
 if(process.env.LENTE_PREVIEW_DIR){
  const {pathToFileURL}=require('node:url');await page.goto(pathToFileURL(path.join(process.env.LENTE_PREVIEW_DIR,'obras-para-experimentar.html')).href);await page.locator('#kafka').waitFor();await page.locator('#kafka [data-anchor="0"]').click();await page.locator('#kafka .lf-levels [data-level="3"]').click();await page.locator('#kafka [data-compare]').click();assert(await page.locator('.lf-original').isVisible());await page.goto(pathToFileURL(path.join(process.env.LENTE_PREVIEW_DIR,'corta.html')).href);await page.locator('[data-phase="1"]').click();await page.locator('[data-preset]').click();await page.locator('#compare').click();await page.locator('#omit').selectOption({index:1});assert(await page.locator('[data-frame="C"]').first().isVisible());console.log('PASS standalone file previews without a server');
 }
 assert.deepEqual(errors,[]);assert.equal(D.items.filter(x=>x.status==='excerto-consultado').length,3);console.log('PASS source-backed reading experiments, drafts retained across filters, 10-source corpus, PT bridges, original routes and legacy progress; no browser errors');
 await prototipos(b,base);
 await ctx.close();
}finally{if(b)await b.close();await new Promise(r=>server.close(r));}}
run().catch(e=>{console.error(e);process.exitCode=1;});
