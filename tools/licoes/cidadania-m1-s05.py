# Fonte da sessão 05 do M1 de Cidadania, «Quem guarda os meus dados?», na versão final do molde cidadania-2026-11 (plano do
# molde, secção 3, linha «05»; decisões 144 a 146, 152 a 155, 161 e 166 a 168). 06/11/2026: substitui a fonte do piloto de 31/10,
# que escrevia cidadania/piloto/m1-s05/ (essa página fica como está até ao pedido 3, que faz os redirecionamentos do piloto de uma
# vez); a chave epi-cid-m1-s05 é a mesma, e a versão sobe com preservarAnterior (cfg da família). Corre-se para escrever o .json
# ao lado; o .json é que o gerador (tools/licoes_lente.py) lê, e nunca se edita à mão. Os cartões montam-se com o ajudante comum
# tools/cidadania_molde.py; cada excerto de lei ou de acórdão vem do registo tools/cidadania_fontes.json (texto exato da fonte
# oficial, aberta a 6/11/2026, confirmado) e o ajudante recusa escrever um excerto que lá não esteja.
#
# 23 cartões (9 de ler, 14 de fazer), pela ordem e com os tempos da secção 2 do plano, como a s01; a ordem é fixa (cfg.aula) e a
# resposta certa de cada escolha fica no lugar pedido em LUGARES, calculado com a semente do motor. Cada exercício tem a sua pista,
# que não dá a resposta. O que só o docente faz vive no guia (tools/cidadania_piloto.py, GUIA['05']), nunca aqui.
#
# Fontes abertas a 6/11/2026, uma de cada vez (nada citado de memória):
# - Lei n.º 58/2019, artigos 19.º, n.os 3 e 4, e 21.º, n.os 1 e 4, no Diário da República Eletrónico (registo lei58-19-*, lei58-21-*);
# - Constituição, artigos 18.º, n.º 2, e 35.º, n.os 1 e 4, texto consolidado no Diário da República Eletrónico (crp-18-2, crp-35-*);
#   e artigo 26.º, n.º 1 (crp-26-1, já no registo, da s01);
# - Acórdão do Supremo Tribunal de Justiça de 8/2/2006, processo 05S3139, em dgsi.pt (registo stj-2006-*): o caso real da sessão
#   (decisão 161). Um armazenista de produtos farmacêuticos, depois de furtos de medicamentos, pôs câmaras viradas para os postos
#   de trabalho; o tribunal mandou retirá-las do armazém.
# - Gravura: «A General Idea of a Penitentiary Panopticon in an Improved, but as yet, Jan.y 23.d 1791) Unfinished State» (assim, com
#   o parêntese só a fechar, na estampa; 06/11/2026, revisão: nas Fontes vai só o princípio do título, como no crédito), a
#   estampa desdobrável de The Works of Jeremy Bentham, vol. IV (Edimburgo, William Tait, 1843), no exemplar da Biblioteca da
#   Universidade de Sevilha digitalizado no Internet Archive (BRes092083, imagem n36), com a marca de domínio público (Public Domain
#   Mark 1.0) lida nos metadados do registo. Vista inteira; a estampa não nomeia o desenhador (a atribuição habitual ao arquiteto
#   Willey Reveley fica «a confirmar» no guia). O ficheiro img/cidadania/panotico-bentham-1791-planta.webp (1400 × 1138) é a folha
#   inteira, só reduzida. O Commons respondeu 429 aos pedidos do ficheiro; não se insistiu.
# - Vídeo (decisão 155): nenhum. O plano tira o TED-Ed do piloto.
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

IMG = '../../../../img/cidadania/panotico-bentham-1791-planta.webp'
ALT = ('Gravura de arquitetura: em cima, à esquerda, a fachada de um edifício redondo de seis pisos, com janelas em arco; à '
       'direita, o mesmo edifício cortado ao meio, com as celas, marcadas A, na parede de fora e, no centro, o alojamento do '
       'inspetor, H, e as galerias de inspeção, F; em baixo, metade da planta, um anel de celas à volta de um centro com '
       'círculos concêntricos; à direita, a legenda das letras, em inglês.')
