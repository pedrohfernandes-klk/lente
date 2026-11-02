# Desenhos a traço (SVG nosso, preto e branco: o traço segue a cor do texto).
# Os cinco casos da lição 1 vêm já desenhados das fontes (desenhos.json, extraídos do guião das fontes);
# os novos (bote, balança, carro, ecrãs) seguem o mesmo traço.
import json, math, os
AQUI = os.path.dirname(os.path.abspath(__file__))
_F = json.load(open(os.path.join(AQUI, 'desenhos.json'), encoding='utf-8'))

def n1(x):
    v = round(float(x), 1)
    return str(int(v)) if v == int(v) else str(v)

def ST(w=1.8):
    return f'fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'

def tr(d, w=1.8, extra=''):
    return f'<path d="{d}" {ST(w)}{extra}/>'

def svg(w, h, corpo):
    return f'<svg viewBox="0 0 {w} {h}" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">{corpo}</svg>'

def pessoa(x, y, s=1):
    X = lambda v: n1(x + v * s); Y = lambda v: n1(y - v * s)
    return (f'<g {ST(1.6)}><circle cx="{X(0)}" cy="{Y(27)}" r="{n1(4.5*s)}"/>'
            f'<path d="M{X(0)} {Y(22.5)}V{Y(11)}M{X(-5)} {Y(0)}L{X(0)} {Y(11)}L{X(5)} {Y(0)}M{X(-6)} {Y(14)}L{X(0)} {Y(19)}L{X(6)} {Y(14)}"/></g>')

def busto(x, y, s=1):
    """sentado: só a cabeça, o tronco e os braços acima da borda (y)"""
    X = lambda v: n1(x + v * s); Y = lambda v: n1(y - v * s)
    return (f'<g {ST(1.6)}><circle cx="{X(0)}" cy="{Y(20)}" r="{n1(4.5*s)}"/>'
            f'<path d="M{X(0)} {Y(15.5)}V{Y(0)}M{X(-6)} {Y(4)}L{X(0)} {Y(11)}L{X(6)} {Y(4)}"/></g>')

def seta(d, x, y, ang):
    a1 = (n1(x - 7 * math.cos(ang - 0.45)), n1(y - 7 * math.sin(ang - 0.45)))
    a2 = (n1(x - 7 * math.cos(ang + 0.45)), n1(y - 7 * math.sin(ang + 0.45)))
    return tr(d, 1.4, ' stroke-dasharray="4 4"') + tr(f'M{a1[0]} {a1[1]}L{x} {y}L{a2[0]} {a2[1]}', 1.4)

def bote():
    ondas = ''.join(f'M{x} 112q8 -5 16 0t16 0' for x in range(4, 228, 32))
    corpo = (tr(ondas, 1.2)
             + tr('M30 82H210L194 104Q120 114 46 104Z', 2.2)  # o casco
             + tr('M38 90H202', 1.1)
             + busto(64, 82) + busto(92, 82) + busto(120, 82)
             # Parker, deitado no fundo do bote, a um canto
             + f'<g {ST(1.6)}><circle cx="150" cy="96" r="4"/><path d="M154.5 97H180M162 97L168 92M170 97L176 101"/></g>'
             # as duas latas e a faca ficam fora: só as pessoas e o mar
             )
    return svg(240, 124, corpo)

def balanca():
    # o braço inclina para o lado do dinheiro; a pessoa de pé no prato da esquerda, as moedas no da direita
    moedas = ''.join(f'<ellipse cx="186" cy="{n1(91 - k*5.5)}" rx="11" ry="3.2" {ST(1.4)}/>' for k in range(5))
    corpo = (tr('M120 18V128M96 128H144', 2.2)  # o poste e a base
             + tr('M52 30L188 44', 2)
             + f'<circle cx="120" cy="37" r="3.5" {ST(1.6)}/>'
             + tr('M52 30L22 82M52 30L82 82M188 44L160 96M188 44L216 96', 1.1)
             + tr('M18 82H86M156 96H220', 2.2)  # os pratos
             + pessoa(52, 81, 1.2)
             + moedas)
    return svg(240, 134, corpo)

