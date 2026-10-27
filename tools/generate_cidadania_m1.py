"""Gera fichas estáticas de M1 e integra-as sem apagar recursos/estado anteriores.

Executar na raiz: python tools/generate_cidadania_m1.py
Base preservada é explícita; não usa origin/main, que pode avançar após revisão.
"""
from pathlib import Path
from html import escape as e
import json,re,subprocess,posixpath,base64
from urllib.parse import quote
from cidadania_m1_conteudos import FICHAS,UNITS,CAPSULES
R=Path(__file__).resolve().parents[1]
BASE='66dc1b818e6f99ed1b0bddf7b5d4f7b5cca59f0d'
M=R/'cidadania/m1'
def old(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=R).decode('utf-8')
def write(path,s):
 p=R/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def rel(path,target):
 value=posixpath.relpath(target,posixpath.dirname(path))
 return value+'/' if target.endswith('/') and not value.endswith('/') else value
def anchor(path,target,label):return '<a href="'+e(rel(path,target),quote=True)+'">'+e(label)+'</a>'
def root_target(resource):
 # Dados editoriais referem-se a M1, com atalhos explícitos para dependências.
 if resource.startswith('../../../'):return resource[9:]
 return posixpath.normpath('cidadania/m1/'+resource)+'/' if not resource.endswith('.pdf') else posixpath.normpath('cidadania/m1/'+resource)
def source_label(target):
 if target.rstrip('/')=='cidadania/projeto':return 'Pergunta Humana · enunciado partilhado'
 if target.rstrip('/')=='cidadania/m1/oficina-guiao':return 'Argumento e guião'
 p=R/target
 if p.is_dir():p=p/'index.html'
 if p.exists():
  m=re.search('<title>(.*?)</title>',p.read_text('utf-8'),re.S)
  if m:return re.split(r' · |, com Michael',m[1])[0]
 return target
def resources(path,items):
 out=[]
 for v in items:
  target=root_target(v);out.append('<li>'+anchor(path,target,source_label(target))+'</li>')
 return '<ul>'+''.join(out)+'</ul>'
def nav(path):
 projection=rel(path,'projetar/')+'?pagina='+quote('/lente/'+posixpath.dirname(path)+'/',safe='')
 return '<nav class="m1-nav" aria-label="Navegação de Cidadania">'+anchor(path,'cidadania/m1/','Módulo 1')+anchor(path,'cidadania/projeto/','Projeto e critérios')+anchor(path,'cidadania/m1/biblioteca/','Biblioteca')+'<button type="button" data-m1-print hidden>Imprimir</button><a class="epi-projection-menu-link" href="'+projection+'">Projetar</a></nav>'
def main(path,body,ident=''):
 return '<main class="m1-v2" data-m1-v2'+(' data-ficha="'+ident+'"' if ident else '')+'><a class="m1-skip" href="#m1-conteudo">Ir para o conteúdo</a>'+nav(path)+'<div id="m1-conteudo">'+body+'</div></main>'
def assets(path):
 return '<link rel="stylesheet" href="'+rel(path,'assets/cidadania-m1.css')+'?v=20261027-molde-1"><script defer src="'+rel(path,'assets/cidadania-m1.js')+'"></script>'
def shell(path,title,body):
 return '<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+' · Cidadania · Lente</title><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet"><link rel="stylesheet" href="'+rel(path,'assets/appearance.css')+'"><script src="'+rel(path,'assets/appearance.js')+'"></script>'+assets(path)+'</head><body class="m1-sheet">'+body+'<script defer src="'+rel(path,'assets/projection-launcher.js')+'" data-site="lente"></script></body></html>\n'
def wrap(path,body,aliases=()):
 s=old(path);s=s.replace('</head>',assets(path)+'</head>')
 if path=='cidadania/projeto/index.html':s=re.sub(r'<title>.*?</title>','<title>SER-SE HUMANO · Projeto · Cidadania</title>',s,count=1)
 # Preservar todos os scripts e o corpo antigo no mesmo endereço evita quebrar
 # caminhos relativos. Âncoras de critérios passam para o enunciado vigente.
 m=re.search(r'<body\b[^>]*>',s);end=s.rfind('</body>');legacy=s[m.end():end]
 for ident in aliases:legacy=legacy.replace('id="'+ident+'"','id="arquivo-'+ident+'"')
 notice='<p class="m1-archive-note">Arquivo do percurso anterior. Os conteúdos, registos e materiais mantêm-se disponíveis. As datas e exigências de teatro-documento aqui reproduzidas pertencem à versão anterior; o enunciado vigente está no início desta página e em Projeto e critérios.</p>'
 s=s[:m.end()]+body+'<details class="m1-archive" id="arquivo-anterior"><summary>Consultar o percurso e os materiais anteriores</summary>'+notice+legacy+'</details>'+s[end:]
 write(path,s)

