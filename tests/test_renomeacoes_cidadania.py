"""Não confundir títulos novos com ocorrências anteriores em citações."""
import subprocess
import unittest
from pathlib import Path
from renomeacoes_cidadania import renomear, TROCAS

ROOT = Path(__file__).resolve().parents[1]
FICHEIRO = 'cidadania/m1/cid-m1-o-juri/index.html'
BASE = '349d2457e1f056b69c6dda550aace2a6f5377051'


class Renomeacoes(unittest.TestCase):
    def test_base_antiga_e_publicada_com_direitos_humanos(self):
        antiga = subprocess.check_output(['git', 'show', BASE + ':' + FICHEIRO], cwd=ROOT)
        publicada = subprocess.check_output(['git', 'show', 'bbdbec4705477c43ccdff1a93e399bdade2e3a8f:' + FICHEIRO], cwd=ROOT)
        self.assertIn(b'Direitos Humanos', antiga)
        self.assertEqual(renomear(antiga, FICHEIRO), publicada)
        for texto in [publicada, publicada.decode('utf-8')]:
            with self.subTest(binario=isinstance(texto, bytes)):
                self.assertEqual(renomear(texto, FICHEIRO, base_ja_renomeada=True), texto)

    def test_rejeita_contagem_a_menos_ou_a_mais(self):
        antiga = subprocess.check_output(['git', 'show', BASE + ':' + FICHEIRO], cwd=ROOT).decode('utf-8')
        self.assertEqual(TROCAS[FICHEIRO], [['Ser-se humano', 'Humanos', 3]])
        sem_titulo = antiga.replace('Ser-se humano', '')
        duplicado = antiga.replace('Ser-se humano', 'Humanos Humanos')
        for texto in [sem_titulo, duplicado]:
            with self.subTest(texto=texto[:30]):
                with self.assertRaises(AssertionError):
                    renomear(texto, FICHEIRO, base_ja_renomeada=True)


if __name__ == '__main__':
    unittest.main()
