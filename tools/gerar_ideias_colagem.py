"""05/11/2026: entrada do «Ideias», colagem de fotografia e traço (docente, 5/11: «isto tem um ar incipiente, colagem é
sempre bem-vinda»). Substitui o desenho das notas e fios só a traço.

A folha é a mancha de Alexander Cozens (The Metropolitan Museum of Art, 30.49.9, domínio público, imagem DP801056, lida na
API do Met a 2/11/2026), o exercício do século XVIII para inventar paisagens a partir de uma mancha. Está pousada na mesa;
por cima, a traço, três cartões de notas e os fios que os ligam ao que a folha mostra: o barco, o contorno a lápis e a
árvore. A fotografia foi reduzida a 960 px, passada a cinzentos com autocontraste (1 %) e a duas cores (tinta e papel),
WebP qualidade 78. Sem movimento.

Uso: python tools/gerar_ideias_colagem.py            (escreve assets/laboratorio/ideias/notas-fios.svg)
     python tools/gerar_ideias_colagem.py --verificar
"""
import hashlib, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DESTINO = ROOT / 'assets/laboratorio/ideias/notas-fios.svg'
FOTO = 'laboratorio/ideias/cozens-mancha-entrada.webp'
FOTO_SHA256 = '7e226f9a7f5816c91b8ea9371411db1338e7fc2f51e7d052e6e953fb56f3a4ed'
W, H = 960, 727          # a fotografia tratada
S = 300 / W              # escala da folha no desenho (300 de largura)
X0, Y0 = 190, 78         # canto da folha
ROT = (-3, 340, 192)     # a folha ligeiramente rodada, como pousada à mão
CREDITO = ('Alexander Cozens, <i>Uma mancha</i> (título nosso), 1750 a 1786, The Metropolitan Museum of Art, Nova Iorque '
           '(domínio público). Por cima, a traço, cartões e fios. Grafismo gerado com recurso a IA, EPI, 2026.')


def ponto(px, py):
    """Coordenadas de um ponto da fotografia (em px de 960) no desenho, antes da rotação da folha."""
    return X0 + px * S, Y0 + py * S


def cartao(x, y, w, h, rot, linhas, extra=''):
    a = [f'<g transform="rotate({rot} {x + w / 2:.0f} {y + h / 2:.0f})">',
         f'<path d="M{x} {y}h{w}v{h}h-{w}z" fill="var(--ly-papel,#f3f2ee)" stroke-width="1.6"/>',
         f'<path d="M{x} {y + 16}h{w}" stroke="var(--vermelho,#b3261e)" stroke-width="1" opacity=".55"/>']
    for k, frac in enumerate(linhas):
        yy = y + 30 + k * 13
        a.append(f'<path d="M{x + 12} {yy}h{(w - 24) * frac:.0f}" stroke-width="1.1" opacity=".75"/>')
    a.append(extra + '</g>')
    return ''.join(a)


def cena(href='../../assets/' + FOTO):
    hw, hh = W * S, H * S
    barco, contorno, arvore = ponto(560, 495), ponto(350, 200), ponto(615, 410)
    a = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 440" preserveAspectRatio="xMidYMid slice" focusable="false">',
         '<g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">',
         # A mesa: linhas leves, como no desenho anterior.
         '<g stroke-width=".7" opacity=".14">' + ''.join(f'<path d="M0 {y}H680"/>' for y in range(18, 440, 21)) + '</g>',
         # A folha de Cozens, com sombra e fita.
         f'<g transform="rotate({ROT[0]} {ROT[1]} {ROT[2]})">',
         f'<path d="M{X0 + 6} {Y0 + 8}h{hw:.0f}v{hh:.0f}h-{hw:.0f}z" fill="currentColor" stroke="none" opacity=".12"/>',
         f'<image class="ideias-foto" href="{href}" x="{X0}" y="{Y0}" width="{hw:.0f}" height="{hh:.0f}"/>',
         f'<path d="M{X0} {Y0}h{hw:.0f}v{hh:.0f}h-{hw:.0f}z" stroke-width=".8" opacity=".35"/>',
         f'<path d="M{X0 + 120} {Y0 - 9}h60v18h-60z" fill="var(--ly-papel,#f3f2ee)" stroke-width="1" opacity=".85"/>',
         # O que se observa na folha: três círculos a traço.
         ''.join(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" stroke="var(--vermelho,#b3261e)" stroke-width="2"/>'
                 for (cx, cy), r in ((barco, 11), (contorno, 15), (arvore, 13))),
         '</g>']
    # Três cartões de notas à volta da folha.
    a.append(cartao(28, 70, 138, 96, -6, [1, .8, .9, .55], ''))
    a.append(cartao(516, 52, 130, 92, 5, [.9, 1, .6, .8], ''))
    a.append(cartao(500, 292, 150, 100, -3, [1, .7, .85, .5, .9], ''))
    # Os fios: de cada coisa observada ao seu cartão (a vermelho, como a linha dos cartões).
    import math
    def rodar(p):
        ang = math.radians(ROT[0]); cx, cy = ROT[1], ROT[2]; x, y = p[0] - cx, p[1] - cy
        return cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang)
    c, b, r = rodar(contorno), rodar(barco), rodar(arvore)
    fio = 'stroke="var(--vermelho,#b3261e)" stroke-width="1.6" stroke-dasharray="1 0"'
    a.append(f'<path d="M{c[0]:.0f} {c[1]:.0f}C{c[0] - 70:.0f} {c[1] - 40:.0f} 220 70 166 112" {fio}/>')
    a.append(f'<path d="M{r[0]:.0f} {r[1]:.0f}C{r[0] + 60:.0f} {r[1] - 70:.0f} 470 100 520 96" {fio}/>')
    a.append(f'<path d="M{b[0]:.0f} {b[1]:.0f}C{b[0] + 40:.0f} {b[1] + 60:.0f} 440 360 502 334" {fio}/>')
    # Um alfinete em cada ponta de fio, nos cartões.
    a.append(''.join(f'<circle cx="{x}" cy="{y}" r="3.5" fill="var(--vermelho,#b3261e)" stroke="none"/>' for x, y in ((166, 112), (520, 96), (502, 334))))
    # Um lápis pousado.
    a.append('<g stroke-width="1.4"><path d="M120 372L300 338l8 9-180 34z" fill="var(--ly-papel,#f3f2ee)"/><path d="M300 338l20 2-12 7"/><path d="M128 374l-4 8"/></g>')
    a.append('</g></svg>')
    return '\n'.join(a) + '\n'


def main(argv):
    svg = cena()
    assert len(svg.encode('utf-8')) < 20_000
    if '--verificar' in argv:
        assert DESTINO.read_text('utf-8') == svg, 'Desenho diferente do gerador'
        assert hashlib.sha256((ROOT / 'assets' / FOTO).read_bytes()).hexdigest() == FOTO_SHA256, 'Fotografia diferente da registada'
        print('Conferido: colagem da entrada do «Ideias»')
        return 0
    DESTINO.write_text(svg, 'utf-8')
    print('Gerado:', DESTINO.relative_to(ROOT), len(svg.encode('utf-8')), 'bytes')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
