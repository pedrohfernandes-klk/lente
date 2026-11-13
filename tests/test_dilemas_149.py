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
import sys
sys.path.insert(0, str(ROOT / 'tests'))
sys.path.insert(0, str(ROOT / 'tools'))
import entrada_temas_20261112  # noqa: E402
import temas_paginas_20261113  # noqa: E402
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
            # 12/11/2026: pedido entrada-temas. A entrada em quatro temas é a camada mais recente (manifesto fechado
            # tests/fixtures/entrada-temas-20261112.json): desfaz-se primeiro, com contagem exata de cada «novo», e o que fica, a
            # entrada do main b8abe97, confere-se como antes. Na entrada nova, a família é o destino do tema 01 (ver o teste abaixo).
            # 13/11/2026: pedido temas-01-03-04. A camada das páginas dos temas 01, 03 e 04 (manifesto fechado
            # tests/fixtures/temas-paginas-20261113.json: index.html e mapa/index.html) é agora a mais recente: desfaz-se antes da da entrada em
            # quatro temas, com contagem exata de cada «novo»; o resto confere-se como antes.
            if nome in temas_paginas_20261113.TROCAS:
                texto = temas_paginas_20261113.desfazer(texto, nome)
            if nome in entrada_temas_20261112.TROCAS:
                texto = entrada_temas_20261112.desfazer(texto, nome)
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
        # 12/11/2026: pedido entrada-temas. Na entrada, o tema 01 («Justiça e vida em comum») abre, por agora, a família Dilemas:
        # o rótulo é o nome do tema, não um nome novo da família. Aceita-se só aí, uma única vez, dentro do título do cartão do
        # tema 01; todas as outras ligações continuam a ter de dizer «Dilemas», e o mínimo de ligações vistas não desce.
        TEMA_01 = 'Justiça e vida em comum'
        # 13/11/2026: pedido temas-01-03-04. O cartão do tema 01 abre a página do tema (justica-e-vida-em-comum/), que liga à família com
        # o rótulo «Dilemas», na primeira ligação de «Ver tudo neste tema». A exceção de 12/11 deixa de ser precisa: nenhuma ligação
        # à raiz da família pode ter outro rótulo, a página do tema tem de ser uma das que a ligam, e o mínimo sobe de 25 para 26.
        vistos, temas = 0, []
        for nome in publicados():
            for texto in rotulo.findall((ROOT / nome).read_text(encoding='utf-8', errors='replace')):
                vistos += 1
                with self.subTest(ficheiro=nome, rotulo=texto):
                    if texto == TEMA_01:
                        temas.append(nome)
                    else:
                        self.assertIn(texto, aceites)
        self.assertGreaterEqual(vistos, 26)
        self.assertEqual(temas, [])
        self.assertEqual(rotulo.findall((ROOT / 'justica-e-vida-em-comum/index.html').read_text(encoding='utf-8')), ['Dilemas'])
        self.assertIn('justica-e-vida-em-comum/index.html', publicados())
        # 13/11/2026: o cartão do tema 01, uma única vez, com o destino novo; a entrada já não liga diretamente à família.
        self.assertEqual((ROOT / 'index.html').read_text(encoding='utf-8').count(
            '<h3 class="tm-n"><b aria-hidden="true">01</b><a href="justica-e-vida-em-comum/">'
            + TEMA_01 + '</a></h3>'), 1)
        self.assertNotIn('olhar-e-decidir/', (ROOT / 'index.html').read_text(encoding='utf-8'))
        # a página da família continua a chamar-se «Dilemas»
        self.assertIn('<title>Dilemas · Lente</title>', (ROOT / 'olhar-e-decidir/index.html').read_text(encoding='utf-8'))

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
