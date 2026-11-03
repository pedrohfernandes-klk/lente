# Menus do Lente: acabamento visual

03/11/2026. Camada isolada sobre o #112, cabeça 39b391f7969e9a99f04d9b16f715ea0e4bd183ea, que já inclui o #108. Não altera sessões, motores, arquitetura ou bancos. Sem publicação.

## Inventário e intervenção

| Entrada | Endereço | Causa observada na estrutura |
| --- | --- | --- |
| Lente e Ferramentas | https://pedrohfernandes-klk.github.io/lente/#ferramentas | Duas portas com ações secundárias concorrentes; grupos de ferramentas com numeração decorativa. |
| Laboratório | https://pedrohfernandes-klk.github.io/lente/narrativas/ | Recursos, catálogo e exploração têm pouco contraste entre níveis. |
| Ideias | https://pedrohfernandes-klk.github.io/lente/narrativas/ideias/ | Ação principal e saídas de apoio precisam de ritmo e foco comuns. |
| Observar | https://pedrohfernandes-klk.github.io/lente/narrativas/ver/ | Linhas e aberturas com pouco espaço entre grupos. |
| Treinar | https://pedrohfernandes-klk.github.io/lente/narrativas/treinar/ | Linhas e aberturas com pouco espaço entre grupos. |
| Criar | https://pedrohfernandes-klk.github.io/lente/narrativas/criar/ | Linhas e aberturas com pouco espaço entre grupos. |
| Catálogo do Laboratório | https://pedrohfernandes-klk.github.io/lente/narrativas/tudo/ | Lista longa, ligações sublinhadas e grupos pouco diferenciados. |
| Cidadania | https://pedrohfernandes-klk.github.io/lente/cidadania/ | Módulos, recursos e referências precisam de separação visual consistente. |
| Mapa | https://pedrohfernandes-klk.github.io/lente/mapa/ | Árvore extensa com ligações de menu visualmente próximas de prosa. |
| Como se usa | https://pedrohfernandes-klk.github.io/lente/como/ | A saída de navegação tem o tratamento de ligação em prosa. |
| Apoio ao docente | https://pedrohfernandes-klk.github.io/lente/docente/ | Saídas dos percursos e ligações de apoio pouco distintas do texto. |
| Apoio a Ideias | https://pedrohfernandes-klk.github.io/lente/narrativas/ideias/docente/ | Saídas de apoio sem o mesmo tratamento do índice. |

| Como se lê | https://pedrohfernandes-klk.github.io/lente/ler/ | Apoios do rodapé partilhavam linhas e competiam com a continuação. |
| Como se apresenta | https://pedrohfernandes-klk.github.io/lente/apresentar/ | Apoios do rodapé sem alinhamento comum nem alvo inteiro. |

## Proposta

Ideias conserva a ação principal do Laboratório. As ações de entrada ganham fundo sólido; as saídas secundárias ficam em linhas discretas. Observar, Treinar e Criar formam um grupo de recursos. Ferramentas perde apenas os números decorativos, já escondidos da leitura assistida. Os módulos conservam os nomes, descrições e estados.

O catálogo mantém a ordem de leitura e todos os destinos: duas colunas no ecrã largo e uma no telemóvel, com títulos de grupo próximos das suas linhas. As linhas de navegação têm alvo inteiro, mínimo de 48 px e um pequeno sinal de direção. Os grupos usam espaço e separadores leves em vez de caixas sobrepostas. Foco de teclado, passagem do ponteiro e aberturas usam o mesmo tratamento. As cores derivam das cores existentes do tema.

As ligações dentro da prosa e os créditos conservam o tratamento anterior. No mapa, Ideias é a ação principal do Laboratório e os seis apoios finais ficam dentro de «Outros recursos do Laboratório». Este é o único rótulo novo; os nomes e textos anteriores conservam-se. Não se alteram os cabeçalhos, grafismos ou a sua altura, reservados ao GPT3.

