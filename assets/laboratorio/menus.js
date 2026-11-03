/* Apenas apresentação: não consulta nem escreve armazenamento. */
(function(){'use strict';const root=document.querySelector('[data-menu-piloto]');if(!root)return;
 let target=null;try{target=document.getElementById(decodeURIComponent(location.hash.slice(1)));}catch{}
 root.querySelectorAll('.cz-fold').forEach(f=>{f.open=!!target&&(f.contains(target)||target.contains(f));});
 const nav=document.querySelector('.menu-portas');if(nav)nav.addEventListener('keydown',e=>{if(e.key==='Escape'){nav.open=false;nav.querySelector('summary').focus();e.preventDefault();}});
 let saved=null;addEventListener('beforeprint',()=>{saved=[...root.querySelectorAll('details')].map(el=>[el,el.open]);saved.forEach(([el])=>el.open=true);});
 addEventListener('afterprint',()=>{if(saved)saved.forEach(([el,open])=>el.open=open);saved=null;});
})();
