"""06/11/2026: plano do molde da Cidadania, sessão 04 do M1 na versão final (decisões 166 a 168: as sessões do M1 pelo mesmo molde,
uma de cada vez). Uma camada por cima da da sessão 02 (tests/molde_s02.py) e da do pedido 2 (tests/molde_pedido2.py), para os testes
que comparam com bases antigas, com as mesmas regras e sem aceitar mais nada:

- TROCAS: o manifesto fechado tools/trocas/molde-s04-20261106.json, trocas literais [antigo, novo, contagem] nos ficheiros que a
  s04 muda só em parte (a página do módulo do piloto, em que só muda a linha da sessão 04; o guia, em que muda a secção da sessão 04
  e a frase sobre as sessões no molde, agora tirada da lista das sessões; o gerador das sessões publicadas, que deixa de escrever a
  04; e o gerador da página do módulo e do guia). aplicar() e desfazer() exigem a contagem exata, como em molde_pedido2.py.
- INTEIROS: os ficheiros que a s04 escreve inteiros (a página e a versão para imprimir da s04, a sua fonte e o seu .json). Não se
  comparam com a base: comparam-se, letra a letra, com o que o seu gerador escreve hoje (inteiro_ok()), e a s04 tem de cumprir o
  contrato do molde.

É a camada mais recente: desfaz-se antes da da sessão 02 e aplica-se depois dela.

06/11/2026 (fusão do main com as sessões 2 e 3 finais, os menus da decisão 163 e o «Dilemas» da decisão 149): o manifesto foi gerado
de novo a partir do main (ba5211f), e leva a versão do main de cada ficheiro mudado em parte ao ficheiro de hoje, letra a letra (o
gerador confere que aplicar e desfazer dão a volta completa). A s04 fica por cima de todas as camadas, também da da sessão 03
(tests/molde_s03.py): desfaz-se primeiro no ficheiro atual, antes da da s03, ou aplica-se em último lugar ao lado esperado."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TROCAS = json.loads((ROOT / 'tools/trocas/molde-s04-20261106.json').read_text(encoding='utf-8'))
S04 = 'tools/licoes/cidadania-m1-s04'
INTEIROS = ('cidadania/m1/sessoes/04/index.html', 'cidadania/m1/sessoes/04/imprimir/index.html', S04 + '.json', S04 + '.py')


def _modulo(nome, rel):
    spec = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def aplicar(texto, ficheiro):
    for antigo, novo, n in TROCAS.get(ficheiro, []):
        if texto.count(antigo) != n:
            raise AssertionError(('molde, sessão 04', ficheiro, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def desfazer(texto, ficheiro):
    for antigo, novo, n in reversed(TROCAS.get(ficheiro, [])):
        if texto.count(novo) != n:
            raise AssertionError(('molde, sessão 04 (desfazer)', ficheiro, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def inteiro_ok(ficheiro):
    """O ficheiro que a s04 escreve inteiro é exatamente o que o seu gerador escreve (e a s04 cumpre o contrato)."""
    L = _modulo('licoes_lente', 'tools/licoes_lente.py')
    d = json.loads((ROOT / (S04 + '.json')).read_text('utf-8'))
    if ficheiro == 'cidadania/m1/sessoes/04/index.html':
        return (ROOT / ficheiro).read_text('utf-8') == L.pagina(d) and d.get('molde') == L.MOLDE and L.validar(d) == []
    if ficheiro == 'cidadania/m1/sessoes/04/imprimir/index.html':
        P = _modulo('cidadania_piloto', 'tools/cidadania_piloto.py')
        return (ROOT / ficheiro).read_text('utf-8') == P.paginas()[ficheiro]
    if ficheiro in (S04 + '.json', S04 + '.py'):
        fonte = _modulo('cidadania_m1_s04', S04 + '.py')
        return json.dumps(fonte.sessao(), ensure_ascii=False, indent=1) + '\n' == (ROOT / (S04 + '.json')).read_text('utf-8') \
            and d.get('molde') == L.MOLDE and L.validar(d) == []
    return False
