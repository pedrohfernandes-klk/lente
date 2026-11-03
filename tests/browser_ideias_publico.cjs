// 01/11/2026: contratos das famílias migradas em navegador real.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..');
const lab=fs.existsSync(path.join(root,'assets/laboratorio/cartaz.js'));
const entry=fs.readFileSync(path.join(root,'index.html'),'utf8').includes('data-cartaz-entrada');
const unusedPages=[...(entry?['']:[]),...(lab?['narrativas/','narrativas/ver/','narrativas/treinar/','narrativas/criar/']:[])];
const server=http.createServer((req,res)=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname).replace(/^\/lente/,''));if(!f.startsWith(root+path.sep)&&f!==root){res.writeHead(403);return res.end();}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});
// 02/11/2026: decisão do docente (141): o «Ideias» é público e tem ligação a partir das páginas públicas
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
const b=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})}),rows=[];
try{for(const pagePath of ['','narrativas/'])for(const width of [320,390,1366])for(const mode of ['light','dark','projection']){
 const ctx=await b.newContext({viewport:{width,height:900},colorScheme:mode==='dark'?'dark':'light'}),p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.route('https://pedrohfernandes-klk.github.io/lente/**',async r=>{const u=new URL(r.request().url());await r.fulfill({response:await ctx.request.get(origin+u.pathname+u.search)})});
 await p.goto(origin+'/lente/'+pagePath+(mode==='projection'?'?projetar=1':''),{waitUntil:'networkidle'});
 const dimensions=await p.evaluate(()=>({height:document.documentElement.scrollHeight,overflow:Math.max(0,document.documentElement.scrollWidth-innerWidth)}));
 assert.equal(dimensions.overflow,0,pagePath+' '+width+' '+mode);
 if(width===390&&mode!=='projection')assert.ok(dimensions.height<3000,pagePath+' altura '+dimensions.height);
 const region=p.locator(pagePath?'.ideias-publico':'#inicio-narrativas');
 if(!pagePath){const fold=region.locator('details');if(!await fold.evaluate(e=>e.open))await fold.locator('summary').click()}
 // 03/11/2026: a ação abre a primeira sessão real; o curso fica como destino secundário.
 const a=region.locator('[data-ideias-acao]');assert.equal(await a.count(),1);assert.ok(await a.isVisible());assert.equal(await a.evaluate(e=>new URL(e.href).pathname),'/lente/narrativas/ideias/sessao-01/');
 assert.equal(await a.textContent(),'Começar Ideias →');assert.equal(await a.locator('.cz-state').count(),0);
 if(!pagePath&&mode!=='projection'){
  await p.waitForFunction(()=>document.querySelector('[data-cartaz-entrada]').dataset.retomaPronta==='true');
  assert.deepEqual(await region.locator('.ideias-recursos a').allTextContents(),['Observar','Treinar','Criar']);
  assert.equal(await region.locator('.ideias-recursos .current').count(),0);
 }
 const r=await a.boundingBox();assert.ok(r.height>=44);
 if(pagePath){const dados=JSON.parse(await region.locator('[data-ideias-sessoes]').textContent());assert.deepEqual(dados.map(x=>x.chave),['epi-lab-ideias-s01','epi-lab-ideias-s02']);assert.equal(await region.locator('a.ideias-mapa').count(),1);assert.equal(await region.locator('a.ideias-mapa').evaluate(e=>new URL(e.href).pathname),'/lente/narrativas/ideias/');assert.equal(await region.locator('nav>a').count(),1)}
 assert.deepEqual(errors,[]);
 if(process.env.IDEIAS_PROVAS){fs.mkdirSync(process.env.IDEIAS_PROVAS,{recursive:true});await p.screenshot({path:path.join(process.env.IDEIAS_PROVAS,(pagePath?'laboratorio':'lente')+'-'+width+'-'+mode+'.png'),fullPage:true})}
 rows.push({pagePath,width,mode,...dimensions,errors});await ctx.close();console.log('PASS',pagePath||'Lente',width,mode);
}
if(process.env.IDEIAS_PROVAS)fs.writeFileSync(path.join(process.env.IDEIAS_PROVAS,'medidas.json'),JSON.stringify(rows,null,2));
}finally{await b.close();server.closeAllConnections();server.close()}})().catch(e=>{console.error(e);process.exitCode=1});
