# Fonte da sessão 1 de «Ideias», o coração do Laboratório (piloto escondido de 31/10/2026; plano em coracao/plano.md, no
# caderno de bordo). Corre-se para escrever o .json ao lado; o .json é que o gerador (tools/licoes_lente.py) lê.
# Escreve-se em Python para não ter de escapar aspas à mão.
#
# 01/11/2026 (método, encargo do docente «assumir o método de Young, passo a passo»): o «Abre» situa o método (passo 1 de 5,
# o que o passo pede e porque vem agora, os cinco passos numa linha com o de hoje marcado); um cartão novo, «O método», apresenta
# Young uma vez (quem é, quando escreveu, porque o seguimos) com a frase dele que resume o método, conferida em
# biblioteca-young/texto.txt, capítulo «Ideias São Novas Combinações»; nos outros cartões o método trabalha sem se anunciar
# («O método não pede que decores»); o «Para levar» diz que passo se fez e o que vem a seguir; a marca da casca diz «passo 1 de
# 5» (campo «passo»). O cartão novo muda a ordem: a versão sobe para 2026-11-01-1 e o progresso guardado da versão anterior
# recomeça no primeiro cartão (jogo.js; a entrada deixa de a mostrar como feita). As perguntas, as respostas certas, a chave e
# os 13 cartões de fazer não mudam.
#
# 01/11/2026 (correção 1 do método): a fonte do cartão «O método» com o título do livro como no texto (revisor de pt-PT); no
# retorno do atol, a citação volta a ter dono, «diz o livro», sem o nome (revisor); no retorno dos cartões, «O conselho dos
# cartões não fala de mostrar trabalho…» (era «O método…», e o passo 5 do método é levar a ideia à crítica; verificador).
#
# 01/11/2026 (correção 4, revisor de pt-PT): no emparelhar «estatuto», o quarto par na forma dos outros três («Uma pergunta:
# fica por investigar.»).
# 01/11/2026 (correção 3): o texto do revisor de pt-PT e os factos do verificador (o retorno do resumo de Herman, «apontar no quadro o que ela diz» e «o que não se vê numa imagem»).
#
# Fontes lidas a 31/10/2026, um pedido de cada vez (nada citado de memória):
# - Arthur Conan Doyle, «A Scandal in Bohemia», The Strand Magazine, julho de 1891:
#   https://www.gutenberg.org/cache/epub/1661/pg1661.txt (os dezassete degraus; «my eyes are as good as yours»).
# - Amy E. Herman, «How art can help you analyze», TED-Ed: https://ed.ted.com/lessons/how-art-can-help-you-analyze-amy-e-herman
#   (descrição oficial e duração PT290S); oEmbed do YouTube: «How art can help you analyze - Amy E. Herman», canal TED-Ed.
# - Georges de La Tour, The Fortune-Teller: API do Met, objeto 436838 (isPublicDomain true; 60.30; Rogers Fund, 1960).
#   Imagem: images.metmuseum.org, DP-14286-015, reduzida a 1200 px (assets/laboratorio/ideias/latour-leitora-da-sina.webp).
#   As zonas dos cartões «mapa» foram medidas nessa imagem (coordenadas de 1000 × 827) e conferidas a ver.
# - James Webb Young, Uma Técnica para Produzir Ideias, tradução nossa (texto de trabalho no caderno de bordo,
#   biblioteca-young/texto.txt).
# - Universidade Aalto, Diving into Radical Creativity, «Ideation» (parte pública):
#   https://divingintoradicalcreativity.aalto.fi/sub-chapter/observing-andideation/ («The creative process starts with observation.»).
import importlib.util, json, pathlib

LENTE = 'https://pedrohfernandes-klk.github.io/lente/'
IMG = '../../../assets/laboratorio/ideias/'
AALTO = 'https://divingintoradicalcreativity.aalto.fi/sub-chapter/observing-andideation/'
TEDED = 'https://ed.ted.com/lessons/how-art-can-help-you-analyze-amy-e-herman'

