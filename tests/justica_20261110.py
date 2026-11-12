"""Continuação de Justiça: alterações exatas às três páginas de navegação existentes."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import creditos_i
TROCAS=json.loads((Path(__file__).parent/'fixtures/justica-20261110.json').read_text('utf-8'))
CURTAS=json.loads((Path(__file__).parent/'fixtures/justica-curta-20261110.json').read_text('utf-8'))
# 11/11/2026: terceira camada exata. As lições 4 a 13 passam ao formato guiado; mudam a descrição no índice e a secção
# «licoes-4-13» do guia docente (tests/fixtures/justica-guiada-20261111.json, sobre a base 70ded68).
GUIADAS=json.loads((Path(__file__).parent/'fixtures/justica-guiada-20261111.json').read_text('utf-8'))
def aplicar(texto,ficheiro):
    anterior=creditos_i.aplicar(texto,TROCAS.get(ficheiro,[]),'Justiça '+ficheiro)
    anterior=creditos_i.aplicar(anterior,CURTAS.get(ficheiro,[]),'Justiça curta '+ficheiro)
    return creditos_i.aplicar(anterior,GUIADAS.get(ficheiro,[]),'Justiça guiada '+ficheiro)
def desfazer(texto,ficheiro):
    anterior=creditos_i.desfazer(texto,GUIADAS.get(ficheiro,[]),'Justiça guiada '+ficheiro)
    anterior=creditos_i.desfazer(anterior,CURTAS.get(ficheiro,[]),'Justiça curta '+ficheiro)
    return creditos_i.desfazer(anterior,TROCAS.get(ficheiro,[]),'Justiça '+ficheiro)
def alinhar(texto,ficheiro):
    guiadas=GUIADAS.get(ficheiro,[])
    if guiadas and all(texto.count(novo)==quantidade for _,novo,quantidade in guiadas):
        return aplicar(desfazer(texto,ficheiro),ficheiro)
    return creditos_i.alinhar(_alinhar_ate_curta(texto,ficheiro),guiadas,'Justiça guiada '+ficheiro)
def _aplicar_ate_curta(texto,ficheiro):
    return creditos_i.aplicar(creditos_i.aplicar(texto,TROCAS.get(ficheiro,[]),'Justiça '+ficheiro),CURTAS.get(ficheiro,[]),'Justiça curta '+ficheiro)
def _desfazer_ate_curta(texto,ficheiro):
    return creditos_i.desfazer(creditos_i.desfazer(texto,CURTAS.get(ficheiro,[]),'Justiça curta '+ficheiro),TROCAS.get(ficheiro,[]),'Justiça '+ficheiro)
def _alinhar_ate_curta(texto,ficheiro):
    curtas=CURTAS.get(ficheiro,[])
    if curtas and all(texto.count(novo)==quantidade for _,novo,quantidade in curtas):
        return _aplicar_ate_curta(_desfazer_ate_curta(texto,ficheiro),ficheiro)
    anterior=creditos_i.alinhar(texto,TROCAS.get(ficheiro,[]),'Justiça '+ficheiro)
    return creditos_i.alinhar(anterior,curtas,'Justiça curta '+ficheiro)
