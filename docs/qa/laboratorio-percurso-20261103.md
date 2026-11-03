# Ideias como entrada do Laboratório

Protótipo navegável para revisão, separado do #107 e dos pilotos de fundos. Página: `demonstracoes/laboratorio-percurso/index.html`. Não está ligada à navegação pública e tem noindex. Não altera URLs nem consulta ou escreve progresso. A barra de revisão seleciona estados simulados; o excerto não declara uma sessão completa realizada.

## Percurso concreto

1. Laboratório: uma ação principal, «Entrar em Ideias», seguida de recursos escolhidos pela necessidade atual. Na retoma, o texto lembra a pergunta deixada em aberto; na conclusão, propõe voltar ao material recolhido.
2. Ideias: o próximo passo distingue começo, retoma e conclusão. O método conserva os cinco passos de Young, com os nomes e a ordem publicados. As quatro portas dos recursos não são uma nova sequência pedagógica.
3. «Ver ou observar?»: um excerto da sessão 1 existente. A escolha produz uma explicação ou convida a reler o texto. Sem pontos, prémios ou respostas decorativas.
4. Recurso: reler a conversa de Watson e Holmes. O botão principal devolve à pergunta, conservando em memória a opção escolhida. Uma ligação secundária abre o recurso completo publicado num novo separador, identificado no rótulo.
5. Regresso: a escolha fica visível e pode ser revista. O fecho retoma a escada e o caderno da sessão publicada. A ação seguinte prepara «O cocheiro»; explorar outro recurso continua disponível.

## Hierarquia e recursos

| Porta | Necessidade | Destino existente |
| --- | --- | --- |
| Observar | Distinguir o que se vê do que se conclui | `narrativas/ver/` |
| Experimentar | Pôr uma escolha à prova | `narrativas/treinar/` |
| Relacionar | Ligar o material observado | `narrativas/ideias/sessao-02/` |
| Dar forma | Apresentar e pôr à prova | `narrativas/criar/` |

O menu Explorar é secundário. A posição no percurso fica no topo; o regresso aparece junto do recurso. As ligações para páginas publicadas permanecem intactas. A demonstração serve para aprovar o percurso antes de ligar estes estados ao motor real, que continua a ser o único responsável pelo progresso.

## Movimento

Duas notas e uma ligação representam juntar e relacionar material. Só a linha se move, lentamente; título e texto mantêm a posição. Usa o motor comum `assets/fundos.js`, com pausa, limite de dois ciclos, suspensão fora de vista e com separador oculto, movimento reduzido e projeção estática. O desenho é código SVG do protótipo, sem imagem externa nem nova fonte. Sem JavaScript há ligações diretas para Ideias e para a sessão publicada.

## Fontes e limites

O gerador `tools/laboratorio_percurso_demo.py` extrai a leitura e a pergunta de Watson do banco público existente. Não foram necessárias novas pesquisas do GPT2. A explicação para tentar novamente é uma orientação de leitura, sem acrescentar uma afirmação histórica. Os estados não persistem ao recarregar. A sessão integral, os sete percursos futuros e os cinco tipos de interação pendentes não são implementados por este protótipo.

Não houve controlo interativo. Zoom real a 200% continua fora da validação. Não publicar nem propagar antes do parecer sobre o percurso.

## Validação da entrega

27 percursos aprovados: três estados, 320/390/1366 px, claro/escuro/projeção, com seis vistas por contexto. Regresso à opção escolhida e armazenamento intacto. Mais seis contextos conferem boia sem sobreposição, Enter/Escape/foco, sinais e tokens dos resultados, ligação única ao Wordle e zero pedidos externos. Pausa, retoma e projeção dinâmica aprovadas. Gerador sem diferenças. Capturas móveis da entrada e da porta Português abertas e conferidas. Provas locais em `outputs/laboratorio-percurso-provas-20261103/`. A especificação comum foi enviada ao GPT3 após autorização direta do docente.
