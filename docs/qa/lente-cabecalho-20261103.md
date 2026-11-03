# Lente: lupa integrada no cabeçalho

03/11/2026. Base: piloto dos menus #108, `927df96b9f1ff688c52d4425f392489b5f007c40`. Entrega separada, para revisão.

## Alteração

A lupa e a página de texto existentes passam a ocupar o fundo da abertura, em vez de uma faixa opaca abaixo do subtítulo. Uma máscara esbate os bordos e atenua o desenho sob a área de leitura; a zona livre conserva a lupa reconhecível. O título e o subtítulo têm mais espaço entre si, ficam acima da ilustração e não se movem. O ponto de cor do título e a virola da lupa conservam o acento retro.

O título adapta-se à largura disponível em ampliação. Conservam-se o texto, a epígrafe, a atribuição do grafismo ao recurso a IA, a fonte de Saramago, os destinos e todos os scripts. Não se altera o motor comum, o ritmo de 40 segundos, a relação matemática entre a lupa e a ampliação, nem as chaves de progresso.

Laboratório e Ideias foram avaliados: mantêm as entradas breves, a ação principal e os motivos já presentes. Não se lhes acrescenta animação nesta entrega. Os motivos próprios de Cidadania ficam num piloto posterior, separado. A renomeação Humanos/Algoritmos/Decisões pertence ao #107; os rótulos antigos presentes na base das capturas não são uma reversão dessa entrega.

## Provas

- Três testes existentes de `cartaz_entrada.test.cjs` aprovados: destinos/scripts, leitura do progresso sem escrita, grafismo e contas da ampliação. No Windows, o ensaio foi executado encaminhando apenas a chamada `python3` para o Python disponível; as asserções não mudaram. O SVG também foi verificado diretamente pelo gerador.
- Teste integral `browser_cartaz_familia.cjs` aprovado: temas, larguras, alvos, abertura por teclado, projeção, impressão, alternativa sem JavaScript, progresso e tipos de letra. Nenhum limiar foi alterado. A integração do desenho reduz a altura da entrada.
- Comparação antes/depois nas larguras 320, 390 e 1366 px, em claro, escuro e projeção: 18 capturas integrais, sem transbordo a 100%. O ensaio de capturas respeita movimento reduzido e espera pelas fontes.
- Vídeo real de navegador: movimento, pausa por Enter, retoma por Enter e passagem dinâmica à projeção. As asserções confirmam mudança de transformação durante o movimento e ausência de animação após a pausa e na projeção.
- Ampliação de 200% por CSS: o título proposto cabe, mas permanecem transbordos anteriores noutros elementos da página. Não se declara a página inteira aprovada a 200%, nem se apresenta esta simulação como zoom nativo do navegador. As capturas e medidas antes/depois permitem comparar a limitação.

Provas locais: `outputs/lente-cabecalho-provas-20261103/comparacao.html`, imagens antes/depois e `movimento-pausa.webm`. Ensaio local: `outputs/lente-cabecalho-browser.cjs`; ampliação: `outputs/lente-cabecalho-zoom.cjs`.

A entrega aguarda revisão visual, confirmação dos limites e CI. Não autoriza publicação.


## L107-02: moldura real de projeção

03/11/2026. Reproduzidos 338 px para janela de 320 px no tamanho médio, e 426 px no tamanho grande. Na cabeça anterior deste pedido, a caixa da lupa ocupava exatamente 0–320 px e a epígrafe 16–304 px. A medição de todos os elementos identificou o excesso documental no título «Ferramentas»; o tamanho grande revelou ainda créditos sem quebra, títulos de grupos e rótulos. A imagem decorativa conserva a máscara original; não se acrescenta ocultação para fazer caber texto.

Correção em cartaz-entrada.css, limitada a html.epi-projection: texto recompõe-se à largura disponível, créditos podem quebrar linha, números dos percursos usam a largura do conteúdo e a porta Português passa a uma coluna em ecrãs estreitos. Não se reduz a escala de texto nem se esconde excesso. Cache da folha atualizada.

