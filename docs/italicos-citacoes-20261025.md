# Itálicos nas citações — 25/10/2026

Correção delimitada aos dados HTML das citações: etiquetas de itálico que estavam escapadas (`&lt;i&gt;`) passam a elementos de formatação. Não se descodifica HTML genericamente e não se altera o motor.

Inventário transversal: duas páginas de Português e quatro do LENTE, 62 etiquetas (31 pares). A comparação após descodificação confirma a conservação integral do texto, grafia, pontuação e dos restantes dados. As etiquetas de abertura/fecho ficam equilibradas. A pesquisa final nos HTML dos dois repositórios não encontra etiquetas i/em escapadas.

Verificação de navegador: 28 cartões de leitura das seis páginas, montados pelo motor original numa cópia QA com seleção só das leituras. Zero etiquetas i/em visíveis, 72 elementos com estilo itálico confirmado. Este teste é das leituras afetadas, não um percurso de avaliação completo. As cópias QA têm chaves próprias e não alteram o progresso publicado.

Testes do repositório: Português 178 aprovados; LENTE 52 aprovados. Abertura/fecho de imagens, conteúdo pedagógico, respostas, URLs e chaves mantidos. Recursos de projeção e Cidadania M1 não alterados. Nenhum caminho do PR LENTE #38 coincide.

A correção ocorre no HTML publicado, sem editar os geradores externos do Claude. Na avaliação final, confirmar que regenerar estas páginas não reintroduz o escape indevido; a regra é conservar a marcação inline confiável da edição, mantendo o escape do texto não marcado. Não tornar o escape geral do motor permissivo.

Páginas: PT `m5/m5-o-pais-ou-eles/`, `m5/m5-quem-podia-ter-feito-diferente/`; LENTE `narrativas/quem-conta/`, `narrativas/desenlace/`, `narrativas/linhas-de-enredo/`, `narrativas/corta/maias/`.