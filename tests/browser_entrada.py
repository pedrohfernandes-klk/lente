from pathlib import Path
import json, mimetypes, os, unittest
from playwright.sync_api import sync_playwright
# A entrada do Lente no Chromium (25/10/2026, sistema de desenho «Cartaz», SISTEMA-DESENHO.md, aprovado pelo docente a 25/10): sem
# transbordo de 320 a 1857 px, sem erros de JavaScript, uma só região preta; a região «A seguir» mostra o encontro de Cidadania pela data
# de hoje (?hoje=), «Continuar» com uma peça acabada, e só factos na projeção (não lê o aparelho); no telemóvel abre-se só a porta do que
# vem a seguir; «Olhar de lado» mostra e esconde o texto; com movimento reduzido nada anima.
# O endereço publicado (https://pedrohfernandes-klk.github.io/lente/…) é servido a partir da cópia local; nada sai para a rede.
# Uso: python3 browser_entrada.py   (LENTE_RAIZ=<cópia do Lente> para correr fora da pasta tests do Lente)
R = Path(os.environ.get('LENTE_RAIZ') or Path(__file__).resolve().parents[1])
U = 'https://pedrohfernandes-klk.github.io/lente/'
T = lambda iso: int(__import__('datetime').datetime.fromisoformat(iso).timestamp() * 1000)
LICAO1 = {'lente-justica-licao-1': json.dumps({'lida': True, 't': T('2026-10-22T10:00:00')})}
TREINO = {'epi-treinos': json.dumps({'feitas': {'sem-olhos': T('2026-10-23T10:00:00')}})}


def servir(route):
    url = route.request.url
    if not url.startswith(U):
        return route.abort()  # o Google Fonts e o resto: a página tem de funcionar sem eles
    rel = url[len(U):].split('#')[0].split('?')[0]
    f = R / rel / 'index.html' if rel == '' or rel.endswith('/') else R / rel
    if not f.is_file():
        return route.fulfill(status=404, path=str(R / '404.html'), content_type='text/html; charset=utf-8')
    tipo = mimetypes.guess_type(str(f))[0] or 'application/octet-stream'
    route.fulfill(status=200, path=str(f), content_type=tipo + ('; charset=utf-8' if tipo.startswith('text/') else ''))


