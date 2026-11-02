"""02/11/2026: decisão 138, entregas individuais sem apagar os casos narrados."""
import importlib.util
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('piloto', ROOT / 'tools/cidadania_piloto.py')
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)
BASE = json.loads((ROOT / 'tests/fixtures/cidadania-indices-20261102.json').read_text('utf-8'))['sessoes']


class Individual(unittest.TestCase):
    def test_projeto_individual_com_os_mesmos_pesos_e_fontes(self):
        # 02/11/2026: reforça o contrato do piloto, preservando o enunciado anterior.
        antes = (ROOT / 'cidadania/projeto/index.html').read_text('utf-8')
        depois = (ROOT / 'cidadania/piloto/m1/projeto/index.html').read_text('utf-8')
        self.assertEqual(re.findall(r'<td class="n">(\d+)%</td>', antes),
                         re.findall(r'<td class="n">(\d+)%</td>', depois))
        self.assertEqual(re.findall(r'<td class="n">(\d+)%</td>', depois), ['20', '20', '30', '30'])
        self.assertNotRegex(depois, r'(?i)em grupo|cada grupo|do grupo|vosso|vossa|trabalho de equipa')
        for ancora in ('pergunta-resposta', 'fases', 'metodo', 'avaliacao', 'av-diario', 'av-laboratorio', 'av-dossie', 'av-teatro'):
            self.assertIn(f'id="{ancora}"', depois)
        for requisito in ('5 a 8 minutos', 'três minutos', 'duas fontes independentes', 'Consentimento', 'Anonimato'):
            self.assertIn(requisito, depois)
        self.assertIn('href="projeto/"', (ROOT / 'cidadania/piloto/m1/index.html').read_text('utf-8'))
        self.assertNotIn('../../../projeto/', (ROOT / 'cidadania/piloto/m1/docente/index.html').read_text('utf-8'))

    def test_entregas_e_instrucoes_individuais(self):
        proibido = re.compile(r'em grupos|cada grupo|por grupo|do teu grupo|do vosso grupo|outro grupo|acórdão da turma', re.I)
        for n, g in G.GUIA.items():
            d = json.loads((ROOT / f'tools/licoes/cidadania-m1-s{n}.json').read_text('utf-8'))
            aula = next(c['html'] for c in d['cartoes'] if c.get('rot') == 'Na aula')
            self.assertRegex(aula, r'(?i)individual|teu|tua', n)
            self.assertIsNone(proibido.search(aula), n)
            for campo in ('passos', 'materiais', 'escrito', 'produto', 'projeto', 'grelha'):
                self.assertIsNone(proibido.search(str(g[campo])), f'{n}: {campo}')
            self.assertEqual(sum(p for _, p in g['grelha']), 20, n)

    def test_indices_chaves_e_duracoes_preservados(self):
        for n in G.NOMES:
            rel = f'tools/licoes/cidadania-m1-s{n}.json'
            antes = BASE[n]
            depois = json.loads((ROOT / rel).read_text('utf-8'))
            for campo in ('chave', 'versao', 'saida'):
                self.assertEqual(antes[campo], depois[campo], f'{n}: {campo}')
            self.assertEqual(antes['sequencia'],
                             [[c['t'], c.get('g'), c.get('rot')] for c in depois['cartoes']], n)
        self.assertIn('5 a 8 minutos', str(G.GUIA['10']))
        self.assertIn('três de defesa', str(G.GUIA['10']))

    def test_grupos_narrativos_nao_foram_apagados(self):
        s02 = json.loads((ROOT / 'tools/licoes/cidadania-m1-s02.json').read_text('utf-8'))
        s06 = json.loads((ROOT / 'tools/licoes/cidadania-m1-s06.json').read_text('utf-8'))
        self.assertIn('a Marta aceitou ser filmada para o grupo rever a cena', s02['cartoes'][0]['html'])
        self.assertIn('seis turnos de filmagem para três grupos', s06['cartoes'][0]['html'])


if __name__ == '__main__':
    unittest.main()
