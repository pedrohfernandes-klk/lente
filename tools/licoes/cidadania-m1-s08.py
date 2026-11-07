# Fonte da sessão 08 do M1 de Cidadania, «Quem decide o quê?», na versão final do molde cidadania-2026-11 (plano do molde, secção 3,
# linha «08»; decisões 144 a 146, 152 a 155, 161 e 166 a 168). 06/11/2026: substitui a fonte do piloto de 31/10, que escrevia
# cidadania/piloto/m1-s08/ (essa página fica como está até ao pedido 3, que faz os redirecionamentos do piloto de uma vez); a chave
# epi-cid-m1-s08 é a mesma, e a versão sobe com preservarAnterior (cfg da família). Corre-se para escrever o .json ao lado; o .json
# é que o gerador (tools/licoes_lente.py) lê, e nunca se edita à mão. Os cartões montam-se com o ajudante comum
# tools/cidadania_molde.py; cada excerto vem do registo tools/cidadania_fontes.json (texto exato da fonte oficial, aberta a
# 6/11/2026, confirmado) e o ajudante recusa escrever um excerto que lá não esteja.
#
# 23 cartões (9 de ler, 14 de fazer), pela ordem e com os tempos da secção 2 do plano, como a s01 a s03; a ordem é fixa (cfg.aula) e a
# resposta certa de cada escolha fica no lugar pedido em LUGARES, calculado com a semente do motor. Cada exercício tem a sua pista,
# que não dá a resposta. O que só o docente faz vive no guia (tools/cidadania_piloto.py, GUIA['08']), nunca aqui. Na cadeia (cartões
# 19 a 21), o apoio retira-se como o plano pede para as sessões 08 a 10: a charneira 2 pede a conclusão que vai além das provas.
#
# Fontes abertas a 6/11/2026, uma de cada vez (nada citado de memória):
# - Constituição, artigos 23.º, 52.º, 161.º (proémio e alínea c)), 182.º e 202.º, versão consolidada no Diário da República
#   Eletrónico (registo crp-23-1, crp-52-1, crp-161, crp-161-c, crp-182, crp-202-1); a grafia é a da fonte («colectivamente»,
#   «respectiva», «acções»);
# - Lei n.º 43/90 (exercício do direito de petição), artigos 2.º, n.º 3, 8.º, n.º 1, e 9.º, n.º 5, alínea b), versão consolidada no
#   Diário da República Eletrónico (https://diariodarepublica.pt/dr/legislacao-consolidada/lei/1990-73102175; registo lei43-2-3,
#   lei43-8-1, lei43-9-5, lei43-9-5b);
# - O caso real (decisão 161): Provedor de Justiça, boletim informativo de novembro e dezembro de 2016, «Plano Diretor Municipal de
#   Lisboa – Recomendação n.º 5/A/2016» (PDF no sítio do Provedor, registo prov-2016-pdm). O cartão 12 conta só o que o boletim diz
#   (uma queixa, ilegalidade em normas do plano, uma recomendação ao presidente da câmara); o que a câmara fez depois não se sabe e não
#   se diz;
# - Fotografia: William Edward Kilburn, _View of the Great Chartist Meeting on Kennington Common_, 1848, daguerreótipo, Royal
#   Collection, RCIN 2932484. O ficheiro img/cidadania/kilburn-cartistas-1848.webp (640 × 456) é o do piloto, a versão do Wikimedia
#   Commons (registo aberto a 6/11/2026: autor William Edward Kilburn, 1818 a 1891; data 1848; daguerreótipo, 107 × 147 mm; Royal
#   Collection, RCIN 2932484; domínio público, autor morto em 1891, PD-Art). O registo da Royal Collection (rct.uk) não abriu nesta
#   passagem (desafio a robôs, que não se contornou): por isso, como o plano manda, a legenda não liga o comício à petição cartista;
# - Vídeo (decisão 155): nenhum. O plano não propõe candidato, e o vídeo do piloto (TED-Ed, sistemas de voto) sai com o método de Hondt.
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

IMG = '../../../../img/cidadania/kilburn-cartistas-1848.webp'
ALT = ('Fotografia antiga de uma multidão enorme de homens de chapéu num campo aberto. Ao centro, um palanque com bandeiras; à frente, '
       'uma carroça e um cavalo; ao fundo, uma chaminé alta e edifícios.')
