from pathlib import Path
import json,re,subprocess,unittest
R=Path(__file__).resolve().parents[1]
def bank(s):
 m=re.search(r'itens:(\[)',s);return json.JSONDecoder().raw_decode(s[m.start(1):])[0]
class Anomalias(unittest.TestCase):
 def test_images_and_card_order_preserved(self):
  for rel in ['m1/passo-00','m2/passo-00','m2/passo-01']:
   path='cidadania/'+rel+'/index.html';s=(R/path).read_text('utf-8');old=bank(subprocess.check_output(['git','show','origin/main:'+path],cwd=R).decode());new=bank(s)
   self.assertEqual([x['t'] for x in old],[x['t'] for x in new])
   for a,b in zip(old,new):
    if a['t']=='imagens':self.assertEqual(a['imagens'],b['imagens'])
    if b['t']=='posicao':self.assertTrue(b['reflexao'])
   self.assertIn('x.t!=="ler"&&!x.reflexao',s);self.assertIn('hist[i]=neutro?"ler":ok',s)
 def test_visual_question_is_precise_and_feedback_covers_every_crop(self):
  s=(R/'cidadania/m1/passo-00/index.html').read_text('utf-8');c=bank(s)[6];self.assertNotIn('frase que o quadro',c['p']);self.assertIn('mais de perto',c['p']);self.assertEqual(len(c['feedback']),len(c['imagens']));self.assertIn('três',c['nota']);self.assertIn('também contém',c['feedback'][2]);self.assertIn('x.feedback[j]',s)
 def test_choices_have_diagnostic_feedback(self):
  for rel,i in [('m1/passo-00',7),('m2/passo-00',5),('m2/passo-01',5)]:
   c=bank((R/f'cidadania/{rel}/index.html').read_text('utf-8'))[i];self.assertEqual(len(c['o']),len(c['fe']));self.assertTrue(all(c['fe'][j] for j in range(len(c['o'])) if j!=c['c']))
if __name__=='__main__':unittest.main()
