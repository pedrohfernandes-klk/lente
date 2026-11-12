"""02/11/2026: bases reprodutíveis e regras estritas para conteúdo novo."""
import importlib.util
import hashlib
import json
import re
import sys
import unittest
from renomeacoes_cidadania import renomear, dilemas_149
# 08/11/2026: decisão 152 («cuidado em todas as lições»): manifesto fechado tools/trocas/cuidado-lente-20261108.json.
import cuidado_lente
# 08/11/2026: decisões 153 e 176 (pedido lente-2): manifesto fechado tools/trocas/creditos-i-lente2-20261108.json.
import creditos_i_lente2
import justica_20261110
from pathlib import Path

R = Path(__file__).resolve().parents[1]
T = R / 'tools/justica'
spec = importlib.util.spec_from_file_location('justica_validar', T / 'validar.py')
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)
MANIFESTO = json.loads((T / 'licoes.json').read_text('utf-8'))

# 02/11/2026: leituras publicadas acima de 95 palavras, a dividir na fase 1.
# Lista fechada: só desaparece quando a leitura passa a ter <=95 palavras;
# enquanto exceder, a contagem tem de ser exatamente a registada, nunca maior.
LEITURAS_PUBLICADAS = {(1, 12): 99}
LEITURAS_HASH = {(1, 12): 'd8c4de55a28f228068bd46a35da1246e043eff98f1e2189b48eaab437e424d38'}


def banco(n):
    return json.loads((T / f'bancos/licao-{n}.json').read_text('utf-8'))


