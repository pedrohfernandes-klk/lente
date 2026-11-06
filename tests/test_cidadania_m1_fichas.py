from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import unittest,re,json,subprocess,sys

R=Path(__file__).resolve().parents[1]
import grupos146  # 05/11/2026: decisão 146
BASE='66dc1b818e6f99ed1b0bddf7b5d4f7b5cca59f0d'
class Page(HTMLParser):
 def __init__(self,s):super().__init__();self.ids=[];self.refs=[];self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for k in ('href','src'):
   if a.get(k):self.refs.append(a[k])
# 30/10/2026: pedido do docente (perguntas em português europeu, «Qual das citações…» e não «Qual citação…»): o
# original passa pelas trocas de tools/trocas/lingua-perguntas-20261030.json antes de se comparar; tudo o resto continua
# a ter de ser igual, byte a byte.
LINGUA=json.loads((R/'tools/trocas/lingua-perguntas-20261030.json').read_text('utf-8'))
def com_lingua(path,s):
 for t in LINGUA:
  if t['ficheiro']==path:s=s.replace(t['antigo'],t['novo'])
 return s
def original(path):return com_lingua(path,subprocess.check_output(['git','show',BASE+':'+path],cwd=R).decode())
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
   # 05/11/2026: decisão 146 (discussões em turma, trabalhos individuais): desfazem-se só as trocas do manifesto fechado, com contagem exata.
   if path in grupos146.TROCAS:new=grupos146.desfazer(new,path)
   self.assertEqual(bank(old),bank(new))
   # 05/11/2026: decisão 163 (menus). Os scripts antigos ficam todos, iguais e pela mesma ordem; junta-se exatamente um,
   # o do menu ≡ (assets/licoes/menu.js, com defer, no fim do corpo).
   novos=re.findall(r'<script\b[^>]*>.*?</script>',new,re.S)
   self.assertEqual(novos[-1],'<script defer src="../../../assets/licoes/menu.js?v=20261105-163"></script>')
   self.assertEqual(re.findall(r'<script\b[^>]*>.*?</script>',old,re.S),novos[:-1])
   css=re.findall(r'<style\b[^>]*>(.*?)</style>',old,re.S)
   if blocks is None:blocks=css
   self.assertEqual(blocks,css)
   self.assertEqual(new.count('cidadania-m1-legado.css'),1)
  self.assertEqual((R/'assets/cidadania-m1-legado.css').read_text('utf-8'),'\n'.join(blocks))
 def test_published_task_is_untouched_and_only_session_three_runs_it(self):
  # 05/11/2026: decisão 146 (discussões em turma, trabalhos individuais): o enunciado muda só pelas trocas do manifesto fechado (tarefa e entrega individuais), com contagem exata.
  self.assertEqual(grupos146.desfazer((R/'cidadania/projeto/index.html').read_text('utf-8'),'cidadania/projeto/index.html').encode('utf-8'),subprocess.check_output(['git','show',BASE+':cidadania/projeto/index.html'],cwd=R))
  s=(R/'cidadania/m1/index.html').read_text('utf-8')
  self.assertEqual(len(re.findall(r'data-session-card="\d{2}"',s)),10)
  self.assertIn('href="sessoes/03/" data-continue',s);self.assertNotIn('data-m1-next',s)
  # 27/10/2026 (molde das sessões): as sessões 01 e 02 já decorreram; ficam sem registo pessoal e sem
  # avisos sobre o que a turma já estudou, que pertencem ao guia do docente. O plano da sessão 03
  # (sete grupos, 10, 5, 60, 35 e 70 minutos) confere-se no guia; a página do aluno só diz o que fazer.
  for n in (1,2):
   s=(R/f'cidadania/m1/sessoes/{n:02}/index.html').read_text('utf-8')
   self.assertNotIn('data-session-done',s);self.assertNotIn('Percurso já realizado',s)
  # 06/11/2026 (decisões 166 a 168): no endereço da sessão 03 está agora a lição no molde final (tools/licoes/cidadania-m1-s03.json),
  # escrita inteira pelo seu gerador e conferida em tests/test_molde_cidadania.py (SessaoS03) e tests/test_cidadania_m1_molde.py; a
  # obra _The Egg_ entra nela como «Recupera» (decisão 144). Continua sem registo pessoal, sem avisos sobre o que a turma já estudou
  # e com a ligação ao enunciado da Pergunta Humana.
  s=(R/'cidadania/m1/sessoes/03/index.html').read_text('utf-8')
  self.assertIn('molde-cidadania',s);self.assertIn('"chave": "epi-cid-m1-s03"',s);self.assertIn('href=\\"../../../projeto/#pergunta-resposta\\"',s)
  self.assertNotIn('data-session-done',s);self.assertNotIn('conhecimentos prévios',s)
  # 06/11/2026: só _The Egg_ entra na sessão 03 nova; as outras duas obras da sessão antiga continuam proibidas nela, como antes.
  for text in ['Marina Abramović','The Truman Show']:self.assertNotIn(text,s)
  g=(R/'cidadania/m1/sessoes/index.html').read_text('utf-8')
  # 05/11/2026: decisão 146 (discussões em turma, trabalhos individuais): os sete grupos da sessão 03 passam a mostras curtas individuais.
  for text in ['Mostras curtas individuais','Abramović','The Egg','Truman','Recupera · 10 min','Vê · 5 min','Investiga · 60 min','Prepara · 35 min','Apresenta · 70 min']:self.assertIn(text,g)
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
   # 06/11/2026 (decisões 166 a 168): no endereço da sessão 03 está agora a lição no molde final, sem os cinco momentos (conferida em
   # tests/test_molde_cidadania.py, SessaoS03); os momentos continuam exigidos às sessões 04 a 10 publicadas.
   if n==3:continue
   page=(R/f'cidadania/m1/sessoes/{n:02}/index.html').read_text('utf-8')
   # 06/11/2026 (sessão 07 no molde): uma sessão cujo .json tem o campo «molde» passou à lição no molde final, no mesmo endereço
   # (agora também a 07); confere-se aqui que é essa lição, e o contrato do molde confere-se em tests/test_molde_cidadania.py. As
   # outras continuam a ter de ter os cinco momentos e os controlos de sempre.
   if json.loads((R/f'tools/licoes/cidadania-m1-s{n:02}.json').read_text('utf-8')).get('molde'):
    self.assertIn('molde-cidadania',page,n);self.assertNotIn('data-stage',page,n);continue
   self.assertEqual(page.count(' data-stage data-label='),5)
   # 27/10/2026: o modo «um momento de cada vez» deixa de ser opcional (data-focus-mode); a sessão abre
   # com «Começar» e avança com Anterior e Seguinte.
   self.assertIn('data-start',page);self.assertIn('data-step-controls',page);self.assertIn('data-feedback',page)
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