def ficha(n):
 f=FICHAS[n-1];u=(n-1)//3;ident=f'F{n:02}';path=f'cidadania/m1/fichas/{ident.lower()}/index.html'
 body=f'<p class="m1-kicker">Apoio {n:02} · {UNITS[u][0]} · Ser-se humano</p><h1>{e(f["title"])}</h1><p class="m1-lead">{e(f["question"])}</p><section class="m1-reading" aria-label="Contexto"><p>{e(f["context"])}</p></section>'
 if 'capsule' in f:
  c=CAPSULES[f['capsule']];links=[]
  for label,url in c['sources']:
   if not url.startswith('http'):url=rel(path,'cidadania/m1/passo-06/')
   links.append('<li><a href="'+e(url,quote=True)+'">'+e(label)+'</a></li>')
  body+='<section class="m1-block" data-capsule="'+f['capsule']+'"><p class="m1-kicker">História do teatro · cápsula integrada</p><h2>'+e(c['title'])+'</h2><p>'+e(c['text'])+'</p><p><strong>Aplicar à escrita.</strong> '+e(c['task'])+'</p><details><summary>Fontes da cápsula</summary><div><ul>'+''.join(links)+'</ul></div></details></section>'
 body+='<section class="m1-block"><h2>Ler e comparar</h2><p class="m1-note">Exemplo didático redigido para este apoio; casos e obras identificados no contexto. Não é uma citação.</p><div class="m1-sample">'+e(f['sample'])+'</div><ol class="m1-tasks">'+''.join('<li>'+e(t)+'</li>' for t in f['tasks'])+'</ol><details data-feedback><summary>Depois de decidir · comparar razões</summary><div><p>'+e(f['feedback'])+'</p></div></details></section>'
 body+='<section class="m1-block" id="oficina"><p class="m1-kicker">SER-SE HUMANO · oficina de escrita</p><h2>Levar ao guião</h2><p>'+e(f['work'])+'</p><p><strong>Rever.</strong> '+e(f['review'])+'</p><p class="m1-note">Escreve no caderno ou no ficheiro do projeto. Este apoio não cria uma entrega separada.</p></section>'
 body+='<aside class="m1-justice"><h2>Regressar à Justiça</h2><p>'+e(f['justice'])+'</p>'+anchor(path,'cidadania/m1/#unidade-3','Retomar a unidade central')+'</aside>'
 body+='<details><summary>Fontes e recursos completos</summary><div>'+resources(path,f['resources'])+'<p>'+anchor(path,'cidadania/m1/biblioteca/','Biblioteca completa: obras, fontes, créditos e materiais anteriores')+'</p><p class="m1-note">Contextualização e exemplos: síntese didática do LENTE. As fontes originais permitem aprofundar e verificar; uma ligação não implica visionamento integral obrigatório.</p></div></details>'
 body+='<section class="m1-progress" data-m1-storage hidden aria-label="Registo pessoal"><label><input type="checkbox" data-m1-done="'+ident+'">Registei e revi este trabalho no meu caderno ou projeto.</label><p class="m1-live" data-m1-live role="status" aria-live="polite">Este registo fica neste aparelho. Não é uma classificação automática.</p></section><noscript><p>As tarefas e os apoios podem ser lidos e impressos sem JavaScript. Conserva o registo no caderno.</p></noscript>'
 body+='<nav class="m1-bottom" aria-label="Sequência dos apoios">'+(anchor(path,f'cidadania/m1/fichas/f{n-1:02}/','← Apoio anterior') if n>1 else anchor(path,'cidadania/m1/','← Percurso'))+(anchor(path,f'cidadania/m1/fichas/f{n+1:02}/','Apoio seguinte →') if n<18 else anchor(path,'cidadania/projeto/','Rever a entrega →'))+'</nav>'
 write(path,shell(path,f'Apoio {n:02} · {f["title"]}',main(path,body,ident)))


