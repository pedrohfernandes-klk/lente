# Justiça, fase 0: comparação dos desenhos

02/11/2026. Desenhos publicados abertos lado a lado, com a mesma caixa de visualização. Os valores de espessura vêm dos SVG; as diferenças de escala foram também vistas. A lição 1 é a referência de estilo, sujeita aos limites fixados pelo docente.

| Lição e cartão | Antes: espessura, figura, escala e pormenor | Depois desta fase | Trabalho da fase 1 |
|---|---|---|---|
| L1 C3, condutor | 1,1 a 2; pessoas pequenas, cabeça circular, corpo simples; seta tracejada | Igual | Referência para escala e figura |
| L1 C7, ponte | 1,1 a 2,4; duas escalas de pessoa na ponte; muitos traços na via | Igual | Limitar a 2,2 e uniformizar as figuras com as primitivas |
| L1 C9, alçapão | 1,1 a 2,4; homem maior e trabalhadores pequenos; mecanismo mais detalhado | Igual | Limitar a 2,2; pessoa e seta pelas primitivas |
| L1 C12, urgências | 1,6 a 2,6; cama do caso grave mais espessa; figura médica maior | Igual | Retirar o excesso de espessura e uniformizar a figura |
| L1 C12, transplantes | 1,2 a 2,4; sinais de sono em forma de letras, embora desenhados por caminhos | Igual | Retirar as letras e limitar a 2,2 |
| L1 C21, bote | 1,1 a 2,2; bustos, figura deitada e ondas; figuras maiores na caixa que no elétrico | Igual | Mesma escala de figura e uso consistente de `busto()` |
| L2 C6, balança | 1,1 a 2,2; pessoa da mesma família gráfica, mas ampliada em relação ao elétrico | Igual | Ajustar a escala da pessoa e da composição |
| L2 C9, Ford Pinto | 1,3 a 2,2; sem pessoas; carro ocupa quase toda a largura; contorno tracejado para o choque | Igual | Preservar a simplicidade; uniformizar seta com `seta()` |
| L2 C22, três ecrãs | 1,1 a 2; pessoas de pé e bustos com tamanhos diferentes nos três ecrãs | Igual | Usar `pessoa()` e `busto()` com escala comum |
| L3 | Sem desenhos publicados | Igual | Não há desenho antigo para refazer |

Todos usam preto e branco, `currentColor`, ausência de preenchimento e pontas e junções redondas. Não foram desenhados novos elementos nesta fase.

## Imagens documentais

| Imagens acrescentadas | Página, licença e tarefa «Olha» |
|---|---|
| Nenhuma na fase 0 | Não aplicável. As candidatas e a conferência de direitos pertencem à preparação das lições e à fase 1. |

## Alterações visíveis autorizadas

- L1 C11: troca exata do #90, cabeça `5c9268c5`, preservada nos dados e na regeneração. A revisão do texto deste cartão continua coordenada com esse pedido.
- L2 C18: «O pushpin era, explica Sandel, um jogo de crianças.» passa a «O pushpin era, explica Sandel, uma brincadeira de crianças.». Nenhuma outra parte desse cartão muda.
- Restantes cartões, menus, chaves e índices: sem diferenças. A prova é automática, por inversão das duas trocas e comparação do resumo SHA-256 de cada página publicada.

## Por confirmar

- Episódios 4 a 12: o pedido das faixas inglesas publicadas devolveu zero bytes nos nove vídeos oficiais. Não foram usados serviços de terceiros nem criados ficheiros de legendas vazios. São necessárias as transcrições do canal oficial e a conferência audiovisual dos tempos.
- A imagem e os cartões do molde novo entram apenas depois da revisão e integração da fase 0 e das dependências comunicadas pelo docente.

## Revisão L95-01 e L95-02, 02/11 à noite

O main foi integrado por merge antes das correções. A validação do molde novo passou para uma função usada também pelo validador de bancos. `frase` e `versos` são ordenação; a produção livre pedida num cartão `ler` declara o booleano `producao_livre` e entra no teto de uma escrita. A sucessão é medida na sequência visível, incluindo leituras. As variantes têm de ser selecionadas antes da validação.

As provas sintéticas aceitam frase e versos com uma escrita, recusam duas escritas ou uma escrita mais produção livre em leitura, validam a marcação semântica e distinguem escolhas intercaladas de três escolhas ou três leituras consecutivas. Não dependem de ativar `molde_novo` nos três bancos antigos.

Verificação local: 17 testes específicos e 13 testes Node passaram. A regeneração confirmou as três lições e o manifesto de 72 citações. O navegador percorreu 450 cartões em 18 combinações de lição, largura (320/390/1366) e projeção, sem erros JavaScript nem deslocamento horizontal. Esta bateria não cobre o modo escuro; a revisão independente mede também esse modo.

A bateria geral executou 260 testes. Após normalização local para LF, ficaram duas falhas de finais de linha de geradores antigos da Cidadania: `test_source_generation_is_reproducible` e `test_m1_igual_a_origin_main`. Não foram alterados esses testes nem os geradores alheios ao pedido. Os ficheiros alterados apenas pela execução foram repostos depois de comparar o conteúdo. O resultado integral local não é declarado verde.

Mantém-se a dívida já declarada: a projeção ainda pode gravar a conclusão pessoal no motor antigo. Não foi dada como resolvida pela extração. Tempos e funcionamento audiovisual não foram certificados por esta bateria.
