# Fonte da sessão 09 do M1 de Cidadania, «Muitas vozes, uma escola», na versão final do molde cidadania-2026-11 (plano do molde,
# secção 3, linha «09»; decisões 144 a 146, 152 a 155, 161 e 166 a 168 e 174). 07/11/2026: substitui a fonte do piloto de 31/10, que
# escrevia cidadania/piloto/m1-s09/ (essa página fica como está até ao pedido 3, que faz os redirecionamentos do piloto de uma vez); a
# chave epi-cid-m1-s09 é a mesma, e a versão sobe com preservarAnterior (cfg da família). Corre-se para escrever o .json ao lado; o
# .json é que o gerador (tools/licoes_lente.py) lê, e nunca se edita à mão. Os cartões montam-se com o ajudante comum
# tools/cidadania_molde.py; cada excerto vem do registo tools/cidadania_fontes.json (texto exato da fonte oficial, aberta a
# 7/11/2026, confirmado) e o ajudante recusa escrever um excerto que lá não esteja.
#
# 23 cartões (9 de ler, 14 de fazer), pela ordem e com os tempos da secção 2 do plano, como a s01 a s08; a ordem é fixa (cfg.aula) e a
# resposta certa de cada escolha fica no lugar pedido em LUGARES, calculado com a semente do motor. Cada exercício tem a sua pista,
# que não dá a resposta. O que só o docente faz vive no guia (tools/cidadania_piloto.py, GUIA['09']), nunca aqui. Na cadeia (cartões
# 19 a 21), o apoio retira-se como o plano pede para as sessões 08 a 10: a charneira 2 pede a conclusão que vai além das provas.
# Do piloto ficam o caso do intervalo (agora com a Mariana desde o Abre), a fotografia de Hine, o estereótipo que parece elogio
# (agora como charneira 1, presa ao artigo 13.º, n.º 2) e a pergunta pela religião (artigo 41.º, n.º 3); sai o cartão 13 do piloto,
# que repetia a s03 e a s06 (plano), e sai o vídeo do TED-Ed (decisão 155: não foi visto por inteiro).
#
# Fontes abertas a 7/11/2026, uma de cada vez (nada citado de memória):
# - Constituição, artigos 13.º, n.º 2, e 41.º, n.º 3, versão consolidada no Diário da República Eletrónico (registo crp-13-2, já
#   conferido na s03 e igual hoje, e crp-41-3); a grafia é a da fonte;
# - Convenção sobre os Direitos da Criança, artigo 30.º, na tradução portuguesa anexa à Resolução da Assembleia da República
#   n.º 20/90, no Diário da República Eletrónico (registo cdc-30); as Retificações n.º 1/91 e n.º 8/91 não tocam no artigo 30.º. O
#   cartão 8 traz o artigo inteiro, o início no «Ler mais» e o resto à vista (07/11/2026, decisão 179: o validador aceita «grupo»
#   nos excertos de lei registados e copiados letra a letra; antes cortava-se «conjuntamente com membros do seu grupo», pela
#   decisão 146);
# - O caso real (decisão 161): Tribunal Europeu dos Direitos Humanos, _Osmanoğlu e Kocabaş c. Suíça_, queixa n.º 29086/12, acórdão
#   de 10/01/2017, no HUDOC (texto inglês, 001-170436). O cartão 15 conta, por palavras nossas e sem citar (não há versão portuguesa),
#   só o que o acórdão diz: aulas de natação mistas obrigatórias na escola primária (§ 9), pais muçulmanos que recusaram mandar as
#   filhas (§ 9), as autoridades ofereceram o burkini e balneários sem rapazes (§ 101), e o Tribunal concluiu, por unanimidade, que
#   não houve violação do artigo 9.º (dispositivo, ponto 2). 07/11/2026 (revisão): passa a escolha, como na s06 e na s07 (o cartão dá
#   a decisão e pergunta porquê); a interferência na liberdade de religião dos pais é o § 42;
# - Fotografia: Lewis Hine, _Immigrant Family in the Baggage Room of Ellis Island_, 1905, Museum of Fine Arts, Houston. O ficheiro
#   img/cidadania/hine-familia-bagagens-1905.webp (640 × 811) é o do piloto, que o plano nomeia; o registo do Wikimedia Commons
#   (aberto a 7/11/2026: Lewis Hine, 1874 a 1940; 1905; prova em gelatina e prata, 19,1 × 24,1 cm; Museum of Fine Arts, Houston;
#   domínio público nos Estados Unidos por publicação antes de 1931, PD-Art) confirma a licença. O título do museu não diz de que país
#   vinha a família, e a legenda também não o diz;
#   07/11/2026 (decisão 179): o ficheiro passa a ser o do Commons, sem filtros nem cortes (a prova inteira, com o seu tom), descarregado
#   a 1280 × 1618 por Special:FilePath e guardado a 960 × 1214; o HTML continua com width="640" height="811" (a mesma proporção,
#   a menos de 0,3 %), por isso as páginas geradas não mudam;
# - R1: _This Is Water_, o discurso de David Foster Wallace aos finalistas do Kenyon College em 2005 (#84, s09), contado por palavras
#   nossas e sem citar. 07/11/2026 (revisão): a história confere com o texto publicado pelo Kenyon College
#   (https://www.kenyon.edu/news/archive/this-is-water/, aberto a 7/11/2026): «two young fish» encontram «an older fish», que pergunta
#   «how's the water?»; seguem a nadar e um pergunta ao outro «What the hell is water?»; a leitura certa é a do próprio texto (as
#   realidades mais óbvias são muitas vezes as mais difíceis de ver). A página não dá o dia do discurso, e a sessão não o diz;
# - Vídeo (decisão 155): nenhum. O plano não propõe candidato, e o do piloto (TED-Ed) não foi visto por inteiro.
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

