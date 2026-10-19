# Projeção com QR — verificação de 19 de outubro de 2026

## Comportamento

`projetar/` abre as páginas existentes dentro da mesma origem. Não altera o motor das atividades nem as chaves de progresso. O QR é gerado localmente e abre a página pública normal, sem parâmetros de projeção, depuração ou fragmentos de professor. A barra aceita ligações dos dois sítios, acompanha navegação e fragmentos, permite ocultar o QR e entrar/sair do ecrã inteiro.

Entradas: páginas iniciais, mapas e módulos; no Português incluem-se também os três anos. No Lente incluem-se Narrativas, Cidadania, os dois módulos, o guia docente e Fora da página. As fichas individuais podem abrir-se pelo percurso ou colando a sua ligação no campo da projeção.

## Testes executados

- Sintaxe dos três novos scripts por repositório: aprovada.
- Nenhum ID antigo perdido, nenhum ID duplicado ou fragmento interno quebrado nas páginas alteradas. Scripts existentes preservados integralmente.
- Português M3-F18, no navegador: abertura, avanço de cartões, seleção de «Já», confirmação e feedback correto (+10 pontos). Não foi repetida a ficha inteira: o seu motor e conteúdo não foram modificados.
- Navegação Português → Cidadania através do campo da projeção: aprovada. QR e título atualizam.
- Fragmentos de Cidadania e acesso início → conjunto → projeção: aprovados.
- Ocultar/mostrar QR e entrar/sair do ecrã inteiro: aprovados.
- URL externa recusada com mensagem, sem navegar; `?debug=1#professor` removidos da ligação do aluno: aprovado.
- Largura efetiva de 322 px: sem transbordo horizontal na moldura; QR recolhido inicialmente, expande abaixo da barra e cabe na largura. Verificação de largura do painel e posição após expansão.
- Dois QR extraídos de capturas reais e descodificados por jsQR, independente do gerador: devolveram exatamente `/pt/m3/licao-m3-f18/` e `/lente/cidadania/#investigar-e-criar`, no domínio público correto. Bordo branco de quatro módulos preservado.
- Biblioteca geradora: 32 960 bytes, alojada no próprio repositório; a proveniência e a licença MIT acompanham o ficheiro. O descodificador de teste não é publicado.

## Pendências complementares

Leitura física por telemóveis numa sala, projeção a distância, leitor de ecrã real, Safari/iOS e medição formal de desempenho não executados. A validação acima não equivale a uma certificação desses ambientes. Não foi reexecutado o conjunto integral de exercícios dos dois sítios; os respetivos motores permanecem inalterados.

## Reproduzir

1. Abrir `projetar/?pagina=/pt/m3/licao-m3-f18/` ou `projetar/?pagina=/lente/cidadania/`.
2. Navegar numa página; verificar que o QR acompanha o destino e que a ligação do aluno não contém `projetar`.
3. Alternar QR/ecrã inteiro e testar a 322 px.
4. Ler o QR com uma câmara e confirmar que abre a página normal.

## Revisão de contraste

Removidas as imposições de fundo branco e tinta preta da moldura: as páginas preservam agora as suas cores e temas, evitando combinar texto do tema escuro com um fundo branco forçado. Mantêm-se letra ampliada, foco e controlos. O foco usa cor clara em tema escuro. Recarregamento da projeção de Cidadania no navegador e letra de 22 px confirmados. Tema escuro num navegador real continua pendente; não se declara essa verificação executada.
