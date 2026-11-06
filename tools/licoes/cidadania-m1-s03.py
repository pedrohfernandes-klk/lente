# Fonte da sessão 03 do M1 de Cidadania, «Quem tem lugar?», na versão final do molde cidadania-2026-11 (plano do molde, secção 3,
# linha «03»; decisões 144 a 146, 152 a 155, 161 e 166 a 168). 06/11/2026: substitui a fonte do piloto de 31/10, que escrevia
# cidadania/piloto/m1-s03/ (essa página fica como está até ao pedido 3, que faz os redirecionamentos do piloto de uma vez); a chave
# epi-cid-m1-s03 é a mesma, e a versão sobe com preservarAnterior (cfg da família). Corre-se para escrever o .json ao lado; o .json
# é que o gerador (tools/licoes_lente.py) lê, e nunca se edita à mão. Os cartões montam-se com o ajudante comum
# tools/cidadania_molde.py; cada excerto de lei vem do registo tools/cidadania_fontes.json (texto exato da fonte oficial, aberta a
# 6/11/2026, confirmado) e o ajudante recusa escrever um excerto que lá não esteja.
#
# 23 cartões (9 de ler, 14 de fazer), pela ordem e com os tempos da secção 2 do plano, como a s01 e a s02; a ordem é fixa
# (cfg.aula) e a resposta certa de cada escolha fica no lugar pedido em LUGARES, calculado com a semente do motor. Cada exercício tem
# a sua pista, que não dá a resposta. O que só o docente faz vive no guia (tools/cidadania_piloto.py, GUIA['03']), nunca aqui.
#
# Fontes abertas a 6/11/2026, uma de cada vez (nada citado de memória):
# - Constituição, artigos 13.º e 71.º, versão consolidada no Diário da República Eletrónico (registo crp-13-1, crp-13-2, crp-71-1);
# - Convenção sobre os Direitos da Criança, artigos 1.º e 23.º, na tradução portuguesa anexa à Resolução da Assembleia da República
#   n.º 20/90, no Diário da República Eletrónico (registo cdc-1, cdc-23-1; as Retificações n.º 1/91 e n.º 8/91 não tocam nestes
#   artigos); a grafia é a da fonte («activa»);
# - Lei n.º 46/2006, artigos 3.º, alínea b), e 4.º, alínea e), versão consolidada no Diário da República Eletrónico (registo
#   lei46-3b, lei46-4e; a alínea e) do artigo 4.º só aparece numa nota do guia);
# - O caso real (decisão 161): Tribunal Europeu dos Direitos Humanos, Enver Şahin c. Turquia, queixa n.º 23065/12, acórdão de 30 de
#   janeiro de 2018, no HUDOC (https://hudoc.echr.coe.int/eng?i=001-180499, texto em inglês aberto a 6/11/2026). Não há tradução
#   portuguesa no HUDOC; por isso o cartão não cita: conta os factos e a razão do Tribunal por palavras nossas, fiéis ao acórdão
#   (§§ 6 a 10 e 69 a 72; dispositivo, ponto 3, por seis votos contra um);
# - Fotografia: Esther Bubley, setembro de 1943, placa numa estação de autocarros de Rome, na Geórgia. O ficheiro
#   img/cidadania/bubley-sala-de-espera-1943.webp (640 × 671) é o do piloto, a versão do Wikimedia Commons com as margens cortadas
#   (https://commons.wikimedia.org/wiki/File:1943_Colored_Waiting_Room_Sign.jpg, aberto a 6/11/2026: Esther Bubley, setembro de
#   1943, estação Greyhound de Rome, Geórgia, Library of Congress cph.3b22541, «Public domain», PD-US-no notice). 06/11/2026
#   (revisão): o «Registo de origem» é o handle oficial da Library of Congress para cph.3b22541
#   (https://hdl.loc.gov/loc.pnp/cph.3b22541, que resolve para loc.gov/pictures/resource/cph.3b22541/); o handle resolve para o
#   registo 2017862110 da Library of Congress (o mesmo que loc.gov/item/2017862110; reproduções LC-DIG-fsa-8d33365 e
#   LC-USZ62-75338); o crédito liga pelo handle, o número que nomeia (confirmação de 6/11/2026);
# - R1: _The Egg_, conto de Andy Weir, como no #84 (s03). 06/11/2026 (revisão): a premissa confere com o texto no sítio do autor
#   (https://galactanet.com/oneoff/theegg_mod.html, aberto a 6/11/2026: «I'm every human being who ever lived?» «Or who will ever
#   live, yes.»); o cartão só usa a premissa;
# - Vídeo (decisão 155): nenhum. O plano não propõe candidato para esta sessão, e o vídeo do piloto (TED-Ed, o símbolo de acesso)
#   não foi visto por inteiro.
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

