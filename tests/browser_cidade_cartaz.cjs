// 08/11/2026: pedido cidade-cartaz-lente. O cartão «Ler a cidade.» da entrada do Lente, no mesmo componente do cartão «Português.»:
// a 320, 390, 768 e 1280 px (e a 390 e a 1280 px no modo escuro) a página não rola para o lado, o cartão não transborda, a fotografia
// carrega, o «i» abre e fecha (rato, teclado e toque) e os alvos têm pelo menos 44 px; no modo escuro, o cartão segue as cores da
// entrada. Com CIDADE_CARTAZ_PROVAS, guarda capturas da zona dos dois cartões (deviceScaleFactor 1).
// 12/11/2026: pedido entrada-temas. Na entrada em quatro temas, «Ler a cidade» é o destino do tema 04 («Imagem, som e cidade»): o cartão
// «Ler a cidade.» deu lugar ao cartão do tema, no componente dos quatro temas (article.tm), com a fotografia da Rua da Boavista, do
// arquivo da escola, servida pelo próprio Lente. O teste mede esse cartão com as mesmas exigências, nas mesmas larguras e modos: sem
// deslize, sem transbordo, fotografia carregada (agora sempre, já não depende de rede), moldura e enquadramento, alvos de 44 px,
// contraste de 4,5:1, cores do tema, e o «i» a abrir e a fechar por rato, teclado e toque, com o crédito exato. Em vez de «logo antes
// do cartão do Português, com a mesma largura», confere-se que é o quarto dos quatro temas, logo depois do tema 03 e com a mesma largura.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),PROVAS=process.env.CIDADE_CARTAZ_PROVAS;
const FOTO='img/arquivo/rua-da-boavista-carris-2026-720.webp';
const server=http.createServer((req,res)=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname).replace(/^\/lente/,''));if(!f.startsWith(root+path.sep)&&f!==root){res.writeHead(403);return res.end();}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.webp':'image/webp','.jpg':'image/jpeg'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});
// Medidas do cartão dentro da página.
function medir(){
 const cartoes=[...document.querySelectorAll('[data-cartaz-entrada] .tm-g>li>article.tm')],wrap=cartoes[3],pt=cartoes[2];
 const a=wrap.querySelector('h3.tm-n a'),img=wrap.querySelector('.tm-img img'),caixa=wrap.querySelector('.tm-img'),d=wrap.querySelector('details.info-i'),s=d.querySelector('summary');
 const r=e=>e.getBoundingClientRect(),ra=r(wrap);
 const dentro=(e,c,f=1)=>{const x=r(e),y=r(c);return x.left>=y.left-f&&x.right<=y.right+f&&x.top>=y.top-f&&x.bottom<=y.bottom+f;};
 // elementos de texto do cartão que transbordam a sua caixa ou o cartão
 const transborda=[...wrap.querySelectorAll('.tm-corpo,.tm-n,.tm-q,.tm-f,.tm-seta')].filter(e=>e.scrollWidth>e.clientWidth+1||!dentro(e,wrap)).map(e=>e.className);
 const lum=c=>{const v=c.match(/[\d.]+/g).slice(0,3).map(Number).map(x=>{x/=255;return x<=.03928?x/12.92:Math.pow((x+.055)/1.055,2.4);});return .2126*v[0]+.7152*v[1]+.0722*v[2];};
 const fundo=getComputedStyle(wrap).backgroundColor,contraste=[...wrap.querySelectorAll('.tm-n a,.tm-q,.tm-f,.tm-seta')].map(e=>{const l1=lum(getComputedStyle(e).color),l2=lum(fundo);return Math.round((Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05)*100)/100;});
 // a ligação do título estica-se ao cartão inteiro: o alvo da ligação é o cartão
 const alvo=(()=>{const x=ra.left+ra.width/2,y=r(wrap.querySelector('.tm-q')).top+4,e=document.elementFromPoint(x,y);return !!e&&(e===a||a.contains(e));})();
 return {lado:document.documentElement.scrollWidth-innerWidth,cartao:[ra.left,ra.right,ra.width,ra.height],ecra:innerWidth,quantos:cartoes.length,dentroDoAside:dentro(wrap,document.querySelector('.tm-temas')),
  mesmaLargura:Math.abs(ra.width-r(pt).width)<=1&&(innerWidth>=760?Math.abs(ra.top-r(pt).top)<=1&&Math.abs(ra.height-r(pt).height)<=1:Math.abs(ra.left-r(pt).left)<=1),
  antesDoPortugues:wrap.parentElement.previousElementSibling===pt.parentElement&&!wrap.parentElement.nextElementSibling,
  transborda,imagem:{completa:img.complete,largura:img.naturalWidth,caixa:[r(caixa).width,r(caixa).height],dentro:dentro(caixa,wrap),cobre:getComputedStyle(img).objectFit,pos:getComputedStyle(img).objectPosition,etiquetaDentro:dentro(s,caixa)},
  alvos:{cartao:[ra.width,ra.height],acao:alvo?ra.height:0,i:[r(s).width,r(s).height]},iForaDaLigacao:!d.closest('a'),iAberto:d.open,
  textoI:d.open?{visivel:d.querySelector('.info-i-texto').getClientRects().length>0,dentro:r(d.querySelector('.info-i-texto')).right<=innerWidth+1&&r(d.querySelector('.info-i-texto')).left>=-1}:null,
  tema:document.documentElement.dataset.theme,fundo,contraste,textos:[...wrap.querySelectorAll('.tm-n b,.tm-n a,.tm-q,.tm-f,.tm-seta')].map(e=>e.textContent.replace(/\s+/g,' ').trim())};}
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});let n=0,semRede=0;
 if(PROVAS)fs.mkdirSync(PROVAS,{recursive:true});
 try{for(const [tema,larguras] of [['light',[320,390,768,1280]],['dark',[390,1280]]])for(const width of larguras){
  const rot=`${width} px, ${tema==='dark'?'escuro':'claro'}`;
  const ctx=await browser.newContext({viewport:{width,height:900},deviceScaleFactor:1,hasTouch:true,colorScheme:tema});
  // o modo escuro liga-se como o aluno o liga: a escolha guardada por assets/appearance.js (epi-theme)
  if(tema==='dark')await ctx.addInitScript(()=>{try{localStorage.setItem('epi-theme','dark');}catch(e){}});
  await ctx.route('https://pedrohfernandes-klk.github.io/lente/**',async route=>{const u=new URL(route.request().url());const response=await ctx.request.get(origin+u.pathname+u.search);await route.fulfill({response});});
  await ctx.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());
  const page=await ctx.newPage(),errors=[];let fotoFalhou=null;page.on('pageerror',e=>errors.push(e.message));
  page.on('requestfailed',q=>{if(q.url().endsWith(FOTO))fotoFalhou=q.failure()?q.failure().errorText:'falhou';});
  await page.goto(origin+'/lente/',{waitUntil:'networkidle'});
  const wrap=page.locator('[data-cartaz-entrada] .tm-g>li:nth-child(4)>article.tm');assert.equal(await wrap.count(),1,rot+': um cartão');
  assert.equal(await page.locator('[data-cartaz-entrada] article.tm a[href="https://pedrohfernandes-klk.github.io/lente/cidade/"]').count(),1,rot+': uma só ligação à cidade');
  assert.equal(await wrap.locator('h3.tm-n a').getAttribute('href'),'https://pedrohfernandes-klk.github.io/lente/cidade/',rot+': destino');
  await wrap.scrollIntoViewIfNeeded();
  // 08/11/2026 (revisão do #142): a fotografia tem loading="lazy"; com o cartão à vista, tem de carregar.
  assert.equal(await wrap.locator('.tm-img img').getAttribute('loading'),'lazy',rot+': carregamento diferido');
  assert.equal(await wrap.locator('.tm-img img').getAttribute('src'),FOTO,rot+': fotografia do arquivo, servida pelo Lente');
  await wrap.locator('.tm-img img').evaluate(i=>i.complete?null:new Promise(r=>{i.addEventListener('load',r,{once:true});i.addEventListener('error',r,{once:true});setTimeout(r,15000);}));
  let m=await page.evaluate(medir);
  assert.equal(m.tema,tema,rot+': tema da página');
  assert.ok(m.lado<=0,rot+': sem deslize horizontal ('+m.lado+' px)');
  assert.ok(m.cartao[0]>=0&&m.cartao[1]<=m.ecra,rot+': o cartão cabe no ecrã '+JSON.stringify(m.cartao));
  assert.equal(m.quantos,4,rot+': quatro temas');
  assert.ok(m.dentroDoAside,rot+': o cartão fica dentro da secção dos temas');assert.ok(m.mesmaLargura,rot+': mesma largura e alinhamento do cartão do tema 03');
  assert.ok(m.antesDoPortugues,rot+': o último dos quatro, logo depois do tema 03');
  assert.deepEqual(m.transborda,[],rot+': nenhum texto transborda o cartão');
  assert.deepEqual(m.textos,['04','Imagem, som e cidade','O que muda quando mudas o enquadramento?','Lês uma rua como um texto, escolhes uma das 14 missões e explicas o que ficou fora da fotografia.','→'],rot+': texto do cartão');
  // fotografia: carrega (sem rede, como nos outros testes que deixam a rede de fora, conta-se à parte e a moldura tem de se manter)
  // 08/11/2026 (revisão do #142): no CI há rede; aí, uma falha da fotografia faz falhar o teste.
  // 12/11/2026: a fotografia é do próprio repositório; tem de carregar sempre, com rede ou sem ela.
  if(fotoFalhou)assert.fail(rot+': a fotografia não carregou ('+fotoFalhou+')');
  assert.ok(m.imagem.completa&&m.imagem.largura===720,rot+': a fotografia carrega ('+m.imagem.largura+')');
  assert.ok(m.imagem.caixa[0]>=80&&m.imagem.caixa[1]>=150&&m.imagem.dentro,rot+': moldura da fotografia '+JSON.stringify(m.imagem.caixa));
  assert.equal(m.imagem.cobre,'cover',rot);assert.equal(m.imagem.pos,'50% 60%',rot+': enquadramento');assert.ok(m.imagem.etiquetaDentro,rot+': «i» dentro da fotografia');
  // alvos de pelo menos 44 px
  assert.ok(m.alvos.cartao[0]>=44&&m.alvos.cartao[1]>=44&&m.alvos.acao>=44,rot+': alvo do cartão');assert.ok(m.alvos.i[0]>=44&&m.alvos.i[1]>=44,rot+': alvo do «i» '+JSON.stringify(m.alvos.i));
  assert.ok(m.iForaDaLigacao,rot+': «i» fora da ligação');assert.equal(m.iAberto,false,rot+': «i» fechado ao carregar');
  // contraste do texto do cartão (no claro e no escuro, o cartão segue as cores da entrada)
  assert.ok(m.contraste.every(c=>c>=4.5),rot+': contraste '+JSON.stringify(m.contraste));
  const fundoClaro=await page.evaluate(f=>{const v=f.match(/[\d.]+/g).map(Number);return (v[0]+v[1]+v[2])/3>128;},m.fundo);assert.equal(fundoClaro,tema==='light',rot+': fundo do cartão '+m.fundo);
  // o «i»: rato, teclado e toque
  const s=wrap.locator('details.info-i>summary'),d=wrap.locator('details.info-i');
  await s.click();m=await page.evaluate(medir);assert.ok(m.iAberto&&m.textoI.visivel&&m.textoI.dentro,rot+': clique abre');assert.ok(m.lado<=0,rot+': aberto, sem deslize');
  assert.equal((await wrap.locator('.info-i-texto').textContent()).trim(),'Rua da Boavista, Lisboa. Fotografia: Arquivo da EPI, 2026.',rot+': crédito');
  await s.click();assert.equal(await d.evaluate(e=>e.open),false,rot+': clique fecha');
  await s.focus();await page.keyboard.press('Enter');assert.equal(await d.evaluate(e=>e.open),true,rot+': Enter abre');
  await page.keyboard.press('Escape');assert.equal(await d.evaluate(e=>e.open),false,rot+': Escape fecha');assert.ok(await s.evaluate(e=>document.activeElement===e),rot+': o foco volta ao «i»');
  await s.tap();assert.equal(await d.evaluate(e=>e.open),true,rot+': toque abre');await s.tap();assert.equal(await d.evaluate(e=>e.open),false,rot+': toque fecha');
  if(PROVAS&&(width===390||width===1280)){
   await page.evaluate(()=>document.activeElement&&document.activeElement.blur());await page.mouse.move(0,0);
   const caixas=await page.locator('[data-cartaz-entrada] article.tm').evaluateAll(es=>es.map(e=>{const r=e.getBoundingClientRect();return [r.top+scrollY,r.bottom+scrollY];}));
   const y=Math.max(0,caixas[0][0]-24),h=caixas[caixas.length-1][1]+24-y;
   await page.screenshot({path:path.join(PROVAS,`cartazes-${width}-${tema==='dark'?'escuro':'claro'}.png`),fullPage:true,clip:{x:0,y,width,height:h}});
  }
  assert.deepEqual(errors,[],rot+': sem erros');n++;await ctx.close();
 }
 console.log('Cartão do tema 04 («Ler a cidade»): '+n+' larguras e modos, sem deslize, sem transbordo, «i» a abrir e a fechar, alvos de 44 px'+(semRede?', '+semRede+' sem rede para a fotografia':', fotografia carregada')+'.');
 }finally{await browser.close();server.closeAllConnections();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
