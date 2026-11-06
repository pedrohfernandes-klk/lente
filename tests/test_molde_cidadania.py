"""05/11/2026: plano do molde da Cidadania (plano-molde-20261105.md, secção 5), pedido 1: motor, casca e progresso, sem
conteúdo novo. Verifica o que já faz sentido sem as sessões novas:
- o cfg da família da Cidadania (aula, semPontos, preservarAnterior, retomar, feita, fim) e o progresso comum nas páginas;
- o contrato do validador, opcional por ficheiro ("molde": "cidadania-2026-11"): as lições sem o campo validam como até aqui,
  uma lição de ensaio (tests/fixtures/molde_ensaio.py, nunca publicada) cumpre-o, e cada regra apanha o seu erro;
- a posição da resposta certa calculada com a semente do motor (o port em Python é igual ao código de assets/licoes/jogo.js);
- as peças comuns: aulas claras e ampliação copiadas do Português, o «i» dos créditos, a peça dos artefactos, o COMO do Lente.
O resto do contrato (as vinte sessões, cada R2 com palavras da sessão de origem) entra com a s01. O percurso no navegador
(retoma a meio, ordem fixa, estado antigo «Feita», posições, artefactos, «i», projeção) está em tests/browser_licoes_lente.cjs."""
import copy, importlib.util, json, pathlib, re, subprocess, sys, unittest
from html import escape as html_escape, unescape as html_unescape

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('licoes_lente', ROOT / 'tools/licoes_lente.py')
L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
sys.path.insert(0, str(ROOT / 'tests' / 'fixtures'))
import molde_ensaio as E  # noqa: E402

FONTES = sorted((ROOT / 'tools/licoes').glob('*.json'))
CIDADANIA = [p for p in FONTES if p.name.startswith('cidadania-')]
# 05/11/2026 (pedido 2): as sessões já no molde final, numa lista fechada (só a s01 do M1 até o docente dizer que sim às outras
# dezanove, decisão 157); as outras continuam no piloto e sem as peças novas.
# 06/11/2026 (decisão 166): a s02 do M1 entra na lista, depois de a s01 ser aprovada e publicada (lente #126).
# 06/11/2026 (decisões 166 a 168): e a s03 do M1, pelo mesmo molde, uma de cada vez.
NO_MOLDE = {'cidadania-m1-s01.json', 'cidadania-m1-s02.json', 'cidadania-m1-s03.json'}
# 06/11/2026 (decisões 166 a 168): e a s08 do M1, feita fora de ordem (as s04 a s07 entram pelos seus ramos).
NO_MOLDE |= {'cidadania-m1-s08.json'}
PILOTO = [p for p in CIDADANIA if p.name not in NO_MOLDE]


def carregar(p):
    return json.loads(p.read_text('utf-8'))


def cfg_da_pagina(s):
    m = re.search(r',CFG=(\{.*?\});var el=', s)
    return json.loads(m.group(1))


class CfgDaFamilia(unittest.TestCase):
    def test_cfg_da_cidadania(self):
        cfg = L.FAMILIAS['cidadania']['cfg']
        self.assertIs(cfg['aula'], True)               # a ordem dos cartões e das opções é fixa e igual em todos os ecrãs
        self.assertIs(cfg['semPontos'], True)          # sem pontos nem sequências
        self.assertIs(cfg['preservarAnterior'], True)  # subir a versão conserva o «feita»
        self.assertEqual(cfg['retomar'], 12)           # recarregar a meio volta ao mesmo cartão durante 12 horas
        self.assertEqual(cfg['feita'], 'Sessão feita.')
        self.assertIn('O módulo já a marca.', L.FIM_CIDADANIA)
        # 05/11/2026: correções da revisão da s01 (06/11/2026). Nas sessões no molde, a retoma dura oito dias (a segunda aula de
        # 90 minutos, noutro dia, continua no cartão 16) e o fim diz onde fica marcada a sessão; as do piloto ficam como estavam.
        self.assertEqual(L.RETOMAR_MOLDE, 192)
        self.assertEqual(L.FIM_MOLDE, L.FIM_CIDADANIA.replace('O módulo já a marca.', 'A página do módulo já a marca como feita.'))
        # o Laboratório fica como estava
        self.assertEqual(L.FAMILIAS['laboratorio']['cfg'], {'semPontos': True, 'preservarAnterior': True})

    def test_as_dez_sessoes_do_piloto_levam_o_cfg_e_o_progresso_comum(self):
        self.assertEqual(len(CIDADANIA), 10)
        for p in CIDADANIA:
            d = carregar(p)
            s = (ROOT / d['saida']).read_text('utf-8')
            cfg = cfg_da_pagina(s)
            # 05/11/2026: correções da revisão da s01 (06/11/2026): no molde, a retoma é a de RETOMAR_MOLDE e o fim é FIM_MOLDE; o
            # resto do cfg é o da família, chave a chave, como antes
            esperado = dict(L.FAMILIAS['cidadania']['cfg'], **({'retomar': L.RETOMAR_MOLDE} if p.name in NO_MOLDE else {}))
            for k, v in esperado.items():
                self.assertEqual(cfg.get(k), v, p.name + ': ' + k)
            self.assertIs(cfg['variar'], False)
            fim, outro = (L.FIM_MOLDE, L.FIM_CIDADANIA) if p.name in NO_MOLDE else (L.FIM_CIDADANIA, L.FIM_MOLDE)
            self.assertEqual(s.count(fim), 1, p.name)
            self.assertEqual(s.count(outro), 0, p.name)
            prog = s.index('assets/licoes/' + L.PROGRESSO)
            self.assertLess(prog, s.index('assets/licoes/jogo.js'), p.name)
            # sem molde, nenhuma peça nova entra na página; 05/11/2026 (pedido 2): com molde (a lista fechada NO_MOLDE),
            # entram todas, e o .json tem o campo
            for f in ('assets/licoes/aula-clara', 'assets/licoes/casca-pc', 'assets/licoes/ampliar-documentos', 'assets/licoes/recolha',
                      'assets/info-i', ' molde-cidadania', 'EPIRecolha'):
                if p.name in NO_MOLDE:
                    self.assertIn(f, s, p.name + ': ' + f)
                else:
                    self.assertNotIn(f, s, p.name + ': ' + f)
            self.assertEqual(d.get('molde') == L.MOLDE, p.name in NO_MOLDE, p.name)

    def test_o_laboratorio_carrega_o_progresso_comum(self):
        for p in FONTES:
            d = carregar(p)
            if d.get('familia') != 'laboratorio':
                continue
            s = (ROOT / d['saida']).read_text('utf-8')
            self.assertIn('assets/licoes/' + L.PROGRESSO, s)
            self.assertNotIn('progresso-laboratorio.js', s)
        self.assertFalse((ROOT / 'assets/licoes/progresso-laboratorio.js').exists())


class ContratoOpcional(unittest.TestCase):
    def test_sem_molde_tudo_como_hoje(self):
        # 05/11/2026 (pedido 2): só as sessões da lista fechada NO_MOLDE têm o campo; todas validam (as do molde, com o contrato)
        for p in FONTES:
            d = carregar(p)
            if p.name not in NO_MOLDE:
                self.assertNotIn('molde', d, p.name)
            self.assertEqual(L.validar(d), [], p.name)

    def test_com_molde_o_contrato_aplica_se(self):
        # 05/11/2026 (pedido 2): a primeira sessão ainda sem molde (a s01 já o tem e cumpre-o)
        d = carregar(PILOTO[0])
        erros = L.validar(dict(d, molde=L.MOLDE))
        self.assertTrue(any(e.startswith('molde') for e in erros), erros)
        self.assertFalse(any(e.startswith('molde') for e in L.validar(d)))
        self.assertIn('molde desconhecido', ' | '.join(L.validar(dict(d, molde='cidadania-2099'))))
        lab = carregar(next(p for p in FONTES if carregar(p).get('familia') == 'laboratorio'))
        self.assertIn('só se aplica às sessões da Cidadania', ' | '.join(L.validar(dict(lab, molde=L.MOLDE))))

    def test_o_ensaio_cumpre_o_contrato(self):
        self.assertEqual(L.validar(E.licao()), [])


