"""05/11/2026: plano do molde da Cidadania, pedido 2 (a sessão 01 do M1 na versão final). Uma camada por cima do pedido 1,
para os testes que comparam com bases antigas, com as mesmas regras e sem aceitar mais nada:

- TROCAS: o manifesto fechado tools/trocas/molde-pedido2-20261105.json, trocas literais [antigo, novo, contagem] nos ficheiros
  que o pedido 2 muda só em parte (o gerador das sessões publicadas, que deixa de escrever a 01; o da página do módulo e do guia;
  a página do módulo, em que só muda a linha da sessão 01; e o guia, em que só muda a secção da sessão 01 e uma frase).
  aplicar() e desfazer() exigem a contagem exata, como em grupos146.py.
- INTEIROS: os ficheiros que o pedido 2 escreve inteiros. Não se comparam com a base: comparam-se, letra a letra, com o que o
  seu gerador escreve hoje (inteiro_ok()), e a fonte da sessão tem de ser a do .json e cumprir o contrato do molde.

06/11/2026 (correções da revisão da s01): as correções mudam texto dentro das trocas que o pedido 2 já tinha (a secção da sessão 01
no guia e no seu gerador, a frase do guia sobre a s01, a versão para imprimir). O «novo» dessas seis trocas passou ao texto
corrigido; o «antigo» e as contagens ficam iguais, e desfazer o ficheiro de hoje dá, letra a letra, a mesma base que antes."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TROCAS = json.loads((ROOT / 'tools/trocas/molde-pedido2-20261105.json').read_text(encoding='utf-8'))
S01 = 'tools/licoes/cidadania-m1-s01'
INTEIROS = ('cidadania/m1/sessoes/01/index.html', 'cidadania/m1/sessoes/01/imprimir/index.html', S01 + '.json', S01 + '.py')


def _modulo(nome, rel):
    spec = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def aplicar(texto, ficheiro):
    for antigo, novo, n in TROCAS.get(ficheiro, []):
        if texto.count(antigo) != n:
            raise AssertionError(('molde, pedido 2', ficheiro, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def desfazer(texto, ficheiro):
    for antigo, novo, n in reversed(TROCAS.get(ficheiro, [])):
        if texto.count(novo) != n:
            raise AssertionError(('molde, pedido 2 (desfazer)', ficheiro, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def inteiro_ok(ficheiro):
    """O ficheiro que o pedido 2 escreve inteiro é exatamente o que o seu gerador escreve (e a s01 cumpre o contrato)."""
    L = _modulo('licoes_lente', 'tools/licoes_lente.py')
    d = json.loads((ROOT / (S01 + '.json')).read_text('utf-8'))
    if ficheiro == 'cidadania/m1/sessoes/01/index.html':
        return (ROOT / ficheiro).read_text('utf-8') == L.pagina(d) and d.get('molde') == L.MOLDE and L.validar(d) == []
    if ficheiro == 'cidadania/m1/sessoes/01/imprimir/index.html':
        P = _modulo('cidadania_piloto', 'tools/cidadania_piloto.py')
        return (ROOT / ficheiro).read_text('utf-8') == P.paginas()[ficheiro]
    if ficheiro in (S01 + '.json', S01 + '.py'):
        fonte = _modulo('cidadania_m1_s01', S01 + '.py')
        return json.dumps(fonte.sessao(), ensure_ascii=False, indent=1) + '\n' == (ROOT / (S01 + '.json')).read_text('utf-8') \
            and d.get('molde') == L.MOLDE and L.validar(d) == []
    return False
