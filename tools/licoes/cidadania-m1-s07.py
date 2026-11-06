# Fonte da sessão 07 do M1 de Cidadania, «Nove contra dois», na versão final do molde cidadania-2026-11 (plano do molde, secção 3,
# linha «07»; decisões 144 a 146, 152 a 155, 161 e 166 a 168). 06/11/2026: substitui a fonte do piloto de 31/10, que escrevia
# cidadania/piloto/m1-s07/ (essa página fica como está até ao pedido 3, que faz os redirecionamentos do piloto de uma vez); a chave
# epi-cid-m1-s07 é a mesma, e a versão sobe com preservarAnterior (cfg da família). Corre-se para escrever o .json ao lado; o .json
# é que o gerador (tools/licoes_lente.py) lê, e nunca se edita à mão. Os cartões montam-se com o ajudante comum
# tools/cidadania_molde.py; cada excerto de lei vem do registo tools/cidadania_fontes.json (texto exato da fonte oficial, aberta a
# 6/11/2026, confirmado) e o ajudante recusa escrever um excerto que lá não esteja.
#
# 23 cartões (9 de ler, 14 de fazer), pela ordem e com os tempos da secção 2 do plano, como as sessões 01 a 03; a ordem é fixa
# (cfg.aula) e a resposta certa de cada escolha fica no lugar pedido em LUGARES, calculado com a semente do motor. Cada exercício tem
# a sua pista, que não dá a resposta. O que só o docente faz vive no guia (tools/cidadania_piloto.py, GUIA['07']), nunca aqui.
# A cadeia (cartões 19 a 21) é a das sessões 04 a 07: o aluno encontra o passo em falta (aqui, a fonte).
#
# Fontes abertas a 6/11/2026, uma de cada vez (nada citado de memória):
# - Constituição, artigo 32.º, n.os 2 e 10, versão consolidada no Diário da República Eletrónico (registo crp-32-2, crp-32-10);
# - Declaração Universal dos Direitos Humanos, artigos 10.º, 11.º (primeiro parágrafo) e 12.º, na transcrição do UNRIC (registo
#   dudh-10, dudh-11-1; dudh-12 é o da sessão 01); a grafia é a da fonte («acto», «protecção»);
# - Convenção sobre os Direitos da Criança, artigo 12.º, n.º 2, na tradução portuguesa anexa à Resolução da Assembleia da República
#   n.º 20/90, no Diário da República Eletrónico (registo cdc-12-2; as Retificações n.º 1/91 e n.º 8/91 não tocam neste artigo);
# - O caso real (decisão 161): acórdão do Tribunal da Relação de Évora de 10/10/2023, processo 320/20.8GBSSB.E1, no dgsi.pt
#   (registo tre-2023-instagram, tre-2023-admitimos). O cartão só diz o que o acórdão diz: a conta de Instagram tinha o nome e o dia
#   de anos do arguido; a consulta ao Facebook não deu resultado; o tribunal não conseguiu a certeza de que a conta era dele,
#   aplicou o princípio in dubio pro reo e absolveu-o; a publicação ficou atribuída a «indivíduo não identificado»;
# - Litografia: Honoré Daumier, «Voilà le ministère public qui vous dit des choses très désagréables…», prancha 21 de _Les Gens de
#   Justice_, 24 de agosto de 1846, The Metropolitan Museum of Art, 2013.999.1 (API do museu, objeto 625296, aberta a 6/11/2026:
#   «isPublicDomain»: true; imagem DP833796, 2537 × 3354). O ficheiro novo img/cidadania/daumier-gens-de-justice-21-inteira.webp
#   (760 × 1005) é a prancha inteira, com o título, o número e a legenda, sem filtros nem cortes (plano, secção 2: o documento
#   inteiro). O recorte do piloto (daumier-gens-de-justice-21.webp, sem título nem legenda) fica para a página do piloto;
# - R1: _Doze Homens em Fúria_, filme de Sidney Lumet, como no #84 (s07), corrigido pelo plano: o jurado vota «não culpado», não
#   «inocente». A premissa confere com o registo da Library of Congress (https://www.loc.gov/item/96513458/, aberto a 6/11/2026:
#   «In a preliminary vote, all jurors vote "guilty" except Juror 8»; «If there is any reasonable doubt they are to return a verdict
#   of not guilty»);
# - Vídeo (decisão 155): nenhum. O plano não propõe candidato para esta sessão, e o vídeo do piloto (TED-Ed, democracia em Atenas)
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

