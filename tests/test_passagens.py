from pathlib import Path
import os, re, unittest
# Na pasta tests do Lente, a raiz é a pasta de cima; LENTE_RAIZ aponta para outra cópia (nas fontes, antes de o teste ir para o Lente).
R = Path(os.environ.get('LENTE_RAIZ') or Path(__file__).resolve().parents[1])
U = 'https://pedrohfernandes-klk.github.io/lente/'
FORA = {'tests', 'docs', 'assets', 'img', 'fontes'}


def paginas():
    return sorted(p for p in R.rglob('index.html') if not (set(p.relative_to(R).parts[:1]) & FORA) and not any(x.startswith('.') for x in p.relative_to(R).parts))


def passagem(s):
    return bool(re.search(r'<html[^>]*\bdata-passagem\b', s)) and 'location.replace(' in s


class Passagens(unittest.TestCase):
    """As páginas de passagem do Lente (plano de reestruturação do Lente, secção 4): um endereço antigo projetado continua projetado e o QR
    da moldura continua a levar à âncora certa. Cada passagem faz location.replace(destino + location.search + (location.hash || âncora)),
    com o meta refresh só como recurso (em <noscript>), <link rel="canonical"> e uma linha de texto com a ligação. O comportamento no
    navegador está em browser_passagens.py."""

    @classmethod
    def setUpClass(cls):
        cls.todas = {p: p.read_text('utf-8') for p in paginas()}
        cls.passagens = {p: s for p, s in cls.todas.items() if passagem(s)}

    def test_ha_passagens(self):
        # desde o lote 1 (mapa/, ler/ e curadoria/) o Lente tem sempre páginas de passagem
        self.assertTrue(self.passagens, 'nenhuma página de passagem no Lente')

    def test_cada_passagem_guarda_a_pesquisa_e_a_ancora(self):
        for p, s in self.passagens.items():
            m = re.search(r'<link rel="canonical" href="([^"]+)">', s)
            self.assertTrue(m, p)
            d = m.group(1)
            self.assertTrue(d.startswith(U) and '#' not in d, (p, d))
            j = re.search(r'<script>location\.replace\("([^"]+)"\+location\.search\+\(location\.hash\|\|"((?:#[A-Za-z][\w-]*)?)"\)\)</script>', s)
            self.assertTrue(j, f'{p}: o script não guarda location.search e location.hash')
            self.assertEqual(j.group(1), d, p)
            a = j.group(2)
            self.assertIn(f'<noscript><meta http-equiv="refresh" content="0; url={d}{a}"></noscript>', s, p)
            self.assertLess(s.index('location.replace('), s.index('http-equiv="refresh"'), p)
            self.assertRegex(s, r'<p>[^<]+<a href="' + re.escape(d + a) + r'">[^<]+</a>\.</p>', p)
            self.assertIn('<html lang="pt-PT" data-passagem>', s, p)
            self.assertIn('<meta name="robots" content="noindex">', s, p)

    def test_nenhum_outro_redirecionamento(self):
        # um meta refresh ou um location.replace fora do molde perde «?projetar=1» ou a âncora
        for p, s in self.todas.items():
            if 'http-equiv="refresh"' in s or 'location.replace(' in s:
                self.assertIn(p, self.passagens, f'{p}: redirecionamento fora do molde das passagens')


if __name__ == '__main__':
    unittest.main()
