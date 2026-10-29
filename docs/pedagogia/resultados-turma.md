# Resultados da turma

28 de outubro de 2026. O docente perguntou se era possível «um login sem utilização de dados» para ver os resultados dos alunos. A resposta não tem servidor nem contas: cada aluno entrega um ficheiro identificado por um código, e o docente lê os ficheiros da turma numa página do sítio, no próprio navegador.

## O que é

- No caderno do Lente (`caderno/#entregar`), a secção «Entregar ao docente»: o aluno escreve o código que o docente lhe deu, vê uma pré-visualização curta (o código, quantos registos, de que percursos e «Não vai o teu nome.») e descarrega `entrega-CÓDIGO-AAAA-MM-DD.json`.
- Na área do docente, a página «Resultados da turma» (`docente/resultados/`): o docente escolhe ou arrasta muitos ficheiros de uma vez e vê uma tabela com uma linha por código e um resumo por percurso, o pormenor de cada código e um botão para descarregar a tabela em CSV.

## Como o docente usa

1. **Dar os códigos.** Um código por aluno, por exemplo `10A-07`: 2 a 12 caracteres, letras de A a Z, algarismos e hífen, com pelo menos um algarismo (o algarismo desencoraja nomes) e pelo menos uma letra, sem hífen no início nem no fim. O caderno recusa os códigos que o Excel e o LibreOffice trocam por números ao abrir o CSV: só com algarismos (`007` passa a 7) e com a forma da notação científica (`10E-07` passa a 0,000001, `11E1` a 110). Na turma E, a letra vai à frente: `E10-07`.
2. **Guardar a lista código e nome fora do sítio**, no computador da escola ou em papel. O sítio nunca vê essa lista.
3. **Pedir as entregas.** Cada aluno abre o caderno, escreve o código e descarrega o ficheiro; envia-o pelo canal combinado na turma (é aí, e não no sítio, que o ficheiro passa pela internet). O código não fica guardado no aparelho: o aluno escreve-o de cada vez.
4. **Abrir a página.** Em «Para o docente», no bloco «03, Acompanhar», em «Entregas do caderno», a ligação «Resultados da turma». Escolher ou arrastar os ficheiros todos. Os recusados aparecem numa lista com a razão e o que pedir ao aluno, sem parar os outros; as listas de avisos e de recusados mostram o último lote. Ordenar pelo código, carregar num código para abrir o pormenor, descarregar o CSV (BOM UTF-8, separador «;», abre no Excel em pt-PT). A coluna Código fica fixa quando a tabela desliza. «Limpar a tabela» ou fechar a página: não fica nada.

## O que vai no ficheiro

`{"formato":"epi-entrega","versao":1,"codigo":"10A-07","data":"<ISO>","origem":"lente/caderno","registos":{…}}`

Os registos são os de «Guardar num ficheiro», filtrados pela lista das chaves aceites: lições, desafios, sínteses e notas dos módulos de Português; exercícios, questionários e trabalhos longos; Atlas; a cidade; sessões e apoios de Cidadania; Ter juízo; Laboratório e Ginásio; percursos transversais; Biblioteca; Ver para fazer; visitas de estudo. Vão também as respostas escritas nos percursos, e a pré-visualização di-lo ao aluno. O pormenor mostra-as só como texto.

## O que não vai

- **Os campos do nome.** As chaves com nome (`cd1-nome`, `terra-firme-…`) e o campo `nome` das respostas antigas de Cidadania (`cd-…`) ficam de fora. A página do docente retira-os também dos ficheiros antigos. As respostas escritas vão como o aluno as escreveu, e um código mal escolhido (um nome com um algarismo, como `ANA1`) passa: o caderno só desencoraja.
- A Sala, desligada a 17/10; o que só serve o aparelho (tema, som, o cartaz que já rodou, letra da projeção, relógio das tarefas e sessões de exame).
- As provas rápidas e os testes, que ficam no aparelho onde se fizeram. Os progressos antigos («Guardar num ficheiro» exporta tudo) trazem-nos, e a página retira-os ao ler.

## Limites

- Os registos são declarados pelo aluno e o ficheiro é texto: um aluno pode alterar o próprio ficheiro, incluindo a data e o código. A tabela serve para acompanhar, não para avaliar. Uma data mais de um dia à frente do relógio do docente aparece como «data no futuro» e nunca substitui outra entrega com o mesmo código.
- Um aparelho partilhado junta numa só entrega o que várias pessoas fizeram nele.
- O progresso digital não certifica o trabalho em papel nem a qualidade de uma resposta.
- Só as sessões de Cidadania (8 que contam no M1, da 03 à 10, porque a 01 e a 02 não têm registo; 10 no M2) e os 18 apoios do M1 aparecem com total; os testes conferem-nos com as pastas. Os outros percursos mostram o que foi feito, sem total, porque os totais mudam quando o percurso muda.

## RGPD

