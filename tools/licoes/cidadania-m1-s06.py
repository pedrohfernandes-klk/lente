# Fonte da sessão 06 do M1 de Cidadania (piloto de 31/10/2026, no molde da sessão 01). Corre-se para escrever o .json
# ao lado; o .json é que o gerador (tools/licoes_lente.py) lê. Escreve-se em Python para não ter de escapar aspas à mão.
# Lido a 31/10/2026: Constituição (artigo 13.º) e Código do Procedimento Administrativo (artigos 9.º e 69.º) na página da
# Procuradoria-Geral Distrital de Lisboa; Declaração Universal (artigo 1.º) na página do UNRIC; Foot (1967), Thomson
# (1976 e 1985) e Rawls (1971) na Stanford Encyclopedia of Philosophy (entradas «Doctrine of Double Effect» e «John Rawls»).
import json, pathlib
ABRE = (
 '<p class="pergunta-c">Uma regra é justa se a aceitasses sem saber o lugar que te ia calhar?</p>'
 '<p>Caso inventado. Há seis turnos de filmagem para três grupos, A, B e C. O delegado de turma, que está num dos grupos, propõe a regra: primeiro quem tem o guião mais avançado. É o grupo dele.</p>'
 '<p class="aula-linha"><b>Hoje</b>, 180 minutos com uma pausa: decidir, pensar no problema do elétrico e repartir seis turnos sem saber o teu lugar.</p>')
DECIDE = (
 '<p>A regra do delegado pode ficar?</p>'
 '<p class="pergunta-c">Decide em silêncio, de braço no ar: sim, não ou depende.</p>'
 '<details class="lado"><summary>A razão do delegado</summary><div><p>«É clara e premeia quem trabalhou. Não a fiz para mim.»</p></div></details>'
 '<details class="lado"><summary>A razão do grupo C</summary><div><p>«Perdemos um turno porque o material prometido não chegou. Com esta regra, perdemos outro.»</p></div></details>'
 '<details class="lado"><summary>Uma objeção</summary><div><p>E se a regra for boa, mas quem a propõe ganhar com ela? Quem a devia propor?</p></div></details>'
 '<p>Não há resposta certa neste cartão. Guarda a tua posição: vais voltar a ela.</p>')
# 31/10/2026 (decisão 18): a imagem e o vídeo da sessão. Gravura do Met (CC0, página do ficheiro no Commons verificada a
# 31/10; o guia do docente leva uma linha de enquadramento por causa dos castigos) e lição do TED-Ed (oEmbed e página da
# lição verificados a 31/10). A versão da ponte não vem da descrição do vídeo: o cartão propõe-na como pergunta nossa.
CARTAZ = (
 '<figure class="fig inteiro"><span class="moldura"><img src="../../../img/cidadania/justica-galle-bruegel.webp" '
 'alt="Gravura a preto e branco cheia de gente. Ao centro, sobre uma base com a palavra IUSTICIA, uma mulher de olhos vendados segura uma espada e uma balança, rodeada de soldados com lanças. À direita, escrivães e juízes numa sala de tribunal; à esquerda e ao fundo, cenas de castigos e de execuções." loading="lazy"></span>'
 '<figcaption>Philips Galle, segundo Pieter Bruegel, o Velho, <i>Justicia</i>, da série <i>As Virtudes</i>, cerca de 1559 a 1560, gravura editada por Hieronymus Cock. Metropolitan Museum of Art, Nova Iorque. CC0.</figcaption></figure>'
 '<p>Ao centro, numa base com a palavra IUSTICIA, a Justiça de olhos vendados segura uma espada e uma balança. À direita, escrivães e juízes; à esquerda e ao fundo, os castigos da época.</p>'
 '<p class="pergunta-c">A Justiça não vê quem julga. Olha à volta dela: ser imparcial chega para ser justo?</p>'
 '<p>Responde no caderno, numa linha. Voltas a esta pergunta no fim da sessão.</p>')
VIDEO = (
 '<p>Um vídeo curto do TED-Ed, numa lição de Eleanor Nelsen, sobre o problema do elétrico: desviá-lo para salvar cinco pessoas, sabendo que morre uma. É em inglês: liga as legendas no leitor.</p>'
 '<p class="pergunta-c">Depois de ver, imagina outra versão: para travar o elétrico, terias de empurrar uma pessoa de uma ponte para a linha. Morre uma e salvam-se cinco, como antes. O que muda?</p>'
 '<div class="yt" data-yt="yg16u_bzjPE" data-titulo="Would you sacrifice one person to save five?, TED-Ed">'
 '<button type="button" class="yt-abrir" data-yt-abrir>Ver: «Would you sacrifice one person to save five?» (4 min 56 s)</button>'
 '<p class="yt-cred">TED-Ed, lição de Eleanor Nelsen. O vídeo só se liga ao YouTube quando tocas no botão.</p></div>'
 '<p>Escreve numa linha a diferença entre desviar e empurrar.</p>')
