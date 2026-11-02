/* 02/11/2026: proposta A; só lê progresso. Projeção não lê nem grava. */
(function(){'use strict';
var proj=/[?&]projetar=1(&|$)/.test(location.search)||window.self!==window.top||document.documentElement.classList.contains('epi-projection');
if(proj)document.documentElement.classList.add('em-projecao');
var lista=Array.from(document.querySelectorAll('ol.sessoes li[data-chave]')),feitas=[],proxima=null;
lista.forEach(function(li){var st=null;if(!proj)try{st=JSON.parse(localStorage.getItem(li.dataset.chave)||'null')}catch(e){}
var estado=li.querySelector('[data-estado]');if(window.EPILabProgresso.feita(st)){
 var t=window.EPILabProgresso.data(st),d=t===null?null:new Date(t),data=d&&!isNaN(d)?String(d.getDate()).padStart(2,'0')+'/'+String(d.getMonth()+1).padStart(2,'0'):'';
 li.classList.add('feita');estado.textContent='Feita'+(data?' '+data:'');feitas.push({li:li,data:data});
}else if(!proxima){proxima=li;li.classList.add('seguir');li.querySelector('a').setAttribute('aria-current','step');estado.textContent='A seguir';}});
var botao=document.querySelector('[data-p-botao]'),titulo=document.querySelector('[data-p-t]'),feito=document.querySelector('[data-p-feito]');
if(feitas.length){var ultima=feitas[feitas.length-1];feito.textContent='Feita: sessão '+ultima.li.dataset.n+(ultima.data?', '+ultima.data:'')+'.';
var alvo=proxima||ultima.li;botao.href=alvo.dataset.href;botao.textContent=(proxima?'Continuar na sessão ':'Rever a sessão ')+alvo.dataset.n+' →';
titulo.textContent=proxima?alvo.dataset.titulo:'As sessões publicadas estão feitas.';}
})();
