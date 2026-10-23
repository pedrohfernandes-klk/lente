from pathlib import Path
import re, unittest
R = Path(__file__).resolve().parents[1]
U = 'https://pedrohfernandes-klk.github.io/lente/'
# A ordem das vozes (a do índice, por grupos): Porta, Pensar, Escrever, Pintar, Filmar (23/10/2026: mais cinco artistas)
ORDEM = ['arte-e-vida', 'nietzsche', 'absurdo', 'oscar-wilde', 'paula-rego', 'basquiat', 'manoel-de-oliveira', 'joao-cesar-monteiro']
NOVAS = {'oscar-wilde': 'oscar-wilde-sarony-1882.webp', 'paula-rego': 'casa-das-historias-2012.webp', 'basquiat': 'basquiat-placa-paris-2021.webp',
         'manoel-de-oliveira': 'manoel-de-oliveira-1991.webp', 'joao-cesar-monteiro': 'joao-cesar-monteiro-1989.webp'}


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
            self.assertIn(f'href="{U}vozes/{v}/" data-id="vozes-{v}"', s)
        i = s.index('id="vidas-artistas"')
        bloco = s[i:s.index('</details>', i)]
        self.assertEqual(re.findall(r'data-id="vozes-([^"]+)"', bloco), list(NOVAS))
        self.assertIn('>Cinco coleções</h2>', s)

    def test_imagens_existem(self):
        for v, f in NOVAS.items():
            self.assertTrue((R / 'img/narrativas' / f).is_file(), f)
            self.assertIn(f'{U}img/narrativas/{f}', montar(pagina(v)))

    def test_palavras_proibidas_no_texto(self):
        for v in NOVAS:
            texto = re.sub(r'<[^>]+>', ' ', montar(pagina(v)).replace('\\"', '"'))
            for m in [r'\bprofessor', r'\bjog(ar|as?|am|amos|ou|aste|ue|uem|ando|ado)\b', r'\bfichas?\b', r'\bfolhas?\b', '—']:
                self.assertIsNone(re.search(m, texto, re.I), (v, m))


if __name__ == '__main__':
    unittest.main()
