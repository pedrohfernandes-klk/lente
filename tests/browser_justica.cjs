'use strict';
// 02/11/2026: três lições, três larguras e projeção; progresso antigo e vídeos só ao toque.
const {chromium}=require('playwright'), fs=require('fs'), path=require('path'), assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'..'), OUT=process.env.JUSTICA_QA||path.join(ROOT,'../justica-qa');
fs.mkdirSync(OUT,{recursive:true});
const manifest=JSON.parse(fs.readFileSync(path.join(ROOT,'tools/justica/licoes.json'),'utf8'));
const BASE='https://pedrohfernandes-klk.github.io/lente/';
const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.webp':'image/webp'};
const clean=s=>s.replace(/\*\*|_/g,'');
(async()=>{
 const browser=await chromium.launch(process.env.JUSTICA_CHROME?{executablePath:process.env.JUSTICA_CHROME}:{});let total=0;
 try {
  // Comparação visual dos desenhos publicados, antes de qualquer redesenho.
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  let h='<style>body{font:16px Arial;color:#000;background:#fff}main{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}figure{margin:15px 0;border:1px solid #bbb;padding:10px}svg{width:100%;height:190px}figcaption{font-size:13px}</style><main>';
  for(const m of manifest){const bank=JSON.parse(fs.readFileSync(path.join(ROOT,`tools/justica/bancos/licao-${m.numero}.json`),'utf8'));h+=`<section><h2>Lição ${m.numero}</h2>`;let figs=0;for(const [i,x] of bank.entries())for(const f of (x.html||'').matchAll(/<figure\b[^>]*>[\s\S]*?<\/figure>/g)){h+=`<p>Cartão ${i+1}</p>`+f[0];figs++}if(!figs)h+='<p>Sem desenhos publicados.</p>';h+='</section>';}h+='</main>';
  await page.setContent(h);await page.screenshot({path:path.join(OUT,'desenhos-antes.png'),fullPage:true});await page.close();
  for(const m of manifest)for(const width of [320,390,1366])for(const projection of [false,true]){
   const ctx=await browser.newContext({viewport:{width,height:900}});const p=await ctx.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
   await ctx.route('**/*',r=>{const u=r.request().url();if(!u.startsWith(BASE))return r.abort();let rel=decodeURIComponent(u.slice(BASE.length).split('?')[0]);if(rel.endsWith('/'))rel+='index.html';const f=path.resolve(ROOT,rel);if(!f.startsWith(ROOT+path.sep)||!fs.existsSync(f))return r.fulfill({status:404,body:''});return r.fulfill({status:200,contentType:mime[path.extname(f)]||'application/octet-stream',body:fs.readFileSync(f)});});
   const saved={lida:true,melhor:7,totalMelhor:8,tentativas:2};
   await ctx.addInitScript(({key,saved})=>{if(window.top!==window||location.hostname!=='pedrohfernandes-klk.github.io')return;if(!sessionStorage.getItem('justica-teste'))localStorage.setItem(key,JSON.stringify(saved));},{key:m.chave,saved});
   await p.goto(BASE+`olhar-e-decidir/justica/licao-${m.numero}/`+(projection?'?projetar=1':''));
   assert.equal(await p.locator('iframe').count(),0);
   // Um progresso concluído continua legível e não é apagado ao abrir.
   assert.equal(await p.evaluate(k=>JSON.parse(localStorage.getItem(k)).melhor,m.chave),7);
   await p.evaluate(k=>{localStorage.removeItem(k);sessionStorage.setItem('justica-teste','1');},m.chave);
   await p.reload();
   if(projection)await p.evaluate(({key,saved})=>localStorage.setItem(key,JSON.stringify(saved)),{key:m.chave,saved});
   const bank=JSON.parse(fs.readFileSync(path.join(ROOT,`tools/justica/bancos/licao-${m.numero}.json`),'utf8'));
   for(let i=0;i<bank.length;i++){
    await p.locator('#baralho .cartao').first().waitFor();
    const norm=s=>clean(String(s||'').replace(/<[^>]+>/g,' ')).replace(/\s+/g,' ').trim();
    const visible=norm(await p.locator('#baralho').innerText());
    const matches=bank.filter(x=>x.t!=='ler'&&[x.p,x.p2].some(q=>q&&visible.includes(norm(q))));
    const x=bank[i].t==='ler'?bank[i]:(matches.length===1?matches[0]:bank[i]);
    const label=`L${m.numero} C${i+1} ${width} ${projection}`;
    const overflow=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);assert.equal(overflow,false,label);
    if(x.t==='ler'){
     const v=p.locator('#baralho .ju-video');
     if(await v.count()){const d=await v.evaluate(e=>({...e.dataset}));await v.locator('button').click();const src=await v.locator('iframe').getAttribute('src');assert.ok(src.startsWith('https://www.youtube-nocookie.com/embed/'+m.video));assert.ok(src.includes('&start='+d.ini)&&src.includes('&end='+d.fim));}
     await p.locator('#baralho details').evaluateAll(ds=>ds.forEach(d=>d.open=true));
     if((m.numero===2&&i===17)||(m.numero===1&&i===10))await p.screenshot({path:path.join(OUT,`l${m.numero}-c${i+1}-${width}-${projection}.png`)});
     await p.locator('[data-c-acoes] [data-seguinte]').click();
    }else{
     if(x.t==='escolha')await p.locator('#baralho .ops button.op').filter({hasText:clean(x.o[x.c])}).first().click();
     else if(x.t==='vf')await p.locator('#baralho .ops button.op').filter({hasText:x.v?'Verdadeiro':'Falso'}).click();
     else if(x.t==='ordenar')for(const passo of x.passos)await p.locator('#baralho .soltos button.op').filter({hasText:clean(passo)}).first().click();
     else if(x.t==='emparelhar'){
      const colunas=await p.locator('#baralho .classes').count();
      for(let j=0;j<x.pares.length;j++){
       await p.locator('#baralho [data-e="'+j+'"]').click();
       if(colunas)await p.locator('#baralho .regiao .cab').filter({hasText:clean(x.pares[j][1])}).first().click();
       else await p.locator('#baralho [data-d="'+j+'"]').click();
      }
     }else throw Error('Tipo não tratado: '+x.t);
     await p.locator('[data-c-folha]:not([hidden]) [data-seguinte]').waitFor();
     if(m.numero===1&&i===10)await p.screenshot({path:path.join(OUT,`l1-c11-${width}-${projection}.png`)});
     await p.locator('[data-c-folha]:not([hidden]) [data-seguinte]').click();
    }
    total++;
   }
   await p.locator('.cartao.fim').waitFor();assert.deepEqual(errors,[]);
   const after=await p.evaluate(k=>JSON.parse(localStorage.getItem(k)),m.chave);
   // 02/11/2026: o motor publicado também grava ao concluir com ?projetar=1.
   // A fase 0 preserva esse comportamento; a casca e o motor são verificados contra o SHA de origem.
   assert.equal(after.lida,true);
   assert.equal(after.totalMelhor,bank.filter(x=>x.t!=='ler').length);
   console.log(`L${m.numero}: ${width}px, projeção ${projection}, ${bank.length} cartões`);await ctx.close();
  }
  console.log(`${total} cartões percorridos; sem erros JavaScript nem deslocamento horizontal.`);
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
