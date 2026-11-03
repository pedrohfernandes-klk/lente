/* 02/11/2026: o feito do Laboratório sobrevive à revisão dos cartões, sem reutilizar respostas por índice. */
(function(root){'use strict';
 function objeto(v){return v&&typeof v==='object'&&!Array.isArray(v)?v:{}}
 function data(st){st=objeto(st);var t=st.data!=null?st.data:st.t;return typeof t==='number'&&isFinite(t)&&t>=0?t:null}
 function feita(st){st=objeto(st);return st.lida===true||objeto(st.antes).lida===true}
 function migrar(estado,versao){
  var st=objeto(estado);if(st.versao===versao)return st;
  var anterior=objeto(st.antes),agora={versao:st.versao,lida:st.lida===true,data:data(st),melhor:st.melhor,total:st.totalMelhor!=null?st.totalMelhor:st.total,tentativas:st.tentativas};
  // Se uma conclusão mais antiga já estava guardada, não a substituir por uma tentativa incompleta ou posterior.
  if(anterior.lida===true&&(!agora.lida||data(agora)===null||(data(anterior)!==null&&data(anterior)<=data(agora))))agora=anterior;
  var novo={versao:versao};if(Object.keys(st).length)novo.antes=agora;return novo;
 }
 var api={migrar:migrar,feita:feita,data:function(st){st=objeto(st);var atual=st.lida===true?data(st):null,ant=objeto(st.antes).lida===true?data(st.antes):null;return atual===null?ant:ant===null?atual:Math.min(atual,ant)}};
 if(typeof module==='object'&&module.exports)module.exports=api;else root.EPILabProgresso=api;
})(typeof window==='object'?window:globalThis);
