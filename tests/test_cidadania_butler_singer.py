from pathlib import Path
import json,re,unittest
ROOT=Path(__file__).resolve().parents[1];PATH='cidadania/m1/cid-m1-butler-singer/index.html'
def bank():
 s=(ROOT/PATH).read_text('utf-8');m=re.search(r'itens:(\[)',s);return json.JSONDecoder().raw_decode(s[m.start(1):])[0]
class ButlerSinger(unittest.TestCase):
 def test_bank_structure_and_sources(self):
  c=bank();self.assertEqual(len(c),15);self.assertEqual(sum(x.get('reflexao',False) for x in c),2);self.assertEqual(sum(x['t']!='ler' and not x.get('reflexao') for x in c),4)
  text=json.dumps(c,ensure_ascii=False);self.assertIn('Situação inventada',text);self.assertIn('não citação literal',text);self.assertIn('versobooks.com',text);self.assertIn('givingwhatwecan.org',text);self.assertIn('petersinger.info',text);self.assertIn('eficácia equivalente',text)
 def test_teaching_before_application_and_open_positions(self):
  c=bank();self.assertIn('Berkeley',c[1]['html']);self.assertIn('Melbourne',c[2]['html']);self.assertEqual(c[5]['t'],'ler');self.assertEqual(c[7]['t'],'ler')
  for i in [4,11]:self.assertTrue(c[i]['reflexao']);self.assertNotIn('c',c[i]);self.assertEqual(len(c[i]['opcoes']),3)
  self.assertIn('importância moral comparável',c[7]['html']);self.assertIn('não mede o valor',c[5]['html']);self.assertIn('oralmente ou no caderno',c[13]['html'])
 def test_neutral_feedback_and_independent_storage(self):
  s=(ROOT/PATH).read_text('utf-8');self.assertIn('x.t!=="ler"&&!x.reflexao',s);self.assertIn('neutro?"Para discutir."',s);self.assertIn('if(!neutro&&ok)',s);self.assertIn('hist[i]=neutro?"ler":ok',s);self.assertIn('var K="epi-cidadania-m1-butler-singer-conclusao"',s);self.assertIn('chave:"epi-cidadania-m1-butler-singer"',s);self.assertNotIn('S.feitas["passo-08"]',s)
if __name__=='__main__':unittest.main()