IMG = '../../../../img/cidadania/bubley-sala-de-espera-1943.webp'
ALT = ('Uma placa presa a uma barra de ferro, contra o céu. Em letras grandes, a palavra «COLORED»; por baixo, uma seta para a '
       'esquerda e as palavras «WAITING ROOM». Em baixo, o alto de uma parede de tijolo e fios elétricos.')
ALT_VER = 'A mesma fotografia: a placa com «COLORED» e uma seta para a esquerda com «WAITING ROOM», contra o céu.'
VER = f'<img src="{IMG}" alt="{ALT_VER}">'
LOC = 'https://hdl.loc.gov/loc.pnp/cph.3b22541'  # 06/11/2026 (revisão): o handle do registo cph.3b22541
COMMONS = 'https://commons.wikimedia.org/wiki/File:1943_Colored_Waiting_Room_Sign.jpg'
DRE_CRP = 'https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-aprovacao-constituicao/1976-34520775'
DRE_CDC = 'https://diariodarepublica.pt/dr/detalhe/resolucao-assembleia-republica/20-1990-222390'
DRE_L46 = 'https://diariodarepublica.pt/dr/legislacao-consolidada/lei/2006-156233888'
HUDOC = 'https://hudoc.echr.coe.int/eng?i=001-180499'
CREDITO = ('Esther Bubley, placa numa estação de autocarros Greyhound, Rome, Geórgia, setembro de 1943. Library of Congress '
           '(cph.3b22541). '
           f'<a href="{LOC}">Registo de origem</a>; <a href="{COMMONS}">ficheiro no Wikimedia Commons</a>. Domínio público.')
PERGUNTA = 'Uma regra igual para todos pode deixar alguém de fora?'
DECIDE_Q = 'A mostra deve mudar para o rés do chão, mesmo que a sala seja pior?'
FRASE = 'Uma regra igual para todos pode ter efeitos desiguais.'


def escolha(rot, p, p2, certa, erradas, f, minutos, tipo, conceito, **extra):
    """Uma escolha de três opções; a certa vai para o lugar de LUGARES (preenchido em sessao())."""
    c = M.fazer('escolha', rot, p, p2, f, minutos, tipo, conceito, **extra)
    c['_certa'], c['_erradas'] = M.ref(certa), [(M.ref(o), M.ref(e)) for o, e in erradas]
    return c


