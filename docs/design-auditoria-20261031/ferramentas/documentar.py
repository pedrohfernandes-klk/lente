"""31/10/2026: monta documentos e estudos visuais, nunca páginas do sítio."""
from pathlib import Path
import json,html,re,shutil
OUT=Path(__file__).resolve().parents[1]
def esc(s):return html.escape(str(s))
def write(p,s):
 p=OUT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf8')
def load(p):return json.loads((OUT/p).read_text(encoding='utf8'))
BASECSS='''body{margin:0} .doc-meta{padding:16px 24px;background:#e8e6df;color:#222;font:13px/1.5 Arial} .spec{margin:48px 0;padding-top:24px;border-top:2px solid var(--cz-ink)} .spec>h2{font:400 32px/1.1 var(--cz-font-poster);margin:0 0 16px}.spec-note{font:13px/1.5 Arial;color:var(--cz-muted);max-width:80ch}.states{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}.state{min-width:0;padding:16px;background:var(--cz-paper)}.state>h3{font:700 13px/1.4 Arial;margin:0 0 16px}.state .cz-next{margin:0}.opening{display:grid;grid-template-columns:7fr 5fr;gap:40px;align-items:start}.opening .cz-next{margin-top:0}.reserve{min-height:56px;display:flex;align-items:center;font:13px/1.4 Arial;padding:16px 24px;border-bottom:1px solid var(--cz-muted);background:var(--cz-paper);color:var(--cz-muted)}details.proposal-unit{margin:8px 0;background:var(--cz-paper);padding:0 16px}details.proposal-unit>summary{min-height:88px;display:flex;align-items:center;justify-content:space-between;font-weight:bold;cursor:pointer}details.proposal-unit>summary::after{content:'+';font-size:24px}details.proposal-unit[open]>summary::after{content:'−'}@media(max-width:899px){.states,.opening{grid-template-columns:1fr}.opening{gap:0}}@media print{.doc-meta,.reserve{display:none}.spec{break-before:page}.states{grid-template-columns:repeat(2,minmax(0,1fr))}}'''
BASECSS+='''@media print{.spec{margin:0;padding-top:16px;break-before:page}.spec>h2{margin:0 0 12px}.states{gap:16px}.state{padding:8px;break-inside:avoid}.state>h3{margin:0 0 8px;break-after:avoid}.spec .cz-button{display:inline-flex}.spec .cz-crumbs{display:flex}.spec .cz-footer-links{display:grid}.spec .cz-door>a{min-height:96px;padding:16px}.spec .cz-next{padding:16px}.spec .cz-next h2{font-size:20px}.spec .cz-next p{margin-bottom:8px}.spec .cz-quote{padding:16px;margin:8px 0}.spec .cz-footer{margin-top:16px;padding:16px}}'''
def shell(title,body,css='appearance.css',extra='',theme=True):
 return f'''<!doctype html><html lang="pt-PT" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><link rel="stylesheet" href="{css}"><link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet"><style>{BASECSS}{extra}</style><script>document.documentElement.dataset.theme=new URLSearchParams(location.search).get('tema')==='escuro'?'dark':'light';if(new URLSearchParams(location.search).has('projetar'))document.documentElement.classList.add('em-projecao');</script></head><body data-cartaz="2">{body}</body></html>'''
def row(n,title,state='',cls=''):
 status=f'<span class="cz-state {"done" if state.startswith("Feita") else "current"}">{state}</span>' if state else '<span></span>'
 return f'<a class="cz-row {cls}" href="#destino"><span>{n:02}</span><span><strong>{esc(title)}</strong><small>Lê, observa e escolhe o teu caminho.</small></span>{status}<span class="arrow" aria-hidden="true">→</span></a>'
def nextblock(title='A forma da história',label='A seguir',action='Continuar',disabled=False):
 return f'<section class="cz-next"><p class="cz-label">{label}</p><h2>{esc(title)}</h2><p class="cz-prose">Retoma a leitura no ponto em que ficaste.</p><button class="cz-button primary" {"disabled" if disabled else ""}>{action}<span aria-hidden="true">→</span></button></section>'
