# Fonte da sessão 09 do M1 de Cidadania (piloto de 31/10/2026, no molde da sessão 01). Corre-se para escrever o .json ao
# lado; o .json é que o gerador (tools/licoes_lente.py) lê. Escreve-se em Python para não ter de escapar aspas à mão.
# Leis lidas a 31/10/2026: Constituição (PGDL, nid=4) e Convenção sobre os Direitos da Criança (PDF do Ministério Público,
# dcjri.ministeriopublico.pt; o antigo gddc responde 301 para lá). A Declaração
# Universal e a Resolução do Conselho de Ministros n.º 127/2025 não entram nos cartões (endereços por confirmar).
# Imagem: o plano previa Sherman, Pipers (Commons, domínio público); o descarregamento deu 429 três vezes e a NYPL tem um
# bloqueio a robôs, que não se contornou. Fica a fotografia da Library of Congress (LC-D6-87, registo lido a 31/10/2026).
# 31/10/2026 (verificação final, decisão 39): a fotografia da LoC saiu. O registo (97501656, LC-USZ62-67910) não diz quem a
# tirou e só diz «No known restrictions on publication», que não é nenhum dos estatutos da casa; a atribuição a Lewis Hine
# («Italian Family Seeking Lost Luggage», Met 285814) não se confirmou: o Met não mostra a imagem, o George Eastman Museum e o
# MFAH têm bloqueio Cloudflare e a Biblioteca Pública de Nova Iorque um bloqueio Incapsula, que não se contornaram. Entrou outra
# fotografia de Hine em Ellis Island, com domínio público declarado no Wikimedia Commons (PD-1923, PD-Art): «Immigrant Family
# in the Baggage Room of Ellis Island», 1905, prova de 1939, Museum of Fine Arts, Houston (ficha do museu no Google Arts &
# Culture, hwEWiyJnUAWQ5g, lida a 31/10/2026). O título do museu não diz a origem da família: o cartão fala de imigrantes e
# não de um país, e descreve só o que se vê (a mulher com o bebé ao colo, o rapaz com o saco às riscas, a menina de touca, as
# malas e a caixa com palavras escritas à mão).
# A imagem veio do Google Arts & Culture (949 × 1200, a reprodução que o Commons guarda), porque upload.wikimedia.org respondeu
# 429 quatro vezes (Retry-After de 600 s, respeitado, um pedido de cada vez). Tratamento igual ao da sessão 02 (Hine, Addie Card):
# tons de cinzento, níveis de 0,5 % a 99,5 %, margens aparadas (4, 2, 2 e 3 px), 640 × 811, webp.
import json, pathlib
ABRE = (
 '<p class="pergunta-c">Uma escola com muitas línguas e crenças precisa de regras iguais ou de regras que ouçam todos?</p>'
 '<p>Caso inventado. Nos intervalos ouvem-se português, crioulo cabo-verdiano, romeno e nepalês. A direção propõe uma regra: nos intervalos, só português, «para todos se entenderem».</p>'
 '<p class="aula-linha"><b>Hoje</b>, 180 minutos com uma pausa: decidir, desmontar um estereótipo e ensaiar o teatro-documento com outro grupo.</p>')
DECIDE = (
 '<p>A regra do português nos intervalos deve avançar?</p>'
 '<p class="pergunta-c">Decide em silêncio, de braço no ar: sim, não ou depende.</p>'
 '<details class="lado"><summary>A razão da direção</summary><div><p>«Uma língua comum junta a turma e ajuda quem está a aprender português.»</p></div></details>'
 '<details class="lado"><summary>A razão de uma aluna</summary><div><p>«No intervalo falo com a minha irmã na nossa língua. Proibir isso é dizer que a minha língua não cabe aqui.»</p></div></details>'
 '<details class="lado"><summary>Uma objeção</summary><div><p>E se alguém usar outra língua para gozar com um colega que não percebe? Isso pede uma regra para todos ou uma conversa?</p></div></details>'
 '<p>Não há resposta certa neste cartão. Guarda a tua posição: vais voltar a ela.</p>')
