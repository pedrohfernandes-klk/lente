# Cidadania M2: as dez sessões

28 de outubro de 2026. Construídas a partir de `docs/pedagogia/plano-cidadania-m2.md`, no mesmo molde das dez sessões do M1: abertura com uma imagem, uma pergunta e «Começar»; depois cinco passos, Recupera, Vê, Decide, Faz e Leva, um de cada vez.

## O que mudou

**Páginas novas**
- `cidadania/m2/sessoes/01/` a `10/`: uma sessão de três horas por página, com uma imagem, os cinco passos, o cartão de obra (sessões 01 a 09), a casa da sessão no mapa do Contra-feed e o registo do trabalho revisto.
- `cidadania/m2/sessoes/`: o guia do docente, com as decisões provisórias, o mapa em dez casas, a origem de cada evidência (pesos do Contra-feed), os tempos, as regras comuns e, por sessão, os tempos, a casa, o cartão de obra, a condução, a inclusão e o que fica para o telemóvel.

**Integração (idempotente, como a do M1)**
- `cidadania/m2/aulas/01/` a `10/`: uma linha no topo, «Abrir a sessão NN: Recupera, Vê, Decide, Faz e Leva». O índice das etapas ganha uma linha para as dez sessões.
- `cidadania/m2/`: a entrada do módulo abre com «Dez sessões», o botão «Começar» ou «Continuar na sessão NN» e os dez cartões, com o estado de cada sessão. O resto da página (passos, casos, contador «0 de 11», tabelas e motores) fica igual; a ligação às etapas mantém-se, por baixo dos cartões.
- `cidadania/index.html`: o cartão do M2 passa a dizer «Dez sessões: ver as regras, pô-las à prova e criar um Contra-feed.» e «10 sessões», como o do M1. O contador de passos do cartão sai, como saiu o do M1: o progresso das sessões vive na página do módulo. A chave `epi-cidadania-m2` não é tocada.
- `docente/`: uma linha para o guia das dez sessões, a seguir à do M1.

**Código**
- `tools/cidadania_sessoes_molde.py`: as peças comuns (topo, abertura, barra dos passos, cabeçalho do passo, Recupera, cartão de obra, controlos, registo, cartão de sessão, página). O M1 (`tools/cidadania_m1_layout.py`) passa a usá-las; o HTML do M1 fica igual a `origin/main`, byte a byte.
- `tools/cidadania_m2_molde.py`: o conteúdo das dez sessões, os nove cartões de obra, as dez casas, os quatro instrumentos, as cinco decisões provisórias e os créditos das imagens.
- `tools/cidadania_m2_sessoes.py`: as páginas das sessões, o guia e o bloco do índice.
- `tools/cidadania_m2_correcoes.py`: as correções dos «Riscos» do plano.
- `tools/generate_cidadania_m2.py`: gera tudo e integra (`python3 tools/generate_cidadania_m2.py`).
- `assets/cidadania-sessoes-molde.js`: o motor das sessões, generalizado a partir do do M1. Lê a chave na página (`data-chave`), pinta os estados e o «Continuar», e não grava nada em projeção. O M1 continua com o seu motor, porque o seu HTML não muda.
- `assets/cidadania-m2-sessoes.css`: só o que o M2 acrescenta ao sistema do M1 (que continua a ser a folha base): materiais numerados no Vê, o vídeo opcional, o mapa do Contra-feed, o bloco do índice e as tabelas do guia.

**Chave de progresso nova:** `lente-cidadania-m2-sessoes-v1` (`{"version":1,"sessions":{"NN":{"stage":n,"done":true}}}`), só no aparelho de cada aluno. As chaves `epi-cidadania-m2` e `lente-cidadania-m1-sessoes-v2` não são lidas nem escritas.

**Testes**
- `tests/test_cidadania_m2_molde.py`: molde, recuperação a partir da sessão anterior, mapa em dez casas, pesos iguais aos do Contra-feed, tempos, cartões de obra, escrita, ligações locais, fontes externas já presentes no Lente, chave nova, M1 igual a `origin/main`, etapas, índice, portal e guia do docente, decisões provisórias, vídeos, riscos corrigidos e geração reprodutível.
- `tests/browser_cidadania_m2_sessoes.cjs`: as dez sessões de 320 a 1440 px nos dois temas, capa e cada passo, sem transbordo nem erros; teclado; retoma depois de recarregar; registo e «Continuar»; impressão; projeção sem registo; estado inválido, armazenamento bloqueado e sem JavaScript; chaves antigas intactas; ligações locais a 200.
- Três testes existentes mudaram de propósito, com comentário datado: `test_cidadania_m2_aulas` (a fonte de Nagel passa a ser o JSTOR), `test_cidadania_percurso` (o índice do M2 carrega também o motor das sessões; os outros motores ficam iguais) e `test_videos_escolhidos` (as correções verificadas aplicam-se também ao lado de `origin/main` antes de comparar).

