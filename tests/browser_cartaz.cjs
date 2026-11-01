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
<section class="cz-next"><h2>A seguir</h2><p>Continua a leitura.</p><a class="cz-button primary" href="#destino">Continuar</a></section>
<button class="cz-button">Voltar</button><button class="cz-button" disabled>Indisponível</button>
<div class="cz-grid"><article class="cz-door"><a href="#destino"><h2>Observar</h2><span>Descobre os percursos.</span><span class="arrow">→</span></a></article></div>
<a class="cz-row" href="#destino"><b>1</b><span>Percurso</span><span class="cz-state current">A seguir</span><span>→</span></a>
<p class="cz-credit"><a href="https://commons.wikimedia.org/" data-external aria-label="Wikimedia Commons, sítio externo">Wikimedia Commons</a></p>
<nav class="cz-crumbs"><a href="#destino">Início</a><span aria-current="page">Observar</span></nav>
<span class="cz-state"></span><span class="cz-state done">Feita 01/11</span>
<details class="cz-fold" open><summary>Primeira banda</summary><p id="destino">Conteúdo da primeira banda</p></details>
<details class="cz-fold" open><summary>Segunda banda</summary><p data-cz-next>A seguir</p></details>
<details class="cz-fold" open><summary>Terceira banda</summary><p id="alvo">Conteúdo da âncora</p></details>
<footer class="cz-footer"><a href="#destino">Início <span>→</span></a></footer>
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
   for (const selector of ['.cz-button','.cz-row','.cz-door>a','.cz-credit a','.cz-crumbs a','.cz-footer a','.cz-fold>summary']) {
    const sizes = await page.locator(selector).evaluateAll(es=>es.map(e=>{const r=e.getBoundingClientRect();return [r.width,r.height]}));
    for(const [w,h] of sizes) assert.ok(w>=44 && h>=(selector==='.cz-button'?48:44),`${selector}: ${w}×${h}`);
   }
   assert.equal(await page.locator('.cz-fold>summary').first().evaluate(e=>e.getBoundingClientRect().height),88);
   assert.equal(await page.locator('.cz-state:empty').evaluate(e=>getComputedStyle(e).display),'none');
   for(const selector of ['.cz-row','.cz-door>a','.cz-credit a','.cz-button']) {
    assert.equal(await page.locator(selector).first().evaluate(e=>getComputedStyle(e).textDecorationLine),'none');
   }
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