IMG = '../../../../img/cidadania/hine-familia-bagagens-1905.webp'
ALT = ('Fotografia a preto e branco. Uma mulher de lenço na cabeça tem um bebé ao colo; ao lado, um rapaz de boné leva ao ombro um grande '
       'saco às riscas e dá a mão a uma menina pequena de touca. Atrás, malas e baús empilhados; à frente, no chão, uma caixa atada '
       'com cordas, com palavras escritas à mão.')
ALT_VER = 'A mesma fotografia: uma mulher com um bebé ao colo, um rapaz com um saco às riscas ao ombro e uma menina de touca, entre malas.'
VER = f'<img src="{IMG}" alt="{ALT_VER}">'
COMMONS = ('https://commons.wikimedia.org/wiki/File:Lewis_W._Hine_-_Immigrant_Family_in_the_Baggage_Room_of_Ellis_Island_-_'
           'Google_Art_Project.jpg')
DRE_CRP = 'https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-aprovacao-constituicao/1976-34520775'
DRE_CDC = 'https://diariodarepublica.pt/dr/detalhe/resolucao-assembleia-republica/20-1990-222390'
HUDOC = 'https://hudoc.echr.coe.int/eng?i=001-170436'
CREDITO = ('Lewis Hine, <i>Immigrant Family in the Baggage Room of Ellis Island</i>, 1905, prova em gelatina e prata. Museum of Fine Arts, '
           f'Houston. <a href="{COMMONS}">Registo no Wikimedia Commons</a>. Domínio público.')