## Decisões provisórias, a confirmar pelo docente

Estão também no guia, cada uma marcada «Decisão provisória».

1. **As etapas.** As páginas `cidadania/m2/aulas/NN/` ficam publicadas, cada uma com uma linha para `sessoes/NN/`.
2. **A análise crítica.** É individual, com revisão em pares. A lista de casos reais é do docente; a sessão 06 diz os critérios (real, datado, duas fontes independentes, sem menores nem pessoas privadas). As páginas não trazem casos reais de exemplo.
3. **A sessão 10.** Tempos de 5, 10, 20, 125 e 20 minutos; público de outra turma ou das famílias; um espaço fora da sala, a decidir pelo docente.
4. **O manifesto.** A assinatura é livre e pode levar uma reserva escrita.
5. **Vídeos e Naufrágio.** Os vídeos «em revisão» de Ver para fazer (CHIROPTERA, v120; Hilltop, v108) e o romance *Naufrágio* não entram nas sessões. «Arte ou design?» (passo 00) e «Ler para os lados» (Como se investiga, passo 8) aparecem só como ligação, em «Depois, no telemóvel». O único vídeo das sessões, o excerto do Ford Pinto (sessão 02), é opcional, abre-se por ligação (não fica incorporado) e tem pergunta antes, pergunta depois e a alternativa escrita.

## Outras decisões (minhas, a rever)

- **O material que se observa fica à vista** (revisto a 28/10: a decisão inicial, «uma imagem por página», foi rejeitada pela revisão de design). Cada sessão abre com a sua imagem; o Vê repete-a quando ela é o primeiro material. O tear de Jacquard (sessão 01) e as duas fotografias de Lisboa, A e B (sessão 05), aparecem no próprio material, com crédito completo; A e B são cópias com nomes neutros (`img/cidadania/lisboa-1907-a.webp` e `-b.webp`) e o crédito não diz qual foi alterada. Na sessão 06, o tear volta como primeiro material («O tear de Jacquard, outra vez»), com a leitura do passo 07 que explica o título «Pedir o cartão».
- **A resposta do Recupera vem da sessão anterior.** O teste exige que as palavras de cada resposta estejam na página anterior. Para isso, quatro sínteses de «Comparar razões» passaram a dizer o que o Recupera seguinte pergunta: a definição de algoritmo (01), «falta o ponto de vista de quem a vive» (04), «esconder que a usaste e assinar o que não criaste» (05) e a diferença entre observação e interpretação (08). Na sessão 10, a segunda pergunta passou a ser sobre a peça que falta à fachada (vista na 09), em vez de repetir a primeira.
- **O passo 08 fica na sessão 09.** O plano diz que as 11 atividades ficam até à sessão 07, mas também põe o passo 08 na 09. Ficou na 09, porque prepara a mostra e o manifesto; as outras dez ficam até à 07.
- **A ordem dentro do Faz:** tarefas, revisão com outra pessoa e, por fim, «Guardar» na casa, com o mapa das dez casas à vista. A casa da sessão é a figura (preenchida); as anteriores têm contorno cheio; as seguintes, tracejado. No telemóvel, o mapa mostra só os números (o nome da casa está na linha «Guardar»).
- **O Decide mostra o protocolo do plano** em duas linhas curtas: três minutos com o cartão de decisão e uma volta sem comentários; no fim, a decisão e uma razão vencida.
- **O índice do M2** ganhou as folhas e o motor das sessões (para o «Continuar» e os estados). Nada mais muda nessa página fora do bloco marcado.
- **Sem «·» no texto das páginas novas.** Nos títulos e etiquetas usa-se «/» (como na marca «Lente / Cidadania»).

## Correções dos «Riscos» do plano

Todas em `tools/cidadania_m2_correcoes.py`, conferidas nesta sessão.

