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


SESSOES = [f'cidadania/m2/sessoes/{n:02}/index.html' for n in range(1, 11)]
GUIA = 'cidadania/m2/sessoes/index.html'


class Molde(unittest.TestCase):
    def test_abertura_uma_imagem_pergunta_comecar(self):
        for n in range(1, 11):
            s = sessao(n)
            capa = s[s.index('data-session-intro'):s.index('data-session-flow')]
            self.assertEqual(capa.count('<img '), 1, n)
            self.assertIn('class="c10-deck"', capa)
            self.assertIn('data-start>Começar</a>', capa)
            # uma imagem por página: o Vê repete a imagem da abertura, nunca outra
            self.assertEqual(len(set(Pagina(s).imgs)), 1, n)

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
        for n in range(2, 11):
            anterior = palavras(Pagina(sessao(n - 1)).texto)
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
            self.assertEqual(s.count('class="c10-obra"'), 1, n)
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
        # Nenhum endereço externo novo sem conferência: todos já estão em origin/main, menos o registo certo
        # da Library of Congress, aberto a 28/10/2026 (tools/cidadania_m2_correcoes.py).
        conferidos = {correcoes.LOC}
        externos = set()
        for p in SESSOES + [GUIA]:
            for ref in Pagina(ler(p)).refs:
                if ref.startswith('http') and not ref.startswith(LENTE):
                    externos.add(ref)
        for url in sorted(externos - conferidos):
            r = subprocess.run(['git', 'grep', '-q', '-F', '-e', url, '-e', url.replace('&', '&amp;'), 'origin/main', '--', '*.html'], cwd=R)
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
        lista = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', 'origin/main', 'cidadania/m1'], cwd=R).decode().split()
        locais = sorted(str(p.relative_to(R)) for p in (R / 'cidadania/m1').rglob('*') if p.is_file())
        self.assertEqual(sorted(lista), locais)
        for f in lista + ['assets/cidadania-m1-sessoes.css', 'assets/cidadania-m1-sessoes.js']:
            self.assertEqual((R / f).read_bytes(), subprocess.check_output(['git', 'show', 'origin/main:' + f], cwd=R), f)

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
        glossario = ler('cidadania/m2/glossario/index.html')
        for termo in ('Sinal', 'Critério', 'Contexto', 'Independência', 'Leitura lateral', 'Viragem'):
            self.assertEqual(glossario.count('<dt>' + termo + '</dt>'), 1, termo)
        termos = re.findall(r'<dt>([^<]+)</dt>', glossario)
        self.assertEqual(termos, sorted(termos, key=lambda t: t.lower().replace('é', 'e').replace('í', 'i')))

    def test_geracao_reprodutivel(self):
        tocados = SESSOES + [GUIA, 'cidadania/m2/index.html', 'cidadania/index.html', 'docente/index.html', 'cidadania/m2/aulas/index.html']
        tocados += [f'cidadania/m2/aulas/{n:02}/index.html' for n in range(1, 11)] + correcoes.paginas()
        tocados += ['cidadania/m2/imagens/index.html', 'cidadania/m2/glossario/index.html']
        antes = {p: (R / p).read_bytes() for p in tocados}
        subprocess.run([sys.executable, '-B', 'tools/generate_cidadania_m2.py'], cwd=R, check=True, capture_output=True)
        for p, conteudo in antes.items():
            self.assertEqual(conteudo, (R / p).read_bytes(), p)


if __name__ == '__main__':
    unittest.main()
