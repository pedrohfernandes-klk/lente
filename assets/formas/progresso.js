/* Registo do Laboratório de formas: «experimentei» e «revi», neste aparelho, numa chave própria.
   Nunca guarda texto escrito pelo aluno e nunca toca nas chaves antigas (mesa de montagem e cenas do Corta!): a entrada lê-as por conta própria.
   Em projeção (?projetar=1 ou dentro do enquadramento /projetar/) não lê a primeira leitura nem grava nada. */
window.LenteProgresso=(function(){'use strict';
 var CHAVE='lente-formas-v1',SESSAO='lente-formas-textos-v1';
 var projetado=(function(){try{return window.self!==window.top||new URL(location.href).searchParams.get('projetar')==='1';}catch(x){return true;}})();
 function ler(){try{var v=JSON.parse(localStorage.getItem(CHAVE)||'null');if(v&&v.version===1&&v.itens&&typeof v.itens==='object')return v;}catch(x){}return {version:1,itens:{}};}
 function gravar(v){if(projetado)return false;try{localStorage.setItem(CHAVE,JSON.stringify(v));return true;}catch(x){return false;}}
 function item(v,id){if(!v.itens[id]||typeof v.itens[id]!=='object')v.itens[id]={};return v.itens[id];}
 function estado(id){var it=ler().itens[id]||{};return {experimentei:typeof it.experimentei==='number'?it.experimentei:0,revi:typeof it.revi==='number'?it.revi:0};}
 function marcar(id,nome){if(projetado||(nome!=='experimentei'&&nome!=='revi'))return false;var v=ler(),it=item(v,id);if(!it[nome])it[nome]=Date.now();return gravar(v);}
 function so(o){var r={};Object.keys(o||{}).forEach(function(k){if(/^[a-z]+$/.test(k)&&/^[a-z]+$/.test(String(o[k])))r[k]=String(o[k]);});return r;}
 function primeira(id,arrumacao){
  if(arrumacao===undefined){if(projetado)return null;var it=ler().itens[id];return it&&it.primeira&&it.primeira.arrumacao?{em:it.primeira.em||0,arrumacao:so(it.primeira.arrumacao),depois:so(it.depoisExplicacao)}:null;}
  if(projetado)return false;var v=ler(),i=item(v,id);i.primeira={em:Date.now(),arrumacao:so(arrumacao)};delete i.depoisExplicacao;return gravar(v);
 }
 function depois(id,mudancas){if(projetado)return false;var v=ler(),i=item(v,id);if(!i.primeira)return false;i.depoisExplicacao=so(mudancas);return gravar(v);}
 function disponivel(){try{var k='lente-formas-teste';localStorage.setItem(k,'1');localStorage.removeItem(k);return true;}catch(x){return false;}}
 /* O que se faz na página (escolhas e textos) fica só neste separador. */
 function sessao(id,valor){if(projetado)return valor===undefined?null:false;try{var t=JSON.parse(sessionStorage.getItem(SESSAO)||'{}');if(valor===undefined)return t[id]||null;if(valor===null)delete t[id];else t[id]=valor;sessionStorage.setItem(SESSAO,JSON.stringify(t));return true;}catch(x){return valor===undefined?null:false;}}
 return {CHAVE:CHAVE,SESSAO:SESSAO,projetado:projetado,estado:estado,marcar:marcar,primeira:primeira,depois:depois,disponivel:disponivel,sessao:sessao};
})();