ALT_VER = 'A mesma gravura: o edifício redondo em fachada e em corte, e por baixo metade da planta, com o anel de celas à volta do centro.'
VER = f'<img src="{IMG}" alt="{ALT_VER}">'
IA = 'https://archive.org/details/BRes092083'
DRE_LEI = 'https://diariodarepublica.pt/dr/detalhe/lei/58-2019-123815982'
DRE_CRP = 'https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-aprovacao-constituicao/1976-34520775'
DGSI = 'https://www.dgsi.pt/jstj.nsf/954f0ce6ad9dd8b980256b5f003fa814/65e859e4729cc7688025712d00421026?OpenDocument'
CREDITO = ('<i>A General Idea of a Penitentiary Panopticon […]</i>, 1791, estampa de <i>The Works of Jeremy Bentham</i>, vol. IV, '
           'Edimburgo, William Tait, 1843. Biblioteca da Universidade de '
           f'Sevilha, digitalização no Internet Archive. <a href="{IA}">Registo de origem</a>. Domínio público (Public Domain Mark 1.0).')
PERGUNTA = 'Uma câmara na sala protege quem?'
DECIDE_Q = 'A escola deve pôr câmaras nas salas de aula?'
FRASE = 'Primeiro, para quê; depois, só o necessário.'
LEI_19_3 = ('Nos estabelecimentos de ensino, as câmaras de videovigilância só podem incidir sobre os perímetros externos e locais de '
            'acesso, e ainda sobre espaços cujos bens e equipamentos requeiram especial proteção, como laboratórios ou salas de '
            'informática.')


def escolha(rot, p, p2, certa, erradas, f, minutos, tipo, conceito, **extra):
    """Uma escolha de três opções; a certa vai para o lugar de LUGARES (preenchido em sessao())."""
    c = M.fazer('escolha', rot, p, p2, f, minutos, tipo, conceito, **extra)
    c['_certa'], c['_erradas'] = M.ref(certa), [(M.ref(o), M.ref(e)) for o, e in erradas]
    return c


