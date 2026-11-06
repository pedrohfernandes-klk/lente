# Fonte da sessão 06 do M1 de Cidadania, «Uma regra para quem perde», na versão final do molde cidadania-2026-11 (plano do molde,
# secção 3, linha «06»; decisões 144 a 146, 152 a 155, 161 e 166 a 168). 06/11/2026: substitui a fonte do piloto de 31/10, que
# escrevia cidadania/piloto/m1-s06/ (essa página fica como está até ao pedido 3, que faz os redirecionamentos do piloto de uma vez);
# a chave epi-cid-m1-s06 é a mesma, e a versão sobe com preservarAnterior (cfg da família). Corre-se para escrever o .json ao lado;
# o .json é que o gerador (tools/licoes_lente.py) lê, e nunca se edita à mão. Os cartões montam-se com o ajudante comum
# tools/cidadania_molde.py; cada excerto de lei ou de acórdão vem do registo tools/cidadania_fontes.json (texto exato da fonte
# oficial, aberta a 6/11/2026, confirmado) e o ajudante recusa escrever um excerto que lá não esteja.
#
# 23 cartões (9 de ler, 14 de fazer), pela ordem e com os tempos da secção 2 do plano, como a s01; a ordem é fixa (cfg.aula) e a
# resposta certa de cada escolha fica no lugar pedido em LUGARES, calculado com a semente do motor. Cada exercício tem a sua pista,
# que não dá a resposta. O que só o docente faz vive no guia (tools/cidadania_piloto.py, GUIA['06']), nunca aqui.
#
# O caso do piloto (o delegado e os seis turnos) passa de «grupos» a turmas (A, B e C do 10.º ano) e a seis tardes de ensaio no
# auditório: a decisão 146 tira os grupos das instruções, e o validador só aceita «grupo» no texto de um caso inventado; com turmas,
# o R1 e o R2 do plano («acordasses no grupo C», «o grupo C não trabalhou») escrevem-se sem exceções. As seis sessões de câmara
# (M1 publicado, sessão 07) ficam como caso de transferência (cartão 14), com os seus três projetos.
#
# Fontes abertas a 6/11/2026, uma de cada vez (nada citado de memória):
# - Código do Procedimento Administrativo (anexo ao Decreto-Lei n.º 4/2015), artigos 9.º e 69.º, versão consolidada no Diário da
#   República Eletrónico (registo cpa-9, cpa-69-1);
# - Acórdão do Supremo Tribunal Administrativo de 24/10/2024, processo 0778/23.3BELRA, em dgsi.pt (registo sta-2024-*): o caso real
#   da sessão (decisão 161);
# - Imagem do Olha: Metropolitan Museum of Art, registo 410925 (API de dados abertos do museu: «Justice (Justicia) from The
#   Virtues», Philips Galle, «After Pieter Bruegel the Elder», editor Hieronymus Cock, «ca. 1559–60», «Engraving», 28.4(29),
#   «Harris Brisbane Dick Fund, 1928», «isPublicDomain»: true) e o ficheiro do museu no Wikimedia Commons (File:Justice (Justicia)
#   from The Virtues MET DP825752.jpg, 3682 × 2789, «CC0», doado pelo museu). O Olha mostra a gravura inteira, sem filtros nem cortes,
#   reduzida a 1400 × 1060 a partir do original do museu (img/cidadania/justica-galle-bruegel-inteira.webp); os cartões 6 e 7 levam
#   dois pormenores do mesmo ficheiro (a figura do centro e o canto de baixo, à esquerda), que herdam a licença. A figura do Olha vai
#   sem width e height, como a da s01: com eles, a gravura deitada (mais larga do que a coluna) ficava com a altura máxima e faixas
#   vazias por cima e por baixo, e o «i» longe da imagem (visto a 1366 px);
# - Conceito, «Ler mais»: John Rawls, _A Theory of Justice_ (1971), e o véu de ignorância, e Robert Nozick, _Anarchy, State, and
#   Utopia_ (1974), na Stanford Encyclopedia of Philosophy (entradas «John Rawls» e «Robert Nozick's Political Philosophy»); é a
#   mesma leitura do cartão de obra 7 do M1 publicado («Escolher sem saber o teu lugar»);
# - R1: _The Egg_, conto de Andy Weir: só a premissa, conferida pela sessão 03 no sítio do autor (galactanet.com, a 6/11/2026);
# - Graus de parentesco: Código Civil, artigo 1581.º, n.º 2 (texto consolidado do Diário da República, descarregado a 6/11/2026
#   pela sessão 02): os irmãos ficam no segundo grau da linha colateral (a conta é nossa, pela regra do artigo);
# - Vídeo (decisão 155): nenhum. Os candidatos do plano (The Ethics Centre; CrashCourse, filosofia, episódio 40) não foram vistos
#   por inteiro; ficam no guia, para o docente decidir.
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
ART9 = M.registo()['cpa-9']['texto']

