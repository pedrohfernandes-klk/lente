"""30/10/2026: opções equilibradas (pedido do docente)."""
from pathlib import Path
import importlib.util,unittest,json,math,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('medir_opcoes',ROOT/'tools/medir_opcoes.py')
medir=importlib.util.module_from_spec(spec);spec.loader.exec_module(medir)
class OpcoesEquilibradas(unittest.TestCase):
 def test_caracteres_visiveis(self):
  self.assertEqual(medir.visivel('<b>Uma</b> _ideia_ &amp; **outra**\n aqui'),'Uma ideia & outra aqui')
 def test_palavras_proibidas(self):
  # 30/10/2026: revisão do #72 (opções equilibradas), terceira ronda: as flexões de «jogar» e «jogo» são proibidas,
  # palavras como «jogral» não.
  for p in ('jogo','jogar','joga','jogas','jogam','jogou','joguei','jogámos','professores','fichas','folha','um · dois','sim — não'):
   self.assertIsNotNone(PROIBIDAS.search(p),p)
  for p in ('jogral','jograis','folhagem','fichário','professorado'):
   self.assertIsNone(PROIBIDAS.search(p),p)
 def test_ambito(self):
  # 30/10/2026: revisão de pt-PT da Cidadania refeita (M1, 31/10): as lições piloto (cidadania/piloto) também se medem.
  self.assertEqual(set(medir.PASTAS),{'cidade','investigar','projetos','fachada','apresentar','estetica','etica','ler','direitos','olhar-e-decidir','cidadania/piloto'})
 def test_sem_denunciadoras(self):
  perguntas=list(medir.perguntas(ROOT));self.assertTrue(perguntas,'A medição não encontrou perguntas')
  falhas=[f"{q['pagina']} #{q['numero']}: {q['comprimentos']}, certa {q['certa']}" for q in perguntas if q['denunciadora']]
  self.assertEqual(falhas,[],str(len(falhas))+' denunciadoras:\n'+'\n'.join(falhas))
 def test_amplitude_e_excecoes_justificadas(self):
  ids=set()
  for q in medir.perguntas(ROOT):
   id=q['pagina']+'#'+str(q['numero'])
   if q['amplitude20']:
    self.assertTrue(q['excecao'],id);ids.add(id)
  self.assertEqual(ids,set(medir.EXCECOES),'Rever exceções obsoletas ou novas')
 def test_distribuicao_por_pagina(self):
  # 30/10/2026: revisão do #72 (opções equilibradas): regra simétrica; a certa também não pode ser a mais curta
  # mais vezes do que o acaso daria (antes só falhava se fosse a mais curta em todas as perguntas da página).
  for p,r in medir.resumir(list(medir.perguntas(ROOT)),'pagina').items():
   self.assertLessEqual(r['certaMaisLonga'],math.ceil(r['esperadoMaisLonga']),p)
   self.assertLessEqual(r['certaMaisCurta'],math.ceil(r['esperadoMaisLonga']),p)
 def test_trocas_preservam_os_contratos(self):
  # 30/10/2026: revisão do #72 (opções equilibradas): aceita também trocas de um «completar» inteiro (quando o f
  # que tem de mudar está no objeto pai das lacunas) e a correção do enunciado (p); a certa e o número de opções
  # continuam fixos, e o resto do objeto também. Cada «antigo» tem de existir, uma só vez, no main, e as palavras
  # proibidas são procuradas com as flexões em tudo o que muda (opções, f, p e lacunas).
  # 30/10/2026: revisão do #72 (opções equilibradas), terceira ronda: compara-se com a base fixa gravada em cada troca
  # («base», o sha do main de onde as trocas partem) e não com o main vivo, que depois da fusão já tem o «novo». Sem essa
  # referência (checkout raso), aceita-se a troca quando o «novo» aparece «ocorrencias» vezes na árvore atual, como em
  # test_videos_escolhidos. Nunca se salta.
  trocas=json.loads((ROOT/'tools/trocas/opcoes-lente-20261030.json').read_text('utf-8'))
  self.assertTrue(trocas)
  for t in trocas:
   self.assertEqual(set(t),{'ficheiro','local','antigo','novo','ocorrencias','achado','base'})
   self.assertRegex(t['base'],r'^[0-9a-f]{40}$')
   self.assertIn(t['ficheiro'].split('/')[0],medir.PASTAS);self.assertTrue(t['achado'])
   base=da_base(t['base'],t['ficheiro'])
   if base is not None:self.assertEqual(base.count(t['antigo']),t['ocorrencias'],'antigo fora da base '+t['base'][:7]+': '+t['ficheiro']+' '+t['local'])
   antes=json.loads(t['antigo']);depois=json.loads(t['novo'])
   self.assertEqual(contrato(antes),contrato(depois),t['ficheiro']+' '+t['local'])
   self.assertEqual({k:v for k,v in antes.items() if k not in MUDAVEIS},{k:v for k,v in depois.items() if k not in MUDAVEIS})
   actual=(ROOT/t['ficheiro']).read_text('utf-8')
   self.assertEqual(actual.count(t['novo']),t['ocorrencias'],t['ficheiro'])
   for k in MUDAVEIS:
    if antes.get(k)!=depois.get(k):self.assertIsNone(PROIBIDAS.search(json.dumps(depois[k],ensure_ascii=False)),t['ficheiro']+' '+t['local'])
 def test_feedback_nao_cita_opcoes_retiradas(self):
  # 30/10/2026: revisão do #72 (opções equilibradas): um f (ou fe) que cita entre «» ou em **negrito** um trecho que
  # estava numa opção no main e já não está em nenhuma opção da pergunta falha. Só não falha se o trecho estiver no
  # próprio cartão (enunciado, citação, frase a completar) ou se o texto lido do baralho (os cartões «ler») o tiver
  # também entre «», ou com duas palavras ou mais: aí a citação é desse texto e não da opção. As opções e o feedback das
  # outras perguntas não contam. O trecho pode ter só 2 caracteres («eu») e procura-se como palavra inteira; uma palavra
  # solta que o texto lido só usa sem aspas não chega para a desculpar.
  # 30/10/2026: revisão do #72 (opções equilibradas), terceira ronda: tiram-se os artigos iniciais (o, a, os, as, um,
  # uma) da citação e das opções, para que «A testemunha fixa» contra «Uma testemunha fixa» também conte; e o texto lido
  # sem aspas só desculpa trechos de três palavras ou mais (já sem o artigo), porque «testemunha fixa» também está no
  # texto de cidade/m03 e era precisamente a opção antiga.
  trocas=json.loads((ROOT/'tools/trocas/opcoes-lente-20261030.json').read_text('utf-8'))
  falhas=[];vistas=0
  for t in trocas:
   pagina=(ROOT/t['ficheiro']).read_text('utf-8');antes=json.loads(t['antigo']);depois=json.loads(t['novo'])
   pai=depois;velhas=opcoes(antes)
   if 'f' not in depois:
    # lacuna solta: o f e as outras lacunas estão no «completar» que a contém
    for obj,a,b in objetos(pagina):
     if isinstance(obj.get('lacunas'),list) and depois in obj['lacunas']:pai=obj;break
    velhas=velhas+[o for L in pai.get('lacunas',[]) if L!=depois for o in L['o']]
   novas=[sem_artigo(normal(o)) for o in opcoes(pai)];velhas=[sem_artigo(normal(o)) for o in velhas]
   lido=' '.join(o.get('html','')+' '+o.get('titulo','') for o,_,_ in objetos(pagina) if o.get('t')=='ler')
   aspas=[normal(x) for x in re.findall(r'«([^«»]+)»',lido)];lido=normal(lido)
   proprio=normal(' '.join(v for k,v in pai.items() if isinstance(v,str) and k not in ('f','fe','t','rot','g')))
   for c in citacoes(pai):
    q=sem_artigo(normal(c));vistas+=1
    do_texto=contem(proprio,q) or any(contem(x,q) for x in aspas) or (len(q.split())>=3 and contem(lido,q))
    if len(q)>=2 and any(contem(v,q) for v in velhas) and not any(contem(n,q) for n in novas) and not do_texto:
     falhas.append(t['ficheiro']+' '+t['local']+': «'+c+'»')
  self.assertTrue(vistas)
  self.assertEqual(falhas,[],'\n'.join(falhas))
 def test_feedback_sem_ordinais_de_opcoes(self):
  # 30/10/2026: revisão do #72 (opções equilibradas): o motor baralha as opções de «escolha» e de «pistas»
  # (opcoes(): com mais de três, mostra a certa e duas erradas ao acaso; com três ou menos, baralha-as), por isso o
  # f e o fe não podem referir opções pela posição («a primeira», «a terceira opção», «a opção B»); referem-nas pelo
  # conteúdo. Ordinais seguidos de um nome do texto («o segundo parágrafo», «a terceira estrofe») continuam livres.
  # 30/10/2026: revisão do #72 (opções equilibradas), terceira ronda: apanha também os ordinais depois de vírgula, «e»,
  # «mas» e «só»; e «frase», «proposta», «hipótese» e «pergunta» deixam de ser nomes livres quando o enunciado usa esse
  # nome para as opções («Qual das duas propostas…»).
  falhas=[];vistas=0
  for pasta in medir.PASTAS:
   for p in sorted((ROOT/pasta).rglob('*.html')):
    s=p.read_text('utf-8')
    if not re.search(r'"t":\s*"(?:escolha|pistas)"',s):continue
    # 30/10/2026: as lições piloto da Cidadania (cidadania/piloto) carregam o motor único de fora (assets/licoes/jogo.js):
    # aí confirma-se no ficheiro do motor que as opções se baralham.
    motor=(ROOT/'assets/licoes/jogo.js').read_text('utf-8') if 'assets/licoes/jogo.js' in s else s
    self.assertIn('function opcoes(o,c)',motor,p);self.assertRegex(motor,r'estado\.ord=opcoes\(x\.o,x\.c\)')
    for obj,a,b in objetos(s):
     if obj.get('t') not in ('escolha','pistas'):continue
     fe=obj.get('fe');vistas+=1
     for txt in [obj.get('f') or '']+([fe] if isinstance(fe,str) else [e for e in (fe or []) if isinstance(e,str)]):
      for m in ordinal(obj.get('p','')+' '+obj.get('p2','')).finditer(txt):falhas.append(p.relative_to(ROOT).as_posix()+': '+m.group(0).strip()+' | '+obj.get('p','')[:60])
  # 30/10/2026: Laboratório simples (pedido do docente). Dados dos dois percursos curtos.
  for nome in ('certa-manha','cena-que-falta'):
   s=(ROOT/'assets/formas'/f'{nome}.js').read_text('utf-8')
   for obj in json.loads(s.split('=',1)[1].strip().rstrip(';'))['piloto']:
    for txt in [obj.get('f','')]+[f for f in obj.get('fe',[]) if f]:
     for m in ordinal(obj['p']).finditer(txt):falhas.append(nome+': '+m.group(0))
  self.assertTrue(vistas)
  self.assertEqual(falhas,[],'\n'.join(falhas))
