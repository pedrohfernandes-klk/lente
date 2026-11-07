"""07/11/2026: plano do molde da Cidadania, sessão 10 do M1 na versão final, a sessão de mostra (decisões 166 a 168; variante «mostra»
do plano, secção 2). Uma camada por cima da da sessão 08 (tests/molde_s08.py), para os testes que comparam com bases antigas, com as
mesmas regras e sem aceitar mais nada:

- TROCAS: o manifesto fechado tools/trocas/molde-s10-20261107.json, trocas literais [antigo, novo, contagem] nos ficheiros que a
  s10 muda só em parte (a página do módulo do piloto, em que só muda a linha da sessão 10; o guia, em que muda a secção da sessão 10
  e a frase sobre as sessões no molde; o gerador das sessões publicadas, que deixa de escrever a 10; e o gerador da página do módulo,
  do guia e da versão para imprimir, com a entrada da s10 e a forma da sessão de mostra). aplicar() e desfazer() exigem a contagem
  exata, como nas outras camadas.
- INTEIROS: os ficheiros que a s10 escreve inteiros (a página e a versão para imprimir da s10, a sua fonte e o seu .json). Não se
  comparam com a base: comparam-se, letra a letra, com o que o seu gerador escreve hoje (inteiro_ok()), e a s10 tem de cumprir o
  contrato do molde, na sua variante.

O manifesto parte do main dc01487 (com as sessões 01 a 08 finais) e leva a versão do main de cada ficheiro mudado em parte ao ficheiro
de hoje, letra a letra (o gerador conferiu que aplicar e desfazer dão a volta completa). É a camada mais recente: desfaz-se primeiro
no ficheiro atual, antes da da s08, ou aplica-se em último lugar ao lado esperado. A sessão 09 faz-se ao mesmo tempo noutro ramo, a
partir do mesmo main; na fusão, o manifesto gera-se de novo a partir do main que então houver."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TROCAS = json.loads((ROOT / 'tools/trocas/molde-s10-20261107.json').read_text(encoding='utf-8'))
S10 = 'tools/licoes/cidadania-m1-s10'
INTEIROS = ('cidadania/m1/sessoes/10/index.html', 'cidadania/m1/sessoes/10/imprimir/index.html', S10 + '.json', S10 + '.py')


def _modulo(nome, rel):
    spec = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def aplicar(texto, ficheiro):
    for antigo, novo, n in TROCAS.get(ficheiro, []):
        if texto.count(antigo) != n:
            raise AssertionError(('molde, sessão 10', ficheiro, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def desfazer(texto, ficheiro):
    for antigo, novo, n in reversed(TROCAS.get(ficheiro, [])):
        if texto.count(novo) != n:
            raise AssertionError(('molde, sessão 10 (desfazer)', ficheiro, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def inteiro_ok(ficheiro):
    """O ficheiro que a s10 escreve inteiro é exatamente o que o seu gerador escreve (e a s10 cumpre o contrato, na variante «mostra»)."""
    L = _modulo('licoes_lente', 'tools/licoes_lente.py')
    d = json.loads((ROOT / (S10 + '.json')).read_text('utf-8'))
    ok = d.get('molde') == L.MOLDE and d.get('variante') == 'mostra' and L.validar(d) == []
    if ficheiro == 'cidadania/m1/sessoes/10/index.html':
        return ok and (ROOT / ficheiro).read_text('utf-8') == L.pagina(d)
    if ficheiro == 'cidadania/m1/sessoes/10/imprimir/index.html':
        P = _modulo('cidadania_piloto', 'tools/cidadania_piloto.py')
        return ok and (ROOT / ficheiro).read_text('utf-8') == P.paginas()[ficheiro]
    if ficheiro in (S10 + '.json', S10 + '.py'):
        fonte = _modulo('cidadania_m1_s10', S10 + '.py')
        return ok and json.dumps(fonte.sessao(), ensure_ascii=False, indent=1) + '\n' == (ROOT / (S10 + '.json')).read_text('utf-8')
    return False
