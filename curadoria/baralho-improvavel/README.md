# Baralho improvável — passagem para Claude Code

Materiais de trabalho pedidos pelo docente em 29 outubro 2026. **Começar por [RELATORIO.md](RELATORIO.md)**. O [relatório visual e a galeria](index.html) funcionam localmente com a pasta `pranchas/` ao lado. Não é preciso o ZIP nem um serviço externo.

## O que está aqui

- **140 cartas selecionadas**, provenientes de 25 atlas WebP de seis vinhetas. O catálogo tem 156 registos: 140 mantidos e 16 excluídos (10,26%, arredondamento de 10%).
- [CURADORIA.json](CURADORIA.json): IDs estáveis, descrições, linha/coluna, procedência, decisão e motivos de exclusão. `row` e `column` começam em zero.
- `index.html`: mostra apenas as cartas mantidas, através de recortes de apresentação. Não mostrar atlas inteiros no jogo: alguns ainda contêm vinhetas excluídas.
- `pranchas/`: versões WebP com a resolução original, 1536 × 1024. Recompressão de distribuição com qualidade 90; não houve alteração de composição. Os PNG e o atlas 24, integralmente excluído, não entram no repositório. Metadados de origem e hashes estão no catálogo.
- [JORNADAS.md](JORNADAS.md): extensões opcionais e motores narrativos; consultar depois do relatório conciso. Os números históricos desse documento antecedem a seleção final; os totais atuais são os de `CURADORIA.json`.
- `prompts/`: prompts de geração e decisões de estilo. São documentação de produção, não texto destinado aos alunos. As imagens foram geradas com a ferramenta integrada imagegen.

O pacote contém ficções autorais, motivos populares e um conjunto inspirado num facto documentado. A procedência acompanha cada carta. A inspiração factual não transforma as pessoas ou detalhes desenhados em documentação histórica.

## Pedido de desenvolvimento

**Novas propostas:** [Mais perto do quotidiano](novos-estudos/README.md) acrescenta 12 estudos sobre trabalho, amizade, casa, ajuda e tempo. Têm catálogo próprio e permanecem fora da seleção consolidada de 140 até validação.

Criar primeiro um protótipo: **três imagens de universos diferentes, duas ligações possíveis e dois géneros de texto**. Comparar A/B, conservar a primeira tentativa e permitir revisão. Uma ligação pode ser causal; outra, analógica, descoberta durante a escrita. Não há uma sequência correta universal.

Reutilizar os controlos, navegação e caderno atuais das lições. Pistas progressivas, montagem por teclado, alternativa em papel e projeção sem respostas privadas. Nas jornadas de Cidadania, alterar perspetiva, contexto ou ação deve mudar efetivamente informação e consequências; não pontuar virtude ou concordância com o sistema.

Dar prioridade à linguagem mais crua dos conjuntos 09–15, 17–21 e 25–26. Os conjuntos cinematográficos e os mais figurativos são variantes disponíveis, não uma imposição do mesmo acabamento a tudo.

Usar **apenas `kept: true`**. Para um atlas de 1536 × 1024 em grelha 3 × 2: cada vinheta ocupa 512 × 512; `x = column * 512`, `y = row * 512`. A galeria demonstra uma implementação por CSS; não é necessário gerar outras 140 imagens para o primeiro protótipo.

## Relação com o trabalho já publicado

Esta pasta foi preparada sobre `main` em `aea224b`, depois da integração dos PRs #68 (Kafka e Corta!), #69 (créditos/licença dos desenhos da carteira) e #66 (Resultados da turma). Não substituir essas alterações pelas versões históricas mencionadas nos documentos de exploração.

Esta entrega acrescenta **apenas uma pasta de curadoria**. Não modifica páginas de alunos, Cidadania, fichas de Português, exercícios publicados ou geradores. Antes de implementar, integrar o `main` que estiver atual no ambiente do Claude e localizar as fontes geradoras correspondentes.

O `index.html` está marcado `noindex` e não foi ligado à navegação do site. A entrega em branch/PR serve para consulta e desenvolvimento; não representa a publicação de novos exercícios. Mostrar um protótipo funcional e validado antes de expandir ou publicar.

## Verificação desta entrega

As imagens passaram de 64,63 MB em PNG para 8,43 MB em WebP (menos 87%), mantendo a resolução. Conferência visual dos desenhos e ensaio da galeria em Chromium: os 140 recortes mantidos aparecem; os 16 excluídos não; os 25 ficheiros de imagem carregam localmente; sem deslizamento horizontal a 360/1440 px e sem erros de página. O ensaio não avalia ainda um jogo ou a aprendizagem em turma.
