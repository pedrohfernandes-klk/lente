# Fonte da sessão 02 do M1 de Cidadania (piloto de 31/10/2026, no molde da sessão 01). Corre-se para escrever o .json ao
# lado; o .json é que o gerador (tools/licoes_lente.py) lê. Escreve-se em Python para não ter de escapar aspas à mão.
#
# Fontes lidas a 31/10/2026 (nada citado de memória):
# - Código Civil, artigos 79.º e 81.º: https://www.pgdlisboa.pt/leis/lei_mostra_articulado.php?nid=775&tabela=leis
# - Constituição, artigos 26.º e 34.º: https://www.pgdlisboa.pt/leis/lei_mostra_articulado.php?nid=4&tabela=leis
# - Lei n.º 58/2019, artigo 16.º («Consentimento de menores»): https://www.pgdlisboa.pt/leis/lei_mostra_articulado.php?nid=3118&tabela=leis
# - Convenção sobre os Direitos da Criança, artigo 16.º (texto do Ministério Público):
#   https://gddc.ministeriopublico.pt/sites/default/files/documentos/instrumentos/convencao_sobre_direitos_da_crianca.pdf
# - Fotografia: Lewis Hine, 1910, Library of Congress (cph.3a20286), domínio público («No known restrictions»; PDM no
#   Commons). Página do ficheiro: https://commons.wikimedia.org/wiki/File:Addie_Card,_12_years._Spinner_in_North_Pormal_(i.e.,_Pownal)_Cotton_Mill._Vt._Girls_in_mill_say_she_is_ten_years._She_admitted_to_me_she_was_twelve;_that_she_started_during_school_vacation_LOC_cph.3a20286.jpg
#   Registo: https://www.loc.gov/pictures/item/ncl2004001725/PP/
# - Vídeo: TED, «When AI Can Fake Reality, Who Can You Trust? | Sam Gregory | TED», canal oficial @TED (oEmbed, 31/10),
#   id Hnjr7o-HNx8, 12 min 5 s. Excerto de 0 a 47 s, marcado pela transcrição oficial do TED
#   (https://www.ted.com/talks/sam_gregory_when_ai_can_fake_reality_who_can_you_trust/transcript): o primeiro minuto diz
#   que bastam poucos segundos de voz e poucas imagens da cara para imitar alguém, e que fica mais fácil fabricar a
#   realidade e também desmentir a verdadeira. Escolha provisória (decisão 18: perguntar ao docente); confirmar o excerto
#   com legendas antes de usar com a turma.
import json, pathlib
ABRE = (
 '<p class="pergunta-c">Quem decide o que se faz com a tua imagem?</p>'
 '<p>Caso inventado. No ensaio de quinta-feira, a Marta aceitou ser filmada para o grupo rever a cena. Aos 40 segundos, escorrega e cai. O grupo acha que a cena ficou ótima e quer publicar o vídeo na conta da escola.</p>'
 '<p class="aula-linha"><b>Hoje</b>, 180 minutos com uma pausa: decidir, ver uma fotografia de 1910, separar filmar de publicar e escrever o pedido de consentimento do teu grupo.</p>')
DECIDE = (
 '<p>O grupo pode publicar o vídeo do ensaio?</p>'
 '<p class="pergunta-c">Decide em silêncio, de braço no ar: sim, não ou depende.</p>'
 '<details class="lado"><summary>A razão do grupo</summary><div><p>«A Marta aceitou ser filmada e o vídeo é trabalho da turma. A queda dura dois segundos.»</p></div></details>'
 '<details class="lado"><summary>A razão da Marta</summary><div><p>«Aceitei que o grupo visse o ensaio. Não aceitei a internet, nem a queda.»</p></div></details>'
 '<details class="lado"><summary>Uma objeção</summary><div><p>E se cortarem a queda? E se a escola disser que o vídeo é para fins didáticos?</p></div></details>'
 '<p>Não há resposta certa neste cartão. Guarda a tua posição: vais voltar a ela.</p>')