MUDAVEIS=('o','f','p','lacunas')
def contrato(x):
 if isinstance(x.get('o'),list):return [(x['c'],len(x['o']))]
 return [(L['c'],len(L['o'])) for L in x['lacunas']]
def opcoes(x):
 if isinstance(x.get('o'),list):return list(x['o'])
 return [o for L in x.get('lacunas',[]) for o in L['o']]
def normal(s):
 return re.sub(r'\s+',' ',medir.visivel(s)).strip(' .,;:!?…«»"').lower()
def citacoes(x):
 fe=x.get('fe');textos=[x.get('f') or '']+([fe] if isinstance(fe,str) else [e for e in (fe or []) if e])
 return [c for s in textos for c in re.findall(r'«([^«»]+)»',s)+re.findall(r'\*\*([^*]+)\*\*',s)]
def sem_artigo(s):
 return re.sub(r'^(?:o|a|os|as|um|uma)\s+','',s)
def contem(texto,trecho):
 return re.search(r'(?<!\w)'+re.escape(trecho)+r'(?!\w)',texto) is not None
PROIBIDAS=re.compile(r'(?<![\wÀ-ÿ])(?:professor(?:a|es|as)?|jog(?:ar|a[sm]?|o|ou|uei|ámos)|fichas?|folhas?)(?![\wÀ-ÿ])|[·—]',re.I)
_ORD=r'(?:primeir|segund|terceir|quart|quint|penúltim|últim)[ao]s?'
_NOMES_DO_TEXTO=('parágrafo','estrofe','verso','didascália','andar','linha','página','capítulo','etapa','parte','vez','pressuposto','lista','fala','pessoa','senhora')
_NOMES_DAS_OPCOES=('frase','hipótese','proposta','pergunta')
_ORDINAIS={}
def ordinal(enunciado):
 livres=_NOMES_DO_TEXTO+tuple(n for n in _NOMES_DAS_OPCOES if not re.search(r'(?<!\w)'+n+r's?(?!\w)',enunciado,re.I))
 if livres not in _ORDINAIS:
  _ORDINAIS[livres]=re.compile(r'(?:^|[.;:!?]\s+|\*\*|(?:,|\be|\bmas|\bsó)\s+)[AaOo]s?\s+'+_ORD+r'(?=\s*[.,;:!?)*]|\s+(?!(?:'+'|'.join(livres)+r')\w*\b)\w)|\bopç(?:ão|ões)\s+[A-E]\b')
 return _ORDINAIS[livres]
_BASE={}
def da_base(sha,f):
 # o texto do ficheiro na base fixa; None se a base não existir neste checkout (clone raso); falha se a base existir
 # e o ficheiro não estiver lá
 if sha not in _BASE:
  try:_BASE[sha]=subprocess.run(['git','cat-file','-e',sha+'^{commit}'],cwd=ROOT,capture_output=True).returncode==0
  except OSError:_BASE[sha]=False
 if not _BASE[sha]:return None
 r=subprocess.run(['git','show',sha+':'+f],cwd=ROOT,capture_output=True,text=True)
 if r.returncode:raise AssertionError(f+' não existe na base '+sha[:7])
 return r.stdout
def objetos(texto):
 dec=json.JSONDecoder()
 for m in re.finditer(r'\{',texto):
  try:obj,fim=dec.raw_decode(texto,m.start())
  except json.JSONDecodeError:continue
  if isinstance(obj,dict):yield obj,m.start(),fim
if __name__=='__main__':unittest.main()
