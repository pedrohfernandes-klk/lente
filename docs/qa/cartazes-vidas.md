# Vidas e ideias — seis cartazes documentais

Baseline: 6f8815b314283ef69ad457ad2be8218b2603e27d. Continuação autorizada da família de cartazes, com publicação incremental e testes críticos proporcionais.

## Alteração delimitada

Os seis acessos de Vidas e ideias passam a reunir nome, pergunta de entrada, imagem ou composição gráfica, sinopse, tempo, ação e estado de leitura. Títulos, sinopses, durações, destinos e chaves originais são preservados. O texto de introdução esclarece que as perguntas despertam a leitura e não são questionários.

- Duchamp: fotografia de Alfred Stieglitz, 1917; o recorte mantém a assinatura visível. A pergunta não fecha a discussão de autoria tratada no percurso.
- Sofonisba Anguissola: Autorretrato ao cavalete, 1556; recorte da pintora e do quadro.
- Lavinia Fontana: composição tipográfica com as iniciais, identificada como tal; não imita uma assinatura histórica.
- Leonardo: paisagem do vale do Arno, 1473; pergunta sobre desenhar para descobrir.
- Cigoli: esquema de luz e sombra em CSS, identificado como esquema; não substitui a obra no percurso.
- Galileu: aguadas cuja atribuição permanece explícita como incerta.

A curadoria independente leu os seis percursos e confirmou os créditos nos registos de origem. Não há nova transcrição ou questionário nas páginas das leituras, que permanecem inalteradas.

## Preservação e custo

66 cartões mantidos, com os mesmos IDs, ordem e destinos. Os outros 60 são byte a byte idênticos. Todos os scripts inline e externos permanecem idênticos; nenhum armazenamento novo. O CSS anterior mantém-se como prefixo, com cerca de 3,7 KB acrescentados e regras limitadas aos seis cartazes. O URL da folha é versionado para evitar cache antiga.

Sem fontes, bibliotecas ou imagens novas no repositório. Quatro imagens já existentes, todas lazy e com dimensões explícitas. Galileu reutiliza o URL do cartaz da coleção; os três URLs adicionais somam 465 732 bytes. Fontana e Cigoli evitam transferir imagens grandes para a navegação. Não se apresenta este inventário como uma medição de desempenho.

## Testes executados

- Verificação estática local e independente: 66 IDs/ordem/destinos; metadados r/t/s/a preservados; scripts idênticos; CSS anterior preservado; IDs únicos. Sem falhas.
- Seis destinos abertos por Enter a partir dos novos cartazes; títulos e interfaces das leituras carregados nos seis casos. Não foram repetidas as leituras integrais.
- Larguras de viewport CSS 320, 390, 768 e 1440: sem transbordo da página ou dos cartazes; imagens carregadas; elementos gráficos sem recortes acidentais. A escala atual do navegador foi considerada para medir a largura CSS real.
- Cenário QA isolado antes/depois: uma de quatro aulas lidas, nove cartões marcados e as seis leituras com Feita. Rever, em ambos os casos. Nenhuma alteração às chaves públicas por estas fixtures.
- Projeção: 66 missões e três inícios continuam a receber projetar=1, incluindo os seis cartazes documentais.
- Consola sem avisos/erros nos fluxos testados. Comparações antes/depois em computador e telemóvel guardadas no workspace.

Fixtures, scripts auxiliares e capturas ficam fora da publicação. As cores reutilizam as três paletas já aprovadas, com contrastes dos textos entre 11,82:1 e 14,69:1.

## Complementares não executados

Leitor de ecrã real, dispositivo físico, desempenho representativo e todos os estados possíveis de progresso. Os testes de abertura não certificam todos os conteúdos históricos nem todos os percursos de leitura. Estas verificações não são apresentadas como aprovadas.

Antes de declarar publicação concluída, confirmar Pages para o SHA integrado e os seis cartazes no endereço público.
