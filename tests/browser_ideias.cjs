// 02/11/2026: pedido 2. Proposta A substitui gesto/atol/composição antiga.
// Mantém documentos, impressão e percursos das sessões; acrescenta 27 estados reais, teclado e movimento reduzido.
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

(async()=>{await new Promise(r=>srv.listen(0,r));const base='http://localhost:'+srv.address().port+'/lente/';const b=await chromium.launch(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{});
const rows=[],out=process.env.IDEIAS_PROVAS;if(out)fs.mkdirSync(out,{recursive:true});
try{
for(const width of [320,390,1366])for(const mode of ['light','dark','projection'])for(const estado of ['inicio','meio','feito']){
 const ctx=await b.newContext({viewport:{width,height:900},colorScheme:mode==='dark'?'dark':'light',reducedMotion:'reduce'}),p=await ctx.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));
 await p.addInitScript(({estado})=>{localStorage.setItem('epi-ultima','não alterar');if(estado!=='inicio')localStorage.setItem('epi-lab-ideias-s01',JSON.stringify({versao:'antiga',lida:true,t:Date.parse('2026-11-01T12:00:00Z'),melhor:10}));if(estado==='feito')localStorage.setItem('epi-lab-ideias-s02',JSON.stringify({versao:'nova',antes:{versao:'antiga',lida:true,data:Date.parse('2026-11-02T12:00:00Z')}}));},{estado});
 await p.goto(base+'narrativas/ideias/'+(mode==='projection'?'?projetar=1':''));await p.waitForTimeout(200);
 const armazenamento=await p.evaluate(()=>JSON.stringify(Object.entries(localStorage).sort()));
 const botao=p.locator('[data-p-botao]'),r=await botao.boundingBox();assert(r&&r.y+r.height<=900,'ação fora do primeiro ecrã');assert.equal(await botao.count(),1);
 const inicio=mode==='projection'||estado==='inicio',acao=inicio?'Começar':estado==='meio'?'Continuar':'Rever';assert.match(await botao.innerText(),new RegExp('^'+acao));assert.match(await botao.getAttribute('href'),new RegExp('sessao-0'+(inicio?1:2)+'/'));
 assert.equal(await p.locator('li.feita').count(),mode==='projection'?0:estado==='inicio'?0:estado==='meio'?1:2);
 if(!inicio)assert.match(await p.locator('li.feita [data-estado]').first().textContent(),/Feita 01\/11/);
 assert.equal(await p.locator('a[aria-current="step"]').count(),mode==='projection'||estado!=='feito'?1:0);
 assert.equal(await largo(p),0);assert.equal(await p.locator('[data-gesto],.atol').count(),0);
 assert.equal(await p.locator('h1').getAttribute('aria-label'),'Ideias');assert.equal(await p.locator('h1 .pingo-retro[aria-hidden="true"]').count(),1);
 const acento=await p.locator('h1 .pingo-retro').evaluate(e=>{const s=getComputedStyle(e,'::after');return{w:parseFloat(s.width),h:parseFloat(s.height),bg:s.backgroundColor}});assert(acento.w>0&&acento.w<12&&acento.h===acento.w);assert.notEqual(acento.bg,'rgba(0, 0, 0, 0)');

 const details=p.locator('details.metodo'),sum=details.locator('summary');assert.equal(await details.evaluate(e=>e.open),false);
 await sum.focus();assert.equal(await sum.evaluate(e=>e===document.activeElement),true);assert.notEqual(await sum.evaluate(e=>getComputedStyle(e).outlineStyle),'none');
 await p.keyboard.press('Enter');assert.equal(await details.evaluate(e=>e.open),true);assert.equal(await details.locator('ol li').count(),5);assert(await details.locator('a').isVisible());
 await p.keyboard.press('Space');assert.equal(await details.evaluate(e=>e.open),false);assert.equal(await p.evaluate(()=>JSON.stringify(Object.entries(localStorage).sort())),armazenamento,'abrir método escreve progresso');
 const motion=await p.locator('.drawing svg').evaluate(e=>({anim:getComputedStyle(e).animationName,transition:getComputedStyle(e).transitionDuration}));assert.equal(motion.anim,'none');assert.equal(motion.transition,'0s');
 const contraste=await p.evaluate(()=>{function rgb(s){return s.match(/[\d.]+/g).slice(0,3).map(Number)}function lum(v){return rgb(v).map(n=>{n/=255;return n<=.04045?n/12.92:Math.pow((n+.055)/1.055,2.4)}).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0)}function ratio(a,b){a=lum(a);b=lum(b);return(Math.max(a,b)+.05)/(Math.min(a,b)+.05)}const body=getComputedStyle(document.body),btn=getComputedStyle(document.querySelector('[data-p-botao]'));return {acao:ratio(btn.color,btn.backgroundColor),estado:ratio(getComputedStyle(document.querySelector('.state')).color,body.backgroundColor)};});
 assert(contraste.acao>=4.5&&contraste.estado>=4.5,JSON.stringify(contraste));
 assert.deepEqual(erros,[]);if(out)await p.screenshot({path:path.join(out,`entrada-${width}-${mode}-${estado}.png`),fullPage:true});rows.push({width,mode,estado,acao,contraste,erros});await ctx.close();
}
console.log('PASS entrada A: 27 contextos, progresso antigo, projeção, ação principal, teclado, contraste e movimento reduzido');
// Documentos e Biblioteca continuam a ser medidos nas cinco larguras dos testes anteriores, nos dois temas.
for(const pag of PAGINAS.slice(1))for(const [w,h] of LARGURAS)for(const tema of ['light','dark']){
 const {ctx,p,erros}=await abrir(b,base+pag,w,h,tema);assert.equal(await largo(p),0,pag+' '+w+' '+tema);assert.equal(await p.locator('meta[name=robots][content*=noindex]').count(),0);assert.deepEqual(erros,[]);await ctx.close();
}
for(const [pag,n] of [['narrativas/ideias/guiao/',4],['narrativas/ideias/docente/',9]]){
 const {ctx,p}=await abrir(b,base+pag,1024,768,'light');await p.emulateMedia({media:'print'});const pdf=await p.pdf({format:'A4',printBackground:true,preferCSSPageSize:true});const pags=(pdf.toString('latin1').match(/\/Type\s*\/Page[^s]/g)||[]).length;assert.equal(pags,n,pag+': páginas A4');if(out)fs.writeFileSync(path.join(out,pag.includes('docente')?'guia.pdf':'guiao.pdf'),pdf);await ctx.close();
}
console.log('PASS documentos: 30 contextos e impressão A4 (4 e 9 páginas)');
 // 4. as duas lições a responder certo, a 320 px (claro) e a 1440 px (escuro), sem deslize em nenhum cartão
 for(const f of ['ideias-s01.json','ideias-s02.json']){const d=JSON.parse(fs.readFileSync(path.join(ROOT,'tools/licoes',f),'utf8'));
  for(const [w,h,tema] of [[320,640,'light'],[1440,900,'dark']]){
   const {ctx,p,erros}=await abrir(b,base+d.saida.replace(/index\.html$/,''),w,h,tema);
   for(let i=0;i<d.cartoes.length;i++){const x=d.cartoes[i];
    assert.equal(await largo(p),0,f+' cartão '+(i+1)+' a '+w+' px');
    if(x.t!=='ler'){await responder(p,x);assert.match(await p.locator('.casca-folha').innerText(),/Certo/,f+' cartão '+(i+1)+' ('+x.t+') a '+w+' px');assert.equal(await largo(p),0,f+' folha do cartão '+(i+1)+' a '+w+' px')}
    if(i<d.cartoes.length-1)await seguinte(p)}
   await seguinte(p);await p.waitForTimeout(1100);assert.match(await p.locator('.fim').innerText(),/Lição feita/);assert.doesNotMatch(await p.locator('.fim').innerText(),/\d+\s+(?:pontos|de\s+\d+)/);
   assert.deepEqual(erros,[],f+' a '+w+' px');await ctx.close();
   console.log('PASS '+d.id+': '+d.cartoes.length+' cartões a responder certo a '+w+' px ('+tema+'), sem deslize')}}

if(out)fs.writeFileSync(path.join(out,'medidas.json'),JSON.stringify(rows,null,2));
}finally{await b.close();srv.closeAllConnections();srv.close()}
})().catch(e=>{console.error(e);process.exit(1)});
