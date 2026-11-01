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
            self.assertIn('<title>' + d['titulo'].replace('?', '?') + ' | Ideias | Laboratório | Lente</title>', s)

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
        for p, (n, fazer) in zip(FONTES, [(20, 13), (19, 12)]):
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
            self.assertIn('<span class="c-marca-t">Ideias</span></a>', (ROOT / d['saida']).read_text('utf-8'))
        for p in sorted((ROOT / 'tools/licoes').glob('cidadania-*.json')):
            d = json.loads(p.read_text('utf-8'))
            self.assertNotIn('c-marca-t', (ROOT / d['saida']).read_text('utf-8'), p.name)
        css = (ROOT / 'assets/licoes/laboratorio.css').read_text('utf-8')
        self.assertIn('.licao-laboratorio .c-marca-t{position:absolute', css)

    def test_tema_do_young_na_barra(self):
        self.assertIn('</ol><span data-appearance-control></span></nav>', BIB.read_text('utf-8'))


if __name__ == '__main__':
    unittest.main()
