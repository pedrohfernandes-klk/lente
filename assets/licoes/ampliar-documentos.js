/* Cópia de pt/assets/ampliar-documentos.js (main 10da5a83), 05/11/2026: ampliação de todas as figuras das lições do Lente (toque, Enter e Espaço; Esc fecha e devolve o foco), plano do molde da Cidadania, pedido 1. Corrige-se no Português e copia-se de novo. */
// 02/11/2026: derivado do ampliador comum das fontes, mantendo EPIAmpliar.
(function(){if(window.EPIAmpliar)return;var ov=null,ult=null,fundo=[];
function rotuloAmpliar(img,leg){var t=String(leg||(img&&img.getAttribute("alt"))||"").replace(/\s+/g," ").trim();var d=/^([^:]{1,80}?):\s+(\S.*)$/.exec(t);if(d&&/^(Fotografia|Ilustração|Desenho|Gravura|Pintura|Imagem|Mapa|Planta)\b/i.test(d[1]))t=d[2];var re=/[.:;](?=\s)|\s(?=\()/g,m,f;while((m=re.exec(t))){if(m.index<12)continue;if(t.charAt(m.index)==="."&&/(^|[\s(])([A-ZÁÉÍÓÚÂÊÔ]|Sr|Sra|Dr|Dra|Sto|Sta|séc|p|pp|vol|cap|n\.º|ed|trad)\.$/.test(t.slice(0,m.index+1)))continue;if(t.charAt(m.index)===" "){f=t.indexOf(")",m.index);if(f>0&&f<70){re.lastIndex=f;continue}}t=t.slice(0,m.index);break}if(t.length>70){t=t.slice(0,70);var s=t.lastIndexOf(" ");t=(s>30?t.slice(0,s):t).replace(/[,.;:\s]+$/,"")+"\u2026"}return t?"Ampliar: "+t:"Ampliar: imagem sem legenda"}
function focaveis(){return ov?[].slice.call(ov.querySelectorAll('button,[href],input,select,textarea,[tabindex]:not([tabindex="-1"])')).filter(function(e){return !e.disabled&&e.getClientRects().length}):[]}
function fecha(){if(!ov)return;var o=ov;ov=null;if(o.parentNode)o.parentNode.removeChild(o);fundo.forEach(function(x){x.removeAttribute("inert")});fundo=[];document.documentElement.style.overflow="";var u=ult;ult=null;if(u&&u.isConnected&&u.focus)try{u.focus({preventScroll:true})}catch(x){}}
function abre(img,leg,de){if(ov)fecha();var a=document.activeElement;ult=de||(img&&img.hasAttribute("tabindex")?img:(a&&a!==document.body?a:null));
ov=document.createElement("div");ov.className="amp-ov";ov.setAttribute("role","dialog");ov.setAttribute("aria-modal","true");ov.setAttribute("aria-label",rotuloAmpliar(img,leg).replace(/^Ampliar: /,"Imagem ampliada: "));
var i=document.createElement("img");i.src=img.getAttribute("data-original")||img.currentSrc||img.src;i.alt=img.alt||"";var area=document.createElement("div");area.className="amp-area";area.tabIndex=0;area.setAttribute("aria-label","Imagem: usa as setas para percorrer quando ampliada");area.appendChild(i);ov.appendChild(area);
var p=document.createElement("p");p.className="amp-leg";p.textContent=leg||img.alt||"";ov.appendChild(p);
var x=document.createElement("button");x.type="button";x.className="amp-x";x.setAttribute("aria-label","Fechar a imagem ampliada");x.textContent="\u00d7";ov.appendChild(x);
var escala=1,baseW=0,baseH=0;
var barra=document.createElement("div");barra.className="amp-tools";
function zoom(v){if(!baseW){baseW=i.getBoundingClientRect().width;baseH=i.getBoundingClientRect().height}escala=Math.max(1,Math.min(4,v));i.style.maxWidth="none";i.style.maxHeight="none";i.style.width=(baseW*escala)+"px";i.style.height=(baseH*escala)+"px";estado.textContent=Math.round(escala*100)+" %";menos.disabled=escala===1;mais.disabled=escala===4}
function botao(txt,fn){var b=document.createElement("button");b.type="button";b.textContent=txt;b.onclick=fn;barra.appendChild(b);return b}
var menos=botao("Reduzir",function(){zoom(escala-.5)}),mais=botao("Ampliar",function(){zoom(escala+.5)});
botao("Imagem inteira",function(){zoom(1);area.scrollTop=area.scrollLeft=0});
var estado=document.createElement("output");estado.setAttribute("aria-live","polite");estado.textContent="100 %";barra.appendChild(estado);menos.disabled=true;ov.appendChild(barra);
ov.addEventListener("keydown",function(e){if(e.key==="+"||e.key==="="){e.preventDefault();e.stopPropagation();zoom(escala+.5)}else if(e.key==="-"){e.preventDefault();e.stopPropagation();zoom(escala-.5)}});
x.onclick=fecha;ov.addEventListener("click",function(e){if(e.target===ov)fecha()});document.body.appendChild(ov);
// o resto da página fica inerte (nem foco nem leitor de ecrã) enquanto a imagem está aberta
fundo=[];[].forEach.call(document.body.children,function(n){if(n!==ov&&!n.hasAttribute("inert")&&!/^(SCRIPT|STYLE|TEMPLATE|LINK)$/.test(n.nodeName)){n.setAttribute("inert","");fundo.push(n)}});
document.documentElement.style.overflow="hidden";x.focus()}
function legendaDe(img){var f=img.closest("figure");if(f){var c=f.querySelector("figcaption");if(c){var p=c.querySelector(":scope > p");if(p)return p.textContent.replace(/\s+/g," ").trim();var k=c.cloneNode(true);[].forEach.call(k.querySelectorAll("details,table,summary,caption"),function(n){n.parentNode.removeChild(n)});return k.textContent.replace(/\s+/g," ").trim()}}return img.getAttribute("data-legenda")||img.alt||""}
function elegivel(img){if(!img||img.tagName!=="IMG")return false;if(img.closest("a,button,.amp-ov,.ver-fig,.lp-img,.mf,.cavalo"))return false;if(img.classList.contains("sem-amp"))return false;if(!img.closest("figure")&&!img.hasAttribute("data-ampliar"))return false;return true}
document.addEventListener("click",function(e){var img=e.target&&e.target.closest?e.target.closest("img"):null;if(!elegivel(img))return;e.preventDefault();abre(img,legendaDe(img),img)});
// com a imagem aberta: Esc fecha só a imagem; Tab e Shift+Tab andam só dentro do diálogo (fase de captura, antes dos outros)
window.addEventListener("keydown",function(e){if(!ov)return;if(e.key==="Escape"||e.key==="Esc"){e.preventDefault();e.stopPropagation();fecha();return}
 if(e.key==="Tab"){var L=focaveis(),at=document.activeElement;e.stopPropagation();if(!L.length){e.preventDefault();return}var a=L[0],z=L[L.length-1];if(!ov.contains(at)){e.preventDefault();(e.shiftKey?z:a).focus();return}if(e.shiftKey&&at===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&at===z){e.preventDefault();a.focus()}}},true);
document.addEventListener("focusin",function(e){if(ov&&!ov.contains(e.target)){var L=focaveis();if(L[0])L[0].focus()}});
document.addEventListener("keydown",function(e){if(ov)return;if((e.key==="Enter"||e.key===" ")&&elegivel(e.target)){e.preventDefault();abre(e.target,legendaDe(e.target),e.target)}});
function marcar(r){var L=(r||document).querySelectorAll?(r||document).querySelectorAll("figure:not(.ver-fig) img,img[data-ampliar]"):[];for(var k=0;k<L.length;k++){var im=L[k];if(!elegivel(im))continue;if(!im.hasAttribute("tabindex"))im.setAttribute("tabindex","0");if(!im.hasAttribute("role"))im.setAttribute("role","button");if(!im.getAttribute("aria-label"))im.setAttribute("aria-label",rotuloAmpliar(im,legendaDe(im)))}}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",function(){marcar()});else marcar();
if(window.MutationObserver)new MutationObserver(function(ms){for(var i=0;i<ms.length;i++)for(var j=0;j<ms[i].addedNodes.length;j++){var n=ms[i].addedNodes[j];if(n.nodeType===1&&n!==ov)marcar(n)}}).observe(document.documentElement,{childList:true,subtree:true});
window.EPIAmpliar={abre:abre,fecha:fecha,rotulo:rotuloAmpliar,legenda:legendaDe}})();
// 02/11/2026: a ligação conserva o destino sem JS e abre o documento no diálogo com JS.
document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest(".documento > a");if(!a||!window.EPIAmpliar)return;var img=a.querySelector("img"),f=a.closest("figure");if(!img)return;e.preventDefault();EPIAmpliar.abre(img,EPIAmpliar.legenda?EPIAmpliar.legenda(img):(img.alt||""),a)});
