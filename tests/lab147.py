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
