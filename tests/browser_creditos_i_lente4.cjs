// 08/11/2026: decisões 153 e 176 (pedido lente-4 do plano plano-creditos-i-20261105.md, secção 1, a peça «i»). Duas partes:
// 1. O «i» das missões de «Ler a cidade», nos cartões da página e na gaveta de um lugar (que copia os cartões), a 320, 390, 768 e
//    1280 px, em claro e em escuro: fechado ao carregar, alvo de 44 px no canto de baixo do cartão, fora da ligação e sem tapar o texto
//    do cartão; abre e fecha por clique, abre com Enter e fecha com Escape (o foco volta ao «i»; na gaveta, o Escape fecha primeiro o
//    «i» e só o seguinte fecha a gaveta); um clique fora fecha; tocar no «i» não segue a ligação do cartão; aberto, leva o crédito de
//    antes (o mesmo texto, com a ligação para a fonte e a da licença), lê-se (4,5:1) e não sai do ecrã; a página não desliza para o
//    lado; o filtro das portas esconde o cartão com o seu «i»; na impressão, o «i» não sai e o crédito sai por baixo do cartão.
// 2. O «i» na projeção, nos três modos (em-projecao, na entrada com ?projetar=1; epi-projection, na moldura de /projetar/; e
//    data-cz-projection), em claro e em escuro: o círculo vê-se fechado e aberto, com 3:1 ou mais contra o que o rodeia, medido nos
//    píxeis da página (o pior píxel à volta do círculo, ou a fronteira do halo, do anel ou do fundo do próprio círculo), e o foco vê-se
//    (em cada um de 72 raios, o anel de foco muda o píxel com 3:1 ou mais, ou tem 3:1 ou mais contra o que lhe fica colado). Fora da
//    projeção, o «i» continua como era (fundo, halo e borda de 2 px).
const fs=require('fs'),path=require('path'),http=require('http'),zlib=require('zlib'),assert=require('node:assert/strict'),{execFileSync}=require('child_process');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),BASE='e0c55dec56c9926c89da4382b519b7a4123f3f90';
const antigo=p=>execFileSync('git',['show',BASE+':'+p],{cwd:root,encoding:'utf8',maxBuffer:1<<28});
const ent=s=>String(s).replace(/&amp;/g,'&').replace(/&nbsp;/g,'\u00a0');
const norm=s=>ent(String(s).replace(/<[^>]+>/g,'')).replace(/\s+/g,' ').trim();
// Os créditos de antes (span.cr, dentro da ligação de cada cartão), por missão.
const CR=Object.fromEntries([...antigo('cidade/index.html').matchAll(/<a class="missao p-cartao" href="(m\d\d)\/"[^>]*>(?:(?!<\/a>).)*?<span class="cr">([^<]*)<\/span><\/a>/g)].map(m=>[m[1],m[2]]));
assert.equal(Object.keys(CR).length,10);
const LUGARES={epi:['m01','m02','m16'],'frente-ribeirinha':['m04','m10','m12']};
const server=http.createServer((req,res)=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname).replace(/^\/lente/,''));if(!f.startsWith(root+path.sep)&&f!==root){res.writeHead(403);return res.end();}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.webp':'image/webp','.jpg':'image/jpeg','.png':'image/png'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});
// As fotografias de «Ler a cidade» vivem no sítio do Português (/pt/img/arquivo/): sem rede, uma fotografia do Lente faz de conta.
const SUBSTITUTA=fs.readFileSync(path.join(root,'img/arquivo/rua-da-boavista-tres-predios-2026.jpg'));
async function contexto(browser,width,tema){
 const ctx=await browser.newContext({viewport:{width,height:width<500?740:900},colorScheme:tema,deviceScaleFactor:1});
 await ctx.route('https://pedrohfernandes-klk.github.io/**',async route=>{const u=new URL(route.request().url());
  if(u.pathname.startsWith('/pt/'))return route.fulfill({status:200,contentType:'image/jpeg',body:SUBSTITUTA});
  const response=await ctx.request.get(origin+u.pathname+u.search);await route.fulfill({response});});
 await ctx.route(/fonts\.(googleapis|gstatic)\.com|youtube/,r=>r.abort());
 return ctx;}
