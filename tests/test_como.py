from pathlib import Path
import os, re, unittest
# Na pasta tests do Lente, a raiz é a pasta de cima; LENTE_RAIZ aponta para outra cópia.
R = Path(os.environ.get('LENTE_RAIZ') or Path(__file__).resolve().parents[1])
PT_COMO = 'https://pedrohfernandes-klk.github.io/pt/como/'
PULAR = {'.git', 'tests', 'node_modules', '__pycache__'}
# a escolha do vídeo pelo tipo do cartão (chaveComo no motor dos baralhos; os tipos de Cidadania trazem o seu «como» em EPITipos)
COMO_DO_TIPO = {'escolha': ['escolher'], 'vf': ['verdadeiro-falso'], 'completar': ['completar'], 'sublinhar': ['tocar-palavras'],
                'ordenar': ['ordenar'], 'versos': ['ordenar'], 'frase': ['frase'], 'pistas': ['quem-sou-eu'],
                'calcada': ['calcada-contar', 'calcada-ritmo'], 'emparelhar': ['ligar-pares', 'ligar-lados']}


def paginas():
    for d, ds, fs in os.walk(R):
        ds[:] = [x for x in ds if x not in PULAR]
        for f in fs:
            if f.endswith(('.html', '.js')):
                yield Path(d) / f


class ComoSeFaz(unittest.TestCase):
    """Os vídeos de ajuda numa só cópia, a do Português (23/10/2026, plano de reestruturação do Lente, lote 1): a página como/ do Lente
    mostra só os cartões que o Lente usa, chama-se só «Como se faz» e nenhuma página do Lente carrega um vídeo de uma cópia local."""

    @classmethod
    def setUpClass(cls):
        cls.como = (R / 'como/index.html').read_text('utf-8')
        cls.figuras = re.findall(r'<figure id="([a-z-]+)">', cls.como)

    def test_sem_copia_local_dos_videos(self):
        self.assertEqual(sorted(p.name for p in (R / 'como').iterdir()), ['index.html'])
        for v in re.findall(r'(?:src|poster)="([^"]+\.(?:mp4|webm|jpg))"', self.como):
            self.assertTrue(v.startswith(PT_COMO), v)
        local = re.compile(r'(?:lente/|\.\./|["\'(])como/[a-z-]+\.(?:mp4|webm|jpg)')
        for p in paginas():
            self.assertIsNone(local.search(p.read_text('utf-8', errors='replace')), p.relative_to(R))

    def test_os_baralhos_abrem_o_video_no_portugues(self):
        n = 0
        for p in paginas():
            s = p.read_text('utf-8', errors='replace')
            if 'COMO+ch' in s:
                n += 1
                self.assertIn(f'var COMO="{PT_COMO}"', s, p.relative_to(R))
        self.assertGreater(n, 200)

    def test_so_os_cartoes_que_o_lente_usa(self):
        tipos, ext = set(), {}
        for p in paginas():
            s = p.read_text('utf-8', errors='replace')
            tipos |= set(re.findall(r'[{,]"?t"?: ?"([a-z-]+)"', s))
            ext.update(re.findall(r'EPITipos\.([a-z]+)=\{rot:"[^"]*",como:"([a-z-]+)"', s))
        precisa = {'andar-na-licao'}  # o «?» do cartão de leitura e de todos os tipos sem vídeo próprio
        for t in tipos:
            precisa |= set([ext[t]] if t in ext else COMO_DO_TIPO.get(t, []))
        # os ombros de gigante: os 21 gigantes ligam ao vídeo pela âncora, enquanto estiverem publicados (lote 4a)
        if any('como/#subir-aos-ombros' in p.read_text('utf-8', errors='replace') for p in (R / 'gigantes').rglob('index.html')):
            precisa.add('subir-aos-ombros')
        # um par de «ligar» só aparece quando há cartões de emparelhar: aceita-se o vídeo dos dois modos
        self.assertEqual(sorted(set(self.figuras)), sorted(precisa))
        self.assertEqual(len(self.figuras), len(set(self.figuras)))

    def test_um_so_nome(self):
        self.assertIn('<title>Como se faz · Lente</title>', self.como)
        self.assertEqual(re.findall(r'<h1[^>]*>(.*?)</h1>', self.como), ['Como se faz'])
        for sai in ('Como se usa o Lente', 'Os vídeos'):
            self.assertNotIn(f'>{sai}<', self.como)
        texto = re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[\s\S]*?</\1>', '', self.como))
        self.assertNotRegex(texto, r'(?i)\bfichas?\b|\bfolhas?\b|professor|\bjog(ar|a|as|o)\b|—')


if __name__ == '__main__':
    unittest.main()
