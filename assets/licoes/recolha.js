/* 05/11/2026 (plano do molde da Cidadania, pedido 1; decisões 115 e 118): a peça comum que recolhe, lista, copia e partilha o
   que o aluno guarda ao longo de uma sessão. Na Cidadania chama-se «artefactos»; no Laboratório será a caixa dos «cartões»
   (decisão 115), com outro nome e a mesma peça. Fica só no aparelho (localStorage, uma chave por coleção), nunca vai na
   entrega ao docente, e não lê nem grava nada na projeção. Não conta como exercício: vive dentro dos cartões de ler.

   Uso: EPIRecolha.ligar({raiz, chave, sessao, titulo, colecao, nome, lista}) antes de EPIJogo.montar(...).
     chave    a chave da coleção (por exemplo «epi-cid-m1-artefactos»);
     sessao   a chave da sessão (por exemplo «epi-cid-m1-s01»); titulo, o título da sessão;
     colecao  o nome da coleção, à cabeça do texto copiado («Cidadania, módulo 1, Humanos»);
     nome     o nome no plural («artefactos»); lista, o título da lista («Os teus artefactos»).

   Marcação nos cartões (o HTML dos cartões de ler):
     [data-artefacto="id"][data-rot="A pergunta"]   guarda-se quando fica à vista (o texto do elemento, ou data-texto);
     .posicao[data-artefacto="id"][data-rot="…"]    escolha sem certa nem errada: botões .pos-op com data-valor (e
                                                    data-frase, a forma dentro de uma frase); guarda-se ao escolher e
                                                    pode mudar-se; abre os [data-depois-de="id"];
     [data-modelo="No início decidiste {a}; depois, {b}."]  preenche-se com o que está guardado (fica escondido se faltar);
     [data-recolha-lista]                           a lista da sessão, com «Copiar para as notas» e «Partilhar»;
     [data-recolha-todas]                           todas as sessões da coleção (a página «Os meus artefactos»). */
