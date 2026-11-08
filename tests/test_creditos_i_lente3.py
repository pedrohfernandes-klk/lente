"""08/11/2026: decisões 153, 162 e 176 (pedido lente-3 do plano plano-creditos-i-20261105.md, famílias L14 a L19). Cada «i» novo
confere-se contra o main de partida (fec58ae), página a página, também quando o HTML vive dentro dos JSON dos cartões:

- o crédito que estava à vista está agora inteiro dentro do «i» (as mesmas palavras e as mesmas ligações; a ligação para a fonte
  leva data-external e aria-label, como no pedido lente-1, e a licença CC leva rel="license" e a sua ligação), e fora do «i» não
  fica crédito nenhum;
- o que fica à vista é só o que diz quem ou o que se vê: span.fr-leg e span.fa-leg (L15, L18), a identificação e a frase que
  serve a pergunta (L14), quem se vê nos retratos (L16) e a primeira frase das legendas das vozes (L17);
- no portal da Cidadania, cada imagem tem o seu «i» e sai a linha agregada p.cid-image-credits (L19);
- fora da tabela do plano, com a mesma estrutura e ainda publicadas: as duas imagens do passo 02 de «Como se investiga»
  (figure.fig-inv, como no L14) e o retrato de Oscar Wilde no passo 01 dos Direitos (figure.fig, como na Ética do pedido lente-2);
- cada «i» tem a marcação da peça comum, vive fora de ligações, botões, rótulos, legendas e partes decorativas, e a página carrega
  a peça comum (assets/info-i.css e assets/info-i.js, que este pedido não muda) com o caminho relativo certo;
- a camada (tools/trocas/creditos-i-lente3-20261108.json) é fechada e reversível, e tools/creditos_i.py trata o escape dos cartões;
- nada do que entrou traz «·», «—», «professor», «jogo», «jogar», «ficha» nem «folha»."""
import hashlib
import json
import posixpath
import re
import subprocess
import sys
import unittest
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'tools'))
import creditos_i  # noqa: E402
import creditos_i_lente3  # noqa: E402

BASE = 'fec58ae298fd44a9144799ebb8f007b92054720a'
V = '20261106-3'
PROIBIDAS = re.compile(r'(?<![\wÀ-ÿ])(?:professor(?:a|es|as)?|jog(?:ar|a[sm]?|o|os|ou|uei|ámos)|fichas?|folhas?)(?![\wÀ-ÿ])|—|·', re.I)
I_RE = re.compile(r'<details class="info-i( info-i--linha)?" name="info-i"><summary aria-label="([^"]+)"><span aria-hidden="true">i</span></summary>'
                  r'<p class="info-i-texto">(.*?)</p></details>', re.S)
MARCAS = re.compile(r'Domínio público|domínio público|CC BY|CC0|Wikimedia Commons|commons\.wikimedia|no registo de origem|Grafismo gerado|'
                    r'Fotografia:|Ilustração:|Gravura:|Library of Congress|Biblioteca do Congresso|Arquivo da EPI|metmuseum|loc\.gov|archive\.org|'
                    r'sem restrições conhecidas|Redimensionada')
PAGINAS = sorted(f for f in creditos_i_lente3.TROCAS if f.endswith('.html'))
# Os «i» que já lá estavam antes deste pedido (o da fotografia nas letras do cabeçalho, pedido lente-1).
ANTES = {'cidade/index.html': 1, 'investigar/index.html': 1, 'projetos/index.html': 1, 'sidequests/index.html': 1}
L15C = ('gigantes/', 'vozes/', 'sidequests/')


def ler(f):
    return (R / f).read_text('utf-8')


def antigo(f):
    return subprocess.check_output(['git', 'show', f'{BASE}:{f}'], cwd=R).decode('utf-8')


def sem_escape(s):
    """O HTML dos cartões como o motor o lê (aspas e «</» sem escape); fora dos cartões não muda nada."""
    return s.replace('\\"', '"').replace('<\\/', '</')


def sem_dados(s):
    return re.sub(r'data:image/[a-z+]+;base64,[A-Za-z0-9+/=]+', 'DATA', s)


def texto(h):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', '', h))).strip()


def ligacoes(h):
    return re.findall(r'href="([^"]+)"', h)


def sem_licencas(hs):
    return [h for h in hs if 'creativecommons.org' not in h]