# 01/11/2026 (método): os cinco passos, com os nomes da entrada (tools/ideias_piloto.py, PASSOS), conferidos no resumo de
# Young (capítulo «A Fase Final»: a recolha, o tratamento mental, a incubação, o nascimento da ideia, a moldagem). O de hoje leva
# a palavra «hoje» (texto, não só cor) e aria-current.
PASSOS = ['Juntar material', 'Trabalhar o material', 'Largar', 'A ideia aparece', 'Dar forma e pôr à prova']


def passos(hoje):
    return ('<ol class="passos-m" aria-label="Os cinco passos do método">'
            + ''.join(f'<li class="hoje" aria-current="step"><b>{n}</b> {t} <span class="hoje-t">hoje</span></li>' if n in hoje
                      else f'<li><b>{n}</b> {t}</li>' for n, t in enumerate(PASSOS, 1)) + '</ol>')


ABRE = (
 '<p class="pergunta-c">Quantos degraus tem a escada que sobes todos os dias?</p>'
 '<p>Escreve o número no caderno, já, sem ir ver e sem perguntar a ninguém. Guarda-o: antes do fim da aula, vais saber se acertaste.</p>'
 '<div class="metodo-linha"><p><b>Passo 1 de 5: juntar material.</b> Estas sete sessões seguem um método de cinco passos para chegar a uma ideia tua. O primeiro pede que olhes e registes antes de concluir. Vem antes dos outros porque, sem material, não há nada em que trabalhar.</p></div>'
 + passos({1}) +
 '<p class="aula-linha"><b>Hoje</b>, 180 minutos com uma pausa: uma conversa de 1891, um quadro com um pormenor escondido e a primeira investigação na escola.</p>')
# 01/11/2026 (método): a apresentação de Young, num cartão próprio e curto. Tudo vem do texto de trabalho (biblioteca-young/
# texto.txt): «executivo numa agência de publicidade em Chicago» (capítulo «Como Começou»); as considerações «primeiro
# apresentadas a alunos de estudos pós-graduados em publicidade na School of Business da Universidade de Chicago» e preparadas
# para «uma aula» (Nota Prévia); a citação, letra a letra, do capítulo «Ideias São Novas Combinações»; a ordem dos passos, dita
# por palavras nossas, é a da frase seguinte do livro («numa ordem definida»). A data (1940) é a da primeira edição, como na
# Biblioteca.
METODO = (
 '<p>James Webb Young foi um publicitário norte-americano. Em 1940 publicou <i>A Technique for Producing Ideas</i>, um livro de poucas páginas, nascido de uma aula na Universidade de Chicago. Ao apresentar o método, escreve:</p>'
 '<blockquote><p>«Esta técnica intelectual consiste em cinco passos. Tenho a certeza de que todos, um por um, são reconhecíveis.»</p></blockquote>'
 # 01/11/2026 (correção 1 do método, revisor de pt-PT): na fonte, o título do livro como no texto do cartão, na entrada, no guia e
 # no menu de fontes (antes, «Uma Técnica para Produzir Ideias», e nada dizia ao aluno que era o mesmo livro)
 '<p class="fonte">James Webb Young, <i>A Technique for Producing Ideas</i>, capítulo «Ideias São Novas Combinações». Tradução nossa.</p>'
 '<p>Os passos dão-se por ordem. Há outros métodos; seguimos este por ser simples e claro, por fazer sentido e por ajudar de facto. Aprende-o aqui, para depois o usares por tua conta.</p>')
DECIDE = (
 '<p>As ideias caem do céu?</p>'
 '<p class="pergunta-c">Decide em silêncio, de braço no ar: sim, não ou depende.</p>'
 '<details class="lado"><summary>A razão de quem diz que sim</summary><div><p>O livro do método diz que a ideia chega quando menos se espera: «enquanto se faz a barba, no banho, ou, mais vulgarmente, enquanto estamos ainda meio acordados, de manhã».</p></div></details>'
 '<details class="lado"><summary>A razão de quem diz que não</summary><div><p>O mesmo livro compara uma ideia a um atol, uma ilha de coral que aparece de repente no meio do mar. Parece magia, mas é obra de corais que trabalham debaixo de água, sem ninguém os ver.</p></div></details>'
 '<details class="lado"><summary>Uma objeção</summary><div><p>Se uma ideia dá assim tanto trabalho, porque é que não aparece à hora marcada?</p></div></details>'
 '<p>Não há resposta certa neste cartão. Guarda a tua posição: voltas a ela na última sessão.</p>')
