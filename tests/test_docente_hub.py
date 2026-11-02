from pathlib import Path
from html.parser import HTMLParser
import unittest

ROOT=Path(__file__).resolve().parents[1]

class Anchors(HTMLParser):
 def __init__(self,s):super().__init__();self.links=[];self.ids=set();self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if t=='a':self.links.append(a.get('href',''))

class TeacherHub(unittest.TestCase):
 def test_guides_and_archive_are_reachable_from_the_same_entry(self):
  source=(ROOT/'docente/index.html').read_text('utf-8');page=Anchors(source)
  for ident in ['portugues','conduzir-aula','tarefa-90','reserva','arquivo','guia-1','guia-2','guia-3','guia-4']:
   self.assertIn(ident,page.ids)
  for href in ['https://pedrohfernandes-klk.github.io/pt/m1/aulas/','https://pedrohfernandes-klk.github.io/pt/m4/aulas/','../sidequests/','../vozes/#arquivo','guia-docente.pdf']:
   self.assertIn(href,page.links)
  for href in page.links:
   if href.startswith('#'):self.assertIn(href[1:],page.ids)
  self.assertTrue((ROOT/'docente/guia-docente.pdf').is_file())
  self.assertIn('60 min',source)
  self.assertIn('fotografias legíveis',source)
 def test_home_buoy_targets_the_hub(self):
  s=(ROOT/'index.html').read_text('utf-8')
  # 01/11/2026: a revisão transfere a âncora para a saída com texto e elimina o ícone duplicado.
  self.assertIn('<a id="inicio-vozes" href="docente/">Para o docente <span aria-hidden="true">→</span></a>',s)
  self.assertNotIn('<a id="inicio-vozes" class="teacher-archive"',s)
  self.assertEqual(s.count('id="inicio-vozes"'),1)

if __name__=='__main__':unittest.main()