class ContratoApanhaOsErros(unittest.TestCase):
    def com(self, f):
        d = E.licao()
        f(d)
        return ' | '.join(L.validar(d))

    def idx(self, d, rot):
        return next(i for i, c in enumerate(d['cartoes']) if c.get('rot') == rot)

    def test_abre_decide_e_recupera(self):
        self.assertIn('linha «Hoje»', self.com(lambda d: d['cartoes'][0].pop('aula')))
        self.assertIn('Caso inventado', self.com(lambda d: d['cartoes'][0].__setitem__('html', d['cartoes'][0]['html'].replace('Caso inventado.', 'Caso.'))))
        self.assertIn('três lados', self.com(lambda d: d['cartoes'][1].__setitem__('html', d['cartoes'][1]['html'].replace('<details class="lado"><summary>Uma objeção', '<details class="outro"><summary>Uma objeção'))))
        self.assertIn('Não há resposta certa', self.com(lambda d: d['cartoes'][1].__setitem__('html', d['cartoes'][1]['html'].replace('Não há resposta certa', 'Escolhe'))))
        self.assertIn('«Recupera»', self.com(lambda d: d['cartoes'][2].pop('g')))
        self.assertIn('sessão de origem', self.com(lambda d: d['cartoes'][3].pop('origem')))

    def test_cada_exercicio(self):
        k = 9  # uma escolha depois do Lê
        self.assertIn('«rot» próprio', self.com(lambda d: d['cartoes'][k].__setitem__('rot', 'Escolhe')))
        self.assertIn('falta «p2»', self.com(lambda d: d['cartoes'][k].pop('p2')))
        self.assertIn('do exercício', self.com(lambda d: d['cartoes'][10].__setitem__('fe', 'Volta ao enunciado do exercício.')))
        self.assertIn('da opção', self.com(lambda d: d['cartoes'][10].__setitem__('f', 'O texto da opção certa diz tudo.')))
        self.assertIn('«tipo»', self.com(lambda d: d['cartoes'][k].pop('tipo')))
        self.assertIn('nenhuma escrita', self.com(lambda d: d['cartoes'][k].__setitem__('prod', 'escrita')))
        # 05/11/2026: correções da revisão da s01 (06/11/2026). Cada exercício tem a sua pista, que não dá a resposta: nem a opção
        # certa, nem as palavras certas de um sublinhar, nem o lado direito de um par; e nenhum passo de um ordenar fica no seu
        # lugar na ordem do ecrã (a semente do motor com a rotação de semNoLugar).
        self.assertIn('falta a pista', self.com(lambda d: d['cartoes'][k].pop('pista')))
        self.assertIn('a pista dá a resposta', self.com(lambda d: d['cartoes'][k].__setitem__('pista', 'Pensa: ' + d['cartoes'][k]['o'][d['cartoes'][k]['c']] + '?')))
        sub = lambda d: next(c for c in d['cartoes'] if c['t'] == 'sublinhar')
        self.assertIn('a pista dá a resposta', self.com(lambda d: sub(d).__setitem__('pista', 'Procura «vida privada».')))
        par = lambda d: next(c for c in d['cartoes'] if c['t'] == 'emparelhar')
        self.assertIn('a pista dá a resposta', self.com(lambda d: par(d).__setitem__('pista', 'Um deles é o Par de ensaio A.')))
        self.assertEqual(L.sem_no_lugar([0, 3, 1, 2]), [2, 0, 3, 1])
        self.assertEqual(L.sem_no_lugar([0, 1]), [1, 0])
        for d in (E.licao(), carregar(ROOT / 'tools/licoes/cidadania-m1-s01.json')):
            for i, c in enumerate(d['cartoes']):
                if c['t'] == 'ordenar':
                    ordem = L.ordem_ordenar(d, i)
                    self.assertEqual(sorted(ordem), list(range(len(c['passos']))))
                    self.assertFalse(any(j == q for q, j in enumerate(ordem)), (d['id'], i, ordem))
        L_sem = L.sem_no_lugar
        try:
            L.sem_no_lugar = lambda a: list(range(len(a)))  # um motor que deixasse tudo no lugar seria apanhado
            self.assertIn('fica no seu lugar', ' | '.join(L.validar(E.licao())))
        finally:
            L.sem_no_lugar = L_sem

    def test_contagens_e_ordem(self):
        self.assertIn('13 cartões de fazer', self.com(lambda d: d['cartoes'].pop(10)))
        self.assertIn('três cartões seguidos', self.com(lambda d: d['cartoes'].insert(2, E.ler('Olha', 'Olha', '<div class="m-olha"><p>Ensaio.</p></div>', 1))))
        self.assertIn('seis exercícios de aplicar ou transferir', self.com(lambda d: [c.__setitem__('tipo', 'reconhecer') for c in d['cartoes'] if c['t'] != 'ler']))
        self.assertIn('conceito espaçado', self.com(lambda d: d['cartoes'][13].pop('origem')))
        self.assertIn('não há «Na aula»', self.com(lambda d: d['cartoes'][self.idx(d, 'Volta ao caso')].__setitem__('rot', 'Na aula')))

    def test_em_turma_papel_e_fim(self):
        t = lambda d: d['cartoes'][self.idx(d, 'Em turma')]
        self.assertIn('quatro campos', self.com(lambda d: t(d).__setitem__('html', t(d)['html'].replace('Se estás sozinho', 'Sozinho'))))
        self.assertIn('exatamente um', self.com(lambda d: d['cartoes'][self.idx(d, 'Volta ao caso')].__setitem__('rot', 'Em turma')))
        self.assertIn('posição depois do material', self.com(lambda d: t(d).__setitem__('html', t(d)['html'].replace('class="posicao"', 'class="pos"'))))
        self.assertIn('«Agora, em papel»', self.com(lambda d: d['cartoes'][-2].__setitem__('html', d['cartoes'][-2]['html'].replace('O que conta', 'Critérios'))))
        self.assertIn('falta «depois»', self.com(lambda d: d.pop('depois')))

    def test_palavras_e_tempos(self):
        self.assertIn('palavras à vista', self.com(lambda d: d['cartoes'][7].__setitem__('html', d['cartoes'][7]['html'] + '<p>' + 'ensaio ' * 60 + '</p>')))
        # o que está dentro de um details conta à parte
        self.assertEqual(L.validar(E.copia(cartoes=[dict(c, html=c['html'] + '<details class="mais"><summary>Ler mais</summary><div><p>' + 'ensaio ' * 90 + '</p></div></details>') if i == 7 else c for i, c in enumerate(E.licao()['cartoes'])])), [])
        self.assertIn('minutos (entre 175 e 185)', self.com(lambda d: d['tempos'].__setitem__('projeto', 20)))
        self.assertIn('«min»', self.com(lambda d: d['cartoes'][4].pop('min')))

    def test_turma_docente_referencias(self):
        k = 9
        self.assertIn('«grupo»', self.com(lambda d: d['cartoes'][k].__setitem__('p', 'Ensaio: o que decide o teu grupo?')))
        self.assertEqual(L.validar(E.copia(cartoes=[dict(c, p='Ensaio: a fotografia pode ficar no grupo da turma?') if i == k else c for i, c in enumerate(E.licao()['cartoes'])])), [])
        self.assertEqual(L.validar(E.copia(cartoes=[dict(c, html=c['html'].replace('Página de ensaio', 'Página de ensaio, num grupo de amigos,')) if i == 0 else c for i, c in enumerate(E.licao()['cartoes'])])), [])
        self.assertIn('depende do docente', self.com(lambda d: d['cartoes'][k].__setitem__('p', 'Ensaio: espera que o docente explique.')))
        self.assertIn('espaço inseparável', self.com(lambda d: d['cartoes'][7].__setitem__('html', d['cartoes'][7]['html'].replace('artigo 12.º', 'artigo 12.º'))))
        self.assertIn('espaço inseparável', self.com(lambda d: d['cartoes'][7].__setitem__('html', d['cartoes'][7]['html'].replace('n.º 2', 'n.º 2'))))
        # 05/11/2026: correções da revisão da s01 (06/11/2026; decisão 152): também as datas e os números com unidade ou nome
        for partido in ('ratificada a 21 de setembro de 1990', 'em novembro de 1949', 'uma rapariga de 12 anos', 'mais 1 min', 'Os 180 minutos'):
            self.assertIn('espaço inseparável', self.com(lambda d: d['cartoes'][k].__setitem__('f', 'Ensaio: ' + partido + '.')), partido)
        self.assertIn('espaço inseparável', self.com(lambda d: d['cartoes'][k].__setitem__('pista', 'Ensaio: lê o artigo 12.º.')))
        for inteiro in ('ratificada a 21\u00a0de\u00a0setembro\u00a0de\u00a01990', 'uma rapariga de 12\u00a0anos', 'em 2015, o tribunal'):
            self.assertEqual(L.validar(E.copia(cartoes=[dict(c, f='Ensaio: ' + inteiro + '.') if i == k else c for i, c in enumerate(E.licao()['cartoes'])])), [], inteiro)

    def test_imagens_e_creditos(self):
        o = lambda d: d['cartoes'][4]
        self.assertIn('atrás do «i»', self.com(lambda d: o(d).__setitem__('html', re.sub(r'<details class="info-i".*?</details>', '', o(d)['html'], flags=re.S))))
        self.assertIn('diz a licença', self.com(lambda d: o(d).__setitem__('html', o(d)['html'].replace('CC BY 2.0</a>', 'CC BY-NC 2.0</a>'))))
        self.assertIn('diz a licença', self.com(lambda d: o(d).__setitem__('html', o(d)['html'].replace('<a href="https://www.flickr.com/photos/fdrlibrary/27758131387/">Registo de origem</a>. ', ''))))
        self.assertIn('é um div', self.com(lambda d: o(d).__setitem__('html', o(d)['html'].replace('<div class="moldura com-i">', '<span class="moldura com-i">').replace('</details></div>', '</details></span>'))))
        self.assertIn('a legenda só diz', self.com(lambda d: o(d).__setitem__('html', o(d)['html'].replace('circula em cartaz.</figcaption>', 'circula em cartaz. CC BY 2.0.</figcaption>'))))

    def test_posicao_da_certa(self):
        self.assertIn('mais de metade', ' | '.join(L.validar(E.licao(lugares=(0, 0, 1, 0, 2, 0)))))
        self.assertIn('três vezes seguidas', ' | '.join(L.validar(E.licao(lugares=(1, 2, 2, 2, 0, 1)))))
        self.assertEqual(L.posicoes_certas(E.licao()), [0, 2, 1, 0, 1, 2])


