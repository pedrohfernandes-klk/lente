# Cidadania: Humanos, Algoritmos e Decisões

## Integração de 03/11/2026

### Correção L107-01

Os quatro trabalhos de CI falhados na cabeça a882dfd8 partilhavam três causas: comparação do M1 com a base sem renomeação; comparação dos 86 motores antigos que não reconhecia os dois rótulos de Anguissola/Cigoli; hash histórico de Justiça calculado depois de renomear a navegação. Os testes passam agora pelo mesmo manifesto fechado, com contagens exatas por ficheiro. Na Justiça desfazem-se apenas os rótulos antes de verificar o hash original, que permanece intacto. Não mudam páginas, motores, opções, contagens, lista de exceções de leitura ou limites de testes.

Sete testes de contratos, dez de Justiça e 26 de Cidadania M2 conferidos; a comparação binária do M1 foi repetida com os dois assets locais repostos nos bytes LF do Git. As cinco verificações de regeneração do CI passaram: Justiça, lições, Ideias piloto, Ideias público e opções. O achado visual L107-02 fica no cabeçalho #109, fora deste incremento.

A correção técnica das fontes foi entregue separadamente em fontes #17, cabeça d97d0eec7da7976ecc6c64c37003d49002d6a54b. Resolve CRLF e Python no Windows, mas a comparação do modelo antigo com o sítio atual continua a mostrar divergências, explicitadas nesse pedido. Não se copia essa saída sobre as páginas deste pedido.

Main publicado `349d2457e1f056b69c6dda550aace2a6f5377051` integrado por merge `86b61a5`. Os doze conflitos foram resolvidos conservando o main e reaplicando apenas os títulos autorizados. Menus, cabeçalho e fundos não entram nesta entrega.

Comparação exata de 124 ficheiros com esse main, segundo manifesto fechado em `tests/fixtures/cidadania-nomes-20261103.json`. O contrato anterior de preservação mantém a base fixa, a comparação binária e a única normalização de cache; reconhece agora os títulos por ficheiro e contagem. O teste adicional compara todo o texto dos 124 ficheiros com o main mais essas trocas. URLs, identificadores, progresso e usos literários não mudam. No Windows, os ficheiros de texto da cópia de ensaio foram repostos em LF para a comparação binária; os PDFs conservam os bytes do Git.

A pesquisa adicional encontrou uma referência no dossiê de Lu Xun: «Módulo 2: os algoritmos» passa a «Módulo 2: Algoritmos». A origem privada em `gigantes.json` recebe a mesma correção no fontes #16. As referências anteriores nas fontes e o bloqueio da regeneração privada mantêm-se documentados nesse pedido; nenhum conteúdo privado é copiado para o sítio.

Navegador automático sem janela: 45 contextos aprovados, cinco entradas em 320/390/1366 px, claro/escuro/projeção, títulos conferidos, sem transbordos nem erros JavaScript. Provas externas em `outputs/cidadania-nomes-provas-20261103/`. Sem controlo interativo e sem declaração de aprovação do zoom real.

02/11/2026. Renomeação separada do pedido #106. URLs, âncoras, identificadores e chaves de progresso preservados. Os usos comuns de «ser-se humano», títulos de obras, citações e os conteúdos de Justiça, Ética e Estética mantêm-se. Não se cria um módulo 3: Decisões é o nome da secção anteriormente chamada Ter juízo.

Verificações: onze testes Python existentes e treze testes de resultados aprovados. Vinte contextos no navegador: cinco entradas, 390/1366 px, claro/escuro, sem deslocamento lateral ou erros JavaScript; nomes conferidos. Capturas e medidas em outputs/cidadania-nomes-provas-20261102, fora do repositório.

Regenerados pelo gerador: dez lições do piloto, três páginas de apoio do piloto e dezoito fichas HTML. O gerador de Justiça confirmou as três lições e as 72 citações; os moldes receberam o novo rótulo. As restantes páginas conservam integralmente o publicado, com substituição exclusiva dos títulos inventariados abaixo. A comparação com a base aceita somente estas seis trocas textuais; não encontrou outra diferença.

As fontes privadas correspondentes foram atualizadas em ramo separado. A regeneração privada completa está bloqueada por uma falha já existente na base; não se copiava a sua saída parcial sobre estas páginas. O #106 permanece intacto; a comparação fixa de Cidadania nesse pedido terá de reconhecer esta renomeação, em alteração separada e revista, quando ambos se integrarem.

