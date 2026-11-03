// 03/11/2026: sessão-modelo isolada, 20 cartões e 14 atividades.
// Percurso completo em 320/390/1366, claro/escuro e modo de projeção.
// Confere também o lançador real, visor por teclado, resultado privado e progresso original intacto.
const {chromium}=require('playwright');const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
const ROOT=path.resolve(__dirname,'..'),resultados=[];
const sessoes=process.env.CIDADANIA_SESSAO?[process.env.CIDADANIA_SESSAO]:['01','02','03','04'];assert(sessoes.every(n=>/^0[1-4]$/.test(n)));
const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript','.json':'application/json','.css':'text/css','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.jpg':'image/jpeg'};
const srv=http.createServer((q,r)=>{let u=decodeURIComponent(q.url.split('?')[0]).replace(/^\/lente(?=\/)/,'');if(u.endsWith('/'))u+='index.html';const f=path.join(ROOT,u);if(!f.startsWith(ROOT)||!fs.existsSync(f)){r.writeHead(404);r.end();return}r.writeHead(200,{'content-type':mime[path.extname(f)]||'application/octet-stream'});fs.createReadStream(f).pipe(r)});
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
 else if(x.t==='emparelhar'){for(const [a,b] of x.pares){await p.locator('#baralho').getByRole('button',{name:vis(a),exact:true}).click();await p.waitForTimeout(80);await p.locator('#baralho').getByRole('button',{name:vis(b),exact:true}).click();await p.waitForTimeout(120)}}
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
(async()=>{await new Promise(r=>srv.listen(0,r));const base='http://localhost:'+srv.address().port;const b=await chromium.launch(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{});
 for(const f of sessoes.map(n=>'cidadania-m1-s'+n+'.json')){
  const d=JSON.parse(fs.readFileSync(path.join(ROOT,'tools/cidadania-interativas',f),'utf8'));const url=base+'/'+d.saida.replace(/index\.html$/,'');
  const fazer=d.cartoes.filter(x=>x.t!=='ler').length;
  for(const [w,h] of [[320,900],[390,900],[1366,900]])for(const tema of ['light','dark'])for(const projecao of [false,true]){
   const ctx=await b.newContext({viewport:{width:w,height:h},colorScheme:tema});const p=await ctx.newPage();const erros=[];p.on('pageerror',e=>erros.push(e.message));
   await p.addInitScript(k=>localStorage.setItem(k,JSON.stringify({lida:true,versao:'original',t:123,exposicoes:{3:7},resposta:'ANTERIOR'})),d.chave);await p.goto(url+(projecao?'?projetar=1':''));await p.waitForTimeout(500);
   // o motor baralha os cartões de fazer do mesmo grupo «g» e alterna p/p2: o cartão do ecrã identifica-se pelo enunciado
   const norm=t=>String(t||'').replace(/<[^>]+>/g,' ').replace(/[*_]/g,'').replace(/\s+/g,' ').trim();
   async function atual(i){const txt=norm(await p.locator('#baralho').innerText());const c=d.cartoes.filter(x=>x.t!=='ler'&&[x.p,x.p2].some(q=>q&&txt.includes(norm(q).slice(0,60))));return c.length===1?c[0]:d.cartoes[i]}
   for(let i=0;i<d.cartoes.length;i++){const x=d.cartoes[i].t==='ler'?d.cartoes[i]:await atual(i);
    assert.equal(await p.locator('[data-c-num]').innerText(),(i+1)+'/'+d.cartoes.length,f+' cartão '+(i+1));
    assert(await p.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),'deslocamento horizontal no cartão '+(i+1)+' a '+w+' px');
    if(i===1&&d.ampliar){const img=p.locator('#baralho figure img');await img.focus();await p.keyboard.press('Enter');assert.equal(await p.locator('.amp-ov[role="dialog"]').count(),1);assert(await p.locator('.casca').evaluate(e=>e.inert));await p.locator('.amp-tools button',{hasText:/^Ampliar$/}).click();assert.equal(await p.locator('.amp-tools output').innerText(),'150 %');await p.keyboard.press('Escape');assert.equal(await p.locator('.amp-ov').count(),0);assert(await img.evaluate(e=>document.activeElement===e));}
    if(process.env.MODELO_PROVAS&&[0,1,4,8,13,19].includes(i)){fs.mkdirSync(process.env.MODELO_PROVAS,{recursive:true});await p.screenshot({path:path.join(process.env.MODELO_PROVAS,`${d.id}-cartao-${i+1}-${w}-${tema}-${projecao?"projecao":"normal"}.png`)});}
    if(x.t!=='ler'){await responder(p,x);assert.match(await p.locator('.casca-folha').innerText(),/Certo/,f+' cartão '+(i+1)+' ('+x.t+')')}
    if(i<d.cartoes.length-1)await seguinte(p);
   }
   await seguinte(p).catch(()=>{});await p.waitForTimeout(1400); // o «x de y» do fim anima durante cerca de 900 ms
   const fim=await p.locator('#baralho').innerText();if(projecao){assert.match(fim,/Fim da lição/);assert.doesNotMatch(fim,/\d+\s+de\s+\d+/,'a projeção não expõe o resultado individual');}else assert.match(fim,new RegExp(fazer+'\\s*de\\s*'+fazer),f+': o fim tem de mostrar '+fazer+' de '+fazer);
   assert.equal(await p.evaluate(k=>localStorage.getItem(k),d.chave),JSON.stringify({lida:true,versao:'original',t:123,exposicoes:{3:7},resposta:'ANTERIOR'}));
   const st=await p.evaluate(k=>JSON.parse(localStorage.getItem(k)||'null'),d.chave+'-'+d.edicao);if(projecao)assert.equal(st,null,f+': a projeção completa não grava progresso');else assert(st&&st.melhor===fazer,f+': progresso gravado em '+d.chave);
   if(w===390)await p.screenshot({path:path.join(require('os').tmpdir(),'licao-'+d.id+'-fim-390.png')});
   assert.deepEqual(erros,[],f+' a '+w+' px');await ctx.close();
   resultados.push({sessao:d.id,largura:w,tema,projecao,cartoes:d.cartoes.length,atividades:fazer,todasCertas:true,originalIntacto:true,semErros:true});
   console.log('PASS '+d.id+': '+d.cartoes.length+' cartões, '+fazer+' de fazer, todos certos, fim e progresso a '+w+' px, '+tema+', '+(projecao?'projeção':'normal'));
  }
 }
 for(const n of sessoes)for(const w of [320,390,1366])for(const tema of ['light','dark']){
  const ctx=await b.newContext({viewport:{width:w,height:900},colorScheme:tema}),p=await ctx.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));
  const chave='epi-cid-m1-s'+n;await ctx.addInitScript(k=>localStorage.setItem(k,JSON.stringify({lida:true,versao:'original',t:123})),chave);
  await p.goto(base+'/lente/projetar/?pagina=/lente/cidadania/m1/licoes/'+n+'/');await p.frameLocator('#lesson-frame').locator('html.epi-projection').waitFor();
  const frame=p.frames().find(f=>f!==p.mainFrame()&&f.url().includes('/cidadania/m1/licoes/'+n+'/'));
  assert.equal(await frame.locator('[data-c-num]').innerText(),'1/20');await seguinte(frame);
  assert.equal(await frame.locator('[data-c-num]').innerText(),'2/20');assert(await frame.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  if(n!=='03'){const img=frame.locator('#baralho figure img');await img.focus();await p.keyboard.press('Enter');assert.equal(await frame.locator('.amp-ov[role="dialog"]').count(),1);await p.keyboard.press('Escape');assert(await img.evaluate(e=>document.activeElement===e));}
  assert.equal(await frame.evaluate(k=>localStorage.getItem(k),chave+'-20261103'),null);assert.equal(await frame.evaluate(k=>localStorage.getItem(k),chave),JSON.stringify({lida:true,versao:'original',t:123}));assert.deepEqual(erros,[]);
  if(process.env.MODELO_PROVAS)await p.screenshot({path:path.join(process.env.MODELO_PROVAS,`lancador-${n}-${w}-${tema}.png`)});
  resultados.push({sessao:n,largura:w,tema,lancadorReal:true,visorTeclado:true,originalIntacto:true,semErros:true});await ctx.close();console.log('PASS lançador real '+w+' '+tema);
 }
 if(process.env.MODELO_PROVAS)fs.writeFileSync(path.join(process.env.MODELO_PROVAS,'resultado.json'),JSON.stringify(resultados,null,2));
 await b.close();srv.close();})().catch(e=>{console.error(e);process.exit(1)});
