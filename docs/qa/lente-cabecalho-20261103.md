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
