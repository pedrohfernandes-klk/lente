"""Continuação de Justiça: alterações exatas às três páginas de navegação existentes."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import creditos_i
TROCAS=json.loads((Path(__file__).parent/'fixtures/justica-20261110.json').read_text('utf-8'))
def aplicar(texto,ficheiro):
    return creditos_i.aplicar(texto,TROCAS.get(ficheiro,[]),'Justiça '+ficheiro)
def desfazer(texto,ficheiro):
    return creditos_i.desfazer(texto,TROCAS.get(ficheiro,[]),'Justiça '+ficheiro)
def alinhar(texto,ficheiro):
    return creditos_i.alinhar(texto,TROCAS.get(ficheiro,[]),'Justiça '+ficheiro)
