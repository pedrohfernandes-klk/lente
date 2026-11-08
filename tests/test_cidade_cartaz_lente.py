"""2026-11-08: pedido cidade-cartaz-lente. A secção da cidade chama-se «Ler a cidade» nos dois sítios (nenhuma página nem script servido
diz «A cidade antes da aula») e a entrada do Lente tem um cartão «Ler a cidade.» no mesmo componente do cartão «Português.»
(a.site-portal com fotografia, etiqueta e o «i» dos créditos), logo antes dele; a linha pequena repetida no cartão do Português sai.
As trocas estão no manifesto fechado tools/trocas/cidade-cartaz-lente-20261108.json (tests/cidade_cartaz_lente.py)."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

import cidade_cartaz_lente

ROOT = Path(__file__).resolve().parents[1]
URL_CIDADE = 'https://pedrohfernandes-klk.github.io/lente/cidade/'
FOTO = 'https://pedrohfernandes-klk.github.io/pt/img/arquivo/tejo-1907-vela-e-cidade.jpg'
CREDITO = ('Fotografia de autor não identificado, publicada por H. C. White Co. em 1907. Domínio público. '
           '<a data-external aria-label="Fonte da fotografia, sítio externo" href="https://www.loc.gov/item/2021640928/">Fonte da fotografia</a>')


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
        cls.asides = re.findall(r'<aside class="site-portal-wrap"[^>]*>.*?</aside>', cls.pagina, re.S)

    def test_cartao_antes_do_portugues_no_mesmo_componente(self):
        self.assertEqual([re.search(r'aria-label="([^"]+)"', a)[1] for a in self.asides],
                         ['Explorar Ler a cidade', 'Explorar Português'])
        self.assertEqual(len(re.findall(r'<aside class="site-portal-wrap" aria-label="Explorar Ler a cidade">', self.pagina)), 1)
        cidade, portugues = self.asides
        # o cartão da cidade vem imediatamente antes do do Português, nada pelo meio
        self.assertIn(cidade + portugues, self.pagina)
        for a in (cidade, portugues):
            self.assertRegex(a, r'^<aside class="site-portal-wrap" aria-label="[^"]+"><a class="site-portal portal-[a-z]+" href="[^"]+"')

    def test_texto_exato_ligacao_e_fotografia(self):
        cartao = Arvore(self.asides[0]).raiz
        a = um(cartao, 'a', 'site-portal')
        self.assertEqual(a['attrs']['href'], URL_CIDADE)
        # página do próprio Lente: ligação interna absoluta, sem rel="external" nem target
        self.assertNotIn('rel', a['attrs'])
        self.assertNotIn('target', a['attrs'])
        self.assertEqual(a['attrs']['class'], 'site-portal portal-cidade')
        self.assertIn(
            '<span class="sp-copy"><span class="sp-kicker">Português × Cidadania</span>'
            '<strong class="sp-title">Ler a cidade<span aria-hidden="true">.</span></strong>'
            '<span class="sp-description">Uma rua pode ser lida como um texto. São 14 missões, no bairro ou a partir das fotografias.</span>'
            '<span class="sp-action">Entrar <span aria-hidden="true">→</span></span></span>', self.asides[0])
        self.assertEqual(um(a, 'span', 'sp-kicker')['texto'], 'Português × Cidadania')
        self.assertEqual(um(a, 'strong', 'sp-title')['texto'], 'Ler a cidade.')
        self.assertEqual(um(a, 'span', 'sp-action')['texto'], 'Entrar →')
        # a descrição vem do parágrafo de abertura da própria página da cidade
        abertura = (ROOT / 'cidade/index.html').read_text(encoding='utf-8')
        self.assertIn('<p class="p-lead">Uma rua pode ser lida como um texto e', abertura)
        self.assertIn('As 14 missões são escolhas livres; podes trabalhar no bairro ou a partir das fotografias.', abertura)
        imagem = um(a, 'span', 'sp-image')
        img = um(imagem, 'img')
        self.assertEqual(img['attrs']['src'], FOTO)
        self.assertEqual((img['attrs']['width'], img['attrs']['height']), ('1160', '773'))
        self.assertGreater(len(img['attrs']['alt']), 40)
        self.assertEqual(img['attrs']['decoding'], 'async')
        # a mesma fotografia, do mesmo endereço e com as mesmas medidas, que a página da cidade já usa
        self.assertIn(f'<img src="{FOTO}" alt="" width="1160" height="773"', abertura)
        self.assertEqual(um(imagem, 'span', 'sp-image-label')['texto'], 'Lisboa vista do Tejo, 1907')

    def test_credito_completo_no_i(self):
        cartao = Arvore(self.asides[0]).raiz
        d = um(cartao, 'details', 'info-i')
        self.assertEqual(d['attrs']['class'], 'info-i info-i--linha sp-i')
        self.assertEqual(d['attrs']['name'], 'info-i')
        self.assertNotIn('open', d['attrs'])
        s = um(d, 'summary')
        self.assertEqual(s['attrs']['aria-label'], 'Créditos da fotografia: Lisboa vista do Tejo')
        self.assertIn('<details class="info-i info-i--linha sp-i" name="info-i"><summary aria-label="Créditos da fotografia: Lisboa vista do Tejo">'
                      '<span aria-hidden="true">i</span></summary><p class="info-i-texto">' + CREDITO + '</p></details></aside>', self.asides[0])
        # o «i» fica fora da ligação do cartão, como no Português
        self.assertNotIn('info-i', re.search(r'<a class="site-portal.*?</a><details', self.asides[0], re.S)[0])
        # mesmo formato do crédito do cartão do Português: autor, licença e «Fonte da fotografia» com data-external e aria-label
        self.assertIn('<p class="info-i-texto">Retrato de autor não identificado. Domínio público. <a data-external aria-label="Fonte da '
                      'fotografia, sítio externo" href="https://commons.wikimedia.org/wiki/File:PessoaChapeu.jpg">Fonte da fotografia</a></p>',
                      self.asides[1])

    def test_linha_repetida_sai_do_portugues(self):
        self.assertNotIn('sp-credit', self.pagina)
        self.assertNotIn('Ler a cidade: observar, criar e discutir o espaço comum', self.pagina)
        # o Português fica com a sua fotografia e o seu «i», e nada mais depois deles
        self.assertTrue(self.asides[1].endswith('Fonte da fotografia</a></p></details></aside>'))
        # a entrada só liga à cidade pelo cartão novo
        self.assertEqual(self.pagina.count('href="' + URL_CIDADE + '"'), 1)

    def test_regras_de_texto_no_cartao(self):
        texto = re.sub(r'<[^>]+>', ' ', self.asides[0])
        for proibido in ('·', '—', 'professor', 'jogar', 'jogo', 'ficha', 'folha'):
            self.assertNotIn(proibido, texto.lower(), proibido)
        self.assertNotIn('·', re.search(r'alt="([^"]*)"', self.asides[0])[1])

    def test_enquadramento_da_fotografia_no_componente(self):
        css = (ROOT / 'assets/site-portals.css').read_text(encoding='utf-8')
        self.assertIn('.portal-portugues .sp-image img{object-position:50% 28%}\n', css)
        self.assertRegex(css, r'\n\.portal-cidade \.sp-image img\{object-position:[^}]+\}\n')
        # a folha mudou: a entrada pede a versão nova (cache)
        self.assertEqual(re.findall(r'assets/site-portals\.css\?v=([\w.-]+)', self.pagina), ['20261108-1'])

    def test_nome_unico_em_paginas_e_scripts(self):
        achados = []
        for p in list(ROOT.rglob('*.html')) + list((ROOT / 'assets').rglob('*.js')):
            rel = p.relative_to(ROOT).as_posix()
            if rel.startswith(('docs/', 'node_modules/', '.git/')):
                continue
            if 'cidade antes da aula' in p.read_text(encoding='utf-8', errors='replace').lower():
                achados.append(rel)
        self.assertEqual(achados, [])
        registos = (ROOT / 'assets/progresso-registos.js').read_text(encoding='utf-8')
        self.assertIn('["^(epi-bairro|bairro-)", "Ler a cidade"],', registos)

    def test_manifesto_fechado_em_vigor(self):
        # cada «novo» está no ficheiro o número de vezes registado e nenhum «antigo» voltou (como tests/cidade_cartaz_lente.alinhar
        # o reconhece); o gerador do percurso anterior aplica a camada.
        self.assertGreaterEqual(len(cidade_cartaz_lente.TROCAS), 26)
        for ficheiro, trocas in cidade_cartaz_lente.TROCAS.items():
            texto = (ROOT / ficheiro).read_text(encoding='utf-8')
            for antigo, novo, n in trocas:
                self.assertEqual(texto.count(novo), n, ficheiro)
                self.assertNotIn(antigo, texto, ficheiro)
            self.assertEqual(cidade_cartaz_lente.alinhar(texto, ficheiro), texto, ficheiro)
        gerador = (ROOT / 'tools/cidadania_m1_layout.py').read_text(encoding='utf-8')
        self.assertIn("tools/trocas/cidade-cartaz-lente-20261108.json", gerador)
        self.assertIn('for camada in (g146,g154,gi,gc):', gerador)


if __name__ == '__main__':
    unittest.main()
