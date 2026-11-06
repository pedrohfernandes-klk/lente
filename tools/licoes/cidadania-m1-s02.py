# Fonte da sessão 02 do M1 de Cidadania, «A imagem dos outros», na versão final do molde cidadania-2026-11 (plano do molde,
# secção 3, linha «02»; decisões 144 a 146, 152 a 155, 161 e 166). 06/11/2026: substitui a fonte do piloto de 31/10, que escrevia
# cidadania/piloto/m1-s02/ (essa página fica como está até ao pedido 3, que faz os redirecionamentos do piloto de uma vez); a
# chave epi-cid-m1-s02 é a mesma, e a versão sobe com preservarAnterior (cfg da família). Corre-se para escrever o .json ao lado;
# o .json é que o gerador (tools/licoes_lente.py) lê, e nunca se edita à mão. Os cartões montam-se com o ajudante comum
# tools/cidadania_molde.py; cada excerto de lei ou de acórdão vem do registo tools/cidadania_fontes.json (texto exato da fonte
# oficial, aberta a 6/11/2026, confirmado) e o ajudante recusa escrever um excerto que lá não esteja.
#
# 23 cartões (9 de ler, 14 de fazer), pela ordem e com os tempos da secção 2 do plano, como a s01; a ordem é fixa (cfg.aula) e a
# resposta certa de cada escolha fica no lugar pedido em LUGARES, calculado com a semente do motor. Cada exercício tem a sua pista,
# que não dá a resposta. O que só o docente faz vive no guia (tools/cidadania_piloto.py, GUIA['02']), nunca aqui.
#
# Fontes abertas a 6/11/2026 (nada citado de memória):
# - Código Civil, artigos 79.º e 81.º, versão consolidada no Diário da República Eletrónico (registo cc-79-1 a cc-79-3, cc-81-2);
# - Lei n.º 58/2019, artigo 16.º, no Diário da República Eletrónico (registo lei58-16-1);
# - Acórdão do Supremo Tribunal de Justiça de 7/6/2011, processo 1581/07.3TVLSB.L1.S1, em dgsi.pt (registo stj-2011-*): o caso
#   real da sessão (decisão 161); 06/11/2026 (revisão): cita-se a conclusão do tribunal (stj-2011-indicacao), não o depoimento;
# - Fotografia: Library of Congress, registo https://www.loc.gov/item/2018675335/ (o endereço antigo ncl2004001725 leva lá):
#   «Addie Card, 12 years. Spinner in North Pormal [i.e., Pownal] Cotton Mill. Vt. […] Location: North Pownal, Vermont.»,
#   «1910 February», «Hine, Lewis Wickes, 1874-1940, photographer» («Attribution to Hine based on provenance»), «No known
#   restrictions on publication.», «Credit line: National Child Labor Committee collection, Library of Congress, Prints and
#   Photographs Division.». 06/11/2026 (revisão): o ficheiro img/cidadania/hine-addie-card-1910.webp (825 × 1024) passa a sair do
#   LC-DIG-nclc-05282 (ficheiro preto e branco do negativo de vidro, tile.loc.gov/…/nclc/05200/05282v.jpg), inteiro, sem filtro
#   nem corte; o do piloto era a impressão a cores (01830) dessaturada.
# - Vídeo (decisão 155): nenhum. O candidato do plano, «Be kind online: consent to share and cyberbullying», está no sítio
#   oficial (bullyingnoway.gov.au, © State of Queensland em nome das autoridades de educação australianas), mas trata de uma
#   imagem íntima partilhada sem consentimento e a equipa não o viu por inteiro; fica para o docente ver e decidir (guia).
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

IMG = '../../../../img/cidadania/hine-addie-card-1910.webp'
ALT = ('Uma rapariga descalça, de vestido e avental compridos e cabelo apanhado, está de pé diante de uma fila de máquinas de fiar '
       'cheias de bobinas, com um braço apoiado numa delas, e olha de frente para a câmara.')
ALT_VER = 'A mesma fotografia: a rapariga descalça, de pé diante das máquinas de fiar, olha de frente para a câmara.'
VER = f'<img src="{IMG}" alt="{ALT_VER}">'
LOC = 'https://www.loc.gov/item/2018675335/'
DRE_CC = 'https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/1966-34509075'
DRE_LEI = 'https://diariodarepublica.pt/dr/detalhe/lei/58-2019-123815982'
DGSI = 'https://www.dgsi.pt/jstj.nsf/954f0ce6ad9dd8b980256b5f003fa814/6190a514bc9d85cf802578aa003183d3?OpenDocument'
CREDITO = ('Lewis Hine (atribuição), <i>Addie Card, 12 years. Spinner in North Pormal [i.e., Pownal] Cotton Mill. Vt. […]</i>, 1910. '
           'National Child Labor Committee collection, Library of Congress, Prints and Photographs Division (LC-DIG-nclc-05282). '
           f'<a href="{LOC}">Registo de origem</a>. Domínio público (o registo diz «No known restrictions on publication»).')
