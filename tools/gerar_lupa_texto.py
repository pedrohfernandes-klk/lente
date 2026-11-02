#!/usr/bin/env python3
"""02/11/2026: decisão 139 (docente: «maiores e mais bem feitos»). A página de texto miúdo por baixo da lupa da entrada do Lente.

Gera assets/lupa-texto.svg: um bloco de 1200 × 480 em letra serifada de 11 px, com linhas mais compridas do que o bloco (o
desenho corta-as à direita, como uma página vista de perto; nada de espaçar letras para justificar), feito só da
epígrafe de _Ensaio sobre a Cegueira_, de José Saramago (1995): «Se podes olhar, vê. Se podes ver, repara.» De longe é uma
mancha de texto; a lupa amplia-a e a frase lê-se. Determinístico: python3 tools/gerar_lupa_texto.py --verificar.
"""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESTINO = ROOT / 'assets/lupa-texto.svg'
FRASE = 'Se podes olhar, vê. Se podes ver, repara.'
LARGURA, ALTURA = 1200, 480
MARGEM = 6
CORPO = 11          # px
ENTRELINHA = 15     # px
POR_LINHA = 277     # carateres por linha: sempre mais do que cabe em 1200 px, e não é múltiplo da frase


def linhas():
    palavras = (FRASE + ' ') * 400
    palavras = palavras.split()
    saida, atual, k = [], [], 0
    total = (ALTURA - MARGEM) // ENTRELINHA
    for p in palavras:
        if atual and len(' '.join(atual + [p])) > POR_LINHA:
            saida.append(' '.join(atual))
            atual = []
            if len(saida) == total:
                break
        atual.append(p)
    return saida


def svg():
    corpo = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGURA} {ALTURA}" width="{LARGURA}" height="{ALTURA}">',
             '<!-- Grafismo gerado com recurso a IA, EPI, 2026. Texto: epígrafe de Ensaio sobre a Cegueira, de José Saramago (1995). '
             'Gerado por tools/gerar_lupa_texto.py. -->',
             f'<g font-family="Georgia,\'Times New Roman\',serif" font-size="{CORPO}" fill="#1c1b19" fill-opacity=".72">']
    for n, linha in enumerate(linhas()):
        y = MARGEM + CORPO + n * ENTRELINHA
        corpo.append(f'<text x="{MARGEM}" y="{y}">{linha}</text>')
    corpo.append('</g></svg>')
    return '\n'.join(corpo) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--verificar', action='store_true')
    texto = svg()
    if ap.parse_args().verificar:
        assert DESTINO.read_text('utf-8') == texto, 'assets/lupa-texto.svg não corresponde ao gerador'
        print('Conferido:', DESTINO.relative_to(ROOT))
    else:
        DESTINO.write_text(texto, 'utf-8', newline='\n')
        print('Gerado:', DESTINO.relative_to(ROOT), len(texto.encode()), 'bytes')


if __name__ == '__main__':
    main()
