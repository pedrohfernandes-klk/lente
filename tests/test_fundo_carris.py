"""02/11/2026: decisão 125 (docente). Fundo animado a traço «Os carris» na entrada da Justiça.

O desenho é decorativo (aria-hidden) e fica numa faixa abaixo da apresentação, sem mudar o texto da página. Parado por
omissão (sem JavaScript, com movimento reduzido e na projeção: a alavanca a meio e os dois ramos iguais); não sai na
impressão. Os dois lados do ciclo da alavanca têm o mesmo tempo, e nunca há pessoas nos carris.
"""
from pathlib import Path
import re
import unittest

R = Path(__file__).resolve().parents[1]
HTML = (R / 'olhar-e-decidir/justica/index.html').read_text('utf-8')
CSS = (R / 'assets/fundo-carris.css').read_text('utf-8')
JS = (R / 'assets/fundo-carris.js').read_text('utf-8')


def bloco(texto, inicio):
    i = texto.index(inicio)
    nivel = 0
    for j in range(i, len(texto)):
        if texto[j] == '{':
            nivel += 1
        elif texto[j] == '}':
            nivel -= 1
            if nivel == 0:
                return texto[i:j + 1]
    raise AssertionError(inicio)


class FundoCarris(unittest.TestCase):
    def test_faixa_decorativa_depois_da_apresentacao(self):
        lead = '<p class="lead">Qual é a coisa certa a fazer? Vês Michael Sandel a ensinar, em excertos das aulas que deu em Harvard, decides antes de ouvires a sala e levas as razões para o debate.</p>'
        self.assertIn(lead + '\n<div class="jc-fundo" aria-hidden="true"><svg ', HTML)
        self.assertIn('<p class="jc-credito">Desenho nosso, a traço, EPI, 2026, a partir do caso do elétrico (Philippa Foot, 1967), '
                      'com que Michael Sandel abre o curso <i>Justice</i>.</p>', HTML)
        self.assertNotIn('jc-anda', HTML, 'o movimento só se liga pelo script')
        self.assertEqual(HTML.count('class="jc-alavanca"'), 1)
        self.assertEqual(HTML.count('class="jc-ramo jc-ramo-e"'), 1)
        self.assertEqual(HTML.count('class="jc-ramo jc-ramo-d"'), 1)
        self.assertIn('../../assets/fundo-carris.css?v=', HTML)
        self.assertIn('<script defer src="../../assets/fundo-carris.js?v=', HTML)

    def test_animacoes_so_no_bloco_de_movimento(self):
        movimento = bloco(CSS, '@media(prefers-reduced-motion:no-preference){')
        usos = list(re.finditer(r'animation(?:-name)?:\s*([\w-]+)', CSS))
        self.assertEqual(len(usos), 5)
        for uso in usos:
            self.assertIn(uso.group(0), movimento)
        for linha in movimento.splitlines()[1:-1]:
            self.assertTrue(linha.startswith('html:not(.em-projecao) .ju .jc-anda '), linha)
        self.assertIn('.ju .jc-fora *{animation-play-state:paused!important}', CSS)
        self.assertIn('@media print{.ju .jc-fundo{display:none}}', CSS)

    def test_tempo_igual_dos_dois_lados(self):
        # a alavanca fica 7 s à esquerda e 7 s à direita (36 s por ciclo); o ramo aceso segue-a, com o mesmo tempo
        alav = bloco(CSS, '@keyframes jc-alav{')
        self.assertIn('16.667%,36.111%{transform:rotate(-16deg)}', alav)
        self.assertIn('66.667%,86.111%{transform:rotate(16deg)}', alav)
        e, d = bloco(CSS, '@keyframes jc-ramo-e{'), bloco(CSS, '@keyframes jc-ramo-d{')
        self.assertIn('16.667%,36.111%{color:var(--jc-acento);opacity:1}', e)
        self.assertIn('66.667%,86.111%{color:var(--jc-acento);opacity:1}', d)
        self.assertAlmostEqual(36.111 - 16.667, 86.111 - 66.667, places=3)

    def test_script_respeita_projecao_e_movimento_reduzido(self):
        self.assertIn("matchMedia('(prefers-reduced-motion: no-preference)')", JS)
        self.assertIn('window.self!==window.top', JS)
        self.assertIn('projetar=1', JS)
        self.assertIn("classList.add('jc-anda')", JS)
        self.assertIn('IntersectionObserver', JS)
        self.assertNotRegex(JS, r'localStorage|sessionStorage')


if __name__ == '__main__':
    unittest.main()
