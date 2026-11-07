# Fonte da sessão 10 do M1 de Cidadania, «O que consegues defender?», na versão final do molde cidadania-2026-11 (plano do molde,
# secção 2, «Variantes», e secção 3, linha «10»; decisões 144 a 146, 152 a 155, 159, 161 e 166 a 168). 07/11/2026: substitui a fonte
# do piloto de 31/10, que escrevia cidadania/piloto/m1-s10/ (essa página fica como está até ao pedido 3, que faz os redirecionamentos
# do piloto de uma vez); a chave epi-cid-m1-s10 é a mesma, e a versão sobe com preservarAnterior (cfg da família). Corre-se para
# escrever o .json ao lado; o .json é que o gerador (tools/licoes_lente.py) lê, e nunca se edita à mão. Os cartões montam-se com o
# ajudante comum tools/cidadania_molde.py. A sessão de mostra não tem excertos de lei: o Lê são os arranques de frase da defesa, e
# nenhum cartão cita um texto legal (nada a acrescentar ao registo tools/cidadania_fontes.json).
#
# Sessão de mostra («variante»: «mostra», só das sessões 10; o validador aplica-lhe o contrato da variante e nenhuma outra sessão o
# usa): núcleo curto com 7 de fazer, o Ponto de chegada em papel antes do cartão 1 (10 minutos, decisão 179, as mesmas dez perguntas do Ponto de
# partida, como na sessão 01), a mostra individual de 3 minutos com 2 de defesa por aluno (decisão 159) no «Em turma», com a pausa a
# meio, e três linhas em papel no fim. 14 cartões (7 de ler, 7 de fazer): Abre, Decide, quatro Recupera (R1 a obra, Camus; R2 a R4
# um item novo das sessões 01 a 03, 04 a 06 e 07 a 09), Olha, um exercício com o cartaz, Lê, a charneira 1, a mostra, a charneira 2,
# «Agora, em papel» e Para levar. A ordem é fixa (cfg.aula) e a resposta certa de cada escolha fica no lugar pedido em LUGARES,
# calculado com a semente do motor. Cada exercício tem a sua pista, que não dá a resposta. O que só o docente faz vive no guia
# (tools/cidadania_piloto.py, GUIA['10']), nunca aqui.
#
# Fontes abertas a 7/11/2026, uma de cada vez (nada citado de memória):
# - Cartaz: _Federal Theatre presents «… one-third of a nation»_, Federal Theatre Project, Adelphi Theatre, Nova Iorque, entre 1936 e
#   1939, serigrafia, «made by WPA Federal Art Project, N.Y.C.», Library of Congress, Work Projects Administration Poster Collection,
#   LCCN 95509661. O registo da Library of Congress (loc.gov) não abriu nesta passagem (desafio a robôs, que não se contornou); leu-se a
#   cópia do registo no Wikimedia Commons (File:Federal_Theatre_presents_"..._one-third_of_a_nation"_LCCN95509661.jpg): título,
#   resumo («Poster for Federal Theatre Project presentation of "...one-third of a nation" at the Adelphi Theatre, showing drawing of
#   urban row houses»), «No known restrictions on publication» e domínio público (obra de um funcionário da WPA). O ficheiro
#   img/cidadania/one-third-of-a-nation-cartaz.webp (640 × 996) é o do piloto, visto: o mesmo cartaz. O nome do desenhador que o piloto
#   dava não está no registo e sai.
# - Ticiano, _Sísifo_, entre 1548 e 1549, óleo sobre tela, 237 × 216 cm, Museo Nacional del Prado, P00426: registo do Wikimedia
#   Commons (File:Punishment_sisyph.jpg), domínio público (autor morto em 1576, PD-Art). O ficheiro img/cidadania/sisifo.webp
#   (881 × 1000), visto, é essa pintura.
# - Albert Camus, _O Mito de Sísifo_ (1942): o cartão diz só que o livro acaba com a ideia de que é preciso imaginar Sísifo feliz (a
#   frase final do livro); não se cita a tradução, protegida.
# - Os arranques de frase do Lê vêm da sessão 10 publicada do percurso anterior (cidadania/m1/sessoes/10/, «Mostrar o guião, explicar
#   as escolhas»), já no singular.
# - Caso real (decisão 161): 07/11/2026 (revisão): a sessão não tem caso real confirmado. O registo da Library of Congress do cartaz
#   não abriu outra vez (loc.gov com desafio a robôs; lccn.loc.gov/95509661 leva ao catálogo, que respondeu «No Connections
#   Available» ao pedido do registo), e a cópia do Commons não é fonte oficial: o cartão 8 deixa de se apresentar como caso real e
#   fica como transferência com o cartaz. O caso da Inês, o da Joana, o da ordem das mostras, o da Rita e o da fila do bar são
#   inventados.
# - 07/11/2026 (revisão): o registo do Prado (P00426, museodelprado.es) também não abriu (Cloudflare recusou o pedido); o crédito do
#   Sísifo fica com os dados do registo do Commons, e o guia di-lo.
# - Vídeo (decisão 155): nenhum. O plano não propõe candidato, e o vídeo do piloto (TED-Ed, Aristóteles e Joshua Bell) sai.
import importlib.util, json, pathlib