PERGUNTA = 'Aceitar ser filmado é aceitar ser publicado?'
DECIDE_Q = 'O vídeo do ensaio pode ir para a página da escola?'
FRASE = 'Aceitar ser filmado não é aceitar ser publicado.'


def escolha(rot, p, p2, certa, erradas, f, minutos, tipo, conceito, **extra):
    """Uma escolha de três opções; a certa vai para o lugar de LUGARES (preenchido em sessao())."""
    c = M.fazer('escolha', rot, p, p2, f, minutos, tipo, conceito, **extra)
    c['_certa'], c['_erradas'] = M.ref(certa), [(M.ref(o), M.ref(e)) for o, e in erradas]
    return c


CARTOES = [
 # ---------------------------------------------------------------- parte 1, ver antes de concluir (60 minutos)
 # O caso da Marta vem do piloto (s02, cartão 1), reescrito: sem «grupo» (decisão 146) e sem a resposta no caso.
 M.abre('A imagem dos outros',
        f'ver e ler (60{NB}min), pausa (10{NB}min), pesar e escrever (50{NB}min) e o teu projeto (45{NB}min).',
        'Na quinta-feira, a turma ensaia uma peça. A Marta aceita que o Duarte filme a cena, para a turma a rever '
        'depois e corrigir o que falha. Aos 40 segundos, ela escorrega e cai. Ao ver o vídeo, os colegas riem-se: a cena ficou '
        'ótima. Querem publicá-la na página da escola.',
        PERGUNTA),
 M.decide(DECIDE_Q, [
     ('Quem acha que pode ir', 'A Marta aceitou ser filmada, e o vídeo mostra o trabalho da turma. A queda dura dois segundos.'),
     ('Quem acha que não', 'A Marta aceitou que a turma revisse a cena. A página da escola é vista por quem ela não conhece.'),
     ('Uma objeção', 'E se cortarem a queda? Fica resolvido, ou falta perguntar alguma coisa à Marta?')]),
 # R1: a obra do #84 s02 (The Truman Show), sem a citação do Código Civil no retorno (o Lê vem depois). Os factos são a premissa
 # do filme: Truman vive num cenário, a vida dele passa na televisão e todos à volta são atores, menos ele.
 M.recupera(escolha(
     'A quem pertence a imagem',
     'Em _The Truman Show_ (Peter Weir, 1998), a vida de Truman passa na televisão; todos à volta são atores, menos ele. O que '
     'falta ao uso da sua imagem?',
     'Em _The Truman Show_, toda a gente que aparece com Truman é atriz ou ator; ele não sabe que é filmado. O que falta, antes '
     'de tudo?',
     'O sim dele, que ninguém lhe pediu.',
     [('O sim dos atores que vivem à volta dele.',
       'Os atores trabalham no programa: sabem que são filmados. Quem nunca foi ouvido é o próprio Truman. Repara em quem é filmado '
       'sem saber.'),
      ('O sim de quem cria e produz o programa.',
       'Quem produz o programa é dono da gravação, não da imagem de Truman: o sim tinha de ser dele, e nunca lho pediram. Repara '
       'em quem é filmado sem saber.')],
     'Só Truman pode dizer que sim ao uso da sua imagem; nem o sim dos atores nem o de quem produz o programa o substituem. A '
     'pergunta de hoje é parecida: a que disse a Marta que sim?',
     3, 'reconhecer', 'consentimento', pista='Pensa no que distingue Truman de todos os outros que aparecem no programa.')),
 # R2: «honra e reputação» (sessão 01), um item novo: a montagem. Falso, para a turma não aprender o padrão (os V/F são F, V, F).
 M.recupera(M.fazer(
     'vf', 'Mais do que a vida privada',
     'Caso inventado: uma montagem põe a cara de um colega no corpo de um palhaço. Não mostra a vida privada dele; logo, o artigo '
     '12.º da Declaração não o protege.',
     'Uma montagem com a cara de um colega não revela nada da vida privada dele. Então, fica fora do artigo 12.º da Declaração.',
     'Falso. O artigo 12.º protege também contra «ataques à sua honra e reputação»: a montagem faz do colega uma piada diante dos '
     'outros. É o que viste na sessão 01, com a fotografia da Sara.',
     4, 'distinguir', 'honra e reputação', v=False,
     fe='O 12.º não acaba na vida privada: protege também contra «ataques à sua honra e reputação». Uma montagem que põe os outros '
        'a rir atinge o modo como o colega é visto. Volta à sessão 01, à fotografia da Sara.',
     citacoes=[('dudh-12', 'ataques à sua honra e reputação')],
     pista='Lembra-te de tudo o que o artigo 12.º protege, até ao fim da frase.'),
     origem='cidadania/m1/sessoes/01/'),
 M.olha('Uma fotografia de 1910', 'Olha primeiro para a fotografia; só depois lê a legenda.',
        M.figura(IMG, ALT, CREDITO, 'Addie Card, 12 anos, fiandeira numa fábrica de algodão de North Pownal, no Vermont (Estados '
                 'Unidos), em fevereiro de 1910.', artefacto='Addie Card numa fábrica de algodão, 1910', largura=825, altura=1024)),
 # Conceito espaçado (origem): a Etapa 1, «O que vemos» (cidadania/aula-1/), começa pelo que se observa. 06/11/2026 (revisão): o
 # retorno já não atribui à Etapa 1 uma distinção que lá não está; o terceiro caso (o que nenhuma das duas prova) entra como distrator.
 escolha('O que só a legenda diz',
         'Sem a legenda, o que ficarias sem saber sobre esta rapariga?',
         'Tapa a legenda. O que deixa a fotografia sozinha por dizer?',
         'O nome, a idade e a fábrica onde trabalha.',
         [('Que trabalhava ali contra a vontade dela.',
           'Nem a fotografia nem a legenda dizem o que ela queria: isso é supor. A legenda acrescenta o nome, a idade e a fábrica. '
           'Tapa a legenda e olha outra vez.'),
          ('Que está entre máquinas cheias de bobinas.',
           'As máquinas e as bobinas veem-se na imagem. A legenda é que diz quem ela é, que idade tem e em que fábrica trabalha. '
           'Tapa a legenda e olha outra vez.')],
         'A legenda diz quem ela é: Addie Card, 12 anos, fiandeira numa fábrica de North Pownal. Os pés descalços e as máquinas vês '
         'tu. Como na Etapa 1, «O que vemos», começa-se pelo que se observa.',
         3, 'distinguir', 'imagem e legenda', ver=VER, origem='cidadania/aula-1/', pista='Tapa a legenda: o que continuas a ver?'),
 M.fazer('vf', 'Um rosto que se reconhece',
         'Mesmo sem a legenda, quem conhecesse a Addie podia reconhecê-la nesta fotografia.',
         'Tapada a legenda, alguém que conhecesse a Addie ainda a reconheceria na fotografia.',
         'Verdadeiro. O rosto vê-se de frente e com nitidez: para quem a conhecia, bastava. A legenda junta-lhe o nome, e com ele '
         'qualquer pessoa a pode identificar, mais de cem anos depois.',
         3, 'aplicar', 'pessoa identificável', v=True, ver=VER,
         fe='A legenda não é o que a torna reconhecível: o rosto está de frente e nítido, e quem a conhecesse reconhecê-la-ia. A '
            'legenda junta-lhe o nome. Volta à imagem e tapa a legenda.',
         pista='Pergunta-te o que serve para reconhecer alguém.'),
 M.le('O direito à imagem', 'Quando se pede?',
      [(f'N.º{NB}1', 'O retrato de uma pessoa não pode ser exposto, reproduzido ou lançado no comércio sem o consentimento dela […]', 'cc-79-1', 'n1'),
       (f'N.º{NB}2', 'Não é necessário o consentimento […] quando a reprodução da imagem vier enquadrada na de lugares públicos […]', 'cc-79-2', 'n2'),
       (f'N.º{NB}3', 'O retrato não pode, porém, ser reproduzido, exposto ou lançado no comércio, se do facto resultar prejuízo para '
                    'a honra, reputação ou simples decoro […]', 'cc-79-3', 'n3')],
      f'Código Civil, <a href="{DRE_CC}">Diário da República</a>',
      mais=(M.lei([('Lei n.º 58/2019, artigo 16.º', '[…] os dados pessoais de crianças só podem ser objeto de tratamento com '
                    'base no consentimento […] relativo à oferta direta de serviços da sociedade de informação quando as mesmas já '
                    'tenham completado 13 anos de idade.', 'lei58-16-1', None)], f'<a href="{DRE_LEI}">Diário da República</a>')
            + '<p class="glossa"><b>Decoro</b>: o respeito com que alguém se apresenta aos outros.</p>')),
 M.fazer('sublinhar', 'O que precisa de um sim',
         'No n.º 1, toca nas três palavras que dizem o que não se pode fazer ao retrato sem o sim da pessoa.',
         'No n.º 1 do artigo 79.º, o que não se pode fazer ao retrato sem o consentimento de quem aparece? Toca numa palavra por ação.',
         'As três ações são «exposto, reproduzido ou lançado no comércio»: mostrar, copiar ou vender o retrato. É para estes usos que '
         'a lei pede o sim de quem aparece.',
         3, 'reconhecer', 'direito à imagem',
         frase='O retrato de uma pessoa não pode ser exposto, reproduzido ou lançado no comércio sem o consentimento dela',
         certas=[8, 9, 11], fonte='cc-79-1', l='n1',
         fe='A confusão mais provável é tocar em «retrato» ou em «consentimento»: dizem o que se protege e o que falta, não o que se '
            'faz ao retrato. Procura as três ações entre «pode ser» e «sem».',
         pista='Procura o que se pode fazer a um retrato.'),
 M.fazer('emparelhar', 'Filmar, rever, publicar',
         'Para cada uso do vídeo da Marta: o sim que ela deu já chega, ou falta perguntar-lhe?',
         'Liga cada uso do vídeo ao que a Marta aceitou: já está coberto, ou falta um sim novo?',
         'A Marta disse que sim a filmar e a rever. Pôr o vídeo na página da escola ou enviá-lo a outra pessoa é expô-lo ou '
         'reproduzi-lo: para isso, falta o sim dela.',
         4, 'aplicar', 'consentimento para um uso',
         pares=[['O Duarte filma a cena no ensaio.', 'O sim dela já chega'],
                ['A turma revê o vídeo para corrigir a cena.', 'O sim dela já chega'],
                ['O vídeo vai para a página da escola.', 'Falta perguntar-lhe'],
                ['O Duarte manda o vídeo a um primo.', 'Falta perguntar-lhe']],
         fe='A confusão mais provável é pensar que o sim de filmar cobre o resto. A Marta aceitou um uso: rever a cena. Volta ao caso '
            'e ao n.º 1: expor e reproduzir pedem consentimento.',
         pista='Relê para que aceitou a Marta ser filmada.'),
 escolha('Parte do lugar',
         'Situação nova: fotografas a praça num dia de mercado, cheia de gente; as pessoas aparecem pequenas, ao longe. Para publicar, '
         'precisas do sim de cada uma?',
         'Numa fotografia da praça cheia, as pessoas aparecem ao longe. É preciso o consentimento de cada uma para a publicar?',
         'Não, porque as pessoas aparecem como parte do lugar.',
         [('Não, salvo se alguém na praça tiver menos de 13 anos.',
           'Os 13 anos vêm da Lei n.º 58/2019 e dizem quando uma criança pode aceitar sozinha que um serviço digital trate os seus '
           'dados; não falam de quem aparece numa fotografia da praça. Volta ao n.º 2.'),
          ('Sim: cada pessoa tem de autorizar o seu retrato.',
           'É o n.º 1 lido sozinho. O n.º 2 dispensa o consentimento quando a imagem vem «enquadrada na de lugares públicos»: aqui, '
           'as pessoas fazem parte da praça. Volta ao n.º 2.')],
         'O n.º 2 dispensa o consentimento quando a imagem vem «enquadrada na de lugares públicos»: a fotografia é da praça, e as '
         'pessoas aparecem nela como parte do lugar.',
         3, 'aplicar', 'exceções do n.º 2', citacoes=[('cc-79-2', 'enquadrada na de lugares públicos')],
         pista='Pergunta-te: quem é o assunto desta fotografia?'),
 # Charneira 1: o limite. O lugar público, sozinho, não decide; o n.º 3 vale também nos casos do n.º 2. 06/11/2026 (revisão): uma
 # só ideia (o n.º 3); o rapaz já não é filmado de perto, para a charneira não se resolver com o cartão 11.
 M.fazer('vf', 'Um lugar público não chega',
         'Caso inventado: na praça cheia, o vídeo do mercado apanha um rapaz a cair numa poça. Como foi num lugar público, pode '
         'publicar-se sem lhe perguntar.',
         'Um rapaz cai numa poça, no meio do mercado, e aparece no vídeo da praça. Por ter sido num lugar público, pode publicar-se '
         'sem o consentimento dele.',
         'Falso. Mesmo nos casos do n.º 2, o n.º 3 põe um limite: o retrato não se expõe «se do facto resultar prejuízo para a honra, '
         'reputação ou simples decoro». Uma queda filmada pode prejudicá-lo.',
         4, 'aplicar', 'limite do n.º 3', v=False,
         citacoes=[('cc-79-3', 'se do facto resultar prejuízo para a honra, reputação ou simples decoro')],
         fe='O lugar público não basta. O n.º 3 vale também para os casos do n.º 2: um vídeo de alguém a cair pode prejudicar o seu '
            '«simples decoro». Lê o n.º 3.',
         pista='Relê os três números do artigo 79.º até ao fim.'),
 # Conceito (uma vez, não três): consentimento informado, para um uso, retirável, antes de publicar. Os três traços paralelos vão
 # em tabela (decisão 152). Retirável: Código Civil, artigo 81.º, n.º 2, no «Ler mais» (leitura nossa: o artigo fala da limitação
 # voluntária dos direitos de personalidade, de que o direito à imagem é um).
 M.conceito('Um sim para um uso',
            '<p>A Marta disse que sim. Chega?</p>',
            '<table class="tabela"><thead><tr><th scope="col">O sim</th><th scope="col">No ensaio</th></tr></thead><tbody>'
            '<tr><td data-th="O sim">vale para um uso</td><td data-th="No ensaio">rever a cena, não publicá-la</td></tr>'
            '<tr><td data-th="O sim">pode ser retirado</td><td data-th="No ensaio">se ela mudar de ideias</td></tr>'
            '<tr><td data-th="O sim">pede-se antes</td><td data-th="No ensaio">antes de o vídeo sair</td></tr></tbody></table>',
            'Consentimento informado', 'Um sim de quem sabe para que serve a imagem.',
            '<p>Não depende de ter 13 anos: essa idade, na Lei n.º 58/2019, é a dos serviços digitais.</p>',
            mais=(f'<p>No Código Civil, a limitação voluntária de um direito de personalidade, quando legal, {M.citado("cc-81-2", "é sempre revogável")}, '
                  'ainda que com obrigação de indemnizar (artigo 81.º, n.º 2).</p>')),
 # Transferir 1: a cena da Lia, escrita para a sessão 05 do M1 publicado («Exemplo escrito para esta sessão»), que a turma não fez.
 escolha('O que a Lia aceitou',
         'Caso inventado: a Lia aceita trabalhar numa sala; ninguém lhe diz que as conversas lá dentro são transmitidas. «Aceitaste '
         'trabalhar aqui», diz o coordenador. Isso autoriza a transmissão?',
         'A Lia disse que sim a trabalhar numa sala onde, sem ela saber, as conversas são transmitidas. O sim dela chega para isso?',
         'Não: ela aceitou trabalhar ali, não ser transmitida.',
         [('Sim: quem aceita a sala aceita o que lá se passa.',
           'Aceitar trabalhar numa sala não é aceitar tudo o que lá se faz: o sim vale para o que se explicou, e a transmissão '
           'ninguém lha explicou. Volta à cena e procura o que lhe disseram.'),
          ('Depende de a Lia ter assinado um papel a aceitar.',
           'Uma assinatura não muda o que a Lia sabia: assinaria o mesmo sem saber da transmissão. O sim vale para aquilo que se '
           'explicou. Volta à cena e procura o que lhe disseram.')],
         'A Lia aceitou o que lhe explicaram: trabalhar ali. A transmissão ficou de fora, e um sim só vale para o que se sabe. Na cena, '
         'ela responde: «Aceitei aquilo que me explicaram.»',
         3, 'transferir', 'consentimento informado', pista='Pergunta-te o que sabia a Lia quando disse que sim.'),
 # Decisão 161: o caso real, com fonte oficial aberta (dgsi.pt). Cita-se só o que o acórdão diz: a conclusão do próprio tribunal
 # sobre o que foi dito à mãe (06/11/2026, revisão: antes citava-se o depoimento da representante do clube, que é uma das partes) e
 # o princípio do sumário (IV). A mãe perdeu: o tribunal concluiu que ela consentira na publicação numa publicação; o que dizia (que
 # as fotografias eram só para os sócios) não ficou provado. A sessão era «pública aberta a sócios e familiares» (facto 7).
 escolha('Um caso real',
         'Caso real (Supremo Tribunal de Justiça, 2011): uma mãe e a filha, fotografadas na piscina do clube, saíram na capa de uma '
         'revista. A mãe (a «1.ª A.») perdeu. Porquê?',
         'Em 2011, o Supremo Tribunal de Justiça não deu razão a uma mãe que se queixava de fotografias dela e da filha numa revista. '
         'Segundo esta passagem, porquê?',
         'Tinham-lhe dito que as fotografias eram para uma publicação.',
         [('A piscina era um lugar público, onde não é preciso pedir.',
           'O tribunal não decidiu pelo lugar: as fotografias foram tiradas numa sessão pública aberta a sócios e familiares, e o '
           'acórdão não discute se isso dispensava o consentimento. Decidiu pelo que se disse à mãe antes das fotografias. Volta à '
           'passagem citada.'),
          ('A revista tinha fins didáticos, por ser sobre o bem-estar.',
           'O tribunal não decidiu pelos fins da revista, e ficou provado que ela servia para captar clientes para o clube. Decidiu '
           'pelo que se disse à mãe. Volta à passagem citada.')],
         'Para o tribunal, quem aceita ser fotografado para um fim não autoriza, sem mais, outro: «não podem as imagens ser utilizadas '
         'para fim diverso». Aqui, disseram à mãe que era para uma publicação; que seria só para os sócios, ela não o provou.',
         4, 'transferir', 'consentimento para um uso',
         cita=('[…] extrai-se a conclusão de que à 1.ª A. foi dada indicação de que as fotografias se destinavam a figurar numa '
               'publicação'),
         fonte='stj-2011-indicacao', citacoes=[('stj-2011-iv', 'não podem as imagens ser utilizadas para fim diverso')],
         liga=[{'t': 'Ler o acórdão do Supremo Tribunal de Justiça, 07/06/2011 (dgsi.pt)', 'href': DGSI}],
         pista='Pergunta-te em que se apoiou o tribunal para decidir.'),
 # ---------------------------------------------------------------- parte 2, pesar e escrever (50 minutos)
 M.volta('A direção diz que é para ensinar',
         'A direção gosta da ideia: diz que o vídeo tem fins didáticos, porque mostra como se prepara uma peça. A Marta '
         'pede: «A queda não.» O Duarte responde: «Aceitaste ser filmada.»',
         [('Código Civil, artigo 79.º, n.º 2', 'Não é necessário o consentimento da pessoa retratada quando assim o justifiquem […] '
                                              'finalidades científicas, didácticas ou culturais […]', 'cc-79-2', None)],
         f'Código Civil, <a href="{DRE_CC}">Diário da República</a>.', carimbo='Caso inventado.'),
 M.fazer('emparelhar', 'O que se sabe e o que falta',
         'Depois da resposta do Duarte: o que já está no caso e o que ainda está por saber?',
         'Em cada linha: está no caso ou ainda falta saber?',
         'Sabes para que a Marta aceitou e o que pede. Não sabes se o vídeo serve para ensinar, só que a direção o diz, nem se a '
         'queda a prejudica. São estas as dúvidas que vão para o papel.',
         3, 'aplicar', 'facto e dúvida',
         pares=[['A razão por que a Marta aceitou ser filmada', 'Já está no caso'],
                ['O pedido da Marta sobre a queda', 'Já está no caso'],
                ['A utilidade do vídeo para ensinar', 'Ainda está em aberto'],
                ['O efeito da queda no decoro da Marta', 'Ainda está em aberto']],
         fe='A confusão mais provável é tomar a palavra da direção por prova: dizer «fins didáticos» não mostra que o vídeo sirva para '
            'ensinar. Volta ao caso e separa o que está nele do que alguém afirma.',
         pista='Pergunta-te: isto está no caso, ou alguém só o afirma?'),
 M.em_turma(DECIDE_Q, [
     ('O lado da direção', f'O n.º 2 dispensa o consentimento por {M.citado("cc-79-2", "finalidades científicas, didácticas ou culturais")}. '
                           'Mostrar a preparação de uma peça ensina.'),
     ('O lado da Marta', f'O retrato não pode ser {M.citado("cc-79-1", "exposto")} sem {M.citado("cc-79-1", "o consentimento dela")}; '
                         'ela só aceitou rever a cena.'),
     ('Uma objeção', f'E se a queda prejudicar o {M.citado("cc-79-3", "simples decoro")} da Marta (n.º 3)?')],
     {'O que se faz': 'Decides outra vez e escolhes a razão que pesou.',
      'Quanto tempo': 'Três minutos; em turma, até treze.',
      'O que fica escrito': 'Nada em papel; a escolha fica nos artefactos.',
      'Se estás sozinho': 'Compara com a escolha do início e abre os três lados.'},
     prova=('O que pesou mais na escolha?', ('O uso aceite (n.º 1)', 'Fins didáticos (n.º 2)', 'O decoro (n.º 3)')),
     prova_rot='A razão que pesou', intro='', nota=None),
 M.fazer('emparelhar', 'Facto, regra ou razão',
         'Liga cada frase ao que ela é numa justificação.',
         'Facto, regra ou razão de uma das partes: o que é cada frase?',
         'Que a Marta aceitou ser filmada para rever é um facto do caso; o n.º 1 é uma regra escrita numa lei, que vale para todos; '
         '«Aceitaste ser filmada» é a razão de quem quer publicar, que ainda tem de ser pesada.',
         3, 'distinguir', 'relato e princípio',
         pares=[['A Marta aceitou ser filmada para a turma rever a cena.', 'Um facto do caso'],
                ['«O retrato de uma pessoa não pode ser exposto […] sem o consentimento dela»', 'Uma regra que vale para todos'],
                ['«Aceitaste ser filmada.»', 'A razão de uma das partes']],
         citacoes=[('cc-79-1', 'O retrato de uma pessoa não pode ser exposto')],
         fe='A confusão mais provável é tomar a razão de uma parte por regra: «Aceitaste ser filmada» explica o que o Duarte quer, '
            'mas não vale para todos. Uma regra está escrita numa lei. Volta ao artigo 79.º.',
         pista='Pergunta a cada frase: aconteceu, está numa lei, ou é de alguém?'),
 M.fazer('ordenar', 'A justificação por ordem',
         'Põe a justificação por ordem: primeiro o facto, depois a fonte, a aplicação e, no fim, o limite.',
         'Ordena: o que aconteceu, o texto que se aplica, a ligação entre os dois e o que ainda falta saber.',
         'Facto, fonte, aplicação, limite: cada passo apoia-se no anterior, e o limite diz até onde a conclusão pode ir.',
         4, 'aplicar', 'facto, fonte, aplicação, limite',
         passos=['A Marta aceitou ser filmada só para a turma rever a cena.',
                 'O Código Civil pede o consentimento da pessoa para expor o seu retrato.',
                 'Pôr o vídeo na página da escola é expô-lo sem o sim dela.',
                 'Falta saber se a queda prejudica o decoro da Marta.'],
         fe='A confusão mais provável é começar pela lei ou pôr o que falta saber antes da aplicação. Começa pelo que aconteceu; '
            'depois o texto; o que falta saber fecha a justificação.',
         pista='Começa pelo que aconteceu.'),
 # Charneira 2: a conclusão que não vai além das provas; o erro esperado é a razão do Duarte, ou uma intenção suposta (tirada, como
 # no Abre, dos risos dos colegas).
 escolha('O que as provas permitem',
         'O que se pode concluir sem ir além do que o caso e o artigo 79.º mostram?',
         'O que permitem concluir as provas, sem ir além delas?',
         'O sim de rever não chega; os fins didáticos estão por provar.',
         [('A escola pode publicar, porque a Marta aceitou ser filmada.',
           'É a razão do Duarte, não uma prova: a Marta aceitou um uso, rever a cena. Para expor o retrato, o n.º 1 pede «o '
           'consentimento dela». Esta conclusão deixa de fora o que ela aceitou.'),
          ('A escola não pode publicar, porque os colegas se riram dela.',
           'Os colegas riram-se porque a cena ficou ótima: isso não prova que a queda prejudique o decoro da Marta, que ainda está '
           'em aberto. Esta conclusão vai além das provas. Separa o que aconteceu do que alguém supõe.')],
         'Diz o que as provas mostram (a Marta aceitou um uso: rever a cena) e deixa aberto o que falta provar: se o vídeo serve '
         'para ensinar.',
         3, 'aplicar', 'conclusão e provas', citacoes=[('cc-79-1', 'o consentimento dela')],
         pista='Procura a conclusão que não junta nada às provas.'),
 M.papel(PERGUNTA,
         ['A tua conclusão, por agora.',
          'Uma prova: um facto do caso e uma expressão exata, entre aspas, com o artigo.',
          'Uma dúvida que ainda tens.'],
         ['A conclusão responde à pergunta sem ir além das provas.',
          'A prova junta um facto a uma expressão exata, com o artigo.',
          'A dúvida, respondida, podia mudar a conclusão.'],
         '<p>Outro caso, inventado: um jornal publica uma fotografia da praça em festa, com as pessoas ao longe.</p><ol>'
         '<li>Conclusão: pode publicá-la sem pedir a cada pessoa.</li>'
         '<li>Prova: a fotografia é da praça; o consentimento não é necessário quando a imagem vem '
         f'{M.citado("cc-79-2", "enquadrada na de lugares públicos")} (artigo 79.º, n.º 2).</li>'
         '<li>Dúvida: alguém aparece de perto, como assunto?</li></ol>',
         'Num papel pequeno, sozinho e sem telemóvel.',
         relogio_min=12),
 M.levar(FRASE, ['O sim vale para o uso que se explicou.',
                 'Mesmo quando a lei dispensa o consentimento, o retrato não pode prejudicar a honra, a reputação ou o decoro.']),
]

