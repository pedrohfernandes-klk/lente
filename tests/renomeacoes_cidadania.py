"""Renomeações fechadas do #107 para comparações com bases históricas."""
import json
from pathlib import Path

TROCAS = json.loads((Path(__file__).parent / 'fixtures/cidadania-nomes-20261103.json').read_text(encoding='utf-8'))


def renomear(texto, ficheiro, inverter=False, base_ja_renomeada=False):
    binario = isinstance(texto, bytes)
    for antigo, novo, quantidade in TROCAS.get(ficheiro, []):
        if inverter:
            antigo, novo = novo, antigo
        if binario:
            antigo, novo = antigo.encode(), novo.encode()
        if base_ja_renomeada and texto.count(antigo) == 0:
            assert texto.count(novo) == quantidade, ficheiro
            continue
        assert texto.count(antigo) == quantidade, ficheiro
        texto = texto.replace(antigo, novo)
    return texto
