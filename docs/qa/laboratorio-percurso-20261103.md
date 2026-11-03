# Ideias como entrada do Laboratório

Protótipo navegável para revisão, separado do #107 e dos pilotos de fundos. Página: `demonstracoes/laboratorio-percurso/index.html`. Não está ligada à navegação pública e tem noindex. Não altera URLs nem consulta ou escreve progresso. A barra de revisão seleciona estados simulados; o excerto não declara uma sessão completa realizada.

## Percurso concreto

1. Laboratório: uma ação principal, «Entrar em Ideias», seguida de recursos escolhidos pela necessidade atual. Na retoma, o texto lembra a pergunta deixada em aberto; na conclusão, propõe voltar ao material recolhido.
2. Ideias: o próximo passo distingue começo, retoma e conclusão. O método conserva os cinco passos de Young, com os nomes e a ordem publicados. As quatro portas dos recursos não são uma nova sequência pedagógica.
3. «Ver ou observar?»: um excerto da sessão 1 existente. A escolha produz uma explicação ou convida a reler o texto. Sem pontos, prémios ou respostas decorativas.
4. Recurso: reler a conversa de Watson e Holmes. O botão principal devolve à pergunta, conservando em memória a opção escolhida. Uma ligação secundária abre o recurso completo publicado num novo separador, identificado no rótulo.
5. Regresso: a escolha fica visível e pode ser revista. O fecho retoma a escada e o caderno da sessão publicada. A ação seguinte prepara «O cocheiro»; explorar outro recurso continua disponível.

## Hierarquia e recursos

| Porta | Necessidade | Destino existente |
| --- | --- | --- |
| Observar | Distinguir o que se vê do que se conclui | `narrativas/ver/` |
| Experimentar | Pôr uma escolha à prova | `narrativas/treinar/` |
| Relacionar | Ligar o material observado | `narrativas/ideias/sessao-02/` |
| Dar forma | Apresentar e pôr à prova | `narrativas/criar/` |

O menu Explorar é secundário. A posição no percurso fica no topo; o regresso aparece junto do recurso. As ligações para páginas publicadas permanecem intactas. A demonstração serve para aprovar o percurso antes de ligar estes estados ao motor real, que continua a ser o único responsável pelo progresso.

## Movimento

Duas notas e uma ligação representam juntar e relacionar material. Só a linha se move, lentamente; título e texto mantêm a posição. Usa o motor comum `assets/fundos.js`, com pausa, limite de dois ciclos, suspensão fora de vista e com separador oculto, movimento reduzido e projeção estática. O desenho é código SVG do protótipo, sem imagem externa nem nova fonte. Sem JavaScript há ligações diretas para Ideias e para a sessão publicada.

## Fontes e limites

O gerador `tools/laboratorio_percurso_demo.py` extrai a leitura e a pergunta de Watson do banco público existente. Não foram necessárias novas pesquisas do GPT2. A explicação para tentar novamente é uma orientação de leitura, sem acrescentar uma afirmação histórica. Os estados não persistem ao recarregar. A sessão integral, os sete percursos futuros e os cinco tipos de interação pendentes não são implementados por este protótipo.

Não houve controlo interativo. Zoom real a 200% continua fora da validação. Não publicar nem propagar antes do parecer sobre o percurso.

## Validação da entrega

27 percursos aprovados: três estados, 320/390/1366 px, claro/escuro/projeção, com seis vistas por contexto. Regresso à opção escolhida e armazenamento intacto. Mais seis contextos conferem boia sem sobreposição, Enter/Escape/foco, sinais e tokens dos resultados, ligação única ao Wordle e zero pedidos externos. Pausa, retoma e projeção dinâmica aprovadas. Gerador sem diferenças. Capturas móveis da entrada e da porta Português abertas e conferidas. Provas locais em `outputs/laboratorio-percurso-provas-20261103/`. A especificação comum foi enviada ao GPT3 após autorização direta do docente.

## Correção de contraste, 03/11

Achado do GPT3 corrigido: texto e rótulo passam à tinta principal sobre fundos tintados; só a marca e o símbolo conservam verde/vermelho. Animação de 180 ms apenas no desenho da marca, sem atenuar texto. O novo ensaio de CI mede 48 resultados em 320/390/1366, claro/escuro, normal/projeção e com/sem movimento reduzido. Texto mínimo 10,75:1; símbolo mínimo 3,82:1, acompanhado sempre de rótulo. Texto sem animação e com opacidade 1; marca estática em projeção/redução. Capturas claro positivo e escuro negativo abertas e conferidas. Provas: `outputs/laboratorio-contraste-provas-20261103/contraste.json`.


## Explorar, decisão do docente de 03/11/2026

Área secundária a Ideias, nesta mesma proposta de redesenho. Onze recursos, seleção fechada. A entrada destaca Wordle, Color e Music Lab; os restantes aparecem nas cinco categorias aprovadas. Cada ligação tem nome, ação, língua ou requisito relevante e indicação de novo separador. Nenhum recurso é incorporado ou consultado antes do clique. O retorno conserva a escolha da sessão em memória.

- Jogar com palavras: Wordle, Léxico, Elos.
- Ver e desenhar: Color, Boolean, Bézier.
- Criar com som: Music Lab, Blob Opera.
- Experimentar decisões: Polygons.
- Descobrir: Arts & Culture, RTP Ensina.