IMG = '../../../../img/cidadania/justica-galle-bruegel-inteira.webp'
ALT = ('Gravura a preto e branco, inteira, com a margem do papel. Ao centro, uma mulher de olhos vendados, de pé sobre uma base com uma palavra '
       'em latim, segura uma espada e uma balança, rodeada de homens com alabardas. À direita, homens escrevem em livros, numa sala; à '
       'esquerda e ao fundo, castigos: um homem deitado e preso a um banco, um homem pendurado por uma corda, forcas, rodas no alto '
       'de postes e uma fogueira, com multidões a ver. Por baixo, duas linhas em latim.')
MET = 'https://www.metmuseum.org/art/collection/search/410925'
CREDITO = ('Philips Galle, segundo Pieter Bruegel, o Velho, <i>Justice (Justicia) from The Virtues</i>; editor: Hieronymus Cock. '
           'The Metropolitan Museum of Art, 28.4(29). '
           f'<a href="{MET}">Registo de origem</a>. Domínio público; a imagem do museu é CC0.')
ROTULO_I = 'Créditos da gravura'
PORMENOR = 'Pormenor de <i>Justicia</i>, cerca de 1559 a 1560.'
VER_CENTRO = ('<img src="../../../../img/cidadania/justica-galle-bruegel-centro.webp" alt="Pormenor: a figura do centro, uma mulher de '
              'olhos vendados com uma espada na mão esquerda e uma balança na direita, entre homens com alabardas." width="960" height="576">'
              f'<figcaption class="ver-leg">{PORMENOR}</figcaption>')
VER_BANCO = ('<img src="../../../../img/cidadania/justica-galle-bruegel-banco.webp" alt="Pormenor do canto de baixo, à esquerda: um '
             'homem deitado e preso a um banco; outro deita-lhe um líquido na boca com um jarro; à volta, homens de pé, e um deles escreve '
             'num livro." width="960" height="665">'
             f'<figcaption class="ver-leg">{PORMENOR}</figcaption>')
DRE_CPA = 'https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/2015-105602322'
DGSI = 'https://www.dgsi.pt/jsta.nsf/35fbbbf22e1bb1e680256f8e003ea931/dfbeca2f658ff52680258c1f00505dc4?OpenDocument'
PERGUNTA = 'Uma regra é justa se quem a faz ganha com ela?'
DECIDE_Q = 'A regra do Gonçalo pode ficar?'
FRASE = 'Uma regra justa é a que consegues explicar a quem perde com ela.'
SUMARIO = ('[…] não basta que se demonstre a ilegalidade da intervenção do autarca num procedimento administrativo em que são '
           'interessados familiares seus, sendo necessário que se demonstre que essa intervenção foi determinada intencionalmente com o '
           'propósito de obter uma vantagem patrimonial indevida.')


def escolha(rot, p, p2, certa, erradas, f, minutos, tipo, conceito, **extra):
    """Uma escolha de três opções; a certa vai para o lugar de LUGARES (preenchido em sessao())."""
    c = M.fazer('escolha', rot, p, p2, f, minutos, tipo, conceito, **extra)
    c['_certa'], c['_erradas'] = M.ref(certa), [(M.ref(o), M.ref(e)) for o, e in erradas]
    return c


