# Passagem ao Claude Code — Cidadania M1

Este ramo é trabalho em curso, enviado a pedido do utilizador para permitir a continuação no Claude Code. Não está pronto para merge ou publicação.

Base: `66dc1b818e6f99ed1b0bddf7b5d4f7b5cca59f0d`.

## Decisões atuais do utilizador

- Estrutura principal de dez sessões. A tarefa Pergunta Humana é realizada apenas na sessão 03, por sete grupos.
- Preservar integralmente o enunciado já partilhado em `cidadania/projeto/index.html`, os critérios e pesos. O conteúdo coincide com a base Git; não o substituir pelo enunciado da oficina posterior.
- Sessão 03: orientação 10 min, enunciado 5, investigação 60, preparação 35, apresentações/defesa/transições 70 = 180 min. Sete grupos, até 8 min de apresentação + 1 de defesa + 1 de transição.
- Caverna, Sísifo, CHIROPTERA, Abramović, The Egg e Truman fazem parte do contexto conhecido. Não repetir ao aluno frases administrativas como «são conhecimentos prévios», «já estudámos» ou «não há novo visionamento». Esse contexto pertence à condução docente.
- Oficina posterior: argumento narrativo e guião original para teatro, cinema ou áudio, com convenções, diálogos, indicações, fontes e revisão. Apresentação comentada sem encenação obrigatória nesta oficina, distinguindo-a da tarefa publicada.
- Justiça central; quatro cápsulas de história do teatro integradas em tarefas; referências breves e biblioteca completa.
- Continuar as lições de Justice e desenvolver equivalentes de Ética e Estética a partir dos recursos existentes. Auditar antes de ampliar. Usar fontes identificadas, casos, razões, objeções e revisão; não classificar uma posição moral como resposta única.

## Direção visual confirmada por widget

1. Abertura com imagem, pergunta curta e «Começar».
2. Um momento de cada vez; cinco passos visíveis e Anterior/Seguinte.
3. Cartaz editorial: números fortes, imagens selecionadas, linhas e poucos blocos.

O utilizador pede Gestalt minimalista e brutalista, identidade EPI/LENTE, um «edge» visual quando tiver função e atenção especial a UX/UI. Reduzir texto e navegação concorrente; aproximar ação e material; preservar acessibilidade, teclado, impressão, temas, projeção e progresso.

## Estado exato desta passagem

Há uma versão anterior gerada das dez sessões. A revisão editorial mais recente foi iniciada mas **não foi concluída nem validada**:

- `tools/cidadania_m1_editorial.py`: textos concisos, perguntas e tarefas para as dez sessões.
- `tools/cidadania_m1_layout.py`: novo gerador da abertura, cinco momentos, biblioteca e apoio à escrita.
- `tools/cidadania_m1_sessoes.py`: dados e planeamento; aplica a camada editorial e chama o novo layout.
- `tools/generate_cidadania_m1.py`: ponto de geração; a antiga constante extensa do enunciado da oficina foi retirada.
- `assets/cidadania-m1-sessoes.js`: alterado para abertura → cinco momentos.
- `assets/cidadania-m1-sessoes.css`: ainda precisa de ser alinhado com o novo layout; a tentativa de concluir a revisão foi interrompida pelo limite da revisão automática de ferramentas.
- Os HTML gerados **podem ainda corresponder à versão anterior**, enquanto o JS já espera o novo layout. Não interpretar o estado atual da pré-visualização como resultado final.
- Os testes de navegador e algumas expectativas Python ainda refletem a interação anterior («Conduzir por momentos», sem abertura). Atualizá-los às decisões confirmadas, mantendo verificações reais de preservação.

Os resultados anteriores de 71 testes Python e 82 observações de navegador pertencem à versão anterior à última revisão editorial. **Não validam o estado deste commit.**

## Próximos passos

1. Ler os geradores e harmonizar HTML/CSS/JS. Executar `python -B tools/generate_cidadania_m1.py` e corrigir os problemas encontrados.
2. Rever especialmente a sessão 03: ações curtas, pergunta/fonte/resposta claras, enunciado acessível, sem texto administrativo sobre o que os alunos já conhecem.
3. Concluir acabamento editorial e Gestalt; verificar imagens, contraste, hierarquia e leitura em projeção e telemóvel.
4. Atualizar e executar testes de fluxo, teclado, retomada, impressão completa, armazenamento indisponível, modo sem JavaScript e projeção sem escrita no progresso individual.
5. Confirmar que `cidadania/projeto/index.html` mantém o conteúdo Git original e que M2, recursos e chaves antigas não foram alterados indevidamente.
6. Continuar Justice e equivalentes de Ética e Estética, apresentando alterações e validação para revisão.

## Comandos e preservação

- Testes Python: `python -B -m unittest discover -s tests -p 'test_*.py'`.
- Teste de navegador: `tests/browser_cidadania_m1_sessoes.cjs` (Playwright; usar instalação disponível no ambiente).
- Estado novo das sessões: `lente-cidadania-m1-sessoes-v2`. Não apagar nem converter automaticamente as chaves antigas.
- O percurso integral anterior está em `cidadania/m1/percurso-anterior.html`; as 18 fichas permanecem como apoio, não como navegação principal.
- A imagem horizontal da entrada de Cidadania na página principal usa Wright of Derby, extraído dos materiais existentes, com origem e créditos; conservar.

O push deste ramo foi autorizado expressamente. Não fazer merge nem publicar o site sem autorização posterior.