AQUI = pathlib.Path(__file__).resolve()
ROOT = AQUI.parents[2]


def _carregar(nome, rel):
    spec = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M = _carregar('cidadania_molde', 'tools/cidadania_molde.py')
L = _carregar('licoes_lente', 'tools/licoes_lente.py')
NB = M.NB

CARTAZ = '../../../../img/cidadania/one-third-of-a-nation-cartaz.webp'
CARTAZ_ALT = ('Cartaz de fundo escuro. Ao centro, um desenho de prédios apertados, vistos de cima, com roupa estendida; por cima, em letras '
              'grandes e inclinadas, «… one-third of a nation». Em cima, «Federal Theatre presents»; em baixo, «A living newspaper about '
              'housing» e «Adelphi Theatre».')
CARTAZ_ALT_VER = 'O mesmo cartaz: prédios apertados vistos de cima, o título «… one-third of a nation» e, em baixo, «A living newspaper about housing».'
# 07/11/2026 (revisão): o endereço permanente do registo que a cópia do Commons dá (lccn.loc.gov), em vez de www.loc.gov/item/.
LOC = 'https://lccn.loc.gov/95509661'
COMMONS_CARTAZ = ('https://commons.wikimedia.org/wiki/File:Federal_Theatre_presents_%22..._one-third_of_a_nation%22_LCCN95509661.jpg')
CARTAZ_CREDITO = ('<i>Federal Theatre presents «… one-third of a nation»</i>, cartaz do Federal Theatre Project para o Adelphi Theatre, Nova '
                  'Iorque, entre 1936 e 1939, serigrafia feita pelo WPA Federal Art Project. Library of Congress, Work Projects Administration '
                  f'Poster Collection (LCCN 95509661). <a href="{LOC}">Registo na Library of Congress</a>. '
                  f'<a href="{COMMONS_CARTAZ}">Registo no Wikimedia Commons</a>. Domínio público.')
SISIFO = '../../../../img/cidadania/sisifo.webp'
SISIFO_ALT = ('Pintura escura: um homem musculado, de pano branco e faixa à cintura, curvado sob um rochedo enorme que segura sobre a '
              'cabeça e os ombros, a subir uma encosta; à direita, chamas.')
# 07/11/2026 (revisão): espaço inseparável nas medidas (decisão 152).
SISIFO_CREDITO = (f'Ticiano, <i>Sísifo</i>, entre 1548 e 1549, óleo sobre tela, 237{NB}×{NB}216{NB}cm. Museo Nacional del Prado, Madrid (P00426). '
                  '<a href="https://commons.wikimedia.org/wiki/File:Punishment_sisyph.jpg">Registo no Wikimedia Commons</a>. Domínio público.')
VER_SISIFO = M.figura(SISIFO, SISIFO_ALT, SISIFO_CREDITO, 'Ticiano, <i>Sísifo</i>, entre 1548 e 1549.', largura=881, altura=1000,
                      rotulo_i='Créditos da pintura')
