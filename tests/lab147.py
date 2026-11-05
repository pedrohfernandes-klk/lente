"""05/11/2026: decisão 147 (Laboratório sem o Português). Trocas fechadas do manifesto
tests/fixtures/lab-147-20261105.json, para as comparações com bases antigas: cada troca com contagem exata."""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
TROCAS = json.loads((R / 'tests/fixtures/lab-147-20261105.json').read_text(encoding='utf-8'))
RETIRADAS = [x['url'] for x in json.loads((R / 'assets/laboratorio/retiradas.json').read_text(encoding='utf-8'))['retiradas']]


def aplicar(texto, ficheiro):
    for antigo, novo, quantidade in TROCAS.get(ficheiro, []):
        assert texto.count(antigo) == quantidade, (ficheiro, antigo[:80])
        texto = texto.replace(antigo, novo)
    return texto


def alinhar(texto, ficheiro):
    """05/11/2026: para bases que mudam com o tempo (origin/main e git merge-base HEAD origin/main). Antes da fusão do #122
    a base ainda tem cada «antigo» com a contagem exata e recebe as trocas; depois da fusão já tem cada «novo» com a
    contagem exata e fica como está. Qualquer outro estado falha, como em grupos146.alinhar."""
    trocas = TROCAS.get(ficheiro, [])
    if all(texto.count(antigo) == n for antigo, novo, n in trocas):
        return aplicar(texto, ficheiro)
    # Uma troca que apaga (novo vazio) conta como feita quando o «antigo» já não aparece.
    if all((texto.count(novo) == n) if novo else (texto.count(antigo) == 0) for antigo, novo, n in trocas):
        return texto
    raise AssertionError(('decisão 147 (base em estado misto)', ficheiro))
