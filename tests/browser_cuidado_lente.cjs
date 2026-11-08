// 08/11/2026: decisão 152 («cuidado em todas as lições», pedido cuidado-lente). As tabelas novas (Justiça 1 e 2, Aplicar, sete
// oficinas do Laboratório e as sessões 02, 03 e 08 do M2) a 360 e a 900 px, no modo claro e no escuro: a página não rola para o lado,
// a tabela e as células não transbordam, a 360 px cada linha empilha com o nome da coluna antes de cada célula e a 900 px lê-se em
// colunas, e o texto tem contraste com o fundo. As referências e os números com espaço sem quebra ou junção ficam numa só linha,
// na página a 360 px e a estreitar a caixa de 8 em 8 px. Com CUIDADO_PROVAS, guarda capturas das tabelas (deviceScaleFactor 1).
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),PROVAS=process.env.CUIDADO_PROVAS;
const server=http.createServer((req,res)=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname).replace(/^\/lente/,''));if(!f.startsWith(root+path.sep)&&f!==root){res.writeHead(403);return res.end();}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.webp':'image/webp','.jpg':'image/jpeg','.png':'image/png'})[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end();}});
const NB=' ',WJ='⁠';
// [nome, endereço, tabelas esperadas, como chegar: null (à vista), '#momento-N' (passo da sessão) ou 'cartoes' (avança como o aluno)]
const TABELAS=[
 ['justica-1','olhar-e-decidir/justica/licao-1/',1,'cartoes'],
 ['justica-2','olhar-e-decidir/justica/licao-2/',1,'cartoes'],
 ['aplicar','olhar-e-decidir/justica/aplicar/',1,'cartoes'],
 ['oficina-argumento','narrativas/oficina-argumento/',1,'cartoes'],
 ['oficina-manifesto','narrativas/oficina-manifesto/',1,'cartoes'],
 ['oficina-pedacos','narrativas/oficina-pedacos/',1,'cartoes'],
 ['oficina-plano','narrativas/oficina-plano/',1,'cartoes'],
 ['oficina-restricao','narrativas/oficina-restricao/',1,'cartoes'],
 ['oficina-texto-imagem','narrativas/oficina-texto-imagem/',2,'cartoes'],
 ['oficina-visivel','narrativas/oficina-visivel/',1,'cartoes'],
 ['m2-s02','cidadania/m2/sessoes/02/',1,'#momento-3'],
 ['m2-s03','cidadania/m2/sessoes/03/',1,'#momento-3'],
 ['m2-s08','cidadania/m2/sessoes/08/',1,'#momento-2'],
];
// [endereço, referências que não podem partir-se (só a parte protegida: em «45 a 60 min», «60 min»); as de cartões estão no
// primeiro cartão]
const REFERENCIAS=[
 ['olhar-e-decidir/justica/docente/',[`(1${NB}min${NB}07${NB}s)`,`11${NB}de${NB}Setembro`,`ISBN${NB}978-${WJ}972-${WJ}23-${WJ}6911-${WJ}4`]],
 ['olhar-e-decidir/justica/',[`14${NB}000`]],
 ['olhar-e-decidir/etica/licao-1/',[`19${NB}000`]],
 ['cidadania/m2/sessoes/',[`6${NB}horas`,`125${NB}minutos`]],
 ['cidadania/m2/sessoes/04/#momento-2',[`pp.${NB}435–${WJ}450`]],
 ['biblioteca/caeiro-guardador-xx/',[`pp.${NB}53–${WJ}54`]],
 ['biblioteca/orta-benjui/',[`vol.${NB}I`,`p.${NB}105–${WJ}106`]],
 ['narrativas/oficina-arco/',[`60${NB}min`,`10${NB}min`]],
 ['narrativas/treinar/docente/',[`12${NB}min`]],
 ['narrativas/ideias/docente/',[`180${NB}minutos`]],
];