VER_CARTAZ = f'<img src="{CARTAZ}" alt="{CARTAZ_ALT_VER}">'
PERGUNTA = 'Uma resposta que admite um limite fica mais fraca?'
DECIDE_Q = 'A Inês deve dizer, na defesa, que só entrevistou duas pessoas?'
FRASE = 'Uma boa resposta diz o que sabe, de onde o sabe e o que ainda não sabe.'
R4_FRASE = 'Os alunos de informática percebem todos de computadores, por isso a Rita vai arranjar o projetor.'

# Os arranques de frase da defesa (sessão 10 publicada do percurso anterior), em tabela (decisão 152): o arranque e o que mostra.
ARRANQUES = [('Parti desta pergunta…', 'a pergunta que investigaste'),
             ('Esta fonte ajudou-me a compreender…', 'de onde vem o que dizes'),
             ('Na cena central, a personagem escolhe…', 'o que a peça põe em cena'),
             ('Depois da leitura dos colegas, mudei…', 'o que a revisão mudou'),
             ('Ainda reconheço este limite…', 'o que a tua resposta ainda não sabe')]
TABELA = ('<table class="tabela"><thead><tr><th scope="col">Arranque</th><th scope="col">O que mostra</th></tr></thead><tbody>'
          + ''.join(f'<tr><td data-th="Arranque">«{a}»</td><td data-th="O que mostra">{b}</td></tr>' for a, b in ARRANQUES)
          + '</tbody></table>')


def escolha(rot, p, p2, certa, erradas, f, minutos, tipo, conceito, **extra):
    """Uma escolha de três opções; a certa vai para o lugar de LUGARES (preenchido em sessao())."""
    c = M.fazer('escolha', rot, p, p2, f, minutos, tipo, conceito, **extra)
    c['_certa'], c['_erradas'] = M.ref(certa), [(M.ref(o), M.ref(e)) for o, e in erradas]
    return c


def palavras(frase, alvo):
    """Os índices das palavras de «alvo» na frase do sublinhar (sem a pontuação colada)."""
    w = [x.strip('.,;:') for x in frase.split()]
    return [w.index(a) for a in alvo]


