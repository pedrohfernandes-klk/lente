from pathlib import Path
import importlib.util,re,subprocess,unittest
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('menus',R/'tools/menus_acabamento.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
BASE='39b391f7969e9a99f04d9b16f715ea0e4bd183ea'
class Menus(unittest.TestCase):
 def test_preservacao_integral(self):
  for nome in M.PAGES:
   with self.subTest(page=nome):
    old=subprocess.check_output(['git','show',BASE+':'+nome],cwd=R)
    now=(R/nome).read_bytes()
    self.assertEqual(now.count(b' data-menus-acabamento="20261103"'),1)
    self.assertEqual(now.count(b'<link data-menus-acabamento-css '),1)
    stripped=re.sub(rb'<link data-menus-acabamento-css[^>]*>',b'',now).replace(b' data-menus-acabamento="20261103"',b'')
    if nome=='mapa/index.html':
     for extra in [b'<!-- menus-apoios --><details class="menu-apoios"><summary>Outros recursos do Laborat\xc3\xb3rio</summary><div>',b'</div></details><!-- /menus-apoios -->',b' class="menu-curso-principal"']:
      self.assertEqual(stripped.count(extra),1);stripped=stripped.replace(extra,b'')
    self.assertEqual(old,stripped,'Texto, scripts, dados, destinos e ordem conservados byte a byte')
 def test_regeneracao(self):
  for nome in M.PAGES:
   s=(R/nome).read_text('utf-8');self.assertEqual(M.instalar(s,nome),s)
if __name__=='__main__':unittest.main()
