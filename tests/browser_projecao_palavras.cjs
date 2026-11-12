// 05/11/2026: revisão de 5/11 (lente-cabecalho-2). Na moldura real de projeção, a entrada do Lente não parte palavras a meio
// sem hífen nem desliza para o lado, de 320 a 1920 px, nos três tamanhos de letra, com o QR aberto (vem assim por omissão).
// 05/11/2026: revisão de 5/11 (lente-cabecalho-3). A partir de 640 px, na moldura e em ?projetar=1, o sobretítulo «EPI, Escola
// Profissional de Imagem» não corre por cima do vidro da lupa, que fica parada a aula inteira.
// 05/11/2026: revisão adversarial. Também 640, 660, 700, 912 e 960 px (molduras de 640 a 767 px), o nome das portas sempre num
// degrau da escala Cartaz e o retrato de Pessoa nunca mais alto do que a moldura. O sobretítulo mede-se quando a moldura
// (e não a janela) tem 640 px ou mais: abaixo disso a entrada é a do telemóvel.
const assert=require('node:assert/strict'),fs=require('fs'),path=require('path'),http=require('http');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..');
const server=http.createServer((q,r)=>{let rel=decodeURIComponent(new URL(q.url,'http://x').pathname.replace(/^\/lente\//,''));if(!rel||rel.endsWith('/'))rel+='index.html';const f=path.resolve(root,rel);if(!f.startsWith(root+path.sep)){r.writeHead(403);return r.end()}try{r.setHeader('content-type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.webp':'image/webp','.json':'application/json','.woff2':'font/woff2'})[path.extname(f)]||'application/octet-stream');r.end(fs.readFileSync(f))}catch{r.writeHead(404);r.end()}});
const TODOS=['small','medium','large'],CASOS=[[320,900,TODOS],[390,900,TODOS],[640,900,TODOS],[660,900,TODOS],[700,900,TODOS],[912,900,TODOS],[960,900,TODOS],[768,1024,TODOS],[1024,768,TODOS],[1280,800,TODOS],[1366,768,TODOS],[1920,1080,TODOS]];
function partidas(){
 // 12/11/2026: pedido entrada-temas. Entram na medição as ligações das linhas dos acessos secundários, a do Ideias e a do Português
 // (os títulos, as perguntas e as frases dos temas já são h2, h3 e p); os seletores antigos ficam, para o que ainda existir.
 const sel='h2,h3,p,small,.lab-set-copy,.sp-copy,.sp-kicker,.sp-image-label,.ld-rot,.cz-button,.cz-footer-links a,.tm-linha a,.tm-extra a,.pt-a',out=[];
 for(const el of document.querySelectorAll('[data-cartaz-entrada] :is('+sel+')')){
  // 07/11/2026: decisões 153, 176 e 177, o texto de um «i» fechado não se vê e não se mede aqui; cada «i» mede-se aberto, em partidasNosI.
  if(!el.offsetParent||getComputedStyle(el).hyphens==='auto'||!el.checkVisibility({contentVisibilityAuto:true}))continue;
  const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let n;
  while(n=w.nextNode()){const re=/[^\s ]{4,}/g;let m;while(m=re.exec(n.textContent)){const r=document.createRange();r.setStart(n,m.index);r.setEnd(n,m.index+m[0].length);const tops=new Set([...r.getClientRects()].filter(x=>x.width>0).map(x=>Math.round(x.top)));if(tops.size>1)out.push(m[0])}}
 }
 // 05/11/2026: revisão adversarial. O nome das portas fica num degrau da escala Cartaz (t25, t31, t39) e o retrato de Pessoa cabe na moldura.
 // 12/11/2026: pedido entrada-temas. As duas portas deram lugar a quatro temas: mede-se a pergunta de cada tema (.tm-q), que na
 // projeção desce pelos degraus t39, t31, t25 e t20 da escala Cartaz, e exige-se que as quatro se meçam; em vez do retrato de Pessoa,
 // que saiu, nenhuma das quatro imagens dos temas pode ser mais alta do que a moldura, e têm de estar as quatro à vista.
 const raiz=parseFloat(getComputedStyle(document.documentElement).fontSize),degraus=[1.25,1.5625,1.9375,2.4375].map(k=>k*raiz);
 const perguntas=[...document.querySelectorAll('[data-cartaz-entrada] .tm-q')].filter(h=>h.offsetParent);
 const foraDaEscala=perguntas.map(h=>parseFloat(getComputedStyle(h).fontSize)).filter(fs=>!degraus.some(d=>Math.abs(d-fs)<.2));
 if(perguntas.length!==4)foraDaEscala.push('perguntas à vista: '+perguntas.length);
 const imgs=[...document.querySelectorAll('[data-cartaz-entrada] .tm-img')].filter(e=>e.offsetParent),retratoAlto=imgs.length===4?Math.max(...imgs.map(img=>Math.round(img.getBoundingClientRect().height-innerHeight))):1;
 return {partidas:[...new Set(out)],desliza:document.documentElement.scrollWidth-innerWidth,foraDaEscala,retratoAlto};
}
// 07/11/2026: decisões 153, 176 e 177. Os créditos passaram para o «i»: abre-se cada «i» à vista, um de cada vez, e o crédito aberto
// também não pode ter palavras partidas sem hífen nem fazer deslizar a página.
function partidasNosI(){
 const out=[];let desliza=0;
 for(const d of document.querySelectorAll('[data-cartaz-entrada] details.info-i')){
  if(!d.querySelector('summary').offsetParent)continue;
  d.open=true;const r=partidas();out.push(...r.partidas);desliza=Math.max(desliza,r.desliza);d.open=false;
 }
 return {partidas:[...new Set(out)],desliza};
}
function etqNoVidro(){
 const aro=document.querySelector('.lf-borda'),etq=document.querySelector('.lente-cab>.lente-etq');if(!aro||!etq)return -1;
 const A=aro.getBoundingClientRect(),cx=A.left+A.width/2,cy=A.top+A.height/2,r=A.width/2,rg=document.createRange();rg.selectNodeContents(etq);let dentro=0;
 for(const x of rg.getClientRects())for(let i=0;i<20;i++)for(let j=0;j<6;j++){const px=x.left+x.width*(i+.5)/20,py=x.top+x.height*(j+.5)/6;if((px-cx)**2+(py-cy)**2<=r*r)dentro++}
 return dentro;
}
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port,b=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});let falhas=[];
try{for(const [w,h,tamanhos] of CASOS)for(const t of tamanhos){
  const ctx=await b.newContext({viewport:{width:w,height:h}});await ctx.route('**/*',r=>{const u=new URL(r.request().url());return u.origin===base?r.continue():r.abort()});const p=await ctx.newPage();
  await p.goto(base+'/lente/projetar/?pagina=/lente/');await p.frameLocator('#lesson-frame').locator('html.epi-projection').waitFor();
  await p.locator('[data-projection-size="'+t+'"]').click();await p.waitForFunction(t=>document.querySelector('[data-projection-size="'+t+'"]').getAttribute('aria-pressed')==='true',t);await p.waitForTimeout(400);
  const frame=await(await p.locator('#lesson-frame').elementHandle()).contentFrame();await frame.evaluate(()=>document.fonts.ready);
  const m=await frame.evaluate(partidas);if(await frame.evaluate(()=>innerWidth>=640)){m.etq=await frame.evaluate(etqNoVidro);if(m.etq!==0)falhas.push({w,h,t,etqNoVidro:m.etq})}m.raiz=await frame.evaluate(()=>getComputedStyle(document.documentElement).fontSize);const mi=await frame.evaluate(`(()=>{${partidas.toString()};${partidasNosI.toString()};return partidasNosI();})()`);if(mi.partidas.length||mi.desliza>0)falhas.push({w,h,t,i:mi});if(m.partidas.length||m.desliza>0||m.foraDaEscala.length||m.retratoAlto>0)falhas.push({w,h,t,...m});console.log(w+'x'+h,t,m.raiz,m.partidas.length,'partidas; desliza',m.desliza);await ctx.close();
 }
 for(const w of [768,1024,1366]){const ctx=await b.newContext({viewport:{width:w,height:900},reducedMotion:'reduce'});await ctx.route('**/*',r=>{const u=new URL(r.request().url());return u.origin===base?r.continue():r.abort()});const p=await ctx.newPage();await p.goto(base+'/lente/?projetar=1');await p.evaluate(()=>document.fonts.ready);const n=await p.evaluate(etqNoVidro);console.log('?projetar=1',w,'sobretítulo no vidro',n);if(n!==0)falhas.push({w,modo:'?projetar=1',etqNoVidro:n});await ctx.close()}
 assert.deepEqual(falhas,[],JSON.stringify(falhas));console.log('PASS projeção: nenhuma palavra partida sem hífen, nenhum deslize lateral e, a partir de 640 px, o sobretítulo fora do vidro da lupa');
}finally{await b.close();server.close()}})().catch(e=>{console.error(e.message.slice(0,1500));process.exitCode=1});