CARTOES = [
 # ---------------------------------------------------------------- antes da mostra (30 minutos, depois do Ponto de chegada)
 # O caso do piloto («Isso é só a vossa opinião», cartão 2) passa ao singular e ganha o limite que a pergunta da sessão pede.
 M.abre('O que consegues defender?',
        # 07/11/2026: decisão 179 (docente). Ponto de chegada em 10 minutos e mostra em 125 (135 com a pausa); o total fica em 180.
        f'o Ponto de chegada em papel (10{NB}min), recuperar e ler (20{NB}min), a mostra (135{NB}min, com a pausa a meio) e o fecho '
        f'(15{NB}min).',
        'Na mostra, a Inês apresenta o seu teatro-documento sobre a falta de lugares na cantina, feito com uma contagem dos lugares e '
        'duas entrevistas. Na defesa, um colega diz: «Isso é só a tua opinião.» A Inês sabe de onde vem cada fala da peça, mas também '
        'sabe que só entrevistou duas pessoas. Tem dois minutos para responder.',
        PERGUNTA, minutos=2),
 M.decide(DECIDE_Q, [
     ('Quem acha que sim', 'Se for ela a dizê-lo, ninguém a apanha em falta. Esconder o que falta é pior do que o admitir.'),
     ('Quem acha que não', 'Dois minutos são pouco. Se falar do que falta, o público pode lembrar-se só da fraqueza.'),
     ('Uma objeção', 'E se ela mostrar primeiro de onde vem a resposta, e só depois o que ainda não sabe?')], minutos=2),
 # R1, a obra do #84 s10: Camus e Sísifo, com o Sísifo de Ticiano em miniatura. A obra apresentada numa linha; a pergunta liga-a à
 # revisão depois da mostra. Os distratores são os dois erros reais diante de uma objeção: não mexer em nada ou deitar tudo fora.
 M.recupera(escolha(
     'A pedra outra vez',
     'Camus fecha o ensaio _O Mito de Sísifo_ (1942): é preciso imaginar Sísifo feliz, a recomeçar com a mesma pedra. Depois da '
     'mostra, o que fazes com a tua resposta?',
     'Para Camus, é preciso imaginar Sísifo feliz, a recomeçar com a mesma pedra. Depois de defenderes a tua resposta, o que fazes com '
     'ela?',
     'Revê-la com as objeções que ouviste.',
     [('Guardá-la tal como a apresentaste.',
       'A pedra não fica lá em cima, e Sísifo recomeça com ela. Guardar a resposta como estava é fazer de conta que a objeção não '
       'aconteceu. '
       'Volta à pedra: o que faz Sísifo com ela?'),
      ('Trocar de pergunta e começar do zero.',
       'Sísifo recomeça com a mesma pedra, não com outra. Uma objeção pede uma segunda versão da tua resposta, não uma pergunta nova. '
       'Volta à pedra: é a mesma ou outra?')],
     'Sísifo recomeça com a mesma pedra. Na tua resposta, recomeçar é revê-la com as objeções que ouviste, sem deitar fora o que já '
     'provaste.',
     2, 'aplicar', 'rever depois da objeção', ver=VER_SISIFO,
     pista='Pensa no que uma objeção pede à resposta que já tens.')),
 # R2 (sessões 01 a 03): um item novo do consentimento para um uso (sessão 02), sobre as entrevistas do projeto.
 M.recupera(M.fazer(
     'emparelhar', 'O sim da Joana',
     'Sessão 02: a Joana deixou gravar a voz dela para o podcast da turma. Liga cada situação ao que vale o sim dela.',
     'A Joana disse que sim à gravação da voz para o podcast da turma. Em cada situação, o que vale esse sim?',
     'Na sessão 02, viste que o «consentimento» vale para o uso que se explicou: aqui, o podcast. Para a tua peça, pede-se outra vez; '
     'e, se a Joana o retirar, respeita-se.',
     2, 'aplicar', 'consentimento para um uso',
     pares=[['Pôr a gravação no podcast da turma', 'Cabe no sim que deu'],
            ['Usar um excerto no teu teatro-documento', 'Pede um sim novo'],
            ['A Joana pede que a voz saia do podcast', 'Respeita-se: o sim pode ser retirado']],
     fe='A confusão mais provável é achar que o sim para o podcast serve para tudo. Vale para o uso que se explicou, e pode ser '
        'retirado. Relê o que a Joana autorizou.',
     pista='Pergunta, em cada linha, se é o mesmo uso que a Joana autorizou.'),
     origem='cidadania/m1/sessoes/02/'),
 # R3 (sessões 04 a 06): escolher a regra sem saber o lugar (sessão 06), num caso novo: a ordem das mostras de hoje.
 M.recupera(M.fazer(
     'ordenar', 'A ordem das mostras',
     'Sessão 06: é preciso decidir a ordem das mostras. Põe por ordem os passos para escolher a regra sem saber o teu lugar.',
     'Para decidir quem mostra primeiro, por que ordem se escolhe a regra sem saber o lugar de cada um?',
     'Primeiro as regras em cima da mesa; depois a escolha, ainda «sem saber o lugar», como na sessão 06; só então os números; no '
     'fim, a voz de quem perde.',
     2, 'aplicar', 'escolher sem saber o lugar',
     passos=['Juntar as regras propostas para a ordem das mostras.',
             'Escolher uma regra para a ordem.',
             'Tirar à sorte o número de cada um na lista.',
             'Ouvir a objeção de quem ficou para o fim.'],
     fe='A confusão mais provável é tirar os números antes de escolher a regra: quem já sabe o seu número escolhe a pensar em si. '
        'Relê os passos pela ordem do tempo.',
     pista='Pergunta-te o que muda se cada um já souber o seu número quando escolhe.'),
     origem='cidadania/m1/sessoes/06/'),
 # R4 (sessões 07 a 09; a s09 deixa de ficar de fora): um item novo do estereótipo (sessão 09).
 M.recupera(M.fazer(
     'sublinhar', 'Onde está o estereótipo',
     'Sessão 09: nesta frase, toca na palavra que faz dela um estereótipo.',
     'Toca na palavra que, nesta frase, transforma uma ideia sobre um curso num estereótipo.',
     'A palavra «todos» diz o mesmo de toda a gente de um curso, sem prova: é o que faz um «estereótipo», como viste na sessão 09. A '
     'Rita pode perceber de computadores ou não; a frase não o prova.',
     2, 'reconhecer', 'estereótipo', frase=R4_FRASE, certas=palavras(R4_FRASE, ['todos']),
     fe='A confusão mais provável é tocar em «alunos» ou em «informática»: dizem de quem se fala, não que se diz o mesmo de cada um '
        'deles. Procura a palavra que estende a ideia a toda a gente do curso.',
     pista='Procura a palavra que fala de muitas pessoas como se fossem uma só.'),
     origem='cidadania/m1/sessoes/09/'),
 M.olha('Um cartaz do Federal Theatre', 'Olha primeiro para o desenho; só depois lê as palavras.',
        M.figura(CARTAZ, CARTAZ_ALT, CARTAZ_CREDITO, 'Cartaz de uma peça do Federal Theatre, em Nova Iorque, entre 1936 e 1939.',
                 artefacto='Um cartaz do Federal Theatre, Nova Iorque', largura=640, altura=996, rotulo_i='Créditos do cartaz'),
        minutos=2),
 # Transferência com o cartaz: o que o cartaz diz da peça, levado ao teu teatro-documento. 07/11/2026 (revisão): deixa de se apresentar
 # como caso real (decisão 161), porque o registo da Library of Congress não se abriu.
 escolha('Um jornal em palco',
         'O cartaz chama à peça «a living newspaper about housing», um jornal vivo sobre a habitação. Em que se parece com o teu '
         'teatro-documento?',
         'Um «jornal vivo» sobre a habitação, num teatro de Nova Iorque: em que se parece essa peça com o teu teatro-documento?',
         'Leva para o palco um assunto real.',
         [('Conta a vida de uma pessoa inventada.',
           'O cartaz não fala de uma personagem: diz que a peça é um jornal sobre a habitação, um assunto que existe fora do palco. Volta '
           'às palavras do cartaz.'),
          ('Diz só a opinião de quem a escreveu.',
           'O cartaz não fala de opiniões: diz que a peça é um jornal sobre a habitação. Um jornal trata de assuntos reais. Volta às '
           'palavras do cartaz.')],
         'O cartaz chama à peça um jornal vivo sobre a habitação: um assunto real, posto em cena. O teu teatro-documento também leva para '
         'o palco um assunto real, com as fontes que investigaste.',
         2, 'transferir', 'teatro-documento', ver=VER_CARTAZ,
         liga=[{'t': 'Ver o registo do cartaz na Library of Congress', 'href': LOC}],
         pista='Relê as palavras do cartaz sobre a peça e pensa no que a tua peça foi buscar às fontes.'),
 M._ler('Lê', 'Para responder a uma objeção',
        '<div class="m-le"><p class="ex-antes"><b>Antes de ler</b> Cinco maneiras de começar uma frase na defesa. Cada uma mostra uma '
        f'parte do teu trabalho.</p>{TABELA}</div>', 2),
 # Charneira 1 (piloto, cartão 15, no singular): a resposta que mostra de onde vem. Os distratores são as respostas reais a uma
 # objeção: o direito à opinião (que aceita a objeção) e a convicção (que não mostra prova).
 escolha('Mais do que opinião',
         'A Inês ouve: «Isso é só a tua opinião.» Encontra a resposta que mostra que não é.',
         'Depois da peça, alguém diz à Inês que aquilo é só opinião. Encontra a resposta que desfaz a objeção.',
         'Contei os lugares numa semana: faltaram em quatro dias.',
         [('Tenho direito à minha opinião, como toda a gente.',
           'Assim, a Inês aceita que é só opinião e põe de lado a contagem e as entrevistas. A objeção pede de onde vem a resposta. Volta '
           'ao caso: o que tem a Inês, além da opinião?'),
          ('Acredito mesmo nisto e defendi-o com convicção.',
           'A convicção mostra o que a Inês sente, não de onde vem o que diz. Quem objetou continua sem saber em que se apoia a resposta. '
           'Volta ao caso: em que se apoia a Inês?')],
         'Uma contagem com dias e números mostra de onde vem a resposta, e quem objetou pode confirmá-la. É o que faz o arranque «Esta '
         'fonte ajudou-me a compreender…».',
         2, 'aplicar', 'opinião e prova', pista='Relê, no Lê, a linha sobre de onde vem o que dizes.'),
 # ---------------------------------------------------------------- a mostra (125 minutos, com a pausa a meio) e o fecho
 # 07/11/2026 (revisão): 120 minutos, 24 alunos a 5 minutos (decisão 159: cerca de 125; os 5 que faltam eram pergunta ao docente).
 # 07/11/2026: decisão 179 (docente). O Ponto de chegada passa a 10 minutos e a mostra fica com os 125 da decisão 159 (25 alunos).
 M.em_turma(DECIDE_Q, [
     ('Quem acha que sim', 'Um dos arranques é «Ainda reconheço este limite…»: dizer o que falta também é responder.'),
     ('Quem acha que não', 'Em dois minutos de defesa, o limite pode ficar como a única coisa que o público ouve.'),
     ('Uma objeção', 'E se a Inês começar por «Esta fonte ajudou-me a compreender…» e deixar o limite para o fim?')],
     {'O que se faz': 'Mostras a peça, respondes a uma objeção e decides outra vez.',
      'Quanto tempo': 'Três minutos de mostra e dois de defesa.',
      'O que fica escrito': 'Nada no ecrã; a escolha fica nos artefactos.',
      'Se estás sozinho': 'Mostra a peça em voz alta, três minutos no relógio, e responde em dois à objeção do início.'},
     titulo='A mostra', minutos=125, intro='', nota=None),
 # Charneira 2 («reconhecer um limite não enfraquece», piloto, cartão 16, sem o absoluto do piloto): o limite das entrevistas não
 # apaga a contagem. O erro esperado é achar que admitir uma fraqueza estraga tudo.
 M.fazer('vf', 'O limite e a contagem',
         'A Inês diz na defesa: «Ainda reconheço este limite: só entrevistei duas pessoas.» Com isso, a contagem dos lugares deixa de '
         'valer como prova.',
         'Depois de a Inês admitir que só entrevistou duas pessoas, a contagem dos lugares perde o valor de prova.',
         'É falso: o limite fala das entrevistas, não da contagem, que continua a provar o que provava. Dizer o limite mostra até onde '
         'chega uma das provas e deixa a outra como estava.',
         2, 'aplicar', 'limite e prova', v=False,
         fe='Admitir que entrevistou poucas pessoas não apaga a contagem: são duas provas diferentes. O limite diz até onde chega uma '
            'delas. Volta à frase da Inês e vê se fala da contagem ou das entrevistas.',
         pista='Separa as duas provas da Inês e vê de qual fala o limite.'),
 M.papel(PERGUNTA,
         ['O que defendes, depois da objeção que ouviste.',
          'A tua prova mais forte: um facto e a fonte, com uma expressão exata entre aspas.',
          'O limite: o que a tua resposta ainda não sabe.'],
         ['A resposta diz o que defendes, sem ir além das provas.',
          'A prova junta um facto à sua fonte, com uma expressão exata entre aspas.',
          'O limite é verdadeiro: se tivesse resposta, podia mudar o que defendes.'],
         '<p>Outro caso, inventado: uma peça sobre a fila do bar.</p><ol>'
         '<li>Defendo: o bar devia abrir mais cedo.</li>'
         '<li>Prova: contei 31 alunos na fila às 10h15; a funcionária disse «não dá tempo».</li>'
         '<li>Limite: só contei numa semana.</li></ol>',
         'Num papel pequeno, sozinho e sem telemóvel.', minutos=6, relogio_min=6),
 M.levar(FRASE, ['Dizer o limite protege a parte que está provada.',
                 'Mudar a resposta por uma boa razão faz parte de investigar.'], minutos=2),
]

