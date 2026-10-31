# Fonte da sessão 07 do M1 de Cidadania (piloto de 31/10/2026, no molde da sessão 01). Corre-se para escrever o .json
# ao lado; o .json é que o gerador (tools/licoes_lente.py) lê. Escreve-se em Python para não ter de escapar aspas à mão.
# Lido a 31/10/2026: Constituição (artigos 32.º e 207.º) na página da Procuradoria-Geral Distrital de Lisboa; Convenção
# sobre os Direitos da Criança (artigo 12.º) no PDF do Ministério Público (dcjri; o antigo gddc responde 301); Declaração Universal (artigos 10.º e 11.º) na página do
# UNRIC.
import json, pathlib
ABRE = (
 '<p class="pergunta-c">Quando quase todos já decidiram, ainda vale a pena ouvir a defesa?</p>'
 '<p>Caso inventado. Um vídeo de um ensaio, montado para gozar com uma colega, circula no grupo do curso. Uma captura de ecrã mostra o nome do Tomás ao lado do vídeo. No primeiro voto, nove dizem que foi ele e dois pedem para ver as provas.</p>'
 '<p class="aula-linha"><b>Hoje</b>, 180 minutos com uma pausa: decidir, separar prova de inferência e julgar um caso no Tribunal de turma.</p>')
DECIDE = (
 '<p>O Tomás deve sair já do grupo de trabalho, antes de se decidir?</p>'
 '<p class="pergunta-c">Decide em silêncio, de braço no ar: sim, não ou depende.</p>'
 '<details class="lado"><summary>A razão da maioria</summary><div><p>«A captura é clara. Esperar é deixar a colega sozinha.»</p></div></details>'
 '<details class="lado"><summary>A razão dos dois</summary><div><p>«Uma captura mostra um nome, não mostra quem carregou no botão. Ainda não ouvimos o Tomás.»</p></div></details>'
 '<details class="lado"><summary>Uma objeção</summary><div><p>Há uma medida que proteja a colega sem castigar já o Tomás?</p></div></details>'
 '<p>Não há resposta certa neste cartão. Guarda a tua posição: vais voltar a ela.</p>')
INFERENCIA = 'A captura mostra o nome do Tomás ao lado do vídeo, por isso foi ele que o montou e publicou.'
# 31/10/2026 (decisão 18): a imagem e o vídeo da sessão. A fotografia dos óstracos de Temístocles (Commons, CC BY-SA
# 2.0, página verificada a 31/10) não se conseguiu descarregar: upload.wikimedia.org respondeu 429 (Retry-After 600 s)
# e o Flickr da autora respondeu «CIDR range blocked»; não se insistiu. Entra uma litografia de Daumier do Met (Open
# Access, CC0; metadados lidos na API do museu a 31/10), com a legenda em tradução nossa (francês). Lição do TED-Ed:
# oEmbed e página da lição verificados a 31/10. A litografia foi recortada ao filete (sem o cabeçalho «LES GENS DE
# JUSTICE», o número e a legenda, que o cartão traduz), a partir da imagem do Met (revisão do diretor de arte, 31/10).
CARTAZ = (
 '<figure class="fig inteiro"><span class="moldura"><img src="../../../img/cidadania/daumier-gens-de-justice-21.webp" '
 'alt="Litografia a preto e branco. Num tribunal, um advogado de toga e barrete inclina-se para trás e fala ao ouvido de um homem despenteado, apoiado na barra dos acusados. À esquerda, outra figura de toga está de olhos fechados; ao fundo, o público." loading="lazy"></span>'
 '<figcaption>Honoré Daumier, «Voilà le ministère public qui vous dit des choses très désagréables», prancha 21 de <i>Les Gens de Justice</i>, 1846, litografia. Metropolitan Museum of Art, Nova Iorque. CC0.</figcaption></figure>'
 '<p>Na legenda, o advogado diz ao acusado (tradução nossa): «Aí está o Ministério Público a dizer-lhe coisas muito desagradáveis… trate então de chorar ao menos de um olho… fica sempre bem!»</p>'
 '<p class="pergunta-c">Um julgamento decide pelo que comove ou pelo que se prova?</p>'
 '<p>Responde no caderno, numa linha. Voltas a esta pergunta no fim da sessão.</p>')
