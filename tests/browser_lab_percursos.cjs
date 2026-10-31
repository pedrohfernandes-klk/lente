// 30/10/2026: estado real, projeção, links, imagens de arquivo e quatro larguras.
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),D=require('../assets/laboratorio/percursos.json');
const out=process.env.LENTE_SHOTS||fs.mkdtempSync(path.join(require('node:os').tmpdir(),'lab-percursos-'));fs.mkdirSync(out,{recursive:true});
const server=http.createServer((req,res)=>{let f=path.join(root,decodeURIComponent(req.url.split('?')[0]));if(fs.existsSync(f)&&fs.statSync(f).isDirectory())f=path.join(f,'index.html');if(!fs.existsSync(f)){res.writeHead(404).end();return;}res.setHeader('Content-Type',({'.js':'application/javascript','.css':'text/css','.html':'text/html','.webp':'image/webp'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port;const b=await chromium.launch();
try{for(const width of [320,390,1366,1440]){const ctx=await b.newContext({viewport:{width,height:900},reducedMotion:'reduce'}),p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.goto(base+'/narrativas/');assert.match(await p.locator('[data-continuar]').innerText(),/^Começar: A forma/);
 await p.evaluate(()=>localStorage.setItem('epi-narrativas',JSON.stringify({feitas:{'aula-forma':123},privado:'RESPOSTA PRIVADA'})));
 await p.reload();assert.match(await p.locator('[data-continuar]').innerText(),/^Continuar: A pirâmide/);assert((await p.locator('[data-continuar]').getAttribute('href')).endsWith('/narrativas/piramide/'));
 if(width===390){const downloaded=p.waitForEvent('download');await p.locator('[data-guardar]').click();const file=await (await downloaded).path(),data=JSON.parse(fs.readFileSync(file,'utf8'));assert.deepEqual(data.registos,[{id:'aula-forma',estado:'feito'}]);assert(!fs.readFileSync(file,'utf8').includes('PRIVADA'));
  const restored={formato:'lente-laboratorio',versao:1,registos:[...data.registos,{id:'formas/certa-manha',estado:'revisto'}]};await Promise.all([p.waitForEvent('load'),p.locator('[data-repor]').setInputFiles({name:'progresso.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(restored))})]);assert.equal(await p.evaluate(()=>JSON.parse(localStorage.getItem('epi-narrativas')).privado),'RESPOSTA PRIVADA');assert(await p.evaluate(()=>JSON.parse(localStorage.getItem('lente-formas-v1')).itens['certa-manha'].revi>0));
  const before=await p.evaluate(()=>JSON.stringify({...localStorage}));await p.locator('[data-repor]').setInputFiles({name:'incorreto.json',mimeType:'application/json',buffer:Buffer.from('{"formato":"outro"}')});await p.waitForFunction(()=>document.querySelector('[data-registos-aviso]').textContent.includes('Não foi'));assert.equal(await p.evaluate(()=>JSON.stringify({...localStorage})),before);
 }
 await p.goto(base+'/narrativas/percursos/ordem/');assert.equal(await p.locator('[data-estado="aula-forma"]').innerText(),'feito');
 await p.goto(base+'/narrativas/?projetar=1');assert.match(await p.locator('[data-continuar]').innerText(),/^Começar:/);assert(!(await p.locator('body').innerText()).includes('RESPOSTA PRIVADA'));assert.equal(await p.evaluate(()=>JSON.parse(localStorage.getItem('epi-narrativas')).feitas['aula-forma']),123);
 await p.evaluate(()=>localStorage.clear());
 for(const url of ['/narrativas/','/narrativas/tudo/','/narrativas/ver/','/narrativas/treinar/','/narrativas/criar/',...D.routes.map(r=>'/narrativas/percursos/'+r.id+'/')]){
  await p.goto(base+url);assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),width+' '+url);
  if(url==='/narrativas/')for(const im of await p.locator('main img').all()){await im.scrollIntoViewIfNeeded();assert(await im.evaluate(i=>i.complete&&i.naturalWidth>0));assert((await im.getAttribute('alt')).length>25);}
  if([390,1366].includes(width)&&['/narrativas/','/narrativas/percursos/ordem/','/narrativas/tudo/'].includes(url)){await p.evaluate(()=>scrollTo(0,0));const n=url==='/narrativas/'?'entrada':url.includes('tudo')?'tudo':'percurso';await p.screenshot({path:path.join(out,n+'-'+width+'.png'),fullPage:true});}
 }
 await p.emulateMedia({colorScheme:'dark'});await p.goto(base+'/narrativas/');assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));if(width===390)await p.screenshot({path:path.join(out,'entrada-escuro-390.png')});
 assert.deepEqual(errors,[]);await ctx.close();console.log(width+' px: estado, projeção, imagens e 22 páginas sem deslocamento horizontal.');}
}finally{await b.close();server.close();}console.log('Capturas: '+out);})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
