const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
global.window={};require('../assets/formas/tres-cartas-dados.js');const D=window.LenteTresCartasDados;
const root=path.resolve(__dirname,'..'),out=fs.mkdtempSync(path.join(require('node:os').tmpdir(),'baralho-'));console.log('Capturas e PDF: '+out);
const server=http.createServer((req,res)=>{let f=path.join(root,decodeURIComponent(req.url.split('?')[0]));if(fs.existsSync(f)&&fs.statSync(f).isDirectory())f=path.join(f,'index.html');if(!fs.existsSync(f)){res.writeHead(404).end();return;}res.setHeader('Content-Type',({'.js':'application/javascript','.css':'text/css','.html':'text/html','.webp':'image/webp'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}/narrativas/formas/tres-cartas/`;const browser=await chromium.launch();
try{for(const width of [320,390,1366]){
 const ctx=await browser.newContext({viewport:{width,height:844},reducedMotion:'reduce'});const p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));await p.goto(base);
 const snap=async name=>{if(width===390)await p.screenshot({path:path.join(out,name+'.png')});};
 await snap('01-primeiro');const firstBox=await p.locator('[data-op]').last().boundingBox();assert(firstBox.y+firstBox.height<844);assert.equal(await p.locator('meta[name=robots]').getAttribute('content'),'noindex');
 await p.evaluate(()=>localStorage.setItem('epi-corta','preservar'));
 for(let i=0;i<24;i++){
  const card=p.locator('[data-cartao]'),id=await card.getAttribute('data-cartao'),type=await card.getAttribute('data-tipo');
  assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${width}/${id}`);

  if(['sombra','horizonte','rampa'].includes(id)){const im=p.locator('#cartoes img');assert(await im.evaluate(x=>x.complete&&x.naturalWidth===512&&x.naturalHeight===512));assert(await im.getAttribute('alt'));}
  if(['escolher','completar','classificar','autoavaliacao'].includes(type)){
   if(id==='ligacao')await snap('04-escolha');
   const c=D.cartoes.find(c=>c.id===id);
   if(c.certa){await p.locator('[data-op]').filter({hasText:c.opcoes.find(o=>o.id!==c.certa).texto}).click();assert(await p.locator('[data-seguinte]').isDisabled());await p.locator('.casca-folha button').click();}
   await p.locator(c.certa?'[data-op="'+c.certa+'"]':'[data-op]').first().focus();await p.keyboard.press('Enter');
   assert(await p.locator('.casca-folha').isVisible());await p.locator('.casca-folha button').click();
  }else if(type==='ordenar'){
   for(let j=0;j<3;j++){await p.locator('[data-ord]').last().focus();await p.keyboard.press('Enter');}
   assert.equal(await p.locator('.tc-ordem li').count(),3);
  }else if(type==='composicao'){
   assert.match(await p.locator('.tc-plano').last().innerText(),/Uma ação provoca a seguinte/);
   assert.match(await p.locator('.tc-plano').last().innerText(),/Primeiro, inventar a passagem; depois, transportar a linha; por fim, autorizar a mudança[.]/);
   assert.deepEqual(await p.locator('.tc-plano').last().locator('h3').allTextContents(),['O conto','A notícia']);
   assert.match(await p.locator('.tc-plano').last().innerText(),/Para ligar causa e consequência: Por isso/);
   if(id==='plano'){
    await ctx.grantPermissions(['clipboard-read','clipboard-write']);await p.locator('[data-copiar]').click();assert.equal((await p.evaluate(()=>navigator.clipboard.readText())).replace(/\s+/g,' ').trim(),(await p.locator('.tc-plano').innerText()).replace(/\s+/g,' ').trim());await snap('15-composicao');const before=await p.evaluate(()=>JSON.parse(localStorage.getItem('lente-formas-v1')).itens['tres-cartas']);assert(before.experimentei);assert.equal(before.primeira.arrumacao.ordem,'cba');
    await p.reload();assert.equal(await p.locator('[data-cartao]').getAttribute('data-cartao'),'plano');
   }else{
    for(let j=0;j<18;j++)await p.getByRole('button',{name:'Cartão anterior',exact:true}).click();
    assert.equal(await p.locator('[data-cartao]').getAttribute('data-cartao'),'ligacao');
    await p.locator('[data-op="b"]').click();await p.locator('.casca-folha button').click();
    for(let j=0;j<18;j++)await p.locator('[data-seguinte]').click();
    assert.match(await p.locator('.tc-plano').first().innerText(),/Uma ação provoca a seguinte/);
    assert.match(await p.locator('.tc-plano').last().innerText(),/As ações partilham uma ideia/);
    assert.doesNotMatch(await p.locator('.tc-plano').last().innerText(),/Para ligar causa e consequência|Por isso/);
    assert.match(await p.locator('.tc-plano').first().innerText(),/Para ligar causa e consequência: Por isso/);
    await p.locator('[data-copiar]').click();assert.equal((await p.evaluate(()=>navigator.clipboard.readText())).replace(/\s+/g,' ').trim(),(await p.locator('.tc-plano').last().innerText()).replace(/\s+/g,' ').trim());
    assert.equal(await p.evaluate(()=>JSON.parse(localStorage.getItem('lente-formas-v1')).itens['tres-cartas'].primeira.arrumacao.ligacao),'a');
    await p.locator('[data-comparar]').click();assert(await p.evaluate(()=>JSON.parse(localStorage.getItem('lente-formas-v1')).itens['tres-cartas'].revi));}
  }else if(type==='escrita'){if(id==='conto')await snap('16-escrita');await p.locator('[data-escrevi]').click();await p.locator('.casca-folha button').click();}
  if(id==='exnoticia')break;
  await p.locator('[data-seguinte]').click();
 }
 assert.match(await p.locator('#cartoes').innerText(),/CC BY-SA 4.0/);assert.equal(await p.evaluate(()=>localStorage.getItem('epi-corta')),'preservar');
 if(width===390){await p.emulateMedia({media:'print'});assert(await p.locator('.tc-print').isVisible());await p.pdf({path:path.join(out,'papel.pdf'),format:'A4',printBackground:true});await p.emulateMedia({media:'screen'});}
 const ls=await p.evaluate(()=>JSON.stringify(localStorage)),ss=await p.evaluate(()=>JSON.stringify(sessionStorage));
 await p.goto(base+'?projetar=1');assert.equal(await p.locator('[data-cartao]').getAttribute('data-cartao'),'sombra');assert.equal(await p.locator('[data-op][aria-pressed=true]').count(),0);
 await p.locator('[data-op]').last().click();assert.equal(await p.evaluate(()=>JSON.stringify(localStorage)),ls);assert.equal(await p.evaluate(()=>JSON.stringify(sessionStorage)),ss);
 assert.deepEqual(errors,[]);await ctx.close();console.log(`OK ${width}px: percurso, imagens, teclado, progresso, projeção e largura`);
 }
}finally{await browser.close();server.close();}})().catch(e=>{console.error(e);process.exitCode=1;server.close();});
