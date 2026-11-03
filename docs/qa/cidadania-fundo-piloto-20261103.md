# Cidadania: piloto de fundo em Algoritmos

03/11/2026. Base #107, `315c8432ce02bc1e5b5ddc621d32934ad3754cdc`. Alteração separada do #106, dos menus e da sessão-modelo. Apenas a abertura de `cidadania/m2/` recebe o piloto.

## Desenho e função

Três sinais entram numa grelha; um traço percorre lentamente uma ligação entre a entrada e uma saída. O esquema introduz visualmente o encaminhamento por uma regra. Não pretende representar o funcionamento de uma plataforma real. O pequeno quadrado mostarda liga a proposta à gramática gráfica do sítio; o esquema de percursos distingue este motivo da lupa do Lente.

O fundo é transparente, esbatido nos bordos e atenuado sob o texto. Título, subtítulo, texto e controlos ficam estáveis e acima dele. O espaço entre título e subtítulo aumenta para 24 px. O desenho não captura toques, não cria navegação e não escreve progresso. O crédito identifica o recurso a IA e o carácter ilustrativo.

Reutiliza-se `fundos.js/css` sem alterações: ciclo de 36 segundos, paragem após dois ciclos, botão de pausa/retoma, pausa fora de vista e com separador escondido. Movimento reduzido e projeção ficam estáticos. Sem JavaScript há um desenho parado e o botão fica oculto. A impressão omite o desenho.

## Verificações

- Dezoito capturas antes/depois, 320/390/1366 px, claro/escuro/projeção, esperando pelas fontes. Sem deslocamento lateral a 100%. As capturas usam movimento reduzido para permitir comparação estável.
- Vídeo real de movimento, pausa por Enter, retoma e passagem dinâmica à projeção.
- Ensaio reprodutível em `tests/browser_fundo_cidadania.cjs`, com nove contextos, ausência de erros, título estável, armazenamento intacto, alternativa sem JavaScript e impressão. Inclui pausa automática fora de vista.
- Destinos de ligações, identificadores e scripts incorporados idênticos à base. Só se acrescentam as referências aos dois estilos e ao motor comum. A aplicação de `tools/fundo_cidadania_piloto.py` é idempotente.
- A 200% por CSS, o título cabe e o desenho fica contido. A página inteira conserva transbordos anteriores, com as mesmas medidas: 229 px em 320 claro/escuro, 136 px em 320 projeção, 159 px em 390 claro/escuro, 66 px em 390 projeção; zero em 1366 nos três modos. Não se declara aprovação integral da página a 200% nem zoom nativo verificado.

Provas locais: `outputs/cidadania-fundo-provas-20261103/comparacao.html`, capturas, `medidas.json`, `zoom.json` e `movimento-pausa.webm`. A pausa fora de vista está também no ensaio gravado em `comportamento/`.

O piloto aguarda revisão antes de qualquer propagação. Humanos e Decisões ainda não receberam novos fundos. A intenção é dar a cada um um motivo próprio ligado ao conteúdo, conservando a gramática de traço, transparência, pausa e acento discreto. Não se aplica este efeito a todos os cartões. Nada foi publicado.
