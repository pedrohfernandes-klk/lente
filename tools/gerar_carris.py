"""02/11/2026: elétrico e agulha, desenho vetorial original. Semente fixa; --verificar confere SVG e integração.
Não reconstitui uma rua nem um veículo com número de carreira. Não altera os textos, ligações ou progresso da página.
05/11/2026: decisão 142 (docente). Passa a colagem de fotografia e traço: o elétrico 260 da Graça no Rossio
(Eduardo Alexandre Cunha, entre 1906 e 1914, domínio público) e, por cima, as duas vias, a agulha e a alavanca.
"""
from pathlib import Path

FOTO='justica/rossio-eletrico-260.webp'
# 05/11/2026: decisão 142 (docente, proposta B). A fotografia é a do Commons «CCFL260(porAlexCunha).jpg», na miniatura
# padrão de 1920 px: recorte (560, 780, 1900, 1380), cinzentos com autocontraste (1 %) e contraste ×1,08, depois tinta
# (34, 30, 26) e papel (243, 242, 238), WebP qualidade 80. O ficheiro fica no repositório e --verificar confere-lhe o SHA-256.
FOTO_SHA256='a4d78d9948874b581a3d53e89bbb6d854839f7b8d2df2ef8e9ae80eda858dc55'
W,H=1340,600

