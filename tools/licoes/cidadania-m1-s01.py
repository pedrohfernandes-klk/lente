# Fonte da sessão 01 do M1 de Cidadania, «Uma fotografia no grupo», na versão final do molde cidadania-2026-11 (plano do
# molde, pedido 2, 05/11/2026; decisões 144 a 146, 152 a 155, 157, 158 e 161). Corre-se para escrever o .json ao lado; o
# .json é que o gerador (tools/licoes_lente.py) lê, e nunca se edita à mão. Os cartões montam-se com o ajudante comum
# tools/cidadania_molde.py; cada excerto de lei, declaração ou acórdão vem do registo tools/cidadania_fontes.json (texto
# exato da fonte oficial, confirmado) e o ajudante recusa escrever um excerto que lá não esteja.
#
# 23 cartões (9 de ler, 14 de fazer), pela ordem e com os tempos da secção 2 do plano; a ordem é fixa (cfg.aula) e a resposta
# certa de cada escolha fica no lugar pedido em LUGARES, calculado com a semente do motor (nunca o mesmo lugar em mais de
# metade das escolhas nem três vezes seguidas). O que só o docente faz vive no guia (tools/cidadania_piloto.py), nunca aqui.
#
# 06/11/2026: correções da revisão (factos e fontes, aprendizagem e direção de arte, pt-PT). Cada exercício traz a sua pista
# («pista»), que o validador confere (nunca dá a resposta); as pistas escolhidas por palavras («pistas» da sessão) saíram.
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

IMG = '../../../../img/cidadania/eleanor-roosevelt-dudh-1949.webp'
ALT = ('Eleanor Roosevelt, de vestido escuro e colar de pérolas, segura com as duas mãos um grande cartaz encurvado e olha para ele. '
       'No cartaz, o emblema das Nações Unidas, o título «The Universal Declaration of Human Rights» e muitas colunas de texto miúdo.')
ALT_VER = 'A mesma fotografia: Eleanor Roosevelt segura o cartaz da Declaração Universal e olha para ele.'
VER = f'<img src="{IMG}" alt="{ALT_VER}">'
UNRIC = 'https://unric.org/pt/declaracao-universal-dos-direitos-humanos/'
DRE = 'https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-aprovacao-constituicao/1976-34520775'
DGSI = 'https://www.dgsi.pt/jtre.nsf/134973db04f39bf2802579bf005f080b/7c52769f1dfab8be80257e830052d374?OpenDocument'
CREDITO = ('Eleanor Roosevelt com a Declaração Universal dos Direitos Humanos, 1949. '
           'Fotógrafo não identificado. Franklin D. Roosevelt Presidential Library &amp; Museum, 64-165. '
           '<a href="https://www.flickr.com/photos/fdrlibrary/27758131387/">Registo de origem</a>. '
           '<a rel="license" href="https://creativecommons.org/licenses/by/2.0/deed.pt">CC BY 2.0</a>.')
PERGUNTA = 'Que direitos estão em causa quando uma fotografia chega ao grupo da turma?'
DECIDE_Q = 'A fotografia pode ficar no grupo da turma?'
FRASE = 'Quando dois direitos chocam, pesam-se no caso.'


def escolha(rot, p, p2, certa, erradas, f, minutos, tipo, conceito, **extra):
    """Uma escolha de três opções; a certa vai para o lugar de LUGARES (preenchido em sessao())."""
    c = M.fazer('escolha', rot, p, p2, f, minutos, tipo, conceito, **extra)
    c['_certa'], c['_erradas'] = M.ref(certa), [(M.ref(o), M.ref(e)) for o, e in erradas]
    return c