HOLMES = (
 '<p>Em 1891, numa revista de Londres, Arthur Conan Doyle publicou um conto em que o médico Watson visita o amigo Sherlock Holmes e lhe diz que tem olhos tão bons como os dele. Holmes responde:</p>'
 '<blockquote><p>«Vê, mas não observa. A diferença é clara. Por exemplo, já viu muitas vezes os degraus que sobem da entrada até esta sala.»</p>'
 '<p>«Muitas vezes.»</p><p>«Quantas?»</p><p>«Bem, umas centenas.»</p><p>«Então, quantos são?»</p><p>«Quantos? Não sei.»</p>'
 '<p>«Exatamente! Não observou. E, no entanto, viu. É isso que eu quero dizer. Ora, eu sei que são dezassete degraus, porque vi e observei.»</p></blockquote>'
 '<p class="fonte">Arthur Conan Doyle, «A Scandal in Bohemia», <i>The Strand Magazine</i>, julho de 1891. Tradução nossa.</p>')
HERMAN = (
 '<p>Amy\u00a0E.\u00a0Herman é historiadora de arte. Nesta lição do TED-Ed, explica porque é que analisar quadros pode preparar médicos, enfermeiros e polícias para investigar no mundo real. No resumo oficial, o exemplo é <i lang="en">Time Transfixed</i>, do pintor belga René Magritte.</p>'
 '<p class="pergunta-c">Enquanto vês, faz duas colunas no caderno: o que está em cada quadro que o vídeo mostra e o que lá não está, mas conta.</p>'
 '<div class="yt" data-yt="ubEadhXWwV4" data-titulo="How art can help you analyze, TED-Ed">'
 '<button type="button" class="yt-abrir" data-yt-abrir><span>Ver: «<span lang="en">How art can help you analyze</span>» (4\u00a0min\u00a050\u00a0s)</span></button>'
 '<p class="yt-cred">TED-Ed, lição de Amy\u00a0E.\u00a0Herman. É em inglês: ativa as legendas no leitor. O vídeo só se liga ao YouTube quando tocas no botão.</p></div>')
LATOUR = (
 f'<figure class="fig inteiro"><span class="moldura"><img src="{IMG}latour-leitora-da-sina.webp" '
 'alt="Um rapaz de colete de couro e faixa à cintura, entre quatro mulheres. À direita, uma velha mostra-lhe uma moeda e ele estende a mão aberta; junto à cintura dele e junto à corrente que lhe cai do peito há mãos das outras mulheres." loading="lazy"></span>'
 '<figcaption>Georges de La Tour, <i>The Fortune-Teller</i> (<i>A leitora da sina</i>, título nosso), provavelmente da década de 1630. Óleo sobre tela, 101,9 × 123,5 cm. '
 '<a href="https://www.metmuseum.org/art/collection/search/436838">The Metropolitan Museum of Art</a>, Nova Iorque, 60.30. Domínio público (Open Access).</figcaption></figure>'
 # 01/11/2026 (método; padrão 13 dos cartões, «Observar a sério», decisão 92): primeiro o quadro inteiro, depois ampliado
 '<p>Agora é a tua vez: dois minutos em silêncio. Vê primeiro o quadro inteiro; depois amplia-o e procura as mãos. Ainda não concluas nada.</p>'
 '<p class="pergunta-c">Escreve no caderno cinco coisas que se veem. Só o que se vê: nada de «parece» nem de «está a pensar».</p>')


def quadro(zonas, rotulo):
    """A figura de um cartão «mapa» sobre o quadro: a imagem e um anel por zona (com halo, para se ver no claro e no
    escuro da pintura). As coordenadas são de 1000 × 827, medidas na imagem do repositório (1200 × 992)."""
    g = ''.join(f'<g class="op-m" data-j="{j}" tabindex="0" role="button" aria-label="{n}">'
                f'<circle class="halo" cx="{x}" cy="{y}" r="40"/><circle class="anel" cx="{x}" cy="{y}" r="40"/></g>'
                for j, (n, (x, y)) in enumerate(zonas))
    return (f'<svg viewBox="0 0 1000 827" role="group" aria-label="{rotulo}">'
            f'<image href="{IMG}latour-leitora-da-sina.webp" width="1000" height="827" aria-hidden="true"/>{g}</svg>')


