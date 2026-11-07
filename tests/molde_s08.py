"""06/11/2026: plano do molde da Cidadania, sessão 08 do M1 na versão final (decisões 166 a 168: as sessões do M1 pelo mesmo molde,
uma de cada vez; a 08 faz-se fora de ordem, enquanto as 04 a 07 se fazem e publicam pelos seus ramos). Uma camada por cima da da
sessão 03 (tests/molde_s03.py), para os testes que comparam com bases antigas, com as mesmas regras e sem aceitar mais nada:

- TROCAS: o manifesto fechado tools/trocas/molde-s08-20261106.json, trocas literais [antigo, novo, contagem] nos ficheiros que a
  s08 muda só em parte (a página do módulo do piloto, em que só muda a linha da sessão 08; o guia, em que muda a secção da sessão 08
  e a frase sobre as sessões no molde; o gerador das sessões publicadas, que deixa de escrever a 08; e o gerador da página do módulo
  e do guia). aplicar() e desfazer() exigem a contagem exata, como na camada da sessão 03.
- INTEIROS: os ficheiros que a s08 escreve inteiros (a página e a versão para imprimir da s08, a sua fonte e o seu .json). Não se
  comparam com a base: comparam-se, letra a letra, com o que o seu gerador escreve hoje (inteiro_ok()), e a s08 tem de cumprir o
  contrato do molde.

O manifesto parte do main 88c2cba (com as sessões 01 a 03 finais, os menus da decisão 163, o «Dilemas» da decisão 149 e o elétrico da
Justiça) e leva a versão do main de cada ficheiro mudado em parte ao ficheiro de hoje, letra a letra (o gerador confere que aplicar e
desfazer dão a volta completa). É a camada mais recente: desfaz-se primeiro no ficheiro atual, ou aplica-se em último lugar ao lado
esperado. Quando as sessões 04 a 07 entrarem no main, o manifesto gera-se de novo a partir desse main.

06/11/2026 (fusão do main com as sessões 2 a 7 finais na sessão 8): o manifesto foi gerado de novo a partir do main (3c774cb), e
leva a versão do main de cada ficheiro mudado em parte ao ficheiro de hoje, letra a letra (o gerador confere que aplicar e desfazer
dão a volta completa). A s08 fica por cima de todas as camadas, também das da s04 à s07 (tests/molde_s04.py a tests/molde_s07.py):
desfaz-se primeiro no ficheiro atual, antes da da s07, ou aplica-se em último lugar ao lado esperado. A frase das sessões no molde e
os seus ajudantes (_frase_molde() e NUMEROS, que o main já tem, iguais) saem do manifesto; no guia, a frase passa a nomear as sessões
01 a 08. Fica também no guia a frase da decisão 172 na nota sobre Hondt. As regras e as contagens exatas não mudam."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TROCAS = json.loads((ROOT / 'tools/trocas/molde-s08-20261106.json').read_text(encoding='utf-8'))
S08 = 'tools/licoes/cidadania-m1-s08'
INTEIROS = ('cidadania/m1/sessoes/08/index.html', 'cidadania/m1/sessoes/08/imprimir/index.html', S08 + '.json', S08 + '.py')


def _modulo(nome, rel):
    spec = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def aplicar(texto, ficheiro):
    for antigo, novo, n in TROCAS.get(ficheiro, []):
        if texto.count(antigo) != n:
            raise AssertionError(('molde, sessão 08', ficheiro, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def desfazer(texto, ficheiro):
    for antigo, novo, n in reversed(TROCAS.get(ficheiro, [])):
        if texto.count(novo) != n:
            raise AssertionError(('molde, sessão 08 (desfazer)', ficheiro, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def inteiro_ok(ficheiro):
    """O ficheiro que a s08 escreve inteiro é exatamente o que o seu gerador escreve (e a s08 cumpre o contrato)."""
    L = _modulo('licoes_lente', 'tools/licoes_lente.py')
    d = json.loads((ROOT / (S08 + '.json')).read_text('utf-8'))
    if ficheiro == 'cidadania/m1/sessoes/08/index.html':
        return (ROOT / ficheiro).read_text('utf-8') == L.pagina(d) and d.get('molde') == L.MOLDE and L.validar(d) == []
    if ficheiro == 'cidadania/m1/sessoes/08/imprimir/index.html':
        P = _modulo('cidadania_piloto', 'tools/cidadania_piloto.py')
        return (ROOT / ficheiro).read_text('utf-8') == P.paginas()[ficheiro]
    if ficheiro in (S08 + '.json', S08 + '.py'):
        fonte = _modulo('cidadania_m1_s08', S08 + '.py')
        return json.dumps(fonte.sessao(), ensure_ascii=False, indent=1) + '\n' == (ROOT / (S08 + '.json')).read_text('utf-8') \
            and d.get('molde') == L.MOLDE and L.validar(d) == []
    return False
