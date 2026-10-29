(function(){'use strict';
 const key='lente-formas-corta-v1',ids=['curiosidade','suspense','surpresa','julgamento'];let done=[];
 try{const saved=JSON.parse(localStorage.getItem(key)||'{}');if(saved.version===1&&Array.isArray(saved.done))done=ids.filter(id=>saved.done.includes(id));}catch{}
 document.querySelectorAll('[data-formas-progress]').forEach(el=>el.textContent=done.length+' de 4 experiências de montagem registadas');
 const next=ids.find(id=>!done.includes(id))||ids[0];document.querySelectorAll('[data-formas-next]').forEach(a=>{const u=new URL(a.href);u.searchParams.set('experiencia',next);if(new URL(location.href).searchParams.get('projetar')==='1')u.searchParams.set('projetar','1');a.href=u.href;});
})();