def carro():
    corpo = (tr('M8 104H352', 2)
             # o carro pequeno, de perfil, com o depósito atrás
             + tr('M150 96V78Q150 72 156 72H186L204 56H262Q272 56 280 66L296 78Q302 80 302 86V96Z', 2)
             + tr('M210 60V72M262 60L276 72H210', 1.3)
             + f'<circle cx="176" cy="98" r="9" {ST(1.8)}/><circle cx="276" cy="98" r="9" {ST(1.8)}/>'
             + f'<rect x="138" y="80" width="14" height="12" rx="2" {ST(2.2)}/>'
             # o carro de trás e o choque, a tracejado
             + tr('M14 96V82Q14 76 20 76H44L56 66H92Q100 66 104 74L112 82V96Z', 1.4, ' stroke-dasharray="5 4"')
             + f'<circle cx="34" cy="98" r="7" {ST(1.4)}/><circle cx="92" cy="98" r="7" {ST(1.4)}/>'
             + seta('M114 88H132', 132, 88, 0)
             + tr('M128 70l4 -8M138 66l8 -6M142 76l9 -2', 1.3))
    return svg(360, 116, corpo)

def ecras():
    def ecra(x):
        return (f'<rect x="{x}" y="14" width="96" height="66" rx="4" {ST(2)}/>'
                + tr(f'M{x+38} 92H{x+58}M{x+48} 80V92', 1.6))
    # 1: alguém de pé, de mão no ar, a falar sozinho; 2: alguém pendurado numa barra; 3: três no sofá
    falar = pessoa(48, 74, 1.4) + tr('M54 46L66 36', 1.6) + tr('M70 30q6 -4 12 0M74 24q6 -4 12 0', 1.1)
    barra = tr('M128 24H200', 2) + f'<g {ST(1.6)}><circle cx="164" cy="44" r="5"/><path d="M164 49V64M156 24L164 38L172 24M164 64L158 76M164 64L170 76"/></g>' + tr('M140 74q8 4 16 0M174 74q8 4 16 0', 1.1)
    sofa = tr('M232 74V60Q232 56 236 56H300Q304 56 304 60V74M228 62V76H308V62', 1.8) + busto(248, 58, 0.8) + busto(268, 58, 0.8) + busto(288, 58, 0.8)
    return svg(330, 100, ecra(10) + ecra(117) + ecra(224) + falar + barra + sofa)

LEGENDAS = {
    'condutor': 'O condutor: em frente, cinco trabalhadores na via; no desvio, um.',
    'ponte': 'O espectador na ponte: um empurrão faz cair o homem à frente do elétrico e poupa os cinco.',
    'alcapao': 'O alçapão: rodas um volante e o alçapão abre-se debaixo do homem, sem lhe tocares.',
    'urgencias': 'O médico das urgências: cinco feridos moderados e um grave; não há tempo para todos.',
    'cirurgiao': 'O cirurgião de transplantes: cinco doentes à espera de órgãos; na sala ao lado, um homem saudável a dormir.',
    'bote': 'O bote do Mignonette: quatro náufragos; Parker, doente, deitado a um canto.',
    'balanca': 'Pôr um preço à vida: de um lado uma pessoa, do outro dinheiro.',
    'carro': 'O Ford Pinto: o depósito de combustível atrás; num choque por trás, podia explodir.',
    'ecras': 'Três excertos: um monólogo de Hamlet, o concurso Fear Factor e Os Simpsons.',
}
_NOVOS = {'bote': bote, 'balanca': balanca, 'carro': carro, 'ecras': ecras}

def desenho(id):
    return _NOVOS[id]() if id in _NOVOS else _F[id]['svg']

def figura(id, cls='desenho'):
    return f'<figure class="{cls}">{desenho(id)}<figcaption>{LEGENDAS[id]}</figcaption></figure>'

def par(a, b):
    """dois desenhos lado a lado, com uma legenda cada"""
    return f'<div class="desenho-par">{figura(a)}{figura(b)}</div>'
