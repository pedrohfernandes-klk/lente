from pathlib import Path
import json,re,hashlib,unittest,datetime
ROOT=Path(__file__).resolve().parents[1]
def text(p):return (ROOT/p).read_text('utf-8')
BASE=json.loads((ROOT/'tests/fixtures/cidadania-m1-baseline.json').read_text('utf-8'))
class CidadaniaM1(unittest.TestCase):
 def test_old_destinations_and_images_preserved(self):
  for p in ['cidadania/index.html','cidadania/m1/index.html','cidadania/projeto/index.html']:
   a,b=BASE["files"][p],text(p)
   for href in a['hrefs']:
    # Intermediate category menus were removed; their incoming anchors remain valid.
    if p=='cidadania/index.html' and href in ['#aulas-e-percursos','#investigar-e-criar','#preparar-e-rever']:
     self.assertIn('id="'+href[1:]+'"',b)
    else:self.assertIn('href="'+href+'"',b,(p,href))
   # The new module previews are additions; every original image stays unchanged.
   original=b
   if p=='cidadania/index.html':
    previews=re.findall(r'<span class="cid-module-image">(.*?)</span>',b,re.S)
    self.assertEqual(len(previews),2)
    self.assertIn('hals.webp',previews[0]);self.assertIn('turco.webp',previews[1])
    original=re.sub(r'<span class="cid-module-image">.*?</span>','',b,flags=re.S)
   self.assertEqual(a['images_sha256'],[hashlib.sha256(x.encode()).hexdigest() for x in re.findall(r'<img[^>]+src="([^"]+)"',original)])
   for id in a['ids']:self.assertIn('id="'+id+'"',b)
 def test_progress_ids_preserved(self):
  p='cidadania/m1/index.html';a,b=BASE["files"][p],text(p)
  def ids(s):return json.JSONDecoder().raw_decode(s.split('window.EPI_MISSOES=',1)[1])[0]
  self.assertEqual(BASE["missions"],ids(b));self.assertEqual(len(ids(b)),13);self.assertIn('de 10 passos principais',b);self.assertIn('de 3 atividades de apoio',b);self.assertIn('epi-cidadania-m1',b)
 def test_weights_and_requirements_preserved(self):
  for p in ['cidadania/index.html','cidadania/projeto/index.html']:
   self.assertEqual([t.replace('cada aula','cada exploração') for t in BASE['files'][p]['tables']],re.findall(r'<table>.*?</table>',text(p),re.S))
  s=text('cidadania/projeto/index.html');self.assertIn('5 a 8 minutos',s)
  for x in ['av-diario','av-laboratorio','av-dossie','av-teatro','investigar/passo-03/','investigar/passo-08/','investigar/passo-09/']:self.assertIn(x,s)
 def test_local_links_and_fragments(self):
  from urllib.parse import urlsplit,unquote
  for p in ['cidadania/index.html','cidadania/m1/index.html','cidadania/projeto/index.html','cidadania/m2/index.html','cidadania/contra-feed/index.html','cidadania/m1/cid-m1-butler-singer/index.html']:
   for href in re.findall(r'href="([^"]+)"',re.sub(r'<(script|style)\b[^>]*>.*?</\1>','',text(p),flags=re.S)):
    u=urlsplit(href)
    if u.scheme and not href.startswith('https://pedrohfernandes-klk.github.io/lente/'):continue
    target=ROOT/unquote(u.path.removeprefix('/lente/')) if u.scheme else ((ROOT/p).parent/unquote(u.path) if u.path else ROOT/p)
    if target.is_dir():target=target/'index.html'
    self.assertTrue(target.exists(),(p,href))
    if u.fragment and target.suffix=='.html':self.assertIn('id="'+u.fragment+'"',target.read_text('utf-8'),(p,href))
if __name__=='__main__':unittest.main()