PERGUNTA = 'Quando uma regra parece servir todos, de quem é a voz que falta?'
DECIDE_Q = 'A regra «só português nos intervalos» deve avançar?'
FRASE = 'Antes de decidir por todos, ouve quem a regra cala.'
CDC30_FIM = 'ter a sua própria vida cultural, professar e praticar a sua própria religião ou utilizar a sua própria língua.'
ART41_3 = M.registo()['crp-41-3']['texto']


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
 # ---------------------------------------------------------------- parte 1, ver antes de concluir (60 minutos)
 # O caso do intervalo vem do piloto (s09, cartão 1), reescrito: a Mariana, que fala nepalês com a irmã, entra já no Abre (plano:
 # «a aluna que fala com a irmã»), e a razão da direção e a frase do átrio ficam para a Volta ao caso.
 M.abre('Muitas vozes, uma escola',
        f'ver e ler (60{NB}min), pausa (10{NB}min), pesar e escrever (50{NB}min) e o teu projeto (45{NB}min).',
        'Nos intervalos ouvem-se português, crioulo cabo-verdiano, romeno e nepalês. A direção propõe uma regra: nos intervalos, só '
        'português, «para todos se entenderem». A proposta está afixada no átrio, com espaço para comentários. Os que lá estão são '
        'todos de alunos que só falam português. A Mariana, que fala nepalês com a irmã no intervalo, ainda não escreveu nada.',
        PERGUNTA),
 M.decide(DECIDE_Q, [
     ('Quem acha que sim', 'Uma língua comum junta a escola e ajuda quem está a aprender português.'),
     ('Quem acha que não', 'Falar com um irmão na língua de casa não tira nada a ninguém. Proibi-lo é dizer que essa língua não cabe '
                           'na escola.'),
     ('Uma objeção', 'E se alguém usar outra língua para gozar com um colega que não a percebe? Isso pede esta regra ou outra resposta?')]),
 # R1: a obra do #84 s09 (This Is Water, 2005), por palavras nossas. O retorno liga a história à regra que parece neutra para quem fala
 # português em casa; não fala de efeitos desiguais (o R2) nem da Mariana (os cartões do Lê).
 M.recupera(escolha(
     'A pergunta do peixe mais velho',
     'Em 2005, David Foster Wallace contou: um peixe mais velho pergunta a dois novos como está a água; um deles pergunta o que é a água. '
     'O que mostra isto?',
     'Na história dos peixes que David Foster Wallace contou em 2005, os peixes novos não sabem o que é a água. O que mostra isto?',
     'Que o mais habitual é, muitas vezes, o mais difícil de ver.',
     [('Que os peixes velhos sabem mais do que os peixes novos.',
       'A história não mede quem sabe mais: os peixes novos vivem na água e não a veem, por estar sempre lá. Volta à pergunta que um '
       'faz ao outro.'),
      ('Que os peixes novos não ouviram bem a pergunta do mais velho.',
       'Ouviram: seguem a nadar e só depois um pergunta ao outro o que é a água. A dúvida não vem de ouvir mal. Volta ao que um '
       'pergunta ao outro.')],
     'A água é o que está sempre à volta e, por isso, deixa de se ver. Para quem fala português em casa, uma regra só em português '
     'pode parecer a água: normal, sem nada para explicar.',
     3, 'distinguir', 'o que não se vê', pista='Pensa porque é que os peixes novos não sabem responder.')),
 # R2: um item novo da regra igual com efeito desigual (sessão 03), recuperada sem a reensinar. «conta o efeito» está na s03 do molde.
 M.recupera(M.fazer(
     'vf', 'O mesmo preço para todos',
     'Caso inventado: a visita de estudo custa 25 euros a cada aluno. Como o preço é igual, pesa o mesmo em cada família.',
     'Se a visita de estudo custa 25 euros a cada aluno, o mesmo preço pesa o mesmo em todas as casas.',
     'É falso: o preço é o mesmo, mas 25 euros pesam mais a quem tem menos dinheiro em casa. Na sessão 03, viste que numa regra igual '
     '«conta o efeito», e não só o que está escrito.',
     4, 'aplicar', 'discriminação indireta', v=False,
     fe='Um preço igual não é um peso igual: depende do dinheiro de cada família. Na sessão 03, viste que «conta o efeito» de uma regra. '
        'Pergunta-te a quem custa mais pagar.',
     pista='Imagina duas famílias, com rendimentos diferentes, a pagar a mesma visita.'),
     origem='cidadania/m1/sessoes/03/'),
 M.olha('Uma família à chegada', 'Olha primeiro para as pessoas e para o que trazem; só depois lê a legenda.',
        M.figura(IMG, ALT, CREDITO, 'Ilha de Ellis, 1905: uma família de imigrantes na sala das bagagens.',
                 artefacto='Uma família de imigrantes, ilha de Ellis, 1905', largura=640, altura=811)),
 # O que se vê sem a legenda (plano: distratores que não se resolvem a olhar). O retorno não fala de onde vem a família (o cartão
 # seguinte).
 escolha('O que se vê',
         'Só a olhar para a imagem, sem a legenda: o que podes afirmar?',
         'Sem ler a legenda, o que se pode dizer desta fotografia com segurança?',
         'O rapaz leva um grande saco ao ombro.',
         [('A família está cansada da longa viagem.',
           'Os rostos sérios podem ser cansaço, medo ou só a pose diante da câmara: a imagem não decide entre eles. Volta à imagem e fica '
           'com o que se vê sem adivinhar.'),
          ('Esta família não sabe falar inglês.',
           'Uma fotografia não tem som: nada nela mostra a língua desta família. Volta à imagem e procura o que se pode confirmar só '
           'a olhar.')],
         'Vê-se o saco às riscas ao ombro do rapaz. O cansaço e a língua não se veem: são hipóteses sobre as pessoas, que a imagem não '
         'confirma.',
         3, 'reconhecer', 'observação', ver=VER, pista='Para cada frase, pergunta-te se a podias apontar com o dedo na imagem.'),
 # O que só a legenda diz (plano: V/F «a fotografia mostra de onde vem a família»; di-lo a legenda, e só em parte).
 M.fazer('vf', 'Imagem e legenda',
         'Só pela fotografia, sem a legenda, sabes que esta família acabava de chegar de outro país.',
         'Tapa a legenda: a imagem, sozinha, mostra que esta família vinha de outro país.',
         'É falso: a imagem mostra uma mulher, três crianças e bagagem, como numa viagem qualquer. Que são imigrantes, na ilha de Ellis, '
         'di-lo a legenda; e nem a legenda diz o país de onde vinham.',
         3, 'distinguir', 'imagem e legenda', v=False, ver=VER,
         fe='Bagagem e roupa não dizem de onde se vem: quem diz que são imigrantes é a legenda. Separa o que vês do que lês por baixo.',
         pista='Pergunta-te o que sabias sem as palavras por baixo da imagem.'),
 # 07/11/2026: as referências na margem são curtas (a margem tem 5,6 rem e não parte a linha); o documento de cada uma diz-se no
 # «Antes de ler», pela mesma ordem, e no «Ler mais».
 M.le('O que uma regra não pode tirar', 'O que diz cada texto sobre a língua?',  # 07/11/2026: decisão 179, mais curta para caber o artigo 30.º
      [(f'13.º, n.º{NB}2', 'Ninguém pode ser privilegiado, beneficiado, prejudicado […] em razão de […] língua, território de '
                          'origem, religião […]', 'crp-13-2', 'a13'),
       # 07/11/2026: decisão 179. Já não se corta «conjuntamente com membros do seu grupo»: o validador aceita a palavra só nos
       # excertos de lei registados e copiados letra a letra. O início do artigo («Nos Estados em que existam minorias…») fica no
       # «Ler mais», como antes, para o cartão caber nas 80 palavras à vista; entre os dois, o artigo 30.º está inteiro no cartão.
       (f'Artigo{NB}30.º', '[…] nenhuma criança indígena ou que pertença a uma dessas minorias poderá ser privada do direito '
                          'de, conjuntamente com membros do seu grupo, ' + CDC30_FIM, 'cdc-30', 'c30')],
      f'<a href="{DRE_CRP}">Constituição</a> e <a href="{DRE_CDC}">Convenção</a>',
      mais=M.lei([('30.º, início', 'Nos Estados em que existam minorias étnicas, religiosas ou linguísticas ou '
                   'pessoas de origem indígena, […]', 'cdc-30', None),
                  ('41.º, n.º 3', ART41_3, 'crp-41-3', None)],
                 f'<a href="{DRE_CDC}">Convenção</a>, 30.º; <a href="{DRE_CRP}">Constituição</a>, 41.º')),
 # Leitura exata: o que a regra tira à Mariana, no artigo 30.º (o verbo e o que ele rege).
 M.fazer('sublinhar', 'O que a regra tira',
         'No artigo 30.º, sublinha as duas palavras que dizem o que a regra do intervalo tira à Mariana.',
         'No artigo 30.º, onde está o que a Mariana deixa de poder fazer no intervalo? Sublinha as duas palavras.',
         'A regra não tira à Mariana a língua que tem: tira-lhe o direito de a «utilizar» no intervalo. É essa a parte do artigo 30.º que '
         'fica em causa.',
         3, 'reconhecer', 'direitos das minorias', frase=CDC30_FIM, certas=palavras(CDC30_FIM, ['utilizar', 'língua']),
         fonte='cdc-30', l='c30', citacoes=[('cdc-30', 'utilizar'), ('cdc-30', 'vida cultural')],
         fe='A confusão mais provável é sublinhar «vida cultural»: a regra não toca em festas nem costumes, só no que se fala. Procura o '
            'verbo do que se faz e a palavra que o completa.',
         pista='Lê a frase até ao fim e procura a parte que toca no que a Mariana faz no intervalo.'),
 # Aplicação ao caso: o artigo 13.º, n.º 2, também nomeia a língua (o erro: só ver a origem).
 M.fazer('vf', f'A regra e o artigo{NB}13.º',
         'A regra do intervalo não pergunta de onde vem cada aluno. Por isso, fica fora do artigo 13.º, n.º 2.',
         'Como a regra não fala do país de onde vem ninguém, o artigo 13.º, n.º 2, não tem a ver com ela.',
         'É falso: a lista do artigo 13.º, n.º 2, tem a «língua», além do «território de origem». Uma regra sobre a língua que se fala '
         'pode prejudicar alguém em razão dela, sem perguntar de onde vem.',
         4, 'aplicar', 'igualdade', v=False, l='a13',
         citacoes=[('crp-13-2', 'língua'), ('crp-13-2', 'território de origem')],
         fe='O artigo 13.º, n.º 2, não fala só da origem: na mesma lista está a «língua». Volta à lista e procura o que a regra do '
            'intervalo toca.',
         pista='Relê a lista do artigo, palavra a palavra.'),
 # Um limite da liberdade religiosa: a pergunta pela religião (artigo 41.º, n.º 3, no próprio cartão). Os distratores são as duas
 # leituras erradas do próprio texto: «para estatística» chega; não ser prejudicado torna a pergunta permitida.
 escolha('Perguntar pela religião',
         'Caso inventado: um inquérito da câmara pede a religião de cada pessoa, com o nome e a morada, «para estatística». O artigo '
         '41.º, n.º 3, permite-o?',
         'Uma câmara municipal quer saber a religião de cada pessoa, com o nome e a morada, para fazer estatística. O artigo 41.º, n.º 3, '
         'permite-o?',
         'Não: com nome e morada, cada resposta identifica alguém.',
         [('Sim: sendo para estatística, a pergunta é permitida.',
           'A exceção não é só ser para estatística: os dados têm de ser «não individualmente identificáveis». Com o nome e a morada, '
           'cada resposta diz quem é quem. Relê o fim da exceção.'),
          ('Sim: basta que quem não responder não fique prejudicado.',
           'Não ser «prejudicado por se recusar a responder» é outra proteção, que se junta à primeira; não torna a pergunta permitida. '
           'Relê a exceção até ao fim.')],
         'A exceção vale só para «dados estatísticos não individualmente identificáveis». Com o nome e a morada, as respostas identificam '
         'cada pessoa: assim, a câmara não pode perguntar.',
         3, 'aplicar', 'liberdade religiosa', cita=ART41_3, fonte='crp-41-3',
         citacoes=[('crp-41-3', 'não individualmente identificáveis'), ('crp-41-3', 'prejudicado por se recusar a responder'),
                   ('crp-41-3', 'dados estatísticos não individualmente identificáveis')],
         pista='Relê a exceção até ao fim e compara-a com o que o inquérito pede.'),
 # Charneira 1 (plano: o estereótipo que parece elogio, piloto 9), numa situação nova sem as palavras do texto: escolher pela origem,
 # com um elogio, é beneficiar «em razão de» território de origem. O erro esperado: o artigo só proíbe prejudicar.
 escolha('Um elogio pela origem',
         'Caso inventado: para uma visita a uma empresa, a escola escolhe só alunos vindos de fora, «porque são mais trabalhadores». É '
         'um elogio. Pelo artigo 13.º, n.º 2, há problema?',
         'A escola leva à visita só os alunos vindos de fora, por serem «mais trabalhadores». Por ser um elogio, o artigo 13.º, n.º 2, '
         'permite-o?',
         'Sim: ninguém pode ser beneficiado em razão da origem.',
         [('Não: o artigo só proíbe prejudicar, e ninguém perde.',
           'A lista do artigo 13.º, n.º 2, abre com «privilegiado, beneficiado»: favorecer pela origem também conta. E quem fica sem a visita '
           'perde. Relê o início do artigo.'),
          ('Não: é um elogio a esses alunos, não uma ofensa.',
           'Um elogio pela origem continua a tratar cada aluno pelo sítio de onde vem, e não pelo que faz. Relê o artigo 13.º, n.º 2, '
           'desde a primeira linha.')],
         'O artigo 13.º, n.º 2, proíbe prejudicar e também beneficiar alguém em razão do «território de origem». Escolher pela origem, '
         'mesmo com um elogio, trata cada aluno pelo sítio de onde vem.',
         4, 'transferir', 'estereótipo',
         citacoes=[('crp-13-2', 'privilegiado, beneficiado'), ('crp-13-2', 'território de origem')],
         pista=f'Relê o artigo{NB}13.º, n.º{NB}2, desde a primeira palavra, e volta à escolha da escola.'),
 # Conceito (uma vez): facto, dado, opinião e estereótipo, em tabela (decisão 152). Os exemplos não são os dos cartões 17 e 19.
 M.conceito('Facto, dado, opinião, estereótipo',
            '<p>«Quem vem de fora não quer aprender português.» Soa a facto. É?</p>',
            '<table class="tabela"><thead><tr><th scope="col">Tipo de frase</th><th scope="col">Como se confere</th></tr></thead><tbody>'
            '<tr><td data-th="Tipo de frase">facto</td><td data-th="Como se confere">vendo ou ouvindo</td></tr>'
            '<tr><td data-th="Tipo de frase">dado</td><td data-th="Como se confere">na fonte do número</td></tr>'
            '<tr><td data-th="Tipo de frase">opinião</td><td data-th="Como se confere">não se confere: discute-se</td></tr>'
            '<tr><td data-th="Tipo de frase">estereótipo</td><td data-th="Como se confere">não se confere: generaliza sem provas</td></tr>'
            '</tbody></table>',
            'Estereótipo', 'Uma ideia feita, igual para todos os de uma origem, língua ou religião.',
            '<p>Mesmo um elogio: «quem vem de fora é trabalhador» também é um estereótipo.</p>'),
 # Transferir 1 (conceito espaçado, sessão 01: o que se vê e o que se conclui). Plano: «Nunca queres» (Leonor e Rui, do M1 publicado):
 # «nunca» faz de um momento um traço de carácter, o mesmo salto do estereótipo, agora sobre uma só pessoa.
 M.fazer('emparelhar', 'Um momento ou um traço',
         'Caso inventado: à porta, a Leonor guarda um envelope ao ver os colegas e pede para falar depois. O Rui: «Nunca queres '
         'participar.» O que é cada frase?',
         'A Leonor guarda um envelope e pede para falar depois; o Rui diz «Nunca queres participar». Liga cada frase ao que ela é.',
         'Guardar o envelope e pedir para falar depois vê-se na cena. «Nunca» faz de um momento um traço de carácter, como o estereótipo '
         'faz com quem vem de fora. Que ela prefira falar a sós é uma hipótese, que se confirma perguntando.',
         3, 'transferir', 'observação e interpretação', origem='cidadania/m1/sessoes/01/',
         pares=[['A Leonor guarda o envelope e pede para falar depois.', 'O que a cena mostra'],
                ['«Nunca queres participar.»', 'Um momento tornado traço de carácter'],
                ['Ela prefere falar sem os colegas por perto.', 'Uma hipótese, que se pode pôr à prova']],
         fe='A confusão mais provável é tomar «Nunca queres participar» pelo que se viu. O Rui viu um momento; «nunca» fala de todos. Na '
            'sessão 01, viste que isso já é uma interpretação.',
         pista='Pergunta a cada frase: viu-se, ou alguém o concluiu?'),
 # Transferir 2 e caso real (decisão 161): Osmanoğlu e Kocabaş c. Suíça (TEDH, 2017), contado por palavras nossas, sem citar.
 # 07/11/2026 (revisão): passa de V/F a escolha, como na s06 e na s07: o cartão dá a decisão e pergunta porquê (o V/F pedia para
 # adivinhar o veredicto). Os erros que se tratam: uma regra igual não se discute (os pais levaram-na ao Tribunal) e a liberdade de
 # religião não protege o que os pais ensinam (o Tribunal aceitou a interferência, § 42). As adaptações são as que o § 101 diz
 # «oferecidas», sem lhes dar causa.
 escolha('A natação obrigatória',
         'Caso real (Tribunal Europeu dos Direitos Humanos, 2017): sem dispensa da natação mista, duas alunas de família muçulmana podiam '
         'nadar de burkini. O Tribunal não viu violação. Porquê?',
         'Caso real (Tribunal Europeu dos Direitos Humanos, 2017): duas alunas não foram dispensadas da natação mista, mas podiam usar '
         'burkini. O Tribunal não viu violação. Porquê?',
         'Pesou aprender em conjunto, e a escola adaptou a aula sem dispensar ninguém.',
         [('Uma regra que é igual para todos não se pode contestar num tribunal.',
           'Pode: os pais contestaram-na até ao Tribunal, que pesou as razões dos dois lados. Uma regra igual também se discute. Volta ao '
           'que pesou contra a dispensa.'),
          ('A liberdade de religião não protege o que os pais ensinam aos filhos.',
           'Protege: o Tribunal aceitou que a recusa da dispensa interferia na liberdade de religião dos pais (§ 42). Mesmo assim, pesou '
           'outras razões. Volta às adaptações.')],
         'O Tribunal aceitou a interferência, mas pesou aprender em conjunto e as adaptações, o burkini e o balneário sem rapazes. Um '
         'efeito desigual obriga a pesar; não decide sozinho.',
         4, 'transferir', 'regra comum e adaptação',
         liga=[{'t': 'Ler o acórdão no HUDOC (10/01/2017, em inglês)', 'href': HUDOC}],
         pista='Lê cada razão e pergunta-te se o caso, como o cartão o conta, a sustenta.'),
 # ---------------------------------------------------------------- parte 2, pesar e escrever (50 minutos)
 # Volta ao caso: duas razões que chocam (proteger quem foi gozado e deixar a Mariana falar com a irmã).
 M.volta('A razão da direção',
         'A diretora explica: na semana passada, um aluno queixou-se de que dois colegas se riam dele em romeno; e ela acha que uma '
         'língua comum junta a escola. A Mariana escreve no átrio: a irmã chegou há dois meses e ainda não percebe português. Por '
         'baixo, alguém acrescenta: «Quem fala outra língua no intervalo está a esconder alguma coisa.»',
         carimbo='Caso inventado.'),
 # A dúvida ainda aberta: a queixa conta um episódio; se a regra o evitaria, ainda não se sabe.
 M.fazer('vf', 'O que a queixa prova',
         'Pela queixa do aluno, já se sabe que só falar português no intervalo acaba com o gozo.',
         'A queixa do aluno prova que, com a regra do português, deixa de haver gozo no intervalo.',
         'É falso: a queixa conta um episódio, em romeno. Se a regra o evitaria, ainda não se sabe: também se pode gozar em português. '
         'É uma dúvida para o papel.',
         3, 'aplicar', 'facto e dúvida', v=False,
         fe='A queixa diz o que aconteceu uma vez; não diz o que a regra mudaria. Separa o que está no caso do que se espera da regra.',
         pista='Relê a queixa na Volta ao caso: o que conta ela, e quantas vezes aconteceu?'),
 M.em_turma(DECIDE_Q, [
     ('Quem acha que sim', 'Um aluno foi gozado numa língua que não percebia. Uma língua comum pode evitar que se repita.'),
     ('Quem acha que não', f'A irmã da Mariana não percebe português, e o artigo 30.º fala de '
                           f'{M.citado("cdc-30", "utilizar a sua própria língua")}.'),
     ('Uma objeção', 'O gozo trava-se com uma regra sobre a língua, ou com uma regra sobre o gozo?')],
     {'O que se faz': 'Decides outra vez e escolhes a prova que mais pesa.',
      'Quanto tempo': 'Três minutos; em turma, até treze.',
      'O que fica escrito': 'Nada em papel; a escolha fica nos artefactos.',
      'Se estás sozinho': 'Compara com a escolha do início e abre os três lados.'},
     prova=('O que pesa mais?', ('A queixa do aluno', 'A irmã da Mariana', f'O artigo{NB}30.º')),
     intro='', nota=None),
 M.fazer('emparelhar', 'Facto, princípio, opinião ou estereótipo',
         'Liga cada frase ao que ela é numa justificação.',
         'Facto do caso, princípio de um texto, opinião de uma das partes ou estereótipo: o que é cada frase?',
         'A chegada da irmã é um facto do caso; «utilizar a sua própria língua» é um princípio da Convenção; a frase da diretora é a '
         'opinião dela; a frase do átrio é um estereótipo: não prova nada sobre ninguém.',
         3, 'distinguir', 'relato e princípio',
         pares=[['A irmã da Mariana chegou há dois meses.', 'Um facto do caso'],
                ['«[…] utilizar a sua própria língua.»', 'Um princípio escrito num texto'],
                ['A diretora acha que uma língua comum junta a escola.', 'A opinião de uma das partes'],
                ['«Quem fala outra língua no intervalo está a esconder alguma coisa.»', 'Um estereótipo']],
         citacoes=[('cdc-30', 'utilizar a sua própria língua')],
         fe='A confusão mais provável é tomar a frase do átrio por facto: põe a mesma ideia em todos os que falam outra língua, sem olhar '
            'para ninguém. Pergunta a cada frase de onde vem e como se confere.',
         pista='Pergunta a cada frase de onde vem e quem a diz.'),
 M.fazer('ordenar', 'A justificação por ordem',
         'Põe a justificação por ordem: cada passo tem de se apoiar no que vem antes.',
         'Ordena os quatro passos, de modo que cada um se apoie no anterior.',
         'Facto, fonte, aplicação, limite: cada passo apoia-se no anterior, e o limite diz até onde a conclusão pode ir.',
         4, 'aplicar', 'facto, fonte, aplicação, limite',
         passos=['A irmã da Mariana chegou há dois meses e ainda não percebe português.',
                 'A Convenção diz que nenhuma criança de uma minoria pode ser privada do direito de utilizar a sua própria língua.',
                 'Com a regra, a Mariana deixa de poder falar com a irmã no intervalo.',
                 'Falta saber se só falar português no intervalo evitaria o gozo.'],
         fe='A confusão mais provável é começar pelo artigo ou pôr o que falta saber antes da aplicação. Começa no que aconteceu; o que '
            'falta saber fecha a justificação.',
         pista='Pergunta-te o que tem de vir primeiro para o resto se apoiar.'),
 # Charneira 2, no apoio que se retira (sessões 08 a 10): encontrar a conclusão que vai além das provas. 07/11/2026 (revisão): a que
 # excede é uma ideia feita ligada ao lado «sim» do Decide (falar nepalês atrasa o português da irmã), que nenhuma frase do caso
 # sustenta; as outras duas estão no caso, por outras palavras. O erro esperado é escolher uma das que o caso sustenta.
 escolha('A conclusão que vai longe de mais',
         'Só uma destas conclusões vai além do que o caso mostra. Encontra-a.',
         'Uma destas conclusões diz mais do que as provas do caso permitem. Encontra-a.',
         'Falar nepalês no intervalo atrasa o português da irmã.',
         [('A irmã da Mariana chegou à escola há pouco tempo.',
           'Está no caso: a Mariana escreveu que a irmã chegou há dois meses. Procura a conclusão que junta ao caso uma ideia que ninguém '
           'provou.'),
          ('A diretora propõe a regra a pensar na queixa de um aluno.',
           'Está no caso: a diretora explica a regra com a queixa da semana passada. Procura a conclusão que nenhuma frase do caso '
           'sustenta.')],
         'Ninguém no caso diz que falar nepalês atrasa o português da irmã: é uma ideia feita com ar de conclusão. As outras duas estão '
         'no caso.',
         3, 'aplicar', 'conclusão e provas', pista='Para cada conclusão, procura no caso a frase que a sustenta.'),
 M.papel(PERGUNTA,
         ['A tua conclusão: a regra deve avançar, mudar ou cair?',
          'Uma prova: um facto do caso e uma expressão exata, entre aspas, com o artigo.',
          'Uma dúvida que ainda tens.'],
         ['A conclusão responde à pergunta sem ir além das provas.',
          'A prova junta um facto a uma expressão exata, com o artigo.',
          'A dúvida, respondida, podia mudar a conclusão.'],
         '<p>Caso inventado: o clube de teatro só aceita inscrições pelo telemóvel.</p><ol>'
         '<li>Conclusão: deve haver também inscrição em papel.</li>'
         f'<li>Prova: dois alunos não têm telemóvel, por falta de dinheiro; ninguém pode ser '
         f'{M.citado("crp-13-2", "prejudicado")} em razão da '
         f'{M.citado("crp-13-2", "situação económica")} (artigo 13.º, n.º 2).</li>'
         '<li>Dúvida: quantos ficam de fora?</li></ol>',
         'Num papel pequeno, sozinho, sem telemóvel.',
         relogio_min=12),
 M.levar(FRASE, ['Um estereótipo diz o mesmo de todos; cada pessoa é mais.',
                 'Uma regra que pesa mais sobre alguns obriga a pesar razões; não cai só por isso.']),
]

