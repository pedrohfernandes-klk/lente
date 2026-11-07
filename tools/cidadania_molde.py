"""05/11/2026 (plano do molde da Cidadania, pedido 2): o ajudante comum das sessões no molde cidadania-2026-11.

Fica fora de tools/licoes/ (o gerador lê todos os .json dessa pasta) e é importado pelas fontes das sessões
(tools/licoes/cidadania-mN-sNN.py). Cada função devolve um cartão (um dict do .json) com o HTML igual em todas as sessões:
a raiz de cada cartão de ler leva a classe do seu tipo (.m-abre, .m-decide, .m-olha, .m-le, .m-conceito, .m-volta, .m-turma,
.m-papel, .m-levar), que assets/licoes/cidadania.css usa para a identidade, e as peças do motor descritas em
/home/user/bordo/cidadania-v3/molde-s01/motor.md (posições, artefactos, «i» dos créditos, relógio, lei em citação).

Regras que o ajudante garante sozinho:
- referências sem quebra de linha: «artigo 12.º», «n.º 1», «art. 3» levam espaço inseparável (decisão 152), em todo o texto;
  06/11/2026 (revisão da s01): também as datas («21 de setembro de 1990», «novembro de 1949») e os números com unidade ou
  nome («12 anos», «60 min», «+1 min»), com as mesmas regras do validador (tools/licoes_lente.py, DATA_PARTIDA e NUMERO_PARTIDO);
- cada excerto de lei ou declaração leva data-fonte com o identificador do registo tools/cidadania_fontes.json (o teste
  tests/test_molde_cidadania.py confere que o texto está lá, letra a letra, e confirmado);
- a imagem leva o crédito atrás do «i» (decisão 153) e só a legenda que serve a pergunta fica à vista.

Funções: abre(), decide(), recupera(), olha(), le(), conceito(), volta(), em_turma(), papel(), levar(), e as peças
posicao(), lados(), lei(), figura() e relogio()."""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
NB = ' '
FONTES = ROOT / 'tools' / 'cidadania_fontes.json'
_REF = re.compile(r'(?<![\wÀ-ÿ])(n\.º|n\.os|[Aa]rtigos?|art\.|[Aa]línea|cap\.|p\.|pp\.) (?=\d)')
_MESES = r'(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)'
_DATA = re.compile(r'(?<!\d)\d{1,2} de ' + _MESES + r'(?: de \d{4})?|' + _MESES + r' de \d{4}', re.I)
_NUM = re.compile(r'(?<![\w.,/:])(\d+) (?!(?:que|com|por|sem|dos|das|nos|nas|não|mas|para|pela|pelo|como|mais|até|foi|era|são)(?![\wÀ-ÿ]))(?=[a-zà-ÿ]{3,})')


def ref(s):
    """Espaço inseparável entre a palavra da referência e o número («artigo 12.º», «n.º 1»), só no texto, nunca dentro
    das etiquetas."""
    partes = re.split(r'(<[^>]+>)', str(s))
    for i in range(0, len(partes), 2):
        partes[i] = _REF.sub(lambda m: m.group(1) + NB, partes[i])
        partes[i] = _DATA.sub(lambda m: m.group(0).replace(' ', NB), partes[i])
        partes[i] = _NUM.sub(lambda m: m.group(1) + NB, partes[i])
    return ''.join(partes)


def esc(s):
    return html.escape(str(s), quote=True)


def registo():
    """O registo dos excertos: {id: entrada}."""
    d = json.loads(FONTES.read_text('utf-8'))
    return {x['id']: x for x in d['excertos']}


def _excerto_ok(ident, texto):
    """Confere, ao escrever a sessão, que o excerto está no registo, confirmado, e que cada pedaço (separado por «[…]»)
    é texto exato da fonte. O teste faz a mesma conta sobre o .json escrito."""
    r = registo().get(ident)
    if not r or r.get('confirmado') is not True:
        raise ValueError(f'excerto «{ident}» fora do registo ou por confirmar')
    alvo = ' '.join(r['texto'].replace(NB, ' ').split())
    for pedaco in re.split(r'\s*\[…\]\s*', texto.replace(NB, ' ')):
        pedaco = ' '.join(pedaco.strip(' «»').split())
        if pedaco and pedaco not in alvo:
            raise ValueError(f'excerto «{ident}»: «{pedaco}» não está na fonte')
    return texto


def citado(ident, texto):
    """Um excerto curto dentro de uma frase (por exemplo numa tabela), marcado com o registo."""
    _excerto_ok(ident, texto)
    return f'<span class="citado" data-fonte="{ident}">«{texto}»</span>'


