"""Renomeações fechadas do #107 para comparações com bases históricas."""
import json
import subprocess
from functools import lru_cache
from pathlib import Path

TROCAS = json.loads((Path(__file__).parent / 'fixtures/cidadania-nomes-20261103.json').read_text(encoding='utf-8'))


@lru_cache(maxsize=None)
def contagens_finais(ficheiro):
    """Conta também os usos que já existiam na base imutável anterior ao #107."""
    raiz = Path(__file__).resolve().parents[1]
    texto = subprocess.check_output(
        ['git', 'show', f'349d2457e1f056b69c6dda550aace2a6f5377051:{ficheiro}'], cwd=raiz
    ).decode('utf-8')
    for antigo, novo, quantidade in TROCAS[ficheiro]:
        assert texto.count(antigo) == quantidade, ficheiro
        texto = texto.replace(antigo, novo)
    return {novo: texto.count(novo) for _, novo, _ in TROCAS[ficheiro]}


def renomear(texto, ficheiro, inverter=False, base_ja_renomeada=False):
    binario = isinstance(texto, bytes)
    for antigo, novo, quantidade in TROCAS.get(ficheiro, []):
        if inverter:
            antigo, novo = novo, antigo
        if binario:
            antigo, novo = antigo.encode(), novo.encode()
        if base_ja_renomeada and texto.count(antigo) == 0:
            rotulo = novo.decode('utf-8') if binario else novo
            assert texto.count(novo) == contagens_finais(ficheiro)[rotulo], ficheiro
            continue
        assert texto.count(antigo) == quantidade, ficheiro
        texto = texto.replace(antigo, novo)
    return texto
