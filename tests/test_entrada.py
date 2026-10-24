from pathlib import Path
import os, re, unittest
from urllib.parse import urlsplit
# Na pasta tests do Lente, a raiz é a pasta de cima; LENTE_RAIZ aponta para outra cópia.
R = Path(os.environ.get('LENTE_RAIZ') or Path(__file__).resolve().parents[1])
LENTE = 'https://pedrohfernandes-klk.github.io/lente/'
PT = 'https://pedrohfernandes-klk.github.io/pt/'
PROIBIDO = re.compile(r'(?<![\wÀ-ÿ])(?:professor(?:a|es|as)?|jog(?:ar|a|as|amos|am|ou|o)|fichas?|folhas?)(?![\wÀ-ÿ])|—', re.I)
# as entradas fora de Cidadania de onde a faixa das missões extra saiu no lote 1
SEM_FAIXA = ['investigar', 'direitos', 'apresentar', 'biblioteca', 'narrativas', 'narrativas/corta', 'narrativas/margens', 'ver-para-fazer']


def ler(rel):
    return (R / rel).read_text('utf-8')


def texto(s):
    s = re.sub(r'<(script|style|svg)[\s\S]*?</\1>', ' ', s)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))


def existe(href, de):
    """a ligação abre uma página desta árvore (os endereços do Lente, inteiros ou relativos a «de»); None se for para fora"""
    if href.startswith(LENTE):
        rel = urlsplit(href).path[len('/lente/'):]
    elif re.match(r'^[a-z]+:|^/|^#', href):
        return None
    else:
        rel = os.path.normpath(os.path.join(os.path.dirname(de), urlsplit(href).path)).replace('\\', '/')
        rel = '' if rel == '.' else rel + ('/' if href.split('#')[0].split('?')[0].endswith('/') else '')
    alvo = R / rel
    return (alvo / 'index.html').exists() if rel == '' or rel.endswith('/') or not alvo.suffix else alvo.exists()