NA_AULA = (
 '<p><b>O que se faz.</b> Repartir os seis turnos de filmagem sem saber o lugar. Cada grupo escolhe primeiro a regra (igualdade, necessidade, ordem de inscrição, sorteio ou outra) e só depois tira uma carta com o lugar que lhe calha. Quem perde apresenta a objeção e o grupo revê. No fim, a mesma pergunta para o teatro-documento: como se repartem as falas e o tempo de cena?</p>'
 '<p><b>Quanto tempo.</b> 60 a 75 minutos, com a pausa.</p>'
 '<p><b>O que fica escrito.</b> A regra final, quem perde com ela e porque a aceitaria mesmo assim; a regra do grupo para repartir as falas, com o primeiro esboço do guião.</p>')
LEVAR = (
 '<p class="levar">Uma regra justa é a que consegues explicar a quem perde com ela.</p>'
 '<p>Nesta sessão comparaste critérios, separaste o resultado dos limites e viste o que muda quando quem decide ganha com a decisão. Volta à gravura: a venda chegava? E volta à tua posição do início: a regra do delegado ficava?</p>'
 '<p><b>As frases da sessão</b></p>'
 '<ul><li>Quem ganha com a regra não deve decidi-la sozinho.</li>'
 '<li>Há coisas que não se fazem a uma pessoa, nem para salvar mais.</li>'
 '<li>Igualdade, necessidade e ordem são critérios diferentes, com efeitos diferentes.</li>'
 '<li>Antes de votar uma regra, imagino-me no pior lugar.</li></ul>')

