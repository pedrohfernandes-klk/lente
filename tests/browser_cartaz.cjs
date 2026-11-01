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
<p class="cz-credit">Fotografia em <a href="https://commons.wikimedia.org/" data-external aria-label="Wikimedia Commons, sítio externo">Wikimedia Commons</a>.</p>
<nav class="cz-crumbs"><a href="#destino">Início</a><span aria-current="page">Observar</span></nav>
<span class="cz-state"></span><span class="cz-state done">Feita 01/11</span>
<details class="cz-fold" open><summary>Primeira banda</summary><p id="destino">Conteúdo da primeira banda</p></details>
<details class="cz-fold" open><summary>Segunda banda</summary><p data-cz-next>A seguir</p></details>
<details class="cz-fold" open><summary>Terceira banda</summary><p id="alvo">Conteúdo da âncora</p></details>
<footer class="cz-footer"><nav class="cz-footer-links" aria-label="Saídas"><a href="#destino">Início <span>→</span></a></nav><p class="cz-prose">Texto do rodapé com <a href="#destino">ligação</a>.</p></footer>
</main></body></html>`;
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
   for (const selector of ['.cz-button','.cz-row','.cz-door>a','.cz-credit a','.cz-crumbs a','.cz-footer-links a','.cz-fold>summary']) {
    const sizes = await page.locator(selector).evaluateAll(es=>es.map(e=>{const r=e.getBoundingClientRect();return [r.width,r.height]}));
    for(const [w,h] of sizes) assert.ok(w>=44 && h>=(selector==='.cz-button'?48:44),`${selector}: ${w}×${h}`);
   }
   assert.equal(await page.locator('.cz-fold>summary').first().evaluate(e=>e.getBoundingClientRect().height),88);
   assert.equal(await page.locator('.cz-state:empty').evaluate(e=>getComputedStyle(e).display),'none');
   for(const selector of ['.cz-row','.cz-door>a','.cz-credit a','.cz-button']) {
    assert.equal(await page.locator(selector).first().evaluate(e=>getComputedStyle(e).textDecorationLine),'none');
   }
   // 01/11/2026: revisão curta. A ligação do crédito fica em linha e não muda a entrelinha da frase.
   const credit = await page.locator('.cz-credit').evaluate(e=>({h:e.getBoundingClientRect().height,lh:parseFloat(getComputedStyle(e).lineHeight),display:getComputedStyle(e.querySelector('a')).display}));
   assert.equal(credit.display,'inline');
   assert.ok(credit.h<44 && Math.abs(credit.h-credit.lh*Math.round(credit.h/credit.lh))<.5,`crédito: ${credit.h} px para linhas de ${credit.lh} px`);
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
   // 01/11/2026: revisão curta. Em projeção (classe do sistema), só degraus da escala: 20 e 16 px com a raiz a 16 px;
   // o antetítulo fica abaixo de 65 % do título da região «A seguir».
   await page.evaluate(()=>document.documentElement.classList.add('em-projecao'));
   const projected = await page.evaluate(()=>{const size=s=>parseFloat(getComputedStyle(document.querySelector(s)).fontSize);return {root:size('[data-cartaz="2"]'),label:size('.cz-label'),credit:size('.cz-credit'),state:size('.cz-state:not(:empty)'),crumbs:size('.cz-crumbs'),prose:size('.cz-prose'),button:size('.cz-button'),title:size('.cz-next h2')};});
   assert.deepEqual(projected,{root:20,label:16,credit:16,state:16,crumbs:16,prose:20,button:20,title:25});
   assert.ok(projected.label<=.65*projected.title,`antetítulo ${projected.label} px para título de ${projected.title} px`);
   assert.equal(await page.evaluate(()=>localStorage.length),0);
   assert.equal(await page.evaluate(()=>Math.max(0,document.documentElement.scrollWidth-innerWidth)),0);
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