def cena(href='../../assets/'+FOTO):
    """Colagem: a fotografia do Rossio (elétrico 260 a vir de frente e, no chão, a via que se divide em duas)
    e, por cima, a traço, as duas vias que saem da agulha, a marca da agulha e a alavanca. Ninguém está na via.
    As coordenadas são as da fotografia recortada (1340 × 600); a cena alarga-se 660 de cada lado."""
    import random
    rng=random.Random(20261105)
    # A cena é mais larga do que a fotografia (de -660 a 2000): no telemóvel só se vê a fotografia; no computador,
    # a fotografia fica ao centro e esbate-se para o papel, com a calçada e o fio do elétrico desenhados à volta.
    a=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-660 0 {W+1320} {H}" preserveAspectRatio="xMidYMin slice" focusable="false">',
       '<defs><linearGradient id="jc-esbate" x1="0" x2="1"><stop offset="0" stop-color="var(--jc-esbate,#f3f2ee)"/><stop offset=".12" stop-color="var(--jc-esbate,#f3f2ee)" stop-opacity="0"/><stop offset=".8" stop-color="var(--jc-esbate,#f3f2ee)" stop-opacity="0"/><stop offset="1" stop-color="var(--jc-esbate,#f3f2ee)"/></linearGradient></defs>',
       '<g class="jc-traco" fill="none" stroke="currentColor" stroke-linecap="round">']
    # Calçada a traço nas margens, com semente fixa (pedras irregulares, só fora da fotografia).
    a.append('<g stroke-width="1.1" opacity=".22">')
    for y in range(330,600,22):
        for x in range(-660,2000,36):
            xx=x+(18 if (y//22)%2 else 0)+rng.uniform(-3,3)
            if -40<xx<W+10: continue
            a.append(f'<path d="M{xx:.1f} {y+rng.uniform(-2,2):.1f}h30m-30 0v15"/>')
    a.append('</g><path d="M-660 34H2000" stroke-width="1.4" opacity=".45"/></g>')
    a+=['<g class="jc-eletrico">',
       f'<image class="jc-foto" href="{href}" width="{W}" height="{H}"/>',
       f'<rect width="{W}" height="{H}" fill="url(#jc-esbate)"/>',
       # O elétrico 260 da Graça, na fotografia, marcado a tracejado.
       '<path class="jc-alvo" d="M490 66h148v156h-148z" fill="none" stroke="currentColor" stroke-width="2.5" stroke-dasharray="6 7" opacity=".75"/>',
       '<g fill="none" stroke-linecap="round" stroke-linejoin="round">',
       # As duas vias possíveis, a pontilhado: nenhuma é escolhida.
       '<path class="jc-via jc-via-a" d="M568 225C576 300 584 350 591 385C606 440 622 480 641 525C664 570 690 620 716 655" stroke="var(--jc-terra,#a84939)" stroke-width="7" stroke-dasharray="1 17"/>',
       '<path class="jc-via jc-via-b" d="M581 225C606 280 628 320 656 355C700 402 748 440 796 465C860 500 920 540 976 565C1040 596 1100 620 1146 635" stroke="var(--jc-terra,#a84939)" stroke-width="7" stroke-dasharray="1 17"/>',
       # A agulha: as duas lâminas onde a via se divide.
       '<path class="jc-agulha" d="M586 352l14 16M604 350l12 14" stroke="currentColor" stroke-width="3"/>',
       # A alavanca, neutra, ao lado da via.
       '<g class="jc-alavanca" stroke="currentColor" stroke-width="4"><path d="M712 368L770 368L784 382L726 382Z" fill="var(--jc-papel,#f3f2ee)"/><path d="M748 368L730 276"/><circle cx="728" cy="266" r="11" fill="var(--jc-papel,#f3f2ee)"/><path d="M712 375L660 375" stroke-width="2.5" stroke-dasharray="4 6"/></g>',
       '</g></g></svg>']
    return '\n'.join(a)+'\n'


import argparse
import re
ROOT=Path(__file__).resolve().parents[1]
DESTINO=ROOT/'assets/carris-eletrico.svg'
PAGINA=ROOT/'olhar-e-decidir/justica/index.html'
CREDITO=('Fotografia: elétrico 260 da Graça no Rossio, Lisboa, entre 1906 e 1914, de Eduardo Alexandre Cunha (Arquivo Municipal de Lisboa; domínio público, '
         '<a href="https://commons.wikimedia.org/wiki/File:CCFL260(porAlexCunha).jpg">Wikimedia Commons</a>). '
         'Por cima, a traço, as duas vias que saem da agulha e a alavanca. Grafismo gerado com recurso a IA, EPI, 2026. Duas vias possíveis, sem desfecho.')

def instalar(texto):
    desenho='<div class="jc-fundo" aria-hidden="true" data-fundo="jc" data-fundo-ciclo="36">'+cena().rstrip()+'</div>'
    texto,n=re.subn(r'<div class="jc-fundo"[^>]*>.*?</svg></div>',lambda _:desenho,texto,flags=re.S)
    assert n==1, 'Esperava-se uma só faixa da Justiça'
    credito='<p class="jc-credito">'+CREDITO+' <button type="button" class="fundo-botao" data-fundo-botao="jc" hidden>Parar o desenho</button></p>'
    texto,n=re.subn(r'<p class="jc-credito">.*?</p>',lambda _:credito,texto,flags=re.S)
    assert n==1, 'Esperava-se um só crédito'
    texto,n=re.subn(r'assets/fundo-carris.css[?]v=[^" ]+', 'assets/fundo-carris.css?v=20261105-2',texto)
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
    args=ap.parse_args();svg=cena(FOTO);pagina=PAGINA.read_text('utf-8');gerada=instalar(pagina)
    assert len(svg.encode('utf-8'))<120_000
    if args.verificar:
        assert DESTINO.read_text('utf-8')==svg, 'SVG diferente do gerador'
        assert pagina==gerada, 'Integração da faixa diferente do gerador'
        import hashlib
        assert hashlib.sha256((ROOT/'assets'/FOTO).read_bytes()).hexdigest()==FOTO_SHA256, 'Fotografia diferente da registada'
        print('Conferidos: SVG determinístico e faixa da Justiça')
    else:
        DESTINO.write_text(svg,'utf-8',newline='\n')
        PAGINA.write_text(gerada,'utf-8',newline='\n')
        print('Gerado:',DESTINO.name,len(svg.encode('utf-8')),'bytes')

if __name__=='__main__':main()
