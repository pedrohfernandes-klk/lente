# Cidadania M2: projeção sem estado pessoal

03/11/2026. Camada separada sobre main 1f990b2aebe9ba4fa4043310efff3c53f63b5cc2. Os pedidos 113 e 114 permanecem intactos.

## Reprodução

Com um registo prévio de duas sessões concluídas e a sessão 01 no passo 5, abrir cidadania/m2/?projetar=1 a 320 px produziu duas chamadas getItem à chave lente-cidadania-m2-sessoes-v1 e apresentou «2 registos de trabalho». O novo teste falhou antes da correção com esse estado exato. O bloqueio de save() já existente evitava escrever, mas não evitava ler e apresentar a retoma pessoal.

## Correção

read() devolve um estado vazio em projeção antes de consultar localStorage. A mesma proteção cobre a inicialização, pageshow e storage. Em uso normal, a leitura, a gravação e a retoma mantêm-se. Não se apagam registos nem se mudam chaves.

O gerador atualiza o parâmetro de cache do ficheiro de navegação. Foram regenerados o índice, as dez sessões e o guia. A comparação integral confirma que cada uma dessas 12 páginas só muda essa referência; o conteúdo pedagógico não mudou.

## Provas

O teste browser_cidadania_m2_privacidade.cjs passou 12 contextos: 320/1366 px, normal, parâmetro de projeção e visor real, no índice e numa sessão. Semeia dados prévios, interceta leituras/escritas/remoção/limpeza da chave, exige estado visual vazio na projeção e armazenamento intacto, aciona pageshow e storage e confirma a retoma e gravação normais. Não aceita a exposição dos registos pessoais.

A bateria anterior browser_cidadania_m2_sessoes.cjs passou: 16 observações agregadas sobre dez sessões, passos, teclado, impressão, ausência de JavaScript, armazenamento inválido/bloqueado e ligações. Provas em outputs/cidadania-m2-privacidade-provas-20261103/.

A verificação automática nova executa os dois testes de navegador. Nenhum teste foi removido ou enfraquecido. CI e revisão da cabeça exata por confirmar; nada publicado.
