# Videoteca «Ver para fazer» — organização e leitor
**Proposta para Português e Lente · 17 de outubro de 2026**

## Decisão recomendada

Criar uma videoteca editorial única, preferencialmente sediada no Lente e referenciada nas lições de Português. Usar YouTube na primeira versão, com o leitor oficial incorporado e uma ligação de alternativa ao original. O valor do repositório está no objetivo, na seleção e no exercício que acompanha cada vídeo.

Não recomendo descarregar vídeos para os alojar nos repositórios. A primeira versão pode ser estática, com catálogo JSON e páginas geradas, sem contas ou base de dados. Guardar metadados e autoria, não ficheiros audiovisuais de terceiros.

Esta entrega cria uma base documental local. **Não foi criado um repositório público no GitHub, nem alterado ou publicado código dos sites.**

## O que foi verificado, exatamente

1. Foram identificados 50 vídeos diferentes, com IDs YouTube distintos.
2. Os 50 endereços foram abertos no navegador e apresentaram os títulos esperados.
3. Foram consultados contexto editorial e descrições; para várias atividades foram também lidas instruções ou transcrições de apoio.
4. No vídeo 50, foi observada a opção oficial Embed, o código do iframe e a pré-visualização do leitor.
5. A tentativa de testar incorporação em série ultrapassou o limite de tempo da ferramenta. Não existe, por isso, confirmação de incorporação para os restantes 49, nem de reprodução no domínio dos sites.
6. Não houve visionamento audiovisual integral dos 50 vídeos. A disponibilidade de legendas PT, a sua qualidade, os excertos adequados e eventuais restrições na rede da escola continuam por validar.

As durações conhecidas vêm da interface ou do catálogo de transcrições; as outras ficaram vazias. Uma duração lida durante publicidade pode corresponder ao anúncio: não deve ser registada automaticamente como duração do vídeo.

A seleção é uma curadoria argumentada, não uma classificação objetiva dos 50 melhores vídeos da Internet. Não preencher o número com conteúdo medíocre é uma regra editorial; também é necessário evitar a falsa certeza de uma auditoria integral que não aconteceu.

## Organização que ajuda a escolher

Nome proposto: **Ver para fazer**.

Cinco portas iniciais:
- **Contar:** personagem, estrutura, descrição e suspense.
- **Compor:** forma, cor, escala e enquadramento.
- **Experimentar:** materiais, objetos, regras e variações.
- **Observar:** lugar, detalhe, imagem, som e investigação.
- **Montar:** sequência, tempo, som e apresentação.

Cada vídeo pode aparecer em mais de uma porta através de etiquetas. O JSON mantém uma categoria principal para gestão editorial. Não duplicar fisicamente a ficha.

Filtros prioritários: competência; modo de trabalho; materiais/equipamento; língua e apoio disponível; duração do vídeo apenas quando confirmada; duração estimada do exercício. Criar uma vista para o docente com os estados de revisão. Não expor aos alunos uma etiqueta enganadora de «verificado» quando apenas a ligação foi verificada.

Ficha curta no catálogo:
**Mobiliário que comunica** — Christoph Niemann
Espaço · Desenho · Papel e lápis
«Como se desenha um conflito sem desenhar pessoas?»
**Ver e experimentar →**

Na ficha completa: título original, autor/canal, fonte, objetivo, instrução de observação, leitor, tarefa, produto esperado e critério de qualidade. Manter o nome do autor visível. Uma nota editorial em português não substitui legendas.

## O leitor no próprio site

**Sim, recomendo-o**, porque permite manter juntos o vídeo, a pergunta e a atividade. Deve usar o leitor oficial do YouTube, não um leitor HTML de um ficheiro extraído.

### Antes de carregar
Apresentar capa local autorizada ou painel tipográfico, autoria e botão «Carregar vídeo do YouTube». A informação deve explicar de forma breve que o vídeo é servido por um serviço externo. O iframe e os recursos externos associados só devem carregar depois da ação de carregar. Não antecipar ligações ou miniaturas remotas se se pretende adiar os pedidos ao YouTube.