def library():
 states=[('Normal',''),('Sobrevoo','is-hover'),('Foco de teclado','is-focus'),('Pressionado','is-active'),('Visitado','is-visited')]
 sections=[]
 def spec(title,note,items):sections.append(f'<section class="spec"><h2>{title}</h2><p class="spec-note">{note}</p><div class="states">'+''.join(f'<div class="state"><h3>{name}</h3>{content}</div>' for name,content in items)+'</div></section>')
 spec('01 / Ligações na leitura','Georgia 16/24,8 px; linha até 65 ch; sublinhado de 1 px a 0,2 em. Sobrevoo de 2 px. Foco de 3 px, afastado 4 px. Visitado com sublinhado duplo, nunca com mostarda. Exceção de alvo apenas em frases corridas.',[(name,f'<p class="cz-prose">Podes <a class="{cls}" href="#destino">ler a obra</a> antes de continuar.</p>') for name,cls in states])
 spec('02 / Ligações em cartões e listas','Todo o cartão acionável é uma única ligação; sem ligações aninhadas. A seta não é outro alvo. Mínimo 64 px nas linhas e 160 px nos cartões. Visitar não equivale a concluir.',[(name,row(1,'Dar forma a uma história',cls=cls)) for name,cls in states]+[('Destino indisponível','<p class="cz-prose">Dar forma a uma história<br><strong>Indisponível</strong></p>')])
 spec('03 / Créditos e fontes','Arial 13/19,5 px; cinzento #444 / #b3b1aa; alvo autónomo de 44 px; sem sublinhado em repouso; ↗ apenas para outro sítio. A licença permanece texto visível. Foco e sobrevoo distinguem a ligação.',[(name,f'<p class="cz-credit"><a class="{cls}" href="https://commons.wikimedia.org/wiki/File:Blake_manuscript_-_Notebook_25_-_Tyger_-_1st_draft.jpg">Wikimedia Commons <span aria-hidden="true">↗</span></a><br>Domínio público.</p>') for name,cls in states]+[('Fonte em falta','<p class="cz-credit">Origem por confirmar. Não publicar a imagem.</p>')])
 spec('04 / Botões e «Continuar»','Arial 700, 16/24 px; altura mínima 48 px; espaço interno 8 × 24 px; contorno 2 px. Primário só dentro da região «A seguir». Ligação para navegar, button para agir. Estados de visita não se aplicam a botões.',[(name,f'<section class="cz-next"><button class="cz-button primary {cls}">Continuar →</button></section><button class="cz-button {cls}">Rever a leitura</button>') for name,cls in states[:4]]+[('Indisponível','<button class="cz-button primary" disabled>Continuar</button><p class="cz-credit">Escolhe uma resposta para continuar.</p>'),('Em curso','<button class="cz-button" disabled aria-busy="true">A guardar…</button>')])
 spec('05 / Portas','Corpo como alvo integral. Título Bebas Neue 39/41 px; corpo Georgia 16/24,8 px; 24 px de espaço interno; 24 px entre portas. Três colunas acima de 900 px. Créditos fora da ligação principal. Na dobra, banda 88 px com controlo mínimo 48 px.',[(name,f'<article class="cz-door"><a class="{cls}" href="#destino"><span class="cz-label">01 / Laboratório</span><h2>Observar</h2><span class="cz-prose">Como os outros fizeram.</span><span class="arrow">→</span></a></article>') for name,cls in states]+[('Dobrado / aberto','<details class="proposal-unit"><summary>Observar: seis percursos</summary>'+row(1,'Dar forma a uma história')+'</details>')])
 spec('06 / Percurso e progresso','64 px de altura mínima, crescimento com o texto; 16 px de espaço interno; separação 2 px; número 32 px; coluna de estado desce abaixo de 420 px. A data só aparece quando existe no registo. Nunca inventar uma data antiga.',[('Sem registo',row(1,'A forma da história')),('Atual',row(2,'A pirâmide de Freytag','A seguir','current')),('Concluído com data',row(3,'História e enredo','Feita 31/10')),('Concluído sem data',row(4,'O desenlace','Feita')),('Foco e concluído',row(5,'A espinha da história','Feita 31/10','is-focus')),('Foco e atual',row(6,'Começar pelo meio','A seguir','current is-focus'))])
 spec('07 / Região «A seguir»','Uma só por página, invertida entre temas; 24 px de espaço interno; título 25/30 px; corpo 16/24,8 px; botão 48 px. Sem animação. Mesma estrutura para início, retoma, conclusão e indisponibilidade. As várias instâncias nesta prancha são amostras, não uma composição de página.',[('Sem progresso',nextblock(label='Começa aqui',action='Começar')),('Com progresso',nextblock()),('Percurso concluído',nextblock(title='Percurso concluído',label='Feito',action='Rever')),('Sem destino válido',nextblock(title='Escolhe um percurso',label='A seguir',action='Continuar',disabled=True)),('Projeção',nextblock(title='A forma da história',label='Na sala',action='Abrir a leitura')),('Data ultrapassada','<section class="cz-next"><p class="cz-label">Na sala</p><h2>Foi a 28/10</h2><p>Consulta o encontro e prepara o seguinte.</p></section>')])
 spec('08 / Migalhas','Arial 13/19,5 px; 8 px entre níveis; alvos 44 px. O último nível é texto com aria-current. Este componente vive no conteúdo, se a barra não o fornecer; nunca duplicar os dois.',[(name,f'<nav class="cz-crumbs" aria-label="Onde estás"><a class="{cls}" href="#destino">Lente</a><span aria-hidden="true">›</span><a class="{cls}" href="#destino">Laboratório</a><span aria-hidden="true">›</span><span aria-current="page">Observar</span></nav>') for name,cls in states[:3]])
 img='../../../assets/laboratorio/blake-tyger.webp'
 museum=f'<figure class="cz-museum"><img src="{img}" alt="Rascunho manuscrito de The Tyger, com versos riscados e emendas."><figcaption class="cz-credit">William Blake<br><cite>Primeiro rascunho de The Tyger</cite><br>Antes da publicação de 1794<br>British Library, Add MS 49460<br><a href="https://commons.wikimedia.org/wiki/File:Blake_manuscript_-_Notebook_25_-_Tyger_-_1st_draft.jpg">Wikimedia Commons ↗</a><br>Domínio público.</figcaption></figure>'
 spec('09 / Tabela de museu','Imagem sem recorte neste exemplo; legenda adjacente a 8 px; texto 13/19,5 px, alinhado à esquerda. Campos: autor, obra, data, instituição, origem e licença. A informação continua visível se a imagem falhar.',[('Imagem e crédito',museum),('Imagem indisponível','<figure class="cz-museum"><p class="cz-notice">A imagem não está disponível.</p><figcaption class="cz-credit">William Blake, <cite>Primeiro rascunho de The Tyger</cite>, antes de 1794. British Library. Domínio público.</figcaption></figure>'),('Imagem ampliável','<p class="cz-prose">A ampliação tem alvo próprio de 48 px, nome acessível e regresso pelo teclado.</p><button class="cz-button">Ampliar a imagem +</button>')])
 spec('10 / Citações e excertos','Georgia 20/31 px na citação breve; texto longo 16/24,8 px, máximo 65 ch; 24 px de espaço interno; origem 13 px. Aspas portuguesas e título da obra em itálico. Sem justificação em colunas de crédito.',[('Citação breve','<figure class="cz-quote"><blockquote>«O poeta é um fingidor.»</blockquote><figcaption class="cz-credit">Fernando Pessoa, <cite>Autopsicografia</cite>, 1931. Texto em domínio público.</figcaption></figure>'),('Excerto longo','<article class="cz-quote"><p class="cz-prose">O excerto conserva a divisão em parágrafos e a pontuação da edição usada. As notas aparecem depois do texto, com a mesma medida de linha.</p><p class="cz-credit">Exemplo de composição, sem transcrição de uma obra.</p></article>')])
 spec('11 / Avisos','16 × 24 px; faixa a tinta de 4 px; título e mensagem explícitos; sem vermelho ou mostarda decorativos. Informação estática sem role=alert; erro após ação com role=alert; confirmação com role=status.',[('Informação','<aside class="cz-notice"><strong>Neste aparelho</strong>O teu progresso fica guardado aqui.</aside>'),('Erro','<aside class="cz-notice" role="alert"><strong>Não foi possível guardar</strong>Tenta de novo. A tua resposta continua visível.</aside>'),('Confirmação','<aside class="cz-notice" role="status"><strong>Registo guardado</strong>Podes continuar.</aside>')])
 footer='<footer class="cz-footer"><h2>Daqui também se vai</h2><div class="cz-footer-links">'+''.join(f'<a href="#destino">{x} <span>→</span></a>' for x in ['Biblioteca','Cidadania','Laboratório','Português'])+'</div><p class="cz-credit">O teu progresso fica neste aparelho.</p></footer>'
 spec('12 / Rodapé','Uma região de papel; 24 px de espaço interno; saídas 64 px; grelha 4 × 1, passando a 2 × 2 abaixo de 900 px. As ligações herdam foco de 3 px e contorno no sobrevoo. Sem estados pessoais na projeção.',[('Quatro destinos',footer)])
 body='<div class="doc-meta">GPT3 / Proposta para decisão / 31/10/2026 / <a href="?tema=claro">Claro</a> / <a href="?tema=escuro">Escuro</a></div><main class="cz-wrap"><p class="cz-label">Português + Lente / Cartaz</p><h1 class="cz-title">Uma linguagem.<br>Doze peças.</h1><p class="cz-prose">Biblioteca visual para a ronda do docente e da direção de arte. As amostras de sobrevoo, foco, pressionado e visitado estão fixadas para comparação. Não gravam progresso.</p>'+''.join(sections)+'<p id="destino" class="cz-notice">Destino de demonstração. Nenhum registo foi alterado.</p></main>'
 write(Path('proposta/biblioteca.html'),shell('Cartaz / Biblioteca de peças',body))

