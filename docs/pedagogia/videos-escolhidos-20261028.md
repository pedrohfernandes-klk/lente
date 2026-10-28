# Vídeos escolhidos, ronda 1 (28/10/2026)

Na página de curadoria, o docente disse «Sim» a 33 dos 105 vídeos da primeira lista. Este documento diz onde ficou cada um, o que convém confirmar antes da aula e o que ainda não entrou.

## Como funciona

- Cada vídeo entra num cartão de leitura «Para ver», no próprio baralho. O cartão tem:
  - o porquê daquele vídeo naquele sítio;
  - uma pergunta antes de ver;
  - o leitor;
  - uma pergunta depois de ver, para responder em papel ou em voz alta;
  - uma nota curta (língua, legendas, data).
- O leitor só carrega quando o aluno toca em «Ver o vídeo». Usa o modo de privacidade reforçada do YouTube (youtube-nocookie), com as legendas ligadas. Ao lado, há uma ligação «Ver no YouTube».
- No máximo dois cartões «Para ver» por baralho.
- Os cartões de leitura não contam para a pontuação, e o motor só guarda tentativas e melhores resultados. O progresso já guardado nos aparelhos não muda.
- No cartão «Uma pergunta, um vídeo», da Ética, o aluno escolhe uma das três perguntas de bolso. Cada botão troca o vídeo e as perguntas.
- Componente: `assets/para-ver.css` e `assets/para-ver.js`.
- Dados: `tools/videos-escolhidos.json`. Aplicação: `python3 tools/videos_escolhidos.py`. O script é idempotente e não reescreve os outros cartões. Se um gerador refizer uma destas páginas, basta voltar a correr o script.
- Teste: `tests/test_videos_escolhidos.py`.

## Onde ficou cada vídeo (23 neste PR)

| Página | Cartão | Vídeo | Confirmar antes da aula |
| --- | --- | --- | --- |
| Ética | Lei, moral e ética | The Ethics Centre, «What is the difference between Ethics, Morality and the Law?» (5:14) | Legendas; exemplos de contexto australiano |
| Ética | Uma pergunta, um vídeo | The Ethics Centre: «Consequentialism» (4:03), «Deontology» (3:10), «Virtue Ethics» (3:19) | Exemplos de cada vídeo |
| Estética | O que é arte? | CrashCourse, «Aesthetics», Philosophy #31 (10:38) | Que teorias apresenta |
| Estética | O sublime | The School of Life, «Burke on: The Sublime» (4:21) | Conteúdo |
| Cidadania M1, O júri | De onde vem a certeza? | The Ethics Centre, «Moral Intuition & Ethical Judgement» (3:26) | Conteúdo |
| Cidadania M1, O júri | Saltar para a conclusão | The Ethics Centre, «What is Unconscious Bias?» (2:37) | Tema sensível: ver os exemplos |
| Ter juízo, Ética, lição 2 (Nagel) | Outro Nagel: a sorte moral | CrashCourse, «Moral Luck», Philosophy #39 (9:46) | O exemplo clássico envolve condução sob efeito de álcool |
| Sidequest «A caverna» | Para ir mais longe: Platão e os poetas | Michael Sugrue, «Plato and Poetry» (46:43) | Aula longa: indicar o trecho (até 12 minutos) |
| Sidequest «O herói» | Ouvir a fonte | Joseph Campbell Foundation, «The Hero with a Thousand Faces» (3:12) | Se é leitura do livro ou entrevista |
| Sidequest «O herói» | Para ir mais longe: o monomito | CrashCourse, «The Hero's Journey and the Monomyth», World Mythology #25 (13:20) | Se critica o modelo de Campbell |
| Cidadania M2, O contexto em falta | Uma imagem verdadeira pode enganar | CrashCourse, «Evaluating Photos & Videos», Navigating Digital Information #7 (13:19) | Exemplos de catástrofes ou conflitos; série de 2019 |
| Cidadania M2, O rasto da afirmação | Em quem confias? | The Ethics Centre, «What sources do you use and trust when preparing to vote?» (2:49) | Contexto eleitoral australiano: discutir fontes, não partidos |
| Cidadania M2, passo 0 | Arte ou design? | CrashCourse, «What's the Difference Between Art & Design?» (11:29) | Conteúdo |
| Como se investiga, passo 6 | Saber, crer e não saber | Carl Sagan, «Carl Sagan on the Existence of God» (5:01) | Canal não oficial: confirmar a origem da gravação |
| Como se investiga, passo 8 | Ler para os lados | CrashCourse, «Check Yourself with Lateral Reading», Navigating Digital Information #3 (13:52) | Apoios declarados no fim do vídeo |
| Lab, A fábula em pedaços | Uma espera sem desenlace | Philosophy Tube, «"Waiting for Godot" Explained with Philosophy» (8:37) | Tom e linguagem |
| Lab, História e enredo | A tua vida como enredo | The School of Life, «How to Narrate Your Life Story» (5:08) | Tom de autoajuda; troca de nomes se partir da vida real |
| Lab, Começar pelo meio | Ulisses também começa a meio | Joseph Campbell Foundation, «The Homeric Legends: The Journey of Odysseus» (3:40) | Conteúdo |
| Lab, O cenário como personagem | O lugar vazio | aesthetics explained, «liminal space aesthetics explained in 7 minutes» (7:23) | Algumas imagens podem ter um tom de terror ligeiro |
| Lab, A personagem | Falhado ou herói trágico? | The School of Life, «Losers and Tragic Heroes» (4:17) | Pode falar de morte ou ruína |
| Lab, A pirâmide de Freytag | Provas: Freytag e Campbell | Joseph Campbell Foundation, «Initiation Through Trials» (4:00) | Imagem e legendas (carregado há 16 anos) |

