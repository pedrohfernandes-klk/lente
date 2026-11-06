# Fonte da sessão 04 do M1 de Cidadania, «Posso dizer tudo?», na versão final do molde cidadania-2026-11 (plano do molde, secção 3,
# linha «04»; decisões 144 a 146, 152 a 155, 161 e 166 a 168). 06/11/2026: substitui a fonte do piloto de 31/10, que escrevia
# cidadania/piloto/m1-s04/ (essa página fica como está até ao pedido 3, que faz os redirecionamentos do piloto de uma vez); a
# chave epi-cid-m1-s04 é a mesma, e a versão sobe com preservarAnterior (cfg da família). Corre-se para escrever o .json ao lado;
# o .json é que o gerador (tools/licoes_lente.py) lê, e nunca se edita à mão. Os cartões montam-se com o ajudante comum
# tools/cidadania_molde.py; cada excerto de lei ou de acórdão vem do registo tools/cidadania_fontes.json (texto exato da fonte
# oficial, aberta a 6/11/2026, confirmado) e o ajudante recusa escrever um excerto que lá não esteja.
#
# 23 cartões (9 de ler, 14 de fazer), pela ordem e com os tempos da secção 2 do plano, como a s01; a ordem é fixa (cfg.aula) e a
# resposta certa de cada escolha fica no lugar pedido em LUGARES, calculado com a semente do motor. Cada exercício tem a sua pista,
# que não dá a resposta. O que só o docente faz vive no guia (tools/cidadania_piloto.py, GUIA['04']), nunca aqui.
#
# Fontes abertas a 6/11/2026, uma de cada vez (nada citado de memória):
# - Constituição, artigos 26.º, 37.º e 13.º, texto consolidado no Diário da República Eletrónico (registo crp-26-1, crp-37-1,
#   crp-37-2, crp-37-3; o 13.º, n.º 2, só se refere, sem citação);
# - Convenção sobre os Direitos da Criança, artigo 13.º, na tradução portuguesa anexa à Resolução da Assembleia da República n.º
#   20/90, no Diário da República Eletrónico, com as Retificações n.º 1/91 e n.º 8/91 (registo cdc-13-1, cdc-13-2);
# - Acórdão do Tribunal da Relação de Évora de 21/3/2017, processo 373/14.8T9STR.E1, em dgsi.pt (registo tre-2017-*): o caso real
#   da sessão (decisão 161);
# - Imagem do Olha: Wikimedia Commons, File:Les_Poires_(1834).jpg (registo lido pela API do Commons): «Design by Honoré Daumier
#   (possibly) after Charles Philipon's lithograph published in La Caricature in 1831. Wood engraver unknown.», «17 January 1834»,
#   Gallica bpt6k3058046f/f3, «Public domain». A página da Gallica não abriu (bloqueio do servidor), por isso a ligação do «i» é a
#   do Commons, que cita a Gallica. O ficheiro img/cidadania/les-poires-1834.webp (640 × 626) é o recorte do piloto: os quatro
#   desenhos com as legendas, que se leram na imagem.
# - Miniatura do R1: Wikimedia Commons, File:Platon_Cave_Sanraedam_1604.jpg: Jan Saenredam, segundo Cornelis van Haarlem, 1604,
#   British Museum 1852,1211.120, «Public domain». O ficheiro img/cidadania/caverna.webp (1100 × 802) é o mesmo, visto.
# - Vídeo (decisão 155): nenhum. O candidato do plano, «How false news can spread» (TED-Ed, lição de Noah Tavlin, 3 min 42 s), está
#   no sítio oficial (ed.ted.com, aberto a 6/11/2026), mas a equipa não o viu por inteiro; fica no guia, para o docente decidir.
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

IMG = '../../../../img/cidadania/les-poires-1834.webp'
ALT = ('Quatro desenhos a traço, dois em cima e dois em baixo, cada um com uma legenda em francês por baixo. O rosto de um homem de '
       'patilhas e cabelo encaracolado vai ganhando, de desenho para desenho, a forma de uma pera; no último, é uma pera com folhas, '
       'com marcas no lugar dos olhos e da boca.')
# 06/11/2026: no cartão, o motor mostra a imagem em miniatura, recortada a 210 px de altura (lesson.css, .ver-fig); para que nada
# importante fique de fora, os cartões 6 e 7 levam recortes do mesmo documento (domínio público, como o original), feitos de
# img/cidadania/les-poires-1834.webp: o 3.º e o 4.º desenhos lado a lado, e os quatro numa linha, sem as legendas.
VER_BAIXO = ('<img src="../../../../img/cidadania/les-poires-1834-baixo.webp" alt="Pormenor: o terceiro desenho, um rosto já quase '
             'em forma de pera, e o quarto, a pera, lado a lado.">')
