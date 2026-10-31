// 30/10/2026: lições do Lente no motor único (assets/licoes/), a começar pela sessão 01 do M1 de Cidadania (piloto).
// Percorre cada lição de tools/licoes/*.json a responder certo a todos os cartões, em 390 e 1366 px, e confirma: nenhum
// erro, nenhum deslocamento horizontal, o fim com todas as certas, o progresso gravado na chave da lição, e a projeção a
// não gravar nada.
const {chromium}=require('playwright');const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
const ROOT=path.resolve(__dirname,'..');
const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript','.json':'application/json','.css':'text/css','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.jpg':'image/jpeg'};
const srv=http.createServer((q,r)=>{let u=decodeURIComponent(q.url.split('?')[0]);if(u.endsWith('/'))u+='index.html';const f=path.join(ROOT,u);if(!f.startsWith(ROOT)||!fs.existsSync(f)){r.writeHead(404);r.end();return}r.writeHead(200,{'content-type':mime[path.extname(f)]||'application/octet-stream'});fs.createReadStream(f).pipe(r)});
async function seguinte(p){const s=p.locator('.casca-folha:not([hidden]) button, .casca-acoes button',{hasText:/Seguinte|Continuar|Ver o resultado|Terminar/});await s.first().click();await p.waitForTimeout(250)}
async function responder(p,x){
 if(x.t==='escolha'){await p.locator('#baralho button.op',{hasText:x.o[x.c]}).first().click()}
 else if(x.t==='vf'){await p.locator('#baralho button.op',{hasText:x.v?'Verdadeiro':'Falso'}).click()}
 else if(x.t==='emparelhar'){for(const [a,b] of x.pares){await p.locator('#baralho button',{hasText:a}).first().click();await p.waitForTimeout(80);await p.locator('#baralho button',{hasText:b}).first().click();await p.waitForTimeout(120)}}
 else if(x.t==='sublinhar'){for(const j of x.certas)await p.locator('#baralho button.pal[data-j="'+j+'"]').click();await p.locator('.casca-acoes [data-confirmar]').click()}
 else if(x.t==='ordenar'){for(const t of x.passos){await p.locator('#baralho .soltos button',{hasText:t}).first().click();await p.waitForTimeout(80)}}
 // 30/10/2026: as sessões 02 a 10 do M1 (pilotos de 31/10) têm cartões de completar; em cada lacuna escolhe-se o valor da
 // opção certa, como o motor o guarda (o valor é o índice da opção em lacunas[k].o; data-k é a ordem da lacuna na frase).
 else if(x.t==='completar'){for(let k=0;k<x.lacunas.length;k++){await p.locator('#baralho select[data-k="'+k+'"]').selectOption(String(x.lacunas[k].c));await p.waitForTimeout(80)}}
 else throw new Error('tipo sem resposta automática: '+x.t);
 await p.waitForTimeout(350);
 const conf=p.locator('.casca-acoes [data-confirmar]');if(await conf.count()&&await conf.isVisible()&&await conf.isEnabled())await conf.click();
 await p.waitForTimeout(250);
}
(async()=>{await new Promise(r=>srv.listen(0,r));const base='http://localhost:'+srv.address().port;const b=await chromium.launch();
 for(const f of fs.readdirSync(path.join(ROOT,'tools/licoes')).filter(f=>f.endsWith('.json'))){
  const d=JSON.parse(fs.readFileSync(path.join(ROOT,'tools/licoes',f),'utf8'));const url=base+'/'+d.saida.replace(/index\.html$/,'');
  const fazer=d.cartoes.filter(x=>x.t!=='ler').length;
  for(const [w,h] of [[390,844],[1366,900]]){
   const ctx=await b.newContext({viewport:{width:w,height:h}});const p=await ctx.newPage();const erros=[];p.on('pageerror',e=>erros.push(e.message));
   await p.goto(url);await p.waitForTimeout(500);
   // o motor baralha os cartões de fazer do mesmo grupo «g» e alterna p/p2: o cartão do ecrã identifica-se pelo enunciado
   const norm=t=>String(t||'').replace(/<[^>]+>/g,' ').replace(/[*_]/g,'').replace(/\s+/g,' ').trim();
   async function atual(i){const txt=norm(await p.locator('#baralho').innerText());const c=d.cartoes.filter(x=>x.t!=='ler'&&[x.p,x.p2].some(q=>q&&txt.includes(norm(q).slice(0,60))));return c.length===1?c[0]:d.cartoes[i]}
   for(let i=0;i<d.cartoes.length;i++){const x=d.cartoes[i].t==='ler'?d.cartoes[i]:await atual(i);
    assert.equal(await p.locator('[data-c-num]').innerText(),(i+1)+'/'+d.cartoes.length,f+' cartão '+(i+1));
    assert(await p.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),'deslocamento horizontal no cartão '+(i+1)+' a '+w+' px');
    if(x.t!=='ler'){await responder(p,x);assert.match(await p.locator('.casca-folha').innerText(),/Certo/,f+' cartão '+(i+1)+' ('+x.t+')')}
    if(i<d.cartoes.length-1)await seguinte(p);
   }
   await seguinte(p).catch(()=>{});await p.waitForTimeout(1400); // o «x de y» do fim anima durante cerca de 900 ms
   const fim=await p.locator('#baralho').innerText();assert.match(fim,new RegExp(fazer+'\\s*de\\s*'+fazer),f+': o fim tem de mostrar '+fazer+' de '+fazer);
   const st=await p.evaluate(k=>JSON.parse(localStorage.getItem(k)||'null'),d.chave);assert(st&&st.melhor===fazer,f+': progresso gravado em '+d.chave);
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
 await b.close();srv.close();})().catch(e=>{console.error(e);process.exit(1)});
