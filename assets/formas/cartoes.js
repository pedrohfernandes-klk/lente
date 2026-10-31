/* 30/10/2026: Laboratório simples (pedido do docente).
   Dados em certa-manha.js e cena-que-falta.js: piloto = cartões {id,tipo,p,apoio?,o?,c?,fe?,f?,valores?}.
   Os registos existentes mantêm as chaves e os campos; simples guarda apenas o estado novo do separador. */
(function(){'use strict';
/*TEXTOS*/
const TEXTOS={
 "anterior":"Cartão anterior",
 "seguinte":"Seguinte",
 "verificar":"Verificar",
 "outra":"Outra tentativa",
 "lerExplicacoes":"Ler as explicações",
 "revelar":"Revelar apoio",
 "fecharApoio":"Fechar o apoio",
 "mostrarExplicacao":"Mostrar a explicação",
 "painelRotulo":"O que a tua escolha mostra",
 "alternativa":"Outra leitura defensável:",
 "fechar":"Fechar",
 "fonteTitulo":"Fonte e créditos",
 "emPapel":"Em papel",
 "registo":{
  "nada":"Neste aparelho ainda não ficou nada registado deste percurso.",
  "exp":"Neste aparelho ficou registado: experimentei.",
  "revi":"Neste aparelho ficou registado: revi.",
  "expRevi":"Neste aparelho ficou registado: experimentei, revi.",
  "nota":"O registo diz o que fizeste, não se a tua leitura está certa.",
  "fica":"O registo fica neste aparelho.",
  "semGuardar":"Este navegador não deixa guardar. O que fizeste continua nesta página; leva-o no caderno.",
  "projecao":"Projeção: nada do que se faz aqui fica guardado.",
  "falta":{
   "certa-manha":{"exp":"Para «experimentei», compara pelo menos uma variante e verifica a arrumação no cartão «Arruma».","revi":"Para «revi», verifica a revisão no cartão «Revê», diz que informação fez diferença e, no último cartão, toca numa mudança."},
   "cena-que-falta":{"exp":"Para «experimentei», verifica dois planos diferentes e as legendas no cartão «Compara».","revi":"Para «revi», responde no cartão «Revê» e diz que plano fez mais diferença."}
  }
 },
 "recomecar":{
  "certa-manha":"Recomeçar apaga o que escreveste e arrumaste neste separador. A primeira leitura guardada neste aparelho e o registo «experimentei, revi» ficam. Queres recomeçar?",
  "cena-que-falta":"Recomeçar apaga o que escreveste e montaste neste percurso, neste separador. O registo «experimentei, revi» fica. Queres recomeçar?"
 },
 "aparelho":{
  "pergunta":"Neste aparelho há uma primeira leitura guardada a {data}. É tua?",
  "sim":"Sim, continuar com ela",
  "nao":"Não, começar do zero",
  "simFeito":"Continuas com a leitura guardada neste aparelho.",
  "naoFeito":"Começas do zero. A leitura guardada é substituída quando verificares a tua."
 },
 "primeiraVersao":"Primeira versão, conservada",
 "autoTitulo":"Verifica tu",
 "auto":["Sim","Em parte","Ainda não"],
 "autoNota":"Não é uma nota: serve para decidires o que rever.",
 "verificacaoLinha":"A verificação procura só: {lista}. O resto verificas tu.",
 "semAvisos":"A verificação não encontrou nenhuma das palavras que procura.",
 "bichosLista":"nomes de bichos ({lista}…)",
 "eco":"◐ Repara em «{palavra}»: {linha}. A regra pede o impossível dito sem espanto; se a usaste de propósito, explica no caderno porquê.",
 "x":"✗ A frase tem «{palavra}». A regra pede {regra}. Se a usaste de propósito, explica no caderno porquê.",
 "bicho":"◐ Repara em «{palavra}»: é um bicho? A regra pede uma criatura que não seja a de Kafka.",
 "afirmacaoN":"Afirmação {n} de {N}",
 "arrumadas":"{n} de {N} arrumadas.",
 "colocada":"«{curto}» em «{col}».",
 "primeiraEscolha":"1.ª escolha: {col}",
 "mudouDepois":"mudou depois da explicação",
 "guardadaAqui":"guardada aqui",
 "mudou":"mudou",
 "de":"antes: {col}",
 "mudarPara":"Mudar para:",
 "aTuaColuna":"Puseste em «{col}».",
 "corte1":"1.º corte",
 "original":"Original",
 "comVariante":"Com a {v}, escolheste «{r}».",
 "comparada":"comparada",
 "acrescentado":"acrescentado:",
 "retirado":"retirado:",
 "pauta":"A pauta: original e variante",
 "difere":"diferente da original",
 "ficouEm":"«{curto}»: ficou em «{col}».",
 "mudouDePara":"«{curto}»: de «{a}» para «{b}».",
 "escolheste":"Escolheste: {t}.",
 "semPrimeira":"Para rever, precisas da primeira leitura. Volta ao cartão «Arruma» e carrega em «Verificar».",
 "verSequencia":"Ver a sequência",
 "pausa":"Pausa",
 "continuar":"Continuar",
 "verOutra":"Ver outra vez",
 "planoAnterior":"Plano anterior",
 "planoSeguinte":"Plano seguinte",
 "seqComecou":"A sequência começou.",
 "seqAcabou":"A sequência acabou. Toca num plano da tira para o ler com a legenda.",
 "planoN":"Plano {n} de {N}: {legenda}",
 "tira":"A sequência, plano a plano",
 "experimentarOutro":"Experimentar outro plano",
 "semPlano":"Sem plano",
 "com":"Com «{p}»",
 "comMin":"com «{p}»",
 "escolhaInicial":"a tua escolha inicial",
 "verMontagem":"Ver",
 "imagemFinal":"O último plano desta montagem: a devolução.",
 "legendaEscolhida":"Legenda: {l}",
 "paraContinuar":"Para continuar",
 "voltar":"Voltar ao laboratório",
 "hipotese":"Hipótese",
 "hipoteses":"Hipóteses",
 "quadro":"Quadro",
 "aTuaArrumacao":"A tua arrumação",
 "aTuaPrimeira":"A tua primeira leitura",
 "aTuaAgora":"A tua leitura agora",
 "porArrumar":"por arrumar",
 "variantes":"Variantes",
 "aTuaResposta":"A tua resposta",
 "coluna":"Coluna",
 "planosPossiveis":"Planos possíveis",
 "planosLugar":"Planos possíveis para o lugar 04",
 "antes":"Antes",
 "agoraSr":", agora",
 "legendaEstados":"▲ ganha apoio, ▼ perde apoio, = não muda",
 "discutivel":"◐ Também se defende outra leitura: {alt}",
 "discutivelCurto":"◐ também se defende outra leitura",
 "tuMarca":"tu: {m}",
 "txt":{"corte":"Onde a frase deixa de contar uma manhã qualquer:","abertura":"A minha abertura:","primeira":"A minha primeira leitura:","agora":"A minha leitura agora:","inicial":"Hipótese inicial:","montagem":"Montagem com:","marquei":"Com «{p}», marquei:","legenda":"Legenda com «{p}»:","revisao":"Revisão:","plano":"Plano que fez mais diferença:","meio":"A frase do meio:","marcasMeio":"Com a frase do meio, marquei:"},
 "caderno":{"titulo":"Laboratório de formas: o meu caderno","nota":"Este ficheiro não tem o teu nome. Cola-o ou copia-o para o teu caderno."},
 "impressao":{"enunciado":"Enunciado","apoios":"Apoios para depois da discussão","nome":"Nome:","escreve":"Escreve aqui:","vira":"Vira a página só depois de preencheres o 4."}
};
/*FIM-TEXTOS*/
const T=TEXTOS,P=window.LenteProgresso,raizCasca=document.querySelector('[data-lf-percurso]');
if(!P||!raizCasca||!window.EPICasca)return;
const ID=raizCasca.dataset.lfPercurso,D=ID==='certa-manha'?window.LenteCertaManha:window.LenteCenaQueFalta;
if(!D||!D.piloto)return;
const K=ID==='certa-manha'?D:null,F=K?null:D,C=EPICasca.pagina(raizCasca),corpo=document.getElementById('cartoes');C.como(null);
const IMG=new URL('carteira/',document.currentScript.src).href;
const e=v=>String(v==null?'':v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const it=v=>e(v).replace(/_([^_]+)_/g,'<i>$1</i>');
const fmt=(s,o)=>String(s).replace(/\{(\w+)\}/g,(m,k)=>o&&o[k]!=null?o[k]:m);
const nomeMarca=m=>D.marcas[m]||'',titulo=p=>F.quadros[p].titulo;
const colNome=(id,quatro)=>{const c=(quatro?K.f1.colunas:K.colunas).find(c=>c.id===id);return c?c.t:id||'';};
const hTexto=id=>{const h=F.hipoteses.find(x=>x.id===id);return h?h.t:'';};
function fresco(){
 if(ID==='certa-manha')return {a1:{corte:null,primeiro:null},a2:{variante:0,respostas:{}},a3:{texto:'',primeira:null,verificado:false,apoio:false,auto:{}},
  b1:{pos:{},atual:0,verificado:false,primeira:null,em:0,depois:{},sel:null},b2:{esc:{},linha:''},b3:{texto:''},orig:{abertas:[]},
  f1:{pos:null,inicio:null,sel:null,verificado:false,revista:null,depois:{}},f2:{info:null,porque:''},f3:{toque:null},aparelho:null,revelado:{},vistos:[0],atual:0};
 return {inicial:null,escolhas:[],plano:null,marcas:{},verif:{},visor:0,f3:{l1:null,l2:null,verificado:false},f4:{resp:null,plano:null},f5:{texto:'',verificado:false,marcas:{}},revelado:{},vistos:[0],atual:0};
}

let S=Object.assign(fresco(),P.sessao(ID)||{});
if(!S.simples)S.simples={atual:0,respostas:{},planos:[],primeira:null,agora:null,consentimento:false,texto:K?S.a3.texto||'':'',versaoA:K?S.a3.primeira||null:null};
const s=S.simples,cartoes=D.piloto;
const distintas=()=>S.escolhas.filter((p,i,a)=>a.indexOf(p)===i);
function guardar(){P.sessao(ID,S);}
function atual(){return cartoes[s.atual];}
function qHtml(q){return '<h2 class="lf-q" tabindex="-1">'+e(q.p)+'</h2>';}
function opcoes(q){return '<div class="ls-opcoes">'+q.o.map((t,i)=>'<button type="button" class="lf-op" data-op="'+i+'" aria-pressed="'+(s.respostas[q.id]===i)+'">'+e(t)+'</button>').join('')+'</div>';}
function foto(id,cls){const q=F.quadros[id];return '<span class="ls-plano-texto '+(cls||'')+'">'+e(q.legenda)+'</span>';}
function sequencia(p){return '<div class="ls-tira" aria-label="Sequência montada">'+['perda','olhar','mao',p,'devolucao'].map(x=>foto(x)).join('')+'</div>';}
function primeiraTexto(v){const q=cartoes.find(q=>q.id==='primeira');return q&&q.o[q.valores.indexOf(v)]||colNome(v);}
function comparacao(){
 if(K)return '<div class="ls-compara"><p><b>Antes:</b> '+e(primeiraTexto(s.primeira))+'</p><p><b>Agora:</b> '+e((cartoes.find(q=>q.id==='revisao').o[cartoes.find(q=>q.id==='revisao').valores.indexOf(s.agora)])||'Por escolher')+'</p></div>';
 return '<p class="ls-resultado">Antes, supunhas: '+e(cartoes[0].o[cartoes[0].valores.indexOf(S.inicial)]||'')+'</p><div class="ls-par">'+s.planos.slice(-2).map(p=>'<figure>'+foto(p)+'<figcaption>'+e(F.quadros[p].titulo)+'</figcaption></figure>').join('')+'</div><p class="ls-resultado">O fim mantém-se: a carteira volta à dona.</p>';
}
function fonteHtml(){return K?'<p>'+it(K.credito.completo)+'</p><p><a href="'+e(K.credito.rtp)+'">RTP Ensina</a></p><p>'+it(K.inicio.credito)+'</p><p><a href="'+e(K.original.gutenberg)+'">Original no Projeto Gutenberg</a></p>':'<p>'+e(F.creditos)+'</p>';}
function fim(){return '<h2 class="lf-q">'+e(atual().p)+'</h2><p>'+(K?'O texto diz uma coisa; a tua leitura pode acrescentar outra. Voltar ao texto permite distinguir as duas.':'Um plano muda o que supões sobre uma cena, sem mudar o fim.')+'</p><div class="ls-opcoes"><button class="lf-op" data-imprimir>Versão em papel</button><a class="lf-op" href="?guia=1">Guia do docente e fontes</a></div><details><summary>Créditos</summary>'+fonteHtml()+'</details>';}
function corpoHtml(q){
 const n=s.respostas[q.id];
 if(q.tipo==='fim')return fim();
 if(q.tipo==='toque'){
  let frase=e(K.frase);q.o.forEach((w,i)=>{frase=frase.replace(w,'<button type="button" class="ls-palavra" data-op="'+i+'" aria-pressed="'+(n===i)+'">'+e(w)+'</button>');});
  return '<blockquote class="lf-prosa"><p>'+frase+'</p></blockquote>'+qHtml(q);
 }
 if(q.tipo==='hipotese')return '<div class="ls-par">'+foto('perda')+foto('devolucao')+'</div>'+qHtml(q)+opcoes(q);
 if(q.tipo==='planos')return qHtml(q)+'<div class="ls-planos">'+q.valores.map((p,i)=>'<button type="button" class="ls-plano" data-op="'+i+'" aria-label="'+e(q.o[i])+'" aria-pressed="'+(n===i)+'"'+(q.id==='outra'&&s.planos[0]===p?' disabled':'')+'>'+foto(p)+'<span>'+e(q.o[i])+'</span></button>').join('')+'</div>'+(n==null?'':sequencia(q.valores[n]));
 if(q.tipo==='primeira'&&!s.consentimento&&P.primeira(ID))return qHtml({p:'A leitura guardada neste aparelho é tua?'})+'<div class="ls-opcoes"><button class="lf-op" data-dono="sim">'+e(K.pilotoIdentidade.o[0])+'</button><button class="lf-op" data-dono="nao">'+e(K.pilotoIdentidade.o[1])+'</button></div>';
 if(q.tipo==='comparar')return comparacao()+qHtml(q)+opcoes(q);
 if(q.tipo==='escrita')return qHtml(q)+'<p>'+e(q.apoio)+'</p><label for="ls-texto" class="c-sr">O teu começo</label><textarea id="ls-texto" rows="4" maxlength="1500">'+e(s.texto)+'</textarea>'+(s.versaoA?'<details><summary>Primeira versão conservada</summary><p>'+e(s.versaoA)+'</p></details>':'');
 return (q.apoio?'<p class="ls-apoio">'+e(q.apoio)+'</p>':'')+qHtml(q)+opcoes(q);
}
function resposta(q,i){
 s.respostas[q.id]=i;
 if(q.tipo==='toque'){S.a1.corte=['t0','t3','t5'][i];if(!S.a1.primeiro)S.a1.primeiro=S.a1.corte;}
 if(q.id==='versao')S.a2.respostas.v2=i===0?'original':'variante';
 if(q.id==='primeira'){
  s.consentimento=true;if(!s.primeira)s.primeira=q.valores[i];S.b1.pos.sozinho=q.valores[i];S.b1.primeira=Object.assign({},S.b1.primeira||{},{sozinho:s.primeira});S.b1.verificado=true;
  if(!P.primeira(ID)||s.substituir)P.primeira(ID,S.b1.primeira);s.substituir=false;
  if(s.respostas.versao!=null)P.marcar(ID,'experimentei');
 }
 if(q.id==='revisao'){s.agora=q.valores[i];S.f1.pos=Object.assign({},S.f1.pos||{},{sozinho:s.agora});S.f1.verificado=true;}
 if(q.tipo==='hipotese')S.inicial=q.valores[i];
 if(q.tipo==='planos'){
  const p=q.valores[i];if(q.id==='outra'&&p===s.planos[0])return;
  s.planos[q.id==='montar'?0:1]=p;S.plano=p;S.escolhas=S.escolhas.filter(x=>x!==p).concat(p);S.verif[p]=true;
  if(q.id==='montar'){delete s.respostas.outra;s.planos=s.planos.slice(0,1);}
 }
 if(q.tipo==='comparar'){
  if(K){S.f2.info=['familia','original','nenhuma'][i];S.f3.toque='sozinho';P.marcar(ID,'revi');}
  else{S.f3.verificado=true;S.f4.resp=q.valores[i]===S.inicial?'mantenho':'corrijo';if(s.planos.length===2){P.marcar(ID,'experimentei');P.marcar(ID,'revi');}}
 }
 guardar();render();const escolhido=corpo.querySelector('[data-op="'+i+'"]');if(escolhido)escolhido.focus({preventScroll:true});
}
function pronto(q){return q.tipo==='fim'||q.tipo==='escrita'||s.respostas[q.id]!=null;}
function feedback(q){const i=s.respostas[q.id];if(i==null||q.tipo==='fim')return '';
 let txt=(q.fe&&q.fe[i])||q.f||'';if(F&&q.tipo==='comparar'){const h=q.valores[i];txt=s.planos.slice(-2).map(p=>F.quadros[p].titulo+': '+F.estados[p][h].razao).join(' ');}
 const efeito=q.efeitos?'<p class="ls-corte">'+e(q.efeitos[i])+'</p>':q.tipo==='escolha'||q.tipo==='primeira'||q.tipo==='contexto'?'<p class="ls-escolhida">'+e(q.o[i])+'</p>':'';
 return '<div class="lf-consequencia ls-feedback" role="status">'+efeito+'<p>'+e(txt)+'</p></div>';
}
function render(){
 const q=atual();corpo.innerHTML='<article class="cartao lf-cartao ls-cartao" data-cartao="'+q.id+'" data-tipo="'+q.tipo+'">'+corpoHtml(q)+feedback(q)+'</article>';
 corpo.querySelectorAll('[data-op]').forEach(b=>b.onclick=()=>resposta(q,+b.dataset.op));
 corpo.querySelectorAll('[data-dono]').forEach(b=>b.onclick=()=>{s.consentimento=true;const pr=P.primeira(ID);if(b.dataset.dono==='sim'&&pr&&pr.arrumacao.sozinho){S.b1.primeira=pr.arrumacao;s.primeira=pr.arrumacao.sozinho;s.respostas.primeira=q.valores.indexOf(s.primeira);}else s.substituir=true;guardar();render();});
 const ta=corpo.querySelector('textarea');if(ta)ta.oninput=()=>{s.texto=ta.value;S.a3.texto=s.texto;guardar();};
 const imp=corpo.querySelector('[data-imprimir]');if(imp)imp.onclick=()=>window.print();
 C.num(s.atual+1,cartoes.length);C.barra(cartoes.map((c,i)=>i===s.atual?'atual':s.respostas[c.id]!=null?'ok':''),s.atual,null);
 C.acoes([{t:'←',cls:'seta',esq:true,rotulo:'Cartão anterior',disabled:s.atual===0,onclick:()=>ir(s.atual-1)},s.atual===cartoes.length-1?{t:'Laboratório',cls:'prim',href:'../../'}:{t:'Seguinte',cls:'prim',attrs:{'data-seguinte':''},disabled:!pronto(q),onclick:()=>{if(q.tipo==='escrita'&&s.texto&&!s.versaoA){s.versaoA=s.texto;S.a3.primeira=s.texto;}ir(s.atual+1);}}]);
}
function ir(i){if(i<0||i>=cartoes.length)return;if(atual().tipo==='escrita'&&s.texto&&!s.versaoA){s.versaoA=s.texto;S.a3.primeira=s.texto;}s.atual=i;guardar();C.folha.fechar();render();C.rolarTopo();}
document.addEventListener('keydown',ev=>{if(ev.target.closest('textarea,input,[data-c-painel]'))return;if(ev.key==='ArrowRight'&&pronto(atual())){ev.preventDefault();ir(s.atual+1);}if(ev.key==='ArrowLeft'){ev.preventDefault();ir(s.atual-1);}});

const impressao=document.createElement('div');impressao.className='lf-print';impressao.id='lf-print';document.body.appendChild(impressao);
const linhas=n=>'<div class="lf-lines" style="height:'+(n*9)+'mm"></div>';
const so=(modo,h,tag)=>'<'+(tag||'div')+' class="lf-p-'+modo+'">'+h+'</'+(tag||'div')+'>';
function impressaoHtml(){
 let h='<h1>'+e(D.titulo)+'</h1><p>'+e(T.impressao.nome)+' ______________________ '+so('enunciado',e(T.impressao.enunciado),'span')+so('apoios',e(T.impressao.apoios),'span')+'</p>',en='',ap='';
 if(ID==='certa-manha'){
  h+='<blockquote class="lf-prosa"><p>'+e(K.frase)+'</p></blockquote><p class="lf-pc">'+it(K.credito.completo)+'</p>';
  en+='<section><h2>1. '+e(K.a1.pergunta)+'</h2><p>'+K.segmentos.map(s=>'[ ] '+e(s.t)).join(' &nbsp; ')+'</p><p>'+e(K.a1.antes)+'</p>'+linhas(2)+'</section>';
  en+='<section><h2>2. '+e(K.a2.pergunta)+'</h2><ol>'+K.a2.variantes.map(v=>'<li>'+e(v.texto)+' &nbsp; [ ] '+K.a2.respostas.map(r=>e(r.t)).join(' [ ] ')+'</li>').join('')+'</ol><p>'+e(K.a2.nota)+'</p></section>';
  en+='<section><h2>3. '+e(K.a3.pergunta)+'</h2><p>'+e(K.a3.regra)+'</p>'+linhas(3)+'</section>';
  en+='<section><h2>4. '+e(K.b1.pergunta)+'</h2><table><thead><tr><th></th>'+K.colunas.map(c=>'<th>'+e(c.t)+'</th>').join('')+'</tr></thead><tbody>'+K.afirmacoes.map(a=>'<tr><td>'+e(a.t)+'</td><td>□</td><td>□</td><td>□</td></tr>').join('')+'</tbody></table><p class="lf-vira">'+e(T.impressao.vira)+'</p></section>';
  en+='<section class="lf-quebra"><h2>5. '+e(K.original.pergunta)+'</h2><p>'+e(K.original.antes)+' '+K.original.expressoes.map(x=>'<i lang="de">'+e(x.t)+'</i>'+e(x.depois)).join(' ')+'</p><ul>'+K.original.expressoes.map(x=>'<li><i lang="de">'+e(x.t)+'</i>: '+e(x.g)+'</li>').join('')+'</ul><ol>'+K.inicio.passagens.map(p=>'<li>'+e(p.par)+'. '+e(p.t)+'</li>').join('')+'</ol></section>';
  en+='<section><h2>6. '+e(K.f1.pergunta)+'</h2><table><thead><tr><th></th>'+K.f1.colunas.map(c=>'<th>'+e(c.t)+'</th>').join('')+'</tr></thead><tbody>'+K.afirmacoes.map(a=>'<tr><td>'+e(a.t)+'</td><td>□</td><td>□</td><td>□</td><td>□</td></tr>').join('')+'</tbody></table><p>'+e(K.f2.pergunta)+'</p>'+linhas(4)+'</section>';
  ap+='<section><h2>'+e(K.a1.rotulo)+'</h2><ul>'+K.segmentos.map(s=>{const q=K.a1.toques[s.id];return '<li><b>'+e(q.titulo)+'</b> '+e(q.corpo)+(q.alternativa?' '+e(T.alternativa)+' '+e(q.alternativa):'')+'</li>';}).join('')+'</ul></section>';
  ap+='<section><h2>'+e(K.a2.rotulo)+'</h2>'+K.a2.variantes.map(v=>'<p><b>'+e(v.nome)+'</b></p><ul>'+K.a2.respostas.map(r=>'<li>'+e(r.t)+': '+e(v.explica[r.id])+'</li>').join('')+'</ul>').join('')+'</section>';
  ap+='<section><h2>'+e(K.b1.rotulo)+'</h2>'+K.afirmacoes.map(a=>'<p><b>'+e(a.t)+'</b></p><ul>'+K.colunas.map(c=>'<li>'+e(c.t)+': '+e(a.b1[c.id].marca)+' '+e(nomeMarca(a.b1[c.id].marca))+'. '+e(a.b1[c.id].t)+'</li>').join('')+'</ul>').join('')+'</section>';
  ap+='<section><h2>'+e(K.f1.rotulo)+'</h2>'+K.afirmacoes.map(a=>'<p><b>'+e(a.t)+'</b></p><ul>'+K.f1.colunas.map(c=>'<li>'+e(c.t)+': '+e(a.f[c.id].marca)+' '+e(nomeMarca(a.f[c.id].marca))+'. '+e(a.f[c.id].t)+'</li>').join('')+'</ul>').join('')+'</section>';
 }else{
  const fig=id=>{const q=F.quadros[id];return '<figure>'+'<div class="ls-plano-texto">'+e(q.legenda)+'</div>'+'<figcaption>'+e(q.n+' '+q.titulo+'. '+q.legenda)+'</figcaption></figure>';};
  h+='<section><h2>'+e(F.abre.texto)+'</h2><div class="lf-pgrelha">'+F.tira.map(fig).join('')+'</div><h2>'+e(T.planosLugar)+'</h2><div class="lf-pgrelha">'+F.candidatos.map(fig).join('')+'</div></section>';
  en+='<section><h2>'+e(F.ve.pergunta)+'</h2><table><thead><tr><th>'+e(T.hipotese)+'</th><th>'+e(T.antes)+'</th>'+F.candidatos.map(p=>'<th>'+e(titulo(p))+'</th>').join('')+'</tr></thead><tbody>'+F.hipoteses.map(h1=>'<tr><td>'+e(h1.t)+'</td><td>□</td><td></td><td></td><td></td></tr>').join('')+'</tbody></table><p>'+e(T.legendaEstados)+'</p></section>';
  en+='<section><h2>'+e(F.compara.pergunta)+'</h2>'+linhas(3)+'<h2>'+e(F.escreve.pergunta)+'</h2><ol><li>'+e(F.escreve.frases[0])+'</li><li>______________________</li><li>'+e(F.escreve.frases[2])+'</li></ol><p>'+e(F.escreve.regra)+'</p></section>';
  ap+='<section><h2>'+e(F.quadroTitulo)+'</h2><table><thead><tr><th>'+e(T.hipotese)+'</th>'+F.candidatos.map(p=>'<th>'+e(titulo(p))+'</th>').join('')+'</tr></thead><tbody>'+F.hipoteses.map(h1=>'<tr><td>'+e(h1.t)+'</td>'+F.candidatos.map(p=>{const s=F.estados[p][h1.id];return '<td>'+e(F.estadosSimbolos[s.estado]+' '+F.estadosNomes[s.estado])+'. '+e(s.razao)+'</td>';}).join('')+'</tr>').join('')+'</tbody></table><p>'+e(F.quadroNota)+'</p></section>';
  ap+='<section>'+F.candidatos.map(p=>'<p><b>'+e(F.explicacao[p].titulo)+'</b> '+e(F.explicacao[p].corpo)+'</p>').join('')+'</section>';
 }
 return h+so('enunciado',en)+so('apoios',ap);}

function guiaExtra(){
 if(K)return '<section><h2>Procurar informação</h2><p>'+e(K.b2.pergunta)+'</p>'+K.b2.afirmacoes.map(id=>'<h3>'+e(K.afirmacoes.find(a=>a.id===id).t)+'</h3><ul>'+K.b2.tipos.map(t=>'<li><b>'+e(t.t)+':</b> '+e(K.b2.explica[id][t.id].t)+'</li>').join('')+'</ul>').join('')+'</section><section><h2>Escrever e rever</h2><p>'+e(K.b3.molde)+'</p><p>'+e(K.f2.pergunta)+'</p><ul>'+K.f2.explica.map(x=>'<li>'+e(x.t)+'</li>').join('')+'</ul><h3>Uma abertura tua</h3><p>'+e(K.a3.modelo)+' '+e(K.a3.modeloFonte)+'</p><ul>'+K.a3.autoverificacao.map(t=>'<li>'+e(t)+'</li>').join('')+'</ul></section>';
 return '<section><h2>Comparar outras hipóteses</h2>'+Object.values(F.pares).map(p=>'<p>'+e(p.sintese)+'</p>').join('')+'<h2>Escrever uma cena</h2><p>'+e(F.escreve.marcar)+'</p><ul>'+F.escreve.hipoteses.map(t=>'<li>'+e(t)+'</li>').join('')+'</ul><p>Compara a tua leitura com a de um colega e explica que gesto visível apoia cada hipótese.</p></section>';
}
const guia=new URL(location.href).searchParams.get('guia')==='1';
if(guia){document.body.classList.add('lf-guia');raizCasca.hidden=true;impressao.innerHTML='<p><a href="'+location.pathname+'">Voltar à experiência</a></p><h1>Guia do docente</h1><p>Propostas de aprofundamento, fontes e explicações. O percurso curto mantém uma escolha por cartão.</p>'+impressaoHtml()+guiaExtra()+fonteHtml();}
else{impressao.innerHTML='<h1>'+e(D.titulo)+'</h1>'+cartoes.filter(q=>q.tipo!=='fim').map(q=>'<section><h2>'+e(q.p)+'</h2>'+(q.apoio?'<p>'+e(q.apoio)+'</p>':'')+(q.tipo==='toque'?'<p>'+e(K.frase)+'</p>':'')+(q.tipo==='hipotese'?foto('perda')+foto('devolucao'):'')+(q.tipo==='planos'?'<div class="ls-par">'+q.valores.map(p=>foto(p)).join('')+'</div>':'')+(q.o?'<ul>'+q.o.map(o=>'<li>□ '+e(o)+'</li>').join('')+'</ul>':linhas(4))+'</section>').join('')+fonteHtml();}
function cadernoTexto(){return [D.titulo,K?K.frase:'',...cartoes.filter(q=>q.o&&s.respostas[q.id]!=null).map(q=>q.p+'\n'+q.o[s.respostas[q.id]]),s.versaoA?'Primeira versão: '+s.versaoA:'',s.texto?'Versão atual: '+s.texto:'',F&&S.f5.texto?'Escrita anterior: '+S.f5.texto:''].filter(Boolean).join('\n\n');}
function levarCaderno(){C.menu.fechar();const url=URL.createObjectURL(new Blob([cadernoTexto()],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='lente-'+ID+'.txt';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),2000);}

raizCasca.querySelectorAll('[data-lf-menu]').forEach(b=>b.onclick=()=>{const a=b.dataset.lfMenu;if(a==='caderno')levarCaderno();if(a==='recomecar'){if(confirm('Recomeçar neste separador? A leitura inicial guardada no aparelho mantém-se.')){delete S.simples;P.sessao(ID,S);location.reload();}}});
window.LenteCartoes={ir,estado:()=>JSON.parse(JSON.stringify(S))};
if(s.atual>=cartoes.length)s.atual=0;
if(!guia)render();
})();
