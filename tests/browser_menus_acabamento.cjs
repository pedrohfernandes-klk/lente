const fs=require('fs'),path=require('path'),assert=require('assert'),{chromium}=require('playwright');
const root=path.resolve(__dirname,'..'),before=path.resolve(root,'../lente-ideias-real-20261103');
const out=process.env.MENUS_PROVAS||path.resolve(root,'../lente-menus-acabamento-provas-20261103');
const pages=JSON.parse(fs.readFileSync(path.join(root,'tools/menus-acabamento-20261103.json'),'utf8'));
const selected=process.env.MENUS_PAGES?process.env.MENUS_PAGES.split(','):Object.keys(pages);assert(selected.every(x=>x in pages));
const targets='.ideias-recursos>a,.ferr-grupo li>a,.lista li>a,.catalogo li>a,.map-tree li>a,.saidas-sec>a,.cz-footer-links>a,.ideias-mapa,.guide-route>a,.ligacoes>a,.map-open p>a,.map-section>h2>a,.map-footer>a,.tambem>a';
(async()=>{fs.mkdirSync(out,{recursive:true});const browser=await chromium.launch({executablePath:process.env.CHROME_PATH});const phases=process.env.MENUS_PHASES?process.env.MENUS_PHASES.split(','):(fs.existsSync(before)?['antes','depois']:['depois']);assert(phases.every(x=>['antes','depois'].includes(x)));const saved=path.join(out,'resultados.json');const rows=fs.existsSync(saved)?JSON.parse(fs.readFileSync(saved,'utf8')).filter(r=>!phases.includes(r.phase)||!selected.includes(r.file)):[];
try{for(const phase of phases)for(const file of selected)for(const width of [320,390,1366])for(const mode of ['light','dark','projection-light','projection-dark']){
 const projected=mode.startsWith('projection'),dark=mode.endsWith('dark'),base=phase==='antes'?before:root;
 const context=await browser.newContext({viewport:{width,height:900},colorScheme:dark?'dark':'light',reducedMotion:'reduce'});
 await context.route('**/*',async route=>{const u=new URL(route.request().url());if(u.hostname!=='pedrohfernandes-klk.github.io'||!u.pathname.startsWith('/lente/'))return route.abort();let rel=decodeURIComponent(u.pathname.slice(7));if(!rel||rel.endsWith('/'))rel+='index.html';const f=path.resolve(base,rel);if(!f.startsWith(base+path.sep)||!fs.existsSync(f))return route.fulfill({status:404,body:'Not found'});return route.fulfill({path:f,contentType:({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml'})[path.extname(f)]});});
 const p=await context.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));let view=p;
 if(projected){await p.goto('https://pedrohfernandes-klk.github.io/lente/projetar/?pagina='+encodeURIComponent('/lente/'+file),{waitUntil:'load'});await p.locator('#lesson-frame').waitFor();view=await (await p.locator('#lesson-frame').elementHandle()).contentFrame();await view.waitForSelector('html.epi-projection');await view.waitForFunction(()=>!!document.querySelector('#epi-projection-frame-style')?.sheet);}
 else await p.goto('https://pedrohfernandes-klk.github.io/lente/'+file,{waitUntil:'load'});
 await view.evaluate(()=>document.fonts.ready);await p.waitForTimeout(100);
 const metrics=await view.evaluate(sel=>{const visible=e=>!!e.getClientRects().length;return {overflow:document.documentElement.scrollWidth-innerWidth,theme:document.documentElement.dataset.theme,projected:document.documentElement.className,targets:[...document.querySelectorAll(sel)].filter(visible).map(e=>({text:e.textContent.trim().slice(0,50),height:e.getBoundingClientRect().height,width:e.getBoundingClientRect().width})),storage:JSON.stringify(Object.entries(localStorage).sort())};},targets);
 const name=phase+'-'+file.replace(/\/index.html$|index.html$/,'').replaceAll('/','-')+'-'+width+'-'+mode;
 await p.screenshot({path:path.join(out,name+'.png'),fullPage:true,animations:'disabled'});
 if(phase==='depois'){
  assert.equal(await view.locator('body[data-menus-acabamento]').count(),1,'camada aplicada '+file);
  assert.deepEqual(errors,[],'erros JS '+file);if(projected)assert(metrics.projected.includes('epi-projection'));
  assert(metrics.overflow<=1,JSON.stringify({file,width,mode,overflow:metrics.overflow}));
  assert(metrics.targets.every(x=>x.height>=43.9),JSON.stringify({file,width,mode,small:metrics.targets.filter(x=>x.height<43.9)}));
  const a=view.locator(targets).filter({visible:true}).first();if(await a.count()){await a.focus();const focus=await a.evaluate(e=>({active:document.activeElement===e,outline:getComputedStyle(e).outlineStyle}));assert(focus.active&&focus.outline!=='none','focus '+file);}
  const details=view.locator('main details>summary').first();if(await details.count()&&await details.isVisible()){await details.focus();const old=await details.evaluate(e=>e.parentElement.open);await p.keyboard.press('Enter');// A entrada geral conserva dobras abertas em projeção e no ecrã largo (contrato publicado).
  const locked=file==='index.html'&&(projected||width>=640);assert.equal(await details.evaluate(e=>e.parentElement.open),locked?old:!old,JSON.stringify({file,width,mode,locked}));await p.keyboard.press('Enter');}
  if(file==='mapa/index.html'){const extra=view.locator('.menu-apoios>summary');await extra.focus();await p.keyboard.press('Enter');assert.equal(await extra.evaluate(e=>e.parentElement.open),true);assert.equal(await view.locator('.menu-apoios a').count(),6);await p.keyboard.press('Enter');}
  assert.equal(await view.evaluate(()=>JSON.stringify(Object.entries(localStorage).sort())),metrics.storage,'storage '+file);
 }
 rows.push({phase,file,width,mode,...metrics,errors,image:name+'.png'});fs.writeFileSync(path.join(out,'resultados.json'),JSON.stringify(rows,null,2));await context.close();console.log(name);
}
fs.writeFileSync(path.join(out,'comparacao.html'),'<!doctype html><meta charset="utf-8"><title>Menus do Lente: antes e depois</title><style>body{font:16px system-ui;max-width:1400px;margin:32px auto;padding:16px}section{display:grid;grid-template-columns:1fr 1fr;gap:16px}img{width:100%}summary{padding:16px;cursor:pointer}a{color:inherit}</style><h1>Menus do Lente: antes e depois</h1>'+rows.filter(r=>r.phase==='antes').map(r=>'<details><summary>'+r.file+' | '+r.width+' | '+r.mode+'</summary><section><figure><figcaption>Antes</figcaption><img loading="lazy" src="'+r.image+'"></figure><figure><figcaption>Depois</figcaption><img loading="lazy" src="'+r.image.replace('antes-','depois-')+'"></figure></section></details>').join(''));
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