CARTOES = [
 # ---------------------------------------------------------------- parte 1, ver antes de concluir (60 minutos)
 # O caso das câmaras vem do piloto (s05, cartão 1), reescrito: o furto, a proposta para as salas e o cartaz. Sem «grupo».
 M.abre('Quem guarda os meus dados?',
        f'ver e ler (60{NB}min), pausa (10{NB}min), pesar e escrever (50{NB}min) e o teu projeto (45{NB}min).',
        'Num mês, desapareceram três telemóveis da sala 12. A associação de estudantes propõe câmaras em todas as salas de aula, a '
        'filmar durante as aulas, e afixa um cartaz: «Quem não deve não teme.» A direção decide na próxima semana.',
        PERGUNTA),
 M.decide(DECIDE_Q, [
     ('Quem acha que sim', '«Com câmaras, ninguém rouba.» Desapareceram três telemóveis, e quem não deve não teme.'),
     ('Quem acha que não', 'Numa sala filmada o dia todo, ninguém fala à vontade. E não se sabe quem vê as imagens.'),
     ('Uma objeção', 'E se só a direção visse as imagens, e só depois de um furto? Mudava a tua resposta?')]),
 # R1 (sessão 04, sem obra): o que se prova e o que se discute. «Com câmaras, ninguém rouba» é uma previsão: fala do que vai
 # acontecer e só se põe à prova depois. Os erros prováveis: tomá-la por facto (os furtos aconteceram) ou por mera opinião.
 M.recupera(escolha(
     'Prever não é provar',
     'Há quem diga: «Com câmaras, ninguém rouba.» Como se classifica esta frase?',
     'A frase «Com câmaras, ninguém rouba» é um facto, uma opinião ou outra coisa?',
     'Uma previsão: só o futuro a confirma ou desmente.',
     [('Um facto: os três telemóveis desapareceram mesmo.',
       'Os furtos são um facto, mas a frase não fala deles: diz o que vai acontecer com câmaras. Isso ainda ninguém viu. Repara '
       'no que a frase promete para depois das câmaras.'),
      ('Uma opinião: diz só o que alguém acha melhor.',
       'Uma opinião diz o que alguém acha bom ou mau, e discute-se. Esta frase diz o que vai acontecer, e isso pode contar-se '
       'depois. Repara no que a frase promete.')],
     'Na sessão 04 viste que uma opinião se discute e um facto se prova. «Ninguém rouba» fala do futuro: é uma previsão, que só '
     'os furtos contados depois das câmaras podem confirmar ou desmentir.',
     3, 'distinguir', 'facto, previsão e opinião', pista='Pergunta-te o que seria preciso para saber se a frase é verdadeira.')),
 # R2: consentimento para um uso (sessão 02), que aqui passa a finalidade. Falso, para a turma não aprender o padrão.
 M.recupera(M.fazer(
     'vf', 'Dado para quê',
     'Caso inventado: deste o teu contacto à escola para a visita de estudo. Já que o deste, a escola pode passá-lo à agência de '
     'viagens, para publicidade.',
     'O teu contacto foi dado à escola para a visita de estudo. Por isso, pode servir também para a agência de viagens te mandar '
     'publicidade.',
     'Falso. Deste o contacto para a visita: é para isso que serve. Na sessão 02, a regra era «O sim vale para o uso que se '
     'explicou»; com os dados chama-se finalidade.',
     4, 'aplicar', 'finalidade', v=False,
     fe='Dar um dado para uma coisa não o entrega para todas. Na sessão 02, com o vídeo da Marta: «O sim vale para o uso que se '
        'explicou.» Com os dados é igual: servem a finalidade para que os deste, a visita.',
     pista='Lembra-te para que aceitou a Marta ser filmada, na sessão 02.'),
     origem='cidadania/m1/sessoes/02/'),
 M.olha('Uma casa de inspeção', 'Olha primeiro para a gravura inteira; só depois lê a legenda.',
        M.figura(IMG, ALT, CREDITO, 'Uma prisão redonda proposta por Jeremy Bentham, numa gravura datada de 23 de janeiro de 1791: '
                 'fachada e corte (em cima), metade da planta (em baixo). A: celas; F: galerias de inspeção; H: alojamento do inspetor.',
                 artefacto='Uma prisão redonda de Jeremy Bentham, 1791', largura=1400, altura=1138)),
 # Quem vê quem: o centro vê o anel inteiro. Os erros: a entrada (um ponto da parede de fora) e as janelas (dão para fora).
 escolha('Quem vê quem',
         'Pela gravura, de onde se pode ver o anel inteiro das celas?',
         'Na gravura, há um sítio de onde se vê cada cela do anel. Onde fica?',
         'Do meio do edifício, onde ficam H e F.',
         [('Da entrada, E, aberta na parede de fora.',
           'A entrada fica num ponto da parede de fora, por baixo das celas: dali não se vê o anel. Procura no corte e na planta o '
           'que fica no meio, com as celas à volta.'),
          ('Das janelas da fachada, abertas para a rua.',
           'As janelas abrem as celas para fora, para a luz; não dão para as outras celas. Procura o ponto de onde o anel se vê '
           'inteiro: o meio do edifício.')],
         'O inspetor (H) e as galerias de inspeção (F) ficam no meio, e as celas (A) dão a volta: do centro, o anel vê-se inteiro.',
         3, 'reconhecer', 'quem vê quem', ver=VER, pista='Compara a planta com o corte: onde fica cada letra?'),
 # O que se vê, o que só a legenda diz e o que nenhuma das duas prova (a distinção da s01, cartão 7, com outro material).
 M.fazer('emparelhar', 'Gravura, legenda ou nenhuma',
         'Liga cada frase ao que a sustenta: a gravura, a legenda ou nenhuma das duas.',
         'Para cada frase: vê-se na gravura, só a legenda o diz, ou nenhuma das duas o prova?',
         'O anel de celas vê-se no desenho. O nome de Bentham não está na estampa: só a legenda o diz. Que alguém se porte melhor por '
         'poder ser visto é uma ideia sobre pessoas; um desenho de um edifício não a prova.',
         3, 'distinguir', 'imagem e legenda',
         pares=[['As celas ficam em anel, à volta do centro.', 'A gravura mostra'],
                ['Foi Jeremy Bentham quem propôs este edifício.', 'Só a legenda diz'],
                ['Quem está numa cela porta-se melhor por poder ser visto.', 'Nenhuma das duas prova']],
         ver=VER,
         fe='A confusão mais provável é dar à gravura uma ideia sobre pessoas: o desenho mostra paredes e lugares, não o que alguém '
            'sente ou faz. E o nome de Bentham não está no desenho. Olha outra vez, sem a legenda.',
         pista='Tapa a legenda e pergunta-te o que um desenho de paredes consegue mostrar.'),
 M.le('Onde, e para quê', 'Onde, e para quê?',
      [(f'19.º, n.º{NB}3', LEI_19_3, 'lei58-19-3', 'n3'),
       (f'35.º, n.º{NB}1', '[…] o direito de acesso aos dados informatizados que lhes digam respeito […] e o direito de conhecer a '
                          'finalidade a que se destinam […]', 'crp-35-1', 'c1')],
      f'<a href="{DRE_LEI}">Lei n.º 58/2019</a>; <a href="{DRE_CRP}">Constituição</a>.',
      mais=(M.lei([('Lei n.º 58/2019, artigo 19.º, n.º 4', 'Nos casos em que é admitida a videovigilância, é proibida a captação de som, '
                    'exceto no período em que as instalações vigiadas estejam encerradas ou mediante autorização prévia da CNPD.',
                    'lei58-19-4', None)])
            + '<p class="glossa"><b>Perímetro externo</b>: a zona à volta dos edifícios. <b>CNPD</b>: Comissão Nacional '
              'de Proteção de Dados.</p>')),
 M.fazer('sublinhar', 'Uma lista fechada',
         'No n.º 3, toca na palavra que fecha a lista: fora dos sítios que a lei nomeia, as câmaras não podem filmar.',
         'No n.º 3, uma palavra impede as câmaras de filmar os sítios que a lista não nomeia. Toca nela.',
         'A palavra é «só»: as câmaras «só podem incidir» sobre os sítios da lista. Sem ela, a lista seria um exemplo; com ela, é '
         'o limite.',
         3, 'reconhecer', 'lista fechada', frase=LEI_19_3, certas=[8], fonte='lei58-19-3', l='n3',
         fe='A confusão mais provável é tocar em «podem»: sozinha, essa palavra deixa filmar. É outra palavra, antes dela, que '
            'limita os sítios. Lê o princípio da frase devagar.',
         pista='Lê a frase e tira-lhe uma palavra de cada vez: quando é que os sítios deixam de ter limite?'),
 M.fazer('emparelhar', 'Cada dado, para quê',
         'Caso inventado: o formulário da visita de estudo pede estes dados. Liga cada um à finalidade que o justifica.',
         'Para que serve cada dado do formulário da visita de estudo? Liga cada um à sua finalidade.',
         'Cada dado tem uma razão concreta na visita. A profissão dos pais não serve para nada nela: um dado sem finalidade não se '
         'pede.',
         4, 'aplicar', 'finalidade',
         pares=[['Alergias alimentares', 'O almoço durante a visita'],
                ['Contacto de emergência', 'Um acidente durante a saída'],
                ['Autorização do encarregado de educação', 'Sair da escola em tempo de aula'],
                ['Profissão dos pais', 'Nenhuma finalidade da visita']],
         fe='A confusão mais provável é arranjar uma finalidade para todos os dados. A profissão dos pais não ajuda a almoçar, a sair '
            'nem a socorrer ninguém. Pergunta primeiro para quê, e só depois o quê.',
         pista='Para cada dado, imagina o dia da visita: em que momento faz falta?'),
 escolha('Onde a lei deixa',
         'Situação nova: outra escola quer uma câmara virada para um espaço lá dentro. Para onde a lei a deixa virar?',
         'Numa escola que não é a tua, para onde pode estar virada uma câmara, segundo o n.º 3?',
         'Para a oficina onde se guardam as máquinas de soldar.',
         [('Para o pátio interior, onde os alunos passam o intervalo.',
           'O pátio interior não é perímetro externo nem um acesso, e não guarda equipamentos que peçam especial proteção. Com o '
           '«só», o que não está na lista fica de fora. Volta ao n.º 3.'),
          ('Para a sala de convívio, com os sofás e as mesas.',
           'A sala de convívio não cabe em nenhuma parte da lista: não é perímetro, nem acesso, nem um espaço como um laboratório. '
           'Volta ao n.º 3 e aos exemplos do fim.')],
         'A oficina guarda equipamentos caros, como um laboratório ou uma sala de informática: cabe na terceira parte da '
         'lista do n.º 3. O pátio interior e a sala de convívio não estão nela.',
         3, 'aplicar', 'o que as câmaras podem filmar', pista='Lê os exemplos do fim do n.º 3 e procura o lugar que se parece com eles.'),
 # Charneira 1: o limite da lista. O erro esperado é ler «espaços cujos bens… requeiram especial proteção» como qualquer sala
 # onde haja coisas de valor (os telemóveis dos alunos).
 M.fazer('vf', 'Uma sala não é um laboratório',
         'Como desapareceram telemóveis, a escola pode filmar as salas de aula: são espaços com bens que pedem especial proteção.',
         'Com os furtos de telemóveis, as salas de aula passam a ser espaços cujos bens pedem especial proteção, e podem ser filmadas.',
         'Falso. Os exemplos da lei são «laboratórios ou salas de informática»: espaços pelos equipamentos que guardam. Uma sala de '
         'aula comum não está na lista, e o «só» fecha-a.',
         4, 'aplicar', 'limite da lista', v=False,
         citacoes=[('lei58-19-3', 'laboratórios ou salas de informática')],
         fe='Os telemóveis andam com os alunos; não fazem da sala de aula um laboratório. A lei dá como exemplos «laboratórios ou '
            'salas de informática», e o «só» fecha a lista. Volta ao n.º 3.',
         pista='Compara a sala de aula com os exemplos que a lei dá no fim do n.º 3.'),
 # Conceito: finalidade e proporcionalidade (Constituição, artigo 18.º, n.º 2). As três perguntas paralelas vão em tabela
 # (decisão 152); o artigo vai em «Ler mais», com a expressão exata.
 M.conceito('Para quê, e quanto',
            '<p>Câmaras nas salas: podiam travar os furtos. Chega isso?</p>',
            '<table class="tabela"><thead><tr><th scope="col">A pergunta</th><th scope="col">Na sala 12</th></tr></thead><tbody>'
            '<tr><td data-th="A pergunta">Para quê?</td><td data-th="Na sala 12">travar os furtos de telemóveis</td></tr>'
            '<tr><td data-th="A pergunta">Há outro meio?</td><td data-th="Na sala 12">cacifos com chave, câmaras nas entradas</td></tr>'
            '<tr><td data-th="A pergunta">O que custa?</td><td data-th="Na sala 12">uma turma filmada o dia todo</td></tr>'
            '</tbody></table>',
            'Proporcionalidade', 'Restringir um direito só no necessário para proteger outro.',
            '<p>Não é «quem não deve não teme»: não ter culpa não torna uma câmara necessária.</p>',
            mais=(f'<p>Na Constituição, as restrições a direitos devem {M.citado("crp-18-2", "limitar-se ao necessário para salvaguardar outros direitos ou interesses constitucionalmente protegidos")} '
                  '(artigo 18.º, n.º 2).</p>')),
 # Transferir 1 (o completar do 18.º, n.º 2, piloto 16, aplicado à aplicação de presenças do piloto 14, aqui «programa», para não
 # se confundir com a aplicação da cadeia): a finalidade e o necessário, num caso novo. Os erros: confundir o que o programa faz com aquilo para que serve; trocar necessário por seguro.
 M.fazer('completar', 'O que a finalidade pede',
         'Caso inventado: para marcar presenças, um programa passa a guardar onde está cada aluno, o dia todo. Completa.',
         'Um programa de presenças guarda a localização de cada aluno durante todo o dia. Completa o raciocínio.',
         'Marcar presenças pede saber quem está na aula. A localização o dia todo junta dados que essa finalidade dispensa: vai além '
         'do necessário, a medida que a Constituição põe às restrições.',
         3, 'transferir', 'proporcionalidade',
         frase='A finalidade é saber [1]. Guardar a localização o dia todo [2].',
         lacunas=[{'o': ['quem está na aula', 'por onde anda cada aluno', 'se os alunos estão seguros'], 'c': 0},
                  {'o': ['junta dados que a finalidade dispensa', 'é o meio mais completo', 'fica justificado se ninguém se queixar'], 'c': 0}],
         fe='A confusão mais provável é tomar o que o programa faz pela sua finalidade. Pergunta primeiro para quê: para marcar '
            'presenças, basta saber quem está na aula. O resto vai além.',
         pista='Separa o que o programa faz daquilo para que existe.'),
 # Decisão 161: o caso real, com fonte oficial aberta (dgsi.pt). Cita-se só o que o acórdão diz: a passagem da fundamentação sobre
 # os trabalhadores tornados suspeitos; nos retornos, a autorização da CNPD (o tribunal decidiu «independentemente» dela) e o facto
 # provado dos furtos. Conceito espaçado (origem): o artigo 26.º da Constituição, que a turma leu na sessão 01 (Volta ao caso).
 escolha('Um caso real',
         'Caso real (Supremo Tribunal de Justiça, 2006): depois de furtos de medicamentos, um armazenista filmava os trabalhadores sem '
         'parar. O tribunal mandou tirar as câmaras do armazém. Porquê?',
         'Em 2006, o Supremo Tribunal de Justiça mandou um armazenista retirar do armazém as câmaras viradas para os trabalhadores. '
         'Segundo esta passagem, porquê?',
         'Faziam de cada trabalhador um suspeito, sem prazo.',
         [('Faltava à empresa a autorização para as câmaras.',
           'Não foi por isso: o tribunal decidiu «independentemente da autorização concedida pela Comissão Nacional de Protecção de '
           'Dados». Volta à passagem: o que faziam as câmaras aos trabalhadores?'),
          ('Os furtos não tinham acontecido; eram só um receio.',
           'Os furtos aconteceram: nos factos provados lê-se que «a R. via-se confrontada com furtos de medicamentos» (a R. é a '
           'empresa). Mesmo assim, as câmaras saíram. Volta à passagem citada.')],
         'O tribunal não negou os furtos: disse que as câmaras transformavam os trabalhadores «indefinidamente em suspeitos». Na '
         'sessão 01 leste, no artigo 26.º, o direito «à reserva da intimidade da vida privada»: é esse que estava em causa.',
         4, 'transferir', 'reserva da vida privada',
         cita=('[…] o empregador […] não pode sujeitar os seus trabalhadores a uma permanente medida de polícia, transformando-os '
               'indefinidamente em suspeitos de prática de ilícitos criminais […]'),
         fonte='stj-2006-suspeitos',
         citacoes=[('stj-2006-suspeitos', 'indefinidamente em suspeitos'),
                   ('stj-2006-autorizacao', 'independentemente da autorização concedida pela Comissão Nacional de Protecção de Dados'),
                   ('stj-2006-furtos', 'a R. via-se confrontada com furtos de medicamentos'),
                   ('crp-26-1', 'à reserva da intimidade da vida privada')],
         origem='cidadania/m1/sessoes/01/',
         liga=[{'t': 'Ler o acórdão do Supremo Tribunal de Justiça, 08/02/2006 (dgsi.pt)', 'href': DGSI}],
         pista='Lê a passagem citada até ao fim.'),
 # ---------------------------------------------------------------- parte 2, pesar e escrever (50 minutos)
 # A informação nova que cria o conflito: as câmaras nas entradas, contestadas pela associação (os bens) e pela aluna que pergunta
 # quem vê e quando se apagam (a vida privada). O artigo 21.º, n.º 4, prepara o cartão 17.
 M.volta('Câmaras nas entradas?',
         'A direção propõe câmaras só nas entradas, com as imagens guardadas «para o caso de serem precisas». A associação '
         'responde: «Nas entradas, não se vê quem tira o telemóvel da mochila.» Uma aluna pergunta: «E quem vê as imagens? Quando '
         'se apagam?»',
         [('Lei n.º 58/2019, artigo 21.º, n.º 4', 'Quando cesse a finalidade que motivou o tratamento […] de dados pessoais, o '
                                                 'responsável pelo tratamento deve proceder à sua destruição ou anonimização.', 'lei58-21-4', None)],
         f'<a href="{DRE_LEI}">Diário da República</a>.', carimbo='Caso inventado.'),
 # A dúvida aberta, levada ao projeto (plano: «apagar no prazo combinado», piloto 17): uma palavra-passe não é um prazo. 06/11/2026
 # (revisão): o enunciado já não diz que se combinou apagar, para o «Falso» vir do artigo 21.º, n.º 4, e não da premissa.
 M.fazer('vf', 'Segura não é para sempre',
         'Caso inventado: gravaste uma entrevista para o projeto. Acabado o trabalho, podes guardá-la sem prazo, numa pasta com '
         'palavra-passe.',
         'O trabalho acabou. A gravação da entrevista está numa pasta com palavra-passe; como está segura, pode ficar lá sem prazo.',
         'Falso. A palavra-passe protege a gravação, mas não lhe dá uma finalidade nova. Acabado o trabalho, a lei manda «proceder '
         'à sua destruição ou anonimização».',
         3, 'transferir', 'prazo de conservação', v=False,
         citacoes=[('lei58-21-4', 'proceder à sua destruição ou anonimização')],
         fe='Guardar bem não é o mesmo que poder guardar. Quando a finalidade acaba, a lei manda «proceder à sua destruição ou '
            'anonimização». Volta ao artigo 21.º.',
         pista='Pergunta-te para que foi feita a gravação e se essa finalidade ainda existe.'),
 M.em_turma(DECIDE_Q, [
     ('O lado da associação', 'Os furtos aconteceram; nas entradas, «não se vê quem tira o telemóvel da mochila».'),
     ('O lado de quem discorda', f'Numa escola, as câmaras {M.citado("lei58-19-3", "só podem incidir sobre os perímetros externos e locais de acesso")} '
                                 'e espaços como laboratórios.'),
     ('Uma objeção', f'E as imagens das entradas? Acabada a finalidade, a lei manda {M.citado("lei58-21-4", "proceder à sua destruição ou anonimização")}.')],
     {'O que se faz': 'Decides outra vez e escolhes a razão que pesou.',
      'Quanto tempo': 'Três minutos; em turma, até treze.',
      'O que fica escrito': 'Nada em papel; a escolha fica nos artefactos.',
      'Se estás sozinho': 'Compara com a escolha do início e abre os três lados.'},
     prova=('A razão que pesou mais:', ('Os furtos', f'O «só» (19.º, n.º{NB}3)', f'O prazo (21.º, n.º{NB}4)')),
     prova_rot='A razão que pesou', intro='', nota=None),
 # A cadeia (plano, secção 2), no programa de presenças: cada frase com o seu papel numa justificação.
 M.fazer('emparelhar', 'Cada frase, o seu papel',
         'Caso inventado: o programa de presenças que guarda a localização. Liga cada frase ao seu papel numa justificação.',
         'Numa justificação sobre o programa de presenças, o que faz cada frase?',
         'Que o programa guarda a localização é um facto; o direito de conhecer a finalidade vem da Constituição; dizer que a '
         'localização está a mais liga os dois; e o que ainda não se sabe é o limite.',
         3, 'distinguir', 'facto, fonte, aplicação, limite',
         pares=[['O programa guarda onde está cada aluno, o dia todo.', 'O facto'],
                ['A Constituição dá o direito de conhecer a finalidade dos dados.', 'A fonte'],
                ['Para marcar presenças, a localização o dia todo está a mais.', 'A aplicação'],
                ['Falta saber quem consulta esses dados, e durante quanto tempo.', 'O limite']],
         fe='A confusão mais provável é trocar a aplicação pelo facto: o facto diz o que o programa guarda; a aplicação liga isso à '
            'finalidade e diz que está a mais. Pergunta a cada frase de onde vem.',
         pista='Pergunta a cada frase: aconteceu, está escrito numa lei, liga as duas coisas, ou diz o que ainda não se sabe?'),
 # Cadeia com o passo em falta (plano, secção 2: nas sessões 04 a 07, o aluno encontra o passo que falta). Na s04 faltava a
 # aplicação; aqui falta a fonte. 06/11/2026 (revisão): a cadeia passa à gravação da entrevista do cartão 17; a das salas dava a
 # resposta da charneira 2, logo a seguir. O p2 repete a cadeia, porque é ele que aparece na segunda tentativa e em «Só os que errei».
 escolha('O passo que falta',
         'Facto: a gravação da entrevista ficou guardada depois do trabalho. Aplicação: acabou a finalidade. Limite: falta saber se '
         'a pessoa aceitou outro uso. Escolhe a fonte que falta.',
         'A gravação da entrevista ficou guardada depois do trabalho, e a finalidade acabou; falta saber se a pessoa aceitou outro '
         'uso. Falta a fonte: escolhe-a.',
         f'A Lei n.º{NB}58/2019 manda destruir ou anonimizar esses dados.',
         [('A gravação ficou numa pasta protegida com palavra-passe.',
           'Isto é outro facto do caso, não uma regra. A fonte é o texto que diz o que fazer aos dados quando a finalidade acaba. '
           'Volta ao artigo 21.º.'),
          ('Quase toda a gente acaba por apagar as gravações antigas.',
           'Isto é um hábito, não uma regra que obrigue. A fonte é o texto de onde vem a regra que a aplicação usa. Volta ao '
           'artigo 21.º.')],
         'A aplicação diz que a finalidade acabou; a fonte é o texto que diz o que isso obriga a fazer: a Lei n.º 58/2019, artigo '
         '21.º, n.º 4.',
         4, 'aplicar', 'facto, fonte, aplicação, limite', pista='A fonte é o texto de onde vem a regra que a aplicação usa.'),
 # Charneira 2: a conclusão que não vai além das provas. Os erros esperados: a razão do cartaz, ou ler «podem» como «têm de».
 escolha('O que as provas permitem',
         'Escolhe a conclusão que não vai além do caso e da lei.',
         'Escolhe a conclusão que fica dentro do que o caso e os artigos mostram.',
         'Nas salas, não; nas entradas, falta ver se chega.',
         [('Nas salas, sim, porque quem não deve não teme.',
           'É a razão do cartaz, não uma prova. As câmaras «só podem incidir sobre os perímetros externos e locais de acesso» e '
           'espaços como laboratórios; a sala de aula não é nenhum deles. Separa o que se prova do que se repete.'),
          ('A escola tem de pôr câmaras nas entradas, já.',
           'A lei diz o que as câmaras podem filmar; não obriga a pô-las. E ninguém sabe ainda se as das entradas travam os furtos. '
           'Volta ao verbo do n.º 3.')],
         'Diz o que as provas mostram (a lei não deixa filmar as salas de aula) e deixa aberto o que falta saber: se as câmaras '
         'nas entradas chegam para os furtos.',
         3, 'aplicar', 'conclusão e provas',
         citacoes=[('lei58-19-3', 'só podem incidir sobre os perímetros externos e locais de acesso')],
         pista='Procura a conclusão que não acrescenta nada às provas.'),
 M.papel(PERGUNTA,
         ['A tua conclusão, por agora.',
          'Uma prova: um facto do caso e uma expressão exata, entre aspas, com o artigo.',
          'Uma dúvida que ainda tens.'],
         ['A conclusão responde à pergunta sem ir além das provas.',
          'A prova junta um facto a uma expressão exata, com o artigo.',
          'A dúvida, respondida, podia mudar a conclusão.'],
         '<p>Outro caso, inventado: um clube de xadrez pede o número do cartão de cidadão para uma inscrição.</p><ol>'
         '<li>Conclusão: para uma inscrição, o número parece a mais.</li>'
         f'<li>Prova: pedem o número do cartão; a Constituição dá o direito {M.citado("crp-35-1", "de conhecer a finalidade a que se destinam")} '
         'os dados (artigo 35.º, n.º 1).</li>'
         '<li>Dúvida: o regulamento do torneio exige-o?</li></ol>',
         'Num papel pequeno, sozinho e sem telemóvel.',
         relogio_min=12),
 M.levar(FRASE, ['Numa escola, as câmaras só podem filmar os acessos, o perímetro externo e espaços como laboratórios.',
                 'Acabada a finalidade, os dados não ficam «para o caso de».']),
]

