# Conjuntos de aprendizagem e cartaz de Fontana

Baseline: `487dc85a7dd3ed95fbc450dafb3f713e4a39db5a` (PR #9). Âmbito: entrada do LENTE, índice do Laboratório e CSS partilhado dos cartazes. Sem alterações em Português, exercícios ou armazenamento.

## Organização

Sete cartazes abrem coleções nativas (`details`/`summary`), sem JavaScript novo. Aulas reúne Compreender a narrativa (quatro aulas originais), Ler e investigar, Ética e estética, Preparar e comunicar. Experimentar reúne ainda Explorar e observar e Criar um projeto. Vidas e ideias agrega Gigantes e Margens em Alargar referências. Os quinze recursos conservam um acesso cada, os identificadores e os destinos originais. Como se faz é ajuda de utilização; Caderno mantém portefólio e gestão do progresso; Sidequests não é limitado à rua.

Os 66 cartões mantêm ordem, atributos de ligação e estado. Apenas o interior visual de Fontana muda: pormenor do autorretrato à espineta (1577), já usado na própria leitura, a cores, com rosto visível e legenda. Reutiliza `img/narrativas/fontana-1577.webp` (1200 × 1283, 282742 bytes), carregamento diferido, dimensões declaradas. O recorte é CSS, sem novo ficheiro de imagem. Fonte original identificada na leitura: Accademia Nazionale di San Luca, Roma; fotografia ParadiseChronicle, 2024; [Commons](https://commons.wikimedia.org/wiki/File:Self_Portrait_am_Spinett_(1577)_-_Lavinia_Fontana_(Accademia_Nazionale_di_San_Luca).jpg).

## Verificações executadas

- Comparação automática antes/depois: scripts internos e externos idênticos; identificadores originais preservados e sem duplicados; multiconjunto de todos os destinos idêntico; atributos e ordem dos 66 cartões preservados; 65 interiores dos cartões idênticos. Revisão independente favorável por outro agente.
- Navegador real: sete conjuntos abrem com Enter e fecham com Espaço; abrir um segundo conjunto de Aulas fecha o primeiro. Estado expandido/recolhido exposto na árvore de acessibilidade; nenhum link aninhado no comando.
- 28 verificações de conjuntos abertos a larguras CSS efetivas de 320, 390, 768 e 1440 px: sem deslocamento horizontal; comandos maiores que 44 px. Inspeção visual no computador e telemóvel. Corrigida uma regra demasiado específica do estado aberto, que estreitava o texto a 320 px; repetidos os 28 casos após a correção. CSS publicado com nova versão de cache `20261018-4`.
- Progresso: fixture exclusivamente local antes/depois com aulas, biografia e recursos concluídos apresenta o mesmo contador, os mesmos quatro cartões concluídos e as mesmas marcas da Biblioteca e Fachada; contador continua restrito às quatro aulas de narrativa. Nenhum estado do utilizador no site público foi alterado pelo teste.
- Projeção: os 66 cartões e três entradas rápidas recebem `?projetar=1`, incluindo as aulas dentro de coleções recolhidas.
- Imagem de Fontana carregada com dimensões naturais corretas; rosto visível em computador e telemóvel. Ligação real «Como se lê» abriu o percurso público e os seus sete passos. Sem avisos ou erros de consola nas verificações locais.
- Capturas locais guardadas: Aulas antes/depois em computador e telemóvel; cartaz de Fontana depois. Fixtures e capturas não integram o site.

## Limites documentados

Não foram repetidos integralmente os percursos de todos os conteúdos preservados, nem executados testes com leitor de ecrã real, dispositivos físicos ou medição de desempenho com rede condicionada. São verificações complementares pendentes neste incremento de navegação. A verificação final da publicação e do endereço público é registada no PR após o deployment. Não é uma certificação funcional de todo o LENTE.
