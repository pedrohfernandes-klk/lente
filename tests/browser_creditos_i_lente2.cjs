// 08/11/2026: decisões 153, 162 e 176 (pedido lente-2, famílias L8 a L13 do plano dos créditos). Uma amostra de cada família de
// «i» novos (desenhos da Justiça, sozinhos e lado a lado; Ética e Estética; imagem e vídeo do piloto do M1 e do «Ideias»; abertura,
// material e as duas fotografias de uma sessão do M2; guia das sessões do M2; índice do M1), a 320, 390, 768 e 1280 px, em claro e
// em escuro: a página não desliza para o lado; o «i» está fechado ao carregar, tem alvo de 44 px e o nome «Créditos…»; abre e
// fecha por clique, abre com Enter e fecha com Escape (o foco volta ao «i»); um clique fora fecha; aberto, o crédito é o de antes,
// palavra a palavra e com as mesmas ligações, cabe no ecrã, não tapa texto nem fica tapado, e lê-se (contraste de 4,5:1); na
// impressão, o «i» não sai e o crédito sai por extenso sempre que sai a imagem a que pertence, com o endereço da licença.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict'),{execFileSync}=require('child_process');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),BASE='cc75fc62e18a731c671ad9f06f8fb708af6f7ddb';
const antigo=p=>execFileSync('git',['show',BASE+':'+p],{cwd:root,encoding:'utf8',maxBuffer:1<<28}).replace(/\\"/g,'"').replace(/<\\\//g,'</');
const norm=s=>String(s).replace(/<[^>]+>/g,'').replace(/&amp;/g,'&').replace(/\s+/g,' ').trim();
const clean=s=>String(s||'').replace(/\*\*|_/g,'');
// os cartões de uma página (JSON dentro do <script>)
function banco(pg,chave){const src=fs.readFileSync(path.join(root,pg,'index.html'),'utf8');let i=src.indexOf('[',src.indexOf(chave));let d=0,str=false,esc=false;
 for(let k=i;k<src.length;k++){const c=src[k];if(str){if(esc)esc=false;else if(c==='\\')esc=true;else if(c==='"')str=false;continue}if(c==='"')str=true;else if(c==='[')d++;else if(c===']'&&!--d)return JSON.parse(src.slice(i,k+1));}}
// O crédito de antes (main cc75fc6), pelo que a figura mostra.
function legendaAntiga(pg,src){const s=antigo(pg+'index.html'),nome=src.split('/').pop();
 const f=[...s.matchAll(/<figure\b[^>]*>[\s\S]*?<\/figure>/g)].map(m=>m[0]).find(x=>x.includes(nome+'"')&&x.includes('<figcaption>'));assert.ok(f,pg+': figura antiga de '+nome);
 const cap=f.match(/<figcaption>([\s\S]*?)<\/figcaption>/)[1];return {texto:norm(cap),ligacoes:[...cap.matchAll(/href="([^"]+)"/g)].map(m=>m[1])};}
const PAGINAS=[
 {p:'olhar-e-decidir/justica/licao-1/',motor:'antigo',paradas:[{cartao:2,is:['desenho']},{cartao:11,is:['desenho','desenho']}]},
 {p:'olhar-e-decidir/etica/licao-1/',motor:'antigo',paradas:[{cartao:1,is:['fig']}]},
 {p:'olhar-e-decidir/estetica/licao-1/',motor:'antigo',paradas:[{cartao:1,is:['fig']}]},
 {p:'cidadania/piloto/m1-s01/',motor:'licoes',chave:'CARTOES=',paradas:[{cartao:5,is:['fig']},{cartao:6,is:['video']}]},
 {p:'narrativas/ideias/sessao-01/',motor:'licoes',chave:'CARTOES=',paradas:[{cartao:7,is:['video']},{cartao:10,is:['fig']}]},
 {p:'cidadania/m2/sessoes/05/',motor:'c10',paradas:[{passo:0,is:['fig']},{passo:2,is:['fig','par']}]},
 {p:'cidadania/m2/sessoes/',motor:'c10',paradas:[{passo:0,is:['fig']}]},
 {p:'cidadania/m1/',motor:'c10',paradas:[{passo:0,is:['m1']}]},
];
const server=http.createServer((req,res)=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname).replace(/^\/lente/,''));if(!f.startsWith(root+path.sep)&&f!==root){res.writeHead(403);return res.end();}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.webp':'image/webp','.jpg':'image/jpeg','.png':'image/png'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});
// Motor dos cartões da Justiça, da Ética e da Estética: responde certo até ao cartão «alvo» (contado a partir de 0).
async function motorAntigo(p,bank,de,alvo){
 for(let i=de;i<alvo;i++){
  await p.locator('#baralho .cartao').first().waitFor();
  const n=s=>clean(String(s||'').replace(/<[^>]+>/g,' ')).replace(/\s+/g,' ').trim();
  const visto=n(await p.locator('#baralho').innerText());const cand=bank.filter(x=>x.t!=='ler'&&[x.p,x.p2].some(q=>q&&visto.includes(n(q))));
  const x=bank[i].t==='ler'?bank[i]:(cand.length===1?cand[0]:bank[i]);
  if(x.t==='ler'){await p.locator('[data-c-acoes] [data-seguinte]').click();continue}
  if(x.t==='escolha')await p.locator('#baralho .ops button.op').filter({hasText:clean(x.o[x.c])}).first().click();
  else if(x.t==='vf')await p.locator('#baralho .ops button.op').filter({hasText:x.v?'Verdadeiro':'Falso'}).click();
  else if(x.t==='ordenar')for(const passo of x.passos)await p.locator('#baralho .soltos button.op').filter({hasText:clean(passo)}).first().click();
  else if(x.t==='emparelhar'){const col=await p.locator('#baralho .classes').count();for(let j=0;j<x.pares.length;j++){await p.locator('#baralho [data-e="'+j+'"]').click();if(col)await p.locator('#baralho .regiao .cab').filter({hasText:clean(x.pares[j][1])}).first().click();else await p.locator('#baralho [data-d="'+j+'"]').click();}}
  else throw Error('tipo sem resposta: '+x.t);
  await p.locator('[data-c-folha]:not([hidden]) [data-seguinte]').click();
 }
}
// Motor único das lições (assets/licoes/): o mesmo, para o piloto e o «Ideias».
async function motorLicoes(p,bank,de,alvo){
 for(let i=de;i<alvo;i++){const x=bank[i];
  if(x.t!=='ler'){
   if(x.t==='escolha')await p.locator('#baralho button.op',{hasText:clean(x.o[x.c])}).first().click();
   else if(x.t==='vf')await p.locator('#baralho button.op',{hasText:x.v?'Verdadeiro':'Falso'}).click();
   else if(x.t==='completar'){for(let k=0;k<x.lacunas.length;k++)await p.locator('#baralho select[data-k="'+k+'"]').selectOption(String(x.lacunas[k].c));}
   else if(x.t==='emparelhar'){for(const [a,b] of x.pares){await p.locator('#baralho button',{hasText:clean(a)}).first().click();await p.locator('#baralho button',{hasText:clean(b)}).first().click();}}
   else throw Error('tipo sem resposta: '+x.t);
   await p.waitForTimeout(300);const conf=p.locator('.casca-acoes [data-confirmar]');if(await conf.count()&&await conf.isVisible()&&await conf.isEnabled())await conf.click();await p.waitForTimeout(200);
  }
  await p.locator('.casca-folha:not([hidden]) button, .casca-acoes button',{hasText:/Seguinte|Continuar/}).first().click();await p.waitForTimeout(250);
 }
}
// Medidas dentro da página: o n-ésimo «i» à vista, aberto ou fechado.
function medir(n){
 const visivel=e=>!!e&&e.getClientRects().length>0&&e.checkVisibility({visibilityProperty:true,contentVisibilityAuto:true});
 const d=[...document.querySelectorAll('details.info-i[name="info-i"]')].filter(x=>visivel(x.querySelector('summary')))[n];
 const s=d.querySelector('summary'),t=d.querySelector('.info-i-texto'),fig=d.closest('figure'),yt=d.closest('.yt');
 const nt=x=>x.replace(/\s+/g,' ').trim();
 const fora=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let no;while(no=w.nextNode()){const el=no.parentElement;if(!no.data.trim()||d.contains(el)||el.closest('[aria-hidden="true"],script,style,.c-sr,.c10-sr,.salta,.sr-only')||!visivel(el))continue;const r=document.createRange();r.selectNodeContents(no);for(const q of r.getClientRects())if(q.width>1&&q.height>1)fora.push({x:q.left,y:q.top,r:q.right,b:q.bottom,t:no.data.trim().slice(0,40)});}
 const cruza=(a,b)=>a.left<b.r-1&&a.right>b.x+1&&a.top<b.b-1&&a.bottom>b.y+1;
 const lum=c=>{const v=c.match(/[\d.]+/g).slice(0,3).map(Number).map(x=>{x/=255;return x<=.03928?x/12.92:Math.pow((x+.055)/1.055,2.4)});return .2126*v[0]+.7152*v[1]+.0722*v[2]};
 const contraste=(a,b)=>{const [x,y]=[lum(a),lum(b)].sort((p,q)=>q-p);return (x+.05)/(y+.05)};
 const fundo=e=>{for(let x=e;x;x=x.parentElement){const c=getComputedStyle(x).backgroundColor;const m=c.match(/[\d.]+/g);if(m&&(m.length<4||+m[3]>.95))return c;}return 'rgb(255, 255, 255)'};
 const span=s.querySelector('span'),circ=span.getBoundingClientRect(),sr=s.getBoundingClientRect();
 const capFora=fig?[...fig.querySelectorAll('figcaption')].filter(c=>!d.contains(c)).map(c=>nt(c.textContent)).join(' '):'';
 const out={open:d.open,summary:visivel(s),alvo:[sr.width,sr.height],nome:s.getAttribute('aria-label'),so:s.innerHTML,
  dentro:!!d.parentElement.closest('a,button,label,figcaption,summary,[aria-hidden="true"]'),texto:nt(t.textContent),ligacoes:[...t.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')),
  externas:[...t.querySelectorAll('a[href^="http"]')].map(a=>({rel:a.getAttribute('rel'),ext:a.hasAttribute('data-external'),rot:a.getAttribute('aria-label'),href:a.getAttribute('href')})),
  src:fig&&fig.querySelector('img')?fig.querySelector('img').getAttribute('src'):null,legenda:capFora,aviso:yt?nt(yt.querySelector('.yt-cred').textContent):null,
  lado:document.documentElement.scrollWidth-innerWidth,circuloTapa:fora.filter(b=>cruza(circ,b)).map(b=>b.t),cIcone:contraste(getComputedStyle(span).color,getComputedStyle(span).backgroundColor)};
 if(d.open){out.textoVisivel=visivel(t);const r=t.getBoundingClientRect();
  const linhas=[];const w2=document.createTreeWalker(t,NodeFilter.SHOW_TEXT);let m;while(m=w2.nextNode()){if(!m.data.trim())continue;const rr=document.createRange();rr.selectNodeContents(m);for(const q of rr.getClientRects())if(q.width>2)linhas.push(q);}
  out.textoTapa=[...new Set(linhas.flatMap(q=>fora.filter(b=>cruza(q,b)).map(b=>b.t)))];
  out.tapado=linhas.filter(q=>{const x=q.left+Math.min(q.width/2,8),y=q.top+q.height/2;if(y<r.top||y>r.bottom||y<0||y>innerHeight)return false;const e=document.elementFromPoint(x,y);return !e||!(t.contains(e)||e===t);}).length;
  out.foraDoEcra=r.left<-1||r.right>innerWidth+1;out.rola=t.scrollHeight>t.clientHeight+1?getComputedStyle(t).overflowY:'nao';out.cTexto=contraste(getComputedStyle(t).color,fundo(t));}
 return out;}
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});let n=0;
 try{for(const tema of ['light','dark'])for(const width of [320,390,768,1280]){
  const ctx=await browser.newContext({viewport:{width,height:width<500?740:900},colorScheme:tema});
  await ctx.route('https://pedrohfernandes-klk.github.io/lente/**',async route=>{const u=new URL(route.request().url());const response=await ctx.request.get(origin+u.pathname+u.search);await route.fulfill({response});});
  await ctx.route(/fonts\.(googleapis|gstatic)\.com|youtube/,r=>r.abort());
  for(const pg of PAGINAS){
   const page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(origin+'/lente/'+pg.p,{waitUntil:'networkidle'});await page.evaluate(()=>{try{localStorage.clear()}catch(e){}});await page.reload({waitUntil:'networkidle'});
   const bank=pg.motor==='antigo'?banco(pg.p,'itens:'):pg.motor==='licoes'?banco(pg.p,pg.chave):null;let cartao=0;
   for(const parada of pg.paradas){
    if(pg.motor==='antigo'){await motorAntigo(page,bank,cartao,parada.cartao);cartao=parada.cartao;}
    if(pg.motor==='licoes'){await motorLicoes(page,bank,cartao,parada.cartao);cartao=parada.cartao;}
    if(pg.motor==='c10'&&parada.passo){await page.click('[data-start]');await page.click(`a[href="#momento-${parada.passo}"][data-stage-link]`);}
    await page.waitForTimeout(300);
    const sel='details.info-i[name="info-i"]';
    const vistos=await page.locator(sel).evaluateAll(ds=>ds.filter(d=>d.querySelector('summary').getClientRects().length>0).length);
    assert.equal(vistos,parada.is.length,`${width} ${tema} /${pg.p} (${cartao}): número de «i» à vista`);
    for(const [k,tipo] of parada.is.entries()){
     const rot=`${width} px, ${tema}, /${pg.p} (cartão ${cartao}) «i» ${k+1}`;
     const d=page.locator(sel).filter({has:page.locator('summary:visible')}).nth(k),s=d.locator('summary');
     await s.scrollIntoViewIfNeeded();let m=await page.evaluate(medir,k);
     assert.equal(m.open,false,rot+': fechado ao carregar');assert.ok(m.summary,rot+': «i» à vista');assert.ok(m.alvo[0]>=44&&m.alvo[1]>=44,rot+': alvo de 44 px');
     assert.match(m.nome,/^Créditos d/,rot);assert.equal(m.so,'<span aria-hidden="true">i</span>',rot);assert.equal(m.dentro,false,rot+': fora de ligação, legenda ou parte decorativa');
     assert.ok(m.cIcone>=4.5,rot+': a letra do «i» lê-se ('+m.cIcone.toFixed(2)+')');
     // o crédito de antes, palavra a palavra, e as mesmas ligações (a da licença CC pode ter-se juntado)
     if(tipo==='desenho'){const velho=antigo(pg.p+'index.html');assert.ok(velho.includes('<figcaption>'+m.legenda+' <span class="cred">'+m.texto+'</span></figcaption>'),rot+': crédito e legenda do desenho');}
     else if(tipo==='fig'){const v=legendaAntiga(pg.p,m.src);assert.equal(m.texto,v.texto,rot+': crédito completo');assert.ok(!m.legenda||v.texto.startsWith(m.legenda),rot+': à vista, só o que diz o que se vê');
      assert.deepEqual(m.ligacoes.filter(h=>!h.includes('creativecommons.org')),v.ligacoes.filter(h=>!h.includes('creativecommons.org')),rot+': mesmas ligações');assert.ok(v.ligacoes.every(h=>m.ligacoes.includes(h)),rot);}
     else if(tipo==='par'){const velho=antigo(pg.p+'index.html');const cap=norm(velho.match(/<figure class="c10-par">[\s\S]*?<figcaption>([\s\S]*?)<\/figcaption>/)[1]);assert.equal(m.texto+' '+m.legenda,cap,rot+': crédito completo e aviso à vista');}
     else if(tipo==='video'){const velho=antigo(pg.p+'index.html');const cap=norm(velho.match(/<p class="yt-cred">([\s\S]*?)<\/p>/)[1]);assert.equal(m.texto+' '+m.aviso,cap,rot+': crédito do vídeo completo e aviso à vista');}
     else if(tipo==='m1'){const velho=antigo(pg.p+'index.html');const cap=norm(velho.match(/<figcaption>([\s\S]*?)<\/figcaption>/)[1]);for(const parte of cap.split(' · ').slice(0,-1).flatMap(x=>x.split(', ')))assert.ok(m.texto.includes(parte),rot+': '+parte);assert.ok(m.ligacoes.includes('imagens/'),rot);assert.equal(m.legenda,'',rot);}
     for(const a of m.externas)if(a.href.includes('creativecommons.org'))assert.equal(a.rel,'license',rot);else{assert.ok(a.ext,rot+': data-external');assert.match(a.rot||'',/, sítio externo$/,rot+': aria-label');}
     assert.deepEqual(m.circuloTapa,[],rot+': o «i» fechado não tapa texto');assert.ok(m.lado<=0,rot+': sem deslize para o lado');
     // clique abre e fecha
     // (aberto por baixo do «i», o crédito pode ficar sob a barra fixa do fundo do ecrã: rola-se até ele, como faria o aluno)
     await s.click();await d.locator('.info-i-texto').evaluate(e=>{const r=e.getBoundingClientRect();if(r.bottom>innerHeight-90||r.top<0)e.scrollIntoView({block:'center'})});
     m=await page.evaluate(medir,k);assert.ok(m.open&&m.textoVisivel,rot+': clique abre');
     assert.deepEqual(m.textoTapa,[],rot+': o crédito aberto não tapa texto');assert.equal(m.tapado,0,rot+': nada tapa o crédito');assert.equal(m.foraDoEcra,false,rot+': crédito dentro do ecrã');
     assert.ok(m.rola==='nao'||m.rola==='auto',rot+': crédito inteiro ou a rolar por dentro');assert.ok(m.lado<=0,rot+': aberto, sem deslize');assert.ok(m.cTexto>=4.5,rot+': o crédito lê-se ('+m.cTexto.toFixed(2)+')');
     await s.click();assert.equal(await d.evaluate(e=>e.open),false,rot+': clique fecha');
     // teclado: Enter abre, Escape fecha e devolve o foco ao «i»
     await s.focus();await page.keyboard.press('Enter');assert.equal(await d.evaluate(e=>e.open),true,rot+': Enter abre');
     assert.ok(await s.evaluate(e=>parseFloat(getComputedStyle(e).outlineWidth)>=2||e.matches(':focus-visible')),rot+': foco visível');
     await page.keyboard.press('Escape');assert.equal(await d.evaluate(e=>e.open),false,rot+': Escape fecha');assert.ok(await s.evaluate(e=>document.activeElement===e),rot+': o foco volta ao «i»');
     // um clique fora fecha
     await s.click();await page.mouse.click(2,Math.round((await page.viewportSize()).height/2));assert.equal(await d.evaluate(e=>e.open),false,rot+': clique fora fecha');
     n++;
    }
    if(parada.is.length>1){const ds=page.locator(sel).filter({has:page.locator('summary:visible')});await ds.nth(0).locator('summary').click();await ds.nth(1).locator('summary').click();
     assert.equal(await page.locator(sel+'[open]').count(),1,`${width} ${tema} /${pg.p}: um só «i» aberto`);await page.keyboard.press('Escape');}
    // impressão: o «i» não sai; o crédito sai por extenso sempre que sai a imagem, com o endereço da licença
    await page.emulateMedia({media:'print'});
    const imp=await page.evaluate(()=>{const v=e=>!!e&&e.getClientRects().length>0&&e.checkVisibility({visibilityProperty:true,contentVisibilityAuto:true});
     return [...document.querySelectorAll('details.info-i[name="info-i"]')].map(d=>{const box=d.closest('figure')||d.closest('.yt');const img=box&&box.querySelector('img,svg,.yt-abrir');
      return {texto:v(d.querySelector('.info-i-texto')),i:v(d.querySelector('summary')),imagem:img?v(img):true,licencas:[...d.querySelectorAll('a[rel~=license]')].map(a=>getComputedStyle(a,'::after').content.includes(a.getAttribute('href')))};});});
    imp.forEach((x,i)=>{const rot=`${width} ${tema} /${pg.p} «i» ${i+1}, impressão`;assert.equal(x.i,false,rot+': sem o botão «i»');assert.equal(x.texto,x.imagem,rot+': o crédito acompanha a imagem');assert.ok(x.licencas.every(Boolean),rot+': o endereço da licença');});
    await page.emulateMedia({media:'screen'});
   }
   assert.deepEqual(errors,[],pg.p);await page.close();
  }
  await ctx.close();
 }
 console.log('Créditos atrás do «i» (lente-2): '+n+' «i» abertos por clique e por teclado, a 320, 390, 768 e 1280 px, em claro e escuro, sem deslize, sem tapar texto e com impressão.');
 }finally{await browser.close();server.closeAllConnections();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
