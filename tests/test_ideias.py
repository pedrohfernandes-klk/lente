"""30/10/2026: coração do Laboratório, «Ideias» (narrativas/ideias/), em piloto escondido (decisões do docente 31 a 34 e 39;
construído a 31/10). Confirma, sem navegador:
- que as lições validam e as páginas geradas estão atualizadas (tools/licoes_lente.py, família «laboratorio»), e que a
  família da Cidadania continua a gerar as mesmas páginas;
- que o validador apanha os erros novos (família desconhecida, cartão «mapa» malformado);
- que a entrada, o guião, o guia do docente e a página do Young na Biblioteca estão atualizados (tools/ideias_piloto.py);
- noindex, nofollow em todas as páginas do piloto e em nenhuma outra página nova; a página da Biblioteca é pública;
- nenhuma página fora do piloto liga para ele (mapa, portas, entrada do Laboratório, percursos.json, Biblioteca);
- que todas as ligações internas e âncoras das páginas novas resolvem;
- opções equilibradas na pasta nova, sem exceções;
- as regras de escrita no texto visível, as imagens (licença e tabela de museu) e o excerto da Biblioteca.
O percurso no navegador está em tests/browser_licoes_lente.cjs (lições) e tests/browser_ideias.cjs (páginas)."""
import copy, hashlib, importlib.util, json, math, pathlib, re, unittest
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = pathlib.Path(__file__).resolve().parents[1]


def carregar(nome, rel):
    spec = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


L = carregar('licoes_lente', 'tools/licoes_lente.py')
I = carregar('ideias_piloto', 'tools/ideias_piloto.py')
M = carregar('medir_opcoes', 'tools/medir_opcoes.py')
LENTE = 'https://pedrohfernandes-klk.github.io/lente/'
PILOTO = ROOT / 'narrativas/ideias'
FONTES = sorted((ROOT / 'tools/licoes').glob('ideias-s*.json'))
BIB = ROOT / 'biblioteca/young-tecnica-1940/index.html'
ROBOTS = '<meta name="robots" content="noindex, nofollow">'


