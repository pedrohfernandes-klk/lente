"""15/11/2026: revisão geral do Lente, achados confirmados n.º 1, 2, 3, 14, 15, 16, 17, 18 e 24, com as decisões do docente de
15/11/2026 («decide tu mesmo isso tudo já»). Confere a camada (tools/trocas/revisao-geral-lente-20261115.json, tests/
revisao_geral_lente_20261115.py) e o que ela muda:

- a camada é fechada e reversível: leva o main e4fd171 ao ficheiro de hoje, letra a letra, com contagem exata, e conserva o fim de
  linha de cada ficheiro (curadoria/ligacoes-atividades-existentes.json tem CRLF); a cadeia das camadas
  (tests/creditos_i_lente3.py) aplica-a por fora de todas e desfaz-a primeiro, e tools/creditos_i.py --verificar desfaz-a antes de
  conferir a camada da lente-3;
- decisão (a): o retrato de Stanislávski sai da oficina do ator, com o crédito e a legenda; o texto fica;
- decisão (b): sai o vídeo não oficial da v108 (o embed e a ligação para a republicação); a página continua a abrir com o texto que
  sobra, mas sai da Oficina 12, das contagens de Ver para fazer e dos catálogos da curadoria;
- decisão (e): «O teste do colega» passa a «A leitura a frio» (o mesmo endereço, id, chave e progresso), o último cartão dos 15
  treinos passa a «A frio», e não sobra «colega», «a pares» nem «em grupo» nos sítios visados (treinos, percurso «Rever», caderno,
  guia do docente dos treinos, fora-da-pagina com as subpáginas, variantes, as oficinas do achado 2, Ver para fazer e a curadoria);
- decisão (f): sem «jogo», «folha» nem «a pares» nos textos visados (v48, v44, catálogos);
- os textos novos cumprem as regras da casa (sem «—», sem «professor», «jogo», «ficha» ou «folha», sem «·» dentro de frases).

A troca e3 n.º 23 (oficina-readymade-imprimir, «(ou o que ouviste)») ficou de fora: o campo pedia uma coisa que os passos já não
pedem. Por isso «(ou o que o colega disse)» continua nessa folha de imprimir até haver uma troca certa; está nas EXCECOES abaixo, com
«(colegas, família)» da variante de voz da oficina do readymade, que fica fora deste pedido."""
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'tests'))
sys.path.insert(0, str(R / 'tools'))
import creditos_i  # noqa: E402
import creditos_i_lente3  # noqa: E402
import revisao_geral_lente_20261115 as camada  # noqa: E402

BASE = 'e4fd171edc04d52e293b49035f47c66208f09a16'
MANIFESTO = 'tools/trocas/revisao-geral-lente-20261115.json'
LENTE = 'https://pedrohfernandes-klk.github.io/lente/'
PROIBIDAS = re.compile(r'(?<![\wÀ-ÿ])(?:professor(?:a|es|as)?|jog(?:o|os|ar|a|as|amos|am|ou|ue|uei|ando|ado)|fichas?|folhas?)(?![\wÀ-ÿ])', re.I)
# o endereço, o id e a chave da peça (teste-do-colega) ficam, por isso o hífen também conta como parte da palavra
PARES = re.compile(r'(?<![\wÀ-ÿ-])(?:colegas?|a pares|em grupo|conversem)(?![\wÀ-ÿ-])', re.I)
TREINOS = ('a-entrevista', 'a-gaveta', 'comeca-mais-tarde', 'cortar-um-quinto', 'dicionario', 'frase-querida', 'interromper',
           'lista-substantivos', 'o-contrario', 'rascunho-mau', 'sem-mente', 'so-gestos', 'teste-do-colega', 'tres-em-cinco', 'voz-alta')