class SementeDoMotor(unittest.TestCase):
    def test_o_port_e_o_codigo_do_motor(self):
        """As funções do motor (semear, rnd, mist, opcoes) correm em Node, tiradas de assets/licoes/jogo.js, e dão a mesma
        ordem que o port em Python, para todas as escolhas das lições e do ensaio (com quatro opções também)."""
        js = (ROOT / 'assets/licoes/jogo.js').read_text('utf-8')
        partes = [re.search(r'var semente=0;function rnd\(\)\{.*?\}', js).group(0), re.search(r'function semear\(x\)\{.*?semente=h\}', js).group(0),
                  re.search(r'function mist\(a\)\{.*?return a\}', js).group(0), re.search(r'function opcoes\(o,c\)\{.*?return mist\(\[Number\(c\)\]\.concat\(err\)\)\}', js).group(0)]
        casos = []
        licoes = [carregar(p) for p in FONTES] + [E.licao()]
        quatro = E.licao()
        quatro['cartoes'][9]['o'].append('Uma quarta linha de ensaio')
        quatro['cartoes'][9]['c'] = 3
        licoes.append(quatro)
        for d in licoes:
            C = L.LC.cartoes(d)
            for k, ordem in L.ordem_opcoes(d):
                casos.append({'K': d['chave'], 'k': k, 'n': len(C), 'o': C[k]['o'], 'c': C[k]['c'], 'esperado': ordem})
        self.assertGreater(len(casos), 40)
        # o código do motor corre dentro de uma função que define K, TODOS e cfg, como dentro de montar(); baralhar (o acaso)
        # nunca pode ser chamado com cfg.aula
        prog = ('"use strict";var casos=JSON.parse(require("fs").readFileSync(0,"utf8")),mal=[];'
                'casos.forEach(function(caso){var cfg={aula:true},K=caso.K,TODOS=[],baralhar=function(){throw new Error("baralhar")};'
                'for(var q=0;q<caso.n;q++)TODOS.push({});' + ';'.join(partes) + ';'
                'semear(TODOS[caso.k]);var r=opcoes(caso.o,caso.c);'
                'if(JSON.stringify(r)!==JSON.stringify(caso.esperado))mal.push([K,caso.k,r,caso.esperado])});'
                'process.stdout.write(JSON.stringify(mal))')
        r = subprocess.run(['node', '-e', prog], input=json.dumps(casos), capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), [])


class PecasComuns(unittest.TestCase):
    def ler(self, rel):
        return (ROOT / rel).read_text('utf-8')

    def test_copias_do_portugues(self):
        for f, origem in (('assets/licoes/aula-clara.css', 'pt/assets/pt-lessons/aula-clara.css'), ('assets/licoes/aula-clara.js', 'pt/assets/pt-lessons/aula-clara.js'),
                          ('assets/licoes/ampliar-documentos.js', 'pt/assets/ampliar-documentos.js'), ('assets/licoes/ampliar-documentos.css', 'pt/assets/ampliar-documentos.css'),
                          ('assets/licoes/casca-pc.css', 'pt main'), ('assets/licoes/casca.js', 'pt/assets/pt-lessons/casca.js')):
            self.assertIn('Cópia d', self.ler(f).splitlines()[0], f)
            self.assertIn(origem, self.ler(f).splitlines()[0], f)
        self.assertIn('var COMO="https://pedrohfernandes-klk.github.io/lente/como/";', self.ler('assets/licoes/casca.js'))
        self.assertIn('aria-modal="true"', self.ler('assets/licoes/casca.js'))  # a correção de foco do Português
        self.assertIn('window.EPIAmpliar', self.ler('assets/licoes/ampliar-documentos.js'))
        self.assertIn('data-cc-mais', self.ler('assets/licoes/aula-clara.js'))
        self.assertIn('min-width:1024px', self.ler('assets/licoes/casca-pc.css'))

    def test_peca_i(self):
        css, js = self.ler('assets/info-i.css'), self.ler('assets/info-i.js')
        for x in ('.info-i>summary{', 'inline-size:44px;block-size:44px', '.info-i--linha', '.info-i::details-content{content-visibility:visible',
                  '.info-i-texto a[rel~=license]{white-space:nowrap}', 'content:" (" attr(href) ")"', 'forced-colors:active', 'prefers-reduced-motion'):
            self.assertIn(x, css)
        for x in ("e.key !== 'Escape'", "querySelector('summary')", "SEL + '[open]'", 'projetar=1', 'MutationObserver'):
            self.assertIn(x, js)
        self.assertNotIn('localStorage', js)  # o «i» nunca grava nada

    def test_peca_dos_artefactos(self):
        js = self.ler('assets/licoes/recolha.js')
        for x in ('window.EPIRecolha', 'Copiar para as notas', 'navigator.share', 'projecao()', 'takeRecords', 'Guardaste: '):
            self.assertIn(x, js)
        self.assertNotIn('fetch(', js)  # só no aparelho, nunca na entrega
        self.assertEqual(L.recolha_cfg(carregar(CIDADANIA[0]))['chave'], 'epi-cid-m1-artefactos')

    def test_pagina_do_molde(self):
        d = E.licao()
        s = L.pagina(d)
        self.assertIn('class="licao-lente licao-cidadania molde-cidadania"', s)
        for f in ('aula-clara.css', 'casca-pc.css', 'ampliar-documentos.css', 'recolha.css', 'assets/info-i.css'):
            self.assertLess(s.index(f), s.index('assets/licoes/cidadania.css'), f)  # o CSS da família tem a última palavra
        for f in ('aula-clara.js', 'ampliar-documentos.js', 'assets/info-i.js', 'recolha.js', L.PROGRESSO):
            self.assertLess(s.index(f), s.index('assets/licoes/jogo.js'), f)
        # 06/11/2026: fusão com os menus do Laboratório e das lições (decisão 163). O menu ≡ comum (tools/menu_casca.py) escreve o
        # item com o ícone e a seta; continua a ir para os vídeos do Lente, e o item confere-se inteiro.
        self.assertIn(f'<a href="{L.COMO_LENTE}">{L.MC.ic("como")}<span>Como se faz (vídeos)</span><span class="seta" aria-hidden="true">→</span></a>', s)
        self.assertIn('EPIRecolha.ligar({"chave": "epi-cid-m1-artefactos", "sessao": "epi-cid-m1-s99"', s)
        self.assertLess(s.index('EPIRecolha.ligar('), s.index('EPIJogo.montar(CFG)'))
        cfg = cfg_da_pagina(s)
        self.assertEqual(cfg['pistas'], d['pistas'])
        self.assertEqual(cfg['depois'], d['depois'])
        self.assertEqual(cfg['retomar'], L.RETOMAR_MOLDE)  # 05/11/2026: correções da revisão da s01 (06/11/2026)

    def test_css_da_cidadania_so_no_molde(self):
        css = self.ler('assets/licoes/cidadania.css')
        bloco = css.split('/* ==== molde cidadania-2026-11 ==== */', 1)[1]
        self.assertIn('--cid:#1f4e79', bloco); self.assertIn('--cid:#9cc1e8', bloco)
        self.assertIn('var(--cartaz', bloco)                    # títulos e frase do Para levar em letra de cartaz
        self.assertIn('@media (min-width:1100px)', bloco)       # o Olha acima de 1100 px
        self.assertIn('html.em-projecao body.molde-cidadania', bloco)
        self.assertNotRegex(bloco, r'c-barra')                  # o azul nunca entra na barra


