#!/usr/bin/env python3
"""01/11/2026: aplica ou verifica as trocas literais do primeiro lote de conteúdos.

As páginas antigas guardam os bancos no próprio HTML. Segue o formato de
tools/trocas: ocorrências exatas, aplicação idempotente e nenhuma geração de
Cidadania ou das entradas do Laboratório. --verificar não escreve.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'tools/trocas/conteudos-lote1-20261101.json'


def aplicar(verificar=False):
    pending = {}
    for e in json.loads(DATA.read_text('utf-8')):
        p = ROOT / e['ficheiro']
        s = pending.get(p, p.read_text('utf-8'))
        old, new, n = e['antigo'], e['novo'], e['ocorrencias']
        if s.count(new) == n and old not in s:
            continue
        if verificar or s.count(old) != n:
            raise ValueError(f"Troca não confere: {e['ficheiro']}: {e['local']}")
        pending[p] = s.replace(old, new)
    # Só escreve depois de conferir o lote completo.
    for p, s in pending.items():
        p.write_text(s, 'utf-8')
    print(f'Conteúdos: {len(pending)} páginas aplicadas; lote conferido.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--verificar', action='store_true')
    aplicar(ap.parse_args().verificar)
