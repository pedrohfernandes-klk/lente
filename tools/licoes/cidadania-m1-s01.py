# Fonte da sessão 01 do M1 de Cidadania (piloto de 30/10/2026). Corre-se para escrever o .json ao lado;
# o .json é que o gerador (tools/licoes_lente.py) lê. Escreve-se em Python para não ter de escapar aspas à mão.
import json, pathlib
ABRE = (
 '<p class="pergunta-c">Que direitos estão em causa num dia normal de escola?</p>'
 '<p>Caso inventado. Às 8h20, uma aluna é fotografada a dormir no autocarro. A fotografia chega ao grupo da turma antes da primeira aula. Ninguém lhe perguntou nada.</p>'
 '<p class="aula-linha"><b>Hoje</b>, 180 minutos com uma pausa: o Ponto de partida em papel, depois decidir, ligar casos a artigos e fazer o mapa de direitos da escola.</p>')
DECIDE = (
 '<p>A fotografia pode ficar no grupo da turma?</p>'
 '<p class="pergunta-c">Decide em silêncio, de braço no ar: sim, não ou depende.</p>'
 '<details class="lado"><summary>A razão de quem a pôs no grupo</summary><div><p>«Foi uma brincadeira. Estava num autocarro, à vista de toda a gente, e não aparece nada de mal.»</p></div></details>'
 '<details class="lado"><summary>A razão da aluna</summary><div><p>«A imagem é minha. Estar num sítio público não quer dizer que aceito ser mostrada a trinta pessoas, a dormir.»</p></div></details>'
 '<details class="lado"><summary>Uma objeção</summary><div><p>E se a fotografia servisse para mostrar que o autocarro vai sempre cheio e os alunos não dormem o suficiente? A finalidade muda alguma coisa?</p></div></details>'
 '<p>Não há resposta certa neste cartão. Guarda a tua posição: vais voltar a ela.</p>')
ART1 = 'Todos os seres humanos nascem livres e iguais em dignidade e em direitos.'
CONCEITO = (
 '<p>Três textos, três forças diferentes:</p>'
 '<ul><li><b>Declaração Universal dos Direitos Humanos</b> (Nações Unidas, Paris, 10 de dezembro de 1948): uma declaração, não um tratado.</li>'
 '<li><b>Convenção sobre os Direitos da Criança</b> (1989): um tratado. Portugal ratificou-o em 1990, por isso obriga o Estado.</li>'
 '<li><b>Constituição da República Portuguesa</b>: a lei mais alta do país. O artigo 16.º manda ler os direitos fundamentais de acordo com a Declaração.</li></ul>')
NA_AULA = (
 '<p><b>O que se faz.</b> Primeiro, o Ponto de partida, em papel e sozinho. Depois, em grupos de três, o mapa de direitos: na planta da escola, colada na parede, cada grupo põe post-its com uma situação real ou possível e o número do artigo que a protege.</p>'
 '<p><b>Quanto tempo.</b> 60 a 75 minutos, com a pausa.</p>'
 '<p><b>O que fica escrito.</b> O teu Ponto de partida e dois post-its do teu grupo, com a situação e o artigo. O mapa fica fotografado para a sessão 10.</p>')
# 30/10/2026 (pedido do docente: «falta imagem e vídeo»): a fotografia de 1949, com a tabela de museu colada a ela, e
# o vídeo do TED-Ed, com uma tarefa tirada das três perguntas da descrição oficial do vídeo.
CARTAZ = (
 '<figure class="fig inteiro"><span class="moldura"><img src="../../../img/cidadania/eleanor-roosevelt-dudh-1949.webp" '
 'alt="Eleanor Roosevelt segura com as duas mãos um grande cartaz com o título «The Universal Declaration of Human Rights» e o símbolo das Nações Unidas." loading="lazy"></span>'
 '<figcaption>Eleanor Roosevelt com o cartaz da Declaração Universal, Lake Success, Nova Iorque, novembro de 1949. Biblioteca Presidencial Franklin D. Roosevelt, CC BY 2.0.</figcaption></figure>'
 '<p>Um ano depois de aprovada, a Declaração já circula em cartaz.</p>'
 '<p class="pergunta-c">Olha primeiro para a fotografia: porque é que se faz um cartaz de um texto que não obriga nenhum Estado?</p>'
 '<p>Responde no caderno, numa linha. Voltas a esta pergunta no fim da sessão.</p>')
