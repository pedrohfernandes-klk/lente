"""02/11/2026: elétrico e agulha, desenho vetorial original. Semente fixa; --verificar confere SVG e integração.
Não reconstitui uma rua nem um veículo com número de carreira. Não altera os textos, ligações ou progresso da página.
05/11/2026: decisão 142 (docente). Passa a colagem de fotografia e traço.
05/11/2026: pedido do docente («a alavanca está em cima dos carris ... e o elétrico n devia vir na nossa direção»; depois,
«o elétrico n pode virar numa das direções, o q é lógico p um humano»). Sai a fotografia do Rossio, com o elétrico de frente.
Entra o elétrico 541 visto de lado (Philip Mallis, 2025, CC BY-SA 4.0), recortado por tools/tratar_corpo_santo.py e posto
sobre uma via desenhada: a agulha fica à frente dele e as duas vias seguem no sentido em que anda; a alavanca fica ao lado
da via, junto à agulha, ligada por uma vara, como as alavancas de agulha a sério.
06/11/2026: decisão 170 (docente: «o elétrico da ilustração de justiça deve ter animação, talvez os pontos vermelhos pisquem
e talvez surjam uns pontos de exclamação»; depois, «a alavanca move, claro»). A haste e a pega da alavanca ficam num grupo
que roda sobre o pé (563, 548); as duas lâminas da agulha passam a peças separadas, cada uma com o seu talão; quatro sinais
de alerta a traço (uma haste e um ponto, nunca letra de fonte nem emoji), dois à frente do elétrico e dois junto à alavanca,
fora das vias, ficam escondidos (opacity="0"). O desenho parado continua a ser a cena neutra: o movimento é todo do CSS.
"""
from pathlib import Path

FOTO='justica/eletrico-541-recorte.webp'
# 05/11/2026: pedido do docente («o elétrico n pode virar numa das direções, o q é lógico p um humano»). A colagem deixa de
# usar a rua da fotografia: o elétrico 541 é recortado (tools/tratar_corpo_santo.py: publicidade apagada, só o elétrico e a
# vara, a preto e branco, fundo transparente) e posto sobre uma via desenhada. À frente dele, no sentido em que anda (para
# a esquerda), fica a agulha; depois dela, as duas vias seguem no mesmo sentido, uma a direito e a outra a curvar para o
# primeiro plano. As duas são possíveis para o elétrico. A alavanca fica junto à agulha, ao lado da via, ligada por uma vara.
# --verificar confere o SHA-256 do recorte.
# 05/11/2026: recorte sem os passageiros (o docente: «esta cara não pode ser visível»; depois, sobre o desfoque, «mais classe nisso»).
FOTO_SHA256='3e672269735b3f8fb983b58c165857fd212b56189214363e5a0a410eddb7f2e4'
W,H=1340,600
# Recorte: 962 x 634 px, desenhado a 0,598 por píxel; as rodas assentam no carril da frente (y 470).
RECORTE=(592.8,100.8,575.3,379.1)

# 06/11/2026: decisão 170. Os sinais de alerta: (x, y) é o fundo do ponto, alto a altura toda, graus a inclinação (positiva
# para a direita). Dois à frente do elétrico, no ar, longe das vias; dois junto à alavanca, à direita dela, no chão, abaixo
# da sombra do elétrico. Todos dentro do recorte do telemóvel (de 200 a 1140, e de 256 a 1084 a 320 px).
SINAIS=((1,556,354,42,-8),(2,518,384,32,-15),(3,622,542,34,9),(4,648,532,26,17))

def sinal(n,x,y,alto,graus):
    """Um ponto de exclamação a traço: a haste (com uma ligeira curva, como à mão) e o ponto. Escondido no desenho parado."""
    import math
    a=math.radians(graus);ux,uy=math.sin(a),-math.cos(a);vx,vy=math.cos(a),math.sin(a)
    def p(d,lado=0.0):
        return f'{x+ux*d+vx*lado:.1f} {y+uy*d+vy*lado:.1f}'
    # O traço engrossa um pouco com o tamanho (3,7 a 4,5, como a alavanca e as lâminas); o ponto é um pouco mais largo do que a haste.
    traco=round(2.4+alto*.05,1);r=round(traco*.78,1)
    return (f'<g class="jc-sinal jc-sinal-{n}" stroke="var(--jc-terra,#a84939)" stroke-width="{traco:g}" opacity="0">'
            f'<path d="M{p(alto*.38)}Q{p(alto*.69,1.6)} {p(alto)}"/>'
            f'<circle cx="{x+ux*r:.1f}" cy="{y+uy*r:.1f}" r="{r}" fill="var(--jc-terra,#a84939)" stroke="none"/></g>')

