# Coleções explícitas e navegação digerível

Baseline: `bc35ce590ebd21ff7203f31846644aeee857032c` (PR #10). Âmbito: índice de Narrativas, CSS dos cartazes e pertença dos índices de Gigantes e Margens; sem alterações em Português ou nos exercícios.

## Resultado

Experimentar reúne seis coleções: 13 experiências curtas, oito cenas Corta, vinte oficinas, quinze aquecimentos, Explorar e observar e Criar um projeto. Conserva as três propostas rápidas. As listas abrem por escolha, em vez de expor todos os cartões em sequência. Um conjunto aberto fecha o anterior dentro da mesma área.

Vidas e ideias apresenta três entradas explícitas: Aos ombros de gigantes (acesso direto aos 21 gestos), Seis vidas entre arte e ciência (abre os seis cartazes individuais, incluindo Fontana) e Margens (acesso direto aos dois estudos). Cada coleção tem um motivo gráfico distinto. Gigantes e Margens indicam Vidas e ideias no caminho de navegação, etiqueta e retorno. As rotas existentes, atalhos para Cidadania e outras relações pedagógicas permanecem.

## Testes executados

- Comparação automática e revisão independente: 66 cartões do Laboratório, 21 de Gigantes e dois de Margens byte a byte idênticos e na mesma ordem; scripts internos e externos idênticos; chaves de progresso preservadas. Todos os destinos do Laboratório preservados, sem duplicação; nos dois índices apenas o retorno genérico passa para o conjunto correspondente. Identificadores antigos preservados e sem duplicados. Sem ligações aninhadas.
- Navegador real: onze conjuntos abrem com Enter e fecham com Espaço; alternância exclusiva confirmada em Experimentar; estado expandido/recolhido exposto na árvore de acessibilidade.
- 44 verificações de conjuntos abertos a larguras CSS efetivas de 320, 390, 768 e 1440 px, sem overflow horizontal ou estreitamento ilegível do título. Cartazes de Gigantes e Margens inspecionados em computador e telemóvel; estado de progresso de Gigantes também inspecionado a 320 px. Os dois índices com breadcrumb/retorno foram abertos a 390 px sem overflow.
- Fixture exclusivamente local: contador, cinco cartões concluídos e três recursos com progresso iguais antes/depois. Inclui uma oficina e uma biografia dentro das novas coleções; o cartaz direto de Gigantes mantém a marca de progresso. Não alterado o armazenamento público do utilizador.
- Projeção aplicada aos 66 cartões, mesmo recolhidos, e aos três atalhos (69 destinos).
- Os cartazes individuais foram abertos e inspecionados, incluindo o retrato de Fontana. Sem erros ou avisos de consola no teste local.
- Medição de composição, não de desempenho: a 390 px, com conjuntos recolhidos, a altura passou de 15308 para 6005 px (menos 60,8%). Os 62 cartões antes expostos ficam dentro das coleções; os 66 continuam no documento. Não é redução de bytes nem benchmark de carregamento.
- Capturas antes/depois em computador e telemóvel guardadas localmente; fixtures não publicadas. CSS com versão de cache `20261019-2`.

## Limites

Não repetidos todos os exercícios preservados; não executados leitor de ecrã real, dispositivos físicos ou benchmark de desempenho/rede. Verificações complementares pendentes. Não é certificação funcional de todo o site. Deployment e percursos públicos finais registados no PR após publicação.