# ---------------------------------------------------------------- peças
def posicao(ident, rot, pergunta, opcoes=('Sim', 'Não', 'Depende'), nota='Não há resposta certa neste cartão.'):
    """Escolha sem certa nem errada (assets/licoes/recolha.js): guarda-se no aparelho e pode mudar-se."""
    ops = ''.join(f'<button type="button" class="pos-op" data-valor="{esc(v)}" data-frase="{esc(v.lower() if len(v) < 12 else v)}">{esc(v)}</button>'
                  for v in opcoes)
    return (f'<div class="posicao" data-artefacto="{ident}" data-rot="{esc(rot)}"><p class="pos-q">{ref(pergunta)}</p>'
            f'<div class="pos-ops" role="group" aria-label="{esc(rot)}">{ops}</div>'
            + (f'<p class="pos-nota">{nota}</p>' if nota else '') + '</div>')


def lados(ident, itens):
    """Os três lados (as duas partes e uma objeção), que só abrem depois de escolher."""
    assert len(itens) == 3, 'três lados'
    corpo = ''.join(f'<details class="lado"><summary>{ref(t)}</summary><div><p>{ref(x)}</p></div></details>' for t, x in itens)
    for _, x in itens:
        assert len(re.sub(r'<[^>]+>', ' ', x).split()) <= 40, f'lado com mais de 40 palavras: {x[:40]}'
    return f'<div class="pos-lados" data-depois-de="{ident}" hidden>{corpo}</div>'


def lei(excertos, fonte_html=''):
    """Excertos em citação, com o artigo na margem. excertos: [(rótulo, texto, id do registo, linha marcável ou None)]."""
    ps = ''
    for rot, texto, ident, linha in excertos:
        _excerto_ok(ident, texto)
        dl = f' data-l="{linha}"' if linha else ''
        ps += f'<p{dl} data-fonte="{ident}"><span class="art">{ref(rot)}</span>«{texto}»</p>'
    return f'<blockquote class="lei">{ps}</blockquote>' + (f'<p class="fonte-lei">{ref(fonte_html)}</p>' if fonte_html else '')


def figura(src, alt, credito, legenda, artefacto=None, largura=None, altura=None, rotulo_i='Créditos da fotografia'):
    """O documento inteiro, ampliável, com o crédito atrás do «i» (decisão 153) e só a legenda que serve a pergunta. 06/11/2026
    (revisão da s04): «rotulo_i» dá o nome do «i» para quem usa leitor de ecrã quando a imagem não é uma fotografia (por exemplo,
    «Créditos da gravura»); sem ele, fica o de antes."""
    art = (f' data-artefacto="imagem" data-rot="A imagem que viste" data-texto="{esc(artefacto)}"' if artefacto else '')
    dim = f' width="{largura}" height="{altura}"' if largura and altura else ''
    return (f'<figure class="fig inteiro"{art}><div class="moldura com-i"><img src="{esc(src)}" alt="{esc(alt)}"{dim} loading="lazy">'
            f'<details class="info-i" name="info-i"><summary aria-label="{esc(rotulo_i)}"><span aria-hidden="true">i</span></summary>'
            f'<p class="info-i-texto">{credito}</p></details></div><figcaption>{ref(legenda)}</figcaption></figure>')


def relogio(minutos, rot='Relógio do papel'):
    """O relógio comum (assets/licoes/relogio.js): começa parado, só avisa, nada se apaga."""
    return (f'<div class="tr-relogio" data-relogio="{minutos * 60}" role="group" aria-label="{esc(rot)}"><p class="tr-tempo">{minutos}:00</p>'
            '<button type="button" data-rl="ir">Começar</button><button type="button" data-rl="parar" hidden>Pausa</button>'
            '<button type="button" data-rl="mais">+1 min</button><p class="tr-aviso" aria-live="polite"></p></div>')


def _ler(rot, titulo, corpo, minutos, **extra):
    return dict({'t': 'ler', 'rot': rot, 'titulo': titulo, 'html': ref(corpo), 'min': minutos}, **extra)


# ---------------------------------------------------------------- cartões de ler
def abre(titulo, linha, caso, pergunta, minutos=5, carimbo='Caso inventado.'):
    """Cartão 1. Título em letra de cartaz, linha «Hoje», carimbo, o caso (até 70 palavras) e a pergunta da sessão."""
    assert len(caso.split()) <= 70, 'o caso tem até 70 palavras'
    corpo = (f'<div class="m-abre"><p class="carimbo">{carimbo}</p>'
             f'<p class="caso" data-artefacto="caso" data-rot="O caso">{caso}</p>'
             f'<p class="pergunta-sessao" data-artefacto="pergunta" data-rot="A pergunta da sessão">{pergunta}</p></div>')
    return _ler('Abre', titulo, corpo, minutos, aula={'linha': ref(linha)})


