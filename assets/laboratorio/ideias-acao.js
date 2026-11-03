/* Só lê as chaves reais das sessões publicadas. Projeção não consulta progresso. */
(function () {
 'use strict';
 const projetada=new URLSearchParams(location.search).get('projetar')==='1'||self!==top||document.documentElement.classList.contains('epi-projection');
 document.querySelectorAll('[data-ideias-sessoes]').forEach(node=>{
  const lista=JSON.parse(node.textContent),botao=node.previousElementSibling;
  if(projetada)return;
  const estados=lista.map(s=>{try{return JSON.parse(localStorage.getItem(s.chave)||'null')}catch{return null}});
  const proxima=estados.findIndex(s=>!window.EPILabProgresso.feita(s));
  const iniciada=estados.some(s=>s&&typeof s==='object'&&Object.keys(s).length>0);
  if(proxima<0){botao.textContent='Rever Ideias →';botao.href=lista[0].url;}
  else if(iniciada){botao.textContent='Continuar Ideias →';botao.href=lista[proxima].url;}
 });
})();
