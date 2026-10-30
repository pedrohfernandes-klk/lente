(function(){'use strict';
 const key='lente-formas-corta-v1',ids=['curiosidade','suspense','surpresa','julgamento'];let done=[];
 try{const saved=JSON.parse(localStorage.getItem(key)||'{}');if(saved.version===1&&Array.isArray(saved.done))done=ids.filter(id=>saved.done.includes(id));}catch{}
 document.querySelectorAll('[data-formas-progress]').forEach(el=>el.textContent=done.length+' de 4 experiências de montagem registadas');
 const projetar=new URL(location.href).searchParams.get('projetar')==='1';
 const next=ids.find(id=>!done.includes(id))||ids[0];document.querySelectorAll('[data-formas-next]').forEach(a=>{const u=new URL(a.href);u.searchParams.set('experiencia',next);if(projetar)u.searchParams.set('projetar','1');a.href=u.href;});
 /* 29/10/2026: «A cena que falta» e «Certa manhã» registam «experimentei» e «revi» em lente-formas-v1. Aqui só se lê; nenhuma chave é escrita. */
 const novos=['cena-que-falta','certa-manha'];let reg={};
 try{const v=JSON.parse(localStorage.getItem('lente-formas-v1')||'{}');if(v.version===1&&v.itens&&typeof v.itens==='object')reg=v.itens;}catch{}
 const tem=(id,k)=>!!(reg[id]&&typeof reg[id][k]==='number'&&reg[id][k]>0);
 document.querySelectorAll('[data-lf-selos]').forEach(el=>{const id=el.dataset.lfSelos,s=[];if(tem(id,'experimentei'))s.push('Já fiz');if(tem(id,'revi'))s.push('Voltei a ver');el.innerHTML=s.map(x=>'<span class="lf-selo">'+x+'</span>').join(' ');el.hidden=!s.length;});
 const n=novos.filter(id=>tem(id,'experimentei')||tem(id,'revi')).length;
 document.querySelectorAll('[data-lf-registo]').forEach(el=>el.textContent=n?'Experimentaste '+n+' de 2.':'Ainda não experimentaste nenhuma.');
 const prox=novos.find(id=>!tem(id,'experimentei'))||novos.find(id=>!tem(id,'revi'));
 document.querySelectorAll('[data-lf-proxima]').forEach(a=>{const porta=prox&&document.querySelector('[data-lf-porta="'+prox+'"]');if(!porta){a.hidden=true;return;}const u=new URL(porta.href);if(projetar)u.searchParams.set('projetar','1');a.href=u.href;});
})();

// 30/10/2026: Laboratório simples (pedido do docente). Âncoras antigas e pesquisa sem escrita de progresso.
(function(){
 function encaminhar(){if(document.body.classList.contains('lab-simples')&&location.hash)location.replace('tudo/'+location.search+location.hash);}
 addEventListener('hashchange',encaminhar);encaminhar();
 var input=document.querySelector('[data-lab-pesquisa]');if(input)input.oninput=function(){var q=this.value.toLocaleLowerCase('pt-PT');document.querySelectorAll('a.missao').forEach(function(a){a.hidden=!a.textContent.toLocaleLowerCase('pt-PT').includes(q);});if(q)document.querySelectorAll('details.lab-bundle,details.lab-subset').forEach(function(d){d.open=true;});};
})();
