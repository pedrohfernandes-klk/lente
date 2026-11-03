"""03/11/2026: contrato do modelo, sem reduzir as exigências das sessões existentes."""
import importlib.util,json,pathlib,re,unittest
R=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ll',R/'tools/licoes_lente.py');G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
D=json.loads((R/'tools/modelos/cidadania-m1-s01.json').read_text('utf-8'))
class Modelo(unittest.TestCase):
 def test_banco_e_pagina(self):
  self.assertEqual(G.validar(D),[])
  self.assertEqual((R/D['saida']).read_text('utf-8'),G.pagina(D))
  self.assertEqual(len(D['cartoes']),20)
  fazer=[c for c in D['cartoes'] if c['t']!='ler']
  self.assertEqual(len(fazer),14)
  self.assertEqual({c['t'] for c in fazer},{'escolha','vf','emparelhar','sublinhar','ordenar'})
 def test_material_e_alternativa(self):
  for c in D['cartoes']:
   self.assertNotIn('data-yt=',c.get('html',''))
   if c['t']=='ler':self.assertLessEqual(len(G.visivel(c['html']).split()),95)
  self.assertIn('Caso inventado',D['cartoes'][0]['html'])
  self.assertIn('CC BY 2.0',D['cartoes'][1]['html'])
  self.assertIn('intromissões arbitrárias',D['cartoes'][4]['html'])
  self.assertIn('pelo ensino e pela educação',D['cartoes'][8]['html'])
  self.assertEqual(D['cartoes'][12]['certas'],[3,4])
  self.assertEqual(D['cartoes'][12]['frase'].split()[3:5],['a','atingir'])
 def test_isolamento_e_visor(self):
  s=G.pagina(D)
  self.assertIn('"chave": "ensaio-epi-cid-m1-s01"',s)
  self.assertIn('noindex, nofollow',s)
  self.assertIn('assets/ampliar-documentos.js',s)
  self.assertEqual(D['saida'],'demonstracoes/cidadania-sessao-modelo/index.html')
  self.assertTrue((R/'cidadania/piloto/m1-s01/index.html').is_file())
if __name__=='__main__':unittest.main()