# o lugar da certa em cada escolha (0, 1 ou 2), com a semente do motor: nunca o mesmo em mais de metade, nem três seguidos
LUGARES = (2, 0, 1, 0, 2, 1)

# O passo do projeto (plano, secção 3: «a nota de privacidade do teu projeto (que dados, para quê, quem vê, quando se apagam)»).
# O que se diz das gravações e dos contactos é o que a página do projeto já diz (cidadania/projeto/, «Ética: as pessoas que
# entrevistas», «Dados pessoais»).
DEPOIS = ('<article class="c"><p class="rot">O passo do teu projeto</p><p class="tit">A nota de privacidade do teu projeto</p>'
          '<p class="sub">No teatro-documento, usas entrevistas, gravações e notas sobre pessoas reais. Escreve, em papel, a nota de '
          'privacidade do teu projeto em quatro linhas: os dados que recolhes; para quê; quem os vê; quando se apagam. O que conta: cada '
          'dado tem uma finalidade; nada se recolhe «para o caso de»; quem vê fica dito com clareza (só tu, ou também a pessoa entrevistada); '
          'o prazo é uma data ou um momento do trabalho. Nada de gravações, fotografias, moradas ou contactos publicados.</p>'
          '<p class="ir"><a href="../../../projeto/#metodo">A ética das entrevistas, no enunciado da Pergunta Humana</a></p></article>')


