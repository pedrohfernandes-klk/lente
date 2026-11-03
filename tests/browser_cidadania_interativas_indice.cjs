// Índice real, chaves anteriores intactas, projeção sem leitura e alternativa em papel.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict'),{chromium}=require('playwright');
const root=path.resolve(__dirname,'..'),out=process.env.INDICE_PROVAS||path.join(require('os').tmpdir(),'cidadania-indice');fs.mkdirSync(out,{recursive:true});
const server=http.createServer((q,r)=>{let u=decodeURIComponent(q.url.split('?')[0]).replace(/^\/lente/,'');if(u.endsWith('/'))u+='index.html';const f=path.resolve(root,'.'+u);if(!f.startsWith(root+path.sep)||!fs.existsSync(f)){r.writeHead(404);return r.end()}r.setHeader('content-type',({'.html':'text/html; charset=utf-8','.js':'application/javascript','.css':'text/css'})[path.extname(f)]||'application/octet-stream');r.end(fs.readFileSync(f));});
(async()=>{await new Promise(r=>server.listen(0,r));const base='http://localhost:'+server.address().port+'/lente/',browser=await chromium.launch(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{});try{
for(const width of [320,390,1366])for(const dark of [false,true])for(const proj of [false,true]){
 const ctx=await browser.newContext({viewport:{width,height:900},colorScheme:dark?'dark':'light'}),p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
 await ctx.addInitScript(()=>{for(let n=1;n<=10;n++)localStorage.setItem('epi-cid-m1-s'+String(n).padStart(2,'0'),JSON.stringify({lida:true,versao:'antiga',exposicoes:{4:9},resposta:'ANTIGA'}));localStorage.setItem('lente-cidadania-m1-sessoes-v2',JSON.stringify({version:2,sessions:{'03':{done:true,stage:4},'05':{done:true}}}));const get=Storage.prototype.getItem;window.qaLeituras=[];Storage.prototype.getItem=function(k){qaLeituras.push(k);return get.call(this,k)};});
 await p.goto(base+'cidadania/m1/'+(proj?'?projetar=1':''));await p.waitForTimeout(100);
 assert.equal(await p.locator('[data-session-card]').count(),10);assert.equal(await p.locator('[data-continue]').getAttribute('href'),'licoes/01/');
 if(proj)assert.deepEqual(await p.evaluate(()=>qaLeituras.filter(k=>/^(epi-cid|lente-cidadania)/.test(k))),[]);
 else{assert.equal(await p.locator('[data-count]').textContent(),'0 de 10 sessões interativas feitas');assert.match(await p.locator('[data-session-card="03"] [data-status]').textContent(),/Registo anterior conservado/);}
 const antigo=await p.evaluate(()=>JSON.stringify(Object.entries(localStorage).sort()));
 assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await p.screenshot({path:path.join(out,`indice-${width}-${dark}-${proj}.png`)});
 if(!proj){await p.evaluate(()=>localStorage.setItem('epi-cid-m1-s01-20261103',JSON.stringify({lida:true,versao:'2026-11-03-real-1'})));await p.reload();assert.equal(await p.locator('[data-continue]').getAttribute('href'),'licoes/02/');
  // 03/11/2026: os registos do lote 01 a 04 retomam na sessão 05.
  await p.evaluate(()=>{for(let n=2;n<=4;n++)localStorage.setItem('epi-cid-m1-s'+String(n).padStart(2,'0')+'-20261103',JSON.stringify({lida:true,versao:'2026-11-03-real-1'}));});await p.reload();assert.equal(await p.locator('[data-continue]').getAttribute('href'),'licoes/05/');
  await p.evaluate(()=>{for(let n=2;n<=10;n++)localStorage.setItem('epi-cid-m1-s'+String(n).padStart(2,'0')+'-20261103',JSON.stringify({lida:true,versao:'2026-11-03-real-1'}));});await p.reload();assert.equal(await p.locator('[data-continue]').textContent(),'Rever as dez sessões');
 }
 const agora=await p.evaluate(()=>JSON.stringify(Object.entries(localStorage).filter(([k])=>!/^epi-cid-m1-s(0[1-9]|10)-20261103$/.test(k)).sort()));assert.equal(agora,antigo);
 for(const name of ['docente','guiao']){await p.goto(base+'cidadania/m1/licoes/'+name+'/');assert.equal(await p.locator('main>section').count(),10);assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await p.screenshot({path:path.join(out,`${name}-${width}-${dark}-${proj}.png`)});}
 assert.deepEqual(errors,[]);await ctx.close();
}
const ctx=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}}),p=await ctx.newPage();for(const n of ['01','02','03','04','05','06','07','08','09','10']){await p.goto(base+'cidadania/m1/licoes/'+n+'/');assert(await p.getByRole('link',{name:'Ler os materiais',exact:true}).isVisible());assert(await p.getByRole('link',{name:'Registo breve em papel',exact:true}).isVisible());}await ctx.close();
console.log('PASS 12 índices e guiões; retoma real, anteriores intactos, projeção sem leituras pessoais e dez alternativas sem JavaScript');
}finally{await browser.close();server.closeAllConnections();server.close()}})().catch(e=>{console.error(e);process.exitCode=1});
