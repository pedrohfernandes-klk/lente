# Cartazes de entrada e três inícios — LENTE

Baseline: 51a9b1911ea6a66ba65bef522dfb8e5a515e7fed. Incremento autorizado depois da publicação dos três conjuntos. Publicação continuada autorizada expressamente; testes críticos proporcionais, complementares documentados.

## Alteração

O índice de Narrativas apresenta três cartazes: Aulas, Experimentar e Vidas e ideias. Cada cartaz reúne pergunta, linguagem visual, âmbito e ação explícita. Aulas usa a sequência de Muybridge já presente; Experimentar usa três momentos em CSS; Vidas usa um pormenor das aguadas atribuídas a Galileu. A atribuição incerta permanece explícita; imagens decorativas nos links não repetem os seus nomes acessíveis. Os créditos visíveis e o percurso documental original são preservados.

No início, mantêm-se os três links compactos, com perguntas correspondentes. A ilustração histórica completa e a animação de Muybridge ficam no conjunto Aulas, depois dos seus quatro cartões, para que a navegação chegue primeiro às propostas. Nenhum conteúdo foi eliminado.

Experimentar oferece três inícios concretos, sem esconder a coleção:

- Tenho cinco minutos: Começar pelo meio; individual, cinco minutos.
- Quero comparar versões: A matriz por meio; dez minutos de preparação e sessenta minutos de aula.
- Queremos criar em pares: Escrever ficção: começar; cinco a oito minutos no ecrã, com troca de papéis descrita na proposta.

Ver todas as propostas leva à coleção existente. Os 66 cartões, catorze apoios, identificadores, armazenamento e âncoras antigas são preservados. Os três atalhos novos participam no modo de projeção através de uma extensão do seletor existente; não há nova lógica de progresso.

## Verificações executadas

- Duas verificações estáticas, uma independente: os 66 blocos de cartões são byte a byte idênticos e mantêm a ordem. Todos os destinos, IDs, atributos de progresso e scripts externos antigos preservados; IDs únicos e fragmentos existentes. JavaScript do início idêntico; única diferença no índice é acrescentar os três atalhos ao seletor de projeção.
- Curadoria independente por leitura dos destinos: os três inícios distinguem análise da ordem, comparação de versões e criação em pares. As durações distinguem preparação e tempo de aula. Imprecisões encontradas noutros conteúdos foram registadas no workspace; esses conteúdos não recebem o novo destaque.
- Navegador: Enter nos três cartazes chega ao hash e foco da secção correta. Ver todas as propostas chega ao título da coleção e ao seu foco.
- Entrada e índice em 320, 390, 768 e 1440 px: sem transbordo; alvos dos acessos testados superiores a 44 px. Composições adaptadas e imagens carregadas (1024×638 e 585×818). Capturas antes/depois em computador e telemóvel no workspace.
- Progresso em cópia QA isolada: duas de quatro aulas, seis cartões feitos e dois apoios marcados; sem alteração das chaves públicas.
- Projeção: 66 cartões e três atalhos recebem projetar=1; os cartazes mantêm os seus fragmentos.
- Consola sem avisos ou erros nos fluxos testados. Contraste calculado dos textos dos cartazes: 14,69:1, 13,93:1 e 11,82:1.

CSS próprio com cerca de 4,8 KB, carregado apenas no índice. Sem nova fonte, biblioteca ou animação. Muybridge reutiliza o mesmo URL; a única imagem adicional transferida no índice é um ficheiro existente de 85 458 bytes, com carregamento lazy. Sem duplicação de imagens no repositório. As cópias QA e auxiliares não são publicadas.

## Limites

Não se repetiram os percursos integrais dos conteúdos, cujas páginas não mudam. Leitor de ecrã real, dispositivo físico e desempenho representativo não executados. O progresso foi verificado num cenário controlado; não cobre todos os estados. Verificações complementares não apresentadas como aprovadas.

Confirmar deployment do SHA integrado e presença dos cartazes/atalhos no site público antes de declarar publicação concluída.