# Zonas (nome, centro): conferidas a 31/10 sobre a imagem, com as mãos ampliadas.
# 01/11/2026 (correção 5, revisor de pt-PT): os nomes com maiúscula inicial, porque o motor mostra a zona escolhida sozinha
# numa linha por baixo do quadro («A moeda entre os dedos?»); o tamanho das opções não muda.
CORDAO = [('A mão do punho de renda', (240, 645)), ('A mão do rapaz, na anca', (278, 515)),
          ('A moeda entre os dedos', (582, 418)), ('O laço da faixa à cintura', (431, 481))]
MEDALHA = [('O par de mãos ao centro', (600, 615)), ('A mão mais baixa da velha', (712, 582)),
           ('A mão aberta do rapaz', (556, 486)), ('A moeda entre os dedos', (582, 418))]
# 01/11/2026 (correção 5, revisor de pt-PT): «um por nota» e não «um de cada vez», que logo a seguir a «Cada um» se lia
# também como «à vez»; o guia (um facto de cada vez) e a grelha (factos registados um a um) dizem o mesmo.
NA_AULA = (
 '<p><b>O que se faz.</b> Em grupos de três, vão a um lugar da escola por onde todos passam (a escada, o portão, o bar). Cada um regista os seus factos, um por nota; o grupo escolhe dez que outro grupo possa confirmar e junta-lhes três inferências e uma pergunta. Depois, os grupos trocam de lugar e confirmam ou desmentem os factos uns dos outros. Pelo caminho, contam os degraus da escada.</p>'
 '<p><b>Quanto tempo.</b> 70 minutos, com a pausa.</p>'
 '<p><b>O que fica escrito.</b> O auto de observação do grupo, no guião; os teus factos, onde guardas o material; o número de degraus, contado por dois grupos.</p>')
LEVAR = (
 '<p class="levar">Ver não custa nada. Observar é contar os degraus.</p>'
 '<p><b>Fizeste o passo 1 de 5, juntar material:</b> separaste o que se vê do que se conclui, num quadro e na escola. Volta ao número que escreveste no início: acertaste?</p>'
 '<p><b>As frases da sessão</b></p>'
 '<ul><li>Primeiro o que se vê; só depois o que se conclui.</li>'
 '<li>Uma inferência junta factos; uma hipótese ainda está à espera deles.</li>'
 '<li>Se não vês diferença nenhuma, ainda não olhaste o suficiente.</li></ul>'
 '<p><b>No Laboratório:</b> <a href="../../galileu/">Ver, «Observar para transformar», <i>Galileu</i></a>: em 1609, um telescópio mostrou que a Lua não é lisa.</p>'
 '<p><b>Para aprofundar:</b> <a href="../../../investigar/passo-02/">Como se investiga, passo 2, «Olhar e registar»</a>.</p>'
 '<p><b>Para a sessão 2</b>, o mesmo passo, mais fundo: repara num lugar a cinco minutos da escola por onde passas sem olhar e escreve-o no guião. A turma pode ir a um deles.</p>')

