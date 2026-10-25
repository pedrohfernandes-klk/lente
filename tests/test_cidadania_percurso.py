from pathlib import Path
import subprocess,re,unittest
R=Path(__file__).resolve().parents[1]
class Percurso(unittest.TestCase):
 def test_private_guide_absent_from_public_tree_and_ancestry(self):
  self.assertFalse((R/'cidadania/m1/guia-docente/index.html').exists())
  for folder in ['cidadania','docs','assets']:
   for p in (R/folder).rglob('*'):
    if p.is_file() and p.suffix in ['.html','.md','.css','.js']:
     self.assertNotIn('/guia-docente/',p.read_text('utf-8'),str(p))
  names=subprocess.check_output(['git','log','--format=','--name-only','origin/main..HEAD'],cwd=R).decode()
  self.assertNotIn('cidadania/m1/guia-docente/',names)
 def test_five_meetings_and_prequel_direct_links(self):
  s=(R/'cidadania/m1/index.html').read_text('utf-8')
  for d in ['2026-10-28','2026-11-04','2026-11-11','2026-11-18','2026-11-25']:self.assertIn('id="aula-'+d+'"',s)
  for x in ['id="prequela"','hora de pesquisa','cidadania/m2/#projeto-filosofico','cidadania/m1/passo-00/','cidadania/m1/cid-m1-butler-singer/']:self.assertIn(x,s)
 def test_m2_assessment_progress_and_original_destinations(self):
  for path in ['cidadania/m2/index.html','cidadania/contra-feed/index.html']:
   old=subprocess.check_output(['git','show','origin/main:'+path],cwd=R).decode();new=(R/path).read_text('utf-8')
   self.assertEqual(re.findall(r'<table>.*?</table>',old,re.S),re.findall(r'<table>.*?</table>',new,re.S))
   for href in re.findall(r'href="([^"]+)"',old):self.assertIn('href="'+href+'"',new)
   # 25/10: o tema universal acrescenta apenas o seu carregamento independente.
   # Todos os restantes scripts, incluindo progresso, conservam-se byte a byte.
   def engines(s):
    return [script for script in re.findall(r'<script\b.*?</script>',s,re.S) if not re.search(r'src="[^\"]*assets/appearance\.js',script)]
   self.assertEqual(engines(old),engines(new))
  s=(R/'cidadania/contra-feed/index.html').read_text('utf-8');self.assertIn('Não há uma conclusão filosófica única premiada',s)
if __name__=='__main__':unittest.main()
