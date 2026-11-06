"""06/11/2026: decisão 149. A terceira família da Cidadania chama-se «Dilemas» (decisão 15: «Humanos, Algoritmos, Dilemas»).

O #107 publicou «Decisões» sem decisão registada. Volta «Dilemas» onde o nome é o da família (títulos, migalhas, menus,
mapa, entrada, cartões e o rótulo do progresso); os endereços (olhar-e-decidir/), as âncoras, as chaves do progresso e os
outros sentidos de «decisões» (o sidequest «Decisões que parecem razoáveis», as «Decisões provisórias» do guia do M2)
ficam como estão.
"""
import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFESTO = json.loads((ROOT / 'tests/fixtures/dilemas-149-20261106.json').read_text(encoding='utf-8'))

# 06/11/2026: as formas que o nome da família toma nas páginas; nenhuma pode voltar a dizer «Decisões».
FORMAS_ANTIGAS = [
    'olhar-e-decidir/">Decisões',
    'olhar-e-decidir/\\">Decisões',
    'Voltar a Decisões',
    'percursoRotulo:"Decisões"',
    '· Decisões ·',
    '<title>Decisões · Lente</title>',
    '<h1>Decisões.</h1>',
    'Decisões: justiça, ética e estética',
    'Decisões: Justiça, Ética e Estética',
    'Decisões · Justiça, ética e estética',
    '<strong>Decisões</strong>',
    'assinatura-orientacao">Decisões<',
    'Abrir Decisões',
    # 06/11/2026: o nome ainda mais antigo da família, que o #107 não viu (escrito com escape unicode no último cartão).
    'Voltar a Ter ju\\u00edzo',
    'Voltar a Ter juízo',
]


def publicados():
    nomes = subprocess.check_output(['git', 'ls-files', '*.html', '*.js'], cwd=ROOT).decode().splitlines()
    return [n for n in nomes if not n.startswith(('tests/', 'docs/', 'node_modules/'))
            and (not n.startswith('tools/') or n.startswith('tools/justica/moldes/'))]


class Dilemas149(unittest.TestCase):
    def test_manifesto_aplicado_com_contagem_exata(self):
        # 06/11/2026: 43 sítios em 21 ficheiros (o 44.º do #107, o ramo repetido do mapa, saiu com a revisão de 5/11),
        # mais o botão «Voltar a Ter juízo» do último cartão da lição 1 de Estética, o nome anterior da família.
        self.assertEqual(len(MANIFESTO), 21)
        for nome, trocas in MANIFESTO.items():
            texto = (ROOT / nome).read_text(encoding='utf-8')
            for antigo, novo, quantidade in trocas:
                with self.subTest(ficheiro=nome, troca=novo[:60]):
                    self.assertEqual(texto.count(antigo), 0)
                    self.assertEqual(texto.count(novo), quantidade)

    def test_nenhuma_pagina_chama_decisoes_a_familia(self):
        for nome in publicados():
            texto = (ROOT / nome).read_text(encoding='utf-8', errors='replace')
            for forma in FORMAS_ANTIGAS:
                with self.subTest(ficheiro=nome, forma=forma):
                    self.assertNotIn(forma, texto)

    def test_ligacoes_para_a_familia_dizem_dilemas(self):
        # Toda a ligação de texto para a raiz da família diz «Dilemas» (ou «Voltar a Dilemas», «Abrir Dilemas»).
        rotulo = re.compile(r'olhar-e-decidir/\\?">([^<]+)<')
        aceites = {'Dilemas', 'Voltar a Dilemas', 'Abrir Dilemas ', 'Abrir Ética e estética '}
        vistos = 0
        for nome in publicados():
            for texto in rotulo.findall((ROOT / nome).read_text(encoding='utf-8', errors='replace')):
                vistos += 1
                with self.subTest(ficheiro=nome, rotulo=texto):
                    self.assertIn(texto, aceites)
        self.assertGreaterEqual(vistos, 25)

    def test_o_resto_fica(self):
        # Endereços, chaves do progresso e os outros sentidos de «decisões» não mudam.
        self.assertTrue((ROOT / 'olhar-e-decidir/index.html').exists())
        registos = (ROOT / 'assets/progresso-registos.js').read_text(encoding='utf-8')
        self.assertIn('["^(epi-justica|lente-(justica|etica|estetica)-)", "Dilemas: Justiça, Ética e Estética"]', registos)
        sidequest = (ROOT / 'sidequests/decisoes/index.html').read_text(encoding='utf-8')
        self.assertEqual(sidequest.count('Decisões que parecem razoáveis'), 5)
        self.assertNotIn('Dilemas', sidequest)
        self.assertIn('<h2>Decisões provisórias</h2>', (ROOT / 'cidadania/m2/sessoes/index.html').read_text(encoding='utf-8'))
        mapa = (ROOT / 'mapa/index.html').read_text(encoding='utf-8')
        self.assertIn('sidequests/decisoes/">Decisões que parecem razoáveis</a>', mapa)
        self.assertIn('<li style="--k:1"><a href="https://pedrohfernandes-klk.github.io/lente/olhar-e-decidir/">Dilemas</a></li>',
                      (ROOT / 'olhar-e-decidir/justica/licao-1/index.html').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