CARTOES = [
 # ---------------------------------------------------------------- parte 1, ver antes de concluir (60 minutos)
 # O caso do Rui vem do piloto (s03, cartão 1), reescrito: sem «grupo» (decisão 146), com a idade (a Convenção vale até aos 18
 # anos, artigo 1.º) e sem a resposta no caso. A frase do Rui («quero estar nela») fica para a Volta ao caso, onde é informação nova.
 M.abre('Quem tem lugar?',
        f'ver e ler (60{NB}min), pausa (10{NB}min), pesar e escrever (50{NB}min) e o teu projeto (45{NB}min).',
        'A turma prepara a mostra do período: cada aluno apresenta o seu trabalho e, no fim, há um debate. A sala marcada é a '
        'do primeiro andar, a de melhor luz, e não há elevador. O Rui, de 16 anos, usa cadeira de rodas. A organização propõe '
        'enviar-lhe o vídeo da mostra no próprio dia.',
        PERGUNTA),
 M.decide(DECIDE_Q, [
     ('Quem acha que sim', 'A mostra é de toda a turma. Uma sala onde um aluno não entra não serve, por melhor que seja a luz.'),
     ('Quem acha que não', 'A sala de cima está marcada e tem a melhor luz. Com o vídeo, o Rui vê a mostra inteira.'),
     ('Uma objeção', 'E se a sala de baixo tiver menos lugares? Há outra solução?')]),
 # R1: a obra do #84 s03 (The Egg, de Andy Weir), como está: a premissa do conto e a pergunta sobre a mostra. As opções foram
 # acertadas ao molde (comprimentos e um retorno por opção); o retorno não ensina a charneira 1 (ver não é participar).
 M.recupera(escolha(
     'Se pudesses ser qualquer um',
     'No conto _The Egg_, de Andy Weir, um homem morre e descobre que vai viver a vida de cada pessoa. Se pudesses ser qualquer '
     'colega, aceitavas a sala de cima?',
     'Imagina, como no conto _The Egg_, que podes vir a ser qualquer pessoa da turma. A mostra no primeiro andar, sem elevador, '
     'continua a parecer-te justa?',
     'Não: podia ser eu a ficar à porta da sala de cima.',
     [('Sim, porque a regra é a mesma para toda a turma.',
       'A regra é a mesma, mas não chega igual a todos: o Rui não sobe a escada. O conto pede-te que te ponhas no lugar de cada '
       'pessoa. Imagina que acordas na vida do Rui.'),
      ('Sim: o Rui recebe o vídeo no próprio dia da mostra.',
       'Imagina que acordas na vida do Rui, no dia da mostra: a turma está na sala de cima e tu não consegues subir. O conto pede-te '
       'que julgues a regra a partir desse lugar.')],
     'No conto, quem julga uma regra pode vir a ocupar qualquer lugar. Se pudesses ser o Rui, a sala de cima deixava-te à porta, por '
     'igual que a regra pareça. É a pergunta de hoje.',
     3, 'aplicar', 'pôr-se no lugar do outro', pista='Pensa no que o conto faz a quem julga: que lugares pode vir a ocupar?')),
 # R2: força jurídica (sessão 01), um item novo. Falso; usa as palavras do Conceito da s01 (artigo 18.º, n.º 1).
 M.recupera(M.fazer(
     'vf', 'Mais do que uma declaração',
     'Caso inventado: a direção lembra que a Declaração Universal não é lei. Conclui que nenhum texto a obriga a tratar o Rui como '
     'os outros alunos.',
     'Como a Declaração Universal não é lei, nenhum texto obriga a escola a tratar o Rui como os outros alunos.',
     'É falso: a Constituição obriga a escola, porque os direitos, liberdades e garantias «vinculam as entidades públicas e '
     'privadas» (artigo 18.º, n.º 1). É a força jurídica que viste na sessão 01.',
     4, 'distinguir', 'força jurídica', v=False,
     fe='A Declaração não é o único texto. A Constituição diz que os direitos, liberdades e garantias «vinculam as entidades públicas '
        'e privadas» (artigo 18.º, n.º 1), e uma escola é uma delas. Volta à sessão 01, aos três textos e à força de cada um.',
     citacoes=[('crp-18-1', 'vinculam as entidades públicas e privadas')],
     pista='Lembra-te dos três textos da sessão 01 e de quem cada um obriga.'),
     origem='cidadania/m1/sessoes/01/'),
 M.olha('Uma placa de 1943', 'Olha primeiro; só depois lê a legenda.',
        M.figura(IMG, ALT, CREDITO, 'Estação de autocarros de Rome, na Geórgia (Estados Unidos), em setembro de 1943. «Colored waiting '
                 'room»: sala de espera para «pessoas de cor».', artefacto='A placa de uma sala de espera, Rome, 1943', largura=640,
                 altura=671)),
 # Conceito espaçado (origem): a distinção da sessão 01 (cartão 7, «Imagem, legenda ou nenhuma»), duas sessões antes.
 M.fazer('emparelhar', 'Imagem, legenda ou nenhuma',
         'Para cada frase: vê-se na fotografia, só a legenda o diz, ou nenhuma das duas o prova?',
         'De onde vem cada informação: da fotografia, da legenda, ou de nenhuma das duas?',
         'A seta vê-se. A estação e a data, só a legenda as dá. Que toda a gente fizesse o que a placa mandava, nem a fotografia nem a '
         'legenda o mostram. É a distinção que fizeste na sessão 01, com a fotografia de Eleanor Roosevelt.',
         3, 'distinguir', 'imagem e legenda', ver=VER, origem='cidadania/m1/sessoes/01/',
         pares=[['Uma seta indica de que lado fica a sala.', 'Vê-se na fotografia'],
                ['A placa estava numa estação de autocarros.', 'Só a legenda o diz'],
                ['Quem passava ali fazia o que a placa mandava.', 'Nenhuma das duas o prova']],
         fe='A confusão mais provável é tomar o que a placa manda pelo que as pessoas faziam: uma ordem escrita não prova que foi '
            'cumprida. Volta à fotografia e tapa a legenda.',
         pista='Para cada frase, pergunta-te onde a leste ou viste.'),
 # «Placa ou escada» (piloto, 9): a separação escrita na regra e a barreira sem regra escrita. O distrator «uma sala para cada um»
 # é o argumento histórico do «separados, mas iguais»; o outro supõe uma intenção que o caso não diz.
 escolha('Placa ou escada',
         'A placa de 1943 e a escada da mostra deixam pessoas de fora. Em que são diferentes?',
         'A placa e a escada da mostra afastam pessoas. O que tem a placa que a escada não tem?',
         'Na placa, quem fica à parte está escrito na regra.',
         [('Na placa ninguém fica de fora: cada um tem a sua sala.',
           'Uma sala à parte, escolhida pela cor da pele, é pôr pessoas de lado: a placa manda uns para outro sítio só por serem quem '
           'são. Volta à legenda e à seta.'),
          ('Na escada, alguém quis afastar o Rui da mostra.',
           'Nada no caso diz que a sala foi escolhida para afastar o Rui: foi pela luz. Uma barreira pode deixar alguém de fora sem que '
           'ninguém o queira. Volta ao caso.')],
         'A placa escreve na própria regra quem vai para onde, pela cor da pele. Na mostra, nenhuma regra diz que o Rui não entra: a '
         'regra é igual para todos, e é a escada que o deixa de fora.',
         3, 'distinguir', 'igual no papel e no efeito', ver=VER, pista='Compara as duas: o que diz cada regra e o que faz?'),
 M.le('Igualdade na lei', 'De que protegem?',
      # 06/11/2026: na margem só cabe um rótulo curto («Artigo 13.º», como na s01); o documento e o número vão na linha da fonte.
      [(f'Artigo{NB}13.º', 'Ninguém pode ser privilegiado, beneficiado, prejudicado, privado de qualquer direito ou isento de qualquer '
                          'dever em razão de ascendência, sexo, raça, língua […]', 'crp-13-2', 'n2'),
       (f'Artigo{NB}23.º', '[…] reconhecem à criança mental e fisicamente deficiente o direito a uma vida plena e decente em condições '
                          'que […] facilitem a sua participação activa na vida da comunidade.', 'cdc-23-1', 'c23')],
      f'<a href="{DRE_CRP}">Constituição, artigo 13.º, n.º 2</a>; <a href="{DRE_CDC}">Convenção sobre os Direitos da Criança, artigo '
      '23.º, n.º 1</a>',
      mais=(M.lei([('Constituição, artigo 13.º, n.º 1', 'Todos os cidadãos têm a mesma dignidade social e são iguais perante a lei.',
                    'crp-13-1', None),
                   ('Constituição, artigo 71.º, n.º 1', 'Os cidadãos portadores de deficiência física ou mental gozam plenamente dos '
                    'direitos […]', 'crp-71-1', None),
                   ('Convenção, artigo 1.º', '[…] criança é todo o ser humano menor de 18 anos […]', 'cdc-1', None)]))),
 # Leitura exata: o que o n.º 2 proíbe, nas duas palavras que dizem uma perda (piloto, cartão 5 do Lê antigo).
 M.fazer('sublinhar', 'Como se fica a perder',
         'No artigo 13.º, n.º 2, sublinha as duas palavras que dizem como alguém pode ficar a perder.',
         'No n.º 2 do artigo 13.º, que duas palavras descrevem uma perda para quem é tratado de forma diferente? Sublinha-as.',
         'Ninguém pode ser «prejudicado» nem «privado de qualquer direito» por causa da origem, do sexo, da língua ou da religião, entre '
         'outras razões. As outras três também são proibidas, mas dizem um ganho: «privilegiado», «beneficiado» e «isento» de um dever.',
         3, 'reconhecer', 'princípio da igualdade',
         frase=('Ninguém pode ser privilegiado, beneficiado, prejudicado, privado de qualquer direito ou isento de qualquer dever em razão '
                'de ascendência, sexo, raça, língua, território de origem, religião, convicções políticas ou ideológicas, instrução, '
                'situação económica, condição social ou orientação sexual.'),
         certas=[5, 6], fonte='crp-13-2', l='n2',
         citacoes=[('crp-13-2', 'privado de qualquer direito'), ('crp-13-2', 'prejudicado'), ('crp-13-2', 'privilegiado'),
                   ('crp-13-2', 'beneficiado'), ('crp-13-2', 'isento')],
         fe='A confusão mais provável é sublinhar «privilegiado» ou «beneficiado»: também são proibidos, mas dizem como alguém fica a '
            'ganhar. Procura as duas que dizem uma perda.',
         pista='Separa as palavras que dizem ganhar das que dizem perder.'),
 # Um limite: a lista do n.º 2 não diz «deficiência»; outros textos protegem o Rui (a Convenção, artigo 23.º; a Constituição,
 # artigo 71.º, no «Ler mais»). Não se diz nada sobre a lista ser exemplificativa: só o que os textos dizem.
 escolha('Fora da lista',
         'A lista do artigo 13.º, n.º 2, não diz «deficiência». Que conclusão podes tirar para o Rui?',
         'A deficiência não aparece entre as razões do artigo 13.º, n.º 2. O que muda isso para o Rui?',
         'Há outro texto que o protege: a Convenção, artigo 23.º.',
         [('A Constituição não o protege: a deficiência não vem nessa lista.',
           'A lista do n.º 2 não é o único texto: a Constituição tem o artigo 71.º, e a Convenção reconhece à criança com deficiência '
           'direitos próprios. O Rui tem 16 anos. Volta ao artigo 23.º.'),
          ('Fica protegido só se o regulamento da escola o disser.',
           'Um regulamento tem de respeitar a Convenção, um tratado que obriga Portugal desde 1990 (sessão 01). A proteção não depende '
           'de a escola a pôr por escrito. Volta ao artigo 23.º.')],
         'A lista do n.º 2 não esgota a proteção: a Convenção reconhece à criança com deficiência o direito a condições que «garantam a '
         'sua dignidade, favoreçam a sua autonomia». E a Constituição tem um artigo só para a deficiência, o 71.º.',
         4, 'distinguir', 'o limite da lista',
         citacoes=[('cdc-23-1', 'garantam a sua dignidade, favoreçam a sua autonomia')],
         pista='Antes de concluir, relê os dois textos até ao fim.'),
 # Situação nova sem as palavras do texto: as barreiras no espaço, na informação, na decisão e no horário (piloto, cartão 5).
 M.fazer('emparelhar', 'Onde está a barreira',
         'Situações novas, numa escola: onde está a barreira que deixa alguém de fora?',
         'Liga cada situação ao sítio onde está o que impede alguém de participar.',
         'Uma barreira pode estar no espaço (os degraus), na informação (um aviso só dito em voz alta), na forma de decidir (sem ouvir '
         'quem é afetado) ou no horário (depois do último autocarro). Nenhuma está escrita como proibição, e todas deixam alguém de fora.',
         3, 'aplicar', 'barreiras',
         pares=[['Três degraus à porta do laboratório.', 'No espaço'],
                ['O aviso da visita só é dito em voz alta; a Joana é surda.', 'Na informação'],
                ['A direção muda as regras do bar sem ouvir os alunos.', 'Na decisão'],
                ['O clube de teatro ensaia às 19h, depois do último autocarro.', 'No horário']],
         fe='A confusão mais provável é ver barreiras só no espaço. Pergunta a cada situação o que impede a pessoa de participar: o '
            'sítio, o que se diz, quem decide ou a hora?',
         pista='Imagina-te em cada situação: o que te falta para participar?'),
 # Charneira 1: «assistir não é participar» (piloto, cartão 15), aplicada ao caso com a expressão do artigo 23.º.
 M.fazer('vf', 'O que o vídeo dá',
         'Com o vídeo que recebe no próprio dia, o Rui participa na mostra e no debate como os colegas.',
         'Se receber o vídeo no próprio dia, o Rui fica a participar na mostra da mesma forma que os colegas.',
         'É falso: pelo vídeo, o Rui vê; não apresenta o seu trabalho nem fala no debate. O artigo 23.º pede condições que «facilitem a sua '
         'participação activa na vida da comunidade»: participar é estar e intervir, não só ver.',
         4, 'aplicar', 'participar e assistir', v=False,
         citacoes=[('cdc-23-1', 'facilitem a sua participação activa na vida da comunidade'), ('cdc-23-1', 'participação activa')],
         fe='Ver não é o mesmo que participar: pelo vídeo, o Rui não apresenta o trabalho nem fala no debate. O artigo 23.º fala de '
            '«participação activa». Relê o caso: o que faz cada aluno na mostra?',
         pista='Lista o que cada aluno faz na mostra.'),
 # Conceito (uma vez só): igualdade no papel e no efeito. Os três exemplos paralelos vão em tabela (decisão 152). O nome e a
 # definição assentam na Lei n.º 46/2006, artigo 3.º, alínea b) (no «Ler mais», com a exceção do fim legítimo).
 M.conceito('Igual no papel, desigual no efeito',
            '<p>A sala é igual para todos. Onde falha?</p>',
            '<table class="tabela"><thead><tr><th scope="col">Regra</th><th scope="col">No papel</th><th scope="col">No efeito</th></tr>'
            '</thead><tbody>'
            '<tr><td data-th="Regra">a placa de 1943</td><td data-th="No papel">separa pela cor</td><td data-th="No efeito">afasta quem nomeia</td></tr>'
            '<tr><td data-th="Regra">a sala de cima</td><td data-th="No papel">igual para todos</td><td data-th="No efeito">deixa o Rui à porta</td></tr>'
            '</tbody></table>',
            'Discriminação indireta', 'Uma regra que parece neutra e põe algumas pessoas em desvantagem.',
            '<p>Não precisa de má intenção: conta o efeito.</p>',
            mais=(f'<p>A <a href="{DRE_L46}">Lei n.º 46/2006</a> (artigo 3.º, alínea b)) chama {M.citado("lei46-3b", "Discriminação indirecta")} '
                  'à que ocorre quando uma prática '
                  f'{M.citado("lei46-3b", "aparentemente neutra seja susceptível de colocar pessoas com deficiência numa posição de desvantagem")}, '
                  f'salvo se for justificada {M.citado("lei46-3b", "por um fim legítimo")}, com meios '
                  f'{M.citado("lei46-3b", "adequados e necessários")}.</p>')),
 # Transferir 1: o horário de uma atividade (plano), com a religião, uma das razões do artigo 13.º, n.º 2.
 escolha('O dia da visita',
         'Caso inventado: por maioria, a turma marca a visita de estudo para o dia de uma festa religiosa de duas colegas. Elas não '
         'podem ir. O que pesa?',
         'A visita de estudo, votada pela turma, calha no dia de uma festa religiosa de duas colegas, que assim não podem ir. O que conta?',
         'A data é igual para todos, mas afasta as duas.',
         [('A maioria votou; quem perde a votação aceita.',
           'Votar escolhe a data, mas não apaga o efeito: as duas ficam de fora por causa da religião, uma das razões do artigo 13.º, '
           'n.º 2. Volta ao efeito da regra, e não só à forma de a escolher.'),
          ('Só há problema se alguém as quiser afastar.',
           'Não é preciso querer afastar: a discriminação indireta vê-se no efeito de uma regra que parece neutra. Relê o que o '
           'conceito não exige.')],
         'Votar escolhe a data, mas não apaga o efeito: a regra é igual para todos e deixa duas colegas de fora por causa da «religião», '
         'uma das razões do artigo 13.º, n.º 2. É uma regra igual no papel e desigual no efeito.',
         3, 'transferir', 'discriminação indireta', citacoes=[('crp-13-2', 'religião')],
         pista='Pergunta-te quem fica de fora, e porquê.'),
 # Decisão 161: o caso real, com fonte oficial aberta (HUDOC, o sítio do Tribunal Europeu dos Direitos Humanos). Não há tradução
 # portuguesa: o cartão não cita; conta, por palavras nossas, o que o acórdão diz (§§ 6, 7, 10, 69, 72 e o dispositivo).
 escolha('Um caso real',
         'Caso real (Tribunal Europeu dos Direitos Humanos, 2018): um estudante paraplégico pediu obras na faculdade, num edifício de '
         'três pisos. Ofereceram-lhe um acompanhante. Para o Tribunal, porque não bastava?',
         'Em 2018, o Tribunal Europeu dos Direitos Humanos deu razão a um estudante paraplégico a quem a faculdade ofereceu um '
         'acompanhante, em vez de obras. Porquê?',
         'Ignorava a necessidade dele de ser o mais autónomo possível.',
         [('A faculdade recusou logo o pedido de obras do estudante.',
           'O Tribunal nota que a faculdade não recusou logo os pedidos (§ 69): ofereceu um acompanhante. O problema foi oferecê-lo sem '
           'avaliar a situação dele. Volta ao que lhe ofereceram.'),
          ('As aulas práticas eram dadas no rés do chão do próprio edifício.',
           'Era a administração que o lembrava; as aulas teóricas eram num edifício de três pisos. O Tribunal julgou a oferta do acompanhante. '
           'Volta ao que lhe ofereceram e ao que o Tribunal disse dessa oferta.')],
         'Para o Tribunal, a ajuda de um acompanhante, oferecida sem avaliar a situação dele, não era razoável: ignorava a necessidade de '
         'viver da forma mais independente e autónoma possível. Concluiu que houve discriminação no direito à instrução.',
         4, 'transferir', 'autonomia',
         # 06/11/2026 (revisão): o nome do caso iria em itálico, mas a ligação é inline-flex (lesson.css) e o <i> parte-a em colunas;
         # como na s01 e na s02, a ligação nomeia o tribunal e a data (o nome, em itálico, está nas fontes e no guia)
         liga=[{'t': 'Ler o acórdão do Tribunal Europeu dos Direitos Humanos, 30/01/2018 (HUDOC, em inglês)', 'href': HUDOC}],
         pista='Separa o que a universidade alegou do que o Tribunal decidiu.'),
 # ---------------------------------------------------------------- parte 2, pesar e escrever (50 minutos)
 # Volta ao caso: o orçamento de cinco unidades (guia do piloto), com três medidas que não cabem todas: dois direitos e uma razão
 # que chocam (a participação do Rui, o debate da Joana e os lugares dos convidados).
 M.volta('Cinco unidades',
         'A direção dá cinco unidades. Mudar para o rés do chão custa três, e lá só cabe um convidado por aluno, em vez de dois. '
         'Legendar o debate, para a Joana, que é surda, custa duas. Transmitir para o átrio, para os outros convidados, custa duas. '
         'Alguns pais protestam: «Por causa de um, perdem todos.» O Rui: «Não quero ver a mostra; quero estar nela.»',
         carimbo='Caso inventado.'),
 M.fazer('emparelhar', 'O que se sabe e o que falta',
         'Depois do que o Rui disse: o que já está no caso e o que ainda falta saber?',
         'Em cada linha: está no caso ou ainda falta saber?',
         'Sabes o que custa cada medida e o que o Rui pede. Não sabes se a sala de baixo serve aos trabalhos, nem quantos convidados vêm: '
         'se vierem poucos, um lugar por aluno pode chegar. São estas as dúvidas que vão para o papel.',
         3, 'aplicar', 'facto e dúvida',
         pares=[['O que custa mudar para o rés do chão', 'Já está no caso'],
                ['O que o Rui quer da mostra', 'Já está no caso'],
                ['Se a sala de baixo serve aos trabalhos', 'Ainda está em aberto'],
                ['Quantos convidados vêm de facto', 'Ainda está em aberto']],
         fe='A confusão mais provável é dar por sabido quantos convidados vêm, por causa do protesto dos pais: «perdem todos» é uma razão, '
            'não uma contagem. Volta ao caso e separa o que está nele do que alguém afirma.',
         pista='Procura cada informação no texto do caso.'),
 M.em_turma(DECIDE_Q, [
     # 06/11/2026 (revisão): o lado dos pais leva as duas condições da lei (o fim legítimo e os meios); para o cartão caber nas 140
     # palavras, o lado do Rui cita até «participação activa» e a objeção diz «não acompanha».
     ('O lado do Rui', f'A Convenção pede condições que {M.citado("cdc-23-1", "facilitem a sua participação activa")}; '
                       'pelo vídeo, só vê.'),
     ('O lado dos pais', f'Uma regra pode justificar-se {M.citado("lei46-3b", "por um fim legítimo")}, com meios '
                         f'{M.citado("lei46-3b", "adequados e necessários")}: em cima cabem dois convidados.'),
     ('Uma objeção', f'E a Joana? Sem legendas, não acompanha o debate. Todos têm {M.citado("crp-13-1", "a mesma dignidade social")}.')],
     {'O que se faz': 'Decides outra vez e gastas sozinho as cinco unidades.',
      'Quanto tempo': 'Três minutos; em turma, até treze.',
      'O que fica escrito': 'Nada em papel; a escolha fica nos artefactos.',
      'Se estás sozinho': 'Compara com a escolha do início e abre os três lados.'},
     prova=('Como gastas as cinco unidades?', ('Mudar e legendar', 'Mudar e transmitir', 'Legendar e transmitir')),
     prova_rot='Como gastaste as cinco unidades', intro='', nota=None),
 M.fazer('emparelhar', 'Facto, regra ou razão',
         'Liga cada frase ao que ela é numa justificação.',
         'Facto, regra ou razão de uma das partes: o que é cada frase?',
         'Que a sala fica num primeiro andar sem elevador é um facto do caso; o artigo 23.º é uma regra escrita num texto legal; «Por '
         'causa de um, perdem todos» é a razão de alguns pais, que ainda tem de ser pesada.',
         3, 'distinguir', 'relato e princípio',
         pares=[['A sala de cima fica num primeiro andar sem elevador.', 'Um facto do caso'],
                ['«[…] facilitem a sua participação activa na vida da comunidade.»', 'Uma regra escrita num texto legal'],
                ['«Por causa de um, perdem todos.»', 'A razão de uma das partes']],
         citacoes=[('cdc-23-1', 'facilitem a sua participação activa na vida da comunidade')],
         fe='A confusão mais provável é tomar a razão de uma parte por regra: «Por causa de um, perdem todos» diz o que alguns pais '
            'pensam, mas não está em nenhuma lei. Volta ao artigo 23.º.',
         pista='Pergunta a cada frase de onde vem e a quem se aplica.'),
 M.fazer('ordenar', 'A justificação por ordem',
         'Põe a justificação por ordem: primeiro o facto, depois a fonte, a aplicação e, no fim, o limite.',
         'Ordena: o que aconteceu, o texto que se aplica, a ligação entre os dois e o que ainda falta saber.',
         'Facto, fonte, aplicação, limite: cada passo apoia-se no anterior, e o limite diz até onde a conclusão pode ir.',
         4, 'aplicar', 'facto, fonte, aplicação, limite',
         passos=['A sala marcada fica num primeiro andar sem elevador, e o Rui usa cadeira de rodas.',
                 'A Convenção pede condições que facilitem a participação ativa da criança com deficiência.',
                 'Ver a mostra pelo vídeo não é participar nela: o Rui ficaria só a assistir.',
                 'Falta saber se a sala de baixo serve aos trabalhos.'],
         fe='A confusão mais provável é começar pela lei ou pôr o que falta saber antes da aplicação. Começa pelo que aconteceu; depois o '
            'texto; o que falta saber fecha a justificação.',
         pista='Pergunta-te o que tem de vir primeiro para o resto se apoiar.'),
 # Charneira 2: a conclusão que não vai além das provas; o erro esperado é a razão dos pais tomada por prova, ou uma intenção suposta.
 escolha('O que as provas permitem',
         'Que conclusão fica dentro do que o caso e os textos mostram?',
         'Que conclusão diz o que as provas permitem, sem ir além delas?',
         'Pelo vídeo, o Rui só assiste; ainda não se sabe quantos convidados vêm.',
         [('A mostra fica em cima, porque a maioria perderia os seus lugares.',
           'É a razão de alguns pais, não uma prova: ninguém contou os convidados. E esta conclusão deixa de fora o que o Rui pede. '
           'Separa o que se sabe do que alguém afirma.'),
          ('A organização escolheu a sala de cima para afastar o Rui da mostra.',
           'Nada no caso mostra que a organização queira afastar o Rui: escolheu a sala pela luz. Uma intenção não se supõe; prova-se. '
           'Separa o que aconteceu do que alguém supõe.')],
         'Diz o que as provas mostram (pelo vídeo, o Rui só assiste, e o artigo 23.º pede participação) e deixa aberto o que ninguém '
         'contou: quantos convidados vêm.',
         3, 'aplicar', 'conclusão e provas', pista='Para cada conclusão, pergunta-te que prova a sustenta.'),
 M.papel(PERGUNTA,
         ['A tua conclusão, por agora.',
          'Uma prova: um facto do caso e uma expressão exata, entre aspas, com o artigo.',
          'Uma dúvida que ainda tens.'],
         ['A conclusão responde à pergunta sem ir além das provas.',
          'A prova junta um facto a uma expressão exata, com o artigo.',
          'A dúvida, respondida, podia mudar a conclusão.'],
         '<p>Outro caso, inventado: o aviso da reunião só sai em português, que a mãe da Ana não lê.</p><ol>'
         '<li>Conclusão: o aviso igual para todos deixa-a de fora.</li>'
         f'<li>Prova: só sai em português; ninguém pode ser {M.citado("crp-13-2", "prejudicado […] em razão de […] língua")} '
         '(artigo 13.º, n.º 2).</li>'
         '<li>Dúvida: alguém lhe perguntou que língua lê?</li></ol>',
         'Num papel pequeno, sozinho e sem telemóvel.',
         relogio_min=12),
 M.levar(FRASE, ['Ver não é participar.',
                 'Antes de escolher por alguém, ouve essa pessoa.']),
]