Os textos dos cartões só afirmam o que está verificado: o título, o canal, a duração e factos das obras (a *Odisseia*, a *República*, Burke, Nagel). O resto são perguntas.

## Mudanças de destino em relação à lista de curadoria

- **«Waiting for Godot»** passa de «Linhas de enredo» para «A fábula em pedaços», a oficina que já cita *À Espera de Godot*.
- **«How to Narrate Your Life Story»** passa para «História e enredo»: os mesmos factos com outro enredo.
- **«The Journey of Odysseus»** e **«The Hero's Journey»** saem de «A rapsódia épica», que trata o teatro épico (distanciação) e não a epopeia. O primeiro vai para «Começar pelo meio»: a *Odisseia* abre a meio, como *Os Lusíadas*. O segundo vai para a sidequest «O herói».
- **«Consequentialism»**, **«Deontology»** e **«Virtue Ethics»** juntam-se na Ética, como as três perguntas de bolso. A lição do elétrico já tem dez excertos de Sandel.
- **«Moral Intuition»** passa da Ética para «O júri», onde se decide em silêncio cinco vezes.
- **«Moral Luck»** vai para a lição de Nagel: o ensaio sobre a sorte moral está no mesmo livro, *Mortal Questions* (1979).
- **«Plato and Poetry»** vai para a sidequest «A caverna»: também é a *República*.
- **«Check Yourself with Lateral Reading»** vai para «Verificação lateral», o passo 8 de «Como se investiga».

## O que ainda não entrou (10)

- **Cidadania M1, sessões novas** (estão só no PR #60). Entram num PR por cima dele:
  - «What Is Justice?», CrashCourse Philosophy #40;
  - «Ethical Decision Making», no passo «Uma posição com fundamento»;
  - «Deontology», sessão 06;
  - «What would a society without ethics look like?», sessão 07;
  - «How to Have Moral Courage & Moral Imagination?», sessão 08.
- **Português**, num PR no pt:
  - «What is Literature for?», M1;
  - «Plato's Symposium», M3, com excerto a marcar;
  - «Edward Hopper», M6;
  - «Arguments Against Personal Identity», M7.
- **Para desenvolver quando se proporcionar:**
  - «Fitter Happier», para a exploração de *OK Computer*;
  - «Not Waving But Drowning», com a tradução do docente.