def decide(pergunta, itens, titulo='Antes dos materiais', minutos=8,
           intro='Decide: sim, não ou depende. Escolhe antes de veres os materiais; no fim, voltas a esta pergunta.'):
    """Cartão 2. A posição no início (artefacto) e os três lados, que só abrem depois de escolher."""
    corpo = (f'<div class="m-decide"><p class="pos-intro">{intro}</p>'
             + posicao('posicao-inicio', 'A tua posição no início', pergunta) + lados('posicao-inicio', itens) + '</div>')
    return _ler('Decide', titulo, corpo, minutos)


def olha(titulo, antes, fig, minutos=3):
    """Cartão 5. O documento inteiro, com «Antes de olhar»."""
    return _ler('Olha', titulo, f'<div class="m-olha"><p class="ex-antes"><b>Antes de olhar</b> {antes}</p>{fig}</div>', minutos)


def le(titulo, antes, excertos, fonte_html, mais='', minutos=4):
    """Cartão 8. «Antes de ler», os excertos em citação (linhas marcáveis) e a fonte oficial; o resto em «Ler mais»."""
    corpo = f'<div class="m-le"><p class="ex-antes"><b>Antes de ler</b> {antes}</p>' + lei(excertos, fonte_html)
    if mais:
        corpo += f'<details class="mais"><summary>Ler mais</summary><div>{mais}</div></details>'
    return _ler('Lê', titulo, corpo + '</div>', minutos)


def conceito(titulo, caso, perto, nome, definicao, nao_e, mais='', minutos=6, botao='Mais perto'):
    """Cartão 13. O cartão de conceito do Português (.cc): o caso, mais perto, o nome, o que não é. O nome e a definição
    ficam nos artefactos quando o passo se abre."""
    passos = (f'<div class="cc-passo cc-caso"><p class="cc-r">O caso</p>{caso}</div>'
              f'<div class="cc-passo" hidden><p class="cc-r">Mais perto</p>{perto}</div>'
              f'<div class="cc-passo" hidden data-artefacto="conceito" data-rot="O conceito" data-texto="{esc(nome)}: {esc(definicao[:1].lower() + definicao[1:])}">'
              f'<p class="cc-r">O nome</p><p class="cc-termo">{nome}</p><p class="cc-def">{definicao}</p></div>'
              f'<div class="cc-passo" hidden><p class="cc-r">O que não é</p>{nao_e}</div>')
    corpo = (f'<div class="m-conceito"><div class="cc" data-cc>{passos}'
             f'<button type="button" class="cc-mais" data-cc-mais>{botao} <span aria-hidden="true">→</span></button></div>')
    if mais:
        corpo += f'<details class="mais"><summary>Ler mais</summary><div>{mais}</div></details>'
    return _ler('Conceito', titulo, corpo + '</div>', minutos)


def volta(titulo, caso, excertos=(), fonte_html='', minutos=4, carimbo=None):
    """Cartão 16. Abre a parte 2: a informação nova que cria o conflito (serve de reentrada numa segunda aula). 06/11/2026: com
    «carimbo» («Caso inventado.»), quem entra aqui numa segunda aula sabe logo que o caso é inventado."""
    corpo = (f'<div class="m-volta"><p class="parte">Parte 2</p>' + (f'<p class="carimbo">{carimbo}</p>' if carimbo else '')
             + f'<p class="caso">{caso}</p>')
    if excertos:
        corpo += lei(excertos, fonte_html)
    return _ler('Volta ao caso', titulo, corpo + '</div>', minutos)


CAMPOS = ('O que se faz', 'Quanto tempo', 'O que fica escrito', 'Se estás sozinho')


def em_turma(pergunta, itens, campos, prova=None, titulo='Depois dos materiais', minutos=13,
             intro='Volta à pergunta do início com o que viste. Decide outra vez.', prova_rot='A prova que pesou',
             nota='Não há resposta certa neste cartão.'):
    """Cartão 18. A posição depois (artefacto), os lados presos ao material, a prova que pesou (artefacto, opcional) e os
    quatro campos. Acaba-se sozinho (decisão 154): o campo «Se estás sozinho» diz como. 06/11/2026: «prova_rot» dá o nome do
    artefacto quando o que se escolhe não é uma prova (na s01, «O direito que pesou»); o identificador fica «prova». Sem «intro»
    nem «nota», o cartão fica sem a linha de abertura e sem «Não há resposta certa» (o campo «O que se faz» já diz o que fazer)."""
    assert tuple(campos) == CAMPOS, 'os quatro campos, por esta ordem'
    dl = ''.join(f'<dt>{k}</dt><dd>{ref(v)}</dd>' for k, v in campos.items())
    corpo = ('<div class="m-turma">' + (f'<p class="pos-intro">{intro}</p>' if intro else '')
             + '<p class="pos-antes" data-modelo="No início, escolheste «{posicao-inicio}»." hidden></p>'
             + posicao('posicao-depois', 'A tua posição depois', pergunta, nota=nota) + lados('posicao-depois', itens))
    if prova:
        q, ops = prova
        corpo += posicao('prova', prova_rot, q, ops, nota=None)
    return _ler('Em turma', titulo, corpo + f'<dl class="campos">{dl}</dl></div>', minutos)


