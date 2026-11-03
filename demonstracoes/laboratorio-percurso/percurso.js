/* Demonstração isolada: estado em memória, sem leitura ou escrita de armazenamento. */
(function(){'use strict';
const params=new URLSearchParams(location.search),main=document.querySelector('main'),selector=document.querySelector('#estado');
let state=['inicio','retoma','conclusao'].includes(params.get('estado'))?params.get('estado'):'inicio',answer=null,feedback='',correct=false,back='sessao',resource='observar',animatedHeader=null;
selector.value=state;if(params.get('projetar')==='1')document.documentElement.classList.add('em-projecao');
const content=window.PERCURSO;
const project=document.querySelector('#projetar'),boia=document.querySelector('.boia');
project.setAttribute('aria-pressed',String(document.documentElement.classList.contains('em-projecao')));
project.onclick=()=>{const active=document.documentElement.classList.toggle('em-projecao');project.setAttribute('aria-pressed',String(active));project.querySelector('span').textContent=active?'Sair da projeção':'Projetar';boia.open=false;};
document.querySelector('#imprimir').onclick=()=>window.print();
boia.addEventListener('keydown',e=>{if(e.key==='Escape'){boia.open=false;boia.querySelector('summary').focus();}});
boia.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>boia.open=false));
const portal='<section class="porta-pt"><div><p class="etq">Leitura / Língua / Escrita</p><h2>Português</h2><p>Leva a observação para a leitura e para a escrita. Escolhe um dos nove módulos.</p><a href="https://pedrohfernandes-klk.github.io/pt/">Entrar em Português →</a></div><svg viewBox="0 0 360 180" aria-hidden="true"><path d="M0 35Q90 0 180 35T360 35M0 70Q90 35 180 70T360 70M0 105Q90 70 180 105T360 105M0 140Q90 105 180 140T360 140"/><path class="livro" d="M110 48q35-12 70 0q35-12 70 0v90q-35-12-70 0q-35-12-70 0zM180 48v90"/></svg><small>Grafismo gerado com recurso a IA. Livro e linhas de calçada, EPI, 2026.</small></section>';

// Seleção fechada aprovada em 03/11/2026. Só ligações, sem pedidos externos.
const explorar=[
 ['Jogar com palavras',[
  ['Wordle','Descobre a palavra do dia em inglês.','https://www.nytimes.com/games/wordle/index.html','Inglês'],
  ['Léxico','Experimenta um desafio de palavras em português.','https://letra.games/lexico','Português'],
  ['Elos','Procura ligações entre palavras.','https://letra.games/elos','Português']]],
 ['Ver e desenhar',[
  ['Color','Ajusta a cor até encontrares a combinação.','https://color.method.ac/','Inglês'],
  ['Boolean','Combina e recorta formas para construir outra.','https://boolean.method.ac/','Inglês'],
  ['Bézier','Desenha curvas com pontos e puxadores.','https://bezier.method.ac/','Inglês. Teclado e rato ou painel tátil']]],
 ['Criar com som',[
  ['Music Lab','Experimenta ritmos, sons e melodias.','https://musiclab.chromeexperiments.com/Experiments','Inglês. Som'],
  ['Blob Opera','Move as vozes e cria uma pequena composição.','https://artsandculture.google.com/experiment/blob-opera/AAHWrq360NcGbw','Som']]],
 ['Experimentar decisões',[
  ['Polygons','Muda escolhas individuais e observa o efeito no conjunto.','https://ncase.me/polygons/','Inglês']]],
 ['Descobrir',[
  ['Arts & Culture','Escolhe uma obra e observa os seus pormenores.','https://artsandculture.google.com/','Várias línguas'],
  ['RTP Ensina','Descobre uma história, uma obra ou uma ideia em vídeo.','https://ensina.rtp.pt/','Português. Som nos vídeos']]]
];
const recursoExterno=r=>'<a class="recurso-externo'+(r[0]==='Wordle'?' wordle':'')+'" href="'+r[2]+'" target="_blank" rel="noopener noreferrer"><b>'+r[0]+' ↗</b><span>'+r[1]+'</span><small>'+r[3]+'. Abre noutro sítio, num novo separador.</small></a>';
const entradaExplorar=()=>'<section class="explorar-entrada" aria-labelledby="explorar-titulo"><h2 id="explorar-titulo">Explorar</h2><p>Uma pausa para experimentar palavras, imagens, sons e escolhas.</p><div class="explorar-destaques">'+[explorar[0][1][0],explorar[1][1][0],explorar[2][1][0]].map(recursoExterno).join('')+'</div><a class="secundaria" href="#explorar">Ver todos os recursos por categoria →</a></section>';
const categoriasExplorar=()=>'<div class="explorar-categorias">'+explorar.map(([titulo,lista])=>'<section><h2>'+titulo+'</h2>'+lista.map(recursoExterno).join('')+'</section>').join('')+'</div>';

