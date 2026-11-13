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
// 13/11/2026: pedido temas-01-03-04. Os temas 01, 03 e 04 têm página própria (justica-e-vida-em-comum/, historias-e-criacao/ e
// imagem-som-e-cidade/) e os cartões da entrada abrem-nas. Tudo o que se media na página do tema 02 mede-se nas quatro, pela tabela PAGINAS
// (títulos, atividade que abre, «i», dobra com todas as ligações à vista e a responder, foco, contraste, impressão, regresso, moldura de
// projeção e sem JavaScript); mede-se também a 768 px; na entrada, cada um dos quatro cartões abre a sua página, e o cartão do tema 03
// conserva, à vista, a ligação ao Laboratório (o destino antigo) e a do Ideias.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),PROVAS=process.env.ENTRADA_TEMAS_PROVAS,SITIO='https://pedrohfernandes-klk.github.io/lente/';
const TIPOS={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.webp':'image/webp','.jpg':'image/jpeg','.png':'image/png'};
const server=http.createServer((req,res)=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname).replace(/^\/lente/,''));if(!f.startsWith(root+path.sep)&&f!==root){res.writeHead(403);return res.end();}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',TIPOS[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});
// 13/11/2026: os quatro cartões abrem a página do seu tema (antes, só o do tema 02).
const TEMAS=[['01','justica-e-vida-em-comum/','Justiça e vida em comum','Uma regra igual é sempre justa?'],['02','informacao/','Informação e mundo digital','Porque estás a ver isto?'],['03','historias-e-criacao/','Histórias e criação','O que transforma uma ideia numa história?'],['04','imagem-som-e-cidade/','Imagem, som e cidade','O que muda quando mudas o enquadramento?']];
// 13/11/2026: o que cada página de tema mostra: títulos h2 pela ordem (atividade, quatro alternativas, bloco para aplicar), destino do botão,
// ligações de «Para aplicar», grupos e número de ligações de «Ver tudo neste tema», a primeira dessas ligações (nos temas 01, 03 e 04, o
// destino antigo do cartão) e se o crédito da imagem tem ligação à fonte.
// 13/11/2026 (revisão): no tema 03, o botão abre a experiência (oficina-ficcao-comecar-imprimir/), que entra também em «Ver tudo» (31 ligações);
// duas alternativas mudam de pergunta para a que a página ligada faz.
// 13/11/2026 (decisão do docente): no tema 03, a 4.ª alternativa passa a ser «As ideias caem do céu?» e abre narrativas/ideias/sessao-01/; confere-se
// o destino da 4.ª alternativa, que responde 200, e que a pergunta se lê na sessão 1 aberta no navegador (é o terceiro cartão: dois «Seguinte»).
const PAGINAS={
 '01':{h2:['Quem fica com o quê?','O elétrico não trava: desvias ou segues em frente?','Quando é que um grupo pode decidir sobre alguém que não está na sala?','Uma proposta é aberta a todos quando nem todos conseguem participar?','Que data funda uma democracia?','Pergunta Humana.'],botao:'olhar-e-decidir/justica/aplicar/',aplicar:['cidadania/projeto/','etica-grelha/'],grupos:['Justiça, com Michael Sandel','As lições 4 a 13','Casos para decidir','Ética','Os passos do módulo Humanos','Criar e mostrar','Para consultar'],tudo:41,primeira:['olhar-e-decidir/','Dilemas'],fonte:true},
 '02':{h2:['A regra do feed','Três páginas que repetem a mesma frase são três confirmações?','Quem está por trás desta página?','Se a conta é grátis, quem paga?','Quando a máquina faz, quem responde?','Contra-feed.'],botao:'cidadania/m2/cid-m2-a-regra-do-feed/',aplicar:['projetos/contra-feed/','cidadania/contra-feed/'],grupos:['Casos para decidir','Verificar fontes','Criar e mostrar','Os passos do módulo Algoritmos','Para consultar'],tudo:23,primeira:['cidadania/m2/cid-m2-a-regra-do-feed/','A regra do feed'],fonte:true},
 '03':{h2:['Uma chave na mesa','Que contradição dá começo a uma história?','Que plano liga uma perda a uma devolução?','O que muda numa frase quando sabes mais?','As ideias caem do céu?','Do conto à prancha.'],botao:'narrativas/oficina-ficcao-comecar-imprimir/',aplicar:['projetos/prancha/','narrativas/proposta-subtexto/'],grupos:['O Laboratório','Ideias','Observar','Treinar','Criar','Montar e comparar','Criar e mostrar'],tudo:31,primeira:['narrativas/','Laboratório'],fonte:true},
 '04':{h2:['Enquadrar a Boavista','O que ouves numa rua quando fechas os olhos?','Porque é que um prédio te parece mais bonito do que os outros?','Quanto da nossa interpretação vem da imagem e quanto vem da legenda?','O que é que a fachada quer de ti?','A cidade em voz e luz.'],botao:'cidade/m17/',aplicar:['projetos/cidade/','projetos/geometria/'],grupos:['Ler a cidade','As 14 missões de Ler a cidade','Olhar e julgar','A escola na cidade','Oficinas de imagem, no Laboratório','Criar e mostrar'],tudo:32,primeira:['cidade/','Ler a cidade'],fonte:false}};
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
 // 13/11/2026: mede-se também a 768 px.
 for(const width of [320,390,768,1280])for(const tema of ['light','dark']){
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
   {const pt=paragens.filter(p=>p.nome==='https://pedrohfernandes-klk.github.io/pt/');assert.equal(pt.length,1,rot);assert.ok(pt[0].contraste>=3,rot+': anel de «Português e Exames» com '+pt[0].contraste+':1');assert.ok(paragens.filter(p=>p.contraste!==null).length>=18,rot+': anéis medidos');}
   // 13/11/2026: os cartões 01, 03 e 04 abrem a página do tema; no cartão 03, o Laboratório vem antes do Ideias.
   const esperados=['Créditos da imagem: Honoré Daumier','justica-e-vida-em-comum/','Créditos da imagem: Joseph Racknitz','informacao/','Créditos da imagem: Vincent van Gogh','historias-e-criacao/',SITIO+'narrativas/','narrativas/ideias/','Créditos da fotografia: Rua da Boavista','imagem-som-e-cidade/',
    SITIO+'ler/',SITIO+'investigar/',SITIO+'praticar/#escrever',SITIO+'apresentar/',SITIO+'direitos/','cidadania/m1/','cidadania/m2/',SITIO+'biblioteca/','docente/','https://pedrohfernandes-klk.github.io/pt/','caderno/','como/','mapa/'];
   assert.deepEqual(nomes.filter(x=>esperados.includes(x)),esperados,rot+': ordem do foco');
   // cada «i»: o do desenho do cabeçalho e os dos quatro temas
   const is=page.locator('[data-cartaz-entrada] details.info-i');assert.equal(await is.count(),5,rot+': cinco «i»');
   for(let k=1;k<5;k++)await conferirI(page,is.nth(k),`${rot}, «i» do tema ${k}`,k<4);
   await is.nth(1).locator('summary').click();await is.nth(2).locator('summary').click();assert.deepEqual(await is.evaluateAll(es=>es.map(e=>e.open)),[false,false,true,false,false],rot+': um só «i» aberto');
   await page.keyboard.press('Escape');assert.equal(await page.locator('details.info-i[open]').count(),0,rot);
   // a ligação ao Ideias fica por cima da ligação do cartão e abre o Ideias
   // 13/11/2026: o cartão tem agora duas ligações por cima da do título: a do Ideias, escolhida pelo seu destino, e a do Laboratório, que
   // abre o Laboratório; cada uma existe uma só vez e fica à vista.
   assert.deepEqual(await page.locator('#inicio-narrativas .tm-extra a').evaluateAll(es=>es.map(e=>[e.getAttribute('href'),e.textContent])),[[SITIO+'narrativas/','Laboratório'],['narrativas/ideias/','Ideias: o método em cinco passos']],rot);
   const ideias=page.locator('#inicio-narrativas .tm-extra a[href="narrativas/ideias/"]');await ideias.scrollIntoViewIfNeeded();assert.ok(await ideias.isVisible(),rot);await ideias.click();await page.waitForURL('**/lente/narrativas/ideias/');
   assert.equal(new URL(page.url()).pathname,'/lente/narrativas/ideias/',rot);await page.goBack({waitUntil:'networkidle'});
   const lab=page.locator('#inicio-narrativas .tm-extra a[href="'+SITIO+'narrativas/"]');await lab.scrollIntoViewIfNeeded();assert.ok(await lab.isVisible(),rot);await lab.click();await page.waitForURL(u=>u.pathname==='/lente/narrativas/');await page.goBack({waitUntil:'networkidle'});
   // o cartão inteiro do tema 02 abre a página do tema (clique na pergunta, que não é a ligação)
   m=await page.evaluate(geometria);assert.equal(m.lado,0,rot);
   await prova(page,`entrada-${width}-${esc}${projecao?'-projecao':''}`);
   // 13/11/2026: o mesmo para os quatro cartões: cada um abre a página do seu tema, com a pergunta do cartão como título.
   for(let k=0;k<4;k++){const pergunta=page.locator('.tm-g>li:nth-child('+(k+1)+') .tm-q');await pergunta.scrollIntoViewIfNeeded();{const b=await pergunta.boundingBox();await page.mouse.click(b.x+b.width/2,b.y+b.height/2);}await page.waitForURL('**/lente/'+TEMAS[k][1]);
    assert.equal(await page.locator('h1').textContent(),TEMAS[k][3],rot+': o tema '+TEMAS[k][0]+' abre');if(k<3)await page.goBack({waitUntil:'networkidle'});}
   assert.deepEqual(erros,[],rot+': sem erros');n++;await ctx.close();
  }
  // ---------- as quatro páginas de tema ----------
  // 13/11/2026: era só a página do tema 02; o mesmo bloco corre agora para as quatro, com os valores de cada uma (PAGINAS).
  for(const [num,pasta,nomeTema,perguntaTema] of TEMAS){const P=PAGINAS[num],rot=`tema ${num}, ${width} px, ${esc}`,ctx=await contexto(width,tema),{page,erros}=await pagina(ctx);
   await page.goto(origin+'/lente/'+pasta,{waitUntil:'networkidle'});await carregar(page);
   let m=await page.evaluate(geometria);limpo(m,rot);assert.equal(m.tema,tema,rot+': tema');
   assert.equal(await page.title(),nomeTema+' · Lente',rot);assert.equal(m.imagens.length,1,rot+': uma imagem');
   assert.deepEqual(await page.locator('h1,h2').allTextContents(),[perguntaTema,...P.h2,'Ver tudo neste tema'],rot);
   assert.equal(await page.getByText(/[Pp]révia/).count(),0,rot+': sem nota de prévia');
   // a pergunta é o maior título da página
   const tamanhos=await page.locator('h1,h2,h3').evaluateAll(es=>es.filter(e=>e.getClientRects().length).map(e=>parseFloat(getComputedStyle(e).fontSize)));assert.ok(tamanhos.slice(1).every(t=>t<tamanhos[0]),rot+': '+tamanhos);
   // fundo da página e blocos seguem o tema
   const fundo=await page.evaluate(()=>{const v=getComputedStyle(document.body).backgroundColor.match(/[\d.]+/g).map(Number);return (v[0]+v[1]+v[2])/3>128;});assert.equal(fundo,tema==='light',rot+': fundo');
   // a atividade que abre o tema
   const botao=page.locator('a.tm-botao');assert.equal(await botao.getAttribute('href'),SITIO+P.botao,rot);assert.ok(await botao.isVisible(),rot);
   // o «i» da gravura
   assert.equal(await page.locator('details.info-i').count(),1,rot);await conferirI(page,page.locator('details.info-i'),rot+', «i»',P.fonte);
   // a dobra «Ver tudo neste tema»: fechada ao carregar; abre e fecha por clique, Enter e Espaço
   const dobra=page.locator('details.tm-tudo'),sumario=dobra.locator('summary'),ligacoes=dobra.locator('li a');
   assert.equal(await dobra.evaluate(e=>e.open),false,rot+': dobra fechada ao carregar');assert.equal(await ligacoes.count(),P.tudo,rot);
   // 13/11/2026: a primeira ligação da dobra (nos temas 01, 03 e 04, o destino que o cartão tinha na entrada)
   assert.deepEqual(await ligacoes.first().evaluate(e=>[e.getAttribute('href'),e.textContent]),[SITIO+P.primeira[0],P.primeira[1]],rot+': primeira ligação de «Ver tudo»');assert.ok(!(await ligacoes.first().isVisible()),rot+': fechada, sem ligações à vista');
   await sumario.scrollIntoViewIfNeeded();await sumario.click();assert.equal(await dobra.evaluate(e=>e.open),true,rot+': clique abre');
   assert.deepEqual(await ligacoes.evaluateAll(es=>es.map(e=>e.getClientRects().length>0)),Array(P.tudo).fill(true),rot+': '+P.tudo+' ligações à vista');
   m=await page.evaluate(geometria);limpo(m,rot+', dobra aberta');await prova(page,`tema-${pasta.slice(0,-1)}-${width}-${esc}-tudo-aberto`);
   await sumario.click();assert.equal(await dobra.evaluate(e=>e.open),false,rot+': clique fecha');
   await sumario.focus();await page.keyboard.press('Enter');assert.equal(await dobra.evaluate(e=>e.open),true,rot+': Enter abre');
   await page.keyboard.press(' ');assert.equal(await dobra.evaluate(e=>e.open),false,rot+': Espaço fecha');
   await page.keyboard.press(' ');assert.equal(await dobra.evaluate(e=>e.open),true,rot+': Espaço abre');
   assert.deepEqual(await dobra.locator('h3').allTextContents(),P.grupos,rot);
   // todas as ligações da página respondem (as do Lente, servidas pela cópia de trabalho)
   if(width===390&&tema==='light'){const hrefs=await page.locator('main a[href]').evaluateAll(es=>[...new Set(es.map(e=>e.href))]);assert.ok(hrefs.length>=P.tudo+4,rot+': '+hrefs.length);for(const h of hrefs){if(/commons\.wikimedia\.org|\/projetar\//.test(h))continue;const u=new URL(h),r=await ctx.request.get(origin+u.pathname);assert.equal(r.status(),200,rot+': '+h);}}
   // 13/11/2026 (decisão do docente): a 4.ª alternativa do tema 03 abre a sessão 1 de Ideias; o destino responde 200 e a pergunta do cartão lê-se lá,
   // à vista, no terceiro cartão da sessão (dois «Seguinte»), e está no ficheiro servido letra a letra.
   if(num==='03'){const alt=await page.locator('.tm-alt h2 a').evaluateAll(es=>es.map(e=>[e.getAttribute('href'),e.textContent]));assert.equal(alt.length,4,rot);assert.deepEqual(alt[3],[SITIO+'narrativas/ideias/sessao-01/','As ideias caem do céu?'],rot+': 4.ª alternativa');
    assert.equal(await dobra.locator('li a[href="'+alt[3][0]+'"]').count(),1,rot+': a sessão 1 está em «Ver tudo»');
    if(width===390&&tema==='light'){const r=await ctx.request.get(origin+new URL(alt[3][0]).pathname);assert.equal(r.status(),200,rot+': '+alt[3][0]);assert.ok((await r.text()).includes('<p>As ideias caem do céu?<\\/p>'),rot+': a pergunta no ficheiro da sessão 1');
     const s1=await ctx.newPage(),e1=[];s1.on('pageerror',e=>e1.push(e.message));await s1.goto(alt[3][0],{waitUntil:'networkidle'});assert.equal(new URL(s1.url()).pathname,'/lente/narrativas/ideias/sessao-01/',rot);
     const perg=s1.getByText('As ideias caem do céu?',{exact:true});for(let k=0;k<2;k++){await s1.locator('button.c-prim:visible').first().click();await s1.waitForTimeout(400);}
     assert.equal(await perg.count(),1,rot+': a pergunta na sessão 1');assert.ok(await perg.isVisible(),rot+': a pergunta à vista na sessão 1');assert.deepEqual(e1,[],rot+': sessão 1 sem erros');await s1.close();}}
   // foco de teclado, com a dobra aberta: todas as ligações recebem foco, à vista e no ecrã
   await page.evaluate(()=>scrollTo(0,0));await page.locator('body').click({position:{x:2,y:2}});
   const paragens=(await tabular(page,90)).filter(p=>p.dentro);for(const p of paragens){assert.ok(p.anel,rot+': foco sem contorno em '+p.nome);assert.ok(p.noEcra,rot+': foco fora do ecrã em '+p.nome);if(p.contraste!==null)assert.ok(p.contraste>=3,rot+': anel de foco com '+p.contraste+':1 em '+p.nome);}
   {const ap=paragens.filter(p=>P.aplicar.some(x=>p.nome===SITIO+x)&&p.contraste!==null);assert.ok(ap.length>=2,rot+': anéis de «Para aplicar» medidos');assert.ok(paragens.filter(p=>p.contraste!==null).length>=P.tudo+13,rot+': anéis medidos');}
   // 12/11/2026: revisão. O bloco «Para aplicar» é invertido nos dois modos: título, ponto do título, frase e ligações com 4,5:1 sobre o bloco.
   {const fracos=await page.locator('.tm-aplicar').evaluate(b=>{const lum=x=>{const v=x.match(/[\d.]+/g).slice(0,3).map(Number).map(y=>{y/=255;return y<=.03928?y/12.92:Math.pow((y+.055)/1.055,2.4);});return .2126*v[0]+.7152*v[1]+.0722*v[2];},z=lum(getComputedStyle(b).backgroundColor),es=[...b.querySelectorAll('h2,h2 span,p,a')];if(es.length!==5)return ['peças: '+es.length];return es.map(e=>{const a=lum(getComputedStyle(e).color);return [e.tagName,Math.round((Math.max(a,z)+.05)/(Math.min(a,z)+.05)*100)/100];}).filter(x=>x[1]<4.5).map(String);});assert.deepEqual(fracos,[],rot+': contraste no bloco «Para aplicar»');}
   const comFoco=paragens.map(p=>p.nome),doTema=await page.locator('main :is(a[href],summary)').evaluateAll(es=>es.filter(e=>!e.closest('.info-i-texto')).map(e=>(e.getAttribute('href')||e.getAttribute('aria-label')||e.textContent.trim()).slice(0,90)));
   assert.deepEqual(comFoco.filter(x=>!/^https:\/\/commons/.test(x)),doTema,rot+': ordem do foco');assert.equal(doTema.length,P.tudo+14,rot+': '+doTema.length);
   // impressão: a dobra sai por extenso, mesmo fechada
   await sumario.click();assert.equal(await dobra.evaluate(e=>e.open),false,rot);await page.emulateMedia({media:'print'});
   assert.deepEqual(await ligacoes.evaluateAll(es=>es.map(e=>e.getClientRects().length>0&&e.checkVisibility({contentVisibilityAuto:true}))),Array(P.tudo).fill(true),rot+': impressão com a dobra por extenso');await page.emulateMedia({media:'screen'});
   await prova(page,`tema-${pasta.slice(0,-1)}-${width}-${esc}`);
   // o regresso aos quatro temas
   const volta=page.locator('.tm-rodape a[href="../"]');await volta.scrollIntoViewIfNeeded();await volta.click();await page.waitForURL(u=>u.pathname==='/lente/');assert.equal(await page.locator('.tm-g>li>article.tm').count(),4,rot+': volta à entrada');
   assert.deepEqual(erros,[],rot+': sem erros');n++;await ctx.close();}
  // ---------- a entrada e as quatro páginas de tema dentro da moldura de projeção, nos três tamanhos ----------
  // 13/11/2026: eram a entrada e a página do tema 02; entram as páginas dos temas 01, 03 e 04, com as mesmas medições.
  if(tema==='light')for(const [nome,alvo] of [['entrada','/lente/'],...TEMAS.map(t=>['tema '+t[0],'/lente/'+t[1]])]){
   const ctx=await contexto(width,tema),{page,erros}=await pagina(ctx);
   await page.goto(origin+'/lente/projetar/?pagina='+alvo);await page.frameLocator('#lesson-frame').locator('html.epi-projection').waitFor();
   const frame=await(await page.locator('#lesson-frame').elementHandle()).contentFrame();
   for(const tamanho of ['small','medium','large']){
    const rot=`${nome} na moldura de projeção, ${width} px, letra ${tamanho}`;
    await page.locator('[data-projection-size="'+tamanho+'"]').click();await page.waitForFunction(t=>document.querySelector('[data-projection-size="'+t+'"]').getAttribute('aria-pressed')==='true',tamanho);await page.waitForTimeout(300);await carregar(frame);
    if(nome!=='entrada')await frame.evaluate(()=>{document.querySelector('details.tm-tudo').open=true;});
    const m=await frame.evaluate(geometria);assert.equal(m.lado,0,rot+': sem deslize');assert.deepEqual(m.fora,[],rot+': nada fora da moldura');assert.deepEqual(m.transborda,[],rot+': nada transborda');assert.ok(m.imagens.every(Boolean),rot);
    // nenhuma palavra partida a meio (sem hífen) nos títulos, perguntas e frases
    const partidas=await frame.evaluate(()=>{const out=[];for(const el of document.querySelectorAll('main :is(h1,h2,h3,.tm-q,.tm-f,.tm-n,.tm-ante,.tm-linha-t,.tm-linha-d,.tm-linha a,.tm-abre-t,.tm-comeca p,.tm-alt p,.tm-aplicar p,.tm-aplicar a,.tm-tudo li a,.tm-botao)')){if(!el.offsetParent||getComputedStyle(el).hyphens==='auto')continue;const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let no;while(no=w.nextNode()){const re=/[^\s -]{4,}/g;let x;while(x=re.exec(no.textContent)){const r=document.createRange();r.setStart(no,x.index);r.setEnd(no,x.index+x[0].length);if(new Set([...r.getClientRects()].filter(q=>q.width>0).map(q=>Math.round(q.top))).size>1)out.push(x[0]);}}}return [...new Set(out)];});
    assert.deepEqual(partidas,[],rot+': palavras partidas');
    // na página do tema, nenhum texto abaixo da letra da raiz da moldura
    if(nome!=='entrada'){const pequenos=await frame.evaluate(()=>{const raiz=parseFloat(getComputedStyle(document.documentElement).fontSize);return [...document.querySelectorAll('main *')].filter(e=>e.offsetParent&&!e.closest('.info-i')&&[...e.childNodes].some(x=>x.nodeType===3&&x.textContent.trim())&&parseFloat(getComputedStyle(e).fontSize)<raiz-.05).map(e=>e.className+' '+getComputedStyle(e).fontSize);});assert.deepEqual(pequenos,[],rot+': letra abaixo da raiz');}
    if(PROVAS&&tamanho==='medium')await page.screenshot({path:path.join(PROVAS,(nome==='entrada'?'entrada':'tema-'+alvo.split('/')[2])+`-${width}-moldura.png`),fullPage:true});
   }
   assert.deepEqual(erros,[],nome+' na moldura: sem erros');n++;await ctx.close();
  }
 }
 // sem JavaScript: os quatro temas, os acessos e a dobra da página do tema funcionam como HTML simples
 {const ctx=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}}),p=await ctx.newPage();
  await p.goto(origin+'/lente/');assert.equal(await p.locator('.tm-g>li>article.tm').count(),4);assert.ok(await p.locator('#ferramentas a').first().isVisible());assert.equal(await p.evaluate(()=>Math.max(0,document.documentElement.scrollWidth-innerWidth)),0);
  // 13/11/2026: o mesmo nas quatro páginas de tema.
  for(const t of TEMAS){await p.goto(origin+'/lente/'+t[1]);assert.ok(await p.locator('h1').isVisible());assert.equal(await p.locator('h1').textContent(),t[3]);await p.locator('details.tm-tudo summary').click();assert.ok(await p.locator('details.tm-tudo li a').first().isVisible(),'sem JavaScript, a dobra abre');assert.equal(await p.evaluate(()=>Math.max(0,document.documentElement.scrollWidth-innerWidth)),0);}await ctx.close();n++;}
 // 13/11/2026 (revisão): a pergunta do tema (h1) mede o mesmo que no main nas páginas dos temas 01, 02 e 03, clamp(2,4375rem; 9,5vw; 3,8125rem):
 // 39 px a 320 px e 61 px a 860 px. Só a do tema 04 encolhe, e só onde «enquadramento?» não cabia (a do tema 03 só encolhe em projeção, medida acima na moldura); em nenhuma das quatro uma palavra
 // fica partida em duas linhas. Mede-se também a 360, 960 e 1024 px, onde a folha partilhada tinha mudado a página do tema 02 sem aviso.
 for(const width of [320,360,390,768,860,960,1024,1280]){const ctx=await contexto(width,'light'),{page,erros}=await pagina(ctx);
  for(const [num,pasta] of TEMAS){const rot=`pergunta do tema ${num}, ${width} px`;
   await page.goto(origin+'/lente/'+pasta,{waitUntil:'networkidle'});await carregar(page);
   const h=await page.locator('h1.tm-perg').evaluate(el=>{const raiz=parseFloat(getComputedStyle(document.documentElement).fontSize),partidas=[];
    const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let no;while(no=w.nextNode()){const re=/\S+/g;let x;while(x=re.exec(no.textContent)){const r=document.createRange();r.setStart(no,x.index);r.setEnd(no,x.index+x[0].length);if(new Set([...r.getClientRects()].filter(q=>q.width>0).map(q=>Math.round(q.top))).size>1)partidas.push(x[0]);}}
    return {raiz,letra:parseFloat(getComputedStyle(el).fontSize),partidas,cabe:el.scrollWidth<=el.clientWidth+1};});
   const antes=Math.min(3.8125*h.raiz,Math.max(2.4375*h.raiz,.095*width));
   assert.deepEqual(h.partidas,[],rot+': palavra partida');assert.ok(h.cabe,rot+': transborda');
   if(num==='04'){assert.ok(h.letra<=antes+.01&&h.letra>=30,rot+': '+h.letra);if([390,768,1280].includes(width))assert.ok(Math.abs(h.letra-antes)<.01,rot+': '+h.letra+' em vez de '+antes);}
   else assert.ok(Math.abs(h.letra-antes)<.01,rot+': '+h.letra+' em vez de '+antes);
   if(num==='02'&&width===320)assert.ok(Math.abs(h.letra-39)<.01,rot+': '+h.letra);
   if(num==='02'&&width===860)assert.ok(Math.abs(h.letra-61)<.01,rot+': '+h.letra);}
  assert.deepEqual(erros,[],'pergunta do tema, '+width+' px: sem erros');n++;await ctx.close();}
 console.log('Entrada em quatro temas e páginas dos quatro temas: '+n+' contextos (320, 390, 768 e 1280 px, claro e escuro, ?projetar=1, moldura de projeção nos três tamanhos sem JavaScript e a letra da pergunta do tema de 320 a 1280 px): sem deslize, foco de teclado, «i», dobras e ligações verificados.');
 }finally{await browser.close();server.closeAllConnections();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
