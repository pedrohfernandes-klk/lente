// 12/11/2026: pedido entrada-temas. A entrada do Lente em quatro temas e a página do tema 02 (informacao/), em navegador real, a 390 e a
// 1280 px, em claro e escuro (o modo escuro liga-se como o aluno o liga, pela escolha guardada por assets/appearance.js) e em projeção
// (a entrada com ?projetar=1 e as duas páginas dentro da moldura de /projetar/, nos três tamanhos de letra).
// Entrada: sem erros nem pedidos falhados, sem deslize e sem nada a sair do ecrã, abaixo de 3000 px a 390 px, quatro temas pela ordem
// com as imagens carregadas, foco de teclado por todas as ligações e à vista, cada «i» a abrir e a fechar (clique, Enter, Escape, um de
// cada vez, com a ligação da fonte livre), alvos de 44 px, o cartão inteiro do tema 02 a abrir a sua página e a ligação ao Ideias a
// abrir o Ideias. Página do tema: o mesmo, mais a pergunta como título, a atividade que abre o tema, a dobra «Ver tudo neste tema»
// fechada ao carregar e a abrir e fechar por clique, Enter e Espaço, com as 23 ligações à vista e a responder, a impressão com a dobra
// por extenso e o regresso aos quatro temas. Com ENTRADA_TEMAS_PROVAS, guarda capturas de página inteira.
// 12/11/2026: revisão. Mede-se também a 320 px; o anel de foco de cada ligação tem de contrastar 3:1 com o fundo onde assenta, em claro
// e em escuro (os blocos invertidos «Português e Exames» e «Para aplicar» incluídos, conferidos pelo nome); o crédito aberto de cada «i»
// lê-se inteiro, sem deslizar por dentro da moldura, a todas as larguras; e os textos do bloco «Para aplicar», com o ponto do título,
// têm 4,5:1 sobre o bloco nos dois modos.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),PROVAS=process.env.ENTRADA_TEMAS_PROVAS,SITIO='https://pedrohfernandes-klk.github.io/lente/';
const TIPOS={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.webp':'image/webp','.jpg':'image/jpeg','.png':'image/png'};
const server=http.createServer((req,res)=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname).replace(/^\/lente/,''));if(!f.startsWith(root+path.sep)&&f!==root){res.writeHead(403);return res.end();}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',TIPOS[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});
const TEMAS=[['01',SITIO+'olhar-e-decidir/','Justiça e vida em comum','Uma regra igual é sempre justa?'],['02','informacao/','Informação e mundo digital','Porque estás a ver isto?'],['03',SITIO+'narrativas/','Histórias e criação','O que transforma uma ideia numa história?'],['04',SITIO+'cidade/','Imagem, som e cidade','O que muda quando mudas o enquadramento?']];
// Dentro da página: o que sai do ecrã, o que transborda a sua caixa e os alvos pequenos (só o que se vê; a lupa do cabeçalho é decorativa).
function geometria(){
 const vis=e=>e.getClientRects().length>0&&e.checkVisibility({visibilityProperty:true,contentVisibilityAuto:true});
 const nome=e=>e.tagName.toLowerCase()+(e.className&&typeof e.className==='string'?'.'+e.className.trim().split(/\s+/).join('.'):'')+' «'+e.textContent.trim().slice(0,30)+'»';
 const todos=[...document.querySelectorAll('body *')].filter(e=>vis(e)&&!e.closest('.lf-mesa,[data-appearance-floating],.epi-appearance-toggle'));
 const fora=todos.filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+1||r.left<-1);}).map(nome);
 const transborda=todos.filter(e=>e.matches('h1,h2,h3,p,li,a,figcaption,summary,.tm,.tm-corpo,.tm-comeca-c,.tm-aplicar')&&e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).display!=='inline').map(nome);
 const alvos=todos.filter(e=>e.matches('a[href],summary,button')&&!e.closest('.info-i-texto,.lente-nota')).filter(e=>{let r=e.getBoundingClientRect();if(e.matches('.tm-n a,.tm-alt h2 a'))r=e.closest('.tm,li').getBoundingClientRect();return r.height<43.5||r.width<43.5;}).map(nome);
 return {lado:Math.max(0,document.documentElement.scrollWidth-innerWidth),altura:document.documentElement.scrollHeight,fora,transborda,alvos,tema:document.documentElement.dataset.theme,
  imagens:[...document.querySelectorAll('main img')].map(i=>i.complete&&i.naturalWidth>0),raiz:parseFloat(getComputedStyle(document.documentElement).fontSize)};
}
// O foco de teclado no elemento ativo: à vista (um contorno no próprio elemento, ou no cartão quando a ligação se estica ao cartão) e dentro do ecrã.
function foco(){
 const e=document.activeElement;if(!e||e===document.body)return null;
 const c=getComputedStyle(e),cartao=e.closest('.tm,.tm-alt li'),cc=cartao?getComputedStyle(cartao):null;
 const anel=x=>x&&x.outlineStyle!=='none'&&parseFloat(x.outlineWidth)>=2;
 const r=(e.matches('.tm-n a,.tm-alt h2 a')?cartao:e).getBoundingClientRect();
 // 12/11/2026: revisão. O contraste do anel com o fundo onde assenta (o do antepassado mais próximo com fundo; o anel fica por fora do
 // elemento). O «i» tem o anel por dentro do alvo, sobre a imagem, e confere-se em tests/browser_creditos_i_lente4.cjs.
 const lum=x=>{const v=x.match(/[\d.]+/g).slice(0,3).map(Number).map(y=>{y/=255;return y<=.03928?y/12.92:Math.pow((y+.055)/1.055,2.4);});return .2126*v[0]+.7152*v[1]+.0722*v[2];};
 const opaco=x=>{const v=x.match(/[\d.]+/g).map(Number);return v.length<4||v[3]===1;};
 const dono=e.matches('.tm-n a,.tm-alt h2 a')&&anel(cc)?cartao:e,cd=getComputedStyle(dono);let contraste=null;
 if(anel(cd)&&!e.closest('.info-i')){let p=dono.parentElement,f=null;while(p&&!f){const b=getComputedStyle(p).backgroundColor;if(opaco(b))f=b;p=p.parentElement;}
  if(f&&opaco(cd.outlineColor)){const a=lum(cd.outlineColor),z=lum(f);contraste=Math.round((Math.max(a,z)+.05)/(Math.min(a,z)+.05)*100)/100;}}
 return {contraste,nome:(e.getAttribute('href')||e.getAttribute('aria-label')||e.textContent.trim()).slice(0,90),tag:e.tagName,anel:anel(c)||(e.matches('.tm-n a,.tm-alt h2 a')&&anel(cc))||c.boxShadow!=='none',noEcra:r.bottom>0&&r.top<innerHeight&&r.right>0&&r.left<innerWidth,dentro:!!e.closest('main')};
}
async function tabular(page,max){const paragens=[];for(let k=0;k<max;k++){await page.keyboard.press('Tab');const f=await page.evaluate(foco);if(!f)break;paragens.push(f);if(!f.dentro&&paragens.some(x=>x.dentro))break;}return paragens;}
async function conferirI(page,d,rot,comLigacao){
 const s=d.locator('summary');await s.scrollIntoViewIfNeeded();
 assert.equal(await d.evaluate(e=>e.open),false,rot+': fechado ao carregar');
 await s.click();assert.equal(await d.evaluate(e=>e.open),true,rot+': clique abre');
 const t=d.locator('.info-i-texto');assert.ok(await t.isVisible(),rot+': crédito à vista');
 assert.ok(await t.evaluate(e=>{const r=e.getBoundingClientRect();return r.left>=-1&&r.right<=innerWidth+1&&e.textContent.trim().length>30;}),rot+': crédito dentro do ecrã');
 assert.equal(await page.evaluate(()=>Math.max(0,document.documentElement.scrollWidth-innerWidth)),0,rot+': aberto, sem deslize');
 // 12/11/2026: revisão. O crédito aberto lê-se inteiro: não desliza por dentro da moldura e a ligação da fonte está livre sem o deslizar.
 await page.waitForTimeout(250);assert.ok(await t.evaluate(e=>e.scrollHeight<=e.clientHeight+1),rot+': crédito inteiro, sem deslizar por dentro');
 assert.equal(await t.evaluate(e=>{e.scrollIntoView({block:'center'});const q=[];const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let no;while(no=w.nextNode()){if(!no.data.trim())continue;const r=document.createRange();r.selectNodeContents(no);for(const c of r.getClientRects())if(c.width>2)q.push(c);}return q.filter(c=>{const x=document.elementFromPoint(c.left+Math.min(c.width/2,8),c.top+c.height/2);return !x||!(x===e||e.contains(x));}).length;}),0,rot+': nenhuma linha do crédito tapada');
 if(comLigacao){const a=t.locator('a[href^="https://commons.wikimedia.org/wiki/File:"]');assert.equal(await a.count(),1,rot+': ligação à fonte');assert.ok(await a.evaluate(e=>[...e.getClientRects()].every(r=>document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)===e)),rot+': a ligação da fonte fica livre sem deslizar o crédito');await t.evaluate(e=>{e.scrollTop=e.scrollHeight;e.scrollIntoView({block:'center'});});assert.ok(await a.evaluate(e=>[...e.getClientRects()].every(r=>document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)===e)),rot+': a ligação da fonte fica livre');}
 await page.keyboard.press('Escape');assert.equal(await d.evaluate(e=>e.open),false,rot+': Escape fecha');assert.ok(await s.evaluate(e=>document.activeElement===e),rot+': o foco volta ao «i»');
 await page.keyboard.press('Enter');assert.equal(await d.evaluate(e=>e.open),true,rot+': Enter abre');
 await s.click();assert.equal(await d.evaluate(e=>e.open),false,rot+': clique fecha');
}
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});let n=0;
 if(PROVAS)fs.mkdirSync(PROVAS,{recursive:true});
 const contexto=async(width,tema)=>{const ctx=await browser.newContext({viewport:{width,height:900},deviceScaleFactor:1,colorScheme:tema});
  if(tema==='dark')await ctx.addInitScript(()=>{try{localStorage.setItem('epi-theme','dark');}catch(e){}});
  await ctx.route('https://pedrohfernandes-klk.github.io/lente/**',async route=>{const u=new URL(route.request().url());const response=await ctx.request.get(origin+u.pathname+u.search);await route.fulfill({response});});
  await ctx.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.abort());return ctx;};
 const pagina=async ctx=>{const page=await ctx.newPage(),erros=[];page.on('pageerror',e=>erros.push(e.message));page.on('response',r=>{if(r.status()>=400&&!/\/pt\//.test(r.url()))erros.push(r.status()+' '+r.url());});return {page,erros};};
 const carregar=f=>f.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>{i.loading='eager';return i.complete?null:new Promise(r=>{i.addEventListener('load',r,{once:true});i.addEventListener('error',r,{once:true});setTimeout(r,10000);});}));});
 const prova=async(page,nome)=>{if(PROVAS){await page.evaluate(()=>{document.activeElement&&document.activeElement.blur();scrollTo(0,0);});await page.mouse.move(0,0);await page.screenshot({path:path.join(PROVAS,nome+'.png'),fullPage:true});}};
 const limpo=(m,rot)=>{assert.equal(m.lado,0,rot+': sem deslize');assert.deepEqual(m.fora,[],rot+': nada fora do ecrã');assert.deepEqual(m.transborda,[],rot+': nada transborda');assert.deepEqual(m.alvos,[],rot+': alvos de 44 px');assert.ok(m.imagens.length>0&&m.imagens.every(Boolean),rot+': imagens carregadas');};
 try{
 for(const width of [320,390,1280])for(const tema of ['light','dark']){
  const esc=tema==='dark'?'escuro':'claro';
  // ---------- a entrada, normal e com ?projetar=1 ----------
  for(const projecao of [false,true]){
   const rot=`entrada, ${width} px, ${esc}${projecao?', projeção':''}`,ctx=await contexto(width,tema),{page,erros}=await pagina(ctx);
   await page.goto(origin+'/lente/'+(projecao?'?projetar=1':''),{waitUntil:'networkidle'});await carregar(page);
   let m=await page.evaluate(geometria);limpo(m,rot);assert.equal(m.tema,tema,rot+': tema');assert.equal(m.imagens.length,4,rot+': quatro imagens');
   assert.equal(await page.evaluate(()=>document.documentElement.classList.contains('em-projecao')),projecao,rot);
   if(width===390&&!projecao)assert.ok(m.altura<3000,rot+': altura '+m.altura+' px, abaixo de 3000');
   // os quatro temas, pela ordem aprovada, e os acessos secundários
   assert.deepEqual(await page.locator('.tm-g>li>article.tm').evaluateAll(es=>es.map(e=>[e.querySelector('.tm-n b').textContent,e.querySelector('.tm-n a').getAttribute('href'),e.querySelector('.tm-n a').textContent,e.querySelector('.tm-q').textContent])),TEMAS,rot);
   assert.deepEqual(await page.locator('.tm-linha-t').allTextContents(),['Ferramentas para trabalhar','A minha aula','Biblioteca','Área do docente'],rot);
   assert.deepEqual(await page.locator('#ferramentas a').allTextContents(),['Ler','Investigar','Escrever','Apresentar','Direitos e fontes'],rot);
   assert.equal(await page.getByText(/[Pp]révia/).count(),0,rot+': sem nota de prévia');
   // o cartão segue o tema: papel claro no claro, escuro no escuro, com contraste de 4,5:1 nos textos
   const cores=await page.locator('.tm-g>li:nth-child(2)>article.tm').evaluate(c=>{const lum=x=>{const v=x.match(/[\d.]+/g).slice(0,3).map(Number).map(y=>{y/=255;return y<=.03928?y/12.92:Math.pow((y+.055)/1.055,2.4);});return .2126*v[0]+.7152*v[1]+.0722*v[2];},f=getComputedStyle(c).backgroundColor,l2=lum(f);return {claro:l2>.5,contraste:[...c.querySelectorAll('.tm-n a,.tm-q,.tm-f')].map(e=>{const l1=lum(getComputedStyle(e).color);return (Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);})};});
   assert.equal(cores.claro,tema==='light',rot+': papel do cartão');assert.ok(cores.contraste.every(c=>c>=4.5),rot+': contraste '+JSON.stringify(cores.contraste));
   if(projecao){
    // na projeção, os textos dos temas e dos acessos ficam no degrau 20 da escala ou acima (a raiz sobe a partir de 768 px)
    const pequenos=await page.evaluate(()=>{const u=parseFloat(getComputedStyle(document.documentElement).fontSize)/16;return [...document.querySelectorAll('[data-cartaz-entrada] :is(.tm-sec,.tm-n,.tm-q,.tm-f,.tm-extra a,.tm-linha-t,.tm-linha-d,.tm-linha a,.pt-f,.pt-a,.cz-footer-links a,.lente-nota)')].filter(e=>parseFloat(getComputedStyle(e).fontSize)<20*u-.05).map(e=>e.className+' '+getComputedStyle(e).fontSize);});
    assert.deepEqual(pequenos,[],rot+': letra de projeção');
   }
   // foco de teclado: todas as ligações e todos os «i» da entrada recebem foco, pela ordem da página, com o foco à vista e no ecrã
   await page.evaluate(()=>scrollTo(0,0));await page.locator('body').click({position:{x:2,y:2}});
   const paragens=(await tabular(page,60)).filter(p=>p.dentro),nomes=paragens.map(p=>p.nome);
   for(const p of paragens){assert.ok(p.anel,rot+': foco sem contorno em '+p.nome);assert.ok(p.noEcra,rot+': foco fora do ecrã em '+p.nome);if(p.contraste!==null)assert.ok(p.contraste>=3,rot+': anel de foco com '+p.contraste+':1 em '+p.nome);}
   {const pt=paragens.filter(p=>p.nome==='https://pedrohfernandes-klk.github.io/pt/');assert.equal(pt.length,1,rot);assert.ok(pt[0].contraste>=3,rot+': anel de «Português e Exames» com '+pt[0].contraste+':1');assert.ok(paragens.filter(p=>p.contraste!==null).length>=17,rot+': anéis medidos');}
   const esperados=['Créditos da imagem: Honoré Daumier',SITIO+'olhar-e-decidir/','Créditos da imagem: Joseph Racknitz','informacao/','Créditos da imagem: Vincent van Gogh',SITIO+'narrativas/','narrativas/ideias/','Créditos da fotografia: Rua da Boavista',SITIO+'cidade/',
    SITIO+'ler/',SITIO+'investigar/',SITIO+'praticar/#escrever',SITIO+'apresentar/',SITIO+'direitos/','cidadania/m1/','cidadania/m2/',SITIO+'biblioteca/','docente/','https://pedrohfernandes-klk.github.io/pt/','caderno/','como/','mapa/'];
   assert.deepEqual(nomes.filter(x=>esperados.includes(x)),esperados,rot+': ordem do foco');
   // cada «i»: o do desenho do cabeçalho e os dos quatro temas
   const is=page.locator('[data-cartaz-entrada] details.info-i');assert.equal(await is.count(),5,rot+': cinco «i»');
   for(let k=1;k<5;k++)await conferirI(page,is.nth(k),`${rot}, «i» do tema ${k}`,k<4);
   await is.nth(1).locator('summary').click();await is.nth(2).locator('summary').click();assert.deepEqual(await is.evaluateAll(es=>es.map(e=>e.open)),[false,false,true,false,false],rot+': um só «i» aberto');
   await page.keyboard.press('Escape');assert.equal(await page.locator('details.info-i[open]').count(),0,rot);
   // a ligação ao Ideias fica por cima da ligação do cartão e abre o Ideias
   const ideias=page.locator('#inicio-narrativas .tm-extra a');await ideias.scrollIntoViewIfNeeded();await ideias.click();await page.waitForURL('**/lente/narrativas/ideias/');
   assert.equal(new URL(page.url()).pathname,'/lente/narrativas/ideias/',rot);await page.goBack({waitUntil:'networkidle'});
   // o cartão inteiro do tema 02 abre a página do tema (clique na pergunta, que não é a ligação)
   m=await page.evaluate(geometria);assert.equal(m.lado,0,rot);
   await prova(page,`entrada-${width}-${esc}${projecao?'-projecao':''}`);
   const pergunta=page.locator('.tm-g>li:nth-child(2) .tm-q');await pergunta.scrollIntoViewIfNeeded();{const b=await pergunta.boundingBox();await page.mouse.click(b.x+b.width/2,b.y+b.height/2);}await page.waitForURL('**/lente/informacao/');
   assert.equal(await page.locator('h1').textContent(),'Porque estás a ver isto?',rot+': o tema 02 abre');
   assert.deepEqual(erros,[],rot+': sem erros');n++;await ctx.close();
  }
  // ---------- a página do tema 02 ----------
  {const rot=`tema 02, ${width} px, ${esc}`,ctx=await contexto(width,tema),{page,erros}=await pagina(ctx);
   await page.goto(origin+'/lente/informacao/',{waitUntil:'networkidle'});await carregar(page);
   let m=await page.evaluate(geometria);limpo(m,rot);assert.equal(m.tema,tema,rot+': tema');
   assert.equal(await page.title(),'Informação e mundo digital · Lente',rot);
   assert.deepEqual(await page.locator('h1,h2').allTextContents(),['Porque estás a ver isto?','A regra do feed','Três páginas que repetem a mesma frase são três confirmações?','Quem está por trás desta página?','Se a conta é grátis, quem paga?','Quando a máquina faz, quem responde?','Contra-feed.','Ver tudo neste tema'],rot);
   assert.equal(await page.getByText(/[Pp]révia/).count(),0,rot+': sem nota de prévia');
   // a pergunta é o maior título da página
   const tamanhos=await page.locator('h1,h2,h3').evaluateAll(es=>es.filter(e=>e.getClientRects().length).map(e=>parseFloat(getComputedStyle(e).fontSize)));assert.ok(tamanhos.slice(1).every(t=>t<tamanhos[0]),rot+': '+tamanhos);
   // fundo da página e blocos seguem o tema
   const fundo=await page.evaluate(()=>{const v=getComputedStyle(document.body).backgroundColor.match(/[\d.]+/g).map(Number);return (v[0]+v[1]+v[2])/3>128;});assert.equal(fundo,tema==='light',rot+': fundo');
   // a atividade que abre o tema
   const botao=page.locator('a.tm-botao');assert.equal(await botao.getAttribute('href'),SITIO+'cidadania/m2/cid-m2-a-regra-do-feed/',rot);assert.ok(await botao.isVisible(),rot);
   // o «i» da gravura
   assert.equal(await page.locator('details.info-i').count(),1,rot);await conferirI(page,page.locator('details.info-i'),rot+', «i»',true);
   // a dobra «Ver tudo neste tema»: fechada ao carregar; abre e fecha por clique, Enter e Espaço
   const dobra=page.locator('details.tm-tudo'),sumario=dobra.locator('summary'),ligacoes=dobra.locator('li a');
   assert.equal(await dobra.evaluate(e=>e.open),false,rot+': dobra fechada ao carregar');assert.equal(await ligacoes.count(),23,rot);assert.ok(!(await ligacoes.first().isVisible()),rot+': fechada, sem ligações à vista');
   await sumario.scrollIntoViewIfNeeded();await sumario.click();assert.equal(await dobra.evaluate(e=>e.open),true,rot+': clique abre');
   assert.deepEqual(await ligacoes.evaluateAll(es=>es.map(e=>e.getClientRects().length>0)),Array(23).fill(true),rot+': 23 ligações à vista');
   m=await page.evaluate(geometria);limpo(m,rot+', dobra aberta');await prova(page,`tema-informacao-${width}-${esc}-tudo-aberto`);
   await sumario.click();assert.equal(await dobra.evaluate(e=>e.open),false,rot+': clique fecha');
   await sumario.focus();await page.keyboard.press('Enter');assert.equal(await dobra.evaluate(e=>e.open),true,rot+': Enter abre');
   await page.keyboard.press(' ');assert.equal(await dobra.evaluate(e=>e.open),false,rot+': Espaço fecha');
   await page.keyboard.press(' ');assert.equal(await dobra.evaluate(e=>e.open),true,rot+': Espaço abre');
   assert.deepEqual(await dobra.locator('h3').allTextContents(),['Casos para decidir','Verificar fontes','Criar e mostrar','Os passos do módulo Algoritmos','Para consultar'],rot);
   // todas as ligações da página respondem (as do Lente, servidas pela cópia de trabalho)
   if(width===390&&tema==='light'){const hrefs=await page.locator('main a[href]').evaluateAll(es=>[...new Set(es.map(e=>e.href))]);assert.ok(hrefs.length>=27,rot+': '+hrefs.length);for(const h of hrefs){if(/commons\.wikimedia\.org|\/projetar\//.test(h))continue;const u=new URL(h),r=await ctx.request.get(origin+u.pathname);assert.equal(r.status(),200,rot+': '+h);}}
   // foco de teclado, com a dobra aberta: todas as ligações recebem foco, à vista e no ecrã
   await page.evaluate(()=>scrollTo(0,0));await page.locator('body').click({position:{x:2,y:2}});
   const paragens=(await tabular(page,60)).filter(p=>p.dentro);for(const p of paragens){assert.ok(p.anel,rot+': foco sem contorno em '+p.nome);assert.ok(p.noEcra,rot+': foco fora do ecrã em '+p.nome);if(p.contraste!==null)assert.ok(p.contraste>=3,rot+': anel de foco com '+p.contraste+':1 em '+p.nome);}
   {const ap=paragens.filter(p=>/\/(projetos|cidadania)\/contra-feed\/$/.test(p.nome)&&p.contraste!==null);assert.ok(ap.length>=2,rot+': anéis de «Para aplicar» medidos');assert.ok(paragens.filter(p=>p.contraste!==null).length>=36,rot+': anéis medidos');}
   // 12/11/2026: revisão. O bloco «Para aplicar» é invertido nos dois modos: título, ponto do título, frase e ligações com 4,5:1 sobre o bloco.
   {const fracos=await page.locator('.tm-aplicar').evaluate(b=>{const lum=x=>{const v=x.match(/[\d.]+/g).slice(0,3).map(Number).map(y=>{y/=255;return y<=.03928?y/12.92:Math.pow((y+.055)/1.055,2.4);});return .2126*v[0]+.7152*v[1]+.0722*v[2];},z=lum(getComputedStyle(b).backgroundColor),es=[...b.querySelectorAll('h2,h2 span,p,a')];if(es.length!==5)return ['peças: '+es.length];return es.map(e=>{const a=lum(getComputedStyle(e).color);return [e.tagName,Math.round((Math.max(a,z)+.05)/(Math.min(a,z)+.05)*100)/100];}).filter(x=>x[1]<4.5).map(String);});assert.deepEqual(fracos,[],rot+': contraste no bloco «Para aplicar»');}
   const comFoco=paragens.map(p=>p.nome),doTema=await page.locator('main :is(a[href],summary)').evaluateAll(es=>es.filter(e=>!e.closest('.info-i-texto')).map(e=>(e.getAttribute('href')||e.getAttribute('aria-label')||e.textContent.trim()).slice(0,90)));
   assert.deepEqual(comFoco.filter(x=>!/^https:\/\/commons/.test(x)),doTema,rot+': ordem do foco');assert.ok(doTema.length>=36,rot+': '+doTema.length);
   // impressão: a dobra sai por extenso, mesmo fechada
   await sumario.click();assert.equal(await dobra.evaluate(e=>e.open),false,rot);await page.emulateMedia({media:'print'});
   assert.deepEqual(await ligacoes.evaluateAll(es=>es.map(e=>e.getClientRects().length>0&&e.checkVisibility({contentVisibilityAuto:true}))),Array(23).fill(true),rot+': impressão com a dobra por extenso');await page.emulateMedia({media:'screen'});
   await prova(page,`tema-informacao-${width}-${esc}`);
   // o regresso aos quatro temas
   const volta=page.locator('.tm-rodape a[href="../"]');await volta.scrollIntoViewIfNeeded();await volta.click();await page.waitForURL(u=>u.pathname==='/lente/');assert.equal(await page.locator('.tm-g>li>article.tm').count(),4,rot+': volta à entrada');
   assert.deepEqual(erros,[],rot+': sem erros');n++;await ctx.close();}
  // ---------- as duas páginas dentro da moldura de projeção, nos três tamanhos ----------
  if(tema==='light')for(const [nome,alvo] of [['entrada','/lente/'],['tema 02','/lente/informacao/']]){
   const ctx=await contexto(width,tema),{page,erros}=await pagina(ctx);
   await page.goto(origin+'/lente/projetar/?pagina='+alvo);await page.frameLocator('#lesson-frame').locator('html.epi-projection').waitFor();
   const frame=await(await page.locator('#lesson-frame').elementHandle()).contentFrame();
   for(const tamanho of ['small','medium','large']){
    const rot=`${nome} na moldura de projeção, ${width} px, letra ${tamanho}`;
    await page.locator('[data-projection-size="'+tamanho+'"]').click();await page.waitForFunction(t=>document.querySelector('[data-projection-size="'+t+'"]').getAttribute('aria-pressed')==='true',tamanho);await page.waitForTimeout(300);await carregar(frame);
    if(nome==='tema 02')await frame.evaluate(()=>{document.querySelector('details.tm-tudo').open=true;});
    const m=await frame.evaluate(geometria);assert.equal(m.lado,0,rot+': sem deslize');assert.deepEqual(m.fora,[],rot+': nada fora da moldura');assert.deepEqual(m.transborda,[],rot+': nada transborda');assert.ok(m.imagens.every(Boolean),rot);
    // nenhuma palavra partida a meio (sem hífen) nos títulos, perguntas e frases
    const partidas=await frame.evaluate(()=>{const out=[];for(const el of document.querySelectorAll('main :is(h1,h2,h3,.tm-q,.tm-f,.tm-n,.tm-ante,.tm-linha-t,.tm-linha-d,.tm-linha a,.tm-abre-t,.tm-comeca p,.tm-alt p,.tm-aplicar p,.tm-aplicar a,.tm-tudo li a,.tm-botao)')){if(!el.offsetParent||getComputedStyle(el).hyphens==='auto')continue;const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let no;while(no=w.nextNode()){const re=/[^\s -]{4,}/g;let x;while(x=re.exec(no.textContent)){const r=document.createRange();r.setStart(no,x.index);r.setEnd(no,x.index+x[0].length);if(new Set([...r.getClientRects()].filter(q=>q.width>0).map(q=>Math.round(q.top))).size>1)out.push(x[0]);}}}return [...new Set(out)];});
    assert.deepEqual(partidas,[],rot+': palavras partidas');
    // na página do tema, nenhum texto abaixo da letra da raiz da moldura
    if(nome==='tema 02'){const pequenos=await frame.evaluate(()=>{const raiz=parseFloat(getComputedStyle(document.documentElement).fontSize);return [...document.querySelectorAll('main *')].filter(e=>e.offsetParent&&!e.closest('.info-i')&&[...e.childNodes].some(x=>x.nodeType===3&&x.textContent.trim())&&parseFloat(getComputedStyle(e).fontSize)<raiz-.05).map(e=>e.className+' '+getComputedStyle(e).fontSize);});assert.deepEqual(pequenos,[],rot+': letra abaixo da raiz');}
    if(PROVAS&&tamanho==='medium')await page.screenshot({path:path.join(PROVAS,(nome==='entrada'?'entrada':'tema-informacao')+`-${width}-moldura.png`),fullPage:true});
   }
   assert.deepEqual(erros,[],nome+' na moldura: sem erros');n++;await ctx.close();
  }
 }
 // sem JavaScript: os quatro temas, os acessos e a dobra da página do tema funcionam como HTML simples
 {const ctx=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}}),p=await ctx.newPage();
  await p.goto(origin+'/lente/');assert.equal(await p.locator('.tm-g>li>article.tm').count(),4);assert.ok(await p.locator('#ferramentas a').first().isVisible());assert.equal(await p.evaluate(()=>Math.max(0,document.documentElement.scrollWidth-innerWidth)),0);
  await p.goto(origin+'/lente/informacao/');assert.ok(await p.locator('h1').isVisible());await p.locator('details.tm-tudo summary').click();assert.ok(await p.locator('details.tm-tudo li a').first().isVisible(),'sem JavaScript, a dobra abre');assert.equal(await p.evaluate(()=>Math.max(0,document.documentElement.scrollWidth-innerWidth)),0);await ctx.close();n++;}
 console.log('Entrada em quatro temas e tema 02: '+n+' contextos (320, 390 e 1280 px, claro e escuro, ?projetar=1, moldura de projeção nos três tamanhos e sem JavaScript): sem deslize, foco de teclado, «i», dobras e ligações verificados.');
 }finally{await browser.close();server.closeAllConnections();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
