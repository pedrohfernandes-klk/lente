"""05/11/2026: decisão 146 (discussões em turma, trabalhos individuais). Manifesto fechado das trocas literais
[antigo, novo, contagem] que levam cada ficheiro do main de 1e21ab2 à versão da decisão; os testes que comparam com
bases antigas aplicam-no (ou desfazem-no) com contagem exata, sem aceitar mais nada."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# 05/11/2026: decisão 154 (os exercícios fazem-se sozinho). Segunda camada, no mesmo pedido, por cima da 146: o seu manifesto
# leva a versão da decisão 146 à da 154, com as mesmas regras (trocas literais, contagem exata, reversíveis). As funções
# aplicam as camadas por ordem e desfazem-nas pela ordem inversa; TROCAS junta as duas, só para saber que ficheiros mudam.
CAMADAS = [
    ('decisão 146', json.loads((ROOT / 'tools/trocas/grupos-146-20261105.json').read_text(encoding='utf-8'))),
    ('decisão 154', json.loads((ROOT / 'tools/trocas/autonomia-154-20261105.json').read_text(encoding='utf-8'))),
]
TROCAS = {}
for _nome, _camada in CAMADAS:
    for _ficheiro, _lista in _camada.items():
        TROCAS.setdefault(_ficheiro, []).extend(_lista)


def _aplicar(texto, ficheiro, nome, camada):
    for antigo, novo, n in camada.get(ficheiro, []):
        if texto.count(antigo) != n:
            raise AssertionError((nome, ficheiro, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def aplicar(texto, ficheiro):
    for nome, camada in CAMADAS:
        texto = _aplicar(texto, ficheiro, nome, camada)
    return texto


def desfazer(texto, ficheiro):
    for nome, camada in reversed(CAMADAS):
        for antigo, novo, n in reversed(camada.get(ficheiro, [])):
            if texto.count(novo) != n:
                raise AssertionError((nome + ' (desfazer)', ficheiro, novo[:80]))
            texto = texto.replace(novo, antigo)
    return texto


def alinhar(texto, ficheiro):
    """Para bases que mudam com o tempo (origin/main, merge-base): antes da fusão a base ainda tem cada «antigo» com a
    contagem exata e recebe as trocas; depois da fusão já tem cada «novo» com a contagem exata e fica como está.
    Qualquer outro estado falha. Vale camada a camada."""
    # 05/11/2026: decisão 154, em todo o sítio. Depois da fusão deste pedido, a base já traz as duas camadas e, como a 154
    # reescreve textos que a 146 já tinha trocado (por exemplo «Rever em turma» passa a «Rever»), o «novo» da 146 pode já
    # não estar lá. Conta como fundida, e fica como está, só a base que, desfeitas as camadas pela ordem inversa (cada
    # «novo» com a contagem exata), volta a dar o mesmo texto quando se reaplicam; qualquer outro estado segue as regras de
    # cima, camada a camada.
    try:
        if aplicar(desfazer(texto, ficheiro), ficheiro) == texto:
            return texto
    except AssertionError:
        pass
    for nome, camada in CAMADAS:
        trocas = camada.get(ficheiro, [])
        if all(texto.count(antigo) == n for antigo, novo, n in trocas):
            texto = _aplicar(texto, ficheiro, nome, camada)
        elif not all(texto.count(novo) == n for antigo, novo, n in trocas):
            raise AssertionError((nome + ' (base em estado misto)', ficheiro))
    return texto