class Entrada(unittest.TestCase):
    """A entrada nova do Lente (23/10/2026, plano de reestruturação, lote 1, secção 1, «O primeiro ecrã»)."""

    @classmethod
    def setUpClass(cls):
        cls.s = ler('index.html')

    def porta(self, id_):
        i = self.s.index(f'id="{id_}"')
        f = self.s.find('</li><li class="porta', i)
        return self.s[i:f if f > 0 else self.s.index('</ol>', i)]

    def test_seis_portas_por_ordem(self):
        self.assertEqual(re.findall(r'<h2 class="porta-n">(?:<a [^>]+>|<span>)([^<]+)', self.s), ['Cidadania', 'Laboratório', 'Ver para fazer', 'Método', 'Biblioteca', 'Vidas e vozes'])
        self.assertIn('<h2 class="porta-n"><span>Método</span></h2>', self.porta('inicio-metodo'))  # só rótulo, sem página
        for r in ('investigar/', 'direitos/', 'apresentar/', 'caderno/'):
            self.assertIn(f'href="{LENTE}{r}"', self.porta('inicio-metodo'))
        self.assertIn('<p class="porta-f">Os textos inteiros', self.porta('inicio-biblioteca'))
        self.assertIn(f'href="{LENTE}vozes/"', self.porta('inicio-vozes'))  # os Retratos chegam no lote 2, com o nome e o endereço novos

    def test_estado_continuar_e_sugestao(self):
        # cada linha que conta peças tem o lugar do estado em palavra; «Continuar» e a sugestão começam escondidos
        self.assertEqual(len(re.findall(r'<span class="l-e" data-e="[a-z0-9-]+"></span>', self.s)), 12)
        self.assertRegex(self.s, r'<section class="cont" data-cont hidden aria-label="Continuar">')
        self.assertIn('<p class="cont-s" hidden>', self.s)
        js = self.s[self.s.rindex('<script>'):]
        for p in ('"comecado":"Começado"', '"feito":"Feito"', 'É o método do projeto do Módulo 1.', 'Vem a seguir a «{de}».'):
            self.assertIn(p, js)
        self.assertNotIn('localStorage.setItem', js)  # a entrada só lê

    def test_rodape(self):
        rod = self.s[self.s.index('<footer class="rodape">'):]
        nomes = re.findall(r'<li><a href="[^"]+">([^<]+)</a></li>', rod[:rod.index('</ul>')])
        self.assertEqual(nomes[:3], ['Para o docente', 'Como se faz', 'Guardar o progresso'])
        self.assertIn(f'href="{LENTE}caderno/#progresso"', rod)
        self.assertIn('id="progresso"', ler('caderno/index.html'))  # «Guardar o progresso» abre o fim da página do caderno
        self.assertIn(f'<a class="pt" href="{PT}"', rod)
        self.assertRegex(rod, r'<figure class="cartaz"><svg[^>]*role="img"')
        self.assertRegex(rod, r'<figure class="fachada"><img src="[^"]+fachada-epi-2026\.jpg"')

    def test_o_que_saiu(self):
        for sai in ('lente/mapa/', 'Mapa do LENTE', 'data-sugestao', 'Uma experiência', 'mobile-jump', 'lente-ferr', 'site-portal-wrap'):
            self.assertNotIn(sai, self.s)
        # uma só folha de estilo, dentro da página
        self.assertEqual(len(re.findall(r'<style[ >]', self.s)), 1)
        self.assertNotIn('<link rel="stylesheet"', self.s)
        self.assertNotRegex(texto(self.s), PROIBIDO)

    def test_cada_ligacao_da_casca_abre_uma_pagina(self):
        for rel in ('index.html', '404.html', 'docente/index.html', 'docente/tudo/index.html', 'como/index.html'):
            s = ler(rel)
            for h in re.findall(r'href="([^"]+)"', s):
                self.assertIsNot(existe(h, rel), False, (rel, h))


