# 30/10/2026: contratos atualizados para percursos e imagens retiradas por decisão do docente.
from pathlib import Path
import json, re, unittest
ROOT=Path(__file__).resolve().parents[1]

class Formas(unittest.TestCase):
 def test_corpus_is_honest_and_has_two_uses(self):
  data=json.loads((ROOT/'assets/formas/corpus.json').read_text('utf-8'))
  self.assertEqual(len(data['items']),10)
  self.assertEqual(len({x['id'] for x in data['items']}),10)
  for item in data['items']:
   self.assertTrue(item['source'].startswith('https://'))
   for key in ('status','statusLabel','edition','language','locator','operation','modules','ptUse'):
    self.assertTrue(item[key],(item['id'],key))
   if item['status']=='excerto-consultado':
    self.assertLessEqual(len(item['quote'].split()),25)
    self.assertTrue(item['variants'] and item['task'] and item['review'])
    self.assertIn(item['answer'],range(len(item['options'])))
   else:self.assertNotIn('quote',item)
  by={x['id']:x for x in data['items']}
  # 29/10/2026: a frase ativa de Kafka passou a ser a citada pela RTP Ensina (decisão docente); a página não identifica a tradução.
  # A atribuição a Helena Topa (Penguin, 2021) fica no histórico do item, distinguida da fonte ativa, e é verificada em test_kafka_fonte_ativa_e_historico.
  self.assertIsNone(by['kafka']['translator'])
  self.assertEqual(by['kafka']['history'][0]['translator'],'Helena Topa')
  self.assertIn('não confundir',by['borges']['locator'].lower())
  self.assertNotIn('Pastelaria',by['cesariny']['work'])

 def test_legacy_paths_and_keys_remain(self):
  for name in ('ines','frei-luis','cesario','chuva','torneol','restelo','maias','bras-cubas'):
   self.assertTrue((ROOT/'narrativas/corta'/name/'index.html').exists())
  entry=(ROOT/'narrativas/index.html').read_text('utf-8')
  # 30/10/2026: as âncoras antigas que já não estão na entrada levam a tudo/, onde ficam no percurso equivalente.
  tudo=(ROOT/'narrativas/tudo/index.html').read_text('utf-8')
  self.assertIn('location.replace("tudo/"',entry)
  for anchor in ('ler-como-quem-escreve','treinar','criar','corta','aulas','experimentar','vidas-e-ideias'):
   self.assertIn('id="'+anchor+'"',entry if anchor in ('ler-como-quem-escreve','treinar','criar') else tudo)
  script=(ROOT/'assets/formas/corta.js').read_text('utf-8')
  self.assertIn('lente-formas-corta-v1',script)
  self.assertNotIn("setItem('epi-corta'",script)

 def test_all_new_local_dependencies_exist(self):
  for rel in ('narrativas/corta/mesa/index.html','narrativas/formas/index.html'):
   page=ROOT/rel
   for asset in re.findall(r'(?:src|href)="([^"]+)"',page.read_text('utf-8')):
    if asset.startswith(('http','#')):continue
    clean=asset.split('?')[0].split('#')[0]
    target=(page.parent/clean).resolve()
    if clean.endswith('/'):target=target/'index.html'
    self.assertTrue(target.exists(),(rel,asset))
  # 30/10/2026: planos descritos substituem a imagem de IA.
  self.assertFalse((ROOT/'assets/formas/carteira-linha.png').exists())
  self.assertIn('D.shots[id].caption',(ROOT/'assets/formas/corta.js').read_text('utf-8'))


