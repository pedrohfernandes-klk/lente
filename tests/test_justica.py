from pathlib import Path
import re, json, math, unittest
from html import unescape
from urllib.parse import urlsplit
R = Path(__file__).resolve().parents[1]
J = R / 'olhar-e-decidir/justica'
LENTE = 'https://pedrohfernandes-klk.github.io/lente/'
# 02/11/2026: número, chaves, vídeos, aulas e navegação vêm do manifesto.
MANIFESTO = json.loads((R / 'tools/justica/licoes.json').read_text('utf-8'))
PROIBIDAS = re.compile(r'(?<![\wÀ-ÿ])(?:jog(?:o|os|ar|a|as|amos|am|ou|ue|uei|ando|ado)|fichas?|folhas?)(?![\wÀ-ÿ])', re.I)


def itens(p):
    s = p.read_text('utf-8')
    if 'CFG.itens=' in s:
        cfg = json.JSONDecoder().raw_decode(s.split('var CFG=', 1)[1])[0]
        cards = json.JSONDecoder().raw_decode(s.split('CFG.itens=', 1)[1])[0]
        return cards, cfg['chave']
    m = re.search(r'EPIJogo\.montar\(\{.*?itens:(\[.*?\]),chave:"([^"]+)"', s, re.S)
    return json.loads(m.group(1)), m.group(2)


