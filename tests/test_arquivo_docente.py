from pathlib import Path
import re,unittest
R=Path(__file__).resolve().parents[1]
class ArquivoDocente(unittest.TestCase):
 def test_arquivo_nao_regressa_como_porta_principal(self):
  s=(R/'index.html').read_text('utf-8')
  self.assertNotRegex(s,r'<article\b[^>]*id="inicio-vozes"')
  self.assertNotIn('href="#inicio-vozes"',s)
  self.assertIn('id="inicio-vozes"',s) # endereço antigo não fica sem destino
  # 26/10: a boia abre a área docente; o arquivo conserva o seu id.
  self.assertIn('href="docente/"',s)
  self.assertNotIn('treinar a mão',s)
 def test_colecoes_e_guioes_acessiveis_pelo_docente(self):
  s=(R/'docente/index.html').read_text('utf-8')
  self.assertIn('id="arquivo"',s);self.assertIn('href="../vozes/#arquivo"',s)
  for href in re.findall(r'href="(../vozes/[^"]*)"',s):
   path=(R/'docente'/href.split('#')[0]).resolve()
   self.assertTrue((path/'index.html').exists(),href)
  v=(R/'vozes/index.html').read_text('utf-8')
  self.assertIn('id="arquivo"',v);self.assertIn('href="../docente/#arquivo"',v)
  self.assertIn('id="vidas-referencias"',v)
 def test_mapa_e_lab_nao_promovem_o_conjunto_como_percurso(self):
  n=(R/'narrativas/index.html').read_text('utf-8')
  self.assertNotIn('<span class="bundle-label">Vidas e vozes</span>',n)
  s=(R/'mapa/index.html').read_text('utf-8')
  self.assertIn('Arquivo do docente',s)
  self.assertIn('<details><summary>Consultar materiais de reserva</summary>',s)
