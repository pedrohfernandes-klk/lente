# 03/11/2026: aproximação única e repouso final, sem salto entre ciclos.
"""02/11/2026: decisão 125 (docente). 05/11/2026: decisão 142, colagem de fotografia (Rossio, entre 1906 e 1914) e traço.
 Fundo animado a traço «Os carris» na entrada da Justiça.

O desenho é decorativo (aria-hidden) e integra a abertura. A aproximação única termina antes da agulha.
Sem JavaScript, com movimento reduzido e em projeção, mostra logo esse estado final. Não sai na impressão.
A alavanca fica neutra, nenhum ramo é escolhido e nunca há pessoas nos carris.
"""
from pathlib import Path
import re
import unittest
import importlib.util
import xml.etree.ElementTree as ET

R = Path(__file__).resolve().parents[1]
HTML = (R / 'olhar-e-decidir/justica/index.html').read_text('utf-8')
CSS = (R / 'assets/fundo-carris.css').read_text('utf-8')
# 02/11/2026: decisão 137. O script próprio saiu: o movimento é do motor comum (assets/fundos.js e assets/fundos.css).
JS = (R / 'assets/fundos.js').read_text('utf-8')
MOTOR_CSS = (R / 'assets/fundos.css').read_text('utf-8')
spec = importlib.util.spec_from_file_location('gerar_carris', R / 'tools/gerar_carris.py')
GERADOR = importlib.util.module_from_spec(spec)
spec.loader.exec_module(GERADOR)


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
        # 02/11/2026: decisão 137. O fundo leva a marca do motor comum e o crédito o botão «Parar o desenho», escondido sem script.
        self.assertIn(lead + '\n<div class="jc-fundo" aria-hidden="true" data-fundo="jc" data-fundo-ciclo="36"><svg ', HTML)
        # 02/11/2026: encargo das 20h, crédito descreve a nova cena, não afirma uma reconstituição histórica.
        self.assertIn('<p class="jc-credito">'+GERADOR.CREDITO+' <button type="button" class="fundo-botao" data-fundo-botao="jc" hidden>Parar o desenho</button></p>', HTML)
        # 02/11/2026: atribuição editorial expressa do docente, também nos grafismos vetoriais.
        self.assertIn('Grafismo gerado com recurso a IA, EPI, 2026.', HTML)
        self.assertNotIn('Desenho nosso', HTML)
        self.assertNotIn('jc-anda', HTML, 'o movimento só se liga pelo script')
        self.assertEqual(HTML.count('class="jc-alavanca"'), 1)
        self.assertEqual(HTML.count('class="jc-eletrico"'), 1)
        self.assertEqual(HTML.count('class="jc-agulha"'), 1)
        # 05/11/2026: decisão 142. As duas vias possíveis, desenhadas por cima da fotografia, uma de cada.
        self.assertEqual(HTML.count('class="jc-via jc-via-a"'), 1)
        self.assertEqual(HTML.count('class="jc-via jc-via-b"'), 1)
        self.assertIn('../../assets/fundo-carris.css?v=', HTML)
        self.assertIn('../../assets/fundos.css?v=', HTML)
        self.assertIn('<script defer src="../../assets/fundos.js?v=', HTML)
        self.assertNotIn('fundo-carris.js', HTML)

    def test_animacoes_so_no_bloco_de_movimento(self):
        movimento = bloco(CSS, '@media(prefers-reduced-motion:no-preference){')
        usos = list(re.finditer(r'animation(?:-name)?:\s*([\w-]+)', CSS))
        # 02/11/2026: só o elétrico se move; a alavanca não escolhe um ramo.
        # 05/11/2026: decisão 142. A aproximação da fotografia e as duas vias que se acendem à vez; a alavanca e a agulha não mexem.
        self.assertEqual([x.group(1) for x in usos], ['jc-aproxima', 'jc-via-a', 'jc-via-b'])
        for uso in usos:
            self.assertIn(uso.group(0), movimento)
        for linha in movimento.splitlines()[1:-1]:
            self.assertTrue(linha.startswith('html:not(.em-projecao) .ju .jc-anda '), linha)
        # 02/11/2026: decisão 137. A pausa fora do ecrã e com o separador escondido é a do motor comum.
        self.assertIn('[data-fundo].fundo-pausa *{animation-play-state:paused!important}', MOTOR_CSS)
        self.assertIn('@media print{.ju .jc-fundo{display:none}}', CSS)

    def test_aproximacao_sem_escolher_um_ramo(self):
        # 02/11/2026: substitui o ciclo simétrico da decisão anterior pelo novo contrato explícito: nenhum desfecho.
        # 05/11/2026: decisão 142. Com a colagem, a aproximação é a da fotografia (escala de 1 para 1,04, a mesma regra de
        # repouso: parado mostra a chegada); as vias começam e acabam iguais, por isso nenhuma fica escolhida.
        anim = bloco(CSS, '@keyframes jc-aproxima{')
        self.assertIn('0%,10%{transform:scale(1)}', anim)
        self.assertIn('60%,100%{transform:scale(1.04)}', anim)
        self.assertIn('animation:jc-aproxima 36s ease-in-out 1;', CSS)
        self.assertIn('transform:scale(1.04)}', bloco(CSS, '.ju .jc-eletrico{'))
        for via in ('jc-via-a', 'jc-via-b'):
            k = bloco(CSS, '@keyframes ' + via + '{')
            self.assertIn('0%,100%{opacity:1}', k)
            self.assertIn('animation:' + via + ' 36s ease-in-out 1;', CSS)
        self.assertIn('<header class="jc-abertura">',HTML)
        self.assertNotIn('pára',GERADOR.CREDITO)
        self.assertNotRegex(CSS, r'jc-(?:alavanca|agulha|ramo)[^{]*\{')
        # O elétrico (marcado a tracejado) fica acima da agulha: nunca a passa.
        alvo = re.search(r'class="jc-alvo" d="M(\d+) (\d+)h(\d+)v(\d+)', HTML)
        agulha = re.search(r'class="jc-agulha" d="M(\d+) (\d+)', HTML)
        self.assertLess(int(alvo.group(2)) + int(alvo.group(4)), int(agulha.group(2)), 'o elétrico pára antes da agulha')

    def test_svg_deterministico_seguro_e_integracao_reproduzivel(self):
        # 02/11/2026: ficheiro, integração e duas execuções coincidem, sem dispensar nenhuma conferência anterior.
        svg = (R / 'assets/carris-eletrico.svg').read_text('utf-8')
        # 05/11/2026: o SVG avulso aponta para a fotografia a partir de assets/; a página, a partir de ../../assets/.
        self.assertEqual(svg, GERADOR.cena(GERADOR.FOTO))
        self.assertEqual(GERADOR.cena(), GERADOR.cena())
        self.assertEqual(HTML, GERADOR.instalar(HTML))
        self.assertLess(len(svg.encode('utf-8')), 120_000)
        tree = ET.fromstring(svg)
        # 05/11/2026: decisão 142. A colagem tem uma fotografia: só uma <image>, local, a do Rossio registada no gerador
        # (WebP, menos de 250 KB, SHA-256 conferido). Continuam proibidos scripts, foreignObject, ligações e eventos.
        imagens = []
        for node in tree.iter():
            tag = node.tag.split('}')[-1]
            self.assertNotIn(tag, ['script','foreignObject','a'])
            self.assertFalse(any(k.split('}')[-1].startswith('on') or k.split('}')[-1] == 'src' for k in node.attrib))
            hrefs = [v for k, v in node.attrib.items() if k.split('}')[-1] == 'href']
            if tag == 'image':
                imagens.append(hrefs)
            else:
                self.assertEqual(hrefs, [])
        self.assertEqual(imagens, [[GERADOR.FOTO]])
        foto = R / 'assets' / GERADOR.FOTO
        dados = foto.read_bytes()
        self.assertEqual(dados[:4] + dados[8:12], b'RIFFWEBP')
        self.assertLess(len(dados), 250_000)
        import hashlib
        self.assertEqual(hashlib.sha256(dados).hexdigest(), GERADOR.FOTO_SHA256)
        self.assertEqual(HTML.count('<image class="jc-foto" href="../../assets/' + GERADOR.FOTO + '"'), 1)
        self.assertIn('random.Random(20261105)', (R/'tools/gerar_carris.py').read_text('utf-8'))

    def test_faixa_ocupa_a_largura_e_mantem_a_escala(self):
        # 02/11/2026: alturas contratadas, sem uma faixa reduzida a uma percentagem da cena.
        self.assertIn('height:clamp(232px,64vw,300px)', CSS)
        self.assertIn('height:340px', CSS)
        self.assertIn('height:clamp(360px,44vh,440px)', CSS)
        self.assertIn('margin-left:calc(50% - 50vw);margin-right:calc(50% - 50vw)', CSS)

    def test_script_respeita_projecao_e_movimento_reduzido(self):
        self.assertIn("matchMedia('(prefers-reduced-motion: no-preference)')", JS)
        # 02/11/2026: decisão 137. A mesma condição da moldura, escrita no motor comum com espaços.
        self.assertIn('window.self !== window.top', JS)
        self.assertIn('projetar=1', JS)
        # 02/11/2026: decisão 137. O motor liga <prefixo>-anda (aqui jc-anda), pausa com o separador escondido, pára ao fim de dois
        # ciclos e desliga-se se a moldura de projeção marcar a página depois de carregar.
        self.assertIn("classList.add(p + '-anda')", JS)
        self.assertIn('IntersectionObserver', JS)
        self.assertIn('visibilitychange', JS)
        self.assertIn('setTimeout(parar, 2 * ciclo)', JS)
        self.assertIn('epi-projection', JS)
        self.assertIn('MutationObserver', JS)
        self.assertNotRegex(JS, r'localStorage|sessionStorage')


if __name__ == '__main__':
    unittest.main()
