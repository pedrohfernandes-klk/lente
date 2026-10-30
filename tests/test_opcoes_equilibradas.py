"""30/10/2026: opções equilibradas (pedido do docente)."""
from pathlib import Path
import importlib.util,unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('medir_opcoes',ROOT/'tools/medir_opcoes.py')
medir=importlib.util.module_from_spec(spec);spec.loader.exec_module(medir)
class OpcoesEquilibradas(unittest.TestCase):
 def test_caracteres_visiveis(self):
  self.assertEqual(medir.visivel('<b>Uma</b> _ideia_ &amp; **outra**\n aqui'),'Uma ideia & outra aqui')
 def test_ambito(self):
  self.assertNotIn('narrativas',medir.PASTAS);self.assertNotIn('cidadania',medir.PASTAS)
 def test_sem_denunciadoras(self):
  perguntas=list(medir.perguntas(ROOT));self.assertTrue(perguntas,'A medição não encontrou perguntas')
  falhas=[f"{q['pagina']} #{q['numero']}: {q['comprimentos']}, certa {q['certa']}" for q in perguntas if q['denunciadora']]
  self.assertEqual(falhas,[],str(len(falhas))+' denunciadoras:\n'+'\n'.join(falhas))
if __name__=='__main__':unittest.main()
