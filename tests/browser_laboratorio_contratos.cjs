// 02/11/2026: contratos opcionais do pedido 2, sem conteúdo novo publicado.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
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


(async()=>{await new Promise(r=>srv.listen(0,r));const base='http://localhost:'+srv.address().port+'/lente/',b=await chromium.launch(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{});
try{for(const w of [390,1366])for(const proj of [false,true]){
 const {ctx,p,erros}=await abrir(b,base+'narrativas/ideias/sessao-01/'+(proj?'?projetar=1':''),w,900,'light');
 await p.addScriptTag({url:base+'assets/licoes/relogio.js'});const antes=await p.evaluate(()=>JSON.stringify(Object.entries(localStorage).sort()));
 await p.evaluate(()=>{const imagens=[0,1,2].map(j=>({src:'../../../assets/laboratorio/ideias/atget-quiosque-fiacres.webp?amostra='+j,alt:'Fotografia de uma rua, amostra '+j+'.',credito:'Eugène Atget, CC0. Amostra '+j+'.'}));EPIJogo.montar({casca:EPICasca.pagina(),el:document.querySelector('#baralho'),marca:'Verificação',chave:'qa-creditos-2',semPontos:true,aula:true,variar:false,itens:[{t:'escolha',p:'Escolhe um.',o:['Um','Dois'],c:0,f:'Um vem primeiro.',fe:['','Dois vem depois.'],imagens:imagens.slice(0,2)},{t:'ordenar',p:'Ordena.',passos:['Um','Dois','Três'],f:'Esta é a ordem.',imagens},{t:'ler',rot:'Para levar',html:'<div class="tr-relogio" data-relogio="3"><p class="tr-tempo">0:03</p><button data-rl="ir">Começar</button><button data-rl="parar">Pausa</button><button data-rl="zero">Repor</button><p class="tr-aviso" role="status"></p></div>'}]})});
 await p.locator('.op-imagem').first().waitFor();assert.equal(await p.locator('.op-imagem').count(),2);assert(await p.locator('.op-imagem').first().evaluate(e=>e.complete&&e.naturalWidth>0));
 // Conferir por índice de dados, nunca pela posição visual baralhada.
 async function creditos(){for(const btn of await p.locator('#baralho button.op').all()){
  const j=await btn.getAttribute('data-j'),cred=btn.locator('.op-credito');
  assert.equal(await cred.innerText(),'Eugène Atget, CC0. Amostra '+j+'.');assert(await cred.isVisible());
  assert.equal(await btn.locator('img').getAttribute('alt'),'Fotografia de uma rua, amostra '+j+'.');
  assert((await btn.locator('img').getAttribute('src')).endsWith('?amostra='+j));
  assert.equal(await btn.locator('a,button').count(),0);assert.match(await btn.ariaSnapshot(),/Eugène Atget, CC0/);
 }}
 await creditos();let baralhadas=(await p.locator("#baralho button.op").evaluateAll(bs=>bs.map(b=>b.dataset.j).join(",")))!=="0,1";
 const errada=p.locator('#baralho button.op',{hasText:'Dois'});await errada.focus();await p.keyboard.press('Enter');assert.match(await p.locator('.casca-folha').innerText(),/Dois vem depois/);await seguinte(p);
 assert.equal(await p.locator('.op-imagem').count(),3);await creditos();baralhadas=baralhadas&&(await p.locator('#baralho button.op').evaluateAll(bs=>bs.map(b=>b.dataset.j).join(',')))!=='0,1,2';assert(baralhadas,'a amostra tem de exercer uma ordem baralhada');
 // Selecionar e retirar antes da sequência completa mantém a atribuição no mesmo botão.
 const primeiro=p.locator('#baralho button.op[data-j="0"]');await primeiro.click();await creditos();await primeiro.click();await creditos();
 for(const t of ['Um','Dois','Três']){const btn=p.locator('.soltos button',{hasText:t});await btn.focus();await p.keyboard.press('Enter');await creditos()}
 assert.match(await p.locator('.casca-folha').innerText(),/Certo/);await seguinte(p);
 // 03/11/2026: L106-02. Usar o comando publicado e provar a pausa antes de repor.
 await p.locator('[data-rl="ir"]').click();await p.waitForFunction(()=>document.querySelector('[data-relogio]').getAttribute('data-resta')==='2');await p.locator('[data-rl="parar"]').click();
 const relogio=p.locator('[data-relogio]');assert.equal(await relogio.evaluate(e=>e.classList.contains('a-correr')),false);assert.equal(await relogio.getAttribute('data-resta'),'2');const tempoParado=await p.locator('.tr-tempo').innerText();await p.waitForTimeout(1250);assert.equal(await relogio.getAttribute('data-resta'),'2');assert.equal(await p.locator('.tr-tempo').innerText(),tempoParado);assert.equal(await relogio.evaluate(e=>e.classList.contains('a-correr')),false);await p.locator('[data-rl="zero"]').click();assert.equal(await p.locator('.tr-tempo').innerText(),'0:03');
 await seguinte(p);await p.waitForTimeout(1100);assert.doesNotMatch(await p.locator('.fim').innerText(),/\d+\s+(?:pontos|de\s+\d+)/);if(proj)assert.equal(await p.evaluate(()=>JSON.stringify(Object.entries(localStorage).sort())),antes);else assert.equal(await p.evaluate(()=>JSON.parse(localStorage.getItem('qa-creditos-2')).melhor),1);
 assert.equal(await largo(p),0);assert.deepEqual(erros,[]);await ctx.close();console.log('PASS imagens, teclado, retorno e relógio',w,proj);
}}finally{await b.close();srv.closeAllConnections();srv.close()}})().catch(e=>{console.error(e);process.exit(1)});
