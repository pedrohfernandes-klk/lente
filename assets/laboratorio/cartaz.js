/* 01/11/2026: D4/D5, camada de apresentação; preserva o motor de progresso. */
(function(){'use strict';
 const root=document.querySelector('[data-cartaz-laboratorio]');if(!root)return;
 const data=JSON.parse(document.getElementById('lab-dados').textContent),by=Object.fromEntries(data.map(p=>[p.id,p]));
 const projected=new URLSearchParams(location.search).get('projetar')==='1'||window.self!==window.top;
 const read=k=>{if(projected)return {};try{return JSON.parse(localStorage.getItem(k)||'{}')||{};}catch{return {};}};
 root.querySelectorAll('[data-estado]').forEach(el=>{
   const q=by[el.dataset.estado].progress,s=read(q.key);let v;
   if(q.kind==='formas'){const item=s.version===1&&s.itens&&s.itens[q.id];v=item&&(item.revi||item.experimentei);}
   else if(q.kind==='montagem')v=s.version===1&&Array.isArray(s.done)&&q.ids.every(id=>s.done.includes(id));
   else v=s.feitas&&s.feitas[q.id];
   const done=!!v,next=el.closest('li').classList.contains('seguir');
   const date=typeof v==='number'&&v>1?new Date(v):null;
   const label=done?'Feita'+(date&&Number.isFinite(date.getTime())?' '+String(date.getDate()).padStart(2,'0')+'/'+String(date.getMonth()+1).padStart(2,'0'):''):next?'A seguir':'';
   el.textContent=label;el.classList.toggle('done',done);el.classList.toggle('current',!done&&next);
   // 01/11/2026: o filete pertence à linha inteira, não ao rótulo.
   const row=el.closest('.cz-row');if(row)row.classList.toggle('current',!done&&next);
   if(next)el.setAttribute('data-cz-next','');
 });
 // A entrada tem cartões de percursos: abrir a banda correspondente ao destino da retoma.
 const go=root.querySelector('[data-continuar]');
 const state=p=>{const q=p.progress,s=read(q.key);if(q.kind==='formas'){const item=s.version===1&&s.itens&&s.itens[q.id];return item&&(item.revi||item.experimentei);}if(q.kind==='montagem')return s.version===1&&Array.isArray(s.done)&&q.ids.every(id=>s.done.includes(id));return s.feitas&&s.feitas[q.id];};
 // 01/11/2026: título e estado separados da ação; nunca inventar uma data.
 if(go){const ids=JSON.parse(go.dataset.continuar),next=ids.find(id=>!state(by[id])),p=by[next||ids[0]],done=ids.filter(id=>state(by[id]));
  root.querySelector('#cz-prox').textContent=p.title;go.textContent=next?(done.length?'Continuar →':'Começar →'):'Rever o percurso →';
  const last=done.sort((a,b)=>(Number(state(by[b]))||0)-(Number(state(by[a]))||0))[0],stamp=last&&state(by[last]);
  root.querySelector('[data-cz-estado]').textContent=last?'Feita: '+by[last].title+(typeof stamp==='number'&&stamp>1?', '+new Date(stamp).toLocaleDateString('pt-PT',{day:'2-digit',month:'2-digit'}):'')+'.':'';
  root.querySelectorAll('[data-cz-route]').forEach(row=>{const list=JSON.parse(row.dataset.czRoute),complete=list.every(id=>state(by[id])),current=!!next&&list.includes(next),values=list.map(id=>state(by[id])),date=complete&&values.every(v=>typeof v==='number'&&v>1)?new Date(Math.max(...values)):null;
   const label=row.querySelector('.cz-state');label.textContent=complete?'Feita'+(date?' '+date.toLocaleDateString('pt-PT',{day:'2-digit',month:'2-digit'}):''):current?'A seguir':'';label.classList.toggle('done',complete);row.classList.toggle('current',current);row.toggleAttribute('data-cz-next',current);
  });
 }
 root.querySelectorAll('.contagem').forEach(c=>{c.hidden=/^0 de /.test(c.textContent.trim());});
 if(go){const ids=JSON.parse(go.dataset.continuar),next=data.find(p=>new URL(p.url,new URL(root.dataset.raiz,location.href)).pathname===new URL(go.href).pathname);
   if(next)root.querySelectorAll('.cz-fold').forEach(f=>{
     const ids=JSON.parse(f.dataset.czIds||'[]');
     if(ids.includes(next.id)||f.querySelector('[data-estado="'+CSS.escape(next.id)+'"]'))f.querySelector('summary').setAttribute('data-cz-next','');
   });
 }
 function revealHash(){try{const target=document.getElementById(decodeURIComponent(location.hash.slice(1))),fold=target&&(target.matches('.bloco')?target.querySelector('.cz-fold'):target.closest('.cz-fold'));if(fold)fold.open=true;}catch{}}
 document.addEventListener('DOMContentLoaded',revealHash);
 addEventListener('hashchange',revealHash);
})();