### Durante
Um leitor de cada vez, com controlos, teclado e ecrã completo. Sem autoplay. Formato adaptável e dimensões que respeitem os mínimos do fornecedor; a documentação indica pelo menos 200 × 200 px. Uma janela muito estreita pode precisar de altura mínima em vez de seguir 16:9 rigidamente.

A pergunta fica fora do leitor, em texto real:
«Observa como a posição das cadeiras sugere uma relação. Que mudança altera mais a interpretação?»

### Depois
Apresentar uma ação do nosso percurso:
**Agora experimenta — três disposições, três relações.**
A passagem a «concluído» deve depender da atividade ou de uma confirmação do aluno; atingir o fim do vídeo não prova aprendizagem.

Manter sempre «Abrir no YouTube» e uma alternativa pedagógica em português para quando o vídeo não pode ser visto. Uma explicação nossa pode cobrir o objetivo, sem reproduzir integralmente conteúdos protegidos.

## O que o YouTube permite e o que não devemos prometer

O modo de privacidade reforçada usa youtube-nocookie.com e reduz personalização. Não significa ausência de comunicação com a Google nem garante ausência de anúncios. O YouTube permite ao proprietário limitar a incorporação; conteúdos com restrição etária podem exigir saída para o YouTube. Fonte: [ajuda oficial de incorporação](https://support.google.com/youtube/answer/171780).

É possível solicitar legendas, selecionar língua de interface e definir início/fim de um excerto. Isso não cria legendas nem garante a existência de tradução. rel=0 restringe recomendações ao mesmo canal, sem as eliminar; modestbranding está descontinuado. Fonte: [parâmetros oficiais](https://developers.google.com/youtube/player_parameters).

Não tapar controlos, marcas, publicidade ou recomendações com elementos nossos. O desenho da ficha envolve o leitor e não o adultera. Fonte: [requisitos do serviço](https://developers.google.com/youtube/terms/required-minimum-functionality).

Para incorporação, prever erro 100 para vídeo removido/privado, 101/150 para incorporação recusada e 153 para falta de identificação por Referer. Preservar a identificação de origem; uma política no-referrer pode causar problemas. Fonte: [referência da IFrame API](https://developers.google.com/youtube/iframe_api_reference).

O Player for Education oferece uma experiência sem publicidade e recomendações em plataformas educativas que o tenham adquirido e adotado. Não é uma opção que possamos simplesmente ativar num site GitHub Pages. Vale a pena verificar se a escola já dispõe de uma plataforma aderente. Fonte: [YouTube Player for Education](https://support.google.com/youtube/answer/18481571).

## YouTube apenas?

**Na primeira versão, sim.** Há suficiente qualidade e um único fornecedor simplifica operação e manutenção. A variedade deve vir dos artistas, das linguagens e dos exercícios.

Na estrutura dos dados, manter provider e URL de origem separados do ID interno. Isso permite acrescentar uma fonte institucional no futuro sem alterar as lições. Não incluir outro fornecedor apenas para aumentar o catálogo.

Limitações atuais da seleção:
- Predominância de inglês; não foi encontrada e validada uma seleção equivalente em português neste trabalho.
- Forte presença de The Art Assignment, intencional pela adequação dos exercícios, mas a diversidade geográfica e de práticas deve continuar a ser revista.
- As análises de cinema não equivalem a tutoriais; precisam de mediação e tarefas.
- Alguns vídeos técnicos requerem oficina; a adaptação escolar deve ser identificada.
- A acessibilidade deve ser conferida vídeo a vídeo e tarefa a tarefa.

## Ligações pedagógicas concretas a testar

| Origem da lição | Vídeo | Tarefa de ligação proposta |
|---|---|---|
| Português M1 — voz e relato | 06, descrição; 41, legenda | Distinguir o que a imagem/texto mostra e o que a legenda acrescenta |
| Português M2 — teatro vicentino | 02, personagem; 22, encenação; 33, mobiliário | Dispor personagens e objetos para sugerir estatuto ou conflito |
| Português M3 — épica | 08, modelo do herói | Aplicar e criticar o modelo; identificar o que ele não explica |
| Português M5 — narrativa do século XIX | 03, estrutura; 07, suspense | Reorganizar um episódio e justificar o efeito da informação adiada |
| Português M6 — poesia e cidade | 06, descrição; 17, detalhe; 43, observação | Selecionar detalhes do espaço urbano e justificar uma interpretação |
| Português M7 — vozes e perspetivas | 27, paisagem; 33, mobiliário | Representar uma perspetiva sem a reduzir a um conjunto de adjetivos |
| Lente — oficina de espaço | 22 e 33 | Planta simples da cena e três disposições |
| Lente — investigar | 16, vídeo-ensaio; 26, representação; 39, notícia | Separar prova, escolha de enquadramento e inferência |
| Lente — texto-imagem | 30, livros; 41, legenda | Produzir duas montagens com efeitos diferentes |
| Lente — projetos/cartaz | 37, flyer; 48, associação | Idear, reduzir texto e testar a leitura do cartaz |
| Lente — cidade | 35, textura; 43, lugar; 45, escuta | Construir um registo multimodal de um espaço acessível |
| Lente — narrativas | 50, animação | Testar um princípio em papel antes de usar software |

Estas relações são propostas; não afirmam que já haja um exercício equivalente publicado em cada módulo. A validação curricular cabe ao desenho da aula.

## Modelo de ligação a lições

O vídeo recebe um identificador permanente, por exemplo vid-033. Uma lição referencia esse ID e acrescenta a sua pergunta, tarefa e, se necessário, um excerto. O mesmo vídeo pode servir várias lições sem perder uma fonte única de autoria, estado e revisão.

O excerto pertence à relação vídeo–lição: para um objetivo podem interessar dois minutos, para outro o vídeo completo. Não atribuir intervalos de tempo sem rever o conteúdo. Conservar acesso à fonte integral.

## Aprovação e manutenção

Fluxo proposto:
**selecionado → ligação confirmada → conteúdo e legendas revistos → leitor testado → aprovado para uma turma/objetivo → publicado**.

No ficheiro entregue, os 50 estão em rascunho editorial. A confirmação de título não promove automaticamente uma ficha a «aprovada».

Antes de publicar cada ficha:
- Rever integralmente áudio e imagem; assinalar linguagem, violência, nudez artística ou outros elementos relevantes ao uso concreto, quando presentes.
- Confirmar legendas, qualidade linguística e alternativa acessível.
- Confirmar duração, capítulos ou excerto.
- Testar o leitor no domínio e na rede escolar, incluindo telemóvel.
- Experimentar a tarefa e ajustar materiais, tempo e critérios.
- Guardar data, nome do revisor e contexto da aprovação.

Rever a disponibilidade no início de cada período e quando houver erro reportado. Essa revisão periódica é uma recomendação; não foi criada qualquer automação.

Não guardar classificação individual com base em telemetria de visualização. Para avaliar o projeto, observar se o vídeo ajuda a compreender e a produzir: qualidade do trabalho, necessidade de ajuda e capacidade de transferir a ideia. Mais minutos de reprodução, por si só, não constituem sucesso.

## Primeiro lançamento proposto

Fazer o piloto com dez fichas: **02, 06, 22, 30, 33, 35, 37, 41, 48 e 50**. Selecionar o excerto do vídeo 50 após revisão, aproveitando os capítulos do autor. Validar com duas ou três atividades e só depois expandir.

A primeira entrega técnica deve ser pequena: um catálogo, uma ficha, um leitor comum e duas ligações a aulas. Esta entrega não implementa essas alterações; prepara-as para decisão e execução posterior.