VER_TIRA = ('<img src="../../../../img/cidadania/les-poires-1834-tira.webp" alt="Os quatro desenhos numa linha, pela ordem da página: '
            'o rosto do rei vai ganhando, de um para o outro, a forma de uma pera.">')
COMMONS_POIRES = 'https://commons.wikimedia.org/wiki/File:Les_Poires_(1834).jpg'
CREDITO = ('<i>Les Poires</i>, gravura em madeira publicada em <i>Le Charivari</i>, 17 de janeiro de 1834. Desenho talvez de Honoré '
           'Daumier, a partir de uma litografia de Charles Philipon (<i>La Caricature</i>, 1831); gravador desconhecido. Gallica, '
           'Biblioteca Nacional de França, bpt6k3058046f, f. 3. '
           f'<a href="{COMMONS_POIRES}">Registo de origem</a>. Domínio público.')
CAVERNA = '../../../../img/cidadania/caverna.webp'
COMMONS_CAVERNA = 'https://commons.wikimedia.org/wiki/File:Platon_Cave_Sanraedam_1604.jpg'
CREDITO_CAVERNA = ('Jan Saenredam, segundo Cornelis van Haarlem, <i>Antrum Platonicum</i>, gravura, 1604. British Museum, 1852,1211.120. '
                   f'<a href="{COMMONS_CAVERNA}">Registo de origem</a>. Domínio público.')
VER_CAVERNA = M.figura(CAVERNA, 'Gravura antiga: à direita, uma multidão virada para um muro alto, onde se veem figuras; à esquerda, '
                       'uma abertura deixa entrar a luz de fora.', CREDITO_CAVERNA,
                       'Jan Saenredam, <i>A caverna de Platão</i>, 1604.', largura=1100, altura=802)
DRE = 'https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-aprovacao-constituicao/1976-34520775'
DRE_CDC = 'https://diariodarepublica.pt/dr/detalhe/resolucao-assembleia-republica/20-1990-222390'
DGSI = 'https://www.dgsi.pt/jtre.nsf/134973db04f39bf2802579bf005f080b/abfc60d25966d946802581080032685a?OpenDocument'
PERGUNTA = 'Onde acaba a crítica e começa o ataque?'
DECIDE_Q = 'A conta de memes deve ser apagada?'
FRASE = 'Sem censura antes, com responsabilidade depois.'
COMENTARIO = ('antes de contratar mais funcionários deve pagar os ordenados em atraso e a fornecedores! Faz constantemente o mesmo: '
              'os funcionários passam de bestial a besta em segundos, e não paga o que deve! Não tem vergonha')


def escolha(rot, p, p2, certa, erradas, f, minutos, tipo, conceito, **extra):
    """Uma escolha de três opções; a certa vai para o lugar de LUGARES (preenchido em sessao())."""
    c = M.fazer('escolha', rot, p, p2, f, minutos, tipo, conceito, **extra)
    c['_certa'], c['_erradas'] = M.ref(certa), [(M.ref(o), M.ref(e)) for o, e in erradas]
    return c