ART79_3 = 'O retrato não pode, porém, ser reproduzido, exposto ou lançado no comércio, se do facto resultar prejuízo para a honra, reputação ou simples decoro da pessoa retratada.'
FOTO = (
 '<figure class="fig inteiro"><span class="moldura"><img src="../../../img/cidadania/hine-addie-card-1910.webp" '
 'alt="Uma rapariga descalça, de vestido e avental, está de pé numa fábrica, entre duas filas de máquinas de fiar cheias de bobinas, e olha de frente para a câmara." loading="lazy"></span>'
 '<figcaption>Lewis Hine, <i>Addie Card, 12 years. Spinner in North Pormal [i.e., Pownal] Cotton Mill. Vt.</i>, 1910. Library of Congress, National Child Labor Committee Collection. Domínio público.</figcaption></figure>'
 '<p>Nos arquivos do National Child Labor Committee, a legenda desta fotografia dá o nome da rapariga, a idade e a fábrica onde trabalhava.</p>'
 '<p class="pergunta-c">O que acrescenta a legenda ao que se vê? A Addie podia recusar? Um fim bom chega para mostrar o nome?</p>'
 '<p>Responde no caderno, numa linha. Voltas a esta pergunta no fim da sessão.</p>')
NA_AULA = (
 '<p><b>O que se faz.</b> Em grupos de três, quatro situações em papel: o ensaio da Marta, uma fotografia de rua com uma pessoa reconhecível, uma captura de ecrã e a entrevista do projeto. Em cada uma, o grupo decide, lê o efeito, recebe uma informação nova e revê a decisão. No fim, escreve o pedido de consentimento para as entrevistas da Pergunta Humana.</p>'
 '<p><b>Quanto tempo.</b> 60 a 75 minutos, com a pausa.</p>'
 '<p><b>O que fica escrito.</b> O pedido de consentimento do grupo (para quê, que uso, onde fica, como se retira) e a decisão revista de uma das situações. O pedido entra no dossiê da Pergunta Humana.</p>')
VIDEO = (
 '<p>O início de uma conferência TED de Sam Gregory, que dirige a WITNESS, uma organização que ajuda as pessoas a usar o vídeo para defender os seus direitos. É em inglês: liga as legendas no leitor.</p>'
 '<div class="yt" data-yt="Hnjr7o-HNx8" data-ini="0" data-fim="47" data-titulo="When AI Can Fake Reality, Who Can You Trust?, TED">'
 '<button type="button" class="yt-abrir" data-yt-abrir>Ver: «When AI Can Fake Reality, Who Can You Trust?» (excerto, 47 s)</button>'
 '<p class="yt-cred">TED, conferência de Sam Gregory (12 min 5 s; vês só o início). O vídeo só se liga ao YouTube quando tocas no botão.</p></div>'
 '<p class="pergunta-c">Segundo o orador, de quanto precisa alguém para imitar a tua voz e a tua cara? Que dois perigos vêm daí?</p>'
 '<p>Uma linha para cada resposta, no caderno. Depois: o que muda isto na decisão sobre o vídeo da Marta?</p>')
LEVAR = (
 '<p class="levar">Aceitar ser filmado não é aceitar ser publicado.</p>'
 '<p>Nesta sessão separaste filmar, guardar e publicar, e viste que o consentimento vale para um uso. Volta à pergunta da fotografia de 1910: um fim bom chega para mostrar o nome? Mudou a tua resposta?</p>'
 '<p><b>As frases da sessão</b></p>'
 '<ul><li>O consentimento é para um uso, não para todos.</li>'
 '<li>Posso retirar o consentimento; quem publicou tem de me ouvir.</li>'
 '<li>Fins didáticos não autorizam expor alguém ao ridículo.</li>'
 '<li>Antes de partilhar, pergunto a quem aparece.</li></ul>')