let origin;
// PNG das capturas do Playwright (8 bits, RGB ou RGBA, sem entrelaçado): os píxeis, sem dependências.
function png(buf){let p=8,w,h,ct;const ids=[];while(p<buf.length){const n=buf.readUInt32BE(p),t=buf.toString('ascii',p+4,p+8),d=buf.subarray(p+8,p+8+n);if(t==='IHDR'){w=d.readUInt32BE(0);h=d.readUInt32BE(4);ct=d[9];assert.ok(d[8]===8&&!d[12],'PNG de 8 bits sem entrelaçado');}else if(t==='IDAT')ids.push(d);else if(t==='IEND')break;p+=12+n;}
 const bpp=ct===6?4:ct===2?3:0;assert.ok(bpp,'PNG RGB ou RGBA');const raw=zlib.inflateSync(Buffer.concat(ids)),st=w*bpp,out=Buffer.alloc(w*h*3);let prev=Buffer.alloc(st);
 for(let y=0;y<h;y++){const f=raw[y*(st+1)],l=Buffer.from(raw.subarray(y*(st+1)+1,(y+1)*(st+1)));for(let x=0;x<st;x++){const a=x>=bpp?l[x-bpp]:0,b=prev[x],c=x>=bpp?prev[x-bpp]:0;let v=l[x];if(f===1)v+=a;else if(f===2)v+=b;else if(f===3)v+=(a+b)>>1;else if(f===4){const q=a+b-c,pa=Math.abs(q-a),pb=Math.abs(q-b),pc=Math.abs(q-c);v+=pa<=pb&&pa<=pc?a:pb<=pc?b:c;}l[x]=v&255;}
  for(let x=0;x<w;x++)for(let k=0;k<3;k++)out[(y*w+x)*3+k]=l[x*bpp+k];prev=l;}
 return {w,h,px:(x,y)=>[out[(y*w+x)*3],out[(y*w+x)*3+1],out[(y*w+x)*3+2]]};}
const lin=x=>{x/=255;return x<=.03928?x/12.92:Math.pow((x+.055)/1.055,2.4)};
const lum=c=>.2126*lin(c[0])+.7152*lin(c[1])+.0722*lin(c[2]);
const contraste=(a,b)=>{const [x,y]=[lum(a),lum(b)].sort((p,q)=>q-p);return (x+.05)/(y+.05)};
const cor=s=>{const m=String(s).match(/[\d.]+/g);if(!m)return null;const v=m.map(Number);return {c:v.slice(0,3),a:v.length>3?v[3]:1};};
// O círculo de um «i»: as camadas (halo, anel e fundo do círculo, pelos estilos calculados) e, nos píxeis, o que fica à volta dele
// (com o círculo escondido). Vê-se se uma das fronteiras, de fora para dentro, tem 3:1 ou mais: o pior píxel à volta contra a
// primeira camada, ou duas camadas vizinhas (inteiras, à volta de todo o círculo).
async function circulo(page,d){
 const s=d.locator('summary>span');
 const est=await s.evaluate(e=>{const c=getComputedStyle(e);let halo=null;const m=c.boxShadow.match(/^(rgba?\([^)]*\))\s+(-?[\d.]+)px\s+(-?[\d.]+)px\s+(-?[\d.]+)px\s+(-?[\d.]+)px/);if(m&&+m[5]>0&&!/inset/.test(c.boxShadow))halo={cor:m[1],larg:+m[5]};
  return {anel:c.borderTopColor,anelL:parseFloat(c.borderTopWidth),fundo:c.backgroundColor,halo};});
 const bb=await s.boundingBox(),R=bb.width/2,cx=bb.x+R,cy=bb.y+R,ext=R+(est.halo?est.halo.larg:0);
 await s.evaluate(e=>e.style.visibility='hidden');
 const clip={x:Math.floor(cx-ext-5),y:Math.floor(cy-ext-5),width:Math.ceil(2*ext+10),height:Math.ceil(2*ext+10)};
 const im=png(await page.screenshot({clip}));await s.evaluate(e=>e.style.visibility='');
 const volta=[];for(let y=0;y<im.h;y++)for(let x=0;x<im.w;x++){const r=Math.hypot(clip.x+x+.5-cx,clip.y+y+.5-cy);if(r>=ext+1&&r<=ext+3)volta.push(im.px(x,y));}
 const camadas=[];if(est.halo)camadas.push(cor(est.halo.cor));if(est.anelL>0)camadas.push(cor(est.anel));camadas.push(cor(est.fundo));
 const opacas=camadas.filter(x=>x&&x.a>.95).map(x=>x.c);if(!opacas.length)return {valor:1,est};
 let valor=Math.min(...volta.map(p=>contraste(p,opacas[0])));for(let i=1;i<opacas.length;i++)valor=Math.max(valor,contraste(opacas[i-1],opacas[i]));
 return {valor,est};}
