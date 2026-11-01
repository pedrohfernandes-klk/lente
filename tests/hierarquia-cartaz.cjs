// 01/11/2026: decisão 61. MEASURE preservado do medir-hierarquia.js fornecido pelo docente.
// O invólucro limita a medição às páginas migradas, compara R4 entre blocos e verifica a escala.
const assert=require('node:assert/strict'),fs=require('fs'),path=require('path'),http=require('http');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..');
// 01/11/2026: a demonstração nova também passa pela medição integral R1–R5.
const candidates=['demonstracoes/cartaz-animacoes/index.html','index.html','narrativas/index.html','narrativas/ver/index.html','narrativas/treinar/index.html','narrativas/criar/index.html'];
const pages=candidates.filter(p=>fs.existsSync(path.join(root,p))&&fs.readFileSync(path.join(root,p),'utf8').includes('data-cartaz="2"'));
const server=http.createServer((q,r)=>{let f=path.resolve(root,'.'+new URL(q.url,'http://local').pathname.replace(/^\/lente/,''));if(f!==root&&!f.startsWith(root+path.sep)){r.writeHead(403);return r.end();}try{if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');r.setHeader('content-type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.json':'application/json'})[path.extname(f)]||'application/octet-stream');r.end(fs.readFileSync(f));}catch{r.writeHead(404);r.end();}});
const MEASURE=()=>{
  const vis=e=>{const r=e.getBoundingClientRect();if(r.width<2||r.height<2)return false;for(let x=e;x&&x!==document.documentElement;x=x.parentElement){if(x.hidden)return false;const c=getComputedStyle(x);if(c.display==='none'||c.visibility==='hidden'||+c.opacity<.05)return false;if(x.matches&&x.matches('.sr-only,.c-sr,.p-sr,.visually-hidden,dialog:not([open]),details:not([open])>:not(summary)'))return false;}return true;};
  const fs=e=>parseFloat(getComputedStyle(e).fontSize);
  const txt=e=>e.textContent.replace(/\s+/g,' ').trim().slice(0,80);
  const desc=e=>e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(typeof e.className==='string'&&e.className.trim()?'.'+e.className.trim().split(/\s+/).slice(0,3).join('.'):'');
  const sig=e=>{const parent=e.parentElement;const pc=parent&&typeof parent.className==='string'&&parent.className.trim()?'.'+parent.className.trim().split(/\s+/)[0]:'';return (parent?parent.tagName.toLowerCase()+pc+'>':'')+desc(e).replace(/#[^.]+/,'');};
  const level=e=>{const m=e.tagName.match(/^H([1-6])$/);if(m)return +m[1];const a=e.getAttribute('aria-level');return a?+a:2;};
  const heads=[...document.querySelectorAll('h1,h2,h3,h4,h5,h6,[role=heading]')].filter(e=>vis(e)&&txt(e));
  const out={r1:[],r2:[],r3:[],r5:[],roles:[]};
  heads.forEach((h,i)=>{const L=level(h),F=fs(h);out.roles.push({sig:sig(h),lvl:L,fs:F,txt:txt(h)});
    for(let j=i+1;j<heads.length;j++){const k=heads[j],Lk=level(k);if(Lk<=L)break;const Fk=fs(k);if(Fk>F+.5){out.r1.push({pai:desc(h),paiTxt:txt(h),paiFs:F,filho:desc(k),filhoTxt:txt(k),filhoFs:Fk});break;}}
    // R2 antetítulo
    const prev=h.previousElementSibling;if(prev&&vis(prev)&&!/^H[1-6]$/.test(prev.tagName)&&!prev.closest('[aria-hidden="true"]')){const t=txt(prev);const c=getComputedStyle(prev);const ls=parseFloat(c.letterSpacing)||0;if(t&&t.length<=60&&(c.textTransform==='uppercase'||ls>=.05*parseFloat(c.fontSize))){const Fp=fs(prev);out.r3.push({cls:desc(prev).replace(/#[^.]+/,''),desc:desc(prev),txt:t,fs:Fp,fam:c.fontFamily.split(',')[0].replace(/["']/g,''),w:c.fontWeight});if(Fp>.65*F)out.r2.push({ante:desc(prev),anteTxt:t,anteFs:Fp,titulo:desc(h),tituloTxt:txt(h),tituloFs:F});}}
    // R5 texto corrido a seguir
    const c=getComputedStyle(h);if(c.textTransform!=='uppercase'){let n=h.nextElementSibling;while(n&&!vis(n))n=n.nextElementSibling;if(n&&n.tagName==='P'&&txt(n).length>60){const Fn=fs(n);if(F<Fn-.5)out.r5.push({titulo:desc(h),tituloTxt:txt(h),tituloFs:F,texto:desc(n),textoFs:Fn});}}
  });
  const byCls={};for(const k of out.r3)(byCls[k.cls]=byCls[k.cls]||new Set()).add(k.fam+'|'+Math.round(k.fs)+'|'+k.w);out.r3=out.r3.filter(k=>byCls[k.cls].size>1);
  return out;};

(async()=>{
 if(!pages.length){console.log('Hierarquia: sem páginas ativadas neste lote de peças; não aplicável.');return;}
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});const rows=[];
 try{
 for(const theme of ['light','dark'])for(const width of [390,1366]){
 const ctx=await browser.newContext({viewport:{width,height:900},colorScheme:theme,reducedMotion:'reduce'});
 // O CSS absoluto do próprio sítio é servido pela árvore local; fontes externas não alteram tamanhos.
 await ctx.route('**/*',async route=>{const u=new URL(route.request().url());if(u.origin===origin)return route.continue();if(u.hostname==='pedrohfernandes-klk.github.io'&&u.pathname.startsWith('/lente/')){const response=await ctx.request.get(origin+u.pathname+u.search);return route.fulfill({response});}return route.abort();});
 const page=await ctx.newPage();
 for(const p of pages){await page.goto(origin+'/lente/'+p,{waitUntil:'networkidle'});
 for(const mode of ['normal','dobras abertas']){
 if(mode==='dobras abertas')await page.locator('details').evaluateAll(es=>es.forEach(e=>e.open=true));
 const m=await page.evaluate(MEASURE);const row={page:p,width,theme,mode,...m};rows.push(row);
 for(const rule of ['r1','r2','r3','r5'])assert.deepEqual(m[rule],[],`${p} ${width} ${theme} ${mode} ${rule}: ${JSON.stringify(m[rule])}`);
 const offScale=await page.evaluate(()=>{const scale=[13,16,20,25,31,39,49,61];return [...document.querySelectorAll('[data-cartaz="2"] :is(h1,h2,h3,h4,h5,h6,[role=heading],h1 a,h2 a,h3 a,.cz-label,.marca,.lente-etq,.ld-rot,.sp-title,.sp-kicker)')].filter(e=>!e.closest('[aria-hidden="true"]')&&e.getBoundingClientRect().height>0).map(e=>({text:e.textContent.trim().slice(0,60),size:parseFloat(getComputedStyle(e).fontSize)})).filter(x=>!scale.some(n=>Math.abs(n-x.size)<.02));});
 assert.deepEqual(offScale,[],`${p} fora da escala: ${JSON.stringify(offScale)}`);
 }
 }await ctx.close();}
 const roles=new Map();let r4=0;
 for(const row of rows){const template=/narrativas\/(ver|treinar|criar)\//.test(row.page)?'bloco':row.page;for(const role of row.roles){const key=[template,row.width,row.theme,row.mode,role.sig].join('|');if(roles.has(key)&&Math.abs(roles.get(key)-role.fs)>.02)r4++;roles.set(key,role.fs);}}
 assert.equal(r4,0,'R4: tamanhos diferentes no mesmo molde');
 for(const p of pages)for(const width of [390,1366])console.log(`${p} | ${width}px | claro/escuro, normal/dobras abertas | R1=0 R2=0 R3=0 R4=0 R5=0 | escala conforme`);
 if(process.env.HIERARQUIA_SAIDA)fs.writeFileSync(process.env.HIERARQUIA_SAIDA,JSON.stringify(rows,null,2));
 }finally{await browser.close();server.closeAllConnections();server.close();}
})().catch(e=>{console.error(e);process.exitCode=1;server.closeAllConnections();server.close();});