cartoes = [
 {"t":"ler","rot":"Abre","titulo":"Uma regra para quem perde","html":ABRE},
 {"t":"ler","rot":"Decide","titulo":"A regra do delegado","html":DECIDE},
 {"t":"escolha","g":"delegado","p":"Que problema tem a regra do delegado, mesmo sendo clara?","p2":"A regra do delegado é clara. O que a torna difícil de aceitar?",
  "o":["Quem a propõe é quem mais ganha com ela.","Não diz quantos turnos há para repartir.","Foi proposta sem uma votação de braço no ar."],"c":0,
  "f":"Uma regra pode ser clara e premiar o trabalho e, mesmo assim, levantar dúvidas: quem a propôs é quem mais ganha com ela. É o que se chama um conflito de interesses.",
  "fe":["","O número está no caso: seis turnos para três grupos. O problema está em quem decide e em quem ganha.","Uma votação pode vir depois. Antes disso, há a dúvida sobre quem propôs a regra e quem ganha com ela."]},
 {"t":"emparelhar","g":"criterios","p":"Liga cada critério ao que ele faz aos seis turnos.","p2":"Que efeito tem cada critério na divisão dos seis turnos?",
  "pares":[["Igualdade","Dois turnos para cada grupo"],["Necessidade","Mais turnos para quem perdeu material"],["Ordem de inscrição","Primeiro quem se inscreveu primeiro"],["Sorteio","Ninguém escolhe quem fica com o quê"]],
  "f":"Cada critério é defensável e cada um deixa alguém a perder. Escolher a regra é escolher quem perde e porquê.",
  "fe":"Lê o critério e pergunta: com ele, quem recebe mais?"},
 # 31/10/2026 (revisão de pt-PT): o vídeo vem antes do elétrico e da ponte, para a tarefa não repetir uma pergunta já respondida.
 {"t":"ler","rot":"Ver","titulo":"Desviar ou empurrar?","html":VIDEO},
 {"t":"escolha","g":"eletrico","p":"Um elétrico desgovernado vai atropelar cinco trabalhadores. Se puxares uma alavanca, desvia-se para uma linha onde está um só. Que razão defende puxar a alavanca?","p2":"Elétrico desgovernado: cinco pessoas numa linha, uma na outra. Que razão defende desviá-lo?",
  "o":["Morre uma pessoa em vez de cinco.","A alavanca está mesmo ao teu lado.","Ninguém vai saber quem a puxou."],"c":0,
  "f":"É uma razão de consequências: pesa-se o resultado e salvam-se mais vidas. Casos como este vêm de um artigo da filósofa Philippa Foot, de 1967.",
  "fe":["","Estar perto torna o gesto possível, mas não diz se é certo fazê-lo. A razão tem de falar das pessoas na linha.","Ninguém saber não torna nada certo nem errado. A razão tem de falar do que acontece às pessoas."]},
 {"t":"escolha","g":"ponte","p":"Outra versão: só travas o elétrico se empurrares uma pessoa de uma ponte para a linha. Morre uma, salvam-se cinco. Que razão explica que muitos recusem empurrar?","p2":"Empurrar uma pessoa para a linha também salvaria cinco. Porque é que muitos recusam?",
  "o":["Seria usar uma pessoa como meio para salvar outras.","A ponte é alta e podias cair também na linha.","Empurrar alguém exige mais força do que puxar."],"c":0,
  "f":"Na alavanca, a morte de um é um efeito do desvio. Na ponte, a pessoa é usada como meio para travar o elétrico. Para muitos, isso não se faz a ninguém, mesmo para salvar mais. A Declaração Universal começa por aí: todos nascem iguais em dignidade (artigo 1.º).",
  "fe":["","O risco para ti não explica a diferença. Imagina que não havia risco nenhum: muitos continuariam a recusar.","A força não muda o que se faz à pessoa. A diferença está em usá-la como meio."]},
 {"t":"ler","rot":"Ver","titulo":"A Justiça de olhos vendados","html":CARTAZ},
 {"t":"vf","g":"maioria","p":"Se a maioria vota uma regra, a regra é justa.","p2":"Uma regra aprovada pela maioria é, por isso, uma regra justa.","v":False,
  "f":"A votação diz quantos aceitam a regra, não se ela é justa. Uma maioria pode aprovar uma regra que prejudica sempre os mesmos. Por isso se pergunta também quem perde e porquê.",
  "fe":"Pensa no grupo C: se os outros dois grupos votassem tirar-lhe os turnos, a regra passava a ser justa?"},
 {"t":"ordenar","g":"passos","p":"Põe por ordem os passos para escolher uma regra justa.","p2":"Qual é a ordem para chegar a uma regra justa?",
  "passos":["Listar os critérios possíveis.","Escolher um sem saber o lugar que te calha.","Ouvir quem perde com a regra escolhida.","Rever a regra, se a objeção for boa."],
  "f":"Primeiro as opções, depois a escolha às cegas, depois a voz de quem perde e, no fim, a revisão. A ideia de escolher regras sem saber o lugar que nos calha vem do filósofo John Rawls, em _A Theory of Justice_ (1971)."},
 {"t":"escolha","g":"gravura","p":"Na gravura, a Justiça tem os olhos vendados. O que quer dizer a venda?","p2":"Porque é que a Justiça da gravura não vê?",
  "o":["Julga sem olhar a quem está a ser julgado.","Não quer ver os castigos que estão à volta.","Foi castigada e perdeu o direito de ver."],"c":0,
  "f":"A venda lê-se como imparcialidade: a decisão não deve mudar consoante quem é a pessoa. Mas olha outra vez à volta da Justiça: ser imparcial chega para ser justo?",
  "fe":["","A venda diz como se deve julgar, não o que a Justiça quer evitar ver. Repara no que ela continua a segurar.","Nada na gravura mostra a Justiça castigada. A venda é um atributo: diz como deve julgar."]},
 {"t":"vf","g":"mesma","p":"Aplicar a mesma regra a situações diferentes garante, por si só, que a decisão é justa.","p2":"Tratar todos pela mesma regra chega sempre para ser justo.","v":False,
  "f":"A Constituição diz que todos são iguais perante a lei (artigo 13.º). Mas o grupo C perdeu um turno sem culpa: dar dois a cada grupo é igual para todos e não repara essa perda. Às vezes, ser justo é ter em conta a situação de cada um.",
  "fe":"Volta ao grupo C: a mesma regra para todos apaga o turno que já perdeu?"},
 {"t":"ler","rot":"Na aula","titulo":"Repartir sem saber o lugar","html":NA_AULA},
 {"t":"escolha","g":"jurado","p":"Caso inventado: num concurso de curtas da escola, um dos jurados é irmão de um concorrente. Que deve ele fazer?","p2":"O irmão de um concorrente está no júri do concurso de curtas. O que deve fazer?",
  "o":["Afastar-se da decisão sobre essa curta.","Votar, desde que prometa ser imparcial.","Dar menos pontos ao irmão, para compensar."],"c":0,
  "f":"Mesmo que decida bem, a relação levanta dúvidas sobre a decisão. Na Administração Pública, o Código do Procedimento Administrativo impede de intervir quem tem um irmão interessado no procedimento (artigo 69.º). Na escola, a mesma ideia ajuda: quem tem um interesse afasta-se.",
  "fe":["","A promessa não apaga a dúvida dos outros concorrentes. Afastar-se protege a decisão e o próprio jurado.","Dar menos pontos também é decidir pela relação, não pela curta. Continua a não ser imparcial."]},
 {"t":"completar","g":"criterios2","p":"Completa o que cada critério faz.","p2":"Que palavras completam a definição dos três critérios?",
  "frase":"A igualdade dá [1] a todos; a necessidade dá mais a quem [2]; a ordem de inscrição premeia quem [3].",
  "lacunas":[{"o":["o mesmo","mais","menos"],"c":0},{"o":["precisa","trabalhou","pede"],"c":0},{"o":["chega primeiro","faz melhor","tem mais votos"],"c":0}],
  "f":"Igualdade: o mesmo para todos. Necessidade: mais a quem precisa. Ordem: quem chega primeiro. São critérios diferentes, com efeitos diferentes.",
  "fe":"Volta aos seis turnos: com cada critério, quem fica com mais?"},
 {"t":"vf","g":"conflito","p":"Há conflito de interesses mesmo que a pessoa acabe por decidir bem.","p2":"Um conflito de interesses existe ainda que a decisão tomada seja a correta.","v":True,
  "f":"O conflito está na situação, não no resultado: quem decide tem um interesse próprio na decisão. O Código do Procedimento Administrativo pede soluções que preservem a isenção e a «confiança nessa isenção» (artigo 9.º): a confiança perde-se antes de se saber como a pessoa decide.",
  "fe":"Pensa no delegado: mesmo que a regra fosse boa, os outros grupos tinham razões para duvidar."},
 {"t":"escolha","g":"falas","p":"No teatro-documento, que regra para repartir as falas se consegue explicar a quem fala menos?","p2":"Que regra das falas aguenta a pergunta de quem ficou com menos?",
  "o":["A que se combina antes e diz o critério usado.","A que dá mais falas a quem fala mais alto.","A que se decide no dia, conforme quem aparece."],"c":0,
  "f":"Uma regra combinada antes, com o critério dito, pode ser explicada a quem perde: sabe porquê e pôde objetar. Uma regra feita no momento, ou à medida de alguém, não se explica.",
  "fe":["","Falar alto não é um critério que se explique a quem é mais calado. Premeia um feitio, não o trabalho.","Decidir no dia deixa tudo ao acaso de quem chega. Quem fala menos não teve como objetar."]},
 {"t":"ler","rot":"Para levar","escuro":True,"html":LEVAR},
]
dados = {
 "id":"cidadania-m1-s06","chave":"epi-cid-m1-s06","versao":"2026-10-31-2",
 "marca":"CD","titulo":"Sessão 06: Uma regra para quem perde","h1":"Cidadania, módulo 1, sessão 06: Uma regra para quem perde",
 "modulo":{"n":1,"nome":"Ser-se humano","url":"https://pedrohfernandes-klk.github.io/lente/cidadania/piloto/m1/"},
 "saida":"cidadania/piloto/m1-s06/index.html","piloto":True,
 "seguinte":"../m1-s07/","seguinteRotulo":"Sessão 07: Nove contra dois",
 "fontes":"Constituição da República Portuguesa, artigo 13.º; Declaração Universal dos Direitos Humanos (1948), artigo 1.º, no texto do Ministério Público (https://dcjri.ministeriopublico.pt/sites/default/files/documentos/pdf/declaracao_universal_dos_direitos_do_homem_5.pdf); Código do Procedimento Administrativo (Decreto-Lei n.º 4/2015), artigos 9.º e 69.º. O problema do elétrico: Philippa Foot, «The Problem of Abortion and the Doctrine of the Double Effect» (1967), e Judith Jarvis Thomson, «The Trolley Problem» (1985). Escolher regras sem saber o lugar: John Rawls, _A Theory of Justice_ (1971). Imagem: Philips Galle, segundo Pieter Bruegel, o Velho, _Justicia_, da série _As Virtudes_, cerca de 1559 a 1560 (Metropolitan Museum of Art, CC0). Vídeo: TED-Ed, «Would you sacrifice one person to save five?», lição de Eleanor Nelsen. Os casos são inventados.",
 "cartoes":cartoes,
}
p = pathlib.Path(__file__).with_suffix('.json')
p.write_text(json.dumps(dados, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print(p, len(cartoes), 'cartões', sum(1 for c in cartoes if c['t'] != 'ler'), 'de fazer')
