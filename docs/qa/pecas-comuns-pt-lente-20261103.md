# Peças comuns de Português e Lente

Proposta para revisão, 03/11/2026. Não autoriza propagação nem publicação. Inventário de Português confirmado no main `e3b4b00fb3990744d6c6eebca18a47b6ba399bde`; Lente publicado `349d2457e1f056b69c6dda550aace2a6f5377051`. O protótipo fica no ramo dos menus, sem alterar o #107 ou o repositório Português.

## O que existe

| Peça | Português | Lente | Decisão para o protótipo |
| --- | --- | --- | --- |
| Resultados | `assets/appearance.css`, `assets/pt-lessons/lesson.css` | `assets/appearance.css`, `assets/licoes/lesson.css` | Os tokens já coincidem; conservar os valores, acrescentar sempre texto e símbolo |
| Movimentos | Entrada lateral de cartão, traço, resposta e outros efeitos no CSS das lições | Base semelhante, com alterações próprias | Não copiar o conjunto inteiro; propor um contrato comum de estados e ensaiá-lo isoladamente |
| Acesso docente | `.teacher-access`, fixo a 12 px da esquerda e do fundo, 44 px | Não existe esse ficheiro no main consultado; apoios distribuídos pelas páginas | Boia inferior esquerda, alvo 48 px, numa faixa reservada que não se sobrepõe à área de respostas |
| Projeção | Ícone com quatro marcas internas, variantes escondidas abaixo de 600 px | Ecrã com linhas internas e controlo circular | Um ecrã com suporte, sem marcas internas; alvo 48 px e nome acessível «Projetar» |
| Porta entre sítios | `assets/site-portals.css` e entradas PT | `.site-portal.portal-portugues`, fotografia de Pessoa e camadas `cartaz-entrada.css` | Uma porta com ação clara, livro e linhas de calçada integrados, sem faixa fotográfica isolada |

## Tokens e estados propostos

| Token | Claro | Escuro |
| --- | --- | --- |
| `--certo` | `#1b7f3b` | `#7fd9bb` |
| `--errado` | `#c8232c` | `#e4555c` |
| `--certo-fundo` | `#e2f3e8` | `#163d30` |
| `--errado-fundo` | `#fbe5e3` | `#4a1f1f` |

Neutro: sem marca de resultado. Escolhido: contorno e `aria-pressed`. Correto: símbolo de confirmação, «Certo» e explicação. Incorreto: cruz, «Ainda não» e orientação para rever. Parcial, quando o motor o permite: palavra «Parcial» e explicação, nunca simular um certo nem usar apenas a cor. Desativado: conservar legibilidade e impedir nova submissão. O protótipo exercita correto/incorreto; os restantes contratos continuam a depender da integração revista nos motores.

Correção de contraste de 03/11: texto e rótulo usam a tinta principal (`--ink` no protótipo, equivalente a `--tinta` nos sítios), sobre o fundo tintado. Verde/vermelho ficam na marca e no símbolo, nunca no texto pequeno. Proposta de movimento comum: desenho vertical da marca, 180 ms, uma vez; texto e controlos não mudam de posição nem de opacidade. Sem abanão de erro, pulsação, prémio ou som novo. Redução de movimento, projeção e impressão: resultado imediato, sem animação. O motor de fundo continua separado, lento, com pausa e dois ciclos. Estes valores são uma proposta nova para ambos os sítios, não uma alegação de que os motores atuais já são iguais.

Ícone único: SVG `viewBox="0 0 24 24"`, retângulo `x=3 y=3 width=18 height=13 rx=1`, suporte `M12 16v5M7 21h10`, traço 1,6, sem preenchimento. `aria-hidden` no SVG; botão com nome acessível, foco visível, alvo mínimo 48 px. Não esconder em móvel. A integração final deve conservar o lançador e os parâmetros reais de projeção; o botão do protótipo só demonstra o modo visual e não substitui o QR.

Boia: docente, guião para imprimir, impressão e apoio contextual. Abrir/fechar por teclado, Escape devolve foco ao botão. No protótipo, o conteúdo principal tem deslocamento próprio acima da faixa inferior, pelo que a boia fechada não tapa controlos a 320/390 px. A abertura dos apoios é explícita. Decisão posterior do docente, 03/11: a boia mantém-se no canto inferior esquerdo também em projeção; imprimir remove os controlos. Os acessos «Para o docente» passam para o interior da boia, conservando os destinos.

## Porta Português e materiais

A porta aparece no percurso do Laboratório, depois dos recursos, sem competir com Ideias. Texto: «Leva a observação para a leitura e para a escrita. Escolhe um dos nove módulos.» Ação: «Entrar em Português». Livro e linhas de calçada retomam leitura/escrita e o motivo já trabalhado em PT. Grafismo SVG identificado como gerado com recurso a IA, EPI, 2026. Não se acrescenta fotografia ou vídeo sem uma atividade concreta e fonte confirmada. Vídeos futuros: poster e crédito locais, botão de arranque explícito, nenhum iframe ou pedido ao fornecedor antes do toque, legendas e alternativa textual verificadas.

Wordle: pesquisa de duplicados sem ocorrências no ramo. Uma ligação compacta na entrada do protótipo, acento discreto, indicação de inglês e de sítio externo, destino original do NYT. Não é banner nem catálogo. Nenhum conteúdo externo é carregado antes do clique.

## Alinhamento

GPT3 recebe esta especificação para comparar e adaptar as peças em Português. Os quatro caminhos reservados do Lente continuam sob responsabilidade do GPT4: `tools/ideias_piloto.py`, `tools/licoes_lente.py`, `tools/laboratorio.py` e `assets/licoes/`. A integração posterior ajusta em `tools/ideias_piloto.py` apenas a largura da tabela do guião em projeção, detetada ao verificar a boia. A propagação requer revisão do percurso e dos contratos de comportamento.
