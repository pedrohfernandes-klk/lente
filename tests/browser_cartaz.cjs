// 01/11/2026: decisão 57, D1–D5. Contratos das peças em navegador real.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const css = fs.readFileSync(path.join(__dirname,'../assets/cartaz-components.css'),'utf8');
const appearance = fs.readFileSync(path.join(__dirname,'../assets/appearance.css'),'utf8');
const js = fs.readFileSync(path.join(__dirname,'../assets/cartaz-components.js'),'utf8');
const fixture = theme => `<!doctype html><html lang="pt" data-theme="${theme}"><meta charset="utf-8"><style>${appearance}\n${css}</style><body>
<nav class="casca"><a href="#fora">Barra</a></nav>
<main data-cartaz="2" style="background:var(--cz-ground);color:var(--cz-ink)">
<p class="cz-prose">Texto com <a href="#destino">ligação</a>.</p>
<section class="cz-next"><p class="cz-label">Próximo passo</p><h2>A seguir</h2><p>Continua a leitura. <span class="cz-state done">Feita 01/11</span></p><a class="cz-button primary" href="#destino">Continuar</a></section>
<button class="cz-button">Voltar</button><button class="cz-button" disabled>Indisponível</button>
<div class="cz-grid"><article class="cz-door"><a href="#destino"><h2>Observar</h2><span>Descobre os percursos.</span><span class="arrow">→</span></a></article></div>
<a class="cz-row" href="#destino"><b>1</b><span>Percurso</span><span class="cz-state current">A seguir</span><span>→</span></a>
<p class="cz-credit">Fotografia em <a href="https://commons.wikimedia.org/" data-external aria-label="Wikimedia Commons, sítio externo">Wikimedia Commons</a>. Licença <a href="#destino">CC0</a>.</p>
<nav class="cz-crumbs"><a href="#destino">Início</a><span aria-current="page">Observar</span></nav>
<span class="cz-state"></span><span class="cz-state done">Feita 01/11</span>
<details class="cz-fold" open><summary>Primeira banda</summary><p id="destino">Conteúdo da primeira banda</p></details>
<details class="cz-fold" open><summary>Segunda banda</summary><p data-cz-next>A seguir</p></details>
<details class="cz-fold" open><summary>Terceira banda</summary><p id="alvo">Conteúdo da âncora</p></details>
<footer class="cz-footer"><nav class="cz-footer-links" aria-label="Saídas"><a href="#destino">Início <span>→</span></a></nav><p class="cz-prose">Texto do rodapé com <a href="#destino">ligação</a>.</p></footer>
</main></body></html>`;
// 01/11/2026: volta 3. Créditos longos: em #seguidas, duas ligações em linhas seguidas e sobrepostas na horizontal; em #quebra, o
// crédito da entrada do lente #88, com «Wikimedia Commons» no sítio onde, em linha, partiria no fim da linha.
const fixtureCreditos = theme => `<!doctype html><html lang="pt" data-theme="${theme}"><meta charset="utf-8"><style>${appearance}\n${css}</style><body>
<main data-cartaz="2" style="background:var(--cz-ground);color:var(--cz-ink);padding:48px 32px">
<p class="cz-credit" id="seguidas" style="max-width:12.5em">Fotografia de Joshua Benoliel, 1910. <a href="#o">Arquivo Municipal</a> <a href="#l">CC BY-SA 4.0</a>.</p>
<p class="cz-credit" id="quebra">Joseph Wright of Derby, <i>Uma experiência com uma ave numa bomba de ar</i>, 1768. Óleo sobre tela. National Gallery, Londres. <a href="https://commons.wikimedia.org/" data-external aria-label="Wikimedia Commons, sítio externo">Wikimedia Commons</a>. Domínio público.</p>
</main></body></html>`;
// 01/11/2026: volta 4. Pontuação colada à ligação do crédito (corre na página, com page.evaluate). Para cada ligação dos créditos
// escolhidos e para cada largura do crédito, desde a largura da ligação mais 8 px até à largura toda (sem max-width), de 1 em 1 px:
// - o primeiro carácter do texto a seguir à ligação, medido com um Range de um carácter, fica na mesma linha que o fim da ligação
//   (centros a menos de meia entrelinha). Sem retângulo, só se aceita um espaço em que a linha parte: o navegador retira-o no fim
//   da linha da ligação, e exige-se que o carácter a seguir a ele comece numa linha abaixo (em #seguidas, entre as duas ligações).
//   Qualquer outro carácter sem retângulo falha;
// - nenhuma ligação do crédito parte por dentro (um só retângulo em getClientRects).
// No fim, o max-width do crédito volta ao que era.
const creditLines = selector => [...document.querySelectorAll(selector)].flatMap(c=>{
 const keep=c.style.maxWidth,lh=parseFloat(getComputedStyle(c).lineHeight),links=[...c.querySelectorAll('a')];
 c.style.maxWidth='none';
 const full=Math.floor(c.getBoundingClientRect().width);
 const out=links.map(a=>{
  const walker=document.createTreeWalker(c,NodeFilter.SHOW_TEXT);walker.currentNode=a;
  let next=walker.nextNode();while(next&&(a.contains(next)||!next.length))next=walker.nextNode();
  let then=next,thenAt=1;if(then&&then.length<2){thenAt=0;then=walker.nextNode();while(then&&!then.length)then=walker.nextNode();}
  const charRect=(node,i)=>{if(!node)return;const r=document.createRange();r.setStart(node,i);r.setEnd(node,i+1);const cs=r.getClientRects();return cs[cs.length-1];};
  const from=Math.ceil(a.getBoundingClientRect().width)+8,bad=[];let widths=0;
  if(next)for(let w=from;w<=full;w++){
   c.style.maxWidth=w+'px';widths++;
   const split=links.filter(l=>l.getClientRects().length!==1).map(l=>l.textContent);
   const rects=a.getClientRects(),end=rects[rects.length-1],ch=charRect(next,0),below=!ch&&/^\s$/.test(next.data[0])&&charRect(then,thenAt);
   const dy=ch&&end ? ((ch.top+ch.bottom)-(end.top+end.bottom))/2 : null;
   const same=ch ? !!end&&Math.abs(dy)<lh/2 : !!below&&!!end&&((below.top+below.bottom)-(end.top+end.bottom))/2>=lh/2;
   if(split.length||!same)bad.push({w,split,linhas:dy===null?null:Math.round(dy/lh)});
  }
  return {credit:c.id?'#'+c.id:'.'+c.className,text:a.textContent,after:next?next.data[0]:null,from,full,widths,bad};
 });
 c.style.maxWidth=keep;
 return out;
});
const assertCreditLines = (lines,where,count) => {
 assert.equal(lines.length,count,`${where}: ligações de crédito verificadas`);
 for(const l of lines) {
  assert.ok(l.after!==null && l.widths>0 && l.widths===l.full-l.from+1,`${where}, ${l.credit} ${l.text}: sem texto a seguir ou sem larguras (${l.from} a ${l.full} px)`);
  assert.equal(l.bad.length,0,`${where}, ${l.credit} ${l.text}: em ${l.bad.length} de ${l.widths} larguras (${l.from} a ${l.full} px), ${JSON.stringify(l.after)} sai da linha da ligação ou uma ligação parte por dentro; a primeira: ${JSON.stringify(l.bad[0])}`);
 }
};
(async () => {
 const browser = await chromium.launch({headless:true,...(process.env.CHROME_PATH ? {executablePath:process.env.CHROME_PATH} : {})});
 try {
  for (const theme of ['light','dark']) for(const width of [390,1366]) {
   const context = await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});
   const page = await context.newPage();
   await page.route('http://cartaz.test/**',route => route.fulfill({contentType:'text/html',body:fixture(theme)}));
   await page.goto('http://cartaz.test/');
   // Sem JavaScript de melhoria: todo o conteúdo vem aberto no HTML.
   assert.deepEqual(await page.locator('.cz-fold').evaluateAll(es => es.map(e=>e.open)),[true,true,true]);
   await page.addScriptTag({content:js});
   assert.deepEqual(await page.locator('.cz-fold').evaluateAll(es=>es.map(e=>e.open)),width<640 ? [false,true,false] : [true,true,true]);
   await page.evaluate(()=>location.hash='alvo');
   await page.waitForFunction(()=>document.getElementById('alvo').parentElement.open);
   // 01/11/2026: revisão curta. As caixas do rodapé são as ligações de .cz-footer-links; a ligação do texto do rodapé é verificada abaixo.
   for (const selector of ['.cz-button','.cz-row','.cz-door>a','.cz-crumbs a','.cz-footer-links a','.cz-fold>summary']) {
    const sizes = await page.locator(selector).evaluateAll(es=>es.map(e=>{const r=e.getBoundingClientRect();return [r.width,r.height]}));
    for(const [w,h] of sizes) assert.ok(w>=44 && h>=(selector==='.cz-button'?48:44),`${selector}: ${w}×${h}`);
   }
   // 01/11/2026: volta 2. A ligação do crédito não tem padding: o alvo é o ::before invisível, que se mede em todas as ligações
   // do crédito, também na curta («CC0»). Mínimo de 44 × 44 px, à unidade de desenho do Chrome (1/64 px, que arredonda os 50 %
   // de uma ligação de 26 px); um toque perto dos cantos desse quadrado abre a ligação.
   const creditTargets = await page.locator('.cz-credit a').evaluateAll(es=>es.map(e=>{e.scrollIntoView({block:'center'});const s=getComputedStyle(e,'::before'),r=e.getBoundingClientRect(),cx=(r.left+r.right)/2,cy=(r.top+r.bottom)/2;
    const hits=[[-21,-21],[21,-21],[-21,21],[21,21]].map(([dx,dy])=>{const t=document.elementFromPoint(cx+dx,cy+dy);return !!t&&(t===e||e.contains(t));});
    return {text:e.textContent,content:s.content,w:parseFloat(s.width),h:parseFloat(s.height),hits};}));
   assert.equal(creditTargets.length,2);
   for(const t of creditTargets) {
    assert.equal(t.content,'""',`${t.text}: sem ::before`);
    assert.ok(t.w>=44-1/64 && t.h>=44-1/64,`.cz-credit a::before (${t.text}): ${t.w}×${t.h}`);
    assert.deepEqual(t.hits,[true,true,true,true],`${t.text}: toque nos cantos do alvo`);
   }
   assert.equal(await page.locator('.cz-fold>summary').first().evaluate(e=>e.getBoundingClientRect().height),88);
   assert.equal(await page.locator('.cz-state:empty').evaluate(e=>getComputedStyle(e).display),'none');
   for(const selector of ['.cz-row','.cz-door>a','.cz-credit a','.cz-button']) {
    assert.equal(await page.locator(selector).first().evaluate(e=>getComputedStyle(e).textDecorationLine),'none');
   }
   // 01/11/2026: volta 4. No crédito da peça, a pontuação a seguir a cada ligação fica na linha da ligação, e nenhuma ligação parte
   // por dentro, em todas as larguras do crédito desde a ligação mais 8 px (creditLines, acima; também nos créditos longos, abaixo).
   assertCreditLines(await page.evaluate(creditLines,'.cz-credit'),`${theme}, ${width} px, crédito da peça`,2);
   // 01/11/2026: revisão curta. A ligação do crédito fica em linha e não muda a entrelinha da frase.
   // 01/11/2026: volta 3. A ligação passa a inline-block, para não partir de linha e o ::before envolver um só retângulo (verificado
   // abaixo, nos créditos longos). A entrelinha da frase continua garantida pela altura do crédito, múltipla da linha.
   // 01/11/2026: volta 4. A ligação volta a inline, com white-space:nowrap: o inline-block abria uma quebra antes da pontuação. Não
   // partir continua verificado nos créditos longos e, com a pontuação colada, em creditLines.
   const credit = await page.locator('.cz-credit').evaluate(e=>({h:e.getBoundingClientRect().height,lh:parseFloat(getComputedStyle(e).lineHeight),display:getComputedStyle(e.querySelector('a')).display}));
   assert.equal(credit.display,'inline');
   assert.ok(credit.h<44 && Math.abs(credit.h-credit.lh*Math.round(credit.h/credit.lh))<.5,`crédito: ${credit.h} px para linhas de ${credit.lh} px`);
   // 01/11/2026: volta 2. A caixa de cada ligação do crédito não passa da entrelinha, e os estados ficam nessa caixa: o fundo de
   // :active pinta só a caixa de conteúdo, o hover sublinha sem contorno e o anel de foco (3 px, também com o rato por cima) cabe
   // no espaço entre o texto desta linha e o das vizinhas. Assim nenhum estado tapa as linhas vizinhas.
   const creditStates = await page.locator('.cz-credit a').evaluateAll(es=>es.map(e=>{
    const lh=parseFloat(getComputedStyle(e.parentElement).lineHeight),box=()=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {h:r.height,content:r.height-parseFloat(s.paddingTop)-parseFloat(s.paddingBottom)-parseFloat(s.borderTopWidth)-parseFloat(s.borderBottomWidth)};};
    const read=c=>{e.className=c;const s=getComputedStyle(e),out={...box(),clip:s.backgroundClip,bg:s.backgroundColor,outline:s.outlineStyle,ow:parseFloat(s.outlineWidth),oo:parseFloat(s.outlineOffset),deco:s.textDecorationLine};e.className='';return out;};
    return {text:e.textContent,lh,normal:box(),active:read('is-active'),hover:read('is-hover'),focus:read('is-hover is-focus')};}));
   for(const c of creditStates) {
    assert.ok(c.normal.h<=c.lh,`${c.text}: caixa de ${c.normal.h} px numa linha de ${c.lh} px`);
    assert.equal(c.active.clip,'content-box',`${c.text}: fundo de :active fora da caixa de conteúdo`);
    assert.notEqual(c.active.bg,'rgba(0, 0, 0, 0)');
    assert.ok(c.active.content<=c.lh,`${c.text}: fundo de :active com ${c.active.content} px numa linha de ${c.lh} px`);
    assert.deepEqual([c.hover.outline,c.hover.deco],['none','underline'],`${c.text}: hover`);
    assert.equal(c.focus.ow,3,`${c.text}: anel de foco perdido com o rato por cima`);
    assert.ok(c.focus.oo+c.focus.ow<=c.lh-c.normal.h,`${c.text}: anel de foco a ${c.focus.oo}+${c.focus.ow} px, entre o texto de duas linhas há ${c.lh-c.normal.h} px`);
   }
   // 01/11/2026: revisão curta. A ligação do texto do rodapé fica com o desenho de .cz-prose a.
   assert.deepEqual(await page.locator('.cz-footer .cz-prose a').evaluate(e=>{const s=getComputedStyle(e);return [s.display,s.textDecorationLine,s.backgroundColor];}),['inline','underline','rgba(0, 0, 0, 0)']);
   // 01/11/2026: revisão curta. Rótulos com 0,14 em de espaçamento.
   const labelSpacing = await page.locator('.cz-label').evaluate(e=>{const s=getComputedStyle(e);return parseFloat(s.letterSpacing)/parseFloat(s.fontSize);});
   assert.ok(Math.abs(labelSpacing-.14)<.001,`rótulo: ${labelSpacing} em`);
   // 01/11/2026: revisão curta. O contorno do quadrado do estado segue a cor do texto e não desaparece dentro de .cz-next.
   for(const [border,color] of await page.locator('.cz-state:not(:empty)').evaluateAll(es=>es.map(e=>[getComputedStyle(e,'::before').borderTopColor,getComputedStyle(e).color]))) assert.equal(border,color);
   const nextState = await page.locator('.cz-next .cz-state').evaluate(e=>[getComputedStyle(e,'::before').borderTopColor,getComputedStyle(e.closest('.cz-next')).backgroundColor]);
   assert.notEqual(nextState[0],nextState[1],'contorno do estado igual ao fundo de .cz-next');
   // 01/11/2026: decisão 57, D2. Só .cz-next admite uma região invertida.
   const region = await page.locator('.cz-next').evaluate(e=>({bg:getComputedStyle(e).backgroundColor,ink:getComputedStyle(e).color}));
   assert.equal(region.bg,theme==='light'?'rgb(0, 0, 0)':'rgb(236, 235, 229)');
   assert.equal(region.ink,theme==='light'?'rgb(255, 255, 255)':'rgb(18, 18, 16)');
   assert.equal(await page.evaluate(()=>document.querySelectorAll('.cz-next').length),1);
   const inverted = await page.locator('main :is(section,article,aside,footer,details)').evaluateAll(es => {
     const ink=getComputedStyle(document.querySelector('.cz-next')).backgroundColor;
     return es.filter(e=>getComputedStyle(e).backgroundColor===ink).map(e=>e.className);
   });
   assert.deepEqual(inverted,['cz-next'], 'A exceção não autoriza outros blocos invertidos');
   const contrast = await page.evaluate(() => {
     const rgb = s => s.match(/[\d.]+/g).map(Number).slice(0,3);
     const lum = c => c.map(v => {v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0);
     return ['.cz-next','.cz-next .primary','.cz-credit','.cz-row'].map(sel => {
       const e=document.querySelector(sel), s=getComputedStyle(e); let bg;
       for(let n=e;n;n=n.parentElement){const b=getComputedStyle(n).backgroundColor;if(b!=='rgba(0, 0, 0, 0)'){bg=rgb(b);break;}}
       if(!bg) bg=rgb(getComputedStyle(document.documentElement).getPropertyValue('--fundo').trim().startsWith('#') ? getComputedStyle(document.body).backgroundColor : 'rgb(255,255,255)');
       const a=lum(rgb(s.color)), b=lum(bg);return [sel,(Math.max(a,b)+.05)/(Math.min(a,b)+.05)];
     });
   });
   for(const [sel,ratio] of contrast) assert.ok(ratio>=4.5,`${sel}: contraste ${ratio}`);
   await page.locator('.cz-next .primary').focus();
   assert.equal(await page.locator('.cz-next .primary').evaluate(e=>getComputedStyle(e).outlineWidth),'3px');

   await page.evaluate(()=>dispatchEvent(new Event('beforeprint')));
   assert.deepEqual(await page.locator('.cz-fold').evaluateAll(es=>es.map(e=>e.open)),[true,true,true]);
   await page.emulateMedia({media:'print'});
   assert.equal(await page.locator('.cz-next').evaluate(e=>getComputedStyle(e).backgroundColor),'rgb(255, 255, 255)');
   await page.emulateMedia({media:'screen'});
   await page.evaluate(()=>dispatchEvent(new Event('afterprint')));
   await page.goto('http://cartaz.test/?projetar=1');
   await page.addScriptTag({content:js});
   assert.deepEqual(await page.locator('.cz-fold').evaluateAll(es=>es.map(e=>e.open)),[true,true,true]);
   // 01/11/2026: volta 2. Em projeção (classe do sistema), a raiz fica a 22 px e as peças nos degraus normais, sem depender da
   // raiz da família: texto a 22 px, rótulos, créditos, estados e migalhas a 17,875 px (SISTEMA-DESENHO, secção 8); o antetítulo
   // fica abaixo de 65 % do título da região «A seguir». Antes: 20 e 16 px com a raiz da página a 16 px.
   await page.evaluate(()=>document.documentElement.classList.add('em-projecao'));
   const projectionSizes = ()=>{const size=s=>parseFloat(getComputedStyle(document.querySelector(s)).fontSize);return {root:size('[data-cartaz="2"]'),label:size('.cz-label'),credit:size('.cz-credit'),state:size('.cz-state:not(:empty)'),crumbs:size('.cz-crumbs'),prose:size('.cz-prose'),button:size('.cz-button'),title:size('.cz-next h2')};};
   const projected = await page.evaluate(projectionSizes);
   assert.deepEqual(projected,{root:22,label:17.875,credit:17.875,state:17.875,crumbs:17.875,prose:22,button:22,title:34.375});
   assert.ok(projected.label<=.65*projected.title,`antetítulo ${projected.label} px para título de ${projected.title} px`);
   // 01/11/2026: volta 2. Nenhum texto visível das peças abaixo do mínimo da projeção (17,9 px, isto é, 13 × 1,375 = 17,875).
   const small = await page.evaluate(()=>[...document.querySelectorAll('[data-cartaz="2"], [data-cartaz="2"] *')].filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())&&e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden').map(e=>[e.tagName.toLowerCase()+(e.className?'.'+e.className:''),parseFloat(getComputedStyle(e).fontSize)]).filter(([,size])=>size<17.85));
   assert.deepEqual(small,[],'texto das peças abaixo de 17,85 px em projeção');
   // 01/11/2026: volta 3. Os degraus da projeção não leem os tokens da família: com uma família que fixa --cz-t13 e --cz-t16 em
   // projeção (como o Laboratório do lente #89), as peças ficam nas mesmas medidas. Antes: raiz das peças a 16 px.
   const family = await page.addStyleTag({content:'html.em-projecao [data-cartaz="2"]{--cz-t13:13px;--cz-t16:16px}'});
   assert.deepEqual(await page.evaluate(projectionSizes),{root:22,label:17.875,credit:17.875,state:17.875,crumbs:17.875,prose:22,button:22,title:34.375},'projeção com os tokens fixados pela família');
   await family.evaluate(e=>e.remove());
   assert.equal(await page.evaluate(()=>localStorage.length),0);
   assert.equal(await page.evaluate(()=>Math.max(0,document.documentElement.scrollWidth-innerWidth)),0);
   await context.close();
  }
  // 01/11/2026: volta 3. Créditos longos, nos dois temas, a 320, 390 e 1366 px, com e sem projeção.
  // - Em #seguidas, cada ponto da caixa das letras de uma ligação abre essa ligação, e não a área de toque da outra.
  // - Em #quebra, procura-se a largura do crédito em que «Wikimedia Commons», em linha, partiria no fim da linha. A ligação tem de dar
  //   um só retângulo, com o ::before de 44 × 44 px no mínimo à volta dela; os cantos do ::before e um toque a ±21 px do centro abrem-na.
  // - Nenhum ponto a mais de 15 px acima ou abaixo de uma ligação, nem fora dos 44 px de largura mínima, a abre (com 1 px de
  //   arredondamento do Chrome). A altura de cada crédito é múltipla da entrelinha e não há deslize horizontal.
  // - 01/11/2026: volta 4. Como a peça tem white-space:nowrap na ligação, a procura da largura de quebra de #quebra põe também
  //   white-space:normal na ligação enquanto procura, e retira-o depois. Em #quebra e #seguidas, a pontuação a seguir a cada ligação
  //   fica na linha da ligação e nenhuma ligação parte por dentro (creditLines), em todas as larguras desde a ligação mais 8 px.
  for (const theme of ['light','dark']) for (const width of [320,390,1366]) for (const projection of [false,true]) {
   const where = `${theme}, ${width} px${projection?', projeção':''}`;
   const context = await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});
   const page = await context.newPage();
   await page.route('http://cartaz.test/**',route => route.fulfill({contentType:'text/html',body:fixtureCreditos(theme)}));
   await page.goto('http://cartaz.test/');
   if(projection) await page.evaluate(()=>document.documentElement.classList.add('em-projecao'));
   const r = await page.evaluate(()=>{
    const hit=(a,x,y)=>{const t=document.elementFromPoint(x,y);return !!t&&(t===a||a.contains(t));};
    const q=document.getElementById('quebra'),qa=q.querySelector('a');let breakWidth=0;
    qa.style.display='inline';qa.style.whiteSpace='normal';
    for(let w=Math.ceil(q.getBoundingClientRect().width);w>=120;w--){q.style.maxWidth=w+'px';if(qa.getClientRects().length>1){breakWidth=w;break;}}
    qa.style.removeProperty('display');qa.style.removeProperty('white-space');
    const links=[...document.querySelectorAll('.cz-credit a')].map(a=>{
     a.scrollIntoView({block:'center'});
     const p=a.parentElement.getBoundingClientRect(),R=a.getBoundingClientRect(),s=getComputedStyle(a,'::before');
     const before={left:R.left+parseFloat(s.left),top:R.top+parseFloat(s.top),width:parseFloat(s.width),height:parseFloat(s.height)};
     let letters=0,stolen=0;
     for(let x=R.left+.5;x<R.right;x++)for(let y=R.top+.5;y<R.bottom;y++){letters++;if(!hit(a,x,y))stolen++;}
     const ex=Math.max(0,22-R.width/2)+1;let far=0;
     for(let x=p.left-40;x<p.right+40;x+=2)for(let y=p.top-40;y<p.bottom+40;y+=2)if(hit(a,x,y)&&!(x>=R.left-ex&&x<=R.right+ex&&y>=R.top-16&&y<=R.bottom+16))far++;
     const cx=(R.left+R.right)/2,cy=(R.top+R.bottom)/2,bl=before.left,bt=before.top,br=bl+before.width,bb=bt+before.height;
     return {credit:a.parentElement.id,text:a.textContent,rects:a.getClientRects().length,R:[R.left,R.top,R.right,R.bottom],before,letters,stolen,far,
      corners:[[bl+1.5,bt+1.5],[br-1.5,bt+1.5],[bl+1.5,bb-1.5],[br-1.5,bb-1.5]].map(([x,y])=>hit(a,x,y)),
      near:[[-21,-21],[21,-21],[-21,21],[21,21]].map(([dx,dy])=>hit(a,cx+dx,cy+dy))};
    });
    const credits=[...document.querySelectorAll('.cz-credit')].map(e=>({id:e.id,h:e.getBoundingClientRect().height,lh:parseFloat(getComputedStyle(e).lineHeight)}));
    return {breakWidth,links,credits,slide:Math.max(0,document.documentElement.scrollWidth-innerWidth)};
   });
   assert.ok(r.breakWidth>0,`${where}: «Wikimedia Commons» não partiria em linha em nenhuma largura de #quebra`);
   const [upper,lower]=r.links.filter(l=>l.credit==='seguidas'),lh=r.credits.find(c=>c.id==='seguidas').lh;
   assert.ok(Math.abs(lower.R[1]-upper.R[1]-lh)<.5,`${where}: as ligações de #seguidas não estão em linhas seguidas`);
   assert.ok(Math.min(upper.R[2],lower.R[2])-Math.max(upper.R[0],lower.R[0])>22,`${where}: as ligações de #seguidas não se sobrepõem na horizontal`);
   for(const l of r.links) {
    const b=l.before;
    assert.equal(l.rects,1,`${where}, ${l.text}: ligação partida em ${l.rects} retângulos`);
    assert.ok(b.width>=44-1/64 && b.height>=44-1/64,`${where}, ${l.text}: ::before de ${b.width}×${b.height}`);
    assert.ok(b.left<=l.R[0]+.02 && b.top<=l.R[1]+.02 && b.left+b.width>=l.R[2]-.02 && b.top+b.height>=l.R[3]-.02,`${where}, ${l.text}: o ::before não envolve a ligação`);
    assert.equal(l.stolen,0,`${where}, ${l.text}: ${l.stolen} de ${l.letters} pontos das letras não abrem esta ligação`);
    assert.equal(l.far,0,`${where}, ${l.text}: ${l.far} pontos fora do alvo abrem a ligação`);
   }
   const wiki=r.links.find(l=>l.credit==='quebra');
   assert.deepEqual(wiki.corners,[true,true,true,true],`${where}: toque nos cantos do ::before de «Wikimedia Commons»`);
   assert.deepEqual(wiki.near,[true,true,true,true],`${where}: toque a ±21 px do centro de «Wikimedia Commons»`);
   for(const c of r.credits) assert.ok(Math.abs(c.h-c.lh*Math.round(c.h/c.lh))<.5,`${where}, #${c.id}: ${c.h} px para linhas de ${c.lh} px`);
   assert.equal(r.slide,0,`${where}: deslize horizontal`);
   // 01/11/2026: volta 4. Pontuação colada e ligações inteiras em #quebra e #seguidas, em todas as larguras dos dois créditos.
   assertCreditLines(await page.evaluate(creditLines,'#quebra, #seguidas'),where,3);
   await context.close();
  }
  const nojs = await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
  const p = await nojs.newPage();
  await p.route('http://cartaz.test/**',r=>r.fulfill({contentType:'text/html',body:fixture('light')+`<script>${js}</script>`}));
  await p.goto('http://cartaz.test/');
  for(const id of ['destino','alvo']) assert.ok(await p.locator('#'+id).isVisible());
  await nojs.close();
  console.log('Cartaz: alvos, estados, dobras, âncora, impressão, projeção e ausência de JavaScript verificados.');
 } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1});
