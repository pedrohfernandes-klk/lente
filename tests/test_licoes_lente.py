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
            self.assertEqual(s.count('robots" content="noindex'), 1 if d.get('piloto') else 0, p.name)

    def test_o_validador_apanha_os_erros(self):
        d = json.loads(FONTES[0].read_text('utf-8'))
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

    def test_sessao_01_m1(self):
        d = json.loads((ROOT / 'tools/licoes/cidadania-m1-s01.json').read_text('utf-8'))
        self.assertEqual(d['chave'], 'epi-cid-m1-s01')
        rot = [c.get('rot') for c in d['cartoes']]
        self.assertEqual(rot[0], 'Abre'); self.assertEqual(rot[-1], 'Para levar'); self.assertEqual(rot.count('Na aula'), 1); self.assertIn('Decide', rot)
        self.assertIn('Caso inventado', d['cartoes'][0]['html'])
        self.assertIn('Os casos são inventados', d['fontes'])


if __name__ == '__main__':
    unittest.main()