VIDEO = (
 '<p>Um vídeo curto do TED-Ed, numa lição de Melissa Schwartzberg. Em Atenas, muitos dos que decidiam não eram escolhidos como hoje. É em inglês: liga as legendas no leitor.</p>'
 '<p class="pergunta-c">Enquanto vês: como se escolhiam muitos dos que decidiam? Anota uma vantagem e um perigo desse modo de escolher.</p>'
 '<div class="yt" data-yt="0fivQUlC7-8" data-titulo="What did democracy really mean in Athens?, TED-Ed">'
 '<button type="button" class="yt-abrir" data-yt-abrir>Ver: «What did democracy really mean in Athens?» (4 min 51 s)</button>'
 '<p class="yt-cred">TED-Ed, lição de Melissa Schwartzberg. O vídeo só se liga ao YouTube quando tocas no botão.</p></div>')
NA_AULA = (
 '<p><b>O que se faz.</b> O Tribunal de turma. Os papéis saem em cartas: acusação, defesa, três testemunhas, júri, relator e quem guarda o tempo. Cada intervenção tem dois minutos, com o relógio. O júri vota em boletim, com uma razão obrigatória, antes e depois de deliberar, e o relator conta quantos votos citam uma prova.</p>'
 '<p><b>Quanto tempo.</b> 60 a 75 minutos, com a pausa.</p>'
 '<p><b>O que fica escrito.</b> O acórdão da turma (a decisão, duas provas citadas, uma dúvida razoável e um voto vencido) e as notas de cada papel, com o nome de quem as escreveu.</p>')
LEVAR = (
 '<p class="levar">Uma decisão de muitos vale o que valem as provas que a sustentam.</p>'
 '<p>Nesta sessão separaste facto de inferência, ouviste a defesa e viste o voto mudar, ou não mudar, com as provas. Volta à litografia de Daumier: o vosso júri decidiu pelas lágrimas ou pelas provas? E volta à tua posição do início: o Tomás saía já?</p>'
 '<p><b>As frases da sessão</b></p>'
 '<ul><li>Votar conta posições; deliberar pesa razões.</li>'
 '<li>Todos se presumem inocentes até prova em contrário.</li>'
 '<li>Uma captura de ecrã mostra um nome, não mostra quem fez.</li>'
 '<li>Quem pode ser castigado tem direito a ser ouvido (artigo 32.º, n.º 10).</li></ul>')

