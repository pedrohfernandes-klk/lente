"""02/11/2026: o pedido 2 de Ideias só pode mudar o cache dos ficheiros na Cidadania."""
from pathlib import Path
import re
import json
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = 'fbfb8509d6e104f00811321d95ed4d999f8df2cd'
RENOMEACOES = json.loads((ROOT / 'tests/fixtures/cidadania-nomes-20261103.json').read_text(encoding='utf-8'))
# 05/11/2026: manifesto fechado das trocas da revisão de 5/11 no Lente.
REVISAO_0511 = json.loads((ROOT / 'tests/fixtures/revisao-lente-20261105.json').read_text(encoding='utf-8'))
# 05/11/2026: decisão 147 (Laboratório sem o Português), manifesto fechado das trocas na navegação do Laboratório.
LAB_147 = json.loads((ROOT / 'tests/fixtures/lab-147-20261105.json').read_text(encoding='utf-8'))
# 05/11/2026: decisão 146 (discussões em turma, trabalhos individuais): manifesto fechado tools/trocas/grupos-146-20261105.json.
import grupos146  # noqa: E402
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
# 06/11/2026: plano do molde da Cidadania, sessão 06 do M1 na versão final (decisões 166 a 168). Mais uma camada, agora a mais
# recente, com as mesmas regras: o manifesto fechado tools/trocas/molde-s06-20261106.json (trocas literais, contagem exata) nos
# ficheiros que a s06 muda em parte; os que escreve inteiros (molde_s06.INTEIROS: a página e a versão para imprimir da s06, a sua
# fonte e o seu .json) comparam-se, letra a letra, com o que o gerador escreve hoje, e a s06 tem de cumprir o contrato do molde.
import molde_s06  # noqa: E402


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
                # 06/11/2026 (sessão 06 no molde): o mesmo para os ficheiros que a s06 escreve inteiros.
                if nome in molde_s06.INTEIROS:
                    self.assertTrue(molde_s06.inteiro_ok(nome), nome)
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
                # 06/11/2026 (sessão 06 no molde): desfaz-se primeiro a camada da s06, que é agora a mais recente.
                if nome in molde_s06.TROCAS:
                    depois = molde_s06.desfazer(depois.decode('utf-8'), nome).encode('utf-8')
                # 06/11/2026 (sessão 02 no molde): desfaz-se primeiro a camada da s02, que é agora a mais recente.
                if nome in molde_s02.TROCAS:
                    depois = molde_s02.desfazer(depois.decode('utf-8'), nome).encode('utf-8')
                # 05/11/2026 (pedido 2): desfaz-se primeiro a camada do pedido 2, que é agora a mais recente.
                if nome in molde_pedido2.TROCAS:
                    depois = molde_pedido2.desfazer(depois.decode('utf-8'), nome).encode('utf-8')
                # 05/11/2026: plano do molde da Cidadania, pedido 1: desfaz-se primeiro a camada do molde (a mais recente).
                if nome in MOLDE_P1:
                    depois = desfazer_molde(depois.decode('utf-8'), nome).encode('utf-8')
                if nome == 'assets/licoes/cidadania.css':
                    self.assertEqual(depois.count(MARCA_MOLDE), 1)
                    depois, bloco = depois.split(MARCA_MOLDE)
                    self.assertEqual(seletores_fora_do_molde(bloco.decode('utf-8')), [])
                # 05/11/2026: decisão 146 (discussões em turma, trabalhos individuais): só se desfazem as trocas do manifesto fechado, com contagem exata; o resto compara-se como antes.
                if nome in grupos146.TROCAS:
                    depois = grupos146.desfazer(depois.decode('utf-8'), nome).encode('utf-8')
                self.assertEqual(re.sub(rb'\?v=[\w-]+', b'?v=CACHE', antes),
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
                # 06/11/2026 (sessão 06 no molde): o mesmo para os ficheiros que a s06 escreve inteiros.
                if nome in molde_s06.INTEIROS:
                    self.assertTrue(molde_s06.inteiro_ok(nome), nome)
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
                # 06/11/2026: a camada da sessão 02 no molde, com contagem exata, por cima de tudo.
                esperado = molde_s02.aplicar(esperado, nome)
                # 06/11/2026: a camada da sessão 06 no molde, com contagem exata, por cima de tudo.
                esperado = molde_s06.aplicar(esperado, nome)
                # 03/11/2026: #103 gera apenas a abertura e o crédito da Justiça;
                # conserva a comparação integral de todos os restantes conteúdos.
                if nome == 'olhar-e-decidir/justica/index.html':
                    import importlib.util
                    spec = importlib.util.spec_from_file_location('carris', ROOT / 'tools/gerar_carris.py')
                    carris = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(carris)
                    esperado = carris.instalar(esperado)
                self.assertEqual(esperado, (ROOT / nome).read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
