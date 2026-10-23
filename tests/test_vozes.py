from pathlib import Path
import re, unittest
R = Path(__file__).resolve().parents[1]
U = 'https://pedrohfernandes-klk.github.io/lente/'
# A ordem das vozes (a do índice, por grupos): Porta, Pensar, Escrever, Som, Vestir, Pintar, Filmar, Cena, Tempo
# (23/10/2026: mais cinco artistas; depois mais doze vozes com dossier verificado, num total de vinte)
ORDEM = ['arte-e-vida', 'nietzsche', 'absurdo', 'oscar-wilde', 'sa-carneiro', 'foster-wallace', 'beatles', 'antonio-variacoes', 'prince',
         'nirvana-cobain', 'da-weasel', 'kendrick-lamar', 'versace', 'warhol', 'paula-rego', 'basquiat', 'manoel-de-oliveira',
         'joao-cesar-monteiro', 'mario-viegas', '25-de-abril']
NOVAS = {'oscar-wilde': 'oscar-wilde-sarony-1882.webp', 'paula-rego': 'casa-das-historias-2012.webp', 'basquiat': 'basquiat-placa-paris-2021.webp',
         'manoel-de-oliveira': 'manoel-de-oliveira-1991.webp', 'joao-cesar-monteiro': 'joao-cesar-monteiro-1989.webp',
         'sa-carneiro': 'sa-carneiro-orpheu-2-capa-1915.webp', 'foster-wallace': 'foster-wallace-leitura-2006.webp',
         'beatles': 'beatles-chegada-nova-iorque-1964.webp', 'antonio-variacoes': 'antonio-variacoes-painel-fiscal-2019.webp',
         'prince': 'prince-bruxelas-1986.webp', 'nirvana-cobain': 'nirvana-cobain-placa-aberdeen-2014.webp',
         'da-weasel': 'da-weasel-pac-pavilhao-atlantico-2007.webp', 'kendrick-lamar': 'kendrick-lamar-pulitzer-2018.webp',
         'versace': 'versace-medusa-rondanini-2005.webp', 'warhol': 'warhol-polavision-1978.webp',
         'mario-viegas': 'mario-viegas-teatro-estudio-2009.webp', '25-de-abril': '25-de-abril-diario-governo-1974.webp'}
CONJUNTOS = {'vidas-vozes': ['arte-e-vida', 'nietzsche', 'absurdo'], 'vidas-escrever': ['oscar-wilde', 'sa-carneiro', 'foster-wallace'],
             'vidas-som': ['beatles', 'antonio-variacoes', 'prince', 'nirvana-cobain', 'da-weasel', 'kendrick-lamar'],
             'vidas-imagem': ['versace', 'warhol', 'paula-rego', 'basquiat', 'manoel-de-oliveira', 'joao-cesar-monteiro', 'mario-viegas'],
             'vidas-tempo': ['25-de-abril']}
# linhas de apoio no fim: as vozes em que houve suicídio (o facto numa frase, REGRAS-VOZES) e Camus, que pergunta pelo suicídio em
# _O Mito de Sísifo_ (decisão já publicada)
APOIO = ['absurdo', 'sa-carneiro', 'foster-wallace', 'nirvana-cobain']


def pagina(v):
    return (R / 'vozes' / v / 'index.html').read_text('utf-8')


def montar(s):
    i = s.index('EPIJogo.montar(')
    return s[i:s.index('</script>', i)]


class Vozes(unittest.TestCase):
    """Vidas e vozes: oito vozes, uma a seguir à outra, com o nome da secção decidido a 23/10/2026."""

    def test_rotulo_da_seccao(self):
        for p in [R / 'vozes' / v / 'index.html' for v in ORDEM] + [R / 'vozes/index.html', R / 'gigantes/index.html', R / 'narrativas/margens/index.html']:
            s = p.read_text('utf-8')
            self.assertNotIn('Vidas e ideias', s, p)
        for v in ORDEM:
            s = pagina(v)
            self.assertIn(' · Vidas e vozes · Lente</title>', s, v)
            self.assertIn(f'<a href="{U}vozes/">Vidas e vozes</a>', s, v)

    def test_seguinte_pela_ordem(self):
        for k, v in enumerate(ORDEM):
            c = montar(pagina(v))
            self.assertIn(f'chave:"epi-vozes-{v}"', c)
            self.assertIn(f'S.feitas["{v}"]', c)
            seg = f'{U}vozes/{ORDEM[k + 1]}/' if k + 1 < len(ORDEM) else f'{U}vozes/'
            self.assertIn(f'seguinte:"{seg}"', c, v)
            self.assertIn('seguinteRotulo:"Voz seguinte"' if k + 1 < len(ORDEM) else 'seguinteRotulo:"Voltar a Vidas e vozes"', c, v)

    def test_entrada_lista_todas(self):
        s = (R / 'vozes/index.html').read_text('utf-8')
        for v in ORDEM:
            self.assertEqual(s.count(f'href="{U}vozes/{v}/" data-id="vozes-{v}"'), 1, v)
        for cid, vozes in CONJUNTOS.items():
            i = s.index(f'id="{cid}"')
            bloco = s[i:s.index('</details>', i)]
            self.assertEqual(re.findall(r'data-id="vozes-([^"]+)"', bloco), vozes, cid)
        self.assertEqual(sorted(v for vs in CONJUNTOS.values() for v in vs), sorted(ORDEM))
        self.assertIn('>Oito coleções</h2>', s)

    def test_linhas_de_apoio(self):
        for v in ORDEM:
            tem = 'class=\\"vz-apoio\\"' in montar(pagina(v))
            self.assertEqual(tem, v in APOIO, v)

    def test_imagens_existem(self):
        for v, f in NOVAS.items():
            self.assertTrue((R / 'img/narrativas' / f).is_file(), f)
            self.assertIn(f'{U}img/narrativas/{f}', montar(pagina(v)))

    def test_palavras_proibidas_no_texto(self):
        for v in ORDEM:
            texto = re.sub(r'<[^>]+>', ' ', montar(pagina(v)).replace('\\"', '"'))
            for m in [r'\bprofessor', r'\bjog(ar|as?|am|amos|ou|aste|ue|uem|ando|ado)\b', r'\bfichas?\b', r'\bfolhas?\b', '—']:
                self.assertIsNone(re.search(m, texto, re.I), (v, m))


if __name__ == '__main__':
    unittest.main()
