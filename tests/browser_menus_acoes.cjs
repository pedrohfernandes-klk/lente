const fs=require('fs'),path=require('path'),assert=require('assert'),{chromium}=require('playwright');
const root=path.resolve(__dirname,'..'),base='https://pedrohfernandes-klk.github.io/lente/';
async function route(c){await c.route('**/*',r=>{const u=new URL(r.request().url());if(!u.pathname.startsWith('/lente/'))return r.abort();let f=path.resolve(root,u.pathname.slice(7));if(u.pathname.endsWith('/'))f=path.join(f,'index.html');if(!f.startsWith(root+path.sep)||!fs.existsSync(f))return r.abort();return r.fulfill({path:f});});}
(async()=>{const b=await chromium.launch({executablePath:process.env.CHROME_PATH});let count=0;try{
for(const file of ['index.html','narrativas/index.html'])for(const width of [320,390,1366])for(const projected of [false,true])for(const done of [0,1,2]){
 const c=await b.newContext({viewport:{width,height:900}});await route(c);await c.addInitScript(n=>{for(let i=1;i<=n;i++)localStorage.setItem('epi-lab-ideias-s0'+i,JSON.stringify({lida:true,t:1700000000000}));},done);
 const p=await c.newPage();let v=p;if(projected){await p.goto(base+'projetar/?pagina='+encodeURIComponent('/lente/'+file));v=await(await p.locator('#lesson-frame').elementHandle()).contentFrame();await v.waitForSelector('html.epi-projection');}else await p.goto(base+file);
 const a=v.locator('[data-ideias-acao]');await a.waitFor({state:'attached'});assert.match(await a.textContent(),new RegExp(projected||done===0?'Começar':done===1?'Continuar':'Rever'));assert.match(await a.getAttribute('href'),new RegExp('sessao-0'+(!projected&&done===1?2:1)+'/'));
 for(let i=1;i<=done;i++)assert.deepEqual(await v.evaluate(i=>JSON.parse(localStorage.getItem('epi-lab-ideias-s0'+i)),i),{lida:true,t:1700000000000});
 await c.close();count++;
}
for(const file of ['index.html','narrativas/index.html','mapa/index.html','ler/index.html']){
 const c=await b.newContext({viewport:{width:320,height:900},javaScriptEnabled:false});await route(c);const p=await c.newPage();await p.goto(base+file);assert(await p.locator('main a[href]').count()>0);if(file==='mapa/index.html'){const s=p.locator('.menu-apoios>summary');await s.click();assert(await s.evaluate(e=>e.parentElement.open));}await c.close();count++;
}
console.log('PASS '+count+' contextos: começar, continuar, rever, projeção e alternativa sem JavaScript');
}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
