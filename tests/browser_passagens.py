from pathlib import Path
import mimetypes, os, re, unittest
from playwright.sync_api import sync_playwright
# As páginas de passagem no Chromium (plano de reestruturação do Lente, secção 4): um endereço antigo aberto com «?projetar=1» e uma
# âncora chega ao destino com as duas; sem âncora, chega à âncora do destino; sem JavaScript, o meta refresh leva ao destino.
# O endereço publicado (https://pedrohfernandes-klk.github.io/lente/…) é servido a partir da cópia local; nada sai para a rede.
# Uso: python3 browser_passagens.py   (LENTE_RAIZ=<cópia do Lente> para correr fora da pasta tests do Lente)
R = Path(os.environ.get('LENTE_RAIZ') or Path(__file__).resolve().parents[1])
U = 'https://pedrohfernandes-klk.github.io/lente/'
FORA = {'tests', 'docs', 'assets', 'img', 'fontes'}


def passagens():
    L = []
    for p in sorted(R.rglob('index.html')):
        rel = p.relative_to(R)
        if set(rel.parts[:1]) & FORA:
            continue
        s = p.read_text('utf-8')
        if re.search(r'<html[^>]*\bdata-passagem\b', s) and 'location.replace(' in s:
            d = re.search(r'<link rel="canonical" href="([^"]+)">', s).group(1)
            a = re.search(r'location\.hash\|\|"([^"]*)"', s).group(1)
            L.append(('/'.join(rel.parts[:-1]) + '/', d, a))
    return L


def servir(route):
    url = route.request.url
    if not url.startswith(U):
        return route.abort()
    rel = url[len(U):].split('#')[0].split('?')[0]
    f = R / rel / 'index.html' if rel == '' or rel.endswith('/') else R / rel
    if not f.is_file():
        return route.fulfill(status=404, path=str(R / '404.html'), content_type='text/html; charset=utf-8')
    tipo = mimetypes.guess_type(str(f))[0] or 'application/octet-stream'
    route.fulfill(status=200, path=str(f), content_type=tipo + ('; charset=utf-8' if tipo.startswith('text/') else ''))


class PassagensNoNavegador(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.L = passagens()
        cls.pw = sync_playwright().start()
        cls.b = cls.pw.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.b.close()
        cls.pw.stop()

    def abrir(self, url, js=True):
        ctx = self.b.new_context(java_script_enabled=js, reduced_motion='reduce')
        ctx.route('**/*', servir)
        p = ctx.new_page()
        p.set_default_timeout(10000)
        p.goto(url, wait_until='commit')
        return ctx, p

    def test_ha_passagens(self):
        self.assertTrue(self.L, 'nenhuma página de passagem no Lente')

    def test_guarda_projetar_e_ancora(self):
        for de, d, a in self.L:
            with self.subTest(de=de):
                ctx, p = self.abrir(f'{U}{de}?projetar=1#teste-ancora')
                p.wait_for_url(f'{d}?projetar=1#teste-ancora')
                self.assertEqual(p.url, f'{d}?projetar=1#teste-ancora')
                ctx.close()

    def test_sem_ancora_vai_a_ancora_do_destino(self):
        for de, d, a in self.L:
            with self.subTest(de=de):
                ctx, p = self.abrir(f'{U}{de}?projetar=1')
                p.wait_for_url(f'{d}?projetar=1{a}')
                self.assertEqual(p.url, f'{d}?projetar=1{a}')
                ctx.close()

    def test_sem_javascript_o_meta_refresh_leva_ao_destino(self):
        for de, d, a in self.L:
            with self.subTest(de=de):
                ctx, p = self.abrir(f'{U}{de}', js=False)
                p.wait_for_url(f'{d}{a}')
                self.assertEqual(p.url, f'{d}{a}')
                ctx.close()


if __name__ == '__main__':
    unittest.main()
