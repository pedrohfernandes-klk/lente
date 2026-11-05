"""05/11/2026: decisão 147 (Laboratório sem o Português). As peças que dependiam do Português saem do Laboratório;
cada endereço fica como redirecionamento para o Laboratório e nenhuma página do Lente continua a levar até lá."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json, posixpath, re, unittest

R = Path(__file__).resolve().parents[1]
ABS = 'https://pedrohfernandes-klk.github.io/lente/'
RET = json.loads((R / 'assets/laboratorio/retiradas.json').read_text('utf-8'))['retiradas']
URLS = {x['url'] for x in RET}
D = json.loads((R / 'assets/laboratorio/percursos.json').read_text('utf-8'))


def paginas():
    for p in sorted(R.rglob('*.html')):
        rel = p.relative_to(R).as_posix()
        if rel.split('/')[0] in ('.git', 'tests', 'docs', '_qa', 'node_modules'):
            continue
        yield rel, p.read_text('utf-8')


class Retiradas(unittest.TestCase):
    def test_lista_coerente(self):
        self.assertGreaterEqual(len(RET), 18)
        self.assertEqual(len(URLS), len(RET))
        nomes = {'narrativas/'} | {'narrativas/' + b['id'] + '/' for b in D['blocks']}
        for x in RET:
            self.assertRegex(x['url'], r'^narrativas/[a-z0-9/-]+/$')
            self.assertIn(x['destino'], nomes, x['url'])
            self.assertTrue(x['titulo'].strip(), x['url'])
        vivas = {p['url'] for p in D['pieces']}
        self.assertFalse(URLS & vivas)
        ids = {u.removeprefix('narrativas/').rstrip('/') for u in URLS}
        self.assertFalse(ids & {i for r in D['routes'] for i in r['pieces']})
        self.assertFalse({'percursos/' + r['id'] for r in D['routes']} & ids)

    def test_cada_endereco_redireciona_para_o_laboratorio(self):
        for x in RET:
            with self.subTest(pagina=x['url']):
                s = (R / x['url'] / 'index.html').read_text('utf-8')
                destino = ABS + x['destino']
                self.assertTrue(s.startswith('<!doctype html><html lang="pt-PT" data-appearance-site="lente">'))
                self.assertIn('<meta http-equiv="refresh" content="0; url=' + destino + '">', s)
                self.assertIn('<link rel="canonical" href="' + destino + '">', s)
                self.assertIn('<meta name="robots" content="noindex">', s)
                self.assertIn('<a href="' + destino + '">', s)
                for proibido in ('EPIJogo', 'localStorage', '<script>', 'Português', 'Módulo'):
                    self.assertNotIn(proibido, s)
                self.assertTrue((R / x['destino'] / 'index.html').is_file())

    def test_nenhuma_pagina_leva_a_uma_peca_retirada(self):
        falhas = []
        for rel, s in paginas():
            if rel.removesuffix('index.html') in URLS:
                continue
            base = posixpath.dirname(rel)
            for href in re.findall(r'(?:href|src)=\\?"([^"\\]+)', s):
                u = urlsplit(href)
                if u.scheme in ('http', 'https'):
                    if not href.startswith(ABS):
                        continue
                    caminho = u.path.removeprefix('/lente/')
                elif u.scheme or not u.path:
                    continue
                else:
                    caminho = posixpath.normpath(posixpath.join(base, unquote(u.path)))
                    caminho = caminho + '/' if not caminho.endswith('.html') else caminho.removesuffix('index.html')
                if caminho in URLS:
                    falhas.append((rel, href))
        self.assertEqual(falhas, [])

    def test_dados_e_geradores_sem_pecas_retiradas(self):
        fontes = [p for p in (R / 'assets/laboratorio').glob('*.json') if p.name != 'retiradas.json']
        fontes += list((R / 'tools/licoes').glob('*.json')) + [R / 'tools/ideias_piloto.py']
        for p in fontes:
            s = p.read_text('utf-8')
            for u in URLS:
                with self.subTest(ficheiro=p.relative_to(R).as_posix(), peca=u):
                    self.assertNotIn(ABS + u, s)
                    self.assertNotIn('"' + u.removeprefix('narrativas/'), s)
                    self.assertNotIn("'" + u.removeprefix('narrativas/'), s)

    def test_reposicao_ignora_so_as_retiradas(self):
        ids = sorted(u.removeprefix('narrativas/').rstrip('/') for u in URLS if not u.startswith('narrativas/percursos/'))
        for rel in ('narrativas/index.html', 'narrativas/ver/index.html', 'narrativas/treinar/index.html', 'narrativas/criar/index.html'):
            s = (R / rel).read_text('utf-8')
            dados = json.loads(re.search(r'<script type="application/json" id="lab-retiradas">([^<]*)</script>', s).group(1))
            self.assertEqual(sorted(dados), ids, rel)
        js = (R / 'assets/laboratorio/percursos.js').read_text('utf-8')
        self.assertIn("!Object.hasOwn(by,r.id)&&RET.includes(r.id)", js)
        self.assertIn('for(const r of regs){if(!r||!Object.hasOwn(by,r.id)', js)


if __name__ == '__main__':
    unittest.main()
