"""30/10/2026: texto corrido justificado e hifenizado em português europeu (decisão do docente).

O único ficheiro de estilos comum às páginas todas do Lente é assets/appearance.css; a regra vive no fim dele.
Este teste confirma, sem navegador:
- que cada família de páginas carrega a regra (liga appearance.css e tem conteúdo que a regra visa);
- que a regra só mexe no alinhamento e na hifenização, fora de qualquer @media;
- que os versos, os blocos com <br>, os créditos curtos e as caixas de outra natureza ficam fora;
- que as marcações corrigidas para separar verso de prosa continuam no sítio;
- que a língua efetiva é pt-PT, salvo nos textos que declaram a sua.
O estilo calculado no navegador é verificado em tests/browser_texto_justificado.py."""
from pathlib import Path
import json,re,unittest

R=Path(__file__).resolve().parents[1]
CSS=(R/'assets/appearance.css').read_text('utf-8')
MARCA='/* 30/10/2026: texto corrido justificado'

def paginas():
 out=[]
 for p in sorted(R.rglob('*.html')):
  rel=p.relative_to(R).as_posix()
  if rel.split('/')[0] in ('.git','tests','_qa'):continue
  s=p.read_text('utf-8')
  if re.search(r'</head\s*>',s,re.I):out.append((rel,s))
 return out
PAGINAS=paginas()

def sem_comentarios(css):return re.sub(r'/\*.*?\*/','',css,flags=re.S)
def bloco():
 return CSS[CSS.index(MARCA):]
def regras():
 """As regras do bloco, em pares (seletor, declarações)."""
 return [(m.group(1).strip(),m.group(2).strip()) for m in re.finditer(r'([^{}]+)\{([^{}]*)\}',sem_comentarios(bloco()))]
def classes(seletor):return set(re.findall(r'\.([A-Za-z][\w-]*)',seletor))
def argumentos_not(seletor):
 """Conteúdo de cada :not(...), com parênteses equilibrados."""
 out=[];i=0
 while True:
  i=seletor.find(':not(',i)
  if i<0:return out
  j=i+5;n=1
  while n:
   n+={'(':1,')':-1}.get(seletor[j],0);j+=1
  out.append(seletor[i+5:j-1]);i+=5

def familia(rel,s):
 """Família de cada página, como no mapa de 30/10/2026 (29 famílias; todas carregam a regra)."""
 d=rel.split('/');top=d[0]
 if rel in ('narrativas/formas/certa-manha/index.html','narrativas/corta/cena-que-falta/index.html'):return 'L2b'
 if rel in ('narrativas/formas/index.html','narrativas/corta/mesa/index.html'):return 'L3'
 if rel in ('docente/index.html','docente/resultados/index.html','narrativas/fora-da-pagina/index.html'):return 'D1'
 if rel.startswith('narrativas/fora-da-pagina/'):return 'L2a'
 if 'window.EPIJogo' in s:
  if top=='narrativas':return 'L1a'
  if top=='gigantes':return 'L1b'
  if top=='vozes':return 'L1c'
  if top=='cidade':return 'L1d'
  if top=='sidequests':return 'L1e'
  if top in ('ler','direitos','apresentar','investigar','projetos'):return 'L1f'
  if top=='cidadania':return 'L1g'
  return 'L1h'
 if rel.startswith('cidadania/m1/fichas/'):return 'C1'
 if rel.startswith(('cidadania/m1/sessoes/','cidadania/m1/biblioteca/','cidadania/m1/oficina-guiao/')) or rel=='cidadania/m1/index.html':return 'C2'
 if rel.startswith('cidadania/m2/sessoes/'):return 'C3'
 if rel.startswith(('cidadania/m2/aulas/','cidadania/m1/abertura/')):return 'C4'
 if rel.startswith('cidadania/ferramentas/'):return 'C5'
 if rel in ('cidadania/index.html','cidadania/m2/index.html','cidadania/m1/percurso-anterior.html'):return 'C6'
 if top=='cidadania':return 'C7'
 if top=='ver-para-fazer' and len(d)>2:return 'P1'
 if top=='biblioteca' and len(d)>2:return 'P2'
 if rel in ('narrativas/oficina-espaco-imprimir/index.html','dar-forma-as-palavras/index.html'):return 'P3b'
 if re.fullmatch(r'narrativas/oficina-[\w-]+-imprimir/index\.html',rel):return 'P3'
 if rel in ('index.html','narrativas/index.html','vozes/index.html'):return 'E1'
 if len(d)==2 or rel in ('narrativas/corta/index.html','narrativas/margens/index.html'):
  if top not in ('404.html','como','caderno','curadoria','mapa','projetar'):return 'E2'
 if rel.startswith('narrativas/treinar/') or rel=='narrativas/proposta-subtexto/index.html':return 'G1'
 if rel.startswith('olhar-e-decidir/'):return 'J1'
 if re.fullmatch(r'vozes/[\w-]+/guiao/index\.html',rel):return 'V1'
 return 'X'

