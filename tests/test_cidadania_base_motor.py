"""02/11/2026: o pedido 2 de Ideias só pode mudar o cache dos ficheiros na Cidadania."""
from pathlib import Path
import re
import json
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = 'fbfb8509d6e104f00811321d95ed4d999f8df2cd'
RENOMEACOES = json.loads((ROOT / 'tests/fixtures/cidadania-nomes-20261103.json').read_text(encoding='utf-8'))
# 05/11/2026: manifesto fechado das trocas da revisão de 5/11 no Lente.
REVISAO_0511 = json.loads((ROOT / 'tests/fixtures/revisao-lente-20261105.json').read_text(encoding='utf-8'))
# 05/11/2026: decisão 147 (Laboratório sem o Português), manifesto fechado das trocas na navegação do Laboratório.
LAB_147 = json.loads((ROOT / 'tests/fixtures/lab-147-20261105.json').read_text(encoding='utf-8'))
# 05/11/2026: decisão 146 (discussões em turma, trabalhos individuais): manifesto fechado tools/trocas/grupos-146-20261105.json.
import grupos146  # noqa: E402
# 06/11/2026: decisão 149 (volta «Dilemas»): manifesto fechado tests/fixtures/dilemas-149-20261106.json.
from renomeacoes_cidadania import dilemas_149  # noqa: E402


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
                # 05/11/2026: decisão 147. O cartaz rotativo deixa de anunciar o Corta! e as peças do Laboratório
                # (percurso-anterior); só as trocas do manifesto fechado, com contagem exata.
                for antigo, novo, quantidade in LAB_147.get(nome, []):
                    self.assertEqual(antes.count(antigo.encode()), quantidade)
                    antes = antes.replace(antigo.encode(), novo.encode())
                depois = (ROOT / nome).read_bytes()
                # 05/11/2026: decisão 146 (discussões em turma, trabalhos individuais): só se desfazem as trocas do manifesto fechado, com contagem exata; o resto compara-se como antes.
                if nome in grupos146.TROCAS:
                    depois = grupos146.desfazer(depois.decode('utf-8'), nome).encode('utf-8')
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
                # 05/11/2026: revisão de 5/11 (Lente). Só as trocas deste manifesto fechado (linha do «Ideias» no cartão do
                # Laboratório, rodapé dos excertos, ramo «Decisões» do mapa, bloco repetido da Cidadania e crédito dos desenhos
                # das lições 1 e 2 da Justiça), com contagem exata; a comparação continua integral.
                for antigo, novo, quantidade in REVISAO_0511.get(nome, []):
                    self.assertEqual(esperado.count(antigo), quantidade)
                    esperado = esperado.replace(antigo, novo)
                # 05/11/2026: decisão 147. O ramo do Laboratório no mapa segue percursos.json sem as peças retiradas;
                # só as trocas deste manifesto, com contagem exata.
                for antigo, novo, quantidade in LAB_147.get(nome, []):
                    self.assertEqual(esperado.count(antigo), quantidade)
                    esperado = esperado.replace(antigo, novo)
                # 05/11/2026: decisão 146 (discussões em turma, trabalhos individuais): as trocas do manifesto fechado, com contagem exata.
                # 05/11/2026: depois da fusão do #122, por cima da camada da decisão 147 (as camadas 146 e 154 partem do main com o #122).
                esperado = grupos146.aplicar(esperado, nome)
                # 03/11/2026: #103 gera apenas a abertura e o crédito da Justiça;
                # conserva a comparação integral de todos os restantes conteúdos.
                if nome == 'olhar-e-decidir/justica/index.html':
                    import importlib.util
                    spec = importlib.util.spec_from_file_location('carris', ROOT / 'tools/gerar_carris.py')
                    carris = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(carris)
                    esperado = carris.instalar(esperado)
                # 06/11/2026: decisão 149, volta «Dilemas» onde o #107 pôs «Decisões» como nome da família; só as trocas do
                # manifesto fechado, com contagem exata. O sidequest «Decisões que parecem razoáveis» e endereços ficam.
                esperado = dilemas_149(esperado, nome)
                self.assertEqual(esperado, (ROOT / nome).read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
