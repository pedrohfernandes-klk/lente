from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import unittest,re,json,subprocess,sys

R=Path(__file__).resolve().parents[1]
BASE='66dc1b818e6f99ed1b0bddf7b5d4f7b5cca59f0d'
class Page(HTMLParser):
 def __init__(self,s):super().__init__();self.ids=[];self.refs=[];self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for k in ('href','src'):
   if a.get(k):self.refs.append(a[k])
def original(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=R).decode()
def bank(s):
 m=re.search(r'itens:(\[)',s);return json.JSONDecoder().raw_decode(s[m.start(1):])[0]
class FichasM1(unittest.TestCase):
 def test_eighteen_unique_pages_and_four_integrated_capsules(self):
  pages=sorted((R/'cidadania/m1/fichas').glob('*/index.html'))
  self.assertEqual([p.parent.name for p in pages],[f'f{n:02}' for n in range(1,19)])
  capsules=[]
  for n,p in enumerate(pages,1):
   s=p.read_text('utf-8');self.assertIn(f'data-ficha="F{n:02}"',s)
   self.assertIn('id="oficina"',s);self.assertIn('data-feedback',s)
   self.assertIn('Exemplo didático',s);self.assertIn('Regressar à Justiça',s)
   self.assertIn('data-m1-done',s);self.assertNotRegex(s,r'<textarea\b')
   capsules+=re.findall(r'data-capsule="([^"]+)"',s)
  self.assertEqual(capsules,['grecia','vicente','moderno','contemporaneo'])
 def test_legacy_banks_and_scripts_survive_css_extraction(self):
  blocks=None
  for n in range(11):
   path=f'cidadania/m1/passo-{n:02}/index.html';old=original(path);new=(R/path).read_text('utf-8')
   self.assertEqual(bank(old),bank(new))
   self.assertEqual(re.findall(r'<script\b[^>]*>.*?</script>',old,re.S),re.findall(r'<script\b[^>]*>.*?</script>',new,re.S))
   css=re.findall(r'<style\b[^>]*>(.*?)</style>',old,re.S)
   if blocks is None:blocks=css
   self.assertEqual(blocks,css)
   self.assertEqual(new.count('cidadania-m1-legado.css'),1)
  self.assertEqual((R/'assets/cidadania-m1-legado.css').read_text('utf-8'),'\n'.join(blocks))
 def test_published_task_is_untouched_and_only_session_three_runs_it(self):
  self.assertEqual((R/'cidadania/projeto/index.html').read_bytes(),subprocess.check_output(['git','show',BASE+':cidadania/projeto/index.html'],cwd=R))
  s=(R/'cidadania/m1/index.html').read_text('utf-8')
  self.assertEqual(len(re.findall(r'data-session-card="\d{2}"',s)),10)
  self.assertIn('href="sessoes/03/" data-continue',s);self.assertNotIn('data-m1-next',s)
  for n in (1,2):
   s=(R/f'cidadania/m1/sessoes/{n:02}/index.html').read_text('utf-8')
   self.assertIn('Percurso já realizado',s);self.assertNotIn('data-session-done',s)
  s=(R/'cidadania/m1/sessoes/03/index.html').read_text('utf-8')
  for text in ['sete grupos','Marina Abramović','The Egg','The Truman Show','60 min','35 min','70 min','5 a 8 minutos']:self.assertIn(text,s)
 def test_sessions_are_complete_and_timed(self):
  import importlib.util
  spec=importlib.util.spec_from_file_location('sessions_content',R/'tools/cidadania_m1_sessoes.py');m=importlib.util.module_from_spec(spec)
  sys.path.insert(0,str(R/'tools'))
  try:spec.loader.exec_module(m)
  finally:sys.path.pop(0)
  self.assertEqual(len(m.SESSOES),10)
  for n,s in enumerate(m.SESSOES,1):
   if s.get('prior'):continue
   self.assertEqual(sum(s['times']),180,n)
   page=(R/f'cidadania/m1/sessoes/{n:02}/index.html').read_text('utf-8')
   self.assertEqual(page.count(' data-stage data-label='),5)
   self.assertIn('data-focus-mode',page);self.assertIn('data-feedback',page)
  self.assertEqual([n for n,s in enumerate(m.SESSOES,1) if s.get('capsule')],[4,5,8,9])
 def test_local_links_and_no_duplicate_ids(self):
  paths=list((R/'cidadania/m1/fichas').glob('*/index.html'))+list((R/'cidadania/m1/sessoes').glob('*/index.html'))+[R/p for p in ['cidadania/m1/index.html','cidadania/projeto/index.html','cidadania/m1/biblioteca/index.html','cidadania/m1/sessoes/index.html','cidadania/m1/oficina-guiao/index.html']]
  for p in paths:
   parser=Page(p.read_text('utf-8'));self.assertEqual(len(parser.ids),len(set(parser.ids)),p)
   for ref in parser.refs:
    u=urlsplit(ref)
    if u.scheme and not ref.startswith('https://pedrohfernandes-klk.github.io/lente/'):continue
    target=R/unquote(u.path.removeprefix('/lente/')) if u.scheme else p.parent/unquote(u.path) if u.path else p
    if target.is_dir():target=target/'index.html'
    self.assertTrue(target.exists(),(p,ref))
    if u.fragment and target.suffix=='.html':self.assertIn(unquote(u.fragment),Page(target.read_text('utf-8')).ids,(p,ref))
 def test_only_v2_key_is_written(self):
  s=(R/'assets/cidadania-m1.js').read_text('utf-8')
  self.assertIn("KEY='lente-cidadania-m1-v2'",s)
  self.assertEqual(re.findall(r'localStorage\.setItem\(([^,]+),',s),['KEY'])
  self.assertNotIn('removeItem',s);self.assertNotIn('localStorage.clear',s)
  self.assertIn('if(projection){check.disabled=true',s)
 def test_source_generation_is_reproducible(self):
  paths=list((R/'cidadania/m1/fichas').glob('*/index.html'))+list((R/'cidadania/m1/sessoes').glob('*/index.html'))+[R/p for p in ['cidadania/m1/index.html','cidadania/projeto/index.html','cidadania/m1/biblioteca/index.html','cidadania/m1/sessoes/index.html','cidadania/m1/oficina-guiao/index.html','index.html','docente/index.html','cidadania/index.html']]
  before={p:p.read_bytes() for p in paths}
  subprocess.run([sys.executable,'-B','tools/generate_cidadania_m1.py'],cwd=R,check=True,capture_output=True)
  for p,content in before.items():self.assertEqual(content,p.read_bytes(),p)

if __name__=='__main__':unittest.main()
