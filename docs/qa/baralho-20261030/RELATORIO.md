# Baralho improvável: relatório para revisão

## 1. Ramo, commit e pedido de integração

Ramo: `codex/baralho-prototipo-20261030`, criado a partir de `main` em `aea224be2db786a7ddfd814852fc6255ed71952a`. O SHA final e o número do pedido em rascunho acompanham a entrega no chat. Nada fundido ou publicado.

## 2. Ficheiros

Todos os ficheiros desta entrega são novos. Nenhum ficheiro partilhado ou página existente foi alterado.

- `narrativas/formas/tres-cartas/index.html`: página noindex, sem ligação de entrada, com a casca e sem carregar cartoes.js.
- `assets/formas/tres-cartas-dados.js`: cartões, opções, pistas, explicações, exemplos, interface e composição declarativa.
- `assets/formas/tres-cartas.js`: controlador com oito tipos de cartão e integração EPICasca/LenteProgresso.
- `assets/formas/tres-cartas.css`: dimensões das imagens, disposição das opções, plano e impressão; nenhuma regra de alinhamento.
- `assets/formas/baralho/11-01.webp`: recorte de 512 × 512 da sombra.
- `assets/formas/baralho/13-02.webp`: recorte de 512 × 512 do horizonte.
- `assets/formas/baralho/20-03.webp`: recorte de 512 × 512 da rampa.
- `assets/formas/baralho/origem.json`: proveniência dos três recortes, coordenadas, kept e commit da curadoria.
- `tests/test_tres_cartas.py`: contratos de estrutura, língua, licença, seleção e dimensões.
- `tests/opcoes_tres_cartas.cjs`: medição de comprimentos visíveis e distribuição das respostas certas.
- `tests/browser_tres_cartas.cjs`: percurso integral com teclado, erros e correção, cópia, revisão A/B, recarga, projeção, impressão e três larguras.
- `docs/qa/baralho-20261030/01-primeiro.png`: primeiro cartão a 390 px.
- `docs/qa/baralho-20261030/04-escolha.png`: escolha de ligação a 390 px.
- `docs/qa/baralho-20261030/15-composicao.png`: plano a 390 px.
- `docs/qa/baralho-20261030/16-escrita.png`: escrita do conto com plano a 390 px.
- `docs/qa/baralho-20261030/papel.pdf`: impressão A4 de referência, seis páginas, revista visualmente.
- `docs/qa/baralho-20261030/opcoes.txt`: resultado integral da medição.
- `docs/qa/baralho-20261030/suite-baralho.log`: primeira execução da suite, incluindo falhas de ambiente.
- `docs/qa/baralho-20261030/suite-baralho-final.log`: execução final dos 150 testes Python.
- `docs/qa/baralho-20261030/navegador-baralho.log`: resultados Chromium do novo percurso.
- `docs/qa/baralho-20261030/navegador-formas.log`: resultados do navegador do Laboratório existente.
- `docs/qa/baralho-20261030/navegador-treinos.log`: resultados dos 12 percursos de treinos.
- `docs/qa/baralho-20261030/testes-node.log`: resultados dos 27 testes JavaScript existentes.
- `docs/qa/baralho-20261030/RELATORIO.md`: este relatório.

## 3. Percurso

14 exercícios antecedem a composição e a escrita. Nas perguntas com solução, o feedback explica a tentativa e o avanço exige correção. Ligação, narrador, começo, ordem e fim admitem escolha livre. Não se impõe uma sequência universal.

