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
  for p,r in medir.resumir(list(medir.perguntas(ROOT)),'pagina').items():
   self.assertLessEqual(r['certaMaisLonga'],math.ceil(r['esperadoMaisLonga']),p)
   if r['perguntas']>1:self.assertLess(r['certaMaisCurta'],r['perguntas'],p)
 def test_trocas_preservam_os_contratos(self):
  trocas=json.loads((ROOT/'tools/trocas/opcoes-lente-20261030.json').read_text('utf-8'))
  self.assertTrue(trocas)
  for t in trocas:
   self.assertEqual(set(t),{'ficheiro','local','antigo','novo','ocorrencias','achado'})
   self.assertIn(t['ficheiro'].split('/')[0],medir.PASTAS);self.assertTrue(t['achado'])
   antes=json.loads(t['antigo']);depois=json.loads(t['novo'])
   self.assertEqual(antes['c'],depois['c']);self.assertEqual(len(antes['o']),len(depois['o']))
   self.assertEqual({k:v for k,v in antes.items() if k not in ('o','f')},{k:v for k,v in depois.items() if k not in ('o','f')})
   actual=(ROOT/t['ficheiro']).read_text('utf-8')
   self.assertEqual(actual.count(t['novo']),t['ocorrencias'],t['ficheiro'])
   for k in ('o','f'):
    if antes.get(k)!=depois.get(k):self.assertIsNone(re.search(r'\b(professor|professora|jogar|ficha|folha)\b|[·—]',str(depois[k]),re.I))
if __name__=='__main__':unittest.main()