# ── 29/10/2026: Kafka com a frase da RTP Ensina e os dois protótipos em cartões curtos («Certa manhã», «A cena que falta») ──
from html.parser import HTMLParser
FRASE='Certa manhã, ao acordar de sonhos inquietos, Gregor Samsa viu-se transformado num gigantesco inseto.'
RTP='https://ensina.rtp.pt/artigo/a-metamorfose-ou-a-parabola-do-homem-inseto-de-franz-kafka/'
# Primeira frase do original (Projeto Gutenberg, livro n.º 22367, linhas 70-71), copiada a 29/10/2026; o CI não vai buscar nada à rede.
GUTENBERG='Als Gregor Samsa eines Morgens aus unruhigen Träumen erwachte, fand er sich in seinem Bett zu einem ungeheueren Ungeziefer verwandelt.'
PROIBIDAS=re.compile(r'\b(ficha|fichas|folha|folhas|jogar|joga|jogas|professor|professora|professores)\b',re.I)
def dados(nome):
 txt=(ROOT/'assets/formas'/nome).read_text('utf-8').strip()
 m=re.match(r'^window\.\w+\s*=\s*(\{.*\});?\s*$',txt,re.S)
 return json.loads(m.group(1))
def textos_cartoes():
 js=(ROOT/'assets/formas/cartoes.js').read_text('utf-8')
 m=re.search(r'/\*TEXTOS\*/\s*const TEXTOS=(\{.*?\});\s*/\*FIM-TEXTOS\*/',js,re.S)
 return json.loads(m.group(1))
def cadeias(v,fora=('rtp','rtpPlay','gutenberg','href','img','source','secondarySource','id','escolha','se','pede')):
 if isinstance(v,str):yield v
 elif isinstance(v,list):
  for x in v:yield from cadeias(x,fora)
 elif isinstance(v,dict):
  for k,x in v.items():
   if k not in fora:yield from cadeias(x,fora)
class Texto(HTMLParser):
 def __init__(s):super().__init__();s.pilha=[];s.partes=[];s.titulo=''
 def handle_starttag(s,t,a):s.pilha.append(t)
 def handle_endtag(s,t):
  if t in s.pilha:
   while s.pilha and s.pilha.pop()!=t:pass
 def handle_data(s,d):
  if s.pilha and s.pilha[-1] in ('script','style'):return
  if s.pilha and s.pilha[-1]=='title':s.titulo+=d;return
  if d.strip():s.partes.append(d.strip())

