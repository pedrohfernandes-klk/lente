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
            # 08/11/2026: decisão 152 (achado 61 da varredura de 6/11): o tempo de escrita leva espaço sem quebra («12 min»).
            self.assertIn('\u00a0min de escrita</p>', itens[0]['html'], d.name)

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
        # 12/11/2026: pedido entrada-temas. A entrada abre por quatro temas. A antiga porta da Cidadania (três linhas: módulo 1,
        # módulo 2 e Dilemas) reparte-se: os dois módulos ficam na linha «A minha aula», que conserva o id inicio-cidadania, e os
        # Dilemas são o destino do tema 01. A mesma exigência, com os destinos exatos: nenhuma das três ligações se perde.
        i = s.index('id="inicio-cidadania"'); j = s.index('</nav>', i)
        self.assertEqual(re.findall(r'<li><a href="([^"]+)">([^<]+)</a></li>', s[i:j]),
                         [('cidadania/m1/', 'Cidadania, módulo 1'), ('cidadania/m2/', 'Cidadania, módulo 2')])
        self.assertEqual(s[i:j].count('<li><a '), 2)
        # 13/11/2026: pedido temas-01-03-04. O tema 01 abre a sua página (justica-e-vida-em-comum/), onde os Dilemas são a primeira
        # ligação de «Ver tudo neste tema»; continuam também no mapa. Nenhuma das três ligações se perde.
        self.assertEqual(s.count('<h3 class="tm-n"><b aria-hidden="true">01</b><a href="justica-e-vida-em-comum/">'), 1)
        self.assertEqual(re.search(r'<details class="tm-tudo">.*?<li><a href="([^"]+)">([^<]+)</a>', (R / 'justica-e-vida-em-comum/index.html').read_text('utf-8'), re.S).groups(),
                         ('https://pedrohfernandes-klk.github.io/lente/olhar-e-decidir/', 'Dilemas'))
        self.assertEqual((R / 'mapa/index.html').read_text('utf-8').count('href="https://pedrohfernandes-klk.github.io/lente/olhar-e-decidir/"'), 1)
        i = s.index('id="inicio-narrativas"'); j = s.index('</article>', i)
        # 30/10/2026: cartão do Laboratório refeito (pedido do docente); as três portas são as da entrada nova do
        # Laboratório (#78) e apontam para o catálogo, onde as secções vivem desde então (narrativas/#… redireciona para lá).
        # 12/11/2026: pedido entrada-temas. O cartão do Laboratório passa a ser o do tema 03 («Histórias e criação»), com o mesmo id:
        # abre o Laboratório e conserva a ligação ao Ideias (decisão 141). As três portas do catálogo saem do cartão e ficam no mapa,
        # com os mesmos destinos, a mesma ordem e os mesmos rótulos (decisão 54), numa linha fora da secção que tools/laboratorio.py
        # reescreve; as secções continuam a existir no catálogo.
        mapa = (R / 'mapa/index.html').read_text('utf-8')
        self.assertEqual(re.findall(r'href="\.\./narrativas/tudo/#([a-z-]+)">([^<]+)</a>', mapa),
                         [('ler-como-quem-escreve', 'Observar'), ('treinar', 'Treinar'), ('criar', 'Criar')])
        tudo = (R / 'narrativas/tudo/index.html').read_text('utf-8')
        for ancora in ('ler-como-quem-escreve', 'treinar', 'criar'):
            self.assertEqual(tudo.count('id="' + ancora + '"'), 1, ancora)
        self.assertEqual(re.findall(r'<h3 class="tm-n"><b aria-hidden="true">(\d\d)</b><a href="([^"]+)">([^<]+)</a></h3>', s[i:j]),
                         [('03', 'historias-e-criacao/', 'Histórias e criação')])
        # 13/11/2026: pedido temas-01-03-04. O título do cartão abre a página do tema 03 (historias-e-criacao/); o Laboratório, que
        # era o destino, fica à vista no mesmo cartão, numa ligação própria antes da do Ideias, e é a primeira ligação de «Ver tudo
        # neste tema» na página do tema.
        self.assertEqual(re.search(r'<details class="tm-tudo">.*?<li><a href="([^"]+)">([^<]+)</a>', (R / 'historias-e-criacao/index.html').read_text('utf-8'), re.S).groups(),
                         ('https://pedrohfernandes-klk.github.io/lente/narrativas/', 'Laboratório'))
        # 01/11/2026: decisão 54, rótulo Observar; destinos e ordem preservados.
        # 02/11/2026: decisão do docente (141): o «Ideias» é público e tem ligação a partir das páginas públicas
        # 05/11/2026: decisão 163 (e decisão 97). A ordem passa a Ideias, Observar, Treinar e Criar, como no fio do Laboratório.
        # 13/11/2026: a ligação ao Laboratório vem antes; a do Ideias fica igual, uma só vez, imediatamente antes da seta.
        self.assertEqual(re.findall(r'<p class="tm-extra"><a href="([^"]+)">([^<]+)</a></p>', s[i:j]),
                         [('https://pedrohfernandes-klk.github.io/lente/narrativas/', 'Laboratório'), ('narrativas/ideias/', 'Ideias: o método em cinco passos')])
        self.assertEqual(s[i:j].count('narrativas/ideias/'), 1)
        self.assertIn('<p class="tm-extra"><a href="narrativas/ideias/">Ideias: o método em cinco passos</a></p><span class="tm-seta" aria-hidden="true">→</span></div>', s[i:j])
        self.assertIn('href="narrativas/ideias/"',s[i:j])
        # 30/10/2026: decisão 34: a porta mostra o esboço de O Quarto (carta a Theo), com a tabela de museu colada à imagem,
        # e os dados vêm de imagens.json (entrada «porta»).
        porta = next(x for x in json.loads((R / 'assets/laboratorio/imagens.json').read_text('utf-8')) if x['id'] == 'porta')
        self.assertIn('<img src="' + porta['file'] + '" alt="' + porta['alt'] + '" width="' + str(porta['width']) + '" height="' + str(porta['height']) + '"', s[i:j])
        self.assertTrue((R / porta['file']).is_file())
        # 01/11/2026: D1, classe comum dos créditos; mesma imagem e posição da legenda.
        # 02/11/2026: decisão 34, tabela colada à imagem também com a dobra
        # 07/11/2026: decisões 153, 176 e 177, a tabela de museu passa, inteira, para o «i» no canto da imagem, fora da ligação.
        # 12/11/2026: pedido entrada-temas. A imagem deixa de estar dentro de uma ligação; o «i» segue-se à imagem, na mesma moldura,
        # e fica antes (e fora) da ligação do título do cartão.
        self.assertRegex(s[i:j], r'style="object-position:50% 40%"><details class="info-i" name="info-i"><summary aria-label="Créditos da imagem: Vincent van Gogh"><span aria-hidden="true">i</span></summary><p class="info-i-texto">Vincent van Gogh, esboço de <i>O Quarto</i>')
        # 02/11/2026: a dobra continua a seguir-se à tabela, com o nome da porta no summary e a fonte no mesmo cartão.
        # 07/11/2026: decisões 153, 176 e 177, a dobra segue-se à moldura da imagem, que fecha depois do «i».
        # 12/11/2026: pedido entrada-temas. Já não há dobra: à moldura da imagem, que fecha depois do «i», segue-se o corpo do cartão,
        # com o nome do tema no título e a fonte no mesmo cartão.
        self.assertRegex(s[i:j], r'Domínio público\.</p></details></div><div class="tm-corpo"><h3 class="tm-n"><b aria-hidden="true">03</b><a href="[^"]+">Histórias e criação</a></h3>')
        self.assertNotIn('<a', s[i:j][s[i:j].index('<details class="info-i"'):s[i:j].index('<summary')])
        for campo in ('Pena e tinta sobre papel.', porta['institution'] + '.', 'href="' + porta['source'] + '">Wikimedia Commons</a>. Domínio público.'):
            self.assertIn(campo, s[i:j])
        self.assertIn('id="inicio-vozes"', s)
        self.assertIn('id="ferramentas"', s)


if __name__ == '__main__':
    unittest.main()