class Justica(unittest.TestCase):
    def test_lessons_size_key_and_excerpts(self):
        # a lição 3 (episódio 3, «Free to Choose») entrou a 23/10/2026; antes o teste só via as lições 1 e 2
        # 02/11/2026: preserva todos os limites e percorre cada lição publicada.
        for meta in MANIFESTO:
            n, chave = meta['numero'], meta['chave']
            I, k = itens(J / f'licao-{n}/index.html')
            self.assertEqual(k, chave)
            if meta.get('formato_curto'):
                self.assertEqual(len(I), 10)
            else:
                self.assertTrue(20 <= len(I) <= 26, len(I))
            html = ''.join(x.get('html', '') for x in I)
            vids = re.findall(r'data-yt="([\w-]{11})" data-ini="(\d+)" data-fim="(\d+)"', html)
            if meta.get('formato_curto'):
                fontes = json.loads((R / 'tools/justica/excertos-curtos.json').read_text('utf-8'))
                selecao = next(f for f in fontes if f['licao'] == n)
                self.assertEqual(vids, [(selecao['video'], str(c['inicio']), str(c['fim'])) for c in selecao['excertos']])
                self.assertEqual(len(vids), 4)
                for _, a, b in vids:
                    self.assertTrue(60 <= int(b)-int(a) <= 180)
            elif meta['molde_novo']:
                from urllib.parse import urlparse, parse_qs
                fontes = json.loads((R / 'tools/justica/novas/videos.json').read_text('utf-8'))
                expected = []
                for fonte in fontes:
                    if fonte['aula'] in meta['aulas']:
                        u = urlparse(fonte['video']); q = parse_qs(u.query)
                        expected.append((u.path.split('/')[-1], q['start'][0], q['end'][0]))
                self.assertEqual(vids, expected)
            else:
                self.assertGreaterEqual(len(vids), 6)
            for yt, a, b in vids:
                self.assertEqual(yt, meta['video'])
                self.assertLess(int(a), int(b))
            curtas, esperado = 0, 0.0
            for x in I:
                if x['t'] == 'escolha':
                    self.assertEqual(len(x['o']), 4)
                    self.assertTrue(all((j == x['c']) == (x['fe'][j] is None) for j in range(4)))
                    # 30/10/2026: opções equilibradas (pedido do docente)
                    n = [len(re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]*>', '', o)).replace('_', '').replace('*', '')).strip()) for o in x['o']]
                    self.assertLessEqual(max(n), 1.2 * min(n), x['p'])
                    # 30/10/2026: revisão do #72 (opções equilibradas): volta a regra antiga, a certa nunca é mais longa
                    # do que a maior errada, a par da amplitude de 20 %; e não pode ser a mais curta mais vezes do que ceil(n/k).
                    self.assertLess(len(x['o'][x['c']]), max(len(o) for j, o in enumerate(x['o']) if j != x['c']), x['p'])
                    curtas += n[x['c']] < min(v for j, v in enumerate(n) if j != x['c'])
                    esperado += 1 / len(x['o'])
                if x['t'] == 'vf':
                    self.assertIsInstance(x['v'], bool)
                    self.assertTrue(x['f'] and x['fe'])
            self.assertLessEqual(curtas, math.ceil(esperado), k)

    def test_player_only_on_touch_nocookie(self):
        # 02/11/2026: não limitar a validação às primeiras três lições.
        for meta in MANIFESTO:
            n = meta['numero']
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
        # 02/11/2026: não limitar a validação às primeiras três lições.
        for meta in MANIFESTO:
            n = meta['numero']
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
        # 02/11/2026: todas as lições do manifesto têm entrada.
        for h in [f"licao-{m['numero']}/" for m in MANIFESTO] + ['aplicar/', 'guiao/', 'docente/']:
            self.assertIn(f'href="{h}"', s)

    def test_lessons_are_chained(self):
        # 02/11/2026: índice, anterior e seguinte substituem o menu de todas com todas.
        for meta in MANIFESTO:
            n = meta['numero']
            s = (J / f'licao-{n}/index.html').read_text('utf-8')
            if meta['molde_novo']:
                cfg = json.JSONDecoder().raw_decode(s.split('var CFG=', 1)[1])[0]
                self.assertEqual(cfg['seguinte'], meta['seguinte'])
            else:
                self.assertIn('seguinte:' + json.dumps(meta['seguinte']), s)
            self.assertIn('id="casca-pc"', s)
            self.assertIn('<a href="../">', s)
            self.assertIn('href="' + meta['anterior'] + '"', s)
            # 02/11/2026: a ligação seguinte também está no HTML do fecho, serializado em JSON.
            self.assertIn('href="' + meta['seguinte'] + '"', s.replace('\\"', '"'))
        # 05/11/2026: revisão de 5/11 (lente-justica-1). Voltam as verificações que o #95 tirou sem equivalente: os rótulos
        # do botão seguinte das lições 2 e 3, o menu de cada uma das lições 1 a 3 para as outras duas, e os vídeos das três
        # escritos no próprio teste (o manifesto não se confere a si próprio).
        s2 = (J / 'licao-2/index.html').read_text('utf-8')
        self.assertIn('seguinte:"../licao-3/",seguinteRotulo:"Lição 3"', s2)
        s3 = (J / 'licao-3/index.html').read_text('utf-8')
        self.assertIn('seguinte:"../licao-4/",seguinteRotulo:"Lição 4"', s3)
        YT = {1: 'kBdfcR-8hEY', 2: '0O2Rq4HJBxw', 3: 'Qw4l1w0rkjs'}
        self.assertEqual({m['numero']: m['video'] for m in MANIFESTO if m['numero'] in YT}, YT)
        for n in (1, 2, 3):
            s = (J / f'licao-{n}/index.html').read_text('utf-8')
            self.assertIn(YT[n], s, n)
            for o in {1, 2, 3} - {n}:
                self.assertIn(f'<a href="../licao-{o}/">Lição {o}:', s, (n, o))
        g = (J / 'guiao/index.html').read_text('utf-8')
        # 26/10: título aprovado pelo docente; conceitos e cadeia conservados.
        self.assertIn('Lição 3: Até onde vai a minha liberdade?', g)
        self.assertIn('Lição 3: Até onde vai a minha liberdade? (episódio 3', (J / 'docente/index.html').read_text('utf-8'))

    def test_house_rules_and_local_links(self):
        # 02/11/2026: a expressão inclui também o substantivo proibido.
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