class Prototipos(unittest.TestCase):
 def test_kafka_fonte_ativa_e_historico(self):
  by={x['id']:x for x in json.loads((ROOT/'assets/formas/corpus.json').read_text('utf-8'))['items']}
  k=by['kafka']
  self.assertEqual(k['quote'],FRASE);self.assertLessEqual(len(k['quote'].split()),25)
  self.assertEqual(k['source'],RTP);self.assertIsNone(k['translator']);self.assertEqual(k['translatorStatus'],'não confirmado')
  for campo in ('quote','edition','statusLabel','locator','source','creditLine','sourceLabel'):
   for velho in ('Helena Topa','Penguin','bicharoco','deu por si'):
    self.assertNotIn(velho,str(k.get(campo) or ''),(campo,velho))
  self.assertIn('RTP Ensina',k['statusLabel']);self.assertIn('não identifica a tradução',k['locator'])
  self.assertTrue(k['history'][0]['status'].startswith('substituída a 29/10/2026'))
  self.assertIn('bicharoco monstruoso',k['history'][0]['quote'])
  self.assertTrue((ROOT/'narrativas/formas'/k['route']/'index.html').is_file())
  readme=(ROOT/'curadoria/README-formas.md').read_text('utf-8')
  self.assertIn('Fonte ativa',readme);self.assertIn('Histórico (não é a fonte ativa)',readme);self.assertIn(RTP,readme)

 def test_kafka_expressoes_selecionaveis_na_frase_nova(self):
  js=(ROOT/'assets/formas/leituras.js').read_text('utf-8')
  linha=next(l for l in js.splitlines() if l.startswith(' kafka:'))
  ancoras=re.findall(r"\['([^']+)','",linha.split('hypotheses:')[0])
  self.assertEqual(ancoras,['Certa manhã','viu-se transformado','gigantesco inseto'])
  for a in ancoras:self.assertIn(a,FRASE)
  for velho in ('Uma manhã','deu por si','bicharoco','monstruoso'):self.assertNotIn(velho,linha)
  self.assertIn('«Gregor Samsa»',linha);self.assertIn('«viu-se»',linha)
  self.assertIsNone(PROIBIDAS.search(linha))

 def test_certa_manha_contrato(self):
  K=dados('certa-manha.js');by={x['id']:x for x in json.loads((ROOT/'assets/formas/corpus.json').read_text('utf-8'))['items']}
  self.assertEqual(K['frase'],FRASE);self.assertEqual(K['frase'],by['kafka']['quote'])
  segs=[s['t'] for s in K['segmentos']];self.assertEqual(len(segs),6);self.assertEqual(' '.join(segs),FRASE)
  # o final comum inclui o pedaço tocado (C4 da revisão de 29/10); no último pedaço não há final comum
  finais=set()
  for i,s in enumerate(K['segmentos']):
   q=K['a1']['toques'][s['id']]
   if i==len(segs)-1:self.assertIn('semFim',q);self.assertNotIn('fim',q);continue
   final=' '.join(segs[:i+1])+q['fim'];self.assertNotEqual(final,FRASE);self.assertNotIn('inseto',final);finais.add(final)
  self.assertEqual(len(finais),5)
  self.assertIn('pedaço',K['a1']['pergunta']);self.assertNotIn('palavra a partir',K['a1']['pergunta'])
  self.assertEqual(len({q['titulo'] for q in K['a1']['toques'].values()}),6)
  self.assertEqual(len(K['a2']['variantes']),3)
  for v in K['a2']['variantes']:
   self.assertEqual(''.join(p.get('t',p.get('mais','')) for p in v['partes']),v['texto']);self.assertNotEqual(v['texto'],FRASE)
   self.assertEqual(set(v['explica']),{'original','variante','igual'});self.assertEqual(len(set(v['explica'].values())),3)
   for linha in ('acontece','espanto'):self.assertEqual(len(v['pauta'][linha]),3)
   self.assertTrue(v['fecho'])  # cada variante tem o seu fecho (C11)
   if v['pauta']['espanto']==K['a2']['original']['espanto']:self.assertNotIn('nunca sai',v['fecho'])
  self.assertNotIn('vê se a tua escolha se mantém',json.dumps(K['a2'],ensure_ascii=False));self.assertNotIn('precisamente de não haver aviso',json.dumps(K['a2'],ensure_ascii=False))
  # A3 (C6): a regra do «transformar» tem frase própria e as reações das variantes têm aviso
  self.assertEqual([p['regra'] for p in K['a3']['proibidas'] if p.get('raiz')=='transform'],['que não uses o verbo «transformar»'])
  ecos=[w for g in K['a3']['ecos'] for w in g['raizes']+g['palavras']]
  for w in ('horroriz','assust','espant','grit','pavor','medo','terrív'):self.assertIn(w,ecos)
  ids=[a['id'] for a in K['afirmacoes']];self.assertEqual(len(ids),9)
  for x in ('identidade','emprego','sozinho','intencao','manha','dormiu'):self.assertIn(x,ids)
  # C14: pôr tudo em «Preciso de mais contexto» não pode valer mais ● do que metade
  marcas_falta=[a['b1']['falta']['marca'] for a in K['afirmacoes']]
  self.assertLess(marcas_falta.count('●'),len(ids)/2);self.assertGreaterEqual(marcas_falta.count('○'),3)
  for a in K['afirmacoes']:
   self.assertEqual(set(a['b1']),{'mostra','infiro','falta'});self.assertEqual(set(a['f']),{'mostra','infiro','falta','desmente'})
   for c in list(a['b1'].values())+list(a['f'].values()):self.assertIn(c['marca'],'●◐○');self.assertTrue(c['t'])
  melhor=lambda cel:[k for k,c in cel.items() if c['marca']=='●']
  mudam=[a['id'] for a in K['afirmacoes'] if set(melhor(a['b1']))!=set(melhor(a['f']))]
  for x in ('cama','emprego','sozinho','repulsa'):self.assertIn(x,mudam)  # a informação nova muda de facto o estatuto destas afirmações
  self.assertEqual(K['afirmacoes'][ids.index('intencao')]['f']['falta']['marca'],'●')  # a intenção do autor continua fora do texto
  self.assertEqual(len(K['b2']['afirmacoes']),3)
  for a in K['b2']['afirmacoes']:self.assertEqual(set(K['b2']['explica'][a]),{t['id'] for t in K['b2']['tipos']})
  for esc in K['f2']['escolhas']:self.assertTrue(any(r['escolha']==esc['id'] and not r['se'] for r in K['f2']['explica']),esc['id'])
  for r in K['f2']['explica']:
   if r['se']:self.assertIn(r['se'].split(':')[1],ids)
  for x in K['original']['expressoes']:self.assertIn(x['t'],GUTENBERG)
  self.assertEqual([p['par'] for p in K['inicio']['passagens']],['§ 1','§ 2','§ 2','§ 5','§ 7'])
  # C7: o § 1 descreve o corpo; o nome da espécie é que é escolha da versão portuguesa
  corpo=next(a for a in K['afirmacoes'] if a['id']=='corpo')
  self.assertEqual(corpo['f']['mostra']['marca'],'●');self.assertIn('§ 1',corpo['f']['mostra']['t'])
  bruto_k=json.dumps(K,ensure_ascii=False)
  for velho in ('escolha da tradução','a tradução deixou-a de fora','a tradução que leste deixou-a de fora'):self.assertNotIn(velho,bruto_k)
  self.assertIn('versão portuguesa citada pela RTP',bruto_k)
  # G2: o que se manteve lê-se contra o que se leu, sem «mais firme» por defeito
  self.assertNotIn('Ficou mais firme porque',bruto_k)
  # P3: a escolha de uma fonte não usa os nomes das marcas de leitura
  self.assertEqual(set(K['marcasFonte']),{'●','◐','○'});self.assertFalse(set(K['marcasFonte'].values())&set(K['marcas'].values()))
  bruto=(ROOT/'assets/formas/certa-manha.js').read_text('utf-8')
  self.assertNotIn(GUTENBERG,bruto)  # decisão de 16/10/2026: não se guardam textos em alemão; fica o relato e a ligação à edição
  self.assertNotIn('Als Gregor Samsa',bruto)
  self.assertIn('Projeto Gutenberg',K['original']['credito']);self.assertIn('Projeto Gutenberg',K['inicio']['credito'])
  self.assertEqual(K['credito']['rtp'],RTP);self.assertIn('RTP Ensina',K['credito']['curto']);self.assertIn('não identifica a tradução',K['credito']['curto'])
  for velho in ('Helena Topa','Penguin','bicharoco'):self.assertNotIn(velho,bruto)

 def test_cena_que_falta_combinacoes_distintas(self):
  F=dados('cena-que-falta.js');H=[h['id'] for h in F['hipoteses']]
  self.assertEqual(len(F['candidatos']),3);self.assertEqual(len(H),4);self.assertEqual(F['tira'][3],'lacuna');self.assertEqual(len(F['tira']),5)
  vet={p:tuple(F['estados'][p][h]['estado'] for h in H) for p in F['candidatos']}
  for v in vet.values():
   self.assertTrue(set(v)<={'ganha','perde','igual'});self.assertIn('ganha',v)
  self.assertEqual(len(set(vet.values())),3)
  for c in [F['estados'][p][h] for p in F['candidatos'] for h in H]:
   self.assertTrue(c['razao'])
   if c.get('discutivel'):self.assertTrue(c.get('alternativa'))
  import itertools
  for a,b in itertools.combinations(F['candidatos'],2):
   par=F['pares'].get(a+'+'+b) or F['pares'].get(b+'+'+a);self.assertTrue(par and par['sintese'])
   dif=[h for h in H if F['estados'][a][h]['estado']!=F['estados'][b][h]['estado']]
   self.assertGreaterEqual(len(dif),2,(a,b))
   for h in dif:self.assertTrue(par.get(h),(a,b,h))
   self.assertIn(par['principal'],dif)
  self.assertEqual(len({F['explicacao'][p]['titulo'] for p in F['candidatos']}),3)
  self.assertEqual(len({F['explicacao'][p]['corpo'] for p in F['candidatos']}),3)
  self.assertEqual({l['pede'] for l in F['legendasFim'] if l['pede']},set(F['candidatos']))
  for l in F['legendasFim']:
   if l['pede']:self.assertNotEqual(l['com'],l['sem'])
  for q in ('perda','regresso'):self.assertIn('esquerda',F['quadros'][q]['legenda'])
  for q in F['quadros'].values():
   if q.get('img'):
    # 30/10/2026: cada plano conserva a descrição; os ficheiros de IA saíram.
    self.assertGreater(len(q['legenda']),25);self.assertFalse((ROOT/'assets/formas/carteira'/(q['img']+'.webp')).exists())
  self.assertTrue(all(F['quadros'][p].get('intertitulo') for p in F['candidatos']))
  self.assertNotIn('senta',F['escreve']['palavras']);self.assertIn('pensou',F['escreve']['palavras'])
  # C1 e C2: nada de «sem efeito» nem da linha genérica da câmara; a razão é a de cada combinação
  bruto_f=json.dumps(F,ensure_ascii=False)
  self.assertNotIn('sem efeito',bruto_f);self.assertNotIn('linhaSemEfeito',F);self.assertNotIn('a câmara olha para outro lado',bruto_f)
  self.assertEqual(F['estadosNomes']['igual'],'não muda');self.assertEqual(F['estadoFrase']['igual'],'fica como estava')
  # G3: só a legenda neutra se apoia no que se vê; as outras supõem
  self.assertEqual([l['id'] for l in F['legendasFim'] if not l['pede']],['neutra'])
  for l in F['legendasFim']:self.assertNotIn('Apoia-se no que vês',l['com'])
  self.assertIn('vês no meio',F['compara']['difCorpo']);self.assertIn('mais prudente',F['compara']['neutraCorpo'])
  # P2: os símbolos têm um só sentido, o mesmo nos dois percursos
  self.assertEqual(F['marcas'],dados('certa-manha.js')['marcas'])
  # C13: apoio misto também em «Mantenho» e «Corrijo»
  for r in ('mantenho','corrijo','aberto'):self.assertIn('ambos',F['reve']['textos'][r])
  self.assertIn('à hipótese',F['escolhe']['perguntaOutra']);self.assertEqual(F['escreve']['marca'],'Opcional');self.assertIn('não porquê',F['escreve']['avisoPorque'])
  self.assertNotIn('rapaz',json.dumps(F,ensure_ascii=False))

 def test_textos_visiveis_cumprem_as_regras(self):
  K=dados('certa-manha.js');F=dados('cena-que-falta.js');T=textos_cartoes()
  for nome,valores in (('certa-manha.js',list(cadeias(K))),('cena-que-falta.js',list(cadeias(F))),('TEXTOS',list(cadeias(T)))):
   for v in valores:
    self.assertIsNone(PROIBIDAS.search(v),(nome,v));self.assertNotIn('—',v,(nome,v));self.assertNotIn('·',v,(nome,v))
    # aspas: « » no primeiro nível; “ ” só dentro de « » (tech C5)
    fora=re.sub(r'«[^«»]*»','',v);self.assertNotIn('“',fora,(nome,v))
  for rel in ('narrativas/formas/certa-manha/index.html','narrativas/corta/cena-que-falta/index.html','narrativas/corta/mesa/index.html','narrativas/formas/index.html'):
   t=Texto();t.feed((ROOT/rel).read_text('utf-8'))
   for v in t.partes:
    self.assertIsNone(PROIBIDAS.search(v),(rel,v));self.assertNotIn('—',v,(rel,v));self.assertNotRegex(v,r'[^\s/]\s·\s[^\s/]',(rel,v))
  i=(ROOT/'narrativas/index.html').read_text('utf-8');bloco=i.split('<script type="application/json"')[0] # 30/10/2026: toda a entrada nova, não apenas o piloto.
  t=Texto();t.feed(bloco)
  for v in t.partes:self.assertIsNone(PROIBIDAS.search(v),v);self.assertNotIn('·',v)
  corpus=json.loads((ROOT/'assets/formas/corpus.json').read_text('utf-8'))
  self.assertIsNone(PROIBIDAS.search(corpus['policy']))
  for item in corpus['items']:
   for k,v in item.items():
    if k in ('source','secondarySource','history','translatorLead','original') or not isinstance(v,str):continue
    self.assertIsNone(PROIBIDAS.search(v),(item['id'],k,v))
    if k not in ('statusLabel','edition'):self.assertNotIn(' · ',v,(item['id'],k))
  for nome in ('obras.js','corta.js'):
   js=(ROOT/'assets/formas'/nome).read_text('utf-8')
   for lit in re.findall(r"'([^'\\]*(?:\\.[^'\\]*)*)'",js):
    self.assertIsNone(re.search(r'\bficha|\bfolha',lit,re.I),(nome,lit))
   self.assertNotIn('Versão C · uma ausência',js);self.assertNotIn('· conservada',js);self.assertNotIn('· não guardada',js)
  lit=(ROOT/'assets/formas/leituras.js').read_text('utf-8');self.assertIsNone(PROIBIDAS.search(lit))

 def test_progresso_novo_sem_apagar_o_antigo(self):
  prog=(ROOT/'assets/formas/progresso.js').read_text('utf-8')
  self.assertIn("'lente-formas-v1'",prog);self.assertNotIn('lente-formas-corta-v1',prog)  # a chave antiga só a lê a entrada (tech P4: sem função morta)
  self.assertEqual(len(re.findall(r'localStorage\.setItem\(',prog)),2)  # a chave nova e o teste de disponibilidade
  self.assertIn('localStorage.setItem(CHAVE',prog);self.assertNotIn('epi-corta',prog);self.assertNotIn('apagarPrimeira',prog)
  self.assertIn("lente-formas-corta-v1",(ROOT/'assets/formas/entrada.js').read_text('utf-8'))
  # tech G2: «Recomeçar» não apaga a primeira leitura guardada no aparelho; tech G1: o bloco de impressão compõe-se uma vez
  cart=(ROOT/'assets/formas/cartoes.js').read_text('utf-8')
  self.assertNotIn('apagarPrimeira',cart);self.assertNotRegex(cart,r"beforeprint',\(\)=>\{impressao\.innerHTML")
  self.assertIn('if(projetado)return false',prog)
  for nome in ('cartoes.js','entrada.js'):
   js=(ROOT/'assets/formas'/nome).read_text('utf-8')
   self.assertNotIn('setItem',js,nome);self.assertNotIn('removeItem',js,nome)
  self.assertNotIn('localStorage',(ROOT/'assets/formas/cartoes.js').read_text('utf-8'))
  self.assertIn("lente-formas-v1",(ROOT/'assets/formas/entrada.js').read_text('utf-8'))

 def test_acessos_e_dependencias_das_paginas_novas(self):
  for rel in ('narrativas/formas/certa-manha/index.html','narrativas/corta/cena-que-falta/index.html'):
   page=ROOT/rel;html=page.read_text('utf-8')
   for asset in re.findall(r'(?:src|href)="([^"]+)"',html):
    if asset.startswith(('http','#')):continue
    clean=asset.split('?')[0].split('#')[0];target=(page.parent/clean).resolve()
    if clean.endswith('/'):target=target/'index.html'
    self.assertTrue(target.exists(),(rel,asset))
   for x in ('data-casca','data-lf-percurso=','projection-launcher.js','data-site="lente"','assets/formas/cartoes.js','assets/formas/progresso.js','data-lf-menu="caderno"','data-lf-menu="recomecar"','lang="pt-PT"'):
    self.assertIn(x,html,(rel,x))
  # 30/10/2026: Laboratório simples (pedido do docente). Catálogo e fontes passam para destinos próprios.
  entrada=(ROOT/'narrativas/index.html').read_text('utf-8')
  for x in ('href="aula-forma/"','href="tudo/"','<h2>Ver</h2>','<h2>Treinar</h2>','<h2>Criar</h2>'):self.assertIn(x,entrada)
  tudo=(ROOT/'narrativas/tudo/index.html').read_text('utf-8')
  for nome in ('duchamp','anguissola','fontana','leonardo','cigoli','galileu','margens'):self.assertIn('href="../'+nome+'/"',tudo)
  # 30/10/2026: catálogo simples por percursos, com todas as peças.
  self.assertIn('class="catalogo"',tudo)
  js=(ROOT/'assets/formas/cartoes.js').read_text('utf-8')
  for texto in ('Guia do docente e fontes','Versão em papel','fonteHtml()'):self.assertIn(texto,js)
  mesa=(ROOT/'narrativas/corta/mesa/index.html').read_text('utf-8')
  self.assertIn('href="../cena-que-falta/"',mesa);self.assertIn('href="../../formas/certa-manha/"',mesa)
  self.assertIn('href="cena-que-falta/"',(ROOT/'narrativas/corta/index.html').read_text('utf-8'))
  self.assertIn('href="certa-manha/"',(ROOT/'narrativas/formas/index.html').read_text('utf-8'))
  wf=(ROOT/'.github/workflows/formas-qa.yml').read_text('utf-8')
  for x in ('progresso.js','cartoes.js','certa-manha.js','cena-que-falta.js'):self.assertIn('node --check assets/formas/'+x,wf)
  for x in ("'assets/narrativas-core/**'","'assets/appearance*'","'assets/projection-launcher.js'"):self.assertIn(x,wf)

