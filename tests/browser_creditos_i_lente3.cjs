// 08/11/2026: decisões 153, 162 e 176 (pedido lente-3, famílias L14 a L19 do plano dos créditos). Uma amostra de cada família de
// «i» novos (portal da Cidadania, com as portas dos módulos e a imagem da página; passos do M1, congelados, e do M2, com cartões;
// cartões com span.fr-cred das narrativas, de «Como se investiga», da Ética e dos gigantes; vozes com vz-fig, Warhol e 25 de
// Abril; retratos de Butler e Singer, na variante «linha»; «Ler a cidade», num cartão com dois «i» e na gaveta de um lugar, com
// as miniaturas; e, fora da tabela, o passo 02 de «Como se investiga», com dois «i» no mesmo cartão, e o retrato de Oscar Wilde
// no passo 01 dos Direitos), a 320, 390, 768 e 1280 px, em claro e em escuro: a página não desliza para o lado; o «i» está fechado ao
// carregar, tem alvo de 44 px e o nome «Créditos…», sem nada da casa por cima (nem o «+» dos summary dos cartões); abre e fecha
// por clique, abre com Enter e fecha com Escape (o foco volta ao «i», e na gaveta o Escape só fecha o «i»); um clique fora fecha;
// aberto, leva o crédito de antes (o mesmo texto e as mesmas ligações; a da fonte com data-external e aria-label, a licença CC
// com rel="license"), cabe no ecrã, não tapa texto nem fica tapado, e lê-se (contraste de 4,5:1); na impressão, o «i» não sai e
// o crédito sai por extenso sempre que sai a imagem a que pertence, com o endereço da licença.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict'),{execFileSync}=require('child_process');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),BASE='fec58ae298fd44a9144799ebb8f007b92054720a';
const antigo=p=>execFileSync('git',['show',BASE+':'+p],{cwd:root,encoding:'utf8',maxBuffer:1<<28}).replace(/\\"/g,'"').replace(/<\\\//g,'</');
const ent=s=>String(s).replace(/&amp;/g,'&').replace(/&#x27;/g,"'").replace(/&quot;/g,'"');
const norm=s=>ent(String(s).replace(/<[^>]+>/g,'')).replace(/\s+/g,' ').trim();
const clean=s=>String(s||'').replace(/\*\*|_/g,'');
const hrefs=h=>[...String(h).matchAll(/href="([^"]+)"/g)].map(m=>m[1]);
// os cartões de uma página (JSON dentro do <script>)
function banco(pg,chave){const src=fs.readFileSync(path.join(root,pg,'index.html'),'utf8');let i=src.indexOf('[',src.indexOf(chave));let d=0,str=false,esc=false;
 for(let k=i;k<src.length;k++){const c=src[k];if(str){if(esc)esc=false;else if(c==='\\')esc=true;else if(c==='"')str=false;continue}if(c==='"')str=true;else if(c==='[')d++;else if(c===']'&&!--d)return JSON.parse(src.slice(i,k+1));}}
// O crédito de antes (main fec58ae), pela figura que tem o mesmo texto alternativo, conforme a família.
function creditoAntigo(pg,tipo,alt,porta){const s=antigo(pg+'index.html');
 if(tipo==='porta'){const linha=s.match(/<p class="cid-image-credits">([\s\S]*?)<\/p>/)[1];const a=[...linha.matchAll(/<a href="([^"]+)">([^<]+)<\/a>/g)].find(m=>m[2]===porta);assert.ok(a,porta);return {texto:'domínio público',ligacoes:[a[1]],contem:true};}
 const figs=[...s.replace(/data:image\/[a-z+]+;base64,[A-Za-z0-9+/=]+/g,'DATA').matchAll(/<figure\b[^>]*>[\s\S]*?<\/figure>/g)].map(m=>m[0]);
 const f=figs.find(x=>x.includes('alt="'+alt+'"')&&/fr-cred|fa-cred|<figcaption>[^]*?<a /.test(x));assert.ok(f,pg+': figura antiga «'+alt.slice(0,40)+'»');
 const cap=(f.match(/<figcaption>([\s\S]*?)<\/figcaption>/)||[])[1]||'';
 if(tipo==='fr'){const c=f.match(/<span class="fr-cred">([\s\S]*?)<\/span>/)[1];return {texto:norm(c).replace(', 1610-1613 (fotografia de.','.'),ligacoes:hrefs(c)};}
 if(tipo==='fa'){const c=f.match(/<span class="fa-cred">([\s\S]*?)<\/span>/)[1];return {texto:norm(c),ligacoes:hrefs(c)};}
 if(tipo==='cid'){const b=norm(cap).match(/([^.]*(?:\.(?! )[^.]*)*\. (?:Domínio público|Licença CC BY-SA 3\.0)[^]* no registo de origem \(Wikimedia Commons\), consulta de [\d/-]+\.)$/);assert.ok(b,cap.slice(-120));return {texto:b[1],ligacoes:hrefs(cap),contem:true,fim:true};}
 if(tipo==='vz')return {texto:norm(cap).replace(/\.?$/,''),ligacoes:hrefs(cap),contem:true,comeco:true};
 if(tipo==='pessoa')return {texto:norm(cap).replace(/ · /g,' '),ligacoes:hrefs(cap),palavras:true};
 throw Error(tipo);}
const PAGINAS=[
 {p:'cidadania/',motor:'nenhum',paradas:[{is:['porta','porta','porta','cid'],portas:['Frans Hals','Joseph Racknitz','Honoré Daumier']}]},
 {p:'cidadania/m1/passo-01/',motor:'antigo',paradas:[{cartao:1,is:['cid']}]},
 {p:'cidadania/m2/passo-03/',motor:'antigo',paradas:[{cartao:1,is:['cid']}]},
 {p:'narrativas/anguissola/',motor:'antigo',paradas:[{cartao:1,is:['fr']}]},
 {p:'investigar/',motor:'nenhum',sel:'figure details.info-i',paradas:[{is:['fr']}]},
 {p:'investigar/passo-02/',motor:'antigo',paradas:[{cartao:1,is:['cid','cid']}]},
 {p:'etica/',motor:'antigo',paradas:[{cartao:0,is:['fr']}]},
 {p:'gigantes/darwin/',motor:'antigo',paradas:[{cartao:0,is:['fr']}]},
 {p:'vozes/warhol/',motor:'antigo',paradas:[{cartao:0,is:['vz']}]},
 {p:'cidadania/m1/cid-m1-butler-singer/',motor:'antigo',paradas:[{cartao:1,is:['pessoa']}]},
 {p:'cidadania/25-de-abril/',motor:'antigo',paradas:[{cartao:1,is:['vz']}]},
 {p:'direitos/passo-01/',motor:'antigo',paradas:[{cartao:12,is:['vz']}]},
 {p:'cidade/m04/',motor:'antigo',paradas:[{cartao:0,is:['fa','fa']}]},
 {p:'cidade/',hash:'#lugar-epi',motor:'nenhum',sel:'#gaveta details.info-i',paradas:[{is:['fa','fa','fa','fa','fa','fa','fa'],testar:[0,5]}]},
];
const server=http.createServer((req,res)=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname).replace(/^\/lente/,''));if(!f.startsWith(root+path.sep)&&f!==root){res.writeHead(403);return res.end();}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.webp':'image/webp','.jpg':'image/jpeg','.png':'image/png'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});
// As fotografias de «Ler a cidade» vivem no sítio do Português (/pt/img/arquivo/): sem rede, uma fotografia do Lente faz de conta.
const SUBSTITUTA=fs.readFileSync(path.join(root,'img/arquivo/rua-da-boavista-tres-predios-2026.jpg'));
// Motor dos cartões (EPIJogo.montar): responde certo até ao cartão «alvo» (contado a partir de 0), como no pedido lente-2.
async function motorAntigo(p,bank,de,alvo){
 for(let i=de;i<alvo;i++){
  await p.locator('#baralho .cartao').first().waitFor();
  const n=s=>clean(String(s||'').replace(/<[^>]+>/g,' ')).replace(/\s+/g,' ').trim();
  const visto=n(await p.locator('#baralho').innerText());const cand=bank.filter(x=>x.t!=='ler'&&[x.p,x.p2].some(q=>q&&visto.includes(n(q))));
  const x=bank[i].t==='ler'?bank[i]:(cand.length===1?cand[0]:bank[i]);
  if(x.t==='ler'){await p.locator('[data-c-acoes] [data-seguinte]').click();continue}
  if(x.t==='escolha')await p.locator('#baralho .ops button.op').filter({hasText:clean(x.o[x.c])}).first().click();
  else if(x.t==='vf')await p.locator('#baralho .ops button.op').filter({hasText:x.v?'Verdadeiro':'Falso'}).click();
  else throw Error('tipo sem resposta: '+x.t);
  await p.locator('[data-c-folha]:not([hidden]) [data-seguinte]').click();
 }
}
// Medidas dentro da página: o n-ésimo «i» à vista (dentro do seletor da página), aberto ou fechado.
function medir([sel,n]){
 const visivel=e=>!!e&&e.getClientRects().length>0&&e.checkVisibility({visibilityProperty:true,contentVisibilityAuto:true});
 const d=[...document.querySelectorAll(sel)].filter(x=>visivel(x.querySelector('summary')))[n];
 const s=d.querySelector('summary'),t=d.querySelector('.info-i-texto'),caixa=d.closest('figure')||d.closest('.cid-porta');
 const nt=x=>x.replace(/\s+/g,' ').trim();
 const fora=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let no;while(no=w.nextNode()){const el=no.parentElement;if(!no.data.trim()||d.contains(el)||el.closest('[aria-hidden="true"],script,style,.c-sr,.c10-sr,.salta,.sr-only,.foto-arq.mini figcaption')||!visivel(el))continue;const r=document.createRange();r.selectNodeContents(no);for(const q of r.getClientRects())if(q.width>1&&q.height>1)fora.push({x:q.left,y:q.top,r:q.right,b:q.bottom,t:no.data.trim().slice(0,40)});}
 const cruza=(a,b)=>a.left<b.r-1&&a.right>b.x+1&&a.top<b.b-1&&a.bottom>b.y+1;
 const lum=c=>{const v=c.match(/[\d.]+/g).slice(0,3).map(Number).map(x=>{x/=255;return x<=.03928?x/12.92:Math.pow((x+.055)/1.055,2.4)});return .2126*v[0]+.7152*v[1]+.0722*v[2]};
 const contraste=(a,b)=>{const [x,y]=[lum(a),lum(b)].sort((p,q)=>q-p);return (x+.05)/(y+.05)};
 const fundo=e=>{for(let x=e;x;x=x.parentElement){const c=getComputedStyle(x).backgroundColor;const m=c.match(/[\d.]+/g);if(m&&(m.length<4||+m[3]>.95))return c;}return 'rgb(255, 255, 255)'};
 const span=s.querySelector('span'),circ=span.getBoundingClientRect(),sr=s.getBoundingClientRect();
 const img=caixa&&caixa.querySelector('img');
 const out={open:d.open,summary:visivel(s),alvo:[sr.width,sr.height],nome:s.getAttribute('aria-label'),so:s.innerHTML,linha:d.classList.contains('info-i--linha'),
  antes:getComputedStyle(s,'::before').content,depois:getComputedStyle(s,'::after').content,
  dentro:!!d.parentElement.closest('a,button,label,figcaption,summary,[aria-hidden="true"]'),texto:nt(t.textContent),html:t.innerHTML,ligacoes:[...t.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')),
  externas:[...t.querySelectorAll('a[href^="http"]')].map(a=>({rel:a.getAttribute('rel'),ext:a.hasAttribute('data-external'),rot:a.getAttribute('aria-label'),href:a.getAttribute('href'),txt:nt(a.textContent)})),
  alt:img?img.getAttribute('alt'):null,
  lado:document.documentElement.scrollWidth-innerWidth,circuloTapa:fora.filter(b=>cruza(circ,b)).map(b=>b.t),cIcone:contraste(getComputedStyle(span).color,getComputedStyle(span).backgroundColor)};
 if(img&&!out.linha){const ir=img.getBoundingClientRect();out.noCanto=sr.right<=ir.right+1&&sr.bottom<=ir.bottom+1&&sr.left>=ir.left-1&&sr.top>=ir.top-1;}
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
  await ctx.route('https://pedrohfernandes-klk.github.io/**',async route=>{const u=new URL(route.request().url());
   if(u.pathname.startsWith('/pt/'))return route.fulfill({status:200,contentType:'image/jpeg',body:SUBSTITUTA});
   const response=await ctx.request.get(origin+u.pathname+u.search);await route.fulfill({response});});
  await ctx.route(/fonts\.(googleapis|gstatic)\.com|youtube/,r=>r.abort());
  for(const pg of PAGINAS){
   const page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(origin+'/lente/'+pg.p,{waitUntil:'networkidle'});await page.evaluate(()=>{try{localStorage.clear()}catch(e){}});
   await page.goto(origin+'/lente/'+pg.p+(pg.hash||''),{waitUntil:'networkidle'});if(pg.hash)await page.reload({waitUntil:'networkidle'});
   const bank=pg.motor==='antigo'?banco(pg.p,'itens:'):null;let cartao=0;const sel=pg.sel||'details.info-i[name="info-i"]';
   for(const parada of pg.paradas){
    if(pg.motor==='antigo'){await motorAntigo(page,bank,cartao,parada.cartao);cartao=parada.cartao;}
    await page.waitForTimeout(300);
    // as imagens carregadas (as «lazy» também), para medir o «i» no canto delas
    await page.evaluate(async s=>{for(const d of document.querySelectorAll(s)){const f=d.closest('figure,.cid-porta');const im=f&&f.querySelector('img');if(im){im.loading='eager';if(!im.complete)await new Promise(r=>{im.onload=im.onerror=r;setTimeout(r,3000)});}}},sel);
    const vistos=await page.locator(sel).evaluateAll(ds=>ds.filter(d=>d.querySelector('summary').getClientRects().length>0&&d.querySelector('summary').checkVisibility()).length);
    assert.equal(vistos,parada.is.length,`${width} ${tema} /${pg.p} (${cartao}): número de «i» à vista`);
    for(const [k,tipo] of parada.is.entries()){
     if(parada.testar&&!parada.testar.includes(k))continue;
     const rot=`${width} px, ${tema}, /${pg.p} (cartão ${cartao}) «i» ${k+1}`;
     const d=page.locator(sel).filter({has:page.locator('summary:visible')}).nth(k),s=d.locator('summary');
     await s.scrollIntoViewIfNeeded();let m=await page.evaluate(medir,[sel,k]);
     assert.equal(m.open,false,rot+': fechado ao carregar');assert.ok(m.summary,rot+': «i» à vista');assert.ok(m.alvo[0]>=44&&m.alvo[1]>=44,rot+': alvo de 44 px');
     assert.match(m.nome,/^Créditos d/,rot);assert.equal(m.so,'<span aria-hidden="true">i</span>',rot);assert.equal(m.dentro,false,rot+': fora de ligação, legenda ou parte decorativa');
     assert.ok(['none','normal'].includes(m.antes)&&['none','normal'].includes(m.depois),rot+': nada da casa no «i» ('+m.antes+')');
     assert.ok(m.cIcone>=4.5,rot+': a letra do «i» lê-se ('+m.cIcone.toFixed(2)+')');
     if(m.noCanto!==undefined)assert.ok(m.noCanto,rot+': o «i» no canto da imagem');
     // o crédito de antes: o mesmo texto e as mesmas ligações (a da licença CC pode ter-se juntado)
     const v=creditoAntigo(pg.p,tipo,m.alt,parada.portas&&parada.portas[k]);
     const t1=m.texto.toLowerCase(),t0=v.texto.toLowerCase();
     if(v.palavras)assert.deepEqual(m.texto.replace(/[.,]/g,'').split(' ').sort(),v.texto.replace(/[.,]/g,'').split(' ').sort(),rot+': crédito completo');
     else if(v.fim)assert.ok(t1.endsWith(t0.slice(1))&&t1.length>t0.length,rot+': crédito completo ('+m.texto+')');
     else if(v.comeco)assert.ok(t1.startsWith(t0),rot+': crédito completo ('+m.texto+')');
     else if(v.contem)assert.ok(t1.includes(t0),rot+': crédito completo ('+m.texto+')');
     else assert.equal(t1,t0,rot+': crédito completo');
     for(const h of v.ligacoes)assert.ok(m.ligacoes.includes(h),rot+': ligação '+h);
     const fonte=hs=>[...new Set(hs.filter(h=>!h.includes('creativecommons.org')))].sort();
     assert.deepEqual(fonte(m.ligacoes),fonte(v.ligacoes),rot+': as mesmas ligações para a fonte');
     for(const lic of (m.texto.match(/CC BY(?:-SA)? \d\.\d/g)||[]))assert.ok(m.externas.some(a=>a.rel==='license'&&a.txt===lic),rot+': ligação da licença '+lic);
     for(const a of m.externas)if(a.href.includes('creativecommons.org'))assert.equal(a.rel,'license',rot);else{assert.ok(a.ext,rot+': data-external');assert.match(a.rot||'',/, sítio externo$/,rot+': aria-label');assert.ok((a.rot||'').startsWith(a.txt),rot+': o nome acessível começa pelo texto da ligação');}
     assert.deepEqual(m.circuloTapa,[],rot+': o «i» fechado não tapa texto');assert.ok(m.lado<=0,rot+': sem deslize para o lado');
     // clique abre e fecha (aberto por baixo do «i», o crédito pode ficar sob a barra fixa do fundo do ecrã: rola-se até ele)
     await s.click();await d.locator('.info-i-texto').evaluate(e=>{const r=e.getBoundingClientRect();if(r.bottom>innerHeight-90||r.top<0)e.scrollIntoView({block:'center'})});
     m=await page.evaluate(medir,[sel,k]);assert.ok(m.open&&m.textoVisivel,rot+': clique abre');
     assert.deepEqual(m.textoTapa,[],rot+': o crédito aberto não tapa texto');assert.equal(m.tapado,0,rot+': nada tapa o crédito');assert.equal(m.foraDoEcra,false,rot+': crédito dentro do ecrã');
     assert.ok(m.rola==='nao'||m.rola==='auto',rot+': crédito inteiro ou a rolar por dentro');assert.ok(m.lado<=0,rot+': aberto, sem deslize');assert.ok(m.cTexto>=4.5,rot+': o crédito lê-se ('+m.cTexto.toFixed(2)+')');
     await s.click();assert.equal(await d.evaluate(e=>e.open),false,rot+': clique fecha');
     // teclado: Enter abre, Escape fecha e devolve o foco ao «i» (na gaveta de «Ler a cidade», a gaveta fica aberta)
     await s.focus();await page.keyboard.press('Enter');assert.equal(await d.evaluate(e=>e.open),true,rot+': Enter abre');
     assert.ok(await s.evaluate(e=>parseFloat(getComputedStyle(e).outlineWidth)>=2||e.matches(':focus-visible')),rot+': foco visível');
     await page.keyboard.press('Escape');assert.equal(await d.evaluate(e=>e.open),false,rot+': Escape fecha');assert.ok(await s.evaluate(e=>document.activeElement===e),rot+': o foco volta ao «i»');
     if(pg.hash)assert.ok(await page.evaluate(()=>document.querySelector('#gaveta').classList.contains('aberta')),rot+': o Escape não fecha a gaveta');
     // um clique fora fecha
     await s.click();await page.mouse.click(2,Math.round((await page.viewportSize()).height/2));assert.equal(await d.evaluate(e=>e.open),false,rot+': clique fora fecha');
     if(pg.hash)assert.ok(await page.evaluate(()=>document.querySelector('#gaveta').classList.contains('aberta')),rot+': a gaveta continua aberta');
     n++;
    }
    if(parada.is.length>1){const ds=page.locator(sel).filter({has:page.locator('summary:visible')});await ds.nth(0).locator('summary').click();await ds.nth(1).locator('summary').click();
     assert.equal(await page.locator(sel+'[open]').count(),1,`${width} ${tema} /${pg.p}: um só «i» aberto`);await page.keyboard.press('Escape');}
    // impressão: o «i» não sai; o crédito sai por extenso sempre que sai a imagem, com o endereço da licença
    await page.emulateMedia({media:'print'});
    const imp=await page.evaluate(s=>{const v=e=>!!e&&e.getClientRects().length>0&&e.checkVisibility({visibilityProperty:true,contentVisibilityAuto:true});
     return [...document.querySelectorAll(s)].map(d=>{const box=d.closest('figure')||d.closest('.cid-porta');const img=box&&box.querySelector('img');
      return {texto:v(d.querySelector('.info-i-texto')),i:v(d.querySelector('summary')),imagem:img?v(img):true,licencas:[...d.querySelectorAll('a[rel~=license]')].map(a=>getComputedStyle(a,'::after').content.includes(a.getAttribute('href')))};});},sel);
    imp.forEach((x,i)=>{const rot=`${width} ${tema} /${pg.p} «i» ${i+1}, impressão`;assert.equal(x.i,false,rot+': sem o botão «i»');assert.equal(x.texto,x.imagem,rot+': o crédito acompanha a imagem');assert.ok(x.licencas.every(Boolean),rot+': o endereço da licença');});
    await page.emulateMedia({media:'screen'});
   }
   assert.deepEqual(errors,[],pg.p);await page.close();
  }
  await ctx.close();
 }
 console.log('Créditos atrás do «i» (lente-3): '+n+' «i» abertos por clique e por teclado, a 320, 390, 768 e 1280 px, em claro e escuro, sem deslize, sem tapar texto e com impressão.');
 }finally{await browser.close();server.closeAllConnections();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
