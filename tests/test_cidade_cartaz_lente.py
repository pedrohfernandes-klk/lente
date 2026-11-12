"""08/11/2026: pedido cidade-cartaz-lente. A secção da cidade chama-se «Ler a cidade» nos dois sítios (nenhuma página nem script servido
diz «A cidade antes da aula», nem o nome do antigo anexo de fontes) e a entrada do Lente tem um cartão «Ler a cidade.» no mesmo componente do cartão «Português.»
(a.site-portal com fotografia, etiqueta e o «i» dos créditos), logo antes dele; a linha pequena repetida no cartão do Português sai.
As trocas estão no manifesto fechado tools/trocas/cidade-cartaz-lente-20261108.json (tests/cidade_cartaz_lente.py)."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

import cidade_cartaz_lente

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / 'tools'))
import entrada_temas_20261112  # noqa: E402
URL_CIDADE = 'https://pedrohfernandes-klk.github.io/lente/cidade/'
# 12/11/2026: pedido entrada-temas. Na entrada em quatro temas, «Ler a cidade» é o destino do tema 04 («Imagem, som e cidade»): o
# cartão «Ler a cidade.» (a.site-portal, com a fotografia do Tejo de 1907) dá lugar ao cartão do tema, no componente dos quatro temas
# (article.tm). Os testes da entrada passam a conferir esse cartão com a mesma força: lugar e componente, texto exato, ligação única,
# fotografia, crédito completo atrás do «i», regras de texto e enquadramento. A fotografia é do arquivo da escola (a mesma que a página
# da cidade usa na missão 17) e fica servida pelo próprio Lente; a do Tejo continua na página da cidade, como antes.
FOTO = 'img/arquivo/rua-da-boavista-carris-2026-720.webp'
CREDITO = 'Rua da Boavista, Lisboa. Fotografia: Arquivo da EPI, 2026.'
TEMAS = ['Justiça e vida em comum', 'Informação e mundo digital', 'Histórias e criação', 'Imagem, som e cidade']


class Arvore(HTMLParser):
    """Elementos com atributos, texto e filhos, o bastante para ler um cartão."""

    VAZIOS = {'img', 'br', 'meta', 'link', 'input', 'source', 'hr', 'wbr'}

    def __init__(self, fonte):
        super().__init__(convert_charrefs=True)
        self.raiz = {'tag': None, 'attrs': {}, 'filhos': [], 'texto': ''}
        self.pilha = [self.raiz]
        self.feed(fonte)

    def handle_starttag(self, tag, attrs):
        no = {'tag': tag, 'attrs': dict(attrs), 'filhos': [], 'texto': ''}
        self.pilha[-1]['filhos'].append(no)
        if tag not in self.VAZIOS:
            self.pilha.append(no)

    def handle_endtag(self, tag):
        for i in range(len(self.pilha) - 1, 0, -1):
            if self.pilha[i]['tag'] == tag:
                del self.pilha[i:]
                break

    def handle_data(self, data):
        for no in self.pilha:
            no['texto'] += data


def todos(no):
    for f in no['filhos']:
        yield f
        yield from todos(f)


def um(no, tag, classe=None):
    achados = [e for e in todos(no) if e['tag'] == tag and (classe is None or classe in e['attrs'].get('class', '').split())]
    assert len(achados) == 1, (tag, classe, len(achados))
    return achados[0]


class CartazLerACidade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pagina = (ROOT / 'index.html').read_text(encoding='utf-8')
        cls.cartoes = re.findall(r'<li><article class="tm"[^>]*>.*?</article></li>', cls.pagina, re.S)
        cls.cartao = cls.cartoes[-1]

    def test_cartao_antes_do_portugues_no_mesmo_componente(self):
        # 12/11/2026: o cartão da cidade é o último dos quatro temas, todos no mesmo componente e pela ordem aprovada; depois dos
        # temas vêm os acessos secundários e só então a faixa «Português e Exames», uma só vez.
        self.assertEqual([re.search(r'<h3 class="tm-n"><b aria-hidden="true">(\d\d)</b><a href="[^"]+">([^<]+)</a></h3>', c).groups() for c in self.cartoes],
                         list(zip(['01', '02', '03', '04'], TEMAS)))
        self.assertEqual(self.pagina.count('<article class="tm"'), 4)
        # os quatro cartões seguem-se sem nada pelo meio, dentro da lista dos temas
        self.assertIn('<ul class="tm-g">' + ''.join(self.cartoes) + '</ul></section>', self.pagina)
        for c in self.cartoes:
            self.assertRegex(c, r'^<li><article class="tm"(?: id="inicio-narrativas" tabindex="-1")?><div class="tm-img com-i"><img src="[^"]+" alt="[^"]+" width="\d+" height="\d+" loading="(?:eager|lazy)" decoding="async" style="object-position:\d+% \d+%"><details class="info-i" name="info-i">')
        self.assertEqual(self.pagina.count('<aside class="lente-pt lente-pt-linha" aria-label="Português e Exames">'), 1)
        self.assertLess(self.pagina.index(self.cartao), self.pagina.index('<section class="tm-mais"'))
        self.assertLess(self.pagina.index('<section class="tm-mais"'), self.pagina.index('<aside class="lente-pt lente-pt-linha"'))

    def test_texto_exato_ligacao_e_fotografia(self):
        cartao = Arvore(self.cartao).raiz
        a = um(um(cartao, 'h3', 'tm-n'), 'a')
        self.assertEqual(a['attrs']['href'], URL_CIDADE)
        # página do próprio Lente: ligação interna absoluta, sem rel="external" nem target
        self.assertNotIn('rel', a['attrs'])
        self.assertNotIn('target', a['attrs'])
        self.assertEqual(list(a['attrs']), ['href'])
        self.assertIn(
            '<div class="tm-corpo"><h3 class="tm-n"><b aria-hidden="true">04</b><a href="' + URL_CIDADE + '">Imagem, som e cidade</a></h3>'
            '<p class="tm-q">O que muda quando mudas o enquadramento?</p>'
            '<p class="tm-f">Lês uma rua como um texto, escolhes uma das 14 missões e explicas o que ficou fora da fotografia.</p>'
            '<span class="tm-seta" aria-hidden="true">→</span></div></article></li>', self.cartao)
        self.assertEqual(a['texto'], 'Imagem, som e cidade')
        self.assertEqual(um(cartao, 'p', 'tm-q')['texto'], 'O que muda quando mudas o enquadramento?')
        self.assertEqual(um(cartao, 'span', 'tm-seta')['texto'], '→')
        # a descrição vem da própria página da cidade: a abertura, as 14 missões e o percurso «Modos de ver»
        abertura = (ROOT / 'cidade/index.html').read_text(encoding='utf-8')
        self.assertIn('<p class="p-lead">Uma rua pode ser lida como um texto e', abertura)
        self.assertIn('As 14 missões são escolhas livres; podes trabalhar no bairro ou a partir das fotografias.', abertura)
        self.assertIn('discutir como o enquadramento muda o que percebemos', abertura)
        self.assertIn('Volta à fotografia e explica o que ficou fora dela.', abertura)
        self.assertEqual(len(re.findall(r'<a class="missao[^>]*href="([^"]+)"', abertura)), 14)
        imagem = um(cartao, 'div', 'tm-img')
        img = um(imagem, 'img')
        self.assertEqual(img['attrs']['src'], FOTO)
        self.assertTrue((ROOT / FOTO).is_file())
        self.assertEqual((img['attrs']['width'], img['attrs']['height']), ('720', '540'))
        # 08/11/2026 (revisão do #142): o alt fica curto. A fotografia fica abaixo da dobra em todas as larguras: carrega-se quando
        # se aproxima. 12/11/2026: a imagem já não está dentro da ligação; o alt descreve-a, sem pontos de meio.
        self.assertEqual(img['attrs']['alt'], 'Fotografia de uma rua reta de Lisboa: dois carris de elétrico no chão e uma fila de prédios até ao fundo.')
        self.assertEqual(img['attrs']['loading'], 'lazy')
        self.assertEqual(img['attrs']['decoding'], 'async')
        # a mesma fotografia do arquivo que a página da cidade usa na missão 17 (lá, no tamanho grande)
        self.assertIn('rua-da-boavista-carris-2026.jpg', abertura)
        self.assertIn('Fotografia: Arquivo da EPI, 2026.', (ROOT / 'cidade/m17/index.html').read_text(encoding='utf-8'))

    def test_credito_completo_no_i(self):
        cartao = Arvore(self.cartao).raiz
        d = um(cartao, 'details', 'info-i')
        self.assertEqual(d['attrs']['class'], 'info-i')
        self.assertEqual(d['attrs']['name'], 'info-i')
        self.assertNotIn('open', d['attrs'])
        s = um(d, 'summary')
        self.assertEqual(s['attrs']['aria-label'], 'Créditos da fotografia: Rua da Boavista')
        self.assertIn('<details class="info-i" name="info-i"><summary aria-label="Créditos da fotografia: Rua da Boavista">'
                      '<span aria-hidden="true">i</span></summary><p class="info-i-texto">' + CREDITO + '</p></details></div><div class="tm-corpo">', self.cartao)
        # o «i» fica fora da ligação do cartão, na moldura da imagem, e antes dela
        self.assertNotIn('info-i', re.search(r'<h3 class="tm-n">.*?</h3>', self.cartao, re.S)[0])
        self.assertLess(self.cartao.index('</details>'), self.cartao.index('<a '))
        # os outros três cartões têm o crédito no mesmo formato da casa: autor ou obra, «Wikimedia Commons» com data-external e
        # aria-label, e a licença no fim
        for c in self.cartoes[:3]:
            self.assertRegex(c, r'<p class="info-i-texto">[^<]+(?:<i>[^<]+</i>[^<]+)?<a data-external aria-label="Wikimedia Commons, sítio externo" '
                                r'href="https://commons\.wikimedia\.org/wiki/File:[^"]+">Wikimedia Commons</a>\. Domínio público\.</p></details></div>')

    def test_linha_repetida_sai_do_portugues(self):
        self.assertNotIn('sp-credit', self.pagina)
        self.assertNotIn('Ler a cidade: observar, criar e discutir o espaço comum', self.pagina)
        # 12/11/2026: o Português passa a ser uma faixa só com texto e a ligação de saída, sem fotografia e sem mais nada depois
        self.assertIn('<aside class="lente-pt lente-pt-linha" aria-label="Português e Exames"><p class="pt-f"><b>Português e Exames</b> ficam noutro sítio.</p>'
                      '<a class="pt-a" href="https://pedrohfernandes-klk.github.io/pt/" rel="external">Ir para Português e Exames <span aria-hidden="true">↗</span></a></aside>\n<footer class="cz-footer">', self.pagina)
        # a entrada só liga à cidade pelo cartão do tema
        self.assertEqual(self.pagina.count('href="' + URL_CIDADE + '"'), 1)
        self.assertEqual(self.pagina.count('/cidade/'), 1)

    def test_regras_de_texto_no_cartao(self):
        # 12/11/2026: as mesmas regras, agora nos quatro cartões
        for c in self.cartoes:
            texto = re.sub(r'<[^>]+>', ' ', c)
            for proibido in ('·', '—', 'professor', 'jogar', 'jogo', 'ficha', 'folha'):
                self.assertNotIn(proibido, texto.lower(), proibido)
            self.assertNotIn('·', re.search(r'alt="([^"]*)"', c)[1])

    def test_enquadramento_da_fotografia_no_componente(self):
        css = (ROOT / 'assets/site-portals.css').read_text(encoding='utf-8')
        self.assertIn('.portal-portugues .sp-image img{object-position:50% 28%}\n', css)
        self.assertRegex(css, r'\n\.portal-cidade \.sp-image img\{object-position:[^}]+\}\n')
        # a folha mudou: a entrada pede a versão nova (cache)
        self.assertEqual(re.findall(r'assets/site-portals\.css\?v=([\w.-]+)', self.pagina), ['20261108-1'])
        # 12/11/2026: no cartão do tema, o enquadramento vem no próprio cartão e a folha dos temas corta a fotografia à caixa;
        # a entrada pede a folha dos temas com versão (cache)
        self.assertIn('style="object-position:50% 60%"', self.cartao)
        temas = (ROOT / 'assets/temas.css').read_text(encoding='utf-8')
        self.assertIn('[data-cartaz-entrada] .tm-img img{position:absolute;inset:0;display:block;width:100%;height:100%;object-fit:cover;', temas)
        self.assertEqual(re.findall(r'assets/temas\.css\?v=([\w.-]+)', self.pagina), ['20261112-1'])

    def test_nome_unico_em_paginas_e_scripts(self):
        # 08/11/2026 (revisão do #142): também o nome escrito de outras formas (maiúsculas, hífenes, sublinhados, como no nome do
        # antigo ANEXO-A-CIDADE-ANTES-DA-AULA.txt citado nas missões 02 e 16).
        antigo = re.compile(r'cidade[\W_]+antes[\W_]+da[\W_]+aula', re.I)
        achados = []
        for p in list(ROOT.rglob('*.html')) + list((ROOT / 'assets').rglob('*.js')):
            rel = p.relative_to(ROOT).as_posix()
            if rel.startswith(('docs/', 'node_modules/', '.git/')):
                continue
            if antigo.search(p.read_text(encoding='utf-8', errors='replace')):
                achados.append(rel)
        self.assertEqual(achados, [])
        for missao, nova in (('m02', 'e a nota editorial do anexo de fontes de Ler a cidade sobre os mapas ilustrados.'),
                             ('m16', 'e o anexo de fontes de Ler a cidade (a EPI na Rua D. Luís I).')):
            self.assertIn(nova, (ROOT / 'cidade' / missao / 'index.html').read_text(encoding='utf-8'), missao)
        registos = (ROOT / 'assets/progresso-registos.js').read_text(encoding='utf-8')
        self.assertIn('["^(epi-bairro|bairro-)", "Ler a cidade"],', registos)

    def test_manifesto_fechado_em_vigor(self):
        # cada «novo» está no ficheiro o número de vezes registado e nenhum «antigo» voltou (como tests/cidade_cartaz_lente.alinhar
        # o reconhece); o gerador do percurso anterior aplica a camada.
        self.assertGreaterEqual(len(cidade_cartaz_lente.TROCAS), 29)
        for ficheiro, trocas in cidade_cartaz_lente.TROCAS.items():
            texto = (ROOT / ficheiro).read_text(encoding='utf-8')
            # 12/11/2026: pedido entrada-temas. A camada da entrada em quatro temas é a mais recente (manifesto fechado
            # tests/fixtures/entrada-temas-20261112.json): desfaz-se primeiro, com contagem exata de cada «novo», e esta camada
            # confere-se, como antes, no ficheiro que fica (a entrada do main b8abe97).
            if ficheiro in entrada_temas_20261112.TROCAS:
                texto = entrada_temas_20261112.desfazer(texto, ficheiro)
            for antigo, novo, n in trocas:
                self.assertEqual(texto.count(novo), n, ficheiro)
                self.assertNotIn(antigo, texto, ficheiro)
            self.assertEqual(cidade_cartaz_lente.alinhar(texto, ficheiro), texto, ficheiro)
        gerador = (ROOT / 'tools/cidadania_m1_layout.py').read_text(encoding='utf-8')
        self.assertIn("tools/trocas/cidade-cartaz-lente-20261108.json", gerador)
        self.assertIn('for camada in (g146,g154,gi,gc):', gerador)


if __name__ == '__main__':
    unittest.main()
