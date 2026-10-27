"""Molde das sessões (27/10/2026, decisões do docente): Recupera, Vê, Decide, Faz, Leva.

Recupera: duas ou três perguntas de memória sobre a sessão anterior; quando há uma
resposta conceptual, ela vem da própria sessão anterior e abre-se em «Confirmar».
Vê: um material de cada vez (imagem ou excerto), com a instrução ao lado.
Decide: primeiro em silêncio, cada pessoa; depois em grupo; sem ecrã.
Faz: produção em papel ou no ficheiro do grupo; a revisão com outra pessoa fecha-a.
Leva: uma pergunta de saída, em papel.
A sessão 03 realiza a tarefa já partilhada e segue o plano de 180 minutos.

Cartão de obra: obra e acesso legal, razão da escolha, contexto (até 100 palavras),
pergunta aberta, duas ligações e uma leitura discordante. Factos e ligações vêm das
páginas e fontes já publicadas no Lente; obras protegidas ficam descritas, não citadas.
"""

PASSOS = ['Recupera', 'Vê', 'Decide', 'Faz', 'Leva']
PASSOS_TAREFA = ['Recupera', 'Vê', 'Investiga', 'Prepara', 'Apresenta']

# O que se faz em cada passo, numa linha (a mesma em todas as sessões).
LINHA = {
 'Recupera': 'De memória, sem abrir o caderno.',
 'Vê': 'Observa primeiro. Lê depois.',
 'Decide': 'Primeiro em silêncio, cada pessoa. Depois em grupo.',
 'Faz': 'Em papel ou no ficheiro do grupo.',
 'Leva': 'Em papel, antes de sair.',
 'Investiga': 'Em grupo. O ecrã serve para procurar e verificar fontes.',
 'Prepara': 'Em papel ou no ficheiro do grupo.',
 'Apresenta': 'Até oito minutos por grupo, seguidos de defesa.',
}
# Na sessão 03, os dois primeiros passos servem a tarefa já partilhada.
LINHA_TAREFA = {'Recupera': 'O grupo reúne a pergunta e os materiais.', 'Vê': 'Confirmem o enunciado antes de investigar.'}
# Marca visível no cabeçalho do passo.
MARCA = {'Recupera': 'De memória', 'Decide': 'Sem ecrã', 'Faz': 'Em papel', 'Leva': 'Em papel', 'Prepara': 'Em papel'}