// O foco: capturas com e sem foco no mesmo sítio; em cada raio, entre o círculo e o fim do contorno, os píxeis que o foco muda.
// Vê-se se, em todos os raios, um desses píxeis muda 3:1 ou mais, ou tem 3:1 ou mais contra um píxel colado (até 2,5 px, com foco).
async function foco(page,d){
 const s=d.locator('summary');await s.evaluate(e=>e.scrollIntoView({block:'center'}));
 await s.focus();await page.keyboard.press('Shift+Tab');await page.keyboard.press('Tab');await s.evaluate(e=>e.scrollIntoView({block:'center'}));await page.waitForTimeout(150);
 const info=await s.evaluate(e=>{const c=getComputedStyle(e);return {focado:document.activeElement===e,fv:e.matches(':focus-visible'),ow:c.outlineStyle==='none'?0:parseFloat(c.outlineWidth),oo:parseFloat(c.outlineOffset)||0};});
 const bb=await s.boundingBox(),sp=await s.locator('span').boundingBox(),R=bb.width/2,cx=bb.x+R,cy=bb.y+R;
 const clip={x:Math.floor(cx-R-14),y:Math.floor(cy-R-14),width:Math.ceil(2*R+28),height:Math.ceil(2*R+28)};
 const com=png(await page.screenshot({clip}));await page.evaluate(()=>document.activeElement&&document.activeElement.blur());await page.waitForTimeout(150);
 const bb2=await s.boundingBox();assert.ok(Math.abs(bb2.x-bb.x)<.5&&Math.abs(bb2.y-bb.y)<.5,'o «i» não mexeu entre as capturas');
 const sem=png(await page.screenshot({clip}));
 const r0=sp.width/2,r1=R+Math.max(0,info.oo)+info.ow+2;let pior=Infinity;
 for(let k=0;k<72;k++){const a=k*Math.PI/36,raio=[];for(let r=r0;r<=r1;r+=.5){const x=Math.floor(cx+r*Math.cos(a))-clip.x,y=Math.floor(cy+r*Math.sin(a))-clip.y;if(x>=0&&y>=0&&x<com.w&&y<com.h)raio.push({r,f:com.px(x,y),u:sem.px(x,y)});}
  let melhor=1;for(const p of raio){if(contraste(p.f,p.u)<1.5)continue;melhor=Math.max(melhor,contraste(p.f,p.u));for(const q of raio)if(q!==p&&Math.abs(q.r-p.r)<=2.5)melhor=Math.max(melhor,contraste(p.f,q.f));}
  pior=Math.min(pior,melhor);}
 info.valor=pior;return info;}
