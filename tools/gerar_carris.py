"""02/11/2026: elétrico e agulha, desenho vetorial original. Semente fixa; --verificar confere SVG e integração.
Não reconstitui uma rua nem um veículo com número de carreira. Não altera os textos, ligações ou progresso da página.
05/11/2026: decisão 142 (docente). Passa a colagem de fotografia e traço.
05/11/2026: pedido do docente («a alavanca está em cima dos carris ... e o elétrico n devia vir na nossa direção»). Sai a
fotografia do Rossio, com o elétrico de frente; entra o elétrico 541 visto de lado no Largo do Corpo Santo, com as duas vias
a separarem-se no chão (Philip Mallis, 2025, CC BY-SA 4.0). A alavanca fica no passeio, ao lado da via, e liga-se à agulha
por uma vara, como as alavancas de agulha a sério. A fotografia é tratada por tools/tratar_corpo_santo.py.
"""
from pathlib import Path

FOTO='justica/corpo-santo-541.webp'
# 05/11/2026: a fotografia é a do Commons «Remodelados class tram no. 541 turning street corner in Largo do Corpo Santo in
# Lisbon, Portugal (55127582736).jpg», na miniatura padrão de 1920 px (SHA-256 da miniatura em tools/tratar_corpo_santo.py):
# publicidade da lateral do elétrico apagada, recorte (0, 580, 1920, 1440) reduzido a 1340 x 600, cinzentos com autocontraste
# (1 %) e contraste x1,08, tinta (34, 30, 26) e papel (243, 242, 238), WebP qualidade 80. --verificar confere-lhe o SHA-256.
FOTO_SHA256='e547cd191311d92071572587b302490a5a19ffe039d1ba07dce8d62402801e56'
W,H=1340,600

def cena(href='../../assets/'+FOTO):
    """Colagem: a fotografia do Largo do Corpo Santo (o elétrico 541 de lado, a seguir para a esquerda, e no chão a via
    que se divide em duas) e, por cima, a traço, as duas vias que saem da agulha, a marca da agulha e a alavanca no passeio,
    ao lado da via, ligada à agulha por uma vara. Ninguém está na via.
    As coordenadas são as da fotografia recortada (1340 x 600); a cena alarga-se 660 de cada lado."""
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
       # O elétrico 541, na fotografia, marcado a tracejado.
       '<path class="jc-alvo" d="M604 12h642v258h-642z" fill="none" stroke="currentColor" stroke-width="2.5" stroke-dasharray="6 7" opacity=".75"/>',
       '<g fill="none" stroke-linecap="round" stroke-linejoin="round">',
       # As duas vias possíveis, a pontilhado, por cima dos carris da fotografia: nenhuma é escolhida.
       '<path class="jc-via jc-via-a" d="M263 598C330 552 392 510 430 483C470 452 500 420 523 397C552 368 573 348 590 330C612 306 630 288 642 270" stroke="var(--jc-terra,#a84939)" stroke-width="7" stroke-dasharray="1 17"/>',
       '<path class="jc-via jc-via-b" d="M547 598C640 555 740 515 835 477C930 442 1020 420 1105 397C1190 375 1270 355 1340 340" stroke="var(--jc-terra,#a84939)" stroke-width="7" stroke-dasharray="1 17"/>',
       # A agulha: as lâminas onde a via se divide, junto ao fundo da fotografia.
       '<path class="jc-agulha" d="M402 568l22 20M432 566l20 18" stroke="currentColor" stroke-width="3.5"/>',
       # A alavanca, neutra, no passeio à esquerda da via (também à vista no telemóvel); a vara tracejada leva-a até à agulha.
       '<g class="jc-alavanca" stroke="currentColor" stroke-width="4"><path d="M298 404H352L362 416H308Z" fill="var(--jc-papel,#f3f2ee)"/><path d="M330 404L328 338"/><circle cx="328" cy="328" r="11" fill="var(--jc-papel,#f3f2ee)"/><path d="M362 412L406 564" stroke-width="2.5" stroke-dasharray="5 7"/></g>',
       '</g></g></svg>']
    return '\n'.join(a)+'\n'


import argparse
import re
ROOT=Path(__file__).resolve().parents[1]
DESTINO=ROOT/'assets/carris-eletrico.svg'
PAGINA=ROOT/'olhar-e-decidir/justica/index.html'
# 05/11/2026: CC BY-SA 4.0: título, autor, fonte, licença e as alterações; a fotografia tratada fica com a mesma licença.
CREDITO=('Fotografia: elétrico 541 no Largo do Corpo Santo, Lisboa, 29 de maio de 2025, de Philip Mallis '
         '(<a href="https://commons.wikimedia.org/wiki/File:Remodelados_class_tram_no._541_turning_street_corner_in_Largo_do_Corpo_Santo_in_Lisbon,_Portugal_(55127582736).jpg">Wikimedia Commons</a>, '
         '<a href="https://creativecommons.org/licenses/by-sa/4.0/deed.pt">CC BY-SA 4.0</a>); recortada, a preto e branco e sem a publicidade, com a mesma licença. '
         'Por cima, a traço, as duas vias que saem da agulha e a alavanca ao lado da via. Grafismo gerado com recurso a IA, EPI, 2026. Duas vias possíveis, sem desfecho.')

def instalar(texto):
    desenho='<div class="jc-fundo" aria-hidden="true" data-fundo="jc" data-fundo-ciclo="36">'+cena().rstrip()+'</div>'
    texto,n=re.subn(r'<div class="jc-fundo"[^>]*>.*?</svg></div>',lambda _:desenho,texto,flags=re.S)
    assert n==1, 'Esperava-se uma só faixa da Justiça'
    credito='<p class="jc-credito">'+CREDITO+' <button type="button" class="fundo-botao" data-fundo-botao="jc" hidden>Parar o desenho</button></p>'
    texto,n=re.subn(r'<p class="jc-credito">.*?</p>',lambda _:credito,texto,flags=re.S)
    assert n==1, 'Esperava-se um só crédito'
    texto,n=re.subn(r'assets/fundo-carris.css[?]v=[^" ]+', 'assets/fundo-carris.css?v=20261105-3',texto)
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
