# Fonte da sessão 2 de «Ideias», o coração do Laboratório (piloto escondido de 31/10/2026; plano em coracao/plano.md, no
# caderno de bordo). Corre-se para escrever o .json ao lado; o .json é que o gerador (tools/licoes_lente.py) lê.
#
# 01/11/2026 (método, encargo do docente «assumir o método de Young, passo a passo»): o «Abre» situa o método (passo 1 de 5,
# até ao fundo; o que pede e porque vem agora; os cinco passos numa linha, com o de hoje marcado); nos cartões, o conselho é «a
# versão de 1940» ou «o livro do método», e o nome de Young fica na fonte da citação do cocheiro e na passagem para o passo 2,
# no «Para levar»; a marca da casca diz «passo 1 de 5» (campo «passo»). Nenhum cartão novo nem mudança de ordem: a versão
# fica 2026-10-31-1. As perguntas, as respostas certas, a chave e os 12 cartões de fazer não mudam; a opção «O nome de
# Flaubert, que Young não diz.» passa a «O nome de Flaubert, que o livro omite.», com o mesmo comprimento (38 carateres).
#
# 01/11/2026 (correção 1 do método, revisor de pt-PT): a fonte do cartão 3 com o título do livro como no menu de fontes; no
# «Para levar», «Passo 1 de 5: falta o material geral.» (era «feito», com o material geral ainda por juntar na sessão 3).
#
# 01/11/2026 (correção 4, revisor de pt-PT): o p2 do cartão «cedo» pede as três palavras que tocas; a linha do «Na aula» só serve
# para esse «cocheiro»; «Também puseste» no «Para levar», sem duas frases seguidas a abrir com «E».
# 01/11/2026 (correção 3): o texto do revisor de pt-PT e os factos do verificador («entre dez e catorze anos» depois do prefácio, o «lugar escolhido» sem «pela turma», O teu «cocheiro», «abrir a porta de casa»).
#
# Fontes lidas a 31/10/2026, um pedido de cada vez (nada citado de memória):
# - James Webb Young, Uma Técnica para Produzir Ideias, tradução nossa (texto de trabalho no caderno de bordo,
#   biblioteca-young/texto.txt):
#   o conselho do cocheiro, as matérias-primas «específicas e gerais», «interrompe demasiado cedo».
# - Guy de Maupassant, «Le Roman», prefácio de Pierre et Jean (1888): https://www.gutenberg.org/cache/epub/11131/pg11131.txt
#   (linhas 488 a 545: a «longue patience», «Il s'agit de regarder…», o fogo e a árvore, «La moindre chose contient un peu
#   d'inconnu», «en quelques phrases», o cavalo de fiacre «par un seul mot», «qu'un mot pour l'exprimer»).
# - Eugène Atget, Kiosque et fiacres, Paris, Musée Carnavalet, PH1179: página da Paris Musées, «CC0 Paris Musées / Musée
#   Carnavalet – Histoire de Paris» (imagem pm_diaporama_zoom, 804 × 1080, em assets/laboratorio/ideias/).
import importlib.util, json, pathlib

LENTE = 'https://pedrohfernandes-klk.github.io/lente/'
IMG = '../../../assets/laboratorio/ideias/'
MAUP = 'https://www.gutenberg.org/ebooks/11131'

# 01/11/2026 (método): os cinco passos, como na sessão 1 e na entrada (tools/ideias_piloto.py, PASSOS)
PASSOS = ['Juntar material', 'Trabalhar o material', 'Largar', 'A ideia aparece', 'Dar forma e pôr à prova']


def passos(hoje):
    return ('<ol class="passos-m" aria-label="Os cinco passos do método">'
            + ''.join(f'<li class="hoje" aria-current="step"><b>{n}</b> {t} <span class="hoje-t">hoje</span></li>' if n in hoje
                      else f'<li><b>{n}</b> {t}</li>' for n, t in enumerate(PASSOS, 1)) + '</ol>')