// Avança um cartão como o aluno (a mesma ação de tests/browser_cidadania_butler_singer.py).
async function avancar(p){
 const tenta=async sel=>{const l=p.locator(sel);if(await l.count()){await l.first().click();return true;}return false;};
 if(await tenta('.casca [data-c-folha]:visible [data-seguinte]'))return;
 if(await tenta('.casca [data-c-acoes] [data-seguinte]'))return;
 if(await tenta('#baralho [data-tipo-ext="posicao"] [data-ops] button'))return;
 const esq=p.locator('#baralho .pares .col.esq [data-e]');
 if(await esq.count()){const n=await esq.count();for(let i=0;i<n;i++){await p.locator(`#baralho .pares .col.esq [data-e="${i}"]`).click();await p.locator(`#baralho .pares .col.dir [data-d="${i}"]`).click();}return;}
 // emparelhar por colunas (como em tests/browser_justica.cjs): cada cartão vai para uma coluna
 if(await p.locator('#baralho .classes').count()){const n=await p.locator('#baralho [data-e]').count();for(let i=0;i<n;i++){await p.locator(`#baralho [data-e="${i}"]`).click();await p.locator('#baralho .regiao .cab').first().click();}return;}
 const soltos=p.locator('#baralho .ordem .soltos button.op');
 if(await soltos.count()){const n=await soltos.count();for(let i=0;i<n;i++)await soltos.first().click();return;}
 if(await tenta('#baralho .ops button.op[data-j="0"]'))return;
 throw new Error('não sei avançar: '+(await p.locator('#baralho').innerText()).slice(0,200));
}
async function chegar(p,como,n){
 if(como!=='cartoes')return;
 for(let k=0;k<40;k++){
  if(await p.locator('table.apoio-tabela').count()>=n)break;
  await avancar(p);await p.waitForTimeout(60);
 }
}
// Medidas de cada tabela: transbordo, empilhamento, rótulos e contraste.
function medir(){
 const lum=c=>{const v=c.match(/[\d.]+/g).slice(0,3).map(Number).map(x=>{x/=255;return x<=.03928?x/12.92:Math.pow((x+.055)/1.055,2.4);});return .2126*v[0]+.7152*v[1]+.0722*v[2];};
 const fundo=e=>{for(;e;e=e.parentElement){const c=getComputedStyle(e).backgroundColor;const a=c.match(/[\d.]+/g);if(a&&(a.length<4||+a[3]>.9))return c;}return 'rgb(255,255,255)';};
 const contraste=(a,b)=>{const l1=lum(a),l2=lum(b);return (Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);};
 return {lado:document.documentElement.scrollWidth-innerWidth,tema:document.documentElement.dataset.theme||'light',tabelas:[...document.querySelectorAll('table.apoio-tabela')].map(t=>{
  const r=t.getBoundingClientRect(),caixa=(t.closest('.cartao,.c10-stage,.c10-mat,main')||document.body).getBoundingClientRect();
  // as células à vista (o cabeçalho da .c10-tabela, a 560 px, fica só para o leitor de ecrã: 1 px, recortado)
  const celulas=[...t.querySelectorAll('td,th')].filter(c=>{const b=c.getBoundingClientRect();return b.width>2&&b.height>2;});
  const td=t.querySelector('tbody tr:not(:first-child) td:nth-child(2), tbody tr td[data-rotulo]')||t.querySelector('td');
  const corpo=[...t.querySelectorAll('td')].filter(c=>c.getClientRects().length);
  return {largura:r.width,altura:r.height,esquerda:r.left,direita:r.right,ecra:innerWidth,dentro:r.left>=caixa.left-1&&r.right<=caixa.right+1,
   transborda:t.scrollWidth>t.clientWidth+1,celulasTransbordam:celulas.filter(c=>c.scrollWidth>c.clientWidth+1).map(c=>c.textContent.slice(0,40)),
   empilhada:getComputedStyle(td).display==='block',rotulo:getComputedStyle(td,'::before').content,
   cabecalhoVisivel:[...t.querySelectorAll('th[scope=col]')].some(h=>h.getBoundingClientRect().width>2&&h.getBoundingClientRect().height>2),
   contraste:Math.min(...corpo.map(c=>contraste(getComputedStyle(c).color,fundo(c)))),
   alinhamento:[...new Set(celulas.map(c=>getComputedStyle(c).textAlign))]};})};
}
// A referência fica numa só linha: os retângulos do texto têm todos o mesmo topo.
function umaLinha(ref){
 const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while((n=w.nextNode())){let i=n.data.indexOf(ref);while(i>=0){const el=n.parentElement;if(el.getClientRects().length){
   const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+ref.length);
   const linhas=()=>new Set([...r.getClientRects()].filter(x=>x.width>0).map(x=>Math.round(x.top))).size;
   const bloco=(()=>{let b=el;while(b&&getComputedStyle(b).display.startsWith('inline'))b=b.parentElement;return b;})();
   const larguraRef=r.getBoundingClientRect().width,orig=bloco.style.width,partidas=[];
   if(linhas()>1)partidas.push('na página');
   // estreita a caixa de 8 em 8 px, até pouco mais do que a própria referência
   for(let L=Math.floor(bloco.getBoundingClientRect().width);L>larguraRef+12;L-=8){bloco.style.width=L+'px';if(linhas()>1){partidas.push(L+' px');break;}}
   bloco.style.width=orig;out.push({ref,partidas});}
  i=n.data.indexOf(ref,i+1);}}
 return out;
}
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
 if(PROVAS)fs.mkdirSync(PROVAS,{recursive:true});
 let nt=0,nr=0;
 const contexto=async(width,tema)=>{const ctx=await browser.newContext({viewport:{width,height:900},deviceScaleFactor:1,colorScheme:tema});
  // o modo escuro liga-se como o aluno o liga: a escolha guardada por assets/appearance.js (epi-theme)
  await ctx.addInitScript(t=>{try{localStorage.setItem('epi-theme',t);}catch(e){}},tema);
  // os endereços absolutos do sítio publicado servem-se da cópia de trabalho, lidos do disco
  await ctx.route('https://pedrohfernandes-klk.github.io/lente/**',route=>{let f=path.resolve(root,'.'+decodeURIComponent(new URL(route.request().url()).pathname).replace(/^\/lente/,''));
   try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');return route.fulfill({path:f});}catch{return route.fulfill({status:404,body:''});}}).catch(()=>{});
  await ctx.route(/fonts\.(googleapis|gstatic)\.com|youtube|ytimg/,r=>r.abort());return ctx;};
 try{
  for(const tema of ['light','dark'])for(const width of [360,900]){
   const ctx=await contexto(width,tema);
   for(const [nome,url,n,como] of TABELAS){
    const rot=`${nome}, ${width} px, ${tema==='dark'?'escuro':'claro'}`;
    const p=await ctx.newPage(),erros=[];p.on('pageerror',e=>erros.push(e.message));
    await p.goto(origin+'/lente/'+url+(como&&como.startsWith('#')?como:''),{waitUntil:'networkidle'});
    await chegar(p,como,n);
    // as tabelas que estão dentro de um details («Ler mais», «Os benefícios», «Comparar razões») abrem-se como o aluno as abre
    for(const s of await p.locator('details:has(table.apoio-tabela)').all()){if(!(await s.evaluate(d=>d.open)))await s.locator(':scope>summary').click();}
    await p.locator('table.apoio-tabela').first().scrollIntoViewIfNeeded();
    const m=await p.evaluate(medir);
    assert.equal(m.tema,tema,rot+': tema');
    assert.equal(m.tabelas.length,n,rot+': tabelas novas');
    assert.ok(m.lado<=0,rot+': a página rola para o lado ('+m.lado+' px)');
    for(const t of m.tabelas){
     assert.ok(t.largura>0&&t.altura>0,rot+': tabela à vista');
     assert.ok(t.esquerda>=0&&t.direita<=t.ecra,rot+': a tabela cabe no ecrã '+JSON.stringify([t.esquerda,t.direita]));
     assert.ok(t.dentro,rot+': a tabela fica dentro do seu cartão');
     assert.ok(!t.transborda,rot+': a tabela não transborda');
     assert.deepEqual(t.celulasTransbordam,[],rot+': nenhuma célula transborda');
     assert.deepEqual(t.alinhamento,['left'],rot+': texto à esquerda, sem justificar');
     if(width===360){assert.ok(t.empilhada,rot+': empilhada');assert.ok(t.rotulo&&t.rotulo!=='none'&&t.rotulo!=='normal',rot+': rótulo antes da célula ('+t.rotulo+')');assert.ok(!t.cabecalhoVisivel,rot+': cabeçalho escondido (vai no rótulo)');}
     else{assert.ok(!t.empilhada,rot+': em colunas');assert.ok(t.cabecalhoVisivel,rot+': cabeçalho à vista');}
     assert.ok(t.contraste>=4.5,rot+': contraste '+t.contraste.toFixed(2));
    }
    if(PROVAS){
     let i=0;for(const t of await p.locator('table.apoio-tabela').all()){await t.scrollIntoViewIfNeeded();await t.screenshot({path:path.join(PROVAS,`${nome}${i?'-'+(i+1):''}-${width}-${tema==='dark'?'escuro':'claro'}.png`)});i++;}
    }
    assert.deepEqual(erros,[],rot+': sem erros');await p.close();nt++;
   }
   await ctx.close();
  }
  // referências e números: numa só linha, na página a 360 px e a estreitar a caixa
  const ctx=await contexto(360,'light');
  for(const [url,refs] of REFERENCIAS){
   const p=await ctx.newPage();await p.goto(origin+'/lente/'+url,{waitUntil:'networkidle'});
   for(const ref of refs){
    const r=await p.evaluate(umaLinha,ref);
    assert.ok(r.length>0,url+': a referência está à vista: '+JSON.stringify(ref));
    for(const x of r)assert.deepEqual(x.partidas,[],url+': «'+ref.replace(/⁠/g,'')+'» parte-se');
    nr+=r.length;
   }
   await p.close();
  }
  await ctx.close();
  console.log(`Cuidado em todas as lições: ${nt} páginas com tabelas novas (360 e 900 px, claro e escuro), sem transbordo; ${nr} referências numa só linha.`);
 }finally{await browser.close();server.closeAllConnections();server.close();}
})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