const steps='<ol><li>Juntar material</li><li>Trabalhar o material</li><li>Largar</li><li>A ideia aparece</li><li>Dar forma e pôr à prova</li></ol>';
const method='<details class="metodo"><summary>Os cinco passos do método</summary><p>Seguimos o método de James Webb Young. Nas duas sessões publicadas, começas por juntar material e observar melhor.</p>'+steps+'<a href="../../biblioteca/young-tecnica-1940/">Ler sobre o método de Young</a></details>';
const resources={observar:['Observar','Volta ao que o texto mostra. Separa o que viste do que concluíste.','../../narrativas/ver/','Explorar os percursos de observação'],experimentar:['Experimentar','Põe à prova uma escolha e vê o que muda.','../../narrativas/treinar/','Abrir os treinos'],relacionar:['Relacionar','Junta o que observaste a outro material. Que ligação consegues explicar?','../../narrativas/ideias/sessao-02/','Abrir «O cocheiro»'],forma:['Dar forma','Escolhe como apresentar e pôr à prova a tua ideia.','../../narrativas/criar/','Abrir as oficinas']};
const portas=()=>'<div class="portas">'+Object.entries(resources).map(([key,r])=>'<a class="porta" href="#recurso-'+key+'"><b>'+r[0]+' →</b><span>'+r[1]+'</span></a>').join('')+'</div>';
const action=()=>state==='conclusao'?['Voltar ao que observaste','fim']:state==='retoma'?['Continuar a sessão 1','sessao']:['Começar a sessão 1','sessao'];
function drawing(){return '<svg viewBox="0 0 500 320" aria-hidden="true"><rect class="nota" x="60" y="40" width="120" height="90" transform="rotate(-7 120 85)"/><rect class="nota" x="300" y="160" width="130" height="100" transform="rotate(5 365 210)"/><path d="M80 70h75m-75 16h60m175 115h90m-90 18h70"/><path class="ligacao" d="M170 110C370 30 100 270 310 210"/></svg>';}
function header(title,text,cta,href){return '<header class="abertura" data-fundo="lm" data-fundo-ciclo="36"><p class="etq">Laboratório / Ideias</p><h1>'+title+'</h1><p>'+text+'</p><a class="principal" href="#'+href+'">'+cta+' →</a>'+drawing()+'<p class="credito-desenho">Grafismo gerado com recurso a IA. Notas e ligação, EPI, 2026.</p><button class="pausa" data-fundo-botao="lm" hidden>Parar o desenho</button></header>';}
function render(){const route=location.hash.slice(1)||'lab';document.querySelector('#onde').textContent=route==='lab'?'':route==='ideias'?' / Ideias':route==='sessao'?' / Ideias / Ver ou observar?':route==='fim'?' / Ideias / O que levas':route==='explorar'?' / Explorar':' / Recursos';
 if(route==='lab'){main.innerHTML=header('Uma ideia começa no que observas.',state==='conclusao'?'Já tens material. Volta ao que registaste e escolhe o que te falta explorar.':state==='retoma'?'Deixaste uma pergunta em aberto. Volta a ela, ou procura um recurso para avançar.':'Olha para o que te rodeia. Junta material, faz ligações e dá forma a uma ideia tua.',state==='inicio'?'Entrar em Ideias':'Voltar a Ideias','ideias')+'<h2>O que precisas agora?</h2><p>Estes recursos acompanham o teu trabalho em Ideias. Podes explorá-los e voltar ao ponto em que estavas.</p>'+portas()+entradaExplorar()+portal;back='lab';}
 else if(route==='ideias'){const a=action();main.innerHTML=header('Ideias','Observa o que te rodeia e dá forma a uma ideia tua.',a[0],a[1])+method+'<h2>As sessões publicadas</h2><p><a href="#sessao">1. Ver ou observar?</a></p><p><a href="../../narrativas/ideias/sessao-02/">2. O cocheiro</a></p><a href="#explorar">Explorar um recurso antes de continuar</a>';back='ideias';}
 else if(route==='sessao'){main.innerHTML='<p class="etq">Ideias / Sessão 1 / Juntar material</p><h1>Ver ou observar?</h1><p>'+content.pergunta.p+'</p><div class="opcoes">'+content.pergunta.o.map((o,i)=>'<button data-answer="'+i+'" aria-pressed="'+(answer===i)+'">'+o+'</button>').join('')+'</div><div class="feedback '+(feedback?(correct?'positivo':'negativo'):'')+'" role="status">'+(feedback?'<b>'+('<span class="resultado-simbolo" aria-hidden="true">'+(correct?'✓':'✗')+'</span> '+(correct?'Certo.':'Ainda não.'))+'</b> ':'')+feedback+'</div><a class="principal" href="#fim" '+(correct?'':'hidden')+'>O que levas →</a><div class="apoio"><h2>Falta-te uma pista?</h2><a href="#recurso-observar">Reler a conversa de Watson e Holmes →</a><p>Ao voltar, a tua escolha continua aqui.</p></div><a class="secundaria" href="../../narrativas/ideias/sessao-01/">Abrir a sessão completa publicada</a>';back='sessao';main.querySelectorAll('[data-answer]').forEach(b=>b.onclick=()=>{answer=Number(b.dataset.answer);correct=answer===content.pergunta.c;feedback=correct?content.pergunta.f:'Volta à conversa: o que Watson viu e o que conseguiu dizer sobre a escada? Podes reler e escolher de novo.';render();main.querySelector('[data-answer="'+answer+'"]').focus();});}
 else if(route==='fim'){main.innerHTML='<section class="fim"><p class="etq">Ideias / O que levas</p><h1>Ver não basta.</h1><p>O texto distingue passar os olhos de observar e conseguir dizer o que está lá.</p><p>Volta ao número de degraus que escreveste no caderno. Confirma-o quando puderes observar a escada.</p><a class="principal" href="#recurso-relacionar">Preparar a próxima sessão →</a><a href="#explorar">Ou escolher outro recurso</a><p><a href="#ideias">Voltar a Ideias</a></p></section>';back='fim';}
 else if(route==='explorar'){main.innerHTML='<p class="etq">Laboratório / Explorar</p><h1>Explorar</h1><p>Escolhe uma experiência. Cada ligação abre noutro separador; o teu percurso fica aqui.</p>'+categoriasExplorar()+'<a class="secundaria" href="#'+back+'">Voltar ao ponto de partida →</a>';}
 else if(route.startsWith('recurso-')&&resources[route.slice(8)]){resource=route.slice(8);const r=resources[resource];main.innerHTML='<p class="etq">Um recurso para '+r[0].toLowerCase()+'</p><h1>'+r[0]+'</h1>'+(resource==='observar'?content.leitura.html:resource==='relacionar'?'<p>A próxima sessão publicada é «O cocheiro». Leva o material que observaste para continuar o trabalho.</p>':'<p>'+r[1]+'</p>')+'<a class="principal" href="#'+back+'">'+(back==='sessao'?'Voltar à pergunta':'Voltar ao percurso')+' →</a><a class="secundaria" target="_blank" rel="noopener" href="'+r[2]+'">'+r[3]+' (novo separador)</a><p class="fonte">O recurso completo abre à parte para poderes regressar a este ponto.</p>';}
 else{location.hash='lab';return;}
 // O motor comum conserva pausa, dois ciclos, fora de vista, redução de movimento e projeção.
 const mountedHeader=main.querySelector('[data-fundo]');
 if(mountedHeader&&!animatedHeader){animatedHeader=mountedHeader;const s=document.createElement('script');s.src='../../assets/fundos.js';document.body.append(s);}
 else if(mountedHeader){
  // Reutilizar o mesmo desenho e botão evita acumular observadores e relógios.
  for(const selector of ['h1','p:not(.etq):not(.credito-desenho)','.principal']){
   const before=animatedHeader.querySelector(selector),after=mountedHeader.querySelector(selector);
   before.textContent=after.textContent;if(after.hasAttribute('href'))before.setAttribute('href',after.getAttribute('href'));
  }
  mountedHeader.replaceWith(animatedHeader);
 }
}
selector.onchange=()=>{state=selector.value;answer=null;feedback='';correct=false;history.replaceState(null,'',location.pathname+'?estado='+state+(params.get('projetar')==='1'?'&projetar=1':'')+'#lab');render();};
addEventListener('hashchange',()=>{render();main.focus();main.scrollTop=0;window.scrollTo(0,0);});render();
})();