ALT_VER = 'A mesma fotografia: uma multidão de chapéu num campo, à volta de um palanque com bandeiras; ao fundo, uma chaminé.'
VER = f'<img src="{IMG}" alt="{ALT_VER}">'
COMMONS = ('https://commons.wikimedia.org/wiki/File:William_Edward_Kilburn_-_View_of_the_Great_Chartist_Meeting_on_Kennington_Common_'
           '-_Google_Art_Project.jpg')
DRE_CRP = 'https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-aprovacao-constituicao/1976-34520775'
DRE_L43 = 'https://diariodarepublica.pt/dr/legislacao-consolidada/lei/1990-73102175'
PROVEDOR = 'https://provedor-jus.pt/documentos/Boletim_informativo_Novembro_Dezembro_2016.pdf'
CREDITO = ('William Edward Kilburn, <i>View of the Great Chartist Meeting on Kennington Common</i>, 1848, daguerreótipo. Royal Collection '
           f'(RCIN 2932484). <a href="{COMMONS}">Registo no Wikimedia Commons</a>. Domínio público.')
PERGUNTA = 'A quem se pede, e com que fundamento?'
DECIDE_Q = 'A turma deve fazer um pedido escrito, com assinaturas, contra a mudança?'
FRASE = 'Pede-se a quem decidiu, com factos que se podem confirmar.'
ART52 = M.registo()['crp-52-1']['texto']


def escolha(rot, p, p2, certa, erradas, f, minutos, tipo, conceito, **extra):
    """Uma escolha de três opções; a certa vai para o lugar de LUGARES (preenchido em sessao())."""
    c = M.fazer('escolha', rot, p, p2, f, minutos, tipo, conceito, **extra)
    c['_certa'], c['_erradas'] = M.ref(certa), [(M.ref(o), M.ref(e)) for o, e in erradas]
    return c


def palavras(frase, alvo):
    """Os índices das palavras de «alvo» na frase do sublinhar (sem a pontuação colada)."""
    w = [x.strip('.,;:') for x in frase.split()]
    return [w.index(a) for a in alvo]


R1_FRASE = 'Às 8h15 atravessam ali muitos alunos e o semáforo fica a duzentos metros, por isso a passadeira deve ficar.'

