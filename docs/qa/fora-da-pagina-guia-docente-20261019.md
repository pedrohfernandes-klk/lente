# Fora da página e guia docente — QA de publicação

Data: 19-10-2026. Baseline LENTE: 4684bd9a2f1ec05a5adfb7ad64ec808598d69358, reconfirmada antes da publicação. Português: 2df708a2ce0529c0a933b53e0108257eb009ca25; sete novas lições já publicadas, total de 108.

## Âmbito e decisão editorial

Um conjunto novo dentro de Experimentar > Oficinas de criação > Cena, imagem e espaço. Três experiências: escultura/perspetiva; desenho ou poema-objeto/elipse; pequena tese, manifesto ou instalação/prova e revisão. Cada uma tem seis atividades fechadas com feedback e um guião de produção fora do ecrã. As situações e os diagramas são originais. Os cartões verificam raciocínios; a peça não recebe avaliação automática.

Um guia docente comum a Português e Cidadania, em HTML e PDF A4 de quatro páginas, com tempos flexíveis, caminhos por objetivo, alternativas de participação e plano sem rede. Acesso por Aulas e pelos mapas. Os tempos propostos ainda não foram ensaiados com uma turma; não são uma garantia universal.

Os 66 cartões anteriores do Laboratório mantêm exatamente o seu HTML; acrescenta-se um cartão de conjunto. Ligações, IDs e scripts anteriores conservados. Acrescentada a âncora compatível experimentar-criar dentro das oficinas: o mapa anterior e o novo regresso passam a abrir o agrupamento nativo correto. Não se deslocaram as oficinas anteriores, dossiers ou aquecimentos.

## Engenharia

Os motores casca.js/jogo.js e a folha de estilo base foram extraídos, sem alteração, da oficina-atelie existente para recursos partilhados. As três páginas novas carregam estes recursos e os seus próprios dados, em vez de repetir cerca de 100 KB de código comum em cada HTML. É uma redução de duplicação, não uma medição formal de desempenho. As páginas antigas mantêm os seus motores e dependências atuais.

A composição usa papel e carvão, traços e pontos terracota, sem grandes blocos de cor saturada. A nova folha de estilo não altera o body nem a tipografia das páginas antigas. As ligações de projeção propagam o modo entre coleção, experiência, menu e regresso.

## Executado antes de publicar

- Três percursos reais completos, 18 atividades através dos controlos: escolhas, associação/classificação, verdadeiro/falso, ordenação, lacunas e sublinhado. Feedback de acerto confirmado; resultados 6/6.
- Persistência: três estados «Cartões explorados» na coleção e novo cartão agregado marcado como explorado no Laboratório. Os dados anteriores são preservados pelo callback, que acrescenta apenas os novos IDs.
- Percurso em projeção desde o Laboratório à coleção e à escultura; erro escolhido por teclado; explicação inicialmente escondida e revelada pelo botão; menu/Escape com foco devolvido; regresso mantém projetar=1.
- Regresso do guião à âncora experimentar-criar abre as oficinas nativas. Índice do guia navega para o capítulo Português.
- Quinze verificações responsivas: coleção, guia e três experiências a 320/390/1440 px, sem transbordo horizontal, imagens quebradas ou campos de texto. As produções ficam fora do ecrã.
- Validação estática: 11 scripts sem erro de sintaxe; 485 destinos internos e âncoras conferidos contra os ficheiros publicados e novos; IDs únicos; seis atividades por sequência e respostas válidas; motores extraídos byte a byte iguais à fonte.
- PDF: quatro páginas A4; 18 ligações; acentos e colunas legíveis; todas as páginas finais renderizadas e inspecionadas. Download real pelo navegador: 26 821 bytes, SHA-256 153fe6d8b14600e6eb15f4afd923aa7905f038dcf0ae42e0cf064a99b80cb1c8, igual ao PDF da entrega. Sem erros de consola no teste do guia.

## Complementares pendentes

Leitor de ecrã real e PDF marcado para acessibilidade; Safari/iOS e dispositivo físico; medição formal de desempenho; impressão física e leitura dos QR por uma câmara; ensaio dos tempos e dos produtos com uma turma. Não se afirma que os cartões avaliem a qualidade da peça ou que o guia seja infalível. Aplicado o critério autorizado: testes críticos aprovados e complementares documentados.

## Evidência local

outputs/fora-escultura-browser.json; outputs/fora-intervalo-browser.json; outputs/fora-tese-browser.json; outputs/crossmedia-responsive-browser.json; outputs/crossmedia-static-validation.json; outputs/teacher-guide-pdf-validation.json. Capturas de computador/telemóvel e renderizações do PDF guardadas na entrega local. Não foram enviados dados de alunos para serviços externos.
