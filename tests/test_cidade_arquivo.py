from pathlib import Path
from html.parser import HTMLParser
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.hrefs = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.hrefs.append(dict(attrs).get('href', ''))

class ArchiveAndFieldwork(unittest.TestCase):
    def test_tools_have_distinct_named_groups_and_no_promotional_banner(self):
        page = (ROOT / 'index.html').read_text('utf-8')
        # 01/11/2026: D5, mesmos três grupos em dobras abertas sem JavaScript.
        # 12/11/2026: pedido entrada-temas. Os três grupos em dobras dão lugar a quatro linhas com nome, sempre à vista e sem
        # JavaScript: «Ferramentas para trabalhar», «A minha aula», Biblioteca e Área do docente, cada uma com a lista exata dos
        # seus destinos, por ordem. O caderno passa para o rodapé e «Ver para fazer» fica no mapa (confere-se abaixo).
        groups = re.findall(r'<(nav|div) class="tm-linha(?: tm-so)?"[^>]*>(.*?)</\1>', page, re.S)
        self.assertEqual(len(groups), 4)
        expected = [
            ('Ferramentas para trabalhar', ['ler', 'investigar', 'praticar/#escrever', 'apresentar', 'direitos']),
            ('A minha aula', ['cidadania/m1', 'cidadania/m2']),
            ('Biblioteca', ['biblioteca']),
            ('Área do docente', ['docente']),
        ]
        for (_, group), (title, destinations) in zip(groups, expected):
            self.assertEqual(re.findall(r'<p class="tm-linha-t"[^>]*>([^<]+)</p>', group), [title])
            self.assertEqual([href.removeprefix('https://pedrohfernandes-klk.github.io/lente/').rstrip('/') for href in Links(group).hrefs], destinations)
        self.assertEqual(page.count('class="tm-linha'), 4 + 6)  # as quatro linhas, mais os quatro títulos e as duas descrições
        self.assertNotIn('<details class="ferr-grupo', page)
        footer = re.search(r'<nav class="cz-footer-links".*?</nav>', page, re.S).group()
        self.assertEqual(Links(footer).hrefs, ['caderno/', 'como/', 'mapa/'])
        mapa = (ROOT / 'mapa/index.html').read_text('utf-8')
        self.assertIn('href="https://pedrohfernandes-klk.github.io/lente/ver-para-fazer/"', mapa)
        self.assertIn('href="https://pedrohfernandes-klk.github.io/lente/caderno/"', mapa)
        self.assertNotIn('data-sugestao=', page)
        self.assertNotIn('data-reabrir', page)
        self.assertNotIn('editorial-02.js', page)
        self.assertTrue((ROOT / 'narrativas/variantes/index.html').is_file())

    def test_tools_do_not_promote_fieldwork_or_archived_collection(self):
        page = (ROOT / 'index.html').read_text('utf-8')
        # 12/11/2026: pedido entrada-temas. As ferramentas passam a ser a linha nav#ferramentas («Ferramentas para trabalhar»): cinco
        # ligações (antes sete: a Biblioteca tem linha própria, o caderno está no rodapé e «Ver para fazer» no mapa), sem o arquivo
        # nem a cidade. A cidade deixa o cartão «Português × Cidadania» e é o destino do tema 04, com uma só ligação.
        tools = re.search(r'<nav class="tm-linha" id="ferramentas".*?</nav>', page, re.S).group()
        self.assertNotIn('/sidequests/', tools)
        self.assertNotIn('/cidade/', tools)
        self.assertEqual(len(Links(tools).hrefs), 5)
        self.assertNotIn('/sidequests/', page)
        self.assertEqual(page.count('<h3 class="tm-n"><b aria-hidden="true">04</b><a href="https://pedrohfernandes-klk.github.io/lente/cidade/">Imagem, som e cidade</a></h3>'), 1)
        self.assertEqual(page.count('/lente/cidade/'), 1)

    def test_archive_keeps_all_fourteen_destinations(self):
        teacher = (ROOT / 'docente/index.html').read_text('utf-8')
        self.assertIn('../sidequests/', teacher)
        archive = (ROOT / 'sidequests/index.html').read_text('utf-8')
        missions = re.findall(r'<a class="missao[^>]*href="([^"]+)"', archive)
        self.assertEqual(len(missions), 14)
        for href in missions:
            self.assertTrue((ROOT / 'sidequests' / href / 'index.html').is_file(), href)
        self.assertIn('epi-sidequests', archive)
        self.assertIn('Não constituem um percurso obrigatório', archive)

    def test_shared_route_and_all_city_missions_remain_reachable(self):
        city = (ROOT / 'cidade/index.html').read_text('utf-8')
        for href in ['m10/', '../cidadania/m1/passo-00/']:
            self.assertIn(href, Links(city).hrefs)
            self.assertTrue((ROOT / 'cidade' / href / 'index.html').is_file())
        self.assertIn('/pt/m6/licao-m6-f06/', city)
        missions = re.findall(r'<a class="missao[^>]*href="([^"]+)"', city)
        self.assertEqual(len(missions), 14)
        for href in missions:
            page = (ROOT / 'cidade' / href / 'index.html').read_text('utf-8')
            self.assertIn('Ler a cidade', page)
            self.assertIn('epi-bairro', page)

    def test_archive_is_not_automatically_suggested(self):
        found = 0
        for page in ROOT.rglob('*.html'):
            for order in re.findall(r'"ordem":\[([^\]]+)\]', page.read_text('utf-8')):
                if '"atlas"' in order:
                    found += 1
                    self.assertNotIn('"sidequests"', order, str(page))
        self.assertGreater(found, 10)

if __name__ == '__main__':
    unittest.main()
