/* Apoio real, sem desmontar a sessão nem alterar o seu registo. */
(function(){'use strict';
 const raiz=new URL('../../',document.currentScript.src),param=new URLSearchParams(location.search);
 const sessoes=[{n:'01',recurso:'galileu/',nome:'Galileu'},{n:'02',recurso:'personagem-faz/',nome:'A personagem pelo que faz'}];
 const local=p=>new URL('narrativas/'+p,raiz),path=location.pathname.replace(/index\.html$/,'');
 const sessao=sessoes.find(s=>local('ideias/sessao-'+s.n+'/').pathname===path);
 const origem=sessoes.find(s=>s.n===param.get('de-ideias')&&local(s.recurso).pathname===path);
 const projetada=param.get('projetar')==='1'||self!==top;
 if(sessao){
  const destino=local(sessao.recurso);destino.searchParams.set('de-ideias',sessao.n);if(projetada)destino.searchParams.set('projetar','1');
  const a=document.createElement('a');a.href=destino.href;a.textContent='Recurso desta sessão: '+sessao.nome;
  document.querySelector('#epi-apoios-menu').appendChild(a);
  // Os cartões entram no DOM à medida que se avança. Atualizar só o destino conhecido.
  const ajustar=()=>document.querySelectorAll('a[href]').forEach(link=>{const url=new URL(link.href,location.href);if(url.origin===raiz.origin&&url.pathname===destino.pathname)link.href=destino.href;});
  ajustar();new MutationObserver(ajustar).observe(document.body,{childList:true,subtree:true});
  document.addEventListener('click',event=>{
   const link=event.target.closest('a[href]');if(!link||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
   const url=new URL(link.href);if(url.origin!==destino.origin||url.pathname!==destino.pathname)return;
   event.preventDefault();
   const painel=document.createElement('dialog');painel.setAttribute('aria-label','Recurso da sessão: '+sessao.nome);
   painel.style.cssText='width:calc(100% - 16px);max-width:1100px;height:calc(100dvh - 16px);max-height:none;box-sizing:border-box;padding:8px;border:2px solid currentColor;background:var(--papel,#fff);color:var(--tinta,#111);';
   const voltar=document.createElement('button');voltar.type='button';voltar.textContent='Voltar à sessão '+Number(sessao.n)+' de Ideias';voltar.style.cssText='min-height:48px;padding:8px 12px;font:700 1rem Arial;color:inherit;background:inherit;border:1px solid currentColor;';
   const frame=document.createElement('iframe');frame.title=sessao.nome;frame.src=destino.href;frame.style.cssText='display:block;width:100%;height:calc(100% - 56px);border:0;margin-top:8px';
   painel.append(voltar,frame);document.body.appendChild(painel);
   const fechar=()=>{painel.close();painel.remove();removeEventListener('message',mensagem);link.focus();};
   const mensagem=e=>{if(e.source===frame.contentWindow&&e.origin===raiz.origin&&e.data&&e.data.type==='epi-ideias-voltar')fechar();};
   voltar.onclick=fechar;painel.addEventListener('cancel',e=>{e.preventDefault();fechar();});addEventListener('message',mensagem);painel.showModal();voltar.focus();
  });
 }
 if(origem){
  const destino=local('ideias/sessao-'+origem.n+'/');if(projetada)destino.searchParams.set('projetar','1');
  const a=document.createElement('a');a.className='epi-retomar-ideias';a.href=destino.href;a.textContent='Voltar à sessão '+Number(origem.n)+' de Ideias';
  document.body.appendChild(a);
  if(self!==top){
   const voltar=()=>parent.postMessage({type:'epi-ideias-voltar'},raiz.origin);
   a.addEventListener('click',e=>{e.preventDefault();voltar();});
   document.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();voltar();}});
  }
  const css=document.createElement('style');css.textContent='.epi-retomar-ideias{position:fixed;z-index:1001;bottom:16px;left:80px;max-width:calc(100% - 96px);box-sizing:border-box;min-height:48px;display:flex;align-items:center;padding:8px 12px;background:var(--paper,#fff);color:var(--ink,#111);border:2px solid currentColor;font:700 .85rem/1.35 Arial,sans-serif;text-underline-offset:3px}.epi-retomar-ideias:focus-visible{outline:3px solid currentColor;outline-offset:3px}@media print{.epi-retomar-ideias{display:none}}';document.head.appendChild(css);
 }
})();