# o lugar da certa em cada escolha (0, 1 ou 2), com a semente do motor: nunca o mesmo em mais de metade, nem três seguidos
LUGARES = (2, 0, 1, 1, 2, 0)

# O passo do projeto (plano, secção 3: «ética das entrevistas (#84), o teu pedido de consentimento em quatro partes»). O que se diz
# dos menores, do anonimato e da desistência é o que a página do projeto já diz (cidadania/projeto/, «Ética: as pessoas que
# entrevistas»).
DEPOIS = ('<article class="c"><p class="rot">O passo do teu projeto</p><p class="tit">O teu pedido de consentimento</p>'
          '<p class="sub">No teatro-documento, as falas vêm do que investigas, entrevistas incluídas. Antes de gravar alguém, escreves, '
          'em papel, o teu pedido de consentimento em quatro partes: para quê; que uso (a voz, a cara ou só as palavras); onde fica e '
          'até quando; como se retira o sim. O que conta: cada parte numa frase simples; o uso diz se a pessoa aparece ou não; a pessoa '
          'sabe que pode desistir a qualquer momento; se for menor, o pedido vai também ao encarregado de educação.</p>'
          '<p class="ir"><a href="../../../projeto/#metodo">A ética das entrevistas, no enunciado da Pergunta Humana</a></p></article>')