IMG = '../../../../img/cidadania/daumier-gens-de-justice-21-inteira.webp'
ALT = ('Litografia a preto e branco, com o título «LES GENS DE JUSTICE» e o número 21. Num tribunal, um homem de toga e barrete '
       'inclina-se para trás; atrás de uma barra de madeira, outro homem, despenteado, debruça-se, e os dois rostos quase se tocam. '
       'À esquerda, outro homem de toga e barrete tem os olhos fechados; ao fundo, o público. Por baixo, duas linhas em francês.')
ALT_VER = 'A mesma litografia: dois homens com os rostos quase encostados, num tribunal, e duas linhas em francês por baixo.'
VER = f'<img src="{IMG}" alt="{ALT_VER}">'
MET = 'https://www.metmuseum.org/art/collection/search/625296'
DRE_CRP = 'https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-aprovacao-constituicao/1976-34520775'
UNRIC = 'https://unric.org/pt/declaracao-universal-dos-direitos-humanos/'
DRE_CDC = 'https://diariodarepublica.pt/dr/detalhe/resolucao-assembleia-republica/20-1990-222390'
DGSI = 'https://www.dgsi.pt/jtre.nsf/134973db04f39bf2802579bf005f080b/aa218f7fd0f67b8180258a4b0053c754?OpenDocument'
CREDITO = ('Honoré Daumier, «Voilà le ministère public qui vous dit des choses très désagréables…», prancha 21 de <i>Les Gens de '
           'Justice</i>, 24 de agosto de 1846, litografia. The Metropolitan Museum of Art, Nova Iorque (2013.999.1). '
           f'<a href="{MET}">Registo de origem</a>. Domínio público; a imagem do museu é CC0.')
PERGUNTA = 'Uma captura de ecrã chega para culpar alguém?'
DECIDE_Q = 'O Tomás deve sair já da peça?'
FRASE = 'Um nome no ecrã não prova quem carregou no botão.'


def escolha(rot, p, p2, certa, erradas, f, minutos, tipo, conceito, **extra):
    """Uma escolha de três opções; a certa vai para o lugar de LUGARES (preenchido em sessao())."""
    c = M.fazer('escolha', rot, p, p2, f, minutos, tipo, conceito, **extra)
    c['_certa'], c['_erradas'] = M.ref(certa), [(M.ref(o), M.ref(e)) for o, e in erradas]
    return c


