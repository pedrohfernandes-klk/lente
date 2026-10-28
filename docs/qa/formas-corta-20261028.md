# Laboratório de formas / Corta! — proposta para validação

Data: 28/10/2026. Repositório Lente; base `2157bc0f53e0d7cfb5fe4169775698c784624eb6`. Branch `codex/lente-formas-corta`. Sem publicação ou merge.

## Problema e resposta

O utilizador identificou dois problemas no Corta!: a troca de ordem não produzia uma descoberta interessante e a instrução era pouco clara. A nova mesa trabalha curiosidade, suspense, surpresa e julgamento, com quatro momentos explícitos: observar, montar com uma intenção, comparar A/B e transferir para escrita/reflexão.

O material é uma cena visual autoral, em quatro desenhos simples. A perda, o olhar, a recolha e a devolução de uma carteira permitem distinguir ação observada de intenção inferida e observar quando a informação é revelada. Não se apresentam os desenhos como fotogramas de um filme ou como adaptação de uma obra.

Cada missão contém uma alteração delimitada, controlos de adicionar/retirar/mover sem dependência de arrastar, proposta opcional para experimentar, navegação manual pelos planos, hipótese inicial e confronto com uma leitura fundamentada. A aplicação reconhece a possibilidade de efeitos diferentes: não promete que toda a pessoa terá a mesma surpresa ou o mesmo julgamento. Os selos exigem uma tentativa e reflexão, ou confirmação de registo em papel; não medem domínio semântico nem equivalem a uma nota.

## Organização do laboratório

O título da entrada passa a «Laboratório de formas», como proposta de âmbito para revisão. Mantêm-se Academia, Ginásio e Ateliê, os seus identificadores e os trinta treinos. Acrescenta-se uma entrada por intenção: montagem, leitura/criação com obras e mesa de pesquisa com pontes para Português. As oito cenas literárias continuam acessíveis pelo Corta! existente e pelas suas rotas antigas. Não foram reescritos os exercícios antigos nem migradas as chaves de progresso.

O PR de reestruturação geral #38 é trabalho independente. Esta proposta não altera a entrada principal do Lente nem pretende substituir a organização global em discussão.

## Conteúdos e dupla utilização

Três experiências prontas de leitura e escrita partem de fontes breves consultadas: Kafka (tradução editorial de Helena Topa), Mia Couto (original em português de Moçambique, numa edição brasileira que declara manter a grafia moçambicana) e Cesariny (verso divulgado pela editora). As comparações e tarefas são autorais, separadas das citações.

O corpus de dez referências inclui ainda Pacheco, Gógol, Vian, Borges, Lynch, Wells e Celine Song. Cada entrada declara o que foi efetivamente consultado, a edição/tradução, a localização, a condição de acesso e o próximo passo. Vídeo catalogado não é declarado reproduzido; edição identificada não é declarada texto consultado. Não houve compras de livros nem aquisição de direitos. Ver `curadoria/README-formas.md` e `assets/formas/corpus.json`.

Os módulos e utilizações em Português são sinalizações para revisão docente. Não se editaram fichas do repositório PT. A consulta integral necessária e a correspondência curricular devem preceder qualquer nova ficha.

## Design e ilustração

Foi descartada a primeira proposta de colagem, a pedido do utilizador. A versão integrada usa line art simples, linguagem de zine, fundo claro e apontamentos vermelho/verde. Não foi acrescentada pixel art depois da clarificação do pedido. O sprite é apresentado por recorte CSS, sem modificar os ficheiros gerados. O desenho tem legendas textuais completas e as experiências funcionam sem depender da leitura visual.

Ferramenta: imagegen integrada. Ficheiro: `assets/formas/carteira-linha.png`. Brief final: quatro vinhetas iguais, traço preto simples e irregular sobre papel marfim, sem colagem/fotografia, carteira vermelha e casaco verde; perda, observação, recolha e devolução; sem letras ou números. Trata-se de imagem assistida por IA, identificada no rodapé.

## Estado, projeção e papel

- Chave nova `lente-formas-corta-v1`, apenas versão e identificadores das experiências registadas. Nenhuma chave antiga é escrita.
- Hipótese, texto de criação e reflexão ficam apenas em memória. Exportação local opcional em texto simples. O ecrã avisa para copiar/exportar antes de sair.
- Projeção oculta textos pessoais e reduz a introdução; a comparação e as explicações mantêm-se controladas pelo docente.
- Impressão gera proposta e linhas de escrita, sem respostas pessoais, soluções ocultas ou dados de progresso.
- Falha de armazenamento não bloqueia o percurso. Conteúdo livre é escapado antes de entrar no HTML.

## Verificações

- 93 testes Python passaram (90 existentes + 3 novos), com `PYTHONUTF8=1` no Windows.
- JavaScript verificado com `node --check`; `git diff --check` sem erros.
- Playwright/Edge: quatro percursos completos em 360/1440 px; montagem, mover/retirar, restrições pedagógicas, comparação, revisão de resposta, teclado, registo idempotente, recarga, conservação da chave antiga, privacidade em projeção/impressão, três casos prontos e dez referências, texto conservado ao mudar de filtro, ligações de entrada e oito destinos preservados. Sem erros de página.
- As capturas de revisão e os exports ficam fora do repositório; a CI de PR repete os contratos do laboratório e o percurso em Chromium.

No primeiro ensaio, o checkout Windows revelou falhas de comparação byte a byte por CRLF e uma descodificação de subprocesso. O ficheiro gerado por um teste foi reposto com o conteúdo de HEAD; a execução com UTF-8 passou. Não se alterou Cidadania para resolver esses ensaios.

## Limites e validação seguinte

Não foram executados testes com alunos, leitor de ecrã real ou projetor físico. As imagens de line art devem ser aprovadas pelo docente. As quatro missões partem de um único caso visual para controlar variáveis; uma expansão deve acrescentar cenas e meios, com descoberta pedagógica própria, em vez de trocar apenas a decoração.

A nova mesa melhora o Corta! sem afirmar que os oito exercícios antigos foram todos redesenhados. O passo seguinte é aplicar a abordagem a obras concretas consultadas: selecionar excerto, definir uma pergunta, preparar duas versões e pedir evidência do efeito. Os autores ainda em pesquisa não devem passar a «prontos» por mera identificação bibliográfica.

Não há gerador de fontes do laboratório neste checkout. Se existir um repositório autoral separado que publique estas páginas, as alterações de entrada devem ser transpostas para esse gerador antes de o voltar a executar, para evitar sobrescrita.
