# Vídeos escolhidos, ronda 1 (28/10/2026)

Na página de curadoria, o docente disse «Sim» a 33 dos 105 vídeos da primeira lista. Este documento diz onde ficou cada um, o que saiu por estar fora de contexto e o que ainda não entrou.

## A regra: vídeos fora de contexto saem

Decisão do docente (28/10): um vídeo que pareça fora de contexto sai, esteja ou não em inglês.

Um vídeo só fica se cumprir as três condições:
1. trata diretamente do texto, do autor, da obra ou do conceito que o cartão ou a página ensina;
2. um aluno percebe logo porque está ali, sem uma ponte explicativa nossa;
3. acrescenta algo que o cartão não dá.

Sai quando:
- a ligação depende de uma ponte que só nós fazemos;
- é uma explicação genérica (filosofia, psicologia, autoajuda) encostada a outro assunto;
- o tema é vizinho, mas não o mesmo;
- é longo e acessório para aquele ponto.

Cada colocação foi lida por três júris independentes, que abriram o cartão e os cartões à volta:
- um aluno de 16 anos de um curso profissional;
- um docente;
- um curador de conteúdos educativos.

Sai o que a maioria considerou fora de contexto. Quando os júris se dividiram, decidiu um editor-chefe com a mesma regra.

## Como funciona

- Cada vídeo entra num cartão de leitura «Para ver», no próprio baralho. O cartão tem:
  - o porquê daquele vídeo naquele sítio;
  - uma pergunta antes de ver;
  - o leitor;
  - uma pergunta depois de ver, para responder em papel ou em voz alta;
  - uma nota curta (língua, legendas).
- O leitor só carrega quando o aluno toca em «Ver o vídeo». Usa o modo de privacidade reforçada do YouTube (youtube-nocookie), com as legendas ligadas. Ao lado, há uma ligação «Ver no YouTube».
- Um vídeo que deixa de estar à vista (porque o cartão ou o passo mudou) para de tocar.
- No máximo dois cartões «Para ver» por baralho.
- Os cartões de leitura não contam para a pontuação, e o motor só guarda tentativas e melhores resultados. O progresso já guardado nos aparelhos não muda.
- Ficheiros:
  - componente: `assets/para-ver.css` e `assets/para-ver.js`;
  - dados: `tools/videos-escolhidos.json`;
  - aplicação: `python3 tools/videos_escolhidos.py`. O script é idempotente e não reescreve os outros cartões. Se um gerador refizer uma destas páginas, basta voltar a correr o script;
  - teste: `tests/test_videos_escolhidos.py`.

## Ficam (5 cartões, 7 vídeos)

| Página | Cartão | Vídeo | Confirmar antes da aula |
| --- | --- | --- | --- |
| Ética | Lei, moral e ética | The Ethics Centre, «What is the difference between Ethics, Morality and the Law?» (5:14) | Legendas; exemplos de contexto australiano |
| Ética | Uma pergunta, um vídeo | The Ethics Centre: «Consequentialism» (4:03), «Deontology» (3:10), «Virtue Ethics» (3:19) | Exemplos de cada vídeo |
| Sidequest «O herói» | Ouvir a fonte | Joseph Campbell Foundation, «The Hero with a Thousand Faces» (3:12) | Se é leitura do livro ou entrevista |
| Cidadania M2, passo 0 | Arte ou design? | CrashCourse, «What's the Difference Between Art & Design?» (11:29) | Conteúdo |
| Como se investiga, passo 8 | Ler para os lados | CrashCourse, «Check Yourself with Lateral Reading», Navigating Digital Information #3 (13:52) | Apoios declarados no fim do vídeo |

Nas páginas que prometem «sem escrita», as perguntas pedem resposta em voz alta.

## Saíram por estar fora de contexto (16 cartões neste PR)

