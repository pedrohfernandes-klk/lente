from pathlib import Path
import json, re, unittest
R = Path(__file__).resolve().parents[1]
M = json.loads((R / 'tests/lab-manifesto.json').read_text('utf-8'))


class Manifesto(unittest.TestCase):
    """Nada do Laboratório desaparece sem decisão: endereços, âncoras e chaves de progresso (relatório de 23/10/2026, D0)."""

    def test_paginas_existem(self):
        falta = [p for p in M['paginas'] if not (R / p / 'index.html').exists()]
        self.assertEqual(falta, [])

    def test_ancoras_existem(self):
        for rel, ids in M['ancoras'].items():
            # 30/10/2026: Laboratório simples (pedido do docente). As âncoras e leituras de progresso vivem no catálogo.
            destino = 'narrativas/tudo' if rel.rstrip('/') == 'narrativas' else rel
            s = (R / destino / 'index.html').read_text('utf-8')
            tem = set(re.findall(r'\bid="([^"]+)"', s))
            self.assertEqual(sorted(set(ids) - tem), [], rel or 'index.html')

    def test_chaves_de_progresso_mantem_se(self):
        for rel, chaves in M['chaves'].items():
            # 30/10/2026: Laboratório simples (pedido do docente). As âncoras e leituras de progresso vivem no catálogo.
            destino = 'narrativas/tudo' if rel.rstrip('/') == 'narrativas' else rel
            s = (R / destino / 'index.html').read_text('utf-8')
            for k in chaves:
                self.assertTrue(f'"{k}"' in s, (rel, k))


if __name__ == '__main__':
    unittest.main()
