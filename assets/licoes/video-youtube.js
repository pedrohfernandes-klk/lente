/* Cópia de pt/assets/pt-lessons/video-youtube.js (main ac99261f), 30/10/2026: o mesmo leitor de vídeo nas lições do Lente (Cidadania). */
/* Vídeo do YouTube dentro de um cartão: nenhum pedido antes do toque (youtube-nocookie), com início e fim opcionais.
   Marcação: <div class="yt" data-yt="ID11" data-ini="segundos" data-fim="segundos" data-titulo="…">
               <button type="button" class="yt-abrir" data-yt-abrir>Ver …</button> <p class="yt-cred">…</p></div> */
(function(){'use strict';
 var ID=/^[\w-]{11}$/;
 function seg(v){v=parseInt(v,10);return isFinite(v)&&v>=0?v:null}
 if(!document.getElementById('yt-css')){var s=document.createElement('style');s.id='yt-css';s.textContent=
  '.yt{margin:12px 0 0;border-top:1px solid currentColor;padding-top:10px}'+
  '.yt .yt-abrir{display:flex;align-items:center;gap:10px;width:100%;min-height:48px;padding:10px 14px;border:2px solid currentColor;background:transparent;color:inherit;font:700 .95rem/1.3 Arial,sans-serif;text-align:left;cursor:pointer}'+
  '.yt .yt-abrir::before{content:"";flex:none;border-style:solid;border-width:7px 0 7px 11px;border-color:transparent transparent transparent currentColor}'+
  '.yt .yt-quadro{position:relative;aspect-ratio:16/9;width:100%;background:#000}.yt .yt-quadro iframe{position:absolute;inset:0;width:100%;height:100%;border:0}'+
  '.yt .yt-fechar{margin:8px 0 0;min-height:44px;padding:8px 12px;border:1px solid currentColor;background:transparent;color:inherit;font:700 .85rem Arial,sans-serif;cursor:pointer}'+
  '.yt .yt-cred{font:.8125rem/1.4 Arial,sans-serif;margin:6px 0 0;color:var(--suave)}';
  document.head.appendChild(s)}
 document.addEventListener('click',function(e){
  var b=e.target.closest('[data-yt-abrir],[data-yt-fechar]');if(!b)return;var box=b.closest('[data-yt]');if(!box)return;
  var abrir=box.querySelector('[data-yt-abrir]');
  if(b.hasAttribute('data-yt-fechar')){var q=box.querySelector('.yt-quadro');if(q)q.remove();b.remove();if(abrir){abrir.hidden=false;abrir.focus()}return}
  var id=box.getAttribute('data-yt');if(!ID.test(id||''))return;
  var ini=seg(box.getAttribute('data-ini')),fim=seg(box.getAttribute('data-fim'));
  var u='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&cc_load_policy=1&hl=pt-PT'+(ini!=null?'&start='+ini:'')+(fim!=null&&(ini==null||fim>ini)?'&end='+fim:'');
  var f=document.createElement('iframe');f.src=u;f.title=box.getAttribute('data-titulo')||'Vídeo';f.allow='autoplay; encrypted-media; picture-in-picture';f.allowFullscreen=true;f.referrerPolicy='strict-origin-when-cross-origin';
  var quadro=document.createElement('div');quadro.className='yt-quadro';quadro.appendChild(f);
  var fechar=document.createElement('button');fechar.type='button';fechar.className='yt-fechar';fechar.setAttribute('data-yt-fechar','');fechar.textContent='Fechar o vídeo';
  if(abrir)abrir.hidden=true;box.insertBefore(quadro,abrir?abrir.nextSibling:box.firstChild);quadro.insertAdjacentElement('afterend',fechar);fechar.focus({preventScroll:true});
 });
})();