class SessaoS01(unittest.TestCase):
    """05/11/2026: plano do molde, pedido 2. A sessão 01 do M1 na versão final: o contrato, o registo dos excertos (secção 5), o
    R2 com palavras da sessão de origem, o conceito espaçado, o caso real com fonte oficial (decisão 161), a imagem com o crédito
    atrás do «i» (decisão 153), nenhum vídeo (decisão 155) e a versão para imprimir sem respostas."""
    D = carregar(ROOT / 'tools/licoes/cidadania-m1-s01.json')
    REG = {x['id']: x for x in json.loads((ROOT / 'tools/cidadania_fontes.json').read_text('utf-8'))['excertos']}

    @staticmethod
    def norm(t):
        return ' '.join(html_unescape(re.sub(r'<[^>]+>', ' ', t)).replace('\u00a0', ' ').split())

    def confere(self, ident, texto, onde):
        r = self.REG.get(ident)
        self.assertIsNotNone(r, f'{onde}: «{ident}» fora do registo')
        self.assertIs(r['confirmado'], True, ident)
        alvo = self.norm(r['texto'])
        pedacos = [self.norm(x).strip(' «»') for x in re.split(r'\[…\]', texto)]
        self.assertTrue(any(pedacos), onde)
        for x in pedacos:
            if x:
                self.assertIn(x, alvo, f'{onde}: «{x}» não está, letra a letra, em {ident}')

    def test_contrato_e_cfg(self):
        self.assertEqual(self.D['molde'], L.MOLDE)
        self.assertEqual(L.validar(self.D), [])
        self.assertEqual(self.D['saida'], 'cidadania/m1/sessoes/01/index.html')
        self.assertEqual(self.D['chave'], 'epi-cid-m1-s01')
        cfg = cfg_da_pagina((ROOT / self.D['saida']).read_text('utf-8'))
        for k in ('aula', 'semPontos', 'preservarAnterior'):
            self.assertIs(cfg[k], True, k)
        # 05/11/2026: correções da revisão da s01 (06/11/2026): a retoma de oito dias e uma pista própria em cada exercício (as
        # pistas escolhidas por palavras saíram)
        self.assertEqual(cfg['retomar'], 192)
        self.assertNotIn('pistas', cfg)
        self.assertTrue(all(c.get('pista') for c in self.D['cartoes'] if c['t'] != 'ler'))
        C = self.D['cartoes']
        self.assertEqual(len(C), 23)
        self.assertEqual(sum(c['t'] == 'ler' for c in C), 9)
        self.assertEqual([c['rot'] for c in C if c['t'] == 'ler'],
                         ['Abre', 'Decide', 'Olha', 'Lê', 'Conceito', 'Volta ao caso', 'Em turma', 'Agora, em papel', 'Para levar'])

    def test_registo_dos_excertos(self):
        for r in self.REG.values():
            self.assertTrue(r['texto'] and r['fonte'] and r['ligacao'].startswith('https://'), r['id'])
            self.assertRegex(r['consultado'], r'^\d{4}-\d{2}-\d{2}$')
            self.assertIs(r['confirmado'], True, r['id'])
            # 06/11/2026 (sessão 08): também o sítio do Provedor de Justiça, um órgão do Estado (decisão 161: o caso real vem de um
            # tribunal ou de um organismo público); só esse domínio entra, e só para o boletim registado em prov-2016-pdm.
            self.assertTrue(any(d in r['ligacao'] for d in ('unric.org', 'diariodarepublica.pt', 'dgsi.pt'))
                            or (r['id'] == 'prov-2016-pdm' and r['ligacao'].startswith('https://provedor-jus.pt/')), r['id'])

    def test_cada_excerto_esta_no_registo_e_confirmado(self):
        vistos = 0
        for i, c in enumerate(self.D['cartoes'], 1):
            h = c.get('html') or ''
            # cada parágrafo de lei em citação tem de dizer de onde vem
            for bq in re.findall(r'<blockquote class="lei">(.*?)</blockquote>', h, re.S):
                self.assertEqual(len(re.findall(r'<p\b', bq)), len(re.findall(r'<p\b[^>]*data-fonte=', bq)), f'cartão {i}')
            for tag, ident, corpo in re.findall(r'<(p|span)\b[^>]*data-fonte="([^"]+)"[^>]*>(.*?)</\1>', h, re.S):
                corpo = re.sub(r'<span class="art">.*?</span>', '', corpo)
                self.confere(ident, corpo, f'cartão {i}')
                vistos += 1
            if c.get('fonte'):
                # 05/11/2026: correções da revisão da s01 (06/11/2026). Uma citação pode juntar passagens de várias entradas do
                # registo (o caso real: a ordem e a fundamentação do acórdão): «fonte» é então a lista, e cada pedaço entre «[…]»
                # confere-se, letra a letra e pela ordem, com a sua entrada; o número de pedaços tem de ser o de entradas.
                texto = c.get('cita') or c.get('frase')
                if isinstance(c['fonte'], list):
                    pedacos = re.split(r'\s*\[…\]\s*', texto)
                    self.assertEqual(len(pedacos), len(c['fonte']), f'cartão {i}')
                    for ident, pedaco in zip(c['fonte'], pedacos):
                        self.confere(ident, pedaco, f'cartão {i}')
                else:
                    self.confere(c['fonte'], texto, f'cartão {i}')
                vistos += 1
            texto = self.norm(' '.join([c.get('f', '')] + (c['fe'] if isinstance(c.get('fe'), list) else [c.get('fe') or ''])
                                       + [x for par in c.get('pares', []) for x in par]))
            for ident, frase in c.get('citacoes', []):
                self.confere(ident, frase, f'cartão {i}')
                self.assertIn(self.norm(frase), texto, f'cartão {i}: a citação registada está no cartão')
                # 05/11/2026: correções da revisão da s01 (06/11/2026). Mais estrito: o «…» inteiro que contém a frase registada é
                # texto exato do registo, com «[…]» em cada corte (apanha um ponto final que a fonte não tem)
                aspas = [q for q in re.findall(r'«([^«»]*)»', texto) if self.norm(frase) in q]
                self.assertTrue(aspas, f'cartão {i}: «{frase}» está entre aspas')
                for q in aspas:
                    for pedaco in re.split(r'\s*\[…\]\s*', q):
                        if pedaco.strip():
                            self.assertIn(pedaco.strip(), self.norm(self.REG[ident]['texto']), f'cartão {i}: «{q}» não é texto exato de {ident}')
                vistos += 1
        self.assertGreaterEqual(vistos, 20)
        # os artigos que a tarefa pede: Declaração 1.º, 12.º (até «honra e reputação») e 19.º; Constituição 26.º, n.º 1, e 34.º
        tudo = json.dumps(self.D, ensure_ascii=False)
        for ident in ('dudh-1', 'dudh-12', 'dudh-19', 'crp-26-1', 'crp-34-1', 'tre-2015-ordem'):
            self.assertIn(ident, tudo)
        le = next(c for c in self.D['cartoes'] if c['rot'] == 'Lê')
        self.assertIn('nem ataques à sua honra e reputação.', self.norm(L.sem_details(le['html'])))

    def test_recupera_e_conceito_espacado(self):
        C = self.D['cartoes']
        r2 = C[3]
        self.assertEqual(r2['g'], 'recupera')
        origem = (ROOT / r2['origem'] / 'index.html').read_text('utf-8')
        citadas = re.findall(r'«([^»]{8,})»', r2['fe'] + ' ' + r2['f'])
        self.assertTrue(any(self.norm(q) in self.norm(origem) for q in citadas), 'o R2 usa palavras da sessão de origem')
        espacado = [c for c in C if c.get('origem') and c.get('g') != 'recupera']
        self.assertTrue(espacado)
        for c in espacado:
            self.assertTrue((ROOT / c['origem'] / 'index.html').is_file(), c['origem'])
        self.assertIn('Rhythm 0', C[2]['p'])

    def test_caso_real_imagem_e_sem_video(self):
        C = self.D['cartoes']
        real = [c for c in C if 'Caso real' in c.get('p', '')]
        self.assertEqual(len(real), 1)
        self.assertTrue(real[0]['liga'][0]['href'].startswith('https://www.dgsi.pt/'))
        self.assertEqual(real[0]['tipo'], 'transferir')
        olha = next(c for c in C if c['rot'] == 'Olha')
        self.assertIn('CC BY 2.0', olha['html']); self.assertIn('flickr.com/photos/fdrlibrary/27758131387', olha['html'])
        self.assertIn('64-165', olha['html'])
        self.assertTrue((ROOT / 'img/cidadania/eleanor-roosevelt-dudh-1949.webp').is_file())
        self.assertNotIn('data-yt', json.dumps(self.D))
        self.assertNotIn('Na aula', [c.get('rot') for c in C])

    def test_versao_para_imprimir(self):
        s = (ROOT / 'cidadania/m1/sessoes/01/imprimir/index.html').read_text('utf-8')
        self.assertEqual(len(re.findall(r'<p class="rot">Exercício \d+:', s)), 14)
        self.assertIn('Código', s); self.assertIn('O que conta', s)
        for c in self.D['cartoes']:
            if c['t'] != 'ler':
                self.assertNotIn(html_escape(c['f'])[:60], s)  # as respostas e os retornos ficam no guia do docente
        self.assertIn('CC BY 2.0', s)  # na impressão, o crédito sai por extenso



