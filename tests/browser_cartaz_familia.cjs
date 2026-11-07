// 01/11/2026: contratos das famílias migradas em navegador real.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..');
const lab=fs.existsSync(path.join(root,'assets/laboratorio/cartaz.js'));
const entry=fs.readFileSync(path.join(root,'index.html'),'utf8').includes('data-cartaz-entrada');
const pages=[...(entry?['']:[]),...(lab?['narrativas/','narrativas/ver/','narrativas/treinar/','narrativas/criar/']:[])];
const server=http.createServer((req,res)=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname).replace(/^\/lente/,''));if(!f.startsWith(root+path.sep)&&f!==root){res.writeHead(403);return res.end();}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
// 02/11/2026: inclui o limite largo apontado na confirmação, sem retirar larguras anteriores.
try{for(const theme of ['light','dark'])for(const width of [320,390,1024,1366,1440])for(const pagePath of pages){
 const ctx=await browser.newContext({viewport:{width,height:900},colorScheme:theme});const page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.route('https://pedrohfernandes-klk.github.io/lente/**',async route=>{const u=new URL(route.request().url());const response=await ctx.request.get(origin+u.pathname+u.search);await route.fulfill({response});});
 await page.goto(origin+'/lente/'+pagePath,{waitUntil:'networkidle'});
 // 01/11/2026: 320 e 1024 px, títulos sem transbordo e retoma completa.
 // 02/11/2026: decisões 131 e 134 (docente). Nem a entrada do Lente nem as entradas do Laboratório têm a caixa «A seguir».
 assert.deepEqual(errors,[]);assert.equal(await page.locator('.cz-next').count(),0);
 assert.equal(await page.evaluate(()=>Math.max(0,document.documentElement.scrollWidth-innerWidth)),0,pagePath);
 for(const sel of ['.cz-next .cz-button','.cz-fold>summary'])for(const box of await page.locator(sel).all()){const r=await box.boundingBox();assert.ok(r.height>=(sel.includes('summary')?88:48),`${pagePath} ${sel}: ${r.height}`);}
 const clipped=await page.locator('.modulo h3').evaluateAll(es=>es.filter(e=>e.scrollWidth>e.clientWidth).map(e=>e.textContent));assert.deepEqual(clipped,[],'títulos dos percursos');
 if(entry&&pagePath===''&&width===390)assert.ok(await page.evaluate(()=>document.documentElement.scrollHeight)<3000,'entrada abaixo de 3000 px');
 // 05/11/2026: decisão 163 (menus do Laboratório). Já não há dobras no Laboratório: em vez de «a banda do próximo passo aberta»,
 // nenhuma dobra e todas as portas (na entrada) e todas as linhas (nas portas) à vista, uma exigência maior.
 if(pagePath.startsWith('narrativas/')){assert.equal(await page.locator('main details:not(.info-i)').count(),0,'sem dobras');const itens=page.locator(pagePath==='narrativas/'?'.porta3':'li[data-peca]');assert.ok(await itens.count()>=3,'portas ou linhas');for(const it of await itens.all())assert.ok(await it.isVisible(),'banda à vista');assert.equal(await page.locator('.cz-state,.etq').filter({hasText:/por fazer/i}).count(),0);}
 // 02/11/2026: regressões da confirmação, imagem sem caixa 3:2 e largura útil da legenda.
 if(pagePath==='narrativas/'&&width===390)assert.ok(await page.evaluate(()=>document.documentElement.scrollHeight)<3000,'Laboratório abaixo de 3000 px');
 if(pagePath.startsWith('narrativas/')&&width>=1024){
  const layout=await page.evaluate(()=>{const r=s=>document.querySelector(s).getBoundingClientRect();return {main:r('main').width,folds:[...document.querySelectorAll('.unidade.cz-fold')].map(e=>e.getBoundingClientRect().width)};});
  // 02/11/2026: decisão 134. Sem a caixa «A seguir», deixa de se medir a região ao lado da abertura; as dobras continuam à largura útil.
  for(const w of layout.folds)assert.ok(Math.abs(w-(layout.main-32))<=1,'dobras ocupam toda a largura útil');
  if(pagePath!=='narrativas/'){
   // 05/11/2026: decisão 163. A imagem da porta passa para a abertura (figure.lab-figura, com o «i» da decisão 153); as mesmas medidas.
   const museum=await page.locator('main .lab-abre .lab-figura').evaluate(e=>({height:e.getBoundingClientRect().height,caption:e.querySelector('figcaption').getBoundingClientRect().width,ratio:getComputedStyle(e.querySelector('img')).aspectRatio}));
   assert.ok(museum.caption>=240,JSON.stringify(museum));assert.ok(museum.height<=400,JSON.stringify(museum));assert.equal(museum.ratio,'auto');
  }
 }
 // 02/11/2026: decisão 34, tabela de museu colada à imagem também com a dobra; abaixo de 640 px, a porta dobrada não mostra imagem sem tabela.
 // 07/11/2026: decisões 153, 176 e 177, a tabela de museu colada à imagem dá lugar ao «i» da porta: dentro da caixa da imagem, a 8 px
 // do canto inferior direito, com alvo de 44 px, visível sempre que a imagem se vê (também com a dobra), fora da ligação e com o
 // crédito inteiro (autor, Wikimedia Commons e licença) dentro; abaixo de 640 px, a porta dobrada continua sem imagem.
 if(entry&&pagePath===''){const tabela=await page.locator('.lente-div .ld').evaluateAll(es=>es.map(d=>{const i=d.querySelector('.ld-moldura>.ld-img'),c=d.querySelector('.ld-moldura>details.info-i'),f=d.querySelector('details.cz-fold');if(!i||!c||c.closest('a'))return d.id+': «i» fora do sítio';const s=c.querySelector('summary'),t=c.querySelector('.info-i-texto').textContent;if(!/Wikimedia Commons\. Domínio público\.$/.test(t)||!c.querySelector('.info-i-texto a[href^="https://commons.wikimedia.org/"]'))return d.id+': crédito incompleto';const vi=getComputedStyle(i).display!=='none'&&i.getClientRects().length>0,vc=s.getClientRects().length>0&&getComputedStyle(s).visibility!=='hidden';if(vi!==vc)return d.id+': imagem sem «i»';if(vi){const a=i.getBoundingClientRect(),b=s.getBoundingClientRect();if(b.width<44||b.height<44)return d.id+': alvo pequeno';if(Math.abs(a.right-8-b.right)>1||Math.abs(a.bottom-8-b.bottom)>1)return d.id+': «i» longe do canto';}if(vi&&!f.open)return d.id+': porta dobrada com imagem';return null;}).filter(Boolean));assert.deepEqual(tabela,[],`${width} ${theme}`);}
 // 02/11/2026: D5, nada se dobra a partir de 640 px nem na projeção.
 const naoDobra=async rotulo=>{for(const [sel,acao] of [['#inicio-cidadania .ld-n','clique'],['#inicio-cidadania .cz-fold>summary','Enter'],['#ferr-ler','clique'],['#ferr-ler','Enter']]){if(acao==='clique')await page.locator(sel).click();else await page.locator(sel).press(acao);assert.deepEqual(await page.locator('#inicio-cidadania details.cz-fold, details.ferr-grupo:has(>#ferr-ler)').evaluateAll(es=>es.map(e=>e.open)),[true,true],`${rotulo}: ${sel}, ${acao}`);}assert.deepEqual(await page.locator('.cz-fold>summary').evaluateAll(es=>[...new Set(es.map(e=>getComputedStyle(e,'::after').content))]),['none'],rotulo+': sinal de dobra');};
 if(entry&&pagePath===''&&width>=1024)await naoDobra(`${width} ${theme}`);
 if(process.env.CARTAZ_CAPTURAS){await page.evaluate(async()=>{await Promise.all([...document.images].map(im=>{im.loading='eager';return im.decode().catch(()=>{});}));});fs.mkdirSync(process.env.CARTAZ_CAPTURAS,{recursive:true});await page.screenshot({path:path.join(process.env.CARTAZ_CAPTURAS,(pagePath.replaceAll('/','-')||'entrada')+width+'-'+theme+'.png'),fullPage:true});}
 await page.goto(origin+'/lente/'+pagePath+'?projetar=1',{waitUntil:'networkidle'});
 assert.equal(await page.locator('.cz-fold:not([open])').count(),0,'projeção');assert.deepEqual(errors,[]);assert.equal(await page.evaluate(()=>Math.max(0,document.documentElement.scrollWidth-innerWidth)),0,'projeção');
 // 02/11/2026: mede texto efetivamente visível, incluindo o lead e os rótulos das dobras.
 if(pagePath.startsWith('narrativas/'))assert.deepEqual(await page.locator('main').evaluate(main=>[...main.querySelectorAll('*')].filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())&&e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden').filter(e=>parseFloat(getComputedStyle(e).fontSize)<17.85).map(e=>({text:e.textContent.trim(),size:getComputedStyle(e).fontSize}))),[],'projeção sem texto abaixo de 17,9 px arredondados');
 if(entry&&pagePath===''){
  // 02/11/2026: projeção, o título de cada grupo das Ferramentas fica acima das suas ligações.
  assert.ok(await page.evaluate(()=>[...document.querySelectorAll('.ferr-grupo')].every(g=>parseFloat(getComputedStyle(g.querySelector('h3')).fontSize)>parseFloat(getComputedStyle(g.querySelector('ul a')).fontSize))),'grupo acima das ligações em projeção');
  // 02/11/2026: projeção, créditos, descrições das linhas e nota do rodapé a 20 px e ligações do rodapé a 25 px, na escala da entrada.
  // 02/11/2026: com as peças da volta 4, a projeção sobe a raiz (137,5 % a partir de 768 px); os créditos e o rodapé ficam nos degraus 20 e 25 dessa unidade.
  // 07/11/2026: decisões 153, 176 e 177, os créditos das portas passam para o «i»: na projeção, fechado, com alvo de 44 px, e o texto aberto
  // no degrau 20, como a antiga tabela.
  {const u=await page.evaluate(()=>parseFloat(getComputedStyle(document.documentElement).fontSize)/16);assert.deepEqual(await page.evaluate(()=>{const t=q=>[...new Set([...document.querySelectorAll(q)].map(e=>Math.round(parseFloat(getComputedStyle(e).fontSize)*1000)/1000))];return [t('.ld-moldura .info-i-texto,.lab-sets small,.cz-footer .lente-nota'),t('.cz-footer-links a')];}),[[Math.round(20*u*1000)/1000],[Math.round(25*u*1000)/1000]],'projeção: créditos e rodapé');
   assert.deepEqual(await page.locator('.ld-moldura>details.info-i').evaluateAll(es=>es.map(e=>{const r=e.querySelector('summary').getBoundingClientRect();return [e.open,r.width>=44&&r.height>=44];})),[[false,true],[false,true]],'projeção: «i» das portas fechado, alvo de 44 px');}
  if(width>=1024)await naoDobra(`${width} ${theme} projeção`);
 }
 await page.evaluate(()=>dispatchEvent(new Event('beforeprint')));await page.emulateMedia({media:'print'});
 assert.equal(await page.locator('.cz-fold:not([open])').count(),0,'impressão');
 await ctx.close();
 }
 const ctx=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}}),p=await ctx.newPage();
 for(const route of pages){await p.goto(origin+'/lente/'+route);assert.equal(await p.locator('.cz-fold:not([open])').count(),0,'sem JavaScript');
 // 02/11/2026: o botão sem JavaScript não repete o título, mas conserva o destino.
 // 02/11/2026: decisão 134. A caixa saiu; a ligação de continuar fica escondida, com o destino, só para o progresso.
 if(route.startsWith('narrativas/')){assert.equal(await p.locator('.cz-next').count(),0);assert.equal(await p.locator('a.continuar[hidden][data-continuar]').count(),1);assert.ok(await p.locator('a.continuar[hidden]').getAttribute('href'));}}
 await ctx.close();
 if(lab){const ctx=await browser.newContext({viewport:{width:390,height:900}});const data=JSON.parse(fs.readFileSync(path.join(root,'assets/laboratorio/percursos.json'),'utf8')),item=data.pieces.find(p=>p.progress.kind==='feitas'),key=item.progress.key,id=item.progress.id;
 const value={feitas:{[id]:Date.UTC(2026,10,1,12)}};await ctx.addInitScript(({key,value})=>localStorage.setItem(key,JSON.stringify(value)),{key,value});
 const p=await ctx.newPage();/* 05/11/2026: decisão 147 (Laboratório sem o Português): o percurso «montagem» saiu; usa-se o percurso «voz». */await p.goto(origin+'/lente/narrativas/ver/#voz',{waitUntil:'networkidle'});
 const label=p.locator('[data-estado="'+item.id+'"]');if(await label.count())assert.equal(await label.first().textContent(),'Feita 01/11');
 assert.equal(await p.evaluate(k=>localStorage.getItem(k),key),JSON.stringify(value));
 assert.equal(await p.locator('#voz').count(),1);
 const closedAnchor=await p.evaluate(()=>{const target=document.getElementById(location.hash.slice(1));return target&&target.matches('details')&&!target.open;});assert.ok(!closedAnchor);
 // 05/11/2026: decisão 163. Sem dobras: a âncora antiga #criar leva à porta Criar, inteira e à vista no ecrã.
 await p.goto(origin+'/lente/narrativas/#criar',{waitUntil:'networkidle'});assert.ok(await p.locator('#criar a.porta3').isVisible());assert.ok(await p.locator('#criar a.porta3').evaluate(e=>{const r=e.getBoundingClientRect();return r.top>=0&&r.top<innerHeight;}));
 await ctx.close();}
 // 02/11/2026: o percurso atual recebe filete e quadrado, também na entrada geral.
 /* 05/11/2026: decisão 147 (Laboratório sem o Português): as peças de exemplo passam a ser Leonardo, Galileu e Cigoli, que ficam no Laboratório. */
 if(lab){for(const theme of ['light','dark']){const ctx=await browser.newContext({viewport:{width:1366,height:900},colorScheme:theme});await ctx.addInitScript(()=>localStorage.setItem('epi-narrativas',JSON.stringify({feitas:{leonardo:Date.UTC(2026,10,1,12),galileu:Date.UTC(2026,10,1,12)}})));const p=await ctx.newPage();await p.goto(origin+'/lente/narrativas/',{waitUntil:'networkidle'});/* 05/11/2026: decisão 163. Os percursos da entrada passam ao índice do pé (uma linha por percurso); as mesmas exigências. */const row=p.locator('.lab-indice .ind.current');assert.equal(await row.count(),1);assert.equal(await row.evaluate(e=>getComputedStyle(e).borderLeftWidth),'4px');assert.equal(await row.locator('.cz-state.current').textContent(),'A seguir');assert.equal(await row.locator('.cz-state').evaluate(e=>getComputedStyle(e,'::before').backgroundColor),await row.evaluate(e=>getComputedStyle(e).borderLeftColor));assert.deepEqual(await p.evaluate(()=>Object.keys(JSON.parse(localStorage.getItem('epi-narrativas')).feitas)),['leonardo','galileu']);await ctx.close();}}
 if(entry){const ctx=await browser.newContext();await ctx.addInitScript(()=>localStorage.setItem('epi-narrativas',JSON.stringify({feitas:{leonardo:Date.UTC(2026,10,1,12)}})));const p=await ctx.newPage();await p.goto(origin+'/lente/',{waitUntil:'networkidle'});// 02/11/2026: decisão 131. Sem caixa: a retoma marca a divisão do Laboratório e não grava nada.
 await p.waitForFunction(()=>document.querySelectorAll('#inicio-narrativas .lab-sets a .cz-state').length>0);assert.equal(await p.locator('.cz-next,[data-cz-retoma]').count(),0);assert.equal(await p.locator('#inicio-narrativas .cz-fold>summary[data-cz-next]').count(),1);assert.equal(await p.locator('#inicio-cidadania .cz-fold>summary[data-cz-next]').count(),0);assert.deepEqual(await p.evaluate(()=>Object.keys(JSON.parse(localStorage.getItem('epi-narrativas')).feitas)),['leonardo']);await ctx.close();}

 // 01/11/2026: regressões da revisão curta, sem escrever nas chaves do aluno.
 if(entry){
  const data=JSON.parse(fs.readFileSync(path.join(root,'assets/laboratorio/percursos.json'),'utf8'));
  const completed=ids=>{const out={};for(const id of ids){const p=data.pieces.find(p=>p.id===id),q=p.progress,s=out[q.key]??={};if(q.kind==='formas'){s.version=1;s.itens??={};s.itens[q.id]={experimentei:1793534400000};}else if(q.kind==='montagem'){s.version=1;s.done=[...new Set([...(s.done||[]),...q.ids])];}else{(s.feitas??={})[q.id]=1793534400000;}}return out;};
  const observing=data.routes.filter(r=>r.block==='ver').flatMap(r=>r.pieces),all=data.routes.flatMap(r=>r.pieces);
  const cases=[
   [{ 'lente-cidadania-m1-sessoes-v2':{version:2,sessions:{'03':{done:true},'04':{done:true},'05':{done:true}}}},'cidadania/m1/','Continuar →'],
   [{ 'epi-cidadania-m2':{feitas:{'passo-01':1793534400000}}},'cidadania/m2/','Continuar →'],
   [completed(observing),data.pieces.find(p=>p.id===all.find(id=>!observing.includes(id))).url,'Continuar →'],
   [{...completed([all[0]]),'epi-ultima':{id:'m1-f99',t:1893534400000}},data.pieces.find(p=>p.id===all[1]).url,'Continuar →'],
   [completed(all),null,'Rever o percurso →'],
   // 02/11/2026: formato atual das sessões do M2, módulos acabados (M1 com 8 sessões, passos antigos do M2 com 9) e M2 acabado com o M1 a meio.
   [{'lente-cidadania-m2-sessoes-v1':{version:1,sessions:{'01':{done:true},'02':{done:true}}}},'cidadania/m2/','Continuar →'],
   [{'lente-cidadania-m1-sessoes-v2':{version:2,sessions:{'03':{done:true},'04':{done:true},'05':{done:true},'06':{done:true},'07':{done:true},'08':{done:true},'09':{done:true},'10':{done:true}}}},'narrativas/','Começar no Laboratório →'],
   [{'epi-cidadania-m2':{feitas:{'passo-00':1793534400000,'passo-01':1793534400000,'passo-02':1793534400000,'passo-03':1793534400000,'passo-04':1793534400000,'passo-05':1793534400000,'passo-06':1793534400000,'passo-07':1793534400000,'passo-08':1793534400000}}},'narrativas/','Começar no Laboratório →'],
   [{'epi-cidadania-m2':{feitas:{'passo-00':1793534400000,'passo-01':1793534400000,'passo-02':1793534400000,'passo-03':1793534400000,'passo-04':1793534400000,'passo-05':1793534400000,'passo-06':1793534400000,'passo-07':1793534400000,'passo-08':1793534400000}},'lente-cidadania-m1-sessoes-v2':{version:2,sessions:{'03':{done:true}}}},'cidadania/m1/','Continuar →'],
   [{'lente-cidadania-m1-sessoes-v2':{version:2,sessions:{'03':{done:true},'04':{done:true},'05':{done:true},'06':{done:true},'07':{done:true},'08':{done:true},'09':{done:true},'10':{done:true}}},'lente-cidadania-m2-sessoes-v1':{version:1,sessions:{'01':{done:true},'02':{done:true},'03':{done:true}}}},'cidadania/m2/','Continuar →']
  ];
  // 02/11/2026: decisão 131. Cada caso confirma, a 390 px, a divisão marcada e aberta (e a outra fechada quando há retoma; «Começar no Laboratório →» é o caso
  // sem retoma, que fica como no HTML), sem caixa e sem gravar nada. O destino e o botão de cada caso continuam a dizer qual seria a retoma.
  for(const [saved,dest,button] of cases){const ctx=await browser.newContext({viewport:{width:390,height:900}});await ctx.addInitScript(saved=>{for(const [k,v] of Object.entries(saved))localStorage.setItem(k,JSON.stringify(v));},saved);const p=await ctx.newPage();await p.goto(origin+'/lente/',{waitUntil:'networkidle'});await p.waitForFunction(()=>document.querySelectorAll('#inicio-narrativas .lab-sets a .cz-state').length>0);const alvo=dest&&dest.includes('cidadania/')?'inicio-cidadania':'inicio-narrativas',outra=alvo==='inicio-cidadania'?'inicio-narrativas':'inicio-cidadania';assert.equal(await p.locator('.cz-next,[data-cz-retoma]').count(),0);assert.equal(await p.locator('#'+alvo+' .cz-fold>summary[data-cz-next]').count(),1,dest);assert.equal(await p.locator('#'+outra+' .cz-fold>summary[data-cz-next]').count(),0,dest);assert.ok(await p.locator('#'+alvo+' .cz-fold').evaluate(e=>e.open),dest);if(button!=='Começar no Laboratório →')assert.ok(!(await p.locator('#'+outra+' .cz-fold').evaluate(e=>e.open)),dest);for(const [k,v] of Object.entries(saved))assert.deepEqual(await p.evaluate(k=>JSON.parse(localStorage.getItem(k)),k),v);await ctx.close();}
  // 02/11/2026: nota da retoma do Laboratório, «Peça feita» sem dupla pontuação e com o dia local (Lisboa, hora de verão).
  // 02/11/2026: decisão 131. A nota deixou de se mostrar (a caixa saiu); com as mesmas peças feitas, a divisão do Laboratório fica marcada e aberta e nada se grava.
  for(const [saved,nota] of [[{'epi-narrativas':{feitas:{cigoli:true}}},'Peça feita: Cigoli'],[{'epi-narrativas':{feitas:{leonardo:Date.parse('2026-06-15T00:30:00+01:00')}}},'Peça feita: '+data.pieces.find(p=>p.id==='leonardo').title+', 15/06.']]){const ctx=await browser.newContext({viewport:{width:390,height:900},timezoneId:'Europe/Lisbon'});await ctx.addInitScript(saved=>{for(const [k,v] of Object.entries(saved))localStorage.setItem(k,JSON.stringify(v));},saved);const p=await ctx.newPage();await p.goto(origin+'/lente/',{waitUntil:'networkidle'});await p.waitForFunction(()=>document.querySelectorAll('#inicio-narrativas .lab-sets a .cz-state').length>0);assert.ok(nota.startsWith('Peça feita: '));assert.equal(await p.locator('.cz-next,[data-cz-retoma-estado]').count(),0);assert.equal(await p.locator('#inicio-narrativas .cz-fold>summary[data-cz-next]').count(),1);assert.ok(await p.locator('#inicio-narrativas .cz-fold').evaluate(e=>e.open));assert.ok(!(await p.locator('#inicio-cidadania .cz-fold').evaluate(e=>e.open)));for(const [k,v] of Object.entries(saved))assert.deepEqual(await p.evaluate(k=>JSON.parse(localStorage.getItem(k)),k),v);await ctx.close();}
 }
 // 01/11/2026: forçar uma fonte larga para que Windows e Linux detetem a mesma regressão sem Bebas Neue.
 // 02/11/2026: nenhuma palavra partida a meio no nome da porta (translineação pt-PT: só se quebra depois de espaço ou de hífen) e nenhum nome a transbordar, com as Google Fonts bloqueadas e Arial forçada a 320, 360, 375, 640 e 768 px, e com a fonte externa a 640 px.
 if(entry){const partidas=()=>[...document.querySelectorAll('.ld-n')].flatMap(h=>{const out=[],w=document.createTreeWalker(h,NodeFilter.SHOW_TEXT);let n,prev=null,antes='',feito='';while(n=w.nextNode())for(let i=0;i<n.data.length;i++){const c=n.data[i],r=document.createRange();r.setStart(n,i);r.setEnd(n,i+1);const q=[...r.getClientRects()].find(x=>x.width>0);if(q&&prev&&q.top>prev.top+q.height/2&&!/[\s\-\u00ad\u2010]/.test(antes)&&!/\s/.test(c))out.push(feito+'|'+c);if(q)prev=q;antes=c;feito+=c;}return out;});
  const transborda=()=>[...document.querySelectorAll('.ld-n')].filter(e=>e.scrollWidth>e.clientWidth).map(e=>e.textContent);
  for(const [width,bloquear] of [[320,true],[360,true],[375,true],[640,true],[768,true],[640,false]]){const ctx=await browser.newContext({viewport:{width,height:900}});if(bloquear)for(const u of ['https://fonts.googleapis.com/**','https://fonts.gstatic.com/**'])await ctx.route(u,r=>r.abort());const p=await ctx.newPage();await p.goto(origin+'/lente/',{waitUntil:'networkidle'});if(bloquear)await p.addStyleTag({content:'[data-cartaz-entrada] .ld-n{font-family:Arial,sans-serif!important}'});await p.evaluate(()=>document.fonts.ready);await p.locator('.ld details').evaluateAll(es=>es.forEach(e=>e.open=true));const rotulo=width+' px, '+(bloquear?'fonte alternativa':'fonte externa');assert.equal(await p.evaluate(()=>Math.max(0,document.documentElement.scrollWidth-innerWidth)),0,'títulos com fonte alternativa larga, '+rotulo);assert.deepEqual(await p.evaluate(partidas),[],'palavra partida no nome da porta, '+rotulo);assert.deepEqual(await p.evaluate(transborda),[],'nome da porta a transbordar, '+rotulo);await ctx.close();}}
 console.log('Família Cartaz: temas, alvos, dobras, projeção, impressão, sem JavaScript e progresso verificados.');
}finally{await browser.close();server.closeAllConnections();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
