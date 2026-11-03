"""02/11/2026: o pedido 2 de Ideias só pode mudar o cache dos ficheiros na Cidadania."""
from pathlib import Path
import re
import json
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = 'fbfb8509d6e104f00811321d95ed4d999f8df2cd'
RENOMEACOES = json.loads((ROOT / 'tests/fixtures/cidadania-nomes-20261103.json').read_text(encoding='utf-8'))


class CidadaniaBase(unittest.TestCase):
    def test_cidadania_igual_a_base(self):
        nomes = subprocess.check_output(
            ['git', 'ls-tree', '-r', '--name-only', BASE, '--',
             'cidadania/piloto', 'cidadania/m1', 'assets/licoes/cidadania.css'], cwd=ROOT
        ).decode().splitlines()
        self.assertGreater(len(nomes), 50)
        for nome in nomes:
            with self.subTest(ficheiro=nome):
                antes = subprocess.check_output(['git', 'show', f'{BASE}:{nome}'], cwd=ROOT)
                # 03/11/2026: #107 autoriza só os títulos deste manifesto fechado.
                for antigo, novo, quantidade in RENOMEACOES.get(nome, []):
                    self.assertEqual(antes.count(antigo.encode()), quantidade)
                    antes = antes.replace(antigo.encode(), novo.encode())
                depois = (ROOT / nome).read_bytes()
                self.assertEqual(re.sub(rb'\?v=[\w-]+', b'?v=CACHE', antes),
                                 re.sub(rb'\?v=[\w-]+', b'?v=CACHE', depois))

    def test_renomeacao_exata_sobre_main_publicado(self):
        base = '349d2457e1f056b69c6dda550aace2a6f5377051'
        geracao = json.loads((ROOT / 'tests/fixtures/cidadania-geracao-20261103.json').read_text(encoding='utf-8'))
        for nome, trocas in RENOMEACOES.items():
            with self.subTest(ficheiro=nome):
                esperado = subprocess.check_output(['git', 'show', f'{base}:{nome}'], cwd=ROOT).decode()
                for antigo, novo, quantidade in trocas:
                    self.assertEqual(esperado.count(antigo), quantidade)
                    esperado = esperado.replace(antigo, novo)
                for antigo, novo, quantidade in geracao.get(nome, []):
                    self.assertEqual(esperado.count(antigo), quantidade)
                    esperado = esperado.replace(antigo, novo)
                # 03/11/2026: #103 gera apenas a abertura e o crédito da Justiça;
                # conserva a comparação integral de todos os restantes conteúdos.
                if nome == 'olhar-e-decidir/justica/index.html':
                    import importlib.util
                    spec = importlib.util.spec_from_file_location('carris', ROOT / 'tools/gerar_carris.py')
                    carris = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(carris)
                    esperado = carris.instalar(esperado)
                self.assertEqual(esperado, (ROOT / nome).read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
