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
 // 07/11/2026: decisões 153, 176 e 177, a porta passa a ter também o «i» do crédito da imagem (details.info-i); a dobra é a details.cz-fold.
 // 12/11/2026: pedido entrada-temas. A região #inicio-narrativas é agora o cartão do tema 03 («Histórias e criação»), sem dobra: a
 // ligação ao Ideias fica sempre à vista, sem abrir nada (antes, no telemóvel, podia ser preciso abrir a porta).
 if(!pagePath){assert.equal(await region.count(),1);assert.equal(await region.locator('details:not(.info-i)').count(),0,'sem dobras no cartão');assert.equal(await region.evaluate(e=>e.matches('article.tm')),true)}
 const a=pagePath?region.locator('a').filter({hasText:/^Abrir Ideias/}):region.locator('a[href*="narrativas/ideias/"]');assert.equal(await a.count(),1);assert.ok(await a.isVisible());assert.equal(await a.evaluate(e=>new URL(e.href).pathname),'/lente/narrativas/ideias/');
 // 02/11/2026: Ideias não recebe o estado da porta Observar; a retoma original mantém a associação.
 if(!pagePath&&mode!=='projection'){
  // 12/11/2026: pedido entrada-temas. As três portas do catálogo saíram da entrada (estão no mapa e no Laboratório, onde o percurso
  // atual continua a receber «A seguir»: tests/browser_cartaz_familia.cjs). Na entrada, a retoma
  // já não tem portas a que dar estado: nem o Ideias nem nenhum outro elemento recebe estado, e o texto da ligação é o das outras
  // páginas públicas.
  assert.equal(await a.locator('.cz-state').count(),0);
  assert.equal(await p.locator('[data-cartaz-entrada] .cz-state').count(),0);
  assert.equal((await a.innerText()).trim(),'Ideias: o método em cinco passos');
  await a.scrollIntoViewIfNeeded();
  assert.ok(await a.evaluate(e=>{const r=e.getBoundingClientRect(),x=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return x===e||e.contains(x);}),'a ligação ao Ideias fica por cima da ligação do cartão');
 }
 const r=await a.boundingBox();assert.ok(r.height>=44);
 if(pagePath){for(const n of ['01','02'])assert.equal(await region.locator('a[href*="ideias/sessao-'+n+'/"]').count(),1);assert.equal(await region.locator('a').count(),3)}
 assert.deepEqual(errors,[]);
 if(process.env.IDEIAS_PROVAS){fs.mkdirSync(process.env.IDEIAS_PROVAS,{recursive:true});await p.screenshot({path:path.join(process.env.IDEIAS_PROVAS,(pagePath?'laboratorio':'lente')+'-'+width+'-'+mode+'.png'),fullPage:true})}
 rows.push({pagePath,width,mode,...dimensions,errors});await ctx.close();console.log('PASS',pagePath||'Lente',width,mode);
}
if(process.env.IDEIAS_PROVAS)fs.writeFileSync(path.join(process.env.IDEIAS_PROVAS,'medidas.json'),JSON.stringify(rows,null,2));
}finally{await b.close();server.closeAllConnections();server.close()}})().catch(e=>{console.error(e);process.exitCode=1});
