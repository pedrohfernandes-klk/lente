"""30/10/2026: lições do Lente no motor único (assets/licoes/, cópia do motor das lições do Português), a começar pela
Cidadania refeita (decisões do docente de 30/10). O gerador é tools/licoes_lente.py; as fontes são tools/licoes/*.json.
O percurso no navegador está em tests/browser_licoes_lente.cjs."""
import copy, importlib.util, json, pathlib, re, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('licoes_lente', ROOT / 'tools/licoes_lente.py')
L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
FONTES = sorted((ROOT / 'tools/licoes').glob('*.json'))


class LicoesLente(unittest.TestCase):
    def test_ha_licoes(self):
        self.assertTrue(FONTES)

    def test_fontes_validas_e_paginas_atualizadas(self):
        for p in FONTES:
            d = json.loads(p.read_text('utf-8'))
            self.assertEqual(L.validar(d), [], p.name)
            self.assertEqual((ROOT / d['saida']).read_text('utf-8'), L.pagina(d), p.name + ': corre python3 tools/licoes_lente.py')

    def test_fonte_python_e_json_iguais(self):
        # cada .json tem um .py ao lado, de onde sai; o .json não se edita à mão
        for p in FONTES:
            self.assertTrue(p.with_suffix('.py').exists(), p.name)

    def test_motor_unico(self):
        for f in ('jogo.js', 'casca.js', 'lesson.css'):
            s = (ROOT / 'assets/licoes' / f).read_text('utf-8')
            self.assertRegex(s.splitlines()[0], r'^/\* Cópia de pt/assets/pt-lessons/' + re.escape(f) + r' \(main [0-9a-f]{7,}\)')
        for p in FONTES:
            d = json.loads(p.read_text('utf-8'))
            s = (ROOT / d['saida']).read_text('utf-8')
            self.assertIn('assets/licoes/jogo.js', s); self.assertIn('assets/licoes/casca.js', s); self.assertIn('assets/licoes/lesson.css', s)
            self.assertIn('"variar": false', s)  # numa aula, todos os cartões; o motor não tira à sorte
            # 02/11/2026: decisão do docente (141): o «Ideias» é público e tem ligação a partir das páginas públicas
            if d['id'].startswith('ideias-'):self.assertFalse(d.get('piloto'))
            self.assertEqual(s.count('robots" content="noindex'), 1 if d.get('piloto') else 0, p.name)

    def test_o_validador_apanha_os_erros(self):
        # 05/11/2026 (plano do molde, pedido 2): a s01 (FONTES[0]) passou ao molde, que não tem «Na aula» nem a contagem de 12 a
        # 16; os erros do contrato antigo provam-se com a primeira sessão ainda sem molde, e os do contrato novo com a s01, logo
        # abaixo. Nenhuma verificação saiu.
        d = json.loads(next(p for p in FONTES if 'molde' not in json.loads(p.read_text('utf-8'))).read_text('utf-8'))
        def com(f):
            e = copy.deepcopy(d); f(e); return ' | '.join(L.validar(e))
        esc = next(i for i, c in enumerate(d['cartoes']) if c['t'] == 'escolha')
        self.assertIn('denuncia-se', com(lambda e: e['cartoes'][esc]['o'].__setitem__(e['cartoes'][esc]['c'], e['cartoes'][esc]['o'][e['cartoes'][esc]['c']] * 2)))
        self.assertIn('fe', com(lambda e: e['cartoes'][esc].__setitem__('fe', ['', '', ''])))
        self.assertIn('não pode aparecer', com(lambda e: e['cartoes'][esc].__setitem__('f', 'O professor explica.')))
        self.assertIn('Qual das', com(lambda e: e['cartoes'][esc].__setitem__('p', 'Qual frase está certa?')))
        self.assertIn('pela posição', com(lambda e: e['cartoes'][esc].__setitem__('f', 'Certo. A primeira é a melhor.')))
        self.assertIn('Na aula', com(lambda e: e['cartoes'].append(dict(e['cartoes'][[c.get('rot') for c in e['cartoes']].index('Na aula')]))))
        self.assertIn('imagem', com(lambda e: e['cartoes'][0].__setitem__('html', e['cartoes'][0]['html'] + '<img src="x.jpg" alt="">')))
        self.assertIn('12 a 16', com(lambda e: e.__setitem__('cartoes', [c for c in e['cartoes'] if c['t'] not in ('vf',)])))
        # 05/11/2026 (pedido 2): o contrato do molde, sobre a s01 na versão final
        m = json.loads((ROOT / 'tools/licoes/cidadania-m1-s01.json').read_text('utf-8'))
        self.assertEqual(L.validar(m), [])
        def comm(f):
            e = copy.deepcopy(m); f(e); return ' | '.join(L.validar(e))
        self.assertIn('«Em turma»', comm(lambda e: e['cartoes'].pop(17)))
        self.assertIn('grupo', comm(lambda e: e['cartoes'][2].__setitem__('p', 'Em grupo, decidam o que a sala pôs à prova.')))
        self.assertIn('docente', comm(lambda e: e['cartoes'][2].__setitem__('p', 'Pergunta ao docente o que a sala pôs à prova.')))
        self.assertIn('espaço inseparável', comm(lambda e: e['cartoes'][10].__setitem__('f', 'Volta ao artigo 12 e lê outra vez.')))
        self.assertIn('Na aula', comm(lambda e: e['cartoes'].insert(5, {'t': 'ler', 'rot': 'Na aula', 'titulo': 'x', 'html': '<p>x</p>', 'min': 1})))

    def test_sessao_01_m1(self):
        # 05/11/2026 (plano do molde, pedido 2; decisões 157 e 158): a s01 passa à versão final, no molde cidadania-2026-11. O
        # «Na aula» sai (o momento da aula é o «Em turma», e o que depende do docente vive no guia, decisão 154); o caso continua
        # inventado e di-lo, e as fontes dizem também qual é o caso real (decisão 161). Exige-se o Decide em 2.º e o «Em turma».
        d = json.loads((ROOT / 'tools/licoes/cidadania-m1-s01.json').read_text('utf-8'))
        self.assertEqual(d['chave'], 'epi-cid-m1-s01')
        self.assertEqual(d['molde'], L.MOLDE)
        rot = [c.get('rot') for c in d['cartoes']]
        self.assertEqual(rot[0], 'Abre'); self.assertEqual(rot[-1], 'Para levar'); self.assertEqual(rot.count('Na aula'), 0)
        self.assertEqual(rot[1], 'Decide'); self.assertEqual(rot.count('Em turma'), 1)
        self.assertIn('Caso inventado', d['cartoes'][0]['html'])
        self.assertIn('O caso da Sara e o das mensagens são inventados', d['fontes'])
        self.assertIn('o da Relação de Évora é real', d['fontes'])


if __name__ == '__main__':
    unittest.main()