def papel(pergunta, linhas, conta, exemplo, intro, minutos=15, relogio_min=12):
    """Cartão 22. A pergunta do Abre e três linhas num papel A6 com código e data; «O que conta» e «Um exemplo»."""
    li = ''.join(f'<li>{ref(x)}</li>' for x in linhas)
    ct = ''.join(f'<li>{ref(x)}</li>' for x in conta)
    corpo = (f'<div class="m-papel"><p class="papel-intro">{intro}</p><p class="papel-q">{pergunta}</p>'
             f'<div class="papel-a6"><p class="papel-cab"><span>Código</span><span>Data</span></p><ol>{li}</ol></div>'
             + relogio(relogio_min) +
             f'<details class="mais"><summary>O que conta</summary><div><ol>{ct}</ol></div></details>'
             f'<details class="mais"><summary>Um exemplo, sobre outro caso</summary><div>{ref(exemplo)}</div></details></div>')
    return _ler('Agora, em papel', 'Agora, em papel', corpo, minutos)


def levar(frase, frases, minutos=5, modelo='No início, decidiste «{posicao-inicio}»; depois, «{posicao-depois}».'):
    """Cartão 23 (escuro). A frase da sessão letra a letra (artefacto), as frases da sessão, a volta à posição e a lista
    dos artefactos com «Copiar para as notas» e «Partilhar»."""
    letras = ''.join(f'<span class="ch" style="--i:{i}">{esc(c)}</span>' for i, c in enumerate(frase))
    fr = ''.join(f'<li>{ref(x)}</li>' for x in frases)
    corpo = (f'<div class="m-levar"><p class="levar" data-artefacto="frase" data-rot="A frase da sessão" data-texto="{esc(frase)}">{letras}</p>'
             f'<p class="levar-volta" data-modelo="{esc(modelo)}" hidden></p>'
             f'<p class="frases-t">As frases da sessão</p><ul class="frases">{fr}</ul><div data-recolha-lista></div></div>')
    return dict(_ler('Para levar', '', corpo, minutos), escuro=True)


# ---------------------------------------------------------------- cartões de fazer
def recupera(cartao, origem=None):
    """Cartões 3 e 4. Um exercício que recupera: «g» recupera; o 2.º diz a sessão de origem."""
    c = dict(cartao, g='recupera')
    if origem:
        c['origem'] = origem
    return c


def fazer(t, rot, p, p2, f, minutos, tipo, conceito, **extra):
    """Um cartão de fazer com os campos que o contrato exige (rot próprio, p2, retorno, tipo e conceito)."""
    c = {'t': t, 'rot': rot, 'p': ref(p), 'p2': ref(p2), 'f': ref(f), 'min': minutos, 'tipo': tipo, 'conceito': conceito}
    for k, v in extra.items():
        if k in ('fe',):
            v = [ref(x) for x in v] if isinstance(v, list) else ref(v)
        elif k in ('o', 'passos'):
            v = [ref(x) for x in v]
        elif k == 'pares':
            v = [[ref(a), ref(b)] for a, b in v]
        elif k in ('cita', 'pista'):
            v = ref(v)
        c[k] = v
    if extra.get('fonte') and (extra.get('cita') or extra.get('frase')):
        fonte, texto = extra['fonte'], extra.get('cita') or extra.get('frase')
        if isinstance(fonte, list):
            # 06/11/2026: uma citação com passagens de várias entradas do registo (por exemplo a ordem e a fundamentação de um
            # acórdão): os pedaços separados por «[…]» conferem-se, um a um e pela ordem, com a entrada respetiva.
            pedacos = re.split(r'\s*\[…\]\s*', texto)
            if len(pedacos) != len(fonte):
                raise ValueError(f'citação com {len(pedacos)} pedaços para {len(fonte)} entradas do registo')
            for ident, pedaco in zip(fonte, pedacos):
                _excerto_ok(ident, pedaco)
        else:
            _excerto_ok(fonte, texto)
    for ident, texto in extra.get('citacoes', []):
        _excerto_ok(ident, texto)
    return c
