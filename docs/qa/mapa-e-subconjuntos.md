# Mapa do LENTE e segundo nível das coleções

Baseline `70cc80228e4400377f9b726b41e09cc486e4cbc5`. Mapa em `/mapa/`, acessível no início e no Laboratório. Duas áreas: Cidadania e Desenvolvimento e Laboratório de Narrativas. O Laboratório conserva três portas: Aulas, Experimentar e Vidas e ideias. Os níveis do mapa começam recolhidos e abrem por escolha; as ligações conduzem às páginas reais. Agrupadores sem página própria não recebem um falso acesso a um hub representativo.

Segundo nível no índice do Laboratório:

- Oficinas: Construir e escrever (7), Cena, imagem e espaço (6), Deslocar e questionar (7).
- Aquecimentos: Ler a fundo (7), Ouvir e ler (5), Palavras, imagens, hábitos (3).

As vinte oficinas foram reordenadas por estas finalidades, preservando cada cartão, identificador, número e destino. Os quinze aquecimentos mantêm as três famílias que já constavam do índice. «Ver para fazer» integra Ler e investigar; «Fazer. Voltar a ver.» integra Criar um projeto. As outras relações estão explícitas no mapa, incluindo Ética/Estética sob Olhar e decidir e Mesa de edição como apoio editorial. As cores assinalam níveis e acessos: numerais dos três conjuntos, sinais de abertura e setas, sem criar uma quarta área.

## Verificações

- Revisão independente: scripts raw idênticos nas duas páginas existentes; 66 cartões byte a byte preservados como multiconjunto; hooks de progresso, IDs e destinos anteriores intactos. Seis novos subconjuntos com contagens 7/6/7 e 7/5/3. Sem IDs duplicados ou links em comandos de abertura.
- 275 ligações LENTE do mapa verificadas contra a árvore do repositório e o candidato, incluindo fragmentos; zero falhas. Os quinze aquecimentos PT conservam os destinos existentes, confirmados também no inventário local do Português. Não é uma verificação funcional integral de todos os destinos.
- Navegador real: 41 ramos do mapa abriram com Enter e fecharam com Espaço; clique num ramo visível também confirmado. Mapa aberto e recolhido em 320, 390, 768 e 1440 px, larguras CSS efetivas confirmadas, sem overflow. Verificação adicional chegou a 264 px.
- Seis subconjuntos em quatro larguras: 24 casos abertos, sem overflow e com comandos maiores que 44 px. A ligação direta a `#oficinas-escrever` abriu nativamente o conjunto exterior e apresentou o subconjunto; sem código novo para revelar os ancestrais.
- Continuação e progresso local comparados antes/depois, sem diferenças. Projeção mantida nos 66 cartões e três atalhos (69 destinos), mesmo dentro dos subconjuntos. Nenhum armazenamento público do utilizador foi alterado para os testes.
- Inspeção visual e capturas locais dos mapas, do índice e das marcas de cor. CSS dos mapas usa regras de página restritas a `.site-map` e classes próprias para não reformular o início. Sem novas bibliotecas, imagens ou scripts.

## Limites e manutenção

Não repetidos os percursos completos de todos os exercícios; não executados leitor de ecrã real, dispositivos físicos, mudança real do esquema escuro, zoom real 200% ou benchmark de rede/desempenho. Pendências complementares documentadas. Navegação pública e ligações entre os dois mapas serão registadas no PR depois dos deployments.

Ao alterar coleções, atualizar também o mapa e verificar destinos e fragmentos. Manter os agrupamentos editoriais como escolhas, sem os apresentar como novos percursos obrigatórios. Não propagar dados biográficos de sinopses para o mapa sem verificação factual.