CARTOES = [
 # ---------------------------------------------------------------- parte 1, ver antes de concluir (60 minutos)
 # O caso da conta de memes vem do piloto (s04, cartão 1), reescrito: sem «grupo» (decisão 146) e sem a resposta no caso.
 M.abre('Posso dizer tudo?',
        f'ver e ler (60{NB}min), pausa (10{NB}min), pesar e escrever (50{NB}min) e o teu projeto (45{NB}min).',
        'A conta anónima de memes da escola publica um desenho do diretor com cara de pera, por causa das regras novas do bar. Num '
        'comentário, alguém escreve: «E o Diogo, do 10.º B, rouba na cantina.» Em dois dias, o comentário corre a escola. O Diogo diz '
        'que é mentira. Ninguém diz que viu.',
        PERGUNTA),
 M.decide(DECIDE_Q, [
     ('Quem acha que sim', 'A conta espalhou uma acusação contra um colega. Apagá-la é a maneira mais rápida de parar o dano.'),
     ('Quem acha que não', 'A pera critica as regras do diretor, e criticar quem manda é um direito. Apagar a conta cala também isso.'),
     ('Uma objeção', 'E se saísse só o comentário sobre o Diogo? Quem decidia o que fica e o que sai?')]),
 # R1: a obra do #84 s04, a caverna de Platão (_República_, livro VII), com a gravura de Saenredam em miniatura. Só a premissa da
 # alegoria: os prisioneiros só conhecem as sombras na parede e tomam-nas pela realidade.
 M.recupera(escolha(
     'Sombras na parede',
     'Na alegoria da caverna, de Platão, os prisioneiros passam a vida a olhar para sombras numa parede. Porque as tomam pela '
     'realidade?',
     'Os prisioneiros da caverna de Platão nunca saíram dali e só veem sombras na parede. O que os faz tomá-las pelas próprias coisas?',
     'Nunca viram as coisas que fazem as sombras.',
     [('Alguém os convenceu de que as sombras eram reais.',
       'Na alegoria, ninguém precisa de os convencer: presos desde sempre, só conhecem as sombras e não têm com que as comparar. '
       'Repara, na gravura, para onde está virada a multidão.'),
      ('As sombras são mais nítidas do que as coisas.',
       'Não é uma questão de nitidez. Quem só viu sombras não tem com que as comparar. Repara, na gravura, para onde está virada a '
       'multidão e por onde entra a luz.')],
     'Só conhecem as sombras, por isso tomam-nas pela verdade. Com um comentário que corre a escola passa-se o mesmo: quem só o viu '
     'repetido não sabe de onde vem. Para saber, vai-se à origem.',
     3, 'reconhecer', 'aparência e realidade', ver=VER_CAVERNA,
     pista='Pensa no que os prisioneiros têm, ou não têm, para comparar.')),
 # R2: consentimento para um uso (sessão 02), um item novo: a caricatura de um colega reconhecível. Falso (os V/F são F, V, F).
 M.recupera(M.fazer(
     'vf', 'Um sim para um uso',
     'Caso inventado: a Inês deixa o Tiago mostrar à turma uma caricatura dela, bem reconhecível. Com esse sim, ele pode publicá-la '
     'também na conta de memes.',
     'A Inês aceitou que a caricatura dela fosse mostrada à turma. Então, o Tiago também a pode pôr na conta de memes.',
     'Falso. A Inês disse que sim a mostrar a caricatura à turma, não a publicá-la numa conta que toda a escola vê. É a ideia da '
     'sessão 02: «O sim vale para o uso que se explicou.»',
     4, 'aplicar', 'consentimento para um uso', v=False,
     fe='Um sim não passa de um uso para outro: a Inês aceitou a turma, não a conta de memes. É o que viste na sessão 02: «Aceitar '
        'ser filmado não é aceitar ser publicado.» Volta ao caso e vê para que uso foi o sim.',
     pista='Pergunta-te para que uso a Inês disse que sim.'),
     origem='cidadania/m1/sessoes/02/'),
 M.olha('Um rei que vira pera', 'Procura o desenho em que o rosto deixa de ser o do rei.',
        M.figura(IMG, ALT, CREDITO, 'Quatro desenhos do jornal francês <i>Le Charivari</i>, 17 de janeiro de 1834. O primeiro rosto é o '
                 'do rei Luís Filipe.', artefacto='Quatro desenhos de 1834: o rei que vira pera', largura=640, altura=626)),
 M.fazer('vf', 'O que resta do rosto',
         'Na pera do último desenho, ainda se veem marcas do rosto dos desenhos anteriores.',
         'O último desenho já é uma pera, mas guarda alguma coisa do rosto que vinha de trás.',
         'Verdadeiro. No meio da pera há marcas no lugar dos olhos e da boca, onde estavam no terceiro desenho. A pera ainda se '
         'parece com ele.',
         3, 'distinguir', 'observar', v=True, ver=VER_BAIXO,
         fe='Olha para o meio da pera: há marcas onde estavam os olhos e a boca. Compara-a com o terceiro desenho, ao lado.',
         pista='Compara o meio da pera com o terceiro desenho.'),
 escolha('Onde passa a linha',
         'Em que desenho deixa o rosto de ser o do rei?',
         'De desenho para desenho, o rosto do rei passa a pera. Onde se pode dizer «aqui já não é o rei»?',
         'Em nenhum: cada um parece-se com o anterior.',
         [('No último, porque aí já só se vê uma pera.',
           'A pera ainda tem as marcas dos olhos e da boca do terceiro desenho. Se o terceiro é o rei, a pera parece-se com ele. Volta '
           'à imagem e compara os dois.'),
          ('No segundo, porque aí a cara já está deformada.',
           'Esse desenho é quase igual ao primeiro: o mesmo cabelo, as mesmas patilhas, o mesmo queixo. Se o primeiro é o rei, o '
           'segundo também. Compara os dois.')],
         'Não há um desenho em que se possa traçar a linha. Diz a última legenda, em francês, que, por coerência, não se poderia '
         'absolver a pera, parecida com os esboços anteriores. Proibir um desenho por se parecer com o rei não tem onde parar.',
         3, 'aplicar', 'proibir uma forma', ver=VER_TIRA, pista='Compara cada desenho com o que está antes dele.'),
 M.le('Antes e depois de publicar', 'Procura o que vem antes de publicar e o que vem depois.',
      [(f'N.º{NB}1', 'Todos têm o direito de exprimir e divulgar livremente o seu pensamento pela palavra, pela imagem […]', 'crp-37-1', 'n1'),
       (f'N.º{NB}2', 'O exercício destes direitos não pode ser impedido ou limitado por qualquer tipo ou forma de censura.', 'crp-37-2', 'n2'),
       (f'N.º{NB}3', 'As infracções cometidas no exercício destes direitos ficam submetidas aos princípios gerais de direito criminal […]',
        'crp-37-3', 'n3')],
      f'Constituição, artigo 37.º, no <a href="{DRE}">Diário da República</a>.',
      mais=('<p class="glossa"><b>Infracções</b>: o que se faz contra a lei. O n.º 3 continua: quem as julga são os tribunais ou '
            'uma entidade administrativa independente.</p>')),
 M.fazer('sublinhar', 'A palavra que corta antes',
         'No n.º 2, toca na palavra que nomeia o corte feito por outros ao que vais dizer, antes de chegar a quem lê.',
         'No n.º 2 do artigo 37.º, que palavra nomeia o controlo do que se publica, feito antes de sair? Toca nela.',
         '«Censura»: alguém que revê e corta o que se vai publicar, antes de sair. O n.º 2 diz que nenhum tipo ou forma dela pode '
         'impedir ou limitar a liberdade de expressão.',
         3, 'reconhecer', 'censura',
         frase='O exercício destes direitos não pode ser impedido ou limitado por qualquer tipo ou forma de censura.',
         certas=[16], fonte='crp-37-2', l='n2',
         fe='A confusão mais provável é tocar em «impedido» ou «limitado»: dizem o que não pode acontecer à liberdade, não o nome de '
            'quem corta. Procura esse nome no fim da frase.',
         pista='Lê a frase do n.º 2 até ao fim.'),
 M.fazer('emparelhar', 'Cada situação, o seu número',
         'Três situações novas: liga cada uma ao número do artigo 37.º que se aplica.',
         'Que número do artigo 37.º está em causa em cada uma destas situações?',
         'Fazer uma caricatura é exprimir-se pela imagem (n.º 1); aprovar cada texto antes de sair é controlo prévio (n.º 2); julgar o '
         'que já saiu é a resposta depois (n.º 3).',
         4, 'aplicar', 'censura e responsabilidade',
         pares=[['Um aluno publica a caricatura de um ministro.', f'Artigo 37.º, n.º{NB}1'],
                ['A direção quer aprovar cada texto do jornal da escola antes de sair.', f'Artigo 37.º, n.º{NB}2'],
                ['Um tribunal julga um texto já publicado num jornal.', f'Artigo 37.º, n.º{NB}3']],
         fe='A confusão mais provável é trocar o n.º 2 pelo n.º 3: o n.º 2 trata do que se corta antes de sair; o n.º 3, do que se '
            'responde depois. Volta aos dois números e vê quando acontece cada situação.',
         pista='Pergunta-te, em cada situação, se o texto já saiu.'),
 # A Convenção, artigo 13.º, n.º 2, com a frase inteira (plano), no próprio cartão.
 escolha('A razão que não está lá',
         'Caso inventado: uma aluna de 15 anos publica um vídeo a pedir comida vegetariana na cantina. A escola manda apagá-lo, por ela '
         'ser menor. A Convenção aceita essa razão?',
         'Uma aluna de 15 anos pede, num vídeo, comida vegetariana na cantina. Mandam-na apagá-lo por ser menor. O artigo 13.º, n.º 2, '
         'aceita isso?',
         'Não: ser menor não é uma das razões do n.º 2.',
         [('Sim: até aos 18 anos, quem decide é a escola.',
           'A Convenção diz o contrário: «A criança tem direito à liberdade de expressão». Só se pode restringir com uma lei e por uma '
           'das razões do n.º 2. Volta ao artigo e procura a idade.'),
          ('Sim: o vídeo atinge a reputação de outrem.',
           'Pedir comida vegetariana não acusa ninguém de nada. O n.º 2 fala dos «direitos e da reputação de outrem», isto é, de '
           'outras pessoas. Volta ao artigo: quem é atingido pelo vídeo?')],
         'O n.º 2 só admite restrições «previstas na lei e que sejam necessárias» para duas coisas: os direitos e a reputação dos '
         'outros, ou a segurança, a ordem, a saúde e a moral públicas. A idade não está lá.',
         3, 'aplicar', 'restrições à liberdade de expressão',
         cita=('O exercício deste direito só pode ser objecto de restrições previstas na lei e que sejam necessárias: a) Ao respeito dos '
               'direitos e da reputação de outrem; b) À salvaguarda da segurança nacional, da ordem pública, da saúde ou da moral '
               'públicas.'),
         fonte='cdc-13-2',
         citacoes=[('cdc-13-1', 'A criança tem direito à liberdade de expressão'), ('cdc-13-2', 'direitos e da reputação de outrem'),
                   ('cdc-13-2', 'previstas na lei e que sejam necessárias')],
         pista='Procura a idade entre as razões do n.º 2.'),
 # Charneira 1: o erro esperado é ler o n.º 2 sozinho («sem censura, ninguém responde»).
 M.fazer('vf', 'Sem censura não é sem resposta',
         'Como a Constituição proíbe a censura, a conta pode publicar o comentário sobre o Diogo sem ter de responder por ele.',
         'Sem censura prévia, quem gere a conta de memes fica livre de responder pelo que lá publica sobre o Diogo.',
         'Falso. O n.º 2 impede que alguém corte antes; o n.º 3 diz que as infrações ficam submetidas aos princípios do direito '
         'criminal. Sem censura antes, com responsabilidade depois.',
         4, 'aplicar', 'censura e responsabilidade', v=False,
         citacoes=[('crp-37-3', 'princípios gerais de direito criminal')],
         fe='O n.º 2 não está sozinho: o n.º 3 diz que as infracções ficam submetidas aos «princípios gerais de direito criminal». '
            'Não haver corte antes não apaga a resposta depois. Volta ao artigo e lê o n.º 3 a seguir ao n.º 2.',
         pista='Lê o n.º 3 logo a seguir ao n.º 2.'),
 M.conceito('Quatro maneiras de falar de alguém',
            '<p>A pera e o comentário: são a mesma coisa?</p>',
            '<table class="tabela"><thead><tr><th scope="col">Tipo</th><th scope="col">O que faz</th></tr></thead><tbody>'
            '<tr><td data-th="Tipo">Crítica</td><td data-th="O que faz">discute uma decisão</td></tr>'
            '<tr><td data-th="Tipo">Sátira</td><td data-th="O que faz">exagera quem manda</td></tr>'
            '<tr><td data-th="Tipo">Acusação de facto</td><td data-th="O que faz">afirma um facto sobre alguém</td></tr>'
            '<tr><td data-th="Tipo">Ataque pela origem</td><td data-th="O que faz">visa pessoas pela origem</td></tr>'
            '</tbody></table>',
            'Acusação de facto', 'Dizer que alguém fez uma coisa concreta, verdadeira ou falsa.',
            '<p>Não é opinião: «o diretor manda mal» discute-se; «o Diogo rouba» prova-se.</p>',
            mais='<p>Sobre a origem, a Constituição diz que ninguém pode ser prejudicado em razão, entre outras, do território de origem, '
                 'da língua ou da religião (artigo 13.º, n.º 2).</p>'),
 M.fazer('emparelhar', 'Quatro publicações, quatro tipos',
         'Caso inventado: quatro publicações na página de outra escola. Liga cada uma ao seu tipo.',
         'De que tipo é cada uma destas publicações, inventadas, de outra escola?',
         'Pôr em causa uma regra é crítica; o semáforo exagera quem manda; dizer que o treinador fica com o dinheiro acusa uma pessoa '
         'concreta, e prova-se ou não; visar colegas pelo país de onde vêm é atacá-los pela origem.',
         3, 'transferir', 'quatro tipos de publicação',
         pares=[['As regras novas do bar são injustas para quem chega cedo.', 'Crítica'],
                ['A diretora desenhada como um semáforo a dar ordens.', 'Sátira'],
                ['O treinador fica com o dinheiro das quotas.', 'Acusação de facto'],
                ['Os alunos que vieram de outro país não deviam estar aqui.', 'Ataque pela origem']],
         fe='A confusão mais provável é ler a acusação como crítica: «fica com o dinheiro» diz que uma pessoa concreta fez uma coisa '
            'concreta. Isso prova-se ou não; uma crítica discute-se. Volta aos quatro tipos.',
         pista='Pergunta a cada publicação: discute, exagera, acusa ou visa a origem?'),
 # Decisão 161: o caso real, com fonte oficial aberta (dgsi.pt). Cita-se só o que o acórdão diz: o comentário (sumário I), os dois
 # requisitos (sumário II) e a razão (sumário IV).
 escolha('Um caso real',
         'Caso real: em 2017, a Relação de Évora confirmou a condenação de uma antiga funcionária por este comentário. Ela provou os '
         'ordenados em atraso. Porque não bastou?',
         'Este comentário, escrito no Facebook de uma empresa por uma antiga funcionária, valeu-lhe uma condenação, confirmada em '
         '2017. Segundo o tribunal, o que lhe faltou?',
         'Provar também as dívidas a fornecedores, de que acusou o gerente.',
         [('Uma licença da empresa para poder comentar na sua página.',
           'A página estava aberta: o tribunal fala da «liberdade de interacção» que ela concedia. O problema foi o que ela escreveu. '
           'Volta ao comentário: de que mais acusa o gerente?'),
          ('Ficar calada: dizer em público que alguém deve dinheiro é crime.',
           'O tribunal diz que não há crime se a acusação servir «interesses legítimos» e se o agente «prove a verdade da imputação». '
           'Ela provou os ordenados; o resto, não. Volta ao comentário.')],
         'O tribunal escreveu que ela imputou ao gerente «outros comportamentos genéricos, que não concretiza nem demonstra, como sejam '
         'as dívidas a fornecedores». Provar um facto não prova os outros. E «Não tem vergonha» é um juízo de valor, que não se prova.',
         4, 'transferir', 'acusação de facto e prova',
         cita=COMENTARIO, fonte='tre-2017-i',
         citacoes=[('tre-2017-iv', 'outros comportamentos genéricos, que não concretiza nem demonstra, como sejam as dívidas a fornecedores'),
                   ('tre-2017-i', 'Não tem vergonha'), ('tre-2017-i', 'liberdade de interacção'),
                   ('tre-2017-ii', 'interesses legítimos'), ('tre-2017-ii', 'prove a verdade da imputação')],
         liga=[{'t': 'Ler o acórdão da Relação de Évora, 21/03/2017 (dgsi.pt)', 'href': DGSI}],
         pista='Repara em tudo aquilo de que o comentário acusa o gerente.'),
 # ---------------------------------------------------------------- parte 2, pesar e escrever (50 minutos)
 M.volta('O Diogo pede que apaguem',
         'Na segunda aula, o Diogo pede à conta que apague o comentário. A conta responde: «Aqui cada um escreve o que quer. Apagar é '
         'censura.» O comentário já tem 40 partilhas.',
         [('Constituição, artigo 26.º, n.º 1', 'A todos são reconhecidos os direitos […] ao bom nome e reputação […]', 'crp-26-1', None)],
         f'Constituição da República Portuguesa, <a href="{DRE}">Diário da República</a>.', carimbo='Caso inventado.'),
 M.fazer('ordenar', 'Antes de repetir',
         'Antes de repetires o comentário sobre o Diogo, põe por ordem o que fazes.',
         'Chega-te uma acusação contra um colega. Que ordem segues antes de a passar a outros?',
         'Primeiro a origem, depois como se sabe, depois uma fonte que não dependa da primeira. Só então se decide. Quarenta partilhas '
         'do mesmo comentário contam como uma fonte só.',
         3, 'aplicar', 'verificar antes de repetir',
         passos=['Procurar quem escreveu primeiro o comentário.',
                 'Perguntar como é que essa pessoa sabe.',
                 'Procurar quem tenha visto, sem ser pelo comentário.',
                 'Decidir: repetir, corrigir ou não dizer nada.'],
         fe='A confusão mais provável é procurar outra fonte antes de saber qual é a primeira: sem a origem, não sabes se a segunda a '
            'copiou. Começa por quem escreveu primeiro.',
         pista='Começa pela origem do comentário.'),
 M.em_turma(DECIDE_Q, [
     ('O lado da conta', f'A Constituição protege o direito de {M.citado("crp-37-1", "exprimir e divulgar livremente o seu pensamento")}. '
                                    'Para a conta, apagar é censurar.'),
     ('O lado do Diogo', f'A todos se reconhece o direito {M.citado("crp-26-1", "ao bom nome e reputação")}. E ele diz que é mentira.'),
     ('Uma objeção', 'A censura corta antes de publicar. Apagar depois, a pedido do acusado, é o mesmo?')],
     {'O que se faz': 'Decides outra vez e escolhes a razão que pesou.',
      'Quanto tempo': 'Três minutos; em turma, até treze.',
      'O que fica escrito': 'Nada em papel; a escolha fica nos artefactos.',
      'Se estás sozinho': 'Compara com a escolha do início e abre os três lados.'},
     prova=('Que razão pesou mais?', ('O bom nome (26.º)', 'A liberdade de expressão (37.º)', 'Nada de censura (37.º, n.º 2)')),
     prova_rot='A razão que pesou', intro='', nota=None),
 # Conceito espaçado (origem): facto, regra ou razão, a distinção da sessão 01 («Facto, regra ou razão», cartão 19).
 M.fazer('emparelhar', 'Facto, regra ou razão',
         'Liga cada frase ao que ela é numa justificação.',
         'Facto, regra ou razão de uma das partes: o que é cada frase?',
         'As partilhas são um facto do caso; o n.º 2 é uma regra escrita na Constituição, que vale para todos; «apagar é censura» é a '
         'razão de quem gere a conta, que ainda tem de ser pesada.',
         3, 'distinguir', 'relato e princípio',
         pares=[['O comentário sobre o Diogo já tem 40 partilhas.', 'Um facto do caso'],
                ['«O exercício destes direitos não pode ser impedido ou limitado por qualquer tipo ou forma de censura.»',
                 'Uma regra que vale para todos'],
                ['«Apagar é censura.»', 'A razão de uma das partes']],
         citacoes=[('crp-37-2', 'O exercício destes direitos não pode ser impedido ou limitado por qualquer tipo ou forma de censura.')],
         origem='cidadania/m1/sessoes/01/',
         fe='A confusão mais provável é tomar a razão da conta por regra: usa a palavra «censura», mas é a leitura de uma das partes. '
            'É a distinção da sessão 01: um facto, uma regra escrita que vale para todos, a razão de alguém. Volta ao artigo.',
         pista='Uma regra vale para todos; uma razão é de alguém.'),
 # Cadeia com o passo em falta (plano, secção 2: nas sessões 04 a 07, o aluno encontra o passo que falta).
 escolha('O passo que falta',
         'Facto: acusam o Diogo, pelo nome, de roubar. Fonte: a Constituição protege o bom nome. Limite: ninguém disse que viu. '
         'Que aplicação falta?',
         'Nesta justificação há facto, fonte e limite, mas falta a aplicação: a frase que liga o facto à fonte. Qual é?',
         'Acusá-lo de roubar, sem prova, atinge o seu bom nome.',
         [('Quem partilhou o comentário também é culpado de roubo.',
           'Isto não liga o facto à fonte: confunde quem repete uma acusação com quem rouba. A aplicação diz o que a acusação faz ao '
           'direito do Diogo. Volta ao bom nome.'),
          ('Numa conta de memes é humor, e o bom nome fica de fora.',
           'É a razão de quem gere a conta, não uma aplicação: o comentário não exagera um traço, diz que um colega roubou. Volta aos '
           'quatro tipos: sátira não é acusação de facto.')],
         'A aplicação liga o facto (a acusação com o nome dele) à fonte (o direito ao bom nome): uma acusação sem prova atinge esse '
         'direito. O limite diz o que falta saber.',
         4, 'aplicar', 'facto, fonte, aplicação, limite',
         pista='A aplicação junta o facto e a fonte.'),
 # Charneira 2: o erro esperado é tomar «sem prova» por «falso», ou a acusação por humor.
 escolha('O que as provas permitem',
         'Que conclusão diz o que as provas permitem, sem ir além delas?',
         'Qual das conclusões fica dentro do que o caso e os artigos mostram?',
         'O comentário acusa sem prova; a pera critica quem manda.',
         [('O comentário é falso, por isso a conta tem de fechar.',
           'Ninguém provou que é falso: só se sabe que não tem prova. E fechar a conta cala também a pera. Esta conclusão vai além do '
           'que se sabe.'),
          ('O comentário pode ficar: numa conta de memes, é humor.',
           'A pera exagera um traço de quem manda; o comentário diz que um colega concreto roubou. Uma acusação não passa a humor por '
           'estar numa conta de memes. Volta aos quatro tipos.')],
         'Diz o que se sabe (a acusação não tem prova; a pera exagera o diretor) e deixa aberto o que ninguém sabe: se o Diogo roubou.',
         3, 'aplicar', 'conclusão e provas', pista='Procura a conclusão que não acrescenta nada às provas.'),
 M.papel(PERGUNTA,
         ['A tua conclusão, por agora.',
          'Uma prova: um facto do caso e uma expressão exata, entre aspas, com o artigo.',
          'Uma dúvida que ainda tens.'],
         ['A conclusão responde à pergunta sem ir além das provas.',
          'A prova junta um facto a uma expressão exata, com o artigo.',
          'A dúvida, respondida, podia mudar a conclusão.'],
         '<p>Outro caso, inventado: numa página da escola, alguém diz que a funcionária da reprografia perde trabalhos de '
         'propósito.</p><ol>'
         '<li>Conclusão: é uma acusação de facto sem prova.</li>'
         f'<li>Prova: atribui-lhe um facto; a Constituição reconhece a todos o direito {M.citado("crp-26-1", "ao bom nome e reputação")} '
         '(artigo 26.º, n.º 1).</li>'
         '<li>Dúvida: perdeu-se mesmo algum trabalho?</li></ol>',
         'Num papel pequeno, sozinho e sem telemóvel.',
         relogio_min=12),
 M.levar(FRASE, ['Uma opinião discute-se; uma acusação de facto prova-se.',
                 'Muitas partilhas do mesmo comentário contam como uma fonte só.']),
]

