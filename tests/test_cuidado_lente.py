"""08/11/2026: decisão 152 («cuidado em todas as lições»), pedido cuidado-lente. Os achados confirmados da varredura de 6/11
(/home/user/bordo/cidadania-v3/cuidado-152/lente-confirmados.json) aplicados ao Lente:

- o manifesto fechado tools/trocas/cuidado-lente-20261108.json leva o main de a99d2d4, letra a letra, ao estado de hoje (e
  volta), com contagem exata, e cada troca pode alinhar-se depois da fusão (o «antigo» nunca está dentro do «novo»);
- cada achado aplicado está nas páginas com o texto exato da proposta final (ou da adaptação ao texto de hoje);
- nenhum dos onze achados recusados («real: false») foi aplicado, e os que ficaram de fora de propósito continuam como estavam;
- as tabelas novas têm cabeçalho de coluna e o nome da coluna em cada célula, e as páginas com tabelas em cartões ligam
  assets/apoio-tabela.css uma vez;
- nada do que entrou traz «professor», «jogo», «jogar», «ficha», «folha», «—», «você» nem um «·» novo, e as referências
  protegidas não voltam a ter espaço normal."""
import importlib.util
import json
import re
import subprocess
import unittest
from pathlib import Path

import cuidado_lente
# 08/11/2026: decisões 153, 162 e 176 (pedido lente-2): a camada dos créditos atrás do «i» (tools/trocas/creditos-i-lente2-20261108.json)
# fica por cima desta; desfaz-se primeiro, com contagem exata, para se conferir esta camada como antes.
import creditos_i_lente2
# 08/11/2026: decisões 153, 162 e 176 (pedido lente-3): a camada dos créditos atrás do «i» das famílias L14 a L19
# (tools/trocas/creditos-i-lente3-20261108.json) fica por cima da do pedido lente-2; desfaz-se primeiro, com contagem exata.
import creditos_i_lente3

R = Path(__file__).resolve().parents[1]
BASE = 'a99d2d469bb3df2a85e1205bf15e820a9cab649e'
NB, WJ = ' ', '⁠'
MANIFESTO = cuidado_lente.TROCAS


def ler(f):
    return (R / f).read_text('utf-8')


def base(f):
    return subprocess.check_output(['git', 'show', f'{BASE}:{f}'], cwd=R).decode('utf-8')


def visivel(f):
    """O texto de uma página com os cartões em JSON lido como o motor o lê (aspas e «</» sem escape)."""
    return ler(f).replace('\\"', '"').replace('<\\/', '</')


def banco(n):
    """Todo o texto dos cartões da lição N da Justiça (leituras, perguntas, opções e retornos)."""
    def textos(v):
        if isinstance(v, str):
            yield v
        elif isinstance(v, dict):
            for x in v.values():
                yield from textos(x)
        elif isinstance(v, list):
            for x in v:
                yield from textos(x)
    return '\n'.join(textos(json.loads(ler(f'tools/justica/bancos/licao-{n}.json'))))