| N.º | Tipo | Operação | Resposta |
|---|---|---|---|
| 1 | escolher | O que faz a figura sentada? | Carimba um documento. |
| 2 | escolher | Que pormenor permite imaginar um horizonte transportado? | A linha entre duas pessoas. |
| 3 | escolher | Que objeto sai da mala? | Uma rampa desdobrável. |
| 4 | escolher | Como vais ligar as três cartas? | Escolha livre |
| 5 | escolher | Quem conta e a partir de onde? | Escolha livre |
| 6 | escolher | Que começo queres desenvolver? | Escolha livre |
| 7 | ordenar | Por que ordem vais revelar os acontecimentos? | Escolha livre |
| 8 | classificar | Qual destes títulos informa melhor numa notícia fictícia? | O horizonte chegou à praça |
| 9 | escolher | Que abertura situa quem, o quê, quando e onde? | Os moradores mudaram ontem o horizonte para a praça. |
| 10 | completar | Que conector exprime a consequência? | Por isso |
| 11 | classificar | Qual frase retira a opinião da notícia fictícia? | A mudança do horizonte foi autorizada pela sombra. |
| 12 | escolher | Qual citação identifica a testemunha inventada? | «Vi a linha passar», contou Eva, moradora da praça. |
| 13 | classificar | Que frase usa terceira pessoa e passado? | Ela levou a rampa até à praça. |
| 14 | escolher | Que fim queres desenvolver no conto? | Escolha livre |
| 15 | composicao | Que plano vais levar para o caderno? | Sem resposta única |
| 16 | escrita | Escreve o conto no caderno. | Sem resposta única |
| 17 | escrita | Conta o mesmo acontecimento numa notícia fictícia. | Sem resposta única |
| 18 | autoavaliacao | Os dois textos contam o mesmo acontecimento? | Sem resposta única |
| 19 | autoavaliacao | O conto cria expectativa e a notícia informa? | Sem resposta única |
| 20 | autoavaliacao | A notícia responde às seis perguntas essenciais? | Sem resposta única |
| 21 | autoavaliacao | Identificaste a notícia e a testemunha como fictícias? | Sem resposta única |
| 22 | composicao | O que vais alterar na versão B? | Sem resposta única |
| 23 | exemplo | Como se ligam as peças deste conto? | Sem resposta única |
| 24 | exemplo | Como organiza a notícia o mesmo acontecimento? | Sem resposta única |

## 4. Composição

O cartão lê `partes: [{rotulo, fonte, conector}]`. Resolve cada fonte nas opções escolhidas e apresenta uma lista numerada; em ordenar, segue a ordem dos códigos selecionados. Não há um texto modelo montado automaticamente. Copiar o plano produz texto simples.

Exemplo concreto: ligação causal; narrador participante; começo «Na fila, a minha sombra avançou.»; acontecimentos «Inventar a passagem → Transportar a linha → Autorizar a mudança»; consequência possível «Por isso»; fim «A fila atravessou a linha do horizonte». Esta ordem de apresentação permite recuperar a causa depois da consequência. Seguem-se as peças da notícia: título informativo, abertura situada, relato sem opinião, testemunha fictícia e pessoa/tempo.

A escolha do conector causal surge expressamente condicionada à ligação causal. O aluno pode optar pela analogia e descobrir a relação de passagem durante a escrita. O plano manda adaptar a pessoa gramatical e desenvolver, não copiar, as peças.

## 5. Opções

Comando: `node tests/opcoes_tres_cartas.cjs`.

```
sombra: 21/22 caracteres; diferença 4.76%
horizonte: 27/27 caracteres; diferença 0.00%
rampa: 23/22 caracteres; diferença 4.55%
ligacao: 28/29 caracteres; diferença 3.57%
narrador: 30/28 caracteres; diferença 7.14%
comeco: 32/32 caracteres; diferença 0.00%
ordem: 20/20/20 caracteres; diferença 0.00%
titulo: 26/29 caracteres; diferença 11.54%
lead: 52/57 caracteres; diferença 9.62%
conector: 8/7 caracteres; diferença 14.29%
corrigir: 55/50 caracteres; diferença 10.00%
citacao: 50/51 caracteres; diferença 2.00%
verbo: 34/30 caracteres; diferença 13.33%
fim: 39/38 caracteres; diferença 2.63%
Certa entre as mais longas: 3/9; limite para duas opções: 5.

```

A medição usa caracteres Unicode visíveis, sem marcação HTML. Os quatro cartões de autoavaliação têm sempre Sim/Não, ambos com 3 caracteres. A distribuição conta empates como «entre as mais longas», de forma conservadora. As duas opções de citação contêm citação; a informação adicional não se confunde com extensão. A pergunta pede deliberadamente a identificação da testemunha.

A primeira execução encontrou 7/9 respostas certas entre as mais longas; as opções foram reescritas e o teste foi repetido. Nenhuma asserção foi removida.

## 6. Testes

Comandos executados na raiz, com Python UTF-8 (`PYTHONUTF8=1`) e Playwright/Chromium compatíveis:

