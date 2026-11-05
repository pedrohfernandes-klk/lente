// 30/10/2026: estado real, projeção, links, imagens de arquivo e quatro larguras.
// 05/11/2026: decisão 147 (Laboratório sem o Português). As peças de exemplo passam a ser as que ficam (Leonardo, Galileu,
// Cigoli e Anguissola, no percurso «Observar para transformar», agora o primeiro); um ficheiro guardado antes do corte, com
// uma peça retirada (treinar/sem-olhos), continua a repor as outras.
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),D=require('../assets/laboratorio/percursos.json');
const out=process.env.LENTE_SHOTS||fs.mkdtempSync(path.join(require('node:os').tmpdir(),'lab-percursos-'));fs.mkdirSync(out,{recursive:true});
const server=http.createServer((req,res)=>{let f=path.join(root,decodeURIComponent(req.url.split('?')[0]));if(fs.existsSync(f)&&fs.statSync(f).isDirectory())f=path.join(f,'index.html');if(!fs.existsSync(f)){res.writeHead(404).end();return;}res.setHeader('Content-Type',({'.js':'application/javascript','.css':'text/css','.html':'text/html','.webp':'image/webp'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port;const b=await chromium.launch();
try{for(const width of [320,390,1366,1440]){const ctx=await b.newContext({viewport:{width,height:900},reducedMotion:'reduce'}),p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
 // 01/11/2026: título e ação são agora elementos separados da mesma região; ambos continuam obrigatórios.
 // 02/11/2026: decisão 134 (docente). Sem a caixa «A seguir»: a ligação de continuar fica escondida e a peça seguinte marca a linha do percurso atual.
 await p.goto(base+'/narrativas/');assert.equal(await p.locator('.cz-next').count(),0);assert(await p.locator('[data-continuar]').isHidden());assert((await p.locator('[data-continuar]').getAttribute('href')).endsWith('/narrativas/leonardo/'));assert(JSON.parse(await p.locator('[data-cz-route].current').getAttribute('data-cz-route')).includes('leonardo'));
 await p.evaluate(()=>localStorage.setItem('epi-narrativas',JSON.stringify({feitas:{'leonardo':123},privado:'RESPOSTA PRIVADA'})));
 await p.reload();assert(await p.locator('[data-continuar]').isHidden());assert(JSON.parse(await p.locator('[data-cz-route].current').getAttribute('data-cz-route')).includes('galileu'));assert((await p.locator('[data-continuar]').getAttribute('href')).endsWith('/narrativas/galileu/'));
 if(width===390){const downloaded=p.waitForEvent('download');await p.locator('[data-guardar]').click();const file=await (await downloaded).path(),data=JSON.parse(fs.readFileSync(file,'utf8'));assert.deepEqual(data.registos,[{id:'leonardo',estado:'feito'}]);assert(!fs.readFileSync(file,'utf8').includes('PRIVADA'));
  const restored={formato:'lente-laboratorio',versao:1,registos:[...data.registos,{id:'formas/certa-manha',estado:'revisto'}]};await Promise.all([p.waitForEvent('load'),p.locator('[data-repor]').setInputFiles({name:'progresso.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(restored))})]);assert.equal(await p.evaluate(()=>JSON.parse(localStorage.getItem('epi-narrativas')).privado),'RESPOSTA PRIVADA');assert(await p.evaluate(()=>JSON.parse(localStorage.getItem('lente-formas-v1')).itens['certa-manha'].revi>0));
  // 30/10/2026: repor lê o aparelho no momento da reposição; o que outro separador gravou depois de abrir a página fica (revisão técnica).
  await p.goto(base+'/narrativas/');const outro=await ctx.newPage();await outro.goto(base+'/narrativas/tudo/');await outro.evaluate(()=>{const s=JSON.parse(localStorage.getItem('epi-narrativas'));s.feitas.cigoli=456;localStorage.setItem('epi-narrativas',JSON.stringify(s));});await outro.close();
  await Promise.all([p.waitForEvent('load'),p.locator('[data-repor]').setInputFiles({name:'progresso.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify({formato:'lente-laboratorio',versao:1,registos:[{id:'anguissola',estado:'feito'},{id:'treinar/sem-olhos',estado:'feito'}]}))})]);
  assert.deepEqual(await p.evaluate(()=>{const f=JSON.parse(localStorage.getItem('epi-narrativas')).feitas;return [f.cigoli,f['leonardo'],f.anguissola>0];}),[456,123,true]);
  // 05/11/2026: decisão 147 (revisão). Depois de repor um ficheiro misto, o aviso diz o que entrou e o que já não faz parte do Laboratório.
  assert.equal(await p.locator('[data-registos-aviso]').textContent(),'Reposta 1 peça; 1 já não faz parte do Laboratório.');
  const before=await p.evaluate(()=>JSON.stringify({...localStorage}));await p.locator('[data-repor]').setInputFiles({name:'incorreto.json',mimeType:'application/json',buffer:Buffer.from('{"formato":"outro"}')});await p.waitForFunction(()=>document.querySelector('[data-registos-aviso]').textContent.includes('Não foi'));assert.equal(await p.evaluate(()=>JSON.stringify({...localStorage})),before);
  // 05/11/2026: decisão 147 (revisão). Um id desconhecido continua recusado, mesmo ao lado de uma peça retirada: nada se repõe.
  const repor=async(name,registos)=>{await p.evaluate(()=>{window.semRecarregar=true;document.querySelector('[data-registos-aviso]').textContent='';});await p.locator('[data-repor]').setInputFiles({name,mimeType:'application/json',buffer:Buffer.from(JSON.stringify({formato:'lente-laboratorio',versao:1,registos}))});};
  await repor('desconhecido.json',[{id:'anguissola',estado:'feito'},{id:'treinar/sem-olhos',estado:'feito'},{id:'nao-existe',estado:'feito'}]);
  await p.waitForFunction(()=>document.querySelector('[data-registos-aviso]').textContent.includes('Não foi'));assert(await p.evaluate(()=>window.semRecarregar));assert.equal(await p.evaluate(()=>JSON.stringify({...localStorage})),before);
  // 05/11/2026: decisão 147 (revisão). Um ficheiro só com peças retiradas não recarrega a página e diz porquê; o aparelho fica igual.
  await repor('so-retiradas.json',[{id:'treinar/sem-olhos',estado:'feito'}]);
  await p.waitForFunction(()=>document.querySelector('[data-registos-aviso]').textContent==='As peças deste ficheiro já não fazem parte do Laboratório; não havia nada para repor.');assert(await p.evaluate(()=>window.semRecarregar));assert.equal(await p.evaluate(()=>JSON.stringify({...localStorage})),before);
 }
 await p.goto(base+'/narrativas/percursos/olhar/');assert.equal(await p.locator('[data-estado="leonardo"]').textContent(),'feito'); // 30/10/2026: textContent, porque o estado se mostra em caixa alta por CSS.
 // 30/10/2026: âncoras antigas levam ao percurso, no catálogo (revisão técnica).
 await p.goto(base+'/narrativas/#treinar-voz');await p.waitForURL('**/narrativas/tudo/#treinar-voz');assert(await p.locator('h3:has(#treinar-voz)').isVisible());assert(await p.evaluate(()=>{const r=document.getElementById('treinar-voz').parentElement.getBoundingClientRect();return r.top>=0&&r.top<innerHeight;}));
 await p.goto(base+'/narrativas/?projetar=1');assert(await p.locator('[data-continuar]').isHidden());assert((await p.locator('[data-continuar]').getAttribute('href')).includes('/narrativas/leonardo/'));assert(JSON.parse(await p.locator('[data-cz-route].current').getAttribute('data-cz-route')).includes('leonardo'));assert(!(await p.locator('body').innerText()).includes('RESPOSTA PRIVADA'));assert.equal(await p.evaluate(()=>JSON.parse(localStorage.getItem('epi-narrativas')).feitas['leonardo']),123);
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
  if([390,1366].includes(width)&&['/narrativas/','/narrativas/percursos/olhar/','/narrativas/tudo/'].includes(url)){await p.evaluate(()=>scrollTo(0,0));const n=url==='/narrativas/'?'entrada':url.includes('tudo')?'tudo':'percurso';await p.screenshot({path:path.join(out,n+'-'+width+'.png'),fullPage:true});}
 }
 await p.emulateMedia({colorScheme:'dark'});await p.goto(base+'/narrativas/');assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));if(width===390)await p.screenshot({path:path.join(out,'entrada-escuro-390.png')});
 assert.deepEqual(errors,[]);await ctx.close();console.log(width+' px: estado, projeção, imagens e 23 páginas sem deslocamento horizontal.');}
}finally{await b.close();server.close();}console.log('Capturas: '+out);})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