def instalar_carris(texto):
    spec = importlib.util.spec_from_file_location('carris', R / 'tools/gerar_carris.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.instalar(texto)


def isbn(n):
    return 'ISBN' + NB + n.replace('-', '-' + WJ)


def tabela(cab, linhas):
    out = '<table class="apoio-tabela empilha"><tr>' + ''.join(f'<th scope="col">{c}</th>' for c in cab) + '</tr>'
    for linha in linhas:
        out += '<tr>' + ''.join(f'<td data-th="{c}">{v}</td>' for c, v in zip(cab, linha)) + '</tr>'
    return out + '</table>'


OFICINAS_VIVAS = ['arco', 'argumento', 'atelie', 'ator', 'dilema', 'epico', 'manifesto', 'pedacos', 'plano', 'readymade', 'restricao',
                  'texto-imagem', 'visivel']

# Cada achado aplicado (pelo índice «i» da varredura): (ficheiro, leitura, texto exato). A leitura é 'bruto' (o ficheiro como
# está), 'visivel' (cartões em JSON sem escape) ou 'banco-N' (os cartões da lição N da Justiça).
APLICADOS = {
    3: [('banco-1', tabela(['Quem', 'A razão', 'A resposta'], [
        ['<b>Um aluno (6:17)</b>', 'empurrar é uma escolha ativa e mete no caso alguém que estava fora dele.', '<b>Sandel (6:50):</b> o trabalhador do desvio também não escolheu sacrificar a vida.'],
        ['<b>Outro aluno (7:30)</b>', 'empurrar o homem é um assassínio teu; o elétrico desgovernado não o controlas.', '<b>Da sala (8:09):</b> nos dois casos escolhes quem morre, porque virar também é um ato consciente.'],
        ['<b>Andrew (8:29)</b>', 'na ponte estás a matá-lo tu, com as tuas próprias mãos.', '<b>Sandel (8:59):</b> e se o homem estivesse em cima de um alçapão que se abre a rodar um volante?']]))],
    4: [('banco-2', tabela(['Na conta da Ford', 'Quantos', 'A quanto cada'], [['Mortes', '180', f'200{NB}mil dólares'], ['Feridos', '180', f'67{NB}mil'],
                                                                            ['Veículos destruídos', '2000', f'700{NB}dólares']]) + f'<p>Só 49,5{NB}milhões. A Ford não instalou a proteção.</p>')],
    6: [('olhar-e-decidir/justica/aplicar/index.html', tabela(['Projeto', 'Técnica', 'Outra câmara'], [
        ['<strong>A, Estreia</strong>', 'Precisa de aprender.', 'Não tem outra câmara.'], ['<strong>B, Portefólio</strong>', 'Já domina a técnica.', 'Tem uma câmara própria disponível.'],
        ['<strong>C, Memória</strong>', 'Tem alguma experiência.', 'Só pode usar outra câmara num dia.']]))],
    7: [('cidadania/m2/sessoes/02/index.html', '<li>No caso «A regra do feed», ordenem os três conteúdos pelo tempo, depois pelas avaliações. Que critério deve decidir o que aparece primeiro?'
         '<table class="apoio-tabela c10-tabela"><caption>A regra do feed</caption><thead><tr><th scope="col">Conteúdo</th><th scope="col">Atenção média</th><th scope="col">Avaliações positivas</th></tr></thead>'
         f'<tbody><tr><th scope="row">A</th><td data-rotulo="Atenção média">90{NB}segundos</td><td data-rotulo="Avaliações positivas">20</td></tr>'
         f'<tr><th scope="row">B</th><td data-rotulo="Atenção média">45{NB}segundos</td><td data-rotulo="Avaliações positivas">50</td></tr>'
         f'<tr><th scope="row">C</th><td data-rotulo="Atenção média">120{NB}segundos</td><td data-rotulo="Avaliações positivas">10</td></tr></tbody></table></li>')],
    8: [('cidadania/m2/sessoes/03/index.html', '<details data-feedback><summary>Comparar razões</summary><div><table class="apoio-tabela c10-tabela"><thead><tr><th scope="col">Situação</th>'
         '<th scope="col">Direito ou limite</th><th scope="col">Onde está</th></tr></thead><tbody><tr><th scope="row">Publicar uma crítica dura ao horário da escola</th>'
         f'<td data-rotulo="Direito ou limite">Liberdade de expressão: criticar uma instituição está no centro desse direito.</td><td data-rotulo="Onde está">Declaração Universal, artigo{NB}19.º; Constituição, artigo{NB}37.º</td></tr>'
         f'<tr><th scope="row">Fazer uma curta-metragem que ninguém pediu e mostrá-la</th><td data-rotulo="Direito ou limite">Liberdade de criação cultural.</td><td data-rotulo="Onde está">Constituição, artigo{NB}42.º</td></tr>'
         '<tr><th scope="row">Publicar um vídeo a pedir que se expulsem «os de fora» da escola</th><td data-rotulo="Direito ou limite">Passa o limite: apelar à violência ou ao ódio contra pessoas por uma característica do grupo não é opinião, é crime.</td>'
         f'<td data-rotulo="Onde está">Código Penal, artigo{NB}240.º</td></tr></tbody></table><p>Entre a crítica e o crime, a moderação tem de explicar e permitir recurso. O Regulamento dos Serviços Digitais dá três direitos: denunciar, receber uma explicação e recorrer.</p></div></details>')],
    11: [('cidadania/m2/sessoes/08/index.html', '<table class="apoio-tabela c10-tabela c10-colunas"><thead><tr><th scope="col">Intenção</th><th scope="col">Observação</th><th scope="col">Interpretação possível</th></tr></thead>'
          '<tbody><tr><td data-rotulo="Intenção">«O público devia perceber que só avança quem é aplaudido.»</td><td data-rotulo="Observação">«Na viragem, duas pessoas olharam para trás; uma perguntou se podia sair da fila.»</td>'
          '<td data-rotulo="Interpretação possível">«A regra foi sentida, mas não se percebeu que podia ser recusada.»</td></tr></tbody></table>')],
    13: [('narrativas/oficina-argumento/index.html', tabela(['Documento', 'O que é'], [['<b>Logline</b>', 'a premissa e o protagonista numa ou duas frases'], ['<b>Sinopse</b>', 'o enredo resumido, sem as cenas'],
        ['<b>Escaleta</b> (<i>step outline</i>)', 'a lista ordenada de todas as cenas'],
        ['<b>Argumento</b> (em inglês, <i>treatment</i>)', 'a história em prosa corrida, no presente, com princípio, meio e fim, os pontos de viragem e a atmosfera; os diálogos diluídos na prosa, sem travessões'],
        ['<b>Guião</b> (<i>screenplay</i>)', 'cabeçalhos de cena, ação e diálogo, no formato da rodagem']]))],
    17: [('narrativas/oficina-manifesto/index.html', '<p>Um manifesto tem cinco peças.</p>' + tabela(['Peça', 'O que faz'], [['<b>O imperativo</b>', 'não descreve, manda («arregaça as mangas»)'],
        ['<b>A lista</b>', 'pontos numerados ou um rosário de imperativos, sem parágrafos que expliquem'],
        ['<b>O inimigo</b>', 'o que se recusa (o passado, para Marinetti; Dantas, para Almada; os efeitos e a música de fora, para o Dogma)'],
        ['<b>O excesso</b>', 'diz-se de mais, de propósito; um manifesto moderado não é um manifesto'],
        ['<b>A quebra de tom</b>', 'a piada ou a frase terna no meio dos pedidos (o corte de cabelo na fachada), que impede o sermão']]))],
    18: [('narrativas/oficina-pedacos/index.html', tabela(['Técnica', 'Como funciona'], [
        ['<b>Supressão das etiquetas</b>', 'tira os nomes das personagens; o texto vira uma massa de vozes e o leitor tem de ouvir quem fala'],
        [f'<b>Corte e recolagem</b> (<i>cut-up</i>, Burroughs e Gysin, 1959–{WJ}1960)', 'corta o texto em frases e reordena por acaso ou por ritmo; vê o que os encontros novos dizem'],
        ['<b>Repetição e acumulação</b>', 'repete uma palavra ou uma estrutura fora do contexto até perder o sentido literal e ficar só som e textura']]))],
    19: [('narrativas/oficina-plano/index.html', tabela(['Conversão', 'O que muda'], [
        ['<b>Da violência verbal ao grande plano</b>', 'no palco, o insulto precisa de projeção; no cinema, o que importa é o rosto de quem o recebe. Corta para quem ouve.'],
        ['<b>Do espaço fixo à montagem</b>', 'o espectador de teatro vê tudo de uma vez; a câmara escolhe. Plano e contraplano assimétricos, picado e contrapicado, cortes rítmicos dizem quem tem o poder.'],
        ['<b>Do diálogo explicativo à encenação</b>', 'risca as falas que contam o passado ou descrevem estados; passa a informação para um objeto em primeiro plano, para a profundidade de campo, para o que fica fora de campo.']]))],
    20: [('narrativas/oficina-restricao/index.html', tabela(['Unidade', 'O que pede'], [['<b>Ação</b>', 'uma só linha de conflito, sem tramas laterais'], ['<b>Lugar</b>', 'um só espaço, contínuo'],
        ['<b>Tempo</b>', 'o que se passa em cena demora o que demora a representar']])
        + f'<p>A regra vem da leitura que o século{NB}XVI fez da <i>Poética</i> de Aristóteles e foi lei no teatro clássico francês.</p>')],
    # 21: a única palavra mudada é «jogo» (regra da casa), na célula da função poética: «a brincadeira com a própria forma».
    21: [('narrativas/oficina-texto-imagem/index.html', '<p>A tipologia que Santaella e Nöth divulgam em <i>Imagem</i> (1998):</p>' + tabela(['Relação', 'O que acontece'], [
        ['<b>redundância</b>', 'a imagem só ilustra o que o texto já diz'], ['<b>informatividade</b>', 'a imagem traz o essencial e o texto fica marginal'],
        ['<b>complementaridade</b>', 'texto e imagem têm o mesmo peso e só juntos fazem a mensagem']])
        + '<p>No cinema, na publicidade e nos media digitais mandam as duas últimas.</p><p>Das funções da linguagem de Jakobson (1960), três são decisivas numa peça visual:</p>'
        + tabela(['Função', 'O que faz', 'Por exemplo'], [['<b>conativa</b>', 'virada para quem recebe', '«toca aqui», «vem ver»'],
                                                         ['<b>poética</b>', 'a brincadeira com a própria forma', 'o duplo sentido entre a palavra e a imagem'],
                                                         ['<b>fática</b>', 'o contacto, aquilo que prende a atenção', 'a cor, o contraste, o movimento']])
        + '<p>E o <b>não-dito</b>: o que não está escrito mas o leitor lê, porque a imagem o convoca. Um pote fechado diz «guardado» sem a palavra.</p>')],
    22: [('narrativas/oficina-visivel/index.html', tabela(['Sistema', 'O que pode contar'], [
        ['<b>Luz</b>', 'o que se vê e o que se esconde; a cor, o ângulo (zenital, rasante), o tamanho do círculo iluminado'],
        ['<b>Cenário</b>', 'o espaço que fecha ou abre, o que entra e o que sai, a escala do corpo no palco'],
        ['<b>Figurino</b>', 'o que a personagem veste e, sobretudo, o que tira, o que se amarrota, o que troca']]))],
    26: [('banco-3', '<ol><li>Os pobres precisam mais do dinheiro.</li><li>Não é escravatura, porque numa democracia os impostos são votados.</li>'
          '<li>Os ricos devem à sociedade parte do seu sucesso.</li></ol>')],
    27: [('cidadania/m2/sessoes/06/index.html', '<li>Responde às quatro perguntas, por ordem:<ol><li>O que aconteceu? Factos, com data e fonte.</li><li>Quem decidiu? Pessoa, empresa, máquina.</li>'
          '<li>Com que regras? Lei, regras da casa, algoritmo.</li><li>O que podia ter sido diferente, e que direito o permitia?</li></ol></li>'),
         ('cidadania/m2/sessoes/06/index.html', f'A análise crítica de um caso vale 20{NB}% do módulo. É individual.')],
    28: [('cidadania/m2/sessoes/07/index.html', '<li>Escreve o guião, versão 1, em quatro partes:<ol><li>Entrada: o que o público faz ao chegar.</li><li>Regras: o que a peça lhe faz, sem explicar.</li>'
          f'<li>Viragem: o momento em que o público percebe a regra. Pode usar a frase do caso, da casa{NB}6.</li><li>Saída: o que fica a saber.</li></ol></li>')],
    30: [(f'narrativas/oficina-{n}/index.html', '<b>Memória descritiva, cinco linhas</b>No fim, no caderno, uma linha para cada:<ol><li>o que fiz;</li><li>para quem;</li>'
          '<li>que obra ou ideia me guiou;</li><li>o que tirei;</li><li>o que mudava.</li></ol>É o que o júri lê primeiro.') for n in OFICINAS_VIVAS]
        + [(f'narrativas/oficina-{n}-imprimir/index.html', '<span class="linhas"><i>1. O que fiz</i><i>2. Para quem</i><i>3. Que obra ou ideia me guiou</i><i>4. O que tirei</i><i>5. O que mudava</i></span>')
           for n in OFICINAS_VIVAS],
    31: [('narrativas/oficina-arco/index.html', f'tradução nossa: «Que é a vida? Um frenesi.{NB}/ Que é a vida? Uma ilusão,{NB}/ uma sombra, uma ficção;{NB}/ e o maior bem é pequeno,{NB}/ '
          f'porque toda a vida é sonho,{NB}/ e os sonhos, sonhos são.»'),
         ('narrativas/oficina-arco/index.html', f'«¿Qué es la vida? Un frenesí.{NB}/ ¿Qué es la vida? Una ilusión,{NB}/ una sombra, una ficción,{NB}/ y el mayor bien es pequeño:{NB}/ '
          f'que toda la vida es sueño,{NB}/ y los sueños, sueños son.»')],
    32: [('olhar-e-decidir/justica/guiao/index.html', '@media (max-width:639px){table.gr thead th{font-size:.66rem;letter-spacing:0;text-transform:none}table.gr col.c1{width:34%}'
          'table.gr th,table.gr td{overflow-wrap:normal;word-break:normal;padding:4px}table.gr tbody th b{font-size:.74rem}}')],
    33: [('olhar-e-decidir/justica/docente/index.html', '@media (max-width:560px){table.ob col.c1{width:36%}table.ob th,table.ob td{padding:3px;overflow-wrap:normal;word-break:normal}table.ob thead th{font-size:.6rem}}')],
    # 35, 39 e 57 adaptados às sessões no molde final (o resto das referências já vem protegido por tools/cidadania_molde.py).
    35: [('cidadania/m1/sessoes/01/index.html', f'Franklin D.{NB}Roosevelt')],
    39: [('cidadania/m1/sessoes/05/index.html', f'vol.{NB}IV'), ('cidadania/piloto/m1/docente/index.html', f'vol.{NB}IV (Edimburgo')],
    38: [('cidadania/piloto/m1/docente/index.html', f'(TED-Ed, lição de Noah Tavlin, 3{NB}min{NB}42{NB}s)')],
    45: [('narrativas/ideias/sessao-01/index.html', t) for t in (f'julho{NB}de{NB}1891', f'180{NB}minutos', f'70{NB}minutos', f'12,5 por 7,5{NB}centímetros', f'123,5{NB}cm', f'n.º{NB}1661')],
    46: [('narrativas/ideias/sessao-02/index.html', t) for t in (f'180{NB}minutos', f'70{NB}minutos', f'17{NB}cm', f'século{NB}XIX', f'n.º{NB}11131')],
    47: [('banco-1', f'Ver o excerto <span>(1{NB}min{NB}07{NB}s)</span>'), ('banco-1', f'data-dur="1{NB}min{NB}07{NB}s"'), ('banco-1', f'século{NB}XVIII'), ('banco-1', f'século{NB}XIX')],
    48: [('banco-2', t) for t in (f'147{NB}milhões de dólares', f'1200{NB}dólares', f'11{NB}dólares', f'12,5{NB}milhões', f'137{NB}milhões', f'200{NB}mil dólares', f'67{NB}mil',
                                  f'700{NB}dólares', f'49,5{NB}milhões', f'300{NB}mil', f'100{NB}mil', f'4500{NB}dólares', f'(2{NB}min{NB}58{NB}s)', f'data-dur="2{NB}min{NB}58{NB}s"')],
    49: [('banco-3', t) for t in (f'150{NB}dólares', f'14{NB}horas', f'100{NB}dólares', f'31{NB}milhões de dólares', f'47{NB}milhões', f'78{NB}milhões', f'(3{NB}min{NB}45{NB}s)')],
    50: [('olhar-e-decidir/justica/aplicar/index.html', t) for t in (f'explorações 14–{WJ}16, sobre Rawls, e 18–{WJ}20', f'6 a 8{NB}minutos', f'excerto de 25{NB}s')],
    51: [('olhar-e-decidir/justica/docente/index.html', t) for t in (f'(1{NB}min{NB}07{NB}s)', f'11{NB}de{NB}Setembro', f'século{NB}XIX', isbn('978-972-23-6911-4'))]
        + [('olhar-e-decidir/justica/index.html', t) for t in (f'mais de 14{NB}000 até 2009', isbn('978-972-23-6911-4'), f'29{NB}de{NB}maio{NB}de{NB}2025')]
        + [('olhar-e-decidir/justica/guiao/index.html', f'600{NB}euros')],
    52: [('olhar-e-decidir/etica/licao-1/index.html', t) for t in (f'6,9{NB}milhões são 19{NB}000 crianças', f'80{NB}000', f'40{NB}000{NB}dólares', f'17{NB}minutos', f'(17{NB}min)',
                                                                  f'40{NB}segundos', f'41{NB}segundos', f'12{NB}milhões', f'entre 20 e 50{NB}dólares', f'100{NB}euros', f'p.{NB}231',
                                                                  f'novembro{NB}de{NB}1971', f'1548–{WJ}1549', f'3.ª{NB}ed.', isbn('978-989-616-431-7'), isbn('978-972-44-1880-3'),
                                                                  isbn('978-972-662-723-4'), isbn('978-972-44-2839-0'))],
    53: [('olhar-e-decidir/etica/licao-2/index.html', t) for t in (f'vol.{NB}83, n.º{NB}4, 1974, pp.{NB}435–{WJ}450', f'3.ª{NB}ed.', isbn('978-972-662-421-9'), isbn('978-972-8531-69-0'),
                                                                  isbn('972-662-655-2'))],
    54: [('olhar-e-decidir/estetica/licao-1/index.html', t) for t in (f'(1711–{WJ}1776)', f'(1724–{WJ}1804)', f'século{NB}XVIII', f'século{NB}XVII;', f'vol.{NB}5', f'3.ª{NB}ed.',
                                                                     isbn('978-972-44-2633-4'), isbn('978-972-27-2454-8'), f'J.{NB}H.{NB}Bernard')],
    55: [('cidadania/m2/sessoes/06/index.html', f'Reporter X, n.º{NB}9, 4{NB}de{NB}outubro{NB}de{NB}1930, p.{NB}3'), ('cidadania/m2/sessoes/04/index.html', f'83(4), 1974, pp.{NB}435–{WJ}450'),
         ('cidadania/m2/sessoes/01/index.html', f'(1907–{WJ}1998)'), ('cidadania/m2/sessoes/05/index.html', f'(1815–{WJ}1852)'), ('cidadania/m2/sessoes/06/index.html', f'(Lisboa, 1897–{WJ}1935)'),
         ('cidadania/m2/sessoes/08/index.html', f'(1711–{WJ}1776)'), ('cidadania/m2/sessoes/06/index.html', f'11{NB}de{NB}junho{NB}de{NB}1917'),
         # «agosto de 1945» está no cartão de obra do Orwell, que nenhuma sessão mostra (a 09 tem o caso em português): confere-se na fonte.
         ('cidadania/m2/sessoes/09/index.html', f'5{NB}de{NB}fevereiro{NB}de{NB}1916'), ('tools/cidadania_m2_molde.py', 'agosto\\u00a0de\\u00a01945'),
         ('cidadania/m2/sessoes/06/index.html', f'3{NB}de{NB}março'), ('cidadania/m2/sessoes/03/index.html', f'artigo{NB}19.º'), ('cidadania/m2/sessoes/04/index.html', f'artigo{NB}19.º'),
         ('cidadania/m2/sessoes/03/index.html', f'artigos{NB}VII a{NB}IX'), ('cidadania/m2/sessoes/09/index.html', f'capítulo{NB}II'), ('cidadania/m2/sessoes/02/index.html', f'(2{NB}min{NB}58{NB}s)'),
         ('cidadania/m2/sessoes/02/index.html', f'415{NB}TWh'), ('cidadania/m2/sessoes/02/index.html', f'62{NB}milhões'), ('cidadania/m2/sessoes/index.html', f'125 e 20{NB}minutos')],
    56: [('cidadania/m2/sessoes/index.html', t) for t in (f'6{NB}horas', f'a pausa de 10{NB}minutos e cerca de 20{NB}minutos', f'os 125{NB}minutos')],
    57: [('cidadania/m1/sessoes/04/index.html', f'livro{NB}VII'), ('cidadania/piloto/m1/docente/index.html', f'ainda diz 5 a 8{NB}minutos'),
         ('cidadania/piloto/m1/docente/index.html', f'(_República_, livro{NB}VII)'.replace('_República_', '<i>República</i>')),
         ('cidadania/piloto/m1/docente/index.html', f'tortura do século{NB}XVI')],
    58: [('narrativas/ideias/docente/index.html', t) for t in (f'(4{NB}min{NB}50{NB}s)', f'70{NB}minutos', f'180{NB}minutos', f'50{NB}minutos', f'25{NB}minutos', f'7,5{NB}centímetros',
                                                              )]
        # o crédito da fotografia do atol (ATOL) não está hoje em nenhuma página: confere-se na fonte
        + [('tools/ideias_piloto.py', '9\\u00a0de\\u00a0março\\u00a0de\\u00a02003')]
        + [('biblioteca/young-tecnica-1940/index.html', f'1{NB}min de leitura')],
    59: [('biblioteca/caeiro-guardador-xx/index.html', f'pp.{NB}53–{WJ}54'), ('biblioteca/orta-benjui/index.html', f'vol.{NB}I, p.{NB}105–{WJ}106'),
         ('biblioteca/reporterx-reporterxizar-1930/index.html', f'(1885–{WJ}1953)'), ('biblioteca/reporterx-reporterxizar-1930/index.html', f'n.º{NB}8, 27{NB}de{NB}setembro{NB}de{NB}1930, p.{NB}3'),
         ('biblioteca/einstein-introducao/index.html', f'vol.{NB}17'), ('biblioteca/campos-tabacaria/index.html', f'15{NB}de{NB}janeiro{NB}de{NB}1928'),
         ('biblioteca/vitruvio-liber-1-caput-3/index.html', f'séc.{NB}I a.C.'), ('biblioteca/metalogicon-anoes/index.html', f'livro{NB}III, capítulo{NB}4'),
         ('biblioteca/garrett-frei-luis-sousa/index.html', f'D.{NB}Sebastião'), ('biblioteca/cesario-sentimento-ocidental/index.html', f'S.{NB}Petersburgo'),
         ('biblioteca/codax-ondas-vigo/index.html', f'século{NB}XIII'), ('biblioteca/caeiro-guardador-xx/index.html', f'1{NB}min')],
    60: [('narrativas/oficina-arco/index.html', f'Oficina · 45 a 60{NB}min de exploração · 10{NB}min de preparação'), ('narrativas/oficina-readymade/index.html', f'(1864–{WJ}1946)'),
         ('narrativas/oficina-ator/index.html', f'(1863–{WJ}1938)'), ('narrativas/oficina-pedacos/index.html', f'(1959–{WJ}1960)'),
         ('narrativas/oficina-ficcao-comecar-imprimir/index.html', f'5–{WJ}8{NB}minutos'), ('narrativas/oficina-ficcao-comecar-imprimir/index.html', f'0:49–{WJ}1:08'),
         ('narrativas/oficina-ficcao-personagem-imprimir/index.html', f'1:54–{WJ}2:22'), ('narrativas/oficina-matriz-imprimir/index.html', f'2:27–{WJ}2:59'),
         ('narrativas/oficina-matriz-imprimir/index.html', f'32{NB}segundos'), ('narrativas/oficina-atelie/index.html', f'5{NB}de{NB}agosto{NB}de{NB}1473'),
         ('narrativas/oficina-atelie/index.html', f'século{NB}XV'), ('narrativas/oficina-manifesto/index.html', f'Rua D.{NB}Luís{NB}I'),
         ('narrativas/oficina-manifesto/index.html', f'16{NB}de{NB}outubro{NB}de{NB}2026'), ('narrativas/oficina-dilema/index.html', f'ato{NB}III, cena{NB}1')],
    61: [('narrativas/treinar/a-entrevista/index.html', f'12{NB}min de escrita'), ('narrativas/treinar/index.html', f'12{NB}min de escrita'),
         ('narrativas/treinar/a-entrevista/index.html', f'n.º{NB}54829'), ('narrativas/treinar/docente/index.html', f'<td>5 a 12{NB}min</td>'),
         ('narrativas/treinar/docente/index.html', f'outubro{NB}de{NB}2026')],
}
# O que voltaria a partir-se: a forma antiga não pode reaparecer nas mesmas páginas.
ANTIGOS = {
    'olhar-e-decidir/etica/licao-1/index.html': ['19 000', '80 000', '40 000', '6,9 milhões', '1548-1549', 'p. 231'],
    'olhar-e-decidir/etica/licao-2/index.html': ['pp. 435-450', 'vol. 83', '3.ª ed.'],
    'olhar-e-decidir/estetica/licao-1/index.html': ['(1711-1776)', '(1724-1804)', 'J. H. Bernard', 'vol. 5'],
    'olhar-e-decidir/justica/docente/index.html': ['min 07 s', '11 de Setembro', 'ISBN 978'],
    'olhar-e-decidir/justica/index.html': ['14 000', 'ISBN 978', '29 de maio de 2025'],
    'tools/justica/bancos/licao-1.json': ['1 min 07 s', 'século XVIII'],
    'tools/justica/bancos/licao-2.json': ['147 milhões', '2 min 58 s'],
    'tools/justica/bancos/licao-3.json': ['3 min 45 s', '78 milhões'],
    'cidadania/m2/sessoes/04/index.html': ['pp. 435-450'],
    'biblioteca/caeiro-guardador-xx/index.html': ['pp. 53–54'],
    'biblioteca/garrett-frei-luis-sousa/index.html': ['D. João', 'D. Sebastião'],
}
# Os onze recusados (real: false): o ficheiro de destino não traz a tabela proposta (e o texto, quando existe, fica como estava).
RECUSADOS = {
    1: ('tools/licoes/cidadania-m1-s08.py', '<th scope="col">Quem decide</th>', None),
    2: ('tools/licoes/cidadania-m1-s03.py', '<th scope="col">Medida</th>', None),
    5: ('banco-3', '<summary>As três leis</summary>', '1. Leis paternalistas'),
    9: ('tools/cidadania_m1_editorial.py', '<th scope="col">Meio</th>', "reading='Teatro: falas, ação e espaço."),
    10: ('tools/cidadania_m1_editorial.py', '<th scope="col">Palavra</th>', "reading='O objetivo é o que a personagem procura;"),
    14: ('narrativas/oficina-dramaturgista/index.html', 'apoio-tabela', None),
    15: ('narrativas/oficina-ficcao-espaco/index.html', 'apoio-tabela', None),
    16: ('narrativas/oficina-ficcao-genero/index.html', 'apoio-tabela', None),
    23: ('narrativas/oficina-arco/index.html', 'apoio-tabela', '<p>Na <b>exposição</b> semeia-se tudo o que o desenlace vai precisar.'),
    24: ('narrativas/oficina-dilema/index.html', 'apoio-tabela', 'é uma estrutura com três perguntas. <b>Quem quer o quê</b> (o objetivo de cada um).'),
    25: ('narrativas/oficina-readymade/index.html', 'apoio-tabela', 'passa a obra por três gestos: a <b>escolha</b> (entre mil, este),'),
}
# As páginas (e fontes) com tabelas novas: nenhuma outra.
COM_TABELA = {'olhar-e-decidir/justica/licao-1/index.html', 'olhar-e-decidir/justica/licao-2/index.html', 'olhar-e-decidir/justica/aplicar/index.html',
              'cidadania/m2/sessoes/02/index.html', 'cidadania/m2/sessoes/03/index.html', 'cidadania/m2/sessoes/08/index.html'} | {
    f'narrativas/oficina-{n}/index.html' for n in ('argumento', 'manifesto', 'pedacos', 'plano', 'restricao', 'texto-imagem', 'visivel')}
PROIBIDAS = re.compile(r'(?<![\wÀ-ÿ])(?:professor(?:a|es|as)?|jog(?:ar|a[sm]?|o|os|ou|uei|ámos)|fichas?|folhas?|vocês?)(?![\wÀ-ÿ])|—|·', re.I)


def conteudo(chave):
    if chave.startswith('banco-'):
        return banco(int(chave.split('-')[1]))
    if chave.endswith('.json') or chave.endswith('.py') or chave.endswith('.css'):
        return ler(chave)
    return visivel(chave)


class CuidadoLente(unittest.TestCase):
    def test_manifesto_fechado_e_reversivel(self):
        self.assertTrue(MANIFESTO)
        for f, trocas in MANIFESTO.items():
            with self.subTest(ficheiro=f):
                # 08/11/2026: pedido lente-2. A camada dos créditos atrás do «i» parte do main cc75fc6, já com esta: desfaz-se
                # primeiro (contagem exata de cada «novo»); o que fica tem de ser, como antes, este manifesto sobre o main a99d2d4.
                # 08/11/2026: pedido lente-3. A camada dos créditos das famílias L14 a L19 parte do main fec58ae, já com a do pedido
                # lente-2: desfaz-se antes dela (contagem exata de cada «novo»); o resto confere-se como antes.
                agora = creditos_i_lente2.desfazer(creditos_i_lente3.desfazer(ler(f), f), f)
                for antigo, novo, n in trocas:
                    self.assertGreater(n, 0)
                    self.assertNotIn(antigo, novo, 'o «antigo» dentro do «novo» impede alinhar depois da fusão')
                    self.assertEqual(agora.count(novo), n, novo[:80])
                    self.assertNotIn(antigo, agora, antigo[:80])
                # desfeita a camada, fica o main de partida, letra a letra (na entrada da Justiça, com a linha do «i» que
                # tools/gerar_carris.py escreve hoje: a data do crédito sai do gerador)
                esperado = base(f)
                if f == 'olhar-e-decidir/justica/index.html':
                    esperado = instalar_carris(esperado)
                self.assertEqual(cuidado_lente.desfazer(agora, f), esperado)
                self.assertEqual(cuidado_lente.aplicar(esperado, f), agora)
                self.assertEqual(cuidado_lente.alinhar(agora, f), agora)

    def test_cada_achado_aplicado_com_o_texto_exato(self):
        for i, casos in APLICADOS.items():
            for chave, texto in casos:
                with self.subTest(achado=i, ficheiro=chave):
                    self.assertIn(texto, conteudo(chave))

    def test_formas_antigas_nao_voltam(self):
        for f, antigos in ANTIGOS.items():
            s = ler(f)
            for a in antigos:
                with self.subTest(ficheiro=f, antigo=a):
                    self.assertNotIn(a, s)

    def test_nenhum_recusado_aplicado(self):
        for i, (chave, proposta, trecho) in RECUSADOS.items():
            with self.subTest(recusado=i):
                s = conteudo(chave) if (R / chave).exists() or chave.startswith('banco-') else ''
                self.assertNotIn(proposta, s)
                if trecho:
                    self.assertIn(trecho, s)

    def test_nao_aplicados_de_proposito(self):
        # Ficam fora desta camada (nenhuma troca no manifesto) e sem a proposta, enquanto as páginas existirem:
        # 0: a s01 foi reescrita no molde final (#126) e já tem a sua tabela «Texto, Tipo, Obriga?»; a proposta da varredura não entra.
        s01 = ler('tools/licoes/cidadania-m1-s01.py')
        self.assertIn('<table class="tabela"><thead><tr><th scope="col">Texto</th><th scope="col">Tipo</th><th scope="col">Obriga?</th>', s01)
        self.assertNotIn('Que força tem', s01)
        # 12: o guia antigo do M1 descreve as sessões de cinco passos, que já não existem; o guia do molde tem os seus quadros.
        self.assertNotIn('Minutos por passo', ler('tools/cidadania_m1_layout.py'))
        # 29: o caso das seis sessões já não chega a nenhuma sessão; o apoio 09 do percurso anterior fica como estava.
        self.assertNotIn('Projeto A: já tem quatro cenas', ler('tools/cidadania_m1_conteudos.py'))
        fora = ['cidadania/m1/sessoes/index.html', 'cidadania/m1/fichas/f09/index.html', 'tools/cidadania_m1_layout.py', 'tools/cidadania_m1_conteudos.py',
                'tools/cidadania_m1_sessoes.py', 'tools/cidadania_m1_editorial.py', 'tools/cidadania_m1_molde.py', 'tools/videos-cidadania-m1.json']
        # 35 a 44: as páginas antigas do piloto (cidadania/piloto/m1-sNN/) já não têm gerador (redirecionam-se no pedido 3).
        fora += [f'cidadania/piloto/m1-s{n:02d}/index.html' for n in range(1, 11)]
        for f in fora:
            with self.subTest(ficheiro=f):
                self.assertNotIn(f, MANIFESTO)
                if (R / f).exists() and f.endswith('.html'):
                    self.assertNotIn('Minutos por passo', ler(f))
                    self.assertNotIn('Projeto A: já tem quatro cenas', ler(f))

    def test_tabelas_novas_bem_formadas(self):
        paginas = {str(p.relative_to(R)) for p in R.glob('**/*.html') if '.git' not in p.parts and 'node_modules' not in p.parts
                   and p.parts[len(R.parts)] != 'tools' and 'apoio-tabela' in p.read_text('utf-8')}
        self.assertEqual(paginas, COM_TABELA)
        for f in sorted(COM_TABELA):
            s = visivel(f) if 'justica/licao-' not in f else banco(int(f.split('licao-')[1][0]))
            tabelas = re.findall(r'<table class="apoio-tabela[^"]*">.*?</table>', s, re.S)
            self.assertTrue(tabelas, f)
            for t in tabelas:
                with self.subTest(pagina=f, tabela=t[:60]):
                    cab = re.findall(r'<th scope="col">(.*?)</th>', t)
                    self.assertGreaterEqual(len(cab), 2)
                    for linha in re.findall(r'<tr>(.*?)</tr>', t)[1:] if 'empilha' in t else re.findall(r'<tbody>(.*?)</tbody>', t):
                        rotulos = re.findall(r'<td data-(?:th|rotulo)="([^"]*)"', linha)
                        self.assertTrue(rotulos)
                        self.assertTrue(set(rotulos) <= set(cab), (rotulos, cab))
                    self.assertNotIn('<td>', t)
            if 'c10-tabela' not in s:
                pagina = ler(f)
                self.assertEqual(pagina.count('assets/apoio-tabela.css?v=20261108-1'), 1, f)
                # a folha vem depois dos estilos da página, para valer sobre eles (mesma especificidade)
                self.assertGreater(pagina.index('apoio-tabela.css'), pagina.rindex('</style>'), f)

    def test_folha_da_tabela_de_apoio(self):
        css = ler('assets/apoio-tabela.css')
        self.assertIn('@media (max-width:560px){', css)
        self.assertIn('td[data-th]:not(:first-child)::before{content:attr(data-th) ": "', css)
        # só as cores do tema (claro e escuro em assets/appearance.css), nenhuma cor fixa sem token
        for cor in re.findall(r'#[0-9a-fA-F]{3,6}', css):
            self.assertRegex(css, r'var\(--[\w-]+,' + re.escape(cor) + r'\)')

    def test_regras_de_texto_no_que_entrou(self):
        # Em cada troca, nada de novo do que as regras da casa proíbem (o «·» das linhas de metadados já lá estava; a troca
        # pode tirar, nunca acrescentar), e só espaço sem quebra ou junção onde antes havia espaço ou hífen.
        for f, trocas in MANIFESTO.items():
            for antigo, novo, n in trocas:
                with self.subTest(ficheiro=f, novo=novo[:60]):
                    for m in set(x.group(0).lower() for x in PROIBIDAS.finditer(novo)):
                        self.assertLessEqual(len(re.findall(re.escape(m), novo, re.I)), len(re.findall(re.escape(m), antigo, re.I)), m)
                    self.assertNotIn('Você', novo)
        # e nenhuma referência protegida aparece, nos ficheiros mudados, com espaço normal ao lado da forma nova
        for i in (45, 46, 47, 48, 49, 51, 52, 53, 54, 56, 58, 59, 61):
            for chave, texto in APLICADOS[i]:
                if NB in texto and ' ' not in texto:
                    with self.subTest(achado=i, texto=texto):
                        self.assertNotIn(texto.replace(NB, ' ').replace(WJ, ''), conteudo(chave).replace(WJ, ''))


if __name__ == '__main__':
    unittest.main()