# o lugar da certa em cada escolha (0, 1 ou 2), com a semente do motor: nunca o mesmo em mais de metade, nem três seguidos
LUGARES = (1, 2, 0, 2, 0, 1)  # 07/11/2026 (revisão): o cartão 15 passa a escolha (a 5.ª)

# O passo do projeto (plano, secção 3: «guião, versão 2, com a voz de quem discorda e a fonte», piloto 18). O que se diz do guião é o
# que a página do projeto já diz (cidadania/projeto/, «As fases»: no guião, tornar localizáveis as fontes das falas).
DEPOIS = ('<article class="c"><p class="rot">O passo do teu projeto</p><p class="tit">O guião, versão 2</p>'
          '<p class="sub">Volta, em papel, ao guião do teu teatro-documento e junta-lhe a voz de alguém que discorda da tua resposta à '
          'pergunta. Essa fala também tem fonte: a entrevista, o documento ou a notícia, com o que é preciso para a reencontrar. O que '
          'conta: a voz que discorda diz o que essa pessoa disse, sem a tornar ridícula; tem a sua fonte; o guião mostra o que responde a '
          'essa voz, ou deixa a dúvida à vista.</p>'
          '<p class="ir"><a href="../../../projeto/#fases">As fases do teatro-documento, no enunciado da Pergunta Humana</a></p></article>')


