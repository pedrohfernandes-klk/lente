# 30/10/2026: nomes curtos e listas de percursos substituem as montras.
from pathlib import Path
import json, re, unittest
from urllib.parse import urlsplit
R = Path(__file__).resolve().parents[1]
G = R / 'narrativas/treinar'
LENTE = 'https://pedrohfernandes-klk.github.io/lente/'
PILOTO = ('o-contrario',)
PROIBIDAS = re.compile(r'(?<![\wÀ-ÿ])(?:professor(?:a|es|as)?|jog(?:ar|a|as|amos|am|ou|ue|uei|ando|ado)|fichas?|folhas?)(?![\wÀ-ÿ])', re.I)


def montar(p):
    s = p.read_text('utf-8')
    k = s.index('itens:', s.index('EPIJogo.montar(')) + len('itens:')
    itens, _ = json.JSONDecoder().raw_decode(s, k)
    chave = re.search(r'chave:"([^"]+)"', s[k:]).group(1)
    return s, itens, chave


def treinos():
    # 05/11/2026: decisão 147 (os 15 treinos feitos sobre textos do Português saíram e ficam como redirecionamento):
    # os treinos são os de percursos.json; as pastas retiradas confirmam-se em tests/test_lab_retiradas.py.
    ids = [p['id'] for p in json.loads((R / 'assets/laboratorio/percursos.json').read_text('utf-8'))['pieces'] if p['id'].startswith('treinar/')]
    ds = sorted(G / i.split('/', 1)[1] for i in ids)
    assert ds == sorted(d for d in G.iterdir() if d.is_dir() and d.name not in ('caderno', 'docente') and 'http-equiv="refresh"' not in (d / 'index.html').read_text('utf-8'))
    return ds


