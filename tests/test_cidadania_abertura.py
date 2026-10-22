from pathlib import Path
import re,json,unittest
from urllib.parse import urlsplit
R=Path(__file__).resolve().parents[1]
class Abertura(unittest.TestCase):
 def test_berger_is_support_not_first_sequential_step(self):
  s=(R/'cidadania/m1/index.html').read_text('utf-8');support=re.search(r'<details class="cid-disclosure" id="apoio-imagens">.*?</details>',s,re.S)[0]
  self.assertIn('href="passo-00/"',support);self.assertIn('Apoio · imagens',support);self.assertNotIn('data-g=',support)
  arc=re.search(r'<nav[^>]*class="arco-faixa".*?</nav>',s,re.S)[0];self.assertNotIn('data-id="passo-00"',arc)
  self.assertIn('d.id!=="passo-00"',s);self.assertIn('id="proxima-aula"',s)
 def test_exercises_repeat_without_progress_or_grade(self):
  s=(R/'cidadania/m1/abertura/index.html').read_text('utf-8');self.assertEqual(s.count('type="application/json"'),2);self.assertNotIn('localStorage',s);self.assertNotRegex(s,r'<(?:input|textarea)\b')
  for data in re.findall(r'<script type="application/json"[^>]*>(.*?)</script>',s,re.S):
   d=json.loads(data);self.assertEqual(len(d['feedback']),3);self.assertTrue(all(d['feedback']))
 def test_opening_local_links(self):
  for file in ['cidadania/m1/abertura/index.html','cidadania/m1/index.html']:
   p=R/file;s=re.sub(r'<script\b.*?</script>','',p.read_text('utf-8'),flags=re.S)
   for href in re.findall(r'href="([^"]+)"',s):
    u=urlsplit(href)
    if u.scheme and not href.startswith('https://pedrohfernandes-klk.github.io/lente/'):continue
    target=R/u.path.removeprefix('/lente/') if u.scheme else p.parent/u.path if u.path else p
    if target.is_dir():target=target/'index.html'
    self.assertTrue(target.exists(),href)
    if u.fragment and target.suffix=='.html':self.assertIn('id="'+u.fragment+'"',target.read_text('utf-8'),href)
if __name__=='__main__':unittest.main()
