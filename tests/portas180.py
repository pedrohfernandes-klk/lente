"""07/11/2026: decisão 180 (docente). As três portas do Laboratório (Observar, Treinar, Criar) não são passos de um método
com ordem. Trocas fechadas do manifesto tests/fixtures/portas-180-20261107.json, para as comparações com bases antigas:
no cartão do Laboratório da entrada do Lente, as portas perdem o número (01, 02, 03) e o «passo» e dizem o seu subtítulo;
nas três peças antigas que acabam o último percurso de uma porta (Duchamp, «O teste do colega» e a oficina do ateliê), o «a
seguir» («Passo seguinte» ou «No Ideias») passa a «As outras portas», com destino na entrada do Laboratório (#portas), como
o docente escolheu na nota à decisão 180. Cada troca tem contagem exata; qualquer outra diferença continua a falhar, como em
tests/menus163.py."""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
TROCAS = json.loads((R / 'tests/fixtures/portas-180-20261107.json').read_text(encoding='utf-8'))


def aplicar(texto, ficheiro):
    trocas = TROCAS['exato'].get(ficheiro, [])
    if not trocas:
        return texto
    for antigo, novo, quantidade in trocas:
        assert texto.count(antigo) == quantidade, ('decisão 180', ficheiro, antigo[:80])
        texto = texto.replace(antigo, novo)
    return texto
