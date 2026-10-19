# Acesso à projeção em todas as páginas de conteúdo

Baseline: `60afb448885157b511d5eef678b587e0dbe38a1f`. Cobertura: 270 páginas de conteúdo em 272 HTML. Excluídos apenas redirecionamentos, a própria vista de projeção e o erro 404.

Cada página carrega um único launcher partilhado, com versão na ligação para evitar a reutilização da versão anterior em cache. Nas atividades fica na barra superior e no menu; nas apresentações entra na própria barra, sem ficar atrás do ecrã fixo. Nas páginas editoriais usa a navegação/cabeçalho. Em impressão fica oculto; dentro da projeção não se duplica. Aberturas dinâmicas de exercícios reposicionam o acesso fora da área de atividade.

Verificação integral por comparação de bytes: nenhuma alteração fora da inserção/versão do launcher nas páginas. Corpos dos scripts existentes, links e IDs preservados em todas as 270 páginas. Conteúdos e motores não foram modificados. Sintaxe do launcher verificada.

Os testes funcionais representativos e as pendências são registados no relatório de entrega desta correção. Não se afirma que todas as atividades foram reexecutadas: esta alteração modifica apenas o acesso à projeção.

## Testes funcionais executados

- M3-F18: avanço de cartões, seleção, confirmação e feedback correto (+10 pontos); menu → projeção; nenhuma entrada recursiva no iframe.
- LENTE Cidade/m02: botão da barra → projeção da missão correta.
- Fontana: menu com uma única entrada de projeção. A 322 px, o botão adicional da barra fica recolhido no menu e o botão Menu termina dentro do ecrã (316,3 px); evita cortar controlos existentes.
- Biblioteca/1984: acesso editorial → projeção do recurso correto.
- Diapositivos M1: acesso visível e clicável na navegação, sem a sobreposição da barra original; entrada por teclado confirmada. Dentro da projeção, passar do diapositivo18 para17 atualiza a ligação/QR para #17, mesmo quando a página usa history.replaceState.
- Atlas: o acesso passa para a barra da missão ao abrir e regressa às migalhas ao fechar; permanece um único acesso principal.
- Painéis de aula: os93 painéis ativos mantêm o botão, handler, QR e atalho F originais, sem transformar a sala ativa numa nova página. Não foi criada uma sala nem certificado o funcionamento da sessão em rede. Se um painel for aberto manualmente no projetor genérico, a ligação/QR do aluno aponta para a lição correspondente, em vez do painel docente; todos esses destinos existem no inventário.
- Sintaxe dos dois scripts aprovada. Verificação de preservação efetuada sobre todos os HTML de conteúdo.

## Pendências

Não foram reexecutadas todas as atividades dos dois sites; os motores e os respetivos scripts não mudaram. Leitor de ecrã real, Safari/iOS, impressão física, sala multiutilizador e desempenho formal não executados. Não se declara equivalência com esses testes.

## Organização do incremento

As inclusões nos HTML são repetidas por necessidade: estes sites servem páginas estáticas, sem um cabeçalho global aplicado pelo servidor. A lógica e os estilos do acesso ficam num único recurso partilhado por site. Os redirecionamentos, o404 e o próprio portal não recebem um segundo acesso. A versão na ligação evita reutilizar o launcher anterior em cache.
