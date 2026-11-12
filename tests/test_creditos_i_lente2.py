"""08/11/2026: decisões 153, 162 e 176 (pedido lente-2 do plano plano-creditos-i-20261105.md, famílias L8 a L13). Cada «i» novo
confere-se contra o main de partida (cc75fc6), página a página:

- o crédito que estava à vista está agora inteiro dentro do «i» (as mesmas palavras e as mesmas ligações; a ligação para a
  fonte leva data-external e aria-label, como no pedido lente-1, e a da licença CC leva rel="license"), e fora do «i» não fica
  crédito nenhum;
- o que fica à vista é só o que diz quem ou o que se vê: a legenda descritiva dos desenhos da Justiça, «Peter Singer no MIT,
  em 2009.», a descrição da fotografia de Eleanor Roosevelt, o aviso do vídeo e o aviso do exercício das duas fotografias de
  Lisboa; sem nada que diga o que se vê, o figcaption sai e o alt descreve a imagem;
- cada «i» tem a marcação da peça comum (details.info-i com name="info-i", summary com «Créditos…» e só a letra, um
  p.info-i-texto), vive fora de ligações, botões, rótulos, legendas e partes decorativas, e a página carrega a peça comum
  (assets/info-i.css e assets/info-i.js, que este pedido não muda);
- nada do que entrou traz «·», «—», «professor», «jogo», «jogar», «ficha» nem «folha»."""
import hashlib
import json
import re
import subprocess
import unittest
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

# 08/11/2026: decisões 153 e 176 (pedido lente-4). A regra da projeção da peça comum muda no pedido lente-4, pela camada fechada
# tools/trocas/creditos-i-lente4-20261108.json; para conferir a peça, desfaz-se essa camada, com contagem exata.
import creditos_i_lente4

R = Path(__file__).resolve().parents[1]
BASE = 'cc75fc62e18a731c671ad9f06f8fb708af6f7ddb'
PROIBIDAS = re.compile(r'(?<![\wÀ-ÿ])(?:professor(?:a|es|as)?|jog(?:ar|a[sm]?|o|os|ou|uei|ámos)|fichas?|folhas?)(?![\wÀ-ÿ])|—|·', re.I)
I_RE = re.compile(r'<details class="info-i( info-i--linha)?" name="info-i"><summary aria-label="([^"]+)"><span aria-hidden="true">i</span></summary>'
                  r'<p class="info-i-texto">(.*?)</p></details>', re.S)

# Os «i» novos, por página e por ordem: (família, imagem ou vídeo).
JUSTICA = {'olhar-e-decidir/justica/licao-1/index.html': 6, 'olhar-e-decidir/justica/licao-2/index.html': 3}
TER_JUIZO = {'olhar-e-decidir/estetica/licao-1/index.html': 2, 'olhar-e-decidir/etica/licao-1/index.html': 2, 'olhar-e-decidir/etica/licao-2/index.html': 1}
PILOTO = [f'cidadania/piloto/m1-s{n:02d}/index.html' for n in range(1, 11)]
IDEIAS = {'narrativas/ideias/sessao-01/index.html': 2, 'narrativas/ideias/sessao-02/index.html': 1}
M2 = {f'cidadania/m2/sessoes/{n:02d}/index.html': k for n, k in zip(range(1, 11), (3, 2, 1, 2, 3, 2, 2, 2, 1, 2))}
M2['cidadania/m2/sessoes/index.html'] = 1
M1 = ['cidadania/m1/index.html', 'cidadania/m1/sessoes/index.html', 'cidadania/m1/biblioteca/index.html', 'cidadania/m1/oficina-guiao/index.html']
TODAS = {**JUSTICA, **TER_JUIZO, **{p: 2 for p in PILOTO}, **IDEIAS, **M2, **{p: 1 for p in M1}}
# O que fica à vista, por cima do «i» (o resto da legenda antiga era só crédito).
A_VISTA = {'Peter Singer no MIT, em 2009.', 'Eleanor Roosevelt com o cartaz da Declaração Universal, Lake Success, Nova Iorque, novembro de 1949.'}


def ler(f):
    return (R / f).read_text('utf-8')


