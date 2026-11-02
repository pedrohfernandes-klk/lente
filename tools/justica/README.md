# Justiça: bases para treze lições

02/11/2026. Fase 0. Os bancos foram extraídos do HTML publicado, no main `ba946f6`, e não do gerador histórico. Conservam as opções revistas no #72, os endereços, as chaves, a ordem dos cartões, o motor e `?projetar=1`.

## Construir e verificar

```sh
python tools/justica/build.py --verificar
python tools/justica/build.py
python -m unittest discover -s tests -p 'test_justica*.py' -v
node --test tests/resultados_turma.test.cjs
node tests/browser_justica.cjs
```

`licoes.json` declara as lições publicadas: número, chave, vídeo, aulas, anterior, seguinte e estado do molde. `bancos/` contém JSON válido, conservando a serialização publicada para permitir a comparação literal. `moldes/` guarda a casca publicada sem o banco. Para atualizar um cartão, altera-se o banco e regenera-se; nunca se extrai automaticamente uma mudança do HTML por cima dos dados.

`migracao.json` contém as únicas diferenças autorizadas face ao main de partida: o cartão 11 da lição 1 trazido do #90 (cabeça `5c9268c5`), e «um jogo de crianças» para «uma brincadeira de crianças», no cartão 18 da lição 2. O teste desfaz apenas estas duas trocas e exige o SHA-256 do HTML de origem. A lição 3 é idêntica à publicada.

## Citações

`citacoes.json` guarda só as citações curtas usadas nos bancos, com episódio, vídeo, cartão e tempo. Cada entrada tem no máximo duas frases. Quando existe um par explícito de original e tradução, a tradução também consta do manifesto. O teste exige que o manifesto corresponda aos bancos.

As legendas e as transcrições não entram neste repositório, nem no CI. Para conferir localmente, definir `JUSTICA_LEGENDAS` com uma pasta privada e executar:

```sh
python tools/justica/build.py --verificar --legendas
```

São aceites os nomes `ep01.en.vtt` e `ep1.en.vtt`. O programa exige que cada frase exista nas legendas do episódio certo. Esta verificação textual não substitui a conferência audiovisual dos tempos. Os tempos das lições 1 a 3 são os publicados; não se atribuem tempos aos episódios novos sem os conferir.

## Regras e passagem à fase 1

O teto de 26 cartões mantém-se. O validador cobre as palavras proibidas, a pontuação, os retornos, as opções equilibradas e as leituras novas até 95 palavras visíveis, incluindo original e tradução. A única leitura publicada acima do limite é L1 C12, 99 palavras, registada numa lista fechada no teste por decisão do docente de 02/11. Não se admitem novas exceções nem aumentos; a ocorrência sai quando for dividida na fase 1.

O molde novo exige pelo menos 14 atividades, cinco tipos sem escrita, no máximo uma escrita, nunca três atividades seguidas do mesmo tipo, «Na aula», imagem no «Abre», «Olha» logo a seguir e «No fim, consegues». A navegação é lida pelo manifesto; o teste exige índice, anterior e seguinte. Os menus existentes ficam preservados na fase 0.

`desenhos.py` e `desenhos.json` conservam as primitivas do desenho a traço. A tabela de comparação está em `docs/qa/justica-fase0-20261102.md`. O redesenho e as imagens documentais pertencem à fase 1. Nenhuma imagem documental foi acrescentada nesta fase.
