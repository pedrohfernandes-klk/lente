# Cidadania: quatro sessões reais, 03/11/2026

Base: main 1f990b2aebe9ba4fa4043310efff3c53f63b5cc2. Integração independente dos pedidos 108, 110 e 112, sem publicação.

## Inventário

| Sessões | Destino | Estado |
| --- | --- | --- |
| M1, 01 a 04 | cidadania/m1/licoes/01/ a 04/ | Quatro bancos revistos, 20 cartões por sessão e 14 atividades de cinco tipos |
| M1, 05 a 10 | cidadania/m1/sessoes/05/ a 10/ | Formato anterior conservado |
| M1, sessões e pilotos anteriores | Endereços existentes | Ficheiros e registos conservados |
| M2 | Endereços existentes | Sem conversão neste lote |
| Guia docente e registo breve | cidadania/m1/licoes/docente/ e guiao/ | Fontes, materiais de leitura e três linhas finais por sessão |

A sessão 01 inclui as três correções confirmadas no pedido 110, cabeça ab434f0. Os bancos 02 a 04 são os revistos pelo GPT2. Os casos inventados e as traduções estão identificados. Não se introduzem vídeos por visionar nem imagens com direitos por confirmar. A duração depende do uso em turma e não foi aferida. Apresentações e ponto de chegada são extensão, sem requisito adicional neste percurso breve.

## Progresso

Cada cartão tem identificador estável e grupo próprio. As novas chaves acrescentam a edição 20261103. Não se transferem respostas nem conclusões por índice. O mapa de 80 cartões em cidadania-m1-migracao-20261103.json conserva as referências dos bancos anteriores e os resumos criptográficos. O main tinha bancos diferentes dos usados na primeira correspondência do modelo; as duas origens ficam distinguidas e as correspondências incertas não são inventadas.

O índice lê separadamente os registos anteriores e os quatro novos. Conta apenas as quatro sessões novas; ao terminarem, permite revê-las. As sessões 05 a 10 continuam acessíveis. Projeção e visor incorporado não leem o progresso pessoal. Os registos antigos não são apagados nem escritos pelo índice.

## Geração e validação

O gerador principal aplica tools/cidadania_interativas.py no fim. As opções de edição e ampliação em tools/licoes_lente.py são optativas; não alteram as páginas anteriores. Sem JavaScript, cada sessão oferece os materiais e o registo breve. Os testes de comparação integral conservam todos os ficheiros antigos; só a transformação exata do índice e os seis ficheiros novos entram na lista fechada.

Passaram quatro testes próprios, 50 testes de Cidadania M1/M2 e 82 observações do navegador sobre o formato anterior. Na bateria Python geral, 279 de 281 passaram antes dos dois contratos antigos serem atualizados; esses contratos estão incluídos nos 50 testes repetidos com sucesso.

Cada uma das quatro sessões passou 12 contextos completos (320, 390 e 1366 px, claro/escuro, normal/projeção), com todos os cartões, 14 respostas certas, conclusão e conservação dos registos anteriores, mais seis contextos do lançador real. O índice e os guias passaram 12 contextos, além das quatro alternativas sem JavaScript. As capturas da leitura, imagens, índice e guia a 320/390 px foram inspecionadas. Sem interação com o navegador pessoal.

Provas locais: outputs/cidadania-real-s01-20261103/ a cidadania-real-s04-20261103/, outputs/cidadania-real-indice-20261103/ e outputs/cidadania-real-legado-20261103/. A nova verificação automática percorre as quatro sessões em matriz e verifica o índice.

## Por confirmar

Revisão pedagógica da integração real e resultados do CI da cabeça enviada. A auditoria das sessões 05 a 10 alimenta um lote posterior; este pedido não as apresenta como convertidas. A revisão favorável do modelo 110 não substitui a revisão desta camada.