Regressão nova tests/browser_lente_projecao_entrada.cjs, incluída no CI: moldura /projetar/ com iframe real, 320/390/1366 px, claro/escuro, pequeno/médio/grande, 18 contextos. Todos aprovados: largura documental igual à janela, caixas da lupa/título/frase/epígrafe dentro dos limites, nenhum conteúdo textual ou controlo com excesso na sua caixa. O fundo decorativo sangra para a margem do cabeçalho, mantendo ambas as caixas dentro da janela; não se confunde esse fundo ampliado com texto interativo. Capturas de 320 px nos dois temas abertas e conferidas, com QR recolhido.

Provas: outputs/lente-cabecalho-projecao-final-20261103/medidas.json e capturas. Isto verifica a projeção real, não substitui a verificação pendente de zoom nativo. Sem publicação.

O teste integral existente browser_cartaz_familia.cjs também passou após esta correção: temas, alvos, dobras, projeção, impressão, alternativa sem JavaScript e progresso. Nenhuma asserção ou limite existente foi alterado.


## Integração do main publicado, 03/11/2026

Merge `a54b702e2dc949c8f3713165d3035426a7969b04`, com main `bbdbec4705477c43ccdff1a93e399bdade2e3a8f` como segundo pai. Preserva os commits anteriores. Os conflitos de Ideias, pilotos de Cidadania e contratos ficaram exatamente como no main publicado. Os menus herdados do antigo ramo-base #108 foram separados desta entrega; os pedidos #108, #110 e #111 não mudaram.

Diferença delimitada contra main: os seis ficheiros próprios do cabeçalho/projeção e o manifesto técnico de comparação. No index.html só mudam duas versões de cache das folhas de estilo. O manifesto acrescenta apenas essas duas substituições literais, uma ocorrência cada, mantendo a comparação integral dos 124 ficheiros e todas as asserções. Nenhum teste é removido nem passa a ignorar diferenças arbitrárias de cache.

Dois testes de preservação/comparação exata aprovados após o merge. Dezoito contextos de projeção real aprovados novamente, sobre o main com Humanos, Algoritmos e Decisões. Prova atual: outputs/lente109-main-projecao-20261103/medidas.json. A bateria visual existente é repetida porque a separação dos menus mudou a base efetiva do ensaio.

A revisão automática recusou uma reposição global durante a resolução. Foi adotada resolução delimitada a 35 caminhos, depois de salvaguardar os 41 caminhos divergentes e o índice em outputs/lente109-merge-salvaguarda-20261103.zip. Nenhum trabalho não guardado se perdeu. A cópia de segurança fica fora do repositório.

Resultado após o merge: browser_cartaz_familia.cjs aprovado, incluindo temas, alvos, dobras, projeção, impressão, alternativa sem JavaScript e progresso.


## Correção da falha CI depois da publicação do #107

Job 125865947739, cabeça 216f7f66: uma falha em 273 testes Python. test_m1_igual_a_origin_main chamava renomear com base_ja_renomeada=True; a asserção exigia que todas as ocorrências de «Humanos» fossem títulos renomeados. No exercício «O júri», «Direitos Humanos» já aparecia no conteúdo da base anterior.

O auxiliar passa a calcular a contagem final a partir do commit imutável 349d2457e1f056b69c6dda550aace2a6f5377051, aplicando o manifesto fechado e conferindo primeiro cada contagem antiga. Exige a contagem final exata, incluindo os usos anteriores. A comparação binária integral com a base continua intacta. Nenhuma página, CSS, script público ou limite de preservação muda neste incremento.

Regressão adicional: compara a base antiga e a publicação bbdbec47, em bytes e texto; demonstra que «Direitos Humanos» permanece e que contagens em falta ou a mais são rejeitadas. Dois testes novos aprovados; 26 testes de Cidadania M2, incluindo a asserção falhada, aprovados. A alteração foi preparada em outputs/lente109-ci-20261103, mantendo intacta a árvore original enquanto decorria o ensaio independente de movimento.

Os dois testes de preservação/comparação exata também passaram. Total desta verificação local: 30 testes aprovados. CI integral da nova cabeça pendente.
