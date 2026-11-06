"""05/11/2026: plano do molde da Cidadania, pedido 1. Uma lição de ENSAIO no molde cidadania-2026-11, só para os testes: não
é uma sessão, não se publica e não está em tools/licoes/. Cumpre o contrato do validador (tests/test_molde_cidadania.py
estraga-a de propósito, regra a regra) e serve ao percurso no navegador das peças do molde (posições, artefactos, «i»,
ampliação, retoma e projeção) em tests/browser_licoes_lente.cjs. O texto é neutro e diz que é de ensaio; o único material
real é a fotografia de 1949 que já está no repositório, com o crédito e as ligações da sessão-modelo (#110). Os conteúdos
das sessões entram com a s01."""
import copy, importlib.util, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location('licoes_lente', ROOT / 'tools/licoes_lente.py')
L = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(L)

NB = ' '
LADOS = ('<div class="pos-lados" data-depois-de="{id}" hidden>'
         '<details class="lado"><summary>Um lado</summary><div><p>Texto de ensaio do primeiro lado.</p></div></details>'
         '<details class="lado"><summary>O outro lado</summary><div><p>Texto de ensaio do segundo lado.</p></div></details>'
         '<details class="lado"><summary>Uma objeção</summary><div><p>Texto de ensaio da objeção.</p></div></details></div>')


def posicao(ident, rot, pergunta):
    ops = ''.join(f'<button type="button" class="pos-op" data-valor="{v}" data-frase="{v.lower()}">{v}</button>' for v in ('Sim', 'Não', 'Depende'))
    return (f'<div class="posicao" data-artefacto="{ident}" data-rot="{rot}"><p class="pos-q">{pergunta}</p>'
            f'<div class="pos-ops" role="group" aria-label="A tua posição">{ops}</div>'
            '<p class="pos-nota">Não há resposta certa neste cartão.</p></div>' + LADOS.format(id=ident))


FIG = ('<figure class="fig inteiro" data-artefacto="imagem" data-rot="A imagem vista" data-texto="Eleanor Roosevelt com o cartaz da Declaração, 1949">'
       '<div class="moldura com-i"><img src="../../../img/cidadania/eleanor-roosevelt-dudh-1949.webp" alt="Eleanor Roosevelt segura com as duas mãos '
       'um grande cartaz com o título «The Universal Declaration of Human Rights» e o símbolo das Nações Unidas." loading="lazy">'
       '<details class="info-i" name="info-i"><summary aria-label="Créditos da fotografia"><span aria-hidden="true">i</span></summary>'
       f'<p class="info-i-texto">Eleanor Roosevelt com a Declaração Universal, Lake Success, novembro{NB}de{NB}1949. Fotógrafo não identificado. '
       'FDR Presidential Library &amp; Museum, 64-165. <a href="https://www.flickr.com/photos/fdrlibrary/27758131387/">Registo de origem</a>. '
       '<a rel="license" href="https://creativecommons.org/licenses/by/2.0/deed.pt">CC BY 2.0</a>.</p></details></div>'
       '<figcaption>Lake Success, 1949: um ano depois de aprovada, a Declaração já circula em cartaz.</figcaption></figure>')
VER = '<img src="../../../img/cidadania/eleanor-roosevelt-dudh-1949.webp" alt="Eleanor Roosevelt segura um grande cartaz com o título da Declaração.">'
FRASE = 'Um molde serve quando se faz sozinho.'


# 06/11/2026 (correções da revisão da s01): o contrato do molde passou a exigir uma pista própria em cada exercício, que não dê
# a resposta; o ensaio leva uma pista de ensaio em todos.
PISTA = 'Ensaio: volta ao material antes de responder.'


def ler(rot, titulo, html, minutos, **extra):
    return dict({'t': 'ler', 'rot': rot, 'titulo': titulo, 'html': html, 'min': minutos}, **extra)