ABRE = (
 '<p class="pergunta-c">O que distingue uma coisa de todas as outras iguais a ela?</p>'
 '<p>Hoje a turma olha para um lugar perto da escola. Parece igual a tantos outros. Até ao fim da sessão, vais conhecer uma coisa desse lugar como ninguém a conhece.</p>'
 '<div class="metodo-linha"><p><b>Passo 1 de 5: juntar material, até ao fundo.</b> Na sessão 1, recolheste factos a olhar; hoje vais mais fundo, numa só coisa. Sem este material específico, os passos seguintes não têm em que trabalhar.</p></div>'
 + passos({1}) +
 '<p class="aula-linha"><b>Hoje</b>, 180 minutos com uma pausa: o conselho de um romancista, uma testemunha posta à prova, uma fotografia de Paris e uma saída à rua (ou, em vez dela, o mesmo exercício feito da janela ou numa fotografia de rua).</p>')
DECIDE = (
 '<p>Uma árvore da tua rua é só uma árvore?</p>'
 '<p class="pergunta-c">Decide em silêncio, de braço no ar: sim, não ou depende.</p>'
 '<details class="lado"><summary>A razão de quem diz que sim</summary><div><p>Há milhares de árvores iguais na cidade. Olhar meia hora para uma é perder meia hora.</p></div></details>'
 '<details class="lado"><summary>A razão de quem diz que não</summary><div><p>O escritor francês Guy de Maupassant resume assim uma lição do seu mestre, o romancista Gustave Flaubert: «Para descrever um fogo que arde e uma árvore numa planície, fiquemos diante desse fogo e dessa árvore até que deixem de se parecer, para nós, com qualquer outra árvore e com qualquer outro fogo» (tradução nossa).</p></div></details>'
 '<details class="lado"><summary>Uma objeção</summary><div><p>Mesmo que as diferenças existam, para que servem a quem quer escrever ou criar?</p></div></details>'
 '<p>Não há resposta certa neste cartão. Guarda a tua posição: voltas a ela no fim.</p>')
YOUNG = (
 '<p>No livro do método, de 1940, vem um conselho dado ao jovem Guy de Maupassant, o contista francês, quando aprendia a escrever:</p>'
 '<blockquote><p>«Saia para as ruas de Paris», disse-lhe um dia um escritor mais velho, «e escolha um cocheiro. Parecer-lhe-á um cocheiro igual a tantos outros. Estude-o até conseguir descrevê-lo como um indivíduo único, distinto de todos os outros cocheiros do mundo.»</p></blockquote>'
 # 01/11/2026 (correção 1 do método, revisor de pt-PT): o título do livro como no menu de fontes e na sessão 1
 '<p class="fonte">James Webb Young, <i>A Technique for Producing Ideas</i>, capítulo «Ideias São Novas Combinações». Tradução nossa.</p>'
 '<p>O livro não diz onde foi buscar a história. Um detetive vai à fonte.</p>')
MAUPASSANT = (
 '<p>Maupassant contou a história em 1888, no prefácio do romance <i>Pierre et Jean</i>, onde resume assim a lição do mestre, Gustave Flaubert:</p>'
 '<blockquote><p>Trata-se de olhar para tudo o que se quer exprimir durante tempo suficiente e com atenção suficiente para lhe descobrir um aspeto que ninguém tenha visto nem dito.</p></blockquote>'
 '<p>Flaubert obrigava-o a exprimir, em poucas frases, um ser ou um objeto, até o distinguir de todos os outros da mesma espécie. E dizia-lhe:</p>'
 '<blockquote><p>«Quando passa diante de um merceeiro sentado à porta, diante de um porteiro que fuma cachimbo, diante de uma praça de fiacres, […] faça-me ver, com uma só palavra, em que é que um cavalo de fiacre não se parece com os outros cinquenta que o seguem e o precedem.»</p></blockquote>'
 '<p class="fonte">Guy de Maupassant, «Le Roman», prefácio de <i>Pierre et Jean</i>, 1888. Tradução nossa.</p>')
