"""Revisão autorizada da entrada e dos exercícios, 10/11/2026."""
import json
from pathlib import Path
import creditos_i
TROCAS = json.loads((Path(__file__).parent / 'fixtures/praticar-20261110.json').read_text('utf-8'))
def aplicar(texto, ficheiro):
    return creditos_i.aplicar(texto, TROCAS.get(ficheiro, []), 'praticar ' + ficheiro)
def desfazer(texto, ficheiro):
    return creditos_i.desfazer(texto, TROCAS.get(ficheiro, []), 'praticar ' + ficheiro)
def alinhar(texto, ficheiro):
    return creditos_i.alinhar(texto, TROCAS.get(ficheiro, []), 'praticar ' + ficheiro)
