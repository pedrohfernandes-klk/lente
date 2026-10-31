# Fonte da sessão 05 do M1 de Cidadania (piloto de 31/10/2026, no molde da sessão 01). Corre-se para escrever o .json
# ao lado; o .json é que o gerador (tools/licoes_lente.py) lê. Escreve-se em Python para não ter de escapar aspas à mão.
# Leis lidas a 31/10/2026: Lei n.º 58/2019 (artigos 3.º, 19.º e 21.º) e Constituição (artigos 18.º, 26.º e 35.º) na
# página da Procuradoria-Geral Distrital de Lisboa; Convenção sobre os Direitos da Criança (artigo 16.º) no PDF do GDDC;
# Declaração Universal (artigo 12.º) na página do Centro Regional de Informação das Nações Unidas (UNRIC).
# Bentham, «Panopticon; or, The Inspection-House» (1791), carta V, lido no Internet Archive (panopticonorins00bentgoog).
import json, pathlib
ABRE = (
 '<p class="pergunta-c">Que dados sobre ti a escola precisa de ter, e quem os pode ver?</p>'
 '<p>Caso inventado. Depois de três telemóveis desaparecidos, a associação de estudantes propõe câmaras nos corredores e nas salas. O cartaz diz: «Quem não deve, não teme.»</p>'
 '<p class="aula-linha"><b>Hoje</b>, 180 minutos com uma pausa: decidir, rever um formulário e contar as câmaras à volta da escola.</p>')
DECIDE = (
 '<p>A escola deve pôr câmaras nas salas de aula?</p>'
 '<p class="pergunta-c">Decide em silêncio, de braço no ar: sim, não ou depende.</p>'
 '<details class="lado"><summary>A razão de quem propõe</summary><div><p>«Com câmaras, ninguém rouba. Quem não deve, não teme.»</p></div></details>'
 '<details class="lado"><summary>A razão de quem discorda</summary><div><p>«Numa sala filmada o dia todo, ninguém fala à vontade. E quem vê as imagens?»</p></div></details>'
 '<details class="lado"><summary>Uma objeção</summary><div><p>E se as câmaras ficassem só à entrada e as imagens se apagassem ao fim de uma semana? Resolvia o problema dos telemóveis?</p></div></details>'
 '<p>Não há resposta certa neste cartão. Guarda a tua posição: vais voltar a ela.</p>')
LEI_19_3 = ('Nos estabelecimentos de ensino, as câmaras de videovigilância só podem incidir sobre os perímetros externos e locais de acesso, '
            'e ainda sobre espaços cujos bens e equipamentos requeiram especial proteção, como laboratórios ou salas de informática.')
# 31/10/2026 (decisão 18): a imagem e o vídeo da sessão. A planta de Willey Reveley (Commons) não se conseguiu
# descarregar: upload.wikimedia.org respondeu 429 três vezes, com Retry-After de 600 s, e não se insistiu. Entra a página
# de título da edição de 1791 (Bayerische Staatsbibliothek, digitalização no Internet Archive, 10059224bsb), domínio
# público, que acaba em «and schools». Lição do TED-Ed: oEmbed e página da lição verificados a 31/10; o título traz um
# travessão, por isso o botão descreve o vídeo em vez de o citar.
CARTAZ = (
 '<figure class="fig inteiro"><span class="moldura"><img src="../../../img/cidadania/panotico-bentham-1791.webp" '
 'alt="Página de título impressa de um livro de 1791, «Panopticon; or, The Inspection-House», de Jeremy Bentham. Uma lista em maiúsculas enumera os edifícios onde o plano se pode usar, de prisões e fábricas a hospitais, e acaba em «and schools»." loading="lazy"></span>'
 '<figcaption>Jeremy Bentham, <i>Panopticon; or, The Inspection-House</i>, página de título, Dublin e Londres, 1791. Bayerische Staatsbibliothek, via Internet Archive. Domínio público.</figcaption></figure>'
 '<p>Bentham propôs um edifício circular: as celas à volta e, ao centro, o lugar de quem inspeciona. Lê a lista do título até ao fim.</p>'
 '<p class="pergunta-c">Em que sítios queria Bentham pôr este edifício? Porque estará uma escola na lista?</p>'
 '<p>Responde no caderno, numa linha: o que muda no que as pessoas fazem quando nunca sabem se alguém está a ver?</p>')
