"""Camada visual fechada: conserva texto, destinos, scripts e dados das entradas."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = json.loads((ROOT/'tools/menus-acabamento-20261103.json').read_text('utf-8'))
MARK = ' data-menus-acabamento="20261103"'

MAP_OPEN = '<!-- menus-apoios --><details class="menu-apoios"><summary>Outros recursos do Laboratório</summary><div>'
MAP_CLOSE = '</div></details><!-- /menus-apoios -->'
COURSE = ' class="menu-curso-principal"'

def mapa(texto):
    texto = texto.replace(MAP_OPEN, '').replace(MAP_CLOSE, '').replace(COURSE, '')
    first = '<p class="map-open"><a href="https://pedrohfernandes-klk.github.io/lente/narrativas/fora-da-pagina/">Fora da página</a></p>'
    assert texto.count(first) == 1
    start = texto.index(first)
    end = texto.index('</section>', start)
    texto = texto[:start]+MAP_OPEN+texto[start:end]+MAP_CLOSE+texto[end:]
    course = '<a href="https://pedrohfernandes-klk.github.io/lente/narrativas/ideias/">'
    assert texto.count(course) == 1
    return texto.replace(course, '<a'+COURSE+course[2:], 1)

def instalar(texto, nome):
    if nome == 'mapa/index.html':
        texto = mapa(texto)
    prefixo = '../' * (len(Path(nome).parts)-1)
    link = '<link data-menus-acabamento-css rel="stylesheet" href="'+prefixo+'assets/menus-acabamento.css?v=20261103-1">'
    texto = re.sub(r'<link data-menus-acabamento-css[^>]*>', '', texto)
    texto = texto.replace(MARK, '')
    texto = texto.replace('<body', '<body'+MARK, 1)
    return texto.replace('</head>', link+'</head>', 1)

if __name__ == '__main__':
    for nome in PAGES:
        p = ROOT/nome
        p.write_bytes(instalar(p.read_text('utf-8'), nome).encode('utf-8'))
