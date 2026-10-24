from pathlib import Path
import json, os, re, unittest
# Na pasta tests do Lente, a raiz é a pasta de cima; LENTE_RAIZ aponta para outra cópia (nas fontes, antes de o teste ir para o Lente).
R = Path(os.environ.get('LENTE_RAIZ') or Path(__file__).resolve().parents[1])
U = 'https://pedrohfernandes-klk.github.io/lente/'
HOJE = json.loads(Path(__file__).with_name('enderecos-2026-10-23.json').read_text('utf-8'))


def passagem(s):
    """a página de passagem do molde de 23/10/2026 (lente-passagens.mjs nas fontes): marca data-passagem e location.replace"""
    return bool(re.search(r'<html[^>]*\bdata-passagem\b', s)) and 'location.replace(' in s


def destino(s):
    m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    return m.group(1) if m else None


class Enderecos(unittest.TestCase):
    """Nenhum endereço do Lente de 23/10/2026 se perde (plano de reestruturação do Lente, secção 4): cada página que existia continua
    a existir ou passa a ser uma página de passagem para uma página que existe, sem cadeias."""

    def test_cada_endereco_de_hoje_existe(self):
        falta = [p or '(a entrada)' for p in HOJE['paginas'] if not (R / p / 'index.html').exists()]
        self.assertEqual(falta, [], 'endereços de 23/10/2026 sem página nem passagem')
        for f in HOJE['ficheiros']:
            self.assertTrue((R / f).exists(), f)

    def test_a_entrada_e_a_pagina_de_erro_nunca_sao_passagens(self):
        for f in ['index.html', '404.html']:
            self.assertFalse(passagem((R / f).read_text('utf-8')), f)

    def test_cada_passagem_leva_a_uma_pagina_que_existe(self):
        for p in HOJE['paginas']:
            s = (R / p / 'index.html').read_text('utf-8')
            if not passagem(s):
                continue
            d = destino(s)
            self.assertTrue(d and d.startswith(U), (p, d))
            alvo = R / d[len(U):].split('#')[0] / 'index.html'
            self.assertTrue(alvo.exists(), (p, d))
            self.assertFalse(passagem(alvo.read_text('utf-8')), f'{p}: a passagem leva a outra passagem ({d})')


if __name__ == '__main__':
    unittest.main()