def library():
 path='cidadania/m1/biblioteca/index.html'
 body='<p class="m1-kicker">Módulo 1 · Biblioteca</p><h1>Obras, fontes e apoios</h1><p class="m1-lead">As sessões escolhem o essencial. Aqui encontras os materiais completos.</p><p>'+anchor(path,'cidadania/projeto/','Pergunta Humana: consultar o enunciado já partilhado')+'. Os recursos e registos existentes mantêm-se disponíveis. A oficina de argumento e guião desenvolve a escrita nas sessões seguintes.</p><p>'+anchor(path,'cidadania/m1/percurso-anterior.html','Consultar o percurso anterior completo')+'</p>'
 groups=[('Ver, interpretar e construir perspetivas',['passo-00/','passo-02/','cid-m1-duas-legendas/','imagens/','../../aula-1/']),('Liberdade e ação · Truman, Sísifo, Camus, Stanislavski e Actors Studio',['passo-01/','passo-04/','passo-05/','cid-m1-vida-em-direto-hoje/','../../aula-2/']),('Justiça · Sandel, prova e decisão',['../../../olhar-e-decidir/justica/','../../../olhar-e-decidir/justica/licao-1/','../../../olhar-e-decidir/justica/licao-2/','../../../olhar-e-decidir/justica/licao-3/','../../../olhar-e-decidir/justica/aplicar/','../../../olhar-e-decidir/justica/guiao/','cid-m1-o-juri/','passo-06/']),('Direitos e vozes · The Egg, Shakespeare, Sarah Kane, Butler e Singer',['passo-03/','passo-08/','cid-m1-butler-singer/','cid-m1-quem-tem-lugar/','cid-m1-guardar-ou-partilhar/']),('Autoridade e deliberação · Pinter, Doze Homens, Sylvia e CHIROPTERA',['passo-07/','passo-09/','guiao-2/']),('Escrever, investigar e rever',['abertura/','passo-10/','oficina/','glossario/','revisao/','verificar/','guiao-1/','ensaio-1/','ensaio-2/'])]
 # Os diários estão em cidadania/aula-1 e aula-2, um nível acima de M1.
 groups=[(title,[v.replace('../../aula-','../aula-') for v in items]) for title,items in groups]
 for title,items in groups:body+='<section class="m1-block"><h2>'+e(title)+'</h2>'+resources(path,items)+'</section>'
 body+='<section class="m1-block"><h2>História do teatro · quatro cápsulas</h2><ul>'
 for n in [3,6,14,16]:body+='<li>'+anchor(path,f'cidadania/m1/fichas/f{n:02}/',CAPSULES[FICHAS[n-1]['capsule']]['title'])+'</li>'
 body+='</ul></section><section class="m1-block"><h2>Materiais anteriores para imprimir</h2><ul>'
 # 27/10/2026: nomes legíveis para os PDF (os nomes dos ficheiros mantêm-se; o texto visível evita «ficha»).
 pdf={'Doze_Homens_Ficha_Ensaio':'Doze Homens em Fúria: ensaio','Doze_Homens_Guiao_Investigacao':'Doze Homens em Fúria: guião de investigação','EPI_Cidadania_Guiao_Investigacao':'Guião de investigação de Cidadania','Truman_Show_Ficha_Interpretacao':'The Truman Show: interpretação'}
 for p in sorted((M/'materiais').glob('*.pdf')):body+='<li>'+anchor(path,p.relative_to(R).as_posix(),pdf.get(p.stem,p.stem.replace('_',' ')))+' (PDF original, sem alteração)</li>'
 for p in ['cidadania/ferramentas/m1-aula-01-ficha/','cidadania/ferramentas/m1-aula-01-diapositivos/']:body+='<li>'+anchor(path,p,source_label(p))+'</li>'
 body+='</ul><p>'+anchor(path,'biblioteca/','Biblioteca transversal do LENTE')+'</p></section>'
 write(path,shell(path,'Biblioteca de M1',main(path,body)))


def extract_legacy_css():
 paths=[f'cidadania/m1/passo-{n:02}/index.html' for n in range(11)]
 blocks=re.findall(r'<style\b[^>]*>(.*?)</style>',old(paths[0]),re.S)
 assert len(blocks)==5
 write('assets/cidadania-m1-legado.css','\n'.join(blocks))
 for path in paths:
  s=old(path);assert re.findall(r'<style\b[^>]*>(.*?)</style>',s,re.S)==blocks
  first=True
  def replace(m):
   nonlocal first
   if first:first=False;return '<link rel="stylesheet" href="../../../assets/cidadania-m1-legado.css">'
   ident=re.search(r'\bid="([^"]+)"',m[0])
   return '<style id="'+ident[1]+'"></style>' if ident else ''
  s=re.sub(r'<style\b[^>]*>.*?</style>',replace,s,flags=re.S)
  write(path,s)