MOLDE = {
1: dict(
 recupera=[('Lembra-te de uma imagem que, à primeira vista, te fez pensar uma coisa que depois não se confirmou. O que viste primeiro?', None),
           ('O que te fez mudar de ideia: uma informação nova, outra pessoa ou outro ângulo?', None)],
 ve='entry', material='image',
 leva='Numa frase: que diferença há entre ver e compreender?'),
2: dict(
 recupera=[('Que diferença há entre descrever e interpretar?', 'Descrever é indicar o que está visível. Interpretar é propor um sentido a partir de pistas.'),
           ('Uma legenda transforma uma hipótese em facto?', 'Não. A legenda orienta a leitura; a hipótese continua a precisar de pistas e de verificação.')],
 ve='entry', material='image',
 leva='Numa frase: uma boa intenção chega para justificar uma ação sobre outra pessoa?'),
3: dict(
 recupera=[('Que diferença há entre uma observação e uma hipótese?', 'A observação indica o que está visível ou documentado. A hipótese propõe uma explicação que ainda precisa de ser verificada.'),
           ('O que precisa uma pessoa de saber para poder aceitar ou recusar o que lhe propõem?', 'Precisa de conhecer a situação e de poder dizer que não. Sem informação nem possibilidade de recusa, não há consentimento.')],
 tarefa=True),
4: dict(
 recupera=[('Que fonte sustentou melhor a resposta do teu grupo? Porquê essa?', None),
           ('Que pergunta ou observação recebeste na defesa?', None),
           ('Duas páginas que repetem a mesma origem contam como duas confirmações?', 'Não. Se partem da mesma origem, valem como uma só confirmação.')],
 ve='Lê a cena. Repara no que cada pessoa faz antes de reparar no que diz.', material='document', faz_inicio=True,
 leva='Numa frase: o que torna uma personagem reconhecível sem a reduzir a um rótulo?'),
5: dict(
 recupera=[('O que quer cada voz numa cena?', 'Cada voz tenta conseguir algo. O conflito surge quando esse objetivo encontra resistência.'),
           ('A voz de uma personagem é a posição do autor?', 'Não automaticamente. O autor pode dar voz a posições que não defende.'),
           ('Que indicação usaste na tua microcena: ação, pausa ou som? Que efeito teve?', None)],
 ve='Lê a cena de Lia. O que sabe ela, e o que lhe esconderam?', material='document', faz_inicio=True,
 leva='Numa frase: o que muda numa história quando a personagem pode escolher?'),
6: dict(
 recupera=[('Que diferença há entre objetivo, ação e obstáculo?', 'O objetivo é o que a personagem procura; a ação é o que faz; o obstáculo dificulta essa tentativa.'),
           ('Uma consequência é um castigo acrescentado no fim?', 'Não. Deve nascer da ação e das condições construídas na história.'),
           ('Que formato escolheste para o argumento, e porquê?', None)],
 ve='Lê os dois casos. Ainda não decidas.', material='document', silencio='entry',
 leva='Numa frase: há limites que uma boa consequência não apaga? Dá um exemplo.'),
7: dict(
 recupera=[('Nos dois casos do elétrico, o que muda se o número de pessoas é semelhante?', 'Muda a ação proposta: desviar o elétrico não é o mesmo que empurrar uma pessoa.'),
           ('A maioria dos votos decide qual razão é mais forte?', 'Não. A quantidade de votos não resolve a força de uma objeção.'),
           ('Que objeção te fez pensar mais na sessão anterior?', None)],
 ve='Lê o caso. Quem ganha e quem perde com cada decisão?', material='document', silencio='entry',
 leva='Numa frase: aceitarias a tua regra se recebesses menos? Porquê?'),
8: dict(
 recupera=[('Que critérios diferentes podem orientar uma distribuição?', 'Igualdade, necessidade e ordem de chegada, entre outros. Cada critério tem efeitos diferentes.'),
           ('Aplicar a mesma regra a situações diferentes garante justiça?', 'Não, por si só. A regra tem de poder ser explicada a quem recebe menos.'),
           ('O que mudou do teu argumento v1 para o v2?', None)],
 ve='Lê a situação. Conta os votos; depois procura as razões.', material='document', faz_inicio=True,
 leva='Numa frase: o que distingue votar de deliberar?'),
9: dict(
 recupera=[('O que distingue votar de deliberar?', 'Votar conta posições; deliberar confronta razões.'),
           ('Uma pausa significa sempre medo ou submissão?', 'Não. O sentido de uma pausa depende das falas e das ações à sua volta.'),
           ('Que passagem do teu guião assinalaste para rever?', None)],
 ve='Compara as três versões da mesma ação.', material='document', faz_inicio=True,
 silencio='Escolhe a versão que torna a ação mais clara. Guarda uma razão, sem a dizer ainda.',
 leva='Numa frase: que escolha do teu guião só funciona no meio que escolheste?'),
10: dict(
 recupera=[('O que precisa um texto de áudio para que a ação se compreenda sem imagem?', 'Vozes identificadas, sons com contexto e transições claras.'),
           ('Discordar de uma personagem é o mesmo que não compreender a cena?', 'Não. Discordar pode ser um efeito desejado; não compreender quem fez uma ação decisiva exige revisão.'),
           ('Que duas alterações registaste na última revisão?', None)],
 ve='entry', material='document', fecho_leva=True,
 leva='Numa frase: o que mudou entre a tua primeira ideia e o texto que apresentaste?'),
}