1. **Âncora partida.** O passo 00 ligava para `ver-para-fazer/#arte`, que não existe. O vídeo que a âncora queria (Joana Vasconcelos, `ver-para-fazer/v62/`) está «Em revisão» e é uma entrevista de 1 minuto sobre «Plug-in», fora do contexto do passo: a 28/10 a ligação sai (primeiro tinha passado para v62). O passo já tem o vídeo opcional «Arte ou design?».
2. **A ferramenta do feed.** `curl` a 28/10: o endereço `/pt/cidadania/ferramentas/m2-aula-01-feed/` responde com a página «mudou de endereço»; `/lente/...` responde com a ferramenta. Os passos 01, 03 e 06 e «O preço de um minuto» passam a ligar para `/lente/`.
3. **Créditos e licenças**, a partir dos registos do Wikimedia Commons e da Library of Congress:
   - Hogarth: o gravado está em domínio público e o ficheiro foi dedicado ao domínio público (CC0) pela National Gallery of Art. O passo 03 e a página das imagens dizem agora o mesmo.
   - Declaração de 1789: o registo atribui a pintura a Jean-Jacques Le Barbier (cerca de 1789, Musée Carnavalet, P809; fotografia CC0 do Paris Musées). «Autor desconhecido» sai do passo 02 e da página das imagens.
   - Chaleira da AEG: Christos Vittoratos, CC BY-SA 3.0. Entra na página das imagens, e o rodapé do índice do M2 passa a nomeá-la ao lado do Jacquard.
   - Máquina de Jacquard: «O preço de um minuto» dava a licença sem o autor; passa a «David Monniaux, 2006. CC BY-SA 3.0».
   - Lisboa 1907: a fotografia é um recorte da estereoscopia n.º 11420 da H. C. White Co., «Statue of the Duke of Terceira, Lisbon, Portugal», 1907, item 2021640877 da Library of Congress (sem restrições conhecidas). As páginas ligavam para o item 2021640870, que é «The arch, Praca do Commercio». A ligação certa passa para `investigar/passo-08/` e `etica/`; o crédito entra no passo 04 e na página das imagens.
4. **Texto alternativo em inglês** passa a português: a abertura dos dois exercícios longos, a fotografia de Lisboa em `investigar/passo-08/` e as duas versões dessa fotografia em `etica/`.
5. **Nagel.** A etapa 04 liga agora para o registo no JSTOR (já ligado na Ética, lição 2), no lugar da cópia em faculty.fiu.edu.
6. **Pergunta do passo 06.** A sessão 07 usa a do passo («Como podemos tornar visíveis as regras de um algoritmo?»). O cartão do índice não foi mexido.
7. **Glossário do M2.** Entram sinal, critério, contexto, independência, leitura lateral e viragem, com definições dos casos e passos já publicados («A regra do feed», «O contexto em falta», «O rasto da afirmação», Como se investiga, passo 8, e passo 06).

Os riscos 8 a 10 (vídeos em revisão, calendário do diário, sessões densas) ficaram nas decisões provisórias e no guia.

## O que foi cortado por falta de fonte

- Do plano, já cortados antes desta sessão e mantidos fora: Turing em 1950; a frase de Poe sobre o xadrez e o Deep Blue; Baudelaire; Dennett; o prefácio ucraniano de Orwell; Bourdieu; o duplo sentido de «sueño» no dicionário da RAE; a atribuição da *Fountain* a Elsa von Freytag-Loringhoven; o endereço do Prado.
- O endereço da Library of Congress que o plano dava para Lisboa 1907 (2021640870) estava errado; foi trocado pelo certo, depois de aberto o registo.
- O nome da personagem da reportagem de 1930 (sessão 06) ficou fora: basta o aviso «este nome ou outro que os leitores quiserem», e a reportagem tem temas adultos.
- A fotografia da fachada da EPI não entra (sem licença declarada). A sessão 09 lê o texto ao portão; quem não puder ir lê o texto transcrito pelo docente (a oficina «O manifesto na fachada» mostra a fotografia, por isso deixou de ser a alternativa).
- Os vídeos «em revisão» (v120, v108) e *Naufrágio* (decisão provisória 5).

## Pendente

- O docente confirma as cinco decisões provisórias e prepara a lista de casos reais da sessão 06.
- Ver o excerto do Ford Pinto antes de o propor (é opcional).
- Se os passos, os casos, a Ética ou Como se investiga forem gerados noutro repositório, as correções têm de passar também para lá (ou voltar a correr `tools/generate_cidadania_m2.py`, que as reaplica e avisa se o texto mudou).
- Fora deste trabalho: textos alternativos em inglês em `cidadania/m1/cid-m1-o-juri/`, `cidadania/m1/cid-m1-vida-em-direto-hoje/` (o M1 está congelado) e `projetos/contra-feed/`; a âncora `ver-para-fazer/#siza`, que também não existe, em `narrativas/oficina-espaco/`.
- Corrigido a 28/10, depois da publicação (PR de pendentes): as ligações de Orwell (o n.º 70483 do Project Gutenberg é *Children of the Lens*; passam ao Project Gutenberg Austrália, 0100011 e 0100021), a âncora `ver-para-fazer/#siza` em `narrativas/oficina-espaco/` (não há vídeo de Siza publicado), «jogador» no passo 04 e na revisão, a definição de «Suposição» e o texto alternativo em inglês de `projetos/contra-feed/`. Ficam: os textos alternativos em inglês do M1 (congelado) e a fotografia da fachada, que é do arquivo da EPI (16/10).
- Fora deste trabalho, vistos na revisão de 28/10: o endereço `gutenberg.org/ebooks/70483` (é *Children of the lens*, não *Animal Farm*) em `gigantes/triunfo-porcos/`, `gigantes/1984/`, `biblioteca/animal-farm-capitulo-2/`, `biblioteca/1984-capitulo-1/`, `sidequests/orwell/` e `sidequests/poder/`; a prova de Daumier ainda dita «litografia, 1845-1848» na página das imagens e no passo 05 (o registo diz «etching», sem data, e a prova traz «Huis clos»); a fotografia da fachada da EPI, sem licença declarada, em `narrativas/oficina-manifesto/`; «jogador humano» no texto do passo 04; a definição de «Suposição» no glossário («sem o poder confirmar»); levar ao M1 as regras de foco e de impressão que o M2 ganhou.