class SessaoS02(unittest.TestCase):
    """06/11/2026 (decisão 166): a sessão 02 do M1, «A imagem dos outros», na versão final, pelo mesmo molde e com as mesmas
    exigências da s01: o contrato e o cfg, cada excerto (Código Civil, artigos 79.º e 81.º; Lei n.º 58/2019, artigo 16.º; o
    acórdão do Supremo Tribunal de Justiça de 2011) no registo, confirmado e letra a letra, o R2 com palavras da sessão de origem,
    o conceito espaçado, o caso real com fonte oficial (decisão 161), a imagem com o crédito atrás do «i» (decisão 153), nenhum
    vídeo (decisão 155) e a versão para imprimir sem respostas."""
    D = carregar(ROOT / 'tools/licoes/cidadania-m1-s02.json')
    REG = SessaoS01.REG
    norm = staticmethod(SessaoS01.norm)
    confere = SessaoS01.confere

    def test_contrato_e_cfg(self):
        self.assertEqual(self.D['molde'], L.MOLDE)
        self.assertEqual(L.validar(self.D), [])
        self.assertEqual(self.D['saida'], 'cidadania/m1/sessoes/02/index.html')
        self.assertEqual(self.D['chave'], 'epi-cid-m1-s02')
        self.assertNotEqual(self.D['versao'], '2026-10-31-2')  # a versão do piloto sobe (preservarAnterior guarda o «feita»)
        cfg = cfg_da_pagina((ROOT / self.D['saida']).read_text('utf-8'))
        for k in ('aula', 'semPontos', 'preservarAnterior'):
            self.assertIs(cfg[k], True, k)
        self.assertEqual(cfg['retomar'], 192)
        self.assertNotIn('pistas', cfg)
        C = self.D['cartoes']
        self.assertTrue(all(c.get('pista') for c in C if c['t'] != 'ler'))
        self.assertEqual(len(C), 23)
        self.assertEqual([c['rot'] for c in C if c['t'] == 'ler'],
                         ['Abre', 'Decide', 'Olha', 'Lê', 'Conceito', 'Volta ao caso', 'Em turma', 'Agora, em papel', 'Para levar'])
        # os mesmos minutos da s01, cartão a cartão (a secção 2 do plano)
        self.assertEqual([c['min'] for c in C], [c['min'] for c in SessaoS01.D['cartoes']])
        self.assertEqual(self.D['tempos'], SessaoS01.D['tempos'])
        self.assertIn('Aceitar ser filmado é aceitar ser publicado?', C[0]['html'])
        # a s01 leva à s02 nova; 06/11/2026 (decisões 166 a 168): a s02 leva à s03 nova, que também passou ao molde final
        self.assertEqual(SessaoS01.D['seguinte'], '../02/')
        self.assertEqual(self.D['seguinte'], '../03/')

    def test_cada_excerto_esta_no_registo_e_confirmado(self):
        vistos = 0
        for i, c in enumerate(self.D['cartoes'], 1):
            h = c.get('html') or ''
            for bq in re.findall(r'<blockquote class="lei">(.*?)</blockquote>', h, re.S):
                self.assertEqual(len(re.findall(r'<p\b', bq)), len(re.findall(r'<p\b[^>]*data-fonte=', bq)), f'cartão {i}')
            for tag, ident, corpo in re.findall(r'<(p|span)\b[^>]*data-fonte="([^"]+)"[^>]*>(.*?)</\1>', h, re.S):
                corpo = re.sub(r'<span class="art">.*?</span>', '', corpo)
                self.confere(ident, corpo, f'cartão {i}')
                vistos += 1
            if c.get('fonte'):
                self.confere(c['fonte'], c.get('cita') or c.get('frase'), f'cartão {i}')
                vistos += 1
            texto = self.norm(' '.join([c.get('f', '')] + (c['fe'] if isinstance(c.get('fe'), list) else [c.get('fe') or ''])
                                       + [x for par in c.get('pares', []) for x in par]))
            for ident, frase in c.get('citacoes', []):
                self.confere(ident, frase, f'cartão {i}')
                self.assertIn(self.norm(frase), texto, f'cartão {i}: a citação registada está no cartão')
                aspas = [q for q in re.findall(r'«([^«»]*)»', texto) if self.norm(frase) in q]
                self.assertTrue(aspas, f'cartão {i}: «{frase}» está entre aspas')
                for q in aspas:
                    for pedaco in re.split(r'\s*\[…\]\s*', q):
                        if pedaco.strip():
                            self.assertIn(pedaco.strip(), self.norm(self.REG[ident]['texto']), f'cartão {i}: «{q}» não é texto exato de {ident}')
                vistos += 1
        self.assertGreaterEqual(vistos, 18)  # a s02 cita 19 excertos (a s01, mais de 20)
        # os excertos que a tarefa pede: Código Civil, artigo 79.º, n.os 1 a 3, e Lei n.º 58/2019, artigo 16.º, todos do DRE
        tudo = json.dumps(self.D, ensure_ascii=False)
        # 06/11/2026: revisão da s02; o cartão 15 cita a conclusão do tribunal (stj-2011-indicacao), não o depoimento de uma das
        # partes (stj-2011-dito), e o depoimento já não pode aparecer como palavras do tribunal
        self.assertNotIn('stj-2011-dito', tudo)
        for ident in ('cc-79-1', 'cc-79-2', 'cc-79-3', 'cc-81-2', 'lei58-16-1', 'stj-2011-indicacao', 'stj-2011-iv', 'dudh-12'):
            self.assertIn(ident, tudo)
            self.assertIs(self.REG[ident]['confirmado'], True, ident)
        for ident in ('cc-79-1', 'cc-79-2', 'cc-79-3', 'cc-81-2', 'lei58-16-1', 'lei58-16-2'):
            self.assertTrue(self.REG[ident]['ligacao'].startswith('https://diariodarepublica.pt/'), ident)
        # a grafia é a da fonte (texto consolidado do Código Civil, anterior ao Acordo Ortográfico)
        self.assertIn('didácticas', self.REG['cc-79-2']['texto']); self.assertIn('pùblicamente', self.REG['cc-79-2']['texto'])
        le = next(c for c in self.D['cartoes'] if c['rot'] == 'Lê')
        self.assertIn('se do facto resultar prejuízo para a honra, reputação ou simples decoro', self.norm(L.sem_details(le['html'])))

    def test_recupera_e_conceito_espacado(self):
        C = self.D['cartoes']
        self.assertIn('The Truman Show', C[2]['p'])
        self.assertNotIn('Código Civil', C[2]['f'] + ' '.join(C[2]['fe']))  # o R1 não cita a lei antes do Lê (plano, secção 3)
        r2 = C[3]
        self.assertEqual(r2['g'], 'recupera')
        self.assertEqual(r2['origem'], 'cidadania/m1/sessoes/01/')
        origem = (ROOT / r2['origem'] / 'index.html').read_text('utf-8')
        citadas = re.findall(r'«([^»]{8,})»', r2['fe'] + ' ' + r2['f'])
        self.assertTrue(any(self.norm(q) in self.norm(origem) for q in citadas), 'o R2 usa palavras da sessão de origem')
        espacado = [c for c in C if c.get('origem') and c.get('g') != 'recupera']
        self.assertTrue(espacado)
        for c in espacado:
            self.assertTrue((ROOT / c['origem'] / 'index.html').is_file(), c['origem'])

    def test_caso_real_imagem_e_sem_video(self):
        C = self.D['cartoes']
        real = [c for c in C if 'Caso real' in c.get('p', '')]
        self.assertEqual(len(real), 1)
        self.assertTrue(real[0]['liga'][0]['href'].startswith('https://www.dgsi.pt/'))
        self.assertEqual(real[0]['liga'][0]['href'], self.REG['stj-2011-indicacao']['ligacao'])  # 06/11/2026: revisão da s02
        self.assertEqual(real[0]['fonte'], 'stj-2011-indicacao')
        self.assertEqual(real[0]['tipo'], 'transferir')
        self.assertIn('o do Supremo Tribunal de Justiça é real', self.D['fontes'])
        olha = next(c for c in C if c['rot'] == 'Olha')
        self.assertIn('hine-addie-card-1910.webp', olha['html'])
        self.assertIn('https://www.loc.gov/item/2018675335/', olha['html'])
        self.assertIn('Domínio público', olha['html'])
        # 06/11/2026: revisão da s02; o «i» diz o número de reprodução usado e o que o registo diz, entre aspas
        self.assertIn('LC-DIG-nclc-05282', olha['html'])
        self.assertIn('«No known restrictions on publication»', olha['html'])
        self.assertTrue((ROOT / 'img/cidadania/hine-addie-card-1910.webp').is_file())
        self.assertNotIn('data-yt', json.dumps(self.D))
        self.assertNotIn('Na aula', [c.get('rot') for c in C])
        # decisão 146: «grupo» só no caso inventado ou como «grupo da turma» (o validador também o confere)
        self.assertNotRegex(json.dumps([c for c in C if c['t'] != 'ler'], ensure_ascii=False), r'(?i)\bgrupos?\b(?! da turma)')

    def test_versao_para_imprimir(self):
        s = (ROOT / 'cidadania/m1/sessoes/02/imprimir/index.html').read_text('utf-8')
        self.assertEqual(len(re.findall(r'<p class="rot">Exercício \d+:', s)), 14)
        self.assertIn('Código', s); self.assertIn('O que conta', s)
        for c in self.D['cartoes']:
            if c['t'] != 'ler':
                self.assertNotIn(html_escape(c['f'])[:60], s)
        self.assertIn('Domínio público', s)
        self.assertIn('https://www.loc.gov/item/2018675335/', s)
        # 06/11/2026: revisão da s02; em papel não se toca em nada, e as referências não se partem (decisão 152)
        self.assertNotRegex(s, r'(?i)\btoca\b')
        self.assertIn('n.º\u00a01', s)
        self.assertIn('13\u00a0anos', s)



