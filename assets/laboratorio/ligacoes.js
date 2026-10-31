/* Continuação nas páginas que não usam a configuração EPIJogo.
   As três propostas sem registo anterior só ficam feitas por ação explícita. */
(function(){'use strict';
 const nav=document.querySelector('.lab-fim-percurso');if(!nav)return;
 const proj=new URLSearchParams(location.search).get('projetar')==='1';
 if(proj)nav.querySelectorAll('a').forEach(a=>{const u=new URL(a.href);u.searchParams.set('projetar','1');a.href=u.href;});
 const id=nav.dataset.registo;
 if(id&&!proj){const b=document.createElement('button');b.type='button';b.textContent='Marcar como feito';nav.prepend(b);b.onclick=()=>{try{const s=JSON.parse(localStorage.getItem('lente-laboratorio-v1')||'{}');s.feitas=s.feitas||{};s.feitas[id]=Date.now();localStorage.setItem('lente-laboratorio-v1',JSON.stringify(s));b.textContent='Feito';b.disabled=true;}catch{b.textContent='Não foi possível guardar neste aparelho';}};}
 function place(){const end=document.querySelector('.lf-cartao[data-tipo="fim"],.lf-cartao[data-tipo="exemplo"]:has([data-imprimir])');if(end&&!end.contains(nav))end.appendChild(nav);if(document.querySelector('[data-lf-percurso]')||document.querySelector('#cartoes'))nav.hidden=!end;}
 place();new MutationObserver(place).observe(document.body,{childList:true,subtree:true});
})();