CARTOES = [
 # ---------------------------------------------------------------- parte 1, ver antes de concluir (60 minutos)
 M.abre('Uma fotografia no grupo',
        f'ver e ler (60{NB}min), pausa (10{NB}min), pesar e escrever (50{NB}min) e o teu projeto (45{NB}min).',
        'Às 8h20, no autocarro para a escola, a Sara adormece encostada à janela. Um colega fotografa-a e envia a fotografia para '
        'o grupo da turma, onde estão 28 pessoas. Antes da primeira aula, a fotografia já tem doze reações a rir. Ninguém perguntou '
        'nada à Sara.',
        PERGUNTA),
 M.decide(DECIDE_Q, [
     ('Quem acha que pode ficar', 'A Sara estava no autocarro, à vista de quem lá ia. A fotografia só a mostra a dormir.'),
     ('Quem acha que não pode', 'No autocarro, viram-na uns minutos. No grupo da turma, 28 pessoas podem guardar a fotografia e reenviá-la.'),
     ('Uma objeção', 'E se a fotografia servisse para mostrar que o autocarro sai cedo de mais? Uma boa finalidade muda alguma coisa?')]),
 # R1: a obra do #84 (Etapa 2, «O que somos»), reescrita para perguntar o que a sala pôs à prova, sem pedir o artigo antes do Lê.
 # Factos: MG+MSUM, Moderna galerija, Ljubljana (a obra está na coleção do museu), registo «Marina Abramović: Rhythm 0, 1974»:
 # «To test the limits of the relationship between performer and audience» (06/11/2026: o retorno diz o que o museu diz).
 M.recupera(escolha(
     'O que a sala pôs à prova',
     'Em _Rhythm 0_ (Nápoles, 1974), a artista Marina Abramović ficou imóvel seis horas, e o público podia usar nela 72 objetos. '
     'O que é que a sala pôs à prova?',
     'Em _Rhythm 0_, o público pôde usar 72 objetos na artista durante seis horas. O que estava, afinal, a ser testado?',
     'O que fazemos a alguém quando nada nos trava.',
     [('Quanto tempo uma pessoa aguenta parada numa sala.',
       'As seis horas eram a duração, não a pergunta. Repara no que o público recebeu: objetos e licença para os usar nela. '
       'O que se viu foi o que as pessoas fizeram com essa licença.'),
      ('Se o público percebe o que é uma obra de arte.',
       'Segundo a Moderna galerija de Ljubljana, que tem a obra, Abramović quis testar os limites da relação entre a artista e o '
       'público, e não o que o público sabe de arte. Relê o que o público podia fazer.')],
     'Parte do público passou da cautela à agressão, e houve quem defendesse a artista: quando alguém lhe apontou uma arma, '
     'outra pessoa tirou-lha. Fica a pergunta da sessão «O que somos»: a dignidade de uma pessoa depende de os outros a '
     'respeitarem?',
     3, 'reconhecer', 'dignidade', pista='Repara no que o público podia fazer com os objetos.')),
 # R2: observação ou interpretação (Etapa 1, «O que vemos», cidadania/aula-1/), item novo sobre a fotografia do autocarro.
 # 06/11/2026: verdadeiro (o 12 é falso), para a turma não aprender o padrão em vez da ideia.
 M.recupera(M.fazer(
     'vf', 'Ver ou supor',
     'Na fotografia do autocarro, «a Sara não se importou» já é uma interpretação.',
     '«A Sara não se importou com a fotografia» é uma interpretação, e não uma observação.',
     'É uma interpretação: observa-se que a Sara dorme encostada à janela; que não se importou, a fotografia não mostra, e a '
     'dormir ela não podia aceitar nem recusar.',
     4, 'distinguir', 'observação e interpretação', v=True,
     fe='«Não se importou» diz o que a Sara sentiu, e isso não se vê. É a distinção da sessão «O que vemos»: «demora a pagar» '
        'observa-se; «está a fazer-me perder tempo» já é interpretação. Volta ao caso e fica pelo que se vê.',
     pista='Pergunta-te: isto vê-se ou alguém o supõe?'),
     origem='cidadania/aula-1/'),
 # 06/11/2026: o cargo de Eleanor Roosevelt confere com as Nações Unidas, «Drafters of the Declaration»
 # (https://www.un.org/en/about-us/udhr/drafters-of-the-declaration, aberta a 6/11/2026: «Chairperson of the Commission on
 # Human Rights»).
 M.olha('Um documento nas mãos', 'Separa o que a fotografia mostra do que só a legenda te diz.',
        M.figura(IMG, ALT, CREDITO, 'Eleanor Roosevelt, que presidiu à Comissão dos Direitos Humanos da ONU, com o cartaz da '
                 'Declaração Universal. Lake Success, Nova Iorque, novembro de 1949.',
                 artefacto='Eleanor Roosevelt com o cartaz da Declaração Universal, 1949')),
 escolha('O que a fotografia mostra',
         'Sem acrescentar nada teu, o que se observa na fotografia?',
         'Que frase fica só pelo que a fotografia deixa ver?',
         'Uma mulher segura um cartaz e olha para ele.',
         [('Uma mulher lê em voz alta o texto do cartaz.',
           'Ler em voz alta é uma suposição: uma fotografia não tem som e não mostra se ela fala. O que vês é o gesto: segura o '
           'cartaz com as duas mãos e olha para ele. Volta à imagem.'),
          ('Uma mulher mostra à câmara um texto que escreveu.',
           'Duas suposições: que o texto é dela e que o mostra a quem fotografa. Ela não olha para a câmara, olha para o cartaz; '
           'e quem escreveu o texto, a fotografia não diz.')],
         'Vês as duas mãos no cartaz e o olhar dirigido a ele. Se lê, se fala ou quem escreveu o texto, já seria acrescentar.',
         3, 'distinguir', 'observar e supor', ver=VER, pista='Fica pelo gesto e pelo olhar.'),
 M.fazer('emparelhar', 'Imagem, legenda ou nenhuma',
         'De onde vem cada informação? Liga cada frase à sua prova.',
         'Para cada frase, onde está a prova: na imagem, na legenda ou em lado nenhum?',
         'O título lê-se no cartaz: «The Universal Declaration of Human Rights», isto é, «A Declaração Universal dos Direitos '
         'Humanos». O lugar e a data vêm da legenda. O efeito em quem lê não se fotografa.',
         3, 'distinguir', 'imagem e legenda',
         pares=[['O título do cartaz está escrito em inglês.', 'Vê-se na fotografia'],
                ['A cena passa-se em Lake Success, em 1949.', 'Só a legenda o diz'],
                ['Quem lê o cartaz passa a respeitar os direitos.', 'Nenhuma das duas o prova']],
         fe='A confusão mais provável é dar à fotografia o que só a legenda diz: Lake Success e 1949 não estão escritos no cartaz. '
            'Volta à imagem e procura, em cada frase, onde está a prova.', ver=VER,
         pista='Procura cada informação no cartaz e depois na legenda.'),
 M.le('Três artigos da Declaração', 'Procura o que protege cada um: a Sara e o colega.',
      [('Artigo 1.º', 'Todos os seres humanos nascem livres e iguais em dignidade e em direitos. […]', 'dudh-1', 'a1'),
       ('Artigo 12.º', 'Ninguém sofrerá intromissões arbitrárias na sua vida privada, na sua família, no seu domicílio ou na sua '
                       'correspondência, nem ataques à sua honra e reputação. […]', 'dudh-12', 'a12'),
       ('Artigo 19.º', 'Todo o indivíduo tem direito à liberdade de opinião e de expressão […]', 'dudh-19', 'a19')],
      f'<a href="{UNRIC}">Transcrição portuguesa do UNRIC</a>, Nações Unidas.',
      mais=(M.lei([('Artigo 12.º', '[…] Contra tais intromissões ou ataques toda a pessoa tem direito a protecção da lei.', 'dudh-12', None)])
            + '<p class="glossa"><b>Intromissão arbitrária</b>: entrar na vida de alguém sem razão nem direito. <b>Reputação</b>: o que '
              'os outros pensam de uma pessoa.</p>')),
 M.fazer('sublinhar', 'O que a piada atinge',
         'As doze reações a rir fazem da Sara uma piada. Toca nas palavras do artigo 12.º que dizem o que essa piada pode atingir.',
         'No artigo 12.º, toca nas palavras que dizem o que fica em risco quando a Sara é posta em ridículo diante da turma.',
         '«Honra e reputação»: o modo como os outros veem e tratam alguém. Uma fotografia feita piada atinge-as, além da vida '
         'privada que já expõe.',
         3, 'reconhecer', 'vida privada, honra e reputação',
         frase='Ninguém sofrerá intromissões arbitrárias na sua vida privada, na sua família, no seu domicílio ou na sua '
               'correspondência, nem ataques à sua honra e reputação.',
         certas=[22, 23, 24], fonte='dudh-12', l='a12',
         fe='A confusão mais provável é ficar pela vida privada, que a fotografia expõe. As reações a rir vão mais longe: mexem '
            'com a forma como a turma vê a Sara. Procura isso no fim da frase.',
         pista='Lê a frase do artigo 12.º até ao fim.'),
 M.fazer('emparelhar', 'Cada situação, o seu artigo',
         'Três situações novas: liga cada uma ao artigo da Declaração que se aplica.',
         'Que artigo da Declaração está em causa em cada uma destas situações?',
         'As mensagens guardadas são correspondência (12.º); tratar alguém como se valesse menos nega a igualdade «em dignidade e '
         'em direitos» (1.º); escrever uma crítica é exprimir uma opinião (19.º).',
         4, 'aplicar', 'artigos 1.º, 12.º e 19.º',
         pares=[['Um colega lê, sem licença, as mensagens que guardas no telemóvel.', 'Artigo 12.º'],
                ['Um aluno é tratado como se valesse menos do que os colegas.', 'Artigo 1.º'],
                ['Um aluno escreve no jornal da escola que a cantina devia mudar.', 'Artigo 19.º']],
         citacoes=[('dudh-1', 'em dignidade e em direitos')],
         fe='A confusão mais provável é ligar as mensagens ao 19.º, por serem palavras. Mas ninguém impede o dono de falar: '
            'alguém entrou no que é dele. Volta ao 12.º e procura «correspondência».',
         pista='Procura nos três artigos a palavra que cada situação toca.'),
 escolha('Dois artigos em choque',
         'No caso da Sara, que dois artigos puxam em sentidos contrários?',
         'Que par de artigos põe a Sara de um lado e o colega do outro?',
         'O 12.º, da vida privada, e o 19.º, da expressão.',
         [('O 1.º, da dignidade, e o 12.º, da vida privada.',
           'Os dois protegem a Sara: puxam para o mesmo lado. Chocar é puxar em sentidos contrários. Procura o artigo que o '
           'colega pode invocar para pôr a fotografia no grupo da turma.'),
          ('O 1.º, da dignidade, e o 19.º, da expressão.',
           'O 19.º é o lado do colega. Do lado da Sara, o artigo que fala do que a fotografia atinge é o 12.º, a vida privada; o '
           '1.º é a base de todos os outros. Volta aos artigos.')],
         'De um lado, a Sara e a vida privada (12.º); do outro, o colega e a liberdade de expressão (19.º).',
         3, 'aplicar', 'choque de direitos', pista='Chocar é puxar em sentidos contrários: um artigo de cada lado.'),
 M.fazer('vf', 'Até onde vai a expressão',
         'Como o artigo 19.º protege a liberdade de expressão, o colega pode deixar a fotografia da Sara no grupo da turma.',
         'Com o artigo 19.º do seu lado, o colega fica com razão para manter a fotografia no grupo da turma.',
         'O 19.º protege o colega, mas o 12.º protege a Sara, e nenhum dos dois apaga o outro. Quando dois direitos puxam em '
         'sentidos contrários, nenhum ganha só por existir: pesam-se no caso.',
         4, 'aplicar', 'choque de direitos', v=False,
         citacoes=[('dudh-12', 'intromissões arbitrárias na sua vida privada')],
         fe='O 19.º não está sozinho: o 12.º diz que ninguém sofrerá «intromissões arbitrárias na sua vida privada». Ter um direito '
            'do teu lado não apaga o direito do outro. Volta aos artigos e lê o 12.º ao lado do 19.º.',
         pista='Põe o 19.º ao lado do 12.º.'),
 M.conceito('Três textos, três forças',
            '<p>A Declaração não é lei; então, não conta?</p>',
            '<table class="tabela"><thead><tr><th scope="col">Texto</th><th scope="col">Tipo</th><th scope="col">Obriga?</th></tr></thead><tbody>'
            '<tr><td data-th="Texto">Declaração Universal, 1948</td><td data-th="Tipo">declaração da ONU</td>'
            '<td data-th="Obriga?">pela Constituição (artigo 16.º, n.º 2)</td></tr>'
            '<tr><td data-th="Texto">Convenção sobre os Direitos da Criança, 1989</td><td data-th="Tipo">tratado</td>'
            '<td data-th="Obriga?">sim, desde 1990</td></tr>'
            '<tr><td data-th="Texto">Constituição</td><td data-th="Tipo">lei fundamental</td>'
            '<td data-th="Obriga?">sim, entidades públicas e privadas (artigo 18.º, n.º 1)</td></tr></tbody></table>',
            'Força jurídica', 'A que obriga um texto e quem fica obrigado.',
            '<p>Não é importância: a Declaração pesa, mas obriga pela Constituição.</p>',
            mais=(f'<p>A Constituição manda ler os direitos {M.citado("crp-16-2", "de harmonia com a Declaração Universal dos Direitos do Homem")} '
                  f'(artigo 16.º, n.º 2) e diz que os direitos, liberdades e garantias {M.citado("crp-18-1", "vinculam as entidades públicas e privadas")} '
                  '(artigo 18.º, n.º 1).</p>')),
 escolha('Que texto obriga a escola',
         'Caso inventado: para descobrir o autor de um vídeo ofensivo, a direção quer ler as mensagens dos alunos. Esta frase '
         'da Constituição (artigo 34.º, n.º 1) obriga a escola. Porquê?',
         'Caso inventado: a direção quer ler as mensagens dos alunos para encontrar o autor de um vídeo. O que faz esta frase da '
         'Constituição obrigar a escola?',
         'A Constituição obriga também uma escola, não só o Estado.',
         [('Repete a Declaração Universal, que é um tratado entre Estados.',
           'A Declaração não é um tratado: em Portugal, conta porque a Constituição manda ler os direitos de harmonia com ela '
           '(artigo 16.º, n.º 2). Aqui, a força vem da própria Constituição. Volta aos três textos.'),
          ('Foi copiada para o regulamento interno daquela escola.',
           'Um regulamento tem de respeitar a Constituição, não o contrário: mesmo sem a repetir, a escola está obrigada. '
           'Volta aos três textos e procura quem a Constituição obriga.')],
         'A Constituição diz que estes direitos «vinculam as entidades públicas e privadas» (artigo 18.º, n.º 1). Procurar o autor '
         'é legítimo; ler as mensagens de todos choca com o sigilo que o artigo 34.º declara inviolável.',
         3, 'transferir', 'força jurídica',
         cita='O domicílio e o sigilo da correspondência e dos outros meios de comunicação privada são invioláveis.',
         fonte='crp-34-1', citacoes=[('crp-18-1', 'vinculam as entidades públicas e privadas')],
         pista='Volta aos três textos: a quem obriga a Constituição?'),
 # Decisão 161: o caso real, com fonte oficial aberta (dgsi.pt). Só se cita o que o acórdão diz: a ordem e, 06/11/2026, a razão que
 # o tribunal escreveu (a pergunta já não se responde por eliminação); o retorno liga-o à dignidade de «O que somos» (Etapa 2), o
 # conceito espaçado da sessão, e diz, como o sumário, que pesou sobretudo a segurança da filha.
 escolha('Um caso real',
         'Caso real: em 2015, o Tribunal da Relação de Évora manteve esta ordem dirigida aos pais de uma rapariga de 12 anos. '
         'Segundo o tribunal, o que a justifica?',
         'Num acórdão de 2015, o Tribunal da Relação de Évora confirmou esta ordem dirigida aos pais. Segundo o que o tribunal '
         'escreveu, qual das razões a justifica?',
         'A filha tem direitos seus, que os pais têm de respeitar.',
         [('Os pais tinham publicado fotografias que ofendiam a filha.',
           'O acórdão não fala de fotografias ofensivas. Para o tribunal, a ordem não precisava desse facto: é uma obrigação dos '
           'pais «tão natural quanto a de garantir o sustento, a saúde e a educação dos filhos». Volta à ordem citada.'),
          ('A filha pediu ao tribunal que a protegesse dos pais.',
           'O acórdão não diz que a filha pediu nada. A proteção vem dos direitos dela, não de um pedido. Volta à ordem: é dirigida '
           'aos pais, que «deverão abster-se».')],
         'O tribunal escreveu que os filhos «São pessoas e consequentemente titulares de direitos». A ordem protege a vida privada '
         'e, sobretudo, a segurança da filha nas redes sociais. É a dignidade da sessão «O que somos».',
         4, 'transferir', 'dignidade',
         cita=('Os pais deverão abster-se de divulgar fotografias ou informações que permitam identificar a filha nas redes sociais. '
               '[…] Na verdade, os filhos não são coisas ou objectos pertencentes aos pais e de que estes podem dispor a seu belo '
               'prazer. São pessoas e consequentemente titulares de direitos.'),
         fonte=['tre-2015-ordem', 'tre-2015-pessoas'], origem='cidadania/aula-2/',
         citacoes=[('tre-2015-natural', 'tão natural quanto a de garantir o sustento, a saúde e a educação dos filhos'),
                   ('tre-2015-pessoas', 'São pessoas e consequentemente titulares de direitos'),
                   ('tre-2015-ordem', 'deverão abster-se')],
         liga=[{'t': 'Ler o acórdão da Relação de Évora, 25/06/2015 (dgsi.pt)', 'href': DGSI}],
         pista='Fica pelo que o tribunal escreveu.'),
 # ---------------------------------------------------------------- parte 2, pesar e escrever (50 minutos)
 M.volta('A Sara pede que apaguem',
         'Na segunda aula, a Sara escreve no grupo da turma: «Apaguem, por favor.» O colega responde: «Foi uma brincadeira. Estavas no '
         'autocarro, toda a gente te via.» A fotografia continua lá.',
         [('Constituição, artigo 26.º, n.º 1', 'A todos são reconhecidos os direitos […] ao bom nome e reputação, à imagem, à palavra, '
                                              'à reserva da intimidade da vida privada e familiar […]', 'crp-26-1', None)],
         f'Constituição da República Portuguesa, <a href="{DRE}">Diário da República</a>.', carimbo='Caso inventado.'),
 M.fazer('emparelhar', 'O que se sabe e o que falta',
         'Separa o que o caso já mostra do que ainda não sabes.',
         'Em cada linha: é um facto do caso ou uma dúvida por resolver?',
         'Sabes onde a Sara estava e o que pediu. Não sabes o que o colega quis, só o que diz, nem até onde a fotografia chegou. '
         'São estas as dúvidas que vão para o papel.',
         3, 'aplicar', 'facto e dúvida',
         pares=[['Onde estava a Sara quando a fotografaram', 'Já se sabe'],
                ['Se o colega quis gozar com ela', 'Ainda não se sabe'],
                ['O que a Sara pediu aos colegas', 'Já se sabe'],
                ['Quem guardou ou reenviou a fotografia', 'Ainda não se sabe']],
         fe='A confusão mais provável é tomar a palavra do colega por prova: «foi uma brincadeira» diz o que ele afirma, não o que '
            'quis. Volta ao caso e separa o que aconteceu do que alguém diz que aconteceu.',
         pista='Separa o que aconteceu do que alguém diz.'),
 M.em_turma(DECIDE_Q, [
     ('O lado do colega', f'O 19.º protege a {M.citado("dudh-19", "liberdade de opinião e de expressão")}. Para ele, foi uma brincadeira.'),
     ('O lado da Sara', f'O 12.º protege contra {M.citado("dudh-12", "intromissões arbitrárias na sua vida privada")}; a Constituição '
                        f'reconhece a todos o direito {M.citado("crp-26-1", "à imagem")}. E ela pediu que apagassem.'),
     ('Uma objeção', f'O 12.º fala de intromissões {M.citado("dudh-12", "arbitrárias")}. Se a Sara tivesse concordado, a partilha '
                     'pesaria o mesmo?')],
     {'O que se faz': 'Decides outra vez e escolhes o direito que pesou.',
      'Quanto tempo': 'Três minutos; em turma, até treze.',
      'O que fica escrito': 'Nada em papel; a escolha fica nos artefactos.',
      'Se estás sozinho': 'Compara com a escolha do início e abre os três lados.'},
     prova=('Que direito pesou mais?', ('Vida privada (12.º)', 'Imagem (26.º)', 'Liberdade de expressão (19.º)')),
     prova_rot='O direito que pesou', intro='', nota=None),
 M.fazer('emparelhar', 'Facto, regra ou razão',
         'Liga cada frase ao que ela é numa justificação.',
         'Facto, regra ou razão de uma das partes: o que é cada frase?',
         'O envio é um facto do caso; o 12.º é uma regra escrita num texto, que vale para todos; «foi uma brincadeira» é a razão '
         'de quem partilhou, que ainda tem de ser pesada.',
         3, 'distinguir', 'relato e princípio',
         pares=[['Um colega enviou a fotografia para o grupo da turma.', 'Um facto do caso'],
                ['«Ninguém sofrerá intromissões arbitrárias na sua vida privada […]»', 'Uma regra que vale para todos'],
                ['«Foi uma brincadeira.»', 'A razão de uma das partes']],
         citacoes=[('dudh-12', 'Ninguém sofrerá intromissões arbitrárias na sua vida privada')],
         fe='A confusão mais provável é tomar a razão de uma parte por regra: «foi uma brincadeira» explica o que alguém fez, mas '
            'não vale para todos. Uma regra está escrita num texto que vale para todos, como a Declaração ou a Constituição. '
            'Volta aos artigos.',
         pista='Uma regra vale para todos; uma razão é de alguém.'),
 M.fazer('ordenar', 'A justificação por ordem',
         'Põe a justificação por ordem: primeiro o facto, depois a fonte, a aplicação e, no fim, o limite.',
         'Ordena: o que aconteceu, o texto que se aplica, a ligação entre os dois e o que ainda falta saber.',
         'Facto, fonte, aplicação, limite: cada passo apoia-se no anterior, e o limite diz até onde a conclusão pode ir.',
         4, 'aplicar', 'facto, fonte, aplicação, limite',
         passos=['A fotografia da Sara foi para o grupo da turma sem lhe perguntarem.',
                 'A Constituição reconhece a todos o direito à imagem.',
                 'Partilhar a imagem dela sem acordo choca com esse direito.',
                 'Falta saber se a fotografia já saiu do grupo da turma.'],
         fe='A confusão mais provável é começar pelo artigo ou pôr o limite antes da aplicação. Começa pelo que aconteceu; depois '
            'o texto; o que falta saber fecha a justificação.',
         pista='Começa pelo que aconteceu.'),
 # Charneira 2 (06/11/2026): a certa já não está escrita no cartão 20; o erro esperado é tomar a palavra do colega, ou uma
 # suposição sobre ele, por prova.
 escolha('O que as provas permitem',
         'Que conclusão diz o que as provas permitem, sem ir além delas?',
         'Qual das conclusões fica dentro do que o caso e os artigos mostram?',
         'A partilha atinge a imagem da Sara; a intenção do colega não se sabe.',
         [('A partilha atinge a imagem da Sara, e o colega quis humilhá-la.',
           '«Foi uma brincadeira» é o que o colega diz; o que quis, nenhum material mostra. Separa o que aconteceu do que alguém '
           'diz que aconteceu.'),
          ('A partilha é aceitável, porque a Sara estava num sítio público.',
           'Estar no autocarro não apaga o direito à imagem: o 26.º começa por «A todos são reconhecidos». E a Sara pediu que '
           'apagassem. Esta conclusão deixa de fora as provas que a contrariam.')],
         'Diz o que as provas mostram (a imagem da Sara foi usada sem acordo) e deixa aberto o que nenhuma mostra: o que o colega '
         'quis.',
         3, 'aplicar', 'conclusão e provas', citacoes=[('crp-26-1', 'A todos são reconhecidos')],
         pista='Procura a conclusão que não acrescenta nada às provas.'),
 M.papel(PERGUNTA,
         ['A tua conclusão, por agora.',
          'Uma prova: um facto do caso e uma expressão exata, entre aspas, com o artigo.',
          'Uma dúvida que ainda tens.'],
         ['A conclusão responde à pergunta sem ir além das provas.',
          'A prova junta um facto a uma expressão exata, com o artigo.',
          'A dúvida, respondida, podia mudar a conclusão.'],
         '<p>Outro caso, inventado: um aluno partilha a voz gravada de um colega.</p><ol>'
         '<li>Conclusão: atinge um direito do colega; não sei se aceitou.</li>'
         f'<li>Prova: foi partilhada sem lhe perguntarem; a Constituição reconhece a todos o direito {M.citado("crp-26-1", "à palavra")} (artigo 26.º, n.º 1).</li>'
         '<li>Dúvida: o colega sabia que estava a ser gravado?</li></ol>',
         'Num papel pequeno, sozinho e sem telemóvel.',
         relogio_min=12),
 M.levar(FRASE, ['Estar à vista no autocarro não apaga o direito à imagem.',
                 'A Declaração conta em Portugal porque a Constituição manda ler os direitos de harmonia com ela.']),
]

