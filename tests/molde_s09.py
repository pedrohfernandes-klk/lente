"""07/11/2026: plano do molde da Cidadania, sessão 09 do M1 na versão final (decisões 166 a 168 e 174: as sessões do M1 pelo mesmo
molde, uma de cada vez; a 09 faz-se a partir do main dc01487, com as sessões 01 a 08 finais, enquanto a 10 se faz noutro ramo). Uma
camada por cima da da sessão 08 (tests/molde_s08.py), para os testes que comparam com bases antigas, com as mesmas regras e sem aceitar
mais nada:

- TROCAS: o manifesto fechado tools/trocas/molde-s09-20261107.json, trocas literais [antigo, novo, contagem] nos ficheiros que a
  s09 muda só em parte (a página do módulo do piloto, em que só muda a linha da sessão 09; o guia, em que muda a secção da sessão 09
  e a frase sobre as sessões no molde; o gerador das sessões publicadas, que deixa de escrever a 09; e o gerador da página do módulo
  e do guia). aplicar() e desfazer() exigem a contagem exata, como nas camadas das sessões 03 a 08.
- INTEIROS: os ficheiros que a s09 escreve inteiros (a página e a versão para imprimir da s09, a sua fonte e o seu .json). Não se
  comparam com a base: comparam-se, letra a letra, com o que o seu gerador escreve hoje (inteiro_ok()), e a s09 tem de cumprir o
  contrato do molde.

O manifesto parte do main dc01487 (com as sessões 01 a 08 finais) e leva a versão do main de cada ficheiro mudado em parte ao ficheiro de
hoje, letra a letra (o gerador confere que aplicar e desfazer dão a volta completa). É a camada mais recente: desfaz-se primeiro no
ficheiro atual, antes da da s08, ou aplica-se em último lugar ao lado esperado. A única mudança da s09 numa sessão anterior é o
«seguinte» da 08, que passa a ../09/; a página, a fonte e o .json da 08 são INTEIROS da camada da s08 e conferem-se com o gerador."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TROCAS = json.loads((ROOT / 'tools/trocas/molde-s09-20261107.json').read_text(encoding='utf-8'))
S09 = 'tools/licoes/cidadania-m1-s09'
INTEIROS = ('cidadania/m1/sessoes/09/index.html', 'cidadania/m1/sessoes/09/imprimir/index.html', S09 + '.json', S09 + '.py')


def _modulo(nome, rel):
    spec = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def aplicar(texto, ficheiro):
    for antigo, novo, n in TROCAS.get(ficheiro, []):
        if texto.count(antigo) != n:
            raise AssertionError(('molde, sessão 09', ficheiro, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def desfazer(texto, ficheiro):
    for antigo, novo, n in reversed(TROCAS.get(ficheiro, [])):
        if texto.count(novo) != n:
            raise AssertionError(('molde, sessão 09 (desfazer)', ficheiro, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def inteiro_ok(ficheiro):
    """O ficheiro que a s09 escreve inteiro é exatamente o que o seu gerador escreve (e a s09 cumpre o contrato)."""
    L = _modulo('licoes_lente', 'tools/licoes_lente.py')
    d = json.loads((ROOT / (S09 + '.json')).read_text('utf-8'))
    if ficheiro == 'cidadania/m1/sessoes/09/index.html':
        return (ROOT / ficheiro).read_text('utf-8') == L.pagina(d) and d.get('molde') == L.MOLDE and L.validar(d) == []
    if ficheiro == 'cidadania/m1/sessoes/09/imprimir/index.html':
        P = _modulo('cidadania_piloto', 'tools/cidadania_piloto.py')
        return (ROOT / ficheiro).read_text('utf-8') == P.paginas()[ficheiro]
    if ficheiro in (S09 + '.json', S09 + '.py'):
        fonte = _modulo('cidadania_m1_s09', S09 + '.py')
        return json.dumps(fonte.sessao(), ensure_ascii=False, indent=1) + '\n' == (ROOT / (S09 + '.json')).read_text('utf-8') \
            and d.get('molde') == L.MOLDE and L.validar(d) == []
    return False