## Revisão de 28/10/2026 (design, texto, factos, engenharia)

Aplicado, sempre pela fonte (`tools/cidadania_m2_*.py`, `assets/cidadania-m2-sessoes.css`) e pelo gerador:
- **A sessão 05 já não dá a resposta.** O crédito de Lisboa diz «Uma das versões foi alterada por nós»; a resposta (B) e a forma de a confirmar pela fonte ficam em «Comparar razões». A página das imagens também deixou de dizer qual é; no passo 04, os textos alternativos de A e B descrevem só o que se vê.
- **Factos corrigidos:** as notas de Lovelace passam a ligar à transcrição Fourmilab (o n.º 74223 do Project Gutenberg é um número de 1886 do *Chambers's Journal*), também nos passos 01 e 07; *Animal Farm* liga ao Project Gutenberg Austrália (o n.º 70483 é outro livro); a gravura de Racknitz desenha em corte o homem escondido (leitura, instrução e texto alternativo, também no exercício longo, no passo 04, na página das imagens e no guia); Daumier fica «Huis clos, gravura do conjunto Les gens de justice», sem data; a Declaração de 1789 e Goya 43 têm textos alternativos certos; Lisboa 1907 tem a editora e o copyright do cartão; «Tradução oficial» sai da fonte do artigo 19.º; a ligação «em revisão» do passo 00 sai.
- **Página das imagens:** subtítulo «Domínio público e licenças livres»; entra a gravura de Haeckel (sessão 04); a licença CC BY-SA 3.0 leva a ligação ao texto da licença (também nas legendas das sessões 01 e 06); «jogador» sai.
- **Texto:** artigo 19.º («três ações», não «três verbos»); Recupera da 03, 06, 07, 08 e 10; Decide da 03 (instrução com verbo, linha com alternativa sentada), da 06 (frases em lista A a D, com a opinião), da 02, da 05 e da 07; linha comum «Escreve a tua resposta e uma razão»; razões dos cartões com sujeito; slogans e perguntas ambíguas reescritos; Brecht e Barthes apresentados com o que as páginas de origem dizem; frases longas partidas; calendário do diário e da análise coerente entre as sessões e o guia; sessão 08 passa a «O ensaio com público»; pergunta de abertura da 10; guia sem nomes de chaves nem caminhos e com o resumo certo das casas que voltam.
- **Design:** o foco nunca fica por baixo das barras fixas (`scroll-padding`); resumos que se abrem com «+» e «−»; no telemóvel, o botão do tema sai durante a sessão; sem JavaScript, a barra de controlo vazia não aparece; o mapa diz o estado de cada casa por palavras e tem legenda; os materiais em papel da 10 têm caixa; a capa carrega já (`eager`, prioridade alta, versão de 700 px com `srcset`); a fonte do Google deixa de bloquear a página; a linha das etapas diz a relação com a sessão e tem aspeto de ação; no índice, um só «começa aqui» (o passo 00 só se destaca depois do primeiro passo) e o título «Dez sessões» com o sistema da página; o portal mostra «N de 10 sessões registadas» (só lê a chave nova).
- **Impressão:** sem folhas em branco nem páginas quase vazias a meio; cabeçalhos dos passos inteiros e presos ao passo; o guia imprime cada sessão numa página, sem títulos órfãos.
- **Testes:** fontes externas numa lista explícita (`FONTES_EXTERNAS`) comparada com o commit base fixo; M1 comparado com a base comum (e fora quando não há `origin/main`); geração reprodutível sem sujar a árvore; Recupera comparado só com o que a sessão anterior ensina; testes novos para a resposta da 05, o guia, o portal, a fonte, o mapa e as frases da 06; no navegador, foco sob as barras, botão do tema, um só «começa aqui», portal, fonte pendurada e barra vazia sem JavaScript.