class BasesJustica(unittest.TestCase):
    def test_manifesto_cobre_todas_as_paginas_e_bancos(self):
        # 02/11/2026: omitir uma lição no manifesto não pode afastá-la dos testes.
        numeros = [m['numero'] for m in MANIFESTO]
        self.assertEqual(len(numeros), len(set(numeros)))
        self.assertEqual(numeros, list(range(1, len(numeros)+1)))
        self.assertEqual(set(numeros), {int(p.parent.name.split('-')[1]) for p in (R/'olhar-e-decidir/justica').glob('licao-*/index.html')})
        self.assertEqual(set(numeros), {int(p.stem.split('-')[1]) for p in (T/'bancos').glob('licao-*.json')})
        for m in MANIFESTO:
            self.assertEqual(m['chave'], f"lente-justica-licao-{m['numero']}")
            self.assertRegex(m['video'], r'^[\w-]{11}$')
            self.assertTrue(1 <= len(m['aulas']) <= 2)
            self.assertTrue(all(type(a) is int and 1 <= a <= 24 for a in m['aulas']))
            self.assertIsInstance(m['molde_novo'], bool)

    def test_regeneracao_literal(self):
        # 02/11/2026: inclui casca, menus, motor, chaves, ordem e índices do banco.
        for m in MANIFESTO:
            n = m['numero']
            molde = (T/f'moldes/licao-{n}.html').read_text('utf-8')
            self.assertEqual(molde.count('@@ITENS@@'), 1)
            gerada = molde.replace('@@ITENS@@', (T/f'bancos/licao-{n}.json').read_text('utf-8').rstrip('\n'))
            self.assertEqual(gerada, (R/f'olhar-e-decidir/justica/licao-{n}/index.html').read_text('utf-8'))
            if n > 3:
                self.assertTrue(m["molde_novo"])
                continue  # Páginas novas: regeneração e regras verificadas acima e abaixo.
            # 02/11/2026: prova contra o main de partida, só com as duas trocas autorizadas.
            # 03/11/2026 (#107; data posta a 05/11/2026): conserva o hash histórico; desfaz só os títulos autorizados do #107.
            # 06/11/2026: decisão 149 (volta «Dilemas»): antes do #107, desfaz-se só a troca do manifesto fechado
            # tests/fixtures/dilemas-149-20261106.json, com contagem exata; o hash histórico é o mesmo.
            # 08/11/2026: decisão 152 (pedido cuidado-lente). A camada mais recente desfaz-se primeiro, com contagem exata de cada
            # «novo»: as tabelas da lição 1 (três razões) e da lição 2 (a conta da Ford), a lista das três objeções da lição 3, o
            # espaço sem quebra nas durações, nos valores e nos séculos, e a folha da tabela de apoio no molde das lições 1 e 2
            # (tools/trocas/cuidado-lente-20261108.json); o hash histórico é o mesmo.
            # 08/11/2026: decisões 153 e 176 (pedido lente-2). A camada dos créditos atrás do «i» é agora a mais recente e desfaz-se
            # antes da do pedido cuidado-lente, com contagem exata de cada «novo»: o crédito de cada desenho volta ao span.cred da
            # legenda e saem a peça comum e o seu estilo no molde das lições 1 e 2; o hash histórico é o mesmo.
            gerada0 = creditos_i_lente2.desfazer(justica_20261110.desfazer(gerada, f'olhar-e-decidir/justica/licao-{n}/index.html'), f'olhar-e-decidir/justica/licao-{n}/index.html')
            original = renomear(dilemas_149(cuidado_lente.desfazer(gerada0, f'olhar-e-decidir/justica/licao-{n}/index.html'),
                                            f'olhar-e-decidir/justica/licao-{n}/index.html', inverter=True),
                                f'olhar-e-decidir/justica/licao-{n}/index.html', inverter=True)
            for troca in json.loads((T/'migracao.json').read_text('utf-8')):
                if troca['licao'] == n:
                    self.assertEqual(original.count(troca['novo']), 1)
                    original = original.replace(troca['novo'], troca['antigo'])
            self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), m['sha256_publicado'])

    def test_regras_e_lista_fechada_das_leituras(self):
        # 02/11/2026: os cartões novos não herdam exceções do publicado.
        encontradas = {}
        for m in MANIFESTO:
            n = m['numero']
            self.assertEqual(V.validar_banco(banco(n), n, m['molde_novo'], m.get('formato_curto', False), m.get('formato_guiado', False)), [])
            for k, x in enumerate(banco(n), 1):
                if x['t'] == 'ler' and V.palavras_visiveis(x) > 95:
                    encontradas[n,k] = V.palavras_visiveis(x)
                    self.assertFalse(m['molde_novo'])
                    # 05/11/2026: revisão de 5/11 (crédito dos desenhos). O hash histórico confere-se depois de desfazer só as trocas
                    # dessa revisão registadas em migracao.json; qualquer outra mudança no cartão continua a falhar.
                    # 08/11/2026: decisão 152 (pedido cuidado-lente). O cartão confere-se sem a camada do espaço sem quebra (as
                    # durações do botão e do data-dur), desfeita no banco com contagem exata pelo manifesto fechado
                    # tools/trocas/cuidado-lente-20261108.json; as palavras visíveis contam-se no cartão de hoje, como antes.
                    f = f'tools/justica/bancos/licao-{n}.json'
                    # 08/11/2026: decisões 153 e 176 (pedido lente-2). Antes, desfaz-se no banco a camada dos créditos atrás do «i»,
                    # a mais recente, com contagem exata (o crédito dos dois desenhos do cartão volta à legenda); o resto como antes.
                    x0 = dict(json.loads(cuidado_lente.desfazer(creditos_i_lente2.desfazer((T/f'bancos/licao-{n}.json').read_text('utf-8'), f), f))[k-1])
                    for t in json.loads((T/'migracao.json').read_text('utf-8')):
                        if t['licao'] == n and t['origem'].startswith('revisão de 5/11'):
                            antigo, novo = json.loads('"' + t['antigo'] + '"'), json.loads('"' + t['novo'] + '"')
                            x0['html'] = x0['html'].replace(novo, antigo)
                    self.assertEqual(hashlib.sha256(json.dumps(x0,ensure_ascii=False,sort_keys=True).encode()).hexdigest(), LEITURAS_HASH.get((n,k)))
        self.assertEqual(encontradas, {k: v for k,v in LEITURAS_PUBLICADAS.items() if k in encontradas})

    def test_desenhos_das_licoes_com_credito(self):
        # 05/11/2026: revisão de 5/11 (lente-cidadania-creditos-1): cada desenho das lições tem o crédito «Grafismo gerado com
        # recurso a IA.» na legenda, como no guião; um desenho novo sem crédito falha.
        # 08/11/2026: decisões 153 e 176 (pedido lente-2). O crédito passa para trás do «i» de cada desenho: continua a exigir o
        # texto completo, «Grafismo gerado com recurso a IA.», agora dentro de details.info-i (variante «linha», logo depois do
        # desenho e antes da legenda, com o nome «Créditos do desenho: …» e o que a legenda diz antes dos dois pontos); a legenda
        # que diz o que se vê fica, sem o crédito. Os mesmos 9 desenhos.
        total = 0
        for m in MANIFESTO:
            for x in banco(m['numero']):
                for fig in re.findall(r'<figure class="desenho">.*?</figure>', x.get('html') or '', re.S):
                    total += 1
                    self.assertRegex(fig, r'</svg><details class="info-i info-i--linha" name="info-i"><summary aria-label="Créditos do desenho: ([^"<:]+)"><span aria-hidden="true">i</span></summary>'
                                          r'<p class="info-i-texto">Grafismo gerado com recurso a IA\.</p></details><figcaption>\1: [^<]+</figcaption></figure>$', fig[-300:])
                    self.assertNotIn('class="cred"', fig)
        self.assertEqual(total, 9)

    def test_validador_recusa_regressoes(self):
        # 02/11/2026: provar que palavras proibidas e leitura longa nova falham.
        from copy import deepcopy
        for palavra in ('jogo', 'jogar', 'ficha', 'folha', 'professor'):
            itens = deepcopy(banco(2)); itens[0]['html'] = '<p>' + palavra + '</p>'
            self.assertTrue(V.validar_banco(itens, 2))
        itens = deepcopy(banco(2)); itens[0]['html'] = '<p>' + 'palavra ' * 96 + '</p>'
        self.assertTrue(V.validar_banco(itens, 2, True))
        self.assertEqual(V.palavras_visiveis({'html':'<p>one two</p><p>um dois</p>'}), 4)

    def test_manifesto_citacoes_e_privacidade(self):
        # 02/11/2026: formato, tempo e cobertura dos bancos, sem legendas em CI.
        citacoes = json.loads((T/'citacoes.json').read_text('utf-8'))
        self.assertEqual(citacoes, V.extrair_citacoes(T))
        self.assertTrue(citacoes)
        for c in citacoes:
            self.assertRegex(c['tempo'], r'^\d+:[0-5]\d$')
            self.assertTrue(c['frase'])
            self.assertLessEqual(len(re.findall(r'[.!?](?=\s|$)', c['frase'])), 2)
            self.assertIsNone(V.PROIBIDAS.search(c['frase']))
            self.assertEqual(c['video'], next(m['video'] for m in MANIFESTO if m['numero']==c['licao']))
        self.assertEqual(list(T.rglob('*.vtt')) + list(T.rglob('*.srt')), [])

    def test_molde_novo(self):
        # 02/11/2026: decisões 63/65 sem reduzir o teto nem dispensar o molde antigo.
        for m in MANIFESTO:
            if not m['molde_novo']:
                continue
            # 11/11/2026: cada lição nova é validada pelo formato que declara (guiado, curto ou molde novo).
            validar = V.validar_molde_guiado if m.get('formato_guiado') else V.validar_molde_curto if m.get('formato_curto') else V.validar_molde_novo
            self.assertEqual(validar(banco(m['numero'])), [])

    def test_molde_curto_recusa_cortes_longos_e_atividades_em_falta(self):
        from copy import deepcopy
        # 11/11/2026: as lições 4 a 13 passaram ao formato guiado. A prova do formato curto fica, sobre o banco curto da lição 4
        # tal como foi publicado a 10/11 (tests/fixtures/justica-formato-curto-exemplo.json), para o validador antigo não ficar sem teste.
        curto = json.loads((R/'tests/fixtures/justica-formato-curto-exemplo.json').read_text('utf-8'))
        itens = deepcopy(curto)
        self.assertEqual(V.validar_molde_curto(itens), [])
        itens[1]['html'] = itens[1]['html'].replace('data-fim="277"', 'data-fim="340"')
        self.assertIn('duracao_excerto', V.validar_molde_curto(itens))
        itens = deepcopy(curto); itens[2]['t'] = 'ler'
        self.assertIn('sequencia_curta', V.validar_molde_curto(itens))
        itens = deepcopy(curto); itens[2]['producao_livre'] = True
        self.assertIn('producao_livre', V.validar_molde_curto(itens))

    def test_molde_guiado_recusa_o_que_o_formato_proibe(self):
        # 11/11/2026: o formato guiado recusa cortes longos, excertos sem pergunta de escuta, retornos repetidos e falta de variedade.
        from copy import deepcopy
        n = next(m['numero'] for m in MANIFESTO if m.get('formato_guiado'))
        base = banco(n)
        self.assertEqual(V.validar_molde_guiado(base), [])
        k = next(i for i, x in enumerate(base) if 'ju-video' in x.get('html', ''))
        itens = deepcopy(base); fim = re.search(r'data-fim="(\d+)"', itens[k]['html'])[1]
        itens[k]['html'] = itens[k]['html'].replace(f'data-fim="{fim}"', f'data-fim="{int(fim)+200}"')
        self.assertIn('duracao_excerto', V.validar_molde_guiado(itens))
        itens = deepcopy(base); itens[k]['html'] = itens[k]['html'].replace('class="ex-antes"', 'class="x"')
        self.assertIn('escuta_orientada', V.validar_molde_guiado(itens))
        itens = deepcopy(base); itens[k]['html'] = itens[k]['html'].replace('Tempos conferidos com o áudio', 'Tempos')
        self.assertIn('proveniencia_tempos', V.validar_molde_guiado(itens))
        itens = deepcopy(base); v = next(x for x in itens if x['t'] == 'vf'); v['fe'] = v['f']
        self.assertIn('retorno_repetido', V.validar_molde_guiado(itens))
        itens = deepcopy(base); itens[1]['rot'] = 'Outra'
        self.assertIn('vocabulario', V.validar_molde_guiado(itens))
        itens = deepcopy(base); itens[-1]['producao_livre'] = False
        self.assertIn('sintese_curta', V.validar_molde_guiado(itens))

    def molde_de_prova(self):
        # 02/11/2026: prova independente dos bancos antigos, todos molde_novo=false.
        tipos = ['escolha', 'ler', 'escolha', 'ler', 'escolha', 'frase',
                 'versos', 'vf', 'frase', 'versos', 'vf', 'escolha',
                 'escrita', 'frase', 'versos', 'vf', 'escolha', 'ler']
        return [{'t':'ler', 'rot':'Abre', 'html':'<img src="exemplo.svg">No fim, consegues comparar.'},
                {'t':'mapa', 'rot':'Olha'}] + [dict(t=t) for t in tipos[:-1]] + [{'t':'ler', 'rot':'Na aula'}]

    def test_molde_ordena_palavras_e_versos_sem_contar_como_escrita(self):
        # 02/11/2026: L95-01; frase e versos contam também para os cinco tipos.
        itens = self.molde_de_prova()
        self.assertEqual(V.validar_molde_novo(itens), [])
        itens[7]['t'] = 'escrita'
        self.assertIn('producao_livre', V.validar_molde_novo(itens))

    def test_molde_conta_producao_livre_em_leitura(self):
        # 02/11/2026: L95-01; produção em papel não desaparece dentro de ler.
        itens = self.molde_de_prova()
        itens[-1]['producao_livre'] = True
        self.assertIn('producao_livre', V.validar_molde_novo(itens))
        next(x for x in itens if x['t'] == 'escrita')['t'] = 'vf'
        self.assertEqual(V.validar_molde_novo(itens), [])
        itens[3]['producao_livre'] = True
        self.assertIn('producao_livre', V.validar_molde_novo(itens))
        itens[3]['producao_livre'] = 'sim'
        self.assertIn('marcacao_producao_livre', V.validar_molde_novo(itens))

    def test_molde_mede_sucessao_visivel_incluindo_leituras(self):
        # 02/11/2026: L95-02; escolha/ler/escolha/ler/escolha não são três seguidas.
        itens = self.molde_de_prova()
        self.assertEqual(V.validar_molde_novo(itens), [])
        itens[3]['t'] = 'escolha'
        self.assertIn('sucessao', V.validar_molde_novo(itens))
        itens = self.molde_de_prova()
        itens[2]['t'] = 'ler'; itens[4]['t'] = 'ler'
        self.assertIn('sucessao', V.validar_molde_novo(itens))

    def test_validacao_do_banco_aplica_molde_novo(self):
        # 02/11/2026: o caminho usado pelo gerador não pode ignorar a regra.
        itens = self.molde_de_prova()
        itens[3]['t'] = 'escolha'
        self.assertIn('L4: molde novo: sucessao', V.validar_banco(itens, 4, True))


if __name__ == '__main__':
    unittest.main()
