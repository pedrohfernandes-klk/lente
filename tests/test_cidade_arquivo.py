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
        groups = re.findall(r'<section class="ferr-grupo".*?</section>', page, re.S)
        self.assertEqual(len(groups), 3)
        expected = [
            ('Ler e investigar', ['biblioteca', 'ler', 'investigar']),
            ('Criar e apresentar', ['ver-para-fazer', 'apresentar']),
            ('Citar e guardar', ['direitos', 'caderno']),
        ]
        for group, (title, destinations) in zip(groups, expected):
            self.assertIn(title, group)
            self.assertEqual([href.rstrip('/').split('/')[-1] for href in Links(group).hrefs], destinations)
        self.assertNotIn('data-sugestao=', page)
        self.assertNotIn('data-reabrir', page)
        self.assertNotIn('editorial-02.js', page)
        self.assertTrue((ROOT / 'narrativas/variantes/index.html').is_file())

    def test_tools_do_not_promote_fieldwork_or_archived_collection(self):
        page = (ROOT / 'index.html').read_text('utf-8')
        tools = re.search(r'<nav class="lente-ferr".*?</nav>', page, re.S).group()
        self.assertNotIn('/sidequests/', tools)
        self.assertNotIn('/cidade/', tools)
        self.assertEqual(len(Links(tools).hrefs), 7)
        self.assertIn('Português × Cidadania', page)
        self.assertIn('/lente/cidade/', page)

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
