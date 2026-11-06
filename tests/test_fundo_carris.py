# 03/11/2026: aproximação única e repouso final, sem salto entre ciclos.
"""02/11/2026: decisão 125 (docente). 05/11/2026: decisão 142, colagem de fotografia (Rossio, entre 1906 e 1914) e traço.
 05/11/2026: pedido do docente (alavanca ao lado dos carris, elétrico que não vem de frente): a fotografia passa a ser a do
 elétrico 541 visto de lado no Largo do Corpo Santo (Philip Mallis, 2025, CC BY-SA 4.0); as exigências mantêm-se todas.
 05/11/2026: pedido do docente («o elétrico n pode virar numa das direções»): o elétrico passa a recorte, sobre uma via
 desenhada, com a agulha à frente e as duas vias no sentido em que anda; as exigências continuam todas.
 06/11/2026: decisão 170 (docente: «o elétrico da ilustração de justiça deve ter animação, talvez os pontos vermelhos pisquem e
 talvez surjam uns pontos de exclamação»; depois, «a alavanca move, claro»). A alavanca passa a mexer-se (vai a um lado, volta ao
 meio, vai ao outro e acaba ao meio), com as lâminas; a via indicada pisca devagar; surgem sinais de alerta a traço à frente do
 elétrico e junto à alavanca, nunca nas vias. O desenho parado continua neutro e as outras exigências continuam todas.
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


def passos(keyframes):
    """06/11/2026: decisão 170. Os quadros de um @keyframes, por ordem: [(percentagem, {propriedade: valor}), ...]."""
    corpo = keyframes[keyframes.index('{') + 1:-1]
    quadros = {}
    for seletor, decl in re.findall(r'([\d.%,]+)\{([^{}]*)\}', corpo):
        props = dict(tuple(x.strip() for x in d.split(':', 1)) for d in decl.split(';') if d.strip())
        for pct in seletor.split(','):
            quadros.setdefault(float(pct.rstrip('%')), {}).update(props)
    return sorted(quadros.items())


def valor_em(quadros, prop, pct):
    """Valor numérico de prop em pct, por interpolação linear entre os quadros que a definem."""
    pontos = [(t, float(re.sub(r'[^\d.-]', '', v[prop]))) for t, v in quadros if prop in v]
    for (t0, v0), (t1, v1) in zip(pontos, pontos[1:]):
        if t0 <= pct <= t1:
            return v0 if t1 == t0 else v0 + (v1 - v0) * (pct - t0) / (t1 - t0)
    raise AssertionError((prop, pct))


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
        # 06/11/2026: decisão 170. As peças que mexem, uma de cada: o braço da alavanca, as duas lâminas e os quatro sinais.
        for classe in ('jc-alavanca-braco', 'jc-agulha-perto', 'jc-agulha-longe'):
            self.assertEqual(HTML.count('class="' + classe + '"'), 1, classe)
        self.assertEqual(re.findall(r'class="jc-sinal (jc-sinal-\d)"', HTML), ['jc-sinal-1', 'jc-sinal-2', 'jc-sinal-3', 'jc-sinal-4'])
        self.assertIn('../../assets/fundo-carris.css?v=', HTML)
        self.assertIn('../../assets/fundos.css?v=', HTML)
        self.assertIn('<script defer src="../../assets/fundos.js?v=', HTML)
        self.assertNotIn('fundo-carris.js', HTML)

    def test_animacoes_so_no_bloco_de_movimento(self):
        movimento = bloco(CSS, '@media(prefers-reduced-motion:no-preference){')
        usos = list(re.finditer(r'animation(?:-name)?:\s*([\w-]+)', CSS))
        # 02/11/2026: só o elétrico se move; a alavanca não escolhe um ramo.
        # 05/11/2026: decisão 142. A aproximação da fotografia e as duas vias que se acendem à vez; a alavanca e a agulha não mexem.
        # 06/11/2026: decisão 170. Lista fechada, por esta ordem: a aproximação, as duas vias (agora a piscar à vez), a alavanca,
        # as duas lâminas e os quatro sinais de alerta. Uma animação a mais ou a menos falha.
        self.assertEqual([x.group(1) for x in usos], ['jc-aproxima', 'jc-via-a', 'jc-via-b', 'jc-alavanca', 'jc-agulha-longe',
                                                      'jc-agulha-perto', 'jc-sinal-1', 'jc-sinal-2', 'jc-sinal-3', 'jc-sinal-4'])
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
        # 05/11/2026: revisão de 5/11 (lente-justica-4). A aproximação continua de 1 a 1,04 (um movimento só), e a fotografia entra
        # a partir de transparente no primeiro segundo e meio: ao recomeçar, a troca de 1,04 para 1 fica escondida. Fixam-se os quatro
        # pontos (mais do que os dois de antes), por isso a exigência não baixa.
        self.assertIn('0%{transform:scale(1);opacity:0}', anim)
        self.assertIn('4%{opacity:1}', anim)
        self.assertIn('10%{transform:scale(1)}', anim)
        self.assertIn('60%,100%{transform:scale(1.04);opacity:1}', anim)
        self.assertIn('animation:jc-aproxima 36s ease-in-out 1;', CSS)
        self.assertIn('transform:scale(1.04)}', bloco(CSS, '.ju .jc-eletrico{'))
        for via in ('jc-via-a', 'jc-via-b'):
            k = bloco(CSS, '@keyframes ' + via + '{')
            # 06/11/2026: decisão 170. As vias piscam à vez, mas continuam a começar e a acabar iguais (opacidade 1), por isso
            # nenhuma fica escolhida; o 0% e o 100% conferem-se no próprio quadro, não pela forma de o escrever.
            quadros = passos(k)
            self.assertEqual((quadros[0][0], quadros[0][1].get('opacity')), (0.0, '1'), via)
            self.assertEqual((quadros[-1][0], quadros[-1][1].get('opacity')), (100.0, '1'), via)
            self.assertIn('animation:' + via + ' 36s ease-in-out 1;', CSS)
        self.assertIn('<header class="jc-abertura">',HTML)
        self.assertNotIn('pára',GERADOR.CREDITO)
        # 06/11/2026: decisão 170 («a alavanca move, claro»). Antes, nenhuma regra podia nomear a alavanca ou a agulha. Agora
        # mexem-se, mas só dentro do bloco do movimento (ver Movimento170) e acabam onde começaram: a alavanca a direito e as
        # lâminas encostadas, sem desfecho. Fora do bloco, continua a não haver nenhuma regra para elas; «jc-ramo» continua proibido.
        fora = CSS.replace(bloco(CSS, '@media(prefers-reduced-motion:no-preference){'), '')
        fora = re.sub(r'@keyframes [\w-]+\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}', '', fora)
        self.assertNotRegex(fora, r'jc-(?:alavanca|agulha|ramo|sinal)[^{]*\{')
        self.assertNotIn('jc-ramo', CSS)
        for nome in ('jc-alavanca', 'jc-agulha-longe', 'jc-agulha-perto'):
            quadros = passos(bloco(CSS, '@keyframes ' + nome + '{'))
            self.assertEqual((quadros[0][0], quadros[0][1]), (0.0, {'transform': 'rotate(0deg)'}), nome)
            self.assertEqual((quadros[-1][0], quadros[-1][1]), (100.0, {'transform': 'rotate(0deg)'}), nome)
        # O elétrico (marcado a tracejado) fica acima da agulha: nunca a passa.
        # 06/11/2026: decisão 170. A agulha passa a um grupo com as duas lâminas; confere-se a mais alta (a de longe) e a outra.
        alvo = re.search(r'class="jc-alvo" d="M(\d+) (\d+)h(\d+)v(\d+)', HTML)
        self.assertEqual(HTML.count('<g class="jc-agulha" '), 1)
        for lamina in ('jc-agulha-longe', 'jc-agulha-perto'):
            agulha = re.search(r'class="' + lamina + r'" d="M(\d+) (\d+)', HTML)
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
        # 05/11/2026: pedido do docente: a fotografia registada passa a ser o recorte do elétrico 541 (tools/tratar_corpo_santo.py).
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


class Movimento170(unittest.TestCase):
    """06/11/2026: decisão 170. A alavanca move-se, a via indicada pisca devagar e surgem sinais de alerta; tudo só com o motor
    comum ligado (jc-anda) e fora da projeção; parado, é a cena neutra do SVG."""
    CICLO = 36.0
    NOMES = ('jc-via-a', 'jc-via-b', 'jc-alavanca', 'jc-agulha-longe', 'jc-agulha-perto',
             'jc-sinal-1', 'jc-sinal-2', 'jc-sinal-3', 'jc-sinal-4')

    def setUp(self):
        self.movimento = bloco(CSS, '@media(prefers-reduced-motion:no-preference){')
        self.svg = (R / 'assets/carris-eletrico.svg').read_text('utf-8')

    def quadros(self, nome):
        return passos(bloco(CSS, '@keyframes ' + nome + '{'))

    def test_so_com_jc_anda_e_fora_da_projecao(self):
        # Cada animação e cada transformação das peças novas estão no bloco do movimento, em regras que começam todas por
        # html:not(.em-projecao) .ju .jc-anda; fora dele não há animação nem transição nenhuma.
        linhas = self.movimento.splitlines()[1:-1]
        self.assertTrue(linhas)
        for linha in linhas:
            self.assertTrue(linha.startswith('html:not(.em-projecao) .ju .jc-anda '), linha)
        fora = CSS.replace(self.movimento, '')
        fora = re.sub(r'@keyframes [\w-]+\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}', '', fora)
        self.assertNotRegex(fora, r'animation|transition')
        for nome in self.NOMES:
            self.assertEqual(self.movimento.count('animation:' + nome + ' 36s ease-in-out 1;animation-fill-mode:forwards}'), 1, nome)
            self.assertEqual(CSS.count('@keyframes ' + nome + '{'), 1, nome)
        # O ciclo do CSS é o do motor comum (data-fundo-ciclo="36"), que pára ao fim de dois ciclos.
        self.assertIn('data-fundo="jc" data-fundo-ciclo="36"', HTML)
        self.assertIn('setTimeout(parar, 2 * ciclo)', JS)

    def test_movimento_reduzido_e_desenho_parado_neutros(self):
        # Com movimento reduzido o bloco não se aplica (e o motor não liga jc-anda): fica o SVG, que é a cena neutra. No SVG,
        # nenhuma peça que mexe tem transform; os sinais têm opacity="0"; não há texto nenhum (nem letra de fonte nem emoji).
        self.assertTrue(CSS.count('@media(prefers-reduced-motion:no-preference){') == 1)
        self.assertNotIn('prefers-reduced-motion:reduce', CSS)
        self.assertIn("matchMedia('(prefers-reduced-motion: no-preference)')", JS)
        arvore = ET.fromstring(self.svg)
        classes = lambda n: (n.get('class') or '').split()
        for node in arvore.iter():
            self.assertNotIn(node.tag.split('}')[-1], ('text', 'tspan', 'textPath', 'use'))
            if set(classes(node)) & {'jc-alavanca', 'jc-alavanca-braco', 'jc-agulha', 'jc-agulha-longe', 'jc-agulha-perto', 'jc-via'}:
                self.assertIsNone(node.get('transform'), classes(node))
                self.assertIsNone(node.get('opacity'), classes(node))
        self.assertNotRegex(self.svg, r'[^\x00-\x7f]')

    def test_sinais_escondidos_no_desenho_parado(self):
        arvore = ET.fromstring(self.svg)
        sinais = [n for n in arvore.iter() if 'jc-sinal' in (n.get('class') or '').split()]
        self.assertEqual([n.get('class') for n in sinais], ['jc-sinal jc-sinal-%d' % i for i in (1, 2, 3, 4)])
        for g in sinais:
            self.assertEqual(g.tag.split('}')[-1], 'g')
            self.assertEqual(g.get('opacity'), '0')
            self.assertEqual(g.get('stroke'), 'var(--jc-terra,#a84939)')
            filhos = [f.tag.split('}')[-1] for f in g]
            self.assertEqual(filhos, ['path', 'circle'], 'uma haste e um ponto, a traço')
            for f in g.iter():
                self.assertIn(f.get('opacity'), (None, '0'))
        # Os sinais começam e acabam escondidos no ciclo.
        for i in (1, 2, 3, 4):
            q = self.quadros('jc-sinal-%d' % i)
            self.assertEqual((q[0][0], q[0][1]['opacity']), (0.0, '0'))
            self.assertEqual((q[-1][0], q[-1][1]['opacity']), (100.0, '0'))

    def test_nenhum_piscar_acima_de_tres_por_segundo(self):
        # WCAG 2.3.1: em todas as animações do ficheiro, entre dois mínimos (ou dois máximos) seguidos de opacidade passa pelo
        # menos 1/3 s. As vias piscam cinco vezes cada, uma a cada 1,08 s (cerca de uma por segundo, como decidido).
        nomes = re.findall(r'@keyframes ([\w-]+)\{', CSS)
        self.assertIn('jc-via-a', nomes)
        for nome in nomes:
            serie = [(t * self.CICLO / 100, float(v['opacity'])) for t, v in self.quadros(nome) if 'opacity' in v]
            limpa = [x for i, x in enumerate(serie) if i == 0 or x[1] != serie[i - 1][1]]
            minimos = [limpa[i][0] for i in range(1, len(limpa) - 1) if limpa[i][1] < limpa[i - 1][1] and limpa[i][1] < limpa[i + 1][1]]
            maximos = [limpa[i][0] for i in range(1, len(limpa) - 1) if limpa[i][1] > limpa[i - 1][1] and limpa[i][1] > limpa[i + 1][1]]
            for extremos in (minimos, maximos):
                for a, b in zip(extremos, extremos[1:]):
                    self.assertGreaterEqual(b - a, 1 / 3, (nome, a, b))
            if nome in ('jc-via-a', 'jc-via-b'):
                # Os piscares contam-se enquanto a alavanca aponta para a via (fora disso, a via só baixa de luz uma vez).
                ini, fim = {'jc-via-a': (22, 37), 'jc-via-b': (49, 64)}[nome]
                minimos = [t for t in minimos if ini * self.CICLO / 100 < t < fim * self.CICLO / 100]
                periodos = [round(b - a, 3) for a, b in zip(minimos, minimos[1:])]
                self.assertEqual(len(minimos), 5, nome)
                self.assertTrue(all(1.0 <= x <= 1.2 for x in periodos), (nome, periodos))

    def test_alavanca_lâminas_e_via_que_pisca_coincidem(self):
        # A alavanca vai para a direita (a via a direito, A) e depois para a esquerda (a via que curva, B), e acaba ao meio.
        # Enquanto aponta para uma via, só essa pisca e a lâmina que lhe corresponde abre; a via que pisca nunca fica mais
        # apagada do que a outra.
        alav, longe, perto = self.quadros('jc-alavanca'), self.quadros('jc-agulha-longe'), self.quadros('jc-agulha-perto')
        va, vb = self.quadros('jc-via-a'), self.quadros('jc-via-b')
        graus = lambda q, t: valor_em(q, 'transform', t)
        janelas = {'a': [t for t, v in alav if v.get('transform') == 'rotate(26deg)'],
                   'b': [t for t, v in alav if v.get('transform') == 'rotate(-26deg)']}
        self.assertEqual(janelas, {'a': [22.0, 37.0], 'b': [49.0, 64.0]})
        for t in (22, 30, 37):
            self.assertEqual((graus(longe, t), graus(perto, t)), (-12, 0))
        for t in (49, 56, 64):
            self.assertEqual((graus(longe, t), graus(perto, t)), (0, 10))
        for t in (0, 10, 41, 43, 45, 68, 80, 100):
            self.assertEqual((graus(alav, t), graus(longe, t), graus(perto, t)), (0, 0, 0), t)
        tempos = sorted({t for t, v in va + vb if 'opacity' in v})
        for (ini, fim), pisca, outra in (((22, 37), va, vb), ((49, 64), vb, va)):
            dentro = [t for t, v in pisca if 'opacity' in v and ini < t < fim]
            self.assertGreaterEqual(len(dentro), 9)
            self.assertEqual({v['opacity'] for t, v in outra if ini <= t <= fim and 'opacity' in v}, {'.25'})
            for t in tempos:
                if ini <= t <= fim:
                    self.assertGreaterEqual(valor_em(pisca, 'opacity', t), valor_em(outra, 'opacity', t), t)

    def test_pivos_na_geometria_do_desenho(self):
        # A haste roda sobre o seu pé, em cima da base; cada lâmina roda sobre o seu talão (a ponta direita).
        regra = lambda c: next(l for l in self.movimento.splitlines() if l.startswith('html:not(.em-projecao) .ju .jc-anda ' + c + '{'))
        haste = re.search(r'<g class="jc-alavanca-braco"><path d="M(\d+) (\d+)L', self.svg)
        base = re.search(r'<path d="M(\d+) (\d+)H(\d+)L', self.svg[self.svg.index('class="jc-alavanca"'):])
        self.assertEqual(haste.group(2), base.group(2), 'o pé da haste está no topo da base')
        self.assertTrue(int(base.group(1)) < int(haste.group(1)) < int(base.group(3)))
        self.assertIn('transform-box:view-box;transform-origin:%spx %spx;' % haste.groups(), regra('.jc-alavanca-braco'))
        for lamina in ('jc-agulha-longe', 'jc-agulha-perto'):
            x, y, dx, dy = map(int, re.search(r'class="' + lamina + r'" d="M(\d+) (\d+)l(\d+) ?(-?\d+)"', self.svg).groups())
            self.assertIn('transform-box:view-box;transform-origin:%dpx %dpx;' % (x + dx, y + dy), regra('.' + lamina))
        self.assertIn('transform-box:fill-box;transform-origin:50% 100%}', regra('.jc-sinal'))

    def test_tudo_o_que_mexe_no_recorte_do_telemovel_e_sinais_fora_das_vias(self):
        # O recorte mais estreito é a 320 px: a faixa tem 232 px de altura e 600 unidades, logo vê-se 320*600/232 unidades à
        # volta do meio da cena (670). Confere-se com o elétrico à escala 1 e 1,04 (a aproximação, sobre 500 465) e com os
        # sinais no salto (1,12 sobre o pé).
        import math
        meio, meia = 670, 320 * 600 / 232 / 2
        self.assertAlmostEqual(meio - meia, 256.2, places=1)
        pontos = []
        # A pega da alavanca nos dois extremos (raio 10 e traço 4) e as pontas das lâminas.
        hx, hy = 563, 548
        for graus in (-26, 0, 26):
            a = math.radians(graus)
            cx, cy = hx + (561 - hx) * math.cos(a) - (486 - hy) * math.sin(a), hy + (561 - hx) * math.sin(a) + (486 - hy) * math.cos(a)
            pontos += [(cx - 12, cy - 12), (cx + 12, cy + 12)]
        pontos += [(468, 456), (508, 472), (530, 546), (596, 562)]
        caixas = {}
        for i, g in enumerate(re.findall(r'<g class="jc-sinal jc-sinal-\d".*?</g>', self.svg), 1):
            # A haste (M x y Q x y x y) e o ponto (cx, cy, r), com meia largura de traço de folga.
            nums = [float(v) for v in re.findall(r'-?\d+(?:\.\d+)?', re.search(r'<path d="([^"]+)"', g).group(1))]
            cx, cy, r = (float(re.search(k + r'="([\d.]+)"', g).group(1)) for k in (' cx', ' cy', ' r'))
            xs, ys = nums[0::2] + [cx - r, cx + r], nums[1::2] + [cy - r, cy + r]
            self.assertEqual(len(nums), 6)
            x0, x1, y0, y1 = min(xs) - 2.5, max(xs) + 2.5, min(ys) - 2.5, max(ys) + 2.5
            # o salto de 1,12 sobre o meio do pé
            px = (x0 + x1) / 2
            x0, x1, y0 = px - (px - x0) * 1.12, px + (x1 - px) * 1.12, y1 - (y1 - y0) * 1.12
            caixas[i] = (x0, y0, x1, y1)
            pontos += [(x0, y0), (x1, y1)]
            # Nunca nas vias: ou no ar, acima dos carris (y < 440), ou no chão à direita da alavanca, longe da via que curva.
            self.assertTrue(y1 < 440 or (y0 > 482 and x0 > 600), (i, caixas[i]))
        self.assertEqual(len(caixas), 4)
        self.assertEqual(sum(1 for c in caixas.values() if c[3] < 440), 2, 'dois à frente do elétrico')
        self.assertTrue(all(c[2] < 598 for c in caixas.values() if c[3] < 440), 'à frente do elétrico (a frente está em x 598)')
        for escala in (1, 1.04):
            for x, y in pontos:
                xe = 500 + (x - 500) * escala
                self.assertTrue(meio - meia <= xe <= meio + meia, (x, y, escala))



if __name__ == '__main__':
    unittest.main()
