"""Vídeos escolhidos pelo docente (28/10/2026): cartões «Para ver» nos baralhos do Lente."""
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import videos_escolhidos as ve  # noqa: E402

DADOS = json.loads((ROOT / 'tools' / 'videos-escolhidos.json').read_text('utf-8'))


def baralho(pagina):
    s = (ROOT / pagina).read_text('utf-8')
    a, b = ve.lista(s)
    return s, json.loads(s[a:b])


class VideosEscolhidos(unittest.TestCase):
    def test_dados_sem_erros_de_escrita(self):
        self.assertEqual(ve.verificar(DADOS), [])

    def test_aplicado_e_idempotente(self):
        r = subprocess.run([sys.executable, str(ROOT / 'tools' / 'videos_escolhidos.py'), '--verificar'],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_cada_cartao_esta_no_sitio_certo(self):
        for p in DADOS['paginas']:
            s, itens = baralho(p['pagina'])
            pvs = [x for x in itens if 'pv' in x]
            self.assertLessEqual(len(pvs), 2, p['pagina'] + ': no máximo dois cartões «Para ver» por baralho')
            self.assertIn('assets/para-ver.css?v=' + DADOS['versao'], s)
            self.assertIn('assets/para-ver.js?v=' + DADOS['versao'], s)
            for c in p['cartoes']:
                n = next(i for i, x in enumerate(itens) if x.get('pv') == c['id'])
                x = itens[n]
                self.assertEqual((x['t'], x['rot'], x['titulo']), ('ler', 'Para ver', c['titulo']))
                if 'antes_de' in c:
                    (campo, valor), = c['antes_de'].items()
                    self.assertEqual(itens[n + 1].get(campo), valor, c['id'])
                else:
                    (campo, valor), = c['depois_de'].items()
                    self.assertEqual(itens[n - 1].get(campo), valor, c['id'])
                for v in c['videos']:
                    self.assertIn('data-yt="%s"' % v['yt'], x['html'])
                self.assertIn('class="pv-antes"', x['html'])
                self.assertIn('class="pv-depois"', x['html'])

    def test_os_outros_cartoes_nao_mudam(self):
        # Os cartões existentes ficam iguais e pela mesma ordem: só se acrescentam leituras.
        for p in DADOS['paginas']:
            _, itens = baralho(p['pagina'])
            antigos = [x for x in itens if 'pv' not in x]
            r = subprocess.run(['git', 'show', 'origin/main:' + p['pagina']], cwd=ROOT, capture_output=True, text=True)
            if r.returncode:
                self.skipTest('sem origin/main local')
            a, b = ve.lista(r.stdout)
            self.assertEqual(antigos, json.loads(r.stdout[a:b]), p['pagina'])

    def test_leitor_so_ao_toque_e_sem_cookies(self):
        js = (ROOT / 'assets' / 'para-ver.js').read_text('utf-8')
        self.assertIn('https://www.youtube-nocookie.com/embed/', js)
        self.assertNotIn('www.youtube.com/embed', js)
        for p in DADOS['paginas']:
            s = (ROOT / p['pagina']).read_text('utf-8')
            self.assertNotRegex(s, r'<iframe[^>]+youtube', p['pagina'] + ': nenhum leitor antes do toque')

    def test_escolhidos_da_ronda_1(self):
        ids = {v['yt'] for p in DADOS['paginas'] for c in p['cartoes'] for v in c['videos']}
        self.assertEqual(len(ids), 23)
        for i in ids:
            self.assertRegex(i, r'^[A-Za-z0-9_-]{11}$')


if __name__ == '__main__':
    unittest.main()