## Inventário antes e depois

| Ficheiro | Antes | Depois | Ocorrências |
| --- | --- | --- | ---: |
| `assets/progresso-registos.js` | Ter juízo | Decisões | 1 |
| `cidadania/25-de-abril/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/ferramentas/m1-aula-01-diapositivos/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/ferramentas/m1-aula-01-ficha/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/ferramentas/m2-aula-01-diapositivos/index.html` | Expressão: os algoritmos | Algoritmos | 2 |
| `cidadania/ferramentas/m2-aula-01-ficha/index.html` | Expressão: os algoritmos | Algoritmos | 1 |
| `cidadania/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/index.html` | Os algoritmos | Algoritmos | 1 |
| `cidadania/index.html` | Ter juízo | Decisões | 1 |
| `cidadania/m1/cid-m1-butler-singer/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/cid-m1-duas-legendas/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/cid-m1-guardar-ou-partilhar/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/cid-m1-o-juri/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/cid-m1-quem-tem-lugar/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/cid-m1-vida-em-direto-hoje/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/fichas/f01/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f01/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f02/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f02/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f03/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f03/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f04/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f04/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f05/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f05/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f06/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f06/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f07/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f07/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f08/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f08/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f09/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f09/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f10/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f10/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f11/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f11/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f12/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f12/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f13/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f13/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f14/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f14/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f15/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f15/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f16/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f16/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f17/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f17/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/fichas/f18/index.html` | Ser-se humano | Humanos | 1 |
| `cidadania/m1/fichas/f18/index.html` | SER-SE HUMANO | HUMANOS | 1 |
| `cidadania/m1/index.html` | Ser-se humano | Humanos | 2 |
| `cidadania/m1/passo-00/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/passo-01/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/passo-02/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/passo-03/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/passo-04/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/passo-05/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/passo-06/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/passo-07/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/passo-08/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/passo-09/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/passo-10/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m1/percurso-anterior.html` | Ser-se humano | Humanos | 2 |
| `cidadania/m1/sessoes/10/index.html` | Expressão: os algoritmos | Algoritmos | 1 |
| `cidadania/m1/verificar/index.html` | Ser-se humano | Humanos | 3 |
| `cidadania/m2/cid-m2-a-regra-do-feed/index.html` | Os algoritmos | Algoritmos | 3 |
| `cidadania/m2/cid-m2-dentro-da-caixa/index.html` | Os algoritmos | Algoritmos | 3 |
| `cidadania/m2/cid-m2-o-contexto-em-falta/index.html` | Os algoritmos | Algoritmos | 3 |
| `cidadania/m2/cid-m2-o-rasto-da-afirmacao/index.html` | Os algoritmos | Algoritmos | 3 |
| `cidadania/m2/cid-m2-preco-minuto/index.html` | Os algoritmos | Algoritmos | 3 |
| `cidadania/m2/index.html` | Expressão: os algoritmos | Algoritmos | 2 |
| `cidadania/m2/passo-00/index.html` | Os algoritmos | Algoritmos | 3 |
| `cidadania/m2/passo-01/index.html` | Os algoritmos | Algoritmos | 3 |
| `cidadania/m2/passo-02/index.html` | Os algoritmos | Algoritmos | 3 |
| `cidadania/m2/passo-03/index.html` | Os algoritmos | Algoritmos | 3 |
| `cidadania/m2/passo-04/index.html` | Os algoritmos | Algoritmos | 3 |
| `cidadania/m2/passo-05/index.html` | Os algoritmos | Algoritmos | 3 |
| `cidadania/m2/passo-06/index.html` | Os algoritmos | Algoritmos | 3 |
| `cidadania/m2/passo-07/index.html` | Os algoritmos | Algoritmos | 3 |
| `cidadania/m2/passo-08/index.html` | Os algoritmos | Algoritmos | 3 |
| `cidadania/piloto/m1-s01/index.html` | Ser-se humano | Humanos | 2 |
| `cidadania/piloto/m1-s02/index.html` | Ser-se humano | Humanos | 2 |
| `cidadania/piloto/m1-s03/index.html` | Ser-se humano | Humanos | 2 |
| `cidadania/piloto/m1-s04/index.html` | Ser-se humano | Humanos | 2 |
| `cidadania/piloto/m1-s05/index.html` | Ser-se humano | Humanos | 2 |
| `cidadania/piloto/m1-s06/index.html` | Ser-se humano | Humanos | 2 |
| `cidadania/piloto/m1-s07/index.html` | Ser-se humano | Humanos | 2 |
| `cidadania/piloto/m1-s08/index.html` | Ser-se humano | Humanos | 2 |
| `cidadania/piloto/m1-s09/index.html` | Ser-se humano | Humanos | 2 |
| `cidadania/piloto/m1-s10/index.html` | Ser-se humano | Humanos | 2 |
| `cidadania/piloto/m1/index.html` | Ser-se humano | Humanos | 2 |
| `docente/index.html` | Ser-se humano | Humanos | 1 |
| `estetica/index.html` | Ter juízo | Decisões | 1 |
| `etica/index.html` | Ter juízo | Decisões | 1 |
| `gigantes/orgulho/index.html` | Módulo 1: ser-se humano | Módulo 1: Humanos | 1 |
| `gigantes/quixote/index.html` | Módulo 1: ser-se humano | Módulo 1: Humanos | 1 |
| `index.html` | Ser-se humano | Humanos | 1 |
| `index.html` | Os algoritmos | Algoritmos | 1 |
| `index.html` | Ter juízo | Decisões | 1 |
| `mapa/index.html` | Expressão: os algoritmos | Algoritmos | 2 |
| `mapa/index.html` | Ser-se humano | Humanos | 2 |
| `mapa/index.html` | Ter juízo | Decisões | 3 |
| `narrativas/anguissola/index.html` | Módulo 1: ser-se humano | Módulo 1: Humanos | 2 |
| `narrativas/cigoli/index.html` | Módulo 1: ser-se humano | Módulo 1: Humanos | 2 |
| `narrativas/margens/index.html` | Os algoritmos | Algoritmos | 2 |
| `olhar-e-decidir/estetica/licao-1/index.html` | Ter juízo | Decisões | 7 |
| `olhar-e-decidir/etica/licao-1/index.html` | Ter juízo | Decisões | 7 |
| `olhar-e-decidir/etica/licao-2/index.html` | Ter juízo | Decisões | 7 |
| `olhar-e-decidir/index.html` | Ter juízo | Decisões | 2 |
| `olhar-e-decidir/justica/aplicar/index.html` | Ter juízo | Decisões | 1 |
| `olhar-e-decidir/justica/docente/index.html` | Ter juízo | Decisões | 1 |
| `olhar-e-decidir/justica/guiao/index.html` | Ter juízo | Decisões | 1 |
| `olhar-e-decidir/justica/index.html` | Ter juízo | Decisões | 2 |
| `olhar-e-decidir/justica/licao-1/index.html` | Ter juízo | Decisões | 1 |
| `olhar-e-decidir/justica/licao-2/index.html` | Ter juízo | Decisões | 1 |
| `olhar-e-decidir/justica/licao-3/index.html` | Ter juízo | Decisões | 1 |
| `tests/resultados_turma.test.cjs` | Ter juízo | Decisões | 2 |
| `tests/test_cidadania_casos.py` | Ser-se humano | Humanos | 1 |
| `tests/test_cidadania_casos.py` | Os algoritmos | Algoritmos | 1 |
| `tools/cidadania_m1_layout.py` | Ser-se humano | Humanos | 2 |
| `tools/cidadania_piloto.py` | Ser-se humano | Humanos | 2 |
| `tools/generate_cidadania_m1.py` | Ser-se humano | Humanos | 1 |
| `tools/generate_cidadania_m1.py` | SER-SE HUMANO | HUMANOS | 2 |
| `tools/justica/moldes/licao-1.html` | Ter juízo | Decisões | 1 |
| `tools/justica/moldes/licao-2.html` | Ter juízo | Decisões | 1 |
| `tools/justica/moldes/licao-3.html` | Ter juízo | Decisões | 1 |
| `tools/licoes/cidadania-m1-s01.json` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s01.py` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s02.json` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s02.py` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s03.json` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s03.py` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s04.json` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s04.py` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s05.json` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s05.py` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s06.json` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s06.py` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s07.json` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s07.py` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s08.json` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s08.py` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s09.json` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s09.py` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s10.json` | Ser-se humano | Humanos | 1 |
| `tools/licoes/cidadania-m1-s10.py` | Ser-se humano | Humanos | 1 |
| `vozes/25-de-abril/index.html` | Ser-se humano | Humanos | 1 |
| `vozes/absurdo/index.html` | Ser-se humano | Humanos | 1 |