# Classes que ligam cada família à regra: têm de estar no seletor da regra e numa página da família
# (ou num script local que essa página carrega).
# 30/10/2026: L1c deixa de ter 'vz-vc' (as biografias ficam à esquerda); E2 ganha 'entrada-fontes' e C6 'cid-route-step'
# (texto corrido dentro de details, revisão adversarial).
MARCADORES={
 'L1a':['ler','c-expl','excerto','trad'],'L1b':['ler','c-expl','ap-texto'],'L1c':['ler','c-expl','conceito'],
 'L1d':['ler','c-expl','ap-texto'],'L1e':['ler','c-expl','ap-texto'],'L1f':['ler','c-expl','ap-texto'],
 'L1g':['ler','c-expl','termo'],'L1h':['ler','c-expl','lado-c'],'L2a':['ler'],'L2b':['formas-cartoes','lf-prosa'],
 'L3':['lf-hero','lf-lead'],'P1':['vpf','vpf-porque','vpf-fazer'],'P2':['bib-texto','bib-fonte'],'P3':['pg'],
 'P3b':['comum'],'E1':['p-lead','lab-saiu'],'E2':['p-cab','p-lead','entrada-fontes'],'G1':['pg'],'J1':['comum','lado','caso-im'],
 'V1':['gu'],'C1':['m1-v2','m1-block','m1-sample'],'C2':['c10','c10-reading','c10-instruction'],
 'C3':['c10','c10-document'],'C4':[],'C5':['citacao','nota'],'C6':['p-lead','rodape','cid-route-step'],
 'C7':['pg','termo','citacao'],'D1':['atelier-lead','guide-block','rt-antes'],'X':['pg'],
}
# Páginas sem texto corrido a justificar (carregam a regra, mas nada nelas é texto corrido):
# 30/10/2026: o feed das ferramentas saiu desta lista: as notas longas dentro de details passaram a justificar-se.
SEM_TEXTO_CORRIDO={
 '404.html':'mensagem centrada de duas linhas; o seletor da página nua exclui main com svg à cabeça',
 'index.html':'portal: cartões em mosaico, rótulos e créditos',
 'mapa/index.html':'mapa do sítio: ligações e listas',
 'projetar/index.html':'ferramenta de projeção',
 'caderno/duas-colunas/index.html':'duas colunas de 19 car. por linha (caixa estreita)',
 'cidadania/m1/index.html':'índice em cartões',
 'cidadania/ferramentas/m1-aula-01-diapositivos/index.html':'diapositivos',
 'cidadania/ferramentas/m2-aula-01-diapositivos/index.html':'diapositivos',
 'narrativas/corta/cena-que-falta/index.html':'cartões curtos, opções e feedback curto (cartoes.js)',
}

def scripts_locais(rel,s):
 out=''
 for src in re.findall(r'<script[^>]+src="([^"]+)"',s):
  if src.startswith(('http:','https:','//')):continue
  f=(R/rel).parent/src.split('?')[0]
  if f.is_file():out+=f.read_text('utf-8')
 return out