O código é um pseudónimo: só o docente, com a lista que guarda fora do sítio, o liga a um aluno. O sítio não recolhe dados; o progresso fica no aparelho do aluno (no armazenamento local do navegador) até ele o entregar. O ficheiro passa pelo canal que a escola já usa (correio, plataforma), com as regras desse canal. A página do docente lê os ficheiros no navegador, sem os enviar nem guardar.

## Decisões tomadas

- **Guardar e Repor ficam como estavam.** O caderno publicado exporta e repõe todas as chaves, sem lista nem limites: o Repor validado de 17/10 nunca chegou ao Lente. O script dos dois botões fica igual ao publicado; só a frase da secção mudou, para mandar o aluno a «Entregar ao docente» quando quiser mostrar o progresso ao docente. As regras de 17/10 (listas, limites, chaves proibidas a qualquer profundidade) ficam em `assets/progresso-registos.js` e servem a entrega e a página do docente. Publicar o Repor seguro é outra tarefa.
- **Listas corrigidas a 28/10.** Entram as sessões e os apoios de Cidadania (`lente-cidadania-…`), que faltavam; `epi-theme`, `epi-som`, `epi-cartaz` e `pt-relogio:…` ficam no aparelho sem recusar o ficheiro.
- **O código não fica lembrado (revisão de 28/10).** Num aparelho partilhado, o aluno seguinte encontraria o código do anterior e podia entregar com ele, e a entrega dele substituiria a verdadeira na tabela. O caderno só lê o armazenamento, nunca escreve nele.
- **Códigos que o Excel estraga (revisão de 28/10).** À regra do algarismo juntam-se: pelo menos uma letra, sem hífen nas pontas, sem a forma `10E-07`. Testado no LibreOffice (pt-PT, «;», UTF-8): `10E-07`, `12E-03`, `11E1`, `1E5`, `007` e `-1` passam a números; `10A-07`, `E10-07` e `12C-03` ficam como texto.
- **Desafios ganhos antes de 10/10.** Gravados com `vencido: true` (e não `ganho`); a página conta as duas marcas, como o Português.
- **Estrita nas entregas, tolerante nos ficheiros antigos.** Uma entrega com uma chave que o caderno não entrega é recusada. Um «epi-progresso» antigo (do caderno de 16/10 ou da página inicial do Português) leva tudo o que o aparelho tinha: o que não se reconhece fica de fora e conta-se, e a linha aparece «sem código», com o nome do ficheiro (dois ficheiros com o mesmo nome dão duas linhas, a segunda com «(2)»).
- **Duplicados.** Com o mesmo código, fica a entrega mais recente (pela data da entrega, depois pela data do ficheiro, depois pelo nome) e a página avisa numa linha curta. Uma data mais de um dia no futuro (ou nenhuma) nunca ganha a uma data plausível. O mesmo ficheiro escolhido duas vezes também gera aviso.
- **Nada sai do navegador.** A página do docente tem `connect-src 'none'` e `form-action 'none'` na política de segurança, não usa armazenamento local e não leva o lançador da projeção. Tudo o que vem dos ficheiros entra na página por `textContent`.
- **A seguir, fora deste repositório.** O caderno é gerado nas fontes (`web.mjs` e `progresso.mjs`): a entrega tem de ser espelhada lá antes da próxima publicação a partir das fontes. Publicar o Repor validado de 17/10 continua por fazer.

## Ficheiros e testes

- `caderno/index.html`: a secção «Entregar ao docente» e a frase de «O teu progresso» que manda o aluno para ela.
- `docente/index.html`: a ligação, em «Entregas do caderno», dentro de «03, Acompanhar» (com o subtítulo em `assets/docente-hub.css`).
- `docente/resultados/index.html`, `assets/resultados-turma.js` e `assets/resultados-turma.css`: a página do docente.
- `assets/progresso-registos.js`: as regras comuns (listas, limites, código, entrega, leitura dos ficheiros), sem DOM, sem armazenamento e sem rede.
- `assets/caderno-entrega.js`: o código, a pré-visualização e a descarga no caderno.
- `tests/test_resultados_turma.py`: estrutura, escrita, noindex e política de segurança, nenhuma chamada de rede, ligação no hub, Guardar e Repor iguais ao publicado (conferidos por sha256, sem precisar do histórico git), totais conferidos com as pastas. `python3 -B -m unittest tests.test_resultados_turma`
- `tests/resultados_turma.test.cjs`: código, chaves, entrega, leitura dos ficheiros (proibidas, limites, conteúdo), resumo, CSV, duplicados e ordem. `node --test tests/resultados_turma.test.cjs`
- `tests/browser_resultados_turma.cjs`: o fluxo do aluno e o do docente no Chromium, ficheiros maliciosos, CSV, largar ficheiros, zero pedidos fora da origem local, nada guardado, de 320 a 1440 px nos dois temas. `RT_OUT=<pasta> node tests/browser_resultados_turma.cjs`
