# Mostrar o que se pede para observar

Base 60bf6a1e95b7e67fcad6ec78a098f21cd480248f. Lote isolado do modo noturno e dos 141 ficheiros do PR #38 (head b33f21c8). Não altera Cidadania M1, Cartaz, geradores ou recursos partilhados de projeção.

## Problema e alcance

O utilizador encontrou o rosto de Demóstenes cortado em `investigar/passo-01/`. A imagem vertical estava a preencher uma faixa horizontal. A pesquisa de figuras didáticas verticais com a mesma regra encontrou mais seis casos:

- `investigar/passo-03/`: Cancioneiro da Biblioteca Nacional.
- `narrativas/aula-nao-dito/`: Rapariga a ler uma carta à janela, Vermeer.
- `narrativas/piramide/`: Aparição do Adamastor, Carlos Reis.
- `sidequests/bach/`: retrato com partitura, Haussmann.
- `sidequests/mozart/`: retrato de Barbara Krafft.
- `cidadania/m2/cid-m2-preco-minuto/`: máquina de Jacquard com cartões perfurados.

Cada figura recebe `completa` e regras locais para manter a proporção, centrar a moldura e limitar a altura a `min(44vh,420px)`, com a ampliação existente. Não é substituição global de cover: cartazes e outros recortes editoriais ficam intactos. Imagens, bytes, alt, legendas, atribuições, licenças, fontes, URLs, textos, exercícios, índices, pontuação, progresso e motor mantêm-se. A reversão da classe e CSS restituiu exatamente o conteúdo anterior nas sete páginas.

## Validação própria

- 52 testes Python e `git diff --check` aprovados.
- Antes/depois de Demóstenes a 1280×800 e 390×844: a testa isolada é substituída pela cabeça completa e suporte, sem deformação.
- Sete aberturas a 1280×800 e 390×844, imagens carregadas e proporcionais, sem transbordo horizontal; sete composições inspecionadas visualmente.
- Sete ampliações por Enter e fechos por Escape a 320×740, com foco devolvido à figura, sem transbordo.
- Sete páginas projetadas × três tamanhos: 21 estados, seleção correta e imagem/QR presentes. Capturas de Demóstenes nos três tamanhos e amostras Vermeer/Jacquard em grande.
- Evidências externas: outputs/enquadramentos-20261025/qa-completas-investigar.json, qa-completas-320.json e qa-completas-projecao.json, com capturas correspondentes.

Não foram repetidos todos os percursos pedagógicos, leitor de ecrã, impressão, QR/aparelho e projetor físicos, desempenho ou modo noturno ainda em desenvolvimento. A pesquisa cobriu imagens locais de figuras fig-rev com proporção vertical identificada; não certifica todos os tipos de imagens do site. Os geradores devem preservar estas classes/regras na próxima regeneração; não foram editados neste lote.

Publicação autorizada pelo utilizador após testes críticos. Confirmar head, publicação Pages e os recursos no site público; manter o lote separado da reestruturação #38.
