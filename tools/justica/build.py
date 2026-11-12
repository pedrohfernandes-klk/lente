"""Regeneração literal dos bancos publicados, sem transcrições no repositório."""
import argparse
import json
import os
from pathlib import Path
from validar import extrair_citacoes, conferir_legendas, validar_banco

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]


def gerar(meta):
    numero = meta['numero']
    banco = (AQUI / f'bancos/licao-{numero}.json').read_text('utf-8').rstrip('\n')
    json.loads(banco)  # Rejeitar um banco inválido antes de escrever.
    molde = (AQUI / f'moldes/licao-{numero}.html').read_text('utf-8')
    if molde.count('@@ITENS@@') != 1:
        raise ValueError('O molde deve ter exatamente um lugar para os itens.')
    return molde.replace('@@ITENS@@', banco)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verificar', action='store_true')
    parser.add_argument('--legendas', action='store_true', help='Conferir localmente com JUSTICA_LEGENDAS.')
    args = parser.parse_args()
    manifesto = json.loads((AQUI / 'licoes.json').read_text('utf-8'))
    erros = []
    for meta in manifesto:
        numero = meta['numero']
        itens = json.loads((AQUI / f'bancos/licao-{numero}.json').read_text('utf-8'))
        erros.extend(validar_banco(itens, numero, meta['molde_novo'], meta.get('formato_curto', False), meta.get('formato_guiado', False)))
        pagina = RAIZ / f'olhar-e-decidir/justica/licao-{numero}/index.html'
        gerada = gerar(meta)
        if args.verificar:
            if pagina.read_text('utf-8') != gerada:
                erros.append(f'L{numero}: HTML diferente da regeneração')
        elif not erros:
            pagina.write_text(gerada, 'utf-8', newline='\n')
    citacoes = extrair_citacoes(AQUI)
    if citacoes != json.loads((AQUI / 'citacoes.json').read_text('utf-8')):
        erros.append('O manifesto de citações difere dos bancos.')
    if args.legendas:
        caminho = os.environ.get('JUSTICA_LEGENDAS')
        if not caminho:
            parser.error('Definir JUSTICA_LEGENDAS com a pasta privada das legendas.')
        erros.extend(conferir_legendas(citacoes, Path(caminho)))
    if erros:
        raise SystemExit('\n'.join(erros))
    print(f'{len(manifesto)} lições verificadas; {len(citacoes)} citações no manifesto.')


if __name__ == '__main__':
    main()
