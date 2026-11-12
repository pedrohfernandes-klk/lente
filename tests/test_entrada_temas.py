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

SITIO = 'https://pedrohfernandes-klk.github.io/lente/'
BASE = 'b8abe97f65adb6c995579807bb89f9359d7ce869'
TEMAS = [
    ('01', SITIO + 'olhar-e-decidir/', 'Justiça e vida em comum', 'Uma regra igual é sempre justa?', 'img/cidadania/daumier-700.webp'),
    ('02', 'informacao/', 'Informação e mundo digital', 'Porque estás a ver isto?', 'img/cidadania/turco-700.webp'),
    ('03', SITIO + 'narrativas/', 'Histórias e criação', 'O que transforma uma ideia numa história?', 'assets/laboratorio/van-gogh-quarto-carta.webp'),
    ('04', SITIO + 'cidade/', 'Imagem, som e cidade', 'O que muda quando mudas o enquadramento?', 'img/arquivo/rua-da-boavista-carris-2026-720.webp'),
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
PAGINAS = ['index.html', 'informacao/index.html']
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

    def test_so_o_tema_02_tem_pagina_nova_e_nada_promete_outras(self):
        # o tema 02 abre a página nova; os outros três abrem áreas que já existiam no main
        existentes = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT).decode().splitlines()
        self.assertNotIn('informacao/index.html', existentes)
        self.assertTrue((ROOT / 'informacao/index.html').is_file())
        for n, href, _, _, _ in TEMAS:
            f, _ = alvo('index.html', href)
            self.assertTrue(f.is_file(), href)
            self.assertEqual(f.relative_to(ROOT).as_posix() in existentes, n != '02', href)
        # não há outras páginas de tema, nem ligações para elas
        self.assertEqual(sorted(p.parent.name for p in ROOT.glob('*/index.html') if 'class="tm-pag"' in p.read_text(encoding='utf-8')), ['informacao'])
        for rel in PAGINAS:
            texto = visivel(ler(rel))
            for promessa in ('noutro tema', 'outros temas', 'página nova', 'em breve', 'brevemente', 'a caminho', 'por agora', 'ainda não', 'em construção'):
                self.assertNotIn(promessa, texto.lower(), (rel, promessa))
        # na página do tema, «os quatro temas» é a entrada
        self.assertEqual(re.findall(r'<a href="\.\./">([^<]+)</a>', self.tema), ['← Lente: os quatro temas', '← Voltar aos quatro temas'])

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
        self.assertGreater(vistos, 350)
        # as ligações da entrada e da página do tema, uma a uma
        self.assertEqual(len(Pagina(self.entrada).hrefs), 4 + 3 + 1 + 5 + 2 + 2 + 1 + 3 + 2)
        self.assertEqual(len(Pagina(self.tema).hrefs), 1 + 1 + 1 + 4 + 2 + 1 + 23 + 2)
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
        self.assertEqual(antes - agora - sairam, {
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
        perguntas = re.findall(r'<p class="tm-q">([^<]+)</p>', self.entrada) + re.findall(r'<h2><a href="[^"]+">([^<]+)</a></h2>', self.tema)
        self.assertEqual(len(perguntas), 8)
        for p in perguntas:
            self.assertTrue(p.endswith('?'), p)
        # títulos de obras em itálico nos créditos
        self.assertIn('<i>Les gens de justice</i>', self.entrada)
        self.assertIn('<i>O Quarto</i>', self.entrada)
        self.assertIn('<i>Ensaio sobre a Cegueira</i>', self.entrada)
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
        for pagina, frase, origem, passagens in provas:
            with self.subTest(frase=frase[:50]):
                self.assertIn(frase, re.sub(r'<[^>]+>', '', ler(pagina)))
                fonte = re.sub(r'<[^>]+>', '', ler(origem).replace('\\u003c', '<').replace('\\"', '"').replace('\\/', '/'))
                fonte = re.sub(r'\s+', ' ', fonte.replace('&nbsp;', ' '))
                for passagem in passagens:
                    self.assertIn(passagem, fonte, (origem, passagem))
        # os rótulos de «Ver tudo neste tema» são os títulos das páginas (com um acrescento onde dois títulos são iguais)
        for href, rotulo in re.findall(r'<li><a href="' + re.escape(SITIO) + r'([^"]+)">([^<]+)</a></li>', self.tema[self.tema.index('<details class="tm-tudo">'):]):
            titulo = re.search(r'<title>([^<]+)</title>', ler(href + 'index.html'))[1].split(' · ')[0]
            with self.subTest(href=href):
                self.assertTrue(rotulo.startswith(titulo.rstrip('?')) or rotulo.startswith(titulo), (rotulo, titulo))

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

    def test_casca_da_pagina_do_tema(self):
        t = self.tema
        self.assertTrue(t.startswith('<!doctype html><html lang="pt-PT" data-appearance-site="lente"><head><meta charset="utf-8">'))
        for uma_vez in ('assets/appearance.css', 'assets/appearance.js', 'assets/info-i.css', 'assets/info-i.js', 'assets/temas.css?v=20261112-1',
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
                        'assets/projection-launcher.js', 'lente-cidadania-m1-sessoes-v2', '<script id="amp-js">', 'assets/temas.css?v=20261112-1'):
            self.assertEqual(e.count(uma_vez), 1, uma_vez)
        self.assertNotIn('assets/praticar.css', e)
        self.assertTrue((ROOT / 'praticar/index.html').is_file())
        self.assertIn('assets/praticar.css', ler('praticar/index.html'))

    def test_manifesto_fechado_em_vigor_e_reversivel(self):
        self.assertEqual(sorted(entrada_temas_20261112.TROCAS), ['como/index.html', 'index.html', 'mapa/index.html'])
        self.assertEqual({f: len(t) for f, t in entrada_temas_20261112.TROCAS.items()}, {'como/index.html': 1, 'index.html': 4, 'mapa/index.html': 1})
        for f, trocas in entrada_temas_20261112.TROCAS.items():
            with self.subTest(ficheiro=f):
                agora = ler(f)
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
            for caminho in ("'index.html'", "'informacao/**'", "'assets/temas.css'", "'mapa/**'", "'como/**'", "'tests/*entrada_temas*'",
                            "'tests/fixtures/entrada-temas-20261112.json'", "'tools/ideias_publico.py'"):
                self.assertIn(caminho, linha, caminho)
        # a página nova entra também nas baterias que percorrem todas as páginas (hierarquia dos títulos e texto justificado)
        self.assertIn('python tests/browser_hierarquia_titulos.py', wf)
        self.assertIn('python tests/browser_texto_justificado.py', wf)


if __name__ == '__main__':
    unittest.main()