VIDEO = (
 '<p>Um vídeo curto do TED-Ed, numa lição escrita por Benedetta Berti. É em inglês: liga as legendas no leitor.</p>'
 '<div class="yt" data-yt="nDgIVseTkuE" data-titulo="What are the universal human rights?, TED-Ed">'
 '<button type="button" class="yt-abrir" data-yt-abrir>Ver: «What are the universal human rights?» (4 min 47 s)</button>'
 '<p class="yt-cred">TED-Ed, lição de Benedetta Berti. O vídeo só se liga ao YouTube quando tocas no botão.</p></div>'
 '<p class="pergunta-c">Enquanto vês, procura a resposta do vídeo a três perguntas: o que são os direitos humanos básicos? Quem os escolhe? Quem os faz cumprir?</p>'
 '<p>Uma linha para cada uma, no caderno.</p>')
LEVAR = (
 '<p class="levar">Um direito é uma proteção que vale para todos, também para quem não conheces.</p>'
 '<p>Nesta sessão situaste casos da escola em artigos concretos e distinguiste uma declaração, um tratado e a Constituição. Volta à pergunta do cartaz de 1949: mudou a tua resposta? Na sessão 10 voltas ao mesmo mapa: o que mudou?</p>'
 '<p><b>As frases da sessão</b></p>'
 '<ul><li>Primeiro descrevo o que aconteceu; só depois procuro o direito.</li>'
 '<li>A Declaração não é uma lei portuguesa, mas a Constituição manda lê-la.</li>'
 '<li>Estar num sítio público não apaga o direito à imagem.</li>'
 '<li>Quando dois direitos chocam, pesa-se cada um no caso concreto.</li></ul>')