## Preservação e provas

O gerador acrescenta apenas uma marca no body e a ligação à folha de estilos, nas catorze páginas do manifesto. No mapa acrescenta também o agrupamento dos seis apoios e a classe da ação principal. O teste reverte explicitamente cada adição, exige uma ocorrência de cada uma e mantém igualdade byte a byte com a base: texto, ordem, destinos, identificadores, scripts e dados. A regeneração é idempotente. Os geradores do Laboratório e de Ideias aplicam a camada, para não a retirar ao regenerar. Passaram os 282 testes Python. Os testes históricos continuam a comparar todo o conteúdo depois da transformação autorizada; o teste novo verifica a reversão independentemente.

Matriz de navegador: 320, 390 e 1366 px; claro, escuro e visor real de projeção em ambos os temas, com a classe epi-projection e a folha do visor carregadas. Capturas antes e depois; largura, alvos mínimos, foco, teclado e armazenamento. A entrada geral conserva as dobras abertas no ecrã largo e na projeção, como exige o script publicado; as outras aberturas continuam a responder ao teclado.

Ronda aprovada: 336 contextos, 168 antes e 168 depois, nas catorze páginas. Zero erros de JavaScript, sem deslocamento lateral na proposta, alvos de navegação com pelo menos 44 px, foco e teclado. A nova abertura do mapa conserva os seis destinos e responde a Enter. Passaram também 40 contextos separados: Começar/Continuar/Rever com registos reais, preservação do armazenamento, projeção e alternativa sem JavaScript. Provas locais: outputs/lente-menus-acabamento-provas-20261103/. A comparação usa a proposta #112 como antes, não afirma que essa proposta já esteja publicada.

A primeira ronda por parâmetro não certificava o visor em cinco páginas. A ronda final usa o visor real. Este revelou uma regra de grelha específica da projeção que conservava três colunas depois de retirar a numeração decorativa; corrigiu-se a grelha dos módulos, sem alterar o cabeçalho nem reduzir o texto.

## Retoma e limites

Checkout: outputs/lente-menus-acabamento-20261103. Ramo: codex/menus-acabamento-20261103. A integração deve aguardar revisão da cabeça exata, verificações automáticas e vez de publicação. A autorização comunicada para este âmbito não substitui a revisão dos pré-requisitos #108 e #112. #115, sessões e outros lotes não fazem parte desta camada.

## Acerto pontual do visor

A pedido do docente, transmitido pela coordenação, projetar/index.html muda apenas «Abrir fora da projeção ↗» para «Sair da projeção». O destino e o comportamento existentes mantêm-se; não se alteram scripts, estilos, identificadores ou arquitetura do visor. Esta substituição foi recebida no checkout e incluída na entrega.

## Ampliação real e contraste

A prova adicional da cabeça e96a8aa passou 112 contextos com ampliação nativa do Chrome a 200 %, nas catorze páginas, nos dois temas e no visor real. A calibração confirmou o dobro da densidade de píxeis e metade da largura útil, sem CSS zoom. Não houve deslocamento lateral nem alvos abaixo de 44 px. O painel QR foi fechado pelo respetivo botão.

A prova de contraste revelou dois defeitos nesta camada: o foco branco da ação principal desaparecia no fundo claro; no mapa, o hover clareava o fundo da entrada de Ideias sem mudar o texto branco. As correções limitam-se ao contorno exterior e ao estado hover desses elementos. O teste novo mede texto com mínimo de 4,5:1 e contorno com mínimo de 3:1, nos estados normal, hover e foco, nos dois temas. Integra as verificações automáticas, sem exceções nem redução dos mínimos.

Ronda final de contraste aprovada: 1350 medições, catorze páginas em cada tema. Contraste mínimo do texto: 5.36:1; do contorno de foco: 14.15:1. Os dois testes de preservação e regeneração passaram novamente.
