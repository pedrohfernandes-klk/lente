"""Continuação de Justiça: alterações exatas às três páginas de navegação existentes."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import creditos_i
TROCAS=json.loads((Path(__file__).parent/'fixtures/justica-20261110.json').read_text('utf-8'))
CURTAS=json.loads((Path(__file__).parent/'fixtures/justica-curta-20261110.json').read_text('utf-8'))
def aplicar(texto,ficheiro):
    anterior=creditos_i.aplicar(texto,TROCAS.get(ficheiro,[]),'Justiça '+ficheiro)
    return creditos_i.aplicar(anterior,CURTAS.get(ficheiro,[]),'Justiça curta '+ficheiro)
def desfazer(texto,ficheiro):
    anterior=creditos_i.desfazer(texto,CURTAS.get(ficheiro,[]),'Justiça curta '+ficheiro)
    return creditos_i.desfazer(anterior,TROCAS.get(ficheiro,[]),'Justiça '+ficheiro)
def alinhar(texto,ficheiro):
    curtas=CURTAS.get(ficheiro,[])
    if curtas and all(texto.count(novo)==quantidade for _,novo,quantidade in curtas):
        return aplicar(desfazer(texto,ficheiro),ficheiro)
    anterior=creditos_i.alinhar(texto,TROCAS.get(ficheiro,[]),'Justiça '+ficheiro)
    return creditos_i.alinhar(anterior,curtas,'Justiça curta '+ficheiro)
