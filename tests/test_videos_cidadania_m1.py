"""Vídeos escolhidos pelo docente (28/10/2026) nas sessões novas de Cidadania M1."""
import json
import re
import sys
import unittest
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'tools'))
import videos_escolhidos as ve  # noqa: E402

D = json.loads((R / 'tools/videos-cidadania-m1.json').read_text('utf-8'))
PASSO = {'ve': 2, 'leva': 5}


def passo(s, n):
    m = re.search(r'<section class="c10-stage" id="momento-%d".*?</section>' % n, s, re.S)
    return m.group(0) if m else ''


class VideosCidadaniaM1(unittest.TestCase):
    def test_escrita(self):
        self.assertEqual(ve.verificar({'paginas': [{'cartoes': v} for v in D['sessoes'].values()]}), [])

    def test_cada_bloco_no_passo_certo(self):
        for n in range(1, 11):
            s = (R / f'cidadania/m1/sessoes/{n:02}/index.html').read_text('utf-8')
            # 06/11/2026 (decisões 155 e 166 a 168): uma sessão cujo .json tem o campo «molde» passou à lição no molde final, no
            # mesmo endereço (hoje, a 06, que tinha o bloco «Para ver» do TED-Ed no passo Leva). No molde não há vídeo no núcleo
            # (no máximo um, em «Para ir mais longe», depois de visto por inteiro): confere-se que a página não traz nenhum bloco nem
            # leitor. As outras sessões publicadas continuam a ter de ter os blocos de tools/videos-cidadania-m1.json.
            if json.loads((R / f'tools/licoes/cidadania-m1-s{n:02}.json').read_text('utf-8')).get('molde'):
                self.assertNotIn('data-pv=', s, n)
                self.assertNotIn('data-yt=', s, n)
                continue
            blocos = D['sessoes'].get(str(n), [])
            self.assertEqual(s.count('data-pv='), len(blocos), n)
            self.assertEqual('assets/para-ver.js?v=' + D['versao'] in s, bool(blocos), n)
            for c in blocos:
                p = passo(s, PASSO[c['onde']])
                self.assertIn('data-pv="%s"' % c['id'], p, c['id'])
                for v in c['videos']:
                    self.assertIn('data-yt="%s"' % v['yt'], p)
            # O passo Decide é sem ecrã: nunca leva vídeo.
            self.assertNotIn('data-pv=', passo(s, 3))

    def test_guia_do_docente(self):
        s = (R / 'cidadania/m1/sessoes/index.html').read_text('utf-8')
        for c in [c for v in D['sessoes'].values() for c in v]:
            for v in c['videos']:
                self.assertIn(v['original'].replace('&', '&amp;'), s)

    def test_cinco_videos_sem_leitor_antes_do_toque(self):
        ids = {v['yt'] for b in D['sessoes'].values() for c in b for v in c['videos']}
        # 28/10/2026: saem os vídeos fora de contexto (sessão 07, Vê, e sessão 08), pela regra do docente.
        self.assertEqual(ids, {'WoHJhwh4mVQ', 'n0uwTBrgqxI', 'H0CTHVCkm90'})
        for n in (6, 7, 8):
            self.assertNotRegex((R / f'cidadania/m1/sessoes/{n:02}/index.html').read_text('utf-8'), r'<iframe[^>]+youtube')


if __name__ == '__main__':
    unittest.main()