def proposals():
 pages=load(Path('paginas.json'))
 for p in pages:
  f=OUT/'medidas'/f"{p['id']}-390-light.json"
  if not f.exists():continue
  m=json.loads(f.read_text(encoding='utf8'))
  actions=[a for a in m['links'] if not any(s in a['selector'] for s in ['projection','appearance']) and a['text'] and not any(s in a['text'] for s in ['Mapa','Commons','Ampliar','Guardar','Repor'])]
  first=next((a for a in actions if re.search(r'Começar|Continuar|Seguinte|Começa',a['text'])),actions[0] if actions else {'text':p['title']})
  chosen=[]
  for a in actions:
   text=re.sub(r'\s*(POR FAZER|A SEGUIR|→|↗)\s*',' ',a['text']).strip()
   if text!=first['text'] and text not in chosen and len(text)<100 and not re.search(r'folha|ficha|jogo|jogar|professor',text,re.I):chosen.append(text)
  names=(chosen+[p['title'],'Consulta o percurso','Rever a leitura'])[:3]
  deck=p['id'] in ['peca','licao','sessao']
  title=m['h1'][0]['text'] if m['h1'] else p['title']
  config={
   'pt':('Português','Ler com atenção. Relacionar ideias. Experimentar outras vozes.','Escolhe o teu módulo',['1.º ano','2.º ano','3.º ano']),
   'lente':('Lente.','Olhar, experimentar e dar forma ao que pensas.','Escolhe um percurso',['Cidadania','Laboratório','Ferramentas']),
   'lab':('Laboratório','Observa uma escolha, experimenta uma regra e cria uma peça tua.','A forma da história',['Observar','Treinar','Criar']),
   'ver':('Observar','Como os outros fizeram. Porque é que resulta?','A forma da história',['Observar 1: Dar forma a uma história','Observar 2: Conhecer uma personagem','Observar 3: Ler o que não se diz']),
   'treinar':('Treinar','Uma regra de cada vez. Que escolha queres treinar?','Sem olhos',['Descrever com os sentidos','Fazer falar sem explicar','Dar uma voz à personagem']),
   'criar':('Criar','Uma peça, com palavras e imagens. Como levas uma ideia mais longe?','Escrever ficção: o começo',['Construir uma ficção','Construir com palavras e imagens','Transformar uma forma conhecida']),
   'percurso':('Observar 1: Dar forma a uma história','Que forma tem uma história, por baixo do que conta?','A forma da história',['A forma da história','A pirâmide de Freytag','História e enredo']),
   'cidadania':('Cidadania','Direitos, escolhas e vida em comum.','Ser-se humano',['Humanos','Algoritmos','Dilemas']),
   'piloto':('Ser-se humano','Direitos humanos, democracia e instituições políticas.','Um mapa de direitos',['Um mapa de direitos','A imagem dos outros','Quem tem lugar?']),
   'biblioteca':('Biblioteca','Ler, escutar e descobrir outras vozes.','Ondas do mar de Vigo',['Cantiga de amigo','Poesia','Prosa']),
   'atlas':('Atlas Lusófono','Pessoas, obras e lugares. Quem vais conhecer a seguir?','Uma imagem também se lê?',['Olhar','Escutar','Pessoas por país']),
   'exame':('Da leitura à resposta','Aquecer no ecrã, escrever no papel, rever com critérios.','Escolhe uma sessão',['Ler','Escrever','Rever'])}
  lead='Lê com atenção e avança ao teu ritmo.' if deck else 'Escolhe por onde começar. O percurso mostra-te o que vem a seguir.'
  target=re.sub(r'^(Começar|Continuar):\s*','',first['text']).replace('→','').strip()
  if p['id'] in config:title,lead,target,names=config[p['id']]
  if p['id'].startswith('m') and p['id'][1:].isdigit():
   source=OUT.parents[2]/p['url'].lstrip('/')/'index.html'
   headings=[html.unescape(re.sub('<[^>]+>','',s)).strip() for s in re.findall(r'<h2[^>]*>(.*?)</h2>',source.read_text(encoding='utf8'),re.S)]
   names=[n for n in headings if n!='Arquivo anterior'][:3]
   lead=f'Módulo {p["id"][1:]}. Lê, relaciona e constrói a tua resposta.'
  note='Estudo de composição, sem aplicação. Recorte das três mudanças propostas; não representa a página inteira nem suprime conteúdos. A altura reservada de 56 px é uma hipótese de ensaio, a confirmar com a equipa da barra.'
  reserve='' if deck else '<div class="reserve">Espaço de ensaio para a barra comum / desenho a cargo da equipa</div>'
  opening=f'<div class="opening"><header><p class="cz-label">{"Português" if p["url"].startswith("/pt/") else "Lente"} / {"Leitura" if deck else "Percurso"}</p><h1 class="cz-title">{esc(title)}</h1><p class="cz-prose">{esc(lead)}</p></header>{nextblock(target,action="Seguinte" if deck else "Continuar")}</div>'
  if deck:
   content='<figure class="cz-quote"><blockquote>Leitura com espaço para pensar.</blockquote><figcaption class="cz-credit">Amostra tipográfica. O texto da lição será preservado na implementação.</figcaption></figure><aside class="cz-notice"><strong>Uma ação de cada vez</strong>A casca conserva a navegação, os segmentos e as respostas. O ecrã final recebe a mesma peça «A seguir».</aside>'
  elif p['id'].startswith('m') and p['id'][1:].isdigit() or p['id'] in ['ver','treinar','criar','piloto']:
   content=''.join(f'<details class="proposal-unit" {"open" if i==0 else ""}><summary>{esc(n[:80])}</summary>{row(i+1,"Retomar a leitura","A seguir" if i==0 else "", "current" if i==0 else "")}</details>' for i,n in enumerate(names))
  elif p['id']=='percurso':content=''.join(row(i+1,n,'A seguir' if i==0 else '', 'current' if i==0 else '') for i,n in enumerate(names))
  else:content='<div class="cz-grid">'+''.join(f'<article class="cz-door"><a href="#destino"><span class="cz-label">{i+1:02} / Percurso</span><h2>{esc(n)}</h2><span class="cz-prose">Abre e escolhe o próximo passo.</span><span class="arrow">→</span></a></article>' for i,n in enumerate(names))+'</div>'
  if p['id']=='lente':opening=opening.replace('class="cz-title"','class="cz-title" style="font-family:Arial,Helvetica,sans-serif;font-weight:700;letter-spacing:-.05em"')
  if p['id']=='lab':
   museums=[('William Blake','Primeiro rascunho de The Tyger','Antes de 1794','British Library, Add MS 49460','Domínio público.'),('Edgar Degas','Bailarinas a ensaiar na barra','1877','Metropolitan Museum of Art','CC0.'),('El Lissitzky','Bate os Brancos com a cunha vermelha','1919 a 1920','Biblioteca Estatal Russa','Domínio público.')]
   sources=[a['href'] for a in m['links'] if a.get('href') and 'commons.wikimedia' in a['href']]
   content='<div class="cz-grid">'
   for i,(im,meta,name) in enumerate(zip(m['images'],museums,names)):
    author,work,date,institution,licence=meta
    content+=f'<article class="cz-door"><figure class="cz-museum"><img style="height:240px" src="../../../../assets/laboratorio/{esc(im["src"].split("/")[-1])}" alt="{esc(im["alt"])}"><figcaption class="cz-credit" style="min-height:176px">{esc(author)}<br><cite>{esc(work)}</cite><br>{date}<br>{institution}<br><a href="{esc(sources[i])}">Wikimedia Commons ↗</a><br>{licence}</figcaption></figure><a href="#destino"><span class="cz-label">{i+1:02} / Laboratório</span><h2>{name}</h2><span class="cz-prose">{["Como os outros fizeram.","Uma regra de cada vez.","Uma peça, com palavras e imagens."][i]}</span><span class="arrow">→</span></a></article>'
   content+='</div>'
  if p['id'] in ['ver','treinar','criar']:
   im=m['images'][0]
   filename=im['src'].split('/')[-1]
   credit=im['caption'].split('\n')[0]
   source=next((a['href'] for a in m['links'] if a.get('href','') and 'commons.wikimedia' in a['href']),'https://commons.wikimedia.org/')
   content+=f'<figure class="cz-museum" style="max-width:400px;margin-top:24px"><img src="../../../../assets/laboratorio/{esc(filename)}" alt="{esc(im["alt"])}"><figcaption class="cz-credit">{esc(credit)}<br><a href="{esc(source)}">Consultar a origem ↗</a></figcaption></figure>'
  body=reserve+'<main class="cz-wrap">'+opening+content+'<p id="destino" class="cz-credit" style="margin-top:40px">'+esc(note)+'</p></main>'
  if p['id']=='lente':body=body.replace('<h2>Laboratório</h2><span class="cz-prose">Abre e escolhe o próximo passo.</span>','<h2>Laboratório</h2><span class="cz-prose">Observar, Treinar, Criar.</span>')
  write(Path('proposta/paginas')/(p['id']+'.html'),shell(title+' / estudo',body,'../appearance.css'))

if __name__=='__main__':library();proposals()
