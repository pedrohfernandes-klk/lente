"""02/11/2026: o pedido 2 de Ideias só pode mudar o cache dos ficheiros na Cidadania."""
from pathlib import Path
import re
import json
import subprocess
import unittest
import menus163

ROOT = Path(__file__).resolve().parents[1]
BASE = 'fbfb8509d6e104f00811321d95ed4d999f8df2cd'
RENOMEACOES = json.loads((ROOT / 'tests/fixtures/cidadania-nomes-20261103.json').read_text(encoding='utf-8'))
# 05/11/2026: manifesto fechado das trocas da revisão de 5/11 no Lente.
REVISAO_0511 = json.loads((ROOT / 'tests/fixtures/revisao-lente-20261105.json').read_text(encoding='utf-8'))
# 05/11/2026: decisão 147 (Laboratório sem o Português), manifesto fechado das trocas na navegação do Laboratório.
LAB_147 = json.loads((ROOT / 'tests/fixtures/lab-147-20261105.json').read_text(encoding='utf-8'))
# 05/11/2026: decisão 146 (discussões em turma, trabalhos individuais): manifesto fechado tools/trocas/grupos-146-20261105.json.
import grupos146  # noqa: E402
# 06/11/2026: decisão 149 (volta «Dilemas»): manifesto fechado tests/fixtures/dilemas-149-20261106.json.
from renomeacoes_cidadania import dilemas_149  # noqa: E402
# 05/11/2026: plano do molde da Cidadania, pedido 1 (motor, casca e progresso, sem conteúdo novo). Manifesto fechado das trocas
# literais, com contagem exata, por cima das decisões 146 e 154: nas dez sessões do piloto, só o cfg da família (as chaves novas
# do CFG e o CFG.fim) e o progresso comum que esse cfg pede; na página do módulo e no seu gerador, «Feita» com feita(st) do
# progresso comum. Em assets/licoes/cidadania.css, só um bloco no fim, marcado, em que todas as regras pertencem a
# body.molde-cidadania (as páginas sem o molde não mudam). Nada mais se aceita.
MOLDE_P1 = json.loads((ROOT / 'tools/trocas/molde-pedido1-20261105.json').read_text(encoding='utf-8'))
MARCA_MOLDE = b'/* ==== molde cidadania-2026-11 ==== */'
# 05/11/2026: plano do molde da Cidadania, pedido 2 (s01 do M1 na versão final). Mais uma camada, a mais recente, com as mesmas
# regras: o manifesto fechado tools/trocas/molde-pedido2-20261105.json (trocas literais, contagem exata) nos ficheiros que o
# pedido 2 muda em parte; os que escreve inteiros (molde_pedido2.INTEIROS: a página e a versão para imprimir da s01, a sua fonte
# e o seu .json) comparam-se, letra a letra, com o que o gerador escreve hoje, e a s01 tem de cumprir o contrato do molde.
import molde_pedido2  # noqa: E402
# 06/11/2026: plano do molde da Cidadania, sessão 02 do M1 na versão final (decisão 166). Mais uma camada, agora a mais recente,
# com as mesmas regras: o manifesto fechado tools/trocas/molde-s02-20261106.json (trocas literais, contagem exata) nos ficheiros
# que a s02 muda em parte; os que escreve inteiros (molde_s02.INTEIROS: a página e a versão para imprimir da s02, a sua fonte e o
# seu .json) comparam-se, letra a letra, com o que o gerador escreve hoje, e a s02 tem de cumprir o contrato do molde.
import molde_s02  # noqa: E402
# 06/11/2026: plano do molde da Cidadania, sessão 03 do M1 na versão final (decisões 166 a 168). Mais uma camada, agora a mais
# recente, com as mesmas regras: o manifesto fechado tools/trocas/molde-s03-20261106.json (trocas literais, contagem exata) nos
# ficheiros que a s03 muda em parte; os que escreve inteiros (molde_s03.INTEIROS: a página e a versão para imprimir da s03, a sua
# fonte e o seu .json) comparam-se, letra a letra, com o que o gerador escreve hoje, e a s03 tem de cumprir o contrato do molde.
import molde_s03  # noqa: E402
# 06/11/2026: plano do molde da Cidadania, sessão 04 do M1 na versão final (decisões 166 a 168). Mais uma camada, agora a mais
# recente, por cima da da s03, com as mesmas regras: o manifesto fechado tools/trocas/molde-s04-20261106.json (trocas literais,
# contagem exata) nos ficheiros que a s04 muda em parte; os que escreve inteiros (molde_s04.INTEIROS: a página e a versão para
# imprimir da s04, a sua fonte e o seu .json) comparam-se, letra a letra, com o que o gerador escreve hoje, e a s04 tem de cumprir o
# contrato do molde.
import molde_s04  # noqa: E402
# 06/11/2026: sessão 05 do M1 na versão final (decisões 166 a 168). Mais uma camada, agora a mais recente, por cima da da s04, com
# as mesmas regras: o manifesto fechado tools/trocas/molde-s05-20261106.json nos ficheiros que a s05 muda em parte; os que escreve
# inteiros (molde_s05.INTEIROS) comparam-se, letra a letra, com o que o gerador escreve hoje, e a s05 tem de cumprir o contrato do
# molde. 06/11/2026 (fusão do main com as sessões 2 a 4 finais e o elétrico): o manifesto parte do main (5b4a451), já com a s04.
import molde_s05  # noqa: E402
# 06/11/2026: sessão 06 do M1 na versão final (decisões 166 a 168). Mais uma camada, agora a mais recente, por cima da da s05, com
# as mesmas regras: o manifesto fechado tools/trocas/molde-s06-20261106.json (trocas literais, contagem exata) nos ficheiros que a
# s06 muda em parte; os que escreve inteiros (molde_s06.INTEIROS: a página e a versão para imprimir da s06, a sua fonte e o seu
# .json) comparam-se, letra a letra, com o que o gerador escreve hoje, e a s06 tem de cumprir o contrato do molde. 06/11/2026
# (fusão do main com as sessões 2 a 5 finais na sessão 6): o manifesto parte do main (d04c20f), já com a s05.
import molde_s06  # noqa: E402
# 06/11/2026: sessão 07 do M1 na versão final (decisões 166 a 168). Mais uma camada, agora a mais recente, por cima da da s06, com
# as mesmas regras: o manifesto fechado tools/trocas/molde-s07-20261106.json (trocas literais, contagem exata) nos ficheiros que a
# s07 muda em parte; os que escreve inteiros (molde_s07.INTEIROS: a página e a versão para imprimir da s07, a sua fonte e o seu
# .json) comparam-se, letra a letra, com o que o gerador escreve hoje, e a s07 tem de cumprir o contrato do molde. 06/11/2026
# (fusão do main com as sessões 2 a 6 finais na sessão 7): o manifesto parte do main (8731fb9), já com a s06.
import molde_s07  # noqa: E402
# 06/11/2026: sessão 08 do M1 na versão final (decisões 166 a 168). Mais uma camada, agora a mais recente, por cima da da s07, com
# as mesmas regras: o manifesto fechado tools/trocas/molde-s08-20261106.json (trocas literais, contagem exata) nos ficheiros que a
# s08 muda em parte; os que escreve inteiros (molde_s08.INTEIROS: a página e a versão para imprimir da s08, a sua fonte e o seu
# .json) comparam-se, letra a letra, com o que o gerador escreve hoje, e a s08 tem de cumprir o contrato do molde. 06/11/2026
# (fusão do main com as sessões 2 a 7 finais na sessão 8): o manifesto parte do main (3c774cb), já com a s07.
import molde_s08  # noqa: E402
# 07/11/2026: plano do molde da Cidadania, sessão 10 do M1 na versão final, a sessão de mostra (decisões 166 a 168). Mais uma camada,
# a mais recente, com as mesmas regras: o manifesto fechado tools/trocas/molde-s10-20261107.json (parte do main dc01487) nos
# ficheiros que a s10 muda em parte; os que escreve inteiros (molde_s10.INTEIROS) comparam-se com o que o gerador escreve hoje.
import molde_s10  # noqa: E402


