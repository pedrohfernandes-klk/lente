"""31/10/2026: Cidadania refeita, M1 em piloto (decisões do docente de 30/10: segunda ronda, 5, 8, 17, 18 e 38).
A página do módulo, o guia do docente e o Ponto de partida e de chegada saem de tools/cidadania_piloto.py, a partir das
lições em tools/licoes/cidadania-m1-sNN.json. Confirma que a página do módulo lista as 10 sessões, que as ligações
locais resolvem, que as três páginas estão escondidas dos motores de busca e que o guia diz que a avaliação é
indicativa."""
import html, importlib.util, json, math, pathlib, re, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cidadania_piloto', ROOT / 'tools/cidadania_piloto.py')
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
MOD = ROOT / 'cidadania/piloto/m1/index.html'
GUIA = ROOT / 'cidadania/piloto/m1/docente/index.html'
PONTO = ROOT / 'cidadania/piloto/m1/ponto/index.html'


def ler(p):
    return p.read_text('utf-8')


def ligacoes_locais(p):
    s = re.sub(r'<script\b.*?</script>', '', ler(p), flags=re.S)
    for h in re.findall(r'(?:href|src)="([^"]+)"', s):
        h = html.unescape(h)
        if h.startswith(('http:', 'https:', '//', 'mailto:', '#')):
            continue
        yield h