CARTOES = [
 # ---------------------------------------------------------------- parte 1, ver antes de concluir (60 minutos)
 # O caso da passadeira vem do piloto (s08, cartão 1), reescrito: o aviso é assinado pela câmara (o destinatário prova-se no caso) e a
 # junta, ao lado da escola, fica como tentação; a razão da câmara e a contagem dos alunos ficam para a Volta ao caso.
 M.abre('Quem decide o quê?',
        f'ver e ler (60{NB}min), pausa (10{NB}min), pesar e escrever (50{NB}min) e o teu projeto (45{NB}min).',
        'A passadeira em frente ao portão da escola vai desaparecer: passa a haver só um semáforo na esquina, a duzentos metros. A '
        'turma soube por um aviso afixado na paragem, assinado pela câmara municipal. Há quem queira juntar assinaturas, quem prefira '
        'falar com a junta de freguesia, ao lado da escola, e quem ache que reclamar não serve de nada.',
        PERGUNTA),
 M.decide(DECIDE_Q, [
     ('Quem acha que sim', 'Um pedido escrito fica registado, e quem o recebe tem de o examinar. Com muitos nomes, mostra que não é a '
                           'vontade de um só.'),
     ('Quem acha que não', 'O aviso já está afixado: a decisão está tomada. Um papel com nomes não muda uma obra marcada.'),
     ('Uma objeção', 'Sabem a quem escrever? E o que vão pedir: a passadeira de volta, ou outra travessia segura?')]),
 # R1 (sem obra; plano: «onde começa a conclusão numa frase sobre a passadeira com “por isso”»): a marca da conclusão da sessão 07.
 M.recupera(M.fazer(
     'sublinhar', 'Onde começa a conclusão',
     'Nesta frase sobre a passadeira, sublinha as duas palavras que anunciam a conclusão.',
     'Que duas palavras, nesta frase, mostram que o que vem a seguir é a conclusão? Sublinha-as.',
     'Antes de «por isso» estão as razões (quantos atravessam, a distância do semáforo); depois vem a conclusão: a passadeira deve '
     'ficar. É a marca que procuraste na sessão 07.',
     3, 'reconhecer', 'prova e conclusão', frase=R1_FRASE, certas=palavras(R1_FRASE, ['por', 'isso']),
     fe='A confusão mais provável é sublinhar uma das razões, como «duzentos metros». As razões vêm primeiro; procura as duas palavras '
        'que fazem a passagem para o que se pede.',
     pista='Procura onde a frase passa do que se vê ao que se pede.')),
 # R2: um item novo da finalidade (sessão 05): contar sem identificar. «finalidade» está na s05 do piloto e na do molde.
 M.recupera(escolha(
     'O registo da contagem',
     'Para mostrar que muita gente atravessa no portão, a turma vai registar quem passa entre as 8h e as 8h30. O que precisa de anotar?',
     'A turma quer provar que a passagem do portão é muito usada de manhã. Que registo basta para isso?',
     'Quantas pessoas passam e a que horas.',
     [('O nome e a turma de cada aluno que passa.',
       'Para contar, não precisas de saber quem é quem. Na sessão 05, viste que os dados servem a «finalidade» para que se recolhem: '
       'aqui, mostrar quantos passam. Volta ao que a turma quer provar.'),
      ('Uma fotografia de cada pessoa que atravessa.',
       'Uma fotografia identifica as pessoas e não acrescenta nada à contagem. A «finalidade» é mostrar quantos passam, e a que horas. '
       'Volta ao que a turma quer provar.')],
     'A «finalidade» é mostrar quantos atravessam e quando: basta um traço por pessoa e a hora. Nomes e fotografias são dados a mais, '
     'como viste na sessão 05.',
     4, 'aplicar', 'finalidade', pista='Pergunta-te o que a turma quer provar, e o que basta para isso.'),
     origem='cidadania/m1/sessoes/05/'),
 M.olha('Uma multidão em 1848', 'Olha primeiro; só depois lê a legenda.',
        M.figura(IMG, ALT, CREDITO, 'Kennington Common, Londres, 1848: um comício do movimento cartista.',
                 artefacto='Uma multidão num comício, Londres, 1848', largura=640, altura=456)),
 # O que a fotografia mostra (uma multidão): erros de observação reais (a chaminé ao fundo, o palanque tomado por palco). O retorno não
 # fala do pedido, que é o cartão seguinte.
 escolha('O que se vê',
         'Sem ler a legenda: o que mostra a fotografia?',
         'Olha só para a imagem. O que se vê nela?',
         'Uma multidão de chapéu à volta de um palanque.',
         [('Uma fila de pessoas à porta de uma fábrica.',
           'Ao fundo há uma chaminé e edifícios, mas ninguém está em fila nem à porta: a multidão enche o campo e vira-se para o centro. '
           'Volta à imagem e procura para onde olham.'),
          ('Um público sentado a ver uma peça de teatro.',
           'O palanque pode lembrar um palco, mas ninguém está sentado: a multidão está de pé, num campo aberto. Volta à imagem e olha '
           'para a frente.')],
         'Vê-se uma multidão de pé, quase toda de chapéu, num campo aberto, virada para um palanque com bandeiras. Ao fundo, uma chaminé '
         'alta e edifícios.',
         3, 'reconhecer', 'observação', ver=VER, pista='Olha para onde se vira a maior parte das pessoas.'),
 # O que a fotografia não mostra (o pedido): a força do número não diz o destinatário nem o pedido.
 M.fazer('vf', 'Imagem e legenda',
         'Pela fotografia e pela legenda, sabes a quem se dirigia aquela multidão e o que pedia.',
         'A imagem e a legenda dizem o que aquela multidão queria e a quem o queria pedir.',
         'É falso: a fotografia mostra quantos eram, e a legenda diz o lugar, o ano e que era um comício cartista. Nenhuma das duas diz o '
         'que pediam, nem a quem. Para isso, era preciso ler o próprio pedido.',
         3, 'distinguir', 'número e pedido', v=False, ver=VER,
         fe='Uma multidão mostra força, não um pedido. A legenda diz o lugar, o ano e o movimento; não diz o que se pedia, nem a quem. '
            'Volta à legenda e procura um destinatário.',
         pista='Separa o que vês e lês do que precisarias de saber.'),
 M.le('Pedir é um direito', 'A quem se pede?',
      [(f'Artigo{NB}52.º', 'Todos os cidadãos têm o direito de apresentar […] aos órgãos de soberania […] ou a quaisquer autoridades '
                          'petições […] para defesa dos seus direitos, da Constituição, das leis ou do interesse geral […]', 'crp-52-1', 'a52'),
       (f'Artigo{NB}23.º', 'Os cidadãos podem apresentar queixas […] ao Provedor de Justiça, que as apreciará sem poder decisório, '
                          'dirigindo aos órgãos competentes as recomendações necessárias […]', 'crp-23-1', 'a23')],
      f'<a href="{DRE_CRP}">Constituição, artigos 52.º e 23.º</a>',
      mais=(M.lei([('Lei n.º 43/90, artigo 2.º, n.º 3', 'Entende-se por reclamação a impugnação de um acto perante o órgão, funcionário '
                    'ou agente que o praticou ou perante o seu superior hierárquico.', 'lei43-2-3', None),
                   ('Lei n.º 43/90, artigo 8.º, n.º 1', 'O exercício do direito de petição obriga a entidade destinatária a receber e '
                    'examinar […] bem como a comunicar as decisões que forem tomadas.', 'lei43-8-1', None)]))),
 # Leitura exata: em defesa de quê se pode pedir (o fundamento, que o Conceito vai nomear).
 M.fazer('sublinhar', 'Em defesa de quê',
         'No artigo 52.º, n.º 1, sublinha as palavras que dizem em defesa de quê se pode pedir.',
         'Segundo o n.º 1 do artigo 52.º, um pedido pode defender o quê? Sublinha essas palavras.',
         'Pede-se «para defesa dos seus direitos, da Constituição, das leis ou do interesse geral». É daí que um pedido tira o '
         'fundamento: não basta querer.',
         3, 'reconhecer', 'direito de petição', frase=ART52,
         certas=palavras(ART52, ['direitos', 'Constituição', 'leis', 'interesse', 'geral']), fonte='crp-52-1', l='a52',
         citacoes=[('crp-52-1', 'para defesa dos seus direitos, da Constituição, das leis ou do interesse geral'),
                   ('crp-52-1', 'órgãos de soberania'), ('crp-52-1', 'autoridades'), ('crp-52-1', 'petições'), ('crp-52-1', 'queixas'),
                   ('crp-52-1', 'para defesa')],
         fe='A confusão mais provável é sublinhar a quem se pede («órgãos de soberania», «autoridades») ou as formas do pedido '
            '(«petições», «queixas»). Procura o que vem logo depois de «para defesa».',
         pista='Separa a quem se pede, como se pede e o que se defende.'),
 # Órgãos e funções (piloto, cartão 3), agora depois do material: o texto da Constituição vai no próprio cartão. 06/11/2026 (revisão):
 # os três artigos são itens paralelos (decisão 152) e vão um em cada par, com a sua referência, em vez de fundidos numa só citação.
 M.fazer('emparelhar', 'Quem faz o quê',
         'Situações novas: segundo a Constituição, a que órgão cabe cada uma?',
         'Liga cada situação ao órgão que a Constituição encarrega disso.',
         'A Assembleia faz leis, o Governo conduz a política geral do país e os tribunais administram a justiça. Relê o verbo de cada '
         'artigo.',
         4, 'aplicar', 'órgãos de soberania',
         pares=[['Aprovar uma lei nova sobre o direito de petição',
                 f'Artigo{NB}161.º, alínea c): à Assembleia da República compete «Fazer leis sobre todas as matérias»'],
                ['Definir a política de transportes para todo o país',
                 f'Artigo{NB}182.º: o Governo é o «órgão de condução da política geral do país»'],
                ['Decidir, num processo, quem tem razão num conflito',
                 f'Artigo{NB}202.º, n.º{NB}1: os tribunais têm competência para «administrar a justiça em nome do povo»']],
         citacoes=[('crp-182', 'a política geral do país'), ('crp-161-c', 'Fazer leis sobre todas as matérias'),
                   ('crp-182', 'órgão de condução da política geral do país'),
                   ('crp-202-1', 'administrar a justiça em nome do povo')],
         fe='A confusão mais provável é trocar a Assembleia e o Governo. O Governo conduz «a política geral do país»; a Assembleia pode '
            '«Fazer leis sobre todas as matérias», salvo as que a Constituição reserva ao Governo. Relê cada artigo e procura o verbo.',
         pista='Para cada situação, procura o verbo que lhe corresponde nos artigos.'),
 # A junta ou a câmara (plano): o destinatário prova-se no caso (o aviso é da câmara); o artigo 52.º deixa pedir a «quaisquer
 # autoridades», mas quem pode rever a decisão é quem a tomou (Lei n.º 43/90, artigo 2.º, n.º 3, no «Ler mais»).
 escolha('A junta ou a câmara',
         'A junta de freguesia fica ao lado da escola, e a turma pensa escrever-lhe sobre a passadeira. É o melhor destinatário?',
         'Escrever à junta de freguesia, que fica ao lado da escola, é a melhor maneira de pedir a passadeira de volta?',
         'Não: o pedido deve ir a quem decidiu, a câmara.',
         [('Sim: a junta é a autoridade mais perto da rua.',
           'Perto não quer dizer que decida. O aviso da mudança é da câmara, e uma reclamação faz-se perante quem praticou o ato. Volta ao '
           'caso: quem assinou o aviso?'),
          ('Não: o pedido deve ir à Assembleia da República.',
           'A Assembleia faz leis para o país; a passadeira é uma decisão sobre uma rua, e o aviso é da câmara. Volta ao caso e ao aviso.')],
         'O artigo 52.º deixa pedir a «quaisquer autoridades», mas uma reclamação faz-se «perante o órgão, funcionário ou agente que o '
         'praticou» (Lei n.º 43/90), e o aviso da mudança é da câmara.',
         3, 'aplicar', 'destinatário',
         citacoes=[('crp-52-1', 'quaisquer autoridades'), ('lei43-2-3', 'perante o órgão, funcionário ou agente que o praticou')],
         pista='Volta ao caso: o que diz o aviso, além da mudança?'),
 # Charneira 1 e caso real (decisão 161): o Provedor recomenda, não decide (piloto, cartões 7 e 16, agora uma vez só), num caso
 # contado com as palavras do boletim do Provedor de Justiça (registo prov-2016-pdm).
 M.fazer('vf', 'Uma queixa ao Provedor',
         'Caso real (Provedor de Justiça, Lisboa, 2016): após uma queixa, o Provedor detetou ilegalidade em normas do plano municipal e '
         'fez uma recomendação ao presidente da câmara. A recomendação anulou-as.',
         'Em 2016, depois de uma queixa, o Provedor de Justiça detetou ilegalidade em normas do plano municipal de Lisboa e fez uma '
         'recomendação ao presidente da câmara. Essa recomendação anulou as normas.',
         'É falso: o Provedor aprecia as queixas «sem poder decisório» e dirige «aos órgãos competentes as recomendações necessárias» '
         '(artigo 23.º). A recomendação pesa, mas quem decide são os órgãos competentes.',
         4, 'transferir', 'recomendar e decidir', v=False,
         citacoes=[('crp-23-1', 'sem poder decisório'), ('crp-23-1', 'aos órgãos competentes as recomendações necessárias')],
         fe='Recomendar não é decidir. O Provedor aprecia as queixas «sem poder decisório» (artigo 23.º): aponta o problema aos órgãos '
            'competentes, e são eles que decidem. Volta ao artigo 23.º.',
         liga=[{'t': 'Ler o boletim do Provedor de Justiça, novembro e dezembro de 2016 (PDF)', 'href': PROVEDOR}],
         pista='Relê o artigo 23.º: o que faz o Provedor com uma queixa?'),
 # Conceito (uma vez): destinatário, pedido, fundamento verificável. Os três itens paralelos vão em tabela (decisão 152).
 M.conceito('A quem, o quê, porquê',
            '<p>A turma quer a passadeira de volta. Basta dizê-lo?</p>',
            '<table class="tabela"><thead><tr><th scope="col">Parte</th><th scope="col">Pergunta</th><th scope="col">No caso</th></tr>'
            '</thead><tbody>'
            '<tr><td data-th="Parte">destinatário</td><td data-th="Pergunta">a quem?</td><td data-th="No caso">quem assinou o aviso</td></tr>'
            '<tr><td data-th="Parte">pedido</td><td data-th="Pergunta">o quê?</td><td data-th="No caso">uma medida concreta</td></tr>'
            '<tr><td data-th="Parte">fundamento</td><td data-th="Pergunta">porquê?</td><td data-th="No caso">um facto que se confirma e o artigo</td></tr>'
            '</tbody></table>',
            'Pedido fundamentado', 'Um pedido a quem pode decidir, que diz o que se quer e porquê, com factos que se confirmam.',
            '<p>Não é juntar assinaturas: o número dá força, não fundamento.</p>',
            mais=(f'<p>Se o escrito não diz o que se pede, a <a href="{DRE_L43}">Lei n.º 43/90</a> (artigo 9.º, n.º 5) manda: '
                  f'{M.citado("lei43-9-5", "A entidade destinatária convida o peticionário a completar o escrito apresentado")} quando '
                  f'{M.citado("lei43-9-5b", "não especifique o objecto de petição")}.</p>')),
 # Transferir 1: um pedido novo, à diretora, sobre o bar; o aluno reconhece as partes do pedido fora do caso da passadeira.
 M.fazer('emparelhar', 'As partes de um pedido',
         'Caso inventado: um pedido à diretora sobre o horário do bar. Liga cada parte ao papel que tem no pedido.',
         'Neste pedido sobre o horário do bar, que papel tem cada parte?',
         'A diretora é a quem se dirige; abrir às 8h é a medida; o horário das aulas e do bar é o facto que o apoia; o '
         'artigo 52.º é a norma invocada. Sem destinatário ou sem pedido, ninguém sabe o que decidir.',
         3, 'transferir', 'pedido fundamentado',
         pares=[['À diretora da escola,', 'A quem se dirige'],
                ['solicitamos que o bar abra às 8h, e não às 8h30,', 'A medida que se quer'],
                ['porque há aulas às 8h15 e o bar só abre às 8h30,', 'O facto que o apoia'],
                ['ao abrigo do artigo 52.º da Constituição.', 'A norma invocada']],
         fe='A confusão mais provável é tomar o horário pela medida que se quer. O que se quer é que o bar abra às 8h; o horário das '
            'aulas e do bar é o facto que o apoia. Relê o pedido parte a parte.',
         pista='Lê cada parte e pergunta: diz a quem, o quê ou porquê?'),
 # Transferir 2 (conceito espaçado, sessão 04: o facto que se pode verificar, separado da opinião e da previsão). Plano: «Contámos
 # 140 alunos às 8h15» (piloto, cartão 19), num caso novo; sem absolutos nos distratores.
 escolha('Um fundamento que se confirma',
         'Caso inventado: a turma pede mais um autocarro às 17h40. Que frase dá ao pedido um fundamento que se pode confirmar?',
         'Num pedido de mais um autocarro às 17h40, que frase traz um fundamento que quem recebe o pedido pode conferir?',
         'Na terça, 38 alunos ficaram à espera desse autocarro.',
         [('Os alunos acham que um autocarro às 17h40 é pouco.',
           'É uma opinião: diz o que os alunos pensam, e ninguém a pode conferir. Na sessão 04, separaste factos de opiniões. Procura a '
           'frase que quem recebe o pedido pode confirmar.'),
          ('Sem outro autocarro, vai haver alunos a faltar.',
           'É uma previsão: diz o que pode vir a acontecer, não o que aconteceu. Procura o que já aconteceu e se pode contar.')],
         'Uma contagem com dia e número é um facto: quem recebe o pedido pode confirmá-la. A opinião e a previsão podem acompanhar o '
         'pedido, mas não o fundamentam.',
         4, 'transferir', 'fundamento verificável', origem='cidadania/m1/sessoes/04/',
         pista='Pergunta a cada frase: alguém a pode ir confirmar?'),
 # ---------------------------------------------------------------- parte 2, pesar e escrever (50 minutos)
 # Volta ao caso: duas razões que chocam (a segurança que a câmara invoca e o uso real da passagem).
 M.volta('A razão da câmara',
         'Em letra pequena, o aviso dá a razão: quem sai da rotunda não vê quem atravessa junto ao portão, e o semáforo da esquina é mais '
         'seguro. A turma contou, numa manhã: entre as 8h e as 8h30, 140 alunos atravessaram ali. Um vizinho avisa: «Ninguém vai andar '
         'duzentos metros para trás.»',
         carimbo='Caso inventado.'),
 M.fazer('emparelhar', 'O que se sabe e o que falta',
         'Depois da razão da câmara e da contagem: o que já está no caso e o que ainda falta saber?',
         'Em cada linha: está no caso ou ainda falta saber?',
         'Sabes quem decidiu e quantos atravessaram numa manhã. Não sabes se o semáforo é mesmo mais seguro, nem quantos vão até lá. '
         'São dúvidas para o papel.',
         3, 'aplicar', 'facto e dúvida',
         pares=[['Quem decidiu tirar a passadeira', 'Já está no caso'],
                ['Quantos atravessaram numa manhã', 'Já está no caso'],
                ['Se o semáforo é mais seguro do que a passadeira', 'Ainda está em aberto'],
                ['Quantos alunos vão mesmo até ao semáforo', 'Ainda está em aberto']],
         fe='A confusão mais provável é dar por provado que o semáforo é mais seguro, porque o aviso o diz: é a razão da câmara, que ainda '
            'se pode pôr à prova. Separa o que está no caso do que alguém afirma.',
         pista='Procura cada informação no caso e vê quem a afirma.'),
 M.em_turma(DECIDE_Q, [
     ('Quem acha que sim', f'Pode pedir-se a {M.citado("crp-52-1", "quaisquer autoridades")}, e a contagem é um facto que a câmara '
                           'pode confirmar.'),
     ('Quem acha que não', 'A câmara deu uma razão de segurança. Um pedido só pesa se responder a essa razão.'),
     ('Uma objeção', 'E se o pedido for outra travessia segura, com a contagem como prova?')],
     {'O que se faz': 'Decides outra vez e escolhes a prova que mais pesa.',
      'Quanto tempo': 'Três minutos; em turma, até treze.',
      'O que fica escrito': 'Nada em papel; a escolha fica nos artefactos.',
      'Se estás sozinho': 'Compara com a escolha do início e abre os três lados.'},
     prova=('Que prova pesa mais?', ('A contagem da manhã', 'O aviso da câmara', 'O artigo 52.º')),
     intro='', nota=None),
 M.fazer('emparelhar', 'Facto, regra ou razão',
         'Liga cada frase ao que ela é numa justificação.',
         'Facto, regra ou razão de uma das partes: o que é cada frase?',
         'Que o aviso é da câmara é um facto do caso; o direito de ser informado está no artigo 52.º; «Ninguém vai andar duzentos metros '
         'para trás» é a razão de um vizinho, que ainda tem de ser pesada.',
         3, 'distinguir', 'relato e princípio',
         pares=[['O aviso da mudança é assinado pela câmara municipal.', 'Um facto do caso'],
                ['«[…] o direito de serem informados, em prazo razoável, sobre o resultado […]»', 'Uma regra escrita num texto legal'],
                ['«Ninguém vai andar duzentos metros para trás.»', 'A razão de uma das partes']],
         citacoes=[('crp-52-1', 'o direito de serem informados, em prazo razoável, sobre o resultado')],
         fe='A confusão mais provável é tomar a razão do vizinho por facto: diz o que ele prevê, e ninguém o contou. Volta ao caso e '
            'pergunta a cada frase de onde vem.',
         pista='Pergunta a cada frase de onde vem e quem a diz.'),
 M.fazer('ordenar', 'A justificação por ordem',
         'Põe a justificação por ordem, do que aconteceu ao que ainda falta saber.',
         'Ordena a justificação: começa no que se sabe e acaba no que ainda está por saber.',
         'Facto, fonte, aplicação, limite: cada passo apoia-se no anterior, e o limite diz até onde o pedido pode ir.',
         4, 'aplicar', 'facto, fonte, aplicação, limite',
         passos=['O aviso é da câmara, e numa manhã atravessaram ali 140 alunos.',
                 'A Constituição dá o direito de pedir a quaisquer autoridades, em defesa do interesse geral.',
                 'A turma pode pedir à câmara que reveja a decisão, com a contagem como prova.',
                 'Falta saber se o semáforo da esquina é mais seguro do que a passadeira.'],
         fe='A confusão mais provável é começar pelo artigo ou pôr o que falta saber antes do pedido. Começa no que aconteceu; o que '
            'falta saber fecha a justificação.',
         pista='Pergunta-te o que tem de vir primeiro para o resto se apoiar.'),
 # Charneira 2, no apoio que se retira (sessões 08 a 10): encontrar a conclusão que vai além das provas. O erro esperado é ficar
 # com uma das duas que as provas sustentam, por parecerem fracas.
 escolha('A conclusão que vai longe de mais',
         'Só uma destas conclusões vai além do que o caso e a contagem mostram. Encontra-a.',
         'Uma destas conclusões diz mais do que as provas permitem. Encontra-a.',
         'A câmara decidiu sem ouvir ninguém antes.',
         [('Numa manhã, muitos alunos atravessaram no portão.',
           'A contagem diz quantos atravessaram nessa manhã, e a conclusão não vai além disso. Procura a conclusão que afirma o que '
           'ninguém viu.'),
          ('A câmara deu uma razão de segurança para mudar.',
           'A razão de segurança está escrita no aviso: está provado que a câmara a deu. Procura a conclusão que afirma o que nenhum '
           'material mostra.')],
         'Que a turma soube por um aviso não prova que ninguém foi ouvido: pode ter havido consulta que a turma não viu. As outras duas '
         'dizem só o que a contagem e o aviso mostram.',
         3, 'aplicar', 'conclusão e provas', pista='Para cada conclusão, procura a prova que a sustenta.'),
 M.papel(PERGUNTA,
         ['A tua conclusão, por agora: a quem pedes e o quê.',
          'Uma prova: um facto do caso e uma expressão exata, entre aspas, com o artigo.',
          'Uma dúvida que ainda tens.'],
         ['A conclusão diz a quem se pede e o quê, sem ir além das provas.',
          'A prova junta um facto a uma expressão exata, com o artigo.',
          'A dúvida, respondida, podia mudar o pedido.'],
         '<p>Outro caso, inventado: o bebedouro do pavilhão está avariado desde outubro.</p><ol>'
         '<li>Conclusão: pede-se à direção que o mande reparar.</li>'
         f'<li>Prova: está avariado desde outubro; pede-se {M.citado("crp-52-1", "para defesa […] do interesse geral")} (artigo 52.º, '
         'n.º 1).</li>'
         '<li>Dúvida: a reparação cabe à escola ou a outra entidade?</li></ol>',
         'Num papel pequeno, sozinho e sem telemóvel.',
         relogio_min=12),
 M.levar(FRASE, ['O Provedor de Justiça recomenda; não decide.',
                 'Uma multidão mostra quantos são; o pedido diz o que querem.']),
]

