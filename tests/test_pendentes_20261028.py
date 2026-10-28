"""28/10/2026: pendentes do #65 (Cidadania M2) corrigidos fora do molde das sessões."""
from pathlib import Path
import unittest

R = Path(__file__).resolve().parents[1]


def ler(p):
    return (R / p).read_text('utf-8')


class Pendentes(unittest.TestCase):
    def test_orwell_liga_ao_livro_certo(self):
        # O n.º 70483 do Project Gutenberg é «Children of the Lens», de E. E. Smith, e não um livro de Orwell.
        for p in R.rglob('*.html'):
            if '.git' in p.parts:
                continue
            self.assertNotIn('gutenberg.org/ebooks/70483', p.read_text('utf-8', errors='ignore'), str(p.relative_to(R)))
        for p in ('gigantes/triunfo-porcos/index.html', 'sidequests/poder/index.html', 'biblioteca/animal-farm-capitulo-2/index.html'):
            self.assertIn('gutenberg.net.au/ebooks01/0100011.txt', ler(p), p)
        for p in ('gigantes/1984/index.html', 'sidequests/orwell/index.html', 'biblioteca/1984-capitulo-1/index.html'):
            self.assertIn('gutenberg.net.au/ebooks01/0100021.txt', ler(p), p)

    def test_sem_ancora_inexistente_de_siza(self):
        # Ver para fazer não tem nenhum vídeo de Siza publicado: a ligação levava ao topo da página.
        self.assertNotIn('ver-para-fazer/#siza', ler('narrativas/oficina-espaco/index.html'))

    def test_turco_sem_jogador_e_suposicao_com_tu(self):
        for p in ('cidadania/m2/passo-04/index.html', 'cidadania/m2/revisao/index.html'):
            self.assertNotIn('jogador', ler(p), p)
        self.assertIn('O que achas que aconteceu, sem o poderes confirmar.', ler('cidadania/m2/glossario/index.html'))

    def test_contra_feed_com_texto_alternativo_em_portugues(self):
        s = ler('projetos/contra-feed/index.html')
        self.assertNotIn('An Experiment on a Bird in an Air Pump by', s)
        self.assertIn('Pintura a óleo, noturna', s)


if __name__ == '__main__':
    unittest.main()
