from pathlib import Path
import re,unittest
from urllib.parse import urlsplit
R=Path(__file__).resolve().parents[1]
class AulasM2(unittest.TestCase):
 def test_ten_sessions_reachable_from_module(self):
  index=(R/'cidadania/m2/aulas/index.html').read_text('utf-8')
  self.assertIn('cidadania/m2/aulas/',(R/'cidadania/m2/index.html').read_text('utf-8'))
  for n in range(1,11):self.assertIn(f'cidadania/m2/aulas/{n:02d}/',index)
 def test_local_links_and_anchors(self):
  for p in (R/'cidadania/m2/aulas').rglob('*.html'):
   for href in re.findall(r'href="([^"]+)"',p.read_text('utf-8')):
    u=urlsplit(href)
    if u.scheme and not href.startswith('https://pedrohfernandes-klk.github.io/lente/'):continue
    target=R/u.path.removeprefix('/lente/') if u.scheme else p.parent/u.path
    if target.is_dir():target=target/'index.html'
    self.assertTrue(target.exists(),(str(p),href))
    if u.fragment:self.assertIn('id="'+u.fragment+'"',target.read_text('utf-8'),href)
 def test_materials_are_not_a_second_progress_or_assessment_engine(self):
  for p in (R/'cidadania/m2/aulas').rglob('*.html'):
   s=p.read_text('utf-8');self.assertNotIn('localStorage',s);self.assertNotRegex(s,r'<(?:input|textarea)\b');self.assertNotIn('guia-docente',s)
  for n in range(1,11):
   s=(R/f'cidadania/m2/aulas/{n:02d}/index.html').read_text('utf-8');self.assertIn('cidadania/m2/',s);self.assertIn('Antes de avançar',s)
 def test_nagel_has_a_primary_source_and_distinguishes_application(self):
  s=(R/'cidadania/m2/aulas/04/index.html').read_text('utf-8');self.assertIn('Thomas Nagel',s);self.assertIn('1974',s);self.assertIn('faculty.fiu.edu',s);self.assertIn('aplicação desta aula',s)
if __name__=='__main__':unittest.main()