OFICINAS = ('arco', 'epico', 'visivel', 'ator', 'dilema', 'plano', 'restricao', 'readymade')
# O que ainda pode dizer «colega» nos sítios visados (15/11/2026), com a razão; nada mais.
EXCECOES = {
    'narrativas/oficina-readymade-imprimir/index.html': ['(ou o que o colega disse)'],  # troca e3 n.º 23 de fora (ver acima)
    'narrativas/oficina-readymade/index.html': ['(colegas, família)'],  # a variante de voz da oficina, fora deste pedido
}


def ler(f):
    return (R / f).read_text('utf-8')


def base(f):
    return subprocess.check_output(['git', 'show', f'{BASE}:{f}'], cwd=R)


def cartoes(f):
    s = ler(f)
    k = s.index('itens:', s.index('EPIJogo.montar(')) + len('itens:')
    return json.JSONDecoder().raw_decode(s, k)[0]


def visados():
    fs = [f'narrativas/treinar/{d}/index.html' for d in TREINOS + ('caderno', 'docente')]
    fs += ['narrativas/treinar/index.html', 'narrativas/percursos/rever/index.html', 'narrativas/variantes/index.html',
           'narrativas/fora-da-pagina/index.html', 'praticar/index.html', 'ver-para-fazer/catalogo.json', 'ver-para-fazer/v44/index.html']
    for sub in ('escultura', 'intervalo', 'tese'):
        fs += [f'narrativas/fora-da-pagina/{sub}/index.html', f'narrativas/fora-da-pagina/{sub}/lesson.js']
    for o in OFICINAS:
        fs += [f'narrativas/oficina-{o}/index.html', f'narrativas/oficina-{o}-imprimir/index.html']
    return fs


def itens_curadoria():
    return {x['id']: x for x in json.loads(ler('curadoria/catalogo-123.json'))['items']}


