/* 01/11/2026: retoma das três áreas, sem escrever progresso. */
(function(){'use strict';
 const main=document.querySelector('[data-cartaz-entrada]');if(!main)return;
 if(new URLSearchParams(location.search).get('projetar')==='1'||self!==top){document.documentElement.classList.add('em-projecao');return;}
 const read=k=>{try{return JSON.parse(localStorage.getItem(k)||'null')||{};}catch{return {};}};
 const go=main.querySelector('[data-cz-retoma]'),title=main.querySelector('#cz-retoma-titulo'),note=main.querySelector('[data-cz-retoma-estado]');
 function show(url,label,state,button='Continuar →'){
  go.href=url;go.textContent=button;title.textContent=label;note.textContent=state;
  const target=url.includes('cidadania/')?'inicio-cidadania':'inicio-narrativas';
  main.querySelectorAll('.ld details.cz-fold').forEach(f=>{const current=f.closest('.ld').id===target;f.querySelector('summary').toggleAttribute('data-cz-next',current);if(matchMedia('(max-width:639px)').matches&&!location.hash)f.open=current;});
 }
 const one=read('lente-cidadania-m1-sessoes-v2'),two=read('epi-cidadania-m2');
 const s1=Object.values(one.sessions||{}),s2=Object.entries(two.feitas||{}).filter(([k,v])=>/^passo-\d+$/.test(k)&&v);
 if(s2.length&&s2.length<10)show('cidadania/m2/','Continua «Os algoritmos»','Retoma a sessão seguinte do Módulo 2.');
 else if(s1.some(s=>s.done)&&s1.filter(s=>s.done).length<10)show('cidadania/m1/','Continua «Ser-se humano»','Retoma a sessão seguinte do Módulo 1.');
 const ultima=read('epi-ultima');
 const portuguese=(async()=>{if(typeof ultima.id!=='string'||!/^m[1-9]-f\d+$/i.test(ultima.id))return null;const id=ultima.id.toLowerCase(),url=new URL('../pt/'+id.split('-')[0]+'/licao-'+id+'/',location.href);try{const r=await fetch(url,{method:'HEAD',signal:AbortSignal.timeout(3000)});return r.ok?{url:url.href,time:Number(ultima.t)||0}:null;}catch{return null;}})();
 Promise.all([portuguese,fetch('assets/laboratorio/percursos.json').then(r=>{if(!r.ok)throw Error();return r.json();}).catch(()=>null)]).then(([pt,data])=>{
  if(!data){if(pt)show(pt.url,'A última lição que abriste','Abre-a no Português, onde a deixaste.');return;}
  const states=new Map();for(const p of data.pieces){const q=p.progress,s=read(q.key);let value;if(q.kind==='formas'){const item=s.version===1&&s.itens&&s.itens[q.id];value=item&&(item.revi||item.experimentei);}else if(q.kind==='montagem')value=s.version===1&&Array.isArray(s.done)&&q.ids.every(id=>s.done.includes(id));else value=s.feitas&&s.feitas[q.id];states.set(p.id,{done:!!value,time:typeof value==='number'&&value>1?value:0});}
  let last=null,latest=0;for(const p of data.pieces){const st=states.get(p.id);if(st.time>latest||(!last&&st.done)){latest=st.time;last=p;}}
  if(pt&&pt.time>latest)show(pt.url,'A última lição que abriste','Abre-a no Português, onde a deixaste.');
  else if(last){const order=data.routes.flatMap(r=>r.pieces),next=order.slice(Math.max(0,order.indexOf(last.id))).concat(order).find(id=>!states.get(id).done),p=data.pieces.find(p=>p.id===next);if(p){const date=latest?new Date(latest).toISOString():null,label=window.EPICartaz.stateLabel({done:true,date});show(p.url,p.title,'Feita: '+last.title+(label.startsWith('Feita ')?', '+label.slice(6):'')+'.');}else{const route=data.routes.find(r=>r.pieces.includes(last.id));show('narrativas/percursos/'+route.id+'/',route.title,'Percurso feito: podes revê-lo.','Rever o percurso →');}}
  const links=main.querySelectorAll('#inicio-narrativas .lab-sets a');data.blocks.forEach((b,i)=>{const a=links[i];if(!a)return;const ids=data.routes.filter(r=>r.block===b.id).flatMap(r=>r.pieces),done=ids.length>0&&ids.every(id=>states.get(id).done),times=ids.map(id=>states.get(id).time),date=done&&times.every(Boolean)?new Date(Math.max(...times)).toISOString():null,next=!done&&i===data.blocks.findIndex(block=>data.routes.filter(r=>r.block===block.id).some(r=>r.pieces.some(id=>!states.get(id).done)));const span=document.createElement('span');span.className='cz-state'+(done?' done':next?' current':'');span.textContent=window.EPICartaz.stateLabel({done,next,date});a.append(span);a.classList.toggle('current',next);});
 }).catch(()=>{});
})();