CARTOES = [
 # ---------------------------------------------------------------- parte 1, ver antes de concluir (60 minutos)
 # O caso do Tomás vem do piloto (s07, cartão 1), reescrito: a peça da turma em vez do grupo de trabalho (decisão 146), a captura
 # mostra uma conta com o nome dele (é isso que se pode provar), e a resposta não está no caso.
 M.abre('Nove contra dois',
        f'ver e ler (60{NB}min), pausa (10{NB}min), pesar e escrever (50{NB}min) e o teu projeto (45{NB}min).',
        'A turma prepara uma peça para o fim do período. No grupo da turma aparece um vídeo do ensaio, montado para gozar com a '
        'Sara. Uma captura de ecrã mostra a conta que o publicou: tem o nome do Tomás. De braço no ar, nove colegas dizem que '
        'foi ele; dois pedem para ver primeiro as provas.',
        PERGUNTA),
 M.decide(DECIDE_Q, [
     ('Quem acha que sim', 'A captura mostra o nome dele. Esperar é deixar a Sara sozinha, com o vídeo a circular.'),
     ('Quem acha que não', 'Ainda ninguém ouviu o Tomás. Tirá-lo já da peça é castigá-lo antes de o ouvir.'),
     ('Uma objeção', 'Há maneira de proteger já a Sara sem castigar o Tomás?')]),
 # R1: a obra do #84 s07 (Doze Homens em Fúria), corrigida pelo plano: o voto é «não culpado», não «inocente». A premissa é a do
 # registo da Library of Congress (ver acima); o retorno não ensina a charneira 1 (o que a captura prova).
 M.recupera(escolha(
     'O voto que ficou sozinho',
     'No filme _Doze Homens em Fúria_, um júri decide se um rapaz matou o pai. Ao início, onze votam «culpado» e um vota «não '
     'culpado». O que diz esse voto?',
     'Em _Doze Homens em Fúria_, de Sidney Lumet, um só jurado vota «não culpado» contra onze. O que quer dizer esse voto?',
     'Que, para ele, a culpa ainda não está provada.',
     [('Que ele acredita que o rapaz está inocente.',
       '«Não culpado» não quer dizer «inocente»: quer dizer que a culpa não ficou provada. No filme, se houver uma dúvida razoável, '
       'o júri não condena. Repara no nome do voto.'),
      ('Que ele quer contrariar a opinião da maioria.',
       'Nada indica que vote para contrariar: o jurado defende que a vida do rapaz merece mais do que um voto rápido. Repara no '
       'nome do voto: diz alguma coisa sobre a culpa?')],
     'Votar «não culpado» é dizer que a culpa não está provada, e não que o rapaz está inocente: com uma dúvida razoável, o júri não '
     'condena. É a pergunta de hoje, com uma captura de ecrã no lugar das provas do filme.',
     3, 'distinguir', 'não culpado e inocente', pista='Lê o nome do voto, palavra a palavra.')),
 # R2: acusação de facto (sessão 04), um item novo: a mesma acusação partilhada nove vezes. Falso; usa as palavras da sessão 04.
 M.recupera(M.fazer(
     'vf', 'Nove vezes a mesma frase',
     'Caso inventado: nove colegas partilham a mesma mensagem, «Foi o Tomás». Assim, há nove provas contra ele.',
     'Se nove pessoas partilharem a mensagem «Foi o Tomás», ficam nove provas de que foi ele.',
     'É falso: nove partilhas são a mesma frase, repetida, e nenhuma diz o que alguém viu. «Foi o Tomás» é uma «acusação de facto»: '
     'tem de se provar. É o que separaste na sessão 04.',
     4, 'aplicar', 'acusação de facto', v=False,
     fe='Repetir uma acusação não a prova: nove partilhas são uma frase, nove vezes. Na sessão 04, viste que uma «acusação de facto» '
        'tem de se provar. Pergunta-te o que viu quem partilhou.',
     pista='Pergunta-te o que cada partilha acrescenta à primeira mensagem.'),
     origem='cidadania/m1/sessoes/04/'),
 M.olha('Um tribunal, em 1846', 'Olha primeiro para as figuras; só depois lê a legenda.',
        M.figura(IMG, ALT, CREDITO, 'Honoré Daumier, <i>Les Gens de Justice</i>, prancha 21, 1846. Por baixo, em francês (tradução '
                 'nossa): «Aí está o Ministério Público a dizer-lhe coisas muito desagradáveis… trate lá de chorar ao menos de um olho… '
                 'fica sempre bem!»', artefacto='Daumier, um conselho no tribunal, 1846', largura=760, altura=1005,
                 rotulo_i='Créditos da litografia')),
 # Conceito espaçado (origem): a distinção da sessão 01 (cartão 7, «Imagem, legenda ou nenhuma»), seis sessões antes.
 M.fazer('emparelhar', 'O que se vê e o que se diz',
         'Para cada frase: vê-se na litografia, só a legenda o diz, ou nenhuma das duas o prova?',
         'De onde vem cada informação: da litografia, da legenda, ou de nenhuma das duas?',
         'Os rostos quase encostados veem-se. O conselho de chorar, só a legenda o dá. Se alguém chorou, e se isso convenceu o tribunal, '
         'nem a litografia nem a legenda o mostram. É a distinção que fizeste na sessão 01.',
         3, 'distinguir', 'imagem e legenda', ver=VER, origem='cidadania/m1/sessoes/01/',
         pares=[['Dois homens têm os rostos quase encostados.', 'Vê-se na litografia'],
                ['Um deles aconselha o outro a chorar.', 'Só a legenda o diz'],
                ['As lágrimas convenceram o tribunal.', 'Nenhuma das duas o prova']],
         fe='A confusão mais provável é tomar o conselho pelo efeito: a legenda diz o que um pede ao outro, não o que o tribunal decidiu. '
            'Volta à litografia e tapa a legenda.',
         pista='Tapa a legenda e vê o que ainda consegues dizer.'),
 # «Comove ou prova» (plano): o gesto que se aconselha e o efeito que se procura. Falso: umas lágrimas não mostram os factos.
 M.fazer('vf', 'Comover não é provar',
         'Se o acusado chorar, como lhe aconselham, o tribunal fica com uma prova de que está inocente.',
         'As lágrimas que a legenda aconselha dariam ao tribunal uma prova da inocência do acusado.',
         'É falso: as lágrimas podem comover quem julga, mas não mostram o que aconteceu. A legenda diz que chorar «fica sempre bem»: '
         'é um efeito em quem vê. Um tribunal decide pelo que se prova.',
         3, 'aplicar', 'comover e provar', v=False, ver=VER,
         fe='Chorar pode comover, e quem dá o conselho conta com isso; mas umas lágrimas não mostram quem fez o quê. Pergunta-te o que o '
            'tribunal ficaria a saber sobre os factos.',
         pista='Pergunta-te o que um tribunal precisa de saber para decidir.'),
 M.le('Quem prova, quem é ouvido', 'Quem prova a culpa? E quem é ouvido?',
      # 06/11/2026: na margem só cabe um rótulo curto («Artigo 32.º», como na s01 e na s03); o documento e o número vão na linha da fonte.
      [(f'Artigo{NB}32.º', 'Todo o arguido se presume inocente até ao trânsito em julgado da sentença de condenação […]', 'crp-32-2', 'n2'),
       (f'Artigo{NB}11.º', 'Toda a pessoa acusada de um acto delituoso presume-se inocente até que a sua culpabilidade fique legalmente '
                          'provada […]', 'dudh-11-1', 'a11'),
       (f'Artigo{NB}32.º', '[…] em quaisquer processos sancionatórios, são assegurados ao arguido os direitos de audiência e defesa.',
        'crp-32-10', 'n10')],
      f'<a href="{DRE_CRP}">Constituição, artigo 32.º, n.os 2 e 10</a>; <a href="{UNRIC}">Declaração Universal, artigo 11.º</a>',
      # 06/11/2026: no «Ler mais», a ligação à fonte oficial vai no rótulo de cada excerto (cabem as 140 palavras do cartão).
      mais=('<p>«Trânsito em julgado»: já não há recurso.</p>'
            + M.lei([(f'<a href="{UNRIC}">Declaração Universal, artigo 10.º</a>', '[…] a que a sua causa seja equitativa e publicamente '
                      'julgada por um tribunal independente e imparcial […]', 'dudh-10', None),
                     (f'<a href="{DRE_CDC}">Convenção sobre os Direitos da Criança, artigo 12.º, n.º 2</a>', '[…] é assegurada à criança a '
                      'oportunidade de ser ouvida nos processos judiciais e administrativos que lhe respeitem […]', 'cdc-12-2', None)]))),
 # Leitura exata: o que tem de acontecer à culpa antes de alguém ser tratado como culpado (Declaração, artigo 11.º).
 M.fazer('sublinhar', 'Antes de ser culpado',
         'No artigo 11.º, sublinha as duas palavras que dizem o que tem de acontecer à culpa antes de alguém ser tratado como culpado.',
         'Segundo o artigo 11.º, até quando se presume inocente quem é acusado? Sublinha as duas palavras que o dizem.',
         'Ninguém é tratado como culpado antes de a culpa ficar «legalmente provada». Até lá, presume-se inocente. Não basta que muitos '
         'acreditem: a prova faz-se num processo, com «garantias necessárias de defesa».',
         3, 'reconhecer', 'presunção de inocência',
         frase=('Toda a pessoa acusada de um acto delituoso presume-se inocente até que a sua culpabilidade fique legalmente provada no '
                'decurso de um processo público em que todas as garantias necessárias de defesa lhe sejam asseguradas.'),
         certas=[16, 17], fonte='dudh-11-1', l='a11',
         citacoes=[('dudh-11-1', 'legalmente provada'), ('dudh-11-1', 'garantias necessárias de defesa')],
         fe='A confusão mais provável é sublinhar «acusada» ou «inocente»: dizem quem é protegido e como fica até lá. Procura o que tem de '
            'acontecer à culpa.',
         pista='Procura o momento a partir do qual alguém deixa de se presumir inocente.'),
 # Aplicação ao caso: onde começa a conclusão, numa frase sobre o Tomás com «por isso» (piloto, cartão 3). A frase usa um dado novo
 # (estar online), para não ensinar aqui o que a captura prova (a charneira 1, no cartão 12).
 M.fazer('sublinhar', 'Onde começa a conclusão',
         'Alguém escreve no grupo da turma esta frase. Sublinha as duas palavras onde deixa de dizer o que se sabe e passa a concluir.',
         'Nesta frase sobre o Tomás, onde termina o que se sabe e começa a conclusão? Sublinha as duas palavras.',
         'Até ao «por isso», a frase diz o que se sabe: o Tomás estava online. Depois, tira uma conclusão que esse dado não mostra: '
         'muitas pessoas podiam estar online à mesma hora. A conclusão começa no «por isso».',
         4, 'distinguir', 'conclusão e dado',
         frase='O Tomás estava online quando o vídeo apareceu, por isso foi ele que o publicou.',
         certas=[8, 9],
         fe='A confusão mais provável é sublinhar «foi ele»: aí a conclusão já vai a meio. Procura as palavras que fazem a passagem do que '
            'se sabe para o que se conclui.',
         pista='Divide a frase em duas: o que se sabe e o que se conclui.'),
 # Situação nova sem as palavras do texto: ser ouvido antes de um castigo, mesmo com fotografias (Constituição, artigo 32.º, n.º 10).
 M.fazer('vf', 'Antes do castigo',
         'Caso inventado: há fotografias claras de um aluno a riscar uma parede da escola. Assim, a direção pode castigá-lo sem o ouvir.',
         'Com fotografias claras de um aluno a riscar uma parede, a direção pode castigá-lo sem lhe dar a palavra.',
         'É falso: em «quaisquer processos sancionatórios», o arguido tem «os direitos de audiência e defesa» (artigo 32.º, n.º 10). '
         'Uma prova forte não dispensa ouvir quem pode ser castigado: pode haver uma explicação que as fotografias não mostram.',
         3, 'aplicar', 'direito a ser ouvido', v=False,
         citacoes=[('crp-32-10', 'quaisquer processos sancionatórios'), ('crp-32-10', 'os direitos de audiência e defesa')],
         fe='Mesmo com fotografias claras, quem pode ser castigado tem direito a ser ouvido e a defender-se, em «quaisquer processos '
            'sancionatórios» (artigo 32.º, n.º 10). Volta a esse número: abre alguma exceção para quando há provas?',
         pista='Procura no artigo 32.º o que vale para quem pode ser castigado.'),
 # Charneira 1: o que prova, com segurança, a captura (piloto, cartão 4). O erro esperado é tomar a conta com o nome pela autoria.
 escolha('O que a captura prova',
         'Com a captura de ecrã na mão, o que se pode afirmar com segurança sobre o Tomás?',
         'A captura é a única prova. Sem ir além dela, o que se pode dizer do Tomás?',
         'Que uma conta com o nome dele publicou o vídeo.',
         [('Que foi ele quem montou e publicou o vídeo.',
           'Isso já vai além da captura: uma conta pode ter o nome de alguém sem ser dessa pessoa, e quem publica pode não ser quem montou. '
           'Volta à captura: o que se vê nela, e só isso?'),
          ('Que ele quis gozar com a Sara diante da turma.',
           'A captura não mostra intenções, e ainda ninguém ouviu o Tomás. Dar-lhe uma intenção é concluir antes de provar quem foi. '
           'Volta à captura e separa o que mostra do que supões.')],
         'A captura prova o que mostra: uma conta com o nome do Tomás publicou o vídeo. Quem criou a conta, quem carregou no botão e com '
         'que intenção são perguntas que pedem outras provas.',
         4, 'aplicar', 'prova e inferência', pista='Para cada frase, pergunta-te se a captura chega para a afirmar.'),
 # Conceito: prova e inferência; «Votar conta posições; deliberar pesa razões» (plano). Itens paralelos em tabela (decisão 152).
 M.conceito('Prova e inferência',
            '<p>A conta tem o nome do Tomás. Nove dizem que foi ele.</p>',
            '<table class="tabela"><thead><tr><th scope="col">Prova</th><th scope="col">Supõe-se</th>'
            '<th scope="col">O que falta</th></tr></thead><tbody>'
            '<tr><td data-th="Prova">a conta com o nome</td><td data-th="Supõe-se">foi ele que publicou</td>'
            '<td data-th="O que falta">quem criou a conta</td></tr>'
            '<tr><td data-th="Prova">nove mãos no ar</td><td data-th="Supõe-se">foi ele</td>'
            '<td data-th="O que falta">quem viu</td></tr>'
            '</tbody></table>',
            'Inferência', 'Uma conclusão que vai além do que a prova mostra.',
            '<p>Não é mentira: pode estar certa, mas falta confirmá-la. Votar conta posições; deliberar pesa razões.</p>'),
 # Transferir 1: o caso ao contrário (piloto, cartão 14): uma prova nova desfaz aquela em que a decisão assentava.
 M.fazer('ordenar', 'Quando a prova muda',
         'Caso inventado, noutra escola: um aluno foi castigado por causa de uma captura. Põe por ordem o que aconteceu e o que daí se '
         'conclui.',
         'Noutra escola, um castigo assentou numa captura, e depois apareceu outra prova. Ordena os factos e a conclusão.',
         'Uma decisão vale o que valem as provas em que assenta. Quando aparece uma prova que as desfaz, a decisão revê-se, e diz-se a '
         'quem soube do castigo que mudou. Manter um erro conhecido é escolher o erro.',
         3, 'transferir', 'rever uma decisão',
         passos=['O castigo assentou numa captura com o nome do aluno.',
                 'Depois, outro aluno confessa que foi ele que o fez.',
                 'A prova em que o castigo assentava deixou de chegar.',
                 'A escola revê a decisão e diz à turma que mudou.'],
         fe='A confusão mais provável é pôr a revisão antes de a prova nova aparecer. Começa pelo que aconteceu; a conclusão vem no fim, '
            'apoiada na prova nova.',
         pista='Pergunta-te o que tem de vir antes para o passo seguinte fazer sentido.'),
 # Decisão 161: o caso real, com fonte oficial aberta (dgsi.pt). O cartão só diz o que o acórdão diz (ver o cabeçalho).
 escolha('Um caso real',
         'Caso real (Relação de Évora, 2023): condenado por um vídeo publicado numa conta de Instagram com o seu nome e dia de anos, um '
         'jovem recorreu. Porque foi absolvido?',
         'Em 2023, a Relação de Évora absolveu um jovem condenado por um vídeo publicado numa conta com o nome dele. Porquê?',
         'Não se provou que aquela conta era mesmo dele.',
         [('Ficou provado que outra pessoa criou aquela conta.',
           'O tribunal não descobriu quem foi: a publicação ficou atribuída a «indivíduo não identificado». Absolveu porque ficou em dúvida, '
           'e não porque provou outra autoria. Volta à razão do tribunal.'),
          ('Publicar o vídeo de uma detenção policial não é crime.',
           'O tribunal não decidiu isso: disse que não conseguia dar como provado que a conta era do jovem. Sem essa prova, a publicação '
           'não lhe pode ser imputada. Volta ao que ficou por provar.')],
         'O tribunal escreveu que, no Instagram, «qualquer pessoa pode criar um perfil de utilizador, sem verificação dos dados». A '
         'consulta ao Facebook não deu resultado. «Admitimos que sim, mas não arriscamos afirmá-lo»: na dúvida, absolveu.',
         4, 'transferir', 'na dúvida, a favor do arguido',
         citacoes=[('tre-2023-instagram', 'qualquer pessoa pode criar um perfil de utilizador, sem verificação dos dados'),
                   ('tre-2023-admitimos', 'Admitimos que sim, mas não arriscamos afirmá-lo'),
                   ('tre-2023-nao-identificado', 'indivíduo não identificado')],
         # como na s01 a s03, a ligação nomeia o tribunal e a data (o número do processo está nas fontes e no guia)
         liga=[{'t': 'Ler o acórdão do Tribunal da Relação de Évora, 10/10/2023 (dgsi.pt)', 'href': DGSI}],
         pista='Separa o que o tribunal provou do que ficou em dúvida.'),
 # ---------------------------------------------------------------- parte 2, pesar e escrever (50 minutos)
 # Volta ao caso: o que o Tomás diz, a razão dos nove e o que a Sara está a passar: a proteção dela e a presunção de inocência dele
 # chocam (o «Somos nove» é o do M1 publicado, sessão 08).
 M.volta('O que diz o Tomás',
         'A direção vai decidir se castiga o Tomás. Ele diz que a conta não é dele e que nunca a criou. Os nove insistem: «Somos nove a '
         'dizer que foi ele.» A Sara já não quer ir aos ensaios enquanto o vídeo circular, e a estreia é daqui a uma semana.',
         carimbo='Caso inventado.'),
 # A dúvida ainda aberta (piloto, cartão 17): a medida que protege a Sara sem castigar já o Tomás. Falso.
 M.fazer('vf', 'Proteger sem castigar',
         'Pedir que o vídeo seja apagado do grupo da turma, antes de se saber quem o fez, já é castigar o Tomás.',
         'Antes de se saber quem montou o vídeo, mandar apagá-lo do grupo da turma é já castigar o Tomás.',
         'É falso: apagar o vídeo protege a Sara já e não decide nada sobre quem o fez. O Tomás continua a presumir-se inocente, e a '
         'direção tem de o ouvir antes de qualquer castigo.',
         3, 'aplicar', 'proteger e castigar', v=False,
         fe='Apagar o vídeo não diz quem o fez: tira-o de circulação para proteger a Sara. Castigar é outra coisa: é decidir sobre o Tomás. '
            'Volta ao caso: o que magoa a Sara, hoje?',
         pista='Pensa no que é um castigo e em quem o recebe.'),
 M.em_turma(DECIDE_Q, [
     ('O lado da Sara', f'Tem direito a {M.citado("dudh-12", "protecção da lei")} contra '
                        f'{M.citado("dudh-12", "ataques à sua honra e reputação")}; o vídeo circula.'),
     ('O lado do Tomás', f'{M.citado("crp-32-2", "Todo o arguido se presume inocente")}, e ninguém o ouviu: tem '
                         f'{M.citado("crp-32-10", "os direitos de audiência e defesa")}.'),
     ('Uma objeção', 'Nove votos contam posições. Quem viu criar a conta?')],
     {'O que se faz': 'Decides outra vez e dizes o que pesou.',
      'Quanto tempo': 'Três minutos; em turma, até treze.',
      'O que fica escrito': 'Nada em papel; a escolha fica nos artefactos.',
      'Se estás sozinho': 'Compara com a escolha do início e abre os três lados.'},
     prova=('O que pesou mais, para ti?', ('A captura com o nome', 'O Tomás não ter sido ouvido', 'O que a Sara está a passar')),
     prova_rot='O que pesou mais', intro='', nota=None),
 M.fazer('emparelhar', 'Facto, regra ou razão',
         'Liga cada frase ao que ela é numa justificação.',
         'Facto, regra ou razão de uma das partes: o que é cada frase?',
         'Que uma conta com o nome do Tomás publicou o vídeo é um facto do caso; a presunção de inocência é uma regra da Constituição; '
         '«Somos nove a dizer que foi ele» é a razão de uma das partes, ainda por pesar.',
         3, 'distinguir', 'relato e princípio',
         pares=[['Uma conta com o nome do Tomás publicou o vídeo.', 'Um facto do caso'],
                ['«Todo o arguido se presume inocente […]»', 'Uma regra escrita num texto legal'],
                ['«Somos nove a dizer que foi ele.»', 'A razão de uma das partes']],
         citacoes=[('crp-32-2', 'Todo o arguido se presume inocente')],
         fe='A confusão mais provável é tomar a razão dos nove por facto: diz quantos pensam assim, não o que aconteceu. Volta ao caso e '
            'separa o que se viu do que alguém afirma.',
         pista='Pergunta a cada frase de onde vem: do caso, de uma lei ou de alguém?'),
 # O passo em falta (sessões 04 a 07): aqui, a fonte. Não diz a conclusão da charneira 2 (o vídeo e a autoria).
 escolha('A fonte que falta',
         'Facto: a direção vai decidir se castiga o Tomás. Aplicação: antes, tem de o ouvir. Limite: ouvi-lo não prova que diz a '
         'verdade. Falta a fonte: onde se apoia?',
         'Facto, aplicação e limite já estão: a direção vai decidir, tem de o ouvir, ouvi-lo não prova nada. Falta a fonte. Escolhe-a.',
         'Quem pode ser castigado tem direito a ser ouvido e a defender-se.',
         [('Toda a pessoa tem direito a exprimir livremente a sua opinião.',
           'Exprimir a opinião é outro direito, o da sessão 01: não obriga ninguém a ouvir o Tomás antes de o castigar. Procura o texto que '
           'fala de quem pode ser castigado.'),
          ('Ninguém pode sofrer ataques à sua honra e à sua reputação.',
           'A honra e a reputação protegem a Sara, que foi gozada no vídeo; não dizem o que a direção deve fazer antes de castigar. Procura '
           'o texto que fala de quem pode ser castigado.')],
         'A aplicação apoia-se no artigo 32.º, n.º 10: em «quaisquer processos sancionatórios», o arguido tem «os direitos de audiência e '
         'defesa». Com a fonte, a cadeia fica completa: facto, fonte, aplicação, limite.',
         4, 'aplicar', 'facto, fonte, aplicação, limite',
         citacoes=[('crp-32-10', 'quaisquer processos sancionatórios'), ('crp-32-10', 'os direitos de audiência e defesa')],
         pista='Procura, entre os textos que leste, o que fala do que vem antes de um castigo.'),
 # Charneira 2: a conclusão que não vai além das provas; os dois erros esperados vão além delas, cada um para seu lado.
 escolha('O que as provas permitem',
         'Escolhe a conclusão que fica dentro do que o caso e os textos mostram.',
         'Das três conclusões, escolhe a que diz o que as provas permitem, sem ir além delas.',
         'O vídeo deve sair já; quem o fez ainda está por provar.',
         [('Foi o Tomás: a captura e os nove votos chegam para isso.',
           'A captura mostra uma conta com o nome dele, e os nove votos contam opiniões: nada disto mostra quem a criou. Separa o que se viu '
           'do que alguém concluiu.'),
          ('Não foi o Tomás: ninguém o viu criar aquela conta.',
           'Também vai além das provas, no outro sentido: não se ter visto não prova que não foi ele. Por agora, sabe-se só que a autoria '
           'está por provar. Separa o que se sabe do que falta saber.')],
         'Diz o que as provas permitem: o vídeo magoa a Sara e pode sair já; quem o fez está por provar, e até lá o Tomás presume-se '
         'inocente e tem de ser ouvido.',
         3, 'aplicar', 'conclusão e provas', pista='Para cada conclusão, procura a prova que a sustenta.'),
 M.papel(PERGUNTA,
         ['A tua conclusão, por agora.',
          'Uma prova: um facto do caso e uma expressão exata, entre aspas, com o artigo.',
          'Uma dúvida que ainda tens.'],
         ['A conclusão responde à pergunta sem ir além das provas.',
          'A prova junta um facto a uma expressão exata, com o artigo.',
          'A dúvida, respondida, podia mudar a conclusão.'],
         '<p>Outro caso, inventado: a câmara do bar filma o Luís a guardar uma carteira do balcão.</p><ol>'
         '<li>Conclusão: a prova é forte, mas falta ouvir o Luís.</li>'
         f'<li>Prova: o vídeo mostra-o com a carteira; e o arguido tem '
         f'{M.citado("crp-32-10", "os direitos de audiência e defesa")} (artigo 32.º, n.º 10).</li>'
         '<li>Dúvida: a carteira era de quem?</li></ol>',
         'Num papel pequeno, sozinho e sem telemóvel.',
         relogio_min=12),
 M.levar(FRASE, ['«Não culpado» quer dizer que a culpa não ficou provada.',
                 'Votar conta posições; deliberar pesa razões.']),
]

