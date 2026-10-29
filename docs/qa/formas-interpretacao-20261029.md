# Laboratório: interpretação e revisão — 29 outubro 2026

## Estado partilhado com Claude Code

Continuação do rascunho #63, branch `codex/lente-formas-corta`. Integra `origin/main` em `6362b3f` por merge, sem conflitos. A verificação remota de 29 outubro manteve esse estado e o PR aberto, em rascunho, sem merge. Não há publicação autorizada.

Esta revisão incide em `assets/formas/`, nas duas páginas novas `narrativas/formas/` e `narrativas/corta/mesa/`, no teste de navegador e na respetiva CI. Não altera a oficina do espaço, Cidadania, as fichas de Português ou o sistema geral do site. As alterações anteriores à entrada do laboratório continuam no PR.

Para continuar no Claude Code: obter a versão atual da branch, verificar diferenças locais e integrar os commits antes de editar. Não substituir a branch pelo `main`, não copiar por cima um HTML antigo e não regenerar páginas a partir de fontes desatualizadas. `corpus.json` conserva o registo documental; `leituras.js` contém a orientação pedagógica autoral; `obras.js` gere o percurso; `interpretacao.css` acrescenta a apresentação. A ordem de carregamento é importante: guias antes do motor.

## O que mudou

Cada uma das três obras com excerto consultado tem quatro níveis, livremente navegáveis:

1. Observar: selecionar expressões do próprio excerto, distinguir evidência e inferência.
2. Interpretar: confrontar duas hipóteses defensáveis, respetivos apoios e limites; justificar e declarar o estado da hipótese.
3. Contrapor: enfrentar uma objeção, escrever uma resposta e revelar uma pista opcional.
4. Criar e rever: alternar duas frases autorais, produzir uma tentativa, conservá-la e escrever uma revisão; retomar a interpretação inicial.

O foco fica numa obra de cada vez. Textos e escolhas mantêm-se ao circular por níveis, obras e filtros. Recomeçar pede confirmação se houver texto. A primeira tentativa conservada não é substituída pela versão revista. Não há classificação automática nem persistência dos textos após recarga. Projeção oculta o material pessoal.

No Corta!, a comparação A/B inclui «vejo / sei / suponho», calculada apenas sobre o prefixo já percorrido em B. O conhecimento de A é explicitamente reconhecido para não fingir que o mesmo espectador esquece o que viu. Uma versão C permite retirar um plano de B e percorrer a sequência resultante; B não é alterada. Pistas por ausência interrogam contexto, elipse, ritmo e juízo. Os selos continuam a registar prática, não domínio interpretativo.

Mantêm-se a line art simples, o papel marfim, dois apontamentos retro e a hierarquia editorial. Não foram geradas novas imagens ou acrescentada colagem.

## Fontes e limites pedagógicos

Não se acrescentaram citações ou traduções. Os guias partem dos excertos já consultados de Kafka, Mia Couto e Cesariny. A pertença de cada expressão ao excerto é verificada nos testes. O verso de Cesariny continua sem identificação de poema/página; o percurso avisa desse limite e não inventa contexto. Gógol, Vian, Pacheco, Borges e cinema continuam candidatos documentados, sem os transformar em atividades prontas por mera existência de uma referência.

As tarefas são formativas e autorais. Não são itens IAVE nem grelhas oficiais. O desenvolvimento posterior deve privilegiar mais texto contextualizado e casos com uma descoberta própria, em vez de atribuir interpretações totais a citações de uma frase.

## Verificação e continuação

Contratos específicos: 3 testes de fontes e dependências, 12 testes do laboratório existente e 2 de aparência passaram. Navegador Chromium: quatro missões e três obras com quatro níveis a 360/1440 px; seleção por teclado, restrições de montagem, versão C, ausência de informação futura na análise de B, revisão, conservação entre filtros, cancelamento de reinício, conteúdo escapado, projeção e impressão, chaves de progresso antigas e navegação preservadas. Sem erros de página.

A execução geral reuniu 123 testes: 120 passaram inicialmente; duas falhas de comparação byte a byte em Cidadania foram resolvidas no reensaio de 7 testes após normalização das quebras de linha. Resta `test_m1_igual_a_origin_main`, que compara caminhos POSIX do Git com caminhos Windows de `Path`. Não se corrigiu um teste de Cidadania nesta revisão. O ficheiro reescrito pelo ensaio gerador foi reposto em HEAD, sem o incluir no PR.

As demonstrações HTML autónomas e as capturas são entregues fora do repositório. Sem ensaio com alunos, leitor de ecrã real ou projetor físico. Próxima validação docente: dificuldade das objeções, valor da revisão e suficiência do contexto de cada excerto. Só depois decidir integração/publicação e expansão a novas obras.