ATGET = (
 f'<figure class="fig inteiro"><span class="moldura"><img src="{IMG}atget-quiosque-fiacres.webp" '
 'alt="Uma rua de Paris com árvores de ramos nus. À esquerda, um quiosque envidraçado, com cúpula; junto dele, de pé, ao lado de um candeeiro, um homem de capa comprida e chapéu, de cabeça baixa; logo atrás dele, mais acima, um homem de chapéu alto; atrás, fiacres com cavalos e, na ponta esquerda, um homem sentado no alto de um deles." loading="lazy"></span>'
 '<figcaption>Eugène Atget, <i>Kiosque et fiacres, Paris</i>, entre 1898 e 1902. Tiragem em papel albuminado, 22,1 × 17 cm. '
 '<a href="https://www.parismuseescollections.paris.fr/fr/musee-carnavalet/oeuvres/kiosque-et-fiacres-paris">Musée Carnavalet, Histoire de Paris</a>, PH1179 (Paris Musées). CC0.</figcaption></figure>'
 '<p>Entre dez e catorze anos depois do prefácio de Maupassant, o fotógrafo francês Eugène Atget registou este quiosque e estes fiacres de Paris.</p>'
 # 01/11/2026 (método; padrão 13 dos cartões, «Observar a sério», decisão 92): primeiro a fotografia inteira, depois ampliada
 '<p>Vê primeiro a fotografia inteira; depois amplia-a e percorre-a de uma ponta à outra.</p>'
 '<p class="pergunta-c">Faz três colunas no caderno: «vejo», «concluo» e «não sei». Escreve pelo menos três linhas em cada uma.</p>')
NA_AULA = (
 '<p><b>O que se faz.</b> Aos pares, saem com o docente até ao lugar escolhido. Cada um escolhe o seu «cocheiro»: uma banca, uma árvore, uma montra, uma porta (pessoas só de longe, e nunca se fotografam caras). Regista quinze notas: cinco do que vê; cinco do que ouve, cheira ou toca; cinco do que o distingue dos outros. No guião, escreve uma linha que só sirva para esse «cocheiro». De volta à sala, a fila de reconhecimento: cada um lê a sua linha sem dizer o que é, e a turma tenta dizer qual é. Se a turma não sair, faz-se o mesmo da janela ou numa fotografia de rua.</p>'
 '<p><b>Quanto tempo.</b> 70 minutos, com a pausa.</p>'
 '<p><b>O que fica escrito.</b> As quinze notas, onde guardas o material; no guião, a tua linha e o resultado da fila.</p>')
LEVAR = (
 '<p class="levar">Olhar até a coisa deixar de ser igual às outras.</p>'
 '<p>Foste à fonte de uma citação: a testemunha mudava pormenores, mas o essencial mantinha-se. Também puseste uma descrição à prova em quem não sabia o que descrevias. E agora: uma árvore da tua rua é só uma árvore?</p>'
 '<p><b>As frases da sessão</b></p>'
 '<ul><li>Uma testemunha honesta também se engana: confirma na fonte.</li>'
 '<li>A prova de uma descrição é alguém reconhecer a coisa.</li>'
 '<li>Uma palavra exata vale mais do que três bonitas.</li></ul>'
 '<p><b>No Laboratório:</b> <a href="../../personagem-faz/">Ver, «Conhecer uma personagem», <i>A personagem pelo que faz</i></a>: o adjetivo afirma, o gesto prova.</p>'
 # 01/11/2026 (correção 1 do método, revisor de pt-PT): «Passo 1 de 5: feito.» dava o passo por acabado e, na mesma frase, mandava
 # juntar o material geral, que ainda é passo 1 (entrada, sessão 3; guia, sessões 1 a 3; cartão 16 desta sessão)
 '<p><b>Passo 1 de 5: falta o material geral.</b> Na sessão 3, junta-lo e começas o passo 2 de Young, trabalhar o material. Traz dez notas sobre o que sabes bem fora da escola: um desporto, uma receita, um ofício da família.</p>')