class Ginasio(unittest.TestCase):
    def test_trinta_treinos_com_o_mesmo_molde(self):
        ds = treinos()
        # 05/11/2026: decisão 147, ficam 15 dos 30 treinos.
        self.assertEqual(len(ds), 15)
        for d in ds:
            s, itens, chave = montar(d / 'index.html')
            self.assertEqual(chave, 'epi-treinos-' + d.name)
            # piloto Subtexto (relatório do Lab de 23/10/2026, mudança deliberada): «Uma fala, duas intenções» (o-contrario) tem
            # mais dois cartões, as duas leituras defensáveis depois da escolha e a transferência no fim; os outros 14 não mudam (05/11/2026: decisão 147)
            base = ['A regra', 'O modelo', 'escolha', 'Escreve', 'Verifica', 'Revê', 'Troca']
            esperado = ['A regra', 'O modelo', 'escolha', 'Duas leituras', 'Escreve', 'Verifica', 'Revê', 'Troca', 'Transfere'] if d.name in PILOTO else base
            self.assertEqual([x.get('rot', x['t']) for x in itens], esperado, d.name)
            por = {x.get('rot', x['t']): x for x in itens}
            esc = itens[2]
            self.assertEqual(len(esc['o']), 4)
            self.assertTrue(all((j == esc['c']) == (esc['fe'][j] is None) for j in range(4)), d.name)
            # a certa nunca é a mais longa
            self.assertLess(len(esc['o'][esc['c']]), max(len(o) for j, o in enumerate(esc['o']) if j != esc['c']), d.name)
            self.assertIn('data-relogio=', por['Escreve']['html'])
            # relatório de 23/10: o relógio começa parado, dá mais um minuto, esconde-se e não anuncia cada segundo
            for b in ('data-rl="ir"', 'data-rl="parar"', 'data-rl="mais"', 'data-rl="zero"', 'data-rl="ver"'):
                self.assertIn(b, por['Escreve']['html'], d.name)
            self.assertNotIn('class="tr-tempo" aria-live', por['Escreve']['html'])
            # a revisão tem quatro estados por critério (sim, em parte, ainda não, não se aplica), sem bloqueio nem nota;
            # antes eram três caixas de sim/não (mudança deliberada, 23/10/2026)
            v = por['Verifica']['html']
            self.assertEqual(v.count('<fieldset>'), 3, d.name)
            self.assertEqual(v.count('type="radio"'), 12, d.name)
            self.assertIn('regra para esta tentativa', itens[0]['html'])
            self.assertIn('tr-relogio-js', s)
            self.assertIn('S.vezes[', s)

    def test_piloto_subtexto(self):
        # relatório do Lab de 23/10/2026: a mesma competência nas três portas (Academia, Ginásio, Ateliê); ids e chaves não mudam
        s, itens, chave = montar(G / 'o-contrario/index.html')
        self.assertEqual(chave, 'epi-treinos-o-contrario')
        self.assertIn('titulo:"Uma fala, duas intenções"', s)
        por = {x.get('rot', x['t']): x for x in itens}
        self.assertEqual(por['Duas leituras']['html'].count('<p class="tr-pista">'), 2)
        self.assertIn('class="tr-leit"', por['Duas leituras']['html'])
        self.assertIn('.tr-leit{', s)
        self.assertIn(LENTE + 'narrativas/proposta-subtexto/', por['Transfere']['html'])
        # 05/11/2026: decisão 147. «Duas vozes, nenhum nome» (sem-disse) saiu com os treinos do Português; o estilo das
        # leituras continua só no treino que as tem, e a proposta liga ao subtexto e ao treino piloto.
        for d in treinos():
            if d.name not in PILOTO:
                self.assertNotIn('.tr-leit{', (d / 'index.html').read_text('utf-8'), d.name)
        prop = (R / 'narrativas/proposta-subtexto/index.html').read_text('utf-8')
        # 05/11/2026: decisão 147 (Laboratório sem o Português): «O subtexto» (exercício sobre Frei Luís de Sousa e a Farsa) saiu; a proposta parte do treino piloto.
        for h in ('narrativas/treinar/o-contrario/',):
            self.assertIn(LENTE + h, prop)
        self.assertNotIn(LENTE + 'narrativas/subtexto/', prop)
        self.assertNotIn(LENTE + 'narrativas/treinar/sem-disse/', prop)
        # 05/11/2026: decisão 154 (os exercícios fazem-se sozinho): o segundo passo é «A leitura de fora» (outra pessoa, ou tu
        # noutro dia); os cinco passos continuam todos exigidos.
        for passo in ('Versão A', 'A leitura de fora', 'Duas leituras defensáveis', 'Versão B', 'A razão da mudança'):
            self.assertIn(passo, prop)
        # 30/10/2026: Laboratório simples (pedido do docente). A proposta continua no catálogo.
        lab = (R / 'narrativas/tudo/index.html').read_text('utf-8')
        # 30/10/2026: a proposta de subtexto é uma cena para escrever; passa para Criar, no percurso da ficção (revisão do editor).
        i = lab.index('id="criar"')
        self.assertIn('href="../proposta-subtexto/"', lab[i:lab.index('</section>', i)])
        for p in list((R / 'narrativas').rglob('index.html')) + [R / 'mapa/index.html']:
            t = p.read_text('utf-8')
            self.assertNotIn('Sem «disse»', t, p)
            self.assertNotIn('Dizer o contrário', t, p)

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

    def test_fase0_sem_etiquetas_nem_pontos(self):
        # Fase 0 (23/10/2026): o motor escapa o «titulo» e passa «p», «o», «f» e «fe» por it() (só _itálico_ e **negrito**),
        # por isso uma etiqueta HTML nestes campos fica à vista; e nenhum treino dá pontos (decisão 8 do docente)
        for d in treinos():
            s, itens, _ = montar(d / 'index.html')
            for x in itens:
                for k in ('titulo', 'p', 'o', 'f', 'fe'):
                    v = x.get(k)
                    for y in (v if isinstance(v, list) else [v]):
                        self.assertFalse(isinstance(y, str) and '<' in y, (d.name, x.get('rot', x['t']), k, y))
            self.assertIn('semPontos:true', s, d.name)
            self.assertIn('var soLer=!nFazer()||cfg.semPontos;', s, d.name)
            self.assertIn('pontos:ganho&&!cfg.semPontos?', s, d.name)
            self.assertIn(' min de escrita</p>', itens[0]['html'], d.name)

    def test_ligacoes_locais_existem(self):
        paginas = [d / 'index.html' for d in treinos()] + [G / 'index.html', G / 'caderno/index.html', G / 'docente/index.html', R / 'narrativas/index.html', R / 'vozes/index.html', R / 'index.html', R / 'mapa/index.html', R / 'narrativas/proposta-subtexto/index.html']
        for p in paginas:
            s = p.read_text('utf-8')
            for href in set(re.findall(r'href=\\?"(https://pedrohfernandes-klk\.github\.io/lente/[^"\\#?]*)', s)):
                alvo = R / urlsplit(href).path.replace('/lente/', '', 1)
                if not alvo.suffix:
                    alvo = alvo / 'index.html'
                self.assertTrue(alvo.exists(), (p.relative_to(R), href))

    def test_entrada_do_lab_em_tres_portas(self):
        # 30/10/2026: Laboratório simples (pedido do docente). Três portas curtas; os conjuntos passam para tudo/.
        entrada = (R / 'narrativas/index.html').read_text('utf-8')
        # 01/11/2026: decisão 54, Observar; as três portas e os destinos mantêm-se.
        for nome in ('<h2>Observar</h2>', '<h2>Treinar</h2>', '<h2>Criar</h2>'):
            self.assertIn(nome, entrada)
        s = (R / 'narrativas/tudo/index.html').read_text('utf-8')
        self.assertEqual(re.findall(r'<section id="([^"]+)"', s), ['ler-como-quem-escreve', 'treinar', 'criar'])
        # 05/11/2026: decisão 147, 15 treinos no catálogo.
        self.assertEqual(len(set(re.findall(r'href="../treinar/([a-z-]+)/"', s)) - {'caderno','docente'}), 15)
        for antiga in ('id="aulas"', 'id="experimentar"', 'id="vidas-e-ideias"'):
            self.assertIn(antiga, s)
        # 30/10/2026: a entrada já não guarda âncoras escondidas; uma âncora que lá não existe leva a tudo/.
        self.assertIn('location.replace("tudo/"', entrada)
        self.assertIn("addEventListener('hashchange',encaminhar)", (R / 'assets/formas/entrada.js').read_text('utf-8'))

    def test_exercicios_e_oficinas_apontam_para_o_ginasio(self):
        n = sum('tr-liga-lab' in (R / 'narrativas' / d / 'index.html').read_text('utf-8') for d in [p.name for p in (R / 'narrativas').iterdir() if p.is_dir()])
        # 05/11/2026: decisão 147 (Laboratório sem o Português): os exercícios de Observar que ligavam ao ginásio saíram com os textos do programa; ficam as 15 oficinas
        # com «Antes desta oficina, em Treinar» (duas perderam os treinos todos, que eram do Português).
        self.assertGreaterEqual(n, 15)

    def test_entrada_do_lente(self):
        s = (R / 'index.html').read_text('utf-8')
        i = s.index('id="inicio-cidadania"'); j = s.index('</article>', i)
        self.assertEqual(s[i:j].count('<li><a '), 3)
        i = s.index('id="inicio-narrativas"'); j = s.index('</article>', i)
        # 30/10/2026: cartão do Laboratório refeito (pedido do docente); as três portas são as da entrada nova do
        # Laboratório (#78) e apontam para o catálogo, onde as secções vivem desde então (narrativas/#… redireciona para lá).
        self.assertEqual(re.findall(r'href="narrativas/tudo/#([a-z-]+)"', s[i:j]), ['ler-como-quem-escreve', 'treinar', 'criar'])
        # 01/11/2026: decisão 54, rótulo Observar; destinos e ordem preservados.
        # 02/11/2026: decisão do docente (141): o «Ideias» é público e tem ligação a partir das páginas públicas
        self.assertEqual(re.findall(r'<strong>([^<]+)</strong>', s[i:j]), ['Observar', 'Treinar', 'Criar', 'Ideias'])
        self.assertIn('href="narrativas/ideias/"',s[i:j])
        # 30/10/2026: decisão 34: a porta mostra o esboço de O Quarto (carta a Theo), com a tabela de museu colada à imagem,
        # e os dados vêm de imagens.json (entrada «porta»).
        porta = next(x for x in json.loads((R / 'assets/laboratorio/imagens.json').read_text('utf-8')) if x['id'] == 'porta')
        self.assertIn('<img src="' + porta['file'] + '"', s[i:j])
        self.assertTrue((R / porta['file']).is_file())
        # 01/11/2026: D1, classe comum dos créditos; mesma imagem e posição da legenda.
        # 02/11/2026: decisão 34, tabela colada à imagem também com a dobra
        self.assertRegex(s[i:j], r'</a><p class="m1-home-credit ld-credito cz-credit">Vincent van Gogh, esboço de <i>O Quarto</i>')
        # 02/11/2026: a dobra continua a seguir-se à tabela, com o nome da porta no summary e a fonte no mesmo cartão.
        self.assertRegex(s[i:j], r'Domínio público\.</p><details class="cz-fold" open><summary data-cz-next><h2 class="ld-n">Laboratório\.</h2></summary><div class="ld-corpo">')
        for campo in ('Pena e tinta sobre papel.', porta['institution'] + '.', 'href="' + porta['source'] + '">Wikimedia Commons</a>. Domínio público.'):
            self.assertIn(campo, s[i:j])
        self.assertIn('id="inicio-vozes"', s)
        self.assertIn('id="ferramentas"', s)


if __name__ == '__main__':
    unittest.main()
