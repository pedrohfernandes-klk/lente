"""02/11/2026: bases reprodutíveis e regras estritas para conteúdo novo."""
import importlib.util
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

R = Path(__file__).resolve().parents[1]
T = R / 'tools/justica'
spec = importlib.util.spec_from_file_location('justica_validar', T / 'validar.py')
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)
MANIFESTO = json.loads((T / 'licoes.json').read_text('utf-8'))

# 02/11/2026: leituras publicadas acima de 95 palavras, a dividir na fase 1.
# Lista fechada: só desaparece quando a leitura passa a ter <=95 palavras;
# enquanto exceder, a contagem tem de ser exatamente a registada, nunca maior.
LEITURAS_PUBLICADAS = {(1, 12): 99}
LEITURAS_HASH = {(1, 12): 'd8c4de55a28f228068bd46a35da1246e043eff98f1e2189b48eaab437e424d38'}


def banco(n):
    return json.loads((T / f'bancos/licao-{n}.json').read_text('utf-8'))


class BasesJustica(unittest.TestCase):
    def test_manifesto_cobre_todas_as_paginas_e_bancos(self):
        # 02/11/2026: omitir uma lição no manifesto não pode afastá-la dos testes.
        numeros = [m['numero'] for m in MANIFESTO]
        self.assertEqual(len(numeros), len(set(numeros)))
        self.assertEqual(numeros, list(range(1, len(numeros)+1)))
        self.assertEqual(set(numeros), {int(p.parent.name.split('-')[1]) for p in (R/'olhar-e-decidir/justica').glob('licao-*/index.html')})
        self.assertEqual(set(numeros), {int(p.stem.split('-')[1]) for p in (T/'bancos').glob('licao-*.json')})
        for m in MANIFESTO:
            self.assertEqual(m['chave'], f"lente-justica-licao-{m['numero']}")
            self.assertRegex(m['video'], r'^[\w-]{11}$')
            self.assertTrue(1 <= len(m['aulas']) <= 2)
            self.assertTrue(all(type(a) is int and 1 <= a <= 24 for a in m['aulas']))
            self.assertIsInstance(m['molde_novo'], bool)

    def test_regeneracao_literal(self):
        # 02/11/2026: inclui casca, menus, motor, chaves, ordem e índices do banco.
        for m in MANIFESTO:
            n = m['numero']
            molde = (T/f'moldes/licao-{n}.html').read_text('utf-8')
            self.assertEqual(molde.count('@@ITENS@@'), 1)
            gerada = molde.replace('@@ITENS@@', (T/f'bancos/licao-{n}.json').read_text('utf-8').rstrip('\n'))
            self.assertEqual(gerada, (R/f'olhar-e-decidir/justica/licao-{n}/index.html').read_text('utf-8'))
            # 02/11/2026: prova contra o main de partida, só com as duas trocas autorizadas.
            original = gerada
            for troca in json.loads((T/'migracao.json').read_text('utf-8')):
                if troca['licao'] == n:
                    self.assertEqual(original.count(troca['novo']), 1)
                    original = original.replace(troca['novo'], troca['antigo'])
            self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), m['sha256_publicado'])

    def test_regras_e_lista_fechada_das_leituras(self):
        # 02/11/2026: os cartões novos não herdam exceções do publicado.
        encontradas = {}
        for m in MANIFESTO:
            n = m['numero']
            self.assertEqual(V.validar_banco(banco(n), n, m['molde_novo']), [])
            for k, x in enumerate(banco(n), 1):
                if x['t'] == 'ler' and V.palavras_visiveis(x) > 95:
                    encontradas[n,k] = V.palavras_visiveis(x)
                    self.assertFalse(m['molde_novo'])
                    self.assertEqual(hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True).encode()).hexdigest(), LEITURAS_HASH.get((n,k)))
        self.assertEqual(encontradas, {k: v for k,v in LEITURAS_PUBLICADAS.items() if k in encontradas})

    def test_validador_recusa_regressoes(self):
        # 02/11/2026: provar que palavras proibidas e leitura longa nova falham.
        from copy import deepcopy
        for palavra in ('jogo', 'jogar', 'ficha', 'folha', 'professor'):
            itens = deepcopy(banco(2)); itens[0]['html'] = '<p>' + palavra + '</p>'
            self.assertTrue(V.validar_banco(itens, 2))
        itens = deepcopy(banco(2)); itens[0]['html'] = '<p>' + 'palavra ' * 96 + '</p>'
        self.assertTrue(V.validar_banco(itens, 2, True))
        self.assertEqual(V.palavras_visiveis({'html':'<p>one two</p><p>um dois</p>'}), 4)

    def test_manifesto_citacoes_e_privacidade(self):
        # 02/11/2026: formato, tempo e cobertura dos bancos, sem legendas em CI.
        citacoes = json.loads((T/'citacoes.json').read_text('utf-8'))
        self.assertEqual(citacoes, V.extrair_citacoes(T))
        self.assertTrue(citacoes)
        for c in citacoes:
            self.assertRegex(c['tempo'], r'^\d+:[0-5]\d$')
            self.assertTrue(c['frase'])
            self.assertLessEqual(len(re.findall(r'[.!?](?=\s|$)', c['frase'])), 2)
            self.assertIsNone(V.PROIBIDAS.search(c['frase']))
            self.assertEqual(c['video'], next(m['video'] for m in MANIFESTO if m['numero']==c['licao']))
        self.assertEqual(list(T.rglob('*.vtt')) + list(T.rglob('*.srt')), [])

    def test_molde_novo(self):
        # 02/11/2026: decisões 63/65 sem reduzir o teto nem dispensar o molde antigo.
        for m in MANIFESTO:
            if not m['molde_novo']:
                continue
            itens = banco(m['numero']); fazer = [x for x in itens if x['t'] != 'ler']
            self.assertTrue(20 <= len(itens) <= 26)
            self.assertGreaterEqual(len(fazer), 14)
            escrita = {'escrita', 'frase', 'versos'}
            self.assertLessEqual(sum(x['t'] in escrita for x in fazer), 1)
            self.assertGreaterEqual(len({x['t'] for x in fazer} - escrita), 5)
            for a,b,c in zip(fazer, fazer[1:], fazer[2:]):
                self.assertFalse(a['t']==b['t']==c['t'])
            self.assertEqual(sum(x.get('rot')=='Na aula' for x in itens), 1)
            self.assertEqual(itens[0]['rot'], 'Abre')
            self.assertIn('No fim, consegues', itens[0]['html'])
            self.assertRegex(itens[0]['html'], r'<img\b')
            self.assertEqual(itens[1]['rot'], 'Olha')
            self.assertEqual(itens[1]['t'], 'mapa')


if __name__ == '__main__':
    unittest.main()
