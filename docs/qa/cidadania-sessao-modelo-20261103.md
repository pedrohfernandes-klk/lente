# Cidadania: sessão-modelo para revisão

03/11/2026. Base: #84, `d40fd3f7e27348aa5c0528b84c4d5b5760320fe2`. Demonstração isolada em `demonstracoes/cidadania-sessao-modelo/`, escondida dos motores de busca. Não substitui a sessão 1 existente nem altera o #84.

## O que se ensaia

Uma fotografia partilhada no grupo da turma serve de caso, explicitamente inventado. Os materiais surgem antes das perguntas: fotografia inteira de Eleanor Roosevelt, título transcrito, três excertos da Declaração e apoio escrito a partir do preâmbulo. A conclusão limita-se a três linhas individuais em papel. Não há mapa em post-its, recuperação de Rhythm 0, tarefa escrita durante um vídeo ou vídeo não visionado.

São 20 cartões, 14 de fazer, com cinco tipos já existentes. Os cartões de leitura têm entre 49 e 80 palavras. As alternativas são equilibradas pelo validador existente e cada erro remete para uma prova. As decisões do caso não são apresentadas como vereditos jurídicos.

| Cartões | Material e atividade |
| --- | --- |
| 1 | Caso inventado e pergunta de trabalho |
| 2 a 4 | Fotografia com ampliação; elemento observável; palavras do título |
| 5 a 8 | Excertos dos artigos 1.º, 12.º e 19.º; pares, verdadeiro/falso e prova textual |
| 9 a 13 | Alternativa escrita do preâmbulo; ordem do apoio, meio citado, limite da conclusão e palavras «a atingir» |
| 14 a 19 | Regresso ao caso; dúvida em aberto, provas, ordem da justificação e conclusão limitada |
| 20 | Conclusão provisória, prova e dúvida, em três linhas |

A duração de 180 minutos do plano é uma proposta a ensaiar com a turma, não uma duração demonstrada por estes testes. Não se inventou uma nova grelha com pesos. A integração no guia, a sequência posterior e a redução da oferta dependem da revisão deste modelo.

## Fontes e visor

A fotografia local foi inspecionada: 1000 × 793, título e emblema legíveis; não se exige leitura dos artigos na fotografia. Crédito com fotógrafo não identificado, Lake Success, novembro de 1949, FDR Presidential Library & Museum, 64-165, CC BY 2.0; ligações à publicação institucional e à licença. A pré-verificação documental do GPT2 foi conservada; não se descarregou um original maior.

Os excertos e o apoio foram confrontados com a [transcrição oficial portuguesa do UNRIC](https://unric.org/pt/declaracao-universal-dos-direitos-humanos/), consultada em 03/11/2026. As passagens aparecem identificadas como excertos. O qualificativo «arbitrárias» foi conservado. A alternativa escrita substitui o vídeo TED-Ed, que continua sem visionamento comprovado.

O visor usa os ficheiros `ampliar-documentos.js/css` da entrega do GPT1 no repositório público pt, copiados sem alterações do checkout `pt-conteudos-lote2`. Não foi criado outro motor. Só a demonstração ativa esta inclusão opcional. Confirmados abertura por Enter, ampliação, Escape, fundo inerte e restituição do foco à fotografia.

## Isolamento e verificações

O banco fica em `tools/modelos/`; o gerador mantém o validador existente. O campo `modelo` dá ao ensaio a chave `ensaio-epi-cid-m1-s01`, preservando a chave da sessão publicada. Nenhuma página do percurso anterior foi regenerada ou removida. Não se mudou nenhum teste anterior para acomodar o modelo.

- Seis testes das lições e sete testes do piloto existente: aprovados, incluindo correspondência entre fontes e páginas.
- Três testes novos: banco e página gerada, sequência/material, leitura até 95 palavras, isolamento e visor.
- Percurso completo dos 20 cartões em 320, 390 e 1366 px, com as 14 respostas certas, sem deslocamento lateral; resultado e gravação apenas na chave de ensaio. O registo original semeado antes da visita fica idêntico.
- Projeção nas três larguras: começa no início e não grava progresso.
- Capturas locais dos cartões 1, 2, 5, 9, 14 e 20: `outputs/cidadania-modelo-provas-20261103/`. Foram inspecionadas a fotografia e a leitura dos artigos em telemóvel.

O CI acrescenta uma execução própria do modelo, sem retirar baterias existentes. A revisão pedagógica e a aprovação de integração continuam pendentes. Nada foi publicado.