def sessao():
    d = {
        'id': 'cidadania-m1-s05', 'chave': 'epi-cid-m1-s05', 'versao': '2026-11-06-molde', 'marca': 'CD', 'molde': L.MOLDE,
        'titulo': 'Sessão 05: Quem guarda os meus dados?', 'h1': 'Cidadania, módulo 1, sessão 05: Quem guarda os meus dados?',
        'modulo': {'n': 1, 'nome': 'Humanos', 'url': L.LENTE + 'cidadania/piloto/m1/'},
        'saida': 'cidadania/m1/sessoes/05/index.html',
        # 06/11/2026: a sessão 06 também passou ao molde final (decisões 166 a 168); a s05 leva à s06 nova.
        'seguinte': '../06/', 'seguinteRotulo': 'Sessão 06: Uma regra para quem perde',
        'fontes': M.ref('Lei n.º 58/2019, de 8 de agosto, artigos 19.º, n.os 3 e 4, e 21.º, n.º 4, no Diário da República. Constituição '
                        'da República Portuguesa, artigos 18.º, n.º 2, 26.º, n.º 1, e 35.º, n.º 1, no Diário da República. Acórdão do '
                        'Supremo Tribunal de Justiça de 8 de fevereiro de 2006, processo 05S3139, em dgsi.pt. Gravura: _A General Idea of '
                        'a Penitentiary Panopticon […]_ (1791), estampa de _The Works of '
                        'Jeremy Bentham_, vol. IV (Edimburgo, William Tait, 1843), Biblioteca da Universidade de Sevilha, via Internet '
                        'Archive, domínio público. O caso da sala 12, o do contacto dado para a visita, o do formulário, o da oficina, o do '
                        'programa de presenças, o da entrevista gravada e o do torneio de xadrez são inventados; o do Supremo Tribunal '
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