def sessao():
    d = {
        'id': 'cidadania-m1-s09', 'chave': 'epi-cid-m1-s09', 'versao': '2026-11-07-molde', 'marca': 'CD', 'molde': L.MOLDE,
        'titulo': 'Sessão 09: Muitas vozes, uma escola', 'h1': 'Cidadania, módulo 1, sessão 09: Muitas vozes, uma escola',
        'modulo': {'n': 1, 'nome': 'Humanos', 'url': L.LENTE + 'cidadania/piloto/m1/'},
        'saida': 'cidadania/m1/sessoes/09/index.html',
        # 07/11/2026 (sessão 10 no molde): a seguinte passa a ser a s10 nova, no mesmo endereço das sessões (era a do piloto).
        'seguinte': '../10/', 'seguinteRotulo': 'Sessão 10: O que consegues defender?',
        'fontes': M.ref('Constituição da República Portuguesa, artigos 13.º, n.º 2, e 41.º, n.º 3, na versão consolidada do Diário da '
                        'República. Convenção sobre os Direitos da Criança, artigo 30.º, na tradução portuguesa anexa à Resolução da '
                        'Assembleia da República n.º 20/90, no Diário da República. Tribunal Europeu dos Direitos Humanos, _Osmanoğlu e '
                        'Kocabaş c. Suíça_, queixa n.º 29086/12, acórdão de 10 de janeiro de 2017 (HUDOC, texto inglês). Fotografia: Lewis '
                        'Hine, _Immigrant Family in the Baggage Room of Ellis Island_, 1905, Museum of Fine Arts, Houston, domínio público. '
                        'David Foster Wallace, _This Is Water_, discurso aos finalistas do Kenyon College, 2005, no texto publicado pelo Kenyon '
                        'College. O caso do intervalo, o da visita de estudo, o do '
                        'inquérito da câmara, o da visita à empresa, o da Leonor e do Rui e o do clube de teatro são inventados; o da '
                        'natação em Basileia é real.'),
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