// Medidas de um «i» das missões, na página ou na gaveta.
function medir(sel){
 const d=document.querySelector(sel),s=d.querySelector('summary'),t=d.querySelector('.info-i-texto'),caixa=d.parentElement,cartao=caixa.querySelector('a.missao');
 const visivel=e=>!!e&&e.getClientRects().length>0&&e.checkVisibility({visibilityProperty:true,contentVisibilityAuto:true});
 const nt=x=>x.replace(/\s+/g,' ').trim(),sr=s.getBoundingClientRect(),cr=cartao.getBoundingClientRect(),circ=s.querySelector('span').getBoundingClientRect();
 const textos=[];const w=document.createTreeWalker(cartao,NodeFilter.SHOW_TEXT);let no;while(no=w.nextNode()){if(!no.data.trim()||!visivel(no.parentElement)||no.parentElement.closest('.p-sr'))continue;const r=document.createRange();r.selectNodeContents(no);for(const q of r.getClientRects())if(q.width>1&&q.height>1)textos.push(q);}
 const cruza=(a,b)=>a.left<b.right-1&&a.right>b.left+1&&a.top<b.bottom-1&&a.bottom>b.top+1;
 const lumi=c=>{const v=c.match(/[\d.]+/g).slice(0,3).map(Number).map(x=>{x/=255;return x<=.03928?x/12.92:Math.pow((x+.055)/1.055,2.4)});return .2126*v[0]+.7152*v[1]+.0722*v[2]};
 const cont=(a,b)=>{const [x,y]=[lumi(a),lumi(b)].sort((p,q)=>q-p);return (x+.05)/(y+.05)};
 const out={open:d.open,summary:visivel(s),alvo:[sr.width,sr.height],nome:s.getAttribute('aria-label'),so:s.innerHTML,classe:caixa.className,
  dentro:!!d.parentElement.closest('a,button,label,figcaption,summary,[aria-hidden="true"]'),irmao:cartao.nextElementSibling===d,
  noCartao:sr.left>=cr.left-1&&sr.right<=cr.right+1&&sr.top>=cr.top-1&&sr.bottom<=cr.bottom+1,cantoBaixo:cr.bottom-sr.bottom<=12&&cr.right-sr.right<=12,
  tapa:textos.filter(q=>cruza(circ,q)).length,missao:(cartao.querySelector('.r')||{}).textContent,
  texto:nt(t.textContent),html:t.innerHTML,lado:document.documentElement.scrollWidth-innerWidth};
 if(d.open){const r=t.getBoundingClientRect();out.textoVisivel=visivel(t);out.dentroEcra=r.left>=-1&&r.right<=innerWidth+1&&r.top>=-1&&r.bottom<=innerHeight+1;out.noCartaoAberto=r.left>=cr.left-1&&r.right<=cr.right+1&&r.top>=cr.top-1&&r.bottom<=cr.bottom+1;
  const x=r.left+Math.min(r.width/2,24),y=r.top+Math.min(r.height/2,16),e=document.elementFromPoint(x,y);out.livre=!!e&&t.contains(e);
  let f=t;let fundo='rgb(255, 255, 255)';for(;f;f=f.parentElement){const c=getComputedStyle(f).backgroundColor,m=c.match(/[\d.]+/g);if(m&&(m.length<4||+m[3]>.95)){fundo=c;break;}}
  out.cTexto=cont(getComputedStyle(t).color,fundo);out.rola=t.scrollHeight>t.clientHeight+1?getComputedStyle(t).overflowY:'nao';}
 return out;}