- `python -m unittest discover -s tests -p 'test_*.py' -v`: 150 testes, 149 passaram, 1 falhou. Zero testes desativados ou saltados.
- `python -m unittest discover -s tests -p test_tres_cartas.py -v`: 3 passaram; incluídos nos 150.
- `node tests/opcoes_tres_cartas.cjs`: passou.
- `node --check assets/formas/tres-cartas.js`: passou.
- `node tests/browser_tres_cartas.cjs`: passou a 320, 390 e 1366 px; três imagens carregadas a 512 × 512, sem erros de página e sem deslocamento horizontal em todos os cartões. Teclado, bloqueio de respostas incorretas, copiar, primeira versão, mudança real de ligação A/B, recarga e projeção verificados.
- `node tests/browser_formas.cjs`: passou, incluindo Certa manhã e A cena que falta a 360/1440 px.
- `python tests/browser_lab_treinos.py`: passou, 12 percursos completos, relógio, verificação, 320/1440 px e projeção.
- `node --test tests/appearance.test.cjs tests/resultados_turma.test.cjs`: 27 passaram, zero falhas e zero saltados.

Falha final, preservada integralmente em `suite-baralho-final.log`:

```
FAIL: test_m1_igual_a_origin_main (test_cidadania_m2_molde.Molde.test_m1_igual_a_origin_main)
  tests/test_cidadania_m2_molde.py, line 294
    self.assertEqual(sorted(lista), locais)
AssertionError: Lists differ
First differing element 0:
'cidadania/m1/abertura/index.html'
'cidadania\m1\abertura\index.html'
Ran 150 tests in 18.068s
FAILED (failures=1)
```

O teste usa `str(Path.relative_to(...))`, que devolve separadores Windows, e compara-o com caminhos POSIX do Git. Não foi corrigido porque está na área reservada. Não afirmo que a suite inteira passou.

A primeira execução também encontrou diferenças CRLF/LF e uma leitura cp1252. O gerador invocado por um teste reescreveu localmente cidadania/projeto/index.html sem mudar conteúdo. Esse efeito foi revertido com `git restore` após os testes; o diff dos ficheiros existentes ficou vazio. A execução final usou UTF-8. Os ensaios iniciais Chromium precisaram de instalar a versão compatível e de permissão para aceder ao servidor local. Os testes não foram alterados para contornar essas condições.

## 7. Capturas

As quatro imagens de 390 × 844 px estão nesta pasta. O plano e a escrita têm deslocamento vertical normal, nunca horizontal. As capturas mostram o topo desses cartões; o plano completo pode ser percorrido e copiado. `papel.pdf` tem as três imagens, exercícios, referências para montar o plano, escrita e autoavaliação; os exemplos começam numa página separada no fim. Sem respostas pessoais na impressão.

## 8. Decisões, júris e pendências

**Aprendizagem:** operações específicas de observação, relação, narrador, começo, ordem, género, conector, objetividade, citação, pessoa/tempo e fim. As pistas são progressivas e próprias de cada exercício. A autoavaliação precede os exemplos. Os exemplos são breves e identificados como ficção; não substituem os textos pedidos.

**Clareza:** Chromium a 390 px, imagem primeiro e pergunta junto das duas escolhas no primeiro ecrã; a primeira ação não exige ler instruções nem deslocar. Revisão visual compatível com uma resposta em menos de 10 segundos, mas não é um teste observado com um aluno real. Esse ensaio permanece por fazer.

**Técnica:** o id é `tres-cartas` nas APIs existentes. Estado do separador em `sessao`, plano A imutável em `primeira`, `experimentei` apenas após os 14 exercícios e chegada ao plano, `revi` após confirmação da comparação A/B. Em projeção o controlador não recupera nem grava estado pessoal. Os testes verificam que localStorage e sessionStorage ficam iguais após interação projetada.

**Decisão sobre o caderno:** os textos completos A/B são escritos e conservados no caderno físico. Não introduzi caixas de texto. A página conserva e compara os planos A/B. A API `primeira` aceita apenas códigos alfabéticos; as escolhas e a ordem são codificadas por letras sem alterar progresso.js. Não há promessa de cópia digital dos textos. A declaração «Comparei A e B no caderno» regista uma ação, não avalia a qualidade da revisão.

**Pendente:** revisão do Claude/docente, ensaio real dos 10 segundos e decisão sobre a portabilidade do teste de Cidadania. Sorteio fora do âmbito. Nenhuma alteração necessária nas camadas reservadas. Não executar publicar.mjs, não fundir este ramo.
