# Modo noturno universal

Implementação de 25/10/2026, autorizada pelo utilizador para todas as páginas dos dois sites, incluindo a apresentação de Cidadania M1. Não altera conteúdos, avaliação ou motores de progresso.

## Contrato de integração

Todas as páginas HTML completas carregam `assets/appearance.css` e `assets/appearance.js` no fim do head. O script síncrono aplica a preferência antes do corpo; os restantes scripts mantêm a ordem original. O instalador calcula caminhos relativos e é idempotente.

Depois de qualquer geração de HTML, executar:

```
python tools/install-appearance.py
python tools/install-appearance.py --check
python -m unittest discover -s tests -p 'test_*.py'
node --test tests/appearance.test.cjs
```

`tests/test_appearance_universal.py` verifica a cobertura de todos os HTML completos e a existência dos dois recursos referenciados. Não confundir esta cobertura estática com inspeção visual individual de cada página. Os geradores privados não foram editados nesta ronda: integrar esta etapa no processo de geração, sem retirar os carregamentos.

## Comportamento

- Sem escolha guardada, segue o sistema; o botão alterna entre claro e escuro. `EPIAppearance.reset()` repõe o seguimento do sistema.
- Só escreve a preferência `epi-theme`; não escreve respostas, notas ou progresso. PT e LENTE partilham origem no GitHub Pages, logo partilham esta preferência.
- As variantes escuras já existentes são ativadas/desativadas via CSSOM conforme a escolha manual. Mantêm-se as condições de largura, impressão e movimento. Folhas externas inacessíveis são ignoradas.
- Um botão de 44×44 fica no cabeçalho dos cartões/projeção ou acompanha a leitura num canto inferior. Nome acessível, foco e estado `aria-pressed` explícitos. Se o motor substituir o cabeçalho, o controlo é reposto.
- Dentro da moldura não há um segundo botão: a página acompanha o controlo da moldura por mensagens validadas, da mesma origem e do pai direto.
- Sem JavaScript, continua o desenho e a preferência automática que cada página já possuía.

## Apresentação

Paleta Cartaz: papel `#121210`, fundo `#1d1d1a`, tinta `#ecebe5`; terracota no PT, mostarda no LENTE. Adaptadores locais no recurso comum para exame, guias, provas antigas e projeção, sem reescrever os respetivos CSS originais.

O tema não aplica filtros às imagens/vídeos. Mantém os tratamentos artísticos anteriores. O QR permanece preto sobre branco. Impressão usa cores claras e esconde o botão. PDFs/PPTX descarregados são documentos próprios, apresentados pelo respetivo leitor, não páginas HTML tematizadas.

`projection.js`, `projection-launcher.js`, motores pedagógicos e dados das atividades permanecem inalterados. As três dimensões de projeção são independentes do tema.

## Trabalho concorrente

O LENTE #38 e o arquivo dependente #44 continuam separados. Esta alteração não publica as suas entradas. Ao integrar ou regenerar esses HTML, executar o instalador e os testes acima; não restaurar uma página sem o carregamento comum. A autorização universal do tema não equivale a aprovação da arquitetura em rascunho.

## Verificação e limites

Testes específicos cobrem preferência manual/sistema, armazenamento bloqueado, sincronização entre separadores, origem/pai das mensagens, frames tardios, controlo único, CSSOM e condições responsivas. Navegador: famílias de páginas dos nove módulos, Atlas, exame, Cidadania, guias, provas, diapositivos, leituras e projeção PT dentro do LENTE, com larguras 320/390/540/768/1280 e QR/três tamanhos. A mudança de tema mantém uma resposta e respetivo feedback em curso. O motor pode reiniciar uma sessão incompleta ao recarregar, conforme o seu comportamento anterior: esta alteração não cria persistência nova.

Complementares não executados: leitor de ecrã humano, impressão física, projetor da escola e revisão visual de cada HTML individual. O teste físico da nova entrada Cartaz continua pendente no #38; não é apresentado como concluído pelos ensaios do tema.