class CidadaniaPiloto(unittest.TestCase):
    def test_paginas_atualizadas_e_com_as_regras_da_casa(self):
        for rel, s in G.paginas().items():
            self.assertEqual(G.regras(rel, s), [], rel)
            self.assertEqual((ROOT / rel).read_text('utf-8'), s, rel + ': corre python3 tools/cidadania_piloto.py')

    def test_escondidas_dos_motores_de_busca(self):
        for p in (MOD, GUIA, PONTO):
            self.assertEqual(ler(p).count('<meta name="robots" content="noindex, nofollow">'), 1, p)
            self.assertIn('<html lang="pt-PT" data-appearance-site="lente">', ler(p))

    def test_modulo_lista_as_10_sessoes_por_ordem(self):
        s = ler(MOD)
        chaves = re.findall(r'data-chave="(epi-cid-m1-s\d\d)"', s)
        self.assertEqual(chaves, [f'epi-cid-m1-s{n:02d}' for n in range(1, 11)])
        # 05/11/2026 (plano do molde, pedido 2): uma sessão no molde final vive no endereço que a turma já usa
        # (cidadania/m1/sessoes/NN/; a s01 primeiro) e tem a pergunta no Abre em .pergunta-sessao; as do piloto continuam em
        # ../m1-sNN/ com .pergunta-c. Exige-se, para cada sessão, a ligação exata à pasta da sua página.
        hrefs = re.findall(r'<li data-chave="epi-cid-m1-s\d\d"[^>]*><a href="([^"]+)">', s)
        self.assertEqual(len(hrefs), 10)
        for n in range(1, 11):
            d = json.loads(ler(ROOT / f'tools/licoes/cidadania-m1-s{n:02d}.json'))
            # 06/11/2026 (decisão 166): com a s02 no molde, a ligação de cada sessão no molde é a da sua própria pasta
            # (cidadania/m1/sessoes/NN/); antes, a única sessão no molde era a 01 e o endereço vinha escrito por extenso.
            self.assertEqual(hrefs[n - 1], f'../../m1/sessoes/{n:02d}/' if d.get('molde') else f'../m1-s{n:02d}/', n)
            if d.get('molde'):
                self.assertEqual(d['saida'], f'cidadania/m1/sessoes/{n:02d}/index.html')
            self.assertIn(f'data-chave="{d["chave"]}" data-versao="{d["versao"]}"', s)  # a versão decide se conta como feita
            self.assertIn(html.escape(d['titulo'].split(': ', 1)[1]), s)
            self.assertIn(re.search(r'<p class="pergunta-sessao"[^>]*>(.*?)</p>' if d.get('molde') else r'<p class="pergunta-c">(.*?)</p>',
                                    d['cartoes'][0]['html']).group(1), s)
            self.assertEqual(d['modulo']['url'], G.LENTE + 'cidadania/piloto/m1/', 'a lição volta à página do módulo piloto')
        # só as sessões: o estado escreve-se por extenso (legível sem cor), Começar ou Continuar, e o guia do docente
        # 30/10/2026: revisão do diretor de arte (sistema «Cartaz»): «por fazer» nunca se escreve; o estado começa vazio e o
        # script escreve «Feita dd/mm» (a partir de st.t) ou «A seguir» (a próxima por fazer, com a classe seguir).
        self.assertEqual(s.count('data-estado></span>'), 10)
        self.assertNotIn('por fazer', re.sub(r'<script\b.*?</script>', '', s, flags=re.S))
        self.assertIn('"Feita"', s); self.assertIn('li.classList.add("seguir")', s); self.assertIn('"A seguir"', s)
        self.assertIn('<section class="proximo"', s)
        # 05/11/2026 (pedido 2): a sessão 01 já está no molde final, em cidadania/m1/sessoes/01/.
        self.assertIn('data-continuar href="../../m1/sessoes/01/">Começar: Sessão 01', s)
        self.assertIn('"Continuar: Sessão "', s)
        self.assertIn('<a href="docente/">Guia do docente</a>', s)
        self.assertNotIn('<img', s)
        # o formato que o motor grava: «lida» no fim e «versao» da lição (assets/licoes/jogo.js)
        motor = ler(ROOT / 'assets/licoes/jogo.js')
        self.assertIn('st.lida=true', motor); self.assertIn('st.versao!==cfg.versao', motor)
        # 05/11/2026: plano do molde da Cidadania, pedido 1. «Feita» deixa de exigir a versão igual à da página (subir a versão
        # apagava o «feita» de todos) e passa a contar com feita(st) do progresso comum (assets/licoes/progresso-licoes.js): a
        # conclusão desta versão, ou de uma anterior que o motor guarda em «antes» com preservarAnterior. Exige-se o progresso
        # comum carregado antes do script, a contagem por feita(st), a data da primeira conclusão, o motor a migrar com o
        # progresso comum e nada lido na projeção. tests/browser_licoes_lente.cjs prova-o com um estado antigo semeado.
        self.assertIn('<script src="../../../assets/licoes/progresso-licoes.js?v=', s)
        self.assertLess(s.index('assets/licoes/progresso-licoes.js'), s.index('var P=window.EPILicoesProgresso'))
        self.assertIn('var ok=!!(st&&P&&P.feita(st))', s)
        self.assertIn('var t=P.data(st)', s)
        self.assertIn('st=proj?null:JSON.parse(localStorage.getItem(li.getAttribute("data-chave"))', s)
        self.assertIn('PROG.migrar(st,cfg.versao)', motor)
        self.assertNotIn('st.versao===li.getAttribute', s)

    def test_ligacoes_locais_resolvem(self):
        for p in (MOD, GUIA, PONTO):
            for h in ligacoes_locais(p):
                alvo = (p.parent / h.split('#')[0].split('?')[0]).resolve()
                if h.split('#')[0].split('?')[0].endswith('/') or alvo.is_dir():
                    alvo = alvo / 'index.html'
                self.assertTrue(alvo.is_file(), f'{p.relative_to(ROOT)}: {h}')
                if '#' in h and alvo.suffix == '.html':
                    ancora = h.split('#', 1)[1]
                    self.assertIn(f'id="{ancora}"', ler(alvo), f'{p.relative_to(ROOT)}: {h}')

    def test_guia_uma_secao_por_sessao_com_grelha_indicativa(self):
        s = ler(GUIA)
        self.assertEqual(re.findall(r'<section class="sessao" id="s(\d\d)">', s), [f'{n:02d}' for n in range(1, 11)])
        self.assertGreaterEqual(s.count('Avaliação indicativa'), 11)  # no início e em cada sessão (decisão 17)
        self.assertEqual(s.count('<td class="num">20</td></tr></tfoot>'), 10)
        for n, g in G.GUIA.items():
            self.assertEqual(sum(p for _, p in g['grelha']), 20, n)
            # 05/11/2026 (plano do molde, pedido 2): uma sessão no molde final não tem «Na aula» de 60 a 75 minutos; tem a tabela
            # dos tempos cartão a cartão, que tem de somar 175 a 185 minutos, com a pausa e o passo do projeto.
            if g.get('molde'):
                d = json.loads(ler(ROOT / f'tools/licoes/cidadania-m1-s{n}.json'))
                self.assertTrue(175 <= sum(c['min'] for c in d['cartoes']) + sum(d['tempos'].values()) <= 185, n)
                self.assertIn(f'<section class="sessao" id="s{n}"><p class="marca">Sessão {n}, no molde final</p>', s)
                self.assertIn('<table class="tempos">', s); self.assertIn('As duas charneiras', s); self.assertIn('Se só houver 90 minutos', s)
                continue
            self.assertTrue(60 <= sum(m for m, _ in g['passos']) <= 75, n)
            self.assertIn('../../../projeto/', s)
        self.assertEqual(s.count('<h3>Pergunta Humana: '), 10)
        self.assertIn('href="../ponto/"', s)

    def test_ponto_as_mesmas_10_perguntas_sem_chave(self):
        p, g = ler(PONTO), ler(GUIA)
        self.assertEqual(len(G.PONTO), 10)
        self.assertEqual(len(re.findall(r'<div class="q"><p><b>\d+\.</b>', p)), 10)
        for _, q, ops, c in G.PONTO:
            self.assertIn(html.escape(q), p); self.assertIn(html.escape(q), g)
            if ops:
                self.assertTrue(2 <= len(ops) <= 4)
                self.assertIn(html.escape(ops[c]), g)
        self.assertNotIn('Chave', p)  # a chave e a cotação ficam no guia do docente
        self.assertIn('O teu código', p)

    def test_ponto_opcoes_equilibradas(self):
        # 30/10/2026: verificação final da Cidadania refeita (M1, 31/10): nenhuma ferramenta media o Ponto de partida e de
        # chegada (PONTO não está numa página com JSON). Mede-se aqui com a função de tools/medir_opcoes.py (escolha e
        # resumir), com as regras de tests/test_opcoes_equilibradas.py: no máximo 20 % de amplitude em cada pergunta,
        # nenhuma certa denunciadora, e a certa a mais longa (ou a mais curta) no máximo tantas vezes quanto o acaso daria
        # (3 em 8, com três opções).
        spec_m = importlib.util.spec_from_file_location('medir_opcoes', ROOT / 'tools/medir_opcoes.py')
        M = importlib.util.module_from_spec(spec_m); spec_m.loader.exec_module(M)
        rows = []
        for i, (_, q, ops, c) in enumerate(G.PONTO, 1):
            if not ops:
                continue
            r = dict(M.escolha(ops, c), pagina='ponto')
            self.assertFalse(r['amplitude20'], f'pergunta {i}: {r["comprimentos"]}')
            self.assertFalse(r['denunciadora'], f'pergunta {i}: {r["comprimentos"]}')
            rows.append(r)
        self.assertEqual(len(rows), 8)
        r = M.resumir(rows, 'pagina')['ponto']
        self.assertLessEqual(r['certaMaisLonga'], math.ceil(r['esperadoMaisLonga']))
        self.assertLessEqual(r['certaMaisCurta'], math.ceil(r['esperadoMaisLonga']))


if __name__ == '__main__':
    unittest.main()