def escolha(rot, p, certa, erradas, minutos, tipo='aplicar', **extra):
    # a certa fica no índice que pedir «lugar» (preenchido em licao(), com a semente do motor)
    return dict({'t': 'escolha', 'rot': rot, 'p': p, 'p2': 'Outra redação: ' + p[0].lower() + p[1:], '_certa': certa, '_erradas': erradas,
                 'f': 'A linha de ensaio certa é «' + certa + '».', 'min': minutos, 'tipo': tipo, 'conceito': 'ensaio', 'pista': PISTA}, **extra)


def vf(rot, p, v, minutos, tipo='aplicar', **extra):
    return dict({'t': 'vf', 'rot': rot, 'p': p, 'p2': 'Outra redação: ' + p[0].lower() + p[1:], 'v': v,
                 'f': 'Volta ao cartão de ensaio e confere a frase.', 'fe': 'A frase de ensaio diz outra coisa: volta ao material.',
                 'min': minutos, 'tipo': tipo, 'conceito': 'ensaio', 'pista': PISTA}, **extra)


def licao(lugares=(0, 2, 1, 0, 1, 2)):
    C = [
        ler('Abre', 'Ensaio do molde', '<div class="m-abre"><p class="carimbo">Caso inventado.</p><p class="caso">Página de ensaio do motor das '
            'sessões: não é uma sessão nem um caso real. Serve para ver os cartões, as posições, os artefactos e o crédito atrás do «i».</p>'
            '<p class="pergunta-sessao" data-artefacto="pergunta" data-rot="A pergunta da sessão">O molde novo funciona do princípio ao fim?</p></div>', 5,
            # 06/11/2026: datas e números com unidade com espaço inseparável, como o contrato passou a exigir (decisão 152)
            aula={'linha': f'ensaio do motor (60{NB}min), pausa, ensaio da parte 2 (50{NB}min), o teu projeto (45{NB}min).'}),
        ler('Decide', 'Antes dos materiais', '<div class="m-decide">' + posicao('posicao-inicio', 'A tua posição no início', 'O molde novo funciona do princípio ao fim?') + '</div>', 8),
        escolha('A linha que fecha', 'Ensaio: qual das três linhas fecha a frase de ensaio?', 'Linha de ensaio certa', ['Linha de ensaio dois', 'Linha de ensaio três'], 3,
                tipo='reconhecer', g='recupera'),
        vf('O que já sabias', 'Ensaio: a frase de ensaio vem da sessão anterior.', True, 4, tipo='reconhecer', g='recupera', origem='m1-s00'),
        ler('Olha', 'Olha', '<div class="m-olha"><p class="ex-antes"><b>Antes de olhar</b> Procura o cartaz e as mãos que o seguram.</p>' + FIG + '</div>', 3),
        escolha('O que a imagem mostra', 'Ensaio: o que se vê na fotografia de ensaio?', 'Um cartaz seguro com as mãos', ['Um livro aberto numa mesa', 'Uma sala vazia de pessoas'], 3, ver=VER),
        dict({'t': 'emparelhar', 'rot': 'Ver e saber', 'p': 'Ensaio: liga cada linha ao seu par.', 'p2': 'Outra redação: liga as linhas de ensaio.',
              'pares': [['Lado de ensaio um', 'Par de ensaio A'], ['Lado de ensaio dois', 'Par de ensaio B'], ['Lado de ensaio três', 'Par de ensaio C']],
              'f': 'Cada lado tem o seu par de ensaio.', 'fe': 'A confusão mais provável é trocar os pares: volta à fotografia.', 'min': 3, 'tipo': 'distinguir',
              'conceito': 'ensaio', 'ver': VER, 'pista': PISTA}),
        ler('Lê', 'Lê', '<div class="m-le"><p class="ex-antes"><b>Antes de ler</b> Procura a palavra que diz o que se protege.</p><blockquote class="lei"><p>'
            f'<span class="art">Ensaio</span>Texto de ensaio no lugar do excerto: a sessão real traz aqui o artigo copiado da fonte oficial, com a referência sem quebra, como no artigo{NB}12.º, n.º{NB}2.</p></blockquote>'
            '<p class="fonte-lei">Fonte de ensaio.</p></div>', 4),
        dict({'t': 'sublinhar', 'rot': 'A palavra que pesa', 'p': 'Ensaio: toca na palavra que diz o que se protege.', 'p2': 'Outra redação: toca na palavra protegida.',
              'frase': 'Texto de ensaio que protege a vida privada', 'certas': [5, 6], 'f': 'As palavras certas são «vida privada».',
              'fe': 'A confusão mais provável é tocar em «protege»: procura o que fica protegido.', 'min': 3, 'tipo': 'reconhecer', 'conceito': 'ensaio',
              'cita': 'Texto de ensaio que protege a vida privada.', 'pista': PISTA}),
        escolha('Ler com exatidão', 'Ensaio: o que diz, com exatidão, o texto de ensaio?', 'Protege a vida privada', ['Protege todas as fotos', 'Proíbe qualquer imagem'], 4),
        vf('Uma situação nova', 'Ensaio: o texto de ensaio vale para uma situação nova.', True, 3),
        dict({'t': 'ordenar', 'rot': 'Facto antes da regra', 'p': 'Ensaio: põe os passos por ordem.', 'p2': 'Outra redação: ordena os passos de ensaio.',
              'passos': ['Passo de ensaio um', 'Passo de ensaio dois', 'Passo de ensaio três'], 'f': 'Primeiro o facto, depois a regra.',
              'fe': 'A confusão mais provável é começar pela regra: volta ao caso.', 'min': 4, 'tipo': 'aplicar', 'conceito': 'ensaio', 'pista': PISTA}),
        ler('Conceito', 'Conceito', '<div class="m-conceito"><table class="tabela"><thead><tr><th>Texto</th><th>O que é</th><th>Obriga?</th></tr></thead><tbody>'
            '<tr><td data-th="Texto">Ensaio A</td><td data-th="O que é">Linha de ensaio</td><td data-th="Obriga?">Não</td></tr>'
            '<tr><td data-th="Texto">Ensaio B</td><td data-th="O que é">Linha de ensaio</td><td data-th="Obriga?">Sim</td></tr>'
            '<tr><td data-th="Texto">Ensaio C</td><td data-th="O que é">Linha de ensaio</td><td data-th="Obriga?">Sim</td></tr></tbody></table>'
            '<p data-artefacto="conceito" data-rot="O conceito">Ensaio: três linhas paralelas ficam numa tabela.</p></div>', 6),
        escolha('Outro caso', 'Ensaio: em que caso novo pesa o conceito de ensaio?', 'No caso de ensaio novo', ['No caso de ensaio velho', 'Em nenhum caso de ensaio'], 4,
                tipo='transferir', origem='m1-s01'),
        vf('A força de cada texto', 'Ensaio: o conceito de ensaio vale também noutro módulo.', False, 3, tipo='transferir'),
        ler('Volta ao caso', 'Volta ao caso', '<div class="m-volta"><p class="parte">Parte 2</p><p class="caso">Texto de ensaio da informação nova que cria o conflito '
            'entre duas razões.</p></div>', 4),
        escolha('A dúvida aberta', 'Ensaio: o que falta saber no caso de ensaio?', 'Falta saber quem pediu', ['Já se sabe o que importa', 'Nada mais pesa no caso'], 3,
                tipo='transferir'),
        ler('Em turma', 'Depois dos materiais', '<div class="m-turma"><p class="pos-antes" data-modelo="No início, a tua posição foi: {posicao-inicio}." hidden></p>'
            + posicao('posicao-depois', 'A tua posição depois', 'Volta à pergunta do início com o que viste.') + '<dl class="campos"><dt>O que se faz</dt>'
            '<dd>Decides outra vez, com o que viste.</dd><dt>Quanto tempo</dt><dd>Treze minutos.</dd><dt>O que fica escrito</dt><dd>Nada: a posição fica nos '
            'teus artefactos.</dd><dt>Se estás sozinho</dt><dd>Compara com a tua escolha do início e abre os três lados.</dd></dl></div>', 13),
        dict({'t': 'emparelhar', 'rot': 'Relato ou princípio', 'p': 'Ensaio: liga cada frase ao que ela é.', 'p2': 'Outra redação: liga as frases de ensaio.',
              'pares': [['Frase de ensaio um', 'Um relato'], ['Frase de ensaio dois', 'Um princípio'], ['Frase de ensaio três', 'Uma dúvida']],
              'f': 'Cada frase de ensaio tem o seu lugar.', 'fe': 'A confusão mais provável é ler um relato como princípio.', 'min': 3, 'tipo': 'aplicar',
              'conceito': 'ensaio', 'pista': PISTA}),
        dict({'t': 'ordenar', 'rot': 'A cadeia', 'p': 'Ensaio: facto, fonte, aplicação, limite, por esta ordem.', 'p2': 'Outra redação: ordena a cadeia de ensaio.',
              'passos': ['Facto de ensaio', 'Fonte de ensaio', 'Aplicação de ensaio', 'Limite de ensaio'], 'f': 'Facto, fonte, aplicação, limite.',
              'fe': 'A confusão mais provável é pôr o limite antes da aplicação.', 'min': 4, 'tipo': 'aplicar', 'conceito': 'ensaio', 'pista': PISTA}),
        escolha('O que as provas dão', 'Ensaio: que conclusão não vai além das provas?', 'Uma conclusão de ensaio prudente', ['Uma conclusão de ensaio exagerada', 'Uma conclusão de ensaio vazia'], 3),
        ler('Agora, em papel', 'Agora, em papel', '<div class="m-papel"><p class="papel-q">O molde novo funciona do princípio ao fim?</p><div class="papel-a6">'
            '<p class="papel-cab"><span>Código</span><span>Data</span></p><ol><li>Conclusão provisória.</li><li>Uma prova.</li><li>Uma dúvida.</li></ol></div>'
            '<details class="mais"><summary>O que conta</summary><div><p>Texto de ensaio dos três critérios.</p></div></details></div>', 15),
        ler('Para levar', '', '<div class="m-levar"><p class="levar" data-artefacto="frase" data-rot="A frase da sessão">'
            + ''.join(f'<span class="ch" style="--i:{i}">{c}</span>' for i, c in enumerate(FRASE)) + '</p>'
            '<p data-modelo="No início decidiste {posicao-inicio}; depois, {posicao-depois}." hidden></p><div data-recolha-lista></div></div>', 5, escuro=True),
    ]
    d = {'id': 'cidadania-m1-ensaio', 'chave': 'epi-cid-m1-s99', 'versao': '2026-11-05-ensaio', 'marca': 'CD', 'molde': L.MOLDE,
         'titulo': 'Ensaio do molde', 'h1': 'Cidadania, ensaio do molde novo (página de teste)', 'piloto': True,
         'modulo': {'n': 1, 'nome': 'Humanos', 'url': L.LENTE + 'cidadania/piloto/m1/'}, 'saida': 'cidadania/piloto/ensaio-molde/index.html',
         'fontes': 'Página de ensaio. Fotografia: Eleanor Roosevelt com a Declaração Universal, Lake Success, novembro de 1949, FDR Presidential Library '
                   '&amp; Museum, 64-165, CC BY 2.0.',
         'tempos': {'folga': 10, 'pausa': 10, 'projeto': 45, 'entrega': 5},
         'pistas': ['Ensaio: as pistas vêm das frases da sessão.', 'Ensaio: a prova está no material antes do exercício.'],
         'depois': '<article class="c"><p class="rot">O passo do teu projeto</p><p class="tit">Ensaio do passo</p><p class="sub">Texto de ensaio do passo de hoje.</p></article>',
         'cartoes': C}
    # as escolhas: a certa fica no lugar pedido, com a semente do motor (com três opções, a ordem não depende de «c»)
    esc = [k for k, c in enumerate(C) if c['t'] == 'escolha']
    for k, lugar in zip(esc, lugares):
        c = C[k]
        ordem = L._mist(L._semente(d['chave'], k), [0, 1, 2])
        cc = ordem[lugar]
        o = list(c.pop('_erradas'))
        o.insert(cc, c.pop('_certa'))
        c.update(o=o, c=cc, fe=['' if j == cc else 'Não é esta: volta ao material de ensaio e procura a prova.' for j in range(3)])
    return d


def copia(**mudancas):
    d = copy.deepcopy(licao())
    d.update(mudancas)
    return d