(function(){"use strict";
if(window.EPIRecolha)return;
var CFG=null,feitos=typeof WeakSet==="function"?new WeakSet():null;
function ler(k){try{var v=JSON.parse(localStorage.getItem(k)||"null");return v&&typeof v==="object"&&!Array.isArray(v)?v:null}catch(x){return null}}
function gravar(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(x){}}
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function limpo(s){return String(s==null?"":s).replace(/\s+/g," ").trim()}
function minuscula(s){s=limpo(s);return s?s.charAt(0).toLowerCase()+s.slice(1):s}
function projecao(){var h=document.documentElement;return /[?&]projetar=1(&|$)/.test(location.search)||h.classList.contains("em-projecao")||h.classList.contains("epi-projection")||window.self!==window.top}
function dd(n){return(n<10?"0":"")+n}
function dataCurta(t){var d=new Date(t);return isNaN(d)?"":dd(d.getDate())+"/"+dd(d.getMonth()+1)+"/"+d.getFullYear()}
function estado(){var e=CFG?ler(CFG.chave):null;if(!e||e.v!==1||!e.sessoes||typeof e.sessoes!=="object")e={v:1,sessoes:{}};return e}
function daSessao(e,k){var s=e.sessoes[k];if(!s||!Array.isArray(s.itens))s=e.sessoes[k]={titulo:CFG.titulo||"",itens:[]};return s}
function itens(k){var e=estado(),s=e.sessoes[k||CFG.sessao];return s&&Array.isArray(s.itens)?s.itens:[]}
function valor(id){var it=itens().filter(function(x){return x&&x.id===id})[0];return it||null}
function guardar(id,rot,texto,frase){if(!CFG||projecao()||!id||!limpo(texto))return false;var e=estado(),s=daSessao(e,CFG.sessao),agora=Date.now();s.titulo=CFG.titulo||s.titulo;
 var it=s.itens.filter(function(x){return x&&x.id===id})[0];if(it){if(it.texto===limpo(texto)&&it.rot===limpo(rot))return false;it.texto=limpo(texto);it.rot=limpo(rot);it.frase=frase?limpo(frase):undefined;it.t=agora}
 else s.itens.push({id:id,rot:limpo(rot),texto:limpo(texto),frase:frase?limpo(frase):undefined,t:agora});
 gravar(CFG.chave,e);return true}
function linha(onde,txt){if(!onde)return;var p=onde.querySelector(":scope > .guardaste");if(!p){p=document.createElement("p");p.className="guardaste";p.setAttribute("role","status");onde.appendChild(p)}if(p.textContent!==txt)p.textContent=txt}
function cartaoDe(el){return el.closest?el.closest(".cartao"):null}
function emRevisao(el){return !!(el.closest&&el.closest(".jogo.rev"))}
function escondido(el){for(var n=el;n&&n.nodeType===1;n=n.parentElement){if(n.hidden)return true;if(n.classList&&n.classList.contains("cartao"))break}return false}
function textoDe(el){return el.getAttribute("data-texto")||el.textContent}
// o que se guarda ao ficar à vista
function verArtefactos(raiz){if(!CFG||projecao())return;[].forEach.call(raiz.querySelectorAll("[data-artefacto]:not(.posicao)"),function(el){if(feitos&&feitos.has(el))return;if(emRevisao(el)||escondido(el))return;if(feitos)feitos.add(el);
 var rot=el.getAttribute("data-rot")||"";guardar(el.getAttribute("data-artefacto"),rot,textoDe(el));var c=cartaoDe(el);if(c){var ja=c.querySelector(":scope > .guardaste");linha(c,(ja?ja.textContent.replace(/\.$/,"")+"; ":"Guardaste: ")+minuscula(rot)+".")}})}
// as escolhas sem certa nem errada (Decide, «Em turma»)
function abrirDepois(raiz,id){[].forEach.call((raiz.closest&&raiz.closest(".cartao")||document).querySelectorAll('[data-depois-de="'+id+'"]'),function(x){if(x.hidden)x.hidden=false})}
function marcar(pos,v){[].forEach.call(pos.querySelectorAll(".pos-op"),function(b){b.setAttribute("aria-pressed",String(!!v&&b.getAttribute("data-valor")===v))});pos.classList.toggle("escolhida",!!v)}
function verPosicoes(raiz){[].forEach.call(raiz.querySelectorAll(".posicao[data-artefacto]"),function(pos){var id=pos.getAttribute("data-artefacto");
 [].forEach.call(pos.querySelectorAll(".pos-op"),function(b){if(!b.hasAttribute("aria-pressed"))b.setAttribute("aria-pressed","false")});
 if(projecao())return;var it=valor(id);if(it){marcar(pos,it.texto);abrirDepois(pos,id);if(!emRevisao(pos)&&!pos.querySelector(":scope > .guardaste"))linha(pos,"Escolheste «"+it.texto+"». Podes mudar.")}})}
function preencher(raiz){[].forEach.call(raiz.querySelectorAll("[data-modelo]"),function(el){if(projecao()){if(!el.hidden)el.hidden=true;return}var falta=false,t=el.getAttribute("data-modelo").replace(/\{([\w-]+)\}/g,function(_,id){var it=valor(id);if(!it){falta=true;return""}return it.frase||minuscula(it.texto)});if(el.hidden!==falta)el.hidden=falta;if(!falta&&el.textContent!==t)el.textContent=t})}
function textoCopiar(chaves){var e=estado(),L=[];if(CFG.colecao)L.push(CFG.colecao);(chaves||[CFG.sessao]).forEach(function(k){var s=e.sessoes[k];if(!s||!s.itens||!s.itens.length)return;var t=s.itens.reduce(function(m,x){return Math.max(m,x.t||0)},0);L.push("");L.push((s.titulo||k)+(t?" ("+dataCurta(t)+")":""));s.itens.forEach(function(x){L.push(x.rot+": "+x.texto)})});return L.join("\n")}
function copiar(txt,nota){function ok(){nota.textContent="Copiado. Cola nas tuas notas."}function falha(){nota.textContent="Não deu para copiar aqui. Seleciona o texto da lista e copia-o."}
 try{if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(ok,function(){copiarVelho(txt)?ok():falha()});return}}catch(x){}copiarVelho(txt)?ok():falha()}
function copiarVelho(txt){var a=document.createElement("textarea");a.value=txt;a.setAttribute("readonly","");a.style.cssText="position:fixed;left:-9999px;top:0;opacity:0";document.body.appendChild(a);a.select();var r=false;try{r=document.execCommand("copy")}catch(x){}document.body.removeChild(a);return r}
function listaHTML(chaves,titulo){var e=estado(),blocos="",n=0;(chaves).forEach(function(k){var s=e.sessoes[k];if(!s||!s.itens||!s.itens.length)return;n+=s.itens.length;blocos+=(chaves.length>1?'<p class="recolha-s">'+esc(s.titulo||k)+'</p>':'')+'<ol class="recolha-itens">'+s.itens.map(function(x){return '<li><span class="r-rot">'+esc(x.rot)+'</span> <span class="r-tx">'+esc(x.texto)+'</span></li>'}).join("")+'</ol>'});
 var nome=CFG.nome||"artefactos";
 return '<p class="recolha-t">'+esc(titulo)+'</p>'+(n?blocos+'<div class="recolha-acoes"><button type="button" data-recolha-copiar>Copiar para as notas</button>'+(navigator.share?'<button type="button" data-recolha-partilhar>Partilhar</button>':'')+'</div><p class="recolha-nota" role="status" aria-live="polite"></p>':'<p class="recolha-vazia">Ainda não guardaste '+esc(nome)+' nesta sessão.</p>')+'<p class="recolha-aviso">Ficam só neste aparelho e não vão na entrega.</p>'}
function verListas(raiz){[].forEach.call(raiz.querySelectorAll("[data-recolha-lista],[data-recolha-todas]"),function(el){if(projecao()||emRevisao(el)){if(!el.hidden)el.hidden=true;if(el.innerHTML)el.innerHTML="";return}
 var todas=el.hasAttribute("data-recolha-todas"),chaves=todas?Object.keys(estado().sessoes).sort():[CFG.sessao],h=listaHTML(chaves,CFG.lista||"Os teus artefactos");
 // só se volta a desenhar quando a lista muda (cada desenho é uma mutação que o observador também vê)
 if(el.getAttribute("data-recolha-h")===String(h.length)+":"+textoCopiar(chaves).length&&el.firstChild){if(el.hidden)el.hidden=false;return}
 el.setAttribute("data-recolha-h",String(h.length)+":"+textoCopiar(chaves).length);el.classList.add("recolha");el.setAttribute("aria-label",CFG.lista||"Os teus artefactos");el.innerHTML=h;if(el.hidden)el.hidden=false;
 var bc=el.querySelector("[data-recolha-copiar]"),bp=el.querySelector("[data-recolha-partilhar]"),nota=el.querySelector(".recolha-nota");
 if(bc)bc.onclick=function(){copiar(textoCopiar(chaves),nota)};
 if(bp)bp.onclick=function(){try{navigator.share({title:CFG.lista||"",text:textoCopiar(chaves)}).catch(function(){})}catch(x){}}})}
function varrer(raiz){if(!CFG||!raiz||!raiz.querySelectorAll)return;verPosicoes(raiz);verArtefactos(raiz);preencher(raiz);verListas(raiz)}
document.addEventListener("click",function(ev){var b=ev.target&&ev.target.closest?ev.target.closest(".pos-op"):null;if(!b||!CFG||b.disabled||emRevisao(b))return;var pos=b.closest(".posicao[data-artefacto]");if(!pos)return;
 var id=pos.getAttribute("data-artefacto"),v=b.getAttribute("data-valor")||limpo(b.textContent);marcar(pos,v);abrirDepois(pos,id);
 if(projecao())return;guardar(id,pos.getAttribute("data-rot")||"",v,b.getAttribute("data-frase"));linha(pos,"Guardaste: "+minuscula(pos.getAttribute("data-rot")||"")+", «"+v+"».");
 var c=cartaoDe(pos);if(c)preencher(c)});
function ligar(o){CFG=o||{};if(!CFG.chave||!CFG.sessao){CFG=null;return}var r=CFG.raiz||document.getElementById("baralho")||document.body;varrer(r);
 // o que a própria peça muda ao varrer gera mutações: deitam-se fora no fim (takeRecords), para não voltar a varrer sem fim
 if(window.MutationObserver){var ob=new MutationObserver(function(ms){var ver=false;ms.forEach(function(m){if(m.type==="childList"&&m.addedNodes.length)ver=true;else if(m.type==="attributes")ver=true});if(ver){varrer(r);ob.takeRecords()}});ob.observe(r,{childList:true,subtree:true,attributes:true,attributeFilter:["hidden"]})}}
window.EPIRecolha={ligar:ligar,itens:itens,texto:function(chaves){return CFG?textoCopiar(chaves):""},guardar:guardar};
})();