cartoes = [
 {"t":"ler","rot":"Abre","titulo":"Um mapa de direitos","html":ABRE},
 {"t":"ler","rot":"Decide","titulo":"A fotografia no grupo","html":DECIDE},
 {"t":"escolha","g":"caso","p":"No caso da fotografia, que direito da aluna está em causa em primeiro lugar?","p2":"A fotografia da aluna a dormir chegou ao grupo da turma. Que direito pesa mais neste caso?",
  "o":["A reserva da vida privada e a imagem.","A liberdade de reunião durante o intervalo.","O acesso gratuito ao ensino obrigatório."],"c":0,
  "f":"A fotografia mostra a aluna num momento que ela não escolheu mostrar. A Declaração protege a vida privada (artigo 12.º) e a Constituição protege a imagem e a reserva da intimidade (artigo 26.º).",
  "fe":["","A reunião é um direito de grupo e não está em causa: ninguém impediu a aluna de se juntar a outros.","A educação é um direito, mas a aluna não perdeu o acesso à escola. O que perdeu foi o controlo da sua imagem."]},
 {"t":"emparelhar","g":"artigos","p":"Liga cada situação ao artigo da Declaração que a protege.","p2":"Que artigo da Declaração está em causa em cada situação?",
  "pares":[["Uma fotografia partilhada sem perguntar","Artigo 12.º: vida privada"],["Um aluno de fora da visita pela nacionalidade","Artigo 2.º: sem discriminação"],["A turma quer reunir-se para fazer uma proposta","Artigo 20.º: reunião"],["Uma crítica à cantina no jornal da escola","Artigo 19.º: expressão"]],
  "f":"Cada artigo protege uma coisa concreta: a vida privada (12.º), a igualdade sem distinções (2.º), a reunião pacífica (20.º) e a liberdade de opinião e expressão (19.º).",
  "fe":"Lê primeiro o que a pessoa perdeu ou quer fazer; o artigo vem depois."},
 {"t":"ler","rot":"Conceito","titulo":"Declaração, tratado, Constituição","html":CONCEITO},
 {"t":"ler","rot":"Ver","titulo":"Um cartaz de 1949","html":CARTAZ},
 {"t":"ler","rot":"Ver","titulo":"Quem escolhe os direitos?","html":VIDEO},
 {"t":"vf","g":"forca","p":"A Declaração Universal dos Direitos Humanos é uma lei aprovada pela Assembleia da República.","p2":"A Declaração Universal foi aprovada como lei pelo Parlamento português.","v":False,
  "f":"A Declaração foi aprovada pela Assembleia Geral das Nações Unidas, em 1948. Não é uma lei portuguesa, mas a Constituição manda interpretar os direitos fundamentais de acordo com ela (artigo 16.º, n.º 2).",
  "fe":"Uma declaração das Nações Unidas não passa a lei portuguesa por ser importante. O elo com o direito português é o artigo 16.º da Constituição."},
 {"t":"vf","g":"forca","p":"A Convenção sobre os Direitos da Criança obriga o Estado português.","p2":"Portugal está obrigado a cumprir a Convenção sobre os Direitos da Criança.","v":True,
  "f":"A Convenção é um tratado e Portugal ratificou-a em 1990. Um tratado ratificado obriga o Estado que o ratificou.",
  "fe":"Ao contrário da Declaração, a Convenção é um tratado. Quando um Estado a ratifica, fica obrigado a cumpri-la."},
 {"t":"sublinhar","g":"artigo1","p":"Artigo 1.º da Declaração: toca nas duas palavras que dizem o que todos temos de igual.","p2":"No artigo 1.º, em que somos iguais? Toca nas duas palavras.","frase":ART1,"certas":[9,12],
  "f":"Somos iguais **em dignidade e em direitos**. Não diz que somos iguais em tudo: diz que ninguém vale menos e que os direitos são os mesmos para todos."},
 {"t":"escolha","g":"educacao","p":"Segundo a Declaração (artigo 26.º), o ensino elementar deve ser…","p2":"O que diz a Declaração sobre o ensino elementar?",
  "o":["gratuito e obrigatório.","pago pelas famílias.","escolhido por cada um."],"c":0,
  "f":"A Declaração diz que a educação deve ser gratuita, pelo menos no ensino elementar, e que esse ensino é obrigatório.",
  "fe":["","Se fosse pago, quem não pudesse pagar ficava de fora. É isso que a Declaração quer evitar.","A Declaração diz que o ensino elementar é obrigatório: não fica ao critério de cada um."]},
 {"t":"ordenar","g":"metodo","p":"Põe por ordem os passos para situar um direito num caso.","p2":"Qual é a ordem para encontrar o direito em causa num caso?",
  "passos":["Descrever o que aconteceu, sem adjetivos.","Perguntar quem foi afetado e de que forma.","Procurar o artigo que protege essa pessoa.","Ver se outro direito pesa do outro lado."],
  "f":"Primeiro os factos, depois a pessoa afetada, depois o artigo. No fim, ver se há outro direito do outro lado: muitas vezes há."},
 {"t":"escolha","g":"regras","p":"Um colega diz: «Na escola não há direitos, há regras.» Qual das respostas mostra melhor a relação entre as duas coisas?","p2":"«Na escola há regras, não direitos.» Qual das respostas corrige melhor esta ideia?",
  "o":["As regras da escola têm de respeitar os direitos.","As regras da escola substituem todos os direitos.","Os direitos só valem quando se sai do recinto da escola."],"c":0,
  "f":"A escola pode e deve ter regras, mas as regras ficam dentro dos direitos: não os podem anular. Uma regra que os anulasse podia ser contestada.",
  "fe":["","Uma regra de escola não pode tirar um direito que a Constituição garante. Pode organizá-lo, por exemplo dizer onde e quando se fazem reuniões.","Os direitos não ficam à porta. Valem na escola como em qualquer outro sítio."]},
 {"t":"ler","rot":"Na aula","titulo":"O mapa de direitos","html":NA_AULA},
 {"t":"escolha","g":"novo","p":"Caso inventado: para encontrar quem fez um vídeo ofensivo, a direção quer ler as mensagens dos telemóveis à entrada. Qual dos argumentos usa um direito para pôr limites a esta medida?","p2":"A direção quer ver as mensagens de todos os alunos para encontrar o autor de um vídeo. Que argumento põe limites com base num direito?",
  "o":["As mensagens privadas estão protegidas por lei.","O vídeo ofensivo não tem importância nenhuma.","A escola não pode ter regras sobre telemóveis."],"c":0,
  "f":"A Declaração protege a correspondência (artigo 12.º) e a Constituição protege o sigilo da correspondência e das comunicações privadas (artigo 34.º). Procurar o autor é legítimo; ler as mensagens de todos é outra coisa.",
  "fe":["","O vídeo pode ser grave e merecer investigação. O argumento não toca no problema dos direitos.","A escola pode ter regras sobre telemóveis. A questão é se pode ler mensagens privadas."]},
 {"t":"vf","g":"novo","p":"Quando dois direitos chocam, ganha sempre o de quem se queixou primeiro.","p2":"Se dois direitos entram em choque, vence o de quem apresentou queixa em primeiro lugar.","v":False,
  "f":"Quando dois direitos chocam, pesa-se cada um no caso concreto: o que está em causa, quanto se perde de cada lado e se há outra forma menos pesada de resolver.",
  "fe":"A ordem das queixas não decide nada. O que decide é o peso de cada direito naquele caso."},
 {"t":"escolha","g":"crianca","p":"A Convenção diz que a criança tem o direito de ser ouvida nos assuntos que lhe dizem respeito (artigo 12.º). Em que situação da escola isto pesa mais?","p2":"Onde é que o direito de um aluno a ser ouvido pesa mais?",
  "o":["Numa decisão disciplinar sobre o próprio aluno.","Na escolha da cor das paredes do pavilhão.","No horário de abertura da biblioteca municipal."],"c":0,
  "f":"O direito a ser ouvido pesa mais quando a decisão é sobre a própria pessoa e pode ter consequências para ela, como num processo disciplinar.",
  "fe":["","A opinião dos alunos pode contar, mas a cor das paredes não decide nada sobre um aluno em concreto.","A biblioteca municipal não é um assunto da escola nem uma decisão sobre um aluno."]},
 {"t":"vf","g":"novo","p":"A liberdade de expressão permite publicar a fotografia de qualquer pessoa sem lhe perguntar.","p2":"Por haver liberdade de expressão, posso publicar a fotografia de alguém sem autorização.","v":False,
  "f":"A liberdade de expressão (artigo 37.º da Constituição) convive com o direito à imagem (artigo 26.º). Exprimir uma opinião não dá licença para expor outra pessoa.",
  "fe":"Os dois direitos existem ao mesmo tempo. Volta ao caso da fotografia no autocarro: o que mudava se tivessem pedido?"},
 {"t":"ler","rot":"Para levar","escuro":True,"html":LEVAR},
]
dados = {
 "id":"cidadania-m1-s01","chave":"epi-cid-m1-s01","versao":"2026-10-30-2",
 "marca":"CD","titulo":"Sessão 01: Um mapa de direitos","h1":"Cidadania, módulo 1, sessão 01: Um mapa de direitos",
 "modulo":{"n":1,"nome":"Ser-se humano","url":"https://pedrohfernandes-klk.github.io/lente/cidadania/piloto/m1/"},
 "saida":"cidadania/piloto/m1-s01/index.html","piloto":True,
 "fontes":"Declaração Universal dos Direitos Humanos (Nações Unidas, 1948), artigos 1.º, 2.º, 12.º, 19.º, 20.º e 26.º; Convenção sobre os Direitos da Criança (1989), artigo 12.º; Constituição da República Portuguesa, artigos 16.º, 26.º, 34.º e 37.º. Fotografia: Eleanor Roosevelt com o cartaz da Declaração Universal, Lake Success, novembro de 1949 (Biblioteca Presidencial Franklin D. Roosevelt, CC BY 2.0). Vídeo: TED-Ed, «What are the universal human rights?», lição de Benedetta Berti. Os casos são inventados.",
 "cartoes":cartoes,
}
p = pathlib.Path(__file__).with_suffix('.json')
p.write_text(json.dumps(dados, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print(p, len(cartoes), 'cartões', sum(1 for c in cartoes if c['t'] != 'ler'), 'de fazer')
