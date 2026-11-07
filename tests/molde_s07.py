"""06/11/2026: plano do molde da Cidadania, sessão 07 do M1 na versão final (decisões 166 a 168: as sessões do M1 pelo mesmo molde,
uma de cada vez). Uma camada por cima da da s03 (tests/molde_s03.py), para os testes que comparam com bases antigas, com as mesmas
regras e sem aceitar mais nada:

- TROCAS: o manifesto fechado tools/trocas/molde-s07-20261106.json, trocas literais [antigo, novo, contagem] nos ficheiros que a
  s07 muda só em parte (a página do módulo do piloto, em que só muda a linha da sessão 07; o guia, em que muda a secção da sessão 07
  e a frase sobre as sessões no molde, que passa a sair da lista das sessões; o gerador das sessões publicadas, que deixa de escrever
  a 07; e o gerador da página do módulo e do guia). aplicar() e desfazer() exigem a contagem exata, como em molde_s03.py.
- INTEIROS: os ficheiros que a s07 escreve inteiros (a página e a versão para imprimir da s07, a sua fonte e o seu .json). Não se
  comparam com a base: comparam-se, letra a letra, com o que o seu gerador escreve hoje (inteiro_ok()), e a s07 tem de cumprir o
  contrato do molde.

O manifesto parte do main 88c2cba (com a s03): é a camada mais recente, por cima de todas as outras, também da 163 e da 149 e da
s03. Desfaz-se primeiro no ficheiro atual, ou aplica-se em último lugar ao lado esperado. As sessões 04 a 06, construídas noutros
ramos, juntam-se depois com as suas camadas.

06/11/2026: correções da revisão da s07. O manifesto foi refeito com o mesmo gerador e a mesma base (88c2cba): mudam só as trocas
do guia (GUIA['07'], «a opinião de muitos» e a charneira 2) na página do docente e em tools/cidadania_piloto.py. As regras
de aplicar(), desfazer() e inteiro_ok() não mudam.

06/11/2026 (fusão do main com as sessões 2 a 6 finais na sessão 7): o manifesto foi gerado de novo a partir do main (8731fb9), e
leva a versão do main de cada ficheiro mudado em parte ao ficheiro de hoje, letra a letra (o gerador confere que aplicar e desfazer
dão a volta completa). A s07 fica por cima de todas as camadas, também das da s04, da s05 e da s06 (tests/molde_s04.py a
tests/molde_s06.py): desfaz-se primeiro no ficheiro atual, antes da da s06, ou aplica-se em último lugar ao lado esperado. A frase
das sessões no molde já sai da lista das sessões no main (_frase_molde(), da s04), e sai do manifesto; no guia, a frase passa a
nomear as sessões 01 a 07. As regras e as contagens exatas não mudam."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TROCAS = json.loads((ROOT / 'tools/trocas/molde-s07-20261106.json').read_text(encoding='utf-8'))
S07 = 'tools/licoes/cidadania-m1-s07'
INTEIROS = ('cidadania/m1/sessoes/07/index.html', 'cidadania/m1/sessoes/07/imprimir/index.html', S07 + '.json', S07 + '.py')


def _modulo(nome, rel):
    spec = importlib.util.spec_from_file_location(nome, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def aplicar(texto, ficheiro):
    for antigo, novo, n in TROCAS.get(ficheiro, []):
        if texto.count(antigo) != n:
            raise AssertionError(('molde, sessão 07', ficheiro, antigo[:80]))
        texto = texto.replace(antigo, novo)
    return texto


def desfazer(texto, ficheiro):
    for antigo, novo, n in reversed(TROCAS.get(ficheiro, [])):
        if texto.count(novo) != n:
            raise AssertionError(('molde, sessão 07 (desfazer)', ficheiro, novo[:80]))
        texto = texto.replace(novo, antigo)
    return texto


def inteiro_ok(ficheiro):
    """O ficheiro que a s07 escreve inteiro é exatamente o que o seu gerador escreve (e a s07 cumpre o contrato)."""
    L = _modulo('licoes_lente', 'tools/licoes_lente.py')
    d = json.loads((ROOT / (S07 + '.json')).read_text('utf-8'))
    if ficheiro == 'cidadania/m1/sessoes/07/index.html':
        return (ROOT / ficheiro).read_text('utf-8') == L.pagina(d) and d.get('molde') == L.MOLDE and L.validar(d) == []
    if ficheiro == 'cidadania/m1/sessoes/07/imprimir/index.html':
        P = _modulo('cidadania_piloto', 'tools/cidadania_piloto.py')
        return (ROOT / ficheiro).read_text('utf-8') == P.paginas()[ficheiro]
    if ficheiro in (S07 + '.json', S07 + '.py'):
        fonte = _modulo('cidadania_m1_s07', S07 + '.py')
        return json.dumps(fonte.sessao(), ensure_ascii=False, indent=1) + '\n' == (ROOT / (S07 + '.json')).read_text('utf-8') \
            and d.get('molde') == L.MOLDE and L.validar(d) == []
    return False