Verificação das páginas oficiais em 03/11/2026: os dez endereços além de Wordle responderam ao leitor web; Léxico e Elos apresentam uma aplicação JavaScript («A carregar…»). Wordle mantém o endereço oficial aprovado na coordenação, mas o leitor web devolveu erro de acesso. Isto não demonstra que o recurso esteja indisponível. Não se promete funcionamento completo das aplicações externas. Bézier declara expressamente teclado e rato ou painel tátil. Não se acrescentaram recursos à seleção aprovada.

As ligações verificáveis e as frases de ação ficam em demonstracoes/laboratorio-percurso/percurso.js. O teste de navegador exige os onze endereços exatos, as cinco categorias, apenas três destaques, novo separador seguro, ausência de pedidos externos e retorno ao Laboratório. Mantém também os 27 percursos, os estados das respostas, o armazenamento intacto e os limites de largura.


## Integração do main com #109, 03/11/2026

Merge 372296de0c0f5b8cb4777f3934f70760392dbbe2, com main 2f88092636389458a6ea9bf3ca9362bd42e6bb3b como segundo pai. Cabeçalho, projeção, renomeações e atributos LF preservados. Os conflitos das camadas anteriores ficaram com main; o gerador do Laboratório recebeu apenas o incremento próprio dos menus. Quatro entradas e conteúdo do protótipo regenerados sem diferenças.

A bateria Python encontrou duas falhas, ambas na demonstração: faltava o par appearance.css/appearance.js exigido em todas as páginas. Corrigido o HTML, com data-appearance-site e um lugar próprio para o controlo de tema na navegação. Nenhum teste dispensado. Os 17 testes dos dois conjuntos afetados passaram depois da correção. Os restantes 273 da execução integral anterior tinham passado; o CI repetirá a bateria completa.

Menus: 72 contextos aprovados. Percurso: 27 contextos com seis vistas, retorno à resposta e armazenamento preservado, mais os controlos, Explorar e ligações externas. Contraste após o tema comum: 48 combinações aprovadas, mínimo do texto 10,08:1 e dos símbolos 3,82:1. A demonstração continua explicitamente um excerto com estados simulados, não uma sessão completa nem uma implementação do lançador/QR.

Provas atuais: outputs/lente108-main-menus-20261103/, outputs/lente108-main-percurso-final-20261103/ e outputs/lente108-main-contraste-final-20261103/. A ampliação por CSS não certifica zoom nativo. Não foram alterados os pedidos #110/#111 nem ampliada a seleção de Explorar. Sem publicação.


## Boia comum e acessos docentes, 03/11/2026

Decisão do docente recebida durante a integração: retirar os acessos expostos «Para o docente» e reuni-los na boia fixa no canto inferior esquerdo. `assets/apoios.js` é carregado pelo ponto comum de aparência, já presente nas páginas. Move os elementos de ligação, conservando o endereço e o identificador; não elimina materiais. No interior usa «Guia do docente». Sem JavaScript, os destinos originais continuam acessíveis. As páginas sem ligação docente específica recebem o acesso geral.

O rodapé da Justiça em `olhar-e-decidir/justica/index.html` está incluído: o reconhecimento aceita «Para o docente:». Não se edita essa página, reservada ao #103. A boia tem nome acessível, alvo de 48 px, abertura por Enter, Escape com devolução do foco, espaço inferior reservado e permanece acessível em projeção. A demonstração usa a faixa inferior fixa e deixa de esconder a boia nesse modo.

`tests/browser_apoios.cjs`: 60 contextos, cinco páginas, 320/390/1366 px, claro/escuro e projeção real. Exige destinos docentes preservados, ausência de acessos com o rótulo anterior, posição fixa, teclado, ausência de transbordo e última ação/rodapé fora da boia. Os elementos de percursos fechados não são conteúdo visível; a medição usa `checkVisibility()`. Capturas em `outputs/lente108-boia-20261103/`, incluindo móvel claro e projeção escura, conferidas.

A verificação encontrou uma tabela do guião com 19 px de transbordo a 320 px em projeção. Corrigiu-se no gerador de Ideias a distribuição das colunas e a quebra de palavras apenas em projeção; regeneraram-se a entrada, o guião e o guia docente. Nenhum texto, grelha ou dimensão de impressão foi alterado.

Após o acerto: 27 percursos e 48 combinações de contraste passaram; mínimos 10,08:1 no texto e 3,82:1 nos símbolos. Os 15 testes da aparência passaram. A especificação comum foi atualizada e enviada ao GPT3 com autorização direta do docente. Não houve controlo interativo do computador nem publicação.

A bateria integral Python passou: 275 testes, 172,682 s, sem falhas. Os menus passaram nos 72 contextos; o zoom 2 deste ensaio é CSS, não zoom nativo do navegador.


### Correção após o primeiro CI da boia

Na cabeça 27d3b99, o CI detetou que a boia interceptava «Cartão anterior» e «Nova tentativa» nos visores fixos. O espaço no corpo da página não chegava à `.casca`, que ocupa a janela inteira. O componente reserva agora 88 px também nesse visor, apenas em ecrã, sem alterar a impressão. A boia usa um botão com `aria-expanded` e `aria-controls`, evitando interferência com os `details` do conteúdo. Os testes existentes não foram modificados.

Após a correção, `browser_formas.cjs` passou integralmente, incluindo o ponto exato da falha, e os 60 contextos da boia passaram novamente. Provas finais em `outputs/lente108-boia-final-20261103/`. A família Cartaz também passou antes deste acerto específico do visor. A execução local de `browser_reciclagem_lente.py` não arrancou porque o Python disponível não tem o módulo Playwright; a confirmação desse percurso fica no CI da nova cabeça.
