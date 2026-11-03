/* 03/11/2026: dez sessões revistas. As chaves anteriores nunca são escritas. */
(function(){'use strict';
 const root=document.querySelector('[data-c10]');if(!root)return;
 const proj=self!==top||new URLSearchParams(location.search).get('projetar')==='1'||document.documentElement.classList.contains('epi-projection');
 function ler(k){if(proj)return {};try{const v=JSON.parse(localStorage.getItem(k)||'null');return v&&typeof v==='object'&&!Array.isArray(v)?v:{}}catch{return {}}}
 function pintar(){
  const anterior=ler('lente-cidadania-m1-sessoes-v2'),sessoes=anterior.version===2&&anterior.sessions&&!Array.isArray(anterior.sessions)?anterior.sessions:{};
  let proxima=null,feitas=0;
  root.querySelectorAll('[data-session-card]').forEach(card=>{
   const id=card.dataset.sessionCard,n=Number(id),revista=n<=10;
   const chave='epi-cid-m1-s'+id,estado=revista?ler(chave+'-20261103'):sessoes[id]||{};
   const feita=revista?estado.lida===true:estado.done===true;
   const antiga=revista&&(ler(chave).lida===true||(sessoes[id]||{}).done===true);
   if(revista&&feita)feitas++;else if(revista&&!feita&&!proxima)proxima=card;
   card.classList.toggle('is-done',feita);
   const label=card.querySelector('[data-status]');if(label)label.textContent=!revista?(feita?'Formato anterior: feita':'Formato anterior'):feita?'Feita':antiga?'Registo anterior conservado. Nova sessão por fazer.':'Sessão interativa por fazer';
  });
  const contagem=root.querySelector('[data-count]');if(contagem)contagem.textContent=proj?'':feitas+' de 10 sessões interativas feitas';
  const next=root.querySelector('[data-continue]');if(next){next.href=proxima?proxima.querySelector('a').getAttribute('href'):'licoes/01/';next.textContent=proxima?(feitas?'Continuar na sessão ':'Começar na sessão ')+proxima.dataset.sessionCard:'Rever as dez sessões';}
  root.querySelectorAll('[data-session-card]').forEach(card=>card.dataset.current=String(card===proxima));
 }
 pintar();addEventListener('pageshow',pintar);addEventListener('storage',pintar);
 root.querySelectorAll('[data-print]').forEach(b=>{b.hidden=false;b.onclick=()=>print()});
 // Preservar os atalhos das versões anteriores sem mudar o destino dos registos.
 if(location.hash){const h=location.hash.slice(1),u=h.match(/^unidade-([1-6])$/);if(u)location.replace('sessoes/'+['04','05','06','07','08','09'][+u[1]-1]+'/');else if(document.getElementById(h)?.closest('[hidden]'))location.replace('percurso-anterior.html'+location.hash);}
})();
