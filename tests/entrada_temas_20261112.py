"""12/11/2026: pedido entrada-temas. A entrada do Lente passa a abrir por quatro temas de exploração (01 Justiça e vida em comum,
02 Informação e mundo digital, 03 Histórias e criação, 04 Imagem, som e cidade), com os acessos secundários («Ferramentas para
trabalhar», «A minha aula», Biblioteca e Área do docente) e a ligação a «Português e Exames»; o tema 02 tem página própria
(informacao/), escrita de raiz, e os outros três abrem, por agora, a área que já existe.

Manifesto fechado das trocas literais [antigo, novo, contagem] que levam o main de b8abe97 à entrada nova
(tests/fixtures/entrada-temas-20261112.json): em index.html, a descrição, a folha assets/temas.css no lugar de assets/praticar.css,
a frase do cabeçalho e o miolo (do acesso ao mapa até às ligações do rodapé); em mapa/index.html, as ligações que saíram da entrada
(as secções de «Praticar» e do catálogo do Laboratório) e a página do tema 02; em como/index.html, a frase que descrevia a entrada
antiga. Nada é apagado nem movido: os ids ferramentas, inicio-cidadania, inicio-narrativas e inicio-vozes continuam na entrada.

Os testes que comparam com bases antigas aplicam-no (ou desfazem-no) como a camada mais recente, por cima da da Justiça, com contagem
exata, sem aceitar mais nada (tests/creditos_i_lente3.py)."""
import json
import sys
from pathlib import Path
# 12/11/2026: tools/ no caminho, como em tests/justica_20261110.py, para o módulo abrir também quando um teste corre sozinho
# (licoes-qa.yml corre test_menus_163.py isolado).
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import creditos_i  # noqa: E402
TROCAS = json.loads((Path(__file__).parent / 'fixtures/entrada-temas-20261112.json').read_text('utf-8'))
def aplicar(texto, ficheiro):
    return creditos_i.aplicar(texto, TROCAS.get(ficheiro, []), 'entrada em temas ' + ficheiro)
def desfazer(texto, ficheiro):
    return creditos_i.desfazer(texto, TROCAS.get(ficheiro, []), 'entrada em temas ' + ficheiro)
def alinhar(texto, ficheiro):
    return creditos_i.alinhar(texto, TROCAS.get(ficheiro, []), 'entrada em temas ' + ficheiro)
