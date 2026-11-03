# Laboratório: piloto dos menus

03/11/2026. Base de trabalho: `2db238f82b41e057e822fbca36f1752dea4f952b`, cabeça do #106 entregue para revisão incremental. Este ramo é separado; não altera as cabeças do #106 ou do #107. Não depende dos cinco tipos externos de cartões.

## Alterações

| Local | Antes | Piloto |
| --- | --- | --- |
| Barra das quatro entradas | Todas as portas na barra | Mesmos destinos, com Observar, Treinar e Criar agrupados em «Percursos» |
| Entrada do Laboratório | Blocos com cabeçalhos, imagens e listas extensas | Uma linha por bloco; imagem, crédito, contexto e percursos abrem por pedido |
| Ideias na entrada | Três ações com o mesmo tratamento | «Abrir Ideias» como ação principal; ligações diretas às sessões numa abertura secundária |
| Observar, Treinar e Criar | Continuação escondida, imagem e percursos expostos | Continuação visível a partir do progresso real; imagem e percursos em aberturas independentes |
| Registos | Exportação e reposição sempre na página | Mesmos controlos e formato, em «O teu progresso e os teus registos» |
| Tratamento visual | Fundos e caixas repetidos | Linhas, espaço entre grupos, fontes e cores existentes; pequeno sinal retro nos títulos principais |

Os títulos Humanos, Algoritmos e Decisões pertencem à entrega #107. Estas quatro entradas não contêm rótulos desses módulos; não se duplica aqui a renomeação. A integração posterior das entregas deve conservar os títulos aprovados.

## Preservação

Comparação das quatro páginas com a base: nenhum `href` ou `id` desapareceu. O JSON `lab-dados` é idêntico, incluindo URLs, identificadores e chaves de progresso. Não se alteram exercícios, fontes de imagens, créditos, ordem dos percursos ou dados privados. Os 92 itens dos percursos e as 93 peças do catálogo mantêm-se.

A abertura automática da peça comum foi excluída apenas nas páginas marcadas `data-menu-piloto`. As restantes famílias conservam o comportamento anterior. Sem JavaScript, os percursos conservam-se abertos; o script fecha-os por omissão e preserva a abertura do destino indicado no endereço. Na impressão, as aberturas do piloto expandem-se e depois recuperam o estado anterior. O menu da barra fecha com Escape e devolve o foco ao seu resumo. O movimento reduzido mantém todas as ações.

## Verificações

- Cinco testes Python dos percursos: aprovados, incluindo regeneração idempotente e ligações.
- Sete testes Node das peças comuns e da preservação das quatro barras: aprovados.
- Navegador dos percursos: 320, 390, 1366 e 1440 px; estados reais, projeção, imagens, exportação e reposição, conservação de um registo criado noutro separador, rejeição de ficheiro inválido e 23 páginas sem deslocamento lateral.
- Hierarquia R1 a R5 e escala do sítio: aprovada nas quatro entradas, na entrada geral e na demonstração, em claro/escuro, normal/projeção, secções abertas/fechadas.
- Comparação visual: 72 contextos anteriores e 72 do piloto, nas quatro entradas, 320/390/1366 px, claro/escuro/projeção e ampliação de 100%/200%. A ronda final do piloto exige largura sem deslocamento lateral também com todos os detalhes abertos, teclado, foco visível, destinos e armazenamento intacto. Ronda final aprovada nos 72 contextos.
- Regressão da família visual: o teste integral para no limite de 3000 px da entrada geral do Lente. A medição é 3012 px, em claro e escuro, tanto na base como no piloto, antes e depois de esperar pelas fontes. Essa página não muda neste ramo; não se relaxou o limite. O diagnóstico específico das quatro páginas alteradas passou: larguras e temas, projeção, impressão, alternativa sem JavaScript, progresso e destinos com fragmento. A última ronda confirmou separadamente os contratos sem JavaScript e de progresso após o acerto da alternativa estática. A bateria integral não é declarada aprovada.

O zoom de 200% destes ensaios usa CSS. Não é uma prova de acionamento do zoom nativo pela barra do navegador. Não se apresenta como tal.

Provas locais, fora do repositório: `outputs/laboratorio-menus-provas-20261102/comparacao.html`, com seletor de página, largura, modo e ampliação; pastas `antes/` e `depois/` com capturas e medições. A prova dos registos está em `outputs/laboratorio-menus-progresso-20261103/`.

## Contratos atualizados

A barra continua a ser comparada integralmente com a base: o teste acrescenta exatamente a abertura «Percursos» à estrutura esperada, mantendo todas as ligações. O ensaio de registos abre a nova secção por teclado antes de descarregar o mesmo ficheiro e conserva as verificações de conteúdo e privacidade.

O teste da família visual exige agora, no piloto, secções inicialmente fechadas e abertura/fecho por Enter e Espaço em todas as larguras e na projeção. Fora do piloto, mantém a exigência anterior de abertura automática. Conservam-se os alvos de 88 px, os limites da legenda, a escala tipográfica e o mínimo de leitura na projeção; não foram alargadas tolerâncias para aceitar cortes.

Entrega apenas para revisão. O #106 tem CI verde na base indicada; o piloto precisa da sua própria revisão e CI. Não há autorização de publicação inferida destes resultados.