# o lugar da certa em cada escolha (0, 1 ou 2), com a semente do motor: nunca o mesmo em mais de metade, nem três seguidos
LUGARES = (2, 0, 1, 2, 0)

# O passo do projeto (plano, secção 3: «guião, versão 1, com a fonte de cada fala»). O que se diz do guião é o que a página do projeto
# já diz (cidadania/projeto/, «As fases»: no guião, tornar localizáveis as fontes das falas).
DEPOIS = ('<article class="c"><p class="rot">O passo do teu projeto</p><p class="tit">O guião, versão 1</p>'
          '<p class="sub">Escreve, em papel, a primeira versão do guião do teu teatro-documento. Ao lado de cada fala, anota de onde vem: '
          'a entrevista, o documento ou a notícia, com o que é preciso para a reencontrar. O que conta: cada fala tem a sua fonte; '
          'nenhuma fala atribui a alguém o que essa pessoa não disse; o que é teu (a ordem, as ligações) distingue-se do que é citado.</p>'
          '<p class="ir"><a href="../../../projeto/#fases">As fases do teatro-documento, no enunciado da Pergunta Humana</a></p></article>')


def sessao():
    d = {
        'id': 'cidadania-m1-s08', 'chave': 'epi-cid-m1-s08', 'versao': '2026-11-06-molde', 'marca': 'CD', 'molde': L.MOLDE,
        'titulo': 'Sessão 08: Quem decide o quê?', 'h1': 'Cidadania, módulo 1, sessão 08: Quem decide o quê?',
        'modulo': {'n': 1, 'nome': 'Humanos', 'url': L.LENTE + 'cidadania/piloto/m1/'},
        'saida': 'cidadania/m1/sessoes/08/index.html',
        # 07/11/2026 (sessão 09 no molde): a seguinte passa a ser a s09 nova, no mesmo endereço das sessões (era a do piloto).
        'seguinte': '../09/', 'seguinteRotulo': 'Sessão 09: Muitas vozes, uma escola',
        'fontes': M.ref('Constituição da República Portuguesa, artigos 23.º, n.º 1, 52.º, n.º 1, 161.º, alínea c), 182.º e 202.º, n.º 1, na '
                        'versão consolidada do Diário da República. Lei n.º 43/90, de 10 de agosto (exercício do direito de petição), '
                        'artigos 2.º, n.º 3, 8.º, n.º 1, e 9.º, n.º 5, na versão consolidada do Diário da República. Provedor de Justiça, '
                        'boletim informativo de novembro e dezembro de 2016, «Plano Diretor Municipal de Lisboa – Recomendação n.º '
                        '5/A/2016». Fotografia: William Edward Kilburn, _View of the Great Chartist Meeting on Kennington Common_, 1848, '
                        'daguerreótipo, Royal Collection, domínio público. O caso da passadeira, o da contagem, o do bar, o do autocarro e '
                        'o do bebedouro são inventados; o do Provedor de Justiça é real.'),
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
