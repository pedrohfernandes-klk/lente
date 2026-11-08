"""2026-11-08: pedido cidade-cartaz-lente (a secção da cidade chama-se «Ler a cidade» nos dois sítios e tem um cartaz na entrada do
Lente). Manifesto fechado das trocas literais [antigo, novo, contagem] que levam o main de cca60c2 à versão com o nome único e o
cartaz (tools/trocas/cidade-cartaz-lente-20261108.json): a frase do cartaz rotativo, as ligações e os títulos que diziam «A cidade
antes da aula», o rótulo do registo de progresso, o cartão «Ler a cidade.» na entrada (sem a linha pequena repetida no cartão do
Português), o enquadramento da fotografia e o gerador do percurso anterior do M1. Os testes que comparam com bases antigas aplicam-no
(ou desfazem-no) como a camada mais recente, por cima da dos créditos atrás do «i», com contagem exata, sem aceitar mais nada."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TROCAS = json.loads((ROOT / 'tools/trocas/cidade-cartaz-lente-20261108.json').read_text(encoding='utf-8'))


def aplicar(texto, ficheiro):
    for antigo, novo, n in TROCAS.get(ficheiro, []):
        if texto.count(antigo) != n:
            raise AssertionError(('Ler a cidade, cartaz', ficheiro, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def desfazer(texto, ficheiro):
    for antigo, novo, n in reversed(TROCAS.get(ficheiro, [])):
        if texto.count(novo) != n:
            raise AssertionError(('Ler a cidade, cartaz (desfazer)', ficheiro, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def alinhar(texto, ficheiro):
    """Para bases que mudam com o tempo (git merge-base HEAD origin/main): se a base já traz esta camada (cada «novo» com a
    contagem exata e nenhum «antigo»), fica como está; senão, recebe-a com contagem exata. Um estado misto falha."""
    trocas = TROCAS.get(ficheiro, [])
    if trocas and all(texto.count(novo) == n and antigo not in texto for antigo, novo, n in trocas):
        return texto
    return aplicar(texto, ficheiro)
