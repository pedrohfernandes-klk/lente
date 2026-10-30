from pathlib import Path
import re, json, math, unittest
from html import unescape
R = Path(__file__).resolve().parents[1]
O = R / 'olhar-e-decidir'
LENTE = 'https://pedrohfernandes-klk.github.io/lente/'
PROIBIDAS = re.compile(r'(?<![\wÀ-ÿ])(?:professor(?:a|es|as)?|jog(?:ar|a|as|amos|am|ou|ue|uei|ando|ado)|fichas?|folhas?)(?![\wÀ-ÿ])', re.I)
# lições novas de Ter juízo (decisão do docente de 23/10/2026): Singer, Nagel, Hume e Kant, no formato das lições da Justiça
LICOES = {'etica/licao-1': 'lente-etica-licao-1', 'etica/licao-2': 'lente-etica-licao-2', 'estetica/licao-1': 'lente-estetica-licao-1'}


def montar(p):
    s = p.read_text('utf-8')
    k = s.index('itens:', s.index('EPIJogo.montar(')) + len('itens:')
    itens, _ = json.JSONDecoder().raw_decode(s, k)
    return s, itens, re.search(r'chave:"([^"]+)"', s[k:]).group(1)


class TerJuizo(unittest.TestCase):
    def test_licoes_chave_e_regras(self):
        for pasta, chave in LICOES.items():
            s, itens, k = montar(O / pasta / 'index.html')
            self.assertEqual(k, chave)
            self.assertTrue(18 <= len(itens) <= 26, (pasta, len(itens)))
            self.assertIn('id="casca-pc"', s)
            curtas, esperado = 0, 0.0
            for x in itens:
                if x['t'] == 'escolha':
                    self.assertEqual(len(x['o']), len(x['fe']))
                    self.assertTrue(all((j == x['c']) == (x['fe'][j] is None) for j in range(len(x['o']))), pasta)
                    # 30/10/2026: opções equilibradas (pedido do docente)
                    n = [len(re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]*>', '', o)).replace('_', '').replace('*', '')).strip()) for o in x['o']]
                    self.assertLessEqual(max(n), 1.2 * min(n), x['p'])
                    # 30/10/2026: revisão do #72 (opções equilibradas): volta a regra antiga, a certa nunca é mais longa
                    # do que a maior errada, a par da amplitude de 20 %; e não pode ser a mais curta mais vezes do que ceil(n/k).
                    self.assertLess(len(x['o'][x['c']]), max(len(o) for j, o in enumerate(x['o']) if j != x['c']), (pasta, x['p']))
                    curtas += n[x['c']] < min(v for j, v in enumerate(n) if j != x['c'])
                    esperado += 1 / len(x['o'])
                if x['t'] == 'vf':
                    self.assertIsInstance(x['v'], bool)
                    self.assertIsInstance(x['fe'], str)
                # fora do «html», o motor escapa as etiquetas: só _itálico_ e **negrito**
                fora = json.dumps({c: v for c, v in x.items() if c not in ('html', 't', 'rot', 'titulo')}, ensure_ascii=False)
                self.assertNotRegex(fora, r'<[a-z/]', (pasta, x.get('rot')))
                txt = re.sub(r'<[^>]+>', ' ', json.dumps(x, ensure_ascii=False))
                self.assertNotIn('—', txt, pasta)
                self.assertIsNone(PROIBIDAS.search(txt), (pasta, x.get('rot')))
                self.assertNotRegex(txt, r'[^\s"]\s·\s[^\s"]', pasta)
            self.assertLessEqual(curtas, math.ceil(esperado), pasta)

    def test_imagens_existem_e_tem_credito(self):
        for pasta in LICOES:
            s, itens, _ = montar(O / pasta / 'index.html')
            for x in itens:
                for fig in re.findall(r'<figure class="fig">.*?</figure>', x.get('html', ''), re.S):
                    src = re.search(r'src="([^"]+)"', fig).group(1)
                    self.assertTrue(src.startswith(LENTE), src)
                    self.assertTrue((R / src[len(LENTE):]).exists(), src)
                    self.assertRegex(fig, r'domínio público|CC BY', src)
                    self.assertRegex(fig, r'alt="[^"]{20,}"', src)

    def test_cadeia_e_entrada(self):
        hub = (O / 'index.html').read_text('utf-8')
        for pasta in list(LICOES) + ['justica/licao-3']:
            self.assertIn(f'{LENTE}olhar-e-decidir/{pasta}/', hub, pasta)
        _, _, _ = montar(O / 'etica/licao-1/index.html')
        s1 = (O / 'etica/licao-1/index.html').read_text('utf-8')
        self.assertIn(f'seguinte:"{LENTE}olhar-e-decidir/etica/licao-2/"', s1)
        s2 = (O / 'etica/licao-2/index.html').read_text('utf-8')
        self.assertIn(f'seguinte:"{LENTE}olhar-e-decidir/estetica/licao-1/"', s2)

    def test_ligacoes_locais_existem(self):
        for pasta in LICOES:
            s = (O / pasta / 'index.html').read_text('utf-8')
            for href in set(re.findall(r'href=\\?"(https://pedrohfernandes-klk\.github\.io/lente/[^"\\#?]*)', s)):
                alvo = R / href[len(LENTE):]
                if not alvo.suffix:
                    alvo = alvo / 'index.html'
                self.assertTrue(alvo.exists(), (pasta, href))


if __name__ == '__main__':
    unittest.main()