cartoes = [
 {"t":"ler","rot":"Abre","titulo":"Nove contra dois","html":ABRE},
 {"t":"ler","rot":"Decide","titulo":"O Tomás sai já?","html":DECIDE},
 {"t":"sublinhar","g":"inferencia","p":"Toca nas duas palavras onde a frase deixa de descrever a captura e passa a tirar uma conclusão.","p2":"Onde começa a inferência nesta frase? Toca nas duas palavras.","frase":INFERENCIA,"certas":[11,12],
  "f":"Até ao **por isso**, a frase descreve o que se vê. Depois, tira uma conclusão que a captura não mostra: quem montou e quem publicou."},
 {"t":"escolha","g":"captura","p":"O que prova, com segurança, a captura de ecrã?","p2":"Com a captura na mão, o que se pode afirmar sem ir além dela?",
  "o":["Que o nome do Tomás aparece ao lado do vídeo.","Que foi o Tomás quem montou e publicou o vídeo.","Que o Tomás quis gozar com a colega no grupo."],"c":0,
  "f":"A captura prova o que mostra: um nome ao lado de um vídeo. Quem montou, quem publicou e com que intenção são perguntas que precisam de outras provas.",
  "fe":["","Isso já é uma inferência. Um nome pode aparecer por muitas razões: uma conta partilhada, um reencaminhamento, uma montagem.","Ninguém ouviu ainda o Tomás. Dar-lhe uma intenção é concluir antes de ouvir."]},
 {"t":"vf","g":"presuncao","p":"A Constituição diz que todo o arguido se presume inocente até à condenação definitiva.","p2":"Segundo a Constituição, um arguido é tratado como inocente até haver sentença de condenação definitiva.","v":True,
  "f":"O artigo 32.º, n.º 2, diz que «todo o arguido se presume inocente até ao trânsito em julgado da sentença de condenação». Trânsito em julgado quer dizer que a sentença já não admite recurso. A Declaração Universal também consagra a presunção de inocência (artigo 11.º, n.º 1).",
  "fe":"Está no artigo 32.º, n.º 2: a culpa tem de ser provada, não presumida."},
 {"t":"vf","g":"defesa","p":"Num processo disciplinar na escola, o aluno não tem direito a defender-se.","p2":"Quem enfrenta um processo disciplinar na escola não tem de ser ouvido.","v":False,
  "f":"O artigo 32.º, n.º 10, da Constituição assegura os direitos de audiência e defesa «em quaisquer processos sancionatórios». A Convenção sobre os Direitos da Criança garante à criança a oportunidade de ser ouvida nos processos administrativos que lhe respeitem (artigo 12.º, n.º 2).",
  "fe":"Quaisquer processos sancionatórios: a Constituição não deixa de fora os da escola."},
 {"t":"ler","rot":"Ver","titulo":"Chorar fica sempre bem?","html":CARTAZ},
 {"t":"emparelhar","g":"papeis","p":"No Tribunal de turma, liga cada papel à sua função.","p2":"Que função tem cada papel no Tribunal de turma?",
  "pares":[["Acusação","Apresenta as provas contra o Tomás"],["Defesa","Mostra o que as provas não provam"],["Testemunha","Conta só o que viu ou ouviu"],["Júri","Decide, com uma razão por escrito"],["Relator","Escreve o acórdão e conta as provas citadas"]],
  "f":"Cada papel tem um limite: a acusação não decide, a testemunha não opina, o júri não decide sem razão. O relator guarda o que se decidiu e porquê.",
  "fe":"Pergunta o que cada papel pode fazer e o que não pode."},
 {"t":"ordenar","g":"deliberar","p":"Põe por ordem os passos de uma deliberação justa.","p2":"Qual é a ordem de uma deliberação justa?",
  "passos":["Ouvir a acusação.","Ouvir a defesa.","Pesar as provas, uma a uma.","Votar, com uma razão escrita."],
  "f":"Primeiro ouvem-se os dois lados, depois pesam-se as provas e só no fim se vota, com uma razão. Votar antes de ouvir é decidir sem saber. A Declaração Universal pede um tribunal independente e imparcial, que ouça a causa de forma equitativa (artigo 10.º)."},
 {"t":"ler","rot":"Ver","titulo":"Quem decidia em Atenas?","html":VIDEO},
 {"t":"escolha","g":"nove","p":"Nove contra dois: que razão justifica continuar a discutir?","p2":"A maioria já votou nove contra dois. Porque vale a pena continuar a discutir?",
  "o":["Nove votos não são uma prova de quem o fez.","Os dois podem estar a proteger um amigo.","Discutir mais tempo é sempre melhor."],"c":0,
  "f":"Votar conta posições; deliberar pesa razões. Nove votos dizem o que nove pessoas pensam, não o que aconteceu. A maioria também precisa de fundamento.",
  "fe":["","Pode ser, mas isso também é uma suposição sem prova. O que se pede é ver as provas, não adivinhar intenções.","Discutir não é bom por si. Vale a pena porque nove votos contam opiniões e ainda faltam provas."]},
 {"t":"escolha","g":"daumier","p":"Na litografia de Daumier, o advogado aconselha o acusado a chorar. Que perigo mostra a cena para quem julga?","p2":"Chorar «fica sempre bem», diz o advogado de Daumier. Que perigo há nisso para um julgamento?",
  "o":["Decidir pela emoção e não pelas provas.","O acusado não ter um advogado ao lado.","O juiz não ouvir bem o que se diz."],"c":0,
  "f":"Daumier troça de uma defesa feita de efeitos: umas lágrimas para comover quem julga. Um júri decide pelo que se prova, não pelo que comove. Lembra-te disso no Tribunal de turma.",
  "fe":["","O acusado tem advogado: é ele quem dá o conselho. O perigo está no que o conselho pede.","A cena não mostra problemas de audição. Mostra alguém a preparar um efeito para quem julga."]},
 {"t":"ler","rot":"Na aula","titulo":"O Tribunal de turma","html":NA_AULA},
 {"t":"escolha","g":"contrario","p":"Caso ao contrário: depois da decisão, aparecem mensagens que mostram que outra pessoa usou o telemóvel do Tomás. Que deve a turma fazer?","p2":"Surge uma prova nova: outra pessoa usou o telemóvel do Tomás. O que se faz à decisão?",
  "o":["Rever a decisão e dizê-lo a quem foi afetado.","Manter a decisão, porque já foi votada.","Esquecer o assunto e não falar mais nisso."],"c":0,
  "f":"Uma decisão vale o que valem as provas. Se aparece uma prova nova que muda tudo, revê-se a decisão e repara-se o dano, a começar por dizer ao Tomás e à turma que a decisão mudou.",
  "fe":["","Ter sido votada não torna a decisão certa. Manter um erro conhecido é escolher o erro.","Calar deixa o Tomás com a culpa à vista de todos. Rever também é dizer, em voz alta, que a decisão mudou."]},
 {"t":"vf","g":"nova","p":"Se a maioria já votou, uma informação nova já não muda nada.","p2":"Depois do voto, uma prova nova não deve alterar a decisão.","v":False,
  "f":"O voto fecha a discussão daquele momento, não a verdade. Uma prova nova pode e deve reabrir a decisão.",
  "fe":"Pensa no caso ao contrário: se as mensagens aparecessem depois do voto, o Tomás ficava culpado na mesma?"},
 {"t":"completar","g":"acordao","p":"Completa o que leva o acórdão do Tribunal de turma.","p2":"Que palavras completam o acórdão da turma?",
  "frase":"O acórdão da turma tem a decisão, duas [1] citadas, uma [2] e um voto [3].",
  "lacunas":[{"o":["provas","opiniões","pessoas"],"c":0},{"o":["dúvida razoável","certeza absoluta","regra nova"],"c":0},{"o":["vencido","secreto","anulado"],"c":0}],
  "f":"Um acórdão mostra porque se decidiu: as provas citadas, a dúvida que ficou e o voto de quem perdeu, com a razão. Quem o lê percebe o caminho, não só o resultado.",
  "fe":"Pensa no que o acórdão tem de mostrar: com que provas se decidiu, que dúvida ficou e quem votou contra."},
 {"t":"escolha","g":"medida","p":"Enquanto se apura quem fez, que medida protege a colega sem castigar já o Tomás?","p2":"Que medida protege já a colega, antes de se saber quem fez o vídeo?",
  "o":["Pedir que o vídeo saia do grupo e seja apagado.","Tirar o Tomás do grupo de trabalho até ao fim do ano.","Publicar a captura para todos verem quem foi."],"c":0,
  "f":"Retirar o vídeo protege a colega já e não decide nada sobre quem o fez. Castigar antes de ouvir o Tomás seria decidir sem provas.",
  "fe":["","Isso já é um castigo, antes de se ouvir o Tomás e de se pesarem as provas.","Publicar a captura espalha o vídeo e acusa sem provas. Faz mal aos dois."]},
 {"t":"vf","g":"juri","p":"A Constituição portuguesa prevê júri no julgamento de alguns crimes graves.","p2":"Em Portugal, a Constituição admite que um júri intervenha no julgamento de crimes graves.","v":True,
  "f":"O artigo 207.º, n.º 1, diz que o júri, nos casos e com a composição que a lei fixar, intervém no julgamento dos crimes graves, designadamente quando a acusação ou a defesa o requeiram. Ficam de fora os crimes de terrorismo e os de criminalidade altamente organizada.",
  "fe":"Está no artigo 207.º: o júri existe para crimes graves, nos casos que a lei fixar."},
 {"t":"ler","rot":"Para levar","escuro":True,"html":LEVAR},
]
dados = {
 "id":"cidadania-m1-s07","chave":"epi-cid-m1-s07","versao":"2026-10-31-2",
 "marca":"CD","titulo":"Sessão 07: Nove contra dois","h1":"Cidadania, módulo 1, sessão 07: Nove contra dois",
 "modulo":{"n":1,"nome":"Ser-se humano","url":"https://pedrohfernandes-klk.github.io/lente/cidadania/piloto/m1/"},
 "saida":"cidadania/piloto/m1-s07/index.html","piloto":True,
 "seguinte":"../m1-s08/","seguinteRotulo":"Sessão 08: Quem decide o quê?",
 "fontes":"Constituição da República Portuguesa, artigos 32.º e 207.º; Convenção sobre os Direitos da Criança (1989), artigo 12.º; Declaração Universal dos Direitos Humanos (1948), artigos 10.º e 11.º, no texto do Ministério Público (https://dcjri.ministeriopublico.pt/sites/default/files/documentos/pdf/declaracao_universal_dos_direitos_do_homem_5.pdf). Imagem: Honoré Daumier, «Voilà le ministère public qui vous dit des choses très désagréables», prancha 21 de _Les Gens de Justice_, 1846, litografia (Metropolitan Museum of Art, CC0); legenda em tradução nossa. Vídeo: TED-Ed, «What did democracy really mean in Athens?», lição de Melissa Schwartzberg. Os casos são inventados.",
 "cartoes":cartoes,
}
p = pathlib.Path(__file__).with_suffix('.json')
p.write_text(json.dumps(dados, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print(p, len(cartoes), 'cartões', sum(1 for c in cartoes if c['t'] != 'ler'), 'de fazer')
