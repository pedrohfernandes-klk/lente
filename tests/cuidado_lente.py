"""08/11/2026: decisão 152 («cuidado em todas as lições»), pedido cuidado-lente. Manifesto fechado das trocas literais
[antigo, novo, contagem] que levam o main de a99d2d4 à versão com os achados confirmados da varredura de 6/11
(tools/trocas/cuidado-lente-20261108.json): tabelas onde havia itens paralelos (Justiça 1 e 2, Aplicar, oficinas do
Laboratório e, pelos geradores, as sessões 02, 03 e 08 do M2), listas onde havia enumerações, referências e números que não se
partem entre linhas (espaço sem quebra U+00A0 e junção U+2060), as grelhas que partiam palavras a 375 px e a folha da tabela de
apoio (assets/apoio-tabela.css) nas páginas que a usam. Os testes que comparam com bases antigas aplicam-no (ou desfazem-no)
como a camada mais recente, por cima da do pedido cidade-cartaz-lente, com contagem exata, sem aceitar mais nada."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TROCAS = json.loads((ROOT / 'tools/trocas/cuidado-lente-20261108.json').read_text(encoding='utf-8'))


def aplicar(texto, ficheiro):
    for antigo, novo, n in TROCAS.get(ficheiro, []):
        if texto.count(antigo) != n:
            raise AssertionError(('cuidado em todas as lições', ficheiro, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def desfazer(texto, ficheiro):
    for antigo, novo, n in reversed(TROCAS.get(ficheiro, [])):
        if texto.count(novo) != n:
            raise AssertionError(('cuidado em todas as lições (desfazer)', ficheiro, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def alinhar(texto, ficheiro):
    """Para bases que mudam com o tempo (git merge-base HEAD origin/main): se a base já traz esta camada (cada «novo» com a
    contagem exata e nenhum «antigo»), fica como está; senão, recebe-a com contagem exata. Um estado misto falha."""
    trocas = TROCAS.get(ficheiro, [])
    if trocas and all(texto.count(novo) == n and antigo not in texto for antigo, novo, n in trocas):
        return texto
    return aplicar(texto, ficheiro)