VIDEO = (
 '<p>Um vídeo curto do TED-Ed, numa lição escrita por Michael Vazquez e Sarah Stroud. Num futuro com carros que flutuam, um governo quer dar uma pontuação a cada condutor e, para isso, pôr câmaras e microfones em todos os veículos. É em inglês: liga as legendas no leitor.</p>'
 '<div class="yt" data-yt="tmwIhOCXLrQ" data-titulo="Vídeo do TED-Ed sobre segurança e privacidade, lição de Michael Vazquez e Sarah Stroud">'
 '<button type="button" class="yt-abrir" data-yt-abrir>Ver: câmaras e microfones em todos os carros (5 min 30 s)</button>'
 '<p class="yt-cred">TED-Ed, lição de Michael Vazquez e Sarah Stroud. O vídeo só se liga ao YouTube quando tocas no botão.</p></div>'
 '<p class="pergunta-c">Enquanto vês, anota uma razão a favor, uma contra e a pergunta que farias a quem guarda as gravações.</p>')
NA_AULA = (
 '<p><b>O que se faz.</b> Primeiro, em grupos de três, a auditoria do formulário da visita de estudo, inventado e em papel: riscar o que não é preciso, dizer quem vê cada dado e quando se apaga. Depois, uma volta de 20 minutos ao quarteirão da escola, com o docente, a contar câmaras e avisos de videovigilância e a anotar o que cada aviso diz. Não se fotografam pessoas nem matrículas.</p>'
 '<p><b>Quanto tempo.</b> 60 a 75 minutos, com a pausa.</p>'
 '<p><b>O que fica escrito.</b> O formulário revisto, uma nota de privacidade em cinco linhas, o registo dos avisos e o plano de recolha das entrevistas do teatro-documento «Pergunta Humana»: o que se guarda, onde e até quando.</p>')
LEVAR = (
 '<p class="levar">Os dados pedem-se para uma finalidade, e só os que essa finalidade precisa.</p>'
 '<p>Nesta sessão pesaste segurança e privacidade e viste o que a lei deixa fazer numa escola. Volta ao panóptico: em que sítio da escola te sentes dentro dele? E volta à tua posição do início: as câmaras nas salas ficavam?</p>'
 '<p><b>As frases da sessão</b></p>'
 '<ul><li>Antes de dar um dado, pergunto para quê e quem o vê.</li>'
 '<li>Na escola, as câmaras só podem estar nos acessos, no perímetro e onde há bens que pedem especial proteção (Lei n.º 58/2019, artigo 19.º).</li>'
 '<li>Tenho direito a saber que dados há sobre mim e para quê (artigo 35.º).</li>'
 '<li>Ganha a medida menos pesada que resolve o problema.</li></ul>')

