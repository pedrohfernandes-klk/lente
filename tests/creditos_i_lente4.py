"""08/11/2026: decisões 153 e 176 (pedido lente-4, créditos atrás do «i»). Manifesto fechado das trocas literais que levam o main
de e0c55de à versão com o «i» visível na projeção e com o crédito das missões de «Ler a cidade» atrás do «i»
(tools/trocas/creditos-i-lente4-20261108.json): na peça comum (assets/info-i.css), só a regra da projeção, que tirava o fundo e o
halo a todos os «i» (também ao aberto e ao do canto, pousado na fotografia); em cidade/index.html, os dez cartões das missões com
span.cr passam a div.missao-i, com o cartão e o «i» lado a lado (o «i» fora da ligação), o estilo do cartão com «i» fica no lugar da
regra do span.cr, a gaveta de cada lugar copia o cartão com o seu «i» e o filtro esconde o conjunto.

Os testes que comparam com bases antigas aplicam-no (ou desfazem-no) como a camada mais recente, por cima da do pedido lente-3, com
contagem exata, sem aceitar mais nada. O manifesto aplica-se, desfaz-se e confere-se com tools/creditos_i.py --manifesto."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import creditos_i  # noqa: E402

CAMINHO = ROOT / 'tools/trocas/creditos-i-lente4-20261108.json'
MANIFESTO = creditos_i.ler_manifesto(CAMINHO)
TROCAS = creditos_i.literais(MANIFESTO)


def aplicar(texto, ficheiro):
    return creditos_i.aplicar(texto, TROCAS.get(ficheiro, []), 'créditos i, lente-4 ' + ficheiro)


def desfazer(texto, ficheiro):
    return creditos_i.desfazer(texto, TROCAS.get(ficheiro, []), 'créditos i, lente-4 ' + ficheiro)


def alinhar(texto, ficheiro):
    """Para bases que mudam com o tempo (git merge-base HEAD origin/main): se a base já traz esta camada (cada «novo» com a
    contagem exata e nenhum «antigo» fora de um «novo»), fica como está; senão, recebe-a com contagem exata. Um estado misto
    falha."""
    return creditos_i.alinhar(texto, TROCAS.get(ficheiro, []), 'créditos i, lente-4 ' + ficheiro)
