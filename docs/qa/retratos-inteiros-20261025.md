# Retratos completos nos cartões do Laboratório

25 de outubro de 2026. Base: dce51b094cef8766c5e130fb73c7b4649858e751.

## Problema e alteração

A abertura de «Quem conta?» mostrava sobretudo o chapéu e a testa de uma figura tradicionalmente identificada como Fernão Lopes. O original vertical era forçado a ocupar uma faixa horizontal. O mesmo padrão foi identificado em seis outras páginas.

O lote limita-se às aberturas de `quem-conta`, `dialogo`, `oficina-ator`, `subtexto`, `oficina-dilema`, `querer-agir` e `personagem-faz`. Cada figura recebe a classe `retrato`. Uma regra local conserva a proporção e a imagem completa, centra a moldura e limita a altura a `min(44vh,420px)`. Mantém a ampliação já existente. Não altera os outros cartazes ou recortes editoriais.

Preserva imagens, URLs, texto alternativo, atribuições, legendas, créditos, perguntas, motor, índices, critérios e progresso. A reversão exata da classe e das regras acrescentadas restitui o ficheiro anterior integralmente; verificação executada pelo preparador externo de QA.

## Coordenação

O PR LENTE #38 foi reconfirmado no head b33f21c83e3cf3a6a6ae28facd65253008ff63c8. Nenhuma das sete páginas consta dos seus 141 ficheiros. Os blobs das seis páginas adicionais coincidem com main; a página inicial também fora verificada antes de editar. Não se alteram entradas, geradores, Cartaz, Cidadania ou os recursos de projeção.

O novo PR PT #95 altera os nove mapas. Os problemas encontrados nas galerias de Português ficam como propostas e cópias externas de comparação, sem alterações a esses ficheiros. O responsável pelas fontes deve incorporar estes contratos locais nos geradores antes de voltar a gerar as páginas; não se editou o seu repositório nesta ronda.

## Verificações executadas

- 52 testes Python aprovados depois das sete alterações.
- `git diff --check` aprovado.
- Sete aberturas em navegador real a 1280×800, 390×844 e 320×740: imagens carregadas, proporções naturais conservadas e sem transbordamento horizontal na página.
- Nas sete páginas móveis: abrir imagem ampliada e fechar por Escape.
- Em «Quem conta?»: avançar ao poema e regressar ao cartão inicial.
- Nas sete páginas projetadas: alternar 18/22/28 px, com estado selecionado correto, imagem ampliável e QR presentes. Foram guardadas 21 capturas. A inspeção visual amostral confirma o retrato completo; isto não certifica a legibilidade de todas as informações no projetor físico.
- Comparação antes/depois de «Quem conta?» no mesmo viewport de computador. Capturas e medições externas em `outputs/enquadramentos-20261025`, incluindo `qa-retratos-medidas.json`, `qa-retratos-320.json` e `qa-projecao-retratos.json`.

## Limites e publicação

Não executados neste lote: percurso integral de todas as atividades, leitor de ecrã, impressão, projetor físico, leitura do QR num segundo dispositivo, desempenho medido e integração com o modo noturno ainda experimental. São verificações complementares; o código funcional foi preservado.

As cópias de galeria de Português não estão certificadas: a sessão de navegador foi interrompida durante essa comparação. Não apresentar o diagnóstico estático como correção aplicada.

Lote local, ainda não enviado, integrado ou publicado. A revisão automática do envio anterior atingiu o limite de utilização; aguardar reposição e reconfirmar conflitos antes de enviar, sem recorrer a outra via de escrita para contornar a aprovação. CI e resultado público continuam pendentes.