class FamiliasCarregamARegra(unittest.TestCase):
 def test_bloco_unico_no_fim_e_fora_de_media(self):
  self.assertEqual(CSS.count(MARCA),1)
  antes=sem_comentarios(CSS[:CSS.index(MARCA)])
  self.assertEqual(antes.count('{'),antes.count('}'),'o bloco tem de começar fora de qualquer @media')
  self.assertNotIn('@media',sem_comentarios(bloco()))
  # 30/10/2026: quarta regra (revisão adversarial): os itálicos sem lang próprio não se partem com as regras do português
  self.assertEqual(len(regras()),4,'uma regra que justifica, duas que repõem por dentro o alinhamento e a hifenização, e a dos itálicos')

 def test_so_mexe_no_alinhamento_e_na_hifenizacao(self):
  sel,dec=regras()[0]
  props=dict(re.findall(r'([-\w]+)\s*:\s*([^;]+)',dec))
  self.assertEqual(props,{'text-align':'justify','text-align-last':'auto','-webkit-hyphens':'auto','hyphens':'auto',
   '-webkit-hyphenate-limit-before':'3','-webkit-hyphenate-limit-after':'3','hyphenate-limit-chars':'6 3 3',
   'word-spacing':'normal','overflow-wrap':'break-word'})
  sel2,dec2=regras()[1]
  self.assertEqual(dict(re.findall(r'([-\w]+)\s*:\s*([^;]+)',dec2)),{'text-align':'start'})
  sel3,dec3=regras()[2]
  self.assertEqual(dict(re.findall(r'([-\w]+)\s*:\s*([^;]+)',dec3)),{'-webkit-hyphens':'manual','hyphens':'manual'})
  # as reposições não pesam (:where), para não passarem por cima das regras da própria página
  for sel in (sel2,sel3):
   sel=re.sub(r'\s+',' ',sel);self.assertTrue(sel.startswith(':where(') and ') :where(' in sel,sel[:40])
  # 30/10/2026: títulos e citações em itálico com a língua da página (muitos títulos ingleses sem lang) ficam sem hifenização
  # automática; um texto com lang próprio continua com as suas regras, e a prosa da Biblioteca fica como estava
  sel4,dec4=regras()[3]
  self.assertEqual(sel4.strip(),':where(i,em,cite):lang(pt):not(.bib-texto *)')
  self.assertEqual(dict(re.findall(r'([-\w]+)\s*:\s*([^;]+)',dec4)),{'-webkit-hyphens':'manual','hyphens':'manual'})
  for proibida in ('font','color','line-height','letter-spacing','font-size','margin','padding'):
   self.assertNotRegex(sem_comentarios(bloco()),r'[{;]\s*'+proibida+r'\s*:')

 def test_versos_br_e_botoes_ficam_fora(self):
  sel,_=regras()[0]
  # 30/10/2026: qualquer bloco com botão fica fora (a frase de Kafka com os pedaços em botão, na entrada do Laboratório)
  self.assertTrue(sel.rstrip().endswith(':not(:has(br, button, > .c10-action, > .lf-button))'),sel[-80:])
  excluidas=set().union(*(classes(a) for a in argumentos_not(sel)))
  for c in ('versos','poema','verso-q','fachada-texto','levar','etq-m','q-pensa','bib-passagem','lf-actions','fonte-x','ap-fonte','quem'):
   self.assertIn(c,excluidas,c)
  # 30/10/2026 (revisão adversarial): elenco e linhas de personagens de Frei Luís de Sousa, listas em parágrafos,
  # instruções curtas com rótulo, guião em letra de máquina e explicações dentro de itens de lista ficam fora
  for c in ('personagens','elenco','lista','ex-antes','ex-depois','c10-script','c10-check'):
   self.assertIn(c,excluidas,c)
  # 30/10/2026: biografias de Vidas e vozes (dl em duas colunas, 16 a 22 car. por linha a 320 px), cartões de rotas do
  # docente (grelha de três colunas), caixa de crédito das Sidequests e frase de Kafka com botões ficam à esquerda
  for fora in ('vz-vc','guide-route','div.fonte','lf-evidence-quote'):
   self.assertNotIn(fora,sel,fora)
  # nenhuma etiqueta de lista, tabela, formulário, legenda ou título é alvo direto da regra
  alvos=[a.strip() for a in re.split(r',(?![^()]*\))',sel[sel.index('(')+1:sel.rindex(')')])]
  for a in alvos:
   ultimo=re.split(r'[\s>]+',re.sub(r'\([^()]*\)','',a).strip())[-1]
   self.assertNotRegex(ultimo,r'^(li|td|th|button|label|figcaption|summary|h[1-6]|legend|caption|pre|code|input|option)\b',a)
  sel2=regras()[1][0]
  for c in ('li','td','label','figcaption','summary','cite','versos','poema'):
   self.assertRegex(sel2,r'[(,]\.?'+c+r'[,)]',c)
  # botões, cabeçalhos de tabela e legendas de tabela têm alinhamento próprio do navegador: não se lhes mexe
  for c in ('button','th','caption'):
   self.assertNotRegex(sel2,r'[(,]'+c+r'[,)]',c)
  # o guia do docente da Justiça é uma grelha de pares curtos (Começa em, Acaba em, Antes, Depois, Debate): fica à esquerda
  self.assertNotIn('.ex >',sel)

 def test_cada_pagina_tem_familia_e_liga_a_appearance(self):
  contagem={}
  for rel,s in PAGINAS:
   f=familia(rel,s);contagem[f]=contagem.get(f,0)+1
   with self.subTest(pagina=rel):
    refs=re.findall(r'href="([^"]*assets/appearance\.css[^"]*)"',s)
    self.assertEqual(len(refs),1)
    self.assertTrue(((R/rel).parent/refs[0].split('?')[0]).resolve().is_file())
  self.assertEqual(set(contagem),set(MARCADORES),contagem)
  self.assertGreaterEqual(sum(contagem.values()),530)

 def test_cada_familia_tem_conteudo_que_a_regra_visa(self):
  sel,_=regras()[0];cls=classes(sel)
  por_familia={}
  for rel,s in PAGINAS:por_familia.setdefault(familia(rel,s),[]).append((rel,s))
  for f,marcas in MARCADORES.items():
   for m in marcas:
    with self.subTest(familia=f,classe=m):
     self.assertIn(m,cls,'a classe tem de constar do seletor da regra')
     pat=re.compile(r'class=\\?"(?:[^"\\]*\s)?'+re.escape(m)+r'(?:\s[^"\\]*)?\\?"|className\s*=\s*["\']'+re.escape(m))
     achou=any(pat.search(s) or pat.search(scripts_locais(rel,s)) for rel,s in por_familia[f])
     if f=='L2b' and not achou:achou=m in (R/'assets/formas/cartoes.js').read_text('utf-8')
     self.assertTrue(achou,f'nenhuma página de {f} usa .{m}')
  # C4 (aulas do M2, abertura do M1) não tem classes próprias: parágrafos num main nu ou nas suas secções
  self.assertIn('body > main:not([class]) :is(section,header) > p:not([class])',sel)
  self.assertIn('body > main:not([class]):not(:has(> svg:first-child)) > :is(p:not([class])',sel)
  for rel,s in por_familia['C4']:
   with self.subTest(familia='C4',pagina=rel):self.assertRegex(s,r'<main>[\s\S]*<p>')

 def test_paginas_sem_texto_corrido_estao_listadas_e_existem(self):
  for rel in SEM_TEXTO_CORRIDO:self.assertTrue((R/rel).is_file(),rel)
  s=(R/'404.html').read_text('utf-8')
  self.assertRegex(s,r'<main><svg','a página 404 só fica centrada enquanto o main começar pelo svg')
  self.assertIn(':not(:has(> svg:first-child))',regras()[0][0])