CONCEITO = (
 '<p>Dois textos dizem o que uma regra da escola não pode apagar:</p>'
 '<ul><li><b>Constituição, artigo 13.º, n.º 2</b>: ninguém pode ser privilegiado, beneficiado, prejudicado ou privado de qualquer direito em razão, entre outras coisas, da língua, do território de origem ou da religião.</li>'
 '<li><b>Convenção sobre os Direitos da Criança, artigo 30.º</b>: a criança de uma minoria não pode ser privada do direito de ter a sua vida cultural, praticar a sua religião ou utilizar a sua própria língua, com os membros do seu grupo.</li></ul>'
 '<p>Uma regra pode ser igual para todos e, mesmo assim, pesar mais sobre alguns.</p>')
CDC30 = 'ter a sua própria vida cultural, professar e praticar a sua própria religião ou utilizar a sua própria língua.'
FOTO = (
 '<figure class="fig inteiro"><span class="moldura"><img src="../../../img/cidadania/hine-familia-bagagens-1905.webp" '
 'alt="Fotografia a preto e branco. Uma mulher de lenço na cabeça tem um bebé ao colo; ao lado, um rapaz de boné leva ao ombro um grande saco às riscas; à frente, uma menina pequena de touca. Atrás, malas e baús empilhados; no chão, à esquerda, uma caixa com palavras escritas à mão." loading="lazy"></span>'
 '<figcaption>Lewis Hine, <i>Immigrant Family in the Baggage Room of Ellis Island</i>, 1905 (prova de 1939). Museum of Fine Arts, Houston, via Google Arts &amp; Culture. Domínio público.</figcaption></figure>'
 '<p>Uma família na sala das bagagens da ilha de Ellis, por onde entravam os imigrantes nos Estados Unidos. Fotografou-a em 1905 o norte-americano Lewis Hine.</p>'
 '<p class="pergunta-c">Se esta fosse a única imagem que conhecesses dos imigrantes que chegavam aos Estados Unidos, que ideia farias deles? O que é que a fotografia não mostra?</p>'
 '<p>Responde no caderno, numa linha para cada pergunta.</p>')
VIDEO = (
 '<p>Um vídeo curto do TED-Ed, numa lição de Sheila Marie Orfano e Densho: um estereótipo que parece um elogio também pode fazer mal. É em inglês: liga as legendas no leitor.</p>'
 '<p class="pergunta-c">Escreve o estereótipo de que o vídeo fala, o dano que aponta e um exemplo da tua escola.</p>'
 '<div class="yt" data-yt="aFXmyNUaXFo" data-titulo="Can stereotypes ever be good?, TED-Ed">'
 '<button type="button" class="yt-abrir" data-yt-abrir>Ver: «Can stereotypes ever be good?» (5 min 52 s)</button>'
 '<p class="yt-cred">TED-Ed, lição de Sheila Marie Orfano e Densho. O vídeo só se liga ao YouTube quando tocas no botão.</p></div>'
 '<p>Três linhas no caderno. No exemplo, não nomeies colegas.</p>')
NA_AULA = (
 '<p><b>O que se faz.</b> Primeiro, o aquecimento «O outro lado»: 10 minutos de improvisação com posições sorteadas. Depois, cada grupo mostra o teatro-documento em ensaio a outro grupo. Quem observa toma notas em três colunas (o que se ouviu, de quem é a voz, de que fonte vem) e procura a voz que falta.</p>'
 '<p><b>Quanto tempo.</b> 60 a 75 minutos, com a pausa.</p>'
 '<p><b>O que fica escrito.</b> As notas dadas ao outro grupo e duas mudanças que o vosso grupo decide fazer, uma delas para incluir uma voz que ainda não estava.</p>')
