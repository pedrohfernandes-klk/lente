from pathlib import Path
import json, re, unittest
from urllib.parse import urlsplit
R = Path(__file__).resolve().parents[1]
G = R / 'narrativas/treinar'
LENTE = 'https://pedrohfernandes-klk.github.io/lente/'
PROIBIDAS = re.compile(r'(?<![\wÀ-ÿ])(?:professor(?:a|es|as)?|jog(?:ar|a|as|amos|am|ou|ue|uei|ando|ado)|fichas?|folhas?)(?![\wÀ-ÿ])', re.I)


def montar(p):
    s = p.read_text('utf-8')
    k = s.index('itens:', s.index('EPIJogo.montar(')) + len('itens:')
    itens, _ = json.JSONDecoder().raw_decode(s, k)
    chave = re.search(r'chave:"([^"]+)"', s[k:]).group(1)
    return s, itens, chave


def treinos():
    return sorted(d for d in G.iterdir() if d.is_dir() and d.name not in ('caderno', 'docente'))


class Ginasio(unittest.TestCase):
    def test_trinta_treinos_com_o_mesmo_molde(self):
        ds = treinos()
        self.assertEqual(len(ds), 30)
        for d in ds:
            s, itens, chave = montar(d / 'index.html')
            self.assertEqual(chave, 'epi-treinos-' + d.name)
            self.assertEqual([x.get('rot', x['t']) for x in itens], ['A regra', 'O modelo', 'escolha', 'Escreve', 'Verifica', 'Revê', 'Troca'], d.name)
            esc = itens[2]
            self.assertEqual(len(esc['o']), 4)
            self.assertTrue(all((j == esc['c']) == (esc['fe'][j] is None) for j in range(4)), d.name)
            # a certa nunca é a mais longa
            self.assertLess(len(esc['o'][esc['c']]), max(len(o) for j, o in enumerate(esc['o']) if j != esc['c']), d.name)
            self.assertIn('data-relogio=', itens[3]['html'])
            # relatório de 23/10: o relógio começa parado, dá mais um minuto, esconde-se e não anuncia cada segundo
            for b in ('data-rl="ir"', 'data-rl="parar"', 'data-rl="mais"', 'data-rl="zero"', 'data-rl="ver"'):
                self.assertIn(b, itens[3]['html'], d.name)
            self.assertNotIn('class="tr-tempo" aria-live', itens[3]['html'])
            # a revisão tem quatro estados por critério (sim, em parte, ainda não, não se aplica), sem bloqueio nem nota;
            # antes eram três caixas de sim/não (mudança deliberada, 23/10/2026)
            v = itens[4]['html']
            self.assertEqual(v.count('<fieldset>'), 3, d.name)
            self.assertEqual(v.count('type="radio"'), 12, d.name)
            self.assertIn('regra para esta tentativa', itens[0]['html'])
            self.assertIn('tr-relogio-js', s)
            self.assertIn('S.vezes[', s)

    def test_sem_atribuicoes_por_confirmar(self):
        # relatório de 23/10: nenhuma regra atribuída a um escritor sem a obra confirmada; nada de efeitos psicológicos sem fonte
        for p in [d / 'index.html' for d in treinos()] + [G / 'docente/index.html']:
            s = p.read_text('utf-8')
            for nome in ('Bradbury', 'Lamott', 'Stephen King', 'McPhee', 'juiz interior'):
                self.assertNotIn(nome, s, (p.relative_to(R), nome))

    def test_regras_da_casa(self):
        for d in treinos():
            _, itens, _ = montar(d / 'index.html')
            for x in itens:
                txt = ' '.join(str(v) for k, v in x.items() if k in ('html', 'p', 'f', 'titulo') or k in ('o', 'fe'))
                # o travessão só pode aparecer nos versos citados (pontuação do autor), dentro do modelo
                fora = re.sub(r'<div class="tr-modelo">.*?</div>', '', txt, flags=re.S)
                self.assertNotIn('—', fora, d.name)
                self.assertIsNone(PROIBIDAS.search(re.sub(r'<[^>]+>', ' ', txt)), (d.name, x.get('rot')))
            esc = itens[2]
            frases = ' '.join([esc['p'], esc['f']] + esc['o'] + [t for t in esc['fe'] if t])
            self.assertNotRegex(frases, r'[^\s"]\s·\s[^\s"]', d.name)  # nunca «·» dentro de uma frase

    def test_ligacoes_locais_existem(self):
        paginas = [d / 'index.html' for d in treinos()] + [G / 'index.html', G / 'caderno/index.html', G / 'docente/index.html', R / 'narrativas/index.html', R / 'vozes/index.html', R / 'index.html', R / 'mapa/index.html']
        for p in paginas:
            s = p.read_text('utf-8')
            for href in set(re.findall(r'href=\\?"(https://pedrohfernandes-klk\.github\.io/lente/[^"\\#?]*)', s)):
                alvo = R / urlsplit(href).path.replace('/lente/', '', 1)
                if not alvo.suffix:
                    alvo = alvo / 'index.html'
                self.assertTrue(alvo.exists(), (p.relative_to(R), href))

    def test_entrada_do_lab_em_tres_portas(self):
        s = (R / 'narrativas/index.html').read_text('utf-8')
        # Academia, Ginásio, Ateliê (decisão de 23/10/2026; antes: Treinar, Criar, Ler como quem escreve); os ids não mudam
        self.assertEqual(re.findall(r'<section class="lab-set" id="([^"]+)"', s), ['ler-como-quem-escreve', 'treinar', 'criar'])
        for nome in ('Academia', 'Ginásio', 'Ateliê'):
            self.assertIn(f'>{nome}<span class="vh">', s)
        i = s.index('id="ler-como-quem-escreve"'); j = s.index('</section>', s.index('id="aulas-narrativa"'))
        self.assertIn('lente/vozes/"><span class="bundle-label">Vidas e vozes</span>', s[i:s.index('id="treinar"')])
        self.assertEqual(len(set(re.findall(r'href="treinar/([a-z-]+)/"', s))), 30)
        for antiga in ('id="aulas"', 'id="experimentar"', 'id="vidas-e-ideias"'):
            self.assertIn(antiga, s)  # quem chega por um endereço antigo ainda cai no sítio certo
        for sai in ('Ler e investigar', 'Ética e estética', 'Preparar e comunicar', 'Aquecer o olhar', 'Explorar e observar'):
            self.assertNotIn(f'<span class="bundle-label">{sai}</span>', s)

    def test_exercicios_e_oficinas_apontam_para_o_ginasio(self):
        n = sum('tr-liga-lab' in (R / 'narrativas' / d / 'index.html').read_text('utf-8') for d in [p.name for p in (R / 'narrativas').iterdir() if p.is_dir()])
        self.assertGreaterEqual(n, 33)

    def test_entrada_do_lente(self):
        s = (R / 'index.html').read_text('utf-8')
        i = s.index('id="inicio-cidadania"'); j = s.index('</article>', i)
        self.assertEqual(s[i:j].count('<li><a '), 3)
        i = s.index('id="inicio-narrativas"'); j = s.index('</article>', i)
        self.assertEqual(re.findall(r'href="narrativas/#([a-z-]+)"', s[i:j]), ['ler-como-quem-escreve', 'treinar', 'criar'])
        self.assertIn('id="inicio-vozes"', s)
        self.assertIn('id="ferramentas"', s)


if __name__ == '__main__':
    unittest.main()
