"""02/11/2026: elétrico e agulha, desenho vetorial original. Semente fixa; --verificar confere SVG e integração.
Não reconstitui uma rua nem um veículo com número de carreira. Não altera os textos, ligações ou progresso da página.
"""
from pathlib import Path
import random

def cena():
    rng=random.Random(20261102)
    a=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 440" preserveAspectRatio="xMidYMid slice" focusable="false">',
       '<defs><pattern id="jc-hachura" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M-1 7L7 -1" fill="none" stroke="currentColor" stroke-width=".7" opacity=".45"/></pattern></defs>',
       '<g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">']
    # Pavimento irregular, com semente fixa. A gravura não reconstitui um local real.
    a.append('<g stroke-width=".7" opacity=".18">')
    for y in range(264,438,20):
        for x in range(-20,1210,34):
            xx=x+(17 if (y//20)%2 else 0);dy=rng.uniform(-2,2)
            a.append(f'<path d="M{xx:.1f} {y+dy:.1f}h29m-29 0v14"/>')
    a.append('</g>')
    a.append('<g stroke-width="2"><path d="M0 318H710Q780 318 838 284L1200 88M0 354H730Q801 354 863 316L1200 130"/><path d="M704 318Q806 318 886 353L1200 430M730 354Q795 354 875 390L1080 440"/></g>')
    a.append('<g opacity=".45" stroke-width=".8">')
    for x in range(50,751,24):a.append(f'<path d="M{x} 310v52"/>')
    a.append('</g><g class="jc-agulha" stroke-width="3"><path d="M705 322L790 318M731 350L808 352"/></g>')
    # Agulha neutra e alavanca fixa: nenhum dos ramos é escolhido.
    a.append('<g class="jc-alavanca" stroke-width="2"><path d="M798 315V252L778 236M756 250h45l13 10h-48z" fill="var(--jc-papel,#f3f2ee)"/><path d="M778 245V157" stroke-width="5"/><circle cx="778" cy="150" r="9" fill="var(--jc-papel,#f3f2ee)"/><path d="M754 207Q778 187 802 207M764 247l-8 -36m35 36 9 -36"/><path d="M770 235h16m-16 5h16"/></g>')
    # Elétrico de Lisboa: caixa de madeira, tejadilho arredondado, janelas altas e trólei.
    a.append('<g class="jc-eletrico" stroke-width="2"><g transform="translate(330 116)">')
    a.append('<path d="M28 24Q42 9 77 7H224Q246 7 263 26L280 42V177L247 200H42L10 177V48Z" fill="var(--jc-papel,#f3f2ee)"/>')
    a.append('<path d="M10 48L46 31H244L280 42M46 31V188M244 31V198M10 158L46 177H244L280 158M46 116H244M48 171H243M12 161l32 17M12 168l32 17M12 175l32 17"/>')
    a.append('<path d="M28 24Q50 12 77 12H224Q245 13 263 26L244 31H46Z" fill="url(#jc-hachura)"/>')
    for x in [57,94,131,168,205]:
        a.append(f'<path d="M{x} 43h27v61h-27zM{x+3} 47h21v53h-21z"/><path d="M{x+4} 87l17 -28" opacity=".3"/>')
    a.append('<path d="M255 48l15 4v50l-15 8zM17 54l20 -10v65l-20 -9zM255 119l15 -7v38l-15 9z"/><path d="M56 126h176v36H56z" fill="url(#jc-hachura)"/><path d="M58 132h173M58 156h173"/>')
    a.append('<path d="M60 188h170l13 12H47z" fill="currentColor"/><g fill="var(--jc-papel,#f3f2ee)"><ellipse cx="78" cy="194" rx="14" ry="10"/><ellipse cx="214" cy="194" rx="14" ry="10"/><circle cx="266" cy="135" r="7"/></g><path d="M65 194h26m110 0h26M252 170l27 -14M253 178l26 -14M254 187l25 -14"/>')
    a.append('<path d="M131 8L206 -55l8 3L144 9"/><circle cx="211" cy="-56" r="4"/><path d="M-330 -56H870" stroke-width=".8" opacity=".3"/><path d="M72 16H218M68 20H228M64 24H235" stroke-width=".7"/>')
    a.append('</g></g>')
    a.append('</g></svg>')
    return '\n'.join(a)+'\n'


import argparse
import re
ROOT=Path(__file__).resolve().parents[1]
DESTINO=ROOT/'assets/carris-eletrico.svg'
PAGINA=ROOT/'olhar-e-decidir/justica/index.html'
CREDITO='Grafismo gerado com recurso a IA, EPI, 2026. Um elétrico de Lisboa aproxima-se da agulha e para antes dela. Duas vias possíveis, sem desfecho.'

def instalar(texto):
    desenho='<div class="jc-fundo" aria-hidden="true" data-fundo="jc" data-fundo-ciclo="36">'+cena().rstrip()+'</div>'
    texto,n=re.subn(r'<div class="jc-fundo"[^>]*>.*?</svg></div>',lambda _:desenho,texto,flags=re.S)
    assert n==1, 'Esperava-se uma só faixa da Justiça'
    credito='<p class="jc-credito">'+CREDITO+' <button type="button" class="fundo-botao" data-fundo-botao="jc" hidden>Parar o desenho</button></p>'
    texto,n=re.subn(r'<p class="jc-credito">.*?</p>',lambda _:credito,texto,flags=re.S)
    assert n==1, 'Esperava-se um só crédito'
    texto,n=re.subn(r'assets/fundo-carris.css[?]v=[^" ]+', 'assets/fundo-carris.css?v=20261102-3',texto)
    assert n==1, 'Esperava-se um só carregamento do CSS'
    # 03/11/2026: integra a gravura na abertura sem alterar os seus textos.
    if '<header class="jc-abertura">' not in texto:
        texto,n=re.subn(
            r'(<h1>Justiça.*?</h1>\s*<p class="lead">.*?</p>)\s*(<div class="jc-fundo".*?</svg></div>)',
            r'<header class="jc-abertura">\1\n\2</header>', texto, flags=re.S)
        assert n==1, 'Esperava-se uma abertura da Justiça'
    return texto

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--verificar',action='store_true')
    args=ap.parse_args();svg=cena();pagina=PAGINA.read_text('utf-8');gerada=instalar(pagina)
    assert len(svg.encode('utf-8'))<120_000
    if args.verificar:
        assert DESTINO.read_text('utf-8')==svg, 'SVG diferente do gerador'
        assert pagina==gerada, 'Integração da faixa diferente do gerador'
        print('Conferidos: SVG determinístico e faixa da Justiça')
    else:
        DESTINO.write_text(svg,'utf-8',newline='\n')
        PAGINA.write_text(gerada,'utf-8',newline='\n')
        print('Gerado:',DESTINO.name,len(svg.encode('utf-8')),'bytes')

if __name__=='__main__':main()