LEVAR = (
 '<p class="levar">Ouvir outra voz não é concordar com ela: é saber sobre o que se decide.</p>'
 '<p>Nesta sessão viste como uma regra igual pode calar alguém e como um estereótipo diz o mesmo de todos. No ensaio, procuraste a voz que faltava. Volta à fotografia da ilha de Ellis: o que ficou de fora?</p>'
 '<p><b>As frases da sessão</b></p>'
 '<ul><li>Ninguém pode ser prejudicado pela língua ou pela religião (artigo 13.º).</li>'
 '<li>Um estereótipo diz o mesmo de todos; uma pessoa é sempre mais.</li>'
 '<li>Uma regra para todos tem de ser explicada a quem ela cala.</li>'
 '<li>Na cena, a voz de quem discorda também tem fonte.</li></ul>')

cartoes = [
 {"t":"ler","rot":"Abre","titulo":"Muitas vozes, uma escola","html":ABRE},
 {"t":"ler","rot":"Decide","titulo":"Só português no intervalo?","html":DECIDE},
 {"t":"escolha","g":"direito","p":"Segundo a Constituição, que direito pode ser tocado pela regra «só português nos intervalos»?","p2":"A regra do português nos intervalos pode chocar com que direito da Constituição?",
  "o":["Não ser prejudicado por causa da língua.","Escolher a escola que se quer frequentar.","Ter um intervalo com a duração certa."],"c":0,
  "f":"O artigo 13.º, n.º 2, diz que ninguém pode ser prejudicado ou privado de qualquer direito em razão da língua. A regra não proíbe ninguém de estar na escola, mas pode prejudicar quem fala outra língua com os seus.",
  "fe":["","A regra não muda a escola de ninguém. O que toca é a língua em que se pode falar.","A duração do intervalo não está em causa. A regra mexe na língua, não no tempo."]},
 {"t":"ler","rot":"Conceito","titulo":"O que uma regra não apaga","html":CONCEITO},
 {"t":"sublinhar","g":"cdc30","p":"Artigo 30.º da Convenção (a parte final): a criança de uma minoria não pode ser privada do direito de… Toca nas quatro palavras que dizem o que a criança tem o direito de fazer.","p2":"No final do artigo 30.º da Convenção, que quatro verbos dizem o que a criança pode fazer? Toca neles.","frase":CDC30,"certas":[0,6,8,14],
  "f":"A Convenção protege quatro ações: **ter** a sua vida cultural, **professar** e **praticar** a sua religião e **utilizar** a sua própria língua. Não basta ter uma língua: é preciso poder usá-la."},
 {"t":"vf","g":"religiao","p":"Uma autoridade não pode perguntar-te pela tua religião, salvo para estatísticas que não te identifiquem.","p2":"A Constituição só deixa uma autoridade perguntar a religião de alguém para recolher estatísticas sem identificação.","v":True,
  "f":"O artigo 41.º, n.º 3, diz que ninguém pode ser perguntado por qualquer autoridade sobre as suas convicções ou prática religiosa, salvo para dados estatísticos não individualmente identificáveis, nem ser prejudicado por se recusar a responder.",
  "fe":"A tua religião não tem de ser dita a nenhuma autoridade: a única exceção é a estatística sem nomes."},
 {"t":"emparelhar","g":"tipos","p":"Liga cada frase ao que ela é.","p2":"Que tipo de frase é cada uma destas?",
  "pares":[["Nos intervalos ouvem-se quatro línguas.","Facto que se pode observar"],["Quem vem de fora não quer aprender português.","Estereótipo sobre um grupo"],["Acho que o intervalo devia ser mais longo.","Opinião de quem fala"],["No inquérito da turma, 12 em 25 falam outra língua em casa.","Dado com a fonte indicada"]],
  "f":"Um facto pode ser observado por qualquer um. Um dado diz de onde vem. Uma opinião é de quem fala. Um estereótipo diz o mesmo de todas as pessoas de um grupo, sem prova.",
  "fe":"Procura as marcas: «acho» é opinião; «quem vem de fora» fala de um grupo inteiro; um número com a origem é um dado."},
 {"t":"ler","rot":"Ver","titulo":"Um elogio que faz mal?","html":VIDEO},
 {"t":"escolha","g":"positivo","p":"Dizer «os alunos daquele país são todos ótimos a matemática» parece um elogio. Porque é que também faz mal?","p2":"Um estereótipo «positivo» também pode magoar. Porquê?",
  "o":["Trata cada pessoa pelo grupo, não por ela.","Os elogios nunca devem ser feitos na escola.","Só faz mal quando é dito por um adulto."],"c":0,
  "f":"Mesmo quando parece bom, o estereótipo apaga a pessoa: quem não é «ótimo a matemática» fica de fora, e quem é deixa de ter mérito próprio. É o dano de que fala o vídeo.",
  "fe":["","Elogiar o trabalho de alguém é bom. O problema é atribuir uma qualidade a todos os de um grupo.","Quem diz a frase não muda o problema: a frase trata as pessoas pelo grupo."]},
 {"t":"ler","rot":"Ver","titulo":"Uma fotografia à chegada","html":FOTO},
 {"t":"escolha","g":"foto","p":"Na fotografia da ilha de Ellis, uma mulher e três crianças na sala das bagagens. O que é que esta imagem não pode mostrar?","p2":"A fotografia da ilha de Ellis mostra uma família à chegada. Que coisa fica, de certeza, fora dela?",
  "o":["Como eram as outras famílias à chegada.","O saco às riscas que o rapaz leva ao ombro.","O bebé que a mulher de lenço tem ao colo."],"c":0,
  "f":"Uma fotografia mostra quatro pessoas num momento. Tomá-la pelo retrato de todos os imigrantes é o primeiro passo de um estereótipo.",
  "fe":["","O saco vê-se bem, ao ombro do rapaz: é das coisas que a fotografia mostra com certeza.","O bebé está à vista, ao colo da mulher. É o que a fotografia mostra."]},
 {"t":"ordenar","g":"responder","p":"Alguém diz uma frase que generaliza sobre um grupo. Põe por ordem os passos para responder.","p2":"Por que ordem respondes a um comentário que generaliza?",
  "passos":["Perguntar de onde vem essa ideia.","Ouvir a resposta até ao fim.","Dar um facto que se possa verificar.","Propor outra pergunta para a conversa."],
  "f":"Perguntar primeiro abre a conversa em vez de a fechar. Depois ouve-se a resposta até ao fim, e só então se traz um facto. No fim, uma pergunta nova evita voltar ao mesmo."},
 {"t":"vf","g":"neutra","p":"Uma regra que vale para todos é sempre neutra para todos.","p2":"Se uma regra se aplica a toda a gente, nunca pesa mais sobre uns do que sobre outros.","v":False,
  "f":"A regra do português vale para todos, mas só pesa a quem fala outra língua com os seus. Por isso a Constituição proíbe prejudicar alguém em razão da língua (artigo 13.º, n.º 2), mesmo com regras iguais.",
  "fe":"Para saber se uma regra é neutra, pergunta quem perde com ela. Se perde sempre o mesmo grupo, não é neutra."},
 {"t":"ler","rot":"Na aula","titulo":"O ensaio cruzado","html":NA_AULA},
 {"t":"escolha","g":"festa","p":"Caso inventado: a festa de fim de período calha num dia de jejum de alguns colegas. Que decisão ouve todos?","p2":"Alguns colegas jejuam no dia marcado para a festa da turma. Que solução ouve toda a gente?",
  "o":["Perguntar a quem jejua e ajustar a hora.","Manter tudo: a maioria não está de jejum.","Cancelar a festa para a turma inteira."],"c":0,
  "f":"Perguntar a quem é afetado e ajustar a hora ou a comida deixa a festa para todos. Ninguém tem de explicar a sua religião: basta dizer aquilo de que precisa.",
  "fe":["","A maioria não decide sozinha sobre quem fica de fora. Uma pequena mudança pode bastar.","Cancelar tira a festa a todos, e ninguém o pediu. Há soluções menos pesadas."]},
 {"t":"emparelhar","g":"colunas","p":"Notas de um ensaio: liga cada nota à coluna onde fica.","p2":"Em que coluna das notas do ensaio fica cada uma?",
  "pares":[["«A escola não ouve os pais», diz a personagem da mãe.","O que se ouviu"],["Quem fala é a mãe, não a direção.","De quem é a voz"],["Vem da entrevista à associação de pais.","De que fonte vem"]],
  "f":"Separar o que se ouviu, de quem é a voz e de onde vem ajuda a encontrar a voz que falta: neste exemplo, a da direção.",
  "fe":"Pergunta a cada nota: é uma fala, uma pessoa ou uma origem?"},
 {"t":"completar","g":"regra","p":"Completa a frase sobre uma regra comum justa.","p2":"Quando é que uma regra comum é justa?",
  "frase":"Uma regra comum é justa quando é [1] a todos e não [2] ninguém.",
  "lacunas":[{"o":["explicada","imposta","escondida"],"c":0},{"o":["cala","ouve","avisa"],"c":0}],
  "f":"Uma regra comum justa explica-se a quem a cumpre e não cala ninguém. Se calar sempre os mesmos, tem de ser revista.",
  "fe":"Volta ao caso do intervalo: a quem é que a regra tira a palavra?"},
 {"t":"vf","g":"discorda","p":"No teatro-documento, a fala de alguém que discorda do grupo pode entrar, desde que se diga de onde vem.","p2":"Uma voz contrária à do grupo pode entrar no teatro-documento, se tiver a sua fonte.","v":True,
  "f":"O teatro-documento é feito do que se investigou. Uma voz que discorda, com fonte, mostra que o grupo ouviu mais do que um lado.",
  "fe":"Pôr em cena quem discorda não é dar-lhe razão: é mostrar o que se ouviu, com a fonte."},
 {"t":"ler","rot":"Para levar","escuro":True,"html":LEVAR},
]
dados = {
 "id":"cidadania-m1-s09","chave":"epi-cid-m1-s09","versao":"2026-10-31-2",
 "marca":"CD","titulo":"Sessão 09: Muitas vozes, uma escola","h1":"Cidadania, módulo 1, sessão 09: Muitas vozes, uma escola",
 "modulo":{"n":1,"nome":"Ser-se humano","url":"https://pedrohfernandes-klk.github.io/lente/cidadania/piloto/m1/"},
 "saida":"cidadania/piloto/m1-s09/index.html","piloto":True,
 "seguinte":"../m1-s10/","seguinteRotulo":"Sessão 10: O que conseguimos defender?",
 "fontes":"Constituição da República Portuguesa, artigos 13.º, n.º 2, e 41.º, n.º 3 (texto da Procuradoria-Geral Distrital de Lisboa, https://www.pgdlisboa.pt/leis/lei_mostra_articulado.php?nid=4&tabela=leis, lido a 31/10/2026). Convenção sobre os Direitos da Criança (1989), artigos 2.º e 30.º (texto do Ministério Público, https://dcjri.ministeriopublico.pt/sites/default/files/documentos/instrumentos/convencao_sobre_direitos_da_crianca.pdf, lido a 31/10/2026). Pergunta Humana: requisitos do teatro-documento (cidadania/projeto/). Fotografia: Lewis Hine, _Immigrant Family in the Baggage Room of Ellis Island_, 1905, prova de 1939 (Museum of Fine Arts, Houston; domínio público segundo o Wikimedia Commons; página e reprodução no Google Arts & Culture, https://artsandculture.google.com/asset/hwEWiyJnUAWQ5g, consultadas a 31/10/2026). Vídeo: TED-Ed, «Can stereotypes ever be good?», lição de Sheila Marie Orfano e Densho. Os casos são inventados.",
 "cartoes":cartoes,
}
p = pathlib.Path(__file__).with_suffix('.json')
p.write_text(json.dumps(dados, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print(p, len(cartoes), 'cartões', sum(1 for c in cartoes if c['t'] != 'ler'), 'de fazer')