# o lugar da certa em cada escolha (0, 1 ou 2), com a semente do motor: nunca o mesmo em mais de metade, nem três seguidos
LUGARES = (1, 2, 0, 2, 0, 1)

# O passo do projeto (plano, secção 3: «duas fontes independentes da tua pergunta, com leitura lateral (#84); as três afirmações
# reais vêm prontas na página, confirmadas e datadas»). As três afirmações conferem-se em páginas oficiais do Diário da República,
# abertas a 6/11/2026: o artigo 37.º, n.º 2, da Constituição (verdadeira) e a Resolução da Assembleia da República n.º 20/90
# (a Convenção foi «assinada em Nova Iorque a 26 de Janeiro de 1990»: a segunda é falsa; «Aprovada em 8 de Junho de 1990.»: a
# terceira é verdadeira). As respostas ficam no guia (GUIA['04']).
DEPOIS = ('<article class="c"><p class="rot">O passo do teu projeto</p><p class="tit">Duas fontes que não se copiam</p>'
          '<p class="sub">Antes de pores uma fala no teu teatro-documento, verificas de onde ela vem. Primeiro, treina com três afirmações '
          'reais, confirmadas a 6 de novembro de 2026: «A Constituição portuguesa proíbe a censura.»; «Portugal assinou a Convenção '
          'sobre os Direitos da Criança em Lisboa.»; «A Assembleia da República aprovou essa Convenção em 1990.» Para cada uma, escreve em papel: quem o diz, duas fontes que não se copiam (abre outros separadores antes de ler '
          'uma página até ao fim) e o teu veredicto: verdadeira, falsa ou sem prova. Depois, faz o mesmo para a tua pergunta: duas '
          'fontes independentes, com o que é preciso para as reencontrar. O que conta: as duas fontes chegaram à informação cada uma '
          'pelo seu lado; uma página que copia outra conta como uma só; o que um assistente de inteligência artificial responde é mais '
          'uma afirmação a verificar, não uma fonte.</p>'
          '<p class="ir"><a href="../../../projeto/#metodo">As fontes, no enunciado da Pergunta Humana</a></p></article>')