cartoes = [
 {"t":"ler","rot":"Abre","titulo":"A imagem dos outros","html":ABRE},
 {"t":"ler","rot":"Decide","titulo":"O vídeo do ensaio","html":DECIDE},
 {"t":"escolha","g":"caso","p":"No caso do ensaio, que direito da Marta pesa mais?","p2":"A Marta aceitou ser filmada, mas não sabe que o vídeo vai ser publicado. Que direito dela está em causa?",
  "o":["O direito à imagem e à reserva da vida privada.","O direito de autor do grupo sobre o vídeo.","A liberdade de criação artística da turma."],"c":0,
  "f":"A Constituição reconhece a todos o direito à imagem e à reserva da intimidade da vida privada (artigo 26.º, n.º 1). É isso que está em causa quando um vídeo da Marta sai do grupo.",
  "fe":["","O vídeo pode ser trabalho do grupo, mas isso não responde ao que a Marta perde: o controlo da sua imagem.","A liberdade de criação é da turma, não da Marta, e não dá licença para expor quem aparece."]},
 {"t":"vf","g":"lei","p":"O Código Civil diz que o retrato de uma pessoa não pode ser exposto nem reproduzido sem o consentimento dela.","p2":"Segundo o Código Civil, para expor ou reproduzir o retrato de alguém é preciso o consentimento dessa pessoa.","v":True,
  "f":"É o artigo 79.º, n.º 1, do Código Civil: o retrato não pode ser exposto, reproduzido ou lançado no comércio sem o consentimento da pessoa. O n.º 2 do mesmo artigo abre exceções.",
  "fe":"A regra geral é o consentimento. As exceções existem, mas são exceções: estão no n.º 2 do mesmo artigo."},
 {"t":"sublinhar","g":"honra","p":"Código Civil, artigo 79.º, n.º 3: toca nas três palavras que dizem o que o retrato nunca pode prejudicar.","p2":"No n.º 3 do artigo 79.º, que três coisas da pessoa retratada ficam sempre protegidas? Toca nelas.","frase":ART79_3,"certas":[19,20,23],
  "f":"Mesmo quando não é preciso pedir, o retrato não pode prejudicar a **honra**, a **reputação** ou o simples **decoro** da pessoa. Uma queda filmada e publicada pode tocar no decoro."},
 {"t":"emparelhar","g":"pedido","p":"Antes de dizer que sim, a Marta faz quatro perguntas. Liga cada uma à parte do pedido de consentimento que lhe responde.","p2":"A que parte de um pedido de consentimento responde cada pergunta da Marta?",
  "pares":[["«Para que é o vídeo?»","Para quê"],["«Vai aparecer onde, e quem o vê?»","Que uso"],["«Até quando fica guardado?»","Onde fica e até quando"],["«E se eu mudar de ideias?»","Como se retira"]],
  "f":"Um pedido de consentimento claro diz para que serve a imagem, como vai ser usada, onde fica e até quando, e como se retira o sim. Sem isto, a pessoa não sabe a que está a dizer que sim.",
  "fe":"Lê cada pergunta como se fosses a Marta: o que quer ela saber antes de decidir?"},
 {"t":"escolha","g":"didatico","p":"A escola diz que o vídeo da queda tem fins didáticos. Isso chega para o publicar sem perguntar à Marta?","p2":"«É para fins didáticos», diz a escola. Pode então publicar o vídeo da queda sem a Marta concordar?",
  "o":["Não, se a imagem expuser a Marta ao ridículo.","Sim, porque os fins didáticos valem sempre.","Sim, porque a conta pertence à escola."],"c":0,
  "f":"O artigo 79.º, n.º 2, do Código Civil dispensa o consentimento em certos casos, entre eles as finalidades didáticas. Mas o n.º 3 põe um limite: nunca com prejuízo para a honra, a reputação ou o simples decoro da pessoa.",
  "fe":["","As exceções do n.º 2 têm um limite no n.º 3: se a imagem prejudica o decoro da pessoa, não pode ser exposta.","Ser a escola a publicar não muda o que a imagem faz à Marta. O limite do n.º 3 vale para todos."]},
 {"t":"vf","g":"idade","p":"Em Portugal, com 13 anos já podes aceitar sozinho que uma rede social trate os teus dados pessoais.","p2":"A lei portuguesa fixa nos 13 anos a idade a partir da qual podes dar sozinho consentimento a um serviço digital.","v":True,
  "f":"A Lei n.º 58/2019 (artigo 16.º) fixa os 13 anos para o consentimento nos serviços digitais; abaixo disso, consentem os representantes legais. É uma regra sobre os teus dados, não sobre publicar a imagem de outra pessoa.",
  "fe":"A idade está no artigo 16.º da Lei n.º 58/2019: 13 anos. Mas aceitar as regras de uma rede social não te autoriza a publicar outras pessoas."},
 {"t":"ordenar","g":"passos","p":"Põe por ordem os passos antes de publicar uma imagem onde aparecem pessoas.","p2":"Que ordem seguir antes de publicar uma imagem com pessoas?",
  "passos":["Ver quem aparece e se é reconhecível.","Perguntar a cada pessoa se aceita aquele uso.","Mostrar a versão final a quem aparece.","Guardar a resposta e publicar só o que foi aceite."],
  "f":"Primeiro saber quem aparece; depois pedir para aquele uso; depois mostrar o que vai sair; no fim, guardar a resposta. Assim, quem aparece decide antes, e não depois de ver o vídeo publicado."},
 {"t":"ler","rot":"Ver","titulo":"Uma fotografia de 1910","html":FOTO},
 {"t":"escolha","g":"legenda","p":"Na fotografia de 1910, o que acrescenta a legenda ao que a imagem já mostra?","p2":"Sem a legenda, vês uma rapariga numa fábrica. Que informação junta a legenda?",
  "o":["O nome e a idade da rapariga.","A cor do vestido que ela usava.","A opinião dela sobre o trabalho."],"c":0,
  "f":"A legenda identifica a rapariga: Addie Card, 12 anos, fiandeira numa fábrica de algodão de North Pownal, no Vermont. É a legenda que faz de uma imagem anónima o retrato de uma pessoa concreta.",
  "fe":["","A fotografia é a preto e branco, e a legenda não fala da roupa: fala de quem ela é.","A legenda regista o que o fotógrafo soube dela, como a idade, e não a opinião dela sobre o trabalho."]},
 {"t":"ler","rot":"Na aula","titulo":"Decidir e voltar a decidir","html":NA_AULA},
 {"t":"ler","rot":"Ver","titulo":"Uma cara que se imita","html":VIDEO},
 {"t":"escolha","g":"rua","p":"Caso inventado: num exercício de fotografia de rua, uma pessoa numa paragem fica em primeiro plano, bem reconhecível. O que deves fazer antes de publicar?","p2":"Fotografaste a rua e uma pessoa ficou no centro da imagem, reconhecível. Que fazes antes de a publicar?",
  "o":["Perguntar-lhe ou escolher uma imagem em que não seja o centro.","Publicar, porque quem está na rua aceita ser fotografado.","Publicar, mas sem dizer onde a fotografia foi tirada."],"c":0,
  "f":"O Código Civil dispensa o consentimento quando a imagem vem enquadrada na de lugares públicos (artigo 79.º, n.º 2). Uma pessoa em primeiro plano já não é parte da rua: é o assunto da fotografia. Perguntar resolve; tirá-la do centro também.",
  "fe":["","Estar na rua não é aceitar tudo. A lei dispensa o consentimento quando a pessoa aparece enquadrada no lugar, não quando é o assunto da imagem.","Esconder o sítio não esconde a pessoa: continua reconhecível."]},
 {"t":"vf","g":"retirar","p":"Se a Marta pedir para tirar o vídeo depois de publicado, o grupo já não tem de fazer nada.","p2":"Depois de o vídeo estar publicado, o pedido da Marta para o retirar já não obriga o grupo a nada.","v":False,
  "f":"Aceitar limitar um direito de personalidade, como o direito à imagem, é sempre revogável (Código Civil, artigo 81.º, n.º 2). Se a Marta já não aceita, o grupo tem de a ouvir e tirar o vídeo.",
  "fe":"Publicar não apaga o direito à imagem. A Marta pode retirar o sim que deu, mesmo depois."},
 {"t":"completar","g":"consentimento","p":"Completa a frase sobre o consentimento.","p2":"Completa: três coisas que tens de saber sobre o consentimento.",
  "frase":"O consentimento vale para [1], pode ser [2] e pede-se [3].",
  "lacunas":[{"o":["um uso","qualquer uso","um ano"],"c":0},{"o":["retirado","esquecido","vendido"],"c":0},{"o":["antes de publicar","depois de publicar","se alguém se queixar"],"c":0}],
  "f":"O consentimento vale para **um uso**, pode ser **retirado** e pede-se **antes de publicar**. Pedir depois é pôr a pessoa perante um facto consumado.",
  "fe":"Volta ao caso da Marta: aceitou um uso, pode mudar de ideias e devia ter sido ouvida antes."},
 {"t":"escolha","g":"captura","p":"Caso inventado: alguém tira uma captura de ecrã de uma conversa privada com a Marta e mostra-a ao grupo da turma. Que direito protege a conversa?","p2":"Uma conversa privada aparece em captura de ecrã no grupo da turma. Que direito está em causa?",
  "o":["O sigilo das comunicações privadas.","A liberdade de expressão de quem a tirou.","O direito de reunião do grupo da turma."],"c":0,
  "f":"A Constituição diz que o sigilo da correspondência e dos outros meios de comunicação privada é inviolável (artigo 34.º, n.º 1). A Convenção sobre os Direitos da Criança também protege a correspondência (artigo 16.º).",
  "fe":["","A liberdade de expressão protege o que tu pensas e dizes. Não te dá a conversa de outra pessoa para mostrar.","Ninguém impediu o grupo de se reunir. O que está em causa é uma conversa que era só de duas pessoas."]},
 {"t":"emparelhar","g":"projeto","p":"Frases do pedido de consentimento para as entrevistas da Pergunta Humana. Liga cada frase à parte do pedido que cumpre.","p2":"Que parte do pedido de consentimento cumpre cada uma destas frases?",
  "pares":[["«A entrevista serve para o nosso teatro-documento.»","Para quê"],["«Só usamos a tua voz, sem mostrar a cara.»","Que uso"],["«A gravação fica no computador da escola até julho.»","Onde fica e até quando"],["«Podes desistir até ao dia do ensaio.»","Como se retira"]],
  "f":"Um pedido completo responde às quatro perguntas da Marta: para quê, que uso, onde fica e até quando, e como se retira. É este o pedido que o teu grupo leva para as entrevistas.",
  "fe":"Pergunta a cada frase: diz para que serve, como se usa, onde fica ou como se desiste?"},
 {"t":"ler","rot":"Para levar","escuro":True,"html":LEVAR},
]
dados = {
 "id":"cidadania-m1-s02","chave":"epi-cid-m1-s02","versao":"2026-10-31-1",
 "marca":"CD","titulo":"Sessão 02: A imagem dos outros","h1":"Cidadania, módulo 1, sessão 02: A imagem dos outros",
 "modulo":{"n":1,"nome":"Ser-se humano","url":"https://pedrohfernandes-klk.github.io/lente/cidadania/piloto/m1/"},
 "saida":"cidadania/piloto/m1-s02/index.html","piloto":True,
 "fontes":"Código Civil, artigos 79.º (direito à imagem) e 81.º, n.º 2; Constituição da República Portuguesa, artigos 26.º, n.º 1, e 34.º, n.º 1; Lei n.º 58/2019, artigo 16.º (textos lidos no sítio da Procuradoria-Geral Distrital de Lisboa a 31/10/2026). Convenção sobre os Direitos da Criança (1989), artigo 16.º, no texto do Ministério Público. Fotografia: Lewis Hine, Addie Card, 12 years. Spinner in North Pormal [i.e., Pownal] Cotton Mill. Vt., 1910 (Library of Congress, National Child Labor Committee Collection, domínio público). Vídeo: TED, «When AI Can Fake Reality, Who Can You Trust?», conferência de Sam Gregory (excerto). Os casos são inventados.",
 "cartoes":cartoes,
}
p = pathlib.Path(__file__).with_suffix('.json')
p.write_text(json.dumps(dados, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print(p, len(cartoes), 'cartões', sum(1 for c in cartoes if c['t'] != 'ler'), 'de fazer')
