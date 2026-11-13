"""13/11/2026: pedido temas-01-03-04. Os temas 01 («Justiça e vida em comum»), 03 («Histórias e criação») e 04 («Imagem, som e cidade»)
passam a ter página própria (justica-e-vida-em-comum/, historias-e-criacao/ e imagem-som-e-cidade/), escritas de raiz no molde da do
tema 02 (informacao/), e os cartões da entrada passam a abri-las.

Manifesto fechado das trocas literais [antigo, novo, contagem] que levam o main de 9a5e6e1 a esse estado
(tests/fixtures/temas-paginas-20261113.json): em index.html, o destino dos cartões 01, 03 e 04 e, no cartão 03, que conserva o id
inicio-narrativas, uma ligação à vista ao Laboratório antes da do Ideias (o destino antigo do cartão; a retoma guardada do aluno
continua a ter para onde ir); em mapa/index.html, as páginas dos quatro temas, pela ordem, no lugar da linha do tema 02. Nada é apagado
nem movido: olhar-e-decidir/, narrativas/ e cidade/ continuam ligadas no mapa e são a primeira ligação de «Ver tudo neste tema» em cada
página nova.

Os testes que comparam com bases antigas aplicam-no (ou desfazem-no) como a camada mais recente, por cima da da entrada em quatro temas
(tests/entrada_temas_20261112.py), com contagem exata, sem aceitar mais nada (tests/creditos_i_lente3.py)."""
import json
import sys
from pathlib import Path
# tools/ no caminho, como em tests/justica_20261110.py, para o módulo abrir também quando um teste corre sozinho.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import creditos_i  # noqa: E402
TROCAS = json.loads((Path(__file__).parent / 'fixtures/temas-paginas-20261113.json').read_text('utf-8'))
def aplicar(texto, ficheiro):
    return creditos_i.aplicar(texto, TROCAS.get(ficheiro, []), 'páginas dos temas ' + ficheiro)
def desfazer(texto, ficheiro):
    return creditos_i.desfazer(texto, TROCAS.get(ficheiro, []), 'páginas dos temas ' + ficheiro)
def alinhar(texto, ficheiro):
    return creditos_i.alinhar(texto, TROCAS.get(ficheiro, []), 'páginas dos temas ' + ficheiro)