CARTOES = [
 # ---------------------------------------------------------------- parte 1, ver antes de concluir (60 minutos)
 # O caso do delegado vem do piloto (s06, cartão 1), reescrito: turmas em vez de grupos (decisão 146) e sem a resposta no caso.
 M.abre('Uma regra para quem perde',
        f'ver e ler (60{NB}min), pausa (10{NB}min), pesar e escrever (50{NB}min) e o teu projeto (45{NB}min).',
        f'A escola tem seis tardes no auditório para as turmas A, B e C do 10.º{NB}ano ensaiarem as peças. '
        f'Na reunião de delegados, o Gonçalo, do 10.º{NB}A, propõe a regra: primeiro, a turma com o guião mais adiantado. É a dele. '
        'A regra passa com dois votos contra um.',
        PERGUNTA),
 M.decide(DECIDE_Q, [
     ('Quem acha que sim', 'A regra é clara e premeia quem trabalhou. E dois delegados em três votaram sim.'),
     ('Quem acha que não', 'Quem propôs a regra é quem ganha com ela. As outras turmas podem duvidar de que o Gonçalo tenha pensado nelas.'),
     ('Uma objeção', 'E se a regra for boa, mesmo vinda de quem ganha? Mudaria alguma coisa se outro delegado a propusesse?')]),
 # R1: a obra da sessão 03 (The Egg, de Andy Weir) outra vez, com um item novo: a regra julgada de cada lugar (plano, secção 3).
 M.recupera(escolha(
     'Se acordasses noutra turma',
     f'No conto _The Egg_, de Andy Weir (sessão{NB}03), o homem descobre um segredo sobre as outras vidas. De onde julgarias a regra '
     'do Gonçalo?',
     f'Lembra-te do fim de _The Egg_, da sessão{NB}03. Se fosses o homem do conto, de onde julgarias a regra do Gonçalo?',
     'Também do lugar da turma que fica para o fim.',
     [('Do lugar do Gonçalo, que teve o trabalho de a propor.',
       'O conto não te põe só no lugar de quem propõe: põe-te em todas as vidas. Imagina que acordas na turma que ensaia em último lugar. '
       'A regra ainda te parece boa?'),
      ('Pelo voto: se dois em três a aprovaram, está julgada.',
       'O voto diz quantos aceitam a regra; o conto pede outra coisa: que a julgues de cada lugar. Imagina que acordas na turma que '
       'votou contra.')],
     'No conto, quem julga pode vir a viver qualquer vida. Se pudesses acordar na turma que ensaia em último lugar, a regra teria de te '
     'parecer aceitável também de lá. É a pergunta de hoje, vista de outro lugar.',
     3, 'aplicar', 'pôr-se no lugar do outro', pista='Lembra-te do que o homem do conto descobre no fim.')),
 # R2: acusação de facto ou opinião (sessão 04), um item novo sobre o 10.º C. Falso (os V/F da sessão são F, F, V).
 M.recupera(M.fazer(
     'vf', 'Facto ou opinião',
     f'Caso inventado: no corredor, alguém diz «O 10.º{NB}C não trabalhou nada este período». É uma opinião: discute-se, não precisa '
     'de prova.',
     f'«O 10.º{NB}C não trabalhou nada este período» é só uma opinião, que ninguém tem de provar.',
     'Falso. Dizer que uma turma não trabalhou afirma um facto concreto, verdadeiro ou falso: é uma «acusação de facto», e tem de se '
     f'provar. «O 10.º{NB}C trabalha mal» já seria uma opinião. É o que viste na sessão{NB}04.',
     4, 'distinguir', 'acusação de facto e opinião', v=False,
     fe='«Não trabalhou» diz que uma turma concreta deixou de fazer uma coisa concreta: isso prova-se, ou não. Uma opinião discute-se. '
        f'Volta à sessão{NB}04, à diferença entre opinião e «acusação de facto».',
     pista='Pergunta-te o que seria preciso para saber se a frase é verdade.'),
     origem='cidadania/m1/sessoes/04/'),
 M.olha('Uma gravura cheia de gente', 'Olha primeiro para a gravura inteira; só depois para a figura do centro.',
        M.figura(IMG, ALT, CREDITO, '<i>Justicia</i> (a Justiça), da série <i>As Virtudes</i>, gravura segundo Pieter Bruegel, o Velho, '
                 'cerca de 1559 a 1560.', artefacto='A Justiça, gravura de Philips Galle segundo Bruegel, cerca de 1559',
                 rotulo_i=ROTULO_I)),
 escolha('O que a figura mostra',
         'Olha para a figura do centro. O que se vê nela, sem acrescentar nada?',
         'Descreve a figura do centro só com o que a gravura mostra.',
         'Olhos vendados, uma espada numa mão e uma balança na outra.',
         [('Olhos vendados: por isso, não vê quem está a julgar.',
           'A venda vê-se; «por isso, não vê quem está a julgar» é uma leitura do símbolo, que a figura não mostra. Olha só para o que '
           'ela tem.'),
          ('Olhos vendados, uma espada numa mão e um livro na outra.',
           'Olha outra vez para a mão que não segura a espada: o que pende dela tem dois pratos. Descreve só o que lá está.')],
         'Vê-se uma mulher de olhos vendados, com uma espada numa mão e uma balança na outra, entre homens com alabardas. O que a venda '
         'quer dizer já é uma leitura do símbolo, que a figura não mostra.',
         3, 'distinguir', 'observar', ver=VER_CENTRO, pista='Confere na figura cada parte da opção: vê-se tudo o que ela diz?'),
 M.fazer('emparelhar', 'Imagem, legenda ou nenhuma',
         'Liga cada frase ao sítio onde se apoia: na gravura, na legenda ou em nenhuma das duas.',
         'Para cada frase: vê-se na gravura, só a legenda o diz ou nenhuma das duas o prova?',
         'O homem preso ao banco vê-se; a série das virtudes, só a legenda o diz; o que pensava quem a desenhou, nem a imagem nem a '
         'legenda o mostram. Mostrar uma cena não é aprová-la.',
         3, 'distinguir', 'imagem e legenda', ver=VER_BANCO,
         pares=[['Um homem está deitado e preso a um banco.', 'Vê-se na gravura'],
                ['A gravura faz parte de uma série sobre as virtudes.', 'Só a legenda o diz'],
                ['Quem a desenhou achava justo o que se faz à volta.', 'Nenhuma das duas o prova']],
         fe='A confusão mais provável é tomar o que a gravura mostra pelo que o autor pensava: mostrar uma cena não é aprová-la. Volta '
            'à imagem e à legenda e vê o que cada uma diz.',
         pista='Para cada frase, procura-a primeiro na imagem e depois na legenda.'),
 M.le('O que se pede a quem decide', 'O que a lei pede a quem decide pela Administração Pública.',
      [(f'Artigo{NB}9.º', ART9, 'cpa-9', 'a9')],
      f'Código do Procedimento Administrativo, no <a href="{DRE_CPA}">Diário da República</a>.',
      mais=(M.lei([(f'Artigo 69.º, n.º{NB}1', '[…] não podem intervir em procedimento administrativo […] nos seguintes casos: a) '
                    'Quando nele tenham interesse […] b) Quando […] nele tenham interesse […] algum parente […] até ao segundo grau da '
                    'linha colateral […]', 'cpa-69-1', None)], f'<a href="{DRE_CPA}">Diário da República</a>')
            + '<p class="glossa"><b>Segundo grau da linha colateral</b>: irmãos (Código Civil, artigo 1581.º).</p>')),
 M.fazer('sublinhar', 'Aquilo em que se confia',
         'No artigo 9.º, toca na palavra que diz o que a Administração tem de preservar; depois, toca na palavra que diz em que os outros têm de poder confiar.',
         'O artigo 9.º pede que se preserve uma coisa e que os outros confiem nela. Toca na palavra que a nomeia em cada um dos dois pedidos.',
         '«Isenção»: decidir sem se deixar levar por interesses próprios. O artigo 9.º pede que se preserve e que os outros possam '
         'confiar nela.',
         3, 'reconhecer', 'isenção', frase=ART9, certas=[39, 45], fonte='cpa-9', l='a9',
         fe='A confusão mais provável é tocar em «confiança» ou em «imparcial»: «confiança» é o que os outros sentem, não aquilo em que '
            'confiam. Volta ao fim do artigo.',
         pista='Pergunta-te o que a Administração tem de preservar.'),
 escolha('Quem decide e quem ganha',
         'O artigo 69.º afasta quem decide na Administração Pública em certos casos. O que tem a regra do Gonçalo em comum com eles?',
         'Nos casos do artigo 69.º, quem decide não pode intervir. Em que se parece com eles a regra do Gonçalo?',
         'Quem propõe a regra ganha com o que se decide.',
         [('A regra foi aprovada só por dois dos três delegados.',
           'Dois votos em três aprovam a regra; o artigo 69.º não fala de votos, fala de quem tem interesse naquilo que se decide. '
           'Relê a alínea a).'),
          ('O critério do guião adiantado é difícil de medir.',
           'Talvez seja difícil de medir, mas o artigo 69.º não trata da clareza do critério: trata de quem decide ter interesse no que '
           'se decide. Relê a alínea a).')],
         'Nos casos do artigo 69.º, quem decide tem interesse naquilo que se decide. Com a regra do Gonçalo passa-se o mesmo: a turma '
         'dele fica à frente. Uma reunião de delegados não é a Administração Pública, mas a pergunta é a mesma.',
         4, 'aplicar', 'conflito de interesses',
         cita='[…] não podem intervir em procedimento administrativo […] nos seguintes casos: a) Quando nele tenham interesse, por si […]',
         fonte='cpa-69-1', pista='Lê a alínea a) e procura quem tem interesse.'),
 M.fazer('vf', 'Um júri com um irmão',
         f'Caso inventado: um membro do júri de um concurso da câmara é irmão (2.º{NB}grau da linha colateral) de um candidato. Pode '
         'ficar, desde que não avalie o irmão.',
         'Um jurado de um concurso da câmara é irmão de um dos candidatos. Basta-lhe não dar nota ao irmão para continuar no júri.',
         'Falso. Um irmão é parente no segundo grau da linha colateral, e nesse caso quem decide não pode intervir «em procedimento '
         'administrativo»: no concurso inteiro, não só na nota do irmão. Cada nota que dá aos outros também mexe no lugar dele.',
         3, 'aplicar', 'impedimento', v=False,
         cita=('[…] não podem intervir em procedimento administrativo […] b) Quando […] nele tenham interesse o seu cônjuge […] algum '
               'parente ou afim em linha reta ou até ao segundo grau da linha colateral […]'),
         fonte='cpa-69-1', citacoes=[('cpa-69-1', 'em procedimento administrativo')],
         fe='Não chega deixar de avaliar o irmão: num concurso, a nota de cada candidato mexe no lugar de todos. O artigo afasta quem '
            'decide do procedimento inteiro, não de uma nota. Relê a alínea b).',
         pista='Relê a alínea b): de onde afasta o artigo quem decide?'),
 # Charneira 1: o limite. Uma boa regra não apaga o problema de quem a propõe ganhar com ela (artigo 9.º, «confiança nessa isenção»).
 M.fazer('vf', 'Se a regra for a melhor',
         'Imagina que a regra do Gonçalo era mesmo a melhor para as três turmas. Mesmo assim, havia um problema em ter sido ele a '
         'propô-la.',
         'Ainda que a regra do Gonçalo fosse a melhor, continuava a haver um problema por ser ele, que ganha com ela, a propô-la.',
         'Verdadeiro. O artigo 9.º não pede só decisões certas: pede também a «confiança nessa isenção». Quando quem propõe ganha com a '
         'regra, os outros ficam com razões para duvidar, mesmo que ela seja boa.',
         4, 'aplicar', 'conflito de interesses', v=True, citacoes=[('cpa-9', 'confiança nessa isenção')],
         fe='Uma boa regra não apaga a dúvida: o artigo 9.º pede também a «confiança nessa isenção». Quem ganha com a regra que propõe '
            'dá aos outros razões para duvidar. Relê o fim do artigo 9.º.',
         pista='Relê o artigo 9.º até ao fim e conta o que ele pede.'),
 # Conceito: escolher sem saber o lugar (Rawls, cartão de obra 7 do M1 publicado); Nozick em «Ler mais». As três posições
 # paralelas vão em tabela (decisão 152).
 M.conceito('Escolher sem saber o lugar',
            '<p>O Gonçalo sabia onde estava. E se não soubesse?</p>',
            '<table class="tabela"><thead><tr><th scope="col">Se ficas</th><th scope="col">Convém-te</th></tr></thead><tbody>'
            f'<tr><td data-th="Se ficas">no 10.º{NB}A</td><td data-th="Convém-te">o guião mais adiantado primeiro</td></tr>'
            '<tr><td data-th="Se ficas">na turma mais atrasada</td><td data-th="Convém-te">não ficar para o fim</td></tr>'
            '<tr><td data-th="Se ficas">num lugar que não sabes</td><td data-th="Convém-te">uma regra boa em qualquer lugar</td></tr>'
            '</tbody></table>',
            'Escolher sem saber o lugar', 'Escolher a regra antes de saberes se ganhas ou perdes.',
            '<p>Não é sorteio: escolhe-se às cegas a regra, não quem ganha.</p>',
            mais=('<p>A ideia é de John Rawls (<i>Uma Teoria da Justiça</i>, 1971): escolher as regras atrás de um véu de ignorância, '
                  'sem saber o lugar que nos calha. Robert Nozick respondeu (<i>Anarquia, Estado e Utopia</i>, 1974): uma repartição é '
                  'justa se vier de aquisições e transferências legítimas, feitas livremente, não de um padrão escolhido à partida.</p>')),
 # Transferir 1: as seis sessões de câmara (M1 publicado, sessão 07, «Exemplo»), com os critérios do piloto (cartão 4).
 M.fazer('emparelhar', 'Cada regra, o seu efeito',
         'Caso inventado: seis sessões de câmara para três projetos. O A tem quatro cenas prontas; o C perdeu uma sessão porque faltou '
         'material. Liga cada regra ao seu efeito.',
         'Três projetos repartem seis sessões de câmara: o A vai adiantado e o C perdeu uma sessão. Liga cada regra ao efeito que tem.',
         'Duas para cada um não compensa a perda do C; mais para quem perdeu compensa-a; primeiro as cenas prontas põe o A à frente; o '
         'sorteio não escolhe ninguém. Escolher a regra é escolher quem perde.',
         3, 'transferir', 'critérios de repartir',
         pares=[['Duas sessões para cada projeto.', 'A perda do C fica por compensar.'],
                ['Mais sessões para quem perdeu material.', 'O C recupera o que lhe faltou.'],
                ['Primeiro, quem tem mais cenas prontas.', 'O A filma antes dos outros.'],
                ['A ordem tira-se à sorte.', 'Qualquer um pode ficar para o fim.']],
         fe='A confusão mais provável é achar que dar o mesmo a todos compensa a perda do C: com duas sessões para cada um, o C continua '
            'com menos uma. Volta às regras e pergunta, em cada uma, quem fica à frente.',
         pista='Em cada regra, pergunta-te quem fica à frente e quem fica para trás.'),
 # Decisão 161: o caso real, com fonte oficial aberta (dgsi.pt). Cita-se só o que o acórdão diz: o sumário, e, no retorno, o que a
 # primeira sentença já reconhecera («situação de isenção e imparcialidade», «desde logo»). Os factos vêm da matéria de facto provada
 # (pontos 2, 7, 9, 12, 14, 16 e 18 a 20) e a decisão, do ponto IV (confirma a sentença do TAF de Leiria: não houve perda de mandato).
 escolha('Um caso real',
         'Caso real (Supremo Tribunal Administrativo, 2024): uma vereadora abriu um concurso da câmara a que concorreram a filha, o irmão '
         'e a cunhada. Não perdeu o mandato. Porquê?',
         'Em 2024, o Supremo Tribunal Administrativo decidiu que uma vereadora não perdia o mandato, embora a filha, o irmão e a cunhada '
         'tivessem concorrido ao concurso que ela abriu. Porquê?',
         'Não se provou que quisesse dar-lhes uma vantagem indevida.',
         [('Declarou-se impedida, embora só no fim do concurso.',
           'Não foi isso que pesou: o tribunal de Leiria, na primeira sentença, até a censurou por não se ter declarado impedida «desde '
           'logo». Lê o que o sumário diz que era necessário.'),
          ('Os familiares não chegaram a entrar para a câmara.',
           'Entraram: os três assinaram contrato com o município em janeiro de 2019. O tribunal decidiu por outra razão. Lê o que o '
           'sumário diz que era necessário.')],
         'Para perder o mandato, não chegava intervir num concurso a que concorriam familiares: era preciso provar que quis obter uma «vantagem '
         'patrimonial indevida». Na primeira sentença, o tribunal de Leiria já reconhecera que não estava em «situação de isenção e '
         'imparcialidade»; '
         'faltou a outra prova.',
         4, 'transferir', 'conflito de interesses e prova',
         cita=SUMARIO, fonte='sta-2024-sumario',
         citacoes=[('sta-2024-sumario', 'vantagem patrimonial indevida'), ('sta-2024-isencao', 'situação de isenção e imparcialidade'),
                   ('sta-2024-isencao', 'desde logo')],
         liga=[{'t': 'Ler o acórdão do Supremo Tribunal Administrativo, 24/10/2024 (dgsi.pt)', 'href': DGSI}],
         pista='Lê no sumário o que não basta e o que é necessário.'),
 # ---------------------------------------------------------------- parte 2, pesar e escrever (50 minutos)
 M.volta(f'A delegada do 10.º{NB}C pede a palavra',
         f'Na reunião seguinte, a Beatriz, delegada do 10.º{NB}C, lembra que a turma dela perdeu duas tardes com as obras no '
         f'auditório. Propõe outra regra: mais tardes para o 10.º{NB}C. O Gonçalo responde: «A minha regra '
         'premeia quem trabalhou. Não a fiz para mim.»',
         carimbo='Caso inventado.'),
 M.fazer('ordenar', 'Sem saber o lugar',
         'A reunião vai decidir outra vez. Põe por ordem os passos para escolher a regra sem saber o lugar.',
         'Ordena o que a reunião faz para escolher a regra das tardes sem que ninguém saiba a turma que lhe calha.',
         'Primeiro as regras em cima da mesa; depois a escolha sem saber o lugar; depois a voz de quem perde; no fim, a revisão. Quem '
         'propôs uma regra também a escolhe às cegas.',
         3, 'aplicar', 'escolher sem saber o lugar',
         passos=['Juntar as regras propostas, a do Gonçalo e a da Beatriz.',
                 'Escolher uma sem saber a turma que calha a cada um.',
                 'Ouvir a objeção da turma que fica a perder.',
                 'Rever a regra, se a objeção for boa.'],
         fe='A confusão mais provável é ouvir quem perde antes de escolher: só há quem perde depois de haver uma regra. Começa por juntar '
            'as regras.',
         pista='Pergunta-te o que tem de existir antes de alguém poder perder.'),
 M.em_turma(DECIDE_Q, [
     ('O lado do Gonçalo', f'O artigo 9.º pede que se considerem {M.citado("cpa-9", "todos e apenas os interesses relevantes")}. Um '
                           'guião adiantado é um critério verificável.'),
     ('O lado da Beatriz', f'Quem decide deve preservar a {M.citado("cpa-9", "confiança nessa isenção")}. E o 10.º{NB}C perdeu duas '
                           'tardes sem culpa.'),
     ('Uma objeção', 'Também a Beatriz propõe uma regra que favorece a turma dela. Quem devia escolher?')],
     {'O que se faz': 'Decides outra vez e escolhes a razão que pesou.',
      'Quanto tempo': 'Três minutos; em turma, até treze.',
      'O que fica escrito': 'Nada em papel; a escolha fica nos artefactos.',
      'Se estás sozinho': 'Compara com a escolha do início e abre os três lados.'},
     prova=('A razão que pesou mais:', ('O guião adiantado', f'As tardes perdidas do 10.º{NB}C', f'A confiança (artigo{NB}9.º)')),
     prova_rot='A razão que pesou', intro='', nota=None),
 # Conceito espaçado (origem): facto, regra ou razão, a distinção da sessão 01 («Facto, regra ou razão», cartão 19).
 M.fazer('emparelhar', 'Facto, regra ou razão',
         'Liga cada frase ao que ela é numa justificação.',
         'Facto, regra ou razão de uma das partes: o que é cada frase?',
         'As tardes perdidas são um facto do caso; o artigo 9.º é uma regra escrita numa lei, que obriga a Administração Pública; «Não a '
         'fiz para mim» é a razão de quem propôs a regra, que ainda tem de ser pesada.',
         3, 'distinguir', 'relato e princípio',
         pares=[[f'O 10.º{NB}C perdeu duas tardes de ensaio com as obras.', 'Um facto do caso'],
                ['«A Administração Pública deve tratar de forma imparcial aqueles que com ela entrem em relação»',
                 'Uma regra escrita numa lei'],
                ['«Não a fiz para mim.»', 'A razão de uma das partes']],
         citacoes=[('cpa-9', 'A Administração Pública deve tratar de forma imparcial aqueles que com ela entrem em relação')],
         origem='cidadania/m1/sessoes/01/',
         fe='A confusão mais provável é tomar a razão do Gonçalo por facto: «Não a fiz para mim» diz o que ele afirma, não o que se '
            f'provou. É a distinção da sessão{NB}01: facto, regra escrita, razão de alguém.',
         pista='Uma regra está escrita e obriga quem decide; uma razão é de alguém.'),
 # Cadeia com o passo em falta (plano, secção 2: nas sessões 04 a 07, o aluno encontra o passo que falta). Na s04 faltava a
 # aplicação; aqui falta o limite. 06/11/2026 (revisão, bloqueante): a justificação é a da Beatriz (as tardes perdidas), e não a da
 # dúvida sobre quem propôs, que escrevia a resposta da charneira 2 no cartão de cima; «pesar» e «dúvida» ficam fora deste cartão.
 escolha('O passo que falta',
         f'Facto: o 10.º{NB}C perdeu duas tardes com as obras. Fonte: o artigo 9.º, «todos e apenas os interesses relevantes». '
         'Aplicação: a perda conta. Falta o limite.',
         'Nesta justificação há facto, fonte e aplicação; falta a frase que diz até onde vai a conclusão. Escolhe-a.',
         'Isto não decide sozinho quem deve ensaiar primeiro.',
         [('Por isso, a Beatriz tem razão e o Gonçalo está errado.',
           'Isto vai além das provas: um interesse relevante entra na conta, não a fecha. O limite diz o que a justificação ainda não '
           'prova. Volta à justificação.'),
          (f'A Beatriz falou na reunião como delegada do 10.º{NB}C.',
           'Isso é mais um facto do caso, não um limite. O limite diz até onde vai a conclusão. Volta à justificação.')],
         'O limite diz até onde vai a conclusão: a perda das tardes conta, mas não decide sozinha quem ensaia primeiro.',
         4, 'aplicar', 'facto, fonte, aplicação, limite',
         pista='Pergunta-te o que a justificação ainda deixa em aberto.'),
 # Charneira 2: a conclusão que não vai além das provas; os erros esperados são supor a intenção e tomar o voto por justiça.
 escolha('O que as provas permitem',
         'Escolhe a conclusão que diz o que as provas permitem, sem ir além delas.',
         'Escolhe a conclusão que fica dentro do que o caso e o artigo 9.º mostram.',
         'Vinda de quem ganha com ela, a regra deixa dúvidas; falta pesá-la.',
         [('A regra é injusta, porque o Gonçalo quis favorecer a turma.',
           'Nenhum material mostra o que o Gonçalo quis: só que a turma dele ganha com a regra. Uma intenção não se supõe; prova-se. '
           'Separa o que aconteceu do que alguém supõe.'),
          ('A regra é justa, porque a maioria dos delegados a aprovou.',
           'O voto diz quantos a aceitaram, não se é justa: a maioria também pode aprovar uma regra que deixa alguém para trás. Volta à '
           'dúvida sobre quem a propôs.')],
         f'Diz o que se sabe (quem propôs ganha com a regra, e isso tira confiança) e deixa aberto o que falta: se a regra, pesada com as '
         f'tardes perdidas do 10.º{NB}C, é justa.',
         3, 'aplicar', 'conclusão e provas',
         pista='Procura a conclusão que não acrescenta nada às provas.'),
 M.papel(PERGUNTA,
         ['A tua conclusão, por agora.',
          'Uma prova: um facto do caso e uma expressão exata, entre aspas, com o artigo.',
          'Uma dúvida que ainda tens.'],
         ['A conclusão responde à pergunta sem ir além das provas.',
          'A prova junta um facto a uma expressão exata, com o artigo.',
          'A dúvida, respondida, podia mudar a conclusão.'],
         # o exemplo mostra só a forma, noutro caso e com outro texto (a Declaração, artigo 1.º), sem a conclusão nem a prova de hoje
         f'<p>Caso inventado: na cantina, os do 12.º{NB}ano passam sempre à frente na fila.</p><ol>'
         '<li>Conclusão: ser mais velho não explica a vantagem a quem espera.</li>'
         f'<li>Prova: todos esperam pela mesma refeição; todos nascem {M.citado("dudh-1", "iguais em dignidade e em direitos")} '
         '(Declaração, artigo 1.º).</li>'
         '<li>Dúvida: há outra razão, como um horário mais curto?</li></ol>',
         'Num papel pequeno, sozinho e sem telemóvel.',
         relogio_min=12),
 M.levar(FRASE, ['Quem ganha com uma regra dá aos outros razões para duvidar dela.',
                 'Escolher sem saber o lugar obriga a pensar em quem perde.']),
]