def desfazer_molde(texto, nome):
    for antigo, novo, n in reversed(MOLDE_P1.get(nome, [])):
        if texto.count(novo) != n:
            raise AssertionError(('molde, pedido 1 (desfazer)', nome, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def aplicar_molde(texto, nome):
    for antigo, novo, n in MOLDE_P1.get(nome, []):
        if texto.count(antigo) != n:
            raise AssertionError(('molde, pedido 1', nome, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def seletores_fora_do_molde(css):
    """Os seletores do bloco do molde que não pertencem a body.molde-cidadania (tem de dar lista vazia)."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    fora = []
    for sel in re.findall(r'([^{}]+)\{[^{}]*\}', re.sub(r'@media[^{]*\{', '', css)):
        partes, nivel, atual = [], 0, ''
        for ch in sel:  # só as vírgulas de fora dos parênteses separam seletores (:is(a,summary) é um só)
            nivel += (ch == '(') - (ch == ')')
            if ch == ',' and nivel == 0:
                partes.append(atual)
                atual = ''
            else:
                atual += ch
        for s in partes + [atual]:
            s = s.strip()
            if s and not s.startswith('@') and 'body.molde-cidadania' not in s and not re.fullmatch(r'(?:from|to|\d+%)', s):
                fora.append(s)
    return fora


class CidadaniaBase(unittest.TestCase):
    def test_cidadania_igual_a_base(self):
        nomes = subprocess.check_output(
            ['git', 'ls-tree', '-r', '--name-only', BASE, '--',
             'cidadania/piloto', 'cidadania/m1', 'assets/licoes/cidadania.css'], cwd=ROOT
        ).decode().splitlines()
        self.assertGreater(len(nomes), 50)
        for nome in nomes:
            with self.subTest(ficheiro=nome):
                # 05/11/2026 (pedido 2): o ficheiro escrito inteiro tem de ser o do seu gerador; nada mais se aceita.
                if nome in molde_pedido2.INTEIROS:
                    self.assertTrue(molde_pedido2.inteiro_ok(nome), nome)
                    continue
                # 06/11/2026 (sessão 02 no molde): o mesmo para os ficheiros que a s02 escreve inteiros.
                if nome in molde_s02.INTEIROS:
                    self.assertTrue(molde_s02.inteiro_ok(nome), nome)
                    continue
                # 06/11/2026 (sessão 03 no molde): o mesmo para os ficheiros que a s03 escreve inteiros.
                if nome in molde_s03.INTEIROS:
                    self.assertTrue(molde_s03.inteiro_ok(nome), nome)
                    continue
                # 06/11/2026 (sessão 04 no molde): o mesmo para os ficheiros que a s04 escreve inteiros.
                if nome in molde_s04.INTEIROS:
                    self.assertTrue(molde_s04.inteiro_ok(nome), nome)
                    continue
                # 06/11/2026 (sessão 05 no molde): o mesmo para os ficheiros que a s05 escreve inteiros.
                if nome in molde_s05.INTEIROS:
                    self.assertTrue(molde_s05.inteiro_ok(nome), nome)
                    continue
                # 06/11/2026 (sessão 06 no molde): o mesmo para os ficheiros que a s06 escreve inteiros.
                if nome in molde_s06.INTEIROS:
                    self.assertTrue(molde_s06.inteiro_ok(nome), nome)
                    continue
                # 06/11/2026 (sessão 07 no molde): o mesmo para os ficheiros que a s07 escreve inteiros.
                if nome in molde_s07.INTEIROS:
                    self.assertTrue(molde_s07.inteiro_ok(nome), nome)
                    continue
                # 06/11/2026 (sessão 08 no molde): o mesmo para os ficheiros que a s08 escreve inteiros.
                if nome in molde_s08.INTEIROS:
                    self.assertTrue(molde_s08.inteiro_ok(nome), nome)
                    continue
                # 07/11/2026 (sessão 10 no molde): o mesmo para os ficheiros que a s10 escreve inteiros.
                if nome in molde_s10.INTEIROS:
                    self.assertTrue(molde_s10.inteiro_ok(nome), nome)
                    continue
                antes = subprocess.check_output(['git', 'show', f'{BASE}:{nome}'], cwd=ROOT)
                # 03/11/2026: #107 autoriza só os títulos deste manifesto fechado.
                for antigo, novo, quantidade in RENOMEACOES.get(nome, []):
                    self.assertEqual(antes.count(antigo.encode()), quantidade)
                    antes = antes.replace(antigo.encode(), novo.encode())
                # 05/11/2026: decisão 147. O cartaz rotativo deixa de anunciar o Corta! e as peças do Laboratório
                # (percurso-anterior); só as trocas do manifesto fechado, com contagem exata.
                for antigo, novo, quantidade in LAB_147.get(nome, []):
                    self.assertEqual(antes.count(antigo.encode()), quantidade)
                    antes = antes.replace(antigo.encode(), novo.encode())
                depois = (ROOT / nome).read_bytes()
                # 06/11/2026: fusão do main (com a sessão 1 da Cidadania, #126) nos menus do Laboratório (decisão 163). As camadas do
                # molde (pedidos 1 e 2) deixam de se desfazer no ficheiro atual e passam a aplicar-se à base, pela ordem em que se
                # sobrepõem (ver abaixo); aplicar exige a contagem exata de cada «antigo» como desfazer exigia a de cada «novo».
                # 06/11/2026 (sessão 03 no molde, na fusão do main com a sessão 2 final, os menus e o «Dilemas»): o manifesto da s03
                # parte agora do main (b29833d), já com a 163 e a 149; a s03 é a camada mais recente e desfaz-se no ficheiro atual,
                # com contagem exata de cada «novo», antes de se tirarem as versões de cache; a comparação continua integral.
                # 06/11/2026 (sessão 04 no molde, na fusão do main com as sessões 2 e 3 finais, os menus e o «Dilemas»): o manifesto
                # da s04 parte do main (ba5211f), já com a s03; a s04 é agora a camada mais recente e desfaz-se primeiro no ficheiro
                # atual, com contagem exata de cada «novo»; depois desfaz-se a da s03, como antes, e só então se tiram as versões de
                # cache; a comparação continua integral.
                # 06/11/2026 (sessão 05 no molde, na fusão do main com as sessões 2 a 4 finais e o elétrico): o manifesto da s05 parte
                # do main (5b4a451), já com a s04; a s05 é agora a camada mais recente e desfaz-se primeiro no ficheiro atual, com
                # contagem exata de cada «novo»; depois a da s04 e a da s03, como antes, e só então se tiram as versões de cache.
                # 06/11/2026 (sessão 06 no molde, na fusão do main com as sessões 2 a 5 finais): o manifesto da s06 parte do main
                # (d04c20f), já com a s05; a s06 é agora a camada mais recente e desfaz-se primeiro no ficheiro atual, com contagem
                # exata de cada «novo»; depois a da s05, a da s04 e a da s03, como antes, e só então se tiram as versões de cache.
                # 06/11/2026 (sessão 07 no molde, na fusão do main com as sessões 2 a 6 finais): o manifesto da s07 parte do main
                # (8731fb9), já com a s06; a s07 é agora a camada mais recente e desfaz-se primeiro no ficheiro atual, com contagem
                # exata de cada «novo»; depois a da s06, a da s05, a da s04 e a da s03, como antes, e só então se tiram as versões de
                # cache.
                # 06/11/2026 (sessão 08 no molde, na fusão do main com as sessões 2 a 7 finais): o manifesto da s08 parte do main
                # (3c774cb), já com a s07; a s08 é agora a camada mais recente e desfaz-se primeiro no ficheiro atual, com contagem
                # exata de cada «novo»; depois a da s07, a da s06, a da s05, a da s04 e a da s03, como antes, e só então se tiram as
                # versões de cache.
                # 07/11/2026 (sessão 10 no molde): a camada da s10 parte do main dc01487, por cima da da s08: desfaz-se primeiro.
                if nome in molde_s10.TROCAS:
                    depois = molde_s10.desfazer(depois.decode('utf-8'), nome).encode('utf-8')
                if nome in molde_s08.TROCAS:
                    depois = molde_s08.desfazer(depois.decode('utf-8'), nome).encode('utf-8')
                if nome in molde_s07.TROCAS:
                    depois = molde_s07.desfazer(depois.decode('utf-8'), nome).encode('utf-8')
                if nome in molde_s06.TROCAS:
                    depois = molde_s06.desfazer(depois.decode('utf-8'), nome).encode('utf-8')
                if nome in molde_s05.TROCAS:
                    depois = molde_s05.desfazer(depois.decode('utf-8'), nome).encode('utf-8')
                if nome in molde_s04.TROCAS:
                    depois = molde_s04.desfazer(depois.decode('utf-8'), nome).encode('utf-8')
                if nome in molde_s03.TROCAS:
                    depois = molde_s03.desfazer(depois.decode('utf-8'), nome).encode('utf-8')
                if nome == 'assets/licoes/cidadania.css':
                    self.assertEqual(depois.count(MARCA_MOLDE), 1)
                    depois, bloco = depois.split(MARCA_MOLDE)
                    self.assertEqual(seletores_fora_do_molde(bloco.decode('utf-8')), [])
                # 05/11/2026: decisão 146 (discussões em turma, trabalhos individuais): só se desfazem as trocas do manifesto fechado, com contagem exata; o resto compara-se como antes.
                # 06/11/2026: fusão do main (com o #123) nos menus do Laboratório (decisão 163). As camadas compõem-se pela ordem em que
                # se sobrepõem, todas sobre a base: 147 (acima), 146 e 154 (tests/grupos146.py aplica-as por esta ordem) e, por último,
                # a 163. Por isso a 146 e a 154 passam a aplicar-se à base, em vez de se desfazerem no ficheiro atual; aplicar exige a
                # contagem exata de cada «antigo» como desfazer exigia a de cada «novo», e a comparação continua integral.
                if nome in grupos146.TROCAS:
                    antes = grupos146.aplicar(antes.decode('utf-8'), nome).encode('utf-8')
                # 05/11/2026: plano do molde da Cidadania, pedido 1, por cima da 146 e da 154; depois o pedido 2, por cima do 1.
                # 06/11/2026: fusão com os menus (decisão 163). Aplicam-se à base, como a 146 e a 154, antes da 163; cada troca com
                # contagem exata, e a comparação continua integral.
                if nome in MOLDE_P1:
                    antes = aplicar_molde(antes.decode('utf-8'), nome).encode('utf-8')
                if nome in molde_pedido2.TROCAS:
                    antes = molde_pedido2.aplicar(antes.decode('utf-8'), nome).encode('utf-8')
                # 06/11/2026 (sessão 02 no molde, na fusão do main com os menus): a camada da s02 aplica-se à base por cima do
                # pedido 2 e antes da 163, com contagem exata de cada «antigo»; a comparação continua integral.
                if nome in molde_s02.TROCAS:
                    antes = molde_s02.aplicar(antes.decode('utf-8'), nome).encode('utf-8')
                # 05/11/2026: decisão 163 (menus do Laboratório e das lições). O menu ≡ novo, menu.css, menu.js, o aviso sem
                # JavaScript e a marca «Cidadania» do piloto: só as trocas do manifesto fechado tests/fixtures/menus-163-20261105.json,
                # com contagem exata, sobre o texto já sem as versões de cache (como a comparação); a comparação continua integral.
                self.assertEqual(menus163.aplicar(re.sub(rb'\?v=[\w-]+', b'?v=CACHE', antes), nome, sem_cache=True),
                                 re.sub(rb'\?v=[\w-]+', b'?v=CACHE', depois))

    def test_renomeacao_exata_sobre_main_publicado(self):
        base = '349d2457e1f056b69c6dda550aace2a6f5377051'
        geracao = json.loads((ROOT / 'tests/fixtures/cidadania-geracao-20261103.json').read_text(encoding='utf-8'))
        for nome, trocas in RENOMEACOES.items():
            with self.subTest(ficheiro=nome):
                # 05/11/2026 (pedido 2): o ficheiro escrito inteiro tem de ser o do seu gerador; nada mais se aceita.
                if nome in molde_pedido2.INTEIROS:
                    self.assertTrue(molde_pedido2.inteiro_ok(nome), nome)
                    continue
                # 06/11/2026 (sessão 02 no molde): o mesmo para os ficheiros que a s02 escreve inteiros.
                if nome in molde_s02.INTEIROS:
                    self.assertTrue(molde_s02.inteiro_ok(nome), nome)
                    continue
                # 06/11/2026 (sessão 03 no molde): o mesmo para os ficheiros que a s03 escreve inteiros.
                if nome in molde_s03.INTEIROS:
                    self.assertTrue(molde_s03.inteiro_ok(nome), nome)
                    continue
                # 06/11/2026 (sessão 04 no molde): o mesmo para os ficheiros que a s04 escreve inteiros.
                if nome in molde_s04.INTEIROS:
                    self.assertTrue(molde_s04.inteiro_ok(nome), nome)
                    continue
                # 06/11/2026 (sessão 05 no molde): o mesmo para os ficheiros que a s05 escreve inteiros.
                if nome in molde_s05.INTEIROS:
                    self.assertTrue(molde_s05.inteiro_ok(nome), nome)
                    continue
                # 06/11/2026 (sessão 06 no molde): o mesmo para os ficheiros que a s06 escreve inteiros.
                if nome in molde_s06.INTEIROS:
                    self.assertTrue(molde_s06.inteiro_ok(nome), nome)
                    continue
                # 06/11/2026 (sessão 07 no molde): o mesmo para os ficheiros que a s07 escreve inteiros.
                if nome in molde_s07.INTEIROS:
                    self.assertTrue(molde_s07.inteiro_ok(nome), nome)
                    continue
                # 06/11/2026 (sessão 08 no molde): o mesmo para os ficheiros que a s08 escreve inteiros.
                if nome in molde_s08.INTEIROS:
                    self.assertTrue(molde_s08.inteiro_ok(nome), nome)
                    continue
                # 07/11/2026 (sessão 10 no molde): o mesmo para os ficheiros que a s10 escreve inteiros.
                if nome in molde_s10.INTEIROS:
                    self.assertTrue(molde_s10.inteiro_ok(nome), nome)
                    continue
                esperado = subprocess.check_output(['git', 'show', f'{base}:{nome}'], cwd=ROOT).decode()
                for antigo, novo, quantidade in trocas:
                    self.assertEqual(esperado.count(antigo), quantidade)
                    esperado = esperado.replace(antigo, novo)
                for antigo, novo, quantidade in geracao.get(nome, []):
                    self.assertEqual(esperado.count(antigo), quantidade)
                    esperado = esperado.replace(antigo, novo)
                # 05/11/2026: revisão de 5/11 (Lente). Só as trocas deste manifesto fechado (linha do «Ideias» no cartão do
                # Laboratório, rodapé dos excertos, ramo «Decisões» do mapa, bloco repetido da Cidadania e crédito dos desenhos
                # das lições 1 e 2 da Justiça), com contagem exata; a comparação continua integral.
                for antigo, novo, quantidade in REVISAO_0511.get(nome, []):
                    self.assertEqual(esperado.count(antigo), quantidade)
                    esperado = esperado.replace(antigo, novo)
                # 05/11/2026: decisão 147. O ramo do Laboratório no mapa segue percursos.json sem as peças retiradas;
                # só as trocas deste manifesto, com contagem exata.
                for antigo, novo, quantidade in LAB_147.get(nome, []):
                    self.assertEqual(esperado.count(antigo), quantidade)
                    esperado = esperado.replace(antigo, novo)
                # 05/11/2026: decisão 146 (discussões em turma, trabalhos individuais): as trocas do manifesto fechado, com contagem exata.
                # 05/11/2026: depois da fusão do #122, por cima da camada da decisão 147 (as camadas 146 e 154 partem do main com o #122).
                esperado = grupos146.aplicar(esperado, nome)
                # 05/11/2026: plano do molde da Cidadania, pedido 1: a camada do molde, com contagem exata, por cima.
                esperado = aplicar_molde(esperado, nome)
                # 05/11/2026: plano do molde, pedido 2: a camada do pedido 2, com contagem exata, por cima de tudo.
                esperado = molde_pedido2.aplicar(esperado, nome)
                # 06/11/2026: a camada da sessão 02 no molde, com contagem exata, por cima do pedido 2.
                # 06/11/2026: fusão do main (com os menus, #125, e o «Dilemas», #127): a s02 foi feita sobre fa6c6c2, antes da
                # 163; aplica-se aqui e a 163 e a 149 vêm depois, pela ordem em que se sobrepõem.
                esperado = molde_s02.aplicar(esperado, nome)
                # 05/11/2026: decisão 163. O menu ≡ novo e a ordem do Laboratório na entrada do Lente: só as trocas do manifesto
                # fechado tests/fixtures/menus-163-20261105.json, com contagem exata; a comparação continua integral.
                # 06/11/2026: fusão do main (com o #123). A 163 aplica-se por último, por cima da 147, da 146 e da 154.
                # 06/11/2026: fusão do main (com a sessão 1 da Cidadania, #126). A 163 continua a ser a última, também por cima dos
                # pedidos 1 e 2 do molde.
                esperado = menus163.aplicar(esperado, nome)
                # 03/11/2026: #103 gera apenas a abertura e o crédito da Justiça;
                # conserva a comparação integral de todos os restantes conteúdos.
                # 06/11/2026: decisão 170 (o elétrico mexe-se). O instalar() passa a escrever a faixa com a alavanca que roda, as
                # duas lâminas e os quatro sinais de alerta escondidos, o crédito com «os sinais de alerta» e o CSS em
                # ?v=20261106-1. Continua a ser a única coisa gerada nesta página; o resto continua a comparar-se letra a letra.
                if nome == 'olhar-e-decidir/justica/index.html':
                    import importlib.util
                    spec = importlib.util.spec_from_file_location('carris', ROOT / 'tools/gerar_carris.py')
                    carris = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(carris)
                    esperado = carris.instalar(esperado)
                # 06/11/2026: decisão 149, volta «Dilemas» onde o #107 pôs «Decisões» como nome da família; só as trocas do
                # manifesto fechado, com contagem exata. O sidequest «Decisões que parecem razoáveis» e endereços ficam.
                esperado = dilemas_149(esperado, nome)
                # 06/11/2026: a camada da sessão 03 no molde, com contagem exata, por cima de tudo. 06/11/2026 (fusão do main com a
                # sessão 2 final, os menus e o «Dilemas»): o manifesto da s03 parte do main (b29833d), por isso aplica-se depois da 163
                # e da 149, em último lugar.
                esperado = molde_s03.aplicar(esperado, nome)
                # 06/11/2026: a camada da sessão 04 no molde, com contagem exata, por cima de tudo. 06/11/2026 (fusão do main com as
                # sessões 2 e 3 finais, os menus e o «Dilemas»): o manifesto da s04 parte do main (ba5211f), por isso aplica-se depois
                # da s03, em último lugar.
                esperado = molde_s04.aplicar(esperado, nome)
                # 06/11/2026: a camada da sessão 05 no molde, com contagem exata, por cima de tudo. 06/11/2026 (fusão do main com as
                # sessões 2 a 4 finais e o elétrico): o manifesto da s05 parte do main (5b4a451), por isso aplica-se depois da s04,
                # em último lugar.
                esperado = molde_s05.aplicar(esperado, nome)
                # 06/11/2026: a camada da sessão 06 no molde, com contagem exata, por cima de tudo. 06/11/2026 (fusão do main com as
                # sessões 2 a 5 finais): o manifesto da s06 parte do main (d04c20f), por isso aplica-se depois da s05, em último lugar.
                esperado = molde_s06.aplicar(esperado, nome)
                # 06/11/2026: a camada da sessão 07 no molde, com contagem exata, por cima de tudo. 06/11/2026 (fusão do main com as
                # sessões 2 a 6 finais): o manifesto da s07 parte do main (8731fb9), por isso aplica-se depois da s06, em último lugar.
                esperado = molde_s07.aplicar(esperado, nome)
                # 06/11/2026: a camada da sessão 08 no molde, com contagem exata, por cima de tudo. 06/11/2026 (fusão do main com as
                # sessões 2 a 7 finais): o manifesto da s08 parte do main (3c774cb), por isso aplica-se depois da s07, em último lugar.
                esperado = molde_s08.aplicar(esperado, nome)
                # 07/11/2026: a camada da sessão 10 no molde (manifesto a partir do main dc01487), em último lugar.
                esperado = molde_s10.aplicar(esperado, nome)
                self.assertEqual(esperado, (ROOT / nome).read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
