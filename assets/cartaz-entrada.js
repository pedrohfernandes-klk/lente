/* 01/11/2026: retoma sem escrever progresso. Os scripts anteriores permanecem. */
(function(){'use strict';
 const main=document.querySelector('[data-cartaz-entrada]');if(!main)return;
 const projected=new URLSearchParams(location.search).get('projetar')==='1';
 if(projected){document.documentElement.classList.add('em-projecao');return;}
 const read=k=>{try{return JSON.parse(localStorage.getItem(k)||'null')||{};}catch{return {};}};
 const go=main.querySelector('[data-cz-retoma]'),title=main.querySelector('#cz-retoma-titulo'),note=main.querySelector('[data-cz-retoma-estado]');
 function show(url,label,state){go.href=url;go.textContent='Continuar →';title.textContent=label;note.textContent=state;}
 const ultima=read('epi-ultima');
 // Só retomar uma lição que existe: os ids antigos não são transformados em destinos inventados.
 if(typeof ultima.id==='string' && /^m[1-9]-f\d+$/i.test(ultima.id)) {
   const id=ultima.id.toLowerCase(),url=new URL('../pt/'+id.split('-')[0]+'/licao-'+id+'/',location.href);
   fetch(url,{method:'HEAD'}).then(r=>{if(r.ok && Number(ultima.t)>latest)show(url.href,'Retoma a última lição aberta','A seguir: continuar a leitura no Português.');}).catch(()=>{});
 }
 let latest=0;
 fetch('assets/laboratorio/percursos.json').then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{
   const states=new Map();
   for(const p of data.pieces){const q=p.progress,s=read(q.key);let value;
     if(q.kind==='formas'){const item=s.version===1&&s.itens&&s.itens[q.id];value=item&&(item.revi||item.experimentei);}
     else if(q.kind==='montagem')value=s.version===1&&Array.isArray(s.done)&&q.ids.every(id=>s.done.includes(id));
     else value=s.feitas&&s.feitas[q.id];
     states.set(p.id,{done:!!value,time:typeof value==='number'&&value>1?value:0});
   }
   let last=null;
   for(const p of data.pieces){const st=states.get(p.id),t=st.time;if(t>latest||(!last&&st.done)){latest=t;last=p;}}
   if(last && latest>=Number(ultima.t||0)) {
     const route=data.routes.find(r=>r.pieces.includes(last.id));
     if(route){const next=route.pieces.find(id=>!states.get(id).done);const p=next&&data.pieces.find(p=>p.id===next);
       show(p?p.url:'narrativas/percursos/'+route.id+'/',p?p.title:route.title,p?'A seguir: a primeira peça por concluir deste percurso.':'Feita: podes rever este percurso.');}
   }
   const links=main.querySelectorAll('#inicio-narrativas .lab-sets a');
   data.blocks.forEach((b,i)=>{const a=links[i];if(!a)return;const ids=data.routes.filter(r=>r.block===b.id).flatMap(r=>r.pieces),done=ids.length>0&&ids.every(id=>states.get(id).done);
     const times=ids.map(id=>states.get(id).time),stamp=done&&times.every(Boolean)?new Date(Math.max(...times)):null,date=stamp&&Number.isFinite(stamp.getTime())?stamp.toISOString():null;
     const next=!done && i===data.blocks.findIndex(block=>data.routes.filter(r=>r.block===block.id).some(r=>r.pieces.some(id=>!states.get(id).done)));
     const span=document.createElement('span');span.className='cz-state'+(done?' done':next?' current':'');span.textContent=window.EPICartaz.stateLabel({done,next,date});a.append(span);
   });
 }).catch(()=>{});
})();
