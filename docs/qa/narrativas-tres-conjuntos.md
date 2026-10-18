# Narrativas: três conjuntos reais

Baseline: d58b5b58e44c98965baf4027c673d88f2f6a25b9. Alteração autorizada neste pedido: reorganizar os acessos ao Laboratório e substituir o nome coletivo «Dossiers». Sem merge ou publicação.

## Estrutura

- Aulas: quatro percursos existentes.
- Experimentar: 13 exercícios, oito Corta!, 20 oficinas e 15 aquecimentos. A ligação de apoio «Dar forma às palavras» permanece.
- Vidas e ideias: os seis percursos documentais, com os mesmos destinos e sem lhes acrescentar questionários.

Os três acessos da página inicial e da navegação do Laboratório levam a secções identificadas do índice existente, não à primeira página de cada coleção. As páginas individuais, identificadores e chaves de progresso são preservados. O nome coletivo muda no acesso e no índice; os textos e títulos internos dos seis percursos não são reescritos neste lote.

Só duas páginas HTML e uma folha de estilos própria são alteradas. A folha partilhada continua intacta. Não se cria uma quarta área curricular nem se altera Cidadania ou Português.

## Verificação estática independente

66 cartões identificados preservados; mesmos destinos e atributos de cada cartão. As âncoras antigas, incluindo corta e aquecimentos, mantêm-se. IDs únicos e destinos dos novos fragmentos existentes. Seis scripts inline idênticos e com sintaxe válida; scripts externos e recursos antigos preservados. O único recurso adicional é o CSS deste acesso. Hierarquia H1, três H2, e H3/H4 nos subgrupos.

## Testes no navegador

- As três ligações da entrada foram ativadas por Enter. Hash e foco chegam às secções certas; contagens observadas: quatro, 56 e seis cartões.
- As duas páginas foram abertas em janelas de 320×568, 390×844, 768×1024 e 1440×900. Sem transbordo horizontal; os três acessos têm altura superior a 44 px em todos os casos. A largura útil do documento desconta a barra de deslocação vertical.
- As âncoras antigas corta e aquecimentos continuam a apresentar os títulos corretos.
- Dados de teste locais controlados, em cópias QA não incluídas no PR: antes/depois mostraram duas de quatro aulas, a mesma próxima aula e seis marcas de conclusão distribuídas por aulas, exercício, Corta!, aquecimento e leitura documental. A entrada mostrou as mesmas quatro peças guardadas nos dois casos. As chaves do site público não foram tocadas.
- Modo de projeção: os 66 destinos recebem projetar=1 e os três acessos de conjunto mantêm os fragmentos próprios.
- Nenhum aviso ou erro de consola capturado nesses fluxos.

Capturas antes/depois de computador e telemóvel e registos JSON estão no workspace de revisão. As cópias QA, scripts auxiliares e capturas não são publicados por este PR.

## Limites

Não foram repetidos os exercícios dos 66 conteúdos: as suas páginas não mudam. Leitor de ecrã real, telemóvel físico, falhas de rede e medição de desempenho não certificados neste lote. A preservação do progresso combina identidade do código com um cenário controlado; não equivale a testar todos os estados de armazenamento. Aprovação expressa necessária antes de merge e deployment.