def sessao():
    d = {
        'id': 'cidadania-m1-s02', 'chave': 'epi-cid-m1-s02', 'versao': '2026-11-06-molde', 'marca': 'CD', 'molde': L.MOLDE,
        'titulo': 'Sessão 02: A imagem dos outros', 'h1': 'Cidadania, módulo 1, sessão 02: A imagem dos outros',
        'modulo': {'n': 1, 'nome': 'Humanos', 'url': L.LENTE + 'cidadania/piloto/m1/'},
        'saida': 'cidadania/m1/sessoes/02/index.html',
        # 06/11/2026: a sessão 03 também passou ao molde final (decisão 166); a s02 leva à s03 nova.
        'seguinte': '../03/', 'seguinteRotulo': 'Sessão 03: Quem tem lugar?',
        'fontes': M.ref('Código Civil, artigos 79.º, n.os 1 a 3, e 81.º, n.º 2, na versão consolidada do Diário da República. Lei n.º '
                        '58/2019, de 8 de agosto, artigo 16.º, n.º 1, no Diário da República. Declaração Universal dos Direitos Humanos, '
                        'artigo 12.º, na transcrição portuguesa do UNRIC. Acórdão do Supremo Tribunal de Justiça de 7 de junho de 2011, '
                        'processo 1581/07.3TVLSB.L1.S1, em dgsi.pt. Fotografia: Lewis Hine (atribuição), _Addie Card, 12 years. Spinner '
                        'in North Pormal [i.e., Pownal] Cotton Mill. Vt. […]_, fevereiro de 1910, National Child Labor Committee collection, '
                        'Library of Congress, Prints and Photographs Division (LC-DIG-nclc-05282), domínio público (o registo diz «No known '
                        'restrictions on publication»). '
                        '_The Truman Show_, filme de Peter Weir (1998). O caso da Marta, o da montagem, o da praça, o do rapaz na poça, '
                        'o da Lia (escrito para a sessão 05 do M1 publicado) e o do jornal são inventados; o do Supremo Tribunal '
                        'de Justiça é real.'),
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
