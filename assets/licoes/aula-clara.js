/* Cópia de pt/assets/pt-lessons/aula-clara.js (main 10da5a83), 05/11/2026: peças das lições refeitas do Português (linha «Hoje», conceito em passos, «Antes de ler», «Para ir mais longe», resposta projetada), para as sessões da Cidadania no molde novo (plano do molde, pedido 1). Corrige-se no Português e copia-se de novo. */
/* 23/10/2026, aulas claras (plano de melhoria, padrão da Justiça do Lente): peças das lições refeitas.
   Vídeo: <div class="ju-video" data-yt="ID11" data-ini="s" data-fim="s" data-t="título" data-m="canal" data-dur="1 min" data-rot="Ver o excerto">
     o leitor (youtube-nocookie, com início e fim) só nasce ao toque; o motor guarda cópias dos cartões para rever, e uma cópia com o
     leitor volta a ser o botão.
   Conceito: <div class="cc" data-cc> com .cc-passo (o caso, mais perto, o nome, o que não é) e o botão [data-cc-mais]; cada toque
     mostra o passo seguinte; ao imprimir, tudo à vista.
   Lados (decidir e depois abrir) e «Ler mais» são <details> e não precisam de código. */
(function(){"use strict";
var vivos=typeof WeakSet==="function"?new WeakSet():null;
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function botao(c){var d=c.dataset;c.classList.remove("tocado");c.innerHTML='<p class="ju-t">'+esc(d.t)+'</p><p class="ju-m">'+esc(d.m)+'</p><button type="button">'+esc(d.rot||"Ver o vídeo")+(d.dur?' <span>('+esc(d.dur)+')</span>':'')+'</button>'}
var ROT=["Mais perto","O nome","O que não é"];
// modelo dos conceitos (23/10/2026): cada passo diz no data-rot o nome do botão que o abre; data-acende acende as marcas do caso
// (<span data-c="a">); o «Decide» (sem pontos) mostra a resposta neutra e só depois deixa avançar
function rotDe(p,k){return p&&p.getAttribute("data-rot")||ROT[k-1]||"Seguinte"}
function acender(cc,p){var a=(p.getAttribute("data-acende")||"").split(/\s+/).filter(Boolean);a.forEach(function(c){[].forEach.call(cc.querySelectorAll('[data-c="'+c+'"]'),function(m){m.classList.add("acesa")})})}
function arrumar(){
 [].forEach.call(document.querySelectorAll(".ju-video"),function(c){var f=c.querySelector("iframe");if(f&&!(vivos&&vivos.has(f)))botao(c)});
 [].forEach.call(document.querySelectorAll("[data-cc]"),function(c){var b=c.querySelector("[data-cc-mais]"),ps=c.querySelectorAll(".cc-passo"),k=[].filter.call(ps,function(p){return !p.hidden}).length;if(b&&k>=ps.length)b.hidden=true})}
document.addEventListener("click",function(ev){
 var b=ev.target.closest&&ev.target.closest(".ju-video button");
 if(b){var c=b.closest(".ju-video"),d=c.dataset;if(!/^[A-Za-z0-9_-]{11}$/.test(d.yt||""))return;
  [].forEach.call(document.querySelectorAll(".ju-video.tocado"),function(o){if(o!==c)botao(o)});
  var f=document.createElement("iframe");f.src="https://www.youtube-nocookie.com/embed/"+d.yt+"?autoplay=1&rel=0&cc_load_policy=1&hl=pt-PT"+(d.ini?"&start="+d.ini:"")+(d.fim?"&end="+d.fim:"");f.title=d.titulo||d.t||"Vídeo";f.allow="autoplay; encrypted-media; picture-in-picture; fullscreen";f.setAttribute("allowfullscreen","");f.referrerPolicy="strict-origin-when-cross-origin";if(vivos)vivos.add(f);c.innerHTML="";c.classList.add("tocado");c.appendChild(f);try{f.focus()}catch(x){}return}
 var m=ev.target.closest&&ev.target.closest("[data-cc-mais]");
 if(m){var cc=m.closest("[data-cc]"),ps=[].slice.call(cc.querySelectorAll(".cc-passo")),k=ps.filter(function(p){return !p.hidden}).length;if(k<ps.length){ps[k].hidden=false;ps[k].classList.add("cc-novo");acender(cc,ps[k]);if(cc.querySelector(".cc-cx"))cc.classList.add("cc-andar");ps[k].setAttribute("tabindex","-1");try{ps[k].focus({preventScroll:true})}catch(x){}}k++;if(k>=ps.length)m.hidden=true;else m.firstChild.nodeValue=rotDe(ps[k],k)+" ";return}
 var op=ev.target.closest&&ev.target.closest("[data-cc-op]");
 if(op){var dc=op.closest(".cc-decide"),c2=op.closest("[data-cc]");[].forEach.call(dc.querySelectorAll("[data-cc-op]"),function(o){o.setAttribute("aria-pressed",String(o===op))});var r=dc.querySelector(".cc-resp");if(r){r.hidden=false;r.setAttribute("aria-live","polite")}var bm=c2.querySelector("[data-cc-mais]"),ps2=[].slice.call(c2.querySelectorAll(".cc-passo")),k2=ps2.filter(function(p){return !p.hidden}).length;if(bm&&k2<ps2.length){bm.hidden=false;bm.firstChild.nodeValue=rotDe(ps2[k2],k2)+" "}}});
var alvo=document.getElementById("baralho");if(alvo&&window.MutationObserver)new MutationObserver(arrumar).observe(alvo,{childList:true,subtree:true});
window.addEventListener("beforeprint",function(){[].forEach.call(document.querySelectorAll("[data-cc] .cc-passo"),function(p){p.hidden=false;acender(p.closest("[data-cc]"),p)})});})();
