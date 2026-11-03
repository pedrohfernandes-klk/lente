# Ideias: pedido 2, entrega delimitada

02/11/2026. Base: `e71ebf4600a11b3d2bd73abce68fa92f6be22076`.

## Resultado

A entrada pública passa à proposta A, com notas e fios, uma ação principal antes do desenho no telemóvel e o método numa secção expansível. Usa a barra real, os destinos publicados e o progresso do aparelho. O título tem um único acento gráfico sobre o segundo I; o nome acessível continua «Ideias». O desenho conserva o crédito de geração com IA.

O Laboratório deixa de mostrar pontos, incluindo os 86 motores incorporados e as duas sessões no motor partilhado. Os valores internos necessários ao progresso continuam a ser calculados. A projeção não lê nem grava progresso. As conclusões anteriores ficam em `antes`, sem transferir respostas por índice para cartões diferentes. A entrada conserva a data mais antiga de conclusão.

Os cinco passos e os três critérios por sessão têm uma fonte comum. Os critérios substituem as grelhas no guia e nos guiões e coincidem com o cartão «Na aula». O cartão final inclui «Para a tua caixa». As tarefas continuam individuais, com os mesmos produtos e regras de segurança. Não se mudam as versões pedagógicas nem a ordem das respostas de S1 e S2.

O gerador aceita, de forma opcional, «Na aula» estruturado, registo nas chaves antigas dos percursos, relógio, imagens em escolha e ordenar, citação literal delimitada e regras de contagem para sessões futuras. A citação só permite a pontuação original dentro de um bloco com fonte HTTPS e até 120 palavras; as outras regras de escrita continuam ativas. Nenhuma sessão nova é publicada neste pedido.

## Verificações locais

- 83 testes Python aprovados na ronda conjunta; os sete testes dos contratos foram repetidos após a última alteração e passaram.
- Geradores de lições e de Ideias em modo de verificação: sem diferenças pendentes.
- Cinco testes da migração; ensaios de abertura com progresso anterior e projeção, incluindo incorporação sem parâmetro na URL.
- Entrada: 27 combinações de 320, 390 e 1366 px, claro, escuro e projeção, com estado inicial, intermédio e concluído. Sem deslocamento lateral ou erro JavaScript. Ação principal no primeiro ecrã, teclado, foco, contraste, movimento reduzido e acento verificados.
- Documentos: 30 contextos; impressão do guião em quatro páginas e do guia em nove. Inspeção visual das páginas 2 e 4 do guião e 5 do guia, sem tabelas cortadas ou conteúdo em branco.
- S1 e S2: percurso completo com respostas corretas a 320 e 1440 px. Ensaio adicional do motor comum com Cidadania S01 e as duas sessões a 390 e 1366 px.
- Motores incorporados: 18 contextos nos dois formatos existentes, incluindo resposta, fim, reabertura e projeção. A transformação dos 86 ficheiros é comparada com a base fixa e é idempotente.
- Imagens e relógio: quatro contextos, teclado, resposta errada com explicação, ordenação correta, pausa e reposição do relógio, fim sem pontos e armazenamento intacto em projeção. A amostra fixa a ordem dos cartões com `aula:true`; não altera o baralhamento do produto.
- Cidadania: comparação de todos os ficheiros de `cidadania/piloto/`, `cidadania/m1/` e do respetivo CSS com `fbfb8509d6e104f00811321d95ed4d999f8df2cd`. Só se normaliza o parâmetro de cache. As dez páginas geradas só mudam esse parâmetro.

As provas locais estão em `outputs/ideias-motor-provas-20261102/` e `outputs/ideias-previsualizacao-20261102/`, fora do repositório. A segunda pasta contém a ronda final da entrada com o acento. A integração contínua executa os ensaios completos; o resultado da cabeça entregue deve ser confirmado antes de publicar.

## Correspondência entre os contratos dos testes

