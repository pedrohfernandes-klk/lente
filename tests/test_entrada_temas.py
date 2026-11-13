"""12/11/2026: pedido entrada-temas. A entrada do Lente abre por quatro temas e o tema 02 tem página própria (informacao/).

O que estes testes fixam, sem navegador (o navegador está em tests/browser_entrada_temas.cjs):
- os quatro temas, pela ordem aprovada, cada um com a sua pergunta, a sua imagem e o seu destino; só o tema 02 tem página nova e os
  outros três abrem a área que já existe; nada na entrada nem na página do tema promete páginas que não existem;
- todas as ligações da entrada e da página do tema resolvem para ficheiros do repositório, e as âncoras para ids que existem;
- nenhum endereço da entrada antiga se perde: cada destino da entrada do main b8abe97 tem ligação na entrada nova ou no mapa;
- nem nota de prévia nem noindex; nenhuma palavra proibida; tratamento por «tu», sem género;
- os créditos das imagens completos e atrás do «i» da casa (assets/info-i.css), com as imagens no repositório;
- a casca da página do tema (aparência, «i», projeção) e os títulos na ordem certa;
- o manifesto fechado da camada (tests/fixtures/entrada-temas-20261112.json) está em vigor e volta atrás sem perdas;
- os fluxos correm estes testes.

13/11/2026: pedido temas-01-03-04. Os temas 01, 03 e 04 passam a ter página própria (justica-e-vida-em-comum/, historias-e-criacao/ e
imagem-som-e-cidade/), no molde da do tema 02, e os cartões da entrada abrem-nas. Tudo o que estes testes fixavam para a página do tema
02 passa a fixar-se para as quatro (ligações, frases com prova na página ligada, regras de texto, créditos, casca, títulos, dobra), e
acrescenta-se: o destino antigo de cada cartão é a primeira ligação de «Ver tudo neste tema» da página nova e continua no mapa; a camada
nova (tests/temas_paginas_20261113.py, manifesto tests/fixtures/temas-paginas-20261113.json) está em vigor e volta atrás sem perdas.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
sys.path.insert(0, str(ROOT / 'tools'))
import entrada_temas_20261112  # noqa: E402
import temas_paginas_20261113  # noqa: E402

SITIO = 'https://pedrohfernandes-klk.github.io/lente/'
BASE = 'b8abe97f65adb6c995579807bb89f9359d7ce869'
# 13/11/2026: pedido temas-01-03-04. O main de que parte a camada das páginas dos temas 01, 03 e 04.
BASE_TEMAS = '9a5e6e14d7361a57e46f47678effd758b99d4bea'
# 13/11/2026: pedido temas-01-03-04. Os cartões 01, 03 e 04 abrem a página do tema (antes abriam olhar-e-decidir/, narrativas/ e cidade/,
# que são agora a primeira ligação de «Ver tudo neste tema» em cada página: ver ANTIGOS e test_nenhum_endereco_da_entrada_antiga_se_perde).
TEMAS = [
    ('01', 'justica-e-vida-em-comum/', 'Justiça e vida em comum', 'Uma regra igual é sempre justa?', 'img/cidadania/daumier-700.webp'),
    ('02', 'informacao/', 'Informação e mundo digital', 'Porque estás a ver isto?', 'img/cidadania/turco-700.webp'),
    ('03', 'historias-e-criacao/', 'Histórias e criação', 'O que transforma uma ideia numa história?', 'assets/laboratorio/van-gogh-quarto-carta.webp'),
    ('04', 'imagem-som-e-cidade/', 'Imagem, som e cidade', 'O que muda quando mudas o enquadramento?', 'img/arquivo/rua-da-boavista-carris-2026-720.webp'),
]
COMMONS = ('<a data-external aria-label="Wikimedia Commons, sítio externo" href="{}">Wikimedia Commons</a>. Domínio público.')
CREDITOS = [
    ('Créditos da imagem: Honoré Daumier', 'Honoré Daumier, <i>Les gens de justice</i>. Gravura. '
     + COMMONS.format('https://commons.wikimedia.org/wiki/File:Honor%C3%A9_Daumier_-_Les_gens_de_justice.jpg')),
    ('Créditos da imagem: Joseph Racknitz', 'O Turco, o autómato de xadrez de Wolfgang von Kempelen, numa gravura de Joseph Racknitz, 1789. '
     + COMMONS.format('https://commons.wikimedia.org/wiki/File:Racknitz_-_The_Turk_3.jpg')),
    ('Créditos da imagem: Vincent van Gogh', 'Vincent van Gogh, esboço de <i>O Quarto</i> enviado ao irmão, Theo, com a carta 705 (Arles, 16 de outubro de 1888). '
     'Pena e tinta sobre papel. Van Gogh Museum, Amesterdão (Vincent van Gogh Foundation). '
     + COMMONS.format('https://commons.wikimedia.org/wiki/File:Vincent_van_Gogh_-_Vincent%27s_Bedroom_in_Arles_-_Letter_Sketch_October_1888.jpg')),
    ('Créditos da fotografia: Rua da Boavista', 'Rua da Boavista, Lisboa. Fotografia: Arquivo da EPI, 2026.'),
]
# 13/11/2026: pedido temas-01-03-04. As páginas dos quatro temas entram em todas as verificações que percorrem PAGINAS.
PAGINAS = ['index.html', 'justica-e-vida-em-comum/index.html', 'informacao/index.html', 'historias-e-criacao/index.html', 'imagem-som-e-cidade/index.html']
# o destino que cada cartão tinha na entrada de 12/11 (o tema 02 já tinha página)
ANTIGOS = {'01': 'olhar-e-decidir/', '03': 'narrativas/', '04': 'cidade/'}
J, M1, M2, LAB = 'olhar-e-decidir/justica/', 'cidadania/m1/', 'cidadania/m2/', 'narrativas/'
# 13/11/2026: o que cada página de tema tem, peça a peça: a imagem (como está escrita), a legenda, os títulos pela ordem, a atividade que
# abre o tema, as quatro alternativas, as ligações de «Para aplicar», a ligação «É para uma aula?» e os grupos de «Ver tudo neste tema».
PECAS = {
    '01': dict(
        img='<img src="../img/cidadania/daumier.webp" srcset="../img/cidadania/daumier-700.webp 700w, ../img/cidadania/daumier.webp 1100w"',
        legenda='Uma gravura de Honoré Daumier: três homens de toga e uma rapariga de pé diante deles.',
        comeca=('Quem fica com o quê?', J + 'aplicar/'),
        alternativas=[(J + 'licao-1/', 'O elétrico não trava: desvias ou segues em frente?'),
                      (M1 + 'cid-m1-o-juri/', 'Quando é que um grupo pode decidir sobre alguém que não está na sala?'),
                      (M1 + 'cid-m1-quem-tem-lugar/', 'Uma proposta é aberta a todos quando nem todos conseguem participar?'),
                      ('cidadania/25-de-abril/', 'Que data funda uma democracia?')],
        aplicar=('Pergunta Humana.', ['cidadania/projeto/', 'etica-grelha/']), aula=(M1, 'Vai a A minha aula: Cidadania, módulo 1'),
        grupos=[('Justiça, com Michael Sandel', 7), ('As lições 4 a 13', 10), ('Casos para decidir', 6), ('Ética', 4), ('Os passos do módulo Humanos', 10),
                ('Criar e mostrar', 1), ('Para consultar', 3)]),
    '02': dict(
        img='<img src="../img/cidadania/turco.webp" srcset="../img/cidadania/turco-700.webp 700w, ../img/cidadania/turco.webp 1100w"',
        legenda='O Turco, numa gravura de 1789: a caixa onde estava alguém.',
        comeca=('A regra do feed', M2 + 'cid-m2-a-regra-do-feed/'),
        alternativas=[(M2 + 'cid-m2-o-rasto-da-afirmacao/', 'Três páginas que repetem a mesma frase são três confirmações?'),
                      ('investigar/passo-08/', 'Quem está por trás desta página?'),
                      (M2 + 'cid-m2-preco-minuto/', 'Se a conta é grátis, quem paga?'),
                      (M2 + 'cid-m2-dentro-da-caixa/', 'Quando a máquina faz, quem responde?')],
        aplicar=('Contra-feed.', ['projetos/contra-feed/', 'cidadania/contra-feed/']), aula=(M2, 'Vai a A minha aula: Cidadania, módulo 2'),
        grupos=[('Casos para decidir', 5), ('Verificar fontes', 3), ('Criar e mostrar', 3), ('Os passos do módulo Algoritmos', 9), ('Para consultar', 3)]),
    '03': dict(
        img='<img src="../assets/laboratorio/van-gogh-quarto-carta.webp" width="900" height="520"',
        legenda='O esboço de <i>O Quarto</i>, numa carta de 1888: o quadro antes do quadro.',
        comeca=('Uma chave na mesa', LAB + 'oficina-ficcao-comecar/'),
        alternativas=[(LAB + 'treinar/tres-em-cinco/', 'Como reconheces uma personagem sem a descrever?'),
                      (LAB + 'corta/cena-que-falta/', 'Que plano liga uma perda a uma devolução?'),
                      (LAB + 'formas/certa-manha/', 'O que muda numa frase quando sabes mais?'),
                      (LAB + 'ideias/', 'As ideias caem do céu?')],
        # o tema 03 não tem conteúdos nos módulos de Cidadania: a linha «É para uma aula?» leva às sessões do Ideias
        aplicar=('Do conto à prancha.', ['projetos/prancha/', LAB + 'proposta-subtexto/']), aula=(LAB + 'ideias/', 'Vai a Ideias: duas sessões publicadas, com guião para imprimir'),
        grupos=[('O Laboratório', 3), ('Ideias', 4), ('Observar', 6), ('Treinar', 4), ('Criar', 9), ('Montar e comparar', 3), ('Criar e mostrar', 1)]),
    '04': dict(
        img='<img src="../img/arquivo/rua-da-boavista-carris-2026.jpg" srcset="../img/arquivo/rua-da-boavista-carris-2026-720.webp 720w, ../img/arquivo/rua-da-boavista-carris-2026.jpg 1600w"',
        legenda='Rua da Boavista: os carris a fugirem para o fundo.',
        comeca=('Enquadrar a Boavista', 'cidade/m17/'),
        alternativas=[('cidade/m18/', 'O que ouves numa rua quando fechas os olhos?'),
                      ('estetica/', 'Porque é que um prédio te parece mais bonito do que os outros?'),
                      (M1 + 'cid-m1-duas-legendas/', 'Quanto da nossa interpretação vem da imagem e quanto vem da legenda?'),
                      ('fachada/', 'O que é que a fachada quer de ti?')],
        aplicar=('A cidade em voz e luz.', ['projetos/cidade/', 'projetos/geometria/']), aula=(M1, 'Vai a A minha aula: Cidadania, módulo 1'),
        grupos=[('Ler a cidade', 1), ('As 14 missões de Ler a cidade', 14), ('Olhar e julgar', 6), ('A escola na cidade', 2), ('Oficinas de imagem, no Laboratório', 7),
                ('Criar e mostrar', 2)]),
}
# palavras que o Lente não usa nos textos para alunos (inteiras, sem contar endereços nem atributos)
PROIBIDAS = re.compile(r'\b(professor(?:a|es|as)?|jog(?:o|os|ar|a|as|amos|am)|fichas?|folhas?|prévia|rascunho|em breve|brevemente|em construção)\b', re.I)
# tratamento com género ou na terceira pessoa (a casa escreve por «tu», sem género)
GENERO = re.compile(r'\b(sozinh[oa]s?|obrigad[oa]s?|bem-vind[oa]s?|pront[oa]s?|convidad[oa]s?|você|vocês|o aluno|a aluna|os alunos)\b', re.I)


def ler(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


class Pagina(HTMLParser):
    """Ligações, ids, imagens e texto à vista de uma página."""

    def __init__(self, fonte):
        super().__init__(convert_charrefs=True)
        self.hrefs, self.ids, self.imgs, self.titulos, self.texto = [], [], [], [], []
        self._fora = 0
        self._titulo = None
        self.feed(fonte)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a' and 'href' in a:
            self.hrefs.append(a['href'])
        if tag == 'img':
            self.imgs.append(a)
        if tag in ('script', 'style'):
            self._fora += 1
        if re.fullmatch(r'h[1-6]', tag):
            self._titulo = [tag, '']

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self._fora -= 1
        if self._titulo and tag == self._titulo[0]:
            self.titulos.append((self._titulo[0], re.sub(r'\s+', ' ', self._titulo[1]).strip()))
            self._titulo = None

    def handle_data(self, data):
        if self._fora:
            return
        self.texto.append(data)
        if self._titulo:
            self._titulo[1] += data


def visivel(fonte):
    """O texto que se lê: sem scripts nem estilos, com o alt das imagens e os rótulos acessíveis."""
    p = Pagina(fonte)
    extra = re.findall(r'(?:alt|aria-label|content|title)="([^"]*)"', fonte)
    return re.sub(r'\s+', ' ', ' '.join(p.texto + extra))


def alvo(rel, href):
    """O ficheiro e a âncora de uma ligação interna; None se a ligação sai do Lente."""
    u = urljoin(SITIO + (rel[:-len('index.html')] if rel.endswith('index.html') else rel), href)
    if not u.startswith(SITIO):
        return None
    partes = urlsplit(u)
    caminho = partes.path[len('/lente/'):]
    f = ROOT / caminho
    if caminho == '' or caminho.endswith('/'):
        f = f / 'index.html'
    return f, partes.fragment


class EntradaEmTemas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entrada = ler('index.html')
        cls.tema = ler('informacao/index.html')
        # 13/11/2026: as quatro páginas de tema, pelo número do tema
        cls.temas = {n: ler(href + 'index.html') for n, href, _, _, _ in TEMAS}
        cls.cartoes = re.findall(r'<li><article class="tm"[^>]*>.*?</article></li>', cls.entrada, re.S)

    def test_quatro_temas_pela_ordem_aprovada(self):
        self.assertEqual(len(self.cartoes), 4)
        self.assertEqual(self.entrada.count('<article class="tm"'), 4)
        for cartao, (n, href, nome, pergunta, imagem) in zip(self.cartoes, TEMAS):
            with self.subTest(tema=n):
                self.assertEqual(re.findall(r'<h3 class="tm-n"><b aria-hidden="true">(\d\d)</b><a href="([^"]+)">([^<]+)</a></h3>', cartao), [(n, href, nome)])
                self.assertEqual(re.findall(r'<p class="tm-q">([^<]+)</p>', cartao), [pergunta])
                self.assertEqual(re.findall(r'<img src="([^"]+)"', cartao), [imagem])
                self.assertEqual(len(re.findall(r'<p class="tm-f">.+?</p>', cartao)), 1)
        # os quatro vêm seguidos, logo depois do cabeçalho e do seu crédito, e antes dos acessos secundários, do Português e do rodapé
        ordem = ['<header class="lente-cab"', '<div class="fundo-acoes lf-credito">', '<section class="tm-temas"', '<h2 class="tm-sec" id="tm-temas-t">Escolhe um tema</h2>',
                 self.cartoes[0], self.cartoes[3], '<section class="tm-mais"', '<h2 class="tm-sec" id="tm-mais-t">Também no Lente</h2>',
                 'id="ferramentas"', 'id="inicio-cidadania"', '>Biblioteca</p>', '>Área do docente</p>', '<aside class="lente-pt lente-pt-linha"', '<footer class="cz-footer">']
        posicoes = [self.entrada.index(x) for x in ordem]
        self.assertEqual(posicoes, sorted(posicoes))
        for x in ordem:
            self.assertEqual(self.entrada.count(x), 1, x[:60])
        # a frase de abertura apresenta os quatro temas
        self.assertIn('<p class="lente-frase">Quatro perguntas. Escolhe uma e começa por aí.</p>', self.entrada)

    # 13/11/2026: pedido temas-01-03-04. Era test_so_o_tema_02_tem_pagina_nova_e_nada_promete_outras: os quatro temas têm agora página
    # nova. A exigência cresce: cada cartão abre uma página que não existia no main b8abe97 e que existe; as páginas de tema são
    # exatamente estas quatro; o destino antigo de cada cartão continua a existir e é a primeira ligação de «Ver tudo neste tema».
    def test_os_quatro_temas_tem_pagina_nova_e_nada_promete_outras(self):
        existentes = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT).decode().splitlines()
        for n, href, _, _, _ in TEMAS:
            f, _ = alvo('index.html', href)
            self.assertTrue(f.is_file(), href)
            self.assertNotIn(f.relative_to(ROOT).as_posix(), existentes, href)
            self.assertRegex(href, r'^[a-z-]+/$')
        for n, antigo in ANTIGOS.items():
            self.assertIn(antigo + 'index.html', existentes)
            self.assertTrue((ROOT / antigo / 'index.html').is_file())
            tudo = self.temas[n][self.temas[n].index('<details class="tm-tudo">'):]
            self.assertEqual(re.search(r'<li><a href="([^"]+)">', tudo)[1], SITIO + antigo, n)
        # não há outras páginas de tema, nem ligações para elas
        self.assertEqual(sorted(p.parent.name for p in ROOT.glob('*/index.html') if 'class="tm-pag"' in p.read_text(encoding='utf-8')),
                         ['historias-e-criacao', 'imagem-som-e-cidade', 'informacao', 'justica-e-vida-em-comum'])
        for rel in PAGINAS:
            texto = visivel(ler(rel))
            for promessa in ('noutro tema', 'outros temas', 'página nova', 'em breve', 'brevemente', 'a caminho', 'por agora', 'ainda não', 'em construção'):
                self.assertNotIn(promessa, texto.lower(), (rel, promessa))
        # na página do tema, «os quatro temas» é a entrada
        for n, t in self.temas.items():
            self.assertEqual(re.findall(r'<a href="\.\./">([^<]+)</a>', t), ['← Lente: os quatro temas', '← Voltar aos quatro temas'], n)
            # 13/11/2026: uma página de tema não liga a outra página de tema (cada uma é um ponto de partida; o regresso é a entrada)
            for _, outra, _, _, _ in TEMAS:
                self.assertNotIn('/lente/' + outra, t)
                self.assertNotIn('../' + outra, t)

    def test_todas_as_ligacoes_resolvem(self):
        vistos = 0
        for rel in PAGINAS + ['mapa/index.html', 'como/index.html']:
            pagina = Pagina(ler(rel))
            for href in pagina.hrefs:
                with self.subTest(pagina=rel, href=href):
                    if href.startswith('#'):
                        self.assertIn(href[1:], pagina.ids)
                        continue
                    a = alvo(rel, href)
                    if a is None:
                        self.assertRegex(href, r'^https://(pedrohfernandes-klk\.github\.io/pt/|commons\.wikimedia\.org/wiki/File:|[a-z0-9.-]+/)')
                        continue
                    f, ancora = a
                    self.assertTrue(f.is_file(), f)
                    # as âncoras conferem-se na entrada, na página do tema e nas ligações que esta camada pôs no mapa (as de
                    # «Ver para fazer», mais antigas, são filtros que a própria página lê)
                    if ancora and (rel in PAGINAS or '/praticar/#' in href or '/narrativas/tudo/#' in href or href.endswith('/lente/#ferramentas')):
                        self.assertIn('id="' + ancora + '"', f.read_text(encoding='utf-8'))
                    vistos += 1
        # 13/11/2026: com as três páginas novas, o mínimo de ligações vistas sobe de 350 para 480
        self.assertGreater(vistos, 480)
        # as ligações da entrada e da página do tema, uma a uma
        # 13/11/2026: a entrada ganha uma ligação (o Laboratório, no cartão do tema 03) e contam-se as ligações das quatro páginas de tema
        # (migas, crédito com ligação à fonte, botão, quatro alternativas, duas de «Para aplicar», aula, «Ver tudo» e duas do rodapé)
        self.assertEqual(len(Pagina(self.entrada).hrefs), 4 + 3 + 1 + 1 + 5 + 2 + 2 + 1 + 3 + 2)
        self.assertEqual(len(Pagina(self.tema).hrefs), 1 + 1 + 1 + 4 + 2 + 1 + 23 + 2)
        for n, credito, tudo in (('01', 1, 41), ('02', 1, 23), ('03', 1, 30), ('04', 0, 32)):
            self.assertEqual(len(Pagina(self.temas[n]).hrefs), 1 + credito + 1 + 4 + 2 + 1 + tudo + 2, n)
            self.assertEqual(sum(q for _, q in PECAS[n]['grupos']), tudo, n)
        # imagens e folhas da página do tema e da entrada existem
        for rel in PAGINAS:
            fonte = ler(rel)
            for src in re.findall(r'<(?:img|script)\b[^>]*\bsrc="([^"]+)"', fonte) + re.findall(r'<link rel="stylesheet" href="([^"]+)"', fonte):
                if src.startswith('https://fonts.'):
                    continue
                f, _ = alvo(rel, src.split('?')[0])
                self.assertTrue(f.is_file(), (rel, src))

    def test_nenhum_endereco_da_entrada_antiga_se_perde(self):
        antiga = subprocess.check_output(['git', 'show', BASE + ':index.html'], cwd=ROOT).decode('utf-8')
        absolutas = lambda fonte, rel: {urljoin(SITIO + rel, h) for h in Pagina(fonte).hrefs}  # noqa: E731
        antes, agora, mapa = absolutas(antiga, ''), absolutas(self.entrada, ''), absolutas(ler('mapa/index.html'), 'mapa/')
        # só saem os créditos das três imagens que saíram da entrada e os três saltos internos da navegação móvel (os ids ficam)
        sairam = {'https://commons.wikimedia.org/wiki/File:An_Experiment_on_a_Bird_in_an_Air_Pump_by_Joseph_Wright_of_Derby,_1768.jpg',
                  'https://commons.wikimedia.org/wiki/File:PessoaChapeu.jpg', 'https://www.loc.gov/item/2021640928/',
                  SITIO + '#inicio-cidadania', SITIO + '#inicio-narrativas'}
        self.assertEqual(antes - agora - mapa, sairam)
        # 13/11/2026: pedido temas-01-03-04. Os Dilemas e «Ler a cidade» deixam de ser destino de um cartão: saem da entrada para o
        # mapa (onde já estavam) e para a primeira ligação de «Ver tudo neste tema» das páginas dos temas 01 e 04. O Laboratório
        # continua na entrada, à vista, no cartão do tema 03.
        self.assertIn(SITIO + 'narrativas/', agora)
        for n, antigo in ANTIGOS.items():
            self.assertIn(SITIO + antigo, mapa, antigo)
            self.assertIn(SITIO + antigo, absolutas(self.temas[n], TEMAS[int(n) - 1][1]), antigo)
        self.assertEqual(self.entrada.count('<p class="tm-extra"><a href="' + SITIO + 'narrativas/">Laboratório</a></p><p class="tm-extra"><a href="narrativas/ideias/">Ideias: o método em cinco passos</a></p><span class="tm-seta" aria-hidden="true">→</span></div></article>'), 1)
        self.assertEqual(antes - agora - sairam, {
            SITIO + 'olhar-e-decidir/', SITIO + 'cidade/',
            SITIO + '#ferramentas', SITIO + 'cidadania/', SITIO + 'ver-para-fazer/',
            SITIO + 'narrativas/tudo/#ler-como-quem-escreve', SITIO + 'narrativas/tudo/#treinar', SITIO + 'narrativas/tudo/#criar',
            SITIO + 'praticar/#compreender', SITIO + 'praticar/#investigar', SITIO + 'praticar/#criar', SITIO + 'praticar/#apresentar', SITIO + 'praticar/#aplicar'})
        for imagem in ('wright-experiencia', 'tejo-1907', 'pessoa-1914'):
            self.assertNotIn(imagem, self.entrada)
        # os ids para onde outras páginas (ou endereços guardados) apontam continuam na entrada, uma vez cada
        for i in ('ferramentas', 'inicio-cidadania', 'inicio-narrativas', 'inicio-vozes'):
            self.assertEqual(self.entrada.count('id="' + i + '"'), 1, i)
        ids = Pagina(self.entrada).ids
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ler('mapa/index.html').count(SITIO + '#ferramentas'), 4)
        # nenhum ficheiro do main foi apagado nem mudou de sítio
        apagados = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT).decode().splitlines()
        self.assertEqual([f for f in apagados if not (ROOT / f).exists()], [])
        # a página do tema está no mapa, fora da secção que tools/laboratorio.py reescreve, e a ajuda descreve a entrada nova
        mapa = ler('mapa/index.html')
        self.assertEqual(mapa.count('<p><a href="../informacao/">Informação e mundo digital, um dos quatro temas da entrada →</a></p>'), 1)
        self.assertLess(mapa.index('href="../informacao/"'), mapa.index('<section class="map-section">'))
        # 13/11/2026: as quatro páginas de tema estão no mapa, seguidas e pela ordem dos temas, no mesmo lugar
        linhas = ''.join('<p><a href="../' + href + '">' + nome + ', um dos quatro temas da entrada →</a></p>' for _, href, nome, _, _ in TEMAS)
        self.assertEqual(mapa.count(linhas), 1)
        self.assertEqual(mapa.count('um dos quatro temas da entrada'), 4)
        self.assertLess(mapa.index(linhas) + len(linhas), mapa.index('<section class="map-section">'))
        # 12/11/2026: revisão. A alínea acaba aí: a entrada, a página do tema e praticar/ não marcam progresso, por isso a frase
        # «Cada índice marca o que já fizeste.» saiu (a alínea seguinte já diz que o progresso guardado depende do recurso).
        self.assertIn('<li>Começa por escolher um dos quatro temas na <a href="../">entrada do Lente</a>, ou por <a href="../praticar/">escolher o que precisas de praticar</a>.</li>', ler('como/index.html'))
        self.assertNotIn('Cada índice marca', ler('como/index.html'))
        self.assertNotIn('duas divisões', self.entrada + ler('como/index.html'))

    def test_sem_nota_de_previa_nem_noindex(self):
        for rel in PAGINAS:
            fonte = ler(rel)
            for marca in ('noindex', 'nofollow', 'class="previa"', 'Prévia', 'prévia', 'para o docente.', 'tema-informacao'):
                self.assertNotIn(marca, fonte, (rel, marca))
            self.assertNotRegex(fonte, r'<meta name="robots"')
        self.assertIn('<title>Lente · EPI 2026/2027</title>', self.entrada)
        self.assertIn('<title>Informação e mundo digital · Lente</title>', self.tema)
        # 13/11/2026: o título de cada página de tema é o nome do tema, e a descrição apresenta-o como um dos quatro
        for n, _, nome, _, _ in TEMAS:
            self.assertIn('<title>' + nome + ' · Lente</title><meta name="description" content="' + nome + ', um dos quatro temas do Lente: ', self.temas[n])

    def test_regras_de_texto(self):
        for rel in PAGINAS:
            fonte = ler(rel)
            texto = visivel(fonte)
            with self.subTest(pagina=rel):
                self.assertIsNone(PROIBIDAS.search(texto), PROIBIDAS.search(texto))
                self.assertIsNone(GENERO.search(texto), GENERO.search(texto))
                # nem ponto de meio nem travessão dentro de frases: só o ponto de meio do <title>, como em todas as páginas do Lente
                corpo = visivel(fonte[fonte.index('<body'):])
                self.assertNotIn('·', corpo)
                self.assertNotIn('—', texto)
                self.assertNotIn('–', texto)
                self.assertEqual(texto.count('·'), 1)
                # «Que + nome» ou «Qual das…», nunca «Qual + nome»
                self.assertEqual(re.findall(r'\bQua(?:l|is)\s+(?!d[aeo]s?\b|é\b|foi\b)\w+', texto), [])
                # aspas da casa
                self.assertNotRegex(corpo, r'[“”"]')
                # o nome do docente não aparece (nem iniciais): a única palavra «docente» é a da área do docente
                self.assertNotRegex(texto, r'\b[A-Z]\. ?[A-Z]\.(?! White)')
        # perguntas dos temas e das alternativas: acabam em ponto de interrogação
        # 13/11/2026: as perguntas das quatro páginas de tema (quatro alternativas cada), com as quatro da entrada: de 8 para 20
        perguntas = re.findall(r'<p class="tm-q">([^<]+)</p>', self.entrada) + [p for t in self.temas.values() for p in re.findall(r'<h2><a href="[^"]+">([^<]+)</a></h2>', t)]
        self.assertEqual(len(perguntas), 20)
        self.assertEqual(len(set(perguntas)), 20)
        for p in perguntas:
            self.assertTrue(p.endswith('?'), p)
        # títulos de obras em itálico nos créditos
        self.assertIn('<i>Les gens de justice</i>', self.entrada)
        self.assertIn('<i>O Quarto</i>', self.entrada)
        self.assertIn('<i>Ensaio sobre a Cegueira</i>', self.entrada)
        # 13/11/2026: e nas páginas dos temas (créditos, legenda e frases); o poema de Cesário vai entre aspas da casa, como na origem
        self.assertIn('<i>Les gens de justice</i>', self.temas['01'])
        self.assertIn('do curso <i>Justice</i>, em Harvard', self.temas['01'])
        self.assertEqual(self.temas['03'].count('<i>O Quarto</i>'), 2)
        self.assertIn('com <i>Mr e Mrs Andrews</i>, de Thomas Gainsborough', self.temas['04'])
        self.assertIn('a partir de «O Sentimento dum Ocidental», de Cesário Verde', self.temas['04'])
        # 13/11/2026: «docente» não aparece nas páginas dos temas (nem o nome, nem a área)
        for n, t in self.temas.items():
            self.assertNotRegex(visivel(t).lower(), r'docente|\bstor\b', n)
        # o trabalho é individual: nada pede grupos
        for rel in PAGINAS:
            self.assertNotRegex(visivel(ler(rel)).lower(), r'\b(em grupo|grupos de|em pares|a pares)\b')

    def test_frases_correspondem_as_paginas_ligadas(self):
        """Cada frase sobre um conteúdo diz o que a página ligada tem (as passagens de origem ficam aqui escritas)."""
        provas = [
            ('index.html', 'Vês Michael Sandel a ensinar, decides antes de ouvires a sala e pões uma regra à prova num caso.',
             'olhar-e-decidir/index.html', ['Justiça, com Michael Sandel', 'uma decisão antes de ouvires a sala e um dilema para aplicar']),
            ('index.html', 'Juntas material, treinas uma regra de cada vez e crias uma peça tua.',
             'narrativas/index.html', ['Junta material', 'Uma regra de cada vez', 'cria uma peça tua']),
            ('index.html', 'Lês uma rua como um texto, escolhes uma das 14 missões e explicas o que ficou fora da fotografia.',
             'cidade/index.html', ['Uma rua pode ser lida como um texto', 'As 14 missões são escolhas livres', 'explica o que ficou fora dela']),
            ('index.html', 'Os textos de que partem os exercícios, com a fonte junto do texto.',
             'biblioteca/index.html', ['Lê os textos de que partem os exercícios', 'encontras a fonte junto do texto']),
            ('index.html', 'Guiões, resultados da turma e arquivo.', 'docente/index.html', ['Guiões', 'Resultados da turma', 'Arquivo']),
            ('informacao/index.html', 'Uma plataforma inventada testa três conteúdos: um sketch, uma leitura de poesia e um debate.',
             'cidadania/m2/cid-m2-a-regra-do-feed/index.html', ['Uma plataforma cultural fictícia testa três conteúdos', 'um sketch', 'uma leitura de poesia', 'Abre as três perspetivas',
                                                                 'Justifica as escolhas oralmente; o exercício digital não pede texto escrito']),
            ('informacao/index.html', 'Três páginas que repetem a mesma frase são três confirmações?',
             'cidadania/m2/cid-m2-o-rasto-da-afirmacao/index.html', ['Três páginas que repetem a mesma frase são três confirmações?', 'a biblioteca do bairro vai fechar', 'o exercício digital não pede texto escrito']),
            ('informacao/index.html', 'Verificação lateral, em Como se investiga. 6 min.',
             'investigar/passo-08/index.html', ['Verificação lateral · Como se investiga', '6 min', 'Abrir outro separador']),
            ('informacao/index.html', 'A direção propõe que a turma gira uma conta da escola numa plataforma de vídeos curtos.',
             'cidadania/m2/cid-m2-preco-minuto/index.html', ['a direção propõe que a turma gira uma conta da escola numa plataforma de vídeos curtos', 'quatro rastos: o dinheiro, a atenção, a energia e o lixo',
                                                             'cerca de 25 min', 'Se a conta é grátis, quem paga']),
            ('informacao/index.html', 'Um cartaz junta uma fotografia alterada e um texto gerado por um assistente.',
             'cidadania/m2/cid-m2-dentro-da-caixa/index.html', ['Quando a máquina faz, quem responde?', 'cerca de 25 min', 'decides quem responde pelo cartaz', 'Em 1770, Kempelen apresentou um autómato de xadrez',
                                                                'O Turco, numa gravura de 1789: a caixa onde estava alguém.']),
            ('informacao/index.html', 'Uma performance ou vídeo-performance, feita por ti, que torna visível a regra de um algoritmo. Acompanha-a um manifesto de uso, curto e assinado.',
             'cidadania/contra-feed/index.html', ['uma performance ou vídeo-performance', 'Acompanha-a um manifesto de uso escrito por ti, curto, assinado']),
            ('informacao/index.html', 'Ler a apresentação do Contra-feed, 4 min', 'projetos/contra-feed/index.html', ['4 min de leitura']),
            ('informacao/index.html', 'Contra-feed: do conceito ao guião', 'cidadania/m2/passo-06/index.html', ['Do conceito ao guião da performance']),
        ]
        # 13/11/2026: pedido temas-01-03-04. As frases das três páginas novas, com as passagens da página ligada que as sustentam.
        T1, T3, T4 = 'justica-e-vida-em-comum/index.html', 'historias-e-criacao/index.html', 'imagem-som-e-cidade/index.html'
        provas += [
            (T1, 'A escola pode emprestar uma câmara em seis sessões de uma hora. Três projetos pedem quatro sessões cada. Escolhes uma regra de distribuição, testa-la sem saberes qual é o teu projeto e respondes a uma objeção. Podes mudar de ideias.',
             J + 'aplicar/index.html', ['A escola pode emprestar uma câmara em seis sessões de uma hora. Três projetos pedem quatro sessões cada.', 'O mesmo tempo para todos',
                                                                            'E se não soubesses qual era o teu projeto?', 'Escolhe uma objeção à regra que mais te convenceu', 'Podes mudar de ideias.']),
            (T1, 'Um caso para decidir. 6 a 8 minutos, sem escrever no ecrã.', J + 'aplicar/index.html', ['6 a 8 minutos. Sem escrever no ecrã.', 'Quem fica com o quê?']),
            (T1, 'Vês Michael Sandel a ensinar em dez excertos curtos do primeiro episódio do curso Justice, em Harvard. Antes de cada um sabes o que observar; depois, decides.',
             J + 'licao-1/index.html', ['Episódio 1 do curso «Justice», em Harvard', 'Vais vê-lo a ensinar em dez excertos curtos. Antes de cada um, sabes o que observar; depois, decides.',
                                        'Um elétrico sem travões', 'desvias o elétrico ou segues em frente?']),
            (T1, 'O elétrico, lição 1 de Justiça. Excertos em inglês.', J + 'licao-1/index.html', ['Lição 1: O elétrico', 'e estão em inglês']),
            (T1, 'Um vídeo circula e nove de onze colegas querem afastar outro da mostra final. Ele não está na reunião. Separas o que se sabe do que se supõe, recebes uma ordem e uma objeção, e só no fim decides.',
             M1 + 'cid-m1-o-juri/index.html', ['Quando é que um grupo pode decidir sobre alguém que não está na sala?', 'Um vídeo circula', 'não está na reunião', 'continua na mostra final',
                                               'São onze pessoas. Nove querem que fique de fora já hoje.', 'separar o que se sabe do que se supõe, receber uma ordem e uma objeção, e só no fim decidir']),
            (T1, 'O júri. Cerca de 22 min, sem escrita.', M1 + 'cid-m1-o-juri/index.html', ['cerca de 22 min', 'Não há nada para escrever.']),
            (T1, 'Uma equipa prepara uma mostra num piso superior, sem elevador. Uma participante usa cadeira de rodas; outra precisa de acompanhar o debate por texto. Escolhes, recebes informação nova, abres três perspetivas e podes rever a decisão.',
             M1 + 'cid-m1-quem-tem-lugar/index.html', ['Uma proposta é aberta a todos quando nem todos conseguem participar?', 'Uma equipa prepara uma mostra num piso superior, sem elevador.',
                                                       'Uma participante usa cadeira de rodas; outra precisa de acompanhar o debate por texto.', 'conhecer informação nova e rever a decisão', 'Abre as três perspetivas']),
            (T1, 'Quem tem lugar? Um caso para decidir, sem escrita.', M1 + 'cid-m1-quem-tem-lugar/index.html', ['Justifica as escolhas oralmente; o exercício digital não pede texto escrito']),
            (T1, 'Às 22h55 de 24 de abril de 1974, uma canção na rádio mandou os quartéis preparar a saída. Ouves os documentos e distingues o que aconteceu de quem lhe dá sentido.',
             'cidadania/25-de-abril/index.html', ['Que data funda uma democracia?', 'Às 22h55 de 24 de abril de 1974, uma canção na rádio mandou os quartéis preparar a saída.',
                                                  'Ouve os documentos. Distingue o que aconteceu de quem lhe dá sentido.']),
            (T1, 'O 25 de Abril de 1974 em seis ângulos.', 'cidadania/25-de-abril/index.html', [('fonte', '<meta name="description" content="O 25 de Abril de 1974 em seis ângulos:')]),
            (T1, 'Escolhes uma pergunta sobre o que é ser humano, investiga-la a sério e transformas o que encontraste num teatro-documento de 5 a 8 minutos, apresentado em público. É um projeto individual.',
             'cidadania/projeto/index.html', ['Cada aluno escolhe uma pergunta sobre o que é ser humano, investiga-a a sério e transforma o que encontrou num teatro-documento de 5 a 8 minutos, apresentado em público.',
                                              'Projeto do Módulo 1, individual: um teatro-documento', 'Pergunta Humana']),
            (T1, 'Imprimir um caso, três perguntas, uma decisão', 'etica-grelha/index.html', ['Ética: um caso, três perguntas, uma decisão', 'Imprimir']),
            (T1, 'Lição 1: A criança e a distância, com Peter Singer', 'olhar-e-decidir/etica/licao-1/index.html', ['Peter Singer']),
            (T1, 'Vai a A minha aula: Cidadania, módulo 1', M1 + 'index.html', ['Justiça e Direitos', 'decidir e justificar']),
            (T3, 'Uma chave na mesa. Alguém a leva. Mudas a ação, alteras a ordem da informação, experimentas o ritmo e comparas a versão final com a inicial.',
             LAB + 'oficina-ficcao-comecar/index.html', ['Uma chave na mesa. Alguém a leva.', 'Muda a ação.', 'Altera a ordem da informação.', 'Experimenta o ritmo e compara a versão final com a inicial.']),
            (T3, 'Escrever ficção: o começo. 5 a 8 min, sem escrever.', LAB + 'oficina-ficcao-comecar/index.html', ['Oficina · 5 a 8 min · sem escrever', 'Escrever ficção: o começo']),
            (T3, 'Inventas três personagens: nome, idade, ofício, um medo, um desejo e uma contradição para cada uma. Se quiseres, com o relógio de cinco minutos.',
             LAB + 'treinar/tres-em-cinco/index.html', ['Inventa três personagens: nome, idade, ofício, um medo, um desejo e uma contradição para cada uma. Se quiseres, com o relógio de cinco minutos.']),
            (T3, 'Três em cinco minutos, em Treinar. 5 min de escrita.', LAB + 'treinar/tres-em-cinco/index.html', ['Treino · Dar uma voz à personagem · 5 min de escrita']),
            (T3, 'Como reconheces uma personagem sem a descrever?', LAB + 'percursos/index.html', ['Dar uma voz à personagemComo reconheces uma personagem sem a descrever?']),
            (T3, 'Uma carteira perdida, uma carteira devolvida. Entre as duas falta um plano: escolhes um e vês que hipóteses aguentam.',
             LAB + 'corta/cena-que-falta/index.html', [('fonte', '<meta name="description" content="Uma carteira perdida, uma carteira devolvida. Entre as duas, falta um plano: escolhe-o e vê que hipóteses aguentam.">'), 'A cena que falta | Criar']),
            (T3, 'Uma frase de Kafka, lida três vezes: onde muda de mundo, o que te deixa dizer e o que muda quando sabes mais.',
             LAB + 'formas/certa-manha/index.html', [('fonte', '<meta name="description" content="Uma frase de Kafka, lida três vezes: onde muda de mundo, o que te deixa dizer e o que muda quando sabes mais.">'), 'Certa manhã | Observar']),
            (T3, 'Segues, passo a passo, o método de James Webb Young. Nas duas sessões publicadas, começas por juntar material e observar melhor.',
             LAB + 'ideias/index.html', ['O método em cinco passos', 'Seguimos, passo a passo, o método de James Webb Young', 'Nas duas sessões publicadas, começas por juntar material e observar melhor.']),
            (T3, 'As ideias caem do céu?', LAB + 'ideias/sessao-01/index.html', ['As ideias caem do céu?']),
            (T3, 'Vai a Ideias: duas sessões publicadas, com guião para imprimir', LAB + 'ideias/guiao/index.html', ['Para imprimir em A4: frente e verso de cada sessão pronta']),
            (T3, 'Um conto curto em domínio público, transposto por ti para oito a doze pranchas de banda desenhada ou para um animatic de um minuto. O trabalho é escolher o que se corta.',
             'projetos/prancha/index.html', ['Individualmente, um conto curto em domínio público transposto para oito a doze pranchas de banda desenhada, ou para um animatic de um minuto',
                                             'O trabalho é escolher o que se corta']),
            (T3, 'Ler a apresentação de Do conto à prancha, 5 min', 'projetos/prancha/index.html', ['5 min de leitura']),
            (T3, 'Escrever uma cena tua, de dois minutos: Uma cena com subtexto', LAB + 'proposta-subtexto/index.html', ['Aqui: uma cena tua, de dois minutos.', 'Escreve uma cena curta entre duas personagens']),
            (T3, 'Em outubro de 1888, Van Gogh desenhou o seu quarto numa carta ao irmão. Um esboço também é uma maneira de pensar uma obra.',
             'assets/laboratorio/imagens.json', ['um esboço também é uma maneira de pensar uma obra']),
            (T3, 'Observar: como os outros fizeram', LAB + 'index.html', ['ObservarComo os outros fizeram.', 'TreinarUma regra de cada vez.', 'CriarUma peça, com palavras e imagens.']),
            (T3, 'Percursos: os 10 percursos do Laboratório, por porta', LAB + 'percursos/index.html', ['Os 10 percursos do Laboratório, por porta.']),
            (T3, 'Tudo o que há no Laboratório', LAB + 'tudo/index.html', ['Tudo o que há no Laboratório']),
            (T4, 'A Rua da Boavista fica a dois passos da escola. Quem a olha de dentro, para o fundo, vê um caminho. Quem se põe de frente para três prédios de azulejo vê uma parede com ritmo. É a mesma rua.',
             'cidade/m17/index.html', ['a dois passos da escola', 'de dentro da rua, a olhar para o fundo', 'a rua é um caminho', 'Quem se põe de frente para três prédios de azulejo', 'a rua é uma parede com ritmo', 'É a mesma rua']),
            (T4, 'Olhas a Rua da Boavista antes de levantar o telemóvel: o ponto de vista, as linhas, o ritmo, a luz e o corte. Depois decides qual das três imagens, todas boas, abre um vídeo curto sobre o bairro.',
             'cidade/m17/index.html', ['olhas a rua antes de levantar o telemóvel: ponto de vista, linhas, ritmo, luz e o corte', 'Três imagens boas, uma certa', 'abrir um vídeo curto sobre o bairro']),
            (T4, 'Uma missão de Ler a cidade. 7 min. No fim, desenhas três retângulos no caderno.', 'cidade/m17/index.html', ['Rua da Boavista · 7 min', 'Desenha no caderno três retângulos pequenos, como três enquadramentos da Rua da Boavista']),
            (T4, 'Rua da Boavista: os carris a fugirem para o fundo.', 'cidade/m17/index.html', ['a fugirem para o fundo', 'Fotografia: Arquivo da EPI, 2026.', ('fonte', 'rua-da-boavista-carris-2026.jpg')]),
            (T4, 'Na Rua de São Paulo, fechas os olhos um minuto e escutas antes de gravar: o que está perto e o que está ao fundo, o que não para e o que acontece, de onde vem cada som.',
             'cidade/m18/index.html', ['Estás na Rua de São Paulo', 'fechas os olhos um minuto e escutas antes de gravar: o que está perto e o que está ao fundo, o que não para e o que acontece, de onde vem cada som']),
            (T4, 'Um minuto de olhos fechados, em Ler a cidade. 7 min.', 'cidade/m18/index.html', ['Rua de São Paulo · 7 min']),
            (T4, 'Três prédios de azulejo lado a lado, na Rua da Boavista. Lês sobre o gosto e o juízo, sobre o que a forma faz aos olhos e sobre cinco passos para olhar devagar antes de julgar.',
             'estetica/index.html', ['Rua da Boavista, a dois passos da escola: três prédios de azulejo lado a lado', 'Porque é que um te parece mais bonito do que os outros?',
                                     'o que é o gosto, o que é um juízo, o que a forma faz aos olhos, e como se olha devagar antes de julgar', 'Olhar devagar, em cinco passos']),
            (T4, 'Estética. Cerca de 25 min de leitura, sem escrita.', 'estetica/index.html', ['cerca de 25 min de leitura · sem escrita']),
            (T4, 'Uma equipa prepara uma pequena exposição com Mr e Mrs Andrews, de Thomas Gainsborough, e compara duas legendas. Escolhes, conheces informação nova e reves a decisão.',
             M1 + 'cid-m1-duas-legendas/index.html', ['Quanto da nossa interpretação vem da imagem e quanto vem da legenda?', 'Uma equipa prepara uma pequena exposição com Mr e Mrs Andrews, de Thomas Gainsborough',
                                                      'A equipa compara duas legendas', 'Um caso para observar, escolher, conhecer informação nova e rever a decisão.']),
            (T4, 'Duas legendas, o mesmo quadro. Um caso para decidir, sem escrita.', M1 + 'cid-m1-duas-legendas/index.html', ['Justifica as escolhas oralmente; o exercício digital não pede texto escrito']),
            (T4, 'Acima do portão da escola há um texto escrito à mão. Lês devagar, em inglês e em português, dezanove imperativos e uma afirmação.',
             'fachada/index.html', ['O que é que a fachada quer de ti?', 'Acima do portão da escola, na Rua D. Luís I, há um texto escrito à mão.', 'Vais lê-lo devagar, em inglês e em português',
                                    'Dezanove imperativos e uma afirmação, acima do portão.']),
            (T4, 'A fachada. Cerca de 15 min, sem escrita.', 'fachada/index.html', ['cerca de 15 min · sem escrita']),
            (T4, 'Uma instalação de som e luz, feita por ti, a partir de «O Sentimento dum Ocidental», de Cesário Verde. A voz é a figura; a cidade gravada hoje, à porta da escola, é o fundo.',
             'projetos/cidade/index.html', ['Uma instalação de som e luz a partir de Cesário Verde', 'Individualmente, uma instalação num estúdio ou numa sala escura: «O Sentimento dum Ocidental», de Cesário Verde (1880)',
                                            'A voz é a figura; a cidade gravada hoje, à porta da escola, é o fundo.']),
            (T4, 'Ler a apresentação de A cidade em voz e luz, 5 min', 'projetos/cidade/index.html', ['5 min de leitura']),
            (T4, 'Preferes filmar? Ler a apresentação de A geometria do olhar, 5 min', 'projetos/geometria/index.html', ['5 min de leitura', 'Individualmente, uma curta de dois a três minutos']),
            (T4, 'As 14 missões de Ler a cidade', 'cidade/index.html', ['As 14 missões são escolhas livres']),
            (T4, 'Vai a A minha aula: Cidadania, módulo 1', M1 + 'passo-00/index.html', ['Modos de ver · Cidadania · Humanos']),
            (T4, 'Duas legendas, o mesmo quadro', M1 + 'cid-m1-duas-legendas/index.html', ['Duas legendas, o mesmo quadro · Cidadania · Humanos']),
        ]
        for pagina, frase, origem, passagens in provas:
            with self.subTest(frase=frase[:50]):
                self.assertIn(frase, re.sub(r'<[^>]+>', '', ler(pagina)))
                fonte = re.sub(r'<[^>]+>', '', ler(origem).replace('\\u003c', '<').replace('\\"', '"').replace('\\/', '/'))
                fonte = re.sub(r'\s+', ' ', fonte.replace('&nbsp;', ' '))
                for passagem in passagens:
                    # 13/11/2026: uma passagem escrita como ('fonte', texto) procura-se no ficheiro tal como está (a descrição da página
                    # e os endereços das imagens não ficam no texto corrido); as outras, como antes, no texto sem marcas.
                    if isinstance(passagem, tuple):
                        self.assertEqual(passagem[0], 'fonte')
                        self.assertIn(passagem[1], ler(origem), (origem, passagem))
                        continue
                    self.assertIn(passagem, fonte, (origem, passagem))
        # os rótulos de «Ver tudo neste tema» são os títulos das páginas (com um acrescento onde dois títulos são iguais)
        # 13/11/2026: pedido temas-01-03-04. O mesmo nas quatro páginas. O título acaba no primeiro separador da página ligada: « · »,
        # como antes, e também « | » (Laboratório) e « / » (25 de Abril); a exigência é a mesma, o rótulo começa pelo título. Conta-se
        # ainda que todas as ligações de «Ver tudo» passam por aqui e que nenhuma se repete dentro da mesma página.
        conferidos = 0
        for n, t in self.temas.items():
            pares = re.findall(r'<li><a href="' + re.escape(SITIO) + r'([^"]+)">([^<]+)</a></li>', t[t.index('<details class="tm-tudo">'):t.index('<footer')])
            self.assertEqual(len(pares), sum(q for _, q in PECAS[n]['grupos']), n)
            self.assertEqual(len({h for h, _ in pares}), len(pares), n)
            self.assertEqual(len({r for _, r in pares}), len(pares), n)
            for href, rotulo in pares:
                titulo = re.split(r' (?:·|\||/) ', re.search(r'<title>([^<]+)</title>', ler(href + 'index.html'))[1])[0]
                with self.subTest(href=href):
                    self.assertTrue(rotulo.startswith(titulo.rstrip('?')) or rotulo.startswith(titulo), (rotulo, titulo))
                    self.assertNotRegex(ler(href + 'index.html'), r'noindex|http-equiv="refresh"')
                    conferidos += 1
        self.assertEqual(conferidos, 41 + 23 + 30 + 32)
        # 13/11/2026: a atividade que abre o tema e as alternativas também estão em «Ver tudo neste tema» da mesma página
        for n, t in self.temas.items():
            tudo = t[t.index('<details class="tm-tudo">'):]
            for href in [PECAS[n]['comeca'][1]] + [h for h, _ in PECAS[n]['alternativas']]:
                self.assertIn('<li><a href="' + SITIO + href + '">', tudo, (n, href))

    def test_creditos_completos_atras_do_i(self):
        # entrada: o «i» do grafismo do cabeçalho (gerado com recurso a IA) e um por tema, na moldura da imagem e fora de ligações
        peca = '<details class="info-i" name="info-i"><summary aria-label="{}"><span aria-hidden="true">i</span></summary><p class="info-i-texto">{}</p></details>'
        self.assertEqual(self.entrada.count('<details class="info-i'), 5)
        self.assertIn('<p class="info-i-texto">Grafismo gerado com recurso a IA, EPI, 2026. Na página, a epígrafe de <i>Ensaio sobre a Cegueira</i>, de José Saramago (1995): '
                      '«Se podes olhar, vê. Se podes ver, repara.»</p>', self.entrada)
        for cartao, (rotulo, credito), (_, _, _, _, imagem) in zip(self.cartoes, CREDITOS, TEMAS):
            with self.subTest(imagem=imagem):
                self.assertEqual(cartao.count('<details'), 1)
                self.assertIn('<div class="tm-img com-i"><img src="' + imagem + '"', cartao)
                self.assertIn('decoding="async" style="object-position:', cartao)
                self.assertIn('">' + peca.format(rotulo, credito) + '</div><div class="tm-corpo">', cartao)
                self.assertRegex(cartao, r'<img src="[^"]+" alt="[^"]{40,}" width="\d+" height="\d+"')
                self.assertTrue((ROOT / imagem).is_file())
                # licença dita por extenso: domínio público, ou fotografia do arquivo da escola
                self.assertRegex(credito, r'(Domínio público\.|Fotografia: Arquivo da EPI, 2026\.)$')
        # 12/11/2026: revisão. O crédito do tema 01 fica pelo que o registo do Wikimedia Commons dá (título e técnica), sem «do conjunto»;
        # o texto alternativo descreve a gravura como ela é (só um dos três homens se debruça); e a nota do rodapé conta também a
        # fotografia do arquivo da escola, que não é domínio público nem Creative Commons.
        self.assertNotIn('do conjunto', self.entrada)
        self.assertIn('alt="Gravura: uma rapariga de pé diante de uma bancada alta com três homens de toga; um deles debruça-se a olhar para ela."', self.cartoes[0])
        self.assertEqual(self.entrada.count('Imagens em domínio público, Creative Commons ou do arquivo da EPI, com crédito; dos textos protegidos, só excertos curtos, com crédito e ligação.'), 1)
        self.assertNotIn('Imagens em domínio público ou Creative Commons', self.entrada)
        # página do tema: uma imagem, com o crédito no «i» da moldura e a legenda sem marcas de crédito
        self.assertEqual(self.tema.count('<details class="info-i'), 1)
        self.assertEqual(self.tema.count('<img '), 1)
        # 13/11/2026: pedido temas-01-03-04. O mesmo nas quatro páginas: a imagem é a do cartão da entrada (o mesmo texto alternativo e
        # o mesmo crédito, letra a letra), uma só, com o crédito no «i» da moldura e a legenda sem marcas de crédito.
        for (n, _, _, _, imagem), (rotulo, credito), cartao in zip(TEMAS, CREDITOS, self.cartoes):
            t = self.temas[n]
            with self.subTest(tema=n):
                self.assertEqual(t.count('<details class="info-i'), 1)
                self.assertEqual(t.count('<img '), 1)
                self.assertIn('<figure class="fig tm-fig"><div class="com-i">' + PECAS[n]['img'], t)
                self.assertIn(peca.format(rotulo, credito) + '</div><figcaption>' + PECAS[n]['legenda'] + '</figcaption></figure>', t)
                self.assertNotRegex(PECAS[n]['legenda'], r'Wikimedia|Domínio público|Arquivo da EPI|Fotografia:')
                alt = re.search(r'<img src="[^"]+" alt="([^"]+)"', cartao)[1]
                # (na página do tema 02, de 12/11, o texto alternativo descreve a gravura grande com mais pormenor)
                self.assertIn(' alt="' + (alt if n != '02' else 'Gravura: um autómato de turbante e casaco de peles sobre um armário aberto; lá dentro, entre engrenagens, um homem sentado diante de um tabuleiro de xadrez, à luz de duas velas.') + '" decoding="async"', t)
                # a imagem do cartão é a mesma obra (o mesmo ficheiro, ou o seu tamanho maior)
                self.assertIn('../' + re.sub(r'-7[02]0\.webp$', '', imagem).replace('.webp', ''), t)
        self.assertIn('<figure class="fig tm-fig"><div class="com-i"><img src="../img/cidadania/turco.webp" srcset="../img/cidadania/turco-700.webp 700w, ../img/cidadania/turco.webp 1100w"', self.tema)
        self.assertIn(peca.format(*CREDITOS[1]) + '</div><figcaption>O Turco, numa gravura de 1789: a caixa onde estava alguém.</figcaption></figure>', self.tema)
        # o mesmo crédito que a sessão 05 do módulo 2 já dá a esta gravura
        self.assertIn('O Turco, o autómato de xadrez de Wolfgang von Kempelen, numa gravura de Joseph Racknitz, 1789.', ler('cidadania/m2/sessoes/index.html') + ''.join(
            ler(p.relative_to(ROOT).as_posix()) for p in (ROOT / 'cidadania/m2/sessoes').glob('*/index.html')))
        # nenhuma imagem nova: as cinco já estavam no repositório, e nenhuma é servida de fora
        existentes = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT).decode().splitlines()
        for rel in PAGINAS:
            for img in Pagina(ler(rel)).imgs:
                f, _ = alvo(rel, img['src'])
                self.assertIn(f.relative_to(ROOT).as_posix(), existentes)
                self.assertNotIn('://', img['src'])
        # vídeos: nenhum incorporado nestas páginas
        for rel in PAGINAS:
            self.assertNotRegex(ler(rel), r'<(?:iframe|video)\b|youtube|youtu\.be|vimeo')

    def test_casca_das_quatro_paginas_de_tema(self):
        # 13/11/2026: pedido temas-01-03-04. A casca, os títulos, a atividade que abre, as alternativas, o bloco para aplicar, a linha da
        # aula e a dobra «Ver tudo neste tema» conferem-se nas quatro páginas, pela tabela PECAS; o teste que se segue conserva, letra a
        # letra, o que já se exigia à página do tema 02.
        css = ler('assets/temas.css')
        for n, href, nome, pergunta, _ in TEMAS:
            t, p = self.temas[n], PECAS[n]
            with self.subTest(tema=n):
                self.assertTrue(t.startswith('<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8">'))
                for uma_vez in ('assets/appearance.css', 'assets/appearance.js', 'assets/info-i.css', 'assets/info-i.js', 'assets/temas.css?v=20261113-1',
                                '<script defer src="../assets/projection-launcher.js?v=20261019.4" data-site="lente"></script>', '<body class="tm-pag" data-site="lente">',
                                '<main class="tm-main">', '<h1 ', '<meta name="viewport" content="width=device-width,initial-scale=1', '<p class="tm-sec" id="tm-comeca-t">Começa por aqui</p>',
                                '<p class="tm-sec" id="tm-alt-t">Ou escolhe outra pergunta</p>', '<p class="tm-sec" id="tm-aplicar-t">Para aplicar</p>', '<span class="tm-comeca-rot" aria-hidden="true">Começar</span>',
                                '<footer class="tm-rodape"><nav aria-label="Mais ligações"><ul><li><a href="../">← Voltar aos quatro temas</a></li><li><a href="../mapa/">Mapa do Lente</a></li></ul></nav></footer>'):
                    self.assertEqual(t.count(uma_vez), 1, uma_vez)
                self.assertNotIn('<style', t)
                self.assertNotRegex(t, r'<script(?![^>]*\bsrc=)')
                # a mesma casca, letra a letra, da página do tema 02 (da abertura ao título e do rodapé ao fim)
                self.assertEqual(re.sub(r'<title>.*', '', t, flags=re.S), re.sub(r'<title>.*', '', self.tema, flags=re.S))
                self.assertEqual(t[t.index('<footer class="tm-rodape">'):], self.tema[self.tema.index('<footer class="tm-rodape">'):])
                for folha in ('appearance.css', 'appearance.js', 'info-i.css', 'info-i.js', 'temas.css', 'projection-launcher.js'):
                    self.assertEqual(re.findall(r'assets/' + re.escape(folha) + r'\?v=([\w.-]+)', t), re.findall(r'assets/' + re.escape(folha) + r'\?v=([\w.-]+)', self.entrada), folha)
                self.assertEqual(Pagina(t).titulos, [('h1', pergunta), ('h2', p['comeca'][0])] + [('h2', q) for _, q in p['alternativas']] + [('h2', p['aplicar'][0]), ('h2', 'Ver tudo neste tema')]
                                 + [('h3', g) for g, _ in p['grupos']])
                self.assertIn('<p class="tm-ante"><b aria-hidden="true">' + n + '</b>' + nome + '</p><h1 class="tm-perg">' + pergunta + '</h1><p class="tm-abre-t">', t)
                self.assertIn('<p class="tm-q">' + pergunta + '</p>', self.cartoes[int(n) - 1])
                self.assertEqual(re.findall(r'<a class="tm-botao" href="([^"]+)">', t), [SITIO + p['comeca'][1]])
                self.assertEqual(re.findall(r'<li><h2><a href="' + re.escape(SITIO) + r'([^"]+)">([^<]+)</a></h2><p>[^<]', t), p['alternativas'])
                self.assertEqual(len(re.findall(r'</h2><p>.+?</p><p class="tm-meta">[^<]+</p><span class="tm-seta" aria-hidden="true">→</span></li>', t)), 4)
                # um bloco para aplicar, com duas ligações, e uma linha para a aula
                aplicar = t[t.index('<div class="tm-aplicar">'):t.index('</section>', t.index('<div class="tm-aplicar">'))]
                self.assertEqual(re.findall(r'<li><a href="' + re.escape(SITIO) + r'([^"]+)">[^<]+</a></li>', aplicar), p['aplicar'][1])
                self.assertEqual(t.count('<p class="tm-aula">É para uma aula? <a href="' + SITIO + p['aula'][0] + '">' + p['aula'][1] + '</a></p>'), 1)
                self.assertEqual(t.count('class="tm-aula"'), 1)
                # «Ver tudo» é uma details nativa, fechada ao carregar, em duas colunas
                self.assertEqual(t.count('<details class="tm-tudo"><summary><h2>Ver tudo neste tema</h2></summary><p class="tm-tudo-n">As páginas deste tema, por tipo. '), 1)
                self.assertNotRegex(t, r'<details[^>]*\bopen\b')
                tudo = t[t.index('<details class="tm-tudo">'):t.index('</details>', t.index('<details class="tm-tudo">'))]
                self.assertEqual([len(re.findall(r'<li>', g)) for g in re.findall(r'<ul>.*?</ul>', tudo)], [q for _, q in p['grupos']])
                self.assertEqual(tudo.count('<div><h3>'), 2)
                # a ordem dos blocos
                ordem = [t.index(x) for x in ('<nav class="tm-migas"', '<header class="tm-abre">', 'id="tm-comeca-t"', 'id="tm-alt-t"', 'id="tm-aplicar-t"', '<p class="tm-aula">', '<details class="tm-tudo">', '<footer class="tm-rodape">')]
                self.assertEqual(ordem, sorted(ordem))
        for regra in ('--tm-tinta:var(--tinta,#000)', 'html.epi-projection .tm-pag', '@media print{',
                      # o crédito aberto lê-se inteiro: a moldura da imagem cresce com ele (o do esboço de Van Gogh, a 320 px)
                      '.tm-fig .com-i:has(>.info-i[open])>.info-i>.info-i-texto{position:relative;inset:auto;margin:8px;max-block-size:none;overflow:visible}'):
            self.assertIn(regra, css)
        self.assertEqual(len(set(re.findall(r'temas\.css\?v=([\w.-]+)', ''.join(ler(p) for p in PAGINAS)))), 1)

    # 13/11/2026: a folha dos temas ganhou a regra do crédito aberto nas páginas de tema (ver abaixo) e passa a pedir-se com a versão
    # 20261113-1 na entrada e nas quatro páginas; a exigência é a mesma (uma só vez, a mesma versão em todas).
    def test_casca_da_pagina_do_tema(self):
        t = self.tema
        self.assertTrue(t.startswith('<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8">'))
        for uma_vez in ('assets/appearance.css', 'assets/appearance.js', 'assets/info-i.css', 'assets/info-i.js', 'assets/temas.css?v=20261113-1',
                        '<script defer src="../assets/projection-launcher.js?v=20261019.4" data-site="lente"></script>', '<body class="tm-pag" data-site="lente">',
                        '<main class="tm-main">', '<h1 ', '<meta name="viewport" content="width=device-width,initial-scale=1'):
            self.assertEqual(t.count(uma_vez), 1, uma_vez)
        self.assertNotIn('<style', t)
        self.assertNotRegex(t, r'<script(?![^>]*\bsrc=)')
        # as mesmas versões das folhas e dos scripts comuns que a entrada pede
        for peca in ('appearance.css', 'appearance.js', 'info-i.css', 'info-i.js', 'temas.css', 'projection-launcher.js'):
            v = re.findall(r'assets/' + re.escape(peca) + r'\?v=([\w.-]+)', self.entrada)
            self.assertEqual(re.findall(r'assets/' + re.escape(peca) + r'\?v=([\w.-]+)', t), v, peca)
            self.assertEqual(len(v), 1, peca)
        # títulos: a pergunta é o h1; cada bloco tem o seu h2; os grupos de «Ver tudo» são h3
        self.assertEqual(Pagina(t).titulos, [
            ('h1', 'Porque estás a ver isto?'), ('h2', 'A regra do feed'),
            ('h2', 'Três páginas que repetem a mesma frase são três confirmações?'), ('h2', 'Quem está por trás desta página?'),
            ('h2', 'Se a conta é grátis, quem paga?'), ('h2', 'Quando a máquina faz, quem responde?'), ('h2', 'Contra-feed.'),
            ('h2', 'Ver tudo neste tema'), ('h3', 'Casos para decidir'), ('h3', 'Verificar fontes'), ('h3', 'Criar e mostrar'),
            ('h3', 'Os passos do módulo Algoritmos'), ('h3', 'Para consultar')])
        self.assertIn('<p class="tm-ante"><b aria-hidden="true">02</b>Informação e mundo digital</p><h1 class="tm-perg">Porque estás a ver isto?</h1>', t)
        # a mesma pergunta e o mesmo nome do cartão da entrada
        self.assertIn('<p class="tm-q">Porque estás a ver isto?</p>', self.cartoes[1])
        # a atividade que abre o tema e as quatro alternativas, pela ordem
        self.assertEqual(re.findall(r'<a class="tm-botao" href="([^"]+)">', t), [SITIO + 'cidadania/m2/cid-m2-a-regra-do-feed/'])
        self.assertEqual(re.findall(r'<li><h2><a href="' + re.escape(SITIO) + r'([^"]+)">', t),
                         ['cidadania/m2/cid-m2-o-rasto-da-afirmacao/', 'investigar/passo-08/', 'cidadania/m2/cid-m2-preco-minuto/', 'cidadania/m2/cid-m2-dentro-da-caixa/'])
        # «Ver tudo» é uma details nativa, fechada ao carregar, com 23 ligações em cinco grupos
        self.assertEqual(t.count('<details class="tm-tudo"><summary><h2>Ver tudo neste tema</h2></summary>'), 1)
        tudo = t[t.index('<details class="tm-tudo">'):t.index('</details>', t.index('<details class="tm-tudo">'))]
        self.assertEqual([len(re.findall(r'<li>', g)) for g in re.findall(r'<ul>.*?</ul>', tudo)], [5, 3, 3, 9, 3])
        # a folha dos temas segue o alternador de aparência (variáveis da casa) e os dois modos de projeção
        css = ler('assets/temas.css')
        for regra in ('--tm-tinta:var(--tinta,#000)', '--tm-papel:var(--papel,#fff)', '--tm-fundo:var(--fundo,#f3f2ee)', 'html.em-projecao [data-cartaz-entrada]',
                      'html.epi-projection .tm-pag', '@media print{'):
            self.assertIn(regra, css)

    def test_entrada_conserva_a_casca(self):
        e = self.entrada
        self.assertIn('<main class="lente" data-cartaz="2" data-cartaz-entrada>', e)
        for uma_vez in ('assets/appearance.css', 'assets/appearance.js', 'data-appearance-site="lente"', '<h1 class="lente-nome">Lente<i aria-hidden="true">.</i></h1>',
                        '<div class="lf-mesa" aria-hidden="true">', 'assets/cartaz-entrada.js', 'assets/cartaz-entrada.css', 'assets/fundos.js', 'assets/info-i.js',
                        'assets/projection-launcher.js', 'lente-cidadania-m1-sessoes-v2', '<script id="amp-js">', 'assets/temas.css?v=20261113-1'):
            self.assertEqual(e.count(uma_vez), 1, uma_vez)
        self.assertNotIn('assets/praticar.css', e)
        self.assertTrue((ROOT / 'praticar/index.html').is_file())
        self.assertIn('assets/praticar.css', ler('praticar/index.html'))

    def test_camada_das_paginas_dos_temas_fechada_em_vigor_e_reversivel(self):
        # 13/11/2026: pedido temas-01-03-04. A camada nova, a mais recente: leva o main 9a5e6e1 ao ficheiro de hoje, letra a letra.
        c = temas_paginas_20261113
        self.assertEqual({f: len(t) for f, t in c.TROCAS.items()}, {'index.html': 5, 'mapa/index.html': 1})
        for f, trocas in c.TROCAS.items():
            with self.subTest(ficheiro=f):
                agora = ler(f)
                partida = subprocess.check_output(['git', 'show', BASE_TEMAS + ':' + f], cwd=ROOT).decode('utf-8')
                for antigo, novo, n in trocas:
                    self.assertEqual(n, 1)
                    self.assertEqual(agora.count(novo), n)
                    self.assertEqual(partida.count(antigo), n)
                    self.assertNotIn(antigo, agora.replace(novo, ''))
                self.assertEqual(c.desfazer(agora, f), partida)
                self.assertEqual(c.aplicar(partida, f), agora)
                self.assertEqual(c.alinhar(agora, f), agora)
                self.assertEqual(c.alinhar(partida, f), agora)
        # o que não está no manifesto fica como no main: a ajuda fica igual; a página do tema 02 só muda a versão da folha dos temas;
        # a folha dos temas só ganha um bloco (o crédito aberto nas páginas de tema), sem perder nem mudar nenhuma regra
        do_main = lambda f: subprocess.check_output(['git', 'show', BASE_TEMAS + ':' + f], cwd=ROOT).decode('utf-8')  # noqa: E731
        self.assertEqual(ler('como/index.html'), do_main('como/index.html'))
        self.assertEqual(do_main('informacao/index.html').count('assets/temas.css?v=20261112-1'), 1)
        self.assertEqual(ler('informacao/index.html'), do_main('informacao/index.html').replace('assets/temas.css?v=20261112-1', 'assets/temas.css?v=20261113-1'))
        css, antes = ler('assets/temas.css'), do_main('assets/temas.css')
        corte = css.index('/* 13/11/2026 (páginas dos temas 01, 03 e 04)')
        fim = css.index('\n', css.index('.tm-perg{font-size:min(clamp(2.4375rem,9.5vw,3.8125rem),11.5cqw)}', corte)) + 1
        self.assertEqual(css[:corte] + css[fim:], antes)
        self.assertTrue(css[corte:fim].count('.tm-fig .com-i:has(>.info-i[open])') == 5 and '@media screen{' in css[corte:fim])
        apagados = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE_TEMAS], cwd=ROOT).decode().splitlines()
        self.assertEqual([f for f in apagados if not (ROOT / f).exists()], [])
        # as três páginas novas não existiam nesse main
        for n in ANTIGOS:
            self.assertNotIn(TEMAS[int(n) - 1][1] + 'index.html', apagados)
        # a cadeia das camadas (tests/creditos_i_lente3.py) aplica e desfaz esta por fora de todas
        cadeia = ler('tests/creditos_i_lente3.py')
        self.assertIn('return temas_paginas_20261113.aplicar(entrada_temas_20261112.aplicar(', cadeia)
        self.assertIn('entrada_temas_20261112.desfazer(temas_paginas_20261113.desfazer(texto, ficheiro), ficheiro)', cadeia)
        self.assertIn('return temas_paginas_20261113.alinhar(entrada_temas_20261112.alinhar(', cadeia)

    def test_manifesto_fechado_em_vigor_e_reversivel(self):
        self.assertEqual(sorted(entrada_temas_20261112.TROCAS), ['como/index.html', 'index.html', 'mapa/index.html'])
        self.assertEqual({f: len(t) for f, t in entrada_temas_20261112.TROCAS.items()}, {'como/index.html': 1, 'index.html': 4, 'mapa/index.html': 1})
        for f, trocas in entrada_temas_20261112.TROCAS.items():
            with self.subTest(ficheiro=f):
                # 13/11/2026: pedido temas-01-03-04. A camada das páginas dos temas é agora a mais recente: desfaz-se primeiro, com
                # contagem exata, e o que fica (o main 9a5e6e1) confere-se como antes com a camada da entrada em quatro temas.
                agora = temas_paginas_20261113.desfazer(ler(f), f)
                partida = subprocess.check_output(['git', 'show', BASE + ':' + f], cwd=ROOT).decode('utf-8')
                for antigo, novo, n in trocas:
                    self.assertEqual(agora.count(novo), n)
                    self.assertEqual(partida.count(antigo), n)
                    self.assertNotIn(antigo, agora.replace(novo, ''))
                # letra a letra: o ficheiro de hoje é o do main com as trocas do manifesto, e mais nada
                self.assertEqual(entrada_temas_20261112.desfazer(agora, f), partida)
                self.assertEqual(entrada_temas_20261112.aplicar(partida, f), agora)
                self.assertEqual(entrada_temas_20261112.alinhar(agora, f), agora)
                self.assertEqual(entrada_temas_20261112.alinhar(partida, f), agora)
        # os verificadores que escrevem na entrada ou no mapa deixam-nos como estão
        for comando in (['tools/ideias_publico.py', '--verificar'],):
            r = subprocess.run([sys.executable] + comando, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_fluxos_correm_estes_testes(self):
        wf = ler('.github/workflows/cartaz-qa.yml')
        self.assertIn("- run: python -m unittest discover -s tests -p 'test_*.py'\n", wf)
        self.assertIn('- run: node tests/browser_entrada_temas.cjs\n', wf)
        self.assertTrue((ROOT / 'tests/browser_entrada_temas.cjs').is_file())
        caminhos = re.findall(r"paths: \[(.*?)\]", wf)
        self.assertEqual(len(caminhos), 2)
        for linha in caminhos:
            # 13/11/2026: pedido temas-01-03-04. As três páginas novas e o manifesto da camada nova também acordam o fluxo.
            for caminho in ("'justica-e-vida-em-comum/**'", "'historias-e-criacao/**'", "'imagem-som-e-cidade/**'", "'tests/fixtures/temas-paginas-20261113.json'", "'tests/temas_paginas_20261113.py'"):
                self.assertIn(caminho, linha, caminho)
            for caminho in ("'index.html'", "'informacao/**'", "'assets/temas.css'", "'mapa/**'", "'como/**'", "'tests/*entrada_temas*'",
                            "'tests/fixtures/entrada-temas-20261112.json'", "'tools/ideias_publico.py'"):
                self.assertIn(caminho, linha, caminho)
        # a página nova entra também nas baterias que percorrem todas as páginas (hierarquia dos títulos e texto justificado)
        self.assertIn('python tests/browser_hierarquia_titulos.py', wf)
        self.assertIn('python tests/browser_texto_justificado.py', wf)


if __name__ == '__main__':
    unittest.main()