class LinguaEMarcacoes(unittest.TestCase):
 def test_todas_as_paginas_em_pt_PT(self):
  for rel,s in PAGINAS:
   with self.subTest(pagina=rel):self.assertRegex(s,r'<html lang="pt-PT"')

 def test_lang_proprio_so_em_textos_doutra_lingua_ou_variedade(self):
  validos={'pt-PT','pt','en','de','es','fr','it','la','zh'}
  for rel,s in PAGINAS:
   for v in re.findall(r'\slang=\\?"([^"\\]+)\\?"',s):
    with self.subTest(pagina=rel,lang=v):self.assertIn(v,validos)
  # lang="pt" (sem variedade) só nas cantigas em galego-português
  for rel,s in PAGINAS:
   if 'class="bib-texto" lang="pt"' in s:
    with self.subTest(pagina=rel):self.assertRegex(rel,r'biblioteca/(codax|dinis|mendinho|guilhade|torneol)-')
  for t in ('brascubas-ao-leitor','garrett-frei-luis-sousa','reporterx-conselhos-1930','reporterx-reporterxizar-1930','orta-benjui'):
   self.assertIn('class="bib-texto" lang="pt-PT"',(R/'biblioteca'/t/'index.html').read_text('utf-8'),t)

 def itens(self,rel):
  s=(R/rel/'index.html').read_text('utf-8');m=re.search(r'itens\s*:\s*(\[)',s)
  return json.JSONDecoder().raw_decode(s[m.start(1):])[0]

 def test_excertos_em_verso_marcados_como_poema(self):
  # versos um por <p> sem classe: sem a marca .poema o CSS não os distingue da prosa
  esperado={'narrativas/aula-forma':1,'narrativas/aula-lugar':1,'narrativas/aula-nao-dito':1,'narrativas/aula-personagem':1,
   'narrativas/cenario-personagem':3,'narrativas/comecar-pelo-meio':3,'narrativas/corta/cesario':1,'narrativas/corta/chuva':1,
   'narrativas/corta/ines':1,'narrativas/corta/restelo':1,'narrativas/corta/torneol':1,'narrativas/espinha':3,
   'narrativas/oficina-ficcao-espaco':1,'narrativas/oficina-ficcao-personagem':1,'narrativas/piramide':2,'narrativas/quem-conta':1,
   'narrativas/querer-agir':3,'narrativas/subtexto':1}
  total=0
  for rel,n in esperado.items():
   h=''.join(x.get('html') or '' for x in self.itens(rel))
   with self.subTest(licao=rel):self.assertEqual(h.count('<div class="trad poema">'),n)
   total+=n
  self.assertEqual(total,27)

 def test_versos_com_classe_e_prosa_sem_ela(self):
  # p.versos sem <br> é prosa (falas de Frei Luís de Sousa passaram a p.fala); só um verso de romance fica numa linha
  sem_br=[]
  for rel,s in PAGINAS:
   if 'itens' not in s or 'window.EPIJogo' not in s:continue
   m=re.search(r'itens\s*:\s*(\[)',s)
   if not m:continue
   for x in json.JSONDecoder().raw_decode(s[m.start(1):])[0]:
    for v in re.findall(r'<p class="versos">(.*?)</p>',x.get('html') or '',re.S):
     if '<br' not in v:sem_br.append((rel,v[:40]))
  self.assertEqual(sem_br,[('projetos/vozes/index.html','Postos estão, frente a frente, Os dois v')])
  # 30/10/2026: em Corta! Frei Luís, as quatro linhas de personagens depois de «SCENA» deixaram de ser falas (20 passam a 16)
  falas={'apresentar/passo-04':8,'ler/passo-04':31,'ler/passo-07':6,'narrativas/corta/frei-luis':16,'projetos/vozes':6,'sidequests/cinema':6,'sidequests/retorica':7}
  for rel,n in falas.items():
   with self.subTest(licao=rel):
    self.assertEqual(sum((x.get('html') or '').count('<p class="fala">') for x in self.itens(rel)),n)
  h=''.join(x.get('html') or '' for x in self.itens('narrativas/corta/frei-luis'))
  self.assertEqual(re.findall(r'</h2><p class="personagens">([^<]+)</p>',h),['MANUEL DE SOUSA, MAGDALENA, TELMO, MIRANDA e outros criados, entrando apressadamente.',
   'MANUEL DE SOUSA, MAGDALENA, TELMO, MIRANDA e os outros criados; JORGE e MARIA entrando.','MANUEL DE SOUSA, MIRANDA e os outros criados.',
   'MANUEL-DE-SOUSA e criados: MAGDALENA, MARIA, TELMO E JORGE accudindo.'])

 def test_bras_cubas_em_prosa_sem_as_quebras_da_transcricao(self):
  b=(R/'biblioteca/brascubas-ao-leitor/index.html').read_text('utf-8')
  self.assertRegex(b,r'<p>Com effeito, um dia de manhã, estando a passear na chacara, pendurou-se-me[^<]*</p>')
  h=''.join(x.get('html') or '' for x in self.itens('narrativas/corta/bras-cubas'))
  self.assertRegex(h,r'<p>Com effeito, um dia de manhã, estando a passear na chacara, pendurou-se-me[^<]*</p>')
  self.assertNotIn('class="versos">Com effeito',b+h)

 def test_frei_luis_elenco_e_personagens(self):
  # 30/10/2026 (revisão adversarial): o elenco era um só parágrafo com os nomes seguidos (uma lista); passa a um nome por
  # linha. As linhas de personagens no início das cenas (até 90 car.) são rótulos e ficam à esquerda; as mais longas são
  # didascálias em prosa e continuam justificadas.
  s=(R/'biblioteca/garrett-frei-luis-sousa/index.html').read_text('utf-8')
  el=re.findall(r'<p class="elenco">(.*?)</p>',s)
  self.assertEqual(len(el),2)
  self.assertEqual(el[0].split('<br>'),['MANUEL (FREI LUIZ) DE SOUSA','DONA MAGDALENA DE VILHENA','DONA MARIA DE NORONHA','FREI JORGE-COUTINHO',
   'O ROMEIRO','TELMO-PAES','O PRIOR DE BEMFICA','O IRMÃO CONVERSO','MIRANDA','O ARCEBISPO DE LISBOA','DOROTHEA'])
  self.assertEqual(el[1],"CÔRO DE FRADES DE SAN'DOMINGOS")
  pers=re.findall(r'<h2>SCENA [IVXL]+</h2>\n?<p class="personagens">([^<]+)</p>',s)
  self.assertEqual(len(pers),31)
  self.assertEqual(len(pers),s.count('class="personagens"'))
  for t in pers:self.assertRegex(t,r"^[A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ'()-]+");self.assertLessEqual(len(t),90,t)
  for t in re.findall(r'<h2>SCENA [IVXL]+</h2>\n?<p>([^<]+)</p>',s):
   with self.subTest(didascalia=t[:40]):self.assertGreater(len(t),90)

 def test_citacoes_inglesas_com_lang(self):
  # 30/10/2026 (revisão adversarial): frases e títulos ingleses dentro de texto justificado em pt-PT levam lang="en",
  # para não se partirem com as regras do português. Os itálicos sem lang ficam sem hifenização (regra de appearance.css);
  # as citações dentro das explicações (campo f, texto escapado pelo motor) ficam para o gerador.
  h=lambda rel:''.join(x.get('html') or '' for x in self.itens(rel))
  self.assertEqual(h('vozes/prince').count('«<span lang="en">'),6)
  self.assertIn('«<span lang="en">If you don\'t own your masters, your master owns you</span>»',h('vozes/prince'))
  self.assertEqual(h('vozes/paula-rego').count('«<span lang="en">'),3)
  v=(R/'ver-para-fazer/index.html').read_text('utf-8')
  self.assertEqual(len(re.findall(r'<a href="v\d\d/" style="color:inherit" lang="en">',v)),4)
  self.assertEqual((R/'ver-para-fazer/v124/index.html').read_text('utf-8').count('«<span lang="en">'),2)

 def test_mandamentos_em_lista(self):
  # 30/10/2026 (revisão adversarial): os Sete Mandamentos, no original inglês, são uma lista numerada em parágrafos
  h=''.join(x.get('html') or '' for x in self.itens('gigantes/triunfo-porcos'))
  self.assertIn('<div class="orig lista" lang="en"><p>THE SEVEN COMMANDMENTS</p><p>1. Whatever goes upon two legs is an enemy.</p>',h)

if __name__=='__main__':unittest.main()
