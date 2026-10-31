/* 30/10/2026: apenas lê os registos reais. Visitar nunca equivale a concluir.
   Não lê respostas, não envia dados e não consulta progresso em projeção (?projetar=1 ou dentro da moldura /projetar/).
   31/10/2026: a reposição lê o aparelho no momento em que repõe; «a seguir» na primeira peça por fazer. */
(function(){'use strict';
 const node=document.getElementById('lab-dados');if(!node)return;
 const D=JSON.parse(node.textContent),by=Object.fromEntries(D.map(p=>[p.id,p]));
 const projected=new URLSearchParams(location.search).get('projetar')==='1'||window.self!==window.top;
 if(projected)document.documentElement.classList.add('em-projecao');
 const cache={};function read(k){if(projected)return {};if(!(k in cache)){try{cache[k]=JSON.parse(localStorage.getItem(k)||'{}')||{};}catch{cache[k]={};}}return cache[k];}
 function state(p){const q=p.progress,s=read(q.key);if(q.kind==='formas'){const it=s.version===1&&s.itens&&s.itens[q.id];return it&&typeof it.revi==='number'?'revisto':it&&typeof it.experimentei==='number'?'feito':'por fazer';}if(q.kind==='montagem')return s.version===1&&Array.isArray(s.done)&&q.ids.every(id=>s.done.includes(id))?'feito':'por fazer';return s.feitas&&s.feitas[q.id]?'feito':'por fazer';}
 const states=Object.fromEntries(D.map(p=>[p.id,state(p)]));
 const save=document.querySelector('[data-guardar]'),restore=document.querySelector('[data-repor]'),note=document.querySelector('[data-registos-aviso]');
 if(save&&restore){
  if(projected){save.hidden=true;restore.parentElement.hidden=true;}
  else{
   save.onclick=()=>{const registos=D.filter(p=>states[p.id]!=='por fazer').map(p=>({id:p.id,estado:states[p.id]}));const blob=new Blob([JSON.stringify({formato:'lente-laboratorio',versao:1,registos},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='laboratorio-progresso.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);note.textContent='Guardaste os estados. O ficheiro não inclui respostas nem textos.';};
   restore.onchange=async()=>{try{const file=restore.files[0];if(!file)return;note.textContent='Ficheiro escolhido: '+file.name+'.';if(file.size>100000)throw Error();const d=JSON.parse(await file.text());if(d.formato!=='lente-laboratorio'||d.versao!==1||!Array.isArray(d.registos)||d.registos.length>D.length)throw Error();const seen=new Set();for(const r of d.registos){if(!r||!Object.hasOwn(by,r.id)||seen.has(r.id)||!['feito','revisto'].includes(r.estado)||(r.estado==='revisto'&&by[r.id].progress.kind!=='formas'))throw Error();seen.add(r.id);}
    const changes={};for(const r of d.registos){const q=by[r.id].progress;if(!changes[q.key]){const raw=localStorage.getItem(q.key),v=raw?JSON.parse(raw):{};if(!v||typeof v!=='object'||Array.isArray(v))throw Error();changes[q.key]=v;}const s=changes[q.key];if(q.kind==='formas'){s.version=1;s.itens=s.itens||{};s.itens[q.id]=s.itens[q.id]||{};s.itens[q.id].experimentei=s.itens[q.id].experimentei||Date.now();if(r.estado==='revisto')s.itens[q.id].revi=s.itens[q.id].revi||Date.now();}else if(q.kind==='montagem'){s.version=1;s.done=[...new Set([...(Array.isArray(s.done)?s.done:[]),...q.ids])];}else{s.feitas=s.feitas||{};s.feitas[q.id]=s.feitas[q.id]||Date.now();}}
    for(const [k,v] of Object.entries(changes))localStorage.setItem(k,JSON.stringify(v));location.reload();
   }catch{note.textContent='Não foi possível repor. Escolhe um ficheiro de progresso guardado nesta página, ou confirma que o progresso deste aparelho não está estragado.';}finally{restore.value='';}};
  }
 }
 function ids(el,key){return JSON.parse(el.dataset[key]);}
 document.querySelectorAll('[data-estado]').forEach(el=>{const s=states[el.dataset.estado];el.textContent=s;if(s!=='por fazer')el.closest('li').classList.add('feito');});
 document.querySelectorAll('ol.passos').forEach(ol=>{const li=[...ol.children].find(li=>states[li.dataset.peca]==='por fazer');if(li){li.classList.add('seguir');const c=li.querySelector('[data-estado]');if(c)c.textContent='a seguir';}});
 document.querySelectorAll('[data-contagem]').forEach(el=>{const all=ids(el,'contagem'),n=all.filter(id=>states[id]!=='por fazer').length;el.textContent=n+' de '+all.length+' peças feitas';});
 const root=new URL(document.querySelector('[data-raiz]').dataset.raiz,location.href);
 document.querySelectorAll('[data-continuar]').forEach(el=>{const all=ids(el,'continuar'),done=all.some(id=>states[id]!=='por fazer'),id=all.find(id=>states[id]==='por fazer')||all[0],p=by[id];el.textContent=(all.every(id=>states[id]!=='por fazer')?'Percurso feito. Recomeçar: ':done?'Continuar: ':'Começar: ')+p.title+' →';const u=new URL(p.url,root);if(projected)u.searchParams.set('projetar','1');el.href=u.href;});
 if(projected)document.querySelectorAll('a[href]').forEach(a=>{const u=new URL(a.href);if(u.origin===location.origin){u.searchParams.set('projetar','1');a.href=u.href;}});
 const wide=matchMedia('(min-width:640px)');function dobras(){if(wide.matches)document.querySelectorAll('details.dobra').forEach(d=>{d.open=true;});}dobras();if(wide.addEventListener)wide.addEventListener('change',dobras);
 addEventListener('pageshow',e=>{if(e.persisted)location.reload();});
})();