cartoes = [
 {"t":"ler","rot":"Abre","titulo":"Quem guarda os meus dados?","html":ABRE},
 {"t":"ler","rot":"Decide","titulo":"Câmaras nas salas","html":DECIDE},
 {"t":"escolha","g":"direito","p":"No caso das câmaras nas salas, que direito dos alunos está em causa em primeiro lugar?","p2":"Câmaras a filmar as salas o dia todo: que direito pesa mais neste caso?",
  "o":["A reserva da vida privada e os dados pessoais.","A liberdade de reunião dentro do recinto da escola.","O direito a um ensino gratuito e obrigatório."],"c":0,
  "f":"Uma câmara na sala grava cada aluno, a cada momento. A Constituição protege a imagem e a reserva da vida privada (artigo 26.º); a Convenção sobre os Direitos da Criança (artigo 16.º) e a Declaração Universal (artigo 12.º) protegem contra intromissões arbitrárias na vida privada.",
  "fe":["","Ninguém fica impedido de se reunir. O que muda é que cada gesto fica gravado e alguém o pode ver.","Ninguém perde o acesso às aulas. O que está em causa são as imagens de cada um e quem as vê."]},
 {"t":"vf","g":"lei","p":"Numa escola, as câmaras de videovigilância podem filmar o interior das salas de aula.","p2":"A lei deixa uma escola filmar as salas de aula com câmaras de videovigilância.","v":False,
  "f":"A Lei n.º 58/2019 (artigo 19.º, n.º 3) diz que, nas escolas, as câmaras só podem incidir sobre os perímetros externos, os locais de acesso e os espaços com bens que precisem de especial proteção, como laboratórios ou salas de informática. A sala de aula comum não está na lista.",
  "fe":"Volta à lista da lei: perímetros externos, acessos e espaços com equipamento que precisa de especial proteção. A sala de aula comum fica de fora."},
 {"t":"sublinhar","g":"lei19","p":"Lei n.º 58/2019, artigo 19.º, n.º 3: toca nas duas palavras que dizem onde as câmaras podem estar, à volta da escola e por onde se entra.","p2":"Onde podem estar as câmaras numa escola, à volta e por onde se entra? Toca nas duas palavras.","frase":LEI_19_3,"certas":[13,18],
  "f":"As câmaras podem incidir sobre os **perímetros** externos e os locais de **acesso**, e ainda sobre espaços com bens que precisem de especial proteção. Repara também no «só»: a lista é fechada."},
 {"t":"ler","rot":"Ver","titulo":"Uma casa de inspeção","html":CARTAZ},
 {"t":"emparelhar","g":"finalidade","p":"No formulário da visita de estudo, liga cada dado à finalidade que o justifica.","p2":"Para que serve cada dado do formulário da visita de estudo?",
  "pares":[["Alergias alimentares","O almoço durante a visita"],["Contacto de emergência","Um acidente durante a saída"],["Autorização do encarregado","Sair da escola em tempo de aula"],["Turma e número","A lista de presenças no autocarro"]],
  "f":"Cada dado tem uma razão concreta. Um dado sem finalidade, como a profissão dos pais numa visita de estudo, não se pede.",
  "fe":"Pergunta para quê antes de perguntar o quê: o dado vem depois da finalidade."},
 {"t":"escolha","g":"art35","p":"O artigo 35.º da Constituição fala dos dados informatizados que te dizem respeito. O que te garante?","p2":"Que direitos te dá o artigo 35.º da Constituição sobre os teus dados?",
  "o":["Aceder-lhes, corrigi-los e saber para que servem.","Apagar, quando quiseres, os dados de qualquer colega.","Escolher sozinho os dados que a escola recolhe."],"c":0,
  "f":"O artigo 35.º, n.º 1, garante o acesso aos dados informatizados que te digam respeito, o direito de exigir a sua retificação e atualização e o de conhecer a finalidade a que se destinam. O n.º 7 dá a mesma proteção aos dados em ficheiros manuais, como um formulário em papel.",
  "fe":["","O artigo protege os teus dados, não te dá poder sobre os dos outros. O n.º 4 proíbe o acesso a dados pessoais de terceiros, salvo exceções previstas na lei.","A escola pode pedir os dados que a lei exige ou que uma finalidade justifica. O que tens é o direito de os ver, corrigir e saber para quê."]},
 {"t":"ler","rot":"Ver","titulo":"Câmaras em todos os carros","html":VIDEO},
 {"t":"vf","g":"guardar","p":"Uma pasta partilhada com a turma toda é um bom sítio para guardar as alergias dos colegas.","p2":"Guardar as alergias de todos numa pasta aberta à turma inteira é adequado.","v":False,
  "f":"As alergias são dados de saúde. Quem precisa delas é quem organiza a refeição e quem acompanha a visita, não a turma toda. O artigo 35.º, n.º 4, da Constituição proíbe o acesso a dados pessoais de terceiros, salvo exceções previstas na lei.",
  "fe":"Pergunta quem precisa de ver o dado. Se a resposta é duas pessoas, a pasta não pode estar aberta a trinta."},
 {"t":"escolha","g":"panotico","p":"No panóptico de Bentham, o que faz o edifício funcionar mesmo quando ninguém está a vigiar?","p2":"Porque é que o panóptico pode funcionar sem ninguém no posto de vigia?",
  "o":["Quem é vigiado nunca sabe se está a ser visto.","As celas ficam fechadas com grades muito fortes.","Os guardas trocam de turno de hora a hora."],"c":0,
  "f":"Bentham escreveu que o ponto mais importante era quem é inspecionado sentir-se sempre sob inspeção, ou com grande probabilidade de o estar. Quem nunca sabe porta-se como se estivesse sempre a ser visto.",
  "fe":["","As grades fecham, mas não explicam a ideia do plano. O que conta é a dúvida: estarei a ser visto agora?","A troca de turno não muda nada para quem está na cela. O que conta é não saber se alguém está a ver."]},
 {"t":"ordenar","g":"passos","p":"Põe por ordem os passos para recolher dados de alguém.","p2":"Qual é a ordem certa para recolher dados de uma pessoa?",
  "passos":["Decidir para que servem os dados.","Riscar o que essa finalidade não precisa.","Pedir os dados, dizendo para quê e quem os vê.","Apagá-los quando a finalidade acaba."],
  "f":"Primeiro a finalidade, depois só o que ela precisa. Ao pedir, diz-se para quê e quem vê. No fim, apaga-se: a Lei n.º 58/2019 (artigo 21.º) diz que, sem prazo fixado por norma, os dados se guardam o tempo necessário para a finalidade."},
 {"t":"ler","rot":"Na aula","titulo":"O formulário e o quarteirão","html":NA_AULA},
 {"t":"escolha","g":"novo","p":"Caso inventado: uma aplicação de presenças passa a guardar a localização dos alunos o dia todo. Qual dos argumentos põe limites a esta medida?","p2":"Uma aplicação de presenças guarda onde está cada aluno, todo o dia. Que argumento lhe põe limites?",
  "o":["Para marcar presenças, basta saber quem entrou na aula.","A aplicação é nova e ainda pode ter alguns erros graves.","Os alunos já usam outras aplicações com localização."],"c":0,
  "f":"A finalidade é marcar presenças. Para isso não é preciso saber onde cada aluno está a cada minuto. Recolher mais do que a finalidade precisa é recolher dados a mais.",
  "fe":["","Os erros podem corrigir-se. O problema continua: a aplicação recolhe muito mais do que a finalidade precisa.","Que outras aplicações o façam não torna esta recolha necessária. A pergunta é sempre: para quê?"]},
 {"t":"vf","g":"som","p":"Numa escola com videovigilância, as câmaras podem gravar o som das conversas durante as aulas.","p2":"Durante as aulas, as câmaras de videovigilância de uma escola podem captar o som.","v":False,
  "f":"A Lei n.º 58/2019 (artigo 19.º, n.º 4) proíbe a captação de som onde há videovigilância, exceto quando as instalações vigiadas estão encerradas ou com autorização prévia da Comissão Nacional de Proteção de Dados.",
  "fe":"Imagem e som são coisas diferentes. Mesmo onde a câmara é permitida, o som fica de fora enquanto as instalações estão abertas."},
 {"t":"completar","g":"medida","p":"Completa a ideia do artigo 18.º, n.º 2, da Constituição e a regra que dela se tira.","p2":"Que palavras completam a regra das restrições a direitos?",
  "frase":"Uma lei só pode restringir um direito no que for [1] para salvaguardar outros direitos. Se duas medidas resolvem o problema, escolhe-se a [2].",
  "lacunas":[{"o":["necessário","conveniente","possível"],"c":0},{"o":["menos pesada","mais barata","mais rápida"],"c":0}],
  "f":"A Constituição diz que as restrições a direitos devem «limitar-se ao necessário para salvaguardar outros direitos ou interesses constitucionalmente protegidos» (artigo 18.º, n.º 2). Daí a regra prática: se duas medidas resolvem o problema, fica a menos pesada.",
  "fe":"Volta às câmaras: à entrada resolvem os furtos com menos peso do que nas salas."},
 {"t":"escolha","g":"projeto","p":"No projeto, gravaste uma entrevista com uma funcionária da escola. O trabalho acabou. Que fazer à gravação?","p2":"O trabalho com a entrevista gravada terminou. O que se faz à gravação?",
  "o":["Apagá-la no prazo combinado com a pessoa entrevistada.","Guardá-la no telemóvel, para o caso de vir a servir.","Pô-la na conta da turma, para que outros a possam ouvir."],"c":0,
  "f":"A gravação foi feita para o trabalho. Acabada a finalidade, apaga-se no prazo que se combinou com a pessoa. Guardar «para o caso de» é guardar sem finalidade.",
  "fe":["","«Para o caso de» não é uma finalidade. A pessoa aceitou ser gravada para o trabalho, não para sempre.","Publicar é outra finalidade, que a pessoa não aceitou. Teria de se lhe pedir de novo."]},
 {"t":"emparelhar","g":"papeis","p":"No formulário da visita, liga cada papel na proteção de dados a quem o tem.","p2":"No formulário da visita, quem é quem na proteção de dados?",
  "pares":[["Titular dos dados","O aluno que preenche o formulário"],["Responsável pelo tratamento","A escola que organiza a visita"],["Autoridade de controlo","A Comissão Nacional de Proteção de Dados"]],
  "f":"O titular é a pessoa a quem os dados dizem respeito. O responsável pelo tratamento decide para que servem e como se guardam. A Comissão Nacional de Proteção de Dados é a autoridade de controlo em Portugal (Lei n.º 58/2019, artigo 3.º).",
  "fe":"Pergunta de quem são os dados, quem os usa e quem vigia quem os usa."},
 {"t":"ler","rot":"Para levar","escuro":True,"html":LEVAR},
]
dados = {
 "id":"cidadania-m1-s05","chave":"epi-cid-m1-s05","versao":"2026-10-31-1",
 "marca":"CD","titulo":"Sessão 05: Quem guarda os meus dados?","h1":"Cidadania, módulo 1, sessão 05: Quem guarda os meus dados?",
 "modulo":{"n":1,"nome":"Ser-se humano","url":"https://pedrohfernandes-klk.github.io/lente/cidadania/piloto/m1/"},
 "saida":"cidadania/piloto/m1-s05/index.html","piloto":True,
 "fontes":"Lei n.º 58/2019, de 8 de agosto (Lei da Proteção de Dados Pessoais), artigos 3.º, 19.º e 21.º; Constituição da República Portuguesa, artigos 18.º, 26.º e 35.º; Convenção sobre os Direitos da Criança (1989), artigo 16.º; Declaração Universal dos Direitos Humanos (1948), artigo 12.º. Jeremy Bentham, «Panopticon; or, The Inspection-House» (1791), cartas II e V. Imagem: Jeremy Bentham, «Panopticon; or, The Inspection-House», página de título, 1791 (Bayerische Staatsbibliothek, via Internet Archive, domínio público). Vídeo: TED-Ed, lição de Michael Vazquez e Sarah Stroud. Os casos são inventados.",
 "cartoes":cartoes,
}
p = pathlib.Path(__file__).with_suffix('.json')
p.write_text(json.dumps(dados, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print(p, len(cartoes), 'cartões', sum(1 for c in cartoes if c['t'] != 'ler'), 'de fazer')