# o lugar da certa em cada escolha (0, 1 ou 2), com a semente do motor: com três escolhas, um lugar diferente em cada uma
LUGARES = (1, 2, 0)

# O passo do projeto: na sessão de mostra, o projeto é a própria mostra; o passo do fim é a revisão depois da objeção (o enunciado
# da Pergunta Humana, «Teatro-documento e defesa»: «capacidade de explicar e defender as próprias escolhas»).
DEPOIS = ('<article class="c"><p class="rot">O passo do teu projeto</p><p class="tit">Depois da mostra</p>'
          '<p class="sub">No dossiê, escreve o que mudarias na peça depois da objeção que ouviste, porquê, e o limite que ficou por '
          'resolver. O que conta: a mudança responde à objeção; a razão aponta para uma fonte; o limite é dito com clareza.</p>'
          '<p class="ir"><a href="../../../projeto/#av-teatro">O teatro-documento e a defesa, no enunciado da Pergunta Humana</a></p></article>')


def sessao():
    d = {
        'id': 'cidadania-m1-s10', 'chave': 'epi-cid-m1-s10', 'versao': '2026-11-07-molde', 'marca': 'CD', 'molde': L.MOLDE,
        # 07/11/2026: a variante do plano para as sessões 10 (secção 2, «Variantes»), com nome, para o validador lhe aplicar o seu
        # contrato (tools/licoes_lente.py, validar_molde) sem mexer nas regras das outras sessões.
        'variante': 'mostra',
        'titulo': 'Sessão 10: O que consegues defender?', 'h1': 'Cidadania, módulo 1, sessão 10: O que consegues defender?',
        'modulo': {'n': 1, 'nome': 'Humanos', 'url': L.LENTE + 'cidadania/piloto/m1/'},
        'saida': 'cidadania/m1/sessoes/10/index.html',
        'seguinte': '../../../piloto/m1/', 'seguinteRotulo': 'As 10 sessões',
        'fontes': M.ref('Cartaz: _Federal Theatre presents «… one-third of a nation»_, Federal Theatre Project, Nova Iorque, entre 1936 e 1939, '
                        'serigrafia do WPA Federal Art Project, Library of Congress (LCCN 95509661), domínio público. Pintura: Ticiano, '
                        '_Sísifo_, entre 1548 e 1549, Museo Nacional del Prado, domínio público. Albert Camus, _O Mito de Sísifo_ (1942). '
                        'Os arranques de frase da defesa vêm da sessão 10 do percurso anterior. O caso da Inês, o da Joana, o da ordem das '
                        'mostras, o da Rita e o da fila do bar são inventados. A sessão não tem caso real confirmado: o registo do cartaz '
                        'na Library of Congress não se abriu, só a sua cópia no Wikimedia Commons.'),
        # 07/11/2026 (variante «mostra»): o Ponto de chegada em papel antes do cartão 1, a pausa a meio da mostra e a entrega; não há
        # folga nem passo do projeto à parte (a mostra é o projeto).
        'tempos': {'ponto': 10, 'pausa': 10, 'entrega': 5},  # 07/11/2026: decisão 179, o Ponto de chegada em 10 minutos
        'depois': DEPOIS,
        'cartoes': CARTOES,
    }
    esc = [k for k, c in enumerate(CARTOES) if c['t'] == 'escolha']
    assert len(esc) == len(LUGARES), (len(esc), len(LUGARES))
    for k, lugar in zip(esc, LUGARES):
        c = CARTOES[k]
        if '_certa' not in c:
            continue
        ordem = L._mist(L._semente(d['chave'], k), [0, 1, 2])
        cc = ordem[lugar]
        erradas = c.pop('_erradas')
        o, fe = [x for x, _ in erradas], [y for _, y in erradas]
        o.insert(cc, c.pop('_certa'))
        fe.insert(cc, '')
        c.update(o=o, c=cc, fe=fe)
    return d


if __name__ == '__main__':
    d = sessao()
    p = AQUI.with_suffix('.json')
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', 'utf-8')
    print(p, len(d['cartoes']), 'cartões', sum(1 for c in d['cartoes'] if c['t'] != 'ler'), 'de fazer')