class SessaoS03(unittest.TestCase):
    """06/11/2026 (decisões 166 a 168): a sessão 03 do M1, «Quem tem lugar?», na versão final, pelo mesmo molde e com as mesmas
    exigências da s01 e da s02: o contrato e o cfg, cada excerto (Constituição, artigos 13.º, 18.º e 71.º; Convenção sobre os Direitos
    da Criança, artigos 1.º e 23.º; Lei n.º 46/2006, artigo 3.º) no registo, confirmado e letra a letra, o R2 com palavras da sessão de
    origem, o conceito espaçado, o caso real com fonte oficial (decisão 161: o acórdão do Tribunal Europeu dos Direitos Humanos no
    HUDOC, contado sem citação porque não há texto português), a imagem com o crédito atrás do «i» (decisão 153), nenhum vídeo
    (decisão 155) e a versão para imprimir sem respostas."""
    D = carregar(ROOT / 'tools/licoes/cidadania-m1-s03.json')
    REG = SessaoS01.REG
    norm = staticmethod(SessaoS01.norm)
    confere = SessaoS01.confere

    def test_contrato_e_cfg(self):
        self.assertEqual(self.D['molde'], L.MOLDE)
        self.assertEqual(L.validar(self.D), [])
        self.assertEqual(self.D['saida'], 'cidadania/m1/sessoes/03/index.html')
        self.assertEqual(self.D['chave'], 'epi-cid-m1-s03')
        self.assertNotEqual(self.D['versao'], '2026-10-31-2')  # a versão do piloto sobe (preservarAnterior guarda o «feita»)
        cfg = cfg_da_pagina((ROOT / self.D['saida']).read_text('utf-8'))
        for k in ('aula', 'semPontos', 'preservarAnterior'):
            self.assertIs(cfg[k], True, k)
        self.assertEqual(cfg['retomar'], 192)
        self.assertNotIn('pistas', cfg)
        C = self.D['cartoes']
        self.assertTrue(all(c.get('pista') for c in C if c['t'] != 'ler'))
        self.assertEqual(len(C), 23)
        self.assertEqual([c['rot'] for c in C if c['t'] == 'ler'],
                         ['Abre', 'Decide', 'Olha', 'Lê', 'Conceito', 'Volta ao caso', 'Em turma', 'Agora, em papel', 'Para levar'])
        # os mesmos minutos da s01, cartão a cartão (a secção 2 do plano)
        self.assertEqual([c['min'] for c in C], [c['min'] for c in SessaoS01.D['cartoes']])
        self.assertEqual(self.D['tempos'], SessaoS01.D['tempos'])
        self.assertIn('Uma regra igual para todos pode deixar alguém de fora?', C[0]['html'])
        self.assertEqual(self.D['seguinte'], '../../../piloto/m1-s04/')
        # cada retorno até 45 palavras (molde, secção 2)
        for i, c in enumerate(C, 1):
            if c['t'] == 'ler':
                continue
            for x in [c['f']] + (c['fe'] if isinstance(c['fe'], list) else [c['fe']]):
                self.assertLessEqual(len(L.visivel(x).split()), 45, f'cartão {i}')

    def test_cada_excerto_esta_no_registo_e_confirmado(self):
        vistos = 0
        for i, c in enumerate(self.D['cartoes'], 1):
            h = c.get('html') or ''
            for bq in re.findall(r'<blockquote class="lei">(.*?)</blockquote>', h, re.S):
                self.assertEqual(len(re.findall(r'<p\b', bq)), len(re.findall(r'<p\b[^>]*data-fonte=', bq)), f'cartão {i}')
            for tag, ident, corpo in re.findall(r'<(p|span)\b[^>]*data-fonte="([^"]+)"[^>]*>(.*?)</\1>', h, re.S):
                corpo = re.sub(r'<span class="art">.*?</span>', '', corpo)
                self.confere(ident, corpo, f'cartão {i}')
                vistos += 1
            if c.get('fonte'):
                self.confere(c['fonte'], c.get('cita') or c.get('frase'), f'cartão {i}')
                vistos += 1
            texto = self.norm(' '.join([c.get('f', '')] + (c['fe'] if isinstance(c.get('fe'), list) else [c.get('fe') or ''])
                                       + [x for par in c.get('pares', []) for x in par]))
            for ident, frase in c.get('citacoes', []):
                self.confere(ident, frase, f'cartão {i}')
                self.assertIn(self.norm(frase), texto, f'cartão {i}: a citação registada está no cartão')
                aspas = [q for q in re.findall(r'«([^«»]*)»', texto) if self.norm(frase) in q]
                self.assertTrue(aspas, f'cartão {i}: «{frase}» está entre aspas')
                for q in aspas:
                    for pedaco in re.split(r'\s*\[…\]\s*', q):
                        if pedaco.strip():
                            self.assertIn(pedaco.strip(), self.norm(self.REG[ident]['texto']), f'cartão {i}: «{q}» não é texto exato de {ident}')
                vistos += 1
        self.assertGreaterEqual(vistos, 18)
        # os excertos que a tarefa pede: Constituição, artigo 13.º, n.º 2; Convenção, artigo 23.º; todos do Diário da República
        tudo = json.dumps(self.D, ensure_ascii=False)
        for ident in ('crp-13-1', 'crp-13-2', 'crp-18-1', 'crp-71-1', 'cdc-1', 'cdc-23-1', 'lei46-3b'):
            self.assertIn(ident, tudo)
            self.assertIs(self.REG[ident]['confirmado'], True, ident)
            self.assertTrue(self.REG[ident]['ligacao'].startswith('https://diariodarepublica.pt/'), ident)
        # a grafia é a da fonte (a tradução de 1990 e o texto consolidado, anteriores ao Acordo Ortográfico)
        self.assertIn('participação activa', self.REG['cdc-23-1']['texto'])
        self.assertIn('Discriminação indirecta', self.REG['lei46-3b']['texto'])
        le = next(c for c in self.D['cartoes'] if c['rot'] == 'Lê')
        vista = self.norm(L.sem_details(le['html']))
        self.assertIn('prejudicado, privado de qualquer direito', vista)
        self.assertIn('facilitem a sua participação activa na vida da comunidade.', vista)
        # o sublinhar é o artigo 13.º, n.º 2, inteiro, e as palavras certas dizem uma perda
        sub = next(c for c in self.D['cartoes'] if c['t'] == 'sublinhar')
        self.assertEqual(sub['frase'], self.REG['crp-13-2']['texto'])
        self.assertEqual([sub['frase'].split()[j].strip(',') for j in sub['certas']], ['prejudicado', 'privado'])

    def test_recupera_e_conceito_espacado(self):
        C = self.D['cartoes']
        self.assertIn('The Egg', C[2]['p'])
        r2 = C[3]
        self.assertEqual(r2['g'], 'recupera')
        self.assertEqual(r2['origem'], 'cidadania/m1/sessoes/01/')
        origem = (ROOT / r2['origem'] / 'index.html').read_text('utf-8')
        citadas = re.findall(r'«([^»]{8,})»', r2['fe'] + ' ' + r2['f'])
        self.assertTrue(any(self.norm(q) in self.norm(origem) for q in citadas), 'o R2 usa palavras da sessão de origem')
        espacado = [c for c in C if c.get('origem') and c.get('g') != 'recupera']
        self.assertTrue(espacado)
        for c in espacado:
            self.assertTrue((ROOT / c['origem'] / 'index.html').is_file(), c['origem'])
        # duas charneiras: a 1 no cartão 12 (ver não é participar), a 2 no cartão 21 (a conclusão que não vai além das provas)
        self.assertEqual((C[11]['t'], C[11]['v']), ('vf', False))
        self.assertEqual(C[20]['t'], 'escolha')

    def test_caso_real_imagem_e_sem_video(self):
        C = self.D['cartoes']
        real = [c for c in C if 'Caso real' in c.get('p', '')]
        self.assertEqual(len(real), 1)
        self.assertEqual(real[0]['liga'][0]['href'], 'https://hudoc.echr.coe.int/eng?i=001-180499')
        self.assertEqual(real[0]['tipo'], 'transferir')
        self.assertNotIn('cita', real[0])  # não há texto português do acórdão: conta-se, não se cita
        self.assertIn('o do Tribunal Europeu dos Direitos Humanos é real', self.D['fontes'])
        olha = next(c for c in C if c['rot'] == 'Olha')
        self.assertIn('bubley-sala-de-espera-1943.webp', olha['html'])
        # 06/11/2026 (revisão da s03): o «Registo de origem» é o handle da Library of Congress do registo cph.3b22541, o que o
        # crédito nomeia. 06/11/2026 (confirmação): o handle resolve para o registo 2017862110 (o mesmo que loc.gov/item/2017862110;
        # reproduções LC-DIG-fsa-8d33365 e LC-USZ62-75338); o crédito liga pelo handle, o número que nomeia
        self.assertIn('https://hdl.loc.gov/loc.pnp/cph.3b22541', olha['html'])
        self.assertNotIn('loc.gov/item/2017862110', olha['html'])
        self.assertIn('https://commons.wikimedia.org/wiki/File:1943_Colored_Waiting_Room_Sign.jpg', olha['html'])
        self.assertIn('Domínio público', olha['html'])
        self.assertTrue((ROOT / 'img/cidadania/bubley-sala-de-espera-1943.webp').is_file())
        self.assertNotIn('data-yt', json.dumps(self.D))
        self.assertNotIn('Na aula', [c.get('rot') for c in C])
        # decisão 146: «grupo» só no caso inventado ou como «grupo da turma» (o validador também o confere)
        self.assertNotRegex(json.dumps([c for c in C if c['t'] != 'ler'], ensure_ascii=False), r'(?i)\bgrupos?\b(?! da turma)')

    def test_versao_para_imprimir(self):
        s = (ROOT / 'cidadania/m1/sessoes/03/imprimir/index.html').read_text('utf-8')
        self.assertEqual(len(re.findall(r'<p class="rot">Exercício \d+:', s)), 14)
        self.assertIn('Código', s); self.assertIn('O que conta', s)
        for c in self.D['cartoes']:
            if c['t'] != 'ler':
                self.assertNotIn(html_escape(c['f'])[:60], s)
        self.assertIn('Domínio público', s)
        # 06/11/2026 (revisão da s03): o handle do registo cph.3b22541 (ver test_caso_real_imagem_e_sem_video)
        self.assertIn('https://hdl.loc.gov/loc.pnp/cph.3b22541', s)


