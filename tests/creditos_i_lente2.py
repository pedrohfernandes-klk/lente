"""08/11/2026: decisões 153, 162 e 176 (pedido lente-2, créditos atrás do «i»). Manifesto fechado das trocas literais
[antigo, novo, contagem] que levam o main de cc75fc6 à versão com o crédito atrás do «i» nas famílias L8 a L13 do plano
(plano-creditos-i-20261105.md): desenhos das lições 1 e 2 da Justiça, Ética e Estética, lições do motor único (piloto
congelado do M1 e «Ideias»), vídeos dessas lições, sessões do M2 e páginas do M1 que ainda levavam a ligação «Créditos»
(tools/trocas/creditos-i-lente2-20261108.json). Nas páginas sem gerador (Ética e Estética, piloto do M1), o manifesto é a
própria mudança; nas outras, regista o que os geradores passaram a escrever. Os testes que comparam com bases antigas
aplicam-no (ou desfazem-no) como a camada mais recente, por cima da do pedido cuidado-lente, com contagem exata, sem aceitar
mais nada."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TROCAS = json.loads((ROOT / 'tools/trocas/creditos-i-lente2-20261108.json').read_text(encoding='utf-8'))


def aplicar(texto, ficheiro):
    for antigo, novo, n in TROCAS.get(ficheiro, []):
        if texto.count(antigo) != n:
            raise AssertionError(('créditos i, lente-2', ficheiro, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def desfazer(texto, ficheiro):
    for antigo, novo, n in reversed(TROCAS.get(ficheiro, [])):
        if texto.count(novo) != n:
            raise AssertionError(('créditos i, lente-2 (desfazer)', ficheiro, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def alinhar(texto, ficheiro):
    """Para bases que mudam com o tempo (git merge-base HEAD origin/main): se a base já traz esta camada (cada «novo» com a
    contagem exata e nenhum «antigo»), fica como está; senão, recebe-a com contagem exata. Um estado misto falha."""
    trocas = TROCAS.get(ficheiro, [])
    # 08/11/2026: pedido lente-3. Em 36 trocas desta camada (a folha e o script da peça juntam-se a seguir a um script que já lá
    # estava), o «antigo» vem dentro do «novo»; depois da fusão no main (fec58ae), a base já traz a camada e o «antigo» continua lá,
    # dentro do «novo», e o teste do M1 (test_cidadania_m2_molde) falhava no main. Conta-se agora o «antigo» que fica fora de um
    # «novo»: tem de ser zero, como antes; cada «novo» continua com a contagem exata e um estado misto continua a falhar.
    if trocas and all(texto.count(novo) == n and texto.count(antigo) == sum(m * novo2.count(antigo) for _, novo2, m in trocas)
                      for antigo, novo, n in trocas):
        return texto
    return aplicar(texto, ficheiro)
