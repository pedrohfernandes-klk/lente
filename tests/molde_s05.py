"""06/11/2026: plano do molde da Cidadania, sessão 05 do M1 na versão final (decisões 166 a 168: as sessões do M1 pelo mesmo
molde, uma de cada vez). Uma camada por cima das do pedido 2 e da s02 (tests/molde_pedido2.py, tests/molde_s02.py), para os testes
que comparam com bases antigas, com as mesmas regras e sem aceitar mais nada:

- TROCAS: o manifesto fechado tools/trocas/molde-s05-20261106.json, trocas literais [antigo, novo, contagem] nos ficheiros que a
  s05 muda só em parte (a página do módulo do piloto, em que só muda a linha da sessão 05; o guia, em que muda a secção da sessão 05
  e a frase sobre as sessões no molde; o gerador das sessões publicadas, que deixa de escrever a 05; e o gerador da página do módulo
  e do guia, que ganha o completar no guia e na versão para imprimir). aplicar() e desfazer() exigem a contagem exata, como em
  molde_pedido2.py.
- INTEIROS: os ficheiros que a s05 escreve inteiros (a página e a versão para imprimir da s05, a sua fonte e o seu .json). Não se
  comparam com a base: comparam-se, letra a letra, com o que o seu gerador escreve hoje (inteiro_ok()), e a s05 tem de cumprir o
  contrato do molde.

É a camada mais recente: desfaz-se antes das da s02 e do pedido 2 e aplica-se depois delas."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TROCAS = json.loads((ROOT / 'tools/trocas/molde-s05-20261106.json').read_text(encoding='utf-8'))
S05 = 'tools/licoes/cidadania-m1-s05'
INTEIROS = ('cidadania/m1/sessoes/05/index.html', 'cidadania/m1/sessoes/05/imprimir/index.html', S05 + '.json', S05 + '.py')


def _modulo(nome, rel):
    spec = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def aplicar(texto, ficheiro):
    for antigo, novo, n in TROCAS.get(ficheiro, []):
        if texto.count(antigo) != n:
            raise AssertionError(('molde, sessão 05', ficheiro, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def desfazer(texto, ficheiro):
    for antigo, novo, n in reversed(TROCAS.get(ficheiro, [])):
        if texto.count(novo) != n:
            raise AssertionError(('molde, sessão 05 (desfazer)', ficheiro, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def inteiro_ok(ficheiro):
    """O ficheiro que a s05 escreve inteiro é exatamente o que o seu gerador escreve (e a s05 cumpre o contrato)."""
    L = _modulo('licoes_lente', 'tools/licoes_lente.py')
    d = json.loads((ROOT / (S05 + '.json')).read_text('utf-8'))
    if ficheiro == 'cidadania/m1/sessoes/05/index.html':
        return (ROOT / ficheiro).read_text('utf-8') == L.pagina(d) and d.get('molde') == L.MOLDE and L.validar(d) == []
    if ficheiro == 'cidadania/m1/sessoes/05/imprimir/index.html':
        P = _modulo('cidadania_piloto', 'tools/cidadania_piloto.py')
        return (ROOT / ficheiro).read_text('utf-8') == P.paginas()[ficheiro]
    if ficheiro in (S05 + '.json', S05 + '.py'):
        fonte = _modulo('cidadania_m1_s05', S05 + '.py')
        return json.dumps(fonte.sessao(), ensure_ascii=False, indent=1) + '\n' == (ROOT / (S05 + '.json')).read_text('utf-8') \
            and d.get('molde') == L.MOLDE and L.validar(d) == []
    return False
