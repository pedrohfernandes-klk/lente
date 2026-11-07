"""05/11/2026: decisão 163 (menus do Laboratório e das lições). O que os geradores escrevem: a barra única e o fio do
Laboratório, as portas e os percursos com o passo do método, a ligação às sessões do Ideias, o menu ≡ comum
(tools/menu_casca.py) nas quatro famílias, a continuação no fim de cada percurso e a preservação, contra a base e5acb14, de
todos os destinos, ids, dados e chaves de progresso. O navegador confere-se em tests/browser_menus_lab.cjs."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import importlib.util, json, posixpath, re, subprocess, sys, unittest

R = Path(__file__).resolve().parents[1]
BASE = 'e5acb14'
ABS = 'https://pedrohfernandes-klk.github.io/lente/'
D = json.loads((R / 'assets/laboratorio/percursos.json').read_text('utf-8'))
_ll = importlib.util.spec_from_file_location('licoes_lente', R / 'tools/licoes_lente.py')
LL = importlib.util.module_from_spec(_ll); _ll.loader.exec_module(LL)

PORTAS = {b['id']: 'narrativas/' + b['id'] + '/index.html' for b in D['blocks']}
PERCURSOS = {r['id']: 'narrativas/percursos/' + r['id'] + '/index.html' for r in D['routes']}
LAB = ['narrativas/index.html', 'narrativas/tudo/index.html', 'narrativas/percursos/index.html', 'narrativas/ideias/index.html'] + list(PORTAS.values()) + list(PERCURSOS.values())
SESSOES = ['narrativas/ideias/sessao-01/index.html', 'narrativas/ideias/sessao-02/index.html'] + sorted(p.relative_to(R).as_posix() for p in (R / 'cidadania/piloto').glob('m1-s*/index.html'))
# 06/11/2026: fusão do main (com a sessão 1 da Cidadania, #126). O gerador das lições escreve também as sessões da Cidadania no
# molde novo (cidadania/m1/sessoes/01/), com o mesmo menu ≡ das do piloto; entram na lista e conferem-se como as outras.
MOLDE = sorted(LL.carregar(p)['saida'] for p in LL.PASTA.glob('*.json') if LL.carregar(p).get('molde') == LL.MOLDE)
SESSOES += MOLDE
# 06/11/2026: as camadas do #126 sobre a base, para a preservação (abaixo): o manifesto fechado do pedido 1 e o do pedido 2
# (tests/molde_pedido2.py), por cima da 146 e da 154 (tests/grupos146.py), cada troca com contagem exata.
MOLDE_P1 = json.loads((R / 'tools/trocas/molde-pedido1-20261105.json').read_text('utf-8'))
sys.path.insert(0, str(R / 'tests'))
import grupos146, molde_pedido2  # noqa: E402
import molde_s02  # noqa: E402  06/11/2026: fusão do main na sessão 02 do M1 (camada por cima do pedido 2)
# 06/11/2026: fusão do main (com a sessão 2 final, os menus e o «Dilemas») na sessão 03 do M1. O manifesto fechado da s03
# (tests/molde_s03.py) parte do main b29833d, já com a 163: é a camada mais recente e desfaz-se no ficheiro atual (abaixo).
import molde_s03  # noqa: E402
# 06/11/2026: fusão do main (com as sessões 2 e 3 finais, os menus e o «Dilemas») na sessão 04 do M1. O manifesto fechado da s04
# (tests/molde_s04.py) parte do main ba5211f, já com a s03: é agora a camada mais recente e desfaz-se no ficheiro atual antes da
# da s03 (abaixo).
import molde_s04  # noqa: E402
# 06/11/2026: fusão do main (com as sessões 2 a 4 finais e o elétrico) na sessão 05 do M1. O manifesto fechado da s05
# (tests/molde_s05.py) parte do main 5b4a451, já com a s04: é agora a camada mais recente e desfaz-se no ficheiro atual antes da da
# s04 (abaixo).
import molde_s05  # noqa: E402
# 06/11/2026: fusão do main (com as sessões 2 a 5 finais) na sessão 06 do M1. O manifesto fechado da s06 (tests/molde_s06.py)
# parte do main d04c20f, já com a s05: é agora a camada mais recente e desfaz-se no ficheiro atual antes da da s05 (abaixo).
import molde_s06  # noqa: E402
# 06/11/2026: fusão do main (com as sessões 2 a 6 finais) na sessão 07 do M1. O manifesto fechado da s07 (tests/molde_s07.py)
# parte do main 8731fb9, já com a s06: é agora a camada mais recente e desfaz-se no ficheiro atual antes da da s06 (abaixo).
import molde_s07  # noqa: E402
# 06/11/2026: fusão do main (com as sessões 2 a 7 finais) na sessão 08 do M1. O manifesto fechado da s08 (tests/molde_s08.py)
# parte do main 3c774cb, já com a s07: é agora a camada mais recente e desfaz-se no ficheiro atual antes da da s07 (abaixo).
import molde_s08  # noqa: E402
# 07/11/2026: a sessão 09 do M1 (tests/molde_s09.py). O manifesto fechado parte do main dc01487, já com a s08: é agora a camada
# mais recente e desfaz-se no ficheiro atual antes da da s08 (abaixo).
import molde_s09  # noqa: E402


def com_molde(texto, rel):
    if rel in grupos146.TROCAS:
        texto = grupos146.aplicar(texto, rel)
    for antigo, novo, n in MOLDE_P1.get(rel, []):
        assert texto.count(antigo) == n, ('molde, pedido 1', rel, antigo[:80])
        texto = texto.replace(antigo, novo)
    # 06/11/2026: fusão do main na sessão 02 do M1. A camada da s02 (manifesto fechado, contagem exata) aplica-se por cima do
    # pedido 2, como no test_cidadania_base_motor.
    return molde_s02.aplicar(molde_pedido2.aplicar(texto, rel), rel)


def ler(rel):
    return (R / rel).read_text('utf-8')


def base(rel):
    try:
        return subprocess.check_output(['git', 'show', f'{BASE}:{rel}'], cwd=R, stderr=subprocess.DEVNULL).decode('utf-8')
    except subprocess.CalledProcessError:
        return None


def menu_de(s):
    i = s.find('<div class="casca-menu')
    if i < 0:
        return None
    n = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        n += 1 if m.group(0) == '<div' else -1
        if n == 0:
            return s[i:i + m.end()]


def paginas_com_menu():
    """As páginas das quatro famílias com o menu ≡ (sessões, piloto, peças do Laboratório e Cidadania estática)."""
    pecas = [p['url'] + 'index.html' for p in D['pieces'] if '<div class="casca-menu' in ler(p['url'] + 'index.html')]
    estaticas = sorted(p.relative_to(R).as_posix() for d in ('cidadania/m1', 'cidadania/m2') for p in (R / d).glob('*/index.html') if '<div class="casca-menu' in p.read_text('utf-8'))
    return SESSOES + pecas + estaticas + ['cidadania/25-de-abril/index.html']


class Ligacoes(HTMLParser):
    def __init__(self):
        super().__init__(); self.hrefs = []; self.ids = []
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k == 'href' and v and tag == 'a':
                self.hrefs.append(v)
            if k == 'id' and v:
                self.ids.append(v)


def destinos(rel, s):
    """Os destinos internos (no Lente) de uma página, como caminhos absolutos com a âncora."""
    p = Ligacoes(); p.feed(s); out = set()
    for h in p.hrefs:
        if h.startswith(('?', 'javascript:', 'mailto:')):
            continue
        u = urlsplit(urljoin(ABS + rel, h))
        url = u.scheme + '://' + u.netloc + u.path
        if not url.startswith(ABS):
            continue
        caminho = posixpath.normpath(url[len(ABS):] or '.')
        caminho = '' if caminho == '.' else caminho.removesuffix('/index.html').removesuffix('index.html').rstrip('/')
        out.add(caminho + ('#' + u.fragment if u.fragment else ''))
    return out


def visivel(s):
    s = re.sub(r'<(script|style)\b.*?</\1>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s)


class BarraEFio(unittest.TestCase):
    def test_uma_barra_e_o_fio_com_o_atual_certo(self):
        for rel in LAB:
            s = ler(rel)
            with self.subTest(rel=rel):
                self.assertEqual(s.count('<header class="lab-barra">'), 1)
                self.assertNotIn('barra-nav', s)
                barra = re.search(r'<header class="lab-barra">.*?</header>', s).group(0)
                self.assertEqual(re.findall(r'>([^<>]+)</a>', barra), ['Lente', 'Laboratório'])
                self.assertEqual(barra.count('data-appearance-control'), 1)
                fio = re.search(r'<nav class="lab-fio" aria-label="Partes do Laboratório">.*?</nav>', s)
                if rel == 'narrativas/index.html':
                    self.assertIsNone(fio)
                    self.assertIn('<a href="./" aria-current="page">Laboratório</a>', barra)
                    continue
                self.assertIsNotNone(fio)
                self.assertEqual(re.findall(r'<b>([^<]+)</b>', fio.group(0)), ['Ideias', 'Observar', 'Treinar', 'Criar'])
                atuais = re.findall(r'aria-current="(page|true)"><span class="n">(?:(?!</a>).)*<b>([^<]+)</b>', fio.group(0))
                porta = next((b['title'] for b in D['blocks'] if rel == PORTAS[b['id']]), None)
                rota = next((r for r in D['routes'] if rel == PERCURSOS[r['id']]), None)
                if porta:
                    self.assertEqual(atuais, [('page', porta)])
                elif rota:
                    self.assertEqual(atuais, [('true', next(b['title'] for b in D['blocks'] if b['id'] == rota['block']))])
                elif rel == 'narrativas/ideias/index.html':
                    self.assertEqual(atuais, [('page', 'Ideias')])
                else:
                    self.assertEqual(atuais, [])

    def test_portas_percursos_e_passos(self):
        entrada = ler('narrativas/index.html')
        for b in D['blocks']:
            s = ler(PORTAS[b['id']])
            self.assertIn('<p class="rotulo">' + b['passoTexto'].rstrip('.') + '</p>', s)
            self.assertIn('<span class="passo">' + b['passoTexto'] + '</span>', entrada)
            n = str(b['passos'][0]) if len(b['passos']) == 1 else f'{b["passos"][0]}–{b["passos"][-1]}'
            self.assertIn('<span class="nums" aria-hidden="true">' + n + '</span>', entrada)
            # uma só ligação por porta na entrada, com o id antigo do bloco no item
            self.assertEqual(len(re.findall(r'<li id="' + re.escape(b['anchor']) + r'"><a class="porta3" href="' + b['id'] + r'/"', entrada)), 1)
            for r in D['routes']:
                if r['block'] != b['id']:
                    continue
                p = ler(PERCURSOS[r['id']])
                palavra, nums = ('passo', str(b['passos'][0])) if len(b['passos']) == 1 else ('passos', ', '.join(map(str, b['passos'][:-1])) + ' e ' + str(b['passos'][-1]))
                self.assertIn(f'<p class="rotulo">{b["title"]}, {palavra} {nums}</p>', p)
                # nenhum beco: «Daqui segues para» com o seguinte e o regresso à porta
                depois = re.search(r'<nav class="depois" aria-label="Daqui segues para">(.*?)</nav>', p).group(1)
                self.assertEqual(len(re.findall(r'<a href=', depois)), 2)
                self.assertIn('<small>Voltar a</small><b>' + b['title'] + '</b>', depois)
        # os dois percursos de Observar ligam às sessões 1 e 2 do Ideias (pelo campo «passo» das sessões publicadas)
        for r in ('olhar', 'voz'):
            p = ler(PERCURSOS[r])
            self.assertIn('No Ideias, este passo faz-se na sessão 1, «<a href="../../ideias/sessao-01/">Ver ou observar?</a>», e na sessão 2, «<a href="../../ideias/sessao-02/">O cocheiro</a>».', p)
        for r in D['routes']:
            if r['block'] != 'ver':
                self.assertNotIn('liga-ideias', ler(PERCURSOS[r['id']]), r['id'])
        self.assertIn('Para treinar este passo: <a href="../ver/">Observar →</a>', ler('narrativas/ideias/index.html'))

    def test_sem_dobras_e_texto_da_casa(self):
        proibido = re.compile(r'por fazer|Página inicial|Abrir o percurso|[·—]', re.I)
        for rel in LAB:
            s = ler(rel)
            with self.subTest(rel=rel):
                self.assertNotIn('<details class="dobra', s)
                self.assertNotIn('cz-fold', s)
                self.assertEqual(proibido.findall(visivel(s)), [])
        # o texto da navegação nova (barra, fio, rótulos, «Daqui segues para», portas) segue as regras do texto do aluno
        for rel in LAB:
            s = ler(rel)
            nav = ' '.join(re.findall(r'<(?:header class="lab-barra"|nav class="lab-fio"|nav class="depois"|p class="rotulo"|p class="liga-ideias"|a class="porta3")[^>]*>.*?</(?:header|nav|p|a)>', s, re.S))
            with self.subTest(rel=rel, parte='navegação'):
                self.assertIsNone(LL.PROIBIDAS.search(visivel(nav)))
                self.assertIsNone(LL.QUAL_NOME.search(visivel(nav)))


class Menu(unittest.TestCase):
    def test_um_so_menu_nas_quatro_familias(self):
        paginas = paginas_com_menu()
        self.assertGreaterEqual(len(paginas), 12 + 46 + 33)
        proibido = re.compile(r'por fazer|Página inicial|Abrir o percurso|[·—]', re.I)
        for rel in paginas:
            s = ler(rel); m = menu_de(s)
            with self.subTest(rel=rel):
                # 05/11/2026: revisão. O nome acessível do diálogo junta o cabeçalho e o título (aria-labelledby="m-cab m-t"); a
                # exigência continua a ser o início exato do painel.
                self.assertTrue(m.startswith('<div class="casca-menu m2" data-c-painel hidden><div class="c-menu-in" id="c-menu" role="dialog" aria-modal="true" aria-labelledby="m-cab m-t"><div class="c-menu-cab"><p id="m-cab">'))
                self.assertEqual(s.count('data-appearance-control'), 1)
                self.assertIn('data-appearance-control', m)
                self.assertRegex(s, r'<button type="button" class="c-ic" data-c-menu aria-label="Menu" aria-expanded="false" aria-controls="c-menu"')
                # «Estás em», depois «Voltar…» como primeira ação, «Como se faz» para /lente/como/
                self.assertRegex(m, r'<div class="m-aqui"><p class="k">Estás em</p><p class="t" id="m-t">[^<]+</p>')
                self.assertRegex(m, r'<nav aria-label="Menu"><a class="principal" href="[^"]+"><svg[^>]*>.*?</svg><span>Voltar (?:ao|à|a) ')
                self.assertIn('<a href="' + ABS + 'como/"><svg', m)
                # a projeção está no menu de todas as páginas com o motor das lições (as seis peças com motor próprio, das Formas e
                # de Fora da página, guardam no menu os botões e as ligações do seu motor, em nav.m-orig)
                if 'EPIJogo' in s:
                    self.assertIn('class="so-normal" href="?projetar=1"', m)
                    self.assertIn('class="so-aula" href="?" hidden', m)
                else:
                    # os botões do motor próprio (data-lf-menu) ficam todos, no menu
                    antigo = base(rel) or ''
                    self.assertEqual(sorted(re.findall(r'data-lf-menu="([^"]+)"', menu_de(antigo) or '')), sorted(re.findall(r'data-lf-menu="([^"]+)"', m)))
                    self.assertTrue('<nav class="m-orig"' in m or 'class="so-normal" href="?projetar=1"' in m)
                self.assertIn('assets/licoes/menu.css?v=', s)
                self.assertIn('assets/licoes/menu.js?v=', s)
                self.assertNotIn('<style id="mg-css">', s)
                self.assertNotIn('c-migalhas', m)
                self.assertEqual(proibido.findall(visivel(m)), [])
                self.assertIsNone(LL.QUAL_NOME.search(visivel(m)))
                # 05/11/2026: revisão. Também nenhum nome acessível diz «Página inicial» (a marca das páginas estáticas dizia-o) e a
                # marca da barra tem o nome visível num <span class="c-marca-t">, nas quatro famílias (as seis peças com motor próprio
                # não têm a casa desenhada).
                self.assertEqual(re.findall(r'aria-label="[^"]*Página inicial[^"]*"', s), [])
                topo = re.search(r'<header class="casca-topo">(.*?)</header>', s, re.S).group(1)
                self.assertRegex(topo, r'^<a class="c-marca" href="[^"]+" aria-label="[^"]+">(?:<svg class="c-casa"[^>]*>.*?</svg>)?<span class="c-marca-t">[^<]+</span></a>')

    def test_marca_das_estaticas_como_no_piloto(self):
        # 05/11/2026: revisão. O mesmo destino tem sempre o mesmo nome: nas M1 e M2 a marca leva ao módulo e chama-se «Cidadania,
        # módulo N» (como no piloto); no 25 de Abril leva à Cidadania e chama-se «Cidadania». A entrada do Lente continua no
        # caminho do menu («Lente»).
        for d in ('cidadania/m1', 'cidadania/m2'):
            n = d[-1]
            for p in sorted((R / d).glob('*/index.html')):
                s = p.read_text('utf-8')
                if '<div class="casca-menu' not in s:
                    continue
                with self.subTest(rel=p.relative_to(R).as_posix()):
                    self.assertIn(f'<header class="casca-topo"><a class="c-marca" href="{ABS}cidadania/m{n}/" aria-label="Cidadania, módulo {n}"><svg class="c-casa"', s)
                    self.assertIn(f'<li><a href="{ABS}">Lente</a></li>', menu_de(s))
        s = ler('cidadania/25-de-abril/index.html')
        self.assertIn('<header class="casca-topo"><a class="c-marca" href="../" aria-label="Cidadania"><svg class="c-casa"', s)

    def test_sem_javascript_diz_para_onde_ir(self):
        for rel in SESSOES:
            self.assertRegex(ler(rel), r'<main class="casca-corpo" id="casca-corpo" tabindex="-1"><noscript><p class="c-semjs">Os cartões desta sessão precisam de JavaScript\. Sem ele, <a href="[^"]+">volta ')

    def test_estaticas_idempotentes(self):
        r = subprocess.run([sys.executable, str(R / 'tools/menu_casca.py'), '--estaticas', '--verificar'], capture_output=True, text=True, cwd=R)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('0 página(s) por atualizar', r.stdout)

    def test_ultima_peca_de_cada_percurso_tem_seguinte(self):
        P = {p['id']: p for p in D['pieces']}
        for r in D['routes']:
            p = P[r['pieces'][-1]]; s = ler(p['url'] + 'index.html')
            with self.subTest(peca=p['id']):
                nav = re.findall(r'<nav class="lab-fim-percurso"[^>]*>(.*?)</nav>', s, re.S)
                cfg = re.findall(r',seguinte:"([^"]+)"', s)
                self.assertTrue(cfg or (nav and len(re.findall(r'href=', nav[0])) == 2), p['id'])
                m = menu_de(s)
                if m:
                    self.assertRegex(m, r'</span></a><a href="[^"]+"><svg[^>]*>.*?</svg><span>(?:Seguinte|Percurso seguinte|Passo seguinte|No Ideias)<small>')


class Preservacao(unittest.TestCase):
    def test_nenhum_destino_nenhum_id_nenhuma_chave_se_perde(self):
        mudados = subprocess.check_output(['git', 'diff', '--name-only', BASE, '--', '*.html'], cwd=R).decode().split()
        antes_d, depois_d = set(), set()
        for rel in mudados:
            antes = base(rel)
            if antes is None or not (R / rel).exists():
                continue
            # 06/11/2026: fusão do main (com a sessão 1 da Cidadania, #126). Os ficheiros que o #126 escreve inteiros (a sessão 01 no
            # molde) têm de ser, letra a letra, o que o seu gerador escreve, e a sessão cumpre o contrato do molde; os que muda em
            # parte comparam-se com a base já com as camadas do #126 (com_molde), e tudo o resto continua a conferir-se.
            if rel in molde_pedido2.INTEIROS:
                with self.subTest(rel=rel):
                    self.assertTrue(molde_pedido2.inteiro_ok(rel), rel)
                continue
            # 06/11/2026: fusão do main na sessão 02 do M1. O mesmo para os ficheiros que a s02 escreve inteiros (a sua página e a
            # versão para imprimir): letra a letra o que o gerador escreve, e a sessão cumpre o contrato do molde. Nenhuma outra
            # página liga às âncoras da página antiga da s02 (#momento-1 a #momento-5, #abertura).
            if rel in molde_s02.INTEIROS:
                with self.subTest(rel=rel):
                    self.assertTrue(molde_s02.inteiro_ok(rel), rel)
                continue
            # 06/11/2026: fusão do main na sessão 03 do M1. O mesmo para os ficheiros que a s03 escreve inteiros (a sua página e a
            # versão para imprimir): letra a letra o que o gerador escreve, e a sessão cumpre o contrato do molde.
            if rel in molde_s03.INTEIROS:
                with self.subTest(rel=rel):
                    self.assertTrue(molde_s03.inteiro_ok(rel), rel)
                continue
            # 06/11/2026: fusão do main na sessão 04 do M1. O mesmo para os ficheiros que a s04 escreve inteiros (a sua página e a
            # versão para imprimir): letra a letra o que o gerador escreve, e a sessão cumpre o contrato do molde.
            if rel in molde_s04.INTEIROS:
                with self.subTest(rel=rel):
                    self.assertTrue(molde_s04.inteiro_ok(rel), rel)
                continue
            # 06/11/2026: fusão do main na sessão 05 do M1. O mesmo para os ficheiros que a s05 escreve inteiros (a sua página e a
            # versão para imprimir): letra a letra o que o gerador escreve, e a sessão cumpre o contrato do molde.
            if rel in molde_s05.INTEIROS:
                with self.subTest(rel=rel):
                    self.assertTrue(molde_s05.inteiro_ok(rel), rel)
                continue
            # 06/11/2026: fusão do main na sessão 06 do M1. O mesmo para os ficheiros que a s06 escreve inteiros (a sua página e a
            # versão para imprimir): letra a letra o que o gerador escreve, e a sessão cumpre o contrato do molde.
            if rel in molde_s06.INTEIROS:
                with self.subTest(rel=rel):
                    self.assertTrue(molde_s06.inteiro_ok(rel), rel)
                continue
            # 06/11/2026: fusão do main na sessão 07 do M1. O mesmo para os ficheiros que a s07 escreve inteiros (a sua página e a
            # versão para imprimir): letra a letra o que o gerador escreve, e a sessão cumpre o contrato do molde.
            if rel in molde_s07.INTEIROS:
                with self.subTest(rel=rel):
                    self.assertTrue(molde_s07.inteiro_ok(rel), rel)
                continue
            # 06/11/2026: fusão do main na sessão 08 do M1. O mesmo para os ficheiros que a s08 escreve inteiros (a sua página e a
            # versão para imprimir): letra a letra o que o gerador escreve, e a sessão cumpre o contrato do molde.
            if rel in molde_s08.INTEIROS:
                with self.subTest(rel=rel):
                    self.assertTrue(molde_s08.inteiro_ok(rel), rel)
                continue
            # 07/11/2026: sessão 09 do M1 no molde. O mesmo para os ficheiros que a s09 escreve inteiros.
            if rel in molde_s09.INTEIROS:
                with self.subTest(rel=rel):
                    self.assertTrue(molde_s09.inteiro_ok(rel), rel)
                continue
            if rel in MOLDE_P1 or rel in molde_pedido2.TROCAS or rel in molde_s02.TROCAS:  # 06/11/2026: também a camada da s02
                antes = com_molde(antes, rel)
            agora = ler(rel)
            # 06/11/2026: fusão do main na sessão 03 do M1. Nos ficheiros que a s03 muda em parte, desfaz-se primeiro a sua camada
            # no ficheiro atual (manifesto fechado, contagem exata de cada «novo»); o que fica, o ficheiro do main, confere-se como antes.
            # 06/11/2026: fusão do main na sessão 04 do M1. Nos ficheiros que a s04 muda em parte, desfaz-se antes a sua camada, a
            # mais recente (manifesto fechado, contagem exata de cada «novo»); depois a da s03, como acima.
            # 06/11/2026: fusão do main na sessão 05 do M1. Nos ficheiros que a s05 muda em parte, desfaz-se primeiro a sua camada,
            # agora a mais recente (manifesto fechado, contagem exata de cada «novo»); depois a da s04 e a da s03, como acima.
            # 06/11/2026: fusão do main na sessão 06 do M1. Nos ficheiros que a s06 muda em parte, desfaz-se primeiro a sua camada,
            # agora a mais recente (manifesto fechado, contagem exata de cada «novo»); depois a da s05, a da s04 e a da s03, como acima.
            # 06/11/2026: fusão do main na sessão 07 do M1. Nos ficheiros que a s07 muda em parte, desfaz-se primeiro a sua camada,
            # agora a mais recente (manifesto fechado, contagem exata de cada «novo»); depois a da s06, a da s05, a da s04 e a da s03.
            # 06/11/2026: fusão do main na sessão 08 do M1. Nos ficheiros que a s08 muda em parte, desfaz-se primeiro a sua camada,
            # agora a mais recente (manifesto fechado, contagem exata de cada «novo»); depois a da s07, a da s06, a da s05, a da s04 e a
            # da s03.
            # 07/11/2026: sessão 09 do M1 no molde. A sua camada, a mais recente, desfaz-se antes da da s08.
            if rel in molde_s09.TROCAS:
                agora = molde_s09.desfazer(agora, rel)
            if rel in molde_s08.TROCAS:
                agora = molde_s08.desfazer(agora, rel)
            if rel in molde_s07.TROCAS:
                agora = molde_s07.desfazer(agora, rel)
            if rel in molde_s06.TROCAS:
                agora = molde_s06.desfazer(agora, rel)
            if rel in molde_s05.TROCAS:
                agora = molde_s05.desfazer(agora, rel)
            if rel in molde_s04.TROCAS:
                agora = molde_s04.desfazer(agora, rel)
            if rel in molde_s03.TROCAS:
                agora = molde_s03.desfazer(agora, rel)
            antes_d |= destinos(rel, antes); depois_d |= destinos(rel, agora)
            with self.subTest(rel=rel):
                a, b = Ligacoes(), Ligacoes(); a.feed(antes); b.feed(agora)
                # só sai o id do estilo das migalhas antigas do menu (style#mg-css), que deixou de servir
                self.assertEqual(set(a.ids) - set(b.ids) - {'mg-css'}, set())
                for padrao in (r'<script type="application/json" id="lab-dados">.*?</script>', r'<script type="application/json" id="lab-retiradas">.*?</script>'):
                    self.assertEqual(re.findall(padrao, antes, re.S), re.findall(padrao, agora, re.S))
                # nenhuma chave nem peça se perde (a entrada do Laboratório passa a ler também as chaves das sessões do Ideias)
                from collections import Counter
                for attr in ('data-chave', 'data-peca', 'data-versao', 'data-registo'):
                    self.assertEqual(Counter(re.findall(attr + r'="([^"]*)"', antes)) - Counter(re.findall(attr + r'="([^"]*)"', agora)), Counter(), attr)
                for chave in (r'[{,]chave:"([^"]*)"', r'[{,]versao:"([^"]*)"', r'var K="([^"]*)"', r'"chave": "([^"]*)"', r'"versao": "([^"]*)"'):
                    self.assertEqual(re.findall(chave, antes), re.findall(chave, agora), chave)
        self.assertEqual(antes_d - depois_d, set())

    def test_chaves_de_progresso_nos_scripts(self):
        # as chaves de localStorage que os scripts do Laboratório leem continuam as mesmas (nenhuma chave nova)
        js = (R / 'assets/laboratorio/percursos.js').read_text('utf-8')
        self.assertIn("AVISO='lente-laboratorio-reposicao'", js)
        self.assertEqual(re.findall(r"localStorage\.(?:get|set)Item\(([^,)]+)", js), ['k', 'q.key', 'k'])
        ent = (R / 'assets/laboratorio/ideias/entrada.js').read_text('utf-8')
        self.assertIn('localStorage.getItem(li.dataset.chave)', ent)
        menu = (R / 'assets/licoes/menu.js').read_text('utf-8')
        self.assertNotIn('localStorage', menu)
        # a entrada do Laboratório lê as mesmas chaves das sessões publicadas do Ideias, com o mesmo código da página Ideias
        self.assertEqual(re.findall(r'<li data-chave="([^"]+)"', ler('narrativas/index.html')), ['epi-lab-ideias-s01', 'epi-lab-ideias-s02'])
        self.assertIn('assets/laboratorio/ideias/entrada.js', ler('narrativas/index.html'))


if __name__ == '__main__':
    unittest.main()
