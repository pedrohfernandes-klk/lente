"""08/11/2026: decisões 153, 162 e 176 (pedido lente-3, créditos atrás do «i»). Manifesto fechado das trocas literais que levam
o main de fec58ae à versão com o crédito atrás do «i» nas famílias L14 a L19 do plano (plano-creditos-i-20261105.md): passos e
casos da Cidadania (fig-cid), cartões com span.fr-cred (narrativas, casos da Cidadania, «Como se investiga», projetos, caderno,
Ética, Estética, fachada, gigantes, vozes e sidequests), retratos de Butler e Singer, cartões das vozes com vz-fig (25 de Abril, nos
dois lados, Warhol e Paula Rego), fotografias de «Ler a cidade» (span.fa-cred) e portas do portal da Cidadania, que deixa a linha
agregada dos créditos; e, fora da tabela, com a mesma estrutura, as duas imagens do passo 02 de «Como se investiga» e o retrato
de Oscar Wilde no passo 01 dos Direitos (tools/trocas/creditos-i-lente3-20261108.json). Nas páginas sem gerador, o manifesto é a
própria mudança; no gerador das correções do M2 (tools/cidadania_m2_correcoes.py), regista o que passou a escrever.

Onde o HTML vive dentro dos JSON dos cartões, o manifesto escreve-o em HTML corrido e tools/creditos_i.py trata o escape (as
aspas e as barras); aqui as trocas chegam já na forma literal do ficheiro, como nas outras camadas. Os testes que comparam com
bases antigas aplicam-no (ou desfazem-no) como a camada mais recente, por cima da do pedido lente-2, com contagem exata, sem aceitar
mais nada."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import creditos_i  # noqa: E402

MANIFESTO = creditos_i.ler_manifesto()
TROCAS = creditos_i.literais(MANIFESTO)


def aplicar(texto, ficheiro):
    return creditos_i.aplicar(texto, TROCAS.get(ficheiro, []), 'créditos i, lente-3 ' + ficheiro)


def desfazer(texto, ficheiro):
    return creditos_i.desfazer(texto, TROCAS.get(ficheiro, []), 'créditos i, lente-3 ' + ficheiro)


def alinhar(texto, ficheiro):
    """Para bases que mudam com o tempo (git merge-base HEAD origin/main): se a base já traz esta camada (cada «novo» com a
    contagem exata e nenhum «antigo» fora de um «novo»), fica como está; senão, recebe-a com contagem exata. Um estado misto
    falha."""
    return creditos_i.alinhar(texto, TROCAS.get(ficheiro, []), 'créditos i, lente-3 ' + ficheiro)
