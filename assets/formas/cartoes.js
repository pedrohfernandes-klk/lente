/* Laboratório de formas: condutor dos cartões curtos («Certa manhã» e «A cena que falta»).
   Usa a casca das lições (EPICasca) sem o motor de perguntas: não há «Certo/Errado», pontos nem opções sorteadas.
   Cada cartão: uma pergunta, um gesto, uma consequência visível no material, uma explicação daquela escolha, outra tentativa.
   Os conteúdos estão nos ficheiros de dados (certa-manha.js, cena-que-falta.js); os textos da interface, em TEXTOS. */
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
const T=TEXTOS,P=window.LenteProgresso,raizCasca=document.querySelector('[data-casca]');
if(!raizCasca||!window.EPICasca||!P)return;
const ID=raizCasca.getAttribute('data-lf-percurso'),D=ID==='certa-manha'?window.LenteCertaManha:window.LenteCenaQueFalta;
if(!D)return;
const SCRIPT=document.currentScript,IMG=new URL('carteira/',SCRIPT?SCRIPT.src:location.href).href;
const e=v=>String(v==null?'':v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const it=v=>e(v).replace(/(^|[^0-9A-Za-zÀ-ÿ_])_([^_<>]{1,120}?)_(?![0-9A-Za-zÀ-ÿ_])/g,'$1<i>$2</i>');
const fmt=(s,o)=>String(s).replace(/\{(\w+)\}/g,(m,k)=>o&&o[k]!=null?o[k]:m);
const semPonto=s=>String(s).replace(/[.!?]$/,'');
const reduz=(()=>{try{return matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(x){return false;}})();
const C=EPICasca.pagina(raizCasca);C.como(null);
const corpo=document.getElementById('cartoes');
document.body.classList.toggle('lf-projetar',P.projetado);
const nomeMarca=m=>D.marcas?D.marcas[m]:'';

/* ── estado: só neste separador (sessionStorage), nunca em projeção ── */
function fresco(){
 if(ID==='certa-manha')return {a1:{corte:null,primeiro:null},a2:{variante:0,respostas:{}},a3:{texto:'',primeira:null,verificado:false,apoio:false,auto:{}},
  b1:{pos:{},atual:0,verificado:false,primeira:null,em:0,depois:{},sel:null},b2:{esc:{},linha:''},b3:{texto:''},orig:{abertas:[]},
  f1:{pos:null,inicio:null,sel:null,verificado:false,revista:null,depois:{}},f2:{info:null,porque:''},f3:{toque:null},aparelho:null,revelado:{},vistos:[0],atual:0};
 return {inicial:null,escolhas:[],plano:null,marcas:{},verif:{},visor:0,f3:{l1:null,l2:null,verificado:false},f4:{resp:null,plano:null},f5:{texto:'',verificado:false,marcas:{}},revelado:{},vistos:[0],atual:0};
}
let S=fresco();
(function(){const g=P.sessao(ID);if(g&&typeof g==='object'){const f=fresco();Object.keys(f).forEach(k=>{if(g[k]!==undefined)S[k]=g[k];});}})();
function guardar(){P.sessao(ID,S);}

/* ── registo «experimentei / revi» (regras por percurso) ── */
function regras(){
 if(ID==='certa-manha'){
  if(Object.keys(S.a2.respostas).length>=1&&S.b1.verificado)P.marcar(ID,'experimentei');
  if(S.b1.primeira&&S.f2.info&&S.f3.toque)P.marcar(ID,'revi');
 }else{
  if(distintas().length>=2&&S.f3.verificado)P.marcar(ID,'experimentei');
  if(S.inicial&&S.f4.resp&&S.f4.plano)P.marcar(ID,'revi');
 }
}
function linhaRegisto(){const r=P.estado(ID);if(P.projetado)return T.registo.projecao;return r.experimentei&&r.revi?T.registo.expRevi:r.experimentei?T.registo.exp:r.revi?T.registo.revi:T.registo.nada;}

/* ── painel de explicação (a casca), com segundo botão, véu em projeção e descrição para leitores de ecrã ── */
const folhaEl=raizCasca.querySelector('[data-c-folha]');
function painel(o){
 const velar=P.projetado&&!o.semVeu;
 if(folhaEl)folhaEl.setAttribute('aria-live','off');
 const corpoHtml=(o.html||'')+(o.alternativa?'<p class="lf-alt"><b>'+e(T.alternativa)+'</b> '+e(o.alternativa)+'</p>':'')+(o.apoio?'<button type="button" class="lf-apoio" data-apoio-p aria-expanded="false">'+e(T.revelar)+'</button><div class="lf-apoio-c" hidden>'+o.apoio+'</div>':'');
 const html=velar?'<button type="button" class="revelar lf-revelar">'+e(T.mostrarExplicacao)+'</button><div class="lf-velado" hidden><p class="lf-painel-titulo">'+e(o.titulo)+'</p>'+corpoHtml+'</div>':corpoHtml;
 const prim=o.botoes.find(b=>b.prim)||o.botoes[0];
 C.folha.abrir({estado:'lf',titulo:velar?'':o.titulo,html:(o.rotulo===false?'':'<p class="lf-painel-rot">'+e(o.rotulo||T.painelRotulo)+'</p>')+html,botao:{t:e(prim.t),vai:!!prim.vai,onclick:prim.onclick,attrs:prim.attrs},focar:false});
 if(!folhaEl)return;
 const s=folhaEl.querySelector('.c-s');if(s){s.textContent=velar?'':(o.simbolo||'');}
 const ver=folhaEl.querySelector('.c-veredito');if(ver){ver.id='lf-painel-t';if(o.simbolo&&!velar)ver.insertAdjacentHTML('beforeend','<span class="c-sr">'+e(o.palavra||'')+'</span>');if(!o.titulo||velar)ver.hidden=true;}
 const ex=folhaEl.querySelector('.c-expl');if(ex)ex.id='lf-painel-c';
 const pb=folhaEl.querySelector('.c-folha-in>.c-prim');
 const linha=document.createElement('div');linha.className='lf-painel-botoes';
 if(pb){pb.parentNode.insertBefore(linha,pb);o.botoes.filter(b=>b!==prim).forEach(b=>{const x=document.createElement('button');x.type='button';x.className='c-sec';x.textContent=b.t;x.onclick=b.onclick;linha.appendChild(x);});linha.appendChild(pb);pb.setAttribute('aria-describedby','lf-painel-t lf-painel-c');}
 const ap=folhaEl.querySelector('[data-apoio-p]');if(ap)ap.onclick=()=>{const c=ap.nextElementSibling,abre=c.hidden;c.hidden=!abre;ap.setAttribute('aria-expanded',String(abre));ap.textContent=abre?T.fecharApoio:T.revelar;};
 const rv=folhaEl.querySelector('.lf-revelar');if(rv)rv.onclick=()=>{const v=folhaEl.querySelector('.lf-velado');if(v)v.hidden=false;rv.hidden=true;S.revelado[cartaoAtual().id]=true;guardar();refazer();if(pb)pb.focus({preventScroll:true});};
 (pb||folhaEl).focus({preventScroll:true});
 mostrarConsequencia();
}
/* no telemóvel, o painel sobe por cima do cartão: a consequência da escolha tem de ficar à vista por cima dele */
function mostrarConsequencia(){
 if(!C.corpo||!folhaEl)return;
 const alvo=[...corpo.querySelectorAll('.lf-consequencia')].filter(x=>x.children.length).pop()||corpo.querySelector('[aria-pressed="true"]');
 if(!alvo)return;
 requestAnimationFrame(()=>{const sobre=getComputedStyle(folhaEl).position==='absolute',fr=folhaEl.getBoundingClientRect(),ar=alvo.getBoundingClientRect(),cr=C.corpo.getBoundingClientRect(),limite=sobre?fr.top:cr.bottom,falta=ar.bottom-limite+8,folga=ar.top-cr.top-8;if(falta>0)C.corpo.scrollTop+=Math.max(0,Math.min(falta,folga));});
}
function fecharPainel(){C.folha.fechar();}

/* ── peças comuns ── */
function rotulo(r,extra){return '<p class="rot lf-rot"><span>'+e(r)+'</span>'+(extra||[]).filter(Boolean).map(x=>'<span class="lf-mrc">'+e(x)+'</span>').join('')+'</p>';}
function pergunta(q){return '<h2 class="q lf-q" tabindex="-1">'+e(q)+'</h2>';}
function marcaHtml(m){return m?'<span class="lf-marca-j" data-m="'+e(m)+'"><span aria-hidden="true">'+e(m)+'</span> '+e(nomeMarca(m))+'</span>':'';}
function veu(id){return P.projetado&&!S.revelado[id];}
function botaoVeu(){return '<button type="button" class="revelar" data-lf-revelar>'+e(T.mostrarExplicacao)+'</button>';}
function hora(ts){const d=new Date(ts);return String(d.getHours()).padStart(2,'0')+'h'+String(d.getMinutes()).padStart(2,'0');}
function data(ts){const d=new Date(ts);return String(d.getDate()).padStart(2,'0')+'/'+String(d.getMonth()+1).padStart(2,'0')+'/'+d.getFullYear()+', às '+hora(ts);}

/* ═══════════════ CERTA MANHÃ ═══════════════ */
const K=ID==='certa-manha'?D:null;
const colNome=(id,quatro)=>{const l=quatro?K.f1.colunas:K.colunas;const c=l.find(x=>x.id===id);return c?c.t:'';};
const afirm=id=>K.afirmacoes.find(a=>a.id===id);
function fraseHtml(){return '<blockquote class="lf-prosa"><span class="lf-par" aria-hidden="true">1</span><p>'+e(K.frase)+'</p></blockquote>';}
function creditoCurto(){return '<p class="lf-credito">'+it(K.credito.curto)+' <a href="'+e(K.credito.rtp)+'" target="_blank" rel="noopener">'+e(K.credito.verRtp)+'</a></p>';}
function b1Atual(){return S.b1.verificado?Object.assign({},S.b1.primeira,S.b1.depois):Object.assign({},S.b1.pos);}
function quadro(pos,o){
 o=o||{};const cols=o.quatro?K.f1.colunas:K.colunas;
 return '<div class="lf-quadro'+(o.quatro?' lf-q4':'')+'" role="group" aria-label="'+e(o.rotulo||T.quadro)+'">'+cols.map(c=>{
  const tags=K.afirmacoes.filter(a=>pos[a.id]===c.id).map(a=>{
   const m=o.marcas?o.marcas(a):null,extra=o.extra?o.extra(a):'';
   return '<li><button type="button" class="lf-tag'+(o.sel===a.id?' lf-sel':'')+'" data-tag="'+a.id+'" aria-pressed="'+(o.sel===a.id)+'"'+(o.inerte?' disabled':'')+'><span class="lf-tag-t">'+e(a.curto)+'</span>'+(m?marcaHtml(m):'')+extra+'</button></li>';}).join('');
  const fantasmas=o.fantasma?K.afirmacoes.filter(a=>o.fantasma[a.id]===c.id&&pos[a.id]!==c.id).map(a=>'<li class="lf-fantasma" aria-hidden="true">'+e(a.curto)+' <small>'+e(T.guardadaAqui)+'</small></li>').join(''):'';
  return '<section class="lf-col" data-col="'+c.id+'"><h3>'+e(c.t)+'</h3><ul>'+tags+fantasmas+'</ul></section>';}).join('')+'</div>';
}
function textoQuadro(pos,quatro){return '<table class="c-sr"><caption>'+e(T.quadro)+'</caption><tbody>'+K.afirmacoes.map(a=>'<tr><th scope="row">'+e(a.t)+'</th><td>'+e(pos[a.id]?colNome(pos[a.id],quatro):T.porArrumar)+'</td></tr>').join('')+'</tbody></table>';}

const cartoesK=[
 {id:'abre',tipo:'ler',html(){
   const pr=S.b1.verificado?null:primeiraValida();
   const perg=pr&&!S.aparelho?'<div class="lf-aparelho" role="group" aria-labelledby="lf-ap-t"><p id="lf-ap-t">'+e(fmt(T.aparelho.pergunta,{data:data(pr.em)}))+'</p><div class="lf-linha-botoes"><button type="button" class="lf-op" data-aparelho="sim">'+e(T.aparelho.sim)+'</button><button type="button" class="lf-op" data-aparelho="nao">'+e(T.aparelho.nao)+'</button></div></div>':S.aparelho?'<p class="lf-estado" role="status">'+e(S.aparelho==='sim'?T.aparelho.simFeito:T.aparelho.naoFeito)+'</p>':'';
   return rotulo(K.abre.rotulo,[K.abre.meta])+'<h2 class="lf-n1" tabindex="-1">'+e(K.titulo)+'</h2>'+fraseHtml()+creditoCurto()+'<p class="lf-ler">'+e(K.abre.texto)+'</p><p class="lf-papel"><span class="lf-mrc">'+e(T.emPapel)+'</span> '+e(K.abre.papel)+'</p>'+perg;},
  ligar(r){r.querySelectorAll('[data-aparelho]').forEach(b=>b.onclick=()=>{S.aparelho=b.dataset.aparelho;if(S.aparelho==='sim'){const pr=primeiraValida();if(pr){S.b1.pos=Object.assign({},pr.arrumacao);S.b1.primeira=Object.assign({},pr.arrumacao);S.b1.depois=Object.assign({},pr.depois);S.b1.verificado=true;S.b1.em=pr.em;S.b1.atual=null;}}guardar();refazer('.lf-estado');});},
  pronto:()=>true},

 {id:'a1',tipo:'segmentos',html(){
   const a=K.a1,c=S.a1.corte,ci=c?K.segmentos.findIndex(s=>s.id===c):-1;
   const p1=S.a1.primeiro,ant=id=>p1===id&&p1!==c;
   const segs=K.segmentos.map((s,i)=>'<button type="button" class="lf-seg'+(ci>=0&&i>ci?' lf-esbatido':'')+(ci===i?' lf-cortado':'')+(ant(s.id)?' lf-corte-ant':'')+'" data-seg="'+s.id+'" aria-pressed="'+(c===s.id)+'">'+(ci===i?'<span class="lf-tesoura" aria-hidden="true"></span>':'')+e(s.t)+(ant(s.id)?'<small class="lf-c1">'+e(T.corte1)+'</small>':'')+'</button>').join(' ');
   let cons='';
   if(c){const tq=a.toques[c];cons=tq.semFim?'<p class="lf-final">'+e(tq.semFim)+'</p>':'<p class="lf-antes">'+e(a.antes)+'</p><p class="lf-final">'+e(K.segmentos.slice(0,ci+1).map(s=>s.t).join(' '))+'<em class="lf-inventado">'+e(tq.fim)+'</em></p><p class="lf-nota-p">'+e(a.nota)+'</p>';}
   return rotulo(a.rotulo,[a.tempo])+pergunta(a.pergunta)+'<p class="dica">'+e(a.dica)+'</p><p class="lf-prosa lf-toques" data-composto>'+segs+'</p><div class="lf-consequencia" aria-live="polite">'+cons+'</div>';},
  ligar(r){r.querySelectorAll('[data-seg]').forEach(b=>b.onclick=()=>{const id=b.dataset.seg;if(!S.a1.primeiro)S.a1.primeiro=id;S.a1.corte=id;guardar();refazer('[data-seg="'+id+'"]');const tq=K.a1.toques[id];
   painel({titulo:tq.titulo,html:'<p>'+e(tq.corpo)+'</p>',alternativa:tq.alternativa,botoes:[{t:T.outra,onclick:()=>{fecharPainel();foco('[data-seg="'+id+'"]');}},{t:T.seguinte,prim:true,vai:true,onclick:seguinte}]});});},
  pronto:()=>!!S.a1.corte},

 {id:'a2',tipo:'variantes',html(){
   const a=K.a2,v=a.variantes[S.a2.variante],resp=S.a2.respostas[v.id];
   const partes=v.partes.map(p=>p.t!=null?e(p.t):p.mais!=null?'<ins><span class="c-sr">'+e(T.acrescentado)+'</span>'+e(p.mais)+'</ins>':'<del'+(/^[.,;:!?]$/.test(p.menos)?' class="lf-pont"':'')+'><span class="c-sr">'+e(T.retirado)+'</span>'+e(p.menos)+'</del>').join('');
   const tabs='<div class="lf-tabs" role="group" aria-label="'+e(T.variantes)+'" data-composto>'+a.variantes.map((x,i)=>'<button type="button" data-var="'+i+'" aria-pressed="'+(i===S.a2.variante)+'">'+e(x.nome)+(S.a2.respostas[x.id]?' <small>✓ '+e(T.comparada)+'</small>':'')+'</button>').join('')+'</div>';
   const pauta=resp?pautaHtml(v):'';
   return rotulo(a.rotulo,[a.marca])+pergunta(a.pergunta)+'<p class="lf-etq">'+e(T.original)+'</p><blockquote class="lf-prosa lf-pequena"><p>'+e(K.frase)+'</p></blockquote>'+tabs+'<p class="lf-etq">'+e(v.nome)+'</p><blockquote class="lf-prosa lf-pequena lf-variante"><p>'+partes+'</p></blockquote><p class="lf-nota-p">'+e(a.nota)+'</p><div class="lf-linha-botoes lf-respostas" role="group" aria-label="'+e(T.aTuaResposta)+'">'+a.respostas.map(x=>'<button type="button" class="lf-op" data-resp="'+x.id+'" aria-pressed="'+(resp===x.id)+'">'+e(x.t)+'</button>').join('')+'</div><div class="lf-consequencia" aria-live="polite">'+pauta+'</div>';},
  ligar(r){
   r.querySelectorAll('[data-var]').forEach(b=>b.onclick=()=>{S.a2.variante=+b.dataset.var;guardar();refazer('[data-var="'+b.dataset.var+'"]');});
   r.querySelectorAll('[data-resp]').forEach(b=>b.onclick=()=>{const a=K.a2,v=a.variantes[S.a2.variante],rid=b.dataset.resp;S.a2.respostas[v.id]=rid;guardar();regras();refazer('[data-resp="'+rid+'"]');
    const n=Object.keys(S.a2.respostas).length,rt=a.respostas.find(x=>x.id===rid).t.toLowerCase();
    painel({titulo:fmt(T.comVariante,{v:v.nome.toLowerCase(),r:rt}),html:'<p>'+e(v.explica[rid])+'</p>'+(n>=2?'<p class="lf-fecho">'+e(v.fecho||a.fecho||'')+'</p>':''),botoes:[{t:T.outra,onclick:()=>{fecharPainel();const prox=a.variantes.findIndex(x=>!S.a2.respostas[x.id]);if(prox>=0)S.a2.variante=prox;guardar();refazer('[data-var="'+S.a2.variante+'"]');}},{t:T.seguinte,prim:true,vai:true,onclick:seguinte}]});});},
  pronto:()=>Object.keys(S.a2.respostas).length>0},

 {id:'a3',tipo:'escrever',opcional:true,html(){
   const a=K.a3,st=S.a3;
   const apoio='<button type="button" class="lf-apoio" data-apoio aria-expanded="'+st.apoio+'">'+e(st.apoio?T.fecharApoio:T.revelar)+'</button><div class="lf-apoio-c"'+(st.apoio?'':' hidden')+'><p class="lf-modelo">'+e(a.modelo)+' <small>'+e(a.modeloFonte)+'</small></p><ul class="lf-sementes">'+a.sementes.map(s=>'<li>'+e(s)+'</li>').join('')+'</ul></div>';
   const prim=st.primeira!==null?'<section class="lf-first lf-personal"><h3>'+e(T.primeiraVersao)+'</h3><p class="lf-manuscript">'+e(st.primeira)+'</p></section>':'';
   let cons='';
   if(st.verificado){const av=avisosA3(st.texto);cons=(av.length?'<ul class="lf-avisos">'+av.map(x=>'<li class="'+(x.x?'lf-x':'lf-meio')+'">'+e(x.t)+'</li>').join('')+'</ul>':'<p>'+e(T.semAvisos)+'</p>')+'<p class="lf-nota-p">'+e(fmt(T.verificacaoLinha,{lista:listaA3()}))+'</p>'+autoHtml(a.autoverificacao,'a3')+'<button type="button" class="lf-op" data-outra>'+e(T.outra)+'</button>';}
   return rotulo(a.rotulo,[a.marca,T.emPapel])+pergunta(a.pergunta)+'<p class="lf-regra">'+e(a.regra)+'</p>'+apoio+prim+'<div class="lf-personal"><label class="lf-label" for="a3-texto">'+e(a.legenda)+'</label><textarea id="a3-texto" rows="4" maxlength="1200">'+e(st.texto)+'</textarea></div><div class="lf-consequencia" aria-live="polite">'+cons+'</div>';},
  ligar(r){const st=S.a3;
   const ap=r.querySelector('[data-apoio]');ap.onclick=()=>{st.apoio=!st.apoio;guardar();refazer('[data-apoio]');};
   const ta=r.querySelector('#a3-texto');ta.oninput=()=>{st.texto=ta.value;st.verificado=false;guardar();acoes();};
   const ou=r.querySelector('[data-outra]');if(ou)ou.onclick=()=>{if(st.texto.trim()&&st.primeira===null)st.primeira=st.texto;st.texto='';st.verificado=false;st.auto={};guardar();refazer('#a3-texto');};
   ligarAuto(r,'a3');},
  verificar:{pronto:()=>!!S.a3.texto.trim(),fazer(){const st=S.a3;if(st.primeira===null&&st.texto.trim())st.primeira=st.texto;st.verificado=true;guardar();refazer('.lf-consequencia');}},
  pronto:()=>true},

 {id:'b1',tipo:'arrumar',html(){
   const b=K.b1,st=S.b1,pos=st.verificado?Object.assign({},st.primeira,st.depois):st.pos,n=Object.keys(pos).length;
   let topo='';
   if(!st.verificado){
    const idx=st.atual==null?-1:st.atual,a=idx>=0?K.afirmacoes[idx]:null;
    topo=a?'<div class="lf-afirmacao" aria-describedby="lf-atalhos"><p class="lf-etq">'+e(fmt(T.afirmacaoN,{n:idx+1,N:K.afirmacoes.length}))+'</p><p class="lf-afirma-t">'+e(a.t)+'</p><div class="lf-linha-botoes lf-cols-botoes" role="group" aria-label="'+e(T.coluna)+'">'+K.colunas.map((c,i)=>'<button type="button" class="lf-op" data-colocar="'+c.id+'" aria-pressed="'+(pos[a.id]===c.id)+'"><kbd>'+(i+1)+'</kbd> '+e(c.t)+'</button>').join('')+'</div><p class="c-sr" id="lf-atalhos">'+e(b.atalhos)+'</p></div>':'<p class="lf-estado">'+e(fmt(T.arrumadas,{n:K.afirmacoes.length,N:K.afirmacoes.length}))+'</p>';
   }
   const marcas=st.verificado&&!veu('b1')?(a=>a.b1[pos[a.id]].marca):null;
   const extra=st.verificado?(a=>st.depois&&st.depois[a.id]?'<small class="lf-mudou">'+e(T.mudouDepois)+'</small>':''):null;
   let zona='';
   if(st.verificado&&st.sel){const a=afirm(st.sel),c=pos[a.id],x=a.b1[c],pr=st.primeira[a.id];
    zona=veu('b1')?botaoVeu():'<div class="lf-explica"><p class="lf-afirma-t">'+e(a.t)+'</p><p>'+e(fmt(T.aTuaColuna,{col:colNome(c)}))+' '+marcaHtml(x.marca)+'</p><p>'+e(x.t)+'</p>'+(pr!==c?'<p class="lf-nota-p">'+e(fmt(T.primeiraEscolha,{col:colNome(pr)}))+'</p>':'')+'<p class="lf-etq">'+e(T.mudarPara)+'</p><div class="lf-linha-botoes">'+K.colunas.filter(k=>k.id!==c).map(k=>'<button type="button" class="lf-op" data-mover="'+k.id+'">'+e(k.t)+(k.id===pr?' <small>('+e(fmt(T.primeiraEscolha,{col:''}).replace(/:\s*$/,''))+')</small>':'')+'</button>').join('')+'</div></div>';}
   return rotulo(b.rotulo,[b.tempo])+pergunta(b.pergunta)+'<blockquote class="lf-prosa lf-pequena"><p>'+e(K.frase)+'</p></blockquote>'+topo+quadro(pos,{sel:st.sel,marcas,extra,rotulo:T.aTuaArrumacao})+textoQuadro(pos)+(st.verificado?'':'<p class="lf-nota-p">'+e(b.aviso)+'</p><p class="c-sr" role="status" id="lf-b1-st">'+e(fmt(T.arrumadas,{n,N:K.afirmacoes.length}))+'</p>')+'<div class="lf-consequencia" aria-live="polite">'+zona+'</div>';},
  ligar(r){const st=S.b1;
   r.querySelectorAll('[data-colocar]').forEach(b=>b.onclick=()=>colocarB1(b.dataset.colocar));
   r.querySelectorAll('[data-tag]').forEach(b=>b.onclick=()=>{const id=b.dataset.tag;if(!st.verificado){st.atual=K.afirmacoes.findIndex(a=>a.id===id);guardar();refazer('[data-colocar]');return;}st.sel=id;guardar();refazer('.lf-explica [data-mover],[data-lf-revelar]');});
   r.querySelectorAll('[data-mover]').forEach(b=>b.onclick=()=>{const id=st.sel,c=b.dataset.mover;if(c===st.primeira[id])delete st.depois[id];else st.depois[id]=c;P.depois(ID,st.depois);guardar();refazer('[data-tag="'+id+'"]');});
   const rv=r.querySelector('[data-lf-revelar]');if(rv)rv.onclick=()=>{S.revelado.b1=true;guardar();refazer('.lf-explica');};},
  teclas(k){if(S.b1.verificado||S.b1.atual==null)return false;const c=K.colunas[+k-1];if(!c)return false;colocarB1(c.id);return true;},
  verificar:{pronto:()=>K.afirmacoes.every(a=>S.b1.pos[a.id]),fazer(){const st=S.b1;st.verificado=true;st.primeira=Object.assign({},st.pos);st.depois={};st.em=Date.now();st.sel=null;P.primeira(ID,st.primeira);guardar();regras();refazer();
   painel({titulo:K.b1.titulo,html:'<p>'+e(K.b1.corpo)+'</p>',botoes:[{t:T.lerExplicacoes,onclick:()=>{fecharPainel();foco('[data-tag]');}},{t:T.seguinte,prim:true,vai:true,onclick:seguinte}]});}},
  pronto:()=>S.b1.verificado},

 {id:'b2',tipo:'faltava',html(){
   const b=K.b2;
   return rotulo(b.rotulo)+pergunta(b.pergunta)+'<ol class="lf-faltava">'+b.afirmacoes.map(id=>{const a=afirm(id),esc=S.b2.esc[id],x=esc?b.explica[id][esc]:null;
    return '<li><p class="lf-afirma-t">'+e(a.t)+'</p><div class="lf-linha-botoes" role="group" aria-label="'+e(a.curto)+'">'+b.tipos.map(t=>'<button type="button" class="lf-op" data-falta="'+id+'" data-tipo="'+t.id+'" aria-pressed="'+(esc===t.id)+'">'+e(t.t)+'</button>').join('')+'</div><div class="lf-consequencia" aria-live="polite">'+(x?(veu('b2')?botaoVeu():'<p><span class="lf-marca-j lf-marca-fonte">'+e(K.marcasFonte[x.marca])+'</span> '+e(x.t)+'</p>'):'')+'</div></li>';}).join('')+'</ol><div class="lf-personal"><label class="lf-label" for="b2-linha">'+e(b.linha)+'</label><input id="b2-linha" type="text" maxlength="300" value="'+e(S.b2.linha)+'"></div>';},
  ligar(r){r.querySelectorAll('[data-falta]').forEach(b=>b.onclick=()=>{S.b2.esc[b.dataset.falta]=b.dataset.tipo;guardar();refazer('[data-falta="'+b.dataset.falta+'"][data-tipo="'+b.dataset.tipo+'"]');});
   const l=r.querySelector('#b2-linha');l.oninput=()=>{S.b2.linha=l.value;guardar();};
   r.querySelectorAll('[data-lf-revelar]').forEach(x=>x.onclick=()=>{S.revelado.b2=true;guardar();refazer();});},
  pronto:()=>true},

 {id:'b3',tipo:'guardar',opcional:true,html(){
   const b=K.b3,st=S.b1;
   if(!st.verificado)return rotulo(b.rotulo,[b.marca])+pergunta(b.pergunta)+'<p class="lf-estado">'+e(b.semLeitura)+'</p>';
   return rotulo(b.rotulo,[b.marca])+pergunta(b.pergunta)+'<p class="lf-carimbo">'+e(P.projetado?b.carimboProjecao:fmt(b.carimbo,{hora:hora(st.em||Date.now())}))+'</p>'+quadro(st.primeira,{inerte:true,rotulo:T.aTuaPrimeira})+textoQuadro(st.primeira)+'<div class="lf-personal"><label class="lf-label" for="b3-texto">'+e(b.molde)+'</label><textarea id="b3-texto" rows="3" maxlength="800">'+e(S.b3.texto)+'</textarea></div>';},
  ligar(r){const ta=r.querySelector('#b3-texto');if(ta)ta.oninput=()=>{S.b3.texto=ta.value;guardar();};},
  pronto:()=>true},

 {id:'original',tipo:'glosas',html(){
   const o=K.original,ab=S.orig.abertas;
   const frase=e(o.antes)+o.expressoes.map(x=>' <button type="button" class="lf-glosavel" lang="de" data-glosa="'+x.id+'" aria-expanded="'+ab.includes(x.id)+'">'+e(x.t)+'</button>'+e(x.depois)).join('');
   const glosas=o.expressoes.filter(x=>ab.includes(x.id)).map(x=>'<li><b lang="de">'+e(x.t)+'</b> '+e(x.g)+'</li>').join('');
   return rotulo(o.rotulo,[o.tempo])+pergunta(o.pergunta)+'<p class="lf-prosa lf-relato" data-composto>'+frase+'</p><div class="lf-consequencia" aria-live="polite">'+(glosas?'<ul class="lf-glosas">'+glosas+'</ul>':'')+'</div><p class="lf-credito">'+it(o.credito)+' <a href="'+e(o.gutenberg)+'" target="_blank" rel="noopener">'+e(o.verGutenberg)+'</a></p>';},
  ligar(r){r.querySelectorAll('[data-glosa]').forEach(b=>b.onclick=()=>{const id=b.dataset.glosa,ab=S.orig.abertas;S.orig.abertas=ab.includes(id)?ab.filter(x=>x!==id):ab.concat(id);guardar();refazer('[data-glosa="'+id+'"]');});},
  pronto:()=>true},

 {id:'inicio',tipo:'ler',html(){const o=K.inicio;return rotulo(o.rotulo)+pergunta(o.pergunta)+'<ol class="lf-passagens">'+o.passagens.map(p=>'<li><span class="lf-par">'+e(p.par)+'</span><p>'+e(p.t)+'</p></li>').join('')+'</ol><p class="lf-credito">'+e(o.credito)+'</p>';},pronto:()=>true},

 {id:'f1',tipo:'rever',entrar(){if(!S.b1.verificado||S.f1.verificado)return;const sem=!S.f1.pos||JSON.stringify(S.f1.pos)===JSON.stringify(S.f1.inicio);if(sem){S.f1.pos=b1Atual();S.f1.inicio=Object.assign({},S.f1.pos);guardar();}},html(){
   const f=K.f1;if(!S.b1.verificado)return rotulo(f.rotulo)+pergunta(f.pergunta)+'<p class="lf-estado">'+e(T.semPrimeira)+'</p>';
   const st=S.f1,pr=S.b1.primeira,dep=st.depois||{},N=K.afirmacoes.length,n=K.afirmacoes.filter(a=>st.pos[a.id]!==pr[a.id]).length,expl=st.verificado&&!veu('f1');
   const marcas=expl?(a=>a.f[st.pos[a.id]].marca):null;
   const extra=a=>(st.pos[a.id]!==pr[a.id]?'<small class="lf-mudou">'+e(T.mudou)+', '+e(fmt(T.de,{col:colNome(pr[a.id],true)}))+'</small>':'')+(st.verificado&&dep[a.id]?'<small class="lf-mudou">'+e(T.mudouDepois)+'</small>':'');
   let zona='';
   if(st.sel){const a=afirm(st.sel),c=st.pos[a.id],x=a.f[c];
    zona='<div class="lf-explica"><p class="lf-afirma-t">'+e(a.t)+'</p><div class="lf-linha-botoes lf-cols-botoes" role="group" aria-label="'+e(T.coluna)+'" aria-describedby="lf-atalhos4">'+f.colunas.map((k,i)=>'<button type="button" class="lf-op" data-mover4="'+k.id+'" aria-pressed="'+(k.id===c)+'"><kbd>'+(i+1)+'</kbd> '+e(k.t)+'</button>').join('')+'</div><p class="c-sr" id="lf-atalhos4">'+e(f.atalhos)+'</p>'+(!st.verificado?'':veu('f1')?botaoVeu():'<p>'+marcaHtml(x.marca)+' '+e(x.t)+'</p>')+'</div>';}
   return rotulo(f.rotulo)+pergunta(f.pergunta)+'<p class="lf-nota-p">'+e(f.nota)+'</p>'+quadro(st.pos,{quatro:true,sel:st.sel,marcas,extra,fantasma:pr,rotulo:T.aTuaAgora})+textoQuadro(st.pos,true)+'<p class="lf-estado" role="status">'+e(n?fmt(f.contador,{n,N}):f.nenhuma)+'</p><div class="lf-consequencia" aria-live="polite">'+zona+'</div>';},
  ligar(r){const st=S.f1;
   r.querySelectorAll('[data-tag]').forEach(b=>b.onclick=()=>{st.sel=b.dataset.tag;guardar();refazer('[data-mover4][aria-pressed="true"]');});
   r.querySelectorAll('[data-mover4]').forEach(b=>b.onclick=()=>moverF1(b.dataset.mover4));
   const rv=r.querySelector('[data-lf-revelar]');if(rv)rv.onclick=()=>{S.revelado.f1=true;guardar();refazer();};},
  teclas(k){if(!S.f1.sel)return false;const c=K.f1.colunas[+k-1];if(!c)return false;moverF1(c.id);return true;},
  verificar:{pronto:()=>S.b1.verificado&&!!S.f1.pos,fazer(){const st=S.f1;st.verificado=true;st.revista=Object.assign({},st.pos);st.depois={};st.sel=null;guardar();regras();refazer();
   painel({titulo:K.f1.titulo,html:'<p>'+e(K.f1.corpo)+'</p>',botoes:[{t:T.lerExplicacoes,onclick:()=>{fecharPainel();foco('[data-tag]');}},{t:T.seguinte,prim:true,vai:true,onclick:seguinte}]});}},
  pronto:()=>!S.b1.verificado||S.f1.verificado},

 {id:'f2',tipo:'perguntas',html(){
   const f=K.f2;if(!S.b1.verificado||!S.f1.verificado)return rotulo(f.rotulo)+pergunta(f.pergunta)+'<p class="lf-estado">'+e(T.semPrimeira)+'</p>';
   const pr=S.b1.primeira,ag=S.f1.pos,man=K.afirmacoes.filter(a=>ag[a.id]===pr[a.id]),cor=K.afirmacoes.filter(a=>ag[a.id]!==pr[a.id]);
   return rotulo(f.rotulo)+pergunta(f.pergunta)+'<div class="lf-duas"><section><h3 class="lf-etq">'+e(f.mantens)+'</h3><ul class="lf-lista">'+(man.map(a=>'<li>'+e(a.curto)+': '+e(colNome(ag[a.id],true))+'</li>').join('')||'<li>…</li>')+'</ul></section><section><h3 class="lf-etq">'+e(f.corriges)+'</h3><ul class="lf-lista">'+(cor.map(a=>'<li>'+e(a.curto)+': '+e(colNome(pr[a.id],true))+' <span aria-hidden="true">→</span><span class="c-sr">'+e(T.agoraSr)+'</span> '+e(colNome(ag[a.id],true))+'</li>').join('')||'<li>'+e(f.nenhumaCorrigida)+'</li>')+'</ul>'+(cor.length?'<div class="lf-personal"><label class="lf-label" for="f2-porque">'+e(f.porque)+'</label><input id="f2-porque" type="text" maxlength="300" value="'+e(S.f2.porque)+'"></div>':'')+'</section></div><h3 class="lf-etq">'+e(f.informacao)+'</h3><div class="lf-linha-botoes lf-info" role="group" aria-label="'+e(f.informacao)+'">'+f.escolhas.map(x=>'<button type="button" class="lf-op" data-info="'+x.id+'" aria-pressed="'+(S.f2.info===x.id)+'">'+e(x.t)+(x.de?' <small'+(/^[a-z]/.test(x.de)?' lang="de"':'')+'>'+e(x.de)+'</small>':'')+'</button>').join('')+'</div>';},
  ligar(r){const p=r.querySelector('#f2-porque');if(p)p.oninput=()=>{S.f2.porque=p.value;guardar();};
   r.querySelectorAll('[data-info]').forEach(b=>b.onclick=()=>{const id=b.dataset.info;S.f2.info=id;guardar();regras();refazer('[data-info="'+id+'"]');const x=K.f2.escolhas.find(y=>y.id===id);
    const tt=x.t.split(':')[0];painel({titulo:fmt(T.escolheste,{t:tt.charAt(0).toLowerCase()+tt.slice(1)}),html:'<p>'+e(explicaF2(id))+'</p>',botoes:[{t:T.outra,onclick:()=>{fecharPainel();foco('[data-info="'+id+'"]');}},{t:T.seguinte,prim:true,vai:true,onclick:seguinte}]});});},
  pronto:()=>!!S.f2.info},

 {id:'f3',tipo:'lado',html(){
   const f=K.f3;if(!S.b1.verificado||!S.f1.verificado)return rotulo(f.rotulo)+pergunta(f.pergunta)+'<p class="lf-estado">'+e(T.semPrimeira)+'</p>';
   const pr=S.b1.primeira,ag=S.f1.pos,mud=K.afirmacoes.filter(a=>ag[a.id]!==pr[a.id]),todas=!mud.length;
   const col=(qual,pos)=>'<section class="lf-lado-col"><h3 class="lf-etq">'+e(qual)+'</h3><ul>'+K.afirmacoes.map(a=>'<li>'+(qual===f.agora&&(todas||pos[a.id]!==pr[a.id])?'<button type="button" class="lf-tag lf-tag-l" data-lado="'+a.id+'" aria-pressed="'+(S.f3.toque===a.id)+'">':'<span class="lf-tag lf-tag-l lf-inerte">')+'<span class="lf-tag-t">'+e(a.curto)+'</span> <small>'+e(colNome(pos[a.id],true))+'</small>'+(qual===f.agora&&pos[a.id]!==pr[a.id]?'<small class="lf-mudou">'+e(S.f1.depois&&S.f1.depois[a.id]?T.mudouDepois:f.mudou)+'</small>':'')+(qual===f.agora&&(todas||pos[a.id]!==pr[a.id])?'</button>':'</span>')+'</li>').join('')+'</ul></section>';
   const textos=S.b3.texto?'<p class="lf-manuscript lf-personal">'+e(S.b3.texto)+'</p>':'';
   return rotulo(f.rotulo)+pergunta(todas?f.perguntaSem:f.pergunta)+'<div class="lf-duas lf-lado">'+col(f.primeira,pr)+col(f.agora,ag)+'</div>'+textos;},
  ligar(r){r.querySelectorAll('[data-lado]').forEach(b=>b.onclick=()=>{const id=b.dataset.lado;S.f3.toque=id;guardar();regras();refazer('[data-lado="'+id+'"]');
   const a=afirm(id),pr=S.b1.primeira[id],ag=S.f1.pos[id];
   painel({titulo:pr===ag?fmt(T.ficouEm,{curto:a.curto,col:colNome(ag,true)}):fmt(T.mudouDePara,{curto:a.curto,a:colNome(pr,true),b:colNome(ag,true)}),html:'<p>'+e(explicaF3(id))+'</p>',botoes:[{t:T.outra,onclick:()=>{fecharPainel();foco('[data-lado="'+id+'"]');}},{t:T.seguinte,prim:true,vai:true,onclick:seguinte}]});});},
  pronto:()=>!!S.f3.toque||!S.b1.verificado},

 {id:'fim',tipo:'fim',html(){return fimHtml(K.fim);},pronto:()=>true}
];
function colocarB1(col){const st=S.b1,a=K.afirmacoes[st.atual];if(!a)return;st.pos[a.id]=col;const prox=K.afirmacoes.findIndex(x=>!st.pos[x.id]);st.atual=prox>=0?prox:null;guardar();refazer(st.atual==null?null:'[data-colocar]');const s=document.getElementById('lf-b1-st');if(s)s.textContent=fmt(T.colocada,{curto:a.curto,col:colNome(col)})+' '+fmt(T.arrumadas,{n:Object.keys(st.pos).length,N:K.afirmacoes.length});if(st.atual==null){const v=C.acao('[data-lf-verificar]');if(v)v.focus();}}
/* uma primeira leitura guardada só se oferece se tiver todas as afirmações, em colunas que existem (tech P8) */
function primeiraValida(){const pr=P.primeira(ID);if(!pr)return null;const cols=K.colunas.map(c=>c.id),ids=K.afirmacoes.map(a=>a.id),arr=pr.arrumacao||{};
 if(!ids.every(i=>cols.includes(arr[i]))||!Object.keys(arr).every(k=>ids.includes(k)))return null;
 const dep={};Object.keys(pr.depois||{}).forEach(k=>{if(ids.includes(k)&&cols.includes(pr.depois[k]))dep[k]=pr.depois[k];});return {em:pr.em,arrumacao:arr,depois:dep};}
function moverF1(col){const st=S.f1;if(!st.sel)return;st.pos[st.sel]=col;if(st.verificado){st.depois=st.depois||{};if(col===st.revista[st.sel])delete st.depois[st.sel];else st.depois[st.sel]=col;}guardar();refazer('[data-mover4][aria-pressed="true"]');}
const plural=n=>n===1?'1 afirmação':n+' afirmações';
function explicaF2(id){const mov=K.afirmacoes.filter(a=>S.f1.pos[a.id]!==S.f1.inicio[a.id]).map(a=>a.id);
 if(id==='nenhuma'){const cor=K.afirmacoes.filter(a=>S.f1.pos[a.id]!==S.b1.primeira[a.id]).length;if(mov.length)return fmt(K.f2.nenhumaMudou,{n:plural(mov.length)});if(cor)return K.f2.nenhumaArruma;}
 const l=K.f2.explica.find(x=>x.escolha===id&&(!x.se||mov.includes(x.se.split(':')[1])));return l?l.t:'';}
/* G2: o que se manteve lê-se contra o que se leu; a origem de cada mudança fica dita (informação nova, explicação do «Arruma» ou do «Revê») */
function explicaF3(id){const a=afirm(id),L=K.f3.lado,pr=S.b1.primeira[id],ag=S.f1.pos[id],ini=S.f1.inicio[id],x=a.f[ag];
 if(pr===ag){if(x.marca==='●')return L.firme+' '+x.t;if(x.marca==='◐')return x.t;return fmt(L.contraria,{curto:a.curto,col:colNome(ag,true)})+' '+x.t+' '+L.contrariaFim;}
 if(S.f1.depois&&S.f1.depois[id])return L.depoisRevisao+' '+x.t;
 if(ag===ini&&ini!==pr)return L.depoisExplicacao;
 if(['corpo','cama','repulsa','manha','dormiu'].includes(id))return x.t;return L[id]||x.t;}
/* A3: só procura palavras; a lista do que procura fica à vista (C6) */
function avisosA3(txt){const a=K.a3,l=[],low=txt.toLowerCase(),pal=low.match(/[a-zà-ÿ]+/g)||[];
 a.proibidas.forEach(p=>{if(p.raiz){const w=pal.find(x=>x.startsWith(p.raiz));if(w)l.push({x:true,t:fmt(T.x,{palavra:w,regra:p.regra})});}else if(low.includes(p.p))l.push({x:true,t:fmt(T.x,{palavra:p.p,regra:p.regra})});});
 (a.ecos||[]).forEach(g=>{const vistos=[];pal.forEach(w=>{if(!vistos.includes(w)&&(g.palavras.includes(w)||g.raizes.some(r=>w.startsWith(r)))){vistos.push(w);l.push({x:false,t:fmt(T.eco,{palavra:w,linha:g.linha})});}});});
 a.bichos.forEach(b=>{if(pal.includes(b))l.push({x:false,t:fmt(T.bicho,{palavra:b})});});return l;}
function listaA3(){const a=K.a3,q=w=>'«'+w+'»';return a.proibidas.map(p=>q(p.mostra||p.p)).concat(...(a.ecos||[]).map(g=>g.mostra.map(q))).concat(fmt(T.bichosLista,{lista:a.bichos.filter((b,i)=>i%2===0).slice(0,6).join(', ')})).join(', ');}
function pautaHtml(v){const a=K.a2,lin=['acontece','espanto'];
 return '<table class="lf-pauta"><caption>'+e(T.pauta)+'</caption><thead><tr><td></td>'+a.colunas.map(c=>'<th scope="col">'+e(c)+'</th>').join('')+'</tr></thead>'+lin.map((k,i)=>'<tbody><tr class="lf-pauta-l"><th colspan="4" scope="rowgroup">'+e(a.linhas[i])+'</th></tr><tr><th scope="row">'+e(T.original)+'</th>'+a.original[k].map(x=>'<td>'+e(x)+'</td>').join('')+'</tr><tr><th scope="row">'+e(v.nome)+'</th>'+v.pauta[k].map((x,j)=>x!==a.original[k][j]?'<td class="lf-difere"><b>'+e(x)+'</b><span class="c-sr"> ('+e(T.difere)+')</span></td>':'<td>'+e(x)+'</td>').join('')+'</tr></tbody>').join('')+'</table>';}

/* ═══════════════ A CENA QUE FALTA ═══════════════ */
const F=ID==='cena-que-falta'?D:null;
const titulo=p=>F.quadros[p].titulo,distintas=()=>{const v=[];S.escolhas.filter(p=>S.verif&&S.verif[p]).forEach(p=>{const i=v.indexOf(p);if(i>=0)v.splice(i,1);v.push(p);});return v;};
const tiraAtual=()=>F.tira.map(id=>id==='lacuna'&&S.plano?S.plano:id);
const hTexto=id=>{const h=F.hipoteses.find(x=>x.id===id);return h?h.t:'';};
function quadroArte(id,o){o=o||{};const q=F.quadros[id];
 if(q.img)return '<img class="lf-arte" src="'+e(IMG+q.img+'.webp')+'" alt="'+(o.semAlt?'':e(q.legenda))+'" width="600" height="600">';
 if(q.intertitulo)return '<span class="lf-arte lf-intertitulo"'+(o.semAlt?' aria-hidden="true"':' role="img" aria-label="'+e(q.titulo+'. '+q.legenda)+'"')+'><span>'+e(o.mini?q.titulo:q.legenda)+'</span></span>';
 return '<span class="lf-arte lf-lacuna"'+(o.semAlt?' aria-hidden="true"':' role="img" aria-label="'+e(q.legenda)+'"')+'><span>?</span></span>';}
function tiraHtml(o){o=o||{};const t=o.tira||tiraAtual();return '<ol class="lf-tira" aria-label="'+e(T.tira)+'" data-composto>'+t.map((id,i)=>{const q=F.quadros[id],novo=i===3&&id!=='lacuna';return '<li><button type="button" class="lf-mini'+(o.visor===i?' lf-sel':'')+(novo?' lf-novo':'')+'" data-mini="'+i+'"'+(o.inerte?' tabindex="-1"':'')+' aria-label="'+e(q.n+' '+q.titulo+(novo?', '+F.escolhe.novo:''))+'">'+quadroArte(id,{semAlt:true,mini:true})+'<span class="lf-claquete" aria-hidden="true">'+e(q.n)+'</span></button></li>';}).join('')+'</ol>';}
function visorHtml(){const t=tiraAtual(),i=Math.min(S.visor||0,t.length-1),id=t[i],q=F.quadros[id];
 return '<figure class="lf-visor" data-visor>'+quadroArte(id)+'<figcaption><span class="lf-claquete">'+e(q.n)+'</span> <b>'+e(q.titulo)+'</b> <span class="lf-leg">'+e(q.legenda)+'</span></figcaption></figure><div class="lf-leitor" role="group" aria-label="'+e(T.tira)+'"><button type="button" class="lf-op" data-passo="-1"'+(i===0?' disabled':'')+'>← '+e(T.planoAnterior)+'</button>'+(reduz?'':'<button type="button" class="lf-op" data-seq>'+e(T.verSequencia)+'</button>')+'<button type="button" class="lf-op" data-passo="1"'+(i===t.length-1?' disabled':'')+'>'+e(T.planoSeguinte)+' →</button></div><p class="c-sr" aria-live="polite" data-anuncio></p>';}
function estadoDe(p,h){return p?F.estados[p][h]:{estado:'aberto',razao:F.abertoLinha};}
function linhaH(h,st,o){o=o||{};return '<span class="lf-est" data-estado="'+st.estado+'"><span aria-hidden="true">'+e(F.estadosSimbolos[st.estado])+'</span> '+e(F.estadosNomes[st.estado])+'</span>'+(o.razao!==false?'<small class="lf-razao">'+e(st.razao)+(st.discutivel?' <span class="lf-disc">'+e(T.discutivelCurto)+'</span>':'')+'</small>':'')+(o.tu?'<small class="lf-tu">'+e(fmt(T.tuMarca,{m:F.estadosSimbolos[o.tu]+' '+F.estadosNomes[o.tu]}))+'</small>':'');}
function quadroH(p,o){o=o||{};const ant=o.anterior,tu=o.tu||{};return '<section class="lf-hips"><h3 class="lf-etq">'+e(F.quadroTitulo)+'</h3><ul>'+F.hipoteses.map(h=>{const st=estadoDe(p,h.id),mud=ant!==undefined&&estadoDe(ant,h.id).estado!==st.estado;return '<li class="lf-h'+(mud?' lf-mudou-h':'')+(S.inicial===h.id?' lf-inicial':'')+'" data-h="'+h.id+'"><p class="lf-h-t">'+e(h.t)+(S.inicial===h.id?' <small>('+e(T.escolhaInicial)+')</small>':'')+'</p>'+linhaH(h.id,st,{tu:tu[h.id]})+(mud?'<small class="lf-mudou">'+e(T.mudou)+'</small>':'')+'</li>';}).join('')+'</ul><p class="lf-nota-p">'+e(F.quadroNota)+'</p></section>';}
function marcarH(p){const x=F.escolhe,hI=S.inicial&&S.inicial!=='nenhuma'?S.inicial:null,m=S.marcas[p]||{};
 return '<section class="lf-hips lf-marcar-h"><h3 class="lf-etq">'+e(F.quadroTitulo)+'</h3><p class="lf-instr">'+e(fmt(hI?x.marcarH:x.marcarSem,{plano:titulo(p)}))+'</p><ul>'+F.hipoteses.map(h=>'<li class="lf-h'+(S.inicial===h.id?' lf-inicial':'')+'" data-h="'+h.id+'"><p class="lf-h-t" id="mh-'+h.id+'">'+e(h.t)+(S.inicial===h.id?' <small>('+e(T.escolhaInicial)+')</small>':'')+'</p><span class="lf-linha-botoes" role="group" aria-labelledby="mh-'+h.id+'">'+['ganha','perde','igual'].map(s=>'<button type="button" class="lf-op lf-mini-op" data-marcah="'+h.id+'" data-s="'+s+'" aria-pressed="'+(m[h.id]===s)+'" aria-label="'+e(F.estadosNomes[s])+'"><span aria-hidden="true">'+e(F.estadosSimbolos[s])+' '+e(F.estadosCurtos[s])+'</span></button>').join('')+'</span></li>').join('')+'</ul></section>';}
function quadroComp(ps){return '<table class="lf-comp"><caption>'+e(F.quadroTitulo)+'</caption><thead><tr><th scope="col">'+e(T.hipotese)+'</th><th scope="col">'+e(T.semPlano)+'</th>'+ps.map(p=>'<th scope="col">'+e(fmt(T.com,{p:titulo(p)}))+'</th>').join('')+'</tr></thead><tbody>'+F.hipoteses.map(h=>'<tr><th scope="row"><button type="button" class="lf-hbtn" data-hpar="'+h.id+'">'+e(h.t)+'</button></th><td>'+linhaH(h.id,estadoDe(null,h.id),{razao:false})+'</td>'+ps.map(p=>'<td>'+linhaH(h.id,estadoDe(p,h.id),{razao:false})+'</td>').join('')+'</tr>').join('')+'</tbody></table><p class="lf-nota-p">'+e(F.quadroNota)+'</p>';}
function parDe(a,b){return F.pares[a+'+'+b]||F.pares[b+'+'+a];}
function textoPar(a,b,h){const par=parDe(a,b);if(par&&par[h])return par[h];return fmt(F.igual,{estado:F.estadosNomes[estadoDe(a,h).estado]});}

const cartoesF=[
 {id:'abre',tipo:'ler',html(){const a=F.abre;return rotulo(a.rotulo,[a.meta])+'<h2 class="lf-n1" tabindex="-1">'+e(F.titulo)+'</h2>'+tiraHtml({tira:F.tira,inerte:true})+'<p class="lf-ler">'+e(a.texto)+'</p><p class="lf-nota-p">'+e(a.nota)+'</p><p class="lf-papel"><span class="lf-mrc">'+e(T.emPapel)+'</span> '+e(a.papel)+'</p>';},ligar(r){r.querySelectorAll('[data-mini]').forEach(b=>b.disabled=true);},pronto:()=>true},

 {id:'ve',tipo:'ve',html(){const v=F.ve;return rotulo(v.rotulo)+pergunta(v.pergunta)+'<div class="lf-ve-grade"><div>'+visorHtml()+tiraHtml({visor:S.visor})+'</div><div><ul class="lf-escolha-h" role="group" aria-label="'+e(T.hipoteses)+'">'+F.hipoteses.map(h=>'<li><button type="button" class="lf-op lf-op-h" data-inicial="'+h.id+'" aria-pressed="'+(S.inicial===h.id)+'"><span>'+e(h.t)+'</span>'+linhaH(h.id,estadoDe(null,h.id),{razao:false})+(S.inicial===h.id?'<small class="lf-escolhida">'+e(T.escolhaInicial)+'</small>':'')+'</button></li>').join('')+'<li><button type="button" class="lf-op lf-op-h" data-inicial="nenhuma" aria-pressed="'+(S.inicial==='nenhuma')+'"><span>'+e(F.nenhuma)+'</span>'+(S.inicial==='nenhuma'?'<small class="lf-escolhida">'+e(T.escolhaInicial)+'</small>':'')+'</button></li></ul><p class="lf-nota-p">'+e(F.abertoLinha)+'</p></div></div>';},
  ligar(r){ligarVisor(r);r.querySelectorAll('[data-inicial]').forEach(b=>b.onclick=()=>{S.inicial=b.dataset.inicial;guardar();refazer('[data-inicial="'+S.inicial+'"]');});},
  pronto:()=>!!S.inicial},

 {id:'escolhe',tipo:'montagem',html(){const x=F.escolhe,hI=S.inicial&&S.inicial!=='nenhuma'?hTexto(S.inicial):null,p=S.plano,ver=!!(p&&S.verif[p]),nd=distintas().filter(y=>y!==p).length+(ver?1:0);
   const q=nd>=1?(hI?fmt(x.perguntaOutra,{H:semPonto(hI)}):x.perguntaOutraSem):(hI?fmt(x.perguntaH,{H:semPonto(hI)}):x.pergunta);
   const dv=distintas(),ant=dv.filter(y=>y!==p).pop();
   const cands='<ul class="lf-candidatos'+(p?' lf-recolhidos':'')+'" role="group" aria-label="'+e(T.planosPossiveis)+'">'+F.candidatos.map(c=>{const qd=F.quadros[c];return '<li><button type="button" class="lf-cand" data-cand="'+c+'" aria-pressed="'+(p===c)+'">'+quadroArte(c,{semAlt:true,mini:true})+'<span class="lf-cand-t"><b>'+e(qd.titulo)+'</b>'+(p===c?' <small class="lf-escolhida">'+e(x.noMeio)+'</small>':'')+'<span class="lf-leg">'+e(qd.legenda)+'</span></span></button></li>';}).join('')+'</ul>';
   const cons=!p?quadroH(null):!ver?marcarH(p):quadroH(p,{anterior:ant,tu:S.marcas[p]});
   return rotulo(x.rotulo)+pergunta(q)+'<div class="lf-ve-grade"><div>'+tiraHtml({visor:S.visor})+cands+visorHtml()+'</div><div class="lf-consequencia" aria-live="polite">'+cons+'</div></div>';},
  ligar(r){ligarVisor(r);r.querySelectorAll('[data-cand]').forEach(b=>b.onclick=()=>escolherPlano(b.dataset.cand));
   r.querySelectorAll('[data-marcah]').forEach(b=>b.onclick=()=>{const p=S.plano;if(!p)return;S.marcas[p]=Object.assign({},S.marcas[p],{[b.dataset.marcah]:b.dataset.s});guardar();refazer('[data-marcah="'+b.dataset.marcah+'"][data-s="'+b.dataset.s+'"]');});},
  verificar:{pronto:()=>{const p=S.plano;if(!p||S.verif[p])return false;const m=S.marcas[p]||{},hI=S.inicial&&S.inicial!=='nenhuma'?S.inicial:null;return hI?!!m[hI]:Object.keys(m).length>0;},fazer(){verificarPlano();}},
  pronto:()=>!!S.plano&&!!S.verif[S.plano]},

 {id:'compara',tipo:'comparar',html(){const x=F.compara,d=distintas();
   if(d.length<2)return rotulo(x.rotulo)+pergunta(x.pergunta)+'<p class="lf-estado">'+e(x.precisa)+'</p><button type="button" class="lf-op" data-voltar-escolhe>'+e(T.experimentarOutro)+'</button>';
   const p1=d[d.length-2],p2=d[d.length-1];
   const coluna=(p,k)=>{const tira=F.tira.map(id=>id==='lacuna'?p:id),esc=S.f3[k];return '<section class="lf-monta"><h3 class="lf-etq">'+e(fmt(T.com,{p:titulo(p)}))+'</h3>'+tiraHtml({tira,inerte:true})+'<figure class="lf-final-img">'+quadroArte('devolucao',{semAlt:true})+'<figcaption>'+(esc?'<b>'+e(fmt(T.legendaEscolhida,{l:F.legendasFim.find(l=>l.id===esc).t}))+'</b>':'<span class="c-sr">'+e(T.imagemFinal)+'</span>')+'</figcaption></figure><div class="lf-legendas" role="group" aria-label="'+e(fmt(T.com,{p:titulo(p)}))+'">'+F.legendasFim.map(l=>'<button type="button" class="lf-op" data-leg="'+k+'" data-l="'+l.id+'" aria-pressed="'+(esc===l.id)+'">'+e(l.t)+'</button>').join('')+'</div></section>';};
   return rotulo(x.rotulo)+pergunta(x.pergunta)+'<p class="lf-nota-p">'+e(x.ultimas)+(d.length>2?' '+e(fmt(x.foraTres,{p:titulo(d[d.length-3])})):'')+'</p><div class="lf-duas lf-montagens">'+coluna(p1,'l1')+coluna(p2,'l2')+'</div><div class="lf-consequencia" aria-live="polite">'+quadroComp([p1,p2])+(S.f3.hpar?'<p class="lf-par-texto">'+e(textoPar(p1,p2,S.f3.hpar))+'</p>':'')+'</div>';},
  ligar(r){const vb=r.querySelector('[data-voltar-escolhe]');if(vb)vb.onclick=()=>ir(cartoes.findIndex(c=>c.id==='escolhe'));
   r.querySelectorAll('[data-mini]').forEach(b=>b.disabled=true);
   r.querySelectorAll('[data-leg]').forEach(b=>b.onclick=()=>{S.f3[b.dataset.leg]=b.dataset.l;S.f3.verificado=false;guardar();refazer('[data-leg="'+b.dataset.leg+'"][data-l="'+b.dataset.l+'"]');});
   r.querySelectorAll('[data-hpar]').forEach(b=>b.onclick=()=>{S.f3.hpar=b.dataset.hpar;guardar();refazer('[data-hpar="'+b.dataset.hpar+'"]');});},
  verificar:{pronto:()=>distintas().length>=2&&!!S.f3.l1&&!!S.f3.l2,fazer(){S.f3.verificado=true;guardar();regras();refazer();const d=distintas(),p1=d[d.length-2],p2=d[d.length-1],x=F.compara;
   const L=k=>F.legendasFim.find(l=>l.id===S.f3[k]),l1=L('l1'),l2=L('l2'),par=parDe(p1,p2);
   const linha=(l,p)=>{const neutra=!l.pede,ok=l.pede===p,m=neutra?'●':ok?'◐':'○';return '<li>'+marcaHtml(m)+' «'+e(semPonto(l.t))+'», '+e(fmt(T.comMin,{p:titulo(p)}))+'. '+e(neutra?x.ves:ok?x.supoesCom:x.supoesSem)+' '+e(neutra||ok?l.com:l.sem)+'</li>';};
   const igual=l1.id===l2.id,neutra=igual&&!l1.pede,H=par.principal;
   const corpoP=neutra?fmt(x.neutraCorpo,{l:semPonto(l1.t)}):igual?fmt(x.igualCorpo,{l:semPonto(l1.t),H:semPonto(hTexto(H))}):fmt(x.difCorpo,{p1:titulo(p1),p2:titulo(p2),l1:semPonto(l1.t),l2:semPonto(l2.t)});
   painel({titulo:neutra?x.neutraTitulo:igual?x.igualTitulo:x.difTitulo,html:'<p>'+e(corpoP)+'</p><ul class="lf-linhas">'+linha(l1,p1)+linha(l2,p2)+'</ul><p>'+e(par.sintese)+'</p>'+(igual?'':'<p>'+e(par[H])+'</p>'),botoes:[{t:T.outra,onclick:()=>{fecharPainel();foco('[data-leg="l1"]');}},{t:T.seguinte,prim:true,vai:true,onclick:seguinte}]});}},
  pronto:()=>S.f3.verificado},

 {id:'reve',tipo:'revisao',html(){const x=F.reve,d=distintas(),nen=S.inicial==='nenhuma';
   if(!S.inicial)return rotulo(x.rotulo)+pergunta(x.pergunta)+'<p class="lf-estado">'+e(F.ve.pergunta)+'</p>';
   const est=nen?'':'<p class="lf-afirma-t">'+e(hTexto(S.inicial))+'</p><ul class="lf-lista">'+d.map(p=>'<li>'+e(fmt(T.com,{p:titulo(p)}))+': '+linhaH(S.inicial,estadoDe(p,S.inicial),{razao:false})+'</li>').join('')+'</ul>';
   const resp=nen?'<button type="button" class="lf-op" data-rev="continua" aria-pressed="'+(S.f4.resp==='continua')+'">'+e(x.continua)+'</button>'+F.hipoteses.map(h=>'<button type="button" class="lf-op" data-rev="'+h.id+'" aria-pressed="'+(S.f4.resp===h.id)+'">'+e(h.t)+'</button>').join(''):x.respostas.map(r=>'<button type="button" class="lf-op" data-rev="'+r.id+'" aria-pressed="'+(S.f4.resp===r.id)+'">'+e(r.t)+'</button>').join('');
   const planos=d.map(p=>'<button type="button" class="lf-op" data-plano="'+p+'" aria-pressed="'+(S.f4.plano===p)+'">'+e(titulo(p))+'</button>').join('')+'<button type="button" class="lf-op" data-plano="nenhum" aria-pressed="'+(S.f4.plano==='nenhum')+'">'+e(x.nenhumPlano)+'</button>';
   return rotulo(x.rotulo)+pergunta(nen?x.perguntaNenhuma:x.pergunta)+est+'<div class="lf-linha-botoes lf-col-botoes" role="group" aria-label="'+e(nen?x.perguntaNenhuma:x.pergunta)+'">'+resp+'</div><h3 class="lf-etq">'+e(x.plano)+'</h3><div class="lf-linha-botoes" role="group" aria-label="'+e(x.plano)+'">'+planos+'</div>';},
  ligar(r){const fim=()=>{if(S.f4.resp&&S.f4.plano){regras();painel({titulo:F.reve.respostas.concat([{id:'continua',t:F.reve.continua}]).concat(F.hipoteses).find(x=>x.id===S.f4.resp).t,html:'<p>'+e(explicaRev())+'</p><p>'+e(linhaPlano())+'</p>',botoes:[{t:T.outra,onclick:()=>{fecharPainel();foco('[data-rev]');}},{t:T.seguinte,prim:true,vai:true,onclick:seguinte}]});}};
   r.querySelectorAll('[data-rev]').forEach(b=>b.onclick=()=>{S.f4.resp=b.dataset.rev;guardar();refazer('[data-rev="'+S.f4.resp+'"]');fim();});
   r.querySelectorAll('[data-plano]').forEach(b=>b.onclick=()=>{S.f4.plano=b.dataset.plano;guardar();refazer('[data-plano="'+S.f4.plano+'"]');fim();});},
  pronto:()=>!S.inicial||!!(S.f4.resp&&S.f4.plano)},

 {id:'escreve',tipo:'transferir',opcional:true,html(){const x=F.escreve,st=S.f5;
   const av=st.verificado?avisosF5(st.texto):null;
   const cons=st.verificado?((av.length?'<ul class="lf-avisos">'+av.map(t=>'<li class="lf-meio">◐ '+e(t)+'</li>').join('')+'</ul>':'<p>'+e(x.semAviso)+'</p>')+'<h3 class="lf-etq">'+e(x.marcar)+'</h3><ul class="lf-marcar">'+x.hipoteses.map((h,i)=>'<li><span>'+e(h)+'</span><span class="lf-linha-botoes" role="group" aria-label="'+e(h)+'">'+['ganha','perde','igual'].map(s=>'<button type="button" class="lf-op lf-mini-op" data-marca5="'+i+'" data-s="'+s+'" aria-pressed="'+(st.marcas[i]===s)+'" aria-label="'+e(F.estadosNomes[s])+'">'+e(F.estadosSimbolos[s])+'</button>').join('')+'</span></li>').join('')+'</ul>'):'';
   return rotulo(x.rotulo,[x.marca,T.emPapel])+pergunta(x.pergunta)+'<ol class="lf-frases5">'+x.frases.map((f,i)=>'<li'+(i===1?' class="lf-falta"':'')+'>'+e(f)+'</li>').join('')+'</ol><p class="lf-regra">'+e(x.regra)+'</p><p class="lf-etq">'+e(T.hipoteses)+'</p><ul class="lf-lista">'+x.hipoteses.map(h=>'<li>'+e(h)+'</li>').join('')+'</ul><div class="lf-personal"><label class="lf-label" for="f5-texto">'+e(x.legenda)+'</label><textarea id="f5-texto" rows="3" maxlength="600">'+e(st.texto)+'</textarea></div><div class="lf-consequencia" aria-live="polite">'+cons+'</div>';},
  ligar(r){const st=S.f5,ta=r.querySelector('#f5-texto');ta.oninput=()=>{st.texto=ta.value;st.verificado=false;guardar();acoes();};
   r.querySelectorAll('[data-marca5]').forEach(b=>b.onclick=()=>{const antes=F.escreve.hipoteses.every((h,i)=>st.marcas[i]);st.marcas[b.dataset.marca5]=b.dataset.s;guardar();refazer('[data-marca5="'+b.dataset.marca5+'"][data-s="'+b.dataset.s+'"]');if(!antes)painelF5();});},
  verificar:{pronto:()=>!!S.f5.texto.trim(),fazer(){S.f5.verificado=true;guardar();refazer('.lf-consequencia');painelF5();}},
  pronto:()=>true},

 {id:'fim',tipo:'fim',html(){return fimHtml(F.fim);},pronto:()=>true}
];
function escolherPlano(p){S.plano=p;S.escolhas=S.escolhas.filter(x=>x!==p).concat(p);S.visor=3;S.f3.verificado=false;guardar();regras();
 const hI=S.inicial&&S.inicial!=='nenhuma'?S.inicial:null;refazer(S.verif[p]?'[data-cand="'+p+'"]':'[data-marcah="'+(hI||F.hipoteses[0].id)+'"]');}
/* C1 e C3: a linha compara a marca do aluno com a do Lente, com a razão daquela combinação; o corpo longo fica em «Revelar apoio» */
function verificarPlano(){const p=S.plano,x=F.explicacao[p],m=S.marcas[p]||{},hI=S.inicial&&S.inicial!=='nenhuma'?S.inicial:null;
 S.verif[p]=true;guardar();regras();refazer('.lf-consequencia');
 const nome=s=>F.estadosSimbolos[s]+' '+F.estadosNomes[s];
 const linha=h=>{const st=estadoDe(p,h),o={H:semPonto(hTexto(h)),lente:nome(st.estado),razao:st.razao};let l=!m[h]?fmt(F.linhaSo,o):m[h]===st.estado?fmt(F.linhaIgual,o):fmt(F.linhaTu,Object.assign(o,{tu:nome(m[h])}));if(st.discutivel&&st.alternativa)l+=' '+fmt(T.discutivel,{alt:st.alternativa});return l;};
 const ids=(hI?[hI]:[]).concat(F.hipoteses.map(h=>h.id).filter(h=>h!==hI&&m[h]));
 const nd=distintas().length,outro={t:T.experimentarOutro,onclick:()=>{fecharPainel();foco('[data-cand]:not([aria-pressed="true"])');}};
 painel({titulo:x.titulo,html:'<ul class="lf-linhas">'+ids.map(h=>'<li>'+e(linha(h))+'</li>').join('')+'</ul>',apoio:'<p>'+e(x.corpo)+'</p><p class="lf-ves">'+e(fmt(F.linhaComum,{ves:x.ves}))+'</p>'+(x.alternativa?'<p class="lf-alt"><b>'+e(T.alternativa)+'</b> '+e(x.alternativa)+'</p>':''),
  botoes:nd>=2?[{t:T.experimentarOutro,onclick:outro.onclick},{t:T.seguinte,prim:true,vai:true,onclick:seguinte}]:[{t:T.seguinte,onclick:seguinte},Object.assign({prim:true},outro)]});}
function avisosF5(txt){const pal=(txt.toLowerCase().match(/[a-zà-ÿ]+/g)||[]);return F.escreve.palavras.filter(w=>pal.includes(w)).map(w=>w==='porque'?F.escreve.avisoPorque:fmt(F.escreve.aviso,{palavra:w}));}
function painelF5(){const x=F.escreve,st=S.f5;if(!st.verificado||x.hipoteses.some((h,i)=>!st.marcas[i]))return;
 const marcas=x.hipoteses.map((h,i)=>'«'+semPonto(h)+'» '+F.estadosSimbolos[st.marcas[i]]+' '+F.estadosNomes[st.marcas[i]]).join('; ');
 painel({titulo:x.titulo,html:'<p>'+e(fmt(x.corpo,{marcas}))+'</p>',semVeu:true,botoes:[{t:T.outra,onclick:()=>{fecharPainel();foco('#f5-texto');}},{t:T.seguinte,prim:true,vai:true,onclick:seguinte}]});}
function explicaRev(){const x=F.reve.textos,d=distintas(),r=S.f4.resp;
 if(S.inicial==='nenhuma'){if(r==='continua')return x.nenhuma.continua;const G=d.find(p=>estadoDe(p,r).estado==='ganha');return G?fmt(x.nenhuma.ganhou,{H:semPonto(hTexto(r)),G:titulo(G)}):fmt(x.nenhuma.sem,{H:semPonto(hTexto(r))});}
 const H=S.inicial,Pp=d.find(p=>estadoDe(p,H).estado==='perde'),G=d.find(p=>estadoDe(p,H).estado==='ganha'),o={H:semPonto(hTexto(H)),P:Pp?titulo(Pp):'',G:G?titulo(G):''};
 if(Pp&&G&&x[r]&&x[r].ambos)return fmt(x[r].ambos,o);return fmt(x[r][Pp?'perdeu':G?'ganhou':'nenhum'],o);}
function linhaPlano(){const x=F.reve,p=S.f4.plano;if(p==='nenhum')return x.nenhumLinha;const H=S.inicial!=='nenhuma'?S.inicial:(F.hipoteses.some(h=>h.id===S.f4.resp)?S.f4.resp:null);if(!H)return fmt(x.planoLinhaSem,{plano:titulo(p)});const st=estadoDe(p,H).estado;return fmt(x.planoLinha,{plano:titulo(p),H:semPonto(hTexto(H)),estado:F.estadoFrase[st]});}
let seqTimer=null;
function ligarVisor(r){
 r.querySelectorAll('[data-mini]').forEach(b=>b.onclick=()=>{pararSeq();S.visor=+b.dataset.mini;guardar();refazer('[data-mini="'+S.visor+'"]');anunciar();});
 r.querySelectorAll('[data-passo]').forEach(b=>b.onclick=()=>{pararSeq();const t=tiraAtual();S.visor=Math.max(0,Math.min(t.length-1,(S.visor||0)+(+b.dataset.passo)));guardar();refazer('[data-passo="'+b.dataset.passo+'"]:not(:disabled),[data-passo]:not(:disabled)');anunciar();});
 const sq=r.querySelector('[data-seq]');if(sq)sq.onclick=()=>{if(seqTimer){pausarSeq(sq);return;}if(sq.dataset.pausa==='1'){correrSeq(sq,+sq.dataset.k||0);return;}correrSeq(sq,0);};
}
function anunciar(){const a=corpo.querySelector('[data-anuncio]');if(!a)return;const t=tiraAtual(),q=F.quadros[t[S.visor||0]];a.textContent=fmt(T.planoN,{n:(S.visor||0)+1,N:t.length,legenda:q.legenda});}
function correrSeq(btn,k){const t=tiraAtual(),visor=corpo.querySelector('[data-visor]'),a=corpo.querySelector('[data-anuncio]');if(!visor)return;
 visor.classList.add('lf-a-correr');btn.textContent=T.pausa;btn.dataset.pausa='0';if(k===0&&a)a.textContent=T.seqComecou;
 const passo=i=>{if(i>=t.length){pararSeq();visor.classList.remove('lf-a-correr');btn.textContent=T.verOutra;btn.dataset.pausa='';btn.dataset.k='0';if(a)a.textContent=T.seqAcabou;return;}
  btn.dataset.k=String(i);const id=t[i];visor.innerHTML=(id==='lacuna'?'<span class="lf-arte lf-negro" aria-hidden="true"><span>…</span></span>':quadroArte(id,{semAlt:true}))+'<figcaption><span class="lf-claquete">'+e(F.quadros[id].n)+'</span></figcaption>';
  corpo.querySelectorAll('[data-mini]').forEach((m,j)=>m.classList.toggle('lf-sel',j===i));
  seqTimer=setTimeout(()=>passo(i+1),id==='lacuna'?1200:2000);};
 passo(k);}
function pausarSeq(btn){clearTimeout(seqTimer);seqTimer=null;btn.textContent=T.continuar;btn.dataset.pausa='1';}
function pararSeq(){if(seqTimer){clearTimeout(seqTimer);seqTimer=null;}}

/* ── autoverificação: o aluno decide, nada é corrigido nem registado ── */
function autoHtml(itens,k){const st=S[k].auto||{};return '<fieldset class="lf-auto"><legend>'+e(T.autoTitulo)+'</legend>'+itens.map((q,i)=>'<div class="lf-auto-l"><p id="auto-'+k+'-'+i+'">'+e(q)+'</p><div class="lf-linha-botoes" role="group" aria-labelledby="auto-'+k+'-'+i+'">'+T.auto.map((o,j)=>'<button type="button" class="lf-op" data-auto="'+i+'" data-o="'+j+'" aria-pressed="'+(st[i]===j)+'">'+e(o)+'</button>').join('')+'</div></div>').join('')+'<p class="lf-nota-p">'+e(T.autoNota)+'</p></fieldset>';}
function ligarAuto(r,k){r.querySelectorAll('[data-auto]').forEach(b=>b.onclick=()=>{S[k].auto[b.dataset.auto]=+b.dataset.o;refazer('[data-auto="'+b.dataset.auto+'"][data-o="'+b.dataset.o+'"]');});}

/* ── fim de percurso ── */
function fimHtml(f){
 const r=P.estado(ID),falta=P.projetado?[]:[r.experimentei?'':T.registo.falta[ID].exp,r.revi?'':T.registo.falta[ID].revi].filter(Boolean);
 return '<div class="lf-fim-escuro">'+rotulo(f.rotulo)+'<h2 class="lf-levar" tabindex="-1">'+e(f.texto)+'</h2><p class="lf-registo" role="status" data-registo>'+e(linhaRegisto())+'</p>'+falta.map(x=>'<p class="lf-nota-p" data-falta>'+e(x)+'</p>').join('')+'<p class="lf-nota-p">'+e(T.registo.nota)+'</p><p class="lf-nota-p" data-guardar>'+e(P.projetado?'':(P.disponivel()?T.registo.fica:T.registo.semGuardar))+'</p></div><h3 class="lf-etq">'+e(T.paraContinuar)+'</h3><ul class="lf-ligacoes">'+f.ligacoes.map(l=>'<li><a href="'+e(l.href)+'"'+(l.fora?' target="_blank" rel="noopener"':'')+'>'+e(l.t)+'</a></li>').join('')+'</ul>';}

/* ── navegação ── */
const cartoes=ID==='certa-manha'?cartoesK:cartoesF;
const cartaoAtual=()=>cartoes[S.atual];
function estadosBarra(){return cartoes.map((c,i)=>i===S.atual?'atual':S.vistos.includes(i)?(c.tipo==='ler'||c.tipo==='fim'?'ler':c.pronto()?'ok':'ler'):'');}
function acoes(){const c=cartaoAtual(),i=S.atual,ult=i===cartoes.length-1,l=[{t:'←',cls:'seta',esq:true,rotulo:T.anterior,disabled:i===0,onclick:anterior}];
 if(c.verificar&&c.opcional)l.push({t:e(T.verificar),cls:'sec',attrs:{'data-lf-verificar':''},disabled:!c.verificar.pronto(),onclick:()=>c.verificar.fazer()});
 if(!ult)l.push(c.verificar&&!c.opcional&&!c.pronto()?{t:e(T.verificar),cls:'prim',attrs:{'data-lf-verificar':''},disabled:!c.verificar.pronto(),onclick:()=>c.verificar.fazer()}:{t:e(T.seguinte),cls:'prim',attrs:{'data-seguinte':''},disabled:!c.pronto(),onclick:seguinte});
 else l.push({t:e(T.voltar),cls:'prim',href:document.querySelector('.c-marca')?document.querySelector('.c-marca').getAttribute('href'):'../'});
 C.acoes(l);C.num(i+1,cartoes.length);C.barra(estadosBarra(),i,null);}
function render(){pararSeq();const c=cartaoAtual();if(c.entrar)c.entrar();corpo.innerHTML='<div class="jogo"><article class="cartao lf-cartao'+(c.tipo==='fim'?' lf-cartao-fim':'')+'" data-cartao="'+c.id+'" data-tipo="'+c.tipo+'">'+c.html()+'</article></div>';if(c.ligar)c.ligar(corpo);acoes();}
function foco(sel){const el=sel?corpo.querySelector(sel):null;(el||corpo.querySelector('.lf-q,.lf-n1,.lf-levar')||corpo).focus({preventScroll:false});}
function refazer(sel){const y=C.corpo?C.corpo.scrollTop:0;render();if(C.corpo)C.corpo.scrollTop=y;if(sel!==undefined&&sel!==null)foco(sel);}
function ir(i){if(i<0||i>=cartoes.length)return;pararSeq();fecharPainel();S.atual=i;if(!S.vistos.includes(i))S.vistos.push(i);guardar();render();C.rolarTopo();foco(null);}
function seguinte(){const c=cartaoAtual();if(!c.pronto())return;ir(S.atual+1);}
function anterior(){ir(S.atual-1);}

/* teclado: setas fora de campos, sem painel aberto e fora dos elementos compostos; números nos quadros; Escape fecha o painel */
document.addEventListener('keydown',ev=>{
 const t=ev.target,campo=t&&(/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)||t.isContentEditable),menu=raizCasca.querySelector('[data-c-painel]');
 if(menu&&!menu.hidden)return;
 if(ev.key==='Escape'&&C.folha.aberta()){fecharPainel();foco(null);return;}
 if(campo||ev.altKey||ev.ctrlKey||ev.metaKey)return;
 if(/^[1-4]$/.test(ev.key)&&!C.folha.aberta()){const c=cartaoAtual();if(c.teclas&&c.teclas(ev.key))ev.preventDefault();return;}
 if((ev.key==='ArrowRight'||ev.key==='ArrowLeft')&&!C.folha.aberta()&&!(t&&t.closest&&t.closest('[data-composto]'))){ev.preventDefault();if(ev.key==='ArrowRight')seguinte();else anterior();}
});

/* ── menu: imprimir, caderno, fonte, recomeçar ── */
const impressao=document.createElement('div');impressao.className='lf-print';impressao.id='lf-print';impressao.setAttribute('aria-hidden','true');document.body.appendChild(impressao);
let modoImpressao='enunciado';
function linhas(n){return '<div class="lf-lines" style="height:'+(n*9)+'mm"></div>';}
const so=(modo,h,tag)=>'<'+(tag||'div')+' class="lf-p-'+modo+'">'+h+'</'+(tag||'div')+'>';
function impressaoHtml(){
 let h='<h1>'+e(D.titulo)+'</h1><p>'+e(T.impressao.nome)+' ______________________ '+so('enunciado',e(T.impressao.enunciado),'span')+so('apoios',e(T.impressao.apoios),'span')+'</p>',en='',ap='';
 if(ID==='certa-manha'){
  h+='<blockquote>'+e(K.frase)+'</blockquote><p class="lf-pc">'+it(K.credito.completo)+'</p>';
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
  const fig=id=>{const q=F.quadros[id];return '<figure>'+(q.img?'<img src="'+e(IMG+q.img+'.webp')+'" alt="" width="600" height="600">':'<div class="lf-pq">'+e(q.intertitulo?q.legenda:'?')+'</div>')+'<figcaption>'+e(q.n+' '+q.titulo+'. '+q.legenda)+'</figcaption></figure>';};
  h+='<section><h2>'+e(F.abre.texto)+'</h2><div class="lf-pgrelha">'+F.tira.map(fig).join('')+'</div><h2>'+e(T.planosLugar)+'</h2><div class="lf-pgrelha">'+F.candidatos.map(fig).join('')+'</div></section>';
  en+='<section><h2>'+e(F.ve.pergunta)+'</h2><table><thead><tr><th>'+e(T.hipotese)+'</th><th>'+e(T.antes)+'</th>'+F.candidatos.map(p=>'<th>'+e(titulo(p))+'</th>').join('')+'</tr></thead><tbody>'+F.hipoteses.map(h1=>'<tr><td>'+e(h1.t)+'</td><td>□</td><td></td><td></td><td></td></tr>').join('')+'</tbody></table><p>'+e(T.legendaEstados)+'</p></section>';
  en+='<section><h2>'+e(F.compara.pergunta)+'</h2>'+linhas(3)+'<h2>'+e(F.escreve.pergunta)+'</h2><ol><li>'+e(F.escreve.frases[0])+'</li><li>______________________</li><li>'+e(F.escreve.frases[2])+'</li></ol><p>'+e(F.escreve.regra)+'</p></section>';
  ap+='<section><h2>'+e(F.quadroTitulo)+'</h2><table><thead><tr><th>'+e(T.hipotese)+'</th>'+F.candidatos.map(p=>'<th>'+e(titulo(p))+'</th>').join('')+'</tr></thead><tbody>'+F.hipoteses.map(h1=>'<tr><td>'+e(h1.t)+'</td>'+F.candidatos.map(p=>{const s=F.estados[p][h1.id];return '<td>'+e(F.estadosSimbolos[s.estado]+' '+F.estadosNomes[s.estado])+'. '+e(s.razao)+'</td>';}).join('')+'</tr>').join('')+'</tbody></table><p>'+e(F.quadroNota)+'</p></section>';
  ap+='<section>'+F.candidatos.map(p=>'<p><b>'+e(F.explicacao[p].titulo)+'</b> '+e(F.explicacao[p].corpo)+'</p>').join('')+'</section>';
 }
 return h+so('enunciado',en)+so('apoios',ap);}
impressao.innerHTML=impressaoHtml();
function modo(m){impressao.classList.toggle('lf-modo-apoios',m==='apoios');}
window.addEventListener('beforeprint',()=>modo(modoImpressao));
window.addEventListener('afterprint',()=>{modoImpressao='enunciado';modo('enunciado');});
function imprimir(m){modoImpressao=m;C.menu.fechar();modo(m);try{window.print();}catch(x){}}
function cadernoTexto(){
 const L=[T.caderno.titulo,D.titulo,T.caderno.nota,''];
 if(ID==='certa-manha'){
  L.push(K.frase,'');
  if(S.a1.corte)L.push(T.txt.corte+' '+K.segmentos.find(s=>s.id===S.a1.corte).t);
  Object.keys(S.a2.respostas).forEach(v=>{const x=K.a2.variantes.find(y=>y.id===v);L.push(x.nome+': '+K.a2.respostas.find(r=>r.id===S.a2.respostas[v]).t);});
  if(S.a3.primeira)L.push('',T.primeiraVersao+': '+S.a3.primeira);if(S.a3.texto)L.push(T.txt.abertura+' '+S.a3.texto);
  if(S.b1.primeira){L.push('',T.txt.primeira);K.afirmacoes.forEach(a=>L.push('  '+a.t+' '+colNome(S.b1.primeira[a.id])));}
  if(S.b2.linha)L.push('',K.b2.linha+' '+S.b2.linha);if(S.b3.texto)L.push('',S.b3.texto);
  if(S.f1.pos){L.push('',T.txt.agora);K.afirmacoes.forEach(a=>L.push('  '+a.t+' '+colNome(S.f1.pos[a.id],true)));}
  if(S.f2.info)L.push('',K.f2.informacao+' '+K.f2.escolhas.find(x=>x.id===S.f2.info).t);if(S.f2.porque)L.push(K.f2.porque+' '+S.f2.porque);
 }else{
  if(S.inicial)L.push(T.txt.inicial+' '+(S.inicial==='nenhuma'?F.nenhuma:hTexto(S.inicial)));
  const nome=s=>F.estadosSimbolos[s]+' '+F.estadosNomes[s],d=distintas();
  d.forEach(p=>{L.push(T.txt.montagem+' '+titulo(p));const m=S.marcas[p]||{};const l=F.hipoteses.filter(h=>m[h.id]).map(h=>'  '+h.t+' '+nome(m[h.id]));if(l.length)L.push(fmt(T.txt.marquei,{p:titulo(p)}),...l);});
  if(d.length>=2)[['l1',d[d.length-2]],['l2',d[d.length-1]]].forEach(([k,p])=>{if(S.f3[k])L.push(fmt(T.txt.legenda,{p:titulo(p)})+' '+F.legendasFim.find(l=>l.id===S.f3[k]).t);});
  if(S.f4.resp)L.push(T.txt.revisao+' '+(F.reve.respostas.concat([{id:'continua',t:F.reve.continua}]).concat(F.hipoteses).find(x=>x.id===S.f4.resp)||{}).t);
  if(S.f4.plano)L.push(T.txt.plano+' '+(S.f4.plano==='nenhum'?F.reve.nenhumPlano:titulo(S.f4.plano)));
  if(S.f5.texto)L.push('',T.txt.meio+' '+S.f5.texto);
  const m5=F.escreve.hipoteses.filter((h,i)=>S.f5.marcas[i]);if(m5.length)L.push(T.txt.marcasMeio,...F.escreve.hipoteses.map((h,i)=>S.f5.marcas[i]?'  '+h+' '+nome(S.f5.marcas[i]):'').filter(Boolean));
 }
 return L.join('\n')+'\n';}
function levarCaderno(){C.menu.fechar();const url=URL.createObjectURL(new Blob([cadernoTexto()],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='lente-'+ID+'.txt';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),2000);}
function fonte(){C.menu.fechar();const h=ID==='certa-manha'?'<p>'+it(K.credito.completo)+'</p><p><a href="'+e(K.credito.rtp)+'" target="_blank" rel="noopener">'+e(K.credito.verRtp)+'</a> <a href="'+e(K.credito.rtpPlay)+'" target="_blank" rel="noopener">'+e(K.credito.verRtpPlay)+'</a></p><p>'+it(K.original.credito)+'</p><p><a href="'+e(K.original.gutenberg)+'" target="_blank" rel="noopener">'+e(K.original.verGutenberg)+'</a></p><p>'+e(K.a2.nota)+'</p>':'<p>'+e(F.creditos)+'</p><p>'+e(F.abre.nota)+'</p>';
 painel({titulo:T.fonteTitulo,rotulo:false,html:h,semVeu:true,botoes:[{t:T.fechar,prim:true,onclick:()=>{fecharPainel();foco(null);}}]});}
function recomecar(){C.menu.fechar();const tem=JSON.stringify(S)!==JSON.stringify(Object.assign(fresco(),{atual:S.atual,vistos:S.vistos}));if(tem&&!confirm(T.recomecar[ID]))return;S=fresco();P.sessao(ID,null);ir(0);}
raizCasca.querySelectorAll('[data-lf-menu]').forEach(b=>b.onclick=()=>{const a=b.dataset.lfMenu;if(a==='enunciado'||a==='apoios')imprimir(a);else if(a==='caderno')levarCaderno();else if(a==='fonte')fonte();else if(a==='recomecar')recomecar();});
if(P.projetado){const n=document.createElement('p');n.className='lf-aviso-proj';n.textContent=T.registo.projecao;raizCasca.appendChild(n);}

window.LenteCartoes={TEXTOS:T,ir:ir,estado:()=>JSON.parse(JSON.stringify(S))};
if(S.atual>=cartoes.length)S.atual=0;
render();
})();
