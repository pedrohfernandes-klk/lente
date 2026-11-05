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

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('licoes_lente', ROOT / 'tools/licoes_lente.py')
L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
sys.path.insert(0, str(ROOT / 'tests' / 'fixtures'))
import molde_ensaio as E  # noqa: E402

FONTES = sorted((ROOT / 'tools/licoes').glob('*.json'))
CIDADANIA = [p for p in FONTES if p.name.startswith('cidadania-')]


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
        # o Laboratório fica como estava
        self.assertEqual(L.FAMILIAS['laboratorio']['cfg'], {'semPontos': True, 'preservarAnterior': True})

    def test_as_dez_sessoes_do_piloto_levam_o_cfg_e_o_progresso_comum(self):
        self.assertEqual(len(CIDADANIA), 10)
        for p in CIDADANIA:
            d = carregar(p)
            s = (ROOT / d['saida']).read_text('utf-8')
            cfg = cfg_da_pagina(s)
            for k, v in L.FAMILIAS['cidadania']['cfg'].items():
                self.assertEqual(cfg.get(k), v, p.name + ': ' + k)
            self.assertIs(cfg['variar'], False)
            self.assertEqual(s.count(L.FIM_CIDADANIA), 1, p.name)
            prog = s.index('assets/licoes/' + L.PROGRESSO)
            self.assertLess(prog, s.index('assets/licoes/jogo.js'), p.name)
            # sem molde, nenhuma peça nova entra na página
            for f in ('assets/licoes/aula-clara', 'assets/licoes/casca-pc', 'assets/licoes/ampliar-documentos', 'assets/licoes/recolha',
                      'assets/info-i', ' molde-cidadania', 'EPIRecolha'):
                self.assertNotIn(f, s, p.name + ': ' + f)

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
        for p in FONTES:
            d = carregar(p)
            self.assertNotIn('molde', d, p.name)
            self.assertEqual(L.validar(d), [], p.name)

    def test_com_molde_o_contrato_aplica_se(self):
        d = carregar(CIDADANIA[0])
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
        self.assertIn(f'<a href="{L.COMO_LENTE}">Como se faz (vídeos)</a>', s)
        self.assertIn('EPIRecolha.ligar({"chave": "epi-cid-m1-artefactos", "sessao": "epi-cid-m1-s99"', s)
        self.assertLess(s.index('EPIRecolha.ligar('), s.index('EPIJogo.montar(CFG)'))
        cfg = cfg_da_pagina(s)
        self.assertEqual(cfg['pistas'], d['pistas'])
        self.assertEqual(cfg['depois'], d['depois'])

    def test_css_da_cidadania_so_no_molde(self):
        css = self.ler('assets/licoes/cidadania.css')
        bloco = css.split('/* ==== molde cidadania-2026-11 ==== */', 1)[1]
        self.assertIn('--cid:#1f4e79', bloco); self.assertIn('--cid:#9cc1e8', bloco)
        self.assertIn('var(--cartaz', bloco)                    # títulos e frase do Para levar em letra de cartaz
        self.assertIn('@media (min-width:1100px)', bloco)       # o Olha acima de 1100 px
        self.assertIn('html.em-projecao body.molde-cidadania', bloco)
        self.assertNotRegex(bloco, r'c-barra')                  # o azul nunca entra na barra


if __name__ == '__main__':
    unittest.main()
