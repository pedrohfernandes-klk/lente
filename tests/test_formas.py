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
  self.assertEqual(by['kafka']['translator'],'Helena Topa')
  self.assertIn('não confundir',by['borges']['locator'].lower())
  self.assertNotIn('Pastelaria',by['cesariny']['work'])

 def test_legacy_paths_and_keys_remain(self):
  for name in ('ines','frei-luis','cesario','chuva','torneol','restelo','maias','bras-cubas'):
   self.assertTrue((ROOT/'narrativas/corta'/name/'index.html').exists())
  entry=(ROOT/'narrativas/index.html').read_text('utf-8')
  for anchor in ('ler-como-quem-escreve','treinar','criar','corta','aulas','experimentar','vidas-e-ideias'):
   self.assertIn('id="'+anchor+'"',entry)
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
  self.assertTrue((ROOT/'assets/formas/carteira-linha.png').is_file())

if __name__=='__main__':unittest.main()
