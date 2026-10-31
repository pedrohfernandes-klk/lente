/* Dados: escolher/completar/classificar/autoavaliacao {id,pergunta,apoio?,opcoes:[{id,texto,feedback}],certa?,pistas?,imagem?};
 ordenar: mesmas opções, ordenadas por toque; composicao {partes:[{bloco,rotulo,fonte,sequencia?,se?:{fonte,valor}}],revisao?};
 escrita {acao,apoio}; exemplo {trechos:[[rotulo,texto]],ultimo?}. Todos têm id, tipo e pergunta.
 A composição resolve fontes e ordem apenas dos dados. IDs de respostas usam letras para LenteProgresso.primeira. */
(function(){'use strict';
const D=window.LenteTresCartasDados,P=window.LenteProgresso,ID='tres-cartas';
const raiz=document.querySelector('[data-casca]'),C=EPICasca.pagina(raiz),alvo=document.getElementById('cartoes');
// Escape adaptado do motor partilhado cartoes.js, sem o carregar.
const e=v=>String(v==null?'':v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const novo=()=>({atual:0,respostas:{},feitos:{},pistas:{},primeira:null,comparou:false});
let S=P.projetado?novo():(P.sessao(ID)||novo());
if(!Number.isInteger(S.atual)||S.atual<0||S.atual>=D.cartoes.length)S=novo();
const porId=id=>D.cartoes.find(c=>c.id===id),atual=()=>D.cartoes[S.atual];
function guardar(){if(!P.projetado)P.sessao(ID,S);}
function imagem(id){const im=D.imagens.find(i=>i.id===id);return '<div class="tc-imagem tc-descricao">'+e(im.alt)+'</div>';}
function titulo(c){return '<h2 class="q lf-q" tabindex="-1">'+e(c.pergunta)+'</h2>'+(c.apoio?'<p class="dica">'+e(c.apoio)+'</p>':'');}
function plano(c,respostas){const blocos=[];for(const p of c.partes){
 if(p.se&&respostas[p.se.fonte]!==p.se.valor)continue;
 const fonte=porId(p.fonte),v=respostas[p.fonte]||'';
 const pecas=[...v].map(k=>fonte.opcoes.find(o=>o.id===k)?.texto||'').filter(Boolean);
 const texto=p.sequencia?pecas.map((t,i)=>p.sequencia[i]+', '+t.replace(/[.]$/,'').replace(/^./,x=>x.toLowerCase())).join('; ')+'.':pecas.join(' ');
 let bloco=blocos.find(b=>b.titulo===p.bloco);if(!bloco){bloco={titulo:p.bloco,partes:[]};blocos.push(bloco);}
 bloco.partes.push({rotulo:p.rotulo,texto:texto||D.ui.t0});
 }return blocos;}
function planoHtml(c,r){return '<div class="tc-plano">'+plano(c,r).map(b=>'<section><h3>'+e(b.titulo)+'</h3><ul>'+b.partes.map(p=>'<li><strong>'+e(p.rotulo)+':</strong> '+e(p.texto)+'</li>').join('')+'</ul></section>').join('')+'</div>';}
function planoTexto(c,r){return plano(c,r).map(b=>b.titulo+'\n'+b.partes.map(p=>p.rotulo+': '+p.texto).join('\n')).join('\n\n');}
function pronto(c){if(['escolher','completar','classificar','autoavaliacao'].includes(c.tipo))return c.certa?S.respostas[c.id]===c.certa:!!S.respostas[c.id];if(c.tipo==='ordenar')return (S.respostas[c.id]||'').length===c.opcoes.length;if(c.tipo==='escrita')return !!S.feitos[c.id];if(c.revisao)return S.comparou;return true;}
function feedback(t){C.folha.abrir({titulo:D.ui.t1,html:'<p>'+e(t)+'</p>',focar:false,botao:{t:D.ui.t2,onclick:()=>{C.folha.fechar();alvo.querySelector('.lf-q').focus();}}});}
function pistas(c){if(!c.pistas)return '';const n=S.pistas[c.id]||0;return '<div class="tc-pistas">'+c.pistas.slice(0,n).map(t=>'<p class="dica">'+e(t)+'</p>').join('')+(n<c.pistas.length?'<button class="lf-apoio" data-pista>'+e(D.ui.pista)+' '+(n+1)+'</button>':'')+'</div>';}
function escolhas(c){const v=S.respostas[c.id];return (c.imagem?imagem(c.imagem):'')+titulo(c)+'<div class="tc-opcoes">'+c.opcoes.map(o=>'<button class="lf-op" data-op="'+o.id+'" aria-pressed="'+(v===o.id)+'">'+e(o.texto)+'</button>').join('')+'</div>'+(v?'<p class="lf-estado" role="status">'+e(c.molde?c.molde.replace('{peca}',c.opcoes.find(o=>o.id===v).texto):c.opcoes.find(o=>o.id===v).texto)+'</p>':'')+pistas(c);}
const tipos={
 escolher:escolhas,completar:escolhas,classificar:escolhas,autoavaliacao:escolhas,
 ordenar:c=>{const v=S.respostas[c.id]||'';return titulo(c)+'<ol class="tc-ordem" aria-live="polite">'+[...v].map(k=>'<li>'+e(c.opcoes.find(o=>o.id===k).texto)+'</li>').join('')+'</ol><div class="tc-opcoes">'+c.opcoes.filter(o=>!v.includes(o.id)).map(o=>'<button class="lf-op" data-ord="'+o.id+'">'+e(o.texto)+'</button>').join('')+'</div>'+(v?'<button class="lf-apoio" data-desfazer>'+e(D.ui.t4)+'</button>':'')+pistas(c);},
 composicao:c=>titulo(c)+(c.revisao?'<h3>'+e(D.ui.t5)+'</h3>'+planoHtml(c,S.primeira||{})+'<h3>'+e(D.ui.t6)+'</h3>':'')+planoHtml(c,S.respostas)+'<button class="lf-op" data-copiar>'+e(D.ui.t7)+'</button>'+(c.revisao?'<button class="lf-op" data-comparar>'+e(D.ui.t8)+'</button>':'')+'<p role="status" data-estado></p>',
 escrita:c=>titulo(c)+'<details open><summary>'+e(D.ui.t9)+'</summary>'+planoHtml(porId(c.plano),S.respostas)+'</details><button class="lf-op" data-escrevi aria-pressed="'+!!S.feitos[c.id]+'">'+e(c.acao)+'</button>',
 exemplo:c=>titulo(c)+c.trechos.map(([r,t])=>'<p><strong>'+e(r)+':</strong> '+e(t)+'</p>').join('')+(c.ultimo?'<p class="lf-credito">'+e(D.credito)+'</p><p><a href="https://creativecommons.org/licenses/by-sa/4.0/deed.pt">'+e(D.ui.t10)+'</a></p><button class="lf-op" data-imprimir>'+e(D.ui.t11)+'</button>':'')
};
function acoes(){const c=atual();C.num(S.atual+1,D.cartoes.length);C.barra(D.cartoes.map((x,i)=>i===S.atual?'atual':S.feitos[x.id]?'ok':''),S.atual,null);C.acoes([{t:'←',rotulo:D.ui.t12,cls:'seta',esq:true,disabled:S.atual===0,onclick:()=>ir(S.atual-1)},S.atual<D.cartoes.length-1?{t:D.ui.t13,cls:'prim',attrs:{'data-seguinte':''},disabled:!pronto(c),onclick:()=>{S.feitos[c.id]=true;ir(S.atual+1);}}:(((n,v)=>n?{t:D.ui.t13,cls:'prim',href:n.href}:{t:v?v.textContent:D.ui.t14,cls:'prim',href:v?v.href:'../../criar/'})(document.querySelector('.lab-fim-percurso a:last-of-type:not(:first-of-type)'),document.querySelector('.lab-fim-percurso a')))]);}
function desenhar(){C.folha.fechar();const c=atual();alvo.innerHTML='<div class="jogo"><article class="cartao lf-cartao" data-cartao="'+c.id+'" data-tipo="'+c.tipo+'">'+tipos[c.tipo](c)+'</article></div>';acoes();
 alvo.querySelectorAll('[data-op]').forEach(b=>b.onclick=()=>{S.respostas[c.id]=b.dataset.op;S.comparou=false;guardar();desenhar();feedback(c.opcoes.find(o=>o.id===b.dataset.op).feedback);});
 alvo.querySelectorAll('[data-ord]').forEach(b=>b.onclick=()=>{S.respostas[c.id]=(S.respostas[c.id]||'')+b.dataset.ord;S.comparou=false;guardar();desenhar();alvo.querySelector('[data-ord], [data-desfazer]')?.focus();});
 const ligar=(s,f)=>{const el=alvo.querySelector(s);if(el)el.onclick=f;};
 ligar('[data-desfazer]',()=>{S.respostas[c.id]=(S.respostas[c.id]||'').slice(0,-1);S.comparou=false;guardar();desenhar();alvo.querySelector('[data-ord]')?.focus();});
 ligar('[data-pista]',()=>{S.pistas[c.id]=(S.pistas[c.id]||0)+1;guardar();desenhar();alvo.querySelector('[data-pista]')?.focus();});
 ligar('[data-escrevi]',()=>{S.feitos[c.id]=true;guardar();desenhar();feedback(D.ui.t15);});
 ligar('[data-copiar]',async()=>{try{await navigator.clipboard.writeText(planoTexto(c,S.respostas));alvo.querySelector('[data-estado]').textContent=D.ui.t16;}catch{alvo.querySelector('[data-estado]').textContent=D.ui.t17;}});
 ligar('[data-comparar]',()=>{S.comparou=true;S.feitos[c.id]=true;if(!P.projetado)P.marcar(ID,'revi');guardar();acoes();alvo.querySelector('[data-estado]').textContent=D.ui.t18;});
 ligar('[data-imprimir]',()=>window.print());
}
function ir(i){if(i<0||i>=D.cartoes.length)return;S.atual=i;const c=atual();if(c.tipo==='composicao'&&!c.revisao&&D.cartoes.filter(x=>['escolher','ordenar','completar','classificar'].includes(x.tipo)).every(pronto)){
 if(!S.primeira){S.primeira=JSON.parse(JSON.stringify(S.respostas));if(!P.projetado&&!P.primeira(ID))P.primeira(ID,S.primeira);}
 if(!P.projetado)P.marcar(ID,'experimentei');
 }guardar();desenhar();C.rolarTopo();alvo.querySelector('.lf-q').focus();}
// Papel: percurso completo sem escolhas pessoais nem soluções; exemplos só na última parte.
function papel(){const d=document.createElement('div');d.className='lf-print tc-print';d.innerHTML='<h1>'+e(D.titulo)+'</h1><p>'+e(D.ui.t19)+'</p>'+D.cartoes.map((c,i)=>'<section><h2>'+ (i+1)+'. '+e(c.pergunta)+'</h2>'+(c.imagem?imagem(c.imagem):'')+(c.apoio?'<p>'+e(c.apoio)+'</p>':'')+(c.opcoes?'<ol type="a">'+c.opcoes.map(o=>'<li>'+e(o.texto)+'</li>').join('')+'</ol>':'')+(c.partes?'<ul>'+c.partes.map(p=>'<li>'+e(p.rotulo)+e(D.ui.papelFonte)+(D.cartoes.indexOf(porId(p.fonte))+1)+'. '+e(p.conector)+'</li>').join('')+'</ul>':'')+(c.pistas?'<p>'+e(D.ui.pistas)+c.pistas.map(e).join(' ')+'</p>':'')+(c.trechos?c.trechos.map(([r,t])=>'<p><strong>'+e(r)+':</strong> '+e(t)+'</p>').join(''):'')+'</section>').join('')+'<p>'+e(D.credito)+'</p>';document.body.appendChild(d);}
if(P.projetado){document.body.classList.add('lf-projetar');const n=document.createElement('p');n.className='lf-aviso-proj';n.textContent=D.ui.t20;raiz.appendChild(n);}
// A primeira versão persistente é um plano de códigos, nunca os textos escritos no caderno.
if(!P.projetado&&!S.primeira){const a=P.primeira(ID);if(a)S.primeira=a.arrumacao;}
papel();desenhar();
})();
