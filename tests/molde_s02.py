"""06/11/2026: plano do molde da Cidadania, sessão 02 do M1 na versão final (decisão 166: as outras 19 sessões pelo mesmo molde,
uma de cada vez). Uma camada por cima da do pedido 2 (tests/molde_pedido2.py), para os testes que comparam com bases antigas, com
as mesmas regras e sem aceitar mais nada:

- TROCAS: o manifesto fechado tools/trocas/molde-s02-20261106.json, trocas literais [antigo, novo, contagem] nos ficheiros que a
  s02 muda só em parte (a página do módulo do piloto, em que só muda a linha da sessão 02; o guia, em que muda a secção da sessão 02
  e a frase sobre as sessões no molde; o gerador das sessões publicadas, que deixa de escrever a 02; e o gerador da página do módulo
  e do guia). aplicar() e desfazer() exigem a contagem exata, como em molde_pedido2.py.
- INTEIROS: os ficheiros que a s02 escreve inteiros (a página e a versão para imprimir da s02, a sua fonte e o seu .json). Não se
  comparam com a base: comparam-se, letra a letra, com o que o seu gerador escreve hoje (inteiro_ok()), e a s02 tem de cumprir o
  contrato do molde.

É a camada mais recente: desfaz-se antes da do pedido 2 e aplica-se depois dela."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TROCAS = json.loads((ROOT / 'tools/trocas/molde-s02-20261106.json').read_text(encoding='utf-8'))
S02 = 'tools/licoes/cidadania-m1-s02'
INTEIROS = ('cidadania/m1/sessoes/02/index.html', 'cidadania/m1/sessoes/02/imprimir/index.html', S02 + '.json', S02 + '.py')


def _modulo(nome, rel):
    spec = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def aplicar(texto, ficheiro):
    for antigo, novo, n in TROCAS.get(ficheiro, []):
        if texto.count(antigo) != n:
            raise AssertionError(('molde, sessão 02', ficheiro, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def desfazer(texto, ficheiro):
    for antigo, novo, n in reversed(TROCAS.get(ficheiro, [])):
        if texto.count(novo) != n:
            raise AssertionError(('molde, sessão 02 (desfazer)', ficheiro, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def inteiro_ok(ficheiro):
    """O ficheiro que a s02 escreve inteiro é exatamente o que o seu gerador escreve (e a s02 cumpre o contrato)."""
    L = _modulo('licoes_lente', 'tools/licoes_lente.py')
    d = json.loads((ROOT / (S02 + '.json')).read_text('utf-8'))
    if ficheiro == 'cidadania/m1/sessoes/02/index.html':
        return (ROOT / ficheiro).read_text('utf-8') == L.pagina(d) and d.get('molde') == L.MOLDE and L.validar(d) == []
    if ficheiro == 'cidadania/m1/sessoes/02/imprimir/index.html':
        P = _modulo('cidadania_piloto', 'tools/cidadania_piloto.py')
        return (ROOT / ficheiro).read_text('utf-8') == P.paginas()[ficheiro]
    if ficheiro in (S02 + '.json', S02 + '.py'):
        fonte = _modulo('cidadania_m1_s02', S02 + '.py')
        return json.dumps(fonte.sessao(), ensure_ascii=False, indent=1) + '\n' == (ROOT / (S02 + '.json')).read_text('utf-8') \
            and d.get('molde') == L.MOLDE and L.validar(d) == []
    return False
