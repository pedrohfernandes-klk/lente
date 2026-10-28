"""Uma abertura, cinco passos, uma ação seguinte. HTML estático e acessível."""
from html import escape as e
from urllib.parse import quote
import subprocess,re

def render(api,sessions,capsules,short_caps,image_prompts):
 R,write,old,link,rel=api['R'],api['write'],api['old'],api['anchor'],api['rel']
 def top(path):
  brand='<span class="c10-brand">'+link(path,'index.html','Lente')+' / '+link(path,'cidadania/','Cidadania')+'</span>'
  module=link(path,'cidadania/m1/','Módulo 1') if path!='cidadania/m1/index.html' else ''
  projection=rel(path,'projetar/')+'?pagina='+quote('/lente/'+path.rsplit('/',1)[0]+'/',safe='')
  return '<nav class="c10-top" aria-label="Navegação do módulo">'+brand+module+link(path,'cidadania/projeto/','Pergunta Humana')+link(path,'cidadania/m1/biblioteca/','Biblioteca')+'<button type="button" data-print hidden>Imprimir</button><a class="epi-projection-menu-link" href="'+projection+'">Projetar</a></nav>'
 def document(path,title,body,num=''):
  assets=rel(path,'assets/').rstrip('/')+'/'
  head='<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+' · M1 · Cidadania</title><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet"><link rel="stylesheet" href="'+assets+'appearance.css"><script src="'+assets+'appearance.js"></script><link rel="stylesheet" href="'+assets+'cidadania-m1-sessoes.css?v=20261027-molde-2"><script defer src="'+assets+'cidadania-m1-sessoes.js?v=20261027-molde-2"></script>'
  return '<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head>'+head+'</head><body class="c10-body"><main class="c10" data-c10'+(' data-session="'+num+'"' if num else '')+'>'+top(path)+body+'</main><script defer src="'+assets+'projection-launcher.js" data-site="lente"></script></body></html>\n'
 def image(path,s,cls=''):
  return '<figure'+(' class="'+cls+'"' if cls else '')+'><img src="'+rel(path,'img/cidadania/'+s['image'])+'" alt="'+e(s['caption'],quote=True)+'" loading="lazy" decoding="async"><figcaption>'+e(s['caption'])+' · '+link(path,'cidadania/m1/imagens/','Créditos')+'</figcaption></figure>'
 def resource_list(path,s):return '<ul>'+''.join('<li>'+link(path,p,api['source_label'](p.split('#')[0]))+'</li>' for p in s['resources'])+'</ul>'
 def capsule(path,key):
  title,text,task=short_caps[key];sources=capsules[key]['sources']
  return '<aside class="c10-capsule"><p class="c10-eyebrow">História do teatro</p><h3>'+e(title)+'</h3><p>'+e(text)+'</p><p><b>Experimenta.</b> '+e(task)+'</p><details><summary>Fontes</summary><div><ul>'+''.join('<li><a href="'+(e(u,quote=True) if u.startswith('http') else rel(path,'cidadania/m1/passo-06/'))+'">'+e(t)+'</a></li>' for t,u in sources)+'</ul></div></details></aside>'
 (R/'cidadania/projeto/index.html').write_bytes(subprocess.check_output(['git','show',api['BASE']+':cidadania/projeto/index.html'],cwd=R))
 write('cidadania/m1/percurso-anterior.html',old('cidadania/m1/index.html'))
 # Molde de 27/10/2026: abertura (imagem, pergunta curta, «Começar») e cinco passos,
 # Recupera, Vê, Decide, Faz, Leva; a sessão 03 realiza a tarefa já partilhada.
 from cidadania_m1_molde import LINHA,LINHA_TAREFA,MARCA,MOLDE,OBRAS
 def para(cls,text):return '<p class="'+cls+'">'+e(text)+'</p>' if text else ''
 def label(text):return '<p class="c10-label">'+e(text)+'</p>'
 def recall(items):
  out='<ol class="c10-recall">'
  for q,a in items:out+='<li><p>'+e(q)+'</p>'+('<details class="c10-check"><summary>Confirmar</summary><div><p>'+e(a)+'</p></div></details>' if a else '')+'</li>'
  return out+'</ol>'
 def obra(path,o):
  out='<aside class="c10-obra" aria-label="Cartão da obra"><p class="c10-label">Cartão da obra</p><h3>'+e(o['titulo'])+'</h3><p class="c10-obra-meta">'+e(o['autor'])+', '+e(o['data'])+'</p>'
  if o.get('citacao'):out+='<blockquote><p>«'+e(o['citacao'])+'»</p><footer>'+e(o['citacao_nota'])+'</footer></blockquote>'
  out+='<p class="c10-obra-razao">'+e(o['razao'])+'</p><p class="c10-obra-pergunta">'+e(o['pergunta'])+'</p>'
  out+='<details><summary>Contexto, acesso e outra leitura</summary><div><p>'+e(o['contexto'])+'</p>'
  out+='<h4>Onde encontrar</h4><ul>'+''.join('<li>'+('<a href="'+e(u,quote=True)+'">'+e(t)+'</a>' if u else e(t))+'</li>' for t,u in o['acesso'])+'</ul>'
  if o.get('protegida'):out+='<p class="c10-small">Obra protegida: aqui fica descrita, com indicação de onde a encontrar.</p>'
  out+='<h4>Ligações</h4><ul>'+''.join('<li>'+link(path,u,t)+'</li>' for t,u in o['ligacoes'])+'</ul>'
  out+='<h4>Outra leitura</h4><p>'+e(o['discordante'])+'</p></div></details></aside>'
  return out
 for n,s in enumerate(sessions,1):
  ident=f'{n:02}';path=f'cidadania/m1/sessoes/{ident}/index.html';labels=s['labels'];m=MOLDE[n];tarefa=m.get('tarefa')
  entry=lambda v:s['entry'] if v=='entry' else v
  body='<header class="c10-hero c10-cover" id="abertura" data-session-intro><div class="c10-cover-text"><p class="c10-eyebrow">Sessão '+ident+' · '+e(s['theme'])+'</p><h1>'+e(s['title'])+'</h1><p class="c10-deck">'+e(s['question'])+'</p><a class="c10-action" href="#momento-1" data-start>Começar</a></div>'+image(path,s,'c10-cover-img')+'</header>'
  body+='<div class="c10-flow" data-session-flow><nav class="c10-stagebar" aria-label="Cinco passos da sessão"><a class="c10-stage-home" href="#abertura" data-cover-link>Sessão '+ident+'</a>'+''.join('<a href="#momento-'+str(i+1)+'" data-stage-link><b>'+f'{i+1:02}'+'</b><span>'+e(lab)+'</span></a>' for i,lab in enumerate(labels))+'</nav>'
  for i,lab in enumerate(labels):
   mark=MARCA.get(lab)
   body+='<section class="c10-stage" id="momento-'+str(i+1)+'" data-stage data-label="'+e(lab,quote=True)+'" tabindex="-1" aria-labelledby="momento-'+str(i+1)+'-t"><header class="c10-step-head"><span class="c10-step-n" aria-hidden="true">'+f'{i+1:02}'+'</span><h2 id="momento-'+str(i+1)+'-t">'+e(lab)+'</h2><p class="c10-step-line">'+e((LINHA_TAREFA if tarefa else {}).get(lab,LINHA[lab]))+'</p>'+('<p class="c10-mark" data-mark="'+e(mark,quote=True)+'">'+e(mark)+'</p>' if mark else '')+'</header><div class="c10-step-body">'
   if i==0:
    if tarefa:body+=para('c10-instruction',s['entry'])
    body+=recall(m['recupera'])
   elif i==1:
    if tarefa:
     body+=para('c10-instruction',s['reading'])+'<ol class="c10-evidence" aria-label="Da pergunta à resposta"><li><b>Pergunta</b><span>O que queremos saber?</span></li><li><b>Fonte</b><span>Em que nos apoiamos?</span></li><li><b>Resposta</b><span>O que podemos defender?</span></li></ol><p><a class="c10-action c10-action-line" href="'+rel(path,'cidadania/projeto/')+'">Abrir o enunciado</a></p>'
    else:
     body+=para('c10-instruction',entry(m['ve']))
     if m['material']=='image':body+=image(path,s,'c10-material')
     elif s['numbers']:body+='<div class="c10-document">'+e(api['FICHAS'][s['numbers'][0]-1]['sample'])+'</div><p class="c10-credit">Exemplo escrito para esta sessão.</p>'
     body+=para('c10-reading',s['reading'])
     if n in OBRAS:body+=obra(path,OBRAS[n])
    body+='<details class="c10-more"><summary>Obras e materiais</summary><div>'+resource_list(path,s)+'</div></details>'
   elif i==2:
    if tarefa:body+='<ol class="c10-tasks">'+''.join('<li>'+e(t)+'</li>' for t in s['tasks'])+'</ol>'
    else:
     solo=entry(m['silencio']) if m.get('silencio') else s['tasks'][0];group=s['tasks'] if m.get('silencio') else s['tasks'][1:]
     body+='<div class="c10-decide"><div class="c10-solo">'+label('Primeiro, em silêncio')+'<p class="c10-prompt">'+e(solo)+'</p></div><div class="c10-group">'+label('Depois, em grupo')+'<ol class="c10-tasks">'+''.join('<li>'+e(t)+'</li>' for t in group)+'</ol></div></div>'
    body+='<details data-feedback><summary>Comparar razões</summary><div><p>'+e(s['feedback'])+'</p></div></details>'
   elif i==3:
    if m.get('faz_inicio'):body+=para('c10-instruction',s['entry'])
    body+=para('c10-reading',s['work'])+'<p class="c10-output"><b>Guardar</b><span>'+e(s['product'])+'</span></p>'
    if s.get('capsule'):body+=capsule(path,s['capsule'])
    if not tarefa and not m.get('fecho_leva'):body+='<div class="c10-review">'+label('Rever com outra pessoa')+'<p>'+e(s['close'])+'</p></div>'
    if n>=4:body+='<p class="c10-aside-link">'+link(path,'cidadania/m1/oficina-guiao/','Apoio à escrita: argumento e guião')+'</p>'
   else:
    if tarefa:body+=para('c10-reading',s['close'])
    else:
     body+='<div class="c10-exit">'+label('Em papel, antes de sair')+'<p class="c10-exit-q">'+e(m['leva'])+'</p></div>'
     if m.get('fecho_leva'):body+=para('c10-reading',s['close'])
    body+=label('Confirma')+'<ul class="c10-checks">'+''.join('<li>'+e(t)+'</li>' for t in s['criteria'])+'</ul>'
    if not s.get('prior'):body+='<section class="c10-completion" data-completion hidden aria-label="Registo"><label><input type="checkbox" data-session-done>Registar o trabalho revisto</label><p data-live class="c10-small" role="status" aria-live="polite">O registo fica neste aparelho.</p></section>'
   body+='</div></section>'
  next_target=f'cidadania/m1/sessoes/{n+1:02}/' if n<10 else 'cidadania/m1/'
  body+='<nav class="c10-control" data-step-controls aria-label="Avançar na sessão"><button type="button" data-prev hidden>← Anterior</button><span data-position role="status" aria-live="polite"></span><button type="button" data-next hidden>Seguinte →</button><a class="c10-action" href="'+rel(path,next_target)+'" data-next-session hidden>'+('Sessão seguinte' if n<10 else 'Voltar às sessões')+'</a></nav></div>'
  body+='<noscript><p class="c10-small">Os cinco passos estão todos nesta página, uns a seguir aos outros.</p></noscript><footer class="c10-support">'+link(path,'cidadania/m1/','Todas as sessões')+link(path,'cidadania/m1/biblioteca/','Biblioteca')+link(path,'cidadania/m1/sessoes/#sessao-'+ident,'Guia do docente')+'</footer>'
  write(path,document(path,s['title'],body,ident))
 path='cidadania/m1/index.html';hero=dict(image='hals.webp',caption='Frans Hals · As regentes do asilo de velhos, 1664')
 body='<header class="c10-hero c10-cover"><div class="c10-cover-text"><p class="c10-eyebrow">Cidadania · Módulo 1</p><h1>Ser-se humano</h1><p class="c10-deck">Quem conta como pessoa?</p><a class="c10-action" href="sessoes/03/" data-continue>Continuar · sessão 03</a></div>'+image(path,hero,'c10-cover-img')+'</header><div class="c10-sectionhead"><h2>Dez sessões</h2><p class="c10-small" data-count></p></div><ol class="c10-session-list">'
 for n,s in enumerate(sessions,1):
  body+='<li class="c10-card" data-session-card="'+f'{n:02}'+'"><a href="sessoes/'+f'{n:02}'+'/"><span class="c10-number">'+f'{n:02}'+'</span><span class="c10-card-text"><span class="c10-topic">'+e(s['theme'])+'</span><h3>'+e(s['title'])+'</h3><span class="c10-card-q">'+e(s['question'])+'</span><small data-status></small></span></a></li>'
 body+='</ol><footer class="c10-support">'+link(path,'cidadania/m1/biblioteca/','Biblioteca')+link(path,'cidadania/m1/oficina-guiao/','Apoio à escrita')+link(path,'cidadania/m1/sessoes/','Guia do docente')+'</footer>'
 ids=list(dict.fromkeys(re.findall(r'\bid="([^"]+)"',old('cidadania/m1/index.html'))))
 body+='<div hidden>'+''.join('<span id="'+e(k,quote=True)+'"></span>' for k in ids)+''.join('<span id="unidade-'+str(n)+'"></span>' for n in range(1,7) if 'unidade-'+str(n) not in ids)+'</div>'
 write(path,document(path,'Ser-se humano · dez sessões',body))
 # O planeamento é consultado separadamente da linha de ação do aluno.
 path='cidadania/m1/sessoes/index.html';body='<header class="c10-hero"><div><p class="c10-eyebrow">Para o docente</p><h1>Dez sessões</h1><p class="c10-deck">Tempos, materiais e condução.</p></div>'+image(path,hero)+'</header><p>A tarefa Pergunta Humana é realizada na sessão 03. A turma conhece a caverna, Sísifo, CHIROPTERA, Abramović, The Egg e Truman. Esse contexto informa a condução; não constitui um aviso a repetir aos alunos. O enunciado publicado permanece intacto.</p>'
 for n,s in enumerate(sessions,1):
  body+='<section class="c10-stage" id="sessao-'+f'{n:02}'+'"><p class="c10-eyebrow">Sessão '+f'{n:02}'+'</p><h2>'+e(s['title'])+'</h2><p>'+e(s['product'])+'</p>'
  if s.get('prior'):body+='<p>Recursos de uma sessão anterior; sem nova tarefa avaliada. Mobilizar observações e notas quando necessário.</p>'
  else:body+='<ol>'+''.join('<li>'+e(l)+' · '+str(t)+' min</li>' for l,t in zip(s['labels'],s['times']))+'</ol><p>'+e(s['teacher'])+'</p>'
  body+=link(path,f'cidadania/m1/sessoes/{n:02}/','Abrir sessão →')+'</section>'
 write(path,document(path,'Guia das dez sessões',body))
 # Reutilizar todas as ligações da biblioteca, com menos informação simultânea.
 path='cidadania/m1/biblioteca/index.html';source=(R/path).read_text('utf-8')
 groups=re.findall(r'<section class="m1-block"><h2>(.*?)</h2>(.*?)</section>',source,re.S)
 titles=['Olhar e interpretar','Liberdade e ação','Justiça','Direitos e vozes','Decidir em conjunto','Investigar e escrever','História do teatro','Materiais para imprimir']
 body='<header class="c10-hero"><div><p class="c10-eyebrow">Módulo 1</p><h1>Biblioteca</h1><p class="c10-deck">Escolhe o apoio de que precisas.</p></div>'+image(path,dict(image='leitura.webp',caption='Johannes Vermeer · Rapariga a ler uma carta à janela'))+'</header>'
 for i,(title,content) in enumerate(groups):body+='<details class="c10-library-group"><summary><span>'+f'{i+1:02}'+'</span>'+e(titles[i] if i<len(titles) else title)+'</summary><div>'+content+'</div></details>'
 body+='<footer class="c10-support">'+link(path,'cidadania/m1/','Voltar às sessões')+link(path,'cidadania/m1/percurso-anterior.html','Percurso anterior completo')+'</footer>'
 write(path,document(path,'Biblioteca de M1',body))
 path='cidadania/m1/oficina-guiao/index.html'
 # 27/10/2026: a oficina de argumento e guião acompanha as sessões 04 a 10 (não é a tarefa
 # Pergunta Humana): o caminho, um argumento-exemplo, a mesma cena em três formatos, revisão e apresentação.
 from cidadania_m1_molde import ARGUMENTO_EXEMPLO,FORMATOS
 body='<header class="c10-hero"><div><p class="c10-eyebrow">Apoio à escrita</p><h1>Argumento e guião</h1><p class="c10-deck">Uma história. Um formato. Escolhas que se podem explicar.</p></div>'+image(path,dict(image='leitura.webp',caption='Johannes Vermeer · Rapariga a ler uma carta à janela'))+'</header>'
 body+='<section class="c10-reference"><h2>O caminho da oficina</h2><p>Da primeira cena ao guião comentado, cada sessão deixa uma peça escrita. Guarda todas as versões: a mudança entre elas também se explica.</p><ol class="c10-path">'
 for n in range(4,11):
  s=sessions[n-1];body+='<li><a href="'+rel(path,f'cidadania/m1/sessoes/{n:02}/')+'"><b>'+f'{n:02}'+'</b><span>'+e(s['title'])+'</span></a><small>'+e(s['product'])+'</small></li>'
 body+='</ol></section>'
 body+='<section class="c10-reference"><h2>1. O argumento narrativo</h2><p>O argumento conta a história por ações, em poucas linhas, antes de escreveres falas. Não confundas com o argumento que sustenta uma posição: aqui, a palavra quer dizer o enredo.</p><dl class="c10-steps">'+''.join('<dt>'+e(k)+'</dt><dd>'+e(v)+'</dd>' for k,v in ARGUMENTO_EXEMPLO)+'</dl><p class="c10-credit">Exemplo escrito para este apoio.</p><p>Testa o teu: a escolha muda alguma coisa? A consequência nasce do que as personagens fizeram?</p></section>'
 body+='<section class="c10-reference"><h2>2. A mesma cena em três formatos</h2><p>Escolhe teatro, cinema ou áudio e explica porquê. A mesma situação pede escolhas diferentes: o que no cinema se vê, no áudio tem de se ouvir.</p><div class="c10-formats">'
 for nome,regras,cena,pergunta in FORMATOS:
  body+='<article><b>'+e(nome)+'</b><ul>'+''.join('<li>'+e(r)+'</li>' for r in regras)+'</ul><div class="c10-document c10-script">'+e(cena)+'</div><p class="c10-small">Rever: '+e(pergunta)+'</p></article>'
 body+='</div><p class="c10-credit">Cena escrita para este apoio.</p></section>'
 body+='<section class="c10-reference"><h2>3. Da cena ao guião inteiro</h2><ul class="c10-checks"><li>Cada cena responde a três perguntas: quem quer o quê, o que impede, o que muda.</li><li>Há uma decisão contestada e as suas consequências veem-se em cena.</li><li>As indicações de ação, pausa ou som têm uma função.</li><li>As cenas ligam-se: ninguém aparece ou desaparece sem razão.</li><li>Duas passagens ficam assinaladas para rever.</li></ul></section>'
 body+='<section class="c10-reference"><h2>4. Citar e distinguir</h2><p>Identifica autor ou entidade, título, data, ligação e página, secção ou minuto. Distingue citação, paráfrase e criação. Não atribuas falas inventadas a autores ou pessoas reais.</p></section>'
 body+='<section class="c10-reference"><h2>5. Rever com outra pessoa</h2><ol class="c10-tasks"><li>O colega resume conflito, decisão e consequência sem a tua explicação.</li><li>Aponta uma passagem clara e uma que precisa de revisão.</li><li>Regista duas alterações: antes, depois e razão.</li></ol></section>'
 body+='<section class="c10-reference"><h2>6. Apresentar e comentar</h2><p>Na sessão 10, o guião fica à vista e o grupo explica as escolhas. Não é preciso encenar, filmar ou gravar.</p><div class="c10-document">'+e(api['FICHAS'][17]['sample'])+'</div><p>Cada pessoa identifica um contributo seu. Às perguntas dos colegas, responde com uma passagem ou uma razão.</p></section>'
 body+='<footer class="c10-support">'+link(path,'cidadania/m1/','Voltar às sessões')+link(path,'cidadania/projeto/','Enunciado da Pergunta Humana')+'</footer>'
 write(path,document(path,'Argumento e guião',body))
