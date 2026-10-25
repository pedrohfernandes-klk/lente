# Modo noturno suave — primeiro lote real, 25/10/2026

## Cobertura explícita

Lote opt-in em duas páginas: Português `m5/gram-dil/` e LENTE `narrativas/quem-conta/`. Em cada repositório, só a página indicada carrega os novos recursos `assets/appearance.js` e `appearance.css` e declara um ponto para o controlo. Não é integração universal. Não altera Cartaz, geradores, recursos de projeção nem Cidadania M1.

## Comportamento

Paleta Cartaz aprovada, com papel/tinta suaves, terracota no Português e mostarda no LENTE. Preferência inicial do sistema, alternância manual sempre no cabeçalho da página normal e persistência local em `epi-theme`. Botão de 44 × 44 px, nome acessível, estado e foco visíveis. O cabeçalho móvel organiza informação e ações em duas linhas. Não aplica filtros às imagens.

O código não escreve nas chaves de progresso. Funciona sem armazenamento, sincroniza separadores na mesma origem e valida origem/emissor das mensagens de iframe. Não cria serviços, pedidos de rede, telemetria ou temporizadores. Um iframe não duplica o botão. A integração do controlo no envolvente de projeção e nas restantes famílias fica fora deste lote.

## Testes executados

- 12 testes Node em cada repositório: sistema/manual, persistência, armazenamento bloqueado, sincronização, ausência de duplicação, mensagens e tokens/impressão.
- 178 testes Python PT e 52 LENTE aprovados, além de sintaxe e diff.
- PT: percurso novo completo de nove passos, 80/90 com um erro deliberado, feedback de erro/acerto, seleção múltipla e classificação, resultado e Rever. Alternar e recarregar preservou as respostas.
- LENTE: treze cartões, sete respostas certas, seleção de palavras, verdadeiro/falso, associação, feedback, proposta no caderno e resultado (95 pontos). Também testada uma resposta errada em tentativa QA separada.
- Leitura e controlo móvel: 320/390 px; computador 1280 px. Sem transbordo horizontal nos estados medidos; controlo 44 px atingível no centro. Comparações claro/escuro registadas.
- Projeção LENTE: os três estados 18/22/28 px foram acionados e vistos, com QR e sem botão noturno duplicado na página incorporada. Os recursos de projeção não foram alterados.

## Limites e pendências complementares

Leitor de ecrã real, impressão física e projetor da escola não executados. Não inferir cobertura de todos os cartões existentes a partir destas duas páginas. A preferência no envolvente da projeção e o alargamento aos moldes requerem um incremento próprio.

Foi observado um erro intermitente de MutationObserver no navegador. O mesmo erro ocorreu em controlo estático sem JavaScript: não há evidência para o atribuir a este módulo. A alternância funcionou nos testes; não se declara ausência de erros em todo o ambiente.

Os ensaios usam cópias QA com chaves próprias; essas cópias e os estados de teste não são publicados. Os textos, URLs, bancos, critérios e chaves de progresso da versão real conservam-se.