class SessaoS08(unittest.TestCase):
    """06/11/2026 (decisões 166 a 168): a sessão 08 do M1, «Quem decide o quê?», na versão final, pelo mesmo molde e com as mesmas
    exigências da s01 a s03, feita fora de ordem: o contrato e o cfg, cada excerto (Constituição, artigos 23.º, 52.º, 161.º, 182.º e
    202.º; Lei n.º 43/90, artigos 2.º, 8.º e 9.º; o boletim do Provedor de Justiça de 2016) no registo, confirmado e letra a letra, o R2
    com palavras da sessão de origem, o conceito espaçado, as duas charneiras (a 2 pede a conclusão que vai além das provas, o apoio
    que se retira nas sessões 08 a 10), o caso real com fonte oficial (decisão 161), a fotografia com o crédito atrás do «i» (decisão
    153), nenhum vídeo (decisão 155) e a versão para imprimir sem respostas."""
    D = carregar(ROOT / 'tools/licoes/cidadania-m1-s08.json')
    REG = SessaoS01.REG
    norm = staticmethod(SessaoS01.norm)
    confere = SessaoS01.confere

    def test_contrato_e_cfg(self):
        self.assertEqual(self.D['molde'], L.MOLDE)
        self.assertEqual(L.validar(self.D), [])
        self.assertEqual(self.D['saida'], 'cidadania/m1/sessoes/08/index.html')
        self.assertEqual(self.D['chave'], 'epi-cid-m1-s08')
        self.assertNotEqual(self.D['versao'], '2026-10-31-2')  # a versão do piloto sobe (preservarAnterior guarda o «feita»)
        cfg = cfg_da_pagina((ROOT / self.D['saida']).read_text('utf-8'))
        for k in ('aula', 'semPontos', 'preservarAnterior'):
            self.assertIs(cfg[k], True, k)
        self.assertEqual(cfg['retomar'], 192)
        self.assertNotIn('pistas', cfg)
        C = self.D['cartoes']
        self.assertTrue(all(c.get('pista') for c in C if c['t'] != 'ler'))
        self.assertEqual(len(C), 23)
        self.assertEqual([c['rot'] for c in C if c['t'] == 'ler'],
                         ['Abre', 'Decide', 'Olha', 'Lê', 'Conceito', 'Volta ao caso', 'Em turma', 'Agora, em papel', 'Para levar'])
        # os mesmos minutos da s01, cartão a cartão (a secção 2 do plano)
        self.assertEqual([c['min'] for c in C], [c['min'] for c in SessaoS01.D['cartoes']])
        self.assertEqual(self.D['tempos'], SessaoS01.D['tempos'])
        self.assertIn('A quem se pede, e com que fundamento?', C[0]['html'])
        self.assertEqual(self.D['seguinte'], '../../../piloto/m1-s09/')
        # cada retorno até 45 palavras e cada enunciado até 30 (molde, secção 2)
        for i, c in enumerate(C, 1):
            if c['t'] == 'ler':
                continue
            for x in [c['f']] + (c['fe'] if isinstance(c['fe'], list) else [c['fe']]):
                self.assertLessEqual(len(L.visivel(x).split()), 45, f'cartão {i}')
            self.assertLessEqual(len(L.visivel(c['p']).split()), 30, f'cartão {i}')

    def test_cada_excerto_esta_no_registo_e_confirmado(self):
        vistos = 0
        for i, c in enumerate(self.D['cartoes'], 1):
            h = c.get('html') or ''
            for bq in re.findall(r'<blockquote class="lei">(.*?)</blockquote>', h, re.S):
                self.assertEqual(len(re.findall(r'<p\b', bq)), len(re.findall(r'<p\b[^>]*data-fonte=', bq)), f'cartão {i}')
            for tag, ident, corpo in re.findall(r'<(p|span)\b[^>]*data-fonte="([^"]+)"[^>]*>(.*?)</\1>', h, re.S):
                corpo = re.sub(r'<span class="art">.*?</span>', '', corpo)
                self.confere(ident, corpo, f'cartão {i}')
                vistos += 1
            if c.get('fonte'):
                texto = c.get('cita') or c.get('frase')
                if isinstance(c['fonte'], list):
                    # uma citação com passagens de várias entradas: cada pedaço confere-se com a sua, pela ordem
                    pedacos = re.split(r'\s*\[…\]\s*', texto)
                    self.assertEqual(len(pedacos), len(c['fonte']), f'cartão {i}')
                    for ident, pedaco in zip(c['fonte'], pedacos):
                        self.confere(ident, pedaco, f'cartão {i}')
                else:
                    self.confere(c['fonte'], texto, f'cartão {i}')
                vistos += 1
            texto = self.norm(' '.join([c.get('f', '')] + (c['fe'] if isinstance(c.get('fe'), list) else [c.get('fe') or ''])
                                       + [x for par in c.get('pares', []) for x in par]))
            for ident, frase in c.get('citacoes', []):
                self.confere(ident, frase, f'cartão {i}')
                self.assertIn(self.norm(frase), texto, f'cartão {i}: a citação registada está no cartão')
                aspas = [q for q in re.findall(r'«([^«»]*)»', texto) if self.norm(frase) in q]
                self.assertTrue(aspas, f'cartão {i}: «{frase}» está entre aspas')
                for q in aspas:
                    for pedaco in re.split(r'\s*\[…\]\s*', q):
                        if pedaco.strip():
                            self.assertIn(pedaco.strip(), self.norm(self.REG[ident]['texto']), f'cartão {i}: «{q}» não é texto exato de {ident}')
                vistos += 1
        self.assertGreaterEqual(vistos, 20)
        tudo = json.dumps(self.D, ensure_ascii=False)
        # a Constituição e a Lei n.º 43/90 vêm do Diário da República; o caso real, do sítio do Provedor de Justiça
        for ident in ('crp-23-1', 'crp-52-1', 'crp-161', 'crp-161-c', 'crp-182', 'crp-202-1', 'lei43-2-3', 'lei43-8-1', 'lei43-9-5',
                      'lei43-9-5b'):
            self.assertIn(ident, tudo)
            self.assertIs(self.REG[ident]['confirmado'], True, ident)
            self.assertTrue(self.REG[ident]['ligacao'].startswith('https://diariodarepublica.pt/'), ident)
        self.assertIs(self.REG['prov-2016-pdm']['confirmado'], True)
        self.assertTrue(self.REG['prov-2016-pdm']['ligacao'].startswith('https://provedor-jus.pt/'))
        # a grafia é a da fonte (o texto consolidado, anterior ao Acordo Ortográfico)
        self.assertIn('colectivamente', self.REG['crp-52-1']['texto'])
        le = next(c for c in self.D['cartoes'] if c['rot'] == 'Lê')
        vista = self.norm(L.sem_details(le['html']))
        self.assertIn('para defesa dos seus direitos, da Constituição, das leis ou do interesse geral', vista)
        self.assertIn('que as apreciará sem poder decisório', vista)
        # o sublinhar do Lê é o artigo 52.º, n.º 1, inteiro, e as palavras certas dizem em defesa de quê se pede
        sub = [c for c in self.D['cartoes'] if c['t'] == 'sublinhar' and c.get('fonte')]
        self.assertEqual(len(sub), 1)
        self.assertEqual(sub[0]['frase'], self.REG['crp-52-1']['texto'])
        self.assertEqual([sub[0]['frase'].split()[j].strip(',') for j in sub[0]['certas']],
                         ['direitos', 'Constituição', 'leis', 'interesse', 'geral'])

    def test_recupera_e_conceito_espacado(self):
        C = self.D['cartoes']
        # R1 (sem obra): a marca da conclusão da sessão 07
        self.assertEqual((C[2]['t'], C[2]['g']), ('sublinhar', 'recupera'))
        self.assertEqual([C[2]['frase'].split()[j].strip(',') for j in C[2]['certas']], ['por', 'isso'])
        self.assertNotIn('por isso', C[2]['pista'])
        r2 = C[3]
        self.assertEqual(r2['g'], 'recupera')
        self.assertEqual(r2['origem'], 'cidadania/m1/sessoes/05/')
        self.assertTrue((ROOT / r2['origem'] / 'index.html').is_file())
        # o R2 usa palavras da sessão de origem. Confere-se na fonte da sessão 05 (tools/licoes/cidadania-m1-s05.json): a página
        # publicada em cidadania/m1/sessoes/05/ é ainda a do percurso anterior, com outro tema; «finalidade» está na s05 do piloto e na
        # do molde (ramo claude/cidadania-m1-s05-20261106).
        origem = json.dumps(carregar(ROOT / 'tools/licoes/cidadania-m1-s05.json'), ensure_ascii=False)
        citadas = re.findall(r'«([^»]{8,})»', ' '.join([r2['f']] + [x for x in r2['fe'] if x]))
        self.assertTrue(any(self.norm(q) in self.norm(origem) for q in citadas), 'o R2 usa palavras da sessão de origem')
        espacado = [c for c in C if c.get('origem') and c.get('g') != 'recupera']
        self.assertEqual([c['origem'] for c in espacado], ['cidadania/m1/sessoes/04/'])
        for c in espacado:
            self.assertTrue((ROOT / c['origem'] / 'index.html').is_file(), c['origem'])
        # duas charneiras: a 1 no cartão 12 (recomendar não é decidir), a 2 no cartão 21 (a conclusão que vai além das provas)
        self.assertEqual((C[11]['t'], C[11]['v']), ('vf', False))
        self.assertEqual(C[20]['t'], 'escolha')
        self.assertIn('vai além', C[20]['p'])
        certa = C[20]['o'][C[20]['c']]
        self.assertIn('sem ouvir ninguém', certa)
        # nenhum cartão antes da charneira 2 escreve a sua resposta (a consulta que ninguém provou)
        for c in C[:20]:
            self.assertNotIn('ouvir ninguém', json.dumps(c, ensure_ascii=False))

    def test_caso_real_imagem_e_sem_video(self):
        C = self.D['cartoes']
        real = [c for c in C if 'Caso real' in c.get('p', '')]
        self.assertEqual(len(real), 1)
        self.assertEqual(real[0]['liga'][0]['href'], self.REG['prov-2016-pdm']['ligacao'])
        self.assertEqual(real[0]['tipo'], 'transferir')
        self.assertIn('o do Provedor de Justiça é real', self.D['fontes'])
        olha = next(c for c in C if c['rot'] == 'Olha')
        self.assertIn('kilburn-cartistas-1848.webp', olha['html'])
        self.assertIn('RCIN 2932484', olha['html'])
        self.assertIn('https://commons.wikimedia.org/wiki/File:William_Edward_Kilburn_-_View_of_the_Great_Chartist_Meeting_on_'
                      'Kennington_Common_-_Google_Art_Project.jpg', olha['html'])
        self.assertIn('Domínio público', olha['html'])
        # o registo da Royal Collection não abriu: a legenda não liga o comício à petição cartista (plano, secção 6)
        self.assertNotIn('petição', re.search(r'<figcaption>(.*?)</figcaption>', olha['html']).group(1))
        self.assertTrue((ROOT / 'img/cidadania/kilburn-cartistas-1848.webp').is_file())
        self.assertNotIn('data-yt', json.dumps(self.D))
        self.assertNotIn('Na aula', [c.get('rot') for c in C])
        # decisão 146: «grupo» só no caso inventado ou como «grupo da turma» (o validador também o confere)
        self.assertNotRegex(json.dumps([c for c in C if c['t'] != 'ler'], ensure_ascii=False), r'(?i)\bgrupos?\b(?! da turma)')

    def test_versao_para_imprimir(self):
        s = (ROOT / 'cidadania/m1/sessoes/08/imprimir/index.html').read_text('utf-8')
        self.assertEqual(len(re.findall(r'<p class="rot">Exercício \d+:', s)), 14)
        self.assertIn('Código', s); self.assertIn('O que conta', s)
        for c in self.D['cartoes']:
            if c['t'] != 'ler':
                self.assertNotIn(html_escape(c['f'])[:60], s)
        self.assertIn('Domínio público', s)
        self.assertIn('RCIN\u00a02932484', s.replace('RCIN 2932484', 'RCIN\u00a02932484'))


if __name__ == '__main__':
    unittest.main()