cartoes = [
 {"t":"ler","rot":"Abre","titulo":"Dezassete degraus","html":ABRE},
 {"t":"ler","rot":"O método","titulo":"Cinco passos, por ordem","html":METODO},
 {"t":"ler","rot":"Decide","titulo":"O banho e o atol","html":DECIDE},
 {"t":"escolha","g":"atol","p":"Uma ideia é como um atol que aparece de repente no mar. Na comparação, o que são os corais que ninguém vê?","p2":"Se a ideia é o atol, o que são os corais que o construíram debaixo de água?",
  "o":["O trabalho feito antes de a ideia aparecer.","A sorte de estar no sítio certo à hora certa.","Os colegas que copiam a ideia mais tarde."],"c":0,
  "f":"O atol parece surgir do nada, mas, diz o livro, «resulta dos esforços ocultos de inúmeros e invisíveis construtores de coral». A ideia é só a parte que chega à superfície; o trabalho fica por baixo.",
  "fe":["","A sorte não constrói nada debaixo de água. A comparação fala de «processos de construção», isto é, de trabalho que ninguém vê.","Os corais vêm antes do atol, não depois. Copiar só pode acontecer quando a ideia já existe."]},
 {"t":"ler","rot":"Ler","titulo":"Vê, mas não observa","html":HOLMES},
 {"t":"escolha","g":"watson","p":"Watson subiu a escada centenas de vezes e não sabe quantos degraus tem. O que lhe faltou?","p2":"Que faltou a Watson, que viu os degraus centenas de vezes, para saber o número?",
  "o":["Olhar com uma pergunta, e não só de passagem.","Uma vista mais apurada, como a de Holmes.","Mais anos a entrar e a sair daquela casa."],"c":0,
  "f":"Faltou-lhe olhar de propósito: Holmes sabe o número porque quis saber. Observar é ver com uma pergunta.",
  "fe":["","Watson diz que tem olhos tão bons como os de Holmes, e o conto não o desmente. A diferença não está na vista.","Centenas de subidas não lhe deram o número. Mais anos davam-lhe mais subidas, não mais atenção."]},
 {"t":"completar","g":"frase","p":"Completa a frase de Holmes.","p2":"Completa: o que diz Holmes a Watson?",
  "frase":"«Vê, mas não [1]. A diferença é [2].»",
  "lacunas":[{"o":["observa","percebe","conhece"],"c":0},{"o":["clara","subtil","grande"],"c":0}],
  "f":"«Vê, mas não **observa**. A diferença é **clara**.» Para Holmes, ver e observar não são graus da mesma coisa: são duas operações diferentes, e a diferença entre elas não tem nada de subtil.",
  "fe":"Volta à conversa: que palavra opõe Holmes a «ver»? E como é, para ele, a diferença entre as duas?"},
 {"t":"ler","rot":"Ver","titulo":"Um quadro para treinar o olhar","html":HERMAN},
 {"t":"emparelhar","g":"resumo","p":"Do resumo oficial da lição de Herman tirámos quatro elementos. Liga cada um ao papel que tem.","p2":"No resumo oficial da lição de Herman, que papel tem cada um destes elementos?",
  "pares":[["Analisar arte prepara para investigar no mundo real.","A tese"],["Médicos, enfermeiros e polícias.","A quem serve"],["_Time Transfixed_, de René Magritte.","O exemplo"],["O que se vê e o que não se vê.","O que se treina"]],
  "f":"Ler um vídeo como se lê um texto é procurar a tese (analisar arte prepara para investigar), o exemplo que a mostra (um quadro de Magritte), a quem serve (médicos, enfermeiros e polícias) e o que se treina (o que se vê e o que não se vê).",
  "fe":"Pergunta a cada elemento: é o que Herman defende, o caso que usa, a quem serve ou o que se treina?",
  "liga":[{"href":TEDED,"t":"A lição no TED-Ed, com o resumo oficial (em inglês)"}]},
 {"t":"vf","g":"invisivel","p":"Para Herman, o que não está num quadro também pode contar como pista.","p2":"Segundo o resumo oficial da lição de Herman, o que não se vê numa imagem também pode contar.","v":True,
  "f":"O resumo oficial da lição fala de treinar a atenção ao que se vê e ao que não se vê. Numa investigação, o que falta (uma testemunha, uma sombra, um som) também é informação.",
  "fe":"A lição pede atenção às duas coisas: ao que se vê e ao que não se vê. O que falta numa cena também diz alguma coisa."},
 {"t":"ler","rot":"Ver","titulo":"O rapaz e a leitora da sina","html":LATOUR},
 {"t":"mapa","g":"cordao","rot":"Toca no quadro","p":"Toca na mão que segura um cordão com uma borla.","p2":"No quadro, onde está a mão que segura um cordão com uma borla?",
  "o":[n for n, _ in CORDAO],"c":0,"centros":[list(c) for _, c in CORDAO],"rotulo":"Toca numa mão ou num objeto.","rotulo2":"Toca outra vez, no sítio que queres.",
  "fig":quadro(CORDAO,"La Tour, A leitora da sina: quatro zonas para tocar"),
  "f":"À esquerda, junto à cintura do rapaz, a mão da mulher de mangas claras segura um cordão com uma borla. O que vem preso ao cordão não se vê: dizer que é a bolsa dele já é uma inferência.",
  "fe":"Procura do lado esquerdo do quadro, à altura da cintura do rapaz, e segue cada mão até ao ombro de quem a tem: há uma que não é dele."},
 {"t":"mapa","g":"medalha","rot":"Toca no quadro","p":"Segue a corrente que o rapaz traz ao peito, até à medalha. Toca nas mãos que seguram essa corrente.","p2":"Onde estão as mãos que seguram a corrente da medalha do rapaz?",
  "o":[n for n, _ in MEDALHA],"c":0,"centros":[list(c) for _, c in MEDALHA],"rotulo":"Toca numa mão ou num objeto.","rotulo2":"Toca outra vez, no sítio que queres.",
  "fig":quadro(MEDALHA,"La Tour, A leitora da sina: quatro zonas para tocar"),
  "f":"Junto à medalha, duas mãos seguram a corrente do rapaz. Que a estão a cortar é uma inferência: o quadro não mostra o fim do gesto. E repara para onde olha o rapaz enquanto isto acontece.",
  "fe":"Começa no ombro do rapaz e segue a corrente até à medalha, que fica pendurada mais abaixo, ao centro: quem lhe está a tocar?"},
 {"t":"emparelhar","g":"estatuto","p":"Liga cada frase sobre o quadro ao que ela é.","p2":"Que tipo de frase é cada uma destas, sobre o quadro?",
  "pares":[["A velha segura uma moeda entre os dedos.","Um facto: vê-se no quadro."],["O rapaz está a ser roubado.","Uma inferência: junta várias pistas."],["As quatro mulheres combinaram tudo antes.","Uma hipótese: o quadro não a prova."],["Porque é que o rapaz não olha para as mãos?","Uma pergunta: fica por investigar."]],
  "f":"Um facto vê-se; uma inferência junta factos; uma hipótese ainda espera provas; uma pergunta fica por investigar. É a ordem desta sessão: primeiro o que se vê, depois o que se conclui.",
  "fe":"Pergunta a cada frase: consigo apontar no quadro, com o dedo, o que ela diz? Se sim, é um facto. Se preciso de juntar várias coisas, é uma inferência. Se nada no quadro a confirma, é uma hipótese."},
 {"t":"ler","rot":"Na aula","titulo":"O auto de observação","html":NA_AULA},
 {"t":"escolha","g":"confirmar","p":"Três registos inventados de um auto de observação. Qual deles é um facto que outro grupo possa ir confirmar?","p2":"Registos inventados, sobre uma escada da escola: que registo pode outro grupo ir confirmar?",
  "o":["O corrimão tem três parafusos soltos à esquerda.","A escada parece mais antiga do que a escola.","Quem sobe esta escada anda sempre com pressa."],"c":0,
  "f":"Três parafusos soltos contam-se: outro grupo pode ir lá confirmar ou desmentir. A idade que a escada parece ter é uma impressão, e o «sempre» faz da pressa uma generalização.",
  "fe":["","A palavra «parece» denuncia a impressão. Que pormenor te fez achar que é antiga? Esse pormenor, sim, é um facto.","Ninguém pode confirmar «sempre». Quantas pessoas viste subir, e quantas iam a correr? Isso conta-se."]},
 {"t":"sublinhar","g":"superficie","p":"O livro do método explica porque é que tantos param de olhar cedo demais. Toca nas palavras que dizem o erro.","p2":"Que palavras desta frase dizem o erro de quem para de olhar?",
  "frase":"Se as diferenças não forem claramente visíveis à superfície, assumimos que não as há.","certas":[9,10,11,12,13],
  "f":"O erro é que **assumimos que não as há**: como não vemos logo a diferença, decidimos que ela não existe. Watson fez o mesmo com os degraus: viu-os centenas de vezes e nunca achou que houvesse ali alguma coisa para saber.",
  "fe":"O começo da frase descreve a situação: as diferenças não se veem logo. Procura onde a frase diz o que fazemos de errado."},
 {"t":"escolha","g":"cartoes","p":"O método aconselha a registar o que se recolhe em cartões brancos de 12,5 por 7,5 centímetros, um assunto por cartão. Para que serve?","p2":"Porque é que o método manda passar a escrito, cartão a cartão, o que se recolhe?",
  "o":["Obriga a escrever e mostra o que falta.","Prova ao docente que trabalhaste muito.","Ajuda a decorar os factos para um teste."],"c":0,
  "f":"O livro diz que o registo ajuda a «dar ordem ao trabalho» e a «evidenciar as falhas no conhecimento», e que obriga o cérebro «a passar pelo processo de expressar os conteúdos pesquisados em forma escrita». Cartões, caderno ou telemóvel: escolhe a forma, mas regista uma coisa de cada vez.",
  "fe":["","O conselho dos cartões não fala de mostrar trabalho a ninguém. Fala do que a escrita faz a quem escreve.","O método não pede que decores. Escrever serve para pensar e para ver o que ainda não se sabe."]},
 {"t":"vf","g":"aalto","p":"No curso aberto da Universidade Aalto sobre criatividade, o processo criativo começa pela observação.","p2":"Segundo o curso da Universidade Aalto, a criatividade começa por observar.","v":True,
  "f":"Na parte pública do curso _Diving into Radical Creativity_, a Universidade Aalto, na Finlândia, escreve: «The creative process starts with observation» (o processo criativo começa com a observação; tradução nossa).",
  "fe":"Holmes, Herman e o curso da Aalto dizem o mesmo por outras palavras: antes das ideias, é preciso material, e o material recolhe-se a olhar.",
  "liga":[{"href":AALTO,"t":"Universidade Aalto, _Diving into Radical Creativity_: «Ideation» (em inglês)"}]},
 {"t":"ordenar","g":"metodo","p":"Põe por ordem a observação desta sessão, do primeiro ao último gesto.","p2":"Em que ordem se faz a observação desta sessão?",
  "passos":["Olhar em silêncio, sem concluir nada.","Escrever só o que se vê.","Juntar factos numa inferência.","Procurar um facto que a desminta."],
  "f":"Primeiro olhar, depois registar, depois concluir. Por fim, o gesto do detetive honesto: antes de acreditares na tua inferência, procura o que a deitaria abaixo."},
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
 "id":"ideias-s01","familia":"laboratorio","chave":"epi-lab-ideias-s01","versao":"2026-11-01-1",
 "marca":"Ideias","passo":"Passo 1 de 5","titulo":"Sessão 1: Ver ou observar?","h1":"Laboratório, Ideias, sessão 1: Ver ou observar?",
 "seccao":{"nome":"Ideias","subtitulo":"Como nasce uma ideia","url":LENTE + "narrativas/ideias/","sessoes":7,"rotulo":"As sete sessões"},
 "saida":"narrativas/ideias/sessao-01/index.html","piloto":True,
 "seguinte":"../sessao-02/","seguinteRotulo":"Sessão 2: O cocheiro",
 "fontes":"Arthur Conan Doyle, «A Scandal in Bohemia», _The Strand Magazine_, julho de 1891 (Project Gutenberg, n.º 1661), tradução nossa. Amy\u00a0E.\u00a0Herman, «How art can help you analyze», lição do TED-Ed (ed.ted.com e canal oficial do TED-Ed no YouTube). Georges de La Tour, _The Fortune-Teller_, The Metropolitan Museum of Art, Nova Iorque (Open Access, domínio público). James Webb Young, _A Technique for Producing Ideas_ (Advertising Publications, 1940; edição de 1960), tradução nossa. Universidade Aalto, _Diving into Radical Creativity_, «Ideation» (parte pública), citação curta. Consultadas a 31/10/2026. Os registos do auto de observação são inventados.",
 "cartoes":cartoes,
}
p = pathlib.Path(__file__).with_suffix('.json')
p.write_text(json.dumps(dados, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print(p, len(cartoes), 'cartões', sum(1 for c in cartoes if c['t'] != 'ler'), 'de fazer')
