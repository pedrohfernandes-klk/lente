window.LenteCenaQueFalta={
"id":"cena-que-falta",
"titulo":"A cena que falta",
"quadros":{
 "perda":{"titulo":"A perda","n":"01","img":"perda","legenda":"Uma mulher de cachecol vermelho afasta-se para a esquerda. A carteira cai-lhe sem ela dar por isso."},
 "olhar":{"titulo":"O olhar","n":"02","img":"olhar","legenda":"Uma pessoa de casaco verde repara na carteira, na outra ponta do banco."},
 "mao":{"titulo":"A mão","n":"03","img":"mao","legenda":"A mão da pessoa de casaco verde pega na carteira."},
 "lacuna":{"titulo":"?","n":"04","legenda":"Entre estes dois planos passa tempo. Não sabes quanto, nem o quê."},
 "devolucao":{"titulo":"A devolução","n":"05","img":"devolucao","legenda":"A pessoa de casaco verde entrega a carteira à mulher."},
 "bolso":{"titulo":"O bolso","n":"04","intertitulo":true,"legenda":"A pessoa de casaco verde guarda a carteira no bolso de dentro e afasta-se do banco."},
 "cartao":{"titulo":"O cartão","n":"04","intertitulo":true,"legenda":"A carteira aberta, segura por mãos de mangas verdes. Num cartão, o retrato de uma mulher de cachecol."},
 "regresso":{"titulo":"O regresso","n":"04","intertitulo":true,"legenda":"A mulher volta pelo caminho, vinda da esquerda, de mala aberta, a olhar para o chão."}
},
"tira":["perda","olhar","mao","lacuna","devolucao"],
"candidatos":["bolso","cartao","regresso"],
"hipoteses":[
 {"id":"H1","t":"Quem a encontrou ficou com ela algum tempo."},
 {"id":"H2","t":"Quem a encontrou foi à procura da dona."},
 {"id":"H3","t":"A dona voltou para a procurar."},
 {"id":"H4","t":"Ninguém abriu a carteira."}
],
"nenhuma":"Nenhuma me parece mais forte",
"estadosNomes":{"ganha":"ganha apoio","perde":"perde apoio","igual":"não muda","aberto":"em aberto"},
"estadosCurtos":{"ganha":"ganha","perde":"perde","igual":"não muda"},
"estadoFrase":{"ganha":"ganha apoio","perde":"perde apoio","igual":"fica como estava"},
"marcas":{"●":"Sustenta-se","◐":"Também se defende","○":"Difícil de sustentar"},
"estadosSimbolos":{"ganha":"▲","perde":"▼","igual":"=","aberto":"?"},
"estados":{
 "bolso":{
  "H1":{"estado":"ganha","razao":"Sai do banco com a carteira no bolso."},
  "H2":{"estado":"igual","razao":"Guardar a carteira não diz para onde a leva."},
  "H3":{"estado":"igual","razao":"A dona não aparece neste plano."},
  "H4":{"estado":"igual","razao":"O bolso esconde a carteira: não se vê se foi aberta."}},
 "cartao":{
  "H1":{"estado":"igual","razao":"Abrir uma carteira pode demorar segundos."},
  "H2":{"estado":"ganha","razao":"Passa a haver um rosto para procurar."},
  "H3":{"estado":"igual","razao":"A dona só aparece num retrato."},
  "H4":{"estado":"perde","razao":"A carteira está aberta."}},
 "regresso":{
  "H1":{"estado":"igual","razao":"Quem a encontrou não aparece neste plano."},
  "H2":{"estado":"perde","razao":"Se a dona volta, o encontro não precisa de procura.","discutivel":true,"alternativa":"A dona voltar não diz o que a outra pessoa fez. Por isso também se lê aqui «não muda»."},
  "H3":{"estado":"ganha","razao":"Volta pelo caminho, a olhar para o chão."},
  "H4":{"estado":"igual","razao":"A carteira não aparece neste plano."}}
},
"quadroTitulo":"O que cada plano faz às hipóteses",
"quadroNota":"Leitura do Lente. Ganhar ou perder apoio não é provar nem excluir.",
"abertoLinha":"A sequência ainda não diz.",
"explicacao":{
 "bolso":{"titulo":"Com «O bolso», a devolução chega depois de uma saída.","corpo":"A carteira vai para o bolso de dentro, e quem a encontrou afasta-se do banco. Ganha apoio a ideia de que ficou com ela algum tempo. É o plano que mais facilmente se lê como suspeita. Repara, porém, no que mostra: um bolso e uma saída. Hesitar, procurar uma morada ou ficar com a carteira até mudar de ideias cabem neste plano. Para onde a leva, o plano não diz. Ficar com ela também cabe: o bolso não desmente quem desconfia.","alternativa":"Guardar uma carteira no bolso também é uma maneira de não a perder. Quem a vai entregar numa esquadra também a guarda.","ves":"um bolso e uma saída"},
 "cartao":{"titulo":"Com «O cartão», quem encontrou passa a ter um rosto para procurar.","corpo":"A carteira está aberta, e num cartão há o retrato de uma mulher de cachecol. Ganha apoio a ideia de que houve procura da dona: agora há como a reconhecer. Perde apoio a de que ninguém abriu a carteira. O mesmo gesto serve duas leituras: abrir a carteira de outra pessoa é procurar a dona e é também mexer no que não é nosso. O plano não escolhe por ti.","ves":"uma carteira aberta e um retrato"},
 "regresso":{"titulo":"Com «O regresso», a dona deixa de ser só quem perdeu.","corpo":"Ela volta pelo caminho, de mala aberta, a olhar para o chão. Ganha apoio a ideia de que deu pela falta da carteira. Sobre o que fez quem a encontrou, o plano não mostra nada; mas dá outra razão para o encontro, e por isso a procura dessa pessoa deixa de ser precisa para explicar o fim. A mulher, que até aqui só perdia e recebia, passa a agir.","alternativa":"A dona voltar não diz o que a outra pessoa fez. Por isso também se lê aqui «não muda» para a procura.","ves":"uma mulher que procura"}
},
"linhaComum":"Vês: {ves}. Sabes: a carteira volta à dona. Supões: o resto.",
"linhaTu":"«{H}»: tu marcaste {tu}; o Lente lê {lente}. {razao}",
"linhaIgual":"«{H}»: tu e o Lente marcam {lente}. {razao}",
"linhaSo":"«{H}»: o Lente lê {lente}. {razao}",
"pares":{
 "bolso+cartao":{"principal":"H2","sintese":"Nas duas montagens, quem encontrou age sozinho; muda o que as suas mãos te deixam supor.",
  "H1":"Com «O bolso», a carteira sai do banco e o tempo alonga-se; com «O cartão», tudo pode ter durado um minuto. Só o plano do meio sugere quanto tempo passou.",
  "H2":"Com «O bolso», a hipótese fica onde estava: guardar a carteira não diz para onde a leva. Com «O cartão», ganha apoio: passa a haver um rosto para procurar. A mesma pessoa, com a mesma carteira, deixa a hipótese parada numa montagem e empurra-a na outra.",
  "H4":"Só «O cartão» mostra a carteira aberta. Com «O bolso» não sabes se foi aberta: o bolso esconde-a. Não ver não é o mesmo que não ter acontecido."},
 "bolso+regresso":{"principal":"H3","sintese":"Uma montagem segue quem encontrou; a outra segue a dona. Mudar o lado para onde a câmara olha muda as perguntas que fazes.",
  "H1":"«O bolso» alonga o tempo de quem a encontrou; «O regresso» não diz nada sobre essa pessoa, porque a câmara está com a dona. Uma hipótese pode ficar como estava só porque o plano olha para outro lado.",
  "H2":"Fica como estava com «O bolso» e perde apoio com «O regresso». Repara de onde vem a perda: não de nada que quem encontrou faça, mas de outra pessoa entrar na cena. É uma leitura discutível; a outra pessoa pode ter procurado na mesma.",
  "H3":"Só «O regresso» mostra que a dona deu pela falta. Com «O bolso», ela fica fora da história entre a perda e a devolução."},
 "cartao+regresso":{"principal":"H2","sintese":"As duas montagens dão uma razão para o encontro: alguém procurou, ou alguém voltou. Nenhuma prova que a outra razão não existiu.",
  "H2":"Ganha apoio com «O cartão» e perde com «O regresso». Numa montagem, quem encontrou procura; na outra, quem perdeu volta. A devolução é o mesmo plano, mas o encontro deixa de ser obra da mesma pessoa.",
  "H3":"Só «O regresso» mostra a dona a procurar. Com «O cartão», ela só existe num retrato, nas mãos de outra pessoa.",
  "H4":"«O cartão» mostra a carteira aberta; «O regresso» não mostra a carteira. Uma montagem responde a esta hipótese; a outra deixa-a em aberto."}
},
"igual":"Esta hipótese ficou igual nas duas montagens ({estado}). Procura uma que tenha mudado.",
"legendasFim":[
 {"id":"neutra","t":"Devolve o que encontrou.","pede":"","com":"diz só o que se vê no princípio e no fim; serve a qualquer montagem.","sem":"diz só o que se vê no princípio e no fim; serve a qualquer montagem."},
 {"id":"afinal","t":"Afinal, devolve.","pede":"bolso","com":"o bolso deixa supor que podia não voltar; não o mostra.","sem":"nenhum plano desta montagem deixa supor que a carteira podia não voltar."},
 {"id":"retrato","t":"Encontrou a dona pelo retrato.","pede":"cartao","com":"o retrato deixa supor uma procura; não a mostra.","sem":"esta montagem não mostra nenhum retrato nem nenhuma procura."},
 {"id":"tempo","t":"A dona voltou a tempo.","pede":"regresso","com":"a dona volta pelo caminho; que tenha chegado a tempo, o plano não mostra.","sem":"esta montagem não mostra a dona a voltar."}
],
"abre":{
 "rotulo":"Lê",
 "meta":"Corta! / montagem / cerca de 15 min",
 "texto":"Uma carteira perdida, uma carteira devolvida. Entre as duas, falta um plano.",
 "nota":"Uma cena do Lente, em planos descritos e intertítulos. Não é uma adaptação de nenhuma obra.",
 "papel":"Também se faz sem ecrã: imprime o enunciado."
},
"ve":{
 "rotulo":"Vê",
 "pergunta":"Lê a sequência. Qual destas hipóteses te parece mais forte agora? Toca numa."
},
"escolhe":{
 "rotulo":"Escolhe",
 "pergunta":"Escolhe o plano que entra no espaço em branco.",
 "perguntaH":"Escolhe o plano que, para ti, mais mexe com «{H}».",
 "perguntaOutra":"Agora outro plano no mesmo lugar. O que fará à hipótese «{H}»?",
 "perguntaOutraSem":"Agora outro plano no mesmo lugar. O que muda nas hipóteses?",
 "marcarH":"Com «{plano}» no meio, o que acontece a cada hipótese? Marca pelo menos a tua e carrega em «Verificar».",
 "marcarSem":"Com «{plano}» no meio, o que acontece às hipóteses? Marca pelo menos uma e carrega em «Verificar».",
 "tu":"tu",
 "lente":"Lente",
 "novo":"novo plano",
 "noMeio":"no meio"
},
"compara":{
 "rotulo":"Compara",
 "pergunta":"As tuas duas montagens acabam no mesmo plano. Dá-lhe uma legenda em cada uma.",
 "precisa":"Para comparar, precisas de duas montagens diferentes.",
 "difTitulo":"O mesmo plano, duas legendas.",
 "difCorpo":"Com «{p1}», legendaste «{l1}»; com «{p2}», «{l2}». O plano não mudou: mudou o que vês no meio.",
 "igualTitulo":"A mesma legenda nas duas.",
 "neutraTitulo":"A legenda mais prudente, nas duas.",
 "neutraCorpo":"«{l}» serve às duas montagens porque diz só o que vês: é a legenda mais prudente. As outras supõem mais, e cada uma se apoia num plano diferente. Experimenta uma delas e vê com que montagem condiz.",
 "igualCorpo":"Para ti, o plano do meio não muda o que o último plano diz. Pode ser: «{l}» serve às duas montagens? Olha para o quadro: «{H}» mudou de uma montagem para a outra.",
 "ves":"Vês:",
 "supoesCom":"Supões, com apoio no plano do meio:",
 "supoesSem":"Supões sem apoio nesta montagem:",
 "ultimas":"Comparas as duas últimas montagens que experimentaste.",
 "foraTres":"«{p}» fica de fora: para o comparar, volta a «Escolhe» e põe-no outra vez no meio."
},
"reve":{
 "rotulo":"Revê",
 "pergunta":"Volta à hipótese que te parecia mais forte. Depois das montagens, o que fazes com ela?",
 "perguntaNenhuma":"No início, nenhuma hipótese te parecia mais forte. E agora?",
 "respostas":[{"id":"mantenho","t":"Mantenho-a"},{"id":"corrijo","t":"Corrijo-a"},{"id":"aberto","t":"Deixo-a em aberto"}],
 "continua":"Continua nenhuma",
 "plano":"Que plano fez mais diferença?",
 "nenhumPlano":"Nenhum",
 "textos":{
  "mantenho":{"perdeu":"Manténs «{H}», embora tenha perdido apoio com «{P}». Pode fazer sentido: essa é só uma das cenas possíveis. Diz, no caderno, que plano escolhes para a tua versão.","ganhou":"Manténs «{H}», e «{G}» deu-lhe apoio. Repara que o apoio veio de um plano que tu escolheste pôr lá.","nenhum":"Manténs «{H}». Nenhum dos planos que experimentaste lhe tocou: a hipótese continua tão aberta como estava.","ambos":"Manténs «{H}»: «{G}» deu-lhe apoio e «{P}» tirou-lho. Mantê-la é escolher a montagem com «{G}»; diz, no caderno, porque te parece a mais provável."},
  "corrijo":{"perdeu":"Corriges «{H}» depois de «{P}» lhe tirar apoio. O plano do fim é o mesmo; mudou o que vês no meio.","ambos":"Corriges «{H}»: «{P}» tirou-lhe apoio, embora «{G}» lho tenha dado. Que montagem te parece mais provável, e porquê?","ganhou":"Corriges «{H}», embora «{G}» lhe tenha dado apoio. Talvez outra montagem te pareça mais provável: qual?","nenhum":"Corriges «{H}» sem que os planos lhe tenham tocado. O que te fez mudar? Pode ter sido a comparação, e não um plano."},
  "aberto":{"perdeu":"Deixas «{H}» em aberto: viste que um plano a pode enfraquecer. Suspender o juízo, aqui, é uma conclusão.","ganhou":"Deixas «{H}» em aberto, embora «{G}» a reforce. Um plano que apoia não é uma prova.","nenhum":"Deixas «{H}» em aberto, e nenhum plano lhe tocou. É a leitura mais prudente com o que viste.","ambos":"Deixas «{H}» em aberto: viste um plano reforçá-la e outro enfraquecê-la. Suspender o juízo, aqui, é uma conclusão."},
  "nenhuma":{"continua":"Manténs o juízo suspenso depois de veres planos que reforçam umas hipóteses e enfraquecem outras. É uma conclusão, não uma falta de resposta.","ganhou":"Escolhes agora «{H}». Repara de onde lhe veio a força: de «{G}», um plano que tu puseste no meio.","sem":"Escolhes «{H}», embora nenhum dos planos que experimentaste lhe tenha dado apoio. O que te fez escolher?"}
 },
 "planoLinha":"Disseste que «{plano}» fez mais diferença. Com esse plano, «{H}» {estado}.",
 "planoLinhaSem":"Disseste que «{plano}» fez mais diferença.",
 "nenhumLinha":"Disseste que nenhum plano fez mais diferença do que os outros."
},
"escreve":{
 "rotulo":"Escreve",
 "marca":"Opcional",
 "pergunta":"Escreve a frase que falta entre estas duas.",
 "frases":["Uma mulher entra no autocarro com um vaso de planta ao colo.","…","No fim da linha, sai sem o vaso."],
 "regra":"Só o que uma câmara mostraria: ações, objetos, lugares. Nada de pensamentos, intenções ou «porque».",
 "hipoteses":["Esqueceu-se do vaso.","Deu o vaso a alguém.","O vaso nunca foi dela."],
 "palavras":["porque","pensa","pensou","pensava","quer","queria","quis","decide","decidiu","lembra","lembrou","esquece","esqueceu","sente","sentiu","acha","achou"],
 "aviso":"Repara em «{palavra}»: é uma ação que se vê ou um pensamento? Se uma câmara a pudesse mostrar, deixa-a ficar.",
 "avisoPorque":"Repara em «porque»: explica; uma câmara mostra o que acontece, não porquê.",
 "semAviso":"A verificação só procura palavras de pensamento e «porque». Não encontrou nenhuma. O resto verificas tu.",
 "marcar":"Com a tua frase no meio, cada hipótese ganha apoio, perde apoio ou não muda?",
 "legenda":"A frase do meio. Fica só neste separador; para a guardar, usa «Levar o caderno» no menu.",
 "titulo":"Fizeste o mesmo gesto da cena, ao contrário.",
 "corpo":"Com a tua frase no meio, marcaste: {marcas}. Em turma: lê a tua frase a um colega, sem mostrares as tuas marcas. Ele marca as hipóteses. Se não coincidirem, a vossa conversa é o exercício."
},
"fim":{
 "rotulo":"Para levar",
 "texto":"Um plano no meio pode mudar o que um fim quer dizer, sem mudar o plano do fim. Vês o que um plano mostra; o resto supões. Um plano que dá apoio a uma hipótese não a prova.",
 "ligacoes":[
  {"t":"Certa manhã (Kafka) →","href":"../../formas/certa-manha/"},
  {"t":"As oito cenas literárias →","href":"../"},
  {"t":"A mesa de montagem anterior →","href":"../mesa/"},
  {"t":"Voltar ao laboratório","href":"../../"}
 ]
},
"creditos":"Cena e descrições dos planos: Lente, 2026, CC BY-SA 4.0.",
"piloto":[
  {
    "id": "ver",
    "tipo": "hipotese",
    "p": "Entre perder e recuperar a carteira, o que pode ter acontecido?",
    "o": [
      "Alguém procurou a dona.",
      "A dona voltou ao local.",
      "Alguém guardou o achado."
    ],
    "valores": [
      "H2",
      "H3",
      "H1"
    ],
    "f": "Os planos mostram a perda e a devolução; o que aconteceu entre eles continua por descobrir.",
    "fe": []
  },
  {
    "id": "montar",
    "tipo": "planos",
    "p": "Que plano pões entre a perda e a devolução?",
    "o": [
      "Guardar a carteira",
      "Procurar no cartão",
      "Voltar pelo caminho"
    ],
    "valores": [
      "bolso",
      "cartao",
      "regresso"
    ],
    "f": "O plano entra na sequência; a devolução mantém-se.",
    "fe": [
      "O bolso permite supor uma demora, mas não revela uma intenção.",
      "O retrato dá um rosto para procurar, mas não prova que houve procura.",
      "O regresso mostra a dona a procurar, sem mostrar o que a outra pessoa fez."
    ]
  },
  {
    "id": "outra",
    "tipo": "planos",
    "p": "Experimenta outro plano no mesmo lugar.",
    "o": [
      "Guardar a carteira",
      "Procurar no cartão",
      "Voltar pelo caminho"
    ],
    "valores": [
      "bolso",
      "cartao",
      "regresso"
    ],
    "f": "O plano entra na sequência; a devolução mantém-se.",
    "fe": [
      "O bolso permite supor uma demora, mas não revela uma intenção.",
      "O retrato dá um rosto para procurar, mas não prova que houve procura.",
      "O regresso mostra a dona a procurar, sem mostrar o que a outra pessoa fez."
    ]
  },
  {
    "id": "comparar",
    "tipo": "comparar",
    "p": "Depois das duas montagens, que hipótese te parece mais forte?",
    "o": [
      "Alguém procurou a dona.",
      "A dona voltou ao local.",
      "Alguém guardou o achado."
    ],
    "f": "Compara o que supunhas com o que cada plano te deixa ver.",
    "fe": [],
    "valores": [
      "H2",
      "H3",
      "H1"
    ]
  },
  {
    "id": "fim",
    "tipo": "fim",
    "p": "Leva esta experiência contigo."
  }
]
};