| Onde estava | Vídeo | Júris | Porquê |
| --- | --- | --- | --- |
| Estética, «O que é arte?» | CrashCourse, «Aesthetics» | 2 a 1, editor-chefe: sai | A página trabalha gosto e juízo e descrever antes de julgar; o episódio trata de outra pergunta e tem 10 minutos |
| Estética, «O sublime» | The School of Life, «Burke on: The Sublime» | 0 a 3 | A página só nomeia o sublime de passagem; o vídeo vinha colado a Munari e ao design |
| Cidadania M1, O júri | The Ethics Centre, «Moral Intuition & Ethical Judgement» | 0 a 3 | O ato ensina a separar facto de inferência; intuição moral é outro conceito |
| Cidadania M1, O júri | The Ethics Centre, «What is Unconscious Bias?» | 0 a 3 | O erro do caso é tomar uma captura cortada como prova, não um preconceito; o vídeo cortava o momento mais forte |
| Ter juízo, lição de Nagel | CrashCourse, «Moral Luck» | 0 a 3 | A lição é sobre o morcego; a sorte moral é outro ensaio, só partilha o autor |
| Sidequest «A caverna» | Michael Sugrue, «Plato and Poetry» (46:43) | 0 a 3 | A sidequest é o livro VII; a aula é sobre o livro X e é longa |
| Sidequest «O herói» | CrashCourse, «The Hero's Journey and the Monomyth» | 1 a 2, editor-chefe: sai | Terceira apresentação da mesma fórmula, depois do TED-Ed e do excerto de Campbell |
| Cidadania M2, O contexto em falta | CrashCourse, «Evaluating Photos & Videos» | 1 a 2, editor-chefe: sai | O passo ensina a rever uma decisão de moderação; o vídeo ensina o utilizador a verificar imagens |
| Cidadania M2, O rasto da afirmação | The Ethics Centre, fontes para votar | 0 a 3 | Contexto eleitoral australiano; a ligação à independência das fontes era nossa |
| Como se investiga, passo 6 | Carl Sagan, sobre a existência de Deus | 0 a 3 | O passo ensina evidência com Darwin; crença e prova é um tema vizinho |
| Lab, A fábula em pedaços | Philosophy Tube, «Waiting for Godot» | 0 a 3 | A oficina ensina a desmontar um texto; o vídeo lê a peça pela filosofia do absurdo |
| Lab, História e enredo | The School of Life, «How to Narrate Your Life Story» | 0 a 3 | Autoajuda encostada à distinção de Forster |
| Lab, Começar pelo meio | Joseph Campbell Foundation, «The Journey of Odysseus» | 0 a 3 | O excerto lê a viagem como mito, não fala do começo a meio |
| Lab, O cenário como personagem | aesthetics explained, espaços liminares | 0 a 3 | Estética da internet; a ponte com Cesário era nossa |
| Lab, A personagem | The School of Life, «Losers and Tragic Heroes» | 0 a 3 | A aula ensina o ofício da personagem; o vídeo é sobre como julgamos quem falha |
| Lab, A pirâmide de Freytag | Joseph Campbell Foundation, «Initiation Through Trials» | 0 a 3 | O excerto trata de rituais de iniciação pela dor, sem relação com Freytag nem com a farsa |

As escolhas do docente que saíram ficam registadas aqui. Podem voltar se aparecer uma página em que o vídeo trate diretamente do que se ensina.

## Noutros PR

- **Cidadania M1, sessões 06 a 08** (PR #62):
  - ficam «Deontology» e «Ethical Decision Making» (sessão 06, Leva) e «What Is Justice?» (sessão 07, Leva);
  - saem «What would a society without ethics look like?» (sessão 07, Vê) e «How to Have Moral Courage & Moral Imagination?» (sessão 08).
- **Português** (PR no pt): fica o soneto de Sá de Miranda dito em voz alta (M3-F17). Saem:
  - «What is Literature for?»;
  - «Plato's Symposium»;
  - o soneto de António Nobre;
  - «Edward Hopper»;
  - «Arguments Against Personal Identity».

## Para desenvolver quando se proporcionar

- «Fitter Happier», para a exploração de *OK Computer*.
- «Not Waving But Drowning», com a tradução do docente.