cartoes = [
 {"t":"ler","rot":"Abre","titulo":"Cinquenta cavalos","html":ABRE},
 {"t":"ler","rot":"Decide","titulo":"A árvore da tua rua","html":DECIDE},
 {"t":"ler","rot":"Ler","titulo":"O conselho, em 1940","html":YOUNG},
 {"t":"escolha","g":"young","p":"Na versão de 1940, o que pediu o escritor mais velho a Maupassant?","p2":"Que conselho recebeu Maupassant, segundo o livro de 1940?",
  "o":["Que estudasse um cocheiro até o ver como único.","Que escrevesse sobre todos os cocheiros de Paris.","Que trabalhasse como cocheiro durante um mês."],"c":0,
  "f":"Na versão de 1940, o conselho é escolher um cocheiro que parece igual aos outros e estudá-lo até o conseguir descrever como único.",
  "fe":["","A versão de 1940 fala de um só cocheiro, escolhido entre muitos. O exercício é ir fundo num, não passar por todos.","Ninguém lhe pede que mude de vida. Pede-lhe que olhe para um cocheiro até ver o que só ele tem."]},
 {"t":"ler","rot":"Ler","titulo":"O conselho, em 1888","html":MAUPASSANT},
 {"t":"emparelhar","g":"testemunha","p":"A testemunha posta à prova: liga cada pormenor da versão de 1940 ao que está em Maupassant.","p2":"No lugar de cada pormenor da versão de 1940, o que está no prefácio de Maupassant?",
  "pares":[["um escritor mais velho","Gustave Flaubert, com nome"],["um cocheiro","um cavalo de fiacre"],["descrevê-lo como um indivíduo único","distingui-lo dos outros da mesma espécie"],["as ruas de Paris","um merceeiro, um porteiro, uma praça de fiacres"]],
  "f":"Mudaram três coisas (Flaubert perdeu o nome, o cavalo passou a cocheiro e os exemplos passaram a «as ruas de Paris») e perdeu-se uma: a exigência de «uma só palavra». O essencial confirma-se, quase com as mesmas palavras: distinguir um ser ou um objeto de todos os outros da mesma espécie.",
  "fe":"Põe as duas versões lado a lado e procura, em cada pormenor de 1940, o que ocupa o mesmo lugar em 1888.",
  "liga":[{"href":MAUP,"t":"O prefácio de _Pierre et Jean_, em francês (Project Gutenberg)"}]},
 {"t":"escolha","g":"palavra","p":"Que pormenor, ausente da versão de 1940, torna o exercício de Flaubert mais difícil?","p2":"Das diferenças entre as duas versões, qual pesa mais no exercício?",
  "o":["A exigência de o dizer com uma só palavra.","O cavalo, mais difícil do que um homem.","O nome de Flaubert, que o livro omite."],"c":0,
  "f":"«Com uma só palavra» obriga a escolher, não a acumular. Descrever um cavalo em vinte linhas é fácil; encontrar a palavra que o separa dos outros cinquenta é que é o exercício.",
  "fe":["","Um cavalo e um homem podem ser igualmente difíceis. O que muda o exercício é o limite que Flaubert impõe.","Calar o nome muda a história, não o que se pede a quem escreve."]},
 {"t":"escolha","g":"leitura","p":"Quem escreveu a versão de 1940 mudou o conselho e não disse onde o leu. Que leitura é mais justa?","p2":"Como ler a versão de 1940, que troca o cavalo por um cocheiro e não diz de onde vem a história?",
  "o":["Contou-o à sua maneira e guardou o essencial.","Inventou-o e atribuiu-o a um escritor famoso.","Copiou Maupassant palavra por palavra."],"c":0,
  "f":"O conselho existe e está no prefácio de Maupassant; a versão de 1940 conta-o à sua maneira, sem dizer onde o foi buscar. Uma testemunha que erra num pormenor não é uma testemunha que mente. Quando uma citação te interessa, vai à fonte.",
  "fe":["","O conselho não é inventado: está no prefácio de _Pierre et Jean_, de 1888.","As palavras não são as mesmas: o cavalo passou a cocheiro, e o merceeiro e o porteiro desapareceram."]},
 {"t":"sublinhar","g":"cedo","p":"Nesta frase do método, três palavras dizem como é que a maioria de nós falha. Toca nelas.","p2":"Que três palavras da frase dizem o que fazemos mal, e quando? Toca nelas.",
  "frase":"A maioria de nós interrompe demasiado cedo o processo que visa esse conhecimento.","certas":[4,5,6],
  "f":"As três palavras são **interrompe demasiado cedo**: paramos de olhar quando a diferença ainda não apareceu. É o contrário da «longa paciência» que Flaubert pedia a Maupassant.",
  "fe":"Procura o verbo que diz o que fazemos ao processo e as duas palavras que dizem quando."},
 {"t":"vf","g":"banal","p":"Para Flaubert, só as coisas raras têm alguma coisa por descobrir.","p2":"Segundo a lição de Flaubert, as coisas banais não escondem nada.","v":False,
  "f":"Maupassant escreve o contrário: «A mais pequena coisa contém um pouco de desconhecido» (tradução nossa). O merceeiro, o porteiro e o cavalo de fiacre são banais de propósito.",
  "fe":"Volta aos exemplos de Flaubert: um merceeiro, um porteiro, um cavalo de fiacre. Nada mais banal na Paris do século XIX."},
 {"t":"ler","rot":"Ver","titulo":"Um quiosque e uns fiacres","html":ATGET},
 {"t":"escolha","g":"deduzo","p":"Na fotografia de Atget, junto ao quiosque, está um homem de capa comprida e chapéu. Qual destas notas já é uma inferência?","p2":"Três notas sobre o homem de capa da fotografia. Que nota passa do que se vê para o que se supõe?",
  "o":["É um cocheiro à espera de clientes.","Tem uma capa comprida e um chapéu.","Está de pé, ao lado de um candeeiro."],"c":0,
  "f":"A capa, o chapéu e o candeeiro veem-se. Dizer que é um cocheiro à espera de clientes junta pistas (a capa, os fiacres atrás), mas a fotografia não o prova: vai para a coluna «concluo». Repara no homem sentado no alto de um fiacre, na ponta esquerda: o sítio onde está é uma pista mais forte do que uma capa.",
  "fe":["","A capa e o chapéu estão à vista de qualquer pessoa. É observação.","O homem e o candeeiro estão na fotografia. É observação, e situa-o."]},
 {"t":"ler","rot":"Na aula","titulo":"O teu «cocheiro»","html":NA_AULA},
 # 01/11/2026 (correção 5, revisor de pt-PT): no retorno, as palavras citadas como palavras vão entre aspas, como no «fe»
 {"t":"escolha","g":"fila","p":"Caso inventado: cinco chaves numa mesa. Qual destas descrições passaria na fila de reconhecimento?","p2":"Caso inventado: que descrição permitiria a um estranho escolher a chave certa entre cinco?",
  "o":["A do dente do meio gasto até brilhar.","Uma chave prateada, bonita e útil.","A que abre a porta da minha casa."],"c":0,
  "f":"Só o dente gasto se vê e é só daquela chave. «Prateada» e «útil» servem para quase todas, «bonita» é uma opinião, e abrir a porta de casa é verdade, mas não se vê na mesa.",
  "fe":["","Prateadas e úteis são quase todas. «Bonita» é uma opinião: ninguém reconhece uma chave por ela.","É verdade, mas quem procura a chave na mesa não vê a tua porta. Uma descrição para reconhecer tem de mostrar o que está à vista."]},
 {"t":"vf","g":"exata","p":"Para distinguir uma coisa, uma palavra rara vale mais do que a palavra exata.","p2":"Para distinguir uma coisa, mais vale uma palavra difícil do que a palavra certa.","v":False,
  "f":"Maupassant resume assim as ideias de Flaubert sobre o estilo: «seja qual for a coisa que se queira dizer, só há uma palavra para a exprimir, um verbo para a animar e um adjetivo para a qualificar» (tradução nossa). Exata, não rara.",
  "fe":"Uma palavra rara chama a atenção para si; uma palavra exata chama a atenção para a coisa. Na fila de reconhecimento, qual delas ajuda?"},
 {"t":"completar","g":"materias","p":"Completa a frase do método sobre o que é preciso juntar.","p2":"Completa: de que tipos são as matérias-primas de uma ideia, segundo o método?",
  "frase":"«As matérias-primas que é necessário recolher são de dois tipos: [1] e [2].»",
  "lacunas":[{"o":["específicas","verdadeiras","escolhidas"],"c":0},{"o":["gerais","novas","raras"],"c":0}],
  "f":"**Específicas** (as do problema, como o teu «cocheiro») e **gerais** (tudo o que vais juntando sobre a vida). Hoje juntaste material específico; na sessão 3, juntas o geral.",
  "fe":"O método opõe o material do problema concreto ao material que se junta a vida inteira."},
 {"t":"escolha","g":"prova","p":"Porque é que a fila de reconhecimento prova mais do que a opinião de quem escreveu a linha?","p2":"O que torna a fila de reconhecimento uma prova melhor do que a opinião do autor?",
  "o":["Testa a linha em quem não sabe o que é.","Quem escreve gosta sempre do que escreveu.","Assim todos os pares têm a mesma nota."],"c":0,
  "f":"Quem escreveu sabe o que descreve e lê na linha o que lá não está. Só quem não sabe mostra se a linha chega. É a mesma ideia do passo 5 do método: levar a ideia a quem a pode criticar.",
  "fe":["","Pode ser verdade, mas não é isso que faz da fila uma prova. O que conta é testar a linha em quem não sabe o que descreves.","A fila não serve para igualar notas. Serve para saber se a linha funciona sem o autor ao lado a explicar."]},
 {"t":"ordenar","g":"viagem","p":"Põe por ordem a viagem do conselho, de Paris até ti.","p2":"Que caminho fez o conselho de Flaubert até chegar a esta sessão?",
  "passos":["Flaubert dá o conselho ao jovem Maupassant.","Maupassant conta-o no prefácio de 1888.","O livro do método conta-o à sua maneira, em 1940.","Lês a versão de 1940, em tradução nossa."],
  "f":"Em cada etapa da viagem, o conselho pode mudar. Por isso, quando uma citação te interessa, segue-a até à fonte."},
 {"t":"ler","rot":"Para levar","escuro":True,"html":LEVAR},
]
# 01/11/2026 (correção 2, diretor de arte): nos cartões de ler, as formas verbais com pronome não se partem no hífen
# (nq() de tools/licoes_lente.py; a regra .nq está em assets/licoes/laboratorio.css)
_spec = importlib.util.spec_from_file_location('licoes_lente', pathlib.Path(__file__).resolve().parents[1] / 'licoes_lente.py')
LL = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(LL)
for c in cartoes:
    if c['t'] == 'ler':
        c['html'] = LL.nq(c['html'])
