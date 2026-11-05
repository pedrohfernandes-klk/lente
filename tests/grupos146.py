"""05/11/2026: decisão 146 (discussões em turma, trabalhos individuais). Manifesto fechado das trocas literais
[antigo, novo, contagem] que levam cada ficheiro do main de 1e21ab2 à versão da decisão; os testes que comparam com
bases antigas aplicam-no (ou desfazem-no) com contagem exata, sem aceitar mais nada."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TROCAS = json.loads((ROOT / 'tools/trocas/grupos-146-20261105.json').read_text(encoding='utf-8'))


def aplicar(texto, ficheiro):
    for antigo, novo, n in TROCAS.get(ficheiro, []):
        if texto.count(antigo) != n:
            raise AssertionError(('decisão 146', ficheiro, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def desfazer(texto, ficheiro):
    for antigo, novo, n in reversed(TROCAS.get(ficheiro, [])):
        if texto.count(novo) != n:
            raise AssertionError(('decisão 146 (desfazer)', ficheiro, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def alinhar(texto, ficheiro):
    """Para bases que mudam com o tempo (origin/main, merge-base): antes da fusão a base ainda tem cada «antigo» com a
    contagem exata e recebe as trocas; depois da fusão já tem cada «novo» com a contagem exata e fica como está.
    Qualquer outro estado falha."""
    trocas = TROCAS.get(ficheiro, [])
    if all(texto.count(antigo) == n for antigo, novo, n in trocas):
        return aplicar(texto, ficheiro)
    if all(texto.count(novo) == n for antigo, novo, n in trocas):
        return texto
    raise AssertionError(('decisão 146 (base em estado misto)', ficheiro))
