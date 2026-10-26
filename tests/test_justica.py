from pathlib import Path
import re, json, unittest
from urllib.parse import urlsplit
R = Path(__file__).resolve().parents[1]
J = R / 'olhar-e-decidir/justica'
LENTE = 'https://pedrohfernandes-klk.github.io/lente/'
PROIBIDAS = re.compile(r'(?<![\wÀ-ÿ])(?:jog(?:ar|a|as|amos|am|ou|ue|uei|ando|ado)|fichas?|folhas?)(?![\wÀ-ÿ])', re.I)


def itens(p):
    s = p.read_text('utf-8')
    m = re.search(r'EPIJogo\.montar\(\{.*?itens:(\[.*?\]),chave:"([^"]+)"', s, re.S)
    return json.loads(m.group(1)), m.group(2)


class Justica(unittest.TestCase):
    def test_lessons_size_key_and_excerpts(self):
        # a lição 3 (episódio 3, «Free to Choose») entrou a 23/10/2026; antes o teste só via as lições 1 e 2
        YT = {1: 'kBdfcR-8hEY', 2: '0O2Rq4HJBxw', 3: 'Qw4l1w0rkjs'}
        for n, chave in ((1, 'lente-justica-licao-1'), (2, 'lente-justica-licao-2'), (3, 'lente-justica-licao-3')):
            I, k = itens(J / f'licao-{n}/index.html')
            self.assertEqual(k, chave)
            self.assertTrue(20 <= len(I) <= 26, len(I))
            html = ''.join(x.get('html', '') for x in I)
            vids = re.findall(r'data-yt="([\w-]{11})" data-ini="(\d+)" data-fim="(\d+)"', html)
            self.assertGreaterEqual(len(vids), 6)
            for yt, a, b in vids:
                self.assertEqual(yt, YT[n])
                self.assertLess(int(a), int(b))
            for x in I:
                if x['t'] == 'escolha':
                    self.assertEqual(len(x['o']), 4)
                    self.assertTrue(all((j == x['c']) == (x['fe'][j] is None) for j in range(4)))
                    self.assertLess(len(x['o'][x['c']]), max(len(o) for j, o in enumerate(x['o']) if j != x['c']))
                if x['t'] == 'vf':
                    self.assertIsInstance(x['v'], bool)
                    self.assertTrue(x['f'] and x['fe'])

    def test_player_only_on_touch_nocookie(self):
        for n in (1, 2, 3):
            s = (J / f'licao-{n}/index.html').read_text('utf-8')
            self.assertNotIn('<iframe', s)
            self.assertIn('https://www.youtube-nocookie.com/embed/"+d.yt+"?autoplay=1&rel=0&cc_load_policy=1', s)
            self.assertIn('"&start="+d.ini', s)
            self.assertIn('"&end="+d.fim', s)

    def test_aplicar_keeps_published_dilemma(self):
        I, k = itens(J / 'aplicar/index.html')
        self.assertEqual(k, 'epi-justica-sandel-v1')
        self.assertEqual(len(I), 6)
        self.assertEqual(I[0]['titulo'], 'Seis sessões. Três projetos. Quem fica com o quê?')
        s = (J / 'aplicar/index.html').read_text('utf-8')
        self.assertIn('data-escuta-player=\\"g_Z_I63vEqA\\"', s)
        self.assertIn('../../../assets/projection-launcher.js', s)

    def test_teacher_guide_names_the_transcript_once(self):
        s = (J / 'docente/index.html').read_text('utf-8')
        self.assertEqual(s.count('Tempos aproximados pela transcrição comunitária da Amara'), 1)
        for n in (1, 2, 3):
            I, _ = itens(J / f'licao-{n}/index.html')
            for x in I:
                textos = [x.get('f') or ''] + (x['fe'] if isinstance(x.get('fe'), list) else [x.get('fe') or ''])
                for t in filter(None, textos):
                    # uma citação em inglês nas explicações leva o tempo ao lado: «...» (m:ss) ou («...», m:ss)
                    for m in re.finditer(r"«([A-Za-z][^»]*?(?:\b(?:the|you|is|that|of|it|we|don't|can't|for)\b)[^»]*)»", t):
                        self.assertRegex(t[m.end():m.end() + 9], r'^(\s*\(\d+:\d\d\)|, \d+:\d\d\))', (n, m.group(1)))

    def test_entry_is_linked(self):
        for f in ('olhar-e-decidir/index.html', 'mapa/index.html'):
            self.assertIn(LENTE + 'olhar-e-decidir/justica/', (R / f).read_text('utf-8'), f)
        s = (J / 'index.html').read_text('utf-8')
        for h in ('licao-1/', 'licao-2/', 'licao-3/', 'aplicar/', 'guiao/', 'docente/'):
            self.assertIn(f'href="{h}"', s)

    def test_lesson_3_is_chained(self):
        # 23/10/2026: a lição 2 segue para a 3, a 3 para «Aplicar»; os menus ligam as três lições
        s2 = (J / 'licao-2/index.html').read_text('utf-8')
        self.assertIn('seguinte:"../licao-3/",seguinteRotulo:"Lição 3"', s2)
        s3 = (J / 'licao-3/index.html').read_text('utf-8')
        self.assertIn('seguinte:"../aplicar/",seguinteRotulo:"Aplicar"', s3)
        self.assertIn('id="casca-pc"', s3)
        for n in (1, 2, 3):
            s = (J / f'licao-{n}/index.html').read_text('utf-8')
            for o in {1, 2, 3} - {n}:
                self.assertIn(f'<a href="../licao-{o}/">Lição {o}:', s, (n, o))
        g = (J / 'guiao/index.html').read_text('utf-8')
        # 26/10: título aprovado pelo docente; conceitos e cadeia conservados.
        self.assertIn('Lição 3: Até onde vai a minha liberdade?', g)
        self.assertIn('Lição 3: Até onde vai a minha liberdade? (episódio 3', (J / 'docente/index.html').read_text('utf-8'))

    def test_house_rules_and_local_links(self):
        for p in sorted(J.rglob('index.html')):
            s = p.read_text('utf-8')
            vis = re.sub(r'<(script|style)\b.*?</\1>', '', s, flags=re.S)
            self.assertNotIn('—', vis, p)
            self.assertIsNone(PROIBIDAS.search(re.sub(r'<[^>]+>', ' ', vis)), p)
            for href in re.findall(r'href="([^"]+)"', vis):
                u = urlsplit(href)
                if u.scheme and not href.startswith(LENTE):
                    continue
                if 'projetar' in href:
                    continue
                t = R / u.path.removeprefix('/lente/') if u.scheme else p.parent / u.path if u.path else p
                if t.is_dir():
                    t = t / 'index.html'
                self.assertTrue(t.exists(), (p, href))


if __name__ == '__main__':
    unittest.main()