dados = {
 "id":"ideias-s02","familia":"laboratorio","chave":"epi-lab-ideias-s02","versao":"2026-10-31-1",
 "marca":"Ideias","passo":"Passo 1 de 5","titulo":"Sessão 2: O cocheiro","h1":"Laboratório, Ideias, sessão 2: O cocheiro",
 "seccao":{"nome":"Ideias","subtitulo":"Como nasce uma ideia","url":LENTE + "narrativas/ideias/","sessoes":7,"rotulo":"As sete sessões"},
 "saida":"narrativas/ideias/sessao-02/index.html","piloto":True,
 "seguinte":"../","seguinteRotulo":"As sete sessões",
 "fontes":"James Webb Young, _A Technique for Producing Ideas_ (Advertising Publications, 1940; edição de 1960), tradução nossa. Guy de Maupassant, «Le Roman», prefácio de _Pierre et Jean_, 1888 (Project Gutenberg, n.º 11131), tradução nossa. Eugène Atget, _Kiosque et fiacres, Paris_, Musée Carnavalet, Histoire de Paris (Paris Musées, CC0). Consultadas a 31/10/2026. O caso das chaves é inventado.",
 "cartoes":cartoes,
}
p = pathlib.Path(__file__).with_suffix('.json')
p.write_text(json.dumps(dados, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print(p, len(cartoes), 'cartões', sum(1 for c in cartoes if c['t'] != 'ler'), 'de fazer')