def antigo(f):
    return subprocess.check_output(['git', 'show', f'{BASE}:{f}'], cwd=R).decode('utf-8')


def sem_escape(s):
    """O HTML dos cartões como o motor o lê (aspas e «</» sem escape)."""
    return s.replace('\\"', '"').replace('<\\/', '</').replace('\\u00a0', ' ')


def texto(h):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', '', h))).strip()


def ligacoes(h):
    return re.findall(r'href="([^"]+)"', h)


def figuras(s):
    return re.findall(r'<figure\b[^>]*>.*?</figure>', s, re.S)


def i_da_figura(fig):
    ms = list(I_RE.finditer(fig))
    return ms[0] if len(ms) == 1 else None


class Ancestrais(HTMLParser):
    """Onde vive cada details.info-i: as etiquetas abertas por cima dele."""
    VAZIAS = {'img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'wbr', 'col', 'area'}

    def __init__(self):
        super().__init__()
        self.pilha, self.achados = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'details' and 'info-i' in (a.get('class') or '').split():
            self.achados.append([(t, x) for t, x in self.pilha])
        if tag not in self.VAZIAS:
            self.pilha.append((tag, a))

    def handle_endtag(self, tag):
        for i in range(len(self.pilha) - 1, -1, -1):
            if self.pilha[i][0] == tag:
                del self.pilha[i:]
                break


class CreditosLente2(unittest.TestCase):
    def test_peca_comum_igual_e_carregada(self):
        # A peça comum não muda neste pedido (é igual à do Português); cada página com «i» novo carrega-a uma vez.
        # 08/11/2026: pedido lente-4. Desfeita a camada do lente-4 (só a regra da projeção), a peça continua igual, byte a byte, à do
        # main de partida deste pedido.
        for f in ('assets/info-i.css', 'assets/info-i.js'):
            self.assertEqual(hashlib.sha256(creditos_i_lente4.desfazer(ler(f), f).encode('utf-8')).hexdigest(),
                             hashlib.sha256(subprocess.check_output(['git', 'show', f'{BASE}:{f}'], cwd=R)).hexdigest(), f)
        for f in TODAS:
            s = ler(f)
            with self.subTest(pagina=f):
                self.assertEqual(len(re.findall(r'assets/info-i\.css\?v=20261106-3"', s)), 1)
                self.assertEqual(len(re.findall(r'assets/info-i\.js\?v=20261106-3"', s)), 1)

    def test_estrutura_de_cada_i(self):
        total = 0
        for f, n in TODAS.items():
            s = sem_escape(ler(f))
            ds = list(I_RE.finditer(s))
            with self.subTest(pagina=f):
                # todos os details.info-i da página têm a marcação da peça comum, e são os esperados
                self.assertEqual(len(re.findall(r'<details class="info-i', s)), n)
                self.assertEqual(len(ds), n)
                for m in ds:
                    self.assertRegex(m.group(2), r'^Créditos d[aoe]s? ')
                    self.assertTrue(texto(m.group(3)))
                    for a in re.findall(r'<a [^>]*>', m.group(3)):
                        if 'creativecommons.org' in a:
                            self.assertIn('rel="license"', a)
                        elif 'href="https://' in a or 'href="http://' in a:
                            self.assertRegex(a, r'^<a data-external aria-label="[^"]+, sítio externo" href="https?://')
                    for x in (m.group(2), m.group(3)):
                        self.assertIsNone(PROIBIDAS.search(texto(x)), x)
                p = Ancestrais()
                # os cartões vêm em JSON dentro de <script>: lê-se o HTML deles como o motor o põe na página
                p.feed(s.replace('<script', '<x-script').replace('</script', '</x-script'))
                self.assertEqual(len(p.achados), n)
                for pilha in p.achados:
                    for tag, a in pilha:
                        self.assertNotIn(tag, ('a', 'button', 'label', 'figcaption', 'summary', 'p'))
                        self.assertNotEqual(a.get('aria-hidden'), 'true')
            total += n
        self.assertEqual(total, 62)

    def comparar_figuras(self, f, antigas, novas):
        """Cada figura antiga com crédito na legenda passa a ter o crédito inteiro no «i» e, à vista, só o que diz o que se vê."""
        self.assertEqual(len(antigas), len(novas), f)
        for velha, nova in zip(antigas, novas):
            cap = re.search(r'<figcaption>(.*?)</figcaption>', velha, re.S).group(1)
            m = i_da_figura(nova)
            self.assertIsNotNone(m, nova[:120])
            self.assertEqual(texto(m.group(3)), texto(cap), f)
            # as mesmas ligações; a licença CC que só vinha em texto ganha a ligação para a licença (piloto, sessão 01)
            self.assertEqual([h for h in ligacoes(m.group(3)) if 'creativecommons.org' not in h], [h for h in ligacoes(cap) if 'creativecommons.org' not in h], f)
            self.assertTrue(set(ligacoes(cap)) <= set(ligacoes(m.group(3))), f)
            resto = nova.replace(m.group(0), '')
            vis = re.search(r'<figcaption>(.*?)</figcaption>', resto, re.S)
            if vis:
                self.assertIn(texto(vis.group(1)), A_VISTA, f)
                self.assertTrue(texto(cap).startswith(texto(vis.group(1))), f)
            else:
                self.assertRegex(resto, r'<img [^>]*alt="[^"]{20,}"', f)
            self.assertEqual(re.search(r'<img [^>]*src="([^"]+)"', velha).group(1), re.search(r'<img [^>]*src="([^"]+)"', nova).group(1))

    def test_l8_desenhos_da_justica(self):
        # A legenda descritiva fica; «Grafismo gerado com recurso a IA.» passa da legenda para o «i» de cada desenho.
        for f, n in JUSTICA.items():
            velhas = [x for x in figuras(sem_escape(antigo(f))) if 'class="desenho"' in x]
            novas = [x for x in figuras(sem_escape(ler(f))) if 'class="desenho"' in x]
            self.assertEqual((len(velhas), len(novas)), (n, n), f)
            for velha, nova in zip(velhas, novas):
                desc, cred = re.search(r'<figcaption>([^<]+) <span class="cred">([^<]+)</span></figcaption>', velha).groups()
                m = i_da_figura(nova)
                self.assertEqual(m.group(3), cred)
                self.assertEqual(m.group(2), 'Créditos do desenho: ' + desc.split(':', 1)[0])
                self.assertTrue(nova.endswith('</details><figcaption>' + desc + '</figcaption></figure>'), nova[-200:])
                self.assertEqual(re.search(r'<svg.*?</svg>', velha, re.S).group(0), re.search(r'<svg.*?</svg>', nova, re.S).group(0))

    def test_l9_etica_e_estetica(self):
        for f, n in TER_JUIZO.items():
            velhas = [x for x in figuras(sem_escape(antigo(f))) if 'class="fig"' in x and '<figcaption>' in x]
            novas = [x for x in figuras(sem_escape(ler(f))) if 'class="fig"' in x and 'info-i' in x]
            self.assertEqual(len(velhas), n, f)
            self.comparar_figuras(f, velhas, novas)

    def test_l10_imagens_do_piloto_e_do_ideias(self):
        for f in PILOTO + list(IDEIAS):
            velhas = [x for x in figuras(sem_escape(antigo(f))) if 'fig inteiro' in x]
            novas = [x for x in figuras(sem_escape(ler(f))) if 'fig inteiro' in x]
            self.assertEqual(len(velhas), 1, f)
            for nova in novas:
                self.assertIn('<div class="moldura com-i">', nova)
                self.assertNotIn('<span class="moldura">', nova)
            self.comparar_figuras(f, velhas, novas)

    def test_l11_videos(self):
        # Vai para o «i» só o crédito (canal e quem fala); o aviso do YouTube e o pedido das legendas ficam à vista, ao lado.
        for f in PILOTO + ['narrativas/ideias/sessao-01/index.html']:
            velho = re.search(r'<p class="yt-cred">(.*?)</p></div>', sem_escape(antigo(f))).group(1)
            novo = re.search(r'<div class="yt-pe"><p class="yt-cred">(.*?)</p>(<details .*?</details>)</div></div>', sem_escape(ler(f)))
            m = I_RE.fullmatch(novo.group(2))
            self.assertEqual((m.group(1), m.group(2)), (' info-i--linha', 'Créditos do vídeo'), f)
            self.assertEqual(texto(m.group(3) + ' ' + novo.group(1)), texto(velho), f)
            self.assertTrue(novo.group(1).endswith('O vídeo só se liga ao YouTube quando tocas no botão.'), f)
            self.assertNotRegex(novo.group(1), r'TED|lição de|conferência de', f)

    def test_l12_sessoes_do_m2(self):
        for f, n in M2.items():
            velhas = [x for x in figuras(antigo(f)) if '<img' in x and 'c10-par' not in x]
            novas = [x for x in figuras(ler(f)) if '<img' in x and 'c10-par' not in x]
            self.comparar_figuras(f, velhas, novas)
            for nova in novas:
                self.assertIn('<div class="com-i"><img ', nova)
        # as duas fotografias de Lisboa (s05): um «i» por baixo das duas; o aviso do exercício fica à vista
        f = 'cidadania/m2/sessoes/05/index.html'
        velha = next(x for x in figuras(antigo(f)) if 'c10-par' in x)
        nova = next(x for x in figuras(ler(f)) if 'c10-par' in x)
        cap = re.search(r'<figcaption>(.*?)</figcaption>', velha).group(1)
        m = i_da_figura(nova)
        self.assertEqual(m.group(1), ' info-i--linha')
        self.assertTrue(nova.endswith('</details><figcaption>Uma das versões foi alterada por nós.</figcaption></figure>'))
        self.assertEqual(texto(m.group(3)) + ' Uma das versões foi alterada por nós.', texto(cap))
        self.assertEqual(ligacoes(m.group(3)), ligacoes(cap))

    def test_l13_paginas_do_m1_com_a_ligacao_creditos(self):
        # O figcaption curto (autor, obra e a ligação «Créditos», separados por pontos médios) sai; o «i» leva o crédito em frases, sem pontos médios, com a licença,
        # o registo e a ligação para a página dos créditos do módulo (cidadania/m1/imagens/), como lá estão.
        imagens = antigo('cidadania/m1/imagens/index.html')
        for f in M1:
            velha = figuras(antigo(f))[0]
            nova = figuras(ler(f))[0]
            cap = re.search(r'<figcaption>(.*?)</figcaption>', velha).group(1)
            m = i_da_figura(nova)
            self.assertNotIn('<figcaption>', nova)
            partes = texto(cap).split(' · ')
            self.assertEqual(partes[-1], 'Créditos')
            for parte in partes[:-1]:
                for palavra in re.split(r',\s*', parte):
                    self.assertIn(palavra, texto(m.group(3)), f)
            self.assertIn(ligacoes(cap)[0], ligacoes(m.group(3)), f)
            self.assertNotIn('·', m.group(0))
            self.assertIn('Domínio público.', texto(m.group(3)))
            # a licença, o registo e o alt vêm da página dos créditos do módulo, sem palavras novas
            autor = partes[0]
            reg = next(c for c in re.findall(r'<img [^>]*>\s*<figcaption>.*?</figcaption>', imagens, re.S) if '<figcaption>' + autor + ', ' in c)
            self.assertIn(re.search(r'alt="([^"]+)"', reg).group(1), nova)
            self.assertIn(re.findall(r'href="(https://commons[^"]+)"', reg)[0], ligacoes(m.group(3)))

    def test_nenhum_credito_fora_do_i(self):
        # Nas páginas tocadas, nenhuma legenda nem linha de crédito conhecida fica com marcas de crédito fora do «i».
        marcas = re.compile(r'Domínio público|domínio público|CC BY|CC0|Wikimedia Commons|commons\.wikimedia|Grafismo gerado com recurso a IA|'
                            r'Fotografia de|Library of Congress|Biblioteca Presidencial|Metropolitan|Open Access|TED-Ed|lição de|loc\.gov|>Créditos<')
        for f in TODAS:
            s = I_RE.sub('', sem_escape(ler(f)))
            with self.subTest(pagina=f):
                for bloco in re.findall(r'<figcaption>(.*?)</figcaption>|<p class="yt-cred">(.*?)</p>|<span class="cred">(.*?)</span>', s, re.S):
                    self.assertIsNone(marcas.search(''.join(bloco)), bloco)


if __name__ == '__main__':
    unittest.main()
