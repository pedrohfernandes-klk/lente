"""30/10/2026: opções equilibradas (pedido do docente)."""
from pathlib import Path
import importlib.util,unittest,json,math,re
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('medir_opcoes',ROOT/'tools/medir_opcoes.py')
medir=importlib.util.module_from_spec(spec);spec.loader.exec_module(medir)
class OpcoesEquilibradas(unittest.TestCase):
 def test_caracteres_visiveis(self):
  self.assertEqual(medir.visivel('<b>Uma</b> _ideia_ &amp; **outra**\n aqui'),'Uma ideia & outra aqui')
 def test_ambito(self):
  self.assertEqual(set(medir.PASTAS),{'cidade','investigar','projetos','fachada','apresentar','estetica','etica','ler','direitos','olhar-e-decidir'})
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
  # continuam fixos, e o resto do objeto também.
  trocas=json.loads((ROOT/'tools/trocas/opcoes-lente-20261030.json').read_text('utf-8'))
  self.assertTrue(trocas)
  for t in trocas:
   self.assertEqual(set(t),{'ficheiro','local','antigo','novo','ocorrencias','achado'})
   self.assertIn(t['ficheiro'].split('/')[0],medir.PASTAS);self.assertTrue(t['achado'])
   antes=json.loads(t['antigo']);depois=json.loads(t['novo'])
   self.assertEqual(contrato(antes),contrato(depois),t['ficheiro']+' '+t['local'])
   self.assertEqual({k:v for k,v in antes.items() if k not in MUDAVEIS},{k:v for k,v in depois.items() if k not in MUDAVEIS})
   actual=(ROOT/t['ficheiro']).read_text('utf-8')
   self.assertEqual(actual.count(t['novo']),t['ocorrencias'],t['ficheiro'])
   for k in MUDAVEIS:
    if antes.get(k)!=depois.get(k):self.assertIsNone(re.search(r'\b(professor|professora|jogar|ficha|folha)\b|[·—]',json.dumps(depois[k],ensure_ascii=False),re.I),t['ficheiro']+' '+t['local'])
 def test_feedback_nao_cita_opcoes_retiradas(self):
  # 30/10/2026: revisão do #72 (opções equilibradas): um f (ou fe) que cita entre «» ou em **negrito** um trecho que
  # estava numa opção no main e já não está em nenhuma opção da pergunta falha. Não falha se o trecho existir noutro
  # sítio da página (no texto lido ou num verso), porque aí a citação é desse texto e não da opção.
  trocas=json.loads((ROOT/'tools/trocas/opcoes-lente-20261030.json').read_text('utf-8'))
  falhas=[];vistas=0
  for t in trocas:
   pagina=(ROOT/t['ficheiro']).read_text('utf-8');antes=json.loads(t['antigo']);depois=json.loads(t['novo'])
   pai=depois;texto=t['novo'];velhas=opcoes(antes)
   if 'f' not in depois:
    # lacuna solta: o f e as outras lacunas estão no «completar» que a contém
    for obj,a,b in objetos(pagina):
     if isinstance(obj.get('lacunas'),list) and depois in obj['lacunas']:pai,texto=obj,pagina[a:b];break
    velhas=velhas+[o for L in pai.get('lacunas',[]) if L!=depois for o in L['o']]
   novas=[normal(o) for o in opcoes(pai)];velhas=[normal(o) for o in velhas]
   resto=normal(pagina.replace(texto,' '))
   for c in citacoes(pai):
    q=normal(c);vistas+=1
    if len(q)>=3 and any(q in v for v in velhas) and not any(q in n for n in novas) and q not in resto:
     falhas.append(t['ficheiro']+' '+t['local']+': «'+c+'»')
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
def objetos(texto):
 dec=json.JSONDecoder()
 for m in re.finditer(r'\{',texto):
  try:obj,fim=dec.raw_decode(texto,m.start())
  except json.JSONDecodeError:continue
  if isinstance(obj,dict):yield obj,m.start(),fim
if __name__=='__main__':unittest.main()