def cena(href='../../assets/'+FOTO):
    """Colagem: o elétrico 541 de lado (fotografia recortada), a andar para a esquerda sobre uma via desenhada. À frente
    dele, a agulha; depois dela, duas vias possíveis no mesmo sentido (a direito e a curvar para o primeiro plano), a
    pontilhado, sem nenhuma escolhida. A alavanca, neutra, fica ao lado da via, junto à agulha, ligada a ela por uma vara.
    Por cima, o fio aéreo onde toca a vara do troleio. Ninguém está na via. A cena vai de -660 a 2000; no telemóvel vê-se
    a parte do meio (de 200 a 1140), com o elétrico, a agulha, a alavanca e o começo das duas vias.
    06/11/2026: decisão 170. A alavanca, as lâminas e os sinais de alerta têm classes para o movimento (assets/fundo-carris.css);
    parados, a alavanca fica a direito, as lâminas encostadas e os sinais escondidos: a mesma cena neutra."""
    import random
    rng=random.Random(20261105)
    x,y,w,h=RECORTE
    a=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-660 0 {W+1320} {H}" preserveAspectRatio="xMidYMin slice" focusable="false">',
       '<g class="jc-traco" fill="none" stroke="currentColor" stroke-linecap="round">']
    # O chão: calçada a traço só abaixo da via, em perspetiva (as fiadas alargam-se para o primeiro plano), com semente fixa.
    a.append('<g stroke-width="1.1" opacity=".26">')
    for i,yy in enumerate((484,497,511,527,545,566,590)):
        passo=14+i*4
        for xx in range(-660,2000,passo):
            px=xx+(passo//2 if i%2 else 0)+rng.uniform(-2,2)
            a.append(f'<path d="M{px:.1f} {yy+rng.uniform(-1.5,1.5):.1f}h{passo-5}"/>')
    # O fio aéreo, onde toca a vara do troleio.
    a.append('</g><path d="M-660 107H2000" stroke-width="1.4" opacity=".55"/></g>')
    a+=['<g class="jc-eletrico">',
       '<g class="jc-carris" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" opacity=".85">',
       # A via do elétrico, até à agulha; depois, a via a direito continua para a esquerda.
       '<path d="M2000 458H-660M2000 470H-660"/>',
       # A via que curva para o primeiro plano, a sair da agulha no sentido em que o elétrico anda.
       '<path d="M506 470C456 471 404 498 352 540C318 568 290 592 276 612M524 458C474 460 424 486 376 528C342 558 314 590 300 612"/>',
       '</g>',
       # A sombra do elétrico no chão.
       f'<ellipse cx="{x+w/2:.1f}" cy="472" rx="{w/2:.1f}" ry="9" fill="currentColor" opacity=".12"/>',
       f'<image class="jc-foto" href="{href}" x="{x}" y="{y}" width="{w}" height="{h}"/>',
       # O elétrico, marcado a tracejado.
       '<path class="jc-alvo" d="M598 254h564v194h-564z" fill="none" stroke="currentColor" stroke-width="2.5" stroke-dasharray="6 7" opacity=".6"/>',
       '<g fill="none" stroke-linecap="round" stroke-linejoin="round">',
       # As duas vias possíveis, a pontilhado: nenhuma é escolhida.
       # 05/11/2026: o docente, «os pontos vermelhos têm de ir até ao fim»: a via a direito vai até à ponta esquerda, como os carris.
       '<path class="jc-via jc-via-a" d="M488 464H-660" stroke="var(--jc-terra,#a84939)" stroke-width="7" stroke-dasharray="1 17"/>',
       '<path class="jc-via jc-via-b" d="M492 466C446 468 400 494 354 536C322 564 300 590 288 610" stroke="var(--jc-terra,#a84939)" stroke-width="7" stroke-dasharray="1 17"/>',
       # A agulha: as duas lâminas, à frente do elétrico.
       # 06/11/2026: decisão 170. Cada lâmina é uma peça, para se mexer com a alavanca: a de perto (no carril de perto) e a de
       # longe (no carril de longe); o talão de cada uma fica à direita. O traço é o mesmo de antes.
       '<g class="jc-agulha" stroke="currentColor" stroke-width="3.5"><path class="jc-agulha-perto" d="M470 470l34-1"/><path class="jc-agulha-longe" d="M478 458l28 2"/></g>',
       # A alavanca, neutra, ao lado da via e junto à agulha; a vara tracejada liga-a às lâminas.
       # 06/11/2026: decisão 170. A haste e a pega num grupo, que roda sobre o pé da haste (563, 548), em cima da base.
       '<g class="jc-alavanca" stroke="currentColor" stroke-width="4"><path d="M532 548H584L594 560H542Z" fill="var(--jc-papel,#f3f2ee)"/><g class="jc-alavanca-braco"><path d="M563 548L561 496"/><circle cx="561" cy="486" r="10" fill="var(--jc-papel,#f3f2ee)"/></g><path d="M546 552L496 476" stroke-width="2.5" stroke-dasharray="5 7"/></g>']
    # 06/11/2026: decisão 170. Os sinais de alerta, escondidos no desenho parado.
    a+=[sinal(*s) for s in SINAIS]
    a+=['</g></g></svg>']
    return '\n'.join(a)+'\n'


import argparse
import re
ROOT=Path(__file__).resolve().parents[1]
DESTINO=ROOT/'assets/carris-eletrico.svg'
PAGINA=ROOT/'olhar-e-decidir/justica/index.html'
# 05/11/2026: CC BY-SA 4.0: título, autor, fonte, licença e as alterações; a fotografia tratada fica com a mesma licença.
# 06/11/2026: decisão 170. A lista do que é desenho passa a incluir «os sinais de alerta».
CREDITO=('Fotografia: elétrico 541 no Largo do Corpo Santo, Lisboa, 29 de maio de 2025, de Philip Mallis '
         '(<a href="https://commons.wikimedia.org/wiki/File:Remodelados_class_tram_no._541_turning_street_corner_in_Largo_do_Corpo_Santo_in_Lisbon,_Portugal_(55127582736).jpg">Wikimedia Commons</a>, '
         '<a href="https://creativecommons.org/licenses/by-sa/4.0/deed.pt">CC BY-SA 4.0</a>); o elétrico recortado, a preto e branco, sem a publicidade e sem os passageiros, com a mesma licença. '
         'A via, a agulha, as duas vias possíveis, a alavanca ao lado da via e os sinais de alerta são desenho. Grafismo gerado com recurso a IA, EPI, 2026. Duas vias possíveis, sem desfecho.')

def instalar(texto):
    desenho='<div class="jc-fundo" aria-hidden="true" data-fundo="jc" data-fundo-ciclo="36">'+cena().rstrip()+'</div>'
    texto,n=re.subn(r'<div class="jc-fundo"[^>]*>.*?</svg></div>',lambda _:desenho,texto,flags=re.S)
    assert n==1, 'Esperava-se uma só faixa da Justiça'
    credito='<p class="jc-credito">'+CREDITO+' <button type="button" class="fundo-botao" data-fundo-botao="jc" hidden>Parar o desenho</button></p>'
    texto,n=re.subn(r'<p class="jc-credito">.*?</p>',lambda _:credito,texto,flags=re.S)
    assert n==1, 'Esperava-se um só crédito'
    # 06/11/2026: decisão 170. Nova versão do CSS (o movimento da alavanca, das vias e dos sinais), para o navegador o recarregar.
    texto,n=re.subn(r'assets/fundo-carris.css[?]v=[^" ]+', 'assets/fundo-carris.css?v=20261106-1',texto)
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
