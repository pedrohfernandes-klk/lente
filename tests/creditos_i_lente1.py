"""07/11/2026: decisões 153, 176 e 177 (pedido lente-1, créditos atrás do «i»). Manifesto fechado das trocas literais
[antigo, novo, contagem] que levam a entrada (index.html), o índice do M2 e o percurso anterior do M1 do main de dc01487 à
versão com o «i» (tools/trocas/creditos-i-lente1-20261107.json). Os testes que comparam com bases antigas aplicam-no (ou
desfazem-no) como a camada mais recente, com contagem exata, sem aceitar mais nada."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TROCAS = json.loads((ROOT / 'tools/trocas/creditos-i-lente1-20261107.json').read_text(encoding='utf-8'))


def aplicar(texto, ficheiro):
    for antigo, novo, n in TROCAS.get(ficheiro, []):
        if texto.count(antigo) != n:
            raise AssertionError(('créditos i, lente-1', ficheiro, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def desfazer(texto, ficheiro):
    for antigo, novo, n in reversed(TROCAS.get(ficheiro, [])):
        if texto.count(novo) != n:
            raise AssertionError(('créditos i, lente-1 (desfazer)', ficheiro, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def alinhar(texto, ficheiro):
    """Para bases que mudam com o tempo (git merge-base HEAD origin/main): se a base já traz esta camada (cada «novo» com a
    contagem exata e nenhum «antigo»), fica como está; senão, recebe-a com contagem exata. Um estado misto falha."""
    trocas = TROCAS.get(ficheiro, [])
    if trocas and all(texto.count(novo) == n and antigo not in texto for antigo, novo, n in trocas):
        return texto
    return aplicar(texto, ficheiro)
