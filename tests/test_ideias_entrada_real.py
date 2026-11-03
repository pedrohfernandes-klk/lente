"""A entrada deriva das sessões reais e conserva a transformação exata."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('eixo', ROOT/'tools/laboratorio_ideias_entrada.py')
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)

class EntradaReal(unittest.TestCase):
    def test_idempotente(self):
        s = (ROOT/'index.html').read_text('utf-8')
        self.assertEqual(E.instalar_raiz(s), s)
        self.assertEqual(s.count('data-ideias-sessoes>'), 1)

    def test_sessoes_publicadas(self):
        dados = E.sessoes()
        self.assertEqual([d['id'] for d in dados], ['ideias-s01', 'ideias-s02'])
        for d in dados:
            self.assertIn(d['chave'], E.acao('../'))
            self.assertIn(d['saida'].removesuffix('index.html'), E.acao('../'))

    def test_catalogo_unico(self):
        s = (ROOT/'narrativas/index.html').read_text('utf-8')
        self.assertEqual(s.count('id="explorar"'), 1)
        for grupo, recursos in __import__('json').loads((ROOT/'assets/laboratorio/ideias-explorar.json').read_text('utf-8')):
            for nome, descricao, url, requisito in recursos:
                self.assertEqual(s.count('href="'+url+'"'), 1)

if __name__ == '__main__':
    unittest.main()