def integrations():
 # Acrescentar ligação ao apoio operacional sem alterar o guia transversal.
 p='docente/index.html';s=old(p);marker='<a href="../cidadania/m1/sessoes/">Cidadania M1: guião das dez sessões →</a>'
 s=s.replace('</body>','<div class="m1-teacher-update" style="max-width:68rem;margin:24px auto;padding:20px">'+marker+'</div></body>');write(p,s)
 # O portal conserva imagens, tabelas e ligações, mas a descrição de M1 passa a ser vigente.
 p='cidadania/index.html';s=old(p)
 s=s.replace('Investigar uma pergunta e dar-lhe forma em teatro-documento.','Dez sessões: investigar, discutir e escrever, a partir da Pergunta Humana.').replace('10 passos','10 sessões',1)
 write(p,s)
 # Extrair a imagem já creditada no passo 01, sem editar o bitmap.
 s=old('cidadania/m1/passo-01/index.html');m=re.search(r'itens:(\[)',s);bank=json.JSONDecoder().raw_decode(s[m.start(1):])[0]
 im=re.search(r'data:image/(\w+);base64,([^"\s]+)',bank[1]['html'])
 assert im
 ext={'jpeg':'jpg'}.get(im[1],im[1]);image_path='img/cidadania/wright-experiencia.'+ext
 (R/image_path).write_bytes(base64.b64decode(im[2]))
 p='index.html';s=old(p)
 s=s.replace('https://pedrohfernandes-klk.github.io/lente/img/cidadania/holbein.webp',image_path)
 # Dimensões verificadas do bitmap incorporado na base fixa acima.
 width,height=1100,824
 s=s.replace('style="object-position:50% 25%"',f'style="object-position:50% 45%" width="{width}" height="{height}"')
 credit='<p class="m1-home-credit" style="font-size:.75rem;margin:8px 0 16px">Joseph Wright of Derby, <i>Uma experiência com uma ave numa bomba de ar</i>, 1768 · <a href="https://commons.wikimedia.org/wiki/File:An_Experiment_on_a_Bird_in_an_Air_Pump_by_Joseph_Wright_of_Derby,_1768.jpg">Imagem em domínio público · origem</a></p>'
 needle='<p class="ld-f">Investigar problemas da vida em comum, comparar argumentos e fundamentar decisões.</p>'
 s=s.replace(needle,needle+credit)
 # Especificidade local: apenas a imagem de Cidadania ganha enquadramento largo.
 s=s.replace('</head>','<style id="m1-home-image">#inicio-cidadania{grid-template-rows:auto 1fr}#inicio-cidadania .ld-img{height:auto;aspect-ratio:2.35/1;position:relative}#inicio-cidadania .ld-img img{position:absolute;inset:0;width:100%!important;height:100%!important;object-fit:cover!important;filter:none;object-position:50% 45%!important}#inicio-cidadania .m1-home-credit a{color:inherit;text-underline-offset:3px}@media(max-width:560px){#inicio-cidadania .ld-img{aspect-ratio:1.85/1}}</style></head>')
 s=s.replace('Módulo 1: investigar, compreender e responder.','Módulo 1: dez sessões, da investigação à escrita.')
 s=s.replace('var a=passos("epi-cidadania-m1"),b=passos("epi-cidadania-m2"),T=[11,9]','var novo=ler("lente-cidadania-m1-sessoes-v2"),a=Object.keys(novo.sessions||{}).filter(function(k){return /^(0[3-9]|10)$/.test(k)&&novo.sessions[k]&&novo.sessions[k].done===true}).length,b=passos("epi-cidadania-m2"),T=[8,9]').replace('J=[!!ler("lente-justica-licao-1").lida,','J=[a===8,')
 write(p,s)

if __name__=='__main__':
 assert len(FICHAS)==18 and len(UNITS)==6
 for n in range(1,19):ficha(n)
 # As fichas são apoios; a navegação principal é agora um percurso de dez sessões.
 library();extract_legacy_css();integrations()
 from cidadania_m1_sessoes import build
 build(globals())
 print('Dez sessões geradas. Enunciado publicado de Pergunta Humana preservado; fichas disponíveis como apoio.')
