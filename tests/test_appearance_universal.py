"""Guarda de publicação: nenhuma página completa fica sem o tema comum."""
from pathlib import Path
import re,unittest
R=Path(__file__).resolve().parents[1]
class AppearanceCoverage(unittest.TestCase):
 def test_every_html_document_has_one_reachable_theme_pair(self):
  pages=[p for p in R.rglob('*.html') if not any(x in ('.git','tests','_qa') for x in p.relative_to(R).parts)]
  self.assertTrue(pages)
  for p in pages:
   s=p.read_text('utf-8')
   if not re.search(r'</head\s*>',s,re.I):continue
   with self.subTest(page=p.relative_to(R).as_posix()):
    for asset in ('css','js'):
     refs=re.findall(r'(?:href|src)="([^"]*assets/appearance\.'+asset+r'[^\"]*)"',s)
     self.assertEqual(len(refs),1)
     self.assertTrue((p.parent/refs[0].split('?')[0]).resolve().is_file())
    self.assertIn('data-appearance-site=',s)
 def test_projection_engines_remain_theme_independent(self):
  for name in ('projection.js','projection-launcher.js'):
   s=(R/'assets'/name).read_text('utf-8')
   self.assertNotIn('epi-theme',s)
