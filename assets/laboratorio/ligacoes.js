/* Continuação nas páginas que não usam a configuração EPIJogo.
   As três propostas sem registo anterior só ficam feitas por ação explícita.
   31/10/2026: um só desenho (continuacao.css), dentro da coluna da página; em projeção também
   dentro da moldura /projetar/; nas peças com motor próprio (#baralho) a continuação fica com o motor. */
(function(){'use strict';
 const SRC=document.currentScript&&document.currentScript.src;
 const nav=document.querySelector('.lab-fim-percurso');if(!nav)return;
 if(document.getElementById('baralho')){nav.remove();return;}
 if(SRC)document.head.insertAdjacentHTML('beforeend','<link rel="stylesheet" href="'+new URL('continuacao.css',SRC)+'">');
 const proj=new URLSearchParams(location.search).get('projetar')==='1'||window.self!==window.top;
 if(proj)nav.querySelectorAll('a').forEach(a=>{const u=new URL(a.href);u.searchParams.set('projetar','1');a.href=u.href;a.setAttribute('data-epi-projection-ready','');});
 const id=nav.dataset.registo;
 if(id&&!proj){const b=document.createElement('button');b.type='button';b.textContent='Marcar como feito';nav.prepend(b);
  try{const s0=JSON.parse(localStorage.getItem('lente-laboratorio-v1')||'{}');if(s0.feitas&&s0.feitas[id]){b.textContent='Feito';b.disabled=true;}}catch{}
  b.onclick=()=>{try{const s=JSON.parse(localStorage.getItem('lente-laboratorio-v1')||'{}');s.feitas=s.feitas||{};s.feitas[id]=Date.now();localStorage.setItem('lente-laboratorio-v1',JSON.stringify(s));b.textContent='Feito';b.disabled=true;}catch{b.textContent='Não foi possível guardar neste aparelho';}};}
 const links=[...nav.querySelectorAll('a')],next=links.length>1?links[links.length-1]:null;
 function place(){
  const end=document.querySelector('.lf-cartao[data-tipo="fim"],.lf-cartao[data-tipo="exemplo"]:has([data-imprimir])');
  if(end&&!end.contains(nav))end.appendChild(nav);
  // No cartão final, o botão negro do motor já leva à peça seguinte.
  if(next)next.hidden=!!(end&&end.contains(nav));
  const col=document.querySelector('main')||document.querySelector('.formas-page main, article');
  if(!end&&col&&!col.contains(nav))col.appendChild(nav);
  if(document.querySelector('[data-lf-percurso]')||document.querySelector('#cartoes'))nav.hidden=!end;
 }
 place();new MutationObserver(place).observe(document.body,{childList:true,subtree:true});
})();
