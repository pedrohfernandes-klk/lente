# Justiça: bases para treze lições

02/11/2026. Fase 0. Os bancos foram extraídos do HTML publicado, no main `ba946f6`, e não do gerador histórico. Conservam as opções revistas no #72, os endereços, as chaves, a ordem dos cartões, o motor e `?projetar=1`.

## Construir e verificar

```sh
python tools/justica/build.py --verificar
python tools/justica/build.py
python -m unittest discover -s tests -p 'test_justica*.py' -v
node --test tests/resultados_turma.test.cjs
node tests/browser_justica.cjs
```

`licoes.json` declara as lições publicadas: número, chave, vídeo, aulas, anterior, seguinte e estado do molde. `bancos/` contém JSON válido, conservando a serialização publicada para permitir a comparação literal. `moldes/` guarda a casca publicada sem o banco. Para atualizar um cartão, altera-se o banco e regenera-se; nunca se extrai automaticamente uma mudança do HTML por cima dos dados.

`migracao.json` contém as únicas diferenças autorizadas face ao main de partida: o cartão 11 da lição 1 trazido do #90 (cabeça `5c9268c5`), e «um jogo de crianças» para «uma brincadeira de crianças», no cartão 18 da lição 2. O teste desfaz apenas estas duas trocas e exige o SHA-256 do HTML de origem. A lição 3 é idêntica à publicada.

## Citações

`citacoes.json` guarda só as citações curtas usadas nos bancos, com episódio, vídeo, cartão e tempo. Cada entrada tem no máximo duas frases. Quando existe um par explícito de original e tradução, a tradução também consta do manifesto. O teste exige que o manifesto corresponda aos bancos.

As legendas e as transcrições não entram neste repositório, nem no CI. Para conferir localmente, definir `JUSTICA_LEGENDAS` com uma pasta privada e executar:

```sh
python tools/justica/build.py --verificar --legendas
```

São aceites os nomes `ep01.en.vtt` e `ep1.en.vtt`. O programa exige que cada frase exista nas legendas do episódio certo. Esta verificação textual não substitui a conferência audiovisual dos tempos. Os tempos das lições 1 a 3 são os publicados; não se atribuem tempos aos episódios novos sem os conferir.

## Regras e passagem à fase 1

O teto de 26 cartões mantém-se. O validador cobre as palavras proibidas, a pontuação, os retornos, as opções equilibradas e as leituras novas até 95 palavras visíveis, incluindo original e tradução. A única leitura publicada acima do limite é L1 C12, 99 palavras, registada numa lista fechada no teste por decisão do docente de 02/11. Não se admitem novas exceções nem aumentos; a ocorrência sai quando for dividida na fase 1.

O molde novo exige pelo menos 14 atividades, cinco tipos sem escrita, no máximo uma escrita, nunca três atividades seguidas do mesmo tipo, «Na aula», imagem no «Abre», «Olha» logo a seguir e «No fim, consegues». A navegação é lida pelo manifesto; o teste exige índice, anterior e seguinte. Os menus existentes ficam preservados na fase 0.

`desenhos.py` e `desenhos.json` conservam as primitivas do desenho a traço. A tabela de comparação está em `docs/qa/justica-fase0-20261102.md`. O redesenho e as imagens documentais pertencem à fase 1. Nenhuma imagem documental foi acrescentada nesta fase.

## Produção livre e sequência do molde novo

02/11/2026: os achados L95-01 e L95-02 corrigem a interpretação das regras, sem alterar os tetos. `frase` e `versos` ordenam material dado: contam para a variedade sem escrita. Só `escrita` é produção livre pelo tipo. Um cartão `ler` que peça produção livre em papel declara `"producao_livre": true`; esse pedido entra no mesmo teto de uma produção por lição. O campo é booleano e só se aplica a `ler`. A autoria tem de o declarar, sem inferência automática a partir do texto.

