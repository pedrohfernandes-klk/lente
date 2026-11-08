// 08/11/2026: pedido cidade-cartaz-lente. O cartão «Ler a cidade.» da entrada do Lente, no mesmo componente do cartão «Português.»:
// a 320, 390, 768 e 1280 px (e a 390 e a 1280 px no modo escuro) a página não rola para o lado, o cartão não transborda, a fotografia
// carrega, o «i» abre e fecha (rato, teclado e toque) e os alvos têm pelo menos 44 px; no modo escuro, o cartão segue as cores da
// entrada. Com CIDADE_CARTAZ_PROVAS, guarda capturas da zona dos dois cartões (deviceScaleFactor 1).
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),PROVAS=process.env.CIDADE_CARTAZ_PROVAS;
const FOTO='https://pedrohfernandes-klk.github.io/pt/img/arquivo/tejo-1907-vela-e-cidade.jpg';
const server=http.createServer((req,res)=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname).replace(/^\/lente/,''));if(!f.startsWith(root+path.sep)&&f!==root){res.writeHead(403);return res.end();}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.webp':'image/webp','.jpg':'image/jpeg'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});
// Medidas do cartão dentro da página.
function medir(){
 const wrap=document.querySelector('aside.site-portal-wrap[aria-label="Explorar Ler a cidade"]'),pt=document.querySelector('aside.site-portal-wrap[aria-label="Explorar Português"]');
 const a=wrap.querySelector('a.site-portal'),img=a.querySelector('.sp-image img'),caixa=a.querySelector('.sp-image'),etq=a.querySelector('.sp-image-label'),d=wrap.querySelector('details.info-i'),s=d.querySelector('summary');
 const r=e=>e.getBoundingClientRect(),ra=r(a),rw=r(wrap);
 const dentro=(e,c,f=1)=>{const x=r(e),y=r(c);return x.left>=y.left-f&&x.right<=y.right+f&&x.top>=y.top-f&&x.bottom<=y.bottom+f;};
 // elementos de texto do cartão que transbordam a sua caixa ou o cartão
 const transborda=[...a.querySelectorAll('.sp-copy,.sp-kicker,.sp-title,.sp-description,.sp-action,.sp-image-label')].filter(e=>e.scrollWidth>e.clientWidth+1||!dentro(e,a)).map(e=>e.className);
 const lum=c=>{const v=c.match(/[\d.]+/g).slice(0,3).map(Number).map(x=>{x/=255;return x<=.03928?x/12.92:Math.pow((x+.055)/1.055,2.4);});return .2126*v[0]+.7152*v[1]+.0722*v[2];};
 const fundo=getComputedStyle(a).backgroundColor,contraste=[...a.querySelectorAll('.sp-kicker,.sp-title,.sp-description,.sp-action')].map(e=>{const l1=lum(getComputedStyle(e).color),l2=lum(fundo);return Math.round((Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05)*100)/100;});
 return {lado:document.documentElement.scrollWidth-innerWidth,cartao:[ra.left,ra.right,ra.width,ra.height],ecra:innerWidth,dentroDoAside:dentro(a,wrap),
  mesmaLargura:Math.abs(ra.width-r(pt.querySelector('a.site-portal')).width)<=1&&Math.abs(ra.left-r(pt.querySelector('a.site-portal')).left)<=1,
  antesDoPortugues:!!(wrap.compareDocumentPosition(pt)&Node.DOCUMENT_POSITION_FOLLOWING)&&wrap.nextElementSibling===pt,
  transborda,imagem:{completa:img.complete,largura:img.naturalWidth,caixa:[r(caixa).width,r(caixa).height],dentro:dentro(caixa,a),cobre:getComputedStyle(img).objectFit,pos:getComputedStyle(img).objectPosition,etiquetaDentro:dentro(etq,caixa)},
  alvos:{cartao:[ra.width,ra.height],acao:r(a.querySelector('.sp-action')).height,i:[r(s).width,r(s).height]},iForaDaLigacao:!d.closest('a'),iAberto:d.open,
  textoI:d.open?{visivel:d.querySelector('.info-i-texto').getClientRects().length>0,dentro:r(d.querySelector('.info-i-texto')).right<=innerWidth+1&&r(d.querySelector('.info-i-texto')).left>=-1}:null,
  tema:document.documentElement.dataset.theme,fundo,contraste,textos:[...a.querySelectorAll('.sp-kicker,.sp-title,.sp-description,.sp-action,.sp-image-label')].map(e=>e.textContent.replace(/\s+/g,' ').trim())};}
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
  page.on('requestfailed',q=>{if(q.url()===FOTO)fotoFalhou=q.failure()?q.failure().errorText:'falhou';});
  await page.goto(origin+'/lente/',{waitUntil:'networkidle'});
  const wrap=page.locator('aside.site-portal-wrap[aria-label="Explorar Ler a cidade"]');assert.equal(await wrap.count(),1,rot+': um cartão');
  await wrap.scrollIntoViewIfNeeded();
  // 08/11/2026 (revisão do #142): a fotografia tem loading="lazy"; com o cartão à vista, tem de carregar.
  assert.equal(await page.locator('.portal-cidade .sp-image img').getAttribute('loading'),'lazy',rot+': carregamento diferido');
  await page.locator('.portal-cidade .sp-image img').evaluate(i=>i.complete?null:new Promise(r=>{i.addEventListener('load',r,{once:true});i.addEventListener('error',r,{once:true});setTimeout(r,15000);}));
  let m=await page.evaluate(medir);
  assert.equal(m.tema,tema,rot+': tema da página');
  assert.ok(m.lado<=0,rot+': sem deslize horizontal ('+m.lado+' px)');
  assert.ok(m.cartao[0]>=0&&m.cartao[1]<=m.ecra,rot+': o cartão cabe no ecrã '+JSON.stringify(m.cartao));
  assert.ok(m.dentroDoAside,rot+': o cartão fica dentro do seu aside');assert.ok(m.mesmaLargura,rot+': mesma largura e alinhamento do cartão do Português');
  assert.ok(m.antesDoPortugues,rot+': logo antes do cartão do Português');
  assert.deepEqual(m.transborda,[],rot+': nenhum texto transborda o cartão');
  assert.deepEqual(m.textos,['Português × Cidadania','Ler a cidade.','Uma rua pode ser lida como um texto. São 14 missões, no bairro ou a partir das fotografias.','Entrar →','Lisboa vista do Tejo, 1907'],rot+': texto do cartão');
  // fotografia: carrega (sem rede, como nos outros testes que deixam a rede de fora, conta-se à parte e a moldura tem de se manter)
  // 08/11/2026 (revisão do #142): no CI há rede; aí, uma falha da fotografia faz falhar o teste.
  if(fotoFalhou&&process.env.CI)assert.fail(rot+': a fotografia não carregou no CI ('+fotoFalhou+')');
  if(fotoFalhou){semRede++;console.log(rot+': fotografia sem rede ('+fotoFalhou+'); confere-se só a moldura.');}
  else assert.ok(m.imagem.completa&&m.imagem.largura===1160,rot+': a fotografia carrega ('+m.imagem.largura+')');
  assert.ok(m.imagem.caixa[0]>=80&&m.imagem.caixa[1]>=150&&m.imagem.dentro,rot+': moldura da fotografia '+JSON.stringify(m.imagem.caixa));
  assert.equal(m.imagem.cobre,'cover',rot);assert.equal(m.imagem.pos,'12% 30%',rot+': enquadramento');assert.ok(m.imagem.etiquetaDentro,rot+': etiqueta dentro da fotografia');
  // alvos de pelo menos 44 px
  assert.ok(m.alvos.cartao[0]>=44&&m.alvos.cartao[1]>=44&&m.alvos.acao>=44,rot+': alvo do cartão');assert.ok(m.alvos.i[0]>=44&&m.alvos.i[1]>=44,rot+': alvo do «i» '+JSON.stringify(m.alvos.i));
  assert.ok(m.iForaDaLigacao,rot+': «i» fora da ligação');assert.equal(m.iAberto,false,rot+': «i» fechado ao carregar');
  // contraste do texto do cartão (no claro e no escuro, o cartão segue as cores da entrada)
  assert.ok(m.contraste.every(c=>c>=4.5),rot+': contraste '+JSON.stringify(m.contraste));
  const fundoClaro=await page.evaluate(f=>{const v=f.match(/[\d.]+/g).map(Number);return (v[0]+v[1]+v[2])/3>128;},m.fundo);assert.equal(fundoClaro,tema==='light',rot+': fundo do cartão '+m.fundo);
  // o «i»: rato, teclado e toque
  const s=wrap.locator('details.info-i>summary'),d=wrap.locator('details.info-i');
  await s.click();m=await page.evaluate(medir);assert.ok(m.iAberto&&m.textoI.visivel&&m.textoI.dentro,rot+': clique abre');assert.ok(m.lado<=0,rot+': aberto, sem deslize');
  assert.equal((await wrap.locator('.info-i-texto').textContent()).trim(),'Metade de um estereograma de 1907, com direitos de J. J. Killelea & Co. e publicado por H. C. White Co. Domínio público. Fonte da fotografia',rot+': crédito');
  await s.click();assert.equal(await d.evaluate(e=>e.open),false,rot+': clique fecha');
  await s.focus();await page.keyboard.press('Enter');assert.equal(await d.evaluate(e=>e.open),true,rot+': Enter abre');
  await page.keyboard.press('Escape');assert.equal(await d.evaluate(e=>e.open),false,rot+': Escape fecha');assert.ok(await s.evaluate(e=>document.activeElement===e),rot+': o foco volta ao «i»');
  await s.tap();assert.equal(await d.evaluate(e=>e.open),true,rot+': toque abre');await s.tap();assert.equal(await d.evaluate(e=>e.open),false,rot+': toque fecha');
  if(PROVAS&&(width===390||width===1280)){
   await page.evaluate(()=>document.activeElement&&document.activeElement.blur());await page.mouse.move(0,0);
   const caixas=await page.locator('aside.site-portal-wrap').evaluateAll(es=>es.map(e=>{const r=e.getBoundingClientRect();return [r.top+scrollY,r.bottom+scrollY];}));
   const y=Math.max(0,caixas[0][0]-24),h=caixas[caixas.length-1][1]+24-y;
   await page.screenshot({path:path.join(PROVAS,`cartazes-${width}-${tema==='dark'?'escuro':'claro'}.png`),fullPage:true,clip:{x:0,y,width,height:h}});
  }
  assert.deepEqual(errors,[],rot+': sem erros');n++;await ctx.close();
 }
 console.log('Cartaz «Ler a cidade»: '+n+' larguras e modos, sem deslize, sem transbordo, «i» a abrir e a fechar, alvos de 44 px'+(semRede?', '+semRede+' sem rede para a fotografia':', fotografia carregada')+'.');
 }finally{await browser.close();server.closeAllConnections();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
