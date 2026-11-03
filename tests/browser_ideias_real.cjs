// Curso real: ação a partir das chaves existentes e apoio sem desmontar a sessão.
const fs=require('fs'),path=require('path'),assert=require('node:assert/strict'),{chromium}=require('playwright');
const root=path.resolve(__dirname,'..'),base='https://pedrohfernandes-klk.github.io/lente/',out=process.env.IDEIAS_PROVAS||path.join(require('os').tmpdir(),'ideias-real');fs.mkdirSync(out,{recursive:true});
(async()=>{const b=await chromium.launch({executablePath:process.env.CHROME_PATH}),rows=[];
async function context(width,dark,proj,states={}){const c=await b.newContext({viewport:{width,height:900},colorScheme:dark?'dark':'light',reducedMotion:'reduce'});
 await c.route('**/*',r=>{const u=r.request().url();if(!u.startsWith(base))return r.abort();let f=decodeURIComponent(u.slice(base.length).split('?')[0]);if(!f||f.endsWith('/'))f+='index.html';f=path.resolve(root,f);if(!f.startsWith(root+path.sep)||!fs.existsSync(f))return r.fulfill({status:404,body:''});return r.fulfill({contentType:({'.html':'text/html; charset=utf-8','.js':'application/javascript','.json':'application/json','.css':'text/css','.svg':'image/svg+xml'})[path.extname(f)]||'application/octet-stream',body:fs.readFileSync(f)});});
 await c.addInitScript(states=>{if(!sessionStorage.getItem('qa-semeado')){for(const [k,v] of Object.entries(states))localStorage.setItem(k,JSON.stringify(v));sessionStorage.setItem('qa-semeado','1')}},states);return c;}
try{
for(const width of [320,390,1366])for(const dark of [false,true])for(const proj of [false,true]){
 const states={'epi-lab-ideias-s01':{versao:'anterior',lida:true,t:1700000000000}},c=await context(width,dark,proj,states),p=await c.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
 for(const page of ['', 'narrativas/']){await p.goto(base+page+(proj?'?projetar=1':''));const a=p.locator('[data-ideias-acao]');await a.waitFor();await p.waitForTimeout(150);
 assert.equal(await a.textContent(),proj?'Começar Ideias →':'Continuar Ideias →');assert.match(await a.getAttribute('href'),proj?/sessao-01/:/sessao-02/);
 assert.deepEqual(await p.evaluate(()=>JSON.parse(localStorage.getItem('epi-lab-ideias-s01'))),states['epi-lab-ideias-s01']);
 assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);assert.deepEqual(errors,[]);
 if(page){assert.equal(await p.locator('h1').textContent(),'Ideias');assert.equal(await p.locator('#explorar a').count(),11);assert.equal(await p.locator('.ideias-portugues a').getAttribute('href'),'https://pedrohfernandes-klk.github.io/pt/'+(proj?'?projetar=1':''));await p.locator('#explorar details').evaluateAll(ds=>ds.forEach(d=>d.open=true));assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);}
 await p.screenshot({path:path.join(out,`${page?'lab':'lente'}-${width}-${dark}-${proj}.png`)});rows.push({page,width,dark,proj});
 }await c.close();
}
for(const [states,label,dest] of [[{},'Começar Ideias →','01'],[{'epi-lab-ideias-s01':{lida:true},'epi-lab-ideias-s02':{antes:{lida:true}}},'Rever Ideias →','01']]){
 const c=await context(390,false,false,states),p=await c.newPage();await p.goto(base+'narrativas/');await p.waitForTimeout(150);assert.equal(await p.locator('[data-ideias-acao]').textContent(),label);assert.match(await p.locator('[data-ideias-acao]').getAttribute('href'),new RegExp('sessao-'+dest));await c.close();
}
for(const width of [320,1366]){
 const c=await context(width,false,false),p=await c.newPage();await p.goto(base+'narrativas/ideias/sessao-01/');
 for(let i=0;i<3;i++)await p.locator('.casca-acoes button',{hasText:/Seguinte/}).click();
 await p.locator('.op[data-j="0"]').click();
 const before=await p.locator('#baralho').innerHTML(),position=await p.locator('[data-c-num]').textContent(),storage=await p.evaluate(()=>JSON.stringify(Object.entries(localStorage).sort()));
 await p.getByRole('button',{name:'Abrir apoios',exact:true}).click();await p.getByRole('link',{name:'Recurso desta sessão: Galileu',exact:true}).click();
 const dialog=p.getByRole('dialog',{name:'Recurso da sessão: Galileu'});await dialog.waitFor();const frame=p.frameLocator('dialog iframe');await frame.locator('.epi-retomar-ideias').waitFor();
 await p.screenshot({path:path.join(out,`recurso-${width}.png`)});await frame.locator('.epi-retomar-ideias').click();await dialog.waitFor({state:'detached'});
 assert.equal(await p.locator('#baralho').innerHTML(),before);assert.equal(await p.locator('[data-c-num]').textContent(),position);assert.equal(await p.evaluate(()=>JSON.stringify(Object.entries(localStorage).sort())),storage);await c.close();
}
fs.writeFileSync(path.join(out,'resultado.json'),JSON.stringify(rows,null,2));console.log('PASS 24 entradas, início/conclusão e dois regressos à resposta conservada');
}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