class EntradaNoNavegador(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        cls.b = cls.pw.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.b.close()
        cls.pw.stop()

    def abrir(self, q='?hoje=2026-10-25', largura=390, altura=844, guardado=None, movimento='reduce', esquema='light'):
        ctx = self.b.new_context(viewport={'width': largura, 'height': altura}, reduced_motion=movimento, color_scheme=esquema)
        ctx.route('**/*', servir)
        if guardado:
            ctx.add_init_script('(o=>{for(const k in o)localStorage.setItem(k,o[k])})(' + json.dumps(guardado) + ')')
        p = ctx.new_page()
        p.set_default_timeout(10000)
        self.erros = []
        p.on('pageerror', lambda e: self.erros.append(str(e)))
        p.goto(U + q, wait_until='load')
        p.wait_for_function('document.documentElement.classList.contains("cv")')
        return ctx, p

    def regiao(self, p):
        return ' '.join(p.locator('[data-proximo]').inner_text().split())

    def test_sem_transbordo_nem_erros(self):
        for w, h in ((320, 640), (390, 844), (1024, 768), (1280, 800), (1857, 1000)):
            for esquema in ('light', 'dark'):
                ctx, p = self.abrir(largura=w, altura=h, esquema=esquema)
                d = p.evaluate('({x:document.documentElement.scrollWidth-innerWidth,inv:document.querySelectorAll(".inverso").length,b:document.querySelectorAll(".botao").length})')
                self.assertEqual(d, {'x': 0, 'inv': 1, 'b': 1}, (w, esquema))
                self.assertEqual(self.erros, [], (w, esquema))
                ctx.close()

    def test_o_encontro_pela_data_de_hoje(self):
        casos = [('2026-10-25', '28/10', 'Perguntar e investigar', 'Obrigatória a 18/11'), ('2026-11-12', '18/11', 'Julgar com razões', 'Obrigatória neste encontro'),
                 ('2026-11-19', '25/11', 'Uma imagem, duas histórias', None), ('2026-12-01', 'M2', 'Os algoritmos', None)]
        for hoje, data, titulo, obr in casos:
            ctx, p = self.abrir(q=f'?hoje={hoje}')
            r = self.regiao(p)
            self.assertIn(data, r, hoje)
            self.assertIn(titulo, r, hoje)
            if obr:
                self.assertIn(obr.upper(), r.upper(), hoje)
            else:
                self.assertFalse(p.locator('[data-obr]').is_visible(), hoje)
            ctx.close()
        ctx, p = self.abrir(q='?hoje=2026-12-01')
        self.assertTrue(p.locator('[data-enc-a]').get_attribute('href').endswith('/lente/cidadania/m2/'))
        ctx.close()

    def test_continuar_com_uma_peca_acabada(self):
        ctx, p = self.abrir(guardado=LICAO1)
        r = self.regiao(p)
        self.assertIn('Justiça, lição 2: Pôr um preço à vida', r)
        self.assertIn('FEITO: TER JUÍZO, JUSTIÇA, LIÇÃO 1: O ELÉTRICO, 22/10', r.upper())
        self.assertTrue(p.locator('.proximo .botao').get_attribute('href').endswith('/lente/olhar-e-decidir/justica/licao-2/'))
        self.assertEqual(p.locator('[data-e="ter-juizo"]').text_content(), '1 de 7')
        self.assertIn('ganho', p.locator('[data-marca]').get_attribute('class'))
        ctx.close()

    def test_a_projecao_nao_le_o_aparelho(self):
        ctx, p = self.abrir(q='?hoje=2026-10-25&projetar=1', largura=1280, altura=800, guardado=LICAO1)
        r = self.regiao(p)
        self.assertIn('Perguntar e investigar', r)
        self.assertNotIn('Continuar', r)
        self.assertEqual(p.locator('.etq').count(), 0)
        self.assertEqual(p.evaluate('document.documentElement.scrollWidth-innerWidth'), 0)
        ctx.close()

    def test_no_telemovel_abre_se_a_porta_do_que_vem_a_seguir(self):
        ctx, p = self.abrir()
        self.assertEqual(p.eval_on_selector_all('[data-dobra].aberta', 'l=>l.map(e=>e.id)'), ['inicio-cidadania'])
        self.assertFalse(p.locator('#inicio-metodo .porta-dentro').is_visible())
        p.click('#inicio-metodo .porta-abre')
        self.assertTrue(p.locator('#inicio-metodo .porta-dentro').is_visible())
        self.assertEqual(p.get_attribute('#inicio-metodo .porta-abre', 'aria-expanded'), 'true')
        ctx.close()
        ctx, p = self.abrir(guardado=TREINO)
        self.assertEqual(p.eval_on_selector_all('[data-dobra].aberta', 'l=>l.map(e=>e.id)'), ['inicio-narrativas'])
        ctx.close()
        ctx, p = self.abrir(q='?hoje=2026-10-25#inicio-biblioteca')
        self.assertIn('inicio-biblioteca', p.eval_on_selector_all('[data-dobra].aberta', 'l=>l.map(e=>e.id)'))
        ctx.close()

    def test_olhar_de_lado(self):
        ctx, p = self.abrir(largura=1280, altura=800)
        b = p.locator('[data-olhar]')
        self.assertFalse(p.locator('.olhar-dep').is_visible())
        b.click()
        self.assertEqual(b.get_attribute('aria-pressed'), 'true')
        self.assertTrue(p.locator('.olhar-dep').is_visible())
        self.assertIn('crânio em anamorfose', p.locator('.olhar-dep').inner_text())
        b.click()
        self.assertFalse(p.locator('.olhar-dep').is_visible())
        ctx.close()

    def test_movimento_reduzido_nada_anima(self):
        ctx, p = self.abrir(largura=1280, altura=800)
        self.assertEqual(p.evaluate('document.getAnimations().length'), 0)
        ctx.close()


if __name__ == '__main__':
    unittest.main()