def i_unico(fig):
    ms = list(I_RE.finditer(fig))
    return ms[0] if len(ms) == 1 else None


def figuras(s, cls):
    return re.findall(r'<figure class="' + cls + r'[^"]*"[^>]*>.*?</figure>', s, re.S)


class Ancestrais(HTMLParser):
    """Onde vive cada details.info-i: as etiquetas abertas por cima dele."""
    VAZIAS = {'img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'wbr', 'col', 'area'}

    def __init__(self):
        super().__init__()
        self.pilha, self.achados = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'details' and 'info-i' in (a.get('class') or '').split():
            self.achados.append(list(self.pilha))
        if tag not in self.VAZIAS:
            self.pilha.append((tag, a))

    def handle_endtag(self, tag):
        for i in range(len(self.pilha) - 1, -1, -1):
            if self.pilha[i][0] == tag:
                del self.pilha[i:]
                break


class CreditosLente3(unittest.TestCase):
    def test_camada_fechada_e_reversivel(self):
        # tools/creditos_i.py --verificar: cada ficheiro na versão nova, contagens exatas, desfazer e voltar a aplicar dá o mesmo
        r = subprocess.run([sys.executable, str(R / 'tools/creditos_i.py'), '--verificar'], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for f in creditos_i_lente3.TROCAS:
            with self.subTest(ficheiro=f):
                agora = ler(f)
                partida = creditos_i_lente3.desfazer(agora, f)
                self.assertEqual(partida, antigo(f))
                self.assertEqual(creditos_i_lente3.aplicar(partida, f), agora)
                self.assertEqual(creditos_i_lente3.alinhar(agora, f), agora)
                self.assertEqual(creditos_i_lente3.alinhar(partida, f), agora)

    def test_escape_dos_cartoes(self):
        # O utilitário escreve no manifesto o HTML corrido e trata o escape das cadeias JSON dos cartões, nos dois sentidos.
        h = '<figure class="x"><img alt="a \\ b"><figcaption>Fonte</figcaption></figure>'
        self.assertEqual(creditos_i.escapar(h, 'json'), '<figure class=\\"x\\"><img alt=\\"a \\\\ b\\"><figcaption>Fonte</figcaption></figure>')
        self.assertEqual(creditos_i.escapar(h, 'json/'), '<figure class=\\"x\\"><img alt=\\"a \\\\ b\\"><figcaption>Fonte<\\/figcaption><\\/figure>')
        for modo in (None, 'json', 'json/'):
            self.assertEqual(creditos_i.desescapar(creditos_i.escapar(h, modo), modo), h)
            # o mesmo HTML, posto numa cadeia JSON com o escape do modo, lê-se de volta igual
            if modo:
                self.assertEqual(json.loads('"' + creditos_i.escapar(h, modo) + '"'), h)
        self.assertRaises(ValueError, creditos_i.escapar, h, 'xml')
        # um estado misto (parte da camada aplicada) falha em vez de passar despercebido
        trocas = [('a1', 'b1', 1), ('a2', 'b2', 1)]
        self.assertEqual(creditos_i.alinhar('a1 a2', trocas), 'b1 b2')
        self.assertEqual(creditos_i.alinhar('b1 b2', trocas), 'b1 b2')
        self.assertRaises(AssertionError, creditos_i.alinhar, 'b1 a2 a2', trocas)
        modos = {t[3] for ts in creditos_i_lente3.MANIFESTO.values() for t in ts if len(t) == 4}
        self.assertEqual(modos, {'json', 'json/'})

    def test_peca_comum_igual_e_carregada(self):
        # A peça comum não muda neste pedido (é igual à do Português); cada página com «i» novo carrega-a uma vez, com o caminho
        # relativo certo, também nas pastas fundas.
        for f in ('assets/info-i.css', 'assets/info-i.js'):
            self.assertEqual(hashlib.sha256((R / f).read_bytes()).hexdigest(),
                             hashlib.sha256(subprocess.check_output(['git', 'show', f'{BASE}:{f}'], cwd=R)).hexdigest(), f)
        self.assertEqual(len(PAGINAS), 112)
        for f in PAGINAS:
            s = ler(f)
            with self.subTest(pagina=f):
                css = re.findall(r'<link rel="stylesheet" href="([^"]*assets/info-i\.css)\?v=' + V + '">', s)
                js = re.findall(r'<script defer src="([^"]*assets/info-i\.js)\?v=' + V + '"></script>', s)
                self.assertEqual((len(css), len(js)), (1, 1))
                for rel in css + js:
                    alvo = posixpath.normpath(posixpath.join(posixpath.dirname(f), rel))
                    self.assertTrue((R / alvo).is_file(), alvo)
                    self.assertIn(alvo, ('assets/info-i.css', 'assets/info-i.js'))
                # a folha da peça vem antes da folha da tabela de apoio (que tem de ficar depois dos estilos da página) e antes
                # da do «Para ver» (que tools/videos_escolhidos.py põe mesmo antes de </head>)
                cab = s[:s.index('</head>')]
                for depois in ('apoio-tabela.css', 'para-ver.css'):
                    if depois in cab:
                        self.assertLess(cab.index('assets/info-i.css'), cab.index(depois))

    def test_estrutura_de_cada_i(self):
        total = 0
        for f in PAGINAS:
            s = sem_escape(ler(f))
            ds = list(I_RE.finditer(s))
            with self.subTest(pagina=f):
                n = len(re.findall(r'<details class="info-i', s))
                # os «i» que já lá estavam (o da fotografia nas letras, info-i--linha mr-i, do pedido lente-1) não mudam
                self.assertEqual(n - len(ds), ANTES.get(f, 0))
                self.assertEqual(len(re.findall(r'<details class="info-i info-i--linha mr-i"', s)), ANTES.get(f, 0))
                novos = len(ds)
                self.assertGreater(novos, 0)
                total += novos
                for m in ds:
                    self.assertRegex(m.group(2), r'^Créditos d[aoe]s? ')
                    self.assertTrue(texto(m.group(3)))
                    for a in re.findall(r'<a [^>]*>', m.group(3)):
                        if 'creativecommons.org' in a:
                            self.assertRegex(a, r'^<a rel="license" href="https://creativecommons\.org/')
                        else:
                            self.assertRegex(a, r'^<a (data-external aria-label="[^"]+, sítio externo" )?href="')
                            if 'href="http' in a:
                                self.assertRegex(a, r'^<a data-external aria-label="[^"]+, sítio externo" href="https?://')
                    for x in (m.group(2), m.group(3)):
                        self.assertIsNone(PROIBIDAS.search(texto(x)), x)
                # mais de um «i» no mesmo cartão: cada um diz de que imagem é (os nomes não se repetem no mesmo ecrã)
                for cadeia in re.findall(r'"html": "((?:[^"\\]|\\.)*)"', ler(f)):
                    nomes = re.findall(r'<summary aria-label=\\"(Créditos[^"\\]+)\\">', cadeia)
                    self.assertEqual(len(nomes), len(set(nomes)), nomes)
                    if len(nomes) > 1:
                        self.assertTrue(all(': ' in x for x in nomes), nomes)
                p = Ancestrais()
                p.feed(s.replace('<script', '<x-script').replace('</script', '</x-script'))
                self.assertEqual(len(p.achados), n)
                for pilha in p.achados:
                    for tag, a in pilha:
                        self.assertNotIn(tag, ('a', 'button', 'label', 'figcaption', 'summary', 'p'))
                        self.assertNotEqual(a.get('aria-hidden'), 'true')
        self.assertEqual(total, 209)

    def test_l14_passos_casos_e_portal(self):
        # A frase que serve a pergunta fica à vista; o bloco «Autor. Direitos no registo de origem (Wikimedia Commons), consulta
        # de …» vai, inteiro e com a mesma ligação, para o «i», com a identificação da obra (autor, obra e data). Cada palavra da
        # legenda antiga fica à vista ou no «i»; nada se perde.
        paginas = [f for f in PAGINAS if re.search(r'<figure class=\\?"fig-cid', antigo(f))]
        self.assertEqual(len(paginas), 22)
        n = 0
        for f in paginas:
            velhas = figuras(sem_dados(sem_escape(antigo(f))), 'fig-cid')
            novas = figuras(sem_dados(sem_escape(ler(f))), 'fig-cid')
            self.assertEqual(len(velhas), len(novas), f)
            for velha, nova in zip(velhas, novas):
                with self.subTest(pagina=f, imagem=re.search(r'alt="([^"]{0,40})', velha).group(1)):
                    cap = re.search(r'<figcaption>(.*?)</figcaption>', velha, re.S).group(1)
                    bloco = re.search(r'(?:^|\. )([^.]*(?:\.(?! )[^.]*)*\. (?:Domínio público|Licença CC BY-SA 3\.0)[^<]* no registo de origem \(<a href="([^"]+)">Wikimedia Commons</a>\), consulta de [\d/-]+\.)$', cap)
                    self.assertIsNotNone(bloco, cap[-160:])
                    m = i_unico(nova)
                    self.assertIsNotNone(m)
                    self.assertIn('<div class="com-i"><img ', nova)
                    vis = texto(re.search(r'<figcaption>(.*?)</figcaption>', nova.replace(m.group(0), ''), re.S).group(1))
                    cred = texto(m.group(3))
                    # o bloco do crédito, palavra a palavra (a primeira letra pode ter passado a maiúscula), no fim do «i»
                    b = texto(bloco.group(1))
                    self.assertTrue(cred.endswith(b[1:]) and cred[-len(b)].lower() == b[0].lower(), (cred, b))
                    self.assertNotIn(b[1:], vis)
                    # a mesma ligação, com data-external e aria-label; a identificação da obra no começo do «i», antes do bloco (a
                    # que a legenda trazia: nos passos 07 e 10 do M1, que voltam a uma imagem sem a identificar, a dessa mesma imagem
                    # nos passos 01 e 02)
                    self.assertEqual(sem_licencas(ligacoes(m.group(3))), [bloco.group(2)])
                    ident = cred[:-len(b)].strip()
                    self.assertRegex(ident, r'^\S.*\.$')
                    self.assertTrue(texto(cap).startswith(ident) or ident.split(',')[0] in texto(cap), (ident, texto(cap)[:120]))
                    # nada se perde: as palavras da legenda antiga estão todas à vista ou no «i»
                    palavras = set(texto(cap).split())
                    self.assertTrue(palavras <= set(vis.split()) | {w.lower() for w in cred.split()} | set(cred.split()), palavras - set(vis.split()) - set(cred.split()))
                    # a imagem é a mesma
                    self.assertEqual(re.search(r'<img [^>]*>', velha).group(0).replace(' loading', '  loading')[:40], re.search(r'<img [^>]*>', nova).group(0).replace(' loading', '  loading')[:40])
                    n += 1
        self.assertEqual(n, 25)

    def test_l15_cartoes_com_fr_cred(self):
        # Só sai o span.fr-cred: passa, com o mesmo texto e as mesmas ligações, para o «i» no canto da imagem; o span.fr-leg fica.
        pat = re.compile(r'<figure class="(fig-rev[^"]*)"><span class="fr-moldura">(<img [^>]*>)</span><figcaption><span class="fr-leg">(.*?)</span> ?'
                         r'<span class="fr-cred">(.*?)</span></figcaption></figure>', re.S)
        contagem = {'L15': 0, 'L15b': 0, 'L15c': 0}
        for f in PAGINAS:
            velhas = list(pat.finditer(sem_escape(antigo(f))))
            if not velhas:
                continue
            novas = figuras(sem_escape(ler(f)), 'fig-rev')
            novas = [x for x in novas if 'fr-moldura com-i' in x]
            self.assertEqual(len(velhas), len(novas), f)
            for v, nova in zip(velhas, novas):
                with self.subTest(pagina=f, legenda=texto(v.group(3))[:40]):
                    m = i_unico(nova)
                    self.assertIsNotNone(m)
                    self.assertEqual(m.group(1), None)
                    self.assertTrue(nova.startswith(f'<figure class="{v.group(1)}"><div class="fr-moldura com-i">{v.group(2)}<details '), nova[:200])
                    self.assertTrue(nova.endswith(f'</details></div><figcaption><span class="fr-leg">{v.group(3)}</span></figcaption></figure>'), nova[-200:])
                    velho, novo = texto(v.group(4)), texto(m.group(3))
                    if f == 'narrativas/cigoli/index.html':
                        # o único conserto: sai o pedaço repetido e partido «, 1610-1613 (fotografia de.»; nada mais muda
                        velho = velho.replace(', 1610-1613 (fotografia de.', '.')
                    self.assertEqual(novo[:1].lower() + novo[1:], velho[:1].lower() + velho[1:])
                    self.assertEqual(sem_licencas(ligacoes(m.group(3))), ligacoes(v.group(4)))
                    for lic in re.findall(r'CC BY(?:-SA)? \d\.\d', velho):
                        self.assertIn(f'<a rel="license" href="https://creativecommons.org/licenses/{lic[3:].lower().replace(" ", "/")}/deed.pt">{lic}</a>', m.group(3))
                    self.assertNotIn('fr-cred', nova)
                    k = 'L15c' if f.startswith(L15C) else 'L15b' if f.startswith(('investigar/', 'projetos/', 'caderno/', 'etica/', 'estetica/', 'fachada/')) else 'L15'
                    contagem[k] += 1
        self.assertEqual(contagem, {'L15': 18, 'L15b': 26, 'L15c': 32})

    def test_l16_retratos_de_butler_e_singer(self):
        f = 'cidadania/m1/cid-m1-butler-singer/index.html'
        velhas = figuras(sem_escape(antigo(f)), 'pessoa-foto')
        novas = figuras(sem_escape(ler(f)), 'pessoa-foto')
        self.assertEqual((len(velhas), len(novas)), (2, 2))
        for velha, nova, quem in zip(velhas, novas, ('Judith Butler, Hamburgo, 2007.', 'Peter Singer, MIT, 2009.')):
            cap = re.search(r'<figcaption>(.*?)</figcaption>', velha).group(1)
            m = i_unico(nova)
            # variante «linha» (o retrato é pequeno): imagem, «i», legenda; à vista, só quem se vê, sem pontos médios
            self.assertEqual((m.group(1), m.group(2)), (' info-i--linha', 'Créditos da fotografia'))
            self.assertTrue(nova.endswith(m.group(0) + f'<figcaption>{quem}</figcaption></figure>'))
            self.assertEqual(sorted(texto(m.group(3)).replace(',', '').replace('.', '').split()), sorted(texto(cap).replace('·', '').replace(',', '').replace('.', '').split()))
            self.assertEqual(ligacoes(m.group(3)), ligacoes(cap))
            self.assertIn('rel="license"', m.group(3))
            self.assertNotIn('·', m.group(0))

    def test_l17_vozes_com_vz_fig(self):
        # 25 de Abril, nos dois lados (test_reciclagem_lente.py exige os cartões iguais), e as vozes Warhol e Paula Rego, que têm a
        # mesma estrutura e continuam publicadas: à vista, a primeira frase (o que se vê); no «i», a legenda inteira.
        esperado = {'cidadania/25-de-abril/index.html': 5, 'vozes/25-de-abril/index.html': 5, 'vozes/warhol/index.html': 5, 'vozes/paula-rego/index.html': 3}
        for f, n in esperado.items():
            velhas = [x for x in figuras(sem_escape(antigo(f)), 'vz-fig') if '<a ' in x]
            novas = [x for x in figuras(sem_escape(ler(f)), 'vz-fig') if 'info-i' in x]
            self.assertEqual((len(velhas), len(novas)), (n, n), f)
            for velha, nova in zip(velhas, novas):
                with self.subTest(pagina=f, imagem=re.search(r'src="([^"]+)"', velha).group(1)[-40:]):
                    cap = re.search(r'<figcaption>(.*?)</figcaption>', velha).group(1)
                    m = i_unico(nova)
                    vis = re.search(r'<figcaption>(.*?)</figcaption>', nova.replace(m.group(0), '')).group(1)
                    self.assertTrue(texto(cap).startswith(texto(vis) + ' '))
                    self.assertRegex(texto(vis), r'\d{4}\.$')
                    self.assertTrue(texto(m.group(3)).startswith(texto(cap).rstrip('.')), (texto(m.group(3)), texto(cap)))
                    self.assertTrue(set(ligacoes(cap)) <= set(ligacoes(m.group(3))))
                    self.assertIn('<div class="com-i"><img ', nova)
        # as cinco figuras com «i» são iguais, letra a letra, nos dois lados do 25 de Abril
        lados = [[x for x in figuras(sem_escape(ler(f)), 'vz-fig') if 'info-i' in x] for f in ('cidadania/25-de-abril/index.html', 'vozes/25-de-abril/index.html')]
        self.assertEqual(lados[0], lados[1])

    def test_l18_ler_a_cidade(self):
        # «Ler a cidade» (a antiga «Cidade antes da aula»): só sai o span.fa-cred, que passa inteiro para o «i»; o span.fa-leg fica.
        # Nas miniaturas da galeria (legenda escondida), o «i» fica por baixo da imagem (variante «linha»).
        pat = re.compile(r'<figure class="(foto-arq[^"]*)"[^>]*>(?:(?!</figure>).)*?<figcaption><span class="fa-leg">(.*?)</span> <span class="fa-cred">(.*?)</span></figcaption></figure>', re.S)
        n = minis = 0
        paginas = [f for f in PAGINAS if f.startswith('cidade/')]
        self.assertEqual(len(paginas), 15)
        for f in paginas:
            velhas = list(pat.finditer(sem_escape(antigo(f))))
            novas = figuras(sem_escape(ler(f)), 'foto-arq')
            self.assertEqual(len(velhas), len(novas), f)
            for v, nova in zip(velhas, novas):
                with self.subTest(pagina=f, legenda=texto(v.group(2))[:40]):
                    m = i_unico(nova)
                    self.assertIsNotNone(m)
                    self.assertEqual(texto(m.group(3)), texto(v.group(3)))
                    self.assertEqual(sem_licencas(ligacoes(m.group(3))), sem_licencas(ligacoes(v.group(3))))
                    self.assertEqual(set(ligacoes(m.group(3))), set(ligacoes(v.group(3))))
                    self.assertTrue(nova.endswith(f'<figcaption><span class="fa-leg">{v.group(2)}</span></figcaption></figure>'))
                    self.assertRegex(m.group(2), r'^Créditos da (fotografia|ilustração|gravura)')
                    mini = 'mini' in v.group(1).split()
                    self.assertEqual(m.group(1) == ' info-i--linha', mini)
                    minis += mini
                    n += 1
        self.assertEqual((n, minis), (82, 32))
        # com um «i» aberto na gaveta do lugar, o Escape fecha só o «i»; o seguinte fecha a gaveta
        self.assertIn('if(ev.key==="Escape"&&aberto&&!document.querySelector("details.info-i[open]"))fecha()', ler('cidade/index.html'))

    def test_l19_portal_da_cidadania(self):
        s = ler('cidadania/index.html')
        velho = antigo('cidadania/index.html')
        linha = re.search(r'<p class="cid-image-credits">(.*?)</p>', velho).group(1)
        self.assertNotIn('cid-image-credits', s)
        portas = re.findall(r'<div class="cid-porta com-i">(<a class="p-cartao" .*?</a>)(<details .*?</details>)</div>', s)
        self.assertEqual(len(portas), 3)
        for (porta, i), (href, autor) in zip(portas, re.findall(r'<a href="([^"]+)">([^<]+)</a>', linha)):
            self.assertIn(porta, velho)  # a ligação da porta fica igual, com o rótulo curto à vista
            m = I_RE.fullmatch(i)
            self.assertEqual(m.group(2), 'Créditos da imagem: ' + autor)
            self.assertIn(f'<small>{autor} · ', porta)
            self.assertTrue(texto(m.group(3)).startswith(autor + ', '))
            self.assertIn('domínio público', texto(m.group(3)))
            self.assertEqual(ligacoes(m.group(3)), [href])
        # a imagem da página (L14) também tem o seu «i»: todas as imagens do portal estão creditadas, por isso a linha sai
        self.assertEqual(len(re.findall(r'<img ', s)), 4)
        self.assertEqual(len(I_RE.findall(s)), 4)

    def test_fora_da_tabela_investigar_02_e_direitos_01(self):
        # «Como se investiga», passo 02: a mesma divisão do L14 (a identificação e a frase que serve a pergunta ficam; o bloco do
        # registo de origem vai, com a identificação e o acervo, para o «i»); dois «i» no mesmo cartão, cada um com o seu nome.
        f = 'investigar/passo-02/index.html'
        velhas = figuras(sem_dados(sem_escape(antigo(f))), 'fig-inv')
        novas = figuras(sem_dados(sem_escape(ler(f))), 'fig-inv')
        self.assertEqual((len(velhas), len(novas)), (2, 2))
        for velha, nova, nome in zip(velhas, novas, ('Fases da Lua', 'Leonardo da Vinci')):
            cap = re.search(r'<figcaption>(.*?)</figcaption>', velha).group(1)
            m = i_unico(nova)
            self.assertEqual(m.group(2), 'Créditos da imagem: ' + nome)
            vis = texto(re.search(r'<figcaption>(.*?)</figcaption>', nova.replace(m.group(0), '')).group(1))
            bloco = texto(re.search(r'Domínio público no registo de origem \(.*?consulta de [\d/]+\.', cap).group(0))
            self.assertTrue(texto(m.group(3)).endswith(bloco))
            self.assertNotIn('registo de origem', vis)
            self.assertEqual(set(texto(cap).split()), set(vis.split()) | set(texto(m.group(3)).split()))
            self.assertEqual(sem_licencas(ligacoes(m.group(3))), ligacoes(cap))
        # Direitos, passo 01: a legenda era só o crédito; vai inteira para o «i» e o texto alternativo diz o que se vê
        f = 'direitos/passo-01/index.html'
        velha = [x for x in figuras(sem_escape(antigo(f)), 'fig') if 'oscar-wilde-sarony' in x][0]
        nova = [x for x in figuras(sem_escape(ler(f)), 'fig') if 'oscar-wilde-sarony' in x][0]
        cap = re.search(r'<figcaption>(.*?)</figcaption>', velha).group(1)
        m = i_unico(nova)
        self.assertEqual(texto(m.group(3)), texto(cap))
        self.assertEqual(ligacoes(m.group(3)), ligacoes(cap))
        self.assertNotIn('<figcaption>', nova)
        self.assertIn('<div class="fig-i com-i"><img ', nova)
        self.assertRegex(nova, r'alt="[^"]{20,}"')

    def test_nenhum_credito_fora_do_i(self):
        # Nas famílias L14 a L19, nenhuma legenda nem linha de crédito fica com marcas de crédito fora do «i»; e em todo o sítio já
        # não há span.fr-cred, span.fa-cred, p.cid-image-credits nem legendas de crédito em fig-cid (fora das páginas que são o
        # destino dos créditos, cidadania/m1/imagens/ e cidadania/m2/imagens/, que ficam por extenso), pessoa-foto ou vz-fig.
        site = [p for p in R.rglob('*.html') if '.git' not in p.parts and 'node_modules' not in p.parts and p.parts[len(R.parts)] != 'tools']
        for p in site:
            rel = p.relative_to(R).as_posix()
            s = sem_escape(p.read_text('utf-8', errors='ignore'))
            with self.subTest(pagina=rel):
                self.assertNotRegex(s, r'class="(fr-cred|fa-cred|cid-image-credits)"')
                # as páginas de demonstração ficam de fora (plano, secção 4)
                if '/imagens/' in rel or rel.startswith('demonstracoes/'):
                    continue
                for cls in ('fig-cid', 'pessoa-foto', 'vz-fig', 'fig-rev', 'foto-arq', 'fig-inv', 'fig'):
                    for fig in figuras(sem_dados(s), cls):
                        resto = I_RE.sub('', fig)
                        for cap in re.findall(r'<figcaption>(.*?)</figcaption>', resto, re.S):
                            # o span.fr-leg e o span.fa-leg ficam como estavam (dizem o que se vê; decisão 153), mesmo quando
                            # nomeiam o arquivo de onde vem a imagem; fora deles não pode ficar marca nenhuma de crédito
                            cap = re.sub(r'<span class="f[ra]-leg">.*?</span>', '', cap, flags=re.S)
                            self.assertIsNone(MARCAS.search(cap), (cls, cap[:200]))

    def test_gerador_das_correcoes_do_m2(self):
        # O gerador das correções do M2 escreve o crédito como fica no «i» (a ligação com data-external e aria-label; no Jacquard do
        # exercício longo, a licença com a sua ligação): voltar a correr as correções não muda nenhuma página.
        sys.path.insert(0, str(R / 'tools'))
        import cidadania_m2_correcoes as c
        for p in c.paginas():
            s = ler(p)
            self.assertEqual(c.aplicar(s, p), s, p)
        corr = ler('tools/cidadania_m2_correcoes.py')
        self.assertEqual(corr.count('<a data-external aria-label=\\\\"Wikimedia Commons, sítio externo\\\\" href=\\\\"'), 2)
        self.assertEqual(corr.count('<a data-external aria-label=\\\\"loc.gov, sítio externo\\\\" href=\\\\"'), 2)
        self.assertIn('<a rel=\\\\"license\\\\" href=\\\\"https://creativecommons.org/licenses/by-sa/3.0/deed.pt\\\\">CC BY-SA 3.0</a>', corr)


def cartoes(f):
    s = ler(f)
    m = re.search(r'itens\s*:\s*', s)
    return json.JSONDecoder().raw_decode(s[m.end():])[0]


if __name__ == '__main__':
    unittest.main()
