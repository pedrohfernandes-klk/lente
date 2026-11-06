/* 05/11/2026: decisão 163. O comportamento novo do menu ≡ (marcação de tools/menu_casca.py), sem tocar em casca.js nem em
   jogo.js, que são cópias do Português. Carrega-se com defer, depois deles.
   1. Foco preso: com o painel aberto, Tab e Shift+Tab só circulam dentro dele; o corpo, as ações e a folha ficam inertes.
      A barra de topo não fica inerte, porque casca.js devolve o foco ao ≡ logo a seguir a esconder o painel. Escape, o ✕ e o
      véu continuam a ser de casca.js.
   2. Posição: ao abrir, «Cartão N de M.», lido do contador da barra («4/18»); vazio quando o contador está vazio.
   3. Cartões já feitos: o item aparece só quando a barra de progresso está ativa; fecha o menu e abre a mesma grelha de leitura
      da barra (nada se apaga nem se refaz).
   4. Projeção: com ?projetar=1 (ou dentro da moldura de projeção), «Sair da projeção» à vista e «Projetar na aula» escondido.
   05/11/2026 (revisão): na projeção, o painel leva .m-proj, que põe a letra do painel em 22 px de base também nas famílias em
   que a raiz não cresce (assets/licoes/menu.css); nenhuma classe nova no html. */
(function(){'use strict';
 var painel=document.querySelector('.casca-menu.m2[data-c-painel]');if(!painel)return;
 var raiz=painel.closest('[data-casca]')||document.body,menuEl=raiz.querySelector('[data-c-menu]'),num=raiz.querySelector('[data-c-num]'),barra=raiz.querySelector('[data-c-barra]');
 var pos=painel.querySelector('[data-c-pos]'),rever=painel.querySelector('[data-c-rever]');
 var html=document.documentElement;
 var proj=/[?&]projetar=1(&|$)/.test(location.search)||html.classList.contains('epi-projection')||html.classList.contains('em-projecao')||window.self!==window.top;
 if(proj)painel.classList.add('m-proj');
 painel.querySelectorAll('.so-normal').forEach(function(a){a.hidden=proj});
 painel.querySelectorAll('.so-aula').forEach(function(a){a.hidden=!proj});
 if(menuEl&&!menuEl.hasAttribute('aria-controls'))menuEl.setAttribute('aria-controls','c-menu');
 function irmaos(){return Array.prototype.slice.call(raiz.querySelectorAll(':scope>.casca-corpo,:scope>.casca-acoes,:scope>.casca-folha'))}
 function focaveis(){return Array.prototype.slice.call(painel.querySelectorAll('a[href],button,summary,input,select,textarea,[tabindex]:not([tabindex="-1"])')).filter(function(el){return !el.disabled&&!el.closest('[hidden]')&&el.getClientRects().length})}
 function posicao(){if(!pos)return;var t=num?num.textContent.replace(/\s+/g,''):'',m=/^(\d+)\/(\d+)$/.exec(t);pos.textContent=m?'Cartão '+m[1]+' de '+m[2]+'.':''}
 function aberto(){
  var a=!painel.hidden;
  irmaos().forEach(function(el){if(a){el.setAttribute('inert','');el.setAttribute('data-m-inerte','')}else if(el.hasAttribute('data-m-inerte')){el.removeAttribute('inert');el.removeAttribute('data-m-inerte')}});
  if(a){posicao();if(rever)rever.hidden=!barra||barra.disabled||barra.hidden}
 }
 new MutationObserver(aberto).observe(painel,{attributes:true,attributeFilter:['hidden']});
 painel.addEventListener('keydown',function(ev){
  if(ev.key!=='Tab'||painel.hidden)return;
  var f=focaveis();if(!f.length)return;
  var i=f.indexOf(document.activeElement);
  if(ev.shiftKey&&(i<=0)){ev.preventDefault();f[f.length-1].focus()}
  else if(!ev.shiftKey&&(i===-1||i===f.length-1)){ev.preventDefault();f[0].focus()}
 });
 if(rever)rever.addEventListener('click',function(){
  var fecha=painel.querySelector('[data-c-fecha-menu]');if(fecha)fecha.click();else painel.hidden=true;
  if(barra&&!barra.disabled)barra.click();
 });
 aberto();
})();
