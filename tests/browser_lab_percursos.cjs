// 30/10/2026: estado real, projeção, links, imagens de arquivo e quatro larguras.
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),D=require('../assets/laboratorio/percursos.json');
const out=process.env.LENTE_SHOTS||fs.mkdtempSync(path.join(require('node:os').tmpdir(),'lab-percursos-'));fs.mkdirSync(out,{recursive:true});
const server=http.createServer((req,res)=>{let f=path.join(root,decodeURIComponent(req.url.split('?')[0]));if(fs.existsSync(f)&&fs.statSync(f).isDirectory())f=path.join(f,'index.html');if(!fs.existsSync(f)){res.writeHead(404).end();return;}res.setHeader('Content-Type',({'.js':'application/javascript','.css':'text/css','.html':'text/html','.webp':'image/webp'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port;const b=await chromium.launch(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{});
try{for(const width of [320,390,1366,1440]){const ctx=await b.newContext({viewport:{width,height:900},reducedMotion:'reduce'}),p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
 // 01/11/2026: título e ação são agora elementos separados da mesma região; ambos continuam obrigatórios.
 // 02/11/2026: decisão 134 (docente). Sem a caixa «A seguir»: a ligação de continuar fica escondida e a peça seguinte marca a linha do percurso atual.
 await p.goto(base+'/narrativas/');assert.equal(await p.locator('.cz-next').count(),0);assert(await p.locator('[data-continuar]').isHidden());assert((await p.locator('[data-continuar]').getAttribute('href')).endsWith('/narrativas/aula-forma/'));assert(JSON.parse(await p.locator('[data-cz-route].current').getAttribute('data-cz-route')).includes('aula-forma'));
 await p.evaluate(()=>localStorage.setItem('epi-narrativas',JSON.stringify({feitas:{'aula-forma':123},privado:'RESPOSTA PRIVADA'})));
 await p.reload();assert(await p.locator('[data-continuar]').isHidden());assert(JSON.parse(await p.locator('[data-cz-route].current').getAttribute('data-cz-route')).includes('piramide'));assert((await p.locator('[data-continuar]').getAttribute('href')).endsWith('/narrativas/piramide/'));
 if(width===390){
  // 02/11/2026: abrir os registos pelo teclado antes de usar os mesmos controlos.
  const reg=p.locator('.menu-registos');if(await reg.count()){await reg.locator('summary').focus();await p.keyboard.press('Enter');assert(await reg.evaluate(e=>e.open));}
  const downloaded=p.waitForEvent('download');await p.locator('[data-guardar]').click();const file=await (await downloaded).path(),data=JSON.parse(fs.readFileSync(file,'utf8'));assert.deepEqual(data.registos,[{id:'aula-forma',estado:'feito'}]);assert(!fs.readFileSync(file,'utf8').includes('PRIVADA'));
  const restored={formato:'lente-laboratorio',versao:1,registos:[...data.registos,{id:'formas/certa-manha',estado:'revisto'}]};await Promise.all([p.waitForEvent('load'),p.locator('[data-repor]').setInputFiles({name:'progresso.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(restored))})]);assert.equal(await p.evaluate(()=>JSON.parse(localStorage.getItem('epi-narrativas')).privado),'RESPOSTA PRIVADA');assert(await p.evaluate(()=>JSON.parse(localStorage.getItem('lente-formas-v1')).itens['certa-manha'].revi>0));
  // 30/10/2026: repor lê o aparelho no momento da reposição; o que outro separador gravou depois de abrir a página fica (revisão técnica).
  await p.goto(base+'/narrativas/');const outro=await ctx.newPage();await outro.goto(base+'/narrativas/tudo/');await outro.evaluate(()=>{const s=JSON.parse(localStorage.getItem('epi-narrativas'));s.feitas.espinha=456;localStorage.setItem('epi-narrativas',JSON.stringify(s));});await outro.close();
  await Promise.all([p.waitForEvent('load'),p.locator('[data-repor]').setInputFiles({name:'progresso.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify({formato:'lente-laboratorio',versao:1,registos:[{id:'desenlace',estado:'feito'}]}))})]);
  assert.deepEqual(await p.evaluate(()=>{const f=JSON.parse(localStorage.getItem('epi-narrativas')).feitas;return [f.espinha,f['aula-forma'],f.desenlace>0];}),[456,123,true]);
  const before=await p.evaluate(()=>JSON.stringify({...localStorage}));await p.locator('[data-repor]').setInputFiles({name:'incorreto.json',mimeType:'application/json',buffer:Buffer.from('{"formato":"outro"}')});await p.waitForFunction(()=>document.querySelector('[data-registos-aviso]').textContent.includes('Não foi'));assert.equal(await p.evaluate(()=>JSON.stringify({...localStorage})),before);
 }
 await p.goto(base+'/narrativas/percursos/ordem/');assert.equal(await p.locator('[data-estado="aula-forma"]').textContent(),'feito'); // 30/10/2026: textContent, porque o estado se mostra em caixa alta por CSS.
 // 30/10/2026: âncoras antigas levam ao percurso, no catálogo (revisão técnica).
 await p.goto(base+'/narrativas/#treinar-voz');await p.waitForURL('**/narrativas/tudo/#treinar-voz');assert(await p.locator('h3:has(#treinar-voz)').isVisible());assert(await p.evaluate(()=>{const r=document.getElementById('treinar-voz').parentElement.getBoundingClientRect();return r.top>=0&&r.top<innerHeight;}));
 await p.goto(base+'/narrativas/?projetar=1');assert(await p.locator('[data-continuar]').isHidden());assert((await p.locator('[data-continuar]').getAttribute('href')).includes('/narrativas/aula-forma/'));assert(JSON.parse(await p.locator('[data-cz-route].current').getAttribute('data-cz-route')).includes('aula-forma'));assert(!(await p.locator('body').innerText()).includes('RESPOSTA PRIVADA'));assert.equal(await p.evaluate(()=>JSON.parse(localStorage.getItem('epi-narrativas')).feitas['aula-forma']),123);
 await p.evaluate(()=>localStorage.clear());
 for(const url of ['/narrativas/','/narrativas/tudo/','/narrativas/ver/','/narrativas/treinar/','/narrativas/criar/',...D.routes.map(r=>'/narrativas/percursos/'+r.id+'/'),'/narrativas/percursos/'/* 30/10/2026: a 23.ª página gerada também entra. */]){
  await p.goto(base+url);assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),width+' '+url);
  // 02/11/2026: a porta inteira fecha no telemóvel; abrir pelo teclado antes de verificar a imagem, sem omitir nenhuma.
  if(url==='/narrativas/')for(const im of await p.locator('main img').all()){
   const block=im.locator('xpath=ancestor::*[contains(concat(" ",normalize-space(@class)," ")," bloco ")]'),fold=block.locator('details.dobra');
   const closed=await fold.count()&&!await fold.evaluate(e=>e.open);
   if(closed){const summary=fold.locator('summary');await summary.focus();await p.keyboard.press('Enter');assert(await fold.evaluate(e=>e.open));}
   await im.scrollIntoViewIfNeeded();assert(await im.isVisible());assert(await im.evaluate(i=>i.complete&&i.naturalWidth>0));assert((await im.getAttribute('alt')).length>25);
   if(closed){await fold.locator('summary').focus();await p.keyboard.press('Enter');assert(!await fold.evaluate(e=>e.open));assert(!await im.isVisible());}
  }
  if([390,1366].includes(width)&&['/narrativas/','/narrativas/percursos/ordem/','/narrativas/tudo/'].includes(url)){await p.evaluate(()=>scrollTo(0,0));const n=url==='/narrativas/'?'entrada':url.includes('tudo')?'tudo':'percurso';await p.screenshot({path:path.join(out,n+'-'+width+'.png'),fullPage:true});}
 }
 await p.emulateMedia({colorScheme:'dark'});await p.goto(base+'/narrativas/');assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));if(width===390)await p.screenshot({path:path.join(out,'entrada-escuro-390.png')});
 assert.deepEqual(errors,[]);await ctx.close();console.log(width+' px: estado, projeção, imagens e 23 páginas sem deslocamento horizontal.');}
}finally{await b.close();server.close();}console.log('Capturas: '+out);})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