class Ligacoes(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.ids = set()

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ('href', 'src', 'data-href') and v:
                self.links.append(v)
            if k == 'id' and v:
                self.ids.add(v)


def analisar(s):
    p = Ligacoes(); p.feed(s); return p


def cartoes_de(s):
    """Os cartões das lições vêm num JSON dentro de um <script>: o html, a figura e as ligações do retorno também contam."""
    m = re.search(r'var CARTOES=(\[.*?\]),CFG=', s, re.S)
    return json.loads(m.group(1).replace('<\\/', '</')) if m else []


def paginas_piloto():
    return sorted(PILOTO.rglob('index.html'))


def alvo(pagina, url):
    """Ficheiro do repositório para onde aponta uma ligação interna (ou None, se for externa)."""
    u = urlsplit(url)
    if u.scheme in ('http', 'https'):
        if not url.startswith(LENTE):
            return None
        caminho = ROOT / unquote(u.path[len('/lente/'):])
    elif u.scheme or url.startswith('#') or not u.path:
        return None if not url.startswith('#') else pagina
    else:
        caminho = (pagina.parent / unquote(u.path)).resolve()
    if caminho.is_dir() or str(u.path).endswith('/'):
        caminho = caminho / 'index.html'
    return caminho


class Licoes(unittest.TestCase):
    def test_ha_duas_sessoes(self):
        self.assertEqual([p.name for p in FONTES], ['ideias-s01.json', 'ideias-s02.json'])

    def test_fontes_validas_e_paginas_atualizadas(self):
        for p in FONTES:
            d = json.loads(p.read_text('utf-8'))
            self.assertEqual(L.validar(d), [], p.name)
            self.assertEqual(d['familia'], 'laboratorio')
            self.assertRegex(d['chave'], r'^epi-lab-ideias-s\d{2}$')
            self.assertTrue(d['piloto'])
            self.assertTrue(d['saida'].startswith('narrativas/ideias/sessao-'))
            s = (ROOT / d['saida']).read_text('utf-8')
            self.assertEqual(s, L.pagina(d), p.name + ': corre python3 tools/licoes_lente.py')
            self.assertIn('class="licao-lente licao-laboratorio"', s)
            self.assertIn('assets/licoes/laboratorio.css', s)
            self.assertNotIn('cidadania.css', s)
            # 01/11/2026: com o método assumido, o <title> diz também o passo («Sessão 1: Ver ou observar? (passo 1 de 5) | …»)
            self.assertRegex(d['passo'], r'^Passos? \d( e \d)? de 5$')
            self.assertIn('<title>' + d['titulo'] + ' (' + d['passo'].lower() + ') | Ideias | Laboratório | Lente</title>', s)

    def test_cada_sessao_tem_imagem_e_a_primeira_video(self):
        for p in FONTES:
            d = json.loads(p.read_text('utf-8'))
            html = ''.join(c.get('html') or '' for c in d['cartoes'])
            self.assertIn('<img', html, p.name)
            self.assertIn('<figcaption>', html, p.name)
        d1 = json.loads(FONTES[0].read_text('utf-8'))
        self.assertIn('data-yt="ubEadhXWwV4"', ''.join(c.get('html') or '' for c in d1['cartoes']))
        self.assertIn('video-youtube.js', (ROOT / d1['saida']).read_text('utf-8'))

    def test_cidadania_sem_mudanca(self):
        # a família por omissão é a Cidadania: os .json não têm «familia» e as páginas saem como estavam
        for p in sorted((ROOT / 'tools/licoes').glob('cidadania-*.json')):
            d = json.loads(p.read_text('utf-8'))
            self.assertNotIn('familia', d, p.name)
            s = (ROOT / d['saida']).read_text('utf-8')
            self.assertEqual(s, L.pagina(d), p.name)
            self.assertIn('class="licao-lente licao-cidadania"', s)
            self.assertNotIn('laboratorio.css', s)
            self.assertIn(' · Cidadania · Lente</title>', s)

    def test_validador_apanha_os_erros_novos(self):
        d = json.loads(FONTES[0].read_text('utf-8'))

        def com(f):
            e = copy.deepcopy(d); f(e); return ' | '.join(L.validar(e))
        self.assertIn('família desconhecida', com(lambda e: e.__setitem__('familia', 'teatro')))
        self.assertIn('epi-lab', com(lambda e: e.__setitem__('chave', 'epi-cid-m1-s01')))
        self.assertIn('seccao', com(lambda e: e.pop('seccao')))
        mapa = next(i for i, c in enumerate(d['cartoes']) if c['t'] == 'mapa')
        self.assertIn('centros', com(lambda e: e['cartoes'][mapa]['centros'].pop()))
        self.assertIn('zona .op-m', com(lambda e: e['cartoes'][mapa].__setitem__('fig', '<svg viewBox="0 0 10 10"></svg>')))
        self.assertIn('fe', com(lambda e: e['cartoes'][mapa].pop('fe')))
        self.assertIn('Qual das', com(lambda e: e['cartoes'][mapa].__setitem__('rotulo', 'Qual pormenor escolhes?')))

    def test_cartoes_mapa_sobre_o_quadro(self):
        d = json.loads(FONTES[0].read_text('utf-8'))
        mapas = [c for c in d['cartoes'] if c['t'] == 'mapa']
        self.assertEqual(len(mapas), 2)
        for c in mapas:
            self.assertEqual(c['rot'], 'Toca no quadro')
            self.assertIn('latour-leitora-da-sina.webp', c['fig'])
            self.assertIn('role="group"', c['fig'])
            # uma zona por opção, com o nome acessível igual à opção
            self.assertEqual(re.findall(r'aria-label="([^"]+)"><circle', c['fig']), c['o'])
            for x, y in c['centros']:
                self.assertTrue(0 < x < 1000 and 0 < y < 827)

    def test_numeros_da_sessao(self):
        # 01/11/2026: a sessão 1 ganha o cartão de leitura «O método» (a apresentação de Young): 21 cartões, os mesmos 13 de fazer
        for p, (n, fazer) in zip(FONTES, [(21, 13), (19, 12)]):
            d = json.loads(p.read_text('utf-8'))
            self.assertEqual(len(d['cartoes']), n, p.name)
            self.assertEqual(sum(c['t'] in L.TIPOS_FAZER for c in d['cartoes']), fazer, p.name)
            self.assertLessEqual(sum(len(L.visivel(c['html']).split()) for c in d['cartoes'] if c['t'] == 'ler'), 900)


class Paginas(unittest.TestCase):
    def test_gerador_das_paginas_atualizado(self):
        for rel, s in I.paginas().items():
            self.assertEqual((ROOT / rel).read_text('utf-8'), s, rel + ': corre python3 tools/ideias_piloto.py')
            self.assertEqual(I.regras(rel, s), [], rel)
        lista = (ROOT / 'biblioteca/index.html').read_text('utf-8')
        self.assertEqual(I.lista_biblioteca(lista), lista)

    def test_noindex_no_piloto_e_biblioteca_publica(self):
        pags = paginas_piloto()
        self.assertEqual(sorted(p.relative_to(ROOT).as_posix() for p in pags),
                         ['narrativas/ideias/docente/index.html', 'narrativas/ideias/guiao/index.html', 'narrativas/ideias/index.html',
                          'narrativas/ideias/sessao-01/index.html', 'narrativas/ideias/sessao-02/index.html'])
        for p in pags:
            self.assertEqual(p.read_text('utf-8').count(ROBOTS), 1, p)
        # a página do Young na Biblioteca é pública (encargo: a entrada na lista é pública, só com o excerto aprovado)
        self.assertNotIn('noindex', BIB.read_text('utf-8'))

    def test_nenhuma_pagina_fora_do_piloto_liga_para_ele(self):
        piloto = PILOTO.resolve()
        falhas = []
        for p in sorted(ROOT.rglob('*.html')):
            rel = p.relative_to(ROOT).as_posix()
            if rel.split('/')[0] in ('.git', 'tests', 'tools', 'node_modules') or p.resolve().is_relative_to(piloto):
                continue
            s = p.read_text('utf-8', errors='replace')
            if 'ideias' not in s:
                continue
            for url in analisar(s).links:
                a = alvo(p, url)
                if a is not None and a.resolve().is_relative_to(piloto):
                    falhas.append(f'{rel}: {url}')
        self.assertEqual(falhas, [])
        for rel in ('assets/laboratorio/percursos.json', 'assets/laboratorio/imagens.json'):
            self.assertNotIn('narrativas/ideias', (ROOT / rel).read_text('utf-8'), rel)
        # nem a página do Young na Biblioteca, enquanto o coração for piloto
        self.assertNotIn('narrativas/ideias', BIB.read_text('utf-8'))

    def test_ligacoes_internas_e_ancoras_resolvem(self):
        falhas = []
        for p in paginas_piloto() + [BIB]:
            s = p.read_text('utf-8')
            links = analisar(s).links
            for c in cartoes_de(s):
                for k in ('html', 'fig'):
                    links += analisar(c.get(k) or '').links
                links += [l['href'] for l in c.get('liga', [])]
            cfg = re.search(r',CFG=(\{.*?\});', s)
            if cfg:
                links += [v for k, v in json.loads(cfg.group(1)).items() if k in ('seguinte', 'percurso')]
            for url in links:
                a = alvo(p, url)
                if a is None:
                    continue
                if not a.is_file():
                    falhas.append(f'{p.relative_to(ROOT)}: {url}')
                    continue
                frag = urlsplit(url).fragment
                if frag and frag not in analisar(a.read_text('utf-8')).ids:
                    falhas.append(f'{p.relative_to(ROOT)}: âncora {url}')
        self.assertEqual(falhas, [])

    def test_entrada(self):
        s = (PILOTO / 'index.html').read_text('utf-8')
        self.assertEqual(s.count('class="proximo inverso"'), 1)
        self.assertEqual(s.count('class="botao"'), 1)
        self.assertLess(s.index('class="botao"'), s.index('class="gesto"'))
        self.assertEqual(len(re.findall(r'<button type="button" data-op aria-pressed="false">', s)), 3)
        self.assertEqual(len(re.findall(r'<li (?:class="prep" )?data-', s)), 7)
        self.assertEqual(s.count('Em preparação</span>'), 5)
        for p in FONTES:
            d = json.loads(p.read_text('utf-8'))
            self.assertIn(f'data-chave="{d["chave"]}" data-versao="{d["versao"]}"', s)
        self.assertIn('Ideias | Laboratório | Lente', s)
        self.assertIn('Como nasce uma ideia', s)
        self.assertIn('projetar=1', s)  # a projeção não lê o progresso
        self.assertIn('manihi-atol.webp', s)

    def test_guiao_e_guia(self):
        g = (PILOTO / 'guiao/index.html').read_text('utf-8')
        self.assertEqual(g.count('<section class="lado"'), 4)
        self.assertIn('window.print()', g)
        d = (PILOTO / 'docente/index.html').read_text('utf-8')
        for n in (1, 2):
            self.assertIn(f'id="s{n}"', d)
            self.assertIn(f'href="../sessao-0{n}/?projetar=1"', d)
        self.assertEqual(d.count('<td class="num">20</td>'), 2)
        self.assertIn('Avaliação indicativa', d)


class Opcoes(unittest.TestCase):
    def test_opcoes_equilibradas_na_pasta_nova(self):
        qs = [q for q in M.perguntas(ROOT) if q['pasta'] == 'narrativas/ideias']
        self.assertEqual(len(qs), 16)
        self.assertEqual([f"{q['pagina']} #{q['numero']}" for q in qs if q['amplitude20'] or q['denunciadora']], [])
        for pagina, r in M.resumir(qs, 'pagina').items():
            self.assertLessEqual(r['certaMaisLonga'], math.ceil(r['esperadoMaisLonga']), pagina)
            self.assertLessEqual(r['certaMaisCurta'], math.ceil(r['esperadoMaisLonga']), pagina)


class Escrita(unittest.TestCase):
    def texto(self, s):
        return L.visivel(re.sub(r'<(script|style|title)[^>]*>.*?</\1>', ' ', s, flags=re.S))

    def test_regras_da_casa_nas_licoes(self):
        for p in FONTES:
            d = json.loads(p.read_text('utf-8'))
            for c in d['cartoes']:
                for x in L.textos(c):
                    self.assertIsNone(L.PROIBIDAS.search(x), x[:60])
                    self.assertIsNone(L.QUAL_NOME.search(x), x[:60])
                    self.assertNotIn('"', x)

    def test_nada_do_nome_do_docente(self):
        # 30/10/2026: o crédito da tradução do Young é só «tradução nossa». Os nomes a evitar guardam-se em SHA-256, para não
        # ficarem escritos no repositório (o Pages serve a raiz, também tests/); e nenhumas iniciais de pessoa («X. Y.»).
        PROIBIDOS = {'ee5cd7d5d96c8874117891b2c92a036f96918e66c102bc698ae77542c186f981',
                     '08614c84a3bbb4b05eeea6030fee50ab3baa8475450a5aba9873c04b7cd96feb'}
        for p in paginas_piloto() + [BIB]:
            t = self.texto(p.read_text('utf-8'))
            for w in re.findall(r'\w+', t.lower()):
                self.assertNotIn(hashlib.sha256(w.encode('utf-8')).hexdigest(), PROIBIDOS, p)
            self.assertNotRegex(t, r'\b[A-ZÁÉÍÓÚ]\.\s?[A-ZÁÉÍÓÚ]\.', p)
        self.assertIn('Tradução nossa', self.texto(BIB.read_text('utf-8')))


class Imagens(unittest.TestCase):
    def test_imagens_vistas_com_tabela_e_licenca(self):
        pasta = ROOT / 'assets/laboratorio/ideias'
        self.assertEqual(sorted(f.name for f in pasta.iterdir()), ['atget-quiosque-fiacres.webp', 'latour-leitora-da-sina.webp', 'manihi-atol.webp'])
        for f in pasta.iterdir():
            self.assertLess(f.stat().st_size, 200_000, f.name)
        tudo = ''.join(p.read_text('utf-8') for p in paginas_piloto())
        for nome, licenca in (('latour-leitora-da-sina.webp', 'Domínio público (Open Access)'), ('atget-quiosque-fiacres.webp', 'CC0'), ('manihi-atol.webp', 'Domínio público')):
            self.assertIn(nome, tudo)
            self.assertIn(licenca, tudo)
        # as imagens das portas do Laboratório (decisão 34) não se repetem aqui
        for porta in ('van-gogh', 'blake', 'degas', 'lissitzky'):
            self.assertNotIn(porta, tudo)

    def test_excerto_da_biblioteca(self):
        s = BIB.read_text('utf-8')
        art = re.search(r'<article class="bib-texto" lang="pt-PT">(.*?)</article>', s, re.S).group(1)
        palavras = len(L.visivel(art.replace('[…]', '')).split())
        self.assertLessEqual(palavras, 120)
        self.assertEqual(palavras, sum(len(x.split()) for x in I.YOUNG_EXCERTO))
        self.assertIn('https://archive.org/details/techniqueforprod0000jame', s)
        self.assertIn('Combinação de Elementos Antigos', s)
        lista = (ROOT / 'biblioteca/index.html').read_text('utf-8')
        self.assertIn('href="young-tecnica-1940/" data-id="young-tecnica-1940"', lista)
        self.assertIn('{"id":"young-tecnica-1940"}', lista)
        self.assertIn('<b data-feitas>0</b> de 16 textos lidos', lista)


class SegundaRevisao(unittest.TestCase):
    """30/10/2026: segunda correção (revisões de 01/11 do diretor de arte, do revisor de pt-PT e do verificador de factos)."""

    def test_fontes_consultadas(self):
        # «Lidos a» não concordava com «Fontes» e colava-se aos casos inventados
        for p in FONTES:
            f = json.loads(p.read_text('utf-8'))['fontes']
            self.assertNotIn('Lidos a', f, p.name)
            self.assertIn('Consultadas a 31/10/2026.', f, p.name)

    def test_formas_com_pronome_sem_quebra_no_hifen(self):
        # nq() é idempotente: se não muda nada, todas as formas verbais com pronome do texto já estão numa <span class="nq">
        for p in FONTES:
            for c in json.loads(p.read_text('utf-8'))['cartoes']:
                if c['t'] == 'ler':
                    self.assertEqual(L.nq(c['html']), c['html'], p.name + ' ' + (c.get('titulo') or c.get('rot') or ''))
        for rel in ('index.html', 'guiao/index.html', 'docente/index.html'):
            s = (PILOTO / rel).read_text('utf-8')
            corpo = re.search(r'<main id="conteudo">(.*)</main>', s, re.S).group(1)
            self.assertEqual(L.nq(corpo), corpo, rel)
        self.assertIn('Amy\u00a0E.\u00a0Herman', (PILOTO / 'index.html').read_text('utf-8'))

    def test_marca_da_barra_e_cidadania_igual(self):
        # no Laboratório, o nome da marca num <span> (escondido abaixo de 400 px); na Cidadania, como estava
        for p in FONTES:
            d = json.loads(p.read_text('utf-8'))
            # 01/11/2026: a marca leva também o passo do método, numa <span> própria, logo a seguir ao nome
            self.assertIn('<span class="c-marca-t">Ideias</span><span class="c-marca-p">Passo 1 de 5</span></a>', (ROOT / d['saida']).read_text('utf-8'))
        for p in sorted((ROOT / 'tools/licoes').glob('cidadania-*.json')):
            d = json.loads(p.read_text('utf-8'))
            self.assertNotIn('c-marca-t', (ROOT / d['saida']).read_text('utf-8'), p.name)
        css = (ROOT / 'assets/licoes/laboratorio.css').read_text('utf-8')
        self.assertIn('.licao-laboratorio .c-marca-t{position:absolute', css)

    def test_tema_do_young_na_barra(self):
        self.assertIn('</ol><span data-appearance-control></span></nav>', BIB.read_text('utf-8'))


class TerceiraRevisao(unittest.TestCase):
    """30/10/2026: terceira correção (revisões de 01/11 do diretor de arte, do revisor de pt-PT e do verificador de factos)."""

    def ler(self, rel):
        return L.visivel((PILOTO / rel).read_text('utf-8'))

    def test_texto_e_factos(self):
        s1 = json.loads(FONTES[0].read_text('utf-8'))
        s2 = json.loads(FONTES[1].read_text('utf-8'))
        c1 = {c.get('g'): c for c in s1['cartoes']}
        c2 = {c.get('g'): c for c in s2['cartoes']}
        # verificador: o resumo do TED-Ed fala do que se vê e do que não se vê; a fotografia de Atget é de 1898 a 1902
        self.assertIn('o que não se vê numa imagem', c1['invisivel']['p2'])
        self.assertIn('a quem serve (médicos, enfermeiros e polícias) e o que se treina (o que se vê e o que não se vê)', c1['resumo']['f'])
        self.assertIn('consigo apontar no quadro, com o dedo, o que ela diz?', c1['estatuto']['fe'])
        self.assertIn('abrir a porta de casa é verdade', c2['fila']['f'])
        html2 = ''.join(c.get('html') or '' for c in s2['cartoes'])
        self.assertIn('Entre dez e catorze anos depois do prefácio', html2)
        self.assertNotIn('Uns dez anos', html2)
        # revisor: quem escolhe o lugar da saída é o docente
        self.assertIn('até ao lugar escolhido.', html2)
        self.assertNotIn('escolhido pela turma', html2)
        self.assertIn('O teu «cocheiro»', [c.get('titulo') for c in s2['cartoes']])
        guia, guiao, entrada = self.ler('docente/index.html'), self.ler('guiao/index.html'), (PILOTO / 'index.html').read_text('utf-8')
        self.assertIn('as três colunas da fotografia passam a limpo no guião', guia)
        self.assertIn('(reconhecida: 6 pontos; não reconhecida, mas revista: 4 pontos)', guia)
        self.assertIn('a enfermeira Florence Nightingale', guia)
        self.assertIn('salvo quando o critério diz outros', guia)
        self.assertIn('se não houver saída, a alternativa', guia)
        # 30/10/2026: na quinta revisão (01/11), o revisor de pt-PT reescreveu a pergunta, que dava por certo que o sítio prova
        # alguma coisa (teste mudado de propósito; a frase nova confirma-se também em QuintaRevisao)
        self.assertIn('Boa pergunta para a turma: o sítio onde está é uma prova ou só uma pista mais forte?', guia)
        self.assertIn('cita-o duas vezes no livro', guia)
        # 01/11/2026: (correção 2 do método, revisor de pt-PT) quem traz Holmes é o autor do método, que o cita no livro; «quem o traz
        # é o próprio método» dava os cinco passos como quem cita (no guia, «o método» são os passos e «o livro» é o livro)
        self.assertIn('Sherlock Holmes é a testemunha que volta, e quem o traz é o autor do método: cita-o duas vezes no livro.', L.visivel(guia))
        self.assertNotIn('o próprio método', L.visivel(guia))
        self.assertNotIn('«Decide»', guiao)  # o papel do aluno não fala das peças da página
        self.assertIn('data-papel="o teu «cocheiro», a linha que levaste à fila e o resultado."', entrada)

    def test_sequencia_em_fichas_no_telemovel(self):
        s = (PILOTO / 'docente/index.html').read_text('utf-8')
        tab = re.search(r'<table class="seq" role="table">(.*?)</table>', s, re.S).group(1)
        cab = re.findall(r'<th role="columnheader"[^>]*>(.*?)</th>', tab)
        self.assertEqual(cab, I.SEQ_COLS)
        linhas = re.findall(r'<tr role="row">(.*?)</tr>', re.search(r'<tbody role="rowgroup">(.*)', tab, re.S).group(1))
        self.assertEqual(len(linhas), 7)
        for ln in linhas:
            self.assertEqual(re.findall(r'data-r="([^"]+)"', ln), I.SEQ_COLS)
        self.assertIn('@media (max-width:639px){.ideias table.seq,', s)

    def test_portas_dobradas_e_guiao(self):
        s = (PILOTO / 'index.html').read_text('utf-8')
        self.assertNotIn('id="porta-ver" aria-labelledby="pt-ver" data-dobra', s)
        for pid, nome, linha in (('treinar', 'Treinar', 'Sessões 3 e 4, em preparação'), ('criar', 'Criar', 'Sessões 5 a 7, em preparação')):
            self.assertIn(f'id="porta-{pid}" aria-labelledby="pt-{pid}" data-dobra', s)
            self.assertIn(f'<p class="porta-linha">{linha}</p><button type="button" class="porta-abre" data-nome="{nome}" '
                          f'aria-expanded="false" aria-controls="pc-{pid}" aria-label="Abrir {nome}"></button>', s)
            self.assertIn(f'id="pc-{pid}"', s)
        # html.cv só com script e fora da projeção, no <head>
        cab = s[:s.index('</head>')]
        self.assertIn('document.documentElement.classList.add("cv")', cab)
        self.assertIn('projetar=1', cab)
        # a tabela de museu continua dentro do <figure>
        self.assertRegex(s, r'<figure class="atol">.*?<figcaption>.*?</figcaption></figure>')
        g = (PILOTO / 'guiao/index.html').read_text('utf-8')
        herman = re.search(r'O vídeo de Herman, em duas colunas</h3><table class="grelha-escrever">(.*?)</table>', g).group(1)
        self.assertEqual(herman.count('<tr><td></td><td></td></tr>'), 8)

    def test_young_so_nesta_pagina(self):
        s = BIB.read_text('utf-8')
        for regra in ('.p-cab .p-etiqueta{font-size:.8125rem}', '.bib-fonte>a[href$="/biblioteca/"]{display:inline-flex;align-items:center;min-height:44px}',
                      '.bib .bib-texto{max-width:32em;line-height:1.55}', '.p-cab .p-lead{text-align:start!important;max-width:32em}'):
            self.assertIn(regra, s)
        self.assertNotIn('letter-spacing:.2em', s)
        # o molde comum das outras páginas da Biblioteca não muda neste pedido
        orta = (ROOT / 'biblioteca/orta-benjui/index.html').read_text('utf-8')
        self.assertNotIn('.bib .bib-texto{max-width:32em', orta)
        self.assertIn('.p-etiqueta{font:700 .72rem/1.2 var(--sans)', orta)



class QuartaRevisao(unittest.TestCase):
    """30/10/2026: as correções da quarta revisão (01/11): o rodapé da lista da Biblioteca deixa de dizer que todos os textos em
    português estão em domínio público (verificador de factos); o texto do revisor de pt-PT; e as regras de desenho do diretor de
    arte que se podem confirmar sem navegador (as medidas estão em tests/browser_ideias.cjs, secção 8)."""

    def test_rodape_da_biblioteca(self):
        # 30/10/2026: o excerto de Young é tradução nossa e não está em domínio público (decisão 31)
        lista = (ROOT / 'biblioteca/index.html').read_text('utf-8')
        self.assertIn(f'<p class="rodape">{I.RODAPE_DEPOIS} ', lista)
        self.assertNotIn('Os textos em português estão em domínio público;', lista)
        self.assertNotIn('o que é nosso é o cabeçalho e a nota.', lista)
        # a troca é idempotente
        self.assertEqual(I.lista_biblioteca(lista), lista)

    def test_texto_do_revisor(self):
        guia = (PILOTO / 'docente/index.html').read_text('utf-8')
        # a decisão do docente (saída opcional, com alternativa) e o «cocheiro» de cada aluno, como no cartão e na grelha
        self.assertIn('sem ela, cada aluno escolhe o seu «cocheiro» da janela', guia)
        self.assertNotIn('cada par escolhe', guia)
        self.assertIn('Guião: cada um completa a tabela das duas versões do conselho; «Para levar».', guia)
        self.assertIn('Grelha /20 indicativa: o auto de observação, por grupo</h3>', guia)
        self.assertIn('Grelha indicativa: o auto de observação, por grupo</caption>', guia)
        self.assertIn('Os dois cartões «Toca no quadro» são novos no Lente:', guia)
        self.assertNotRegex(L.visivel(re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', guia, flags=re.S)), r'\bmotor\b')  # jargão da equipa
        # 01/11/2026: com o cartão «O método» na posição 2, o resumo com a ligação passa a cartão 9 (índice 8)
        self.assertIn('(a ligação aparece no retorno do cartão 9)', guia)
        s1 = json.loads((ROOT / 'tools/licoes/ideias-s01.json').read_text('utf-8'))
        self.assertEqual(s1['cartoes'][8]['g'], 'resumo')
        self.assertTrue(s1['cartoes'][8].get('liga'))
        estatuto = next(c for c in s1['cartoes'] if c.get('g') == 'estatuto')
        self.assertTrue(all(re.match(r'^Uma? [^\W\d_]+: ', d) for _e, d in estatuto['pares']), estatuto['pares'])
        s2 = json.loads((ROOT / 'tools/licoes/ideias-s02.json').read_text('utf-8'))
        cedo = next(c for c in s2['cartoes'] if c.get('g') == 'cedo')
        # 01/11/2026: o nome de Young só onde o método fala; a pergunta é a mesma, sobre «a frase»
        self.assertEqual(cedo['p2'], 'Que três palavras da frase dizem o que fazemos mal, e quando? Toca nelas.')
        self.assertEqual(len(cedo['certas']), 3)
        html2 = json.dumps(s2['cartoes'], ensure_ascii=False)
        self.assertIn('escreve uma linha que só sirva para esse «cocheiro».', html2)
        self.assertIn('Também puseste uma descrição à prova', html2)

    def test_regras_de_desenho(self):
        entrada = (PILOTO / 'index.html').read_text('utf-8')
        self.assertIn('.ideias h2.sessoes-t{font:400 3rem/1 ', entrada)
        self.assertIn('@media (min-width:960px) and (max-width:1099px){html.em-projecao .ideias .gesto .ops{grid-template-columns:minmax(0,1fr)}}', entrada)
        self.assertIn('.ideias .abre .info,.ideias .topo .atol figcaption{max-width:34em}', entrada)
        guia = (PILOTO / 'docente/index.html').read_text('utf-8')
        self.assertEqual(guia.count('<p class="acoes-s"><a class="botao-s"'), 2)
        self.assertIn('@media (max-width:479px){.ideias.guia .acoes-s{display:grid;', guia)
        self.assertIn('.ideias.guia .pg b{white-space:nowrap}', guia)
        self.assertIn('.ideias.guia ul.ligacoes a{display:block;min-height:44px;padding:9px 0}', guia)
        guiao = (PILOTO / 'guiao/index.html').read_text('utf-8')
        self.assertIn('<span class="nq">(grupos <i class="b"></i> e <i class="b"></i>).</span>', guiao)
        self.assertIn('pelo grupo\u00a0___', guiao)
        # só na família do Laboratório: a Cidadania não carrega este ficheiro
        self.assertIn('.licao-laboratorio .jogo .inline .nb{display:inline}', (ROOT / 'assets/licoes/laboratorio.css').read_text('utf-8'))
        for p in (ROOT / 'cidadania/piloto').rglob('index.html'):
            self.assertNotIn('laboratorio.css', p.read_text('utf-8'), p)


class QuintaRevisao(unittest.TestCase):
    """30/10/2026: as correções da quinta revisão (01/11): o texto do revisor de pt-PT e as regras de desenho do diretor de arte que
    se podem confirmar sem navegador (as medidas estão em tests/browser_ideias.cjs, secção 9)."""

    def test_texto_do_revisor(self):
        s1 = json.loads(FONTES[0].read_text('utf-8'))
        s2 = json.loads(FONTES[1].read_text('utf-8'))
        c1 = {c.get('g'): c for c in s1['cartoes']}
        c2 = {c.get('g'): c for c in s2['cartoes']}
        aula = next(c for c in s1['cartoes'] if c.get('rot') == 'Na aula')['html']
        self.assertIn('Cada um regista os seus factos, um por nota; o grupo escolhe dez', aula)
        self.assertNotIn('um de cada vez', aula)
        # o motor mostra a zona sozinha numa linha por baixo do quadro: maiúscula inicial, no nome e no aria-label
        for g in ('cordao', 'medalha'):
            self.assertTrue(all(o[:1].isupper() for o in c1[g]['o']), c1[g]['o'])
            for o in c1[g]['o']:
                self.assertIn(f'aria-label="{o}"', c1[g]['fig'])
        self.assertIn('«Prateada» e «útil» servem para quase todas, «bonita» é uma opinião', c2['fila']['f'])
        guia = L.visivel((PILOTO / 'docente/index.html').read_text('utf-8'))
        guiao = L.visivel((PILOTO / 'guiao/index.html').read_text('utf-8'))
        self.assertIn('escreve-se no guião impresso e onde cada um guarda o material.', guiao)
        self.assertNotIn('escreve-se aqui', guiao)
        self.assertIn('Grelha /20 indicativa: o «cocheiro», individual', guia)
        self.assertNotIn('de cada aluno, individual', guia)
        self.assertIn('Boa pergunta para a turma: o sítio onde está é uma prova ou só uma pista mais forte?', guia)
        self.assertNotIn('o que prova o sítio', guia)
        # 01/11/2026: com o cartão «O método» na posição 2, o vídeo de Herman passa a cartão 8
        self.assertIn('projeta-se com legendas no cartão 8;', guia)
        self.assertNotRegex(guia, r'a partir do cartão \d')
        self.assertRegex((PILOTO / 'docente/index.html').read_text('utf-8'), r'com legendas no leitor\. <a href="https://www\.youtube\.com/watch\?v=ubEadhXWwV4">Abrir no YouTube</a>\.</p>')
        self.assertNotIn('a lição inteira', guia)
        # o guia copia o cartão «Na aula»
        self.assertIn('Cada um regista os seus factos, um por nota;', guia)

    def test_regras_de_desenho(self):
        lab = (ROOT / 'assets/licoes/laboratorio.css').read_text('utf-8')
        self.assertIn('.licao-laboratorio .jogo .tit:not(.cartaz){font-size:1.3125rem;text-wrap:balance}', lab)
        entrada = (PILOTO / 'index.html').read_text('utf-8')
        self.assertIn('@media (min-width:1080px){html:not(.em-projecao) .ideias .gesto .ops{grid-template-columns:minmax(0,1fr)}}', entrada)
        self.assertIn('@media (max-width:599px){html.em-projecao .ideias h2.sessoes-t{font-size:2.5rem}html.em-projecao .ideias .porta h3{font-size:2rem}', entrada)
        for rel in ('index.html', 'guiao/index.html', 'docente/index.html'):
            self.assertIn('@media (min-width:768px){.ideias main{padding-left:24px;padding-right:24px;max-width:1248px}}', (PILOTO / rel).read_text('utf-8'), rel)


class SextaRevisao(unittest.TestCase):
    """30/10/2026: as correções da sexta revisão (01/11): a regência de «responder a» no auto de observação (revisor de pt-PT) e
    as regras de desenho do diretor de arte que se podem confirmar sem navegador (as medidas estão em tests/browser_ideias.cjs,
    secção 10)."""

    def test_texto_do_revisor(self):
        guiao = L.visivel((PILOTO / 'guiao/index.html').read_text('utf-8'))
        guia = L.visivel((PILOTO / 'docente/index.html').read_text('utf-8'))
        # o campo do guião e o critério da grelha que o avalia dizem o mesmo
        self.assertIn('A pergunta a que o lugar não responde:', guiao)
        self.assertIn('A pergunta a que o lugar não responde', guia)
        for t in (guiao, guia):
            self.assertNotIn('pergunta que o lugar', t)

    def test_regras_de_desenho(self):
        entrada = (PILOTO / 'index.html').read_text('utf-8')
        self.assertIn('@media (min-width:960px) and (max-width:1099px){html.em-projecao .ideias .topo{grid-template-areas:"abre proximo" "abre gesto" "atol gesto" "cap gesto";grid-template-rows:auto auto auto 1fr}'
                      'html.em-projecao .ideias .topo .atol figcaption{align-self:start;margin:8px 0 0}}', entrada)
        self.assertIn('@media (min-width:380px) and (max-width:469px){html.em-projecao .ideias .gesto .ops{grid-template-columns:minmax(0,1fr)}}', entrada)
        # «sessão N» inseparável no botão: no HTML («Começar») e no script que o reescreve («Continuar» e «Rever»)
        self.assertIn('data-p-botao href="sessao-01/">Começar a sessão\u00a01\u00a0→</a>', entrada)
        self.assertIn('b.textContent="Continuar na sessão\\u00a0"+prox.getAttribute("data-n")+"\\u00a0→"', entrada)
        self.assertIn('b2.textContent="Rever a sessão\\u00a0"+u.li.getAttribute("data-n")+"\\u00a0→"', entrada)
        self.assertNotIn('Começar a sessão 1', entrada)


class Metodo(unittest.TestCase):
    """01/11/2026: o método de Young assumido à cabeça, passo a passo (encargo do docente de 01/11: «Young é demasiado
    omnipresente»; o método fica como espinha, apresentado uma vez, e depois trabalha sem se anunciar). Guarda a regra nova: o
    bloco «O método» na entrada, logo abaixo do título, com os cinco passos numa lista numerada; «Passo N de 5» em cada sessão
    (na lista da entrada, no rótulo da região «A seguir», no «Abre», na marca da casca, no <title>, no último cartão, no guião e
    no guia); a apresentação de Young num cartão próprio na sessão 1; e o nome de Young só onde o método fala (no máximo três vezes
    em cada sessão, contando a fonte no menu). As medidas no navegador estão em tests/browser_ideias.cjs, secção 11."""

    PASSOS = ['Juntar material', 'Trabalhar o material', 'Largar', 'A ideia aparece', 'Dar forma e pôr à prova']

    def licoes(self):
        return [json.loads(p.read_text('utf-8')) for p in FONTES]

    def young(self, d):
        # o nome em todo o texto que o aluno pode ver na sessão: os cartões (também o p2) e o menu, com as fontes
        cartoes = sum(len(re.findall(r'Young', ' '.join(L.textos(c)))) for c in d['cartoes'])
        s = (ROOT / d['saida']).read_text('utf-8')
        menu = re.search(r'<div class="casca-menu".*?</div></div>', s, re.S).group(0)
        return cartoes, len(re.findall(r'Young', L.visivel(menu)))

    def test_bloco_o_metodo_na_entrada(self):
        s = (PILOTO / 'index.html').read_text('utf-8')
        abre = re.search(r'<header class="abre">(.*?)</header>', s, re.S).group(1)
        # logo abaixo do título: o bloco é o que vem a seguir à frase de abertura, dentro da abertura
        self.assertRegex(abre, r'<h1>Ideias</h1><p class="sub">Como nasce uma ideia</p><p class="lead">[^<]*método de cinco passos[^<]*</p>'
                               r'<section class="metodo" aria-labelledby="metodo-t"><h2 id="metodo-t">O método</h2>')
        bloco = re.search(r'<section class="metodo".*?</section>', abre, re.S).group(0)
        texto = L.visivel(bloco)
        for frag in ('James Webb Young', 'publicitário norte-americano', 'A Technique for Producing Ideas (1940)', 'um livro de poucas páginas',
                     'Seguimos, passo a passo, o método', 'Há outros', 'escolhemos este por ser simples, claro e útil'):
            self.assertIn(frag, texto)
        self.assertIn('<i>A Technique for Producing Ideas</i>', bloco)  # título de obra em itálico
        # 01/11/2026: (correção 2 do método, revisor de pt-PT) «Há outros;» lia-se também como «há outros livros» (o nome mais perto é
        # «um livro de poucas páginas»): a frase diz «métodos», como o encargo pede (ponto 1)
        self.assertIn('Há outros métodos; escolhemos este por ser simples, claro e útil.', texto)
        # 01/11/2026: (correção 2 do método, diretor de arte) o bloco com a largura da coluna, para o filete acabar onde acabam o título,
        # a frase de abertura e a imagem (com 34 em, a 17 px, acabava a meio dela a 1366 e 1440 px); o parágrafo continua com 34 em
        self.assertIn('.ideias .metodo{border-top:2px solid var(--tinta);padding-top:8px;margin:0 0 20px;max-width:none}', s)
        self.assertIn('.ideias .abre .info,.ideias .topo .atol figcaption{max-width:34em}', s)
        self.assertEqual(re.findall(r'<li><b>(\d)</b> ([^<]+)</li>', bloco), [(str(n), t) for n, t in enumerate(self.PASSOS, 1)])
        self.assertEqual(I.PASSOS, self.PASSOS)
        # a linha de informação antiga (o livro e Holmes «como guia») deu lugar ao bloco
        self.assertNotIn('como guia', L.visivel(abre))
        # o passo também no rótulo da região «A seguir» («Começa aqui: passo 1 de 5»), que o script troca com o progresso
        # 01/11/2026: (correção 1 do método, diretor de arte) «passo 1 de 5» inseparável, com espaços duros, no rótulo inicial, no
        # data-passo das sessões prontas e na sessão em preparação que o script escreve (antes partia-se dentro do passo)
        self.assertIn('<p class="kicker"><span data-p-k>Começa aqui</span><span data-p-passo>: passo\u00a01\u00a0de\u00a05</span></p>', s)
        self.assertEqual(re.findall(r'data-passo="([^"]*)"', s), ['passo\u00a01\u00a0de\u00a05'] * 2)
        self.assertIn('q("[data-p-passo]").textContent=": passos\u00a01\u00a0e\u00a02\u00a0de\u00a05";', s)
        # 01/11/2026: (correção 1 do método, diretor de arte) a lista dos cinco passos em grelha, para nenhum ficar sozinho numa linha:
        # um por linha abaixo de 600 px, três mais dois a partir de 600 px (as medidas estão em browser_ideias.cjs, secção 11)
        self.assertIn('@media (max-width:599px){.ideias ol.passos-m{display:grid;grid-template-columns:max-content;row-gap:0}', s)
        self.assertIn('@media (min-width:600px){.ideias ol.passos-m{display:grid;grid-template-columns:repeat(3,max-content);column-gap:16px}}', s)
        self.assertIn('q("[data-p-passo]").textContent=": "+prox.getAttribute("data-passo");', s)

    def test_passo_n_de_5_em_cada_sessao(self):
        s = (PILOTO / 'index.html').read_text('utf-8')
        apoios = re.findall(r'<span class="apoio">(.*?)</span>', s)
        self.assertEqual(len(apoios), 7)
        for n, a in enumerate(apoios, 1):
            self.assertRegex(a, r'^(Passos? \d( e \d)? de 5: |Os cinco passos juntos\.)', f'sessão {n}')
        self.assertEqual([x.split(':')[0] for x in apoios[:6]], ['Passo 1 de 5', 'Passo 1 de 5', 'Passos 1 e 2 de 5', 'Passos 2 e 3 de 5', 'Passo 4 de 5', 'Passo 5 de 5'])
        # 01/11/2026: (correção 2 do método, diretor de arte) o passo escrito em cada porta é o das sessões que estão dentro dela (antes,
        # Ver dizia «Passos 1 e 2» sobre duas sessões do passo 1 e Treinar «Passos 2 e 3» sobre as sessões dos passos 1 a 3); a sessão
        # de síntese («Os cinco passos juntos») não tem um passo só
        def passos(t):
            m = re.match(r'Passos? (\d)(?: (e|a) (\d))?(?: de 5)?:', t)
            self.assertIsNotNone(m, t)
            a, b = int(m.group(1)), int(m.group(3) or m.group(1))
            return set(range(a, b + 1)) if m.group(2) != 'e' else {a, b}
        portas = [(pid, re.sub(r'<[^>]+>', '', t), ss) for pid, t, ss in  # sem as <span class="nq"> que seguram «trabalhá-lo»
                  re.findall(r'<div class="porta-corpo" id="pc-(\w+)"><p class="apoio-porta">(.*?)</p><ol class="sessoes">(.*?)</ol></div>', s, re.S)]
        # 01/11/2026: (correção 3 do método, revisor de pt-PT) a porta Treinar diz «juntar o material geral», para os três elementos da
        # enumeração serem infinitivos paralelos («juntar», «trabalhá-lo», «largá-lo»); antes, «o material geral» ficava sem a ação
        self.assertEqual([(pid, t) for pid, t, _ in portas], [('ver', 'Passo 1: juntar material, com os olhos e até ao fundo.'),
                                                              ('treinar', 'Passos 1 a 3: juntar o material geral, trabalhá-lo na cabeça e, depois, largá-lo.'),
                                                              ('criar', 'Passos 4 e 5: a ideia aparece, ganha forma e vai a quem a pode criticar.')])
        for pid, t, sessoes in portas:
            dentro = [a for a in re.findall(r'<span class="apoio">(.*?)</span>', sessoes) if not a.startswith('Os cinco passos juntos')]
            self.assertTrue(dentro, pid)
            self.assertEqual(passos(t), set().union(*(passos(a) for a in dentro)), pid)
        for d in self.licoes():
            pag = (ROOT / d['saida']).read_text('utf-8')
            abre, ultimo = d['cartoes'][0]['html'], d['cartoes'][-1]['html']
            # o «Abre» situa o método: o passo de hoje e os cinco passos numa linha, com o de hoje marcado com texto
            self.assertIn('<div class="metodo-linha"><p><b>Passo 1 de 5: juntar material', abre, d['id'])
            linha = re.search(r'<ol class="passos-m" aria-label="Os cinco passos do método">(.*?)</ol>', abre).group(1)
            self.assertEqual(re.findall(r'<b>(\d)</b> ([^<]+?)(?: <span|</li>)', linha), [(str(n), t) for n, t in enumerate(self.PASSOS, 1)])
            self.assertEqual(linha.count('class="hoje" aria-current="step"'), 1)
            self.assertIn('<li class="hoje" aria-current="step"><b>1</b> Juntar material <span class="hoje-t">hoje</span></li>', linha)
            # o último cartão diz que passo se fez e o que vem a seguir
            # 01/11/2026: (correção 1 do método, revisor de pt-PT) na sessão 2, «Passo 1 de 5: feito» dava o passo por acabado com o
            # material geral ainda por juntar (sessão 3): passa a «Passo 1 de 5: falta o material geral»
            self.assertRegex(L.visivel(ultimo), r'(Fizeste o passo 1 de 5|Passo 1 de 5: falta o material geral)', d['id'])
            self.assertRegex(L.visivel(ultimo), r'(Para a sessão 2 , o mesmo passo|passo 2 de Young)', d['id'])
            # a marca da casca e o <title>
            self.assertIn('<span class="c-marca-p">Passo 1 de 5</span>', pag)
            self.assertIn('(passo 1 de 5) | Ideias | Laboratório | Lente</title>', pag)
        css = (ROOT / 'assets/licoes/laboratorio.css').read_text('utf-8')
        self.assertIn('.licao-laboratorio .jogo .ler ol.passos-m li.hoje{', css)
        self.assertIn('@media (max-width:429px){.licao-laboratorio .c-marca-p{position:absolute', css)
        # 01/11/2026: (correção 1 do método, diretor de arte) a linha dos passos em grelha também abaixo de 600 px (um por linha), e
        # «hoje» como rótulo de estado do sistema (13 px, 0,14 em), não abaixo da letra mínima
        self.assertIn('.licao-laboratorio .jogo .ler ol.passos-m{list-style:none;display:grid;grid-template-columns:max-content;', css)
        self.assertIn('.licao-laboratorio .jogo .ler ol.passos-m .hoje-t{font-size:.8125rem;letter-spacing:.14em;', css)
        # 01/11/2026: (correção 2 do método, diretor de arte) a lista dos cinco passos do «Abre» com o desenho da lista da entrada: o
        # nome a 15 px e o número em Bebas Neue, a 18 px abaixo de 600 px e a 21 px a partir daí (as medidas, ao lado das da entrada, em
        # browser_ideias.cjs, secção 11)
        self.assertIn('.licao-laboratorio .jogo .ler ol.passos-m li{margin:0;padding:2px 0 3px;font:400 .9375rem/1.2 Arial,Helvetica,sans-serif;', css)
        self.assertIn('.licao-laboratorio .jogo .ler ol.passos-m li b{font:400 1.125rem/1 "Bebas Neue","Arial Narrow",Arial,sans-serif;', css)
        self.assertIn('@media (min-width:600px){.licao-laboratorio .jogo .ler ol.passos-m li b{font-size:1.3125rem}}', css)
        self.assertIn('.ideias ol.passos-m b{font:400 1.3125rem/1 "Bebas Neue","Arial Narrow",Arial,sans-serif}', s)
        # 01/11/2026: (correção 4 do método, diretor de arte) a linha do método com a medida do texto corrido (33 em, até 75 carateres);
        # o filete continua à largura dos cartões de ler (as linhas medidas no Chromium em browser_ideias.cjs, secção 11)
        self.assertIn('.licao-laboratorio .jogo .ler .metodo-linha p{max-width:33em}', css)
        self.assertIn('.licao-laboratorio .jogo .ler .metodo-linha{max-width:var(--medida-ler)}', css)
        # o guião diz o passo no cabeçalho de cada sessão; o guia, na sequência e em cada sessão
        g = (PILOTO / 'guiao/index.html').read_text('utf-8')
        # 01/11/2026: (correção 1 do método, diretor de arte, revisor e verificador) o cabeçalho diz «Passo N de 5» e o nome do passo
        # (encargo, ponto 3), com as palavras do «Abre» de cada sessão; antes, a sessão 2 dizia «o material específico»
        self.assertEqual(re.findall(r'<p class="passo-g">([^<]*)</p>', g), ['Passo 1 de 5: juntar material, com os olhos', 'Passo 1 de 5: juntar material, até ao fundo'])
        self.assertIn('Passo 1 de 5: juntar material, até ao fundo.', L.visivel(self.licoes()[1]['cartoes'][0]['html']))
        guia = (PILOTO / 'docente/index.html').read_text('utf-8')
        # 01/11/2026: (correção 3 do método, verificador) a sequência do guia diz os passos de cada porta como a entrada
        self.assertIn('O passo 1 do método leva a Ver; os passos 1 a 3, a Treinar; os passos 4 e 5, a Criar.', L.visivel(guia))
        self.assertNotIn('Os passos 1 e 2 do método levam a Ver', guia)
        self.assertEqual(len(re.findall(r'data-r="Passo">(?:Passos? \d( e \d)? de 5|Os cinco passos juntos)', guia)), 7)
        self.assertEqual(guia.count('<b>O passo.</b> Passo 1 de 5:'), 2)

    def test_apresentacao_de_young_na_sessao_1(self):
        d1, d2 = self.licoes()
        c = d1['cartoes'][1]
        self.assertEqual((c['t'], c['rot']), ('ler', 'O método'))
        t = L.visivel(c['html'])
        for frag in ('James Webb Young foi um publicitário norte-americano', 'Em 1940 publicou A Technique for Producing Ideas', 'um livro de poucas páginas',
                     'Há outros métodos', 'seguimos este por ser simples e claro, por fazer sentido e por ajudar de facto', 'usares por tua conta'):
            self.assertIn(frag, t)
        # a frase de Young que resume o método, conferida letra a letra na tradução nossa (capítulo «Ideias São Novas Combinações»)
        self.assertIn('<blockquote><p>«Esta técnica intelectual consiste em cinco passos. Tenho a certeza de que todos, um por um, são reconhecíveis.»</p></blockquote>'
                      '<p class="fonte">James Webb Young, <i>A Technique for Producing Ideas</i>, capítulo «Ideias São Novas Combinações». Tradução nossa.</p>', c['html'])
        # 01/11/2026: (correção 1 do método, revisor de pt-PT) na fonte, o título como no texto do cartão, na entrada, no guia e no menu
        # de fontes (antes, «Uma Técnica para Produzir Ideias»); o outro título não aparece em nenhum cartão das duas sessões
        for d in (d1, d2):
            self.assertNotIn('Uma Técnica para Produzir Ideias', ' '.join(' '.join(L.textos(x)) for x in d['cartoes']), d['id'])
        # o cartão novo muda a ordem: a versão da sessão 1 sobe; a sessão 2 não ganha cartão e fica com a versão
        self.assertEqual((d1['versao'], d2['versao']), ('2026-11-01-1', '2026-10-31-1'))
        self.assertEqual((d1['chave'], d2['chave']), ('epi-lab-ideias-s01', 'epi-lab-ideias-s02'))

    def test_respostas_certas_nao_mudam(self):
        # as perguntas, as respostas certas e a ordem dos cartões de fazer, como em d043fa1
        certas = lambda d: [(c['g'], c['t'], c.get('c'), c.get('v'), c.get('certas'), len(c.get('o', [])), len(c.get('pares', [])), len(c.get('passos', [])),
                             [l['c'] for l in c.get('lacunas', [])]) for c in d['cartoes'] if c['t'] in L.TIPOS_FAZER]
        d1, d2 = self.licoes()
        self.assertEqual(certas(d1), [('atol', 'escolha', 0, None, None, 3, 0, 0, []), ('watson', 'escolha', 0, None, None, 3, 0, 0, []), ('frase', 'completar', None, None, None, 0, 0, 0, [0, 0]),
                                      ('resumo', 'emparelhar', None, None, None, 0, 4, 0, []), ('invisivel', 'vf', None, True, None, 0, 0, 0, []), ('cordao', 'mapa', 0, None, None, 4, 0, 0, []),
                                      ('medalha', 'mapa', 0, None, None, 4, 0, 0, []), ('estatuto', 'emparelhar', None, None, None, 0, 4, 0, []), ('confirmar', 'escolha', 0, None, None, 3, 0, 0, []),
                                      ('superficie', 'sublinhar', None, None, [9, 10, 11, 12, 13], 0, 0, 0, []), ('cartoes', 'escolha', 0, None, None, 3, 0, 0, []),
                                      ('aalto', 'vf', None, True, None, 0, 0, 0, []), ('metodo', 'ordenar', None, None, None, 0, 0, 4, [])])
        self.assertEqual(certas(d2), [('young', 'escolha', 0, None, None, 3, 0, 0, []), ('testemunha', 'emparelhar', None, None, None, 0, 4, 0, []), ('palavra', 'escolha', 0, None, None, 3, 0, 0, []),
                                      ('leitura', 'escolha', 0, None, None, 3, 0, 0, []), ('cedo', 'sublinhar', None, None, [4, 5, 6], 0, 0, 0, []), ('banal', 'vf', None, False, None, 0, 0, 0, []),
                                      ('deduzo', 'escolha', 0, None, None, 3, 0, 0, []), ('fila', 'escolha', 0, None, None, 3, 0, 0, []), ('exata', 'vf', None, False, None, 0, 0, 0, []),
                                      ('materias', 'completar', None, None, None, 0, 0, 0, [0, 0]), ('prova', 'escolha', 0, None, None, 3, 0, 0, []), ('viagem', 'ordenar', None, None, None, 0, 0, 4, [])])

    def test_young_so_onde_o_metodo_fala(self):
        d1, d2 = self.licoes()
        for d in (d1, d2):
            cartoes, menu = self.young(d)
            self.assertLessEqual(cartoes, 2, d['id'])
            self.assertLessEqual(cartoes + menu, 3, d['id'])
        # sessão 1: só na apresentação (o nome e a fonte da citação); sessão 2: na fonte da citação do cocheiro e na passagem para
        # o passo 2, no «Para levar»
        onde = lambda d: [(i, c.get('rot') or c.get('g')) for i, c in enumerate(d['cartoes'], 1) if 'Young' in ' '.join(L.textos(c))]
        self.assertEqual(onde(d1), [(2, 'O método')])
        self.assertEqual(onde(d2), [(3, 'Ler'), (19, 'Para levar')])
        self.assertIn('passo 2 de Young', L.visivel(d2['cartoes'][-1]['html']))
        # nos retornos, o método fala sem se anunciar
        cartoes1 = {c.get('g'): c for c in d1['cartoes']}
        self.assertEqual(cartoes1['cartoes']['fe'][2], 'O método não pede que decores. Escrever serve para pensar e para ver o que ainda não se sabe.')
        # 01/11/2026: (correção 1 do método, verificador de factos) o passo 5 do método é levar a ideia a quem a critica: quem não fala
        # de mostrar trabalho é o conselho dos cartões; e a citação do atol diz de onde vem («diz o livro»), sem o nome
        self.assertEqual(cartoes1['cartoes']['fe'][1], 'O conselho dos cartões não fala de mostrar trabalho a ninguém. Fala do que a escrita faz a quem escreve.')
        self.assertIn('mas, diz o livro, «resulta dos esforços ocultos de inúmeros e invisíveis construtores de coral»', cartoes1['atol']['f'])
        # as páginas do piloto: a entrada (o bloco e a saída para a Biblioteca), o guião (nenhuma) e o guia (a razão do método,
        # onde o nome volta e as fontes das duas sessões)
        vis = lambda rel: L.visivel(re.sub(r'<(script|style|title)[^>]*>.*?</\1>', ' ', (PILOTO / rel).read_text('utf-8'), flags=re.S))
        self.assertEqual(vis('index.html').count('Young'), 2)
        self.assertEqual(vis('guiao/index.html').count('Young'), 0)
        self.assertLessEqual(vis('docente/index.html').count('Young'), 4)

    def test_guia_abre_com_o_metodo(self):
        guia = (PILOTO / 'docente/index.html').read_text('utf-8')
        corpo = guia[guia.index('<main'):]
        self.assertLess(corpo.index('<section class="sessao" id="metodo"><h2>Porque seguimos um método</h2>'), corpo.index('id="antes"'))
        self.assertIn('<li><a href="#metodo">Porque seguimos um método</a></li>', guia)
        sec = re.search(r'<section class="sessao" id="metodo">.*?</section>', guia, re.S).group(0)
        t = L.visivel(sec)
        # 01/11/2026: (revisor de pt-PT, volta 4 do método) a frase do guia com antecedente explícito, como na entrada e no cartão 2
        for frag in ('adota como espinha', 'Há outros métodos; escolhemos este por ser simples e claro', 'simples e claro, por fazer sentido e por ajudar de facto', 'depois o usem por conta própria',
                     'Na primeira aula. Cinco minutos', 'os cinco passos no quadro', 'Onde o nome volta.', 'só na passagem de um passo para o outro'):
            self.assertIn(frag, t)
        # 01/11/2026: (correção 4 do método, revisor de pt-PT) a frase antiga, sem antecedente, não volta
        self.assertNotIn('Não é o único método', t)
        self.assertEqual(re.findall(r'<li><b>([^<]+)</b>:', sec), self.PASSOS)
        # os números dos cartões no guia acertam com a lição (o vídeo e o resumo com a ligação)
        d1 = self.licoes()[0]
        video = next(i for i, c in enumerate(d1['cartoes'], 1) if 'data-yt=' in (c.get('html') or ''))
        liga = next(i for i, c in enumerate(d1['cartoes'], 1) if c.get('liga'))
        tg = L.visivel(guia)
        self.assertIn(f'projeta-se com legendas no cartão {video};', tg)
        self.assertIn(f'(a ligação aparece no retorno do cartão {liga})', tg)
        self.assertIn('«O método» (cartão 2)', tg)
        self.assertEqual(d1['cartoes'][1]['rot'], 'O método')

if __name__ == '__main__':
    unittest.main()