| Contrato anterior | Contrato aprovado em 02/11 |
| --- | --- |
| Atol, gesto com três escolhas e região «A seguir» | Uma ação principal antes das notas e fios, com começar, continuar ou rever calculado a partir do progresso real |
| Cinco passos sempre abertos e geometria em três mais dois | Cinco passos integrais em abertura progressiva, operável por Enter e Espaço, com foco visível e fonte acessível |
| Grelhas /20 e resultado numérico | Três critérios iguais no cartão, guia e guião; ausência de pontos visíveis, com progresso interno conservado |
| Estado concluído apenas na versão corrente | Estado corrente ou conclusão anterior, migração idempotente, sem reaproveitar respostas antigas |
| Crédito do atol na entrada | Crédito do grafismo atual; ficheiro e documentação do atol preservados |

Os controlos de respostas, linguagem, modalidade individual, ligações, ausência de deslocamento lateral e compatibilidade de Cidadania mantêm-se. Os controlos da composição substituída têm a decisão datada no teste; não se alargam tolerâncias para aceitar falhas.

## Limites e dependências por resolver

### Correções da primeira revisão

O CI de «formas e montagem» falhou em `test_motores_antigos_so_recebem_transformacao_autorizada`: o checkout superficial não disponibilizava a árvore da base fixa `e71ebf4600a11b3d2bd73abce68fa92f6be22076`. O trabalho `lab` passa a carregar o histórico completo. Mantém-se a comparação exata dos 86 motores; não se altera o teste nem a base.

`figuraOpcao` apresentava a imagem e o texto alternativo, mas omitia o crédito validado pelo gerador. O crédito passa a ser texto simples escapado, visível e acessível no mesmo botão. Não contém ligações ou controlos aninhados. A imagem, o crédito e a opção usam o mesmo índice e deslocam-se juntos ao selecionar, retirar e ordenar. O ensaio usa créditos e imagens identificados por amostra, confere a correspondência por `data-j`, a presença no nome acessível e a ausência de elementos interativos internos. Exige também que a amostra exerça uma ordem baralhada.

Esta entrega não cumpre o requisito dos cinco tipos `classificar`, `linha`, `escala`, `diferencas` e `estimar`. Faltam o código original e os respetivos contratos positivos e negativos em `assets/licoes/`, `tools/licoes_lente.py` e nos testes do motor. As referências `eaa33dd` e `b729dd1` pertencem a um ambiente externo sem caminho ou ramo acessível confirmado. A coordenação ficou com a recuperação; não se recriam os tipos por inferência. S1 e S2 não os usam. As sessões futuras que dependem deles permanecem condicionadas à recuperação e validação.

O visor foi ensaiado isoladamente, mas não está integrado nesta entrega. Os mapas existentes de S1 continuam a usar o motor publicado e os seus ensaios; isso não prova os cinco tipos ausentes nem constitui integração do novo visor.

A reorganização geral dos menus do Laboratório e a mudança dos títulos de Cidadania para «Humanos», «Algoritmos» e «Decisões» ficam em entregas separadas. Não se alteram aqui os repositórios de Português nem as fontes privadas. Publicação apenas depois de revisão da cabeça exata, verificações aprovadas e vez na fila.


## Confirmação incremental L106-02, 03/11/2026

O botão de pausa da amostra de teste usava `data-rl="pausa"`, enquanto o motor e os consumidores publicados usam `data-rl="parar"`. Corrigiu-se a amostra para o comando existente. O motor não mudou e conserva os comandos anteriores.

O ensaio espera pela primeira diminuição do relógio, aciona a pausa, exige a remoção de `a-correr` e confirma que o valor e o texto ficam inalterados após 1250 ms, antes de acionar Repor. A pesquisa nos consumidores encontrou 31 ocorrências de `parar` e nenhuma de `pausa` nos dados HTML não escapados; os testes antigos dos treinos também usam `parar`.

A bateria `browser_laboratorio_contratos.cjs` passou nos quatro contextos: 390 e 1366 px, normal e projeção. Mantém a prova dos créditos baralhados, do teclado e dos retornos. Esta correção não constitui aprovação global do #106.