# Cartões de obra. «acesso»: (texto, endereço ou None para uma edição em papel).
# «ligacoes»: (texto, caminho no Lente). Datas e factos: os das páginas já publicadas.
OBRAS = {
1: dict(titulo='A alegoria da caverna', autor='Platão', data='A República, livro VII',
 razao='Uma das imagens mais antigas sobre o que acontece quando tomamos uma parte pelo todo.',
 contexto='Platão foi um filósofo da Grécia antiga. Na República, imagina pessoas presas numa caverna desde a infância. Só podem olhar em frente: veem sombras numa parede e tomam-nas pela realidade. Atrás delas há objetos e uma fonte de luz que desconhecem. Sair obriga a rever aquilo em que se acreditava. É uma alegoria, uma história que ajuda a pensar um problema, não um relato histórico.',
 acesso=[('Tradução portuguesa de Maria Helena da Rocha Pereira, Fundação Calouste Gulbenkian', None),
         ('A gravura de Jan Saenredam, 1604, no Wikimedia Commons', 'https://commons.wikimedia.org/wiki/File:Platon_Cave_Sanraedam_1604.jpg')],
 pergunta='Que sombras de hoje tomamos por realidade, e quem as projeta?',
 ligacoes=[('Abrir a caverna', 'cidadania/m1/passo-02/'), ('Como se investiga: olhar e registar', 'investigar/passo-02/')],
 discordante='Karl Popper, em A Sociedade Aberta e os Seus Inimigos (1945), criticou a República por entregar o governo a quem afirma conhecer a verdade. Quem saiu da caverna ganha o direito de decidir pelos outros?'),
2: dict(titulo='The Egg', autor='Andy Weir', data='conto, em inglês', protegida=True,
 razao='Põe à prova uma ideia simples: e se cada pessoa com quem te cruzas fosses tu?',
 contexto='The Egg é um conto curto de Andy Weir. Uma personagem morre e descobre uma possibilidade imaginária: todas as vidas humanas estariam ligadas à sua própria existência. Quem ajudou ou magoou seria, afinal, ela mesma. O conto transforma o modo como olhamos para quem é diferente ou desconhecido. É ficção para pensar, não uma tese sobre a realidade.',
 acesso=[('O conto no sítio do autor, em inglês', 'https://galactanet.com/oneoff/theegg_mod.html')],
 pergunta='Precisamos de nos imaginar no lugar do outro para o respeitar?',
 ligacoes=[('O lugar do outro', 'cidadania/m1/passo-03/'), ('Ética: a criança e a distância', 'olhar-e-decidir/etica/licao-1/')],
 discordante='Uma leitura discordante: se todas as pessoas são a mesma, a diferença do outro desaparece. O respeito não deveria valer precisamente para quem não é como nós?'),
4: dict(titulo='Antígona', autor='Sófocles', data='tragédia grega, século V a.C.',
 razao='Duas exigências incompatíveis e um coro que não deixa ninguém falar sozinho.',
 contexto='No teatro da Atenas antiga, as representações integravam festivais e a vida da cidade. Em Antígona, Creonte proíbe que se sepulte Polinices. Antígona, irmã de Polinices, desobedece. Personagens e coro fazem ouvir posições que não se reduzem a uma única voz. A peça permite examinar exigências incompatíveis; não oferece uma equivalência simples com a democracia atual.',
 acesso=[('Texto grego e tradução inglesa, Center for Hellenic Studies', 'https://www-current.chs.harvard.edu/primary-source/sophocles-antigone/')],
 pergunta='Quando a lei da cidade e a consciência se opõem, quem decide qual vale mais?',
 ligacoes=[('A ordem chegou: Pinter e os limites ao poder', 'cidadania/m1/passo-07/'), ('Justiça: até onde vai a minha liberdade?', 'olhar-e-decidir/justica/licao-3/')],
 discordante='Hegel leu a peça como o choque de duas exigências legítimas, a da família e a da cidade, ambas parciais. Antígona resiste a um tirano, ou também só vê uma parte?'),
5: dict(titulo='Farsa de Inês Pereira', autor='Gil Vicente', data='1523',
 citacao='Mais quero asno que me leve que cavalo que me derrube', citacao_nota='o mote da farsa',
 razao='Uma escolha, as suas promessas e as suas consequências, em cena há cinco séculos.',
 contexto='Gil Vicente escreveu para o teatro português do século XVI. Na Farsa de Inês Pereira, Inês quer uma vida diferente e escolhe primeiro um escudeiro que promete muito. As consequências dessa escolha põem em causa aparências e promessas. A sátira constrói uma crítica por falas, atos e contrastes; não é uma descrição factual de todas as pessoas de um grupo.',
 acesso=[('O texto integral no Wikisource', 'https://pt.wikisource.org/wiki/Farsa_de_In%C3%AAs_Pereira'),
         ('Teatro Nacional São João: obra de partida e reescrita contemporânea', 'https://www.tnsj.pt/pt/espetaculos/6786/a-farsa-de-ines-pereira')],
 pergunta='Escolher bem é escolher o que se deseja ou o que se conhece?',
 ligacoes=[('Corta! O desfecho de Inês Pereira', 'narrativas/corta/ines/'), ('Uma vida em direto', 'cidadania/m1/passo-01/')],
 discordante='Uma leitura discordante: o mote parece aconselhar a contentar-se com pouco. A farsa defende a liberdade de Inês, ou ensina-a a desistir do que desejava?'),
6: dict(titulo='Justice: o caso do elétrico', autor='Michael Sandel, Universidade de Harvard', data='episódio 1 do curso', protegida=True,
 razao='Uma aula que pede uma decisão antes de oferecer uma teoria.',
 contexto='Michael Sandel abre o curso Justice com um elétrico sem travões: cinco trabalhadores na via em frente, um no desvio. Depois muda o caso: e se, para parar o elétrico, tivesses de empurrar uma pessoa de uma ponte? Os estudantes decidem, explicam-se e contestam-se. Sandel usa os casos para tornar examináveis os critérios de decisão, não para dar uma resposta única.',
 acesso=[('O episódio no canal da Harvard University, em inglês', 'https://www.youtube.com/watch?v=kBdfcR-8hEY'),
         ('O curso oficial', 'https://sandel.scholars.harvard.edu/justice')],
 pergunta='O que torna uma ação aceitável: o resultado, a intenção ou o modo de agir?',
 ligacoes=[('Justiça, lição 1: O elétrico', 'olhar-e-decidir/justica/licao-1/'), ('Justiça, lição 2: Pôr um preço à vida', 'olhar-e-decidir/justica/licao-2/')],
 discordante='Há quem critique estes casos por serem artificiais: na vida real quase nunca se sabe o resultado com certeza. Um dilema inventado ajuda a pensar, ou simplifica demasiado?'),
7: dict(titulo='Escolher sem saber o teu lugar', autor='John Rawls, discutido por Michael Sandel', data='Uma Teoria da Justiça, 1971', protegida=True,
 razao='Uma experiência mental para escolher regras sem saber se vais ganhar ou perder com elas.',
 contexto='Em Justice, Sandel discute a proposta de John Rawls: pensar princípios de justiça sem conhecer as vantagens que teríamos na sociedade. Quem não sabe se ficará entre os que recebem mais ou entre os que recebem menos tem razões para escolher regras que possa explicar a todos. Esta experiência não reproduz toda a teoria; convida a afastar o interesse próprio ao escolher uma regra.',
 acesso=[('Curso oficial Justice, explorações 14 a 16, sobre Rawls, em inglês', 'https://sandel.scholars.harvard.edu/justice')],
 pergunta='Uma regra justa é aquela que escolherias sem saber o teu lugar?',
 ligacoes=[('Justiça: quem fica com o quê?', 'olhar-e-decidir/justica/aplicar/'), ('Quem conta no nosso cuidado?', 'cidadania/m1/cid-m1-butler-singer/')],
 discordante='Robert Nozick respondeu em Anarquia, Estado e Utopia (1974): uma distribuição é justa se resultar de trocas livres e de aquisições legítimas, não de um padrão escolhido à partida. Conta mais o caminho até à distribuição ou o resultado?'),
8: dict(titulo='Doze Homens em Fúria', autor='Sidney Lumet', data='filme, 1957', protegida=True,
 razao='Uma sala fechada onde uma única dúvida obriga onze pessoas a justificar o voto.',
 contexto='Doze jurados, fechados numa sala, têm de decidir por unanimidade se um jovem acusado de homicídio é culpado. Na primeira votação, só um vota «não culpado» e pede para discutir as provas. O filme passa-se quase todo nesse espaço: falas, silêncios e deslocações mostram como as posições mudam. Um tom convincente não garante que a informação seja verdadeira.',
 acesso=[('Registo do filme na Library of Congress', 'https://www.loc.gov/item/96513458/')],
 pergunta='Quando quase todos concordam, o que justifica continuar a discutir?',
 ligacoes=[('Uma decisão entre muitos', 'cidadania/m1/passo-09/'), ('A ordem chegou', 'cidadania/m1/passo-07/')],
 discordante='Uma leitura discordante: no filme, quem duvida acaba por ter razão. Numa deliberação real, a insistência de uma pessoa também pode arrastar o grupo para um erro. O que distingue persuadir de pressionar?'),
9: dict(titulo='Crave', autor='Sarah Kane', data='teatro, 1998', protegida=True,
 razao='Quatro vozes sem enredo explicado: o sentido nasce da relação entre as falas.',
 contexto='Crave, de Sarah Kane, foi apresentada em 1998. Organiza quatro vozes, identificadas apenas por letras, numa construção fragmentada: as falas cruzam-se sem uma história contada do princípio ao fim. Essa opção permite discutir relações entre falas sem pressupor que cada voz contém uma biografia completa. É uma obra protegida: aqui fica descrita, não citada.',
 acesso=[('Royal Court Theatre: arquivo da peça', 'https://livingarchive.royalcourttheatre.com/plays/crave/'),
         ('Paines Plough: a produção', 'https://painesplough.com/productions/crave/')],
 pergunta='Quando o texto não explica tudo, o que acrescenta quem lê, e o que inventa?',
 ligacoes=[('Escutar sem inventar', 'cidadania/m1/passo-08/'), ('Ética: como é ser um morcego?', 'olhar-e-decidir/etica/licao-2/')],
 discordante='Há quem veja na fragmentação um risco: se o espectador não consegue reconstruir a situação, a forma afasta em vez de aproximar. Quando é que deixar coisas por explicar serve a cena?'),
}
