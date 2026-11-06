/* 30/10/2026: apenas lê os registos reais. Visitar nunca equivale a concluir.
   Não lê respostas, não envia dados e não consulta progresso em projeção (?projetar=1 ou dentro da moldura /projetar/).
   31/10/2026: a reposição lê o aparelho no momento em que repõe; «a seguir» na primeira peça por fazer.
   31/10/2026 (segunda correção): uma só marca «a seguir» por página, a peça para onde leva «Começar» ou «Continuar».
   05/11/2026: decisão 163. Rótulos «Feita dd/mm» e «A seguir» das linhas, das portas e do índice (antes em cartaz.js); sem dobras.
   05/11/2026: decisão 147 (revisão). Um ficheiro só com peças retiradas não recarrega e diz porquê; num ficheiro misto, a nota
   «Repostas N peças; M já não fazem parte do Laboratório.» passa o recarregamento em sessionStorage. Um id desconhecido continua recusado. */
(function(){'use strict';
 const node=document.getElementById('lab-dados');if(!node)return;
 const D=JSON.parse(node.textContent),by=Object.fromEntries(D.map(p=>[p.id,p]));
 // 05/11/2026: decisão 147. Um ficheiro guardado antes do corte repõe-se: as peças retiradas do Laboratório ignoram-se.
 const retNode=document.getElementById('lab-retiradas'),RET=retNode?JSON.parse(retNode.textContent):[];
 const projected=new URLSearchParams(location.search).get('projetar')==='1'||window.self!==window.top;
 if(projected)document.documentElement.classList.add('em-projecao');
 const cache={};function read(k){if(projected)return {};if(!(k in cache)){try{cache[k]=JSON.parse(localStorage.getItem(k)||'{}')||{};}catch{cache[k]={};}}return cache[k];}
 function state(p){const q=p.progress,s=read(q.key);if(q.kind==='formas'){const it=s.version===1&&s.itens&&s.itens[q.id];return it&&typeof it.revi==='number'?'revisto':it&&typeof it.experimentei==='number'?'feito':'por fazer';}if(q.kind==='montagem')return s.version===1&&Array.isArray(s.done)&&q.ids.every(id=>s.done.includes(id))?'feito':'por fazer';return s.feitas&&s.feitas[q.id]?'feito':'por fazer';}
 const states=Object.fromEntries(D.map(p=>[p.id,state(p)]));
 const AVISO='lente-laboratorio-reposicao',save=document.querySelector('[data-guardar]'),restore=document.querySelector('[data-repor]'),note=document.querySelector('[data-registos-aviso]');
 if(save&&restore){
  if(projected){save.hidden=true;restore.parentElement.hidden=true;}
  else{
   try{const m=sessionStorage.getItem(AVISO);if(m){sessionStorage.removeItem(AVISO);note.textContent=m;}}catch{}
   save.onclick=()=>{const registos=D.filter(p=>states[p.id]!=='por fazer').map(p=>({id:p.id,estado:states[p.id]}));const blob=new Blob([JSON.stringify({formato:'lente-laboratorio',versao:1,registos},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='laboratorio-progresso.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);note.textContent='Guardaste os estados. O ficheiro não inclui respostas nem textos.';};
   restore.onchange=async()=>{try{const file=restore.files[0];if(!file)return;note.textContent='Ficheiro escolhido: '+file.name+'.';if(file.size>100000)throw Error();const d=JSON.parse(await file.text());if(d.formato!=='lente-laboratorio'||d.versao!==1||!Array.isArray(d.registos)||d.registos.length>500)throw Error();const regs=d.registos.filter(r=>!(r&&typeof r.id==='string'&&!Object.hasOwn(by,r.id)&&RET.includes(r.id)));if(regs.length>D.length)throw Error();const seen=new Set();for(const r of regs){if(!r||!Object.hasOwn(by,r.id)||seen.has(r.id)||!['feito','revisto'].includes(r.estado)||(r.estado==='revisto'&&by[r.id].progress.kind!=='formas'))throw Error();seen.add(r.id);}
    const fora=d.registos.length-regs.length;if(!regs.length&&fora){note.textContent='As peças deste ficheiro já não fazem parte do Laboratório; não havia nada para repor.';return;}
    const changes={};for(const r of regs){const q=by[r.id].progress;if(!changes[q.key]){const raw=localStorage.getItem(q.key),v=raw?JSON.parse(raw):{};if(!v||typeof v!=='object'||Array.isArray(v))throw Error();changes[q.key]=v;}const s=changes[q.key];if(q.kind==='formas'){s.version=1;s.itens=s.itens||{};s.itens[q.id]=s.itens[q.id]||{};s.itens[q.id].experimentei=s.itens[q.id].experimentei||Date.now();if(r.estado==='revisto')s.itens[q.id].revi=s.itens[q.id].revi||Date.now();}else if(q.kind==='montagem'){s.version=1;s.done=[...new Set([...(Array.isArray(s.done)?s.done:[]),...q.ids])];}else{s.feitas=s.feitas||{};s.feitas[q.id]=s.feitas[q.id]||Date.now();}}
    for(const [k,v] of Object.entries(changes))localStorage.setItem(k,JSON.stringify(v));
    if(fora){try{sessionStorage.setItem(AVISO,(regs.length===1?'Reposta 1 peça; ':'Repostas '+regs.length+' peças; ')+(fora===1?'1 já não faz parte do Laboratório.':fora+' já não fazem parte do Laboratório.'));}catch{}}
    location.reload();
   }catch{note.textContent='Não foi possível repor. Usa um ficheiro guardado nesta página com «Guardar num ficheiro». Se o erro se repetir, o registo deste aparelho pode estar danificado: avisa o docente.';}finally{restore.value='';}};
  }
 }
 function ids(el,key){return JSON.parse(el.dataset[key]);}
 // 05/11/2026: decisão 163 (menus do Laboratório). O estado diz-se com quadrado e palavra: «Feita dd/mm» (a data só quando há
 // uma data verdadeira; nunca se inventa) e «A seguir». «A seguir» só aparece quando já há alguma peça feita na lista da página
 // (a porta, o percurso ou o Laboratório inteiro, na entrada). «Por fazer» nunca se escreve. Substitui o rótulo de cartaz.js.
 function val(p){const q=p.progress,s=read(q.key);if(q.kind==='formas'){const it=s.version===1&&s.itens&&s.itens[q.id];return it&&(it.revi||it.experimentei);}if(q.kind==='montagem')return s.version===1&&Array.isArray(s.done)&&q.ids.every(id=>s.done.includes(id));return s.feitas&&s.feitas[q.id];}
 const DESDE=Date.UTC(2020,0,1);
 function dia(v){const d=typeof v==='number'&&v>DESDE?new Date(v):null;return d&&Number.isFinite(d.getTime())?String(d.getDate()).padStart(2,'0')+'/'+String(d.getMonth()+1).padStart(2,'0'):'';}
 function feita(v){const d=dia(v);return 'Feita'+(d?' '+d:'');}
 const cont=document.querySelector('[data-continuar]'),lista=cont?ids(cont,'continuar'):[],algo=lista.some(id=>states[id]!=='por fazer'),proxima=lista.find(id=>states[id]==='por fazer');
 // as linhas das sessões do Ideias na entrada também têm [data-estado] (vazio): são de entrada.js e ficam de fora
 document.querySelectorAll('[data-estado]').forEach(el=>{const id=el.dataset.estado;if(!id||!Object.hasOwn(by,id))return;const s=states[id],li=el.closest('li');if(s!=='por fazer'){el.textContent=feita(val(by[id]));el.classList.add('feita');if(li)li.classList.add('feito');const a=el.closest('.linha');if(a)a.classList.add('feita');}else el.textContent='';});
 if(proxima&&algo){document.querySelectorAll('li[data-peca="'+CSS.escape(proxima)+'"]').forEach(li=>{li.classList.add('seguir');const a=li.querySelector('.linha');if(a)a.classList.add('seguir');const c=li.querySelector('[data-estado]');if(c){c.textContent='A seguir';c.classList.add('seguir');}});}
 // Contagens: «N de M peças feitas» (ou «N de M feitas» nas portas da entrada); as que começam escondidas só aparecem com algo feito.
 document.querySelectorAll('[data-contagem]').forEach(el=>{const all=ids(el,'contagem'),n=all.filter(id=>states[id]!=='por fazer').length;el.textContent=n+' de '+all.length+(el.hasAttribute('data-curto')?' feitas':' peças feitas');if(el.hasAttribute('hidden')||el.dataset.escondida!==undefined){el.dataset.escondida='';el.hidden=n===0;}});
 // Índice dos percursos na entrada: o percurso da peça seguinte leva a classe «current» (sempre, para o progresso), mas a palavra
 // «A seguir» e o filete só se veem quando já há alguma peça feita; um percurso inteiro feito diz «Feita dd/mm».
 document.querySelectorAll('[data-cz-route]').forEach(row=>{const l=ids(row,'czRoute'),vs=l.map(id=>val(by[id])),completo=l.every(id=>states[id]!=='por fazer'),atual=!!proxima&&l.includes(proxima),lab=row.querySelector('.cz-state');
  row.classList.toggle('current',atual&&!completo);row.classList.toggle('done',completo);
  if(lab){const d=completo&&vs.every(v=>typeof v==='number'&&v>DESDE)?Math.max(...vs):null;lab.textContent=completo?feita(d):atual&&algo?'A seguir':'';lab.classList.toggle('done',completo);lab.classList.toggle('current',atual&&algo&&!completo);}});
 if(algo)document.documentElement.classList.add('lab-tem-feitas');
 const root=new URL(document.querySelector('[data-raiz]').dataset.raiz,location.href);
 document.querySelectorAll('[data-continuar]').forEach(el=>{const all=ids(el,'continuar'),done=all.some(id=>states[id]!=='por fazer'),id=all.find(id=>states[id]==='por fazer')||all[0],p=by[id];el.textContent=(all.every(id=>states[id]!=='por fazer')?'Percurso feito. Recomeçar: ':done?'Continuar: ':'Começar: ')+p.title+' →';const u=new URL(p.url,root);if(projected)u.searchParams.set('projetar','1');el.href=u.href;});
 if(projected)document.querySelectorAll('a[href]').forEach(a=>{const u=new URL(a.href);if(u.origin===location.origin){u.searchParams.set('projetar','1');a.href=u.href;}});
 // Na impressão, os créditos do «i» abrem-se por extenso (decisão 153) e voltam a fechar depois.
 addEventListener('beforeprint',()=>document.querySelectorAll('details.info-i:not([open])').forEach(d=>{d.open=true;d.dataset.impressao='';}));
 addEventListener('afterprint',()=>document.querySelectorAll('details.info-i[data-impressao]').forEach(d=>{d.open=false;delete d.dataset.impressao;}));
 addEventListener('pageshow',e=>{if(e.persisted)location.reload();});
})();