def sessao():
    d = {
        'id': 'cidadania-m1-s04', 'chave': 'epi-cid-m1-s04', 'versao': '2026-11-06-molde', 'marca': 'CD', 'molde': L.MOLDE,
        'titulo': 'Sessão 04: Posso dizer tudo?', 'h1': 'Cidadania, módulo 1, sessão 04: Posso dizer tudo?',
        'modulo': {'n': 1, 'nome': 'Humanos', 'url': L.LENTE + 'cidadania/piloto/m1/'},
        'saida': 'cidadania/m1/sessoes/04/index.html',
        'seguinte': '../../../piloto/m1-s05/', 'seguinteRotulo': 'Sessão 05: Quem guarda os meus dados?',
        'fontes': M.ref('Constituição da República Portuguesa, artigos 26.º, n.º 1, e 37.º, n.os 1 a 3, na versão consolidada do Diário da '
                        'República. Convenção sobre os Direitos da Criança, artigo 13.º, na tradução portuguesa anexa à Resolução da '
                        'Assembleia da República n.º 20/90, no Diário da República. Acórdão do Tribunal da Relação de Évora de 21 de março '
                        'de 2017, processo 373/14.8T9STR.E1, em dgsi.pt. Imagem: _Les Poires_, _Le Charivari_, 17 de janeiro de 1834, '
                        'desenho talvez de Honoré Daumier a partir de Charles Philipon, Gallica (Biblioteca Nacional de França), domínio '
                        'público, segundo o registo do Wikimedia Commons. Gravura: Jan Saenredam, segundo Cornelis van Haarlem, _Antrum '
                        'Platonicum_, 1604, British Museum, domínio público. Platão, _República_, livro VII (a alegoria da caverna). O caso '
                        'da conta de memes, o da caricatura da Inês, o do vídeo da cantina, as quatro publicações de outra escola e o da '
                        'reprografia são inventados; o da Relação de Évora é real.'),
        'tempos': {'folga': 10, 'pausa': 10, 'projeto': 45, 'entrega': 5},
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
