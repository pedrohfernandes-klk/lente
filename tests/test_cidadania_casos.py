from pathlib import Path
import unittest,json,re
R=Path(__file__).resolve().parents[1]
def bank(s):
 m=re.search(r'itens:(\[)',s);return json.JSONDecoder().raw_decode(s[m.start(1):])[0]
class Casos(unittest.TestCase):
 def test_five_cases_per_module(self):
  manifest=json.loads((R/'assets/cidadania-casos.json').read_text('utf-8'))
  for mod,old in [('m1',['cid-m1-o-juri','cid-m1-vida-em-direto-hoje']),('m2',['cid-m2-preco-minuto','cid-m2-dentro-da-caixa'])]:
   path='cidadania/m1/biblioteca/index.html' if mod=='m1' else f'cidadania/{mod}/index.html'
   s=(R/path).read_text('utf-8');slugs=old+[x['slug'] for x in manifest if x['module']==mod];self.assertEqual(len(set(slugs)),5)
   for slug in slugs:self.assertTrue((R/f'cidadania/{mod}/{slug}/index.html').exists());self.assertIn(slug+'/',s)
 def test_new_cases_teach_before_deciding_and_have_sources(self):
  keys=[]
  for x in json.loads((R/'assets/cidadania-casos.json').read_text('utf-8')):
   # 28/10/2026: os cartões «Para ver» (marca pv, tools/videos_escolhidos.py) são leituras acrescentadas e ficam fora desta contagem.
   s=(R/f'cidadania/{x["module"]}/{x["slug"]}/index.html').read_text('utf-8');c=[i for i in bank(s) if 'pv' not in i];self.assertEqual(len(c),15);self.assertEqual(sum(i['t']!='ler' and not i.get('reflexao') for i in c),3)
   self.assertEqual([c[i]['t'] for i in [2,5,6,11,12]],['ler','decisao','revelar','decisao','sintese'])
   self.assertEqual([i['g'] for i in c],list(range(len(c))))
   self.assertEqual(len(c[6]['efeitos']),3);self.assertIn('inventad',c[0]['html']);self.assertIn('http',c[-1]['html'])
   for i in c:
    if i['t'] in ['decisao','revelar','posicoes','sintese']:self.assertTrue(i['reflexao'])
   key=re.search(r'chave:"([^"]+)"',s)[1];keys.append(key);self.assertNotIn('guia-docente',s)
   if x['module']=='m2':self.assertNotIn('Ser-se humano',s);self.assertIn('Os algoritmos',s)
  self.assertEqual(len(set(keys)),6)
 def test_branch_state_is_transient_and_displayed(self):
  s=(R/'assets/cidadania-casos.js').read_text('utf-8');self.assertIn('x.efeitos[d.j]',s);self.assertIn('state.primeira',s);self.assertIn('state.revista',s);self.assertNotIn('localStorage',s)
if __name__=='__main__':unittest.main()
