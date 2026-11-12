// 07/11/2026: decisões 153, 176 e 177 (pedido lente-1). Cada «i» novo das entradas do Lente (fundo, portas e porta do Português
// na entrada, colagem do «Ideias», créditos das portas do Laboratório e fotografia nas letras do cabeçalho) abre por teclado e por
// toque a 390 e a 1366 px; o crédito aberto é o de antes, palavra a palavra e com as mesmas ligações; nada tapa o texto, a página
// não rola para o lado, e na impressão o crédito sai por extenso sempre que sai a imagem a que pertence.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict'),{execFileSync}=require('child_process');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),BASE='dc01487';
const antigo=p=>execFileSync('git',['show',BASE+':'+p],{cwd:root,encoding:'utf8'});
const um=(s,re)=>{const m=s.match(re);assert.ok(m,String(re));return m[1];};
const LETRAS=['apresentar/','biblioteca/','cidadania/m1/percurso-anterior.html','cidadania/m2/','cidade/','direitos/','gigantes/','investigar/','ler/','projetos/','sidequests/'];
const ficheiro=p=>p.endsWith('/')?p+'index.html':p;
// 08/11/2026: decisões 153, 162 e 176 (pedido lente-3). Nas entradas de «Como se investiga», dos projetos e das sidequests, a imagem
// do topo também passou a ter o seu «i» (o crédito que estava no span.fr-cred; confere-se em tests/browser_creditos_i_lente3.cjs e
// tests/test_creditos_i_lente3.py). Esse «i» vem depois do das letras: conta-se no número de «i» da página e, na impressão, o seu
// crédito tem de acompanhar a imagem do topo, como os outros; o «i» das letras confere-se aqui como antes.
const LENTE3={'investigar/':['figure.fig-rev img'],'projetos/':['figure.fig-rev img'],'sidequests/':['figure.fig-rev img']};
// 08/11/2026: decisões 153 e 176 (pedido lente-4). Em «Ler a cidade», os dez cartões das missões com crédito passaram a ter o seu «i»
// (fora da ligação, num div.missao-i; confere-se em tests/browser_creditos_i_lente4.cjs e tests/test_creditos_i_lente4.py). Esses «i»
// vêm depois do das letras: contam-se no número de «i» da página e, na impressão, o crédito de cada um tem de acompanhar a imagem do
// seu cartão; o «i» das letras confere-se aqui como antes.
const LENTE4={'cidade/':['m01','m02','m04','m06','m08','m10','m11','m12','m15','m16'].map(m=>`.missao[data-id="${m}"] .mf img`)};
// Para cada página: os «i» novos, pela ordem da página, com o crédito antigo (HTML) e a imagem a que pertence.
const PAGINAS=[
 {p:'',is:(()=>{const s=antigo('index.html'),portas=[...s.matchAll(/<p class="m1-home-credit ld-credito cz-credit">(.*?)<\/p>/g)].map(m=>m[1]);assert.equal(portas.length,2);
  // 08/11/2026: pedido cidade-cartaz-lente. O cartão «Ler a cidade.» entra logo antes do do Português, com o seu «i» (crédito novo,
  // escrito aqui por extenso, tools/trocas/cidade-cartaz-lente-20261108.json): a entrada passa a ter cinco «i» e a imagem de cada
  // cartão diz-se pelo cartão; o «i» do Português continua com o crédito antigo.
  // 12/11/2026: pedido entrada-temas. A entrada abre por quatro temas: continua a ter cinco «i» (o do fundo e um por tema, na imagem
  // do cartão). O do fundo e o do esboço de Van Gogh (agora no tema 03) conservam o crédito antigo, palavra a palavra; os dos temas 01,
  // 02 e 04 são créditos novos, escritos aqui por extenso (tests/fixtures/entrada-temas-20261112.json). Os «i» do quadro de Wright of
  // Derby, da fotografia do Tejo e do retrato de Pessoa saíram com as suas imagens.
  const C=u=>'<a data-external aria-label="Wikimedia Commons, sítio externo" href="'+u+'">Wikimedia Commons</a>. Domínio público.';
  return [{html:um(s,/<p class="cz-credit lf-credito">(.*?) <button /),visual:'.lf-mesa'},
   {html:'Honoré Daumier, gravura do conjunto <i>Les gens de justice</i>. '+C('https://commons.wikimedia.org/wiki/File:Honor%C3%A9_Daumier_-_Les_gens_de_justice.jpg'),visual:'.tm-g>li:nth-child(1) .tm-img img'},
   {html:'O Turco, o autómato de xadrez de Wolfgang von Kempelen, numa gravura de Joseph Racknitz, 1789. '+C('https://commons.wikimedia.org/wiki/File:Racknitz_-_The_Turk_3.jpg'),visual:'.tm-g>li:nth-child(2) .tm-img img'},
   {html:portas[1],visual:'#inicio-narrativas .tm-img img'},
   {html:'Rua da Boavista, Lisboa. Fotografia: Arquivo da EPI, 2026.',visual:'.tm-g>li:nth-child(4) .tm-img img'}];})()},
 {p:'narrativas/ideias/',is:[{html:um(antigo('narrativas/ideias/index.html'),/<figure class="drawing">[\s\S]*?<figcaption>([\s\S]*?)<\/figcaption>/),visual:'.drawing svg'}]},
 {p:'narrativas/',is:[{html:um(antigo('narrativas/index.html'),/<p class="lab-creditos">([\s\S]*?)<\/p>/),visual:null}]},
 ...LETRAS.map(p=>({p,depois:(LENTE3[p]||[]).concat(LENTE4[p]||[]),is:[{html:'Fotografia nas letras: '+um(antigo(ficheiro(p)),/<small class="mr-cred">\/ nas letras: (.*?) · Arquivo da EPI<\/small>/)+'. Arquivo da EPI.',visual:'.marca-sec'}]})),
];
const server=http.createServer((req,res)=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname).replace(/^\/lente/,''));if(!f.startsWith(root+path.sep)&&f!==root){res.writeHead(403);return res.end();}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.webp':'image/webp','.jpg':'image/jpeg'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});
// Medidas dentro da página: o «i» n, aberto ou fechado.
function medir([n,htmlAntigo]){
 const d=document.querySelectorAll('details.info-i[name="info-i"]')[n],s=d.querySelector('summary'),t=d.querySelector('.info-i-texto');
 const norm=x=>x.replace(/\s+/g,' ').trim(),tpl=document.createElement('template');tpl.innerHTML=htmlAntigo;
 // (checkVisibility: o conteúdo de um «i» fechado conserva as caixas de quando esteve aberto, mas não se vê)
 const visivel=e=>e.getClientRects().length>0&&e.checkVisibility({visibilityProperty:true,contentVisibilityAuto:true});
 // texto à vista fora deste «i» (sem o que é decorativo)
 const fora=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let no;while(no=w.nextNode()){const el=no.parentElement;if(!no.data.trim()||d.contains(el)||el.closest('[aria-hidden="true"],script,style,.c-sr,.salta,.sr-only')||!visivel(el))continue;const r=document.createRange();r.selectNodeContents(no);for(const q of r.getClientRects())if(q.width>1&&q.height>1)fora.push({x:q.left,y:q.top,r:q.right,b:q.bottom,t:no.data.trim().slice(0,40)});}
 const cruza=(a,b)=>a.left<b.r-1&&a.right>b.x+1&&a.top<b.b-1&&a.bottom>b.y+1;
 const circ=s.querySelector('span').getBoundingClientRect();
 const out={open:d.open,summary:visivel(s),alvo:[s.getBoundingClientRect().width,s.getBoundingClientRect().height],nome:s.getAttribute('aria-label'),dentroLigacao:!!d.closest('a,button,label,figcaption,[aria-hidden="true"]'),
  texto:norm(t.textContent),esperado:norm(tpl.content.textContent),ligacoes:[...t.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')),ligacoesAntes:[...tpl.content.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')),
  lado:document.documentElement.scrollWidth-innerWidth,circuloTapa:s.getClientRects().length?fora.filter(b=>cruza(circ,b)).map(b=>b.t):[]};
 if(d.open){out.textoVisivel=visivel(t);const r=t.getBoundingClientRect();
  // cada linha do crédito aberto está por cima (nada a tapa) e cabe no ecrã
  const linhas=[];const w2=document.createTreeWalker(t,NodeFilter.SHOW_TEXT);let m;while(m=w2.nextNode()){if(!m.data.trim())continue;const rr=document.createRange();rr.selectNodeContents(m);for(const q of rr.getClientRects())if(q.width>2)linhas.push(q);}
  // nenhuma linha do crédito aberto cruza texto de fora do «i»
  out.textoTapa=[...new Set(linhas.flatMap(q=>fora.filter(b=>cruza(q,b)).map(b=>b.t)))];
  // (as linhas que só se veem ao rolar o crédito por dentro não se medem aqui)
  out.tapado=linhas.filter(q=>{const x=q.left+Math.min(q.width/2,8),y=q.top+q.height/2;if(y<r.top||y>r.bottom||y<0||y>innerHeight)return false;const e=document.elementFromPoint(x,y);return !e||!(t.contains(e)||e===t);}).length;
  out.foraDoEcra=r.left<-1||r.right>innerWidth+1;out.rola=t.scrollHeight>t.clientHeight+1?getComputedStyle(t).overflowY:'nao';}
 return out;}
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});let n=0;
 try{for(const width of [390,1366]){
  const ctx=await browser.newContext({viewport:{width,height:900},hasTouch:true});
  await ctx.route('https://pedrohfernandes-klk.github.io/lente/**',async route=>{const u=new URL(route.request().url());const response=await ctx.request.get(origin+u.pathname+u.search);await route.fulfill({response});});
  await ctx.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
  for(const pg of PAGINAS){
   const page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(origin+'/lente/'+pg.p,{waitUntil:'networkidle'});
   const sel='details.info-i[name="info-i"]',todos=page.locator(sel);
   assert.equal(await todos.count(),pg.is.length+(pg.depois||[]).length,pg.p+': número de «i»');
   for(const [k,info] of pg.is.entries()){
    const rot=`${width} px, /${pg.p} «i» ${k+1}`,d=todos.nth(k),s=d.locator('summary');
    // abaixo de 640 px a porta dobrada não mostra a imagem: abre-se a porta, como faria o aluno
    if(!(await s.isVisible())){const fold=d.locator('xpath=ancestor::article[contains(@class,"ld")]//details[contains(@class,"cz-fold")]/summary');if(await fold.count())await fold.first().click();}
    await s.scrollIntoViewIfNeeded();
    let m=await page.evaluate(medir,[k,info.html]);
    assert.equal(m.open,false,rot+': fechado ao carregar');assert.ok(m.summary,rot+': «i» à vista');assert.ok(m.alvo[0]>=44&&m.alvo[1]>=44,rot+': alvo de 44 px');
    assert.match(m.nome,/^Créditos /,rot);assert.equal(m.dentroLigacao,false,rot+': fora de ligação, legenda ou parte decorativa');
    assert.equal(m.texto,m.esperado,rot+': crédito completo');assert.deepEqual(m.ligacoes,m.ligacoesAntes,rot+': mesmas ligações');
    assert.deepEqual(m.circuloTapa,[],rot+': o «i» fechado não tapa texto');assert.ok(m.lado<=0,rot+': sem deslocamento para o lado');
    // teclado: Enter abre, Escape fecha e devolve o foco ao «i», Espaço abre
    await s.focus();await page.keyboard.press('Enter');m=await page.evaluate(medir,[k,info.html]);
    assert.ok(m.open&&m.textoVisivel,rot+': Enter abre');assert.deepEqual(m.textoTapa,[],rot+': o crédito aberto não tapa texto');assert.equal(m.tapado,0,rot+': nada tapa o crédito');
    assert.equal(m.foraDoEcra,false,rot+': crédito dentro do ecrã');assert.ok(m.rola==='nao'||m.rola==='auto',rot+': crédito inteiro ou a rolar por dentro');assert.ok(m.lado<=0,rot+': aberto, sem deslocamento para o lado');
    await page.keyboard.press('Escape');assert.equal(await d.evaluate(e=>e.open),false,rot+': Escape fecha');assert.ok(await s.evaluate(e=>document.activeElement===e),rot+': o foco volta ao «i»');
    await page.keyboard.press(' ');assert.equal(await d.evaluate(e=>e.open),true,rot+': Espaço abre');await page.keyboard.press('Escape');
    // toque: abre e fecha
    await s.tap();m=await page.evaluate(medir,[k,info.html]);assert.ok(m.open&&m.textoVisivel,rot+': toque abre');assert.deepEqual(m.textoTapa,[],rot+': aberto ao toque, não tapa texto');assert.ok(m.lado<=0,rot);
    await s.tap();assert.equal(await d.evaluate(e=>e.open),false,rot+': toque fecha');n++;
   }
   if(pg.p===''){
    // um só aberto de cada vez; o botão de parar fica fora do «i» e não fica tapado com o «i» aberto
    const visiveis=[];for(let k=0;k<pg.is.length;k++)if(await todos.nth(k).locator('summary').isVisible())visiveis.push(k);
    await todos.nth(visiveis[0]).locator('summary').click();await todos.nth(visiveis[1]).locator('summary').click();
    assert.deepEqual(await page.locator(sel).evaluateAll(es=>es.map(e=>e.open)).then(a=>a.filter(Boolean).length),1,width+': um só «i» aberto');
    await page.mouse.click(2,2);assert.equal(await page.locator('details.info-i[open]').count(),0,width+': clique fora fecha');
    const b=page.locator('[data-fundo-botao="lf"]');assert.equal(await b.evaluate(e=>!!e.closest('details')),false,'botão fora do «i»');
    if(await b.isVisible()){await todos.first().locator('summary').click();assert.ok(await b.evaluate(e=>{const r=e.getBoundingClientRect();return e.contains(document.elementFromPoint(r.left+r.width/2,r.top+r.height/2));}),width+': botão de parar à vista e livre com o «i» aberto');await page.keyboard.press('Escape');}
   }
   // impressão: o «i» não sai; o crédito sai por extenso sempre que sai a imagem a que pertence
   await page.emulateMedia({media:'print'});
   const imp=await page.evaluate(vis=>{const ds=[...document.querySelectorAll('details.info-i[name="info-i"]')];const v=e=>!!e&&e.getClientRects().length>0&&e.checkVisibility({visibilityProperty:true,contentVisibilityAuto:true});
    return ds.map((d,i)=>({texto:v(d.querySelector('.info-i-texto')),i:v(d.querySelector('summary')),imagem:vis[i]?v(document.querySelector(vis[i])):true}));},pg.is.map(x=>x.visual).concat(pg.depois||[]));
   imp.forEach((x,i)=>{const rot=`${width} px, /${pg.p} «i» ${i+1}, impressão`;assert.equal(x.i,false,rot+': sem o botão «i»');assert.equal(x.texto,x.imagem,rot+': o crédito acompanha a imagem');});
   await page.emulateMedia({media:'screen'});assert.deepEqual(errors,[]);await page.close();
  }
  await ctx.close();
 }
 console.log('Créditos atrás do «i»: '+n+' «i» abertos por teclado e por toque, sem tapar texto, sem deslocamento e com impressão.');
 }finally{await browser.close();server.closeAllConnections();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
