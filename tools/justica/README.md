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

As lições 4 a 13 cobrem os episódios 4 a 12; as aulas 13 e 14 do episódio 7 são duas lições. `novas/` guarda a proveniência das imagens e dos blocos oficiais, não uma segunda cópia dos cartões. Os bancos continuam a ser a fonte única do conteúdo. Não há citações novas atribuídas à fala de Sandel nem cortes curtos com tempos inferidos. Usam-se os limites das aulas incorporadas no sítio oficial, consultado em 10/11/2026. O leitor preserva esses limites.

As novas páginas usam o motor partilhado, mantendo os cartões das três lições antigas. A navegação da lição 3 continua agora para a lição 4, sem retirar o acesso a «Aplicar». Cada banco cumpre o molde novo: 20 a 26 cartões, pelo menos 14 atividades, cinco tipos, imagem e observação inicial, um momento de comparação oral e uma única produção livre de 60 a 100 palavras. Os textos de apoio podem ser usados quando o vídeo não estiver disponível.