# o lugar da certa em cada escolha (0, 1 ou 2), com a semente do motor: nunca o mesmo em mais de metade, nem três seguidos
LUGARES = (1, 0, 2, 1, 0)

# O passo do projeto (plano, secção 3: «o dossiê, com cada “por isso” marcado»). O dossiê é o da página do projeto
# (cidadania/projeto/, «Dossiê de investigação»).
DEPOIS = ('<article class="c"><p class="rot">O passo do teu projeto</p><p class="tit">Cada «por isso» do teu dossiê</p>'
          '<p class="sub">No teatro-documento, cada fala apoia-se numa fonte. Relê, em papel, as notas e o guião do teu dossiê e sublinha '
          'cada «por isso», «logo» e «então». Ao lado de cada um, escreve a prova em que se apoia. O que conta: cada conclusão tem uma '
          'prova; o que é suposição fica marcado como pergunta; nenhuma fala acusa uma pessoa real sem prova.</p>'
          '<p class="ir"><a href="../../../projeto/#av-dossie">O dossiê, no enunciado da Pergunta Humana</a></p></article>')


def sessao():
    d = {
        'id': 'cidadania-m1-s07', 'chave': 'epi-cid-m1-s07', 'versao': '2026-11-06-molde', 'marca': 'CD', 'molde': L.MOLDE,
        'titulo': 'Sessão 07: Nove contra dois', 'h1': 'Cidadania, módulo 1, sessão 07: Nove contra dois',
        'modulo': {'n': 1, 'nome': 'Humanos', 'url': L.LENTE + 'cidadania/piloto/m1/'},
        'saida': 'cidadania/m1/sessoes/07/index.html',
        'seguinte': '../../../piloto/m1-s08/', 'seguinteRotulo': 'Sessão 08: Quem decide o quê?',
        'fontes': M.ref('Constituição da República Portuguesa, artigo 32.º, n.os 2 e 10, na versão consolidada do Diário da República. '
                        'Declaração Universal dos Direitos Humanos, artigos 10.º, 11.º e 12.º, na transcrição do UNRIC. Convenção sobre os '
                        'Direitos da Criança, artigo 12.º, n.º 2, na tradução portuguesa anexa à Resolução da Assembleia da República '
                        'n.º 20/90, no Diário da República. Acórdão do Tribunal da Relação de Évora de 10 de outubro de 2023, processo '
                        '320/20.8GBSSB.E1, no dgsi.pt. Litografia: Honoré Daumier, prancha 21 de _Les Gens de Justice_, 1846, The '
                        'Metropolitan Museum of Art, domínio público (imagem CC0); a legenda é tradução nossa. _Doze Homens em Fúria_, filme '
                        'de Sidney Lumet (1957), no registo da Library of Congress. O caso do Tomás, o das nove partilhas, o da parede '
                        'riscada, o do castigo revisto noutra escola e o do bar são inventados; o da Relação de Évora é real.'),
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
