// 02/11/2026: decisão 125. O fundo «Os carris» só anda fora da projeção (a projeção abre a página numa moldura) e sem
// movimento reduzido, e pára quando sai do ecrã. Sem este script, a alavanca fica a meio.
(function(){
 var f=document.querySelector('.ju .jc-fundo');
 if(!f||!window.matchMedia)return;
 var projetada=/[?&]projetar=1(&|$)/.test(location.search)||window.self!==window.top;
 if(projetada||!matchMedia('(prefers-reduced-motion: no-preference)').matches)return;
 f.classList.add('jc-anda');
 if('IntersectionObserver'in window)new IntersectionObserver(function(e){f.classList.toggle('jc-fora',!e[e.length-1].isIntersecting);}).observe(f);
})();