# o lugar da certa em cada escolha (0, 1 ou 2), com a semente do motor: nunca o mesmo em mais de metade, nem três seguidos
LUGARES = (0, 2, 1, 0, 2, 1)

# O passo do projeto (plano, secção 3: «a tua pergunta, delimitada com “Uma boa pergunta” (#84) e a pergunta investigável (piloto,
# 18)»). O que se diz de uma boa pergunta é o que a página do projeto já diz (cidadania/projeto/, «Uma boa pergunta»).
DEPOIS = ('<article class="c"><p class="rot">O passo do teu projeto</p><p class="tit">A tua pergunta</p>'
          '<p class="sub">No teatro-documento, tudo parte de uma pergunta que consegues investigar. Escolhe a tua e escreve-a, em papel, em '
          'três versões: a primeira que te ocorre, uma mais delimitada (que pessoas, que lugar, que tempo) e a final. O que conta: não se '
          'responde com «sim» ou «não»; não se resolve com cinco minutos de pesquisa; pode ser investigada aqui, na escola, no bairro, na '
          'família ou em fontes a que tens acesso.</p>'
          '<p class="ir"><a href="../../../projeto/#pergunta-resposta">Uma boa pergunta, no enunciado da Pergunta Humana</a></p></article>')


def sessao():
    d = {
        'id': 'cidadania-m1-s03', 'chave': 'epi-cid-m1-s03', 'versao': '2026-11-06-molde', 'marca': 'CD', 'molde': L.MOLDE,
        'titulo': 'Sessão 03: Quem tem lugar?', 'h1': 'Cidadania, módulo 1, sessão 03: Quem tem lugar?',
        'modulo': {'n': 1, 'nome': 'Humanos', 'url': L.LENTE + 'cidadania/piloto/m1/'},
        'saida': 'cidadania/m1/sessoes/03/index.html',
        'seguinte': '../../../piloto/m1-s04/', 'seguinteRotulo': 'Sessão 04: Posso dizer tudo?',
        'fontes': M.ref('Constituição da República Portuguesa, artigos 13.º, n.os 1 e 2, 18.º, n.º 1, e 71.º, n.º 1, na versão consolidada do '
                        'Diário da República. Convenção sobre os Direitos da Criança, artigos 1.º e 23.º, n.º 1, na tradução portuguesa '
                        'anexa à Resolução da Assembleia da República n.º 20/90, no Diário da República. Lei n.º 46/2006, de 28 de agosto, '
                        'artigo 3.º, alínea b), no Diário da República. Tribunal Europeu dos Direitos Humanos, _Enver Şahin c. Turquia_, '
                        'queixa n.º 23065/12, acórdão de 30 de janeiro de 2018, no HUDOC (em inglês). Fotografia: Esther Bubley, placa '
                        'numa estação de autocarros de Rome, na Geórgia, setembro de 1943, Library of Congress, domínio público. _The '
                        'Egg_, conto de Andy Weir. O caso do Rui, o da direção e da Declaração, o das barreiras na escola, o da visita de '
                        'estudo e o da reunião com os pais são inventados; o do Tribunal Europeu dos Direitos Humanos é real.'),
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