# o lugar da certa em cada escolha (0, 1 ou 2), com a semente do motor: nunca o mesmo em mais de metade, nem três seguidos
LUGARES = (1, 0, 2, 1, 2, 0)

DEPOIS = ('<article class="c"><p class="rot">O passo do teu projeto</p><p class="tit">Três perguntas candidatas</p>'
          '<p class="sub">O projeto do módulo é um teatro-documento só teu: as falas vêm do que investigas (entrevistas, documentos e '
          'dados). Hoje escreves, em papel, três perguntas candidatas. O que conta: cada uma cabe numa frase e fala do que é ser '
          'humano; não se responde com «sim» ou «não»; não se resolve com cinco minutos de pesquisa; investiga-se aqui, na escola, '
          'no bairro ou na família; diz de quem ou de que situação fala, sem nomear colegas.</p>'
          '<p class="ir"><a href="../../../projeto/#pergunta-resposta">O enunciado da Pergunta Humana</a></p></article>')


def sessao():
    d = {
        'id': 'cidadania-m1-s01', 'chave': 'epi-cid-m1-s01', 'versao': '2026-11-05-molde', 'marca': 'CD', 'molde': L.MOLDE,
        'titulo': 'Sessão 01: Uma fotografia no grupo', 'h1': 'Cidadania, módulo 1, sessão 01: Uma fotografia no grupo',
        'modulo': {'n': 1, 'nome': 'Humanos', 'url': L.LENTE + 'cidadania/piloto/m1/'},
        'saida': 'cidadania/m1/sessoes/01/index.html',
        # 06/11/2026: a sessão 02 passou ao molde final, em cidadania/m1/sessoes/02/; a seguinte é essa.
        'seguinte': '../02/', 'seguinteRotulo': 'Sessão 02: A imagem dos outros',
        'fontes': M.ref('Declaração Universal dos Direitos Humanos (Nações Unidas, 10 de dezembro de 1948), artigos 1.º, 12.º e 19.º, na '
                        'transcrição portuguesa do UNRIC. Constituição da República Portuguesa, artigos 16.º, n.º 2, 18.º, n.º 1, 26.º, '
                        'n.º 1, e 34.º, n.º 1, no Diário da República. Acórdão do Tribunal da Relação de Évora de 25 de junho de 2015, '
                        'processo 789/13.7TMSTB-B.E1, em dgsi.pt. Convenção sobre os Direitos da Criança (Nova Iorque, 1989), ratificada '
                        'por Portugal em 1990, na Coleção de Tratados das Nações Unidas. Fotografia: Eleanor Roosevelt com a Declaração '
                        'Universal, Lake Success, novembro de 1949, Franklin D. Roosevelt Presidential Library & Museum, 64-165, '
                        'CC BY 2.0. Marina Abramović, _Rhythm 0_, Studio Morra, Nápoles, 1974, segundo a Moderna galerija de Ljubljana '
                        '(MG+MSUM). O cargo de Eleanor Roosevelt: Nações Unidas, «Drafters of the Declaration». O caso da Sara, o das mensagens '
                        'e o da voz gravada são inventados; o da Relação de Évora é real.'),
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
