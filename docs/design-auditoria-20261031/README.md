# Cartaz: auditoria e biblioteca de peças

31/10/2026. GPT3. Fase 1. **Rascunho para decisão, não fundir.**

- [Relatório completo, com tabelas e capturas](relatorio.html)
- [Versão das tabelas para leitura no GitHub](relatorio.md)
- [Biblioteca visual: doze peças e estados](proposta/biblioteca.html)
- [Proposta CSS aditiva, sem aplicação aos sítios](proposta/appearance.css)
- [24 URLs e identificação das páginas](paginas.json)
- [Medidas de base](medidas/) e [provas complementares](provas/)

O relatório HTML abre localmente num navegador. As capturas e as tabelas Markdown podem ser revistas diretamente neste ramo. Não é necessário publicar o documento nos sítios.

240 capturas de base: 24 páginas × cinco larguras × dois temas. Comparação principal a 390 e 1366 px; inspeção complementar a 320, 1024 e 1440 px. Abertura e um cartão seguinte nas três lições escolhidas. Projeção com o parâmetro disponível. Pranchas antes/depois identificadas como estudos parciais, sem prova de redução da altura da página completa.

As únicas adições estão nesta pasta. Sem alterações à barra, às páginas, a assets/appearance.css, a geradores ou a testes. O CSS desta pasta é uma amostra documental opt-in.

## Decisão 54 já aprovada

A primeira porta chama-se **Observar**: Observar, Treinar, Criar. Propostas e biblioteca atualizadas; capturas anteriores preservadas como prova. A equipa da barra comum aplica os rótulos visíveis. Mantêm-se `narrativas/ver/`, âncoras e progresso.

## Decisão pedida

Aprovar ou ajustar D1 a D6 no relatório: ligações, retoma, escala de espaço, estados, dobras e exceções de identidade. Depois da ronda, fechar este pedido sem o fundir. A fase 2 só começa após decisão explícita.

## Reproduzir

Colocar os dois repositórios lado a lado, com os nomes pt e lente. Instalar ou indicar Playwright através de PLAYWRIGHT_MODULE; indicar CHROME_PATH se o Chromium não estiver no caminho habitual. Os programas usam contextos descartáveis e um servidor local na porta 8873.

```text
node ferramentas/capturar.cjs
python ferramentas/documentar.py
node ferramentas/complementar.cjs
python ferramentas/relatorio.py
```

Executar os comandos a partir desta pasta. As versões auditadas estão identificadas no relatório. A repetição sobre outro commit é outra recolha, não substitui a evidência desta ronda.
