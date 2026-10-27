"""Uma abertura, cinco momentos, uma ação seguinte. HTML estático e acessível."""
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
  head='<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+' · M1 · Cidadania</title><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet"><link rel="stylesheet" href="'+assets+'appearance.css"><script src="'+assets+'appearance.js"></script><link rel="stylesheet" href="'+assets+'cidadania-m1-sessoes.css?v=20261027-editorial"><script defer src="'+assets+'cidadania-m1-sessoes.js?v=20261027-editorial"></script>'
  return '<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head>'+head+'</head><body class="c10-body"><main class="c10" data-c10'+(' data-session="'+num+'"' if num else '')+'>'+top(path)+body+'</main><script defer src="'+assets+'projection-launcher.js" data-site="lente"></script></body></html>\n'
 def image(path,s,cls=''):
  return '<figure'+(' class="'+cls+'"' if cls else '')+'><img src="'+rel(path,'img/cidadania/'+s['image'])+'" alt="'+e(s['caption'],quote=True)+'" loading="lazy" decoding="async"><figcaption>'+e(s['caption'])+' · '+link(path,'cidadania/m1/imagens/','Créditos')+'</figcaption></figure>'
 def resource_list(path,s):return '<ul>'+''.join('<li>'+link(path,p,api['source_label'](p.split('#')[0]))+'</li>' for p in s['resources'])+'</ul>'
 def capsule(path,key):
  title,text,task=short_caps[key];sources=capsules[key]['sources']
  return '<aside class="c10-capsule"><p class="c10-eyebrow">História do teatro</p><h3>'+e(title)+'</h3><p>'+e(text)+'</p><p><b>Experimenta.</b> '+e(task)+'</p><details><summary>Fontes</summary><div><ul>'+''.join('<li><a href="'+(e(u,quote=True) if u.startswith('http') else rel(path,'cidadania/m1/passo-06/'))+'">'+e(t)+'</a></li>' for t,u in sources)+'</ul></div></details></aside>'
 (R/'cidadania/projeto/index.html').write_bytes(subprocess.check_output(['git','show',api['BASE']+':cidadania/projeto/index.html'],cwd=R))
 write('cidadania/m1/percurso-anterior.html',old('cidadania/m1/index.html'))
 for n,s in enumerate(sessions,1):
  ident=f'{n:02}';path=f'cidadania/m1/sessoes/{ident}/index.html';labels=s['labels']
  body='<header class="c10-hero" id="abertura" data-session-intro><div><p class="c10-eyebrow">Sessão '+ident+' / 10 · '+e(s['theme'])+'</p><h1>'+e(s['title'])+'</h1><p class="c10-deck">'+e(s['question'])+'</p><a class="c10-action" href="#momento-1" data-start>Começar</a><p class="c10-cover-meta">5 momentos · 3 horas</p></div>'+image(path,s)+'</header>'
  body+='<div data-session-flow><div class="c10-flow-head"><p class="c10-eyebrow">Sessão '+ident+' · '+e(s['title'])+'</p><a href="#abertura" data-cover-link>Ver abertura</a></div><nav class="c10-stagebar" aria-label="Cinco momentos da sessão">'+''.join('<a href="#momento-'+str(i+1)+'" data-stage-link aria-label="'+str(i+1)+'. '+e(label,quote=True)+'"><b>'+f'{i+1:02}'+'</b><span>'+e(label)+'</span></a>' for i,label in enumerate(labels))+'</nav>'
  for i,label in enumerate(labels):
   body+='<section class="c10-stage" id="momento-'+str(i+1)+'" data-stage data-label="'+e(label,quote=True)+'" tabindex="-1"><header class="c10-step-heading"><span aria-hidden="true">'+f'{i+1:02}'+'</span><div><p class="c10-eyebrow">'+str(i+1)+' / 5</p><h2>'+e(label)+'</h2></div></header><div class="c10-step-body">'
   text=[s['entry'],s['reading'],'',s['work'],s['close']][i]
   if text:body+='<p class="c10-reading">'+e(text)+'</p>'
   if i==0 and n==3:
    body+='<ol class="c10-evidence" aria-label="Da pergunta à resposta"><li><b>Pergunta</b><span>O que queremos saber?</span></li><li><b>Fonte</b><span>Em que nos apoiamos?</span></li><li><b>Resposta</b><span>O que podemos defender?</span></li></ol>'
   if i==1:
    if n==3:body+='<p>'+link(path,'cidadania/projeto/','Abrir o enunciado →')+'</p>'
    if n in image_prompts:body+='<div class="c10-image-study">'+image(path,s)+'<p>'+e(image_prompts[n])+'</p></div>'
    if s['numbers']:
     sample=api['FICHAS'][s['numbers'][0]-1]['sample']
     body+='<div class="c10-document">'+e(sample)+'</div><p class="c10-credit">Exemplo didático · redação do LENTE</p>'
    if s.get('capsule'):body+=capsule(path,s['capsule'])
    body+='<details><summary>Obras e materiais</summary><div>'+resource_list(path,s)+'</div></details>'
   if i==2:body+='<ol class="c10-tasks">'+''.join('<li>'+e(t)+'</li>' for t in s['tasks'])+'</ol><details data-feedback><summary>Comparar razões</summary><div><p>'+e(s['feedback'])+'</p></div></details>'
   if i==3:
    body+='<p class="c10-output"><b>Guardar</b><span>'+e(s['product'])+'</span></p>'
    if n>=4:body+='<p>'+link(path,'cidadania/m1/oficina-guiao/','Apoio à escrita →')+'</p>'
   if i==4:
    body+='<ul class="c10-checks">'+''.join('<li>'+e(t)+'</li>' for t in s['criteria'])+'</ul>'
    if not s.get('prior'):body+='<section class="c10-completion" data-completion hidden><label><input type="checkbox" data-session-done>Registar o trabalho revisto</label><p data-live class="c10-small" role="status" aria-live="polite">O registo fica neste aparelho.</p></section>'
   body+='</div></section>'
  next_target=f'cidadania/m1/sessoes/{n+1:02}/' if n<10 else 'cidadania/m1/'
  body+='<nav class="c10-control" data-step-controls aria-label="Avançar na sessão"><button type="button" data-prev hidden>← Anterior</button><span data-position role="status" aria-live="polite"></span><button type="button" data-next hidden>Seguinte →</button><a class="c10-action" href="'+rel(path,next_target)+'" data-next-session hidden>'+('Sessão seguinte' if n<10 else 'Voltar ao percurso')+'</a></nav></div>'
  body+='<noscript><p>Todos os momentos estão disponíveis nesta página. Usa os cinco passos para navegar.</p></noscript><footer class="c10-support">'+link(path,'cidadania/m1/','Todas as sessões')+link(path,'cidadania/m1/biblioteca/','Biblioteca')+link(path,'cidadania/m1/sessoes/#sessao-'+ident,'Guia do docente')+'</footer>'
  write(path,document(path,s['title'],body,ident))
 path='cidadania/m1/index.html';hero=dict(image='hals.webp',caption='Frans Hals · As regentes do asilo de velhos, 1664')
 body='<header class="c10-hero"><div><p class="c10-eyebrow">Cidadania · Módulo 1</p><h1>Ser-se humano</h1><p class="c10-deck">Quem conta como pessoa?</p><a class="c10-action" href="sessoes/03/" data-continue>Continuar · sessão 03</a></div>'+image(path,hero)+'</header><div class="c10-sectionhead"><h2>Dez sessões</h2><p class="c10-small" data-count></p></div><ol class="c10-session-list">'
 for n,s in enumerate(sessions,1):
  thumb='<img class="c10-thumb" src="'+rel(path,'img/cidadania/'+s['image'])+'" alt="" loading="lazy">' if n in (3,6,9) else ''
  body+='<li class="c10-card" data-session-card="'+f'{n:02}'+'"><a href="sessoes/'+f'{n:02}'+'/"><span class="c10-number">'+f'{n:02}'+'</span><div><span class="c10-topic">'+e(s['theme'])+'</span><h3>'+e(s['title'])+'</h3><p>'+e(s['product'])+'</p><small data-status></small></div>'+thumb+'</a></li>'
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
 body='<header class="c10-hero"><div><p class="c10-eyebrow">Apoio à escrita</p><h1>Argumento e guião</h1><p class="c10-deck">Uma história. Um formato. Escolhas que se podem explicar.</p></div>'+image(path,dict(image='leitura.webp',caption='Johannes Vermeer · Rapariga a ler uma carta à janela'))+'</header><section class="c10-reference"><h2>1. Desenvolver o argumento</h2><p>Conta a história por ações: situação inicial, conflito, escolha, viragem e consequência. Um argumento narrativo desenvolve uma história; uma razão sustenta uma posição. Distingue os dois usos da palavra.</p></section><section class="c10-reference"><h2>2. Escolher o formato</h2><div class="c10-formats"><article><b>Teatro</b><p>Personagens, situação e espaço. Falas atribuídas e didascálias de ação, pausa, entrada ou saída.</p></article><article><b>Cinema</b><p>Cabeçalhos de cena: interior/exterior, lugar e momento. Ação no presente, visível ou audível, e diálogos.</p></article><article><b>Áudio</b><p>Vozes identificadas. Marcas de som, silêncio, música e transição. A ação compreende-se sem imagem.</p></article></div></section><section class="c10-reference"><h2>3. Citar e distinguir</h2><p>Identifica autor ou entidade, título, data, ligação e página, secção ou minuto. Distingue citação, paráfrase e criação. Não atribuas falas inventadas a autores ou pessoas reais.</p></section><section class="c10-reference"><h2>4. Rever com outra pessoa</h2><ol class="c10-tasks"><li>O colega resume conflito, decisão e consequência sem a tua explicação.</li><li>Aponta uma passagem clara e uma que precisa de revisão.</li><li>Regista duas alterações: antes, depois e razão.</li></ol></section><footer class="c10-support">'+link(path,'cidadania/m1/','Voltar às sessões')+link(path,'cidadania/projeto/','Enunciado da Pergunta Humana')+'</footer>'
 write(path,document(path,'Argumento e guião',body))