class Casca(unittest.TestCase):
    """A página de erro, a porta do docente e as entradas que o lote 1 mexeu."""

    def test_pagina_de_erro_com_as_portas(self):
        s = ler('404.html')
        self.assertIn('<meta name="robots" content="noindex">', s)
        self.assertEqual(len(re.findall(r'<li><span aria-hidden="true">\d</span>', s)), 6)
        for r in ('cidadania/', 'narrativas/', 'ver-para-fazer/', 'investigar/', 'biblioteca/', 'vozes/'):
            self.assertIn(f'href="{LENTE}{r}"', s)  # endereços inteiros: o GitHub Pages serve-a em qualquer pasta
        self.assertNotRegex(texto(s), PROIBIDO)

    def test_porta_do_docente(self):
        s = ler('docente/index.html')
        lista = s[s.index('<ol class="porta-docente">'):s.index('</ol>', s.index('<ol class="porta-docente">'))]
        self.assertTrue(lista.startswith('<ol class="porta-docente"><li><a href="#guia-de-campo">'))
        self.assertIn('id="guia-de-campo"', s)
        self.assertIn('<a href="tudo/">', lista)
        self.assertIn(f'<a href="{PT}m4/aulas/">', lista)
        self.assertGreaterEqual(lista.count('<span class="pd-t">'), 5)  # o tempo de cada guia, quando o guia o diz
        self.assertNotIn('Mapa do LENTE', s)
        self.assertNotRegex(s, r'lente/mapa/|"(\.\./)+mapa/"')
        self.assertNotRegex(texto(s.replace('Mapa de Português', '')), r'—')

    def test_a_faixa_saiu_das_entradas_fora_de_cidadania(self):
        for d in SEM_FAIXA:
            s = ler(f'{d}/index.html')
            self.assertNotIn('data-cartaz="raiz"', s, d)
            self.assertNotIn('window.CARTAZ_DADOS', s, d)
        self.assertIn('window.CARTAZ_DADOS', ler('cidadania/m1/index.html'))  # Cidadania só no lote 1b, depois de 28/10

    def test_como_se_le_ao_lado_do_passo_9(self):
        s = ler('investigar/index.html')
        # logo a seguir ao cartão do passo 9 (só no índice; o baralho do passo 9 não muda até 25/11)
        self.assertRegex(s, r'href="passo-09/" data-id="passo-09">(?:(?!</a>).)*</a></div><p class="p-lead lead2 ao-lado">Ao lado do passo 9: <a href="' + re.escape(LENTE) + r'ler/passo-06/">Citar com as palavras certas</a>')
        self.assertTrue((R / 'ler/passo-06/index.html').exists())
        self.assertIn('data-passagem', ler('ler/index.html'))

    def test_as_paginas_mexidas_so_ligam_a_paginas_que_existem(self):
        # 24/10/2026: o Ver para fazer gerado de novo (Rotinas) e as entradas que perderam a faixa ou a ligação ao mapa; o v124 ligava a
        # lente/justica/, que não existe (a página publicada já levava a olhar-e-decidir/justica/; acertado em ver-para-fazer.json)
        mexidas = sorted((R / 'ver-para-fazer').rglob('index.html')) + [R / d / 'index.html' for d in SEM_FAIXA + ['narrativas/fora-da-pagina', 'vozes']]
        for p in mexidas:
            rel = p.relative_to(R).as_posix()
            for h in re.findall(r'href="([^"]+)"', re.sub(r'<script[\s\S]*?</script>', ' ', p.read_text('utf-8'))):  # sem as que o JS monta
                self.assertIsNot(existe(h, rel), False, (rel, h))

    def test_oficina_8_rotinas(self):
        s = ler('ver-para-fazer/index.html')
        self.assertRegex(s, r'<span class="r">Oficina 8</span><span class="t">Rotinas</span>')
        self.assertIn('<title>Rotinas · Ver para fazer · Lente</title>', ler('ver-para-fazer/oficina-metodo/index.html'))
        for p in (R / 'ver-para-fazer').rglob('index.html'):
            self.assertNotIn('oficina-metodo/">Método<', p.read_text('utf-8'), p.relative_to(R))

    def test_a_mesa_de_edicao_saiu(self):
        self.assertEqual(sorted(x.name for x in (R / 'curadoria').iterdir()), ['index.html'])
        self.assertIn('data-passagem', ler('curadoria/index.html'))
        self.assertIn('data-passagem', ler('mapa/index.html'))

    def test_nenhuma_pagina_liga_ao_mapa(self):
        # 24/10/2026: o mapa passou a passagem para a entrada; só a lista «Tudo o que há no Lente», nos endereços antigos, o nomeia
        # (saíram «Ver o mapa do LENTE» do Laboratório e das vozes e «Mapa do Lente» do rodapé de Fora da página)
        for d, ds, fs in os.walk(R):
            ds[:] = [x for x in ds if x not in {'.git', 'tests', 'node_modules', '__pycache__'}]
            for f in fs:
                rel = (Path(d) / f).relative_to(R).as_posix()
                if not f.endswith('.html') or rel in ('mapa/index.html', 'docente/tudo/index.html'):
                    continue
                s = ler(rel)
                self.assertNotRegex(texto(s), r'(?i)mapa do lente', rel)
                for h in re.findall(r'href="([^"]+)"', s):
                    if h.startswith(LENTE):
                        alvo = urlsplit(h).path[len('/lente/'):]
                    elif re.match(r'^[a-z]+:|^/|^#', h):
                        continue
                    else:
                        alvo = os.path.normpath(os.path.join(os.path.dirname(rel), urlsplit(h).path)).replace('\\', '/') + '/'
                    self.assertNotEqual(alvo, 'mapa/', (rel, h))


if __name__ == '__main__':
    unittest.main()
