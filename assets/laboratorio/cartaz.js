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
   if(next)el.setAttribute('data-cz-next','');
 });
 // A entrada tem cartões de percursos: abrir a banda correspondente ao destino da retoma.
 const go=root.querySelector('[data-continuar]');
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