# 30/10/2026: Laboratório simples (pedido do docente).
class PilotoSimples(unittest.TestCase):
 def test_cartoes_curto_e_opcoes(self):
  import sys
  sys.path.insert(0,str(ROOT/'tools'));import medir_opcoes
  for nome,n in [('certa-manha',8),('cena-que-falta',5)]:
   d=dados(nome+'.js');self.assertEqual(len(d['piloto']),n)
   for q in d['piloto']:
    self.assertLessEqual(len(q['p'].split()),25,q['id'])
    self.assertLessEqual(len(q.get('apoio','').split()),40,q['id'])
    if 'o' in q:self.assertTrue(2<=len(q['o'])<=4,q['id'])
    for txt in [q.get('f','')]+[t for t in q.get('fe',[]) if t]:self.assertLessEqual(len(re.findall(r'[.!?](?: |$)',txt)),2,(q['id'],txt))
  for q in medir_opcoes.laboratorio(ROOT):self.assertFalse(q['fora20'] or q['denunciadora'],q)
 def test_planos_imagens_e_creditos(self):
  for nome in ('bolso','cartao','regresso'):
   # 30/10/2026: os planos passaram a descrições existentes, com a mesma licença.
   self.assertFalse((ROOT/'assets/formas/carteira'/f'{nome}.svg').exists())
   self.assertTrue(dados('cena-que-falta.js')['quadros'][nome]['legenda'])
  self.assertIn('CC BY-SA 4.0',dados('cena-que-falta.js')['creditos'])
 def test_catalogo_preserva_destinos(self):
  from urllib.parse import urljoin
  # 30/10/2026: Laboratório simples (pedido do docente). Destinos de f7d8b9d, sem depender do histórico no CI.
  antes=set(['/lente/assets/appearance.css?v=20261025-universal-1', '/lente/assets/atelier-pages.css?v=20261019-2', '/lente/assets/formas/entrada.css?v=20261029', '/lente/assets/index-layout.css?v=20261026.1', '/lente/assets/lab-posters.css?v=20261019-3', '/lente/assets/lente-refino.css?v=20261022-1', '/lente/assets/narrativas-sets.css', '/lente/docente/', "/lente/narrativas/'+esc(x.url)+'", '/lente/narrativas/aula-forma/', '/lente/narrativas/aula-lugar/', '/lente/narrativas/aula-nao-dito/', '/lente/narrativas/aula-personagem/', '/lente/narrativas/cenario-personagem/', '/lente/narrativas/comecar-pelo-meio/', '/lente/narrativas/corta/cena-que-falta/', '/lente/narrativas/corta/mesa/', '/lente/narrativas/desenlace/', '/lente/narrativas/dialogo/', '/lente/narrativas/espingarda/', '/lente/narrativas/espinha/', '/lente/narrativas/fora-da-pagina/', '/lente/narrativas/formas/?mesa=pt', '/lente/narrativas/formas/certa-manha/', '/lente/narrativas/historia-enredo/', '/lente/narrativas/linhas-de-enredo/', '/lente/narrativas/oficina-arco/', '/lente/narrativas/oficina-argumento/', '/lente/narrativas/oficina-atelie/', '/lente/narrativas/oficina-ator/', '/lente/narrativas/oficina-dilema/', '/lente/narrativas/oficina-dramaturgista/', '/lente/narrativas/oficina-epico/', '/lente/narrativas/oficina-espaco/', '/lente/narrativas/oficina-ficcao-comecar/', '/lente/narrativas/oficina-ficcao-espaco/', '/lente/narrativas/oficina-ficcao-genero/', '/lente/narrativas/oficina-ficcao-personagem/', '/lente/narrativas/oficina-manifesto/', '/lente/narrativas/oficina-matriz/', '/lente/narrativas/oficina-pedacos/', '/lente/narrativas/oficina-plano/', '/lente/narrativas/oficina-readymade/', '/lente/narrativas/oficina-restricao/', '/lente/narrativas/oficina-texto-imagem/', '/lente/narrativas/oficina-visivel/', '/lente/narrativas/personagem-faz/', '/lente/narrativas/piramide/', '/lente/narrativas/proposta-subtexto/', '/lente/narrativas/quem-conta/', '/lente/narrativas/querer-agir/', '/lente/narrativas/subtexto/', '/lente/narrativas/treinar/', '/lente/narrativas/treinar/a-entrevista/', '/lente/narrativas/treinar/a-espingarda/', '/lente/narrativas/treinar/a-gaveta/', '/lente/narrativas/treinar/acelerar-travar/', '/lente/narrativas/treinar/comeca-mais-tarde/', '/lente/narrativas/treinar/copia-lenta/', '/lente/narrativas/treinar/cortar-um-quinto/', '/lente/narrativas/treinar/dicionario/', '/lente/narrativas/treinar/duas-horas/', '/lente/narrativas/treinar/duas-vozes/', '/lente/narrativas/treinar/frase-querida/', '/lente/narrativas/treinar/interromper/', '/lente/narrativas/treinar/lista-substantivos/', '/lente/narrativas/treinar/o-contrario/', '/lente/narrativas/treinar/objeto-banal/', '/lente/narrativas/treinar/outro-ponto-de-vista/', '/lente/narrativas/treinar/pelo-meio/', '/lente/narrativas/treinar/pelo-que-faz/', '/lente/narrativas/treinar/pergunta-sem-resposta/', '/lente/narrativas/treinar/quarto-que-fala/', '/lente/narrativas/treinar/rascunho-mau/', '/lente/narrativas/treinar/sem-disse/', '/lente/narrativas/treinar/sem-mente/', '/lente/narrativas/treinar/sem-olhos/', '/lente/narrativas/treinar/so-gestos/', '/lente/narrativas/treinar/teste-do-colega/', '/lente/narrativas/treinar/tres-em-cinco/', '/lente/narrativas/treinar/verbo-forte/', '/lente/narrativas/treinar/verdade-dificil/', '/lente/narrativas/treinar/voz-alta/'])
  novo=(ROOT/'narrativas/tudo/index.html').read_text('utf-8')
  depois={urljoin('/lente/narrativas/tudo/',h) for h in re.findall(r'href="([^"#]+)"',novo) if not h.startswith(('https:','http:'))}
  # 30/10/2026: preservam-se destinos de conteúdo; CSS antigo e literais JS não são destinos.
  antes={u for u in antes if '/assets/' not in u and "'+esc" not in u}
  self.assertTrue(antes<=depois,antes-depois)
if __name__=='__main__':unittest.main()
