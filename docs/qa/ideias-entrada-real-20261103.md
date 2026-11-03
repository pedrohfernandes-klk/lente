# Ideias no Laboratório real

Continuação sequencial do #108, a partir de `167a941c9ee6b2f6b8211c4d79cbe25e5bf3b13f`. Cumpre o pedido do docente de 3/11: Ideias é o eixo; Observar, Treinar e Criar são recursos. Não altera a cabeça do #108 nem publica.

## Implementação

- O cartão do Lente apresenta Ideias e uma ação principal. Os três recursos perdem a numeração concorrente. Destinos anteriores conservados.
- `narrativas/` abre com Ideias, uma frase e uma ação. O índice do curso reúne as sessões; as alternativas sem JavaScript continuam disponíveis.
- Começar, Continuar e Rever resultam das chaves existentes das sessões publicadas. A conclusão anterior também conta. Não há escrita de registos nesta entrada; em projeção não se lê o progresso pessoal.
- Explorar passa à página real: onze ligações aprovadas, cinco categorias, três destaques, sem repetir os destinos nem incorporar aplicações externas.
- A porta Português conserva o destino aprovado e o grafismo com crédito de recurso a IA.
- Nas duas sessões publicadas, a boia dá acesso ao recurso próprio. O recurso real abre num painel, mantendo a sessão montada; o regresso conserva a resposta e a posição. Escape e o botão devolvem o foco. O recurso incorporado usa o modo sem registo dos visores existentes; abrir o apoio não marca o recurso como concluído. Abrir a ligação separadamente continua possível.
- Nenhuma alteração aos bancos, ao motor dos exercícios, às chaves, à Justiça, ao cabeçalho Lente ou às animações comuns.

## Geração e contratos

`python tools/laboratorio_ideias_entrada.py` atualiza o cartão da raiz, de forma idempotente. `python tools/laboratorio.py --cartaz-entradas` regenera as quatro entradas. Os ficheiros comuns novos ficam fora da pasta fechada das imagens de Ideias.

O manifesto de comparação integral da raiz recebe duas substituições fechadas, cada uma com contagem exatamente um: cartão do Laboratório e carregamento dos novos recursos. Mantém-se a comparação do ficheiro inteiro. O contrato da navegação exige agora o rótulo exato «Recursos». O teste do cartão exige Ideias como título, exatamente três recursos na ordem anterior, uma ação principal e ausência de números concorrentes. Não se removem verificações de destinos ou de dados de progresso.

## Verificação

- 24 entradas: duas páginas, 320/390/1366 px, claro/escuro, normal/projeção; início, retoma e conclusão com chaves reais.
- Regresso do recurso à resposta e posição conservadas a 320 e 1366 px, sem alteração do armazenamento.
- 72 contextos dos quatro menus, incluindo detalhes abertos, teclado e ampliação por CSS.
- 48 vistas dos quatro menus a 200% de zoom nativo, em claro/escuro e projeção real. Calibração: 1350 para 675 px úteis; DPR 1 para 2; zoom CSS e escala visual iguais a um. Perfis temporários, sem controlo interativo do computador.
- Preservação das ligações, âncoras, navegação e dados das quatro entradas; instalação idempotente; catálogo externo sem duplicados.
- Capturas da entrada a 320 px, da raiz e do apoio Galileu a 320 px inspecionadas.

Provas locais: `outputs/ideias-real-20261103/`, `outputs/ideias-real-menus-20261103/` e `outputs/ideias-real-zoom-nativo-20261103/`. O teste novo de navegador integra a verificação automática de Cartaz.

### Regressão completa após o primeiro envio

O CI encontrou um contrato que ainda esperava o título antigo. A revisão das restantes provas encontrou também um tamanho de letra insuficiente nos novos blocos em projeção. Corrigiu-se o CSS para respeitar o mínimo de 18 px; o teste do mínimo mantém-se intacto.

O controlo oculto da continuação dos recursos foi conservado para o motor e para os registos antigos. A ação principal visível continua a ser Ideias. O carregamento da retoma tem agora um sinal explícito de conclusão; os testes esperam por esse sinal, mantendo todas as verificações dos estados antigos e do armazenamento.

Passaram as quatro baterias repetidas: `browser_formas.cjs`, `browser_lab_percursos.cjs`, `browser_ideias_publico.cjs` e `browser_cartaz_familia.cjs`. Incluem 23 páginas do Laboratório, entrada pública nos dois temas e projeção, percursos completos, impressão, ausência de JavaScript, mínimos de leitura e conservação do progresso. Os contratos de títulos e destinos exigem exatamente a nova estrutura; não usam alternativas que aceitem a antiga.

## Limites

Só estão publicadas duas sessões de Ideias. Esta alteração não apresenta as restantes como concluídas. As aplicações externas não foram ensaiadas integralmente. A integração real de Cidadania é uma entrega distinta: os dez pilotos do M1 e a sessão revista do #110 não equivalem à conversão das vinte sessões principais.

### Correções das verificações automáticas de 03/11

O verificador `tools/ideias_publico.py --verificar` ainda procurava a lista antiga da raiz. Passa a usar a transformação idempotente da entrada atual, mantendo a comparação integral e a verificação da ligação na oficina.

Os títulos de Ideias e dos dois blocos novos usavam 60,8 e 24 px, fora da escala comum. Passam a usar os tokens de 61 e 25 px; os títulos dos recursos em projeção usam o token de 20 px. Nenhum teste foi alterado nesta correção.

Passaram o verificador de geração, a hierarquia R1 a R5 em seis páginas, dois tamanhos, dois temas, normal/projeção e dobras abertas/fechadas, e as 24 entradas com início, conclusão e dois regressos à resposta conservada. Provas adicionais: `outputs/ideias-real-ci-20261103/`.
