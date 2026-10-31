"""Cidadania M2: dez sessões no molde do M1 (28/10/2026, plano em docs/pedagogia/plano-cidadania-m2.md).

Abertura com uma imagem, pergunta curta e «Começar»; cinco passos (Recupera, Vê, Decide, Faz, Leva); Decide sem
ecrã; Faz fecha na casa da sessão do mapa do Contra-feed (dez casas, sem pesos novos); Leva em papel; cartões de
obra nas sessões 01 a 09; chave de progresso nova; escrita do Lente; ligações locais; correções dos «Riscos»;
e o M1 igual a origin/main, byte a byte.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import importlib
import json
import re
import subprocess
import sys
import unittest

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'tools'))
molde = importlib.import_module('cidadania_m2_molde')
correcoes = importlib.import_module('cidadania_m2_correcoes')
CHAVE = 'lente-cidadania-m2-sessoes-v1'
LENTE = 'https://pedrohfernandes-klk.github.io/lente/'


class Pagina(HTMLParser):
    """Texto visível (sem scripts nem estilos), ids e referências de uma página."""
    def __init__(self, s):
        super().__init__()
        self.out, self.ids, self.refs, self.imgs, self.skip = [], [], [], [], 0
        self.feed(s)

    def handle_starttag(self, t, attrs):
        a = dict(attrs)
        if t in ('script', 'style'):
            self.skip += 1
        if 'id' in a:
            self.ids.append(a['id'])
        for k in ('href', 'src'):
            if a.get(k):
                self.refs.append(a[k])
        if t == 'img':
            self.imgs.append(a.get('src'))

    def handle_endtag(self, t):
        if t in ('script', 'style'):
            self.skip -= 1

    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)

    @property
    def texto(self):
        return re.sub(r'\s+', ' ', ' '.join(self.out))


def ler(p):
    return (R / p).read_text('utf-8')


def sessao(n):
    return ler(f'cidadania/m2/sessoes/{n:02}/index.html')


def passos(s):
    return re.split(r'<section class="c10-stage" id="momento-', s)[1:]


def palavras(t):
    return {w for w in re.findall(r'[a-záàâãéêíóôõúç]{5,}', t.lower())}


def ensinado(s):
    """O Vê, o Decide e o Faz de uma sessão, sem o mapa das dez casas."""
    p = passos(s)
    corpo = ''.join(x.split('<div class="c10-step-body">', 1)[1] for x in p[1:4])
    return re.sub(r'<ol class="c10-mapa".*?</ol>', '', corpo, flags=re.S)


SESSOES = [f'cidadania/m2/sessoes/{n:02}/index.html' for n in range(1, 11)]
GUIA = 'cidadania/m2/sessoes/index.html'


class Molde(unittest.TestCase):
    def test_abertura_uma_imagem_pergunta_comecar(self):
        for n in range(1, 11):
            s = sessao(n)
            capa = s[s.index('data-session-intro'):s.index('data-session-flow')]
            # 30/10/2026: reciclagem dos gigantes (decisão do docente).
            self.assertEqual(capa.count('<img '), 0 if n in molde.CASOS_RECICLADOS else 1, n)
            self.assertIn('class="c10-deck"', capa)
            self.assertIn('data-start>Começar</a>', capa)
            # 28/10/2026 (revisão de design): o material que se observa fica à vista, no próprio material, em vez de atrás
            # de uma ligação. Além da imagem da abertura, só entram as que o Vê declara (o tear na 01, A e B na 05).
            dados = molde.SESSOES[n - 1]
            esperadas = {molde.IMAGENS[dados['imagem']]['src']}
            for m in dados['ve']:
                if m.get('imagem'):
                    esperadas.add(molde.IMAGENS[m['imagem']]['src'])
                if m['tipo'] == 'par':
                    esperadas |= {molde.LISBOA_1907['a']['src'], molde.LISBOA_1907['b']['src']}
            self.assertEqual({src.replace('../', '') for src in Pagina(s).imgs}, esperadas, n)
            # a imagem da abertura carrega já (está acima da dobra); as outras esperam
            if n not in molde.CASOS_RECICLADOS:
                self.assertRegex(capa, r'<img [^>]*loading="eager" fetchpriority="high"', n)

    def test_cinco_passos_pela_ordem(self):
        for n in range(1, 11):
            s = sessao(n)
            self.assertEqual(re.findall(r' data-stage data-label="([^"]+)"', s), molde.PASSOS, n)
            self.assertEqual(re.findall(r'data-stage-link><b>\d\d</b><span>([^<]+)</span>', s), molde.PASSOS, n)
            self.assertIn('data-prev hidden>← Anterior', s)
            self.assertIn('data-next hidden>Seguinte →', s)
            self.assertIn(f'data-session="{n:02}"', s)

    def test_recupera_duas_conceptuais_e_uma_pessoal(self):
        for n, s in enumerate(molde.SESSOES, 1):
            r = s['recupera']
            self.assertEqual(len(r), 3, n)
            self.assertEqual([a is None for _, a in r], [False, False, True], n)
            for q, a in r:
                self.assertTrue(q.endswith('?'), q)
                if a:
                    self.assertNotIn('?', a, q)

    def test_recupera_responde_com_a_sessao_anterior(self):
        # A resposta de «Confirmar» vem da sessão anterior: as palavras de cada resposta estão nessa página.
        # 28/10/2026 (revisão de engenharia): só conta o que a sessão anterior ensina (Vê, com o cartão da obra, Decide,
        # com «Comparar razões», e Faz), sem topo, rodapé, barra dos passos nem o mapa das dez casas.
        for n in range(2, 11):
            anterior = palavras(Pagina(ensinado(sessao(n - 1))).texto)
            for q, a in molde.SESSOES[n - 1]['recupera']:
                if a:
                    p = palavras(a)
                    self.assertGreaterEqual(len(p & anterior) / len(p), .75, (n, a, sorted(p - anterior)))

    def test_decide_sem_ecra_faz_casa_leva_em_papel(self):
        for n in range(1, 11):
            p = passos(sessao(n))
            self.assertEqual(len(p), 5)
            self.assertEqual(p[0].count('<li><p>'), 3, n)
            self.assertIn('data-mark="Sem ecrã"', p[2], n)
            self.assertIn('Primeiro, em silêncio', p[2])
            self.assertIn('data-feedback><summary>Comparar razões', p[2])
            self.assertIn('Rever com outra pessoa', p[3], n)
            self.assertIn(f'<b>Guardar</b><span>Casa {n} do mapa do Contra-feed: ', p[3], n)
            self.assertIn('data-mark="Em papel"', p[4], n)
            self.assertEqual(p[4].count('class="c10-exit-q"'), 1, n)
            self.assertEqual(re.search(r'<ul class="c10-checks">(.*?)</ul>', p[4]).group(1).count('<li>'), 3, n)
            self.assertEqual(p[4].count('data-session-done'), 1, n)

    def test_mapa_do_contra_feed_em_dez_casas(self):
        self.assertEqual(len(molde.CASAS), 10)
        for n in range(1, 11):
            m = re.search(r'<ol class="c10-mapa"[^>]*>(.*?)</ol>', sessao(n), re.S).group(1)
            casas = re.findall(r'<li([^>]*)><b>(\d+)</b>', m)
            self.assertEqual([int(c) for _, c in casas], list(range(1, 11)))
            self.assertEqual([i for i, (a, _) in enumerate(casas, 1) if 'aria-current="step"' in a], [n])
        g = ler(GUIA)
        tabela = re.search(r'<caption>As dez casas, uma por sessão</caption>(.*?)</table>', g, re.S).group(1)
        self.assertEqual(tabela.count('<tr><th scope="row">'), 10)
        self.assertIn('não cria entregas nem pesos', g)

    def test_pesos_sao_os_do_contra_feed(self):
        cf = ler('cidadania/contra-feed/index.html')
        pesos = re.findall(r'<td[^>]*>(\d+%)</td>', re.search(r'<table>.*?</table>', cf, re.S).group(0))
        self.assertEqual([p for _, p, _, _ in molde.INSTRUMENTOS], pesos)
        self.assertEqual(sum(int(p[:-1]) for _, p, _, _ in molde.INSTRUMENTOS), 100)
        g = ler(GUIA)
        for nome, peso, _, _ in molde.INSTRUMENTOS:
            self.assertIn(nome, g)

    def test_tempos(self):
        self.assertEqual(molde.TEMPOS, [10, 30, 30, 90, 20])
        self.assertEqual(molde.TEMPOS_MOSTRA, [5, 10, 20, 125, 20])
        self.assertEqual(sum(molde.TEMPOS), 180)
        self.assertEqual(sum(molde.TEMPOS_MOSTRA), 180)
        self.assertEqual([n for n, s in enumerate(molde.SESSOES, 1) if s.get('mostra')], [10])
        g = ler(GUIA)
        s10 = g[g.index('id="sessao-10"'):]
        self.assertEqual(re.findall(r'<span>(\d+) min</span>', s10)[:5], ['5', '10', '20', '125', '20'])

    def test_cartoes_de_obra(self):
        self.assertEqual(sorted(molde.OBRAS), list(range(1, 10)))
        for n, o in molde.OBRAS.items():
            self.assertLessEqual(len(o['contexto'].split()), 100, n)
            self.assertEqual(len(o['ligacoes']), 2, n)
            self.assertTrue(o['acesso'] and o['razao'] and o['discordante'], n)
            self.assertTrue(o['pergunta'].endswith('?'), n)
            if o.get('protegida'):
                self.assertNotIn('citacao', o, n)  # obras protegidas: descritas, nunca citadas
            for _, alvo in o['ligacoes']:
                caminho = alvo.split('#')[0]
                self.assertTrue((R / caminho / 'index.html').exists(), (n, alvo))
            s = sessao(n)
            # 30/10/2026: reciclagem dos gigantes (decisão do docente).
            self.assertEqual(s.count('class="c10-obra"'), 0 if n in molde.CASOS_RECICLADOS else 1, n)
            if n in molde.CASOS_RECICLADOS:
                self.assertIn('id="caso-reciclado"', s)
                self.assertIn('Ler o relato em português', s)
            self.assertIn('Outra leitura', s)
        self.assertNotIn('class="c10-obra"', sessao(10))

    def test_escrita(self):
        # pt-PT AO90, «tu», «docente»; sem travessão, sem «·» no texto, sem «professor», «jogar», «ficha» nem «folha».
        textos = {p: Pagina(ler(p)).texto for p in SESSOES + [GUIA]}
        indice = ler('cidadania/m2/index.html')
        textos['bloco do índice'] = Pagina(indice[indice.index('<!-- sessoes-m2 -->'):indice.index('<!-- /sessoes-m2 -->')]).texto
        for n in range(1, 11):
            a = ler(f'cidadania/m2/aulas/{n:02}/index.html')
            textos[f'linha da etapa {n:02}'] = Pagina(a[a.index('<!-- sessoes-m2 -->'):a.index('<!-- /sessoes-m2 -->')]).texto
        for p, t in textos.items():
            baixo = t.lower()
            self.assertNotIn('—', t, p)
            self.assertNotIn('·', t, p)
            for w in ('professor', 'jogar', 'joga ', 'ficha', 'folha', 'pedrohfernandes'):
                self.assertNotIn(w, baixo, (p, w))
            # «tu» para cada aluno; no plural, «vocês» é o plural de «tu» em português europeu
            self.assertNotRegex(baixo, r'\bvocê\b', p)
        self.assertIn('docente', textos[GUIA])

    def test_dados_sem_regras_proibidas(self):
        # O que vai para o guia e para as páginas, incluindo o que só o docente lê.
        def textos(x):
            if isinstance(x, str):
                if ' ' in x or '/' not in x:  # os caminhos e endereços não são texto visível
                    yield x
            elif isinstance(x, dict):
                for v in x.values():
                    yield from textos(v)
            elif isinstance(x, (list, tuple)):
                for v in x:
                    yield from textos(v)
        for t in textos([molde.SESSOES, molde.OBRAS, molde.CASAS, molde.DECISOES, molde.INSTRUMENTOS, molde.IMAGENS]):
            for w in ('—', '·', 'professor', 'jogar', 'ficha', 'folha'):
                self.assertNotIn(w, t.lower(), (w, t))

    def test_ligacoes_locais_e_ids(self):
        paginas = SESSOES + [GUIA, 'cidadania/m2/index.html', 'cidadania/index.html', 'docente/index.html', 'cidadania/m2/imagens/index.html', 'cidadania/m2/glossario/index.html']
        paginas += [f'cidadania/m2/aulas/{n:02}/index.html' for n in range(1, 11)] + ['cidadania/m2/aulas/index.html']
        for p in paginas:
            s = ler(p)
            pag = Pagina(re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', s, flags=re.S))
            ids = [i for i in pag.ids if i]  # o índice do M2 já tinha id="" em três artigos (origin/main)
            self.assertEqual(len(ids), len(set(ids)), p)
            for ref in pag.refs:
                u = urlsplit(ref)
                if ref.startswith('data:') or (u.scheme and not ref.startswith(LENTE)):
                    continue
                alvo = R / unquote(u.path.removeprefix('/lente/')) if u.scheme else ((R / p).parent / unquote(u.path) if u.path else R / p)
                if alvo.is_dir():
                    alvo = alvo / 'index.html'
                self.assertTrue(alvo.exists(), (p, ref))
                if u.fragment and alvo.suffix == '.html':
                    self.assertIn('id="' + unquote(u.fragment) + '"', alvo.read_text('utf-8'), (p, ref))

    def test_fontes_externas_ja_estao_no_lente(self):
        # Nenhum endereço externo sem conferência.
        # 28/10/2026 (revisão de engenharia): comparar com origin/main deixava de proteger depois da fusão (a própria
        # sessão passava a ser a sua fonte). Agora cada endereço tem de estar na lista explícita do molde
        # (FONTES_EXTERNAS); os marcados «lente» têm de existir no commit BASE (fixo), fora das sessões.
        externos = set()
        for p in SESSOES + [GUIA]:
            for ref in Pagina(ler(p)).refs:
                if ref.startswith('http') and not ref.startswith(LENTE):
                    externos.add(ref)
        self.assertEqual(sorted(externos - set(molde.FONTES_EXTERNAS)), [])
        for url, (_, origem) in molde.FONTES_EXTERNAS.items():
            if origem != 'lente':
                self.assertRegex(origem, r'\d{2}/\d{2}/\d{4}', url)  # aberto e conferido, com data
                continue
            r = subprocess.run(['git', 'grep', '-q', '-F', '-e', url, '-e', url.replace('&', '&amp;'), molde.BASE, '--', '*.html', ':!cidadania/m2/sessoes'], cwd=R)
            self.assertEqual(r.returncode, 0, url)

    def test_chave_nova_so_nas_sessoes_do_m2(self):
        for p in SESSOES + [GUIA]:
            self.assertIn('data-chave="' + CHAVE + '"', ler(p), p)
        indice = ler('cidadania/m2/index.html')
        self.assertIn('data-chave="' + CHAVE + '"', indice)
        self.assertIn('epi-cidadania-m2', indice)  # a chave antiga e o contador mantêm-se
        js = ler('assets/cidadania-sessoes-molde.js')
        self.assertIn('root.dataset.chave', js)
        self.assertEqual(re.findall(r'localStorage\.setItem\(([^,]+),', js), ['KEY'])
        for proibido in ('removeItem', 'localStorage.clear', 'epi-cidadania', 'lente-cidadania-m1'):
            self.assertNotIn(proibido, js)
        self.assertIn('if (projected) return false', js)
        # as chaves existentes continuam nos seus motores
        self.assertIn("KEY='lente-cidadania-m1-sessoes-v2'", ler('assets/cidadania-m1-sessoes.js'))

    def test_m1_igual_a_origin_main(self):
        # 28/10/2026 (revisão de engenharia): compara-se com a base comum deste ramo (git merge-base HEAD origin/main),
        # e não com origin/main, que muda com o tempo; sem origin/main local, o teste fica de fora, como em
        # test_videos_escolhidos.
        r = subprocess.run(['git', 'merge-base', 'HEAD', 'origin/main'], cwd=R, capture_output=True, text=True)
        if r.returncode:
            self.skipTest('sem origin/main local')
        base = r.stdout.strip()
        lista = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', base, 'cidadania/m1'], cwd=R).decode().split()
        # 30/10/2026: caminhos com barras normais, para correr também no Windows
        locais = sorted(p.relative_to(R).as_posix() for p in (R / 'cidadania/m1').rglob('*') if p.is_file())
        self.assertEqual(sorted(lista), locais)
        # 30/10/2026: pedido do docente (perguntas em português europeu, «Qual das perguntas…» e não «Qual pergunta…»): a
        # base passa pelas trocas de tools/trocas/lingua-perguntas-20261030.json antes de se comparar; depois da fusão a
        # base já as tem e a troca não muda nada. Tudo o resto continua igual, byte a byte.
        lingua = json.loads((R / 'tools/trocas/lingua-perguntas-20261030.json').read_text('utf-8'))
        for f in lista + ['assets/cidadania-m1-sessoes.css', 'assets/cidadania-m1-sessoes.js']:
            antes = subprocess.check_output(['git', 'show', base + ':' + f], cwd=R)
            for t in lingua:
                if t['ficheiro'] == f:
                    antes = antes.replace(t['antigo'].encode('utf-8'), t['novo'].encode('utf-8'))
            # 30/10/2026: normalizar só finais de linha; os geradores usam CRLF no Windows.
            self.assertEqual((R / f).read_bytes().replace(b'\r\n',b'\n'), antes.replace(b'\r\n',b'\n'), f)

    def test_etapas_indice_portal_e_docente(self):
        for n in range(1, 11):
            a = ler(f'cidadania/m2/aulas/{n:02}/index.html')
            self.assertEqual(a.count('cidadania/m2/sessoes/'), 1, n)
            self.assertIn(f'{LENTE}cidadania/m2/sessoes/{n:02}/', a)
        indice = ler('cidadania/m2/index.html')
        self.assertEqual(re.findall(r'data-session-card="(\d\d)"><a href="sessoes/(\d\d)/"', indice), [(f'{n:02}', f'{n:02}') for n in range(1, 11)])
        self.assertIn('href="' + LENTE + 'cidadania/m2/aulas/"', indice)
        self.assertIn('data-continue', indice)
        portal = ler('cidadania/index.html')
        self.assertIn('Dez sessões: ver as regras, pô-las à prova e criar um Contra-feed.', portal)
        self.assertIn('data-prog="m2">10 sessões<', portal)
        self.assertIn('href="../cidadania/m2/sessoes/"', ler('docente/index.html'))

    def test_decisoes_provisorias_no_guia(self):
        g = ler(GUIA)
        self.assertEqual(g.count('Decisão provisória '), 5)
        for t in ('individual, com revisão em pares', 'real, datado, tem duas fontes independentes', '5, 10, 20, 125 e 20 minutos',
                  'reserva escrita', 'Naufrágio', 'v120', 'v108'):
            self.assertIn(t, g)
        s06 = sessao(6)
        self.assertIn('lista aprovada pelo docente', s06)
        self.assertIn('sem menores nem pessoas privadas', s06)

    def test_videos(self):
        for n in range(1, 11):
            s = sessao(n)
            self.assertNotRegex(s, r'<iframe')
            self.assertNotIn('ver-para-fazer/v120', s)
            self.assertNotIn('ver-para-fazer/v108', s)
            self.assertNotIn('Naufrágio', s)
            self.assertEqual('youtube.com' in s, n == 2, n)
        s = sessao(2)
        for t in ('Antes de ver.', 'Depois de ver.', 'Sem vídeo', 'Opcional'):
            self.assertIn(t, s)

    def test_riscos_corrigidos(self):
        site = [p for p in R.rglob('*.html') if '.git' not in p.parts and 'node_modules' not in p.parts]
        for p in site:
            s = p.read_text('utf-8', errors='ignore')
            rel = str(p.relative_to(R))
            self.assertNotIn('ver-para-fazer/#arte', s, rel)
            self.assertNotIn('github.io/pt/cidadania/ferramentas', s, rel)
            if not rel.startswith('cidadania/m1/') and not rel.startswith('projetos/'):
                self.assertNotIn(correcoes.LOC_ANTIGO, s, rel)
        self.assertNotIn('faculty.fiu.edu', ler('cidadania/m2/aulas/04/index.html'))
        for p in ('cidadania/m2/passo-02/index.html', 'cidadania/m2/imagens/index.html'):
            self.assertNotIn('autor desconhecido', ler(p))
        for p in ('investigar/passo-08/index.html', 'etica/index.html', 'cidadania/m2/cid-m2-preco-minuto/index.html', 'cidadania/m2/cid-m2-dentro-da-caixa/index.html'):
            self.assertNotRegex(ler(p), r'alt=\\?"(Statue of|Jacquard machine|From book)', p)
        imagens = ler('cidadania/m2/imagens/index.html')
        for a in ('chaleira', 'lisboa-1907', 'jacquard', 'hogarth', 'declaracao'):
            self.assertIn('id="' + a + '"', imagens)
        self.assertIn(correcoes.LOC, imagens)
        self.assertIn('H. C. White Co.', ler('cidadania/m2/passo-04/index.html'))
        # 28/10/2026 (revisões de texto e de factos): o subtítulo diz que há licenças livres; Haeckel entra; o Turco
        # mostra o homem escondido; «jogador» sai; a ligação «em revisão» do passo 00 sai; as notas de Lovelace e
        # Animal Farm deixam de apontar para outros livros; a página das imagens não diz qual das versões foi alterada.
        self.assertNotIn('<p class="p-sub">Domínio público: a imagem', imagens)
        self.assertIn('Domínio público e licenças livres', imagens)
        self.assertIn('id="haeckel"', imagens)
        self.assertIn('haeckel-chiroptera.webp', imagens)
        self.assertNotIn('jogador', imagens)
        self.assertNotIn('versão B, com o pedestal vazio', imagens)
        self.assertNotIn('portas do armário abertas a mostrar engrenagens', imagens + ler('cidadania/m2/passo-04/index.html') + ler('cidadania/m2/cid-m2-dentro-da-caixa/index.html'))
        self.assertNotIn('Ver Joana Vasconcelos', ler('cidadania/m2/passo-00/index.html'))
        self.assertNotIn('ver-para-fazer/v62', ler('cidadania/m2/passo-00/index.html'))
        for p in SESSOES + ['cidadania/m2/passo-01/index.html', 'cidadania/m2/passo-07/index.html']:
            self.assertNotIn('gutenberg.org/ebooks/74223', ler(p), p)
            self.assertNotIn('gutenberg.org/ebooks/70483', ler(p), p)
        glossario = ler('cidadania/m2/glossario/index.html')
        # 28/10/2026: «Verificação lateral», como o título de Como se investiga, passo 8 (era «Leitura lateral»).
        for termo in ('Sinal', 'Critério', 'Contexto', 'Independência', 'Verificação lateral', 'Viragem'):
            self.assertEqual(glossario.count('<dt>' + termo + '</dt>'), 1, termo)
        termos = re.findall(r'<dt>([^<]+)</dt>', glossario)
        self.assertEqual(termos, sorted(termos, key=lambda t: t.lower().replace('é', 'e').replace('í', 'i')))

    def test_geracao_reprodutivel(self):
        tocados = SESSOES + [GUIA, 'cidadania/m2/index.html', 'cidadania/index.html', 'docente/index.html', 'cidadania/m2/aulas/index.html']
        tocados += [f'cidadania/m2/aulas/{n:02}/index.html' for n in range(1, 11)] + correcoes.paginas()
        tocados += ['cidadania/m2/imagens/index.html', 'cidadania/m2/glossario/index.html']
        antes = {p: (R / p).read_bytes() for p in tocados}
        # 28/10/2026 (revisão de engenharia): se a geração deixar de ser reprodutível, o teste falha, mas repõe os
        # ficheiros como estavam, para não deixar a árvore de trabalho suja.
        try:
            subprocess.run([sys.executable, '-B', 'tools/generate_cidadania_m2.py'], cwd=R, check=True, capture_output=True)
            depois = {p: (R / p).read_bytes() for p in tocados}
        finally:
            for p, conteudo in antes.items():
                if (R / p).read_bytes() != conteudo:
                    (R / p).write_bytes(conteudo)
        for p, conteudo in antes.items():
            self.assertEqual(conteudo, depois[p], p)

    # Testes acrescentados a 28/10/2026, depois da revisão em quatro lentes (design, texto, factos, engenharia).

    def test_sessao_05_nao_da_a_resposta(self):
        # O Vê pede para decidir qual das fotografias foi alterada: nada no Vê (nem a legenda, nem o texto
        # alternativo, nem o nome dos ficheiros) diz qual. A resposta fica em «Comparar razões», no fim do Decide.
        p = passos(sessao(5))
        ve = p[1]
        self.assertNotRegex(ve, r'(?i)vers[ãa]o B (foi )?alterada|alterada\.webp|pedestal vazio')
        self.assertIn('lisboa-1907-a.webp', ve)
        self.assertIn('lisboa-1907-b.webp', ve)
        self.assertIn('Uma das versões foi alterada por nós.', Pagina(ve).texto)
        comparar = re.search(r'data-feedback><summary>Comparar razões</summary><div><p>(.*?)</p>', p[2]).group(1)
        self.assertIn('a versão B foi alterada por nós', comparar)

    def test_guia_sem_nomes_tecnicos_e_sem_pontuacao_dupla(self):
        t = Pagina(ler(GUIA)).texto
        for w in ('epi-cidadania-m2', 'lente-cidadania', 'cidadania/m2/aulas', 'pergunta pessoal sobre o produto'):
            self.assertNotIn(w, t)
        self.assertNotRegex(t, r'[?!]\.')

    def test_portal_so_le_a_chave_das_sessoes(self):
        portal = ler('cidadania/index.html')
        self.assertNotIn('var M=[]', portal)  # o script morto saiu
        script = re.search(r'<script>\(function\(\)\{try\{var S=JSON\.parse\(localStorage\.getItem\("' + CHAVE + r'"\).*?</script>', portal, re.S).group(0)
        self.assertNotIn('setItem', script)
        self.assertNotIn('removeItem', script)
        self.assertIn('de 10 sessões registadas', script)
        self.assertIn('epi-cidadania-m2', ler('cidadania/m2/index.html'))  # o contador dos passos continua no módulo

    def test_fonte_nao_bloqueia_a_pagina(self):
        for p in SESSOES + [GUIA]:
            s = ler(p)
            self.assertIn('family=Bebas+Neue&display=swap" rel="stylesheet" media="print" onload="this.media=\'all\'"', s, p)
            self.assertNotRegex(s.split('<noscript>')[0], r'family=Bebas\+Neue&display=swap" rel="stylesheet">', p)

    def test_mapa_diz_o_estado_por_palavras(self):
        for n in (1, 6, 10):
            s = sessao(n)
            m = re.search(r'<ol class="c10-mapa"[^>]*>(.*?)</ol>', s, re.S).group(1)
            self.assertEqual(m.count('(casa anterior)'), n - 1)
            self.assertEqual(m.count('(casa de hoje)'), 1)
            self.assertEqual(m.count('(casa seguinte)'), 10 - n)
            self.assertIn('class="c10-small c10-mapa-legenda"', s)

    def test_frases_para_classificar_em_lista(self):
        # Sessão 06: as quatro frases ficam numa lista (A a D), como na 07, e a pergunta inclui a opinião.
        d = passos(sessao(6))[2]
        self.assertIn('<ol class="c10-document c10-frases" type="A">', d)
        self.assertEqual(re.search(r'type="A">(.*?)</ol>', d).group(1).count('<li>'), 4)
        self.assertIn('qual é uma opinião?', d)


if __name__ == '__main__':
    unittest.main()