`validar_molde_novo` verifica a sequência apresentada ao aluno, incluindo as leituras. Três escolhas separadas por leituras não são consecutivas; três leituras seguidas são. Quando houver variantes, o chamador entrega a sequência já selecionada. A contagem de atividades continua a excluir `ler`.

Os testes sintéticos exercem estas regras mesmo enquanto todos os bancos publicados têm `molde_novo=false`: ordenações com uma escrita; duas escritas; produção livre dentro de leituras; marcação inválida; escolhas intercaladas; três escolhas ou três leituras consecutivas. A validação geral do banco chama também estas regras quando recebe `novo=true`.

## Continuação publicada em novembro de 2026

As lições 4 a 13 cobrem os episódios 4 a 12; as aulas 13 e 14 do episódio 7 são duas lições. A primeira versão usava blocos oficiais completos. Em 10/11/2026, o docente pediu a publicação da prévia curta da lição 4 e a aplicação do mesmo formato às seguintes, sabendo que os tempos eram aproximados.

O formato curto, declarado por `formato_curto` no manifesto, tem dez cartões: abertura, quatro pares de excerto e exercício, e uma produção final de 60 a 100 palavras. Substitui, apenas nestas dez lições, os mínimos de 20 cartões e 14 atividades do formato anterior. O validador exige exatamente quatro vídeos, cada um entre 60 e 180 segundos, sempre seguidos de uma atividade, com a indicação de tempos aproximados. As três lições antigas e os testes do molde anterior mantêm-se.

`excertos-curtos.json` regista os limites, os títulos, a fonte pública dos tempos e a ausência de conferência audiovisual. A seleção usa índices automáticos como orientação, não transcrições verificadas. Os textos pedagógicos são adaptações apoiadas nos temas, leituras e guias oficiais; não são citações da fala de Sandel. As páginas e o guia docente identificam esta limitação. `novas/videos.json` conserva os limites oficiais completos para consulta histórica; os limites atuais do leitor vêm de `excertos-curtos.json` e são conferidos contra os bancos nos testes.

As novas páginas usam o motor partilhado. A navegação da lição 3 continua para a 4, sem retirar o acesso a «Aplicar». Os textos de apoio podem ser usados quando o vídeo não estiver disponível.

## Revisão de 11/11/2026: formato guiado

As lições 4 a 13 declaram `formato_guiado` no manifesto. O formato mantém os quatro excertos de 60 a 180 segundos e a produção final de 60 a 100 palavras, e recupera o apoio das lições 1 a 3: um cartão «Antes de ouvir» com quatro expressões em inglês; em cada excerto, uma pergunta de escuta antes (`ex-antes`), uma frase da aula com tempo e tradução (`cita-en`, `trad`), uma pergunta para depois (`ex-depois`) e um «Ler mais»; e uma ou duas atividades sobre o que se diz no excerto. `validar_molde_guiado` exige 11 a 15 cartões, três tipos de atividade com pelo menos uma escolha, ordenações com quatro passos e retornos ao erro diferentes da explicação. O formato curto já não é declarado por nenhuma lição; o seu validador continua testado sobre `tests/fixtures/justica-formato-curto-exemplo.json`.

Os limites foram refeitos sobre as falas de cada episódio, obtidas por reconhecimento automático do áudio. O texto reconhecido é um auxiliar privado e não entra no repositório. `excertos-curtos.json` regista, por excerto, o início e o fim em segundos, a aula e as palavras de entrada e de saída, e o estado: conferido com o áudio, sem conferência por uma pessoa no leitor do YouTube. As páginas dizem «Tempos conferidos com o áudio»; o validador aceita também «Tempos aproximados» para um corte que volte a esse estado. As lições 9 e 13 passam a ter excertos das duas aulas que declaram.

O índice e a secção `licoes-4-13` do guia docente mudam por uma terceira camada exata, `tests/fixtures/justica-guiada-20261111.json`, encadeada em `tests/justica_20261110.py`.