class RevisaoGeralLente(unittest.TestCase):
    def test_camada_fechada_em_vigor_e_reversivel(self):
        r = subprocess.run([sys.executable, str(R / 'tools/creditos_i.py'), '--verificar', '--manifesto', str(R / MANIFESTO)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(len(camada.TROCAS), 65)
        self.assertEqual(sum(len(t) for t in camada.TROCAS.values()), 173)
        for f, trocas in camada.TROCAS.items():
            with self.subTest(ficheiro=f):
                antes_b, agora_b = base(f), (R / f).read_bytes()
                partida, agora = antes_b.decode('utf-8').replace('\r\n', '\n'), ler(f)
                for antigo, novo, n in trocas:
                    self.assertGreaterEqual(n, 1)
                    self.assertEqual(agora.count(novo), n, novo[:80])
                    self.assertEqual(partida.count(antigo), n, antigo[:80])
                    self.assertNotIn(antigo, agora, antigo[:80])
                # letra a letra: o ficheiro de hoje é o do main com as trocas do manifesto, e mais nada
                self.assertEqual(camada.desfazer(agora, f), partida)
                self.assertEqual(camada.aplicar(partida, f), agora)
                self.assertEqual(camada.alinhar(agora, f), agora)
                self.assertEqual(camada.alinhar(partida, f), agora)
                # e o fim de linha de cada ficheiro fica como estava: onde havia CRLF continua a haver, sem nenhum LF solto a mais
                # (as trocas escrevem-se com LF, como os testes leem os ficheiros, e aplicam-se sem mudar o fim de linha)
                self.assertEqual(b'\r\n' in antes_b, b'\r\n' in agora_b)
                if b'\r\n' in antes_b:
                    self.assertEqual(antes_b.count(b'\n') - antes_b.count(b'\r\n'), agora_b.count(b'\n') - agora_b.count(b'\r\n'))
                if f.endswith('.json'):
                    json.loads(agora)

    def test_cadeia_das_camadas_e_verificador(self):
        cadeia = ler('tests/creditos_i_lente3.py')
        self.assertIn('return revisao_geral_lente_20261115.aplicar(temas_paginas_20261113.aplicar(', cadeia)
        self.assertIn('temas_paginas_20261113.desfazer(revisao_geral_lente_20261115.desfazer(texto, ficheiro), ficheiro)', cadeia)
        self.assertIn('return revisao_geral_lente_20261115.alinhar_por_cima(texto, ficheiro, _alinhar_abaixo)', cadeia)
        # a camada tira um «novo» da lente-3 (o retrato com o «i»): a cadeia alinha-se por cima, sem falhar, e volta ao main fec58ae
        f = 'narrativas/oficina-ator/index.html'
        agora = ler(f)
        self.assertEqual(creditos_i_lente3.alinhar(agora, f), agora)
        self.assertEqual(creditos_i_lente3.aplicar(creditos_i_lente3.desfazer(agora, f), f), agora)
        self.assertEqual(creditos_i_lente3.alinhar(creditos_i_lente3.desfazer(agora, f), f), agora)
        self.assertIn(R / MANIFESTO, creditos_i.POR_CIMA)
        for args in ([], ['--manifesto', 'tools/trocas/creditos-i-lente4-20261108.json']):
            r = subprocess.run([sys.executable, str(R / 'tools/creditos_i.py'), '--verificar'] + args, cwd=R, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        # uma camada de cima que não esteja inteira faz falhar a verificação de baixo
        lente3 = creditos_i.ler_manifesto()
        so_ator = {f: lente3[f]}
        acima = [creditos_i.literais(creditos_i.ler_manifesto(R / MANIFESTO))]
        self.assertEqual(creditos_i.verificar(so_ator, por_cima=acima), [])
        self.assertTrue(creditos_i.verificar(so_ator))
        estragado = [{f: [(a, b, n + 1) for a, b, n in acima[0][f]]}]
        self.assertTrue(creditos_i.verificar(so_ator, por_cima=estragado))

    def test_retrato_de_stanislavski_saiu(self):
        # decisão (a): sai o retrato, com o crédito («i») e a legenda; o texto da oficina fica
        s = ler('narrativas/oficina-ator/index.html')
        for fora in ('stanislavski.webp', 'Konstantin_Stanislavskiy_1912', '<figure class=\\"fig-rev retrato\\">', 'Créditos da fotografia',
                     '<span class=\\"fr-leg\\">', 'Fotografia antiga', 'o ator trabalha com o que a personagem quer'):
            self.assertNotIn(fora, s)
        abre = cartoes('narrativas/oficina-ator/index.html')[0]
        self.assertEqual(abre['rot'], 'Abre')
        self.assertTrue(abre['html'].startswith('<p class="etq-m">Oficina · 60 min de exploração · 10 min de preparação</p><p>O corpo do ator produz sentido'))
        self.assertIn('Stanislavski procurou um método para que isso não dependesse da inspiração do dia.', abre['html'])
        self.assertNotIn('<figure', abre['html'])
        self.assertIn('stanislavski.webp', base('narrativas/oficina-ator/index.html').decode('utf-8'))
        # a imagem continua no sítio (a Cidadania usa-a; fica fora deste pedido)
        self.assertTrue((R / 'img/cidadania/stanislavski.webp').is_file())

    def test_video_nao_oficial_saiu_das_listagens_e_dos_catalogos(self):
        # decisão (b): nenhum ficheiro do sítio traz o vídeo da republicação (só os manifestos e os testes o citam)
        for p in R.rglob('*'):
            if not p.is_file() or {'.git', 'node_modules', '__pycache__'} & set(p.parts) or p.suffix not in ('.html', '.js', '.json', '.css', '.md', '.py', '.csv'):
                continue
            rel = p.relative_to(R).as_posix()
            if rel.startswith(('tests/', 'tools/trocas/')):
                continue
            self.assertNotIn('1VM2eLhvsSM', p.read_text('utf-8', errors='replace'), rel)
        v = ler('ver-para-fazer/v108/index.html')
        for fora in ('<div class="vpf-video"', 'data-yt=', 'youtube.com/watch', 'Ver mesmo assim', 'abri-lo no YouTube', 'Liga as legendas no leitor'):
            self.assertNotIn(fora, v)
        # a página continua a abrir, com o texto que sobra, e o script já não encontra o botão (if(v))
        for fica in ("<h1>Hilltop: «I'd like to buy the world a Coke» (Coca-Cola, 1971)</h1>", '<p class="p-sub">Project ReBrief · 1 min</p>',
                     '<h2 id="f-v108">Fazer a seguir</h2>', 'e não pela Coca-Cola', 'var v=document.querySelector(".vpf-video button");if(v)'):
            self.assertEqual(v.count(fica), 1, fica)
        # nenhuma página liga à v108
        for p in list(R.rglob('*.html')) + list(R.rglob('*.json')) + list(R.rglob('*.js')):
            rel = p.relative_to(R).as_posix()
            if '.git' in p.parts or rel.startswith(('tests/', 'tools/trocas/', 'docs/')) or rel == 'ver-para-fazer/v108/index.html':
                continue
            s = p.read_text('utf-8', errors='replace')
            self.assertNotIn('ver-para-fazer/v108/', s, rel)
            self.assertNotRegex(s, r'href="(\.\./)?v108/', rel)
        # as contagens acompanham as listagens: 6 na Oficina 12, 112 na entrada (a soma das doze oficinas)
        desejo = ler('ver-para-fazer/oficina-desejo/index.html')
        self.assertEqual(re.findall(r'<li data-id="(v\d+)"', desejo), ['v105', 'v106', 'v107', 'v109', 'v110', 'v112'])
        self.assertEqual(desejo.count('<p class="p-sub">6 vídeos e um trabalho final</p>'), 1)
        entrada = ler('ver-para-fazer/index.html')
        total = 0
        for href, sub in re.findall(r'<a class="missao[^"]*"[^>]*href="(oficina-[a-z]+/)"[^>]*><span class="r">[^<]*</span><span class="t">[^<]*</span><span class="s">([^<]*)</span>', entrada):
            n = len(re.findall(r'<li data-id="v\d+"', ler('ver-para-fazer/' + href + 'index.html')))
            self.assertTrue(sub.endswith(f' {n} vídeos.'), (href, sub, n))
            total += n
        self.assertEqual(total, 112)
        self.assertEqual(entrada.count('<p class="rodape">Seleção editorial da escola, 112 vídeos.'), 1)
        # os catálogos da curadoria
        cat = json.loads(ler('curadoria/catalogo-123.json'))
        self.assertNotIn('vid-108', [x['id'] for x in cat['items']])
        self.assertEqual(cat['title'], f'Videoteca: {len(cat["items"])} registos acumulados')
        self.assertEqual(len(cat['items']), 128)
        lig = json.loads(ler('curadoria/ligacoes-atividades-existentes.json'))
        self.assertNotIn('vid-108', json.dumps(lig))
        feed = [x for x in lig['connections'] if x['url'] == LENTE + 'cidadania/m2/cid-m2-preco-minuto/']
        self.assertEqual([x['resource_ids'] for x in feed], [['vid-110']])

    def test_a_leitura_a_frio(self):
        # decisão (e): a peça muda de título e de passos; o endereço, o id, a chave e o progresso ficam
        P = {p['id']: p for p in json.loads(ler('assets/laboratorio/percursos.json'))['pieces']}
        p = P['treinar/teste-do-colega']
        self.assertEqual((p['url'], p['title'], p['description'], p['route'], p['progress']),
                         ('narrativas/treinar/teste-do-colega/', 'A leitura a frio', 'Relê o teu texto noutro dia, como quem o lê pela primeira vez.',
                          'rever', {'kind': 'feitas', 'key': 'epi-treinos', 'id': 'teste-do-colega'}))
        rever = next(r for r in json.loads(ler('assets/laboratorio/percursos.json'))['routes'] if r['id'] == 'rever')
        self.assertEqual(rever['reason'], 'Do primeiro rascunho a um começo mais tarde, à escuta, ao corte e à leitura a frio.')
        self.assertEqual(rever['pieces'][-1], 'treinar/teste-do-colega')
        f = 'narrativas/treinar/teste-do-colega/index.html'
        s = ler(f)
        for fica in ('<title>A leitura a frio | Treinar', '<h1 class="c-sr">A leitura a frio</h1>', '<p class="t" id="m-t">A leitura a frio</p>',
                     'titulo:"A leitura a frio"', 'chave:"epi-treinos-teste-do-colega"', 'S.feitas["teste-do-colega"]'):
            self.assertEqual(s.count(fica), 1, fica)
        regra = ('Deixa o teu texto descansar pelo menos um dia. Depois, lê-o de seguida, como se fosse de outra pessoa, e marca com um '
                 'traço onde te perdes e com um círculo a frase que te fica.')
        self.assertEqual(s.count(regra), 2)  # no cartão «A regra» e no «Treinaste»
        itens = cartoes(f)
        self.assertEqual(itens[0]['titulo'], 'A leitura a frio')
        esc = itens[2]
        self.assertEqual(esc['p'], 'Na leitura a frio, puseste um traço na linha onde a Rita aparece pela primeira vez. O que fazes?')
        self.assertEqual(esc['o'][esc['c']], 'Ponho antes uma pista sobre quem é a Rita.')
        self.assertIn('<legend>Li de seguida, sem parar para corrigir.</legend>', itens[4]['html'])
        self.assertIn('<legend>No meu texto, sei porque é que me perdi.</legend>', itens[4]['html'])
        self.assertIsNone(PARES.search(s))
        self.assertNotIn('O leitor não tem a tua cabeça', s)
        # o título novo em todas as páginas que o mostram, sempre com o mesmo endereço; o antigo já não aparece no sítio
        for g, ligacao in (('mapa/index.html', LENTE + 'narrativas/treinar/teste-do-colega/">A leitura a frio</a>'),
                           ('narrativas/tudo/index.html', '<a href="../treinar/teste-do-colega/">A leitura a frio</a>'),
                           ('praticar/index.html', '<a href="../narrativas/treinar/teste-do-colega/">A leitura a frio</a>'),
                           ('narrativas/treinar/index.html', '<a class="linha" href="teste-do-colega/">'),
                           ('narrativas/percursos/rever/index.html', '<a class="linha" href="../../treinar/teste-do-colega/">'),
                           ('narrativas/treinar/cortar-um-quinto/index.html', '<span>Seguinte<small>A leitura a frio</small>'),
                           ('narrativas/treinar/caderno/index.html', '<b>A leitura a frio</b><br>Relê o teu texto noutro dia, como quem o lê pela primeira vez</td>')):
            self.assertEqual(ler(g).count(ligacao), 1, (g, ligacao))
        for linha in ('narrativas/treinar/index.html', 'narrativas/percursos/rever/index.html'):
            self.assertIn('<strong>A leitura a frio</strong><span class="apoio">Relê o teu texto noutro dia, como quem o lê pela primeira vez.</span>', ler(linha))
        self.assertIn('<p class="razao">Do primeiro rascunho a um começo mais tarde, à escuta, ao corte e à leitura a frio.</p>', ler('narrativas/percursos/rever/index.html'))
        com_dados = 0
        for g in R.rglob('*.html'):
            rel = g.relative_to(R).as_posix()
            if '.git' in g.parts or rel.startswith(('docs/', 'tests/', 'tools/')):
                continue
            t = g.read_text('utf-8', errors='replace')
            self.assertNotIn('O teste do colega', t, rel)
            self.assertNotIn('Dá o teu texto a ler sem explicar nada', t, rel)
            m = re.search(r'<script type="application/json" id="lab-dados">(.*?)</script>', t, re.S)
            if m:
                d = {x['id']: x for x in json.loads(m.group(1))}
                if 'treinar/teste-do-colega' in d:
                    com_dados += 1
                    self.assertEqual(d['treinar/teste-do-colega']['title'], 'A leitura a frio', rel)
        self.assertEqual(com_dados, 16)

    def test_ultimo_cartao_dos_treinos_a_frio(self):
        # decisão (e): a troca de textos com um colega passa a uma segunda leitura do próprio texto noutro dia
        for d in TREINOS:
            with self.subTest(treino=d):
                itens = cartoes(f'narrativas/treinar/{d}/index.html')
                frio = [x for x in itens if x.get('rot') == 'A frio']
                self.assertEqual(len(frio), 1)
                self.assertFalse([x for x in itens if x.get('rot') == 'Troca'])
                x = frio[0]
                if d == 'rascunho-mau':
                    self.assertEqual(x['titulo'], 'Só teu')
                    self.assertTrue(x['html'].startswith('<p>Não se mostra: este rascunho é só teu.</p>'))
                else:
                    self.assertEqual(x['titulo'], 'Noutro dia, a frio')
                    self.assertIn('<p class="sub">A tua leitura a frio não é um veredito: é informação. Se não leste o que querias, muda uma pista e diz porquê.</p>', x['html'])
                self.assertIsNone(PARES.search(x['html']))
                self.assertNotIn('alguém em casa', x['html'])
        voz = [x for x in cartoes('narrativas/treinar/voz-alta/index.html') if x.get('rot') == 'A frio'][0]
        self.assertIn('<b>Outra vez:</b> Um texto teu mais antigo, lido em voz alta sem o releres antes.', voz['html'])
        # o guia do docente acompanha: o passo é escrito, no caderno, e a grelha avalia a leitura a frio
        doc = ler('narrativas/treinar/docente/index.html')
        self.assertIn('<td>3 min</td><td>Caderno</td><td>Reler a frio: noutro dia, quem escreveu responde por escrito a uma pergunta sobre o próprio texto.</td>', doc)
        self.assertIn('<td>Leitura a frio</td><td>Noutro dia, o texto percebe-se sem explicação? Onde se perde a leitura?</td>', doc)
        self.assertNotIn('<td>Oral</td>', doc)

    def test_sem_pares_nem_colega_nos_sitios_visados(self):
        for f in visados():
            with self.subTest(ficheiro=f):
                s = ler(f)
                sobra = [s[max(0, m.start() - 30):m.end() + 30] for m in PARES.finditer(s)]
                aceites = EXCECOES.get(f, [])
                self.assertEqual(len(sobra), len(aceites), sobra)
                for a in aceites:
                    self.assertEqual(s.count(a), 1, a)
        # as variantes e os catálogos de Ver para fazer (achados 1, 14 e 15)
        variantes = ler('narrativas/variantes/index.html')
        self.assertNotIn('individual ou a pares', variantes)
        self.assertEqual(variantes.count(' · papel e lápis · individual</p>'), 3)
        cat = ler('ver-para-fazer/catalogo.json')
        for novo in ('Podes ditar a cena ou relê-la noutro dia.', 'Podes responder por escrito ou ditar ao docente.',
                     'Marca pausas e palavras a destacar, por escrito ou ditando ao docente.'):
            self.assertEqual(cat.count(novo), 1, novo)
        # fora-da-pagina: a página da secção e as subpáginas dizem o mesmo
        hub = ler('narrativas/fora-da-pagina/index.html')
        for sub, frase in (('escultura', '(noutro dia, relê-as sem a resposta à frente: o detalhe ainda as sustenta?)'),
                           ('escultura', 'e explicar oralmente as tuas escolhas.'),
                           ('intervalo', 'propõe duas hipóteses só pelos indícios, como se não conhecesses a intenção.'),
                           ('tese', 'não atribuas sentimentos a ninguém por adivinhação.'),
                           ('tese', 'Depois de uma pausa, explica tu as três relações sem ajuda.')):
            self.assertEqual(hub.count(frase), 1, frase)
            self.assertEqual(ler(f'narrativas/fora-da-pagina/{sub}/lesson.js').count(frase), 1, (sub, frase))

    def test_jogo_folha_e_grupo_nos_catalogos(self):
        # decisão (f) e achados 16 e 24
        v48 = ler('ver-para-fazer/v48/index.html')
        self.assertIn('<p class="vpf-porque">Um exemplo concreto de associação; o original é em japonês.</p>', v48)
        self.assertIsNone(PROIBIDAS.search(re.sub(r'<[^>]+>|data-titulo="[^"]*"', ' ', v48.split('<main', 1)[1].split('</main>')[0])))
        itens = itens_curadoria()
        self.assertEqual(itens['vid-048']['editorial_reason'], 'Propõe um exemplo concreto de associação; o original é em japonês, pelo que requer apoio linguístico.')
        v044 = itens['vid-044']
        self.assertEqual(v044['objective'], 'Criar com informação parcial')
        self.assertEqual(v044['proposed_activity'], 'Dobra um papel em partes e desenha numa parte de cada vez, sem ver o desenho anterior. No fim, constrói uma história para o conjunto.')
        self.assertEqual(v044['materials'], 'Papel e lápis')
        for k in ('objective', 'proposed_activity', 'materials'):
            self.assertIsNone(PROIBIDAS.search(v044[k]))
            self.assertIsNone(PARES.search(v044[k]))
        v44 = ler('ver-para-fazer/v44/index.html')
        self.assertEqual(v44.count('Com papel dobrado em partes, desenha numa parte de cada vez, sem ver o desenho anterior; no fim, uma história para o conjunto.'), 2)
        self.assertEqual(v44.count('Criar com informação parcial.'), 2)
        for fora in ('à vez com alguém', 'colaborativamente'):
            self.assertNotIn(fora, v44)
            self.assertNotIn(fora, ler('curadoria/catalogo-123.json'))

    def test_regras_de_texto_nos_textos_novos(self):
        for f, trocas in json.loads(ler(MANIFESTO)).items():
            for antigo, novo, n in trocas:
                with self.subTest(ficheiro=f, novo=novo[:50]):
                    txt = re.sub(r'<[^>]+>', ' ', novo.replace('\\"', '"').replace('<\\/', '</'))
                    if f == 'curadoria/catalogo-123.json' and '"id": "vid-109"' in novo:
                        continue  # só o contexto da troca que apaga o registo da v108
                    self.assertNotIn('—', txt)
                    self.assertIsNone(PROIBIDAS.search(txt))
                    self.assertIsNone(PARES.search(txt))
                    if not re.match(r'^\d+–\d+ min · papel e lápis · individual$', novo):
                        self.assertNotRegex(txt, r'[^\s"]\s·\s[^\s"]')  # nunca «·» dentro de uma frase

    def test_fluxo_corre_a_camada(self):
        wf = ler('.github/workflows/cartaz-qa.yml')
        self.assertIn('- run: python tools/creditos_i.py --verificar --manifesto ' + MANIFESTO + '\n', wf)
        caminhos = re.findall(r"paths: \[(.*?)\]", wf)
        self.assertEqual(len(caminhos), 2)
        for linha in caminhos:
            for c in ("'" + MANIFESTO + "'", "'tests/revisao_geral_lente_20261115.py'", "'tests/test_revisao_geral_lente_20261115.py'"):
                self.assertIn(c, linha, c)


if __name__ == '__main__':
    unittest.main()