// Um «i» das missões: as verificações todas (sel encontra a <details>; gaveta diz se vive na gaveta de um lugar).
async function umI(page,sel,mid,rot,gaveta){
 const d=page.locator(sel),s=d.locator('summary');await s.evaluate(e=>e.scrollIntoView({block:'center'}));
 let m=await page.evaluate(medir,sel);
 assert.equal(m.open,false,rot+': fechado ao carregar');assert.ok(m.summary,rot+': «i» à vista');assert.ok(m.alvo[0]>=44&&m.alvo[1]>=44,rot+': alvo de 44 px');
 assert.equal(m.nome,`Créditos da ${CR[mid].startsWith('Gravura')?'gravura':'fotografia'}: Missão ${mid.slice(1)}`,rot+': nome');
 assert.equal(m.so,'<span aria-hidden="true">i</span>',rot);assert.equal(m.dentro,false,rot+': fora da ligação');assert.equal(m.irmao,true,rot+': logo a seguir ao cartão');
 assert.equal(m.classe,'missao-i com-i',rot);assert.ok(m.noCartao&&m.cantoBaixo,rot+': no canto de baixo do cartão');assert.equal(m.tapa,0,rot+': não tapa o texto do cartão');
 assert.equal(m.missao.trim(),'Missão '+mid.slice(1),rot);assert.ok(m.lado<=0,rot+': sem deslize para o lado');
 // o crédito de antes, letra a letra, com as ligações (a da fonte com data-external e aria-label; a licença CC com rel="license")
 assert.equal(m.texto,CR[mid],rot+': crédito completo');
 for(const lic of CR[mid].match(/CC BY(?:-SA)? \d\.\d/g)||[])assert.match(m.html,new RegExp('<a rel="license" href="https://creativecommons\\.org/licenses/[^"]+">'+lic.replace(/\./g,'\\.')+'</a>'),rot+': licença');
 for(const [,a,txt] of m.html.matchAll(/<a ([^>]*)>(.*?)<\/a>/g))if(!/rel="license"/.test(a)){assert.match(a,/^data-external(="")? aria-label="[^"]+, sítio externo" href="https:\/\//,rot);assert.ok(a.includes(`aria-label="${txt}, sítio externo"`),rot);}
 // clique abre (sem seguir a ligação do cartão) e fecha
 const url=page.url();await s.click();m=await page.evaluate(medir,sel);
 assert.ok(m.open&&m.textoVisivel,rot+': clique abre');assert.equal(page.url(),url,rot+': o «i» não segue a ligação');
 await d.locator('.info-i-texto').evaluate(e=>{const r=e.getBoundingClientRect();if(r.top<0||r.bottom>innerHeight)e.scrollIntoView({block:'center'});});m=await page.evaluate(medir,sel);
 assert.ok(m.dentroEcra,rot+': o crédito aberto não sai do ecrã');assert.ok(m.noCartaoAberto,rot+': o crédito aberto fica sobre o seu cartão');assert.ok(m.livre,rot+': nada tapa o crédito');
 assert.ok(m.rola==='nao'||m.rola==='auto',rot+': crédito inteiro ou a rolar por dentro');assert.ok(m.cTexto>=4.5,rot+': o crédito lê-se ('+m.cTexto.toFixed(2)+')');assert.ok(m.lado<=0,rot+': aberto, sem deslize');
 await s.click();assert.equal(await d.evaluate(e=>e.open),false,rot+': clique fecha');
 // teclado: Enter abre, Escape fecha e devolve o foco ao «i» (na gaveta, a gaveta fica aberta)
 await s.focus();await page.keyboard.press('Enter');assert.equal(await d.evaluate(e=>e.open),true,rot+': Enter abre');
 assert.ok(await s.evaluate(e=>e.matches(':focus-visible')&&parseFloat(getComputedStyle(e).outlineWidth)>=2),rot+': foco visível');
 await page.keyboard.press('Escape');assert.equal(await d.evaluate(e=>e.open),false,rot+': Escape fecha');assert.ok(await s.evaluate(e=>document.activeElement===e),rot+': o foco volta ao «i»');
 if(gaveta)assert.ok(await page.evaluate(()=>document.querySelector('#gaveta').classList.contains('aberta')),rot+': o Escape não fecha a gaveta');
 // um clique fora fecha
 await s.click();await page.mouse.click(2,Math.round(page.viewportSize().height/2));assert.equal(await d.evaluate(e=>e.open),false,rot+': clique fora fecha');
}
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));origin='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});let n=0,p=0;
 try{
  // 1. O «i» das missões, na página e na gaveta.
  for(const tema of ['light','dark'])for(const width of [320,390,768,1280]){
   const ctx=await contexto(browser,width,tema),page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(origin+'/lente/cidade/',{waitUntil:'networkidle'});await page.evaluate(()=>{try{localStorage.clear()}catch(e){}});await page.reload({waitUntil:'networkidle'});
   await page.evaluate(()=>document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager'));
   assert.equal(await page.locator('.missoes .missao-i details.info-i').count(),10,`${width} ${tema}: dez «i» nas missões`);
   assert.equal(await page.locator('.missoes .cr, .missoes [class~="cr"]').count(),0,`${width} ${tema}: nenhum span.cr`);
   for(const mid of Object.keys(CR)){await umI(page,`.missoes .missao-i:has(> a[data-id="${mid}"]) > details.info-i`,mid,`${width} px, ${tema}, página, ${mid}`,false);n++;}
   // um só aberto de cada vez
   await page.locator('.missoes .missao-i details.info-i summary').nth(0).click();await page.locator('.missoes .missao-i details.info-i summary').nth(1).click();
   assert.equal(await page.locator('details.info-i[open]').count(),1,`${width} ${tema}: um só «i» aberto`);await page.keyboard.press('Escape');
   // o filtro das portas esconde o cartão com o seu «i»; «Todas» devolve-os
   if(width===390){await page.locator('.portas button[data-p="C"]').click();
    const vis=await page.locator('.missoes .missao-i').evaluateAll(es=>es.map(e=>[e.querySelector('a').dataset.id,e.hidden,e.querySelector('summary').getClientRects().length>0]));
    for(const [id,esc,ve] of vis){const porta=await page.locator(`.missao[data-id="${id}"]`).getAttribute('data-porta');assert.equal(esc,porta!=='C',`${tema}: filtro, ${id}`);assert.equal(ve,porta==='C',`${tema}: filtro, «i» de ${id}`);}
    await page.locator('.portas button[data-p="todas"]').click();assert.equal(await page.locator('.missoes .missao-i[hidden]').count(),0);}
   // a gaveta de cada lugar copia os cartões das suas missões, cada um com o seu «i», fechado (mesmo que o da página esteja aberto)
   for(const [lugar,ms] of Object.entries(LUGARES)){
    await page.locator(`.missoes .missao-i:has(> a[data-id="${ms[0]}"]) summary`).click();
    await page.evaluate(l=>{location.hash='#lugar-'+l;},lugar);await page.waitForFunction(()=>document.querySelector('#gaveta').classList.contains('aberta'));await page.waitForTimeout(200);
    await page.evaluate(()=>document.querySelectorAll('#gaveta img[loading=lazy]').forEach(i=>i.loading='eager'));
    const copiados=await page.locator('#gaveta .gv-missoes > *').evaluateAll(es=>es.map(e=>[e.className,(e.querySelector('a.missao')||e).dataset.id,!!e.querySelector('details.info-i'),!!e.querySelector('details[open]')]));
    assert.deepEqual(copiados.filter(x=>x[2]).map(x=>x[1]),ms,`${width} ${tema}: a gaveta de ${lugar} copia o «i» das missões`);
    for(const x of copiados){assert.equal(x[3],false,`${width} ${tema}: na gaveta, o «i» de ${x[1]} começa fechado`);assert.equal(x[0]==='missao-i com-i',!!CR[x[1]],`${width} ${tema}: ${x[1]}`);}
    for(const mid of ms){await umI(page,`#gaveta .missao-i:has(> a[data-id="${mid}"]) > details.info-i`,mid,`${width} px, ${tema}, gaveta de ${lugar}, ${mid}`,true);n++;}
    // com um «i» aberto na gaveta, o primeiro Escape fecha o «i» e o seguinte fecha a gaveta
    const s=page.locator(`#gaveta .missao-i:has(> a[data-id="${ms[0]}"]) summary`);await s.focus();await page.keyboard.press('Enter');
    await page.keyboard.press('Escape');assert.equal(await page.locator('#gaveta details.info-i[open]').count(),0,`${width} ${tema}: o Escape fecha o «i»`);
    assert.ok(await page.evaluate(()=>document.querySelector('#gaveta').classList.contains('aberta')),`${width} ${tema}: a gaveta fica aberta`);
    await page.keyboard.press('Escape');assert.equal(await page.evaluate(()=>document.querySelector('#gaveta').classList.contains('aberta')),false,`${width} ${tema}: o Escape seguinte fecha a gaveta`);
   }
   // impressão: o «i» não sai; o crédito sai por extenso, por baixo do cartão, com o endereço da licença
   await page.emulateMedia({media:'print'});
   const imp=await page.locator('.missoes .missao-i').evaluateAll(es=>es.map(e=>{const v=x=>!!x&&x.getClientRects().length>0&&x.checkVisibility({visibilityProperty:true,contentVisibilityAuto:true});
    const t=e.querySelector('.info-i-texto'),a=e.querySelector('a.missao');return {i:v(e.querySelector('summary')),texto:v(t),debaixo:t.getBoundingClientRect().top>=a.getBoundingClientRect().bottom-1,
     licencas:[...t.querySelectorAll('a[rel~=license]')].map(x=>getComputedStyle(x,'::after').content.includes(x.getAttribute('href')))};}));
   imp.forEach((x,i)=>{const rot=`${width} ${tema}, missão ${i+1}, impressão`;assert.equal(x.i,false,rot+': sem o botão «i»');assert.ok(x.texto&&x.debaixo,rot+': o crédito por baixo do cartão');assert.ok(x.licencas.every(Boolean),rot+': o endereço da licença');});
   await page.emulateMedia({media:'screen'});
   // fora da projeção, o «i» continua como era: papel, halo de 2 px e borda de 2 px; aberto, cheio na cor da tinta
   const fora=await page.locator('.missoes .missao-i details.info-i').first().evaluate(d=>{const c=getComputedStyle(d.querySelector('summary>span'));return {b:c.borderTopWidth,w:c.width,sh:c.boxShadow,bg:c.backgroundColor,tinta:getComputedStyle(document.documentElement).getPropertyValue('--ii-tinta')};});
   assert.equal(fora.b,'2px');assert.equal(fora.w,'28px');assert.match(fora.sh,/ 0px 0px 0px 2px$/);assert.notEqual(fora.bg,'rgba(0, 0, 0, 0)');
   assert.deepEqual(errors,[],`${width} ${tema}: erros na página`);await ctx.close();
  }
  // 2. O «i» na projeção, nos três modos, em claro e em escuro.
  const MODOS=[
   {nome:'em-projecao (entrada com ?projetar=1)',url:'/lente/?projetar=1',marca:'em-projecao'},
   {nome:'epi-projection (moldura de /projetar/, «Ideias»)',url:'/lente/projetar/?pagina='+encodeURIComponent('https://pedrohfernandes-klk.github.io/lente/narrativas/ideias/'),moldura:true,marca:'epi-projection'},
   {nome:'epi-projection (moldura de /projetar/, «Ler a cidade»)',url:'/lente/projetar/?pagina='+encodeURIComponent('https://pedrohfernandes-klk.github.io/lente/cidade/'),moldura:true,marca:'epi-projection',missoes:true},
   {nome:'data-cz-projection (entrada)',url:'/lente/',atributo:true,marca:'data-cz-projection'},
   {nome:'data-cz-projection (gaveta da EPI)',url:'/lente/cidade/#lugar-epi',atributo:true,marca:'data-cz-projection',sel:'#gaveta details.info-i'},
  ];
  for(const tema of ['light','dark'])for(const modo of MODOS){
   const ctx=await contexto(browser,1280,tema),page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(origin+modo.url,{waitUntil:'networkidle'});
   let alvo=page;if(modo.moldura){alvo=page.frameLocator('#lesson-frame');await alvo.locator('details.info-i').first().waitFor({state:'attached'});await page.waitForTimeout(800);}
   if(modo.atributo)await page.evaluate(()=>document.documentElement.setAttribute('data-cz-projection',''));
   const html=alvo.locator('html');
   assert.ok(await html.evaluate((e,m)=>e.classList.contains(m)||e.hasAttribute(m),modo.marca),`${tema}, ${modo.nome}: modo de projeção ligado`);
   await html.evaluate(e=>e.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager'));await page.waitForTimeout(400);
   const ds=alvo.locator(modo.sel||'details.info-i');const total=await ds.count();let vistos=0,missoes=0;
   for(let k=0;k<total;k++){
    const d=ds.nth(k);if(!(await d.locator('summary').evaluate(e=>e.getClientRects().length>0&&e.checkVisibility())))continue;
    const rot=`${tema}, ${modo.nome}, «i» ${k+1}`;const linha=await d.evaluate(e=>e.classList.contains('info-i--linha'));missoes+=await d.evaluate(e=>!!e.closest('.missao-i'));
    await d.locator('summary').evaluate(e=>e.scrollIntoView({block:'center'}));await page.waitForTimeout(100);
    const fechado=await circulo(page,d);assert.ok(fechado.valor>=3,`${rot} (${linha?'linha':'canto'}): o círculo fechado vê-se (${fechado.valor.toFixed(2)}:1)`);
    assert.equal(fechado.est.anelL,1,rot+': borda de 1 px na projeção');
    const f=await foco(page,d);assert.ok(f.focado&&f.fv,rot+': foco no «i»');assert.ok(f.valor>=3,`${rot}: o foco vê-se (${f.valor.toFixed(2)}:1)`);
    await d.locator('summary').click();await page.evaluate(()=>document.activeElement&&document.activeElement.blur());if(modo.moldura)await alvo.locator('body').evaluate(()=>document.activeElement&&document.activeElement.blur());
    await page.mouse.move(1,1);await page.waitForTimeout(250);assert.equal(await d.evaluate(e=>e.open),true,rot+': abre');
    const aberto=await circulo(page,d);assert.ok(aberto.valor>=3,`${rot}: o círculo aberto vê-se (${aberto.valor.toFixed(2)}:1)`);
    await d.locator('summary').click();assert.equal(await d.evaluate(e=>e.open),false,rot+': fecha');
    vistos++;p++;
   }
   assert.ok(vistos>0,`${tema}, ${modo.nome}: há «i» à vista`);if(modo.missoes)assert.equal(missoes,10,`${tema}, ${modo.nome}: os dez «i» das missões`);
   assert.deepEqual(errors,[],`${tema}, ${modo.nome}: erros na página`);await ctx.close();
  }
  console.log(`Créditos atrás do «i» (lente-4): ${n} «i» das missões abertos por clique e por teclado, na página e na gaveta, a 320, 390, 768 e 1280 px, em claro e escuro; ${p} «i» na projeção com o círculo e o foco a 3:1 ou mais.`);
 }finally{await browser.close();server.closeAllConnections();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