# o lugar da certa em cada escolha (0, 1 ou 2), com a semente do motor: nunca o mesmo em mais de metade, nem três seguidos
LUGARES = (1, 2, 0, 1, 0, 2)

# O passo do projeto (plano, secção 3: «do material ao guião, cada fala com fonte (#84)»). A página do projeto diz: «No guião e no
# dossiê, tornar localizáveis as fontes das falas, dados e documentos usados.» (cidadania/projeto/, «Fases»).
DEPOIS = ('<article class="c"><p class="rot">O passo do teu projeto</p><p class="tit">Do material ao guião</p>'
          '<p class="sub">No teatro-documento, cada fala vem do que investigaste. Hoje, escreves em papel as primeiras falas do teu guião, '
          'a partir do material que já tens: entrevistas, documentos, fontes. Ao lado de cada fala, a fonte: quem o disse ou onde está '
          'escrito, e como se reencontra. O que conta: cada fala tem uma fonte que se pode reencontrar; o que é teu (a ligação entre as '
          'falas) distingue-se do que é citado; uma fala sem fonte sai, ou fica marcada como pergunta.</p>'
          '<p class="ir"><a href="../../../projeto/#fases">As fontes das falas, no enunciado da Pergunta Humana</a></p></article>')


def sessao():
    d = {
        'id': 'cidadania-m1-s06', 'chave': 'epi-cid-m1-s06', 'versao': '2026-11-06-molde', 'marca': 'CD', 'molde': L.MOLDE,
        'titulo': 'Sessão 06: Uma regra para quem perde', 'h1': 'Cidadania, módulo 1, sessão 06: Uma regra para quem perde',
        'modulo': {'n': 1, 'nome': 'Humanos', 'url': L.LENTE + 'cidadania/piloto/m1/'},
        'saida': 'cidadania/m1/sessoes/06/index.html',
        'seguinte': '../../../piloto/m1-s07/', 'seguinteRotulo': 'Sessão 07: Nove contra dois',
        'fontes': M.ref('Código do Procedimento Administrativo (anexo ao Decreto-Lei n.º 4/2015, de 7 de janeiro), artigos 9.º e 69.º, '
                        'n.º 1, na versão consolidada do Diário da República. Código Civil, artigo 1581.º, n.º 2, na versão consolidada do '
                        'Diário da República. Declaração Universal dos Direitos Humanos, artigo 1.º, na transcrição portuguesa do UNRIC. '
                        'Acórdão do Supremo Tribunal Administrativo de 24 de outubro de 2024, processo 0778/23.3BELRA, em dgsi.pt. '
                        'Imagem: Philips Galle, segundo Pieter Bruegel, o Velho, _Justice (Justicia) from The Virtues_, cerca de 1559 a '
                        '1560, The Metropolitan Museum of Art, domínio público (imagem CC0). John Rawls, _A Theory of Justice_ (1971), e '
                        'Robert Nozick, _Anarchy, State, and Utopia_ (1974), segundo a Stanford Encyclopedia of Philosophy. _The Egg_, '
                        f'conto de Andy Weir. O caso do Gonçalo e da Beatriz, o do 10.º{NB}C no corredor, o do júri da câmara, o das seis '
                        f'sessões de câmara (escrito para a sessão{NB}07 do M1 publicado) e o da fila da cantina são inventados; o do Supremo '
                        'Tribunal Administrativo é real.'),
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
